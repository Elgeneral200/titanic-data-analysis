import pandas as pd
from typing import Union, Literal, Dict, Any
from pandas import DataFrame


def check_data_types(df: DataFrame) -> pd.Series:
    return df.dtypes


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

    if strategy in ["mean", "median"]:
        for col in target_cols:
            if pd.api.types.is_numeric_dtype(df_copy[col]):
                func = df_copy[col].mean if strategy == "mean" else df_copy[col].median
                df_copy[col] = df_copy[col].fillna(func())
    elif strategy == "mode":
        for col in target_cols:
            mode = df_copy[col].mode()
            if not mode.empty:
                df_copy[col] = df_copy[col].fillna(mode[0])
    elif strategy == "constant":
        if fill_value is None:
            raise ValueError("fill_value is required for constant strategy")
        df_copy[target_cols] = df_copy[target_cols].fillna(fill_value)
    else:
        raise ValueError(f"Unknown strategy: {strategy}")

    return df_copy