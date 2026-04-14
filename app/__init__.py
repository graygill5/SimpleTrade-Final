"""Compatibility package.

Allows running `uvicorn app.main:app` from repository root by extending
`app` package path to include `backend/app`.
"""

from pathlib import Path

_backend_app = Path(__file__).resolve().parent.parent / "backend" / "app"
if _backend_app.exists():
    __path__.append(str(_backend_app))
