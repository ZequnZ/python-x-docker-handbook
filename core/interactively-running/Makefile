SHELL=/bin/bash

build:
	docker build -t python-x-docker:c2 .

rm:
	docker rm $$(docker ps -aq -f "name=python-x-docker-c2")

run:
	docker run -it -p 8999:8999 --name python-x-docker-c2 -v $$(pwd)/src:/app python-x-docker:c2

exec:
	docker exec -it python-x-docker-c2 bash
