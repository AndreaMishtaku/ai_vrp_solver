#!/bin/sh

# Wait to ensure that the database service is fully up
sleep 180
# Log
echo "Application preparing to start" 

echo "Application preparing to start"

# Check if the 'migrations' folder exists
if [ ! -d "migrations" ]; then
    # Initialize and migrate the database
    echo "Initializing and migrating the database"
    flask db init || true
    flask db migrate -m "Initial migration." || true
    flask db upgrade
else
    echo "Migrations folder already exists, skipping database initialization and migration"
fi

# Start the application
exec "$@"