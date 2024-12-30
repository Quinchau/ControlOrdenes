import reflex as rx
from ..backend.backend import States


def filter_component(act_state) -> rx.Component:
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
            value=States.selected_location,
            on_change=lambda value: act_state(value),
        ),
        justify="end",
        width="90%",
    )
