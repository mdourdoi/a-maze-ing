#!/bin/bash


GREEN="\e[1;92m" RESET="\e[0m"
VENV=$1

echo -e "${GREEN}[SCRIPT]${RESET} === Setting up new env ==="
echo -e "${GREEN}[SCRIPT]${RESET} Cleaning env..."
if [ ! -d "${VENV}" ]; then
	echo -e "${GREEN}[SCRIPT]${RESET} Creating Virtual env ${VENV}..."
	python3 -m venv "${VENV}"
fi
echo -e "${GREEN}[SCRIPT] SUCCESS !${RESET} "


echo -e "${GREEN}[SCRIPT]${RESET} Sourcing new env..."
source ${VENV}/bin/activate
echo -e "${GREEN}[SCRIPT] SUCCESS !${RESET} "


echo -e "${GREEN}[SCRIPT]${RESET} Installing Poetry..."
pip install poetry
echo -e "${GREEN}[SCRIPT] SUCCESS !${RESET} "
echo -e "${GREEN}[SCRIPT]${RESET} Script end"
