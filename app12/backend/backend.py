import reflex as rx
from sqlmodel import Field, select, Relationship, update
import sqlalchemy.orm as sqlorm
import sqlalchemy as sq
import hashlib
from typing import Optional


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


class Locstock(rx.Model, table=True):
    loccode: str
    stockid: str = Field(default=None, primary_key=True,
                         foreign_key="stockmaster.stockid")
    quantity: int
    reorderlevel: int
    location: str
    lowstockfee: int
    stock_master: Optional["StockMaster"] = Relationship(
        back_populates="loc_stocks")


class StockMaster(rx.Model, table=True):
    stockid: str = Field(default=None, primary_key=True)
    categoryid: str
    description: str
    minimo: int
    stock_image: Optional["Stock_Image"] = Relationship(
        back_populates="stock_master")
    loc_stocks: list["Locstock"] = Relationship(back_populates="stock_master")


class Stock_Image(rx.Model, table=True):
    id_image: int = Field(default=None, primary_key=True)
    id_product: str = Field(default=None, foreign_key="stockmaster.stockid")
    position: int
    cover: int
    imagen_principal: int
    stock_master: Optional[StockMaster] = Relationship(
        back_populates="stock_image")


class StockDisplayItem(rx.Base):
    """Modelo para mostrar en la tabla."""
    stockid: str
    description: str
    lowstockfee: int
    id_image: Optional[int]


class SearchResult(rx.Base):
    stockid: str
    description: str


