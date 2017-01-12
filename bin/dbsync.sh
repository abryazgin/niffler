#!/usr/bin/env bash
set -e

PARENT_DIR="$( dirname "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )")"
VENV="${PARENT_DIR}/venv"
SRC_DIR="${PARENT_DIR}/src"
ALEMBIC_WORKING_DIR="${SRC_DIR}/core/db"
ALEMBIC_DIR="${PARENT_DIR}/src/core/db/alembic"
ALEMBIC_CONFIG="${PARENT_DIR}/src/core/db/alembic.ini"
CONFIG_PATH="${PARENT_DIR}/src/development_config.py"
DATABASE_URL="sqlite:///${PARENT_DIR}/development.db"

echo "${DATABASE_URL}"

# меняем текующую рабочую директорию
cd ${ALEMBIC_WORKING_DIR}

# дропаем миграции
find ${ALEMBIC_DIR}/versions/ -name "*.pyc" -type f -delete
find ${ALEMBIC_DIR}/versions/ -name "*.py"  -type f -delete

# Активируем virtualenv
source "${VENV}/bin/activate"

# Синхроним БД
MSG="dbsync : "$(date '+%Y_%m_%d__%H_%M_%S')

DATABASE_URL="${DATABASE_URL}" PYTHONPATH="${SRC_DIR}" alembic revision --autogenerate -m "${MSG}"
DATABASE_URL="${DATABASE_URL}" PYTHONPATH="${SRC_DIR}" alembic upgrade head

# Диактивируем virtualenv
deactivate

# Удяляем хеш
sqlite3 ${PARENT_DIR}/development.db 'DELETE FROM alembic_version'

# дропаем миграции
find ${ALEMBIC_DIR}/versions/ -name "*.pyc" -type f -delete
find ${ALEMBIC_DIR}/versions/ -name "*.py"  -type f -delete