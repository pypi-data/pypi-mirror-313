# generated by datamodel-codegen:
#   filename:  data_science_commit.json

from __future__ import annotations

from enum import Enum
from typing import Optional, Sequence, Union

from pydantic import BaseModel, ConfigDict, Field, RootModel, conint


class AwsConfig(BaseModel):
    bucket: str
    objectKey: Optional[str] = None
    region: str


class ColumnDataType(Enum):
    integer = 'integer'
    float = 'float'
    string = 'string'


class ColumnTuple(BaseModel):
    columns: Sequence[conint(ge=0)]


class CredentialsDependencyV91(Enum):
    splickyDsp = 'splickyDsp'


class CredentialsDependencyV92(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    user: str


class CredentialsDependencyV9(
    RootModel[Union[CredentialsDependencyV91, CredentialsDependencyV92]]
):
    root: Union[CredentialsDependencyV91, CredentialsDependencyV92]


class DatasetSinkEncryptionKeyDependency(BaseModel):
    dependency: str
    isKeyHexEncoded: bool


class EnclaveSpecification(BaseModel):
    attestationProtoBase64: str
    id: str
    workerProtocol: conint(ge=0)


class ExportConnectorKind1(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    aws: AwsConfig


class ExportConnectorKind(RootModel[ExportConnectorKind1]):
    root: ExportConnectorKind1


class ExportType1(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    raw: Sequence = Field(..., max_length=0, min_length=0)


class ExportType2(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    zipSingleFile: str


class ExportType3(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    zipAllFiles: Sequence = Field(..., max_length=0, min_length=0)


class ExportType(RootModel[Union[ExportType1, ExportType2, ExportType3]]):
    root: Union[ExportType1, ExportType2, ExportType3]


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


class ImportConnectorKind1(ExportConnectorKind1):
    pass


class ImportConnectorKind(RootModel[ImportConnectorKind1]):
    root: ImportConnectorKind1


class ImportConnectorNode(BaseModel):
    credentialsDependency: str
    kind: ImportConnectorKind
    specificationId: str


class InputDataType1(ExportType1):
    pass


class MaskType(Enum):
    genericString = 'genericString'
    genericNumber = 'genericNumber'
    name = 'name'
    address = 'address'
    postcode = 'postcode'
    phoneNumber = 'phoneNumber'
    socialSecurityNumber = 'socialSecurityNumber'
    email = 'email'
    date = 'date'
    timestamp = 'timestamp'
    iban = 'iban'


class MatchingComputationNode(BaseModel):
    config: str
    dependencies: Sequence[str]
    enableLogsOnError: bool
    enableLogsOnSuccess: bool
    output: str
    specificationId: str
    staticContentSpecificationId: str


class NumRowsValidationRule(BaseModel):
    atLeast: Optional[conint(ge=0)] = None
    atMost: Optional[conint(ge=0)] = None


class NumericRangeRule(BaseModel):
    greaterThan: Optional[float] = None
    greaterThanEquals: Optional[float] = None
    lessThan: Optional[float] = None
    lessThanEquals: Optional[float] = None


class PostComputationNode(BaseModel):
    dependency: str
    specificationId: str
    useMockBackend: bool


class PreviewComputationNode(BaseModel):
    dependency: str
    quotaBytes: conint(ge=0)


class PythonEnvironmentComputationNode(BaseModel):
    extraChunkCacheSizeToAvailableMemoryRatio: Optional[float] = None
    minimumContainerMemorySize: Optional[conint(ge=0)] = None
    requirementsTxtContent: str
    scriptingSpecificationId: str
    staticContentSpecificationId: str


class PythonOptions(BaseModel):
    customVirtualEnvironmentId: Optional[str] = None


class RawLeafNode(BaseModel):
    pass


class S3Provider(Enum):
    Aws = 'Aws'
    Gcs = 'Gcs'


class S3SinkComputationNode(BaseModel):
    credentialsDependencyId: str
    endpoint: str
    region: Optional[str] = ''
    s3Provider: Optional[S3Provider] = 'Aws'
    specificationId: str
    uploadDependencyId: str


class Script(BaseModel):
    content: str
    name: str


class ScriptingLanguage(Enum):
    python = 'python'
    r = 'r'


class ScriptingLanguageV91(Enum):
    r = 'r'


class ScriptingLanguageV92(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    python: PythonOptions


class ScriptingLanguageV9(RootModel[Union[ScriptingLanguageV91, ScriptingLanguageV92]]):
    root: Union[ScriptingLanguageV91, ScriptingLanguageV92]


class SqlNodePrivacyFilter(BaseModel):
    minimumRowsCount: int


class TableMapping(BaseModel):
    nodeId: str
    tableName: str


class UniquenessValidationRule(BaseModel):
    uniqueKeys: Sequence[ColumnTuple]


class ZipInputDataType1(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    all: Sequence = Field(..., max_length=0, min_length=0)


class ZipInputDataType2(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    files: Sequence[str]


class ZipInputDataType(RootModel[Union[ZipInputDataType1, ZipInputDataType2]]):
    root: Union[ZipInputDataType1, ZipInputDataType2]


class ColumnDataFormat(BaseModel):
    dataType: ColumnDataType
    isNullable: bool


class ColumnValidationV0(BaseModel):
    allowNull: bool
    formatType: FormatType
    hashWith: Optional[HashingAlgorithm] = None
    inRange: Optional[NumericRangeRule] = None
    name: Optional[str] = None


class ComputationNodeKind4(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    s3Sink: S3SinkComputationNode


class ComputationNodeKind5(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    match: MatchingComputationNode


class ComputationNodeKindV25(ComputationNodeKind4):
    pass


class ComputationNodeKindV26(ComputationNodeKind5):
    pass


class ComputationNodeKindV27(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    post: PostComputationNode


class ComputationNodeKindV65(ComputationNodeKind4):
    pass


class ComputationNodeKindV66(ComputationNodeKind5):
    pass


class ComputationNodeKindV67(ComputationNodeKindV27):
    pass


class ComputationNodeKindV68(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    preview: PreviewComputationNode


class ComputationNodeKindV69(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    importConnector: ImportConnectorNode


class ComputationNodeKindV95(ComputationNodeKind4):
    pass


class ComputationNodeKindV96(ComputationNodeKind5):
    pass


class ComputationNodeKindV97(ComputationNodeKindV27):
    pass


class ComputationNodeKindV98(ComputationNodeKindV68):
    pass


class ComputationNodeKindV99(ComputationNodeKindV69):
    pass


class EnvironmentComputationNodeKind1(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    python: PythonEnvironmentComputationNode


class EnvironmentComputationNodeKind(RootModel[EnvironmentComputationNodeKind1]):
    root: EnvironmentComputationNodeKind1


class ExportNodeDependency(BaseModel):
    exportType: ExportType
    name: str


class InputDataType2(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    zip: ZipInputDataType


class InputDataType(RootModel[Union[InputDataType1, InputDataType2]]):
    root: Union[InputDataType1, InputDataType2]


class LeafNodeKind1(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    raw: RawLeafNode


class LeafNodeKindV21(LeafNodeKind1):
    pass


class ScriptingComputationNode(BaseModel):
    additionalScripts: Sequence[Script]
    dependencies: Sequence[str]
    enableLogsOnError: bool
    enableLogsOnSuccess: bool
    extraChunkCacheSizeToAvailableMemoryRatio: Optional[float] = None
    mainScript: Script
    minimumContainerMemorySize: Optional[conint(ge=0)] = None
    output: str
    scriptingLanguage: ScriptingLanguage
    scriptingSpecificationId: str
    staticContentSpecificationId: str


class ScriptingComputationNodeV9(BaseModel):
    additionalScripts: Sequence[Script]
    dependencies: Sequence[str]
    enableLogsOnError: bool
    enableLogsOnSuccess: bool
    extraChunkCacheSizeToAvailableMemoryRatio: Optional[float] = None
    mainScript: Script
    minimumContainerMemorySize: Optional[conint(ge=0)] = None
    output: str
    scriptingLanguage: ScriptingLanguageV9
    scriptingSpecificationId: str
    staticContentSpecificationId: str


class SqlComputationNode(BaseModel):
    dependencies: Sequence[TableMapping]
    privacyFilter: Optional[SqlNodePrivacyFilter] = None
    specificationId: str
    statement: str


class SqliteComputationNode(BaseModel):
    dependencies: Sequence[TableMapping]
    enableLogsOnError: bool
    enableLogsOnSuccess: bool
    sqliteSpecificationId: str
    statement: str
    staticContentSpecificationId: str


class SyntheticNodeColumn(BaseModel):
    dataFormat: ColumnDataFormat
    index: int
    maskType: MaskType
    name: Optional[str] = None
    shouldMaskColumn: bool


class TableLeafNodeColumn(BaseModel):
    dataFormat: ColumnDataFormat
    name: str


class TableLeafNodeColumnV2(BaseModel):
    dataFormat: ColumnDataFormat
    name: str
    validation: ColumnValidationV0


class TableValidationV0(BaseModel):
    allowEmpty: Optional[bool] = None
    numRows: Optional[NumRowsValidationRule] = None
    uniqueness: Optional[UniquenessValidationRule] = None


class ValidationNodeV2(BaseModel):
    pythonSpecificationId: str
    staticContentSpecificationId: str
    validation: TableValidationV0


class ComputationNodeKind1(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    sql: SqlComputationNode


class ComputationNodeKind2(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    scripting: ScriptingComputationNode


class ComputationNodeKindV21(ComputationNodeKind1):
    pass


class ComputationNodeKindV22(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    sqlite: SqliteComputationNode


class ComputationNodeKindV23(ComputationNodeKind2):
    pass


class ComputationNodeKindV61(ComputationNodeKind1):
    pass


class ComputationNodeKindV62(ComputationNodeKindV22):
    pass


class ComputationNodeKindV63(ComputationNodeKind2):
    pass


class ComputationNodeKindV91(ComputationNodeKind1):
    pass


class ComputationNodeKindV92(ComputationNodeKindV22):
    pass


class ComputationNodeKindV93(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    scripting: ScriptingComputationNodeV9


class DatasetSinkInput(BaseModel):
    datasetName: str
    dependency: str
    inputDataType: InputDataType


class EnvironmentComputationNode(BaseModel):
    kind: EnvironmentComputationNodeKind


class ExportConnectorNode(BaseModel):
    credentialsDependency: str
    dependency: ExportNodeDependency
    kind: ExportConnectorKind
    specificationId: str


class ExportConnectorNodeV9(BaseModel):
    credentialsDependency: CredentialsDependencyV9
    dependency: ExportNodeDependency
    kind: ExportConnectorKind
    specificationId: str


class SyntheticDataComputationNode(BaseModel):
    columns: Sequence[SyntheticNodeColumn]
    dependency: str
    enableLogsOnError: bool
    enableLogsOnSuccess: bool
    epsilon: float
    outputOriginalDataStatistics: bool
    staticContentSpecificationId: str
    synthSpecificationId: str


class TableLeafNode(BaseModel):
    columns: Sequence[TableLeafNodeColumn]
    sqlSpecificationId: str


class TableLeafNodeV2(BaseModel):
    columns: Sequence[TableLeafNodeColumnV2]
    validationNode: ValidationNodeV2


class ComputationNodeKind3(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    syntheticData: SyntheticDataComputationNode


class ComputationNodeKind(
    RootModel[
        Union[
            ComputationNodeKind1,
            ComputationNodeKind2,
            ComputationNodeKind3,
            ComputationNodeKind4,
            ComputationNodeKind5,
        ]
    ]
):
    root: Union[
        ComputationNodeKind1,
        ComputationNodeKind2,
        ComputationNodeKind3,
        ComputationNodeKind4,
        ComputationNodeKind5,
    ]


class ComputationNodeKindV24(ComputationNodeKind3):
    pass


class ComputationNodeKindV2(
    RootModel[
        Union[
            ComputationNodeKindV21,
            ComputationNodeKindV22,
            ComputationNodeKindV23,
            ComputationNodeKindV24,
            ComputationNodeKindV25,
            ComputationNodeKindV26,
            ComputationNodeKindV27,
        ]
    ]
):
    root: Union[
        ComputationNodeKindV21,
        ComputationNodeKindV22,
        ComputationNodeKindV23,
        ComputationNodeKindV24,
        ComputationNodeKindV25,
        ComputationNodeKindV26,
        ComputationNodeKindV27,
    ]


class ComputationNodeKindV64(ComputationNodeKind3):
    pass


class ComputationNodeKindV610(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    exportConnector: ExportConnectorNode


class ComputationNodeKindV94(ComputationNodeKind3):
    pass


class ComputationNodeKindV910(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    exportConnector: ExportConnectorNodeV9


class ComputationNodeKindV912(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    environment: EnvironmentComputationNode


class ComputationNodeV2(BaseModel):
    kind: ComputationNodeKindV2


class DatasetSinkComputationNode(BaseModel):
    datasetImportId: Optional[str] = None
    encryptionKeyDependency: DatasetSinkEncryptionKeyDependency
    input: DatasetSinkInput
    specificationId: str


class LeafNodeKind2(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    table: TableLeafNode


class LeafNodeKind(RootModel[Union[LeafNodeKind1, LeafNodeKind2]]):
    root: Union[LeafNodeKind1, LeafNodeKind2]


class LeafNodeKindV22(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    table: TableLeafNodeV2


class LeafNodeKindV2(RootModel[Union[LeafNodeKindV21, LeafNodeKindV22]]):
    root: Union[LeafNodeKindV21, LeafNodeKindV22]


class LeafNodeV2(BaseModel):
    isRequired: bool
    kind: LeafNodeKindV2


class NodeKindV21(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    leaf: LeafNodeV2


class NodeKindV22(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    computation: ComputationNodeV2


class NodeKindV2(RootModel[Union[NodeKindV21, NodeKindV22]]):
    root: Union[NodeKindV21, NodeKindV22]


class NodeKindV61(NodeKindV21):
    pass


class NodeKindV91(NodeKindV21):
    pass


class NodeV2(BaseModel):
    id: str
    kind: NodeKindV2
    name: str


class AddComputationCommitV2(BaseModel):
    analysts: Sequence[str]
    enclaveSpecifications: Sequence[EnclaveSpecification]
    node: NodeV2


class ComputationNode(BaseModel):
    kind: ComputationNodeKind


class ComputationNodeKindV611(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    datasetSink: DatasetSinkComputationNode


class ComputationNodeKindV6(
    RootModel[
        Union[
            ComputationNodeKindV61,
            ComputationNodeKindV62,
            ComputationNodeKindV63,
            ComputationNodeKindV64,
            ComputationNodeKindV65,
            ComputationNodeKindV66,
            ComputationNodeKindV67,
            ComputationNodeKindV68,
            ComputationNodeKindV69,
            ComputationNodeKindV610,
            ComputationNodeKindV611,
        ]
    ]
):
    root: Union[
        ComputationNodeKindV61,
        ComputationNodeKindV62,
        ComputationNodeKindV63,
        ComputationNodeKindV64,
        ComputationNodeKindV65,
        ComputationNodeKindV66,
        ComputationNodeKindV67,
        ComputationNodeKindV68,
        ComputationNodeKindV69,
        ComputationNodeKindV610,
        ComputationNodeKindV611,
    ]


class ComputationNodeKindV911(ComputationNodeKindV611):
    pass


class ComputationNodeKindV9(
    RootModel[
        Union[
            ComputationNodeKindV91,
            ComputationNodeKindV92,
            ComputationNodeKindV93,
            ComputationNodeKindV94,
            ComputationNodeKindV95,
            ComputationNodeKindV96,
            ComputationNodeKindV97,
            ComputationNodeKindV98,
            ComputationNodeKindV99,
            ComputationNodeKindV910,
            ComputationNodeKindV911,
            ComputationNodeKindV912,
        ]
    ]
):
    root: Union[
        ComputationNodeKindV91,
        ComputationNodeKindV92,
        ComputationNodeKindV93,
        ComputationNodeKindV94,
        ComputationNodeKindV95,
        ComputationNodeKindV96,
        ComputationNodeKindV97,
        ComputationNodeKindV98,
        ComputationNodeKindV99,
        ComputationNodeKindV910,
        ComputationNodeKindV911,
        ComputationNodeKindV912,
    ]


class ComputationNodeV6(BaseModel):
    kind: ComputationNodeKindV6


class ComputationNodeV9(BaseModel):
    kind: ComputationNodeKindV9


class DataScienceCommitKindV21(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    addComputation: AddComputationCommitV2


class DataScienceCommitKindV2(RootModel[DataScienceCommitKindV21]):
    root: DataScienceCommitKindV21


class DataScienceCommitV2(BaseModel):
    enclaveDataRoomId: str
    historyPin: str
    id: str
    kind: DataScienceCommitKindV2
    name: str


class DataScienceCommitV3(DataScienceCommitV2):
    pass


class DataScienceCommitV4(DataScienceCommitV2):
    pass


class DataScienceCommitV5(DataScienceCommitV2):
    pass


class LeafNode(BaseModel):
    isRequired: bool
    kind: LeafNodeKind


class NodeKind1(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    leaf: LeafNode


class NodeKind2(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    computation: ComputationNode


class NodeKind(RootModel[Union[NodeKind1, NodeKind2]]):
    root: Union[NodeKind1, NodeKind2]


class NodeKindV62(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    computation: ComputationNodeV6


class NodeKindV6(RootModel[Union[NodeKindV61, NodeKindV62]]):
    root: Union[NodeKindV61, NodeKindV62]


class NodeKindV92(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    computation: ComputationNodeV9


class NodeKindV9(RootModel[Union[NodeKindV91, NodeKindV92]]):
    root: Union[NodeKindV91, NodeKindV92]


class NodeV6(BaseModel):
    id: str
    kind: NodeKindV6
    name: str


class NodeV9(BaseModel):
    id: str
    kind: NodeKindV9
    name: str


class DataScienceCommit3(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    v2: DataScienceCommitV2


class DataScienceCommit4(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    v3: DataScienceCommitV3


class DataScienceCommit5(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    v4: DataScienceCommitV4


class DataScienceCommit6(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    v5: DataScienceCommitV5


class AddComputationCommitV6(BaseModel):
    analysts: Sequence[str]
    enclaveSpecifications: Sequence[EnclaveSpecification]
    node: NodeV6


class AddComputationCommitV9(BaseModel):
    analysts: Sequence[str]
    enclaveSpecifications: Sequence[EnclaveSpecification]
    node: NodeV9


class DataScienceCommitKindV61(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    addComputation: AddComputationCommitV6


class DataScienceCommitKindV6(RootModel[DataScienceCommitKindV61]):
    root: DataScienceCommitKindV61


class DataScienceCommitKindV91(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    addComputation: AddComputationCommitV9


class DataScienceCommitKindV9(RootModel[DataScienceCommitKindV91]):
    root: DataScienceCommitKindV91


class DataScienceCommitV6(BaseModel):
    enclaveDataRoomId: str
    historyPin: str
    id: str
    kind: DataScienceCommitKindV6
    name: str


class DataScienceCommitV7(DataScienceCommitV6):
    pass


class DataScienceCommitV8(DataScienceCommitV6):
    pass


class DataScienceCommitV9(BaseModel):
    enclaveDataRoomId: str
    historyPin: str
    id: str
    kind: DataScienceCommitKindV9
    name: str


class Node(BaseModel):
    id: str
    kind: NodeKind
    name: str


class DataScienceCommit7(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    v6: DataScienceCommitV6


class DataScienceCommit8(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    v7: DataScienceCommitV7


class DataScienceCommit9(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    v8: DataScienceCommitV8


class DataScienceCommit10(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    v9: DataScienceCommitV9


class AddComputationCommit(BaseModel):
    analysts: Sequence[str]
    enclaveSpecifications: Sequence[EnclaveSpecification]
    node: Node


class DataScienceCommitKind1(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    addComputation: AddComputationCommit


class DataScienceCommitKind(RootModel[DataScienceCommitKind1]):
    root: DataScienceCommitKind1


class DataScienceCommitV0(BaseModel):
    enclaveDataRoomId: str
    historyPin: str
    id: str
    kind: DataScienceCommitKind
    name: str


class DataScienceCommitV1(DataScienceCommitV0):
    pass


class DataScienceCommit1(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    v0: DataScienceCommitV0


class DataScienceCommit2(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    v1: DataScienceCommitV1


class DataScienceCommit(
    RootModel[
        Union[
            DataScienceCommit1,
            DataScienceCommit2,
            DataScienceCommit3,
            DataScienceCommit4,
            DataScienceCommit5,
            DataScienceCommit6,
            DataScienceCommit7,
            DataScienceCommit8,
            DataScienceCommit9,
            DataScienceCommit10,
        ]
    ]
):
    root: Union[
        DataScienceCommit1,
        DataScienceCommit2,
        DataScienceCommit3,
        DataScienceCommit4,
        DataScienceCommit5,
        DataScienceCommit6,
        DataScienceCommit7,
        DataScienceCommit8,
        DataScienceCommit9,
        DataScienceCommit10,
    ] = Field(..., title='DataScienceCommit')
