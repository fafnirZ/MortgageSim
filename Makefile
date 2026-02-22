run:
	uv run streamlit run ./mortgage_sim/simulation/streamlit.py

venv:
	uv venv

develop:
	uv pip install -e .[dev]

fmt:
	ruff format

lint:
	ruff check --fix


test:
	uv run pytest -vvv
