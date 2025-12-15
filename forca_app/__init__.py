from forca_app.extensions import db

# Expose db at package level so legacy imports like `from . import db` work
__all__ = ["db"]
