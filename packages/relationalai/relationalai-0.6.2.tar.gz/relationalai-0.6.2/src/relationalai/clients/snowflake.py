# pyright: reportUnusedExpression=false
from __future__ import annotations
import base64
import decimal
import importlib.resources
from numbers import Number
import re
import json
import time
import textwrap
import ast
import uuid
import warnings

import snowflake.snowpark

from relationalai.rel_utils import sanitize_identifier
from relationalai.tools.constants import SNOWFLAKE_AUTHS, USE_GRAPH_INDEX
from .. import std
from collections import defaultdict
import requests
import snowflake.connector
import pyarrow as pa

from snowflake.snowpark import Session
from snowflake.snowpark.context import get_active_session
from . import result_helpers
from .. import debugging
from typing import Any, Dict, Iterable, Tuple, List, Literal, cast

from pandas import DataFrame

from ..tools.cli_controls import SpanSpinner, Spinner
from ..clients.types import AvailableModel, EngineState, Import, ImportSource, ImportSourceTable, ImportsStatus, SourceInfo, TransactionAsyncResponse
from ..clients.config import Config
from ..clients.client import Client, ExportParams, ProviderBase, ResourcesBase
from ..clients.util import escape_for_f_string, escape_for_sproc, get_with_retries, poll_with_specified_overhead, scrub_exception
from ..environments import runtime_env, HexEnvironment, SnowbookEnvironment
from .. import dsl, rel, metamodel as m
from ..errors import EngineAutoCreateFailed, EngineNotFoundException, EnginePending, EngineSizeMismatchWarning, EngineResumeFailed, Errors, InvalidSourceTypeWarning, RAIException, HexSessionException, SnowflakeAppMissingException, SnowflakeChangeTrackingNotEnabledException, SnowflakeImportMissingException, SnowflakeInvalidSource, SnowflakeProxyAPIDeprecationWarning, SnowflakeProxySourceError, SnowflakeRaiAppNotStarted, SnowflakeTableObject, SnowflakeTableObjectsException, UnknownSourceWarning
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, date
from snowflake.snowpark.types import StringType, StructField, StructType

# warehouse-based snowflake notebooks currently don't have hazmat
crypto_disabled = False
try:
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import padding
except (ModuleNotFoundError, ImportError):
    crypto_disabled = True

#--------------------------------------------------
# Constants
#--------------------------------------------------

VALID_POOL_STATUS = ["ACTIVE", "IDLE", "SUSPENDED"]
# transaction list and get return different fields (duration vs timings)
LIST_TXN_SQL_FIELDS = ["id", "database_name", "engine_name", "state", "abort_reason", "read_only","created_by", "created_on", "finished_at", "duration"]
GET_TXN_SQL_FIELDS = ["id", "database", "engine", "state", "abort_reason", "read_only","created_by", "created_on", "finished_at", "timings"]
IMPORT_STREAM_FIELDS = ["ID", "CREATED_AT", "CREATED_BY", "STATUS", "REFERENCE_NAME", "REFERENCE_ALIAS", "FQ_OBJECT_NAME", "RAI_DATABASE",
                        "RAI_RELATION", "DATA_SYNC_STATUS", "PENDING_BATCHES_COUNT", "NEXT_BATCH_STATUS", "NEXT_BATCH_UNLOADED_TIMESTAMP",
                        "NEXT_BATCH_DETAILS", "LAST_BATCH_DETAILS", "LAST_BATCH_UNLOADED_TIMESTAMP", "CDC_STATUS"]
VALID_ENGINE_STATES = ["READY", "PENDING"]
ENGINE_SIZES = ["HIGHMEM_X64_S", "HIGHMEM_X64_M"]
INTERNAL_ENGINE_SIZES = [
    "XS",
    "S",
    "M",
    "XL",
    "HIGHMEM_X64_S",
    "HIGHMEM_X64_M",
    "HIGHMEM_X64_L",
]
FIELD_MAP = {
    "database_name": "database",
    "engine_name": "engine",
}
VALID_IMPORT_STATES = ["PENDING", "PROCESSING", "QUARANTINED", "LOADED"]
RAI_APP_NAME = "RELATIONALAI"
PYREL_ROOT_DB = 'pyrel_root_db'

#--------------------------------------------------
# Helpers
#--------------------------------------------------

def process_jinja_template(template: str, indent_spaces = 0, **substitutions) -> str:
    lines = template.split('\n')
    processed_lines = []

    for line in lines:
        processed_line = re.sub(r'{{\s*(\w+)\s*}}', lambda m: str(substitutions[m.group(1)]), line)
        processed_lines.append((indent_spaces * " ") + processed_line)

    return '\n'.join(processed_lines)

def type_to_sql(type) -> str:
    if type is str:
        return "VARCHAR"
    if type is int:
        return "NUMBER"
    if type is Number:
        return "DECIMAL(38, 15)"
    if type is float:
        return "FLOAT"
    if type is decimal.Decimal:
        return "DECIMAL(38, 15)"
    if type is bool:
        return "BOOLEAN"
    if type is dict:
        return "VARIANT"
    if type is list:
        return "ARRAY"
    if type is bytes:
        return "BINARY"
    if type is datetime:
        return "TIMESTAMP"
    if type is date:
        return "DATE"
    if isinstance(type, dsl.Type):
        return "VARCHAR"
    raise ValueError(f"Unknown type {type}")

def type_to_snowpark(type) -> str:
    if type is str:
        return "StringType()"
    if type is int:
        return "IntegerType()"
    if type is float:
        return "FloatType()"
    if type is Number:
        return "DecimalType(38, 15)"
    if type is decimal.Decimal:
        return "DecimalType(38, 15)"
    if type is bool:
        return "BooleanType()"
    if type is dict:
        return "MapType()"
    if type is list:
        return "ArrayType()"
    if type is bytes:
        return "BinaryType()"
    if type is datetime:
        return "TimestampType()"
    if type is date:
        return "DateType()"
    if isinstance(type, dsl.Type):
        return "StringType()"
    raise ValueError(f"Unknown type {type}")

def _sanitize_user_name(user: str) -> str:
    # Extract the part before the '@'
    sanitized_user = user.split('@')[0]
    # Replace any character that is not a letter, number, or underscore with '_'
    sanitized_user = re.sub(r'[^a-zA-Z0-9_]', '_', sanitized_user)
    return sanitized_user

#--------------------------------------------------
# Resources
#--------------------------------------------------

APP_NAME = "___RAI_APP___"

