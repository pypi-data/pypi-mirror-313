import pandas as pd
import numpy as np
import shap
import xgboost
import matplotlib.pyplot as plt
import seaborn as sns
import scipy
from scipy import stats
import random
from typing import Literal
import itertools
import random
from more_itertools import batched
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from imblearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression, LogisticRegressionCV, SGDClassifier
from sklearn.model_selection import train_test_split, GridSearchCV, PredefinedSplit
from sklearn.metrics import (
    mean_squared_error,
    roc_auc_score,
    balanced_accuracy_score,
    accuracy_score,
    confusion_matrix,
    ConfusionMatrixDisplay,
    average_precision_score,
    roc_curve,
    auc,
)


"""
Model object and other functions
"""


# feature importance
def plot_shap(X, y):
    """
    Plot shapley values for a model using XGboost
    """
    # xgboost model to assess feature importance
    # X, y = model.X_train[model.selected_cols], model.y_train
    xgb = xgboost.XGBClassifier(n_estimators=100, max_depth=2).fit(
        X, y * 1, eval_metric="logloss"
    )
    # compute SHAP values
    explainer = shap.Explainer(xgb)
    shap_values = explainer(X)

    # set a display version of the data to use for plotting (has string values)
    # shap_values.display_data = shap.datasets.adult(display=True)[0].values
    fig, axs = plt.subplots(figsize=(5, 5))
    shap.plots.bar(shap_values, max_display=None)
    fig, axs = plt.subplots(figsize=(5, 5))
    shap.plots.beeswarm(shap_values, max_display=None)
    return


def get_incidence(data, cols, target="Mortal"):
    """
    Get feature incidence and target rate plot
    """
    sizes = {}
    for col in cols:
        sizes[col] = {
            "Target Incidence": round(100 * data[data[col] == 1][target].mean(), 2),
            "Feature Incidence": round(100 * data[col].mean(), 2),
        }
    df_incidence = pd.DataFrame.from_dict(sizes).T.reset_index()
    fig, axs = plt.subplots(figsize=(12, len(cols) * 0.3))  # , frameon=False)
    sns.barplot(data=df_incidence, x="Target Incidence", y="index", ax=axs)
    axs.set_ylabel("Feature")
    axs.set_xlabel("Target Incidence (blue)")
    axs2 = axs.twiny()
    axs2.set_xlim([0, df_incidence["Feature Incidence"].max() + 1])
    sns.swarmplot(
        data=df_incidence, x="Feature Incidence", y="index", ax=axs2, color="darkorange"
    )
    axs2.set_xlabel("Feature Incidence (orange)")
    # fig.set_visible(False)
    plt.close()
    return fig


def plot_incidence(data, cols, target="Mortal"):
    """
    Plot feature incidence and target rate
    """
    fig = get_incidence(data, cols, target=target)
    fig.show()


# correlations
def feature_correlations(data, cols, target="Mortal", rows=[]):
    """
    Find feature correlations
    """
    if type(target) == list:
        target = target[0]
    if target in cols:
        cols.remove(target)
    cols = list(set(cols))
    corr = data[[target] + cols].corr(method="pearson")
    if len(rows) > 0:
        corr = corr.loc[rows]
    return corr, cols


def show_feature_correlations(data, cols, target="Mortal", rows=[]):
    """
    Display correlations with colour map
    """
    corr, cols = feature_correlations(data, cols, target=target, rows=rows)
    return corr.style.background_gradient(cmap="Reds")


def get_negative_correlations(data, cols, target="Mortal"):
    """
    Return features negatively correlated with target
    """
    corr, cols = feature_correlations(data, cols, target=target)
    remove_features = corr.loc[corr[target] < 0].index.values
    return remove_features


def get_feature_correlations(data, cols, target):
    """
    Return feature correlations with target, with feature count and incidence, for plotting correlation graph
    """
    corr, cols = feature_correlations(data, cols, target=target, rows=[])
    corr_sizes = data[cols].sum().reset_index(name="Count")
    corr_sizes["Incidence"] = 100 * (corr_sizes["Count"] / data.shape[0])
    corr_bar = corr[target][cols].reset_index()
    corr = pd.merge(corr_bar, corr_sizes, on="index", how="outer").sort_values(
        by=target
    )
    return corr


