import reflex as rx
from rxconfig import config
from .backend.backend import States


class State(rx.State):
    """The app state."""

    ...


@rx.page(route="/", title="Home", on_load=States.check_auth)
def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.flex(
        rx.vstack(
            rx.button("Gestion Mary Kay", width='40vh',
                      height='7vh', radius='full',  on_click=rx.redirect("/purchs_page")),
            rx.button("Gestion Amazon", width='40vh',
                      height='7vh',
                      radius='full', disable='True', on_click=rx.toast("Próximamente...")),
            rx.button("Otros", width='40vh',
                      height='7vh', radius='full', disable='True', on_click=rx.toast("Próximamente...")),
            rx.button("Salir", width='40vh',
                      height='7vh', radius='full', disable='True', on_click=States.logout),
            rx.code("to-do-easy.com", size="6",
                    color_scheme="indigo", weight="bold"),
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
    )


app = rx.App()
