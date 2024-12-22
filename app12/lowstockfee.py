import reflex as rx
from .backend.backend import States
from .components.main_table_lowstockfee import table_products
from .components.filter_orders import filter_component


@rx.page(route='/lowstockfee', title='LowStock', on_load=States.check_auth)
def index() -> rx.Component:
    return rx.cond(
        States.auth_token != "",
        rx.flex(
            rx.vstack(
                rx.hstack(
                    rx.icon(
                        "home",
                        size=30,
                        color="white",
                        bg="black",
                        cursor="pointer",
                        on_click=rx.redirect("/")
                    ),
                    rx.spacer(
                    ),

                    rx.heading(
                        'Applicable Fees', margin_left="1em", width="100%"),
                    margin_top="2em",
                    margin_right="2em",
                    margin_left="1em",

                ),

                table_products(States.stocklowfee)
            ),
            direction='column',
            align='center',
            on_mount=States.get_prod_lowstockfee,
        ),
    )


app = rx.App()
