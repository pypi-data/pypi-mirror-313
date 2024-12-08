import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def create_correlation_heatmap(df: pd.DataFrame,omit_categorical_data: bool = True,
                               fig_size: tuple[int,int] = (10,10))->None:
    """
    Create a correlation heatmap based on a data frame.

    This function handles data with categorical values by setting properly the 'omit_categorical_data' flag.

    :param df: data frame
    :param omit_categorical_data: whether to omit categorical data or convert it to numerical dummy values
    :param fig_size: size of the figure

    """

    if omit_categorical_data:
        correlation_matrix = df.select_dtypes(include=['number']).corr()
    else:
        categorical_columns = df.select_dtypes(include=['object', 'category']).columns
        correlation_matrix = pd.get_dummies(df, columns=categorical_columns, drop_first=True).corr()
    plt.figure(figsize= fig_size)

    sns.heatmap(correlation_matrix, annot=True, cmap = "coolwarm", vmin=-1, vmax=1)

    plt.title("Correlation heatmap")
    plt.show()