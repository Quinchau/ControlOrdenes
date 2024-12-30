import reflex as rx
from rxconfig import config
from .navbar import navbar


def base_page(child: rx.Component, *args, **kwargs) -> rx.Component:
    return rx.container(
        navbar(),
        child,
        rx.logo(),
        rx.color_mode.button(position="bottom-left"),
    )
