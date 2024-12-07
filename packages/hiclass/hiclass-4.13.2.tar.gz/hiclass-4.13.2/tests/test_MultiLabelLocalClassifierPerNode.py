import logging

import networkx as nx
import numpy as np
import pytest
from numpy.testing import assert_array_equal
from scipy.sparse import csr_matrix
from sklearn.exceptions import NotFittedError
from sklearn.linear_model import LogisticRegression
from sklearn.utils.estimator_checks import parametrize_with_checks
from sklearn.utils.validation import check_is_fitted

from hiclass.MultiLabelLocalClassifierPerNode import MultiLabelLocalClassifierPerNode
from hiclass.BinaryPolicy import ExclusivePolicy
from hiclass.ConstantClassifier import ConstantClassifier
import sklearn.utils.validation
import functools


@parametrize_with_checks([MultiLabelLocalClassifierPerNode()])
def test_sklearn_compatible_estimator(estimator, check):
    check(estimator)


@pytest.fixture
def digraph_with_policy():
    digraph = MultiLabelLocalClassifierPerNode(binary_policy="exclusive")
    digraph.hierarchy_ = nx.DiGraph([("a", "b")])
    digraph.X_ = np.array([1, 2])
    digraph.y_ = np.array([[["a", "b"]]])
    digraph.logger_ = logging.getLogger("LCPN")
    digraph.sample_weight_ = None
    return digraph


def test_initialize_binary_policy(digraph_with_policy):
    digraph_with_policy._initialize_binary_policy()
    assert isinstance(digraph_with_policy.binary_policy_, ExclusivePolicy)


@pytest.fixture
def digraph_with_unknown_policy():
    digraph = MultiLabelLocalClassifierPerNode(binary_policy="unknown")
    digraph.hierarchy_ = nx.DiGraph([("a", "b")])
    digraph.y_ = np.array([[["a", "b"]]])
    digraph.logger_ = logging.getLogger("LCPN")
    return digraph


def test_initialize_unknown_binary_policy(digraph_with_unknown_policy):
    with pytest.raises(KeyError):
        digraph_with_unknown_policy._initialize_binary_policy()


@pytest.fixture
def digraph_with_object_policy():
    digraph = MultiLabelLocalClassifierPerNode(binary_policy=ExclusivePolicy)
    digraph.hierarchy_ = nx.DiGraph([("a", "b")])
    digraph.y_ = np.array([[["a", "b"]]])
    digraph.logger_ = logging.getLogger("LCPN")
    return digraph


def test_initialize_object_binary_policy(digraph_with_object_policy):
    with pytest.raises(ValueError):
        digraph_with_object_policy._initialize_binary_policy()


@pytest.fixture
def digraph_logistic_regression():
    digraph = MultiLabelLocalClassifierPerNode(local_classifier=LogisticRegression())
    digraph.hierarchy_ = nx.DiGraph([("a", "b"), ("a", "c")])
    digraph.y_ = np.array(
        [[["a", "b"], ["", ""]], [["a", "c"], ["", ""]], [["a", "b"], ["a", "c"]]]
    )
    digraph.X_ = np.array([[1, 2], [3, 4], [5, 6]])
    digraph.logger_ = logging.getLogger("LCPN")
    digraph.root_ = "a"
    digraph.separator_ = "::HiClass::Separator::"
    digraph.binary_policy_ = ExclusivePolicy(digraph.hierarchy_, digraph.X_, digraph.y_)
    digraph.sample_weight_ = None
    return digraph


def test_initialize_local_classifiers(digraph_logistic_regression):
    digraph_logistic_regression._initialize_local_classifiers()
    for node in digraph_logistic_regression.hierarchy_.nodes:
        if node != digraph_logistic_regression.root_:
            assert isinstance(
                digraph_logistic_regression.hierarchy_.nodes[node]["classifier"],
                LogisticRegression,
            )
        else:
            with pytest.raises(KeyError):
                isinstance(
                    digraph_logistic_regression.hierarchy_.nodes[node]["classifier"],
                    LogisticRegression,
                )


@pytest.mark.parametrize("n_jobs", [1, 2])
def test_fit_digraph(digraph_logistic_regression, n_jobs):
    classifiers = {
        "b": {"classifier": LogisticRegression()},
        "c": {"classifier": LogisticRegression()},
    }
    digraph_logistic_regression.n_jobs = n_jobs
    nx.set_node_attributes(digraph_logistic_regression.hierarchy_, classifiers)
    digraph_logistic_regression._fit_digraph(local_mode=True)
    with pytest.raises(KeyError):
        check_is_fitted(digraph_logistic_regression.hierarchy_.nodes["a"]["classifier"])
    for node in ["b", "c"]:
        try:
            check_is_fitted(
                digraph_logistic_regression.hierarchy_.nodes[node]["classifier"]
            )
        except NotFittedError as e:
            pytest.fail(repr(e))
    assert 1


