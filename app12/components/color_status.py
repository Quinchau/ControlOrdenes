import reflex as rx
from ..backend.backend import States
from ..components.modal_status import modal_status, modal_status_info
from ..components.modal_status_heads import modal_status_heads


def _badge(icon: str, text: str):
    return rx.flex(
        rx.icon(icon, size=16),
        text,
        align_items="center",
        gap="4px",
        padding="x-2 y-1",
        color="black"
    )


def _badge_heads(icon: str, text: str):
    return rx.flex(
        rx.icon(icon, size=16),
        text,  # Aquí se utiliza el valor de text
        align_items="center",
        gap="4px",
        padding="x-2 y-1",
        color="black"
    )


def status_button_heads(n_orders: str, name: str):
    badge_mapping = {
        "0": ("ban", "0", "#E52B50"),
        "1": ("ban", "1", "#E52B50"),
        "2": ("ban", "2", "#E52B50"),
        "3": ("ban", "3", "#E85E65"),
        "4": ("loader", "4", "#E85E65"),
        "5": ("check", "5", "#00FF7F"),
    }

    icon, text, color = badge_mapping.get(
        n_orders, ("check", n_orders, "#00FF7F"))

    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                _badge_heads(icon, text),
                border_radius="20px",
                opacity=1,
                bg=color,
                color="white",
                _hover={"bg": "darken", "color": "white"},
                on_click=States.get_children_orders(name)
            )
        ),

        # Modal para ajuste Status
        modal_status_heads(),
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

    if status == "Delivered" or status == "On the way":
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
            modal_status_info(),
            # Fin de Modal
        )
