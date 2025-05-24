# Project Structure

```
app12/
  admin/
    __init__.py
    master.py
  api/
    views/
      download_pdf_commission.py
    __init__.py
  backend/
    __init__.py
    backend.py
    heads_backend.py
  components/
    __init__.py
    color_status.py
    filter_orders.py
    main_table_heads_admin.py
    main_table_heads.py
    main_table_lowstockfee_admin.py
    main_table_lowstockfee.py
    main_table.py
    modal_inputs_fees_purchs_total.py
    modal_status_heads.py
    modal_status.py
    navbar.py
    table_lowstockfee.py
    ui_base_page.py
  documentacion/
    estructura_general
  __init__.py
  amazon_index.py
  app12.py
  applicable_fees_admin.py
  control_heads.py
  heads_admin.py
  index_admin.py
  login.py
  lowstockfee.py
  marykay_index.py
  purchs_page.py
  tasks.py
assets/
  drops-6392473_640.jpg
  drops-6392473_640.jpg:Zone.Identifier
  favicon.ico
  icon-192x192.png
  icon-512x512.png
  logo.jpg
  logo.jpg:Zone.Identifier
  manifest.json
  nophoto.jpg
  nophoto.jpg:Zone.Identifier
  sw.js
github/
  workflows/
    deploy.yml
    requirements.txt
upload_files/
  2882UQ_document.pdf
uploaded_files/
  1183UX_document.pdf
  2882UQ_document.pdf
  6613QL_document.pdf
  6619QL_document.pdf
  6999QN_document.pdf
  7603IX_document.pdf
  7779QL_document.pdf
  8044UE_document.pdf
  9844QJ_document.pdf
  9866WK_document.pdf
.env
.gitignore
alembic.ini
logica.txt
README.md
reflex.db
requirements.txt
rxconfig.py
```



# Selected Files Content

## app12/admin/__init__.py

```py

```

## app12/admin/master.py

```py
import reflex as rx
from rxconfig import config
from ..backend.backend import States


class State(rx.State):
    """The app state."""

    ...


@rx.page(route="/admin/master", title="Master", on_load=States.check_auth)
def index() -> rx.Component:
    return rx.cond(
        States.auth_token != "",  # Check if token exists in LocalStorage
        # Authenticated view
        rx.flex(
            rx.vstack(
                rx.button("Gestion Mary Kay",
                          width='40vh',
                          height='7vh',
                          radius='full',
                          on_click=rx.redirect("/purchs_page")),
                rx.button("Gestion Amazon",
                          width='40vh',
                          height='7vh',
                          radius='full',
                          disable='True',
                          on_click=rx.toast("Próximamente...")),
                rx.button("Otros",
                          width='40vh',
                          height='7vh',
                          radius='full',
                          disable='True',
                          on_click=rx.toast("Próximamente...")),
                rx.button("Salir",
                          width='40vh',
                          height='7vh',
                          radius='full',
                          on_click=States.logout),
                rx.code("to-do-easy.com",
                        size="6",
                        color_scheme="indigo",
                        weight="bold"),
                border_width="2px",
                border_radius="1em",
                align='center',
                width='100vh',
                height="100vh",
                justify='center',
                max_width='400px',
                spacing="9",
                background_image="url('/drops-6392473_640.jpg')",
            ),
            justify='center'
        ),

    )


app = rx.App()
```

## app12/api/views/download_pdf_commission.py

```py
from fastapi import APIRouter
import reflex as rx
from fastapi.responses import FileResponse
import os
from datetime import datetime

router = APIRouter()

async def get_supplier_doc(supplier_id: str):
    clean_supplier_id = supplier_id.rstrip('/')
    file_path = rx.get_upload_dir() / f"{clean_supplier_id}_document.pdf"
    print(f"Buscando archivo en: {file_path}")
    if os.path.exists(file_path):
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d_%H%M%S")
        new_filename = f"{clean_supplier_id}_document_{timestamp}.pdf"
        return FileResponse(
            file_path,
            media_type="application/pdf",
            filename=new_filename,
            headers={"Cache-Control": "no-store"}  # Evita que el navegador almacene la respuesta
        )
    else:
        print(f"Archivo no encontrado: {file_path}")
        return {"error": "Document not found"}
```

## app12/api/__init__.py

```py

```

## app12/backend/__init__.py

```py

```

## app12/backend/backend.py

```py
import reflex as rx
from sqlmodel import SQLModel, Field, select, Relationship, update, func
import sqlalchemy.orm as sqlorm
from sqlalchemy import select, and_, func
from sqlalchemy.sql.expression import or_, not_
import hashlib
from typing import Optional
from time import strftime
from datetime import datetime, timedelta

# En: /home/charlie_ubu/proyectos/app12/app12/backend/backend.py


class Suppliers(SQLModel, table=True):
    supplierid: str = Field(default=None, primary_key=True)
    suppname: str
    currcode: str
    supptype: str
    phn: str
    refaddress: str
    remittance: int
    lastupdate: str
    monthly_orders_numbers: str
    monthly_fees: float
    monthly_orders_totals: float
    purchorders_list: list["PurchOrders"] = Relationship(
        back_populates="suppliername")


class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    description: str = Field(max_length=255)
    # Podrías usar un Enum aquí si prefieres
    status: str = Field(default="Pending")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default=None)
    user_id: str = Field(max_length=20, foreign_key="www_users.userid")


class Suppliertype(SQLModel, table=True):
    typeid: str = Field(default=None, primary_key=True)
    typename: str


class Locations(SQLModel, table=True):
    loccode: str = Field(default=None, primary_key=True)
    locationname: str


class PurchOrders(SQLModel, table=True):
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


class PurchOrdersDetails(SQLModel, table=True):
    orderno: str = Field(default=None, primary_key=True)
    itemdescription: str
    unitprice: str


class Www_users(SQLModel, table=True):
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


class Locstock(SQLModel, table=True):
    loccode: str
    stockid: str = Field(default=None, primary_key=True,
                         foreign_key="stockmaster.stockid")
    quantity: int
    reorderlevel: int
    location: str
    lowstockfee: int
    stock_master: Optional["StockMaster"] = Relationship(
        back_populates="loc_stocks")


class StockMaster(SQLModel, table=True):
    stockid: str = Field(default=None, primary_key=True)
    categoryid: str
    description: str
    minimo: int
    stock_image: Optional["Stock_Image"] = Relationship(
        back_populates="stock_master")
    loc_stocks: list["Locstock"] = Relationship(back_populates="stock_master")


class Stock_Image(SQLModel, table=True):
    id_image: int = Field(default=None, primary_key=True)
    id_product: str = Field(default=None, foreign_key="stockmaster.stockid")
    position: int
    cover: int
    imagen_principal: int
    stock_master: Optional[StockMaster] = Relationship(
        back_populates="stock_image")


class PurchOrdersDisplay(rx.Base):
    order: str
    refaddress: str
    suppliername: str
    requisition: str
    comments: str


class PurchOrdersModalDisplay(rx.Base):
    orderno: str
    orderref: str
    requisitionno: str
    urltracking: str
    supplierno: str
    deladd1: str
    deladd2: str
    comments: str
    orddate: str


class StockDisplayItem(rx.Base):
    """Modelo para mostrar en la tabla."""
    stockid: str
    description: str
    lowstockfee: int
    id_image: Optional[int]


class SuppliersDisplayItem(rx.Base):
    id: str
    name: str
    nro_orders: str
    comisiones: Optional[float] = None
    totalcompras: Optional[float] = None
    typename: str
    locations: str
    lastupdate: Optional[str] = None


class ChildrensOrdersDisplay(rx.Base):
    childrenid: str
    childrenname: str
    parentname: str
    ordersmonth: str


class ChildrensOrdersDisplayDetails(rx.Base):
    childrenid: str
    childrenname: str
    parentname: str
    ordersmonthdetails: Optional[str] = None


class SearchResult(rx.Base):
    stockid: str
    description: str


class States(rx.State):
    purchorders: list[PurchOrdersDisplay] = []
    selected_order: PurchOrdersModalDisplay = None
    locations: list[Locations] = []
    selected_location: str = "ALL"
    email: str = rx.LocalStorage("")
    password: str = ""
    error_message: str = ""
    auth_token: str = rx.LocalStorage("")
    stocklowfee: list[StockMaster] = []
    user_warehouse: str = rx.LocalStorage("")
    search_term: str = ""
    search_results: list[SearchResult] = []
    selected_product: str = ""
    heads_suppliers: list[SuppliersDisplayItem] = []
    order_by_head: list[Suppliers] = []
    children_orders: list[ChildrensOrdersDisplay] = []
    children_orders_details: list[ChildrensOrdersDisplayDetails] = []
    show_current_month: bool = True
    current_parentname: str = ""
    tasks: list[Task] = []  # Lista de tareas
    new_task_description: str = ""
    dialog_open: bool = False  # Estado para controlar el modal de tareas

    @rx.event(background=True)
    async def load_tasks(self):
        """Cargar todas las tareas de la base de datos."""
        async with self:
            with rx.session() as session:
                query = select(Task).order_by(Task.created_at.desc())
                results = session.exec(
                    query).scalars().all()  # Añadir .scalars()
                self.tasks = results
                # print("Tasks loaded:", [vars(t) for t in self.tasks])

    @rx.var(cache=True)
    def formatted_tasks(self) -> list[dict[str, str]]:
        """Devuelve las primeras 100 tareas con fechas y nombres de usuarios para creación y actualización."""
        if not self.tasks:
            return []

        # Obtener nombres de usuarios desde Www_users
        with rx.session() as session:
            users = session.exec(
                select(Www_users.userid, Www_users.realname)).all()
            user_dict = {user.userid: user.realname for user in users}

        # Dividir tareas en "Pending" y "Completed"
        pending_tasks = [t for t in self.tasks if t.status == "Pending"]
        completed_tasks = [t for t in self.tasks if t.status == "Completed"]

        # Ordenar "Pending" por created_at ascendente (menos reciente primero)
        pending_tasks.sort(key=lambda x: x.created_at)

        # Ordenar "Completed" por updated_at descendente (más reciente primero), con None al final
        completed_tasks.sort(key=lambda x: (
            x.updated_at is None, x.updated_at), reverse=True)

        # Combinar listas: primero Pending, luego Completed, y limitar a 100
        sorted_tasks = (pending_tasks + completed_tasks)[:100]

        # Formatear las tareas ordenadas
        return [
            {
                "id": str(task.id),
                "description": str(task.description),
                "status": str(task.status),
                "created_at": str(
                    f"{task.created_at.strftime('%Y-%m-%d %H:%M')} by {user_dict.get(task.user_id, 'Desconocido')}"
                    if task.created_at else "Sin fecha"
                ),
                "updated_at": str(
                    f"{task.updated_at.strftime('%Y-%m-%d %H:%M')} by {user_dict.get(task.user_id, 'Desconocido')}"
                    if task.updated_at else "Pending"
                ),
                "user_id": str(task.user_id),
            }
            for task in sorted_tasks
        ]

    def toggle_dialog(self, is_open: bool):
        self.dialog_open = is_open

    @rx.event(background=True)
    async def create_task(self):
        """Crear una nueva tarea con validación mejorada."""
        async with self:
            # Validar si la descripción está vacía o solo tiene espacios
            if not self.new_task_description or self.new_task_description.strip() == "":
                return rx.window_alert("Por favor, ingresa una descripción válida para la tarea.")
            if not self.auth_token:
                return rx.redirect("/login")

            with rx.session() as session:
                new_task = Task(
                    description=self.new_task_description.strip(),  # Eliminar espacios innecesarios
                    status="Pending",
                    user_id=self.auth_token,
                )
                session.add(new_task)
                session.commit()
                self.new_task_description = ""  # Limpiar el campo
                return States.load_tasks

    @rx.event(background=True)
    async def toggle_task_status(self, task_id: int):
        """Cambiar el estado de una tarea de 'Pending' a 'Completed', sin permitir el regreso a 'Pending'."""
        async with self:
            with rx.session() as session:
                task = session.get(Task, task_id)
                if task and task.status == "Pending":  # Solo permitir cambio si está en "Pending"
                    task.status = "Completed"
                    task.updated_at = datetime.now()
                    task.user_id = self.auth_token  # Registrar quién cambió el estado
                    session.add(task)
                    session.commit()
                return States.load_tasks

    def set_new_task_description(self, value: str):
        """Actualizar la descripción de la nueva tarea."""
        self.new_task_description = value

    @rx.event
    async def toggle_time_period(self, value: bool):
        """Toggle between current month and last 30 days view."""
        self.show_current_month = value
        return States.get_children_orders_details(self.current_parentname)

    @rx.event
    async def set_current_parentname(self, parentname: str):
        self.current_parentname = parentname

    @rx.event(background=True)
    async def get_children_orders_details(self, parentname: str):
        async with self:
            try:
                self.current_parentname = parentname
                with rx.session() as session:
                    today = datetime.now()
                    if self.show_current_month:
                        start_date = today.replace(
                            day=1, hour=0, minute=0, second=0, microsecond=0)
                        current_date = today
                    else:
                        start_date = datetime.now() - timedelta(days=32)
                        current_date = today

                    subquery = select(Suppliers.supplierid).where(
                        Suppliers.phn.ilike(f"%{parentname}%")
                    )

                    # Consulta principal con LEFT OUTER JOIN y exclusión de Hold/Canceled
                    query = select(
                        Suppliers.supplierid.label('padre_id'),
                        Suppliers.suppname.label('padre_name'),
                        Suppliers.phn.label('supervisor_name'),
                        func.group_concat(
                            PurchOrders.orderref).label('order_refs')
                    ).outerjoin(
                        PurchOrders,
                        and_(
                            PurchOrders.supplierno == Suppliers.supplierid,
                            PurchOrders.orddate.between(
                                start_date, current_date),
                            not_(
                                or_(
                                    func.lower(PurchOrders.comments).like(
                                        'hold'),
                                    func.lower(PurchOrders.comments).like(
                                        'canceled')
                                )
                            )
                        )
                    ).where(
                        Suppliers.supplierid.in_(subquery)
                    ).group_by(
                        Suppliers.supplierid,
                        Suppliers.suppname,
                        Suppliers.phn
                    ).order_by(
                        PurchOrders.orderref.asc()
                    )

                results = session.exec(query).all()
                self.children_orders_details = [
                    ChildrensOrdersDisplayDetails(
                        childrenid=row[0],
                        childrenname=row[1],
                        parentname=row[2],
                        ordersmonthdetails=str(row[3]).replace(
                            ',', ', ') if row[3] else ""
                    ) for row in results
                ]

            except Exception as e:
                print(f"Error executing query: {e}")

    @rx.event(background=True)
    async def get_children_orders(self, parentname: str):
        async with self:
            try:
                with rx.session() as session:
                    current_month = strftime("%Y-%m")

                    # Subquery para obtener los IDs de los hijos
                    subquery = select(Suppliers.supplierid).where(
                        Suppliers.phn.ilike(f"%{parentname}%")
                    )

                    # Consulta principal con LEFT OUTER JOIN y exclusión de Hold/Canceled
                    query = select(
                        Suppliers.supplierid.label('padre_id'),
                        Suppliers.suppname.label('padre_name'),
                        Suppliers.phn.label('supervisor_name'),
                        func.count(PurchOrders.orderno).label('count_orders')
                    ).outerjoin(
                        PurchOrders,
                        and_(
                            PurchOrders.supplierno == Suppliers.supplierid,
                            PurchOrders.orddate.like(f'{current_month}%'),
                            not_(
                                or_(
                                    func.lower(PurchOrders.comments).like(
                                        'hold'),
                                    func.lower(PurchOrders.comments).like(
                                        'canceled')
                                )
                            )
                        )
                    ).where(
                        Suppliers.supplierid.in_(subquery)
                    ).group_by(
                        Suppliers.supplierid,
                        Suppliers.suppname,
                        Suppliers.phn
                    ).order_by(
                        func.count(PurchOrders.orderno).desc()
                    )
                    results = session.exec(query).all()
                    self.children_orders = [
                        ChildrensOrdersDisplay(
                            childrenid=row[0],
                            childrenname=row[1],
                            parentname=row[2],
                            ordersmonth=row[3]
                        ) for row in results
                    ]

                    # print("Query Results:", results)
                    # print("Current Month:", current_month)

            except Exception as e:
                print(f"Error executing query: {e}")

            except Exception as e:
                print(f"Error executing query: {e}")

    @rx.event(background=True)
    async def get_all_heads(self):
        async with self:
            with rx.session() as session:
                query = select(Suppliers.supplierid,
                               Suppliers.suppname,
                               Suppliers.monthly_orders_numbers,
                               Suppliers.monthly_fees,
                               Suppliers.monthly_orders_totals,
                               Suppliertype.typename,
                               Locations.loccode,
                               Suppliers.lastupdate
                               ).join(
                    Suppliertype, Suppliertype.typeid == Suppliers.supptype).join(Locations, Locations.locationname == Suppliertype.typename).where(
                    Suppliers.remittance == 1).order_by(Suppliers.monthly_orders_numbers)
            if self.selected_location != "ALL":
                query = query.where(self.selected_location ==
                                    Locations.loccode)
            results = session.exec(query).all()
            self.heads_suppliers = [
                SuppliersDisplayItem(
                    id=row[0],
                    name=row[1],
                    nro_orders=row[2],
                    comisiones=row[3],
                    totalcompras=row[4],
                    typename=row[5],
                    locations=row[6],
                    lastupdate=str(row[7]) if row[7] else None
                ) for row in results
            ]

            # print(self.heads_suppliers)
            # print(f'Selec_location: {self.selected_location}')

    @rx.event(background=True)
    async def get_all_purchs(self):
        async with self:
            with rx.session() as session:
                query = select(PurchOrders.orderno,
                               Suppliers.refaddress,
                               Suppliers.suppname,
                               PurchOrders.requisitionno,
                               PurchOrders.comments
                               ).join(Suppliers, Suppliers.supplierid == PurchOrders.supplierno
                                      ).where(PurchOrders.status != "Completed", PurchOrders.status != "Cancelled"
                                              )
                if self.selected_location != "ALL":
                    query = query.where(PurchOrders.intostocklocation == self.selected_location
                                        ).order_by(PurchOrders.comments,
                                                   Suppliers.refaddress, Suppliers.suppname)
                results = session.exec(query).all()
                self.purchorders = [PurchOrdersDisplay(
                                    order=row[0],
                                    refaddress=row[1],
                                    suppliername=row[2],
                                    requisition=row[3],
                                    comments=row[4]
                                    )
                                    for row in results
                                    ]
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

                    # print(f"Producto '{stockid}'")
                    # print(f"Location '{self.selected_location}'")

                    # Recargar la lista principal
                    return States.get_prod_lowstockfee

                except Exception as e:
                    session.rollback()
                    print(f"Error al agregar producto: {e}")

    @rx.event
    async def show_order_details(self, orderno: str):
        with rx.session() as session:
            query = select(PurchOrders.orderno,
                           PurchOrders.orderref,
                           PurchOrders.requisitionno,
                           PurchOrders.urltracking,
                           PurchOrders.supplierno,
                           PurchOrders.deladd1,
                           PurchOrders.deladd2,
                           PurchOrders.comments,
                           PurchOrders.orddate
                           ).where(PurchOrders.orderno == orderno)

            results = session.exec(query).first()

            self.selected_order = PurchOrdersModalDisplay(
                orderno=results[0],
                orderref=results[1],
                requisitionno=results[2],
                urltracking=results[3],
                supplierno=results[4],
                deladd1=results[5],
                deladd2=results[6],
                comments=results[7],
                orddate=str(results[8]))

    @rx.event
    async def handle_delivered(self, orderno: str):
        with rx.session() as session:
            order = session.get(PurchOrders, orderno)
            if order:
                order.status = "Completed"
                session.add(order)
                session.commit()

        # Refresh the orders list
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
    def set_selected_location_heads(self, value):
        self.selected_location = value
        return States.get_all_heads

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

    @rx.var(cache=False)
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
            # Modificar la consulta para incluir explícitamente los campos
            user = session.exec(
                select(
                    Www_users.userid,
                    Www_users.password,  # Añadir explícitamente password
                    Www_users.email,
                    Www_users.defaultlocation
                ).where(Www_users.email == email)
            ).first()

            if user:
                if user.password == hash_password(password, 'sha1'):
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


def alert_dialog(state):
    return rx.alert_dialog.root(
        rx.alert_dialog.content(
            rx.alert_dialog.title("Status"),
            rx.alert_dialog.description(state.dialog_message),
            rx.flex(
                rx.alert_dialog.action(
                    rx.button("OK",
                              on_click=state.set_show_dialog(False)
                              ),
                ),
                spacing="3",
                margin_top="16px",
                justify="end",
            ),
            style={"max_width": 450},
        ),
        open=state.show_dialog,
    )
```

## app12/backend/heads_backend.py

```py
import reflex as rx
from .backend import Suppliers, States
from sqlmodel import update
from sqlalchemy import func


class StatesHeads(rx.State):
    nro_orders: str = ""
    total_orders: float = 0.0
    comissions: float = 0.0
    dialog_message: str = ""
    show_dialog_pdf_upload: bool = False
    show_dialog: bool = False
    pdf_path: str = ""
    user_id: str = ""

    @rx.event
    async def set_user_id(self, user_id: str):
        self.user_id = user_id

    @rx.event
    async def handle_pdf_upload(self, files: list[rx.UploadFile]):
        if not files:
            return rx.toast.error("No se seleccionó ningún archivo")
        file = files[0]
        upload_data = await file.read()
        filename = f"{self.user_id}_document.pdf"
        outfile = rx.get_upload_dir() / f"{self.user_id}_document.pdf"
        try:
            with outfile.open("wb") as file_object:
                file_object.write(upload_data)
        except OSError as e:
            return rx.toast.error(f"Error al subir el archivo: {e}")
        self.pdf_path = filename
        return rx.toast.success(f"Archivo subido correctamente en: {outfile}")

    @rx.event
    def pdf_upload(self, value: bool):
        self.show_dialog_pdf_upload = value

    def initialize_state(self, nro_orders, total, comissions):
        """Inicializar el estado con los valores del registro."""
        self.nro_orders = nro_orders
        self.total_orders = total
        self.comissions = comissions

    @rx.event(background=True)
    async def update_comissions_amount_orders(self, id):
        async with self:
            with rx.session() as session:
                try:
                    stmt = update(Suppliers).where(
                        Suppliers.supplierid == id
                    ).values(
                        monthly_fees=self.comissions,
                        monthly_orders_totals=self.total_orders,
                        monthly_orders_numbers=self.nro_orders,
                        lastupdate=func.now()
                    )

                    session.exec(stmt)
                    session.commit()

                except Exception as e:
                    session.rollback()
                    self.dialog_message = f"Error al actualizar: {str(e)}"
                    self.show_dialog = True
                return States.get_all_heads
```

## app12/components/__init__.py

```py

```

## app12/components/color_status.py

```py
import reflex as rx
from ..backend.backend import States
from ..components.modal_status import modal_status, modal_status_info
from ..components.modal_status_heads import modal_status_heads


def _badge(icon: str, text: str):
    return rx.flex(
        rx.icon(icon, size=16),
        text,
        align_items="center",
        gap="4px",
        padding="x-2 y-1",
        color="black"
    )


def _badge_heads(icon: str, text: str):
    return rx.flex(
        rx.icon(icon, size=16),
        text,  # Aquí se utiliza el valor de text
        align_items="center",
        gap="4px",
        padding="x-2 y-1",
        color="black"
    )


def status_button_heads(n_orders: str, name: str):
    badge_mapping = {
        "0": ("ban", "0", "#E52B50"),
        "1": ("ban", "1", "#E52B50"),
        "2": ("ban", "2", "#E52B50"),
        "3": ("ban", "3", "#E85E65"),
        "4": ("loader", "4", "#E85E65"),
        "5": ("check", "5", "#00FF7F"),
    }

    icon, text, color = badge_mapping.get(
        n_orders, ("check", n_orders, "#00FF7F"))

    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                _badge_heads(icon, text),
                border_radius="20px",
                opacity=1,
                bg=color,
                color="white",
                _hover={"bg": "darken", "color": "white"},
                on_click=States.get_children_orders(name)
            )
        ),

        # Modal para ajuste Status
        modal_status_heads(),
    )


def status_button(status: str, orderno: str):
    badge_mapping = {
        "Delivered": ("check", "Delivered", "#00FF7F"),
        "On the way": ("loader", "On the way", "#FFF8DC"),
        "On Hold": ("ban", "On Hold", "#E52B50"),
        "Received": ("check", "Received", "#87CEEB"),
    }

    icon, text, color = badge_mapping.get(
        status, ("loader", "On the way", "#FFF8DC"))

    if status == "Delivered" or status == "On the way":
        return rx.dialog.root(
            rx.dialog.trigger(
                rx.button(
                    _badge(icon, text),
                    border_radius="20px",
                    opacity=1,
                    bg=color,
                    color="white",
                    _hover={"bg": "darken", "color": "white"},
                    on_click=States.show_order_details(orderno)
                )
            ),

            # Modal para ajuste Status
            modal_status(),
            # Fin de Modal
        )

    else:
        return rx.dialog.root(
            rx.dialog.trigger(
                rx.button(
                    _badge(icon, text),
                    border_radius="20px",
                    opacity=1,
                    bg=color,
                    color="white",
                    _hover={"bg": "darken", "color": "white"},
                    on_click=States.show_order_details(orderno)
                )
            ),

            # Modal para ajuste Status
            modal_status_info(),
            # Fin de Modal
        )
```

## app12/components/filter_orders.py

```py
import reflex as rx
from ..backend.backend import States


def filter_component(act_state) -> rx.Component:
    return rx.flex(
        rx.select.root(
            rx.select.trigger(placeholder="Filtrar Ordenes"),
            rx.select.content(
                rx.select.group(
                    rx.select.item("TODAS", value="ALL"),
                    rx.select.item("Carolina", value="VEN"),
                    rx.select.item("Pierina", value="PIE"),
                    rx.select.item("Franyeli", value="FRA"),
                    rx.select.item("Franchesca", value="STR"),
                ),
            ),
            value=States.selected_location,
            on_change=lambda value: act_state(value),
        ),
        justify="end",
        width="90%",
    )
```

## app12/components/main_table_heads_admin.py

```py
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
```

## app12/components/main_table_heads.py

```py
import reflex as rx
from ..backend.backend import SuppliersDisplayItem
from ..components.color_status import status_button_heads
from ..backend.backend import States


def table_heads(list_heads: list[SuppliersDisplayItem]) -> rx.Component:
    return rx.table.root(
        rx.table.header(
            rx.table.row(
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
        rx.table.cell(item.name[:12]),
        rx.table.cell(item.totalcompras),
        rx.table.cell(item.comisiones),
        rx.table.cell(
            rx.match(
                item.nro_orders,
                ("0", status_button_heads("0", item.name)),
                ("1", status_button_heads("1", item.name)),
                ("2", status_button_heads("2", item.name)),
                ("3", status_button_heads("3", item.name)),
                ("4", status_button_heads("4", item.name)),
                ("5", status_button_heads("5", item.name)),
                status_button_heads(item.nro_orders, item.name)
            )
        ),
    )
```

## app12/components/main_table_lowstockfee_admin.py

```py
import reflex as rx
from ..backend.backend import StockMaster
from ..backend.backend import States


def table_products(list_prod: list[StockMaster]) -> rx.Component:
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                rx.table.column_header_cell('Location'),
                rx.table.column_header_cell('Ref'),
                rx.table.column_header_cell('ASIN'),
                rx.table.column_header_cell('Item'),
                rx.table.column_header_cell('Fee'),
            )
        ), rx.table.body(
            rx.foreach(list_prod, row_table)
        )
    )


def row_table(item: dict) -> rx.Component:
    # Concatenación con f-strings (recomendado)
    return rx.table.row(
        rx.table.cell(item["locationname"]),
        rx.table.cell(
            rx.image(
                src=(item["image_url"]),
                width="40px",
                height="40px"
            )),
        rx.table.cell(item["stockid"]),
        rx.table.cell(item["description"]),
        rx.table.cell(rx.button(
            "Excluir",
            on_click=lambda stockid=item["stockid"]: States.exclude_product(
                stockid),  # Pasar stockid
            color_scheme="red",  # Estilo al boton
            size="1"  # Tamaño del boton
        ),
            style={
                "display": "flex",
                "align-items": "center",
                "justify-content": "center",
                "height": "100%"
        }),
    )
```

## app12/components/main_table_lowstockfee.py

```py
import reflex as rx
from ..backend.backend import StockMaster


def table_products(list_prod: list[StockMaster]) -> rx.Component:
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                rx.table.column_header_cell('Ref'),
                rx.table.column_header_cell('ASIN'),
                rx.table.column_header_cell('Item'),
            )
        ), rx.table.body(
            rx.foreach(list_prod, row_table)
        )
    )


def row_table(item: dict) -> rx.Component:
    # Concatenación con f-strings (recomendado)
    stockid_url = f"https://www.amazon.com/dp/{item['stockid']}"

    return rx.table.row(
        rx.table.cell(
            rx.image(
                src=(item["image_url"]),
                width="35px",
                height="35px"
            )),
        rx.table.cell(rx.link(  # Usamos rx.link para que sea un enlace
            item["stockid"],
            href=stockid_url,  # Establecemos la URL generada
            is_external=True  # Para que se abra en una nueva pestaña
        ),
            style={
                "align-items": "center",
                "height": "100%"
        }),
        rx.table.cell(item["description"]),
    )
```

## app12/components/main_table.py

```py
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
```

## app12/components/modal_inputs_fees_purchs_total.py

```py
import reflex as rx
from app12.backend.heads_backend import StatesHeads
from app12.backend.backend import States


def modal_update_fees_comission(id, name, nro_orders, total, comissions) -> rx.Component:
    return rx.dialog.content(
        rx.dialog.title("Current Month Orders"),
        rx.dialog.description(
            rx.flex(
                # Información de Usuario
                rx.vstack(
                    rx.hstack(
                        rx.text("UserId: ", width="150px"),
                        rx.text(id)
                    ),
                    rx.hstack(
                        rx.text("Name: ", width="150px"),
                        rx.text(name)
                    ),
                    width="100%",
                    spacing="3"
                ),

                # Inputs alineados
                rx.vstack(
                    rx.hstack(
                        rx.text("Childrens with Orders: ", width="150px"),
                        rx.input(
                            value=StatesHeads.nro_orders,
                            on_change=StatesHeads.set_nro_orders,
                            width="200px"
                        ),
                        width="100%"
                    ),
                    rx.hstack(
                        rx.text("Total Amount: ", width="150px"),
                        rx.input(
                            value=StatesHeads.total_orders,
                            on_change=StatesHeads.set_total_orders,
                            width="200px"
                        ),
                        width="100%"
                    ),
                    rx.hstack(
                        rx.text("Comissions: ", width="150px"),
                        rx.input(
                            value=StatesHeads.comissions,
                            on_change=StatesHeads.set_comissions,
                            width="200px"
                        ),
                        width="100%"
                    ),
                    spacing="3",
                    width="100%"
                ),
                rx.hstack(
                    rx.dialog.root(
                        rx.dialog.trigger(
                            rx.text(
                                "Actualizar Pdf Comisiones",
                                cursor="pointer",
                                _hover={"color": "blue"},
                                align="center",
                                on_click=[
                                    StatesHeads.set_user_id(id)
                                ]
                            )
                        ),
                        rx.dialog.content(
                            rx.dialog.title("Subir PDF"),
                            rx.dialog.description(
                                "Selecciona el archivo PDF para subir"),
                            rx.vstack(
                                rx.upload(
                                    rx.vstack(
                                        rx.button(
                                            "Seleccionar PDF",
                                            color="rgb(107,99,246)",
                                            bg="white",
                                            border="1px solid rgb(107,99,246)"),
                                        rx.text(
                                            "Arrastra y suelta el PDF aquí o haz clic para seleccionar"
                                        ),
                                        align="center"
                                    ),
                                    id="pdf_upload",
                                    max_files=1,
                                    accept={
                                        "application/pdf": [".pdf"]
                                    },
                                    on_drop=StatesHeads.handle_pdf_upload(
                                        rx.upload_files(upload_id="pdf_upload")
                                    ),
                                    border="1px dotted rgb(107,99,246)",
                                    padding="5em",
                                ),
                                rx.text(rx.selected_files("pdf_upload")),
                                rx.flex(
                                    rx.dialog.close(
                                        rx.button(
                                            "Cancelar",
                                            variant="soft",
                                            color_scheme="gray",
                                        ),
                                    ),
                                    rx.dialog.close(
                                        rx.button("Cerrar"),
                                    ),
                                    spacing="3",
                                    margin_top="16px",
                                    justify="end",
                                ),
                            )
                        )
                    ),
                    rx.switch(
                        checked=States.show_current_month,
                        on_change=States.toggle_time_period,
                    ),
                    rx.badge(
                        rx.cond(
                            States.show_current_month,
                            "Mes Actual",
                            "Últimos 30 días"

                        )
                    ),

                    width="100%",
                    justify="end",
                    spacing="3",
                    align_items="center",
                ),

                # Lista de Children
                rx.dialog.description(
                    rx.vstack(
                        rx.foreach(
                            States.children_orders_details,
                            lambda x: rx.hstack(
                                rx.text(
                                    f"{x.childrenname}:",
                                    font_weight="bold",
                                    color="var(--accent-11)"
                                ),
                                rx.text(
                                    x.ordersmonthdetails
                                ),
                                spacing="2",
                                align="start"
                            )
                        ),
                        spacing="3",
                        align="start"
                    )
                ),

                direction="column",
                spacing="3",
                align="start",
                width="100%"
            )
        ),
        rx.flex(
            rx.dialog.close(
                rx.button(
                    "Cancelar",
                    variant="soft",
                    color_scheme="gray",
                    margin_top="2em"
                ),
            ),
            rx.dialog.close(
                rx.button(
                    "Guardar",
                    on_click=StatesHeads.update_comissions_amount_orders(id),
                    margin_top="2em"
                ),
            ),
            spacing="3",
            justify="center",
        ),
        max_width="600px",
        size="3"
    )
```

## app12/components/modal_status_heads.py

```py
import reflex as rx
from ..backend.backend import States


def modal_status_heads() -> rx.Component:
    return rx.dialog.content(
        rx.dialog.title(
            "Children's Orders",
            text_align="center",  # Centra el texto
            width="100%"  # Asegura que tome todo el ancho disponible
        ),
        rx.dialog.description(
            rx.vstack(
                # Usando foreach para iterar sobre children_orders
                rx.foreach(
                    States.children_orders,
                    lambda x: rx.text(
                        f"{x.childrenname}: {x.ordersmonth}",
                        size="3"
                    )
                ),
                spacing="3",
                align="start"
            )
        ),
        rx.flex(
            rx.dialog.close(
                rx.button(
                    "Volver",
                    variant="soft",
                    color_scheme="gray",
                    margin_top="2em"
                ),
            ),
            spacing="3",
            justify="center",
        ),
        max_width="400px",
        size="4"
    )
```

## app12/components/modal_status.py

```py
import reflex as rx
from ..backend.backend import States


def modal_status() -> rx.Component:
    return rx.dialog.content(
        rx.dialog.title("Detalles de la Orden"),
        rx.dialog.description(
            rx.flex(
                rx.text(f"Referencia: {
                    States.selected_order.orderref}"),
                rx.hstack(rx.text("Tracking: "),
                          rx.cond(
                    States.selected_order.requisitionno,
                    rx.link(
                        States.selected_order.requisitionno,
                        href=States.selected_order.urltracking,
                        is_external=True
                    ),
                    rx.text("")
                )
                ),
                rx.text(f"Proveedor: {
                    States.selected_order.supplierno}"),
                rx.text(f"Deladd1: {
                    States.selected_order.deladd1}"),
                rx.text(f"Deladd2: {
                    States.selected_order.deladd2}"),
                rx.text(f"Comentarios: {
                    States.selected_order.comments}"),
                rx.text(f"Fecha: {States.selected_order.orddate}"),
                # rx.text(f"Estado: {States.selected_order.status}"),
                direction="column",
                spacing="3",
                align="start"
            )
        ),
        rx.flex(
            rx.dialog.close(
                rx.button(
                    "Cancelar",
                    variant="soft",
                    color_scheme="gray",
                    margin_top="2em"
                ),
            ),
            rx.dialog.close(
                rx.button(
                    "Marcar como Recibido",
                    on_click=States.handle_delivered(
                        States.selected_order.orderno),
                    margin_top="2em"
                ),
            ),
            spacing="3",
            justify="center",
        ),
        max_width="400px",
        size="4"
    )


def modal_status_info() -> rx.Component:
    return rx.dialog.content(
        rx.dialog.title("Detalles de la Orden"),
        rx.dialog.description(
            rx.flex(
                rx.text(f"Referencia: {
                    States.selected_order.orderref}"),
                rx.hstack(rx.text("Tracking: "),
                          rx.cond(
                    States.selected_order.requisitionno,
                    rx.link(
                        States.selected_order.requisitionno,
                        href=States.selected_order.urltracking,
                        is_external=True
                    ),
                    rx.text("")
                )
                ),
                rx.text(f"Proveedor: {
                    States.selected_order.supplierno}"),
                rx.text(f"Deladd1: {
                    States.selected_order.deladd1}"),
                rx.text(f"Deladd2: {
                    States.selected_order.deladd2}"),
                rx.text(f"Comentarios: {
                    States.selected_order.comments}"),
                rx.text(f"Fecha: {States.selected_order.orddate}"),
                # rx.text(f"Estado: {States.selected_order.status}"),
                direction="column",
                spacing="3",
                align="start"
            )
        ),
        rx.flex(
            rx.dialog.close(
                rx.button(
                    "Volver",
                    variant="soft",
                    color_scheme="gray",
                    margin_top="2em"
                ),
            ),
            spacing="3",
            justify="center",
        ),
        max_width="400px",
        size="4"
    )
```

## app12/components/navbar.py

```py
import reflex as rx
from rxconfig import config
from ..backend.backend import States


def navbar_link(text: str, url: str) -> rx.Component:
    return rx.link(
        rx.text(text, size="4", weight="medium"), href=url
    )


def navbar() -> rx.Component:
    return rx.box(
        rx.desktop_only(
            rx.hstack(
                rx.hstack(
                    rx.image(
                        src="/logo.jpg",
                        width="2.25em",
                        height="auto",
                        border_radius="25%",
                    ),
                    rx.heading(
                        "to-do-easy", size="7", weight="bold"
                    ),
                    align_items="center",
                ),
                rx.color_mode.button(),
                rx.hstack(
                    navbar_link("Home", "/"),
                    navbar_link("Mary Kay", "/heads_admin"),
                    navbar_link("Orders", "/control_heads"),
                    navbar_link("Tasks", "/tasks"),
                    navbar_link("Contact", "/#"),
                    spacing="5",
                ),
                rx.hstack(
                    rx.button(
                        "Sign Up",
                        size="3",
                        variant="outline",
                    ),
                    rx.button("Log In", size="3"),
                    spacing="4",
                    justify="end",
                ),
                justify="between",
                align_items="center",
                id="my-navbar-desktop"
            ),
        ),
        rx.mobile_and_tablet(
            rx.hstack(
                rx.hstack(
                    rx.image(
                        src="/logo.jpg",
                        width="2em",
                        height="auto",
                        border_radius="25%",
                    ),
                    rx.heading(
                        "to-do-easy", size="6", weight="bold"
                    ),
                    align_items="center",
                ),
                rx.color_mode.button(),
                rx.menu.root(
                    rx.menu.trigger(
                        rx.icon("menu", size=30)
                    ),
                    rx.menu.content(
                        rx.menu.item(rx.link("Home", href="/")),
                        rx.menu.item(
                            rx.link("Purchs Orders", href="purchs_page")),
                        rx.menu.item(
                            rx.link("Monthly Commissions", href="heads_admin")),
                        rx.menu.item(
                            rx.link("Heads Controls", href="control_heads")),
                        rx.menu.item(
                            rx.link("Stock Low Fee", href="lowstockfee")),
                        rx.menu.item(
                            rx.link("Tasks", href="tasks")),
                        rx.menu.separator(),
                        rx.menu.item(rx.link("Login", href="login")),
                        rx.menu.item(
                            "Sign Up", on_click=States.logout, cursor="pointer"),
                    ),
                    justify="end",
                ),
                justify="between",
                align_items="center",
            ),
        ),
        bg=rx.color("accent", 3),
        padding="1em",
        # position="fixed",
        # top="0px",
        # z_index="5",
        width="100%",
        id="my-container-navbar"
    )
```

## app12/components/table_lowstockfee.py

```py
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
```

## app12/components/ui_base_page.py

```py
import reflex as rx
from rxconfig import config
from .navbar import navbar


def base_page(child: rx.Component, *args, **kwargs) -> rx.Component:
    return rx.fragment(
        navbar(),
        child,
    )
```

## app12/__init__.py

```py
from .purchs_page import index
from .login import login_default
from .lowstockfee import index
from .amazon_index import index
from .applicable_fees_admin import index
from .index_admin import index
from .marykay_index import index
from .control_heads import index
from .heads_admin import index
from .tasks import index
```

## app12/amazon_index.py

```py
import reflex as rx
from rxconfig import config
from .backend.backend import States


class State(rx.State):
    """The app state."""

    ...


@rx.page(route="/amazon_index", title="Index_Amazon", on_load=States.check_auth)
def index() -> rx.Component:
    return rx.cond(
        States.auth_token != "",  # Check if token exists in LocalStorage
        # Authenticated view
        rx.flex(
            rx.vstack(
                rx.icon("home", margin="-70px 0px 0px -300px",
                        on_click=rx.redirect("/")),
                rx.button("Applicable Fees",
                          width='40vh',
                          height='7vh',
                          radius='full',
                          on_click=rx.redirect("/lowstockfee")),
                rx.button("Otros",
                          width='40vh',
                          height='7vh',
                          radius='full',
                          disable='True',
                          on_click=rx.toast("Próximamente...")),
                rx.button("Otros",
                          width='40vh',
                          height='7vh',
                          radius='full',
                          disable='True',
                          on_click=rx.toast("Próximamente...")),
                rx.button("Salir",
                          width='40vh',
                          height='7vh',
                          radius='full',
                          on_click=States.logout),
                rx.code("to-do-easy.com",
                        size="6",
                        color_scheme="indigo",
                        weight="bold"),
                border_width="2px",
                border_radius="1em",
                align='center',
                width='100vh',
                height="100vh",
                justify='center',
                max_width='400px',
                spacing="9",
                background_image="url('/drops-6392473_640.jpg')",
            ),
            justify='center'
        ),

    )


app = rx.App()
```

## app12/app12.py

```py
import reflex as rx
from rxconfig import config
from fastapi import FastAPI
from .backend.backend import States
from .components.ui_base_page import base_page
from .api.views.download_pdf_commission import get_supplier_doc

# Configurar la app con PWA
app = rx.App(
    head_components=[
        rx.el.link(rel="manifest", href="/manifest.json"),
        rx.script("""
            console.log('Script de Reflex ejecutándose');
            if ('serviceWorker' in navigator) {
                console.log('Service Worker soportado en este navegador');
                navigator.serviceWorker.register('/sw.js', { scope: '/' })
                    .then(reg => {
                        console.log('Service Worker registrado con éxito. Scope:', reg.scope);
                        if (reg.installing) {
                            console.log('Service Worker en instalación');
                        } else if (reg.waiting) {
                            console.log('Service Worker instalado, en espera');
                        } else if (reg.active) {
                            console.log('Service Worker activo');
                        }
                    })
                    .catch(err => {
                        console.error('Error al registrar Service Worker:', err.message);
                        console.error('Detalles del error:', err);
                    });
            } else {
                console.log('Service Worker no soportado en este navegador');
            }
        """)
    ]
)

# Clase de estado (simplificada)


class State(rx.State):
    """The app state."""
    auth_token: str = ""


@rx.page(route="/", title="Home", on_load=States.check_auth)
def index() -> rx.Component:
    return base_page(
        rx.cond(
            States.auth_token != "",
            rx.flex(
                rx.vstack(
                    rx.button("Gestion Mary Kay",
                              width='40vh',
                              height='7vh',
                              radius='full',
                              on_click=rx.redirect("/marykay_index")),
                    rx.button("Gestion Amazon",
                              width='40vh',
                              height='7vh',
                              radius='full',
                              disable='True',
                              on_click=rx.redirect("/amazon_index")),
                    rx.button("Tasks",
                              width='40vh',
                              height='7vh',
                              radius='full',
                              disable='True',
                              on_click=rx.redirect("/tasks")),
                    rx.button("Salir",
                              width='40vh',
                              height='7vh',
                              radius='full',
                              on_click=States.logout),
                    rx.code("to-do-easy.com",
                            size="6",
                            color_scheme="indigo",
                            weight="bold"),
                    border_width="2px",
                    border_radius="1em",
                    align='center',
                    width='100vh',
                    height="100vh",
                    justify='center',
                    max_width='400px',
                    spacing="9",
                    background_image="url('/drops-6392473_640.jpg')",
                ),
                justify='center'
            ),
        ),

    )


app.api.add_api_route(
    "/api/supplier-doc/{supplier_id:path}", get_supplier_doc, methods=["GET"])
```

## app12/applicable_fees_admin.py

```py
import reflex as rx
from rxconfig import config
from .backend.backend import States
from .components.main_table_lowstockfee_admin import table_products
from .components.table_lowstockfee import table_lowstockfee
from . components.ui_base_page import base_page


@rx.page(route="/applicable_fees_admin", title="Subject Fees", on_load=States.check_auth)
def index() -> rx.Component:
    return base_page(
        rx.cond(
            States.auth_token != "",
            rx.flex(
                rx.vstack(
                    rx.hstack(
                        rx.icon(
                            "home",
                            size=30,
                            color="white",
                            bg="black",
                            cursor="pointer",
                            on_click=rx.redirect("/")
                        ),
                        rx.heading(
                            'Applicable Fees', margin_left="2em", width="100%"), rx.color_mode.button(),
                        margin_top="2em",
                        margin_right="2em",
                        margin_left="1em",
                    ),
                    rx.hstack(
                        table_lowstockfee(States),
                        align="center",
                        justify="between",
                        width="100%",
                    ),

                    table_products(States.stocklowfee),
                ),
                direction='column',
                align='center',
                on_mount=States.get_prod_lowstockfee,
                id="my-flex-applicable-fees"
            )
        )
    )


app = rx.App()
```

## app12/control_heads.py

```py
import reflex as rx
from .backend.backend import States
from .components.main_table_heads import table_heads
from .components.filter_orders import filter_component
from .components.ui_base_page import base_page


@rx.page(route='/control_heads', title='Control Heads', on_load=States.check_auth)
def index() -> rx.Component:
    return base_page(
        rx.cond(
            States.auth_token != "",
            rx.flex(
                rx.vstack(
                    rx.hstack(
                        rx.heading(
                            'Heads Results',),
                        id="my-heading-in-control_heads",
                        width="100%",
                        justify="center"
                    ),
                    rx.hstack(
                        filter_component(
                            States.set_selected_location_heads),
                        align="center",
                        justify="between",
                        width="100%",
                    ),
                    table_heads(States.heads_suppliers)
                ),
                direction='column',
                align='center',
                on_mount=States.get_all_heads()
            ),
        )
    )


app = rx.App()
```

## app12/heads_admin.py

```py
import reflex as rx
from .backend.backend import States
from .components.main_table_heads_admin import table_heads
from .components.filter_orders import filter_component
from .components.ui_base_page import base_page
from .backend.heads_backend import StatesHeads
from .backend.backend import alert_dialog


@rx.page(route='/heads_admin', title='Heads Administrator', on_load=States.check_auth)
def index() -> rx.Component:
    return base_page(
        rx.cond(
            States.auth_token != "",
            rx.flex(
                rx.vstack(
                    rx.hstack(
                        rx.heading(
                            'Heads Results',),
                        id="my-heading-in-control_heads",
                        width="100%",
                        justify="center"
                    ),
                    rx.hstack(
                        filter_component(
                            States.set_selected_location_heads),
                        align="center",
                        justify="between",
                        width="100%",
                    ),
                    table_heads(States.heads_suppliers),
                    alert_dialog(StatesHeads)


                ),
                direction='column',
                align='center',
                on_mount=States.get_all_heads,
                id="my-flex-container"
            ),
        )
    )


app = rx.App()
```

## app12/index_admin.py

```py
import reflex as rx
from .backend.backend import States


class State(rx.State):
    """The app state."""

    ...


@rx.page(route="/index_admin", title="Administrador", on_load=States.check_auth)
def index() -> rx.Component:
    return rx.vstack(
        rx.heading("Indices"),
        rx.link(
            "Administration Low Stocks with Fee Products",
            href="/applicable_fees_admin",
            size="3",  # Controls text size (1-9)
            weight="bold",  # Text weight (light, regular, medium, bold)
            underline="hover",  # Underline behavior (auto, hover, always)
            color_scheme="blue",  # Color theme
            high_contrast=True,
            target="_blank"  # Increases color contrast
        ),
        align='center'
    )


app = rx.App()
```

## app12/login.py

```py
import reflex as rx
from .backend.backend import States


@rx.page(route='/login', title='login')
def login_default() -> rx.Component:
    return rx.flex(
        rx.vstack(
            rx.form.root(
                rx.vstack(
                    rx.form.field(
                        rx.flex(
                            rx.form.label("Email"),
                            rx.form.control(
                                rx.input(
                                    placeholder="Email",
                                    name="email",
                                    type="email",
                                    width="300px",  # Set desired width
                                    height="40px",  # Set desired height
                                ),
                                as_child=True,
                            ),
                            direction="column",
                            spacing="2",
                            aling='center',
                            justify='center'

                        ),
                        name="email",
                        align='center',
                        justify='center'
                    ),
                    rx.form.field(
                        rx.flex(
                            rx.form.label("Password"),
                            rx.form.control(
                                rx.input(
                                    placeholder="Password",
                                    name="password",
                                    type="password",
                                    width="300px",  # Set desired width
                                    height="40px",
                                ),
                                as_child=True,
                            ),
                            direction="column",
                            spacing="2",
                            aling='center'
                        ),
                        name="password",
                        align='center'
                    ),
                    rx.form.submit(
                        rx.button("Login"),
                        as_child=True,
                    ),
                    rx.text(States.error_message, color="red"),
                    align='center',
                    justify='center',
                    max_width='400px',
                ),
                on_submit=States.handle_submit,
                justify='center',
                aling='center'
            ),
            border_width="2px",
            border_radius="1em",
            align='center',
            width='100vh',
            height="100vh",
            justify='center',
            max_width='400px',
            spacing="9",
            background_image="url('/drops-6392473_640.jpg')",
        ),
        justify='center'
    )


app = rx.App()
```

## app12/lowstockfee.py

```py
import reflex as rx
from .backend.backend import States
from .components.main_table_lowstockfee import table_products
from .components.filter_orders import filter_component
from .components.ui_base_page import base_page


@rx.page(route='/lowstockfee', title='LowStock', on_load=States.check_auth)
def index() -> rx.Component:
    return base_page(
        rx.cond(
            States.auth_token != "",
            rx.flex(
                rx.vstack(
                    rx.hstack(
                        rx.heading(
                            'Applicable Fees'
                        ),
                        margin_top="1em",
                        width="100%",
                        justify="center"
                    ),
                    table_products(States.stocklowfee)
                ),
                direction='column',
                align='center',
                on_mount=States.get_prod_lowstockfee,
            ),
        )
    )


app = rx.App()
```

## app12/marykay_index.py

```py
import reflex as rx
from rxconfig import config
from .backend.backend import States
from .components.ui_base_page import base_page


class State(rx.State):
    """The app state."""

    ...


@rx.page(route="/marykay_index", title="Index_MaryKay", on_load=States.check_auth)
def index() -> rx.Component:
    return base_page(
        rx.cond(
            States.auth_token != "",  # Check if token exists in LocalStorage
            # Authenticated view
            rx.flex(
                rx.vstack(
                    rx.button("Purch Orders",
                              width='40vh',
                              height='7vh',
                              radius='full',
                              on_click=rx.redirect("/purchs_page")),
                    rx.button("Heads Controls",
                              width='40vh',
                              height='7vh',
                              radius='full',
                              disable='True',
                              on_click=rx.redirect("/control_heads")),
                    rx.button("Monthly Commissions",
                              width='40vh',
                              height='7vh',
                              radius='full',
                              disable='True',
                              on_click=rx.redirect("/heads_admin")),
                    rx.button("Salir",
                              width='40vh',
                              height='7vh',
                              radius='full',
                              on_click=States.logout),
                    rx.code("to-do-easy.com",
                            size="6",
                            color_scheme="indigo",
                            weight="bold"),
                    border_width="2px",
                    border_radius="1em",
                    align='center',
                    width='100vh',
                    height="100vh",
                    justify='center',
                    max_width='400px',
                    spacing="9",
                    background_image="url('/drops-6392473_640.jpg')",
                ),
                justify='center'
            ),

        )
    )


app = rx.App()
```

## app12/purchs_page.py

```py
import reflex as rx
from .backend.backend import States
from .components.main_table import table_purchs
from .components.filter_orders import filter_component
from .components.ui_base_page import base_page


@rx.page(route='/purchs_page', title='purch_page', on_load=States.check_auth)
def index() -> rx.Component:
    return base_page(

        rx.cond(
            States.auth_token != "",
            rx.flex(
                rx.vstack(
                    rx.hstack(
                        rx.heading(
                            'Ordenes Mary Kay', align='center')
                    ),
                    rx.hstack(
                        filter_component(
                            States.set_selected_location),
                        align="center",
                        justify="between",
                        width="100%",
                    ),
                    table_purchs(States.purchorders)
                ),
                direction='column',
                align='center',
                on_mount=States.get_all_purchs(),
            ),
        )
    )


app = rx.App()
```

## app12/tasks.py

```py
import reflex as rx
from .backend.backend import States
from .components.ui_base_page import base_page


@rx.page(route='/tasks', title='Tareas', on_load=States.check_auth)
def index() -> rx.Component:
    return base_page(
        rx.cond(
            States.auth_token != "",
            rx.flex(
                rx.vstack(
                    # Encabezado
                    rx.hstack(
                        rx.heading("Pending Tasks", size="4"),
                        width="100%",
                        justify="center",
                        margin="0",
                        padding="0",
                    ),
                    rx.desktop_only(
                        rx.container(
                            rx.foreach(
                                States.formatted_tasks,
                                lambda task, index: rx.vstack(
                                    rx.text(
                                        task["description"],
                                        color=rx.cond(
                                            task["status"] == "Pending",
                                            "blue",
                                            "green"
                                        ),
                                    ),
                                    rx.text(
                                        f"Created: {task['created_at']}",
                                        size="1",
                                    ),
                                    rx.hstack(
                                        rx.text(
                                            f"Modify: {task['updated_at']}",
                                            size="1",
                                        ),
                                        rx.cond(
                                            task["status"] == "Completed",
                                            rx.badge(
                                                "Terminado",
                                                color_scheme="green",
                                                variant="soft",
                                                size="3",
                                                cursor="default",
                                            ),
                                            rx.alert_dialog.root(
                                                rx.alert_dialog.trigger(
                                                    rx.badge(
                                                        "Pendiente",
                                                        color_scheme="red",
                                                        variant="soft",
                                                        size="3",
                                                        cursor="pointer"
                                                    ),
                                                ),
                                                rx.alert_dialog.content(
                                                    rx.alert_dialog.title(
                                                        "Confirmar Acción"),
                                                    rx.alert_dialog.description(
                                                        "¿Está seguro de marcar esta tarea como terminada?"
                                                    ),
                                                    rx.flex(
                                                        rx.alert_dialog.cancel(
                                                            rx.button("Cancelar", variant="soft",
                                                                      color_scheme="gray"),
                                                        ),
                                                        rx.alert_dialog.action(
                                                            rx.button(
                                                                "Confirmar",
                                                                color_scheme="red",
                                                                on_click=States.toggle_task_status(
                                                                    task["id"]),
                                                            ),
                                                        ),
                                                        spacing="3",
                                                        justify="end",
                                                    ),
                                                ),
                                            ),
                                        ),
                                        width="100%",
                                        justify="between",
                                        align="center",
                                        spacing="0",
                                    ),
                                    spacing="2",
                                    padding="10px 0",
                                    width="80%",
                                    margin="0",
                                    border_bottom="1px solid #eee",
                                    key=f"task-{index}-desktop",
                                ),
                            ),
                            size="3",
                            center_content=True,
                            width="100%"
                        ),
                        width="100%",
                        justify_content="center",
                        align_items="center"
                    ),

                    # Vista para tablet
                    rx.tablet_only(
                        rx.container(
                            rx.foreach(
                                States.formatted_tasks,
                                lambda task, index: rx.vstack(
                                    rx.text(
                                        task["description"],
                                        color=rx.cond(
                                            task["status"] == "Pending",
                                            "blue",
                                            "green"
                                        ),
                                    ),
                                    rx.hstack(
                                        rx.text(
                                            rx.cond(
                                                task["updated_at"] != "Sin actualizar",
                                                f"Actualizado: {task['updated_at']}",
                                                "Sin actualizar"
                                            ),
                                            size="1"
                                        ),
                                        rx.cond(
                                            task["status"] == "Completed",
                                            rx.badge(
                                                "Terminado",
                                                color_scheme="green",
                                                variant="soft",
                                                size="2",
                                                on_click=lambda: States.toggle_task_status(
                                                    task["id"]),
                                                cursor="pointer"
                                            ),
                                            rx.badge(
                                                "Pendiente",
                                                color_scheme="red",
                                                variant="soft",
                                                size="2",
                                                on_click=lambda: States.toggle_task_status(
                                                    task["id"]),
                                                cursor="pointer"
                                            ),
                                        ),
                                        width="100%",
                                        justify="between",
                                        spacing="1",
                                    ),
                                    spacing="1",
                                    padding="5px 0",
                                    width="100%",
                                    margin="0",
                                    border_bottom="1px solid #eee",
                                    key=f"task-{index}-tablet",
                                ),
                            ),
                            size="1",
                            center_content=False,
                        ),
                    ),

                    rx.mobile_only(
                        rx.vstack(
                            # Iterar sobre las tareas formateadas
                            rx.foreach(
                                States.formatted_tasks,
                                lambda task, index: rx.vstack(
                                    # Descripción de la tarea
                                    rx.text(
                                        task["description"],
                                        color=rx.cond(
                                            task["status"] == "Pending",
                                            "red",
                                            "green"
                                        ),
                                        width="100%",
                                    ),
                                    # Fecha de creación
                                    rx.text(
                                        f"Created: {task['created_at']}",
                                        size="1",
                                        width="100%",
                                    ),
                                    # Fecha de actualización con badge en la misma línea
                                    rx.hstack(
                                        rx.text(
                                            f"Modify: {task['updated_at']}",
                                            size="1",
                                        ),
                                        rx.spacer(),  # Empuja el badge al borde derecho
                                        rx.cond(
                                            task["status"] == "Completed",
                                            rx.badge(
                                                "Terminado",
                                                color_scheme="green",
                                                variant="soft",
                                                size="3",
                                                cursor="default",  # No clicable
                                            ),
                                            rx.alert_dialog.root(
                                                rx.alert_dialog.trigger(
                                                    rx.badge(
                                                        "Pendiente",
                                                        color_scheme="red",
                                                        variant="soft",
                                                        size="3",
                                                        cursor="pointer"
                                                    ),
                                                ),
                                                rx.alert_dialog.content(
                                                    rx.alert_dialog.title(
                                                        "Confirmar Acción"),
                                                    rx.alert_dialog.description(
                                                        "¿Está seguro de marcar esta tarea como terminada?",
                                                    ),
                                                    rx.flex(
                                                        rx.alert_dialog.cancel(
                                                            rx.button("Cancelar", variant="soft",
                                                                      color_scheme="gray"),
                                                        ),
                                                        rx.alert_dialog.action(
                                                            rx.button(
                                                                "Confirmar",
                                                                color_scheme="red",
                                                                on_click=States.toggle_task_status(
                                                                    task["id"]),
                                                            ),
                                                        ),
                                                        spacing="3",
                                                        justify="end",
                                                    ),
                                                ),
                                            ),
                                        ),
                                        width="100%",  # El hstack ocupa todo el ancho
                                        justify="between",  # Justificar los elementos a los extremos
                                        align="center",  # Alinear verticalmente el texto y el badge
                                    ),
                                    # Diálogo de confirmación (agregar fuera del rx.foreach, dentro del rx.vstack principal)

                                    spacing="0",
                                    padding="5px 0",
                                    width="100%",
                                    margin="0",
                                    border_bottom="1px solid #eee",
                                    key=f"task-{index}-mobile",
                                ),
                            ),
                            # Botón flotante para abrir el modal
                            rx.button(
                                rx.icon(
                                    "plus",
                                    color="white",
                                    size=26
                                ),
                                position="fixed",
                                bottom="20px",
                                left="50%",
                                transform="translateX(-50%)",
                                on_click=lambda: States.toggle_dialog(
                                    True),  # Abre el modal
                                style={
                                    "background_color": "#0047AB",
                                    "opacity": "1",
                                    "border_radius": "50%",
                                    "width": "50px",
                                    "height": "50px",
                                    "box_shadow": "0 10px 15px -3px rgba(0, 0, 0, 0.1)",
                                    "_hover": {"background_color": "#003380"}
                                },
                            ),
                            # Fondo oscuro para el modal
                            rx.cond(
                                States.dialog_open,
                                rx.box(
                                    style={
                                        "position": "fixed",
                                        "top": "0",
                                        "left": "0",
                                        "width": "100%",
                                        "height": "100%",
                                        "backgroundColor": "rgba(0, 0, 0, 0.5)",
                                        "zIndex": "998",
                                    },
                                    on_click=lambda: States.toggle_dialog(
                                        False),  # Cierra el modal
                                ),
                            ),
                            # Modal personalizado
                            rx.cond(
                                States.dialog_open,
                                rx.box(
                                    rx.vstack(
                                        rx.text_area(
                                            placeholder="Nueva tarea...",
                                            value=States.new_task_description,
                                            on_change=States.set_new_task_description,
                                            rows='4',
                                            resize="none",
                                            width="100%",
                                            height="auto",
                                            font_size="16px",
                                            padding="10px",
                                            margin="10px 0 0 0",
                                        ),
                                        rx.hstack(
                                            rx.button(
                                                "Agregar Tarea",
                                                on_click=[
                                                    States.create_task,
                                                    lambda: States.toggle_dialog(
                                                        False),
                                                ],
                                                disabled=States.new_task_description == "",
                                                style={
                                                    "marginTop": "10px",
                                                    "padding": "10px 20px",
                                                    "backgroundColor": "#0047AB",
                                                    "color": "white",
                                                    "borderRadius": "5px",
                                                    "cursor": "pointer",
                                                    "_hover": {"backgroundColor": "#003380"}
                                                }
                                            ),
                                            rx.button(
                                                "Abandonar",
                                                on_click=[
                                                    lambda: States.toggle_dialog(
                                                        False),
                                                    lambda: States.set_new_task_description(
                                                        "")
                                                ],
                                                style={
                                                    "marginTop": "10px",
                                                    "padding": "10px 20px",
                                                    "backgroundColor": "#808080",
                                                    "color": "white",
                                                    "borderRadius": "5px",
                                                    "cursor": "pointer",
                                                    "_hover": {"backgroundColor": "#5a5a5a"}
                                                }
                                            ),
                                            spacing="4",
                                            justify="center",
                                            width="100%",
                                        ),
                                        spacing="4",
                                    ),
                                    style={
                                        "position": "fixed",
                                        "left": "50%",
                                        "transform": "translateX(-50%)",
                                        "width": "90%",
                                        "maxWidth": "500px",
                                        "height": "auto",
                                        "backgroundColor": "white",
                                        "padding": "10px",
                                        "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.1)",
                                        "borderRadius": "8px",
                                        "zIndex": "999",
                                        "animation": rx.cond(
                                            States.dialog_open,
                                            "slideUp 0.3s ease-out forwards",
                                            "slideDown 0.3s ease-out forwards"
                                        ),
                                        "@keyframes slideUp": {
                                            "from": {"top": "100%"},
                                            "to": {"top": "20%"}
                                        },
                                        "@keyframes slideDown": {
                                            "from": {"top": "20%"},
                                            "to": {"top": "100%"}
                                        },
                                    },
                                ),
                            ),
                            width="100%",
                            position="relative",
                            padding="0",
                            margin="0",
                        ),
                        width="100%",
                        padding="0",  # Sin padding del contenedor
                        margin="0",   # Sin margen del contenedor
                    ),

                    width="100%",
                    max_width="100%",
                    margin="0",
                    padding="0 5px",
                ),
                direction="column",
                align="stretch",
                width="100%",
                max_width="100%",
                margin="0",
                padding="0 5px",
                on_mount=States.load_tasks,
                id="tasks-container",
            ),
        )
    )


app = rx.App()
```

## assets/drops-6392473_640.jpg

```jpg
���� JFIF      ��@ICC_PROFILE   0ADBE  mntrRGB XYZ �        acspAPPL    none                  ��     �-ADBE                                               
cprt   �   2desc  0   kwtpt  �   bkpt  �   rTRC  �   gTRC  �   bTRC  �   rXYZ  �   gXYZ     bXYZ     text    Copyright 1999 Adobe Systems Incorporated   desc       Adobe RGB (1998)                                                                                XYZ       �Q    �XYZ                 curv       3  curv       3  curv       3  XYZ       �  O�  �XYZ       4�  �,  �XYZ       &1  /  ���� C 	

			

		
�� C	�� ��" ��              �� D  !1AQa"q2��#BR�3r��$b���Cc�%Ds������            �� <    !1A"Qaq��2����#��$RBr�34��Cb��   ? ��I��W�E�{Qq�����`�����U�I�aK�h��%�z0CR��U���|Ը���LP*�cl#��*Jg�$ǽ;z��+�� �l�&3��Afozs0�~i�x�˃��[5� �(�o�^�B%�J�x�I�3��.}��33����Z��A�zC!�$w�I0j����ҩ�A7'8�>9�ɨX��S��w���l����ߚ��V�oQs��ӽe���8�9���G��in��C.i�������W�4@ �8��v��eqP�q�2H1��!ii�d�'ހǚW��(;�=��T�&��{R�2k�p㊕j��p����M/�ށsq��ނ�ԥ���jYza~hbM��Dh��e��M-��WJ�Ng�8�/Bf�z��U�0����34��9V%/HZ�ǚnj�`O�sR#�`x�e�v��*�J�=JkK�5y@�kJǌ�d�M�l�(L�i$ӊ�M��n����n�e����SU���&��)���
 ji>E47�=Sp��\@ܠ>M"��"���|�!F�{#x"���&?��9���֐S���B-Mg4愕��Dg�����i����Z0Nv���T�4�x�H����l�R�W�Aw�;'��p��<���f��NF-�]�-���X�����sF�*�O( �W'�i��t��({���i"sܚcWo�[w����As�Of�@���JkB?8�3v)���Kg�.ր7�4��������k�-_\��DS��,EJ��K�mvȱ����4 �ilE)v����H/.�9gc۵E�W;���[�A�L��qQ�7 �\\���ɹ�i�:VO*�O��qO	�ɨ�> �C)�Q���m�⫞�4k�f�����i���'c���@�P�Q�5$ȡq�B��k�m;Nh���ny�GbOj��X�$��(�R?��ET`y�$�5d�V�4��L,��4 }�Ѩ#���q�J	c�S��qu�j��R#EۓQ.�M� �Q.n���$��ˏ4�\q���Y��T�x��t��n�Ź����$�x�B���U!k��e�&�g���cE����JFmG�bZ���T�#�ɡ��<��V�2F�R"y>)���9��C-�s��B/�¢6�[書�wy�&�� ��L݊B��n�W��G���^�)��1�
@�H��+74�~q\��MQMa	ũqC-�M�R`�����K��9�Ce&�8�i�����8=�$�kE���Ԕ<`T$<���r�'�HWu#��S�@&�2n'#��n�GF�C�A�,��Ms�̅�)DR�׵�d�l�3q�M	�A+��0xjG*���LT�� Ka.;)j�w�+co���ь�o�8"|n(s�	�D���4Ie���q����Z,�[�Oj������@�4,y3<lL*<�9�3]������|G9C�Z��Ƞ�]9$��'��npz�%��py���9�K�y��i�h�4���;��i̇�h/�K(�ci	�\NhlhBqaCg��R���_k__�B�y��-�,�T{�� ����"��r�K�j��=�{�i���/�%��Pf�|���`�d�&yɢ !.%B����2>)�#�QJƔ���(��]H��4��qC`O~ԻsAJjHC���BA椖�[��f�n�}p����s���S"\.j����f�N�6qN2�<�)}`F3U����e��F��S. ��#��
ۺ*�(�����!���!�&N1C2Tf�ɤY��5T�љ�A`�N,1Ls�jR �M��9�+ *O�ߊ�qWH��dYߎ*�v����Sd��O��5�����N���r�RQ�8�DVP8�I�x<"�qAgɥg4"I�U0Z niY����g�M��;qB-�5�KsLl�Li�M�Rd�вM85U&vD�=�5̼`Wd��'�w�ږ}N�I�q����昰���N .EV�4M H��Cy�9�G3���(	Z�6�J,q�\H&�%f�5-Qi	X懟c\�=��j�2F�9�� ��DG��I$�8��K;�~�D� �Y�����lN3�[�-��r��⹥8�⠭����2;�&������E �"�ֈ��Ȩ��l��1���JH���ڞCc$�r���j,�*�TA9{�v�f��\��8�]Y����|��F�$OG�Ms��V���	O�~8���7N�<���Ll'cN�8�Hx欨�R`����&��T�A�*B���j��Hw(�ܳrƫ圚|���Gd��S⍠(w2�Af�4y4�!�F)d_+Xp�DP�e 
8��@�4B�e�v��r�B��M0`j��4�E��9���jF@����{� R���QX�ҫP���R"��Q/��ԈSs|�6	⠛��Bs)9
k���_ �T���D�&���C���,�0MG
E�e )$9�p;�Vq��%�E��rh�Ī)��NC��Y�V�����4�� d�T�yNX�FJP���5E�x5~�l-�@����g� �6PL=\)�L�%A�X�s��)E�H6�"Ӭ�Z��RG���Sg�;��ӡ�T D(+v��x�r����1L1��/?��a�TE<����2�u
+�����E<f��V˟�jgڍ&�<�Ayװ5}���G��钷��s�4��M@��ݠ�9?�O�K0�)	�OV��]���US�F���\�*���0$6MW	l��rl������N��x��=B�2̶Fh/u��X���g�@4���Ech6������v�9�
IH�EQ��RyaMj
��sD�|��ӥ&M)<R)���(�i?{�吞�,҇�UjRQ�<��g��ME����q�*9�"�-�D��l�Um;n䚲�{梵�N@泐I]x�Ƅ�y[�j�+�B��*H8�۰H���ـ�MY0O46o���/J�.<P��$aN>i���)]@�WeuW�z�!Ϛ�'����G�Գkk�u�є��Q�)���R2mXF�C�Nc�)nir�O=�RM��g�0W�4Z�H�[��R4��GE�)bƑ	� �W]�V�GA��2C�O��G���Kn�4�3u4�Mf� j��w4%'�)��ކNj��J94Px�ARI�1��T>ҳ{�� ��n�OSD��Ϸ#q$�<��s�
6���4�ݚ���(Dɫ���Z#٪&����D�H9-i��� �ӎ;�rDy�nd
_�+@��	��p*+\n�M+�ǚ ;@�J�@D�)&n(i��	���p3W��jt15��ŕ����/n�4���*Sh0��ϵJ^��I�|�R�� ,���Q|�9�t�&�g�� �  �J�.ML�aE����L��[8?�ZYE��>*9��SF�Y�=r7*<�J>iH-H_���/�1�P]�0*��WP����kmM�+5ŌH�}G_vk�<�s3*Y�X�4��,-!�w�C���m��&�tٙ�ݜ~j*�?�խ����j G+^D���h����V�>сM-B��sG��c'�A3l�%�� 9<U����#�{�U��mQ�j�1��G�u0��3R�V�|"|�p�u���3B���9�ޘ�{1���[Y=�ڂ�N���6SySmܑ�jG"�[8�S-��	���4� �jR��ދK��d�8�"���hs�J
ĲMP^�U������qvA�O5�]��A`��W�eO������[$��2�h2H�v��1�*�@�f��Ҝ�1M/��x�J��ۀ�ф�i���r��P���%:1�YS	�M�y��8�-R�Ӷ�űBi9��+0"��*����&���Q��oz|��3�PJ=���˳m��t_�2�\��a��v�l��kZ�SU�
���9 !y<�$��4�+ ��ԘZ�N)���i��|��uZ���h���0�×�*�d,o�@i���#s�L1sNor)@���A�1Q�8U&�
z��<U�1����lf��i�.����Z�"2sWRz`sP.Z,rh�`$3-�;�\ge8���)�I
����}����8���@��G`Oz`��Eʿ���6荔�F2y�HK7l
_Pc��3ފ�[XA���Q����4�9�
Qe<�s+�P|'5�=�T~��H{c��F$��P��F�C�]�I���[�f�_�U�h��-ږC�NN�;�W�R�*�EE��qI�a�HU��{�2�K�hک[�̼�Tˋ��,8��w;�|�ۗhj{f R�&�����(f�۱o�ޖa��M(��9���DzRH�ns�@<NhӸTV|���E�x�}��jlZ��bEc�"��{�p�%J�߳���ȣ��+{Uo��=�Ds�+�[K��).ˏ���<y�\�.����k}SZ�JK�������ޠ(X-'nN�,��Ǝ�g�;��Sw8Rm�؞[5Z�O�Sa��� (�

�L�4	�7�@y�1ޘ�!�"�5Pot����(ʫ��r#��	#��T.@b�����S��+���U�p��ʬ2��Үq�5�pƧh�inV7�6�"�h)��73�$W�G4SqT�hh��d������S4C�����jr���3�RxQFH�A���+Ƞ�t�T�4���e�A�Kv�p5�fpv��mw���v��1bS��ݑ�4�?���B�E{Q�chs�'�����$n��6y���6��*�d��,Q2��`�lQ	�����!��уK�����G��;���	e���I��+��h�@��9�4D\�R3�Y�����W,� Ч� T�k�����5�\�6'u q������qޚ�{�I�0�GeM�[渞99�o9��O�n��;�*�TWFT7�2\�=�"S�AGdm󍕆���|��W��j;z���5e��G�.�OU��!�&�#j]�?ˊZ�H?�>�H����*3}��E����E��a!\�i4`��}��`�FYF1V�^ı���mYXߚ{���b��2Cw�Z�k�-����v�����\�勜f�t�ˠ�X=��̀m���R��#�j�.���YT�M6�ÓDK������Qw35Zep���O�� ��Vӡ<�\���,`l�Y�䊞����T�F?4�Bz&���G��Ǔ�cy ��@φ�{T�
�mn���#(Z\qI02Zx����y����hﯬQ$l�Z#p`�s����7Y���@5��ՠF!MAԵY.�g,�z���v���l�>U����&gu��R�����^�O��M;|����B��~(�x��K��B��c�O_�\g�:��,CK�V�h�I��[U�v��
+i��%��pުr��ϫ S�֐�R�>9��T+�b���j�p<�Rj����	���G[.�;]���S�x���W���)ݏ �ezl�$���H��&�M�s�|Tԅ�\�*��N�#Y�Q�B��+��03��e� H�C���V��ƥ�H �y��_<`����9�\�&	o�^��@?z��8\�j�؇\��U�����W%�|�9�*2�-
�,@v�a튢��=S�ϵY��7R�i��򤐠d�G��8��F��uުd�G|�'�V��9�[�=L��X�sQl�l}��M>��*RmoH�|#�4��r n>*��y�m�� �"�Ƌ*�-[���Z!��>jLz#N�<j�Դ�N�]��f#�OP��a>s'?���U��+��SJ��*�F]ϧ�W^6����Ũ��^LGԏzth�1�
�'������<��l՝����e}����s � Z 4��� �l����@tsB���t��\�D����Q@�'b���"�ڴ�b���o��&��t���qGy�ӊ��3>7q���H2��*Jh0J���V���ks�T����fӠ�pj�r��
��Ŝ���	��7jꇓ�iD���4`�P��aFy�~��Ϛ�q��pJ��Sb���4�b0FqH����"��2F�p�����0Y\	���"2��B)F8;v�\��l~(l¸"�:��Fjcv��)�ڀRw�F��ۿ���U�a�'����Gf$�ޥ6����H��������tl�B�I5em���4�q�*�#�W�]F���b�0+6d�3h�)����0NXP5�c���VVK��lol�
Dҵ���a`�4z�4��3 �㏚��V�&�AT��v��W�j���9"��`��౻-�:�H�RO�i�1��9�f, �\d�����5l{�<�%����U�� ��EK��@1R]��q�@e^+�<��q�3�`p*Aa���$�g�( ����I%cއ��ОC�j]�k"��Ћ&���ʏ��I&sR�a�>A�V�rH�U�D��H��(_(O&�cVfڣ'ڬcӟn�#'���&L#�C��-ګ�m���Wf�v��� K���ZK�FKbY#
���0�ѐ���KO[�nb�ֺ����"K�_��r�7�5�Km��� b�s�$)�ǰ���ÕB �:�>����B���p��+��|�y��Y	nf �<ѿA�67dԸ�Œn'�-�s͞�H�ۥ��bL`)�]y'z�� $c.OaS գ`�k��O�)��c�a�Ri�@��Vڇ�Y^k����c�-Q���i3�6�*Ղ̗���ef$2�4�rrH�VbS%M���8���S! M$�G�*�'�4��[��j� YM�f��I�zn�'53J�BL��� j�����!/�	r[	��+V!s�j��E�K9����E(�^��W��c��d��H�>-��|����=a�\�\��j��f#ڥ�7Z<�4 �^�i�����{��HT�*1X�z�V,Dv�xɨ��7�����O��J�"A_�6�,9ɣ���T�=��j�$y�<x�^��d���,6c!Rv��9�8��@2X%x�҃�X��
yd�� gޒ9jmң�-���v�t�L��w2�;�Y�[��L�'y����.�in)��57�Kpy٫�������>����^�w�l-$&/�U1iP�U �}G�遁DƖ��R��nT�����Y��e��+旜�S��<ե�����P����/�Rg�I��i�9��X:�2��6N�c���}�c�2�M����4\$\�P^�Q&s�欬_�4��0����q�[��Uξ�k�� *������Tk�:���ɪS��� b���� J׏�z{�r�e�KwdaPe�KI�7b��Ӓ�}���:r����V�zwNf���.5�hԐğj�m�~��x�B��c�-Sl:m�q#R� �J�#Å�͕���֌�S�PE�/A��9؟�U�v������� ��#=�@iG{�ׁF�G5
)K7=���_ȦB�B�J|,dM���Ҝ(�p��bM'1s��(sjЂQ�O�Ck̓+�'�cd�1��\�;E/��C:� �2����p�Z4�"�G���Kb�Z�Az�9 ���ݮ���R��4��٦�J ��39]���M݃�R0�XX��0y��l�1a\B�~*����qP���xlX����l�D����D��6� F�C�NO�UM�B쪛���g,�j$�]60Mbt����ӳ���Ooo� S�H�a��]Awq'sW:-�� �N��p�SB�&��S���^)������i�����[R$���Fi���4"s愛Mc@e]�$��Ȉc&��M�@�7 �E:��phq��X�Sw��UY�(� �2'T`x��|��ň�U+;�8�P��f'��i�,㇟2|ڬ�7�}�ވ��ѮKd�����|��z|�s@��S�b�$�F�1�UF���p�'4�e�M�������s��V�PDl�	y3��?5h����<ԭ��� ��ѻʪ�$�^�e����]��q�S�d����6S"��)�ݧ!Z�F7�l����:|��OcUO#+m@5gq}+�P�5T �I7����JZ
Վ״Q���)���p�d��9���"��A]���K�+F��=:�7`��'���:{"��j4����J���P��V�4M���c���Pl�z"6��E��h�5ϵ*�Xq�L��E��`8��6�m�BW���}]� �U&�������h1"�Ov;n���hT�z!�E5���FeW�;�����?Y���J�u���El���X	W�*�miمA�M�d�~*e�����qr�2��h'VfB"��7F|G��x-� 
�s�B����Smf��l��Q#����5j�(�(d�u����J��FMSh�����]�}��y�"����RF�
�i�3R�J�f��ǎER�85�J�}M�rq�V1��x���ehP�֫����"���o�����&����d���m��I�g ��'3S�/iǠ
V�.8���4�E�����������v���
��Dr]N8���i�9-���i6�S��H��9X�9,D��z���x��A��\��ޅ��d��'�`�_z���,��e�<� �ɠ_�ެL��
#�\�q��pc]Iu��+6bF*��Y���$�O�d��3^��>��A�)�1���3n��3X��t�����2lO<���*A]���>	<S�H��n�*�������5���W&�g#`��(4�81&�ޜXc5\�;nR��N�5����Fi���3�\�j�~��n���8V3��K-�1�A&y���3�/�@��m��4��f�Z��w���kL���X��4�#ک�"�j�g�&2M\����i\��@b*�1Y�U��;��}N� X��K����]Jp�4��Η�䁾yWQKq&V0O�L�������5�$sƛ��~jݛ"��P�m��'�B���ka�dԽ��+P�X�Yv�eq��!���1�<՞�iԠI��ѱ��$���h���*���-�)S�F;�^�7Kڭ���9\�7���17ŧ{\��y-kH!M��-D[� �w5S�Xi�YA��է�3<�8����fr�H��ڗ,��-u0��|�G>���i�	�5X�R>�U[�א�8+�犋a�^,��v�k͝��DL,g����p��S#����V�\�3ZZ�Ѳ���F��M�E���e+�4	���ݨ�l��y�q���zj��渌
`b�9�쉞����F<f�*�	hE�hm!�5#L�.n�6<V�p��^x
9I[,�6�|Tye�6A��P�I��� *��atg�9<���DpW�$2���@��D��9�JO�0I=��j6r��l�v�Ǌ��<FORLs沆Ӵ�2���4눗�t=�Ty���)�>��X[�S�O�U�j:o�`=�ct��ő� ��*6�E���(�n8��=Ig�p*��SX�_��Ց�k_Cu׉��-O�F�\	���ڄk�G�U$���b�$�����C��Hnmv�Q��I6*@�4%��#��JN��,r��{�ݪf�q�ҙ5wr �i6����½�>����Qs��y_Vu!���ݹs�48���O�M{h�X��O��t���:,S:S�*�S�y
��T�{ɁT'w.��s�t�$��k�����zx�{�������ۻ��	�9�F�ҡ��4�R�L<d1���'����1G4�� i�8����+�n>٩o�0�iW��E��W�G�u&���~��Thg�(Pýc5޻��-�)�i�3�����/����]��V>��1�yC��_ٙ"$v�ܮ,˖<V�o��|����]ŗ��Y��f��'9m�)��R{洰�ks��N1�VkPЮNE��>�a����'8�Ї<l�8��(})W��m��l���5����[ee�Y�>�in�Y\�f��M�p��E�B��_P�����΢9TP�37ݚ9y$����km	�9�G��gF���#����$9M�$�8]uK�*�4ǒ|+�Z���H�<Vn-mM�B�k�(>eՈ������a���ѣ�9��a����%��+;��E����b'��`T{��ұ1���c��-w���V�=�֓�պ͏�)�8Nqi����
�7w�?4)w�%I�TvF�]��B�1�kK�P��dѷH��>�` P%��VC ]#^���;���B�uq$*O94�{r�^�+;`T�B�g�����~*�;��*R�n=��HIcv3��V���Yd?h�7Z��a��qk�r_@e��\{�����r^���uR� ���N�:;y����4�;`�x�g��.A���7m��l9��+l��Q��=7D��y�7�4=�N�za��$�v��#o���DEr�#�P�m�����#Q��A����Q�$=���QLk���;�(�����2�R*�� &��MkC���7��ʣ���D�����(�,����5���u�� ���1��(�qL�B�Z�{��oE��PZF�,O�D����$���U�##AƭG>�#N�KIĪ�Z�gP�h� #�A�m�$ai�u�}@���ӖS�����@�E����������K1��E7D+��)SK3������n;=u˭f�5M��	��Ir$�;��X�������-�5p�b����ׁ�]<�B�<�RP�v��@a6i�z�H�����:������vY(`�T/T�&�h�����['ځiu	$��(4�)��H�m�S��jY�pR�\op�>(� �T���{OWtbhx��#�u-Jq6bN�c�f������gތ���F� ��2���p�U��\����7#<P��E����u��#.�#��:)�ٽD�E��"��W{ڽ �*y뫸D��8��>��_������	�<�.���G��A����'V�m u�Z���~��8�е+�-՟p${Q�:gK���o��=�]y�ً5[E\����8$�&BQϛ�Ӛ�f���e�7L۽P[�Mmu�� j�n�ַc��ޡ���5�� �J�"���|���7�Fy��e'�R���v'������摤���إ�9��6Y�pMp|TK���WA wGߺ��hjJ�)KdU]��Ÿ�Lc\N;��
���M?5��K{TD��P��.�So9��;�r�Z\����hHLg �B$��h��A�V�W��t<����+T7����w�z���.@>MZ��<Bh�A�L�x���;z�Pŭt~Kȓ鮧>�v �Ϥ�&�E� 3��5�h%�P ����#\qV�#��h�#7�e���9�DE;Wh�)�ŉ�ښe@�sDx����ƶ��v��Z�ݾ�le��P2I��.�ۊ��%u�&�,Fኣ`l�b�n��cM�,��fp֯�؃V�Y���W��7��Z+�4�Y��
��]�Zb���/�V_�=�H
��}�����#���z��Z�)V��>���a��5�JC
��Tz�5�ZC���Y����Tb�I���D����.��Y�:����tN�y/�o��h9���NK��R�-�y/Bt'U_��kZ�4j�8��-�Åc>)���f��^���$&`�H�W��Ӻڮ�����i��^�/���Fk|T�S�� ������kM_�Q�V�V(�T�%��e�IDQ��x}T��fݐG|f���J�٭��U���z��Q�O��D�>�ԴH�_]X{f�j�}#��g�j8ȬΣ�j�����~i`��5K,-�s�����
�U�k?w��i7��<��*�M���	apG�D���2�K�Uv�u��pdFf��A�P�����o̵�I8�̚�[���'q�S@&i	'�+�֗q�x�>iNn�+l/����]vAbn! �=����c ��� s���ب�MI��;u 
#GjJ����M���/����il$v\� M6�����'����*\8G ��gPɦ۪�d����CS\@[��7�1f�9����y��?�}E:˫�2��5�д��mV'��h�-x[�hp��
�f����N��;)���#�JNi��WM�
g�$���sޮlz����e�Vr1�NcZ�\~�>N;�f�~�Q�-&��n0*:�7�nj��N�֘�p8'8�t��V�W*����<'a����p�N��j�� ֢�_�];���3��<��s�H7��9����H4��!Ȧ��$,��4	�V�I�s�L����d#ihu+K+Bd�e�|T�KX��c������嘼����}�f��oV����o������Zݒ�F�˟��C�z-��4�_Z{���ΡԚ\:����s�9���T܂�_�_��J�� ����L�|�WK$��]�01��K���� `{�k6{Td�(_�_暐Ge�hE�\^�XU�Rm����C6@5;P���н��g�C1܌Q��^�~�"��SDr�N���!ss� �3_C��Yi�o�R {�L���6F���B�=?H�l����QU�U�I���I&�w]�I%�J��*��#�KiK:��94"��tb\�X��[��inS���7N(]7�3�y7Q�Σ{|�F��	
lU�Z>�}���V���O�KKƵ��<��>Y�Y�V$ϑ�%Ǜ��-�u�:�F�3C:��Ȗ�v3�kr��[0�/��Gn�>� ~+��b\�k�ֆ��'���S���4�i-���lrj���"I%����ǽm��r-r�#s�1ԗPX,���f�	w��r�76��ə&$d \�8�9�l-L�K@&�)gݔ8?���5�z���U��<R�\1ȫk�xT�[.�
�~��M݌s^m�k���n�m���zOO��5��)��`(z� JY�X�Ҽj��i��4��l�b���e:(�N;,ŵϫc�Q�Q��U~ӑ��"�x�b�]�
�I�PY�<Ԩ�,��hv���,Ǿv�Q�,*�h�B4��9��]Gqu�i��,wFEH�ڋ5��[�h�d'5 ދ�ś���F�H%�Z,F��'�x=�pp�*s���O�vX��0�Ecn�;+}^]:ك"~�T�d����s �yd ��A�M	e��4X����ڟ=����1i<'j4�7���/8&��{v-���ۚ�{Θ���]�e+��Zqq��n��]R.��F��� �?ݲ�©2��h,`��{S�����d���zZ|jl�' �Wp棵��,�ou�m/�-#/%Tf������_^M=�� 37�����;�.}ŞU��e�F�qڮm�2($c5�;K��5q����!�*=�gs�T�y�Q�z��%������_g�H��'lx���c���h�]K
?|T)t�g�x�� H�_T�ϕ=�Hr1WJ5��UK�V���?�43�i��x��c� m[�v��_���R�ܙ.4�k[A�� '�4A�0)��j�l�Q&2X�S}d��FB�i��m=� 5O���S$�����7F������Jў�Cc#$x��Oj�h��a��[�[O��l���@��0Ex�P�:�n��{ޖ�T�vڱdcp{E�N��tv��cw�2N��W�Z[�����ղ,[ Q������� �}��ӌ�|�>�}B��&���Me� T��9�|��>�fM�r4����c�a���뮨кwJ����4ڧj�2O�|����STS���%�ݷ�P�D}G��չ�kɄ%�(I�N���v}���7A?P����6J�O��co�6�2�l�q�5�hˀ��X��zcO������[dm�WJ�F5�]M�?%���Jb0M:�3�&F)����� !��Ȟ��mb]:�qɭv�����vnI&�=I��R֝���g�E8�y��n��6׭g����e���G���~�ԙX�,c��E��{ƥ���6�%���F#Ry5�z7V����,�1���^gz�k�o�N�ׯ-bc�ME?�Vץ�j-��Ex����j�ϔ�({����8�5��p>}ֶ��/m���1��_YuWM\��~���v�k�S#�Db��`�H���+N.s�����<���>�uM�1�N������c�/�>���m4�g���+�沴~Z?�Gk}�(�)&N�CKk2�Xu��ޫ�:��	{ٙ擖&��X�*-і�i�]n�49u�4ƴF�!�vC�����fۑN-�Q�;x�n��QL�L�N���1�R�T���*l���[t*Gc�VG��ɕ=��C���tۛ��^ۻT�I�z�� ��dʰ� -�6,yS���Nh?�潾+\�����^L�Fl{�W�Q���O�ZX�0�<ǂ|�bk^h�\.$^$Q���}Jϼ��(�k{(m�j�պ:�U��!s�T
�Au5����,��ϑC#|?�Ӆ;2Ǘ�dz+��V46�h�Z�W7z
���M�(�Ji,�MrGګ�5���3a-�iFW��Q����W�V,�w�g�nz�?��l��{9^*�kk{�XՁ�#ۻv)�cc�3 ��
�^���Z�漚�s��5���ȵ�t�03@�B����sN�9 |�[��b���U>�h%|���Rn4a�9��x
�xa�x5��F��iK{����K$(�̹�5l`�ˠ���}Nm^�m��r�/W�k�;�J̙�'ڌB��X,��8�N1��q���p1J��c4�Ko)�d*�4J�%m 8XM,I$���@�x�=�@�%0ӁHq\O��)�q�|�ծ� ���@�<�b�.!�	rw[g�����������d=�5T�Y��[5�������.n����v"��)�>���e���4H���k[w��FX�<ԁ+/ �3Ma�@6�8��c�X���	&���}��)����jZ�x-��6�5&�EWl43ړ$v4p��Qu8d�X�Ӣ2����֒�.ѡ�����i�Kr�i�Vue�Ωz���Nq�c���}��x�2<���J���T���tS�U��坻�ަA#�n��r�Q�nS��٩�����`��6<��-�+sqN�C��ŝ�$���n��A<9�� �Y/%EԘ�N<T�w�죷��K>���j���J�I11��nl���7��4K8�By_A�q갍�84tڿb�E�7�N����&�eY_�>Ư�H!���w{����0��͊��c�-VrMSOu!��Q�t�SW�E��P�YW�h�I@�ة��g�67��S�Y�� ?��,�7`��e?%�ΠZ9��+����-�?j�(��2�I�E�`k+8��b��sR���h��l����4Qܯ�2�_�
i���ARG�����T��#3E��9 �2j�u_����o�\�E���&5nŸ��d@�r�Y�\��L����Gڊ1����?M_�h7�fO֖�U�Xc��C�]&Ë#��Y z��Q+2!(2E��;�����m�{|�U�T��q��,�o�%�<`
�h��H��7�>��U���M,�.�)'�{U]#�?ū#.�����x���cڸ6FNi���9<sV���h�DL۲x��L�e�ئ� ����<=�ڕE΅apJ��>�]'Hilrm#?�"��x�ݷ4�1��NW�գ��`���|�hB���CA�4��t֛m�%�y� �T�,!�eb���G��~�*�a��§dH�n$��a ����I��V�y�RI�t�x�]+�:m��꺆�=,g�xŧZZC�]�_-؀|w����S���wd��(����k�Y:�GΞ@�
����k�z��Իm4}2�&�b �諸�V�n� Sk0��~�`�i}y���jDQ� P����Tt��1�\��p���n���9ц����u]
��Ӧc	9h[�����r)����8E��V�3>��cEݔ)��*��cO`Ef&�'D��$�]�+���kJ�q0��|�@xu�x]y {^E	�H�Lc��G �����@�4N��H������Yʜ(ɨ���ӥ��v�E,�r˓�U5���>04��� z�Xe����k�C�����3��O�K����fɌm 
��/׍t�A����9�;��s��.�յ}OED�V�ԭϥ:���<� 5���Ql�-���]�#�%ØI[��\�iop?Č�8��G�I�d�� Q�V�)��4�Y���r�Xiv���B���*�ڳ=G�:Εt�i�������T�#�!��V�������EV~�]�V}_Yդ���j�ʣ�C)k���$s�3��Aa� ����Ҕq�U��M�[Z��`;k%i�u���Ǩ������Z�ڽdgO��|��Vg�_Z�M.�3�q�&���t������"dno�/Q^�j�_�=7fۇ>;�*���B���3�j�k���L�4�[+�����4<l{���|�lл��4>>�/H�M�;\��"2sRm��t��m.X�(p�Npj��Ʇd�u��a���kJ���zSJ��`d��y䐗vcܚM��6kԭ�*f=��	<��~��z����8�q�An�� �CҚ���8n�{��MM���Mb	�v� �j&ʸ�Q�Q�4s�q�<�ؓ摎i�ȩj�Hq\!�PV˹�ɦ�sK���Hd(�r�{�6��޶��L$�Z)���_i?Wt1u�>d�G$.A��=Էs��I)�mٰۛ�=�c&�I#?I�,��>�eM�}H� ���ylt�!�Q�Y��j�LdTR�K��e>���l\RA�i�N��8�x4�=�͒�4Bֈ�+�S	�	�y���
���,�7�#~��Ub�. w*99�)y���%0�x�Qm�	_e��LMF߃D�CFVd�;'!OcQ�y�W v����uEՖ�-.4�� I$�a��d��5���I��76��H�%���a"3x��y~��j�BF�-}���������_���W�4�!�4>�w��|;��qM.i��a�B�pO46�I	�\Ni	���"\O4�x� RT��!�(sٶ0�k��sCa��{�(�6� �� �!#�O�R!ͥ�F)�>E,j�8E#'ޝwot��"�d��*Q�P�K�5}WL}��d��kQg�k\��KD����N>+$eo�]u4�*I�c9v��G<���$d`�d�+^���-�'Ikh�yg��F?��+Os�[Z#��m��~03U�zM���ያ��r����h`cCX(�I$���-ėnO��YA�Es ���d2���Y؉�p�$��j����XΝ��� ���� ���..��f_M�o�Pf��t� �����;�q��V���4��U��g��t��#X���x�m�:�u]��uv��QI4#�#m!��{�U��K0f}�b~�ת�3��^q����~����_X��v�)�?v�s�^䅤�de8Ϛ͜��1�)9��ŤzpWG�ut���=���qDq��q�����#k�� KoP�%�a��(�	��e�u�sח�MA�1�ۧ[���i�Z��£�
��"���#��$�.#���?�ݑ�1��F�;�G���K/%�Q�[���餻G"9�P!�>O+Yl�Qf��F�{�UU ����HԐ�;@؞�|֦�O&�y��McF�{���Q����dyW%3��t3J�m����[K2n� ��'�F���Y�^���{	��P����� ���C�\� �k��Y���Q�Ga�49�
������#ku#i�^�
�
�.#a�9�e�	��\i����f"��v�ۉ>P��w�0�$�'��?6�����.�����c#۞)��ړ>0���7��yJ�����D҉v��`�P���A��h ����Q�F�Fka�v��8�n��Fp�0��-�vf�|d�a�R��8� ja<��Q	�qh���H�TYo����9 c��5!CI*[Ń#����
�sA[�ఽ�l�/����O�j�՝?S��d���*�H���iس�[�	�ᄈ@�z�[��-.,e�/��5"؈� �Ř��k�:�(�T�e��?��z�� ?���Ò'�1�W؋�^ǣu�:�;cΈ�6�.#���e}��f�{���K�s����G����=��򫯠�!�[���[�I'�%Jb<���͑�}���CY��I��4�����g� �9�E�W�Z�NB�밶<!�5�]m����x�Ӧ#3�����*���2�J� ������k_�} ����da�M�T�i����(�>�`;ģ!��yC?U�OT�Y뾲F�r��q������������tQ��iX/��>�Vi�5ca�+d1��Q%��PQ�����foL�TV�,Wa�X��ms��P����(n�b�9�~�D��[�YCM����P-EŬ�K����}\}�������D�lQ��Tvd��d�\-�!���p� 5��%q[�[Z,�1�	!Wz���X+n���}�5�St����[켳]Σ� r� �=a֚ł�}����{���Ky� 
�+�z�N����#%�Ӆ���>arx���X����cެ|�c�}��!���%�ϱ�/gѿ�O��դ���E���@��v�1���a�_Rn��,�tΗ�0�D��k�<��j���n�h�d�J��?�������=�Ptխ����l!�ć���?���T��&���ܤ`t�`a��VH5 7۝�wTue��1��4)-��A%�{��^��)�kٴ-j�KK��ԌH��S��R�뎼�A� �?O ��B�kp���6��x�g������Vh�֙�v�5��a�b_Vi�c�v����c�5�.�j�A����b	fo��X��>p���ܒoc����][�B�,ʮ�4��!���ɵ��(^l��Gq<Eq,w6��;�L9�����Nq�@�o�Rm�y�m�	���6�h�H��C1C���O�D��V�ԧկ�g���!m�Tv*F�N���St���o$w�}v� P�>h5v;|ţ#CC���mm��TEh��L�C���OaKwkye"���!���T,2W��ힴ��a�S+*D�%�=�ퟚ�6�Y'�K=�@�E�w�g�> �k��ɒ��]o4>������8�G�9dS����籩гC<M�ãwS�i�桩��Ku)�R�����B'�n|�� �T׸���Zo{�Uzڍړ$���O�Q6�e�ATH��#�QP�}N(mVͭ#�M�4�n��o=�(8M�����G'ޚO�+�@w��X�ID�)�雲2sښO8�j�W]5����&�ѷ��VO#�|���Ӣz5U4����W&�S���o��	:�Y�����Q�J�� U '����������t+��PN��Fs�5�*y �{�9�:nt�i$> � ��G��?B�j�U�.^h��c���j�P>T7A>�\��'�z-����6�+�V�iQ ���CnXk��#�`�\�z��	suN�*�	�I�0���d��C�t�n���kXIg�5����[C��=OG��B�H;�C\��3�/�mK�}�������L���|V�F���$�{WMms�^�D�7.��E;���,L89�SS׵!:�)�vƤ��ǵ&�VWL���mW{��Gf����-oB��s��  ́���,��,�7bGz�1ګ���-���I�$��}�2������.tY奜S��pL�nǓP��פ��m� ��BE����+���3H��{ު�R���7�*v��U�t�����w}Gڒ�ގ�/�I)�9�Ty�5kH�٤S]����*1�ǵ[$���W�%��A1�� ����jǺ>������ql��K�D�N��o���kv0��'$����<��U
������J�gr�X�4|ǧ��r�9c�)��7}����Ķ�v[bXe����"�4����d'�_5�����X��q*�>��t\^7ۿ�RIS�p���Ey ��W2�miy�ջu�����f���&�ln�-)9RF@�Np|�ً�f d��wTj}7�����jK��֋,�0�HI�?�0H�2� �8�,��Eq� Q�P���?E�r��zc�y��#��I�Ovis18P�hf��K# �dUZf��LҖ�DI�%d n���V�;�Z�S]5���4�K�,�����E\��Y)S�f4�,��}��9$�M0�r[�tn�1"��x4L�^H�<״_. ��OE�T@���Z�C��Fg�d����oj-R.�'��0|����O!f �i���p3A�-x���'a����Y�;N��亏��[�]#D �~�5.ǧt-6��ばTM��ǵY��.@R03�3��P/�Ri!��,��vc�`;Ƹ�~�����`n���w��C��Ƚ->���m�Q���⸐�x5]4��?�Gw��8ȓg�2�#�I*6+�-����S\uGR]�3t4Z�C�H�ehnm��,����J?�'�`�vI&'?�����z�I�I��G�T��=I���Lֳ_+�-nIP������Z�ۜ�6�@2�F�G`ѫq�N9��^�:�zkX�������� .S�lo��a�Nps�"�lN�/$7����D���B��l���I�PL�#t���Z0e~,�!�m�w�j<�6?��KϪ=U�:��uƉ�ͻ� ���\}�5:���|�`�|w�{�Օ��~��)4l0U�2��ןO��+�.������ǻ��+qCg���`�f
�q���	�L(�o�����u���ۛ�9�v����y����:~�M��k=̇��q�$��E�������uy��J��gk���[i�{��<s^��tgN�x~�k^�J1��s�F7�~;ճ�I#��d���D}��Ɖ���4�+S������6��6�F	 M��=B<p� ��22<wv��)ǅݜ�q�5ح׋j��)��<I"�E6b�A1,h8
� S��"�.����Ț{*�8e��c ����a�����S��IF��W�VEp� �i d�ӳ��r����㚅[BpP�c�&���[�Z��GC��~��)#S�8#�A�k}���X^��i�ut�D�v��K�)L3`vW�c�sH�����K���v2el��ѽ�����} �4L[h,_��+AB���;S'�����'��O�S���8g`?,��:����al�v��v�)�"��-�bPX�|�f���~�[��K3��20�mW��?_�����MhT����<WRKff��X2��
��2A�x�l��7*���_��G�ވ���{Ɉ2�Hŝ�~I�R���2i��W3T�O��L�n</lx�. \{���Nh�Nv�)F�ˋ� ���(a���8}�{Pl��+��F�S:�.-����TbH��f�H�f����"C�}�wK�����_�l?{�ώv���`z�X�:���ik�zcN�[`�������SӺk���6wh��7�ԭ�i�� ����`��b�[�:��N�n��}`�
�Ȳj�����?����%Q�������dؘ�B�<թ��/����-���w�~����TV��B���'d�^��P��!66����q4�)�&�=�皦���K���=�F�m�Em$���B���P48��Oⴺv���4� XW�����idn&�� dG�+" ����o_+�W��讻�.�t�k��zv�0W�Z����#c~sZ��]Y�'H�}NY:���}N{f���2��)_����5��:'B�s��he�H���>�t-��x��5�v,'*�v���M�� �_�ۤ���r��! �]�}� ��{��=����i6�jc���䁃Z�Qg=��Fr*��K��@�Fg���6e��EAk@v�l��$�ъ�Pg�.��u�X#�;�w���8�_���j�0<S�#�Ѵ�J]N7������՘��0ʈ�< ���U�.�y��#��H. vh�|�������r��������/������3{��xd�m�w"!�l�g.݅H
��� 1 �+�6|��1�i,�=�8o��l���� ����O+.J�r��G��jVW�é��[�pBz�F\�d<b�*�FeJvH#�����B���>ߚ,n�����mg�Rt��k�>���GS%兓%�*���/oM=/mŵ�j70^Z���a}��� 5*��+7�����0d9��{�)���~�%]{���₼�M��65�š�m�Ě����Y㻺���n�.o%3M5ě���>*AjB	��99�P
Gv�wm�b	dd`D��6���*�Ӧ$��:+ϩ�R/Ή�����D)4��i���9�U��j���&�p{�����}f�so}����ѣ��-��J�>�mk^�.���I�.d^#N�?�P$_�<ŪO��C���R�����Ҡh���^P��p*#��p6���{��穯��wp�������0�os����$�pM{����L��ӽ�8dn�#�Mb��d�?WѮz��a}/Xӓ�pH��>�n@��H���G'��%���G���n�ھ�3tzx���=��h�����>����,��Ş�Y^��v�U�'�W��L�H\>q����5?�Zf���g^k:��+5��їЗz���Z�H�G*8� �T��3�sB��S�
i��.�xoŌE;�H.�P�ʂ�/��N���A�~���A�dk�hZ����[�����H�01���4�F�9n�mmͥ�wWr�Pۡ�s����|M���h۔� dk���/ ��>���� qu֥��n]s?�,^��aｗ���m����kc�[��9�|s���ގc��૏qX��ó@�'�]/��@��O�E����/�� P����A��7
�F$���� J}5����vc�׫Iw�?�ۺ� ��Vd��ǚ��è(��敺	��6U��N�������%Oc�cR÷�$W���=�P��PjW�$�������r�ݳ�j��g�岌��Et���i���H����v��`X�doJ�K�D_�����s�?�<�໷��[O��u�	�z�w��k�0J���� ;�K��km�Ϧ��t/�@�Q��@��ZZ�gQ�M�St[[D@$K���#y8�|VgEMF��;]HB^,��ݛ	��ܱ'�(�:v�zۮ��l`��S���^�<Ϳ�~h�K���޵���>�_��Z�*N��Q�U[i��V�-~���-������?Q<~�ӌP~���x����,]>�����~���Yh�ua�ʶ�cayb��H�x	�,����L�c��4|O�w��բkb��G-i��9���a��+c�h�ԏ-���L��6���B�W�I�W����Z5ň3$c;|V� �����4�Ǫ�y�f�.��@�9����yӭlY�k�y?�B?�]2�g�:��3��ΚDq������e��w	�\��G(㺟�V���?��c��Vol�}If��d�b��}���ۑW��[��$�����M�4��^�c��#P�k��1P��smی� 4��M=��!{|�`@}N�"�#�1�*�I�N5�M42,�҈�F�W �"�Cu��k]o�ZR˫j-6�r�ᱷ8�>e~�~ɬzX���/e�'p̌Iv�y�lz�-6韪4��U�Mկ��+�
���j�d��5��g^�.�7�+k��%Y��4~w� ��h��M$���n��� ۠=�<��cM�m����mfP@�5'��8.e�q���s��U?\?�?Lu�I�"���[�Q���LB$V�H��@�=�����F�?�É��c>��,"oj�o���#2��eǠ�|����}��֠�ϊtm��Q�n��y.uXUN�B�8�н��
K=B�S�[�6�;���ё���{�G�+���|�s����u%���]�n��r�]J�l�2@^Y��?5CӺƥ��\�����Q�k�2�nI�YT� �Xs�<P @�M��c��ڿ�B�~�}&X�K	Ip�6|���H!�����Mݤ�6�?���m1�6�s���c�y4^��N������7U�V[MFѶ�=��d'����򋞥����D?�Φ��X��-Z9��I!�ǵsr2d�y�K{������:K��x���g�9�߫M��=�Ϡ���_}�a�=���T=Aѱ����Pګ�cO��������A� O �eo��}u���jˢl�lqG�jOqX�s���l�L��WUu��m��[�[ަ�'ԂŤ�l��1E _8�9���vIӏ'�����k�����<^�;[�k|� r*�@�v~{��N���^������=�6$�[h�}���8�j-l5�X���
DrD��~�1���oR��F�?Ml���zp�;b����G
��+�ɬ����Q����g���G�i�5��ϩ^"X2��&b(��݁{P��	��-�Q��Lh�jگ\��D(����$wc���A��p�;� �_I\���<)[����?���A���攩�� � ��b�E�i����28�M.�&&<� t�n� ?K�»�~���!֬eҥ$(s(�?(�@�|d���9�ibUˏ}ýc,zf=�'�WV!�#C���R�oHЮR~�� ������G��1�;�#b�r�>B։:t0I��m ���G�>��z�|pG�b��' �� � 悬d!�������ǒ�`�k_+���� p d� �A��[wh^P�b3��l~q\]�v]͒8&�	��<�Crn#lnXm�rGz�S�ܪ�C��ul^��v=�J�������x�g%���)w=�*��V�K�x�<��K3�*%��Gs�ʑ���I\��ǜn>� ��a�7�f  � �ܒO��J�~��x�,���K��6������� ���&���� ��5���>���{=C�,l�\f+�LEw�� r;U�������	>����s �O�	��~���Q�ZuU�s�j�OOb���$�ˍ�=ǓK�+�o��_Rm6l�E����tK��UF���u����V��x��Ll�'�>�4BIS���^L�Th7�W����J�XR%[y��@^}���u�����a��aվs�|�u=�� �P}�E�L`����8~���VR�yP[>Fh�σ�d��[<�Bl��⮐5� ��l��P���C ��KeBz�I�O� |Ԇ���$�P����x�U&�Z��[K��Zt�Y�+����x��FG"�7�z�2�@����.��]Bw���8�InN�K/��'��v���� ��Y����XWP����5���^=��`ó7���*H<]�w�Q��-k�I��yڍ��.��YZ� �n�͞���ޡ´^�{��$n�;��^���JAx�]���+"F��=�� �l�k���[Ǽ�e�I�mbH�'ܨ\n# ��U6}�iW���n爳�4?��|�O� K�'�h#��������}.�\
��'�:C8�ӡ���T��!������C|��d�!�x������~���ٻZ�-�A^~�{��{"­�￟aPh��ldt�d�Oӓ�a���2q��s��E$�5�^���g"�i:�ԭ�v���RFH��>�̃���$�<����ۈ��s����� ,,:O(���9���Y���o|���fI?j�������h������c&��4�%a�c� �z�� ]��6�t�B�Ά��(�m���d�c���#����]O�u�]C��gr.�n�Ci�¢��e�Ny {V�D�J2��<gڡ�k&D�+�X�"��q ����귶Ly%l��oh�l��oO�G�{˛2�Gz;d��fH�X3
�;��E_�v7Z;h���c���jr�M4�8ڌ�(��c�4+��-6�K�i�������w2;�GO�n��hMy��}[d�����7x�^6?����z{�/����'��=���$�ޚ~g�ؒt�XZ޾��[�'#2�җI���|g�h!�5m>��kcq
�h�?r���px�D��Xh�|�i?�����J��j�ߦW�X�� |q^m��N��7�]Aq#6�w5���!G.B���%����G�D��'k��McH�4A'����Խ����Q��&����#�6Bk�*�ns�3ޅoa�\����ssu�^^�{���@��Q�������)�C*��8��MS�-b�+ysa��ޅu�ԮnX� �l�B}�p�F{�\@������;�����a���� �kn��_�S,}w��Gnvzp�Lű��I���T-+Q������sbu����)i(x�@�q�##��=�OY�#���V�_�5Ѕ�Ki,���M�>�����I� *�|VE��,����Ŕ_� 7i�}�@b3��pxڽw�� H�� #p�G3X�M�4��ˍw���Ej#���5��:'��WMK����5ˇT��M��3�8�������\�n1Pz�]bN��4��WGf�홣�I?��#5r�����v�N�s��a��~>~�zn~�}8�!���=�Zk������� ���jo��b̀k�>�hϬZ�EO���_��mԥ`��l=�cbA�G����.~�J���}m���� ���̖N��P��Ví�/�����ο�u�Nj�m� �Ť_�۹� ��"ʍ�e��3�K��c��8�I��ݬ��'K�^�v#�k� ;�ׂ�?��w��5��i�����z�'���Iǚ��X\���ޞ���Y[(@���
���i�n�c,�e[Z��8�(�R����4p���{�q��Ϣ��Hـ���y�ze�Xj��ǣ�U�4�m��MA��d�I	�j%��Ӕ��Vq�!\��`.��X�V�g���swYP:� COp'�c���}�/��[� 뎣$�Q��ek+r���8��ZƗe���G�=kY{�BH_���"�6Oݑ�5�� �������MSLS�K-FxS� د���gMh��6���\^�ܳ-��+1��?����4��
�o�������˒dmn���m���^�e��>�z��5{�Ms�(�"O���F@V<�@�͎N���t��Ї�:v�4E
�jP��܁���dq�@����.�������x���P}��WZwI�Q�  o'�⺦en���<� �梟3WO�-���h�;[���ڗ�Z�H�V�;k=�^YI��H���r~��1���N����4�L�;A��o6���o���}!kі���
&� dn����Tk�D��Y$x��S��k�9i� uN�u�����`#���,;�A��4�$! ��q������?T��o��ћ�h[�#���H�1���A �e��h{M�DPw2i=IX��DaH]Ļ�NF�|�dI"`%�xî���tIWɍ� �v%s�\£Im�$̄�@��bv��8\��;�h��۶���3�K�DյKY/ ���0�w"�`���V'������p��ۋ��R�G݊y#�{{f�>��n��v6�n�!6�� �1'����x┑#��z�_T���1��-M$�q;4
�ܞۏּW���t��7�R�$��S��n����۲��lsY�_�v��ZOso}gm
�J�2�E���xn@ۜ��I�\D�M�d��&�K�����R��6�����Tuï�3���NG�#3�o��� �l�=s#)�8�w6/k��9�� ��'��;*�Gs��LQ��U���k}��I��"W$�j�e���	g]��(g��(�rx���G��.T����"iX�
I���wȦ�ό�tRY�s���-=E���S<�� �=�x���o�Hٮ.��<� n0��I �*��>N�OY��)4d���#���+�uK�RГ��6����A��Ӣ�=�c�L,O9��/�`��{������5�����;]s���G��n#����7��vbB�U��<rs�Q�l�ɭ�y�^I�(EUYI�d��>sۊ���F��]?7Q\� ��e< ����)^)TI�"7!���4Fh���eǝ�	���k�5\t=&(�QhU�-�0��i�1�O�ڗ��� �>��=�9��8A�����cr� ����2B��4�����4���Iܯu������Ҿ����O3I<�V6ҽ�NYRgR���=�:���"4ΙӮu٤�������\J{�g8�� 
���_�,I{t��~��mU�V�M�(�A�=�����<�
�6~�v_ ̈́�oP�P���`5� 2����U�E�����-;�t:���$��n\x�AϚ�����E�L,n"R��I&�����D� ��^�KFF�EN|�n�^��=)�~���k`2�vYO�G���.a�4���wM��X�xĂw�I�I>��t.�T�Y�������B$Pɋ�"PFF2�V��O�a�T�c���]!���X�mKB��t���'Y��e�qx�r��)=�8��=m��8�(p�vTfG�c�=@�_�7�aE�r�[�:I�Os]�w�j�M.��%��b����0 Q�'�-��.:�k���Cs7�s�`N#N;�G�W��%�嬶w0��N����H��+����Yt���N�����;,nǪ��[�?4��4e�����?��}��#[2�!�$����;l��WO ���ZKm��|� '^� h�#�h�[x��� ��?�O�3 ��ҭ��vq�$�:�#��� �?�ur>�fe;S'���?�W�6�FH
��k?�}�]	ld꾣���P����;~rG������Ju�����w�A'R�����:{�8jҋ���f�1��F�ϓ��;��϶45���~�b�)����Y@�0o� �� �W=g��>��?D}-�gҴ���^j2��C�A #�9�5��懤�2�э����|Z}D���c��ye`���$�+U�?O:w�"�:��G�ق1����Li�C}�ZNɌz��� �S��|���}�v'��W%y}_714��K����~ԛ�Z��A��4������Kh���E`�	��0{����q�U�Pn�7==�ͯ���;�]�bߖ)���! d�+]gh���QF@  0 ��5�1�;��{^W�l�G��(���zyH����V�$H�Wۣxa�)ܲ���S�u��{����"�1�m;>3U:��TF��84�#%��% �疣$Vܬ�95�<ia�Q;}97�u�C,98�,�u>��Kov��?O���%@�������6�t�T�)�.bym& �W�=�{��W�Hj�uwAkSi:��=�(�7?���1�Ea�|�C�#��z/C�!�J�pip����\�#q��zGOĪ� ���im�E ������>�o�k�kh�o]�9���SO������7�$����L�?�+(�����}O�+�W�� �,p�m~d�}+� ���p��^
� R4m'���O��Y<���ƒ!���	���y�V�o��?U }^-N��d�N���O�|�#�5{�{��������[�1�F��3�͙���4$��{��_gY�q囨��4�ƛܝ��2��[��r���|���l��(-ۊ<�4vs�FY�'h�?��8�;^q�$�L�� Koo����)�zL� b<�?#�ac��  I�ǎ|�C������{�� �5�]F	���s�$wJI8�j��Z�7�}co;��X��oi|s����N{g���9��_{]	�<&��$�5��o�_?"o��o�]gY�4x�=+N��a�u����
p�G$��d�W�Ӊ�?﮴��XK�[�� v 1*x$�q�+ԃ線�u��י��ѭev��
��R2#��\.�G�Bۃ����L � ɤ_��>��}o������6����_�
���/�s�0�ɦ�2е���"�hV��������'��Y��Z��ސ�}3�t'�-:��PVw� �H4�kG���'�N���_▾C�� ߘh��e���հK^�{�{�faq2��0>�T]9�<�qU�Z��ڋ����c�1���sr>�;�p�=��7��jM������6�G�Zva�0|������G���on?��w�#�� 鬤�u*����匂8O�o��w4^#C��g�%��>�;H�U]|���ꮫ�g��&�c�0u��{����=�)�����n[�������"~��m�<��˃��/��crg��5�D@�@��RlA�<�|l>�D�qy<�o�v*�����X��L]%��w6����t���w8�9�_���T��P��4Scv^��#����L,�����r�������ۼK��בD���#���)_w8m���7+T]c��[*@	46 rk��j�\+� c�IBJ�d�O�34r.�p�A|խ-*$�V�emP�
�-v����I�98�?4��z�z[j.�0����;��UJ�����Ob|
�[��#�$Z6����7CiZ�����c�����|��9���iw�G�7� �����3�"c��z����QW�\����yz�A���<PuM��������;���Y%�� ��  �����Y�A�����������4~�N�_C�e��y�j�Z6Zݥ���tQ�?�ɣv3��m�~kc��x�k��Oo"4mʲ��U(+������&�2g�G��U��/Gמ��:Y��T��g!��ȌI?�9�X�ϥ���z^����H���d��wWKӼ+le �]�py �ږ�a����:��3������0�W�u�L�d[���I�E�%ԯ^�T��N �o�FF\� ������ e#~S� �:���:��ڈuW������Z鿤� M�S��n��5r��Ya,!T@� Q��U]O�:���WE֮��J���8�a� �d`��8��T�"���}�F���q�&�t�;r�Fy�|��j��6Ax02��=RC#�;�/�����9k�L]'e-"����Ru��kh��bC��N?ՀH� �[�M-v�PT�:���}������V3 �p]� ������[��s��`� W��1l�`ns���j6n�i.��Z��o9,����A��a��}�	�Ϯ�5��o���R��ⷋr��j��+fe�
�r�M'��f ���M�-�[�Vi�l���a*o�V�� i~�ЀN��*��?t�N��� �X���ɝ$]�A@����9*3���/���c��T�bf� �!>���ZE�Ը�����2�Ѿ�Y�`��ԁ��������.4�mz��ť̊U.5[�.��ڠ�j���6"�l�,�E��c*/;�p�pO<�j}!��*ɨ�]K�	e�VlpO�z͚v�? �E��I���Gb��� "�_H���:�筺�y^��B���p �n��+��Q;�MB���[�������X�oF��HX�q����j�-�}��lxLDٲN� �ə���� �8�oEb���+���TX����5��@���v\���s�|�%��Ņ���$��������#烊����M���d(۔��5M�t������]i�w4�RlV>��'��=L�R�ޅ�k�8#c��m4��ƕ�N������y%���&̏bT��GL�8�����{�=��s*�|W�4��f�}Ѱ�4��U���OFۈ��&>@>�x"Pd��k�WV7�KMg}-~@nV-��l�T���[틖��xPNO�X5�R�i�R���6Zs�i\i�U��7*�q�׷�N��{/Hh:l7w1��I+��99�k�u�-5��/$��˒J����d�]�4�,�o�y���%��;���� �;{O�bm��6���@��2mj��Hei��S ��F2dc s�C�!ݳ `�Pn�.�Թ�Y2r�� j�p��c��]��� t^i���֮4�s�Ī$�����qS[���!};G��@�<�_�� |T�G���Y_Gq��*bQ�
��9>1�E�� 1�bsD��-�K�Ym�6��4���X��A���z���=M�&�l��D��v	��MXtݕ֏e��3�`�ZWD#E�3�i>��I�&֖=��AƎ� �+J�Ե����l�b3��<��g�m��沞'Q�7�8�Q����M��z���D�:}���W�1��Ob $����莛�ҳ�}^�B_�mN�	�ml�b�5�O+H܀�K;qI|����o����?���_��R����A���n���Tۯ��񡏥~��F�/dk�#����nlV�����s!w�`�=�
K~��m�1��?�k��|� �e��ܕ�%�����_��B�_�/%���i��V��+H�98/g	��)� �d���������~��ou�RC��/�36~7g�6�%��=8��EX�1�WK�V��y��Ä2���ztM���"���O̪ޛ��48�;{��# ,q;��@����Դ�+v����-��I(�O⢥̒L�ȡH0s�_���容���[�ws�\��L�7n9Q];��g9Ҽ۶��A�n mߕ�x�����&
2���Y�YW�\n���{�j�6��j���Ӽ�o���	�0O|
�^��e�l(�{� m��e�X�9�1Th�P��y!B���7 ˑ�;ԫ.�:���v�<�W��� ��v�rfK4��NIUZ]G���V4�3q�мSB#wnQe;���a� ���������u~�1��(��՟�_�OG���/#�D!�`���V�7�G|ұ��7�Y>�RO�����L��tx9�s2�� j q\����!�\5Ԧ�Q��p}�޶�?�:.�6W[e_��~���L\|j�\�m�~���'�+C�	������Q�zV�����g`q�/VObr(6����ml1c����1��}��2��"��ȭx*;ϵj�F����W+�R�Q�i���k����u/H�g�"x�K�v|~ES/_h8#�%�N�l2~�՘er>v�zL�&��
	5��z�M�tt��q#���VY�`$�-�C���[y2clo����c�^�����ޢE/Zu�PK��'�%*8#�vF����	��M��ۘ/`��&9 u#ȩ-�1���lL��\��2e�$�m@P p  =��7evr�+g�UKtF����?��� (2D�1���B�OL9�0Pv�;k�66�1����(-�6��7���2�v�kxB��K���@g�]�A#'�1��4�Ζ��^0$B����Y4���C���鎟եmB�F�x}�����4A��i��i�e��ʘ${�E�� Q��O�G�/�61ˣ�1 �� ��*?Nj�%�N�S�&��Ja�h�T�����_}�] s<@�ûl�w���~��m+�Cn���\_�t�����O�E�j�T�~�I��?44�'�w�VGH��V�k�n�~��L{�XSC�׍k$��O���$�]o�~�ϬuI4��^����r}D�ϐ9��Z�z�%d����x��ZOE��-����<��}��4�J�\F5k땁-�`Y��ďaC1l`�M���2$gO`/����@dɂhd�o��\'��$Sdp2|PK�֓�<0E}��U��`c+.60=�ϊ���7\��r����T~�Ԗ:e����<�� ~z�]��Cg�ۤױ0IX,l�r	�n��=C�bҬ�ބ�L����M~gV�$�˒�H��8pE��-�2M�@���	mh��A�/�Y�_�-��.��W}%�RU�Ϧ]����?���o���`C�T�(� +:�EI��-�Fe�r{�T�t����RO�f-͏f�c��.�������'R� n�f���>�}+m>i2���e>�W�t���}M�=y�w�]j���w9ھ{�^�D���[.G�XäG		 {
C���Ӿ�p�g�t��O�3P�y$zY޽��2塁�}��ެ#��o����C���H�mn�I�^�Ī3�� �=?�Z����Lcv}���]R�7'���6v�W�Ɔ�k�}�a�چݫ�+��K�0>�Ҍr,�ا���
<�M��)�a>h	N8�u(�A�튣�����KHd���V��u �by�;ڮw�!sB�܄�=�����[i�<��-��꺗��n~�`@Q�i�?S��k�}$��}�џaڧ_�� ��=V�I��-����I7Y�s�Ska�Iv��&���� 	�� �(K_��y��5_�k�V��N4�H�Z�Q��F�8�k>��Zki����<�GS���ԭ��OG��J�W�׵m^�Qԯg����� ��Z�eu�sT��6���ZKLNk�·o޽������'B�ϣ^b��]�����T�����/��t��2�ܤV�FI���EU_�3��B��g;��`�/���C����+l�C�����WS��ں���4HF˖��^9�]{ןU��:����e�`�H>{��Bhe�{8	�QIK�v��B��pX/j�4yY����ۉ/M���@�^J����=�	u�8�ʮHp+�� Wa�[[�ַ~�f�D�p��k����N����:��F�1��QV$_�F����QG�@Yf���	���R�L����M v�pa✑I�����2��(I^w+�e>#�~E8�)	�;�#�k��}��:߯u�l4�f�Y�Wd$`�;rI�MI^��//e����2� qa��y��k�cpVH�e��3��3�?�ƧA���ll�}Gt�$�p2�ph���*F�}G?VI��'4
�'f�쑥�s�C��ki岺E/)"�"��gijqoo>p���O�����]�Zޱ%����i݆c�j�Op2k=�n.�ih.�Z�Ӊ�SI�vsDB�*p{9W@&Ȣdh���1�w5ì5N�e�פ��K�r� �;�� j>6�N)�,rFa}�#`#�T�:�h��Ɖ[������W�F�
ϧ�1\��Yd�5����p�OrFH�W�W���j1�\h��� ӷ�d� �x���H����-��yd��S��F-�a��� ���t��Ĕ|��𾛃KL���x��8��FYA�9�|����=/���&=���*=����eB,�n�ݽ�Y�hs�~�p����|�o�P��_[���GJ�Z�+��FFYO~+δ�gN�m���`��"��~�����D˩�q*3eS"�kz+�:�8�,1\y�����i��׵��t��<���\|>K��⛹A;�}�,�5 I���m	��������}/�����m�h��O8�q��ɥ��kG&�S��
��qV ?�p�����_J��� 5�E5���s����/�V��[�V5�y�}u�z�Աh�!�qP�ɯh��E|o
|���@��W�|�}�^_^���rj�L�-UoN����ޱ��z���]^�y��ļ�� �SuDj4��h�Uko��$=����o�h��œ���(|��3�Q�,��,O�y����}:���F3<_k�޵es���x���$ra�cx��P1�+���������0��A�+ �>k��p*.�cm��=��),N0U�E'&'McM��fǃ���n�.����4���]V5-�@% �޽�tɔ<w��b$�� ���=��u����O�lEy�� Ҏ���M?�o����5�3fcl��{�����/�p�_g�}e�TC2���� �?�P������i/��8��A�_!����l�cu%�� �4�� C:�Rpu-Z�@O!����������U��5�T�v=��Ǭ?�����J�GGۚ�	����\ud[�%����(*
֣��������jJ�2����b��N��E���M���u�:�� �փ����lv� ��s�F�n���m"�6�J�>���8��F����1�z�� �s���2<�&�K��ݜ���=D+�x�ݥ�Vi��Lţ�2,���	p��1���+�<��ԙ�����,}��� 6U���^��J��2j|�kw�r�A���4���T��<z�\^[Mse�`�x�@��Q�lה�����L~���o0{v����,?&����o�ڨ�K[�Ou��Q1�jP+~q��X�me>hYue>q^����N�.�`E&phcj �ښ]�|Q$��"���{��J�+� �t���
�v���Nn#�y��oE��Hn��%����� �  �io��h�7W�����=��f&���]f8�5+��S'bY]�A?����:{��4H�6��,�ZY$m��|��j�X�[K�MCX�g���K����8�ǆ�J�,�,57�./�u8}�v��ư�8��]Y��X�$p.p�H >��z���j�J�g�<V���� {jߺ��v������[�f�-���0_���WQ�#p�y�X�ߺ^,��dE�;{�ג����4�6v}y ���*Xɪ�+馵�k��7X�7Z��O�9m���^ܶ+s �UFOs�T-Q �.�٥\���X��&�I+�Sv�6���k@$|@Q��E�K0b��H����t`���+ge�$ڍ=�WgS�A���=�)����DUUW�$�h2� 0��oi�y#J!`G~�3��3���	�q��
���Ԋ@��P��6�Մ� ҥ̧rE��܁��Jb��r;!�88�"�Mn�/��.��u;�P��&c���~	��z_F�;�1zz�O[m���Ex.���v�k�{�u�|n#����+d,�������K��3JnFF=�,}�Pgt\.�O2�3�U���>�_��T�*�i=w֓Kt ��<��j���K������O�4R8�a�c�5��OI'��]/�n~.>4L���/ֻ���l4'������i�)�I4�ґC~9�%8n�Z��#���͎j�X	(�S	�"���nE
`�NNy�P����ͣO>��\#� ��Z�����H�8����?D؛|a�@����7��ڜ��S[�,��T�Y"Ec܅ �"���q4�<+3�H�&EpREph8;&~-���Ժ���Դ�[v�TL	Q�=���յ۝��\�����#�Pf�[�f�{�T�X�W�f�=u��:$�U���q#�y.��>i�d�ܟ_jX2��fܜ � �rl�TAջ6H�N�#�(��{�3Z�3�%���*�s�0T�J�/��B."��H�$���1���(:�y$���S�G$�g��Z�?�
pW*���]������Y��mjG�2�i��8��	��A���G��i!�i�Q�m�`���ڣ]ژ��渉���ߎ�U��4��/��t1Is"AIf��4��C"����a��?��u[�?F�9�{�.�rT��8���5C�G�D۴�oE��莝дA{��K5����p}�v�^ky�ڕ��{fd��I��tN���n=_S����� �z������j˫��� ��� o��# ���,]�����=����Y�����6`;R�h�1R�"��^o��9��y��XD$q�����-[��mt��Y�"91�{�śX�w�v:.d�T=���_�i���w�6?O?��Ů���Ҟ{�j��jW�Յ���0I#��e�r�w��;B���Gc�Y�&� �=WP� ����vY�k��髡mf�Hݸ�:(�Q��t� ��j�,�)� ��~O���/�^���_�����&nq�E&�%Ѷ���e����[�i��#k�T�_���i�iښ���8�{R�A�t=�T�H�s�ږ`�K��'hD��8�Aʨ�F
������ߦn�K9 x�G�^��+�kK�譮��+)�<ע_��٠�w��#�yT}��;���G���s�?�^�q4r	" ��|ϧ7/�y.,$�p���f��4�Su�u5�Q��Á� s^�{��O��M�L��T���ܨ� ?���X������]�\L���J�?�[.��w��s*��F�|������!��g�-=#�􇌒�3۸a~��E�)Ӻ�M���bg����TJZ�m�Kt
���R?[
0��5ҍ�������BW�d; �ݺ�>i5{�����sG�E�7ޮ�e��F�$�$�&�Ϧ�!�A����?m�{��;򴰘x*����B���G�Ľ� U��w����������X��k]FQ���ǂ0ß�^��wychѿb��Ǿ<U�H�� 4��NUp(�i�f���6��>)	��I��Hǜf����}��C��DP"ғ�Ltg��ml����w"��G?���уM��d�E�D�P�I}-đ��⏐W�r?�S���6ĆL��}��qVv��¨�$P6�+T�k �R������)�Z���i�M��T��&���W�d��su"p	˶����KK��Y�Sv=���oO��孮u��~��ⴺ�н:� K���XU*��G� {VB��:[�������>�"�l5�-�$����EeuS� �QE��F��@�^��wWZ��,�s�E[�}���u7kMݰ�|и����[���/�x�7���莢��I�idyp����E���諈��VrL�j�sڢt�׽s���%�N^<э����/���_��MwU�kHb?�BO#؟s@g�e�~?�T}^I\̪ j�;��^��[l[˩Tn�N 5�?T������=Ǉ0�s�m��:͸�I"�;������G�sZ�����F��G+.k�8�y�M�>��:��h���ȯH���a�P���b>��(���du�!�m^;)� >0	�|Vo��v]���B<��#G�rhm��ic��xđ�C�Lv�VxD�ouL[-[S�I����3�nh��zg[�FѮ�t�r	���sR� ��N�_n�2�9����u'N>�|/�K6u����k�=@�J2H~�������M���d{S�ZF�װbT�2�T�lP]����E.�1���RǚM��+��G�B#��h-�@BkM����<sHZ��U�,i�k���4%��X�)���)�McT�$'�)��ڔ���CH��x�3R����R ��c�O�1��Y=�@H�H�Hi�…D��S8V5Ko��t��od��M����jԵ#�"�p�Bln�D#\d
�-�F�1��� R�Z�_�Ac��^�Q'������e�������sZ����N経��E=���L
��SO�3CE{$�����+���S�nn��{�^5f�Ex���� ��(A�[�K����۞�m�u������Q]�p�,��R�'4M{�:�h�ˏK<9��*��}RKۛ���!<�AvL�<8<��W7za8<R�+E P�M�>�!
���v�����D�	6zơ{l��k���P:&;r�<�
�+���޷� �5Kۡ�4�����F��-b�<�m\��b��vt�r�p�NȺQ��=��ʅ&R�����XE�������ͻ�_�K�8��ޜ\�44����1�25���B�E����k�6�v^T~��_��Ab�V��r�l�k* \�ȫ%8�W{�y�����FC��;�-d:���bH�''洱�c��f��R���A5��)9����L��_I<�1�*H����e�`B���������d�Q�D�����Cg w�n�j�Ǣ��xn��� #`b�j�0�^Ƿ���or��瑲q�i���@��$�d5���i�g�h����s�⊪4����Yu�d��p>�q�3E�1��^���R9�QO��Mg �b��Tq�@�Ü=���[+L���5�(�5UJ�vq\_��%�qǚeÄ��6 �;&5��H����E&z�~����w�NI��=Ksq1��e�<dw�x�q��F�QZp�8S ���!,d`�K*ą߀)�����6�ps�C�[B{dTH:�L�r�D�;��+1ԝ[q}8M;|�Km#�U8�5&A�K�MU�ʰ� ����J�H��s��W��?c�P6��:��B�E�&��`A��Pم	Lf���o��K;�}�j�>r��O�}L�lΛu����1�RG�Ҫ�9�A�Z�` �$�}�q��@<V�� ��'ұh��-#���֬˵�E 
;
vqMc�,���߭ܨϦڻn1����}E���D��?�}�W��C�t�mN٭�c�q��"��ك��yC�����=6ʐ�aq�s^ǥuF4K"�q���|��K�+�aq,$������:�1鮻|�9�L���򽖶�t���ɋo����~�tHXI/�iN�3_'k=o��Q�a�G�X��L� �O��Q%��[�e���#[���4X�l`7�ZL�df��-�V���:wBk�9�!g�-v�4�f����k=�v��C����W�2�,#��=�:m奾��jE}2pc����<��>gdoJ����ڂ�������P�����i� ���� ���7KEj��[Z�θ�1�ݷN�z��r�YǼ��t�<�PM����l�F�~�u\z�VO&��#*8<ְO�x��=�O��P|
����Cp~V��7# �F�{��k���������b�I�h���;"��I�c>�T��o2y��.�!Q�Q���ԡ��q���6�M��lRg�~hJ �g�4�i~{�n$�s7��qJZ�MQ(�J[�0�qv=��cڄ�`Zq8�7�S Prʧ��P18<g�Q�S�{Swf��0��'g��"��R1�V�\a�!8���P�\��0�}1��UJ�2��W���j"!ϊi8�-��B�v��!8��Nj��o��b)���XJH�M=�r)��+]�Wf��]�TD���0ӋsM85���L�b��Q��ސ:0�O5J/���Oɦ�b�5�W�Ӏ�\��M�ql��õ.({��⪕�O���ǚM���W��>�  I=�G6r�~����Me�N��L���qT����m�6p��� �:f��t�U�
��=OHȻ���#��xͶ�����+ x�j�Uk�`�7�Tr��;/�}ڋ]a^��2*��'�ٰ��|T��|�YU�V �F�b�h�@�,gN]XY޼���0' I�*WV�]���m�ƁӅ�!� �&���t�d0(c�qT�VZ}��[Y�̇�]����u7Ȼ�y>�l�;-�M��V(�'�nO�I�;�m����>i�,������M{u<�"�<.kNH/���4��-^T2����a�>�.�� ��Oa_?KQ�-Y��3�;�V�/���~�p\�&1��f�c�F�����tn���pʹ�K_��i�,����5B�� ]f���3^I}�u�ao/��6U	� �zn�j�v�?j�M�c1&�U'N?�=ڟ�h�ڐ�j*�Oz.�)��Z+�ɧp���jIbɤh�h(�x�ݒ�)"�͏4���Dy85��Z�Z��$�G'��鰕��R�
t���hH0=�"��{L�QU�	U^4�X\vf � ޯ'��r�~E%����$y�~�[�$6���Ի�2�PM�ƭ��*�p� ����4V���:��eD�/�� �C�;d�"�D�W�(��x����~"�h���?;�wcQٶ�j<Z����瓁�5ES��m����m��_w�j=��� �� �{Իބպ��H��g��4�q�(�y8fn�4�G(y5�L�/	�S�J9��`�4[��T��r�y�3g�K�3It!W��G�n)I�1Nc�bM	Ln�wf��ڥ#M�i��O/���b��4�|.���JehG۷!2��b��~���IP�q2$x
���]�̌�0	$����v�	$���n�V�i��fL�d�4�����F[o�s���8G��z{��sƲrr�6���'���=��y�(i��[�O�Mm��d�2�TE��1��kq�n,Ȗ1&Gڹ���i�Y��U' ں��9\n��^�8��j�.qMpEo����'������q�ݘX��X��tB��a���k9
��I��������Me�n���P�q� )c��F�H�З4��3+�
�$����S
�pG5����j���R8�p�ߊ�ť	�+�\�"�˂�Z�b���sE ��Oj�e�NH��@�b��a�����r��]|l�d)C4�i|f�d�4��)4�����T�.c���Nf���X\N)�ɮ&��jI�� ��A�8JUv���Cv�ݰ*���&� �i�5��w��G��Uݤ��ӱ,���>���w&F����G�i�u��'Y�S�9�9������h��i ݏ����`��N�rs0���i���z�ޔI� lӷ
�7k�:@G�v�PR�5JiD.pzO�'�(IF�Z�#x�e�2F;"��:1���ZA{zS����?�sč�>+����P�.L��d�9㸩:֤�`��P��0k#&��!���陹P�؎��C��3K�t�.%��Ǌ�^��F��U�_XuN����dm~7jA�S@��剑�I�nG�.�p��ҟ���m瀽R)C(>���B�*H���q�t�^@e���ǵT� vH�o�FǂÓWe�4�hA6��PIm�0����7SwWn5i[�j�Q�-�D�U+t~������ ���(.%�5�p������E��ok�#�*�r¸Q�q��+�J�PN;�ޮ����2:�SM�-�Y	�*RJA�V�VWxc}�y���(A��څ��L��)�������5	@��{6)�eb{�Ƣ �]�j $xzMФ	0sM�\��k1�Uj�7�B١i7R���S�l9�!8�c�0�m)aLf���4�E	�0�m>j�S�{G3G�~;��$
c�q�)Ohr|O,>ʳK���O�)�1੪������"��I�$`
����&9h���EU�G+�)ΛN��:80�'��P:v;�"���ɫ�&|�T�&01D4�G!��Ef�M4�4���@�k�ȥ\�M-NC��	7�*��	t�"������E����.#��I$���N�x#����B8���f���Q�=�EIC���q{n������]kq�]���Ͻ�A�&���[dU�ı�(H� ��X��0ñ��6M���7�3���"�z�H��^����.�߫O|W�7�:��2[��9�PGY����2{(s��.Bnx�]K���4/J�,�r��|��=f��B"�|�~p{U��]�����MAѴ���E�%��M'/����3�����>G[���^%b|T����k1 _j�W8�T�cu�ͣ��dQɩ�n����,�s��Pİ���UH#h�1��]�̦�ܽ_���+1�|g��v�����Ӻ�},�Lp;�1}g��,zÏs[��C��et9�|<a����:F���w�{�:��m`�O�W����^6�Fn \�/�㾸�7���kv{fpdk��z+�!s�;��w1H�ϱ�]��$"����6oLNEJ;��H��@m���N�"d��%�� ;����qS��#G�߱�$�,���l�Y��؊�?���9�@$�Ds�˘�w�.��4��N�h�q��i#�f�H�����k�t����d�a���&Esw���['n��Sq�HA���k6{S2�L�Uʺ����Q���]��K����)��R H�}�uG�)��^�|�57�(� jB�&��vqC�=��4��*��H��4�+�ۅ$��@���Y���O�=��P݄�a
�S���1������-g�.aY��mCVH_��S,5,jȻ��4��Nw�i�ِ�P�-D���3M]��q"���Q�A9H�O��\��Z���|b�z�k���3��Թ����zo� �9���ӵX�[�\�ryv�������kѭ&�	��*C/��G�0����3L-M2�XS�<5<�|�n���4�x&�j{73�9��)��D�hH��M-�)w
5	Nh�8�ސ��jll�/�#�_��L�7*��棼��/2/���k��e-��Fnm��Jn�1���t��suvW�K���)�3�E�,ľ*S1�@E:�Ȧ�N-�i44���I�J��[=�������i����ГI����n�)����Ƶ?p�M/Lg���3�A�&���E/�4���x�&���=��Ǌj�&�x��\I�4�)0$5��H{���j�0پF�����B�ԂeϚ��$�c1Pj&����������P9�-�L�&:�5kS�ڥ���q櫺�kVW�D�������N^m�s铂�R���uR=wP����E��p�(t�Ǒ��튟n-��?�0�#�b�Z�a@��R7q�Pa��I��RH�dW+QD�0��@�M�S�b���'�w4 򍄎K}�q>��R@yP�G������e��v����H�p��F�E`�Ț;�>6�[6��⮺���Dg�5B���șjD��H[q�t��p���ޑ��6�Q]O�<Tk��ms�W��(���A4
�y���		�j�󤢑��+X�C)���zS�c�	�Fl
�G���ۊd�՝���
�b�E� ������E�0����c#�"�n)������<�m����[d������%�L0�扏s�.H���dz����-"���Ѯ^B��'5&]&ћ>��T��1�@��G�rlq�z�1V陮,��t-��w��T���*�	F��nG5�p;T�.�4�&sHƅXHE�N'ɦf� ���w��jM����0�5Ÿ�o�.�zS�b��8�4��5۳TQ[�X6�D�(�Mԅ�jP�@�A+�3��I�5K�4�#�Z�cF��X��|�T����s\��,n���f�ɈG*�]}P1�QN?��k}_w�NT30'�)碵	_�GlU��б��IW'�Me-��4vtc��;��˙]n.A��1�ګ,,ⴌF�*w� ��1���y�܃�&��Rn���P|� �6E2�=4�����CcM�R��>�7<�O�75 �B3]�i��qBS7Q�K\3c��F�
z���Su˩`�K��6�}�K1UϿz�d���1�ؼWvVΨ�c���$Pl-�����W�h��,J����F�N���RɄP;N���Er��b{�;���2m�#�HcYQ�����H����PU�ЇA�9�oU �M&����P� �cCb8�zBSZI�iɮf���)�$o����(D�֨�9t�=�	I�R��9;��MX�9Q@B{H8Mu4�M/T���x2k����0�c�����r0���!l��|�w�`Q��m���5���-&ҽ ��5���'Bf�&��]�� >qT�LW��3bG��D'uE�>��6����Z%�@] #�v,~y�"��j�\\�ⶆ����Դ�k�h�')	�5��KU"#�<��WM&���QR��n�R���]��:?�<�'�j�ɶ�'�E������sߚc\4���c�E��nu+��R��� ��-���x�MVY�Uh�Q0F��n��6�=�#�)ZC=�!��8�Y]SQ��g�%������o#?i'�z� B�D�V��{V��ye�Zō���u|P4�f�UX`�*�ud��/4ym`���XU��9��6+�(a�Fl)~kG���,~�����5�ѵ��*���x�5��;<I�K�}GC7�@�&�$�B�<���;{�Q�㚓c��2��ȿֺ2�ϕp�Κܡy��|�.YqP���uk����7z�b|�|W/!�#K��H�R��3�>8̇
*28p����K@s�Z�ln�3�ț^2���*��wڪ@Ϛ����x6��5_��nŷ�j|��N��Ø���S[�x56;q�Ƥ�����Ƀ����Ԓ!�O�K�6��ӗ֦(7|����z�������,ҶI�Cr�9@x��5��p�y��zJ�I����K��Wn���L���|��ƻ'4њRqT�;#�(8�Q�F���OzG��IHiI���q �y�F�(۱Lw�Q	�$p�X���DT�B3�' 悂~�yJ2Rq���|��*��T�?nz���Q��[���l�2��>jwTF�۰(D�JO2¡TН���6jij�֪.����r;�wL�[K�����0-�a�X�{���^0P�V	��;[WwFI���:Z��n��Q�ܚ��^�[�;F1�a^[ki4�fvĚ��i���75�<�#(�×����㴬��ʷD�ŲMh�{ن{Uշ@IpAh�=�-�M���]0@� B��+�z��tX�ċ�EY3Y��L#'��[[ɸd��L1е4�+�?�{6�2hRH�}��Ҩ�Djl��NXSD��2���+ȣw�s�@����c�A�Yu��c�mV[�SI�&sښMYB.��!ja8搷�QFs(lOzB��Ʃ�4���M��Lc��Qk�e��Оr	Q�g�)�{�Y)����I�\[�4��%	���#�|����`&2�p��M#��b�BW$�E`O.����p�[�J$��T}�R��z��H��EXO4��\�n�&�M��&�5�e0Fj<�P���G�H[��#�#P �3�6Py��Fpy��p���+I�ױCp�� �=�����wOo;}����:nW ��}K�$~��S�t1sZ�����~����i~��ii�cU�k�-�;��[�jwWu������3d|VKK3I1�����d2I���X2�c锭���885�$����m#m �<��G4�Ņ�lh��^��l��l՗�u<i���g���;U�h�,xb3@&�>�ly��=`g�7�5�������\3����v�2��Օ��� 1Hy�W[��6(��u���>� L�r(��Q><l��ս��Ti1��j�� ����+��b���ey(�n���QH��Eچˮo��T��Z@���js@�s�>j�"�6 8�ZN���1���ܠ|Sm��rjK �(�B����^�;���LQ����8�$�B�+�����j��M�����G4�+�r�[T�)9ťJ�C �O^!�]C�8���.�Ё9�$��ZSټSI�'��6� ���HH4ܜҎ�Ev]��@���5�#4�����y�jR �M�T�{��qޘ�뇚uh���Ӗ��j��4��޹�PG&�yNq�u�IǊ�*��>ԩ7j׌)�f>ո�s^��W:t��̫��٘�����.gFeaY��K�i�8c":�^��L�2y��v�H�6^(�^�|~��W�����3n��>����6���>�:У�M֢FrMm,$>����n���y>�趜D1�Y qp$�I�����!��MO-�l|�g����UAE����j�M�FƖ�VN�K ��H��E��}@��MC��d_�B)�d�ۜ������1�W�_B�P�&h~�E�F7H"�Mb;�	���QDL/Jݩ��R=�g�jc�G�ZF�)� ?��s)ϵ4d��1�(�;SH��8HO�0�iq�!�TxVI��KM5ECl��g� ���|ShF�H�1덽�Y�ǧN|�T� =����U@���S�Sk�
:K�B�<���#�T�.'4��II�	K扼Cࠓ�*;�=��I��V6T��v�܂v�«%��`r��Vc�8�G����Y	��ʙ�X��V��C��fڄ@�x`���QqF��4�� )���#�����V'@*�2H�y^�2����r(B�բiM#��ڹ9j��ip��4��?��#85Kq4��RB*��(��j���r��m$Ti�t��ћ�����#�\�(~��*��c;� ���(���%��t�;}�Nzb�lT��u�� -_��Se����
```

## assets/drops-6392473_640.jpg:Zone.Identifier

```Identifier
[ZoneTransfer]
ZoneId=3
ReferrerUrl=https://pixabay.com/photos/drops-water-blue-background-6392473/
HostUrl=https://pixabay.com/get/g477c9d3930b5a12e6fabd21859333b783b7496d43a575d8b05525f18b5a6a18907321ece115dcbf88f61f20070cf16006967e50bddea94eeaae4204b91e9e3906a47534ef4ac720897238f8b211ff40c_640.jpg?attachment=
```

## assets/favicon.ico

```ico
           �     (       @                             ��������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������ֺ����������������������������������������������������������������������������������������������������������������������������������' �<�,
�c@H���������������������������������M*2�/�:�.�¤��������������������������������������������������������������9�L!'�<�pLR���������������������������������]7?�@�J&�?�ƨ��������������������������������������������������������������6�I%�9�nJP���������������������������������Z5<�=�G#�<�Ƨ��������������������������������������������������������������6�I%�9�nJP���������������������������������Z5<�=�G#�<�Ƨ��������������������������������������������������������������6�I%�9�nJP���������������������������������Z5<�=�G#�<�Ƨ��������������������������������������������������������������6�I%�:�nIP���������������������������������Z6>�?�K%�=�ħ��������������������������������������������������������������6�I%�9�mLQ���������������������������������S18�8�E�6
�¤��������������������������������������������������������������6�I%�:�gBI�����ۿ��������������ۿ������ۼ��kJQ�X28�`8?�T/7�˯��������������������������������������������������������������6�G#�F �F!�F&�E%�G&�F%�F%�G&�D$�I!(�ܾ������������������������������������������������������������������������������6�G#�E �D �B�B�D�D�D�E�B�D"���������������������������������������������������������������������������������6�G#�B �A �@�A�B�C�D�D�A�C"���������������������������������������������������������������������������������6�G#�B �D#�I")�H!(�I!(�I!)�I!)�J"*�F!(�K$,�ۻ������������������������������������������������������������������������������6�I%�:�iCK���������������������������������iFN�R-3�X5:�P+1�ʮ��������������������������������������������������������������6�I%�8�oKS���������������������������������W08�:�C�6�Ħ��������������������������������������������������������������6�I%�:�mIP���������������������������������[5>�?�I$�=�Ũ��������������������������������������������������������������6�I%�9�nKR���������������������������������Y5=�<�F#�:�ŧ��������������������������������������������������������������5�G#�A�O$.�tLT�pKR�nKR�oKR�qKR�pKR�qKS�oJQ�I (�B�E"�9�Ʀ��������������������������������������������������������������4�F#�E!�D�;�;�;�;�<�<�<�<�D�D!�D"�9�ħ��������������������������������������������������������������:�K%�D"�C#�E$�G$�G$�G$�G$�G$�G$�G$�H#�H#�I$�?�Ǧ��������������������������������������������������������������) �:�7�8�8�9�9�9�:�9�9�:�9�5�8�.�ã����������������������������������������������������������־������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������                                                                                                                                
```

## assets/icon-192x192.png

```png
�PNG

   IHDR   �   �   R�l   sRGB ���    IDATx^���w]�u'��{!@$� �w�]l��-YŒl+������y��[k�{Y+o�LƓI\��E�؋�{� 	 �{��{����sν H�i	<ׂ	�{�)߷������F����W�%]�0�^ҝ��+�3�O/�
��Ro���>�4�R��� /����3�O/�
��Ro���>�4�R��� /����3�O/�
��Ro���>�4�R��� /����3�O/�
��Ro���>�4�R��� /����3�O/�
��Ro���>�4�R��� /����3�O/�
��Ro���>�4�R��� /����3�O/�
��Ro���><��˵^��듰0����������-������|&����}�i�����{�� C_�'|#t�t3-�_���~f�1����1���Ob���a>3��	������Q��l�־��y?8Z���gq-����x�!�9�χ	|V��@����.�`,�{��GDD����sL8 <\%f�K@��%�Y����8�!��}�c��p	�)s�x�s�%x2�H�^J������]�~�����!~� | {��g���\�=-�}8����.�"����p埕��\�����mG;7���j��#��u��^fQ�#��>��aa�o��� ���mK�a��,zM����G�w�׿��g�a���x�`�k%?�	R?���A�2t?�ı��Jk�R\�H?�RZOm�}G��C5��T�	���p	���������f�!r�,x?""\�z���&�R�����FQ�k��H��{j��"��j�X�����1�Hp��F�T���ql_o��2�9L����@�?�1]�xW3F	8-�C�}���!@Ǚp.�|gO���3��IDd���@^�+�C� ^��?���1��o�j�<�$�R�N�푬��4oВP)%�1���"#%*:J���%**�d��s]%`�\�~}�>��ꖎ����!�Z��U�ꡦ�id�5��%1�hޯW��h�^��������/�@8�#ԃ�?�S������о��Ur�����h-P��L�h��?#Q�X�Y/=[Hє�dIKK���TIII���DIKO�1c2$DfL$�Ȩ����!����Kkk����KG{�444Huu����KsS�����Q�������U �!¡�h�� ��uh�чP���1>�� ^sƲ��1�Q� ��=�5�0/��+9{z4S(�+��t�K �sTd����JJr�$%%JbR�d�N���ђ�>JR��%!1Q���d̘1IBU�2@@:;:���MZZ[�������(��k���F=�����҆��Vijn�;�"$~P:�Y	8��#}�k�
��>0���n0�tU���Js�� �{r�u�������3�03�F�5���	*5��6!C�X��`qDGEJjJ����ʔ)�RX8N��r$}t:%lL�8�Q����w��&j���$�+�z�{h
�߮�nilj���:���������)++�7nJk[�:ʽ���)����!#Z�G_�|O���ߚO����L�Y����p�?�R�]rO�3�sXZ��c˃䗇	L�D)q�1���%��ْ��)���2~�x��9&C��%.6�X(��H�����FԚě��[����2���;::�����4AuM�ܽ{_��)#S�9jjj���A`��?hڨ�����!��E��W#I4�ȩ�<�ʨ��2��ͩ=�����_T�aN��IY��z鉌�����̔�KKi�[�'ii�-��1�_�U�+��\#=1�dn��I`yC�Nb�H�>����A�	�!���"S�����7�ܹsr��Y�~���wtIwW@zz��!&�	<>��_6���^�2�+���gG�[���`x�38�i$apS#:a$�>IMN���<�0�P��&Ɍ�Ӥ�h����"�S�B�ZcH4`§J�*�M�>D�zU4?@��!�K�^J�a$�@O��4A~�+���r���w��45��ihterU��=���X�W~�F���� '�����Vp�������a8�Qё2~�XY��TJ.�9�gʨ�d��uÚ8����ކH����#H���U���%�;�[0���z(F$M$��.�746ȹs����r��i���/�-�`~�f�5ۥ��X;zz��cs�@87��i���3�0��5	�(��'��(OzZ*�Y3g��Y3e�	�����42�n�b���,clذ���:�`O\�~�/��ĪL��*��\�����N�_�@n�.���o������R��N����$R��D�T�X��y���Ā��Oȃ��c��|fb�өcI�dw#��퓀D��ILt���J�I'Ț5�d��9R��'�II��R��CZ��il�G�ɣ~�NZ �an�oL�G"��G�O�(������w�����v����S�N��=�-B����S��a�N243�|~��k�@� ����eh���s�0�;�gT��S�	����JLT$Ø�ϕE�d޼�2nl�$&�K%��Q+��t
�A	{ e��i}T�2����i�? �.a&ig�Bw  �]��A�ܸyKΜ�@Mp��M����@/�-���$���Ш��sܻ�h�"��g�a���~:ރs�n$�z%"���������7�Ɋ�K%?/[�4�j����Bu3�G�FK���VCX�R�`����8�0��V-���[Ξ=/��/��-W�\��^��$;5�j�նƒ�^]�Z�g��N���F�9 �*�������믿*s�̐	��Jbb<����aT���i�9�bg�����y(��9�c��66�H~GG����P&��L҈(4\z}�ZN�>'���ȡ��%<,���d�Y ��ȗ�<���:���{���@~ė�E�	��+�}%PH/5!U	���8�3Z^]�Z���o�؂lIII4��4 ��M F����(׾wB�A� �Y�,���Q>�65	�"�
�M�9kf�����տ�V<.�����9�<�Y7DM`��O� S{X_��z��4��A�s9��d��aFF�˄���Z�l�,�?G���%:
��7`П��ި��0�Ep�`�3�>��B�Mc#HV���H��{jū=�7�/p��59|��lټC.^�"}}��
�/�d�P+	kb��L�G''�j�����÷k���t��e{{���̐ysg���1}����JT$B�A�i���@�>p dA�!^�!UK�!���ܲ1����5<gk��,oWO@�[d����s�9}�ܻ�PE���G��UG̫3�2A����N�0�Ѷ~=�𭩚.&����p'`+�/��˗Jnv���EK_ �0)��� �2�ҿ{W.xL�0[� 2���#݃L"�Q��ѯ�K�ݺ`�?���@_���j��?~&�6m���*ii�(���H	��� 3H}c�1��q���[��QGzn�qZ����� ϶n|�J�>��Bsܸ|y�[o˒ŋd��	w������	��L��=���۫!B5�F�B�b[M�o8	4O��!zk�Y
-/��S��ʶm;��c����ptt�dg�Ja�xy��N*��#����өaV�����%�~�1l�eO�3��-)�yP���3f�̜9]>��������Ima[��a�[[�&��7�5s�w��� ?��C����}괢��T�i�T!N�	��^�=vL6l�$�Ν�����������,)-]$+W��˗����NY����{�A�5]��[�ᐧa���>��.�2*%Q�.�U�V�ҥK	vS٦�NR6� ��@":�h�H��MxL��zL8����V&�&�"Zm�#$���:�z����P�ع���`�}���%K�,�eK�ɼys	�;r��ٻO�^�Fԩ޶7ĩw�$Q\O�XOs���f����DF��玑�������ے����N��Ѐ���$�F*M��uH���nAz�t|�d��N��z��
r@ۦ5
B���=r��M�b�9r�\�xY::�H��t1m�T���?�y���M�����ʾ}�7ʂuj�e��1@P[����jS�x�� O\��=��@����2cZ����۲j�
�������j0�S-`e�7Cj����ɳ%�B�B����x�m#����G�_��(��p�>sNN?#��I]}��z$1)A�K&ˢE���5,�A��+<����O�k�)/�K,��E,���l��Ȇ0�O�/�?�g��YG�7ёa2w�Y��bY�b�L�6��O�6m#,��h�P��,�x|$jQ�Ƕ��~ �L@X(4�=�uur��ٳg��:}N���Ikk;�D		����+�V/�e˖�:*E���X{�Ŏ]�k�>9q���<�ci�2��6�uڃ_
�{>/��Ժ���LL����:���ߔ)�E2fL�����tG@9����
G<�݊� ���<2�$���Ѫ�Pi uN��z���U<x(�e�r��5�z��ܸqK>��֖� ��Ѻd�"�:�X��b�LYd�������gdﾃ�y��[��!Q�x@D���[��vj�/�*;B�M�w� ��}�]��.�DGJ���·��w?|W�3ǐ!�e�)JTaӬ�5��$T��c��@����0�{����e%~�������!-�mR_�(5�j���Lnܸ!��\�;��Hss��t�HDD�$&$1���l�b)�Z$�Yc��g����n�L:*���ȵ�7@�X`��xqB�K���pl�܈���8!F]G���=��AA�평x�[�;ft��O�w�zC^u5�:�'�y{$zp՘�!������5��,L�]L�	%d�7m�	(b{lS]�ⓐ�Q���6)�����])+�O9C��u����,�M���"��¼���h�$)]�@�Ηi�Jئ%6.�Y� �ѬB/���O������.+d۫���Ymhw�hq�����S�]7�eW\	��h3k�"��2 
YPѵr�2Y�r�̟3S�c�a�6�cX�j�Qی�H��କa��^Smk}�6��w	n�]�P������f
j�����N-�������Y�Wާ�ZQq�q�{��1H��"�L�N%y�92k�4)]0_J��$''�9¾mk�0��'r��y�?���-'N�����n�V?h�<'[�؆ZV =&xI4�W���.�W��v�+�,F�2�~7�*�:Ѳ0R�Ι%}�m�?{���ϥI���@���������!���4M�'(�_5^n,��@�6S�����HL�õw���j���FX��WTTHUu����K{[��wt��]�� RMr!���⤰p,���se���4yR��$��.�fsR\���;�'�/\������=~J�����S���m����ڇnL�)�~s�%`��|���ne���q�y:��-|Y�&	�q�b�b��_�@�&O�Ԥ�4Y_�E�	�zzb�����u"���R�.e �ã�fcK��k�b%�v�knia�����L�G8Sm�j:�����a��>7͗^������=Zrr�ٵbjI�L�Z,�c�%>6��i��i�C@�^S��~B._������#GOʃ�i��"���@���2���
�0r���l
���J+�c2�Y)lr��޲6x���D����5+�g?����fK$�c� �m@B���M�S�va��g��	Ϊ�:����`Ã� ��|��ܻW)���c;�u!��j����zz�?���݃�=�za��Z�V��ƍ��3g�1��P2Ƥ3��2ξ@�y�>x������H	�\�zC����΢�����6�a]�hK�z��(~!��7Le�0?�xd�AU���x�@V�� n9��}�)�[�HIJ����ڵ����~ �����ӝ��y��6���T���i4� ���������|��k`x�)_W���*H�ƆFjv�>����f��G����t=:]��2%77�=�
Ǎ���4�+U��-������&�Iqq�������Ѡ��{l��ǚӕ�)�s�nr�
[Z�3�PW��`q9�u�:\��w5��)0�ɏ4
�������U��ڵ+%-5I��,�c����	؄�6�t�P3�9�) ��{[/ÖhUx�N�ܺ]&�nߑ+��0YɊ�q�H�G;D��:TSR��y<�YT������Ie���R4y�N�$'J|\,c�Zf�p@9 �9 h�IнN�b��qA�z�����'���{���E��A�6���� C�z��Of��'��?n_�Aj���ꭷޔW�/e801!F$,��Z���C��t=p��z]b�?�=6�Q
�bGg����T�ySUU#55���?�����:��o�A��WM�D}¨Q�dԨT�aID{�Q�(������ٓ�9�y�Ą�Pg�T��渚�T��s�İ�_��`4�M�Ϳ}"���� � ��+{"i_��[��K�� _}�M��1�� V�Ţ��E,���L�R,?��_ʒ%���FGC�%���]�f�M�N5�kb�v^Ww�ttu��~[�D:mH.2�
��4�tv4�/EF��Q���x��ΦI����6�h�gvV#9h�Ύӑ���!H����+�Pc�j2��dwoT�mQT���_��:r���;�Y��_�	�Ko�%L_"g�S F��=|�j��h'3΍�**�a����93����GR�p����Hx7� �kN�W�Ln�inkà:XBH�U55r���9w����U>�`���C�J@tD#"$55YF���d�0Hw�6���)ɒ���y�\!�	- �DO�7���@u�>
�U���+e��&�lXӆ�%�&/]���?�Y�;��Z�[��#�T��း�i�eF@���gao�<ȑ�V#� Ay �ܑ��(���`Rh����P�̞��^��d S��i�LRe�-�솫sk;�uuXnX[_/7oݖ��Oȹs��͛��vtu�	Fk"�=:.6��;>>N͗�lJyH���<),,�|���<7����`07�l6�dښ�4{��׎Si<���ޢ�C������s����񓧥������L�
�Rci���k�A����k&��6����������ޕ����<�]��	�	H|J�$+TbkBB�{Y[�ٱ�'�ҥ˔��jk����N0ß}��YC���fK���Ü��Ȑ��IHH`b��?�f��1L��2Mw�r�����'�z���rF�T[���XQ|���������_����Swq��!,X�B�&��#��m��J���\`e�����R�!P��͙%��X&�^]#��
t<��y4���w,�5�a�����	0ag-�j���cr��-|�(�����,�		�:
Q�Lf�'�%`��0�Ncq�e���X�g��I|�so"_��1&�[2lg��:��4w�	2���"������G����_���WM���0��k�{�5���k�gZo(8�2����k$���vFC��%<���Y�r��^��,^�@r�2	E �舱�U����sm�8� a�._��G���;�ˤ�摴��0�%	�	2�p����ɔ�i�R��HJ����x�@p��H�d,�wH,o�Qc՛�3��ŭp3�Vk(��g�|s�3��K[['���ɧ��g薅���*3��$��ݚ�a&|���/���)V�q6ehԛ�������J�w�y����"IKM1�9U�-8i02:����,��'���CRV~����������!�9Y2q�)*����3%>.�����4�r�5I��z_2 ��+�qV�߳c��9r���<6ϥz�-x�ol������]{��������%���Z��>-Sy�����g<h�3����m� ]��X ��wՀ	HfF���%o���v8��""��4�a��C�X�h�45��ŋ��Z�����ͷ�w����Ϙ1�3�L�"YY����hC��ᠶ�@'��w3\��n�p�u`�{��{�la���p��<�@5�@0lu�hU޲��.~���m��    IDATۿ ʴ�S]IE��L}�00WH������K� v�S�V�c��0��L��L���r2�g?�	;=�JEo8|��hF�I��� �)�D�P&�'N����OH����''&��$S&L� �&M�I�&Ȅ	��F=!1NK,�dF�J%�,�<De�����s�f�k�,� �0� �����5�������1����� ��F3V��s����w��y^L�0����a�.��y ���:"@�@#@ ���(���������J\,�F�4X��fT3D�C��i�9\��\�tY6m��r�����bb⤠�@�N�J纤�X�����gG9ؘD��52��c�4CJ�\f{�j�)�a��=�>��&m�Ta��^��3a���-g�_������|������d*��'՟�s�F:.x�=Q�%�%�`	j�b���D��)%��o~�W$T�5r�����@x��;�Q]�?~R>*�N�d�	̏�)..���").."�v>L�Y�5ɳ3���d���4N��J�����V���$Xt(�DZ�i�!�
܏�3j��W� �w씭[�˵7Y��kb�k�$}<�&O?�wd3�]p�����7
ɈM�#�"��9��@�ϛ#��-�?o6��ڐ!�h�\����^�k	g�|�z:���-�0)��2w�\Y�z��1�(�k��@�k@��62����=C�ډ8x$5��Q㡁2�l�bJ4�S����_��)$�!Z��4��c��m�㧟���[������N����l:�����?T`����P�5c�ye�RY�z�L�R���/Ma!��H"I$�-�l)�{�^J~��/?^f̜)S�N�ɓ'���� N�ڴ�Q�:j��k{+bԂ��g�~���]y�5y�����sQ�N�֩�2���^x8ͻ��F�p��FCӡ#�)jku�l�tD�<����$
� j�k�#$1�=K/��_[#�ϕq�
$�8��9}��G-msK�ܽ[I�`�-t�)**��dٲ����K�=&�8Yg:ܞ
�n"M�>�}��C�]^��Մ�`�kn����O��[ZX�[�IĦ������Q�߸�.p��l����b�w�1��?��L�3��\�̎��l�JT�ɉq������R\4I�d�+�2^n3��d ��&�w�9t�ќ0y&O.��,��ɃD�\u8�،M"��H��n�6qV�۽wo�'�x�)�A��ݲK��}/"-��i\^�����^�.�w�S��r�<|�h�e��)чzn�a �z�k)��d��$y�[o�������d1��m�P�;(����['N���?_ϑ�]2m�4)-](�W,���q&�n�Hl�`a ���$��u�4��1�j�R���ۊ�K*��d�c��[�q�- �L���f�!T~��0 Z� ��{C�9�'h4�ˆ�s�J��v�� �e �	&ё�1:M���������� F�MVBU�06Y�C��ș3g�����w�^Taa��X�,\0_rrsXtB2 �,@�1��X9�Y����#����m*� 0]�B�J OC_A�	�j�FwlR�<ރZc��ځ"����3gβsܝ�
yXU�:mŢ?�� .��6�ʷ|x
 �<INJ��y����w>|_��ch�h}��Θ��l@Ww���6o�'N��{�)�/^,�JK	i�D+iǞ���"Sf��d�8��0v���K����^SI	"T�o���\�� ���J��VGg7;<�74KuM�ܯ|(�Ϝ����ɝ;h�U/a���h]�v�!xOz}�d_�N� ��á6b�D�K�g������ɫkWIb|�m�� "����5�h����F**�	U^�t��^�R�2��&u�� ��'6���(�pC�LHt&` � 
�(+��W(IysN�JkÎv4��rJ�]]��P�(�w�ɥKW����,ԩ��a�hV0��RU��M Z����@�z��@qE��ؗ����J���K���`2Q�<}�Y�f�,_�DfϜ&��Q��� ������!�/\�#G��޽{X=����rZ*�TB[��n��-j$�qp]�;�V�W��y���ԑ�,\�.�^���k�ⶶ�����%����,�Տ��y�qK�������a3�m\��;M�d��mĎe��4���`�3�w����AtaÞnx�+=g�0���} �gM���L�PⷓQ�.�je����s�n���d�����)�&N���d�����	Q:���0����һ�#��*��\yo�kY0�6�e�A��J��HGg�466ICC�+=���&&���N����Q�j��QM�<�����V�����q���0{���f���5T�{����g�!���?x����KKFܬ��'t$�@��A0��{��P&M,d����̿Jl(��|��lܸE.]�,s��f����$=-�eZȦ�Ɇ8�W�����m �<����p�Sh����Ix���G���ȲJt�k�h��.�I����Č*(�A-Bkk+;��wD{��w���1�LG�<i8��Q�=�1f��x��@}��쏋�>��?Ց_K�����
�52�4��RU���1Z�h6�V$YG�H~ç�$I�|ym�Zy�oR���gz�� EO�� �'NQB~��)�ϗ��T:�RՁx�j��g�c3�Hi_;�zk��mXQL�r 9�9�pm��R���ʲ+W���
��W���٘��i̦�M;m����/d��MhyI9�z�f���6�w�÷N
ރ\���rrS�0J�9`���u�(n�F��5��wc����+�,�WV,���Ȩ�d5�t"�z������Ď/��o���oJ����_\t`I�F�;�Xl��`�}~7j�O�#ܡ�mt�(C7�
��|Ȧ��uR���>�]]����������k.:�>h�^��~*��䃾V�kCr�j$�om ed����A5�� 2���4dub��Tr�)���H�:�D>���rs������R�������ܩ��6���e����r�J�7w���d�ߎf��vK��m)b�@�Ҙ�Ԟ�}�I2u�Z�8T%�.�zX�n�N��s.���78�im��ϻ��^�K�A�-�[P�׏�CY�k� nT�]t[����逤��V�ˁE$�_��~�6��?���R����8���ߕ�I^G	�㼝����s�n9t��ܽ_)��ڵkh��X����L`��M�K3%^y6���V\��c��v���*�ر�r���;�����2�lmHM�����	���q���,�����~�׎�R^�+n��Q�+oc�:�P�:&b�/T1ڢ�[��z$.6J22�d����l�bY����wMo7M�uJMu�>|D���?ɍ[��6k�lY�b��Z�LƎ˱B�3�ܦ�S_/�C�2K��:��5�)�h��ծ�l��>;��r��y���r�������O���pN��V�: �4z��=k���_�se�N� ^-`	ߚB^F ��fS$�p� ,�6Ú�nڱC����&J@

rd��)��<w�6�B����¤��[*���޽�9����R��@���ʔ3�˻�z[fΜ�~���賩�~T�N�g���������l����h�+���ԁ��Yds���Fͱ���[��2�M��N�ܳPS�ѡA��`񛯺��x��z 8"d�P��Xi�>�D�;��L���񀄅��f�$&�ɨQ�2}z	��ҥ�d����M�Ig{!�gN���ۿ ��Q�t� &1�1�8�{�U)-�/%�%���"ј��鸦E���������e\ݕ�x��mmr��M�]�s�.���bo�H3=����{&��J.g;^{�V!�Z����{�_|��K����@��
��a,�3ʠ���i#�@�09����z�v?p�px1h��2o�,�>c*[&%&�x3CZSS';��#����W�Iu�#���2���x7._�.�7�x]&N,dfh�u��ޫ��Eg���+����ī�����V��Ο>� e���y�
1�7�Q���]���Z)���1�������@�[vO�$k�X�-��1!!!Q������ q�Չ�����Z@\�N�$99QF���I�'ȬYӤͧ��U��� �ݿ�P�\�!�v�3g�S�c���u���"��{ʔ"Y���l)*�(II	����L46�ɕGO��F��p=��䠋�ŋ����òg�~iinub��O:�C��;���c�V�j��٭�Ų�4����(�"�m�	aFD��rs�dڴi����XwuU��>zd�w�	2Dq@��9���SPƏK�S�51��j
�������;({��{�HCC�tvbL���|#l�ޒ�	�C���ȸqc9V	��Ӓ����b���po�����n�fY�_���o�S4���% G��������vj~�1��C7W_,i?�վv�.3�9�2C��b�� ����	�T�Ԍ�#ѳ���DF�il�1$PLDILL`?}J�@@��H�p61C�����h��B}c�&5�f|�Ebc���d�̛7W��'��бyTj
Q������f�(�<���
�t񪜿pAΞ�����ӞD���g��������Z`@�g���ࣾ��f��y]x��� $�>`4�[�/�Ǝ��c��A�|�������EFDq�Z��~Xu���J�}����׮�W�bk@���b��l[�k8Ӗ9�܉��f�~�̚1].�O�-#���p�X ��=���Z.\�(�Ok�I��4�P��96�oM�p����{c�����J$�}x�0��2y 4��� �PBC�ј���I��Bz����+���Hm�ꄶ��� &-޻8A[~������geز�v̱�{%"2\�d����\F��2��܂&B+sV�Q��1��ܢ 4�`�5`��U�Dljh��P07}�I�"P�J���3�)�cϠ�g!���w�&�`���N��<�&�~5ڻ��ŝ6�
�E�%2*\"y�мA2�(���#sS�=g]]�[D[�T�A�HS����;�	��B�7#��Q3�Ȝ�a F!�y`�E�4��]i�JL-���v�1]��0���_b&̓�6�c����V�&B��)C5��4i��[If�������3��W�v~���t��v5�ԥne/�!���d�L3C*}�\(���&Wv&�\�;ӌ0���c�T�I)��8SЭ���(����"�8�k�*��6�t3��xz�ն��Ft�c=F<�sr���X!e����#��)�^\ dQ�5\���y<��^�M�[����E�Խ?�czM��q,�^���ʂdը��"O@-B��#=s��ۢp���^�����,�c�x��br��N��Dn�fxl g���L�L�+��� ��w{0�mh�6x5���2��s]��N0��#�t Mi\%�e -��p����]#Лh�ܷG��K:��&����2�g2�7���8�k�$W�y:xthh{��=�2�!��QU�Vgif�ľ��LϺ�ZE����ri!��I%{��d�����RH���+�z�pO`-j�cˌ^1��:��e8{���J,�����?�����-�U��d��w�����4$i���_nkn8��盩�O�@HN_(QxT��e�$pYG��em{�h�,���_� :���1$�1��+��t�<�̶�T���g�0@�U���X�牙��_	Pa�nAl���{�|��^�׾�"��5�)��7�G�ɷSRP`Nm���ۛ�^Oa+Y�� ��$�#FWZD�ʌ^�&��>�@Z���>��}�c��[�o�p%����i��Є0��I!7Ң�[�u�v�l�f�I�d�������TLZ��[nB5(xm+���v��w5���q��[���$�$���$�3�Ӯ� ǹqj�f��[�pM���I .��oJi���u��n���� Z�u�FP���b�A>�$��sy	�{]{�r ���e���p0�P��%��9~��k ���������p�:�6`
���O��m�JL-:q��~%��-8��9Y��7�DC�A4-��@	\�A��&�������)8�?�nvB�z>|��V´�I�n�.h����6uz��#x��c[�k��Do��%��"DJ۠���ׁ�䏎�f��u��:ڥ���y>�jSx/������@���p��>�� �a��� ���6�������)z��k\fy�&;[��n'ecQx����s{�Ea�Sgd����X¯�jI��G� ��j���|<�Y�4A�-�QB���IW�_��'��0��9�g��9[�E3"H�G��� .}p�l�ʉ�{K��gH�����C�!��M�8^�ϟ')))l{��Y9w�����<\��	�xsh��f`�����y
��l���έ)�޿}�y� s��(\�E����zl^`'Fxv��#�9��`�}_�wo�׊o��1�^�(���^�-���PXb�(Q�H5f-X0O�y�-��#������9C�5L�%�A~��x^���=Nk�Im���Ԯ��RS?M�&��?W�=���e  0����1m���'5��"q����Th���������@��}OR6L��dp-���u���2	ؓ�5��4�2@i�����$++Sn�*���o���vISS�	#y��{�g>si9��%�&��r��%��n��?Sj9�z�w��~�FP���^���؟k_ �Q����ɒ%K��ޕ���u�|��g줌fQ����Q��w!� �"�]̬��c�WF�y[�MU�)�4��Z���H��˖҅��ޗ��lˬ_�E�n�ͩ�*y���!۫(B$�Kz^FeY�w�y�;��L�.�А������$���_����}�g!�D;O�v���Y(C\\���ʒŋ�i-%5Yn޼!�}���ڵ[��:�c����u�����N��r5hM����$i����*p�0,��bc��7�Ä�������5�Ö'|�ے��e`�l۾K�Mm���!��g�Y3�^j3�F��Xރ�9jg7�F5��hs1I�$��f��q�9���X�2OfpM�W� ?<.��/j��-p���>Mބ��S�v����CL5?�*s�3�k�6*P��]+�.�u�2� �l8�С`��"���4�8a��]�Z���N�-ٱc�<pDZZ:�]��������8IH����8���?����������ѾM_5>� �lӇ�5�
���$���Q%$4�B���q�Q��%�ϻ��e����W���dfذU�m4멏U`�3F��V��t=zv��0�}���8	:C $aD���n�`�/�´ۜ�&�ƽ�QQ��>÷�S1~墝�N�1%ŬQ@s��s\�D�D����8��6�[Z�>����QIv�a!�	��~#��J�i6�������6�OBAPLl,��MMM����u Ɗ�CO��3R��S$%u�G�[�p}3W�Y�V�we�a� ^��fo�>n</?OJP;s�L�Z��  ������P�"5�u�����;���C'ɄI��О��%i(xOL&��������RVV!�oܐ�Gu� K�	)#p8���B�S$����XPX?s�t?�P�����=�nih����Zimk���\y��e����ڰ��&�%���(IIN��ce��	,�G� ��(�D���
6�E�;�f��c0�k$"�P�����ax7����fK!�X'��K�C�?�
a�хK���]���{�NT��'�/���g;�ˊ���۷���;���CAY��n�͎�O�ɓ'��ɒ��.q�	�8��$�[�2SQA�	�G7�ֶV�z�
���T?bX��S�~���ʔ)SdƌY�G�(;~����W��IF虪=MT��0pU�͌�*���!�JJJ8X�t�\�4q<ǍBD��4�ݻ��SS]/7nܑ#G�Juu�\l���2mZ�������d.($:�`�Ν29{��ܸqK>����N��f�~Ͱ���    IDAT�-� P�"T����t.�ϗ��"�7w π/`��A���Ȝ.d]��� ��(���@s\�c|a��KRR"%�����g���K��,���!a[�@��H4Ӯ��l���ü��39��h�$)��c��j�cbHXm�*=Ϟ� G����w�������Y�L-�Ӧ�؂/����=b?R�㾫��ȸ 8<��ٳdڴ�2*-M�b� �ym�p�\�xQ��`l�L�>�{u��%5��F�P'p�_D�,-]"���d�]��p&���{`ɪI	e���YM ��؎��ٵme���li�,]�P
�PB�������V����ӧ��g�o�`9�<˗/c����IRrKA0�Ȁ,$l}����9|�={��δM�-<A� ]'�Lj�!�*.	q�z�*Y�f5�'j�;�ۥ��U::�i�DEGIWW;P`�5�fa�g�m�-�vP$%%III1�?�X��y�knj$!�0�b�c�	0�h�m���)��<a;:�ыY(�q��zL��@bf������͕�SK�� y1��ź%$&K\l��߽+�O��twL���0�-\��3٧�[�0�>M������9B�Ν��3g͐�_M�M�*���gk�D534�~gΜ�*%%5�����R�mܸQ6l���MRLh3�`�Y�l�̚5[.^�$��#G�sn����X3P�v���v�p�6�� ^���H �����䉅2uJ�̘VB���e�p�B=��T9y�	I��+_�%K���o�'����r�Ul\��I�&IZZ:%����d���<���;�c�A#u��)�#
�ʺ�^�eK�RJ�ܹv���>���N�0��F�Prrr�;��[�n�g�ob�P���ɕ���!1a�|C#4�y�������yF��Y���-�ɩ$�ɱc'�oG�:Z��lO�%��FED���&O�o���M�<|@������͗���T�֭[��#�\���2m�~\A������H^��T��Ρ����e�?��S9u�D�D�+�_���l ����k����l�ɚ|6�)4=�v����e��id�M7�?��<���翸�X^�uY0�������{d��]r��5�����$��B�!j����U��חf��KḀ�u�2Z��EI|\͠����%;+�v��-�d���l���B��W�yE�ϟ/c�ȍhHuFN�:�6% Ha��U�VrQ�46�ݱ}��<y��" �M�fQ�ڌ&;0+Թ��s�L�8Q�.Y*˖/�d������s�8����}>ddf���+V�stvV�tvw�wY�a��ܵ�������iS�7�-'N��{vsca.@�������/�9�����+W�O~/ǎ���%ѱ(��QH:2U��:ٱ����_���7�!ii�r��L�?&'O����A!aRTT,��\%'N���8ٶm��޽[***Ht�))4�`�w��EL�tv��$�<y�̛?��_TT�ܾU&��O��={v������O~L����O�=���H���F�#&��\��8K-5u��۷�Z M�j���7o�|�����x
�����lٺ�����]��q��)v�fp�p�@�y���T�J`�tXX�,Y�P�����捛��>�];wS�"�|Ѣ���w>���IT��wl�����w�D��`���/���ӳg�a����ʞ={���S����H��1�"�ީ������ѩ{P�@JJ�䭷ޒY�fIjJ�>tXB��l���]Ath��Y���pcoݹ#6nf�����3g�|���)�nݺ)���KcCǓM�O�ܜY�x��^�F��3���F~�����0�$/?_��K�8{Ï�TvPj߭��V�>}�,]��-1��С�r��	�|������I�e���2gx���d�=r��Ey�������1$j�{w3(�7s�LY�x�d��d��׿���ܹ���f�*����32εe�9z�5BݘV3~��Q��K�ɽ~���ݷO�="wnߖ��4Y�h�|���s�#���Tv��������������5��k�ߞIX�6�j�2���bl
Dx�.=$�_��璝��ޖ6l�ݻ�rQp0��5��?��degJ�#�od��}�:�M�m ����Ȭ9��o~S2�d���we�歲g�^IKO�)S����HF��Q#�;­�u�TǐА�����4�0E�w�|"����$���x�E�l������|����;w8"	�����t�"Y�v-����:v]�G
�)��k�1X�����'�w/|���h�"y���$}t:��	��	����R<$ew�H��r�
�:�X>���۷ɍ05�M�$�)@S̛�@�Ν'�������d�cǎQӡSgt��>��J�z#�����1s����K[k��_�A��w�z�y�?�����2�ŋ���Kr��;>|�0hC��h��׬]#mm�r��yٲe��;{V&L�Hs��7ސ��h:��?�@SB���I*�L�	��a� f���� ,!�٭4�E������|7nܖ�7Ц�D��#����$%'Hyy�|������p7}0\��1cF��Y���ޗ���RQ�@6n�,����12w�vfƆ��C5��!�!ᑌ�F��G?���\�@���g�0H�fM��n�̚5S���-cǍ�	���r��aݴe�hN���Ȏ�i�!���6��<�M�>CV�|�Z1q�`��ryuݫ�����&��&��,�S!�7m�K�.�++V�5Z.B߾}�aێv][ۿ�td���?s�,�f���HQQ��L)f�:�Y�?6薮�NILL��1�����&b��o�={�Ѽ�8i�����2c�4������?���e[y�-W�ޠ��`�at�hY�hM��Q)RYyO>��Or��qNہ�ةG�����c�w�>=��Q��!o�IL���9�ad W
c�A�کMM���f�xO���dq�B���ʭ[wd���I|�a5@ ������o"ѱ�r��Mf�!��H 'M�>��Hg����ߗ��B� �d���2&3Cfϙ�	�  8���N���, ��Y3g�O������]�vi�����	:c���,�
�>�|�<|��
N�\H�s��M��@�3�\(��e��_0����6�nݾ�a{�K�|���ilh��{�m�6�v���]��?0+0߸���BZ�B�u؞�� hU�1��0׭[�$4"K�]ơT<�q�G����� Hrr�L�:U�ϟ+3fNc)�(##څ�r��iٷ� ��"���ϛ/����#���M�6Rh,X��&���r��ٲu߻{O��a܈��ց_�a�d��U2������H��1�De�,Y\J���c���O�$;��ɰ�%���F~��IbR"�������es
J ɖ#s�̒��z[��r�N�=ٴq�l߱��t�=�6�I��$�RQ\��J͍����D@��W����s65��T,yx8��ؘ�@��u���߸���&N*�X��T��e��mr��Yj3�b�&���I�̙+��['ӧO������4�nݼ-c23���H�L�ր0�����4�  �u��e�f8�0�V=�����"J(�+���}/�����775�����������p�6�4�H
�ܴi��ٽ��0Z�T�.Ǎ͗������K�LS]U'�/]��N�:���)%�ͷޔ�sgJzF��?��*���gI~�X����_��?|��`~N�7Y�\��Fa��X[�Y� ��5y�d�9�Ig������,*������ !484hE�4zT��xe�|�I���Q6��(��*U&И��(���d�����,�/]c(r��}L�[��&��b��jՐH!��}��$8�9�6n����݊r:��. �G^n.c�o����΀�{G6l�"�ܼY���Ĉg?r���<uB�\�B�w2�"��0G/Y"o��&���G��?��>����L��݅�С%nJ�}��X��X
tw˥K�������"� _4�,�x�U�԰)\D޾���<'S��ӧO����+�0**�>̒��{l���-&m"��_�ˆ��œ��h��D�K����/���ؾ��f;,X8OV�X$�gK}�#<ƍ���g]]�lݶ]~��?���B�TB��Al�D��+��f�����K�Эf�&����D[�������鸞 ��th�ۿЎ� ��(ַ�yK�N��H��S'I�JD�/z�Wd��%'B���s�Dx��EiiE�L�=	�+�� ¢�z`�gΘ���"x��y�^G��*����G����Y�x�L)�x:2��C�ܽ�I&8�}�!�����Ɂd��=R__��,%ej�L�0Q�/].�V��X$����W���:x�k�������C5�G�lw^_���\y��;�c���IGh��1c]�$b3����	�,Y,~�����2�t��!�xἚ�DC&y��73�q�&2 ���)`6�41w���0Uc��|���%+3O�����?��y����$%&r�7����{c��s|B2'a޼y[v��)��l%^��6#�}���� �	�sc �)4��χN:�,Z�@��?���Άs{��I:�p��,#R�h�,^��LP[[#׮]�(E�J=H��������l޴U.\�,��JG��uM� 3�$9���:"�0{�Lb����{��>����$cƌ���n�SV.���$یD?a�|���ѯ ���#G����������p��p�/��h��
���G����>4����7s:���I�X��q��AF��B8����G�A<���3�6��t���{�W�|	3	N��6*�&������y�(�������A�����imk��+���I���	#���7������˽�U�~�/�Ŏ����i�+���Zy�7%� G�a�I���ߓÇ�1_d�#�.5�J��֚�l-IPR֣���g5��3��m��\8o.C� Z�Ԧ�&tF���K��k�g��ղz�J��a���C/D"`Sbӡn���O��-���\H��䖽3CAc8��fJ
�@&uLF������z�*Jў�nC}�ttv��yXd��R�gh�m۾`R/=c4} h<$r`r��� ��ÞNM���'))�pܿ� g~�ك��pe5stq]�V��05 8h�qc�Q:ǔ����"0� 0�4x�$����18ڀ`�=�pii������|h�� ����	�gA~���}�c}��f��0�9c���x��P��[�HX�yڨ4ihh����Z/ǎ���.�]�����,���X%Ӧ�HvN��������O����Ra2�KqRf��]�A�p��3�Zf ũSJ����at&;��h�s�Q<v�$'w�VHL,����'J�K�'�C�F}C�<��/W�]���/ș3g��)`7؆��KE��dV���Gf=~���ɼys�tQ��3�
6�-Ό��L��W?B��b|Ѷ�_Ȟ��Y	�/�d#������9�t���4����i�o�;eer��a9u����<d�w1X��E	��df$�NK#?3g�$C��ZtDM��t�/2�w��5�`��K��_�3��R�_hB*�1ѱ���BF���	��'�Hww�L.*�+VM���<�(o��=]4�n\�%�O]�c�Nq���1�'*\,�)�V/������B�h�&]���>!�f!�i*T��N ��qi��� ��(��m=o�l�d	�qt��_�)�N"}��<
F
A@L�<����t�.M� E��y����D���rH�s4�Y*c6��T-�2�Ȩ��%.X��E�>z4ZR���Ǐ�8 t	�	D���8ż|���Q��-�z'�'jPz��%j��rŀs�0�6ͷLPAa�.*aI��`�k8a'I�I�̟''LdD8�_a�2�� �p�I0L�A� A�Q�����6s�L�D ����[~��x���344�F��ɺ���W �M�0N �ORR�h������Hu�#imiW�3�?�d���t�-^(���ˣ�F�t���P˒�y�;?k�Q��4�P�����c�������Ȳ>|X#�i��!Ӑ]8M���,�&6%��1@ 5��A�&0�
s�y�p���}"�F&�nW��h-��I�R;77�Pb���@r����D�l U!!!�R�Ӿ KŌ+0��)�F���V�	�� �557&A�f�:܏�M۶g7A?@8�O$���s�Nׁ��c2�;2�Xk0]C�¹�n�c�)אb/�������qAkjl��Vy��IA����i�sܻWI��%�Y�t�QB��@�D�����OG{k�}M1{�tY�b1 �!��=p�l޲M>�2�/�tV+¸�&4ژ�+����>�������v�]���rA�q�v<��]����5��6=� ���z�/��)!$��.x��T{J��f.kX8%&�k8��ڸB���P&*�@> |dJ��2�}�4�$��|���%rHo�'8��1R;_q;n�&��W&6�N'�}"}��ch3$�x�Z�F�b�x]�Û_��p��@�cp�D#�lT�T�9���3�o2�l� �� �n�Zͩ��Ӎ����=v�g4�pM�i^�t���)��w�~9p���|k�����C��u�da�ן�2��)Rg+��������Dl֝�S�s�-�C�/�9:;W�D�ùS��_2��J��T�DZz�ddR�=:�`���[��d��@ vэ�a��;��6�r�<�,;�����n�ok�3���&�5@` ���+g]M���a:��C4F@��6HS�:n�wO٥�U��Sq,RU�&������d��a���\Vf&����Yrr2�3@� nܼYN�8-��WJ�	3�f�=�	V��&���� $9��}�1�&�4݆��װ�N��?uZ-hE$Z47q|%*׶w�'E�-�2�-�QiiѡV�6�}�_�)��D��m�Ό7�������Ĩ������*uG��d��*���ӛ9c6�k(���'�s�wfьb�8o��9�٘��#4��!C+H�j���BɵB��㣠���
;�O8�
.>7��<���o�\�������8(��	�����W�2���5io��m�}p��Йm^��ׯX�\����	(;��]If)O��)D��B�4�,.7!M��v���24]��xc��jS��&�q��Z�h�����6���U�j���4v�՜ۡC����N�T��r-��3�d�y���p�
�����='M���*�!�x��(��Vi��N�Ɂ��:3��'"kf��.9��:�fc�������5k�
�@�9�Ј�!@PE4�5w���6��÷�A�6��>�3g��	�i�r(�D0pcXHm�Ac��!ڽ*�T�� ��fVW�NC��ia&�� �mv��J>/��&�C������vqzi�k5!�i��=�E�SeA���M��˘2��� �DX��j&/�D�H	N���4L+Z��)Kc�̞s�v����h�R�(�(t���LK�=�}��|d8>CŇ���_���6U�����*����ɺuk�����B�5�/]br5���ևԶ7�ɲ�	�1�
���3Λ�5�݌�U\�V:��ˌ5N�K��PG���+=� �`��6�e@w��C�Ĭ���A�iT��6����bm�V(�ے�HX���9�Z���{PigC����ŏ�&$(#c�H��V���pυ6�D��o�昭=��)3�M����_z/*}��,�)ȷ�8��OX��Y��,IJR�L#�:`�z#� [{Ɔvb%�ޗwʏ� +|�@�3��.:2�f�ּ�Ya�䴒�6?���HQ�!���D+(�x	[���{C����%
u�Trjt�F��:j�d�����3=E���������AR��+ua˺�nn�+F8�� ���t�#�bq1���Wꝩ ����SgK�gc�62��i���o` �ߠ	��&ӪcO�0o��:�`z9#,|  �IDAT��qi�Y ��:� .%������(��0V
�a-,��Dm8�15�-U��d~�Z�?V;K�~� DBXYanќ�Kn��Z�ނ ��V�[{Z�Qm�Bް�|V�i7\���d����d6wfC�V1id�4��D��@*���%�ky)L
z��c瞩)�B@M�[ I�6ԥ�bs���d"U��ڝC�Q�j�����߇�L@ǩ�pk�т@X��m�d�z<�Rx�>�����(uj�4.m���`�3|ڶN�H�į��e ��mǴ~i��}V�{D��m��+�ݱ�.<�D�����d[1�I��͵\��F]�5�F��o���7�瑭�h�@ϧ3�Uԙ�2gV�i�c�9��7��2���L4zf���3�>��pf?4��L;r�J��֩�h�W�ȼS?5�>b<<#AN�G�|5+F\��g�Z^�0�j<������W�k�Ox�H{;��麨����n��"4� V�B{�־.����~=�zR�$榻�k7k�]��%���v�d�L4=�e
���R*�I��$Ӷ����mdKd��5r�C�P�1��n#3:0�65���1C��겣Gk�_ѩ�c{@ٵ�Z��3�|6��f�'�kp�q���hf���7�H2�mM^�3�cax��@͂_ �SPU�B3��N��:��P�^��&���ut�J$1���Xs!�	Z�����9s�_�a��l����z��h �pmR'ɦ1
����(�q8L�O�̦c����j)���l��]_x�����ײt��mD��>���ޫ���G�9l�Uc��o��X�����JF���@���$�}����z�R�j^�_�.�2�f �F�y���`��y�~�L�zI���=��U��q��O-a=�+��0([�H���O��ݯw=\f���Wz������4�۳�_k|�!�A���z�6���=[����@?�~W��?��#F�T�'�^����j�S�D���>���Cz���y����
�0���i+�3�H�Q�y��>i���G�
�0�v��!��� CZ.����>����gH+�3����?x���� #mG���
�0���i+�3�H�Q�y��>i���G�
�0�v��!��� CZ.����>����gH+�3����?x���� #mG���
�0���i+�3�H�Q�y��>i���G�
�0�v��!��� CZ.����>����gH+�3����?x���� #mG���
�0���i+�3�H�Q�y��>i���G�
�0�v��!��� CZ.����>����gH+�3����?x���� #mG���
�0���i+�3�H�Q�y��>i���G�
�0�v��!��� CZ.����>����gH+�3����?x���� #mG���
�0���i+���"��    IEND�B`�
```

## assets/icon-512x512.png

```png
�PNG

   IHDR         �x��   sRGB ���    IDATx^�	[TG�>�컠".���I�������ML�&�l" �^�W��9(`�+'g�9s�Ɪ��������_H $	�B}%��  }5��!��@H $@	 ��	�B!�>�@ �>�x�@H $	 �9	�B!�>�@ �>�x�@H $	 �9	�B!�>�@ �>�x�@H $	 �9	�B!�>�@ �>�x�@H $	 �9	�B!�>�@ �>�x�@H $	 �9	�B!�>�@ �>�x�@H $	 �9	�B!�>�@ �>�x�@H $	 �9	�B!�>�@ �>�x�@H $	 �9	�B!�>�@ �>�x�@H $	 �9	�B!�>�@ �>�x�@H $	 �9	�B!�>�@ �>�x�@H $	 �9	�B!�>�@ �>�x�@H $	 �9	�B!�>�@ �>�x�@H $	 �9	�B!�>�@ �>�x�@H $	 �9	�B!�>�@ �>�x�@H $	 �9	�B!�>�@ �>�x�@H $	 �9	�B!�>�@ �>�x�@H $	 �9	�B!�>�@ �>�x�@H $	 �9	�B!�>�@ �>�x�@H $	 �9	�B!�>�@ �>�x�@H $	 �9	�B!�>�@ �>�x�@H $	 �9	�B!�>�@ �>�x�@H $	 �9	�B!�>�@ �>�x�@H $	 �9	�B!�>�@ �>�x�@H $	 �9	�B!�>�@ �>�x�@H $	 �9	�B!�>�@ �>�x�@H $	 �9	�B!�>�@ �>�x�@H $	 �9	�B!�>�@ �>�x�@H $	 �9	�B!�>�@ �>�x�@H $	 �9	�B!�>�@ �>�x�@H $	 �9	�B!�>�@ �>�x�@H $	 �9	�B!�>�@ �>�x�@H $	 �9	�B!�>�@ �>�x�@H $	 �9	�B!�>�@ �>�x�@H $	 �9	�B!�>�@ �>�x�@H $	 �9	�B!�>�@ �>�x�@H $	 �986�p'��O��t��Q?��������A]&�v_��V�ޏ�i���pwx����:_ �K�qݐ@&�^��,��,�^>J�|�h՝~�]4��i��i�:j�K�v�G9g��s �7��	J�����k7	|�%��G�(������ p��mep�r?��  'c��.O��.<�����9�.~�\^ǟ�v�N���jGwT[	�;I�Ǫ���ݶ����B9�}�~> �{�|�?j�|�� �Z����8̂s�D�{}_*Y�[�Q)i9o��݀F�=���|-� 5��@,U�7U�3��P#1�ߨ͉6���S{����n��=�hW�v�a��︭�Ώ���n��u-�����,f N�H�s�0	�^d:+rX�P�x�_�%�A@[%]ù�&J\�Q��Xu��e�J>��1 k�uM��=�����༪�𵂁b6��
�(�����δp}���Ȏ��ʟ�����97���9� O	z�n���3�o7o@;������ �0��{$�ny< �Yٝ��W���:]S����*���}%(�_���t�N�T_=T�n�?����+���
��؂��,9�� >�X��ϾWx	��0�e@7\�&8%/����g�G���2�h�v���~����Fcp;)����^|�N�`�҇   �i�'�'L���x��E< ݽ G D�{�P� ��Q�����)�� ���
�W	'�#)�^r���B��6>��� @<!*SE�� �t�߅�s���!`�	�hNѿ®��7�D����Co��[a���Ac������Aȯ1�N�r���3'l�)n7 �����+�O[XD��b�� �\�5��.���D��FZ�a�m`?�y�K�WԆz��E�v�*��3�R�����YєrM�Na4��N	vP�z��>�rp�O����ݟj�ζk�Oj`�@��h������:ռ0�e�]�ů���.�� �B�]	 �y�o�>C��E�\轲�(o�. ��T�gz� yv֦����U��Z�o6%+�{����5T�}��"���^Rv��6mG��	�JCZ�/�	�({�\vr�b��^,l�����AR���C��ȅ��f�Ӑ���\�ٽ�VZ�|t�� �]� ��T�"��/��MWt���]���۾V�G�pM����ZE��b���^zIc�Sg-�P���~6ѱ]�+t�\��nf�gng;�����"U��'��m~yZ�Q�7Μ褨��%輅� ylJ(�1��`�FD�/��ʋP(c�1��  r(��� �]� ��T�"���Y�ޒV>}^ZOF$#E @@ (���!��ב��9�yxcn�-,@o�fϠ_�2ʀ�~�Ǣc¼��m�ᦀ��{!���e�n���1�B(����KU�� �}%[�ʔO�q��	՛%ɰ���s��
5^����A*���n�O  p�jl? @ۥ* @[I�q!�/"�&�$�Y��H�]* ��a/@�AV���n��Kд<���\�9�-yV>FF�@�3ӵb����t  zپ��a!S�f�{N���2Y�%�5�:�*�{��� Е��2: 0g {&
�I�]<DV,�� x* �tHT������^�/
 z���Ȃ�UO ૊;.(%P �
�״���R� P��  ��������6�䢗p�T:c�b�f�g�4�.w��t4Vgq�H�Ff��[�M���[����;ٸf!�O\
1��g�Z_�-����K��N�t��!YT�{B
 @^��|d��Y4qE"-��!n���{��@��� ����m|/��'	�'�<6O��~ ���-/ ����N M�S ` $gx��`�/)tZ2J�ｺ���X�c�kTo�e!�)��;���5昸�q{��ֆ;\��鵩��j�n�ժ��sh���[&GPjh�2%��$,/g{Gh�R;]��*(H�xK��}���vҮ��BЧ̜��֏�� �ۈ����J `ʟ�(O�3�9�ek�N9� D�3��U�+=�=	I�ypb=fV�����FT6 .�!V&>��0�Â���]:3�*����[�
��$Sw6�)����:O���xs�[�*Sw��MFE�Þ��-�I���r��}�|�P���z4(�P��@;��U�+�~;����;j?-N�� N� ��|	��|��B �_L3vxA�*�Q���?�g  ʊ=�P��VnT�CE�֬�/)H�(��^<��6�F�� 0S'�y� �U%A�������;r�h��4�S�1�����g6�1�垛nz�,���P���c2�w=?�)k�ȿ^pH��U$�!��jsV�C�4�����!|��Ȍ�ɞ15~��r�G�O�����W �'_�ؖ��W�� �A j�� ��Y�N��Ջ������1l� �E����K  2�r@��4��抰��}���y��Or��(�b_20J�$��������"L�|�:�
�=�v��vi�-u�0��ˎ�@ȑɋ� �������5"���|�R�p�Z�G ��U4� $pB% Ɩ0�ź @���\�93P�j���(�{<?+���Y	8eA
�ٙ��zP��%s$5qhx('ؓ�^JWe/V���`J���A�� �.o
�n��:��<Y�l��B?��JR젰�o�������K?~L{i�|�R2A��k�,\��H>	�� ��.�N/��B<]S"ry�I_���@��o�O*u� P
�<
H��p\�Y�d��19ۺ�;A �^ޒC��N���8���o�[�͔��`MJ���C�Îl���E��<q<�(���cT��Y�=��j���@�mt�����i �0(xzJ���=�=�FGG�;���:��jLwR��u 1{�l����O{�{TK^���F����:��~��vvv���.�wv����q��p�}�eY*�A���A+��)O_`G>+~�9��.��/`�ɻt���9���� ��{��x-u�BH���V��� ��
�8�0�@� ^�Zsy(��s��*���âR稸��x�
a��;��M_Hcccitl,����kP�F�+xP�# F #P��H�㺇��p-{V��f�>TOl��;<+kP�ޢ��|.``o��և��o[�igw'��0 ��Mww������Ί�vM����x�
 �N�a�$�I��j�4�y������ю�+���8P�kVw'Kܿ����-��?������� {=7��eɥ�¥b0���V�^{�O���t X�-���o�8�����d���j�B�*\Ģ��+�k+X��i||<MLL������K�c��0o�h���JSS�h(�Q��tr�z���k~o�c��%�Ǐ��zww7���ݝ|-���o�����������>l��m ۸���t�(E񻘐$�XU�a��I�i\
AeL*Gr؃H��Vd��8��U�ޥ����B%,vc���R8Y<FoH�a+�Ͽ�{�蓦ʯ��  }���C�����Tb�r�x4�t����ݬe:`�o�����\ܸ�I�c���o#2	���x��|��-����  &�` �  �FF��ml�	  ��lݶ�; �(V�d�=V����:Y��zg�>    >"P�c�#�a�+�-[����B��� � \Y�O��7В��J��2��ҢA���'�_�{n�s����GPds�� �]�ا?���y� �sV�<$0�m◑����xj�4U��ؕۀ�  �k]��		�����=wc#��1���ɏ��r���$��#��vI��Y��&��W �L��u㏍�;�6��I��+b���� p,�0�?���#02L�= (��%���p z>��F�w�G��s�^B �3  ��8@J���mT��Z���fς�DG��o 2���m����d~�9_� �e�`JA�#�BNR�=B�`;[����
x� J�����IAۃus����v��JS>d� �r�㡏�ʎf�T�ZPRb��e�W�a���kvX�(V*�q�^��I�$�����GD=P�䢟LS���'��X�W?���$�y�����`2�8F�@@d
 ��8 r����L��%�z@�Ӟ�����ψ(x�� �P�`���  � (�m&�l��띝���V�ڂp�Vz���C�|aQq^}yk����gr�=j�3�C��S%�H /cT*���'���,M/@�� ��Б�9:�+�3'�8�_�^ |��YC-%��?+0^�J�ݯq^���6cBwv���z-ʲ�pZ�	�1~p#a�)���4;;��f��~v�L�d  {����G��� &0%@��0���l�d�@� (.�\��Q�5���s�T���ǖ.p�޳�%���(k@3 {`���ܷ�# ��#�ɂ�z�(|�೭������lkiss�b��nK�O|FQ�\�����xz��=�\�L���O̗y   �ʼӲΌ�����c##�T����B �����8�����]����+�0<$���t��տ_$����]��Pz[B��m)�����h�>+.�6+\P���w�����t~�|�?>�?.�ϟO333�M�333�@�?�	�5*sR ��)�� .g�;ӳz:�3�E�O�Չ A��ZH����,��\?�?�� ��O� nQ��{T�@���H�z�+�V���JZ^YI��+imm�E0�)�eI9jr&+.������(�� ����F"�a�	���u���E���^)����x
>\C�T��@���?� �Y��piű!�#� �����9��Z�r���=�������b�exA0@f�?DAH�at��˞\�@�#w���l:w�\: ���t�< �iڦa?�^ ��� ��@�"D�I�>�t��7ܽ���R�������YW��_��X�h��<�2�Etds����'!� �Y�Yp�=)�͍ʹ��� ��w������q�	�<`��� ��1�o�ˀ@?�= V,��f BR ���@**v"}Jx�g�X��  �E ��ꏡ�foO@?� ��	V���ͭF��&Nъ�R.�,_��f��x���C�����ݥ��P������49)~�Hy@����3gҙ��Ϟ� |\���@���d�=y���f�Ѕ>����"/`�1A|�(�I�*
�m�T:�Ƞ�#Zņ�,V���Ҁf`� �Z( B�t��a ��w ��Z o1����%`� xȘP��.�������
��}@@RI�kpR��_�Ay���2��Zyr��5tS�=��j,��}� p�(n��K m�ڛ�����-M���_��լ~R{t��(&OD���}� �?7���	P���yO�P��!L�$@&���?�ֈ�#�z�3y=oQ\�8�#"��cg���� *�J�)h�?3`��U��A!�H}��R�N@|�ũ��%�po�1����667���E�ǀ,������(����1	����" ��,�{� �SF	�4C%��&����w��gUx`?��~� 8��%��K�@�k��̰*\)צKhV(��@�B���?������!�a�B�������ٳ�E/�P�Z�R���/�K�	�cˮ^������VmN�ب��-�%y�R���
ʄ����?̬0)�ʨ�.+.���RZ����lZs�
i� K� q���jZ}���w���~������p�8@@f�P(\!�i(ʱ�=0S����UZJ��*<	{93�����P�&��vm@@� �  �Y�ؐ�QK������ŧ(Σ�I�ֻ��{*��黶���X����O)w�����W����q���t��|�?(�OOM�[��ia )�	yLz(i�J�#��S8�c�= Q��I��R�\���Z����J�M4#^��ҢsL�E-J� �⶿��޼}�޾y�޾}K�a��Mz#�y�aj@��H$b�z9���L
�2%�4�U��������Ue���o�{4<�M�^�5B���'  �Q/�q���a%�L�|Q6 p( а��ҟ/k��)����C��?F�~,�C��W�\I��W���iqq��S��7w?T��"Db1
�O:�g/"r[a*c��f� ��c���"�A�^N�Y�dj�<h��BZe��^�rk6�Y�D���;"�A���%�޺�KK�i��RZZ^B>K��dH@�
�k�:��k{.�����F���Bb�����W��4'ϧ���_9�i �X��!��� �}���K�r  ��,�������欤�ڱ�nc�j��o�����I����p�<�!�_���E׾���2����>In:SE:b��^�~���/ih�2M�Xw1��_��y��B:+�ݓ�4z"�e��.~��O�U���@ B��mm�_����5L�אY��B�>����Ž�l�mi���.�V�)�-N�N���D�W_��LZ+��^��� |�������| ��Xĝ��J�c:��؜ϔ�W�z:6|$t��R�Μ��4�������>���IssT���ܩ8f)��f��1�Z@�pS'�n��:��o�N��;��M:�灿 �/
-S�s^�q    IDAT��ϵ�Z�Du��Cr�0�h���Ha��dw�'�Aâ�}J�FCRG@R
��b 760k ^��������N�ؓ6�b��~t�' �����	 (J����O�i�נWsx됮��;�mi�@�.���!��%�Ȉ"�k�ʔ�����-���>A�������ܹt������9*�#�Q lc���>ґ�:v��t9��/X�xz>��c�E��E��\(�ԞlYq�䩉䖰�LHu��_�.��7�X���8Z#'���5���3  _:R �3!����k�i��H
\�ZPLhɊ
��oric*q$D�����%�DPi���Ȅ���<��⍩�j6�M�0P�]C_���S� �]	|����؈��c��.͢w$g[4� <����SS��K��Ņt���t��Ŵ�������i��t�Cj�����).�}�����%ih��� ��_������޵�?p�B��B%�G�\�y���!�|���e`@���7)�=���Ch}S�D��G��T�Q0o�Y�����o@\J�^�N�^�N�_�I/_����.w1��D$��/y����2��(�,s/s�����6��'� l���lb�ZŃÞ�x!��=>qw�\��o.��" }�  �
fF�f����,�k�}��nP��� \����~)��|�; 9��0����exY��
�X�%��o���
V��#�����-)����8r"u0�I�,��8:(�� �zH�_�E�K�S�ŔA�z@����e�///��oަׯ)[���� � p�S!U,C�o%6]�2o�)Hu�T��k�dj#G�}�X6���Ϥ����I N�`ƣ�<	4@^��r�4�xL����;Z2��O){Sij���������7??��b��� G�X�4w_�Đ������_�D~`�Y ��0Hο�n蒾���I.�>_C�������,l�؇|����\��o�YV8GB>�@�H�
�_<�� ����zZ[��zZ�~�ZZxI�!�CA���
�ȥ[d0vr��Bcn���v�R'�s7[���׫�  ���B���Đ�[j�yW�d����oH�_|�� ����L��H:5�q;G��1��x �8{�����m}!%u>��y���x���uY��������4�����"A���V�5H忑T�:�o�:�/��BD��@��`��dA_S�(��i}�mPZ1p���)�������� &��B B� ��R��C{6m0� Q����cȏ@�={7������j
�C5����^U��֜� ����!��@+	�J�� ��7RU���囸
�Ʈy炧�1`�ޥK��˗�e��_�����O����ҽ#бo���`���YS9lqdr\m9�/j@lV̈�ּbm:�`&Ӻj�JL7{�Xݾ���)���b�����)Qt.l�X��)�Th��j�uy\�=Tc_� ��*�@��C���C ���v"����/��/q���	غ���o;��y�Yv)͔�zDy��x�Uֵ��a����C/Z�HԳ?���@��f=� ��b�B�%��6^Gf�0/�RT'o�K�_rX�Mk��Z�5���7�,��ׯ��7����H�������c�2&�[���gE���m��j�Nae�~F?W������*` �XiV!o2$�g�a��~
��&���y����7�1��)rc���U�k�c��� �IUA����Ԋ��< O�<I=y����_Cx`��?@�AD�LȘ��(�D��YP�ƃ����2� l�5~�,�� 8hd*��O ���Z	��@�zw�(A)����X�X�
 ���~�������"?��e|�]�J%}�]E���$�����G�O���󂭖/��U@�*
O�3�M��R��u�Z].Z�Vv����+ `+\Lن�Z0��Z��%� ������ %�x�@�C�����/�K��B �.��?��?������s$Z� ���>~�4A�`A�(h!��#�! 4m��#=t  �|/��gV�߯f��  �{����9�j1��B!��I� �o&�q���ծB^���L]���/1���t��4��">�� �/]�����"8���(S�y&�(J9�/��S0@��� �������P;'dy�\��L=�kB3�Y���L������?�����gM�Ip� )��=�6YD(a���'yc����B�?��
�,ss�wTm�>p����1� ���~l�ᒐW�V�[�����{��\+dbt�U�)�l pȕ( ��G�>_��#�Ėq��ZR��C�WN��Er(ŏ\��=�Y����!���<��=d@�>h D��� pn~u���w��J�;�k!߼�n!autR��K�)�H�����n�Nj�{-��-J�B����+���$ꔿp H����;�h\��PH*��k��R� ���A+�:��1�pii��'�����\��
�������3�TN���P�9�c��<9�h��� �&��+! �cx >5�3�)��V�,�{�V%YQ�,�Jʢ-fq��U������@���=W������ʕK� ���������4�����p���������^��#�O�ǋ��A���U����%g���9iӹ���S�K�$�UțAX˓���|9�Ѱ�u� �pc!$
�%�؆� H��Ɗ�T'���.�TO`��@ӎ�iwA����O�q���I$������ �<���g3( �!�  �X�|	t �'FIR����y�w.TH�><2��}F !����[���[���[����.�?.�Zyo�S�X]�1�*3����P�J��k*�̘���z`@��ј���w���1�a S�&�|�7 =������g� �|�*�x��/_a��W����5�D��wKe� �X�����Z�t�;�g����+�	��!���ů0 @!�1!���@ ����ɯ'9ed�cU<� 0!��&'��k����k�������k�ʕ�ib�P�[��#PP�{M�b���=st��;8�����k�WU{Ǌm_��wc��l������' [��4lh_�H3�� ���k����k"
�����vi��>晠�U`� ����k�(�! �'��R�w
� @�9B  �p�?�cu��ማ�	4�X3M5a��/ �?�9+�~Φ˗)��
��_���ѱ�41���466�\���7pAv�x2u�Щ�F��<� tR���DJ`���_֦�YS�����s� rd�����\��ވ�~��4�6761���_y��<y����)���4�z���q6�^I�<�n\(��+0(�ik ����ϩ�'K�
�3�l���r��v&����* ���x�%�ba�1T\�d�ץ�h��i`H
$n���L�|��*|(�
~�������9����\��a���9(@{��A��T���.���	 Ч�1�|�3�[�X�K��W��uO�7�U��݇�D����0濹����ށҮ�B=����D��°�H���~��qz������`�� ʟ�QH ��t�� rVO��������	��͙
	���u+�Ԝ �� 
Zͅ�uP ��5^q��B]  �I�"0 �f|�����|oݺ�n޼�n޺�{P�D��m� `Y`܄�'�j^�\����k��1���[6v1�Wd8GM����: �#y�B�	�����jE��X+,Dǲ���p��S�Z��9W�J��o'm�즭���������҃_���>J���(=���40 ��@��  u)<H��^K%@�N_e��>�p �[c�@����)��D: �_���: ���6��$/I N��Ž�P	�*C˓�4��u�Y�T���K7>H�B ��������wӽ{�x+�MM�c]��ɉ411�LQ:N ��!����rb����m}�l��y:��_��"]�� +l���6���b~S�cI&�jz�@�	V�d��[�`_,���'�Qu?v�`f����H�������O?��~�����׳48�����,����  @��k��Y$��궰׮ayzyl̪��Q�GЏ �E9�.�Zտ�s�d.E N��]�h	� @�L ��� @�?����a�݇��al�{�;�;�u����Q�8��U����L ����X�;����xz�n�.\{�yz=��A��cS������0`���ҿT���'�4��"�=��lҹA�oA{���G����h�������x � Ɩ< � {/�|��Y�x �A���ϛ3��h3�DRzٚ��9B_)����^l��| ��;��d�V>�i�`���j����}��<�!v�|P����� ܸIl����5d�#�ol$��P�?�ꂝ����]3{Y�~�c����*kg�w��:��|f�"v�Lb�����e�g�U3*]3�4  �(-� �6��\*
��dA�o`��ʹ���{�����c������O� ! 
�˧�T��[�ZȁU��=~�N��F@�[Y}�F1(���nTۅ�� �)�8 $p��� `@V���M@ �����yf��?� `q�
��-.^N�W� �I@����W�+O-�� 5-�]����nYo�u�:g��j��[�V���\9�߻�;ٔ�90��)�������:��R>���B��M͏�����߭P`� ௿����?�b= ��e�d������	yfg�B�b�  =M �qh\��j:���ʓ�uk~�VS� �Z��ɖ@U�[���M�8n*@ ��`�����p��~����~�CD���_6��w� E�̆�%���#l�j~�J�#K ����:k���W�k��n��wj�hz �zU  �"z�����H���^���ۥ���2��.a�gϨ ��߾]&F*ZK�� xO6�З*�ZF��"�r\rw��#O�1N���M�_�PX��u����b<�ɒ@	 �{�-T5@�`)��>t�߼�.��/P��sX��ٹ44$)|�ش����s�V@�DV:�u��w� ��]��-��k1)�T\#Z���I���-�hH �Gg���s�3�q(y�b�`�z�� ��
������P���l���(�5#"XB��ZkI_���OU��YȠ�p�:���Jx\��y�?g������! ��������2W�d�i�������L�L��׮b�?(�{������=3�{0�i�����8������n��gU���?|��^|� h"�� -3A��x�Ӟ=��}-���B�4��3c��{iii9���y�������/T�> �@���'��{��Q�$�����hga�=�7�^%�G���.�ʿ7Oӊ �4�f<ˉ�@�ȱռ�����M�I,�;���f�ի���ի���+��ի�ܹ9+�Ǒ������_h�����N�ϱ�qm��f�k�_���aA@�3v�P���7Y�9��R��?���'�0�(Ri-'�Ea<[�?��CW@h��������������3�?y�޽[K��k�� ��r3 |dr�C�< �<pE&�|�5}��/k���.���L
��@�� ��5n2$p�$PuDb}�'y�R��A1�9��b��E$�]IW/��W�`w?������q���,�*�R��V1��F�B�㶋�;�YKe���v��ڍ�a@�g ���53�^�z�eoE~h�;��p����L�?�%�z��O�G܃���?�J��g���'�?�L��77��R���?�`�_j�s��+�f($W�b ��9X�FMa5��ʜk7��Q�9G}����� |]y��B���3/4�cK�5��a���}��G��/��ʥ43=�] ��J�+�q�_t�����++	��"@���Ǭ�z�ͿQ|��-K����=fQ[��a:_�*��{GEN_�v�[��8X,�i�:�z
~ ��w���Ǐ�����?�~��q����1���&x{{'}������������
Y���� ��Jw�$)�e��8H @���C��Е�����9k] �0Hq��KV���>3$md�,j�C����q!]�t1]���.^���),u4�p��
��0  g���)!KMR��\K��+�Ⳏ��OY�š�+o����'^����j ��%�,��� ݻ���n����4�^�${ ��Y���P��ٳ�ӣ������G����>D� �
>҆|V��#��C�\��Yɨ�XT�����������k`�<d�_ϥ��H��� �q���	�Y�bm( �
k��~p�b���H���? �s��&��� ���Oֽ�`�-�JTC�s�Wҵ�0u��+@� �/@�E�K�t8C�D�&o�0�z[��E]5��cćܱ�đ����KE6�����T�?��3���_��㏿� %~�'���t$�:I��Ci��411���'��. ��~g��� �yB�ʼ��覚��x�?�\$�9�v�9���e���q\H�($� ������A��!��7��~������b��9s3��%: R�X�xNy��xL 
��t�M�}�N�n�;�q�.����m�> ��6*�	�%���Q?m�+��-o�g�K�/>lo���崼��Lx��ŋ������?Y��'O� ��(MMM��ٹ47w6�������	2������Z���DP`�Ǵ���%-9�3�e����8���ځ=�z�� ���Y82	� � �n�iP���o�N�o�Jw��~qq1M���I��&h�A�O�@)M����Z��󅯋
� �^�?��Uo��	<�$+J�K\ɫ2Tl����/hM~�Zgo�ޗ�+!���M�93�]����ҋ/Q������������������Wo�,���Ն�����0��왹t���t���h{��.�y�6�}���++i{{;�� ��<�`7;Dd0�9����X���[��Ǜ ���ů�1< _��g	�%�+dt�
!/��6��(2�a���oҷ�~����_C8 ����?Xh>�ϻ���f�}H�S%� J�x�r`�E�	h�u�W�m-/��F�����[,�"޾��P$M�Ӓ�d� �I�e��s�P���666ғ'Oғ'T���ӧ���7	
���[I�`E����>F�G����ϟ���_�ԍt�:y�@����?�ȣ��ի�ak+m}��>|�fC0���*5@>���Ʊ U������6S�!��2��'D `����FP�P�o,{l�;��ݽ������w ��e���B>F 75���5�Ջ6�!q�1�vB��z�~�� h]s9^Q���O��9�/=(����
�հ8`/]�dny`�?~�~~Ǧ?`� �����hT�`9>6����i?6����;wҝ;����˗�C�	��A���&np~H-���a�X����m@@��������|xoW�_�q>* �q���S&���/�xT���),������y�r ȅ��U��b�rHu�
�?K��:ۼ�][z;��4ܶz�1�CN�jǿ6*��iζ%��e��T�ˋ��MJ���ڕ��N<(2br~J����?�W޽CŌ۟���kk+�K�7��.�3gf����,�M.]���]���?��S������PUA3��,���������i��Xs��ɏqs��F=C�N��;�'�� N� �-�	��Q���H����\�t����ϥ���V�����9����?[Ќ(�1��h�j�i����uS���
0s� �c���y�6s�):��qK��r�g搀*��Į�W= ��N\�D�[G�?��.-���|�    IDAT�����7������H�Ô@��s�^q�ȥ.,�.��K��l�W���7
x�{�����!/2����β�:�~u<Q��Z�q==� 8=cOr�%� P��� %[/,̣���ޟ;w��=G����Q�Ь'�)�̹����É>��Z��?몧�v���X鷚G $��[���HD]4ֻ, i�EƷ
 <�p�x���u�{����~! >G"�t�܃��������K��4l�p5(`N�?w>�;_onlRK�Uj+�?p�>��O�ӧPf������	��׏:�g}+�����ℭ���9( ���x�c/�<���!�և����/�����6ݻ���v599���&���.ʖ���0�0��IJ���<���U%�1��r��l��';�q�2 �*�	�M� ��q�q������
o`����/({�)��`���@�;�b=���?��V�^����ݾ�..���433��gha�4�t��ͭ����O�����~�|�"���d������n�i������	;6 �	��ݓ, \�� b&�A�~�j��ߧ��>��{(�B,l� .+}$��W�jC9Ƶ~��ZK�J�`��^��^A��>���dG6ک�6����J�7����T1_@5��
f���A��O�nn���������2�����2�蕅y��H���t�޽t��=�(�p �Љ��4���q�"@��0������~M~�5=x� =x�C�b(��~��-�e�{5��h��ڽ�!m�:& ����ٓ-� @ſё!l�;:J�kW�������n��*��aR�P ��a qջי���߈�7����c����[/�'xps�
�Z��>�����G�]��0����,z�X��*r$��d;P�ϟ�H�q�-~,Գ��{���]H��ZP3)HCņRc؄���;���[��%�R��;PB��9�� ��>z�A�ᇰ�^�z���v�@��Gܛ��Bp�"��e��� 8�?������ Y�l�`����X������451��^I�~s'}s�v��wT�Su��4�9����Aj����VW3�O�εE��^�ʿ�^��/ �CU��ʞq���@�*{E:��ዓK[߽})���iv�k�iI���Z��¥B?o0&�yd���^
�����.)�s��"���ub��:R��:#�i_Zs/�,�]�����ӫW�1 7��^ ��kc*��>�;����3�W�e�]���/3���� BXqhH��$� ��g�L����t�gf�p��n�H�nQ�X��AN6��lk�\G�jxʵPB��2�.�vY |��OU�_�P8u�B�,��i%F�ui�:�����:��3O��1�`�H{duC%�������.�P�߷+X�<�߁�;x/֜�8#�[b�N�����4v�����Jr� H!a%���텡��c�B��Ts ���Ⱥ�L&	x��(�m�ټ����=6����[K��� �F�q��@	  ;gll$�cS��i��\:�l�r�b�v�j�vmQ����*)�Ŏ�"�Y��ܬs߳����a�7UU�ONA�ަo�����cDK��g�� ��� �C1q�x>D��p�<�$��\��wѽ�����x޽����8d�P!*�@ ��$+zR������y���k �Z�.zW��<��@Ou������2`y�A9 $;�� �9���A��r�����B�$Z�h��@��t�n�/�k������\��'.f���/�yO���6!�R���;w~������Vͨ��:~�_$���
̼� �G{8n���a�Z����t�3���#Z�T_�6����� ����uM�6�A!/�$�ʡ)�~�:OB�Iܮ_E0@E� �
TA̿��W��������3&!��o� )�K��HM��;@���i�p�� ���)�Z �N��� |�R_
	V94���D��x%]�vE�.��u�<��ϟ��(lbm;+�l1�!�;Ϋk�,ՙq5��[qӅ���ч��<ݾ/����u  wUo�� �rw! t�C�]T��e^��x
v?�*�^o�N���c<_6p�C|� 졩�{������㶅
Y�eQ[_`�)����te����'g��$��Aq  �7��-2�=�)���<���r��G���=�0(�- ( o�
�% ��B�ht؅<�	��@m�1��pff*ݺy=ݾuC7P�ssg�h57{7�ܬYLw5X|�o�Q}�k�M����7C����N�y�\�k�N���ڹ�K����?�Z��@w8���[�6���4��[���{$��q}��}��.��a��wig{�~L���eK��	������g�e�L�^�K�%�@]������?95��`?9�^IC�g�p� �����k$���x������� Ѝµ,�G�����z �k�f�v��Y�☐@[	�Z��,�m�u��z�Wy���ٽ��q @�̝�Iw�~����&����0�E`���?�=��?P.���[ç�nr%E����?�����t�.�l���A�@*�.����#S^��Ro�e�q�h���o%;S3ӂ�9�o >(DJ��?��pÆ=P�b��8��w�ַ���֑X�o��L�=�+���333�e��ަ��ia�m/$��U�c#ڝR:OR�� Bo�p%B&&BI`	U<Ð����u��  =fK ��,�qlH��z����|��r��{�S�o���: ���Y g�f���O���;���R��b�=l�Zܭ�
�h��+o(%�YN=d��tp�Z���z��� @�/À��k�_����k��o�k���
����<d�`ʟ�kA��G�>���b#�UP���i��B�ޕ�,�e���)����c!<@���EvjEv���� �-^NW��x9͟'0p�� �+04<��1�P�k!�(��f�,S�aj�9 @
Į�=M���+  &�ϔ��O_t��7�pl���X[E�����I��}�g�}�Mu����7��T�����������?|�����Ogggu��77#�/���+|"&�iQM��|���,f�;�:�y��U	4tmT ٧��:���phW����'Y�� .�#�^Ǉ ��(οO�����!ώ�� W������_ �◐��]
�϶�R��7 E>����U�6YLW�-"P�PΝ��א��e`��^���g3�:�?H@z���CԔ6<��������"'V8 F ��M��I�C���Ɵ���o 8��sRo�J��re��A m���8Z������b��n\>F��죳����hя�U?�{ȹ������w�y�  $;��м�
ӟ�a)h����8�z�x{�1��i����M�U��)/r�Sg(��7�x���r��0������Ql�����F��ONW���2����������a��<���*����X��b:�ڇX?��ש�x��p����^�0�"<p�AIE0�F���8�����'ҟy ��5��i?91�ʟ�DT�DiH�F�P���J�}>�==z���c������/!J���o�/P�1�~n�}�]�N��i��)��q�*��F����:{]�����
�)r�A$�^=��Y ����������*����ߤ{�~��޽��}�-�S@^WK�X��� ҉��Z�U�<)|��f����Gº���D!��4\�:�^t*�'�f��?�W}�AN�9y���)��#╿
 (���㠐��.���O	~[������oa�>��{8fs��&f@� 3� }p��  ����9d?�fҙ�3��	�]\�=�O٠�?��Ixjٜ� �ˆ����y30<��� �	�˃���+��Djd�?�\��l�tB��0{�wkȿ������E��'쥄{ɦ�#-�H���������4.��΋��ռi%��=�
�{aG�Uq���33�	6,�:3�.̧;�o�o�������[izj�\Zl��������n]���W���, �[a�uu��z��=Pː�aB"�sw�$��=��aU:�%n�Oh(�B:<��F��x�Z M�S����K\�O	My����%�){�����}�=�@�i�d"�m��O�m2�+���~�� � ����6ӁN~|]�c���. ��?�1�y|  � ����G��/�G�0�1�<7J�X�8F0��.f3@�a�X��~�%��Ͽ���1��Y��+$��e\<�1�ߜ��e������6c�x�z�c'��  'g�����S>�����l��,��\�r�C˳��KqHV��]��j:�)#S���˾�w���
1�����*s���B�y�Z�u�z��0�y	Mг���O��gk.t5B���R���X�,ix#��H��,(?��AŹ��jf�z|�"W������e�p�1$�! ��,����/��P�:ɗ� �� e���<�Ɨ=���� Z�(%�%���/��  pH��7���~�/��
M-\��a($����y�
\)�$Q�-�/ �,��SB �����������ߏ�������Ac�e�P�T�����t�yLl�,bi�	��9��02 ��jp���u�� p����� �~�t��ƬY�ͳ���q��Oa/ @�^T��B�|,�
�V��+��(� �FoF@������X�Ϊ2��Դ
˞�	_�Pdm2��0^���*�i7 ���-+���3�:�y� =����(����R�6��\�^r���������F=L���C�{g ` @��%�c���[ڦ�u��p���'���,��&Mg�����" �+��?;`t�sss���*0O����� @F23�Ŀ�����^����������  ������/�s���B� ($E�=F:�=8w^;�"b�60��v ��ԓuk_ ����p���˥׼�!/�tY �r���\��%��,'�i���KV�W_c�*|i[��C�FW��^Dߥ�*_��=y3{\vf���)������|�̬Q%&�ם�UO}����� w��T8�R�b"� ��)�wX����0
���Iv{�w�C2���.��s{܏��'d8p�[�_#In��=��K`f!S��%rdx���@2�ZP�gkI@���T��������,����'�)
�@� ��! ���a�� žBw����S�����?����T IUI̛Xʙ"�/'�x�4C$��@wg��^0�q�Z3N����n ������� (?놫����ڣ���^�s~��I�KHr^��E�׫�<Ϙz�M~0��*�_A6x����sia�<f
�
�9���ޔi�А\��W��F^4k������sEkȚ-��de����n�
91w�r����k
������Q V���Pq���vP�H���;����U�#R�&f���S�����^�������������:K#��f?x�&�'���,f���ʒd僵U&g��,����	j�S��U�v��j�_��{\���oޤ� ����駟�
�G  h�co��
L��pݦ�p�f�8���3�|�5�_^n��� �H�q� ��(��G���:�9�7�gW���:��F�Y/����Dۇ�  dݺu��J���+Wpq���aV�?��<�3��7WT5o@!�W�Bf8它��?#Yev/�d%l�1d�ތk�����y��� �sX��"�ſ�KlX�= 07?(}ׄg� K���������4��Af>Z�B��|�5���D��珕�ī ����i�Γ���Q�\�m�Z3�d911����0gjj*�LOq?	��	`�� |>==�ǃ���N�rѩQ�����j��ħ3�AX���m������_�_x  ����Ƈ����e���8!��ͽ ��8�=_�BQ'w� pr����� �<"���eKQ��"�R�ءf�ZW?�%�Ò��h63+�3 b}�͝��7wh�6[��7^���+�ϭ&���ޢJUz��d�罸�YK���)c+FD7Ռ���b�RO��d��˷b��K_�ȸ���՚6V��� ��'`�?�� 7?毣b'�>�0%O���ol�U%�����5�X�6o�\[�1�D?z���S��)����҇�����B���E�4R�@�Cj��\�L(��i�	\�*�4��΄�_#��қ�K�ׇ�҃_�dG�H���x�i�9�z��0��&	0�	,���& p̔L���@S��W�����{��� @�Z�������'�m�� ��;<�{�S
���C!�{w�Mw�~��ݽ�= �..��q�c�UU�&��;���/�� ��LʊK��͝.���HI�e��gd�i�e�EՃQ�:f�N�=�\�  ����4��.)zk��="�YϷ��:���<� P�R��>���j� `  (4i�Ca� x�u����&x�(�����׸�b����G.��t�y%�-���+ �}��id:�A��q����sCQ-o�XW~o����M���Sz���� �~u� �{���m @��V��#�:C�*�
���r�p)�~ �nŎ�B	|i P��F�������^l�ƣ �8c5?������]���K���E�?����Fq�y�����2��8�	�e�)jJ]� ���XZ�e��qɀ�B�nI#�Y�p���V� ��O TÓnz{Jޓ{B�W<5�!׼��ozMq}R�����`�b�>���=�ͧ�?���>��J�p;������aG���cci�m@��_<�ϝM�A3�H@����?*yV�rO���l5-�ɸ��g9��H���o�����~K��BE���һ�5Vо�b] �����/�$fY�_̥��4tǐ����D�v����:�� B '{���� �D"~�O��y�y~_����u�	 ��k�� k��?�aS1��~������   ,1 ��*;�ۂ��BV5ѕCT�N�L�' �����u���YYa�u$� u�˰��X�n�t�4RW:�F>ȡM1���":B�+�ǘ4��١��L�x����X�Ox۔�1~���,9'��\�c����R��ae�33i�+������ �?T���@<7QOg�q�\yk�A	�K��UtK� f��"�����e.���~�nUK���  2�D�+�C���:ލ  s����4j����G�+�1Z���J ��2R��>� ���"��(= ��|t �
�E��Y! �
�6���V�;��!����ߥ￿����w������֥���$ȉ���RM��A�����%�������4*R��w��@%@�Z��(�[�we�v<q�˳�p�����nJ��E�nz,�%v!���鲕i�}b�o��_0�����ٷ4@�H� ���}L{L��S)m�ĕ�I�gv�j�p��A�OLB	ib�O��pA)(*E����/U��I3g�q��� b���88����Ⱥg��_J�J8 �� `����L4�Tk���� �������G���ʭ��gA=T�K�tB:?�JhB�C��C>@���s�K���gp��V7 ������R �0 ����J��5Q������>� �$��J�X|������=������~�MX�YJ�L4O�C��7�.oc���bf��k�{��G��t@�d��W@O��Nr{�Ɠy��c�1�����d������.o�����'b��e� �~!�)��:(�<P �
�+J����� =OE�=��0�g�~���0ο��������=`��g@�'����1���I�	���Y ��ۀx��q��7  �8zإ���������o�j	��    IDAT�M�:��&6>�~@_��
Zv��Oxq)p�%ĥ��z��������# �ء;n7~4 ������y pIP��X�춖�q&�BC�oSQм���?16����	����< �v6����
�m�s\ �oj��6 �0FM���<&O����ֈ�� �O6 `ʲ���+�6�����T�K��{�B�E��0s?O��D0 �Isb�S�%�����<�E�
�ʁp�e��b"2�����z��� �HJۣ���i"�aEI(��}����I,�399�pÈ{�E�k�)8
�?g !җ��emX��rN�TK�c106    �m��qZ  76����,��4B0Q��Z��
�b�e18~C�h��3� ��BǄJ	 h��k���ߣ{&(�5�G�b�� 4nl���Cn�8Zo�(C�5,���B�?� ���FJ,8�t"96栦@���<��$����j�H�3/ -�~�՘����(cاyA^8nXTGb�Tm�ާ�1q�C,�������%�>��C�:x��m��C�h1�ji�V
:;�r�=pC��\/��[>V��c���e厌����P�:�I�_p�[7FQ�.�?H�� ��Oi��D�'��5֋A�)T����)D��$�@��K+ ��~������ �`��?���M4�d��2�Aב" �\�����~<-����x��9.'� � ���P\�">O��?�/t �X�/:�o�N�`�U����fC׿�w���$+�HQ�λࢧ��1{��9�d+���J�5��f��M��s�O ޓ4I�:ǁ�u�������Ћ��5%�y����}���yi�͌ h�����t��.�����+��?d��Ec+�&59Y�Ci��y�:<��P���ۇ���X?���=T��7��NN�G@B�ȁ  C �M#�#֔ISU-5c���������=��+���Ӕ5�́ �w��������o��o� <N��+�X�0 � J  ���1~"
��_ <�w���  �O��o���@����$p� �@@�)ڭ�]ɉHVE�����U�����Nf"rh���!��9��w��Aǿ���&u���8���(I��2ozLOgV����l��g v�}���W����9��{�2hq������uy ��.~Tkkiuu��k�̉�G�H����"?F�����m�ñ��(�xx?��Px~������T1����y��C̞^{_��SS�i|H|cD��=��5� X �k�F��Կ'h2{ 0�ֿ4�ѹ-�0���
ȘJ����[��ֻ�YZy�~�@	  �8 ZBS�#G(�n�&����/0    ��Ӌ}s�/ H� h��Uc6�FNrh�B�k�5O�>��.̧yi�ra����v��dq$p��! Q".�@5oM�(=N��T�%C��ڬ*��0�
��p��K0�6Y��qea�}��0H#N�}�U��6��.w}=�{�-ȥ�%�///cN���L6ы�ؽ�Y)
P$�6��% 0������? � �(�o\X�ch��+��X!���AZ�@h 2J���՘�����w @�8u��K2#	�1=��m��(�>�
��I�I�A�Ų� x ~ �  ++i}�)� 'HV�p����/y�& @^o����O�b!��7���}9 P'��T����'�Nl��F��<�`W�C��l�._�r��/]L�x �0�g��!D�K%��s�6w����,W�b5�U(%�	C�!֒��͓�P�\�Y��e�һ4��h���>~,,p&�k_�Đ(FL~د�o�տ��]z���` ^��n�Q-x�O��]���x=V�c����1}����GXlg��d�c��QKɃ�O�P���]��,�m%}��
��A� �A�_K�<Q^G�! sLP"�W:�+Ȥ�(���N���f^1T�sK��!����  ���; (~| �DR�%��O�{��Ae<sXI����.#��l	�_�q�.� �:���s1q�T�� �v�%�U�k��< ���ZsaႳ����bZ�p>��{�̧��) ��d�@@m��P:G�oD�Z��zyV���~8�O�(^�4��/ea��Nu߹�;ׁG2���S|�������bTޣ=��! X�2 �d�g��f���
LP,,A��.�ڥv��G�̮wt�KM}T�L��<Z����@ؓV�S�L���4��''��Pa~�r��[&5sC2�E���u�qem��Ұs8C�;<��B D�D$�d�K � h�� �H�A� ZK�{�WF�}�_D2��|�pI<W��6w��� �ڡ���K�v���P�J�~���.�zC'�{�FVЎS���ҥK�����o�ׯcі�ggy?��&��*�f) #��C��O��[T�C^���"��Yy���H}�\���+�w�$P 0�"���X!ܼ��EO�)O�^�OJ�k�Y�Xu���Jm~���@t��p݋��Ѕ��9���7)�>N�q�Gq��ѱ4�v��>��%k��� 3��AV�Hfk�#%}�j��q"��5--��٘:>�xf��-�@ �B4�����jcИS�`��0����(`甿{�,P� أ� O(�p��	�ɳ��9!�C�s �!:~t�<i�^�ý ��^e��z �Z�}{� �b`�xFCW���_��~�1]#@��e~��ߝ;�q��M"zq�V����s4��m��)�,p�� ��b�!Z�-__��j��\��&    )|P��\������;�J�j
 2��~?����c_J�
�ȽVÁ���4��� u�~�|HǛ`�l,}*�K�|��i{�����!y��2��?L$P!�o����W~�z%�����	~.@�Ƀ�?B�{~�`�'��kX��`	�  ����B@\ !�P�5�)�J]�C�P�I��%�+�p��<���?�fzk ��Uh������ b��<�2����4¦6� �&�O ���k��=h��m�w�� ����.J��_  -��P�bȖ�U ���x��E�h3E�;�9�r��߇�=�ҕZ�EU� �`� [��y�6�}���?���=���7iw�3�s�T�� >�����CaqyO�#%��9�;IAK�����<X߁
��x���I�83����?91iE�@��W��Z�N ���ٓ��~b�E�ŗhC�/ś�up9+@]�$7��hf�+�S�!�=��]�~K�+� R	  ��a��� �G�^�RH�0�.��}�<:�R �Ұ߿^)��� 8����V' к&.Dq��Be��X�.�� ���}h�s/���^������56N���LJ_,� �`���L�Xc.wZH��l��XZ}ݦ���� �Т�ȭx}[]"���5���=�ط���&<�����5�����IPZ���b0�`{�EJ����K��D1!�a/$�A'���8<�㧬 X�`�OML��������=��8 ��G� ��=�� ���𞸄o��n��Rj�}�,[�' ��4�Z�� �=$
V�@��A��?ߵ�=KK+��7k��A�c H�^ J$@�.~A�\.:T ��b��W �$!��v�ҍ: }�����O
 ���w�g�r#e�R\�O�L͗��{S�vZ�!�O������ݼ��X��b���s ��J�8��{ZO)m6���R�%��	 �e~��y�5X��t����=���U���mm���5���똷/�G���ޫ�r|�ƄJ\������WW��;2�`;f��C)g��!6/�!n�܀q�� �I~���磌���B�?J�bE���5���)�m<t�;>�����W�O����?O��6_$�Ou�/� o����G��_}�~�=�^%R�l[4]�hz����q����f��j��פ�Ȫ��� �#V��}�� PG�?^���B�j�x*6��V?�n)���[�y�v�������{ߢ������W--\��k �-��T8*D��߈[9���
�/%��֥O�!�?�l- Xr��A�S�Yw؜�<���{���}j���>P7?���E���Y���Dʸ��K�]T�c��-'>��{�����(5�3xSe�0���}l�l�}����:B����V�%)��k��!%�6~~b�R���k�Wm�o�y8���CH��y �`O$e|	8B���Ç�������G�����w�k��R��;�4��Q��2@Z><#b��w�q �{ڶ���M�i^��p�G��>��  �X.�SZ`b)�U�qQJ��S���'�7Y�`�޺}3����� ���O��ޥ��+�B�9�j�%� �@��a7 ����� ��k�����]��2��'�)��� ��_����~��`郕G�5L��@�
log?	H��o�pbA��> GP�b�V;��Y/�[�])�K��g(�?��w��6��
{����3c�[��`
��Ǟ�3+t�2�#������h��T�"n!ҽt1�|��L?�h� ��-|$�Th���:���0�܏_��~��W����W�4v�6�dصf@|=�� ��Gʠ�S��h����!�>)��>|���+], �W���	  �6T�C9s��S�0�y ���� �����p�}�v��j��{��ZuSMq�X+[�b��"�	  �f��hq��������ٝ2��W=	.�O��q�*�|�*�x�*�|	��\��b��ב@|b��;#�i�!#BZ3�[�Ϳ�J_:�A�<��Ϥ=���= �I�]xy�w�n3�u+F��?~�/�+l�Dg���_�e��k��["+5�	2���/�Ӈ�� ���c�������rV� h�G�9�R��m���駟�=�����͟�橑�����@�<ΛA-�]�}�:�u�� �l���� ��T&��K����}tr��*� ����/��u�f���}$ ���߰~c��e��Ξ o������j�^��4@����Y���)���f>���v�@�ˋ�lcj����Ϭ~��!�O����|.�a�"B�D��N�6��8�N��#Yθ  �x��=��a��D� ����P ��4���g��WJԿ*��8�ۦ��/���q/1~ 4r�s@�����D ���T�u.�F�>��^�].i������fP@��T�~�&� য়um�ww)�sg��a �\>P����ٟQ6b�/>-�>���$�/����� �r�\,�Š�?[�K���Y�㩐���p��>�荛7�=l�K�Ыs�Y�%@�Z����i^
�i��w5N,��?�tru��"�2Pm�:�A���S��u,������ϯ)�/E~6�{R@�ȃ����K�9RN�
�`1̷�=��'���+���a�q*�c�t|c�q};�M������X�gu�3�S2t�e����#�<v��}�5��_�͙�ڣ8��+d��=?M�[�!c ���V�[C�(ԁ��Az��5Z�?�����g�PY�}n�<�.X+ἓ$��JY<P���L���Rd�H_,���a�y �_�s��;��
������������h�����7�ӝ;wp��M��'-�|��l���\��Y dʿp��Lp�cB�Y�����I	^d���B�O�|�ڇ��Պ~�P�wӪ�a���խ.o� ��-¤؍LEvĵ�%tٲǸ>��)'��8V�6>(~���}\hG���?/�3�9��^)�^5��װ�C?��&F���;2P*��jxK���n���y `.��X,�vTc����W `)_�Q�z���K ?�����O?!IT�I���ZX��R���x����\���V`���.���r��� �oJ�T]�  Sї��B
^@�k��>WVu� �us�n���ڵ�t�֭t�֍t�֭t��5^�X�	;Y�-�O-4�(����VA���B�{��s_@	 D�k*Ӿ�#�JIl�sS�������^�|��~������L��V�Ø?���nf�r�:���� ����)q��2�8=�,�S� ��� �L�U����f>L�Z������LD۰���\�x�ᮈ����ZZ7��5�&��gى��~��3�����o�QCS?	r�+,��C\�?��{`�S�'��!�������&�� ��   {	08� �q1.�G��wݣ,�Z��	 p���>�q \,E�̒"��Wjiy/)[�h ��=@7�sg��s�p��9,} n\��{hL�'������}�d��{  ���ՙ�����k�dq%0�$6,VC�ux_���ke��=y�4={�,=}�,=}����.]X�a��=*F$@��R
a����ݕ�
���ҹ�s�A�s ��m./ � � i�k��#��wI�3enu��cA�+#[W�y�Y!vjC1��{r`���Ͻ ��{p$6�� sH�S���2b)'� L[K`�  �3
�bPRj��  ��S�o�Q�����V���W6��7Yw��q�/Z������0��]?��� �w�~
��) ��96c��So)�n�`	��mUc���e�ٷ�3��61��N��߅�i~�:�-^���^���]]Do��+�ي���>��
+/���t��)< �Xq�ܢ�x�3-�h�1j��~L�;;D�Í��o����2�x���PȈ�T�/�@��p��-v��������:�74�9���75�f���O �\��7��z�06݁=u���b~�%觝^��q��t.9OC-���sы1k^���| �a����K#�B>f��'���r�ڬ� �O��&���I��F�(�A�o�0������f�<x� ��i�0� ��f� ��iNpN�E �s�(\� �P�YH�\hN�a N�P��rX PS�m����=�K@ܶ^ћ5h1^~��G���/.�������\��  ?l�/]��7,��q����J[���I�pl٥`���Y�Jn�P�� ���Z�b��ڇy���@ b�Xҗ� Сo�؆�åo����y��/$=��+���q'=��=,��6V?���>
)�4TP����ե�xYI�rV�jVTd=L���q�K�ri�p+CRy��AH�T�W]�iy�b�5�CG���9�dq�xT����}���ٔ���(>�> ���ᣴ��m��"m�ю?	�C8�����|E.c+w�=��*��� �kK��^�0 ������h��{��i�ȭ$r�K!1h)3����435�._��ە˗ӥKQ�_����.0ɋ �Yc���Wms�V��y�TĔ�¨�7�|$�6����� C�!fm����bG���JZ][M�礼|n�? ���x>x>f~Kid �zx�3������;��:��S�*���R��Q� �>
�Q[�|��0��󿼼�(����
"s�����ϔ�)r��
�|��
��r ��+��H���0�7D�,|���oA � ���� WW����z ��gz���?�L�?��:[�?
3��j�A�C�Y�^�4׌ 2����e�ǃ �ב?��n ���7%� d�u9��/���JÔj�BlmV������+�����"{�Q�/ph��n�<��/���*���2��H��ݻ���"c�T �����{ ����x��@ޒ�����k��v8%[��줽}*�C�pzN�|(Jyhc�sg�(~/{x=7�f�o�韝����7�7`�U?�Fغ�LV�,~�Fy��Xցv|���J��fp�-m2O�+P�y.8 �{x�'ʞΧy����rW��}d��w����X���y ��޺'��T�_&�o��B�!n򴲒^�x���'O����'O1��
���!��%Ĉ�    IDATey�^� !����'X%k�%�>�g�ZxrN ���1��6 �K*�6  �v9� �b�V�M:��RA>[���J�~�*� �~��E�ϟ?���(1G(���/\���H�ފ)Ii�.
 )h����>v��������H���@����_]C��g�{����ȼ���� b�ȓ8?O|����Ӽ��t�|��0ϕ)��b�C�Z��e&�{h�K^-I���򕖼>��Ha�)Ȇ��_`W�����}[��u;��o��7��n�w�JQP�}���d�̡Xp�Ϲ9��L��^����5�B���<nsW��x]3L ���~��lJe��$�e���=s-��ny�A�# �}�r��L>y�4=~���O���/�_Ԣ�2��^����TZ)����8X"��Gk�
� ��|�ݕ� `W��g��
 
PB��\u�������I����w�ڕt��b<ur>������*�p� ���{�sM��kP���k�v)���ڧ�\��R�>�R@ߓ�Oi�~�ϳgR�>]���ftq�@�s%>�Ç��8y��U��������Rt�QTM_���j(6 �@@5ݢ��z�̬lN�&PҰ&���9G�֋W_��';������a��\D�Y��G�jI14̩
��O�o������o�^�X�
��z����ӧ���g�	 �| ܾ�,���h�f���;G30ĭ�$��-ϯg3�UE��ϸ[�n10��ӿ�Ͼ @��'K������A ���׈���u��\O�����#G"֏E������G�`E�S!�G6�a��|�J��|.x|��W����C(��˗ؤ���$��������R@NO�p!"��zĐ8�@�K>��E�>"��0q�p!��||)�3	&� �H���f��Kb1��Wx5i��)�1�����;3t�8��9p����k�4^;�3
�?d#d�Ђ=��7�C	��q�c�F���eMg&�Dj(}$M1 �BQ�K�����h�!���:��x4\��U�S�;�/~��, ����@�����*͓�9gO����4] |?
v*4l%�QM-��<��[7o�۷o�[�n�۷n���$5�0Mp��; �d�H��$:β�F�����8��כɊ�p1�u
�{��s���6��K�H	\[��@0�Q�if����"�)EOH{�a�#GH�W?���G#��� 3������ 2Ql	���e����(��K��[!�����ׄ���`�`�@�#�KOT���� �,�n�L߂�]=9P3r���q��������c}m�� ���t�νt����'�ƐP���D�����*�.'��`vy�N( *�YK����mw�� ة�����Usf'Ӧ�1 ����㸰q^v���bx��4?"�����믿Pտ�~����T���Ӏ�~� ���Z�|�+������M�&pp��j�_+Xk�|��3-����U�,��w������'�b�!��5r����'���ǩ=R$m� �8� 
�J���.M�C`��yो�L�7���E�[��}�f��B�UځQ�7��.�v!&SS� �����)��y�"�E�/eO(B��P��v��+g��S��_����y���O������K- ���JZAj��JZ�Ԃh �����Ԥ��|���YM�و+��}  {zz��Õ�ir7:Tj�u?w��h����\l���j��T�� ���￦?~�=��ۯ���'���������@��&�M��,K����)M��"�=�)��6Ү�_[�L�����޽������޻O�[ �M+Z��-�Z"��:��Ux�OG�%2�S�NQ`��B��DI���}���X��(tB�,.�:����>룶��4���,��t��gY}�Ȏf/�y9P3���8�݅\ �B)���EӺ��[�a\[�#��s
c ��U*����?n���@kok�3� ��!�g�1��i��~V��f���}7 ��{~~��մ����F�G�?�7��q�At�#�d�Jn�F�H����￥?���Z����nj?��M��r
lA AfifM�R�� �k��6�ix��A��C��
~�y��5i����iZZ^�Uj�isP�����L�bပ�?��?N}����8 ��D�j0	�>ZD��c<\�����' 0j��m��ߏ��Z�:���,�,Ic�սW���}t)�%@�E>�,�jc]��P�R�e��.4a1~G�|�>��&�����'���������˗\��3���q܍�Zؘ�0&m��a��7 ���5 �^/�pP���r���,�N�o�qD ⅜�$bє� |d�X�J�N������?���@���A�nh�S0mS*ۤ1 �i8�_3P-+OG�  S�ϭEErl�T��|�_��U�{��څ������i���T��}���L�#�Ϙ�ffȏ�&}���'~���A\�����o�>Gv�s����Ɉ~$h�0TWD]n�1���^�@�Xjt�d�WP+U:h`}�[�C�<w I�	��6�8w����W`��H��;w����&�G[��� �Ȝ��r����;G�N�j��E}g �w6!?nw��ˏ m/�״ ��Q�>q�16���O��=%=	���!�@5��@������?���-&�$�W#��M9�"Tj�{��G:Ͽ�D7Ӫ_a����c��e=}F��2�����H}��������{�9|������y�'I��@1b�R�����S���i�s!t���E�L�o��/:*�H4�n��m�xJN"�=�@�sl��x��	9�T��$?�-\-�Y"?��>�=ᑸ��A��Az����U��u���N�sT:����r�ձ���VW ���=w�� �r���z��t�8�����I$;�:m<Dc��t ���W�$�Ŕ� ��G��E@ -���<m$lQ?w|
��D���&h�^־b\9bqA�,-.'݌Ȧ �7p���c�|�
A�Yӄi�及��ϟO�=�z����C[�� �O��II�S�#O��!`hcD@��΍L����_���X����M�/�Z{B��hQd�+_T���r�,�
6=�.�.D_��-��u�ޛ��� �Z�=zL�?�=�@S ^S�5�� 쮈�ݫ����� ���S�c\ 1}Ӕ�=d�׵�� @̡��3o<����@�  �h��� �j��v2�=s�����ן�Ͽ�E��l��O�Y,�$2��ي��Q�$�B�'��u<l��0Ǯ�i����d���Νt�w�@n���9.�b8�A{l���.]�D�^�t�,T�O|�<��.a�	3���FH�S0 :�I��e �������� ��~�����*��xw��_yrv;e�:֙�K���ͤ B�E#���'�$5uQ�6riW����� �Q�h�6=���K !��7~3d�{���.��7��G �O�޹�� D�H��05Z����h}v	X��0�Q��LQ1  "��߸=8{� ��o��mQ+������U���k�� �����} ���/
�@c��qz��	�]���yv#MOi>��4B��c?�� X ���t����|~SVH%%�,����N\!��_��:�0�o t���#�o0���qv=���Ǉ�w' �ƽ�ӌ��%`�5��`F<??�j�1J�O�Y��_�y��9���I����?��&��9A|��]y����U��= �3
Z����Ǔ�[O[��� �B5�\C�B�*�z�����3�B ��>� �wf=�@,�+PA����ϟJ��&��k]m���)��ؙ��%��?���4r�[��# ���"�O@ ��p��1���>�R�X��
��͋YEp��Ȍ/_�-��Y��kz�A��Bm�Y�x�"YS�sЛ�'��g�|U�jy��uz[����JL��#�o��[%P�"�J`����g^g��>!��E~��g����"q�?� 4�ǣ�{[e�&�g� �>$���(����[��I�F�W5f�]�X˨|3߫`��
��������7ӭ�7�E�z%
��l���0ɏ����lʥ�Un l�1��|��?)����3
�e@��������� m������4?�����@ T�W�~�L����:aRo9ׂ
�
?�U�oD�W ��v�<�D�(���Čj��Kmڶ��t��
PpRz�~i��x�<�O]+� ��x���	kL� �2D"������{�nz��1��@!���*ŗ �$��+TN��3����`�����C�77կ	 �7��h��g)~n*e ��#3 ���G�?	�#�ӹ�gB-�kT t�9 �B�53��T�)�� �g>ى	��>*W?��Tr���#��GO�$��Ok��@�����������υ��ܹsT׀���%�?5E������0�e��H� ����� f��.e!� �%�E@�6][�m����Ҏ܇6�=k�ؙ��䩁�F�VH'�a �%�}=��r�`^cRQ,4藖�F � F�K��P�8_h��`W��=����?��5�3I6$�Db�PK/T뀎� �w[x `�G�'��� ����G�~<����������h P�7L{{4�={6]�r�+^�B���tY�\��d�Yj�Zk�@,�Ǌ9��+�+��.��ߝ;w(���=�R��L��A�3�G��s����w)]�x������!j��Wa��/r�sF�C-�D< �@�$5�T�! �	H*+B"�J7 ����Q���/�}?k@檠g��"0�f���$q�-����
�4��ʎ�^��J�?\�J@��hyU��\͈l�W�!u�---��������?���G\�@׮|oc��;g ���c  �=�?���/t}�z�6 #�Y����hi � `��tr�׳�?A�˗.R4<��/ P�7k_J�R h��Z ^ Qs��j*�
s�� �����T��臀?TcC���?9��	?����Z�� ������3��@|��3g��� ��iY`��ozD�G9�� �հ � �"��T�
 �fr�)ȫ��%���@@��'{��p/o�`A0���ј��P���\k���ŀ1� Q���,�������~T�������!�O�U��7��Ja?���� �N��p�����&޶� ���R�Ǣ�դ�{  &�����=w�L�p�|�x�|�p�[
���7myэ�nu6RZ��U@�$2� Eyb6|�/Qg��+�\����.��߾}�������4�����1�y�����}��U��3\�&�(�X9l ��G�" W��� ���q��+6b��ai��f!����P_��Z-�͟0\#��e�:D�憅p9���(�����,��hA��`R�1���k셵�8��~��
B���a��� `�c8\�2}��o ��/�������P�?iƧI�?{�t:w�,���ٳ��9nA�����@�ռ����GGeA�˗2�L��!9�ļ���cN�{��+o޾1���wiiy�4������h:��=T�A���H}���С4wh.��C���*�F���K,�Uf�Z�����a�D�4���͸��5V��OB�t��Wv&x%�C�]+P�z���|�b�M}��*��F+����<^[\g���(Y_%F��U�B{w.��� �߽��R��9�K8�i�歴v��k
� |�������  �s��P��H�� ��f��  ��>��P{�  ��5�-��^��`Y_��"�� =.��iX(�"iX���u����(l����Vvuey%�}^K�N���_���<�i�߹���ď
�� ��g7�G��F &t��^z�f�R��P0�j�����������_����������H4{Y���E�ca����/��S�dprk_#���#	Z����'1T�E;����Q�ܮ��O�#�◫H�-��@��]C�?y��+B $��D�7~� |�	ث��� �Fſ/^�"K]3E$ �~/]��.]�`���g�I�����/���A*͢%@��8�PG-j�� 8+�o��:6�5� �D,`�C�Z�a�f��%!rWG
���9z���]�x�����?b��zyv�n׹E#s(��:<~��\���A���D � )�'�V^쯾q5K@n������j��
g������9����Y("�������|͚�U�������*��O��Z���S���?"䷴�B$�`�CfI�HԨd�l���[�<�AlD�Qw��w���}� lw��#�� 2�Ɠ��a+�ei%���W._JW�����̀J�s��ħ}��
�ʊ!W~feXkț�A���y��h�e����a��V^<��kփ���Gt�G�MP9_0"���h��O1��=}��J�LԾZ�P��T�ϭ'n�AZpϛ�7J�Ek.�F��ֲ���r�e�Ph�7�:f]�ׅ��7�\�}\ 9�A�T�G�~	" ��}���E ɤ���v��y�i(b�Dɵ�"��=Y �|4�����SV~Z2ktM�0>�܂�w��ڝ� ���W��O?�kmHk���w�?��ZOs�V5T��7���T�~�j�v�*�ׯ^%  N ��q{��0^ ��R��K:6yh[Zt�
�,��M��O�=��ٳgd9�B���#�6�>s�]hϜ&�ѣ�%� ,���TH���BI��'���,��!70`�f�Ì��9�43A*�;D�Y��/g�����O7��I�����~疁 � ��wx�x�Ef%Pn�mRք  ƹ�7 �*G�*���e��{%��Ѣ|4�߫.蛙,�7l
�4�q�0�� �ۍ���s_T��  �o r3���\j"��Wh�7o�H7o^O�n�H7n^O�ϝ%v@�{O��C$��x�e������f�fd'�ɉ�|��g%ao���M�1m̯���L:xp�������y�/���qǏ�H�g�AIDJ ���6�1���|#�1:�!��:r����Pe�disM7*�Ąr����.�`�x/���". j�,�����ݍ(���G�B�
8���8ŃeW7.	1�صľ~��#yB���3�����(f���8T�+P%9��,R���;�x�1���  ��+#����I ЖB�x����y^��U�� +I�b>�T��۷���7��EY ��Z܃h�R�`�������r�M�_����S���|\���`�����SJ�Fa#G����i�Сt�4{N�CJ�E�+@��K�/Q,�$���τ@�%q��	�	�%�1���|F-�P��).�8.�e�w	�w�:����P��B�
+\A�w���^U�c\ ��ZF2���� �s���k"Wmd��$}���+���f$J֡��&&8ht�+H�}��}����Xs�K��$?�M�����b D��8�V��Ųu0�� ��}�4 �O3�_�A���; 2�b�V��&X�+��Ă_3X��)��Q��V� ΁���+}K�'V �C�y�iTR��L z@�����?ih�( �~���� Z�W[���O'N���E
`�H@   V�Wԛs�>�V�@+�E�a6��C�=��T��WN�D��Q�nqi� }� ��v�݋�}t
4�F�Ԥ6F@�K k� �z3�1>*iT��?ZA�{�[��?�K�͛w @��< X�\B�פ+�B�i����;$��h������p�PpX�3}_ݯ Dةѭ�7gR������xS�����_�o��"��d 3��R�8��bK���E�A��}��1*޾�^ �<0    IDATm�m�H�� h���MY����g���ӧNI �! ֊
!X����Մ���p�Z=N�Ql�<��{�Z�s����!u@Słٟ����Z�#���`����>G��.{X���z.�3W�&s�fuux- <��1d��
llRn?��?�UI�����D X��=��?A��h����0 ��
a�:�8� h��ks�=�}w��+G4G`� �bWF��k�M  �!2�S���}����>������������8�j���������ڙ�-�v�[0��F9A�>K���)�y�6=z�(=|��ۇ��tK�{D�v_:E�~L�{��Y�T<v�h:����G������i:2$��$������<xB��	ws`l-"���p�,��  >O�oz.�� ��U���������/"Tj�<N����#�<����gc�,F��Ç��|��K���:ӊ�o߼Mo���[ �!�ń2�? 	YMށ��:w���y��r 0��]����  . BƳF��V_64y�h����ҟ���������?���� �|�����zJ4ͨ�=%�x�&l�؄��)X����	��0�����H*�Q�߹s��pv��f%^aj��i�>g� �f���﹒�R�@�WpK��X�.r�KQ&c�Ss��E���}I���>���CzXj> �h��~��1����X���d���F������:�u�����������k� ������� ?dpL�
���Ȃ3�������b�L��.��`�V��PkW��=y� ��i���������ڙ ��O}�����g? �����_�����Z�[����32-0���T�<g�7�/_fp�?��R��,��m��G$?G��.��@��D?��J :c
���@�p����h @���j;}SQmQR��</Y p������lQ!ikjB�_���!Ƴ�B�@C P�v&*�r�՝�O���}g��A$�Q��4hc��`˒ڠ  �@
����ϟI�c=�5�<={�����S�?��V�����#�#�mI
e?E%�30v� �A@(VY�~?�^{0 ��uf~�~��  G}���T�M��C���-������m� �\��X@p���.լ� ��P��?�ɒֶ�@���녴r:y\���O��9�/� �p��m��to�J�!4`R��N�_�?�b93S�P�Ѐ�g����KF�9��Y>8	����M(���iF���{U�*�\f1�P;�#6��\�{�i�N�����H�1��,��,C����gW�EQp�:�G�h|(�u��֒I���ǩ}p	@��Ŏ)`��+��5l����!���ou���U���o�;�� ��@��G��K��. � ������6�xjP���i
�C<D�#����~�,��~�5�����:����[u/�𠹠*�ƪn�}�����6on���H|���ֆ@,|V�=0;��H`ߙ�g��`� O���?�7jsu��8�-B�L��mՖ��v�����-]��?@�	�p�@� ���IwFk�}��_D���rt��鿠�me���yKP�Q�1S|���B-}��1�|��>҇S���� .���D��kk�2 r��)�'�#5���G@��In4j}��;�����O�k��c ��g�>[�p���hM٘��V{+{��-|�����hn���nߺ�nݺ�nݺ�nݼ�N���_5�k� k��$�Y��<� X�llo?���῞�ݿ'EW��# ��~�»~��a����ϟ��������7@���
|kW�u~���:y؜�QQ �g-Yx�)�B �������\>����X��:mg�"Y~�_�|gE�T�/.k���*Z!,�a�ȯ/�����0��w��� @�����C����Ђuҋ)Xu��V�D�ߗ��[X{#�`��(cO����{�� �9�.��� �i�[x@X`���С9�G�#G������u��v5͟8AJ<��:� � �Q�*��I��>6ծ��ƫ%X���_����?i_<N��H93!艑�E.^`���inn��	(8��bt߬�:�J�c����:3>���DG�{|�����\��?7�3`��!���ڵ|�u����Q�S������<z����XČ�wH��бE�'��5Ú?�B��h���$l�G�?2GX�L��2@k�3_߱���U�w�R��W���x���gWD�?�l�,ׇ} �kx  ߅��{����~= �q�צh�% ��P������ĉcT���.�ЕK��K�wJD� ����%F��6% -��f�%U9?&ؿ��[>�K��7Y  F�գ@A��*Rt9]�bE H� FN���2HϘ�ljkRu6 ��NɒT�����Z�(���.,�X�Ǉhm%XP)n�x�����j���
[^�敚2�����}�"͂�8 �}��=V��!6D�k���Ǿ}��� ���������Z�ü����}���0�	�T���)%X�S��
�E;(S^ �-�� `  {O�~�O�o��sfs��[N� �.悑���Ө�w�$���|�s���s����-���A@	 �3_�栅k� �  `�&&6� �i���;b@���Jÿ/凑�f?h�(W+ ��fUA�;F�32jXG�%�c� &�M;����Κ���R�<��ȗ�U����A��@�Z��-�W����Z4�� I-(&ҢЗ9�jz��٘����]3'��X�ӽ��q��kJ!E�[>����_QZ�� ���刵�[c,�b	��b�����F®�}�s��@@}d����p��o�]�T��]SM;�(�U����b#��A�o�,�9w�l:{����=E��*� ���yp���ډ}d����7��~�޼~���O�Ǐ��O�P����=�`?n���댔���>��A�j�(Cޤ�-h�K�H�h��q�� ����! N�$�B�[��W��Z�D�ty[�����p2U�����k�\���R�_�9O��;$���#%��4�/��S���U�ۣ���9��=	}�d���>�+H�C>�[�v@(�|p��֦p364`0��  ��Xw�� ��������p���l���(M-?������4��A����Et._"{~�x���	nQ�3�B�_����(��"�F�  �T��GD?�˦Ԭ�������!jy󆣵?^#��B��ϓ5��q��=��;�E~�w���,�}g�ttH����u]ڑ ���>�z�,-0��5"/M�l��kp���[U�UAa��x���J媹\M�ʢG�������R�_P���+�0p���ϟ����;W���~X ��ge%�  pe����H�?5����,�+�}Z�n��[aZ�:�i�	��a����T��q�;i����� `��`8��Ы:R�G?_�h�;>��ڦ�՜��Qu�ų���O��w��5����(��98i�^ Gx�5 �v> .;U$��  ��Q鏊�����CJ�[Y��
���_|�W�^�J�T�j���wP
	��E?��4��IS�r��yw��5�s��c<�Iѿ�b:�9CTx�om����u���a~}�������<3����_������V�V���d�|��ڇ��8����i~-����`����:��X�"��=.d��O�*��`��&�� � �WL�cZ��r ����  ���p�#��*�G��m�h��'jg�z����
�o��]�j�o߾M���T���g�̔����a��� <�Mur���>O�>K��o�����������ߴ��.�^l���Pr�ƍt�Ƶt�ƍt�ر45��X�@X���i��3�UiQ����Ct\4��yF[�z��'���rs?�[�g� �����羹��"�/� �n^�QM��_E*ݚq�G��U��:���r
���9#�^Z�c����?�|J+?f�JYE�D�A�b��`>���(`5�w�r�{�bd��5u����Y 0Ɩ��C ��aN=�(?��#��F]=4U��څ@�*��}m,u���7��_�F�?�ܾ�~��v�~������!��rA�@�@��X L�����:�=�}��)	�� ��+N'�"�wX�\����_��-2��������tG�-�mes˾����0�B�ZP~c��(Q������+���! Q#��v��6��<(ς��'/~~�d`0 �:3���*�� ��3 ��!�=b��Fk�h?��S�P�4> ��yO�ER�U�jUϗ��U�^y	�{�G[V���!�A�K�Q�f͙ݚ`0���� d���hm��V����'9���8<h��!Iw��� �7̴`ݪD�߿h��^�� ��r;]�z%MϠ�/��}�?	 �����ϸ xs��NLP��o�x��F���w僚w����=��r8J�JT�)"���@G����a[n��l2Z�����og�O�h�_E>�9'!"B�e��<p�-��l+B�X�*��׹P� �i�0�����L�l>W�*�,�t�3� ����w�)~ "2����M8�ר__4&@Z�pE�K@X�,��T����ћ�G��߆o��0�i�K}�t4l���u��j��Gl  㮨�x�#M66 �چЈ4�����>  ل����^�Ł��]gS�R.N�ɓ�-~zf�L��o�J�oݠ��@�j?U�Y ���^��EY����2�����g/҃����(�>������)��t:AA��?�q��+o@T���t?�
 �5,�p��8�ak�ڠ���=�:��J,�\���ƅ��<�g�i�;����/Z7��3���5	��d�	 �����]Îy�Y (�9�_��X����0 b����m���s��]Q�/��ե��Qn��X���l�[i��k�r����sm� �#��A|�{n�h���惭�im]�3�H��x蚁�$D�c���՛]�ll�,>Gc[r�Sꥱ\���,���s���t˨o���B Z��谘�I��2� ����u_����w���w�͛�����R�����W���2�C�C������B>�q�h$3SpVB��6�S��1ps�}�*��L>/��� !7�{˹Y>C�Y�^���3E�s*�uJ��y*��<.�:�ؽ���}���5�[��߰�@��o��rG��H��9���	��r��9�P��VO9�� ��o�0�6n*����M��>����5k@���u��+�G `�s�ЎiW��|iWM��� r@.trN�2=���^�d��啛�����Ce���1~" �?��������J~s�ڵ+����uj�
(E꼥������V�6D�!���+�/^�Jϟ���+.���Uz���>���_�/��B-��
xj�Z������:���~|�06�06�Bd�ӹ�[<�Չ@'У��S9�,� ���d~� �X�9����+�	'������*����ε8U� �>o�R:&�3��)��@�D��\0��&�.��cdx*].���_��D���^���X���P��+y�s_��\	��o_�����sL�M��~�¿�8�3{��a����wyd�=��f=h��g5-q!0 �B��t�[n �%�j)(�Y\΍���hqN)%�9J9�Gӱ�G������vh���Q�W�A��Q@��"��%������ɳ����������3<��Mt�9�Qt�"޺};]"��}{ �?�4F����#�<K�b�F �kb�
�z��0�P6\4�6A&�r&�/��&;abv;b�c���um���Ȥ��Pǹ��U�����B:�&`W�鬯��� l���m���m�o�;<���yv��[�����]n�]�����s �f�M����w�6� �S;�ݒ����H��T߄� 3O��6S���3�w�m�C�IU¼�j�0��l.h�s�$���h��wΧ�gN�ۀ�Zv���j~^�=�YX��B����1��>�B���Y��׮]����<��  D �y���lB�gY�w�&y�d�9&�_���a�'�?-��P]$(�ы>���%V��G�Ay4��k��)S���ɴ���z�4��e����z�ʹO���Vi>ۉ���K��j|�g�����Hj��������v� ��u�������w� �#��m/�eޏt�,�R�U|�Ǵ2��c6�ǯ��*]���4qz?�:�����;�h�!j��vL_�]'E�#����Ο#�OAwB��_0�1�??���~vղ��-3�1�3�y��:Q�޻� ݽw�>���O<0s �8�P�\���E���H�q0�S��)^��}�T���+ �0��\����,*��?�������u����E,FD3+�C�粷bU!��"{������|���.G�ku<���O�0� *�g|�T�Q�B+@��G `c�ض�+���>8�}� ��c�ݝ�ؤ�4ιv��_['(�z앧����W�B����19 ��~�}��"{]��(t�g	�F�xq��]X���>q�xư��;|T�.*"?
~�� �T�E���%��[���������C����!a�ҾǏ�H�Ң�ϙ3�=����s���I)�Â�S �g`�e&@�mN��� �:?�&Jc����]�6�|�� �s\ԩ��A�̜��i|�,_J��LLy����>��q׊x�d.4{f��H{|Ϫ��>�A�<��8�GQנ�߶�쉋��/��	�|u����l��W� |��ޝ�e�Q˒�NC*�ֵҚ1{��fz�Xݭ��ׁ@؜
�;��T1#7��k��<�_��1N�A����
���|��+4��`=��>4k��!���Mn�=JQ��s�=�v���ڿ������q�M�N�)d�ia�M�������w��������o��/]��.^����)H�;qb>9|���� �X�ndcbc#��g5/�K �p�m�q�cm������V,(P�;�'X��Y��
~��E���2��H�3U.k�h�"�@���/�����0J���q�#��(v$h%�*��j
�.ް��\�����ǲ��o���٭��~O#0 ��i6�ٗ6 P ���W7`2W h�J���e��y2�����c���t��?n̦���[9iS�6���m����t�'��ߍ�  �]T������$�|{��� xR�
'��շL��KK�ի�t����ߝ��Ν{���M�/_I�._N�/_N�.�B �Çg�%���� ����*�������q
N�Tˉ��C��"KA�~�%C��%��J�-D� �B6�s,���L�^�n��%�1�hQeA~�޽������SJ`gBA�ni�n8��u�������VA�-�����	�s��3�6��=u�  ��t�6�P��zfVm��L�gx<� ���2��߄�ڦɓ�-y�����Ip\�)\�a�3 `B�0����������u. t��!
ޙ���|{�/�����D���lVFi_3G�~�^�|�=~�=zl���9����s��<�О�?ÀzO��[
 k���}��Pl����q24�V�T.�qHP.}�d�Q�參 g  }��o��-�*������Ӈ���-��w��[�w�3���?�-Z 4������xT�iґ��`f��3
���@D��;�ϙ}��ᘽ1 ��hA|���_��y����w�1>y@a�`a��Áf�M�f�	�l���h4�
`��@<�  @ �sL�3gy�gϞIW�"��*��]��LڿEv���ܙ>��Ep%��� � �J�>G����9��/(� ��'��Ç-����w    IDAT ��S'��S󖙀`E����e��u	<t$��=�.0S?0�ɉY��t�s��nR�/��܀���[���$B����oD��1ȭ�`��vO<
2�����9���H����H] 6�x�*Z�c���4:W�6�6q��}��q���1  蚓��� ���-b�+`���-�д�ƀ�x_�lbT���]te��\�H���6�L[@xH�s��~m5�3�0� E�?��=�Ξ;��\�2�W.3���TVd�bb����PD�57J�['����Ç��Ǧh���>�.\��.\�@�-\�O�Lg�E\�#Y.a @�	d�}�@A����5��s��ٲ���~
�S��U��P��(p�k�jnrW=�L��?
q|��Ez��1Uz��	��X��(�A���O�z4+%���U �8p<�;
��%5��B�N�%�K@���6 ʯ�9������ �����2ŏ����w[�M��ߕ��OI����iI�QՂ�����tO���]A�z�ڇ󦧧Ҽ�����~��Y2����ҥ�ԂhG"�,PM5o��W)�"N �ҵ�3�*����\���HH1�,�ʮ|�DA��/\H�σ{�۳gP�T:{�e ��"��B�g[~�����p+
���O�^�YqB�ͻi�� *�c)0��A�Dh�R�<H��3���b�C�S޻���{�^��K���L%	�R�R�9�N[��4!)��W��x Ѫ�O�O��9���� |�{��з |���>�Y ��� ��k]�Gtd�WKq�����JYfVg��o~�ᆜ|� ����ퟤ�>h֧N��b;�a�9���}g��T��b���v���K�r�V�͐`�������
�H���5
����}0��yT <C`�(�ҚV�!��o\dI��Pgb"3��l��[�-�@�e3���j�UC&��̐�U��s����˗S��-���r�@���Iz��1Y`�Qb ��'`(ސ�ʚ����Y�[��wF��� <�����~���y>����Z%�{<�7F`  {`G	�����@�XL�)���1õ�R<�xV�l*�l<��5��u'��Ll����v�>_!���p`f:���߄�9�'O�$. �G{���1�[��
@BA�Z�}c3-/-�(6�?y�$=y�4=y��'�&3����}��\:N}8A\ ��ŋ���	/^" ���D5�I�h�]��P��dK��ߗ�?U(�H�����Jv� �rئ]*G��� �w���`	�A������z�MZx�-|��^�J��˅W���^4G
�+�GL<0B��"�?��W_�����2���;D�5 ������> �-�x�R�w�n�?���]��uЪŷ����'!��R*�;�)'7�C.�� Ђo_`	 P�g�����yh��?�<���BW��ޡP�H�30)jh!�ו�7���h�(M�W�(
-�i�R��i0 �
@�#���@�D�n ����v������!��`Qbp{�>u�}�^j��|a��,�߾N���1!_�g{���{L����o޾��������b*���|��f~�`f�B���Օũ��ȸ6�,��T�����|^�i hvd����G�h#0 ��gl;¿dc�|�'D_�syO�yX�o
��(3r~X!�)�T��v��[ \�{|{�2/Z���D�T�SZ_rh�:U�������ѣ�w��Ҭ��v}����NU��Qio�Zz^#$s�l�l͠�B �������_�@�������=y�$1�[ �`�&�$-��w��,��z1"�N8w�\:@i����Hn$�z��B�nQ�H����*h,�F���גk��fC�-�(p�*��<�/Ѹrq$����H�>R�?Z����~X�BcWN �&~�/�l>�<! ���a��wl�r�� ��-tO�8 ���u'��΃�6�^�Tj��9�~��@\Zֵ�2�OZ�N� H����f�k��j�N��*�I%�FP�3�	��w�d��~�0@.<� |"ԙ����SD��Z�#��m����3�+C  8��"�LZ����w'�!�����W�Uk�#N@����d֧XN=������M ���7���.PH�f�355������,�^�XSE�������e���Q#V�B?^���W Z��A�K9���<�T>x�0ݿ� ݧ�D��&��E ��ޏ�x=R�?�r�"Ƞ6� 2��u쁁��dW6�[������W�}�{�X��p�; k�v �v8��G\���ck���U�k�7P��f��ǜ��#��;�&kK��'AUl�Ɂ�n�0N"ܕ�Ωx4�=�_����ǉH�@������M��3T ��&��8�q� ;��CZ����,�iz%d?�gO���G��%@+�i����2crB|��㟔B@�T\�R��/ȀȚq��3��@�L�3�[� 1f��3C������u�>{�r�f��)\A\�'�� )���,+'���2�O�B��i~į -�i�fe�Cl8^t] ��hkY.�f~Z
tM�"`�5���n�o� ���  vl�݋ @�Y�iῳ ��c�u�� ��,�#w?, 9�/Ր,�s���DX�96��)ha���[V����a�@ l�6ff�����d�� �O ��tr�[�إ�?�'ȬNOj�r���1����`����U�L�4'-��=e�|�3�S�R����gs��c�M�~��N�ST���NQ�"�.>	����Xh�ƒ���w~�B�$d|7�IN,������I�Q�4��,ߣ�Q�&)��(�����>{��>}N-�>b+HɅ~��w�a��tdDD�j����ِ������̝[E_��/�_R�g�y  =��<l  ����6���=���7��n�_���5�z0�k����4r�K�$����~��|��҅�o���� ��I[5�I�x�<;���f�j�Ґ��L��y� �?�����f$h�g0x��׀2n�4��3��]XxM%�0���E �-W]l+XKx���c��p�"1^8>�}r#�L��B����� ��h�|�
`�|�*hs��C
��=79r����� �A���!#���p��g���E��G�!��=J�^�NK�K�q�?|Wr���s׊�8�Y����@[mQ�z>#�),T[�}^ʱ��)aݗ�9 @�P��G `��oW�����>ǴwV�Y��@>=�,a��<�����z� 4T��9�N9�IU���s�-��l�����:������x�6)W  ���	C��'�_8�OΓ����=��NOO���4��لΛ��I��<p}���M����ݻ��CL�_��w�������U�(B����a�:[3f���ɲ �B�_�z�Z<=�<� <=x"1HP��ȳ�1*0a�'���
\�K��h`0?�۵Z �E��Gc�-�����'G���{�ڻw聾ׯ�:��9��L��i]�hr�Ǹ���Z� G�kh:���J��H}1�ż<�8;�7��G`  ��G�6�X}�{����Ղ�x��#�US��<65���$�sj�z�]?P��Z�@@��8s�h�,|U8{�?��?�N�8F$>��?�>��08u��,d�� �C����
5�9�->�����N���;������������
Z�����~j�pMܳ6ɴ��@mpnݼ�nݾI��۷�8�fg������ V$�E��.tf�Q`��W�W+��X�2��}�h�z�	�����#"�O' �����/�`S|��-ǖ_~x�b��T�� �.Ez�P����e9M�������iVXz�?��G`  � }AB�Wog�m��y�PWM6Zj 
䍟S�8�-"ԝ�G�٪�H�J(4L�6*���D$E���&q�����>�d��/�{���?
|h�ǎ�|~,;~4?v���U�+�� "��
%Μ`�B	B�)|?���>N�>&k L��;��V?1�����E]5��޻Iq  �Q��`E��������@�Oq�!�M��0]^]6 ���l�� ]w���_�1؎��C��|�BT�_��5�������/��>�7oޒec�������ю�B��;zV1����������ڹ��b{�߶��@��lm��Vׇ��� ���8�����ka�g��=Jm�M�y4���y�fM�+|ה36I�L.��<(�����i�"fY�Ѡ:c���e�?� �?[���<}�����|�����#�2�9L���gr|r9n����TnV��B���;|�� T�C }��$`�`���/��%Q2�bs{0����D��h�q�=p�Ȁ@]��i
�4G��&U)���^$�{Q��k|~qE���h�!�:���!��`�>WI�� ?�<�/��2Z "�?f"�E�Qo�s]�Q�E���_߂U�b��W�Y�T�g�7}V䷰?�pk��wl��= � ؊������X~�_�6�m�]C���Jtp����>��ic|�/_>�U��?�U|VWC�8��ֵ�<��-\	&�9�,E�[��l�=8��Φ�`�C{����/��1�v��3$u\���s=��W��U*����}��*��e�߷���9P	�Ш�[�V~\���j�-!b���@��E` �Jm|N� �QL�� x2��s.5�/6�E _d.�
_B�*f~�I��?Y��B��>��v��$+�z�H ��" 2�h�͞`�[uvI�:X�_��/J`G`�WE���aޖ�o;�C���%��[��d]�i�z\d8d���  � ;�r�	�� 5�ߵ�#&�44�g��ǎ�`3pԣE�ڒ�Q�+���.S�M�R���V�XX��^m��>HJ��'�t� D��-��g� �����#֙b�\+/�I����  $��]\\�b3\n�)�  �wv	�;��ȍ�����,��� ��*���H>cBA�Hq��,�7\�|���/��E> H
�0.=� 6�Az'9�M��Z�� ��x��홓98��ʂ%��R�`O�q~�$�|�� ��Qv 2�Q��1�F�i�����P9wWT�
c��	�T�;V�N��B� .K�� �v����  ��K]�� ���"&@3��Ϧ�x����G P��5<Q6&&H�_ZZJK���b#¦���%��5���, 
�ܓ(}�j_�����8h!���'�����p��Ò[  �!��L�����X�J� �~�V��!(�+�qFE���1�g��YVX�k`";0~��  ir� �_���]��Z�v�
���4��������J��~��&煠���컎���/���6	`)����>~~���rb�8O����䭼!}ՃR�2�l��R�j��k䂳�>���n��5 ����� t���t�  �( ��Z}��_�С��q�[����=v�Zh�l%�L�'�zc�r���V%�{U���M���o�Aۑ��@��I���Of~r�;b�j�A�
 T�c#T�>Ջ_����t���A;%z2?�'2e�{��9��i�Yj)��Mś���d�q���y��m䬡#�Qc��r��������#G�Rr�]7+���X
�Y�$�-fHh���
�!�v��#��5mD\'��*�^�B�?� j�S��gī��9*K�[i��j� �Kq@���؛$��2����(��o���W �x�>�o � @M��7�zT�����`����pea{�Z���K��!Z]�X����qB$�ȯ�,���g5�?Z8�m�|��(���dx�w�7c�a�6)��UD�D��J�\~�H�>�~�}(8��[�`��hilF���F>z��ʴ}�d���.ڳ�LɎ��B��1��O0U0�!�2<�Rq� ��\Ẋ�* _u�3x�3��%�*����Lr��y---�k�
c���*�I�b)�;!�� 3�c��j|���"<���Y-
�������f)��m�6�}0 ��v���~#0 � ti����y.7�� j���~�� �E����S@���?�Ax3i�|�l5P�Z2��2�*U����K��^Z�-k�4��^����HK���O��G���f��CZ��t�Ah�wb�b#%2��I�
+#MjR"#"	�
(Q���XD��hL�E�,#���E�,���p� b88%-

1���fk��#4	�4��)(A"��cM������I�����Đ,-/�y	�����qN�s;-6As.��dO%	��P�{�S���+,ؾ���YY" �'І��� �! @�u�?>^)�s�A���������l5�����4Ofz��a- ;�pPhk���s���xM�g>{D�ڪWTS�"�E���s��Q�:�����Y(�l���社/��Q��Ef�Cz�5��5�L}�:~ƌHs#DCƞ�Y,ht���P�,�K&� �c��B��%��B�n'�c��z�О"�o$MP�S��5�hP���A��,�XW �0�(�
���S�� �^�f����/�b�Q����z����#�� �Nv�P�������C�Z�W�]0 ���pt� � e`�iG�|m�߅�h��O7˸ɗ�B�"�a^��@�4!pH��v�ٙMР���&/-,q��iil�!�<
�Q�B�5t������H��B�SQ*.�y���C����f��x!��&�dQe�$���s�MLs Q��`�S"{���u�_�"@�'��y8q�j����sx�\�!Ѐ�mV�r�}m(x�Ҹ
>~�D��S�����s�����sJ���q��̌��ǝ��- ��{0+�]�F�����,����ТVnu�{ ��h��F`  � �\�ͺ+���p6@���`cD:�@��_�r��(���pZ^�? ����§�g	��a&�@�ҠJ�O�q�>>��a��TE��]&�S?|�j�G�v�k`��GQ#4a�����+@�c����L�����T�����/JgF䣑��- �̓��!�8��k"�;���
������� I�DF����w�G��X���>X0֑����{�0��2[�2s���	 2x �
��ϝ%~( `�l ������=+��, C�� ��e ����p�������  6^l�Q+��Sa���Н��s�#H�M�l��HhPx������d���uR�7�l��׮G�S����9׭~#!����������#i����`�[���x���0�/�W@�Y�{`����b�v��X�<� "��8����U�1Sd�׏dj�+A��'�5�e;p�l���|���l�dIc+ @��bZD���"�h|e>𝟤���(�% {]�o�ĭғ?O����r}��]r��Wo�P>cߵ7�wG`  _ tm"]o!��&�̷M����~������Hx�)����P��?�6)5��o���A�`�c2�@	\�H��-�9���`y��T�j$��$�(��3	q���s䣮��X5?�U���%�{�� u�cA�Q�\Ty����:N��}ɱ+Ɂ� a��%��a�z��A��) @�,)�Rj?d�&Z,4�.%�&쉬gͫ� `0@A�������Z�L`���],����sA���k	�JA�[J�2o�j5���a_�I��[��5����󗦻3�?� ��>½�1�We[\��9%0�ls ���|�� �S�����ʄH�"����>\^��
@�P�~�7D T�ӽ]�����+>�4�i}��X9�IC�R��9���J�� ��s���EoTYe��z���`�)�0�	T�
[APA����e    IDAT/��@��*;Q�u��c�5�0H�$��!Vd��5��i�Ԁ5G�=l�3��|-Bx��g�Wp���a��;ND�A5$�@��
���1W�*b����S�#m~{�iv$���Q�؍v4�ze#h�BA���=��n4�=��  �
 ����9�����Q	 Jb��
�4��Xs�>Tc���A-6c���S%��i�% @P��P �� �UM9�K0V8g��@<-˫-����D���J������-�,�U3Ww�k�
��n��U��+9M5o��
���~ ᖯDd�NdZ��V5Z� a¨����r,pj�߭I��R�{�M �Z�	v�#G�˥���JNcP� �H9����T�^������Ռ�l��:�� z��ޔ䕣 �=
��O �� `�?v��QP�`]�k:k=�_ms���כ��DuX���6; q�2��=Z�P��¼�ۣ�G���*1�ӹ�
3?�bP�������OY���q:?���ۜCV{�;��"�㙳�vB1 �[f$; ����y�LFC����>��Ɯ89i.�iXf�ס�?��՝&H|��I�+J�Zq������ϑ������kW@��,*2�:o�-2!��XUp���1�  ?�����{�N�C#0 �� `��m���	�����2�L��M2���:��;aD�)r-S���J�����u!�y�~�<'��ͱp�>~����Z{*�9����\���qү�����lPb�}^���]SB�81���P#�Y�U�V3/���� �V�N��V���Z���6�f�\�%0���gN����,_ð���­�#R��[L�z��� �tʞ���r�*}�Oi�{\*teqb�(A\�~7@�/�@@��m����"�6  �`�Z��^Ne�Q�f��)�d�\���yS��?h�~%5j�����y X���BC��B9y޵=���b�}M�G�k�`3R �X���pE:5�G�o;�2h��V�n1 j�Д�P��GS2�@��؜�^8��.��(��E,�l�x�.`Z��[���=�����ݵ�%xs�R�����Slp1��U�ba�rR��͟����,�3of�*;q�A����~�c � ���M��%�����5�] ����)pd�l\4��C�_i9�?�P7�Vn�A�Jr i����+�(h��'�zd$�����dA�Z�/Y=P����6߶s��}�Ҽ�Q���(��wx�,p��0ڵNb�k�9O����k3�7�Y|%�s�u�j%��	�j�j�(��	1� �|��\��;�5z���� `�  
��"} ���_�� ��ݰ�^��6OC�W��mS��k��NUNۄ?�����Pim~���6�'�0!"I� �"<B?s�7�t�O�|w�.}VKFx�ڸ��W���>6PŖv�Q�eF�ȵ 8`�������
���J��F���坴�{�4��I?� �7 �P��w�x���Z����S�7#����ǫUFTdn��&z�����^��m�a$�Y�D͟�U�-HzF �p�&�,hhv(�|f���j3�\��a�Z/a��� D[�� �1�nt]���W�%��j��� �9�q�x��=����#�� ` P#sيE>�Zm�[��a�ͤ���-�kB���\(4}�m�a` ��F~�Ξ�.�f}i%'ߺ&�i*^t�x�����L�������������tF?�y^�y�aG��7�is]�=�A��z���; �+��;kо�7���;��ng���F`  =@���ԫё�|���jp���Y(���hG-�����,���{X^g�P����o�m��M���j�b6��_gS5nU�w��%t4l �x� ��'.F����fb��k^�r�K]�
�'s�Hn�h��=M�]�� @�a��:�g���1_����F`  c �ęF���Pj�e��VE!�T�n����Zн�mT}� PFh���R��`@�@��$2�t�f�K2��ᛜ* �-���N�)p�V֔�T���yM��GUe��|u���M�c���b���m��j[��.m����- }F��1{O8O��#0 ��c���|7 @�@/� ��ߝ%� ��5��v^����O�i�n�k�_g����#w:=X
J��\^����j�%��T�@+����}��2 h
�:ph�{1S���%�t�0~���%��m�s��}�� TƮ��/d�Q�{����U�� �' ��ۙ���!�, m)����6@];^-Ȭ]lޥ*���5j�FX��n1�)K�f�\v��&��\����������)��M�T0��- �dMT����u����a�܅6�����n��ZG����� I{�{�A�Z+��z�֑G��s��X�S�� ��x����a�^�rR�b���h]hr����W8h��������ۺ\lv�.���q�������Z�Zb� �˼+��T�S�]"�aߑS�ҩ��g��8�5�����r�Q ��	�����o��Q����e�7&�#ĩ��7�O�5׽��vam���� �6x�^��{r �kZeS���E�6հ�VI�o0�b " (-*����z�����В�6���#̼�[��ަx�)}��=����?���E���C���BuE�{ �?�ϭ��UbqG; h�ֿ�5�>ڎ�	�R����ε��M��$�9����l�>���~p�����v��[��p��5 �5^�~��^v�N,��!� :5.��m��v� �plcs��&�i��|�ik���7=��0�:� H����>m�MkQ����)g?j
2���~&�s���D9Z��Vy���`?#~S�D��?��W�j��"�+V�^���9�+��W�眾c��Bz����9��� @�Y� �f>7k<����ͽ�P �z(IZ�
z=Ʈ��
�g�l������ �P�H���k �ʘ��
 P[ h�
`��'�ϭg�@��Դ 4M�Ե��
��B`bG-I�d���w%��8&a����FX�x`z��>Ǵ]��]��m����z����� ��츦�` �?KZ���C8e  �@@@l{v�+֥)���iGm�5�����G�.3 �x��X��@�+��'?�P������/*�O)��8��ث	��}, u���;�] U�� �h��\-�)F��>�_�ct~ڎ��5�5��׸�W�b�[�� ��p�	�4�ޗ�����(K�DA�����K����u��G��{��rJOa��.����ud>
��L�����s�����H�Ga�c  ���dX�j7Gͷ<��#��'�;���u݉k��#��}�i'�9\�G� |G3UK���j����nl�@@_ �%���ט�Sj��`�D�Z���Q 1�S��5XzJ��~� A��X�]_c�.�Q���o����%�[����ao��H���:0�P;g��N]g��ug��ٙ�W�AF`  cNT[@�m�-����j��5����Y���o����6ү$�ڹ��%-O�� `À��Ř/�#�n+�tu��<��o�� @�P �QXb' ��,}�{�<��o(I��V@�8 `'��N^k�gۇ��{�����#0 ��'��p�T)�G��5�@m������47�f �V�NX �<�� �Jp��@ ���Xh��׏���'�~������7�x '?_Wa�~ ��Xm�Л� (��(a; ����^�ƿ�p��� ly]h�{߀#׼�hJ���@�-�۴��t��#fП�"��^/�<���A Q��@����KԿecH��a�@1�����  � ��T8���ijq�����4��qVך쵌�s�]���n�� [y�w�[�Ǹ����q/:�GF`  cL�kh�����9H�]7���b� � {G˗�i�c������@մ��8n?���v1�x�b_+��;W�ĺ�����F&��hG���u��c��ڻǯ��1�~h�@̨��{} ��;�GO����ca�ё�{ �=F,ʃ��4��LR=�qK��+s�K?���s-&���}_��ǵݩ���UpP�7� ��.��)P�^����S� �(��i]/�fpӀŐX�?[�l��f�������,��>= �<~[��=_�={�xc?��gnx�� @�%��/&ȏ� @����s c��ff�.�[��1#���g[�sL� � _�[��6���]l>_͐ވ�h�U {,������WZM5���g�"B]�|7 ����RJ-��������3�7B��譎��06�r^~�{ ���F�'d��Ds����� �e�V �.�R����G�r��}{�cz�	zߨ\�v 47�\@wQ��gT�/-
Aۯ� d@P"�@�	H��~ `��ά�Z%��SmG���ݙ��]�_�����^��?{� c6�"j>`I/sM��D�m�U
au�h
�?|�D��������9������mS��yE�Q�Ӷ|��GҬ���ޓ2�U���O��')�o2M��$��3��1��__������gTVG�mU6T�w���ٕ~��}WZc�����z�����D��1������8 ��f�_@ߨ=P/�4ӺJ�@�9�/���	��쀣^����柙���?zP��GB���\;��"�����y`��p��i\��������5#����>��g�_>Sv@ۿ���smoE�ċv�h��1ƍ����7]��T��V�t��[y��G� @�y��M��|��G�n4�P�gvA�����5�u��c��f����v��Z�Jw�"cK��	䆖�g� ����I����(� ����45=�������t���r������z����V�Y[����?p�}�e׎Wx�|9z�����m�7߽D����}l���=$=�M�z}{1�so��Ù?� �׼E�7�ͻ��Շ�`=�n.�UP�߮ t�*M�
 b,��l77� p��M�F���[; ZF��
�.uE�,6��0�jf�ܗ&���`f&��?�q#��˗/��Oi������'�P��i��x �ka� ]�黮�ܯ/hɯշ�RH����I�Fm���ܡ�1m�v{���;#0 ��s�Q�.����Z�^3�v�~�j�5��w��z=��al�)�DZ���4���)�}�U�Cm�M����r��l�`����SS�����4w�P���K�ͥ��H��g���ZZ\\J���%�/O��9��Wp���6����������Ϯ#��������2��S.�z��y����} �{�eSaۖ�V���������@��Y��V �}0]��c�BB�7�0ڽ��w��P�-��.��7d݉&�>on����4==�ff��܏�ѣG������c�����ѣG���y�}�+++�����y�۵���14g��y�9.]���KQ�F㞭������v�L�*����=k��6�}�ډ� н�~�# 0���?/���%���&��Q��2?��or|/ `���>���[�R�f��_ql��V� ��G���h
&���h����K@�|�f�?9�8�fg�f����OgN�N�Ϝ����y��Z5���������y!-��m�i)j¡K`�<g%�s���\�����5��gn�P4N�Z?��ѻ�[�=s�qmD��73 ��k�4��>�t]JAB��}Þ�U�4�\�Q�!��吃��oh]���wB�v�Z_d۲���ф&��)�K�U4|�l �_AZ.����  ��H�
�5�ӟ��6��?7w0<x0��3w0�={&]�x�>�ΝK��W>~L++�y��]z��Iz��	��?�X w��( @�84-,���(]Rc�,_��G�v ��>���R���qޕzߺE������}v�K��̮���>��wF`  =�2�u��,��0��o5k�|.�U�L�;.�d���ZJ~d ���ͩ��pz��j5@�D��1>~(X�(f� ��̤���K�y���-�O@ �; ���t��!j>�.]���_���]�J��K����rZZ^�vi9�ZXH��=Hw��O���Ow��O�+��'XNz	�>�8���ز��C�v{���}����Tz���a��H�6�r��=�x\��>O1��F`  =&Z�������M�^H��?����e��/_>�O���ZZ��f��V�3�{|� ��| f�6�>�Wߝ����!,�k `ԽZ� ��kO�A@�	�`�07@����X0ƪ����$O.����?�_�|1ݸq��?�+W.S�?� �Z ��νt�.��WL�;hv]�~kA�e1�`Ԝ�kf��ֵȀ��� �r�ޮ�у4Z(�Y����1]g����o�p�^� ��Uw�A�:t(�Qއ(�ܟ�|I����1-.-�EDy/.���%1e�BA�eFI�#�O*�i9Y�8  ��*��Zh��6@��x��!�[I]�W���=h��??�f?��|��P���O�g�^�(�5N���A�쮂) s��S��� �D�+x��u�{�^���=���.�8 `c���C�m��*^]�+�+�k����2 �pC�st���/P�P·��ѽ`E�S]���m`O��g.t ��� �sQo���|nDz�;��N��S��ܡ���
-�I]�VW���녅��������GU�<�#�JhR��"B�χ�s=���l䵁)~�Ό� �/�y��G�6�/�#�b�٬V����B�}���>��E����~N�8������$@xx.]���t�Z �� ���p�>k�w �	[�r��#��dRЯ��X��a<�@��r� ~�[�uvԃw��qĆ?U�5�|�Z����wDV���h�t����N���}� �A� �u!�{��l�E;;�.�?��_8�Ο?�.����;JD.�>���c���cZXx��<}��<~���}�$��{� 3f�{���i_��ہkn�]���Vб�5�f ��K���ƭ	:��8 ��B�`���44p���&��P����L���|�C�R�?L���z� ^� n X �?� j����	�N:�Q/A�⵹e������ ��H_F���=jo��M�^6�w��[�����[���<�6���8 ���Z]��3 �  )^�����F�ڵt������S'���r�y��Y�{�n�A �F�{
�����{�h������Jm��Vhg0\ m��� ��"�ϦϘ��SK@����VR)g�~��k��F����[� ���@� ��7p=ݼy�b ��//�P�1 j��@ ?=���v�_W[��j�PuIumX5Ý� @;qy��,�)���ٹ���.4�>*v���<������}G4?�~�>��ӧ�O�  Z��~  ڝ��C�ҍ���uhxҞ:u*-/- @�7�gO��;  w�X� �45E�|�;8Ьr�
H���c�d����ja&�C7��]�H�*[��	�}��$!
 ��0¨�)q�l���9ُ��s\�����T��l������ P6 �  �5@��CF�����ȇE�x�T�ڴj6��u�,��d�����ĕ�s�m�[��:�֋�һ�h�`�k�BSڗs�f|��v���XЎ+b4X��狮ojK�k}�s�F�����q�����؞���P]36 �lbJ^{p\s�r�?e��]\�3�f�Q�ho��� ( �v)=}&�;w�
p��]�zG$��2�`��k�Gr8�&lh��;�h�/� �]�.l�3
|�f�?9O:��?&7z0�P�ϡC`���L>5�E�N�5Q��+�pqc��{���Ȅ��5�w<��,Di}\�|)����q=ݼ \ l!�t� P6���� ;sShG���c�\D�����o<��C    IDAT�#6M�\X9�������o�߸��(l�9�E�ְ�Z��<t��dX�.��$<��(T�n>wml]���r	8u&P��<���zV�R�Yt��,e}�6ZS���#���FݔH,S�^�1�٫�oQ�%�C�됂:ńf�G���fGv�b/�;6��{j�vw}UC�G˪�{�PV�k,����v^$����5;u� �z� A^ ���������  1 *ZT���3`h]]f��e�]P�J/�_?#���ReC�{dS����fJ���pqT�X5�%�`�ȯ��Em���`���b.G匎���	u�e���@, d%b p�b �Y  �� 2�K  � 5	����+b�9��ݭ���XXֈ�VJۯ�@ˬU������d&`L��Q�%�A�<��I������W�L3�*b�go���ŝ���÷�j�m��H�z��hz)��ٝ���ֆd���q� �\�Ğ�_�  Jf���
��L�ړ��wm��M�)(�x��Y��$IԎB]G��5�%���0T������Gtɱ�En1D~��.��-$q7�  ʦr&j���u�lUΞ�����w���A��ܲC5d5�<� 4 @7v�,, ��` @@ \ w��Kw�x��}���BR9o.f�Ҿo��`/� L��Wl>6˺���J6Y4&rJ ����,ژ�{��y�������Kꆨ��5Χ80���^�&~��O��D�G���k�mʮL ��!>��� �%���8��� 8 ЌĜ@�7*}� �ݨlm�涓Ƹ�6n^�a�P!RP�s�g��g����Ӆ��|�OW/H��+s7�|/Q�~�~!`D-�ëe��V?�^��	w�1�w��]5�PuA�{[�]����l�`9Pa�R<O�Q:�r�'?�
����-��~�u�s/�` K��#؋מ�������y��ȁ��8��݂���.` 4�S�>r����ҝU��w���&��Dv�(/G釶 �I/�r��/�>�1�� k����\ ��u�  bz[$0�L] �\oX T �G��n����̛j���BLG� ۤ�S�_l�1�@��"t��w*r{�)�Xi˜�
j��}������@��9�jY�_r_�M
`PӾ
��{E�xy`��1@�|.���{ (���%�� E�W&@d�( @, � KK+|uC{̜51�]����-*d��(5����vS�)ن�TL�	<*6�x���G�O<bp-�E?�� �k�9S`.Ԋ@R���E���
w3F�DB ����ᕅ��8��zJ�ͭԧ���"-J�'g��xE���{�[{"��D9������n�m0�sAI��gΪ�jo	���w��G�^P8gﵪfU͚��2�4�4��ӽ��s�k�۝uQ�' Ɣ�T^���)7���
G�@�_@M�5��s���?�����n�'��O��r.����|�_ ����g�W� LQ��M�����͍C���2�̠�����S����={�'�'O�N�`=��oˤw���������͛Í�o7Xo��V�I��uu�5���(�����P����<lѺe��<z�
�l6o񟑱�sFY0^�E eA�
Zb�̄׵a�uu-D�xO����j+U6�bFD��Tp{�ՁM+���foQQd 6v��ޤM�D�ɏ�5aW�C��J��3[�[�	���V����3ZӺ��۾c��c���?~\Y"� ��+�.�� @+5�8�S�L�ɳf�2�H�������j��p/؏k)h�}iq��/mm��u��i#*X��y*�ȱ9���5ZLVƸP"iEsּ�8s�3����s��mf��ﯿ�{\�h;g�8;��|�����J����3��p�� �Ϙ�5�|���}Ƨ��,�$PJ�����8�}���f�dv-C���`��o����}�J��s�B�0<�|)pƚBjU[PJ۶esص�oy6o٫���s<�8�������n�d{�1�Ŗ��a��m�֘���겡�К�>� ��"{o�AP��I�����LV��F9�k �g����q��wl�d7Dp�s������Xg5�eq��#G�ٹ���^���7o�>~�h�}�: {�}�������x���o����q GΟ�������%��ݱmض}[�nf�Y�c������l��ЁX]�d�
�������ޢm���p�%ͻ�S�2��2n=I�������s���Fǡ��k��n`9��0�1���N�۶n�`㏑�e� ���������"�k�!Ξ�, ZE F ��� ((�,�� Դ�H=��4��7K���`Gۻ-��xO�<�?w��&5�პ=C�x�
���ࣗ�..���M3 ��D��A��s� ��iBlE�Vs(�}��}��4/�NR�3�M������,��`N���@ 9p��T�}V���8,^{�ӲTy�}�Z4��p����)���m�=��<nz�/9���D���ۥ��7m�ԙ���TJ��!`����/�1�/��� #�#�K4R�;w
��|&ft&����~?�_v��Qy�vx�֚*|�>7"l�Z��^3������G`leU?��kJ��HLs��쓜�½߽gOd�Y��^�^�cK�ߣ��븧�,P;��-r'��1:M͓}3������e zZ,���Q�?�K� �>�����KN����}�<�9+X%�m�$���'���T
�ueeM�Pf�� �ÿ��F�M����4�źef�Hx���#�����P�jn���D�����C�V�)׉�����G��h`#�_�������L�Ŧ��F������#�`�<�>�[d@���}ssZ��f%�LFұ� �L��P���;E��.��z�Ȣ�?@�O�nÀx���� x�:D��-�-�R~:f���"A��Jyj�b$�Y1�@ ���(���w�«�]@I�Usp���u�Y���ysԳ�~+��VKm&�����h�t�[��|n�����k�C�C2X
��c���8�9ѱ�%�_ hE��� g;�����KKK������/Al�<2Q	(u��� /�%���5�������;�;w(����QVȌ���&E��)��ՁJ+���岼�-jGf�+ۤ��wvvػw�0�wV{p+v��?����;>�	 *3 ��/_H:�EH�s��#��3��7uְw���5k��K}^1e7������m��_�|9��k�ney���:?�;ճ'k��O�>���W�m��F�����������������@ɈM�߿Z	�����6����|
L�g
 �f��;ꟕ�߿0?,,���燅������avvv�պW����mD�ou�=z4<z�H��G�����,kZ߽_������ŋz�!I#���,�i�{�����	��z��^��ډ��Aq���h�U�=ˎ�D����{���!c�����΢E
7L����>W쳞�S}�"7����tco@Qof5vx�N��j)D��-Iw�V�Vu��t*Y��a�R��G��H���Ç�N�R���S�J��c�\0���,��m�2`P%*J�����'@�u�>�,Mhl�5�p�2��j�	��Ϟk\��χ������P+��Z�}�����P*�p��z{�V�<���X6���/�V���x���é����gz�^��k �8��;w�~���~<o��3��ַ��G�5���<ϟ?�tv�3�ӭD�x1dy���4{4g;Pv+Jm���K�=);�c;�����26�R��U����uR)����������m 'e0��5�k�� &9?��~��ӧO��Ϟ�X�>UFR�d��{�gC�.Zw���x���>�L@�Lfb��-蘐G�~i�%J���C������B?;k���<T�G������w��c�frz,�+Ka�d��� &��2 ��:����Q꿂�) `��赑sݿ ������0�ڹ#d�w;w�P�0�BV��ٳ�Ó'lJo�wo1�lt_Z6|��4V�0��U*׵?�с��!�{�`A��Y"A����ؾsخ��N9�L�gz��/�^K/�d��^��<y�dx���]?��-���Ǥ�[\�}�(e#���ɉNA���iw�J����I+¨�PS��0����p,..G��G��G
��9WgW3-�Q����kGM�Y�:A��a(�����;& �ٞO � t�&4�2���֖��qi��xNŮݻ-�|5{�;
�'>O/�]�Oq\��x�.Q�,���[}��K�?�zׁ�u�պ|� `d�6P�l ��JL�i��,;��g+.��9�@���StǪ���=�� ��#~e��j}�<ܻw_ w���ݽ7<��R�&~FI*�N��{u]}�9Tv�<2���=�s�!a��B��jc %D�ϟg�j����p}�ld�⃋ ���şe{�;d*v��� N�'�M��%H��Ç�ž���\��������l����f1��S8�b�[��@M����Uj `��Q��cǇcǏ{=vL��~v��o�[�n7o�nݺ5ܼuK6}���{�6���
�T� ��W�=MyM���J`$q�9�{� ��p� i�ƈ����@۔&b3�.+�`��_�޾����w+B�ihY�p( r�  G"^w��%�2� ��煐3���o�6��+I`ٺm]]�&��H�ˊZp�	p
E�Ju2�x�a��o��{��m���-e^�ۭN����ߥ�P�v�K��\�ia��HK���%�����ࡃ��C��1$�0�E�N�Q��@��p��߽w���;���$��p=�(. +у��)�X�m�d ��m�#��qS#y�\5���`� k�T�-���`��qZ|�"pc�G�G��v���*�r�����"H_�ͪf���Ɍ��#�Ҍ��Z����z!��<�-��G
q����|�v��*� 3xD�  H�LsT*;��5�Tp��`U����W� |����?��������ЛN?W��@�ӱ�-R0�0�g�2 �&ߥ�c�	n��>:�-��1���~:�س�#u0�^���� O2i�#�����D�� '����k����}��+c ���qv�,(`󪌁R�O#�tx���c�fV����=$Ӛم���;6=zLΟ�2n~V�5�^n߾k�ם;���K�ϛ��)��'q���Y����g �����U8 ���l~*�?�u�=i�ީa~_şi�����a�S[��z֪�RP��A0�uo�o޾�6�������0��{��+�"� ����{�?S�s�w�B��׵+�D��Em+���RǢt�BL2\z���5�����//�ܴ��T"�R�������U�h��{^u�����Ն޶�6z/9��G���=q��u^K��$����W��Y�b�9e�C�.�0���+u�8x� �ߑ3  x�0 t P�4`��ϊ��f�u  ;��EAa��h&�ɏ&k��M&9f�&@�τ,�=Q�A���j��l�l��<}�n�k=�6Ծ��X�ґԸ���6 ���(Q���-��Gz���ܜ@u:�$wbg��6o��I�Ͼ�=���x%�(pզ�D_�֞QgA��H�n͕pd�)u���.�EDm�����7v<lQ�y�sR�]ukg*3��ײlX��,�qN�� ��g���s�t��T�@	���6� d��Q0�<�򪥫�h��G87���k~���(�<�`k�%�Xd]ͽ
0v�����J��~�6�A#܋,	�i�"���_��k�\Ɣ�����{�V�G��6�e�z+��h��40���>�O쇴,�K��] �TִP����Dalڋ��d4�g|?�����E�8|�앿�]S��8>��>v�V����ej�o�7���@1��o�v�����T�h�)���>�A6�N��"�����?��
贂k�ٻ�٭�����G� �	���������J_t1�#���j���{J�	��F(�|�U���N,��% /���g�F^BD�r�u\ ����V�%���{�a��i�i[������ ��[�p  ��Y�"�Š!">���d����{�#���"���P� ��~�d1�Uʠ��}-#
�5W��ly�U�U���E?�6����<�~��ua�V�)(�'Z@b���=��9e}��)~��-�oR/�ZY�`�g�D{��3!�f�h�mhzD� 	@r(�P�V$Ζ{�{^@ {� �}CI"xG�T (E��w�sS��Pf�b�.4���Ǖs����#�+�~ʃ�9b�E�[�vO��B��-ɽ��{'2�Z�2I�Gy�����g�m����y����u�%�6�mYY ��7o�l��W ��0�知�<�|��ţ�~���*�d�!����� ��-�3o$�阽ҏ�X�����y`��� �Gw�8�����.�§j�z�T� �=|���-��!�L���Οǭ���
,��\O��y|�� F��6��������F���~�qcx�b)H6&� h7<q��p��q��"vd�/C��gt����6�?���Ae	���x���0���)������@��2�gK��dNF�������1^Fh�հ��d����Y]�gL�C��~Z7ۄǈ1X	���Q�4��J��1R��H>7�L�W�����#�=JaVf=  r(��� ��u��}�� R��ճ�V�a��G�
������= 	Ɵ=��$;��m���Xg]���7o�Y��ƍ��֛J�:�����+�`�o@�fq��j�sG:��bR�����CG��RX�����9������5��aZ�s#VT�hm�	Zw��'�gz�@w.��7��1:���E��!ש,��F�.���p���P�
�9��n�����P�
���(8 ���b��Q)��ǎ�?~LW K�&��g��B�,��[&Ť`�ڧ�>?x����#Sj{�,�	86��S豜P�"9*d3!�^�vm�������k�իה(�o��qY�� M�kV�ϑ#���#G��Ês���*��do�?�9�#  ;��}��m��k�3�V� �EGl5���+G�Ŝ���W �@E����& �숱�I|�=��V/�_��0���/y^@J_�>,-=o"NCn�A��ψ`&N�X�^
�o�5�l[Rz2Rm�}�u�a����y&���`�
oCp�u{�%������G 8��C�Au�cS9ё�,�\�+�[+x2_��V���C,��|�4���9�L�&S��DΕ��Hզ0���Z�G&۾���[������H��z5<|��9~��իc �u�$��x���"Be`s\��&x�"���^೩5��$(�y��:h�(����~�^S�J��̀��d��	��^�$�U�|}*�M����WeO�i+W:-6��ر��1�ձc:��w�{�͵�������s��^���D�U;�;x��y��'� �كvK��p�s�eFD#.8� �w��8'a�Ɲ�=�N`�u�A�q
 �{wȕ �����p��:;�9k%T�R&���i�Nԅ�"����#���S &_" *���ȵ������c�'XY�s��_���E�?�����������qPI�=r���^!85���G�ܹ��E����?y��D�2����u�J�g��:i}��|yY`�M�:J�S�7��� �?�8�#��ua[�_�����BJίݗ��5)Ú����}�UΙڿ�W�m6P�F�L���9�������*?1�<I[��&�(i2ח�D�%5��M:����Y�-�(��6�r&�6��u���wd�nݴ{��a�ljx���ZP#�SU�Y�I�0}`i
�<�ČҒC���6n�vI�ש������?=�9}Z�����l1�w�F|ݜ?�=� �����Tl��`�ݶ���l�V�CJ ��JmV�0T�x�"X"Y�S�:�N    IDAT�{����(*�&!D�ZÑ���q�L@�����jE��~�{�sǁi��?��S�(��R�"�/L�@@��ȣ!��RQ*�=�;���y�v�q!��}�֖53h:�����Qk߽K����d�g7��s֬_�K��u{�^����չN�+��T������yK�h��&Q�R�B3MW��]��%/E�uL��*�&�&����mÛ����Y�?1ܺ� ��G�� .���������ϟ��t��%�ܡ=��iQ$.���H�K�u��/Éf� ��|���}�{��X=u� ܠ����˗�˿\~���V�y�=�ަv9ÐwM�;*�٣����_�$���۷d���8��ْ�c��w�`�d��X�X���e����4������O ?��7�9�ꩧ�F{�[�h��w��[A�{���R�!��3�h@mi����WM���h�	��T�c՝��U�ev���clƣ��H�Б�u}���B��ѬIu����(��(wYK X���t(s9��np���2�՜ƒ^#�5�6���.�Q2��������L��lBd<�ѥV.I6�8��?+Q4��j0p�d_8���>.Ǡ�M<��ʬ�X`���G[�h�C  ���4��k�0��*��U�(�;��Lu�I���|ϤLy� �NG�<ϱ�팀�t#�Eʾwq�0g��2���X[�3S��TW+�d&c$�ڔ�
o��(����ɨ�Y��-""�����~6Y�Q���	E�&�����'	�pv�%V%�P��5{�մ�\�{��a~�\:rX����� ��.�ܼ1ܼ�c�!G��J���:&'�@�$��g둮�<D��j R!T٭��|�P���="�)&�]�"%��!�:ӓ��e{.^�0\�tI��K�t����37���eڛ[I�{c��BV�2�lZ���"�۾�?��i���ϭ+9�ٮ\�u�r��p��_�˗���Ѥ���tiS;c� 'N8�:�6�����97�O ��m�o��W-�)E���c(�;�4��q�|Vz��?+�������e9 �y��O���O�	j&�聨�m.D��\y�]w��k\lRu��T��;CR�"
a��a�hGib����A��&�&rQ��AR�EZʩ)��ւ�4��@��` ���V��8�H#/��D.�V�H��{�-Ȋ���wԹ�$En0z�G��-�����|�XOB�)7�a'��/0҉�VL�S���̨�{�>;P9R��y^��W��=�K��)��G2�&(� ��r����=h���݇�ڡ��ZƱ�4�  ���$|��5BBBX��)����tk(�n�S�
>z���P��s���;��Q�������y��{��a�0K�W��
��̦8P���&�jO�����C�mwFh����e�A������ݺw�Q�S'O��ݞgD�8�'O�;NM��'��C�3�m�F�*f��C!��J���.Aa�Ih�qC-kM[!4�;�e�xg�`��8�St��:�E>�ޣ�3�(� dc�5NX�jKN÷��Q^�\�"���y�9�̀��믆���z�ꫯ����J��iB��l��	d7�ޕ�Y�8` FIŭ�t*��]��?g+d�56����@��s#���ǫW��^�*��W~��H�����6� <{(%��1<{F���� Ϟ��|*���ҢŇ������{"{��3�/$�"�ן� ����k� �!�H�����c���tvJ!G��=��{@P]/]�8\���K��I�3ୢ&#��b��bL�8J����VsL~j�r�G�Ú9px8��lO�@gĢu��c
��Fʃ_��{8OkÇN���VM��16xsB�Vx��}w+��lZ]�������l;Ϣ(` �>�p����"㬋���HD+R��'Y��#�m8�{
��H��MJ-J�gYF��w��5���]�lX]���x�P�E�N��O���i�Z�Ő��(f`L�$@�0��ݜ?)�s���զ](�&s��s�fN`�1����32 �\bE�[%oYP(�V=[ؿ?�\��uJ�lĪ����z�5q�=�I�|�8��G�R�uB[v�𢡄pP{r��v?עɞa�-�lUF���9ꬾQ�h��}Z��+�K�yO�O{�7��#������T���o��d}��������!�7��Y���Q��M 4���0��Mp?�	���!2n�#���'r�y��}hغu{/�<��?�s�駟���y��d��Xػ�(G~��7÷�~;|+������\�c���k �q����ş)af)Sz��޵rIrl �.���.��(kn�&G��?�� ^�5@v�6�[ $<!�8��aC,h����~����믿j����0������*��6s�|>sI�)/�KI��� �:�4��H�6d#����o R<c�z�1^-��F����?��m%���C����Y���Q��[���|��Y8�b�ò��%��f6K��e� �D}�T�Çڐ�h�l���`�Dۍ$�kN�w �԰HN;�{���N�����7�ʁH�ڨ�Mju�P�k�4I���/{�:��Ϸs	Q�X�($(�Y��-;,"����3�^xb��߁�E=O��-�qzu�"р��ѽJ�ߌԉ֬���bK�f 0�*��O��H�lz��i��R�0U̍�˱Դ)`�u�G������r�S����3&���J�ډ�~�����eEkrɉ�}�Ş˶� l07�	��m�UB�HI��������t�p?x�#%�h���gpb߹- ���8��+��t��'tN��8������Y��������gm�SƹL�j A|Y7��� �v\�1�'�)0֢$-���(���dwtعsw��Kxk���?��߇����x�5�s�{�����������������k��L���^�s�m9��9����c��MV�ۦ��l"g}�pR��ʗ�:Vu�q̔6X^�H�W�9VR2����K^/](�.�\��%a�_�rY$^J��VX�{��㽞꩜���&���]��� ���KM��1�Ŕ'���ȂM�0���~  ��^@���&Aq 0E� m4f���*LF+�ɜ95 \c-l�٤2��BB����%�(t���mZ�[�H@F��6����:�>�� i�����=�����r��6 �$%&�����.ɥ�=����DƮ\��K�m�N �e4�9���y"!���?˅�q���sR��x��*�d1N�p ���k��Q䣷{��0��E��,����T��z]CwvH��F�UQND:�#��(���>���z^�7��S�Ʌy$b�0�-g�P���.{zLlym="J"X]6���P�JZ#m�S�}�8���(V���?KHӉ�mze�D�ye��]�ZnvM�1�c������b��`w�=��^*��qP��8�U�����\�����2���J4��[)�7����������6͕�xM}�\�����s�����)Y)�)��)���Y��cd ~�I��F��r	���w������}�����dN2�N�M���9ch��*k��8T��:��3gcu  �q��m%��}LB�^��F��yK� �s W&��f'�;��|�.^М��Řh�8W�h`���H@p�����]	2�^�ȧ����O�Ŀ�`M��(��~��}_7$��������F�1  ��  �``\��ի�j�!�C��7���)2� �=������߿ rK�\X1$�c�@MbѪ��n)��$�P{�R2S��X�o���$���$�<ӃԱ�~D�קO�A?z�D�k�غ��C��t<��鸦b���o5�ߞٴ���;`:��:��F�  z�a��s�T��$�q���V<y�([� ��h�Zf���ǋ���m)I�Jف�z�J��t�a@��lu]m����9�O��ݻ{��ڮ�*���3qG�E6�ѻw-A�J��Θ�@sN����7F7�<93@���D�O8�T��x�����L��5cJ@����UWi��O�Q]��l=q�Z�A�UcwC;�5E�^G�J� u���F��3��F��I������J�����6��|��0D	 �1e� �,�*x���.m���%[=~�dRj�8Քz���Uu��Nj�iS�<�A}�*��ų������hl@��;6���T����2?|�L4Ή�֍��	+��#�͕҈���� 4���Z�#�f 8oY�L=��8��>%H�L����8�����a��YJ "r��s)�~��n���@��W�o��\�  �6F{�%��v�ؑo�O��D I`u��+�����-�{�*���0�=N�� �� �{�>?|�ȟ�l ����M�7�Q�Zi�8%T��t�g��V/^"�tq��ો�T��R�ڼI���u~6������v��o�*�h��N��=םr R�4��`�� ���Ë�Dl|��=Ώ?���l���3�u9�@�Kh�[��Q�[K��:�栗$@߲M6FѧM:N��_j�	C
����3��g�R6C�J-�	�W�����K{��d �2�nq죙]� �oUA��am��H�UQ*������#�q-�"���79DfC��U䵨_�,|w�)2 Ԯ}��߈knK�<�z��\,3�c^|��&��>qB�Jhd�����,F�g��#99�ύh�45��S�R��쮏b:�7(�켮(}�	p�^��ջM��ߩ�!�o*
�uO�tW�ϑat�,�_�f�w
a�;V;؜��
�~A�0S����&Z����`��H��f�ѯ�Ր�ք=�R���={�Z����:�~v ��m;��[��`G�i�����6�w�}��?� �����������we/<f�0.wJ�@պ�D� `� ������-Zc�^�\�4Vd=�)}qNȜ>�/�����?��q��9 �;�~@�6�
���N�k׆��°�`��V{����H�SЩ�S/�9��o 6r�"FlP�~m��~�R�A�(�_e�@v� ��{n)P��` �2 /��;߈0{�q�	 ƈ0#�L5�����_�h��7_�|�M�$˖T�_o��H]
�F�ps^ul���
��}�)'���� � �M��}#1�K��/_KX�M�U��]  ��9�0��#=3eǯ{�L���P�ej��^"�<���PN&���wR�6�} �b��냙ROA%�r[���RRY�QB�)34�Q��1$gϜ=k��Q	� D� ji����Y�,8�~�1�Գ�V�f��19D�ղ�����rۡ;phj�<	 8���@�.$��V	��?h�ĳ_]'����%)G֟�����c�:f���C�d�� &��C��]��/D��nh%
���5yfɿj��k�ln7�Y�c�q�ԋSEn����\'b)�>(�=p$���!x3�U�7�>���L�e�|{�N����xqD�V��ܥ��`���	��J~��]�7�^��\9�R�t�Ə���H�ۓ��'c�Qʩ��� ��.m�����r}�e<��C3�zſ��@�O���)�Ī*��(��/r�Kg�x��>c�3�}��5�l;�6oY��b������K�k��he�����[ܟ/	S`1��� �)�flS3;f_o��� P�"��3�М~�g�R@
n�h @�+Ҏ?��_�R� ��w9�aM���z�Y����V�,��;���2	
J�.�XIi&˺g=�-��(j��wS^`��N�AԐO��!`�E�-.�<��6><�:�]����}þ�Xm�� t 0!qN�8)��D��9���[k��T���I^�x$��8ֵ���2 �(�>�+W���=�m�m�Y�  0Y	R�m~x��<���Y�"��W��3D���y����B��2��P�#�n�{��|kMa+��m�kt�T�]7�m?Y��� �vv
$'��@�x��#E� �m��樑�^�k�8���	X��>�t�[BV;g�C�Zw�����B��Y�_ҩG�+� �����7+-�c�$��}V�s�w�}��bp���� �@������] ���t���;9�Ǧ��	��5�P@�s�����3Zz�������w��po���>;w (v����$]��J�"Q|��Rrb9 � ����[��R���g�3T�T�A���^��890�Ŀ�E��3/��0���6��>	0W$O���b':Y���=����wL���>�\��˻ˍ�E֐����D���ƍ�k��O;-3�re������@;jň��jH|rH�a����餮)��vݩ���g�Ͽ��%���� ��?+�-?+�D^}\n�L�bI[��?|����@��V��k�WR�80�J�D��i����� � �ʆ�3�	d��U �-c� �1 ��&0���HX!����1�Xb)��f�8F;$�d�$V��eK[F�0�]�6{�E�K�r��Na�. ��/�4ە˗U�u��s �ߎ�s@��Tw~g�=3�*�a4��꒘ė��J��1 x-�p�D��~��&JS��`��:ɐH\��Ja;�L��q�N+�Z%�2p�eG�ˑi��!���ڪnGC ���S:>�]�@% ��p��\�s�����s����K�V��_��2��6ym%�΁�5Q��2�9�� hN��7�re�h]2!�UvIN��T1Ʀ�p] ��OM�DK!�c�IV��&�ҭ�KjA�LuN�|��y���g�#������ʭ�8�����3�x.����Rվ��T���  ��c��_Wɢ�D�0u�])��(/^T��m�;�o�TRE�U���Qr��[��Z3=������&sZ�Ϟ#�s|3e2�~N�O�sʀԭ��d ���)�u��>�����D�sp���dnwF�ҭϜ;TQ�źuK�^ɜ����w��8.���\ͽ� ��{
j�~:�H}IN�J��L�0Lf̙4�R�� ���ￗ�����/OP���Jd�%)�:��H+m}��m6����0瀖7����Ƙt`d�E�J��  � `%��v�C���=p�����E\  ��[#�ڵ���`�ۍ!&�;a��+�d�&��P�Y����I�Q�yӲ���  "%� T���7��D��_Z��/��E�TVt�ZiR_�򽲇D�+��0B_e�DS(Ct�5���k�D�҄�&.�>��ub�y�8����  GU�����K����|�t�I��8ƞ��f}���.�Ujo@	}��e�{.=�o��1��}< ��]e��NشI��&-� ��e��*�/ô HZ8��9Q��J��� �L�j�SWgط�q�*���JF	���i�]*��SV�ÏK-�ABl�*�O��M�����&��J��D
4q0ޑV��3��k� �*)�G�/ 1�M]:3�Q��������5�:V I�j;E~Z��&��v�O�-�E�y"j��e�q��V3}�V���R�2y������k��
ZbEԬm;ɾ\���z�}��5eq���E��ö�tx@��D�O�袈�\0�W�X�ێi��y��Q+ �˝�������_�8u���+0�Ȉ����gM��Z�PI���� � ���#`t�(��r� 0�T��D�����mr@�ٲ���sjh��t����]R��I���^�y� ��
� �b��9�woW��Da �?[�$;J �	 2$E�z�Z�4U+/ң�� $\. `4>��Ԍ�1����z.5�[J�~#��o�|����h5���v��?��2
�'���gq ��@��$��&�V�:�VI�ڼYe�o��������{�@ ���,  Ք5��$6���p����Q^�@�#��]�U�T  ����.e���:�=��@�&���+'��pr�>�^�M @".m$�k��}��RŜ���Nsd�t$�Kf��2�+ �1��(�����y    IDAT��H����T��1�@�����8K�JbP<�l�k���1ѷh�i����Ik>X��Z<)4 ������M�v�JJ>Ar:#���q)����PS�kKe�mng`=O e$(V���L5��+�$� ���~�
!+DyE|�cGC]Х.�̴c�{,	�6�rE��j��  ������$�ӓ �{�,�N`d�;O��ye���e&�x>x���*�+�h�t�/k�n�!<C�m Zc��.��9�Q��������� h6.��ڕ�@�D�U� ���o�ޯ�>o��ǿwTRa%& �N��҅n$�:� ��w	��zI��K �E1� %��^��Ɨ�"�� ����Q���s �f�ToK�W��;  ;$q��!�(�iz�ٳ�J����); +l��Y
ƙ�� �~E�`9ĘӃe,Z�f��f����g(��p�� j�u�2!?_��;8�0������ӏ��?�4���OR?#�@c��g�,֍Y��$��2���o��>J ���i�׮	�x�Xo�2�,� :�6˛�b�1�~��V����i����������K�h5���\�)��T�~�� �����Y7�o���8@*���Y~+s >�}^��_u9훙��~s&v2��.� 8)�K�K&�Mx�i��<h`���3ܖH5ҷuv�D�z�-�����M����	��x�M ��ю��̋�|�ۑ6L] ��mm��N(��U��P̙�~�I��,	 H8 ``�W���T�L�3�
���{�>�7��+�Ј ��Q���ǟ��L3G�ܹ'N�}0�|&}���ꚺܟ*�XTi�J��]�m�ʕ_T:%�/����	����p'��wrR"���]f�8pa�䗪�K���$�	5�lO���?���R 0α�e3 �>��ئA�d�B�)$��h�th�
L��iRj����&2��&����� z
 ��*Q�@���i��o,��U����Ǉ� �𒴓��hZ�d�R�v�L #�x	 �t	 ��s���̴3�t�	  ��Fԯ��Z�����7�^;�� ������6�z �os^=+��SWD�V��zV~�gr��   T��b5j�Ѫ*�Ei5�;s�L�@��������%�B֩G �W0%�'�8�Ww  쪳���<�|� �t<�p�  �C\�$�s<pP�B�Z$(�R��Pd���6����t���65����ɸ�)�}`p���?�u���f/�4�Z  ;@$�)t����oݙ�l]@u-=�Xj��~' �f'�`�?rF W"�:����/��O�b�#{�S3|����K�0'��n��?rP)�n�hr�4� �. O⣴ɹL��a��`D�4Dh�;�����Z&%L��8�y� >Z��� d�6�SG>x�;h������ ��N���X�o'CCFi�j�u�ʕF�u�K����>
�/F�{E<-Z�!8��>�;N�� �'fE�]��\؟u��}�{�X�z] �/��Flܚ��G�H����:$֌��8 � ���8 �g��@���f:���-���\r� � ���,�4���^�����+Y,�_5W�ݒ� BC�v*}�����s �����9�:e���X�ſ�*ؕ=<��H���{Tٌ�7��2@�����i�K���m��E��e�x?���R�?Q
P	�qՈP M��g��W�}��*����6mr	�J� P��xrD�(�yMZ�)g ��8`� ��"+�p �n|:z�?����g_c����s�Y1��jE
� `*�~ �4՛��9�܂���R_�� ��Ԫ+Fi�C6���Z)pFd0���!qH U��Jb&��ǘ�9%�QO��UZ�hvW{����8�Vxj���!�Q��ie�FԶ�Z���K׍��2c��$������7����/� P�۶@t-��}��m��˜�I���V��I'�I��L���5�k�k�������
�N�[m�H�9�,��L�����H9�<�=�Ϻ}U�i�7��$3eYȎ�`,�e�M �{w��/�G�����,ltS��C�X���K���W��I7��\��P�x�_�$�/ >E��5�� �F�7N���������s ���	�+�hr�k�D�n̜X��H�] n���V�]br�5��y�>v� |���,��oUW}���f����d������������%s�?W~Nޗ&��D�2����{"����(l�2����-'�c��V궚{���hӳ�S�1N�[�p��6���	�����@��g�� Ny���rd-z}��=�){�b5��o�� @�P]O�x ��N��&Z���D������J�c�  8�B�-jT� aM���j�G=����Q�vJ�ϩh�5e��ֺ3 ���T���R��0�`��j�����S��m��^y����r��޽br��U��>ov<'����X��t�)�,�d�QP-QlG3%�2�6�D������q�/^��̘f4��P���)����
���󢜰:�|i��\�󷓉���T�
�Ǚ�吢B)7M�[�߯�0�[ �ܼ�G�<�J��}s�O��� &(H�P�8���~�8�����)�'�>��(���]��Y�7��S׈�!�?a�F��gx����t��
���?:np�o�9�w�5�ϙ\����|$/%	��6\�|#f_��0��S��i@�o �$�n��{�~E%p��k�`#���fv��D۟� 6 !��
	�s �t%)`��`�Z1
�>N�f�����w�}#��m�D������+�+��kJ'�Pq��Tb2��t �nǍ�$�:u�.�mm��:, �y ��ǎ��o�vED�`/{�YF#�<td<��y�1��NEj��a�LHS��4a߫�q�_��iHjw[e��N�P��_B��t$Lp�v������=�6@�L0d=}������] }�%��P�[Q4	�i;���&���R�X�: 0��3`���N��2#P��_C�$|B�a���ssrj��3 v�Yh����''��R(�X���)+�v4��t��R��{@ �M� ���G��//C�?G'�͔�
1�N�g�db�������|g� 0�k�&��-�'��u����S ����s�aPg��e+ ��m[�������	"�� ձda�� d֊�{Qu/x��C�~�ٽ+��z*�5�	ጆA=ᎄ�赇�,{�������7[��{���I��O�-�O֣�(O���g�
�����j	��17; �U�g��h�Q��K�?v�vM{�=��wAd�嬖�e�6R�jA��ݺ��/�"-�'8!�/��(���;��������s�ԔJ������i��� ���!<����4�6��RR��׀�	P���eJ @�7:�A�9��*`6+�(=�E�|ȵFY��T�?���g=lCj!k�����[J�:.��r6����[$Lݽ���)�4�a�v�(�y%2��Я3c�k�8��  ��.ˊ�����KZ����Q3�Y�Z&xY��	�D3%��C���|?��"r�-��h@v�t)u.IO�5zE��0 �DL��ٺ��c~���- �+�y�o��Hx����{5�V���I���N���8�aF싼�Վ�o��;�%��r��٨�gD5��M+ n�q�y��Y����"Fͽ'�f�\Rr�"�W~��=<ɹOT��P�k��:�����j���-�w;`�:�x�h_}ۆ8�9rhV2�[/�b8#���� �t`�g #"F{c\���R#2��B�	n�����s� �.����3Mm�ʩ�vA������ƹaV���qdfr�.�-gzV����Z�4��;���|z�W��J}@X��1�zP�ꨉ������%������ ��av��[��~0Pȩ���"��qE� ρ������k�z&�S�#ȡ��c�ir �Q0�γ�kD�O}�� P�z���G����iQ������ugo̔d��"�g��� }��O @}�(]}���� ���� d �� ��~����0�鎃R�uD�� �P��٪��8����y�no{P������`��~�*"�W:���i�QSr�ƪ�s�Pc�Y���hF��R��ʎZ[�6R�8�f|��/�r��4/)�]����QFC�$F��Rh(#�QV(z���=a�h	�Vj�9O��B� /"�I{�S�^�l�@fXc�4|&���(��� CN�s����)gKK1��G�"�b�_V�m�R"OE��Dr*}�&B�m��)-J�3�b0���N�A饪��2K�f�	�5!3�R�(n����Zz*���mtȼ�_WL4�[��e2��>}0@ �2]�r�/�
�os7�A�9jw��Q�� `�J�R����s�@O�x}�-%D~� 8�g|���w��{�'�M!�<�j�8�伤�����ǦXa�9K��vL���)����=����<}�<y>���?ն��Ͽ�����+�G'�M�U�̝G��Й����>f���%����}�0��%����/!���kD�hHL��� VǃѠɏ�+�����8���K2 �] �4��۰�͚b�i��X�������/Y���)� =8��dlZ	 �T�F��/Y�� �w��o=�Z���K= k�[������$�rC% �Ն�t�]�	��.ԯ��=�� ��ư�ш*������a�z�ٱ��'׉�æF� D��g�������~S���{�̿��8z���T����yI�SK�� nc��N�&X�:z� ��
c��(��N-}�Q��*�2 �)�q͊#!����hL3�x���8fHW^�잸5I��+2N9B��U���=Ŵ:2J��l���kѧ5U ���T�{�E� ����b/��ڷ�gs�~_M#b�:�-,e��`4� �� �օ"=��kK����r���{8���9��Q�?D]p=�^63�?#�@�V|���1��ƛ 8��X��پ( ��(`�dAV�-
��hI��zW�� ���:�M�r7������)�m�n+D)�: ����R����'�~{>�T]T<#��8��>ZB�������dk�?��O9~@��?����#� �|�$�1Ȉ�P�W�cG��\G�uDY�/"�P�{A�i�V��W��ޫ��,+A��׮I<�<�p)�V[���} ���N���) ���;��9�1��M��@���~�g��n:��Z��������P�iT�^f0  �a�b�~�LD Ykf{��٬ԏ���="Ѐ��'�/  �Jp�]f��4[B.������a�[�>t���7!�v&�?f�Púg�t����{����`�ߏ�isH@#�L����"����&l����zJ��1�����)�-U����CJIX��?�S�TA�<6|h�AUh��qE��s�S �qs�k�s5�H�Ƙ�I���8�k��0�����cz �Z�]X�,Q�bs�x/���y	8� %�A��D��FHc��z�WEҢ��V�hzP�OL����u��O���JNR�;�`���K?hEM�sw��('��� �R_>u��H�>X'd�Q��̬�N���QaIisC@˄C��_�8��� ]	X<����S��,a�e������U
p��+ig��<S�,~�q�� <��Hw� Y#�����`���*��D�۶$m۾5d��ܷm� j�"*t�Z_1 �bc�hR�O?����g5 H�h�)���.Бp�Ա�ԩ��ɸ�)~�����E�Ð���m1s�m#h>x�(�v���μ��E=���}��5T9�2˦gm����/!���j+j��Q��S|�?��Y�M���;E߷���S� 8I	����&	���]��*m�ͬ�V@D?�f�5V�iɬ�L�����=�9b4W��'uɑP�&$Bw��h������svH��5�v;��Уk��G�9G)0�9�*�COZ��d[�Sk0���� �gp	.D���N�B�C��s����Y);p���%�+���>"k����sՁ�	��v�i�d��t=�y�� ���ҡ�M ����KM�W b���G�H�$%5|��gV�������! im�ip�ʩ�� �؀��!EZ¶K�%Bj�$�'$ܢ� )1�E�P�d=�b��K������>~��UC)F�z�>T�罃� �{��4��嘇��y�лI8G�+ޖ�2,�;��s+Q}2��X?c����u�n�Ǚ���Ա�I�Gh4�� ��$	φF��=�3Y3d&ؗ�X8㭴3����30r�#��I��=�ݐa@8~ i���k;=����A��!Q|Fi�K����*����Ο����z���Ck���q��\؊�j�����?����?/�4�n*jM,t+3��憳gOgϝΞ;=�;wZY�:�#dw�V-���HK#c���ne�s  �<$����k��	FRϿ�X���2�I.K��iP�_�I���X�[e ��������͝�:)���q�%��a^�
 ��u��JF9h �`*��[z�y'�+O�4�����z�ѣ	�gw�1���8�y�D���P�f3�-�cKב�II�q�<>�5_.?᎔��?�W�.@�dӧ-�\SG�6��c�gF��j��JkE�q��$e���Y�`��f�<랪�2�6�_�X���h7z�	{��5a�H�]t��1���͛�t�b�������G�b�,;�9�\dS��-�@���z�ڰ��c d>�y}�̀XV��޻J�)�> Ͼ&����� )��Ih�@�Բ�CP�iB-��x޿�rY ��ˬ�C{ ���];=��{�S�a��7x>�m��R�a/W�C��v�TL�<�ϩ�?9���;=k����1_��t�U�� �������IR�gw�*ULV�V2�/^h�v^�k�x8�X P�x�ڌ����Çz�Ձ�Ev*�gț�>�M��C�tr� 4���k�FR��iVJ	o�.G�.����y�h�g���u3��e���_�v�a`�!���O�?����������@�/��m3��`^��p���ҥ���K�tAF,�M��Ԃצ-狨 �A�s�;o,<v+��[���`�P,�����	�8P��Q&�� T]7�Fu���)��# г5v�F�G�f��.���{��ӧ�i�b��iYG�}]k�Z�#�Y��O�~�L��Т�N2� @��'��g>��W nU˖5��F�8$DrB�Sx٪�UN_
]ݹu[isO��loDM�B�k �^jd��C�C�n���\4��8۪�f��i���"> bI�.Z\�h�9�̈́5.V��  N��Q�������!%ʤ�4�N;EL]��ˁ(	�h)�2N�]D"�{"��r���p�����q2�m���o�כ���������y�{�n�zMBS"<|D���(^�t����(�p�����|�u ��	w> :�����x ?��i�j]����Ng5��2*����Z|�~���g˭u�ߋKA���l��Oj=�SN�㞻T勨X�?*/�;x���{t[�	�8e	'�E���S��@_� 2Wd(�M��̔�S�3 �,V�*\G���`�Y ���u1t��n�򕤀w�ds)wa�TRy�
u��D�u����ԥ i�D���v�vY��?8�O&� cT @	 o��&��Ųǔ.^:?\��@ ���\�Ny`@�m�A�Ӂ�/l��kw�%bu�1 @�;�)J�5���
%����F�V��$ H��Q���7�9���?OA�F���ek���X?�p�F���IզUD������{�����0�\�	� Q'�KC?�W+�+{    IDAT4)O,ר��Q����x���Zk�U���d#�31|��a�ڗ�4������e�wԵ_-+j�����-Pӽ���G�N,J��p�
��Mdd鬌m�-�|� ��H��0���<�՜��K-����H�$:��1�VM���,dcxV9Ɨ=�A]��@�c 6�DuW��s���-b���T;��S�Tj��B�٦�Ce�,D?��s���iu�-m���G�%2 ���H�_�=�����<l�}��H0[�Hٟ��ش�$??����24��ޏ8�y6�\"0�{���Rک(��>% --�`��>{�l�w���+��,;S�}P��Ig��w�S�xm�X'��l��3��l@��?v�P�3= �?�b �"hP�eia����hU��5 ���TI���=���( pox��U�y�NY�*U��%�ݸ�Gkkn�]]3'@C����lK�jq��[�9�����&~�V?�K������`��uDޱ��l郹:��p������3Åg5��#��$xu�1�M�ˤ�=�'T	5�y<H�i��˞��K�kkO��~vj����#79�: �S���:�?BDS�Po��wl�
 GƆ��)g8�
 h^�~U�U+�����c�%��&�YS���Z��a|Ieqಿ�C��v:6L�7�M2��{� ���j�Z�)ҩ���}}n�`f�[��]y��!��RO���ٚ�����-�ݾ�����1,�i�1�Q�={�P���qV�t��aw���x5 �gH�:r���
������1�{F�U� )3 )^�%������ܖ͐��f��{����l��FŪ/��Ԫ�����j�R��X�[�,��K&Q���[���!^ ��{d��	mL���lʓ�֎(Oјѿ��T=|��*άg�F{��Fni��R����� R�N);Ŀ5'�u� �%z���;j��&�`�X�����J��G��""��rf�a�YJ�zj <��^�}�������Quf�4���S�`v�O���`��%�S�dL�]�{m�E�~�R��<�~ݗ��|V�*�ǎ�ٛ����8Y�������\W��TW��n�'=���#J�L��㻕���ïWL6%���<�&�4'�&@� Pv�ܩ�������C�0e���3�I�S�N.�m��Uمr��'#3�U]���g��7�8�A��y&��&��|�z�پ�����e=��KڸF?����O=����P[ �H��Is��N�s9���V�����[�Ó���uv�YȠi�и6Hی�ʬN��?�{q��7�1���S<Ũ��q�(� S�V�ڭHw<z����[����� ���ae��^�K�n 7�Q�N���.��T�S��>�A� c`#��Dw N����\���c=����*� I�,G�F���\"-��m��� *5 �<��H {B�)`��E�h�LA J��y��C� �U"����l��3���NO6�	�Aw��DHc�yM4d���&4�?�	 (�#Ka���V�s�m�w�Ա��=�X�";dI��>�'�l�|���'�^健X�8����}�dO�-+�m��)��/����[n��١t�-�����m� �6V2��l�;ٺ�3�l���.�q�MN41���IA�Y��,d� ��9����"q�I���>�<�R�)��N��yv���⋚��te�\� TtN�Dh28G˚6�&> ��q�*��^)�)�-��-cii�N�>1�>sb8�z��p������lQ�� 8������q����~SDg�V$�_H�,�![�S�nM��u0A��Ǎ2a_����������_�K  �Llۢ3ό�\O�<�ЧP��P"T�hW0sʼ_ML޲�;��Y�����(�x�2a�{�	ƣ���;3���t�u�T�K�F�u���332<��/I=R�{��ߗS�  �PCk����u�^�+wt#�wuN>ݵD��I�� �pPt��u�I�����E�)B,OE|M�:%�kX���\x�R!���5���L���Y�8I�(�H �d�������m���Ա=�D`j?�٥
������JI���Hp��/&��ݡ��1?���r�w��I�'�����Vj�f ��`�6n9�OWcK� � x�M��ԕzD$ş)��L�`*K��]�uN������ ��S�k-�Ϩ�3�d;�6�h����=s[�4�}q��u�����E+WP�{�-��u$Z�JK���Q�]@���{ݽ�g��ұ��R�u����s%(q;���p�����3B �����tV)��#����p�(z��S�.���|_t�����Y	�Z�Q2�c^��|��ɓd��'O�J95����M��� ��"W>�9�.'�yj����O��J��ZH�Mro>Wk��?��{v���� �o;�?��� 㼌o�y嫋��%��N����m�PM4q{	L`�����D�T���r����z֖ͪ]��T�9d#3�>W���j=x�<0v^���hT"I�`cj�� �B�gI�i$� �t����G�Q�G|ڢ�=�D�Y(���o����h�[t���s�v����#�/�u�-j��{��w����l.d$~~f r�D���0-�|�4��ruzi�3�dA}��V��1E4u6:�%S�8�Le�3��gO��?ٱC�"2�ʊ"a�Y��W�Hd�'K����B56��g�8��l�a�2%;:�;�����=��Y<�D�G� �� �%_ !��u��^�s���!6HJ r�s�+��ר<�o�-p�jw�����S��/M�<?�?w^{����}2)��"� �T���ePWa:	��i<ݰ����.D:��0?�?Β��\ؼd�g �| t�� (~�K�g1k�{��X���rx���� ��;�l{n{�����$�A�~�͏_�u���p���y�;�M�7iҡAYZ�~� �k��a_s_8�Z��%�I P`�5����_� ���ï�e���ǝS$=���*"q����r���Y�U���J"}����+d����=� �#�x`���جqg:Kr�q�R�ҿ�]��@�f3o��	�D�Q}˯^�|�%2�H(��<6�	�8�	o�����������?L�Ѭ��w �% ~k�۽߼I�Vݧ@	�D��]# ���#���oa�xz2��$�򅤇i�JG��L��,������ �R��JW��p Y@H������2J�w���i��d��؅�Q�B��� M� �w�Y艔0+�g�]�>��&�%��=����A|��O-L�G��I&�#�������7�.S�ʙ� ;�{�
��n("�X?�(�7���s[��R1�C{�t~�}�s P�����P0�`6����$���2�sr�Ŏ�:���q�<�lU�F)nkt+�L��MHo.�_F�Y2��X!�IJ=kk|�(�}P���=�&���fb]�5Ȍ7�L@��rrk�Lr�LX[�h� ���ç�Ç�x'=��܀i���@��X�}8z�  j��"	���[[5�]��hU?�L4_%�+�*[����ｴ�_:�hfg@Z���S�c+���/ �C������Ksm�fTۜ�ۿ�,1+��yѨ�;���!٩�n ����meZ=+��8+U����� oɑQ?c^�S��3f�+��\&ǘ����8�x��821�e�|X(P��HSrda$�(O��8Y[�#��o�g?�(�V2 �`2C`S�6	�K(>2�Ȇf40?/��".�,N���F�����,)_9�=U�+uu�H��ǌ�C���`��ë��r%+����nS���s r`š���nR��d�*9걶}^�#V�i�k�Aѫ����W��I�JO�����Lϑ�2��[:���ߒ U}?u=�9z�������=�2���J����ʽ��9 6��K���M���~��8/���c�K�nc�E�}���=2
���oެ�!���|@�Sm<�+���F�(�-�c!��ߛ���_�`�i��� r��R����(Ms��a���_�o/��9Oj�s�����,��S���=��}��:#d �����H/3yh[���=�k����v���ځ�:�V��?�`�����=�����O[�D�4��AZ�eh�Nyj�� ����Feݿ�ڢg�[��Ĩ7���������9 j�I9Qt�����p�9�
r�V���l�N�<��6���2k~�洓	Ⱥt�V��+�rL�9T6H��Vr�[[  `ǿ��X��Y�a�;8}�H�R 0���N�8�M̨��2�ų�2��IQ��w�YJ+ [-q{v��H��ʈ�6u�M�ʖ�w�����N�8H9K�a�26��I�q���W����) `X���U�#:�a��(�Mb�����I`��M
))���N�%ժw8��j/��e�Y��$@�� ��qɴh�=�)f�R~5}:����A� ��N��g4UIC��V;�<{�!�	>�&��h�۝��Hn?�*�񚖿z&x�����~� �[,΄z�W'��A�u�iM��ߧ6��"�z�=J�������2��F��Ժ	�r�� k�e��E�C����z���Pr�h�<�g� �A����c� ԢG��-��VfP�8��Gm�<"~�P7}�������3��H�I�m vd���C���C^���Lth:3D���C��ʪx.����U����9?�_V���,Kt��6��� ��1����9 |�J�0���K�����E��Ȓ��L�¸������_�s]  k�#�k-wMQs��6��S��۷om�0�,!Q`��/�����h<
7�ZC����t��J%�)mG�\)\���_���FjL�8�-Y?N�m�s*�ܵd��S6�X�B� k����9#�3��'�^ב�2^�����)Y��~�[�L��=�!R3���K�֣tݹA:�w �>�. ����{wU_�`�݄�K'ٌ=Љ{�/`�T��@@jQ��\׫�>E��ָ�&&� ])�>D?�Rrob��K��OM�Z�����u���Z�p;�o�qތ�Qd�u{!#����Еd�۴6%���T{�ҽ�V30�ց8E��P��^P�[�U�=I}���W��C�R�T�I") �{׆t���!�"D�z�	0<0�&M2���C] 8��Ͷd6���>�v;�<��`���C��r�E�R�:��^+�Zj{��l�E���1�8�b߶�ө�J�I�)��Lܻ�`x�t)JYH3��%^
B4_�2�7f>�4�L
��]t&�z���N���� � ���m{��x/-������r�LX&v�lXo��f ��m��}�h�VF�eu��h�f�@�I+ܯhc���-�����sҫ�Ȉ��P�Z��2�X��}����-�?{ N �~�� ���뒣�%�K+`$�L�����$���աL Ѐ@/lLU��.C��x�Br �0Ԕm#�Ef�F���٤!��1�:�L�2� :��wK�d��e���)�X�HSNw)bh��.���YX��j�ѭ�6C�I�	���,9��bN��\ `kԫ3�	�� �^<�`T���#�f[�?�R�!W�^r���#�2.����l@�"�A����ߗʐ����.��N6?�{�y��
d�\j�g�Ž��z���Ϋ�1�b��3� c��:�$8:��6�]=I2ܮ���(%Yhj~_Ht3�a�oWt|�g�%�ds�?��m�"1m���V�g�}��J ��? ��n�]�@�=b�,uo@��s,�k �~D/`������HY���r`�>"�n�[�
 �����  �]V{���ό�n] W��>��gGQJ٥��=+:�L�b'g7k����Q��^nc�:���f �!L@��Su�Mo�l�Q"�l/A���8�i����P�]^�,�"$����4��`*k G�����>�	cF�&�XYn����)THN�8Fy�Ҕո�z#��{�"C�*���_Ѧ���%�.����F�b����FY��+��g��V�D��6���:j63�|
q*��B��z� I��-Ki��+Tdd�D� ���Է�%��`��m��NG�D��X����+��|~͈"Eͨ�"��Z�����S��V����X#��jY[��ZdNS�6U�x.�31�~4&������O���=�Tm�P9wb�!��AW���VM�*;�^N������񝄖$��D�U��ϒU�̿��4z�{����?+�L�G�7�-٧�++��$ퟫkm�A>Kʈ�^x�5���Hb�%�Q�!;`�b�(�z�9�U�K�/�5��"[�'&�����GO�@�f��Ȭ
��aa4~?�pI �}��w{��F�%e��a��m��� �rv֑� �t"c������+�,�N[�����7ą��R�j��lQ���a����,L6�n���y��_ ����K����P��e<�ђaYnװ{�� ΄��m]88[Kkvy��[
vz��C�Z[�x�џ�]Su��oJT*?dmy�)�:��5�n� uF��t�3�����S�@`��WH?\���%���X���7�,vA�Z��Ȑ�n�ou�ghF���O�����݉["�訷fy� �#v��)в�I�C9�[� _��1�7G�1�٧v{�Ф��A!�7t�C�^�~g2�eM�4��p� �@ 5Z�R_�ǿ^8��o�yZ���\�X9�r�_��������Qk6�����+j�5Վ��<6R��7Sx����l���)���<K����Yj���2��-��H=����@#'Dr�- Ľ�[UN�����ѡ�C]�}e�����J@�@I�S�k nʖ�j���.bDJ^Jt@i�N �;*��R�]x�לe��w������y&��郦��ƣLq�"�v9}j����#�8�lmt2��ʖ<��TO��}부P�v^��"�U�=Z;b�[y}0���/�O�� �v�>�] �!��'o�Nhɡ [g;�5A�
 t��c4���ڱ!1�dR�&k��hM�G��:,cG��$'�*�@0�a���ѵ�A2�  �Ӆ�^طp=�MӷABj]b�?�2���	��@i-KG֌�S��S�������G�]�u1�߿׳ahJ��n7�(F�|E"��w����W�N��;�!w��G��6\D-X���tj'��~*1�V���ļ����%���u+S� �s"����1U�	%�.�0IdX��)ލ����oۛe��6�������$i�y}��ܿ"�Z��Bf����b��fm 8�K9��&l�6@{��6&���=i��e�h���AS@@��\3Z�J�i~^�uv{���ߡ`��G���m�*f��,�Ē"�	�%2]n;4(Bv�����2�$��1Uȥ�.8��6 p Ο5�~t �Wį�f]O���0��W�p��
�k�=9�`�; �x����+�'֝� ��;�ٯ� ��7`P����Mrq���~���� a���A���ɤMU��̯7ck���眕�i膶*�u 〹��6m�pɵ�~T��u���"\�w�Tp���{bwJq��������U�RGN P�F�v���E_��:�~?ǂ)M�D	N}�j��O��t��d�I9r�K��Ȭc��[��|�[&.6��|��y�ih���z"%'F�V���[�����^�6�����̌�>��no�v~]�죩?��olp7�*�M��?&��}���^2J m��	v�g�I�tZ�["kGP��=�L��7�Ο{�utZZ;g�s=��s�xd?���/�N�B��g���hţh%�f{��#οo_.4MC��sdQ���K��ns)���ϼq��F������D;�'[��R�t��������;8Z��B�^�5.�9e��j��W���n�{��9â	A�����ߪ/��M#�G-�N�Lڌ]�_F9H����gT�)�����c$e���    IDATH��p
 Hc鈈�Ч�m\?m�Ug�
��f�����	�3 �T�Kw.Q(��$<G�j�� Dr��zD��A���P��RbZ���|fcGk���"�f˯��%��m/O���Ҹ�r���`��Ο�Q��R�ќ�ꭀm�1���>2��]���cM�����Q����h� ��j�m�s��g������=�t2�E�/D'�1[{��7�Y4�P��(K�Aw�&���ry���B;a|f"����B�{���_^�]I$�3��	k-�d��E�s�*�>�Z�T�=����.��vˑ2�f�.�m.9�PR��Ɵ]Y٪-���5M�֨_TNo{�?� ͸��j.����aJ	��~Vr��Q ���R+��q�/�����/ ��{�'���!iO�G�ͺɕ6���h�FD>eS�ˈ�m��u]�s�ƺm�_`������;�ț���t���5L���  ��ԠM|�:�S�����G6�XkiK�(����R|��o��	�z��*9�J�|�����=���G{=�Wf�{�LD���:�R�h%mzô]9��[�}����O�!}&�4��s��?�{� Į�h�X�=k�ݡY'��+C��_����㤭s��R�8�_6ge�u׳ȇ�b��Z����,�����_ŬV�l�a� _���O���t�|�)�ԁ§���u�U_	 �,:HG�#�yݶN�Ix�|�R��L�����s�~��oݾ��\j�p,�n"��;X���ei2�������kp���/q�a�п��`�i��y�/~�� @$o��ʇ�ڽ]� ������ �8���anMI��R��D&�F��;��46i�$�J7M��l �P�GE���'3 ��y	�Y2��{g�[c�������\H�� $��jz ��&���>v��3d��T	�[]�Is8�n3�����_�8��?yƊ��\hW�X h��ܒ��9����� �//%�Q�ؿ�����k0����x��lt;�'�➶o�f��ד �4 �o�'�I;��ٵ�1��f$��wE�#l�����5�r��c�@�!��K��Tc���w T���J��ꖖ����{��
���e�{���%����=o?�>�p���|um�l��<�v#I +�U�/��$�Xߩ���3g7���|����ht;��0J�3�Q@c�h�')Z�G6Ȏw��w��q$��s9�<���Ӷv�ő��% ��`ĕ�:& �Q�v� �,�枻�;DA�9�0)�r_��q(��%���{ӕ��i����ܹܣԐ������4�S-/�p�m5�f��= ^�h4�����%��T�ZK�AgI�Bg6ӡ�0�5l�?/�X;e[�J `t�1��f��<����~t:�u���Jѯ�l�X��#D�]�:�LÉ�H�C&���/�1/�?}��[dD��~�m.�N� ����e,ߤY��e�Ȫ��u��	�׾g=y�qG�)v���c�R8�Dla��$���S��=s:E'�A�;ő��u]��L 2",%rn���ٛF����G~R���6���
63�v:[����U`5�L? څ�J"#���{�y1ޞ8��2?�9��K���l�A#�p�h���x�o��� �<�¶���x�ʷ�y+�n)���1� �>b�F)��4h��� �t�w.C�_�i&�5��.���q������O�4�����;�$���dξX�rc�h��lu_��Ɯ�������i�����$j���*j�8��#���!w�;沉���a'-~�'��,��� /��bȣỴM�c!K�$��#�AC�}���ɃkV�kt��	��������44��@�˥�����h#���/��f�yX�Y�����I����ح���[�7���2D�P�80����v� �ٙ��p�d>uٗ �N���z?�����;�� ہR���6A��8�(��
�2��}+C`w�x-���tFLRx�y��"�o���fs,5#�M�ײi��h��8-ڎ~ҹq��W_}���K�kd)�����9���W~�s~��߾������k�����ތ��ֺ�#�
ݬY�0]�ޑ�&RS�Ҫ��Y �;���5n8��<��g���=�Ah8�a�W]�P����I��"����i� G�#��o�nn�S�
���h[/n�����E�Y[�CJ�T��ͤXjL��/���/�w]�H#�s:S/ȩ����D_�P;�>tF��I�h~����7���;S�譇پ!z�"b� j:�1�G�� ��bб�^�Xݺ��{�d�^�(��-���9r�{^Oc��s���"t���=' DjI��h� O�52IUQ���W+g��
���dE�����{���x�e L��D�sd�,p kbs�17{N:~;���G��ε�3��^,���΀B |���_�}��Wo_}��/( ��b�����]���qޅ������~7^���xr���koC�;�0��"�6q=�
�aE'��'H" 7]���$�"� Y��5�q���% ����e�f�ȶ�)�>����8�7^�
L��E�=��Go�H�^%�_I�k,��@��R���{����$��;��������W$ ��ҽn?�G�|X;Ȋu%#Y���j��O��iЌ+k�{���@�S��`���A)��KL2�B6��k�4��Ȟ�	�P� ����2E�in�a���x�9*�r��_Џ�ED�YH͢����=.D,���%�]���=��p�X�E�������-H�����I�!tW�-���n����Y0�9�����(:vXa��+W�h1����_����z�����8�ן��<�y�t9N<Gx�ϱ`�������I곬�l � �ࠌ����1\נ����L�ֳ�ӂ�/�	p�}]VΖCz���펳r[���"Y�o�-ۏ"��j����q����"�� �����Dw~��uUN"	O55��Y�.^��U���հZ��/Ÿ�?�)gP���us� (-���À���&3d �Ҧ�ufDV��s�M��L�	�X��p�h���Ł�`YP� � "{��z��[#�= !�alg���_l�[��g���HY��Vt2#�Nj��\Xd���R�Y����W�N���l����tt��=I��<w�3B��mN��{�,�c  V�qGϵ�L������I�r6��Z��3���3$>���o������˷�?�?�H�cZ��~?���믧����o޾�f��q���^�<�>^|��Dgb�\�% �:n�虗� i�W������n]I����L�Qz|�M� �vW ��u[���
�K�-���2}��	5��d|�!-�ҹSݓ�h�	C��ںi�L�-�T�G��qM��uTQdz���⬎�nP��{g�ل�%�����3}��H�s�w���g�h��e�tc0�&�c/�lU�@�0�,#�(=��0^�`Ebq��0�Yǈ�<��ò/�I҄Q��b����$���7�f{0��������Q�l�53瞓R��C�ZS(u�ҮK���[dk��e_��i�fOD����$ V�����	IQ�j���A�!�Y)��f��/?����O?}��O�>��Sj4L��7�8G�>��o�K����� ��l|�C`�~����2 }=�v�*�Jw�y��<�Wn��� \��V���7g9�*��GG!X8f\G��f?�6�ts��k���Fd������i|x��T����t��,[�^F˴��tU�+���l�"�캮�z|�^G�=�~��:�@ySo���|N͈x��'{!��(�Ͻ�y�<%Xd�h^N?���l:�U�ս�[�̵�Y��Bΐ��@
��	�������.<���̸,(��,�}y�Wt�g�n�~���l@j�ӽ *�
�6ί��5�1�ۣ����>zC�?֧��q]�Q�r�Ht#<N �wW�������^w��v8�o�D���=>2�Ե7�{초]O��7��4#�45�t�nM�μD����8��_�ź�s g�L7q�5���%G�5����f�q��x��������������[��	����a�{���D�KR�>{�&p��ֳ  |b����f[i<p�1�L�Ӟ��lEB��1m�����c:8��I�Զ���|��/� WcFr�!$k/F�E�ٱP���|�*��|�\ 7T�9�^���YN䒨X�:@8����x�猬:z�lM�dK��0�N��h^)G�1ϒpߘǳ��� ���9�:'8�k��$\Id��K�5>�W��'�+ue�9��/�:s�y<�o��ϙ�[@?F����$-{�MǑÈ�F�g�r�Zۖ�8��{���s��� \g��n����-�^�� ��v�Fd!ݖ�$�e���nژ�3�?���O>��>?��3(G��?bۈ�w�`���f?��O����|!�|�S��b�:���O��� �VH�n ���;Y�;>�]�f2=�F�f��S�(^��Rh�*��T�S�6�s��n����~P	|S�%-_�&"�2��&�����!e���y�D�b$���֞	A�I@]���C�_�`&Ә�0��LÞ�0v�a�&3҈̒|Vy֌E}~�;��ݜ�B��d��O��"�%�(P!�F�0Aэ�֝ZI�Ӛ��L`��&�sW��.�PwLؖIK��3�(9�
-����,5��~��g��Ʌ�Ӗ�<Ĳ8� �$� |���5� J/D��dF�� پp��#i�$=��PI6B�I�?��O�u��վ?�Y+����={�8�g���^M��M����o������	�YHPx���A9�O-���j0S�7�rk�v�^�x���b�(�/��F#'
�@w�9���i1�1�2 "�0�n R�}�����]�x��<Y��ψ��������) ���I��2������<% ���h��{�����>%���9d6��������c@z|�E�K1�M�O��A�t�3?\r��%溗��p]`�P��f]�0�֜��(y!�t��p�Kٚ^��%�%����s�1�h$�oe=�������u��Q�f׹>F)�42~F�s0���,1O·#Z�`~1�q�i��aA���͇��a?�0Xߑ����'�P�8��x9/��������8�o��m�8�>��dnΡ��-�x��-������u6�>�k�����+ᗵ{vjsD+�4����@�X��Н�Ӯ�Q�+D*3���� �A(S2�Zv�igw5�)0>���P�Î��p���g�	@D-]�AU�����y��s��{�2���zt�7��l��*�G>�G���5�Ys�7�9�Q����qp��Y� u6N�`�暆�S�L̱X�`��3��|>�e6�A�b�4}�O���X�doy�o?��.��1v�2��}(Џ$ˣ(�Qƅe�$D��W��V���[#�|ho'�� g3�!3b��Re8|C��I��CT&@F�'� ��C��m|���8N���<�xW��C����_��|�������y=X��t�K^�]hkm]��+�H_e����_�(�`���w�N��
R��ĩPt�پY������ع4r��]�\p0�|�;�,�|��Xdy�N������� v���M�w/Q*��m�-����]#̌F'|�qόϺ�pm/쮯��a�͈v\0N���L�@4� <U;Ϩ�{��j�q�w�m#���S�i�w�����������4{�|;�0�g�{��m=����q菍/���8T���*
��)��Vߏ/���t�_�l��5�����g�S����^����d���r% �jvX@����"D¬�fh��2?kV,��ؒic��dg<���
�6�\�!H�3���6��.Ւ�jS�C�J#,�zXk�п6���6���Ü�"�j�k[`g����Z/��`��7EG#䝫f�8�	+�M|�qW�͎u�0Ԡ灕�ԝ?E�1��I �}�<� ��;�#�!�{A��N�" G�I�u��' �;摲�ð�&��Q�[{�~���e�Ռҋl|�D
&"��p�\D}�\P�d��i�l�с��XM[�
��7��V�k��1�S��T��P����Y�,ː���>�0��f��g �S�d!�� �=����zl���k�nV�����IY�4�#s�t@���l��<Z�	B/�;ةg�O�ʰ3�9ѳD���:Y*%�j�]���V:�$ �y۹V[O��y�
��jW�V�IO�0'5H�i�����J��?���l���ꗂGg4�<+�Z��[S��U�L����-�
w��"vfl���qF�m��Ֆ��cD
9�l\kb�s�	����?�zs���H
F
�By�ѝ�>' �4�HR|�S��MPԱ}��,vm��mA�wpT\&��f��"i�4!au<>�TV*yxi��g�e����;z�����r���g�J<`�`D����|1��ExQ��38=��(��I5O�ʑ�PF�o(m:^�^j���wv-���8�g9�a�=�C�Y�ic<Ij$�����R���R]��j���	����Ŕ;�O�nU���͕5��m<���J ��d������]��5�FN���gD�Skt�x��'LX�ƅc��=k��"3 x�E:?d/����@ ,�����ի}"���?s���Wװ3�`�p.DԿ�>���h�YN`G�T��΋��V��pȥ^s���7�/ڜ까"]�W��1�+!���h��0ՠ����9����5��
N��}�'-ҟ��R7���[�Y��<�R3�@Ѧ����B,3���m����§t�H��i��yc�C���ɹ�]��N�7;��a��6J=0-��*K=!ϰ�<QB�L�	"Y>�d�� KTwBU�!Ϟ�9�kT5� K�V�
zj�[�}1����?1��x��XLe	��ধ�MxA��͚�i6~��S�����`���߁��RQݿ8`~�`NҜanB�Y=��b��}�S�DǻzVqV���,�cM��m:s�
8r����t������-}���c^�l�1�z85�]�k`8;��ه�@XTR�ձ�`�9rRxr$��9�>0h� �ĸ+KDYXj(M�ڻ^%!٘�uh=�~�Ee�Tű�L���f�1?�'�O�܋���%�A@�b��#�m ��>fX}YR	���� ��o����%#�.�#�v� 5��ƹ���)"Ib\�a�I����졘/B_ވ�[�@dZ����%����6=�lͺ0�J���"υ@� }=hzM�t�vhWL�]�Y��g�q�s� \y�
�OQ�P� �w:���W:_t�ڛ���[�4�#]��xnL�ˇ������� LI����)�p�F@�^��fD�R\nD(:�$���C�uI��������;V��_��U��+�i��OP�aY:ьHt)�)�����cL�r�����A�Hc�M��}��ܝ<�ҩ��J�]�ᒨ��3*�����V�zZM%��5�Q���0�u�N�t)�R_w�@�A� 4(��r3���V?�k�_m�����O:Do�:�xWv��l}�����G�[�eOm%�<��APv��Jb�px(e)�a`z@= ~����:�4_�;Eѣ40p���-��I���L�Y��Q �bH�r��5�� ��9sI�3��I��G�C/i��?��=R�w�7��8	�O�s� |���gGɫ�yӌ����2�t�G^��p��.�ӈO̺�#���-�BM�?�������|�h�qߓ0�ўe�j�a-ӤDҡgD�y�g��f��(�Z̏����$����Fa�ۥ>TBj�tO ��� �:���k��:ш��׸w�cp�b�""���C4�HO}5�pF��[d������ ��� [q6�G������c.%���@<��YL^?�L���^S�+F�g��  �IDAT=D�#6��߲��O }�����ݜ��4boJ�A3n�/�	��x�M�i�E٥Ad�K+�^�el|}7�Ms����_�*71��h�>�Vi�%�e�z�0E�p�\��E��-%��ã�ef��ȣ��#Z�j��hkC�r���>0�"�_���#��xF/�p��gwCqM @���jcY�sׄ�۵�3�9s�W�a���(e2?s��C�a;V.��H��2�Q!�B����:d��9�-�2p~����D)�w��B�<`��
z�&�-���r�$�i�f�g�@�,ߩ�0�?���\��(=���	�^%+ȉ�>�{��z�kBc����r�l��3pQI_���ʍ�Ya\�z����\.*��knU�6���T�5��:�tB�hK�TJ�婓�2��q�9��)��z�{���D�A7�l�qŬ��a���gQ	��$w������ﯟQ.,�'7K��A'�W�H8L�#E��������N2ܵEY'um�i�7���Q3�\V��}�S.dŇD��7G����`��g (2��q)R�?�-�wqZmɜ�7��m��}�ڪ���ӣ�D���Kzy��Z�\�����AjS�&#loΒ!����a�9y.���$����>�A.!4+gA��/o
X�����G%��0(9w�舐Vr9�q6k��MV)�{[���&xѬN}W��!۰[h]$�P��!P�j���ă�4$!�T<�D��Q:���5^����w�{<;�M;M�O��6P#�qz�cn ;�+��P����G��U�z��7L�g�aY�8�ލ�#��M���%Zw��{�! 'i�u<��@���?ߌ��j�{n9�@�U��W��7��s$Y3I��jޔ�(�y�u�$#��w��s/| �ѳ��g�%)d^�)��`��z$�,���S�	�M��뉑F>���.�f��'�}f�6�s���1u��l�s�]X1�J�t�(3���$����Ƌ�́��e٤��A��L�[�anOiI�A���~3I�,\�����X��l(.1i��;���^��S�J,�0՛�u߮sw�����<R�J,�G���x�w�d��k���w��c����jyE��a��J la��% �$�����̐Wc��;����jDK@Q'ɨ}-�c��鑑?����8�9h�I\������]�\���y*�	ۣ�֛N��sFͽ��n���+�&�	t�vҹ�7>?�m�cM�@8oo�q�O�L1ײ���2��5n#�ǂ��h����X/�ׯ�q��神�=+�*�yF����h�eM�cׁ���(�����bM�u� b��[���~����{���R����M� ��l{�^Ӫ�#���ٮI)�R�@��X7v7�m,7� >VW�t05Z2 �<Dm���:��r&����Ņ���l�*3�1}ȷv��[2p}6�ɺ
Ұ�K_��Z6L0X0���B���豓"�V�Q�����Q��ߩ奱�DMNv��ct��F���C��}����:��za��zOBV����Yu���1�Q�	h�����2BS�a�w�v�'&��^���j��kJ�' .�����t��"Ug�б�&jTfS�k*�Q�15��d[���56Nt琓�T@��Y5��~���ab�m4V���忦Dˎ�{�1��ձ5�5�� � <�H{`�D8jO�q��3m^P{6g.<�/�-��P�NEg�BZ#7��x��h/�;���5{=������X�Ie��Y��E]���4I���l�������\���{�2��ua4����PE����W�Q;���!&��\�#ǜ����Bd��� �{���@Q��!�Jv�i5��h���~/r��d��E�E���M5[[Uepao �O��)d����ۮ��|�A�k�^���3����e`��aG���Y��"(:�(d�K:æ�c& (�FI#�G ��fj��*Xl.ij�R�Q���N��dpW�6��������R����?^I@8eJr��`�M7W�;���8	؎3�}u��RS��-Nw��0H��[K�υ�������> ��=�KJHT���]?$�	v�">vL�`���V�w��1�O�v_e[@�j���,��{�	�&�_�܉(;��'~}q\���Wv�����zǚ����ƟfK�Ŵ;5�	�K�ޏp� 
�!�K�b��,2�t��kņ�:��E���O-�����랕�B�mia%|O���>j__׷�mGp-�P�b����H����	�I@�3����Ջ��ts�����>��^{���z��3��\Y�'û{�;�|"�ݣ��	{n��cGlJ��j7�����?��k'ahrz����f[V�\���=�#������'�o?�%z6ϫ߿2�W�5���*��z �(��{�w�킾#�G��yi��;�{E��?$�;�;�����u���.2wM�3t�>ow��~����\s���٤���s�w�{o�� ���c_��KN��|�Wܝ�3;���}w�B���ރ�s����wF��˒���7}���*����uW�|eY�}��{����6�#���wVd�a�J�/)�+$^yf��{���g��9���M��_z�a����{�8^}N���݉�?�n�=j�Q�o̯�������?�;#xU�̍�	�n����?�!���:���:��c��I�s��9ɿ�q�{>��:����j�TY��o2�k}���=�߹=��V�������;>������U^w�·���y" we�7�n����FB@����Bה��B@� H��B@����Bה��B@� H��B@����Bה��B@� H��B@����Bה��B@� H��B@����Bה��B@� H��B@����Bה��B@� H��B@����Bה��B@� H��B@����Bה��B@� H��B@����Bה��B@� H��B@����Bה��B@� H��B@����Bה��B@� H��B@����Bה��B@� H��B@����Bה��B@� H��B@����Bה��B@� H��B@����Bה��B@� H��B@����Bה��B@� H��B@����Bה��B@� H��B@����Bה��B@� H��B@����Bה��B@� H��B@����Bה��B@� H��B@����Bה��B@� H��B@����Bה��B@� H��B@����Bה��B@� H��B@����Bה��B@� H��B@����Bה��B@� H��B@����Bה��B@� H��B@����Bה��B@� H��B@����Bה��B@� H��B@����Bה��B@� H��B@����Bה��B@� H��B@����Bה��B@� H��B@����Bה��B@� H��B@����Bה��B@� H��B@����Bה��B@� H��B@����Bה��B@� H��B@����Bה��B@� H��B@����Bה��B@� H��B@����Bה��B@� H��B@����Bה��B@� H��B@����Bה��B@� H��B@����Bה��B@� H��B@����Bה��B@� H��B@����Bה��B@� H��B@����Bה��B@� H��B@����Bה��B@� H��B@����Bה��B@� H��B@����Bה��B@� H��B@����Bה��B@� H��B@����Bה��B@� H��B@����Bה��B@� H��B@����Bה��B@� H��B@����Bה��B@� H��B@����Bה��B@� H��B@����Bה��B@� H��B@����Bה��B@� H��B@����Bה��B@� H��B@���f��,.,m�    IEND�B`�
```

## assets/logo.jpg

```jpg
���� JFIF  ` `  �� :Exif  MM *    Q       Q        Q            �� C 		



	�� C��  h m" ��           	
�� �   } !1AQa"q2���#B��R��$3br�	
%&'()*456789:CDEFGHIJSTUVWXYZcdefghijstuvwxyz���������������������������������������������������������������������������        	
�� �  w !1AQaq"2�B����	#3R�br�
$4�%�&'()*56789:CDEFGHIJSTUVWXYZcdefghijstuvwxyz��������������������������������������������������������������������������   ? �K��+�(�� (�� (�� (�� (�� (�� (�� (�� (�� �~�'�7�?�ZW����~$�&�8��Ӭ 3Op�v X�*�I _������_xz�T���#M�]��k!�4A�]A��n�%u��}��� �@�$6�� �����g�69>1x��;�VY�Oڿ��FQ�*f#�H6�45�^.+0�7--���*��~A��g���Yt� ��-ns��q�񏪬H������ �M~6|���>"��-i�۝�?�_`�)��Ɂ��0bp���� ����f_�W�-����~Ӑ�׺���Nv���9�3 '�槎���4�����~�<�k�\�o�}cK��o,o`h.-%C��D`XA+>�W� j�k�W��K�g�-�}?�;���&�dc�������Jy�]�f�����PW�J�:�~���N<��(��Ԁ��( ��( ����� ��_�����w�/���C�5�=Y7���*n<��I(����U~�����ڇ�ϋ�nmd[]/M��;/�,��.nUOMȰZ�&���U9)JF�c�4��Vp�Y�UQ�Oj����?��|;��u���W�|I�G|N��k
��i��8m�1��M��|�t�D �o����� �U����� ��T�?�_\�1��	}�ޕ���6+/�d�)o-��G'�� ���g���#�go�?�>��/�ƫ�<q� -.'l�3�~gc��� ��ay����7)i������/�ٛμ־~�>�%��
E>�!'�j�J$�	̐t</ݮ����7�|@���%���	�V������bcr��;� `,��q�~�W�'���o�oL��ž?�_�mm�d�5�kUM�{��zu�W�g�^��d�(�-}M�xkÿ���M���xv�l6ְ����o�B����<`k���]ͥ�5)�#��u+� ]�#.J�v����� ��� ������^�7�?�^j~"��<E��[�%�Ikd��o4nI%uQ��@�ï�Mz�u	�.S�q�)4��(���P��( �?�~x��O�մ�;�+��@�-�8�y��';p3�@�<s��ğ/lm�M��o÷��Z��Z����wi(&+�Ċ����V��%�� ����,�Ӭi�}�c�{�/�iu{ψ�]ȅ3��L�8F
20Yz��ǿ�+���#W�/g��Y���,R�ߊ-��i�WR� ��$�O�=�8EtED� I?
����?f�~ֿ-��{5/]Z��G�Q�)���S�B�F8�N09�Z�9���]6_3h���S�7�� ��J� �v��w△��6�g�VT���K�m���$��{�.d!#�gv2y�<�m���ʿp~��Y����H�_}�-S���MyE��?������I��H�s�1�HUv���X��i�|��G%Q�A� �_?��<�o<U�mGG���0��w$:M�=]h�e�IlR|�E�F*�Z�n�(���B�(��x{W�c~m,�ō�w��3%����Ƞ���� ��yN� ����-�+� � ����� �m�?�z7���+�.�{�;���ɼ�]i�ͤ�b����~��W���>���f��*-s�_�� ���>�!е�i��Z}�WZ�W�#���� YF��/Ǿ3� ���d����~	ռ}�\xo����Z�1��»!x�lƿ*s� 0+C��� ���t�����?�F�5��0�{*X�%��ɍÂ1r� ��暳�׿�t:�gy�?ؓ��g�
i� ����j~,���^h�xWP������(n\�0��@�#�#ky|gp��O�����
��σ���|�=�ힿ��z��cs�eooa<K}{r\����hb������$��`�J���;W����M#G�?�D��q�m��i�Cn��g�ž��p<�|�a�aU��_�S��p��<���߳�����/ŭs���s��ϊ����E�{u��9 �%Q��4��\񅬿������������{�,�&-#R���C�z��f�����͑{0�?��"�7�e�9b�O�� �O��������;���h:��������[όy�-�Ry��8<
��x�U�� �5s\ԯ��cV�{���ɚk����yؒ�I$�rj�FjM��|��Fֱ�W�.~�?~~�v���*�<K�mS���/��>�y��il�-������ɞ��&�,���y����<�!�_�[��'�,~����ZL7���C��=7�������Zt";�P�r�2��.�0E|/�+� �A�2~�����j^�֝e���^Z�"�,�U�r"�8Ċ��������(��χ�|a�?��&��i�ڄ0j1j�2#ia��H�F	���8B��T*]�����F�C��g�� ُ����������ω��ztr�Z�׃��Is�C}=�yW)����n��F���x��A��,|O���_\�{�WE���o��D�E��;��L��̮��L�([�b�ym�S8"F����
��Di�t�C�_���F�t+}A�&��L�_"@P��$%���`cѿe��)V����7><�|M���Oßg��GL���ӞD���h�e�ڶ�q�IXf}�H���~=?���A���V_�^���&��߆���Z�c�K;_j������*.n���2,bH�@Iن�|�]�ω���ϊ~$�7�u�jw����i�i�s������0���
(�����( ��( ��( ��( ��( ��( ��( ��( ��( ��( ��( ��( ��(��
```

## assets/logo.jpg:Zone.Identifier

```Identifier
[ZoneTransfer]
ZoneId=3
HostUrl=https://app.freelogodesign.org/
```

## assets/manifest.json

```json
{
    "id": "/to-do-easy",
    "name": "To-Do Easy",
    "short_name": "ToDoEasy",
    "start_url": "/",
    "display": "standalone",
    "background_color": "#ffffff",
    "theme_color": "#4B0082",
    "icons": [
        {
            "src": "/icon-192x192.png",
            "sizes": "192x192",
            "type": "image/png"
        },
        {
            "src": "/icon-512x512.png",
            "sizes": "512x512",
            "type": "image/png"
        }
    ]
}
```

## assets/nophoto.jpg

```jpg
���� JFIF      �� � 		

	 "" $(4,$&1'-=-157:::#+?D?8C49:7


7%%77777777777777777777777777777777777777777777777777��  � �" ��           �� : 	       1AQa�!"5STq��2s��#CRr������                 ��                 ��   ? �@              $�J�              J��               $�J�    ��<և����m��_͛��^�W"<��snK��2<^����9s��{�g|���k�l��{�g|�����/m��;���������w�\����5Lj.]�ݻ��v��1�3�m    	*��    '��Gc���MfG�F�ffb"*�33���i��&j���<��C㇗��b/�^�����U�n�e�s�UZ~�\�,y�\���W����o^���7���k��c�A����t���NW.</��܎���+�qV�U�����ƎO�����z�?7Qķ��r+�\o�����'��Z�>6��WO��n:��@=#'K�ֱ���N�;:�.�mo.�?���=��>�_���ĵ�p`   %RT     r}W��եӤcon�W��f�����x����>���NnTMuM[z=3�5����i�����N�� ~��{���]w;E������<�*��~����^��z��뛗+�ꪩ�fz��ޝ��=Ǔ�?߲���s�<��Y6�1�M���MP��իN��r����[���m⍼ߓ�y;���/��np��cA�v�=ۗb�QT�ͼ�G`5�   �IP               IT�               �IP               IT�               � ��
```

## assets/nophoto.jpg:Zone.Identifier

```Identifier
[ZoneTransfer]
ZoneId=3
ReferrerUrl=https://www.google.com/
HostUrl=https://www.google.com/
```

## assets/sw.js

```js
const CACHE_VERSION = 'V0.0.4';
const CACHE_NAME = `to-do-easy-cache-${CACHE_VERSION}`;

const urlsToCache = [
  '/',
  '/drops-6392473_640.jpg',
  '/manifest.json',
  '/icon-192x192.png',
  '/icon-512x512.png',
  '/logo.jpg',
  '/nophoto.jpg',
  '/favicon.ico',
  '/marykay_index',
  '/amazon_index',
  '/tasks'
];

self.addEventListener('install', (event) => {
  console.log('Service Worker: Instalando versión', CACHE_VERSION);
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Cacheando recursos esenciales');
        return cache.addAll(urlsToCache);
      })
      .catch(error => {
        console.error('Error en precacheo:', error);
      })
  );
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  console.log('Service Worker: Activado');
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            console.log('Eliminando caché antiguo:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
  self.clients.claim();
});

self.addEventListener('fetch', (event) => {
  const requestUrl = new URL(event.request.url);
  const pathname = requestUrl.pathname;

  if (event.request.method !== 'GET' || requestUrl.protocol.startsWith('chrome-extension')) {
    event.respondWith(fetch(event.request).catch(() => {}));
    return;
  }

  event.respondWith(
    caches.match(event.request)
      .then(cachedResponse => {
        if (cachedResponse) {
          console.log('Sirviendo desde caché:', requestUrl);
          return cachedResponse;
        }

        // Intentar la red primero para rutas dinámicas
        return fetch(event.request)
          .then(networkResponse => {
            if (!networkResponse || networkResponse.status !== 200) {
              console.log('Respuesta de red inválida:', networkResponse.status);
              return networkResponse;
            }
            const responseToCache = networkResponse.clone();
            caches.open(CACHE_NAME)
              .then(cache => {
                console.log('Cacheado dinámicamente:', requestUrl);
                cache.put(event.request, responseToCache);
              })
              .catch(error => {
                console.error('Error al cachear dinámicamente:', error);
              });
            return networkResponse;
          })
          .catch(() => {
            console.log('Sin red, manejando offline:', requestUrl);
            if (event.request.destination === 'document') {
              const altPath = pathname.endsWith('/') ? pathname.slice(0, -1) : pathname + '/';
              return caches.match(altPath)
                .then(altResponse => {
                  if (altResponse) {
                    console.log('Sirviendo alternativa desde caché:', altPath);
                    return altResponse;
                  }
                  console.log('Usando fallback a /');
                  return caches.match('/') || new Response('Offline, página no disponible', { status: 503 });
                });
            }
            return caches.match(event.request)
              .then(fallbackResponse => {
                if (fallbackResponse) {
                  console.log('Devolviendo recurso cacheado:', requestUrl);
                  return fallbackResponse;
                }
                console.log('Recurso no cacheado y sin red:', requestUrl);
                return new Response('Offline, recurso no disponible', { status: 503 });
              });
          });
      })
  );
});
```

## github/workflows/deploy.yml

```yml
name: Deploy Reflex App

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to Reflex Cloud
        uses: reflex-dev/reflex-deploy-action@v1
        with:
          auth_token: ${\{ secrets.REFLEX_AUTH_TOKEN }}
          project_id: ${\{ secrets.REFLEX_PROJECT_ID }}
```

## github/workflows/requirements.txt

```txt
alembic==1.14.0
annotated-types==0.7.0
anyio==4.7.0
bidict==0.23.1
build==1.2.2.post1
certifi==2024.8.30
cffi==1.17.1
charset-normalizer==3.4.0
click==8.1.7
cryptography==44.0.0
distro==1.9.0
docutils==0.21.2
fastapi==0.115.6
greenlet==3.1.1
gunicorn==23.0.0
h11==0.14.0
httpcore==1.0.7
httpx==0.28.1
idna==3.10
importlib_metadata==8.5.0
jaraco.classes==3.4.0
jaraco.context==6.0.1
jaraco.functools==4.1.0
jeepney==0.8.0
Jinja2==3.1.4
keyring==25.5.0
lazy_loader==0.4
Mako==1.3.8
markdown-it-py==3.0.0
MarkupSafe==3.0.2
mdurl==0.1.2
more-itertools==10.5.0
mysql-connector-python==9.1.0
nh3==0.2.19
packaging==24.2
pipdeptree==2.16.2
pkginfo==1.10.0
platformdirs==4.3.6
psutil==6.1.0
pycparser==2.22
pydantic==2.10.3
pydantic_core==2.27.1
Pygments==2.18.0
PyMySQL==1.1.1
pyproject_hooks==1.2.0
python-dateutil==2.9.0.post0
python-engineio==4.10.1
python-multipart==0.0.19
python-socketio==5.11.4
readme_renderer==44.0
redis==5.2.1
reflex==0.6.6.post2
reflex-chakra==0.6.2
reflex-hosting-cli==0.1.29
requests==2.32.3
requests-toolbelt==1.0.0
rfc3986==2.0.0
rich==13.9.4
SecretStorage==3.3.3
setuptools==75.6.0
shellingham==1.5.4
simple-websocket==1.1.0
six==1.17.0
sniffio==1.3.1
SQLAlchemy==2.0.36
sqlmodel==0.0.22
starlette==0.41.3
starlette-admin==0.14.1
tabulate==0.9.0
tomlkit==0.13.2
twine==5.1.1
typer==0.15.1
typing_extensions==4.12.2
urllib3==2.2.3
uvicorn==0.32.1
websockets==14.1
wheel==0.45.1
wrapt==1.17.0
wsproto==1.2.0
zipp==3.21.0
```

## upload_files/2882UQ_document.pdf

```pdf
%PDF-1.4
%ÈÁÄ×
9 0 obj
<<
/Length 2007 
/Filter /FlateDecode 
>>
stream
x��Z͎5��)���o	Eڙ�!.�J�(��,(9�ק�.w�=��!��wl�]�\����$@(���"��6�����"�~���� -^>
���F�����9\�d0�@��o�8E��iz�RqH�����8��QJ����禙���D7����7����u�ʬb���H�8�:�-�%���O�'���������!��-y�牟�KӞ*��(�<���BLҬ��[ �dJZ|2�}��c����1B�B?O�
��0�����Ika�)1�+o��
k�d(�˿�,"=�U�?����2:�*�Ď�ҋ3��ϙg�?g���"~�~�V(i�B�upFNU����@\�1m�M����]7!�Cٛ	��-zV��93��/�=�z�Qz(��ɪe��� � ]�UK�������
�S��2cHf���PAy��*�I�
�UH��SA�o_��dN1����!E��W�k#�}�������_�T�W ��R/5"q�}�:W�H$h'�.jQ�;��t�U1.��]���R����\�F#2�]ʑ�l+G�R���PC+�ZK�����ى�Q@��TE=^6�����,���Uu��R��\�G��d�'uT3�I5���J5�{��-�nf�����i�z�ȫ�©ծ:X541�#�N��[c��#��Ba>���&�W_�{{(���^^����<��L���M���Q�9]���'R�����|�|<�(�}r��t�t�̌�l��XmC�sj�qjdBe�q��������b�:j�E��.8I�VG��?����vhH��Z%����W�t/�?�$l�t��ec G9��A�l��ML�f?�=!���괶�Lsٜ{��v����aK 0�dN̄x`�t@O����3d�u�\�您���;�.��'�F$�5��{@i����^��.����[^����]4ݞ���M������ׯ��2F�Ϋ
�%��#�T}�+��|sgn�ASQ�=�t,��Fx����qk}���.No���G��,1�FQ�m���#g��F~���r2�t܇Mkk4�ט[D!C�r��e������n�;��Ԗ�K:X���Mj��Ȥɼ�J�ה��j�WuFTC����-��8򸸇�z��/Iw�� %bR�޼����r�-�mzח�R�ѻc�5֩Dk��|E��i�����aJ���UK��^gB�!A���<O��F�(�jUaD�\�p���j@B���[�n2h���X�x8*a�?(C���l���ׯ�81Rib����7�<[��ce�6cv�L�
�C�$Ή����>B;�%�'�ov�%6��1-A!�"��E��r7%�5W7���W�S�@��oqq�a���R��C�u��6�0b[���G��"����Հ���mn�o�T�.�<S �e�����Su����\�y��<������f�>�_�ty祾��X��V=϶�2v����*v�޺�s�y�)�K�v�ǜ'��,2/�,WYO�<�;;���\s6��_Jk'����.[����y�'��s���m$��I۳R��C�v�|���uҍ���u�R�{����Pa��I���ǜ���T�/�kzƟ�.(n0;�6`vf��B_۹��RB�*g&FM3�w�s�*���ہ�ڡ��w����yc{7Mh�B\�[8LF��Q.�{��Ҕ�bR⤆�M灚�n1!Q�ij �"�K~c��LKd�zsz�qN�����Gjz_�p�?@g�3�|��o x(�Np� �C`�/{k\�$H*�Ib���.��)�8ֽ���`���~YxXȧ��]��V�K
e�a1T��L�.W\~1t�/T���������(B�a�̺R��4<(��Fט<{��^��k%
�׷L�����&ET;�ZVK�n�0է�-(jA�&�jjY�2��:�h4𥀖J�(���:c=CK�@��l�A
endstream
endobj
15 0 obj
<<
/Length 5151 
/Filter /FlateDecode 
>>
stream
x��]�n%�q��O�/ ��_�` I3J`xc{�,�;Y�$���_߼�M6�<�h08�n���X�*Y$���Al���`�M$���������������_�~_��r�ᗲ<AB�
)�����:~}{�E����k�(;�����������0��Sz����Gn%S]������r|��/c����
+gHh}<�zLr�ї���Gۏ��g�y��W~�j�P������~��GA�N�����I�XH�	ů[��Al�2���ʶ#N��X����ga? j��IT�d�k�Be��@���(���G�<�V��
��?_���؆Z��\�<	��8����<��������};��������@����F��	[��I0DlQ�j����q�#1��G���N!O�7/w ��pT��7�T�%<����4�[J�e@2�,�TKR!�d�ҷ`f�5��&H���^g����V��Sy�6Tb���J|	���5�h�G��3y�׀��s��W�v?���������y|��V��JR�7S�ķ�Jˢ�F*���,��a���h4��a��Z2B�i�@D�8K���.��27o��b�]=T�R������e��i��*dG<�>YP=�AcY9V�B_juv�<5ݣXvn;�#��i�4�#U����촨艷\ap _zp�ȡ�v�@�ZZW�e�PT^��k=�R�T�|.���8^r��Kc_���� �ԇ ��5��;򮶧�B!*n5�榺��y��}����f�?
��I�g;������V����5��%{����Ҟ�B��N`vGI��o�GP�m��{��U���)��;�~v(������4�1��0#mlL���ڐѾ�g�7QX�5ׅ��š|�~�۸@%i��2f#��lt-f�8�"��{3�o� @��`)T,��}DEY1���%]L�J{�,���2i2=:2��3K���Ů&���ө&_�p+:�N� ��N%:4碜{H��4�c�5>�&��&ĺ���gO~j]�N(��ӈ%�
/�ИjQBRh������?�W�@bY�
�#k�Y��p���K�q����X���������y���݇C9��L�'� �Pl��݇��p8-�^ A(6�S�O���ᴐN�PD8�@���T���p��F�N>��=���nQ/�X�܅�J��F��E b�9q��Ǔ5�F���R����3�5zuݒ�@ƘM�U݂��ȆT;DO���↋�ҪE�x�(��J��3�=Ο����G��x��]�(����B�����d��!��dEt'�uՒ�FƆ[4��Ma��^oм��(�j+.z��n�$wo/0�d�&�� �{dH����X�@�W�1�n��R�d��4MO����Χ�(�d�'�u��k�7�VuK�[c�r�h]�$J��z�hU� jc^���k��}h����G�F>�{S��ht�/3u*��N,��ɓ['cn4}�.��i�:���K�T؁�v�H��2��L��[���$Z�-�r��J���uK�vn��&ѪniQ����u���S��#Z�-�Z�Bz��ħ{]+Uw2��f�������x'���]Z��#��h]�$��h�&Ѫ���:2�d���-d�|�!��"�I��:��[�k�=X�HP�V���{���4뺍gX��Q>�7��:�%9%�\v��� �B#�@�+�l�BFv7�=��Cv�=��=�������Ӹ������J�Z��`�3�z�4��7�"r���`&B�,��9��w
5�4���N�X�)wx�N�â���mךnu��$ٓ�d>�NHO�y��t.��ѯ�4q-Փ8|�8�vz�'�``��E"]�궛M�4�6�G����M���k^�'ޙ�[F�L�x��FJ7��a�2-�~ĚY\G��7���&�X��巜=��?O�T�a1�CQN�rDcz��
^L�X��=�r#��;���O�X�e~^�		 �@oA(y���m`�D��	����^��a$r� �� Q��-•�j��,H�D�����-•�j��,H EX��d��^��a$rcX��J��Nqb�e!�T5�s���E)�ɓ3��!����p���b.dS�	�u�X�*�̽jdD6�����+8pg]���Z4n�_�!-�g� ��҈)�JC�6W���dV6<�)E�oywBX2�iF؛M1��� ��o�*D�uA��(��B�y�	S�"2�bC���������Cx�Y������3��,��u.R��+��3�R�8��p�1[��U�8s�!�<����tWj,�B�Y��!���fW=��~�<�
��[�a5�2I��L���T��BI�ﮎ���^�f�T 1Ks�=8��?�3L�VKQ��o�^���m4��k:� ��5��8y�z�b��xi��n}Zg4Y�X��-����lӈ��Z��!,,v5$'�E`��bW�2�!g�|	<�M��!�x��X�_!��D���IB�s���A�1��S�-ݻ"�������ɟF]r��ӭ���߫�}�%��wF����"w�,�E�8��b�,��q3����3'��vsJ];�G?z
M�FO7�m�É���;�[�B����^@n�TP�[Xe��Tn��|��R��`�v�I��V�������i�'�n��S�@K���` q\h���^�����_;&�=����=b���XFp���L��c����Xf�������X�l�;�2�Mz�X�ӽ�2L}`,��|)0�ã1@�gC?�R��b7��vƀe������kڌVׇ��3���?,ZI��V��7�>���R+�Yw1|3N9�d?N��v┽�� �~XNr��S�|�{��H���y�ů�FY0����_#�I��9�ـ��Z�_(�9���J]́�<�ʝ���x�L�^�i`�5ӛ�di�����.7��7xs��KԼg�sEoq��D	�V�J�HRq��y��LRq�G�S�� ���=���xrR?E�)#)O�8V)�S�7RO�ցʌB�)Þ�x׿ oy}�RV�)��},D*Ds2��c��%����.N����p���G$ɸǔ���:5G�C�bK.T��s{�Ӂ`����]�9�����c��%�����_�K�?��c���khG8�%�.}���e�?���I`"�*J��0�/w!�R(�s��.��z	u���jQI��[u��&Ѫn5�Cr�^�_�������V'��߸=6��fդ=J����Tl��[Q>��Ӊ�u�"�U_[;^�R�j�$���E��Y�.�a�>��� �ӢB��U]�^����9ֲY�2�����kK�]�n����9��7%��<�>�)���$��dm��D��[�TLl�ꖓ;�\@�At�6$3;��+x�
U)�KĽ���yK�X���pM��n��5q��T��Jk�f�lU�$+��M�ى!x����|�㝳Mc�����.��a{x�����b��<����Q������ײ���V�}�����	�hAMp����R
:�oK��64��AKr�`w�D%j�ZI��8|���(D}�˿�\�o��}��@�7Ӡ.1u����[�v��͔���W;2���N+��RHR�*_��`}�-%����K�H�Aܱ�^"C��/�,�X$n�V�6䎔=��EθX{~�4���ٶ�-�s�9�M9d�8�UF���{�Ƭ���6v�kIfnCy��(xN{�g�槌3G��=�(�@3��0$F��:�.I)�����#,"�Qa���GX$���<�[�t��=�V��G8[ֶG`�=��:�u�s�.�x��=�hO&�!��}��"p2�׎`H����69�w���"�# 3G�����`�� ��^�D�s�V���r�=G7?�?f��cp�߷1��qNw���1$f:�=�fpi���[\����<w�`�}6��;<���ͭ}�"VAl��E��X�45q>u��u?���"��;��΄�,wX��;{;ʪ���M*�O䟪b��l�"�z�w@���3�E(��q�7_T\���iz�[�F/L��[���ni���=�:6/�s�tr��U]6b,���d|b}9̺-�3�?��=L��=���i�j��=@� S���qb&�L�6�`?3�ӳE=�tiqzC�7��?��ӈoQ%������*��*�*�ż��R�8&�x��������Z��k���\�؉���Ea����%��<ؠˬ<�Kx��%l�(�Y�� �h*��}D�� ��E�o�J�1� 2���`�e%���3@�Rc@5�Hh��Te4��3V*�����+�,�肂>�����s/:���ku�>��ny-/�[4T�'?������ہ�<Cx�Wo�r����x��W�e.�� )`���Ƃ�� -ie8��\靃�+\l`�#�W��`�����<=����÷���2��S�psq7�lluw�Wg��������1u�	ɇݤ�!|�MZ�>�&�!nD�HѡG�c#�m�����B���G7��v�V7��)�ۜ��3�1t�4��٭TV��"�S���-��n����M�U�r4	'�v��uK��;��&Ѫn��:����D��׉`�G���|#b�hS�"K��]�U咬-��Uu݊���/ݥZU���Rd�Vw��,��K���`ou���Ž�0�������_Ĵ{.%Y��p�G)cf����$���В��L���f��߿��͠���*�t����E��{�!_��)隿ɾ^��_Ao�M�h��Bu��n����`6� �$z���}����B���&�HzG.��k�fm�o�{֡DÌ��.�A���+2���"C��+�B���2�c��2��,
���,�ѐY^���WP#F9K�Z����l=f�q1��q=�^a�Q3<Jp�����[��_g��P�ۑ�+����W?��c�R��q�ݳ.�<��Y?���X[�X>���t�|��Cgѐ��๏�ژ�	��x��^��
endstream
endobj
6 0 obj
<<
/Parent 7 0 R  
/MediaBox [0 0 597.6 842.4] 
/Type /Page 
/Resources <<
/ProcSet [/PDF /Text] /XObject <<
/DL95 8 0 R >>
 /Font <<
/F-0 10 0 R  /F-1 12 0 R  /Helv 11 0 R  >>
 /ColorSpace <<
/DefaultRGB 4 0 R  >>
 >>
 
/Contents 9 0 R  
>>
endobj
13 0 obj
<<
/Parent 7 0 R  
/MediaBox [0 0 597.6 842.4] 
/Type /Page 
/Resources <<
/ProcSet [/PDF /Text] /XObject <<
/DL96 14 0 R >>
 /Font <<
/F-1 12 0 R  /F-0 10 0 R  /Helv 11 0 R  >>
 /ColorSpace <<
/DefaultRGB 4 0 R  >>
 >>
 
/Contents 15 0 R  
>>
endobj
7 0 obj
<<
/Kids [6 0 R 13 0 R] 
/Type /Pages 
/Parent 2 0 R  
/Count 2 
>>
endobj
2 0 obj
<<
/Kids [7 0 R] 
/Type /Pages 
/Count 2 
>>
endobj
16 0 obj
<<
>>
endobj
8 0 obj
<<
/BBox [-20000 -20000 20000 20000] 
/Length 114 
/Filter /FlateDecode 
/Resources <<
/ProcSet [/PDF /Text] /Font <<
/F-0 10 0 R  >>
 /ColorSpace <<
/DefaultRGB 4 0 R  >>
 >>
 
/Subtype /Form 
>>
stream
x�U�1
1D�=Ż@�$�ɏ 
Z�	��J�j���BXf��y�˕�+1Uņmk,#��C��~�9���[��*}���$ei�<k&d�hGy��2�����<��\�� zQ�
endstream
endobj
14 0 obj
<<
/BBox [-20000 -20000 20000 20000] 
/Length 112 
/Filter /FlateDecode 
/Resources <<
/ProcSet [/PDF /Text] /Font <<
/F-0 10 0 R  >>
 /ColorSpace <<
/DefaultRGB 4 0 R  >>
 >>
 
/Subtype /Form 
>>
stream
x�]�1
1D�=Ż@�$�ɏ ��vB:���b���BPf��c�$�ILU�a���mf�?@<��A4��k�`�X�ϗ����,��om	�,Z�QN?W���߸�O����w�
endstream
endobj
18 0 obj
<<
/D [6 0 R  /XYZ 10 866 null] 
>>
endobj
19 0 obj
<<
/Names [(Total-Page-Count) 18 0 R ] 
>>
endobj
17 0 obj
<<
/Dests 19 0 R  
>>
endobj
1 0 obj
<<
/Names 17 0 R  
/Pages 2 0 R  
/PageMode /UseNone 
/Outlines 3 0 R  
/Type /Catalog 
/ViewerPreferences 16 0 R  
>>
endobj
4 0 obj
[/ICCBased 5 0 R ] 
endobj
5 0 obj
<<
/N 3 
/Length 2591 
/Filter /FlateDecode 
>>
stream
x���gTT��Ͻwz��0tz�m �I��2�0��ņ�
Di� AFC�X�BPT�� ��`QQy3�V���{/��ý�����]�Z �O ��K���C����1�t� �`�9 LVVf`�W8��ӝ�%r���# �o�����I���  �ؒ��b��@�i9�L�}V�ԄT1�(1�E����>��'���"fv:�-b�3��l1��x[��#b$@ą�\N��o�X+M���ql:�� �$�8�d����u� p��/8�pV�I�gd��I��K�nngǠ�pr�8�q0�������L^. �s�$qm�"ۘ���[��Q����%��gz�gm�w۟�e4 ���f�ﶄ* ��  �w�� $E}��E>4�$����999&\�D\���������x���C��$2�i��n���!����dq������0
�$r��("R4e\^���<6W���ѹ�����}�k�(�u�	��F�� E!$n�h��o�H �yQj��������.?��I���C��,!?���Z4  I@
@h=`,�-p .��� b�
�� �A��@!(;�P�@#hm��'�9p\��0�F�xf�k� A"CHR��!C�b@N�' �B1P<�� !�m���2�����o��9�24݅Ơi�W���$�
��:�)̀]a8^'���5p����#p'|�
ã�3x�!�1�@ܑ $ID��z��@�6��Gn"����AQPt�1�僊@�P�P�Q%�j�aT'�u5��E}D���hC�=��NB���&t�z=�~��`h]�-��I��Ŕ`�a�1g1C�q��U�b�AX&V�-�Va�`�`o`'�opD��煋��p��
\�4�n����k���Ax6>_�o����'�i�.��NH!l"T�/�D�юB�7+�G���cķ$�ɝG�v��Β�^��d�9�, � 7�ϓ��HP$L$|%�$j$:%nH<��KjK�J��\#Y!y\��^JG�]�)�^�F��m�9i���t�t�t�t��e�)�����[�@��y�q
BѤ�SX�͔F��Cե�RS���o���YYY+�H�ղ5��dGiM��KK��Ҏ�Fh��T�\�8r����n���+ɻ�s������)�<Rv)t)<TD)(�(�(�W��8�DUrPb))S��+(�*�U>�<�<���⭒�R�r^eF��ꢚ�Z�zZuZ����U+W;���.Kw���+�}�Yueuu�z�������F�F�F��CM�&C3Q�\�WsVKM+P+O�U�6^�����W�_{^GW'Jg�N�Δ������V�zd=g�Uzz��1��T�}��`k�d��k����!�p����Έg�`tۘd�j�m�j<fB3	0�7�2yn�ek�˴�����Y�Y��}ss?�|��_-,X5�,ɖ^�,�-_XZq��[ݱ�XZo���`ck÷i���ղ�����͠2�%�Kvh;7�v'���������`����0�Dw	gI�qGG�c���)��Ө��3ӹ�����ۥ�e�U�5����s737�[�ۼ���:�����G�Ǡ��g�g��#/�$�V�Yok��g}�>�>�|n����|�}g�l������������z�@��݁�j/�-�
A�A����
�>R�$�<4/�?��2�%�u�[xi���aDo�dd\ds�|�GTY�h�i���1�1ܘ�XlldlS��2�e{�M�Y�ƍ,�]�z���+�V�Z)����x<:>*�%�=3����K�M�M�e������]���i�#��3��X�8�䘴;i:�9�"y��έ�H�I�K�OJ=����֞�K�O?�����2T3Vgeff���_�g�,ߟߔe-��PE?SB=��X�SvM���Ȝ㫥W�V��nϝ\��뵨����y�y���ֹ��_�OX߻AsC�����o"lJ��C�Y~Y���Q�{
T
6�o���Z(Q�/���ak�6�6���۫�,b])6+�(~_�*���W�_-�H�1XjS�'f'o��.�]�ˤ�֔����YN//*�g��Vu{	{�{G+*����vV��N��q�i�U��^;�����~��mu*u�u�pܩ���l�i�8�9�}�Icdc�׌������>�=z��ٶ��E���n�N�;r��o�ی���i��G�Q�ѧ��;r��X�q��﴿���tuB����]�]��1�C'�N��8�t|o�����'kNɞ*=M8]pz�̚3sg3�ΜK:7޻�������B�/�_�t����~��3�/��l��ƕ��6W;�:~���c�f������v�{�����|��M��o�޺:�txh$b����ۣw�w���}q/�������J=�x����G��GmFO�y�<{|�5�짬��O<!?��T�l���:9�5}�鲧�2�-��,�s�s��������l������_K^*�<���U�\�ܣ����(�9����]ԻɅ������?�|���`1}q�_����
endstream
endobj
3 0 obj
<<
>>
endobj
20 0 obj
<<
/Length 525 
/Filter /FlateDecode 
>>
stream
x�]��n�@��<��Cdvv�N$�D H�T�} c/�R�-c�}���$Q9�>vf<�L��mvm3����U�8�c��C�tס��OMkfVL�T�b���eof����2��=vf�X���t|��yX��!~3��PǡiO���z?������9��������x/�����h���8�>ο����������x��*e{�����ki��4����Gsd���r���GB��o��0�D���>r_�9�������g���0_�&�q�<H�|E���&Dߜ�-|s�Z�:=����X�:�Z��/����Z�-_����s"|��9���7�6�υ�c����_�RB_�
|�"�˞�����/*�u�v���\�:�L��5�� �W8}���R��<u��ї�|=����q��5�+�;��:��BK�W8__��:���W�2�����oО�{��y������W���&=|���|�T�\���%q�#i�}���:��J[1-��Zj���9��Oy|{�02v
endstream
endobj
21 0 obj
<<
/DW 500 
/FontDescriptor 22 0 R  
/CIDSystemInfo <<
/Registry (Adobe) /Ordering (UCS) /Supplement 0 >>
 
/W [0 [0 833 556 333 500 666 722 556 556 500 556 222 277 666 500 666 556 833 556 556 556 722 722 277 666 666 277 500 556 222 556 277 556 556 556 610 556 500 277 277 556 556 556 722 943 277 610 556 333 556 666 556 556 277 666 722 500 889 556 333 333 500 722 777 666 777 777 556 556 0]] 
/Name /F-0 
/BaseFont /SUBSET+ArialMT 
/Subtype /CIDFontType2 
/Type /Font 
/CIDToGIDMap /Identity 
>>
endobj
22 0 obj
<<
/Ascent 905 
/ItalicAngle 0 
/CapHeight 715 
/FontName /SUBSET+ArialMT 
/MissingWidth 1000 
/Descent -211 
/FontBBox [-664 -324 2000 1039] 
/StemV 0 
/Flags 32 
/FontFile2 23 0 R  
/Type /FontDescriptor 
>>
endobj
23 0 obj
<<
/Length 46140 
/Length1 46140 
>>
stream
    	 0  `loca8U    �   fpgm�A H  b  �maxp�        head�     �   6cvt �Q     nprepB 6  0  /glyf#�S   �  ��hheaH     �   $hmtxQ�    �        �;��_<�     ��'*    ք�����g Q   	         >�N C ���z                 F  � �s J� �  !V �� fs Ds �  ?s �� �9 $V��  PV \s K� �s Us Us U� �� �9  V �V �9   (s �� �s F9 �s �s <s � 0s �  9 �9 �s Vs Ms �� �� 9 �� �s �� As aV �s Ss B9  V �    ws I� |� |  �� �9 XV 	9 c9 ms Ds H� �    F� < �    @ �  �  �T�A,,,"  +* < *��(�&м) �) )�+�'�;@�#�2A-   /      o  �  �   _    � � � �       o � � � A'    � �   / O _ � �   _ o  � �  @��3@���3@��jl2@��a3@��\]2@��WY2@��MQ2@��DI2@��:3@��142@��.B2@��',2@��%2���
2�A �  p �   � �    @�$&2��  d ���2A
��  �� d ����2�AJ� �� �� ���� �  � ?� �� �� �� �� ������ � /� ?� _� �� �� �� �� �   �  � ?� �� � �� � ����Ӳ792���Ӳ+/2���Ӳ%2���Ӳ2���Ӳ2�Ҳ�)�&�;@�" > 3"�%1��<i�� +�A0� ��   � �  � P� `� p�  `� p� �� �� �� ��   � �  �  �  � 0� @� P� в +�ϲ&BA��  ��  ��  ��  ��  �Ʋ A�  � � � /� ��$�A�  � /� ?� O� _� �� �"�dA� �  � �  � � @j@&CI2@ CI2@&:=2@ :=2� �&@&��2@ ��2@&��2@ ��2@&��2@ ��2@&z�2@ z�2@&lv2@ lv2@&dj2@ dj2@&Z_2@ Z_2@&OT2@ OT2���$'7Ok Aw 0w @w Pw www �  ��**��@+)*�����R���e�~���<�^�+���@��8  �@��@��8  �9@�����s�&�%�$� 7@�!�I3@�!�E3@�!�AB2@�!�=>2A! ?! !  �! �! �!  @!� "2@�!�2@�"�*?2@�!�.:2oAJ� � �� ��  /� `� ��  � ?� _� �� �� ��  �"  �"  " /" ?" _" " �"  �! �!  o! ! �!  ! /! ?! O! ��""!!@+H�O�7    ����� 	A	��  ��  ������&�A�  9 &% 8 s 5  4 � 2�V��&,� ��������� ���������/���&��� ���8�ʸ��&���~&���}Gk��e&���^s�@R&ZH�Db@s��?^<&���5��0�+��*V)��#��5UU7�h@,�XO62,!
 ���@+                     J �KKSBK��c Kb ��S#�
QZ�#B�K KTB�8+K��R�7+K�P[X��Y�8+��� TX������CX� ��� (��YY v??>9FD>9FD>9FD>9FD>9F`D>9F`D+++++++++++++++++++++++B��KSX�5��BY�2KSX�5��BYK��S \X���ED���EDYX�>�ERX��>DYYK�VS \X�  �ED� &�EDYX�  ERX�  DYYK��S \X� %�ED� $�EDYX�		 %ERX� %		DYYK�S \X�s$ED�$$EDYX�  sERX� s DYYK�S \X��%ED�%%EDYX�� �ERX� ��DYYK�>S \X�ED�EDYX� ERX� DYYK�VS \X�ED�/EDYX�� ERX� �DYYK�S \X�ED�EDYX�� ERX� �DYY+++++++++++++++++++++++++++++++++++++++++eB++�;Yc\Ee#E`#Ee`#E`��vh��b  �cYEe#E �&`bch �&ae�Y#eD�c#D �;\Ee#E �&`bch �&ae�\#eD�;#D� \ETX�\@eD�;@;E#aDY�GP47Ee#E`#Ee`#E`��vh��b  �4PEe#E �&`bch �&ae�P#eD�4#D �G7Ee#E �&`bch �&ae�7#eD�G#D� 7ETX�7@eD�G@GE#aDY KSBKPX� BYC\X� BY�
CX`!YBp>�CX�;!~� � +Y�#B�#B�CX�-A-A�   +Y�#B�#B�CX�~;!��  +Y�#B�#B +tusu EiDEiDEiDsssstustu++++tu+++++sssssssssssssssssssssssss+++E�@aDst  K�*SK�?QZX�E�@`DY K�:SK�?QZX�E���`DY K�.SK�:QZX�E�@`DY K�.SK�<QZX�		E���`DY++++++++++++++++++u+++++++C\X� ���@t sY�KT�KTZ�C\ZX� �"  sY +ts+s++++++++ssss+++++ ++++++ EiDsEiDsEiDstuEiDsEiDEiDEiDstEiDEiDs+++++s+ +s+tu++++++++++++++stus+stustu+++t+ +++ EiD+\XA6/ A 0/ - -/ 2 2/@&7	7
DD++++++++Y+   @[�tsrqponmlkjihgfeb]XWVUTONA@?>=<;:987543210/.-,+*)('&%$#"! 
	 ,E#F` �&`�&#HH-,E#F#a �&a�&#HH-,E#F`� a �F`�&#HH-,E#F#a� ` �&a� a�&#HH-,E#F`�@a �f`�&#HH-,E#F#a�@` �&a�@a�&#HH-, < <-, E# ��D# �ZQX# ��D#Y ��QX# �MD#Y ��QX# �D#Y!!-,  EhD �` E�Fvh�E`D-,�
C#Ce
-, �
C#C-, �#p�>�#p�E:� -,E�#DE�#D-, E�%Ead�PQXED!!Y-,�Cc#b� #B�+-, E� C`D-,�C�Ce
-, i�@a� � �,���� b`+d#da\X�aY-,E�+�#D�z�-,E�+�#D-,�CX�E�+�#D�z��Ei �#D��� ��QX�+�#D�z�!�z�YY-,-,�%F`�F�@a�H-,KS \X��YX��Y-, �%E�#DE�#DEe#E �%`j �	#B#h�j`a ��� Ry!�@��� E �TX#!�?#YaD� �Ry�@ E �TX#!�?#YaD-,�C#C-,�C#C-,�C#C-,�C#Ce-,�C#Ce-,�C#Ce-,KRXED!!Y-, �%#I�@`� c � RX#�%8#�%e8 �c8!!!!!Y-,K�dQXEi�	C`�:!!!Y-,�%# �� �`#��-,�%# �� �a#��-,�%� ��-, �` < <-, �a < <-,�++�**-, �C�C-,>�**-,5-,v�##p �#E � PX�aY:/-,!!d#d��@ b-,!��QXd#d��  b� @/+Y�`-,!��QXd#d��Ub� �/+Y�`-,d#d��@ b`#!-,�    �&�&�&�&Eh:�-,�    �&�&�&�&Ehe:�-,KS#KQZX E�`D!!Y-,KTX E�`D!!Y-,KS#KQZX8!!Y-,KTX8!!Y-,�CXY-,�CXY-,KT�C\ZX8!!Y-,�C\X�%�%d#dad�QX�%�% F�`H F�`HY
!!!!Y-,�C\X�%�%d#dad�QX�%�% F���`H F���`HY
!!!!Y-,KS#KQZX�:+!!Y-,KS#KQZX�;+!!Y-,KS#KQZ�C\ZX8!!Y-,�KT�&KTZ��
�C\ZX8!!Y-,KRX�%�%I�%�%Ia � TX! C� UX�%�%���8���8Y�@TX C� TX�%���8Y C� TX�%�%���8���8�%���8YYYY!!!!-,F#F`��F# F�`�a���b# #���pE` � PX�a�����F�Y�`h:-,# � P��d� %TX�@�%TX�7C�Y�O+Y#�b+#!#XeY-,�: !T`C-,� B�#�Q�@�SZX�   �TX�C`BY�$�QX�   @�TX�C`B�$�TX� C`B KKRX�C`BY�@  ��TX�C`BY�@  �c� �TX�C`BY�@  c� �TX�C`BY�&�QX�@  c� �TX�@C`BY�@  c� �TX��C`BY�(�QX�@  c� �TX�   C`BYYYYYYY� CTX@
7@:@;@>?�CTX�7@:�  ; �>?��CRX�7@:���;@�  CRX�7@:�� ;@�� CRX�7@:� �;@�7@:�  ; YYY�@  ��U�@  c� �UZX�> ?�> ?YYYBBBBB-,�CTXKS#KQZX8!!Y!!!!Y-,�W+X�KS�&KQZX
8
!!Y!!!!Y-, �CT�#�_#x!� C�V#y!�C#�  \X!!!� GY�� � �#� cVX� cVX!!!�,Y!Y��b \X!!!� Y#��b \X!!!� Y��a���#!-, �CT�#�{#x!� C�r#y!� C��  \X!!!�cY�� � �#� cVX� cVX�&�[�&�&�&!!!!�6 #Y!Y�&#��b \X�\�Z#!#!�Y���b \X!!#!�Y�&�a���#!-,-,�%c� `f�%�  b`#b-,#J�N+-,#J�N+-,#�J#Ed�%d�%ad�5CRX! dY�N+#� PXeY-,#�J#Ed�%d�%ad�5CRX! dY�N+#� PXeY-, �%J�N+�;-, �%J�N+�;-,�%�%��g+�;-,�%�%��h+�;-,�%F�%F`�%.�%�%�& � PX!�j�lY+�%F�%F`a��b � #:# #:-,�%G�%G`�%G��ca�%�%Ic#�%J��c Xb!Y�&F`�F�F`� ca-,�&�%�%�&�n+ � #:# #:-,# �TX!�%�N+��P `Y `` �QX!! �QX! fa�@#a� %P�%�%PZX �%a�SX!� Y!Y�TX fae#!!!� YYY�N+-,�%�%J� SX� ��#��Y�%F fa �&�&I�&�&�p+#ae� ` fa� ae-,�%F � � PX!�N+E#!Yae�%;-,�& � b � c�#a �]`+�%�� 9�X� ]  &cV`+#!  F �N+#a#! � I�N+Y;-,� ]  	%cV`+�%�%�&�m+�]%`+�%�%�%�%�o+� ]  &cV`+ � RX�P+�%�%�%�%�%�q+�8� R�%�RZX�%�%I�%�%I` �@RX!� RX �TX�%�%�%�%I�8�%�%�%�%I�8YYYYY!!!!!-,�%�PX�@  c� �T\�KR[�Y-  � � � &   ��  ��  ���i��� �i���   �   �     � �i � � ��  � � � �  D � | � �  Z � � R R  D ��� / �  � �  W ~ � ��  �� � �  " A P o �L�u \ �� 7 L n p��X������ � ����   c c ������ - \ � � ��	� @ W � �� r �]�g��  ! w �  M ��+ L e �|C�������   ] h � �5G!\�M��  - x � � � � � � � ������  , I  � ������?     ) 9 I o � � �#�o2@z��  1 U W � � ��~~�F�B  � � � � � �/OV)o�r  , 1 1 d i � � � �+��������  & � � � s���C_�����a  ^ m � � �8Q[h|������ATk�hq�BBSs�����X�������2�� Q | � � � � � � � � � � � !U{{~������������  !""#rw�������"+5<Yoq�������22������� ����*��� ����������      < Q a a j x � � � �*>LQ_jqx����������� !".5BOO^eq�����*G]ety���������
"&+G_u���\��
m���6>PQ]���` � � � �            ��E� �3�� - _ dM?  ��}�$x;;N �&����;MKS j1      �   <� ��e�� x~� � 9  �0+� ��� �
��P�>X !� �q} �E  
��+N� � T2�� N � 7� � k� � w � �dg � 3| � ��)n*�i�� �  9$ �]��� u �
 �����M�Rh m } � q�� yX�g V %� � |2! �  r \ / �  � � AM r   LjU � � � � �  x i  W n � �T� ge �  ��R Z�� ��g n�� -�� ��| � � � � ���{ p  � �LF�F�-��S� �              % � � �   >� �� S ?����  ( " � b J � m � � H� 3�N��Fp y� Q���
 h�l O � � a+ ��� � { eR�te�i � � \ @ � u � �q�� � � � � � � � � � �           B����@ � 
� ��1 	�. +�<�<N�<M�< ?<�<�<�<10!!%!!  � ��@ �  �   �  � P��+X�*�@�V*�@ V�CTX� ��@UU���U���@(UU	 	 	
UU����U ���U ����U ����U /+++�/+++� ??�����9++10+++ �CTX@ U U U U U���@#UUUU	U
U����U���@U& 
4 
4  
���U
���U
�V  V@ U U ����U /+++�/�++ ?<?<<9++]10++++++++ +++++@ v��	II)%,X[vx�96OKD@MB
������00RR@	
 	`��� 1� �1�	

�@�V

�@@	V
 @�V � �� A
��  @ V  ��  @�V  p�V� `����;Y+�]�]<�++<���]<�++<���] ??<<<<<<<<��.+�}ć.+�}�10 K�SK�QZX� �� �� ��888YK�SK�(QZ�C�@PZX� ���
88YC\X� �Զ!9,!9��Զ79279��Ե-9,-9++++++Yrq] q]]YY ++@  ?3?3?3??01Y3!67!##�$[05_��V��X���HP���F��5��   J��> ( 7"��+X@,		**)**967:*I*]]*ji*`0��)���(���U'���@U��(��(��(��(D���@UUU5���@OU+,*499,IH,VY+fi+v����+74/$42!_)o))/?���������  @�VU���U���@UUU&�@�V�@�V���,�@@V,

BU� ���@U E'
2)aa A��  @ V  ��  @ V  ��  @@V U %!$���U$���@U$U$���U$����U$���@U$U$����U$�[@'@ && &0&�&9����U&��ִU&���  @�V&19���@#409�9�99����U�@@	V%"/�@�V/�@�V/�@@V/$��?�@�V�@�V�@@.VUUUUUUU18�++++++++++]q�+++��++]q+�+++]��++++++++<�++++�� ?�?�+?��++�9/++++++++]q�q999910 ]++++q]++ q� ++)�-�l'
2�-�l�/�l ?+2/3?+?9/+93901Y%#"&546676767654'&#"'>32#&326765<d�j��GsH5k�g3E�y�nЉ��P	"�b�o\2mih�&�UF��N�N$%
n-=Yqq�K@aJ.x���=8�((M/H`[O=w   �  �> ��+X@;/#4CSft				  
	(�" "�@�V�@�V�@�V% ���@364�     � �  ����U ���@U U U ����U ���@U U U NG�+�++++++++]q+<�+++�]�r� ???�999999 ɇ}�10 ]r]� 
	�6�l ?+22??01Y336632&#"��>i?[^>BB;^&�qH:�'G?`r��   !�Q�& Ű�+X��@�V�@�V�@�V�@�V�@ V ��  @�V�@�V�@�V�@�V�@�V�@�V�@�V�@ V ��  @�V�@ V�CTX@
@ @ U/+���� ???�910����@s9(V�
@@ (04 (04	'''665�((HYYYiiiyvyzz������
�����
�����BU�CTX@D� ???�9]99@7
 %

%

 /��?�@@�T@?@_��B�" E
�T@ @@ 0OP��B�/�?� |f+�q�]q�����]q���]q ?�?<<<�.+}ć.+}� 9�<<�K�SK�QZ�C�@PZX� �� ��88YY+10C\X� �޶79
"79���9"9++++Y]q++ q]+]Y++++++++++++++ +��3@
l

 ???3?+01Y'326767673673#";,<H&�m��+"+��lA$0|V4�g�($k(��u�|vk�ȯBYS   �  R� T��+X@"79	:'
56
G
W��v
��
���@U(����
5�	���@	!4 !4��޳9	���!4���!4���!4����4���@C9	%%=	=*BU	
	
 

	 

  
 �:@0����J�:@0 ������@�V�@�V
�@@V     U ����U ����U ����U ����U ���@
U ];�+�++++++]�+++�]q��]q�<<<< ?<<<?<<<9/�.+}ć.+}�<<K�SK�QZ�C�@PZX� ��8Y�CTX� ��4���@444	4
4 ++++++Y+10+++++++C\X@	"9,9,9"9��޶9"9���@9"9@9��޵%9@9+++++++++++Y +++qr]+ q]++@	

   ????9/39301Y33!!������� �����)��������  f��v� /��+X�cj���U ���@_U  2c p t� �� ������� ��*(* GVWVhk{��������  ��޲(9���@ (9 	&J & �@�V�@�V
�@@
V& �@@VUc\+N�++]M�+++N�]M��� ?�?�910++]]q ]++r@
  �2�l	�2�l ?+?+9/39/301Y#"$54$32&&#"326��=�����כ�C��,;�3��\m憣�1���n��U���-�����銼   D��'>  ���+X�U���U���@eUU
GHVYgi4::5EKKE\\	R]]Rmm	dmmdw	[TT
[lee
l
A��  @ V ��  @ V ��  @@V$@U@U���@UUU���U���U���U���U���@$%40  ���  @�V1����@#40�@�V�@�V�@@AV$ U U U U U U U U @$%4 ?  �@�V �@�V �@�V 147+�+++]+++++++++�+++q+]�+]]++++++++++�+++ ?�?�10q] qC\X@	SS	bb	]Y ++++��/�l�/�l ?+?+01Y7632 #" 32654&#"D����{�������������'�v������������  �  �> 氅+X@���������@"4y���� 
A��  @ V ��  @ V ��  @@V$@U@U(UU���@UU"U���@UU���@U
U���@U@364��N���@464��p���3�@�V�@�V�@�V% ����U ����U ���@U U 
U U ���@U U U ���@364�     � �  N�]q++++++++++<�+++<�<]q+�]q+++++++++++++�+++<< ?<??�9910Cy@	


&
 +++*�]q +]q@	

�0�l ?+2???01Y33632#4&&#"��u�`�P
�*kHs�&��EpM2}�s�nmA����  ?���> 0��+X��@�V�@�VA7@ V (��  @ V '��  @ V &��  @ V %��  @ V $��  @ V #��  @ V "��  @ V !��  @ V  ��  @@|V"":	J	D$V"e"|	�	�$��,�	0K,�U2
\\	\
\\\jj	j
jjj�&�''&$'$)6$Z
Yd&d(t#t$�$�
��(�,�0�
��'�(�&�&(����U"����U#����U$����U(����U"����U#����U$����U���@9Z'%
 &.��@",U?O_��o���U   � ��@U@� ����4���@4.\l����U���U���@U.$@42���@2UUUU U UUUA	@ V [ ��  @�V$*����9�**���U*���U*���U*���U*���  @�V*2���@!'*4`2�2?2�22$ U U  ����U ����U ����U �@@V $UU U���@UUU�@@V"� ? O  147+N�]qM�+++++++�++++++�rN]q+�+++++q+M�+�++++++++++�r ?�+++?�q9/++]qr+��]qr+�99910Cy@@'-#,&"  	(-  !# "#)
('	
+  ++<<+<<+++++*+��� +++++++++]q]rq] ++++++++++++@
 &&.�/�l.�/�l ?+2/3?+939/301Y732654'&'.54676632&&#"#"&?��{|x5%�ƙOA8*�S}�Z�si|j/���Vi�}��=kreD=#%2I�NGy(+H{gR\R7#
$3A|\Z�W�  ����& ���+X� ��@	4 4���@4+$ 
 3A��  @ V ��  @ V ��  @@V%@364@U(UU���@UU���@UU���@UU���@U��N���@464��p����@�V�@�V�@�V%	���@364�	 	 	�	�		����U	���@U	U	
U	���@U	U	U	NGP+�+++++++]q+�+++]q+�]q+++++++++++<�+++� ?�??<99910Cy@   ++**� ]+++� 
�0�l
 ???+2?01Y!5#"&&'&53326653?|�^�O�nQQ�;���HmO5s����1GQS��9��  �  7� ���+X�
�@�V
A@ V ��  @ V  ��  @�V�@�VA@ V ��  @ V  ��  @�V�@�VA@ V ��  @ V  ��  @�V6U����784����454����014����"%4���@%4��O��p��  
% ����784 ���@354� � �     � �  ����U ���@U U 
U U U ����U ����U ���@
U NGP+�+++++++++]qr++<�< ??10]qr++++++++++++++++++� 
  ??01Y33����F   $��*� n��+XA  ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V 
���#&4	���@$#&4� 
 	+
" "�@�V�@�V
�@@"V%�E	E`p��  �������U����U���U����U����U����U���@UU���U�j 6�f+�+++++++++]q���<�+++<��< ?�?<�<9933�10]+++++++��2�l �2@	l

	�-�l
 ?+322/?+?+01Y%#"&&5#5373#32L<bl,�����+(��>e�c�l�����M,  ��  Y�  ���+XA ��  @ V 
��  @ V 	��  @ V ��  @ V ��  @�V�@�V�@�V�@ V ��  @�V�@ V ��  @�V�@ V ��  @�V
�@�V�@�V �@�V�@�V

�@�V
�@�V	�@�V
�@�V�@�VU���U����U���@YU	UU/0gh	`������YVPh����	
		  ���@U  ���@U 	�p@	 �@� @  eRP����@P����@�����+�]q�]q�]q���� ?<�?�<�<�.++}ć.++}�9999����ć����10K�SK�QZ�C�@PZX����  ��8888Yrq]++++++++++++++++++++++++++++��1@l   ?3??9/+01Y#3#!!&'3�Xݫ�����F"3��F��DZ��w��  P���> a��+X� ��  @�V
�@�V	�@�V�@�V�@�V�@ V�CTX@4@ P p  UUUU/++++��� ?�?��]2�]210@G	CCSS``�����
jijup���	�
���"_o��@&0 @ P ` p � � � � 	   A
��  @ V ��  @@V$U"  A
��  @ V  ��  @@V $+ @+�@�V@�@�V@�@�V6�@@ V@U@UHUUI�@�V�@�V�@@!V$�?U
UU�@�V�@�V14�+�+++++]q�+++�++++++++]rKS#KQZX� ��8Y�++r�+�++r ?�?�9/9/]�]�10 ]q]qY++++++@
  �/�l�/�l ?+?+9/39/301Y#" 4632&&#"326<�����r鉭��Z����j����
����kl���  \���� 0A��+XA '��  @ V &��  @ V %��  @�V�@�V�@�VA@ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @�V�@�V�@�V�@@(Vccst%'59CILED$F'SY\W(�#���U$���U%���U&���U'���U#����U$����U%����U&����U'���@FU(&$$'%64#D%E/Z V#U%ljkfeyzz}u$s%������$�%����CTX@-!&&	&)&  )21& e  -y�%-'%%���@U-	 ?�?�+9]99]9]9/�/�/�/�@-%$!%$"-@U�� -���@U P`p���@- BU���@BU-	&J	A��  @ V 	��  @ V 	��  @�V	& ))���U)���@U)2!�@�V!�@�V!�@�V!&&���U����U���@UT   1c[+N�]M�+++��+++N�++]M�+++�� ?�+?�+�]+��]+�99999Y10 ]q++++++++++]q+++++++++++ +++�--�3�l-�3�l ?+?+99//01Y7326654&'&$'&&546632&&#"#"$&\�_�}o�SP\;�lQig~��������98�X�z�������n�WBsDEg#a+7�eo�dí���[O33k(;�vu�st�   K��>  ��+X@ U]]	Ueko	e���U���@RUU'���1:1AMAQ\Ramaxx�� P`p��
 �� ���U���@U�A��  @ V ��  @ V ��  @�V@��ܴU���U���U���@	'*4�����%&4����#40���  @�V3�@�V�@�V�@@V$@$*4?O�@�V�@@+V UUUUUU47+N�++++++++]+M�+++�+Nq++�q++++M�+++ ?��]++�?�9/]<�q<99910] ]+++qr@  P p � � 0 p � � � �   �/@l 0
�/�l
�/�l
 ?+?+9_^]/+3/]q01Y#"  32 !326!&'&#"^�,��������
��c���Q8V�|�V��(���� ��h��Ch�   �  &> #o��+XA� ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ���U����U	���@M4%��	�� ��  #	 	##
�%�%�%%%�UU���@UU���@UUUU����U����U�]��@�V�@�V�@@V%�U���@UU���@UU
U���@UU����U�]� 3#�@�V#�@�V#�@@V#%� � �  ? O  ���@U U U U U ����U ���@U 
U U $%�x�!GP++N�+++++++++]qr<M�+++��+++++++++]�+++�++++++++++]�NEeD�qr ?<<<??<M��99910Cy@& +++�] ]+++++++++++++++++++++++++++@


 
�0�l	�0�l ?+22?+????01Y336632632#4&&#"#4&#"��2�jv�~ʞ��#\>p��XdL�:&�N_bX����'�l_:�����xxP����   U��!� ��+X��@�V�@�V�@�V�@�V�@�V�@ V�CTX� ��@U
��@ ���U���U/++�/�/ ?�?�9/���+10@4UUKy������	*
���@
@�@����@  �@_o��A��  @ V ��  @ V ��  @@Vs@!#40 ����U� �5 � 8���8  ��@!#4  @  �����+�]+������+]q+�+++�]< ?��]�?�9/]9/]��.+}� 910�C�@PX�	00��� ��8888Yq]++Y++++++@  
�/�l�/�l�3�l ?+?+9/+9/339/01Y732654&#"'!!632 #"&U��l����W�(�����O���t�������Ģ��O?��v\���Ǒ��  U���  ���+X�CTX@
	���U	���@U	 U U U /+++�/++� ?�?�10�CTX@
	����U	���U	���@U	 U U U /+++�/+++� ?�?�10@N����	ELJCT\\Rkkclk`ywvz��������A��  @ V ��  @ V ��  @@Vs	@!#40	 			A
��  @ V 	��  @�V	��@�V�@�V�@�Vs ���@!#4  @  �@�V �@�V �@�V �ǋ+�+++]+�+++�++]q+�+++ ?�?�10]q ]�C�@PX� ��� ��� �� �� �� 88888888YYY��/�l�/�l ?+?+01Y632#"'&326&#"UkӠv�tBjӡ�y���||��~|J]�=�_�������í�������hj�i�  U���  *Z��+X�CTX� %����U����U���@(UUU,+(O P���@U" ?�?��+]29/]�299/++/+++�����10�CTX� %���U���@*UU,+(O P" ?�?��]29/]�299/+/++�����10@G:L@#[W#flmg#z}������� � =��:)d(O_"�P  �h�A'��  @ V ��  @ V ��  @ V 9 ��  @ V ��  @ V ��  @ V 8@@!#40 �,�8� �%�@�V%�@�V%�@�V%s���@!#4 @�+ǋ+�]+�+++���]q+�+++�+++ ?��]�?�9/]�10�C�@PX� '�� #��!  8888Y ]q]YY�(�/�l�/�l"�/�l ?+?+9/+29/01Y732>54'#"54 32#"&4&#"326p�|aS}P66�m��Ə�{z��˥tx��|}�SznL�pVk�������������4��Ĝ���   ���"� ;��+X@
&XX����@44;FJv�� ���	A��  @ V ��  @ V ��  @�V&���U���@UU���@U]  P`p��@�V�@�V
�@�V& 

���@
4
 U
����U
����U
���@U
U
����U
���@
U
];Y+N�++++++++]�+++M]]q�++++M�+++ ?�?<10]+ ]��3�l	  ???+01Y3#"$53326`�d������p�G�}ֶ���������O����b�   �  Z�  N��+X@ C A��  @ V ��  @ V ��  @@V& 	@U	 U	
U	U	���@U	�@�V
�@�V�@@V     U ����U ����U ����U ����U ���@
U ];\+�++++++]<�+++<�+++++]�+++ ?<�<?<�<10Cy@6


!!!
! ++++****�]� �3�l �3�l ?+?+01Y3!2#%!2676654&'&#!���Z~YtsNz�ͅ��9��1EM�lN����Lb��ħ���a2�61E���*    ��9�  d��+X� �޲9���@ 9���v     
� ����  �z+<��� ?<?<�.+]}�10]++� 	 ??01Y3���X��  �  ��  .��+X@ekKK[[  A��  @ V ��  @ V ��  @�V&���  @@V
UU���@U  �@�V�@�V
�@@V     U ����U ����U ���@U U ����U ���@
U ];\+�+++++++]<�+++<Nq]�++++M�+++ ??<�<9/<�<10] ]��3�l �3�l ?+?9/+01Y3!2!!!2654&'&#!�)�Ml�Y�����{��]L1����e�m������\�   �  ��  ���+X@ 
	 ���@4TJ 
 
	�@�V	�@�V	
�@@V	     U ����U ����U ����U ����		U ����U ���@
U ];[+N�+++++++]<M�+++<N�]M��+ ?<�<?<�<9/<�<10��3�l 	�3�l �3�l ?+?+9/+01Y3!!!!!�$��+������?���     �� ^��+X@	/0@p���(�����@4
+ 
���@�V@�@�V�@�V�@@V% � ����184 ���@+4� @U@U U (U "U ,U ���@U U ���U ���U ����U ��� ! �
 ++�+++++++++++]++<�<<�+++�+�] ??<<<�<?�9910Cy@		 ++*��+q] r� 
�-�l
�2�l
 ?+?+32?01Y3#535476632&#"3#����vL\82RD����qk4FW�
F`b��f   (  �& +X��@ V ��  @@V��24���@	4>!4���@J!4)(	/99
IFFI	O\TTZ	Plccj	{t{	���	��&)+	9������4,9	���@#9:	


%a+
a ���@	U+
���[   ��@U"� @`�����@$Ut 
~� O o �  U t!|�++N�+]q<M��+]q<�+�<<� ?�+<�?<��99�.+�}��+10+++q] ++++C\X�)&���@	424��·!4>!4 ++++qY]C\X� �޲9	��޲9	���9	=	���9	���@
999++++++++Y ++�
 �0�l 
�/�l ?+3?+2201Y35#!5!63!(�sX�Od��oyj��w�^{	�  ����  ��+X@{$5E?�"3Bp�:<<LL]]X]^jlhnn���������� //0?@LPf��� 
A��  @ V ��  @ V ��  @@"V$�@`�@UUU����U���U����U���U���@Ut�@�V�@�V3 �@�V �@@V U U 3�@�V�@@V%�����?O����U���@UUUUU����U���@UUUG7+N�++++++++++]qr<M�++�++++�++�++++++++]q�+++ ?�??�?9910 ]]qr q�
�/�l�/�l  ??+9?+2?01Y!#3632 #"'32654&#"-��r�b�q@��k4U�v��uv�����O��s���֝��U������  �  <�  
��+X�
�@�V
�@�V
�@�V
A@ V ��  @ V  ��  @ V ��  @ V ��  @�V�@�V�@�V�@�VA@ V ��  @ V  ��  @ V ��  @ V ��  @�V�@�V�@�V�@�VA@ V ��  @ V  ��  @ V ��  @ V ��  @@7V	6UO	�	�	�	�	�	�	 		p	�	�	�	�	�	�	�	
	 	���  @@*V~ 
% �������  ������U���@UU
UU���U����U���@
UNGP+�++++++++]qr<�< ??<?�+999910]rq+++++++++++++++++++++++++�
 @  ?�??01Y533��������&��  F����  ��+X@|
%4D55WT
RSgde	c`�����������+<<Kp�.$.:5KEFIW
Vg����  
A
��  @ V ��  @�V3 ���  @�V %A��  @ V ��  @ V ��  @@$V%�@`�@U@UU���@UUU���@UU���U����U���  @�Vt�@�V�@�V�@�V$�@�V�@@;V����?OUUUUUU4P+N�++++++]q++M�+++�+++++++++++]q<�+++�+<�++ ?�?<?�?<9910 ]q] q��/@
l 
�/�l  ??+?39?+01Y!5#"&&54632332654&#"8e��ujԃ`�/�� �uv��{x��������QA�F�������   �  �&   N��+X@  	<<
</ ?    ���+�]q� ??��999910� @ /�?�01Y5353����Y������  �  �� ɰ�+X� ���4���@U%5E����@4 
A��  @ V ��  @ V ��  @@'V%	@364�	�	@U@U	(U	U	���@U	U	U	���@U	U	���@U	
U	����U	N���@464��p����@�V�@�V�@�V% ���@364�     � �  ����U ���@U U U U ���@U U U NGP+�++++++++]q+<�+++<]q+�++++++++++++]q+�+++ ?<?�?99910Cy@% +++� +]++�
 
�0�l  ??+9??01Y33632#4&#"��~�v�K�ukP�<���]���_��{S�}��  <  � '��+X�CTX@	U����U���@	U���@UUUU��@
  9/��9/� /�++++?�+++�210�CTX@	U���@	U���@UU���
���U���@U  9/��9/++� /�++?�++�210@G;;�����IYTkdzz�������
����O�� ���
A��  @ V 
��  @ V 
��  @@V
s�  @!#4��   8@�?_o�$ ���+�]���+<��+++ ?<�<?��]�99�.+}�910�C�@PX@	��� �� �� 	�� 88888888Y ]]rYY@	�3�l�/�l ?+?+939/01Y%!&76676654&#"'6632�7%��神{�������H�¢\��A<c�~��fk������X����a1    � 
 ��+X� ��  @�V�@�V�@�V�@�V	�@�V
�@�V�@�V�@�V	�@�V
�@�V�@�V�@�V�@�V�@�V�@�V�@�V�@�V�@�V	�@�V
�@@7VXh���LL� 
 � ��  �@
   �
�f�
@4
���U
���U
���U
�7@@"#4�!5����@4  ���U���U�����+�++]+�++�++++<��< ??�<�<9999�.+}�10C\X� �޲9���@39"-9<++++Y] ]C\X@@9�P9@&9"9@-9+++++Y+++++++++++++++++++ +�	�2�l  ??9/+332901Y!!533#������ƴ�5_���J�����k  0  �� ��+X��@�V�@�V�@�VA@ V ��  @ V  ��  @�V�@�VA@ V ��  @ V  ��  @@V 	�s� �� /��   ���@U U ���U ���U ����U ����U �s���+�++++++]<�]<��]�<< ??<�<10++++++++++� �3�l ?+2?01Y!!5!!�������   ��i!>  հ�+X@t-=K? �  )#22Bp � ::JJY[\\jkimk� ������� � #++5:FJZ��� A��  @ V ��  @ V ��  @@V$�

@
`
�
 @U @U
���@U
U
����U
���U
����U
���@U
t33�@�V�@�V�@@V%  �����?O���@UUUUU����U���@UUUG7+N�+++++++++]qr<M�+++���++++++++]q�+++ ??�??�9910 ]]qr q� �/�l�-�l ?+2??+9?01Y36632#"&'32654&#"��:�h��ju�{Z�.�vx��ts��i��QQ�������L:����������    �& 
c��+X� ��  @�VA@ V  ��  @ V ��  @�VA@ V  ��  @ V ��  @�V�@ V�CTX@ 

 	$U/+����33 ???910�5 "9
���@9	44���4���4
���@	!4 (!4
���@	"%4 "%4
���@~(.4  (.4) (	&
9 5
H G
VVYX	ffii	x wwyx	w
������	� �	�
� �
� ��
� �
� �
� �
� �
,
 
 
( &
7
O @
	@4@4�CTX@	  
���@U
 U 	���@UU9/�+��+��+�+ /??910@7
%	
		
 %  

 
	
	 /"@@@	�		��@��@	 @"��+���]�]��]9999 ?<<<?<9�.+�}ć.+�}�Y10 ++q]++++++++++++ ]Y++++++++� 
 ???301Y!3673��l��%+��n&��goTv���  �  �� P��+X��@�V�@�V�@�VA@ V ��  @ V  ��  @�V�@�VA@ V ��  @ V  ��  @�V ����8=4����344����-04����()4����#%4����4����4���@*4 ��   � � � / @ P � �   � � ���@U U ���U ���U ���@U  U ��Y+�++++++]C\X�� ]Yqr<�]++++++++< ??10++++++++++�  ??01Y33����F  �  � �  7��+X@< 
<_ o  � �  ���+�]]� ?�10�@  ?�01Y353����   V��� +���+X�CTX@@U ���@+U)#


)))#  U &���U&/+�/+�/�/�/ 9??��9/���9�+2�+210@0E�EWvRljduy����
#���@  � ) 5��� h@	)A��  @ V ��  @ V ��  @@Vs_ o  U �A��  @ V ��  @ V ��  @@Vs&@!#40& &&&����U&�-�8���8  ��@!#4  @  �,����+�]+����+]q+�+++�+]�+++ ?�?���9/��]�9910�C�@PX� ���88Y] ]qY@	 #
�/�l)�/�l)�/�l ?+2/3?+9/+3299/301Y732654&#"732654&#"'6632 #"&V��k��}3Ls��ji��!�x�kfd������������|��x}c��� ��g�d_�.������   M���  *鰅+X�CTX@_(@"
 %���@UUUU/+++�/+���� ?�?�9/]��]10@-kD@DD ZT kddjd tu���� U'���U#���@U! U(@P�_  �h@	"�8� �%A��  @ V %��  @ V %��  @@V%s@!#40 ���U�,
�8��@�V�@�V�@ V 9@?_o�@�V�@@VUU�$�+ǋ+�++++]�+++��+]q+�+++�� ?�?��]�9/]�10�C�@PX� ��' # !���8888Y++++] ]Y�
(�/�l"�/�l�/�l ?+?+9/+29/01Y&'&#"6632#" 763232654&#"��,IkVAUbA�g��wЄ��䝉���7O�Nr��{z�Sj0M0>��c`��Ҋ�~K|������]�Y�����  �  �� 
��+X�
�@�V �@�V
�@�V �@�V
�@�V �@@!V@4k���	 	�
 ���@
!#40    ���U ���@U U U ���@U U U @4���@!#40 @�<� +N�]q++�+++++++]q+<M�< ??9910] ]+++++++@	@		 ??9/�901Y!#56673��A�T��/t{>|�G�_  �  � 	��+X��@ V ��  @�V���@
4U���U���@#BUBU 		A��  @ V ��  @ V ��  @�V ���U���@UU���@U]  P`p�	�@�V	
�@�V	  ���@4    U ����U ����U ���@U U ����U ���@
U ]
;Y+�+++++++]+<�++<]q�++++<�+++< ?<?<9999�.+�}ıCTX� ��4 4 ++Y++10+++C\X�@F9����F9@29����29"9��޶9"29��޶29"#9���@#999����99����99����9+++++++++++++ ++++Y ++@   ????9901Y333#����������F���    v� ���+X� ��  @�VA@ V ��  @ V ��  @�VA@ V ��  @ V ��  @�V�@�V
�@�V�@�V�@�V�@�VA@ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @@3V) &)&9 696I GIGX WXW��BUBU�CTX@3+44DDKTT[ddktt{   ?????9]99@
	��<�  ��<� ��<@Z	     		 	 		 A	Q   Q Q @ Q�  ����+N�]M����NEeD� ?<<<?<<<<<999999999�M.+�}ć.+�}ć.+�}ć.+�}�+++��ć<ć�ć�ć�ć��K�SK�QZ�C�@PZX�
���88YK�%SK�*QZ�C�@PZX�  ��8Y K�SK�QZ�C�@PZX�@@88YY++10r] ++++++++++++++++++@  ?3???3?301Y!3673673#&'��{��$8
��O#-���n���'����?���$�������F]� eG��  ���� � 
 d��+X�
 ��P@&<
< 
< 8:O _ o  �  ���+�]���<< ?�<<���910�@  ?�/�01Y353'667��PW296��q�&Ma[  �  �� 	 Ӱ�+X@"�  �  	�@�V	�@�V	
�@@V	     U ����U ����U ���@U U ����U ���@
U ]
;\+N�+++++++]<M�+++<N�]M� ??<�<9/]<�<10��3�l �3�l ?+?9/+01Y3!!!!������P���:��f  �  *�  ���+X@  ����@�V�@�V
�@@V     U ����U ����U ����U ����U ���@
U ];\+�++++++]<�+++<�] ?<�<?10� �3�l  ??+01Y33!������   A�jm  =��+X@ppMM# p  p�+N�]� /M�10 q]� @ /�01Y5!A)���  a  �  ���+X@�	 ��@0	s@!#4O_os	� O__?_o����+N�]q<M��N�q+<M� ??<�<99910q]�	 �3�l ?+3?01Y5! #67a����K6�����������ۭ�ǜ  �  ��   *ް�+X� ��@)UF#V#f#s	�	iup	s��'	'*	A��  @ V 	��  @ V 	��  @@V		**))  A��  @ V ��  @ V ��  @@
V&U���@%UUUUUUT%A��  @ V %��  @ V %��  @@V%&U
U���@U,�@�V�@�V
�@@V     U ����U ����U ����U ����U ���@
U ]+;\+�++++++]<�+++<N�+++M�+++�+++++++�+++ ?<�<?<�<9/<�<9/+++99910] ]+�	*�3�l �3�l �3�l ?+?+9/+901Y3!2#!276654&&#!!27>54&&#!�&��sfg��W�����=�8JKF����m^&CZ:T�����Y�e^�3'��g�`1RfMIo)��8kFRy1  S���  # 0ư�+X�CTX� .���@U..!(	U	����U	+���U���U���U���U���U���@U$UUU/+++�/+++�/+++�/++� ?�?�9/+�9910�CTX�	U	����U	+���U���U���U���@"U$UU ..!( ?�?�9/�99/++�/++�/++�/++�10@M5)II&��0	0} }|tqruz� ���������  .�..!(A��  @ V ��  @ V ��  @�Vs�		Ag +��  @ V +��  @ V +��  @@V+s@ #40 ���2�@�V�@�V�@�Vs��g�$�@�V$�@�V$�@�V$s���@!#4 @�1ǋ+�]+�+++�]�+++�]q+�+++�]�+++ ?�?�9]/�999910�C�@PX� "�� ���  /���- &���) 88888888Y]rq qYY� .�/�l(�/�l!�/�l ?+?+9/+9901Y&&54632 #" 54632654&#"32654&#"jpl���km���������b�kh��fg�:I�S�����)�j��ߠf�),Ĉ�� ���Th��_c����M�O�����   B�Q�>  *)��+X@`,%LE	,&,#96JFVXh�
�.#,'>#>'L'�,�,6!6)?,FF!E)T!T)ic!c)`,�,�'�!�#�'���(��@  0 ` p � � �  �}@
E"
3%3
A��  @ V 
��  @ V 
��  @@$V
%�@`�,@U,@UU���@UUU���@UU���U����UA
��  @ V ��  @@Vt% "�@�V�@�V�@@V$����?O�@�V�@@.V UU"UUUU+,t!4P++N�++++++++]qM�+++���++++++++++++]q<�+++��< ?��?��]�?��?<10]q ]q@
    �/�l
"�/�l
(�/�l ?+2??+9?+9/_^]01Y32676'#"5463253#"&32654&#"f�2Ct}�v���nэ�z�e۠�Ꙧ}|��zx�XQ%2dZ7��<ݘ����j��x�*�������     F� `��+X��@�VA@ V ��  @ V  ��  @�V�@�VA@ V ��  @ V  ��  @�VA@ V ��  @ V ��  @ V 	��  @�V�@�V�@�VA@ V ��  @ V  ��  @�V	:;	���4���@444	��س!4���@;!4(!4&)*
/hhh�			
U	 


	���@U  �@	

	 �@		R@
�

��@  RO���@	 U ���@U U ���U ���!`�++�++++<�]��<�]�� ??<<<�<99�.++}��.++}ć�ć��K�SK�QZ�C�@PZX�	��� ��8888Y10 ]]C\X@		"9"9��ޱ9+++Y++++++++++++++++++++++++++��2@
l 	 ???9/+301Y!3673;���!PEB^���mM�F||s������     �& �  ��  @�V�@ V ��  @�V�@�V�@�V�@�VA@ V ��  @ V  ��  @�V�@�VA@ V 	��  @ V ��  @�VA@ V ��  @ V ��  @�V�@ V ��  @�V�@�V�@�VA@ V 	��  @ V ��  @�VA@ V ��  @ V ��  @�VA@ V 
��  @ V ��  @�V"A@ V 
��  @ V ��  @�V �@�V"A@ V 
��  @ V ��  @ V�CTX� ��@UU U
��ԴU���@U U
����U���@/U@U
 
 
U

U����U/++�����+� ?????910 +++++++++@*)
J[� U
���U���U���@	!4'4	���@�$4		 	 $ %*+4 5:;DG@MKCGJ[Rkdgyzt�����	(( ('('/8 7w�������� �����	�����	UUUUU�CTX@
 %%%  %���@7U%*U
&
+TR
\l|�

 
 
 ?????9]99/+�/+�9���999@	


��K�  ��I@f
 � +
%+


 %   

 
�`p���@
 O
o


�U@	Oo�U@`p������f+N�M�]]�]q�]q�]]� ?<<<?<<<<<999999999�M.+�}ć.+�}ć.+�}ć.+�}�+++��<<�ć�K�S�C�@PZX�  ��� �� �д 0 ���88888888YK�4S�C�@PZX� �б088YK�!SK�3QZ�C�@PZX� �� 88YK�SK�QZ�C�@PZX� �ж   ��в0��� 8��� ��8888888888YK�SK�QZ�C�@PZX� ��
   888YY10C\X� �Զ9 ,9 ��Ա9+++Y+++++]qr+++ +++q]]Y ++++++++++++++++++++++++++++++++++++!367373#'K����?3���5=������)�&����n����f��|���     �& +��+X� ��  @�V�@ V 	��  @�V�@ V�CTX@	
 
U/+ ????910�"9���@P9Z��������	@9	5:��/WYYX��
��������	���
�CTX@ U���@U  

 ?<?<99++99@f			 	

� �	% 	  	�%
		 
OI~"
a	~@
��@P��C@ ~"O  I|�+�]���]������] ?<<<?<<<�.+]�}ć.+]}� 99�ć�ć���<<<Y10C\X�9���@9"9"9��޲!9���@
9"!9	@9++++++++Y]q +]++]Y++++@ 
 
	 ????9901Y336773#'����.,%�������:��(��G0B3����JY�]   w����    ' 38��+X@
��h��@1+�� 	e �@%(�� e .��%�� +  1��"�5��   �@	   u4WZ+�]������� ?���<<?<<���9999�.+}�10Cy@R3)+ 3 1-&+ /$1 
 *(2!(,'. 0#.    ++++++++++++++++�]�(�e�%	�e@.% ?3??33/�2�201Y4632#"&"32654&34632#"&"32654&w��������9CYZBDYZB"���垗������:DYZBEYZZ��ſ����t��st��s�s	�����ſ����t��tt��s   I�-A * 1 82��+X@%|0,66/F!U!P/]6jc/zw!s/{6�!�/�61��޷9  $4,���@, #4j8*7 *0! 710! 7!00�770!72���P��� ���+�5@
� *�7�
2�5�)��8 ��5s&���@
90&@&�&&�R@*  8822))*��@ ++11

0 @ � �  �@	.so�� 8@?O�9ǋ+N�]M��q��]<<<<<<�<<<<<<<�]+��� ?��<�<?<�<�����]�9�.+�}�10Cy@J!7$%#%"%&7!5O3(5O,.O 0.O 6%8O! 784'2O 32-+O,+/1O 01 <<+<<+<+<<+++++*+*��++ +]]@ 81@+  )2�/�l)
�/@	l�/�l+�/�l ?+33/+2/3/?+2/3?+3/9/�3201Y5.'7&'&&5476753&&'6654&'���{
�5LjotV]�[�j�\v�eX�,Tj9�jiyg{ji�a�ӴW"�D`=A0�l�wPVVMb�jq��"%j�U��	�(�]\|%��sbw/   |�Q`�  N��+X@
' �3� ��3@�^  ���+�]����� ?<?<10]�  ??01Y&47673ߕ�MZ��y'=#++�Q�������Y������    |�Q`�  v��+X@((	
 	�3�
��3� �^���U����U���U���@

U���+�]++++����� ?<?<10]�	 ??01Y# 4'&'&'3��++"='z��ZM��Q�Ἱ��Z��������   �  �� ��+X�A@ V 	��  @ V ��  @ V ��  @�V�@�V�@�V�@@VUVZ	��	U����U
����U	����U���@UUw
 !4���'4	���'4���!4	���@�'47	G%-
X
wu
���#&%98	?OYYXY	}y�	�������

		

	%%


	  
�@	U"�@ ?U��@�V�@�V�@�V% �@�V�@�V�@@V%� ? O  ���@1U U U 
U U U U �!Gf++N�+++++++]q<M�+++�+++Nq�+]M��+� ?<<<?<?<9�.+}ć.+}�<<<<�CTX@K		�	4 +]qY10C\X@
	,9	<��޲9��Բ 9��Ա!9+++++Y] q]q ++C\X� ���!9����9��޲9��޲9��޲9��ޱ9++++++Y+++C\X@�9	<	<����9���9+++++]Y ]+++++]q++++++ ++@
	 
 
  ????901Y333#�����j���������v�dz�[  �  ��  "��+X@!6Zfm	UUU$����U����U����U����U���4���"'4���'4���'4���'4��س&4���4���4���@I4%JJ S\mr	xy�
������ 	!
		���  @ V ��@U !" A��  @ V ��  @ V ��  @�V&����U����U���@UU] $p$�$$"�@�V�@�V
�@@V     U ����U ����U ���@U U ����U ���@
U ]#;�+N�+++++++]<M�+++<]�++++��+++ ?<<<?<�<9/++�<<9/99�.+}�10]+++++++++++++ +++]C\X@
@9::+++YqC\X� ��@9"9"9@9"9"9"9+++++++Y�	�2@l  "�2�l ?+??9/+901Y3!2#.'&##!26654&#!����z��M(UL���UnW-!K����N���0�O�y��%$Nu�q1��8�u37yGh�  X����  (��+X@�_&�&7##*-+&;<:&LLI&]U#X&o{z��� �� �� �� ��+ *;]��&�&%*&49&IIEE#K&VXUZZVW W"ifk&{&��&��&��Բ9 ���@09*:((& !(& $$	A��  @ V ��  @ V ��  @@
V&U���U���U���U����U���@UJ *�**!�@�V!�@�V!
�@@
V!& �@@VUU)c\+N�+++]M�+++N]�M�++++++�+++ ?�??�9999 3��]10++]] rq]]qr@  &&$($@$�2�l	�2�l ?+?+3/�9/�939301Y%&'#"$54$32%64&#"  327&'��r9���������E��F�n��m�y�����h\[e�]+�9{[�\��d����ڵ�ߍ/]�9�
���������';   	  I� X��+XA ��  @ V ��  @�V�@ V ��  @�V�@ V ��  @�V�@�V�@ V ��  @�V�@ V 	��  @�V�@@*V&))8788	8:57
 !4 !4���!4���!4	���!4���@l!4 !4 !4ww&)(*&6:::5HT]\ZTgejkieuzyzww���
�������������,���@UUU����U�CTX@ 
U���@
U  
 ?<?<99++99@]		 	
	
  	  	 
		 / @�_� 
�
�

���_���@
�@P��_@
  �!`�++N�M�]��]�]�]NEeD�] ?<<<?<<<�M.+�}ć.+�}� 9999�<<ć<<ć<<ć���Y++ ++10] ]++++++++C\X� ��@9"99��޲9��޲9���9"9	����9���@9@9@9<=	<=���@.9"9!= !<
!=!<= <
=<+++++++++++++++++++++++++Yq]q+++++++++++ +� 	 ????01Y33673#&'	7��
S#1C'���+���!1������u?PW��M��-5P�  c����  T��+X@K��� @OO@XX	WU_Z_VW��	A��  @ V ��  @ V ��  @�V& ���  @ V ��U���U���U���U����U���@U��@�V�@�V
�@@
V&   �@�V �@@V U U c\+N�++++]M�+++N]�+++++++]M�+++ ?�?�10]q ]]]q��2�l	�2�l ?+?+01Y !2#"$7 32 4&#" c�6�F������������y�����m����������Z�����4����  m���� %���+X@`'^$$ !% ���@U!	&'%$A��  @ V $��  @ V $��  @@V$   '`���U���U��ڴU���@Ur�''�@�V�@�V
�@@
V& 

�@@V
U
&c[+N�++]M�+++M]�++++]<M�+++<9/ ?�?�9/+<�<999910Cy@D#&%&&%&#%! ! ! "%!!!	!! $!!  ++++++<<+++++++++*�] ]�@$$! �3�l!�2�l	�2�l ?+2/3?+9/+9/�01Y5%#"$54$32.#"3267Lm��Р�����P۟�&�!b�o��w!8��~�>?���rs�^��s�g��0p�MQ�O������a7�� D��'�&    E �   @�� H+�" ) ++]5   H�i�>  ���+X@l+*;Ky??K��44?DDSScc`������)"+95IFZi������ 3 A��  @ V  ��  @ V  ��  @@$V %�@`�@U@UU���@UUU���@UU���U���@
Ut�@�V�@�V�@@V$����?O�@�V�@@(V$UU"UUUt!4P++N�+++++++]qM�+++�++++++++++]q<�+++�< ??�??�9910 ]]q q� �/�l�-�l ?+2??+9?01Y#" 466325332654&#",*�U���o�~�q��!�xs��vu��i;N.������C��������   ��O�  v��+X� �ȳ4����4���@&4��o o oOP  ��`���S� ٧+N�M��� ?�]<10]]]]+++� � /�01Y3ޅ�����       l    �  	  4  �  V  �  �  �  �  (  �  !�  $h  (>  *�  .�  1  3f  6F  7�  9~  9�  ;�  <�  >B  @h  B�  E  Gz  G�  I�  L�  N�  P  RJ  T�  VH  V�  Y  [~  \�  ^�  b@  b�  c�  d�  d�  e�  h
  kd  n  n  p�  v�  yX  {2  ~  ~�  `  ��  ��  �&  ��  ��  ��  ��  �
  ��
endstream
endobj
10 0 obj
<<
/Encoding /Identity-H 
/ToUnicode 20 0 R  
/Name /F-0 
/DescendantFonts [21 0 R ] 
/Subtype /Type0 
/Type /Font 
/BaseFont /SUBSET+ArialMT 
>>
endobj
11 0 obj
<<
/Encoding /WinAnsiEncoding 
/Type /Font 
/Subtype /Type1 
/BaseFont /Helvetica 
/Name /Helv 
>>
endobj
24 0 obj
<<
/Length 488 
/Filter /FlateDecode 
>>
stream
x�]�M��0���
��U��v%���"q�J�Bbh��D&��~_o��@����<���f��w�h�o��a4��kb���Xs�33+�i�1c�՗j0�G��~�eߝz3[.M�}Z���n��M�L�56!���<��&>܆�w��n4s�Z�&��>W×�L�����?k?�C0�?,z��&\�����az�|�Vf��������?�d��T�����ڄN�����%:�+�'\�����EBɥ^� K|Ep�]��'�q����-rs�wqd�����%d�(��u,e�!�Wؕ������������U�l�"|��_�
�ͥ�[���u���,�ee��p�B_�H���*|���m|wR8_��W�9_ύ����h$�}#�W2��SP�+T�
wC9_��|�9n�����RP�+4R�*_B���R�/wC��r������}��j������9�q6Է�s#G�Tx�m>���R� �.�
endstream
endobj
25 0 obj
<<
/DW 500 
/FontDescriptor 26 0 R  
/CIDSystemInfo <<
/Registry (Adobe) /Ordering (UCS) /Supplement 0 >>
 
/W [0 [0 722 610 889 277 556 610 277 722 556 610 333 666 556 389 556 666 556 556 722 277 556 556 277 610 556 556 556 556 610 277 277 610 610 333 777 833 722 722 666 610 277 722 610 556 556 583 943 333 333 610 333 556 556 277 556 556 556 777 777 722]] 
/Name /F-1 
/BaseFont /SUBSET+ArialBoldMT 
/Subtype /CIDFontType2 
/Type /Font 
/CIDToGIDMap /Identity 
>>
endobj
26 0 obj
<<
/ItalicAngle 0 
/FontName /SUBSET+ArialBoldMT 
/Type /FontDescriptor 
/Descent -211 
/FontBBox [-627 -376 2000 1055] 
/FontFile2 27 0 R  
/StemV 0 
/Flags 32 
/Ascent 905 
/MissingWidth 1000 
/CapHeight 715 
>>
endobj
27 0 obj
<<
/Length 26620 
/Length1 26620 
>>
stream
    	 0  `loca'    g   �fpgm�� ,    >maxp
�    �    head�     �   6cvt ��   @  `prep\[ =    �glyf:�3  !�  Edhhea�     �   $hmtx,    �   �      �ʮ_<�     ��<    ք����� r  	         >�N C ���z                 =  � a� R ~9 �s 0� �9���  s U� �� V Js I �s V �s As � �9 �s Fs V9 �� ,s �s Ws Ss A� T9��9 �� T� �� s9 Y� �� �� �V �� �9  � �� �s #s �� U� � k� C� �� s 3s &9 us Ms Ws [9 b9 Y� �    =� < �    / V  K�  A T���5  �� < ���A� ��  �  � ��  @��2@���2@���+2�����:3@���-�2��� _ 3����U3@���@D2@���3;2@���/12@���3@���2A� /�  � /� O� �� �� ��  � �� �� ���F@���3A�  @� �� ��   � �� �� �� ����	2@���3A�  � � �� �� ��  o� �� ��  �� �� ���A
� � �  ����2@���2@A� P�  �M �M  o� � ��K�-12���K�
2A�  � ��  ��   � @� ����2@���2���{�042���{�2PAx en # ~n  cn  bd  ��@�2�A? ? ) A 2 D  ��u�2���u�(*2A
C 2  4 �2 �@  @��	2@���2��  ���
 /
 ��T�	2�AT �T  n  �n  @n�	2AE  k  F  �� F ��&���  @��	2@�>�3@�>�2�A	>  �� �� ����&82 A&( 0(    0  � 0� P� o� � ��   � 0�  /z pw �w �z ���2����$(2��2� ���	2@��2����2?�s Os  @t�2o�*  @,�2@�p�	2� 2 ���2�  ��A   ��  ��  ��  ��  ��  ��  ��г	2@�ҳ	2�A�  _� �� �� 0 �� 2 �� ? �� d �� 3 ��!����!�@���2���ò+/2���ò%2���ò2���ò2A%��  �� $ �� " ��  �t � �5 ; �5 ; ��  �� 8 �������������� ����P/���  ��&���&$�5 �t�A
�X� � ��  ��7����� ���@7@%@-@�0%0-0� % - 7 � A�  �� �� 7  � 0� @� ���7�A�t �t  �t �t  `t pt   t t  �t �t  ?� O�  �~ � �� ��  �z �{ �| �}  �t �u �w  p~ p p� p�  pz p{ p| p}  pt pu pw  `~ ` `� `�  `z `{ `| `}  `t `u `w  P~ P P� P�  Pz P{ P| P}  Pt Pu Pw  @~ @ @� @�  @z @{ @| @}  @t @u @w  0~ 0 0� 0�  0z 0{ 0| 0}  0t 0u 0w   ~    �  �   z  {  |  }   t  u  w  ~  � �  z { | }  t u w  �~ � �� ��  �z �{ �| �}  �t �u �w��A�~ � �� ��  �z �{ �| �}  �t �u �w  0t @t  �~ � �� ��  �z �{ �| �}  �t �u �w  �~ � �� ��  �z �{ �| �}  �t �u �w  �~ � �� ��  �z �{ �| �}  �t �u �w  �~ � �� ��  �z �{ �| �}  �t �u �w   ~    �  �   z  {  |  }   t  u  w �X �)  � ~ � } � | � { � z 7 w & u   t �7A5 O5 _5 o5 �5 �5 �5  �5 �5 �5 �5@"O�����O����� A  _5  �5  5 �5  /5 ?5  ?4 O4 5544@� �*�*�*�*�*A	G    7 X@&>�&>7&'>�����&6���&6�)@+&6�&6�&6�&6�&67&62&6-&6%&6&67&*�X@"&>�&>�&>'&>!&> &>7    @���� 	���'(���'0���'O���'bA	� ' �  � ��������������4�]�'.�[�'�AU  T  S  R�V�Q�)�+�'&A* '% )X � %  $���#�;�"�9A '  -   ���X@�������� ���%�V@
�-��A�A
X  �X  �X��%���X%��.�-���)��X�� ��@�0t-�sJaR]%���\�  YX��P%�I�%�G%�@Fy@'9 ��  8X�7-�%  2X%�,4*%��U7�@*��[B;#"
 ���@+                     J �KKSBK��c Kb ��S#�
QZ�#B�K KTB�8+K��R�7+K�P[X��Y�8+��� TX������CX� ��� ��YY v??>9FD>9FD>9FD>9FD>9F`D>9F`D++++++++++++++++++++++��KSX��Y�2KSX��YK��S \X�ED�EDYX�pERX�pDYYK��S \X�  ED� 'EDYX�B  ERX�  BDYYK�%S \X� &ED� !EDYX�
 &ERX� &
DYYK�S \X�� ED�  EDYX�%  �ERX� �% DYYK�S \X�X &ED�&&EDYX�# XERX�X# DYYK�)S \X�ED�-EDYX� ERX� DYYK�/S \X�ED�%EDYX�5 ERX� 5DYYK�S \X�ED�EDYX�( ERX� (DYY++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++eB+�1u~�Ee#E`#Ee`#E`��vh��b  �~uEe#E �&`bch �&ae�u#eD�~#D �1�Ee#E �&`bch �&ae��#eD�1#D� �ETX��@eD�1@1E#aDY�?<XAEe#E`#Ee`#E`��vh��b  �X<Ee#E �&`bch �&ae�<#eD�X#D �?AEe#E �&`bch �&ae�A#eD�?#D� AETX�A@eD�?@?E#aDYEiSBKPX� BYC\X� BY�
CX`!YBp>�CX�;!~� � +Y�#B�#B�CX�-A-A�   +Y�#B�#B�CX�~;!��  +Y�#B�#B ++++++++ �CXK�5QK�!SZX�&&E�@aDYY+++++++++++++++++++sssssE�@aD EiDEiDssstssststst++++++++++++ sssssssssssssssssssssstttttttttttttttttttttuuustuuuu+s  K�*SK�6QZX�E�@`DY K�.SK�6QZX�E�@`D�		E���`DY+EiDt sss+EiD++C\X@
  �����t�2o�w w ��w�/12���w�"%2@�t�/52@�t�(*2@�t�!2����72����%2���@-2�%�-�7�%�-�7�����2����/� t+s++++++++t+stY ++C\X�����2�����2++Y+s++++ +++++++++++++++++++++++++st++++++++ss++++++s+s+++t+++sssss+ss+++s++ ++++sts+s++++u++++++++u+++++s++++stu++sss+++s+sstu++stu++stu++++++++++++tu +++EiD+ @BUT@?>=<;:987543210/.-,+*)('&%$#"! 
	 ,E#F` �&`�&#HH-,E#F#a �&a�&#HH-,E#F`� a �F`�&#HH-,E#F#a� ` �&a� a�&#HH-,E#F`�@a �f`�&#HH-,E#F#a�@` �&a�@a�&#HH-, < <-, E# ��D# �ZQX# ��D#Y ��QX# �MD#Y ��QX# �D#Y!!-,  EhD �` E�Fvh�E`D-,�
C#Ce
-, �
C#C-, �#p�>�#p�E:� -,E�#DE�#D-, E�%Ead�PQXED!!Y-,�Cc#b� #B�+-, E� C`D-,�C�Ce
-, i�@a� � �,���� b`+d#da\X�aY-,E�+�#D�z�-,E�+�#D-,�CX�E�+�#D�z��Ei �#D��� ��QX�+�#D�z�!�z�YY-,-,�%F`�F�@a�H-,KS \X��YX��Y-, �%E�#DE�#DEe#E �%`j �	#B#h�j`a ��� Ry!�@��� E �TX#!�?#YaD� �Ry�@ E �TX#!�?#YaD-,�C#C-,�C#C-,�C#C-,�C#Ce-,�C#Ce-,�C#Ce-,KRXED!!Y-, �%#I�@`� c � RX#�%8#�%e8 �c8!!!!!Y-,K�dQXEi�	C`�:!!!Y-,�%# �� �`#��-,�%# �� �a#��-,�%� ��-, �` < <-, �a < <-,�++�**-, �C�C-,>�**-,5-,v�6#p �6E � PX�aY:/-,!!d#d��@ b-,!��QXd#d��  b� @/+Y�`-,!��QXd#d��Ub� �/+Y�`-,d#d��@ b`#!-,�    �&�&�&�&Eh:�-,�    �&�&�&�&Ehe:�-,KS#KQZX E�`D!!Y-,KTX E�`D!!Y-,KS#KQZX8!!Y-,KTX8!!Y-,�CXY-,�CXY-,KT�C\ZX8!!Y-,�C\X�%�%d#dad�QX�%�% F�`H F�`HY
!!!!Y-,�C\X�%�%d#dad�QX�%�% F���`H F���`HY
!!!!Y-,KS#KQZX�:+!!Y-,KS#KQZX�;+!!Y-,KS#KQZ�C\ZX8!!Y-,�KT�&KTZ��
�C\ZX8!!Y-,F#F`��F# F�`�a���b# #�����pE` � PX�a�����F�Y�`h:-,� B�#�Q�@�SZX�   �TX�C`BY�$�QX�   @�TX�C`B�$�TX� C`B KKRX�C`BY�@  ��TX�C`BY�@  �c� �TX�C`BY�@  c� �TX�C`BY�&�QX�@  c� �TX�@C`BY�@  c� �TX��C`BY�(�QX�@  c� �TX�   C`BYYYYYYY-,�CTXKS#KQZX8!!Y!!!!Y-� � � &   ��  ��  ���i��� �i���             � � �(  ��  �1 I  �  � � �  T � $  U I+ ���v�� = � ������  � � �  � 7 N U U e �� Y��  �  ; R a � � �   � � �|��   � � < A A���� * ���	� � ��c�i  " �+���� & Y � �+�H ! k � �� k � � �]C�   I V n w � � �P���{��   ( a i �5M��>�� [ � ��[�[�?����  �
��2�������  & 1 = N V b � � � � �� H S w � &(�~~� . A ] k u � � � � � � � � � �Jb��d�����  # % * t � � � � � 0Pjo���������&�����N��   L z  � � � � � � � � �8h����	"Op���N��5Bk����a�������������    & F i � � � � � � � � �+8;Z^hs�������   ";DOor~�����������"6q�����&.1OZ�22GS����<dp�����*��� �h������  Y z � � � � � � � � � � � �!'+9FKMW\e����������"+ASae�����������#+1IZ[nqt~���������uz����Lmm������/j��6P���p*               ��     � +�S� ?�h�n    @�  t� 5�   � ����= �`�n�! �& ���B �<V� �� � k x �ks ��:}7 �S� <��	I� n �d ^                              9 � ���|+ � � Y � �� ���   U a  � � � (  ] � &l� �  7>z � � ��&B  ���i���7�-   � t h G � � � � � h G \ H 
 ( 2 A P Z d } � ��������y�o �  �,�� � � \ < � � � �� � G                                                      �d � �%2��v�����1 x � � � � �
 c � � �B  , 4 A 8 H X lY� C p � ( 7 B P Z d s x � � � � � � �\ � �,c � A K U _ s �	�� A d  * � �8t , @ � � � � � � � � �
 ,;DVc � W d6 P�  �� 9 N D� � $ B"� � ` �   9� ,�N�8i� �  � T  =q A  P � O 5�R , ��� � � �e��w�l � � \ @vDr��         B���?@ � 
� ��& 	� +�<�<N�<M�< ?<�<�<�<10!!%!!  � ��@ �  �   a��^�  �@N�	��� ��	���	%	(())uu	�)*%(��	��?OR � �  ����4 ����
4 �Z@-@4K_O@4�(@"-
�V � O0'�0���~S+N�]qM�N]�]M��� ?��+]q�+?��++]q�]10 ]]]]#   ! &&#"326?B�������z4�d2���v��Ƞv�[���Zn��^�Fr�������   R���>   �@H������	YVVY�����	���	���������u���t�
�t@9`p! XA+N�M�Nq�M� ?�?�10 q]]qCX@	iffi]Y ]]4632  #"$&%32654&#"R����4������ �nn��nn�"�������Ä���������   ~  �> ';� )��@]
?4444#DEED# /)S	`)�)�)������)�)�) )/)P)�)�)�))@4?)P)�)�)�)!�t�
!�t@'&'
 &@Z5`o�F@&@Z5o`�F�%&&'�)�  '����	?'���@6
?'@Z5'@A5'@<5'@$'4'@:=4/'�'�'''�' ' '0'�''(�<+N�]qr+++++++<M��<�]q+<�<�q]+<�< ?<?<<<<<?�?�9 910r+q] ]+!6326632!4'&#"!4&&#"!~��f�0F�\u�(��'Q;h.��?6Ah-��&��TUUT_\D��Y_�.<H���F�Z,F����  �  ��   w� 	��@?
?@	P	�	�	�	�	�		`		�	�	  @ � �  ] 
&���@	!$4?<+N�+<M�< ?<?<?<�]q<<<<<10q]r+!!�������J&��  0��> *�@�#'#���'�*	F���!�#��")Ue���"�A#@$D&g"d&���"�$	7&EFJOF!B""$'&75!5"5#5$
	!'"""#$"@,sxyv)u*��*��*�"�#����*�*�,!@!#4@4�3!P%�%%@4%,���@
?P,0,/,,!03! ����	? ����
? ���@		4 +x�+N�+++M��q�N]qr+�+qM��qr++� �CTX@5&"6!F!TYdi�
!"((_F(PF?�]?�]999]q� "�˳(*4!��˳(*4"���$4!���$4"���4!���@4k6"F"��"�"�"!" ����4 3����-?����	
>����"%4���@4 0@P`�� P`����4�@M _�F(@43@-?@	
>@574@+.4@%)4@4_oU@"$4P�F?�]q+�]++++++�+?�]q�+]qr++++�+9]q++++++Y10q] qqqq]]C\X� $��@	?(?!���99!���9"���9 ++++++Y q]%327654'&'$'&54632&&#"#"&0ncm7%I��[~����(��_Xo0 &�YX����/+RU(/ K>V�����1>B#fJK��Ұ  �  Y>  �@Zh�44DD��t@ 
& @ $4� �  ���@"$4��p��
&�)����@ $4��?<+N�qr+<M��<N]qr+�qr+<M�< ?<<<?<?�10 ]q]!!4&&#"!!632Y��$Q9It+����]�O�e8P���&��Ch�{  ����;�  8@ I  
�� �l+N�M�N�M� ?<?<�.+}�103k�����      ��  
A� ��@	794(794���@	(54@(54���@P!'4(!'4) **(
/8 7?j jefhg
�J	
			    	 
@>
���@4
%	��@  �a@ 0��$@		0	�		�$ a@	 ^c+N�]M��]q�]q�NEeD� ?<<<?<M�9/<�++<�.+�}ć.+�}�<<��ıCTX�	4	4 +Y10K�SK�QZX� ���
��� ���88888Yq]++++++!!!!!������y��;9*��M����� ��   U��?>  �@QXYYhii}y�����������88JJFYi:77ww�������	����4����43����4����4� 
t@ @4 @4 3�� t@ @4! /@4!O!XA+N�M�N�]M�+��+ ?��]�++?��++�++10 ]qq]&&#"3267#"  321��cOi}kPf+���������2ST����[o/��&%�   ���S&  �@Wg�	<<KK��t@ 

	& �)@@ $4�����@"$4��p��
&	���@ $4��?<+N�qr+<M�<N]qr+�qr+M�<�< ?<<<?<?�10 ]]!5#"&&5!32665!N:�ik�LR?Hr*�Ub^�����e;Ou����   ����  �@)   #
):JY  	
�@ ��`�����t� �t@	/
/  /_�@(&U?��`����  0x�+N�]qrK�7SK�;QZX� ��8Y<M�<�<�]<�� ?�?<�<�]q�9310]#327#"&&'&5#535%z�''Jb|Lz9	��&��T�+�*3QE1���Ӥ��  J���� ,�@=���(�,+ee(txt(��#Y
UU"Y#hfg!i(g,w��!#���4#���@e4Q"Q#�"�#q"q#�"�#�"�#+
*$"$#94#K
KD"C#je#yz"��"�
��"	
	"#
""#
V@ 4oo��e ��@9- H���@I 40@P`�����@9-*	��@4K'&.'��K�  0  -�S+N�]KSX� @8YM��]�N�M��+r� ?�q+�]+�?�q+�]r+�9]]qr++C\X� "��>#��г>#���9"���9#��ɲ9"���@9 9
 9
 9"���@9 9
9
9+++++++++++++Y�CTX@:
:5"5#K
IC"F#�
�"
 ]Y10 ]q]%32654&'&'&'&54663 &&#"#  J ����=L4��`����}}�I/,8��u�� ��������yQ4I.;Vy�p�f��qc5"94%/fm��~�k   I��.> # 2q@hJHI%��	6FW&fg&�&������')Yw�����4�$21,$@+.4$@"(4$@4o$�$$F���@04= ��,3 @4   U!@?!@?!@4!�t�
,����?,����?,����4,�t@@1&)	(Y��@4O44`  �03)!_�O_o3iA+N�]qrM��q�]N]�+]qrM����< ?�+++?<?�+++�]+�9/]q+�CTX�/qY��CTX� $���4T$d$]+Y]+++9<<<10q] ]q'6632!&'&'#"&546676754&#"3276765e�+�ϼ�K%��H�]��V���LPoKT^6�$7XDLE3�.��Y������L7FF��Z�K% QE;��2'<;V2&7$e  �  7>  �@(�	Sfu/Xhp
	��?O�w@) 

( 		0	p		�_�� &�)@��?� +N�q<M��<N]q�]M� ?<?<?�]qr9210] ]q K�SK�5QZX�
28Y ]!!!6632&#"���CkD`YWG=;R/&�kD5�.A���  �QR& 4�(���@44444���@:4  `��@/(  0`�����"&4���@49@4�'@	@4�'@9 @64  0  Ġ+N�]+M��]+�]+�NEeD�++qrM�� ?�]/?<<<99 9999<10 ++++++]K�SK�:QZX� ��� ��8888YC\X� ��@???���?���?+++++Y!!#"''3267+��#��C%CWPQNB5b^&����]b="�sY   �  ��   w@%��Gg�% % '�����	4��@0`p�   0  ���1S+N�]<M�<Mq�+qM� ?<?<�<9/<�<10 ]q]3! ##326654&'&#��R~�b�Nj����vC^H5��!ݯ��i����`.bAPh
  A��'>  �� ��@F9�	����
�	��HGF
O����
��
���@4@4������?����?��@P`����43 ���� 4 ����")4 ����+-4 ����4 ���@4�     _�t��t@$ !/!O/_o�!@4iA+N�+M�N]�]M��� ?�C\X@@(?@?@?@?++++Y?�C\X� ���(?����?����?����?++++Y�]q+++++C\X�  ���9 ����9 ����	
> ����A!?+ +++Y�+9]C\X@@?@?@?@? ++++Y/<�++r++<310]q ]+# '&5 32 !326&&#"�6���i���@�aBZ'xV\<<R/�����+����}�HlzCCs     Z& @(/4(/4(/4(/4��س/4���@ :4�
	
" -� ���@ 4
  % *4 :� 	�CTX�
���@	4 	 
 ??<9+99@ 

		 
	9���@(40@
?
O

�0@9?O�0 ��@5  @Ġ+N�]+M�]��]NEeD�]+M� ?<?<<<999Y10q+] ]++++++!!6767!��T'�:�!�Z&��E--��   �  b�    , �@?w*hx*��	!	(,!%O0�#"% % 'p�K('�����	4��@!0.@.P.`.p.�.�.�. .0.."   0���-1S+N�]<M�<M]q�+qM��]� ?<�<?<�<9/]qC\X� ���9����9����9+++Y<�<9 910K�SK�QZX�
 8Y] ]!2!3276654&'&#!276654&&#�J���Zo_��]�vJ���(­*LWKJ,Ѫ�+BS@y��\�_g�+'�d�q���	WGDU	���x	]NB\*   �  ��  S� ��@)
?@P�����`��  
& ���@	!$4 ?<+N�+<M�< ?<?<10q]r+3!���F  F�30   ' .@�XgU[fg wuv u-��� �-&&&75-FG-Uvtv-
.!'.-'& (!
" ) ().-
  '&!"wP�V  ���4 ����4 �(����4(����4(�� I�	w�!@(@4@4/?O�
!@4!@4/!?!O!!��Z�
	��"@-��_o?�+@4���/��@w+/++@4+���P0$���@	4$ $$��@���w���@	4 ��@�/@4/�M��+N�+q]M�q+�]q�q+N�qM�+q��qq+9qrrr/<�]< ?<��]++�]++�]�?���++�++�]�99 99999999<<<<<<<<<<10 q]]]%&&546753&'#5&&'%6654&'�ķϬ����a��Ñ��X6;F@A�K^OZ��8㢤�cc��!v*�yAϢ������Pt `:5[�2oKCa   V���    �@Kx
�
���	��	�	VYYVghhg996	6IIE	F�	���	����	� ���@%4�/@4� �O"�!��+N�M�N�qM� ?�+q?�+q10] ]]2#" 76"32676&&2�x��w�����w�3P4O33P4O����_�`��I�����ATm�����@ATl�A  �  �  $@8 
&    0  gv+N�]M� ?M�103!���   ,  ��  r@#/	00P	p	�	�	% 	�-@
 0   �-@Pp����+N�]KQX�@8Y<M�]<�<�]<EeD� ?<?<�<<<10]!!5!!��M��N����>  �  &� 	 V@	k{��)�_�^�	 	 �X  ]@  �
��� +N�]<M�<�< ?<?<�]�910 ]!!56$73&���n0�#�E�$Ɇ   W  �  �� ��@14
:8
HV����
! //?O@4�� ���X�/�`@O ��+N�<�q<M�]� ?<?<��+]q<9]10]+!!7W�w��������u�J��0x�  S���  $ 0�04&���@l4����uv�& *6 ;F Lncghw'�'�������'�,�0��w���'��  .�+	�  %.@4?.O..�� ��@4p��(���@	40(@((��@?"O""@4"��@�	w+�O2�w%�1��+N�M���N�qM��� ?�+]?�]+9/]q+�]+9]9] 9]9]10q] q]++&&54632#"'&54632654&#"32654&#"Hmc����j`z���ȅ�v�_OP`_NQ`wYWrtYge.�`��֤f�*1�{��i|�w�QT^_TO_`�=t�}vg}�   A���  # �@X;Kez������ ����� ��4VY_R`w���h /@4�! !!���@4!�0	O	�	�		�O���!� ���@4��O%� w�$��+N�M���N�qM� ?�+q�]�]q�+q?�+q9 910q] q]%3267#"54 32  #"&4&#"326]
TEWzj���	������^}RNgpTQoSSP��{�����u�n�����{����  T��a�   �@-YY
YVVY��	�		p�:4:4JDJD�		�t��t@  
)&�)@ �!X<+N�M�Nq�<M��<� ?<?<?�?�10 ]q]CX@ii
iffi]Y!!5#" 32!32654&#"a��A�Z����²��/Dza��gd��[Y'��p�Ln����� ���Q��   �@M& 6�� 	 @ � �  ] _�	&�O3�k !j�<++N�]M�N]q�]<M�< ?�]?<?<�]q<93<<<<10q]!#"&'732665�5�u*a81#+7������˧^�%4��   �  ��  o� ���244����#%4���@?4 @P��`p�� �  � � � �   0 � �  n1�+N�]qr<M�< ?<?<10]qr+++3!�(��F  T�Q`> # /N@bw�p1��1 ##033@CC[YY%V)V+Y/k��;3;(3,KDK(D,��
�*'-$����43 ����> ����> ����(*4 ����#%4 ����144 ���@	4`  _�t�'�t�
-�t@*)&�)@	�11��@
 3$!0X<+N�M���Nq�<M��� ?<?�?�?��r++++++�CTX�  ���4 ����	4++Y�+9 9999<10 q]]qCX@iii%g)f+i/]Y ]32767655#"'&5 325!# &5432654&#"yA(Vn7%~��}b�ŀ>p�������`g��he�F'8!1#^��������G��j<����������  �  Y�  �@+933BB��	$Xh�t@	


  
&	@ $4�	�		���@"$4��p�� &���@ $4��?<+N�qr+<M�<N]qr+�qr+<M�< ?<?<<<?�999<<10] ]632!4&&#"!���a�O�� Q=Fn3�����Hp����1�Z5D�����   s���  2@!0@7   0D   0  �l+N�]M�] /�]10!s(���   Y����   �@U����'x	wwx����������-	-'�
 

 

��@ 0@`p�� �'�   0  ���~�+N�]qM�M]q�]qM� ?�?�10]]q ]4766763   !  32654&#"YC2�g��D��~�����~1汱�ݷ�����p�+:�n�����o�h��������   �  � @&&���@	:4
 :;4	���:;4	���@�.4
 .4	
�	�
	

	
#, 	/
ghe	j
wx�	�
�	�
�	�
��	�
�	�
���	�
���	�
w	x
���	�
�Xejg	h
vyDKD	K
WW	X

/4:4	;
?		
	�CTX@
	22  P4P4���@4@'4@'4���@'4 
  ?<<?<9++++++]/���9��;@-
	 		2

2

		���8 ���[]4���@ST42@�� �8@  @[]4 @ST4 2��1u+�q�++<�<�q�q<�++�<�q ?<<<?<9�.+�}ć.+�}�+Y10K�SX� �� 88Y]]]]]]qr++++ +q]3!!!!��
�������������F��~��~  �  #� 	�@	�� �?����[]4���@*ST42		@[]4@ST42���@@P`p��� 0	����[]4	���@SS4	2  0 �  ���
1u+N�]<M�++<M]]qr�]<M�++< ?<?<99 99�.++++�}ıCTX� ��@	'4 '4����	4@	4 ++++Y10CX� ���5�5���@=.4S.42@F�������� /4;O���������@	354@354���@/24 /245���@	!.4T!.4���@F 4T 4,';3N@\V	ME�������'(Jx��]qrr+++++++++ ]]qr++++Y ]3!!!� X������-��F��D   �  a�   @3((
Gee*9HYh96���% %'�����	4��@�! !0!!   0��� 1S+N�]<M�<M]q�+qM� ?<�<?<�<10 ]q]!2#!327>54&&'&#��`��`-7fM�b���(�|7H_<<lS>��&���ε��cK*��5VŪ��f   �  ��  �@=%0�	%
	% KH
  0@	   0  ���1S+N�]<M�<N]�]<M�<�< ?<�<?<�<9/]qC\X� ���9����9����9+++Y<�<<<103!!!!!�?���� 3������q�  �  ��  =@P%    0  ���1�+N�]<M�<N�< ?<M�<?<10]3!!�(���I�   �  ��  ! �@�9IWjj�	��#��	


6FF	66Guy�
x	xv�	��		Su��� %`�  !% ��@' �'�����p# #0##!   0  ���"1c+N�]<M�<]q�]��]� ?<<<?<�<9/]q<�<99�.+]}�9 910 ]q]]3!2!.##326654&'&##�o�Հ��`}j����rT^f<��j<OH$���Oʂ��8����?�Y!��N$XBJ[   �����   �� ��@197GVV
VVY�5;;5EKKE��	
 �t��t@ 
!p)&�)@p �  ?A+N�q<M��<�Nq�M� ?<?�?�?<10 q]]CX@ff
ffi]Y ]+3!632 #"&'32654&#"��������[�@4Iy]��ge������������[Y�*�Op�����   #����  Z@$i�T	f	iiiz�
H�-	   ��@p0�

�u+N�]M�Mqq�<M�< ?<?���10 ]]!#"&'%3265�' +��� 0bcR��`�b���� ~4Oq�  �  _�  � �ݳ?���@}-4'	f�
�
�	�
�

S`	FWv�	����NNf}������
++***/KK
	
	

	  


�m@/9e&�   ?{+N�]q<M�<�q���<< ?<<<?<?<9�}�<�CTX� �Ȳ	!4 +Y10]]]q r]++3!!!�IZ�����������v�|�^݉��  U �V�  H@	b0@7b? O  b
��@bO��MC+N�]M�<�<� /]��]�<<10%!!!!!���� ���}}������     �� �@++ 3 @:4����:4����:4����5	���@	4
4���@	4 4���@Y4 4		
 	) %	�
��	�
���
�� �	�
�� �		���
����
��	."/
 ���
��CTX�����!4���@	!4@!4����4���@4d4 	  ?<?<<9++++++99�� ��0�
	 ��2@\      
2

	 		2 
	

		 /�0@
 ��@/�0@  0^c+N�]M�]���]NEeD� ?<<<?<<<<<99999999 9�M.+�}ć.+�}ć.+�}ć.+�}�+++Y10]]]]q++++++ ++++q]!!!!!e��/�`�*������������  �FH��  k�Qh�  F@(�	 	 �" 	 "  �@
	�� 0����k+�]����� ??<<10]#&5673e���cV���g=5#�Q���!����W����f   C�Q@�  I@''
gg
���	  �"   	"  �������jC+������ ??<<10]>543ESD:f����BK��Q����u��/���������   ��l�>   �@.8H4994DIID�	VV
YVVY�� �t��t@!p)&�)@p �  ?A+N�qM�<�<�Nq�M� ?<?�?�?<10] ]CX@ff
iffi]Y ]!6632  #"&'!32654&#"�3�j����X�O���fb��cg�&�Pd��������FU����������    ��  �@26*  Y��  	_��t@
��t@  �  
	3?OP(/_�@&_ ������	4x�i +N�+q<M�<�<�]<�]� ?<?]q<�]q<?�]q9210q] ]3546632&#"3#!#�9�uxs&C>=5����&P��S$�9QK���I   3  � ?@_��������CCCV����  (7HCCC$$$&V������  1v������@4     0 @  ����4 ����V@#/@4�	�O  �w��+N�M��N�q<<M� ?�+q�?<�+]q<93+]C\X� ���9����9���@9999++++++Y�CTX@	  99]Y10]KQX� �� �� ��888Yq]]]!6767654&#"%6$32�'��+:eYXh�����GM3��G���	۱?WU^ej{���c�bA�P&   &  D� 
  �@9 9	+Sk��%(H[���	 
 ��@
 @���(  ��   �X��

�@��?�LH +N�q�]M�]<�< ??�<�]<999 99�.+}��CTX@-=M�� ]Y10]] ]+!!533#~��|춶����'���^�����  u���  ?�	
�@�8

r&$    0  gv+N�]M��� ?M���9 9910!'667#�*uZ7UH��z�p tbU   M��� ) �@2��{�����������!
 !
�$@O@��@/@4��V� ���@24�'���������O$$+�w� *��+N�M���N�qM��]�9/] ?�+q�?�+q�9/]q�99 999]10q]] ]%32654&#"7654&#"%>32 #"$MrQWwrR6KrxXIHf��m�y�}g�~��������!hn�pj|�iWJXd`,��[�l��s������  W��*�  # �@;ju�����������6Dz���� �   ���@4�!/!!@4!�?	@	�	�		�O���!@"/@4�� w�O%�$��+N�M�N�qM��� ?�+q�]�]q�+q?�+q9 9]10] ]&&#"632 #"  3232654&#"��
TCY{i���������*����~QNhpTQpSTP��|������Y��d��鉕z���  [��5� @) 7EI����	!#� 
��@
 0@P��V� ����4��Z@
/

@4
����@4 0@��@//?O@4��@���@�!@w�� @ � �  ӹG +N�]qM���N�]qM��< ?<�+]q<�]+�+q�?�+q�]q9�.+}�9 9910q]%32654&#"'!!632 #"$[vMXzyay`����,^b�i���� y_o����k!����/��ٵ���  b����   �@F8KVvv����	((((H[T	Zj{zt������  ���@9  %-	@4KO@4�(@*-  _'V   "0""'�


0

���!~�+N�]qM�N]�<M�<��q9/< ?��+]�+?�9/<�q+<910 ]]]5!#"$54763 &&#"32675?~]�����������3,�������]�C���Z��g��d_I��7l}������I4�  Y�m�  (@}��!� ���x}w �
����	%!%kz t Yhxyyy ���� �������7Xii
z yL \ l $"''$ &-'�L�&O"-	����4�S@�		&&'K�*����	4��@ 0*@*`*p*�*�* *�**'�0���)~�+N�]qM�M]q�+qM��9/ ?��+���?�9 9910 q]]q]]]%&'&'#   !  %6654&#"327&'71m�mC@��������IF~5(��99൵��@9Z]S��N.�#{?�hg��q����n@C�{�������;!�2   ���$�  �@8		GG	W	V��������� %	 ���@"@P`p� 0��   0����1u+N�]<M�<M]qr�]<M�< ?�?<<<10]q!32665!#"&&'&5�(�|~�(0�خ��~���8Zmg��+����ږYa�U~�        l  �  �  J  �  2  	  	r  
�  (    0  �  �  �     �  �  0  �    �  �  �  �      �  "`  #�  $�  %n  %�  '�  (�  )   *(  ,|  .z  /d  0"  0~  0~  1�  2�  3|  4�  5$  7f  7�  8z  9v  :v  <  =6  =�  >�  @2  A�  B�  D�  Ed
endstream
endobj
12 0 obj
<<
/Encoding /Identity-H 
/ToUnicode 24 0 R  
/Name /F-1 
/DescendantFonts [25 0 R ] 
/Subtype /Type0 
/Type /Font 
/BaseFont /SUBSET+ArialBoldMT 
>>
endobj
28 0 obj
<<
/ModDate (D:20250109191209) 
/CreationDate (D:20250109191209) 
/Producer (Ibex PDF Creator 4.7.3.0/7447 [.NET 3.5]/R) 
>>
endobj
xref
0 29
0000000000 65535 f 
0000008847 00000 n 
0000007929 00000 n 
0000011688 00000 n 
0000008981 00000 n 
0000009016 00000 n 
0000007329 00000 n 
0000007846 00000 n 
0000008011 00000 n 
0000000020 00000 n 
0000059259 00000 n 
0000059421 00000 n 
0000087503 00000 n 
0000007586 00000 n 
0000008355 00000 n 
0000002102 00000 n 
0000007989 00000 n 
0000008809 00000 n 
0000008698 00000 n 
0000008750 00000 n 
0000011709 00000 n 
0000012309 00000 n 
0000012822 00000 n 
0000013048 00000 n 
0000059536 00000 n 
0000060099 00000 n 
0000060582 00000 n 
0000060812 00000 n 
0000087669 00000 n 
trailer
<<
/Size 29 
/Info 28 0 R  
/Root 1 0 R 
>>
startxref
87810
%%EOF
```

## uploaded_files/1183UX_document.pdf

```pdf
%PDF-1.4
%ÈÁÄ×
9 0 obj
<<
/Length 2022 
/Filter /FlateDecode 
>>
stream
x��ZIod5�ϯ�h��EB#e��D‸�:�� �*��=?���EN�n���\��->	-�i��L"� ]?�������\�ڈ�_�x|~'�~׎��{��e�4A���~�N0D��ax
�Xq��E���8٠>SJ�CՌU;VT���n��s܇���ֱ*���L�:+}J��lp�(J���<@��0��pL�2z�S.P�D��0쩡�٢�'��YLYڕ����Ɲ)�t��i`bt��BqP<�@8a�A�:��2Fg,{0c����DiS��ُ�-s����r[������U�?Y<��6y�"���K2�+��ߕF�W�;��G|'��-}�P��W
���[�a����o�6�a1�z��b�V݅ Num"P�@�Y�Tj�J�Z���2od4#��Z��@\�HVMKj�HF�c`9y�z�/UMQ�#KB����4�Aw��*�I�
�&$�X�sE�-oX���P����������?���|�����g��b>lm�p�����_�M��c��i�e0U��~@zH'�0Yp��m�!X�0�nD��=�˾ut��,
\l�i�Q�0;��O����Y���[i�lvj��J<�q*�H�PKK��&6z�F�~�&3U��p�n<♉����ՏKp�+'��o�jX���"��4;�jΖ���r�C���I+�m�l�A�������Ѭ����B�6^��6͸U�����b��)>n����/g|ȴ=8(��Y��Qf��V
38t`):/�"C&�s�Q��2�
؝`)hr���0�A��T��}�-�I`7��E�:�(��Cz$6*ˠt�ZL;�@C�����`����K��2��_�70����F(M�f��h���Ժ=�c2G㸆-�X[81���	<u�f�BT˘�!#�;8�n�y<�+7�54x5�@�爃���2�G��^��N������
��N�'ۜ&�
E���x���uGF��y���\�B�\4Uw�ܾ��e�\K%��e�"``���vpX:��u��gU��o����A���.f^�K�{ĸ��޲	>�b_c,Gq���A����b7kj����~kw-�5�|c�A�d��E��d�4���r���tv5u��1���WlsK�z+BS��fː���vJpU_� �#��%���=�a�Y#�;Aҝ edR*��D�[?O���y�5O��&�,�Z���10.�Õ��wdȎ,�`��3�MP;�Ե�c�83p±������n����|�2�X_�p��9�1��G�M��n����@w��V�'9�-�,z���J�ӓ�VW���F�ǛD)V6��Q��93y��_fL��|�G-��l3��"�!��s��b�Q�
��e�I���:
����	�$��W�<I���f�8�&��'J�;��g��� !�b2�mD��E0��JN�ǹ����� ��S�0���[Q�)oJ�"4��2SQ��2�?	 ��«��ng�[��u����$t�?�WC8B����X"FѸVL��N��ȫ�ׅ���4�04�h΀[�̪!aL�+��T�`Z�d����n�BHw�p����	�?���&�����6�
��4�7��G�;��Fwn��W�#%4��ī��wv+}�H����ěG����
����������pwW�d)?FB���-\����`��s"�b~ ��-���-����LS�Ƕ~p���஧�_HJ�����֟t�2ۚ�(|���D�EML`��#��E�n^>�Ȭ2�%���Y��y҄�z8O�S(����zpC�&N�>Ax�S]v�����UlM{9[��Mlo۵c��5Iҩ��(�z���Ț߇&��ӆ�t[ր���r��� �M�yu����/�3�k�;��F<���֟$7�{�Yʃ�ؼ�{1��T��z0��$��Z���� ���<�4Q��-��0�>�+
NFW�P[5YAuCB�vDW��`��/	�ré���h B��Y�:zX�r�w
endstream
endobj
15 0 obj
<<
/Length 4653 
/Filter /FlateDecode 
>>
stream
x��]ˎ%����W��ZoE F����v�0��=^T͠���zP�I�*w�p+#�J�DR�H)��ۨ��6Fɾ�L�o���|�~��ϟ��1�}�۶��a��eyF��1*P�������d�PW1�5�b{:�4ۧ/ޞ��������#Ϗ"?J�����ү�e��_�O������.V^a���}ߞl=�����k�1����a?���b?��������6W��~��c��E������\�����[f���N�X;
;s-�D2-c����#�Gڏ�8m�2��b����4�0��"v��%v�� QvN���w�s�mf��n=����pc�l7���&�}�;��gx��}�R�����-�m���4���Q"�W�OOJf�RW�_۟�1���>*��G�:��=�@ �܁�v��^>��_��5ŉ�Fx���H�tM�^
�%i�2:��G�3���I {���:���tЉ;��
0@�]Bb��x(�<J�{��o�;Q�չ��}������~�??oo�ߎu��8،�4���(��s|i�eIG�WD� ���-�'5�bXc��P:��F�����^a��{�(-�X�Z��QZ��R�L)p�n'�'m;� ��
$�	�E��m�V� [<Nj���b��Zn9Om��X��;�	$|i*G��b��X1#�F�-W�x���8+�P�m`а���X@�j��'V������9LD|�P���4�;AU,D1� �<4��;򮶧 �Y�L��������Ms�"�[\}���S?�<;P�����]lg�qwM�]�(E��r�!������m�2A=؉��L_�����^�Փ���2~&�FIo��y��٠�j���X�sK�
�z�,�<��N ���',a7�k:r��6&�h^{$�t�����9g�2,�voG�s| P�;Y*�'��|Q�.Vk,7|F缠}������c�FS&�S����Sf�pai��E|����FdGu�eg�v�n�Y��y��36n���U\��P"Y�X�2���z�
�=��v	�t��n'"iWxyP���T��B��zUF����(hYN(vY[��̈́#� o_���d�����`���K ^�g��M�?��K|ل�Nx�XN�?�G(��H^�Nx�XN�?�G�w"���P���݇F7�u�ɠ��b����VwČ����٬��(¬1gν�Yb{����l���r5&~���v%��W�-�*r�"ѪnAT�ĺT+DO��h�yv~{⽘�d�¸��;���g�>�����[G��|��g�}4��!��:f=�ɞ�C#��N4�%͝��X�YU-h�î������RmV���0l~O���rLz+� �F��~a ��
�􍁠]O�n ��Xv�t~)]���L�H���W���a8JO4뺵�`�\$Z�-{�*�kD�%QN��Vu���¬�C;���?�7�^��T���o R/3q*��.,���Oi��q��H� ~�M긛�����m`�گWh�3ɺnIԢ>�"ѪnAT�T�F��[�k�].��ڰn�ѺnAt���C���D�@�}��Ħ{Y+Ew���jZ�,�Ν��Q�w���rB�V��txA��[�mטE�U�F;3C�T3�G���q�8K�8&�B��lܹ-�vg�#@-Z1���n���i�uˀӷ���oZ��%9�%}�����P�DrE���x��H���n
�=�`��w4�^{2�I{�];p(��y'Z_/�0-j	N�yϬ�g����hH��\���J��4��9�wr5�����F�Y�!wx�.�æ�޹K̚�4Xyҍ4��|������ӵ<��wQS��ό%.�]��vOd�`�[$���%q!������~�q�����v�����w`�5Un�{Pi,wv�c?�`l��D��L�����/Т�̐�[�g?VÉ��=9�j�j��rH��S�L/�Y�p�#�N" �CS��"�=�H���{B�Ŀ@ħ�^�c>�{��;hB��@���[DJ�T�L�P5P�a@��F"� �@ �' �"(:�U�H�`A4(�4/{�"(:�U�H�`AT(�Ҵ��+Pt �����a5�+Y���?&�5@voL��s���E���ɀ�vֿR.��EC� ��o��e����g}��M�?���Ce5��?���vi��E��=i�8C!Ҽ1;kp�x���/�GF�����~!��͈p�Fa�
�0�ϣN���_EDFRdA�"������,}+��Q�"����_����u�2��0mHJ
�甌�� |�AD�?��;YNpT��3 |�AD��, �'�����R2��P�ف+ �� r�`2K��"KKx��Lť�݇#)��"w�G8�%&�b�$��"tί'����^'b�r�>*;�^"�EN� ��`#jG�L��[u�F�H��[n�������y0�8���V&����p����BM�3���%n��KXQ��{�l���C͵�o)V5K��-Sr�dU��,�h��Or�{��ڼ|--L��B�ڕ��ֲY�ep�A	ũkKs�.���.����PI��S6A�.S�Q�=Ѭ��v#�"Ѫn���9�Dǝ=3K�H�bY�*a{���~����J��Z�W��̮�9.��L��\��V�U�U咬��O�W�N��O��@�Z\��\�~��y��m��9h�9v�ض!���92�֐�edW���4u���� ^�d�M��hAMp����R
:�oK���5���AKr�`wJ`�R�oB*�KK�;>#����Q�X�!��h>��ufbzv*3�;u�����5�>v�;�x
~�����ʁAc��s���@
�j��螑ǫ�����C/�Y�*s+���TE����M&I$���@��^C �w����2nw �9[0 XƖ���'�@�P�Yf���?�qaBu(r,���q�d1�|�xdf��E���z,��`ÚW��j��xK�ʼ�Pgp���XTs��{���@�_�X˖��M�B�S�jRi1��F����X4���Ej�b\h޲Ű��}��f�5�8w#3{�b���C8Wí:�/�5/p�����@�b ��59X{�Aό���q@2����yO#�e۱I��F$:��bR;J����n��Z֏	��Y0�8�'ҭH�4k���P<�K|���_hT��t}���_h26HPc���F�~�h ��$������˶c4��Q`�<���k��[6�\o�L� /����Ac�Z2��y�Q�ˏ��~xgch� �A�,�%�$�n�F�̢��2;�e�[���T,��rc�)�g��qP�z����\������� ��^�x�Ơ."@\�G��N͗�IP���4���X���ۃ2�
�d����p��ٕ��y��孁�v�7h� �X�V��M���L5|��\'�#w������z��E�b&�RN��H�E6߸�%v�A��e�{1�����g��C�7�{ۏ�Y�V���(
6u����5Q�^�AR��E���������D�	�8�?�ۊ30�@ҷ}71�� �CP�
F"����K<�sF@�����zKH�(�,X� ��}4�L�>"H�H�4��P@�>�D&v�GP*��P��	u�4���f��g{e�Ƚ�mY<q��>�o%���F���_<X�
>����/z ��/�{ h D�O/�6.M �f�;�,Ex���|��)+c�?���g�����YL0Y�f<��3$����P��o�B]�,�������fA��0���;lh���bAd�ˋ��p/�/{Qs��k��9#�e/j��/sQ��i��w,�ͩ#uq��.ͱD�&.��:�8�鲹�9��pW�E��t�맣6�|�x:ѿ<�Y@c&@I!�&��2|A�͍�]��IGޤȧ�D`F��2K�~��	�ժ��4��s�D��!�'aH:c�-��m�P�#�+�;�$��͚��չ#�q���L�޹��闶���zN�޽�2k�����Ο4�n�=�ďl:ō[��]es�n��˛��U������rL`��UM�,�R俎��6A)*��
pe1;�"�x��a1L��sz|��G��-l�b2��~�˨�x�.�,<N���b)Ϯ��TD`����A��>(���f���b���3;������MR�#ˋ�bh4&k�ãALν{!&��hpL�c��"��Gp��3�HV��6�q|��87f]a�^�Jo��юJb��®5�+�N�
�mU|�Ӣɖ��)���\$&Խ7�#�
��{z�cfّ��:�%�*�gyX51�0��RkԤ������?h�|����&s~��t�Ў'T�ѸhȂ�	N��K�������:��i��Q�-c�a'ED�N0�>��"8_0�����{	%����˶մ� /wP�݄�	"c�"�0t���I�G�� �_��Bq��#�.�F������V�t'���̯�k	����.o�C��4-�(2_\h������H����e���ĳdW 
|!R�t�T�B7
endstream
endobj
6 0 obj
<<
/Parent 7 0 R  
/MediaBox [0 0 597.6 842.4] 
/Type /Page 
/Resources <<
/ProcSet [/PDF /Text] /XObject <<
/DLbd 8 0 R >>
 /Font <<
/F-1 11 0 R  /F-0 10 0 R  /Helv 12 0 R  >>
 /ColorSpace <<
/DefaultRGB 4 0 R  >>
 >>
 
/Contents 9 0 R  
>>
endobj
13 0 obj
<<
/Parent 7 0 R  
/MediaBox [0 0 597.6 842.4] 
/Type /Page 
/Resources <<
/ProcSet [/PDF /Text] /XObject <<
/DLbe 14 0 R >>
 /Font <<
/F-1 11 0 R  /F-0 10 0 R  /Helv 12 0 R  >>
 /ColorSpace <<
/DefaultRGB 4 0 R  >>
 >>
 
/Contents 15 0 R  
>>
endobj
7 0 obj
<<
/Kids [6 0 R 13 0 R] 
/Type /Pages 
/Parent 2 0 R  
/Count 2 
>>
endobj
2 0 obj
<<
/Kids [7 0 R] 
/Type /Pages 
/Count 2 
>>
endobj
16 0 obj
<<
>>
endobj
8 0 obj
<<
/BBox [-20000 -20000 20000 20000] 
/Length 113 
/Filter /FlateDecode 
/Resources <<
/ProcSet [/PDF /Text] /Font <<
/F-0 10 0 R  >>
 /ColorSpace <<
/DefaultRGB 4 0 R  >>
 >>
 
/Subtype /Form 
>>
stream
x�UJ�
�@���wέ����@R�	ۉ�����7B��y`u$Б0�
=���xvL����%�����1k����L���_\l�5c�d�~�]%��� �6��y�
endstream
endobj
14 0 obj
<<
/BBox [-20000 -20000 20000 20000] 
/Length 112 
/Filter /FlateDecode 
/Resources <<
/ProcSet [/PDF /Text] /Font <<
/F-0 10 0 R  >>
 /ColorSpace <<
/DefaultRGB 4 0 R  >>
 >>
 
/Subtype /Form 
>>
stream
x�]�=
1��=�w��I4yDP��NH'[-h��z�§������8r$6U�a�˚i��?�x>X��h���-��b�>�vRj�����=!�E+���O�ye���~���o� y:�
endstream
endobj
18 0 obj
<<
/D [6 0 R  /XYZ 10 866 null] 
>>
endobj
19 0 obj
<<
/Names [(Total-Page-Count) 18 0 R ] 
>>
endobj
17 0 obj
<<
/Dests 19 0 R  
>>
endobj
1 0 obj
<<
/Names 17 0 R  
/Pages 2 0 R  
/PageMode /UseNone 
/Outlines 3 0 R  
/Type /Catalog 
/ViewerPreferences 16 0 R  
>>
endobj
4 0 obj
[/ICCBased 5 0 R ] 
endobj
5 0 obj
<<
/N 3 
/Length 2591 
/Filter /FlateDecode 
>>
stream
x���gTT��Ͻwz��0tz�m �I��2�0��ņ�
Di� AFC�X�BPT�� ��`QQy3�V���{/��ý�����]�Z �O ��K���C����1�t� �`�9 LVVf`�W8��ӝ�%r���# �o�����I���  �ؒ��b��@�i9�L�}V�ԄT1�(1�E����>��'���"fv:�-b�3��l1��x[��#b$@ą�\N��o�X+M���ql:�� �$�8�d����u� p��/8�pV�I�gd��I��K�nngǠ�pr�8�q0�������L^. �s�$qm�"ۘ���[��Q����%��gz�gm�w۟�e4 ���f�ﶄ* ��  �w�� $E}��E>4�$����999&\�D\���������x���C��$2�i��n���!����dq������0
�$r��("R4e\^���<6W���ѹ�����}�k�(�u�	��F�� E!$n�h��o�H �yQj��������.?��I���C��,!?���Z4  I@
@h=`,�-p .��� b�
�� �A��@!(;�P�@#hm��'�9p\��0�F�xf�k� A"CHR��!C�b@N�' �B1P<�� !�m���2�����o��9�24݅Ơi�W���$�
��:�)̀]a8^'���5p����#p'|�
ã�3x�!�1�@ܑ $ID��z��@�6��Gn"����AQPt�1�僊@�P�P�Q%�j�aT'�u5��E}D���hC�=��NB���&t�z=�~��`h]�-��I��Ŕ`�a�1g1C�q��U�b�AX&V�-�Va�`�`o`'�opD��煋��p��
\�4�n����k���Ax6>_�o����'�i�.��NH!l"T�/�D�юB�7+�G���cķ$�ɝG�v��Β�^��d�9�, � 7�ϓ��HP$L$|%�$j$:%nH<��KjK�J��\#Y!y\��^JG�]�)�^�F��m�9i���t�t�t�t��e�)�����[�@��y�q
BѤ�SX�͔F��Cե�RS���o���YYY+�H�ղ5��dGiM��KK��Ҏ�Fh��T�\�8r����n���+ɻ�s������)�<Rv)t)<TD)(�(�(�W��8�DUrPb))S��+(�*�U>�<�<���⭒�R�r^eF��ꢚ�Z�zZuZ����U+W;���.Kw���+�}�Yueuu�z�������F�F�F��CM�&C3Q�\�WsVKM+P+O�U�6^�����W�_{^GW'Jg�N�Δ������V�zd=g�Uzz��1��T�}��`k�d��k����!�p����Έg�`tۘd�j�m�j<fB3	0�7�2yn�ek�˴�����Y�Y��}ss?�|��_-,X5�,ɖ^�,�-_XZq��[ݱ�XZo���`ck÷i���ղ�����͠2�%�Kvh;7�v'���������`����0�Dw	gI�qGG�c���)��Ө��3ӹ�����ۥ�e�U�5����s737�[�ۼ���:�����G�Ǡ��g�g��#/�$�V�Yok��g}�>�>�|n����|�}g�l������������z�@��݁�j/�-�
A�A����
�>R�$�<4/�?��2�%�u�[xi���aDo�dd\ds�|�GTY�h�i���1�1ܘ�XlldlS��2�e{�M�Y�ƍ,�]�z���+�V�Z)����x<:>*�%�=3����K�M�M�e������]���i�#��3��X�8�䘴;i:�9�"y��έ�H�I�K�OJ=����֞�K�O?�����2T3Vgeff���_�g�,ߟߔe-��PE?SB=��X�SvM���Ȝ㫥W�V��nϝ\��뵨����y�y���ֹ��_�OX߻AsC�����o"lJ��C�Y~Y���Q�{
T
6�o���Z(Q�/���ak�6�6���۫�,b])6+�(~_�*���W�_-�H�1XjS�'f'o��.�]�ˤ�֔����YN//*�g��Vu{	{�{G+*����vV��N��q�i�U��^;�����~��mu*u�u�pܩ���l�i�8�9�}�Icdc�׌������>�=z��ٶ��E���n�N�;r��o�ی���i��G�Q�ѧ��;r��X�q��﴿���tuB����]�]��1�C'�N��8�t|o�����'kNɞ*=M8]pz�̚3sg3�ΜK:7޻�������B�/�_�t����~��3�/��l��ƕ��6W;�:~���c�f������v�{�����|��M��o�޺:�txh$b����ۣw�w���}q/�������J=�x����G��GmFO�y�<{|�5�짬��O<!?��T�l���:9�5}�鲧�2�-��,�s�s��������l������_K^*�<���U�\�ܣ����(�9����]ԻɅ������?�|���`1}q�_����
endstream
endobj
3 0 obj
<<
>>
endobj
20 0 obj
<<
/Length 475 
/Filter /FlateDecode 
>>
stream
x�]����0��<����*x�$���XX$�V�}���$�	�~���U9}xf<_;����M�=��!���vM���`���vff�4m=*�G}�3{���1\�ݩ7���d?�����i�����d�	�������0��6�%t�����4��(���U�`���<�>��Y�y��`�K�7�:Tu�Uw����2���Y�Y��#�2���w�f���&�(	���D|!�	K�-��F,��Z`#K|A��Q*'�=q�0��-r������Iߜ��7��-"|=KY�n��ve��2}�o�k0|{���_GA_�m��i��-�2|�5P��/�NP��9�|K"|����H�빯�׳+�|i$���oN#�o�_�
��+��ߜ=;�"|�t�]����8�:]���ʜ/��Ns9_�;��sD=p�3�����^�b���tä��8�m>o��R�> X�N
endstream
endobj
21 0 obj
<<
/DW 500 
/FontDescriptor 22 0 R  
/CIDSystemInfo <<
/Registry (Adobe) /Ordering (UCS) /Supplement 0 >>
 
/W [0 [0 722 610 889 277 556 610 277 722 556 610 333 666 556 389 556 666 556 556 722 277 556 556 277 610 556 277 556 556 556 610 277 277 333 777 610 833 722 722 666 610 277 722 610 556 556 583 943 610 556 333 333 556 556 556 556 722 610]] 
/Name /F-1 
/BaseFont /SUBSET+ArialBoldMT 
/Subtype /CIDFontType2 
/Type /Font 
/CIDToGIDMap /Identity 
>>
endobj
22 0 obj
<<
/ItalicAngle 0 
/Type /FontDescriptor 
/Descent -211 
/FontBBox [-627 -376 2000 1055] 
/StemV 0 
/Flags 32 
/Ascent 905 
/FontName /SUBSET+ArialBoldMT 
/MissingWidth 1000 
/FontFile2 23 0 R  
/CapHeight 715 
>>
endobj
23 0 obj
<<
/Length 25604 
/Length1 25604 
>>
stream
    	 0  `loca%�    c   �fpgm�� ,  �  >maxp
�    �    head�     �   6cvt ��   4  `prep\[ =     �glyf��  !�  A�hhea�     �   $hmtx    �   �      3�2_<�     ��<    ք����� r  	         >�N C ���z                 :  � a� R ~9 �s 0� �9���  s U� �� V Js I �s V �s As � �9 �s Fs V9 �� ,s �9 us Ms 3s [� T9��9 �� s9 Y� T� �� �� �V �� �9  � �� �s #s �� U� � �s &� k� Cs Ss Ws Ws A� �� �    :� < �    / V  K�  A T���5  �� < ���A� ��  �  � ��  @��2@���2@���+2�����:3@���-�2��� _ 3����U3@���@D2@���3;2@���/12@���3@���2A� /�  � /� O� �� �� ��  � �� �� ���F@���3A�  @� �� ��   � �� �� �� ����	2@���3A�  � � �� �� ��  o� �� ��  �� �� ���A
� � �  ����2@���2@A� P�  �M �M  o� � ��K�-12���K�
2A�  � ��  ��   � @� ����2@���2���{�042���{�2PAx en # ~n  cn  bd  ��@�2�A? ? ) A 2 D  ��u�2���u�(*2A
C 2  4 �2 �@  @��	2@���2��  ���
 /
 ��T�	2�AT �T  n  �n  @n�	2AE  k  F  �� F ��&���  @��	2@�>�3@�>�2�A	>  �� �� ����&82 A&( 0(    0  � 0� P� o� � ��   � 0�  /z pw �w �z ���2����$(2��2� ���	2@��2����2?�s Os  @t�2o�*  @,�2@�p�	2� 2 ���2�  ��A   ��  ��  ��  ��  ��  ��  ��г	2@�ҳ	2�A�  _� �� �� 0 �� 2 �� ? �� d �� 3 ��!����!�@���2���ò+/2���ò%2���ò2���ò2A%��  �� $ �� " ��  �t � �5 ; �5 ; ��  �� 8 �������������� ����P/���  ��&���&$�5 �t�A
�X� � ��  ��7����� ���@7@%@-@�0%0-0� % - 7 � A�  �� �� 7  � 0� @� ���7�A�t �t  �t �t  `t pt   t t  �t �t  ?� O�  �~ � �� ��  �z �{ �| �}  �t �u �w  p~ p p� p�  pz p{ p| p}  pt pu pw  `~ ` `� `�  `z `{ `| `}  `t `u `w  P~ P P� P�  Pz P{ P| P}  Pt Pu Pw  @~ @ @� @�  @z @{ @| @}  @t @u @w  0~ 0 0� 0�  0z 0{ 0| 0}  0t 0u 0w   ~    �  �   z  {  |  }   t  u  w  ~  � �  z { | }  t u w  �~ � �� ��  �z �{ �| �}  �t �u �w��A�~ � �� ��  �z �{ �| �}  �t �u �w  0t @t  �~ � �� ��  �z �{ �| �}  �t �u �w  �~ � �� ��  �z �{ �| �}  �t �u �w  �~ � �� ��  �z �{ �| �}  �t �u �w  �~ � �� ��  �z �{ �| �}  �t �u �w   ~    �  �   z  {  |  }   t  u  w �X �)  � ~ � } � | � { � z 7 w & u   t �7A5 O5 _5 o5 �5 �5 �5  �5 �5 �5 �5@"O�����O����� A  _5  �5  5 �5  /5 ?5  ?4 O4 5544@� �*�*�*�*�*A	G    7 X@&>�&>7&'>�����&6���&6�)@+&6�&6�&6�&6�&67&62&6-&6%&6&67&*�X@"&>�&>�&>'&>!&> &>7    @���� 	���'(���'0���'O���'bA	� ' �  � ��������������4�]�'.�[�'�AU  T  S  R�V�Q�)�+�'&A* '% )X � %  $���#�;�"�9A '  -   ���X@�������� ���%�V@
�-��A�A
X  �X  �X��%���X%��.�-���)��X�� ��@�0t-�sJaR]%���\�  YX��P%�I�%�G%�@Fy@'9 ��  8X�7-�%  2X%�,4*%��U7�@*��[B;#"
 ���@+                     J �KKSBK��c Kb ��S#�
QZ�#B�K KTB�8+K��R�7+K�P[X��Y�8+��� TX������CX� ��� ��YY v??>9FD>9FD>9FD>9FD>9F`D>9F`D++++++++++++++++++++++��KSX��Y�2KSX��YK��S \X�ED�EDYX�pERX�pDYYK��S \X�  ED� 'EDYX�B  ERX�  BDYYK�%S \X� &ED� !EDYX�
 &ERX� &
DYYK�S \X�� ED�  EDYX�%  �ERX� �% DYYK�S \X�X &ED�&&EDYX�# XERX�X# DYYK�)S \X�ED�-EDYX� ERX� DYYK�/S \X�ED�%EDYX�5 ERX� 5DYYK�S \X�ED�EDYX�( ERX� (DYY++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++eB+�1u~�Ee#E`#Ee`#E`��vh��b  �~uEe#E �&`bch �&ae�u#eD�~#D �1�Ee#E �&`bch �&ae��#eD�1#D� �ETX��@eD�1@1E#aDY�?<XAEe#E`#Ee`#E`��vh��b  �X<Ee#E �&`bch �&ae�<#eD�X#D �?AEe#E �&`bch �&ae�A#eD�?#D� AETX�A@eD�?@?E#aDYEiSBKPX� BYC\X� BY�
CX`!YBp>�CX�;!~� � +Y�#B�#B�CX�-A-A�   +Y�#B�#B�CX�~;!��  +Y�#B�#B ++++++++ �CXK�5QK�!SZX�&&E�@aDYY+++++++++++++++++++sssssE�@aD EiDEiDssstssststst++++++++++++ sssssssssssssssssssssstttttttttttttttttttttuuustuuuu+s  K�*SK�6QZX�E�@`DY K�.SK�6QZX�E�@`D�		E���`DY+EiDt sss+EiD++C\X@
  �����t�2o�w w ��w�/12���w�"%2@�t�/52@�t�(*2@�t�!2����72����%2���@-2�%�-�7�%�-�7�����2����/� t+s++++++++t+stY ++C\X�����2�����2++Y+s++++ +++++++++++++++++++++++++st++++++++ss++++++s+s+++t+++sssss+ss+++s++ ++++sts+s++++u++++++++u+++++s++++stu++sss+++s+sstu++stu++stu++++++++++++tu +++EiD+ @BUT@?>=<;:987543210/.-,+*)('&%$#"! 
	 ,E#F` �&`�&#HH-,E#F#a �&a�&#HH-,E#F`� a �F`�&#HH-,E#F#a� ` �&a� a�&#HH-,E#F`�@a �f`�&#HH-,E#F#a�@` �&a�@a�&#HH-, < <-, E# ��D# �ZQX# ��D#Y ��QX# �MD#Y ��QX# �D#Y!!-,  EhD �` E�Fvh�E`D-,�
C#Ce
-, �
C#C-, �#p�>�#p�E:� -,E�#DE�#D-, E�%Ead�PQXED!!Y-,�Cc#b� #B�+-, E� C`D-,�C�Ce
-, i�@a� � �,���� b`+d#da\X�aY-,E�+�#D�z�-,E�+�#D-,�CX�E�+�#D�z��Ei �#D��� ��QX�+�#D�z�!�z�YY-,-,�%F`�F�@a�H-,KS \X��YX��Y-, �%E�#DE�#DEe#E �%`j �	#B#h�j`a ��� Ry!�@��� E �TX#!�?#YaD� �Ry�@ E �TX#!�?#YaD-,�C#C-,�C#C-,�C#C-,�C#Ce-,�C#Ce-,�C#Ce-,KRXED!!Y-, �%#I�@`� c � RX#�%8#�%e8 �c8!!!!!Y-,K�dQXEi�	C`�:!!!Y-,�%# �� �`#��-,�%# �� �a#��-,�%� ��-, �` < <-, �a < <-,�++�**-, �C�C-,>�**-,5-,v�6#p �6E � PX�aY:/-,!!d#d��@ b-,!��QXd#d��  b� @/+Y�`-,!��QXd#d��Ub� �/+Y�`-,d#d��@ b`#!-,�    �&�&�&�&Eh:�-,�    �&�&�&�&Ehe:�-,KS#KQZX E�`D!!Y-,KTX E�`D!!Y-,KS#KQZX8!!Y-,KTX8!!Y-,�CXY-,�CXY-,KT�C\ZX8!!Y-,�C\X�%�%d#dad�QX�%�% F�`H F�`HY
!!!!Y-,�C\X�%�%d#dad�QX�%�% F���`H F���`HY
!!!!Y-,KS#KQZX�:+!!Y-,KS#KQZX�;+!!Y-,KS#KQZ�C\ZX8!!Y-,�KT�&KTZ��
�C\ZX8!!Y-,F#F`��F# F�`�a���b# #�����pE` � PX�a�����F�Y�`h:-,� B�#�Q�@�SZX�   �TX�C`BY�$�QX�   @�TX�C`B�$�TX� C`B KKRX�C`BY�@  ��TX�C`BY�@  �c� �TX�C`BY�@  c� �TX�C`BY�&�QX�@  c� �TX�@C`BY�@  c� �TX��C`BY�(�QX�@  c� �TX�   C`BYYYYYYY-,�CTXKS#KQZX8!!Y!!!!Y-� � � &   ��  ��  ���i��� �i���             � � �(  ��  �1 I  �  � � �  T � $  U I+ ���v�� = � ������  � � �  � 7 N U U e �� Y��  �  ; R a � � �   � � �|��   � � < A A���� * ���	� � ��c�i  " �+���� & Y � �+�H ! k � �� k � � �]C�   I V n w � � �P���{��   ( a i �5M��>�� [ � ��[�[�?����  �
��2�������  & 1 = N V b � � � � �� H S w � &(�~~� . A ] k u � � � � � � � � � �Jb��d�����  # % * t � � � � � 0Pjo���������&�����N��   L z  � � � � � � � � �8h����	"Op���N��5Bk����a�������������    & F i � � � � � � � � �+8;Z^hs�������   ";DOor~�����������"6q�����&.1OZ�22GS����<dp�����*��� �h������  Y z � � � � � � � � � � � �!'+9FKMW\e����������"+ASae�����������#+1IZ[nqt~���������uz����Lmm������/j��6P���p*               ��     � +�S� ?�h�n    @�  t� 5�   � ����= �`�n�! �& ���B �<V� �� � k x �ks ��:}7 �S� <��	I� n �d ^                              9 � ���|+ � � Y � �� ���   U a  � � � (  ] � &l� �  7>z � � ��&B  ���i���7�-   � t h G � � � � � h G \ H 
 ( 2 A P Z d } � ��������y�o �  �,�� � � \ < � � � �� � G                                                      �d � �%2��v�����1 x � � � � �
 c � � �B  , 4 A 8 H X lY� C p � ( 7 B P Z d s x � � � � � � �\ � �,c � A K U _ s �	�� A d  * � �8t , @ � � � � � � � � �
 ,;DVc � W d6 P�  �� 9 N D� � $ B"� � ` �   9� ,�N�8i� �  � T  =q A  P � O 5�R , ��� � � �e��w�l � � \ @vDr��         B���?@ � 
� ��& 	� +�<�<N�<M�< ?<�<�<�<10!!%!!  � ��@ �  �   a��^�  �@N�	��� ��	���	%	(())uu	�)*%(��	��?OR � �  ����4 ����
4 �Z@-@4K_O@4�(@"-
�V � O0'�0���~S+N�]qM�N]�]M��� ?��+]q�+?��++]q�]10 ]]]]#   ! &&#"326?B�������z4�d2���v��Ƞv�[���Zn��^�Fr�������   R���>   �@H������	YVVY�����	���	���������u���t�
�t@9`p! XA+N�M�Nq�M� ?�?�10 q]]qCX@	iffi]Y ]]4632  #"$&%32654&#"R����4������ �nn��nn�"�������Ä���������   ~  �> ';� )��@]
?4444#DEED# /)S	`)�)�)������)�)�) )/)P)�)�)�))@4?)P)�)�)�)!�t�
!�t@'&'
 &@Z5`o�F@&@Z5o`�F�%&&'�)�  '����	?'���@6
?'@Z5'@A5'@<5'@$'4'@:=4/'�'�'''�' ' '0'�''(�<+N�]qr+++++++<M��<�]q+<�<�q]+<�< ?<?<<<<<?�?�9 910r+q] ]+!6326632!4'&#"!4&&#"!~��f�0F�\u�(��'Q;h.��?6Ah-��&��TUUT_\D��Y_�.<H���F�Z,F����  �  ��   w� 	��@?
?@	P	�	�	�	�	�		`		�	�	  @ � �  ] 
&���@	!$4?<+N�+<M�< ?<?<?<�]q<<<<<10q]r+!!�������J&��  0��> *�@�#'#���'�*	F���!�#��")Ue���"�A#@$D&g"d&���"�$	7&EFJOF!B""$'&75!5"5#5$
	!'"""#$"@,sxyv)u*��*��*�"�#����*�*�,!@!#4@4�3!P%�%%@4%,���@
?P,0,/,,!03! ����	? ����
? ���@		4 +x�+N�+++M��q�N]qr+�+qM��qr++� �CTX@5&"6!F!TYdi�
!"((_F(PF?�]?�]999]q� "�˳(*4!��˳(*4"���$4!���$4"���4!���@4k6"F"��"�"�"!" ����4 3����-?����	
>����"%4���@4 0@P`�� P`����4�@M _�F(@43@-?@	
>@574@+.4@%)4@4_oU@"$4P�F?�]q+�]++++++�+?�]q�+]qr++++�+9]q++++++Y10q] qqqq]]C\X� $��@	?(?!���99!���9"���9 ++++++Y q]%327654'&'$'&54632&&#"#"&0ncm7%I��[~����(��_Xo0 &�YX����/+RU(/ K>V�����1>B#fJK��Ұ  �  Y>  �@Zh�44DD��t@ 
& @ $4� �  ���@"$4��p��
&�)����@ $4��?<+N�qr+<M��<N]qr+�qr+<M�< ?<<<?<?�10 ]q]!!4&&#"!!632Y��$Q9It+����]�O�e8P���&��Ch�{  ����;�  8@ I  
�� �l+N�M�N�M� ?<?<�.+}�103k�����      ��  
A� ��@	794(794���@	(54@(54���@P!'4(!'4) **(
/8 7?j jefhg
�J	
			    	 
@>
���@4
%	��@  �a@ 0��$@		0	�		�$ a@	 ^c+N�]M��]q�]q�NEeD� ?<<<?<M�9/<�++<�.+�}ć.+�}�<<��ıCTX�	4	4 +Y10K�SK�QZX� ���
��� ���88888Yq]++++++!!!!!������y��;9*��M����� ��   U��?>  �@QXYYhii}y�����������88JJFYi:77ww�������	����4����43����4����4� 
t@ @4 @4 3�� t@ @4! /@4!O!XA+N�M�N�]M�+��+ ?��]�++?��++�++10 ]qq]&&#"3267#"  321��cOi}kPf+���������2ST����[o/��&%�   ���S&  �@Wg�	<<KK��t@ 

	& �)@@ $4�����@"$4��p��
&	���@ $4��?<+N�qr+<M�<N]qr+�qr+M�<�< ?<<<?<?�10 ]]!5#"&&5!32665!N:�ik�LR?Hr*�Ub^�����e;Ou����   ����  �@)   #
):JY  	
�@ ��`�����t� �t@	/
/  /_�@(&U?��`����  0x�+N�]qrK�7SK�;QZX� ��8Y<M�<�<�]<�� ?�?<�<�]q�9310]#327#"&&'&5#535%z�''Jb|Lz9	��&��T�+�*3QE1���Ӥ��  J���� ,�@=���(�,+ee(txt(��#Y
UU"Y#hfg!i(g,w��!#���4#���@e4Q"Q#�"�#q"q#�"�#�"�#+
*$"$#94#K
KD"C#je#yz"��"�
��"	
	"#
""#
V@ 4oo��e ��@9- H���@I 40@P`�����@9-*	��@4K'&.'��K�  0  -�S+N�]KSX� @8YM��]�N�M��+r� ?�q+�]+�?�q+�]r+�9]]qr++C\X� "��>#��г>#���9"���9#��ɲ9"���@9 9
 9
 9"���@9 9
9
9+++++++++++++Y�CTX@:
:5"5#K
IC"F#�
�"
 ]Y10 ]q]%32654&'&'&'&54663 &&#"#  J ����=L4��`����}}�I/,8��u�� ��������yQ4I.;Vy�p�f��qc5"94%/fm��~�k   I��.> # 2q@hJHI%��	6FW&fg&�&������')Yw�����4�$21,$@+.4$@"(4$@4o$�$$F���@04= ��,3 @4   U!@?!@?!@4!�t�
,����?,����?,����4,�t@@1&)	(Y��@4O44`  �03)!_�O_o3iA+N�]qrM��q�]N]�+]qrM����< ?�+++?<?�+++�]+�9/]q+�CTX�/qY��CTX� $���4T$d$]+Y]+++9<<<10q] ]q'6632!&'&'#"&546676754&#"3276765e�+�ϼ�K%��H�]��V���LPoKT^6�$7XDLE3�.��Y������L7FF��Z�K% QE;��2'<;V2&7$e  �  7>  �@(�	Sfu/Xhp
	��?O�w@) 

( 		0	p		�_�� &�)@��?� +N�q<M��<N]q�]M� ?<?<?�]qr9210] ]q K�SK�5QZX�
28Y ]!!!6632&#"���CkD`YWG=;R/&�kD5�.A���  �QR& 4�(���@44444���@:4  `��@/(  0`�����"&4���@49@4�'@	@4�'@9 @64  0  Ġ+N�]+M��]+�]+�NEeD�++qrM�� ?�]/?<<<99 9999<10 ++++++]K�SK�:QZX� ��� ��8888YC\X� ��@???���?���?+++++Y!!#"''3267+��#��C%CWPQNB5b^&����]b="�sY   �  ��   w@%��Gg�% % '�����	4��@0`p�   0  ���1S+N�]<M�<Mq�+qM� ?<?<�<9/<�<10 ]q]3! ##326654&'&#��R~�b�Nj����vC^H5��!ݯ��i����`.bAPh
  A��'>  �� ��@F9�	����
�	��HGF
O����
��
���@4@4������?����?��@P`����43 ���� 4 ����")4 ����+-4 ����4 ���@4�     _�t��t@$ !/!O/_o�!@4iA+N�+M�N]�]M��� ?�C\X@@(?@?@?@?++++Y?�C\X� ���(?����?����?����?++++Y�]q+++++C\X�  ���9 ����9 ����	
> ����A!?+ +++Y�+9]C\X@@?@?@?@? ++++Y/<�++r++<310]q ]+# '&5 32 !326&&#"�6���i���@�aBZ'xV\<<R/�����+����}�HlzCCs     Z& @(/4(/4(/4(/4��س/4���@ :4�
	
" -� ���@ 4
  % *4 :� 	�CTX�
���@	4 	 
 ??<9+99@ 

		 
	9���@(40@
?
O

�0@9?O�0 ��@5  @Ġ+N�]+M�]��]NEeD�]+M� ?<?<<<999Y10q+] ]++++++!!6767!��T'�:�!�Z&��E--��   �  b�    , �@?w*hx*��	!	(,!%O0�#"% % 'p�K('�����	4��@!0.@.P.`.p.�.�.�. .0.."   0���-1S+N�]<M�<M]q�+qM��]� ?<�<?<�<9/]qC\X� ���9����9����9+++Y<�<9 910K�SK�QZX�
 8Y] ]!2!3276654&'&#!276654&&#�J���Zo_��]�vJ���(­*LWKJ,Ѫ�+BS@y��\�_g�+'�d�q���	WGDU	���x	]NB\*   �  ��  S� ��@)
?@P�����`��  
& ���@	!$4 ?<+N�+<M�< ?<?<10q]r+3!���F  F�30   ' .@�XgU[fg wuv u-��� �-&&&75-FG-Uvtv-
.!'.-'& (!
" ) ().-
  '&!"wP�V  ���4 ����4 �(����4(����4(�� I�	w�!@(@4@4/?O�
!@4!@4/!?!O!!��Z�
	��"@-��_o?�+@4���/��@w+/++@4+���P0$���@	4$ $$��@���w���@	4 ��@�/@4/�M��+N�+q]M�q+�]q�q+N�qM�+q��qq+9qrrr/<�]< ?<��]++�]++�]�?���++�++�]�99 99999999<<<<<<<<<<10 q]]]%&&546753&'#5&&'%6654&'�ķϬ����a��Ñ��X6;F@A�K^OZ��8㢤�cc��!v*�yAϢ������Pt `:5[�2oKCa   V���    �@Kx
�
���	��	�	VYYVghhg996	6IIE	F�	���	����	� ���@%4�/@4� �O"�!��+N�M�N�qM� ?�+q?�+q10] ]]2#" 76"32676&&2�x��w�����w�3P4O33P4O����_�`��I�����ATm�����@ATl�A  �  �  $@8 
&    0  gv+N�]M� ?M�103!���   ,  ��  r@#/	00P	p	�	�	% 	�-@
 0   �-@Pp����+N�]KQX�@8Y<M�]<�<�]<EeD� ?<?<�<<<10]!!5!!��M��N����>  �  &� 	 V@	k{��)�_�^�	 	 �X  ]@  �
��� +N�]<M�<�< ?<?<�]�910 ]!!56$73&���n0�#�E�$Ɇ   u���  ?�	
�@�8

r&$    0  gv+N�]M��� ?M���9 9910!'667#�*uZ7UH��z�p tbU   M��� ) �@2��{�����������!
 !
�$@O@��@/@4��V� ���@24�'���������O$$+�w� *��+N�M���N�qM��]�9/] ?�+q�?�+q�9/]q�99 999]10q]] ]%32654&#"7654&#"%>32 #"$MrQWwrR6KrxXIHf��m�y�}g�~��������!hn�pj|�iWJXd`,��[�l��s������  3  � ?@_��������CCCV����  (7HCCC$$$&V������  1v������@4     0 @  ����4 ����V@#/@4�	�O  �w��+N�M��N�q<<M� ?�+q�?<�+]q<93+]C\X� ���9����9���@9999++++++Y�CTX@	  99]Y10]KQX� �� �� ��888Yq]]]!6767654&#"%6$32�'��+:eYXh�����GM3��G���	۱?WU^ej{���c�bA�P&   [��5� @) 7EI����	!#� 
��@
 0@P��V� ����4��Z@
/

@4
����@4 0@��@//?O@4��@���@�!@w�� @ � �  ӹG +N�]qM���N�]qM��< ?<�+]q<�]+�+q�?�+q�]q9�.+}�9 9910q]%32654&#"'!!632 #"$[vMXzyay`����,^b�i���� y_o����k!����/��ٵ���  T��a�   �@-YY
YVVY��	�		p�:4:4JDJD�		�t��t@  
)&�)@ �!X<+N�M�Nq�<M��<� ?<?<?�?�10 ]q]CX@ii
iffi]Y!!5#" 32!32654&#"a��A�Z����²��/Dza��gd��[Y'��p�Ln����� ���Q��   �@M& 6�� 	 @ � �  ] _�	&�O3�k !j�<++N�]M�N]q�]<M�< ?�]?<?<�]q<93<<<<10q]!#"&'732665�5�u*a81#+7������˧^�%4��   �  ��  o� ���244����#%4���@?4 @P��`p�� �  � � � �   0 � �  n1�+N�]qr<M�< ?<?<10]qr+++3!�(��F  s���  2@!0@7   0D   0  �l+N�]M�] /�]10!s(���   Y����   �@U����'x	wwx����������-	-'�
 

 

��@ 0@`p�� �'�   0  ���~�+N�]qM�M]q�]qM� ?�?�10]]q ]4766763   !  32654&#"YC2�g��D��~�����~1汱�ݷ�����p�+:�n�����o�h��������   T�Q`> # /N@bw�p1��1 ##033@CC[YY%V)V+Y/k��;3;(3,KDK(D,��
�*'-$����43 ����> ����> ����(*4 ����#%4 ����144 ���@	4`  _�t�'�t�
-�t@*)&�)@	�11��@
 3$!0X<+N�M���Nq�<M��� ?<?�?�?��r++++++�CTX�  ���4 ����	4++Y�+9 9999<10 q]]qCX@iii%g)f+i/]Y ]32767655#"'&5 325!# &5432654&#"yA(Vn7%~��}b�ŀ>p�������`g��he�F'8!1#^��������G��j<����������  �  � @&&���@	:4
 :;4	���:;4	���@�.4
 .4	
�	�
	

	
#, 	/
ghe	j
wx�	�
�	�
�	�
��	�
�	�
���	�
���	�
w	x
���	�
�Xejg	h
vyDKD	K
WW	X

/4:4	;
?		
	�CTX@
	22  P4P4���@4@'4@'4���@'4 
  ?<<?<9++++++]/���9��;@-
	 		2

2

		���8 ���[]4���@ST42@�� �8@  @[]4 @ST4 2��1u+�q�++<�<�q�q<�++�<�q ?<<<?<9�.+�}ć.+�}�+Y10K�SX� �� 88Y]]]]]]qr++++ +q]3!!!!��
�������������F��~��~  �  #� 	�@	�� �?����[]4���@*ST42		@[]4@ST42���@@P`p��� 0	����[]4	���@SS4	2  0 �  ���
1u+N�]<M�++<M]]qr�]<M�++< ?<?<99 99�.++++�}ıCTX� ��@	'4 '4����	4@	4 ++++Y10CX� ���5�5���@=.4S.42@F�������� /4;O���������@	354@354���@/24 /245���@	!.4T!.4���@F 4T 4,';3N@\V	ME�������'(Jx��]qrr+++++++++ ]]qr++++Y ]3!!!� X������-��F��D   �  a�   @3((
Gee*9HYh96���% %'�����	4��@�! !0!!   0��� 1S+N�]<M�<M]q�+qM� ?<�<?<�<10 ]q]!2#!327>54&&'&#��`��`-7fM�b���(�|7H_<<lS>��&���ε��cK*��5VŪ��f   �  ��  �@=%0�	%
	% KH
  0@	   0  ���1S+N�]<M�<N]�]<M�<�< ?<�<?<�<9/]qC\X� ���9����9����9+++Y<�<<<103!!!!!�?���� 3������q�  �  ��  =@P%    0  ���1�+N�]<M�<N�< ?<M�<?<10]3!!�(���I�   �  ��  ! �@�9IWjj�	��#��	


6FF	66Guy�
x	xv�	��		Su��� %`�  !% ��@' �'�����p# #0##!   0  ���"1c+N�]<M�<]q�]��]� ?<<<?<�<9/]q<�<99�.+]}�9 910 ]q]]3!2!.##326654&'&##�o�Հ��`}j����rT^f<��j<OH$���Oʂ��8����?�Y!��N$XBJ[   �����   �� ��@197GVV
VVY�5;;5EKKE��	
 �t��t@ 
!p)&�)@p �  ?A+N�q<M��<�Nq�M� ?<?�?�?<10 q]]CX@ff
ffi]Y ]+3!632 #"&'32654&#"��������[�@4Iy]��ge������������[Y�*�Op�����   #����  Z@$i�T	f	iiiz�
H�-	   ��@p0�

�u+N�]M�Mqq�<M�< ?<?���10 ]]!#"&'%3265�' +��� 0bcR��`�b���� ~4Oq�  �  _�  � �ݳ?���@}-4'	f�
�
�	�
�

S`	FWv�	����NNf}������
++***/KK
	
	

	  


�m@/9e&�   ?{+N�]q<M�<�q���<< ?<<<?<?<9�}�<�CTX� �Ȳ	!4 +Y10]]]q r]++3!!!�IZ�����������v�|�^݉��  U �V�  H@	b0@7b? O  b
��@bO��MC+N�]M�<�<� /]��]�<<10%!!!!!���� ���}}������     �� �@++ 3 @:4����:4����:4����5	���@	4
4���@	4 4���@Y4 4		
 	) %	�
��	�
���
�� �	�
�� �		���
����
��	."/
 ���
��CTX�����!4���@	!4@!4����4���@4d4 	  ?<?<<9++++++99�� ��0�
	 ��2@\      
2

	 		2 
	

		 /�0@
 ��@/�0@  0^c+N�]M�]���]NEeD� ?<<<?<<<<<99999999 9�M.+�}ć.+�}ć.+�}ć.+�}�+++Y10]]]]q++++++ ++++q]!!!!!e��/�`�*������������  �FH��  �  Y�  �@+933BB��	$Xh�t@	


  
&	@ $4�	�		���@"$4��p�� &���@ $4��?<+N�qr+<M�<N]qr+�qr+<M�< ?<?<<<?�999<<10] ]632!4&&#"!���a�O�� Q=Fn3�����Hp����1�Z5D�����   &  D� 
  �@9 9	+Sk��%(H[���	 
 ��@
 @���(  ��   �X��

�@��?�LH +N�q�]M�]<�< ??�<�]<999 99�.+}��CTX@-=M�� ]Y10]] ]+!!533#~��|춶����'���^�����  k�Qh�  F@(�	 	 �" 	 "  �@
	�� 0����k+�]����� ??<<10]#&5673e���cV���g=5#�Q���!����W����f   C�Q@�  I@''
gg
���	  �"   	"  �������jC+������ ??<<10]>543ESD:f����BK��Q����u��/���������   S���  $ 0�04&���@l4����uv�& *6 ;F Lncghw'�'�������'�,�0��w���'��  .�+	�  %.@4?.O..�� ��@4p��(���@	40(@((��@?"O""@4"��@�	w+�O2�w%�1��+N�M���N�qM��� ?�+]?�]+9/]q+�]+9]9] 9]9]10q] q]++&&54632#"'&54632654&#"32654&#"Hmc����j`z���ȅ�v�_OP`_NQ`wYWrtYge.�`��֤f�*1�{��i|�w�QT^_TO_`�=t�}vg}�   W  �  �� ��@14
:8
HV����
! //?O@4�� ���X�/�`@O ��+N�<�q<M�]� ?<?<��+]q<9]10]+!!7W�w��������u�J��0x�  W��*�  # �@;ju�����������6Dz���� �   ���@4�!/!!@4!�?	@	�	�		�O���!@"/@4�� w�O%�$��+N�M�N�qM��� ?�+q�]�]q�+q?�+q9 9]10] ]&&#"632 #"  3232654&#"��
TCY{i���������*����~QNhpTQpSTP��|������Y��d��鉕z���  A���  # �@X;Kez������ ����� ��4VY_R`w���h /@4�! !!���@4!�0	O	�	�		�O���!� ���@4��O%� w�$��+N�M���N�qM� ?�+q�]�]q�+q?�+q9 910q] q]%3267#"54 32  #"&4&#"326]
TEWzj���	������^}RNgpTQoSSP��{�����u�n�����{����  ���$�  �@8		GG	W	V��������� %	 ���@"@P`p� 0��   0����1u+N�]<M�<M]qr�]<M�< ?�?<<<10]q!32665!#"&&'&5�(�|~�(0�خ��~���8Zmg��+����ږYa�U~�   ��l�>   �@.8H4994DIID�	VV
YVVY�� �t��t@!p)&�)@p �  ?A+N�qM�<�<�Nq�M� ?<?�?�?<10] ]CX@ff
iffi]Y ]!6632  #"&'!32654&#"�3�j����X�O���fb��cg�&�Pd��������FU����������       l  �  �  J  �  2  	  	r  
�  (    0  �  �  �     �  �  0  �    �  �  �  �      v  !�  #t  $�  %�  &�  '6  '�  (�  *h  ,�  .�  /�  0b  0�  0�  2"  3  3�  4�  5d  7�  8�  9�  :J  :�  <r  =.  >b  ?�  @�  A�
endstream
endobj
11 0 obj
<<
/Encoding /Identity-H 
/ToUnicode 20 0 R  
/Name /F-1 
/DescendantFonts [21 0 R ] 
/Subtype /Type0 
/Type /Font 
/BaseFont /SUBSET+ArialBoldMT 
>>
endobj
12 0 obj
<<
/Encoding /WinAnsiEncoding 
/Type /Font 
/Subtype /Type1 
/BaseFont /Helvetica 
/Name /Helv 
>>
endobj
24 0 obj
<<
/Length 507 
/Filter /FlateDecode 
>>
stream
x�]�M��0���
��U�'vv%���E�������H%�B8����������aO�l���v2ٷ��q2��k�x�oc�1���,�3M[O�飾T�Y<���/��ԛ�je����u��l�c�d��cǶ;�����̇�0����Mfi�k��ӣ��j�R]��R��������}����^꾉ס��Xu�8��r~��j7��f�����y<տ��o>ڄ���K���#��W�G�1 �X�Ԏ�|'����@O|C����iN�⇴�wk�]BO���l��k�+,e�+/D������R��_G__�{��ͅo(��-���l�8K_ކ���@G_v�8_;����/�t��`�*·�`Η=;��|s*8�:N��W4���p�����)|��o�RB_=��㸅��J���6�%��3*���K_v%|�y�B_�[��x�_ϧN���ծ���bsΗ�����?�c����f��8�+(m��`�������!�����'O
endstream
endobj
25 0 obj
<<
/DW 500 
/FontDescriptor 26 0 R  
/CIDSystemInfo <<
/Registry (Adobe) /Ordering (UCS) /Supplement 0 >>
 
/W [0 [0 833 556 333 500 666 722 556 556 500 556 222 277 666 500 666 556 833 556 556 556 722 666 277 666 556 556 500 222 556 556 277 556 722 556 556 556 610 556 277 500 277 277 556 556 722 943 277 610 556 333 556 666 277 777 666 722 500 889 556 777 666 722 500 500 610]] 
/Name /F-0 
/BaseFont /SUBSET+ArialMT 
/Subtype /CIDFontType2 
/Type /Font 
/CIDToGIDMap /Identity 
>>
endobj
26 0 obj
<<
/ItalicAngle 0 
/Type /FontDescriptor 
/Descent -211 
/FontBBox [-664 -324 2000 1039] 
/FontFile2 27 0 R  
/StemV 0 
/Flags 32 
/FontName /SUBSET+ArialMT 
/MissingWidth 1000 
/Ascent 905 
/CapHeight 715 
>>
endobj
27 0 obj
<<
/Length 45224 
/Length1 45224 
>>
stream
    	 0  `loca1�    ��  fpgm�A H  R  �maxp�         head�     �   6cvt �Q     nprepB 6     /glyf�NI   t  �(hheaD     �   $hmtxA3    �        �^��_<�     ��'*    ք�����g Q   	         >�N C ���z                 B  � �s J� �  !V �� fs Ds �  ?s �� �9 $V��  PV \s K� �s �s Ss V� �V 	9  V �s Us B  � �s �s F9 �s �� �s <s Us � 0s �9   (9 �9 �s Ms a� �� 9 �� �s �� As UV �9  9 cV �    ws I9 XV �� �  7  �� )    B� < �    @ �  �  �T�A,,,"  +* < *��(�&м) �) )�+�'�;@�#�2A-   /      o  �  �   _    � � � �       o � � � A'    � �   / O _ � �   _ o  � �  @��3@���3@��jl2@��a3@��\]2@��WY2@��MQ2@��DI2@��:3@��142@��.B2@��',2@��%2���
2�A �  p �   � �    @�$&2��  d ���2A
��  �� d ����2�AJ� �� �� ���� �  � ?� �� �� �� �� ������ � /� ?� _� �� �� �� �� �   �  � ?� �� � �� � ����Ӳ792���Ӳ+/2���Ӳ%2���Ӳ2���Ӳ2�Ҳ�)�&�;@�" > 3"�%1��<i�� +�A0� ��   � �  � P� `� p�  `� p� �� �� �� ��   � �  �  �  � 0� @� P� в +�ϲ&BA��  ��  ��  ��  ��  �Ʋ A�  � � � /� ��$�A�  � /� ?� O� _� �� �"�dA� �  � �  � � @j@&CI2@ CI2@&:=2@ :=2� �&@&��2@ ��2@&��2@ ��2@&��2@ ��2@&z�2@ z�2@&lv2@ lv2@&dj2@ dj2@&Z_2@ Z_2@&OT2@ OT2���$'7Ok Aw 0w @w Pw www �  ��**��@+)*�����R���e�~���<�^�+���@��8  �@��@��8  �9@�����s�&�%�$� 7@�!�I3@�!�E3@�!�AB2@�!�=>2A! ?! !  �! �! �!  @!� "2@�!�2@�"�*?2@�!�.:2oAJ� � �� ��  /� `� ��  � ?� _� �� �� ��  �"  �"  " /" ?" _" " �"  �! �!  o! ! �!  ! /! ?! O! ��""!!@+H�O�7    ����� 	A	��  ��  ������&�A�  9 &% 8 s 5  4 � 2�V��&,� ��������� ���������/���&��� ���8�ʸ��&���~&���}Gk��e&���^s�@R&ZH�Db@s��?^<&���5��0�+��*V)��#��5UU7�h@,�XO62,!
 ���@+                     J �KKSBK��c Kb ��S#�
QZ�#B�K KTB�8+K��R�7+K�P[X��Y�8+��� TX������CX� ��� (��YY v??>9FD>9FD>9FD>9FD>9F`D>9F`D+++++++++++++++++++++++B��KSX�5��BY�2KSX�5��BYK��S \X���ED���EDYX�>�ERX��>DYYK�VS \X�  �ED� &�EDYX�  ERX�  DYYK��S \X� %�ED� $�EDYX�		 %ERX� %		DYYK�S \X�s$ED�$$EDYX�  sERX� s DYYK�S \X��%ED�%%EDYX�� �ERX� ��DYYK�>S \X�ED�EDYX� ERX� DYYK�VS \X�ED�/EDYX�� ERX� �DYYK�S \X�ED�EDYX�� ERX� �DYY+++++++++++++++++++++++++++++++++++++++++eB++�;Yc\Ee#E`#Ee`#E`��vh��b  �cYEe#E �&`bch �&ae�Y#eD�c#D �;\Ee#E �&`bch �&ae�\#eD�;#D� \ETX�\@eD�;@;E#aDY�GP47Ee#E`#Ee`#E`��vh��b  �4PEe#E �&`bch �&ae�P#eD�4#D �G7Ee#E �&`bch �&ae�7#eD�G#D� 7ETX�7@eD�G@GE#aDY KSBKPX� BYC\X� BY�
CX`!YBp>�CX�;!~� � +Y�#B�#B�CX�-A-A�   +Y�#B�#B�CX�~;!��  +Y�#B�#B +tusu EiDEiDEiDsssstustu++++tu+++++sssssssssssssssssssssssss+++E�@aDst  K�*SK�?QZX�E�@`DY K�:SK�?QZX�E���`DY K�.SK�:QZX�E�@`DY K�.SK�<QZX�		E���`DY++++++++++++++++++u+++++++C\X� ���@t sY�KT�KTZ�C\ZX� �"  sY +ts+s++++++++ssss+++++ ++++++ EiDsEiDsEiDstuEiDsEiDEiDEiDstEiDEiDs+++++s+ +s+tu++++++++++++++stus+stustu+++t+ +++ EiD+\XA6/ A 0/ - -/ 2 2/@&7	7
DD++++++++Y+   @[�tsrqponmlkjihgfeb]XWVUTONA@?>=<;:987543210/.-,+*)('&%$#"! 
	 ,E#F` �&`�&#HH-,E#F#a �&a�&#HH-,E#F`� a �F`�&#HH-,E#F#a� ` �&a� a�&#HH-,E#F`�@a �f`�&#HH-,E#F#a�@` �&a�@a�&#HH-, < <-, E# ��D# �ZQX# ��D#Y ��QX# �MD#Y ��QX# �D#Y!!-,  EhD �` E�Fvh�E`D-,�
C#Ce
-, �
C#C-, �#p�>�#p�E:� -,E�#DE�#D-, E�%Ead�PQXED!!Y-,�Cc#b� #B�+-, E� C`D-,�C�Ce
-, i�@a� � �,���� b`+d#da\X�aY-,E�+�#D�z�-,E�+�#D-,�CX�E�+�#D�z��Ei �#D��� ��QX�+�#D�z�!�z�YY-,-,�%F`�F�@a�H-,KS \X��YX��Y-, �%E�#DE�#DEe#E �%`j �	#B#h�j`a ��� Ry!�@��� E �TX#!�?#YaD� �Ry�@ E �TX#!�?#YaD-,�C#C-,�C#C-,�C#C-,�C#Ce-,�C#Ce-,�C#Ce-,KRXED!!Y-, �%#I�@`� c � RX#�%8#�%e8 �c8!!!!!Y-,K�dQXEi�	C`�:!!!Y-,�%# �� �`#��-,�%# �� �a#��-,�%� ��-, �` < <-, �a < <-,�++�**-, �C�C-,>�**-,5-,v�##p �#E � PX�aY:/-,!!d#d��@ b-,!��QXd#d��  b� @/+Y�`-,!��QXd#d��Ub� �/+Y�`-,d#d��@ b`#!-,�    �&�&�&�&Eh:�-,�    �&�&�&�&Ehe:�-,KS#KQZX E�`D!!Y-,KTX E�`D!!Y-,KS#KQZX8!!Y-,KTX8!!Y-,�CXY-,�CXY-,KT�C\ZX8!!Y-,�C\X�%�%d#dad�QX�%�% F�`H F�`HY
!!!!Y-,�C\X�%�%d#dad�QX�%�% F���`H F���`HY
!!!!Y-,KS#KQZX�:+!!Y-,KS#KQZX�;+!!Y-,KS#KQZ�C\ZX8!!Y-,�KT�&KTZ��
�C\ZX8!!Y-,KRX�%�%I�%�%Ia � TX! C� UX�%�%���8���8Y�@TX C� TX�%���8Y C� TX�%�%���8���8�%���8YYYY!!!!-,F#F`��F# F�`�a���b# #���pE` � PX�a�����F�Y�`h:-,# � P��d� %TX�@�%TX�7C�Y�O+Y#�b+#!#XeY-,�: !T`C-,� B�#�Q�@�SZX�   �TX�C`BY�$�QX�   @�TX�C`B�$�TX� C`B KKRX�C`BY�@  ��TX�C`BY�@  �c� �TX�C`BY�@  c� �TX�C`BY�&�QX�@  c� �TX�@C`BY�@  c� �TX��C`BY�(�QX�@  c� �TX�   C`BYYYYYYY� CTX@
7@:@;@>?�CTX�7@:�  ; �>?��CRX�7@:���;@�  CRX�7@:�� ;@�� CRX�7@:� �;@�7@:�  ; YYY�@  ��U�@  c� �UZX�> ?�> ?YYYBBBBB-,�CTXKS#KQZX8!!Y!!!!Y-,�W+X�KS�&KQZX
8
!!Y!!!!Y-, �CT�#�_#x!� C�V#y!�C#�  \X!!!� GY�� � �#� cVX� cVX!!!�,Y!Y��b \X!!!� Y#��b \X!!!� Y��a���#!-, �CT�#�{#x!� C�r#y!� C��  \X!!!�cY�� � �#� cVX� cVX�&�[�&�&�&!!!!�6 #Y!Y�&#��b \X�\�Z#!#!�Y���b \X!!#!�Y�&�a���#!-,-,�%c� `f�%�  b`#b-,#J�N+-,#J�N+-,#�J#Ed�%d�%ad�5CRX! dY�N+#� PXeY-,#�J#Ed�%d�%ad�5CRX! dY�N+#� PXeY-, �%J�N+�;-, �%J�N+�;-,�%�%��g+�;-,�%�%��h+�;-,�%F�%F`�%.�%�%�& � PX!�j�lY+�%F�%F`a��b � #:# #:-,�%G�%G`�%G��ca�%�%Ic#�%J��c Xb!Y�&F`�F�F`� ca-,�&�%�%�&�n+ � #:# #:-,# �TX!�%�N+��P `Y `` �QX!! �QX! fa�@#a� %P�%�%PZX �%a�SX!� Y!Y�TX fae#!!!� YYY�N+-,�%�%J� SX� ��#��Y�%F fa �&�&I�&�&�p+#ae� ` fa� ae-,�%F � � PX!�N+E#!Yae�%;-,�& � b � c�#a �]`+�%�� 9�X� ]  &cV`+#!  F �N+#a#! � I�N+Y;-,� ]  	%cV`+�%�%�&�m+�]%`+�%�%�%�%�o+� ]  &cV`+ � RX�P+�%�%�%�%�%�q+�8� R�%�RZX�%�%I�%�%I` �@RX!� RX �TX�%�%�%�%I�8�%�%�%�%I�8YYYYY!!!!!-,�%�PX�@  c� �T\�KR[�Y-  � � � &   ��  ��  ���i��� �i���   �   �     � �i � � ��  � � � �  D � | � �  Z � � R R  D ��� / �  � �  W ~ � ��  �� � �  " A P o �L�u \ �� 7 L n p��X������ � ����   c c ������ - \ � � ��	� @ W � �� r �]�g��  ! w �  M ��+ L e �|C�������   ] h � �5G!\�M��  - x � � � � � � � ������  , I  � ������?     ) 9 I o � � �#�o2@z��  1 U W � � ��~~�F�B  � � � � � �/OV)o�r  , 1 1 d i � � � �+��������  & � � � s���C_�����a  ^ m � � �8Q[h|������ATk�hq�BBSs�����X�������2�� Q | � � � � � � � � � � � !U{{~������������  !""#rw�������"+5<Yoq�������22������� ����*��� ����������      < Q a a j x � � � �*>LQ_jqx����������� !".5BOO^eq�����*G]ety���������
"&+G_u���\��
m���6>PQ]���` � � � �            ��E� �3�� - _ dM?  ��}�$x;;N �&����;MKS j1      �   <� ��e�� x~� � 9  �0+� ��� �
��P�>X !� �q} �E  
��+N� � T2�� N � 7� � k� � w � �dg � 3| � ��)n*�i�� �  9$ �]��� u �
 �����M�Rh m } � q�� yX�g V %� � |2! �  r \ / �  � � AM r   LjU � � � � �  x i  W n � �T� ge �  ��R Z�� ��g n�� -�� ��| � � � � ���{ p  � �LF�F�-��S� �              % � � �   >� �� S ?����  ( " � b J � m � � H� 3�N��Fp y� Q���
 h�l O � � a+ ��� � { eR�te�i � � \ @ � u � �q�� � � � � � � � � � �           B����@ � 
� ��1 	�. +�<�<N�<M�< ?<�<�<�<10!!%!!  � ��@ �  �   �  � P��+X�*�@�V*�@ V�CTX� ��@UU���U���@(UU	 	 	
UU����U ���U ����U ����U /+++�/+++� ??�����9++10+++ �CTX@ U U U U U���@#UUUU	U
U����U���@U& 
4 
4  
���U
���U
�V  V@ U U ����U /+++�/�++ ?<?<<9++]10++++++++ +++++@ v��	II)%,X[vx�96OKD@MB
������00RR@	
 	`��� 1� �1�	

�@�V

�@@	V
 @�V � �� A
��  @ V  ��  @�V  p�V� `����;Y+�]�]<�++<���]<�++<���] ??<<<<<<<<��.+�}ć.+�}�10 K�SK�QZX� �� �� ��888YK�SK�(QZ�C�@PZX� ���
88YC\X� �Զ!9,!9��Զ79279��Ե-9,-9++++++Yrq] q]]YY ++@  ?3?3?3??01Y3!67!##�$[05_��V��X���HP���F��5��   J��> ( 7"��+X@,		**)**967:*I*]]*ji*`0��)���(���U'���@U��(��(��(��(D���@UUU5���@OU+,*499,IH,VY+fi+v����+74/$42!_)o))/?���������  @�VU���U���@UUU&�@�V�@�V���,�@@V,

BU� ���@U E'
2)aa A��  @ V  ��  @ V  ��  @@V U %!$���U$���@U$U$���U$����U$���@U$U$����U$�[@'@ && &0&�&9����U&��ִU&���  @�V&19���@#409�9�99����U�@@	V%"/�@�V/�@�V/�@@V/$��?�@�V�@�V�@@.VUUUUUUU18�++++++++++]q�+++��++]q+�+++]��++++++++<�++++�� ?�?�+?��++�9/++++++++]q�q999910 ]++++q]++ q� ++)�-�l'
2�-�l�/�l ?+2/3?+?9/+93901Y%#"&546676767654'&#"'>32#&326765<d�j��GsH5k�g3E�y�nЉ��P	"�b�o\2mih�&�UF��N�N$%
n-=Yqq�K@aJ.x���=8�((M/H`[O=w   �  �> ��+X@;/#4CSft				  
	(�" "�@�V�@�V�@�V% ���@364�     � �  ����U ���@U U U ����U ���@U U U NG�+�++++++++]q+<�+++�]�r� ???�999999 ɇ}�10 ]r]� 
	�6�l ?+22??01Y336632&#"��>i?[^>BB;^&�qH:�'G?`r��   !�Q�& Ű�+X��@�V�@�V�@�V�@�V�@ V ��  @�V�@�V�@�V�@�V�@�V�@�V�@�V�@ V ��  @�V�@ V�CTX@
@ @ U/+���� ???�910����@s9(V�
@@ (04 (04	'''665�((HYYYiiiyvyzz������
�����
�����BU�CTX@D� ???�9]99@7
 %

%

 /��?�@@�T@?@_��B�" E
�T@ @@ 0OP��B�/�?� |f+�q�]q�����]q���]q ?�?<<<�.+}ć.+}� 9�<<�K�SK�QZ�C�@PZX� �� ��88YY+10C\X� �޶79
"79���9"9++++Y]q++ q]+]Y++++++++++++++ +��3@
l

 ???3?+01Y'326767673673#";,<H&�m��+"+��lA$0|V4�g�($k(��u�|vk�ȯBYS   �  R� T��+X@"79	:'
56
G
W��v
��
���@U(����
5�	���@	!4 !4��޳9	���!4���!4���!4����4���@C9	%%=	=*BU	
	
 

	 

  
 �:@0����J�:@0 ������@�V�@�V
�@@V     U ����U ����U ����U ����U ���@
U ];�+�++++++]�+++�]q��]q�<<<< ?<<<?<<<9/�.+}ć.+}�<<K�SK�QZ�C�@PZX� ��8Y�CTX� ��4���@444	4
4 ++++++Y+10+++++++C\X@	"9,9,9"9��޶9"9���@9"9@9��޵%9@9+++++++++++Y +++qr]+ q]++@	

   ????9/39301Y33!!������� �����)��������  f��v� /��+X�cj���U ���@_U  2c p t� �� ������� ��*(* GVWVhk{��������  ��޲(9���@ (9 	&J & �@�V�@�V
�@@
V& �@@VUc\+N�++]M�+++N�]M��� ?�?�910++]]q ]++r@
  �2�l	�2�l ?+?+9/39/301Y#"$54$32&&#"326��=�����כ�C��,;�3��\m憣�1���n��U���-�����銼   D��'>  ���+X�U���U���@eUU
GHVYgi4::5EKKE\\	R]]Rmm	dmmdw	[TT
[lee
l
A��  @ V ��  @ V ��  @@V$@U@U���@UUU���U���U���U���U���@$%40  ���  @�V1����@#40�@�V�@�V�@@AV$ U U U U U U U U @$%4 ?  �@�V �@�V �@�V 147+�+++]+++++++++�+++q+]�+]]++++++++++�+++ ?�?�10q] qC\X@	SS	bb	]Y ++++��/�l�/�l ?+?+01Y7632 #" 32654&#"D����{�������������'�v������������  �  �> 氅+X@���������@"4y���� 
A��  @ V ��  @ V ��  @@V$@U@U(UU���@UU"U���@UU���@U
U���@U@364��N���@464��p���3�@�V�@�V�@�V% ����U ����U ���@U U 
U U ���@U U U ���@364�     � �  N�]q++++++++++<�+++<�<]q+�]q+++++++++++++�+++<< ?<??�9910Cy@	


&
 +++*�]q +]q@	

�0�l ?+2???01Y33632#4&&#"��u�`�P
�*kHs�&��EpM2}�s�nmA����  ?���> 0��+X��@�V�@�VA7@ V (��  @ V '��  @ V &��  @ V %��  @ V $��  @ V #��  @ V "��  @ V !��  @ V  ��  @@|V"":	J	D$V"e"|	�	�$��,�	0K,�U2
\\	\
\\\jj	j
jjj�&�''&$'$)6$Z
Yd&d(t#t$�$�
��(�,�0�
��'�(�&�&(����U"����U#����U$����U(����U"����U#����U$����U���@9Z'%
 &.��@",U?O_��o���U   � ��@U@� ����4���@4.\l����U���U���@U.$@42���@2UUUU U UUUA	@ V [ ��  @�V$*����9�**���U*���U*���U*���U*���  @�V*2���@!'*4`2�2?2�22$ U U  ����U ����U ����U �@@V $UU U���@UUU�@@V"� ? O  147+N�]qM�+++++++�++++++�rN]q+�+++++q+M�+�++++++++++�r ?�+++?�q9/++]qr+��]qr+�99910Cy@@'-#,&"  	(-  !# "#)
('	
+  ++<<+<<+++++*+��� +++++++++]q]rq] ++++++++++++@
 &&.�/�l.�/�l ?+2/3?+939/301Y732654'&'.54676632&&#"#"&?��{|x5%�ƙOA8*�S}�Z�si|j/���Vi�}��=kreD=#%2I�NGy(+H{gR\R7#
$3A|\Z�W�  ����& ���+X� ��@	4 4���@4+$ 
 3A��  @ V ��  @ V ��  @@V%@364@U(UU���@UU���@UU���@UU���@U��N���@464��p����@�V�@�V�@�V%	���@364�	 	 	�	�		����U	���@U	U	
U	���@U	U	U	NGP+�+++++++]q+�+++]q+�]q+++++++++++<�+++� ?�??<99910Cy@   ++**� ]+++� 
�0�l
 ???+2?01Y!5#"&&'&53326653?|�^�O�nQQ�;���HmO5s����1GQS��9��  �  7� ���+X�
�@�V
A@ V ��  @ V  ��  @�V�@�VA@ V ��  @ V  ��  @�V�@�VA@ V ��  @ V  ��  @�V6U����784����454����014����"%4���@%4��O��p��  
% ����784 ���@354� � �     � �  ����U ���@U U 
U U U ����U ����U ���@
U NGP+�+++++++++]qr++<�< ??10]qr++++++++++++++++++� 
  ??01Y33����F   $��*� n��+XA  ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V 
���#&4	���@$#&4� 
 	+
" "�@�V�@�V
�@@"V%�E	E`p��  �������U����U���U����U����U����U���@UU���U�j 6�f+�+++++++++]q���<�+++<��< ?�?<�<9933�10]+++++++��2�l �2@	l

	�-�l
 ?+322/?+?+01Y%#"&&5#5373#32L<bl,�����+(��>e�c�l�����M,  ��  Y�  ���+XA ��  @ V 
��  @ V 	��  @ V ��  @ V ��  @�V�@�V�@�V�@ V ��  @�V�@ V ��  @�V�@ V ��  @�V
�@�V�@�V �@�V�@�V

�@�V
�@�V	�@�V
�@�V�@�VU���U����U���@YU	UU/0gh	`������YVPh����	
		  ���@U  ���@U 	�p@	 �@� @  eRP����@P����@�����+�]q�]q�]q���� ?<�?�<�<�.++}ć.++}�9999����ć����10K�SK�QZ�C�@PZX����  ��8888Yrq]++++++++++++++++++++++++++++��1@l   ?3??9/+01Y#3#!!&'3�Xݫ�����F"3��F��DZ��w��  P���> a��+X� ��  @�V
�@�V	�@�V�@�V�@�V�@ V�CTX@4@ P p  UUUU/++++��� ?�?��]2�]210@G	CCSS``�����
jijup���	�
���"_o��@&0 @ P ` p � � � � 	   A
��  @ V ��  @@V$U"  A
��  @ V  ��  @@V $+ @+�@�V@�@�V@�@�V6�@@ V@U@UHUUI�@�V�@�V�@@!V$�?U
UU�@�V�@�V14�+�+++++]q�+++�++++++++]rKS#KQZX� ��8Y�++r�+�++r ?�?�9/9/]�]�10 ]q]qY++++++@
  �/�l�/�l ?+?+9/39/301Y#" 4632&&#"326<�����r鉭��Z����j����
����kl���  \���� 0A��+XA '��  @ V &��  @ V %��  @�V�@�V�@�VA@ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @�V�@�V�@�V�@@(Vccst%'59CILED$F'SY\W(�#���U$���U%���U&���U'���U#����U$����U%����U&����U'���@FU(&$$'%64#D%E/Z V#U%ljkfeyzz}u$s%������$�%����CTX@-!&&	&)&  )21& e  -y�%-'%%���@U-	 ?�?�+9]99]9]9/�/�/�/�@-%$!%$"-@U�� -���@U P`p���@- BU���@BU-	&J	A��  @ V 	��  @ V 	��  @�V	& ))���U)���@U)2!�@�V!�@�V!�@�V!&&���U����U���@UT   1c[+N�]M�+++��+++N�++]M�+++�� ?�+?�+�]+��]+�99999Y10 ]q++++++++++]q+++++++++++ +++�--�3�l-�3�l ?+?+99//01Y7326654&'&$'&&546632&&#"#"$&\�_�}o�SP\;�lQig~��������98�X�z�������n�WBsDEg#a+7�eo�dí���[O33k(;�vu�st�   K��>  ��+X@ U]]	Ueko	e���U���@RUU'���1:1AMAQ\Ramaxx�� P`p��
 �� ���U���@U�A��  @ V ��  @ V ��  @�V@��ܴU���U���U���@	'*4�����%&4����#40���  @�V3�@�V�@�V�@@V$@$*4?O�@�V�@@+V UUUUUU47+N�++++++++]+M�+++�+Nq++�q++++M�+++ ?��]++�?�9/]<�q<99910] ]+++qr@  P p � � 0 p � � � �   �/@l 0
�/�l
�/�l
 ?+?+9_^]/+3/]q01Y#"  32 !326!&'&#"^�,��������
��c���Q8V�|�V��(���� ��h��Ch�   �  &> #o��+XA� ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ���U����U	���@M4%��	�� ��  #	 	##
�%�%�%%%�UU���@UU���@UUUU����U����U�]��@�V�@�V�@@V%�U���@UU���@UU
U���@UU����U�]� 3#�@�V#�@�V#�@@V#%� � �  ? O  ���@U U U U U ����U ���@U 
U U $%�x�!GP++N�+++++++++]qr<M�+++��+++++++++]�+++�++++++++++]�NEeD�qr ?<<<??<M��99910Cy@& +++�] ]+++++++++++++++++++++++++++@


 
�0�l	�0�l ?+22?+????01Y336632632#4&&#"#4&#"��2�jv�~ʞ��#\>p��XdL�:&�N_bX����'�l_:�����xxP����   �  �� 
��+X�
�@�V �@�V
�@�V �@�V
�@�V �@@!V@4k���	 	�
 ���@
!#40    ���U ���@U U U ���@U U U @4���@!#40 @�<� +N�]q++�+++++++]q+<M�< ??9910] ]+++++++@	@		 ??9/�901Y!#56673��A�T��/t{>|�G�_  S���  # 0ư�+X�CTX� .���@U..!(	U	����U	+���U���U���U���U���U���@U$UUU/+++�/+++�/+++�/++� ?�?�9/+�9910�CTX�	U	����U	+���U���U���U���@"U$UU ..!( ?�?�9/�99/++�/++�/++�/++�10@M5)II&��0	0} }|tqruz� ���������  .�..!(A��  @ V ��  @ V ��  @�Vs�		Ag +��  @ V +��  @ V +��  @@V+s@ #40 ���2�@�V�@�V�@�Vs��g�$�@�V$�@�V$�@�V$s���@!#4 @�1ǋ+�]+�+++�]�+++�]q+�+++�]�+++ ?�?�9]/�999910�C�@PX� "�� ���  /���- &���) 88888888Y]rq qYY� .�/�l(�/�l!�/�l ?+?+9/+9901Y&&54632 #" 54632654&#"32654&#"jpl���km���������b�kh��fg�:I�S�����)�j��ߠf�),Ĉ�� ���Th��_c����M�O�����   V��� +���+X�CTX@@U ���@+U)#


)))#  U &���U&/+�/+�/�/�/ 9??��9/���9�+2�+210@0E�EWvRljduy����
#���@  � ) 5��� h@	)A��  @ V ��  @ V ��  @@Vs_ o  U �A��  @ V ��  @ V ��  @@Vs&@!#40& &&&����U&�-�8���8  ��@!#4  @  �,����+�]+����+]q+�+++�+]�+++ ?�?���9/��]�9910�C�@PX� ���88Y] ]qY@	 #
�/�l)�/�l)�/�l ?+2/3?+9/+3299/301Y732654&#"732654&#"'6632 #"&V��k��}3Ls��ji��!�x�kfd������������|��x}c��� ��g�d_�.������   ���"� ;��+X@
&XX����@44;FJv�� ���	A��  @ V ��  @ V ��  @�V&���U���@UU���@U]  P`p��@�V�@�V
�@�V& 

���@
4
 U
����U
����U
���@U
U
����U
���@
U
];Y+N�++++++++]�+++M]]q�++++M�+++ ?�?<10]+ ]��3�l	  ???+01Y3#"$53326`�d������p�G�}ֶ���������O����b�   	  I� X��+XA ��  @ V ��  @�V�@ V ��  @�V�@ V ��  @�V�@�V�@ V ��  @�V�@ V 	��  @�V�@@*V&))8788	8:57
 !4 !4���!4���!4	���!4���@l!4 !4 !4ww&)(*&6:::5HT]\ZTgejkieuzyzww���
�������������,���@UUU����U�CTX@ 
U���@
U  
 ?<?<99++99@]		 	
	
  	  	 
		 / @�_� 
�
�

���_���@
�@P��_@
  �!`�++N�M�]��]�]�]NEeD�] ?<<<?<<<�M.+�}ć.+�}� 9999�<<ć<<ć<<ć���Y++ ++10] ]++++++++C\X� ��@9"99��޲9��޲9���9"9	����9���@9@9@9<=	<=���@.9"9!= !<
!=!<= <
=<+++++++++++++++++++++++++Yq]q+++++++++++ +� 	 ????01Y33673#&'	7��
S#1C'���+���!1������u?PW��M��-5P�   ��9�  d��+X� �޲9���@ 9���v     
� ����  �z+<��� ?<?<�.+]}�10]++� 	 ??01Y3���X��  �  ��  .��+X@ekKK[[  A��  @ V ��  @ V ��  @�V&���  @@V
UU���@U  �@�V�@�V
�@@V     U ����U ����U ���@U U ����U ���@
U ];\+�+++++++]<�+++<Nq]�++++M�+++ ??<�<9/<�<10] ]��3�l �3�l ?+?9/+01Y3!2!!!2654&'&#!�)�Ml�Y�����{��]L1����e�m������\�   U��!� ��+X��@�V�@�V�@�V�@�V�@�V�@ V�CTX� ��@U
��@ ���U���U/++�/�/ ?�?�9/���+10@4UUKy������	*
���@
@�@����@  �@_o��A��  @ V ��  @ V ��  @@Vs@!#40 ����U� �5 � 8���8  ��@!#4  @  �����+�]+������+]q+�+++�]< ?��]�?�9/]9/]��.+}� 910�C�@PX�	00��� ��8888Yq]++Y++++++@  
�/�l�/�l�3�l ?+?+9/+9/339/01Y732654&#"'!!632 #"&U��l����W�(�����O���t�������Ģ��O?��v\���Ǒ��  B�Q�>  *)��+X@`,%LE	,&,#96JFVXh�
�.#,'>#>'L'�,�,6!6)?,FF!E)T!T)ic!c)`,�,�'�!�#�'���(��@  0 ` p � � �  �}@
E"
3%3
A��  @ V 
��  @ V 
��  @@$V
%�@`�,@U,@UU���@UUU���@UU���U����UA
��  @ V ��  @@Vt% "�@�V�@�V�@@V$����?O�@�V�@@.V UU"UUUU+,t!4P++N�++++++++]qM�+++���++++++++++++]q<�+++��< ?��?��]�?��?<10]q ]q@
    �/�l
"�/�l
(�/�l ?+2??+9?+9/_^]01Y32676'#"5463253#"&32654&#"f�2Ct}�v���nэ�z�e۠�Ꙧ}|��zx�XQ%2dZ7��<ݘ����j��x�*�������     �& 
c��+X� ��  @�VA@ V  ��  @ V ��  @�VA@ V  ��  @ V ��  @�V�@ V�CTX@ 

 	$U/+����33 ???910�5 "9
���@9	44���4���4
���@	!4 (!4
���@	"%4 "%4
���@~(.4  (.4) (	&
9 5
H G
VVYX	ffii	x wwyx	w
������	� �	�
� �
� ��
� �
� �
� �
� �
,
 
 
( &
7
O @
	@4@4�CTX@	  
���@U
 U 	���@UU9/�+��+��+�+ /??910@7
%	
		
 %  

 
	
	 /"@@@	�		��@��@	 @"��+���]�]��]9999 ?<<<?<9�.+�}ć.+�}�Y10 ++q]++++++++++++ ]Y++++++++� 
 ???301Y!3673��l��%+��n&��goTv���  �  <�  
��+X�
�@�V
�@�V
�@�V
A@ V ��  @ V  ��  @ V ��  @ V ��  @�V�@�V�@�V�@�VA@ V ��  @ V  ��  @ V ��  @ V ��  @�V�@�V�@�V�@�VA@ V ��  @ V  ��  @ V ��  @ V ��  @@7V	6UO	�	�	�	�	�	�	 		p	�	�	�	�	�	�	�	
	 	���  @@*V~ 
% �������  ������U���@UU
UU���U����U���@
UNGP+�++++++++]qr<�< ??<?�+999910]rq+++++++++++++++++++++++++�
 @  ?�??01Y533��������&��  ����  ��+X@{$5E?�"3Bp�:<<LL]]X]^jlhnn���������� //0?@LPf��� 
A��  @ V ��  @ V ��  @@"V$�@`�@UUU����U���U����U���U���@Ut�@�V�@�V3 �@�V �@@V U U 3�@�V�@@V%�����?O����U���@UUUUU����U���@UUUG7+N�++++++++++]qr<M�++�++++�++�++++++++]q�+++ ?�??�?9910 ]]qr q�
�/�l�/�l  ??+9?+2?01Y!#3632 #"'32654&#"-��r�b�q@��k4U�v��uv�����O��s���֝��U������  F����  ��+X@|
%4D55WT
RSgde	c`�����������+<<Kp�.$.:5KEFIW
Vg����  
A
��  @ V ��  @�V3 ���  @�V %A��  @ V ��  @ V ��  @@$V%�@`�@U@UU���@UUU���@UU���U����U���  @�Vt�@�V�@�V�@�V$�@�V�@@;V����?OUUUUUU4P+N�++++++]q++M�+++�+++++++++++]q<�+++�+<�++ ?�?<?�?<9910 ]q] q��/@
l 
�/�l  ??+?39?+01Y!5#"&&54632332654&#"8e��ujԃ`�/�� �uv��{x��������QA�F�������   �  �&   N��+X@  	<<
</ ?    ���+�]q� ??��999910� @ /�?�01Y5353����Y������  �  �� ɰ�+X� ���4���@U%5E����@4 
A��  @ V ��  @ V ��  @@'V%	@364�	�	@U@U	(U	U	���@U	U	U	���@U	U	���@U	
U	����U	N���@464��p����@�V�@�V�@�V% ���@364�     � �  ����U ���@U U U U ���@U U U NGP+�++++++++]q+<�+++<]q+�++++++++++++]q+�+++ ?<?�?99910Cy@% +++� +]++�
 
�0�l  ??+9??01Y33632#4&#"��~�v�K�ukP�<���]���_��{S�}��  �  Z�  N��+X@ C A��  @ V ��  @ V ��  @@V& 	@U	 U	
U	U	���@U	�@�V
�@�V�@@V     U ����U ����U ����U ����U ���@
U ];\+�++++++]<�+++<�+++++]�+++ ?<�<?<�<10Cy@6


!!!
! ++++****�]� �3�l �3�l ?+?+01Y3!2#%!2676654&'&#!���Z~YtsNz�ͅ��9��1EM�lN����Lb��ħ���a2�61E���*   <  � '��+X�CTX@	U����U���@	U���@UUUU��@
  9/��9/� /�++++?�+++�210�CTX@	U���@	U���@UU���
���U���@U  9/��9/++� /�++?�++�210@G;;�����IYTkdzz�������
����O�� ���
A��  @ V 
��  @ V 
��  @@V
s�  @!#4��   8@�?_o�$ ���+�]���+<��+++ ?<�<?��]�99�.+}�910�C�@PX@	��� �� �� 	�� 88888888Y ]]rYY@	�3�l�/�l ?+?+939/01Y%!&76676654&#"'6632�7%��神{�������H�¢\��A<c�~��fk������X����a1  U���  ���+X�CTX@
	���U	���@U	 U U U /+++�/++� ?�?�10�CTX@
	����U	���U	���@U	 U U U /+++�/+++� ?�?�10@N����	ELJCT\\Rkkclk`ywvz��������A��  @ V ��  @ V ��  @@Vs	@!#40	 			A
��  @ V 	��  @�V	��@�V�@�V�@�Vs ���@!#4  @  �@�V �@�V �@�V �ǋ+�+++]+�+++�++]q+�+++ ?�?�10]q ]�C�@PX� ��� ��� �� �� �� 88888888YYY��/�l�/�l ?+?+01Y632#"'&326&#"UkӠv�tBjӡ�y���||��~|J]�=�_�������í�������hj�i�    � 
 ��+X� ��  @�V�@�V�@�V�@�V	�@�V
�@�V�@�V�@�V	�@�V
�@�V�@�V�@�V�@�V�@�V�@�V�@�V�@�V�@�V	�@�V
�@@7VXh���LL� 
 � ��  �@
   �
�f�
@4
���U
���U
���U
�7@@"#4�!5����@4  ���U���U�����+�++]+�++�++++<��< ??�<�<9999�.+}�10C\X� �޲9���@39"-9<++++Y] ]C\X@@9�P9@&9"9@-9+++++Y+++++++++++++++++++ +�	�2�l  ??9/+332901Y!!533#������ƴ�5_���J�����k  0  �� ��+X��@�V�@�V�@�VA@ V ��  @ V  ��  @�V�@�VA@ V ��  @ V  ��  @@V 	�s� �� /��   ���@U U ���U ���U ����U ����U �s���+�++++++]<�]<��]�<< ??<�<10++++++++++� �3�l ?+2?01Y!!5!!�������   ��i!>  հ�+X@t-=K? �  )#22Bp � ::JJY[\\jkimk� ������� � #++5:FJZ��� A��  @ V ��  @ V ��  @@V$�

@
`
�
 @U @U
���@U
U
����U
���U
����U
���@U
t33�@�V�@�V�@@V%  �����?O���@UUUUU����U���@UUUG7+N�+++++++++]qr<M�+++���++++++++]q�+++ ??�??�9910 ]]qr q� �/�l�-�l ?+2??+9?01Y36632#"&'32654&#"��:�h��ju�{Z�.�vx��ts��i��QQ�������L:����������    �� ^��+X@	/0@p���(�����@4
+ 
���@�V@�@�V�@�V�@@V% � ����184 ���@+4� @U@U U (U "U ,U ���@U U ���U ���U ����U ��� ! �
 ++�+++++++++++]++<�<<�+++�+�] ??<<<�<?�9910Cy@		 ++*��+q] r� 
�-�l
�2�l
 ?+?+32?01Y3#535476632&#"3#����vL\82RD����qk4FW�
F`b��f   (  �& +X��@ V ��  @@V��24���@	4>!4���@J!4)(	/99
IFFI	O\TTZ	Plccj	{t{	���	��&)+	9������4,9	���@#9:	


%a+
a ���@	U+
���[   ��@U"� @`�����@$Ut 
~� O o �  U t!|�++N�+]q<M��+]q<�+�<<� ?�+<�?<��99�.+�}��+10+++q] ++++C\X�)&���@	424��·!4>!4 ++++qY]C\X� �޲9	��޲9	���9	=	���9	���@
999++++++++Y ++�
 �0�l 
�/�l ?+3?+2201Y35#!5!63!(�sX�Od��oyj��w�^{	�  �  �� P��+X��@�V�@�V�@�VA@ V ��  @ V  ��  @�V�@�VA@ V ��  @ V  ��  @�V ����8=4����344����-04����()4����#%4����4����4���@*4 ��   � � � / @ P � �   � � ���@U U ���U ���U ���@U  U ��Y+�++++++]C\X�� ]Yqr<�]++++++++< ??10++++++++++�  ??01Y33����F  �  � �  7��+X@< 
<_ o  � �  ���+�]]� ?�10�@  ?�01Y353����   M���  *鰅+X�CTX@_(@"
 %���@UUUU/+++�/+���� ?�?�9/]��]10@-kD@DD ZT kddjd tu���� U'���U#���@U! U(@P�_  �h@	"�8� �%A��  @ V %��  @ V %��  @@V%s@!#40 ���U�,
�8��@�V�@�V�@ V 9@?_o�@�V�@@VUU�$�+ǋ+�++++]�+++��+]q+�+++�� ?�?��]�9/]�10�C�@PX� ��' # !���8888Y++++] ]Y�
(�/�l"�/�l�/�l ?+?+9/+29/01Y&'&#"6632#" 763232654&#"��,IkVAUbA�g��wЄ��䝉���7O�Nr��{z�Sj0M0>��c`��Ҋ�~K|������]�Y�����  a  �  ���+X@�	 ��@0	s@!#4O_os	� O__?_o����+N�]q<M��N�q+<M� ??<�<99910q]�	 �3�l ?+3?01Y5! #67a����K6�����������ۭ�ǜ  �  � 	��+X��@ V ��  @�V���@
4U���U���@#BUBU 		A��  @ V ��  @ V ��  @�V ���U���@UU���@U]  P`p�	�@�V	
�@�V	  ���@4    U ����U ����U ���@U U ����U ���@
U ]
;Y+�+++++++]+<�++<]q�++++<�+++< ?<?<9999�.+�}ıCTX� ��4 4 ++Y++10+++C\X�@F9����F9@29����29"9��޶9"29��޶29"#9���@#999����99����99����9+++++++++++++ ++++Y ++@   ????9901Y333#����������F���    v� ���+X� ��  @�VA@ V ��  @ V ��  @�VA@ V ��  @ V ��  @�V�@�V
�@�V�@�V�@�V�@�VA@ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @@3V) &)&9 696I GIGX WXW��BUBU�CTX@3+44DDKTT[ddktt{   ?????9]99@
	��<�  ��<� ��<@Z	     		 	 		 A	Q   Q Q @ Q�  ����+N�]M����NEeD� ?<<<?<<<<<999999999�M.+�}ć.+�}ć.+�}ć.+�}�+++��ć<ć�ć�ć�ć��K�SK�QZ�C�@PZX�
���88YK�%SK�*QZ�C�@PZX�  ��8Y K�SK�QZ�C�@PZX�@@88YY++10r] ++++++++++++++++++@  ?3???3?301Y!3673673#&'��{��$8
��O#-���n���'����?���$�������F]� eG��  ���� � 
 d��+X�
 ��P@&<
< 
< 8:O _ o  �  ���+�]���<< ?�<<���910�@  ?�/�01Y353'667��PW296��q�&Ma[  �  �� 	 Ӱ�+X@"�  �  	�@�V	�@�V	
�@@V	     U ����U ����U ���@U U ����U ���@
U ]
;\+N�+++++++]<M�+++<N�]M� ??<�<9/]<�<10��3�l �3�l ?+?9/+01Y3!!!!������P���:��f  �  *�  ���+X@  ����@�V�@�V
�@@V     U ����U ����U ����U ����U ���@
U ];\+�++++++]<�+++<�] ?<�<?10� �3�l  ??+01Y33!������   A�jm  =��+X@ppMM# p  p�+N�]� /M�10 q]� @ /�01Y5!A)���  U���  *Z��+X�CTX� %����U����U���@(UUU,+(O P���@U" ?�?��+]29/]�299/++/+++�����10�CTX� %���U���@*UU,+(O P" ?�?��]29/]�299/+/++�����10@G:L@#[W#flmg#z}������� � =��:)d(O_"�P  �h�A'��  @ V ��  @ V ��  @ V 9 ��  @ V ��  @ V ��  @ V 8@@!#40 �,�8� �%�@�V%�@�V%�@�V%s���@!#4 @�+ǋ+�]+�+++���]q+�+++�+++ ?��]�?�9/]�10�C�@PX� '�� #��!  8888Y ]q]YY�(�/�l�/�l"�/�l ?+?+9/+29/01Y732>54'#"54 32#"&4&#"326p�|aS}P66�m��Ə�{z��˥tx��|}�SznL�pVk�������������4��Ĝ���   �  ��   *ް�+X� ��@)UF#V#f#s	�	iup	s��'	'*	A��  @ V 	��  @ V 	��  @@V		**))  A��  @ V ��  @ V ��  @@
V&U���@%UUUUUUT%A��  @ V %��  @ V %��  @@V%&U
U���@U,�@�V�@�V
�@@V     U ����U ����U ����U ����U ���@
U ]+;\+�++++++]<�+++<N�+++M�+++�+++++++�+++ ?<�<?<�<9/<�<9/+++99910] ]+�	*�3�l �3�l �3�l ?+?+9/+901Y3!2#!276654&&#!!27>54&&#!�&��sfg��W�����=�8JKF����m^&CZ:T�����Y�e^�3'��g�`1RfMIo)��8kFRy1  c����  T��+X@K��� @OO@XX	WU_Z_VW��	A��  @ V ��  @ V ��  @�V& ���  @ V ��U���U���U���U����U���@U��@�V�@�V
�@@
V&   �@�V �@@V U U c\+N�++++]M�+++N]�+++++++]M�+++ ?�?�10]q ]]]q��2�l	�2�l ?+?+01Y !2#"$7 32 4&#" c�6�F������������y�����m����������Z�����4����    F� `��+X��@�VA@ V ��  @ V  ��  @�V�@�VA@ V ��  @ V  ��  @�VA@ V ��  @ V ��  @ V 	��  @�V�@�V�@�VA@ V ��  @ V  ��  @�V	:;	���4���@444	��س!4���@;!4(!4&)*
/hhh�			
U	 


	���@U  �@	

	 �@		R@
�

��@  RO���@	 U ���@U U ���U ���!`�++�++++<�]��<�]�� ??<<<�<99�.++}��.++}ć�ć��K�SK�QZ�C�@PZX�	��� ��8888Y10 ]]C\X@		"9"9��ޱ9+++Y++++++++++++++++++++++++++��2@
l 	 ???9/+301Y!3673;���!PEB^���mM�F||s������     �& �  ��  @�V�@ V ��  @�V�@�V�@�V�@�VA@ V ��  @ V  ��  @�V�@�VA@ V 	��  @ V ��  @�VA@ V ��  @ V ��  @�V�@ V ��  @�V�@�V�@�VA@ V 	��  @ V ��  @�VA@ V ��  @ V ��  @�VA@ V 
��  @ V ��  @�V"A@ V 
��  @ V ��  @�V �@�V"A@ V 
��  @ V ��  @ V�CTX� ��@UU U
��ԴU���@U U
����U���@/U@U
 
 
U

U����U/++�����+� ?????910 +++++++++@*)
J[� U
���U���U���@	!4'4	���@�$4		 	 $ %*+4 5:;DG@MKCGJ[Rkdgyzt�����	(( ('('/8 7w�������� �����	�����	UUUUU�CTX@
 %%%  %���@7U%*U
&
+TR
\l|�

 
 
 ?????9]99/+�/+�9���999@	


��K�  ��I@f
 � +
%+


 %   

 
�`p���@
 O
o


�U@	Oo�U@`p������f+N�M�]]�]q�]q�]]� ?<<<?<<<<<999999999�M.+�}ć.+�}ć.+�}ć.+�}�+++��<<�ć�K�S�C�@PZX�  ��� �� �д 0 ���88888888YK�4S�C�@PZX� �б088YK�!SK�3QZ�C�@PZX� �� 88YK�SK�QZ�C�@PZX� �ж   ��в0��� 8��� ��8888888888YK�SK�QZ�C�@PZX� ��
   888YY10C\X� �Զ9 ,9 ��Ա9+++Y+++++]qr+++ +++q]]Y ++++++++++++++++++++++++++++++++++++!367373#'K����?3���5=������)�&����n����f��|���     �& +��+X� ��  @�V�@ V 	��  @�V�@ V�CTX@	
 
U/+ ????910�"9���@P9Z��������	@9	5:��/WYYX��
��������	���
�CTX@ U���@U  

 ?<?<99++99@f			 	

� �	% 	  	�%
		 
OI~"
a	~@
��@P��C@ ~"O  I|�+�]���]������] ?<<<?<<<�.+]�}ć.+]}� 99�ć�ć���<<<Y10C\X�9���@9"9"9��޲!9���@
9"!9	@9++++++++Y]q +]++]Y++++@ 
 
	 ????9901Y336773#'����.,%�������:��(��G0B3����JY�]   w����    ' 38��+X@
��h��@1+�� 	e �@%(�� e .��%�� +  1��"�5��   �@	   u4WZ+�]������� ?���<<?<<���9999�.+}�10Cy@R3)+ 3 1-&+ /$1 
 *(2!(,'. 0#.    ++++++++++++++++�]�(�e�%	�e@.% ?3??33/�2�201Y4632#"&"32654&34632#"&"32654&w��������9CYZBDYZB"���垗������:DYZBEYZZ��ſ����t��st��s�s	�����ſ����t��tt��s   I�-A * 1 82��+X@%|0,66/F!U!P/]6jc/zw!s/{6�!�/�61��޷9  $4,���@, #4j8*7 *0! 710! 7!00�770!72���P��� ���+�5@
� *�7�
2�5�)��8 ��5s&���@
90&@&�&&�R@*  8822))*��@ ++11

0 @ � �  �@	.so�� 8@?O�9ǋ+N�]M��q��]<<<<<<�<<<<<<<�]+��� ?��<�<?<�<�����]�9�.+�}�10Cy@J!7$%#%"%&7!5O3(5O,.O 0.O 6%8O! 784'2O 32-+O,+/1O 01 <<+<<+<+<<+++++*+*��++ +]]@ 81@+  )2�/�l)
�/@	l�/�l+�/�l ?+33/+2/3/?+2/3?+3/9/�3201Y5.'7&'&&5476753&&'6654&'���{
�5LjotV]�[�j�\v�eX�,Tj9�jiyg{ji�a�ӴW"�D`=A0�l�wPVVMb�jq��"%j�U��	�(�]\|%��sbw/   X����  (��+X@�_&�&7##*-+&;<:&LLI&]U#X&o{z��� �� �� �� ��+ *;]��&�&%*&49&IIEE#K&VXUZZVW W"ifk&{&��&��&��Բ9 ���@09*:((& !(& $$	A��  @ V ��  @ V ��  @@
V&U���U���U���U����U���@UJ *�**!�@�V!�@�V!
�@@
V!& �@@VUU)c\+N�+++]M�+++N]�M�++++++�+++ ?�??�9999 3��]10++]] rq]]qr@  &&$($@$�2�l	�2�l ?+?+3/�9/�939301Y%&'#"$54$32%64&#"  327&'��r9���������E��F�n��m�y�����h\[e�]+�9{[�\��d����ڵ�ߍ/]�9�
���������';   �  ��  ���+X@ 
	 ���@4TJ 
 
	�@�V	�@�V	
�@@V	     U ����U ����U ����U ����		U ����U ���@
U ];[+N�+++++++]<M�+++<N�]M��+ ?<�<?<�<9/<�<10��3�l 	�3�l �3�l ?+?+9/+01Y3!!!!!�$��+������?���   �  ��  "��+X@!6Zfm	UUU$����U����U����U����U���4���"'4���'4���'4���'4��س&4���4���4���@I4%JJ S\mr	xy�
������ 	!
		���  @ V ��@U !" A��  @ V ��  @ V ��  @�V&����U����U���@UU] $p$�$$"�@�V�@�V
�@@V     U ����U ����U ���@U U ����U ���@
U ]#;�+N�+++++++]<M�+++<]�++++��+++ ?<<<?<�<9/++�<<9/99�.+}�10]+++++++++++++ +++]C\X@
@9::+++YqC\X� ��@9"9"9@9"9"9"9+++++++Y�	�2@l  "�2�l ?+??9/+901Y3!2#.'&##!26654&#!����z��M(UL���UnW-!K����N���0�O�y��%$Nu�q1��8�u37yGh�  7��a� ��+X@egtu��	����U��		A��  @ V 	��  @ V 	��  @�V	&

A��  @ V ��  @ V ��  @�V&���U���U����U���U���@U]  @P`& ���U ���U ���@
U K�Y+�+++�]q�+++++�+++<�+++ ?��+?10 ]� 	�3�l		 ??+9/301Y7326653#"&;�pcIj(�Y������|Cs~����j�   �  �� ��+X�A@ V 	��  @ V ��  @ V ��  @�V�@�V�@�V�@@VUVZ	��	U����U
����U	����U���@UUw
 !4���'4	���'4���!4	���@�'47	G%-
X
wu
���#&%98	?OYYXY	}y�	�������

		

	%%


	  
�@	U"�@ ?U��@�V�@�V�@�V% �@�V�@�V�@@V%� ? O  ���@1U U U 
U U U U �!Gf++N�+++++++]q<M�+++�+++Nq�+]M��+� ?<<<?<?<9�.+}ć.+}�<<<<�CTX@K		�	4 +]qY10C\X@
	,9	<��޲9��Բ 9��Ա!9+++++Y] q]q ++C\X� ���!9����9��޲9��޲9��޲9��ޱ9++++++Y+++C\X@�9	<	<����9���9+++++]Y ]+++++]q++++++ ++@
	 
 
  ????901Y333#�����j���������v�dz�[  )  �� S��+X� ��  @�V	�@�V
�@�V���@4HGH	
	�CTX@  ?�<?��99@+�	


&!4(
�

 
(4(4��س4���@4

 
��  �@ 0@J? Q ��+N�M�<<N�]<M�q<�� ?<�<?<�<<9++++�.+]q+�}�ć��rY10q]+C\X@	"!9!9	��޵9"9++++Y++ +� 
�3�l �3�l ?+2?+201Y3567!5!!)�PH����Y���dJ���g�        l    �  	  4  �  V  �  �  �  �  (  �  !�  $h  (>  *�  .�  /�  3,  5�  7*  :�  ;X  <�  ?D  A�  D�  F�  I$  K�  L  N  O�  RP  T�  W
  XF  Z|  \"  ^H  _�  _�  bn  c4  eb  h�  iJ  jF  k  k^  n>  p�  p�  r^  t�  {4  }�  �  �f  ��  �  �   �X  ��  �(
endstream
endobj
10 0 obj
<<
/Encoding /Identity-H 
/ToUnicode 24 0 R  
/Name /F-0 
/DescendantFonts [25 0 R ] 
/Subtype /Type0 
/Type /Font 
/BaseFont /SUBSET+ArialMT 
>>
endobj
28 0 obj
<<
/ModDate (D:20250109195255) 
/CreationDate (D:20250109195255) 
/Producer (Ibex PDF Creator 4.7.3.0/7447 [.NET 3.5]/R) 
>>
endobj
xref
0 29
0000000000 65535 f 
0000008363 00000 n 
0000007446 00000 n 
0000011204 00000 n 
0000008497 00000 n 
0000008532 00000 n 
0000006846 00000 n 
0000007363 00000 n 
0000007528 00000 n 
0000000020 00000 n 
0000085034 00000 n 
0000038151 00000 n 
0000038317 00000 n 
0000007103 00000 n 
0000007871 00000 n 
0000002117 00000 n 
0000007506 00000 n 
0000008325 00000 n 
0000008214 00000 n 
0000008266 00000 n 
0000011225 00000 n 
0000011775 00000 n 
0000012246 00000 n 
0000012476 00000 n 
0000038432 00000 n 
0000039014 00000 n 
0000039513 00000 n 
0000039739 00000 n 
0000085196 00000 n 
trailer
<<
/Size 29 
/Info 28 0 R  
/Root 1 0 R 
>>
startxref
85337
%%EOF
```

## uploaded_files/2882UQ_document.pdf

```pdf
%PDF-1.7
3 0 obj
<</Type /Page
/Parent 1 0 R
/MediaBox [0 0 612.00 792.00]
/Resources 2 0 R
/Contents 4 0 R>>
endobj
4 0 obj
<</Filter /FlateDecode /Length 422>>
stream
x��UMO�@��x'������=!"B����p�@%�������4���f�o����m�a�A������^������C힁1�Rx�hy��5�;D���*$	{�����'np�/�I��|hL������)�n�t6=�=� Rr��Dr���oB�}t�?�I����J"�[4��_D��Lq:�!����d��#΅vVk�o�kp��X�SnTd�g�%�QơPӍ��]����9��2��FN[d�]!%[2w�;�n��F�����,c2(�3��4��4Uќt�w}Z�q��x,�<����W�VSw�dn&�1	�ln:�c�n���V2��d�?�2�h !�b6�ƞh6mo$f�_�I�Pd����Ӗ�Q�N�r}E�Z�vM�n�^�16yj����3�uCJC������ȔO� �w�
endstream
endobj
1 0 obj
<</Type /Pages
/Kids [
3 0 R
]
/Count 1
>>
endobj
5 0 obj
<</Type /OCG /Name (�� p r i n t)
/Usage <</Print <</PrintState /ON>> /View <</ViewState /OFF>>>>>>
endobj
6 0 obj
<</Type /OCG /Name (�� v i e w)
/Usage <</Print <</PrintState /OFF>> /View <</ViewState /ON>>>>>>
endobj
7 0 obj
<</Type /Font
/Subtype /Type1
/BaseFont /Helvetica
/Name /F1
/Encoding /WinAnsiEncoding
>>
endobj
2 0 obj
<<
/ProcSet [/PDF /Text /ImageB /ImageC /ImageI]
/Font <<
/F1 7 0 R
>>
/XObject <<
>>
/Properties <</OC1 5 0 R /OC2 6 0 R>>
/ExtGState <<
>>
>>
endobj
8 0 obj
<<
/Title (�� I n f o r m e   d e   V a l o r a c i & o a c u t e ; n   d e l   I n v e n t a r i o)
/Author (�� W e b E R P   4 . 0 0 R C 1)
/Subject (�� V a l o r a c i & o a c u t e ; n   d e l   I n v e n t a r i o)
/Creator (�� T C P D F)
/Producer (�� T C P D F   4 . 9 . 0 1 4   \( h t t p : / / w w w . t c p d f . o r g \)   \( T C P D F \))
/CreationDate (D:20241126063044-06'00')
/ModDate (D:20241126063044-06'00')
>>
endobj
9 0 obj
<<
/Type /Catalog
/Pages 1 0 R
/OpenAction [3 0 R /FitH null]
/PageLayout /SinglePage
/PageMode /UseNone
/Names <<
>>
/ViewerPreferences<<
/Direction /L2R
>>
/OCProperties <</OCGs [5 0 R 6 0 R] /D <</ON [5 0 R] /OFF [6 0 R] /AS [<</Event /Print /OCGs [5 0 R 6 0 R] /Category [/Print]>> <</Event /View /OCGs [5 0 R 6 0 R] /Category [/View]>>]>>>>
>>
endobj
xref
0 10
0000000000 65535 f 
0000000609 00000 n 
0000001001 00000 n 
0000000009 00000 n 
0000000117 00000 n 
0000000667 00000 n 
0000000782 00000 n 
0000000895 00000 n 
0000001160 00000 n 
0000001604 00000 n 
trailer
<<
/Size 10
/Root 9 0 R
/Info 8 0 R
>>
startxref
1968
%%EOF
```

## uploaded_files/6613QL_document.pdf

```pdf
%PDF-1.7
3 0 obj
<</Type /Page
/Parent 1 0 R
/MediaBox [0 0 612.00 792.00]
/Resources 2 0 R
/Contents 4 0 R>>
endobj
4 0 obj
<</Filter /FlateDecode /Length 422>>
stream
x��UMO�@��x'������=!"B����p�@%�������4���f�o����m�a�A������^������C힁1�Rx�hy��5�;D���*$	{�����'np�/�I��|hL������)�n�t6=�=� Rr��Dr���oB�}t�?�I����J"�[4��_D��Lq:�!����d��#΅vVk�o�kp��X�SnTd�g�%�QơPӍ��]����9��2��FN[d�]!%[2w�;�n��F�����,c2(�3��4��4Uќt�w}Z�q��x,�<����W�VSw�dn&�1	�ln:�c�n���V2��d�?�2�h !�b6�ƞh6mo$f�_�I�Pd����Ӗ�Q�N�r}E�Z�vM�n�^�16yj����3�uCJC������ȔO� �w�
endstream
endobj
1 0 obj
<</Type /Pages
/Kids [
3 0 R
]
/Count 1
>>
endobj
5 0 obj
<</Type /OCG /Name (�� p r i n t)
/Usage <</Print <</PrintState /ON>> /View <</ViewState /OFF>>>>>>
endobj
6 0 obj
<</Type /OCG /Name (�� v i e w)
/Usage <</Print <</PrintState /OFF>> /View <</ViewState /ON>>>>>>
endobj
7 0 obj
<</Type /Font
/Subtype /Type1
/BaseFont /Helvetica
/Name /F1
/Encoding /WinAnsiEncoding
>>
endobj
2 0 obj
<<
/ProcSet [/PDF /Text /ImageB /ImageC /ImageI]
/Font <<
/F1 7 0 R
>>
/XObject <<
>>
/Properties <</OC1 5 0 R /OC2 6 0 R>>
/ExtGState <<
>>
>>
endobj
8 0 obj
<<
/Title (�� I n f o r m e   d e   V a l o r a c i & o a c u t e ; n   d e l   I n v e n t a r i o)
/Author (�� W e b E R P   4 . 0 0 R C 1)
/Subject (�� V a l o r a c i & o a c u t e ; n   d e l   I n v e n t a r i o)
/Creator (�� T C P D F)
/Producer (�� T C P D F   4 . 9 . 0 1 4   \( h t t p : / / w w w . t c p d f . o r g \)   \( T C P D F \))
/CreationDate (D:20241126063044-06'00')
/ModDate (D:20241126063044-06'00')
>>
endobj
9 0 obj
<<
/Type /Catalog
/Pages 1 0 R
/OpenAction [3 0 R /FitH null]
/PageLayout /SinglePage
/PageMode /UseNone
/Names <<
>>
/ViewerPreferences<<
/Direction /L2R
>>
/OCProperties <</OCGs [5 0 R 6 0 R] /D <</ON [5 0 R] /OFF [6 0 R] /AS [<</Event /Print /OCGs [5 0 R 6 0 R] /Category [/Print]>> <</Event /View /OCGs [5 0 R 6 0 R] /Category [/View]>>]>>>>
>>
endobj
xref
0 10
0000000000 65535 f 
0000000609 00000 n 
0000001001 00000 n 
0000000009 00000 n 
0000000117 00000 n 
0000000667 00000 n 
0000000782 00000 n 
0000000895 00000 n 
0000001160 00000 n 
0000001604 00000 n 
trailer
<<
/Size 10
/Root 9 0 R
/Info 8 0 R
>>
startxref
1968
%%EOF
```

## uploaded_files/6619QL_document.pdf

```pdf
%PDF-1.4
%ÈÁÄ×
9 0 obj
<<
/Length 2026 
/Filter /FlateDecode 
>>
stream
x��Z�n�6��S��%���"@��-�^���i�������w�J%Y���b�&���C�/B�Zh%���K��q|��t�Ghϟ�xz~'~z׎��9��d0<A忯���Q4q�#I� �_~�����^a|5��Wo����{��x���:VeV���5��(8�xKp���'��I���s��`p�dp��<���O�)�N��$]>y�e�BLҬp��]�"gJZ�3�|,>���@ u�;b��N�l!^�}zB��QQh��;�Q�Y0����(u3��lL�\U���}98/�/�Jl�(�8�;�;���,�D:�į�/����RH�����*��M�B .��W���ʫnB��6(�k �� *�qfL�\��22�H���T �$��%�Z�$�t�WS=[�EG4ڡ~*�Y#�l�&vHߨӪ&3$���!��{ ,���5��q��Cl�"`�ӭ"��_�?���x����*������J�ޟk�����+���IE����!�Z�d�)��4�]6��Z�\*�Q�w�d,�V���"fXT��*�V��N�u�Y�H�SU!�o�Wv��UӴ��z��-I��(6�!6v�F��ɕ*����N���U��Z�S@��3X,���"1�#�Nl���Bk���A~dqW(�l����Ɍ�Q�fS��=�5��<͆��~�0�
�͙v�k�9��Y���39Ԭ
7
z�"���^aо+Y�c�-)ʢ@&�����	��ndM^s���}$����z�肓�i!����I|�{�Bء#ݓ
�J�+ݧ¯��Ά��&l�n��4a1{9�� }v��%yC��`O�4Bi�7 +�5�Źu}W�����cL��H�;H����(Qi,cb���n���� j�q�εɢ����~�8��-� �hݫ��S@<p}��E��-{W����l��ق�~�����m#[�U�����㰩�c�c/�8�u�T��|�8������sC�f05��\�4?Ԑ��'+�-��!C����SF��tď����%��&(��gVQ \�E�
�a6}��h�q��B�0�k� H�.:��!`��i�#$L?��P��٤��~��X��k�)�:�)�U�Ni�t{Mba�\�HXN,�;Eҝ"%R̹E�OC��szN���w}).5Y(}w�Ͱf^�hM`N�k�ء,�*���2Am��R䎋ۙPrH�%�E���v�tdg��dU�-	��\M�B�b��t�4���9���)E�ZUN�����X9�-�1�rɟ~u�A�
H�7�6��6"����f���ˢ�M��#�����O���L�d����Ũ�!/@Y��U�����1|���ZI0�^�;����&U�-��e�j	d��L)8���&�ݔ�bK�<f������?��h�ų�ҋ���N�g��S����bu�m�F_U��g�D�v��1ƻ��ɚN�f���m�[7^^��[1��:�ڗ"f��6�D[���N
�$��+���yO/Ai�Ԕ�ʹ�QCq�[gd��P	�v�/d�K{{fA������ܹ(���7'�y5C�X㛤�#�TYS�7�?�j��Y�O���?;N�A��+��Q&��i�.�_!����+�4N��7�SƳ�9�����_�W�'5�� WP�|��m���	na9���ueZU���΅-�����\����Q�U���й��}�ɔ�E����ⵎA���t��X9I����)2c���ɂah�9���5c�ZH�S�ʲ��8�F�TV��� e��"�����ؚ�r�[g���Kǥ��(٦�r%��L�I�+�����pb'ݦZ��]
A�tAs-�2c~U얯&�5py3�|�<�k���o1/T��M�C�1i�8`J-mo��C-��Y-���D2i.$����"���
�P
t�����`n��l���^���
`&���r��)7�ˆ� �io�����/�]%�
endstream
endobj
15 0 obj
<<
/Length 4753 
/Filter /FlateDecode 
>>
stream
x��]ێ&������(�3�4j�]�,�x�%_��ʲ�ݻj_x^��L��fgd����~2�"������6
���(ٷ�i"��/߶�/ۏ����n�o_��m�����釲>#J���/P�������U�{1U�5�b{�D��˷�ڞ��?QJ٧���ȏ�0�.�J��#?����?��R���+�R����'�tp}�>>��y�ϫ���8�b��^y��g�|��{A~2�-,����-3�%��2֎�aZF�d[�8~|$||4B���Hf�_�O�u�B�	����<����i3��;c,~x�廒�^��1�]�n\��&�ھm�@A�Do_������_�����?o��m���m�������aP��7~��Ӂ�Ƒ������{D�C�S��B���+�P����~	��@'�g�t%�: 隗�� i�2:��{�5�d����᧗����+=t����$#$ڕ�KH�� ��#{����0h�A,�B�ğ������o?�������ڱ�]�q��ѕl1�_c�-�%�c\̓���	h!=��T��������p�V���;��X�:J��OΔ�9�0Y=i�l�R�5J�|E�7o+�K��)ʙ)V�\˭SOm?�XT�{�w4H:�Ҽ��=�aќ�=�k������	 Rm4��e4����U��ʔ:�\ ��x�P���4�;B�ѣ��8;�Tz�w���<J�{��L��ʣ���z�ܶ(����K�_�!zU0P��*gT���7�)�3pĒ�	�i�T��Zt�k!ԃxM������n%x�gO`܋����������oG���|c�'́���Yh?���E��5<��d=a�`��]��a8gF��#�s�w���s�q(�kW����� �nw�T&O���>��]��Xn���y���#t�֎��2y�2=>�2���yOs��n�#�թ�Z�I�:�.�Я�F%4��t�AVX�,��������D�֓U����K������]��z!��%$�4ÚUF����(Ӳ�P�2���f�
�����(�'2��0�3.%|�`B!z�J_���'B��p�#�o�P<�	D���T���p����E�"��p*���}8���.�j}8�D�>4�Q��MF����꾆� �3V�w�Ge��f��EƜ9�g��	���<Kp5&~������W�[U�Z�H�z� �w.�
��4v���q���l��d��8��1������3�s�(5����e�`k������<��xhb$����Ւ�N,�K4�W����~_�y=±_�ͪ�����o�<�g�Io%���5�� ��5P�o�zbu�_%�qoA��cv��+2m��r���k��.h���V�Y�H�z��qP&�׈��D9Q|_$Z�[�W
�B�Z8���ߓ�h��[�T����H��ĩ�XXhu֟�����I�@~�M긛�/�sm`���W�)�G���%Q@m�"��݂�t�|�h�nI��\$Z�[j�N�kD�w�;�S�Z#Z�[�"�
́M��V��`a�մP��w�Lw؎r��d��������ݒ�]c�V�>0��33�L53�M��0>�pl�b���;��[�k����HP�V�;��{Nߎ4�w�0�o'DeGߴ����h�����owtA�᧾��vN
ddwS �ۣ-x��Ѱ{��$�Av��=�4R���h}���iQKp��{f�Y����ѐ�5ȹ���J�OifKs0���j����g��4�!w|.�æ�޹K��4�<�F��h1�i'��ż%z������]�e�3���g-�30K\��a�]����h��}��/�"G�gvp�c�\�B�<f�z�9�������e���L��U��Wd���0�8_a��f�1\+�@���Q����ݹ\�h��d<�P�1V�?��ت$<Fh
��ɸ���NuB���~*@�p��e��wЄ����	��RDj^�0$b�0��0~���a`�T5�Dnƃ�Q�"�z����-�¸Pi^��"�z����-���P��i	KW8���F"ׇ՘�dm��_A|K�1���W�{GP+3E�`�li�<7��+O�'-�¼�gL!��6�~�_���c���Z`b/��N�����?��wj�'�\��%
F��")p���I#�`��3��>����%2$�T�NeH��!�!�c3$����t�s�L�u���Ȋ�H��]��uᾑ�o�3
]Ķ���"|y��ж�"�H�>�II�
1+�W�Ȋ(�'B��p'�	�J=�cF��r�Q�F"@���>[J���%�%8��A"��&��H*���BL�`�R\*���}8��,/rw�x��1��W�H:(�'B���v3�.�M���_�N���ȉ�H��.�8�Cs�W�[u�G�H�z��J2D/][��`y��[�Hh.�xֹ/�gjR�e��sQ�޽��r����^b�9�C+�B�-��͒$�eJ.���,#.:'��f�>�63_G��(�PM��r�k�,N3"(�s��Ҽn��wH	py�>���g�{ϧl�$����	��\�@�~����V��	J�C�@����gF�)w�=T%l/�{���~�R	��~���`=�����T��+��Ю��^.�jX2�Bv���ѳ���8Sl���~�y��mŋ9i�9v�X�!����d$�!yݗ�]eR�����	Q v���d�M��hAMp���R<:>�ZK��k*��������߆	��.M���<���*��r�L�`ED�sp���ЩK��N� Ja|hg4��@d:�R߇�i}��ε�6	�&�C\�� �=O�F�b�=����ѧ[��|:� �S�6��v�D��d�њ�icx�m���?����[4�����FEy`���g�g��6h>��U�.���n��.�7��cc4�4$�Ce,�5$ϴ>cN/��,�kc�;P,�i��X�f&��,�eC1�`d(�*Pi(a���H����f�1����ŉ�-
�-&��h��S��vQf���X-�A��:��"�6�=:4��w����;&.�$�	��mL�_2 ����$��)��{�la� Z=�yҟ7�{�#���qT�e�a41k�Áf�ws�$�ك�ct}��X�LCm=���G�R��ZL�r9�mze��W(b�f̂X����m�$���D޳�l�l���c3&jw7U�C}��8�ܲ���|f�v2�	o����H��k�)�oS9���zURna8��^��I03&b}]2b�DL_7���%7L�,��̓���N2�qT�e���*j-��� �候tWb'�]U;�ڠ���k|�i�Јy�oXw:9�i�v�4��(��+xU�X6�S_��$k��)m4���gd�X�)�(���A���֘U*4:R�񑵙��ꄤ����#ɕr�Ɵ��������0���_�8��,yh(=�Wc9;v�qs�����u.J�E����(N�К(�R�QRf�/�ⱛ�E���=��(^�T�t��n+V���y�P61����i(щO")Ӿ�9�%���9& �?s�7�`	Y���@��GS!Ȥ�#��o��y�	K�k�1� 2���0<�R���3B�Z}@5�H��Yl%4�>��$���To��O��(�l,��A9[��\���A�٢�+Y�� ��=
�{ iL���^~k0\>�@&P2�
J�"�A+_�w�ʀ�ǃV�<c?k(x(MV����o�;�� iJJÑ(�N��ZM��,-,�ϥ���Y�p_L}����X����1F���͊J���׽�9����ݜ��w7wG�׹�Y�4��;����+uq��.��Dw0U4'�_673Ǖ�Ew5���Q]?�jؘ��E_xP���H�2�B�M:�e���ǻ2�N�I����\x�,�����H @���t��U�82%
��}�H
C�aˏ0o��BQ>a�\�~��q�0�T7k�ogG��!�ƅ��޽�G�`ھKL��9�y�>˨�L?�:�Ґ������t�O�K#���������	���}���ۛ�Y��0	��l�8ҩ��vO���bNv�E�;�ҫ��H0o���메?�m!=�8���~���W�.�,>���b%�-&�Ɣ�8�ێ@b��Yk���,������xjAAW?����m`��W�u���'^di�A碘{�DL����1)��A��$�J�Z#&�$�5JJ��I�$$g��~�V���C>�G�%�س�.@p��KE`�>qi�X,Ǉ�w��:a;��24bbd�U��<�cc�M���CL�XQ���1e]l�W֝濍�2��,�����g�^�O�y�ǳx<����7 =4�v��^ooW��I�DV'!��GLBlI���z���r�4u�v���띷Y�6Odau�f��6���J��~��N��"�t�o�dΏN��6���O,̃S�IC�ΰT����]���)�Æ��Ԍ)�q��@�ߋ�x����mG�G��Zb�ϝ#,m�b�
��;AdRd�^a(�F�Q��T�����}!.q��#�.�F���Χ���p'��7;���l	^_���އy���g@��|s��Iľb�	��ԑ�3}�v�gɮ@�B|�a��zCO
endstream
endobj
6 0 obj
<<
/Parent 7 0 R  
/MediaBox [0 0 597.6 842.4] 
/Type /Page 
/Resources <<
/ProcSet [/PDF /Text] /XObject <<
/DL91 8 0 R >>
 /Font <<
/F-0 10 0 R  /F-1 12 0 R  /Helv 11 0 R  >>
 /ColorSpace <<
/DefaultRGB 4 0 R  >>
 >>
 
/Contents 9 0 R  
>>
endobj
13 0 obj
<<
/Parent 7 0 R  
/MediaBox [0 0 597.6 842.4] 
/Type /Page 
/Resources <<
/ProcSet [/PDF /Text] /XObject <<
/DL92 14 0 R >>
 /Font <<
/Helv 11 0 R  /F-1 12 0 R  /F-0 10 0 R  >>
 /ColorSpace <<
/DefaultRGB 4 0 R  >>
 >>
 
/Contents 15 0 R  
>>
endobj
7 0 obj
<<
/Kids [6 0 R 13 0 R] 
/Type /Pages 
/Parent 2 0 R  
/Count 2 
>>
endobj
2 0 obj
<<
/Kids [7 0 R] 
/Type /Pages 
/Count 2 
>>
endobj
16 0 obj
<<
>>
endobj
8 0 obj
<<
/BBox [-20000 -20000 20000 20000] 
/Length 114 
/Filter /FlateDecode 
/Resources <<
/ProcSet [/PDF /Text] /Font <<
/F-0 10 0 R  >>
 /ColorSpace <<
/DefaultRGB 4 0 R  >>
 >>
 
/Subtype /Form 
>>
stream
x�U��
�0��>������ ܄l�T�S}���A(w��}ǻ+�����W�P|NL����bwu����[8��
my�P%E)�zֈ�f�2+J�*�Ǻ�b��� �6p_�y��
endstream
endobj
14 0 obj
<<
/BBox [-20000 -20000 20000 20000] 
/Length 112 
/Filter /FlateDecode 
/Resources <<
/ProcSet [/PDF /Text] /Font <<
/F-0 10 0 R  >>
 /ColorSpace <<
/DefaultRGB 4 0 R  >>
 >>
 
/Subtype /Form 
>>
stream
x�]��
B1C���Z���VAA7��8	:�A��� (ɐ䄇+!Wb�;�j��3���ygq�3n߷�5�|^K�K�R�zֆ�͢U��Se>��ǅq�`?&No� z1�
endstream
endobj
18 0 obj
<<
/D [6 0 R  /XYZ 10 866 null] 
>>
endobj
19 0 obj
<<
/Names [(Total-Page-Count) 18 0 R ] 
>>
endobj
17 0 obj
<<
/Dests 19 0 R  
>>
endobj
1 0 obj
<<
/Names 17 0 R  
/Pages 2 0 R  
/PageMode /UseNone 
/Outlines 3 0 R  
/Type /Catalog 
/ViewerPreferences 16 0 R  
>>
endobj
4 0 obj
[/ICCBased 5 0 R ] 
endobj
5 0 obj
<<
/N 3 
/Length 2591 
/Filter /FlateDecode 
>>
stream
x���gTT��Ͻwz��0tz�m �I��2�0��ņ�
Di� AFC�X�BPT�� ��`QQy3�V���{/��ý�����]�Z �O ��K���C����1�t� �`�9 LVVf`�W8��ӝ�%r���# �o�����I���  �ؒ��b��@�i9�L�}V�ԄT1�(1�E����>��'���"fv:�-b�3��l1��x[��#b$@ą�\N��o�X+M���ql:�� �$�8�d����u� p��/8�pV�I�gd��I��K�nngǠ�pr�8�q0�������L^. �s�$qm�"ۘ���[��Q����%��gz�gm�w۟�e4 ���f�ﶄ* ��  �w�� $E}��E>4�$����999&\�D\���������x���C��$2�i��n���!����dq������0
�$r��("R4e\^���<6W���ѹ�����}�k�(�u�	��F�� E!$n�h��o�H �yQj��������.?��I���C��,!?���Z4  I@
@h=`,�-p .��� b�
�� �A��@!(;�P�@#hm��'�9p\��0�F�xf�k� A"CHR��!C�b@N�' �B1P<�� !�m���2�����o��9�24݅Ơi�W���$�
��:�)̀]a8^'���5p����#p'|�
ã�3x�!�1�@ܑ $ID��z��@�6��Gn"����AQPt�1�僊@�P�P�Q%�j�aT'�u5��E}D���hC�=��NB���&t�z=�~��`h]�-��I��Ŕ`�a�1g1C�q��U�b�AX&V�-�Va�`�`o`'�opD��煋��p��
\�4�n����k���Ax6>_�o����'�i�.��NH!l"T�/�D�юB�7+�G���cķ$�ɝG�v��Β�^��d�9�, � 7�ϓ��HP$L$|%�$j$:%nH<��KjK�J��\#Y!y\��^JG�]�)�^�F��m�9i���t�t�t�t��e�)�����[�@��y�q
BѤ�SX�͔F��Cե�RS���o���YYY+�H�ղ5��dGiM��KK��Ҏ�Fh��T�\�8r����n���+ɻ�s������)�<Rv)t)<TD)(�(�(�W��8�DUrPb))S��+(�*�U>�<�<���⭒�R�r^eF��ꢚ�Z�zZuZ����U+W;���.Kw���+�}�Yueuu�z�������F�F�F��CM�&C3Q�\�WsVKM+P+O�U�6^�����W�_{^GW'Jg�N�Δ������V�zd=g�Uzz��1��T�}��`k�d��k����!�p����Έg�`tۘd�j�m�j<fB3	0�7�2yn�ek�˴�����Y�Y��}ss?�|��_-,X5�,ɖ^�,�-_XZq��[ݱ�XZo���`ck÷i���ղ�����͠2�%�Kvh;7�v'���������`����0�Dw	gI�qGG�c���)��Ө��3ӹ�����ۥ�e�U�5����s737�[�ۼ���:�����G�Ǡ��g�g��#/�$�V�Yok��g}�>�>�|n����|�}g�l������������z�@��݁�j/�-�
A�A����
�>R�$�<4/�?��2�%�u�[xi���aDo�dd\ds�|�GTY�h�i���1�1ܘ�XlldlS��2�e{�M�Y�ƍ,�]�z���+�V�Z)����x<:>*�%�=3����K�M�M�e������]���i�#��3��X�8�䘴;i:�9�"y��έ�H�I�K�OJ=����֞�K�O?�����2T3Vgeff���_�g�,ߟߔe-��PE?SB=��X�SvM���Ȝ㫥W�V��nϝ\��뵨����y�y���ֹ��_�OX߻AsC�����o"lJ��C�Y~Y���Q�{
T
6�o���Z(Q�/���ak�6�6���۫�,b])6+�(~_�*���W�_-�H�1XjS�'f'o��.�]�ˤ�֔����YN//*�g��Vu{	{�{G+*����vV��N��q�i�U��^;�����~��mu*u�u�pܩ���l�i�8�9�}�Icdc�׌������>�=z��ٶ��E���n�N�;r��o�ی���i��G�Q�ѧ��;r��X�q��﴿���tuB����]�]��1�C'�N��8�t|o�����'kNɞ*=M8]pz�̚3sg3�ΜK:7޻�������B�/�_�t����~��3�/��l��ƕ��6W;�:~���c�f������v�{�����|��M��o�޺:�txh$b����ۣw�w���}q/�������J=�x����G��GmFO�y�<{|�5�짬��O<!?��T�l���:9�5}�鲧�2�-��,�s�s��������l������_K^*�<���U�\�ܣ����(�9����]ԻɅ������?�|���`1}q�_����
endstream
endobj
3 0 obj
<<
>>
endobj
20 0 obj
<<
/Length 475 
/Filter /FlateDecode 
>>
stream
x�]����0��<����*x�$���XX$�V�}���$�	�~���Us ���؟'v��o�];��{��Cͩ���-��ù��̊i�zTL��Rf��?ܯc��Sof˥�~L��1��Ӻ����cb۝�ӯ�a��m��K�F37��i��Q�k5|�.�d)�y�}��3��>#��b-u߄�P�!V�9L�ϧge���Y�Y��#�2���w�f���&�(	���D|!�	K�-0�F,��Z`"K|A��Q*'�=q�0��-r�����r��9}-|Nd�[D�z�����+\���������o���u\���he�:��[髣�-�D�z�
|�-��]��$�W��� ���W��u_O��p7�9wR�[(��SA�[��+���u��-�9���|EG�+�_�v;�:9�:~f���\�:.ñ���r����q&���y��[��U�n�t�G����-4�C���k�N
endstream
endobj
21 0 obj
<<
/DW 500 
/FontDescriptor 22 0 R  
/CIDSystemInfo <<
/Registry (Adobe) /Ordering (UCS) /Supplement 0 >>
 
/W [0 [0 722 610 889 277 556 610 277 722 556 610 333 666 556 389 556 666 556 556 722 277 556 556 277 610 556 277 556 556 610 277 277 333 777 610 833 722 722 666 610 277 722 610 556 556 583 943 610 556 333 333 556 556 556 556 556 722 610]] 
/Name /F-1 
/BaseFont /SUBSET+ArialBoldMT 
/Subtype /CIDFontType2 
/Type /Font 
/CIDToGIDMap /Identity 
>>
endobj
22 0 obj
<<
/ItalicAngle 0 
/Ascent 905 
/Type /FontDescriptor 
/Descent -211 
/FontBBox [-627 -376 2000 1055] 
/MissingWidth 1000 
/StemV 0 
/Flags 32 
/FontName /SUBSET+ArialBoldMT 
/FontFile2 23 0 R  
/CapHeight 715 
>>
endobj
23 0 obj
<<
/Length 25604 
/Length1 25604 
>>
stream
    	 0  `loca#�    c   �fpgm�� ,  �  >maxp
�    �    head�     �   6cvt ��   4  `prep\[ =     �glyf�t  !�  A�hhea�     �   $hmtx    �   �      v��2_<�     ��<    ք����� r  	         >�N C ���z                 :  � a� R ~9 �s 0� �9���  s U� �� V Js I �s V �s As � �9 �s Fs V9 �� ,s �9 us &s S� T9��9 �� s9 Y� T� �� �� �V �� �9  � �� �s #s �� U� � �s 3� k� Cs Ws [s Ms As W� �� �    :� < �    / V  K�  A T���5  �� < ���A� ��  �  � ��  @��2@���2@���+2�����:3@���-�2��� _ 3����U3@���@D2@���3;2@���/12@���3@���2A� /�  � /� O� �� �� ��  � �� �� ���F@���3A�  @� �� ��   � �� �� �� ����	2@���3A�  � � �� �� ��  o� �� ��  �� �� ���A
� � �  ����2@���2@A� P�  �M �M  o� � ��K�-12���K�
2A�  � ��  ��   � @� ����2@���2���{�042���{�2PAx en # ~n  cn  bd  ��@�2�A? ? ) A 2 D  ��u�2���u�(*2A
C 2  4 �2 �@  @��	2@���2��  ���
 /
 ��T�	2�AT �T  n  �n  @n�	2AE  k  F  �� F ��&���  @��	2@�>�3@�>�2�A	>  �� �� ����&82 A&( 0(    0  � 0� P� o� � ��   � 0�  /z pw �w �z ���2����$(2��2� ���	2@��2����2?�s Os  @t�2o�*  @,�2@�p�	2� 2 ���2�  ��A   ��  ��  ��  ��  ��  ��  ��г	2@�ҳ	2�A�  _� �� �� 0 �� 2 �� ? �� d �� 3 ��!����!�@���2���ò+/2���ò%2���ò2���ò2A%��  �� $ �� " ��  �t � �5 ; �5 ; ��  �� 8 �������������� ����P/���  ��&���&$�5 �t�A
�X� � ��  ��7����� ���@7@%@-@�0%0-0� % - 7 � A�  �� �� 7  � 0� @� ���7�A�t �t  �t �t  `t pt   t t  �t �t  ?� O�  �~ � �� ��  �z �{ �| �}  �t �u �w  p~ p p� p�  pz p{ p| p}  pt pu pw  `~ ` `� `�  `z `{ `| `}  `t `u `w  P~ P P� P�  Pz P{ P| P}  Pt Pu Pw  @~ @ @� @�  @z @{ @| @}  @t @u @w  0~ 0 0� 0�  0z 0{ 0| 0}  0t 0u 0w   ~    �  �   z  {  |  }   t  u  w  ~  � �  z { | }  t u w  �~ � �� ��  �z �{ �| �}  �t �u �w��A�~ � �� ��  �z �{ �| �}  �t �u �w  0t @t  �~ � �� ��  �z �{ �| �}  �t �u �w  �~ � �� ��  �z �{ �| �}  �t �u �w  �~ � �� ��  �z �{ �| �}  �t �u �w  �~ � �� ��  �z �{ �| �}  �t �u �w   ~    �  �   z  {  |  }   t  u  w �X �)  � ~ � } � | � { � z 7 w & u   t �7A5 O5 _5 o5 �5 �5 �5  �5 �5 �5 �5@"O�����O����� A  _5  �5  5 �5  /5 ?5  ?4 O4 5544@� �*�*�*�*�*A	G    7 X@&>�&>7&'>�����&6���&6�)@+&6�&6�&6�&6�&67&62&6-&6%&6&67&*�X@"&>�&>�&>'&>!&> &>7    @���� 	���'(���'0���'O���'bA	� ' �  � ��������������4�]�'.�[�'�AU  T  S  R�V�Q�)�+�'&A* '% )X � %  $���#�;�"�9A '  -   ���X@�������� ���%�V@
�-��A�A
X  �X  �X��%���X%��.�-���)��X�� ��@�0t-�sJaR]%���\�  YX��P%�I�%�G%�@Fy@'9 ��  8X�7-�%  2X%�,4*%��U7�@*��[B;#"
 ���@+                     J �KKSBK��c Kb ��S#�
QZ�#B�K KTB�8+K��R�7+K�P[X��Y�8+��� TX������CX� ��� ��YY v??>9FD>9FD>9FD>9FD>9F`D>9F`D++++++++++++++++++++++��KSX��Y�2KSX��YK��S \X�ED�EDYX�pERX�pDYYK��S \X�  ED� 'EDYX�B  ERX�  BDYYK�%S \X� &ED� !EDYX�
 &ERX� &
DYYK�S \X�� ED�  EDYX�%  �ERX� �% DYYK�S \X�X &ED�&&EDYX�# XERX�X# DYYK�)S \X�ED�-EDYX� ERX� DYYK�/S \X�ED�%EDYX�5 ERX� 5DYYK�S \X�ED�EDYX�( ERX� (DYY++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++eB+�1u~�Ee#E`#Ee`#E`��vh��b  �~uEe#E �&`bch �&ae�u#eD�~#D �1�Ee#E �&`bch �&ae��#eD�1#D� �ETX��@eD�1@1E#aDY�?<XAEe#E`#Ee`#E`��vh��b  �X<Ee#E �&`bch �&ae�<#eD�X#D �?AEe#E �&`bch �&ae�A#eD�?#D� AETX�A@eD�?@?E#aDYEiSBKPX� BYC\X� BY�
CX`!YBp>�CX�;!~� � +Y�#B�#B�CX�-A-A�   +Y�#B�#B�CX�~;!��  +Y�#B�#B ++++++++ �CXK�5QK�!SZX�&&E�@aDYY+++++++++++++++++++sssssE�@aD EiDEiDssstssststst++++++++++++ sssssssssssssssssssssstttttttttttttttttttttuuustuuuu+s  K�*SK�6QZX�E�@`DY K�.SK�6QZX�E�@`D�		E���`DY+EiDt sss+EiD++C\X@
  �����t�2o�w w ��w�/12���w�"%2@�t�/52@�t�(*2@�t�!2����72����%2���@-2�%�-�7�%�-�7�����2����/� t+s++++++++t+stY ++C\X�����2�����2++Y+s++++ +++++++++++++++++++++++++st++++++++ss++++++s+s+++t+++sssss+ss+++s++ ++++sts+s++++u++++++++u+++++s++++stu++sss+++s+sstu++stu++stu++++++++++++tu +++EiD+ @BUT@?>=<;:987543210/.-,+*)('&%$#"! 
	 ,E#F` �&`�&#HH-,E#F#a �&a�&#HH-,E#F`� a �F`�&#HH-,E#F#a� ` �&a� a�&#HH-,E#F`�@a �f`�&#HH-,E#F#a�@` �&a�@a�&#HH-, < <-, E# ��D# �ZQX# ��D#Y ��QX# �MD#Y ��QX# �D#Y!!-,  EhD �` E�Fvh�E`D-,�
C#Ce
-, �
C#C-, �#p�>�#p�E:� -,E�#DE�#D-, E�%Ead�PQXED!!Y-,�Cc#b� #B�+-, E� C`D-,�C�Ce
-, i�@a� � �,���� b`+d#da\X�aY-,E�+�#D�z�-,E�+�#D-,�CX�E�+�#D�z��Ei �#D��� ��QX�+�#D�z�!�z�YY-,-,�%F`�F�@a�H-,KS \X��YX��Y-, �%E�#DE�#DEe#E �%`j �	#B#h�j`a ��� Ry!�@��� E �TX#!�?#YaD� �Ry�@ E �TX#!�?#YaD-,�C#C-,�C#C-,�C#C-,�C#Ce-,�C#Ce-,�C#Ce-,KRXED!!Y-, �%#I�@`� c � RX#�%8#�%e8 �c8!!!!!Y-,K�dQXEi�	C`�:!!!Y-,�%# �� �`#��-,�%# �� �a#��-,�%� ��-, �` < <-, �a < <-,�++�**-, �C�C-,>�**-,5-,v�6#p �6E � PX�aY:/-,!!d#d��@ b-,!��QXd#d��  b� @/+Y�`-,!��QXd#d��Ub� �/+Y�`-,d#d��@ b`#!-,�    �&�&�&�&Eh:�-,�    �&�&�&�&Ehe:�-,KS#KQZX E�`D!!Y-,KTX E�`D!!Y-,KS#KQZX8!!Y-,KTX8!!Y-,�CXY-,�CXY-,KT�C\ZX8!!Y-,�C\X�%�%d#dad�QX�%�% F�`H F�`HY
!!!!Y-,�C\X�%�%d#dad�QX�%�% F���`H F���`HY
!!!!Y-,KS#KQZX�:+!!Y-,KS#KQZX�;+!!Y-,KS#KQZ�C\ZX8!!Y-,�KT�&KTZ��
�C\ZX8!!Y-,F#F`��F# F�`�a���b# #�����pE` � PX�a�����F�Y�`h:-,� B�#�Q�@�SZX�   �TX�C`BY�$�QX�   @�TX�C`B�$�TX� C`B KKRX�C`BY�@  ��TX�C`BY�@  �c� �TX�C`BY�@  c� �TX�C`BY�&�QX�@  c� �TX�@C`BY�@  c� �TX��C`BY�(�QX�@  c� �TX�   C`BYYYYYYY-,�CTXKS#KQZX8!!Y!!!!Y-� � � &   ��  ��  ���i��� �i���             � � �(  ��  �1 I  �  � � �  T � $  U I+ ���v�� = � ������  � � �  � 7 N U U e �� Y��  �  ; R a � � �   � � �|��   � � < A A���� * ���	� � ��c�i  " �+���� & Y � �+�H ! k � �� k � � �]C�   I V n w � � �P���{��   ( a i �5M��>�� [ � ��[�[�?����  �
��2�������  & 1 = N V b � � � � �� H S w � &(�~~� . A ] k u � � � � � � � � � �Jb��d�����  # % * t � � � � � 0Pjo���������&�����N��   L z  � � � � � � � � �8h����	"Op���N��5Bk����a�������������    & F i � � � � � � � � �+8;Z^hs�������   ";DOor~�����������"6q�����&.1OZ�22GS����<dp�����*��� �h������  Y z � � � � � � � � � � � �!'+9FKMW\e����������"+ASae�����������#+1IZ[nqt~���������uz����Lmm������/j��6P���p*               ��     � +�S� ?�h�n    @�  t� 5�   � ����= �`�n�! �& ���B �<V� �� � k x �ks ��:}7 �S� <��	I� n �d ^                              9 � ���|+ � � Y � �� ���   U a  � � � (  ] � &l� �  7>z � � ��&B  ���i���7�-   � t h G � � � � � h G \ H 
 ( 2 A P Z d } � ��������y�o �  �,�� � � \ < � � � �� � G                                                      �d � �%2��v�����1 x � � � � �
 c � � �B  , 4 A 8 H X lY� C p � ( 7 B P Z d s x � � � � � � �\ � �,c � A K U _ s �	�� A d  * � �8t , @ � � � � � � � � �
 ,;DVc � W d6 P�  �� 9 N D� � $ B"� � ` �   9� ,�N�8i� �  � T  =q A  P � O 5�R , ��� � � �e��w�l � � \ @vDr��         B���?@ � 
� ��& 	� +�<�<N�<M�< ?<�<�<�<10!!%!!  � ��@ �  �   a��^�  �@N�	��� ��	���	%	(())uu	�)*%(��	��?OR � �  ����4 ����
4 �Z@-@4K_O@4�(@"-
�V � O0'�0���~S+N�]qM�N]�]M��� ?��+]q�+?��++]q�]10 ]]]]#   ! &&#"326?B�������z4�d2���v��Ƞv�[���Zn��^�Fr�������   R���>   �@H������	YVVY�����	���	���������u���t�
�t@9`p! XA+N�M�Nq�M� ?�?�10 q]]qCX@	iffi]Y ]]4632  #"$&%32654&#"R����4������ �nn��nn�"�������Ä���������   ~  �> ';� )��@]
?4444#DEED# /)S	`)�)�)������)�)�) )/)P)�)�)�))@4?)P)�)�)�)!�t�
!�t@'&'
 &@Z5`o�F@&@Z5o`�F�%&&'�)�  '����	?'���@6
?'@Z5'@A5'@<5'@$'4'@:=4/'�'�'''�' ' '0'�''(�<+N�]qr+++++++<M��<�]q+<�<�q]+<�< ?<?<<<<<?�?�9 910r+q] ]+!6326632!4'&#"!4&&#"!~��f�0F�\u�(��'Q;h.��?6Ah-��&��TUUT_\D��Y_�.<H���F�Z,F����  �  ��   w� 	��@?
?@	P	�	�	�	�	�		`		�	�	  @ � �  ] 
&���@	!$4?<+N�+<M�< ?<?<?<�]q<<<<<10q]r+!!�������J&��  0��> *�@�#'#���'�*	F���!�#��")Ue���"�A#@$D&g"d&���"�$	7&EFJOF!B""$'&75!5"5#5$
	!'"""#$"@,sxyv)u*��*��*�"�#����*�*�,!@!#4@4�3!P%�%%@4%,���@
?P,0,/,,!03! ����	? ����
? ���@		4 +x�+N�+++M��q�N]qr+�+qM��qr++� �CTX@5&"6!F!TYdi�
!"((_F(PF?�]?�]999]q� "�˳(*4!��˳(*4"���$4!���$4"���4!���@4k6"F"��"�"�"!" ����4 3����-?����	
>����"%4���@4 0@P`�� P`����4�@M _�F(@43@-?@	
>@574@+.4@%)4@4_oU@"$4P�F?�]q+�]++++++�+?�]q�+]qr++++�+9]q++++++Y10q] qqqq]]C\X� $��@	?(?!���99!���9"���9 ++++++Y q]%327654'&'$'&54632&&#"#"&0ncm7%I��[~����(��_Xo0 &�YX����/+RU(/ K>V�����1>B#fJK��Ұ  �  Y>  �@Zh�44DD��t@ 
& @ $4� �  ���@"$4��p��
&�)����@ $4��?<+N�qr+<M��<N]qr+�qr+<M�< ?<<<?<?�10 ]q]!!4&&#"!!632Y��$Q9It+����]�O�e8P���&��Ch�{  ����;�  8@ I  
�� �l+N�M�N�M� ?<?<�.+}�103k�����      ��  
A� ��@	794(794���@	(54@(54���@P!'4(!'4) **(
/8 7?j jefhg
�J	
			    	 
@>
���@4
%	��@  �a@ 0��$@		0	�		�$ a@	 ^c+N�]M��]q�]q�NEeD� ?<<<?<M�9/<�++<�.+�}ć.+�}�<<��ıCTX�	4	4 +Y10K�SK�QZX� ���
��� ���88888Yq]++++++!!!!!������y��;9*��M����� ��   U��?>  �@QXYYhii}y�����������88JJFYi:77ww�������	����4����43����4����4� 
t@ @4 @4 3�� t@ @4! /@4!O!XA+N�M�N�]M�+��+ ?��]�++?��++�++10 ]qq]&&#"3267#"  321��cOi}kPf+���������2ST����[o/��&%�   ���S&  �@Wg�	<<KK��t@ 

	& �)@@ $4�����@"$4��p��
&	���@ $4��?<+N�qr+<M�<N]qr+�qr+M�<�< ?<<<?<?�10 ]]!5#"&&5!32665!N:�ik�LR?Hr*�Ub^�����e;Ou����   ����  �@)   #
):JY  	
�@ ��`�����t� �t@	/
/  /_�@(&U?��`����  0x�+N�]qrK�7SK�;QZX� ��8Y<M�<�<�]<�� ?�?<�<�]q�9310]#327#"&&'&5#535%z�''Jb|Lz9	��&��T�+�*3QE1���Ӥ��  J���� ,�@=���(�,+ee(txt(��#Y
UU"Y#hfg!i(g,w��!#���4#���@e4Q"Q#�"�#q"q#�"�#�"�#+
*$"$#94#K
KD"C#je#yz"��"�
��"	
	"#
""#
V@ 4oo��e ��@9- H���@I 40@P`�����@9-*	��@4K'&.'��K�  0  -�S+N�]KSX� @8YM��]�N�M��+r� ?�q+�]+�?�q+�]r+�9]]qr++C\X� "��>#��г>#���9"���9#��ɲ9"���@9 9
 9
 9"���@9 9
9
9+++++++++++++Y�CTX@:
:5"5#K
IC"F#�
�"
 ]Y10 ]q]%32654&'&'&'&54663 &&#"#  J ����=L4��`����}}�I/,8��u�� ��������yQ4I.;Vy�p�f��qc5"94%/fm��~�k   I��.> # 2q@hJHI%��	6FW&fg&�&������')Yw�����4�$21,$@+.4$@"(4$@4o$�$$F���@04= ��,3 @4   U!@?!@?!@4!�t�
,����?,����?,����4,�t@@1&)	(Y��@4O44`  �03)!_�O_o3iA+N�]qrM��q�]N]�+]qrM����< ?�+++?<?�+++�]+�9/]q+�CTX�/qY��CTX� $���4T$d$]+Y]+++9<<<10q] ]q'6632!&'&'#"&546676754&#"3276765e�+�ϼ�K%��H�]��V���LPoKT^6�$7XDLE3�.��Y������L7FF��Z�K% QE;��2'<;V2&7$e  �  7>  �@(�	Sfu/Xhp
	��?O�w@) 

( 		0	p		�_�� &�)@��?� +N�q<M��<N]q�]M� ?<?<?�]qr9210] ]q K�SK�5QZX�
28Y ]!!!6632&#"���CkD`YWG=;R/&�kD5�.A���  �QR& 4�(���@44444���@:4  `��@/(  0`�����"&4���@49@4�'@	@4�'@9 @64  0  Ġ+N�]+M��]+�]+�NEeD�++qrM�� ?�]/?<<<99 9999<10 ++++++]K�SK�:QZX� ��� ��8888YC\X� ��@???���?���?+++++Y!!#"''3267+��#��C%CWPQNB5b^&����]b="�sY   �  ��   w@%��Gg�% % '�����	4��@0`p�   0  ���1S+N�]<M�<Mq�+qM� ?<?<�<9/<�<10 ]q]3! ##326654&'&#��R~�b�Nj����vC^H5��!ݯ��i����`.bAPh
  A��'>  �� ��@F9�	����
�	��HGF
O����
��
���@4@4������?����?��@P`����43 ���� 4 ����")4 ����+-4 ����4 ���@4�     _�t��t@$ !/!O/_o�!@4iA+N�+M�N]�]M��� ?�C\X@@(?@?@?@?++++Y?�C\X� ���(?����?����?����?++++Y�]q+++++C\X�  ���9 ����9 ����	
> ����A!?+ +++Y�+9]C\X@@?@?@?@? ++++Y/<�++r++<310]q ]+# '&5 32 !326&&#"�6���i���@�aBZ'xV\<<R/�����+����}�HlzCCs     Z& @(/4(/4(/4(/4��س/4���@ :4�
	
" -� ���@ 4
  % *4 :� 	�CTX�
���@	4 	 
 ??<9+99@ 

		 
	9���@(40@
?
O

�0@9?O�0 ��@5  @Ġ+N�]+M�]��]NEeD�]+M� ?<?<<<999Y10q+] ]++++++!!6767!��T'�:�!�Z&��E--��   �  b�    , �@?w*hx*��	!	(,!%O0�#"% % 'p�K('�����	4��@!0.@.P.`.p.�.�.�. .0.."   0���-1S+N�]<M�<M]q�+qM��]� ?<�<?<�<9/]qC\X� ���9����9����9+++Y<�<9 910K�SK�QZX�
 8Y] ]!2!3276654&'&#!276654&&#�J���Zo_��]�vJ���(­*LWKJ,Ѫ�+BS@y��\�_g�+'�d�q���	WGDU	���x	]NB\*   �  ��  S� ��@)
?@P�����`��  
& ���@	!$4 ?<+N�+<M�< ?<?<10q]r+3!���F  F�30   ' .@�XgU[fg wuv u-��� �-&&&75-FG-Uvtv-
.!'.-'& (!
" ) ().-
  '&!"wP�V  ���4 ����4 �(����4(����4(�� I�	w�!@(@4@4/?O�
!@4!@4/!?!O!!��Z�
	��"@-��_o?�+@4���/��@w+/++@4+���P0$���@	4$ $$��@���w���@	4 ��@�/@4/�M��+N�+q]M�q+�]q�q+N�qM�+q��qq+9qrrr/<�]< ?<��]++�]++�]�?���++�++�]�99 99999999<<<<<<<<<<10 q]]]%&&546753&'#5&&'%6654&'�ķϬ����a��Ñ��X6;F@A�K^OZ��8㢤�cc��!v*�yAϢ������Pt `:5[�2oKCa   V���    �@Kx
�
���	��	�	VYYVghhg996	6IIE	F�	���	����	� ���@%4�/@4� �O"�!��+N�M�N�qM� ?�+q?�+q10] ]]2#" 76"32676&&2�x��w�����w�3P4O33P4O����_�`��I�����ATm�����@ATl�A  �  �  $@8 
&    0  gv+N�]M� ?M�103!���   ,  ��  r@#/	00P	p	�	�	% 	�-@
 0   �-@Pp����+N�]KQX�@8Y<M�]<�<�]<EeD� ?<?<�<<<10]!!5!!��M��N����>  �  &� 	 V@	k{��)�_�^�	 	 �X  ]@  �
��� +N�]<M�<�< ?<?<�]�910 ]!!56$73&���n0�#�E�$Ɇ   u���  ?�	
�@�8

r&$    0  gv+N�]M��� ?M���9 9910!'667#�*uZ7UH��z�p tbU   &  D� 
  �@9 9	+Sk��%(H[���	 
 ��@
 @���(  ��   �X��

�@��?�LH +N�q�]M�]<�< ??�<�]<999 99�.+}��CTX@-=M�� ]Y10]] ]+!!533#~��|춶����'���^�����  S���  $ 0�04&���@l4����uv�& *6 ;F Lncghw'�'�������'�,�0��w���'��  .�+	�  %.@4?.O..�� ��@4p��(���@	40(@((��@?"O""@4"��@�	w+�O2�w%�1��+N�M���N�qM��� ?�+]?�]+9/]q+�]+9]9] 9]9]10q] q]++&&54632#"'&54632654&#"32654&#"Hmc����j`z���ȅ�v�_OP`_NQ`wYWrtYge.�`��֤f�*1�{��i|�w�QT^_TO_`�=t�}vg}�   T��a�   �@-YY
YVVY��	�		p�:4:4JDJD�		�t��t@  
)&�)@ �!X<+N�M�Nq�<M��<� ?<?<?�?�10 ]q]CX@ii
iffi]Y!!5#" 32!32654&#"a��A�Z����²��/Dza��gd��[Y'��p�Ln����� ���Q��   �@M& 6�� 	 @ � �  ] _�	&�O3�k !j�<++N�]M�N]q�]<M�< ?�]?<?<�]q<93<<<<10q]!#"&'732665�5�u*a81#+7������˧^�%4��   �  ��  o� ���244����#%4���@?4 @P��`p�� �  � � � �   0 � �  n1�+N�]qr<M�< ?<?<10]qr+++3!�(��F  s���  2@!0@7   0D   0  �l+N�]M�] /�]10!s(���   Y����   �@U����'x	wwx����������-	-'�
 

 

��@ 0@`p�� �'�   0  ���~�+N�]qM�M]q�]qM� ?�?�10]]q ]4766763   !  32654&#"YC2�g��D��~�����~1汱�ݷ�����p�+:�n�����o�h��������   T�Q`> # /N@bw�p1��1 ##033@CC[YY%V)V+Y/k��;3;(3,KDK(D,��
�*'-$����43 ����> ����> ����(*4 ����#%4 ����144 ���@	4`  _�t�'�t�
-�t@*)&�)@	�11��@
 3$!0X<+N�M���Nq�<M��� ?<?�?�?��r++++++�CTX�  ���4 ����	4++Y�+9 9999<10 q]]qCX@iii%g)f+i/]Y ]32767655#"'&5 325!# &5432654&#"yA(Vn7%~��}b�ŀ>p�������`g��he�F'8!1#^��������G��j<����������  �  � @&&���@	:4
 :;4	���:;4	���@�.4
 .4	
�	�
	

	
#, 	/
ghe	j
wx�	�
�	�
�	�
��	�
�	�
���	�
���	�
w	x
���	�
�Xejg	h
vyDKD	K
WW	X

/4:4	;
?		
	�CTX@
	22  P4P4���@4@'4@'4���@'4 
  ?<<?<9++++++]/���9��;@-
	 		2

2

		���8 ���[]4���@ST42@�� �8@  @[]4 @ST4 2��1u+�q�++<�<�q�q<�++�<�q ?<<<?<9�.+�}ć.+�}�+Y10K�SX� �� 88Y]]]]]]qr++++ +q]3!!!!��
�������������F��~��~  �  #� 	�@	�� �?����[]4���@*ST42		@[]4@ST42���@@P`p��� 0	����[]4	���@SS4	2  0 �  ���
1u+N�]<M�++<M]]qr�]<M�++< ?<?<99 99�.++++�}ıCTX� ��@	'4 '4����	4@	4 ++++Y10CX� ���5�5���@=.4S.42@F�������� /4;O���������@	354@354���@/24 /245���@	!.4T!.4���@F 4T 4,';3N@\V	ME�������'(Jx��]qrr+++++++++ ]]qr++++Y ]3!!!� X������-��F��D   �  a�   @3((
Gee*9HYh96���% %'�����	4��@�! !0!!   0��� 1S+N�]<M�<M]q�+qM� ?<�<?<�<10 ]q]!2#!327>54&&'&#��`��`-7fM�b���(�|7H_<<lS>��&���ε��cK*��5VŪ��f   �  ��  �@=%0�	%
	% KH
  0@	   0  ���1S+N�]<M�<N]�]<M�<�< ?<�<?<�<9/]qC\X� ���9����9����9+++Y<�<<<103!!!!!�?���� 3������q�  �  ��  =@P%    0  ���1�+N�]<M�<N�< ?<M�<?<10]3!!�(���I�   �  ��  ! �@�9IWjj�	��#��	


6FF	66Guy�
x	xv�	��		Su��� %`�  !% ��@' �'�����p# #0##!   0  ���"1c+N�]<M�<]q�]��]� ?<<<?<�<9/]q<�<99�.+]}�9 910 ]q]]3!2!.##326654&'&##�o�Հ��`}j����rT^f<��j<OH$���Oʂ��8����?�Y!��N$XBJ[   �����   �� ��@197GVV
VVY�5;;5EKKE��	
 �t��t@ 
!p)&�)@p �  ?A+N�q<M��<�Nq�M� ?<?�?�?<10 q]]CX@ff
ffi]Y ]+3!632 #"&'32654&#"��������[�@4Iy]��ge������������[Y�*�Op�����   #����  Z@$i�T	f	iiiz�
H�-	   ��@p0�

�u+N�]M�Mqq�<M�< ?<?���10 ]]!#"&'%3265�' +��� 0bcR��`�b���� ~4Oq�  �  _�  � �ݳ?���@}-4'	f�
�
�	�
�

S`	FWv�	����NNf}������
++***/KK
	
	

	  


�m@/9e&�   ?{+N�]q<M�<�q���<< ?<<<?<?<9�}�<�CTX� �Ȳ	!4 +Y10]]]q r]++3!!!�IZ�����������v�|�^݉��  U �V�  H@	b0@7b? O  b
��@bO��MC+N�]M�<�<� /]��]�<<10%!!!!!���� ���}}������     �� �@++ 3 @:4����:4����:4����5	���@	4
4���@	4 4���@Y4 4		
 	) %	�
��	�
���
�� �	�
�� �		���
����
��	."/
 ���
��CTX�����!4���@	!4@!4����4���@4d4 	  ?<?<<9++++++99�� ��0�
	 ��2@\      
2

	 		2 
	

		 /�0@
 ��@/�0@  0^c+N�]M�]���]NEeD� ?<<<?<<<<<99999999 9�M.+�}ć.+�}ć.+�}ć.+�}�+++Y10]]]]q++++++ ++++q]!!!!!e��/�`�*������������  �FH��  �  Y�  �@+933BB��	$Xh�t@	


  
&	@ $4�	�		���@"$4��p�� &���@ $4��?<+N�qr+<M�<N]qr+�qr+<M�< ?<?<<<?�999<<10] ]632!4&&#"!���a�O�� Q=Fn3�����Hp����1�Z5D�����   3  � ?@_��������CCCV����  (7HCCC$$$&V������  1v������@4     0 @  ����4 ����V@#/@4�	�O  �w��+N�M��N�q<<M� ?�+q�?<�+]q<93+]C\X� ���9����9���@9999++++++Y�CTX@	  99]Y10]KQX� �� �� ��888Yq]]]!6767654&#"%6$32�'��+:eYXh�����GM3��G���	۱?WU^ej{���c�bA�P&   k�Qh�  F@(�	 	 �" 	 "  �@
	�� 0����k+�]����� ??<<10]#&5673e���cV���g=5#�Q���!����W����f   C�Q@�  I@''
gg
���	  �"   	"  �������jC+������ ??<<10]>543ESD:f����BK��Q����u��/���������   W��*�  # �@;ju�����������6Dz���� �   ���@4�!/!!@4!�?	@	�	�		�O���!@"/@4�� w�O%�$��+N�M�N�qM��� ?�+q�]�]q�+q?�+q9 9]10] ]&&#"632 #"  3232654&#"��
TCY{i���������*����~QNhpTQpSTP��|������Y��d��鉕z���  [��5� @) 7EI����	!#� 
��@
 0@P��V� ����4��Z@
/

@4
����@4 0@��@//?O@4��@���@�!@w�� @ � �  ӹG +N�]qM���N�]qM��< ?<�+]q<�]+�+q�?�+q�]q9�.+}�9 9910q]%32654&#"'!!632 #"$[vMXzyay`����,^b�i���� y_o����k!����/��ٵ���  M��� ) �@2��{�����������!
 !
�$@O@��@/@4��V� ���@24�'���������O$$+�w� *��+N�M���N�qM��]�9/] ?�+q�?�+q�9/]q�99 999]10q]] ]%32654&#"7654&#"%>32 #"$MrQWwrR6KrxXIHf��m�y�}g�~��������!hn�pj|�iWJXd`,��[�l��s������  A���  # �@X;Kez������ ����� ��4VY_R`w���h /@4�! !!���@4!�0	O	�	�		�O���!� ���@4��O%� w�$��+N�M���N�qM� ?�+q�]�]q�+q?�+q9 910q] q]%3267#"54 32  #"&4&#"326]
TEWzj���	������^}RNgpTQoSSP��{�����u�n�����{����  W  �  �� ��@14
:8
HV����
! //?O@4�� ���X�/�`@O ��+N�<�q<M�]� ?<?<��+]q<9]10]+!!7W�w��������u�J��0x�  ���$�  �@8		GG	W	V��������� %	 ���@"@P`p� 0��   0����1u+N�]<M�<M]qr�]<M�< ?�?<<<10]q!32665!#"&&'&5�(�|~�(0�خ��~���8Zmg��+����ږYa�U~�   ��l�>   �@.8H4994DIID�	VV
YVVY�� �t��t@!p)&�)@p �  ?A+N�qM�<�<�Nq�M� ?<?�?�?<10] ]CX@ff
iffi]Y ]!6632  #"&'!32654&#"�3�j����X�O���fb��cg�&�Pd��������FU����������       l  �  �  J  �  2  	  	r  
�  (    0  �  �  �     �  �  0  �    �  �  �  �      v  !�  #.  $  $�  %~  %�  &�  (�  +  -  -�  .�  /  /  0j  1f  2  30  3�  5�  6�  8�  9  9�  :�  <N  =�  >�  ?�  @�  A�
endstream
endobj
12 0 obj
<<
/Encoding /Identity-H 
/ToUnicode 20 0 R  
/Name /F-1 
/DescendantFonts [21 0 R ] 
/Subtype /Type0 
/Type /Font 
/BaseFont /SUBSET+ArialBoldMT 
>>
endobj
11 0 obj
<<
/Encoding /WinAnsiEncoding 
/Type /Font 
/Subtype /Type1 
/BaseFont /Helvetica 
/Name /Helv 
>>
endobj
24 0 obj
<<
/Length 501 
/Filter /FlateDecode 
>>
stream
x�]��n�0��<���C챓VBH�ġ�ղ� !14Rq"�������@���?�b���B7��G웽ձm������5�F�]3fL��\jv���.�?�±W��B?���o�a���M�c�cN���z?��:���è�j�T�?޷z�����U������?k�n�W?h���[���:��T~>}�j��>K5��?�t�<��:���#�Nh7D���DIX�>r_�%P�������gl��W@G|A�ƪ%nP(��y�mBG��-���oI__)����+���uy��<��������=k�J>|]��jE�o�k��-�1�������:2�}"��2�З�}yf_���u�[�`��F���_K_�?����_W�+l����|-	|��_�v|-}�����F����_G�o��7o�2�җM�ޤ�7��ײ�_�UK�
o|~��/�Q_s���8͜4��D�ϒ.��q7�C���y"$o
endstream
endobj
25 0 obj
<<
/DW 500 
/FontDescriptor 26 0 R  
/CIDSystemInfo <<
/Registry (Adobe) /Ordering (UCS) /Supplement 0 >>
 
/W [0 [0 833 556 333 500 666 722 556 556 500 556 222 277 666 500 666 556 833 556 556 556 777 556 277 666 556 666 500 556 222 556 277 722 556 722 556 556 556 610 556 277 500 277 277 722 943 556 277 610 556 333 666 556 277 777 666 722 500 556 889 556 666 500 722 777]] 
/Name /F-0 
/BaseFont /SUBSET+ArialMT 
/Subtype /CIDFontType2 
/Type /Font 
/CIDToGIDMap /Identity 
>>
endobj
26 0 obj
<<
/ItalicAngle 0 
/CapHeight 715 
/FontName /SUBSET+ArialMT 
/Descent -211 
/FontBBox [-664 -324 2000 1039] 
/FontFile2 27 0 R  
/StemV 0 
/Flags 32 
/MissingWidth 1000 
/Ascent 905 
/Type /FontDescriptor 
>>
endobj
27 0 obj
<<
/Length 44504 
/Length1 44504 
>>
stream
    	 0  `loca2�    ��  fpgm�A H  N  �maxp�    �    head�     �   6cvt �Q      nprepB 6    /glyfR�@   p  �^hheaC     �   $hmtx=�    �        Ů� _<�     ��'*    ք�����g Q   	         >�N C ���z                 A  � �s J� �  !V �� fs Ds �  ?s �� �9 $V��  PV \s K� �s Ms �s U9 Xs �9  V �s UV 	  (s �� �s F9 �� �s �� �s <s Us � 0s �9   9 �9 �� �� s V9 �� �s a� AV �s S9  9 cV �   s B ws IV 	  7� �9 m    A� < �    @ �  �  �T�A,,,"  +* < *��(�&м) �) )�+�'�;@�#�2A-   /      o  �  �   _    � � � �       o � � � A'    � �   / O _ � �   _ o  � �  @��3@���3@��jl2@��a3@��\]2@��WY2@��MQ2@��DI2@��:3@��142@��.B2@��',2@��%2���
2�A �  p �   � �    @�$&2��  d ���2A
��  �� d ����2�AJ� �� �� ���� �  � ?� �� �� �� �� ������ � /� ?� _� �� �� �� �� �   �  � ?� �� � �� � ����Ӳ792���Ӳ+/2���Ӳ%2���Ӳ2���Ӳ2�Ҳ�)�&�;@�" > 3"�%1��<i�� +�A0� ��   � �  � P� `� p�  `� p� �� �� �� ��   � �  �  �  � 0� @� P� в +�ϲ&BA��  ��  ��  ��  ��  �Ʋ A�  � � � /� ��$�A�  � /� ?� O� _� �� �"�dA� �  � �  � � @j@&CI2@ CI2@&:=2@ :=2� �&@&��2@ ��2@&��2@ ��2@&��2@ ��2@&z�2@ z�2@&lv2@ lv2@&dj2@ dj2@&Z_2@ Z_2@&OT2@ OT2���$'7Ok Aw 0w @w Pw www �  ��**��@+)*�����R���e�~���<�^�+���@��8  �@��@��8  �9@�����s�&�%�$� 7@�!�I3@�!�E3@�!�AB2@�!�=>2A! ?! !  �! �! �!  @!� "2@�!�2@�"�*?2@�!�.:2oAJ� � �� ��  /� `� ��  � ?� _� �� �� ��  �"  �"  " /" ?" _" " �"  �! �!  o! ! �!  ! /! ?! O! ��""!!@+H�O�7    ����� 	A	��  ��  ������&�A�  9 &% 8 s 5  4 � 2�V��&,� ��������� ���������/���&��� ���8�ʸ��&���~&���}Gk��e&���^s�@R&ZH�Db@s��?^<&���5��0�+��*V)��#��5UU7�h@,�XO62,!
 ���@+                     J �KKSBK��c Kb ��S#�
QZ�#B�K KTB�8+K��R�7+K�P[X��Y�8+��� TX������CX� ��� (��YY v??>9FD>9FD>9FD>9FD>9F`D>9F`D+++++++++++++++++++++++B��KSX�5��BY�2KSX�5��BYK��S \X���ED���EDYX�>�ERX��>DYYK�VS \X�  �ED� &�EDYX�  ERX�  DYYK��S \X� %�ED� $�EDYX�		 %ERX� %		DYYK�S \X�s$ED�$$EDYX�  sERX� s DYYK�S \X��%ED�%%EDYX�� �ERX� ��DYYK�>S \X�ED�EDYX� ERX� DYYK�VS \X�ED�/EDYX�� ERX� �DYYK�S \X�ED�EDYX�� ERX� �DYY+++++++++++++++++++++++++++++++++++++++++eB++�;Yc\Ee#E`#Ee`#E`��vh��b  �cYEe#E �&`bch �&ae�Y#eD�c#D �;\Ee#E �&`bch �&ae�\#eD�;#D� \ETX�\@eD�;@;E#aDY�GP47Ee#E`#Ee`#E`��vh��b  �4PEe#E �&`bch �&ae�P#eD�4#D �G7Ee#E �&`bch �&ae�7#eD�G#D� 7ETX�7@eD�G@GE#aDY KSBKPX� BYC\X� BY�
CX`!YBp>�CX�;!~� � +Y�#B�#B�CX�-A-A�   +Y�#B�#B�CX�~;!��  +Y�#B�#B +tusu EiDEiDEiDsssstustu++++tu+++++sssssssssssssssssssssssss+++E�@aDst  K�*SK�?QZX�E�@`DY K�:SK�?QZX�E���`DY K�.SK�:QZX�E�@`DY K�.SK�<QZX�		E���`DY++++++++++++++++++u+++++++C\X� ���@t sY�KT�KTZ�C\ZX� �"  sY +ts+s++++++++ssss+++++ ++++++ EiDsEiDsEiDstuEiDsEiDEiDEiDstEiDEiDs+++++s+ +s+tu++++++++++++++stus+stustu+++t+ +++ EiD+\XA6/ A 0/ - -/ 2 2/@&7	7
DD++++++++Y+   @[�tsrqponmlkjihgfeb]XWVUTONA@?>=<;:987543210/.-,+*)('&%$#"! 
	 ,E#F` �&`�&#HH-,E#F#a �&a�&#HH-,E#F`� a �F`�&#HH-,E#F#a� ` �&a� a�&#HH-,E#F`�@a �f`�&#HH-,E#F#a�@` �&a�@a�&#HH-, < <-, E# ��D# �ZQX# ��D#Y ��QX# �MD#Y ��QX# �D#Y!!-,  EhD �` E�Fvh�E`D-,�
C#Ce
-, �
C#C-, �#p�>�#p�E:� -,E�#DE�#D-, E�%Ead�PQXED!!Y-,�Cc#b� #B�+-, E� C`D-,�C�Ce
-, i�@a� � �,���� b`+d#da\X�aY-,E�+�#D�z�-,E�+�#D-,�CX�E�+�#D�z��Ei �#D��� ��QX�+�#D�z�!�z�YY-,-,�%F`�F�@a�H-,KS \X��YX��Y-, �%E�#DE�#DEe#E �%`j �	#B#h�j`a ��� Ry!�@��� E �TX#!�?#YaD� �Ry�@ E �TX#!�?#YaD-,�C#C-,�C#C-,�C#C-,�C#Ce-,�C#Ce-,�C#Ce-,KRXED!!Y-, �%#I�@`� c � RX#�%8#�%e8 �c8!!!!!Y-,K�dQXEi�	C`�:!!!Y-,�%# �� �`#��-,�%# �� �a#��-,�%� ��-, �` < <-, �a < <-,�++�**-, �C�C-,>�**-,5-,v�##p �#E � PX�aY:/-,!!d#d��@ b-,!��QXd#d��  b� @/+Y�`-,!��QXd#d��Ub� �/+Y�`-,d#d��@ b`#!-,�    �&�&�&�&Eh:�-,�    �&�&�&�&Ehe:�-,KS#KQZX E�`D!!Y-,KTX E�`D!!Y-,KS#KQZX8!!Y-,KTX8!!Y-,�CXY-,�CXY-,KT�C\ZX8!!Y-,�C\X�%�%d#dad�QX�%�% F�`H F�`HY
!!!!Y-,�C\X�%�%d#dad�QX�%�% F���`H F���`HY
!!!!Y-,KS#KQZX�:+!!Y-,KS#KQZX�;+!!Y-,KS#KQZ�C\ZX8!!Y-,�KT�&KTZ��
�C\ZX8!!Y-,KRX�%�%I�%�%Ia � TX! C� UX�%�%���8���8Y�@TX C� TX�%���8Y C� TX�%�%���8���8�%���8YYYY!!!!-,F#F`��F# F�`�a���b# #���pE` � PX�a�����F�Y�`h:-,# � P��d� %TX�@�%TX�7C�Y�O+Y#�b+#!#XeY-,�: !T`C-,� B�#�Q�@�SZX�   �TX�C`BY�$�QX�   @�TX�C`B�$�TX� C`B KKRX�C`BY�@  ��TX�C`BY�@  �c� �TX�C`BY�@  c� �TX�C`BY�&�QX�@  c� �TX�@C`BY�@  c� �TX��C`BY�(�QX�@  c� �TX�   C`BYYYYYYY� CTX@
7@:@;@>?�CTX�7@:�  ; �>?��CRX�7@:���;@�  CRX�7@:�� ;@�� CRX�7@:� �;@�7@:�  ; YYY�@  ��U�@  c� �UZX�> ?�> ?YYYBBBBB-,�CTXKS#KQZX8!!Y!!!!Y-,�W+X�KS�&KQZX
8
!!Y!!!!Y-, �CT�#�_#x!� C�V#y!�C#�  \X!!!� GY�� � �#� cVX� cVX!!!�,Y!Y��b \X!!!� Y#��b \X!!!� Y��a���#!-, �CT�#�{#x!� C�r#y!� C��  \X!!!�cY�� � �#� cVX� cVX�&�[�&�&�&!!!!�6 #Y!Y�&#��b \X�\�Z#!#!�Y���b \X!!#!�Y�&�a���#!-,-,�%c� `f�%�  b`#b-,#J�N+-,#J�N+-,#�J#Ed�%d�%ad�5CRX! dY�N+#� PXeY-,#�J#Ed�%d�%ad�5CRX! dY�N+#� PXeY-, �%J�N+�;-, �%J�N+�;-,�%�%��g+�;-,�%�%��h+�;-,�%F�%F`�%.�%�%�& � PX!�j�lY+�%F�%F`a��b � #:# #:-,�%G�%G`�%G��ca�%�%Ic#�%J��c Xb!Y�&F`�F�F`� ca-,�&�%�%�&�n+ � #:# #:-,# �TX!�%�N+��P `Y `` �QX!! �QX! fa�@#a� %P�%�%PZX �%a�SX!� Y!Y�TX fae#!!!� YYY�N+-,�%�%J� SX� ��#��Y�%F fa �&�&I�&�&�p+#ae� ` fa� ae-,�%F � � PX!�N+E#!Yae�%;-,�& � b � c�#a �]`+�%�� 9�X� ]  &cV`+#!  F �N+#a#! � I�N+Y;-,� ]  	%cV`+�%�%�&�m+�]%`+�%�%�%�%�o+� ]  &cV`+ � RX�P+�%�%�%�%�%�q+�8� R�%�RZX�%�%I�%�%I` �@RX!� RX �TX�%�%�%�%I�8�%�%�%�%I�8YYYYY!!!!!-,�%�PX�@  c� �T\�KR[�Y-  � � � &   ��  ��  ���i��� �i���   �   �     � �i � � ��  � � � �  D � | � �  Z � � R R  D ��� / �  � �  W ~ � ��  �� � �  " A P o �L�u \ �� 7 L n p��X������ � ����   c c ������ - \ � � ��	� @ W � �� r �]�g��  ! w �  M ��+ L e �|C�������   ] h � �5G!\�M��  - x � � � � � � � ������  , I  � ������?     ) 9 I o � � �#�o2@z��  1 U W � � ��~~�F�B  � � � � � �/OV)o�r  , 1 1 d i � � � �+��������  & � � � s���C_�����a  ^ m � � �8Q[h|������ATk�hq�BBSs�����X�������2�� Q | � � � � � � � � � � � !U{{~������������  !""#rw�������"+5<Yoq�������22������� ����*��� ����������      < Q a a j x � � � �*>LQ_jqx����������� !".5BOO^eq�����*G]ety���������
"&+G_u���\��
m���6>PQ]���` � � � �            ��E� �3�� - _ dM?  ��}�$x;;N �&����;MKS j1      �   <� ��e�� x~� � 9  �0+� ��� �
��P�>X !� �q} �E  
��+N� � T2�� N � 7� � k� � w � �dg � 3| � ��)n*�i�� �  9$ �]��� u �
 �����M�Rh m } � q�� yX�g V %� � |2! �  r \ / �  � � AM r   LjU � � � � �  x i  W n � �T� ge �  ��R Z�� ��g n�� -�� ��| � � � � ���{ p  � �LF�F�-��S� �              % � � �   >� �� S ?����  ( " � b J � m � � H� 3�N��Fp y� Q���
 h�l O � � a+ ��� � { eR�te�i � � \ @ � u � �q�� � � � � � � � � � �           B����@ � 
� ��1 	�. +�<�<N�<M�< ?<�<�<�<10!!%!!  � ��@ �  �   �  � P��+X�*�@�V*�@ V�CTX� ��@UU���U���@(UU	 	 	
UU����U ���U ����U ����U /+++�/+++� ??�����9++10+++ �CTX@ U U U U U���@#UUUU	U
U����U���@U& 
4 
4  
���U
���U
�V  V@ U U ����U /+++�/�++ ?<?<<9++]10++++++++ +++++@ v��	II)%,X[vx�96OKD@MB
������00RR@	
 	`��� 1� �1�	

�@�V

�@@	V
 @�V � �� A
��  @ V  ��  @�V  p�V� `����;Y+�]�]<�++<���]<�++<���] ??<<<<<<<<��.+�}ć.+�}�10 K�SK�QZX� �� �� ��888YK�SK�(QZ�C�@PZX� ���
88YC\X� �Զ!9,!9��Զ79279��Ե-9,-9++++++Yrq] q]]YY ++@  ?3?3?3??01Y3!67!##�$[05_��V��X���HP���F��5��   J��> ( 7"��+X@,		**)**967:*I*]]*ji*`0��)���(���U'���@U��(��(��(��(D���@UUU5���@OU+,*499,IH,VY+fi+v����+74/$42!_)o))/?���������  @�VU���U���@UUU&�@�V�@�V���,�@@V,

BU� ���@U E'
2)aa A��  @ V  ��  @ V  ��  @@V U %!$���U$���@U$U$���U$����U$���@U$U$����U$�[@'@ && &0&�&9����U&��ִU&���  @�V&19���@#409�9�99����U�@@	V%"/�@�V/�@�V/�@@V/$��?�@�V�@�V�@@.VUUUUUUU18�++++++++++]q�+++��++]q+�+++]��++++++++<�++++�� ?�?�+?��++�9/++++++++]q�q999910 ]++++q]++ q� ++)�-�l'
2�-�l�/�l ?+2/3?+?9/+93901Y%#"&546676767654'&#"'>32#&326765<d�j��GsH5k�g3E�y�nЉ��P	"�b�o\2mih�&�UF��N�N$%
n-=Yqq�K@aJ.x���=8�((M/H`[O=w   �  �> ��+X@;/#4CSft				  
	(�" "�@�V�@�V�@�V% ���@364�     � �  ����U ���@U U U ����U ���@U U U NG�+�++++++++]q+<�+++�]�r� ???�999999 ɇ}�10 ]r]� 
	�6�l ?+22??01Y336632&#"��>i?[^>BB;^&�qH:�'G?`r��   !�Q�& Ű�+X��@�V�@�V�@�V�@�V�@ V ��  @�V�@�V�@�V�@�V�@�V�@�V�@�V�@ V ��  @�V�@ V�CTX@
@ @ U/+���� ???�910����@s9(V�
@@ (04 (04	'''665�((HYYYiiiyvyzz������
�����
�����BU�CTX@D� ???�9]99@7
 %

%

 /��?�@@�T@?@_��B�" E
�T@ @@ 0OP��B�/�?� |f+�q�]q�����]q���]q ?�?<<<�.+}ć.+}� 9�<<�K�SK�QZ�C�@PZX� �� ��88YY+10C\X� �޶79
"79���9"9++++Y]q++ q]+]Y++++++++++++++ +��3@
l

 ???3?+01Y'326767673673#";,<H&�m��+"+��lA$0|V4�g�($k(��u�|vk�ȯBYS   �  R� T��+X@"79	:'
56
G
W��v
��
���@U(����
5�	���@	!4 !4��޳9	���!4���!4���!4����4���@C9	%%=	=*BU	
	
 

	 

  
 �:@0����J�:@0 ������@�V�@�V
�@@V     U ����U ����U ����U ����U ���@
U ];�+�++++++]�+++�]q��]q�<<<< ?<<<?<<<9/�.+}ć.+}�<<K�SK�QZ�C�@PZX� ��8Y�CTX� ��4���@444	4
4 ++++++Y+10+++++++C\X@	"9,9,9"9��޶9"9���@9"9@9��޵%9@9+++++++++++Y +++qr]+ q]++@	

   ????9/39301Y33!!������� �����)��������  f��v� /��+X�cj���U ���@_U  2c p t� �� ������� ��*(* GVWVhk{��������  ��޲(9���@ (9 	&J & �@�V�@�V
�@@
V& �@@VUc\+N�++]M�+++N�]M��� ?�?�910++]]q ]++r@
  �2�l	�2�l ?+?+9/39/301Y#"$54$32&&#"326��=�����כ�C��,;�3��\m憣�1���n��U���-�����銼   D��'>  ���+X�U���U���@eUU
GHVYgi4::5EKKE\\	R]]Rmm	dmmdw	[TT
[lee
l
A��  @ V ��  @ V ��  @@V$@U@U���@UUU���U���U���U���U���@$%40  ���  @�V1����@#40�@�V�@�V�@@AV$ U U U U U U U U @$%4 ?  �@�V �@�V �@�V 147+�+++]+++++++++�+++q+]�+]]++++++++++�+++ ?�?�10q] qC\X@	SS	bb	]Y ++++��/�l�/�l ?+?+01Y7632 #" 32654&#"D����{�������������'�v������������  �  �> 氅+X@���������@"4y���� 
A��  @ V ��  @ V ��  @@V$@U@U(UU���@UU"U���@UU���@U
U���@U@364��N���@464��p���3�@�V�@�V�@�V% ����U ����U ���@U U 
U U ���@U U U ���@364�     � �  N�]q++++++++++<�+++<�<]q+�]q+++++++++++++�+++<< ?<??�9910Cy@	


&
 +++*�]q +]q@	

�0�l ?+2???01Y33632#4&&#"��u�`�P
�*kHs�&��EpM2}�s�nmA����  ?���> 0��+X��@�V�@�VA7@ V (��  @ V '��  @ V &��  @ V %��  @ V $��  @ V #��  @ V "��  @ V !��  @ V  ��  @@|V"":	J	D$V"e"|	�	�$��,�	0K,�U2
\\	\
\\\jj	j
jjj�&�''&$'$)6$Z
Yd&d(t#t$�$�
��(�,�0�
��'�(�&�&(����U"����U#����U$����U(����U"����U#����U$����U���@9Z'%
 &.��@",U?O_��o���U   � ��@U@� ����4���@4.\l����U���U���@U.$@42���@2UUUU U UUUA	@ V [ ��  @�V$*����9�**���U*���U*���U*���U*���  @�V*2���@!'*4`2�2?2�22$ U U  ����U ����U ����U �@@V $UU U���@UUU�@@V"� ? O  147+N�]qM�+++++++�++++++�rN]q+�+++++q+M�+�++++++++++�r ?�+++?�q9/++]qr+��]qr+�99910Cy@@'-#,&"  	(-  !# "#)
('	
+  ++<<+<<+++++*+��� +++++++++]q]rq] ++++++++++++@
 &&.�/�l.�/�l ?+2/3?+939/301Y732654'&'.54676632&&#"#"&?��{|x5%�ƙOA8*�S}�Z�si|j/���Vi�}��=kreD=#%2I�NGy(+H{gR\R7#
$3A|\Z�W�  ����& ���+X� ��@	4 4���@4+$ 
 3A��  @ V ��  @ V ��  @@V%@364@U(UU���@UU���@UU���@UU���@U��N���@464��p����@�V�@�V�@�V%	���@364�	 	 	�	�		����U	���@U	U	
U	���@U	U	U	NGP+�+++++++]q+�+++]q+�]q+++++++++++<�+++� ?�??<99910Cy@   ++**� ]+++� 
�0�l
 ???+2?01Y!5#"&&'&53326653?|�^�O�nQQ�;���HmO5s����1GQS��9��  �  7� ���+X�
�@�V
A@ V ��  @ V  ��  @�V�@�VA@ V ��  @ V  ��  @�V�@�VA@ V ��  @ V  ��  @�V6U����784����454����014����"%4���@%4��O��p��  
% ����784 ���@354� � �     � �  ����U ���@U U 
U U U ����U ����U ���@
U NGP+�+++++++++]qr++<�< ??10]qr++++++++++++++++++� 
  ??01Y33����F   $��*� n��+XA  ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V 
���#&4	���@$#&4� 
 	+
" "�@�V�@�V
�@@"V%�E	E`p��  �������U����U���U����U����U����U���@UU���U�j 6�f+�+++++++++]q���<�+++<��< ?�?<�<9933�10]+++++++��2�l �2@	l

	�-�l
 ?+322/?+?+01Y%#"&&5#5373#32L<bl,�����+(��>e�c�l�����M,  ��  Y�  ���+XA ��  @ V 
��  @ V 	��  @ V ��  @ V ��  @�V�@�V�@�V�@ V ��  @�V�@ V ��  @�V�@ V ��  @�V
�@�V�@�V �@�V�@�V

�@�V
�@�V	�@�V
�@�V�@�VU���U����U���@YU	UU/0gh	`������YVPh����	
		  ���@U  ���@U 	�p@	 �@� @  eRP����@P����@�����+�]q�]q�]q���� ?<�?�<�<�.++}ć.++}�9999����ć����10K�SK�QZ�C�@PZX����  ��8888Yrq]++++++++++++++++++++++++++++��1@l   ?3??9/+01Y#3#!!&'3�Xݫ�����F"3��F��DZ��w��  P���> a��+X� ��  @�V
�@�V	�@�V�@�V�@�V�@ V�CTX@4@ P p  UUUU/++++��� ?�?��]2�]210@G	CCSS``�����
jijup���	�
���"_o��@&0 @ P ` p � � � � 	   A
��  @ V ��  @@V$U"  A
��  @ V  ��  @@V $+ @+�@�V@�@�V@�@�V6�@@ V@U@UHUUI�@�V�@�V�@@!V$�?U
UU�@�V�@�V14�+�+++++]q�+++�++++++++]rKS#KQZX� ��8Y�++r�+�++r ?�?�9/9/]�]�10 ]q]qY++++++@
  �/�l�/�l ?+?+9/39/301Y#" 4632&&#"326<�����r鉭��Z����j����
����kl���  \���� 0A��+XA '��  @ V &��  @ V %��  @�V�@�V�@�VA@ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @�V�@�V�@�V�@@(Vccst%'59CILED$F'SY\W(�#���U$���U%���U&���U'���U#����U$����U%����U&����U'���@FU(&$$'%64#D%E/Z V#U%ljkfeyzz}u$s%������$�%����CTX@-!&&	&)&  )21& e  -y�%-'%%���@U-	 ?�?�+9]99]9]9/�/�/�/�@-%$!%$"-@U�� -���@U P`p���@- BU���@BU-	&J	A��  @ V 	��  @ V 	��  @�V	& ))���U)���@U)2!�@�V!�@�V!�@�V!&&���U����U���@UT   1c[+N�]M�+++��+++N�++]M�+++�� ?�+?�+�]+��]+�99999Y10 ]q++++++++++]q+++++++++++ +++�--�3�l-�3�l ?+?+99//01Y7326654&'&$'&&546632&&#"#"$&\�_�}o�SP\;�lQig~��������98�X�z�������n�WBsDEg#a+7�eo�dí���[O33k(;�vu�st�   K��>  ��+X@ U]]	Ueko	e���U���@RUU'���1:1AMAQ\Ramaxx�� P`p��
 �� ���U���@U�A��  @ V ��  @ V ��  @�V@��ܴU���U���U���@	'*4�����%&4����#40���  @�V3�@�V�@�V�@@V$@$*4?O�@�V�@@+V UUUUUU47+N�++++++++]+M�+++�+Nq++�q++++M�+++ ?��]++�?�9/]<�q<99910] ]+++qr@  P p � � 0 p � � � �   �/@l 0
�/�l
�/�l
 ?+?+9_^]/+3/]q01Y#"  32 !326!&'&#"^�,��������
��c���Q8V�|�V��(���� ��h��Ch�   �  &> #o��+XA� ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ���U����U	���@M4%��	�� ��  #	 	##
�%�%�%%%�UU���@UU���@UUUU����U����U�]��@�V�@�V�@@V%�U���@UU���@UU
U���@UU����U�]� 3#�@�V#�@�V#�@@V#%� � �  ? O  ���@U U U U U ����U ���@U 
U U $%�x�!GP++N�+++++++++]qr<M�+++��+++++++++]�+++�++++++++++]�NEeD�qr ?<<<??<M��99910Cy@& +++�] ]+++++++++++++++++++++++++++@


 
�0�l	�0�l ?+22?+????01Y336632632#4&&#"#4&#"��2�jv�~ʞ��#\>p��XdL�:&�N_bX����'�l_:�����xxP����   M���  *鰅+X�CTX@_(@"
 %���@UUUU/+++�/+���� ?�?�9/]��]10@-kD@DD ZT kddjd tu���� U'���U#���@U! U(@P�_  �h@	"�8� �%A��  @ V %��  @ V %��  @@V%s@!#40 ���U�,
�8��@�V�@�V�@ V 9@?_o�@�V�@@VUU�$�+ǋ+�++++]�+++��+]q+�+++�� ?�?��]�9/]�10�C�@PX� ��' # !���8888Y++++] ]Y�
(�/�l"�/�l�/�l ?+?+9/+29/01Y&'&#"6632#" 763232654&#"��,IkVAUbA�g��wЄ��䝉���7O�Nr��{z�Sj0M0>��c`��Ҋ�~K|������]�Y�����  �  �� 
��+X�
�@�V �@�V
�@�V �@�V
�@�V �@@!V@4k���	 	�
 ���@
!#40    ���U ���@U U U ���@U U U @4���@!#40 @�<� +N�]q++�+++++++]q+<M�< ??9910] ]+++++++@	@		 ??9/�901Y!#56673��A�T��/t{>|�G�_  U���  *Z��+X�CTX� %����U����U���@(UUU,+(O P���@U" ?�?��+]29/]�299/++/+++�����10�CTX� %���U���@*UU,+(O P" ?�?��]29/]�299/+/++�����10@G:L@#[W#flmg#z}������� � =��:)d(O_"�P  �h�A'��  @ V ��  @ V ��  @ V 9 ��  @ V ��  @ V ��  @ V 8@@!#40 �,�8� �%�@�V%�@�V%�@�V%s���@!#4 @�+ǋ+�]+�+++���]q+�+++�+++ ?��]�?�9/]�10�C�@PX� '�� #��!  8888Y ]q]YY�(�/�l�/�l"�/�l ?+?+9/+29/01Y732>54'#"54 32#"&4&#"326p�|aS}P66�m��Ə�{z��˥tx��|}�SznL�pVk�������������4��Ĝ���   X����  (��+X@�_&�&7##*-+&;<:&LLI&]U#X&o{z��� �� �� �� ��+ *;]��&�&%*&49&IIEE#K&VXUZZVW W"ifk&{&��&��&��Բ9 ���@09*:((& !(& $$	A��  @ V ��  @ V ��  @@
V&U���U���U���U����U���@UJ *�**!�@�V!�@�V!
�@@
V!& �@@VUU)c\+N�+++]M�+++N]�M�++++++�+++ ?�??�9999 3��]10++]] rq]]qr@  &&$($@$�2�l	�2�l ?+?+3/�9/�939301Y%&'#"$54$32%64&#"  327&'��r9���������E��F�n��m�y�����h\[e�]+�9{[�\��d����ڵ�ߍ/]�9�
���������';   �  *�  ���+X@  ����@�V�@�V
�@@V     U ����U ����U ����U ����U ���@
U ];\+�++++++]<�+++<�] ?<�<?10� �3�l  ??+01Y33!������    ��9�  d��+X� �޲9���@ 9���v     
� ����  �z+<��� ?<?<�.+]}�10]++� 	 ??01Y3���X��  �  ��  .��+X@ekKK[[  A��  @ V ��  @ V ��  @�V&���  @@V
UU���@U  �@�V�@�V
�@@V     U ����U ����U ���@U U ����U ���@
U ];\+�+++++++]<�+++<Nq]�++++M�+++ ??<�<9/<�<10] ]��3�l �3�l ?+?9/+01Y3!2!!!2654&'&#!�)�Ml�Y�����{��]L1����e�m������\�   U��!� ��+X��@�V�@�V�@�V�@�V�@�V�@ V�CTX� ��@U
��@ ���U���U/++�/�/ ?�?�9/���+10@4UUKy������	*
���@
@�@����@  �@_o��A��  @ V ��  @ V ��  @@Vs@!#40 ����U� �5 � 8���8  ��@!#4  @  �����+�]+������+]q+�+++�]< ?��]�?�9/]9/]��.+}� 910�C�@PX�	00��� ��8888Yq]++Y++++++@  
�/�l�/�l�3�l ?+?+9/+9/339/01Y732654&#"'!!632 #"&U��l����W�(�����O���t�������Ģ��O?��v\���Ǒ��  	  F� 
C��+X�,�@�V�@�VA@ V ��  @ V ��  @ V  ��  @ V ��  @ V ��  @�V�@�VA@ V 	��  @ V ��  @�V
�@ V  ��  @�V$�@�V$�@�V
�@ V  ��  @�V$�@�V$�@ V�CTX@  
 	/����33 ???910@$/* (%
/0`��	��� P�CTX�	  ??99@$
		   	� 
 	ee���@(9P���@@(9_���@ P0`������`�+�]q�]q+�]q+�� ?<�?<�.+}ć.+}�K�SK�QZ�C�@PZX� 
���	������888888YK�(SK�6QZX�  ��8YY10]q] ]Y+++++++++++++++++ +++�  ???301Y!3673A���}."-������׀pxx)�F  (  �& +X��@ V ��  @@V��24���@	4>!4���@J!4)(	/99
IFFI	O\TTZ	Plccj	{t{	���	��&)+	9������4,9	���@#9:	


%a+
a ���@	U+
���[   ��@U"� @`�����@$Ut 
~� O o �  U t!|�++N�+]q<M��+]q<�+�<<� ?�+<�?<��99�.+�}��+10+++q] ++++C\X�)&���@	424��·!4>!4 ++++qY]C\X� �޲9	��޲9	���9	=	���9	���@
999++++++++Y ++�
 �0�l 
�/�l ?+3?+2201Y35#!5!63!(�sX�Od��oyj��w�^{	�  ����  ��+X@{$5E?�"3Bp�:<<LL]]X]^jlhnn���������� //0?@LPf��� 
A��  @ V ��  @ V ��  @@"V$�@`�@UUU����U���U����U���U���@Ut�@�V�@�V3 �@�V �@@V U U 3�@�V�@@V%�����?O����U���@UUUUU����U���@UUUG7+N�++++++++++]qr<M�++�++++�++�++++++++]q�+++ ?�??�?9910 ]]qr q�
�/�l�/�l  ??+9?+2?01Y!#3632 #"'32654&#"-��r�b�q@��k4U�v��uv�����O��s���֝��U������  �  <�  
��+X�
�@�V
�@�V
�@�V
A@ V ��  @ V  ��  @ V ��  @ V ��  @�V�@�V�@�V�@�VA@ V ��  @ V  ��  @ V ��  @ V ��  @�V�@�V�@�V�@�VA@ V ��  @ V  ��  @ V ��  @ V ��  @@7V	6UO	�	�	�	�	�	�	 		p	�	�	�	�	�	�	�	
	 	���  @@*V~ 
% �������  ������U���@UU
UU���U����U���@
UNGP+�++++++++]qr<�< ??<?�+999910]rq+++++++++++++++++++++++++�
 @  ?�??01Y533��������&��  F����  ��+X@|
%4D55WT
RSgde	c`�����������+<<Kp�.$.:5KEFIW
Vg����  
A
��  @ V ��  @�V3 ���  @�V %A��  @ V ��  @ V ��  @@$V%�@`�@U@UU���@UUU���@UU���U����U���  @�Vt�@�V�@�V�@�V$�@�V�@@;V����?OUUUUUU4P+N�++++++]q++M�+++�+++++++++++]q<�+++�+<�++ ?�?<?�?<9910 ]q] q��/@
l 
�/�l  ??+?39?+01Y!5#"&&54632332654&#"8e��ujԃ`�/�� �uv��{x��������QA�F�������   �  �&   N��+X@  	<<
</ ?    ���+�]q� ??��999910� @ /�?�01Y5353����Y������  ���"� ;��+X@
&XX����@44;FJv�� ���	A��  @ V ��  @ V ��  @�V&���U���@UU���@U]  P`p��@�V�@�V
�@�V& 

���@
4
 U
����U
����U
���@U
U
����U
���@
U
];Y+N�++++++++]�+++M]]q�++++M�+++ ?�?<10]+ ]��3�l	  ???+01Y3#"$53326`�d������p�G�}ֶ���������O����b�   �  �� ɰ�+X� ���4���@U%5E����@4 
A��  @ V ��  @ V ��  @@'V%	@364�	�	@U@U	(U	U	���@U	U	U	���@U	U	���@U	
U	����U	N���@464��p����@�V�@�V�@�V% ���@364�     � �  ����U ���@U U U U ���@U U U NGP+�++++++++]q+<�+++<]q+�++++++++++++]q+�+++ ?<?�?99910Cy@% +++� +]++�
 
�0�l  ??+9??01Y33632#4&#"��~�v�K�ukP�<���]���_��{S�}��  �  Z�  N��+X@ C A��  @ V ��  @ V ��  @@V& 	@U	 U	
U	U	���@U	�@�V
�@�V�@@V     U ����U ����U ����U ����U ���@
U ];\+�++++++]<�+++<�+++++]�+++ ?<�<?<�<10Cy@6


!!!
! ++++****�]� �3�l �3�l ?+?+01Y3!2#%!2676654&'&#!���Z~YtsNz�ͅ��9��1EM�lN����Lb��ħ���a2�61E���*   <  � '��+X�CTX@	U����U���@	U���@UUUU��@
  9/��9/� /�++++?�+++�210�CTX@	U���@	U���@UU���
���U���@U  9/��9/++� /�++?�++�210@G;;�����IYTkdzz�������
����O�� ���
A��  @ V 
��  @ V 
��  @@V
s�  @!#4��   8@�?_o�$ ���+�]���+<��+++ ?<�<?��]�99�.+}�910�C�@PX@	��� �� �� 	�� 88888888Y ]]rYY@	�3�l�/�l ?+?+939/01Y%!&76676654&#"'6632�7%��神{�������H�¢\��A<c�~��fk������X����a1  U���  ���+X�CTX@
	���U	���@U	 U U U /+++�/++� ?�?�10�CTX@
	����U	���U	���@U	 U U U /+++�/+++� ?�?�10@N����	ELJCT\\Rkkclk`ywvz��������A��  @ V ��  @ V ��  @@Vs	@!#40	 			A
��  @ V 	��  @�V	��@�V�@�V�@�Vs ���@!#4  @  �@�V �@�V �@�V �ǋ+�+++]+�+++�++]q+�+++ ?�?�10]q ]�C�@PX� ��� ��� �� �� �� 88888888YYY��/�l�/�l ?+?+01Y632#"'&326&#"UkӠv�tBjӡ�y���||��~|J]�=�_�������í�������hj�i�    � 
 ��+X� ��  @�V�@�V�@�V�@�V	�@�V
�@�V�@�V�@�V	�@�V
�@�V�@�V�@�V�@�V�@�V�@�V�@�V�@�V�@�V	�@�V
�@@7VXh���LL� 
 � ��  �@
   �
�f�
@4
���U
���U
���U
�7@@"#4�!5����@4  ���U���U�����+�++]+�++�++++<��< ??�<�<9999�.+}�10C\X� �޲9���@39"-9<++++Y] ]C\X@@9�P9@&9"9@-9+++++Y+++++++++++++++++++ +�	�2�l  ??9/+332901Y!!533#������ƴ�5_���J�����k  0  �� ��+X��@�V�@�V�@�VA@ V ��  @ V  ��  @�V�@�VA@ V ��  @ V  ��  @@V 	�s� �� /��   ���@U U ���U ���U ����U ����U �s���+�++++++]<�]<��]�<< ??<�<10++++++++++� �3�l ?+2?01Y!!5!!�������   ��i!>  հ�+X@t-=K? �  )#22Bp � ::JJY[\\jkimk� ������� � #++5:FJZ��� A��  @ V ��  @ V ��  @@V$�

@
`
�
 @U @U
���@U
U
����U
���U
����U
���@U
t33�@�V�@�V�@@V%  �����?O���@UUUUU����U���@UUUG7+N�+++++++++]qr<M�+++���++++++++]q�+++ ??�??�9910 ]]qr q� �/�l�-�l ?+2??+9?01Y36632#"&'32654&#"��:�h��ju�{Z�.�vx��ts��i��QQ�������L:����������    �� ^��+X@	/0@p���(�����@4
+ 
���@�V@�@�V�@�V�@@V% � ����184 ���@+4� @U@U U (U "U ,U ���@U U ���U ���U ����U ��� ! �
 ++�+++++++++++]++<�<<�+++�+�] ??<<<�<?�9910Cy@		 ++*��+q] r� 
�-�l
�2�l
 ?+?+32?01Y3#535476632&#"3#����vL\82RD����qk4FW�
F`b��f     �& 
c��+X� ��  @�VA@ V  ��  @ V ��  @�VA@ V  ��  @ V ��  @�V�@ V�CTX@ 

 	$U/+����33 ???910�5 "9
���@9	44���4���4
���@	!4 (!4
���@	"%4 "%4
���@~(.4  (.4) (	&
9 5
H G
VVYX	ffii	x wwyx	w
������	� �	�
� �
� ��
� �
� �
� �
� �
,
 
 
( &
7
O @
	@4@4�CTX@	  
���@U
 U 	���@UU9/�+��+��+�+ /??910@7
%	
		
 %  

 
	
	 /"@@@	�		��@��@	 @"��+���]�]��]9999 ?<<<?<9�.+�}ć.+�}�Y10 ++q]++++++++++++ ]Y++++++++� 
 ???301Y!3673��l��%+��n&��goTv���  �  �� P��+X��@�V�@�V�@�VA@ V ��  @ V  ��  @�V�@�VA@ V ��  @ V  ��  @�V ����8=4����344����-04����()4����#%4����4����4���@*4 ��   � � � / @ P � �   � � ���@U U ���U ���U ���@U  U ��Y+�++++++]C\X�� ]Yqr<�]++++++++< ??10++++++++++�  ??01Y33����F  �  � �  7��+X@< 
<_ o  � �  ���+�]]� ?�10�@  ?�01Y353����   �  � 	��+X��@ V ��  @�V���@
4U���U���@#BUBU 		A��  @ V ��  @ V ��  @�V ���U���@UU���@U]  P`p�	�@�V	
�@�V	  ���@4    U ����U ����U ���@U U ����U ���@
U ]
;Y+�+++++++]+<�++<]q�++++<�+++< ?<?<9999�.+�}ıCTX� ��4 4 ++Y++10+++C\X�@F9����F9@29����29"9��޶9"29��޶29"#9���@#999����99����99����9+++++++++++++ ++++Y ++@   ????9901Y333#����������F���    v� ���+X� ��  @�VA@ V ��  @ V ��  @�VA@ V ��  @ V ��  @�V�@�V
�@�V�@�V�@�V�@�VA@ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @@3V) &)&9 696I GIGX WXW��BUBU�CTX@3+44DDKTT[ddktt{   ?????9]99@
	��<�  ��<� ��<@Z	     		 	 		 A	Q   Q Q @ Q�  ����+N�]M����NEeD� ?<<<?<<<<<999999999�M.+�}ć.+�}ć.+�}ć.+�}�+++��ć<ć�ć�ć�ć��K�SK�QZ�C�@PZX�
���88YK�%SK�*QZ�C�@PZX�  ��8Y K�SK�QZ�C�@PZX�@@88YY++10r] ++++++++++++++++++@  ?3???3?301Y!3673673#&'��{��$8
��O#-���n���'����?���$�������F]� eG��  V��� +���+X�CTX@@U ���@+U)#


)))#  U &���U&/+�/+�/�/�/ 9??��9/���9�+2�+210@0E�EWvRljduy����
#���@  � ) 5��� h@	)A��  @ V ��  @ V ��  @@Vs_ o  U �A��  @ V ��  @ V ��  @@Vs&@!#40& &&&����U&�-�8���8  ��@!#4  @  �,����+�]+����+]q+�+++�+]�+++ ?�?���9/��]�9910�C�@PX� ���88Y] ]qY@	 #
�/�l)�/�l)�/�l ?+2/3?+9/+3299/301Y732654&#"732654&#"'6632 #"&V��k��}3Ls��ji��!�x�kfd������������|��x}c��� ��g�d_�.������   ���� � 
 d��+X�
 ��P@&<
< 
< 8:O _ o  �  ���+�]���<< ?�<<���910�@  ?�/�01Y353'667��PW296��q�&Ma[  �  �� 	 Ӱ�+X@"�  �  	�@�V	�@�V	
�@@V	     U ����U ����U ���@U U ����U ���@
U ]
;\+N�+++++++]<M�+++<N�]M� ??<�<9/]<�<10��3�l �3�l ?+?9/+01Y3!!!!������P���:��f  a  �  ���+X@�	 ��@0	s@!#4O_os	� O__?_o����+N�]q<M��N�q+<M� ??<�<99910q]�	 �3�l ?+3?01Y5! #67a����K6�����������ۭ�ǜ  A�jm  =��+X@ppMM# p  p�+N�]� /M�10 q]� @ /�01Y5!A)���  �  ��   *ް�+X� ��@)UF#V#f#s	�	iup	s��'	'*	A��  @ V 	��  @ V 	��  @@V		**))  A��  @ V ��  @ V ��  @@
V&U���@%UUUUUUT%A��  @ V %��  @ V %��  @@V%&U
U���@U,�@�V�@�V
�@@V     U ����U ����U ����U ����U ���@
U ]+;\+�++++++]<�+++<N�+++M�+++�+++++++�+++ ?<�<?<�<9/<�<9/+++99910] ]+�	*�3�l �3�l �3�l ?+?+9/+901Y3!2#!276654&&#!!27>54&&#!�&��sfg��W�����=�8JKF����m^&CZ:T�����Y�e^�3'��g�`1RfMIo)��8kFRy1  S���  # 0ư�+X�CTX� .���@U..!(	U	����U	+���U���U���U���U���U���@U$UUU/+++�/+++�/+++�/++� ?�?�9/+�9910�CTX�	U	����U	+���U���U���U���@"U$UU ..!( ?�?�9/�99/++�/++�/++�/++�10@M5)II&��0	0} }|tqruz� ���������  .�..!(A��  @ V ��  @ V ��  @�Vs�		Ag +��  @ V +��  @ V +��  @@V+s@ #40 ���2�@�V�@�V�@�Vs��g�$�@�V$�@�V$�@�V$s���@!#4 @�1ǋ+�]+�+++�]�+++�]q+�+++�]�+++ ?�?�9]/�999910�C�@PX� "�� ���  /���- &���) 88888888Y]rq qYY� .�/�l(�/�l!�/�l ?+?+9/+9901Y&&54632 #" 54632654&#"32654&#"jpl���km���������b�kh��fg�:I�S�����)�j��ߠf�),Ĉ�� ���Th��_c����M�O�����   c����  T��+X@K��� @OO@XX	WU_Z_VW��	A��  @ V ��  @ V ��  @�V& ���  @ V ��U���U���U���U����U���@U��@�V�@�V
�@@
V&   �@�V �@@V U U c\+N�++++]M�+++N]�+++++++]M�+++ ?�?�10]q ]]]q��2�l	�2�l ?+?+01Y !2#"$7 32 4&#" c�6�F������������y�����m����������Z�����4����    F� `��+X��@�VA@ V ��  @ V  ��  @�V�@�VA@ V ��  @ V  ��  @�VA@ V ��  @ V ��  @ V 	��  @�V�@�V�@�VA@ V ��  @ V  ��  @�V	:;	���4���@444	��س!4���@;!4(!4&)*
/hhh�			
U	 


	���@U  �@	

	 �@		R@
�

��@  RO���@	 U ���@U U ���U ���!`�++�++++<�]��<�]�� ??<<<�<99�.++}��.++}ć�ć��K�SK�QZ�C�@PZX�	��� ��8888Y10 ]]C\X@		"9"9��ޱ9+++Y++++++++++++++++++++++++++��2@
l 	 ???9/+301Y!3673;���!PEB^���mM�F||s������     �& �  ��  @�V�@ V ��  @�V�@�V�@�V�@�VA@ V ��  @ V  ��  @�V�@�VA@ V 	��  @ V ��  @�VA@ V ��  @ V ��  @�V�@ V ��  @�V�@�V�@�VA@ V 	��  @ V ��  @�VA@ V ��  @ V ��  @�VA@ V 
��  @ V ��  @�V"A@ V 
��  @ V ��  @�V �@�V"A@ V 
��  @ V ��  @ V�CTX� ��@UU U
��ԴU���@U U
����U���@/U@U
 
 
U

U����U/++�����+� ?????910 +++++++++@*)
J[� U
���U���U���@	!4'4	���@�$4		 	 $ %*+4 5:;DG@MKCGJ[Rkdgyzt�����	(( ('('/8 7w�������� �����	�����	UUUUU�CTX@
 %%%  %���@7U%*U
&
+TR
\l|�

 
 
 ?????9]99/+�/+�9���999@	


��K�  ��I@f
 � +
%+


 %   

 
�`p���@
 O
o


�U@	Oo�U@`p������f+N�M�]]�]q�]q�]]� ?<<<?<<<<<999999999�M.+�}ć.+�}ć.+�}ć.+�}�+++��<<�ć�K�S�C�@PZX�  ��� �� �д 0 ���88888888YK�4S�C�@PZX� �б088YK�!SK�3QZ�C�@PZX� �� 88YK�SK�QZ�C�@PZX� �ж   ��в0��� 8��� ��8888888888YK�SK�QZ�C�@PZX� ��
   888YY10C\X� �Զ9 ,9 ��Ա9+++Y+++++]qr+++ +++q]]Y ++++++++++++++++++++++++++++++++++++!367373#'K����?3���5=������)�&����n����f��|���     �& +��+X� ��  @�V�@ V 	��  @�V�@ V�CTX@	
 
U/+ ????910�"9���@P9Z��������	@9	5:��/WYYX��
��������	���
�CTX@ U���@U  

 ?<?<99++99@f			 	

� �	% 	  	�%
		 
OI~"
a	~@
��@P��C@ ~"O  I|�+�]���]������] ?<<<?<<<�.+]�}ć.+]}� 99�ć�ć���<<<Y10C\X�9���@9"9"9��޲!9���@
9"!9	@9++++++++Y]q +]++]Y++++@ 
 
	 ????9901Y336773#'����.,%�������:��(��G0B3����JY�]   B�Q�>  *)��+X@`,%LE	,&,#96JFVXh�
�.#,'>#>'L'�,�,6!6)?,FF!E)T!T)ic!c)`,�,�'�!�#�'���(��@  0 ` p � � �  �}@
E"
3%3
A��  @ V 
��  @ V 
��  @@$V
%�@`�,@U,@UU���@UUU���@UU���U����UA
��  @ V ��  @@Vt% "�@�V�@�V�@@V$����?O�@�V�@@.V UU"UUUU+,t!4P++N�++++++++]qM�+++���++++++++++++]q<�+++��< ?��?��]�?��?<10]q ]q@
    �/�l
"�/�l
(�/�l ?+2??+9?+9/_^]01Y32676'#"5463253#"&32654&#"f�2Ct}�v���nэ�z�e۠�Ꙧ}|��zx�XQ%2dZ7��<ݘ����j��x�*�������   w����    ' 38��+X@
��h��@1+�� 	e �@%(�� e .��%�� +  1��"�5��   �@	   u4WZ+�]������� ?���<<?<<���9999�.+}�10Cy@R3)+ 3 1-&+ /$1 
 *(2!(,'. 0#.    ++++++++++++++++�]�(�e�%	�e@.% ?3??33/�2�201Y4632#"&"32654&34632#"&"32654&w��������9CYZBDYZB"���垗������:DYZBEYZZ��ſ����t��st��s�s	�����ſ����t��tt��s   I�-A * 1 82��+X@%|0,66/F!U!P/]6jc/zw!s/{6�!�/�61��޷9  $4,���@, #4j8*7 *0! 710! 7!00�770!72���P��� ���+�5@
� *�7�
2�5�)��8 ��5s&���@
90&@&�&&�R@*  8822))*��@ ++11

0 @ � �  �@	.so�� 8@?O�9ǋ+N�]M��q��]<<<<<<�<<<<<<<�]+��� ?��<�<?<�<�����]�9�.+�}�10Cy@J!7$%#%"%&7!5O3(5O,.O 0.O 6%8O! 784'2O 32-+O,+/1O 01 <<+<<+<+<<+++++*+*��++ +]]@ 81@+  )2�/�l)
�/@	l�/�l+�/�l ?+33/+2/3/?+2/3?+3/9/�3201Y5.'7&'&&5476753&&'6654&'���{
�5LjotV]�[�j�\v�eX�,Tj9�jiyg{ji�a�ӴW"�D`=A0�l�wPVVMb�jq��"%j�U��	�(�]\|%��sbw/   	  I� X��+XA ��  @ V ��  @�V�@ V ��  @�V�@ V ��  @�V�@�V�@ V ��  @�V�@ V 	��  @�V�@@*V&))8788	8:57
 !4 !4���!4���!4	���!4���@l!4 !4 !4ww&)(*&6:::5HT]\ZTgejkieuzyzww���
�������������,���@UUU����U�CTX@ 
U���@
U  
 ?<?<99++99@]		 	
	
  	  	 
		 / @�_� 
�
�

���_���@
�@P��_@
  �!`�++N�M�]��]�]�]NEeD�] ?<<<?<<<�M.+�}ć.+�}� 9999�<<ć<<ć<<ć���Y++ ++10] ]++++++++C\X� ��@9"99��޲9��޲9���9"9	����9���@9@9@9<=	<=���@.9"9!= !<
!=!<= <
=<+++++++++++++++++++++++++Yq]q+++++++++++ +� 	 ????01Y33673#&'	7��
S#1C'���+���!1������u?PW��M��-5P�  7��a� ��+X@egtu��	����U��		A��  @ V 	��  @ V 	��  @�V	&

A��  @ V ��  @ V ��  @�V&���U���U����U���U���@U]  @P`& ���U ���U ���@
U K�Y+�+++�]q�+++++�+++<�+++ ?��+?10 ]� 	�3�l		 ??+9/301Y7326653#"&;�pcIj(�Y������|Cs~����j�   �  "� F��+X� ��@4	
�
�

A��  @ V ��  @ V ��  @�V ���U���@UU���@UU]��@�V�@�V
�@�V    ���@
4  U ����U ����U ���@U U ����U ���@U ]  P`p;Y+]q�++++++++]<�+++<]�+++++<�+++< ?<?<9]/<�<10+�
�3@l   ????9/+01Y33!3#!���������Z�F��M  m���� %���+X@`'^$$ !% ���@U!	&'%$A��  @ V $��  @ V $��  @@V$   '`���U���U��ڴU���@Ur�''�@�V�@�V
�@@
V& 

�@@V
U
&c[+N�++]M�+++M]�++++]<M�+++<9/ ?�?�9/+<�<999910Cy@D#&%&&%&#%! ! ! "%!!!	!! $!!  ++++++<<+++++++++*�] ]�@$$! �3�l!�2�l	�2�l ?+2/3?+9/+9/�01Y5%#"$54$32.#"3267Lm��Р�����P۟�&�!b�o��w!8��~�>?���rs�^��s�g��0p�MQ�O������a7         l    �  	  4  �  V  �  �  �  �  (  �  !�  $h  (>  *�  .�  1  2B  5"  7�  8t  8�  :v  <�  ?X  A~  C�  F  H�  I  J�  L�  NF  P�  S4  U�  V�  X�  Z�  ]8  ^�  ^�  a  dv  f�  g|  hx  i>  i�  k�  oP  oP  q  s�  y�  |X    ��  ��  �n  ��  �:  �^
endstream
endobj
10 0 obj
<<
/Encoding /Identity-H 
/ToUnicode 24 0 R  
/Name /F-0 
/DescendantFonts [25 0 R ] 
/Subtype /Type0 
/Type /Font 
/BaseFont /SUBSET+ArialMT 
>>
endobj
28 0 obj
<<
/ModDate (D:20250109191019) 
/CreationDate (D:20250109191019) 
/Producer (Ibex PDF Creator 4.7.3.0/7447 [.NET 3.5]/R) 
>>
endobj
xref
0 29
0000000000 65535 f 
0000008468 00000 n 
0000007550 00000 n 
0000011309 00000 n 
0000008602 00000 n 
0000008637 00000 n 
0000006950 00000 n 
0000007467 00000 n 
0000007632 00000 n 
0000000020 00000 n 
0000084409 00000 n 
0000038422 00000 n 
0000038256 00000 n 
0000007207 00000 n 
0000007976 00000 n 
0000002121 00000 n 
0000007610 00000 n 
0000008430 00000 n 
0000008319 00000 n 
0000008371 00000 n 
0000011330 00000 n 
0000011880 00000 n 
0000012351 00000 n 
0000012581 00000 n 
0000038537 00000 n 
0000039113 00000 n 
0000039608 00000 n 
0000039834 00000 n 
0000084571 00000 n 
trailer
<<
/Size 29 
/Info 28 0 R  
/Root 1 0 R 
>>
startxref
84712
%%EOF
```

## uploaded_files/6999QN_document.pdf

```pdf
%PDF-1.7
3 0 obj
<</Type /Page
/Parent 1 0 R
/MediaBox [0 0 612.00 792.00]
/Resources 2 0 R
/Contents 4 0 R>>
endobj
4 0 obj
<</Filter /FlateDecode /Length 559>>
stream
x��V]o�0}ϯ�O�����!ƨ���R��*�Ҧl��~7	1���H�e������ؔ({�p��	��Z``YF_�|c���_�O"������@`�=�{D�2�� Y���d>��}����(�>=@r�N�#�O��r��je���.���E
��t�s�*�g�;X�W�]���֪�aB�(>�8N��y���s��f���cN��q�U�,W[��a���&R�x�u�sġ��9��9M�!�^�J[�;��Q��l�_U�}��(�ؑ��_�����?C�7�SD���m-��B��D֩�j��6�����$G%Q��mh�8����D[C8-D���st��X_;Usaw0�F���B
Ib[��q���*Zb�4L7#�־�E��6nPB^n0��k���b����4�C%=	Y�û�<��R����h�}��.4јqv��Ad;�n���mɉ��TQ�r��*�GH��)*芏���(������W�����Bm@YAbQ��0����%���Ĉ0psX#0蜮Y0�&�9{ˏ��Ӎm
endstream
endobj
1 0 obj
<</Type /Pages
/Kids [
3 0 R
]
/Count 1
>>
endobj
5 0 obj
<</Type /OCG /Name (�� p r i n t)
/Usage <</Print <</PrintState /ON>> /View <</ViewState /OFF>>>>>>
endobj
6 0 obj
<</Type /OCG /Name (�� v i e w)
/Usage <</Print <</PrintState /OFF>> /View <</ViewState /ON>>>>>>
endobj
7 0 obj
<</Type /Font
/Subtype /Type1
/BaseFont /Helvetica
/Name /F1
/Encoding /WinAnsiEncoding
>>
endobj
2 0 obj
<<
/ProcSet [/PDF /Text /ImageB /ImageC /ImageI]
/Font <<
/F1 7 0 R
>>
/XObject <<
>>
/Properties <</OC1 5 0 R /OC2 6 0 R>>
/ExtGState <<
>>
>>
endobj
8 0 obj
<<
/Title (�� I n f o r m e   d e   V a l o r a c i & o a c u t e ; n   d e l   I n v e n t a r i o)
/Author (�� W e b E R P   4 . 0 0 R C 1)
/Subject (�� V a l o r a c i & o a c u t e ; n   d e l   I n v e n t a r i o)
/Creator (�� T C P D F)
/Producer (�� T C P D F   4 . 9 . 0 1 4   \( h t t p : / / w w w . t c p d f . o r g \)   \( T C P D F \))
/CreationDate (D:20241126065152-06'00')
/ModDate (D:20241126065152-06'00')
>>
endobj
9 0 obj
<<
/Type /Catalog
/Pages 1 0 R
/OpenAction [3 0 R /FitH null]
/PageLayout /SinglePage
/PageMode /UseNone
/Names <<
>>
/ViewerPreferences<<
/Direction /L2R
>>
/OCProperties <</OCGs [5 0 R 6 0 R] /D <</ON [5 0 R] /OFF [6 0 R] /AS [<</Event /Print /OCGs [5 0 R 6 0 R] /Category [/Print]>> <</Event /View /OCGs [5 0 R 6 0 R] /Category [/View]>>]>>>>
>>
endobj
xref
0 10
0000000000 65535 f 
0000000746 00000 n 
0000001138 00000 n 
0000000009 00000 n 
0000000117 00000 n 
0000000804 00000 n 
0000000919 00000 n 
0000001032 00000 n 
0000001297 00000 n 
0000001741 00000 n 
trailer
<<
/Size 10
/Root 9 0 R
/Info 8 0 R
>>
startxref
2105
%%EOF
```

## uploaded_files/7603IX_document.pdf

```pdf
%PDF-1.7
%����
1 0 obj
<</Pages 2 0 R /Type/Catalog/ViewerPreferences<</HideMenubar true/HideToolbar true/HideWindowUI true>>>>
endobj
2 0 obj
<</Count 1/Kids[ 4 0 R ]/Type/Pages>>
endobj
3 0 obj
<</CreationDate(D:20201214134944)/Creator(PDFium)/Producer(PDFium)>>
endobj
4 0 obj
<</Contents 5 0 R /MediaBox[ 0 0 612 792]/Parent 2 0 R /Resources<</Font<</F1 6 0 R /F2 7 0 R >>/ProcSet[/PDF/Text/ImageB/ImageC/ImageI]/XObject<</img0 8 0 R /img1 9 0 R /img2 10 0 R >>>>/Type/Page>>
endobj
5 0 obj
<</Filter/FlateDecode/Length 997>>stream
x��UɎ�H��qiu�T�3�dq�0^��.�J�V_0d{aS^4�U�/s�?�Ü�֧���.��-�t���ˈ�7�)��n@�*4��)O�[�c�_
kij�9蜀��J��6H���m����q��Y��oQ0PM�_�|c"�d�l6%�-�IR��m�G3eㄌv+�`�l�p���X�FOѶ�v���>&S1�m�V���we��*w�����q�wl/�=#�P2 �S�3S㟢?�c*9�c���2�{'M�P�b3��o�kji*&e������������������`d;�?��б���.p��>�J
����047�GR}�]��N�3z<A���cv����ਸ਼z9��/�;�B3� �j�R�qI5f�!J���?rw��[]�ѵ_`���Q?�8��/��w(t� @�����uzX& �#˘�IR��#�Ǳ|�m��{6��0�Ќ~⨬L�j���{�g{S'��cY'�p�sEb����'5��'7_���a�l�����_��+�X�E̖l�K�ح��8P���������ϊxM�b�~����v��X"CI&
��s�x�Q/���L���<LEऐ��[�
k���5:�n<�ݧ㰬�*Z���n )x�]�]p��tc(�\�G8·C������t7����|���{�6�I���IbXD�{�)�i�d?珀�E�M���B�_��<.�R���b_-�aI�� *�H K��D) �q��m�������^��X@/�8-�UoKqe�ȋ�����f�dY�1�9�E�r��d�I.�,�?�1��P�[��z��a�tݠ�~�fƱ٦����aҚ7j���,�u��kYLb�k*&V�̾gI\VbX����JZc"iV��Nd�^���g�B�u%�!�nWR��s�L�Y����k��+�Z��� ��:��{��l�-��
���W�k�y^�￐MqFw���I^�
endstream
endobj
6 0 obj
<</BaseFont/Helvetica/Encoding/WinAnsiEncoding/Subtype/Type1/Type/Font>>
endobj
7 0 obj
<</BaseFont/Helvetica-Bold/Encoding/WinAnsiEncoding/Subtype/Type1/Type/Font>>
endobj
8 0 obj
<</BitsPerComponent 8/ColorSpace/DeviceRGB/Filter/DCTDecode/Height 73/Length 27046/Subtype/Image/Type/XObject/Width 207>>stream
����IExif  MM *                  b       j(       1       r2       ��i       �   � -��  ' -��  'Adobe Photoshop CC (Macintosh) 2017:01:17 09:38:15     �    ��  �       Ϡ       I                    "      *(             2             H      H   ���� Adobe_CM �� Adobe d�   �� � 			
��  8 �" ��  
��?          	
         	
 3 !1AQa"q�2���B#$R�b34r��C%�S���cs5���&D�TdE£t6�U�e���u��F'���������������Vfv��������7GWgw�������� 5 !1AQaq"2����B#�R��3$b�r��CScs4�%���&5��D�T�dEU6te����u��F���������������Vfv��������'7GWgw�������   ? ���1��,����>�k{���?��>���+��%H����n�
��-�o�z-��������^���3�G֌�n���{����9e��.ֺ�����c��}����C3�� L}��:��N���E�̫klsk��ٿH��ߺ��~���ҩ�F�#�=<[��x��Y�#GZ��u�Z�M��\g0��O����.���zbu[=o�����b�o���[�#��3���EN�'�}�g��� �T������:V6ON{k�̦��懍��썮�]LX�;�b��u<�!K��kK],w��k*��I���`e:��~�� %�s2����]O��>�{qY[�҇�c�v�lw�۽o�?�� ��'�!�Q؎U�fS,x���w��������'�ԩcu������L~f]���K�mm�T?!��k�� �5�o��j�ԯ��?�oTsY�5u4mm����;��g�J� I���F�1��&?��%�q$܅�|[�Y����o���,�ϵ�`�8���M���[�� ��[�Ϭ~�X������b��zc46�^����6z�f��o�l� ��%��Ð	r�~������������f�40CKv�Z��3�\�^`�&8A���� N����Ta�+�����gd�cm���]Z�m-�� ;Ү����� ��/���� Zc�o���K}#;\��}m/o�!�˶V��Wg��W�n�}m��vٝ��>*��i�=��+/����%�99x��x%���5�=L����E�o�&����Fe�$�N'�e8�g�o��K)��_����nL�>��#%���S��h��s�k1j�f�� ��k�u�� =E�������]K���q��%�d��M��������S����_6<9pF�x��/��� FR����P��	:iA[�۾�=ޞβ1��a����o���m��k����
]�����М��A�� ��� �����9ޟ��_�	iR)��� ��� � �~;K��	�ď��r|N8�G,��%�Kܟ�M���$�W��Vh�n��!dyss'l��Wkw{��zVa��� �_h�  �9� Y�!}lk���k�Vza��o�q��Y���A��魪����J�=k}�yKַ�����?�V!�݉�Ő���UgZ�C�uo�8�c��z;�W�׬nv�So����j����x��M�6U{r��zw����l��lo�����Yw�?�o��)z��������� ����C��l�����:�9�nE?a`���� ���n�3���?�Z�z�[��o�?e����n��^����:�~��� �@����}�ǻ!��$AЕ'/� 1f͏��NI|D��P�T�b��_����� _V����z� Mk�c�k}G�Y5��7�� 7�J�z�C����ue�u�i$4�R!��^E�=���c�� ��.��;�	�y62�mw9�4��Xӌ��zm�ڿ�.7�ectg�b;�5�u|��YN<X�Ѻ�W���*����G�GX^����[ 02ɎZ߮���75�	�!�vk#PA�+P���}a��?�U��Э�-srYah%�s�ݾ��ͻ��տ���a}K��V�lƷ���ux��?��O��YzM��V.vmT^�-q�����go�jQр�=gOW�ޕ��n@�^��������{������E��;�6���������S�.g�?�;zn&7]���}u[{k'v=�Z�T���]g���[� ��W��;�}D��µ����Z�܊���c����Y�1X�������p�AcAk�L�Yb��=ɉC£�]<bf��w����ɽk��3�SY3�[{ �z��m�� O�v���*��K;��+30-�r��k]�V�{lg�*��� �y?V���zS�Ξ^oa!��Y��;(�� A�� �htK��� 7Z�j2�ܢ=�o�͕��\���j~Ok3�:�2���\QVe͚��e茺K���G;.���g�fܦa�Ͳ��{��#g�\���_X��R�Ρ��M����]mAmls�[\�ϻ����ml��uƊ���}��H�I�� ��J��S��6f7O����uTk����Z�;{��K?;�2�9�P�ģfC�J�X���|?��8Hi?g�������$I���e�v��r�=VY��2 #�k*����;���*��� �o��#��t� ���>i&��5?��{�/w�ޛ� ���>��?��1�E�6�^����f��<����O�TQE=M�;9�p���U�9�t�v>[��W�� ]G;��y=��Z¸�|B�� 	��,X%1�	���_�,���n�պE�F�^�d���kY��ݵ5��V=q�[�֌~���NqmT��]m��0�=�ce���!v�R2j��w��L| ܗ4Պ�M����l��{��W�u<F�<�;�t�Kr-i��%�!������ ���yxH�.>H��J�y̲�/	������������!���a�YM�n��N�al�� �w"3�V�Ռ��u�r̆�������b�m_�=�F�j� ��kbD~��Q3���ۻ�/ڸ�Gҿ�� 2D�O�?���d�{� |��̲���Sy�m�K*��ϵX)ǰ
� �'�X��:�������?Y��eWW�z�˽��m�̦��YT{��^�ok�l�����\?���_�� �%�S� (�W��� �I��>���*� ���8�'��� �[N�o� �i� �Ko�o֯�=K�y�~�;�k�_�[d����P���� �}+� a� �%��O?��EL�X�,�����`�������F_�&#��/LO~b�����<�������� ���>������u��mT��?`�km�X[n�}U�~�w�]�W�:���O�䶾���vo�4�����[k�oǫ�,�'�q�Ƴ�2�m�ù���0t#��ɝ����� ����mm�jQ�p������V3w����u��}_;?߇[�hu�cC�~r_����r+��6��� 4�X>��]�~̩�b��/mL;l���v�o���� 3b�͸a\�1�AȦ���VѴ���X���g�_�g�2?�Z��/�t ���9��S�[Z��sl���tWg����� �'�A���'�i��_�J/�U>�gG���Sg��;+�޽l������r��:�濜W�����qq�U��]�͆�C��y�]��c����[3-�±��V�^k{��k\��m���_�)ٗn=mm=�kX���f�[K�v=u��7�k�u�T۽/�z;� D��=	�N�����YY:]��Ǳ����d2�^�Qo}����힖�K"謹�n�m�u85�_�+�l����75��?O�ch��,��/ҫ�[�e}]cl���n�em�3ԫ��1��L� I�5��]��(�k�
���u>�����,������=K�1��&��.�I�Bq�J&� ��i��ҙ��r,�� c�W���n1�k�ޥ�ֳs=��C�x� W,�ʳ����c��Em��k62����n��{�z����^�"�11-B6��unl���T��7��n� �ݓ�� Ew�DF�]cݑwE�"����,x|����� �������w����|�e�25�iD�|�W�~'�P,%�O��<��,qk+���?����t��+��������h�H�o�2m�}���- o��)ev1�m�}vb\�}��V�@�,c��>�@sl�Հ�[jk���� >ꝋ���=*-� Z��}�X,蠵�����C�۱��}�T���9�� ��K��uu~��I���e�R�>�<'���`Y�(ǫ�m������U���mg�v��k���=�������Y��d����u�=�'&ӏU�w{���� �g���� �Z�]c����[d�in��%� J�U��7ѩ�����^���)��C��3Y�Ӛۯ�'5�k����� ��_	�� Ί�?͉{��G��p����.��e�(��l��ܐ�⁶�5ϱ����J�Y��-��W�� L�?m�OR�����o��[U�?�]�mwV��.e���YE��lջ�*Ỿ��X�A�=;��i����c���ކ۫�)a���UUU�突�l��(Ƨ}l�hK��/����w�K���NO�nE}ꍥ����]��]��N����v���Wg�U������ů��k�v����_��vߡ�C� ��uju]��6�}'mkh���mt�c2�z��oK��U�������uV��K[�nC�l��I���U��cwz�=��ޕ�}�����yӷ3�����Ѿ����Ւ�9���ݡ6�}m������b��s��
n�ͽ�N��V-yp5�;���o��T����k�=? ��q�,,5�4��;�TG�ow�5*��*$�Eu��a-cA�G��}���3ٽ7��5�]
e��2�9BB�#�N����T�ʩ$�ꤗʩ$�ꤗʩ$���H h|W��$��\�X�nk�y�c_�!�c�]�}�s���I����2��E���aqž��Mm��=��� �B�eI?�}/����� 9�d�u"\Fy � o�����Mߠ��).�k{Fip;_��p����{6/�G��_����� �~�x�_*��^�T��U$��T��U$��T��U$�� ����TPhotoshop 3.0 8BIM%                     8BIM:     �           printOutput       PstSbool    Inteenum    Inte    Img    printSixteenBitbool    printerNameTEXT        printProofSetupObjc    A j u s t e   d e   p r u e b a     
proofSetup       Bltnenum   builtinProof   	proofCMYK 8BIM;    -           printOutputOptions       Cptnbool     Clbrbool     RgsMbool     CrnCbool     CntCbool     Lblsbool     Ngtvbool     EmlDbool     Intrbool     BckgObjc         RGBC       Rd  doub@o�         Grn doub@o�         Bl  doub@o�         BrdTUntF#Rlt            Bld UntF#Rlt            RsltUntF#Pxl@r�        
vectorDatabool    PgPsenum    PgPs    PgPC    LeftUntF#Rlt            Top UntF#Rlt            Scl UntF#Prc@Y         cropWhenPrintingbool    cropRectBottomlong       cropRectLeftlong       cropRectRightlong       cropRectToplong     8BIM�     ,    ,    8BIM&               ?�  8BIM        x8BIM        8BIM�     	         8BIM'     
        8BIM�     H /ff  lff       /ff  ���       2    Z         5    -        8BIM�     p  �����������������������    �����������������������    �����������������������    �����������������������  8BIM       8BIM         8BIM0     8BIM-         8BIM          @  @    8BIM         8BIM    U              I   �    L o g o _ P o r t a l _ 2 0 1 7                                 �   I                                            null      boundsObjc         Rct1       Top long        Leftlong        Btomlong   I    Rghtlong   �   slicesVlLs   Objc        slice      sliceIDlong       groupIDlong       originenum   ESliceOrigin   autoGenerated    Typeenum   
ESliceType    Img    boundsObjc         Rct1       Top long        Leftlong        Btomlong   I    Rghtlong   �   urlTEXT         nullTEXT         MsgeTEXT        altTagTEXT        cellTextIsHTMLbool   cellTextTEXT        	horzAlignenum   ESliceHorzAlign   default   	vertAlignenum   ESliceVertAlign   default   bgColorTypeenum   ESliceBGColorType    None   	topOutsetlong       
leftOutsetlong       bottomOutsetlong       rightOutsetlong     8BIM(        ?�      8BIM        8BIM    +      �   8  �  i     ���� Adobe_CM �� Adobe d�   �� � 			
��  8 �" ��  
��?          	
         	
 3 !1AQa"q�2���B#$R�b34r��C%�S���cs5���&D�TdE£t6�U�e���u��F'���������������Vfv��������7GWgw�������� 5 !1AQaq"2����B#�R��3$b�r��CScs4�%���&5��D�T�dEU6te����u��F���������������Vfv��������'7GWgw�������   ? ���1��,����>�k{���?��>���+��%H����n�
��-�o�z-��������^���3�G֌�n���{����9e��.ֺ�����c��}����C3�� L}��:��N���E�̫klsk��ٿH��ߺ��~���ҩ�F�#�=<[��x��Y�#GZ��u�Z�M��\g0��O����.���zbu[=o�����b�o���[�#��3���EN�'�}�g��� �T������:V6ON{k�̦��懍��썮�]LX�;�b��u<�!K��kK],w��k*��I���`e:��~�� %�s2����]O��>�{qY[�҇�c�v�lw�۽o�?�� ��'�!�Q؎U�fS,x���w��������'�ԩcu������L~f]���K�mm�T?!��k�� �5�o��j�ԯ��?�oTsY�5u4mm����;��g�J� I���F�1��&?��%�q$܅�|[�Y����o���,�ϵ�`�8���M���[�� ��[�Ϭ~�X������b��zc46�^����6z�f��o�l� ��%��Ð	r�~������������f�40CKv�Z��3�\�^`�&8A���� N����Ta�+�����gd�cm���]Z�m-�� ;Ү����� ��/���� Zc�o���K}#;\��}m/o�!�˶V��Wg��W�n�}m��vٝ��>*��i�=��+/����%�99x��x%���5�=L����E�o�&����Fe�$�N'�e8�g�o��K)��_����nL�>��#%���S��h��s�k1j�f�� ��k�u�� =E�������]K���q��%�d��M��������S����_6<9pF�x��/��� FR����P��	:iA[�۾�=ޞβ1��a����o���m��k����
]�����М��A�� ��� �����9ޟ��_�	iR)��� ��� � �~;K��	�ď��r|N8�G,��%�Kܟ�M���$�W��Vh�n��!dyss'l��Wkw{��zVa��� �_h�  �9� Y�!}lk���k�Vza��o�q��Y���A��魪����J�=k}�yKַ�����?�V!�݉�Ő���UgZ�C�uo�8�c��z;�W�׬nv�So����j����x��M�6U{r��zw����l��lo�����Yw�?�o��)z��������� ����C��l�����:�9�nE?a`���� ���n�3���?�Z�z�[��o�?e����n��^����:�~��� �@����}�ǻ!��$AЕ'/� 1f͏��NI|D��P�T�b��_����� _V����z� Mk�c�k}G�Y5��7�� 7�J�z�C����ue�u�i$4�R!��^E�=���c�� ��.��;�	�y62�mw9�4��Xӌ��zm�ڿ�.7�ectg�b;�5�u|��YN<X�Ѻ�W���*����G�GX^����[ 02ɎZ߮���75�	�!�vk#PA�+P���}a��?�U��Э�-srYah%�s�ݾ��ͻ��տ���a}K��V�lƷ���ux��?��O��YzM��V.vmT^�-q�����go�jQр�=gOW�ޕ��n@�^��������{������E��;�6���������S�.g�?�;zn&7]���}u[{k'v=�Z�T���]g���[� ��W��;�}D��µ����Z�܊���c����Y�1X�������p�AcAk�L�Yb��=ɉC£�]<bf��w����ɽk��3�SY3�[{ �z��m�� O�v���*��K;��+30-�r��k]�V�{lg�*��� �y?V���zS�Ξ^oa!��Y��;(�� A�� �htK��� 7Z�j2�ܢ=�o�͕��\���j~Ok3�:�2���\QVe͚��e茺K���G;.���g�fܦa�Ͳ��{��#g�\���_X��R�Ρ��M����]mAmls�[\�ϻ����ml��uƊ���}��H�I�� ��J��S��6f7O����uTk����Z�;{��K?;�2�9�P�ģfC�J�X���|?��8Hi?g�������$I���e�v��r�=VY��2 #�k*����;���*��� �o��#��t� ���>i&��5?��{�/w�ޛ� ���>��?��1�E�6�^����f��<����O�TQE=M�;9�p���U�9�t�v>[��W�� ]G;��y=��Z¸�|B�� 	��,X%1�	���_�,���n�պE�F�^�d���kY��ݵ5��V=q�[�֌~���NqmT��]m��0�=�ce���!v�R2j��w��L| ܗ4Պ�M����l��{��W�u<F�<�;�t�Kr-i��%�!������ ���yxH�.>H��J�y̲�/	������������!���a�YM�n��N�al�� �w"3�V�Ռ��u�r̆�������b�m_�=�F�j� ��kbD~��Q3���ۻ�/ڸ�Gҿ�� 2D�O�?���d�{� |��̲���Sy�m�K*��ϵX)ǰ
� �'�X��:�������?Y��eWW�z�˽��m�̦��YT{��^�ok�l�����\?���_�� �%�S� (�W��� �I��>���*� ���8�'��� �[N�o� �i� �Ko�o֯�=K�y�~�;�k�_�[d����P���� �}+� a� �%��O?��EL�X�,�����`�������F_�&#��/LO~b�����<�������� ���>������u��mT��?`�km�X[n�}U�~�w�]�W�:���O�䶾���vo�4�����[k�oǫ�,�'�q�Ƴ�2�m�ù���0t#��ɝ����� ����mm�jQ�p������V3w����u��}_;?߇[�hu�cC�~r_����r+��6��� 4�X>��]�~̩�b��/mL;l���v�o���� 3b�͸a\�1�AȦ���VѴ���X���g�_�g�2?�Z��/�t ���9��S�[Z��sl���tWg����� �'�A���'�i��_�J/�U>�gG���Sg��;+�޽l������r��:�濜W�����qq�U��]�͆�C��y�]��c����[3-�±��V�^k{��k\��m���_�)ٗn=mm=�kX���f�[K�v=u��7�k�u�T۽/�z;� D��=	�N�����YY:]��Ǳ����d2�^�Qo}����힖�K"謹�n�m�u85�_�+�l����75��?O�ch��,��/ҫ�[�e}]cl���n�em�3ԫ��1��L� I�5��]��(�k�
���u>�����,������=K�1��&��.�I�Bq�J&� ��i��ҙ��r,�� c�W���n1�k�ޥ�ֳs=��C�x� W,�ʳ����c��Em��k62����n��{�z����^�"�11-B6��unl���T��7��n� �ݓ�� Ew�DF�]cݑwE�"����,x|����� �������w����|�e�25�iD�|�W�~'�P,%�O��<��,qk+���?����t��+��������h�H�o�2m�}���- o��)ev1�m�}vb\�}��V�@�,c��>�@sl�Հ�[jk���� >ꝋ���=*-� Z��}�X,蠵�����C�۱��}�T���9�� ��K��uu~��I���e�R�>�<'���`Y�(ǫ�m������U���mg�v��k���=�������Y��d����u�=�'&ӏU�w{���� �g���� �Z�]c����[d�in��%� J�U��7ѩ�����^���)��C��3Y�Ӛۯ�'5�k����� ��_	�� Ί�?͉{��G��p����.��e�(��l��ܐ�⁶�5ϱ����J�Y��-��W�� L�?m�OR�����o��[U�?�]�mwV��.e���YE��lջ�*Ỿ��X�A�=;��i����c���ކ۫�)a���UUU�突�l��(Ƨ}l�hK��/����w�K���NO�nE}ꍥ����]��]��N����v���Wg�U������ů��k�v����_��vߡ�C� ��uju]��6�}'mkh���mt�c2�z��oK��U�������uV��K[�nC�l��I���U��cwz�=��ޕ�}�����yӷ3�����Ѿ����Ւ�9���ݡ6�}m������b��s��
n�ͽ�N��V-yp5�;���o��T����k�=? ��q�,,5�4��;�TG�ow�5*��*$�Eu��a-cA�G��}���3ٽ7��5�]
e��2�9BB�#�N����T�ʩ$�ꤗʩ$�ꤗʩ$���H h|W��$��\�X�nk�y�c_�!�c�]�}�s���I����2��E���aqž��Mm��=��� �B�eI?�}/����� 9�d�u"\Fy � o�����Mߠ��).�k{Fip;_��p����{6/�G��_����� �~�x�_*��^�T��U$��T��U$��T��U$�� �� 8BIM!     S       A d o b e   P h o t o s h o p    A d o b e   P h o t o s h o p   C C    8BIM          ���http://ns.adobe.com/xap/1.0/ <?xpacket begin="﻿" id="W5M0MpCehiHzreSzNTczkc9d"?> <x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="Adobe XMP Core 5.5-c014 79.151481, 2013/03/13-12:09:15        "> <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"> <rdf:Description rdf:about="" xmlns:xmp="http://ns.adobe.com/xap/1.0/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:xmpMM="http://ns.adobe.com/xap/1.0/mm/" xmlns:stEvt="http://ns.adobe.com/xap/1.0/sType/ResourceEvent#" xmlns:stRef="http://ns.adobe.com/xap/1.0/sType/ResourceRef#" xmlns:photoshop="http://ns.adobe.com/photoshop/1.0/" xmp:CreatorTool="Adobe Photoshop CC (Macintosh)" xmp:CreateDate="2017-01-17T09:38:07-04:30" xmp:MetadataDate="2017-01-17T09:38:15-04:30" xmp:ModifyDate="2017-01-17T09:38:15-04:30" dc:format="image/jpeg" xmpMM:InstanceID="xmp.iid:7d10156d-0aec-406b-b477-f41c195febd3" xmpMM:DocumentID="xmp.did:e68ab5d0-5da9-4608-b3d0-d0bbaaf1be73" xmpMM:OriginalDocumentID="xmp.did:e68ab5d0-5da9-4608-b3d0-d0bbaaf1be73" photoshop:ColorMode="3" photoshop:ICCProfile="Adobe RGB (1998)"> <xmpMM:History> <rdf:Seq> <rdf:li stEvt:action="created" stEvt:instanceID="xmp.iid:e68ab5d0-5da9-4608-b3d0-d0bbaaf1be73" stEvt:when="2017-01-17T09:38:07-04:30" stEvt:softwareAgent="Adobe Photoshop CC (Macintosh)"/> <rdf:li stEvt:action="saved" stEvt:instanceID="xmp.iid:f5fa69d7-5f64-4e3f-b29a-8ab087b8884e" stEvt:when="2017-01-17T09:38:15-04:30" stEvt:softwareAgent="Adobe Photoshop CC (Macintosh)" stEvt:changed="/"/> <rdf:li stEvt:action="converted" stEvt:parameters="from application/vnd.adobe.photoshop to image/jpeg"/> <rdf:li stEvt:action="derived" stEvt:parameters="converted from application/vnd.adobe.photoshop to image/jpeg"/> <rdf:li stEvt:action="saved" stEvt:instanceID="xmp.iid:7d10156d-0aec-406b-b477-f41c195febd3" stEvt:when="2017-01-17T09:38:15-04:30" stEvt:softwareAgent="Adobe Photoshop CC (Macintosh)" stEvt:changed="/"/> </rdf:Seq> </xmpMM:History> <xmpMM:DerivedFrom stRef:instanceID="xmp.iid:f5fa69d7-5f64-4e3f-b29a-8ab087b8884e" stRef:documentID="xmp.did:e68ab5d0-5da9-4608-b3d0-d0bbaaf1be73" stRef:originalDocumentID="xmp.did:e68ab5d0-5da9-4608-b3d0-d0bbaaf1be73"/> </rdf:Description> </rdf:RDF> </x:xmpmeta>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 <?xpacket end="w"?>��@ICC_PROFILE   0ADBE  mntrRGB XYZ �        acspAPPL    none                  ��     �-ADBE                                               
cprt   �   2desc  0   kwtpt  �   bkpt  �   rTRC  �   gTRC  �   bTRC  �   rXYZ  �   gXYZ     bXYZ     text    Copyright 1999 Adobe Systems Incorporated   desc       Adobe RGB (1998)                                                                                XYZ       �Q    �XYZ                 curv       3  curv       3  curv       3  XYZ       �  O�  �XYZ       4�  �,  �XYZ       &1  /  ���� Adobe d    �� � 		



��  I � ��  ���            	
         	
 s !1AQa"q�2���B#�R��3b�$r��%C4S���cs�5D'���6Tdt���&�	
��EF��V�U(�������eu��������fv��������7GWgw��������8HXhx��������)9IYiy��������*:JZjz�������� m !1AQa"q��2������#BRbr�3$4C��S%�c��s�5�D�T�	
&6E'dtU7��()��󄔤�����eu��������FVfv��������GWgw��������8HXhx��������9IYiy��������*:JZjz����������   ? ��� �u];�f�P�B�`3\J�Ui�e��-��X�����y.d��%�˨��2�D�trԟ�[U�����N0����ZO�Y��C,��8G��k�W�ZO6y��˚n����Z�n��)��F�S��I$X�ڕ����_
&DF�엌�	�Ay��Y�t;R���f���A�\�C
M$���V(�s���Q�pL�<e"Jc�) ���7�fХh�!aoylVg�Y'Y?D��9/�e����6����&�����?�������+��ʹ)@A�>)Lj��_���rӀqHnxXx���3]��U�� D���x��y?�w'ѷ�H,�����v���G ��?��d��u�.�?.ͩZ,o<sZ����{��rG8��H�+"/�|9�?��Ip�I����o�����X������$6�Ih����]�yI�"~��[��9p����D�y��Y<�/���������5U�dX�q�X��iO����pK�V���v��[y��^+^�R�)#е/BX¹f��!�w���:���}�c�$�>?��A�h�斵�:�:U��4����"K���kg,�5-ƼdF�>L� z7c`'~_O����E5�1��)��E
���n;7�ļNeL��D~���dn|�x\]j��������h<���6is��r�m#I
�6W2��U,�6�}���:r�!����?������7��0��D������\�fx��-���ݙ���Nj� c�X�&��� I���#qʑ��n���V:7�]6�4^�����<� ������Xx��B8n]޲9*U�_���֎�W�-����-��7jZ8�h&�����%]�bW�$���(�Ʋl��4���ɮ<�v�)�B)*щe������;��]�վn_�a��d^l�5'A���a[�,��4	-n��8�����G�_���% V�ȁa&�<ݫZ��c�$�����<}HG�4*%�Qe�7�?���ז�<_�`r_�uϜ5�o6>�-��:k�m,o�3F�9�m��'(�2�/�_�ba�{Ҝ�J�*i�o��_3}v[{[}Y��^���I*������V���Q, p��~;����Pv^x����n��w�CᎢ;kYڋ�VA�I��F�Ï�d�q���?��d< ��j>s�`�B�!n"��n`i�~��&hdNsB��X���O�����&F8A����tI�v�Ml|�%�.����Q��o-��$����m�7U�k+�?H#�����@�oγ�:~�s{h�O��L���,�h�z����/QӔmO�Ս�|9<�8H �_�2X7��������E����r��P
�4��<�?���l� dhnQ) ,����r3�ѳ�-5+�x��t� �I#o�%����;�c���,�g�/����F�f� {YP�*h	��͘�����7c��B���W�^Q���u�&K��[�Dd_M��n^Q�K�yŎL񁢑� ��~[������[���ɇ��ɼ����8�s�+�� Q�����c��υ+����3i厸��c��K��g�-��w$�p����R*1B� ,(,��N*ُ�!t�s�ث������_Fy\X2���f=�1�_�r�Nb{����Y���+2,k��Ԝ��/��Z��P�(���sr�9���B�Օ]�
��v�njtr�qˌqzxӋgȔ?�ٿ�K���� �,�̇�&���k\݋?�qZ��S~�:�gE=~�:O�p��|O��Z� ��q�#��ā���9��a�����'#�1� N���o�m�{�|�~���'�xE�������>y?R�?��������޷��'�_G���ӳ���9�� �,�̇�'/�ߧf� }/�q� FY���K�A��ӳ���8� �,�̇�%���w�ٿ�K��іo�C���Pw�������?��7�!��(;��vo�����e���� d����;7��~��2����_��U��$�\HP
� W}������ɨÛ!�bpC�?���_�r` 9�ё� �Oj��X�4~dY%��(>�J�����T��l��\	�W_�����i��cQ�^��ЛXm���)�98"ʝy�r�������]���3���LE"|��]�z��}�� �����R/MH������ydr���SB$����_�X�./���Ϳfv��"��>��g_��G�~��w��jZ5���p$�h�܅��jH�3[�q�@$�>8�C�4_,y{C��C���X���^5��
��N�y53ye?�ۓ��<�o;��̓$l�C�]z� J�+����Γ�G���u����������|�?�H�zU���6X$'�� �M�c����h����6{���f��xw��5>��z�^
�Ӥ���h��2p�]^���i$R�k�.�aɭ�Y�t%zg�=��E	G/�� �������ezk�\��Z�S�n%X��u�~��,���X�j��q���a�G�`4뻕�F���E�#�h��l>��c0rxw������[6��b��q"�"J#c�7Q�х~�w��xH������]�:����R��T?��:#�wS��<�^�j�����>���;���+�� ��������O��_�O�Y��!����8YC��!@�v;y�b@��/�WO� ���%���#������,�� ��o�K�z7�^4� �I������ C���6����}oF� �Ɵ� I1� \�^���������)�[ѿ��� �L������,� �k���w��o��i� �������� K?��{������$��q� Az�����������}oF� �Ɵ� I1� \�^���������)�[ѿ��� �L������,� �k���L������ho�gE��������G�<��g���>���Ũ�?������ՓS	G����?�����m6	-e[}f�7�dz�r#дR��U_��ff�U���џ�|�qk�O"�H.tmN?�"����e�K� d��X��u�J����k���W-�k���$fK{���S�A�ȣ��>^_
q����8����}GǛ� ��� �����q�E�fvg�g�ߢ-Ϭ{��^韞�R�_*���Z_���n"Fx��o�|�`<c��\Q���;=����*�-@y��ndf��G��O���Y��K�9�D��<��M��� 2?0,/�[�;�.c�VSx��f��c�s��ˏ�9�� �?�-C�:���h�.M��u=})�"�?������s4���?�q�a0>O\����]z�����
�����Ԋ:�� Q�������n�����˗��ű��9� �'���E� �,��4���� �c� �6�� 11ɳ��~�����R?�ɿ����'��˻+闽�]��4�P׼�,4�����*�g�B��%�ӏ�y�u��q� �N�<13T� ��5�1�v�or����M���Ϲ VDf'�1�=�����N�DH��K� �%|�FӼ�u� B�#�xX� �E'�L�����]�����^��S� �m��a��"s��0���o:�L���^k����Hb�F�"�,c�U����� ,���d�R��I��&������i5��W$*<������ ��"d��?���@�W�5/�l���kk�[C�"=�!�Ih�I����<y7�O��b6	'���x�⹢c�~�&�ey}�ZOmij-Z�1謬6�@���x�/�_�#����> �HB�m���:��{mv��ĳ���p�!Hf%��l�$L�$��z ����R�gK�J�.t�e�y-\����Hٗ�G��N� ���h�&������c� �3�Ů�[�����L\�7�?w�S���N��M/G�.���0�MdM�����Â�� �K2�� mx���e!�-r��=Q�d�4-sH��[�9�J�v��Ӡ��\� v���#�$�+�6S������I���J�{2d��V�Yf���xP���E�7����ʝn�>�ra� 95� )����� ����fv��"�Y��sӿ"5-:�=29���A%�Q�Ua[�=	�|I�v�rt�p�[�Z\������6V�zV��fsr��� �5��� �?�1�i����.���=�^д�wJ�ҵH�w+�D=A��e��J٭ǐ�����"B���!�^C�
�]ͫ?��jIU,�n>�����_�:->x�������ӿ�䦑��@�[p~	M�5��h�����=���k�6�֟�Io�����V�O�B�J�W�����`L�'��^�Ǥ�D?� � 5�謵�N^�u������fuf� D'�bqˬɈ���L�;���q�yx������ 0���L��}>��x�Ym�Pą�=8�+Ǜ��!���$�gdv<51�$�<1�b+� 9�.C��hV�Pi��f'�����g������X�%������g���5�,��.�PG.'6��@����	��mp���ߘ�l2�2�@Icb�!�@C)�n�0Ok��?��q�WLE�k������w*,nJ6��I����kw��l����VV�� RO�� �?�`� ,f�?����OO�~P� �l~e�Cq� �Y�}�1�W���IО����� ����#���/� �L�3w���_�'��?(Ļ�VV�� RO�� �?�?����i/�����?�]� ++H� �'�� ������4��	�����.� ���ԓ�� �CO���n���K������������I�� �!����_7y� M%� Bz~���K��ei�$�����c����� ��� �=?y�C�%��_���P򿛮����`�~��ְ,q\�Jv�:���+�]�]� 2'|N���{���ypK��߿���� �ߔz7���������?F)b��Ño�6�V�Jəzm\�l����cg�/�w�O�|���iT
�|+ ���y�4˿=lB<_�&��FF�� �|���(i��G���C\\HyM+�v���*�Q�13g�Croǌ@Pc��zg���5[�FkI �[QH��RG��[��2�>��{��Ӊ��/� B��� ����EǗ� *K�5~Lw�o�o��"����췟�}~����=JS������Q�V+��T�孏��ͬ��^Kq6��<���T�%2�$nhM0fԙ�F��ǄFD���nJ<��]#�,�F�8%I� �2F{:� ͭ�嘲���	�HQH<��_e�N���K����*���>���n�RsU��i�e'������[�{�Wb�E��I��E >9���&0k��{G�4ک|X�� F�h�G��x�<Ӧy��%���!�����Z9&خ�)b������� SV-^�e�����a� �<��E��3����WzlM(EHY�QB�����f�2�rNVL]�����|CyC�-%� �z���i��2����B}��� D�?�����[�����b�Z��SJ�[E(���ʱND� @~�<s7rF z~������\�L� {/���-����Kͺֹy���e��U�Ige@�A0����Y��G9H�N��K��1c����*��[�.?�cM�],��O�n�
�30����o�t1�� �_��� �y'�ל�N� ��� ��������l�����-��/^q� ��;�FO� Tq����� �l�����-��/^q� ��;�FO� Tq����� �l�����-��/^q� ��;�FO� Tq����� �l�����-��/^q� ��;�FO� Tq����� �l�����-��/^q� ��;�FO� Tq����� �l�����-��/^q� ��;�FO� Tq����� �l�����-��/^q� ��;�FO� Tq����� �l�����-�y'�^�|��}6���I��_�ڴM!EoJd���Re_�20���U��|Y��D�������}_����>y�ֵ���ɧ1��IY8�|ßO��	j�+�E$|�U�c̜cm�$	������B�|���^(Q)�ӻ�eQBz�,V���į� u��u�ʿ��)n�>I���/�\Z\<��Ǭk{�YDM�O�A���� u��Gǎ�O�6eᝑ�S�BZ��X\�Wv�rR��c[\ݙE�60���R/�o���l��ߗ�w�I��!�^iK{�[�#�]�K�i
44�I�n-ɓ���|��
����z��Jm�O7���l�m4䃐��;����:��\�#+9��./������X�Q�K�Lt�.y��V���H�-�-��2��і�Bޗ�(�8��[�!,� WJ� cl�%h+? y�8mm����&���319��K�Fa�E-�OD�y&O���KQ��� �}?�1ǽ�F�LZ$�K��W���q4���%Y�?MS╝I�<�f��&W�UJ��J�lSصסf��ɥ`���ȑ,
��%��ܯ���ผ�[��J�r�V��>j�KkK���P[;�'�=V�t�,p+Tr&i�������lr���jF9R'I�l���E(�]6�:�[Hc	B*��S3z,��2�y剈鿤���ij~_���6R\�ad[q��3�͂�-�P&�rF�]���s�φO�����l|)r�p���|�U:�Τ�x���#v���ƞ�������/�B� ���������;�[��_��%�e2�$�+��QIȉ��UkO^)�o�� w��ˌ�����(�z�=JQy�PؼP^E��E�EYc��X]X��щ�F��#s��o�	ώ�~-�{��zk�JkKx�m/-��O����̉�t ѲH߻����>��c� ��o�8͔D~M�\z5�����u�Z]�3Mn���2�W���W�������sC�O�*"Դ�+y��S��%�$�������)��C\�tc5 /�:\"���/�G��,#��� u	]�:����c��A=�s~I-���k��6I���p�^��xw~>�/���ބ����_�z�m�+cs"��g��*�B2��'
3z�쒴���u0�x�1I���V�yn��-֕V��Bo�J���/������l?�������� dĮ� -��f���
A �����M?��rx��p�ח�����̑��_ǩ��������<���M��#<�K/3i���*����~�}?�+9��c���f1����:�\Hm��̗r�����!E�29q���Ϙ������J����� t�X�Yn��y���WK�#���4��G,�qk~G���t^2~�6�1�N$�������N*�Uث�˟�R0_�(a� <]�q̇SUCR�$���(?m�̡�sA���?��{��<��MsCO�K��d�0>7B��9=����c�c�I���P��^�x�5Q�E�+�ܷ	�Id4$=�E���?����q��� � �]�Ή8{�@2��ȇ�7�]�,�W�D�ֶh���|y�ڌ�C��p� �$F]�I�� 9��5 ���if��~����P8�Kҁ㏂2~��k�!\�~���T�@�Ε�@5_��Y�<ww1H�z�!c���*��I�s_�� �� 	��)1��[��tk�$z��ڇ�&�yo[_��O�� su��>����
��[�:�	_?���^_󭮣i>�����؋{�E��Z겓7ƼH!��� �zr�2c ����c	�RO+��+�u���ҷ� I�yG�*��ʄ�}U�Yc��<���|\w���(��sV� y�m��L�:K���2�c�4b���IF���?���Cā7I��sj� C��Ƣ�j1Eh�p�=��*�*�@�����׏��~��[Ҙ������s^\Ki��yˬf�q�/Z	@���w	����o������ S_4U֍�y5�����Ip�Gj.f��i��)��s�߃���~�DN V���Ĥ�W�o/��RE�,3C�i$�9�_X�q��J'�q��'�|��c�G��/��D����r��<�,�����Z���#D�?�LS�9��w���◂}���7/��#,�#�-Y���c���+[O۟	�O���91�U����D%|�+��E�G�����il����h�E-�U@nnM�hu���2$vۧ�/�� z���_�|���1�I*Ȭ��(�Yc���OR���8��qnr91�1��z��^��xxV'7�p��b��ym���Y)�9��ƌ�d�܎	�����人\I}X}ag6�IO��� �N	rG#?�I�Hk"g��p��Vc��v*� ���N*�Uث�Wb��]��v*�U�k^T�Q���5�Y�h= ���S�!����<>>wC/�k�,�F^h�MIʠ�:ƲE�G� UoO�/8��~���F3����+�^M4���C�
������d5�1�#䣔�0'���>��Y�	��"�
���C��� }�/������z���z���2y	 �٢�H��Eӊ/'� b�ù>�M,4��o�{��	�7 �)�	����+��L�h�N�]��v*�Uث�Wb��_���N*�Uث�Wb��]��v*�Uث�Wb��]��v*�Uث�Wb��]��v*�U��
endstream
endobj
9 0 obj
<</BitsPerComponent 1/ColorSpace/DeviceGray/DecodeParms<</Columns 103/K -1/Rows 12>>/Filter/CCITTFaxDecode/Height 12/Length 239/Subtype/Image/Type/XObject/Width 103>>stream
&���ш���r#�>]���/�dtGDvldta���AeZH0@�v	:
�E?����#�(@��`�+B�Q��X�C��� Q(p�����C�j6�� T�"�Z({��������C��S�����	DC��YP��`�
���!�#С ҂#�Ђ#���q�T=& �[Ydu���Y�0�EC�� I�O���E;�"?QT�A?T�����A[}���2:���  
endstream
endobj
10 0 obj
<</BitsPerComponent 8/ColorSpace/DeviceRGB/Filter/FlateDecode/Height 110/Length 1004/Subtype/Image/Type/XObject/Width 110>>stream
x����\9��:{�R�ݓC��2EV��QUUUUUUUU�]�����S����9O�w�^�dRB���y2���q0��_�.���Oo�t��$��w�.�a�ƓӇ9O�LG��4�^����8O���ӎF�W|������UG��+i����L�\4���n�p�t%�M�M�iG/���M��(�L����w�J��L�t^���}ǒ�o��k�w9Ojjλ���d�*ɤ�д6��m���;���K��x��[���w��!���dN���;2�}��^������o��<K��$=U&�	S�~��;�d�6�!�;���|�]6��SIrf��0��}�f�x�fǿݩ$_�Lɓ8�om�M��-��J|ݴ0�y����K�Ѵ�O�j?e6iM�z���ݓ���&��xC/�7J��+MLkN����{ϒ�����K�}�<����P�F%yO�i����ϧ����H��9a�l�̾�fZ���,I���Hz�v������^�v)O��|Ssq�����M�<9��<��;���T��'4iy2�N�3�.���SI:N�����?oV�_�y��n�{�L>�E�>u����]&P��+�HrZNh�����n��;b�EIވ�ށ;�<�Ur`Ϸ*�{����I�������>!�5⻦��5�e�$<�	9�����q�i�i�p�W*�WJ$���/�&7e�3��a72y�w���ۙ��0�nܗ��|G~e�;F%���q>i0�4���u�y�M�W*ɝ؟�����lN�zJ��LU��$��Oy�^>U���I�Jҳ��_�fs��.�&�+��N�)=�s��W�[��;��=I}��`ݼ���bIN���Ok���N~��'g��l_��L2d��웾L�����D%�J��p�K��3�I�x��{�$w�J9o�������W���K;�δ6�-s���-/n�vL#�0�2}�F%��H��'�3s��T7*�O�4;�os�g�h�=M/�)�WWv�8�it��?����iQ�UUUUUUUUU�A�M�:
endstream
endobj
xref
0 11
0000000000 65535 f
0000000017 00000 n
0000000140 00000 n
0000000196 00000 n
0000000283 00000 n
0000000501 00000 n
0000001570 00000 n
0000001661 00000 n
0000001757 00000 n
0000028962 00000 n
0000029405 00000 n
trailer
<<
/Root 1 0 R
/Info 3 0 R
/Size 11/ID[<F80C19B9893A383D834F8822DC29B017><F80C19B9893A383D834F8822DC29B017>]>>
startxref
30571
%%EOF
```

## uploaded_files/7779QL_document.pdf

```pdf
%PDF-1.7
3 0 obj
<</Type /Page
/Parent 1 0 R
/MediaBox [0 0 612.00 792.00]
/Resources 2 0 R
/Contents 4 0 R>>
endobj
4 0 obj
<</Filter /FlateDecode /Length 1056>>
stream
x���m��8���)�U�J��666�W>��'�@"5m_��J�����>��l�m*�:���c2��{�	q��g ���;|����K<n�?s�xA�R����(w��^�?E~�h���g�<�5=)������j�ÿ�FI�d�A��\����X-�{����e�aQ�
�p�,7e�'P���ˎ7L�x��K�����zY@��i�{����(�e� ��V5^�n������	�`�(��O7�M����;��n��nmw�@�b��#��{�������E�T:��5!-)��{�S�k�&�U�x��W�
xR��n��'����b}N��$��h:��N:�ϐE�,�$��w�����3�1c��:r��yǌ}�r�H���
Z�h!�Fj���Ʌ -o]�?�b��	\�[
��ݮc���qU`�!�u.����&VJ��m����e�A��h�{�(�0�����38tj��!b-X?��	��B���ϓ^��z�&v>�+���`�zvh2�h�ir>J�7U��deX�ª�0ʒ�YY��$=��;��W���Ǿl�X�#��K)�p�F�4��Q�u_�H���톨���X�V�d+z�����}�Nt�g0O�g��t�l��]`�#WY
U��%��{F������fFЋ��'˂��5|��]�%��~��a9�Q!��	 �P�Cd�׳8J�̥�Q�\M����+�0W0+TMkT3�b�Jq��WOŶ�޲�a7�I=e�J׳���5�� F�u�z��1֤:�8���_���vb��wyn�u�*�DfW(�ϤR��U��c��I�]T�
p;�"� 5��̳��~��L ��T�[�4���3I�I4�p1��P���{�H����&H�	��7��z��:�H2LM�類c{�Z�jxB�"�O�=T�f2�R��A�U�.�ig�2��2�Nǹ;)�<;(��w����\8uC�|O/w�G�5�pʺq}�y�X�1oynൽdpw��� ����s�cj�>~�+����E0F���,n[
endstream
endobj
1 0 obj
<</Type /Pages
/Kids [
3 0 R
]
/Count 1
>>
endobj
5 0 obj
<</Type /OCG /Name (�� p r i n t)
/Usage <</Print <</PrintState /ON>> /View <</ViewState /OFF>>>>>>
endobj
6 0 obj
<</Type /OCG /Name (�� v i e w)
/Usage <</Print <</PrintState /OFF>> /View <</ViewState /ON>>>>>>
endobj
7 0 obj
<</Type /Font
/Subtype /Type1
/BaseFont /Helvetica
/Name /F1
/Encoding /WinAnsiEncoding
>>
endobj
2 0 obj
<<
/ProcSet [/PDF /Text /ImageB /ImageC /ImageI]
/Font <<
/F1 7 0 R
>>
/XObject <<
>>
/Properties <</OC1 5 0 R /OC2 6 0 R>>
/ExtGState <<
>>
>>
endobj
8 0 obj
<<
/Title (�� L i s t a   d e   S a l d o s   d e   C l i e n t e s   A n t i g u o s)
/Author (�� W e b E R P   4 . 0 0 R C 1)
/Subject (�� S a l d o s   d e   C l i e n t e s   A n t i g u o s)
/Creator (�� T C P D F)
/Producer (�� T C P D F   4 . 9 . 0 1 4   \( h t t p : / / w w w . t c p d f . o r g \)   \( T C P D F \))
/CreationDate (D:20241120134618-06'00')
/ModDate (D:20241120134618-06'00')
>>
endobj
9 0 obj
<<
/Type /Catalog
/Pages 1 0 R
/OpenAction [3 0 R /FitH null]
/PageLayout /SinglePage
/PageMode /UseNone
/Names <<
>>
/ViewerPreferences<<
/Direction /L2R
>>
/OCProperties <</OCGs [5 0 R 6 0 R] /D <</ON [5 0 R] /OFF [6 0 R] /AS [<</Event /Print /OCGs [5 0 R 6 0 R] /Category [/Print]>> <</Event /View /OCGs [5 0 R 6 0 R] /Category [/View]>>]>>>>
>>
endobj
xref
0 10
0000000000 65535 f 
0000001244 00000 n 
0000001636 00000 n 
0000000009 00000 n 
0000000117 00000 n 
0000001302 00000 n 
0000001417 00000 n 
0000001530 00000 n 
0000001795 00000 n 
0000002215 00000 n 
trailer
<<
/Size 10
/Root 9 0 R
/Info 8 0 R
>>
startxref
2579
%%EOF
```

## uploaded_files/8044UE_document.pdf

```pdf
%PDF-1.7
3 0 obj
<</Type /Page
/Parent 1 0 R
/MediaBox [0 0 841.89 595.28]
/Resources 2 0 R
/Contents 4 0 R>>
endobj
4 0 obj
<</Filter /FlateDecode /Length 2102>>
stream
x��[]o�6}������Q�-)����It�L��6}��jV�-Md{f���,/)Jt����}p�K�:���{IJ
Id
��������j�V�si>������@iB,~��bD��'�y�2�3E�]ؿ�s�Zn���E���O����~6����닄g�X�/�͚UQ���I���h�y������Ǧhj�*�o��5zȫ|H�>H�0�|�}��cY�3�#���4� ����|zs5^āS���pu3�a|�g��<���D�	�����ۏz�=�D�Ȋ{�+��\ծ���{����K�G�����q`h�(q@H2]?|��~x{�0���1ʢ �G~���A�,��F��3�d���|ڗ��?z�,��4{�Ȝ�i�I�]��Q7��"���s�����|�&���-���a�iځ؝��z{��`�a}-�B�z����7���#�+��7��8hRR��e�selTZn�d��%��[T�#X"sn{�,wkc�f��K���^C$�c��m�����TZ[JeGp�&�J��m����2ޠMR�=��8��_�{�M��R{%e�"xm!3��#�E��F��z�6z����/̮	�cF��!���U����QY�z�ۘ��F[0�*S6�B9ж�o�%�G��m�������Ҷ���<.Tׄ�6S��&"�C�I;����Ғ����< �@����}g-�&�BA 4��s�ф���< [�R�6u��N
B���P,��--NNh;b�܄PI�h Hl��v�E��^�hS�=�%���v�6��l��ȖX~@d;��=��I������:�6�9��s�:B��q��m �FB]�0D\IGhB��Lm��6�hA4n6��Ж&�-�-�����Qϭ���JmG�W�b�������䆶#�	#���N���	�������G���,XB]��.m|�"�#.��l�uK��d�g�Ov�%�+ڗ��9_P����������-"_�|}������NO�/�=���z�}q�R���/�^N~�r�KD/H��x��E�K�/C���B���/d>m:;Jk~Hdk�D��ۃ/�����+^ؐ�&=�������`�����%0�Lt��6��B>�J�W]i��V�vהzl��y�[����q������蹿+�d[.�7���Q��`0��Q�
sF�U���bU��O/�A2rJ�I���0ӣ�I�2�U���~b�^�MiR��hR��^�uUl��ݭ~���4��T���4�7x�n�z;�aס�}"M��o��~>�zUoam>����	�Ӿ�e]mw�d������B*ݺ�9�Zۮ[�M}�������h��es�z�:��>�-�,�%;�%kU>��uh���p�vٔ�Ji�Ѹٽ)]�r���´u�+Wz54R~�t_E���(�����(KG�)LI�y�΢����T�9�y�ڜ<���y�<�=lx)OM��7�D�pGo����]�ѻrY�5n��H�@f���Ώ0����,���[�W&�9���j������˜W�!
7q��M{��h��� ��ίn�p~}5������~��ͧp>�Gz8QB")= ��� "��Ø%b��N�!�-�q�Nh�	9^^��y��7���]ST5\�P&#�;@���`Ēw ]ޡ"�F�w�BU�O��f�v�yI�!�d|1�B>{>��dz���|2�-�w@����LY�J�D���<�J�@I6�k'��C�����Y��_J�<a��T/� h�7��0_���hP���7}�'���_����Hr��Y$���@DT;>;K�H��)q�����I�$?�����= ���]�^�p�����~��n`���&����F+�2���p��{�E��oOx�(��$�5���D��T��{ �(����^���
���O$�U� ;�%r�4BDy��"�v�PDn.s#^Ǎ{�n��<m���	_|�<�;�2�7�T�M�'&l�kȣ���`���#f>��\���@����}���/���,!�뵁��[H�Z��^�<��S'wb.���)����Çчo�ǀ`���~�V
endstream
endobj
1 0 obj
<</Type /Pages
/Kids [
3 0 R
]
/Count 1
>>
endobj
5 0 obj
<</Type /OCG /Name (�� p r i n t)
/Usage <</Print <</PrintState /ON>> /View <</ViewState /OFF>>>>>>
endobj
6 0 obj
<</Type /OCG /Name (�� v i e w)
/Usage <</Print <</PrintState /OFF>> /View <</ViewState /ON>>>>>>
endobj
7 0 obj
<</Type /Font
/Subtype /Type1
/BaseFont /Helvetica
/Name /F1
/Encoding /WinAnsiEncoding
>>
endobj
8 0 obj
<</Type /XObject
/Subtype /Image
/Width 216
/Height 217
/ColorSpace /DeviceRGB
/BitsPerComponent 8
/Filter /DCTDecode
/Length 9924>>
stream
���� JFIF  ` `  �� C 		
 $.' ",#(7),01444'9=82<.342�� C			2!!22222222222222222222222222222222222222222222222222��  � �" ��           	
�� �   } !1AQa"q2���#B��R��$3br�	
%&'()*456789:CDEFGHIJSTUVWXYZcdefghijstuvwxyz���������������������������������������������������������������������������        	
�� �  w !1AQaq"2�B����	#3R�br�
$4�%�&'()*56789:CDEFGHIJSTUVWXYZcdefghijstuvwxyz��������������������������������������������������������������������������   ? ��)��4 �)��4 �)��4 �)��+\����R�����:�!�u�OM��@}=p�Kr�	M�*�oY:���]�_j0G  4`�q���\�1����:��u�id�k�&���n�pA?x���I�+x�XJ�[��R�nǮ_�U��e���J�;��t+�$pO�K�z[��scy�ı�u�$���^F�*��^"g��՝�T��0kIpt��iW��^A��l$��l���&�� ��5����c��-a�M��Dټ����ONk�Z�aw�\��;� �dg8>���ⅉ�o�%�%�7�k�"� ���� �� �?�El��]!��Nx����w �8>�?�O>��k�� ��FInJ�7֍�K�@G�`u8�c��|>�Hd����z��䘇�<c�ꧯ���qZƧ7��p���'j�����e��}>M� o�.��6}�E�=s���o_»7ƾզ�l�h��%�L�� ���~���_7�mR���K�W�_8�6���m�)^�<�Ϙ�W��ܨ�)��L���]7Q���d�����-^��O^ �i���0�!�zSG<)42,�H����XAu�՜��f���Fi��4 ��L� �њfh� ?4f��3@�dx���w�l���ؗm���=�	������ X�h��+��Lǹcr"q�0�=p98�k�o/��+�o/'i�%m�#u'�aҳ��N�wQ��t�#�֭�EkyYm�Kd[E���77V<�A�s�P�j�W4���J�`�H�(�Q-J;VL�"ԫQ-J��*ԫQ-J��:�H�f��{+��m�1Mʺ��-?�E�wGO$g���ۛ�3>!^�6Jȭ�y����I�s�X�KY𞵡<�m���N~�����'���d
Ю�Þ+kt�P��6Q����1�`�\pW��=t�)i=��/.��CU��������}���`�V-WJ�f����17'a�$pq�`�����֏FqA����~2��9,i�5��^�F��;�y'#�3�����^��[$��E��ne�f���u�a�s����Ջ+˝:�+�I���r:�A����*�U��[��tg�9�5��#�	�¶��h��p?�z7��G��t���<��P�,���3Fi�?4S3E 74f��3@�r~;�|~Қ+i��Vu��mݰg��8�S؀q�^!��z��̧�v鴐ҐJ���O#�{�|���ԯe���渕�<�ԟ�L ���y���rK$Ӽ��I+�gw9,ǩ'��^ա��oX�K6�I�3�L�@F8�H�qל�Q��t؄�"�c�E��6�yy\�OE9�#�<氳z�ь�|�W�b�Տ�u�A��U�,��$h�!�;���v�~��Q��z:��%�P�6`�K7n�`�޲���<�W���\�� VNP]nv��b������D�'� �g�G�� ��?��Io#i�Uc�Tc��d�aT��YI�G%���=I��@�{,wp3���nX�ld����#4��7d�uiT�iԊ��9��}N���M��%��$�9�$���iR8��G!Ud�= �nҴ�����o�%d
M�Ŕ�W�O�H�뚾!�v��_���W]��$�pp��Ԍ������<���:r��+o�W,I��+7C$E�f��<���F�� ����^���(��*�b���m��7g���[v�,��8 ?��?�-?��_�x��_���g�ֵk �M2�]��_0c� �ҳ�7�F�Edu%YX`�;W�E�9�m�_M�6<S�Դ���;�*E$0I����#���/ft��
��⟡���7P�^��E��� ���xx��l�����1��r���-+|�>�l�>lC8���p2z����<4��_���^�̇A�a�w�Ԁ�H��n"a�F�q���P񯅓B�K�ϥ� �I�ʌrvn�#�z�\Uy��D#Z�.�7s&|�2Y3�U���8��q�Uҝ�#9��of��On��8�m�76��]Mm:�1ȹȨqTقWWA���;$���ԐT����~
�k�-��*jh��p;���G�8�;���im.a���M�����Z�Tqf�*�3��њ��c����n�帉	������Nm���>~Qqvc�E34S��e�8bye�c�����'���p��C���.����� Y��X�^�#q�n���P���<� ƾ%o�*�;|�l8+�������5oH�D���y�v���g��ª���?0��:
h�x;LmwZ��'\Z[0��s�'#<|�����5-F�U�{���#p ��;(���k��E^緃�J���+���{P��{q�i�lt��������%�S����{��X�ڊ+�Srwg���S�X!*{KIﮣ�����C�U�� sKii=��v�Ѵ�Hp�;� �I�����3��c�����1,�pv �zg��� ֍'Q���>X�k'�[C����l/�}�2�3�)SK����3��~ �Kω�s]��E�ܞ3q(*���xc�s�w�x��w�$i��M��}� �����q�|Y�%����
*�����V�=Gvz�S��m��g���wAۀ8;V�WR<��6R�%�)�=��aظ1)��x(�2*I�]������\��1�o�:t�2MI��=�_2?��A�� <��UN�=���2 0cs�G������*��r*Ֆ����O�P��@�@=q�r9�:�U��+�__��eΙr���'n
��O��+[����Mt��;�|�5�1T�y d���ddMG6�y�x��a�H3t���q�FEv:.��hKm�۬`(!|��,��'�g�
 �ּe�/�b��d���?��G��ן��ڗ����߈?�ȃ^͚��tMj�����Vwm����=N1\�h){�ў�4�/����� ������5�d�Z"��
�:��H��^�/�����K�O��-B���u� ��{������G��I4b[7���l�L�3������r\�~��*U=��^�� /���1O�����i�sZ�@�"�Nc?��v�Z2F@�����r�T�$�'W��eu9Bq_=b�3�Ư�Xͤ�I{|�����َrO;������<��������E34WQ≚��I,|]��O]�vɤ�q��"G� 'g�C6Ӄ�Q��?j����W�3��$�ۛ��� �����q׶gþ��@ظ�7W�g%� H��8�+*��W;p4j������u)�]F[���f!�v.N}?��5K���99;��ҍ8�Eh��.(�nxWJ����M����L���z��z���y(�15cB��.�O�]�L�V��'�3&�x�s��I�8�<Ư�o
k�Du+]bh"[_�#����-�98 �95?��zf	�Y�!�Ivp99���m�My�Z<�x�
��d|z�QԞ���v�f:W�4�f�y��|�m!�����x�V_⶷"2=�����V��#�~z�N�&3��l~������3,�*������U���+SO����;n����چ�be�tc�H��w���oݜ�q�Qɪ����,w7J�z��%���9��#�q��1�+�� Q]&2���F>���4�h�|�@H� ���5w4f�8��uk���ڵ���lS���9\�21����w�Ira1���R��e�s��������(��X�P�����34֑Q݂���N .k�ּy�h��%�k���^+P�$� ��N)�����[	�(���͎�G {��u���KEo5��=������tH� �*�&�M��H���u��@#�d�7s'��0@k�)��ǖ1c�:�� W��5��x����1xI]%[KD�n}�Q~e�$�Ԍa��t����i��O��x��#c�Fyき�1X�߾����5G�u_���4�&*���[\I��Hأ� ��p7m�J��f*��|t�f��,)}�P���H$~5S�hRiܚ�������I�(�w�ڃ_xr �-Ɂ� gی�T}A��H���Rq}���y�]ܶ4��r�yT �,�����Q��R�'���+go�G@=�0+{Ɨ�6��k+�@Y 9����5�W����.U��̓���yo-�?��&)qF+���&+Ѽ1h�W���>���FBc�Fs�϶�1��m-^��X���E�Kt�
�}q��(�J�\}0��ur>o�+��]u8)-�Q�g��[|��6⠞}� ��� ���*(⮬^��|������+��4���Y��}�Tw?���,-�\�9�|ߏj�� ?4f��3@��f���Fi��4 ��k���K���A����Fhl��G#�W�.e��+��M����ݙwa�S�.O<q�+�-�0���Vf�ڮa��
r1я^* �X4�B���>Y�u�6�v� ��ܤ�-f���|Wq��`��pH�ֹc�E�b�L:y�p"7;G�<� 2h��kTy�-��ķȅ�i<ßV��Mdm�� ������ �-bb���>����e��T���ΞC��}w�[�&y�YQ�c�=x'+�ǵ����Ɗ���l����֊���3�3Z|��稾(� ����� �-dqZ�(?�Q]� �?���כ[���������!x��Lњ��5�2��!���X�Fy
H�@5��jKb{n���x5`}i�b�D��9le��~R��tz�7�� \���O�L���\ؿD�#^�i#�j�*�WQ▭dG����D�)٠��3Fh��4�њ ~h�34f��3L���t���di�h�p��6{��\/�w#c��ⴤD�BȊ�022A���*�y�F$� ���J��b9$Nr��� �R�]��n.���@'����ܑēk�ˀ�$~9��5��j��j���<-���c�k��y5��ϻ�>�f�j6�S�F+�ܦ热��}dݷɍ����q� �~�T��X�������W�������ݼ�G��*+����+5��8Ve$
G��Nz�W>�w�s��*����,��xX[��3L���vs~�x����?�j�ub�XHa��+���i7�-A�C�{�H?���CBa�ݰ$��<c���^��>K<� yO�~�17J���˂p�y�K-u1��O�?5�kp�	�}j�h��4�њ ~h�34f��3L����3Fh���>�1���c8�O,~�'߁�Q��]ÂFs��Kx�{*rv�G�U�&XD��W��� �-6GZ}��3�F ����ަ>�i�N$�y <���� �|Yr��m���i�����,k��7b�Y��d2F����Qx^0?�
�^5Wy�~�����Ћ��Z)(�λ���#�YX��*��������;O;Q{�����l�N���Ez�K�=O��\^1۲���I�{~l����4.H�(�z�����n�C�5��49�	x|�`s��.�:��W�f���ӹ����r�$�F�4n�{�9��녃_�w��=Xλ��i�ff�S�yrw���=���וd�^�k�yz�&C"A������Yp�}�;d���fVMoI�jk��� �/�^>Y#b���GV�W�@ɬ?��X�1j����`��ws� {�@��}y�`�ʀ9���=_(�5�g{�[���ï��(� ��v����r�^�qf��r���W�_���'[�����Soۀ�������8��Z���3Fh��4�њ ~i��"���
3M�X�:�S� ��U���y>����o�)n�R�j�BrJ�?A�O���}p�K/�I��OC��� �Uϋ���6*��ǯ����8�w��*��X��z��$'�dp�$[ANs)Fq��'�;W?��b�_.�g�>�щ�Th���0[�	 t57���8%,#�L��1܁���;�Z|�l��a�"�aӯ��QIEy߭�RU�.�;�������LӱF��s�3ӶqҪrvFU�ƍ7R]�E����≕�V��!�bLp?
(�o�S����h�bZ(�p�3�O�8�� s������H���IT���e�"2:�V*FA��z��i����wym��|�FA�'g�����\��l�:�d�T��$��ԑ��μ9�~�n[_�U�{3���I���3�\>���5�i�-y�Ƃ&�i�}�6\ْI9''�޹|�֎��.����`���0# ��۷�����|L\�u��^gqeq�t)����)��a09��9�>�0y���cOgh��d�����\�' ��ַf�V��H-ݗ3�H����#�}�+��g�4o�{���a�$Ѿ:c#�����S���G���*v�O���^G����43��J�RE*�=2"���QּWỨm�.�H���J��}~��Wt�jڌ�&��9d��?6?�lpz'�|B���k�RBwy�
c��`zp^zש�5�6���]J8�#����H�s�ڪ�4� 2�1<�kN�
 <��'^)�s~h����,AA�/��P�=�9�^����^G-��	9��;s���J�=؁�ʟ�G����xm4��|���g^s�{�����q\�@� �<�;���Ն�.'�mI��?����w!���%�	RXۣ��Q@ȉ,m�����2��⵿��]��\�m#�\~�t#�N9�v��n�Ⲵ{��������T^ڍE��nRf��ƅ6�H�m�9\�#�N9�I�;q�\D�<�4�;3�,��$��ՍJ��׸u	��$� {�RzU<ח^�<��i��V���=� �_Ɩ�NE.�QK18 �}+\�ܒW}��,P�y�(�Z:� �����}v��2�o��	�8��8��U�+���-�R��[��2?�Ӯ3��==�`L� �9�V�=b�#��a��?��F�.��G�fX�_���o���c�����H$��9��4Wa�	������	�<N0�{ӳI� ��J�]6�KY��O��cz�#�� ֪���|E�.�f^(��#�l�p��ǿ�^r��쎥]N
����Z|��,&+��]й��34��ξc��e���氙��-�nq��:t�;��V����q$9�.N��"��oe����<��FFA�A�8���/�?�lSˋv١?����؎GO_�T��4wFTe�ѫ�Ko^�?��m3��_f��d��
�PF?1��\W8<u�ߙ���M��Ċ9���G9�Y���H�F쎄2��GB��?��$W�]q��'�d��v�O]��S�ZX��p|�u]��2|�78 �A�x����K�MJ?6V`2˜:�:������]Ep��;9��C� -/3�G=:�{WJi�Q�,��v��s#��$�>�rF�
������m-�^�u���#op:u� ��t�Kz��X
����d��0	�©�894��c�
F�x!��� r^%��E"�7
��I= ���ҼCe2�o��3n�ח���꧁��=+�v����!�"�?y�G��8�}�bR�=�@������q�x�5�nΜ>�wh/�C��5}6���Z(��|~=ϡ�H�q:��>�8�m��aQs�z���j����ً19$�I��
��=��`r�Xe�'yw�.h���=�ګ����cמH�T���g)k��pȡ��T�f��p�#���TF���W0���*��\�ɲ��@g�ʙ�Sۡ��k�v�H�m�����I�x띧�������~����KK����lA�8�|�׎޸9���V�Q�ڳ˯V�#��G��� �=��注�!I�%�ܞ=Y�����啬VP�@1Jp2}�;����'�tE��� �\�3�S�'?�N~���]T�e���j���d?4S3Ehs	�L�3Fh��Wľ�F����ޖ >� �����z|њR���4�RT���3F���Gᅒ3y��E<0�=}��z�;��Pqz��Lj��Mէ��O�"_��q�N���{��s��Z��.jS���Ҝl��T�M�ɠ�ϳ���'�Ig�G���ڋH�X��ct�qc.7F�^A���L�sZ�k
�qo'�g/1�?��?�**S�Q������g�G��	R�A���F˩N ۀ� � �^���R�v=)ѧQZi3w���-Sȶ� ��8�~ls��b��[�����Ʊ)¯�S�eXG�!��&�kv�Cn�ND�[r�2q���5���diC��� /���`�v�u�>���0�VPF���B����N�������={RM�;w��h�*H��1���k�3ҭW���yf�m���������j������{/�£��n�q�Ɏ��ns�;���~���U*�}Nie�x��������=��!�>���:U6��ji��.1��t"j�|+���q�wk���l1��������7D���ޠ?�[r?"�������S����/r~h�34f�<�����(��4�њ ~h�34f����<9o�n��w�� ��7�?� V�h�&�ѕ8����,�t���F90A�z�����[{�70����:������C�3!/��$@	��8n�<�v�%K����'��9lֶ���h�H��m���!-�r1�鞇�q�YwV�Snax������zT9���u>Z��Tv�ZZj��J�F�q���N�q���I�x����ê��ˤ���u ���+����Ų��G#ʠ$wI���s�=px'��bT�=V�������~��c�®&��0��|�{	�1}�q��~a�&���%=�>&�ex;�){RԽ�3�j����=*��Ț�oz�ogq{7�mH�g�������V���½��1���������E:r���qX�TW��0-�'��Cow#8����G��V͹�q�2���3����H ��!�h;(���5&k��z�9��η��C�Fi��5��?4f��3@���@	�3IE .h�% f��E �4Q@�(���4i$m�]A�5�^�/O�l�[> ;ׯR?�t�Ri=ʌ���]�+P�{[Km����ڳ���n���B	��Ȑ�JI�P�����b�-�<��h��b���G�f����0z���eq U�������oϜu' Mz{?0������9�{=f&��6�3��,�8�8�A��N�t�%�EUs������p�l�EEg,59ts�U-���0c���
I%�(X�b��^zm�{ո4+8����b�;��s�N8���Ӣ�4)ǡ�l�[y[�As�
���U *���O��Q[�(�� (�� (�� (�� ��
endstream
endobj
2 0 obj
<<
/ProcSet [/PDF /Text /ImageB /ImageC /ImageI]
/Font <<
/F1 7 0 R
>>
/XObject <<
/I1 8 0 R
>>
/Properties <</OC1 5 0 R /OC2 6 0 R>>
/ExtGState <<
>>
>>
endobj
9 0 obj
<<
/Title (�� O r d e n   d e   C o m p r a)
/Author (�� W e b E R P   4 . 0 0 R C 1)
/Subject (�� O r d e n   d e   C o m p r a   N & u a c u t e ; m e r o   1 6 7 3)
/Creator (�� T C P D F)
/Producer (�� T C P D F   4 . 9 . 0 1 4   \( h t t p : / / w w w . t c p d f . o r g \)   \( T C P D F \))
/CreationDate (D:20241120133346-06'00')
/ModDate (D:20241120133346-06'00')
>>
endobj
10 0 obj
<<
/Type /Catalog
/Pages 1 0 R
/OpenAction [3 0 R /FitH null]
/PageLayout /SinglePage
/PageMode /UseNone
/Names <<
>>
/ViewerPreferences<<
/Direction /L2R
>>
/OCProperties <</OCGs [5 0 R 6 0 R] /D <</ON [5 0 R] /OFF [6 0 R] /AS [<</Event /Print /OCGs [5 0 R 6 0 R] /Category [/Print]>> <</Event /View /OCGs [5 0 R 6 0 R] /Category [/View]>>]>>>>
>>
endobj
xref
0 11
0000000000 65535 f 
0000002290 00000 n 
0000012772 00000 n 
0000000009 00000 n 
0000000117 00000 n 
0000002348 00000 n 
0000002463 00000 n 
0000002576 00000 n 
0000002682 00000 n 
0000012941 00000 n 
0000013333 00000 n 
trailer
<<
/Size 11
/Root 10 0 R
/Info 9 0 R
>>
startxref
13698
%%EOF
```

## uploaded_files/9844QJ_document.pdf

```pdf
%PDF-1.7
3 0 obj
<</Type /Page
/Parent 1 0 R
/MediaBox [0 0 612.00 792.00]
/Resources 2 0 R
/Contents 4 0 R>>
endobj
4 0 obj
<</Filter /FlateDecode /Length 1092>>
stream
x���mo�H���)�U�J	�Gv����$ŉ�8R����ȕmR�Iw����u⓮*�Hx�=��yvf�_*xC<~���8��8�������'(�	��/����ۏ�/���^�������LI�3	�����&�賙�(-���w(���	����Ŭ���ju=o��*X�-���j�	��O����w�|��\��j}=/�Z�4�Tտ%*�1@�SM�������q��0 �wey�p_}���J�;7���@�fXz�it���,�Ӄ��lM�.:��ކ��bGc���L=$/u���WEr�R�����)���u�H�3ۊ	ʤ�Z��!*��J2��r]�Z:��SK_�=mʸ�d�<��l@*�S"I0��Mϋdd�3�����2��4��w�����#�7����C�(z�_�=��{'h���$D�H�6Y=��7dխÇrU�f�	�H!��w�flyC|���'��6VJ��vX��ݼ^!�Q|f�8��`T��V7T-g0�����3�Ven�
"��H�]�E:H!>��(�R�z_�]³\�c���i�8�ɉMS�0P��m/!�'�8�>���8O�6�f�I
��A�n [^Q�{���%�0�{��PJ5��&Y<$�$#ꡉ� K.ͫ����4�~�Z�7�Vd�Z��QId��?��
�sgqiIS"|��P$�6�6E�x(E�]��9\�c�9�HL���\�����Q���,x[�X���/��J�P�-�|b�������$nm�8U�,�J�J��e6��s־��p�/�w85c����~����+78-(G����e68��q*j��Oۍi�y���kHm]�sG^��G�6-�!#����?���z�Ef�·�/:����7�i���d?t���2��ra��Қ5�~�|�0�ֳzY��,$2 ��[����W��ߠ81�8a�r�{�vO�Dgf�<�4�$
�97W8��7P-O(ntD�Ϧ6P��=�P�2f4��>�!��vRl!z��������'����5R͗3�د���zϱ�Y��2�R���?�Cޝ- ���[���	
�]	c���(||~�����'�5{�_i���
endstream
endobj
1 0 obj
<</Type /Pages
/Kids [
3 0 R
]
/Count 1
>>
endobj
5 0 obj
<</Type /OCG /Name (�� p r i n t)
/Usage <</Print <</PrintState /ON>> /View <</ViewState /OFF>>>>>>
endobj
6 0 obj
<</Type /OCG /Name (�� v i e w)
/Usage <</Print <</PrintState /OFF>> /View <</ViewState /ON>>>>>>
endobj
7 0 obj
<</Type /Font
/Subtype /Type1
/BaseFont /Helvetica
/Name /F1
/Encoding /WinAnsiEncoding
>>
endobj
2 0 obj
<<
/ProcSet [/PDF /Text /ImageB /ImageC /ImageI]
/Font <<
/F1 7 0 R
>>
/XObject <<
>>
/Properties <</OC1 5 0 R /OC2 6 0 R>>
/ExtGState <<
>>
>>
endobj
8 0 obj
<<
/Title (�� L i s t a   d e   S a l d o s   d e   C l i e n t e s   A n t i g u o s)
/Author (�� W e b E R P   4 . 0 0 R C 1)
/Subject (�� S a l d o s   d e   C l i e n t e s   A n t i g u o s)
/Creator (�� T C P D F)
/Producer (�� T C P D F   4 . 9 . 0 1 4   \( h t t p : / / w w w . t c p d f . o r g \)   \( T C P D F \))
/CreationDate (D:20241128093049-06'00')
/ModDate (D:20241128093049-06'00')
>>
endobj
9 0 obj
<<
/Type /Catalog
/Pages 1 0 R
/OpenAction [3 0 R /FitH null]
/PageLayout /SinglePage
/PageMode /UseNone
/Names <<
>>
/ViewerPreferences<<
/Direction /L2R
>>
/OCProperties <</OCGs [5 0 R 6 0 R] /D <</ON [5 0 R] /OFF [6 0 R] /AS [<</Event /Print /OCGs [5 0 R 6 0 R] /Category [/Print]>> <</Event /View /OCGs [5 0 R 6 0 R] /Category [/View]>>]>>>>
>>
endobj
xref
0 10
0000000000 65535 f 
0000001280 00000 n 
0000001672 00000 n 
0000000009 00000 n 
0000000117 00000 n 
0000001338 00000 n 
0000001453 00000 n 
0000001566 00000 n 
0000001831 00000 n 
0000002251 00000 n 
trailer
<<
/Size 10
/Root 9 0 R
/Info 8 0 R
>>
startxref
2615
%%EOF
```

## uploaded_files/9866WK_document.pdf

```pdf
%PDF-1.4
%ÈÁÄ×
9 0 obj
<<
/Length 2021 
/Filter /FlateDecode 
>>
stream
x��Z�n+��߯���U|�X�� �&Y�d0�,�w��OY�f��-��%���ԻXm�]�2�
�N*A�.�����M}�����)@���R�o_�_���A{O��V������ˉ�^8LOA�U��]To�W'���64qlڱ�l$tÐ_]��C����6Vc7����ڧ�N���py�@O�'ѓ�y��L�3Ð�g��1��/y��U�(KV�]�]��-P�e�m�b��nPS)x�2�D��\��8y��!&H� !�b�	$~�Ơᐞd�	ؠ'|P�F��!g��8���aaʳp\�O����,��:y�����K:�����*���U����M�M�G����і~2�Am���@S��M�� n���7�\nʩ�ԩ�-��=��]j�*�z���:�:�G��@i@\�H6]L�5��������R��j��<�,J�Zb�eP�eb���z��f�d6��&$�<C�,�o_qs��r�t�IC�o�$�?z�����z��\� � ]��N%��/J�����:`5��>`sH'l�19p��&2�p�4�@4�Xr:�(pG��o�Ja�U=��"j�8v
��,ʈV��-7��W"����N4��A�Mz��3���oLFߙ��졙�y�������e����a{�IV�'�э���yYv9��,ֺ8*J>3|ꐟ�7��F�7�+9�d��#l'C����=�.;�:	�]dbG��-r���Sd���ڏ^~\𡉗�s��h�Qf�d���K�I��L��ydF��1��;	U ��ߋ���(�]k�G��>z͞��_V�,=J�ؓ#=�%��:�g���.�?ɔ�&�t1�4��@��Xaԡ��ߓӑ��x$��tY�����һ?�k�M�:�Dcm�ĸ��N�uSU��Y�$�z�C>B' ��Qz�����͌�U�e��(�8�d�>=u
H&nKn*.�+<"�h��O��&�
ł����m��D&ȶyՀ�\"�H)�M�f~�}�k7�oy3�&ix$���p�b��o:x��8	�lB�)<� ���`��%\=�)�����D_��M*v���Yđy���
�8a���~��u�)�����V��}��G���%?s8����	�hPH���~?܊,q�g�%���醛��|�I��z�t�ո�W,��)�)3�����&)���K�祍fY��]ʿ����G۴�/��5R��J�br���~{Cpt��w������9ڐĒ�*���v���Nؼ���()vff5GcL�hf�@��V]��� ��/��)��c9T.h�h�%��6Oi�Y� #�ŗ��PW�Ϙ�0s�.z6�5ִrY�;�v�Bo��L�ͭ�� ]�Hǚ�a����J�ߒ�V7�s5�oׄᦕ'5�=&%�h7K�*�� ���nw�+P��Z���*iҋ�:�dr+0Bs���wYu��b\�ġm����.�#j�=����0��x|�WS���]i�>��_ާ�{���:��w�*C��B'WR� GJ���[�Ŏ�+�['w9f΄֔�ʚ�.,�+�q*s���Y~��7��@��{<+�X}���}�<43�[}�J((��)9���NN�m�_�@��a嫸�P.f�T�rڹf��t��/���ģ�|@x�D�p�P"d��Ԑ�0��$<����(�R
x��X��R0�$�3>Br�ѕi���vtm�K�r�S�'�����A�_�/�'Yg[e�]���̐��%n� rѪ^���k��uA'�d�
4��Z'l2�*m��CVБ��j	��'� x��pVΈ�����������\n�UMZl*���n�߷�hgh�~��o�[��&öY��;6�8j/��is��_�8�A��4^}�;�k�����e���ɓ�ؼUEA���u�<��+�,#h��Pg���,���Q���.C��犢���@�o������w?�W����ԗe�SCg��������?��
endstream
endobj
15 0 obj
<<
/Length 5411 
/Filter /FlateDecode 
>>
stream
x��]͎�q�ߧ�4/�)�鞎d{�,ob��'���~���+Q,Q�w0gZ<���HV�,�Z~]�B�?�0J�ee��u����u��wy�����������O��T�gD)[@#� ����?�ϯO6uS�U.���H�|����Ih���}J�<?��(��ƢK_��2�ӟ����S+]���*Q�<�rBK����c�g���~>���~��������W��~���@��l����fa�/d?��Y7":5cu/(�6fkF�dj�,_&�G�GA;�+[��t��	m�V�!4�0��l�X`IN�����]����p<�V�_�	c�<C�C���;�]��o��&�Z�-�؄\�^�������o��,�.���/�����P"�O�OOJf�RW���s��}T4�u��uay
��@H\��6��o��l��|Dqbx�RP"����YKɱ$QFGu}��A]��g"'%�~�t�9U}�J3@�]i>��
⠼��G�_ q4����}��+W5��/�V����o?�������Z�-e�q�zץ�B$�b�0�%�d\̓Z�g�b���xT��a��fB���G �b�[��ᢔ�c+��Ri1�C94�rN�Ǟ�m���@'m[!;��I��$V��V���g'r,�p�If�
u��>D�|4�#UW0�	�@Q�o�¸���A{��m&�tY�◑�TPzmݱ2��T_~.�?�_�;r�;��>RUBQ�! �wM����+�)����K��EU_��;���um�h�nq���w���vo�ͽ�`��7�㑭tv�0RI�sn_��Pԃ8T������|�։=z��T���(���Y��7(��Z��6�8��R���N2��Gd}1������@��	]��n�lF��Q�����l�eʰ�ڥ��[L ��,�Ƀe|����"+�5����iЮd���M��>cgC&�C����Cf�pai^�E|����FdGu�Yg�6�nga��y���s��YY;����K��&�&�����gO~�]��,��[�H�7�h�(!)�y��X�쟯�r ���b���u٬�L8Bx�\}%�D�:�tå�?�����ҧh*���u8\���"�pB�l}8�D�:�h�#y�:!B�>��"t��E�	E��![N�?��n��d�A-�c����VWĈ�Q�(�Q+aQ�YcΜ{���d���<K��jL���[�LG�.[Ud۶I�Uق�^�u�f���C{)�1�0�?yg�����q���9Xǣ�tDY�:x3�WMǬ��<�}hb$�4ݎf]����ͺS4��M����:A�c�TkXq���ͯ�ܽG�Io&���5�l�zTAA������~�ǵf��%��������(~���l��tqG�.[[��I�Uٲŭ2Q=G�.[�D�u�hU� j}^)��s��}h����G��^���
�7�"��S�vb��Q{Jkd�UG��ۭ]��}��+;�����Xp�F�ߓ�˖D-�M��D�[@�sD�%Q;7X�$Ѫl�+�F���DW;O��ѺlA�
Yghl���Rt묦��b�\��x��Jtm��J�D�%��6��$Z��ыؑZ���"�k��f�7/1]�_\�u)�\����G2�Z�b��7��8}�Ӭ�6��oDeGߴ�uTKr4J�v�ѷ+��
���C_�b=��]����YxP�Ѱk��$�vm��P)v��J�>�Xaj�:�Y�CH��7�ar.�cg&�Q���t�۹�b�v�Yf#ͬŐ;<��aQ[����nu�򤛶�&�vB���oD��X�~ݥ�k9��X���YK��,q�D;�n_粀��� �6�<�Z	ьÉ!E1Z��#y0%�������ĬM��B%&p��b�i�{�i�nZ+�@�,��i��Fّ�A���$M%�1�CS4�":����{BL�' �SJ�㰎�^�u yM� � HE!�	�
C"6�	< 
# 
Rd=AU�H�&`A�`A�`A*‬'�j��,�D��ekA*‬'�j��,�DX���t�����a$r}X��J��Nm�diL5�s�����VErg��j��YJ���h�ܦ��O�����:b��f.��Me�I�]Ǝ9;4��֢q���i�8��@�Icv���>��m����Z*��6:��)?v���M���Ga�8��h�!67d$��]D�u����A_�Qg�Q78nn�	��#Ժ
P��X�6$����!77�l'�J���u8��r��R˸Ǹ��g9��P�"@�y ;�岴��'"�|R��*Z�\"���"���q���R�O��Ñ�ey��s�#��{|���%�D�:�gE�D���r����;i��Q����ȉ:�_�]�в�W�-����$Z�-W��S@��y�8�#��u+	�Ʉns���Q��T�G��xタ�k�Pdl��%?�Һ{���X7��ط��%I�)9E�*Y\�M\'9X�mR�I>��?�PH�B-�r�kY��28��@	ũkK�^��.��O6��?\DI��SVA�wt	�.��Y����F�I�U�2�@�s�'��76��hE�����x@��G�yK%XV-��)��v��q���T��Ym�p�%[.�j;�d|��@|������ͅ��`���Wӝ�����<���cWYB���#j���*����ULX����d���&J�7jP�f��������ڒ��5�w��%9����K�RٯB*��m�w|F8G����K�zb��tDLP8��2t���S7�I��-�lǣ�����|�x4����pP�o4�������M�!z�)��4xX�l��E�G����UE۸��a�o$�Rw��
�d�X��&��d jw���M�	�>�l޴�\���#.�6E���[�A�m&2�{fbtr-����D�, �y� ��4��%�5t`�ܢ���>�Y��92nL���/�t���66���h�qn��YH�n��9�Tg��/A�ݗ]S��|f�qn��>�,`AL�$q�����&����]���l@G������j�M̄� �����r��ס9H�n��9�~�g�y�����j�d|���{��� ��cAL�=�8߬�o�(:ZO����H6�p{�`�U��rj������>��&�67���o�6�P64��M0:��x������4��R~N/��q!��T 2�䉥�k������@�3H�w��ǳM�2z�`�\�F�۪�~X3o>)�/H�n�9��I��~�P܀#��+>�G)>����#��)>��]��x6��XF��{�V|)��1sg�Ѵ��2�~����vt;H���8�'�vM�4ÅM��nO�6��U���|-���t��q���ˎ�l�q ג�7�*8f��el���X�s��ܳ4��Q7�������?�R!�k��"�o�FAֆ�Ol��ɏ"b�%o+J��r�o�y9c�x����u���D���/�EdK��E񣈃�`�O�⾙�E���勁(R�����[��k}y�m`�WlD�8c(:�.������%���9�#l{�����%�� (p.�@
 ��}4�L�:"8c��|@����}L5�L�:(8iA��J� @�>�@$ԅ�L���Vك��3�V�e�����K>ˍ4(��X�?(0�<�9��5��5���ʏ����Ħ�v�I����d4V��AFx���
qS� )`������#@BIg8r(7A4l*|����F	=���sAõJ�u�+,3����4[��s�I8Y�}�8�8~�+�3��{�y������Pp4��'�Xz�.Z�\���Uwx�:�;�#���<Έ6pS�8�u ��U�1�[��>qS���P��B�M:Hi����'3�N�J�r���(5�I1�_���$I�i:P�2�IO�:�xd�!�0��{���b�(G�7���6Es\;�)M[����Y�@��Vgz׎��0k�.1��`u��,��KI(E�j�]�{��o�t��8�~6KY����;��1�&�������%g�,�R����󰃍GI��>���W�+�.8XAy��K�=�����d%D������n���L4���j�呁�΁�!t����7��^qK<C�e�H�oڐ�J�#�(M�j�npJ(��v�<Fv 	�]�'۰0��+�Ҷ�����XL��{ &�hpL-A�	����A��`�;&�����}���ľ2�
+63�Y�PXڇ�(lf~Oa'+�F���������f6?X������}��a�y�K������ �23؆���ѵ���@fM���f��L��>����W�_^�)�'��]SӭC��P����Ȅ�	N�0t&돒�`�wKw��)��q9�z#��Ep<a�!ps���J,񹳖m'�i1WP�Մ�"c�"�0�C�7���¯) ?	�9��8�Q��D�@�O8~u���r����Ch|�bK�������E�ݫ�0�@��|s�7���A�	��ԑ�#}�v�gɮ@�B��=���z5��VQ(��,�2cg��k�/|�]d����]�|�XΚL.��/�SG[�qvw��C�5K����ƌ�>�����D�^���@�^Bٻ�Po�<\���0�(�%��x��̕���u?Ε{E�hԅ{���=�έ�
� �y��i��۪�뷙�5�K���2Ȍ��s���A��pr��.�~v:����M���j��eK��p�N��D7J8�f�^jy?w.}|ᤂ��b��V��+���)�`W����{�Sd� }��N��X5y��q���9��؋؜�)ׇ��12(���\k;߀L�\%ҹeAӭ`4�i|4�y?������~?��xi!��!�����5���>;�Y�g�ݜ ^�����������ĵ��Iw��kF�Et������b��ƺ������ݹ�<��+�$'��&!��k�Xo���������m�^�m�H���PN��2"��]#2W��ep�0�DQM+�nG����כ��`L�㿂������l0�}$��
Ig0��d�r���++|=��Z0S��W�[3�v�ҿ��@(d�w3�>��x�{L�pr�%gb�W@� ��x_JH̼
J_��m1�jff�9�u�Tv#���6̯����{No�
��7�Ē��5`ض%V��)�@*��*d={5T#�ü�h��������xFn	�%ynQ;�Nx�F���:����Eo1�O
�������ʣM�ʣI���+�h��V��ܥ�
endstream
endobj
6 0 obj
<<
/Parent 7 0 R  
/MediaBox [0 0 597.6 842.4] 
/Type /Page 
/Resources <<
/ProcSet [/PDF /Text] /XObject <<
/DLb1 8 0 R >>
 /Font <<
/Helv 12 0 R  /F-1 10 0 R  /F-0 11 0 R  >>
 /ColorSpace <<
/DefaultRGB 4 0 R  >>
 >>
 
/Contents 9 0 R  
>>
endobj
13 0 obj
<<
/Parent 7 0 R  
/MediaBox [0 0 597.6 842.4] 
/Type /Page 
/Resources <<
/ProcSet [/PDF /Text] /XObject <<
/DLb2 14 0 R >>
 /Font <<
/F-1 10 0 R  /F-0 11 0 R  /Helv 12 0 R  >>
 /ColorSpace <<
/DefaultRGB 4 0 R  >>
 >>
 
/Contents 15 0 R  
>>
endobj
7 0 obj
<<
/Kids [6 0 R 13 0 R] 
/Type /Pages 
/Parent 2 0 R  
/Count 2 
>>
endobj
2 0 obj
<<
/Kids [7 0 R] 
/Type /Pages 
/Count 2 
>>
endobj
16 0 obj
<<
>>
endobj
8 0 obj
<<
/BBox [-20000 -20000 20000 20000] 
/Length 113 
/Filter /FlateDecode 
/Resources <<
/ProcSet [/PDF /Text] /Font <<
/F-0 11 0 R  >>
 /ColorSpace <<
/DefaultRGB 4 0 R  >>
 >>
 
/Subtype /Form 
>>
stream
x�U�1
�@D���]`�ٍ�?I��.�]��J��/�Za���=^��<�cU����sߘ�����%�����"X,Vi�z��I�R?��D�f�
��r3����F�vpn˷z�
endstream
endobj
14 0 obj
<<
/BBox [-20000 -20000 20000 20000] 
/Length 112 
/Filter /FlateDecode 
/Resources <<
/ProcSet [/PDF /Text] /Font <<
/F-0 11 0 R  >>
 /ColorSpace <<
/DefaultRGB 4 0 R  >>
 >>
 
/Subtype /Form 
>>
stream
x�]��
�@D�|���]g7������]�v�J�*����BPf�y�M	5%�Uq��K�m��C���A��K�`�X��e��I�R?��!�E+L��S��\��+~�����7vu�
endstream
endobj
18 0 obj
<<
/D [6 0 R  /XYZ 10 866 null] 
>>
endobj
19 0 obj
<<
/Names [(Total-Page-Count) 18 0 R ] 
>>
endobj
17 0 obj
<<
/Dests 19 0 R  
>>
endobj
1 0 obj
<<
/Names 17 0 R  
/Pages 2 0 R  
/PageMode /UseNone 
/Outlines 3 0 R  
/Type /Catalog 
/ViewerPreferences 16 0 R  
>>
endobj
4 0 obj
[/ICCBased 5 0 R ] 
endobj
5 0 obj
<<
/N 3 
/Length 2591 
/Filter /FlateDecode 
>>
stream
x���gTT��Ͻwz��0tz�m �I��2�0��ņ�
Di� AFC�X�BPT�� ��`QQy3�V���{/��ý�����]�Z �O ��K���C����1�t� �`�9 LVVf`�W8��ӝ�%r���# �o�����I���  �ؒ��b��@�i9�L�}V�ԄT1�(1�E����>��'���"fv:�-b�3��l1��x[��#b$@ą�\N��o�X+M���ql:�� �$�8�d����u� p��/8�pV�I�gd��I��K�nngǠ�pr�8�q0�������L^. �s�$qm�"ۘ���[��Q����%��gz�gm�w۟�e4 ���f�ﶄ* ��  �w�� $E}��E>4�$����999&\�D\���������x���C��$2�i��n���!����dq������0
�$r��("R4e\^���<6W���ѹ�����}�k�(�u�	��F�� E!$n�h��o�H �yQj��������.?��I���C��,!?���Z4  I@
@h=`,�-p .��� b�
�� �A��@!(;�P�@#hm��'�9p\��0�F�xf�k� A"CHR��!C�b@N�' �B1P<�� !�m���2�����o��9�24݅Ơi�W���$�
��:�)̀]a8^'���5p����#p'|�
ã�3x�!�1�@ܑ $ID��z��@�6��Gn"����AQPt�1�僊@�P�P�Q%�j�aT'�u5��E}D���hC�=��NB���&t�z=�~��`h]�-��I��Ŕ`�a�1g1C�q��U�b�AX&V�-�Va�`�`o`'�opD��煋��p��
\�4�n����k���Ax6>_�o����'�i�.��NH!l"T�/�D�юB�7+�G���cķ$�ɝG�v��Β�^��d�9�, � 7�ϓ��HP$L$|%�$j$:%nH<��KjK�J��\#Y!y\��^JG�]�)�^�F��m�9i���t�t�t�t��e�)�����[�@��y�q
BѤ�SX�͔F��Cե�RS���o���YYY+�H�ղ5��dGiM��KK��Ҏ�Fh��T�\�8r����n���+ɻ�s������)�<Rv)t)<TD)(�(�(�W��8�DUrPb))S��+(�*�U>�<�<���⭒�R�r^eF��ꢚ�Z�zZuZ����U+W;���.Kw���+�}�Yueuu�z�������F�F�F��CM�&C3Q�\�WsVKM+P+O�U�6^�����W�_{^GW'Jg�N�Δ������V�zd=g�Uzz��1��T�}��`k�d��k����!�p����Έg�`tۘd�j�m�j<fB3	0�7�2yn�ek�˴�����Y�Y��}ss?�|��_-,X5�,ɖ^�,�-_XZq��[ݱ�XZo���`ck÷i���ղ�����͠2�%�Kvh;7�v'���������`����0�Dw	gI�qGG�c���)��Ө��3ӹ�����ۥ�e�U�5����s737�[�ۼ���:�����G�Ǡ��g�g��#/�$�V�Yok��g}�>�>�|n����|�}g�l������������z�@��݁�j/�-�
A�A����
�>R�$�<4/�?��2�%�u�[xi���aDo�dd\ds�|�GTY�h�i���1�1ܘ�XlldlS��2�e{�M�Y�ƍ,�]�z���+�V�Z)����x<:>*�%�=3����K�M�M�e������]���i�#��3��X�8�䘴;i:�9�"y��έ�H�I�K�OJ=����֞�K�O?�����2T3Vgeff���_�g�,ߟߔe-��PE?SB=��X�SvM���Ȝ㫥W�V��nϝ\��뵨����y�y���ֹ��_�OX߻AsC�����o"lJ��C�Y~Y���Q�{
T
6�o���Z(Q�/���ak�6�6���۫�,b])6+�(~_�*���W�_-�H�1XjS�'f'o��.�]�ˤ�֔����YN//*�g��Vu{	{�{G+*����vV��N��q�i�U��^;�����~��mu*u�u�pܩ���l�i�8�9�}�Icdc�׌������>�=z��ٶ��E���n�N�;r��o�ی���i��G�Q�ѧ��;r��X�q��﴿���tuB����]�]��1�C'�N��8�t|o�����'kNɞ*=M8]pz�̚3sg3�ΜK:7޻�������B�/�_�t����~��3�/��l��ƕ��6W;�:~���c�f������v�{�����|��M��o�޺:�txh$b����ۣw�w���}q/�������J=�x����G��GmFO�y�<{|�5�짬��O<!?��T�l���:9�5}�鲧�2�-��,�s�s��������l������_K^*�<���U�\�ܣ����(�9����]ԻɅ������?�|���`1}q�_����
endstream
endobj
3 0 obj
<<
>>
endobj
12 0 obj
<<
/Encoding /WinAnsiEncoding 
/Type /Font 
/Subtype /Type1 
/BaseFont /Helvetica 
/Name /Helv 
>>
endobj
20 0 obj
<<
/Length 480 
/Filter /FlateDecode 
>>
stream
x�]����0��<����*x�I	!��HڭJ� !14RI"�����Us ���؟'v��o�];��{��ͩ���-������̊i�zL_�����_G�w��̖K�����c���u�����Ƈ�;��_��ć�0��ߍfnV+��ӣ��j�V]��b���<�g��}�F���Z��ס�}������O��,wӳ23�5�G�dO��*���+���(�Q�[�.�y�2�}#�%�z�D��@p�]�TN|:�&b����M��,�������k�[p"߲ �ױ���_�,|5U�/�-|�_M��%���_}!�7��o�&���W�+l���산��W蛂�� �u�W��u_���
wC���W�[$������x%�W�7Ok�o��Q�*��4
_��(|5!|�

_�g��/?3�oN}�oI_��c���e:�#o���_�B�n�x��s�8�m�?/��b> �K/
endstream
endobj
21 0 obj
<<
/DW 500 
/FontDescriptor 22 0 R  
/CIDSystemInfo <<
/Registry (Adobe) /Ordering (UCS) /Supplement 0 >>
 
/W [0 [0 722 610 889 277 556 610 277 722 556 610 333 666 556 389 556 666 556 556 722 277 556 556 277 610 556 556 556 556 610 277 277 333 777 610 833 722 722 666 610 277 722 610 556 556 583 943 610 556 333 333 556 277 556 556 722 610 610 333]] 
/Name /F-1 
/BaseFont /SUBSET+ArialBoldMT 
/Subtype /CIDFontType2 
/Type /Font 
/CIDToGIDMap /Identity 
>>
endobj
22 0 obj
<<
/ItalicAngle 0 
/MissingWidth 1000 
/Type /FontDescriptor 
/Ascent 905 
/Descent -211 
/FontBBox [-627 -376 2000 1055] 
/StemV 0 
/Flags 32 
/FontName /SUBSET+ArialBoldMT 
/FontFile2 23 0 R  
/CapHeight 715 
>>
endobj
23 0 obj
<<
/Length 25656 
/Length1 25656 
>>
stream
    	 0  `loca$T    cH   �fpgm�� ,  �  >maxp
�    �    head�     �   6cvt ��   8  `prep\[ =    �glyfW/  !�  A�hhea�     �   $hmtx�    �   �      �ٮ9_<�     ��<    ք����� r  	         >�N C ���z                 ;  � a� R ~9 �s 0� �9���  s U� �� V Js I �s V �s As � �9 �s Fs V9 �� ,s 3s Ws Ws S� T9��9 �� s9 Y� T� �� �� �V �� �9  � �� �s #s �� U� � �s &� k� Cs A9 us Ms �� �� �� ��     ;� < �    / V  K�  A T���5  �� < ���A� ��  �  � ��  @��2@���2@���+2�����:3@���-�2��� _ 3����U3@���@D2@���3;2@���/12@���3@���2A� /�  � /� O� �� �� ��  � �� �� ���F@���3A�  @� �� ��   � �� �� �� ����	2@���3A�  � � �� �� ��  o� �� ��  �� �� ���A
� � �  ����2@���2@A� P�  �M �M  o� � ��K�-12���K�
2A�  � ��  ��   � @� ����2@���2���{�042���{�2PAx en # ~n  cn  bd  ��@�2�A? ? ) A 2 D  ��u�2���u�(*2A
C 2  4 �2 �@  @��	2@���2��  ���
 /
 ��T�	2�AT �T  n  �n  @n�	2AE  k  F  �� F ��&���  @��	2@�>�3@�>�2�A	>  �� �� ����&82 A&( 0(    0  � 0� P� o� � ��   � 0�  /z pw �w �z ���2����$(2��2� ���	2@��2����2?�s Os  @t�2o�*  @,�2@�p�	2� 2 ���2�  ��A   ��  ��  ��  ��  ��  ��  ��г	2@�ҳ	2�A�  _� �� �� 0 �� 2 �� ? �� d �� 3 ��!����!�@���2���ò+/2���ò%2���ò2���ò2A%��  �� $ �� " ��  �t � �5 ; �5 ; ��  �� 8 �������������� ����P/���  ��&���&$�5 �t�A
�X� � ��  ��7����� ���@7@%@-@�0%0-0� % - 7 � A�  �� �� 7  � 0� @� ���7�A�t �t  �t �t  `t pt   t t  �t �t  ?� O�  �~ � �� ��  �z �{ �| �}  �t �u �w  p~ p p� p�  pz p{ p| p}  pt pu pw  `~ ` `� `�  `z `{ `| `}  `t `u `w  P~ P P� P�  Pz P{ P| P}  Pt Pu Pw  @~ @ @� @�  @z @{ @| @}  @t @u @w  0~ 0 0� 0�  0z 0{ 0| 0}  0t 0u 0w   ~    �  �   z  {  |  }   t  u  w  ~  � �  z { | }  t u w  �~ � �� ��  �z �{ �| �}  �t �u �w��A�~ � �� ��  �z �{ �| �}  �t �u �w  0t @t  �~ � �� ��  �z �{ �| �}  �t �u �w  �~ � �� ��  �z �{ �| �}  �t �u �w  �~ � �� ��  �z �{ �| �}  �t �u �w  �~ � �� ��  �z �{ �| �}  �t �u �w   ~    �  �   z  {  |  }   t  u  w �X �)  � ~ � } � | � { � z 7 w & u   t �7A5 O5 _5 o5 �5 �5 �5  �5 �5 �5 �5@"O�����O����� A  _5  �5  5 �5  /5 ?5  ?4 O4 5544@� �*�*�*�*�*A	G    7 X@&>�&>7&'>�����&6���&6�)@+&6�&6�&6�&6�&67&62&6-&6%&6&67&*�X@"&>�&>�&>'&>!&> &>7    @���� 	���'(���'0���'O���'bA	� ' �  � ��������������4�]�'.�[�'�AU  T  S  R�V�Q�)�+�'&A* '% )X � %  $���#�;�"�9A '  -   ���X@�������� ���%�V@
�-��A�A
X  �X  �X��%���X%��.�-���)��X�� ��@�0t-�sJaR]%���\�  YX��P%�I�%�G%�@Fy@'9 ��  8X�7-�%  2X%�,4*%��U7�@*��[B;#"
 ���@+                     J �KKSBK��c Kb ��S#�
QZ�#B�K KTB�8+K��R�7+K�P[X��Y�8+��� TX������CX� ��� ��YY v??>9FD>9FD>9FD>9FD>9F`D>9F`D++++++++++++++++++++++��KSX��Y�2KSX��YK��S \X�ED�EDYX�pERX�pDYYK��S \X�  ED� 'EDYX�B  ERX�  BDYYK�%S \X� &ED� !EDYX�
 &ERX� &
DYYK�S \X�� ED�  EDYX�%  �ERX� �% DYYK�S \X�X &ED�&&EDYX�# XERX�X# DYYK�)S \X�ED�-EDYX� ERX� DYYK�/S \X�ED�%EDYX�5 ERX� 5DYYK�S \X�ED�EDYX�( ERX� (DYY++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++eB+�1u~�Ee#E`#Ee`#E`��vh��b  �~uEe#E �&`bch �&ae�u#eD�~#D �1�Ee#E �&`bch �&ae��#eD�1#D� �ETX��@eD�1@1E#aDY�?<XAEe#E`#Ee`#E`��vh��b  �X<Ee#E �&`bch �&ae�<#eD�X#D �?AEe#E �&`bch �&ae�A#eD�?#D� AETX�A@eD�?@?E#aDYEiSBKPX� BYC\X� BY�
CX`!YBp>�CX�;!~� � +Y�#B�#B�CX�-A-A�   +Y�#B�#B�CX�~;!��  +Y�#B�#B ++++++++ �CXK�5QK�!SZX�&&E�@aDYY+++++++++++++++++++sssssE�@aD EiDEiDssstssststst++++++++++++ sssssssssssssssssssssstttttttttttttttttttttuuustuuuu+s  K�*SK�6QZX�E�@`DY K�.SK�6QZX�E�@`D�		E���`DY+EiDt sss+EiD++C\X@
  �����t�2o�w w ��w�/12���w�"%2@�t�/52@�t�(*2@�t�!2����72����%2���@-2�%�-�7�%�-�7�����2����/� t+s++++++++t+stY ++C\X�����2�����2++Y+s++++ +++++++++++++++++++++++++st++++++++ss++++++s+s+++t+++sssss+ss+++s++ ++++sts+s++++u++++++++u+++++s++++stu++sss+++s+sstu++stu++stu++++++++++++tu +++EiD+ @BUT@?>=<;:987543210/.-,+*)('&%$#"! 
	 ,E#F` �&`�&#HH-,E#F#a �&a�&#HH-,E#F`� a �F`�&#HH-,E#F#a� ` �&a� a�&#HH-,E#F`�@a �f`�&#HH-,E#F#a�@` �&a�@a�&#HH-, < <-, E# ��D# �ZQX# ��D#Y ��QX# �MD#Y ��QX# �D#Y!!-,  EhD �` E�Fvh�E`D-,�
C#Ce
-, �
C#C-, �#p�>�#p�E:� -,E�#DE�#D-, E�%Ead�PQXED!!Y-,�Cc#b� #B�+-, E� C`D-,�C�Ce
-, i�@a� � �,���� b`+d#da\X�aY-,E�+�#D�z�-,E�+�#D-,�CX�E�+�#D�z��Ei �#D��� ��QX�+�#D�z�!�z�YY-,-,�%F`�F�@a�H-,KS \X��YX��Y-, �%E�#DE�#DEe#E �%`j �	#B#h�j`a ��� Ry!�@��� E �TX#!�?#YaD� �Ry�@ E �TX#!�?#YaD-,�C#C-,�C#C-,�C#C-,�C#Ce-,�C#Ce-,�C#Ce-,KRXED!!Y-, �%#I�@`� c � RX#�%8#�%e8 �c8!!!!!Y-,K�dQXEi�	C`�:!!!Y-,�%# �� �`#��-,�%# �� �a#��-,�%� ��-, �` < <-, �a < <-,�++�**-, �C�C-,>�**-,5-,v�6#p �6E � PX�aY:/-,!!d#d��@ b-,!��QXd#d��  b� @/+Y�`-,!��QXd#d��Ub� �/+Y�`-,d#d��@ b`#!-,�    �&�&�&�&Eh:�-,�    �&�&�&�&Ehe:�-,KS#KQZX E�`D!!Y-,KTX E�`D!!Y-,KS#KQZX8!!Y-,KTX8!!Y-,�CXY-,�CXY-,KT�C\ZX8!!Y-,�C\X�%�%d#dad�QX�%�% F�`H F�`HY
!!!!Y-,�C\X�%�%d#dad�QX�%�% F���`H F���`HY
!!!!Y-,KS#KQZX�:+!!Y-,KS#KQZX�;+!!Y-,KS#KQZ�C\ZX8!!Y-,�KT�&KTZ��
�C\ZX8!!Y-,F#F`��F# F�`�a���b# #�����pE` � PX�a�����F�Y�`h:-,� B�#�Q�@�SZX�   �TX�C`BY�$�QX�   @�TX�C`B�$�TX� C`B KKRX�C`BY�@  ��TX�C`BY�@  �c� �TX�C`BY�@  c� �TX�C`BY�&�QX�@  c� �TX�@C`BY�@  c� �TX��C`BY�(�QX�@  c� �TX�   C`BYYYYYYY-,�CTXKS#KQZX8!!Y!!!!Y-� � � &   ��  ��  ���i��� �i���             � � �(  ��  �1 I  �  � � �  T � $  U I+ ���v�� = � ������  � � �  � 7 N U U e �� Y��  �  ; R a � � �   � � �|��   � � < A A���� * ���	� � ��c�i  " �+���� & Y � �+�H ! k � �� k � � �]C�   I V n w � � �P���{��   ( a i �5M��>�� [ � ��[�[�?����  �
��2�������  & 1 = N V b � � � � �� H S w � &(�~~� . A ] k u � � � � � � � � � �Jb��d�����  # % * t � � � � � 0Pjo���������&�����N��   L z  � � � � � � � � �8h����	"Op���N��5Bk����a�������������    & F i � � � � � � � � �+8;Z^hs�������   ";DOor~�����������"6q�����&.1OZ�22GS����<dp�����*��� �h������  Y z � � � � � � � � � � � �!'+9FKMW\e����������"+ASae�����������#+1IZ[nqt~���������uz����Lmm������/j��6P���p*               ��     � +�S� ?�h�n    @�  t� 5�   � ����= �`�n�! �& ���B �<V� �� � k x �ks ��:}7 �S� <��	I� n �d ^                              9 � ���|+ � � Y � �� ���   U a  � � � (  ] � &l� �  7>z � � ��&B  ���i���7�-   � t h G � � � � � h G \ H 
 ( 2 A P Z d } � ��������y�o �  �,�� � � \ < � � � �� � G                                                      �d � �%2��v�����1 x � � � � �
 c � � �B  , 4 A 8 H X lY� C p � ( 7 B P Z d s x � � � � � � �\ � �,c � A K U _ s �	�� A d  * � �8t , @ � � � � � � � � �
 ,;DVc � W d6 P�  �� 9 N D� � $ B"� � ` �   9� ,�N�8i� �  � T  =q A  P � O 5�R , ��� � � �e��w�l � � \ @vDr��         B���?@ � 
� ��& 	� +�<�<N�<M�< ?<�<�<�<10!!%!!  � ��@ �  �   a��^�  �@N�	��� ��	���	%	(())uu	�)*%(��	��?OR � �  ����4 ����
4 �Z@-@4K_O@4�(@"-
�V � O0'�0���~S+N�]qM�N]�]M��� ?��+]q�+?��++]q�]10 ]]]]#   ! &&#"326?B�������z4�d2���v��Ƞv�[���Zn��^�Fr�������   R���>   �@H������	YVVY�����	���	���������u���t�
�t@9`p! XA+N�M�Nq�M� ?�?�10 q]]qCX@	iffi]Y ]]4632  #"$&%32654&#"R����4������ �nn��nn�"�������Ä���������   ~  �> ';� )��@]
?4444#DEED# /)S	`)�)�)������)�)�) )/)P)�)�)�))@4?)P)�)�)�)!�t�
!�t@'&'
 &@Z5`o�F@&@Z5o`�F�%&&'�)�  '����	?'���@6
?'@Z5'@A5'@<5'@$'4'@:=4/'�'�'''�' ' '0'�''(�<+N�]qr+++++++<M��<�]q+<�<�q]+<�< ?<?<<<<<?�?�9 910r+q] ]+!6326632!4'&#"!4&&#"!~��f�0F�\u�(��'Q;h.��?6Ah-��&��TUUT_\D��Y_�.<H���F�Z,F����  �  ��   w� 	��@?
?@	P	�	�	�	�	�		`		�	�	  @ � �  ] 
&���@	!$4?<+N�+<M�< ?<?<?<�]q<<<<<10q]r+!!�������J&��  0��> *�@�#'#���'�*	F���!�#��")Ue���"�A#@$D&g"d&���"�$	7&EFJOF!B""$'&75!5"5#5$
	!'"""#$"@,sxyv)u*��*��*�"�#����*�*�,!@!#4@4�3!P%�%%@4%,���@
?P,0,/,,!03! ����	? ����
? ���@		4 +x�+N�+++M��q�N]qr+�+qM��qr++� �CTX@5&"6!F!TYdi�
!"((_F(PF?�]?�]999]q� "�˳(*4!��˳(*4"���$4!���$4"���4!���@4k6"F"��"�"�"!" ����4 3����-?����	
>����"%4���@4 0@P`�� P`����4�@M _�F(@43@-?@	
>@574@+.4@%)4@4_oU@"$4P�F?�]q+�]++++++�+?�]q�+]qr++++�+9]q++++++Y10q] qqqq]]C\X� $��@	?(?!���99!���9"���9 ++++++Y q]%327654'&'$'&54632&&#"#"&0ncm7%I��[~����(��_Xo0 &�YX����/+RU(/ K>V�����1>B#fJK��Ұ  �  Y>  �@Zh�44DD��t@ 
& @ $4� �  ���@"$4��p��
&�)����@ $4��?<+N�qr+<M��<N]qr+�qr+<M�< ?<<<?<?�10 ]q]!!4&&#"!!632Y��$Q9It+����]�O�e8P���&��Ch�{  ����;�  8@ I  
�� �l+N�M�N�M� ?<?<�.+}�103k�����      ��  
A� ��@	794(794���@	(54@(54���@P!'4(!'4) **(
/8 7?j jefhg
�J	
			    	 
@>
���@4
%	��@  �a@ 0��$@		0	�		�$ a@	 ^c+N�]M��]q�]q�NEeD� ?<<<?<M�9/<�++<�.+�}ć.+�}�<<��ıCTX�	4	4 +Y10K�SK�QZX� ���
��� ���88888Yq]++++++!!!!!������y��;9*��M����� ��   U��?>  �@QXYYhii}y�����������88JJFYi:77ww�������	����4����43����4����4� 
t@ @4 @4 3�� t@ @4! /@4!O!XA+N�M�N�]M�+��+ ?��]�++?��++�++10 ]qq]&&#"3267#"  321��cOi}kPf+���������2ST����[o/��&%�   ���S&  �@Wg�	<<KK��t@ 

	& �)@@ $4�����@"$4��p��
&	���@ $4��?<+N�qr+<M�<N]qr+�qr+M�<�< ?<<<?<?�10 ]]!5#"&&5!32665!N:�ik�LR?Hr*�Ub^�����e;Ou����   ����  �@)   #
):JY  	
�@ ��`�����t� �t@	/
/  /_�@(&U?��`����  0x�+N�]qrK�7SK�;QZX� ��8Y<M�<�<�]<�� ?�?<�<�]q�9310]#327#"&&'&5#535%z�''Jb|Lz9	��&��T�+�*3QE1���Ӥ��  J���� ,�@=���(�,+ee(txt(��#Y
UU"Y#hfg!i(g,w��!#���4#���@e4Q"Q#�"�#q"q#�"�#�"�#+
*$"$#94#K
KD"C#je#yz"��"�
��"	
	"#
""#
V@ 4oo��e ��@9- H���@I 40@P`�����@9-*	��@4K'&.'��K�  0  -�S+N�]KSX� @8YM��]�N�M��+r� ?�q+�]+�?�q+�]r+�9]]qr++C\X� "��>#��г>#���9"���9#��ɲ9"���@9 9
 9
 9"���@9 9
9
9+++++++++++++Y�CTX@:
:5"5#K
IC"F#�
�"
 ]Y10 ]q]%32654&'&'&'&54663 &&#"#  J ����=L4��`����}}�I/,8��u�� ��������yQ4I.;Vy�p�f��qc5"94%/fm��~�k   I��.> # 2q@hJHI%��	6FW&fg&�&������')Yw�����4�$21,$@+.4$@"(4$@4o$�$$F���@04= ��,3 @4   U!@?!@?!@4!�t�
,����?,����?,����4,�t@@1&)	(Y��@4O44`  �03)!_�O_o3iA+N�]qrM��q�]N]�+]qrM����< ?�+++?<?�+++�]+�9/]q+�CTX�/qY��CTX� $���4T$d$]+Y]+++9<<<10q] ]q'6632!&'&'#"&546676754&#"3276765e�+�ϼ�K%��H�]��V���LPoKT^6�$7XDLE3�.��Y������L7FF��Z�K% QE;��2'<;V2&7$e  �  7>  �@(�	Sfu/Xhp
	��?O�w@) 

( 		0	p		�_�� &�)@��?� +N�q<M��<N]q�]M� ?<?<?�]qr9210] ]q K�SK�5QZX�
28Y ]!!!6632&#"���CkD`YWG=;R/&�kD5�.A���  �QR& 4�(���@44444���@:4  `��@/(  0`�����"&4���@49@4�'@	@4�'@9 @64  0  Ġ+N�]+M��]+�]+�NEeD�++qrM�� ?�]/?<<<99 9999<10 ++++++]K�SK�:QZX� ��� ��8888YC\X� ��@???���?���?+++++Y!!#"''3267+��#��C%CWPQNB5b^&����]b="�sY   �  ��   w@%��Gg�% % '�����	4��@0`p�   0  ���1S+N�]<M�<Mq�+qM� ?<?<�<9/<�<10 ]q]3! ##326654&'&#��R~�b�Nj����vC^H5��!ݯ��i����`.bAPh
  A��'>  �� ��@F9�	����
�	��HGF
O����
��
���@4@4������?����?��@P`����43 ���� 4 ����")4 ����+-4 ����4 ���@4�     _�t��t@$ !/!O/_o�!@4iA+N�+M�N]�]M��� ?�C\X@@(?@?@?@?++++Y?�C\X� ���(?����?����?����?++++Y�]q+++++C\X�  ���9 ����9 ����	
> ����A!?+ +++Y�+9]C\X@@?@?@?@? ++++Y/<�++r++<310]q ]+# '&5 32 !326&&#"�6���i���@�aBZ'xV\<<R/�����+����}�HlzCCs     Z& @(/4(/4(/4(/4��س/4���@ :4�
	
" -� ���@ 4
  % *4 :� 	�CTX�
���@	4 	 
 ??<9+99@ 

		 
	9���@(40@
?
O

�0@9?O�0 ��@5  @Ġ+N�]+M�]��]NEeD�]+M� ?<?<<<999Y10q+] ]++++++!!6767!��T'�:�!�Z&��E--��   �  b�    , �@?w*hx*��	!	(,!%O0�#"% % 'p�K('�����	4��@!0.@.P.`.p.�.�.�. .0.."   0���-1S+N�]<M�<M]q�+qM��]� ?<�<?<�<9/]qC\X� ���9����9����9+++Y<�<9 910K�SK�QZX�
 8Y] ]!2!3276654&'&#!276654&&#�J���Zo_��]�vJ���(­*LWKJ,Ѫ�+BS@y��\�_g�+'�d�q���	WGDU	���x	]NB\*   �  ��  S� ��@)
?@P�����`��  
& ���@	!$4 ?<+N�+<M�< ?<?<10q]r+3!���F  F�30   ' .@�XgU[fg wuv u-��� �-&&&75-FG-Uvtv-
.!'.-'& (!
" ) ().-
  '&!"wP�V  ���4 ����4 �(����4(����4(�� I�	w�!@(@4@4/?O�
!@4!@4/!?!O!!��Z�
	��"@-��_o?�+@4���/��@w+/++@4+���P0$���@	4$ $$��@���w���@	4 ��@�/@4/�M��+N�+q]M�q+�]q�q+N�qM�+q��qq+9qrrr/<�]< ?<��]++�]++�]�?���++�++�]�99 99999999<<<<<<<<<<10 q]]]%&&546753&'#5&&'%6654&'�ķϬ����a��Ñ��X6;F@A�K^OZ��8㢤�cc��!v*�yAϢ������Pt `:5[�2oKCa   V���    �@Kx
�
���	��	�	VYYVghhg996	6IIE	F�	���	����	� ���@%4�/@4� �O"�!��+N�M�N�qM� ?�+q?�+q10] ]]2#" 76"32676&&2�x��w�����w�3P4O33P4O����_�`��I�����ATm�����@ATl�A  �  �  $@8 
&    0  gv+N�]M� ?M�103!���   ,  ��  r@#/	00P	p	�	�	% 	�-@
 0   �-@Pp����+N�]KQX�@8Y<M�]<�<�]<EeD� ?<?<�<<<10]!!5!!��M��N����>  3  � ?@_��������CCCV����  (7HCCC$$$&V������  1v������@4     0 @  ����4 ����V@#/@4�	�O  �w��+N�M��N�q<<M� ?�+q�?<�+]q<93+]C\X� ���9����9���@9999++++++Y�CTX@	  99]Y10]KQX� �� �� ��888Yq]]]!6767654&#"%6$32�'��+:eYXh�����GM3��G���	۱?WU^ej{���c�bA�P&   W  �  �� ��@14
:8
HV����
! //?O@4�� ���X�/�`@O ��+N�<�q<M�]� ?<?<��+]q<9]10]+!!7W�w��������u�J��0x�  W��*�  # �@;ju�����������6Dz���� �   ���@4�!/!!@4!�?	@	�	�		�O���!@"/@4�� w�O%�$��+N�M�N�qM��� ?�+q�]�]q�+q?�+q9 9]10] ]&&#"632 #"  3232654&#"��
TCY{i���������*����~QNhpTQpSTP��|������Y��d��鉕z���  S���  $ 0�04&���@l4����uv�& *6 ;F Lncghw'�'�������'�,�0��w���'��  .�+	�  %.@4?.O..�� ��@4p��(���@	40(@((��@?"O""@4"��@�	w+�O2�w%�1��+N�M���N�qM��� ?�+]?�]+9/]q+�]+9]9] 9]9]10q] q]++&&54632#"'&54632654&#"32654&#"Hmc����j`z���ȅ�v�_OP`_NQ`wYWrtYge.�`��֤f�*1�{��i|�w�QT^_TO_`�=t�}vg}�   T��a�   �@-YY
YVVY��	�		p�:4:4JDJD�		�t��t@  
)&�)@ �!X<+N�M�Nq�<M��<� ?<?<?�?�10 ]q]CX@ii
iffi]Y!!5#" 32!32654&#"a��A�Z����²��/Dza��gd��[Y'��p�Ln����� ���Q��   �@M& 6�� 	 @ � �  ] _�	&�O3�k !j�<++N�]M�N]q�]<M�< ?�]?<?<�]q<93<<<<10q]!#"&'732665�5�u*a81#+7������˧^�%4��   �  ��  o� ���244����#%4���@?4 @P��`p�� �  � � � �   0 � �  n1�+N�]qr<M�< ?<?<10]qr+++3!�(��F  s���  2@!0@7   0D   0  �l+N�]M�] /�]10!s(���   Y����   �@U����'x	wwx����������-	-'�
 

 

��@ 0@`p�� �'�   0  ���~�+N�]qM�M]q�]qM� ?�?�10]]q ]4766763   !  32654&#"YC2�g��D��~�����~1汱�ݷ�����p�+:�n�����o�h��������   T�Q`> # /N@bw�p1��1 ##033@CC[YY%V)V+Y/k��;3;(3,KDK(D,��
�*'-$����43 ����> ����> ����(*4 ����#%4 ����144 ���@	4`  _�t�'�t�
-�t@*)&�)@	�11��@
 3$!0X<+N�M���Nq�<M��� ?<?�?�?��r++++++�CTX�  ���4 ����	4++Y�+9 9999<10 q]]qCX@iii%g)f+i/]Y ]32767655#"'&5 325!# &5432654&#"yA(Vn7%~��}b�ŀ>p�������`g��he�F'8!1#^��������G��j<����������  �  � @&&���@	:4
 :;4	���:;4	���@�.4
 .4	
�	�
	

	
#, 	/
ghe	j
wx�	�
�	�
�	�
��	�
�	�
���	�
���	�
w	x
���	�
�Xejg	h
vyDKD	K
WW	X

/4:4	;
?		
	�CTX@
	22  P4P4���@4@'4@'4���@'4 
  ?<<?<9++++++]/���9��;@-
	 		2

2

		���8 ���[]4���@ST42@�� �8@  @[]4 @ST4 2��1u+�q�++<�<�q�q<�++�<�q ?<<<?<9�.+�}ć.+�}�+Y10K�SX� �� 88Y]]]]]]qr++++ +q]3!!!!��
�������������F��~��~  �  #� 	�@	�� �?����[]4���@*ST42		@[]4@ST42���@@P`p��� 0	����[]4	���@SS4	2  0 �  ���
1u+N�]<M�++<M]]qr�]<M�++< ?<?<99 99�.++++�}ıCTX� ��@	'4 '4����	4@	4 ++++Y10CX� ���5�5���@=.4S.42@F�������� /4;O���������@	354@354���@/24 /245���@	!.4T!.4���@F 4T 4,';3N@\V	ME�������'(Jx��]qrr+++++++++ ]]qr++++Y ]3!!!� X������-��F��D   �  a�   @3((
Gee*9HYh96���% %'�����	4��@�! !0!!   0��� 1S+N�]<M�<M]q�+qM� ?<�<?<�<10 ]q]!2#!327>54&&'&#��`��`-7fM�b���(�|7H_<<lS>��&���ε��cK*��5VŪ��f   �  ��  �@=%0�	%
	% KH
  0@	   0  ���1S+N�]<M�<N]�]<M�<�< ?<�<?<�<9/]qC\X� ���9����9����9+++Y<�<<<103!!!!!�?���� 3������q�  �  ��  =@P%    0  ���1�+N�]<M�<N�< ?<M�<?<10]3!!�(���I�   �  ��  ! �@�9IWjj�	��#��	


6FF	66Guy�
x	xv�	��		Su��� %`�  !% ��@' �'�����p# #0##!   0  ���"1c+N�]<M�<]q�]��]� ?<<<?<�<9/]q<�<99�.+]}�9 910 ]q]]3!2!.##326654&'&##�o�Հ��`}j����rT^f<��j<OH$���Oʂ��8����?�Y!��N$XBJ[   �����   �� ��@197GVV
VVY�5;;5EKKE��	
 �t��t@ 
!p)&�)@p �  ?A+N�q<M��<�Nq�M� ?<?�?�?<10 q]]CX@ff
ffi]Y ]+3!632 #"&'32654&#"��������[�@4Iy]��ge������������[Y�*�Op�����   #����  Z@$i�T	f	iiiz�
H�-	   ��@p0�

�u+N�]M�Mqq�<M�< ?<?���10 ]]!#"&'%3265�' +��� 0bcR��`�b���� ~4Oq�  �  _�  � �ݳ?���@}-4'	f�
�
�	�
�

S`	FWv�	����NNf}������
++***/KK
	
	

	  


�m@/9e&�   ?{+N�]q<M�<�q���<< ?<<<?<?<9�}�<�CTX� �Ȳ	!4 +Y10]]]q r]++3!!!�IZ�����������v�|�^݉��  U �V�  H@	b0@7b? O  b
��@bO��MC+N�]M�<�<� /]��]�<<10%!!!!!���� ���}}������     �� �@++ 3 @:4����:4����:4����5	���@	4
4���@	4 4���@Y4 4		
 	) %	�
��	�
���
�� �	�
�� �		���
����
��	."/
 ���
��CTX�����!4���@	!4@!4����4���@4d4 	  ?<?<<9++++++99�� ��0�
	 ��2@\      
2

	 		2 
	

		 /�0@
 ��@/�0@  0^c+N�]M�]���]NEeD� ?<<<?<<<<<99999999 9�M.+�}ć.+�}ć.+�}ć.+�}�+++Y10]]]]q++++++ ++++q]!!!!!e��/�`�*������������  �FH��  �  Y�  �@+933BB��	$Xh�t@	


  
&	@ $4�	�		���@"$4��p�� &���@ $4��?<+N�qr+<M�<N]qr+�qr+<M�< ?<?<<<?�999<<10] ]632!4&&#"!���a�O�� Q=Fn3�����Hp����1�Z5D�����   &  D� 
  �@9 9	+Sk��%(H[���	 
 ��@
 @���(  ��   �X��

�@��?�LH +N�q�]M�]<�< ??�<�]<999 99�.+}��CTX@-=M�� ]Y10]] ]+!!533#~��|춶����'���^�����  k�Qh�  F@(�	 	 �" 	 "  �@
	�� 0����k+�]����� ??<<10]#&5673e���cV���g=5#�Q���!����W����f   C�Q@�  I@''
gg
���	  �"   	"  �������jC+������ ??<<10]>543ESD:f����BK��Q����u��/���������   A���  # �@X;Kez������ ����� ��4VY_R`w���h /@4�! !!���@4!�0	O	�	�		�O���!� ���@4��O%� w�$��+N�M���N�qM� ?�+q�]�]q�+q?�+q9 910q] q]%3267#"54 32  #"&4&#"326]
TEWzj���	������^}RNgpTQoSSP��{�����u�n�����{����  u���  ?�	
�@�8

r&$    0  gv+N�]M��� ?M���9 9910!'667#�*uZ7UH��z�p tbU   M��� ) �@2��{�����������!
 !
�$@O@��@/@4��V� ���@24�'���������O$$+�w� *��+N�M���N�qM��]�9/] ?�+q�?�+q�9/]q�99 999]10q]] ]%32654&#"7654&#"%>32 #"$MrQWwrR6KrxXIHf��m�y�}g�~��������!hn�pj|�iWJXd`,��[�l��s������  �  &� 	 V@	k{��)�_�^�	 	 �X  ]@  �
��� +N�]<M�<�< ?<?<�]�910 ]!!56$73&���n0�#�E�$Ɇ   ���$�  �@8		GG	W	V��������� %	 ���@"@P`p� 0��   0����1u+N�]<M�<M]qr�]<M�< ?�?<<<10]q!32665!#"&&'&5�(�|~�(0�خ��~���8Zmg��+����ږYa�U~�   ��l�>   �@.8H4994DIID�	VV
YVVY�� �t��t@!p)&�)@p �  ?A+N�qM�<�<�Nq�M� ?<?�?�?<10] ]CX@ff
iffi]Y ]!6632  #"&'!32654&#"�3�j����X�O���fb��cg�&�Pd��������FU����������  �  �� 	 r@?% 0��/� %	 ?OR  0	   0  ���
1S+N�]<M�<N]�]<M�]< ?<?<�<9/]q<�<<<103!!!!���;d���������     ��  �@26*  Y��  	_��t@
��t@  �  
	3?OP(/_�@&_ ������	4x�i +N�+q<M�<�<�]<�]� ?<?]q<�]q<?�]q9210q] ]3546632&#"3#!#�9�uxs&C>=5����&P��S$�9QK���I          l  �  �  J  �  2  	  	r  
�  (    0  �  �  �     �  �  0  �    �  �  �  �  !*  !�  #  $�  %�  &�  '  'V  (^  *:  ,�  .�  /v  04  0�  0�  1�  2�  3�  4�  56  7x  8x  9�  :  :�  ;�  <\  =�  >6  ?  @  @�  A�
endstream
endobj
10 0 obj
<<
/Encoding /Identity-H 
/ToUnicode 20 0 R  
/Name /F-1 
/DescendantFonts [21 0 R ] 
/Subtype /Type0 
/Type /Font 
/BaseFont /SUBSET+ArialBoldMT 
>>
endobj
24 0 obj
<<
/Length 513 
/Filter /FlateDecode 
>>
stream
x�]����0��<����*x�q	!��HڭJ� !14RI������Us ��x���L��o�m3����U�0�S��C�v��
��MkfVL�Tc���.eof����u�}{��l�4ُi�:w󴮻c�b���CӞ�ӯ�a�í���KhG37������k�+/�dq���<�g��F���^��׾��P��0-?���Y�gef�����fO��r�;��6��%��D�X��s_����v��q�T)x̉��7u�-J�|CpJ���-|=3[�z�Z�*�,|��_�D���BAߜk�i]��)|}Z��<g_O__]ᛧ���ܳ�W�J�ܕЗ��yB�7��s�߂��i��F_a��.-_e�.�WX}��K��qT��r+}Y#����
_��Q��髼�,��7���7e�o�cW��4
_a��B}�o
�o��P�g~VJ_��}N_�6}������>�Nu��#�F�ͣ�4m�l�}��y�� �*#
endstream
endobj
25 0 obj
<<
/DW 500 
/FontDescriptor 26 0 R  
/CIDSystemInfo <<
/Registry (Adobe) /Ordering (UCS) /Supplement 0 >>
 
/W [0 [0 833 556 333 500 666 722 556 556 500 556 222 277 666 500 666 556 833 556 556 556 943 277 666 556 666 222 556 556 277 722 556 556 556 556 610 556 277 500 500 277 277 722 556 722 277 610 556 556 556 333 666 277 777 666 722 500 556 889 556 777 777 500 500 222 333 333]] 
/Name /F-0 
/BaseFont /SUBSET+ArialMT 
/Subtype /CIDFontType2 
/Type /Font 
/CIDToGIDMap /Identity 
>>
endobj
26 0 obj
<<
/MissingWidth 1000 
/ItalicAngle 0 
/CapHeight 715 
/Ascent 905 
/Descent -211 
/FontBBox [-664 -324 2000 1039] 
/StemV 0 
/Flags 32 
/FontName /SUBSET+ArialMT 
/FontFile2 27 0 R  
/Type /FontDescriptor 
>>
endobj
27 0 obj
<<
/Length 44832 
/Length1 44832 
>>
stream
    	 0  `loca1    �  fpgm�A H  V  �maxp�        head�     �   6cvt �Q     nprepB 6  $  /glyf�>   x  ��hheaE     �   $hmtx@!    �        ��_<�     ��'*    ք�����g Q   	         >�N C ���z                 C  � �s J� �  !V �� fs Ds �  ?s �� �9 $V��  PV \s K� �s Us Ss M� 9  V �s UV 	� �s �s F9 �� �s �s <s Us � 0s �9   (  9 �9 �� �s �� �9 �� �s �s Vs a� AV �9  9 cV �   s B ws I9 m9 X  �  7���� |� |    C� < �    @ �  �  �T�A,,,"  +* < *��(�&м) �) )�+�'�;@�#�2A-   /      o  �  �   _    � � � �       o � � � A'    � �   / O _ � �   _ o  � �  @��3@���3@��jl2@��a3@��\]2@��WY2@��MQ2@��DI2@��:3@��142@��.B2@��',2@��%2���
2�A �  p �   � �    @�$&2��  d ���2A
��  �� d ����2�AJ� �� �� ���� �  � ?� �� �� �� �� ������ � /� ?� _� �� �� �� �� �   �  � ?� �� � �� � ����Ӳ792���Ӳ+/2���Ӳ%2���Ӳ2���Ӳ2�Ҳ�)�&�;@�" > 3"�%1��<i�� +�A0� ��   � �  � P� `� p�  `� p� �� �� �� ��   � �  �  �  � 0� @� P� в +�ϲ&BA��  ��  ��  ��  ��  �Ʋ A�  � � � /� ��$�A�  � /� ?� O� _� �� �"�dA� �  � �  � � @j@&CI2@ CI2@&:=2@ :=2� �&@&��2@ ��2@&��2@ ��2@&��2@ ��2@&z�2@ z�2@&lv2@ lv2@&dj2@ dj2@&Z_2@ Z_2@&OT2@ OT2���$'7Ok Aw 0w @w Pw www �  ��**��@+)*�����R���e�~���<�^�+���@��8  �@��@��8  �9@�����s�&�%�$� 7@�!�I3@�!�E3@�!�AB2@�!�=>2A! ?! !  �! �! �!  @!� "2@�!�2@�"�*?2@�!�.:2oAJ� � �� ��  /� `� ��  � ?� _� �� �� ��  �"  �"  " /" ?" _" " �"  �! �!  o! ! �!  ! /! ?! O! ��""!!@+H�O�7    ����� 	A	��  ��  ������&�A�  9 &% 8 s 5  4 � 2�V��&,� ��������� ���������/���&��� ���8�ʸ��&���~&���}Gk��e&���^s�@R&ZH�Db@s��?^<&���5��0�+��*V)��#��5UU7�h@,�XO62,!
 ���@+                     J �KKSBK��c Kb ��S#�
QZ�#B�K KTB�8+K��R�7+K�P[X��Y�8+��� TX������CX� ��� (��YY v??>9FD>9FD>9FD>9FD>9F`D>9F`D+++++++++++++++++++++++B��KSX�5��BY�2KSX�5��BYK��S \X���ED���EDYX�>�ERX��>DYYK�VS \X�  �ED� &�EDYX�  ERX�  DYYK��S \X� %�ED� $�EDYX�		 %ERX� %		DYYK�S \X�s$ED�$$EDYX�  sERX� s DYYK�S \X��%ED�%%EDYX�� �ERX� ��DYYK�>S \X�ED�EDYX� ERX� DYYK�VS \X�ED�/EDYX�� ERX� �DYYK�S \X�ED�EDYX�� ERX� �DYY+++++++++++++++++++++++++++++++++++++++++eB++�;Yc\Ee#E`#Ee`#E`��vh��b  �cYEe#E �&`bch �&ae�Y#eD�c#D �;\Ee#E �&`bch �&ae�\#eD�;#D� \ETX�\@eD�;@;E#aDY�GP47Ee#E`#Ee`#E`��vh��b  �4PEe#E �&`bch �&ae�P#eD�4#D �G7Ee#E �&`bch �&ae�7#eD�G#D� 7ETX�7@eD�G@GE#aDY KSBKPX� BYC\X� BY�
CX`!YBp>�CX�;!~� � +Y�#B�#B�CX�-A-A�   +Y�#B�#B�CX�~;!��  +Y�#B�#B +tusu EiDEiDEiDsssstustu++++tu+++++sssssssssssssssssssssssss+++E�@aDst  K�*SK�?QZX�E�@`DY K�:SK�?QZX�E���`DY K�.SK�:QZX�E�@`DY K�.SK�<QZX�		E���`DY++++++++++++++++++u+++++++C\X� ���@t sY�KT�KTZ�C\ZX� �"  sY +ts+s++++++++ssss+++++ ++++++ EiDsEiDsEiDstuEiDsEiDEiDEiDstEiDEiDs+++++s+ +s+tu++++++++++++++stus+stustu+++t+ +++ EiD+\XA6/ A 0/ - -/ 2 2/@&7	7
DD++++++++Y+   @[�tsrqponmlkjihgfeb]XWVUTONA@?>=<;:987543210/.-,+*)('&%$#"! 
	 ,E#F` �&`�&#HH-,E#F#a �&a�&#HH-,E#F`� a �F`�&#HH-,E#F#a� ` �&a� a�&#HH-,E#F`�@a �f`�&#HH-,E#F#a�@` �&a�@a�&#HH-, < <-, E# ��D# �ZQX# ��D#Y ��QX# �MD#Y ��QX# �D#Y!!-,  EhD �` E�Fvh�E`D-,�
C#Ce
-, �
C#C-, �#p�>�#p�E:� -,E�#DE�#D-, E�%Ead�PQXED!!Y-,�Cc#b� #B�+-, E� C`D-,�C�Ce
-, i�@a� � �,���� b`+d#da\X�aY-,E�+�#D�z�-,E�+�#D-,�CX�E�+�#D�z��Ei �#D��� ��QX�+�#D�z�!�z�YY-,-,�%F`�F�@a�H-,KS \X��YX��Y-, �%E�#DE�#DEe#E �%`j �	#B#h�j`a ��� Ry!�@��� E �TX#!�?#YaD� �Ry�@ E �TX#!�?#YaD-,�C#C-,�C#C-,�C#C-,�C#Ce-,�C#Ce-,�C#Ce-,KRXED!!Y-, �%#I�@`� c � RX#�%8#�%e8 �c8!!!!!Y-,K�dQXEi�	C`�:!!!Y-,�%# �� �`#��-,�%# �� �a#��-,�%� ��-, �` < <-, �a < <-,�++�**-, �C�C-,>�**-,5-,v�##p �#E � PX�aY:/-,!!d#d��@ b-,!��QXd#d��  b� @/+Y�`-,!��QXd#d��Ub� �/+Y�`-,d#d��@ b`#!-,�    �&�&�&�&Eh:�-,�    �&�&�&�&Ehe:�-,KS#KQZX E�`D!!Y-,KTX E�`D!!Y-,KS#KQZX8!!Y-,KTX8!!Y-,�CXY-,�CXY-,KT�C\ZX8!!Y-,�C\X�%�%d#dad�QX�%�% F�`H F�`HY
!!!!Y-,�C\X�%�%d#dad�QX�%�% F���`H F���`HY
!!!!Y-,KS#KQZX�:+!!Y-,KS#KQZX�;+!!Y-,KS#KQZ�C\ZX8!!Y-,�KT�&KTZ��
�C\ZX8!!Y-,KRX�%�%I�%�%Ia � TX! C� UX�%�%���8���8Y�@TX C� TX�%���8Y C� TX�%�%���8���8�%���8YYYY!!!!-,F#F`��F# F�`�a���b# #���pE` � PX�a�����F�Y�`h:-,# � P��d� %TX�@�%TX�7C�Y�O+Y#�b+#!#XeY-,�: !T`C-,� B�#�Q�@�SZX�   �TX�C`BY�$�QX�   @�TX�C`B�$�TX� C`B KKRX�C`BY�@  ��TX�C`BY�@  �c� �TX�C`BY�@  c� �TX�C`BY�&�QX�@  c� �TX�@C`BY�@  c� �TX��C`BY�(�QX�@  c� �TX�   C`BYYYYYYY� CTX@
7@:@;@>?�CTX�7@:�  ; �>?��CRX�7@:���;@�  CRX�7@:�� ;@�� CRX�7@:� �;@�7@:�  ; YYY�@  ��U�@  c� �UZX�> ?�> ?YYYBBBBB-,�CTXKS#KQZX8!!Y!!!!Y-,�W+X�KS�&KQZX
8
!!Y!!!!Y-, �CT�#�_#x!� C�V#y!�C#�  \X!!!� GY�� � �#� cVX� cVX!!!�,Y!Y��b \X!!!� Y#��b \X!!!� Y��a���#!-, �CT�#�{#x!� C�r#y!� C��  \X!!!�cY�� � �#� cVX� cVX�&�[�&�&�&!!!!�6 #Y!Y�&#��b \X�\�Z#!#!�Y���b \X!!#!�Y�&�a���#!-,-,�%c� `f�%�  b`#b-,#J�N+-,#J�N+-,#�J#Ed�%d�%ad�5CRX! dY�N+#� PXeY-,#�J#Ed�%d�%ad�5CRX! dY�N+#� PXeY-, �%J�N+�;-, �%J�N+�;-,�%�%��g+�;-,�%�%��h+�;-,�%F�%F`�%.�%�%�& � PX!�j�lY+�%F�%F`a��b � #:# #:-,�%G�%G`�%G��ca�%�%Ic#�%J��c Xb!Y�&F`�F�F`� ca-,�&�%�%�&�n+ � #:# #:-,# �TX!�%�N+��P `Y `` �QX!! �QX! fa�@#a� %P�%�%PZX �%a�SX!� Y!Y�TX fae#!!!� YYY�N+-,�%�%J� SX� ��#��Y�%F fa �&�&I�&�&�p+#ae� ` fa� ae-,�%F � � PX!�N+E#!Yae�%;-,�& � b � c�#a �]`+�%�� 9�X� ]  &cV`+#!  F �N+#a#! � I�N+Y;-,� ]  	%cV`+�%�%�&�m+�]%`+�%�%�%�%�o+� ]  &cV`+ � RX�P+�%�%�%�%�%�q+�8� R�%�RZX�%�%I�%�%I` �@RX!� RX �TX�%�%�%�%I�8�%�%�%�%I�8YYYYY!!!!!-,�%�PX�@  c� �T\�KR[�Y-  � � � &   ��  ��  ���i��� �i���   �   �     � �i � � ��  � � � �  D � | � �  Z � � R R  D ��� / �  � �  W ~ � ��  �� � �  " A P o �L�u \ �� 7 L n p��X������ � ����   c c ������ - \ � � ��	� @ W � �� r �]�g��  ! w �  M ��+ L e �|C�������   ] h � �5G!\�M��  - x � � � � � � � ������  , I  � ������?     ) 9 I o � � �#�o2@z��  1 U W � � ��~~�F�B  � � � � � �/OV)o�r  , 1 1 d i � � � �+��������  & � � � s���C_�����a  ^ m � � �8Q[h|������ATk�hq�BBSs�����X�������2�� Q | � � � � � � � � � � � !U{{~������������  !""#rw�������"+5<Yoq�������22������� ����*��� ����������      < Q a a j x � � � �*>LQ_jqx����������� !".5BOO^eq�����*G]ety���������
"&+G_u���\��
m���6>PQ]���` � � � �            ��E� �3�� - _ dM?  ��}�$x;;N �&����;MKS j1      �   <� ��e�� x~� � 9  �0+� ��� �
��P�>X !� �q} �E  
��+N� � T2�� N � 7� � k� � w � �dg � 3| � ��)n*�i�� �  9$ �]��� u �
 �����M�Rh m } � q�� yX�g V %� � |2! �  r \ / �  � � AM r   LjU � � � � �  x i  W n � �T� ge �  ��R Z�� ��g n�� -�� ��| � � � � ���{ p  � �LF�F�-��S� �              % � � �   >� �� S ?����  ( " � b J � m � � H� 3�N��Fp y� Q���
 h�l O � � a+ ��� � { eR�te�i � � \ @ � u � �q�� � � � � � � � � � �           B����@ � 
� ��1 	�. +�<�<N�<M�< ?<�<�<�<10!!%!!  � ��@ �  �   �  � P��+X�*�@�V*�@ V�CTX� ��@UU���U���@(UU	 	 	
UU����U ���U ����U ����U /+++�/+++� ??�����9++10+++ �CTX@ U U U U U���@#UUUU	U
U����U���@U& 
4 
4  
���U
���U
�V  V@ U U ����U /+++�/�++ ?<?<<9++]10++++++++ +++++@ v��	II)%,X[vx�96OKD@MB
������00RR@	
 	`��� 1� �1�	

�@�V

�@@	V
 @�V � �� A
��  @ V  ��  @�V  p�V� `����;Y+�]�]<�++<���]<�++<���] ??<<<<<<<<��.+�}ć.+�}�10 K�SK�QZX� �� �� ��888YK�SK�(QZ�C�@PZX� ���
88YC\X� �Զ!9,!9��Զ79279��Ե-9,-9++++++Yrq] q]]YY ++@  ?3?3?3??01Y3!67!##�$[05_��V��X���HP���F��5��   J��> ( 7"��+X@,		**)**967:*I*]]*ji*`0��)���(���U'���@U��(��(��(��(D���@UUU5���@OU+,*499,IH,VY+fi+v����+74/$42!_)o))/?���������  @�VU���U���@UUU&�@�V�@�V���,�@@V,

BU� ���@U E'
2)aa A��  @ V  ��  @ V  ��  @@V U %!$���U$���@U$U$���U$����U$���@U$U$����U$�[@'@ && &0&�&9����U&��ִU&���  @�V&19���@#409�9�99����U�@@	V%"/�@�V/�@�V/�@@V/$��?�@�V�@�V�@@.VUUUUUUU18�++++++++++]q�+++��++]q+�+++]��++++++++<�++++�� ?�?�+?��++�9/++++++++]q�q999910 ]++++q]++ q� ++)�-�l'
2�-�l�/�l ?+2/3?+?9/+93901Y%#"&546676767654'&#"'>32#&326765<d�j��GsH5k�g3E�y�nЉ��P	"�b�o\2mih�&�UF��N�N$%
n-=Yqq�K@aJ.x���=8�((M/H`[O=w   �  �> ��+X@;/#4CSft				  
	(�" "�@�V�@�V�@�V% ���@364�     � �  ����U ���@U U U ����U ���@U U U NG�+�++++++++]q+<�+++�]�r� ???�999999 ɇ}�10 ]r]� 
	�6�l ?+22??01Y336632&#"��>i?[^>BB;^&�qH:�'G?`r��   !�Q�& Ű�+X��@�V�@�V�@�V�@�V�@ V ��  @�V�@�V�@�V�@�V�@�V�@�V�@�V�@ V ��  @�V�@ V�CTX@
@ @ U/+���� ???�910����@s9(V�
@@ (04 (04	'''665�((HYYYiiiyvyzz������
�����
�����BU�CTX@D� ???�9]99@7
 %

%

 /��?�@@�T@?@_��B�" E
�T@ @@ 0OP��B�/�?� |f+�q�]q�����]q���]q ?�?<<<�.+}ć.+}� 9�<<�K�SK�QZ�C�@PZX� �� ��88YY+10C\X� �޶79
"79���9"9++++Y]q++ q]+]Y++++++++++++++ +��3@
l

 ???3?+01Y'326767673673#";,<H&�m��+"+��lA$0|V4�g�($k(��u�|vk�ȯBYS   �  R� T��+X@"79	:'
56
G
W��v
��
���@U(����
5�	���@	!4 !4��޳9	���!4���!4���!4����4���@C9	%%=	=*BU	
	
 

	 

  
 �:@0����J�:@0 ������@�V�@�V
�@@V     U ����U ����U ����U ����U ���@
U ];�+�++++++]�+++�]q��]q�<<<< ?<<<?<<<9/�.+}ć.+}�<<K�SK�QZ�C�@PZX� ��8Y�CTX� ��4���@444	4
4 ++++++Y+10+++++++C\X@	"9,9,9"9��޶9"9���@9"9@9��޵%9@9+++++++++++Y +++qr]+ q]++@	

   ????9/39301Y33!!������� �����)��������  f��v� /��+X�cj���U ���@_U  2c p t� �� ������� ��*(* GVWVhk{��������  ��޲(9���@ (9 	&J & �@�V�@�V
�@@
V& �@@VUc\+N�++]M�+++N�]M��� ?�?�910++]]q ]++r@
  �2�l	�2�l ?+?+9/39/301Y#"$54$32&&#"326��=�����כ�C��,;�3��\m憣�1���n��U���-�����銼   D��'>  ���+X�U���U���@eUU
GHVYgi4::5EKKE\\	R]]Rmm	dmmdw	[TT
[lee
l
A��  @ V ��  @ V ��  @@V$@U@U���@UUU���U���U���U���U���@$%40  ���  @�V1����@#40�@�V�@�V�@@AV$ U U U U U U U U @$%4 ?  �@�V �@�V �@�V 147+�+++]+++++++++�+++q+]�+]]++++++++++�+++ ?�?�10q] qC\X@	SS	bb	]Y ++++��/�l�/�l ?+?+01Y7632 #" 32654&#"D����{�������������'�v������������  �  �> 氅+X@���������@"4y���� 
A��  @ V ��  @ V ��  @@V$@U@U(UU���@UU"U���@UU���@U
U���@U@364��N���@464��p���3�@�V�@�V�@�V% ����U ����U ���@U U 
U U ���@U U U ���@364�     � �  N�]q++++++++++<�+++<�<]q+�]q+++++++++++++�+++<< ?<??�9910Cy@	


&
 +++*�]q +]q@	

�0�l ?+2???01Y33632#4&&#"��u�`�P
�*kHs�&��EpM2}�s�nmA����  ?���> 0��+X��@�V�@�VA7@ V (��  @ V '��  @ V &��  @ V %��  @ V $��  @ V #��  @ V "��  @ V !��  @ V  ��  @@|V"":	J	D$V"e"|	�	�$��,�	0K,�U2
\\	\
\\\jj	j
jjj�&�''&$'$)6$Z
Yd&d(t#t$�$�
��(�,�0�
��'�(�&�&(����U"����U#����U$����U(����U"����U#����U$����U���@9Z'%
 &.��@",U?O_��o���U   � ��@U@� ����4���@4.\l����U���U���@U.$@42���@2UUUU U UUUA	@ V [ ��  @�V$*����9�**���U*���U*���U*���U*���  @�V*2���@!'*4`2�2?2�22$ U U  ����U ����U ����U �@@V $UU U���@UUU�@@V"� ? O  147+N�]qM�+++++++�++++++�rN]q+�+++++q+M�+�++++++++++�r ?�+++?�q9/++]qr+��]qr+�99910Cy@@'-#,&"  	(-  !# "#)
('	
+  ++<<+<<+++++*+��� +++++++++]q]rq] ++++++++++++@
 &&.�/�l.�/�l ?+2/3?+939/301Y732654'&'.54676632&&#"#"&?��{|x5%�ƙOA8*�S}�Z�si|j/���Vi�}��=kreD=#%2I�NGy(+H{gR\R7#
$3A|\Z�W�  ����& ���+X� ��@	4 4���@4+$ 
 3A��  @ V ��  @ V ��  @@V%@364@U(UU���@UU���@UU���@UU���@U��N���@464��p����@�V�@�V�@�V%	���@364�	 	 	�	�		����U	���@U	U	
U	���@U	U	U	NGP+�+++++++]q+�+++]q+�]q+++++++++++<�+++� ?�??<99910Cy@   ++**� ]+++� 
�0�l
 ???+2?01Y!5#"&&'&53326653?|�^�O�nQQ�;���HmO5s����1GQS��9��  �  7� ���+X�
�@�V
A@ V ��  @ V  ��  @�V�@�VA@ V ��  @ V  ��  @�V�@�VA@ V ��  @ V  ��  @�V6U����784����454����014����"%4���@%4��O��p��  
% ����784 ���@354� � �     � �  ����U ���@U U 
U U U ����U ����U ���@
U NGP+�+++++++++]qr++<�< ??10]qr++++++++++++++++++� 
  ??01Y33����F   $��*� n��+XA  ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V 
���#&4	���@$#&4� 
 	+
" "�@�V�@�V
�@@"V%�E	E`p��  �������U����U���U����U����U����U���@UU���U�j 6�f+�+++++++++]q���<�+++<��< ?�?<�<9933�10]+++++++��2�l �2@	l

	�-�l
 ?+322/?+?+01Y%#"&&5#5373#32L<bl,�����+(��>e�c�l�����M,  ��  Y�  ���+XA ��  @ V 
��  @ V 	��  @ V ��  @ V ��  @�V�@�V�@�V�@ V ��  @�V�@ V ��  @�V�@ V ��  @�V
�@�V�@�V �@�V�@�V

�@�V
�@�V	�@�V
�@�V�@�VU���U����U���@YU	UU/0gh	`������YVPh����	
		  ���@U  ���@U 	�p@	 �@� @  eRP����@P����@�����+�]q�]q�]q���� ?<�?�<�<�.++}ć.++}�9999����ć����10K�SK�QZ�C�@PZX����  ��8888Yrq]++++++++++++++++++++++++++++��1@l   ?3??9/+01Y#3#!!&'3�Xݫ�����F"3��F��DZ��w��  P���> a��+X� ��  @�V
�@�V	�@�V�@�V�@�V�@ V�CTX@4@ P p  UUUU/++++��� ?�?��]2�]210@G	CCSS``�����
jijup���	�
���"_o��@&0 @ P ` p � � � � 	   A
��  @ V ��  @@V$U"  A
��  @ V  ��  @@V $+ @+�@�V@�@�V@�@�V6�@@ V@U@UHUUI�@�V�@�V�@@!V$�?U
UU�@�V�@�V14�+�+++++]q�+++�++++++++]rKS#KQZX� ��8Y�++r�+�++r ?�?�9/9/]�]�10 ]q]qY++++++@
  �/�l�/�l ?+?+9/39/301Y#" 4632&&#"326<�����r鉭��Z����j����
����kl���  \���� 0A��+XA '��  @ V &��  @ V %��  @�V�@�V�@�VA@ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @�V�@�V�@�V�@@(Vccst%'59CILED$F'SY\W(�#���U$���U%���U&���U'���U#����U$����U%����U&����U'���@FU(&$$'%64#D%E/Z V#U%ljkfeyzz}u$s%������$�%����CTX@-!&&	&)&  )21& e  -y�%-'%%���@U-	 ?�?�+9]99]9]9/�/�/�/�@-%$!%$"-@U�� -���@U P`p���@- BU���@BU-	&J	A��  @ V 	��  @ V 	��  @�V	& ))���U)���@U)2!�@�V!�@�V!�@�V!&&���U����U���@UT   1c[+N�]M�+++��+++N�++]M�+++�� ?�+?�+�]+��]+�99999Y10 ]q++++++++++]q+++++++++++ +++�--�3�l-�3�l ?+?+99//01Y7326654&'&$'&&546632&&#"#"$&\�_�}o�SP\;�lQig~��������98�X�z�������n�WBsDEg#a+7�eo�dí���[O33k(;�vu�st�   K��>  ��+X@ U]]	Ueko	e���U���@RUU'���1:1AMAQ\Ramaxx�� P`p��
 �� ���U���@U�A��  @ V ��  @ V ��  @�V@��ܴU���U���U���@	'*4�����%&4����#40���  @�V3�@�V�@�V�@@V$@$*4?O�@�V�@@+V UUUUUU47+N�++++++++]+M�+++�+Nq++�q++++M�+++ ?��]++�?�9/]<�q<99910] ]+++qr@  P p � � 0 p � � � �   �/@l 0
�/�l
�/�l
 ?+?+9_^]/+3/]q01Y#"  32 !326!&'&#"^�,��������
��c���Q8V�|�V��(���� ��h��Ch�   �  &> #o��+XA� ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @ V ���U����U	���@M4%��	�� ��  #	 	##
�%�%�%%%�UU���@UU���@UUUU����U����U�]��@�V�@�V�@@V%�U���@UU���@UU
U���@UU����U�]� 3#�@�V#�@�V#�@@V#%� � �  ? O  ���@U U U U U ����U ���@U 
U U $%�x�!GP++N�+++++++++]qr<M�+++��+++++++++]�+++�++++++++++]�NEeD�qr ?<<<??<M��99910Cy@& +++�] ]+++++++++++++++++++++++++++@


 
�0�l	�0�l ?+22?+????01Y336632632#4&&#"#4&#"��2�jv�~ʞ��#\>p��XdL�:&�N_bX����'�l_:�����xxP����   U���  *Z��+X�CTX� %����U����U���@(UUU,+(O P���@U" ?�?��+]29/]�299/++/+++�����10�CTX� %���U���@*UU,+(O P" ?�?��]29/]�299/+/++�����10@G:L@#[W#flmg#z}������� � =��:)d(O_"�P  �h�A'��  @ V ��  @ V ��  @ V 9 ��  @ V ��  @ V ��  @ V 8@@!#40 �,�8� �%�@�V%�@�V%�@�V%s���@!#4 @�+ǋ+�]+�+++���]q+�+++�+++ ?��]�?�9/]�10�C�@PX� '�� #��!  8888Y ]q]YY�(�/�l�/�l"�/�l ?+?+9/+29/01Y732>54'#"54 32#"&4&#"326p�|aS}P66�m��Ə�{z��˥tx��|}�SznL�pVk�������������4��Ĝ���   S���  # 0ư�+X�CTX� .���@U..!(	U	����U	+���U���U���U���U���U���@U$UUU/+++�/+++�/+++�/++� ?�?�9/+�9910�CTX�	U	����U	+���U���U���U���@"U$UU ..!( ?�?�9/�99/++�/++�/++�/++�10@M5)II&��0	0} }|tqruz� ���������  .�..!(A��  @ V ��  @ V ��  @�Vs�		Ag +��  @ V +��  @ V +��  @@V+s@ #40 ���2�@�V�@�V�@�Vs��g�$�@�V$�@�V$�@�V$s���@!#4 @�1ǋ+�]+�+++�]�+++�]q+�+++�]�+++ ?�?�9]/�999910�C�@PX� "�� ���  /���- &���) 88888888Y]rq qYY� .�/�l(�/�l!�/�l ?+?+9/+9901Y&&54632 #" 54632654&#"32654&#"jpl���km���������b�kh��fg�:I�S�����)�j��ߠf�),Ĉ�� ���Th��_c����M�O�����   M���  *鰅+X�CTX@_(@"
 %���@UUUU/+++�/+���� ?�?�9/]��]10@-kD@DD ZT kddjd tu���� U'���U#���@U! U(@P�_  �h@	"�8� �%A��  @ V %��  @ V %��  @@V%s@!#40 ���U�,
�8��@�V�@�V�@ V 9@?_o�@�V�@@VUU�$�+ǋ+�++++]�+++��+]q+�+++�� ?�?��]�9/]�10�C�@PX� ��' # !���8888Y++++] ]Y�
(�/�l"�/�l�/�l ?+?+9/+29/01Y&'&#"6632#" 763232654&#"��,IkVAUbA�g��wЄ��䝉���7O�Nr��{z�Sj0M0>��c`��Ҋ�~K|������]�Y�����    v� ���+X� ��  @�VA@ V ��  @ V ��  @�VA@ V ��  @ V ��  @�V�@�V
�@�V�@�V�@�V�@�VA@ V ��  @ V ��  @ V ��  @ V ��  @ V ��  @@3V) &)&9 696I GIGX WXW��BUBU�CTX@3+44DDKTT[ddktt{   ?????9]99@
	��<�  ��<� ��<@Z	     		 	 		 A	Q   Q Q @ Q�  ����+N�]M����NEeD� ?<<<?<<<<<999999999�M.+�}ć.+�}ć.+�}ć.+�}�+++��ć<ć�ć�ć�ć��K�SK�QZ�C�@PZX�
���88YK�%SK�*QZ�C�@PZX�  ��8Y K�SK�QZ�C�@PZX�@@88YY++10r] ++++++++++++++++++@  ?3???3?301Y!3673673#&'��{��$8
��O#-���n���'����?���$�������F]� eG��   ��9�  d��+X� �޲9���@ 9���v     
� ����  �z+<��� ?<?<�.+]}�10]++� 	 ??01Y3���X��  �  ��  .��+X@ekKK[[  A��  @ V ��  @ V ��  @�V&���  @@V
UU���@U  �@�V�@�V
�@@V     U ����U ����U ���@U U ����U ���@
U ];\+�+++++++]<�+++<Nq]�++++M�+++ ??<�<9/<�<10] ]��3�l �3�l ?+?9/+01Y3!2!!!2654&'&#!�)�Ml�Y�����{��]L1����e�m������\�   U��!� ��+X��@�V�@�V�@�V�@�V�@�V�@ V�CTX� ��@U
��@ ���U���U/++�/�/ ?�?�9/���+10@4UUKy������	*
���@
@�@����@  �@_o��A��  @ V ��  @ V ��  @@Vs@!#40 ����U� �5 � 8���8  ��@!#4  @  �����+�]+������+]q+�+++�]< ?��]�?�9/]9/]��.+}� 910�C�@PX�	00��� ��8888Yq]++Y++++++@  
�/�l�/�l�3�l ?+?+9/+9/339/01Y732654&#"'!!632 #"&U��l����W�(�����O���t�������Ģ��O?��v\���Ǒ��  	  F� 
C��+X�,�@�V�@�VA@ V ��  @ V ��  @ V  ��  @ V ��  @ V ��  @�V�@�VA@ V 	��  @ V ��  @�V
�@ V  ��  @�V$�@�V$�@�V
�@ V  ��  @�V$�@�V$�@ V�CTX@  
 	/����33 ???910@$/* (%
/0`��	��� P�CTX�	  ??99@$
		   	� 
 	ee���@(9P���@@(9_���@ P0`������`�+�]q�]q+�]q+�� ?<�?<�.+}ć.+}�K�SK�QZ�C�@PZX� 
���	������888888YK�(SK�6QZX�  ��8YY10]q] ]Y+++++++++++++++++ +++�  ???301Y!3673A���}."-������׀pxx)�F  �  <�  
��+X�
�@�V
�@�V
�@�V
A@ V ��  @ V  ��  @ V ��  @ V ��  @�V�@�V�@�V�@�VA@ V ��  @ V  ��  @ V ��  @ V ��  @�V�@�V�@�V�@�VA@ V ��  @ V  ��  @ V ��  @ V ��  @@7V	6UO	�	�	�	�	�	�	 		p	�	�	�	�	�	�	�	
	 	���  @@*V~ 
% �������  ������U���@UU
UU���U����U���@
UNGP+�++++++++]qr<�< ??<?�+999910]rq+++++++++++++++++++++++++�
 @  ?�??01Y533��������&��  ����  ��+X@{$5E?�"3Bp�:<<LL]]X]^jlhnn���������� //0?@LPf��� 
A��  @ V ��  @ V ��  @@"V$�@`�@UUU����U���U����U���U���@Ut�@�V�@�V3 �@�V �@@V U U 3�@�V�@@V%�����?O����U���@UUUUU����U���@UUUG7+N�++++++++++]qr<M�++�++++�++�++++++++]q�+++ ?�??�?9910 ]]qr q�
�/�l�/�l  ??+9?+2?01Y!#3632 #"'32654&#"-��r�b�q@��k4U�v��uv�����O��s���֝��U������  F����  ��+X@|
%4D55WT
RSgde	c`�����������+<<Kp�.$.:5KEFIW
Vg����  
A
��  @ V ��  @�V3 ���  @�V %A��  @ V ��  @ V ��  @@$V%�@`�@U@UU���@UUU���@UU���U����U���  @�Vt�@�V�@�V�@�V$�@�V�@@;V����?OUUUUUU4P+N�++++++]q++M�+++�+++++++++++]q<�+++�+<�++ ?�?<?�?<9910 ]q] q��/@
l 
�/�l  ??+?39?+01Y!5#"&&54632332654&#"8e��ujԃ`�/�� �uv��{x��������QA�F�������   �  �&   N��+X@  	<<
</ ?    ���+�]q� ??��999910� @ /�?�01Y5353����Y������  ���"� ;��+X@
&XX����@44;FJv�� ���	A��  @ V ��  @ V ��  @�V&���U���@UU���@U]  P`p��@�V�@�V
�@�V& 

���@
4
 U
����U
����U
���@U
U
����U
���@
U
];Y+N�++++++++]�+++M]]q�++++M�+++ ?�?<10]+ ]��3�l	  ???+01Y3#"$53326`�d������p�G�}ֶ���������O����b�   �  �� ɰ�+X� ���4���@U%5E����@4 
A��  @ V ��  @ V ��  @@'V%	@364�	�	@U@U	(U	U	���@U	U	U	���@U	U	���@U	
U	����U	N���@464��p����@�V�@�V�@�V% ���@364�     � �  ����U ���@U U U U ���@U U U NGP+�++++++++]q+<�+++<]q+�++++++++++++]q+�+++ ?<?�?99910Cy@% +++� +]++�
 
�0�l  ??+9??01Y33632#4&#"��~�v�K�ukP�<���]���_��{S�}��  <  � '��+X�CTX@	U����U���@	U���@UUUU��@
  9/��9/� /�++++?�+++�210�CTX@	U���@	U���@UU���
���U���@U  9/��9/++� /�++?�++�210@G;;�����IYTkdzz�������
����O�� ���
A��  @ V 
��  @ V 
��  @@V
s�  @!#4��   8@�?_o�$ ���+�]���+<��+++ ?<�<?��]�99�.+}�910�C�@PX@	��� �� �� 	�� 88888888Y ]]rYY@	�3�l�/�l ?+?+939/01Y%!&76676654&#"'6632�7%��神{�������H�¢\��A<c�~��fk������X����a1  U���  ���+X�CTX@
	���U	���@U	 U U U /+++�/++� ?�?�10�CTX@
	����U	���U	���@U	 U U U /+++�/+++� ?�?�10@N����	ELJCT\\Rkkclk`ywvz��������A��  @ V ��  @ V ��  @@Vs	@!#40	 			A
��  @ V 	��  @�V	��@�V�@�V�@�Vs ���@!#4  @  �@�V �@�V �@�V �ǋ+�+++]+�+++�++]q+�+++ ?�?�10]q ]�C�@PX� ��� ��� �� �� �� 88888888YYY��/�l�/�l ?+?+01Y632#"'&326&#"UkӠv�tBjӡ�y���||��~|J]�=�_�������í�������hj�i�    � 
 ��+X� ��  @�V�@�V�@�V�@�V	�@�V
�@�V�@�V�@�V	�@�V
�@�V�@�V�@�V�@�V�@�V�@�V�@�V�@�V�@�V	�@�V
�@@7VXh���LL� 
 � ��  �@
   �
�f�
@4
���U
���U
���U
�7@@"#4�!5����@4  ���U���U�����+�++]+�++�++++<��< ??�<�<9999�.+}�10C\X� �޲9���@39"-9<++++Y] ]C\X@@9�P9@&9"9@-9+++++Y+++++++++++++++++++ +�	�2�l  ??9/+332901Y!!533#������ƴ�5_���J�����k  0  �� ��+X��@�V�@�V�@�VA@ V ��  @ V  ��  @�V�@�VA@ V ��  @ V  ��  @@V 	�s� �� /��   ���@U U ���U ���U ����U ����U �s���+�++++++]<�]<��]�<< ??<�<10++++++++++� �3�l ?+2?01Y!!5!!�������   ��i!>  հ�+X@t-=K? �  )#22Bp � ::JJY[\\jkimk� ������� � #++5:FJZ��� A��  @ V ��  @ V ��  @@V$�

@
`
�
 @U @U
���@U
U
����U
���U
����U
���@U
t33�@�V�@�V�@@V%  �����?O���@UUUUU����U���@UUUG7+N�+++++++++]qr<M�+++���++++++++]q�+++ ??�??�9910 ]]qr q� �/�l�-�l ?+2??+9?01Y36632#"&'32654&#"��:�h��ju�{Z�.�vx��ts��i��QQ�������L:����������    �� ^��+X@	/0@p���(�����@4
+ 
���@�V@�@�V�@�V�@@V% � ����184 ���@+4� @U@U U (U "U ,U ���@U U ���U ���U ����U ��� ! �
 ++�+++++++++++]++<�<<�+++�+�] ??<<<�<?�9910Cy@		 ++*��+q] r� 
�-�l
�2�l
 ?+?+32?01Y3#535476632&#"3#����vL\82RD����qk4FW�
F`b��f   (  �& +X��@ V ��  @@V��24���@	4>!4���@J!4)(	/99
IFFI	O\TTZ	Plccj	{t{	���	��&)+	9������4,9	���@#9:	


%a+
a ���@	U+
���[   ��@U"� @`�����@$Ut 
~� O o �  U t!|�++N�+]q<M��+]q<�+�<<� ?�+<�?<��99�.+�}��+10+++q] ++++C\X�)&���@	424��·!4>!4 ++++qY]C\X� �޲9	��޲9	���9	=	���9	���@
999++++++++Y ++�
 �0�l 
�/�l ?+3?+2201Y35#!5!63!(�sX�Od��oyj��w�^{	�    �& 
c��+X� ��  @�VA@ V  ��  @ V ��  @�VA@ V  ��  @ V ��  @�V�@ V�CTX@ 

 	$U/+����33 ???910�5 "9
���@9	44���4���4
���@	!4 (!4
���@	"%4 "%4
���@~(.4  (.4) (	&
9 5
H G
VVYX	ffii	x wwyx	w
������	� �	�
� �
� ��
� �
� �
� �
� �
,
 
 
( &
7
O @
	@4@4�CTX@	  
���@U
 U 	���@UU9/�+��+��+�+ /??910@7
%	
		
 %  

 
	
	 /"@@@	�		��@��@	 @"��+���]�]��]9999 ?<<<?<9�.+�}ć.+�}�Y10 ++q]++++++++++++ ]Y++++++++� 
 ???301Y!3673��l��%+��n&��goTv���  �  �� P��+X��@�V�@�V�@�VA@ V ��  @ V  ��  @�V�@�VA@ V ��  @ V  ��  @�V ����8=4����344����-04����()4����#%4����4����4���@*4 ��   � � � / @ P � �   � � ���@U U ���U ���U ���@U  U ��Y+�++++++]C\X�� ]Yqr<�]++++++++< ??10++++++++++�  ??01Y33����F  �  � �  7��+X@< 
<_ o  � �  ���+�]]� ?�10�@  ?�01Y353����   �  Z�  N��+X@ C A��  @ V ��  @ V ��  @@V& 	@U	 U	
U	U	���@U	�@�V
�@�V�@@V     U ����U ����U ����U ����U ���@
U ];\+�++++++]<�+++<�+++++]�+++ ?<�<?<�<10Cy@6


!!!
! ++++****�]� �3�l �3�l ?+?+01Y3!2#%!2676654&'&#!���Z~YtsNz�ͅ��9��1EM�lN����Lb��ħ���a2�61E���*   �  �� 
��+X�
�@�V �@�V
�@�V �@�V
�@�V �@@!V@4k���	 	�
 ���@
!#40    ���U ���@U U U ���@U U U @4���@!#40 @�<� +N�]q++�+++++++]q+<M�< ??9910] ]+++++++@	@		 ??9/�901Y!#56673��A�T��/t{>|�G�_  �  � 	��+X��@ V ��  @�V���@
4U���U���@#BUBU 		A��  @ V ��  @ V ��  @�V ���U���@UU���@U]  P`p�	�@�V	
�@�V	  ���@4    U ����U ����U ���@U U ����U ���@
U ]
;Y+�+++++++]+<�++<]q�++++<�+++< ?<?<9999�.+�}ıCTX� ��4 4 ++Y++10+++C\X�@F9����F9@29����29"9��޶9"29��޶29"#9���@#999����99����99����9+++++++++++++ ++++Y ++@   ????9901Y333#����������F���  ���� � 
 d��+X�
 ��P@&<
< 
< 8:O _ o  �  ���+�]���<< ?�<<���910�@  ?�/�01Y353'667��PW296��q�&Ma[  �  �� 	 Ӱ�+X@"�  �  	�@�V	�@�V	
�@@V	     U ����U ����U ���@U U ����U ���@
U ]
;\+N�+++++++]<M�+++<N�]M� ??<�<9/]<�<10��3�l �3�l ?+?9/+01Y3!!!!������P���:��f  �  *�  ���+X@  ����@�V�@�V
�@@V     U ����U ����U ����U ����U ���@
U ];\+�++++++]<�+++<�] ?<�<?10� �3�l  ??+01Y33!������   V��� +���+X�CTX@@U ���@+U)#


)))#  U &���U&/+�/+�/�/�/ 9??��9/���9�+2�+210@0E�EWvRljduy����
#���@  � ) 5��� h@	)A��  @ V ��  @ V ��  @@Vs_ o  U �A��  @ V ��  @ V ��  @@Vs&@!#40& &&&����U&�-�8���8  ��@!#4  @  �,����+�]+����+]q+�+++�+]�+++ ?�?���9/��]�9910�C�@PX� ���88Y] ]qY@	 #
�/�l)�/�l)�/�l ?+2/3?+9/+3299/301Y732654&#"732654&#"'6632 #"&V��k��}3Ls��ji��!�x�kfd������������|��x}c��� ��g�d_�.������   a  �  ���+X@�	 ��@0	s@!#4O_os	� O__?_o����+N�]q<M��N�q+<M� ??<�<99910q]�	 �3�l ?+3?01Y5! #67a����K6�����������ۭ�ǜ  A�jm  =��+X@ppMM# p  p�+N�]� /M�10 q]� @ /�01Y5!A)���  �  ��   *ް�+X� ��@)UF#V#f#s	�	iup	s��'	'*	A��  @ V 	��  @ V 	��  @@V		**))  A��  @ V ��  @ V ��  @@
V&U���@%UUUUUUT%A��  @ V %��  @ V %��  @@V%&U
U���@U,�@�V�@�V
�@@V     U ����U ����U ����U ����U ���@
U ]+;\+�++++++]<�+++<N�+++M�+++�+++++++�+++ ?<�<?<�<9/<�<9/+++99910] ]+�	*�3�l �3�l �3�l ?+?+9/+901Y3!2#!276654&&#!!27>54&&#!�&��sfg��W�����=�8JKF����m^&CZ:T�����Y�e^�3'��g�`1RfMIo)��8kFRy1  c����  T��+X@K��� @OO@XX	WU_Z_VW��	A��  @ V ��  @ V ��  @�V& ���  @ V ��U���U���U���U����U���@U��@�V�@�V
�@@
V&   �@�V �@@V U U c\+N�++++]M�+++N]�+++++++]M�+++ ?�?�10]q ]]]q��2�l	�2�l ?+?+01Y !2#"$7 32 4&#" c�6�F������������y�����m����������Z�����4����    F� `��+X��@�VA@ V ��  @ V  ��  @�V�@�VA@ V ��  @ V  ��  @�VA@ V ��  @ V ��  @ V 	��  @�V�@�V�@�VA@ V ��  @ V  ��  @�V	:;	���4���@444	��س!4���@;!4(!4&)*
/hhh�			
U	 


	���@U  �@	

	 �@		R@
�

��@  RO���@	 U ���@U U ���U ���!`�++�++++<�]��<�]�� ??<<<�<99�.++}��.++}ć�ć��K�SK�QZ�C�@PZX�	��� ��8888Y10 ]]C\X@		"9"9��ޱ9+++Y++++++++++++++++++++++++++��2@
l 	 ???9/+301Y!3673;���!PEB^���mM�F||s������     �& �  ��  @�V�@ V ��  @�V�@�V�@�V�@�VA@ V ��  @ V  ��  @�V�@�VA@ V 	��  @ V ��  @�VA@ V ��  @ V ��  @�V�@ V ��  @�V�@�V�@�VA@ V 	��  @ V ��  @�VA@ V ��  @ V ��  @�VA@ V 
��  @ V ��  @�V"A@ V 
��  @ V ��  @�V �@�V"A@ V 
��  @ V ��  @ V�CTX� ��@UU U
��ԴU���@U U
����U���@/U@U
 
 
U

U����U/++�����+� ?????910 +++++++++@*)
J[� U
���U���U���@	!4'4	���@�$4		 	 $ %*+4 5:;DG@MKCGJ[Rkdgyzt�����	(( ('('/8 7w�������� �����	�����	UUUUU�CTX@
 %%%  %���@7U%*U
&
+TR
\l|�

 
 
 ?????9]99/+�/+�9���999@	


��K�  ��I@f
 � +
%+


 %   

 
�`p���@
 O
o


�U@	Oo�U@`p������f+N�M�]]�]q�]q�]]� ?<<<?<<<<<999999999�M.+�}ć.+�}ć.+�}ć.+�}�+++��<<�ć�K�S�C�@PZX�  ��� �� �д 0 ���88888888YK�4S�C�@PZX� �б088YK�!SK�3QZ�C�@PZX� �� 88YK�SK�QZ�C�@PZX� �ж   ��в0��� 8��� ��8888888888YK�SK�QZ�C�@PZX� ��
   888YY10C\X� �Զ9 ,9 ��Ա9+++Y+++++]qr+++ +++q]]Y ++++++++++++++++++++++++++++++++++++!367373#'K����?3���5=������)�&����n����f��|���     �& +��+X� ��  @�V�@ V 	��  @�V�@ V�CTX@	
 
U/+ ????910�"9���@P9Z��������	@9	5:��/WYYX��
��������	���
�CTX@ U���@U  

 ?<?<99++99@f			 	

� �	% 	  	�%
		 
OI~"
a	~@
��@P��C@ ~"O  I|�+�]���]������] ?<<<?<<<�.+]�}ć.+]}� 99�ć�ć���<<<Y10C\X�9���@9"9"9��޲!9���@
9"!9	@9++++++++Y]q +]++]Y++++@ 
 
	 ????9901Y336773#'����.,%�������:��(��G0B3����JY�]   B�Q�>  *)��+X@`,%LE	,&,#96JFVXh�
�.#,'>#>'L'�,�,6!6)?,FF!E)T!T)ic!c)`,�,�'�!�#�'���(��@  0 ` p � � �  �}@
E"
3%3
A��  @ V 
��  @ V 
��  @@$V
%�@`�,@U,@UU���@UUU���@UU���U����UA
��  @ V ��  @@Vt% "�@�V�@�V�@@V$����?O�@�V�@@.V UU"UUUU+,t!4P++N�++++++++]qM�+++���++++++++++++]q<�+++��< ?��?��]�?��?<10]q ]q@
    �/�l
"�/�l
(�/�l ?+2??+9?+9/_^]01Y32676'#"5463253#"&32654&#"f�2Ct}�v���nэ�z�e۠�Ꙧ}|��zx�XQ%2dZ7��<ݘ����j��x�*�������   w����    ' 38��+X@
��h��@1+�� 	e �@%(�� e .��%�� +  1��"�5��   �@	   u4WZ+�]������� ?���<<?<<���9999�.+}�10Cy@R3)+ 3 1-&+ /$1 
 *(2!(,'. 0#.    ++++++++++++++++�]�(�e�%	�e@.% ?3??33/�2�201Y4632#"&"32654&34632#"&"32654&w��������9CYZBDYZB"���垗������:DYZBEYZZ��ſ����t��st��s�s	�����ſ����t��tt��s   I�-A * 1 82��+X@%|0,66/F!U!P/]6jc/zw!s/{6�!�/�61��޷9  $4,���@, #4j8*7 *0! 710! 7!00�770!72���P��� ���+�5@
� *�7�
2�5�)��8 ��5s&���@
90&@&�&&�R@*  8822))*��@ ++11

0 @ � �  �@	.so�� 8@?O�9ǋ+N�]M��q��]<<<<<<�<<<<<<<�]+��� ?��<�<?<�<�����]�9�.+�}�10Cy@J!7$%#%"%&7!5O3(5O,.O 0.O 6%8O! 784'2O 32-+O,+/1O 01 <<+<<+<+<<+++++*+*��++ +]]@ 81@+  )2�/�l)
�/@	l�/�l+�/�l ?+33/+2/3/?+2/3?+3/9/�3201Y5.'7&'&&5476753&&'6654&'���{
�5LjotV]�[�j�\v�eX�,Tj9�jiyg{ji�a�ӴW"�D`=A0�l�wPVVMb�jq��"%j�U��	�(�]\|%��sbw/   m���� %���+X@`'^$$ !% ���@U!	&'%$A��  @ V $��  @ V $��  @@V$   '`���U���U��ڴU���@Ur�''�@�V�@�V
�@@
V& 

�@@V
U
&c[+N�++]M�+++M]�++++]<M�+++<9/ ?�?�9/+<�<999910Cy@D#&%&&%&#%! ! ! "%!!!	!! $!!  ++++++<<+++++++++*�] ]�@$$! �3�l!�2�l	�2�l ?+2/3?+9/+9/�01Y5%#"$54$32.#"3267Lm��Р�����P۟�&�!b�o��w!8��~�>?���rs�^��s�g��0p�MQ�O������a7  X����  (��+X@�_&�&7##*-+&;<:&LLI&]U#X&o{z��� �� �� �� ��+ *;]��&�&%*&49&IIEE#K&VXUZZVW W"ifk&{&��&��&��Բ9 ���@09*:((& !(& $$	A��  @ V ��  @ V ��  @@
V&U���U���U���U����U���@UJ *�**!�@�V!�@�V!
�@@
V!& �@@VUU)c\+N�+++]M�+++N]�M�++++++�+++ ?�??�9999 3��]10++]] rq]]qr@  &&$($@$�2�l	�2�l ?+?+3/�9/�939301Y%&'#"$54$32%64&#"  327&'��r9���������E��F�n��m�y�����h\[e�]+�9{[�\��d����ڵ�ߍ/]�9�
���������';   �  �� ��+X�A@ V 	��  @ V ��  @ V ��  @�V�@�V�@�V�@@VUVZ	��	U����U
����U	����U���@UUw
 !4���'4	���'4���!4	���@�'47	G%-
X
wu
���#&%98	?OYYXY	}y�	�������

		

	%%


	  
�@	U"�@ ?U��@�V�@�V�@�V% �@�V�@�V�@@V%� ? O  ���@1U U U 
U U U U �!Gf++N�+++++++]q<M�+++�+++Nq�+]M��+� ?<<<?<?<9�.+}ć.+}�<<<<�CTX@K		�	4 +]qY10C\X@
	,9	<��޲9��Բ 9��Ա!9+++++Y] q]q ++C\X� ���!9����9��޲9��޲9��޲9��ޱ9++++++Y+++C\X@�9	<	<����9���9+++++]Y ]+++++]q++++++ ++@
	 
 
  ????901Y333#�����j���������v�dz�[  7��a� ��+X@egtu��	����U��		A��  @ V 	��  @ V 	��  @�V	&

A��  @ V ��  @ V ��  @�V&���U���U����U���U���@U]  @P`& ���U ���U ���@
U K�Y+�+++�]q�+++++�+++<�+++ ?��+?10 ]� 	�3�l		 ??+9/301Y7326653#"&;�pcIj(�Y������|Cs~����j�  ���Q:�  ���+X��@�V�@�V�@�V�@�V�@�V�@�V�@�V�@�V�@�V�@�V�@�V�@�V�@@%V%;3� ���  @@#V~ �%

�?O���@7UUUUUUUU�!GP++N�++++++++]q<M�<NEeD�q ?M�??�+99999933�<10Cy@&
	  +++�]+++++++++++++��0@	l @  ?�??+01Y53732653#"���h"676�3A�I����{�I�\���Md  |�Q`�  N��+X@
' �3� ��3@�^  ���+�]����� ?<?<10]�  ??01Y&47673ߕ�MZ��y'=#++�Q�������Y������    |�Q`�  v��+X@((	
 	�3�
��3� �^���U����U���U���@

U���+�]++++����� ?<?<10]�	 ??01Y# 4'&'&'3��++"='z��ZM��Q�Ἱ��Z��������          l    �  	  4  �  V  �  �  �  �  (  �  !�  $h  (>  *�  .�  1x  4�  7B  :�  ;  <�  ?  A�  C�  F   H�  I  J�  L�  O   Q�  S�  U  WL  X�  [  ]�  _  _d  a  bP  d~  e  f  f�  iB  j  j^  l�  l�  n~  q  wT  y�  |r  ~L  �0  �T  ��  �,  ��  �L  ��  ��
endstream
endobj
11 0 obj
<<
/Encoding /Identity-H 
/ToUnicode 24 0 R  
/Name /F-0 
/DescendantFonts [25 0 R ] 
/Subtype /Type0 
/Type /Font 
/BaseFont /SUBSET+ArialMT 
>>
endobj
28 0 obj
<<
/ModDate (D:20250109194522) 
/CreationDate (D:20250109194522) 
/Producer (Ibex PDF Creator 4.7.3.0/7447 [.NET 3.5]/R) 
>>
endobj
xref
0 29
0000000000 65535 f 
0000009120 00000 n 
0000008203 00000 n 
0000011961 00000 n 
0000009254 00000 n 
0000009289 00000 n 
0000007603 00000 n 
0000008120 00000 n 
0000008285 00000 n 
0000000020 00000 n 
0000039084 00000 n 
0000085470 00000 n 
0000011982 00000 n 
0000007860 00000 n 
0000008628 00000 n 
0000002116 00000 n 
0000008263 00000 n 
0000009082 00000 n 
0000008971 00000 n 
0000009023 00000 n 
0000012097 00000 n 
0000012652 00000 n 
0000013127 00000 n 
0000013357 00000 n 
0000039250 00000 n 
0000039838 00000 n 
0000040341 00000 n 
0000040567 00000 n 
0000085632 00000 n 
trailer
<<
/Size 29 
/Info 28 0 R  
/Root 1 0 R 
>>
startxref
85773
%%EOF
```

## .env

```
REFLEX_UPLOADED_FILES_DIR=/home/charlie_ubu/proyectos/app12/uploaded_files
DB_URL=mysql+pymysql://tum12607_reflex:9ujT.uD9G}*L@181.214.83.154/tum12607_app12_reflex
APP_ENV=development
API_URL=http://localhost:8000
```

## .gitignore

```
*.db
*.py[cod]
assets/external/
__pycache__/
.web
uploaded_files
logica.txt
.env
*.pyc
alembic.ini
.venv
README.md
.gitignore
```

## alembic.ini

```ini
# A generic, single database configuration.

[alembic]
# path to migration scripts
# Use forward slashes (/) also on windows to provide an os agnostic path
script_location = alembic

# template used to generate migration file names; The default value is %%(rev)s_%%(slug)s
# Uncomment the line below if you want the files to be prepended with date and time
# see https://alembic.sqlalchemy.org/en/latest/tutorial.html#editing-the-ini-file
# for all available tokens
# file_template = %%(year)d_%%(month).2d_%%(day).2d_%%(hour).2d%%(minute).2d-%%(rev)s_%%(slug)s

# sys.path path, will be prepended to sys.path if present.
# defaults to the current working directory.
prepend_sys_path = .

# timezone to use when rendering the date within the migration file
# as well as the filename.
# If specified, requires the python>=3.9 or backports.zoneinfo library.
# Any required deps can installed by adding `alembic[tz]` to the pip requirements
# string value is passed to ZoneInfo()
# leave blank for localtime
# timezone =

# max length of characters to apply to the "slug" field
# truncate_slug_length = 40

# set to 'true' to run the environment during
# the 'revision' command, regardless of autogenerate
# revision_environment = false

# set to 'true' to allow .pyc and .pyo files without
# a source .py file to be detected as revisions in the
# versions/ directory
# sourceless = false

# version location specification; This defaults
# to alembic/versions.  When using multiple version
# directories, initial revisions must be specified with --version-path.
# The path separator used here should be the separator specified by "version_path_separator" below.
# version_locations = %(here)s/bar:%(here)s/bat:alembic/versions

# version path separator; As mentioned above, this is the character used to split
# version_locations. The default within new alembic.ini files is "os", which uses os.pathsep.
# If this key is omitted entirely, it falls back to the legacy behavior of splitting on spaces and/or commas.
# Valid values for version_path_separator are:
#
# version_path_separator = :
# version_path_separator = ;
# version_path_separator = space
# version_path_separator = newline
version_path_separator = os  # Use os.pathsep. Default configuration used for new projects.

# set to 'true' to search source files recursively
# in each "version_locations" directory
# new in Alembic version 1.10
# recursive_version_locations = false

# the output encoding used when revision files
# are written from script.py.mako
# output_encoding = utf-8

sqlalchemy.url = mysql+mysqlconnector://tum12607_reflex:9ujT.uD9G}*L@181.214.83.154/tum12607_app12_reflex


[post_write_hooks]
# post_write_hooks defines scripts or Python functions that are run
# on newly generated revision scripts.  See the documentation for further
# detail and examples

# format using "black" - use the console_scripts runner, against the "black" entrypoint
# hooks = black
# black.type = console_scripts
# black.entrypoint = black
# black.options = -l 79 REVISION_SCRIPT_FILENAME

# lint with attempts to fix using "ruff" - use the exec runner, execute a binary
# hooks = ruff
# ruff.type = exec
# ruff.executable = %(here)s/.venv/bin/ruff
# ruff.options = --fix REVISION_SCRIPT_FILENAME

# Logging configuration
[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARNING
handlers = console
qualname =

[logger_sqlalchemy]
level = WARNING
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
```

## logica.txt

```txt
Framework: Reflex
Nivel: Principiante
Tu Rol: Tutor
Proyecto: Configuracion Server Worker
Puedo acceder al manifest y al sw.js mediante las rutas http://localhost:3000/sw.js / http://localhost:3000/manifest.json 
Logro ver el manifest en Chrome Devtolls/Applications/Manifest
Presenta solo el metodo/funcion/componente/atributo/argumento/etc a modificar con su respectiva explicación.
Esto para evitar trastocar funcionalidades correctas y operativas
```

## README.md

```md

```
app12
├─ alembic
│  ├─ README
│  ├─ env.py
│  ├─ script.py.mako
│  └─ versions
│     ├─ 3684de5927a1_.py
│     └─ 497bdedb3272_relacion_ordenes_suplidores.py
├─ app12
│  ├─ __init__.py
│  ├─ admin
│  │  ├─ __init__.py
│  │  └─ master.py
│  ├─ amazon_index.py
│  ├─ api
│  │  ├─ __init__.py
│  │  └─ views
│  │     └─ download_pdf_commission.py
│  ├─ app12.py
│  ├─ applicable_fees_admin.py
│  ├─ backend
│  │  ├─ __init__.py
│  │  ├─ backend.py
│  │  └─ heads_backend.py
│  ├─ components
│  │  ├─ __init__.py
│  │  ├─ color_status.py
│  │  ├─ filter_orders.py
│  │  ├─ main_table.py
│  │  ├─ main_table_heads.py
│  │  ├─ main_table_heads_admin.py
│  │  ├─ main_table_lowstockfee.py
│  │  ├─ main_table_lowstockfee_admin.py
│  │  ├─ modal_inputs_fees_purchs_total.py
│  │  ├─ modal_status.py
│  │  ├─ modal_status_heads.py
│  │  ├─ navbar.py
│  │  ├─ table_lowstockfee.py
│  │  └─ ui_base_page.py
│  ├─ control_heads.py
│  ├─ documentacion
│  │  └─ estructura_general
│  ├─ heads_admin.py
│  ├─ index_admin.py
│  ├─ login.py
│  ├─ lowstockfee.py
│  ├─ marykay_index.py
│  ├─ purchs_page.py
│  └─ tasks.py
├─ assets
│  ├─ drops-6392473_640.jpg
│  ├─ drops-6392473_640.jpg:Zone.Identifier
│  ├─ favicon.ico
│  ├─ icon-192x192.png
│  ├─ icon-512x512.png
│  ├─ logo.jpg
│  ├─ logo.jpg:Zone.Identifier
│  ├─ manifest.json
│  ├─ nophoto.jpg
│  ├─ nophoto.jpg:Zone.Identifier
│  └─ sw.js
├─ github
│  └─ workflows
│     ├─ deploy.yml
│     └─ requirements.txt
├─ requirements.txt
├─ rxconfig.py
└─ upload_files
   └─ 2882UQ_document.pdf

```
```

## reflex.db

```db
SQLite format 3   @        	                                                             .v�� N �J�HN                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  �D�WtablesupplierssuppliersCREATE TABLE suppliers (
	supplierid VARCHAR NOT NULL, 
	suppname VARCHAR NOT NULL, 
	currcode VARCHAR NOT NULL, 
	phn VARCHAR NOT NULL, 
	PRIMARY KEY (supplierid)
)1E indexsqlite_autoindex_suppliers_1suppliers	�D''�Gtablepurchorders12purchorders12CREATE TABLE purchorders12 (
	orderno VARCHAR NOT NULL, 
	supplierno VARCHAR NOT NULL, 
	comments VARCHAR NOT NULL, 
	orddate VARCHAR NOT NULL, 
	requisitionno VARCHAR NOT NULL, 
	orderref VARCHAR NOT NULL, 
	status VARCHAR NOT NULL, 
	urltracking VARCHAR NOT NULL, 
	deladd1 VARCHAR NOT NULL, 
	deladd2 VARCHAR NOT NULL, 
	deladd3 VARCHAR NOT NULL, 
	intostocklocation VARCHAR NOT NULL, 
	PRIMARY KEY (orderno)
)9M' indexsqlite_autoindex_purchorders12_1purchorders12��itablelocationslocationsCREATE TABLE locations (
	loccode VARCHAR NOT NULL, 
	locationname VARCHAR NOT NULL, 
	PRIMARY KEY (loccode)
)1E indexsqlite_autoindex_locations_1locations�)++�	tablealembic_versionalembic_versionCREATE TABLE alembic_version (
	version_num VARCHAR(32) NOT NULL, 
	CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
)=Q+ indexsqlite_autoindex_alembic_version_1alembic_version          � �                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      %3684de5927a1
   � �                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      %	3684de5927a1                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
```

## requirements.txt

```txt
alembic==1.14.0
annotated-types==0.7.0
anyio==4.7.0
bidict==0.23.1
build==1.2.2.post1
certifi==2024.8.30
cffi==1.17.1
charset-normalizer==3.4.0
click==8.1.7
cryptography==44.0.0
distro==1.9.0
docutils==0.21.2
fastapi==0.115.6
greenlet==3.1.1
gunicorn==23.0.0
h11==0.14.0
httpcore==1.0.7
httpx==0.28.1
idna==3.10
importlib_metadata==8.5.0
jaraco.classes==3.4.0
jaraco.context==6.0.1
jaraco.functools==4.1.0
jeepney==0.8.0
Jinja2==3.1.4
keyring==25.5.0
lazy_loader==0.4
Mako==1.3.8
markdown-it-py==3.0.0
MarkupSafe==3.0.2
mdurl==0.1.2
more-itertools==10.5.0
mysql-connector-python==9.1.0
mysqlclient==2.2.7
nh3==0.2.19
packaging==24.2
passlib==1.7.4
pipdeptree==2.16.2
pkginfo==1.10.0
platformdirs==4.3.6
psutil==6.1.0
pycparser==2.22
pydantic==2.10.3
pydantic_core==2.27.1
Pygments==2.18.0
PyMySQL==1.1.1
pyproject_hooks==1.2.0
python-dateutil==2.9.0.post0
python-dotenv==1.0.1
python-engineio==4.10.1
python-multipart==0.0.19
python-socketio==5.11.4
readme_renderer==44.0
redis==5.2.1
reflex==0.6.7
reflex-chakra==0.6.2
reflex-hosting-cli==0.1.30
requests==2.32.3
requests-toolbelt==1.0.0
rfc3986==2.0.0
rich==13.9.4
SecretStorage==3.3.3
setuptools==75.6.0
shellingham==1.5.4
simple-websocket==1.1.0
six==1.17.0
sniffio==1.3.1
SQLAlchemy==2.0.36
sqlmodel==0.0.22
starlette==0.41.3
starlette-admin==0.14.1
tabulate==0.9.0
tomlkit==0.13.2
twine==5.1.1
typer==0.15.1
typing_extensions==4.12.2
urllib3==2.2.3
uvicorn==0.32.1
websockets==14.1
wheel==0.45.1
wrapt==1.17.0
wsproto==1.2.0
zipp==3.21.0
```

## rxconfig.py

```py
import reflex as rx
from dotenv import load_dotenv
import os

load_dotenv()

config = rx.Config(
    app_name="app12",
    api_url="http://localhost:8000",
    backend_host="0.0.0.0",
    frontend_port=3000,
    backend_port=8000,
    env_file=".env"
)
```

