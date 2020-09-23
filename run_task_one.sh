#!/bin/bash

export LOG_LEVEL="INFO"
export MYSQL_USER=""
export MYSQL_PASSWORD=""
export MYSQL_HOST="localhost"
export MYSQL_AUTH_PLUGIN="mysql_native_password"
export BASE_API_URL="http://swapi.dev/api/"

python tasks/task_one.py