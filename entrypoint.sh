#!/bin/sh

# Wait for 60 seconds to ensure that the database service is fully up and running
sleep 60

# Log
echo "Application preparing to start" 

# Initialize and migrate the database
flask db init || true
flask db migrate -m "Initial migration." || true
flask db upgrade

# Start the application
exec "$@"