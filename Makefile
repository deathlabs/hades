# ---------------------------------------------------------
# Set the default target.
# ---------------------------------------------------------

.DEFAULT_GOAL := build

# ---------------------------------------------------------
# Load environment variables.
# ---------------------------------------------------------

.PHONY: print-dot-env-files-used
.SILENT: print-dot-env-files-used

# Set the "env" to local if an argument is not provided.
ENV ?= local

# Set the "profile" to "core if an argument is not provided.
PROFILE ?= core

# Load the specified environment file.
ENV_FILE := .env.$(ENV)
include $(ENV_FILE)

print-dot-env-files-used:
	@echo "[+] Set environment variables using $(ENV_FILE)"

# ---------------------------------------------------------
# Build all the containers.
# ---------------------------------------------------------

.PHONY: build
.SILENT: build

build: print-dot-env-files-used
	docker compose --env-file $(ENV_FILE) --profile $(PROFILE) build --no-cache

# ---------------------------------------------------------
# Start all the containers.
# ---------------------------------------------------------

.PHONY: start
.SILENT: start

start: print-dot-env-files-used
	docker compose --profile $(PROFILE) up
