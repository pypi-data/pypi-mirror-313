from __future__ import annotations
import ast
import contextlib
import datetime
import json
from typing import Dict, Generator
import logging
import uuid
import warnings

import numpy as np
from pandas import DataFrame

from relationalai.environments import runtime_env
from relationalai.environments.base import SourceInfo, find_block_in
from relationalai.util import get_timestamp
from relationalai.util.constants import SPAN_FILTER_ATTRS
from .metamodel import Action, Task

find_block_in = find_block_in # re-export

DEBUG = True
handled_error = None

#--------------------------------------------------
# Log Formatters
#--------------------------------------------------

def encode_log_message(obj):
    if isinstance(obj, DataFrame):
        # Replace NaN with None to avoid JSON serialization issues
        df = obj.replace({np.nan: None})
        return df.head(20).to_dict(orient="records")
    if isinstance(obj, datetime.datetime):
        return obj.isoformat() + "Z"
    if isinstance(obj, dict):
        return {k: encode_log_message(v) for k, v in obj.items()}
    if hasattr(obj, "to_dict"):
        return obj.to_dict()
    if hasattr(obj, "to_json"):
        return obj.to_json()
    else:
        return str(obj)

class JsonFormatter(logging.Formatter):
    def format(self, record):
        return json.dumps(record.msg, default=encode_log_message)

#--------------------------------------------------
# Logging
#--------------------------------------------------

logger = logging.getLogger("pyrellogger")
logger.setLevel(logging.DEBUG)
logger.propagate = False

#--------------------------------------------------
# File Logger
#--------------------------------------------------

class FlushingFileHandler(logging.FileHandler):
    def emit(self, record):
        super().emit(record)
        self.flush()

with open('debug.jsonl', 'w'):
    pass

# keep the old file-based debugger around and working until it's fully replaced.
if DEBUG:
    file_handler = FlushingFileHandler('debug.jsonl', mode='a')
    file_handler.setFormatter(JsonFormatter())
    logger.addHandler(file_handler)

#--------------------------------------------------
# Debug Spans
#--------------------------------------------------

# The deepest span in the tree
TIP_SPAN: 'Span | None' = None

def get_current_span_id() -> str | None:
    if TIP_SPAN is None:
        return None
    return str(TIP_SPAN.id)

def span_start(type: str, **kwargs) -> 'Span':
    global TIP_SPAN
    span = Span(type, TIP_SPAN, kwargs)
    TIP_SPAN = span

    if DEBUG:
        logger.debug({"event": "span_start", "span": span})

    return span

def span_end(span):
    if not DEBUG or span is None:
        return

    global TIP_SPAN
    TIP_SPAN = span.parent
    span.mark_finished()

    logger.debug({
        "event": "span_end",
        "id": str(span.id),
        "end_timestamp": span.end_timestamp.isoformat() + "Z",
        "end_attrs": span.end_attrs,
    })

def span_flush():
    while TIP_SPAN:
        span_end(TIP_SPAN)


class Span:
    def __init__(self, type: str, parent, attrs: Dict):
        self.id = uuid.uuid4()
        self.parent = parent
        self.type = type
        self.attrs = attrs
        # additional attributes added during the lifetime of the span
        self.end_attrs = {}
        self.start_timestamp = get_timestamp()
        self.end_timestamp = None

    def mark_finished(self):
        self.end_timestamp = get_timestamp()

    def __setitem__(self, key, value):
        self.end_attrs[key] = value

    def update(self, attrs: Dict):
        if attrs:
            self.end_attrs = {**self.end_attrs, **attrs}

        return self

    def to_json(self):
        return {
            "type": self.type,
            "id": str(self.id),
            "parent_id": str(self.parent.id) if self.parent else None,
            "start_timestamp": self.start_timestamp.isoformat() + "Z",
            "end_timestamp": None if self.end_timestamp is None else (self.end_timestamp.isoformat() + "Z"),
            "attrs": self.attrs,
        }

@contextlib.contextmanager
def span(type: str, **kwargs) -> Generator[Span]:
    cur = span_start(type, **kwargs)
    try:
        yield cur
    except Exception as err:
        error(err)
        raise
    finally:
        span_end(cur)

