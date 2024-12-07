import tempfile

import numpy as np
import pytest

import anomed_challenge as challenge
from anomed_challenge import InMemoryNumpyArrays, NpzFromDisk, NumpyDataset


@pytest.fixture()
def empty_ndarray() -> np.ndarray:
    return np.array([])


@pytest.fixture()
def ten_elem_ndarray() -> np.ndarray:
    return np.arange(10)


@pytest.fixture()
def boolean_ndarray() -> np.ndarray:
    return np.array(5 * [True, False])


@pytest.fixture()
def two_dim_ndarray() -> np.ndarray:
    arr = np.random.default_rng(42).integers(low=0, high=10, size=(10, 10))
    return arr


@pytest.fixture()
def example_dataset() -> NumpyDataset:
    return InMemoryNumpyArrays(np.arange(10), np.arange(10))


@pytest.fixture()
def example_training_dataset() -> NumpyDataset:
    return InMemoryNumpyArrays(np.arange(0, 70), np.arange(0, 70))


@pytest.fixture()
def example_tuning_dataset() -> NumpyDataset:
    return InMemoryNumpyArrays(np.arange(70, 100), np.arange(70, 100))


@pytest.fixture()
def example_validation_dataset() -> NumpyDataset:
    return InMemoryNumpyArrays(np.arange(100, 120), np.arange(100, 120))


def test_NpzFromDisk(empty_ndarray, ten_elem_ndarray):
    with tempfile.NamedTemporaryFile(mode="w+b") as tmp_file:
        np.savez_compressed(tmp_file, X=empty_ndarray, y=empty_ndarray)
        dataset = NpzFromDisk(tmp_file.name)
        assert _compare_dataset_components(empty_ndarray, empty_ndarray, dataset)
    with tempfile.NamedTemporaryFile(mode="w+b") as tmp_file:
        np.savez_compressed(tmp_file, X=ten_elem_ndarray, y=ten_elem_ndarray)
        dataset = NpzFromDisk(tmp_file.name)
        assert _compare_dataset_components(ten_elem_ndarray, ten_elem_ndarray, dataset)


def _compare_dataset_components(
    X: np.ndarray, y: np.ndarray, dataset: NumpyDataset
) -> bool:
    (X_, y_) = dataset.get()
    return np.array_equal(X, X_) and np.array_equal(y, y_)


def test_InMemoryNumpyArrays(empty_ndarray, ten_elem_ndarray):
    dataset = InMemoryNumpyArrays(empty_ndarray, empty_ndarray)
    assert _compare_dataset_components(empty_ndarray, empty_ndarray, dataset)
    dataset = InMemoryNumpyArrays(ten_elem_ndarray, ten_elem_ndarray)
    assert _compare_dataset_components(ten_elem_ndarray, ten_elem_ndarray, dataset)


def test_discard_targets(example_dataset):
    discarded_dataset = challenge.discard_targets(example_dataset)
    (_, y) = discarded_dataset.get()
    assert len(y) == 0


def test_strict_binary_accuracy(empty_ndarray, ten_elem_ndarray, two_dim_ndarray):
    with pytest.raises(ValueError):
        challenge.strict_binary_accuracy(empty_ndarray, empty_ndarray)

    with pytest.raises(ValueError):
        challenge.strict_binary_accuracy(ten_elem_ndarray, two_dim_ndarray)

    altered_array = two_dim_ndarray.copy()
    for i in range(4):
        altered_array[i, i] = -1
    strict_acc = challenge.strict_binary_accuracy(altered_array, two_dim_ndarray)
    assert strict_acc == dict(accuracy=0.6)


def test_evaluate_MIA(empty_ndarray, boolean_ndarray):
    with pytest.raises(ValueError):
        challenge.evaluate_MIA(empty_ndarray.astype(bool), empty_ndarray.astype(bool))

    with pytest.raises(ValueError):
        challenge.evaluate_MIA(
            boolean_ndarray, np.concatenate([boolean_ndarray, boolean_ndarray])
        )

    altered_array = boolean_ndarray.copy()
    for i in range(5):
        altered_array[i] = True
    MIA_evaluation = challenge.evaluate_MIA(altered_array, boolean_ndarray)
    assert MIA_evaluation == dict(acc=0.8, tpr=1.0, fpr=0.2)


def test_SupervisedLearningMIAChallenge(
    example_training_dataset, example_tuning_dataset, example_validation_dataset
):
    chal = challenge.SupervisedLearningMIAChallenge(
        training_data=example_training_dataset,
        tuning_data=example_tuning_dataset,
        validation_data=example_validation_dataset,
        anonymizer_evaluator=challenge.strict_binary_accuracy,
        MIA_evaluator=challenge.evaluate_MIA,
        MIA_evaluation_dataset_length=5,
    )
    assert _is_subset_dataset(
        chal.members, chal.training_data
    ), "Expected the `members` dataset to be derived from training data."
    assert _is_subset_dataset(
        chal.non_members, chal.validation_data
    ), "Expected the `non_members` dataset to be derived from validation data."
    (mia_eval_dataset, _) = chal.MIA_evaluation_data("a", "b")
    assert _is_subset_dataset(
        mia_eval_dataset, _join_datasets(chal.training_data, chal.validation_data)
    ), "Expected the MIA evaluation data to be derived from both, training and "
    "validation data."
    assert _are_disjoint_datasets(
        mia_eval_dataset, chal.members
    ) and _are_disjoint_datasets(
        mia_eval_dataset, chal.non_members
    ), "Expected the MIA evaluation data to be disjoint from both, the members and "
    "non_members."


def _join_datasets(left: NumpyDataset, right: NumpyDataset) -> InMemoryNumpyArrays:
    (X_left, y_left) = left.get()
    (X_right, y_right) = right.get()
    return InMemoryNumpyArrays(
        X=np.concatenate([X_left, X_right]), y=np.concatenate([y_left, y_right])
    )


def _are_disjoint_datasets(left: NumpyDataset, right: NumpyDataset) -> bool:
    (left_X, left_y) = left.get()
    (right_X, right_y) = right.get()
    return _are_disjoint(left_X, right_X) and _are_disjoint(left_y, right_y)


def _are_disjoint(left: np.ndarray, right: np.ndarray) -> bool:
    no_left_in_right = all([e not in right for e in left])
    no_right_in_left = all([e not in left for e in right])
    return no_left_in_right and no_right_in_left


def _is_subset_dataset(subset: NumpyDataset, superset: NumpyDataset) -> bool:
    (subset_X, subset_y) = subset.get()
    (superset_X, superset_y) = superset.get()
    return _is_subset(subset_X, superset_X) and _is_subset(subset_y, superset_y)


def _is_subset(subset: np.ndarray, superset: np.ndarray) -> bool:
    return all([e in superset for e in subset])
