SHELL=/bin/bash

build:
	docker-compose  -f ./docker-compose.yml up --build

up:
	docker-compose  -f ./docker-compose.yml up --no-build
	
exec:
	docker exec -it powerful-docker-compose_log_server_1 bash
