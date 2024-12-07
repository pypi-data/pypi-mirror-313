import hashlib
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Callable

import anomed_utils as utils
import numpy as np


class NumpyDataset(ABC):
    @abstractmethod
    def get(self) -> tuple[np.ndarray, np.ndarray]:
        pass

    def __eq__(self, other) -> bool:
        if isinstance(other, NumpyDataset):
            (X_self, y_self) = self.get()
            (X_other, y_other) = other.get()
            return np.array_equal(X_self, X_other) and np.array_equal(y_self, y_other)
        else:
            return False

    def __repr__(self) -> str:
        (X, y) = self.get()
        return f"NumpyDataset(X={repr(X)}, y={repr(y)})"

    def __str__(self) -> str:
        (X, y) = self.get()
        return f"NumpyDataset(X={str(X)}, y={str(y)})"


class NpzFromDisk(NumpyDataset):
    def __init__(
        self, npz_filepath: str | Path, X_label: str = "X", y_label: str = "y"
    ):
        self._npz_filepath = Path(npz_filepath)
        self._X_label = X_label
        self._y_label = y_label

    def get(self) -> tuple[np.ndarray, np.ndarray]:
        with np.load(self._npz_filepath) as data:
            X = data[self._X_label]
            y = data[self._y_label]
            return (X, y)


class InMemoryNumpyArrays(NumpyDataset):
    def __init__(self, X: np.ndarray, y: np.ndarray):
        self._X = X
        self._y = y

    def get(self):
        return (self._X, self._y)


def discard_targets(data: NumpyDataset) -> InMemoryNumpyArrays:
    (X, _) = data.get()
    return InMemoryNumpyArrays(X, np.array([]))


def _random_partition(
    data: NumpyDataset, first_split_length: float | int = 0.5, seed: int | None = None
) -> tuple[InMemoryNumpyArrays, InMemoryNumpyArrays]:
    (X, y) = data.get()
    n1, n2 = len(X), len(y)
    if n1 != n2:
        raise ValueError(f"Lengths of X ({n1}) and y ({n2}) do not match!")
    if isinstance(first_split_length, float) and 0.0 <= first_split_length <= 1.0:
        desired_length = int(first_split_length * n1)
    elif isinstance(first_split_length, int):
        desired_length = first_split_length
    else:
        raise ValueError(f"Cannot interpret length parameter {first_split_length}.")
    [(X1, X2), (y1, y2)] = utils.random_partitions(
        arrays=[X, y], total_length=n1, desired_length=desired_length, seed=seed
    )
    return (InMemoryNumpyArrays(X1, y1), InMemoryNumpyArrays(X2, y2))


def _create_membership_inference_evaluation_data(
    members: NumpyDataset,
    non_members: NumpyDataset,
    desired_length: int,
    deanonymizer: str,
    anonymizer: str,
) -> tuple[NumpyDataset, np.ndarray]:
    hash_data = anonymizer + deanonymizer
    seed = int(hashlib.sha256(hash_data.encode("utf-8")).hexdigest(), 16)

    # First, reduce the datasets to the desired size
    (members_subset, _) = _random_partition(
        members, first_split_length=desired_length, seed=seed
    )
    (non_members_subset, _) = _random_partition(
        non_members, first_split_length=desired_length, seed=seed
    )

    # Second, go back to Numpy array representation for further processing
    (X_members, y_members) = members_subset.get()
    (X_non_members, y_non_members) = non_members_subset.get()
    X = np.concatenate((X_members, X_non_members))
    y = np.concatenate((y_members, y_non_members))

    members_mask = np.ones(desired_length, dtype=bool)
    nonmembers_mask = np.zeros(desired_length, dtype=bool)
    memberships = np.concatenate((members_mask, nonmembers_mask))

    [X, y, memberships] = utils.shuffles([X, y, memberships], seed=seed)
    return (InMemoryNumpyArrays(X=X, y=y), memberships)


