.PHONY: dev test

dev:
	# run uvicorn with reload using uv-managed venv
	env -u VIRTUAL_ENV uv run uvicorn app:app --reload

test:
	# run pytest
	uv run pytest -q
