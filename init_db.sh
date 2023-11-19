#!/bin/bash

# Input parameters
DB_NAME="Pharmacy_Defender"
DB_OWNER="arthur"
DB_HOST="localhost"

# Database creation
createdb -h ${DB_HOST} -U ${DB_OWNER} ${DB_NAME}

# Setting the database owner
psql -h ${DB_HOST} -U ${DB_OWNER} -c "ALTER DATABASE ${DB_NAME} OWNER TO ${DB_OWNER};"

echo "База данных ${DB_NAME} успешно создана и установлен владелец ${DB_OWNER}."