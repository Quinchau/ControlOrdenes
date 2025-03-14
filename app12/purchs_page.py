import reflex as rx
from .backend.backend import States
from .components.main_table import table_purchs
from .components.filter_orders import filter_component
from .components.ui_base_page import base_page


@rx.page(route='/purchs_page', title='purch_page', on_load=States.check_auth)
def index() -> rx.Component:
    return base_page(

        rx.cond(
            States.auth_token != "",
            rx.flex(
                rx.vstack(
                    rx.hstack(
                        rx.heading(
                            'Ordenes Mary Kay', align='center')
                    ),
                    rx.hstack(
                        filter_component(
                            States.set_selected_location),
                        align="center",
                        justify="between",
                        width="100%",
                    ),
                    table_purchs(States.purchorders)
                ),
                direction='column',
                align='center',
                on_mount=States.get_all_purchs(),
            ),
        )
    )


app = rx.App()
