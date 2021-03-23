# How to develop your Python code interactively with Docker

In this chapter, we will see how to develop your Python code interactively with Docker,
by utilizing the **bind mounts**. 

Long story short, bind mounts allows your container to access some directories on your local machine, instead of keeping its own independent filesystem. 

This enables you to use the development environment set by Docker to develop your code and
can make sure that all the changes would be saved on your machine.