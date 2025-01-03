import reflex as rx
from ..backend.heads_backend import StatesHeads


def modal_update_fees_comission(id, name, nro_orders, total, comissions) -> rx.Component:
    return rx.dialog.content(
        rx.dialog.title("Actualizar Montos y Comisiones"),
        rx.dialog.description(
            rx.flex(
                rx.hstack(
                    rx.text("UserId: "),
                    rx.text(id)
                ),
                rx.hstack(
                    rx.text("Name: "),
                    rx.text(name)
                ),
                rx.hstack(
                    rx.text("Childrens with Orders: "),
                    rx.input(
                        value=StatesHeads.nro_orders,
                        on_change=StatesHeads.set_nro_orders
                    )
                ),
                rx.hstack(
                    rx.text("Total Amount: "),
                    rx.input(
                        value=StatesHeads.total_orders,
                        on_change=StatesHeads.set_total_orders
                    )
                ),
                rx.hstack(
                    rx.text("Comissions: "),
                    rx.input(
                        value=StatesHeads.comissions,
                        on_change=StatesHeads.set_comissions
                    )
                ),
                rx.dialog.description(

                ),
                direction="column",
                spacing="3",
                align="start"
            )
        ),
        rx.flex(
            rx.dialog.close(
                rx.button(
                    "Cancelar",
                    variant="soft",
                    color_scheme="gray",
                    margin_top="2em"
                ),
            ),
            rx.dialog.close(
                rx.button(
                    "Guardar",
                    on_click=StatesHeads.update_comissions_amount_orders(id),
                    margin_top="2em"
                ),
            ),
            spacing="3",
            justify="center",
        ),
        max_width="400px",
        size="4"
    )
