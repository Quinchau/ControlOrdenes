import reflex as rx
from ..backend.backend import States


def modal_status() -> rx.Component:
    return rx.dialog.content(
        rx.dialog.title("Detalles de la Orden"),
        rx.dialog.description(
            rx.flex(
                rx.text(f"Referencia: {
                    States.selected_order.orderref}"),
                rx.hstack(rx.text("Tracking: "),
                          rx.cond(
                    States.selected_order.requisitionno,
                    rx.link(
                        States.selected_order.requisitionno,
                        href=States.selected_order.urltracking,
                        is_external=True
                    ),
                    rx.text("")
                )
                ),
                rx.text(f"Proveedor: {
                    States.selected_order.supplierno}"),
                rx.text(f"Deladd1: {
                    States.selected_order.deladd1}"),
                rx.text(f"Deladd2: {
                    States.selected_order.deladd2}"),
                rx.text(f"Comentarios: {
                    States.selected_order.comments}"),
                rx.text(f"Fecha: {States.selected_order.orddate}"),
                # rx.text(f"Estado: {States.selected_order.status}"),
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
                ),
            ),
            rx.dialog.close(
                rx.button(
                    "Marcar como Recibido",
                    on_click=States.handle_delivered(
                        States.selected_order.orderno),
                ),
            ),
            spacing="3",
            justify="center",
        ),
        max_width="400px",
        size="4"
    )
