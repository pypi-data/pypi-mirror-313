import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def categorical_value_count_plot(df: pd.DataFrame, fig_size: tuple[float] = (10, 6)) -> None:
    """
    Function that plots the count values of each of the category in the given DataFrame.

    Args:
        df: DataFrame to plot categorical values from
        fig_size: Figure size of the resulting subplots all shown in one image

    """
    categorical_columns = df.select_dtypes(include=['object', 'category']).columns
    fig,axes = plt.subplots(len(categorical_columns),1,figsize=(fig_size[0],fig_size[1] * len(categorical_columns)))

    for i, column in enumerate(categorical_columns):
        sns.countplot(x=column,data=df,ax=axes[i])
        axes[i].set_title(f"Count of Values in {column}")
        axes[i].set_ylabel("Count")
        axes[i].set_xlabel(column)

    plt.show()