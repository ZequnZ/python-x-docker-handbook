SHELL=/bin/bash

build:
	docker build -t python-x-docker:c2 .

rm:
	docker rm $$(docker ps -aq -f "name=python-x-docker-c2")

run:
	make -k rm
	docker run --name python-x-docker-c2 -p 0.0.0.0:8998:8999 -v $$(pwd)/:/app python-x-docker:c2 

exec:
	docker exec -it python-x-docker-c2 bash

compose-build:
	docker-compose  -f ./docker-notebook.yml up --build

compose-up:
	docker-compose  -f ./docker-notebook.yml up --no-build