def set_span_attr(attr, value):
    global TIP_SPAN
    assert TIP_SPAN, "Unable to set span attribute outside of any span"
    TIP_SPAN.attrs[attr] = value

def filter_span_attrs(source_attrs: Dict):
    return {k: v for k, v in source_attrs.items() if k not in SPAN_FILTER_ATTRS}

#--------------------------------------------------
# Debug Events
#--------------------------------------------------

EMPTY = {}

def event(event:str, parent:Span|None = None, **kwargs):
    if not DEBUG:
        return

    if not parent:
        parent = TIP_SPAN

    d = {
        "event":event,
        "timestamp": get_timestamp(),
        "parent_id": parent.id if parent else None,
        **kwargs
    }
    logger.debug(d)

def time(type:str, elapsed:float, results:DataFrame = DataFrame(), **kwargs):
    if DEBUG:
        event("time", type=type, elapsed=elapsed, results={
            "values": results,
            "count": len(results)
        }, **kwargs)

def error(err: BaseException):
    global handled_error
    from relationalai.errors import RAIExceptionSet
    if err != handled_error and not isinstance(err, RAIExceptionSet):
        # Prepare kwargs from exception attributes if it's a custom exception
        kwargs = {}

        if hasattr(err, '__dict__'):
            kwargs = {key: getattr(err, key) for key in err.__dict__ if not key.startswith('_')}

        event("error", err=err, span_id=get_current_span_id(), **kwargs)  # Emit the error event only if it's a new or different error
        for handler in logger.handlers:
            handler.flush()
        handled_error = err

def handle_compilation(compilation):
    if not DEBUG:
        return

    (file, line, block) = compilation.get_source()
    source = {"file": file, "line": line, "block": block, "task_id": compilation.task.id}
    passes = [{"name": p[0], "task": p[1], "elapsed": p[2]} for p in compilation.passes]
    emitted = compilation.emitted
    if isinstance(emitted, list):
        emitted = "\n\n".join(emitted)

    event("compilation", source=source, task=compilation.task, passes=passes, emitted=emitted, emit_time=compilation.emit_time)


def warn(warning: Warning, already_dispatched = False):
    # @TODO: Double-check that the warnings.warn path works for snowbook, otherwise call report_alerts manually
    if not already_dispatched:
        warnings.warn(warning)

    if not DEBUG:
        return

    kwargs = {}

    if hasattr(warning, "__dict__"):
        kwargs = {
            key: getattr(warning, key)
            for key in warning.__dict__
            if not key.startswith("_")
        }

    event("warn", warning=warning, **kwargs)

#--------------------------------------------------
# Position capture
#--------------------------------------------------

def check_errors(task:Task|Action):
    class ErrorFinder(ast.NodeVisitor):
        def __init__(self, start_line):
            self.errors = []
            self.start_line = start_line

        def to_line_numbers(self, node):
            return (node.lineno, node.end_lineno)

        def generic_visit(self, node):
            if isinstance(node, ast.If):
                from relationalai.errors import InvalidIfWarning
                InvalidIfWarning(task, *self.to_line_numbers(node))
            elif isinstance(node, ast.For) or isinstance(node, ast.While):
                from relationalai.errors import InvalidLoopWarning
                InvalidLoopWarning(task, *self.to_line_numbers(node))
            elif isinstance(node, ast.Try):
                from relationalai.errors import InvalidTryWarning
                InvalidTryWarning(task, *self.to_line_numbers(node))

            ast.NodeVisitor.generic_visit(self, node)

    source = get_source(task)
    if not source or not source.block:
        return
    ErrorFinder(source.line).visit(source.block)

sources:Dict[Task|Action, SourceInfo|None] = {}
def set_source(item, steps=1, dynamic=False):
    if not DEBUG or item in sources:
        return
    found = runtime_env.get_source()
    if found:
        sources[item] = found
        if not dynamic:
            check_errors(item)
            pass
    return found

def get_source(item):
    return sources.get(item)
