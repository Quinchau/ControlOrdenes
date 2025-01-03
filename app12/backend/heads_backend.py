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

                    self.dialog_message = "Actualización exitosa!"
                    self.show_dialog = True

                except Exception as e:
                    session.rollback()
                    self.dialog_message = f"Error al actualizar: {str(e)}"
                    self.show_dialog = True
                return States.get_all_heads
