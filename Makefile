VENV_DIR ?= .venv
PYTHON ?= $(VENV_DIR)/bin/python

.PHONY: help ingest search chat up down venv db_clear

help:
	@echo "Targets:"
	@echo "  make ingest  - Run PDF ingestion"
	@echo "  make search  - Run search"
	@echo "  make chat    - Run chat"
	@echo "  make up      - Start docker compose services"
	@echo "  make down    - Stop docker compose services"
	@echo "  make db_clear - Clear database schema and recreate vector extension"

ingest:
	@$(PYTHON) src/ingest.py

search:
	@$(PYTHON) src/search.py

chat:
	@$(PYTHON) src/chat.py

venv:
	@/bin/sh -c "if [ ! -x '$(PYTHON)' ]; then python3 -m venv '$(VENV_DIR)'; fi"
	@$(PYTHON) -m pip install -r requirements.txt

up: venv
	@docker compose up -d

down:
	@docker compose down

db_clear:
	@docker compose exec -T postgres psql -U postgres -d rag -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
	@docker compose exec -T postgres psql -U postgres -d rag -c "CREATE EXTENSION IF NOT EXISTS vector;"
