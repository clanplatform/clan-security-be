.PHONY: up down build test lint format clean logs ps

DOCKER_COMPOSE = docker-compose
SERVICES = $(shell ls services/)

up:
	$(DOCKER_COMPOSE) up -d

down:
	$(DOCKER_COMPOSE) down

build:
	$(DOCKER_COMPOSE) build

test:
	@for svc in $(SERVICES); do \
		echo "Testing $$svc..."; \
		cd services/$$svc && python -m pytest tests/ -v && cd ../..; \
	done

lint:
	@for svc in $(SERVICES); do \
		cd services/$$svc && python -m ruff check app/ && cd ../..; \
	done

format:
	@for svc in $(SERVICES); do \
		cd services/$$svc && python -m ruff format app/ && cd ../..; \
	done

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null; \
	find . -type f -name "*.pyc" -delete

logs:
	$(DOCKER_COMPOSE) logs -f

ps:
	$(DOCKER_COMPOSE) ps

install-dev:
	@for svc in $(SERVICES); do \
		echo "Installing $$svc..."; \
		cd services/$$svc && pip install -r requirements.txt && cd ../..; \
	done
