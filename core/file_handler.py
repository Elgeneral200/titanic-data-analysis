import os
import pandas as pd
import sqlite3
from pandas import DataFrame


def read_csv(path) -> DataFrame:
    return pd.read_csv(path)


def write_csv(df: DataFrame, path: str, index: bool = False) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=index)


def read_excel(path) -> DataFrame:
    return pd.read_excel(path)


def read_json(path) -> DataFrame:
    return pd.read_json(path)


def read_sqlite(db_path, table_name: str) -> DataFrame:
    with sqlite3.connect(db_path) as conn:
        return pd.read_sql_query(f"SELECT * FROM {table_name}", conn)