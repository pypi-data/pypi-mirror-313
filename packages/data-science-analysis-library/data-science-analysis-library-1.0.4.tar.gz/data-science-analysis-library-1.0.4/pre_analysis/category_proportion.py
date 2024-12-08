import pandas as pd
import matplotlib.pyplot as plt


def category_proportion_pie(df, column, title=None, filepath=None, n=None, include_others=True):
    """
    Displays the proportion of the top `n` categories within a categorical feature using a pie chart.

    Parameters:
    - df: DataFrame containing the data.
    - column: The categorical column to visualize.
    - title: Title of the chart. If None, a default title is used.
    - filepath: Path to save the plot. If None, the plot is not saved.
    - n: Number of most popular categories to display.
    - include_others: Whether to include "Others" category if `n` is provided.
    """
    if column not in df.columns:
        raise ValueError(f"The column '{column}' is not in the DataFrame.")

    category_counts = df[column].value_counts()

    if n is not None and n < len(category_counts):
        top_categories = category_counts[:n]
        if include_others:
            others_count = category_counts[n:].sum()
            category_counts = pd.concat([top_categories, pd.Series({'Others': others_count})])
        else:
            category_counts = top_categories

    total = category_counts.sum()
    proportions = category_counts / total * 100

    labels = [f"'{cat}' ({count} | {proportion:.1f}%)"
              for cat, count, proportion in zip(category_counts.index, category_counts, proportions)]

    plt.figure(figsize=(8, 8))
    plt.pie(proportions, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.title(title if title else f"Proportions of Categories in '{column}'")
    plt.axis('equal')

    if filepath:
        plt.savefig(filepath)
    plt.show()


def category_proportion_bar(df, column, title=None, filepath=None, n=None, include_others=True, add_labels=False):
    """
    Displays the proportion of the top `n` categories within a categorical feature using a bar chart.

    Parameters:
    - df: DataFrame containing the data.
    - column: The categorical column to visualize.
    - title: Title of the chart. If None, a default title is used.
    - filepath: Path to save the plot. If None, the plot is not saved.
    - n: Number of most popular categories to display.
    - include_others: Whether to include "Others" category if `n` is provided.
    """
    if column not in df.columns:
        raise ValueError(f"The column '{column}' is not in the DataFrame.")

    category_counts = df[column].value_counts()

    if n is not None and n < len(category_counts):
        top_categories = category_counts[:n]
        if include_others:
            others_count = category_counts[n:].sum()
            category_counts = pd.concat([top_categories, pd.Series({'Others': others_count})])
        else:
            category_counts = top_categories

    total = category_counts.sum()
    proportions = category_counts / total * 100

    x_labels = category_counts.index.astype(str)

    plt.figure(figsize=(10, 6))
    plt.bar(x_labels, proportions, color='skyblue')
    plt.xlabel('Categories')
    plt.ylabel('Percentage of Occurrences')
    plt.title(title if title else f"Proportions of Categories in '{column}'")
    plt.xticks(rotation=45)

    if add_labels:
        for i, proportion in enumerate(proportions):
            plt.text(i, proportion + 0.5, f"{proportion:.1f}%", ha='center', fontsize=10)

    if filepath:
        plt.savefig(filepath)
    plt.show()
