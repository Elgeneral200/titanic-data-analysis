import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame
import streamlit as st


def plot_missing_heatmap(df: DataFrame) -> None:
    if df.empty:
        return

    fig, ax = plt.subplots(figsize=(12, 6))
    im = ax.imshow(df.isna(), aspect="auto", cmap="viridis")
    plt.colorbar(im, ax=ax, label="Missing (1) / Not Missing (0)")
    ax.set_title("Missing Data Heatmap")
    ax.set_xlabel("Columns")
    ax.set_ylabel("Rows")
    ax.set_xticks(range(len(df.columns)))
    ax.set_xticklabels(df.columns, rotation=90)
    plt.tight_layout()
    st.pyplot(fig)