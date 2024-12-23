import reflex as rx
from .backend.backend import States
from .components.main_table import table_purchs
from .components.filter_orders import filter_component


@rx.page(route='/purchs_page', title='purch_page', on_load=States.check_auth)
def index() -> rx.Component:
    return rx.cond(
        States.auth_token != "",
        rx.flex(
            rx.vstack(
                rx.hstack(
                    rx.icon(
                        "home",
                        size=20,
                        color="white",
                        bg="black",
                        cursor="pointer",
                        margin_top="0.5em",
                        margin_right="2em",
                        margin_left="1em",
                        on_click=rx.redirect("/")
                    ),

                    rx.heading(
                        'Ordenes Mary Kay', align='center')
                ),
                rx.hstack(
                    filter_component(
                        States.set_selected_location), rx.color_mode.button(),
                    align="center",
                    justify="between",
                    width="100%",
                ),
                table_purchs(States.purchorders)
            ),
            direction='column',
            align='center',
            on_mount=States.get_all_purchs,
        ),
    )


app = rx.App()
