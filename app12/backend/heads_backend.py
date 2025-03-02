import reflex as rx
from .backend import Suppliers, States
from sqlmodel import update
from sqlalchemy import func


class StatesHeads(rx.State):
    nro_orders: str = ""
    total_orders: float = 0.0
    comissions: float = 0.0
    dialog_message: str = ""
    show_dialog_pdf_upload: bool = False
    show_dialog: bool = False
    pdf_path: str = ""
    user_id: str = ""

    @rx.event
    async def set_user_id(self, user_id: str):
        self.user_id = user_id

    @rx.event
    async def handle_pdf_upload(self, files: list[rx.UploadFile]):
        if not files:
            return rx.toast.error("No se seleccionó ningún archivo")
        file = files[0]
        upload_data = await file.read()
        filename = f"{self.user_id}_document.pdf"
        outfile = rx.get_upload_dir() / f"{self.user_id}_document.pdf"
        try:
            with outfile.open("wb") as file_object:
                file_object.write(upload_data)
        except OSError as e:
            return rx.toast.error(f"Error al subir el archivo: {e}")
        self.pdf_path = filename
        return rx.toast.success(f"Archivo subido correctamente en: {outfile}")

    @rx.event
    def pdf_upload(self, value: bool):
        self.show_dialog_pdf_upload = value

    def initialize_state(self, nro_orders, total, comissions):
        """Inicializar el estado con los valores del registro."""
        self.nro_orders = nro_orders
        self.total_orders = total
        self.comissions = comissions

    @rx.event(background=True)
    async def update_comissions_amount_orders(self, id):
        async with self:
            with rx.session() as session:
                try:
                    stmt = update(Suppliers).where(
                        Suppliers.supplierid == id
                    ).values(
                        monthly_fees=self.comissions,
                        monthly_orders_totals=self.total_orders,
                        monthly_orders_numbers=self.nro_orders,
                        lastupdate=func.now()
                    )

                    session.exec(stmt)
                    session.commit()

                except Exception as e:
                    session.rollback()
                    self.dialog_message = f"Error al actualizar: {str(e)}"
                    self.show_dialog = True
                return States.get_all_heads