def test_fit_digraph_joblib_multiprocessing(digraph_logistic_regression):
    classifiers = {
        "b": {"classifier": LogisticRegression()},
        "c": {"classifier": LogisticRegression()},
    }
    digraph_logistic_regression.n_jobs = 2
    nx.set_node_attributes(digraph_logistic_regression.hierarchy_, classifiers)
    digraph_logistic_regression._fit_digraph(local_mode=True, use_joblib=True)
    with pytest.raises(KeyError):
        check_is_fitted(digraph_logistic_regression.hierarchy_.nodes["a"]["classifier"])
    for node in ["b", "c"]:
        try:
            check_is_fitted(
                digraph_logistic_regression.hierarchy_.nodes[node]["classifier"]
            )
        except NotFittedError as e:
            pytest.fail(repr(e))
    assert 1


def test_fit_1_label():
    # test that predict removes multilabel dimension in case of 1 label
    lcpn = MultiLabelLocalClassifierPerNode(
        local_classifier=LogisticRegression(), n_jobs=2
    )
    y = np.array([[["1", "2"]]])
    X = np.array([[1, 2]])
    ground_truth = np.array(
        [[["1", "2"]]]
    )  # TODO: decide if dimension should be removed
    lcpn.fit(X, y)
    prediction = lcpn.predict(X)
    assert_array_equal(ground_truth, prediction)


def test_clean_up(digraph_logistic_regression):
    digraph_logistic_regression._clean_up()
    with pytest.raises(AttributeError):
        assert digraph_logistic_regression.X_ is None
    with pytest.raises(AttributeError):
        assert digraph_logistic_regression.y_ is None
    with pytest.raises(AttributeError):
        assert digraph_logistic_regression.binary_policy_ is None


@pytest.fixture
def fitted_logistic_regression():
    digraph = MultiLabelLocalClassifierPerNode(local_classifier=LogisticRegression())
    digraph.hierarchy_ = nx.DiGraph(
        [("r", "1"), ("r", "2"), ("1", "1.1"), ("1", "1.2"), ("2", "2.1"), ("2", "2.2")]
    )
    digraph.X_ = np.array([[1, -1], [1, 1], [2, -1], [2, 1], [1, 0]])
    digraph.y_ = [
        [["1", "1.1"]],
        [["1", "1.2"]],
        [["2", "2.1"]],
        [["2", "2.2"]],
        [["1", "1.1"], ["1", "1.2"]],
    ]

    digraph.logger_ = logging.getLogger("LCPN")
    digraph.max_levels_ = 2
    digraph.dtype_ = "<U3"
    digraph.root_ = "r"
    digraph.separator_ = "::HiClass::Separator::"
    digraph.max_multi_labels_ = 2
    classifiers = {
        "1": {"classifier": LogisticRegression()},
        "1.1": {"classifier": LogisticRegression()},
        "1.2": {"classifier": LogisticRegression()},
        "2": {"classifier": LogisticRegression()},
        "2.1": {"classifier": LogisticRegression()},
        "2.2": {"classifier": LogisticRegression()},
    }
    # TODO: is selection of labels for trainnig correct with respect to binary policy?
    classifiers["1"]["classifier"].fit(digraph.X_, [1, 1, 0, 0, 1])
    classifiers["1.1"]["classifier"].fit(digraph.X_, [1, 0, 0, 0, 1])
    classifiers["1.2"]["classifier"].fit(digraph.X_, [0, 1, 0, 0, 1])
    classifiers["2"]["classifier"].fit(digraph.X_, [0, 0, 1, 1, 0])
    classifiers["2.1"]["classifier"].fit(digraph.X_, [0, 0, 1, 0, 0])
    classifiers["2.2"]["classifier"].fit(digraph.X_, [0, 0, 0, 1, 0])
    nx.set_node_attributes(digraph.hierarchy_, classifiers)
    return digraph


