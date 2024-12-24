import reflex as rx
from ..backend.backend import StockMaster
from ..backend.backend import States


def table_products(list_prod: list[StockMaster]) -> rx.Component:
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                rx.table.column_header_cell('Location'),
                rx.table.column_header_cell('Ref'),
                rx.table.column_header_cell('ASIN'),
                rx.table.column_header_cell('Item'),
                rx.table.column_header_cell('Fee'),
            )
        ), rx.table.body(
            rx.foreach(list_prod, row_table)
        )
    )


def row_table(item: dict) -> rx.Component:
    # Concatenación con f-strings (recomendado)
    return rx.table.row(
        rx.table.cell(item["locationname"]),
        rx.table.cell(
            rx.image(
                src=(item["image_url"]),
                width="40px",
                height="40px"
            )),
        rx.table.cell(item["stockid"]),
        rx.table.cell(item["description"]),
        rx.table.cell(rx.button(
            "Excluir",
            on_click=lambda stockid=item["stockid"]: States.exclude_product(
                stockid),  # Pasar stockid
            color_scheme="red",  # Estilo al boton
            size="1"  # Tamaño del boton
        ),
            style={
                "display": "flex",
                "align-items": "center",
                "justify-content": "center",
                "height": "100%"
        }),
    )
