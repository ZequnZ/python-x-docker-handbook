SHELL=/bin/bash
tag=pydocker

build:
	docker build -t python-x-docker:$(tag) .

rm:
	docker rm $$(docker ps -aq -f "name=$(tag)")

run:
	echo $$(docker ps -aq -f "name=$(tag)")
	# remove the container if existing
	if [ -z $$(docker ps -aq -f "name=$(tag)") ]; \
	then \
		echo 'not find'; \
	else \
		echo 'find'; \
		make -k rm; \
	fi
	docker run --name $(tag) python-x-docker:$(tag) 
