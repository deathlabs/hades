# Set Dockerfile metadata for the first build.
FROM alpine:3.21 AS first_build
LABEL image.authors="Victor Fernandez III, @cyberphor"

# Install Postgres, pgcrypto, and gen_salt dependencies.
RUN apk update &&\
    apk add postgresql postgresql-contrib libpq-dev

# Set the working directory.
WORKDIR /app

# Copy the entrypoint script.
COPY entrypoint.sh entrypoint.sh
COPY hades_missions.sql hades_missions.sql

# Create prerequisite directories.
RUN chmod u+x /app/entrypoint.sh &&\
    mkdir /var/lib/postgresql/data &&\
    mkdir /run/postgresql &&\
    chown -R postgres:postgres /var/lib/postgresql/data &&\
    chown -R postgres:postgres /run/postgresql

# Switch to a non-root user.
USER postgres

# Expose the default Postgres port.
EXPOSE 5432

# Start Postgres.
ENTRYPOINT [ "./entrypoint.sh" ]
