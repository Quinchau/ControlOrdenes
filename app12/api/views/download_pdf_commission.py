import reflex as rx
from fastapi.responses import FileResponse
import os
from datetime import datetime

async def get_supplier_doc(supplier_id: str):
    file_path = rx.get_upload_dir() / f"{supplier_id}_document.pdf"

    # Check if file exists
    if os.path.exists(file_path):
        # Get current timestamp to append to the filename
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d_%H%M%S")
        new_filename = f"{supplier_id}_document_{timestamp}.pdf"

        return FileResponse(
            file_path,
            media_type="application/pdf",
            filename=new_filename  # Use the new filename with timestamp
        )
    else:
        return {"error": "Document not found"}