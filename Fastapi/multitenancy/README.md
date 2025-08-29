# Multitenancy (Schema-per-tenant) FastAPI

This app uses PostgreSQL schemas per tenant. Shared tables live in
`shared` and tenant tables default to schema `tenant`, remapped per
request with SQLAlchemy's `schema_translate_map`.

Key flow:
- `Tenant` model in `shared.tenants`
- `Student` model in tenant schema
- `get_tenant()` looks up tenant by `Host` header
- `get_db()` opens a session remapped to the tenant schema
