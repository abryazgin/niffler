#!/usr/bin/env bash

USER=$1
HOST=$2
DBURL=$3
PARENT_DIR="$( dirname "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )")"
DIR="${PARENT_DIR}/deploy"

ansible-playbook \
    -i ${DIR}/hosts.cnf \
    ${DIR}/main.yml \
    -e "hosts=${HOST} database_url=${DBURL} user=${USER}"  -v