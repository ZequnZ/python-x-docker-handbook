SHELL=/bin/bash

build:
	docker build -t python-x-docker:c3 .

rm:
	docker rm $$(docker ps -aq -f "name=python-x-docker-c2")

run:
	make -k rm
	docker run --name python-x-docker-c3 python-x-docker:c3 

exec:
	docker exec -it python-x-docker-c3 bash

compose-build:
	docker-compose  -f ./docker-log.yml up --build

compose-up:
	docker-compose  -f ./docker-log.yml up --no-build
