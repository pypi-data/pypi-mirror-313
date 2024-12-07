from sklearn.ensemble import (
    RandomForestClassifier,
    GradientBoostingClassifier,
    AdaBoostClassifier,
    BaggingClassifier,
)
from sklearn.svm import SVC, SVR
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.linear_model import (
    LassoCV,
    LogisticRegression,
    LinearRegression,
    Lasso,
    Ridge,
    RidgeClassifierCV,
    ElasticNet,
)
 
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    matthews_corrcoef,
    roc_curve,
    auc,
    balanced_accuracy_score,
    precision_recall_curve,
    average_precision_score,
)
from typing import Dict, Any, Optional, List, Union
import os, json
import numpy as np
import pandas as pd
from . import ips
from . import plot
import matplotlib.pyplot as plt
plt.style.use(str(ips.get_cwd()) + "/data/styles/stylelib/paper.mplstyle")
import logging
import warnings

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger()

# Ignore specific warnings (UserWarning in this case)
warnings.filterwarnings("ignore", category=UserWarning)
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
#* set random_state global 
import torch 
import random
random_state=1
random.seed(random_state)
np.random.seed(random_state)
torch.manual_seed(random_state)

def features_knn(
    x_train: pd.DataFrame, y_train: pd.Series, knn_params: dict
) -> pd.DataFrame:
    """
    A distance-based classifier that assigns labels based on the majority label of nearest neighbors.
    when to use:
        Effective for small to medium datasets with a low number of features.
        It does not directly provide feature importances but can be assessed through feature permutation or similar methods.
    Recommended Use: Effective for datasets with low feature dimensionality and well-separated clusters.

    Fits KNeighborsClassifier and approximates feature influence using permutation importance.
    """
    knn = KNeighborsClassifier(**knn_params)
    knn.fit(x_train, y_train)
    importances = permutation_importance(
        knn, x_train, y_train, n_repeats=30, random_state=1, scoring="accuracy"
    )
    return pd.DataFrame(
        {"feature": x_train.columns, "importance": importances.importances_mean}
    ).sort_values(by="importance", ascending=False)


#! 1. Linear and Regularized Regression Methods
# 1.1 Lasso
def features_lasso(
    x_train: pd.DataFrame, y_train: pd.Series, lasso_params: dict
) -> np.ndarray:
    """
    Lasso (Least Absolute Shrinkage and Selection Operator):
    A regularized linear regression method that uses L1 penalty to shrink coefficients, effectively
    performing feature selection by zeroing out less important ones.
    """
    lasso = LassoCV(**lasso_params)
    lasso.fit(x_train, y_train)
    # Get non-zero coefficients and their corresponding features
    coefficients = lasso.coef_
    importance_df = pd.DataFrame(
        {"feature": x_train.columns, "importance": np.abs(coefficients)}
    )
    return importance_df[importance_df["importance"] > 0].sort_values(
        by="importance", ascending=False
    )


# 1.2 Ridge regression
def features_ridge(
    x_train: pd.DataFrame, y_train: pd.Series, ridge_params: dict
) -> np.ndarray:
    """
    Ridge Regression: A linear regression technique that applies L2 regularization, reducing coefficient
    magnitudes to avoid overfitting, especially with multicollinearity among features.
    """
    from sklearn.linear_model import RidgeCV

    ridge = RidgeCV(**ridge_params)
    ridge.fit(x_train, y_train)

    # Get the coefficients
    coefficients = ridge.coef_

    # Create a DataFrame to hold feature importance
    importance_df = pd.DataFrame(
        {"feature": x_train.columns, "importance": np.abs(coefficients)}
    )
    return importance_df[importance_df["importance"] > 0].sort_values(
        by="importance", ascending=False
    )


# 1.3 Elastic Net(Enet)
def features_enet(
    x_train: pd.DataFrame, y_train: pd.Series, enet_params: dict
) -> np.ndarray:
    """
    Elastic Net (Enet): Combines L1 and L2 penalties (lasso and ridge) in a linear model, beneficial
    when features are highly correlated or for datasets with more features than samples.
    """
    from sklearn.linear_model import ElasticNetCV

    enet = ElasticNetCV(**enet_params)
    enet.fit(x_train, y_train)
    # Get the coefficients
    coefficients = enet.coef_
    # Create a DataFrame to hold feature importance
    importance_df = pd.DataFrame(
        {"feature": x_train.columns, "importance": np.abs(coefficients)}
    )
    return importance_df[importance_df["importance"] > 0].sort_values(
        by="importance", ascending=False
    )


# 1.4 Partial Least Squares Regression for Generalized Linear Models (plsRglm): Combines regression and
# feature reduction, useful for high-dimensional data with correlated features, such as genomics.

#! 2.Generalized Linear Models and Extensions
# 2.1


#!3.Tree-Based and Ensemble Methods
# 3.1 Random Forest(RF)
def features_rf(
    x_train: pd.DataFrame, y_train: pd.Series, rf_params: dict
) -> np.ndarray:
    """
    An ensemble of decision trees that combines predictions from multiple trees for classification or
    regression, effective with high-dimensional, complex datasets.
    when to use:
        Handles high-dimensional data well.
        Robust to overfitting due to averaging of multiple trees.
        Provides feature importance, which can help in understanding the influence of different genes.
    Fit Random Forest and return sorted feature importances.
    Recommended Use: Great for classification problems, especially when you have many features (genes).
    """
    rf = RandomForestClassifier(**rf_params)
    rf.fit(x_train, y_train)
    return pd.DataFrame(
        {"feature": x_train.columns, "importance": rf.featuress_}
    ).sort_values(by="importance", ascending=False)


# 3.2 Gradient Boosting Trees
def features_gradient_boosting(
    x_train: pd.DataFrame, y_train: pd.Series, gb_params: dict
) -> pd.DataFrame:
    """
    An ensemble of decision trees that combines predictions from multiple trees for classification or regression, effective with
    high-dimensional, complex datasets.
    Gradient Boosting
    Strengths:
        High predictive accuracy and works well for both classification and regression.
        Can handle a mixture of numerical and categorical features.
    Recommended Use:
        Effective for complex relationships and when you need a powerful predictive model.
    Fit Gradient Boosting classifier and return sorted feature importances.
    Recommended Use: Effective for complex datasets with many features (genes).
    """
    gb = GradientBoostingClassifier(**gb_params)
    gb.fit(x_train, y_train)
    return pd.DataFrame(
        {"feature": x_train.columns, "importance": gb.feature_importances_}
    ).sort_values(by="importance", ascending=False)


# 3.3 XGBoost
def features_xgb(
    x_train: pd.DataFrame, y_train: pd.Series, xgb_params: dict
) -> pd.DataFrame:
    """
    XGBoost: An advanced gradient boosting technique, faster and more efficient than GBM, with excellent predictive performance on structured data.
    """
    import xgboost as xgb

    xgb_model = xgb.XGBClassifier(**xgb_params)
    xgb_model.fit(x_train, y_train)
    return pd.DataFrame(
        {"feature": x_train.columns, "importance": xgb_model.feature_importances_}
    ).sort_values(by="importance", ascending=False)


# 3.4.decision tree
def features_decision_tree(
    x_train: pd.DataFrame, y_train: pd.Series, dt_params: dict
) -> pd.DataFrame:
    """
    A single decision tree classifier effective for identifying key decision boundaries in data.
    when to use:
        Good for capturing non-linear patterns.
        Provides feature importance scores for each feature, though it may overfit on small datasets.
        Efficient for low to medium-sized datasets, where interpretability of decisions is key.
    Recommended Use: Useful for interpretable feature importance analysis in smaller or balanced datasets.

    Fits DecisionTreeClassifier and returns sorted feature importances.
    """
    dt = DecisionTreeClassifier(**dt_params)
    dt.fit(x_train, y_train)
    return pd.DataFrame(
        {"feature": x_train.columns, "importance": dt.feature_importances_}
    ).sort_values(by="importance", ascending=False)


# 3.5 bagging
def features_bagging(
    x_train: pd.DataFrame, y_train: pd.Series, bagging_params: dict
) -> pd.DataFrame:
    """
    A bagging ensemble of models, often used with weak learners like decision trees, to reduce variance.
    when to use:
        Helps reduce overfitting, especially on high-variance models.
        Effective when the dataset has numerous features and may benefit from ensemble stability.
    Recommended Use: Beneficial for high-dimensional or noisy datasets needing ensemble stability.

    Fits BaggingClassifier and returns averaged feature importances from underlying estimators if available.
    """
    bagging = BaggingClassifier(**bagging_params)
    bagging.fit(x_train, y_train)

    # Calculate feature importance by averaging importances across estimators, if feature_importances_ is available.
    if hasattr(bagging.estimators_[0], "feature_importances_"):
        importances = np.mean(
            [estimator.feature_importances_ for estimator in bagging.estimators_],
            axis=0,
        )
        return pd.DataFrame(
            {"feature": x_train.columns, "importance": importances}
        ).sort_values(by="importance", ascending=False)
    else:
        # If the base estimator does not support feature importances, fallback to permutation importance.
        importances = permutation_importance(
            bagging, x_train, y_train, n_repeats=30, random_state=1, scoring="accuracy"
        )
        return pd.DataFrame(
            {"feature": x_train.columns, "importance": importances.importances_mean}
        ).sort_values(by="importance", ascending=False)


#! 4.Support Vector Machines
def features_svm(
    x_train: pd.DataFrame, y_train: pd.Series, rfe_params: dict
) -> np.ndarray:
    """
    Suitable for classification tasks where the number of features is much larger than the number of samples.
        1. Effective in high-dimensional spaces and with clear margin of separation.
        2. Works well for both linear and non-linear classification (using kernel functions).
    Select features using RFE with SVM.When combined with SVM, RFE selects features that are most critical for the decision boundary,
        helping reduce the dataset to a more manageable size without losing much predictive power.
    SVM (Support Vector Machines),supports various kernels (linear, rbf, poly, and sigmoid), is good at handling high-dimensional
        data and finding an optimal decision boundary between classes, especially when using the right kernel.
    kernel: ["linear", "rbf", "poly", "sigmoid"]
        'linear': simplest kernel that attempts to separate data by drawing a straight line (or hyperplane) between classes. It is effective
            when the data is linearly separable, meaning the classes can be well divided by a straight boundary.
                Advantages:
                    - Computationally efficient for large datasets.
                    - Works well when the number of features is high, which is common in genomic data where you may have thousands of genes
                        as features.
        'rbf':  a nonlinear kernel that maps the input data into a higher-dimensional space to find a decision boundary. It works well for
            data that is not linearly separable in its original space.
                Advantages:
                    - Handles nonlinear relationships between features and classes
                    - Often better than a linear kernel when there is no clear linear decision boundary in the data.
        'poly': Polynomial Kernel: computes similarity between data points based on polynomial functions of the input features. It can model
            interactions between features to a certain degree, depending on the polynomial degree chosen.
                Advantages:
                    - Allows modeling of feature interactions.
                    - Can fit more complex relationships compared to linear models.
        'sigmoid':  similar to the activation function in neural networks, and it works well when the data follows an S-shaped decision boundary.
                Advantages:
                - Can approximate the behavior of neural networks.
                - Use case: It’s not as widely used as the RBF or linear kernel but can be explored when there is some evidence of non-linear
                    S-shaped relationships.
    """
    from sklearn.feature_selection import RFE
    from sklearn.svm import SVC
    # SVM (Support Vector Machines)
    svc = SVC(kernel=rfe_params["kernel"])  # ["linear", "rbf", "poly", "sigmoid"]
    # RFE(Recursive Feature Elimination)
    selector = RFE(svc, n_features_to_select=rfe_params["n_features_to_select"])
    selector.fit(x_train, y_train)
    return x_train.columns[selector.support_]


#! 5.Bayesian and Probabilistic Methods
def features_naive_bayes(x_train: pd.DataFrame, y_train: pd.Series) -> list:
    """
    Naive Bayes: A probabilistic classifier based on Bayes' theorem, assuming independence between features, simple and fast, especially
    effective for text classification and other high-dimensional data.
    """
    from sklearn.naive_bayes import GaussianNB

    nb = GaussianNB()
    nb.fit(x_train, y_train)
    probabilities = nb.predict_proba(x_train)
    # Limit the number of features safely, choosing the lesser of half the features or all columns
    n_features = min(x_train.shape[1] // 2, len(x_train.columns))

    # Sort probabilities, then map to valid column indices
    sorted_indices = np.argsort(probabilities.max(axis=1))[:n_features]

    # Ensure indices are within the column bounds of x_train
    valid_indices = sorted_indices[sorted_indices < len(x_train.columns)]

    return x_train.columns[valid_indices]


#! 6.Linear Discriminant Analysis (LDA)
def features_lda(x_train: pd.DataFrame, y_train: pd.Series) -> list:
    """
    Linear Discriminant Analysis (LDA): Projects data onto a lower-dimensional space to maximize class separability, often used as a dimensionality
    reduction technique before classification on high-dimensional data.
    """
    from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

    lda = LinearDiscriminantAnalysis()
    lda.fit(x_train, y_train)
    coef = lda.coef_.flatten()
    # Create a DataFrame to hold feature importance
    importance_df = pd.DataFrame(
        {"feature": x_train.columns, "importance": np.abs(coef)}
    )

    return importance_df[importance_df["importance"] > 0].sort_values(
        by="importance", ascending=False
    )


def features_adaboost(
    x_train: pd.DataFrame, y_train: pd.Series, adaboost_params: dict
) -> pd.DataFrame:
    """
    AdaBoost
    Strengths:
        Combines multiple weak learners to create a strong classifier.
        Focuses on examples that are hard to classify, improving overall performance.
    Recommended Use:
        Can be effective for boosting weak models in a genomics context.
    Fit AdaBoost classifier and return sorted feature importances.
    Recommended Use: Great for classification problems with a large number of features (genes).
    """
    ada = AdaBoostClassifier(**adaboost_params)
    ada.fit(x_train, y_train)
    return pd.DataFrame(
        {"feature": x_train.columns, "importance": ada.feature_importances_}
    ).sort_values(by="importance", ascending=False)


import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from skorch import NeuralNetClassifier  # sklearn compatible


class DNNClassifier(nn.Module):
    def __init__(self, input_dim, hidden_dim=128, output_dim=2, dropout_rate=0.5):
        super(DNNClassifier, self).__init__()

        self.hidden_layer1 = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout_rate),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
        )

        self.hidden_layer2 = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim), nn.ReLU(), nn.Dropout(dropout_rate)
        )

        # Adding a residual connection between hidden layers
        self.residual = nn.Linear(input_dim, hidden_dim)

        self.output_layer = nn.Sequential(
            nn.Linear(hidden_dim, output_dim), nn.Softmax(dim=1)
        )

    def forward(self, x):
        residual = self.residual(x)
        x = self.hidden_layer1(x)
        x = x + residual  # Residual connection
        x = self.hidden_layer2(x)
        x = self.output_layer(x)
        return x


def validate_classifier(
    clf,
    x_train: pd.DataFrame,
    y_train: pd.Series,
    x_test: pd.DataFrame,
    y_test: pd.Series,
    metrics: list = ["accuracy", "precision", "recall", "f1", "roc_auc"],
    cv_folds: int = 5,
) -> dict:
    """
    Perform cross-validation for a given classifier and return average scores for specified metrics on training data.
    Then fit the best model on the full training data and evaluate it on the test set.

    Parameters:
    - clf: The classifier to be validated.
    - x_train: Training features.
    - y_train: Training labels.
    - x_test: Test features.
    - y_test: Test labels.
    - metrics: List of metrics to evaluate (e.g., ['accuracy', 'roc_auc']).
    - cv_folds: Number of cross-validation folds.

    Returns:
    - results: Dictionary containing average cv_train_scores and cv_test_scores.
    """
    from sklearn.model_selection import cross_val_score
    cv_train_scores = {metric: [] for metric in metrics}
    skf = StratifiedKFold(n_splits=cv_folds)
    # Perform cross-validation
    for metric in metrics:
        try:
            if metric == "roc_auc" and len(set(y_train)) == 2:
                scores = cross_val_score(
                    clf, x_train, y_train, cv=skf, scoring="roc_auc"
                )
                cv_train_scores[metric] = (
                    np.nanmean(scores) if not np.isnan(scores).all() else float("nan")
                )
            else:
                score = cross_val_score(clf, x_train, y_train, cv=skf, scoring=metric)
                cv_train_scores[metric] = score.mean()
        except Exception as e:
            cv_train_scores[metric] = float("nan")
    clf.fit(x_train, y_train)

    # Evaluate on the test set
    cv_test_scores = {}
    for metric in metrics:
        if metric == "roc_auc" and len(set(y_test)) == 2:
            try:
                y_prob = clf.predict_proba(x_test)[:, 1]
                cv_test_scores[metric] = roc_auc_score(y_test, y_prob)
            except AttributeError:
                cv_test_scores[metric] = float("nan")
        else:
            score_func = globals().get(
                f"{metric}_score"
            )  # Fetching the appropriate scoring function
            if score_func:
                try:
                    y_pred = clf.predict(x_test)
                    cv_test_scores[metric] = score_func(y_test, y_pred)
                except Exception as e:
                    cv_test_scores[metric] = float("nan")

    # Combine results
    results = {"cv_train_scores": cv_train_scores, "cv_test_scores": cv_test_scores}
    return results


def get_models(
    random_state=1,
    cls=[
        "lasso",
        "ridge",
        "Elastic Net(Enet)",
        "gradient Boosting",
        "Random forest (rf)",
        "XGBoost (xgb)",
        "Support Vector Machine(svm)",
        "naive bayes",
        "Linear Discriminant Analysis (lda)",
        "AdaBoost",
        "DecisionTree",
        "KNeighbors",
        "Bagging",
    ],
):
    from sklearn.ensemble import (
        RandomForestClassifier,
        GradientBoostingClassifier,
        AdaBoostClassifier,
        BaggingClassifier,
    )
    from sklearn.svm import SVC
    from sklearn.linear_model import (
        LogisticRegression,
        Lasso,
        RidgeClassifierCV,
        ElasticNet,
    )
    from sklearn.naive_bayes import GaussianNB
    from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
    import xgboost as xgb
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.neighbors import KNeighborsClassifier

    res_cls = {}
    model_all = {
        "Lasso": LogisticRegression(
            penalty="l1", solver="saga", random_state=random_state
        ),
        "Ridge": RidgeClassifierCV(),
        "Elastic Net (Enet)": ElasticNet(random_state=random_state),
        "Gradient Boosting": GradientBoostingClassifier(random_state=random_state),
        "Random Forest (RF)": RandomForestClassifier(random_state=random_state),
        "XGBoost (XGB)": xgb.XGBClassifier(random_state=random_state),
        "Support Vector Machine (SVM)": SVC(kernel="rbf", probability=True),
        "Naive Bayes": GaussianNB(),
        "Linear Discriminant Analysis (LDA)": LinearDiscriminantAnalysis(),
        "AdaBoost": AdaBoostClassifier(random_state=random_state, algorithm="SAMME"),
        "DecisionTree": DecisionTreeClassifier(),
        "KNeighbors": KNeighborsClassifier(n_neighbors=5),
        "Bagging": BaggingClassifier(),
    }
    print("Using default models:")
    for cls_name in cls:
        cls_name = ips.strcmp(cls_name, list(model_all.keys()))[0]
        res_cls[cls_name] = model_all[cls_name]
        print(f"- {cls_name}")
    return res_cls


