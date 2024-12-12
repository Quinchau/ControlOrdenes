import reflex as rx
from ..backend.backend import PurchOrders12
from ..components.color_status import status_button


def table_purchs(list_purchs: list[PurchOrders12]) -> rx.Component:
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                # rx.table.column_header_cell('order'),
                rx.table.column_header_cell('tracking'),
                # rx.table.column_header_cell('ordeno'),
                rx.table.column_header_cell('supplier'),
                # rx.table.column_header_cell('SupplierName'),
                rx.table.column_header_cell('Status'),
                # rx.table.column_header_cell('orddate'),
                # rx.table.column_header_cell('status'),
            )
        ), rx.table.body(
            rx.foreach(list_purchs, row_table)
        )
    )


def row_table(purchorders: PurchOrders12) -> rx.Component:
    return rx.table.row(
        # rx.table.cell(purchorders.orderref),
        rx.table.cell(purchorders.requisitionno[-4:]),
        rx.table.cell(purchorders.supplierno),
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
