import reflex as rx
from .backend.backend import States


class State(rx.State):
    """The app state."""

    ...


@rx.page(route="/index_admin", title="Administrador", on_load=States.check_auth)
def index() -> rx.Component:
    return rx.vstack(
        rx.heading("Indices"),
        rx.link(
            "Administration Low Stocks with Fee Products",
            href="/applicable_fees_admin",
            size="3",  # Controls text size (1-9)
            weight="bold",  # Text weight (light, regular, medium, bold)
            underline="hover",  # Underline behavior (auto, hover, always)
            color_scheme="blue",  # Color theme
            high_contrast=True,
            target="_blank"  # Increases color contrast
        ),
        align='center'
    )


app = rx.App()