def get_features(
    X: Union[pd.DataFrame, np.ndarray],  # n_samples X n_features
    y: Union[pd.Series, np.ndarray, list],  # n_samples X n_features
    test_size: float = 0.2,
    random_state: int = 1,
    n_features: int = 10,
    fill_missing=True,
    rf_params: Optional[Dict] = None,
    rfe_params: Optional[Dict] = None,
    lasso_params: Optional[Dict] = None,
    ridge_params: Optional[Dict] = None,
    enet_params: Optional[Dict] = None,
    gb_params: Optional[Dict] = None,
    adaboost_params: Optional[Dict] = None,
    xgb_params: Optional[Dict] = None,
    dt_params: Optional[Dict] = None,
    bagging_params: Optional[Dict] = None,
    knn_params: Optional[Dict] = None,
    cls: list = [
        "lasso",
        "ridge",
        "Elastic Net(Enet)",
        "gradient Boosting",
        "Random forest (rf)",
        "XGBoost (xgb)",
        "Support Vector Machine(svm)",
        "naive bayes",
        "Linear Discriminant Analysis (lda)",
        "AdaBoost",
        "DecisionTree",
        "KNeighbors",
        "Bagging",
    ],
    metrics: Optional[List[str]] = None,
    cv_folds: int = 5,
    strict: bool = False,
    n_shared: int = 2,  # 只要有两个方法有重合,就纳入common genes
    use_selected_features: bool = True,
    plot_: bool = True,
    dir_save: str = "./",
) -> dict:
    """
    Master function to perform feature selection and validate models.
    """
    from sklearn.compose import ColumnTransformer
    from sklearn.preprocessing import StandardScaler, OneHotEncoder
    from sklearn.model_selection import train_test_split
    # Ensure X and y are DataFrames/Series for consistency
    if isinstance(X, np.ndarray):
        X = pd.DataFrame(X)
    if isinstance(y, (np.ndarray, list)):
        y = pd.Series(y)

    # fill na
    if fill_missing:
        ips.df_fillna(data=X, method="knn", inplace=True, axis=0)
    if isinstance(y, str) and y in X.columns:
        y_col_name = y
        y = X[y]
        y = ips.df_encoder(pd.DataFrame(y), method="label")
        X = X.drop(y_col_name, axis=1)
    else:
        y = ips.df_encoder(pd.DataFrame(y), method="label").values.ravel()
    y = y.loc[X.index]  # Align y with X after dropping rows with missing values in X
    y = y.ravel() if isinstance(y, np.ndarray) else y.values.ravel()

    if X.shape[0] != len(y):
        raise ValueError("X and y must have the same number of samples (rows).")

    # #! # Check for non-numeric columns in X and apply one-hot encoding if needed
    # Check if any column in X is non-numeric
    if any(not np.issubdtype(dtype, np.number) for dtype in X.dtypes):
        X = pd.get_dummies(X, drop_first=True)
    print(X.shape)

    # #!alternative:  # Identify categorical and numerical columns
    # categorical_cols = X.select_dtypes(include=["object", "category"]).columns
    # numerical_cols = X.select_dtypes(include=["number"]).columns

    # # Define preprocessing pipeline
    # preprocessor = ColumnTransformer(
    #     transformers=[
    #         ("num", StandardScaler(), numerical_cols),
    #         ("cat", OneHotEncoder(drop="first", handle_unknown="ignore"), categorical_cols),
    #     ]
    # )
    # # Preprocess the data
    # X = preprocessor.fit_transform(X)

    # Split data into training and test sets
    x_train, x_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    # Standardize features
    scaler = StandardScaler()
    x_train_scaled = scaler.fit_transform(x_train)
    x_test_scaled = scaler.transform(x_test)

    # Convert back to DataFrame for consistency
    x_train = pd.DataFrame(x_train_scaled, columns=x_train.columns)
    x_test = pd.DataFrame(x_test_scaled, columns=x_test.columns)

    rf_defaults = {"n_estimators": 100, "random_state": random_state}
    rfe_defaults = {"kernel": "linear", "n_features_to_select": n_features}
    lasso_defaults = {"alphas": np.logspace(-4, 4, 100), "cv": 10}
    ridge_defaults = {"alphas": np.logspace(-4, 4, 100), "cv": 10}
    enet_defaults = {"alphas": np.logspace(-4, 4, 100), "cv": 10}
    xgb_defaults = {
        "n_estimators": 100,
        "use_label_encoder": False,
        "eval_metric": "logloss",
        "random_state": random_state,
    }
    gb_defaults = {"n_estimators": 100, "random_state": random_state}
    adaboost_defaults = {"n_estimators": 50, "random_state": random_state}
    dt_defaults = {"max_depth": None, "random_state": random_state}
    bagging_defaults = {"n_estimators": 50, "random_state": random_state}
    knn_defaults = {"n_neighbors": 5}
    rf_params, rfe_params = rf_params or rf_defaults, rfe_params or rfe_defaults
    lasso_params, ridge_params = (
        lasso_params or lasso_defaults,
        ridge_params or ridge_defaults,
    )
    enet_params, xgb_params = enet_params or enet_defaults, xgb_params or xgb_defaults
    gb_params, adaboost_params = (
        gb_params or gb_defaults,
        adaboost_params or adaboost_defaults,
    )
    dt_params = dt_params or dt_defaults
    bagging_params = bagging_params or bagging_defaults
    knn_params = knn_params or knn_defaults

    cls_ = [
        "lasso",
        "ridge",
        "Elastic Net(Enet)",
        "Gradient Boosting",
        "Random Forest (rf)",
        "XGBoost (xgb)",
        "Support Vector Machine(svm)",
        "Naive Bayes",
        "Linear Discriminant Analysis (lda)",
        "AdaBoost",
    ]
    cls = [ips.strcmp(i, cls_)[0] for i in cls]

    feature_importances = {}

    # Lasso Feature Selection
    lasso_importances = (
        features_lasso(x_train, y_train, lasso_params)
        if "lasso" in cls
        else pd.DataFrame()
    )
    lasso_selected_features = (
        lasso_importances.head(n_features)["feature"].values if "lasso" in cls else []
    )
    feature_importances["lasso"] = lasso_importances.head(n_features)
    # Ridge
    ridge_importances = (
        features_ridge(x_train, y_train, ridge_params)
        if "ridge" in cls
        else pd.DataFrame()
    )
    selected_ridge_features = (
        ridge_importances.head(n_features)["feature"].values if "ridge" in cls else []
    )
    feature_importances["ridge"] = ridge_importances.head(n_features)
    # Elastic Net
    enet_importances = (
        features_enet(x_train, y_train, enet_params)
        if "Enet" in cls
        else pd.DataFrame()
    )
    selected_enet_features = (
        enet_importances.head(n_features)["feature"].values if "Enet" in cls else []
    )
    feature_importances["Enet"] = enet_importances.head(n_features)
    # Random Forest Feature Importance
    rf_importances = (
        features_rf(x_train, y_train, rf_params)
        if "Random Forest" in cls
        else pd.DataFrame()
    )
    top_rf_features = (
        rf_importances.head(n_features)["feature"].values
        if "Random Forest" in cls
        else []
    )
    feature_importances["Random Forest"] = rf_importances.head(n_features)
    # Gradient Boosting Feature Importance
    gb_importances = (
        features_gradient_boosting(x_train, y_train, gb_params)
        if "Gradient Boosting" in cls
        else pd.DataFrame()
    )
    top_gb_features = (
        gb_importances.head(n_features)["feature"].values
        if "Gradient Boosting" in cls
        else []
    )
    feature_importances["Gradient Boosting"] = gb_importances.head(n_features)
    # xgb
    xgb_importances = (
        features_xgb(x_train, y_train, xgb_params) if "xgb" in cls else pd.DataFrame()
    )
    top_xgb_features = (
        xgb_importances.head(n_features)["feature"].values if "xgb" in cls else []
    )
    feature_importances["xgb"] = xgb_importances.head(n_features)

    # SVM with RFE
    selected_svm_features = (
        features_svm(x_train, y_train, rfe_params) if "svm" in cls else []
    )
    # Naive Bayes
    selected_naive_bayes_features = (
        features_naive_bayes(x_train, y_train) if "Naive Bayes" in cls else []
    )
    # lda: linear discriminant analysis
    lda_importances = features_lda(x_train, y_train) if "lda" in cls else pd.DataFrame()
    selected_lda_features = (
        lda_importances.head(n_features)["feature"].values if "lda" in cls else []
    )
    feature_importances["lda"] = lda_importances.head(n_features)
    # AdaBoost Feature Importance
    adaboost_importances = (
        features_adaboost(x_train, y_train, adaboost_params)
        if "AdaBoost" in cls
        else pd.DataFrame()
    )
    top_adaboost_features = (
        adaboost_importances.head(n_features)["feature"].values
        if "AdaBoost" in cls
        else []
    )
    feature_importances["AdaBoost"] = adaboost_importances.head(n_features)
    # Decision Tree Feature Importance
    dt_importances = (
        features_decision_tree(x_train, y_train, dt_params)
        if "Decision Tree" in cls
        else pd.DataFrame()
    )
    top_dt_features = (
        dt_importances.head(n_features)["feature"].values
        if "Decision Tree" in cls
        else []
    )
    feature_importances["Decision Tree"] = dt_importances.head(n_features)
    # Bagging Feature Importance
    bagging_importances = (
        features_bagging(x_train, y_train, bagging_params)
        if "Bagging" in cls
        else pd.DataFrame()
    )
    top_bagging_features = (
        bagging_importances.head(n_features)["feature"].values
        if "Bagging" in cls
        else []
    )
    feature_importances["Bagging"] = bagging_importances.head(n_features)
    # KNN Feature Importance via Permutation
    knn_importances = (
        features_knn(x_train, y_train, knn_params) if "KNN" in cls else pd.DataFrame()
    )
    top_knn_features = (
        knn_importances.head(n_features)["feature"].values if "KNN" in cls else []
    )
    feature_importances["KNN"] = knn_importances.head(n_features)

    #! Find common features
    common_features = ips.shared(
        lasso_selected_features,
        selected_ridge_features,
        selected_enet_features,
        top_rf_features,
        top_gb_features,
        top_xgb_features,
        selected_svm_features,
        selected_naive_bayes_features,
        selected_lda_features,
        top_adaboost_features,
        top_dt_features,
        top_bagging_features,
        top_knn_features,
        strict=strict,
        n_shared=n_shared,
        verbose=False,
    )

    # Use selected features or all features for model validation
    x_train_selected = (
        x_train[list(common_features)] if use_selected_features else x_train
    )
    x_test_selected = x_test[list(common_features)] if use_selected_features else x_test

    if metrics is None:
        metrics = ["accuracy", "precision", "recall", "f1", "roc_auc"]

    # Prepare results DataFrame for selected features
    features_df = pd.DataFrame(
        {
            "type": ["Lasso"] * len(lasso_selected_features)
            + ["Ridge"] * len(selected_ridge_features)
            + ["Random Forest"] * len(top_rf_features)
            + ["Gradient Boosting"] * len(top_gb_features)
            + ["Enet"] * len(selected_enet_features)
            + ["xgb"] * len(top_xgb_features)
            + ["SVM"] * len(selected_svm_features)
            + ["Naive Bayes"] * len(selected_naive_bayes_features)
            + ["Linear Discriminant Analysis"] * len(selected_lda_features)
            + ["AdaBoost"] * len(top_adaboost_features)
            + ["Decision Tree"] * len(top_dt_features)
            + ["Bagging"] * len(top_bagging_features)
            + ["KNN"] * len(top_knn_features),
            "feature": np.concatenate(
                [
                    lasso_selected_features,
                    selected_ridge_features,
                    top_rf_features,
                    top_gb_features,
                    selected_enet_features,
                    top_xgb_features,
                    selected_svm_features,
                    selected_naive_bayes_features,
                    selected_lda_features,
                    top_adaboost_features,
                    top_dt_features,
                    top_bagging_features,
                    top_knn_features,
                ]
            ),
        }
    )

    #! Validate trained each classifier
    models = get_models(random_state=random_state, cls=cls)
    cv_train_results, cv_test_results = [], []
    for name, clf in models.items():
        if not x_train_selected.empty:
            cv_scores = validate_classifier(
                clf,
                x_train_selected,
                y_train,
                x_test_selected,
                y_test,
                metrics=metrics,
                cv_folds=cv_folds,
            )

            cv_train_score_df = pd.DataFrame(cv_scores["cv_train_scores"], index=[name])
            cv_test_score_df = pd.DataFrame(cv_scores["cv_test_scores"], index=[name])
            cv_train_results.append(cv_train_score_df)
            cv_test_results.append(cv_test_score_df)
    if all([cv_train_results, cv_test_results]):
        cv_train_results_df = (
            pd.concat(cv_train_results)
            .reset_index()
            .rename(columns={"index": "Classifier"})
        )
        cv_test_results_df = (
            pd.concat(cv_test_results)
            .reset_index()
            .rename(columns={"index": "Classifier"})
        )
        #! Store results in the main results dictionary
        results = {
            "selected_features": features_df,
            "cv_train_scores": cv_train_results_df,
            "cv_test_scores": rank_models(cv_test_results_df, plot_=plot_),
            "common_features": list(common_features),
            "feature_importances": feature_importances,
        }
        if all([plot_, dir_save]):
            
            from datetime import datetime
            now_ = datetime.now().strftime("%y%m%d_%H%M%S")
            ips.figsave(dir_save + f"features{now_}.pdf")
            
            lists = []
            for tp in ips.flatten(features_df["type"]):
                lists.append(
                    features_df
                    .loc[features_df["type"] == tp, "feature"]
                    .tolist()
                )
            labels = ips.flatten(features_df["type"])
            # current_fig = plt.gcf() 
            # # ax = current_fig.add_subplot(3, 2, 6)
            # gs = current_fig.add_gridspec(3, 2)
            # ax = current_fig.add_subplot(gs[:, :])
            plt.figure(figsize=[6,6])
            plot.venn(lists, labels, cmap="coolwarm") 
            ips.figsave(dir_save + f"features{now_}shared_features.pdf")
    else:
        results = {
            "selected_features": pd.DataFrame(),
            "cv_train_scores": pd.DataFrame(),
            "cv_test_scores": pd.DataFrame(),
            "common_features": [],
            "feature_importances": {},
        }
        print(f"Warning: 没有找到共同的genes, when n_shared={n_shared}")
    return results


#! # usage:
# # Get features and common features
# results = get_features(X, y)
# common_features = results["common_features"]
def validate_features(
    x_train: pd.DataFrame,
    y_train: pd.Series,
    x_true: pd.DataFrame,
    y_true: pd.Series,
    common_features: set = None,
    models: Optional[Dict[str, Any]] = None,
    metrics: Optional[list] = None,
    random_state: int = 1,
    smote: bool = False,
    n_jobs: int = -1,
    plot_: bool = True,
    class_weight: str = "balanced",
) -> dict:
    """
    Validate models using selected features on the validation dataset.

    Parameters:
    - x_train (pd.DataFrame): Training feature dataset.
    - y_train (pd.Series): Training target variable.
    - x_true (pd.DataFrame): Validation feature dataset.
    - y_true (pd.Series): Validation target variable.
    - common_features (set): Set of common features to use for validation.
    - models (dict, optional): Dictionary of models to validate.
    - metrics (list, optional): List of metrics to compute.
    - random_state (int): Random state for reproducibility.
    - plot_ (bool): Option to plot metrics (to be implemented if needed).
    - class_weight (str or dict): Class weights to handle imbalance.

    """
    from tqdm import tqdm
    from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
    from sklearn.calibration import CalibratedClassifierCV

    # Ensure common features are selected
    common_features = ips.shared(
        common_features, x_train.columns, x_true.columns, strict=True, verbose=False
    )

    # Filter the training and validation datasets for the common features
    x_train_selected = x_train[common_features]
    x_true_selected = x_true[common_features]

    if not x_true_selected.index.equals(y_true.index):
        raise ValueError(
            "Index mismatch between validation features and target. Ensure data alignment."
        )

    y_true = y_true.loc[x_true_selected.index]

    # Handle class imbalance using SMOTE
    if smote:
        from imblearn.over_sampling import SMOTE
        if (
            y_train.value_counts(normalize=True).max() < 0.8
        ):  # Threshold to decide if data is imbalanced
            smote = SMOTE(random_state=random_state)
            x_train_resampled, y_train_resampled = smote.fit_resample(
                x_train_selected, y_train
            )
        else:
            # skip SMOTE
            x_train_resampled, y_train_resampled = x_train_selected, y_train
    else:
        x_train_resampled, y_train_resampled = x_train_selected, y_train

    # Default models if not provided
    if models is None:
        models = {
            "Random Forest": RandomForestClassifier(
                class_weight=class_weight, random_state=random_state
            ),
            "SVM": SVC(probability=True, class_weight=class_weight),
            "Logistic Regression": LogisticRegression(
                class_weight=class_weight, random_state=random_state
            ),
            "Gradient Boosting": GradientBoostingClassifier(random_state=random_state),
            "AdaBoost": AdaBoostClassifier(
                random_state=random_state, algorithm="SAMME"
            ),
            "Lasso": LogisticRegression(
                penalty="l1", solver="saga", random_state=random_state
            ),
            "Ridge": LogisticRegression(
                penalty="l2", solver="saga", random_state=random_state
            ),
            "Elastic Net": LogisticRegression(
                penalty="elasticnet",
                solver="saga",
                l1_ratio=0.5,
                random_state=random_state,
            ),
            "XGBoost": xgb.XGBClassifier(eval_metric="logloss"),
            "Naive Bayes": GaussianNB(),
            "LDA": LinearDiscriminantAnalysis(),
        }

    # Hyperparameter grids for tuning
    param_grids = {
        "Random Forest": {
            "n_estimators": [100, 200, 300, 400, 500],
            "max_depth": [None, 3, 5, 10, 20],
            "min_samples_split": [2, 5, 10],
            "min_samples_leaf": [1, 2, 4],
            "class_weight": [None, "balanced"],
        },
        "SVM": {
            "C": [0.01, 0.1, 1, 10, 100, 1000],
            "gamma": [0.001, 0.01, 0.1, "scale", "auto"],
            "kernel": ["linear", "rbf", "poly"],
        },
        "Logistic Regression": {
            "C": [0.01, 0.1, 1, 10, 100],
            "solver": ["liblinear", "saga", "newton-cg", "lbfgs"],
            "penalty": ["l1", "l2"],
            "max_iter": [100, 200, 300],
        },
        "Gradient Boosting": {
            "n_estimators": [100, 200, 300, 400, 500],
            "learning_rate": np.logspace(-3, 0, 4),
            "max_depth": [3, 5, 7, 9],
            "min_samples_split": [2, 5, 10],
        },
        "AdaBoost": {
            "n_estimators": [50, 100, 200, 300, 500],
            "learning_rate": np.logspace(-3, 0, 4),
        },
        "Lasso": {"C": np.logspace(-3, 1, 10), "max_iter": [100, 200, 300]},
        "Ridge": {"C": np.logspace(-3, 1, 10), "max_iter": [100, 200, 300]},
        "Elastic Net": {
            "C": np.logspace(-3, 1, 10),
            "l1_ratio": [0.1, 0.5, 0.9],
            "max_iter": [100, 200, 300],
        },
        "XGBoost": {
            "n_estimators": [100, 200],
            "max_depth": [3, 5, 7],
            "learning_rate": [0.01, 0.1, 0.2],
            "subsample": [0.8, 1.0],
            "colsample_bytree": [0.8, 1.0],
        },
        "Naive Bayes": {},
        "LDA": {"solver": ["svd", "lsqr", "eigen"]},
    }
    # Default metrics if not provided
    if metrics is None:
        metrics = [
            "accuracy",
            "precision",
            "recall",
            "f1",
            "roc_auc",
            "mcc",
            "specificity",
            "balanced_accuracy",
            "pr_auc",
        ]

    results = {}

    # Validate each classifier with GridSearchCV
    for name, clf in tqdm(
        models.items(),
        desc="for metric in metrics",
        colour="green",
        bar_format="{l_bar}{bar} {n_fmt}/{total_fmt}",
    ):
        print(f"\nValidating {name} on the validation dataset:")

        # Check if `predict_proba` method exists; if not, use CalibratedClassifierCV
        # 没有predict_proba的分类器，使用 CalibratedClassifierCV 可以获得校准的概率估计。此外，为了使代码更灵活，我们可以在创建分类器
        # 时检查 predict_proba 方法是否存在，如果不存在且用户希望计算 roc_auc 或 pr_auc，则启用 CalibratedClassifierCV
        if not hasattr(clf, "predict_proba"):
            print(
                f"Using CalibratedClassifierCV for {name} due to lack of probability estimates."
            )
            calibrated_clf = CalibratedClassifierCV(clf, method="sigmoid", cv="prefit")
        else:
            calibrated_clf = clf
        # Stratified K-Fold for cross-validation
        skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=random_state)

        # Create GridSearchCV object
        gs = GridSearchCV(
            estimator=calibrated_clf,
            param_grid=param_grids[name],
            scoring="roc_auc",  # Optimize for ROC AUC
            cv=skf,  # Stratified K-Folds cross-validation
            n_jobs=n_jobs,
            verbose=1,
        )

        # Fit the model using GridSearchCV
        gs.fit(x_train_resampled, y_train_resampled)
        # Best estimator from grid search
        best_clf = gs.best_estimator_
        # Make predictions on the validation set
        y_pred = best_clf.predict(x_true_selected)
        # Calculate probabilities for ROC AUC if possible
        if hasattr(best_clf, "predict_proba"):
            y_pred_proba = best_clf.predict_proba(x_true_selected)[:, 1]
        elif hasattr(best_clf, "decision_function"):
            # If predict_proba is not available, use decision_function (e.g., for SVM)
            y_pred_proba = best_clf.decision_function(x_true_selected)
            # Ensure y_pred_proba is within 0 and 1 bounds
            y_pred_proba = (y_pred_proba - y_pred_proba.min()) / (
                y_pred_proba.max() - y_pred_proba.min()
            )
        else:
            y_pred_proba = None  # No probability output for certain models

        # Calculate metrics
        validation_scores = {}
        for metric in metrics:
            if metric == "accuracy":
                validation_scores[metric] = accuracy_score(y_true, y_pred)
            elif metric == "precision":
                validation_scores[metric] = precision_score(
                    y_true, y_pred, average="weighted"
                )
            elif metric == "recall":
                validation_scores[metric] = recall_score(
                    y_true, y_pred, average="weighted"
                )
            elif metric == "f1":
                validation_scores[metric] = f1_score(y_true, y_pred, average="weighted")
            elif metric == "roc_auc" and y_pred_proba is not None:
                validation_scores[metric] = roc_auc_score(y_true, y_pred_proba)
            elif metric == "mcc":
                validation_scores[metric] = matthews_corrcoef(y_true, y_pred)
            elif metric == "specificity":
                tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
                validation_scores[metric] = tn / (tn + fp)  # Specificity calculation
            elif metric == "balanced_accuracy":
                validation_scores[metric] = balanced_accuracy_score(y_true, y_pred)
            elif metric == "pr_auc" and y_pred_proba is not None:
                precision, recall, _ = precision_recall_curve(y_true, y_pred_proba)
                validation_scores[metric] = average_precision_score(
                    y_true, y_pred_proba
                )

        # Calculate ROC curve
        # https://scikit-learn.org/stable/auto_examples/model_selection/plot_roc.html
        if y_pred_proba is not None:
            # fpr, tpr, roc_auc = dict(), dict(), dict()
            fpr, tpr, _ = roc_curve(y_true, y_pred_proba)
            lower_ci, upper_ci = cal_auc_ci(y_true, y_pred_proba, verbose=False)
            roc_auc = auc(fpr, tpr)
            roc_info = {
                "fpr": fpr.tolist(),
                "tpr": tpr.tolist(),
                "auc": roc_auc,
                "ci95": (lower_ci, upper_ci),
            }
            # precision-recall curve
            precision_, recall_, _ = precision_recall_curve(y_true, y_pred_proba)
            avg_precision_ = average_precision_score(y_true, y_pred_proba)
            pr_info = {
                "precision": precision_,
                "recall": recall_,
                "avg_precision": avg_precision_,
            }
        else:
            roc_info, pr_info = None, None
        results[name] = {
            "best_params": gs.best_params_,
            "scores": validation_scores,
            "roc_curve": roc_info,
            "pr_curve": pr_info,
            "confusion_matrix": confusion_matrix(y_true, y_pred),
        }

    df_results = pd.DataFrame.from_dict(results, orient="index")

    return df_results


#! usage validate_features()
# Validate models using the validation dataset (X_val, y_val)
# validation_results = validate_features(X, y, X_val, y_val, common_features)


