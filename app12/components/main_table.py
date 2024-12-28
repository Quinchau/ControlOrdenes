import reflex as rx
from ..components.color_status import status_button
from ..backend.backend import PurchOrdersDisplay


def table_purchs(list_purchs: list[PurchOrdersDisplay]) -> rx.Component:
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                rx.table.column_header_cell('Ref'),
                rx.table.column_header_cell('Ordena'),
                rx.table.column_header_cell('track'),
                rx.table.column_header_cell('Status'),
            )
        ), rx.table.body(
            rx.foreach(list_purchs, row_table)
        )
    )


def row_table(item: list[PurchOrdersDisplay]) -> rx.Component:
    return rx.table.row(
        rx.table.cell(item.refaddress),
        rx.table.cell(item.suppliername[:10]),
        rx.table.cell(item.requisition[-4:]),
        rx.table.cell(
            rx.match(
                item.comments.lower(),
                ("delivered", status_button("Delivered", item.order)),
                ("on the way", status_button("On the way", item.order)),
                ("on hold", status_button("On Hold", item.order)),
                ("received", status_button("Received", item.order)),
                status_button("Pending", item.order),
            )
        ),
        # rx.table.cell(purchorders.orddate[:10]),
    )
