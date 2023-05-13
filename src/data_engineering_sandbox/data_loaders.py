from pathlib import Path
from .connectors import PostgresConnector
import pandas as pd
from sqlalchemy import text, TextClause
from .string_utils import sanitize_sql_identifier
from typing import Literal


class FromCSVtoPostgres:
    def __init__(self, csv_file: str | Path, table_name: str) -> None:
        self.table_name = table_name
        self.csv_file = csv_file
        self.postgres_connector = PostgresConnector()

        # Read the csv
        df = pd.read_csv(self.csv_file, nrows=1)

        # Infer the column names and sanitize
        self.column_names = [
            sanitize_sql_identifier(name) for name in df.columns.tolist()
        ]

    def populate_table_from_csv(
        self, if_exists: Literal["fail", "replace", "append"] = "append"
    ) -> int:
        data = pd.read_csv(self.csv_file, names=self.column_names, header=0)

        # Insert the data into the SQL table
        total_inserted = data.to_sql(
            self.table_name,
            self.postgres_connector.engine,
            if_exists=if_exists,
            index=False,
            chunksize=300,
            method="multi",
        )

        return total_inserted