# # If you want to access validation scores
# print(validation_results)
def plot_validate_features(res_val, is_binary=True, figsize=None):
    """
    plot the results of 'validate_features()'
    """
    if is_binary:
        colors = plot.get_color(len(ips.flatten(res_val["pr_curve"].index)))
        if res_val.shape[0] > 5:
            alpha = 0
            figsize = [8, 10] if figsize is None else figsize
            subplot_layout = [1, 2]
            ncols = 2
            bbox_to_anchor = [1.5, 0.6]
        else:
            alpha = 0.03
            figsize = [10, 6] if figsize is None else figsize
            subplot_layout = [1, 1]
            ncols = 1
            bbox_to_anchor = [1, 1]
        nexttile = plot.subplot(figsize=figsize)
        ax = nexttile(subplot_layout[0], subplot_layout[1])
        for i, model_name in enumerate(ips.flatten(res_val["pr_curve"].index)):
            try:
                fpr = res_val["roc_curve"][model_name]["fpr"]
                tpr = res_val["roc_curve"][model_name]["tpr"]
                (lower_ci, upper_ci) = res_val["roc_curve"][model_name]["ci95"]
                mean_auc = res_val["roc_curve"][model_name]["auc"]
                plot_roc_curve(
                    fpr,
                    tpr,
                    mean_auc,
                    lower_ci,
                    upper_ci,
                    model_name=model_name,
                    lw=1.5,
                    color=colors[i],
                    alpha=alpha,
                    ax=ax,
                )
            except Exception as e:
                print(e)
        plot.figsets(
            sp=2,
            legend=dict(
                loc="upper right",
                ncols=ncols,
                fontsize=8,
                bbox_to_anchor=[1.5, 0.6],
                markerscale=0.8,
            ),
        )
        # plot.split_legend(ax,n=2, loc=["upper left", "lower left"],bbox=[[1,0.5],[1,0.5]],ncols=2,labelcolor="k",fontsize=8)

        ax = nexttile(subplot_layout[0], subplot_layout[1])
        for i, model_name in enumerate(ips.flatten(res_val["pr_curve"].index)):
            try:
                plot_pr_curve(
                    recall=res_val["pr_curve"][model_name]["recall"],
                    precision=res_val["pr_curve"][model_name]["precision"],
                    avg_precision=res_val["pr_curve"][model_name]["avg_precision"],
                    model_name=model_name,
                    color=colors[i],
                    lw=1.5,
                    alpha=alpha,
                    ax=ax,
                )
            except Exception as e:
                print(e)
        plot.figsets(
            sp=2,
            legend=dict(
                loc="upper right", ncols=1, fontsize=8, bbox_to_anchor=[1.5, 0.5]
            ),
        )
        # plot.split_legend(ax,n=2, loc=["upper left", "lower left"],bbox=[[1,0.5],[1,0.5]],ncols=2,labelcolor="k",fontsize=8)
    else:
        colors = plot.get_color(len(ips.flatten(res_val["pr_curve"].index)))
        modname_tmp = ips.flatten(res_val["roc_curve"].index)[0]
        classes = list(res_val["roc_curve"][modname_tmp]["fpr"].keys())
        if res_val.shape[0] > 5:
            alpha = 0
            figsize = [8, 8 * 2 * (len(classes))] if figsize is None else figsize
            subplot_layout = [1, 2]
            ncols = 2
            bbox_to_anchor = [1.5, 0.6]
        else:
            alpha = 0.03
            figsize = [10, 6 * (len(classes))] if figsize is None else figsize
            subplot_layout = [1, 1]
            ncols = 1
            bbox_to_anchor = [1, 1]
        nexttile = plot.subplot(2 * (len(classes)), 2, figsize=figsize)
        for iclass, class_ in enumerate(classes):
            ax = nexttile(subplot_layout[0], subplot_layout[1])
            for i, model_name in enumerate(ips.flatten(res_val["pr_curve"].index)):
                try:
                    fpr = res_val["roc_curve"][model_name]["fpr"][class_]
                    tpr = res_val["roc_curve"][model_name]["tpr"][class_]
                    (lower_ci, upper_ci) = res_val["roc_curve"][model_name]["ci95"][iclass]
                    mean_auc = res_val["roc_curve"][model_name]["auc"][class_]
                    plot_roc_curve(
                        fpr,
                        tpr,
                        mean_auc,
                        lower_ci,
                        upper_ci,
                        model_name=model_name,
                        lw=1.5,
                        color=colors[i],
                        alpha=alpha,
                        ax=ax,
                    )
                except Exception as e:
                    print(e)
            plot.figsets(
                sp=2,
                title=class_,
                legend=dict(
                    loc="upper right",
                    ncols=ncols,
                    fontsize=8,
                    bbox_to_anchor=[1.5, 0.6],
                    markerscale=0.8,
                ),
            )
            # plot.split_legend(ax,n=2, loc=["upper left", "lower left"],bbox=[[1,0.5],[1,0.5]],ncols=2,labelcolor="k",fontsize=8)

            ax = nexttile(subplot_layout[0], subplot_layout[1])
            for i, model_name in enumerate(ips.flatten(res_val["pr_curve"].index)):
                try:
                    plot_pr_curve(
                        recall=res_val["pr_curve"][model_name]["recall"][iclass],
                        precision=res_val["pr_curve"][model_name]["precision"][iclass],
                        avg_precision=res_val["pr_curve"][model_name]["avg_precision"][
                            iclass
                        ],
                        model_name=model_name,
                        color=colors[i],
                        lw=1.5,
                        alpha=alpha,
                        ax=ax,
                    )
                except Exception as e:
                    print(e)
            plot.figsets(
                sp=2,
                title=class_,
                legend=dict(
                    loc="upper right", ncols=1, fontsize=8, bbox_to_anchor=[1.5, 0.5]
                ),
            )


def plot_validate_features_single(res_val, figsize=None, is_binary=True):
    if is_binary:
        if figsize is None:
            nexttile = plot.subplot(
                len(ips.flatten(res_val["pr_curve"].index)),
                3,
                figsize=[13, 4 * len(ips.flatten(res_val["pr_curve"].index))],
            )
        else:
            nexttile = plot.subplot(
                len(ips.flatten(res_val["pr_curve"].index)), 3, figsize=figsize
            )
        for model_name in ips.flatten(res_val["pr_curve"].index):
            try:
                fpr = res_val["roc_curve"][model_name]["fpr"]
                tpr = res_val["roc_curve"][model_name]["tpr"]
                (lower_ci, upper_ci) = res_val["roc_curve"][model_name]["ci95"]
                mean_auc = res_val["roc_curve"][model_name]["auc"]

                # Plotting
                plot_roc_curve(
                    fpr,
                    tpr,
                    mean_auc,
                    lower_ci,
                    upper_ci,
                    model_name=model_name,
                    ax=nexttile(),
                )
                plot.figsets(title=model_name, sp=2)

                plot_pr_binary(
                    recall=res_val["pr_curve"][model_name]["recall"],
                    precision=res_val["pr_curve"][model_name]["precision"],
                    avg_precision=res_val["pr_curve"][model_name]["avg_precision"],
                    model_name=model_name,
                    ax=nexttile(),
                )
                plot.figsets(title=model_name, sp=2)

                # plot cm
                plot_cm(
                    res_val["confusion_matrix"][model_name], ax=nexttile(), normalize=False
                )
                plot.figsets(title=model_name, sp=2)
                
            except Exception as e:
                print(e)
    else:

        modname_tmp = ips.flatten(res_val["roc_curve"].index)[0]
        classes = list(res_val["roc_curve"][modname_tmp]["fpr"].keys())
        if figsize is None:
            nexttile = plot.subplot(
                len(modname_tmp), 3, figsize=[15, len(modname_tmp) * 5]
            )
        else:
            nexttile = plot.subplot(len(modname_tmp), 3, figsize=figsize)
        colors = plot.get_color(len(classes))
        for i, model_name in enumerate(ips.flatten(res_val["pr_curve"].index)):
            ax = nexttile()
            for iclass, class_ in enumerate(classes):
                try:
                    fpr = res_val["roc_curve"][model_name]["fpr"][class_]
                    tpr = res_val["roc_curve"][model_name]["tpr"][class_]
                    (lower_ci, upper_ci) = res_val["roc_curve"][model_name]["ci95"][iclass]
                    mean_auc = res_val["roc_curve"][model_name]["auc"][class_]
                    plot_roc_curve(
                        fpr,
                        tpr,
                        mean_auc,
                        lower_ci,
                        upper_ci,
                        model_name=class_,
                        lw=1.5,
                        color=colors[iclass],
                        alpha=0.03,
                        ax=ax,
                    )
                except Exception as e:
                    print(e)
            plot.figsets(
                sp=2,
                title=model_name,
                legend=dict(
                    loc="best",
                    fontsize=8,
                ),
            )

            ax = nexttile()
            for iclass, class_ in enumerate(classes):
                try:
                    plot_pr_curve(
                        recall=res_val["pr_curve"][model_name]["recall"][iclass],
                        precision=res_val["pr_curve"][model_name]["precision"][iclass],
                        avg_precision=res_val["pr_curve"][model_name]["avg_precision"][
                            iclass
                        ],
                        model_name=class_,
                        color=colors[iclass],
                        lw=1.5,
                        alpha=0.03,
                        ax=ax,
                    )
                except Exception as e:
                    print(e)
            plot.figsets(
                sp=2,
                title=class_,
                legend=dict(loc="best", fontsize=8),
            )

            plot_cm(
                res_val["confusion_matrix"][model_name],
                labels_name=classes,
                ax=nexttile(),
                normalize=False,
            )
            plot.figsets(title=model_name, sp=2)


def cal_precision_recall(y_true, y_pred_proba, is_binary=True):
    if is_binary:
        precision_, recall_, _ = precision_recall_curve(y_true, y_pred_proba)
        avg_precision_ = average_precision_score(y_true, y_pred_proba)
        return precision_, recall_, avg_precision_
    else:
        n_classes = y_pred_proba.shape[1]  # Number of classes
        precision_ = []
        recall_ = []

        # One-vs-rest approach for multi-class precision-recall curve
        for class_idx in range(n_classes):
            precision, recall, _ = precision_recall_curve(
                (y_true == class_idx).astype(
                    int
                ),  # Binarize true labels for the current class
                y_pred_proba[:, class_idx],  # Probabilities for the current class
            )

            precision_.append(precision)
            recall_.append(recall)
        # Optionally, you can compute average precision for each class
        avg_precision_ = []
        for class_idx in range(n_classes):
            avg_precision = average_precision_score(
                (y_true == class_idx).astype(
                    int
                ),  # Binarize true labels for the current class
                y_pred_proba[:, class_idx],  # Probabilities for the current class
            )
            avg_precision_.append(avg_precision)
        return precision_, recall_, avg_precision_


def cal_auc_ci(
    y_true,
    y_pred,
    n_bootstraps=1000,
    ci=0.95,
    random_state=1,
    is_binary=True,
    verbose=True,
):
    if is_binary:
        y_true = np.asarray(y_true)
        y_pred = np.asarray(y_pred)
        bootstrapped_scores = []
        if verbose:
            print("auroc score:", roc_auc_score(y_true, y_pred))
        rng = np.random.RandomState(random_state)
        for i in range(n_bootstraps):
            # bootstrap by sampling with replacement on the prediction indices
            indices = rng.randint(0, len(y_pred), len(y_pred))
            if len(np.unique(y_true[indices])) < 2:
                # We need at least one positive and one negative sample for ROC AUC
                # to be defined: reject the sample
                continue
            if isinstance(y_true, np.ndarray):
                score = roc_auc_score(y_true[indices], y_pred[indices])
            else:
                score = roc_auc_score(y_true.iloc[indices], y_pred.iloc[indices])
            bootstrapped_scores.append(score)
            # print("Bootstrap #{} ROC area: {:0.3f}".format(i + 1, score))
        sorted_scores = np.array(bootstrapped_scores)
        sorted_scores.sort()
 
        confidence_lower = sorted_scores[int((1 - ci) * len(sorted_scores))]
        confidence_upper = sorted_scores[int(ci * len(sorted_scores))]
        if verbose:
            print(
                "Confidence interval for the score: [{:0.3f} - {:0.3f}]".format(
                    confidence_lower, confidence_upper
                )
            )
        return confidence_lower, confidence_upper
    else:
        from sklearn.preprocessing import label_binarize

        # Multi-class classification case
        y_true = np.asarray(y_true)
        y_pred = np.asarray(y_pred)

        # Binarize the multi-class labels for OvR computation
        y_true_bin = label_binarize(
            y_true, classes=np.unique(y_true)
        )  # One-vs-Rest transformation
        n_classes = y_true_bin.shape[1]  # Number of classes
 
        bootstrapped_scores = np.full((n_classes, n_bootstraps), np.nan)
        if verbose:
            print("AUROC scores for each class:")
            for i in range(n_classes):
                print(f"Class {i}: {roc_auc_score(y_true_bin[:, i], y_pred[:, i])}")

        rng = np.random.RandomState(random_state)
        for i in range(n_bootstraps):
            indices = rng.randint(0, len(y_pred), len(y_pred))
            for class_idx in range(n_classes):
                if len(np.unique(y_true_bin[indices, class_idx])) < 2:
                    continue  # Reject if the class doesn't have both positive and negative samples
                score = roc_auc_score(
                    y_true_bin[indices, class_idx], y_pred[indices, class_idx]
                )
                bootstrapped_scores[class_idx, i] = score

        # Calculating the confidence intervals for each class
        confidence_intervals = []
        for class_idx in range(n_classes):
            # rm nan
            valid_scores = bootstrapped_scores[class_idx][
                ~np.isnan(bootstrapped_scores[class_idx])
            ]
            if len(valid_scores) > 0:
                sorted_scores = np.sort(valid_scores)
                confidence_lower = sorted_scores[int((1 - ci) * len(sorted_scores))]
                confidence_upper = sorted_scores[int(ci * len(sorted_scores))]
                confidence_intervals[class_idx] = (confidence_lower, confidence_upper)

                if verbose:
                    print(
                        f"Class {class_idx} - Confidence interval: [{confidence_lower:.3f} - {confidence_upper:.3f}]"
                    )
            else:
                confidence_intervals[class_idx] = (np.nan, np.nan)
                if verbose:
                    print(f"Class {class_idx} - Confidence interval: [NaN - NaN]") 

        return confidence_intervals


def plot_roc_curve(
    fpr=None,
    tpr=None,
    mean_auc=None,
    lower_ci=None,
    upper_ci=None,
    model_name=None,
    color="#FF8F00",
    lw=2,
    alpha=0.1,
    ci_display=True,
    title="ROC Curve",
    xlabel="1−Specificity",
    ylabel="Sensitivity",
    legend_loc="lower right",
    diagonal_color="0.5",
    figsize=(5, 5),
    ax=None,
    **kwargs,
):
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    if mean_auc is not None:
        model_name = "ROC curve" if model_name is None else model_name
        if ci_display:
            label = f"{model_name} (AUC = {mean_auc:.3f})\n95% CI: {lower_ci:.3f} - {upper_ci:.3f}"
        else:
            label = f"{model_name} (AUC = {mean_auc:.3f})"
    else:
        label = None

    # Plot ROC curve and the diagonal reference line
    ax.fill_between(fpr, tpr, alpha=alpha, color=color)
    ax.plot([0, 1], [0, 1], color=diagonal_color, clip_on=False, linestyle="--")
    ax.plot(fpr, tpr, color=color, lw=lw, label=label, clip_on=False, **kwargs)
    # Setting plot limits, labels, and title
    ax.set_xlim([-0.01, 1.0])
    ax.set_ylim([0.0, 1.0])
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend(loc=legend_loc)
    return ax


# * usage: ml2ls.plot_roc_curve(fpr, tpr, mean_auc, lower_ci, upper_ci)
# for model_name in flatten(validation_results["roc_curve"].keys())[2:]:
#     fpr = validation_results["roc_curve"][model_name]["fpr"]
#     tpr = validation_results["roc_curve"][model_name]["tpr"]
#     (lower_ci, upper_ci) = validation_results["roc_curve"][model_name]["ci95"]
#     mean_auc = validation_results["roc_curve"][model_name]["auc"]

#     # Plotting
#     ml2ls.plot_roc_curve(fpr, tpr, mean_auc, lower_ci, upper_ci)
#     figsets(title=model_name)


def plot_pr_curve(
    recall=None,
    precision=None,
    avg_precision=None,
    model_name=None,
    lw=2,
    figsize=[5, 5],
    title="Precision-Recall Curve",
    xlabel="Recall",
    ylabel="Precision",
    alpha=0.1,
    color="#FF8F00",
    legend_loc="lower left",
    ax=None,
    **kwargs,
):
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    model_name = "PR curve" if model_name is None else model_name
    # Plot Precision-Recall curve
    ax.plot(
        recall,
        precision,
        lw=lw,
        color=color,
        label=(f"{model_name} (AP={avg_precision:.2f})"),
        clip_on=False,
        **kwargs,
    )
    # Fill area under the curve
    ax.fill_between(recall, precision, alpha=alpha, color=color)

    # Customize axes
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_xlim([-0.01, 1.0])
    ax.set_ylim([0.0, 1.0])
    ax.grid(False)
    ax.legend(loc=legend_loc)
    return ax


# * usage: ml2ls.plot_pr_curve()
# for md_name in flatten(validation_results["pr_curve"].keys()):
#     ml2ls.plot_pr_curve(
#         recall=validation_results["pr_curve"][md_name]["recall"],
#         precision=validation_results["pr_curve"][md_name]["precision"],
#         avg_precision=validation_results["pr_curve"][md_name]["avg_precision"],
#         model_name=md_name,
#         lw=2,
#         alpha=0.1,
#         color="r",
#     )


def plot_pr_binary(
    recall=None,
    precision=None,
    avg_precision=None,
    model_name=None,
    lw=2,
    figsize=[5, 5],
    title="Precision-Recall Curve",
    xlabel="Recall",
    ylabel="Precision",
    alpha=0.1,
    color="#FF8F00",
    legend_loc="lower left",
    ax=None,
    show_avg_precision=False,
    **kwargs,
):
    from scipy.interpolate import interp1d

    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    model_name = "Binary PR Curve" if model_name is None else model_name

    # * use sklearn bulitin function 'PrecisionRecallDisplay'?
    # from sklearn.metrics import PrecisionRecallDisplay
    # disp = PrecisionRecallDisplay(precision=precision,
    #                               recall=recall,
    #                               average_precision=avg_precision,**kwargs)
    # disp.plot(ax=ax, name=model_name, color=color)

    # Plot Precision-Recall curve
    ax.plot(
        recall,
        precision,
        lw=lw,
        color=color,
        label=(f"{model_name} (AP={avg_precision:.2f})"),
        clip_on=False,
        **kwargs,
    )

    # Fill area under the curve
    ax.fill_between(recall, precision, alpha=alpha, color=color)
    # Add F1 score iso-contours
    f_scores = np.linspace(0.2, 0.8, num=4)
    # for f_score in f_scores:
    #     x = np.linspace(0.01, 1)
    #     y = f_score * x / (2 * x - f_score)
    #     plt.plot(x[y >= 0], y[y >= 0], color="gray", alpha=1)
    #     plt.annotate(f"$f_1={f_score:0.1f}$", xy=(0.8, y[45] + 0.02))

    pr_boundary = interp1d(recall, precision, kind="linear", fill_value="extrapolate")
    for f_score in f_scores:
        x_vals = np.linspace(0.01, 1, 20000)
        y_vals = f_score * x_vals / (2 * x_vals - f_score)
        y_vals_clipped = np.minimum(y_vals, pr_boundary(x_vals))
        y_vals_clipped = np.clip(y_vals_clipped, 1e-3, None)  # Prevent going to zero
        valid = y_vals_clipped < pr_boundary(x_vals)
        valid_ = y_vals_clipped > 1e-3
        valid = valid & valid_
        x_vals = x_vals[valid]
        y_vals_clipped = y_vals_clipped[valid]
        if len(x_vals) > 0:  # Ensure annotation is placed only if line segment exists
            ax.plot(x_vals, y_vals_clipped, color="gray", alpha=1)
            plt.annotate(
                f"$f_1={f_score:0.1f}$",
                xy=(0.8, y_vals_clipped[-int(len(y_vals_clipped) * 0.35)] + 0.02),
            )

    # # Plot the average precision line
    if show_avg_precision:
        plt.axhline(
            y=avg_precision,
            color="red",
            ls="--",
            lw=lw,
            label=f"Avg. precision={avg_precision:.2f}",
        )
    # Customize axes
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_xlim([-0.01, 1.0])
    ax.set_ylim([0.0, 1.0])
    ax.grid(False)
    ax.legend(loc=legend_loc)
    return ax


def plot_cm(
    cm,
    labels_name=None,
    thresh=0.8,  # for set color
    axis_labels=None,
    cmap="Reds",
    normalize=True,
    xlabel="Predicted Label",
    ylabel="Actual Label",
    fontsize=12,
    figsize=[5, 5],
    ax=None,
):
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)

    cm_normalized = np.round(
        cm.astype("float") / cm.sum(axis=1)[:, np.newaxis] * 100, 2
    )
    cm_value = cm_normalized if normalize else cm.astype("int")
    # Plot the heatmap
    cax = ax.imshow(cm_normalized, interpolation="nearest", cmap=cmap)
    plt.colorbar(cax, ax=ax, fraction=0.046, pad=0.04)
    cax.set_clim(0, 100)

    # Define tick labels based on provided labels
    num_local = np.arange(len(labels_name)) if labels_name is not None else range(2)
    if axis_labels is None:
        axis_labels = labels_name if labels_name is not None else ["No", "Yes"]
    ax.set_xticks(num_local)
    ax.set_xticklabels(axis_labels)
    ax.set_yticks(num_local)
    ax.set_yticklabels(axis_labels)
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)

    # Add TN, FP, FN, TP annotations specifically for binary classification (2x2 matrix)
    if labels_name is None or len(labels_name) == 2:
        # True Negative (TN), False Positive (FP), False Negative (FN), and True Positive (TP)
        #                 Predicted
        #                0   |   1
        #             ----------------
        #         0 |   TN   |  FP
        # Actual      ----------------
        #         1 |   FN   |  TP
        tn_label = "TN"
        fp_label = "FP"
        fn_label = "FN"
        tp_label = "TP"

        # Adjust positions slightly for TN, FP, FN, TP labels
        ax.text(
            0,
            0,
            (
                f"{tn_label}:{cm_normalized[0, 0]:.2f}%"
                if normalize
                else f"{tn_label}:{cm_value[0, 0]}"
            ),
            ha="center",
            va="center",
            color="white" if cm_normalized[0, 0] > thresh * 100 else "black",
            fontsize=fontsize,
        )
        ax.text(
            1,
            0,
            (
                f"{fp_label}:{cm_normalized[0, 1]:.2f}%"
                if normalize
                else f"{fp_label}:{cm_value[0, 1]}"
            ),
            ha="center",
            va="center",
            color="white" if cm_normalized[0, 1] > thresh * 100 else "black",
            fontsize=fontsize,
        )
        ax.text(
            0,
            1,
            (
                f"{fn_label}:{cm_normalized[1, 0]:.2f}%"
                if normalize
                else f"{fn_label}:{cm_value[1, 0]}"
            ),
            ha="center",
            va="center",
            color="white" if cm_normalized[1, 0] > thresh * 100 else "black",
            fontsize=fontsize,
        )
        ax.text(
            1,
            1,
            (
                f"{tp_label}:{cm_normalized[1, 1]:.2f}%"
                if normalize
                else f"{tp_label}:{cm_value[1, 1]}"
            ),
            ha="center",
            va="center",
            color="white" if cm_normalized[1, 1] > thresh * 100 else "black",
            fontsize=fontsize,
        )
    else:
        # Annotate cells with normalized percentage values
        for i in range(len(labels_name)):
            for j in range(len(labels_name)):
                val = cm_normalized[i, j]
                color = "white" if val > thresh * 100 else "black"
                ax.text(
                    j,
                    i,
                    f"{val:.2f}%",
                    ha="center",
                    va="center",
                    color=color,
                    fontsize=fontsize,
                )

    plot.figsets(ax=ax, boxloc="none")
    return ax


