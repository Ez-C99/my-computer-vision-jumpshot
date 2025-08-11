.PHONY: setup dev hooks fmt lint test demo fetch-third-party

PY=python3.11

setup:
	$(PY) -m venv .venv
	. .venv/bin/activate && python -m pip install --upgrade pip setuptools wheel
	. .venv/bin/activate && pip install -r requirements.txt
	- . .venv/bin/activate && pip install -r requirements-dev.txt
	- . .venv/bin/activate && pre-commit install

dev:
	. .venv/bin/activate && pip install -r requirements-dev.txt

hooks:
	. .venv/bin/activate && pre-commit run --all-files

fmt:
	. .venv/bin/activate && black .
	. .venv/bin/activate && isort .
	. .venv/bin/activate && ruff check --fix .

lint:
	. .venv/bin/activate && ruff check .

test:
	. .venv/bin/activate && pytest

fetch-third-party:
	bash scripts/fetch_third_party.sh

demo:
	. .venv/bin/activate && python -m my_computer_vision_jumpshot.cli \
		--input examples/sample_video.mp4 \
		--out examples/sample_output
