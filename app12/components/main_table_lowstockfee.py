import reflex as rx
from ..backend.backend import StockMaster


def table_products(list_prod: list[StockMaster]) -> rx.Component:
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                rx.table.column_header_cell('Ref'),
                rx.table.column_header_cell('ASIN'),
                rx.table.column_header_cell('Item'),
            )
        ), rx.table.body(
            rx.foreach(list_prod, row_table)
        )
    )


def row_table(item: dict) -> rx.Component:
    # Concatenación con f-strings (recomendado)
    stockid_url = f"https://www.amazon.com/dp/{item['stockid']}"

    return rx.table.row(
        rx.table.cell(
            rx.image(
                src=(item["image_url"]),
                width="35px",
                height="35px"
            )),
        rx.table.cell(rx.link(  # Usamos rx.link para que sea un enlace
            item["stockid"],
            href=stockid_url,  # Establecemos la URL generada
            is_external=True  # Para que se abra en una nueva pestaña
        ),
            style={
                "align-items": "center",
                "height": "100%"
        }),
        rx.table.cell(item["description"]),
    )