def rank_models(
    cv_test_scores,
    rm_outlier=False,
    metric_weights=None,
    plot_=True,
):
    """
    Selects the best model based on a multi-metric scoring approach, with outlier handling, optional visualization,
    and additional performance metrics.

    Parameters:
    - cv_test_scores (pd.DataFrame): DataFrame with cross-validation results across multiple metrics.
                                     Assumes columns are 'Classifier', 'accuracy', 'precision', 'recall', 'f1', 'roc_auc'.
    - metric_weights (dict): Dictionary specifying weights for each metric (e.g., {'accuracy': 0.2, 'precision': 0.3, ...}).
                             If None, default weights are applied equally across available metrics.
                a. equal_weights(standard approch): 所有的metrics同等重要
                    e.g., {"accuracy": 0.2, "precision": 0.2, "recall": 0.2, "f1": 0.2, "roc_auc": 0.2}
                b. accuracy_focosed:  classification correctness (e.g., in balanced datasets), accuracy might be weighted more heavily.
                    e.g., {"accuracy": 0.4, "precision": 0.2, "recall": 0.2, "f1": 0.1, "roc_auc": 0.1}
                c. Precision and Recall Emphasis: In cases where false positives and false negatives are particularly important (such as
                    in medical applications or fraud detection), precision and recall may be weighted more heavily.
                    e.g., {"accuracy": 0.2, "precision": 0.3, "recall": 0.3, "f1": 0.1, "roc_auc": 0.1}
                d. F1-Focused: When balance between precision and recall is crucial (e.g., in imbalanced datasets)
                    e.g., {"accuracy": 0.2, "precision": 0.2, "recall": 0.2, "f1": 0.3, "roc_auc": 0.1}
                e. ROC-AUC Emphasis: In some cases, ROC AUC may be prioritized, particularly in classification tasks where class imbalance
                    is present, as ROC AUC accounts for the model's performance across all classification thresholds.
                    e.g., {"accuracy": 0.1, "precision": 0.2, "recall": 0.2, "f1": 0.3, "roc_auc": 0.3}

    - normalize (bool): Whether to normalize scores of each metric to range [0, 1].
    - visualize (bool): If True, generates visualizations (e.g., bar plot, radar chart).
    - outlier_threshold (float): The threshold to detect outliers using the IQR method. Default is 1.5.
    - cv_folds (int): The number of cross-validation folds used.

    Returns:
    - best_model (str): Name of the best model based on the combined metric scores.
    - scored_df (pd.DataFrame): DataFrame with an added 'combined_score' column used for model selection.
    - visualizations (dict): A dictionary containing visualizations if `visualize=True`.
    """
    from sklearn.preprocessing import MinMaxScaler
    import seaborn as sns
    import matplotlib.pyplot as plt
    from py2ls import plot

    # Check for missing metrics and set default weights if not provided
    available_metrics = cv_test_scores.columns[1:]  # Exclude 'Classifier' column
    if metric_weights is None:
        metric_weights = {
            metric: 1 / len(available_metrics) for metric in available_metrics
        }  # Equal weight if not specified
    elif metric_weights == "a":
        metric_weights = {
            "accuracy": 0.2,
            "precision": 0.2,
            "recall": 0.2,
            "f1": 0.2,
            "roc_auc": 0.2,
        }
    elif metric_weights == "b":
        metric_weights = {
            "accuracy": 0.4,
            "precision": 0.2,
            "recall": 0.2,
            "f1": 0.1,
            "roc_auc": 0.1,
        }
    elif metric_weights == "c":
        metric_weights = {
            "accuracy": 0.2,
            "precision": 0.3,
            "recall": 0.3,
            "f1": 0.1,
            "roc_auc": 0.1,
        }
    elif metric_weights == "d":
        metric_weights = {
            "accuracy": 0.2,
            "precision": 0.2,
            "recall": 0.2,
            "f1": 0.3,
            "roc_auc": 0.1,
        }
    elif metric_weights == "e":
        metric_weights = {
            "accuracy": 0.1,
            "precision": 0.2,
            "recall": 0.2,
            "f1": 0.3,
            "roc_auc": 0.3,
        }
    else:
        metric_weights = {
            metric: 1 / len(available_metrics) for metric in available_metrics
        }

    # Normalize weights if they don’t sum to 1
    total_weight = sum(metric_weights.values())
    metric_weights = {
        metric: weight / total_weight for metric, weight in metric_weights.items()
    }
    if rm_outlier:
        cv_test_scores_ = ips.df_outlier(cv_test_scores)
    else:
        cv_test_scores_ = cv_test_scores

    # Normalize the scores of metrics if normalize is True
    scaler = MinMaxScaler()
    normalized_scores = pd.DataFrame(
        scaler.fit_transform(cv_test_scores_[available_metrics]),
        columns=available_metrics,
    )
    cv_test_scores_ = pd.concat(
        [cv_test_scores_[["Classifier"]], normalized_scores], axis=1
    )

    # Calculate weighted scores for each model
    cv_test_scores_["combined_score"] = sum(
        cv_test_scores_[metric] * weight for metric, weight in metric_weights.items()
    )
    top_models = cv_test_scores_.sort_values(by="combined_score", ascending=False)
    cv_test_scores = cv_test_scores.loc[top_models.index]
    top_models.reset_index(drop=True, inplace=True)
    cv_test_scores.reset_index(drop=True, inplace=True)

    if plot_:

        def generate_bar_plot(ax, cv_test_scores):
            ax = plot.plotxy(
                y="Classifier", x="combined_score", data=cv_test_scores, kind_="bar"
            )
            plt.title("Classifier Performance")
            plt.tight_layout()
            return plt

        nexttile = plot.subplot(2, 2, figsize=[10, 10])
        generate_bar_plot(nexttile(), top_models.dropna())
        plot.radar(
            ax=nexttile(projection="polar"),
            data=cv_test_scores.set_index("Classifier"),
            ylim=[0, 1],
            color=plot.get_color(cv_test_scores.set_index("Classifier").shape[1]),
            alpha=0.02,
            circular=1,
        )
    return cv_test_scores


# # Example Usage:
# metric_weights = {
#     "accuracy": 0.2,
#     "precision": 0.3,
#     "recall": 0.2,
#     "f1": 0.2,
#     "roc_auc": 0.1,
# }
# cv_test_scores = res["cv_test_scores"].copy()
# best_model = rank_models(
#     cv_test_scores, metric_weights=metric_weights, normalize=True, plot_=True
# )

# figsave("classifier_performance.pdf")
def rank_models_reg(df, ascending=False):
    """
    Sorts models based on MSE, RMSE, MAE, and R² with custom priority logic.

    Parameters:
        df (pd.DataFrame): DataFrame containing the regression metrics.
        ascending (bool): Whether to sort in ascending order of ranking score.

    Returns:
        pd.DataFrame: Sorted DataFrame with an added "Ranking_Score" column.
    """
    # Define weights for the 4 metrics
    weights = {
        "mse": -1,  # Lower is better
        "rmse": -1,  # Lower is better
        "mae": -1,  # Lower is better
        "r2": 1,    # Higher is better
    }

    # Normalize the selected metrics
    df = df.copy()  # Work on a copy of the DataFrame
    for metric, weight in weights.items():
        if metric in df.columns:
            if weight > 0:  # Higher is better; normalize 0-1
                df[metric + "_normalized"] = (df[metric] - df[metric].min()) / (
                    df[metric].max() - df[metric].min()
                )
            else:  # Lower is better; reverse normalize 0-1
                df[metric + "_normalized"] = (df[metric].max() - df[metric]) / (
                    df[metric].max() - df[metric].min()
                )

    # Calculate ranking score as a weighted sum
    df["Ranking_Score"] = sum(
        df[metric + "_normalized"] * abs(weights[metric])
        for metric in weights.keys()
        if metric + "_normalized" in df.columns
    )

    # Sort models based on the ranking score
    sorted_df = df.sort_values(by="Ranking_Score", ascending=ascending)
    return sorted_df

models_support = {
    "classification": {
        "Random Forest": "Tree-Based",
        "SVM": "Kernel-Based",
        "Logistic Regression": "Linear",
        "Lasso Logistic Regression": "Linear",
        "Gradient Boosting": "Tree-Based",
        "XGBoost": "Tree-Based",
        "KNN": "Instance-Based",
        "Naive Bayes": "Probabilistic",
        "Linear Discriminant Analysis": "Linear",
        "AdaBoost": "Tree-Based",
        "CatBoost": "Tree-Based",
        "Extra Trees": "Tree-Based",
        "Bagging": "Tree-Based",
        "Neural Network": "Neural Network",
        "DecisionTree": "Tree-Based",
        "Quadratic Discriminant Analysis": "Probabilistic",
        "Ridge": "Linear",
        "Perceptron": "Linear",
        "Bernoulli Naive Bayes": "Probabilistic",
        "SGDClassifier": "Linear",
    },
    "regression": {
        "Linear Regression": "Linear",
        "Ridge": "Linear",
        "RidgeCV": "Linear",
        "TheilSenRegressor": "Linear",
        "HuberRegressor": "Linear",
        "PoissonRegressor": "Linear",
        "LassoCV": "Linear",
        "Bagging": "Tree-Based",
        "ElasticNet": "Linear",
        "Random Forest": "Tree-Based",
        "Gradient Boosting": "Tree-Based",
        "XGBoost": "Tree-Based",
        "CatBoost": "Tree-Based",
        "Extra Trees": "Tree-Based",
        "SVM": "Kernel-Based",
        "KNN": "Instance-Based",
        "Neural Network": "Neural Network",
        "AdaBoost": "Linear",
    },
}
def select_top_models(models, categories, n_top_models, n_models_per_category=1):
    """
    models = list_sort
    purpose = "regression"
    categories = models_support[purpose]
    n_top_models = 3
    select_top_models(models, categories, n_top_models)
    """
    selected = {}
    result = []
    for model in models:
        category = categories.get(model, "Unknown")
        if category not in selected:
            selected[category] = 0  # Initialize counter for the category
        
        if selected[category] < n_models_per_category:  # Allow additional models up to the limit
            selected[category] += 1
            result.append(model)
        
        if len(result) == n_top_models:  # Stop when the desired number of models is reached
            break
    
    return result

