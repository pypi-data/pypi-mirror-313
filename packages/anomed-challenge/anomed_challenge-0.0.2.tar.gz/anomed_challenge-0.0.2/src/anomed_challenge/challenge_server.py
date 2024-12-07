import json
from typing import Any, Callable

import anomed_utils as utils
import falcon
import numpy as np

from . import challenge
from .challenge import NumpyDataset


class StaticJSONResource:
    """Any JSON serializable and static content. Will be displayed as plain text
    JSON string."""

    def __init__(self, obj: dict[str, Any]):
        self._obj = obj

    def on_get(self, _, resp: falcon.Response):
        resp.text = json.dumps(self._obj)


class StaticNumpyDataResource:
    """A static NumPy dataset (byte stream)."""

    def __init__(self, data: NumpyDataset) -> None:
        self.data = data

    def on_get(self, _, resp: falcon.Response) -> None:
        _add_ds_to_resp(self.data, resp)


def _add_ds_to_resp(ds: NumpyDataset, resp: falcon.Response) -> None:
    (X, y) = ds.get()
    arrays = dict(X=X, y=y)
    resp.data = utils.named_ndarrays_to_bytes(arrays)


class DynamicNumpyDataResource:
    """A dynamic NumPy dataset (byte stream), i.e. the specific dataset content
    depends on request parameters."""

    def __init__(
        self, individual_data_provider: Callable[[dict[str, str]], NumpyDataset]
    ) -> None:
        self._individual_data_provider = individual_data_provider

    def on_get(self, _, resp: falcon.Response, **request_path_parameters: str) -> None:
        individualized_data = self._individual_data_provider(request_path_parameters)
        _add_ds_to_resp(individualized_data, resp)


class UtilityResource:
    def __init__(
        self,
        query_param_extractor: Callable[[falcon.Request], dict[str, Any]],
        target_data_provider: Callable[[dict[str, Any]], np.ndarray],
        evaluator: Callable[[np.ndarray, np.ndarray], dict[str, float]],
        submitter: Callable[[dict[str, float]], None],
    ) -> None:
        self._evaluation_data_provider = target_data_provider
        self._evaluator = evaluator
        self._query_param_extractor = query_param_extractor
        self._submitter = submitter

    def on_post(self, req: falcon.Request, resp: falcon.Response) -> None:
        request_params = self._query_param_extractor(req)
        try:
            array_payload = utils.bytes_to_named_ndarrays(req.bounded_stream.read())
            self._validate_array_payload(array_payload)
            prediction = array_payload["prediction"]
            y = self._evaluation_data_provider(request_params)
            evaluation = self._evaluator(prediction, y)
            self._submitter(evaluation)
            resp.text = json.dumps(evaluation)
            resp.status_code = 201
        except (KeyError, ValueError):
            raise falcon.HTTPBadRequest(
                title="Malformed request.",
                description="Expected a NumPy array with name 'prediction'.",
            )

    def _validate_array_payload(self, array_payload: dict[str, np.ndarray]) -> None:
        if "prediction" not in array_payload:
            raise KeyError("'prediction'")


def supervised_learning_MIA_challenge_server_factory(
    challenge_obj: challenge.SupervisedLearningMIAChallenge,
) -> falcon.App:
    app = falcon.App()
    app.add_route("/", StaticJSONResource(dict(message="Challenge server is alive!")))
    app.add_route(
        "/data/anonymizer/training",
        StaticNumpyDataResource(challenge_obj.training_data),
    )
    app.add_route(
        "/data/anonymizer/tuning",
        StaticNumpyDataResource(challenge_obj.tuning_data),
    )
    app.add_route(
        "/data/anonymizer/validation",
        StaticNumpyDataResource(
            challenge.discard_targets(challenge_obj.validation_data)
        ),
    )
    app.add_route(
        "/data/deanonymizer/members", StaticNumpyDataResource(challenge_obj.members)
    )

    app.add_route(
        r"/data/deanonymizer/non-members",
        StaticNumpyDataResource(challenge_obj.non_members),
    )
    app.add_route(
        r"/data/attack-success-evaluation/{deanonymizer}/{anonymizer}",
        DynamicNumpyDataResource(
            lambda rpps: challenge_obj.MIA_evaluation_data(
                anonymizer=rpps["anonymizer"], deanonymizer=rpps["deanonymizer"]
            )[0]
        ),
    )
    app.add_route(
        "/utility/anonymizer",
        UtilityResource(
            query_param_extractor=lambda req: dict(
                anonymizer=req.get_param("anonymizer", required=True)
            ),
            target_data_provider=lambda _: challenge_obj.validation_data.get()[1],
            evaluator=challenge_obj.evaluate_anonymizer,
            # TODO: Submission of evaluation to platform is still missing
            submitter=lambda _: None,
        ),
    )
    app.add_route(
        "/utility/deanonymizer",
        UtilityResource(
            query_param_extractor=lambda req: dict(
                anonymizer=req.get_param("anonymizer", required=True),
                deanonymizer=req.get_param("deanonymizer", required=True),
            ),
            target_data_provider=lambda params: challenge_obj.MIA_evaluation_data(
                anonymizer=params["anonymizer"], deanonymizer=params["deanonymizer"]
            )[1],
            evaluator=challenge_obj.evaluate_membership_inference_attack,
            # TODO: Submission of evaluation to platform is still missing
            submitter=lambda _: None,
        ),
    )
    return app
