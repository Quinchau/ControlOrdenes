import reflex as rx
from rxconfig import config
from .backend.backend import States
from .components.main_table_lowstockfee_admin import table_products
from .components.table_lowstockfee import table_lowstockfee


class State(rx.State):
    """The app state."""

    ...


@rx.page(route="/applicable_fees_admin", title="Subject Fees", on_load=States.check_auth)
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
                    rx.heading(
                        'Applicable Fees', margin_left="2em", width="100%"), rx.color_mode.button(),
                    margin_top="2em",
                    margin_right="2em",
                    margin_left="1em",
                ),
                rx.hstack(
                    table_lowstockfee(States),
                    align="center",
                    justify="between",
                    width="100%",
                ),

                table_products(States.stocklowfee),
            ),
            direction='column',
            align='center',
            on_mount=States.get_prod_lowstockfee,
        ),
    )


app = rx.App()
