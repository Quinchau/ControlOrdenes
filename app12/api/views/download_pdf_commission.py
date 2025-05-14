from fastapi import APIRouter
import reflex as rx
from fastapi.responses import FileResponse
import os
from datetime import datetime

router = APIRouter()

async def get_supplier_doc(supplier_id: str):
    clean_supplier_id = supplier_id.rstrip('/')
    file_path = rx.get_upload_dir() / f"{clean_supplier_id}_document.pdf"
    print(f"Buscando archivo en: {file_path}")
    if os.path.exists(file_path):
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d_%H%M%S")
        new_filename = f"{clean_supplier_id}_document_{timestamp}.pdf"
        return FileResponse(
            file_path,
            media_type="application/pdf",
            filename=new_filename,
            headers={"Cache-Control": "no-store"}  # Evita que el navegador almacene la respuesta
        )
    else:
        print(f"Archivo no encontrado: {file_path}")
        return {"error": "Document not found"}