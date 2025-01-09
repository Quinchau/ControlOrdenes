import reflex as rx
from fastapi.responses import FileResponse
import os


async def get_supplier_doc(supplier_id: str):
    # Construct filename
    filename = f"{supplier_id}_document.pdf"
    # Path to assets folder
    file_path = os.path.join("uploaded_files", filename)

    # Check if file exists
    if os.path.exists(file_path):
        return FileResponse(
            file_path,
            media_type="application/pdf",
            filename=filename
        )
    else:
        return {"error": "Document not found"}
