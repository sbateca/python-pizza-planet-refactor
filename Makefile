override SHELL := /bin/bash

.PHONY: help
help:
	@echo 'Usage:'
	@echo '  make [target] ...'
	@echo
	@echo 'Targets:'
	@grep --no-filename -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
	 sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


.PHONY: init_db
init_db: ## Init db and populate with faker data.
	python manage.py db init && \
	python manage.py db migrate && \
	python manage.py db upgrade


.PHONY: build
build: ## build a docker image for api and ui
	docker-compose build


.PHONY: run
run: ## start docker containers
	docker-compose up -d


.PHONY: stop
stop: ## stop docker containers
	docker-compose stop


.PHONY: run_local
run_local: ## run api locally
	python manage.py run


.PHONY: test
test: ## run python api test
	pytest


.PHONY: populate_db
populate_db: ## run script to populate database
	python populate_db.py
