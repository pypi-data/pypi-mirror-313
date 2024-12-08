import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats as stats
import seaborn as sns


def visualize_distribution(data, columns, bins=30, save_to_file=None):
    """
    Visualize the distribution of data for each specified column.
    For numeric columns, include histogram, KDE, Q-Q plot, and boxplot.
    For categorical columns, include count plot and percentage distribution.

    Parameters:
    - data (pd.DataFrame): Input data.
    - columns (list of str): List of column names to visualize.
    - bins (int): Number of bins for histogram (numeric only).
    - save_to_file (str or None): File path to save the plots (if specified).
    """
    if not isinstance(data, pd.DataFrame):
        raise TypeError("Input data must be a pandas DataFrame.")

    for column_name in columns:
        if column_name not in data.columns:
            print(f"Column '{column_name}' not found in DataFrame.")
            continue

        values = data[column_name].dropna()

        # Check if the column is categorical or numeric
        if pd.api.types.is_numeric_dtype(values):
            # Numeric distribution visualization
            fig, axs = plt.subplots(1, 3, figsize=(18, 6))
            sns.histplot(values, bins=bins, kde=True, ax=axs[0], color='skyblue')
            axs[0].set_title(f'Distribution of {column_name}')
            axs[0].set_xlabel(column_name)
            axs[0].set_ylabel('Frequency')

            stats.probplot(values, dist="norm", plot=axs[1])
            axs[1].set_title('Q-Q Plot')

            if len(values) <= 5000:
                shapiro_test = stats.shapiro(values)
                p_value = shapiro_test.pvalue
                normal = "Yes" if p_value > 0.05 else "No"
                test_name = "Shapiro-Wilk"
            else:
                ad_test = stats.anderson(values, dist='norm')
                p_value = ad_test.significance_level[np.argmax(ad_test.statistic < ad_test.critical_values)]
                normal = "Yes" if ad_test.statistic < ad_test.critical_values[-1] else "No"
                test_name = "Anderson-Darling"

            sns.boxplot(x=values, ax=axs[2], color='lightcoral')
            axs[2].set_title(f'Boxplot of {column_name}')

            plt.suptitle(
                f'Distribution Analysis of {column_name}\nNormal Distribution: {normal} ({test_name} p = {p_value:.4f})')
            plt.tight_layout()
            plt.subplots_adjust(top=0.85)

        else:
            # Categorical distribution visualization
            fig, ax = plt.subplots(1, 2, figsize=(18, 6))

            # Define a consistent color palette for the unique categories
            unique_categories = values.unique()
            palette = sns.color_palette("viridis", len(unique_categories))
            color_dict = dict(zip(unique_categories, palette))
            order = sorted(unique_categories)  # Define order for consistent sorting

            # Count plot for frequencies with hue and legend disabled
            sns.countplot(x=values, ax=ax[0], hue=values, palette=color_dict, order=order, dodge=False, legend=False)
            ax[0].set_title(f'Count of Categories in {column_name}')
            ax[0].set_xlabel(column_name)
            ax[0].set_ylabel('Count')

            # Adding value labels on the count plot
            for p in ax[0].patches:
                ax[0].annotate(f'{int(p.get_height())}',
                               (p.get_x() + p.get_width() / 2., p.get_height()),
                               ha='center', va='baseline', fontsize=10, color='black', xytext=(0, 5),
                               textcoords='offset points')

            # Percentage plot with consistent colors, using `hue` to ensure order
            value_counts = values.value_counts(normalize=True).reindex(order) * 100
            sns.barplot(x=value_counts.index, y=value_counts.values, ax=ax[1], hue=value_counts.index,
                        palette=color_dict, dodge=False, legend=False)
            ax[1].set_title(f'Percentage Distribution of {column_name}')
            ax[1].set_xlabel(column_name)
            ax[1].set_ylabel('Percentage (%)')

            # Adding percentage labels on the percentage plot
            for p in ax[1].patches:
                ax[1].annotate(f'{p.get_height():.1f}%',
                               (p.get_x() + p.get_width() / 2., p.get_height()),
                               ha='center', va='baseline', fontsize=10, color='black', xytext=(0, 5),
                               textcoords='offset points')

            plt.suptitle(f'Distribution Analysis of Categorical Column: {column_name}')
            plt.tight_layout()

        # Save or show plot
        if save_to_file:
            name = f"visualize_distribution_{column_name}.png"
            plt.savefig(f"{save_to_file}/{name}")
            print(f"Plot for '{column_name}' saved as {name} in {save_to_file}.")
        else:
            plt.show()
        plt.close(fig)
