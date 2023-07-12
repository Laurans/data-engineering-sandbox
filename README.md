# Data Engineering Sandbox

The Data Engineering Sandbox is an environment designed for experimentation with data engineering tools. It provides a pre-configured setup for running data pipelines, working with databases, and performing data transformations.

## Features

- Easy setup and initialization using Python 3.11 and Poetry.
- Local environment variables management with `direnv`.
- Convenient task execution with the `just` command.
- Container management with `nerdctl` (a drop-in replacement for `docker-compose`).

## Prerequisites

Make sure you have the following dependencies installed on your system:

- Python 3.11
- Poetry (https://python-poetry.org/)
- direnv (https://direnv.net/)
- just (https://github.com/casey/just)
- nerdctl (https://github.com/containerd/nerdctl) - can be installed with "Rancher Desktop" (https://rancherdesktop.io/)


## Getting Started

Follow the steps below to set up the Data Engineering Sandbox:

1. Clone this repository:

```shell
git clone <repository-url>
cd data-engineering-sandbox
```

2. Install the project dependencies using Poetry:

```shell
poetry install
```

3. Create a .envrc file in the project root directory and define your local environment variables. Example:

```txt
export POSTGRES_USER="myuser"
export POSTGRES_PASSWORD=mypassword
export POSTGRES_DB=mydatabase
```

4. Enable direnv to load the environment variables automatically:

```shell
direnv allow
```

5. Execute tasks using the just command. Some available tasks include:

- Run tests: just test
- Start containers: just start
- Stop containers: just stop
- Load data into databases: just load-data
- Clean up containers: just clean


# Datasets sources

Datasets comes from this repo [https://github.com/neelabalan/mongodb-sample-dataset](https://github.com/neelabalan/mongodb-sample-dataset). 

In your `./data` folder, you should have
- sample_airbnb
- sample_analytics	
- sample_geospatial	
- sample_mflix		
- sample_supplies		
- sample_training		
- sample_weatherdata

Note: json file are in a special format for mongodb import. So you need to transform it to load them using pandas.