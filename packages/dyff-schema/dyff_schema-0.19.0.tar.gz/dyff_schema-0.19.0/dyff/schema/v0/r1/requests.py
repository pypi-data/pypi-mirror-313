# SPDX-FileCopyrightText: 2024 UL Research Institutes
# SPDX-License-Identifier: Apache-2.0
"""The request schemas describe the information that you need to provide when creating
new instances of the core types.

For example, requests do not have
``.id`` fields because these are assigned by the platform when the resource
is created. Similarly, if a resource depends on an instance of another
resource, the request will refer to the dependency by its ID, while the core
resource will include the full dependency object as a sub-resource. The
``create`` endpoints take a request as input and return a full core resource
in response.
"""

from __future__ import annotations

import re
from datetime import datetime
from typing import Optional, Union

import pydantic

from .base import DyffBaseModel
from .platform import (
    AnalysisBase,
    AnalysisScope,
    DatasetBase,
    DataView,
    DocumentationBase,
    EvaluationBase,
    FamilyBase,
    FamilyMembers,
    InferenceServiceBase,
    InferenceSessionBase,
    Labeled,
    MethodBase,
    ModelSpec,
    ModuleBase,
    ReportBase,
)
from .version import SchemaVersion


class DyffRequestDefaultValidators(DyffBaseModel):
    """This must be the base class for *all* request models in the Dyff schema.

    Adds a root validator to ensure that all user-provided datetime fields have a
    timezone set. Timezones will be converted to UTC once the data enters the platform,
    but we allow requests to have non-UTC timezones for user convenience.
    """

    @pydantic.root_validator
    def _require_datetime_timezone_aware(cls, values):
        for k, v in values.items():
            if isinstance(v, datetime):
                if v.tzinfo is None:
                    raise ValueError(f"{cls.__qualname__}.{k}: timezone not set")
        return values


class DyffRequestBase(SchemaVersion, DyffRequestDefaultValidators):
    pass


class DyffEntityCreateRequest(DyffRequestBase):
    account: str = pydantic.Field(description="Account that owns the entity")


class AnalysisCreateRequest(DyffEntityCreateRequest, AnalysisBase):
    """An Analysis transforms Datasets, Evaluations, and Measurements into new
    Measurements or SafetyCases."""

    method: str = pydantic.Field(description="Method ID")

    @pydantic.validator("scope", check_fields=False)
    def _validate_scope(cls, scope: AnalysisScope) -> AnalysisScope:
        # TODO: This has to be a validator function because we can't apply the
        # regex contraint to AnalysisScope, since there are already entities
        # with invalid IDs in the data store. Fix in Schema v1.
        uuid4 = r"^[0-9a-f]{8}[0-9a-f]{4}[4][0-9a-f]{3}[89ab][0-9a-f]{3}[0-9a-f]{12}$"
        id_pattern = re.compile(uuid4)
        if scope.dataset is not None and not re.match(id_pattern, scope.dataset):
            raise ValueError("scope.dataset must be an entity ID")
        if scope.evaluation is not None and not re.match(id_pattern, scope.evaluation):
            raise ValueError("scope.evaluation must be an entity ID")
        if scope.inferenceService is not None and not re.match(
            id_pattern, scope.inferenceService
        ):
            raise ValueError("scope.inferenceService must be an entity ID")
        if scope.model is not None and not re.match(id_pattern, scope.model):
            raise ValueError("scope.model must be an entity ID")
        return scope


class DatasetCreateRequest(DyffEntityCreateRequest, DatasetBase):
    pass


class DocumentationEditRequest(DyffRequestBase, DocumentationBase):
    pass


class InferenceServiceCreateRequest(DyffEntityCreateRequest, InferenceServiceBase):
    model: Optional[str] = pydantic.Field(
        default=None, description="ID of Model backing the service, if applicable"
    )

    # TODO: (DYFF-421) Make .image required and remove this validator
    @pydantic.validator("image", check_fields=False)
    def validate_image_not_none(cls, v):
        if v is None:
            raise ValueError(
                ".image is required for new services; it is defined as Optional"
                " for schema backwards-compatibility only"
            )
        return v


class InferenceSessionCreateRequest(DyffEntityCreateRequest, InferenceSessionBase):
    inferenceService: str = pydantic.Field(description="InferenceService ID")


