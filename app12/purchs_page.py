import reflex as rx
from .backend.backend import States
from .components.main_table import table_purchs
from .components.filter_orders import filter_component


@rx.page(route='/purchs_page', title='purch_page', on_load=[States.on_load, States.get_all_purchs, States.load_locations])
def index() -> rx.Component:
    return rx.flex(
        rx.vstack(
            rx.hstack(
                rx.color_mode.button(),
                rx.heading('Ordenes Mary Kay', align='center'),
                width="80%",
                justify="center"
            ),
            filter_component(),
            table_purchs(States.purchorders),
            direction='column',
            on_mount=States.get_all_purchs,
        ),
        # justify="center",


    )


app = rx.App()