def test_predict_no_tolerance(fitted_logistic_regression):
    ground_truth = np.array(
        [
            [["1", "1.1"], ["", ""]],
            [["1", "1.2"], ["", ""]],
            [["2", "2.1"], ["", ""]],
            [["2", "2.2"], ["", ""]],
            [["1", "1.1"], ["1", "1.2"]],
        ]
    )
    X = np.array(
        [[1, -1], [1, 1], [2, -1], [2, 1], [1, 0]]
    )  # same as fitted_logistic_regression.X_
    prediction = fitted_logistic_regression.predict(X)
    assert_array_equal(ground_truth, prediction)


@pytest.mark.parametrize(
    "tolerance,expected", [(None, [["1", "1.2"]]), (0.1, [["1", "1.1"], ["1", "1.2"]])]
)
def test_predict_tolerance(fitted_logistic_regression, tolerance, expected):
    # test that depending on tolerance set predicts multilabels or not
    ground_truth = np.array([expected])
    X = np.array([[1, 0.01]])
    prediction = fitted_logistic_regression.predict(X, tolerance)
    assert_array_equal(ground_truth, prediction)


def test_predict_sparse(fitted_logistic_regression):
    ground_truth = np.array(
        [
            [["1", "1.1"], ["", ""]],
            [["1", "1.2"], ["", ""]],
            [["2", "2.1"], ["", ""]],
            [["2", "2.2"], ["", ""]],
            [["1", "1.1"], ["1", "1.2"]],
        ]
    )
    prediction = fitted_logistic_regression.predict(
        csr_matrix([[1, -1], [1, 1], [2, -1], [2, 1], [1, 0]])
    )
    assert_array_equal(ground_truth, prediction)


def test_fit_predict():
    lcpn = MultiLabelLocalClassifierPerNode(local_classifier=LogisticRegression())
    x = np.array([[1, 2], [3, 4]])
    y = np.array([[["a", "c"], ["b", "c"]], [["a", "c"], ["b", "c"]]])
    lcpn.fit(x, y)
    predictions = lcpn.predict(x)
    assert_array_equal(y, predictions)


def test_fit_predict_deep():
    lcpn = MultiLabelLocalClassifierPerNode(
        local_classifier=LogisticRegression(), tolerance=0.1
    )
    x = np.array(
        [
            [1, 1, -1],
            [1, 1, 1],
        ]
    )
    y = np.array(
        [
            [
                ["1", "1.1", "1.1.1"],
                ["1", "1.1", "1.1.2"],
                ["1", "1.2", "1.2.1"],
                ["1", "1.2", "1.2.2"],
            ],
            [
                ["1", "1.1", "1.1.1"],
                ["1", "1.1", "1.1.2"],
                ["1", "1.2", "1.2.1"],
                ["1", "1.2", "1.2.2"],
            ],
        ]
    )
    lcpn.fit(x, y)
    predictions = lcpn.predict(x)
    assert_array_equal(y, predictions)


@pytest.fixture
def empty_levels():
    X = [
        [1],
        [2],
        [3],
    ]
    y = [
        [["1", "", ""]],
        [["2", "2.1", ""]],
        [["3", "3.1", "3.1.2"]],
    ]
    return X, y


def test_empty_levels(empty_levels):
    lcpn = MultiLabelLocalClassifierPerNode()
    X, y = empty_levels
    lcpn.fit(X, y)
    predictions = lcpn.predict(X)
    ground_truth = [
        [["1", "", ""]],
        [["2", "2.1", ""]],
        [["3", "3.1", "3.1.2"]],
    ]
    assert list(lcpn.hierarchy_.nodes) == [
        "1",
        "2",
        "2" + lcpn.separator_ + "2.1",
        "3",
        "3" + lcpn.separator_ + "3.1",
        "3" + lcpn.separator_ + "3.1" + lcpn.separator_ + "3.1.2",
        lcpn.root_,
    ]
    assert_array_equal(ground_truth, predictions)


def test_fit_unique_class():
    lcpn = MultiLabelLocalClassifierPerNode(
        local_classifier=LogisticRegression(), n_jobs=1
    )
    y = np.array([[["1"]], [["1"]]])
    X = np.array([[1], [2]])

    lcpn.fit(X, y)
    prediction = lcpn.predict(X)
    assert_array_equal(y, prediction)


def test_fit_bert():
    bert = ConstantClassifier()
    lcpn = MultiLabelLocalClassifierPerNode(
        local_classifier=bert,
        bert=True,
    )
    X = ["Text 1", "Text 2"]
    y = np.array(
        [
            [["a"]],
            [["a"]],
        ]
    )
    lcpn.fit(X, y)
    check_is_fitted(lcpn)

    predictions = lcpn.predict(X)
    assert_array_equal(y, predictions)
