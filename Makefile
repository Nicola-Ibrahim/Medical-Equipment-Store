.PHONY: superuser
superuser:
	poetry run python -m core.manage createsuperuser

.PHONY: lint
lint:
	poetry run pre-commit run --all-files


.PHONY: migrations
migrations:
	poetry run python -m core.manage makemigrations

.PHONY: migrate
migrate:
	poetry run python -m core.manage migrate

.PHONY: run-server
run-server:
	poetry run python -m core.manage runserver 127.0.0.1:8000


.PHONY: install
install:
	poetry install


.PHONY: install-pre-commit
update-pre-commit:
	poetry run pre-commit uninstall
	poetry run pre-commit install

.PHONY: update
update:	install migrate	install-pre-commit
