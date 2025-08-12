import datetime as dt
from sqlalchemy import Column, Integer, String, DateTime, Float


class ProductMixin:
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    created_at = Column(DateTime, default=dt.datetime.utcnow)


class OrderMixin:
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, index=True)
    quantity = Column(Integer)
    total_price = Column(Float)
    order_date = Column(DateTime, default=dt.datetime.utcnow)
