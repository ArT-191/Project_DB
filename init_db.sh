#!/bin/bash

# Input parameters
DB_NAME="Pharmacy_Director"
DB_OWNER="arthur_191"
DB_HOST="localhost"

# Database creation
createdb -h ${DB_HOST} -U ${DB_OWNER} ${DB_NAME}

# Setting the database owner
psql -h ${DB_HOST} -U ${DB_OWNER} -c "ALTER DATABASE ${DB_NAME} OWNER TO ${DB_OWNER};"

echo "Database ${DB_NAME} has been successfully created and owner ${DB_OWNER} has been set."