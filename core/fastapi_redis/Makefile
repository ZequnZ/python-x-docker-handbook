install-packages:
	pip install -r requirements/dev.txt
	pip install -r requirements/app.txt

linter:
	black ./src --check
	ruff check ./src

formatter:
	black ./src -v
	ruff check ./src --fix
	isort ./src -v

checker:
	mypy ./src --check-untyped-defs

run-app:
	docker-compose  -f ./docker-compose-server.yaml up

model-training:
	docker-compose  -f docker-compose-model-training.yaml up

jupyter:
	jupyter-lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root
