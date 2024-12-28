import reflex as rx
from ..backend.backend import States


def modal_status_heads() -> rx.Component:
    return rx.dialog.content(
        rx.dialog.title(
            "Children's Orders",
            text_align="center",  # Centra el texto
            width="100%"  # Asegura que tome todo el ancho disponible
        ),
        rx.dialog.description(
            rx.vstack(
                # Usando foreach para iterar sobre children_orders
                rx.foreach(
                    States.children_orders,
                    lambda x: rx.text(
                        f"{x.childrenname}: {x.ordersmonth}",
                        size="3"
                    )
                ),
                spacing="3",
                align="start"
            )
        ),
        rx.flex(
            rx.dialog.close(
                rx.button(
                    "Volver",
                    variant="soft",
                    color_scheme="gray",
                    margin_top="2em"
                ),
            ),
            spacing="3",
            justify="center",
        ),
        max_width="400px",
        size="4"
    )