class InferenceSessionTokenCreateRequest(DyffRequestBase):
    expires: Optional[datetime] = pydantic.Field(
        default=None,
        description="Expiration time of the token. Must be <= expiration time"
        " of session. Default: expiration time of session.",
    )


class EvaluationInferenceSessionRequest(InferenceSessionBase):
    inferenceService: str = pydantic.Field(description="InferenceService ID")


class EvaluationCreateRequest(DyffEntityCreateRequest, EvaluationBase):
    """A description of how to run an InferenceService on a Dataset to obtain a set of
    evaluation results."""

    inferenceSession: Optional[EvaluationInferenceSessionRequest] = pydantic.Field(
        default=None,
        description="Specification of the InferenceSession that will perform inference for the evaluation.",
    )

    inferenceSessionReference: Optional[str] = pydantic.Field(
        default=None,
        description="The ID of a running inference session that will be used"
        " for the evaluation, instead of starting a new one.",
    )

    @pydantic.root_validator
    def check_session_exactly_one(cls, values):
        session = values.get("inferenceSession") is not None
        session_ref = values.get("inferenceSessionReference") is not None
        if not (session ^ session_ref):
            raise ValueError(
                "must specify exactly one of {inferenceSession, inferenceSessionReference}"
            )
        return values


class FamilyCreateRequest(DyffEntityCreateRequest, FamilyBase):
    pass


class MethodCreateRequest(DyffEntityCreateRequest, MethodBase):
    pass


class ModelCreateRequest(DyffEntityCreateRequest, ModelSpec):
    pass


class ModuleCreateRequest(DyffEntityCreateRequest, ModuleBase):
    pass


class ReportCreateRequest(DyffEntityCreateRequest, ReportBase):
    """A Report transforms raw model outputs into some useful statistics.

    .. deprecated:: 0.8.0

        Report functionality has been refactored into the
        Method/Measurement/Analysis apparatus. Creation of new Reports is
        disabled.
    """

    datasetView: Optional[Union[str, DataView]] = pydantic.Field(
        default=None,
        description="View of the input dataset required by the report (e.g., ground-truth labels).",
    )

    evaluationView: Optional[Union[str, DataView]] = pydantic.Field(
        default=None,
        description="View of the evaluation output data required by the report.",
    )


class FamilyMembersEditRequest(DyffRequestBase, FamilyMembers):
    pass


class LabelUpdateRequest(DyffRequestBase, Labeled):
    pass


# Note: Query requests, as they currently exist, don't work with Versioned
# because fastapi will assign None to every field that the client doesn't
# specify. I think it's not that important, because all of the query parameters
# will always be optional. There could be a problem if the semantics of a
# name change, but let's just not do that!
class DyffEntityQueryRequest(DyffRequestDefaultValidators):
    query: Optional[str] = pydantic.Field(
        default=None,
        description="A JSON structure describing a query, encoded as a string."
        " Valid keys are the same as the valid query keys for the corresponding"
        " endpoint. Values can be scalars or lists. Lists are treated as"
        " disjunctive queries (i.e., 'value $in list').",
    )

    id: Optional[str] = pydantic.Field(default=None)
    account: Optional[str] = pydantic.Field(default=None)
    status: Optional[str] = pydantic.Field(default=None)
    reason: Optional[str] = pydantic.Field(default=None)
    labels: Optional[str] = pydantic.Field(
        default=None, description="Labels dict represented as a JSON string."
    )


class DocumentationQueryRequest(DyffRequestDefaultValidators):
    query: Optional[str] = pydantic.Field(
        default=None,
        description="A JSON structure describing a query, encoded as a string."
        " Valid keys are the same as the valid query keys for the corresponding"
        " endpoint. Values can be scalars or lists. Lists are treated as"
        " disjunctive queries (i.e., 'value $in list').",
    )

    id: Optional[str] = pydantic.Field(default=None)


class _AnalysisProductQueryRequest(DyffEntityQueryRequest):
    method: Optional[str] = pydantic.Field(default=None)
    methodName: Optional[str] = pydantic.Field(default=None)
    dataset: Optional[str] = pydantic.Field(default=None)
    evaluation: Optional[str] = pydantic.Field(default=None)
    inferenceService: Optional[str] = pydantic.Field(default=None)
    model: Optional[str] = pydantic.Field(default=None)
    inputs: Optional[str] = pydantic.Field(default=None)


class AuditQueryRequest(DyffEntityQueryRequest):
    name: Optional[str] = pydantic.Field(default=None)


