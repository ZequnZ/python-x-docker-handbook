# Python x Docker Handbook / Python x Docker 协作指南

[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)  [![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)

![Banner](./asset/banner.png)

In this repo, I will introduce how to use Docker to support Python project/application development
and provide some prototypes that can be used for your development. 
Feel free to fork this repo and create your own Docker container!

## How to use this book 

Just need to install [Python](https://www.python.org/) and [Docker](https://www.docker.com/) and follow this book!

## Content:
[How to set up a reproducible development environment using Docker for Python](./core/reproducible-dev-env)  
**Working on** [How to develop your Python code interactively with Docker](./core/interactively-running)

## An hello world example

If you are new to Docker, you can follow this hello world example to have a first try.

1. Clone this repository `git clone https://github.com/ZequnZ/python-x-docker-handbook.git` 
2. Change your current directory to this repo `cd python-x-docker-handbook`
3. Build the Docker container `docker build -t py-x-docker .`  
4. Execute the container `docker run py-x-docker` 

Then you will see my welcome message.

I also use [Makefile](./Makefile) to make life easier 
so that you do not need to remember the full command:  
- Build the Docker container: `make build`  
- Execute the container: `make run`  

**That is the way to put your Python code into a Docker container**  

It is simple, isn't it? If you want to know more about how to utilize Docker to support your python development, just follow this repo and I will show more interesting use cases!



## TODO

Content：
- how to run your Python code interactively with a Docker container
   - volumn
   - --publish , -p  Publish a container's port(s) to the host
   - docker-compose
- how to dockerize an python application
  - 1 + 2
- The power of docker-compose
  - mocked service

ref:
https://docs.docker.com/language/python/
