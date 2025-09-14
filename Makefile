# ---------------------------------------------------------
# Set the default target.
# ---------------------------------------------------------

.DEFAULT_GOAL := build

# ---------------------------------------------------------
# Load environment variables and secrets.
# ---------------------------------------------------------

.PHONY: print-dot-env-files-used
.SILENT: print-dot-env-files-used

# Load the specified environment variables file.
ENV_FILE ?= .env.local
include $(ENV_FILE)

# Load the specified secrets file.
SECRETS_FILE ?= .env.local.secrets
include $(SECRETS_FILE)

# Set the Docker Compose profile to "all" if an argument is not provided.
DOCKER_COMPOSE_PROFILE ?= all

print-dot-env-files-used:
	@echo "[+] Set environment variables using $(ENV_FILE) and $(SECRETS_FILE)"

# ---------------------------------------------------------
# Build the containers.
# ---------------------------------------------------------

.PHONY: build
.SILENT: build

build: print-dot-env-files-used
	docker compose --profile $(DOCKER_COMPOSE_PROFILE) --env-file $(ENV_FILE) --env-file $(SECRETS_FILE) build --no-cache

# ---------------------------------------------------------
# Start the containers.
# ---------------------------------------------------------

.PHONY: start
.SILENT: start

start: print-dot-env-files-used
	docker compose --profile $(DOCKER_COMPOSE_PROFILE) --env-file $(ENV_FILE) --env-file $(SECRETS_FILE) up -d

# ---------------------------------------------------------
# Stop the containers.
# ---------------------------------------------------------

.PHONY: stop
.SILENT: stop

stop: print-dot-env-files-used
	docker compose --profile $(DOCKER_COMPOSE_PROFILE) --env-file $(ENV_FILE) --env-file $(SECRETS_FILE) down
