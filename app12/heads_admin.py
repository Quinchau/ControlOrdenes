import reflex as rx
from .backend.backend import States
from .components.main_table_heads_admin import table_heads
from .components.filter_orders import filter_component
from .components.ui_base_page import base_page
from .backend.heads_backend import StatesHeads
from .backend.backend import alert_dialog


@rx.page(route='/heads_admin', title='Heads Administrator', on_load=States.check_auth)
def index() -> rx.Component:
    return base_page(
        rx.cond(
            States.auth_token != "",
            rx.flex(
                rx.vstack(
                    rx.hstack(
                        rx.heading(
                            'Heads Results',),
                        id="my-heading-in-control_heads",
                        width="100%",
                        justify="center"
                    ),
                    rx.hstack(
                        filter_component(
                            States.set_selected_location_heads),
                        align="center",
                        justify="between",
                        width="100%",
                    ),
                    table_heads(States.heads_suppliers),
                    alert_dialog(StatesHeads)


                ),
                direction='column',
                align='center',
                on_mount=States.get_all_heads,
                id="my-flex-container"
            ),
        )
    )


app = rx.App()