class DatasetQueryRequest(DyffEntityQueryRequest):
    name: Optional[str] = pydantic.Field(default=None)


class EvaluationQueryRequest(DyffEntityQueryRequest):
    dataset: Optional[str] = pydantic.Field(default=None)
    inferenceService: Optional[str] = pydantic.Field(default=None)
    inferenceServiceName: Optional[str] = pydantic.Field(default=None)
    model: Optional[str] = pydantic.Field(default=None)
    modelName: Optional[str] = pydantic.Field(default=None)


class FamilyQueryRequest(DyffEntityQueryRequest):
    pass


class InferenceServiceQueryRequest(DyffEntityQueryRequest):
    name: Optional[str] = pydantic.Field(default=None)
    model: Optional[str] = pydantic.Field(default=None)
    modelName: Optional[str] = pydantic.Field(default=None)


class InferenceSessionQueryRequest(DyffEntityQueryRequest):
    name: Optional[str] = pydantic.Field(default=None)
    inferenceService: Optional[str] = pydantic.Field(default=None)
    inferenceServiceName: Optional[str] = pydantic.Field(default=None)
    model: Optional[str] = pydantic.Field(default=None)
    modelName: Optional[str] = pydantic.Field(default=None)


class MeasurementQueryRequest(_AnalysisProductQueryRequest):
    pass


class MethodQueryRequest(DyffEntityQueryRequest):
    name: Optional[str] = pydantic.Field(default=None)
    outputKind: Optional[str] = pydantic.Field(default=None)


class ModelQueryRequest(DyffEntityQueryRequest):
    name: Optional[str] = pydantic.Field(default=None)


class ModuleQueryRequest(DyffEntityQueryRequest):
    name: Optional[str] = pydantic.Field(default=None)


class ReportQueryRequest(DyffEntityQueryRequest):
    report: Optional[str] = pydantic.Field(default=None)
    dataset: Optional[str] = pydantic.Field(default=None)
    evaluation: Optional[str] = pydantic.Field(default=None)
    inferenceService: Optional[str] = pydantic.Field(default=None)
    model: Optional[str] = pydantic.Field(default=None)


class SafetyCaseQueryRequest(_AnalysisProductQueryRequest):
    pass


class ScoreQueryRequest(DyffRequestDefaultValidators):
    query: Optional[str] = pydantic.Field(
        default=None,
        description="A JSON structure describing a query, encoded as a string."
        " Valid keys are the same as the valid query keys for the corresponding"
        " endpoint. Values can be scalars or lists. Lists are treated as"
        " disjunctive queries (i.e., 'value $in list').",
    )

    id: Optional[str] = pydantic.Field(default=None)
    name: Optional[str] = pydantic.Field(default=None)
    method: Optional[str] = pydantic.Field(default=None)
    methodName: Optional[str] = pydantic.Field(default=None)
    dataset: Optional[str] = pydantic.Field(default=None)
    evaluation: Optional[str] = pydantic.Field(default=None)
    inferenceService: Optional[str] = pydantic.Field(default=None)
    model: Optional[str] = pydantic.Field(default=None)


__all__ = [
    "AnalysisCreateRequest",
    "AuditQueryRequest",
    "DyffEntityCreateRequest",
    "DyffEntityQueryRequest",
    "DyffRequestBase",
    "DyffRequestDefaultValidators",
    "DatasetCreateRequest",
    "DatasetQueryRequest",
    "DocumentationEditRequest",
    "DocumentationQueryRequest",
    "EvaluationCreateRequest",
    "EvaluationQueryRequest",
    "EvaluationInferenceSessionRequest",
    "FamilyCreateRequest",
    "FamilyMembersEditRequest",
    "FamilyQueryRequest",
    "InferenceServiceCreateRequest",
    "InferenceServiceQueryRequest",
    "InferenceSessionCreateRequest",
    "InferenceSessionQueryRequest",
    "InferenceSessionTokenCreateRequest",
    "LabelUpdateRequest",
    "MeasurementQueryRequest",
    "MethodCreateRequest",
    "MethodQueryRequest",
    "ModelCreateRequest",
    "ModelQueryRequest",
    "ModuleCreateRequest",
    "ModuleQueryRequest",
    "ReportCreateRequest",
    "ReportQueryRequest",
    "SafetyCaseQueryRequest",
    "ScoreQueryRequest",
]
