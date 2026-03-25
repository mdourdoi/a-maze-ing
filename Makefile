ENV_NAME := maze_env
CONFIG_FILE := config.txt

PYTHON := $(ENV_NAME)/bin/python
POETRY := $(ENV_NAME)/bin/poetry
FLAKE8 := $(ENV_NAME)/bin/flake8
MYPY := $(ENV_NAME)/bin/mypy
INSTALL_STAMP := $(ENV_NAME)/.installed

PYPROJECT_TOML := pyproject.toml

$(INSTALL_STAMP): $(PYPROJECT_TOML) scripts/setup_env.sh
	./scripts/setup_env.sh $(ENV_NAME)
	. $(ENV_NAME)/bin/activate && $(POETRY) install
	touch $(INSTALL_STAMP)

install: $(INSTALL_STAMP)

run: $(INSTALL_STAMP)
	$(PYTHON) a_maze_ing.py $(CONFIG_FILE)

debug: $(INSTALL_STAMP)
	$(PYTHON) -m pdb a_maze_ing.py $(CONFIG_FILE)

lint: $(INSTALL_STAMP)
	$(FLAKE8) . --exclude $(ENV_NAME)
	$(MYPY) . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict: $(INSTALL_STAMP)
	$(FLAKE8) . --exclude $(ENV_NAME)
	$(MYPY) . --strict

clean:
	rm -rf $(ENV_NAME)
	find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete
	rm -rf .mypy_cache .pytest_cache build dist *.egg-info
	rm -f poetry.lock

.PHONY: install run debug clean lint lint-strict
