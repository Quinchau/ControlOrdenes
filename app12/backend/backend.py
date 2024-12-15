import reflex as rx
from sqlmodel import Field, select, desc, Relationship
import sqlalchemy


class Suppliers(rx.Model, table=True):
    supplierid: str = Field(default=None, primary_key=True)
    suppname: str
    currcode: str
    phn: str
    refaddress: str
    purchorders_list: list["PurchOrders12"] = Relationship(
        back_populates="suppliername")


class Locations(rx.Model, table=True):
    loccode: str = Field(default=None, primary_key=True)
    locationname: str


class PurchOrders12(rx.Model, table=True):
    orderno: str = Field(default=None, primary_key=True)
    supplierno: str = Field(default=None, foreign_key="suppliers.supplierid")
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
    suppliername: Suppliers | None = Relationship(
        back_populates="purchorders_list")


class States(rx.State):
    purchorders: list[PurchOrders12] = []
    selected_order: PurchOrders12 = None
    locations: list[Locations] = []
    selected_location: str = "ALL"

    @rx.event(background=True)
    async def get_all_purchs(self):
        async with self:
            with rx.session() as session:
                query = select(PurchOrders12).options(
                    sqlalchemy.orm.selectinload(PurchOrders12.suppliername)
                ).join(
                    Suppliers
                ).where(
                    PurchOrders12.status != "Completed",
                    PurchOrders12.status != "Cancelled"
                )
                if self.selected_location and self.selected_location != "ALL":
                    query = query.where(
                        PurchOrders12.intostocklocation == self.selected_location
                    )
                query = query.order_by(
                    (PurchOrders12.comments),
                    Suppliers.refaddress
                )
                results = session.exec(query).all()
            self.purchorders = results

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

    @rx.var
    def last_four_digits(self) -> str:
        """A computed var that returns the last 4 digits."""
        return self.requisitionno[-4:]


def show_location(location: Locations):
    return location.loccode
