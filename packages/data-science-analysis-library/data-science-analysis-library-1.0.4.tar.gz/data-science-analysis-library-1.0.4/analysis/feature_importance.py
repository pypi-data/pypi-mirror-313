import random

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats as stats
import seaborn as sns
import xgboost as xgb
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from tqdm import tqdm


def feature_importance(
        X,
        y,
        num_random_features=5,
        num_models=3,
        random_state=42,
        top_n=20,
        verbose=True
):
    """
    Assess feature importance and model performance as the number of features increases.

    This function trains multiple XGBoost models with different parameters, adds random noise features,
    and aggregates feature importances based on their ranking across models. Additionally, it assigns
    points to features based on how many random features they rank above, enhancing the robustness of
    the feature importance assessment.

    Parameters:
    - X: pandas DataFrame, feature set.
    - y: pandas Series or array-like, target variable.
    - num_random_features: int, number of random (noise) features to add (default=5).
    - num_models: int, number of XGBoost models to train with different parameters for aggregation and mean Gini calculation (default=3).
    - random_state: int, seed for reproducibility (default=42).
    - top_n: int, number of top features to display in the feature ranking plot (default=20).
    - verbose: bool, whether to print progress messages (default=True).

    Returns:
    - None. Displays two plots:
        1. Mean Gini vs. Number of Features
        2. Aggregated Feature Ranking
    """
    # Set random seed for reproducibility
    np.random.seed(random_state)
    random.seed(random_state)

    # 1. Add Random Features
    X_augmented = X.copy()
    random_feature_names = []
    for i in range(num_random_features):
        rand_feature = f"rand_feat_{i + 1}"
        X_augmented[rand_feature] = np.random.randn(X.shape[0])
        random_feature_names.append(rand_feature)

    if verbose:
        print(f"Added {num_random_features} random features: {random_feature_names}")

    # Encode categorical variables if any
    X_encoded = pd.get_dummies(X_augmented, drop_first=True)

    if verbose:
        print("Encoded categorical variables (if any).")
        print(f"Total features after encoding: {X_encoded.shape[1]}")

    # 2. Split the data
    X_train, X_test, y_train, y_test = train_test_split(
        X_encoded, y, test_size=0.3, random_state=random_state, stratify=y
    )

    if verbose:
        print("\nData split into train and test sets.")
        print(f"Training set size: {X_train.shape[0]} samples")
        print(f"Test set size: {X_test.shape[0]} samples")

    # 3. Initialize Models with Different Parameters
    model_params_list = [
        {'objective': 'binary:logistic', 'eval_metric': 'auc', 'seed': random_state},
        {'objective': 'binary:logistic', 'eval_metric': 'auc', 'seed': random_state + 1, 'max_depth': 4,
         'learning_rate': 0.1},
        {'objective': 'binary:logistic', 'eval_metric': 'auc', 'seed': random_state + 2, 'max_depth': 6,
         'learning_rate': 0.05}
    ]

    # Ensure we have enough parameter sets
    if num_models > len(model_params_list):
        # Extend model_params_list by varying existing params
        additional_params = []
        for i in range(num_models - len(model_params_list)):
            params = model_params_list[i % len(model_params_list)].copy()
            params['seed'] += i + 3
            additional_params.append(params)
        model_params_list.extend(additional_params)

    models = []
    for params in model_params_list[:num_models]:
        model = xgb.XGBClassifier(**params, use_label_encoder=False, verbosity=0)
        models.append(model)

    if verbose:
        print(f"\nInitialized {num_models} XGBoost models with different parameters.")

    # 4. Train Models and Collect Feature Importances
    feature_importance_dict = {feature: 0 for feature in X_encoded.columns}
    feature_rank_points = {feature: 0 for feature in X_encoded.columns}
    feature_random_points = {feature: 0 for feature in X_encoded.columns}
    gini_scores = []

    if verbose:
        print("\nTraining models and aggregating feature importances...")

    for idx, model in enumerate(tqdm(models, disable=not verbose), 1):
        if verbose:
            print(f"\nTraining model {idx}...")
        model.fit(X_train, y_train)
        y_pred = model.predict_proba(X_test)[:, 1]
        auc = roc_auc_score(y_test, y_pred)
        gini = 2 * auc - 1
        gini_scores.append(gini)
        if verbose:
            print(f"Model {idx} AUC: {auc:.4f}, Gini: {gini:.4f}")

        # Get feature importances
        importance = model.feature_importances_
        feature_importances = pd.Series(importance, index=X_encoded.columns)
        feature_importances = feature_importances.sort_values(ascending=False)

        # Identify the ranking order
        ranking = feature_importances.index.tolist()

        # 4.a. Update feature importance points (presence)
        for feature in ranking:
            feature_importance_dict[feature] += 1  # Point for being in ranking

        # 4.b. Update feature rank points based on position
        for rank, feature in enumerate(ranking, start=1):
            # Higher rank (lower number) gets more points
            # Assign (total_features - rank + 1) points
            feature_rank_points[feature] += (len(X_encoded.columns) - rank + 1)

        # 4.c. Update feature random points based on ranking above random features
        for feature in X_encoded.columns:
            if feature in random_feature_names:
                continue  # Skip random features themselves
            # Determine how many random features this feature ranks above
            feature_position = ranking.index(feature)
            num_random_below = 0
            for rand_feat in random_feature_names:
                if rand_feat in ranking:
                    rand_position = ranking.index(rand_feat)
                    if feature_position < rand_position:
                        num_random_below += 1
            feature_random_points[feature] += num_random_below  # Points based on random features below

        if verbose:
            print(f"Model {idx} feature importances recorded.")

    # 5. Aggregate Feature Importances
    aggregated_importance = {}
    for feature in X_encoded.columns:
        # Combine presence points, rank-based points, and random benchmark points
        aggregated_importance[feature] = (
                feature_importance_dict[feature] +
                feature_rank_points[feature] +
                feature_random_points[feature]
        )

    aggregated_importance_series = pd.Series(aggregated_importance).sort_values(ascending=False)

    # 6. Determine Feature Selection Order
    selected_features = aggregated_importance_series.index.tolist()

    # 7. Evaluate Performance vs. Number of Features (Mean Gini from multiple models)
    cumulative_features = []
    cumulative_gini = []

    if verbose:
        print("\nEvaluating performance vs. number of features...")

    for n in tqdm(range(1, len(selected_features) + 1), disable=not verbose):
        features_subset = selected_features[:n]
        X_train_subset = X_train[features_subset]
        X_test_subset = X_test[features_subset]

        # To compute mean Gini, we'll train 'num_models' models with different seeds
        gini_subset_list = []
        for m in range(num_models):
            # Initialize model with different seeds for diversity
            params = model_params_list[m % len(model_params_list)].copy()
            params['seed'] = random_state + m + 3  # Different seed
            model_subset = xgb.XGBClassifier(**params, use_label_encoder=False, verbosity=0)
            model_subset.fit(X_train_subset, y_train)
            y_pred_subset = model_subset.predict_proba(X_test_subset)[:, 1]
            auc_subset = roc_auc_score(y_test, y_pred_subset)
            gini_subset = 2 * auc_subset - 1
            gini_subset_list.append(gini_subset)

        mean_gini = np.mean(gini_subset_list)
        cumulative_features.append(n)
        cumulative_gini.append(mean_gini)

    # 8. Plot Mean Gini vs. Number of Features
    plt.figure(figsize=(10, 6))
    sns.lineplot(x=cumulative_features, y=cumulative_gini, marker='o')
    plt.title('Mean Gini Coefficient vs. Number of Features')
    plt.xlabel('Number of Features')
    plt.ylabel('Mean Gini Coefficient')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # 9. Plot Feature Ranking
    plt.figure(figsize=(12, 8))
    sns.barplot(
        x=aggregated_importance_series.head(top_n),
        y=aggregated_importance_series.head(top_n).index,
        palette='viridis',
        hue=aggregated_importance_series.head(top_n).index
    )
    plt.title(f'Top {top_n} Feature Rankings')
    plt.xlabel('Aggregated Importance Score')
    plt.ylabel('Features')
    plt.tight_layout()
    plt.show()

    if verbose:
        print("\nFeature importance analysis completed.")

    return aggregated_importance_series


