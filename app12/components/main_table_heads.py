import reflex as rx
from ..backend.backend import SuppliersDisplayItem
from ..components.color_status import status_button_heads
from ..backend.backend import States


def table_heads(list_heads: list[SuppliersDisplayItem]) -> rx.Component:
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                # rx.table.column_header_cell('Ref'),
                rx.table.column_header_cell('Name'),
                rx.table.column_header_cell('Total'),
                rx.table.column_header_cell('Fee'),
                rx.table.column_header_cell('Ord'),
            )
        ), rx.table.body(
            rx.foreach(list_heads, row_table)
        )
    )


def row_table(item: SuppliersDisplayItem) -> rx.Component:
    return rx.table.row(
        # rx.table.cell(item.supplierid),
        rx.table.cell(item["name"]),
        rx.table.cell(item["totalcompras"]),
        rx.table.cell(item["comisiones"]),
        rx.table.cell(
            rx.match(
                item["nro_orders"],
                ("0", status_button_heads(
                    "0", item["nro_orders"], item["name"])),
                ("1", status_button_heads(
                    "1", item["nro_orders"], item["name"])),
                ("2", status_button_heads(
                    "2", item["nro_orders"], item["name"])),
                ("3", status_button_heads(
                    "3", item["nro_orders"], item["name"])),
                ("4", status_button_heads(
                    "4", item["nro_orders"], item["name"])),
                ("5", status_button_heads(
                    "5", item["nro_orders"], item["name"])),
                status_button_heads(
                    item["nro_orders"], item["id"], item["name"])
            )
        ),
        # rx.table.cell(purchorders.orddate[:10]),
    )
