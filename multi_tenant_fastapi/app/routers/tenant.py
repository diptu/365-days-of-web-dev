import importlib
from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import ProductCreate, ProductOut

router = APIRouter(prefix="/api", tags=["tenants"])

ALLOWED_TENANTS = {"tenant_a", "tenant_b"}


def get_models_for_tenant(tenant: str):
    if tenant not in ALLOWED_TENANTS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unknown tenant: {tenant}",
        )
    # Dynamically import app.tenant_<x>.models
    return importlib.import_module(f"app.{tenant}.models")


@router.post("/products", response_model=ProductOut, status_code=201)
def create_product(
    payload: ProductCreate,
    x_tenant: str = Header(..., alias="X-Tenant"),
    db: Session = Depends(get_db),
):
    m = get_models_for_tenant(x_tenant)
    obj = m.Product(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/products", response_model=list[ProductOut])
def list_products(
    x_tenant: str = Header(..., alias="X-Tenant"),
    db: Session = Depends(get_db),
):
    m = get_models_for_tenant(x_tenant)
    return db.query(m.Product).all()
