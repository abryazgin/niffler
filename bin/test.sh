#!/usr/bin/env bash
set -e

HOST=$1
if [ -z "$HOST" ]; then
    HOST="10.0.3.206"
fi

PARENT_DIR="$( dirname "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )")"
TEST_DIR="${PARENT_DIR}/tests"
SRC_DIR="${PARENT_DIR}/src"
CONFIG_PATH="${PARENT_DIR}/src/development_config.py"
NGINX_TEST_URL="http://${HOST}:80"
NGINX_REAL_URL="http://${HOST}:8800"
VENV="${PARENT_DIR}/venv"

echo $CONFIG_PATH

source ${VENV}/bin/activate

CONFIG_PATH="${CONFIG_PATH}" \
    PYTHONPATH="${SRC_DIR}" \
    NGINX_TEST_URL="${NGINX_TEST_URL}" \
    NGINX_REAL_URL="${NGINX_REAL_URL}" \
    python -m unittest discover "${TEST_DIR}"

deactivate