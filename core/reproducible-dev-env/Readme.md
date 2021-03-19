# How to set up a reproducible development environment using Docker container for Python

In this chapter, we are going to set up a **reproducible development environment** for Python using Docker.
We will go through the following steps:
1. Prepare the code and dependency
2. Finish a *Dockerfile*
3. Build the Docker container and execute it

## Prepare the code and dependency
Prepare your python code in [src](./src) and put your dependencies in [requirements.txt](./requirements.txt)  
Here just as an example, I use the code of sudoku generator, which is [another repo](https://github.com/ZequnZ/CV-based-sudoku-solver) of mine.  
You can see the folder structure as follows:

```
.
├── Dockerfile
├── Makefile
├── Readme.md
├── requirements.txt
└── src
    ├── main.py
    └── sudoku.py

```

## Finish a *Dockerfile*

## Build the Docker container and execute it

In the [hello-world example](https://github.com/ZequnZ/python-x-docker-handbook#an-hello-world-example), we tried to use commands to build Dockerfile into a Docker container and execute it.
