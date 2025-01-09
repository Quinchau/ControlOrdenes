from fastapi import APIRouter
from .views.download_pdf_commission import get_supplier_doc

router = APIRouter()
router.get("/api/supplier-doc/{supplier_id}", get_supplier_doc)
