from __future__ import annotations

from pathlib import Path
from re import error as RegexError  # noqa


def _get_version():
    root = Path(__file__).resolve().parents[1]
    if (root / ".git").exists() and not (root / ".git/shallow").exists():
        try:
            import setuptools_scm  # noqa

            return setuptools_scm.get_version(root=str(root))
        except (ImportError, RegexError, LookupError):
            pass
    try:
        from ._version import version

        return version
    except ImportError:
        return "0.0.0-unknown"


__version__: str = _get_version()
__semver__: str = __version__.split("+")[0]
