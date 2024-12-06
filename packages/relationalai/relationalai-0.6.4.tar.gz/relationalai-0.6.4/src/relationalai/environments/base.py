from __future__ import annotations
from abc import ABC, abstractmethod
import ast
from dataclasses import dataclass, field
from functools import wraps
import inspect
import os
import textwrap
from typing import Any, Type

from relationalai.clients.config import Config

def noop(*_, **__):
    ...

def patch(target, name):
    "Given the `target` class or module, replace method `name` with the decorated wrapper fn."
    original = getattr(target, name, noop)

    def decorator(f):
        @wraps(original)
        def wrapped(*args, **kwargs):
            return f(original, *args, **kwargs)

        setattr(target, name, wrapped)
        return wrapped

    return decorator

def except_return(exc_type: Type[Exception], default):
    "Catch exceptions like `exc_type` and return `default` instead."
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                return fn(*args, **kwargs)
            except exc_type:
                return default
        return wrapper
    return decorator

#--------------------------------------------------
# SourceInfo
#--------------------------------------------------

@dataclass
class SourceInfo:
    file: str = field(default="Unknown")
    line: int = field(default=0)
    source: str = field(default="")
    block: ast.AST|None = None
    source_start_line:int = 0

    def modify(self, transformer:ast.NodeTransformer):
        if not self.block:
            from .. import debugging
            debugging.warn(Warning(f"Cannot find source to provide quick fix suggestions at {self.file}:{self.line}"))
            return

        new_block = transformer.visit(self.block)
        new = SourceInfo(self.file, self.line, ast.unparse(new_block), new_block)
        new.source_start_line = self.source_start_line
        return new

    def to_json(self):
        return {
            "file": self.file,
            "line": self.line,
            "source": self.source
        }

    @classmethod
    def from_source(cls, filename: str, line: int|None, code: str|None):
        line = line or 0
        if not code:
            return cls(filename, line, "")
        else:
            return find_block_in(code, line, filename)

rai_site_packages = os.path.join("site-packages", "relationalai")
rai_src = os.path.join("src", "relationalai")
rai_zip = os.path.join(".", "relationalai.zip", "relationalai")

def first_non_relationalai_frame(frame):
    while frame and frame.f_back:
        file = frame.f_code.co_filename
        if rai_site_packages not in file and rai_src not in file and rai_zip not in file:
            break
        frame = frame.f_back
    return frame

def find_external_frame(steps:int|None = None):
    caller_frame = inspect.currentframe()
    if steps is not None:
        for _ in range(steps):
            if not caller_frame or not caller_frame.f_back:
                break
            caller_frame = caller_frame.f_back
    else:
        caller_frame = first_non_relationalai_frame(caller_frame)

    return caller_frame

def find_block_in(source_code: str, caller_line: int, relative_filename: str):
    # Parse the source code into an AST
    tree = ast.parse(source_code)

    # Find the node that corresponds to the call
    class BlockFinder(ast.NodeVisitor):
        def __init__(self, target_lineno):
            self.target_lineno = target_lineno
            self.current_with_block = None
            self.block_node = None

        def visit_With(self, node):
            # Check if the with statement calls model.query() or model.rule()
            if self.is_model_query_or_rule(node.items[0].context_expr):
                # Save the current with block
                previous_with_block = self.current_with_block
                self.current_with_block = node

                # Check if the target line is within this with block
                if node.lineno <= self.target_lineno <= max(getattr(child, "lineno") for child in ast.walk(node) if hasattr(child, 'lineno')):
                    if self.block_node is None:
                        self.block_node = node

                # Visit children
                self.generic_visit(node)

                # Restore the previous with block
                self.current_with_block = previous_with_block
            else:
                # If it's not a model.query() or model.rule() call, just visit children
                self.generic_visit(node)

        def is_model_query_or_rule(self, node):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute):
                    return node.func.attr in ['query', 'rule']

        def generic_visit(self, node):
            if hasattr(node, "lineno") and getattr(node, "lineno") == self.target_lineno:
                if self.block_node is None:
                    self.block_node = self.current_with_block or node
            ast.NodeVisitor.generic_visit(self, node)

    finder = BlockFinder(caller_line)
    finder.visit(tree)

    if finder.block_node:
        # Extract the lines from the source code
        start_line = getattr(finder.block_node, "lineno", None)
        assert start_line is not None, "Could not find range of block node"
        end_line = getattr(finder.block_node, "end_lineno", start_line)

        block_lines = source_code.splitlines()[start_line - 1:end_line]
        block_code = "\n".join(block_lines)
        return SourceInfo(relative_filename, caller_line, textwrap.dedent(block_code), finder.block_node, source_start_line=start_line)

    lines = source_code.splitlines()
    if caller_line > len(lines):
        return SourceInfo(relative_filename, caller_line)
    return SourceInfo(relative_filename, caller_line, lines[caller_line - 1])

#--------------------------------------------------
# Warnings & Exceptions Display
#--------------------------------------------------

def handle_rai_warning(warning: Warning):
    from ..errors import RAIWarning
    from .. import debugging

    debugging.warn(warning, True)

    if not isinstance(warning, RAIWarning):
        return False

    warning.pprint()
    return True

def handle_rai_exception(exc: BaseException):
    global handled_error
    handled_error = None

    from ..errors import RAIException, RAIExceptionSet
    from .. import debugging

    if not isinstance(exc, RAIException):
        return False

    for err in exc.exceptions if isinstance(exc, RAIExceptionSet) else [exc]:
        err.pprint()
        debugging.error(err)

    return True

#--------------------------------------------------
# RuntimeEnvironment
#--------------------------------------------------

class RuntimeEnvironment(ABC):
    remote = False

    def __init__(self):
        self._patch()

    @classmethod
    @abstractmethod
    def detect(cls) -> bool:
        ...

    @abstractmethod
    def get_source(self, steps:int|None = None) -> SourceInfo|None:
        ...

    def _patch(self):
        ...

@dataclass
class NotebookCell():
    id: str
    name: str
    content: str
    _native: Any|None = None

    def get_source(self, steps: int | None = None) -> SourceInfo | None:
        caller_frame = find_external_frame(steps)
        caller_line = caller_frame.f_lineno if caller_frame else None
        return SourceInfo.from_source(self.name, caller_line, self.content)

class NotebookRuntimeEnvironment(RuntimeEnvironment, ABC):
    def __init__(self):
        super().__init__()
        self.cells: dict[str|None, NotebookCell] = dict()
        self.dirty_cells: set[str] = set()

    @abstractmethod
    def active_cell_id(self) -> str|None:
        ...

    def update_cell(self, cell: NotebookCell|None):
        if cell:
            self.dirty_cells.add(cell.id)
            self.cells[cell.id] = cell

    def cell(self, id: str|None = None) -> NotebookCell|None:
        return self.cells.get(id if id else self.active_cell_id())

    def get_source(self, steps: int | None = None) -> SourceInfo | None:
        cell = self.cell()
        return cell.get_source(steps) if cell else None

class SessionEnvironment(RuntimeEnvironment, ABC):
    @abstractmethod
    def configure_session(self, config: Config, session: Any|None = None) -> Any:
        ...
