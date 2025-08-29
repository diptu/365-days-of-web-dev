#!/usr/bin/env python3
# scripts/create_tenant.py

from pathlib import Path
import sys
import argparse

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Ensure models are registered
import app.core.models.student  # noqa: F401
import app.core.models.tanent  # noqa: F401

from app.core.helper.tenant import create_tenant_schema  # noqa: E402


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a tenant schema")
    parser.add_argument("--name", required=True, help="Tenant name")
    parser.add_argument("--schema", required=True, help="Tenant schema name")
    parser.add_argument("--host", required=True, help="Tenant host")
    args = parser.parse_args()

    create_tenant_schema(schema=args.schema, name=args.name, host=args.host)
    print(f"✅ Tenant '{args.name}' created (schema={args.schema}, host={args.host})")
