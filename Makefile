PYTHON := maze_venv/bin/python3
PIP := maze_venv/bin/pip3
MAIN := a_maze_ing.py
CONFIG := config.txt

install: maze_venv

maze_venv:
	python3.10 -m venv maze_venv
	$(PIP) install -r requirements.txt

run: install
	$(PYTHON) $(MAIN) $(CONFIG)

build:
	python3.10 -m venv build_venv
	build_venv/bin/pip install build
	build_venv/bin/python3.10 -m build
	cp dist/mazegen-1.0.0-py3-none-any.whl .
	rm -rf build_venv dist *.egg-info

debug:
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)

clean:
	find . -type d -name "_pycache_" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name "maze_venv" -exec rm -rf {} +

lint:
	flake8 . --exclude lib,venv
	mypy src/ --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 . --exclude lib,venv
	mypy src/ --strict --allow-untyped-calls

.PHONY: install run debug clean lint lint-strict build