def plot_feature_correlations(
    data, cols, target, sizes: bool = False, size_threshold: float = 1
):
    """
    Plot correlation graph for single target only
    """
    corr = get_feature_correlations(data, cols, target)
    fig, axs = plt.subplots(figsize=(12, len(cols) * 0.3))
    sns.barplot(data=corr, x=target, y="index", ax=axs)
    axs.axvline(x=0, color="black", linestyle="--")
    axs.set_ylabel("Feature")
    axs.set_xlabel("Correlation with target")
    # add size of datapoints
    if sizes:
        axs2 = axs.twiny()
        sns.swarmplot(data=corr, x="Incidence", y="index", ax=axs2, color="darkorange")
        axs2.axvline(x=size_threshold, color="purple", linestyle="dotted")
        axs2.set_xlabel("Incidence (%)")
    fig.show()


def get_low_incidence(data, cols, target="Mortal", threshold: float = 1):
    """
    Return features with low incidence
    Args:
        threshold (float) : percentage incidence threshold under which to remove features
    """
    corr = get_feature_correlations(data, cols, target)
    remove_features = corr.loc[corr["Incidence"] < threshold]["index"].values
    return remove_features


def high_correlations(data, cols, threshold: float = 0.25, target="Mortal"):
    """
    Returns dictionary with keys of feature pairs and values of correlation, and list of features to drop based on lowest correlation with target.
    Ignore correlations between AgeBand features.
    Args:
        threshold (float) : Threshold above which to record high correlation.
    """
    corr, cols = feature_correlations(data, cols, rows=[], target=target)
    corr_high = {}
    key_label = 0
    for col in cols:
        df_corr = corr[col].reset_index(name="Value")
        df_corr.sort_values(by="Value", ascending=False, inplace=True)

        for i, coeff in enumerate(df_corr["Value"].values):
            if coeff > threshold:
                correlated_col = df_corr["index"].values[i]
                # correlated columns must not be the same, must not both be AgeBands, and must not be the target
                if (
                    (col != correlated_col)
                    & (
                        (col.split("_")[0] != "AgeBand")
                        | (correlated_col.split("_")[0] != "AgeBand")
                    )
                    & (col != target)
                    & (correlated_col != target)
                ):
                    ls = sorted([col, correlated_col])
                    if ls not in corr_high.values():   # Ensuring that duplicates are not added to the dictionary 
                        corr_high[key_label] = ls
                        key_label += 1
                    

    # highly correlated features
    corr_high = {
        k: v
        for k, v in sorted(corr_high.items(), key=lambda item: item[0], reverse=True)
    }

    # of these features, drop those with lowest correlation with target. iteratively, so as not to drop features unnecessarily
    features_to_drop = []
    for features in corr_high.values():
        # check if one of these features has already been dropped - if so, skip
        if (features[0] in features_to_drop) or (features[1] in features_to_drop):
            continue
        if corr[features[0]][target] > corr[features[1]][target]:
            features_to_drop.append(features[1])
        else:
            features_to_drop.append(features[0])
    # features_to_drop = list(set(features_to_drop))

    return corr_high, features_to_drop


def get_features_to_investigate(data, cols, threshold=0.15, target="Mortal"):
    corr, to_drop = high_correlations(
        data, cols=cols, threshold=threshold, target=target
    )
    investigate_corr = list(set(list(itertools.chain(*[i for i in corr.values()]))))
    return investigate_corr


def find_closest(arr, val):
    # TODO - check if this breaks anything for PTL - udpated for preop
    if len(arr) == 0:
        return np.nan
    idx = np.abs(arr - val).argmin()
    return idx


