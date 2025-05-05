# ---------------------------------------------------------
# Default Target
# ---------------------------------------------------------

.DEFAULT_GOAL := build

APP_NAME := hades
APP_VERSION := v0.1.0
CONTAINER_NAME := rabbitmq
PORT := 5672
MGMT_PORT := 15672

# ---------------------------------------------------------
# Build
# ---------------------------------------------------------

.PHONY: build
.SILENT: build

build: 
	docker build -t $(APP_NAME)/$(CONTAINER_NAME):$(APP_VERSION) .

# ---------------------------------------------------------
# Start
# ---------------------------------------------------------

.PHONY: start
.SILENT: start

start:
	docker run --name $(CONTAINER_NAME) -d -p $(PORT):$(PORT) -p ${MGMT_PORT}:${MGMT_PORT} --env-file .env $(APP_NAME)/$(CONTAINER_NAME):$(APP_VERSION)

# ---------------------------------------------------------
# Stop
# ---------------------------------------------------------

.PHONY: stop
.SILENT: stop

stop:
	docker container stop $(CONTAINER_NAME)
	docker container rm $(CONTAINER_NAME)
