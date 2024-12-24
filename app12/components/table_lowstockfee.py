import reflex as rx
from ..backend.backend import States
from .filter_orders import filter_component


def table_lowstockfee(state: States) -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.box(
                rx.input(
                    value=state.search_term,
                    placeholder="Buscar productos...",
                    on_change=state.set_search_term,
                    on_key_down=States.key_down_handler,
                ),
                width="50%",
            ),
            rx.box(
                rx.button(
                    "Buscar",
                    on_click=state.search_products,
                    background_color="blue.500",

                ),
                width="20%",
            ),
            rx.box(
                filter_component(
                    States.set_selected_location_lowstockfee),
                width="30%",
            ),
            width="100%",
            # box_shadow="rgba(0, 0, 0, 0.15) 0px 2px 8px"
        ),
        rx.table.root(
            rx.table.header(
                rx.table.row(
                )
            ),
            rx.table.body(
                rx.foreach(
                    state.search_results,
                    lambda item: rx.table.row(
                        rx.table.cell(item["stockid"]),
                        rx.table.cell(item["description"]),
                        on_click=lambda: state.add_to_lowstockfee(
                            item["stockid"]),
                        style={
                            "_hover": {
                                "cursor": "pointer",
                                "bg": rx.color("gray", 3)
                            }
                        }
                    )
                )
            ),
        ),
        width="100%"
    )
