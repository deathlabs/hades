# ---------------------------------------------------------
# Default Target
# ---------------------------------------------------------

.DEFAULT_GOAL := build

APP_NAME := hades
APP_VERSION := v0.1.0
CONTAINER_NAME := backend
PORT := 8001

# ---------------------------------------------------------
# QA
# ---------------------------------------------------------

.PHONY: qa/format qa/lint qa
.SILENT: qa/format qa/lint qa

# Execute formatter.
qa/format: 
	@echo "[*] Formatting '$(APP_NAME)/$(CONTAINER_NAME)'..."

# Execute linter.
qa/lint: 
	@echo "[*] Linting '$(APP_NAME)/$(CONTAINER_NAME)'..."

# Execute all quality assurance tools.
qa: qa/format qa/lint

# ---------------------------------------------------------
# Test
# ---------------------------------------------------------

.PHONY: test
.SILENT: test

# Execute unit tests with test coverage.
test: 
	@echo "[*] Testing '$(APP_NAME)/$(CONTAINER_NAME)'..."

# ---------------------------------------------------------
# Build
# ---------------------------------------------------------

.PHONY: build
.SILENT: build

build: qa test
	docker build -t $(APP_NAME)/$(CONTAINER_NAME):$(APP_VERSION) .

# ---------------------------------------------------------
# Start
# ---------------------------------------------------------

.PHONY: start
.SILENT: start

start:
	docker run --name $(CONTAINER_NAME) -p $(PORT):$(PORT) --env-file .env.docker $(APP_NAME)/$(CONTAINER_NAME):$(APP_VERSION)

# ---------------------------------------------------------
# Stop
# ---------------------------------------------------------

.PHONY: stop
.SILENT: stop

stop:
	docker container stop $(CONTAINER_NAME)
	docker container rm $(CONTAINER_NAME)
