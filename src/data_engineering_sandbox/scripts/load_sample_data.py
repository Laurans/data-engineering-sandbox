import click
import subprocess
from loguru import logger
from data_engineering_sandbox.const import DATA_DIR
from data_engineering_sandbox.connectors import get_values_mongo_env
import shlex
from pathlib import Path


def get_samples_sub_directories():
    directories = [x for x in DATA_DIR.iterdir() if x.is_dir() and "sample" in x.name]
    return directories


@click.group()
def cli():
    pass


@cli.command()
def postgres():
    logger.info("Load sample data into postgres database")


@cli.command()
@click.option("--container_data", default="/opt/data")
def mongodb(container_data):
    logger.info("Load sample data into mango database")
    container_datadir = Path(container_data)

    for directory in get_samples_sub_directories():
        for data_file in directory.iterdir():
            data_file = container_datadir / data_file.relative_to(DATA_DIR)
            cmd_part1 = "nerdctl exec data-engineering-sandbox_mongodb_1"
            (
                database_host,
                database_port,
                database_username,
                database_password,
                _,
            ) = get_values_mongo_env()

            cmd_part2 = (
                f"mongoimport --drop --host {database_host} --port {database_port} "
                f"--db {directory.name} --collection {data_file.name} "
                f"--file {data_file} "
                "--authenticationDatabase admin "
                f"-u {database_username} -p {database_password}"
            )
            command_line = cmd_part1 + " " + cmd_part2
            args = shlex.split(command_line)
            output = subprocess.run(args, capture_output=True)
            logger.debug(output.stderr)


if __name__ == "__main__":
    cli()
