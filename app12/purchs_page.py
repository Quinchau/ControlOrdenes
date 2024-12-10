import reflex as rx
from .backend.backend import States
from .components.main_table import table_purchs


@rx.page(route='/purchs_page', title='purch_page', on_load=[States.on_load, States.get_all_purchs, States.load_locations])
def index() -> rx.Component:
    return rx.container(
        rx.vstack(
            rx.hstack(
                rx.color_mode.button(),
                rx.heading('Ordenes', align='center'),
                width="80%",
                justify="center"
            ),
            rx.flex(
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
            table_purchs(States.purchorders),
            direction='column',
            style={"width": '29vw', 'margin': 'auto'},
            on_mount=States.get_all_purchs,
        )
    )


app = rx.App()
