import reflex as rx
from ..backend.backend import States
from ..components.modal_status import modal_status


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

            # Modal para ajuste Status
            modal_status(),
            # Fin de Modal
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
