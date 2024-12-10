import reflex as rx
from sqlmodel import Field, select, desc, Relationship


class Suppliers(rx.Model, table=True):
    supplierid: str = Field(default=None, primary_key=True)
    suppname: str
    currcode: str
    phn: str


class Locations(rx.Model, table=True):
    loccode: str = Field(default=None, primary_key=True)
    locationname: str


class PurchOrders12(rx.Model, table=True):
    orderno: str = Field(default=None, primary_key=True)
    supplierno: str
    comments: str
    orddate: str
    requisitionno: str
    orderref: str
    status: str
    urltracking: str
    deladd1: str
    deladd2: str
    deladd3: str
    intostocklocation: str


class States(rx.State):
    purchorders: list[PurchOrders12] = []
    selected_order: PurchOrders12 = None
    locations: list[Locations] = []
    selected_location: str = "ALL"

    @rx.event(background=True)
    async def get_all_purchs(self):
        async with self:
            with rx.session() as session:
                query = select(PurchOrders12).where(
                    PurchOrders12.status != "Completed",
                    PurchOrders12.status != "Cancelled"
                )

                # El filtro debe estar dentro del bloque with rx.session
                if self.selected_location and self.selected_location != "ALL":
                    query = query.where(
                        PurchOrders12.intostocklocation == self.selected_location
                    )

                query = query.order_by(
                    desc(PurchOrders12.orddate), PurchOrders12.comments
                )
                # La ejecución del query debe estar dentro del bloque with rx.session
                self.purchorders = session.exec(query).all()

    @rx.event
    async def show_order_details(self, orderno: str):
        with rx.session() as session:
            self.selected_order = session.exec(
                select(PurchOrders12).where(PurchOrders12.orderno == orderno)
            ).first()

    @rx.event
    async def handle_delivered(self, orderno: str):
        with rx.session() as session:
            order = session.exec(
                select(PurchOrders12).where(PurchOrders12.orderno == orderno)
            ).first()
            order.status = "Completed"
            session.commit()
        return States.get_all_purchs

    @rx.event
    def load_locations(self):
        """Cargar las ubicaciones."""
        with rx.session() as session:
            self.locations = session.exec(select(Locations)).all()

    @rx.event
    def set_selected_location(self, value):
        self.selected_location = value
        return States.get_all_purchs

    @rx.event
    async def on_load(self):
        self.selected_location = "ALL"
        return States.get_all_purchs


def show_location(location: Locations):
    return location.loccode
