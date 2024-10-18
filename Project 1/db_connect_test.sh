#!/bin/bash


DB_NAME="logs"
DB_USER="danny"
DB_PASSWORD="dvm1181997"
DB_HOST="/var/run/postgresql"
DB_PORT="5432"

#export PGPASSWORD="$DB_PASSWORD"

psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -c "SELECT * FROM severelogs;"

# unset PGPASSWORD
