from __future__ import annotations
import os
import sys
import warnings

from .base import RuntimeEnvironment, SourceInfo, find_external_frame, handle_rai_exception, handle_rai_warning, patch

class GenericEnvironment(RuntimeEnvironment):
    @classmethod
    def detect(cls):
        return True

    def get_source(self, steps:int|None = None):
        caller_frame = find_external_frame(steps)
        if not caller_frame:
            return

        caller_filename = caller_frame.f_code.co_filename
        caller_line = caller_frame.f_lineno

        relative_filename = os.path.relpath(caller_filename, os.getcwd())

        source_code = None
        try:
            # Read the source code from the caller's file
            with open(caller_filename, "r") as f:
                source_code = f.read()
        except Exception:
            pass

        return SourceInfo.from_source(relative_filename, caller_line, source_code)

    def _patch(self):
        @patch(warnings, "showwarning")
        def _(original, message, category, filename, lineno, file=None, line=None):
            if not handle_rai_warning(message):
                original(message, category, filename, lineno, file, line)

        @patch(sys, "excepthook")
        def _(original, exc_type, exc_value, exc_traceback, quiet=False):
            handle_rai_exception(exc_value)
            original(exc_type, exc_value, exc_traceback)