def predict(
    x_train: pd.DataFrame,
    y_train: pd.Series,
    x_true: pd.DataFrame = None,
    y_true: Optional[pd.Series] = None,
    fill_missing:bool = True, 
    scaler:str='standard',# ["standard", "minmax", "robust","maxabs"]
    backward: bool = False,  # backward_regression
    backward_thr:float = 0.05,# pval thr,only works when backward is True
    common_features: set = None,
    purpose: str = "classification",  # 'classification' or 'regression'
    cls: Optional[Dict[str, Any]] = None,
    metrics: Optional[List[str]] = None,
    stack:bool=True,# run stacking
    stacking_cv:bool=False,# stacking cross_validate, default(False),keep it simple
    vote:bool=False,# run voting
    voting:str="hard", # only for classification purporse of voting
    n_top_models:int=5, #for stacking models
    n_models_per_category:int=1, #for stacking models,可以允许同一个类别2种模型
    smote: bool = False,
    n_jobs: int = -1,
    plot_: bool = True,
    dir_save: str = "./",
    test_size: float = 0.2,  # specific only when x_true is None
    cv_folds: int = 5,  # more cv_folds 得更加稳定,auc可能更低
    cv_level: str = "l",  # "s":'low',"m":'medium',"l":"high"
    class_weight: str = "balanced",
    random_state: int = 1,
    presets = "best_quality",# specific for autogluon
    time_limit=600, # specific for autogluon
    num_bag_folds=5, # specific for autogluon
    num_stack_levels=2, # specific for autogluon
    verbose: bool = False,
    **kwargs
) -> pd.DataFrame:
    """
    第一种情况是内部拆分，第二种是直接预测，第三种是外部验证。
    Usage:
        (1). predict(x_train, y_train,...) 对 x_train 进行拆分训练/测试集，并在测试集上进行验证.
            predict 函数会根据 test_size 参数，将 x_train 和 y_train 拆分出内部测试集。然后模型会在拆分出的训练集上进行训练，并在测试集上验证效果。
        (2). predict(x_train, y_train, x_true,...)使用 x_train 和 y_train 训练并对 x_true 进行预测
            由于传入了 x_true，函数会跳过 x_train 的拆分，直接使用全部的 x_train 和 y_train 进行训练。然后对 x_true 进行预测，但由于没有提供 y_true，
            因此无法与真实值进行对比。
        (3). predict(x_train, y_train, x_true, y_true,...)使用 x_train 和 y_train 训练，并验证 x_true 与真实标签 y_true.
            predict 函数会在 x_train 和 y_train 上进行训练，并将 x_true 作为测试集。由于提供了 y_true，函数可以将预测结果与 y_true 进行对比，从而
            计算验证指标，完成对 x_true 的真正验证。
    trains and validates a variety of machine learning models for both classification and regression tasks.
    It supports hyperparameter tuning with grid search and includes additional features like cross-validation,
    feature scaling, and handling of class imbalance through SMOTE.

    Parameters:
        - x_train (pd.DataFrame):Training feature data, structured with each row as an observation and each column as a feature.
        - y_train (pd.Series):Target variable for the training dataset.
        - x_true (pd.DataFrame, optional):Test feature data. If not provided, the function splits x_train based on test_size.
        - y_true (pd.Series, optional):Test target values. If not provided, y_train is split into training and testing sets.
        - common_features (set, optional):Specifies a subset of features common across training and test data.
        - purpose (str, default = "classification"):Defines whether the task is "classification" or "regression". Determines which
            metrics and models are applied.
        - cls (dict, optional):Dictionary to specify custom classifiers/regressors. Defaults to a set of common models if not provided.
        - metrics (list, optional):List of evaluation metrics (like accuracy, F1 score) used for model evaluation.
        - random_state (int, default = 1):Random seed to ensure reproducibility.
        - smote (bool, default = False):Applies Synthetic Minority Oversampling Technique (SMOTE) to address class imbalance if enabled.
        - n_jobs (int, default = -1):Number of parallel jobs for computation. Set to -1 to use all available cores.
        - plot_ (bool, default = True):If True, generates plots of the model evaluation metrics.
        - test_size (float, default = 0.2):Test data proportion if x_true is not provided.
        - cv_folds (int, default = 5):Number of cross-validation folds.
        - cv_level (str, default = "l"):Sets the detail level of cross-validation. "s" for low, "m" for medium, and "l" for high.
        - class_weight (str, default = "balanced"):Balances class weights in classification tasks.
        - verbose (bool, default = False):If True, prints detailed output during model training.
        - dir_save (str, default = "./"):Directory path to save plot outputs and results.

    Key Steps in the Function:
        Model Initialization: Depending on purpose, initializes either classification or regression models.
        Feature Selection: Ensures training and test sets have matching feature columns.
        SMOTE Application: Balances classes if smote is enabled and the task is classification.
        Cross-Validation and Hyperparameter Tuning: Utilizes GridSearchCV for model tuning based on cv_level.
        Evaluation and Plotting: Outputs evaluation metrics like AUC, confusion matrices, and optional plotting of performance metrics.
    """
    from tqdm import tqdm
    from sklearn.ensemble import (
        RandomForestClassifier,
        RandomForestRegressor,
        ExtraTreesClassifier,
        ExtraTreesRegressor,
        HistGradientBoostingRegressor,
        BaggingClassifier,
        BaggingRegressor,
        AdaBoostClassifier,
        AdaBoostRegressor,
    )
    from sklearn.svm import SVC, SVR, LinearSVR, NuSVR
    from sklearn.tree import DecisionTreeRegressor,ExtraTreeRegressor
    from sklearn.linear_model import (
        LogisticRegression,ElasticNet,ElasticNetCV,
        LinearRegression,Lasso,RidgeClassifierCV,Perceptron,SGDClassifier,
        RidgeCV,Ridge,TheilSenRegressor,HuberRegressor,PoissonRegressor,Lars, LassoLars, BayesianRidge,
        GammaRegressor, TweedieRegressor, LassoCV, LassoLarsCV, LarsCV,
        OrthogonalMatchingPursuit, OrthogonalMatchingPursuitCV, PassiveAggressiveRegressor
    )
    from sklearn.compose import TransformedTargetRegressor
    from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
    from sklearn.naive_bayes import GaussianNB, BernoulliNB
    from sklearn.ensemble import GradientBoostingClassifier, GradientBoostingRegressor,StackingClassifier,StackingRegressor
    import xgboost as xgb
    import lightgbm as lgb
    import catboost as cb
    from sklearn.neural_network import MLPClassifier, MLPRegressor
    from sklearn.model_selection import GridSearchCV, StratifiedKFold, KFold
    from sklearn.discriminant_analysis import (
        LinearDiscriminantAnalysis,
        QuadraticDiscriminantAnalysis,
    )
    from sklearn.preprocessing import PolynomialFeatures
    from sklearn.model_selection import train_test_split
 
    from sklearn.gaussian_process import GaussianProcessRegressor
    from sklearn.kernel_ridge import KernelRidge
    from sklearn.dummy import DummyRegressor
    from autogluon.tabular import TabularPredictor
    # 拼写检查
    purpose = ips.strcmp(purpose, ["classification", "regression"])[0]
    print(f"{purpose} processing...")

    
    # Default models or regressors if not provided
    if purpose == "classification":
        model_ = {
            "Random Forest": RandomForestClassifier(
                random_state=random_state, class_weight=class_weight,n_jobs=n_jobs
            ),
            # SVC (Support Vector Classification)
            "SVM": SVC(
                kernel="rbf",
                probability=True,
                class_weight=class_weight,
                random_state=random_state,
            ),
            # fit the best model without enforcing sparsity, which means it does not directly perform feature selection.
            "Logistic Regression": LogisticRegression(
                class_weight=class_weight, random_state=random_state,n_jobs=n_jobs
            ),
            # Logistic Regression with L1 Regularization (Lasso)
            "Lasso Logistic Regression": LogisticRegression(
                penalty="l1", solver="saga", random_state=random_state
            ),
            "Gradient Boosting": GradientBoostingClassifier(random_state=random_state),
            "XGBoost": xgb.XGBClassifier(
                eval_metric="logloss",
                random_state=random_state,
            ),
            "KNN": KNeighborsClassifier(n_neighbors=5,n_jobs=n_jobs),
            "Naive Bayes": GaussianNB(),
            "Linear Discriminant Analysis": LinearDiscriminantAnalysis(),
            "AdaBoost": AdaBoostClassifier(
                algorithm="SAMME", random_state=random_state
            ),
            "LightGBM": lgb.LGBMClassifier(random_state=random_state, class_weight=class_weight,n_jobs=n_jobs),
            "CatBoost": cb.CatBoostClassifier(verbose=0, random_state=random_state),
            "Extra Trees": ExtraTreesClassifier(
                random_state=random_state, class_weight=class_weight,n_jobs=n_jobs
            ),
            "Bagging": BaggingClassifier(random_state=random_state,n_jobs=n_jobs),
            "Neural Network": MLPClassifier(max_iter=500, random_state=random_state),
            "DecisionTree": DecisionTreeClassifier(),
            "Quadratic Discriminant Analysis": QuadraticDiscriminantAnalysis(),
            "Ridge": RidgeClassifierCV(
                class_weight=class_weight, store_cv_results=True
            ),
            "Perceptron": Perceptron(random_state=random_state,n_jobs=n_jobs),
            "Bernoulli Naive Bayes": BernoulliNB(),
            "SGDClassifier": SGDClassifier(random_state=random_state,n_jobs=n_jobs),
        }
    elif purpose == "regression":
        model_ = {
            "Random Forest": RandomForestRegressor(random_state=random_state,n_jobs=n_jobs),
            "SVM": SVR(),  # SVR (Support Vector Regression)
            "LassoCV": LassoCV(cv=cv_folds, random_state=random_state,n_jobs=n_jobs),  # LassoCV自动找出最适alpha,优于Lasso
            "Gradient Boosting": GradientBoostingRegressor(random_state=random_state),
            "XGBoost": xgb.XGBRegressor(eval_metric="rmse", random_state=random_state,n_jobs=n_jobs),
            "Linear Regression": LinearRegression(n_jobs=n_jobs),
            "AdaBoost": AdaBoostRegressor(random_state=random_state),
            "LightGBM": lgb.LGBMRegressor(random_state=random_state,n_jobs=n_jobs,force_row_wise=True),  # Or use force_col_wise=True if memory is a concern
            "CatBoost": cb.CatBoostRegressor(verbose=0, random_state=random_state),
            "Extra Trees": ExtraTreesRegressor(random_state=random_state,n_jobs=n_jobs),
            "Bagging": BaggingRegressor(random_state=random_state,n_jobs=n_jobs),
            "Neural Network": MLPRegressor(max_iter=500, random_state=random_state),
            "ElasticNet": ElasticNet(random_state=random_state),
            "Ridge": Ridge(random_state=random_state),
            "KNN": KNeighborsRegressor(n_jobs=n_jobs),
            "TheilSen":TheilSenRegressor(n_jobs=n_jobs),
            "Huber":HuberRegressor(),
            "Poisson":PoissonRegressor(),"LinearRegression": LinearRegression(),
            "Lasso": Lasso(random_state=random_state),
            "Lars": Lars(),
            "LassoLars": LassoLars(),
            "BayesianRidge": BayesianRidge(),
            "GammaRegressor": GammaRegressor(),
            "TweedieRegressor": TweedieRegressor(),
            "LassoCV": LassoCV(random_state=random_state, n_jobs=n_jobs),
            "ElasticNetCV": ElasticNetCV(random_state=random_state, n_jobs=n_jobs),
            "LassoLarsCV": LassoLarsCV(n_jobs=n_jobs),
            "LarsCV": LarsCV(),
            "OrthogonalMatchingPursuit": OrthogonalMatchingPursuit(),
            "OrthogonalMatchingPursuitCV": OrthogonalMatchingPursuitCV(n_jobs=n_jobs),
            "PassiveAggressiveRegressor": PassiveAggressiveRegressor(random_state=random_state),
            "LinearSVR": LinearSVR(random_state=random_state),
            "NuSVR": NuSVR(),
            "DecisionTreeRegressor": DecisionTreeRegressor(random_state=random_state),
            "ExtraTreeRegressor": ExtraTreeRegressor(random_state=random_state),
            "HistGradientBoostingRegressor": HistGradientBoostingRegressor(random_state=random_state),
            "GaussianProcessRegressor": GaussianProcessRegressor(),
            "KernelRidge": KernelRidge(),
            "DummyRegressor": DummyRegressor(),
            "TransformedTargetRegressor": TransformedTargetRegressor(regressor=LinearRegression())
        }
    if cls is None:
        models = model_
    else:
        if not isinstance(cls, list):
            cls = [cls]
        models = {}
        for cls_ in cls:
            cls_ = ips.strcmp(cls_, list(model_.keys()))[0]
            models[cls_] = model_[cls_]
    if "LightGBM" in models:
        x_train = ips.df_special_characters_cleaner(x_train)
        x_true = (
            ips.df_special_characters_cleaner(x_true) if x_true is not None else None
        )

    # only keep "autogluon_tab" in models
    cls =  [cls] if isinstance(cls, str) else cls

    if cls is not None:
        models={"autogluon_tab":None} if "auto" in cls else models

    # indicate cls:
    if ips.run_once_within(30):  # 10 min
        print(f"processing: {list(models.keys())}")
    y_train_col_name=None
    # print(isinstance(y_train, str) and y_train in x_train.columns)
    if isinstance(y_train, str) and y_train in x_train.columns:
        y_train_col_name = y_train
        y_train = x_train[y_train]
        # y_train = ips.df_encoder(pd.DataFrame(y_train), method="dummy")
        x_train = x_train.drop(y_train_col_name, axis=1)
    # else:
    #     y_train = ips.df_encoder(pd.DataFrame(y_train), method="dummy").values.ravel()

    y_train = pd.DataFrame(y_train)
    if y_train.select_dtypes(include=np.number).empty:
        y_train_ = ips.df_encoder(y_train, method="dummy", drop=None)
        is_binary = False if y_train_.shape[1] > 2 else True
    else:
        y_train_ = ips.flatten(y_train.values)
        is_binary = False if len(y_train_) > 2 else True

    if is_binary:
        y_train = ips.df_encoder(pd.DataFrame(y_train), method="label")
    print("is_binary:", is_binary)

    if fill_missing:
        ips.df_fillna(data=x_train, method="knn", inplace=True, axis=0)
        ips.df_fillna(data=y_train, method="knn", inplace=True, axis=0)
    # Perform backward feature selection
    if backward:
        selected_features = backward_regression(x_train, y_train, thr=backward_thr)
        x_train = x_train[selected_features]

    if x_true is None:
        x_train, x_true, y_train, y_true = train_test_split(
            x_train,
            y_train,
            test_size=test_size,
            random_state=random_state,
            stratify=y_train if purpose == "classification" else None,
        )

        if isinstance(y_train, str) and y_train in x_train.columns:
            y_train_col_name = y_train
            y_train = x_train[y_train]
            y_train = (
                ips.df_encoder(pd.DataFrame(y_train), method="label")
                if is_binary
                else y_train
            )
            x_train = x_train.drop(y_train_col_name, axis=1)
        if is_binary:
            y_train = ips.df_encoder(
                pd.DataFrame(y_train), method="label"
            ).values.ravel()

    if fill_missing:
        ips.df_fillna(data=x_true, method="knn", inplace=True, axis=0)
    if y_true is not None:
        if isinstance(y_true, str) and y_true in x_true.columns:
            y_true_col_name = y_true
            y_true = x_true[y_true]
            y_true = (
                ips.df_encoder(pd.DataFrame(y_true), method="label")
                if is_binary
                else y_true
            )
            y_true = pd.DataFrame(y_true)
            x_true = x_true.drop(y_true_col_name, axis=1)
        if is_binary:
            y_true = ips.df_encoder(pd.DataFrame(y_true), method="label").values.ravel()
            y_true = pd.DataFrame(y_true)

    # to convert the 2D to 1D: 2D column-vector format (like [[1], [0], [1], ...]) instead of a 1D array ([1, 0, 1, ...]

    # y_train=y_train.values.ravel() if y_train is not None else None
    # y_true=y_true.values.ravel() if y_true is not None else None
    if y_train is not None:
        y_train = (
            y_train.ravel()
            if isinstance(y_train, np.ndarray)
            else y_train.values.ravel()
        )
    if y_true is not None:
        y_true = (
            y_true.ravel() if isinstance(y_true, np.ndarray) else y_true.values.ravel()
        )
    # Ensure common features are selected
    if common_features is not None:
        x_train, x_true = x_train[common_features], x_true[common_features]
        share_col_names=common_features
    else:
        share_col_names = ips.shared(x_train.columns, x_true.columns, verbose=verbose)
        x_train, x_true = x_train[share_col_names], x_true[share_col_names]

    #! scaler 
    # scaler and fit x_train and export scaler to fit the x_true
    x_train,scaler_=ips.df_scaler(x_train,method=scaler,return_scaler=True)
    # 
    x_true=ips.df_scaler(x_true,scaler=scaler_)# make sure 用于同一个scaler
    x_train, x_true = ips.df_encoder(x_train, method="dummy"), ips.df_encoder(
        x_true, method="dummy"
    )
    # Handle class imbalance using SMOTE (only for classification)
    if (
        smote
        and purpose == "classification"
        and y_train.value_counts(normalize=True).max() < 0.8
    ):
        from imblearn.over_sampling import SMOTE

        smote_sampler = SMOTE(random_state=random_state)
        x_train, y_train = smote_sampler.fit_resample(x_train, y_train)
    if not is_binary:
        if isinstance(y_train, np.ndarray):
            y_train = ips.df_encoder(data=pd.DataFrame(y_train), method="label")
            y_train = np.asarray(y_train)
        if y_true is not None:
            if isinstance(y_train, np.ndarray):
                y_true = ips.df_encoder(data=pd.DataFrame(y_true), method="label")
                y_true = np.asarray(y_true)
     #! so far, got the: x_train,x_true,y_train,y_true 
    # Grid search with KFold or StratifiedKFold
    if "autogluon_tab" in models:
        # load hypoer_param
        f_param = os.path.dirname(os.path.abspath(__file__))
        f_param = f_param + "/data/hyper_param_autogluon_zeroshot2024.json"
        with open(f_param, "r") as file:
            hyper_param_autogluon = json.load(file)
        # Train the model with AutoGluon
        features=x_train.columns.tolist()
        label= y_train_col_name if y_train_col_name is not None else 'target'
        df_autogluon = x_train.copy()
        df_autogluon[label]=y_train
        autogluon_presets=["best_quality","good_quality","fast_train"]
        best_clf = TabularPredictor(label=label, path=os.path.join(dir_save,"model_autogluon")).fit(
            train_data=df_autogluon,
            presets=ips.strcmp(presets, autogluon_presets)[0],  # 'best_quality' or 'good_quality' or 'fast_train'
            time_limit=time_limit,#3600,  # in sec:  Limit training time,
            num_bag_folds=num_bag_folds,
            num_stack_levels=num_stack_levels,
            hyperparameters=hyper_param_autogluon,
            verbosity=1 if verbose else 0,
            **kwargs
        )
        #! Get the leaderboard
        gs={}
        # Display the leaderboard for reference
        leaderboard = best_clf.leaderboard()
        gs['info']=best_clf.info()
        # gs["res"]=best_clf
        gs["features"]=features
        gs["leaderboard"] = leaderboard
        best_model_name = leaderboard.iloc[0, 0]  # First row, first column contains the model name
        # Store the best model and its details in the gs dictionary
        gs["best_estimator_"] = best_model_name  # Store the trained model, not just the name
        gs["best_params_"] = best_model_name  # Hyperparameters
        # Make predictions if x_true is provided
        if x_true is not None:
            x_true = x_true.reindex(columns=x_train.columns, fill_value=0)
            gs["predictions"] = best_clf.predict(x_true[features],model=None)# model=None select the best 
            gs["predict_proba"] = best_clf.predict_proba(x_true[features]) if purpose=='classification' else None
            x_true[label]=gs["predictions"]
            if gs["predictions"].value_counts().shape[0]>1:
                gs['evaluate'] = best_clf.evaluate(x_true[features+[label]])
        gs["models"]=leaderboard["model"].tolist()#best_clf.model_names() 
        all_models = gs["models"]
        model_evaluations = {} 
        for model in all_models:
            predictions = best_clf.predict(x_true[features], model=model) 
            evaluation = best_clf.evaluate_predictions(
                y_true=x_true[label],  # True labels
                y_pred=predictions,    # Predictions from the specific model
                auxiliary_metrics=True,  # Include additional metrics if needed
            )
            model_evaluations[model] = evaluation
        gs["scores"]=pd.DataFrame.from_dict(model_evaluations, orient='index')
        #! 试着保持一样的格式
        results = {}
        for model in all_models:
            y_pred = best_clf.predict(x_true[features], model=model).tolist()
            y_pred_proba=best_clf.predict_proba(x_true[features], model=model) if purpose=='classification' else None

            if isinstance(y_pred_proba, pd.DataFrame):
                y_pred_proba=y_pred_proba.iloc[:,1]

            # try to make predict format consistant
            try:
                y_pred= [i[0] for i in y_pred]
            except:
                pass
            try:
                y_true= [i[0] for i in y_true]
            except:
                pass
            try:
                y_train= [i[0] for i in y_train]
            except:
                pass
            validation_scores = {}
            if y_true is not None and y_pred_proba is not None:
                validation_scores = cal_metrics(
                    y_true,
                    y_pred,
                    y_pred_proba=y_pred_proba,
                    is_binary=is_binary,
                    purpose=purpose,
                    average="weighted",
                )
                if is_binary:
                    # Calculate ROC curve
                    # https://scikit-learn.org/stable/auto_examples/model_selection/plot_roc.html
                    if y_pred_proba is not None:
                        # fpr, tpr, roc_auc = dict(), dict(), dict()
                        fpr, tpr, _ = roc_curve(y_true, y_pred_proba)
                        lower_ci, upper_ci = cal_auc_ci(
                            y_true, y_pred_proba, verbose=False, is_binary=is_binary
                        )
                        roc_auc = auc(fpr, tpr)
                        roc_info = {
                            "fpr": fpr.tolist(),
                            "tpr": tpr.tolist(),
                            "auc": roc_auc,
                            "ci95": (lower_ci, upper_ci),
                        }
                        # precision-recall curve
                        precision_, recall_, _ = cal_precision_recall(y_true, y_pred_proba)
                        avg_precision_ = average_precision_score(y_true, y_pred_proba)
                        pr_info = {
                            "precision": precision_,
                            "recall": recall_,
                            "avg_precision": avg_precision_,
                        }
                    else:
                        roc_info, pr_info = None, None
                    if purpose == "classification":
                        results[model] = {
                            # "best_clf": gs.best_estimator_,
                            # "best_params": gs.best_params_,
                            # "auc_indiv": [
                            #     gs.cv_results_[f"split{i}_test_score"][gs.best_index_]
                            #     for i in range(cv_folds)
                            # ],
                            "scores": validation_scores,
                            "roc_curve": roc_info,
                            "pr_curve": pr_info,
                            "confusion_matrix": confusion_matrix(y_true, y_pred),
                            "predictions": y_pred,#.tolist(),
                            "predictions_proba": (
                                y_pred_proba.tolist() if y_pred_proba is not None else None
                            ),
                            "features":features,
                            # "coef":coef_,
                            # "alphas":alphas_
                        }
                    else:  # "regression"
                        results[model] = {
                            # "best_clf": gs.best_estimator_,
                            # "best_params": gs.best_params_,
                            "scores": validation_scores,  # e.g., neg_MSE, R², etc.
                            "predictions": y_pred,#.tolist(),
                            "predictions_proba": (
                                y_pred_proba.tolist() if y_pred_proba is not None else None
                            ),
                            "features":features,
                            # "coef":coef_,
                            # "alphas":alphas_
                        }
                else:  # multi-classes
                    if y_pred_proba is not None:
                        # fpr, tpr, roc_auc = dict(), dict(), dict()
                        # fpr, tpr, _ = roc_curve(y_true, y_pred_proba)
                        confidence_intervals = cal_auc_ci(
                            y_true, y_pred_proba, verbose=False, is_binary=is_binary
                        )
                        roc_info = {
                            "fpr": validation_scores["fpr"],
                            "tpr": validation_scores["tpr"],
                            "auc": validation_scores["roc_auc_by_class"],
                            "ci95": confidence_intervals,
                        }
                        # precision-recall curve
                        precision_, recall_, avg_precision_ = cal_precision_recall(
                            y_true, y_pred_proba, is_binary=is_binary
                        )
                        pr_info = {
                            "precision": precision_,
                            "recall": recall_,
                            "avg_precision": avg_precision_,
                        }
                    else:
                        roc_info, pr_info = None, None

                    if purpose == "classification":
                        results[model] = {
                            # "best_clf": gs.best_estimator_,
                            # "best_params": gs.best_params_,
                            # "auc_indiv": [
                            #     gs.cv_results_[f"split{i}_test_score"][gs.best_index_]
                            #     for i in range(cv_folds)
                            # ],
                            "scores": validation_scores,
                            "roc_curve": roc_info,
                            "pr_curve": pr_info,
                            "confusion_matrix": confusion_matrix(y_true, y_pred),
                            "predictions": y_pred,#.tolist(),
                            "predictions_proba": (
                                y_pred_proba.tolist() if y_pred_proba is not None else None
                            ),
                            "features":features,
                            # "coef":coef_,
                            # "alphas":alphas_
                        }
                    else:  # "regression"
                        results[model] = {
                            # "best_clf": gs.best_estimator_,
                            # "best_params": gs.best_params_,
                            "scores": validation_scores,  # e.g., neg_MSE, R², etc.
                            "predictions": y_pred,#.tolist(),
                            "predictions_proba": (
                                y_pred_proba.tolist() if y_pred_proba is not None else None
                            ),
                            "features":features,
                            # "coef":coef_,
                            # "alphas":alphas_
                        }

            else:
                if y_true is None:
                    validation_scores = []
                else:
                    validation_scores = cal_metrics(
                        y_true,
                        y_pred,
                        y_pred_proba=y_pred_proba,
                        is_binary=is_binary,
                        purpose=purpose,
                        average="weighted",
                    )
                results[model] = {
                    # "best_clf": gs.best_estimator_,
                    # "best_params": gs.best_params_,
                    "scores": validation_scores,
                    "predictions": y_pred,#.tolist(),
                    "predictions_proba": (
                        y_pred_proba.tolist() if y_pred_proba is not None else None
                    ),
                    "features":features,
                    "y_train": y_train if y_train is not None else [],
                    "y_true": y_true if y_true is not None else [],
                    # "coef":coef_,
                    # "alphas":alphas_
                }
            df_results = pd.DataFrame.from_dict(results, orient="index")
            gs['res']=df_results

        if all([plot_, y_true is not None, purpose == "classification"]):
            from datetime import datetime

            now_ = datetime.now().strftime("%y%m%d_%H%M%S")
            # try:
            if df_results.shape[0] > 3:
                try:
                    plot_validate_features(df_results, is_binary=is_binary)
                except Exception as e:
                    print(e)
            else:
                try:
                    plot_validate_features_single(df_results, is_binary=is_binary)
                except Exception as e:
                    print(e)
            if dir_save:
                ips.figsave(dir_save + f"validate_features{now_}.pdf")
        return gs
    
    #! cross_valid
    if cv_level in ["low", "simple", "s", "l"]:
        param_grids = {
            "Random Forest": (
                {
                    "n_estimators": [100],  # One basic option
                    "max_depth": [None, 10],
                    "min_samples_split": [2],
                    "min_samples_leaf": [1],
                    "class_weight": [None],
                }
                if purpose == "classification"
                else {
                    "n_estimators": [100],  # One basic option
                    "max_depth": [None, 10],
                    "min_samples_split": [2],
                    "min_samples_leaf": [1],
                    "max_features": [None],
                    "bootstrap": [True],  # Only one option for simplicity
                }
            ),
            "SVM": {
                "C": [0.1, 1, 10],
                "gamma": ["scale", 0.1, 1],
                "kernel": ["rbf"],
            },
            "Lasso": {
                "alpha": [0.1],
            },
            "LassoCV": {
                "alphas": [[0.1]],
            },
            "Logistic Regression": {
                "C": [1],
                "solver": ["lbfgs"],
                "penalty": ["l2"],
                "max_iter": [500],
            },
            "Gradient Boosting": {
                "n_estimators": [100],
                "learning_rate": [0.1],
                "max_depth": [3],
                "min_samples_split": [2],
                "subsample": [0.8],
            },
            "XGBoost":{
                'learning_rate': [0.01],
                'max_depth': [3],
                'n_estimators': [50],
                'subsample': [0.6],
                'colsample_bytree': [0.6],
                'gamma': [0, 0.1],
                'min_child_weight': [1],
                'reg_alpha': [0, 0.1], 
                'reg_lambda': [1], 
                'objective': ['binary:logistic'] if purpose == "classification" else ['reg:squarederror']
            },
            "KNN": (
                {
                    "n_neighbors": [3],
                    "weights": ["uniform"],
                    "algorithm": ["auto"],
                    "p": [2],
                }
                if purpose == "classification"
                else {
                    "n_neighbors": [3],
                    "weights": ["uniform"],
                    "metric": ["euclidean"],
                    "leaf_size": [30],
                    "p": [2],
                }
            ),
            "Naive Bayes": {
                "var_smoothing": [1e-9],
            },
            "SVR": {
                "C": [1],
                "gamma": ["scale"],
                "kernel": ["rbf"],
            },
            "Linear Regression": {
                "fit_intercept": [True],
            },
            "Extra Trees": {
                "n_estimators": [100],
                "max_depth": [None, 10],
                "min_samples_split": [2],
                "min_samples_leaf": [1],
            },
            "CatBoost": {
                "iterations": [100],
                "learning_rate": [0.1],
                "depth": [3],
                "l2_leaf_reg": [1],
            },
            "LightGBM": {
                "n_estimators": [100],
                "num_leaves": [31],
                "max_depth": [10],
                "min_data_in_leaf": [20],
                "min_gain_to_split": [0.01],
                "scale_pos_weight": [10],
            },
            "Bagging": {
                "n_estimators": [50],
                "max_samples": [0.7],
                "max_features": [0.7],
            },
            "Neural Network": {
                "hidden_layer_sizes": [(50,)],
                "activation": ["relu"],
                "solver": ["adam"],
                "alpha": [0.0001],
            },
            "Decision Tree": {
                "max_depth": [None, 10],
                "min_samples_split": [2],
                "min_samples_leaf": [1],
                "criterion": ["gini"],
            },
            "AdaBoost": {
                "n_estimators": [50],
                "learning_rate": [0.5],
            },
            "Linear Discriminant Analysis": {
                "solver": ["svd"],
                "shrinkage": [None],
            },
            "Quadratic Discriminant Analysis": {
                "reg_param": [0.0],
                "priors": [None],
                "tol": [1e-4],
            },
            "Ridge": (
                {"class_weight": [None, "balanced"]}
                if purpose == "classification"
                else {
                    "alpha": [0.1, 1, 10],
                }
            ),
            "Perceptron": {
                "alpha": [1e-3],
                "penalty": ["l2"],
                "max_iter": [1000],
                "eta0": [1.0],
            },
            "Bernoulli Naive Bayes": {
                "alpha": [0.1, 1, 10],
                "binarize": [0.0],
                "fit_prior": [True],
            },
            "SGDClassifier": {
                "eta0": [0.01],
                "loss": ["hinge"],
                "penalty": ["l2"],
                "alpha": [1e-3],
                "max_iter": [1000],
                "tol": [1e-3],
                "random_state": [random_state],
                "learning_rate": ["constant"],
            },
            "TheilSen":{'max_iter': [100],
                        'tol': [1e-4],
                        'n_subsamples': [100+x_train.shape[1]]},
            "Huber":{'epsilon': [1.35],
                        'alpha': [0.1],
                        'max_iter': [100],},
            "Poisson":{'alpha': [0.1],
                        'max_iter': [100],}, 
            "Lars": {"n_nonzero_coefs": [10, 50, None]},
            "LassoLars": {
                "alpha": [0.01, 0.1, 1]
            },
            "BayesianRidge": {
                "alpha_1": [1e-6, 1e-4, 1e-2],
                "lambda_1": [1e-6, 1e-4, 1e-2]
            },
            "GammaRegressor": {
                "alpha": [0.1, 1, 10]
            },
            "TweedieRegressor": {
                "alpha": [0.1, 1, 10],
                "power": [1, 1.5, 2]
            },
            "LassoCV": {
                "cv": [5]
            },
            "ElasticNetCV": {
                "l1_ratio": [0.2, 0.5, 0.8],
                "cv": [5]
            },
            "LassoLarsCV": {
                "cv": [5]
            },
            "LarsCV": {
                "cv": [5]
            },
            "OrthogonalMatchingPursuit": {
                "n_nonzero_coefs": [10, 50, None]
            },
            "OrthogonalMatchingPursuitCV": {
                "cv": [5]
            },
            "PassiveAggressiveRegressor": {
                "C": [0.1, 1, 10]
            },
            "LinearSVR": {
                "C": [0.1, 1, 10]
            },
            "NuSVR": {
                "C": [0.1, 1, 10]
            },
            "DecisionTreeRegressor": {
                "max_depth": [5, 10, None]
            },
            "ExtraTreeRegressor": {
                "max_depth": [5, 10, None]
            },
            "HistGradientBoostingRegressor": {
                "learning_rate": [0.05, 0.1, 0.2],
                "max_depth": [5, 10, None]
            },
            "GaussianProcessRegressor": {
                "alpha": [1e-5, 1e-2, 0.1]
            },
            "KernelRidge": {
                "alpha": [0.1, 1, 10],
                "kernel": ["linear", "rbf"]
            },
            "DummyRegressor": {
                "strategy": ["mean", "median"]
            },
            "TransformedTargetRegressor": {
                "regressor__fit_intercept": [True, False]
            }
        }
    elif cv_level in ["high", "advanced", "h"]:
        param_grids = {
            "Random Forest": (
                {
                    "n_estimators": [100, 200, 500, 700, 1000],
                    "max_depth": [None, 3, 5, 10, 15, 20, 30],
                    "min_samples_split": [2, 5, 10, 20],
                    "min_samples_leaf": [1, 2, 4],
                    "class_weight": (
                        [None, "balanced"] if purpose == "classification" else {}
                    ),
                }
                if purpose == "classification"
                else {
                    "n_estimators": [100, 200, 500, 700, 1000],
                    "max_depth": [None, 3, 5, 10, 15, 20, 30],
                    "min_samples_split": [2, 5, 10, 20],
                    "min_samples_leaf": [1, 2, 4],
                    "max_features": [
                        "auto",
                        "sqrt",
                        "log2",
                    ],  # Number of features to consider when looking for the best split
                    "bootstrap": [
                        True,
                        False,
                    ],  # Whether bootstrap samples are used when building trees
                }
            ),
            "SVM": {
                "C": [0.001, 0.01, 0.1, 1, 10, 100, 1000],
                "gamma": ["scale", "auto", 0.001, 0.01, 0.1],
                "kernel": ["linear", "rbf", "poly"],
            },
            "Logistic Regression": {
                "C": [0.001, 0.01, 0.1, 1, 10, 100, 1000],
                "solver": ["liblinear", "saga", "newton-cg", "lbfgs"],
                "penalty": ["l1", "l2", "elasticnet"],
                "max_iter": [100, 200, 300, 500],
            },
            "Lasso": {
                "alpha": [0.0001, 0.001, 0.01, 0.1, 1.0, 10.0, 100.0],
                "max_iter": [500, 1000, 2000, 5000],
                "tol": [1e-4, 1e-5, 1e-6],
                "selection": ["cyclic", "random"],
            },
            "LassoCV": {
                "alphas": [[0.0001, 0.001, 0.01, 0.1, 1.0, 10.0, 100.0]],
                "max_iter": [500, 1000, 2000, 5000],
                "cv": [3, 5, 10],
                "tol": [1e-4, 1e-5, 1e-6],
            },
            "Gradient Boosting": {
                "n_estimators": [100, 200, 300, 400, 500, 700, 1000],
                "learning_rate": [0.001, 0.01, 0.1, 0.2, 0.3, 0.5],
                "max_depth": [3, 5, 7, 9, 15],
                "min_samples_split": [2, 5, 10, 20],
                "subsample": [0.8, 1.0],
            },
            "XGBoost": {
                'learning_rate': [0.01, 0.1, 0.2, 0.3],
                'max_depth': [3, 5, 7, 10],
                'n_estimators': [50, 100, 200, 300],
                'subsample': [0.6, 0.8, 1.0],
                'gamma': [0, 0.1, 0.2, 0.5],
                'min_child_weight': [1, 5, 10],
                'reg_alpha': [0, 0.1, 0.5, 1], 
                'reg_lambda': [1, 1.5, 2], 
                **{
                'objective': ['binary:logistic', 'multi:softmax', 'multi:softprob'],
                }} if purpose== "classification" 
            else{
                'learning_rate': [0.01, 0.1, 0.2, 0.3],
                'max_depth': [3, 5, 7, 10],
                'n_estimators': [50, 100, 200, 300],
                'subsample': [0.6, 0.8, 1.0],
                'colsample_bytree': [0.6, 0.8, 1.0],
                'gamma': [0, 0.1, 0.2, 0.5],
                'min_child_weight': [1, 5, 10],
                'reg_alpha': [0, 0.1, 0.5, 1], 
                'reg_lambda': [1, 1.5, 2], 
                 **{
                    'objective': ['reg:squarederror', 'reg:squaredlogerror', 'reg:gamma'],
                }},
            "KNN": (
                {
                    "n_neighbors": [1, 3, 5, 10, 15, 20],
                    "weights": ["uniform", "distance"],
                    "algorithm": ["auto", "ball_tree", "kd_tree", "brute"],
                    "p": [1, 2],  # 1 for Manhattan, 2 for Euclidean distance
                }
                if purpose == "classification"
                else {
                    "n_neighbors": [3, 5, 7, 9, 11],  # Number of neighbors
                    "weights": [
                        "uniform",
                        "distance",
                    ],  # Weight function used in prediction
                    "metric": [
                        "euclidean",
                        "manhattan",
                        "minkowski",
                    ],  # Distance metric
                    "leaf_size": [
                        20,
                        30,
                        40,
                        50,
                    ],  # Leaf size for KDTree or BallTree algorithms
                    "p": [
                        1,
                        2,
                    ],  # Power parameter for the Minkowski metric (1 = Manhattan, 2 = Euclidean)
                }
            ),
            "Naive Bayes": {
                "var_smoothing": [1e-10, 1e-9, 1e-8, 1e-7],
            },
            "AdaBoost": {
                "n_estimators": [50, 100, 200, 300, 500],
                "learning_rate": [0.001, 0.01, 0.1, 0.5, 1.0],
            },
            "SVR": {
                "C": [0.01, 0.1, 1, 10, 100, 1000],
                "gamma": [0.001, 0.01, 0.1, "scale", "auto"],
                "kernel": ["linear", "rbf", "poly"],
            },
            "Linear Regression": {
                "fit_intercept": [True, False],
            },
            "Lasso": {
                "alpha": [0.001, 0.01, 0.1, 1.0, 10.0, 100.0],
                "max_iter": [1000, 2000],  # Higher iteration limit for fine-tuning
            },
            "Extra Trees": {
                "n_estimators": [100, 200, 500, 700, 1000],
                "max_depth": [None, 5, 10, 15, 20, 30],
                "min_samples_split": [2, 5, 10, 20],
                "min_samples_leaf": [1, 2, 4],
            },
            "CatBoost": {
                "iterations": [100, 200, 500],
                "learning_rate": [0.001, 0.01, 0.1, 0.2],
                "depth": [3, 5, 7, 10],
                "l2_leaf_reg": [1, 3, 5, 7, 10],
                "border_count": [32, 64, 128],
            },
            "LightGBM": {
                "n_estimators": [100, 200, 500, 700, 1000],
                "learning_rate": [0.001, 0.01, 0.1, 0.2],
                "num_leaves": [31, 50, 100, 200],
                "max_depth": [-1, 5, 10, 20, 30],
                "min_child_samples": [5, 10, 20],
                "subsample": [0.8, 1.0],
                "colsample_bytree": [0.8, 0.9, 1.0],
            },
            "Neural Network": {
                "hidden_layer_sizes": [(50,), (100,), (100, 50), (200, 100)],
                "activation": ["relu", "tanh", "logistic"],
                "solver": ["adam", "sgd", "lbfgs"],
                "alpha": [0.0001, 0.001, 0.01],
                "learning_rate": ["constant", "adaptive"],
            },
            "Decision Tree": {
                "max_depth": [None, 5, 10, 20, 30],
                "min_samples_split": [2, 5, 10, 20],
                "min_samples_leaf": [1, 2, 5, 10],
                "criterion": ["gini", "entropy"],
                "splitter": ["best", "random"],
            },
            "Linear Discriminant Analysis": {
                "solver": ["svd", "lsqr", "eigen"],
                "shrinkage": [
                    None,
                    "auto",
                    0.1,
                    0.5,
                    1.0,
                ],  # shrinkage levels for 'lsqr' and 'eigen'
            },
            "Ridge": (
                {"class_weight": [None, "balanced"]}
                if purpose == "classification"
                else {
                    "alpha": [0.1, 1, 10, 100, 1000],
                    "solver": ["auto", "svd", "cholesky", "lsqr", "lbfgs"],
                    "fit_intercept": [
                        True,
                        False,
                    ],  # Whether to calculate the intercept
                    "normalize": [
                        True,
                        False,
                    ],  # If True, the regressors X will be normalized
                }
            ),
            "TheilSen":{'max_iter': [100, 200, 300],
                        'tol': [1e-4, 1e-3, 1e-2],
                        'n_subsamples': [100+x_train.shape[1], 200+x_train.shape[1], 300+x_train.shape[1]]},
            "Huber":{'epsilon': [1.35, 1.5, 2.0],
                        'alpha': [0.1, 1.0, 10.0],
                        'max_iter': [100, 200, 300],},
            "Poisson":{'alpha': [0.1, 1.0, 10.0],
                        'max_iter': [100, 200, 300],},
            "Lars": {
                "n_nonzero_coefs": [10, 50, 100, 200, None]
            },
            "LassoLars": {
                "alpha": [0.001, 0.01, 0.1, 1, 10]
            },
            "BayesianRidge": {
                "alpha_1": [1e-6, 1e-5, 1e-4],
                "alpha_2": [1e-6, 1e-5, 1e-4],
                "lambda_1": [1e-6, 1e-5, 1e-4],
                "lambda_2": [1e-6, 1e-5, 1e-4]
            },
            "GammaRegressor": {
                "alpha": [0.01, 0.1, 1, 10],
                "max_iter": [1000, 5000, 10000]
            },
            "TweedieRegressor": {
                "alpha": [0.01, 0.1, 1, 10],
                "power": [0, 1, 1.5, 2, 3]
            },
            "LassoCV": {
                "alphas": [[0.001, 0.01, 0.1, 1, 10]],
                "cv": [3, 5, 10]
            },
            "ElasticNetCV": {
                "l1_ratio": [0.1, 0.5, 0.7, 0.9, 1],
                "alphas": [[0.001, 0.01, 0.1, 1, 10]],
                "cv": [3, 5, 10]
            },
            "LassoLarsCV": {
                "cv": [3, 5, 10]
            },
            "LarsCV": {
                "cv": [3, 5, 10]
            },
            "OrthogonalMatchingPursuit": {
                "n_nonzero_coefs": [10, 50, 100, 200, None]
            },
            "OrthogonalMatchingPursuitCV": {
                "cv": [3, 5, 10]
            },
            "PassiveAggressiveRegressor": {
                "C": [0.01, 0.1, 1, 10],
                "max_iter": [1000, 5000, 10000],
                "early_stopping": [True, False]
            },
            "LinearSVR": {
                "C": [0.01, 0.1, 1, 10],
                "epsilon": [0.01, 0.1, 1],
                "max_iter": [1000, 5000, 10000]
            },
            "NuSVR": {
                "C": [0.01, 0.1, 1, 10],
                "nu": [0.25, 0.5, 0.75],
                "kernel": ["linear", "poly", "rbf", "sigmoid"]
            },
            "DecisionTreeRegressor": {
                "max_depth": [None, 5, 10, 20],
                "min_samples_split": [2, 5, 10],
                "min_samples_leaf": [1, 2, 4]
            },
            "ExtraTreeRegressor": {
                "max_depth": [None, 5, 10, 20],
                "min_samples_split": [2, 5, 10],
                "min_samples_leaf": [1, 2, 4]
            },
            "HistGradientBoostingRegressor": {
                "learning_rate": [0.01, 0.1, 0.2],
                "max_iter": [100, 500, 1000],
                "max_depth": [None, 5, 10, 20],
                "min_samples_leaf": [1, 2, 4]
            },
            "GaussianProcessRegressor": {
                "alpha": [1e-10, 1e-5, 1e-2, 0.1],
                "n_restarts_optimizer": [0, 1, 5, 10]
            },
            "KernelRidge": {
                "alpha": [0.01, 0.1, 1, 10],
                "kernel": ["linear", "poly", "rbf", "sigmoid"],
                "degree": [2, 3, 4]
            },
            "DummyRegressor": {
                "strategy": ["mean", "median", "constant"],
                "constant": [0]  # Only if strategy is 'constant'
            },
            "TransformedTargetRegressor": {
                # Grid for the underlying regressor, example shown for LinearRegression
                "regressor__fit_intercept": [True, False]
            }
        }
    else:  # median level
        param_grids = {
            "Random Forest": (
                {
                    "n_estimators": [100, 200, 500],
                    "max_depth": [None, 10, 20, 30],
                    "min_samples_split": [2, 5, 10],
                    "min_samples_leaf": [1, 2, 4],
                    "class_weight": [None, "balanced"],
                }
                if purpose == "classification"
                else {
                    "n_estimators": [100, 200, 500],
                    "max_depth": [None, 10, 20, 30],
                    "min_samples_split": [2, 5, 10],
                    "min_samples_leaf": [1, 2, 4],
                    "max_features": [
                        "auto",
                        "sqrt",
                        "log2",
                    ],  # Number of features to consider when looking for the best split
                    "bootstrap": [
                        True,
                        False,
                    ],  # Whether bootstrap samples are used when building trees
                }
            ),
            "SVM": {
                "C": [0.1, 1, 10, 100],  # Regularization strength
                "gamma": ["scale", "auto"],  # Common gamma values
                "kernel": ["rbf", "linear", "poly"],
            },
            "Logistic Regression": {
                "C": [0.1, 1, 10, 100],  # Regularization strength
                "solver": ["lbfgs", "liblinear", "saga"],  # Common solvers
                "penalty": ["l2"],  # L2 penalty is most common
                "max_iter": [
                    500,
                    1000,
                    2000,
                ],  # Increased max_iter for better convergence
            },
            "Lasso": {
                "alpha": [0.001, 0.01, 0.1, 1.0, 10.0, 100.0],
                "max_iter": [500, 1000, 2000],
            },
            "LassoCV": {
                "alphas": [[0.001, 0.01, 0.1, 1.0, 10.0, 100.0]],
                "max_iter": [500, 1000, 2000],
            },
            "Gradient Boosting": {
                "n_estimators": [100, 200, 500],
                "learning_rate": [0.01, 0.1, 0.2],
                "max_depth": [3, 5, 7],
                "min_samples_split": [2, 5, 10],
                "subsample": [0.8, 1.0],
            },
            "XGBoost": {
                'learning_rate': [0.01, 0.1],
                'max_depth': [3, 5],
                'n_estimators': [50, 100],
                'subsample': [0.6, 0.8],
                'gamma': [0, 0.1],
                'min_child_weight': [1, 5],
                'reg_alpha': [0, 0.1], 
                'reg_lambda': [1,], 
                **{
                'objective': ['binary:logistic', 'multi:softmax'],
                }} if purpose== "classification" 
                else{
                    'learning_rate': [0.01, 0.1],
                    'max_depth': [3, 5,],
                    'n_estimators': [50, 100],
                    'subsample': [0.6, 0.8],
                    'colsample_bytree': [0.6, 0.8],
                    'gamma': [0, 0.1],
                    'min_child_weight': [1, 5],
                    'reg_alpha': [0, 0.1], 
                    'reg_lambda': [1, 1.5], 
                    **{
                        'objective': ['reg:squarederror', 'reg:squaredlogerror'],
                    }},
            "KNN": (
                {
                    "n_neighbors": [3, 5, 7, 10],
                    "weights": ["uniform", "distance"],
                    "algorithm": ["auto", "ball_tree", "kd_tree", "brute"],
                    "p": [1, 2],
                }
                if purpose == "classification"
                else {
                    "n_neighbors": [3, 5, 7, 9, 11],  # Number of neighbors
                    "weights": [
                        "uniform",
                        "distance",
                    ],  # Weight function used in prediction
                    "metric": [
                        "euclidean",
                        "manhattan",
                        "minkowski",
                    ],  # Distance metric
                    "leaf_size": [
                        20,
                        30,
                        40,
                        50,
                    ],  # Leaf size for KDTree or BallTree algorithms
                    "p": [
                        1,
                        2,
                    ],  # Power parameter for the Minkowski metric (1 = Manhattan, 2 = Euclidean)
                }
            ),
            "Naive Bayes": {
                "var_smoothing": [1e-9, 1e-8, 1e-7],
            },
            "SVR": {
                "C": [0.1, 1, 10, 100],
                "gamma": ["scale", "auto"],
                "kernel": ["rbf", "linear"],
            },
            "Linear Regression": {
                "fit_intercept": [True, False],
            },
            "Lasso": {
                "alpha": [0.1, 1.0, 10.0],
                "max_iter": [1000, 2000],  # Sufficient iterations for convergence
            },
            "Extra Trees": {
                "n_estimators": [100, 200, 500],
                "max_depth": [None, 10, 20, 30],
                "min_samples_split": [2, 5, 10],
                "min_samples_leaf": [1, 2, 4],
            },
            "CatBoost": {
                "iterations": [100, 200],
                "learning_rate": [0.01, 0.1],
                "depth": [3, 6, 10],
                "l2_leaf_reg": [1, 3, 5, 7],
            },
            "LightGBM": {
                "n_estimators": [100, 200, 500],
                "learning_rate": [0.01, 0.1],
                "num_leaves": [31, 50, 100],
                "max_depth": [-1, 10, 20],
                "min_data_in_leaf": [20],  # Minimum samples in each leaf
                "min_gain_to_split": [0.01],  # Minimum gain to allow a split
                "scale_pos_weight": [10],  # Address class imbalance
            },
            "Bagging": {
                "n_estimators": [10, 50, 100],
                "max_samples": [0.5, 0.7, 1.0],
                "max_features": [0.5, 0.7, 1.0],
            },
            "Neural Network": {
                "hidden_layer_sizes": [(50,), (100,), (100, 50)],
                "activation": ["relu", "tanh"],
                "solver": ["adam", "sgd"],
                "alpha": [0.0001, 0.001],
            },
            "Decision Tree": {
                "max_depth": [None, 10, 20],
                "min_samples_split": [2, 10],
                "min_samples_leaf": [1, 4],
                "criterion": ["gini", "entropy"],
            },
            "AdaBoost": {
                "n_estimators": [50, 100],
                "learning_rate": [0.5, 1.0],
            },
            "Linear Discriminant Analysis": {
                "solver": ["svd", "lsqr", "eigen"],
                "shrinkage": [None, "auto"],
            },
            "Quadratic Discriminant Analysis": {
                "reg_param": [0.0, 0.1, 0.5, 1.0],  # Regularization parameter
                "priors": [None, [0.5, 0.5], [0.3, 0.7]],  # Class priors
                "tol": [
                    1e-4,
                    1e-3,
                    1e-2,
                ],  # Tolerance value for the convergence of the algorithm
            },
            "Perceptron": {
                "alpha": [1e-4, 1e-3, 1e-2],  # Regularization parameter
                "penalty": ["l2", "l1", "elasticnet"],  # Regularization penalty
                "max_iter": [1000, 2000],  # Maximum number of iterations
                "eta0": [1.0, 0.1],  # Learning rate for gradient descent
                "tol": [1e-3, 1e-4, 1e-5],  # Tolerance for stopping criteria
                "random_state": [random_state],  # Random state for reproducibility
            },
            "Bernoulli Naive Bayes": {
                "alpha": [0.1, 1.0, 10.0],  # Additive (Laplace) smoothing parameter
                "binarize": [
                    0.0,
                    0.5,
                    1.0,
                ],  # Threshold for binarizing the input features
                "fit_prior": [
                    True,
                    False,
                ],  # Whether to learn class prior probabilities
            },
            "SGDClassifier": {
                "eta0": [0.01, 0.1, 1.0],
                "loss": [
                    "hinge",
                    "log",
                    "modified_huber",
                    "squared_hinge",
                    "perceptron",
                ],  # Loss function
                "penalty": ["l2", "l1", "elasticnet"],  # Regularization penalty
                "alpha": [1e-4, 1e-3, 1e-2],  # Regularization strength
                "l1_ratio": [0.15, 0.5, 0.85],  # L1 ratio for elasticnet penalty
                "max_iter": [1000, 2000],  # Maximum number of iterations
                "tol": [1e-3, 1e-4],  # Tolerance for stopping criteria
                "random_state": [random_state],  # Random state for reproducibility
                "learning_rate": [
                    "constant",
                    "optimal",
                    "invscaling",
                    "adaptive",
                ],  # Learning rate schedule
            },
            "Ridge": (
                {"class_weight": [None, "balanced"]}
                if purpose == "classification"
                else {
                    "alpha": [0.1, 1, 10, 100],
                    "solver": [
                        "auto",
                        "svd",
                        "cholesky",
                        "lsqr",
                    ],  # Solver for optimization
                }
            ),
            "TheilSen":{'max_iter': [100, 200],
                        'tol': [1e-4, 1e-3],
                        'n_subsamples': [100+x_train.shape[1], 200+x_train.shape[1]]},
            "Huber":{'epsilon': [1.35, 1.5],
                        'alpha': [0.1, 1.0],
                        'max_iter': [100, 200],},
            "Poisson":{'alpha': [0.1, 1.0],
                        'max_iter': [100, 200],}, 
            "Lars": {
                "n_nonzero_coefs": [10, 50, 100, 200, None]
            },
            "LassoLars": {
                "alpha": [0.001, 0.01, 0.1, 1, 10]
            },
            "BayesianRidge": {
                "alpha_1": [1e-6, 1e-5, 1e-4],
                "alpha_2": [1e-6, 1e-5, 1e-4],
                "lambda_1": [1e-6, 1e-5, 1e-4],
                "lambda_2": [1e-6, 1e-5, 1e-4]
            },
            "GammaRegressor": {
                "alpha": [0.01, 0.1, 1, 10],
                "max_iter": [1000, 5000, 10000]
            },
            "TweedieRegressor": {
                "alpha": [0.01, 0.1, 1, 10],
                "power": [0, 1, 1.5, 2, 3]
            },
            "LassoCV": {
                "alphas": [[0.001, 0.01, 0.1, 1, 10]],
                "cv": [3, 5, 10]
            },
            "ElasticNetCV": {
                "l1_ratio": [0.1, 0.5, 0.7, 0.9, 1],
                "alphas": [[0.001, 0.01, 0.1, 1, 10]],
                "cv": [3, 5, 10]
            },
            "LassoLarsCV": {
                "cv": [3, 5, 10]
            },
            "LarsCV": {
                "cv": [3, 5, 10]
            },
            "OrthogonalMatchingPursuit": {
                "n_nonzero_coefs": [10, 50, 100, 200, None]
            },
            "OrthogonalMatchingPursuitCV": {
                "cv": [3, 5, 10]
            },
            "PassiveAggressiveRegressor": {
                "C": [0.01, 0.1, 1, 10],
                "max_iter": [1000, 5000, 10000],
                "early_stopping": [True, False]
            },
            "LinearSVR": {
                "C": [0.01, 0.1, 1, 10],
                "epsilon": [0.01, 0.1, 1],
                "max_iter": [1000, 5000, 10000]
            },
            "NuSVR": {
                "C": [0.01, 0.1, 1, 10],
                "nu": [0.25, 0.5, 0.75],
                "kernel": ["linear", "poly", "rbf", "sigmoid"]
            },
            "DecisionTreeRegressor": {
                "max_depth": [None, 5, 10, 20],
                "min_samples_split": [2, 5, 10],
                "min_samples_leaf": [1, 2, 4]
            },
            "ExtraTreeRegressor": {
                "max_depth": [None, 5, 10, 20],
                "min_samples_split": [2, 5, 10],
                "min_samples_leaf": [1, 2, 4]
            },
            "HistGradientBoostingRegressor": {
                "learning_rate": [0.01, 0.1, 0.2],
                "max_iter": [100, 500, 1000],
                "max_depth": [None, 5, 10, 20],
                "min_samples_leaf": [1, 2, 4]
            },
            "GaussianProcessRegressor": {
                "alpha": [1e-10, 1e-5, 1e-2, 0.1],
                "n_restarts_optimizer": [0, 1, 5, 10]
            },
            "KernelRidge": {
                "alpha": [0.01, 0.1, 1, 10],
                "kernel": ["linear", "poly", "rbf", "sigmoid"],
                "degree": [2, 3, 4]
            },
            "DummyRegressor": {
                "strategy": ["mean", "median", "constant"],
                "constant": [0]  # Only if strategy is 'constant'
            },
            "TransformedTargetRegressor": {
                # Grid for the underlying regressor, example shown for LinearRegression
                "regressor__fit_intercept": [True, False]
            }
        }

    results = {}
    # Use StratifiedKFold for classification and KFold for regression
    cv = (
        StratifiedKFold(n_splits=cv_folds, shuffle=True, random_state=random_state)
        if purpose == "classification"
        else KFold(n_splits=cv_folds, shuffle=True, random_state=random_state)
    )
 
    # Train and validate each model
    for name, clf in tqdm(
        models.items(),
        desc="models",
        colour="green",
        bar_format="{l_bar}{bar} {n_fmt}/{total_fmt}",
    ):
        if verbose:
            print(f"\nTraining and validating {name}:")
        try:
            if is_binary: 
                gs = GridSearchCV(
                    clf,
                    param_grid=param_grids.get(name, {}),
                    scoring=(
                        "roc_auc"
                        if purpose == "classification"
                        else "neg_mean_squared_error"
                    ),
                    cv=cv,
                    n_jobs=n_jobs,
                    verbose=verbose,
                )

                gs.fit(x_train, y_train)
                best_clf = gs.best_estimator_

                # make sure x_train and x_test has the same name
                x_true = x_true.reindex(columns=x_train.columns, fill_value=0)
                y_pred = best_clf.predict(x_true)
                if hasattr(best_clf, "predict_proba"):
                    y_pred_proba = best_clf.predict_proba(x_true)
                    print("Shape of predicted probabilities:", y_pred_proba.shape)
                    if y_pred_proba.shape[1] == 1:
                        y_pred_proba = np.hstack(
                            [1 - y_pred_proba, y_pred_proba]
                        )  # Add missing class probabilities
                    if y_pred_proba.shape[1] == 2:
                        if isinstance(y_pred_proba, pd.DataFrame):
                            y_pred_proba = y_pred_proba.iloc[:, 1] 
                        elif isinstance(y_pred_proba, pd.Series):
                            y_pred_proba = y_pred_proba.values[:, 1]
                    else:
                        y_pred_proba = y_pred_proba[:, 1]
                    
                elif hasattr(best_clf, "decision_function"):
                    # If predict_proba is not available, use decision_function (e.g., for SVM)
                    y_pred_proba = best_clf.decision_function(x_true)
                    # Ensure y_pred_proba is within 0 and 1 bounds
                    y_pred_proba = (y_pred_proba - y_pred_proba.min()) / (
                        y_pred_proba.max() - y_pred_proba.min()
                    )
                else:
                    y_pred_proba = None  # No probability output for certain models
                # Access alphas if applicable (e.g., ElasticNetCV, LassoCV)
                if hasattr(best_clf, "alphas_") or hasattr(best_clf, "Cs_"):
                    if hasattr(best_clf, "alphas_"):
                        alphas_ = best_clf.alphas_
                    elif hasattr(best_clf, "alpha_"):
                        alphas_ = best_clf.alpha_
                    elif hasattr(best_clf, "Cs_"):
                        alphas_ = best_clf.Cs_
                else: 
                    alphas_= None
                coef_ = best_clf.coef_ if hasattr(best_clf, "coef_") else None 
            else: 
                gs = GridSearchCV(
                    clf,
                    param_grid=param_grids.get(name, {}),
                    scoring=(
                        "roc_auc_ovr"
                        if purpose == "classification"
                        else "neg_mean_squared_error"
                    ),
                    cv=cv,
                    n_jobs=n_jobs,
                    verbose=verbose,
                )

                # Fit GridSearchCV
                gs.fit(x_train, y_train)
                best_clf = gs.best_estimator_

                # Ensure x_true aligns with x_train columns
                x_true = x_true.reindex(columns=x_train.columns, fill_value=0)

                # do i need to fit the x_train, y_train again? 
                best_clf=best_clf.fit(x_train, y_train)
                y_pred = best_clf.predict(x_true)

                # Handle prediction probabilities for multiclass
                if hasattr(best_clf, "predict_proba"):
                    y_pred_proba = best_clf.predict_proba(x_true)
                elif hasattr(best_clf, "decision_function"):
                    y_pred_proba = best_clf.decision_function(x_true)

                    # Normalize for multiclass if necessary
                    if y_pred_proba.ndim == 2:
                        y_pred_proba = (
                            y_pred_proba - y_pred_proba.min(axis=1, keepdims=True)
                        ) / (
                            y_pred_proba.max(axis=1, keepdims=True)
                            - y_pred_proba.min(axis=1, keepdims=True)
                        )
                else:
                    y_pred_proba = None  # No probability output for certain models
                # Access alphas if applicable (e.g., ElasticNetCV, LassoCV)
                if hasattr(best_clf, "alphas_") or hasattr(best_clf, "Cs_"):
                    if hasattr(best_clf, "alphas_"):
                        alphas_ = best_clf.alphas_
                    elif hasattr(best_clf, "alpha_"):
                        alphas_ = best_clf.alpha_
                    elif hasattr(best_clf, "Cs_"):
                        alphas_ = best_clf.Cs_
                else: 
                    alphas_= None
                coef_ = best_clf.coef_ if hasattr(best_clf, "coef_") else None 
        except Exception as e:
            alphas_,coef_ = None,None
            print(f"skiped {clf}: {e}")
            continue

        # try to make predict format consistant
        try:
           y_pred= [i[0] for i in y_pred]
        except:
            pass
        try:
           y_true= [i[0] for i in y_true]
        except:
            pass
        try:
           y_train= [i[0] for i in y_train]
        except:
            pass
        validation_scores = {}

        if y_true is not None and y_pred_proba is not None:
            validation_scores = cal_metrics(
                y_true,
                y_pred,
                y_pred_proba=y_pred_proba,
                is_binary=is_binary,
                purpose=purpose,
                average="weighted",
            )
            if is_binary:
                # Calculate ROC curve
                # https://scikit-learn.org/stable/auto_examples/model_selection/plot_roc.html
                if y_pred_proba is not None:
                    # fpr, tpr, roc_auc = dict(), dict(), dict()
                    fpr, tpr, _ = roc_curve(y_true, y_pred_proba)
                    lower_ci, upper_ci = cal_auc_ci(
                        y_true, y_pred_proba, verbose=False, is_binary=is_binary
                    )
                    roc_auc = auc(fpr, tpr)
                    roc_info = {
                        "fpr": fpr.tolist(),
                        "tpr": tpr.tolist(),
                        "auc": roc_auc,
                        "ci95": (lower_ci, upper_ci),
                    }
                    # precision-recall curve
                    precision_, recall_, _ = cal_precision_recall(y_true, y_pred_proba)
                    avg_precision_ = average_precision_score(y_true, y_pred_proba)
                    pr_info = {
                        "precision": precision_,
                        "recall": recall_,
                        "avg_precision": avg_precision_,
                    }
                else:
                    roc_info, pr_info = None, None
                if purpose == "classification":
                    results[name] = {
                        "best_clf": gs.best_estimator_,
                        "best_params": gs.best_params_,
                        "auc_indiv": [
                            gs.cv_results_[f"split{i}_test_score"][gs.best_index_]
                            for i in range(cv_folds)
                        ],
                        "scores": validation_scores,
                        "roc_curve": roc_info,
                        "pr_curve": pr_info,
                        "confusion_matrix": confusion_matrix(y_true, y_pred),
                        "predictions": y_pred,#.tolist(),
                        "predictions_proba": (
                            y_pred_proba.tolist() if y_pred_proba is not None else None
                        ),
                        "features":share_col_names,
                        "coef":coef_,
                        "alphas":alphas_
                    }
                else:  # "regression"
                    results[name] = {
                        "best_clf": gs.best_estimator_,
                        "best_params": gs.best_params_,
                        "scores": validation_scores,  # e.g., neg_MSE, R², etc.
                        "predictions": y_pred,#.tolist(),
                        "predictions_proba": (
                            y_pred_proba.tolist() if y_pred_proba is not None else None
                        ),
                        "features":share_col_names,
                        "coef":coef_,
                        "alphas":alphas_
                    }
            else:  # multi-classes
                if y_pred_proba is not None:
                    # fpr, tpr, roc_auc = dict(), dict(), dict()
                    # fpr, tpr, _ = roc_curve(y_true, y_pred_proba)
                    confidence_intervals = cal_auc_ci(
                        y_true, y_pred_proba, verbose=False, is_binary=is_binary
                    )
                    roc_info = {
                        "fpr": validation_scores["fpr"],
                        "tpr": validation_scores["tpr"],
                        "auc": validation_scores["roc_auc_by_class"],
                        "ci95": confidence_intervals,
                    }
                    # precision-recall curve
                    precision_, recall_, avg_precision_ = cal_precision_recall(
                        y_true, y_pred_proba, is_binary=is_binary
                    )
                    pr_info = {
                        "precision": precision_,
                        "recall": recall_,
                        "avg_precision": avg_precision_,
                    }
                else:
                    roc_info, pr_info = None, None

                if purpose == "classification":
                    results[name] = {
                        "best_clf": gs.best_estimator_,
                        "best_params": gs.best_params_,
                        "auc_indiv": [
                            gs.cv_results_[f"split{i}_test_score"][gs.best_index_]
                            for i in range(cv_folds)
                        ],
                        "scores": validation_scores,
                        "roc_curve": roc_info,
                        "pr_curve": pr_info,
                        "confusion_matrix": confusion_matrix(y_true, y_pred),
                        "predictions": y_pred,#.tolist(),
                        "predictions_proba": (
                            y_pred_proba.tolist() if y_pred_proba is not None else None
                        ),
                        "features":share_col_names,
                        "coef":coef_,
                        "alphas":alphas_
                    }
                else:  # "regression"
                    results[name] = {
                        "best_clf": gs.best_estimator_,
                        "best_params": gs.best_params_,
                        "scores": validation_scores,  # e.g., neg_MSE, R², etc.
                        "predictions": y_pred,#.tolist(),
                        "predictions_proba": (
                            y_pred_proba.tolist() if y_pred_proba is not None else None
                        ),
                        "features":share_col_names,
                        "coef":coef_,
                        "alphas":alphas_
                    }

        else:
            if y_true is None:
                validation_scores = []
            else:
                validation_scores = cal_metrics(
                    y_true,
                    y_pred,
                    y_pred_proba=y_pred_proba,
                    is_binary=is_binary,
                    purpose=purpose,
                    average="weighted",
                )
            results[name] = {
                "best_clf": gs.best_estimator_,
                "best_params": gs.best_params_,
                "scores": validation_scores,
                "predictions": y_pred,#.tolist(),
                "predictions_proba": (
                    y_pred_proba.tolist() if y_pred_proba is not None else None
                ),
                "features":share_col_names,
                "y_train": y_train if y_train is not None else [],
                "y_true": y_true if y_true is not None else [],
                "coef":coef_,
                "alphas":alphas_
            }

    # Convert results to DataFrame
    df_results = pd.DataFrame.from_dict(results, orient="index")
    display(df_results)
    # sort 
    if y_true is not None:
        if purpose == "classification":
            df_scores = pd.DataFrame(
                df_results["scores"].tolist(), index=df_results["scores"].index
            ).sort_values(by="roc_auc", ascending=False)
        elif purpose=='regression':
            df_scores = rank_models_reg(
            pd.DataFrame(df_results["scores"].tolist(), index=df_results["scores"].index),
            ascending=False)
        df_results = df_results.loc[df_scores.index]

    if y_true is not None and purpose == "classification":
        if plot_:
            from datetime import datetime

            now_ = datetime.now().strftime("%y%m%d_%H%M%S")
            nexttile = plot.subplot(figsize=[12, 10])
            plot.heatmap(df_scores, kind="direct", ax=nexttile())
            plot.figsets(xangle=30)
            if dir_save:
                ips.figsave(dir_save + f"scores_sorted_heatmap{now_}.pdf")

            df_scores = df_scores.select_dtypes(include=np.number)

            if df_scores.shape[0] > 1:  # draw cluster
                plot.heatmap(df_scores, kind="direct", cluster=True)
                plot.figsets(xangle=30)
                if dir_save:
                    ips.figsave(dir_save + f"scores_clus{now_}.pdf")
    # if all([plot_, y_true is not None, purpose == "classification"]):
    #     # try:
    #     if len(models) > 3:
    #         plot_validate_features(df_results, is_binary=is_binary)
    #     else:
    #         plot_validate_features_single(df_results, is_binary=is_binary)
    #     if dir_save:
    #         ips.figsave(dir_save + f"validate_features{now_}.pdf")
    #     # except Exception as e:
    #     #     print(f"Error: 在画图的过程中出现了问题:{e}")
    if stack:
        #! stacking classifier/regressor
        from sklearn.metrics import make_scorer, accuracy_score
        from sklearn.model_selection import cross_val_score
        
        #* n_top_models防止超过index
        n_top_models = min(n_top_models, df_results.shape[0])
        
        #* 选择出排名靠前的n个, estimators
        models_selecte = select_top_models(models=list(df_results.index), 
                                        categories=models_support[purpose], 
                                        n_top_models=n_top_models,
                                        n_models_per_category=n_models_per_category)
        top_models = df_results.loc[models_selecte]["best_clf"]
        base_estimators = []
        for i, j in top_models.to_dict().items():
            base_estimators.append((i, j))
        if stacking_cv:
            print(f"⤵ stacking_cv is processing...")  
            #* 定义几个象征性的final_estimator
            # 备选的几种
            if purpose == "classification":
                kadt_estimators=["XGBoost","SVM","Logistic Regression","Neural Network"]
            else:
                kadt_estimators=["XGBoost","LassoCV"]
            final_estimators={}
            for name in kadt_estimators:
                param_grid=param_grids.get(name, {})
                print(param_grid)
                if is_binary:
                    gs = GridSearchCV(
                        model_[name],
                        param_grid=param_grid,
                        scoring=(
                            "roc_auc"
                            if purpose == "classification"
                            else "neg_mean_squared_error"
                        ),
                        cv=cv,
                        n_jobs=n_jobs,
                        verbose=verbose,
                    )
                else:
                    gs = GridSearchCV(
                        model_[name],
                        param_grid=param_grid,
                        scoring=(
                            "roc_auc_ovr"
                            if purpose == "classification"
                            else "neg_mean_squared_error"
                        ),
                        cv=cv,
                        n_jobs=n_jobs,
                        verbose=verbose,
                    )
                # Fit GridSearchCV 
                gs.fit(x_train, y_train) 
                final_estimators[name]=gs.best_estimator_
    
            #* Set up cross-validation and performance evaluation
            scorer = make_scorer(accuracy_score) 
            cv_results = []

            #*Cross-validate stacking models with different final estimators
            for final_name, final_estimator in final_estimators.items():
                print(f"Evaluating Stacking Classifier with {final_name} as final estimator...")
                if purpose == "classification":
                    stacking_model = StackingClassifier(estimators=base_estimators, final_estimator=final_estimator,cv=cv)
                else:
                    stacking_model = StackingRegressor(estimators=base_estimators, final_estimator=final_estimator, cv=cv)
            
                scores = cross_val_score(stacking_model, x_train, y_train, cv=StratifiedKFold(n_splits=cv_folds, shuffle=True, random_state=random_state), scoring=scorer)
                
                # Store the result
                cv_results.append({
                    'final_estimator':final_estimator,
                    'Final Estimator': final_name,
                    'Mean Accuracy': np.mean(scores),
                    'Standard Deviation': np.std(scores)
                })

            #* Convert the results into a DataFrame for easy comparison
            cv_results_df = pd.DataFrame(cv_results)

            #* Sort and display the best model
            cv_results_df = cv_results_df.sort_values(by='Mean Accuracy', ascending=False)


            # Optionally: Select the final estimator that gives the best performance
            best_final_estimator = cv_results_df.iloc[0]['final_estimator']
            print(f"Best final estimator based on cross-validation: {best_final_estimator}")
        else:
            print(f"⤵ trying to find the best_final_estimator for stacking...")  
            if purpose=="classification":
                best_final_estimator = LogisticRegression(class_weight=class_weight, 
                                                        random_state=random_state,
                                                        max_iter=1000)
            else:
                best_final_estimator = RidgeCV(cv=5)
        print(f"⤵ the best best_final_estimator: {best_final_estimator}")
        #! apply stacking
        if purpose == "classification":
            print(f"⤵ StackingClassifier...")  
            stacking_model = StackingClassifier(estimators=base_estimators, 
                                                final_estimator=best_final_estimator,
                                                cv=cv)
        else:
            print(f"⤵ StackingRegressor...")  
            stacking_model = StackingRegressor(estimators=base_estimators, 
                                            final_estimator=best_final_estimator,
                                            cv=cv)

        # Train the Stacking Classifier
        print(f"⤵ fit & predict...")
        stacking_model.fit(x_train, y_train)
        y_pred_final = stacking_model.predict(x_true)
        print(f"⤵ collecting results...")
        # pred_proba
        if is_binary:
            if hasattr(stacking_model, "predict_proba"):
                y_pred_proba_final = stacking_model.predict_proba(x_true)
                if y_pred_proba_final.shape[1] == 1:
                    y_pred_proba_final = np.hstack(
                        [1 - y_pred_proba_final, y_pred_proba_final]
                    )  # Add missing class probabilities
                y_pred_proba_final = y_pred_proba_final[:, 1]
            elif hasattr(stacking_model, "decision_function"):
                # If predict_proba is not available, use decision_function (e.g., for SVM)
                y_pred_proba_final = stacking_model.decision_function(x_true)
                # Ensure y_pred_proba_final is within 0 and 1 bounds
                y_pred_proba_final = (y_pred_proba_final - y_pred_proba_final.min()) / (
                    y_pred_proba_final.max() - y_pred_proba_final.min()
                )
            else:
                y_pred_proba_final = None  # No probability output for certain models
            # Access alphas if applicable (e.g., ElasticNetCV, LassoCV)
            if hasattr(best_clf, "alphas_") or hasattr(best_clf, "Cs_"):
                if hasattr(best_clf, "alphas_"):
                    alphas_ = best_clf.alphas_
                elif hasattr(best_clf, "alpha_"):
                    alphas_ = best_clf.alpha_
                elif hasattr(best_clf, "Cs_"):
                    alphas_ = best_clf.Cs_
            else: 
                alphas_= None
            coef_ = best_clf.coef_ if hasattr(best_clf, "coef_") else None 
        if not is_binary:
            # Handle prediction probabilities for multiclass
            if hasattr(stacking_model, "predict_proba"):
                y_pred_proba_final = stacking_model.predict_proba(x_true)
            elif hasattr(stacking_model, "decision_function"):
                y_pred_proba_final = stacking_model.decision_function(x_true)

                # Normalize for multiclass if necessary
                if y_pred_proba_final.ndim == 2:
                    y_pred_proba_final = (
                        y_pred_proba_final - y_pred_proba_final.min(axis=1, keepdims=True)
                    ) / (
                        y_pred_proba_final.max(axis=1, keepdims=True)
                        - y_pred_proba_final.min(axis=1, keepdims=True)
                    )
            else:
                y_pred_proba_final = None  # No probability output for certain models
            # Access alphas if applicable (e.g., ElasticNetCV, LassoCV)
            if hasattr(best_clf, "alphas_") or hasattr(best_clf, "Cs_"):
                if hasattr(best_clf, "alphas_"):
                    alphas_ = best_clf.alphas_
                elif hasattr(best_clf, "alpha_"):
                    alphas_ = best_clf.alpha_
                elif hasattr(best_clf, "Cs_"):
                    alphas_ = best_clf.Cs_
            else: 
                alphas_= None
            coef_ = best_clf.coef_ if hasattr(best_clf, "coef_") else None 
        #! dict_pred_stack
        dict_pred_stack={}
        validation_scores_final = {}
        if y_true is not None and y_pred_proba_final is not None:
            validation_scores_final = cal_metrics(
                y_true,
                y_pred_final,
                y_pred_proba=y_pred_proba_final,
                is_binary=is_binary,
                purpose=purpose,
                average="weighted",
            )
            if is_binary:
                # Calculate ROC curve
                # https://scikit-learn.org/stable/auto_examples/model_selection/plot_roc.html
                if y_pred_proba_final is not None:
                    fpr, tpr, _ = roc_curve(y_true, y_pred_proba_final)
                    lower_ci, upper_ci = cal_auc_ci(
                        y_true, y_pred_proba_final, verbose=False, is_binary=is_binary
                    )
                    roc_auc = auc(fpr, tpr)
                    roc_info = {
                        "fpr": fpr.tolist(),
                        "tpr": tpr.tolist(),
                        "auc": roc_auc,
                        "ci95": (lower_ci, upper_ci),
                    }
                    # precision-recall curve
                    precision_, recall_, _ = cal_precision_recall(y_true, y_pred_proba_final)
                    avg_precision_ = average_precision_score(y_true, y_pred_proba_final)
                    pr_info = {
                        "precision": precision_,
                        "recall": recall_,
                        "avg_precision": avg_precision_,
                    }
                else:
                    roc_info, pr_info = None, None
                if purpose == "classification":
                    dict_pred_stack = {
                        "best_clf": stacking_model,
                        "best_params": None,
                        "auc_indiv": None,
                        "scores": validation_scores_final,
                        "roc_curve": roc_info,
                        "pr_curve": pr_info,
                        "confusion_matrix": confusion_matrix(y_true, y_pred_final),
                        "predictions": y_pred_final.tolist(),
                        "predictions_proba": (
                            y_pred_proba_final.tolist() if y_pred_proba_final is not None else None
                        ),
                        "features":share_col_names,
                        "coef":coef_,
                        "alphas":alphas_
                    }
                else:  # "regression"
                    dict_pred_stack = {
                        "best_clf": stacking_model,
                        "best_params": None,
                        "scores": validation_scores_final,  # e.g., neg_MSE, R², etc.
                        "predictions": y_pred_final.tolist(),
                        "predictions_proba": (
                            y_pred_proba_final.tolist() if y_pred_proba_final is not None else None
                        ),
                        "features":share_col_names,
                        "coef":coef_,
                        "alphas":alphas_
                    }
            else:  # multi-classes
                if y_pred_proba_final is not None:
                    # fpr, tpr, roc_auc = dict(), dict(), dict()
                    # fpr, tpr, _ = roc_curve(y_true, y_pred_proba_final)
                    confidence_intervals = cal_auc_ci(
                        y_true, y_pred_proba_final, verbose=False, is_binary=is_binary
                    )
                    roc_info = {
                        "fpr": validation_scores_final["fpr"],
                        "tpr": validation_scores_final["tpr"],
                        "auc": validation_scores_final["roc_auc_by_class"],
                        "ci95": confidence_intervals,
                    }
                    # precision-recall curve
                    precision_, recall_, avg_precision_ = cal_precision_recall(
                        y_true, y_pred_proba_final, is_binary=is_binary
                    )
                    pr_info = {
                        "precision": precision_,
                        "recall": recall_,
                        "avg_precision": avg_precision_,
                    }
                else:
                    roc_info, pr_info = None, None

                if purpose == "classification":
                    dict_pred_stack = {
                        "best_clf": stacking_model,
                        "best_params": None,
                        "auc_indiv": None,
                        "scores": validation_scores_final,
                        "roc_curve": roc_info,
                        "pr_curve": pr_info,
                        "confusion_matrix": confusion_matrix(y_true, y_pred_final),
                        "predictions": y_pred_final.tolist(),
                        "predictions_proba": (
                            y_pred_proba_final.tolist() if y_pred_proba_final is not None else None
                        ),
                        "features":share_col_names,
                        "coef":coef_,
                        "alphas":alphas_
                    }
                else:  # "regression"
                    dict_pred_stack = {
                        "best_clf": stacking_model,
                        "best_params": None,
                        "scores": validation_scores_final,  # e.g., neg_MSE, R², etc.
                        "predictions": y_pred_final.tolist(),
                        "predictions_proba": (
                            y_pred_proba_final.tolist() if y_pred_proba_final is not None else None
                        ),
                        "features":share_col_names,
                        "coef":coef_,
                        "alphas":alphas_
                    }

        else:
            if y_true is None:
                validation_scores_final = []
            else:
                validation_scores_final = cal_metrics(
                    y_true,
                    y_pred,
                    y_pred_proba=y_pred_proba_final,
                    is_binary=is_binary,
                    purpose=purpose,
                    average="weighted",
                )
            dict_pred_stack = {
                "best_clf": stacking_model,
                "best_params": None,
                "scores": validation_scores_final,
                "predictions": y_pred_final.tolist(),
                "predictions_proba": (
                    y_pred_proba_final.tolist() if y_pred_proba_final is not None else None
                ),
                "features":share_col_names,
                "y_train": y_train if y_train is not None else [],
                "y_true": y_true if y_true is not None else [],
                "coef":coef_,
                "alphas":alphas_
            }
        # merge together
        df_pred = pd.DataFrame(
        [None] * len(df_results.columns), index=df_results.columns, columns=["stack"]).T
        for k, v in dict_pred_stack.items():
            if k in df_pred.columns:
                df_pred[k] = [v]

        # # plot the stacking 
        # if all([plot_, y_true is not None, purpose == "classification"]): 
        #     plot_validate_features_single(df_pred, is_binary=is_binary)
        #     if dir_save:
        #         ips.figsave(dir_save + f"validate_features_stacking_{now_}.pdf") 
    if vote:
        print(f"⤵ voting...")
        from sklearn.ensemble import VotingClassifier, VotingRegressor
        #! voting
        n_top_models = min(n_top_models, df_results.shape[0]) 
        base_estimators=[]
        for name, cls in zip(list(df_results.iloc[:n_top_models, :].index),df_results.iloc[:n_top_models, :]["best_clf"].tolist()):
            base_estimators.append((name,cls))
        # Apply Voting Classifier/Regressor
        if purpose == "classification":
            print(f"⤵ VotingClassifier...via{voting}")
            if voting=='hard':
                # Hard voting does not support `predict_proba`
                voting_model = VotingClassifier(estimators=base_estimators) 
            else:
                # Soft voting supports `predict_proba`
                voting_model = VotingClassifier(estimators=base_estimators, voting="soft")
        else:
            print(f"⤵ VotingRegressor...")
            voting_model = VotingRegressor(estimators=base_estimators)

        # Train the Voting Classifier/Regressor
        try:
            voting_model.fit(x_train, y_train)
            y_pred_vote = voting_model.predict(x_true)
        except Exception as e:
            if purpose == "classification" and not voting=='hard':
                voting_model = VotingClassifier(estimators=base_estimators)
                voting_model.fit(x_train, y_train)
                y_pred_vote = voting_model.predict(x_true)

        # Calculate predicted probabilities if applicable
        if purpose == "classification":
            if hasattr(voting_model, "predict_proba"):
                y_pred_proba_vote = voting_model.predict_proba(x_true)
                print("Shape of predicted probabilities:", y_pred_proba_vote.shape)
                if y_pred_proba_vote.shape[1] == 1:
                    y_pred_proba_vote = np.hstack(
                        [1 - y_pred_proba_vote, y_pred_proba_vote]
                    )  # Add missing class probabilities
                y_pred_proba_vote = y_pred_proba_vote[:, 1]
            else:
                y_pred_proba_vote = None
                
            # Access alphas if applicable (e.g., ElasticNetCV, LassoCV)
            if hasattr(best_clf, "alphas_") or hasattr(best_clf, "Cs_"):
                if hasattr(best_clf, "alphas_"):
                    alphas_ = best_clf.alphas_
                elif hasattr(best_clf, "alpha_"):
                    alphas_ = best_clf.alpha_
                elif hasattr(best_clf, "Cs_"):
                    alphas_ = best_clf.Cs_
            else: 
                alphas_= None
            coef_ = best_clf.coef_ if hasattr(best_clf, "coef_") else None 
        else:  # Regression
            y_pred_proba_vote = None
            coef_,alphas_=None,None

        print(f"⤵ collecting voting results...")
        #! dict_pred_vote
        dict_pred_vote = {}
        validation_scores_vote = {}
        if y_true is not None and y_pred_proba_vote is not None:
            validation_scores_vote = cal_metrics(
                y_true,
                y_pred_vote,
                y_pred_proba=y_pred_proba_vote,
                is_binary=is_binary,
                purpose=purpose,
                average="weighted",
            )

            if is_binary:
                if y_pred_proba_vote is not None:
                    fpr, tpr, _ = roc_curve(y_true, y_pred_proba_vote)
                    lower_ci, upper_ci = cal_auc_ci(
                        y_true, y_pred_proba_vote, verbose=False, is_binary=is_binary
                    )
                    roc_auc = auc(fpr, tpr)
                    roc_info = {
                        "fpr": fpr.tolist(),
                        "tpr": tpr.tolist(),
                        "auc": roc_auc,
                        "ci95": (lower_ci, upper_ci),
                    }
                    precision_, recall_, _ = cal_precision_recall(y_true, y_pred_proba_vote)
                    avg_precision_ = average_precision_score(y_true, y_pred_proba_vote)
                    pr_info = {
                        "precision": precision_,
                        "recall": recall_,
                        "avg_precision": avg_precision_,
                    }
                else:
                    roc_info, pr_info = None, None

                dict_pred_vote = {
                    "best_clf": voting_model,
                    "best_params": None,
                    "auc_indiv": None,
                    "scores": validation_scores_vote,
                    "roc_curve": roc_info,
                    "pr_curve": pr_info,
                    "confusion_matrix": confusion_matrix(y_true, y_pred_vote),
                    "predictions": y_pred_vote.tolist(),
                    "predictions_proba": (
                        y_pred_proba_vote.tolist() if y_pred_proba_vote is not None else None
                    ),
                    "features":share_col_names,
                    "coef":coef_,
                    "alphas":alphas_
                }
            else:  # Multi-class
                if y_pred_proba_vote is not None:
                    confidence_intervals = cal_auc_ci(
                        y_true, y_pred_proba_vote, verbose=False, is_binary=is_binary
                    )
                    roc_info = {
                        "fpr": validation_scores_vote["fpr"],
                        "tpr": validation_scores_vote["tpr"],
                        "auc": validation_scores_vote["roc_auc_by_class"],
                        "ci95": confidence_intervals,
                    }
                    precision_, recall_, avg_precision_ = cal_precision_recall(
                        y_true, y_pred_proba_vote, is_binary=is_binary
                    )
                    pr_info = {
                        "precision": precision_,
                        "recall": recall_,
                        "avg_precision": avg_precision_,
                    }
                else:
                    roc_info, pr_info = None, None

                dict_pred_vote = {
                    "best_clf": voting_model,
                    "best_params": None,
                    "scores": validation_scores_vote,
                    "roc_curve": roc_info,
                    "pr_curve": pr_info,
                    "confusion_matrix": confusion_matrix(y_true, y_pred_vote),
                    "predictions": y_pred_vote.tolist(),
                    "predictions_proba": (
                        y_pred_proba_vote.tolist() if y_pred_proba_vote is not None else None
                    ),
                    "features":share_col_names,
                    "coef":coef_,
                    "alphas":alphas_
                }
        else:
            if y_true is None:
                validation_scores_vote = []
            else:
                validation_scores_vote = cal_metrics(
                    y_true,
                    y_pred,
                    y_pred_proba=y_pred_proba_vote,
                    is_binary=is_binary,
                    purpose=purpose,
                    average="weighted",
                )
            dict_pred_vote = {
                "best_clf": voting_model,
                "best_params": None,
                "scores": validation_scores_vote,
                "predictions": y_pred_vote.tolist(),
                "predictions_proba": (
                    y_pred_proba_vote.tolist() if y_pred_proba_vote is not None else None
                ),
                "features":share_col_names,
                "y_train": y_train if y_train is not None else [],
                "y_true": y_true if y_true is not None else [],
            }
        df_vote = pd.DataFrame(
        [None] * len(df_results.columns), index=df_results.columns, columns=["vote"]).T
        for k, v in dict_pred_vote.items():
            if k in df_vote.columns:
                df_vote[k] = [v]

        # if all([plot_, y_true is not None, purpose == "classification"]):
        #     try:
        #         plot_validate_features_single(df_vote, is_binary=is_binary)
        #         if dir_save:
        #             ips.figsave(dir_save + f"validate_features_vote_{now_}.pdf")
        #     except Exception as e:
        #         print(e)
    print("Done")
    if vote and stack:
        df_res=pd.concat([df_pred,df_vote, df_results],ignore_index=False,axis=0)
    elif vote:
        df_res=pd.concat([df_vote, df_results],ignore_index=False,axis=0)
    elif stack:
        df_res=pd.concat([df_pred,df_results],ignore_index=False,axis=0)
    else:
        df_res=df_results
        
    if all([plot_, y_true is not None, purpose == "classification"]):
        from datetime import datetime

        now_ = datetime.now().strftime("%y%m%d_%H%M%S")
        # try:
        if df_res.shape[0] > 3:
            try:
                plot_validate_features(df_res, is_binary=is_binary)
            except Exception as e:
                print(e)
        else:
            try:
                plot_validate_features_single(df_res, is_binary=is_binary)
            except Exception as e:
                print(e)
        if dir_save:
            ips.figsave(dir_save + f"validate_features{now_}.pdf")
    # except Exception as e:
    #     print(f"Error: 在画图的过程中出现了问题:{e}")
    return df_res

