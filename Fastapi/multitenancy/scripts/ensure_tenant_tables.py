#!/usr/bin/env python3
# scripts/ensure_tenant_tables.py

from pathlib import Path
import sys
import argparse

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Import models package to populate metadata
import app.core.models  # noqa: F401

from app.core.db.database import create_tenant_tables  # noqa: E402


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Ensure tenant tables exist")
    p.add_argument("--schema", required=True, help="Tenant schema name")
    args = p.parse_args()

    create_tenant_tables(args.schema)
    print(f"✅ Ensured tables exist in schema '{args.schema}'")