class Resources(ResourcesBase):
    def __init__(
        self,
        profile: str | None = None,
        config: Config | None = None,
        connection: Session | None = None,
    ):
        super().__init__(profile, config=config)
        self._session = connection
        self._pending_transactions: list[str] = []
        self._ns_cache = {}
        self.sources = set()

    def get_sf_session(self):
        if isinstance(runtime_env, HexEnvironment):
            raise HexSessionException()
        if isinstance(runtime_env, SnowbookEnvironment):
            return get_active_session()
        else:
            connection_parameters = {}
            authenticator = self.config.get('authenticator', "snowflake")
            if authenticator in SNOWFLAKE_AUTHS:
                authenticator = cast(str, authenticator)
                for key in SNOWFLAKE_AUTHS[authenticator]:
                    connection_parameters[key] = self.config.get(key, SNOWFLAKE_AUTHS[authenticator][key])
            else:
                raise ValueError(f'Authenticator "{authenticator}" not supported')
            auth = self.config.get("authenticator", "")
            passcode = self.config.get("passcode", "")
            if passcode != "":
                # if passcode is set, we assume MFA is enabled and we auto set the authenticator
                connection_parameters["authenticator"] = "username_password_mfa"
                connection_parameters["passcode"] = passcode
            elif auth != "":
                connection_parameters["authenticator"] = auth

            session = Session.builder.configs(connection_parameters).create()
            return session

    def _exec(self, code:str, params:List[Any]|Any|None = None, raw=False, help=True) -> Any:
        if not self._session:
            self._session = self.get_sf_session()
        try:
            if params is not None and not isinstance(params, list):
                params = cast(List[Any], [params])
            sess_results = self._session.sql(
                code.replace(APP_NAME, self.get_app_name()),
                params
            )
            if raw:
                return sess_results
            return sess_results.collect()
        except Exception as e:
            if not help:
                raise e
            orig_message = str(e).lower()
            rai_app = self.config.get("rai_app_name", "")
            engine = self.get_default_engine_name()
            assert isinstance(rai_app, str), f"rai_app_name must be a string, not {type(rai_app)}"
            assert isinstance(engine, str), f"engine must be a string, not {type(engine)}"
            print("\n")
            if re.search(f"database '{rai_app}' does not exist or not authorized.".lower(), orig_message):
                exception = SnowflakeAppMissingException(rai_app)
                raise exception from None
            elif re.search(r"javascript execution error", orig_message):
                match = re.search(r"\"message\":\"(.*)\"", orig_message)
                if match:
                    message = match.group(1)
                    if "engine was deleted" in message or "engine not found" in message:
                        assert isinstance(engine, str), f"engine must be a string, not {type(engine)}"
                        exception = EngineNotFoundException(engine, message)
                        # to test
                        raise e
                    if "engine is in pending" in message or "engine is provisioning" in message:
                        raise EnginePending(engine)
                    else:
                        raise RAIException(message) from None

            if re.search(r"the relationalai service has not been started.", orig_message):
                app_name = self.config.get("rai_app_name", "")
                assert isinstance(app_name, str), f"rai_app_name must be a string, not {type(app_name)}"
                raise SnowflakeRaiAppNotStarted(app_name)
            raise RAIException(str(e))


    def reset(self):
        self._session = None


    #--------------------------------------------------
    # Snowflake Account Flags
    #--------------------------------------------------

    def is_account_flag_set(self, flag: str) -> bool:
        results = self._exec(
            f"SHOW PARAMETERS LIKE '%{flag}%' IN ACCOUNT;"
        )
        if not results:
            return False
        return results[0]["value"] == "true"

    #--------------------------------------------------
    # Databases
    #--------------------------------------------------

    def get_database(self, database: str):
        results = self._exec(
            f"call {APP_NAME}.api.get_database('{database}');"
        )
        if not results:
            return None
        db = results[0]
        if not db:
            return None
        return {
            "id": db["ID"],
            "name": db["NAME"],
            "created_by": db["CREATED_BY"],
            "created_on": db["CREATED_ON"],
            "deleted_by": db["DELETED_BY"],
            "deleted_on": db["DELETED_ON"],
            "state": db["STATE"],
        }

    #--------------------------------------------------
    # Engines
    #--------------------------------------------------

    def get_engine_sizes(self):
        if self.config.show_all_engine_sizes():
            return INTERNAL_ENGINE_SIZES
        else:
            return ENGINE_SIZES

    def list_engines(self, state: str | None = None):
        where_clause = f"WHERE STATUS = '{state.upper()}'" if state else ""
        statement = f"SELECT NAME, ID, SIZE, STATUS, CREATED_BY, CREATED_ON, UPDATED_ON FROM {APP_NAME}.api.engines {where_clause} ORDER BY NAME ASC;"
        results = self._exec(statement)
        if not results:
            return []
        return [
            {
                "name": row["NAME"],
                "id": row["ID"],
                "size": row["SIZE"],
                "state": row["STATUS"], # callers are expecting 'state'
                "created_by": row["CREATED_BY"],
                "created_on": row["CREATED_ON"],
                "updated_on": row["UPDATED_ON"],
            }
            for row in results
        ]

    def get_engine(self, name: str):
        results = self._exec(
            f"SELECT NAME, ID, SIZE, STATUS, CREATED_BY, CREATED_ON, UPDATED_ON, VERSION, AUTO_SUSPEND_MINS, SUSPENDS_AT FROM {APP_NAME}.api.engines WHERE NAME='{name}';"
        )
        if not results:
            return None
        engine = results[0]
        if not engine:
            return None
        engine_state: EngineState = {
            "name": engine["NAME"],
            "id": engine["ID"],
            "size": engine["SIZE"],
            "state": engine["STATUS"], # callers are expecting 'state'
            "created_by": engine["CREATED_BY"],
            "created_on": engine["CREATED_ON"],
            "updated_on": engine["UPDATED_ON"],
            "version": engine["VERSION"],
            "auto_suspend": engine["AUTO_SUSPEND_MINS"],
            "suspends_at": engine["SUSPENDS_AT"]
        }
        return engine_state

    def get_default_engine_name(self) -> str:
        engine = self.config.get("engine", None)
        if not engine:
            engine = self.get_user_based_engine_name()
        self.config.set("engine", engine)
        return engine

    def is_valid_engine_state(self, name:str):
        return name in VALID_ENGINE_STATES

    def create_engine(self, name:str, size:str|None=None):
        if size is None:
            size = self.config.get_default_engine_size()
        try:
            with debugging.span("create_engine", name=name, size=size):
                self._exec(f"call {APP_NAME}.api.create_engine('{name}', '{size}');")
        except Exception as e:
            raise Exception(f"Failed to create engine {name} with size {size}: {e}") from e

    def create_engine_async(self, name:str, size:str|None=None):
        if size is None:
            size = self.config.get_default_engine_size()
        auto_suspend_mins = self.config.get_default_auto_suspend_mins()
        try:
            with debugging.span("create_engine", name=name, size=size):
                self._exec(f"call {APP_NAME}.api.create_engine_async('{name}', '{size}', PARSE_JSON('{{\"auto_suspend_mins\": {auto_suspend_mins}}}'), null);")
        except Exception as e:
            raise Exception(f"Failed to create engine {name} with size {size}: {e}") from e

    def delete_engine(self, name:str, force:bool = False):
        self._exec(f"call {APP_NAME}.api.delete_engine('{name}', {force});")

    def suspend_engine(self, name:str):
        raise Exception("Not implemented")

    def resume_engine(self, name:str):
        self._exec(f"call {APP_NAME}.api.resume_engine('{name}');")
        # returning empty dict to match the expected return type
        return {}

    #--------------------------------------------------
    # Graphs
    #--------------------------------------------------

    def list_graphs(self) -> List[AvailableModel]:
        with debugging.span("list_models"):
            query = textwrap.dedent(f"""
                    SELECT NAME, ID, CREATED_BY, CREATED_ON, STATE, DELETED_BY, DELETED_ON
                    FROM {APP_NAME}.api.databases
                    WHERE state <> 'DELETED'
                    ORDER BY NAME ASC;
                    """)
            results = self._exec(query)
            if not results:
                return []
            return [
                {
                    "name": row["NAME"],
                    "id": row["ID"],
                    "created_by": row["CREATED_BY"],
                    "created_on": row["CREATED_ON"],
                    "state": row["STATE"],
                    "deleted_by": row["DELETED_BY"],
                    "deleted_on": row["DELETED_ON"],
                }
                for row in results
            ]

    def get_graph(self, name: str):
        with debugging.span("get_model", name=name):
            results = self._exec(
                textwrap.dedent(f"""
                SELECT ID, NAME, CREATED_BY, CREATED_ON, DELETED_BY, DELETED_ON, STATE
                FROM {APP_NAME}.api.databases
                WHERE NAME='{name}' AND STATE <> 'DELETED'
                """)
            )
            if not results:
                return None
            return results[0]

    def create_graph(self, name: str):
        with debugging.span("create_model", name=name):
            self._exec(f"call {APP_NAME}.api.create_database('{name}');")

    def delete_graph(self, name:str):
        with debugging.span("delete_model", name=name):
            self._exec(f"call {APP_NAME}.api.delete_database('{name}');")

    def clone_graph(self, target_name:str, source_name:str, nowait_durable=True, force=False):
        if force and self.get_graph(target_name):
            self.delete_graph(target_name)
        with debugging.span("clone_model", target_name=target_name, source_name=source_name):
            # not a mistake: the clone_database argument order is indeed target then source:
            self._exec(f"call {APP_NAME}.api.clone_database('{target_name}', '{source_name}', {nowait_durable});")

    #--------------------------------------------------
    # Models
    #--------------------------------------------------

    def list_models(self, database: str, engine: str):
        pass

    def create_models(self, database: str, engine: str | None, models:List[Tuple[str, str]]) -> List[Any]:
        rel_code = self.create_models_code(models)
        self.exec_raw(database, engine, rel_code, readonly=False)
        # TODO: handle SPCS errors once they're figured out
        return []

    def delete_model(self, database:str, engine:str | None, name:str):
        self.exec_raw(database, engine, f"def delete[:rel, :catalog, :model, \"{name}\"]: rel[:catalog, :model, \"{name}\"]", readonly=False)

    def create_models_code(self, models:List[Tuple[str, str]]) -> str:
        lines = []
        for (name, code) in models:
            name = name.replace("\"", "\\\"")
            assert "\"\"\"\"\"\"\"" not in code, "Code literals must use fewer than 7 quotes."

            lines.append(textwrap.dedent(f"""
            def delete[:rel, :catalog, :model, "{name}"]: rel[:catalog, :model, "{name}"]
            def insert[:rel, :catalog, :model, "{name}"]: raw\"\"\"\"\"\"\"
            """) + code + "\n\"\"\"\"\"\"\"")
        rel_code = "\n\n".join(lines)
        return rel_code

    #--------------------------------------------------
    # Exports
    #--------------------------------------------------

    def list_exports(self, database: str, engine: str):
        return []

    def get_export_code(self, params: ExportParams):
        sql_inputs = ", ".join([f"{name} {type_to_sql(type)}" for (name, _, type) in params.inputs])
        input_names = [name for (name, *_) in params.inputs]
        sql_out = ", ".join([f"{name} {type_to_sql(type)}" for (name, type) in params.out_fields])
        sql_out_names = ", ".join([f"CAST(col{ix:03} AS {type_to_sql(type)}) as {name}" for (ix, (name, type)) in enumerate(params.out_fields)])
        py_outs = ", ".join([f"StructField(\"{name}\", {type_to_snowpark(type)})" for (name, type) in params.out_fields])
        py_inputs = ", ".join([name for (name, *_) in params.inputs])
        safe_rel = escape_for_f_string(params.code).strip()
        clean_inputs = []
        for (name, var, type) in params.inputs:
            if type is str:
                clean_inputs.append(f"{name} = '\"' + escape({name}) + '\"'")
            # Replace `var` with `name` and keep the following non-word character unchanged
            pattern = re.compile(re.escape(var) + r'(\W)')
            safe_rel = re.sub(pattern, rf"{{{name}}}\1", safe_rel)
        if py_inputs:
            py_inputs = f", {py_inputs}"
        clean_inputs = ("\n" + " "*20).join(clean_inputs)
        assert __package__ is not None, "Package name must be set"
        with importlib.resources.open_text(
            __package__, "export_procedure.py.jinja"
        ) as f:
            template = f.read()
        def quote(s: str, f = False) -> str:
            return '"' + s + '"' if not f else 'f"' + s + '"'
        python_code = process_jinja_template(
            template,
            indent_spaces=12,
            func_name=quote(params.func_name),
            database=quote(params.root_database),
            proc_database=quote(params.proc_database),
            engine=quote(params.engine),
            rel_code=quote(safe_rel, f=True),
            APP_NAME=quote(APP_NAME),
            input_names=input_names,
            outputs=sql_out,
            sql_out_names=sql_out_names,
            clean_inputs=clean_inputs,
            py_inputs=py_inputs,
            py_outs=py_outs,
        ).strip()
        sql_code = textwrap.dedent(f"""
            CREATE OR REPLACE PROCEDURE {params.func_name}({sql_inputs}{sql_inputs and ',' or ''} engine STRING DEFAULT NULL)
            RETURNS TABLE({sql_out})
            LANGUAGE PYTHON
            RUNTIME_VERSION = '3.10'
            PACKAGES = ('snowflake-snowpark-python')
            HANDLER = 'handle'
            EXECUTE AS CALLER
            AS
            $$
            {escape_for_sproc(python_code)}
            $$;
        """)
        python_code = textwrap.dedent(" " * 12 + python_code)
        # This check helps catch invalid code early and for dry runs:
        try:
            ast.parse(python_code)
        except SyntaxError:
            raise ValueError(f"Internal error: invalid Python code generated:\n{python_code}")
        return sql_code


    def create_export(self, params: ExportParams):
        sql_code = self.get_export_code(params)
        if params.dry_run:
            return
        start = time.perf_counter()
        self.clone_graph(params.proc_database, params.model_database, force=True)
        self._exec(sql_code)
        debugging.time("export", time.perf_counter() - start, DataFrame(), code=sql_code.replace(APP_NAME, self.get_app_name()))


    def create_export_table(self, database: str, engine: str, table: str, relation: str, columns: Dict[str, str], code: str, refresh: str|None=None):
        print("Snowflake doesn't support creating export tables yet. Try creating the table manually first.")
        pass

    def delete_export(self, database: str, engine: str, name: str):
        pass

    #--------------------------------------------------
    # Imports
    #--------------------------------------------------

    def is_valid_import_state(self, state:str):
        return state in VALID_IMPORT_STATES

    def imports_to_dicts(self, results):
        parsed_results = [
            {field.lower(): row[field] for field in IMPORT_STREAM_FIELDS}
            for row in results
        ]
        return parsed_results

    def change_stream_status(self, stream_id: str, model:str, suspend: bool):
        if stream_id and model:
            if suspend:
                self._exec(f"CALL {APP_NAME}.api.suspend_data_stream('{stream_id}', '{model}');")
            else:
                self._exec(f"CALL {APP_NAME}.api.resume_data_stream('{stream_id}', '{model}');")

    def change_imports_status(self, suspend: bool):
        if suspend:
            self._exec(f"CALL {APP_NAME}.app.suspend_cdc();")
        else:
            self._exec(f"CALL {APP_NAME}.app.resume_cdc();")

    def get_imports_status(self) -> ImportsStatus|None:
        # NOTE: We expect there to only ever be one result?
        results = self._exec(f"CALL {APP_NAME}.app.cdc_status();")
        if results:
            result = next(iter(results))
            engine = result['CDC_ENGINE_NAME']
            engine_status = result['CDC_ENGINE_STATUS']
            engine_size = result['CDC_ENGINE_SIZE']
            task_status = result['CDC_TASK_STATUS']
            info = result['CDC_TASK_INFO']
            enabled = result['CDC_ENABLED']
            return {"engine": engine, "engine_size": engine_size, "engine_status": engine_status, "status": task_status, "enabled": enabled, "info": info }
        return None

    def set_imports_engine_size(self, size:str):
        try:
            self._exec(f"CALL {APP_NAME}.app.alter_cdc_engine_size('{size}');")
        except Exception as e:
            raise e

    def list_imports(
        self,
        id:str|None = None,
        name:str|None = None,
        model:str|None = None,
        status:str|None = None,
        creator:str|None = None,
    ) -> list[Import]:
        where = []
        if id and isinstance(id, str):
            where.append(f"LOWER(ID) = '{id.lower()}'")
        if name and isinstance(name, str):
            where.append(f"LOWER(FQ_OBJECT_NAME) = '{name.lower()}'")
        if model and isinstance(model, str):
            where.append(f"LOWER(RAI_DATABASE) = '{model.lower()}'")
        if creator and isinstance(creator, str):
            where.append(f"LOWER(CREATED_BY) = '{creator.lower()}'")
        if status and isinstance(status, str):
            where.append(f"LOWER(batch_status) = '{status.lower()}'")
        where_clause = " AND ".join(where)

        # this is roughly copied from the native app code because we don't have a way to
        # get the status of multiple streams at once and doing them individually is way
        # too slow
        statement = f"""
        select ID, RAI_DATABASE, FQ_OBJECT_NAME, CREATED_AT, CREATED_BY, nextBatch.status as batch_status, processing_errors, nextBatch.batches,
            from {APP_NAME}.api.data_streams as ds
            left JOIN (
            select
                data_stream_id,
                min_by(status, unloaded) as status,
                min_by(batch_details, unloaded) as batch_details,
                min(processing_details:processingErrors) as processing_errors,
                min(unloaded) as unloaded,
                count(*) as batches
            from {APP_NAME}.api.data_stream_batches
            group by data_stream_id
            ) nextBatch
            ON ds.id = nextBatch.data_stream_id
            {f"where {where_clause}" if where_clause else ""}
            ORDER BY FQ_OBJECT_NAME ASC;
        """

        results = self._exec(statement)
        items = []
        if results:
            for stream in results:
                (id, db, name, created_at, created_by, status, processing_errors, batches) = stream
                if status and isinstance(status, str):
                    status = status.upper()
                if processing_errors:
                    if status in ["QUARANTINED", "PENDING"]:
                        start = processing_errors.rfind("Error")
                        if start != -1:
                            processing_errors = processing_errors[start:-1]
                    else:
                        processing_errors = None
                items.append(cast(Import, {
                    "id": id,
                    "model": db,
                    "name": name,
                    "created": created_at,
                    "creator": created_by,
                    "status": status.upper() if status else None,
                    "errors": processing_errors if processing_errors != "[]" else None,
                    "batches": f"{batches}" if batches else "",
                }))
        return items

    def poll_imports(self, sources:List[str], model:str):
        source_set = {source.upper() for source in sources}
        def check_imports():
            imports = [
                import_
                for import_ in self.list_imports(model=model)
                if import_["name"].upper() in source_set
            ]
            statuses = [import_["status"] for import_ in imports]
            if all(status == "LOADED" for status in statuses):
                return True
            if any(status == "QUARANTINED" for status in statuses):
                failed_imports = [import_["name"] for import_ in imports if import_["status"] == "QUARANTINED"]
                raise RAIException("Imports failed:" + ", ".join(failed_imports)) from None
            # this check is necessary in case some of the tables are empty;
            # such tables may be synced even though their status is None:
            def synced(import_):
                if import_["status"] == "LOADED":
                    return True
                if import_["status"] is None:
                    import_full_status = self.get_import_stream(import_["name"], model)
                    if import_full_status and import_full_status[0]["data_sync_status"] == "SYNCED":
                        return True
                return False
            if all(synced(import_) for import_ in imports):
                return True
        poll_with_specified_overhead(check_imports, overhead_rate=0.1, max_delay=10)

    def get_import_stream(self, name:str|None, model:str|None):
        results = self._exec(f"CALL {APP_NAME}.api.get_data_stream('{name}', '{model}');")
        if not results:
            return None
        return self.imports_to_dicts(results)

    def create_import_stream(self, source:ImportSource, model:str, rate = 1, options: dict|None = None):
        assert isinstance(source, ImportSourceTable), "Snowflake integration only supports loading from SF Tables. Try loading your data as a table via the Snowflake interface first."
        object = source.fqn

        if object.lower() in [x["name"].lower() for x in self.list_imports(model=model)]:
            return

        query = f"SHOW OBJECTS LIKE '{source.table}' IN {source.database}.{source.schema}"
        info = self._exec(query)
        if not info:
            raise ValueError(f"Object {source.table} not found in {source.database}.{source.schema}")
        else:
            data = info[0]
            if not data:
                raise ValueError(f"Object {source.table} not found in {source.database}.{source.schema}")
            # (time, name, db_name, schema_name, kind, *rest)
            kind = data["kind"]

        command = f"""call {APP_NAME}.api.create_data_stream(
            {APP_NAME}.api.object_reference('{kind}', '{object}'),
            '{model}',
            '{object.replace('.', '_').lower()}');"""

        def create_stream(tracking_just_changed=False):
            try:
                self._exec(command)
            except Exception as e:
                if "ensure that CHANGE_TRACKING is enabled on the source object" in str(e):
                    if self.config.get("ensure_change_tracking", False) and not tracking_just_changed:
                        try:
                            self._exec(f"ALTER {kind} {object} SET CHANGE_TRACKING = TRUE;")
                            create_stream(tracking_just_changed=True)
                        except Exception:
                            pass
                    else:
                        print("\n")
                        exception = SnowflakeChangeTrackingNotEnabledException((object, kind))
                        raise exception from None
                raise e

        create_stream()

    def create_import_snapshot(self, source:ImportSource, model:str, options: dict|None = None):
        raise Exception("Snowflake integration doesn't support snapshot imports yet")

    def delete_import(self, import_name:str, model:str, force = False):
        engine = self.get_default_engine_name()
        rel_name = import_name.replace('.', '_').lower() # see logic in create_import_stream
        try:
            self._exec(f"""call {APP_NAME}.api.delete_data_stream(
                '{import_name}',
                '{model}'
            );""")
        except RAIException as err:
            if "stream does not exist" not in str(err) or not force:
                raise

        # Clear the leftover relation to free up the name (in case the user re-creates the stream)
        self.exec_raw(model, engine, f"""
            declare ::{rel_name}
            def delete[:\"{rel_name}\"]: {{ {rel_name} }}
        """, readonly=False)

    #--------------------------------------------------
    # Exec Async
    #--------------------------------------------------

    def _check_exec_async_status(self, txn_id: str):
        """Check whether the given transaction has completed."""

        with debugging.span("check_status"):
            response = self._exec(f"CALL {APP_NAME}.api.get_transaction('{txn_id}');")
            assert response, f"No results from get_transaction('{txn_id}')"

        response_row = next(iter(response))
        status: str = response_row['STATE']

        # remove the transaction from the pending list if it's completed or aborted
        if status in ["COMPLETED", "ABORTED"]:
            if txn_id in self._pending_transactions:
                self._pending_transactions.remove(txn_id)

        # @TODO: Find some way to tunnel the ABORT_REASON out. Azure doesn't have this, but it's handy
        return status == "COMPLETED" or status == "ABORTED"

    def decrypt_stream(self, key: bytes, iv: bytes, src: bytes) -> bytes:
        """Decrypt the provided stream with PKCS#5 padding handling."""

        if crypto_disabled:
            raise Exception("library `cryptography.hazmat` missing; please install")

        # `type:ignore`s are because of the conditional import, which
        # we have because warehouse-based snowflake notebooks don't support
        # the crypto library we're using.
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend()) # type: ignore
        decryptor = cipher.decryptor()

        # Decrypt the data
        decrypted_padded_data = decryptor.update(src) + decryptor.finalize()

        # Unpad the decrypted data using PKCS#5
        unpadder = padding.PKCS7(128).unpadder()  # type: ignore # Use 128 directly for AES
        unpadded_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()

        return unpadded_data

    def _decrypt_artifact(self, data: bytes, encryption_material: str) -> bytes:
        """Decrypts the artifact data using provided encryption material."""
        encryption_material_parts = encryption_material.split("|")
        assert len(encryption_material_parts) == 3, "Invalid encryption material"

        algorithm, key_base64, iv_base64 = encryption_material_parts
        assert algorithm == "AES_128_CBC", f"Unsupported encryption algorithm {algorithm}"

        key = base64.standard_b64decode(key_base64)
        iv = base64.standard_b64decode(iv_base64)

        return self.decrypt_stream(key, iv, data)

    def _list_exec_async_artifacts(self, txn_id: str) -> Dict[str, Dict]:
        """Grab the list of artifacts produced in the transaction and the URLs to retrieve their contents."""
        with debugging.span("list_results"):
            response = self._exec(
                f"CALL {APP_NAME}.api.get_transaction_artifacts('{txn_id}');"
            )
            assert response, f"No results from get_transaction_artifacts('{txn_id}')"
            return {row["FILENAME"]: row for row in response}

    def _fetch_exec_async_artifacts(
        self, artifact_info: Dict[str, Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Grab the contents of the given artifacts from SF in parallel using threads."""

        with requests.Session() as session:
            def _fetch_data(name_info):
                filename, metadata = name_info

                try:
                    # Extract the presigned URL and encryption material from metadata
                    url_key = self.get_url_key()
                    presigned_url = metadata[url_key]
                    encryption_material = metadata["ENCRYPTION_MATERIAL"]

                    response = get_with_retries(session, presigned_url)
                    response.raise_for_status()  # Throw if something goes wrong

                    decrypted = self._maybe_decrypt(response.content, encryption_material)
                    return (filename, decrypted)

                except requests.RequestException as e:
                    raise scrub_exception(e)

            # Create a list of tuples for the map function
            name_info_pairs = list(artifact_info.items())

            with ThreadPoolExecutor(max_workers=5) as executor:
                results = executor.map(_fetch_data, name_info_pairs)

                return {name: data for (name, data) in results}

    def _maybe_decrypt(self, content: bytes, encryption_material: str) -> bytes:
        # Decrypt if encryption material is present
        if encryption_material:
            # if there's no padding, the initial file was empty
            if len(content) == 0:
                return b""

            return self._decrypt_artifact(content, encryption_material)

        # otherwise, return content directly
        return content

    def _parse_exec_async_results(self, arrow_files: List[Tuple[str, bytes]]):
        """Mimics the logic in _parse_arrow_results of railib/api.py#L303 without requiring a wrapping multipart form."""
        results = []

        for file_name, file_content in arrow_files:
            with pa.ipc.open_stream(file_content) as reader:
                schema = reader.schema
                batches = [batch for batch in reader]
                table = pa.Table.from_batches(batches=batches, schema=schema)
                results.append({"relationId": file_name, "table": table})

        return results

    def _download_results(
        self, artifact_info: Dict[str, Dict], txn_id: str, state: str
    ) -> TransactionAsyncResponse:
        with debugging.span("download_results"):
            # Fetch artifacts
            artifacts = self._fetch_exec_async_artifacts(artifact_info)

            # Directly use meta_json as it is fetched
            meta_json_bytes = artifacts["metadata.json"]

            # Decode the bytes and parse the JSON
            meta_json_str = meta_json_bytes.decode('utf-8')
            meta_json = json.loads(meta_json_str)  # Parse the JSON string

            # Use the metadata to map arrow files to the relations they contain
            try:
                arrow_files_to_relations = {
                    artifact["filename"]: artifact["relationId"]
                    for artifact in meta_json
                }
            except KeyError:
                # TODO: Remove this fallback mechanism later once several engine versions are updated
                arrow_files_to_relations = {
                    f"{ix}.arrow": artifact["relationId"]
                    for ix, artifact in enumerate(meta_json)
                }

            # Hydrate the arrow files into tables
            results = self._parse_exec_async_results(
                [
                    (arrow_files_to_relations[name], content)
                    for name, content in artifacts.items()
                    if name.endswith(".arrow")
                ]
            )

            # Create and return the response
            rsp = TransactionAsyncResponse()
            rsp.transaction = {
                "id": txn_id,
                "state": state,
                "response_format_version": None,
            }
            rsp.metadata = meta_json
            rsp.problems = artifacts.get(
                "problems.json"
            )  # Safely access possible missing keys
            rsp.results = results
            return rsp

    def get_url_key(self):
        container_runtime = isinstance(runtime_env, SnowbookEnvironment) and runtime_env.runner == "container"
        return 'PRESIGNED_URL_AP' if container_runtime else 'PRESIGNED_URL'

    def _exec_async_v2(
        self,
        database: str,
        engine: str,
        raw_code: str,
        inputs={},
        readonly=True,
        nowait_durable=False,
        headers={},
    ):
        from .. import __version__ # avoid circular import by importing here

        with debugging.span("transaction") as txn_span:
            with debugging.span("create_v2"):
                headers['user-agent'] = f"pyrel/{__version__}"

                use_graph_index = self.config.get("use_graph_index", USE_GRAPH_INDEX)

                # Depending on the shape of the input, the behavior of exec_async_v2 changes.
                # When using the new format (with an object), the function retrieves the
                # 'rai' database by hashing the model and username. In contrast, the
                # current version directly uses the passed database value.
                # Therefore, we must use the original exec_async_v2 when not using the
                # graph index to ensure the correct database is utilized.
                if use_graph_index:
                    sql_string = f"CALL {APP_NAME}.api.exec_async_v2(?, {{'database': '{database}', 'engine': '{engine}', 'inputs': {inputs}, 'readonly': {readonly}, 'nowait_durable': {nowait_durable}, 'headers': {headers}}});"
                else:
                    sql_string = f"CALL {APP_NAME}.api.exec_async_v2('{database}','{engine}', ?, {inputs}, {readonly}, {nowait_durable}, {headers});"

                response = self._exec(
                    sql_string,
                    raw_code,
                )

            if not response:
                raise Exception("Failed to create transaction")

            artifact_info = {}
            rows = list(iter(response))

            # process the first row since txn_id and state are the same for all rows
            first_row = rows[0]
            txn_id = first_row['ID']
            state = first_row['STATE']
            filename = first_row['FILENAME']

            txn_span["txn_id"] = txn_id
            debugging.event("transaction_created", txn_span, txn_id=txn_id)

            # fast path: transaction already finished
            if state in ["COMPLETED", "ABORTED"]:
                if txn_id in self._pending_transactions:
                    self._pending_transactions.remove(txn_id)

                # Process rows to get the rest of the artifacts
                for row in rows:
                    filename = row['FILENAME']
                    artifact_info[filename] = row

            # Slow path: transaction not done yet; start polling
            else:
                self._pending_transactions.append(txn_id)
                with debugging.span("wait", txn_id=txn_id):
                    poll_with_specified_overhead(
                        lambda: self._check_exec_async_status(txn_id), 0.1
                    )
                artifact_info = self._list_exec_async_artifacts(txn_id)

            with debugging.span("fetch"):
                return self._download_results(artifact_info, txn_id, state)

    def get_user_based_engine_name(self):
        if not self._session:
            self._session = self.get_sf_session()
        user_table = self._session.sql("select current_user()").collect()
        user = user_table[0][0]
        assert isinstance(user, str), f"current_user() must return a string, not {type(user)}"
        return _sanitize_user_name(user)

    def auto_create_engine(self, name: str | None = None, size: str | None = None):
        with debugging.span("auto_create_engine", active=self._active_engine) as span:
            active = self._get_active_engine()
            if active:
                return active

            engine_name = name or self.get_default_engine_name()

            # Use the provided size or fall back to the config
            if size:
                engine_size = size
            else:
                engine_size = self.config.get("engine_size", None)

            try:
                engine = self.get_engine(engine_name)
                if engine:
                    span.update(cast(dict, engine))

                # if engine is in the pending state, poll until its status changes
                # if engine is gone, delete it and create new one
                # if engine is in the ready state, return engine name
                if engine:
                    if engine["state"] == "PENDING":
                        # if the user explicitly specified a size, warn if the pending engine size doesn't match it
                        if size is not None and engine["size"] != size:
                            EngineSizeMismatchWarning(engine_name, engine["size"], size)
                        # poll until engine is ready
                        with Spinner(
                            "Waiting for engine to be initialized",
                            "Engine ready",
                        ):
                            while True:
                                engine = self.get_engine(engine_name)
                                if engine and engine["state"] == "PENDING":
                                    time.sleep(2)
                                    continue
                                else:
                                    # sleep for 2 seconds to ensure engine is ready,
                                    # since querying immediately after state change may still return stale state for a few seconds
                                    time.sleep(2)
                                    break
                    elif engine["state"] == "SUSPENDED":
                        with Spinner(f"Resuming engine '{engine_name}'", "Engine ready", f"Failed to resume engine '{engine_name}'"):
                            try:
                                self.resume_engine(engine_name)
                            except Exception:
                                raise EngineResumeFailed(engine_name)
                    elif engine["state"] == "READY":
                        # if the user explicitly specified a size, warn if the ready engine size doesn't match it
                        if size is not None and engine["size"] != size:
                            EngineSizeMismatchWarning(engine_name, engine["size"], size)
                        self._set_active_engine(engine)
                        return engine_name
                    elif engine["state"] == "GONE":
                        try:
                            # "Gone" is abnormal condition when metadata and SF service don't match
                            # Therefore, we have to delete the engine and create a new one
                            # it could be case that engine is already deleted, so we have to catch the exception
                            self.delete_engine(engine_name)
                            # After deleting the engine, set it to None so that we can create a new engine
                            engine = None
                        except Exception as e:
                            # if engine is already deleted, we will get an exception
                            # we can ignore this exception and create a new engine
                            if isinstance(e, EngineNotFoundException):
                                engine = None
                                pass
                            else:
                                raise EngineAutoCreateFailed(engine_name) from e

                if not engine:
                    with Spinner(
                        f"Auto-creating engine {engine_name}",
                        f"Auto-created engine {engine_name}",
                        "Engine creation failed",
                    ):
                        self.create_engine(engine_name, size=engine_size)
            except Exception as e:
                raise EngineAutoCreateFailed(engine_name) from e
            return engine_name

    def auto_create_engine_async(self, name: str | None = None):
        active = self._get_active_engine()
        if active and (active == name or name is None):
            return # @NOTE: This method weirdly doesnt return engine name even though all the other ones do?

        with Spinner(
            "Checking engine status",
            leading_newline=True,
        ) as spinner:
            with debugging.span("auto_create_engine_async", active=self._active_engine):
                engine_name = name or self.get_default_engine_name()
                try:
                    engine = self.get_engine(engine_name)
                    # if engine is gone, delete it and create new one
                    # in case of pending state, do nothing, it is use_index responsibility to wait for engine to be ready
                    if engine:
                        if engine["state"] == "PENDING":
                            spinner.update_messages(
                                {
                                    "finished_message": f"Starting engine {engine_name}",
                                }
                            )
                            pass
                        elif engine["state"] == "SUSPENDED":
                            spinner.update_messages(
                                {
                                    "finished_message": f"Resuming engine {engine_name}",
                                }
                            )
                            try:
                                self.resume_engine(engine_name)
                            except Exception:
                                raise EngineResumeFailed(engine_name)
                        elif engine["state"] == "READY":
                            spinner.update_messages(
                                {
                                    "finished_message": f"Engine {engine_name} initialized",
                                }
                            )
                            pass
                        elif engine["state"] == "GONE":
                            spinner.update_messages(
                                {
                                    "message": f"Restarting engine {engine_name}",
                                }
                            )
                            try:
                                # "Gone" is abnormal condition when metadata and SF service don't match
                                # Therefore, we have to delete the engine and create a new one
                                # it could be case that engine is already deleted, so we have to catch the exception
                                # set it to None so that we can create a new engine
                                engine = None
                                self.delete_engine(engine_name)
                            except Exception as e:
                                # if engine is already deleted, we will get an exception
                                # we can ignore this exception and create a new engine asynchronously
                                if isinstance(e, EngineNotFoundException):
                                    engine = None
                                    pass
                                else:
                                    EngineAutoCreateFailed(engine_name)

                    if not engine:
                        # creating small engine by default, we will change that when configuring graph index will be implemented
                        self.create_engine_async(engine_name)

                        spinner.update_messages(
                            {
                                "finished_message": f"Starting engine {engine_name}...",
                            }
                        )
                    else:
                        self._set_active_engine(engine)

                except Exception as e:
                    spinner.update_messages(
                        {
                            "finished_message": f"Failed to create engine {engine_name}",
                        }
                    )
                    if isinstance(e, RAIException):
                        raise e
                    raise EngineAutoCreateFailed(engine_name) from e

    #--------------------------------------------------
    # Exec
    #--------------------------------------------------

    def exec_raw(
        self,
        database: str,
        engine: str | None,
        raw_code: str,
        readonly=True,
        *,
        inputs: dict = {},
        nowait_durable=False,
        headers={},
    ):
        raw_code = raw_code.replace("'", "\\'")

        # If engine is not provided, create a default engine and use it
        if not engine:
            engine = self.auto_create_engine()

        def exec_async():
            return self._exec_async_v2(
                database, engine, raw_code, inputs, readonly, nowait_durable, headers
            )

        try:
            return exec_async()
        except Exception as e:
            self._active_engine = None
            if "engine not found" in str(e):
                self.auto_create_engine(engine)
                return exec_async()
            raise e


    def format_results(self, results, task:m.Task|None=None) -> Tuple[DataFrame, List[Any]]:
        return result_helpers.format_results(results, task)

    #--------------------------------------------------
    # Exec format
    #--------------------------------------------------

    def exec_format(
        self,
        database: str,
        engine: str,
        raw_code: str,
        task: m.Task,
        format: str,
        inputs: dict = {},
        readonly=True,
        nowait_durable=False,
        headers={},
    ):
        # TODO: add headers and nowait_durable
        start = time.perf_counter()
        output_table = "out" + str(uuid.uuid4()).replace("-", "_")
        temp_table = f"temp_{output_table}"
        use_graph_index = self.config.get("use_graph_index", USE_GRAPH_INDEX)
        try:
            # In the graph index case we need to use the new exec_into_table proc as it obfuscates the db name
            if use_graph_index:
                self._exec(f"call {APP_NAME}.api.exec_into_table(?, ?, ?, ?, ?);", [database, engine, raw_code, output_table, readonly])
            else:
                self._exec(f"call {APP_NAME}.api.exec_into(?, ?, ?, ?, ?);", [database, engine, raw_code, output_table, readonly])
            debugging.time("exec_format", time.perf_counter() - start, DataFrame())

            names = ", ".join([f"col{ix:03} as {name}" for (ix, name) in enumerate(task.return_cols())])
            self._exec(f"CREATE TEMPORARY TABLE {APP_NAME}.results.{temp_table} AS SELECT {names} FROM {APP_NAME}.results.{output_table};")
            self._exec(f"call {APP_NAME}.api.drop_result_table(?)", [output_table])

            temp = cast(snowflake.snowpark.DataFrame, self._exec(f"select * from {APP_NAME}.results.{temp_table}", raw=True))
        except Exception as e:
            msg = str(e).lower()
            if "No columns returned".lower() in msg:
                debugging.time("exec_format", time.perf_counter() - start, DataFrame())
                assert self._session
                return (self._session.createDataFrame([], StructType([StructField(name, StringType()) for name in task.return_cols()])), [])
            raise e
        return (temp, [])

    #--------------------------------------------------
    # Custom model types
    #--------------------------------------------------

    def _get_ns(self, model:dsl.Graph):
        if model not in self._ns_cache:
            self._ns_cache[model] = _Snowflake(model)
        return self._ns_cache[model]

    def to_model_type(self, model:dsl.Graph, name: str, source:str):
        parts = source.split(".")
        if len(parts) < 3:
            raise SnowflakeInvalidSource(Errors.call_source(), source)
        ns = self._get_ns(model)
        for part in parts:
            ns = ns._safe_get(part)
        self.sources.add(source)
        return ns

    #--------------------------------------------------
    # Transactions
    #--------------------------------------------------
    def txn_list_to_dicts(self, transactions):
        dicts = []
        for txn in transactions:
            dict = {}
            txn_dict = txn.asDict()
            for key in txn_dict:
                mapValue = FIELD_MAP.get(key.lower())
                if mapValue:
                    dict[mapValue] = txn_dict[key]
                else:
                    dict[key.lower()] = txn_dict[key]
            dicts.append(dict)
        return dicts

    def get_transaction(self, transaction_id):
        results = self._exec(
            f"CALL {APP_NAME}.api.get_transaction(?);", [transaction_id])
        if not results:
            return None

        results = self.txn_list_to_dicts(results)

        txn = {field: results[0][field] for field in GET_TXN_SQL_FIELDS}

        created_on = txn.get("created_on")
        finished_at = txn.get("finished_at")
        if created_on:
            if finished_at:
                txn['duration'] = finished_at - created_on
            else:
                tz_info = created_on.tzinfo
                txn['duration'] = datetime.now(tz_info) - created_on
        return txn

    def list_transactions(self, **kwargs):
        id = kwargs.get("id", None)
        state = kwargs.get("state", None)
        engine = kwargs.get("engine", None)
        limit = kwargs.get("limit", 100)
        all_users = kwargs.get("all_users", False)
        created_by = kwargs.get("created_by", None)
        only_active = kwargs.get("only_active", False)
        where_clause_arr = []

        if id:
            where_clause_arr.append(f"id = '{id}'")
        if state:
            where_clause_arr.append(f"state = '{state.upper()}'")
        if engine:
            where_clause_arr.append(f"LOWER(engine_name) = '{engine.lower()}'")
        else:
            if only_active:
                where_clause_arr.append("state in ('CREATED', 'RUNNING', 'PENDING')")
        if not all_users and created_by is not None:
            where_clause_arr.append(f"LOWER(created_by) = '{created_by.lower()}'")

        if len(where_clause_arr):
            where_clause = f'WHERE {" AND ".join(where_clause_arr)}'
        else:
            where_clause = ""

        sql_fields = ", ".join(LIST_TXN_SQL_FIELDS)
        query = f"SELECT {sql_fields} from {APP_NAME}.api.transactions {where_clause} ORDER BY created_on DESC LIMIT ?"
        results = self._exec(query, [limit])
        if not results:
            return []
        return self.txn_list_to_dicts(results)

    def cancel_transaction(self, transaction_id):
        self._exec(f"CALL {APP_NAME}.api.CANCEL_TRANSACTION(?);", [transaction_id])
        if transaction_id in self._pending_transactions:
            self._pending_transactions.remove(transaction_id)

    def cancel_pending_transactions(self):
        for txn_id in self._pending_transactions:
            self.cancel_transaction(txn_id)

    def get_transaction_events(self, transaction_id: str, continuation_token:str=''):
        results = self._exec(
            f"SELECT {APP_NAME}.api.get_transaction_events(?, ?);",
            [transaction_id, continuation_token],
        )
        if not results:
            return {
                "events": [],
                "continuation_token": None
            }
        row = results[0][0]
        return json.loads(row)

    #--------------------------------------------------
    # Snowflake specific
    #--------------------------------------------------

    def get_version(self):
        results = self._exec(f"SELECT {APP_NAME}.app.get_release()")
        if not results:
            return None
        return results[0][0]

    def list_warehouses(self):
        results = self._exec("SHOW WAREHOUSES")
        if not results:
            return []
        return [{"name":name}
                for (name, *rest) in results]

    def list_compute_pools(self):
        results = self._exec("SHOW COMPUTE POOLS")
        if not results:
            return []
        return [{"name":name, "status":status, "min_nodes":min_nodes, "max_nodes":max_nodes, "instance_family":instance_family}
                for (name, status, min_nodes, max_nodes, instance_family, *rest) in results]

    def list_roles(self):
        results = self._exec("SELECT CURRENT_AVAILABLE_ROLES()")
        if not results:
            return []
        # the response is a single row with a single column containing
        # a stringified JSON array of role names:
        row = results[0]
        if not row:
            return []
        return [{"name": name} for name in json.loads(row[0])]

    def list_apps(self):
        all_apps = self._exec(f"SHOW APPLICATIONS LIKE '{RAI_APP_NAME}'")
        if not all_apps:
            all_apps = self._exec("SHOW APPLICATIONS")
            if not all_apps:
                return []
        return [{"name":name}
                for (time, name, *rest) in all_apps]

    def list_databases(self):
        results = self._exec("SHOW DATABASES")
        if not results:
            return []
        return [{"name":name}
                for (time, name, *rest) in results]

    def list_sf_schemas(self, database:str):
        results = self._exec(f"SHOW SCHEMAS IN {database}")
        if not results:
            return []
        return [{"name":name}
                for (time, name, *rest) in results]

    def list_tables(self, database:str, schema:str):
        results = self._exec(f"SHOW OBJECTS IN {database}.{schema}")
        items = []
        if results:
            for (time, name, db_name, schema_name, kind, *rest) in results:
                items.append({"name":name, "kind":kind.lower()})
        return items

    def schema_info(self, database:str, schema:str, tables:Iterable[str]):
        pks = self._exec(f"SHOW PRIMARY KEYS IN SCHEMA {database}.{schema};")
        fks = self._exec(f"SHOW IMPORTED KEYS IN SCHEMA {database}.{schema};")
        tables = ", ".join([f"'{x.upper()}'" for x in tables])
        columns = self._exec(textwrap.dedent(f"""
            select TABLE_NAME, COLUMN_NAME, DATA_TYPE
            from {database.upper()}.INFORMATION_SCHEMA.COLUMNS
            where TABLE_SCHEMA ILIKE '{schema.upper()}'
            and TABLE_NAME in ({tables})
            and TABLE_CATALOG ILIKE '{database.upper()}';
        """))
        results = defaultdict(lambda: {"pks": [], "fks": {}, "columns": {}})
        if pks:
            for row in pks:
                results[row[3].lower()]["pks"].append(row[4]) # type: ignore
        if fks:
            for row in fks:
                results[row[7].lower()]["fks"][row[8]] = row[3]
        if columns:
            for row in columns:
                results[row[0].lower()]["columns"][row[1]] = row[2]
        return results

#--------------------------------------------------
# Snowflake Wrapper
#--------------------------------------------------

class PrimaryKey:
    pass

class _Snowflake:
    def __init__(self, model, auto_import=False):
        self._model = model
        self._auto_import = auto_import
        if not isinstance(model._client.resources, Resources):
            raise ValueError("Snowflake model must be used with a snowflake config")
        self._dbs = {}
        imports = model._client.resources.list_imports(model=model.name)
        self._import_structure(imports)

    def _import_structure(self, imports: list[Import]):
        tree = self._dbs
        # pre-create existing imports
        schemas = set()
        for item in imports:
            database_name, schema_name, table_name = item["name"].lower().split('.')
            database = getattr(self, database_name)
            schema = getattr(database, schema_name)
            schemas.add(schema)
            schema._add(table_name, is_imported=True)
        for schema in schemas:
            schema._fetch_info()
        return tree

    def _safe_get(self, name:str) -> 'SnowflakeDB':
        name = name.lower()
        if name in self._dbs:
            return self._dbs[name]
        self._dbs[name] = SnowflakeDB(self, name)
        return self._dbs[name]

    def __getattr__(self, name: str) -> 'SnowflakeDB':
        return self._safe_get(name)


class Snowflake(_Snowflake):
    def __init__(self, model: dsl.Graph, auto_import=False):
        if model._config.get_bool("use_graph_index", USE_GRAPH_INDEX):
            raise SnowflakeProxySourceError()
        else:
            debugging.warn(SnowflakeProxyAPIDeprecationWarning())

        super().__init__(model, auto_import)

class SnowflakeDB:
    def __init__(self, parent, name):
        self._name = name
        self._parent = parent
        self._model = parent._model
        self._schemas = {}

    def _safe_get(self, name: str) -> 'SnowflakeSchema':
        name = name.lower()
        if name in self._schemas:
            return self._schemas[name]
        self._schemas[name] = SnowflakeSchema(self, name)
        return self._schemas[name]

    def __getattr__(self, name: str) -> 'SnowflakeSchema':
        return self._safe_get(name)

class SnowflakeSchema:
    def __init__(self, parent, name):
        self._name = name
        self._parent = parent
        self._model = parent._model
        self._tables = {}
        self._imported = set()
        self._table_info = defaultdict(lambda: {"pks": [], "fks": {}, "columns": {}})

    def _fetch_info(self):
        self._table_info = self._model._client.resources.schema_info(self._parent._name, self._name, self._imported)

    def _add(self, name, is_imported=False):
        name = name.lower()
        if name in self._tables:
            return self._tables[name]
        if is_imported:
            self._imported.add(name)
        else:
            self._tables[name] = SnowflakeTable(self, name)
        return self._tables.get(name)

    def _safe_get(self, name: str) -> 'SnowflakeTable | None':
        table = self._add(name)
        if table:
            table._lazy_init()
        return table

    def __getattr__(self, name: str) -> 'SnowflakeTable | None':
        return self._safe_get(name)

class SnowflakeTable(dsl.Type):
    def __init__(self, parent, name):
        super().__init__(parent._model, f"sf_{name}")
        self._name = name
        self._model = parent._model
        self._parent = parent
        self._aliases = {}
        self._finalzed = False

    def _lazy_init(self):
        parent = self._parent
        name = self._name
        if name not in parent._imported:
            if self._parent._parent._parent._auto_import:
                with Spinner(f"Creating stream for {self.fqname()}", f"Stream created for {self.fqname()}"):
                    db_name = parent._parent._name
                    schema_name = parent._name
                    self._model._client.resources.create_import_stream(ImportSourceTable(db_name, schema_name, name), self._model.name)
                print("")
                parent._imported.add(name)
            else:
                imports = self._model._client.resources.list_imports(model=self._model.name)
                for item in imports:
                    cur_name = item["name"].lower().split(".")[-1]
                    parent._imported.add(cur_name)
            if name not in parent._imported:
                use_graph_index = self._model._config.get("use_graph_index", USE_GRAPH_INDEX)
                if use_graph_index:
                    # use_index will take care of creating the stream
                    # we should just add the table to the imported set
                    parent._imported.add(name)
                    pass
                else:
                    exception = SnowflakeImportMissingException(runtime_env.get_source(), self.fqname(), self._model.name)
                    raise exception from None

        if name not in parent._table_info:
            parent._fetch_info()

        self._finalize()

    def _finalize(self):
        if self._finalzed:
            return

        self._finalzed = True
        self._schema = self._parent._table_info[self._name]
        relation_name = sanitize_identifier(self.fqname().lower())
        model:dsl.Graph = self._model
        model.install_raw(f"declare {relation_name}")
        edb = getattr(std.rel, relation_name)
        id_rel = getattr(std.rel, f"{relation_name}_pyrel_id")

        with model.rule():
            id, val = dsl.create_vars(2)
            edb(dsl.Symbol("METADATA$ROW_ID"), id, val)
            id_rel.add(id)

        with model.rule(dynamic=True):
            prop, id, val = dsl.create_vars(3)
            if self._schema["pks"]:
                getattr(edb, self._schema["pks"][0])(id, val)
            else:
                id_rel(id)
            self.add(snowflake_id=id)

        for prop, prop_type in self._schema["columns"].items():
            prop_ident = sanitize_identifier(prop.lower())
            with model.rule(dynamic=True):
                id, val = dsl.create_vars(2)
                getattr(edb, prop)(id, val)
                _prop = getattr(self, prop_ident)
                if not _prop:
                    raise ValueError(f"Property {prop} couldn't be accessed on {self.fqname()}")
                if _prop.is_multi_valued:
                    inst = self(snowflake_id=id)
                    getattr(inst, prop_ident).add(val)
                else:
                    self(snowflake_id=id).set(**{prop_ident: val})

    def namespace(self):
        return f"{self._parent._parent._name}.{self._parent._name}"

    def fqname(self):
        return f"{self.namespace()}.{self._name}"

    def describe(self, **kwargs):
        model = self._model
        for k, v in kwargs.items():
            if v is PrimaryKey:
                self._schema["pks"] = [k]
            elif isinstance(v, tuple):
                (table, name) = v
                if isinstance(table, SnowflakeTable):
                    fk_table = table
                    pk = fk_table._schema["pks"]
                    with model.rule():
                        inst = fk_table()
                        me = self()
                        getattr(inst, pk[0]) == getattr(me, k)
                        if getattr(self, name).is_multi_valued:
                            getattr(me, name).add(inst)
                        else:
                            me.set(**{name: inst})
                else:
                    raise ValueError(f"Invalid foreign key {v}")
            else:
                raise ValueError(f"Invalid column {k}={v}")
        return self

class Provider(ProviderBase):

    def __init__(
        self,
        profile: str | None = None,
        config: Config | None = None,
        resources: Resources | None = None,
    ):
        if resources:
            self.resources = resources
        else:
            self.resources = Resources(profile, config)

    def list_streams(self, model:str):
        return self.resources.list_imports(model=model)

    def create_streams(self, sources:List[str], model:str, force=False):
        if not self.resources.get_graph(model):
            self.resources.create_graph(model)
        def parse_source(raw:str):
            parts = raw.split(".")
            assert len(parts) == 3, "Snowflake table imports must be in `database.schema.table` format"
            return ImportSourceTable(*parts)
        for source in sources:
            source_table = parse_source(source)
            try:
                with Spinner(f"Creating stream for {source_table.name}", f"Stream for {source_table.name} created"):
                    if force:
                        self.resources.delete_import(source_table.name, model, True)
                    self.resources.create_import_stream(source_table, model)
            except Exception as e:
                if "stream already exists" in f"{e}":
                    raise Exception(f"\n\nStream'{source_table.name.upper()}' already exists.")
                elif "engine not found" in f"{e}":
                    raise Exception("\n\nNo engines found in a READY state. Please use `engines:create` to create an engine that will be used to initialize the target relation.")
                else:
                    raise e
        with Spinner("Waiting for imports to complete", "Imports complete"):
            self.resources.poll_imports(sources, model)

    def delete_stream(self, stream_id: str, model: str):
        return self.resources.delete_import(stream_id, model)

    def sql(self, query:str, params:List[Any]=[], format:Literal["list", "pandas", "lazy"]="list"):
        # note: default format cannot be pandas because .to_pandas() only works on SELECT queries
        result = self.resources._exec(query, params, raw=True, help=False)
        if format == "lazy":
            return result
        elif format == "list":
            return result.collect()
        elif format == "pandas":
            return result.to_pandas()
        else:
            raise ValueError(f"Invalid format {format}. Should be one of 'list', 'pandas', 'lazy'")

    def activate(self):
        with Spinner("Activating RelationalAI app...", "RelationalAI app activated"):
            self.sql("CALL RELATIONALAI.APP.ACTIVATE();")

    def deactivate(self):
        with Spinner("Deactivating RelationalAI app...", "RelationalAI app deactivated"):
            self.sql("CALL RELATIONALAI.APP.DEACTIVATE();")

    def drop_service(self):
        warnings.warn(
            "The drop_service method has been deprecated in favor of deactivate",
            DeprecationWarning,
            stacklevel=2,
        )
        self.deactivate()

    def resume_service(self):
        warnings.warn(
            "The resume_service method has been deprecated in favor of activate",
            DeprecationWarning,
            stacklevel=2,
        )
        self.activate()


#--------------------------------------------------
# SnowflakeClient
#--------------------------------------------------
class SnowflakeClient(Client):
    def _get_source_info(self, sources: Iterable[str]):
        if not sources:
            return {}

        app_name = self.resources.get_app_name()
        partitioned_sources:dict[str, dict[str, list[str]]] = defaultdict(lambda: defaultdict(list))
        for db, schema, table in (source.split('.') for source in sources):
            partitioned_sources[db][schema].append(table)

        query = " UNION ALL ".join(
            f"""SELECT
                    inf.FQN,
                    inf.KIND,
                    IFF(DATEDIFF(second, ds.created_at::TIMESTAMP, inf.LAST_DDL::TIMESTAMP) > 0, 'STALE', 'CURRENT') AS STATE
                FROM (
                    SELECT FQ_OBJECT_NAME, CREATED_AT FROM {app_name}.api.data_streams
                    WHERE RAI_DATABASE = '{PYREL_ROOT_DB}'
                ) ds
                RIGHT JOIN (
                    SELECT
                        (TABLE_CATALOG || '.' || TABLE_SCHEMA || '.' || TABLE_NAME) as FQN,
                        CONVERT_TIMEZONE('UTC', LAST_DDL) AS LAST_DDL,
                        TABLE_TYPE as KIND
                    FROM {db}.INFORMATION_SCHEMA.TABLES
                        WHERE (UPPER(TABLE_SCHEMA), UPPER(TABLE_NAME)) IN (
                        {','.join(f"('{schema.upper()}', '{table.upper()}')"
                        for schema, tables in schemas.items()
                        for table in tables)}
                        )
                ) inf on inf.FQN = ds.FQ_OBJECT_NAME
            """
            for db, schemas in partitioned_sources.items()
        ) + ";"
        source_types: dict[str, SourceInfo] = {source.upper(): cast(SourceInfo, {"type": None, "state": ""}) for source in sources}
        for row in self.resources._exec(query):
            # Unlike SHOW OBJECTS, querying the info schema directly calls them BASE TABLE
            source_types[row['FQN'].upper()] = {"type": "TABLE" if row['KIND'] == "BASE TABLE" else row['KIND'], "state": row['STATE']}

        return source_types

    def _get_source_references(self, source_info: dict[str, SourceInfo]):
        app_name = self.resources.get_app_name()
        missing_sources = []
        invalid_sources = {}
        source_references = []
        for source, info in source_info.items():
            if info['type'] is None:
                missing_sources.append(source)
            elif info['type'] not in ("TABLE", "VIEW"):
                invalid_sources[source] = info['type']
            else:
                source_references.append(f"{app_name}.api.object_reference('{info['type']}', '{source}')")

        if missing_sources:
            debugging.warn(UnknownSourceWarning(missing_sources))

        if invalid_sources:
            debugging.warn(InvalidSourceTypeWarning(invalid_sources))

        return source_references

    def create_database(self, isolated=True, nowait_durable=True):
        assert isinstance(self.resources, Resources)

        if self.last_database_version == len(self.resources.sources):
            return

        app_name = self.resources.get_app_name()
        model = self._source_database
        engine_name = self.resources.get_default_engine_name()

        with debugging.span("poll_use_index", sources=self.resources.sources, model=model, engine=engine_name):
            self.poll_use_index(app_name, self.resources.sources, model, engine_name)

        self.last_database_version = len(self.resources.sources)
        self._manage_packages()

    # Polling for use_index
    # if data is ready, break the loop
    # if data is not ready, print the status of the tables or engines
    # if data is not ready and there are errors, collect the errors and raise exceptions
    def poll_use_index(
        self, app_name: str, sources: Iterable[str], model: str, engine_name: str
    ):
        counter = 1
        tables_with_not_enabled_change_tracking = []
        table_objects_with_other_errors = []
        engine_errors = []

        source_info = self._get_source_info(sources)
        # Source tables that have been altered/changed since the last stream creation
        stale_sources = [source.upper() for source, info in source_info.items() if info["state"] == 'STALE']


        with SpanSpinner("validate_sources", "Validating sources...", "Sources validated", leading_newline=True) as spinner:
            if stale_sources:
                # We have to ensure we have an engine available while deleting the stream
                # in order to clear the base relations. We can remove this once use index
                # cloning is capable of properly whitelisting source relations.
                # We only do this conditionally because it's better to allow it to provision
                # in parallel as part of the use index polling.
                cast(Resources, self.resources).auto_create_engine()
                for source in stale_sources:
                    try:
                        # Delete all stale streams one by one, so use_index could recreate them again
                        query = f"CALL {app_name}.api.delete_data_stream('{source}', '{PYREL_ROOT_DB}');"
                        self.resources._exec(query)
                    except Exception as e:
                        if "data stream does not exist" in str(e).lower():
                            pass
                        else:
                            raise e from None

            # Check if all stale streams have been deleted successfully
            def check_on_deleted_streams():
                result = True
                if stale_sources:
                    query = f"""
                        SELECT UPPER(FQ_OBJECT_NAME)
                        FROM {app_name}.api.data_streams
                        WHERE RAI_DATABASE = '{PYREL_ROOT_DB}' AND
                        FQ_OBJECT_NAME IN ({','.join(f"'{source}'" for source in stale_sources)});
                    """
                    results = self.resources._exec(query)
                    if results:
                        result = False
                return result

            # Poll until we can confirm all stale streams are deleted
            poll_with_specified_overhead(check_on_deleted_streams, overhead_rate=0.1, max_delay=0.5, timeout=600)

        source_references = self._get_source_references(source_info)
        sources_object_references_str = ", ".join(source_references)

        def check_ready(spinner):
            nonlocal counter, tables_with_not_enabled_change_tracking, table_objects_with_other_errors, engine_errors

            sql_string = f"CALL {app_name}.api.use_index([{sources_object_references_str}], {{'model': '{model}', 'engine': '{engine_name}'}});"

            with debugging.span("wait", counter=counter) as span:
                results = self.resources._exec(sql_string)

                # Extract the JSON string from the `USE_INDEX` field
                use_index_json_str = results[0]["USE_INDEX"]

                # Convert the JSON string to lowercase
                use_index_json_str = use_index_json_str.lower()

                # Parse the JSON string into a Python dictionary
                use_index_data = json.loads(use_index_json_str)
                span.update(use_index_data)

                all_data = use_index_data.get("data", [])
                ready = use_index_data.get("ready", False)
                engines = use_index_data.get("engines", [])
                errors = use_index_data.get("errors", [])

                break_loop = False

                if ready:
                    break_loop = True
                    spinner.update_messages(
                        {
                            "finished_message": "Setup complete",
                        }
                    )

                if not ready and all_data:
                    for data in all_data:
                        if data.get("errors", []):
                            for error in data.get("errors", []):
                                error_msg = f"{error.get('error')}, source: {error.get('source')}"
                                table_objects_with_other_errors.append(
                                    SnowflakeTableObject(
                                        error_msg, data.get("fq_object_name")
                                    )
                                )
                            break_loop = True

                        if data.get("data_sync_status") == "created":
                            spinner.update_messages(
                                {
                                    "message": f"Preparing {data.get('fq_object_name')}...",
                                }
                            )
                        if (
                            data.get("data_sync_status") != "synced"
                            or data.get("pending_batches_count") > 0
                        ):
                            batches_count = data.get("pending_batches_count")

                            if batches_count:
                                spinner.update_messages(
                                    {
                                        "message": f"Preparing {data.get('fq_object_name')}, remaining batches: {data.get('pending_batches_count')}...",
                                    }
                                )
                            else:
                                spinner.update_messages(
                                    {
                                        "message": f"Preparing {data.get('fq_object_name')}...",
                                    }
                                )

                    counter += 1

                if not ready and engines:
                    for engine in engines:
                        if (
                            engine.get("state", "") == "pending"
                            or engine.get("status", "") == "pending"
                        ):
                            writer = engine.get("writer", False)
                            message = f"Waiting for {writer and 'writer engine' or 'engine'} to be initialized..."
                            spinner.update_messages(
                                {
                                    "message": message,
                                }
                            )
                        if (
                            engine.get("state", "") == "suspended"
                            or engine.get("status", "") == "suspended"
                        ):
                            message = f"Resuming engine {engine.get('name')}"
                            spinner.update_messages(
                                {
                                    "message": message,
                                }
                            )
                            try:
                                self.resources.resume_engine(engine.get("name"))
                            except Exception:
                                raise EngineResumeFailed(engine.get("name"))

                    counter += 1

                if not ready and errors:
                    for error in errors:
                        if error.get("type") == "data":
                            if (
                                "change_tracking"
                                in error.get("message", "").lower()
                                or "change tracking"
                                in error.get("message", "").lower()
                            ):
                                err_source = error.get("source").upper()
                                err_source_type = source_info.get(err_source, {}).get("type")
                                tables_with_not_enabled_change_tracking.append((err_source, err_source_type))
                            else:
                                table_objects_with_other_errors.append(
                                    SnowflakeTableObject(
                                        error.get("message"), error.get("source")
                                    )
                                )
                        elif error.get("type") == "engine":
                            engine_errors.append(error)
                    break_loop = True

                return break_loop

        def poll_ready(spinner):
            poll_with_specified_overhead(lambda: check_ready(spinner), overhead_rate=0.1, max_delay=1)

        with Spinner(
            "Preparing your data...",
            "Data preparation complete",
            leading_newline=True,
            trailing_newline=True,
        ) as spinner:
            poll_ready(spinner)

            num_tables_altered = 0

            if (
                tables_with_not_enabled_change_tracking
                and self._config.get("ensure_change_tracking", False)
            ):
                for table in tables_with_not_enabled_change_tracking:
                    try:
                        fqn, kind = table
                        self.resources._exec(f"ALTER {kind} {fqn} SET CHANGE_TRACKING = TRUE;")
                        tables_with_not_enabled_change_tracking.remove(table)
                        num_tables_altered += 1
                    except Exception:
                        pass

            if tables_with_not_enabled_change_tracking:
                spinner.update_messages(
                    {
                        "message": "Errors found. See below for details.",
                    }
                )
                raise SnowflakeChangeTrackingNotEnabledException(
                    tables_with_not_enabled_change_tracking
                )

            if table_objects_with_other_errors:
                spinner.update_messages(
                    {
                        "message": "Errors found. See below for details.",
                    }
                )
                raise SnowflakeTableObjectsException(table_objects_with_other_errors)
            if engine_errors:
                spinner.update_messages(
                    {
                        "message": "Errors found. See below for details.",
                    }
                )
                # if there is an engine error, probably auto create engine failed
                raise EngineAutoCreateFailed(engine_name)

            if num_tables_altered > 0:
                s = "s" if num_tables_altered > 1 else ""
                spinner.update_messages(
                    {
                        "message": f"Enabled change tracking on {num_tables_altered} table{s}. Still preparing your data...",
                    }
                )
                poll_ready(spinner)


#--------------------------------------------------
# Graph
#--------------------------------------------------

def Graph(
    name,
    *,
    profile: str | None = None,
    config: Config,
    dry_run: bool = False,
    isolated: bool = True,
    connection: Session | None = None,
    keep_model: bool = False,
    nowait_durable: bool = True,
    format: str = "default",
):

    client_class = Client
    use_graph_index = config.get("use_graph_index", USE_GRAPH_INDEX)
    use_monotype_operators = config.get("compiler.use_monotype_operators", False)

    if use_graph_index:
        client_class = SnowflakeClient
    client = client_class(
        Resources(profile, config, connection),
        rel.Compiler(config),
        name,
        config,
        dry_run=dry_run,
        isolated=isolated,
        keep_model=keep_model,
        nowait_durable=nowait_durable
    )
    base_rel = """
        @inline
        def make_identity(x..., z):
            exists((u) | hash128({x...}, x..., u) and
            hash_value_uint128_convert(u, z))

        @inline
        def pyrel_default({F}, c, k..., v):
            F(k..., v) or (not F(k..., _) and v = c)

        @inline
        def pyrel_unwrap(x in UInt128, y): y = x

        @inline
        def pyrel_dates_period_days(x in Date, y in Date, z in Int):
            exists((u) | dates_period_days(x, y , u) and u = ::std::common::^Day[z])

        @inline
        def pyrel_datetimes_period_milliseconds(x in DateTime, y in DateTime, z in Int):
            exists((u) | datetimes_period_milliseconds(x, y , u) and u = ^Millisecond[z])

        @inline
        def pyrel_bool_filter(a, b, {F}, z): { z = if_then_else[F(a, b), boolean_true, boolean_false] }

        @inline
        def pyrel_strftime(v, fmt, tz in String, s in String):
            (Date(v) and s = format_date[v, fmt])
            or (DateTime(v) and s = format_datetime[v, fmt, tz])

        @inline
        def pyrel_regex_match_all(pattern, string in String, pos in Int, offset in Int, match in String):
            regex_match_all(pattern, string, offset, match) and offset >= pos

        @inline
        def pyrel_regex_match(pattern, string in String, pos in Int, offset in Int, match in String):
            pyrel_regex_match_all(pattern, string, pos, offset, match) and offset = pos

        @inline
        def pyrel_regex_search(pattern, string in String, pos in Int, offset in Int, match in String):
            enumerate(pyrel_regex_match_all[pattern, string, pos], 1, offset, match)

        @inline
        def pyrel_regex_sub(pattern, repl in String, string in String, result in String):
            string_replace_multiple(string, {(last[regex_match_all[pattern, string]], repl)}, result)

        @inline
        def pyrel_capture_group(regex in Pattern, string in String, pos in Int, index, match in String):
            (Integer(index) and capture_group_by_index(regex, string, pos, index, match)) or
            (String(index) and capture_group_by_name(regex, string, pos, index, match))

        declare __resource
        declare __compiled_patterns
    """
    if use_monotype_operators:
        base_rel += """

        // use monotyped operators
        from ::std::monotype import +, -, *, /, <, <=, >, >=
        """
    pyrel_base = dsl.build.raw_task(base_rel)
    debugging.set_source(pyrel_base)
    client.install("pyrel_base", pyrel_base)
    return dsl.Graph(client, name, format=format)
