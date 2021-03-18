SHELL=/bin/bash

build:
	docker build -t py-x-docker .

run:
	docker run py-x-docker
