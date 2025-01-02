import reflex as rx
from .backend import Suppliers, States
from sqlmodel import update
from sqlalchemy import func


class StatesHeads(rx.State):
    nro_orders: str = ""
    total_orders: float = 0.0
    comissions: float = 0.0
    dialog_message: str = ""
    show_dialog: bool = False

    def set_nro_orders(self, value: str):
        self.nro_orders = value

    def set_total_orders(self, value: str):
        self.total_orders = float(value)

    def set_comissions(self, value: str):
        self.comissions = float(value)

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

                    self.dialog_message = "Actualización exitosa!"
                    self.show_dialog = True

                except Exception as e:
                    session.rollback()
                    self.dialog_message = f"Error al actualizar: {str(e)}"
                    self.show_dialog = True
                return States.get_all_heads
