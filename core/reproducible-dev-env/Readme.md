# How to set up a reproducible development environment using Docker for Python

In this chapter, we are going to set up a **reproducible development environment** for Python using Docker.

TODO: dockerfile -> image -> container

We will go through the following steps:
1. Prepare the code and dependency
2. Create a *Dockerfile*
3. Build the Docker image and spin up the container

## Prepare the code and dependency
Prepare your python code in [src](./src) and put your dependencies in [requirements.txt](./requirements.txt)  
Here just as an example, I use the code of [sudoku generator]((https://github.com/ZequnZ/CV-based-sudoku-solver).  
You can run the main function to generate a sudoku with different random seed and level:
```python
python main.py -s <ramdom_seed> -l <level>
```

The folder structure is presented as follows:

```
.
├── Dockerfile
├── Makefile
├── requirements.txt (Dependencies)
└── src (Python code folder)
    ├── main.py
    └── sudoku.py

```
## Create a *Dockerfile*
After having the code, next we need to create a *Dockerfile* which contains instructions that can be used to build a Docker container.  
For this example, we only use several essential and useful instructions.   
I will walk the [Dockerfile](./Dockerfile) line by line:  
```
FROM python:3.8.1-slim
```
A Dockerfile must begin with a `FROM` instruction, initializing a new build stage and specifying a **basic image**.  
Here I choose the `python:3.8.1-slim` image.
From name, you may know that the Python version I pick is `3.8.1`.  
There are several variants of Python images. The postfix `-slim` here means that the image only contains **the minimal packages** needed to run Python.   
You can check [here](https://hub.docker.com/_/python) to see all the available options and based on your need, choose the Python base image for your use case. 

```
LABEL Author="ZequnZ" Link="https://github.com/ZequnZ/python-x-docker-handbook"
```
Here I use `LABEL` to add some metadata. You just need to add one or mulitple `<key>=<value>` pairs.

```
WORKDIR  /app
```
`WORKDIR` is used to set the working directory for instructions likes `RUN`, `CMD`, `ENTRYPOINT`, `COPY` and `ADD`.
In this case, the path `/app` will be created and set as default path.

```
COPY requirements.txt /app
```
It is easy to understand this line: copy the file `requirements.txt` to the filesystem of the container at the path `/app`

```
RUN pip install --no-cache-dir -r requirements.txt
```
Now we have the dependency file, next step is to install it. 
The instruction `RUN` enable you to run any commands on top of the current image, in the format of `RUN <command>`.

```
COPY ./src /app
```
We also need to make sure the Python code will be in place.
Again, here we copy all files in the folder `src` to the container under the path `app`.

```
CMD [ "-s", "43", "-l", "70" ]
ENTRYPOINT [ "python", "main.py" ]

```
Finally, we need to define the executable command for the container.
You may notice that in the [hello-world example](https://github.com/ZequnZ/python-x-docker-handbook#an-hello-world-example), we use `CMD` in the end, but here we use `ENTRYPOINT`.  
The difference is that, `CMD` defines the defaults for the container that can be overwritten during the execution: `docker run py-x-docker <command>`.
If you want your container to run the command every time, using `ENTRYPOINT`.

There is another use case to use the combination of `CMD` and `ENTRYPOINT` together, and I would like show to it here.
As mentioned above, `ENTRYPOINT` defines commands that would be run every time running the container,
while commands defined by `CMD` can be overwritten.
We can use `CMD` to specify the default values of arguments and use `ENTRYPOINT` to specify the main commands.

In [main.py](./src/main.py), I define two arguments with default values:
```python
    parser.add_argument("-s", "--seed", type=str, default=42)
    parser.add_argument("-l", "--level", type=int, default=50)
```
In Dockerfile, I use `CMD` to define the default arguments. If you do not specify any commands when executing the container, it is equivalent to run the command:
```
python main.py -s 43 -l 70
```
However, if you want to change the values of the arguments, you can easily overwrite them while executing the container:
```
docker run py-x-docker -s 50 -l 71
```

## Build the Docker image and spin up the container

Next, we will need to build the Docker image from Dockerfile, with the following command:
```
docker build -t python-x-docker:c1 .
```
Using `-t` this images is tagged with name `python-x-docker:c1`.  

To spin up the container, we need to run 
```
docker run python-x-docker:c1 
```
As mentioned above, if we do not specify any arguments here, the defaults defined by `CMD` would be used.
If you want to use different values, you can just specify them in the commands, for example:
```
docker run python-x-docker:c1 -s 50 -l 70
```
Again, I add a [Makefile](./Makefile) to make life easier: 
- Build the Docker container: `make build`  
- Execute the container: `make run`

Using different arguments here is a bit different, you would need to run:
```
make run command='-s 50 -l 70'
```

Finally, after these steps, you will see a sudoku generated and pop up in your terminal.  
What is more interesting is that, the development environment you just created is identical to the one in my laptop.  
Now you can creat a Dockerfile by youself, to support your own development!
