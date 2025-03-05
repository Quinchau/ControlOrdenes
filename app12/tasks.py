import reflex as rx
from .backend.backend import States
from .components.ui_base_page import base_page


@rx.page(route='/tasks', title='Tareas', on_load=States.check_auth)
def index() -> rx.Component:
    return base_page(
        rx.cond(
            States.auth_token != "",
            rx.flex(
                rx.vstack(
                    # Encabezado
                    rx.hstack(
                        rx.heading("Pending Tasks", size="4"),
                        width="100%",
                        justify="center",
                        margin="0",
                        padding="0",
                    ),
                    rx.desktop_only(
                        rx.container(
                            rx.foreach(
                                States.formatted_tasks,
                                lambda task, index: rx.vstack(
                                    rx.text(
                                        task["description"],
                                        color=rx.cond(
                                            task["status"] == "Pending",
                                            "blue",
                                            "green"
                                        ),
                                    ),
                                    rx.text(
                                        f"Created: {task['created_at']}",
                                        size="1",
                                    ),
                                    rx.hstack(
                                        rx.text(
                                            f"Modify: {task['updated_at']}",
                                            size="1",
                                        ),
                                        rx.cond(
                                            task["status"] == "Completed",
                                            rx.badge(
                                                "Terminado",
                                                color_scheme="green",
                                                variant="soft",
                                                size="3",
                                                cursor="default",
                                            ),
                                            rx.alert_dialog.root(
                                                rx.alert_dialog.trigger(
                                                    rx.badge(
                                                        "Pendiente",
                                                        color_scheme="red",
                                                        variant="soft",
                                                        size="3",
                                                        cursor="pointer"
                                                    ),
                                                ),
                                                rx.alert_dialog.content(
                                                    rx.alert_dialog.title(
                                                        "Confirmar Acción"),
                                                    rx.alert_dialog.description(
                                                        "¿Está seguro de marcar esta tarea como terminada?"
                                                    ),
                                                    rx.flex(
                                                        rx.alert_dialog.cancel(
                                                            rx.button("Cancelar", variant="soft",
                                                                      color_scheme="gray"),
                                                        ),
                                                        rx.alert_dialog.action(
                                                            rx.button(
                                                                "Confirmar",
                                                                color_scheme="red",
                                                                on_click=States.toggle_task_status(
                                                                    task["id"]),
                                                            ),
                                                        ),
                                                        spacing="3",
                                                        justify="end",
                                                    ),
                                                ),
                                            ),
                                        ),
                                        width="100%",
                                        justify="between",
                                        align="center",
                                        spacing="0",
                                    ),
                                    spacing="2",
                                    padding="10px 0",
                                    width="80%",
                                    margin="0",
                                    border_bottom="1px solid #eee",
                                    key=f"task-{index}-desktop",
                                ),
                            ),
                            size="3",
                            center_content=True,
                            width="100%"
                        ),
                        width="100%",
                        justify_content="center",
                        align_items="center"
                    ),

                    # Vista para tablet
                    rx.tablet_only(
                        rx.container(
                            rx.foreach(
                                States.formatted_tasks,
                                lambda task, index: rx.vstack(
                                    rx.text(
                                        task["description"],
                                        color=rx.cond(
                                            task["status"] == "Pending",
                                            "blue",
                                            "green"
                                        ),
                                    ),
                                    rx.hstack(
                                        rx.text(
                                            rx.cond(
                                                task["updated_at"] != "Sin actualizar",
                                                f"Actualizado: {task['updated_at']}",
                                                "Sin actualizar"
                                            ),
                                            size="1"
                                        ),
                                        rx.cond(
                                            task["status"] == "Completed",
                                            rx.badge(
                                                "Terminado",
                                                color_scheme="green",
                                                variant="soft",
                                                size="2",
                                                on_click=lambda: States.toggle_task_status(
                                                    task["id"]),
                                                cursor="pointer"
                                            ),
                                            rx.badge(
                                                "Pendiente",
                                                color_scheme="red",
                                                variant="soft",
                                                size="2",
                                                on_click=lambda: States.toggle_task_status(
                                                    task["id"]),
                                                cursor="pointer"
                                            ),
                                        ),
                                        width="100%",
                                        justify="between",
                                        spacing="1",
                                    ),
                                    spacing="1",
                                    padding="5px 0",
                                    width="100%",
                                    margin="0",
                                    border_bottom="1px solid #eee",
                                    key=f"task-{index}-tablet",
                                ),
                            ),
                            size="1",
                            center_content=False,
                        ),
                    ),

                    rx.mobile_only(
                        rx.vstack(
                            # Iterar sobre las tareas formateadas
                            rx.foreach(
                                States.formatted_tasks,
                                lambda task, index: rx.vstack(
                                    # Descripción de la tarea
                                    rx.text(
                                        task["description"],
                                        color=rx.cond(
                                            task["status"] == "Pending",
                                            "red",
                                            "green"
                                        ),
                                        width="100%",
                                    ),
                                    # Fecha de creación
                                    rx.text(
                                        f"Created: {task['created_at']}",
                                        size="1",
                                        width="100%",
                                    ),
                                    # Fecha de actualización con badge en la misma línea
                                    rx.hstack(
                                        rx.text(
                                            f"Modify: {task['updated_at']}",
                                            size="1",
                                        ),
                                        rx.spacer(),  # Empuja el badge al borde derecho
                                        rx.cond(
                                            task["status"] == "Completed",
                                            rx.badge(
                                                "Terminado",
                                                color_scheme="green",
                                                variant="soft",
                                                size="3",
                                                cursor="default",  # No clicable
                                            ),
                                            rx.alert_dialog.root(
                                                rx.alert_dialog.trigger(
                                                    rx.badge(
                                                        "Pendiente",
                                                        color_scheme="red",
                                                        variant="soft",
                                                        size="3",
                                                        cursor="pointer"
                                                    ),
                                                ),
                                                rx.alert_dialog.content(
                                                    rx.alert_dialog.title(
                                                        "Confirmar Acción"),
                                                    rx.alert_dialog.description(
                                                        "¿Está seguro de marcar esta tarea como terminada?",
                                                    ),
                                                    rx.flex(
                                                        rx.alert_dialog.cancel(
                                                            rx.button("Cancelar", variant="soft",
                                                                      color_scheme="gray"),
                                                        ),
                                                        rx.alert_dialog.action(
                                                            rx.button(
                                                                "Confirmar",
                                                                color_scheme="red",
                                                                on_click=States.toggle_task_status(
                                                                    task["id"]),
                                                            ),
                                                        ),
                                                        spacing="3",
                                                        justify="end",
                                                    ),
                                                ),
                                            ),
                                        ),
                                        width="100%",  # El hstack ocupa todo el ancho
                                        justify="between",  # Justificar los elementos a los extremos
                                        align="center",  # Alinear verticalmente el texto y el badge
                                    ),
                                    # Diálogo de confirmación (agregar fuera del rx.foreach, dentro del rx.vstack principal)

                                    spacing="0",
                                    padding="5px 0",
                                    width="100%",
                                    margin="0",
                                    border_bottom="1px solid #eee",
                                    key=f"task-{index}-mobile",
                                ),
                            ),
                            # Botón flotante para abrir el modal
                            rx.button(
                                rx.icon(
                                    "plus",
                                    color="white",
                                    size=26
                                ),
                                position="fixed",
                                bottom="20px",
                                left="50%",
                                transform="translateX(-50%)",
                                on_click=lambda: States.toggle_dialog(
                                    True),  # Abre el modal
                                style={
                                    "background_color": "#0047AB",
                                    "opacity": "1",
                                    "border_radius": "50%",
                                    "width": "50px",
                                    "height": "50px",
                                    "box_shadow": "0 10px 15px -3px rgba(0, 0, 0, 0.1)",
                                    "_hover": {"background_color": "#003380"}
                                },
                            ),
                            # Fondo oscuro para el modal
                            rx.cond(
                                States.dialog_open,
                                rx.box(
                                    style={
                                        "position": "fixed",
                                        "top": "0",
                                        "left": "0",
                                        "width": "100%",
                                        "height": "100%",
                                        "backgroundColor": "rgba(0, 0, 0, 0.5)",
                                        "zIndex": "998",
                                    },
                                    on_click=lambda: States.toggle_dialog(
                                        False),  # Cierra el modal
                                ),
                            ),
                            # Modal personalizado
                            rx.cond(
                                States.dialog_open,
                                rx.box(
                                    rx.vstack(
                                        rx.text_area(
                                            placeholder="Nueva tarea...",
                                            value=States.new_task_description,
                                            on_change=States.set_new_task_description,
                                            rows='4',
                                            resize="none",
                                            width="100%",
                                            height="auto",
                                            font_size="16px",
                                            padding="10px",
                                            margin="10px 0 0 0",
                                        ),
                                        rx.hstack(
                                            rx.button(
                                                "Agregar Tarea",
                                                on_click=[
                                                    States.create_task,
                                                    lambda: States.toggle_dialog(
                                                        False),
                                                ],
                                                disabled=States.new_task_description == "",
                                                style={
                                                    "marginTop": "10px",
                                                    "padding": "10px 20px",
                                                    "backgroundColor": "#0047AB",
                                                    "color": "white",
                                                    "borderRadius": "5px",
                                                    "cursor": "pointer",
                                                    "_hover": {"backgroundColor": "#003380"}
                                                }
                                            ),
                                            rx.button(
                                                "Abandonar",
                                                on_click=[
                                                    lambda: States.toggle_dialog(
                                                        False),
                                                    lambda: States.set_new_task_description(
                                                        "")
                                                ],
                                                style={
                                                    "marginTop": "10px",
                                                    "padding": "10px 20px",
                                                    "backgroundColor": "#808080",
                                                    "color": "white",
                                                    "borderRadius": "5px",
                                                    "cursor": "pointer",
                                                    "_hover": {"backgroundColor": "#5a5a5a"}
                                                }
                                            ),
                                            spacing="4",
                                            justify="center",
                                            width="100%",
                                        ),
                                        spacing="4",
                                    ),
                                    style={
                                        "position": "fixed",
                                        "left": "50%",
                                        "transform": "translateX(-50%)",
                                        "width": "90%",
                                        "maxWidth": "500px",
                                        "height": "auto",
                                        "backgroundColor": "white",
                                        "padding": "10px",
                                        "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.1)",
                                        "borderRadius": "8px",
                                        "zIndex": "999",
                                        "animation": rx.cond(
                                            States.dialog_open,
                                            "slideUp 0.3s ease-out forwards",
                                            "slideDown 0.3s ease-out forwards"
                                        ),
                                        "@keyframes slideUp": {
                                            "from": {"top": "100%"},
                                            "to": {"top": "20%"}
                                        },
                                        "@keyframes slideDown": {
                                            "from": {"top": "20%"},
                                            "to": {"top": "100%"}
                                        },
                                    },
                                ),
                            ),
                            width="100%",
                            position="relative",
                            padding="0",
                            margin="0",
                        ),
                        width="100%",
                        padding="0",  # Sin padding del contenedor
                        margin="0",   # Sin margen del contenedor
                    ),

                    width="100%",
                    max_width="100%",
                    margin="0",
                    padding="0 5px",
                ),
                direction="column",
                align="stretch",
                width="100%",
                max_width="100%",
                margin="0",
                padding="0 5px",
                on_mount=States.load_tasks,
                id="tasks-container",
            ),
        )
    )


app = rx.App()
