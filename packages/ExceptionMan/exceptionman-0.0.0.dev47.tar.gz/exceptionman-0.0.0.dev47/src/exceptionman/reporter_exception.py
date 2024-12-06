from __future__ import annotations as _annotations

from typing import TYPE_CHECKING as _TYPE_CHECKING

from exceptionman import _traceback

if _TYPE_CHECKING:
    from mdit.document import Document


class ReporterException(Exception):
    """Base exception class with HTML reporting capabilities."""

    def __init__(self, report: Document):
        super().__init__()
        self.report = report
        if not _traceback.USER_INSTALLED:
            _traceback.install(temporary=True)
        return

    def __rich__(self) -> str:
        return self.report.render(target="console", filters="console")