def cal_metrics(
    y_true,
    y_pred,
    y_pred_proba=None,
    is_binary=True,
    purpose="regression",
    average="weighted",
):
    """
    Calculate regression or classification metrics based on the purpose.

    Parameters:
    - y_true: Array of true values.
    - y_pred: Array of predicted labels for classification or predicted values for regression.
    - y_pred_proba: Array of predicted probabilities for classification (optional).
    - purpose: str, "regression" or "classification".
    - average: str, averaging method for multi-class classification ("binary", "micro", "macro", "weighted", etc.).

    Returns:
    - validation_scores: dict of computed metrics.
    """
    from sklearn.metrics import (
        mean_squared_error,
        mean_absolute_error,
        mean_absolute_percentage_error,
        explained_variance_score,
        r2_score,
        mean_squared_log_error,
        accuracy_score,
        precision_score,
        recall_score,
        f1_score,
        roc_auc_score,
        matthews_corrcoef,
        confusion_matrix,
        balanced_accuracy_score,
        average_precision_score,
        precision_recall_curve,
    )

    validation_scores = {}

    if purpose == "regression":
        y_true = np.asarray(y_true)
        y_true = y_true.ravel()
        y_pred = np.asarray(y_pred)
        y_pred = y_pred.ravel()
        # Regression metrics
        validation_scores = {
            "mse": mean_squared_error(y_true, y_pred),
            "rmse": np.sqrt(mean_squared_error(y_true, y_pred)),
            "mae": mean_absolute_error(y_true, y_pred),
            "r2": r2_score(y_true, y_pred),
            "mape": mean_absolute_percentage_error(y_true, y_pred),
            "explained_variance": explained_variance_score(y_true, y_pred),
            "mbd": np.mean(y_pred - y_true),  # Mean Bias Deviation
        }
        # Check if MSLE can be calculated
        if np.all(y_true >= 0) and np.all(y_pred >= 0):  # Ensure no negative values
            validation_scores["msle"] = mean_squared_log_error(y_true, y_pred)
        else:
            validation_scores["msle"] = "Cannot be calculated due to negative values"

    elif purpose == "classification":
        # Classification metrics
        validation_scores = {
            "accuracy": accuracy_score(y_true, y_pred),
            "precision": precision_score(y_true, y_pred, average=average),
            "recall": recall_score(y_true, y_pred, average=average),
            "f1": f1_score(y_true, y_pred, average=average),
            "mcc": matthews_corrcoef(y_true, y_pred),
            "specificity": None,
            "balanced_accuracy": balanced_accuracy_score(y_true, y_pred),
        }

        # Confusion matrix to calculate specificity
        if is_binary:
            cm = confusion_matrix(y_true, y_pred)
            if cm.size == 4:
                tn, fp, fn, tp = cm.ravel()
            else:
                # Handle single-class predictions
                tn, fp, fn, tp = 0, 0, 0, 0
                print("Warning: Only one class found in y_pred or y_true.")

            # Specificity calculation
            validation_scores["specificity"] = tn / (tn + fp) if (tn + fp) > 0 else 0
            if y_pred_proba is not None:
                # Calculate ROC-AUC
                validation_scores["roc_auc"] = roc_auc_score(y_true, y_pred_proba)
                # PR-AUC (Precision-Recall AUC) calculation
                validation_scores["pr_auc"] = average_precision_score(
                    y_true, y_pred_proba
                )

        else:  # multi-class
            from sklearn.preprocessing import label_binarize

            # * Multi-class ROC calculation
            y_pred_proba = np.asarray(y_pred_proba)
            classes = np.unique(y_true)
            y_true_bin = label_binarize(y_true, classes=classes)
            if isinstance(y_true, np.ndarray):
                y_true = ips.df_encoder(
                    data=pd.DataFrame(y_true), method="dum", prefix="Label"
                )
            # Initialize dictionaries to store FPR, TPR, and AUC for each class
            fpr = dict()
            tpr = dict()
            roc_auc = dict()
            for i, class_label in enumerate(classes):
                fpr[class_label], tpr[class_label], _ = roc_curve(
                    y_true_bin[:, i], y_pred_proba[:, i]
                )
                roc_auc[class_label] = auc(fpr[class_label], tpr[class_label])

            # Store the mean ROC AUC
            try:
                validation_scores["roc_auc"] = roc_auc_score(
                    y_true, y_pred_proba, multi_class="ovr", average=average
                )
            except Exception as e:
                y_pred_proba = y_pred_proba / y_pred_proba.sum(axis=1, keepdims=True)
                validation_scores["roc_auc"] = roc_auc_score(
                    y_true, y_pred_proba, multi_class="ovr", average=average
                )

            validation_scores["roc_auc_by_class"] = roc_auc  # Individual class AUCs
            validation_scores["fpr"] = fpr
            validation_scores["tpr"] = tpr

    else:
        raise ValueError(
            "Invalid purpose specified. Choose 'regression' or 'classification'."
        )

    return validation_scores


