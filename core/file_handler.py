# core/file_handler.py
"""
File Handler Module

Functions for reading various file formats including CSV, Excel, JSON, and SQLite.
All functions return pandas DataFrames for consistent data processing.

Author: Data Cleaning Tool Team
Version: 2.5.2
"""

from __future__ import annotations

import os
import sqlite3
import tempfile
from typing import IO, Union

import pandas as pd
from pandas import DataFrame


def read_csv(path_or_buffer: Union[str, IO[bytes], IO[str]]) -> DataFrame:
    try:
        return pd.read_csv(path_or_buffer)
    except Exception as e:
        raise ValueError(f"Error reading CSV file: {str(e)}") from e


def read_excel(path_or_buffer: Union[str, IO[bytes]]) -> DataFrame:
    try:
        return pd.read_excel(path_or_buffer)
    except Exception as e:
        raise ValueError(f"Error reading Excel file: {str(e)}") from e


def read_json(path_or_buffer: Union[str, IO[str], IO[bytes]]) -> DataFrame:
    try:
        return pd.read_json(path_or_buffer)
    except Exception as e:
        raise ValueError(f"Error reading JSON file: {str(e)}") from e


def read_sqlite(db_source: Union[str, IO[bytes]], table_name: str) -> DataFrame:
    try:
        if isinstance(db_source, str) and os.path.exists(db_source):
            with sqlite3.connect(db_source) as conn:
                return pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
        if hasattr(db_source, "read"):
            try: db_source.seek(0)
            except Exception: pass
            with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
                tmp.write(db_source.read()); tmp_path = tmp.name
            try:
                with sqlite3.connect(tmp_path) as conn:
                    df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
                return df
            finally:
                try: os.remove(tmp_path)
                except OSError: pass
        raise ValueError("Invalid SQLite source provided. Must be a path or file-like object.")
    except sqlite3.Error as e:
        raise ValueError(f"Error reading SQLite database: {str(e)}") from e
    except Exception as e:
        raise ValueError(f"Unexpected error: {str(e)}") from e


def validate_file_format(file_path: str) -> bool:
    supported_extensions = [".csv", ".xlsx", ".xls", ".json", ".db"]
    return any(file_path.lower().endswith(ext) for ext in supported_extensions)


def get_file_info(df: DataFrame) -> dict:
    return {
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "memory_usage_mb": float(df.memory_usage(deep=True).sum() / (1024 * 1024)),
        "missing_values": int(df.isna().sum().sum()),
        "data_types": {k: str(v) for k, v in df.dtypes.to_dict().items()},
    }