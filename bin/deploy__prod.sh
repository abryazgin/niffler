#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
${DIR}/deploy.sh developer niffler postgresql://niffler:d41d8cd98f@localhost:5432/niffler
