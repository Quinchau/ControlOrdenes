import reflex as rx
from rxconfig import config
from .navbar import navbar


def base_page(child: rx.Component, *args, **kwargs) -> rx.Component:
    return rx.fragment(
        navbar(),
        child,
    )
