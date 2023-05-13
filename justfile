# justfile
ENV_FILE := '.envrc'

default: 
  @just --list

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

# Clean up containers
clean:
  nerdctl compose down -v --env-file {{ENV_FILE}}

# Load data into databases
load-data:
  # Add your data loading commands here
  echo ""

# Download books dataset in data folder from Kaggle
download-books:
   kaggle datasets download -p data/ --unzip  ishikajohari/best-books-10k-multi-genre-data

# Run tests
test *parameters:
  poetry run pytest -v {{parameters}}

# Format the code
format:
  black src
  isort src

# Apply linting on code
lint: 
  ruff src

# Format then lint the code
format-lint: format lint

debug_justfile:
  echo ${POSTGRES_DB}