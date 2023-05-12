.PHONY: superuser
superuser:
	pipenv run python -m manage makesuperuser

.PHONY: lint
lint:
	pipenv run pre-commit run --all-files


.PHONY: migrations
migrations:
	poetry run python -m src.manage makemigrations

.PHONY: migrate
migrate:
	poetry run python -m src.manage migrate

.PHONY: run-server
run-server:
	poetry run python -m src.manage runserver 127.0.0.1:8000


.PHONY: install
install:
	poetry install


.PHONY: update-pre-commit
update-pre-commit:
	poetry run pre-commit uninstall
	poetry run pre-commit install

.PHONY: update
update: migrations migrate	update-pre-commit


.PHONY: shell
shell:
	pipenv run python -m manage shell_plus

.PHONY: flush-tokens
flush-tokens:
	pipenv run python -m manage flushexpiredtokens

.PHONY: check-deploy
check-deploy:
	pipenv run python -m manage check --deploy


.PHONY: db-graph
db-graph:
	pipenv run python -m manage graph_models -a -g -o lineup_models_visualized.png