class States(rx.State):
    purchorders: list[PurchOrders] = []
    selected_order: PurchOrders = None
    locations: list[Locations] = []
    selected_location: str = "ALL"
    email: str = rx.LocalStorage("")
    password: str = ""
    error_message: str = ""
    auth_token: str = rx.LocalStorage("")
    stocklowfee: list[StockMaster] = []
    user_warehouse: str = rx.LocalStorage("")
    search_term: str = ""  # Initialize with empty string
    search_results: list[SearchResult] = []
    selected_product: str = ""

    @rx.event(background=True)
    async def get_all_purchs(self):
        async with self:
            with rx.session() as session:
                query = select(PurchOrders).options(sqlorm.selectinload(PurchOrders.suppliername)
                                                    ).join(Suppliers).where(PurchOrders.status != "Completed", PurchOrders.status != "Cancelled"
                                                                            )
                if self.selected_location != "ALL":
                    query = query.where(PurchOrders.intostocklocation == self.selected_location
                                        ).order_by(PurchOrders.comments,
                                                   Suppliers.refaddress, Suppliers.suppname)
                results = session.exec(query).all()
            self.purchorders = results
            # print(self.purchorders)

    @rx.event(background=True)
    async def get_prod_lowstockfee(self):
        async with self:
            with rx.session() as session:
                query = select(
                    StockMaster.stockid,
                    StockMaster.description,
                    Locstock.lowstockfee,
                    Stock_Image.id_image,
                    Locations.locationname
                ).join(Locstock, StockMaster.stockid == Locstock.stockid).outerjoin(Stock_Image, StockMaster.stockid == Stock_Image.id_product
                                                                                    ).join(Locations, Locations.loccode == Locstock.loccode).where(Locstock.lowstockfee == 1)
                if self.selected_location != "ALL":
                    query = query.where(Locstock.loccode == self.selected_location,
                                        Locstock.lowstockfee == 1)

            results = session.exec(query).all()

            self.stocklowfee = [
                StockDisplayItem(
                    stockid=row[0],
                    description=row[1],
                    lowstockfee=row[2],
                    id_image=row[3],
                    locationname=row[4],
                    # Add image_url and call get_image_path
                    image_url=self.get_image_path(row[3])
                ) for row in results
            ]

            # Imprime el tipo y los datos para verificación
            # print(type(self.stocklowfee))
            # print(self.stocklowfee)

    def get_image_path(self, id_image) -> str:
        if id_image is None:
            return "/nophoto.jpg"

        image_id_str = str(id_image)
        lista_digitos = list(image_id_str)
        image_path = 'https://quinchau.com/webmaster2/weberp/img/p/' + \
            '/'.join(lista_digitos) + "/" + image_id_str + ".jpg"
        return image_path

    @rx.event(background=True)
    async def exclude_product(self, stockid):
        async with self:
            with rx.session() as session:
                try:
                    # Construir la declaración de actualización
                    if self.selected_location == "ALL":
                        return rx.window_alert("Debe seleccionar una ubicación para Agregar/Eliminar Productos")

                    stmt = update(Locstock).where(
                        (Locstock.stockid == stockid) &
                        (Locstock.loccode == self.selected_location)
                    ).values(lowstockfee=0)

                    # Ejecutar la actualización
                    session.exec(stmt)
                    session.commit()

                    # Recargar tabla

                    return States.get_prod_lowstockfee

                except Exception as e:
                    session.rollback()
                    print(f"Error al actualizar producto: {e}")

    @rx.event
    def set_search_term(self, value: str):
        self.search_term = value

    @rx.event
    async def select_product(self, stockid: str):
        self.selected_product = stockid
        return States.update_lowstockfee(stockid)

    @rx.event(background=True)
    async def update_lowstockfee(self, stockid: str):
        async with self:
            with rx.session() as session:
                try:
                    stmt = (
                        update(Locstock)
                        .where(Locstock.stockid == stockid,
                               Locstock.lowstockfee == self.selected_location)
                        .values(lowstockfee=1)
                    )
                    session.exec(stmt)
                    session.commit()

                    self.search_results = []
                    self.search_term = ""
                    return [
                        States.get_prod_lowstockfee,
                    ]
                except Exception as e:
                    print(f"Error al actualizar el producto: {e}")

    @rx.event
    def key_down_handler(self, key: str):
        if key == "Delete":
            return States.clear_search
        elif key == "Enter":
            return States.search_products

    @rx.event(background=True)
    async def clear_search(self):
        async with self:
            self.search_results = []
            self.search_term = ""

    @rx.event(background=True)
    async def search_products(self):
        async with self:
            with rx.session() as session:
                try:
                    query = (
                        select(
                            StockMaster.stockid,
                            StockMaster.description
                        )
                        .join(
                            Locstock,
                            StockMaster.stockid == Locstock.stockid
                        )
                        .where(
                            (StockMaster.stockid.ilike(f"%{self.search_term}%")) |
                            (StockMaster.description.ilike(
                                f"%{self.search_term}%"))
                        )
                        .group_by(
                            StockMaster.stockid,
                            StockMaster.description
                        )
                    )

                    results = session.exec(query).all()
                    self.search_results = [
                        {"stockid": r[0], "description": r[1]}
                        for r in results
                    ]

                except Exception as e:
                    print(f"Error en la búsqueda: {e}")

    @rx.event(background=True)
    async def add_to_lowstockfee(self, stockid: str):
        async with self:
            with rx.session() as session:
                try:
                    if self.selected_location == "ALL":
                        return rx.window_alert("Debe seleccionar una ubicación para Agregar/Eliminar Productos")

                    # Actualizar lowstockfee a 1
                    stmt = update(Locstock).where(
                        (Locstock.stockid == stockid) &
                        (Locstock.loccode == self.selected_location)
                    ).values(lowstockfee=1)

                    session.exec(stmt)
                    session.commit()

                    # Limpiar resultados de búsqueda
                    self.search_results = []
                    self.search_term = ""

                    print(f"Producto '{stockid}'")
                    print(f"Location '{self.selected_location}'")

                    # Recargar la lista principal
                    return States.get_prod_lowstockfee

                except Exception as e:
                    session.rollback()
                    print(f"Error al agregar producto: {e}")

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
    def set_selected_location_lowstockfee(self, value):
        self.selected_location = value
        return States.get_prod_lowstockfee

    @rx.event
    async def on_load(self):
        if not self.auth_token:
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
        if not email or not password:
            self.error_message = "Please enter both email and password"
            return

        with rx.session() as session:
            user = session.exec(
                select(Www_users).where(Www_users.email == email)
            ).first()

            if user:
                # or 'md5' based on your requirement
                if user and user.password == hash_password(password, 'sha1'):
                    self.auth_token = user.userid
                    self.email = user.email
                    self.user_warehouse = user.defaultlocation

                    return rx.redirect("/")
                else:
                    self.error_message = "Invalid credentials"
            else:
                self.error_message = "Invalid credentials"

    @rx.event
    def check_auth(self):
        # Check if user is authenticated and has valid token
        if not self.auth_token:
            return rx.redirect("/login")

    @rx.event
    async def logout(self):
        """Cerrar sesión del usuario."""
        self.auth_token = ""
        self.email = ""
        return [
            rx.remove_local_storage("states.authenticated"),
            rx.remove_local_storage("states.email"),
            rx.remove_local_storage("states.auth_token"),
            rx.remove_local_storage("states.user_warehouse"),
            rx.redirect("/login")
        ]

        def get_user_warehouse(email):
            with session() as session:
                user = session.query(Www_users).filter_by(email=email).first()
                if user:
                    return user.defaultlocation
                else:
                    return None


def show_location(location: Locations):
    return location.loccode
