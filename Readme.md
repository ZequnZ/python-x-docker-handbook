# Python docker container

__Created at 15/02/2020__

Goal:

- Practice how to build up a Docker container for Python
- Uuderstand the components of a Dockerfile.
- Test how to run a python project in a docker container

## Install and how to run the container

1. Install _Docker_
2. Clone this repository `git clone https://github.com/ZequnZ/py-docker.git`
3. Build the Docker container `docker Build -t zequnz/py-docker:<version> <DockerfilePath>`
4. Run the container `docker run -itd zequn/py-docker:<version>` and get the containerID.
5. Execute the container `docker exec -it <containerID> <command>`

## Notes

### How to run jupyter notebook in the container

1. Bind a port when running the Docker container and get the containerID
   `docker run -itd -p <hostPort>:<containerPort> zequn/py-docker:<version>`
2. Execute the container `docker exec -it <containerID> bash`
3. Inside the contain launch the notebook assigning the port we just bind:
   `jupyter notebook --ip 0.0.0.0 --port <containerPort> --no-brower --allow-root`
4. Then open the jupyter notebook link on the browser.
   **Notice**
   It would be convenient to use the same _hostPort_ and _containerPort_, otherwise when open the jupyter notebook link, you may need to modify the port from _containerPort_ to _hostPort_.

## How to run docker volume for the container

1. Add the option when running the container
   `docker run -itp -p <hostPort>:<containerPort> -v $(pwd)/<VOLUME-FOLDER>:<CONTAINER-PATH> zequn/py-docker:<version>`

## TODO

- [x] Understand how to save jupyter notebooks from docker container to local machine: **Docker volume**
- [ ] Add more important / useful python packages to the requirements.txt
- [ ] Think & learn how to add a selection menu when running the docker container

## Changelog

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)

## Current version [0.0.5] - 2020-02-17

## Added

- gitignore file

## Changed

- Add a instructions in the Readme: _How to run docker volume for the container_

## [0.0.4] - 2020-02-16

### Added

- Add instructions in the Readme: _Install and how to run the container_ and _How to run jupyter notebook in the container_

### Changed

- Comment one line in the Dockerfile as now we don't have folder src yet
- In the Dockerfile, use 'LABEL' instead of deprecated 'MAINTAINER'

## [0.0.3] - 2020-02-15

### Changed

- Fix a bug in the Dockerfile

## [0.0.2] - 2020-02-15

### Added

- Create requirements.txt
- Create Dockerfile
- Create PR template

## [0.0.1] - 2020-02-15

### Added

- Create this repository
- Add Readme
