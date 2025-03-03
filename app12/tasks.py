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
                    rx.hstack(
                        rx.heading("Pending Tasks", size="4"),
                        width="100%",
                        justify="center",
                        margin="0",
                        padding="0",
                    ),
                    # Vista para escritorio
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
                                    rx.hstack(
                                        rx.text(
                                            f"Creado por: {task['user_id']}", size="2"),
                                        rx.cond(
                                            task["status"] == "Completed",
                                            rx.badge("Terminado", color_scheme="green", variant="soft", size="3",
                                                     on_click=States.toggle_task_status(task["id"]), cursor="pointer"),
                                            rx.badge("Pendiente", color_scheme="red", variant="soft", size="3",
                                                     on_click=States.toggle_task_status(task["id"]), cursor="pointer"),
                                        ),
                                        width="100%",
                                        justify="between",
                                        spacing="2",
                                    ),
                                    rx.text(
                                        rx.cond(
                                            task["updated_at"] != "Sin actualizar",
                                            f"Actualizado: {task['updated_at']}",
                                            "Sin actualizar"
                                        ),
                                        size="2"
                                    ),
                                    spacing="2",  # Más espacio para escritorio
                                    padding="10px 0",
                                    width="100%",
                                    margin="0",
                                    border_bottom="1px solid #eee",
                                    key=f"task-{index}-desktop",
                                ),
                            ),
                        ),
                        size="2",
                        center_content=True
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
                                            rx.badge("Terminado", color_scheme="green", variant="soft", size="2",
                                                     on_click=States.toggle_task_status(task["id"]), cursor="pointer"),
                                            rx.badge("Pendiente", color_scheme="red", variant="soft", size="2",
                                                     on_click=States.toggle_task_status(task["id"]), cursor="pointer"),
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
                            size="1",  # Controla el ancho máximo del contenedor
                            center_content=False  # Centra el contenido
                        ),
                    ),
                    # Vista para móvil (configuración actual)
                    rx.mobile_only(
                        rx.vstack(
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
                                        f"Creado por: {task['user_id']}", size="1"),
                                    rx.hstack(
                                        rx.cond(
                                            task["updated_at"] != "Sin actualizar",
                                            rx.text(
                                                f"Actualizado: {task['updated_at']}", size="1"),
                                            rx.text(
                                                "Sin actualizar", size="1"),
                                        ),
                                        rx.cond(
                                            task["status"] == "Completed",
                                            rx.badge("Terminado", color_scheme="green", variant="soft", size="3",
                                                     on_click=States.toggle_task_status(task["id"]), cursor="pointer"),
                                            rx.badge("Pendiente", color_scheme="red", variant="soft", size="3",
                                                     on_click=States.toggle_task_status(task["id"]), cursor="pointer"),
                                        ),
                                        width="100%",
                                        justify="between",
                                        spacing="2",
                                    ),
                                    spacing="0",
                                    padding="5px 0",
                                    width="100%",
                                    margin="0",
                                    border_bottom="1px solid #eee",
                                    key=f"task-{index}-mobile",
                                ),
                            ),
                            rx.button(
                                rx.icon(
                                    "plus",
                                    color="white",  # Color blanco para el icono
                                    size=26        # Número entero, sin "px"
                                ),
                                position="fixed",
                                bottom="20px",
                                left="50%",
                                transform="translateX(-50%)",
                                on_click=States.create_task,
                                disabled=States.new_task_description == "",
                                style={
                                    "background_color": "#0047AB",  # Azul cobalto intenso
                                    "opacity": "1",
                                    "border_radius": "50%",
                                    "width": "50px",
                                    "height": "50px",
                                    "box_shadow": "0 10px 15px -3px rgba(0, 0, 0, 0.1)",
                                    "_hover": {
                                        "background_color": "#003380"
                                    }
                                }
                            ),
                            width="100%",
                            position="relative",
                        ),
                    ),
                    rx.input(
                        placeholder="Nueva tarea...",
                        value=States.new_task_description,
                        on_change=States.set_new_task_description,
                        width="100%",
                        margin="20px 0 0 0",
                        padding="0 5px",
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
            rx.text("Por favor, inicia sesión para ver las tareas."),
        )
    )


app = rx.App()
