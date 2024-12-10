import reflex as rx
from ..backend.backend import States


def filter_component() -> rx.Component:
    return rx.flex(
        rx.select.root(
            rx.select.trigger(placeholder="Filtrar Ordenes"),
            rx.select.content(
                rx.select.group(
                    rx.select.item("TODAS", value="ALL"),
                    rx.select.item("Carolina", value="VEN"),
                    rx.select.item("Pierina", value="PIE"),
                    rx.select.item("Franyeli", value="FRA"),
                    rx.select.item("Franchesca", value="STR"),
                ),
            ),
            on_change=States.set_selected_location,
        ),
        justify="end",
        width="90%",
    ),
