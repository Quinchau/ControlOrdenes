import reflex as rx
from ..backend.backend import SuppliersDisplayItem
from ..backend.heads_backend import StatesHeads
from ..components.modal_inputs_fees_purchs_total import modal_update_fees_comission
from datetime import datetime
from ..backend.backend import States
from dotenv import load_dotenv
import os

load_dotenv()


def table_heads(list_heads: list[SuppliersDisplayItem]) -> rx.Component:
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                rx.table.column_header_cell('Name'),
                rx.table.column_header_cell(
                    'Total', display=["none", "none", "table-cell", "table-cell"]),

                rx.table.column_header_cell('Current Commisions'),

                rx.table.column_header_cell('Qty Ordens', display=[
                                            "none", "none", "table-cell", "table-cell"]),

                rx.table.column_header_cell(
                    'Edit', display=["none", "none", "table-cell", "table-cell"]),

                rx.table.column_header_cell('Last Update', display=[
                                            "none", "none", "table-cell", "table-cell"]),

                rx.table.column_header_cell('Statement', align="center"),
            )
        ), rx.table.body(
            rx.foreach(list_heads, row_table)
        )
    )


def row_table(item: SuppliersDisplayItem) -> rx.Component:
    return rx.table.row(
        rx.table.cell(item.name),
        rx.table.cell(item.totalcompras, align="right", display=[
                      "none", "none", "table-cell", "table-cell"]),
        rx.table.cell(item.comisiones, align="right"),
        rx.table.cell(item.nro_orders, align="center", display=[
                      "none", "none", "table-cell", "table-cell"]),
        rx.table.cell(rx.dialog.root(
            rx.dialog.trigger(
                rx.text(
                    "Editar",
                    cursor="pointer",  # Hace que el cursor cambie al pasar por encima
                    # Cambia el color al pasar el mouse
                    _hover={"color": "blue"},
                    on_click=[StatesHeads.initialize_state(
                        item.nro_orders,
                        item.totalcompras,
                        item.comisiones),
                        States.set_current_parentname(item.name),
                        States.toggle_time_period(True)
                    ]
                )
            ),
            modal_update_fees_comission(
                item.id,
                item.name,
                item.nro_orders,
                item.totalcompras,
                item.comisiones
            )
        ), display=["none", "none", "table-cell", "table-cell"]
        ),
        rx.table.cell(
            rx.cond(
                item.lastupdate == datetime.now().date(),
                rx.text("Hoy"),
                rx.text(item.lastupdate)
            ), display=["none", "none", "table-cell", "table-cell"]
        ),
        rx.table.cell(
            rx.link(
                rx.text(
                    "Ver PDF",
                    cursor="pointer",
                    _hover={"color": "blue"},
                ),
                href=f"{os.getenv('API_URL')}/api/supplier-doc/{item.id}",
                target="_blank"
            ),
            align="center"
        ),
    )
