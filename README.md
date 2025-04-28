# Project Setup and Execution Guide

## Prerequisites

### 0. Download Docker Desktop
Ensure you have Docker Desktop installed on your machine. You can download it from [Docker's official website](https://www.docker.com/products/docker-desktop/).

## Building and Running the Docker Environment

### 1. Build the Docker Image
Navigate to the project root directory in your terminal and build the Docker image using the following command:
```
docker build -t my-fortran-env .
```

### 2. Run the Docker Container
In the project root directory, run the Docker container. This command will start the container and mount the `app` directory, allowing you to execute Python code within the Docker environment:

```
docker run -it --rm -v ./app:/app my-fortran-env bash
```

If you are in a windows environment, you may need to specify the absolute path instead of an absolute path, so the code above would be modified to:

```
docker run -it --rm -v absolute/path/to/app:/app my-fortran-env bash
```

Also, you will want to create a "data" folder within your "app" folder (as the python files are currently written) that has the netCDF files you want to convert.

## Executing Python Scripts

### 3. Generate Intermediate Data Format
Inside the Docker container, run the Python script to generate the intermediate data format:
```
python netcdf2intermediate.py
```

### 4. Read the Generated Intermediate File
After generating the intermediate file, you can read it using the same Python library:
```
python readthefile.py
```

## Exiting and Re-running the Docker Container

### 5. Exit the Docker Container
To exit the Docker container, type the following command. The container will be deleted automatically:

```
exit
```


### 6. Re-run the Docker Container
If you need to run the Docker container again and already have the Docker image built, repeat steps 2 to 5.
