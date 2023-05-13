# justfile
ENV_FILE := '.envrc'

default: 
  @just --list

# Run tests
test:
  poetry run pytest

# Start containers
start: && pg_isready
  nerdctl compose up -d --env-file {{ENV_FILE}}

# Check is pg is ready before continuing
@pg_isready:
  sleep 1
  until `nerdctl exec data-engineering-sandbox_postgres_1 pg_isready -q`; do echo "Waiting for postgres"; sleep 2; done

# Initialize the database
init-db:
  poetry run python src/db_init.py


# Stop containers
stop:
  nerdctl compose down

# Load data into databases
load-data:
  # Add your data loading commands here
  echo ""

# Clean up containers
clean:
  nerdctl compose down -v --env-file {{ENV_FILE}}
