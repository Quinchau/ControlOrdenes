import reflex as rx
from rxconfig import config
from .backend.backend import States
from .components.ui_base_page import base_page


class State(rx.State):
    """The app state."""

    ...


@rx.page(route="/marykay_index", title="Index_MaryKay", on_load=States.check_auth)
def index() -> rx.Component:
    return base_page(
        rx.cond(
            States.auth_token != "",  # Check if token exists in LocalStorage
            # Authenticated view
            rx.flex(
                rx.vstack(
                    rx.button("Purch Orders",
                              width='40vh',
                              height='7vh',
                              radius='full',
                              on_click=rx.redirect("/purchs_page")),
                    rx.button("Heads Controls",
                              width='40vh',
                              height='7vh',
                              radius='full',
                              disable='True',
                              on_click=rx.redirect("/control_heads")),
                    rx.button("Monthly Commissions",
                              width='40vh',
                              height='7vh',
                              radius='full',
                              disable='True',
                              on_click=rx.redirect("/heads_admin")),
                    rx.button("Salir",
                              width='40vh',
                              height='7vh',
                              radius='full',
                              on_click=States.logout),
                    rx.code("to-do-easy.com",
                            size="6",
                            color_scheme="indigo",
                            weight="bold"),
                    border_width="2px",
                    border_radius="1em",
                    align='center',
                    width='100vh',
                    height="100vh",
                    justify='center',
                    max_width='400px',
                    spacing="9",
                    background_image="url('/drops-6392473_640.jpg')",
                ),
                justify='center'
            ),

        )
    )


app = rx.App()
