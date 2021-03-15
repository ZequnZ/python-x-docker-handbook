SHELL=/bin/bash
command='bash'

build:
	docker build -t py-docker .

run:
	docker run --name py-docker -itd py-docker $(command)

exec:
	docker exec -it py-docker $(command)

