# (C) Quantum Computing Inc., 2024.
# Import libs
import os
import sys
import time
import datetime
import json
import warnings
from functools import wraps
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF

from eqc_models.ml.classifierbase import ClassifierBase

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        beg_time = time.time()
        val = func(*args, **kwargs)
        end_time = time.time()
        tot_time = end_time - beg_time

        print(
            "Runtime of %s: %0.2f seconds!"
            % (
                func.__name__,
                tot_time,
            )
        )

        return val

    return wrapper

class WeakClassifierDct:
    def __init__(
        self,
        fea_ind_list,
        X_train,
        y_train,
        max_depth=10,
        min_samples_split=100,
    ):
        assert X_train.shape[0] == len(y_train)

        self.fea_ind_list = fea_ind_list
        self.X_train = X_train
        self.y_train = y_train
        self.clf = DecisionTreeClassifier(
            max_depth=max_depth,
            min_samples_split=min_samples_split,
            random_state=0,
        )

    def train(self):
        X_tmp = self.X_train.transpose()[self.fea_ind_list].transpose()

        self.clf.fit(X_tmp, self.y_train)

    def predict(self, X):
        X_tmp = X.transpose()[self.fea_ind_list].transpose()

        return self.clf.predict(X_tmp)


class WeakClassifierNB:
    def __init__(self, fea_ind_list, X_train, y_train):
        assert X_train.shape[0] == len(y_train)

        self.fea_ind_list = fea_ind_list
        self.X_train = X_train
        self.y_train = y_train
        self.clf = GaussianNB()

    def train(self):
        X_tmp = self.X_train.transpose()[self.fea_ind_list].transpose()

        self.clf.fit(X_tmp, self.y_train)

    def predict(self, X):
        X_tmp = X.transpose()[self.fea_ind_list].transpose()

        return self.clf.predict(X_tmp)


class WeakClassifierLG:
    def __init__(self, fea_ind_list, X_train, y_train):
        assert X_train.shape[0] == len(y_train)

        self.fea_ind_list = fea_ind_list
        self.X_train = X_train
        self.y_train = y_train
        self.clf = LogisticRegression(random_state=0)

    def train(self):
        X_tmp = self.X_train.transpose()[self.fea_ind_list].transpose()

        self.clf.fit(X_tmp, self.y_train)

    def predict(self, X):
        X_tmp = X.transpose()[self.fea_ind_list].transpose()

        return self.clf.predict(X_tmp)


class WeakClassifierGP:
    def __init__(self, fea_ind_list, X_train, y_train):
        assert X_train.shape[0] == len(y_train)

        self.fea_ind_list = fea_ind_list
        self.X_train = X_train
        self.y_train = y_train
        self.clf = GaussianProcessClassifier(
            kernel=1.0 * RBF(1.0),
            random_state=0,
        )

    def train(self):
        X_tmp = self.X_train.transpose()[self.fea_ind_list].transpose()

        self.clf.fit(X_tmp, self.y_train)

    def predict(self, X):
        X_tmp = X.transpose()[self.fea_ind_list].transpose()

        return self.clf.predict(X_tmp)


