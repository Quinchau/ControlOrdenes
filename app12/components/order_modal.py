import reflex as rx
from ..backend.backend import PurchOrders12


def order_details_modal(order: PurchOrders12):
    return rx.dialog.root(
        rx.dialog.trigger(rx.button("Ver Detalles")),
        rx.dialog.content(
            rx.dialog.title("Detalles de la Orden"),
            rx.dialog.description(
                rx.flex(
                    rx.text(f"Orden No: {order.orderno}"),
                    rx.text(f"Referencia: {order.orderref}"),
                    rx.text(f"Requisición: {order.requisitionno}"),
                    rx.text(f"Requisición: {order.urltracking}"),
                    rx.text(f"Proveedor: {order.supplierno}"),
                    rx.text(f"Comentarios: {order.comments}"),
                    rx.text(f"Fecha: {order.orddate}"),
                    rx.text(f"Estado: {order.status}"),
                    direction="column",
                    spacing="3",
                ),
            ),
            rx.dialog.close(
                rx.button("Cerrar", size="3"),
            ),
        ),
    )
