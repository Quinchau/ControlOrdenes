import reflex as rx
from sqlmodel import Field, select, desc, Relationship
import sqlalchemy
import hashlib


class Suppliers(rx.Model, table=True):
    supplierid: str = Field(default=None, primary_key=True)
    suppname: str
    currcode: str
    phn: str
    refaddress: str
    purchorders_list: list["PurchOrders"] = Relationship(
        back_populates="suppliername")


class Locations(rx.Model, table=True):
    loccode: str = Field(default=None, primary_key=True)
    locationname: str


class PurchOrders(rx.Model, table=True):
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


class Www_users(rx.Model, table=True):
    userid: str = Field(default=None, primary_key=True)
    password: str
    realname: str
    customerid: str
    supplierid: str
    salesman: str
    phone: str
    email: str
    defaultlocation: str
    fullaccess: int
    lastvisitdate: str
    branchcode: str
    blocked: int
    displayrecordsmax: int
    theme: str
    language: str
    pdflanguage: int
    accountdefault: int
    currencyuser: str


class States(rx.State):
    purchorders: list[PurchOrders] = []
    selected_order: PurchOrders = None
    locations: list[Locations] = []
    selected_location: str = "ALL"
    email: str = ""
    password: str = ""
    error_message: str = ""
    authenticated: bool = False

    @rx.event(background=True)
    async def get_all_purchs(self):
        async with self:
            with rx.session() as session:
                query = select(PurchOrders).options(sqlalchemy.orm.selectinload(PurchOrders.suppliername)
                                                    ).join(Suppliers).where(PurchOrders.status != "Completed", PurchOrders.status != "Cancelled"
                                                                            )
                if self.selected_location and self.selected_location != "ALL":
                    query = query.where(PurchOrders.intostocklocation == self.selected_location
                                        )
                query = query.order_by(
                    (PurchOrders.comments), Suppliers.suppname, Suppliers.refaddress)
                results = session.exec(query).all()
            self.purchorders = results

    @rx.event
    async def show_order_details(self, orderno: str):
        with rx.session() as session:
            self.selected_order = session.exec(
                select(PurchOrders).where(PurchOrders.orderno == orderno)
            ).first()

    @rx.event
    async def handle_delivered(self, orderno: str):
        with rx.session() as session:
            order = session.exec(
                select(PurchOrders).where(PurchOrders.orderno == orderno)
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
        if not self.authenticated:
            return rx.redirect("/login")
        self.selected_location = "ALL"
        return States.get_all_purchs

    @rx.var
    def last_four_digits(self) -> str:
        """A computed var that returns the last 4 digits."""
        return self.requisitionno[-4:]

    @rx.event
    async def handle_submit(self, form_data: dict):
        def hash_password(password: str, algorithm: str = 'sha1') -> str:
            """Hashes a password using the specified algorithm."""
            if algorithm == 'sha1':
                return hashlib.sha1(password.encode()).hexdigest()
            elif algorithm == 'md5':
                return hashlib.md5(password.encode()).hexdigest()
            else:
                return password

        email = form_data.get("email")
        password = form_data.get("password")

        # Agregar mensajes de depuración
        # print("Form data received:", form_data)
        # print("Email:", email)
        # print("Password:", password)

        if not email or not password:
            self.error_message = "Please enter both email and password"
            return

        with rx.session() as session:
            user = session.exec(
                select(Www_users).where(Www_users.email == email)
            ).first()

            if user:
                # or 'md5' based on your requirement
                hashed_input_password = hash_password(password, 'sha1')
                if user and user.password == hashed_input_password:
                    self.authenticated = True
                    self.email = user.email
                    return rx.redirect("/")
                else:
                    self.error_message = "Invalid credentials"
            else:
                self.error_message = "Invalid credentials"

    @rx.event
    def check_auth(self):
        # Check if user is authenticated
        if not self.authenticated:
            return rx.redirect("/login")

    @rx.event
    async def logout(self):
        """Cerrar sesión del usuario."""
        self.authenticated = False
        self.email = ""
        self.password = ""
        self.error_message = ""
        return rx.redirect("/login")


def show_location(location: Locations):
    return location.loccode
