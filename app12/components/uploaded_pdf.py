import reflex as rx
from


def upload_pdf() -> rx.Component:
    return rx.dialog.content(
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
                        border="1px solid rgb(107,99,246)",
                    ),
                    rx.text(
                        "Arrastra y suelta el PDF aquí o haz clic para seleccionar"
                    ),
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
