import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd


def plot_missing_heatmap(df: pd.DataFrame) -> None:
    if df.empty:
        st.warning("Empty dataframe")
        return
    fig, ax = plt.subplots(figsize=(12, 6))
    im = ax.imshow(df.isna(), aspect="auto", cmap="viridis")
    plt.colorbar(im, ax=ax, label="Missing (1) / Present (0)")
    ax.set_title("Missing Value Heatmap")
    ax.set_xlabel("Columns")
    ax.set_ylabel("Rows")
    ax.set_xticks(range(len(df.columns)))
    ax.set_xticklabels(df.columns, rotation=90)
    st.pyplot(fig)


def plot_missing_bar(df: pd.DataFrame) -> None:
    na_percent = df.isna().mean() * 100
    na_percent = na_percent[na_percent > 0]

    if na_percent.empty:
        st.info("No missing data found.")
        return

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.barh(na_percent.index, na_percent.values, color='tomato')
    ax.set_xlabel("Missing (%)")
    ax.set_title("Missing Values by Column")
    st.pyplot(fig)


def plot_correlation(df: pd.DataFrame) -> None:
    num_df = df.select_dtypes("number")
    if num_df.empty:
        st.warning("No numeric columns.")
        return
    corr = num_df.corr()
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.imshow(corr, cmap="coolwarm", interpolation="none")
    ax.set_title("Correlation Matrix")
    cbar = fig.colorbar(ax.imshow(corr), ax=ax)
    ax.set_xticks(range(len(corr.columns)))
    ax.set_xticklabels(corr.columns, rotation=90)
    ax.set_yticks(range(len(corr.index)))
    ax.set_yticklabels(corr.index)
    st.pyplot(fig)


def plot_distribution(df: pd.DataFrame, column: str) -> None:
    if column not in df.columns:
        st.error("Column not found.")
        return
    fig, ax = plt.subplots()
    df[column].dropna().plot(kind='hist', bins=30, ax=ax, color="skyblue", edgecolor="black")
    ax.set_title(f"Distribution of '{column}'")
    ax.set_xlabel(column)
    st.pyplot(fig)