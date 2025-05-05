#!/usr/bin/env sh

set -e

# Initialize Postgres.
if [ ! -f "/var/lib/postgresql/data/PG_VERSION" ]; then
  # Create prerequisite databases. 
  initdb -D /var/lib/postgresql/data

  # Start Postgres as a background process.
  postgres -D /var/lib/postgresql/data &
  POSTGRES_PID=$!

  # Wait for Postgres to start.
  until pg_isready; do
    sleep 1
  done

  # Configure the "hades_missions" database.
  psql -U postgres -f /app/hades_missions.sql

  # Stop Postgres.
  kill "$POSTGRES_PID"
  wait "$POSTGRES_PID" 2>/dev/null || true
fi

# Configure Postgres to listen on all network interfaces. 
echo "listen_addresses = '*'" >> /var/lib/postgresql/data/postgresql.conf

# Configure Postgres to authenticate every user of every database from every IP address using MD5.
echo "host  all all 0.0.0.0/0 md5" >> /var/lib/postgresql/data/pg_hba.conf

# Start Postgres in the foreground.
exec postgres -D /var/lib/postgresql/data