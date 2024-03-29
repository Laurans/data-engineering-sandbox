# justfile
ENV_FILE := '.envrc'

default: 
  @just --list

# Start containers
start-postgres: && pg_isready
  nerdctl compose up -d --env-file {{ENV_FILE}} --profile postgres

start-mongodb:
  nerdctl compose --profile mongodb up -d --env-file {{ENV_FILE}} 

# Check is pg is ready before continuing
@pg_isready:
  sleep 1
  until `nerdctl exec sandbox-postgres pg_isready -q`; do echo "Waiting for postgres"; sleep 2; done

# Clean up containers
clean:
  nerdctl compose down -v --env-file {{ENV_FILE}} --remove-orphans

# Load data into databases
load-sample-data database_name:
  poetry run load_sample_data {{database_name}}

# Run tests
test *parameters:
  poetry run pytest -v {{parameters}}

# Format the code
format:
  black src
  black tests

  isort src
  isort tests

# Apply linting on code
lint: 
  ruff src
  ruff tests

lint-fix:
  ruff src --fix
  ruff tests --fix

# Format then lint the code
format-lint: format lint