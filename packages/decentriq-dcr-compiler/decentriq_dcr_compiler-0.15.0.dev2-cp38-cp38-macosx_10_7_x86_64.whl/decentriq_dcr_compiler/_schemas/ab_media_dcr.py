# generated by datamodel-codegen:
#   filename:  ab_media_dcr.json

from __future__ import annotations

from enum import Enum
from typing import Optional, Sequence, Union

from pydantic import BaseModel, ConfigDict, Field, RootModel, conint


class EnclaveSpecificationV0(BaseModel):
    attestationProtoBase64: str
    id: str
    workerProtocol: conint(ge=0)


class FormatType(Enum):
    STRING = 'STRING'
    INTEGER = 'INTEGER'
    FLOAT = 'FLOAT'
    EMAIL = 'EMAIL'
    DATE_ISO8601 = 'DATE_ISO8601'
    PHONE_NUMBER_E164 = 'PHONE_NUMBER_E164'
    HASH_SHA256_HEX = 'HASH_SHA256_HEX'


class HashingAlgorithm(Enum):
    SHA256_HEX = 'SHA256_HEX'


class ModelEvaluationType(Enum):
    ROC_CURVE = 'ROC_CURVE'
    DISTANCE_TO_EMBEDDING = 'DISTANCE_TO_EMBEDDING'
    JACCARD = 'JACCARD'


class Type(Enum):
    SUPPORTED = 'SUPPORTED'


class RequirementFlagValue1(BaseModel):
    type: Type


class Type1(Enum):
    DATASET = 'DATASET'


class RequirementFlagValue2(BaseModel):
    type: Type1


class Type2(Enum):
    PROPERTY = 'PROPERTY'


class RequirementFlagValue3(BaseModel):
    type: Type2
    value: str


class RequirementFlagValue(
    RootModel[
        Union[RequirementFlagValue1, RequirementFlagValue2, RequirementFlagValue3]
    ]
):
    root: Union[RequirementFlagValue1, RequirementFlagValue2, RequirementFlagValue3]


class KnownOrUnknownRequirementFlagValue(RootModel[Optional[RequirementFlagValue]]):
    root: Optional[RequirementFlagValue]


class ModelEvaluationConfig(BaseModel):
    postScopeMerge: Sequence[ModelEvaluationType]
    preScopeMerge: Sequence[ModelEvaluationType]


class RequirementFlag(BaseModel):
    details: KnownOrUnknownRequirementFlagValue
    name: str


class RequirementOp4(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    has: RequirementFlag


class AbMediaComputeV0(BaseModel):
    advertiserEmails: Sequence[str]
    agencyEmails: Sequence[str]
    authenticationRootCertificatePem: str
    dataPartnerEmails: Optional[Sequence[str]] = None
    driverEnclaveSpecification: EnclaveSpecificationV0
    hashMatchingIdWith: Optional[HashingAlgorithm] = None
    id: str
    mainAdvertiserEmail: str
    mainPublisherEmail: str
    matchingIdFormat: FormatType
    modelEvaluation: Optional[ModelEvaluationConfig] = None
    name: str
    observerEmails: Sequence[str]
    publisherEmails: Sequence[str]
    pythonEnclaveSpecification: EnclaveSpecificationV0
    rateLimitPublishDataNumPerWindow: Optional[conint(ge=0)] = 10
    rateLimitPublishDataWindowSeconds: Optional[conint(ge=0)] = 604800


class AbMediaComputeV1(AbMediaComputeV0):
    pass


class AbMediaCompute1(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    v0: AbMediaComputeV0


class AbMediaCompute2(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    v1: AbMediaComputeV1


class AbMediaCompute(RootModel[Union[AbMediaCompute1, AbMediaCompute2]]):
    root: Union[AbMediaCompute1, AbMediaCompute2]


class AbMediaComputeOrUnknown(RootModel[Optional[AbMediaCompute]]):
    root: Optional[AbMediaCompute]


class AbMediaDcr1(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    v0: AbMediaDcrInner


class AbMediaDcr(RootModel[AbMediaDcr1]):
    root: AbMediaDcr1 = Field(..., title='AbMediaDcr')


class AbMediaDcrInner(BaseModel):
    compute: AbMediaComputeOrUnknown
    consumes: ConsumerRequirements
    features: Sequence[str]


class ConsumerRequirements(BaseModel):
    optional: Sequence[RequirementFlag]
    required: Optional[RequirementOp] = None


class RequirementOp1(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    or_: Sequence[RequirementOp] = Field(..., alias='or')


class RequirementOp2(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    and_: Sequence[RequirementOp] = Field(..., alias='and')


class RequirementOp3(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    exclusiveOr: Sequence[RequirementOp]


class RequirementOp(
    RootModel[Union[RequirementOp1, RequirementOp2, RequirementOp3, RequirementOp4]]
):
    root: Union[RequirementOp1, RequirementOp2, RequirementOp3, RequirementOp4] = Field(
        ...,
        description='An expression that can be used to check whether a data lab (as a "data provider") provides certain datasets or certain data properties. This was introduced because the system used in the LM DCR didn\'t allow the MediaInsights DCR to express that _either_ a segments or an embeddings dataset is required in case it was configured to enable lookalike modelling.',
    )


AbMediaDcr1.model_rebuild()
AbMediaDcrInner.model_rebuild()
ConsumerRequirements.model_rebuild()
RequirementOp1.model_rebuild()
RequirementOp2.model_rebuild()
RequirementOp3.model_rebuild()
