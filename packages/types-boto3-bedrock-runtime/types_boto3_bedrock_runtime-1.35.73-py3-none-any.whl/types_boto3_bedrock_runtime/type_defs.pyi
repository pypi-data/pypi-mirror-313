"""
Type annotations for bedrock-runtime service type definitions.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_runtime/type_defs/)

Usage::

    ```python
    from types_boto3_bedrock_runtime.type_defs import GuardrailOutputContentTypeDef

    data: GuardrailOutputContentTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import IO, Any, Dict, List, Mapping, Sequence, Union

from botocore.eventstream import EventStream
from botocore.response import StreamingBody

from .literals import (
    ConversationRoleType,
    DocumentFormatType,
    GuardrailActionType,
    GuardrailContentFilterConfidenceType,
    GuardrailContentFilterStrengthType,
    GuardrailContentFilterTypeType,
    GuardrailContentQualifierType,
    GuardrailContentSourceType,
    GuardrailContextualGroundingFilterTypeType,
    GuardrailContextualGroundingPolicyActionType,
    GuardrailConverseContentQualifierType,
    GuardrailPiiEntityTypeType,
    GuardrailSensitiveInformationPolicyActionType,
    GuardrailStreamProcessingModeType,
    GuardrailTraceType,
    ImageFormatType,
    PerformanceConfigLatencyType,
    StopReasonType,
    ToolResultStatusType,
    TraceType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "ApplyGuardrailRequestRequestTypeDef",
    "ApplyGuardrailResponseTypeDef",
    "BlobTypeDef",
    "ContentBlockDeltaEventTypeDef",
    "ContentBlockDeltaTypeDef",
    "ContentBlockOutputTypeDef",
    "ContentBlockStartEventTypeDef",
    "ContentBlockStartTypeDef",
    "ContentBlockStopEventTypeDef",
    "ContentBlockTypeDef",
    "ContentBlockUnionTypeDef",
    "ConverseMetricsTypeDef",
    "ConverseOutputTypeDef",
    "ConverseRequestRequestTypeDef",
    "ConverseResponseTypeDef",
    "ConverseStreamMetadataEventTypeDef",
    "ConverseStreamMetricsTypeDef",
    "ConverseStreamOutputTypeDef",
    "ConverseStreamRequestRequestTypeDef",
    "ConverseStreamResponseTypeDef",
    "ConverseStreamTraceTypeDef",
    "ConverseTraceTypeDef",
    "DocumentBlockOutputTypeDef",
    "DocumentBlockTypeDef",
    "DocumentBlockUnionTypeDef",
    "DocumentSourceOutputTypeDef",
    "DocumentSourceTypeDef",
    "DocumentSourceUnionTypeDef",
    "GuardrailAssessmentTypeDef",
    "GuardrailConfigurationTypeDef",
    "GuardrailContentBlockTypeDef",
    "GuardrailContentFilterTypeDef",
    "GuardrailContentPolicyAssessmentTypeDef",
    "GuardrailContextualGroundingFilterTypeDef",
    "GuardrailContextualGroundingPolicyAssessmentTypeDef",
    "GuardrailConverseContentBlockOutputTypeDef",
    "GuardrailConverseContentBlockTypeDef",
    "GuardrailConverseContentBlockUnionTypeDef",
    "GuardrailConverseTextBlockOutputTypeDef",
    "GuardrailConverseTextBlockTypeDef",
    "GuardrailConverseTextBlockUnionTypeDef",
    "GuardrailCoverageTypeDef",
    "GuardrailCustomWordTypeDef",
    "GuardrailInvocationMetricsTypeDef",
    "GuardrailManagedWordTypeDef",
    "GuardrailOutputContentTypeDef",
    "GuardrailPiiEntityFilterTypeDef",
    "GuardrailRegexFilterTypeDef",
    "GuardrailSensitiveInformationPolicyAssessmentTypeDef",
    "GuardrailStreamConfigurationTypeDef",
    "GuardrailTextBlockTypeDef",
    "GuardrailTextCharactersCoverageTypeDef",
    "GuardrailTopicPolicyAssessmentTypeDef",
    "GuardrailTopicTypeDef",
    "GuardrailTraceAssessmentTypeDef",
    "GuardrailUsageTypeDef",
    "GuardrailWordPolicyAssessmentTypeDef",
    "ImageBlockOutputTypeDef",
    "ImageBlockTypeDef",
    "ImageBlockUnionTypeDef",
    "ImageSourceOutputTypeDef",
    "ImageSourceTypeDef",
    "ImageSourceUnionTypeDef",
    "InferenceConfigurationTypeDef",
    "InternalServerExceptionTypeDef",
    "InvokeModelRequestRequestTypeDef",
    "InvokeModelResponseTypeDef",
    "InvokeModelWithResponseStreamRequestRequestTypeDef",
    "InvokeModelWithResponseStreamResponseTypeDef",
    "MessageOutputTypeDef",
    "MessageStartEventTypeDef",
    "MessageStopEventTypeDef",
    "MessageTypeDef",
    "MessageUnionTypeDef",
    "ModelStreamErrorExceptionTypeDef",
    "ModelTimeoutExceptionTypeDef",
    "PayloadPartTypeDef",
    "PerformanceConfigurationTypeDef",
    "PromptVariableValuesTypeDef",
    "ResponseMetadataTypeDef",
    "ResponseStreamTypeDef",
    "ServiceUnavailableExceptionTypeDef",
    "SpecificToolChoiceTypeDef",
    "SystemContentBlockTypeDef",
    "ThrottlingExceptionTypeDef",
    "TokenUsageTypeDef",
    "ToolChoiceTypeDef",
    "ToolConfigurationTypeDef",
    "ToolInputSchemaTypeDef",
    "ToolResultBlockOutputTypeDef",
    "ToolResultBlockTypeDef",
    "ToolResultBlockUnionTypeDef",
    "ToolResultContentBlockOutputTypeDef",
    "ToolResultContentBlockTypeDef",
    "ToolResultContentBlockUnionTypeDef",
    "ToolSpecificationTypeDef",
    "ToolTypeDef",
    "ToolUseBlockDeltaTypeDef",
    "ToolUseBlockOutputTypeDef",
    "ToolUseBlockStartTypeDef",
    "ToolUseBlockTypeDef",
    "ToolUseBlockUnionTypeDef",
    "ValidationExceptionTypeDef",
)

class GuardrailOutputContentTypeDef(TypedDict):
    text: NotRequired[str]

class GuardrailUsageTypeDef(TypedDict):
    topicPolicyUnits: int
    contentPolicyUnits: int
    wordPolicyUnits: int
    sensitiveInformationPolicyUnits: int
    sensitiveInformationPolicyFreeUnits: int
    contextualGroundingPolicyUnits: int

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]
ToolUseBlockDeltaTypeDef = TypedDict(
    "ToolUseBlockDeltaTypeDef",
    {
        "input": str,
    },
)
ToolUseBlockOutputTypeDef = TypedDict(
    "ToolUseBlockOutputTypeDef",
    {
        "toolUseId": str,
        "name": str,
        "input": Dict[str, Any],
    },
)

class ToolUseBlockStartTypeDef(TypedDict):
    toolUseId: str
    name: str

class ContentBlockStopEventTypeDef(TypedDict):
    contentBlockIndex: int

class ConverseMetricsTypeDef(TypedDict):
    latencyMs: int

class GuardrailConfigurationTypeDef(TypedDict):
    guardrailIdentifier: str
    guardrailVersion: str
    trace: NotRequired[GuardrailTraceType]

class InferenceConfigurationTypeDef(TypedDict):
    maxTokens: NotRequired[int]
    temperature: NotRequired[float]
    topP: NotRequired[float]
    stopSequences: NotRequired[Sequence[str]]

class PerformanceConfigurationTypeDef(TypedDict):
    latency: NotRequired[PerformanceConfigLatencyType]

class PromptVariableValuesTypeDef(TypedDict):
    text: NotRequired[str]

class TokenUsageTypeDef(TypedDict):
    inputTokens: int
    outputTokens: int
    totalTokens: int

class ConverseStreamMetricsTypeDef(TypedDict):
    latencyMs: int

class InternalServerExceptionTypeDef(TypedDict):
    message: NotRequired[str]

class MessageStartEventTypeDef(TypedDict):
    role: ConversationRoleType

class MessageStopEventTypeDef(TypedDict):
    stopReason: StopReasonType
    additionalModelResponseFields: NotRequired[Dict[str, Any]]

class ModelStreamErrorExceptionTypeDef(TypedDict):
    message: NotRequired[str]
    originalStatusCode: NotRequired[int]
    originalMessage: NotRequired[str]

class ServiceUnavailableExceptionTypeDef(TypedDict):
    message: NotRequired[str]

class ThrottlingExceptionTypeDef(TypedDict):
    message: NotRequired[str]

class ValidationExceptionTypeDef(TypedDict):
    message: NotRequired[str]

class GuardrailStreamConfigurationTypeDef(TypedDict):
    guardrailIdentifier: str
    guardrailVersion: str
    trace: NotRequired[GuardrailTraceType]
    streamProcessingMode: NotRequired[GuardrailStreamProcessingModeType]

DocumentSourceOutputTypeDef = TypedDict(
    "DocumentSourceOutputTypeDef",
    {
        "bytes": NotRequired[bytes],
    },
)

class GuardrailTextBlockTypeDef(TypedDict):
    text: str
    qualifiers: NotRequired[Sequence[GuardrailContentQualifierType]]

GuardrailContentFilterTypeDef = TypedDict(
    "GuardrailContentFilterTypeDef",
    {
        "type": GuardrailContentFilterTypeType,
        "confidence": GuardrailContentFilterConfidenceType,
        "action": Literal["BLOCKED"],
        "filterStrength": NotRequired[GuardrailContentFilterStrengthType],
    },
)
GuardrailContextualGroundingFilterTypeDef = TypedDict(
    "GuardrailContextualGroundingFilterTypeDef",
    {
        "type": GuardrailContextualGroundingFilterTypeType,
        "threshold": float,
        "score": float,
        "action": GuardrailContextualGroundingPolicyActionType,
    },
)

class GuardrailConverseTextBlockOutputTypeDef(TypedDict):
    text: str
    qualifiers: NotRequired[List[GuardrailConverseContentQualifierType]]

class GuardrailConverseTextBlockTypeDef(TypedDict):
    text: str
    qualifiers: NotRequired[Sequence[GuardrailConverseContentQualifierType]]

class GuardrailTextCharactersCoverageTypeDef(TypedDict):
    guarded: NotRequired[int]
    total: NotRequired[int]

class GuardrailCustomWordTypeDef(TypedDict):
    match: str
    action: Literal["BLOCKED"]

GuardrailManagedWordTypeDef = TypedDict(
    "GuardrailManagedWordTypeDef",
    {
        "match": str,
        "type": Literal["PROFANITY"],
        "action": Literal["BLOCKED"],
    },
)
GuardrailPiiEntityFilterTypeDef = TypedDict(
    "GuardrailPiiEntityFilterTypeDef",
    {
        "match": str,
        "type": GuardrailPiiEntityTypeType,
        "action": GuardrailSensitiveInformationPolicyActionType,
    },
)

class GuardrailRegexFilterTypeDef(TypedDict):
    action: GuardrailSensitiveInformationPolicyActionType
    name: NotRequired[str]
    match: NotRequired[str]
    regex: NotRequired[str]

GuardrailTopicTypeDef = TypedDict(
    "GuardrailTopicTypeDef",
    {
        "name": str,
        "type": Literal["DENY"],
        "action": Literal["BLOCKED"],
    },
)
ImageSourceOutputTypeDef = TypedDict(
    "ImageSourceOutputTypeDef",
    {
        "bytes": NotRequired[bytes],
    },
)

class ModelTimeoutExceptionTypeDef(TypedDict):
    message: NotRequired[str]

PayloadPartTypeDef = TypedDict(
    "PayloadPartTypeDef",
    {
        "bytes": NotRequired[bytes],
    },
)

class SpecificToolChoiceTypeDef(TypedDict):
    name: str

class ToolInputSchemaTypeDef(TypedDict):
    json: NotRequired[Mapping[str, Any]]

ToolUseBlockTypeDef = TypedDict(
    "ToolUseBlockTypeDef",
    {
        "toolUseId": str,
        "name": str,
        "input": Mapping[str, Any],
    },
)

class InvokeModelResponseTypeDef(TypedDict):
    body: StreamingBody
    contentType: str
    performanceConfigLatency: PerformanceConfigLatencyType
    ResponseMetadata: ResponseMetadataTypeDef

DocumentSourceTypeDef = TypedDict(
    "DocumentSourceTypeDef",
    {
        "bytes": NotRequired[BlobTypeDef],
    },
)
ImageSourceTypeDef = TypedDict(
    "ImageSourceTypeDef",
    {
        "bytes": NotRequired[BlobTypeDef],
    },
)

class InvokeModelRequestRequestTypeDef(TypedDict):
    modelId: str
    body: NotRequired[BlobTypeDef]
    contentType: NotRequired[str]
    accept: NotRequired[str]
    trace: NotRequired[TraceType]
    guardrailIdentifier: NotRequired[str]
    guardrailVersion: NotRequired[str]
    performanceConfigLatency: NotRequired[PerformanceConfigLatencyType]

class InvokeModelWithResponseStreamRequestRequestTypeDef(TypedDict):
    modelId: str
    body: NotRequired[BlobTypeDef]
    contentType: NotRequired[str]
    accept: NotRequired[str]
    trace: NotRequired[TraceType]
    guardrailIdentifier: NotRequired[str]
    guardrailVersion: NotRequired[str]
    performanceConfigLatency: NotRequired[PerformanceConfigLatencyType]

class ContentBlockDeltaTypeDef(TypedDict):
    text: NotRequired[str]
    toolUse: NotRequired[ToolUseBlockDeltaTypeDef]

class ContentBlockStartTypeDef(TypedDict):
    toolUse: NotRequired[ToolUseBlockStartTypeDef]

DocumentBlockOutputTypeDef = TypedDict(
    "DocumentBlockOutputTypeDef",
    {
        "format": DocumentFormatType,
        "name": str,
        "source": DocumentSourceOutputTypeDef,
    },
)

class GuardrailContentBlockTypeDef(TypedDict):
    text: NotRequired[GuardrailTextBlockTypeDef]

class GuardrailContentPolicyAssessmentTypeDef(TypedDict):
    filters: List[GuardrailContentFilterTypeDef]

class GuardrailContextualGroundingPolicyAssessmentTypeDef(TypedDict):
    filters: NotRequired[List[GuardrailContextualGroundingFilterTypeDef]]

class GuardrailConverseContentBlockOutputTypeDef(TypedDict):
    text: NotRequired[GuardrailConverseTextBlockOutputTypeDef]

GuardrailConverseTextBlockUnionTypeDef = Union[
    GuardrailConverseTextBlockTypeDef, GuardrailConverseTextBlockOutputTypeDef
]

class GuardrailCoverageTypeDef(TypedDict):
    textCharacters: NotRequired[GuardrailTextCharactersCoverageTypeDef]

class GuardrailWordPolicyAssessmentTypeDef(TypedDict):
    customWords: List[GuardrailCustomWordTypeDef]
    managedWordLists: List[GuardrailManagedWordTypeDef]

class GuardrailSensitiveInformationPolicyAssessmentTypeDef(TypedDict):
    piiEntities: List[GuardrailPiiEntityFilterTypeDef]
    regexes: List[GuardrailRegexFilterTypeDef]

class GuardrailTopicPolicyAssessmentTypeDef(TypedDict):
    topics: List[GuardrailTopicTypeDef]

ImageBlockOutputTypeDef = TypedDict(
    "ImageBlockOutputTypeDef",
    {
        "format": ImageFormatType,
        "source": ImageSourceOutputTypeDef,
    },
)

class ResponseStreamTypeDef(TypedDict):
    chunk: NotRequired[PayloadPartTypeDef]
    internalServerException: NotRequired[InternalServerExceptionTypeDef]
    modelStreamErrorException: NotRequired[ModelStreamErrorExceptionTypeDef]
    validationException: NotRequired[ValidationExceptionTypeDef]
    throttlingException: NotRequired[ThrottlingExceptionTypeDef]
    modelTimeoutException: NotRequired[ModelTimeoutExceptionTypeDef]
    serviceUnavailableException: NotRequired[ServiceUnavailableExceptionTypeDef]

ToolChoiceTypeDef = TypedDict(
    "ToolChoiceTypeDef",
    {
        "auto": NotRequired[Mapping[str, Any]],
        "any": NotRequired[Mapping[str, Any]],
        "tool": NotRequired[SpecificToolChoiceTypeDef],
    },
)

class ToolSpecificationTypeDef(TypedDict):
    name: str
    inputSchema: ToolInputSchemaTypeDef
    description: NotRequired[str]

ToolUseBlockUnionTypeDef = Union[ToolUseBlockTypeDef, ToolUseBlockOutputTypeDef]
DocumentSourceUnionTypeDef = Union[DocumentSourceTypeDef, DocumentSourceOutputTypeDef]
ImageSourceUnionTypeDef = Union[ImageSourceTypeDef, ImageSourceOutputTypeDef]

class ContentBlockDeltaEventTypeDef(TypedDict):
    delta: ContentBlockDeltaTypeDef
    contentBlockIndex: int

class ContentBlockStartEventTypeDef(TypedDict):
    start: ContentBlockStartTypeDef
    contentBlockIndex: int

class ApplyGuardrailRequestRequestTypeDef(TypedDict):
    guardrailIdentifier: str
    guardrailVersion: str
    source: GuardrailContentSourceType
    content: Sequence[GuardrailContentBlockTypeDef]

class GuardrailConverseContentBlockTypeDef(TypedDict):
    text: NotRequired[GuardrailConverseTextBlockUnionTypeDef]

class GuardrailInvocationMetricsTypeDef(TypedDict):
    guardrailProcessingLatency: NotRequired[int]
    usage: NotRequired[GuardrailUsageTypeDef]
    guardrailCoverage: NotRequired[GuardrailCoverageTypeDef]

class ToolResultContentBlockOutputTypeDef(TypedDict):
    json: NotRequired[Dict[str, Any]]
    text: NotRequired[str]
    image: NotRequired[ImageBlockOutputTypeDef]
    document: NotRequired[DocumentBlockOutputTypeDef]

class InvokeModelWithResponseStreamResponseTypeDef(TypedDict):
    body: "EventStream[ResponseStreamTypeDef]"
    contentType: str
    performanceConfigLatency: PerformanceConfigLatencyType
    ResponseMetadata: ResponseMetadataTypeDef

class ToolTypeDef(TypedDict):
    toolSpec: NotRequired[ToolSpecificationTypeDef]

DocumentBlockTypeDef = TypedDict(
    "DocumentBlockTypeDef",
    {
        "format": DocumentFormatType,
        "name": str,
        "source": DocumentSourceUnionTypeDef,
    },
)
ImageBlockTypeDef = TypedDict(
    "ImageBlockTypeDef",
    {
        "format": ImageFormatType,
        "source": ImageSourceUnionTypeDef,
    },
)
GuardrailConverseContentBlockUnionTypeDef = Union[
    GuardrailConverseContentBlockTypeDef, GuardrailConverseContentBlockOutputTypeDef
]

class GuardrailAssessmentTypeDef(TypedDict):
    topicPolicy: NotRequired[GuardrailTopicPolicyAssessmentTypeDef]
    contentPolicy: NotRequired[GuardrailContentPolicyAssessmentTypeDef]
    wordPolicy: NotRequired[GuardrailWordPolicyAssessmentTypeDef]
    sensitiveInformationPolicy: NotRequired[GuardrailSensitiveInformationPolicyAssessmentTypeDef]
    contextualGroundingPolicy: NotRequired[GuardrailContextualGroundingPolicyAssessmentTypeDef]
    invocationMetrics: NotRequired[GuardrailInvocationMetricsTypeDef]

class ToolResultBlockOutputTypeDef(TypedDict):
    toolUseId: str
    content: List[ToolResultContentBlockOutputTypeDef]
    status: NotRequired[ToolResultStatusType]

class ToolConfigurationTypeDef(TypedDict):
    tools: Sequence[ToolTypeDef]
    toolChoice: NotRequired[ToolChoiceTypeDef]

DocumentBlockUnionTypeDef = Union[DocumentBlockTypeDef, DocumentBlockOutputTypeDef]
ImageBlockUnionTypeDef = Union[ImageBlockTypeDef, ImageBlockOutputTypeDef]

class SystemContentBlockTypeDef(TypedDict):
    text: NotRequired[str]
    guardContent: NotRequired[GuardrailConverseContentBlockUnionTypeDef]

class ApplyGuardrailResponseTypeDef(TypedDict):
    usage: GuardrailUsageTypeDef
    action: GuardrailActionType
    outputs: List[GuardrailOutputContentTypeDef]
    assessments: List[GuardrailAssessmentTypeDef]
    guardrailCoverage: GuardrailCoverageTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GuardrailTraceAssessmentTypeDef(TypedDict):
    modelOutput: NotRequired[List[str]]
    inputAssessment: NotRequired[Dict[str, GuardrailAssessmentTypeDef]]
    outputAssessments: NotRequired[Dict[str, List[GuardrailAssessmentTypeDef]]]

class ContentBlockOutputTypeDef(TypedDict):
    text: NotRequired[str]
    image: NotRequired[ImageBlockOutputTypeDef]
    document: NotRequired[DocumentBlockOutputTypeDef]
    toolUse: NotRequired[ToolUseBlockOutputTypeDef]
    toolResult: NotRequired[ToolResultBlockOutputTypeDef]
    guardContent: NotRequired[GuardrailConverseContentBlockOutputTypeDef]

class ToolResultContentBlockTypeDef(TypedDict):
    json: NotRequired[Mapping[str, Any]]
    text: NotRequired[str]
    image: NotRequired[ImageBlockUnionTypeDef]
    document: NotRequired[DocumentBlockUnionTypeDef]

class ConverseStreamTraceTypeDef(TypedDict):
    guardrail: NotRequired[GuardrailTraceAssessmentTypeDef]

class ConverseTraceTypeDef(TypedDict):
    guardrail: NotRequired[GuardrailTraceAssessmentTypeDef]

class MessageOutputTypeDef(TypedDict):
    role: ConversationRoleType
    content: List[ContentBlockOutputTypeDef]

ToolResultContentBlockUnionTypeDef = Union[
    ToolResultContentBlockTypeDef, ToolResultContentBlockOutputTypeDef
]

class ConverseStreamMetadataEventTypeDef(TypedDict):
    usage: TokenUsageTypeDef
    metrics: ConverseStreamMetricsTypeDef
    trace: NotRequired[ConverseStreamTraceTypeDef]
    performanceConfig: NotRequired[PerformanceConfigurationTypeDef]

class ConverseOutputTypeDef(TypedDict):
    message: NotRequired[MessageOutputTypeDef]

class ToolResultBlockTypeDef(TypedDict):
    toolUseId: str
    content: Sequence[ToolResultContentBlockUnionTypeDef]
    status: NotRequired[ToolResultStatusType]

class ConverseStreamOutputTypeDef(TypedDict):
    messageStart: NotRequired[MessageStartEventTypeDef]
    contentBlockStart: NotRequired[ContentBlockStartEventTypeDef]
    contentBlockDelta: NotRequired[ContentBlockDeltaEventTypeDef]
    contentBlockStop: NotRequired[ContentBlockStopEventTypeDef]
    messageStop: NotRequired[MessageStopEventTypeDef]
    metadata: NotRequired[ConverseStreamMetadataEventTypeDef]
    internalServerException: NotRequired[InternalServerExceptionTypeDef]
    modelStreamErrorException: NotRequired[ModelStreamErrorExceptionTypeDef]
    validationException: NotRequired[ValidationExceptionTypeDef]
    throttlingException: NotRequired[ThrottlingExceptionTypeDef]
    serviceUnavailableException: NotRequired[ServiceUnavailableExceptionTypeDef]

class ConverseResponseTypeDef(TypedDict):
    output: ConverseOutputTypeDef
    stopReason: StopReasonType
    usage: TokenUsageTypeDef
    metrics: ConverseMetricsTypeDef
    additionalModelResponseFields: Dict[str, Any]
    trace: ConverseTraceTypeDef
    performanceConfig: PerformanceConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

ToolResultBlockUnionTypeDef = Union[ToolResultBlockTypeDef, ToolResultBlockOutputTypeDef]

class ConverseStreamResponseTypeDef(TypedDict):
    stream: "EventStream[ConverseStreamOutputTypeDef]"
    ResponseMetadata: ResponseMetadataTypeDef

class ContentBlockTypeDef(TypedDict):
    text: NotRequired[str]
    image: NotRequired[ImageBlockUnionTypeDef]
    document: NotRequired[DocumentBlockUnionTypeDef]
    toolUse: NotRequired[ToolUseBlockUnionTypeDef]
    toolResult: NotRequired[ToolResultBlockUnionTypeDef]
    guardContent: NotRequired[GuardrailConverseContentBlockUnionTypeDef]

ContentBlockUnionTypeDef = Union[ContentBlockTypeDef, ContentBlockOutputTypeDef]

class MessageTypeDef(TypedDict):
    role: ConversationRoleType
    content: Sequence[ContentBlockUnionTypeDef]

class ConverseStreamRequestRequestTypeDef(TypedDict):
    modelId: str
    messages: NotRequired[Sequence[MessageTypeDef]]
    system: NotRequired[Sequence[SystemContentBlockTypeDef]]
    inferenceConfig: NotRequired[InferenceConfigurationTypeDef]
    toolConfig: NotRequired[ToolConfigurationTypeDef]
    guardrailConfig: NotRequired[GuardrailStreamConfigurationTypeDef]
    additionalModelRequestFields: NotRequired[Mapping[str, Any]]
    promptVariables: NotRequired[Mapping[str, PromptVariableValuesTypeDef]]
    additionalModelResponseFieldPaths: NotRequired[Sequence[str]]
    performanceConfig: NotRequired[PerformanceConfigurationTypeDef]

MessageUnionTypeDef = Union[MessageTypeDef, MessageOutputTypeDef]

class ConverseRequestRequestTypeDef(TypedDict):
    modelId: str
    messages: NotRequired[Sequence[MessageUnionTypeDef]]
    system: NotRequired[Sequence[SystemContentBlockTypeDef]]
    inferenceConfig: NotRequired[InferenceConfigurationTypeDef]
    toolConfig: NotRequired[ToolConfigurationTypeDef]
    guardrailConfig: NotRequired[GuardrailConfigurationTypeDef]
    additionalModelRequestFields: NotRequired[Mapping[str, Any]]
    promptVariables: NotRequired[Mapping[str, PromptVariableValuesTypeDef]]
    additionalModelResponseFieldPaths: NotRequired[Sequence[str]]
    performanceConfig: NotRequired[PerformanceConfigurationTypeDef]