def plot_trees(
    X, y, cls:str='random', max_trees=500, test_size=0.2, random_state=42, early_stopping_rounds=None
):
    """
    # # Example usage:
        # X = np.random.rand(100, 10)  # Example data with 100 samples and 10 features
        # y = np.random.randint(0, 2, 100)  # Example binary target
        # # Using the function with different classifiers
        # # Random Forest example
        # plot_trees(X, y, RandomForestClassifier(), max_trees=100)
        # # Gradient Boosting with early stopping example
        # plot_trees(X, y, GradientBoostingClassifier(), max_trees=100, early_stopping_rounds=10)
        # # Extra Trees example
        # plot_trees(X, y, ExtraTreesClassifier(), max_trees=100)
    Master function to plot error rates (OOB, training, and testing) for different tree-based ensemble classifiers.

    Parameters:
    - X (array-like): Feature matrix.
    - y (array-like): Target labels.
    - cls (object): Tree-based ensemble classifier instance (e.g., RandomForestClassifier()).
    - max_trees (int): Maximum number of trees to evaluate. Default is 500.
    - test_size (float): Proportion of data to use as test set for testing error. Default is 0.2.
    - random_state (int): Random state for reproducibility. Default is 42.
    - early_stopping_rounds (int): For boosting models only, stops training if validation error doesn't improve after specified rounds.

    Returns:
    - None
    """
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score
    from sklearn.ensemble import (
        RandomForestClassifier,
        BaggingClassifier,
        ExtraTreesClassifier,
    )
    from sklearn.ensemble import AdaBoostClassifier, GradientBoostingClassifier

    # Split data for training and testing error calculation
    x_train, x_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    # Initialize lists to store error rates
    oob_error_rate = []
    train_error_rate = []
    test_error_rate = []
    validation_error = None
    if isinstance(cls, str):
        cls=ips.strcmp(cls, ["RandomForestClassifier","ExtraTreesClassifier","AdaBoostClassifier","GradientBoostingClassifier"])
    # Configure classifier based on type
    oob_enabled = False  # Default to no OOB error unless explicitly set
    clf_support = {"RandomForestClassifier":RandomForestClassifier(),
                    "ExtraTreesClassifier":ExtraTreesClassifier(),
                    "AdaBoostClassifier":AdaBoostClassifier(),
                    "GradientBoostingClassifier":GradientBoostingClassifier()}
    if isinstance(cls, (RandomForestClassifier, ExtraTreesClassifier)):
        # Enable OOB if cls supports it and is using bootstrapping
        cls.set_params(warm_start=True, n_estimators=1)
        if hasattr(cls, "oob_score"):
            cls.set_params(bootstrap=True, oob_score=True)
            oob_enabled = True
    elif isinstance(cls, BaggingClassifier):
        cls.set_params(warm_start=True, bootstrap=True, oob_score=True, n_estimators=1)
        oob_enabled = True
    elif isinstance(cls, (AdaBoostClassifier, GradientBoostingClassifier)):
        cls.set_params(n_estimators=1)
        oob_enabled = False
        if early_stopping_rounds:
            validation_error = []

    # Train and evaluate with an increasing number of trees
    for i in range(1, max_trees + 1):
        cls.set_params(n_estimators=i)
        cls.fit(x_train, y_train)

        # Calculate OOB error (for models that support it)
        if oob_enabled and hasattr(cls, "oob_score_") and cls.oob_score:
            oob_error = 1 - cls.oob_score_
            oob_error_rate.append(oob_error)

        # Calculate training error
        train_error = 1 - accuracy_score(y_train, cls.predict(x_train))
        train_error_rate.append(train_error)

        # Calculate testing error
        test_error = 1 - accuracy_score(y_test, cls.predict(x_test))
        test_error_rate.append(test_error)

        # For boosting models, use validation error with early stopping
        if early_stopping_rounds and isinstance(
            cls, (AdaBoostClassifier, GradientBoostingClassifier)
        ):
            val_error = 1 - accuracy_score(y_test, cls.predict(x_test))
            validation_error.append(val_error)
            if len(validation_error) > early_stopping_rounds:
                # Stop if validation error has not improved in early_stopping_rounds
                if validation_error[-early_stopping_rounds:] == sorted(
                    validation_error[-early_stopping_rounds:]
                ):
                    print(
                        f"Early stopping at tree {i} due to lack of improvement in validation error."
                    )
                    break

    # Plot results
    plt.figure(figsize=(10, 6))
    if oob_error_rate:
        plt.plot(
            range(1, len(oob_error_rate) + 1),
            oob_error_rate,
            color="black",
            label="OOB Error Rate",
            linewidth=2,
        )
    if train_error_rate:
        plt.plot(
            range(1, len(train_error_rate) + 1),
            train_error_rate,
            linestyle="dotted",
            color="green",
            label="Training Error Rate",
        )
    if test_error_rate:
        plt.plot(
            range(1, len(test_error_rate) + 1),
            test_error_rate,
            linestyle="dashed",
            color="red",
            label="Testing Error Rate",
        )
    if validation_error:
        plt.plot(
            range(1, len(validation_error) + 1),
            validation_error,
            linestyle="solid",
            color="blue",
            label="Validation Error (Boosting)",
        )

    # Customize plot
    plt.xlabel("Number of Trees")
    plt.ylabel("Error Rate")
    plt.title(f"Error Rate Analysis for {cls.__class__.__name__}")
    plt.legend(loc="upper right")
    plt.grid(True)
    plt.show()