def find_cutoffs(target, predicted, readmission_rate):
    """Find the optimal probability cutoff point for a classification model related to event rate
    Parameters
    ----------
    target : Matrix with dependent or target data, where rows are observations
    predicted : Matrix with predicted data, where rows are observations

    Returns
    -------
    list type, with optimal cutoff value
    """
    fpr, tpr, threshold = roc_curve(target, predicted)
    roc = roc_auc_score(target, predicted)
    roc_weighted = roc_auc_score(target, predicted, average="weighted")
    prec = (tpr*readmission_rate)/(tpr*readmission_rate + fpr*(1-readmission_rate))

    # calculate the roc score for each threshold and locate the index of the largest roc score
    idx = np.arange(len(tpr))
    metrics = pd.DataFrame(
        {
            "threshold": pd.Series(threshold, index=idx),
            "gmean": pd.Series(np.sqrt(tpr * (1 - fpr)), index=idx),
            "roc": pd.Series(abs(tpr - (1 - fpr)), index=idx),
            "fbeta": pd.Series(((1+0.2)*prec*tpr)/(0.2*prec+tpr), index = idx)
        }
    )
    metrics = metrics.loc[
        (metrics["roc"] != 1.0) & (metrics["roc"] != 0.0) & (metrics["gmean"] != 0.0)
    ]
    gmean = metrics["gmean"].max()
    fbeta = metrics['fbeta'].max()
    th_values = metrics.loc[metrics["fbeta"] == fbeta]["threshold"].values
    # FIXME - what to do when th_values is empty? debug
    if len(th_values) > 0:
        th = th_values[0]

    # sns.scatterplot(metrics,x='threshold',y='gmean')

    return th, roc, roc_weighted, gmean, fbeta


