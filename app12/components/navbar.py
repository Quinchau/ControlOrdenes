import reflex as rx
from rxconfig import config
from ..backend.backend import States


def navbar_link(text: str, url: str) -> rx.Component:
    return rx.link(
        rx.text(text, size="4", weight="medium"), href=url
    )


def navbar() -> rx.Component:
    return rx.box(
        rx.desktop_only(
            rx.hstack(
                rx.hstack(
                    rx.image(
                        src="/logo.jpg",
                        width="2.25em",
                        height="auto",
                        border_radius="25%",
                    ),
                    rx.heading(
                        "to-do-easy", size="7", weight="bold"
                    ),
                    align_items="center",
                ),
                rx.color_mode.button(),
                rx.hstack(
                    navbar_link("Home", "/"),
                    navbar_link("Mary Kay", "/heads_admin"),
                    navbar_link("Orders", "/control_heads"),
                    navbar_link("Pricing", "/#"),
                    navbar_link("Contact", "/#"),
                    spacing="5",
                ),
                rx.hstack(
                    rx.button(
                        "Sign Up",
                        size="3",
                        variant="outline",
                    ),
                    rx.button("Log In", size="3"),
                    spacing="4",
                    justify="end",
                ),
                justify="between",
                align_items="center",
                id="my-navbar-desktop"
            ),
        ),
        rx.mobile_and_tablet(
            rx.hstack(
                rx.hstack(
                    rx.image(
                        src="/logo.jpg",
                        width="2em",
                        height="auto",
                        border_radius="25%",
                    ),
                    rx.heading(
                        "to-do-easy", size="6", weight="bold"
                    ),
                    align_items="center",
                ),
                rx.color_mode.button(),
                rx.menu.root(
                    rx.menu.trigger(
                        rx.icon("menu", size=30)
                    ),
                    rx.menu.content(
                        rx.menu.item(rx.link("Home", href="/")),
                        rx.menu.item(
                            rx.link("Purchs Orders", href="purchs_page")),
                        rx.menu.item(
                            rx.link("Heads Controls", href="control_heads")),
                        rx.menu.item(
                            rx.link("Stock Low Fee", href="lowstockfee")),
                        rx.menu.separator(),
                        rx.menu.item(rx.link("Login", href="login")),
                        rx.menu.item(
                            "Sign Up", on_click=States.logout, cursor="pointer"),
                    ),
                    justify="end",
                ),
                justify="between",
                align_items="center",
            ),
        ),
        bg=rx.color("accent", 3),
        padding="1em",
        # position="fixed",
        # top="0px",
        # z_index="5",
        width="100%",
        id="my-container-navbar"
    )
