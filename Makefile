venv:
	uv venv

dev:
	uv pip install -e .[dev]

fmt:
	ruff format

lint:
	ruff check --fix


test:
	uv run pytest -vvv