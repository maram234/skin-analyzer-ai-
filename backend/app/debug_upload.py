"""
Lightweight debug endpoint for manual image upload tests.

This keeps debug utilities inside the backend app package while the
main production API remains in `api.py`.
"""

from fastapi import UploadFile, File

from .api import app


@app.post("/debug/upload")
async def debug_upload(file: UploadFile = File(...)):
    """
    Simple debug route that just returns basic info about the uploaded file.
    Safe to leave deployed but not used by the main UI.
    """
    return {
        "filename": file.filename,
        "content_type": file.content_type,
    }

