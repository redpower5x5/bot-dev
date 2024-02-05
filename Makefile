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

.PHONY: dev
dev:
	docker compose -f docker/docker-compose.yaml up -d --build

.PHONY: run
run:
	python3 src/main.py