import reflex as rx
from .backend.backend import States
from .components.main_table import table_purchs
from .components.filter_orders import filter_component


@rx.page(route='/purchs_page', title='purch_page', on_load=[States.on_load, States.get_all_purchs, States.load_locations])
def index() -> rx.Component:
    return rx.flex(
        rx.vstack(
            rx.hstack(rx.heading('Ordenes Mary Kay', align='center')),
            rx.hstack(
                filter_component(), rx.color_mode.button(),
                align="center",
                justify="between",
                width="100%",
            ),
            table_purchs(States.purchorders)
        ),
        direction='column',
        align='center',
        on_mount=States.get_all_purchs,
    )


app = rx.App()
