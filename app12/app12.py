"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from rxconfig import config


class State(rx.State):
    """The app state."""

    ...


def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.flex(
        rx.vstack(
            rx.button("Gestion Mary Kay", width='40vh',
                      height='8vh', radius='full',  on_click=rx.redirect("/purchs_page")),
            rx.button("Gestion Amazon", width='40vh',
                      height='8vh',
                      radius='full', disable='True', on_click=rx.toast("Próximamente...")),
            rx.button("Otros", width='40vh',
                      height='8vh', radius='full', disable='True', on_click=rx.toast("Próximamente...")),
            rx.code("to-do-easy.com", size="6", weight="bold"),
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
app.add_page(index)