# create object for storing trained models
class Model:
    def __init__(
        self, df, target: str = "Mortal", columns=None#, id_col: str = "ID"
    ):

        def _get_initial_df(df, target, columns):
            if columns == None:
                return df
            else:
                return df[['AdmissionDate'] + [target] + columns]


        self.data = _get_initial_df(df, target, columns)
        self.target = target
        self.filtered_cols = columns if columns is not None else df.columns
        self.selected_cols = columns if columns is not None else df.columns
        self.grid_search_results = {}
        self.model = None  # make_pipeline(
        # LogisticRegression(solver="newton-cg", penalty="none", random_state=0)
        # LogisticRegression(solver="newton-cg", penalty=None, random_state=0))
        self.params = []
        self.coefs = {}
        self.roc = 0
        self.roc_weighted = 0
        self.gmean = 0
        self.roc_val = 0
        self.roc_weighted_val = 0
        self.gmean_val = 0
        self.threshold = 0
        self.metrics = {}  # evaluated in evaluate_model_performance
        self.confusion_matrix = {}
        self.correlations = pd.DataFrame()
        self.hyperparameters = {}
        self.best_hyperparameters = {}

    def filter_features(self, all_rel_cols):
        """remove cols not in our data or where mean=0 or 1"""
        print("-------------------------------")
        print("Columns not in our data, with zero mean or constant value:")
        print("-------------------------------")
        remove_cols = []
        for col in all_rel_cols:
            if (
                (col not in self.data.columns)
                | (self.data[col].mean() == 0)
                | (self.data[col].nunique() == 1)
            ):
                print(col)
                remove_cols.append(col)
        filtered_cols = list(set(all_rel_cols).difference(set(remove_cols)))
        self.filtered_cols = filtered_cols
        return

    def remove_features(self, features):
        self.filtered_cols = list(set(self.filtered_cols).difference(set(features)))
        return

    def show_feature_correlations(self):
        return show_feature_correlations(
            self.data, self.filtered_cols, rows=[], target=self.target
        )

    def high_correlations(self, threshold: float = 0.25):
        """
        Returns dictionary with keys of feature pairs and values of correlation.
        Args:
            threshold (float) : Threshold above which to record high correlation.
        """
        return high_correlations(
            self.data,
            [self.target] + self.filtered_cols,
            threshold=threshold,
            target=self.target,
        )

    def split_data(self, test_size: float = 0.3, preop=False):
        """
        Get train,test,val sets.
        If column 'Set' exists, split by 'Set'.
        If column 'Set' doesn't exist, train_test_split is performed here.
        """

        if "Set" not in self.data.columns:
            if preop:
                # s plit according to procedure / procedure group
                X_train = pd.DataFrame()
                X_test = pd.DataFrame()
                X_val = pd.DataFrame()

                for proc in self.data["Procedure"].unique():
                    data_sub = self.data.loc[self.data["Procedure"] == proc]
                    X_train_sub, X_test_sub, y_train, y_test = train_test_split(
                        data_sub[self.filtered_cols],
                        data_sub[self.target],
                        test_size=test_size,
                        random_state=42,
                        shuffle=True,
                    )
                    # Further splitting the test into validation (10%) and test (20%)
                    X_val_sub, X_test_sub, y_val, y_test = train_test_split(
                        X_test_sub,
                        y_test,
                        test_size=0.666667,
                        random_state=42,
                        shuffle=True,
                    )
                    X_train = pd.concat([X_train, X_train_sub])
                    X_test = pd.concat([X_test, X_test_sub])
                    X_val = pd.concat([X_val, X_val_sub])

            else:
                X_train, X_test, y_train, y_test = train_test_split(
                    self.data[self.filtered_cols],
                    self.data[self.target],
                    test_size=test_size,
                    random_state=42,
                    shuffle=True,
                )
                # Further splitting the test into validation (10%) and test (20%)
                X_val, X_test, y_val, y_test = train_test_split(
                    X_test, y_test, test_size=0.666667, random_state=42, shuffle=True
                )
            # TODO - this is slow for larger datasets, replace with merge?
            self.data.loc[self.data.index.isin(X_train.index), "Set"] = "Train"
            self.data.loc[self.data.index.isin(X_test.index), "Set"] = "Test"
            self.data.loc[self.data.index.isin(X_val.index), "Set"] = "Val"
        else:
            X_train = self.data.loc[self.data["Set"] == "Train"]
            X_test = self.data.loc[self.data["Set"] == "Test"]
            X_val = self.data.loc[self.data["Set"] == "Val"]
        print("-------------------------------")
        print("Train, test, validation split:")
        print("-------------------------------")
        """self.X_train = self.data.loc[self.data["Set"] == "Train"]
        self.X_test = self.data.loc[self.data["Set"] == "Test"]
        self.X_val = self.data.loc[self.data["Set"] == "Val"]

        self.y_train = self.X_train[self.target]
        self.y_test = self.X_test[self.target]
        self.y_val = self.X_val[self.target]"""

        print(X_train.shape[0], X_test.shape[0], X_val.shape[0])

        def perc_tot(num, denom):
            return "{0}%".format(round(100 * num.shape[0] / denom.shape[0], 2))

        print(
            perc_tot(X_train, self.data),
            perc_tot(X_test, self.data),
            perc_tot(X_val, self.data),
        )

    def hyperparameter_tuning(
        self,
        p_threshold: float = 0.1,
        solvers: None | list = None,
        penalties: None | list = None,
        C: None | list = None,
    ):
        # uses train model method defined in the Model class instead of standard model fit
        hyperparameter_evaluation = {}

        if solvers == None:
            solvers = [
                "newton-cg",
                "lbfgs",
                "sag",
                "saga",
            ]  # , 'newton-cholesky',  #'liblinear' - smaller sets
        if penalties == None:
            penalties = [None, "l2", "l1"]  #'elasticnet']
        if C == None:
            C = [1]

        for c in C:
            for solver in solvers:
                penalties_iter = penalties
                if (solver != "saga") and ("l1" in penalties):
                    penalties_iter.remove("l1")
                for penalty in penalties_iter:
                    print("Solver: ", solver)
                    print("Penalty: ", penalty)
                    self.train_model(
                        solver=solver, penalty=penalty, p_threshold=p_threshold, C=c
                    )

                    eval = {}
                    for evaluate_set in ["Train", "Val"]:
                        metrics = self.evaluate_model_performance(
                            evaluate_set=evaluate_set, show=False
                        )
                        eval[evaluate_set] = {
                            "metrics": metrics,
                            "solver": solver,
                            "penalty": penalty,
                            "C": c,
                        }
                    hyperparameter_evaluation[(solver, penalty, c)] = eval

                self.hyperparameters = hyperparameter_evaluation

    def get_best_hyperparameters(self):
        best_roc = 0
        for method in self.hyperparameters:
            params = self.hyperparameters[method]["Val"]
            roc = params["metrics"]["ROC"]
            solver = params["solver"]
            penalty = params["penalty"]
            c = params["C"]

            if roc > best_roc:
                best_roc = roc
                self.best_hyperparameters["penalty"] = penalty
                self.best_hyperparameters["solver"] = solver
                self.best_hyperparameters["C"] = c

                self.best_hyperparameters["roc"] = best_roc
        return

    def grid_search(
        self,
        parameters: dict = {
            "solver": ("newton-cg", "liblinear"),
            "penalty": ("l2", "none"),
        },
    ):  # , 'C':[1, 10]}):
        # {'solver':('newton-cg', 'linlinear','lbfgs'), 'penalty': ('l1','l2','elasticnet','none'), 'C':[1, 10]}):
        estimator = LogisticRegression()
        clf = GridSearchCV(estimator, param_grid=parameters, error_score=0.0)
        X = self.X_val[self.selected_cols]
        y = self.X_val[self.target]
        clf.fit(X, y)
        self.grid_search_results = clf.cv_results_
        return

    def get_best_params(self):
        best_params_idx = list(
            np.where(self.grid_search_results["rank_test_score"] == 1)[0]
        )
        best_params = []
        for idx in best_params_idx:
            best_params.append(self.grid_search_results["params"][idx])
        return best_params

    def train_model(
        self,
        solver: str = "newton-cg",
        penalty=None,
        C: float = 1,
        show: bool = True,
        class_weight=None,
        classifier: Literal[
            "LogisticRegression", "LogisticRegressionCV", "SGDClassifier"
        ] = "LogisticRegression",
        p_threshold: float = 0.1,
        pos_only: bool = False,
    ):
        """
        Args:
            solver (str) : solver. defaults to 'newton-cg'.
            penalty: penalty. defaults to None.
            C (float) : regularisation strength
            show (bool) : whether to print results. defaults to True.
            class_weight : class_weight method in LogisticRegression. defaults to None.
            classifier (Literal): Classifier to use. Defaults to LogisticRegression.
            p_threshold (float) : pvalue significance level threshold. defaults to 0.1.
            pos_only (bool) : whether to drop negative coefficients at each iteration. defaults to False.
        """
        self.coefs = {}
        self.selected_cols = self.filtered_cols.copy()
        i = 0
        stop = False
        train = self.data[self.data["Set"] == "Train"]
        X_train = train[self.selected_cols]
        y_train = train[self.target]
        while stop == False:
            i += 1
            if show:
                print("------------------------------------")
                print("Iteration", i)
            # Initiate classifier object
            if classifier == "SGDClassifier":
                estimator = "sgdclassifier"
                """self.model = make_pipeline(
                SGDClassifier(loss="log_loss", penalty=penalty, random_state=0,class_weight=class_weight), #n_jobs=-1),
                )"""
                # without pipeline
                self.model = SGDClassifier(
                    loss="log_loss",
                    penalty=penalty,
                    random_state=0,
                    class_weight=class_weight,
                )
            elif classifier == "LogisticRegressionCV":
                estimator = "logisticregressioncv"
                self.model = make_pipeline(
                    LogisticRegressionCV(
                        cv=3,
                        solver=solver,
                        penalty=penalty,
                        random_state=0,
                        class_weight=class_weight,
                        scoring="roc_auc",
                    ),  # n_jobs=-1,
                )
            else:
                estimator = "logisticregression"
                self.model = make_pipeline(
                    LogisticRegression(
                        solver=solver,
                        penalty=penalty,
                        C=C,
                        random_state=0,
                        class_weight=class_weight,
                    ),  # n_jobs=-1),
                )
                # self.model = LogisticRegression(solver=solver, penalty=penalty, C=C, random_state=0,class_weight=class_weight, warm_start=True)

            # Fit model. Let X_train = matrix of predictors, y_train = matrix of variable.
            # NOTE: Do not include a column for the intercept when fitting the model.

            # TODO  - remove test sample limit - kernel dies with fitting model on very large dataset size
            test_sample_limit = int(1e10)  # no limit
            # train = self.data[self.data["Set"] == "Train"]
            X_train = train[self.selected_cols]
            # y_train = train[self.target]

            print("before fit")
            if classifier == "SGDClassifier":
                # partial fit since dataset too large to fit in memory
                # clf2 = SGDClassifier(loss='log') # shuffle=True is useless here
                idxs = list(X_train.index)
                n_iter = 1
                for n in range(n_iter):
                    print("Iteration ", n)
                    random.shuffle(idxs)
                    shuffledX = X_train.loc[X_train.index.isin(idxs)]
                    shuffledY = y_train.loc[y_train.index.isin(idxs)]
                    splits = 20
                    split = int(len(idxs) / splits)
                    idx_subsets = batched(idxs, split)
                    for it, idx_subset in enumerate(idx_subsets):
                        print("Subset ", it)
                        self.model.partial_fit(
                            shuffledX.loc[shuffledX.index.isin(idx_subset)],
                            shuffledY.loc[shuffledY.index.isin(idx_subset)],
                            classes=np.unique(y_train),
                        )
            else:
                self.model.fit(
                    X_train[self.selected_cols][:test_sample_limit],
                    y_train[:test_sample_limit],
                )
            print("after fit")

            if classifier == "SGDClassifier":
                self.params = np.append(
                    self.model.intercept_[0],
                    self.model.coef_[0],
                )
            else:
                self.params = np.append(
                    self.model.named_steps[estimator].intercept_[0],
                    self.model.named_steps[estimator].coef_[0],
                )

            # self.params = np.append(self.model.intercept_[0], self.model.coef_[0])
            print("Checkpoint 0")
            # Calculate matrix of predicted class probabilities.
            # Check resLogit.classes_ to make sure that sklearn ordered your classes as expected
            test_sample_limit = int(1e6) # no limit
            predProbs = self.model.predict_proba(
                X_train[self.selected_cols][:test_sample_limit]
            )
            print("Checkpoint 1")
            # Design matrix -- add column of 1's at the beginning of your X_train matrix
            X_design = np.hstack(
                [
                    np.ones(
                        (X_train[self.selected_cols][:test_sample_limit].shape[0], 1)
                    ),
                    X_train[self.selected_cols][:test_sample_limit],
                ]
            )
            # Initiate matrix of 0's, fill diagonal with each predicted observation's variance
            # V = scipy.sparse.diags(np.product(predProbs, axis=1))
            print("Checkpoint 2")

            V = scipy.sparse.diags(np.prod(predProbs, axis=1))
            # TODO - reduce complexity for larger datasets? random sample?

            # Covariance matrix
            # Note that the @-operater does matrix multiplication in Python 3.5+, so if you're running
            # Python 3.5+, you can replace the covLogit-line below with the more readable:
            covLogit = np.linalg.pinv(X_design.T @ V @ X_design)

            sd_b = np.sqrt(np.diag(covLogit))
            ts_b = self.params / sd_b

            p_values = [
                2 * (1 - stats.t.cdf(np.abs(i), (len(X_design) - len(X_train.columns))))
                for i in ts_b
            ]
            print("Checkpoint 3")

            sd_b = np.round(sd_b, 3)
            ts_b = np.round(ts_b, 3)
            p_values = np.round(p_values, 3)  # includes intercept pvalue
            if classifier == "SGDClassifier":
                coefs = self.model.coef_[0]
            else:
                coefs = self.model.named_steps[estimator].coef_[0]
            # coefs = self.model.coef_[0]
            self.params = np.round(self.params, 4)

            from tabulate import tabulate

            print("Checkpoint 4")

            if show:
                print(
                    tabulate(
                        zip(
                            ["Intercept"] + list(self.selected_cols),
                            (
                                [self.model.intercept_[0]]
                                if classifier == "SGDClassifier"
                                else [self.model.named_steps[estimator].intercept_[0]]
                            )
                            # [self.model.intercept_[0]]
                            + list(coefs),
                            np.sqrt(np.diag(covLogit)),
                            p_values,
                        ),
                        headers=["Estimate", "SE", "Probabilities"],
                    )
                )

            # cols_ls = ["Intercept"] + self.selected_cols.copy()
            cols_ls = self.selected_cols.copy()
            # pvalues excluding intercept
            p_values_ex = p_values[1:]
            pvalues_to_remove = np.where(p_values_ex > p_threshold)[0]
            negative_to_remove = []
            if pos_only:
                negative_to_remove = np.where(coefs < 0)[0]
            if (len(pvalues_to_remove) == 0) & (len(negative_to_remove) == 0):
                stop = True
            else:
                if show:
                    print("----------------------------------------")
                    print("Columns removed at iteration", i)
                updated_cols = self.selected_cols.copy()
                # remove features according to pvalue threshold
                for idx in pvalues_to_remove:
                    col = cols_ls[idx]
                    if show:
                        print(col)
                    if col not in updated_cols:
                        print(col, "not in cols list")
                    else:
                        updated_cols.remove(col)
                # remove features where negative
                if pos_only:
                    for idx in negative_to_remove:
                        col = cols_ls[idx]
                        if show:
                            print(col)
                        if col not in updated_cols:
                            print(col, "not in cols list")
                        else:
                            updated_cols.remove(col)
                self.selected_cols = updated_cols

        self.coefs["Intercept"] = (
            self.model.intercept_[0]
            if classifier == "SGDClassifier"
            else self.model.named_steps[estimator].intercept_[0]
        )
        # self.coefs["Intercept"] = self.model.intercept_[0]

        for coef, col in zip(
            (
                self.model.coef_[0]
                if classifier == "SGDClassifier"
                else self.model.named_steps[estimator].coef_[0]
            ),
            # self.model.coef_[0],
            self.selected_cols,
        ):
            self.coefs[col] = coef
        from tabulate import tabulate

        coef_vis = {
            k: round(v, 3)
            for k, v in sorted(
                self.coefs.items(), key=lambda item: item[1], reverse=True
            )
            if k != "Intercept"
        }
        intercept_vis = round(self.coefs["Intercept"], 3)

        table = zip(
            ["Intercept"] + list(coef_vis.keys()),
            [intercept_vis] + list(coef_vis.values()),
        )
        if show:
            print("\n", tabulate(table, headers=["Feature", "Coefficient"]))
            print()

    def plot_confusion_matrices(self, conf_matrix_train, set: str, save=True):
        fig, ax = plt.subplots(figsize=(7, 5))
        group_counts = [
            "{0:0.0f}".format(value) for value in conf_matrix_train.flatten()
        ]
        group_percentages = [
            "{0:.2%}".format(value)
            for value in conf_matrix_train.flatten() / np.sum(conf_matrix_train)
        ]
        labels = [f"{v2}\n{v3}" for v2, v3 in zip(group_counts, group_percentages)]
        labels = np.asarray(labels).reshape(2, 2)
        ax = sns.heatmap(
            conf_matrix_train,
            annot=labels,
            fmt="",
            cmap=plt.cm.Reds,
            annot_kws={"size": 12},
            ax=ax,
        )
        ax.set_xlabel("\nPredicted", fontsize=18)
        ax.set_ylabel("True", fontsize=18)
        if save:
            self.confusion_matrix[set] = fig
        return

    def predict_risk(self):
        #y_pred = self.model.predict_proba(self.data[self.selected_cols])
        #self.data["Risk"] = y_pred[:, 1]
        
        # split into chunks for large datasets
        self.data["Risk"] = pd.Series()
        datapoint_limit = int(1e7)
        idx_subsets = batched(self.data.index, datapoint_limit)
        for it, idx_subset in enumerate(idx_subsets):
            print("Subset {}".format(it))
            subset = self.data[self.data.index.isin(idx_subset)]
            y_pred = self.model.predict_proba(subset[self.selected_cols])
            self.data.loc[self.data.index.isin(idx_subset),"Risk"] = y_pred[:, 1]
        

    def evaluate_model_performance(
        self,
        evaluate_set: Literal["Train", "Test", "Val"] = "Test",
        show: bool = True,
        recalculate_risk: bool = False,
    ):
        """
        Evaluate model performanve
        Args:
            evaluate_set (Literal) : Evaluate performance for train, test or validation set. Defaults to Test.
            show (bool) : Whether or not to print confusion matrix. Defaults to True.
            recalculate_risk (bool) : Whether or not to recalculate predicted risk before performance evaluation. Defaults to False.
        """
        # TODO - expensive for large datasets - check for existence of Risk column?
        # if implemented, option to force recalculation of risk
        if "Risk" not in self.data.columns or recalculate_risk:
            self.predict_risk()

        # the defaults if no X,columns,y_true specified
        columns = self.selected_cols
        subset = self.data[self.data["Set"] == evaluate_set]
        """if evaluate_set == "Train":
            X,y_true = self.X_train, self.y_train
        elif evaluate_set == "Val":
            X,y_true = self.X_val, self.y_val
        else:
            X,y_true = self.X_test, self.y_test"""
        X, y_true = subset[self.selected_cols], subset[self.target]

        # Probability predictions
        y_pred_prob = self.model.predict_proba(X[columns])[:, 1]

        # Find readmission rate
        readmission = subset["Trigger_Readmission to hospital within 30 days"].mean()

        # find optimal thresholds
        threshold, roc, roc_weighted, gmean, fbeta = find_cutoffs(y_true, y_pred_prob, readmission)

        # Predictions - using train thresholds
        y_pred = [1 if i >= threshold else 0 for i in y_pred_prob]

        # other metrics
        mse = mean_squared_error(y_true, y_pred_prob)
        bal_acc = balanced_accuracy_score(y_true, y_pred)
        acc = accuracy_score(y_true, y_pred)
        av_prec = average_precision_score(y_true, y_pred_prob)
        mean_pred = subset["Risk"].mean()

        metrics = dict(
            zip(
                [
                    "Trigger_Readmission to hospital within 30 days",
                    "ROC",
                    "Gmean",
                    "Balanced accuracy",
                    "Accuracy",
                    "Average precision",
                    "Mean of predictions",
                    "f-beta score"
                ],
                [readmission, roc, gmean, bal_acc, acc, av_prec, mean_pred, fbeta],
            )
        )

        conf_matrix = confusion_matrix(y_true, y_pred)
        self.metrics[evaluate_set] = metrics

        if show:
            self.print_metrics(metrics)
            self.plot_confusion_matrices(conf_matrix, set=evaluate_set)

        return metrics

    def print_metrics(self, metrics):
        print("---------------")
        print("Metrics")
        print("---------------")
        for metric in metrics:
            if metric == "Mortality":
                print(metric, ": ", round(100 * metrics[metric], 2), "%")
            else:
                print(metric, ": ", round(metrics[metric], 4))

    ####

    def plot_model_evaluation(
        self,
        set: Literal["Train", "Validation", "Test", "Test+Validation"] = "Test",
        compass: Literal["Both", "Compass", "NonCompass"] = "Both",
        elective_only: bool = False,
        mode: Literal["preop", "ptl"] = "preop",
        show: bool = True,
    ):
        """
        Plot model evaluation for a given set (train/test/etc) with the option of filtering for Compass only and/or elective only.
        Args:
            set (Literal) : Which set to use (Train, Validation, Test, Test+Validation). Defaults to Test.
            compass (Literal) : Evaluate with Compass/NonCompass/Both procedures. Defaults to Both.
            elective_only (cool) : Evaluate with elective procedures only. Defaults to False.
            mode (Literal) : Whether to apply for preop or ptl model. Defaults to "preop".
            show (bool) : Show confusion matrices. Defaults to True.
        """
        proc = "Procedure"
        if mode == "ptl":
            proc = "PTL Procedure"

        if set == "Test+Validation":
            df = (
                pd.concat(
                    [
                        self.data[self.data["Set"] == "Test"],
                        self.data[self.data["Set"] == "Val"],
                    ]
                ),
            )
        else:
            df = self.data[self.data["Set"] == set]

        if compass == "Compass":
            df = df.loc[df[proc].fillna("NonCompass") != "NonCompass"]

        elif compass == "NonCompass":
            df = df.loc[df[proc].fillna("NonCompass") == "NonCompass"]

        if elective_only:
            df = df.loc[df["IsEmergency"] == 0]

        columns = self.selected_cols
        y_true = df["Mortal"]
        print("{}: ".format(set))
        metrics = self.evaluate_model_performance(
            df, columns, y_true, show=show, compass=compass
        )
        return metrics

    def coefs_df(self):
        coefs = pd.DataFrame.from_dict(data=self.coefs, orient="index")
        coefs.columns = ["Coefficient"]
        coefs.sort_values(by="Coefficient", ascending=False, inplace=True)
        print(coefs)
        