class QBoostClassifier(ClassifierBase):
    """An implementation of QBoost classifier that uses QCi's Dirac-3.

    Parameters
    ----------
    relaxation_schedule: Relaxation schedule used by Dirac-3;
    default: 2.

    num_samples: Number of samples used by Dirac-3; default: 1.

    lambda_coef: A penalty multiplier; default: 0.

    weak_cls_schedule: Weak classifier schedule. Is either 1, 2,
    or 3; default: 2.

    weak_cls_type: Type of weak classifier
        - dct: Decison tree classifier
        - nb: Naive Baysian classifier
        - lg: Logistic regression
        - gp: Gaussian process classifier

    default: dct.

    weak_max_depth: Max depth of the tree. Applied only when
    weak_cls_type="dct". Default: 10.

    weak_min_samples_split: The minimum number of samples required
    to split an internal node. Applied only when
    weak_cls_type="dct". Default: 100.

    Examples
    -----------

    >>> from sklearn import datasets
    >>> from sklearn.preprocessing import MinMaxScaler
    >>> from sklearn.model_selection import train_test_split
    >>> iris = datasets.load_iris()
    >>> X = iris.data
    >>> y = iris.target
    >>> scaler = MinMaxScaler()
    >>> X = scaler.fit_transform(X)
    >>> for i in range(len(y)):
    ...     if y[i] == 0:
    ...         y[i] = -1
    ...     elif y[i] == 2:
    ...         y[i] = 1
    >>> X_train, X_test, y_train, y_test = train_test_split(
    ...     X,
    ...     y,
    ...     test_size=0.2,
    ...     random_state=42,
    ... )
    >>> from eqc_models.ml.classifierqboost import QBoostClassifier
    >>> obj = QBoostClassifier(
    ...     relaxation_schedule=2,
    ...     num_samples=1,
    ...     lambda_coef=0.0,
    ... )
    >>> from contextlib import redirect_stdout
    >>> import io
    >>> f = io.StringIO()
    >>> with redirect_stdout(f):
    ...    obj = obj.fit(X_train, y_train)
    ...    y_train_prd = obj.predict(X_train)
    ...    y_test_prd = obj.predict(X_test)
    """
    def __init__(
        self,
        relaxation_schedule=2,
        num_samples=1,
        lambda_coef=0,
        weak_cls_schedule=2,
        weak_cls_type="lg",
        weak_max_depth=10,
        weak_min_samples_split=100,
    ):
        super(QBoostClassifier).__init__()

        assert weak_cls_schedule in [1, 2, 3]
        assert weak_cls_type in ["dct", "nb", "lg", "gp"]

        self.relaxation_schedule = relaxation_schedule
        self.num_samples = num_samples
        self.lambda_coef = lambda_coef
        self.weak_cls_schedule = weak_cls_schedule
        self.weak_cls_type = weak_cls_type
        self.weak_max_depth = weak_max_depth
        self.weak_min_samples_split = weak_min_samples_split
        self.h_list = []
        self.classes_ = None

    @timer
    def _build_weak_classifiers(self, X, y):
        n_records = X.shape[0]
        n_dims = X.shape[1]

        assert len(y) == n_records

        self.h_list = []

        for l in range(n_dims):
            if self.weak_cls_type == "dct":
                weak_classifier = WeakClassifierDct(
                    [l],
                    X,
                    y,
                    self.weak_max_depth,
                    self.weak_min_samples_split,
                )
            elif self.weak_cls_type == "nb":
                weak_classifier = WeakClassifierNB([l], X, y)
            elif self.weak_cls_type == "lg":
                weak_classifier = WeakClassifierLG([l], X, y)
            elif self.weak_cls_type == "gp":
                weak_classifier = WeakClassifierGP([l], X, y)

            weak_classifier.train()

            self.h_list.append(weak_classifier)

        if self.weak_cls_schedule >= 2:
            for i in range(n_dims):
                for j in range(i + 1, n_dims):
                    if self.weak_cls_type == "dct":
                        weak_classifier = WeakClassifierDct(
                            [i, j],
                            X,
                            y,
                            self.weak_max_depth,
                            self.weak_min_samples_split,
                        )
                    elif self.weak_cls_type == "nb":
                        weak_classifier = WeakClassifierNB([i, j], X, y)
                    elif self.weak_cls_type == "lg":
                        weak_classifier = WeakClassifierLG([i, j], X, y)
                    elif self.weak_cls_type == "gp":
                        weak_classifier = WeakClassifierGP([i, j], X, y)

                    weak_classifier.train()
                    self.h_list.append(weak_classifier)

        if self.weak_cls_schedule >= 3:
            for i in range(n_dims):
                for j in range(i + 1, n_dims):
                    for k in range(j + 1, n_dims):
                        if self.weak_cls_type == "dct":
                            weak_classifier = WeakClassifierDct(
                                [i, j, k],
                                X,
                                y,
                                self.weak_max_depth,
                                self.weak_min_samples_split,
                            )
                        elif self.weak_cls_type == "nb":
                            weak_classifier = WeakClassifierNB(
                                [i, j, k], X, y
                            )
                        elif self.weak_cls_type == "lg":
                            weak_classifier = WeakClassifierLG(
                                [i, j, k], X, y
                            )
                        elif self.weak_cls_type == "gp":
                            weak_classifier = WeakClassifierGP(
                                [i, j, k], X, y
                            )
                        weak_classifier.train()
                        self.h_list.append(weak_classifier)

        return

    def fit(self, X, y):
        """
        Build a QBoost classifier from the training set (X, y).

        Parameters
        ----------
        X : {array-like, sparse matrix} of shape (n_samples, n_features)
        The training input samples.

        y : array-like of shape (n_samples,)
        The target values.

        Returns
        -------
        Response of Dirac-3 in JSON format.
        """

        assert X.shape[0] == y.shape[0], "Inconsistent sizes!"

        assert set(y) == {-1, 1}, "Target values should be in {-1, 1}"

        self.classes_ = set(y)

        J, C, sum_constraint = self.get_hamiltonian(X, y)

        assert J.shape[0] == J.shape[1], "Inconsistent hamiltonian size!"
        assert J.shape[0] == C.shape[0], "Inconsistent hamiltonian size!"

        self.set_model(J, C, sum_constraint)

        sol, response = self.solve()

        assert len(sol) == C.shape[0], "Inconsistent solution size!"

        self.params = self.convert_sol_to_params(sol)

        assert len(self.params) == len(self.h_list), "Inconsistent size!"

        return response

    def predict_raw(self, X: np.array):
        """
        Predict raw output of the classifier for input X.

        Parameters
        ----------
        X : {array-like, sparse matrix} of shape (n_samples, n_features)

        Returns
        -------
        y : ndarray of shape (n_samples,)
        The predicted raw output of the classifier.
        """

        n_records = X.shape[0]
        n_classifiers = len(self.h_list)

        y = np.zeros(shape=(n_records), dtype=np.float32)
        h_vals = np.array(
            [self.h_list[i].predict(X) for i in range(n_classifiers)]
        )

        y = np.tensordot(self.params, h_vals, axes=(0, 0))

        return y

    def predict(self, X: np.array):
        """
        Predict classes for X.

        Parameters
        ----------
        X : {array-like, sparse matrix} of shape (n_samples, n_features)

        Returns
        -------
        y : ndarray of shape (n_samples,)
        The predicted classes.
        """

        y = self.predict_raw(X)
        y = np.sign(y)

        return y

    @timer
    def get_hamiltonian(
        self,
        X: np.array,
        y: np.array,
    ):
        self._build_weak_classifiers(X, y)
        
        print("Built %d weak classifiers!" % len(self.h_list))
        
        n_classifiers = len(self.h_list)
        n_records = X.shape[0]

        J = np.zeros(
            shape=(n_classifiers, n_classifiers), dtype=np.float32
        )
        C = np.zeros(shape=(n_classifiers,), dtype=np.float32)

        h_vals = np.array(
            [self.h_list[i].predict(X) for i in range(n_classifiers)]
        )

        for i in range(n_classifiers):
            for j in range(n_classifiers):
                J[i][j] = sum(h_vals[i] * h_vals[j])
                if i == j:
                    J[i][i] += self.lambda_coef

            C[i] = -2.0 * sum(y * h_vals[i])

        C = C.reshape((n_classifiers, 1))

        return J, C, 1.0

    def convert_sol_to_params(self, sol):
        return np.array(sol)
