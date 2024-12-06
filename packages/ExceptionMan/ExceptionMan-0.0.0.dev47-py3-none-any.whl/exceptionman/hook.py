from __future__ import annotations as _annotations

import sys as _sys
from contextlib import contextmanager as _contextmanager
from typing import TYPE_CHECKING as _TYPE_CHECKING


if _TYPE_CHECKING:
    from types import TracebackType
    from typing import (
        Any,
        Callable,
        Optional,
        Type,
    )


@_contextmanager
def temporary_install(exception_hook: Callable[[Type[BaseException], BaseException, TracebackType], None]) -> None:
    uninstaller = install(exception_hook)
    try:
        yield
    finally:
        uninstaller()
    return


def install(exception_hook) -> Callable[[], Any]:
    try:
        get_ipython()  # type: ignore[name-defined]
        in_ipython = True
    except Exception:
        in_ipython = False
    if in_ipython:
        showtraceback_old, _showtraceback_old, showsyntaxerror_old = ipython_install(exception_hook)
        return lambda: ipython_uninstall(showtraceback_old, _showtraceback_old, showsyntaxerror_old)
    exception_hook_old = terminal_update(exception_hook)
    return lambda: terminal_update(exception_hook_old)


def terminal_update(exception_hook):
    old_hook = _sys.excepthook
    _sys.excepthook = exception_hook
    return old_hook


def ipython_install(exception_hook):

    def ipy_show_traceback(*args: Any, **kwargs: Any) -> None:
        """wrap the default ip.showtraceback to store info for ip._showtraceback"""
        nonlocal tb_data
        tb_data = kwargs
        showtraceback_old(*args, **kwargs)
        return

    def showtraceback_new(*args: Any, is_syntax: bool = False, **kwargs: Any) -> None:
        """Internally called traceback from ip._showtraceback"""
        nonlocal tb_data
        exc_tuple = ipython._get_exc_info()
        # do not display trace on syntax error
        tb: Optional[TracebackType] = None if is_syntax else exc_tuple[2]
        # determine correct tb_offset
        compiled = tb_data.get("running_compiled_code", False)
        tb_offset = tb_data.get("tb_offset", 1 if compiled else 0)
        # remove ipython internal frames from trace with tb_offset
        for _ in range(tb_offset):
            if tb is None:
                break
            tb = tb.tb_next
        exception_hook(exc_tuple[0], exc_tuple[1], tb)
        tb_data = {}  # clear data upon usage
        return

    try:  # pragma: no cover
        # if within ipython, use customized traceback
        ipython = get_ipython()  # type: ignore[name-defined]
    except Exception as e:
        raise RuntimeError("IPython not found") from e

    tb_data = {}  # store information about showtraceback call

    showtraceback_old = getattr(ipython, "showtraceback", None)
    _showtraceback_old = getattr(ipython, "_showtraceback", None)
    showsyntaxerror_old = getattr(ipython, "showsyntaxerror", None)

    ipython.showtraceback = ipy_show_traceback
    ipython._showtraceback = showtraceback_new
    ipython.showsyntaxerror = lambda *args, **kwargs: showtraceback_new(
        *args, is_syntax=True, **kwargs
    )
    return showtraceback_old, _showtraceback_old, showsyntaxerror_old


def ipython_uninstall(showtraceback, _showtraceback, showsyntaxerror):
    try:  # pragma: no cover
        ipython = get_ipython()  # type: ignore[name-defined]
    except Exception:
        return
    for name, value in [
        ("showtraceback", showtraceback),
        ("_showtraceback", _showtraceback),
        ("showsyntaxerror", showsyntaxerror),
    ]:
        if value is None:
            delattr(ipython, name)
        else:
            setattr(ipython, name, value)
    return