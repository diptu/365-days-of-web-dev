from app.database import get_base
from app.base_models import ProductMixin, OrderMixin

Base = get_base("tenant_a")


class Product(Base, ProductMixin):
    __tablename__ = "products"


class Order(Base, OrderMixin):
    __tablename__ = "orders"
