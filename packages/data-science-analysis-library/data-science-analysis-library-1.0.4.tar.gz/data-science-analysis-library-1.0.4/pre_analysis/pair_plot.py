import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def pair_plot(df: pd.DataFrame, exclude_categorical: bool = True) -> None:
    """
    Function that create a pair plot between all of numerical values. If `exclude_categorical` flag is set to `True` then
    the function also includes categorical values as different hues.
    Args:
        df: DataFrame to create a pair plot from
        exclude_categorical: Flag to exclude categorical values from plot

    """
    if exclude_categorical:
        data = df.copy(True).select_dtypes(include='number')
        sns.pairplot(data)
        plt.show()
    else:
        for category in df.select_dtypes(include=['object', 'category']).columns:
            sns.pairplot(df, hue=category)
            plt.show()
