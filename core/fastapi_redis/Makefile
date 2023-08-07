install-dependency:
	poetry install

activate-virtualenv:
	poetry shell

linter:
	poetry run black ./src --check
	poetry run ruff check ./src

formatter:
	poetry run black ./src -v
	poetry run ruff check ./src --fix
	poetry run isort ./src -v

checker:
	poetry run mypy ./src --check-untyped-defs

rebuild-app:
	docker-compose  -f ./docker-compose-server.yaml up --build

run-app:
	docker-compose  -f ./docker-compose-server.yaml up

model-training:
	docker-compose  -f docker-compose-model-training.yaml up

jupyter:
	jupyter-lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root
