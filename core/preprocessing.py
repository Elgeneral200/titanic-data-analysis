import pandas as pd
from typing import Union, Literal, Dict, Any
from pandas import DataFrame


def check_missing_values(df: DataFrame, percent: bool = False) -> pd.Series:
    return df.isna().mean() * 100 if percent else df.isna().sum()


def process_missing_values(
    df: DataFrame,
    strategy: Literal["drop", "mean", "median", "mode", "constant"],
    columns: Union[list[str], None] = None,
    fill_value: Any = None
) -> DataFrame:
    df_copy = df.copy()
    target_cols = columns if columns else df.columns

    if strategy == "drop":
        return df_copy.dropna(subset=target_cols)

    for col in target_cols:
        if strategy in ["mean", "median"]:
            if pd.api.types.is_numeric_dtype(df_copy[col]):
                value = df_copy[col].mean() if strategy == "mean" else df_copy[col].median()
                df_copy[col] = df_copy[col].fillna(value)
        elif strategy == "mode":
            mode_series = df_copy[col].mode()
            if not mode_series.empty:
                df_copy[col] = df_copy[col].fillna(mode_series[0])
        elif strategy == "constant":
            if fill_value is None:
                raise ValueError("Fill value required for 'constant'")
            df_copy[col] = df_copy[col].fillna(fill_value)
        else:
            raise ValueError(f"Invalid strategy: {strategy}")
    return df_copy


def convert_data_type(df: DataFrame, column: str, dtype: str) -> DataFrame:
    df_copy = df.copy()
    try:
        df_copy[column] = df_copy[column].astype(dtype)
    except Exception as e:
        raise ValueError(f"Conversion error: {e}")
    return df_copy