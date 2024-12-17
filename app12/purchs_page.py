import reflex as rx
from .backend.backend import States
from .components.main_table import table_purchs
from .components.filter_orders import filter_component


@rx.page(route='/purchs_page', title='purch_page', on_load=[States.check_auth, States.get_all_purchs])
def index() -> rx.Component:
    return rx.flex(
        rx.vstack(
            rx.hstack(
                rx.icon(
                    "home",
                    size=15,
                    color="white",
                    bg="black",
                    cursor="pointer",
                    margin_top="0.5em",
                    margin_right="2em",
                    on_click=rx.redirect("/")
                ),

                rx.heading(
                    'Ordenes Mary Kay', align='center')
            ),
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
