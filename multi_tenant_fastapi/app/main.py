from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from .db import SessionLocal
from .tenancy.middleware import TenantMiddleware
from .tenancy.service import create_tenant
from .models.shared import User, Note

app = FastAPI(title="Multi-tenant FastAPI (schema-per-tenant)")

# In dev: set root_domain=None and use X-Tenant header
app.add_middleware(TenantMiddleware, root_domain=None, default="public")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/tenants/{name}")
def api_create_tenant(name: str):
    create_tenant(name)
    return {"ok": True, "tenant": name}


@app.post("/users")
def create_user(
    email: str = Query(...),
    db: Session = Depends(get_db),
):
    u = User(email=email)
    db.add(u)
    db.commit()
    db.refresh(u)
    return u


@app.post("/notes")
def create_note(
    title: str = Query(...),
    body: str | None = Query(None),
    db: Session = Depends(get_db),
):
    n = Note(title=title, body=body)
    db.add(n)
    db.commit()
    db.refresh(n)
    return n


@app.get("/notes")
def list_notes(db: Session = Depends(get_db)):
    return db.query(Note).all()
