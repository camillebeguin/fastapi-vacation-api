.ONESHELL:

CONTAINER_EXECUTOR = docker exec -w /wl/app worklife-test-api

# Deployment
.PHONY: up
up:
	 docker compose -f ./docker-compose.yml up -d
.PHONY: down
down:
	 docker compose -f ./docker-compose.yml down -v

.PHONY: build
build:
	docker compose -f docker-compose.yml build

# DB
.PHONY: create-db
create-db:
	docker exec worklife-test-db psql -U dev -d postgres -f /scripts/create_db.sql -v db="worklife_test_db"

.PHONY: recreate-db
recreate-db:
	docker exec worklife-test-db psql -U dev -d postgres -f /scripts/recreate_db.sql -v db="worklife_test_db"

.PHONY: downgrade-db
downgrade-db:
	$(CONTAINER_EXECUTOR) alembic downgrade -1

.PHONY: migrate-db
migrate-db:
	$(CONTAINER_EXECUTOR) alembic upgrade head

.PHONY: autogenerate-migration
autogenerate-migration:
	$(CONTAINER_EXECUTOR) alembic revision --autogenerate -m $(revision_message)