def feature_correlation_with_target(df, list_of_feat, target, save_to_file=None):
    """
    Calculates and visualizes the correlation coefficients between each feature
    and the target variable for both categorical and numerical features.
    Includes violin plots for numeric features and interpretations as text boxes.

    Parameters:
    - df (pd.DataFrame): The dataset containing the features and target variable.
    - list_of_feat (list of str): List of feature names to analyze.
    - target (str): The name of the target variable.
    - save_to_file (str or None): Folder path to save the plots. If None, plots are not saved.

    Returns:
    - pd.DataFrame: A DataFrame containing correlation values for each feature.
    """
    if target not in df.columns:
        raise ValueError(f"Target column '{target}' not found in the DataFrame.")
    if not all([feat in df.columns for feat in list_of_feat]):
        missing = [feat for feat in list_of_feat if feat not in df.columns]
        raise ValueError(f"The following features are missing in the DataFrame: {missing}")

    # Ensure the target variable is numeric for correlation calculation
    if not pd.api.types.is_numeric_dtype(df[target]):
        raise ValueError("Target variable must be numeric for correlation calculation.")

    results = []
    for feat in list_of_feat:
        if pd.api.types.is_numeric_dtype(df[feat]):
            # Pearson correlation for numeric data
            corr = df[feat].corr(df[target])
            corr_type = 'Pearson'
            plot_type = "violin"
        else:
            # Cramér's V for categorical data
            contingency_table = pd.crosstab(df[feat], df[target])
            chi2 = stats.chi2_contingency(contingency_table)[0]
            n = df.shape[0]
            min_dim = min(contingency_table.shape) - 1
            corr = np.sqrt(chi2 / (n * min_dim))
            corr_type = "Cramér's V"
            plot_type = "barplot"
        results.append({"Feature": feat, "Correlation": corr, "Method": corr_type, "Plot_Type": plot_type})

    # Convert results to DataFrame
    results_df = pd.DataFrame(results).sort_values(by="Correlation", ascending=False)

    # Visualization and Interpretation
    for _, row in results_df.iterrows():
        feat = row['Feature']
        corr = row['Correlation']
        corr_type = row['Method']

        if row["Plot_Type"] == "violin":
            # Violin plot for numeric features
            plt.figure(figsize=(12, 6))
            sns.violinplot(x=df[target], y=df[feat], palette='viridis', hue=df[target])
            plt.title(f"Violin Plot: {feat} vs {target} ({corr_type} Corr = {corr:.2f})")
            plt.xlabel(target)
            plt.ylabel(feat)

            # Interpretation for numeric features
            if corr > 0:
                interpretation = (
                    f"Feature '{feat}' is positively correlated with the target.\n"
                    f"Higher values of '{feat}' tend to be associated with higher values of the target."
                )
            elif corr < 0:
                interpretation = (
                    f"Feature '{feat}' is negatively correlated with the target.\n"
                    f"Higher values of '{feat}' tend to be associated with lower values of the target."
                )
            else:
                interpretation = (
                    f"Feature '{feat}' shows no significant correlation with the target."
                )
        else:
            # Bar plot for categorical features
            plt.figure(figsize=(12, 6))
            sns.barplot(x=feat, y=target, data=df, palette='viridis', hue=feat, errorbar=None)
            plt.title(f"Bar Plot: {feat} vs {target} ({corr_type} Corr = {corr:.2f})")
            plt.xlabel(feat)
            plt.ylabel(f"Mean of {target}")

            # Interpretation for categorical features
            mean_target_by_category = df.groupby(feat)[target].mean().sort_values(ascending=False)
            best_category = mean_target_by_category.idxmax()
            worst_category = mean_target_by_category.idxmin()
            interpretation = (
                f"Feature '{feat}' is categorical.\n"
                f"The category '{best_category}' is associated with the highest mean value of the target, "
                f"while '{worst_category}' is associated with the lowest mean value."
            )

        # Add interpretation as a textbox below the plot
        # Add interpretation as a textbox at the bottom center of the plot
        plt.gcf().text(
            0.5, -0.06, interpretation,
            fontsize=10, color="black", wrap=True, ha="center",
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray')
        )

        # Save or show plot
        if save_to_file:
            filename = f"{save_to_file}/{feat}_correlation_plot.png"
            plt.savefig(filename, bbox_inches="tight")
            print(f"Saved plot for '{feat}' at {filename}.")
        else:
            plt.show()

    # Summary Bar Plot
    plt.figure(figsize=(12, 8))
    sns.barplot(x='Correlation', y='Feature', hue='Method', data=results_df, palette='viridis')
    plt.title(f"Feature Correlation with Target: {target}")
    plt.xlabel("Correlation Coefficient")
    plt.ylabel("Features")
    plt.tight_layout()

    # Save or show summary plot
    if save_to_file:
        summary_filename = f"{save_to_file}/summary_correlation_plot.png"
        plt.savefig(summary_filename, bbox_inches="tight")
        print(f"Saved summary plot at {summary_filename}.")
    else:
        plt.show()

    return results_df
