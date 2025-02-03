# Define directories
BASE_DIR := $(shell pwd)
DOCKER_DIR := $(BASE_DIR)/infra/docker
COMPOSE_DIR := $(BASE_DIR)/infra/compose

# Docker Compose files
COMPOSE_DEV := $(COMPOSE_DIR)/compose.dev.yml
COMPOSE_PROD := $(COMPOSE_DIR)/compose.prod.yml
COMPOSE_LOCAL := $(COMPOSE_DIR)/compose.local.yml

# Environment file
ENV_FILE := $(BASE_DIR)/.env

# Project name
PROJECT_NAME := social_media_project

# Docker Compose command shortcuts with env file
DOCKER_COMPOSE_BASE := docker compose -p $(PROJECT_NAME) --env-file $(ENV_FILE)
DOCKER_COMPOSE_DEV := $(DOCKER_COMPOSE_BASE) -f $(COMPOSE_DEV)
DOCKER_COMPOSE_PROD := $(DOCKER_COMPOSE_BASE) -f $(COMPOSE_PROD)
DOCKER_COMPOSE_LOCAL := $(DOCKER_COMPOSE_BASE) -f $(COMPOSE_LOCAL)

# Docker image details
DOCKER_IMAGE := dxhltd/django-api
DOCKERFILE_PROD := $(DOCKER_DIR)/Dockerfile.prod
DOCKERFILE_LOCAL := $(DOCKER_DIR)/Dockerfile.local
DOCKER_IMAGE_TAG ?= local

# Colors for pretty output
CYAN := \033[36m
GREEN := \033[32m
YELLOW := \033[33m
RESET := \033[0m

# Targets
.PHONY: all dev prod local stop stop-all clean clean-all logs rebuild push push-local test shell help check-env ps update-deps

# Default target
all: help

# Check if .env file exists
check-env:
	@if [ ! -f $(ENV_FILE) ]; then \
		echo "$(YELLOW)Warning: $(ENV_FILE) does not exist$(RESET)"; \
		exit 1; \
	fi

# Development environment
dev: check-env
	@echo "$(CYAN)Starting development environment...$(RESET)"
	@$(DOCKER_COMPOSE_DEV) up --build

# Stop services
define stop_service
	@echo "$(CYAN)Stopping $(1) services...$(RESET)"
	@$(2) down
endef

stop-dev: check-env
	$(call stop_service,development,$(DOCKER_COMPOSE_DEV))

# Clean up Docker volumes
define clean_service
	@echo "$(YELLOW)Cleaning $(1) environment...$(RESET)"
	@$(2) down -v
endef

clean-dev: check-env
	$(call clean_service,development,$(DOCKER_COMPOSE_DEV))

clean-all: clean-dev clean-prod clean-local
	@echo "$(GREEN)All environments cleaned$(RESET)"

# View logs
logs: check-env
	@$(DOCKER_COMPOSE_PROD) logs -f

# Show running containers
ps:
	@echo "$(CYAN)Development containers:$(RESET)"
	@$(DOCKER_COMPOSE_DEV) ps
	@echo "$(CYAN)Production containers:$(RESET)"
	@$(DOCKER_COMPOSE_PROD) ps
	@echo "$(CYAN)Local containers:$(RESET)"
	@$(DOCKER_COMPOSE_LOCAL) ps

# Rebuild images
rebuild: check-env
	@echo "$(CYAN)Rebuilding development images...$(RESET)"
	@$(DOCKER_COMPOSE_DEV) build --no-cache

# Shell access
shell: check-env
	@echo "$(CYAN)Opening shell in django container...$(RESET)"
	@$(DOCKER_COMPOSE_DEV) exec django sh

# Help
help:
	@echo "$(CYAN)Available commands:$(RESET)"
	@echo "  $(GREEN)Environment Management:$(RESET)"
	@echo "    make dev         - Start the development environment"
	@echo "    make prod        - Start the production environment"
	@echo "    make local       - Start the local environment"
	@echo "    make rebuild     - Rebuild development images"
	@echo "  $(GREEN)Service Control:$(RESET)"
	@echo "    make stop-dev    - Stop development services"
	@echo "    make stop-prod   - Stop production services"
	@echo "    make stop-local  - Stop local services"
	@echo "    make stop-all    - Stop all services"
	@echo "    make ps          - Show running containers"
	@echo "  $(GREEN)Cleaning:$(RESET)"
	@echo "    make clean-dev   - Clean development environment"
	@echo "    make clean-prod  - Clean production environment"
	@echo "    make clean-local - Clean local environment"
	@echo "    make clean-all   - Clean all environments"
	@echo "  $(GREEN)Production:$(RESET)"
	@echo "    make logs        - View production logs"
	@echo "    make shell       - Open shell in django container"
	@echo "    make push        - Build and push production image"
	@echo "    make push-local  - Build and push local image"