#!/usr/bin/env bash
set -euo pipefail

MODE="${1:-headers}"          # headers | subdomain
BASE="http://127.0.0.1:8000"
ROOT_DOMAIN="${ROOT_DOMAIN:-localhost}"

# If your routers use @router.post("") (no slash), set SLASH="".
# If they use @router.post("/"), set SLASH="/".
SLASH=""

curl_cmd() {
  # -s silent body, -S show errors, -D - print headers, -w prints status
  curl -sS -D - -w "\nHTTP %{http_code}\n" "$@"
}

echo -e "\n== Health =="
curl_cmd "$BASE/health"

echo -e "\n== Create tenants =="
curl_cmd -X POST "$BASE/tenants/tenant_a"
curl_cmd -X POST "$BASE/tenants/tenant_b"

if [[ "$MODE" == "headers" ]]; then
  echo -e "\n== Create outlets under tenant_a (header mode) =="
  curl_cmd -X POST "$BASE/outlets$SLASH" \
    -H "Content-Type: application/json" \
    -H "X-Tenant: tenant_a" \
    -d '{"code":"jhon","name":"Jhon"}'
  curl_cmd -X POST "$BASE/outlets$SLASH" \
    -H "Content-Type: application/json" \
    -H "X-Tenant: tenant_a" \
    -d '{"code":"jeny","name":"Jeny"}'

  echo -e "\n== Create notes in each outlet =="
  curl_cmd -X POST "$BASE/notes$SLASH" \
    -H "Content-Type: application/json" \
    -H "X-Tenant: tenant_a" \
    -H "X-Outlet: jhon" \
    -d '{"title":"Jhon note 1","body":"Hello from Jhon"}'
  curl_cmd -X POST "$BASE/notes$SLASH" \
    -H "Content-Type: application/json" \
    -H "X-Tenant: tenant_a" \
    -H "X-Outlet: jeny" \
    -d '{"title":"Jeny note 1","body":"Hello from Jeny"}'

  echo -e "\n== List notes per outlet (scoped) =="
  curl_cmd "$BASE/notes$SLASH" -H "X-Tenant: tenant_a" -H "X-Outlet: jhon"
  curl_cmd "$BASE/notes$SLASH" -H "X-Tenant: tenant_a" -H "X-Outlet: jeny"

  echo -e "\n== Tenant summary (tenant_a, all outlets) =="
  curl_cmd "$BASE/notes$SLASH" -H "X-Tenant: tenant_a"

  echo -e "\n== Cross-tenant isolation (tenant_b) =="
  curl_cmd "$BASE/outlets$SLASH" -H "X-Tenant: tenant_b"
  curl_cmd "$BASE/notes$SLASH"   -H "X-Tenant: tenant_b"

else
  echo -e "\n== Subdomain mode (ROOT_DOMAIN=$ROOT_DOMAIN) =="

  echo -e "\n== Create outlets under tenant_a (tenant root domain) =="
  curl_cmd -X POST "http://tenant_a.$ROOT_DOMAIN:8000/outlets$SLASH" \
    --resolve "tenant_a.$ROOT_DOMAIN:8000:127.0.0.1" \
    -H "Content-Type: application/json" \
    -d '{"code":"jhon","name":"Jhon"}'
  curl_cmd -X POST "http://tenant_a.$ROOT_DOMAIN:8000/outlets$SLASH" \
    --resolve "tenant_a.$ROOT_DOMAIN:8000:127.0.0.1" \
    -H "Content-Type: application/json" \
    -d '{"code":"jeny","name":"Jeny"}'

  echo -e "\n== Create notes from each outlet subdomain =="
  curl_cmd -X POST "http://jhon.tenant_a.$ROOT_DOMAIN:8000/notes$SLASH" \
    --resolve "jhon.tenant_a.$ROOT_DOMAIN:8000:127.0.0.1" \
    -H "Content-Type: application/json" \
    -d '{"title":"Jhon note 1","body":"Hello from Jhon"}'
  curl_cmd -X POST "http://jeny.tenant_a.$ROOT_DOMAIN:8000/notes$SLASH" \
    --resolve "jeny.tenant_a.$ROOT_DOMAIN:8000:127.0.0.1" \
    -H "Content-Type: application/json" \
    -d '{"title":"Jeny note 1","body":"Hello from Jeny"}'

  echo -e "\n== List notes per outlet =="
  curl_cmd "http://jhon.tenant_a.$ROOT_DOMAIN:8000/notes$SLASH" \
    --resolve "jhon.tenant_a.$ROOT_DOMAIN:8000:127.0.0.1"
  curl_cmd "http://jeny.tenant_a.$ROOT_DOMAIN:8000/notes$SLASH" \
    --resolve "jeny.tenant_a.$ROOT_DOMAIN:8000:127.0.0.1"

  echo -e "\n== Tenant summary (tenant_a) =="
  curl_cmd "http://tenant_a.$ROOT_DOMAIN:8000/notes$SLASH" \
    --resolve "tenant_a.$ROOT_DOMAIN:8000:127.0.0.1"

  echo -e "\n== Cross-tenant isolation (tenant_b) =="
  curl_cmd "http://tenant_b.$ROOT_DOMAIN:8000/outlets$SLASH" \
    --resolve "tenant_b.$ROOT_DOMAIN:8000:127.0.0.1"
  curl_cmd "http://tenant_b.$ROOT_DOMAIN:8000/notes$SLASH" \
    --resolve "tenant_b.$ROOT_DOMAIN:8000:127.0.0.1"
fi

echo -e "\n== Done. =="
