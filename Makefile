ENV_NAME=new_test
CONFIG_FILE="config.txt"

SRC= ./generators \
	 ./helpers \
	 ./source \

run:
	python3 a_maze_ing.py ${CONFIG_FILE}

debug:
	python3 -m pdb a_maze_ing.py ${CONFIG_FILE}

install:
	make venv
	. $(ENV_NAME)/bin/activate && poetry install

venv:
	./scripts/setup_env.sh ${ENV_NAME}

clean:
	rm -rf ${ENV_NAME}
	find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete

lint:
	flake8 $(SRC)
	mypy $(SRC) --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 $(SRC) 
	mypy $(SRC) --strict
