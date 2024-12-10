import reflex as rx
from ..backend.backend import States


def _badge(icon: str, text: str):
    return rx.flex(
        rx.icon(icon, size=16),
        text,
        align_items="center",
        gap="4px",
        padding="x-2 y-1",
        color="black"
    )


def status_button(status: str, orderno: str):
    badge_mapping = {
        "Delivered": ("check", "Delivered", "#00FF7F"),
        "On the way": ("loader", "On the way", "#FFF8DC"),
        "On Hold": ("ban", "On Hold", "#E52B50"),
        "Received": ("check", "Received", "#87CEEB"),
    }

    icon, text, color = badge_mapping.get(
        status, ("loader", "On the way", "#FFF8DC"))

    if status == "Delivered":
        return rx.dialog.root(
            rx.dialog.trigger(
                rx.button(
                    _badge(icon, text),
                    border_radius="20px",
                    opacity=1,
                    bg=color,
                    color="white",
                    _hover={"bg": "darken", "color": "white"},
                    on_click=States.show_order_details(orderno)
                )
            ),
            rx.dialog.content(
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
            ),
        )
    else:
        return rx.button(
            _badge(icon, text),
            border_radius="20px",
            opacity=1,
            bg=color,
            color="white",
            _hover={"bg": "darken", "color": "white"}
        )