def img_datasets_preprocessing(
    data: pd.DataFrame,
    x_col: str,
    y_col: str = None,
    target_size: tuple = (224, 224),
    batch_size: int = 128,
    class_mode: str = "raw",
    shuffle: bool = False,
    augment: bool = False,
    scaler: str = "normalize",  # 'normalize', 'standardize', 'clahe', 'raw'
    grayscale: bool = False,
    encoder: str = "label",  # Options: 'label', 'onehot', 'binary'
    label_encoder=None,
    kws_augmentation: dict = None,
    verbose: bool = True,
    drop_missing: bool = True,
    output="df",  # "iterator":data_iterator,'df':return DataFrame
):
    """
    Enhanced preprocessing function for loading and preparing image data from a DataFrame.

    Parameters:
    - df (pd.DataFrame): Input DataFrame with image paths and labels.
    - x_col (str): Column in `df` containing image file paths.
    - y_col (str): Column in `df` containing image labels.
    - target_size (tuple): Desired image size in (height, width).
    - batch_size (int): Number of images per batch.
    - class_mode (str): Mode of label ('raw', 'categorical', 'binary').
    - shuffle (bool): Shuffle the images in the DataFrame.
    - augment (bool): Apply data augmentation.
    - scaler (str): 'normalize',  # 'normalize', 'standardize', 'clahe', 'raw'
    - grayscale (bool): Convert images to grayscale.
    - normalize (bool): Normalize image data to [0, 1] range.
    - encoder (str): Label encoder method ('label', 'onehot', 'binary').
    - label_encoder: Optional pre-defined label encoder.
    - kws_augmentation (dict): Parameters for data augmentation.
    - verbose (bool): Print status messages.
    - drop_missing (bool): Drop rows with missing or invalid image paths.

    Returns:
    - pd.DataFrame: DataFrame with flattened image pixels and 'Label' column.
    """
    from tensorflow.keras.preprocessing.image import ImageDataGenerator
    from tensorflow.keras.utils import to_categorical
    from sklearn.preprocessing import LabelEncoder
    from PIL import Image
    import os

    # Validate input DataFrame for required columns
    if y_col:
        assert (
            x_col in data.columns and y_col in data.columns
        ), "Missing required columns in DataFrame."
    if y_col is None:
        class_mode = None
    # 输出格式
    output = ips.strcmp(
        output,
        [
            "generator",
            "tf",
            "iterator",
            "transform",
            "transformer",
            "dataframe",
            "df",
            "pd",
            "pandas",
        ],
    )[0]

    # Handle missing file paths
    if drop_missing:
        data = data[
            data[x_col].apply(
                lambda path: os.path.exists(path) and os.path.isfile(path)
            )
        ]

    # Encoding labels if necessary
    if encoder and y_col is not None:
        if encoder == "binary":
            data[y_col] = (data[y_col] == data[y_col].unique()[0]).astype(int)
        elif encoder == "onehot":
            if not label_encoder:
                label_encoder = LabelEncoder()
                data[y_col] = label_encoder.fit_transform(data[y_col])
            data[y_col] = to_categorical(data[y_col])
        elif encoder == "label":
            if not label_encoder:
                label_encoder = LabelEncoder()
                data[y_col] = label_encoder.fit_transform(data[y_col])

    # Set up data augmentation
    if augment:
        aug_params = {
            "rotation_range": 20,
            "width_shift_range": 0.2,
            "height_shift_range": 0.2,
            "shear_range": 0.2,
            "zoom_range": 0.2,
            "horizontal_flip": True,
            "fill_mode": "nearest",
        }
        if kws_augmentation:
            aug_params.update(kws_augmentation)
        dat = ImageDataGenerator(rescale=scaler, **aug_params)
        dat = ImageDataGenerator(
            rescale=1.0 / 255 if scaler == "normalize" else None, **aug_params
        )

    else:
        dat = ImageDataGenerator(rescale=1.0 / 255 if scaler == "normalize" else None)

    # Create DataFrameIterator
    data_iterator = dat.flow_from_dataframe(
        dataframe=data,
        x_col=x_col,
        y_col=y_col,
        target_size=target_size,
        color_mode="grayscale" if grayscale else "rgb",
        batch_size=batch_size,
        class_mode=class_mode,
        shuffle=shuffle,
    )
    print(f"target_size:{target_size}")
    if output.lower() in ["generator", "tf", "iterator", "transform", "transformer"]:
        return data_iterator
    elif output.lower() in ["dataframe", "df", "pd", "pandas"]:
        # Initialize list to collect processed data
        data_list = []
        total_batches = data_iterator.n // batch_size

        # Load, resize, and process images in batches
        for i, (batch_images, batch_labels) in enumerate(data_iterator):
            for img, label in zip(batch_images, batch_labels):
                if scaler == ["normalize", "raw"]:
                    # Already rescaled by 1.0/255 in ImageDataGenerator
                    pass
                elif scaler == "standardize":
                    # Standardize by subtracting mean and dividing by std
                    img = (img - np.mean(img)) / np.std(img)
                elif scaler == "clahe":
                    # Apply CLAHE to the image
                    img = apply_clahe(img)
                flat_img = img.flatten()
                data_list.append(np.append(flat_img, label))

            # Stop when all images have been processed
            if i >= total_batches:
                break

        # Define column names for flattened image data
        pixel_count = target_size[0] * target_size[1] * (1 if grayscale else 3)
        column_names = [f"pixel_{i}" for i in range(pixel_count)] + ["Label"]

        # Create DataFrame from flattened data
        df_img = pd.DataFrame(data_list, columns=column_names)

        if verbose:
            print("Processed images:", len(df_img))
            print("Final DataFrame shape:", df_img.shape)
            display(df_img.head())

        return df_img


def backward_regression(
    X: pd.DataFrame, y: pd.Series, initial_list=[], thr=0.05, verbose=True
):
    """
    # awesome bit of code from https://www.kaggle.com/code/adibouayjan/house-price-step-by-step-modeling

    Evaluates the p-values of all features, which represent the probability of observing a coefficient
    as extreme as the one calculated if the feature had no true effect on the target.

    Args:
        X -- features values
        y -- target variable
        initial_list -- features header
        thr -- pvalue threshold of features to drop
        verbose -- true to produce lots of logging output

    Returns:
        list of selected features for modeling
    """
    import statsmodels.api as sm
    if isinstance(y, str):
        if y in X.columns:
            y_col_name = y
            y = X[y]
            X = X.drop(y_col_name, axis=1)
        else:
            raise ValueError(f"找不到{y},y设置有误")
    X = X.select_dtypes(include=[np.number])
    
    included = list(X.columns)
    try:
        X=X.astype(float)
        y=y.astype(float)
    except Exception as e:
        raise ValueError(f"无法把数据类型转换成float类型,因而无法进一步进行统计分析: {e}")
        

    while True:
        changed = False
        if not included:
            print("No features remain in the model.")
            break

        model = sm.OLS(y, sm.add_constant(pd.DataFrame(X[included]))).fit()
        # exclude the intercept for p-value checking
        pvalues = model.pvalues.iloc[1:]
        worst_pval = pvalues.max()
        if worst_pval > thr:
            changed = True
            worst_feature = pvalues.idxmax()
            included.remove(worst_feature)
            if verbose:
                print(f"Removing '{worst_feature}' with p-value={round(worst_pval,2)}")
        if not changed:
            break
    print(f"\nSelected Features:\n{included}")
    return included  # Returns the list of selected features


# Function to apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
def apply_clahe(img):
    import cv2

    lab = cv2.cvtColor(img, cv2.COLOR_RGB2LAB)  # Convert to LAB color space
    l, a, b = cv2.split(lab)  # Split into channels
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)  # Apply CLAHE to the L channel
    limg = cv2.merge((cl, a, b))  # Merge back the channels
    img_clahe = cv2.cvtColor(limg, cv2.COLOR_LAB2RGB)  # Convert back to RGB
    return img_clahe
