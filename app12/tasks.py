import reflex as rx
from .backend.backend import States
from .components.ui_base_page import base_page


@rx.page(route='/tareas', title='Tareas', on_load=States.check_auth)
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
                            ),  # Eliminado on_click y cursor
                            rx.text(
                                f"Creado por: {task['user_id']}", size="1"),
                            rx.hstack(
                                rx.cond(
                                    task["updated_at"] != "Sin actualizar",
                                    rx.text(
                                        f"Actualizado: {task['updated_at']}", size="1"),
                                    rx.text("Sin actualizar", size="1"),
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
                            key=f"task-{index}",
                        ),
                    ),
                    rx.input(
                        placeholder="Nueva tarea...",
                        value=States.new_task_description,
                        on_change=States.set_new_task_description,
                        width="100%",
                        margin="20px 0 0 0",  # Ajustado para eliminar márgenes laterales
                        padding="0 5px",
                    ),
                    rx.button(
                        rx.icon("a_arrow_up"),
                        position="fixed",
                        bottom="20px",
                        right="5px",  # Reducido de "20px" para acercarlo al borde derecho
                        on_click=States.create_task,
                        disabled=States.new_task_description == "",
                        color_scheme="blue",
                    ),
                    width="100%",
                    max_width="100%",  # Evita restricciones de ancho máximo
                    margin="0",
                    padding="0 5px",   # Mínimo padding lateral para no tocar el borde
                ),
                direction="column",
                align="stretch",
                width="100%",
                max_width="100%",  # Evita restricciones de ancho máximo
                margin="0",
                padding="0 5px",   # Mínimo padding lateral para no tocar el borde
                on_mount=States.load_tasks,
                id="tasks-container",
            ),
            rx.text("Por favor, inicia sesión para ver las tareas."),
        )
    )


app = rx.App()

# en: /home/charlie_ubu/proyectos/app12/app12/tasks.py
