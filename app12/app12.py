import reflex as rx
from rxconfig import config
from fastapi import FastAPI
from .backend.backend import States
from .components.ui_base_page import base_page
from .api.views.download_pdf_commission import get_supplier_doc

# Configurar la app con PWA
app = rx.App(
    head_components=[
        rx.el.link(rel="manifest", href="/manifest.json"),
        rx.script("""
            console.log('Script de Reflex ejecutándose');
            if ('serviceWorker' in navigator) {
                console.log('Service Worker soportado en este navegador');
                navigator.serviceWorker.register('/sw.js', { scope: '/' })
                    .then(reg => {
                        console.log('Service Worker registrado con éxito. Scope:', reg.scope);
                        if (reg.installing) {
                            console.log('Service Worker en instalación');
                        } else if (reg.waiting) {
                            console.log('Service Worker instalado, en espera');
                        } else if (reg.active) {
                            console.log('Service Worker activo');
                        }
                    })
                    .catch(err => {
                        console.error('Error al registrar Service Worker:', err.message);
                        console.error('Detalles del error:', err);
                    });
            } else {
                console.log('Service Worker no soportado en este navegador');
            }
        """)
    ]
)

# Clase de estado (simplificada)


class State(rx.State):
    """The app state."""
    auth_token: str = ""


@rx.page(route="/", title="Home", on_load=States.check_auth)
def index() -> rx.Component:
    return base_page(
        rx.cond(
            States.auth_token != "",
            rx.flex(
                rx.vstack(
                    rx.button("Gestion Mary Kay",
                              width='40vh',
                              height='7vh',
                              radius='full',
                              on_click=rx.redirect("/marykay_index")),
                    rx.button("Gestion Amazon",
                              width='40vh',
                              height='7vh',
                              radius='full',
                              disable='True',
                              on_click=rx.redirect("/amazon_index")),
                    rx.button("Tasks",
                              width='40vh',
                              height='7vh',
                              radius='full',
                              disable='True',
                              on_click=rx.redirect("/tasks")),
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
        ),

    )


app.api.add_api_route(
    "/api/supplier-doc/{supplier_id:path}", get_supplier_doc, methods=["GET"])
