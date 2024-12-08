import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def feature_distribution_by_target(df, feature, target, directory=None):
    """Plots the distribution of a feature segmented by each category of the target variable.

  Args:
    df: The DataFrame containing the data.
    feature: The name of the feature to be plotted.
    target: The name of the target variable.
  """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input data must be a pandas DataFrame.")
    columns = df.columns.tolist()
    if feature not in columns:
        raise TypeError("Selected feature does not exists.")
    if target not in columns:
        raise TypeError("Selected target does not exists.")

    sns.displot(data=df, x=feature, hue=target, kind='kde', fill=True)
    plt.title(f'Distribution of {feature} by {target} categories')
    plt.xlabel(feature)
    plt.ylabel("Probability Density")

    if directory:
        plt.savefig(f"{directory}/{feature}_by_{target}.png", bbox_inches='tight')
    else:
        plt.show()
    plt.close()


def save_all_distributions(df, directory):
    """Plots the distribution of each feature by each target.

    Args:
        df: The DataFrame containing the data.
    """
    for feature in df.select_dtypes(include=['number']):
        for target in df.select_dtypes(exclude=['number']):
            if target != feature:
                feature_distribution_by_target(df, feature, target, directory)