def strict_binary_accuracy(
    prediction: np.ndarray, ground_truth: np.ndarray
) -> dict[str, float]:
    if len(prediction) == 0 or len(ground_truth) == 0:
        raise ValueError(
            "Accuracy is undefined for empty `prediction` or empty `ground_truth`."
        )
    if not prediction.dtype == ground_truth.dtype:
        raise ValueError(
            f"Dtype mismatch of prediction ({prediction.dtype}) and ground_truth "
            f"({ground_truth.dtype})."
        )
    if not prediction.shape == ground_truth.shape:
        raise ValueError(
            f"Shape mismatch of prediction {prediction.shape} and ground_truth "
            f"{ground_truth.shape}"
        )
    matches = 0
    for i in range(len(prediction)):
        if np.array_equal(prediction[i], ground_truth[i]):
            matches += 1
    accuracy = matches / len(prediction)
    return dict(accuracy=accuracy)


def evaluate_membership_inference_attack(
    prediction: np.ndarray, ground_truth: np.ndarray
) -> dict[str, float]:
    try:
        cm = utils.binary_confusion_matrix(prediction, ground_truth)
        tp = cm["tp"]
        n = len(prediction)
        acc = (tp + cm["tn"]) / n
        tpr = tp / (tp + cm["fn"])
        fpr = cm["fp"] / n
        return dict(acc=acc, tpr=tpr, fpr=fpr)
    except ZeroDivisionError:
        raise ValueError(
            "Can't evaluate MIA if `prediction` or `ground_truth` is empty."
        )


def evaluate_MIA(prediction: np.ndarray, ground_truth: np.ndarray) -> dict[str, float]:
    return evaluate_membership_inference_attack(
        prediction=prediction, ground_truth=ground_truth
    )


class SupervisedLearningMIAChallenge:
    def __init__(
        self,
        training_data: NumpyDataset,
        tuning_data: NumpyDataset,
        validation_data: NumpyDataset,
        anonymizer_evaluator: Callable[[np.ndarray, np.ndarray], dict[str, float]],
        MIA_evaluator: Callable[[np.ndarray, np.ndarray], dict[str, float]],
        MIA_evaluation_dataset_length: int = 100,
        seed: int | None = None,
    ):
        self.training_data = training_data
        self.tuning_data = tuning_data
        self.validation_data = validation_data
        self._anonymizer_evaluator = anonymizer_evaluator
        self._MIA_evaluator = MIA_evaluator
        self._members_train: NumpyDataset = None  # type: ignore
        self._members_val: NumpyDataset = None  # type: ignore
        self._non_members_train: NumpyDataset = None  # type: ignore
        self._non_members_val: NumpyDataset = None  # type: ignore
        self.MIA_evaluation_dataset_length = MIA_evaluation_dataset_length
        if seed is None:
            self._seed = np.random.default_rng().integers(low=0, high=2**30)
        else:
            self._seed = seed

    @property
    def members(self) -> NumpyDataset:
        if self._members_train is None:
            self._init_members()
        return self._members_train

    def _init_members(self) -> None:
        (members1, members2) = _random_partition(self.training_data, seed=self._seed)
        self._members_train = members1
        self._members_val = members2

    @property
    def non_members(self) -> NumpyDataset:
        if self._non_members_train is None:
            self._init_non_members()
        return self._non_members_train

    def _init_non_members(self) -> None:
        (non_members1, non_members2) = _random_partition(
            self.validation_data,
            seed=self._seed,
        )
        self._non_members_train = non_members1
        self._non_members_val = non_members2

    def MIA_evaluation_data(
        self, anonymizer: str, deanonymizer: str
    ) -> tuple[NumpyDataset, np.ndarray]:
        if self._members_val is None:
            self._init_members()
        if self._non_members_val is None:
            self._init_non_members()
        return _create_membership_inference_evaluation_data(
            members=self._members_val,
            non_members=self._non_members_val,
            desired_length=self.MIA_evaluation_dataset_length,
            deanonymizer=deanonymizer,
            anonymizer=anonymizer,
        )

    def evaluate_anonymizer(
        self, prediction: np.ndarray, ground_truth: np.ndarray
    ) -> dict[str, float]:
        return self._anonymizer_evaluator(prediction, ground_truth)

    def evaluate_membership_inference_attack(
        self, prediction: np.ndarray, ground_truth: np.ndarray
    ) -> dict[str, float]:
        return self._MIA_evaluator(prediction, ground_truth)
