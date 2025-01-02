import reflex as rx
from .backend.backend import States
from .components.main_table_lowstockfee import table_products
from .components.filter_orders import filter_component
from .components.ui_base_page import base_page


@rx.page(route='/lowstockfee', title='LowStock', on_load=States.check_auth)
def index() -> rx.Component:
    return base_page(
        rx.cond(
            States.auth_token != "",
            rx.flex(
                rx.vstack(
                    rx.hstack(
                        rx.heading(
                            'Applicable Fees'
                        ),
                        margin_top="1em",
                        width="100%",
                        justify="center"
                    ),
                    table_products(States.stocklowfee)
                ),
                direction='column',
                align='center',
                on_mount=States.get_prod_lowstockfee,
            ),
        )
    )


app = rx.App()
