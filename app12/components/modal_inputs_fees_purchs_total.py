import reflex as rx
from app12.backend.heads_backend import StatesHeads
from app12.backend.backend import States


def modal_update_fees_comission(id, name, nro_orders, total, comissions) -> rx.Component:
    return rx.dialog.content(
        rx.dialog.title("Current Month Orders"),
        rx.dialog.description(
            rx.flex(
                # Información de Usuario
                rx.vstack(
                    rx.hstack(
                        rx.text("UserId: ", width="150px"),
                        rx.text(id)
                    ),
                    rx.hstack(
                        rx.text("Name: ", width="150px"),
                        rx.text(name)
                    ),
                    width="100%",
                    spacing="3"
                ),

                # Inputs alineados
                rx.vstack(
                    rx.hstack(
                        rx.text("Childrens with Orders: ", width="150px"),
                        rx.input(
                            value=StatesHeads.nro_orders,
                            on_change=StatesHeads.set_nro_orders,
                            width="200px"
                        ),
                        width="100%"
                    ),
                    rx.hstack(
                        rx.text("Total Amount: ", width="150px"),
                        rx.input(
                            value=StatesHeads.total_orders,
                            on_change=StatesHeads.set_total_orders,
                            width="200px"
                        ),
                        width="100%"
                    ),
                    rx.hstack(
                        rx.text("Comissions: ", width="150px"),
                        rx.input(
                            value=StatesHeads.comissions,
                            on_change=StatesHeads.set_comissions,
                            width="200px"
                        ),
                        width="100%"
                    ),
                    spacing="3",
                    width="100%"
                ),
                rx.hstack(
                    rx.dialog.root(
                        rx.dialog.trigger(
                            rx.text(
                                "Actualizar Pdf Comisiones",
                                cursor="pointer",
                                _hover={"color": "blue"},
                                align="center",
                                on_click=[
                                    StatesHeads.set_user_id(id),
                                    StatesHeads.pdf_upload(True)
                                ]
                            )
                        ),
                        rx.dialog.content(
                            rx.dialog.title("Subir PDF"),
                            rx.dialog.description(
                                "Selecciona el archivo PDF para subir"),
                            rx.vstack(
                                rx.upload(
                                    rx.vstack(
                                        rx.button(
                                            "Seleccionar PDF",
                                            color="rgb(107,99,246)",
                                            bg="white",
                                            border="1px solid rgb(107,99,246)"),
                                        rx.text(
                                            "Arrastra y suelta el PDF aquí o haz clic para seleccionar"
                                        ),
                                        align="center"
                                    ),
                                    id="pdf_upload",
                                    max_files=1,
                                    accept={
                                        "application/pdf": [".pdf"]
                                    },
                                    on_drop=StatesHeads.handle_pdf_upload(
                                        rx.upload_files(upload_id="pdf_upload")
                                    ),
                                    border="1px dotted rgb(107,99,246)",
                                    padding="5em",
                                ),
                                rx.text(rx.selected_files("pdf_upload")),
                                rx.flex(
                                    rx.dialog.close(
                                        rx.button(
                                            "Cancelar",
                                            variant="soft",
                                            color_scheme="gray",
                                        ),
                                    ),
                                    rx.dialog.close(
                                        rx.button("Cerrar"),
                                    ),
                                    spacing="3",
                                    margin_top="16px",
                                    justify="end",
                                ),
                            )
                        )
                    ),
                    rx.switch(
                        checked=States.show_current_month,
                        on_change=States.toggle_time_period,
                    ),
                    rx.badge(
                        rx.cond(
                            States.show_current_month,
                            "Mes Actual",
                            "Últimos 30 días"

                        )
                    ),

                    width="100%",
                    justify="end",
                    spacing="3",
                    align_items="center",
                ),

                # Lista de Children
                rx.dialog.description(
                    rx.vstack(
                        rx.foreach(
                            States.children_orders_details,
                            lambda x: rx.hstack(
                                rx.text(
                                    f"{x.childrenname}:",
                                    font_weight="bold",
                                    color="var(--accent-11)"
                                ),
                                rx.text(
                                    x.ordersmonthdetails
                                ),
                                spacing="2",
                                align="start"
                            )
                        ),
                        spacing="3",
                        align="start"
                    )
                ),

                direction="column",
                spacing="3",
                align="start",
                width="100%"
            )
        ),
        rx.flex(
            rx.dialog.close(
                rx.button(
                    "Cancelar",
                    variant="soft",
                    color_scheme="gray",
                    margin_top="2em"
                ),
            ),
            rx.dialog.close(
                rx.button(
                    "Guardar",
                    on_click=StatesHeads.update_comissions_amount_orders(id),
                    margin_top="2em"
                ),
            ),
            spacing="3",
            justify="center",
        ),
        max_width="600px",
        size="3"
    )
