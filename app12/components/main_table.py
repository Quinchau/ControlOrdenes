import reflex as rx
from ..backend.backend import PurchOrders
from ..components.color_status import status_button


def table_purchs(list_purchs: list[PurchOrders]) -> rx.Component:
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                rx.table.column_header_cell('Ref'),
                rx.table.column_header_cell('Ordena'),
                rx.table.column_header_cell('track'),
                # rx.table.column_header_cell('ordeno'),
                # rx.table.column_header_cell('SupplierName'),
                rx.table.column_header_cell('Status'),
                # rx.table.column_header_cell('orddate'),
                # rx.table.column_header_cell('status'),
            )
        ), rx.table.body(
            rx.foreach(list_purchs, row_table)
        )
    )


def row_table(purchorders: PurchOrders) -> rx.Component:
    return rx.table.row(
        rx.table.cell(purchorders.suppliername.refaddress),
        rx.table.cell(purchorders.suppliername.suppname[:10]),
        rx.table.cell(purchorders.requisitionno[-4:]),
        rx.table.cell(
            rx.match(
                purchorders.comments.lower(),
                ("delivered", status_button("Delivered", purchorders.orderno)),
                ("on the way", status_button("On the way", purchorders.orderno)),
                ("on hold", status_button("On Hold", purchorders.orderno)),
                ("received", status_button("Received", purchorders.orderno)),
                status_button("Pending", purchorders.orderno),
            )
        ),
        # rx.table.cell(purchorders.orddate[:10]),
    )
