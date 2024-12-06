"""
Type annotations for bedrock service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock/type_defs/)

Usage::

    ```python
    from mypy_boto3_bedrock.type_defs import BatchDeleteEvaluationJobErrorTypeDef

    data: BatchDeleteEvaluationJobErrorTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Mapping, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    ApplicationTypeType,
    CommitmentDurationType,
    CustomizationTypeType,
    EvaluationJobStatusType,
    EvaluationJobTypeType,
    EvaluationTaskTypeType,
    ExternalSourceTypeType,
    FineTuningJobStatusType,
    FoundationModelLifecycleStatusType,
    GuardrailContentFilterTypeType,
    GuardrailContextualGroundingFilterTypeType,
    GuardrailFilterStrengthType,
    GuardrailModalityType,
    GuardrailPiiEntityTypeType,
    GuardrailSensitiveInformationActionType,
    GuardrailStatusType,
    InferenceProfileTypeType,
    InferenceTypeType,
    ModelCopyJobStatusType,
    ModelCustomizationJobStatusType,
    ModelCustomizationType,
    ModelImportJobStatusType,
    ModelInvocationJobStatusType,
    ModelModalityType,
    PromptRouterTypeType,
    ProvisionedModelStatusType,
    RetrieveAndGenerateTypeType,
    SearchTypeType,
    SortOrderType,
    StatusType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AutomatedEvaluationConfigOutputTypeDef",
    "AutomatedEvaluationConfigTypeDef",
    "AutomatedEvaluationConfigUnionTypeDef",
    "BatchDeleteEvaluationJobErrorTypeDef",
    "BatchDeleteEvaluationJobItemTypeDef",
    "BatchDeleteEvaluationJobRequestRequestTypeDef",
    "BatchDeleteEvaluationJobResponseTypeDef",
    "BedrockEvaluatorModelTypeDef",
    "BlobTypeDef",
    "ByteContentDocOutputTypeDef",
    "ByteContentDocTypeDef",
    "ByteContentDocUnionTypeDef",
    "CloudWatchConfigTypeDef",
    "CreateEvaluationJobRequestRequestTypeDef",
    "CreateEvaluationJobResponseTypeDef",
    "CreateGuardrailRequestRequestTypeDef",
    "CreateGuardrailResponseTypeDef",
    "CreateGuardrailVersionRequestRequestTypeDef",
    "CreateGuardrailVersionResponseTypeDef",
    "CreateInferenceProfileRequestRequestTypeDef",
    "CreateInferenceProfileResponseTypeDef",
    "CreateMarketplaceModelEndpointRequestRequestTypeDef",
    "CreateMarketplaceModelEndpointResponseTypeDef",
    "CreateModelCopyJobRequestRequestTypeDef",
    "CreateModelCopyJobResponseTypeDef",
    "CreateModelCustomizationJobRequestRequestTypeDef",
    "CreateModelCustomizationJobResponseTypeDef",
    "CreateModelImportJobRequestRequestTypeDef",
    "CreateModelImportJobResponseTypeDef",
    "CreateModelInvocationJobRequestRequestTypeDef",
    "CreateModelInvocationJobResponseTypeDef",
    "CreateProvisionedModelThroughputRequestRequestTypeDef",
    "CreateProvisionedModelThroughputResponseTypeDef",
    "CustomModelSummaryTypeDef",
    "CustomizationConfigTypeDef",
    "DeleteCustomModelRequestRequestTypeDef",
    "DeleteGuardrailRequestRequestTypeDef",
    "DeleteImportedModelRequestRequestTypeDef",
    "DeleteInferenceProfileRequestRequestTypeDef",
    "DeleteMarketplaceModelEndpointRequestRequestTypeDef",
    "DeleteProvisionedModelThroughputRequestRequestTypeDef",
    "DeregisterMarketplaceModelEndpointRequestRequestTypeDef",
    "DistillationConfigTypeDef",
    "EndpointConfigOutputTypeDef",
    "EndpointConfigTypeDef",
    "EvaluationBedrockModelTypeDef",
    "EvaluationConfigOutputTypeDef",
    "EvaluationConfigTypeDef",
    "EvaluationDatasetLocationTypeDef",
    "EvaluationDatasetMetricConfigOutputTypeDef",
    "EvaluationDatasetMetricConfigTypeDef",
    "EvaluationDatasetMetricConfigUnionTypeDef",
    "EvaluationDatasetTypeDef",
    "EvaluationInferenceConfigOutputTypeDef",
    "EvaluationInferenceConfigTypeDef",
    "EvaluationModelConfigTypeDef",
    "EvaluationOutputDataConfigTypeDef",
    "EvaluationSummaryTypeDef",
    "EvaluatorModelConfigOutputTypeDef",
    "EvaluatorModelConfigTypeDef",
    "EvaluatorModelConfigUnionTypeDef",
    "ExternalSourceOutputTypeDef",
    "ExternalSourceTypeDef",
    "ExternalSourceUnionTypeDef",
    "ExternalSourcesGenerationConfigurationOutputTypeDef",
    "ExternalSourcesGenerationConfigurationTypeDef",
    "ExternalSourcesGenerationConfigurationUnionTypeDef",
    "ExternalSourcesRetrieveAndGenerateConfigurationOutputTypeDef",
    "ExternalSourcesRetrieveAndGenerateConfigurationTypeDef",
    "ExternalSourcesRetrieveAndGenerateConfigurationUnionTypeDef",
    "FilterAttributeOutputTypeDef",
    "FilterAttributeTypeDef",
    "FilterAttributeUnionTypeDef",
    "FoundationModelDetailsTypeDef",
    "FoundationModelLifecycleTypeDef",
    "FoundationModelSummaryTypeDef",
    "GenerationConfigurationOutputTypeDef",
    "GenerationConfigurationTypeDef",
    "GenerationConfigurationUnionTypeDef",
    "GetCustomModelRequestRequestTypeDef",
    "GetCustomModelResponseTypeDef",
    "GetEvaluationJobRequestRequestTypeDef",
    "GetEvaluationJobResponseTypeDef",
    "GetFoundationModelRequestRequestTypeDef",
    "GetFoundationModelResponseTypeDef",
    "GetGuardrailRequestRequestTypeDef",
    "GetGuardrailResponseTypeDef",
    "GetImportedModelRequestRequestTypeDef",
    "GetImportedModelResponseTypeDef",
    "GetInferenceProfileRequestRequestTypeDef",
    "GetInferenceProfileResponseTypeDef",
    "GetMarketplaceModelEndpointRequestRequestTypeDef",
    "GetMarketplaceModelEndpointResponseTypeDef",
    "GetModelCopyJobRequestRequestTypeDef",
    "GetModelCopyJobResponseTypeDef",
    "GetModelCustomizationJobRequestRequestTypeDef",
    "GetModelCustomizationJobResponseTypeDef",
    "GetModelImportJobRequestRequestTypeDef",
    "GetModelImportJobResponseTypeDef",
    "GetModelInvocationJobRequestRequestTypeDef",
    "GetModelInvocationJobResponseTypeDef",
    "GetModelInvocationLoggingConfigurationResponseTypeDef",
    "GetPromptRouterRequestRequestTypeDef",
    "GetPromptRouterResponseTypeDef",
    "GetProvisionedModelThroughputRequestRequestTypeDef",
    "GetProvisionedModelThroughputResponseTypeDef",
    "GuardrailConfigurationTypeDef",
    "GuardrailContentFilterConfigTypeDef",
    "GuardrailContentFilterTypeDef",
    "GuardrailContentPolicyConfigTypeDef",
    "GuardrailContentPolicyTypeDef",
    "GuardrailContextualGroundingFilterConfigTypeDef",
    "GuardrailContextualGroundingFilterTypeDef",
    "GuardrailContextualGroundingPolicyConfigTypeDef",
    "GuardrailContextualGroundingPolicyTypeDef",
    "GuardrailManagedWordsConfigTypeDef",
    "GuardrailManagedWordsTypeDef",
    "GuardrailPiiEntityConfigTypeDef",
    "GuardrailPiiEntityTypeDef",
    "GuardrailRegexConfigTypeDef",
    "GuardrailRegexTypeDef",
    "GuardrailSensitiveInformationPolicyConfigTypeDef",
    "GuardrailSensitiveInformationPolicyTypeDef",
    "GuardrailSummaryTypeDef",
    "GuardrailTopicConfigTypeDef",
    "GuardrailTopicPolicyConfigTypeDef",
    "GuardrailTopicPolicyTypeDef",
    "GuardrailTopicTypeDef",
    "GuardrailWordConfigTypeDef",
    "GuardrailWordPolicyConfigTypeDef",
    "GuardrailWordPolicyTypeDef",
    "GuardrailWordTypeDef",
    "HumanEvaluationConfigOutputTypeDef",
    "HumanEvaluationConfigTypeDef",
    "HumanEvaluationConfigUnionTypeDef",
    "HumanEvaluationCustomMetricTypeDef",
    "HumanWorkflowConfigTypeDef",
    "ImportedModelSummaryTypeDef",
    "InferenceProfileModelSourceTypeDef",
    "InferenceProfileModelTypeDef",
    "InferenceProfileSummaryTypeDef",
    "InvocationLogSourceTypeDef",
    "InvocationLogsConfigOutputTypeDef",
    "InvocationLogsConfigTypeDef",
    "InvocationLogsConfigUnionTypeDef",
    "KbInferenceConfigOutputTypeDef",
    "KbInferenceConfigTypeDef",
    "KbInferenceConfigUnionTypeDef",
    "KnowledgeBaseConfigOutputTypeDef",
    "KnowledgeBaseConfigTypeDef",
    "KnowledgeBaseConfigUnionTypeDef",
    "KnowledgeBaseRetrievalConfigurationOutputTypeDef",
    "KnowledgeBaseRetrievalConfigurationTypeDef",
    "KnowledgeBaseRetrievalConfigurationUnionTypeDef",
    "KnowledgeBaseRetrieveAndGenerateConfigurationOutputTypeDef",
    "KnowledgeBaseRetrieveAndGenerateConfigurationTypeDef",
    "KnowledgeBaseRetrieveAndGenerateConfigurationUnionTypeDef",
    "KnowledgeBaseVectorSearchConfigurationOutputTypeDef",
    "KnowledgeBaseVectorSearchConfigurationTypeDef",
    "KnowledgeBaseVectorSearchConfigurationUnionTypeDef",
    "ListCustomModelsRequestListCustomModelsPaginateTypeDef",
    "ListCustomModelsRequestRequestTypeDef",
    "ListCustomModelsResponseTypeDef",
    "ListEvaluationJobsRequestListEvaluationJobsPaginateTypeDef",
    "ListEvaluationJobsRequestRequestTypeDef",
    "ListEvaluationJobsResponseTypeDef",
    "ListFoundationModelsRequestRequestTypeDef",
    "ListFoundationModelsResponseTypeDef",
    "ListGuardrailsRequestListGuardrailsPaginateTypeDef",
    "ListGuardrailsRequestRequestTypeDef",
    "ListGuardrailsResponseTypeDef",
    "ListImportedModelsRequestListImportedModelsPaginateTypeDef",
    "ListImportedModelsRequestRequestTypeDef",
    "ListImportedModelsResponseTypeDef",
    "ListInferenceProfilesRequestListInferenceProfilesPaginateTypeDef",
    "ListInferenceProfilesRequestRequestTypeDef",
    "ListInferenceProfilesResponseTypeDef",
    "ListMarketplaceModelEndpointsRequestListMarketplaceModelEndpointsPaginateTypeDef",
    "ListMarketplaceModelEndpointsRequestRequestTypeDef",
    "ListMarketplaceModelEndpointsResponseTypeDef",
    "ListModelCopyJobsRequestListModelCopyJobsPaginateTypeDef",
    "ListModelCopyJobsRequestRequestTypeDef",
    "ListModelCopyJobsResponseTypeDef",
    "ListModelCustomizationJobsRequestListModelCustomizationJobsPaginateTypeDef",
    "ListModelCustomizationJobsRequestRequestTypeDef",
    "ListModelCustomizationJobsResponseTypeDef",
    "ListModelImportJobsRequestListModelImportJobsPaginateTypeDef",
    "ListModelImportJobsRequestRequestTypeDef",
    "ListModelImportJobsResponseTypeDef",
    "ListModelInvocationJobsRequestListModelInvocationJobsPaginateTypeDef",
    "ListModelInvocationJobsRequestRequestTypeDef",
    "ListModelInvocationJobsResponseTypeDef",
    "ListPromptRoutersRequestListPromptRoutersPaginateTypeDef",
    "ListPromptRoutersRequestRequestTypeDef",
    "ListPromptRoutersResponseTypeDef",
    "ListProvisionedModelThroughputsRequestListProvisionedModelThroughputsPaginateTypeDef",
    "ListProvisionedModelThroughputsRequestRequestTypeDef",
    "ListProvisionedModelThroughputsResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "LoggingConfigTypeDef",
    "MarketplaceModelEndpointSummaryTypeDef",
    "MarketplaceModelEndpointTypeDef",
    "ModelCopyJobSummaryTypeDef",
    "ModelCustomizationJobSummaryTypeDef",
    "ModelDataSourceTypeDef",
    "ModelImportJobSummaryTypeDef",
    "ModelInvocationJobInputDataConfigTypeDef",
    "ModelInvocationJobOutputDataConfigTypeDef",
    "ModelInvocationJobS3InputDataConfigTypeDef",
    "ModelInvocationJobS3OutputDataConfigTypeDef",
    "ModelInvocationJobSummaryTypeDef",
    "OrchestrationConfigurationTypeDef",
    "OutputDataConfigTypeDef",
    "PaginatorConfigTypeDef",
    "PromptRouterSummaryTypeDef",
    "PromptRouterTargetModelTypeDef",
    "PromptTemplateTypeDef",
    "ProvisionedModelSummaryTypeDef",
    "PutModelInvocationLoggingConfigurationRequestRequestTypeDef",
    "QueryTransformationConfigurationTypeDef",
    "RAGConfigOutputTypeDef",
    "RAGConfigTypeDef",
    "RAGConfigUnionTypeDef",
    "RegisterMarketplaceModelEndpointRequestRequestTypeDef",
    "RegisterMarketplaceModelEndpointResponseTypeDef",
    "RequestMetadataBaseFiltersOutputTypeDef",
    "RequestMetadataBaseFiltersTypeDef",
    "RequestMetadataBaseFiltersUnionTypeDef",
    "RequestMetadataFiltersOutputTypeDef",
    "RequestMetadataFiltersTypeDef",
    "RequestMetadataFiltersUnionTypeDef",
    "ResponseMetadataTypeDef",
    "RetrievalFilterOutputTypeDef",
    "RetrievalFilterTypeDef",
    "RetrievalFilterUnionTypeDef",
    "RetrieveAndGenerateConfigurationOutputTypeDef",
    "RetrieveAndGenerateConfigurationTypeDef",
    "RetrieveAndGenerateConfigurationUnionTypeDef",
    "RetrieveConfigOutputTypeDef",
    "RetrieveConfigTypeDef",
    "RetrieveConfigUnionTypeDef",
    "RoutingCriteriaTypeDef",
    "S3ConfigTypeDef",
    "S3DataSourceTypeDef",
    "S3ObjectDocTypeDef",
    "SageMakerEndpointOutputTypeDef",
    "SageMakerEndpointTypeDef",
    "SageMakerEndpointUnionTypeDef",
    "StopEvaluationJobRequestRequestTypeDef",
    "StopModelCustomizationJobRequestRequestTypeDef",
    "StopModelInvocationJobRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagTypeDef",
    "TeacherModelConfigTypeDef",
    "TextInferenceConfigOutputTypeDef",
    "TextInferenceConfigTypeDef",
    "TextInferenceConfigUnionTypeDef",
    "TimestampTypeDef",
    "TrainingDataConfigOutputTypeDef",
    "TrainingDataConfigTypeDef",
    "TrainingMetricsTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateGuardrailRequestRequestTypeDef",
    "UpdateGuardrailResponseTypeDef",
    "UpdateMarketplaceModelEndpointRequestRequestTypeDef",
    "UpdateMarketplaceModelEndpointResponseTypeDef",
    "UpdateProvisionedModelThroughputRequestRequestTypeDef",
    "ValidationDataConfigOutputTypeDef",
    "ValidationDataConfigTypeDef",
    "ValidatorMetricTypeDef",
    "ValidatorTypeDef",
    "VpcConfigOutputTypeDef",
    "VpcConfigTypeDef",
    "VpcConfigUnionTypeDef",
)


class BatchDeleteEvaluationJobErrorTypeDef(TypedDict):
    jobIdentifier: str
    code: str
    message: NotRequired[str]


class BatchDeleteEvaluationJobItemTypeDef(TypedDict):
    jobIdentifier: str
    jobStatus: EvaluationJobStatusType


class BatchDeleteEvaluationJobRequestRequestTypeDef(TypedDict):
    jobIdentifiers: Sequence[str]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class BedrockEvaluatorModelTypeDef(TypedDict):
    modelIdentifier: str


BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]


class ByteContentDocOutputTypeDef(TypedDict):
    identifier: str
    contentType: str
    data: bytes


class S3ConfigTypeDef(TypedDict):
    bucketName: str
    keyPrefix: NotRequired[str]


class EvaluationOutputDataConfigTypeDef(TypedDict):
    s3Uri: str


class TagTypeDef(TypedDict):
    key: str
    value: str


class CreateGuardrailVersionRequestRequestTypeDef(TypedDict):
    guardrailIdentifier: str
    description: NotRequired[str]
    clientRequestToken: NotRequired[str]


class InferenceProfileModelSourceTypeDef(TypedDict):
    copyFrom: NotRequired[str]


class OutputDataConfigTypeDef(TypedDict):
    s3Uri: str


class VpcConfigTypeDef(TypedDict):
    subnetIds: Sequence[str]
    securityGroupIds: Sequence[str]


class CustomModelSummaryTypeDef(TypedDict):
    modelArn: str
    modelName: str
    creationTime: datetime
    baseModelArn: str
    baseModelName: str
    customizationType: NotRequired[CustomizationTypeType]
    ownerAccountId: NotRequired[str]


class DeleteCustomModelRequestRequestTypeDef(TypedDict):
    modelIdentifier: str


class DeleteGuardrailRequestRequestTypeDef(TypedDict):
    guardrailIdentifier: str
    guardrailVersion: NotRequired[str]


class DeleteImportedModelRequestRequestTypeDef(TypedDict):
    modelIdentifier: str


class DeleteInferenceProfileRequestRequestTypeDef(TypedDict):
    inferenceProfileIdentifier: str


class DeleteMarketplaceModelEndpointRequestRequestTypeDef(TypedDict):
    endpointArn: str


class DeleteProvisionedModelThroughputRequestRequestTypeDef(TypedDict):
    provisionedModelId: str


class DeregisterMarketplaceModelEndpointRequestRequestTypeDef(TypedDict):
    endpointArn: str


class TeacherModelConfigTypeDef(TypedDict):
    teacherModelIdentifier: str
    maxResponseLengthForInference: NotRequired[int]


class EvaluationBedrockModelTypeDef(TypedDict):
    modelIdentifier: str
    inferenceParams: NotRequired[str]


class EvaluationDatasetLocationTypeDef(TypedDict):
    s3Uri: NotRequired[str]


class EvaluationSummaryTypeDef(TypedDict):
    jobArn: str
    jobName: str
    status: EvaluationJobStatusType
    creationTime: datetime
    jobType: EvaluationJobTypeType
    evaluationTaskTypes: List[EvaluationTaskTypeType]
    modelIdentifiers: NotRequired[List[str]]
    ragIdentifiers: NotRequired[List[str]]
    evaluatorModelIdentifiers: NotRequired[List[str]]
    applicationType: NotRequired[ApplicationTypeType]


class S3ObjectDocTypeDef(TypedDict):
    uri: str


class GuardrailConfigurationTypeDef(TypedDict):
    guardrailId: str
    guardrailVersion: str


class PromptTemplateTypeDef(TypedDict):
    textPromptTemplate: NotRequired[str]


class FilterAttributeOutputTypeDef(TypedDict):
    key: str
    value: Dict[str, Any]


class FilterAttributeTypeDef(TypedDict):
    key: str
    value: Mapping[str, Any]


class FoundationModelLifecycleTypeDef(TypedDict):
    status: FoundationModelLifecycleStatusType


class GetCustomModelRequestRequestTypeDef(TypedDict):
    modelIdentifier: str


class TrainingMetricsTypeDef(TypedDict):
    trainingLoss: NotRequired[float]


class ValidatorMetricTypeDef(TypedDict):
    validationLoss: NotRequired[float]


class GetEvaluationJobRequestRequestTypeDef(TypedDict):
    jobIdentifier: str


class GetFoundationModelRequestRequestTypeDef(TypedDict):
    modelIdentifier: str


class GetGuardrailRequestRequestTypeDef(TypedDict):
    guardrailIdentifier: str
    guardrailVersion: NotRequired[str]


class GetImportedModelRequestRequestTypeDef(TypedDict):
    modelIdentifier: str


class GetInferenceProfileRequestRequestTypeDef(TypedDict):
    inferenceProfileIdentifier: str


class InferenceProfileModelTypeDef(TypedDict):
    modelArn: NotRequired[str]


class GetMarketplaceModelEndpointRequestRequestTypeDef(TypedDict):
    endpointArn: str


class GetModelCopyJobRequestRequestTypeDef(TypedDict):
    jobArn: str


class GetModelCustomizationJobRequestRequestTypeDef(TypedDict):
    jobIdentifier: str


class VpcConfigOutputTypeDef(TypedDict):
    subnetIds: List[str]
    securityGroupIds: List[str]


class GetModelImportJobRequestRequestTypeDef(TypedDict):
    jobIdentifier: str


class GetModelInvocationJobRequestRequestTypeDef(TypedDict):
    jobIdentifier: str


class GetPromptRouterRequestRequestTypeDef(TypedDict):
    promptRouterArn: str


class PromptRouterTargetModelTypeDef(TypedDict):
    modelArn: NotRequired[str]


class RoutingCriteriaTypeDef(TypedDict):
    responseQualityDifference: float


class GetProvisionedModelThroughputRequestRequestTypeDef(TypedDict):
    provisionedModelId: str


GuardrailContentFilterConfigTypeDef = TypedDict(
    "GuardrailContentFilterConfigTypeDef",
    {
        "type": GuardrailContentFilterTypeType,
        "inputStrength": GuardrailFilterStrengthType,
        "outputStrength": GuardrailFilterStrengthType,
        "inputModalities": NotRequired[Sequence[GuardrailModalityType]],
        "outputModalities": NotRequired[Sequence[GuardrailModalityType]],
    },
)
GuardrailContentFilterTypeDef = TypedDict(
    "GuardrailContentFilterTypeDef",
    {
        "type": GuardrailContentFilterTypeType,
        "inputStrength": GuardrailFilterStrengthType,
        "outputStrength": GuardrailFilterStrengthType,
        "inputModalities": NotRequired[List[GuardrailModalityType]],
        "outputModalities": NotRequired[List[GuardrailModalityType]],
    },
)
GuardrailContextualGroundingFilterConfigTypeDef = TypedDict(
    "GuardrailContextualGroundingFilterConfigTypeDef",
    {
        "type": GuardrailContextualGroundingFilterTypeType,
        "threshold": float,
    },
)
GuardrailContextualGroundingFilterTypeDef = TypedDict(
    "GuardrailContextualGroundingFilterTypeDef",
    {
        "type": GuardrailContextualGroundingFilterTypeType,
        "threshold": float,
    },
)
GuardrailManagedWordsConfigTypeDef = TypedDict(
    "GuardrailManagedWordsConfigTypeDef",
    {
        "type": Literal["PROFANITY"],
    },
)
GuardrailManagedWordsTypeDef = TypedDict(
    "GuardrailManagedWordsTypeDef",
    {
        "type": Literal["PROFANITY"],
    },
)
GuardrailPiiEntityConfigTypeDef = TypedDict(
    "GuardrailPiiEntityConfigTypeDef",
    {
        "type": GuardrailPiiEntityTypeType,
        "action": GuardrailSensitiveInformationActionType,
    },
)
GuardrailPiiEntityTypeDef = TypedDict(
    "GuardrailPiiEntityTypeDef",
    {
        "type": GuardrailPiiEntityTypeType,
        "action": GuardrailSensitiveInformationActionType,
    },
)


class GuardrailRegexConfigTypeDef(TypedDict):
    name: str
    pattern: str
    action: GuardrailSensitiveInformationActionType
    description: NotRequired[str]


class GuardrailRegexTypeDef(TypedDict):
    name: str
    pattern: str
    action: GuardrailSensitiveInformationActionType
    description: NotRequired[str]


GuardrailSummaryTypeDef = TypedDict(
    "GuardrailSummaryTypeDef",
    {
        "id": str,
        "arn": str,
        "status": GuardrailStatusType,
        "name": str,
        "version": str,
        "createdAt": datetime,
        "updatedAt": datetime,
        "description": NotRequired[str],
    },
)
GuardrailTopicConfigTypeDef = TypedDict(
    "GuardrailTopicConfigTypeDef",
    {
        "name": str,
        "definition": str,
        "type": Literal["DENY"],
        "examples": NotRequired[Sequence[str]],
    },
)
GuardrailTopicTypeDef = TypedDict(
    "GuardrailTopicTypeDef",
    {
        "name": str,
        "definition": str,
        "examples": NotRequired[List[str]],
        "type": NotRequired[Literal["DENY"]],
    },
)


class GuardrailWordConfigTypeDef(TypedDict):
    text: str


class GuardrailWordTypeDef(TypedDict):
    text: str


class HumanEvaluationCustomMetricTypeDef(TypedDict):
    name: str
    ratingMethod: str
    description: NotRequired[str]


class HumanWorkflowConfigTypeDef(TypedDict):
    flowDefinitionArn: str
    instructions: NotRequired[str]


class ImportedModelSummaryTypeDef(TypedDict):
    modelArn: str
    modelName: str
    creationTime: datetime
    instructSupported: NotRequired[bool]
    modelArchitecture: NotRequired[str]


class InvocationLogSourceTypeDef(TypedDict):
    s3Uri: NotRequired[str]


class TextInferenceConfigOutputTypeDef(TypedDict):
    temperature: NotRequired[float]
    topP: NotRequired[float]
    maxTokens: NotRequired[int]
    stopSequences: NotRequired[List[str]]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


TimestampTypeDef = Union[datetime, str]


class ListFoundationModelsRequestRequestTypeDef(TypedDict):
    byProvider: NotRequired[str]
    byCustomizationType: NotRequired[ModelCustomizationType]
    byOutputModality: NotRequired[ModelModalityType]
    byInferenceType: NotRequired[InferenceTypeType]


class ListGuardrailsRequestRequestTypeDef(TypedDict):
    guardrailIdentifier: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListInferenceProfilesRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    typeEquals: NotRequired[InferenceProfileTypeType]


class ListMarketplaceModelEndpointsRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    modelSourceEquals: NotRequired[str]


class MarketplaceModelEndpointSummaryTypeDef(TypedDict):
    endpointArn: str
    modelSourceIdentifier: str
    createdAt: datetime
    updatedAt: datetime
    status: NotRequired[StatusType]
    statusMessage: NotRequired[str]


class ModelCustomizationJobSummaryTypeDef(TypedDict):
    jobArn: str
    baseModelArn: str
    jobName: str
    status: ModelCustomizationJobStatusType
    creationTime: datetime
    lastModifiedTime: NotRequired[datetime]
    endTime: NotRequired[datetime]
    customModelArn: NotRequired[str]
    customModelName: NotRequired[str]
    customizationType: NotRequired[CustomizationTypeType]


class ModelImportJobSummaryTypeDef(TypedDict):
    jobArn: str
    jobName: str
    status: ModelImportJobStatusType
    creationTime: datetime
    lastModifiedTime: NotRequired[datetime]
    endTime: NotRequired[datetime]
    importedModelArn: NotRequired[str]
    importedModelName: NotRequired[str]


class ListPromptRoutersRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ProvisionedModelSummaryTypeDef(TypedDict):
    provisionedModelName: str
    provisionedModelArn: str
    modelArn: str
    desiredModelArn: str
    foundationModelArn: str
    modelUnits: int
    desiredModelUnits: int
    status: ProvisionedModelStatusType
    creationTime: datetime
    lastModifiedTime: datetime
    commitmentDuration: NotRequired[CommitmentDurationType]
    commitmentExpirationTime: NotRequired[datetime]


class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    resourceARN: str


class S3DataSourceTypeDef(TypedDict):
    s3Uri: str


class ModelInvocationJobS3InputDataConfigTypeDef(TypedDict):
    s3Uri: str
    s3InputFormat: NotRequired[Literal["JSONL"]]
    s3BucketOwner: NotRequired[str]


class ModelInvocationJobS3OutputDataConfigTypeDef(TypedDict):
    s3Uri: str
    s3EncryptionKeyId: NotRequired[str]
    s3BucketOwner: NotRequired[str]


QueryTransformationConfigurationTypeDef = TypedDict(
    "QueryTransformationConfigurationTypeDef",
    {
        "type": Literal["QUERY_DECOMPOSITION"],
    },
)


class RegisterMarketplaceModelEndpointRequestRequestTypeDef(TypedDict):
    endpointIdentifier: str
    modelSourceIdentifier: str


class RequestMetadataBaseFiltersOutputTypeDef(TypedDict):
    equals: NotRequired[Dict[str, str]]
    notEquals: NotRequired[Dict[str, str]]


class RequestMetadataBaseFiltersTypeDef(TypedDict):
    equals: NotRequired[Mapping[str, str]]
    notEquals: NotRequired[Mapping[str, str]]


class StopEvaluationJobRequestRequestTypeDef(TypedDict):
    jobIdentifier: str


class StopModelCustomizationJobRequestRequestTypeDef(TypedDict):
    jobIdentifier: str


class StopModelInvocationJobRequestRequestTypeDef(TypedDict):
    jobIdentifier: str


class TextInferenceConfigTypeDef(TypedDict):
    temperature: NotRequired[float]
    topP: NotRequired[float]
    maxTokens: NotRequired[int]
    stopSequences: NotRequired[Sequence[str]]


class UntagResourceRequestRequestTypeDef(TypedDict):
    resourceARN: str
    tagKeys: Sequence[str]


class UpdateProvisionedModelThroughputRequestRequestTypeDef(TypedDict):
    provisionedModelId: str
    desiredProvisionedModelName: NotRequired[str]
    desiredModelId: NotRequired[str]


class ValidatorTypeDef(TypedDict):
    s3Uri: str


class BatchDeleteEvaluationJobResponseTypeDef(TypedDict):
    errors: List[BatchDeleteEvaluationJobErrorTypeDef]
    evaluationJobs: List[BatchDeleteEvaluationJobItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateEvaluationJobResponseTypeDef(TypedDict):
    jobArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateGuardrailResponseTypeDef(TypedDict):
    guardrailId: str
    guardrailArn: str
    version: str
    createdAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class CreateGuardrailVersionResponseTypeDef(TypedDict):
    guardrailId: str
    version: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateInferenceProfileResponseTypeDef(TypedDict):
    inferenceProfileArn: str
    status: Literal["ACTIVE"]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateModelCopyJobResponseTypeDef(TypedDict):
    jobArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateModelCustomizationJobResponseTypeDef(TypedDict):
    jobArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateModelImportJobResponseTypeDef(TypedDict):
    jobArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateModelInvocationJobResponseTypeDef(TypedDict):
    jobArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateProvisionedModelThroughputResponseTypeDef(TypedDict):
    provisionedModelArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetProvisionedModelThroughputResponseTypeDef(TypedDict):
    modelUnits: int
    desiredModelUnits: int
    provisionedModelName: str
    provisionedModelArn: str
    modelArn: str
    desiredModelArn: str
    foundationModelArn: str
    status: ProvisionedModelStatusType
    creationTime: datetime
    lastModifiedTime: datetime
    failureMessage: str
    commitmentDuration: CommitmentDurationType
    commitmentExpirationTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateGuardrailResponseTypeDef(TypedDict):
    guardrailId: str
    guardrailArn: str
    version: str
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class EvaluatorModelConfigOutputTypeDef(TypedDict):
    bedrockEvaluatorModels: NotRequired[List[BedrockEvaluatorModelTypeDef]]


class EvaluatorModelConfigTypeDef(TypedDict):
    bedrockEvaluatorModels: NotRequired[Sequence[BedrockEvaluatorModelTypeDef]]


class ByteContentDocTypeDef(TypedDict):
    identifier: str
    contentType: str
    data: BlobTypeDef


class CloudWatchConfigTypeDef(TypedDict):
    logGroupName: str
    roleArn: str
    largeDataDeliveryS3Config: NotRequired[S3ConfigTypeDef]


class CreateModelCopyJobRequestRequestTypeDef(TypedDict):
    sourceModelArn: str
    targetModelName: str
    modelKmsKeyId: NotRequired[str]
    targetModelTags: NotRequired[Sequence[TagTypeDef]]
    clientRequestToken: NotRequired[str]


class CreateProvisionedModelThroughputRequestRequestTypeDef(TypedDict):
    modelUnits: int
    provisionedModelName: str
    modelId: str
    clientRequestToken: NotRequired[str]
    commitmentDuration: NotRequired[CommitmentDurationType]
    tags: NotRequired[Sequence[TagTypeDef]]


class GetModelCopyJobResponseTypeDef(TypedDict):
    jobArn: str
    status: ModelCopyJobStatusType
    creationTime: datetime
    targetModelArn: str
    targetModelName: str
    sourceAccountId: str
    sourceModelArn: str
    targetModelKmsKeyArn: str
    targetModelTags: List[TagTypeDef]
    failureMessage: str
    sourceModelName: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ModelCopyJobSummaryTypeDef(TypedDict):
    jobArn: str
    status: ModelCopyJobStatusType
    creationTime: datetime
    targetModelArn: str
    sourceAccountId: str
    sourceModelArn: str
    targetModelName: NotRequired[str]
    targetModelKmsKeyArn: NotRequired[str]
    targetModelTags: NotRequired[List[TagTypeDef]]
    failureMessage: NotRequired[str]
    sourceModelName: NotRequired[str]


class TagResourceRequestRequestTypeDef(TypedDict):
    resourceARN: str
    tags: Sequence[TagTypeDef]


class CreateInferenceProfileRequestRequestTypeDef(TypedDict):
    inferenceProfileName: str
    modelSource: InferenceProfileModelSourceTypeDef
    description: NotRequired[str]
    clientRequestToken: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]


class ListCustomModelsResponseTypeDef(TypedDict):
    modelSummaries: List[CustomModelSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class DistillationConfigTypeDef(TypedDict):
    teacherModelConfig: TeacherModelConfigTypeDef


class EvaluationModelConfigTypeDef(TypedDict):
    bedrockModel: NotRequired[EvaluationBedrockModelTypeDef]


class EvaluationDatasetTypeDef(TypedDict):
    name: str
    datasetLocation: NotRequired[EvaluationDatasetLocationTypeDef]


class ListEvaluationJobsResponseTypeDef(TypedDict):
    jobSummaries: List[EvaluationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ExternalSourceOutputTypeDef(TypedDict):
    sourceType: ExternalSourceTypeType
    s3Location: NotRequired[S3ObjectDocTypeDef]
    byteContent: NotRequired[ByteContentDocOutputTypeDef]


RetrievalFilterOutputTypeDef = TypedDict(
    "RetrievalFilterOutputTypeDef",
    {
        "equals": NotRequired[FilterAttributeOutputTypeDef],
        "notEquals": NotRequired[FilterAttributeOutputTypeDef],
        "greaterThan": NotRequired[FilterAttributeOutputTypeDef],
        "greaterThanOrEquals": NotRequired[FilterAttributeOutputTypeDef],
        "lessThan": NotRequired[FilterAttributeOutputTypeDef],
        "lessThanOrEquals": NotRequired[FilterAttributeOutputTypeDef],
        "in": NotRequired[FilterAttributeOutputTypeDef],
        "notIn": NotRequired[FilterAttributeOutputTypeDef],
        "startsWith": NotRequired[FilterAttributeOutputTypeDef],
        "listContains": NotRequired[FilterAttributeOutputTypeDef],
        "stringContains": NotRequired[FilterAttributeOutputTypeDef],
        "andAll": NotRequired[List[Dict[str, Any]]],
        "orAll": NotRequired[List[Dict[str, Any]]],
    },
)
FilterAttributeUnionTypeDef = Union[FilterAttributeTypeDef, FilterAttributeOutputTypeDef]


class FoundationModelDetailsTypeDef(TypedDict):
    modelArn: str
    modelId: str
    modelName: NotRequired[str]
    providerName: NotRequired[str]
    inputModalities: NotRequired[List[ModelModalityType]]
    outputModalities: NotRequired[List[ModelModalityType]]
    responseStreamingSupported: NotRequired[bool]
    customizationsSupported: NotRequired[List[ModelCustomizationType]]
    inferenceTypesSupported: NotRequired[List[InferenceTypeType]]
    modelLifecycle: NotRequired[FoundationModelLifecycleTypeDef]


class FoundationModelSummaryTypeDef(TypedDict):
    modelArn: str
    modelId: str
    modelName: NotRequired[str]
    providerName: NotRequired[str]
    inputModalities: NotRequired[List[ModelModalityType]]
    outputModalities: NotRequired[List[ModelModalityType]]
    responseStreamingSupported: NotRequired[bool]
    customizationsSupported: NotRequired[List[ModelCustomizationType]]
    inferenceTypesSupported: NotRequired[List[InferenceTypeType]]
    modelLifecycle: NotRequired[FoundationModelLifecycleTypeDef]


GetInferenceProfileResponseTypeDef = TypedDict(
    "GetInferenceProfileResponseTypeDef",
    {
        "inferenceProfileName": str,
        "description": str,
        "createdAt": datetime,
        "updatedAt": datetime,
        "inferenceProfileArn": str,
        "models": List[InferenceProfileModelTypeDef],
        "inferenceProfileId": str,
        "status": Literal["ACTIVE"],
        "type": InferenceProfileTypeType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
InferenceProfileSummaryTypeDef = TypedDict(
    "InferenceProfileSummaryTypeDef",
    {
        "inferenceProfileName": str,
        "inferenceProfileArn": str,
        "models": List[InferenceProfileModelTypeDef],
        "inferenceProfileId": str,
        "status": Literal["ACTIVE"],
        "type": InferenceProfileTypeType,
        "description": NotRequired[str],
        "createdAt": NotRequired[datetime],
        "updatedAt": NotRequired[datetime],
    },
)


class SageMakerEndpointOutputTypeDef(TypedDict):
    initialInstanceCount: int
    instanceType: str
    executionRole: str
    kmsEncryptionKey: NotRequired[str]
    vpc: NotRequired[VpcConfigOutputTypeDef]


VpcConfigUnionTypeDef = Union[VpcConfigTypeDef, VpcConfigOutputTypeDef]
GetPromptRouterResponseTypeDef = TypedDict(
    "GetPromptRouterResponseTypeDef",
    {
        "promptRouterName": str,
        "routingCriteria": RoutingCriteriaTypeDef,
        "description": str,
        "createdAt": datetime,
        "updatedAt": datetime,
        "promptRouterArn": str,
        "models": List[PromptRouterTargetModelTypeDef],
        "fallbackModel": PromptRouterTargetModelTypeDef,
        "status": Literal["AVAILABLE"],
        "type": PromptRouterTypeType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
PromptRouterSummaryTypeDef = TypedDict(
    "PromptRouterSummaryTypeDef",
    {
        "promptRouterName": str,
        "routingCriteria": RoutingCriteriaTypeDef,
        "promptRouterArn": str,
        "models": List[PromptRouterTargetModelTypeDef],
        "fallbackModel": PromptRouterTargetModelTypeDef,
        "status": Literal["AVAILABLE"],
        "type": PromptRouterTypeType,
        "description": NotRequired[str],
        "createdAt": NotRequired[datetime],
        "updatedAt": NotRequired[datetime],
    },
)


class GuardrailContentPolicyConfigTypeDef(TypedDict):
    filtersConfig: Sequence[GuardrailContentFilterConfigTypeDef]


class GuardrailContentPolicyTypeDef(TypedDict):
    filters: NotRequired[List[GuardrailContentFilterTypeDef]]


class GuardrailContextualGroundingPolicyConfigTypeDef(TypedDict):
    filtersConfig: Sequence[GuardrailContextualGroundingFilterConfigTypeDef]


class GuardrailContextualGroundingPolicyTypeDef(TypedDict):
    filters: List[GuardrailContextualGroundingFilterTypeDef]


class GuardrailSensitiveInformationPolicyConfigTypeDef(TypedDict):
    piiEntitiesConfig: NotRequired[Sequence[GuardrailPiiEntityConfigTypeDef]]
    regexesConfig: NotRequired[Sequence[GuardrailRegexConfigTypeDef]]


class GuardrailSensitiveInformationPolicyTypeDef(TypedDict):
    piiEntities: NotRequired[List[GuardrailPiiEntityTypeDef]]
    regexes: NotRequired[List[GuardrailRegexTypeDef]]


class ListGuardrailsResponseTypeDef(TypedDict):
    guardrails: List[GuardrailSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class GuardrailTopicPolicyConfigTypeDef(TypedDict):
    topicsConfig: Sequence[GuardrailTopicConfigTypeDef]


class GuardrailTopicPolicyTypeDef(TypedDict):
    topics: List[GuardrailTopicTypeDef]


class GuardrailWordPolicyConfigTypeDef(TypedDict):
    wordsConfig: NotRequired[Sequence[GuardrailWordConfigTypeDef]]
    managedWordListsConfig: NotRequired[Sequence[GuardrailManagedWordsConfigTypeDef]]


class GuardrailWordPolicyTypeDef(TypedDict):
    words: NotRequired[List[GuardrailWordTypeDef]]
    managedWordLists: NotRequired[List[GuardrailManagedWordsTypeDef]]


class ListImportedModelsResponseTypeDef(TypedDict):
    modelSummaries: List[ImportedModelSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class KbInferenceConfigOutputTypeDef(TypedDict):
    textInferenceConfig: NotRequired[TextInferenceConfigOutputTypeDef]


class ListGuardrailsRequestListGuardrailsPaginateTypeDef(TypedDict):
    guardrailIdentifier: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListInferenceProfilesRequestListInferenceProfilesPaginateTypeDef(TypedDict):
    typeEquals: NotRequired[InferenceProfileTypeType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListMarketplaceModelEndpointsRequestListMarketplaceModelEndpointsPaginateTypeDef(TypedDict):
    modelSourceEquals: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListPromptRoutersRequestListPromptRoutersPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListCustomModelsRequestListCustomModelsPaginateTypeDef(TypedDict):
    creationTimeBefore: NotRequired[TimestampTypeDef]
    creationTimeAfter: NotRequired[TimestampTypeDef]
    nameContains: NotRequired[str]
    baseModelArnEquals: NotRequired[str]
    foundationModelArnEquals: NotRequired[str]
    sortBy: NotRequired[Literal["CreationTime"]]
    sortOrder: NotRequired[SortOrderType]
    isOwned: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListCustomModelsRequestRequestTypeDef(TypedDict):
    creationTimeBefore: NotRequired[TimestampTypeDef]
    creationTimeAfter: NotRequired[TimestampTypeDef]
    nameContains: NotRequired[str]
    baseModelArnEquals: NotRequired[str]
    foundationModelArnEquals: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    sortBy: NotRequired[Literal["CreationTime"]]
    sortOrder: NotRequired[SortOrderType]
    isOwned: NotRequired[bool]


class ListEvaluationJobsRequestListEvaluationJobsPaginateTypeDef(TypedDict):
    creationTimeAfter: NotRequired[TimestampTypeDef]
    creationTimeBefore: NotRequired[TimestampTypeDef]
    statusEquals: NotRequired[EvaluationJobStatusType]
    applicationTypeEquals: NotRequired[ApplicationTypeType]
    nameContains: NotRequired[str]
    sortBy: NotRequired[Literal["CreationTime"]]
    sortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListEvaluationJobsRequestRequestTypeDef(TypedDict):
    creationTimeAfter: NotRequired[TimestampTypeDef]
    creationTimeBefore: NotRequired[TimestampTypeDef]
    statusEquals: NotRequired[EvaluationJobStatusType]
    applicationTypeEquals: NotRequired[ApplicationTypeType]
    nameContains: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    sortBy: NotRequired[Literal["CreationTime"]]
    sortOrder: NotRequired[SortOrderType]


class ListImportedModelsRequestListImportedModelsPaginateTypeDef(TypedDict):
    creationTimeBefore: NotRequired[TimestampTypeDef]
    creationTimeAfter: NotRequired[TimestampTypeDef]
    nameContains: NotRequired[str]
    sortBy: NotRequired[Literal["CreationTime"]]
    sortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListImportedModelsRequestRequestTypeDef(TypedDict):
    creationTimeBefore: NotRequired[TimestampTypeDef]
    creationTimeAfter: NotRequired[TimestampTypeDef]
    nameContains: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    sortBy: NotRequired[Literal["CreationTime"]]
    sortOrder: NotRequired[SortOrderType]


class ListModelCopyJobsRequestListModelCopyJobsPaginateTypeDef(TypedDict):
    creationTimeAfter: NotRequired[TimestampTypeDef]
    creationTimeBefore: NotRequired[TimestampTypeDef]
    statusEquals: NotRequired[ModelCopyJobStatusType]
    sourceAccountEquals: NotRequired[str]
    sourceModelArnEquals: NotRequired[str]
    targetModelNameContains: NotRequired[str]
    sortBy: NotRequired[Literal["CreationTime"]]
    sortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListModelCopyJobsRequestRequestTypeDef(TypedDict):
    creationTimeAfter: NotRequired[TimestampTypeDef]
    creationTimeBefore: NotRequired[TimestampTypeDef]
    statusEquals: NotRequired[ModelCopyJobStatusType]
    sourceAccountEquals: NotRequired[str]
    sourceModelArnEquals: NotRequired[str]
    targetModelNameContains: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    sortBy: NotRequired[Literal["CreationTime"]]
    sortOrder: NotRequired[SortOrderType]


class ListModelCustomizationJobsRequestListModelCustomizationJobsPaginateTypeDef(TypedDict):
    creationTimeAfter: NotRequired[TimestampTypeDef]
    creationTimeBefore: NotRequired[TimestampTypeDef]
    statusEquals: NotRequired[FineTuningJobStatusType]
    nameContains: NotRequired[str]
    sortBy: NotRequired[Literal["CreationTime"]]
    sortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListModelCustomizationJobsRequestRequestTypeDef(TypedDict):
    creationTimeAfter: NotRequired[TimestampTypeDef]
    creationTimeBefore: NotRequired[TimestampTypeDef]
    statusEquals: NotRequired[FineTuningJobStatusType]
    nameContains: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    sortBy: NotRequired[Literal["CreationTime"]]
    sortOrder: NotRequired[SortOrderType]


class ListModelImportJobsRequestListModelImportJobsPaginateTypeDef(TypedDict):
    creationTimeAfter: NotRequired[TimestampTypeDef]
    creationTimeBefore: NotRequired[TimestampTypeDef]
    statusEquals: NotRequired[ModelImportJobStatusType]
    nameContains: NotRequired[str]
    sortBy: NotRequired[Literal["CreationTime"]]
    sortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListModelImportJobsRequestRequestTypeDef(TypedDict):
    creationTimeAfter: NotRequired[TimestampTypeDef]
    creationTimeBefore: NotRequired[TimestampTypeDef]
    statusEquals: NotRequired[ModelImportJobStatusType]
    nameContains: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    sortBy: NotRequired[Literal["CreationTime"]]
    sortOrder: NotRequired[SortOrderType]


class ListModelInvocationJobsRequestListModelInvocationJobsPaginateTypeDef(TypedDict):
    submitTimeAfter: NotRequired[TimestampTypeDef]
    submitTimeBefore: NotRequired[TimestampTypeDef]
    statusEquals: NotRequired[ModelInvocationJobStatusType]
    nameContains: NotRequired[str]
    sortBy: NotRequired[Literal["CreationTime"]]
    sortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListModelInvocationJobsRequestRequestTypeDef(TypedDict):
    submitTimeAfter: NotRequired[TimestampTypeDef]
    submitTimeBefore: NotRequired[TimestampTypeDef]
    statusEquals: NotRequired[ModelInvocationJobStatusType]
    nameContains: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    sortBy: NotRequired[Literal["CreationTime"]]
    sortOrder: NotRequired[SortOrderType]


class ListProvisionedModelThroughputsRequestListProvisionedModelThroughputsPaginateTypeDef(
    TypedDict
):
    creationTimeAfter: NotRequired[TimestampTypeDef]
    creationTimeBefore: NotRequired[TimestampTypeDef]
    statusEquals: NotRequired[ProvisionedModelStatusType]
    modelArnEquals: NotRequired[str]
    nameContains: NotRequired[str]
    sortBy: NotRequired[Literal["CreationTime"]]
    sortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListProvisionedModelThroughputsRequestRequestTypeDef(TypedDict):
    creationTimeAfter: NotRequired[TimestampTypeDef]
    creationTimeBefore: NotRequired[TimestampTypeDef]
    statusEquals: NotRequired[ProvisionedModelStatusType]
    modelArnEquals: NotRequired[str]
    nameContains: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    sortBy: NotRequired[Literal["CreationTime"]]
    sortOrder: NotRequired[SortOrderType]


class ListMarketplaceModelEndpointsResponseTypeDef(TypedDict):
    marketplaceModelEndpoints: List[MarketplaceModelEndpointSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListModelCustomizationJobsResponseTypeDef(TypedDict):
    modelCustomizationJobSummaries: List[ModelCustomizationJobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListModelImportJobsResponseTypeDef(TypedDict):
    modelImportJobSummaries: List[ModelImportJobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListProvisionedModelThroughputsResponseTypeDef(TypedDict):
    provisionedModelSummaries: List[ProvisionedModelSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ModelDataSourceTypeDef(TypedDict):
    s3DataSource: NotRequired[S3DataSourceTypeDef]


class ModelInvocationJobInputDataConfigTypeDef(TypedDict):
    s3InputDataConfig: NotRequired[ModelInvocationJobS3InputDataConfigTypeDef]


class ModelInvocationJobOutputDataConfigTypeDef(TypedDict):
    s3OutputDataConfig: NotRequired[ModelInvocationJobS3OutputDataConfigTypeDef]


class OrchestrationConfigurationTypeDef(TypedDict):
    queryTransformationConfiguration: QueryTransformationConfigurationTypeDef


class RequestMetadataFiltersOutputTypeDef(TypedDict):
    equals: NotRequired[Dict[str, str]]
    notEquals: NotRequired[Dict[str, str]]
    andAll: NotRequired[List[RequestMetadataBaseFiltersOutputTypeDef]]
    orAll: NotRequired[List[RequestMetadataBaseFiltersOutputTypeDef]]


RequestMetadataBaseFiltersUnionTypeDef = Union[
    RequestMetadataBaseFiltersTypeDef, RequestMetadataBaseFiltersOutputTypeDef
]
TextInferenceConfigUnionTypeDef = Union[
    TextInferenceConfigTypeDef, TextInferenceConfigOutputTypeDef
]


class ValidationDataConfigOutputTypeDef(TypedDict):
    validators: List[ValidatorTypeDef]


class ValidationDataConfigTypeDef(TypedDict):
    validators: Sequence[ValidatorTypeDef]


EvaluatorModelConfigUnionTypeDef = Union[
    EvaluatorModelConfigTypeDef, EvaluatorModelConfigOutputTypeDef
]
ByteContentDocUnionTypeDef = Union[ByteContentDocTypeDef, ByteContentDocOutputTypeDef]


class LoggingConfigTypeDef(TypedDict):
    cloudWatchConfig: NotRequired[CloudWatchConfigTypeDef]
    s3Config: NotRequired[S3ConfigTypeDef]
    textDataDeliveryEnabled: NotRequired[bool]
    imageDataDeliveryEnabled: NotRequired[bool]
    embeddingDataDeliveryEnabled: NotRequired[bool]
    videoDataDeliveryEnabled: NotRequired[bool]


class ListModelCopyJobsResponseTypeDef(TypedDict):
    modelCopyJobSummaries: List[ModelCopyJobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class CustomizationConfigTypeDef(TypedDict):
    distillationConfig: NotRequired[DistillationConfigTypeDef]


class EvaluationDatasetMetricConfigOutputTypeDef(TypedDict):
    taskType: EvaluationTaskTypeType
    dataset: EvaluationDatasetTypeDef
    metricNames: List[str]


class EvaluationDatasetMetricConfigTypeDef(TypedDict):
    taskType: EvaluationTaskTypeType
    dataset: EvaluationDatasetTypeDef
    metricNames: Sequence[str]


KnowledgeBaseVectorSearchConfigurationOutputTypeDef = TypedDict(
    "KnowledgeBaseVectorSearchConfigurationOutputTypeDef",
    {
        "numberOfResults": NotRequired[int],
        "overrideSearchType": NotRequired[SearchTypeType],
        "filter": NotRequired[RetrievalFilterOutputTypeDef],
    },
)
RetrievalFilterTypeDef = TypedDict(
    "RetrievalFilterTypeDef",
    {
        "equals": NotRequired[FilterAttributeUnionTypeDef],
        "notEquals": NotRequired[FilterAttributeUnionTypeDef],
        "greaterThan": NotRequired[FilterAttributeUnionTypeDef],
        "greaterThanOrEquals": NotRequired[FilterAttributeUnionTypeDef],
        "lessThan": NotRequired[FilterAttributeUnionTypeDef],
        "lessThanOrEquals": NotRequired[FilterAttributeUnionTypeDef],
        "in": NotRequired[FilterAttributeUnionTypeDef],
        "notIn": NotRequired[FilterAttributeUnionTypeDef],
        "startsWith": NotRequired[FilterAttributeUnionTypeDef],
        "listContains": NotRequired[FilterAttributeUnionTypeDef],
        "stringContains": NotRequired[FilterAttributeUnionTypeDef],
        "andAll": NotRequired[Sequence[Mapping[str, Any]]],
        "orAll": NotRequired[Sequence[Mapping[str, Any]]],
    },
)


class GetFoundationModelResponseTypeDef(TypedDict):
    modelDetails: FoundationModelDetailsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListFoundationModelsResponseTypeDef(TypedDict):
    modelSummaries: List[FoundationModelSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ListInferenceProfilesResponseTypeDef(TypedDict):
    inferenceProfileSummaries: List[InferenceProfileSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class EndpointConfigOutputTypeDef(TypedDict):
    sageMaker: NotRequired[SageMakerEndpointOutputTypeDef]


class SageMakerEndpointTypeDef(TypedDict):
    initialInstanceCount: int
    instanceType: str
    executionRole: str
    kmsEncryptionKey: NotRequired[str]
    vpc: NotRequired[VpcConfigUnionTypeDef]


class ListPromptRoutersResponseTypeDef(TypedDict):
    promptRouterSummaries: List[PromptRouterSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class CreateGuardrailRequestRequestTypeDef(TypedDict):
    name: str
    blockedInputMessaging: str
    blockedOutputsMessaging: str
    description: NotRequired[str]
    topicPolicyConfig: NotRequired[GuardrailTopicPolicyConfigTypeDef]
    contentPolicyConfig: NotRequired[GuardrailContentPolicyConfigTypeDef]
    wordPolicyConfig: NotRequired[GuardrailWordPolicyConfigTypeDef]
    sensitiveInformationPolicyConfig: NotRequired[GuardrailSensitiveInformationPolicyConfigTypeDef]
    contextualGroundingPolicyConfig: NotRequired[GuardrailContextualGroundingPolicyConfigTypeDef]
    kmsKeyId: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]
    clientRequestToken: NotRequired[str]


class UpdateGuardrailRequestRequestTypeDef(TypedDict):
    guardrailIdentifier: str
    name: str
    blockedInputMessaging: str
    blockedOutputsMessaging: str
    description: NotRequired[str]
    topicPolicyConfig: NotRequired[GuardrailTopicPolicyConfigTypeDef]
    contentPolicyConfig: NotRequired[GuardrailContentPolicyConfigTypeDef]
    wordPolicyConfig: NotRequired[GuardrailWordPolicyConfigTypeDef]
    sensitiveInformationPolicyConfig: NotRequired[GuardrailSensitiveInformationPolicyConfigTypeDef]
    contextualGroundingPolicyConfig: NotRequired[GuardrailContextualGroundingPolicyConfigTypeDef]
    kmsKeyId: NotRequired[str]


class GetGuardrailResponseTypeDef(TypedDict):
    name: str
    description: str
    guardrailId: str
    guardrailArn: str
    version: str
    status: GuardrailStatusType
    topicPolicy: GuardrailTopicPolicyTypeDef
    contentPolicy: GuardrailContentPolicyTypeDef
    wordPolicy: GuardrailWordPolicyTypeDef
    sensitiveInformationPolicy: GuardrailSensitiveInformationPolicyTypeDef
    contextualGroundingPolicy: GuardrailContextualGroundingPolicyTypeDef
    createdAt: datetime
    updatedAt: datetime
    statusReasons: List[str]
    failureRecommendations: List[str]
    blockedInputMessaging: str
    blockedOutputsMessaging: str
    kmsKeyArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class ExternalSourcesGenerationConfigurationOutputTypeDef(TypedDict):
    promptTemplate: NotRequired[PromptTemplateTypeDef]
    guardrailConfiguration: NotRequired[GuardrailConfigurationTypeDef]
    kbInferenceConfig: NotRequired[KbInferenceConfigOutputTypeDef]
    additionalModelRequestFields: NotRequired[Dict[str, Dict[str, Any]]]


class GenerationConfigurationOutputTypeDef(TypedDict):
    promptTemplate: NotRequired[PromptTemplateTypeDef]
    guardrailConfiguration: NotRequired[GuardrailConfigurationTypeDef]
    kbInferenceConfig: NotRequired[KbInferenceConfigOutputTypeDef]
    additionalModelRequestFields: NotRequired[Dict[str, Dict[str, Any]]]


class CreateModelImportJobRequestRequestTypeDef(TypedDict):
    jobName: str
    importedModelName: str
    roleArn: str
    modelDataSource: ModelDataSourceTypeDef
    jobTags: NotRequired[Sequence[TagTypeDef]]
    importedModelTags: NotRequired[Sequence[TagTypeDef]]
    clientRequestToken: NotRequired[str]
    vpcConfig: NotRequired[VpcConfigTypeDef]
    importedModelKmsKeyId: NotRequired[str]


class GetImportedModelResponseTypeDef(TypedDict):
    modelArn: str
    modelName: str
    jobName: str
    jobArn: str
    modelDataSource: ModelDataSourceTypeDef
    creationTime: datetime
    modelArchitecture: str
    modelKmsKeyArn: str
    instructSupported: bool
    ResponseMetadata: ResponseMetadataTypeDef


class GetModelImportJobResponseTypeDef(TypedDict):
    jobArn: str
    jobName: str
    importedModelName: str
    importedModelArn: str
    roleArn: str
    modelDataSource: ModelDataSourceTypeDef
    status: ModelImportJobStatusType
    failureMessage: str
    creationTime: datetime
    lastModifiedTime: datetime
    endTime: datetime
    vpcConfig: VpcConfigOutputTypeDef
    importedModelKmsKeyArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateModelInvocationJobRequestRequestTypeDef(TypedDict):
    jobName: str
    roleArn: str
    modelId: str
    inputDataConfig: ModelInvocationJobInputDataConfigTypeDef
    outputDataConfig: ModelInvocationJobOutputDataConfigTypeDef
    clientRequestToken: NotRequired[str]
    vpcConfig: NotRequired[VpcConfigTypeDef]
    timeoutDurationInHours: NotRequired[int]
    tags: NotRequired[Sequence[TagTypeDef]]


class GetModelInvocationJobResponseTypeDef(TypedDict):
    jobArn: str
    jobName: str
    modelId: str
    clientRequestToken: str
    roleArn: str
    status: ModelInvocationJobStatusType
    message: str
    submitTime: datetime
    lastModifiedTime: datetime
    endTime: datetime
    inputDataConfig: ModelInvocationJobInputDataConfigTypeDef
    outputDataConfig: ModelInvocationJobOutputDataConfigTypeDef
    vpcConfig: VpcConfigOutputTypeDef
    timeoutDurationInHours: int
    jobExpirationTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class ModelInvocationJobSummaryTypeDef(TypedDict):
    jobArn: str
    jobName: str
    modelId: str
    roleArn: str
    submitTime: datetime
    inputDataConfig: ModelInvocationJobInputDataConfigTypeDef
    outputDataConfig: ModelInvocationJobOutputDataConfigTypeDef
    clientRequestToken: NotRequired[str]
    status: NotRequired[ModelInvocationJobStatusType]
    message: NotRequired[str]
    lastModifiedTime: NotRequired[datetime]
    endTime: NotRequired[datetime]
    vpcConfig: NotRequired[VpcConfigOutputTypeDef]
    timeoutDurationInHours: NotRequired[int]
    jobExpirationTime: NotRequired[datetime]


class InvocationLogsConfigOutputTypeDef(TypedDict):
    invocationLogSource: InvocationLogSourceTypeDef
    usePromptResponse: NotRequired[bool]
    requestMetadataFilters: NotRequired[RequestMetadataFiltersOutputTypeDef]


class RequestMetadataFiltersTypeDef(TypedDict):
    equals: NotRequired[Mapping[str, str]]
    notEquals: NotRequired[Mapping[str, str]]
    andAll: NotRequired[Sequence[RequestMetadataBaseFiltersUnionTypeDef]]
    orAll: NotRequired[Sequence[RequestMetadataBaseFiltersTypeDef]]


class KbInferenceConfigTypeDef(TypedDict):
    textInferenceConfig: NotRequired[TextInferenceConfigUnionTypeDef]


class ExternalSourceTypeDef(TypedDict):
    sourceType: ExternalSourceTypeType
    s3Location: NotRequired[S3ObjectDocTypeDef]
    byteContent: NotRequired[ByteContentDocUnionTypeDef]


class GetModelInvocationLoggingConfigurationResponseTypeDef(TypedDict):
    loggingConfig: LoggingConfigTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class PutModelInvocationLoggingConfigurationRequestRequestTypeDef(TypedDict):
    loggingConfig: LoggingConfigTypeDef


class AutomatedEvaluationConfigOutputTypeDef(TypedDict):
    datasetMetricConfigs: List[EvaluationDatasetMetricConfigOutputTypeDef]
    evaluatorModelConfig: NotRequired[EvaluatorModelConfigOutputTypeDef]


class HumanEvaluationConfigOutputTypeDef(TypedDict):
    datasetMetricConfigs: List[EvaluationDatasetMetricConfigOutputTypeDef]
    humanWorkflowConfig: NotRequired[HumanWorkflowConfigTypeDef]
    customMetrics: NotRequired[List[HumanEvaluationCustomMetricTypeDef]]


EvaluationDatasetMetricConfigUnionTypeDef = Union[
    EvaluationDatasetMetricConfigTypeDef, EvaluationDatasetMetricConfigOutputTypeDef
]


class HumanEvaluationConfigTypeDef(TypedDict):
    datasetMetricConfigs: Sequence[EvaluationDatasetMetricConfigTypeDef]
    humanWorkflowConfig: NotRequired[HumanWorkflowConfigTypeDef]
    customMetrics: NotRequired[Sequence[HumanEvaluationCustomMetricTypeDef]]


class KnowledgeBaseRetrievalConfigurationOutputTypeDef(TypedDict):
    vectorSearchConfiguration: KnowledgeBaseVectorSearchConfigurationOutputTypeDef


RetrievalFilterUnionTypeDef = Union[RetrievalFilterTypeDef, RetrievalFilterOutputTypeDef]


class MarketplaceModelEndpointTypeDef(TypedDict):
    endpointArn: str
    modelSourceIdentifier: str
    createdAt: datetime
    updatedAt: datetime
    endpointConfig: EndpointConfigOutputTypeDef
    endpointStatus: str
    status: NotRequired[StatusType]
    statusMessage: NotRequired[str]
    endpointStatusMessage: NotRequired[str]


SageMakerEndpointUnionTypeDef = Union[SageMakerEndpointTypeDef, SageMakerEndpointOutputTypeDef]


class ExternalSourcesRetrieveAndGenerateConfigurationOutputTypeDef(TypedDict):
    modelArn: str
    sources: List[ExternalSourceOutputTypeDef]
    generationConfiguration: NotRequired[ExternalSourcesGenerationConfigurationOutputTypeDef]


class ListModelInvocationJobsResponseTypeDef(TypedDict):
    invocationJobSummaries: List[ModelInvocationJobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class TrainingDataConfigOutputTypeDef(TypedDict):
    s3Uri: NotRequired[str]
    invocationLogsConfig: NotRequired[InvocationLogsConfigOutputTypeDef]


RequestMetadataFiltersUnionTypeDef = Union[
    RequestMetadataFiltersTypeDef, RequestMetadataFiltersOutputTypeDef
]
KbInferenceConfigUnionTypeDef = Union[KbInferenceConfigTypeDef, KbInferenceConfigOutputTypeDef]
ExternalSourceUnionTypeDef = Union[ExternalSourceTypeDef, ExternalSourceOutputTypeDef]


class EvaluationConfigOutputTypeDef(TypedDict):
    automated: NotRequired[AutomatedEvaluationConfigOutputTypeDef]
    human: NotRequired[HumanEvaluationConfigOutputTypeDef]


class AutomatedEvaluationConfigTypeDef(TypedDict):
    datasetMetricConfigs: Sequence[EvaluationDatasetMetricConfigUnionTypeDef]
    evaluatorModelConfig: NotRequired[EvaluatorModelConfigUnionTypeDef]


HumanEvaluationConfigUnionTypeDef = Union[
    HumanEvaluationConfigTypeDef, HumanEvaluationConfigOutputTypeDef
]


class KnowledgeBaseRetrieveAndGenerateConfigurationOutputTypeDef(TypedDict):
    knowledgeBaseId: str
    modelArn: str
    retrievalConfiguration: NotRequired[KnowledgeBaseRetrievalConfigurationOutputTypeDef]
    generationConfiguration: NotRequired[GenerationConfigurationOutputTypeDef]
    orchestrationConfiguration: NotRequired[OrchestrationConfigurationTypeDef]


class RetrieveConfigOutputTypeDef(TypedDict):
    knowledgeBaseId: str
    knowledgeBaseRetrievalConfiguration: KnowledgeBaseRetrievalConfigurationOutputTypeDef


KnowledgeBaseVectorSearchConfigurationTypeDef = TypedDict(
    "KnowledgeBaseVectorSearchConfigurationTypeDef",
    {
        "numberOfResults": NotRequired[int],
        "overrideSearchType": NotRequired[SearchTypeType],
        "filter": NotRequired[RetrievalFilterUnionTypeDef],
    },
)


class CreateMarketplaceModelEndpointResponseTypeDef(TypedDict):
    marketplaceModelEndpoint: MarketplaceModelEndpointTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetMarketplaceModelEndpointResponseTypeDef(TypedDict):
    marketplaceModelEndpoint: MarketplaceModelEndpointTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class RegisterMarketplaceModelEndpointResponseTypeDef(TypedDict):
    marketplaceModelEndpoint: MarketplaceModelEndpointTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateMarketplaceModelEndpointResponseTypeDef(TypedDict):
    marketplaceModelEndpoint: MarketplaceModelEndpointTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class EndpointConfigTypeDef(TypedDict):
    sageMaker: NotRequired[SageMakerEndpointUnionTypeDef]


class GetCustomModelResponseTypeDef(TypedDict):
    modelArn: str
    modelName: str
    jobName: str
    jobArn: str
    baseModelArn: str
    customizationType: CustomizationTypeType
    modelKmsKeyArn: str
    hyperParameters: Dict[str, str]
    trainingDataConfig: TrainingDataConfigOutputTypeDef
    validationDataConfig: ValidationDataConfigOutputTypeDef
    outputDataConfig: OutputDataConfigTypeDef
    trainingMetrics: TrainingMetricsTypeDef
    validationMetrics: List[ValidatorMetricTypeDef]
    creationTime: datetime
    customizationConfig: CustomizationConfigTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetModelCustomizationJobResponseTypeDef(TypedDict):
    jobArn: str
    jobName: str
    outputModelName: str
    outputModelArn: str
    clientRequestToken: str
    roleArn: str
    status: ModelCustomizationJobStatusType
    failureMessage: str
    creationTime: datetime
    lastModifiedTime: datetime
    endTime: datetime
    baseModelArn: str
    hyperParameters: Dict[str, str]
    trainingDataConfig: TrainingDataConfigOutputTypeDef
    validationDataConfig: ValidationDataConfigOutputTypeDef
    outputDataConfig: OutputDataConfigTypeDef
    customizationType: CustomizationTypeType
    outputModelKmsKeyArn: str
    trainingMetrics: TrainingMetricsTypeDef
    validationMetrics: List[ValidatorMetricTypeDef]
    vpcConfig: VpcConfigOutputTypeDef
    customizationConfig: CustomizationConfigTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class InvocationLogsConfigTypeDef(TypedDict):
    invocationLogSource: InvocationLogSourceTypeDef
    usePromptResponse: NotRequired[bool]
    requestMetadataFilters: NotRequired[RequestMetadataFiltersUnionTypeDef]


class ExternalSourcesGenerationConfigurationTypeDef(TypedDict):
    promptTemplate: NotRequired[PromptTemplateTypeDef]
    guardrailConfiguration: NotRequired[GuardrailConfigurationTypeDef]
    kbInferenceConfig: NotRequired[KbInferenceConfigUnionTypeDef]
    additionalModelRequestFields: NotRequired[Mapping[str, Mapping[str, Any]]]


class GenerationConfigurationTypeDef(TypedDict):
    promptTemplate: NotRequired[PromptTemplateTypeDef]
    guardrailConfiguration: NotRequired[GuardrailConfigurationTypeDef]
    kbInferenceConfig: NotRequired[KbInferenceConfigUnionTypeDef]
    additionalModelRequestFields: NotRequired[Mapping[str, Mapping[str, Any]]]


AutomatedEvaluationConfigUnionTypeDef = Union[
    AutomatedEvaluationConfigTypeDef, AutomatedEvaluationConfigOutputTypeDef
]
RetrieveAndGenerateConfigurationOutputTypeDef = TypedDict(
    "RetrieveAndGenerateConfigurationOutputTypeDef",
    {
        "type": RetrieveAndGenerateTypeType,
        "knowledgeBaseConfiguration": NotRequired[
            KnowledgeBaseRetrieveAndGenerateConfigurationOutputTypeDef
        ],
        "externalSourcesConfiguration": NotRequired[
            ExternalSourcesRetrieveAndGenerateConfigurationOutputTypeDef
        ],
    },
)
KnowledgeBaseVectorSearchConfigurationUnionTypeDef = Union[
    KnowledgeBaseVectorSearchConfigurationTypeDef,
    KnowledgeBaseVectorSearchConfigurationOutputTypeDef,
]


class CreateMarketplaceModelEndpointRequestRequestTypeDef(TypedDict):
    modelSourceIdentifier: str
    endpointConfig: EndpointConfigTypeDef
    endpointName: str
    acceptEula: NotRequired[bool]
    clientRequestToken: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]


class UpdateMarketplaceModelEndpointRequestRequestTypeDef(TypedDict):
    endpointArn: str
    endpointConfig: EndpointConfigTypeDef
    clientRequestToken: NotRequired[str]


InvocationLogsConfigUnionTypeDef = Union[
    InvocationLogsConfigTypeDef, InvocationLogsConfigOutputTypeDef
]
ExternalSourcesGenerationConfigurationUnionTypeDef = Union[
    ExternalSourcesGenerationConfigurationTypeDef,
    ExternalSourcesGenerationConfigurationOutputTypeDef,
]
GenerationConfigurationUnionTypeDef = Union[
    GenerationConfigurationTypeDef, GenerationConfigurationOutputTypeDef
]


class EvaluationConfigTypeDef(TypedDict):
    automated: NotRequired[AutomatedEvaluationConfigUnionTypeDef]
    human: NotRequired[HumanEvaluationConfigUnionTypeDef]


class KnowledgeBaseConfigOutputTypeDef(TypedDict):
    retrieveConfig: NotRequired[RetrieveConfigOutputTypeDef]
    retrieveAndGenerateConfig: NotRequired[RetrieveAndGenerateConfigurationOutputTypeDef]


class KnowledgeBaseRetrievalConfigurationTypeDef(TypedDict):
    vectorSearchConfiguration: KnowledgeBaseVectorSearchConfigurationUnionTypeDef


class TrainingDataConfigTypeDef(TypedDict):
    s3Uri: NotRequired[str]
    invocationLogsConfig: NotRequired[InvocationLogsConfigUnionTypeDef]


class ExternalSourcesRetrieveAndGenerateConfigurationTypeDef(TypedDict):
    modelArn: str
    sources: Sequence[ExternalSourceUnionTypeDef]
    generationConfiguration: NotRequired[ExternalSourcesGenerationConfigurationUnionTypeDef]


class RAGConfigOutputTypeDef(TypedDict):
    knowledgeBaseConfig: NotRequired[KnowledgeBaseConfigOutputTypeDef]


KnowledgeBaseRetrievalConfigurationUnionTypeDef = Union[
    KnowledgeBaseRetrievalConfigurationTypeDef, KnowledgeBaseRetrievalConfigurationOutputTypeDef
]


class CreateModelCustomizationJobRequestRequestTypeDef(TypedDict):
    jobName: str
    customModelName: str
    roleArn: str
    baseModelIdentifier: str
    trainingDataConfig: TrainingDataConfigTypeDef
    outputDataConfig: OutputDataConfigTypeDef
    clientRequestToken: NotRequired[str]
    customizationType: NotRequired[CustomizationTypeType]
    customModelKmsKeyId: NotRequired[str]
    jobTags: NotRequired[Sequence[TagTypeDef]]
    customModelTags: NotRequired[Sequence[TagTypeDef]]
    validationDataConfig: NotRequired[ValidationDataConfigTypeDef]
    hyperParameters: NotRequired[Mapping[str, str]]
    vpcConfig: NotRequired[VpcConfigTypeDef]
    customizationConfig: NotRequired[CustomizationConfigTypeDef]


ExternalSourcesRetrieveAndGenerateConfigurationUnionTypeDef = Union[
    ExternalSourcesRetrieveAndGenerateConfigurationTypeDef,
    ExternalSourcesRetrieveAndGenerateConfigurationOutputTypeDef,
]


class EvaluationInferenceConfigOutputTypeDef(TypedDict):
    models: NotRequired[List[EvaluationModelConfigTypeDef]]
    ragConfigs: NotRequired[List[RAGConfigOutputTypeDef]]


class KnowledgeBaseRetrieveAndGenerateConfigurationTypeDef(TypedDict):
    knowledgeBaseId: str
    modelArn: str
    retrievalConfiguration: NotRequired[KnowledgeBaseRetrievalConfigurationUnionTypeDef]
    generationConfiguration: NotRequired[GenerationConfigurationUnionTypeDef]
    orchestrationConfiguration: NotRequired[OrchestrationConfigurationTypeDef]


class RetrieveConfigTypeDef(TypedDict):
    knowledgeBaseId: str
    knowledgeBaseRetrievalConfiguration: KnowledgeBaseRetrievalConfigurationUnionTypeDef


class GetEvaluationJobResponseTypeDef(TypedDict):
    jobName: str
    status: EvaluationJobStatusType
    jobArn: str
    jobDescription: str
    roleArn: str
    customerEncryptionKeyId: str
    jobType: EvaluationJobTypeType
    applicationType: ApplicationTypeType
    evaluationConfig: EvaluationConfigOutputTypeDef
    inferenceConfig: EvaluationInferenceConfigOutputTypeDef
    outputDataConfig: EvaluationOutputDataConfigTypeDef
    creationTime: datetime
    lastModifiedTime: datetime
    failureMessages: List[str]
    ResponseMetadata: ResponseMetadataTypeDef


KnowledgeBaseRetrieveAndGenerateConfigurationUnionTypeDef = Union[
    KnowledgeBaseRetrieveAndGenerateConfigurationTypeDef,
    KnowledgeBaseRetrieveAndGenerateConfigurationOutputTypeDef,
]
RetrieveConfigUnionTypeDef = Union[RetrieveConfigTypeDef, RetrieveConfigOutputTypeDef]
RetrieveAndGenerateConfigurationTypeDef = TypedDict(
    "RetrieveAndGenerateConfigurationTypeDef",
    {
        "type": RetrieveAndGenerateTypeType,
        "knowledgeBaseConfiguration": NotRequired[
            KnowledgeBaseRetrieveAndGenerateConfigurationUnionTypeDef
        ],
        "externalSourcesConfiguration": NotRequired[
            ExternalSourcesRetrieveAndGenerateConfigurationUnionTypeDef
        ],
    },
)
RetrieveAndGenerateConfigurationUnionTypeDef = Union[
    RetrieveAndGenerateConfigurationTypeDef, RetrieveAndGenerateConfigurationOutputTypeDef
]


class KnowledgeBaseConfigTypeDef(TypedDict):
    retrieveConfig: NotRequired[RetrieveConfigUnionTypeDef]
    retrieveAndGenerateConfig: NotRequired[RetrieveAndGenerateConfigurationUnionTypeDef]


KnowledgeBaseConfigUnionTypeDef = Union[
    KnowledgeBaseConfigTypeDef, KnowledgeBaseConfigOutputTypeDef
]


class RAGConfigTypeDef(TypedDict):
    knowledgeBaseConfig: NotRequired[KnowledgeBaseConfigUnionTypeDef]


RAGConfigUnionTypeDef = Union[RAGConfigTypeDef, RAGConfigOutputTypeDef]


class EvaluationInferenceConfigTypeDef(TypedDict):
    models: NotRequired[Sequence[EvaluationModelConfigTypeDef]]
    ragConfigs: NotRequired[Sequence[RAGConfigUnionTypeDef]]


class CreateEvaluationJobRequestRequestTypeDef(TypedDict):
    jobName: str
    roleArn: str
    evaluationConfig: EvaluationConfigTypeDef
    inferenceConfig: EvaluationInferenceConfigTypeDef
    outputDataConfig: EvaluationOutputDataConfigTypeDef
    jobDescription: NotRequired[str]
    clientRequestToken: NotRequired[str]
    customerEncryptionKeyId: NotRequired[str]
    jobTags: NotRequired[Sequence[TagTypeDef]]
    applicationType: NotRequired[ApplicationTypeType]
