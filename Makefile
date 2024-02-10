project_dir := .
bot_dir := ./src/bot
translations_dir := ./translations

.PHONY: i18n
i18n:
	pybabel extract --input-dirs='$(bot_dir)' -o '$(translations_dir)/messages.pot'
	pybabel init -i $(translations_dir)/messages.pot -d $(translations_dir) -D messages -l ru
	pybabel init -i $(translations_dir)/messages.pot -d $(translations_dir) -D messages -l en

.PHONY: i18n-compile
i18n-compile:
	pybabel compile -d $(translations_dir) -D messages

.PHONY: prod-build
prod-build:
	docker compose -f docker/docker-compose-prod.yaml up -d --build

.PHONY: dev-db
dev-db:
	docker compose -f docker/docker-compose-dev.yaml up -d postgres
.PHONY: logs
logs:
	docker compose -f docker/docker-compose.yaml logs -f

.PHONY: run
run:
	python3 src/main.py