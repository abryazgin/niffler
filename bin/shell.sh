#!/usr/bin/env bash

INTERPRETER=$1 # for example ipython
if [ -z "$INTERPRETER" ]; then
    INTERPRETER="ipython"
fi

PARENT_DIR="$( dirname "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )")"
CONFIG_PATH="${PARENT_DIR}/src/development_config.py"
SRC_DIR="${PARENT_DIR}/src"
VENV="${PARENT_DIR}/venv"

echo $CONFIG_PATH

source ${VENV}/bin/activate

CONFIG_PATH="${CONFIG_PATH}" \
    PYTHONPATH="${SRC_DIR}" \
    ${INTERPRETER}

deactivate