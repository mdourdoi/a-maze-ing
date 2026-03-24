ENV_NAME=maze_env
CONFIG_FILE=config.txt
PYTHON := $(ENV_NAME)/bin/python

POETRY_LOCK := poetry.lock
PYPROJECT_TOML := pyproject.toml

install: $(PYPROJECT_TOML) $(POETRY_TOML) | $(PYTHON)
	make venv
	. $(ENV_NAME)/bin/activate && poetry install

venv:
	./scripts/setup_env.sh ${ENV_NAME}

run:
	$(PYTHON) a_maze_ing.py ${CONFIG_FILE}

debug:
	$(PYTHON) -m pdb a_maze_ing.py ${CONFIG_FILE}

clean:
	rm -rf ${ENV_NAME}
	find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete
	rm -rf .mypy_cache .pytest_cache build dist *.egg-info

lint:
	$(ENV_NAME)/bin/flake8 $(SRC)
	$(ENV_NAME)/bin/mypy $(SRC) --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict: install
	flake8 $(SRC) 
	mypy $(SRC) --strict
