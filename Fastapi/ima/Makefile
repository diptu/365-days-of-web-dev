# Makefile

.PHONY: dev test test-unit test-e2e db-rev db-autogen db-up db-down db-stamp lint format

# Run uvicorn with reload using uv-managed venv
dev:
	@echo "Starting dev server..."
	env -u VIRTUAL_ENV uv run uvicorn app:app --reload

# Run full test suite
test:
	@echo "Running all tests..."
	uv run pytest -q

# Run only unit tests
test-unit:
	@echo "Running unit tests..."
	uv run pytest -q app/tests/unit

# Run only e2e tests
test-e2e:
	@echo "Running e2e tests..."
	uv run pytest -q app/tests/e2e

# Alembic helpers
db-rev:
	@echo "Creating empty revision..."
	uv run alembic revision -m "$(m)"

db-autogen:
	@echo "Autogenerating revision..."
	uv run alembic revision --autogenerate -m "$(m)"

db-up:
	@echo "Upgrading to head..."
	uv run alembic upgrade head

db-down:
	@echo "Downgrading one revision..."
	uv run alembic downgrade -1

db-stamp:
	@echo "Stamping current head..."
	uv run alembic stamp head

# Code quality
lint:
	@echo "Linting with Ruff..."
	uv run ruff check .

format:
	@echo "Formatting with Ruff and Black..."
	uv run ruff check --fix .
	uv run black .
