"""
Type annotations for sagemaker service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/type_defs/)

Usage::

    ```python
    from mypy_boto3_sagemaker.type_defs import ActionSourceTypeDef

    data: ActionSourceTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Any, Dict, List, Mapping, Sequence, Union

from .literals import (
    ActionStatusType,
    AdditionalS3DataSourceDataTypeType,
    AggregationTransformationValueType,
    AlgorithmSortByType,
    AlgorithmStatusType,
    AppImageConfigSortKeyType,
    AppInstanceTypeType,
    AppNetworkAccessTypeType,
    AppSecurityGroupManagementType,
    AppStatusType,
    AppTypeType,
    ArtifactSourceIdTypeType,
    AssemblyTypeType,
    AssociationEdgeTypeType,
    AsyncNotificationTopicTypesType,
    AthenaResultCompressionTypeType,
    AthenaResultFormatType,
    AuthModeType,
    AutoMLAlgorithmType,
    AutoMLChannelTypeType,
    AutoMLJobObjectiveTypeType,
    AutoMLJobSecondaryStatusType,
    AutoMLJobStatusType,
    AutoMLMetricEnumType,
    AutoMLMetricExtendedEnumType,
    AutoMLModeType,
    AutoMLProblemTypeConfigNameType,
    AutoMLProcessingUnitType,
    AutoMLS3DataTypeType,
    AutoMLSortByType,
    AutoMLSortOrderType,
    AutoMountHomeEFSType,
    AwsManagedHumanLoopRequestSourceType,
    BatchDeleteClusterNodesErrorCodeType,
    BatchStrategyType,
    BooleanOperatorType,
    CandidateSortByType,
    CandidateStatusType,
    CandidateStepTypeType,
    CapacitySizeTypeType,
    CaptureModeType,
    CaptureStatusType,
    ClarifyFeatureTypeType,
    ClarifyTextGranularityType,
    ClarifyTextLanguageType,
    ClusterInstanceStatusType,
    ClusterInstanceTypeType,
    ClusterNodeRecoveryType,
    ClusterSortByType,
    ClusterStatusType,
    CodeRepositorySortByType,
    CodeRepositorySortOrderType,
    CollectionTypeType,
    CompilationJobStatusType,
    CompleteOnConvergenceType,
    CompressionTypeType,
    ConditionOutcomeType,
    ContainerModeType,
    ContentClassifierType,
    CrossAccountFilterOptionType,
    DataDistributionTypeType,
    DataSourceNameType,
    DeepHealthCheckTypeType,
    DetailedAlgorithmStatusType,
    DetailedModelPackageStatusType,
    DeviceDeploymentStatusType,
    DeviceSubsetTypeType,
    DirectInternetAccessType,
    DirectionType,
    DomainStatusType,
    EdgePackagingJobStatusType,
    EdgePresetDeploymentStatusType,
    EnabledOrDisabledType,
    EndpointConfigSortKeyType,
    EndpointSortKeyType,
    EndpointStatusType,
    ExecutionRoleIdentityConfigType,
    ExecutionStatusType,
    FailureHandlingPolicyType,
    FeatureGroupSortByType,
    FeatureGroupSortOrderType,
    FeatureGroupStatusType,
    FeatureStatusType,
    FeatureTypeType,
    FileSystemAccessModeType,
    FileSystemTypeType,
    FillingTypeType,
    FlatInvocationsType,
    FlowDefinitionStatusType,
    FrameworkType,
    HubContentSortByType,
    HubContentStatusType,
    HubContentSupportStatusType,
    HubContentTypeType,
    HubSortByType,
    HubStatusType,
    HumanTaskUiStatusType,
    HyperParameterScalingTypeType,
    HyperParameterTuningJobObjectiveTypeType,
    HyperParameterTuningJobSortByOptionsType,
    HyperParameterTuningJobStatusType,
    HyperParameterTuningJobStrategyTypeType,
    HyperParameterTuningJobWarmStartTypeType,
    ImageSortByType,
    ImageSortOrderType,
    ImageStatusType,
    ImageVersionSortByType,
    ImageVersionSortOrderType,
    ImageVersionStatusType,
    InferenceComponentSortKeyType,
    InferenceComponentStatusType,
    InferenceExecutionModeType,
    InferenceExperimentStatusType,
    InferenceExperimentStopDesiredStateType,
    InputModeType,
    InstanceTypeType,
    IsTrackingServerActiveType,
    JobTypeType,
    JoinSourceType,
    LabelingJobStatusType,
    LastUpdateStatusValueType,
    LifecycleManagementType,
    LineageTypeType,
    ListCompilationJobsSortByType,
    ListDeviceFleetsSortByType,
    ListEdgeDeploymentPlansSortByType,
    ListEdgePackagingJobsSortByType,
    ListInferenceRecommendationsJobsSortByType,
    ListOptimizationJobsSortByType,
    ListWorkforcesSortByOptionsType,
    ListWorkteamsSortByOptionsType,
    ManagedInstanceScalingStatusType,
    MetricSetSourceType,
    MlToolsType,
    ModelApprovalStatusType,
    ModelCacheSettingType,
    ModelCardExportJobSortByType,
    ModelCardExportJobSortOrderType,
    ModelCardExportJobStatusType,
    ModelCardProcessingStatusType,
    ModelCardSortByType,
    ModelCardSortOrderType,
    ModelCardStatusType,
    ModelCompressionTypeType,
    ModelMetadataFilterTypeType,
    ModelPackageGroupSortByType,
    ModelPackageGroupStatusType,
    ModelPackageSortByType,
    ModelPackageStatusType,
    ModelPackageTypeType,
    ModelSortKeyType,
    ModelVariantActionType,
    ModelVariantStatusType,
    MonitoringAlertHistorySortKeyType,
    MonitoringAlertStatusType,
    MonitoringExecutionSortKeyType,
    MonitoringJobDefinitionSortKeyType,
    MonitoringProblemTypeType,
    MonitoringScheduleSortKeyType,
    MonitoringTypeType,
    NotebookInstanceAcceleratorTypeType,
    NotebookInstanceLifecycleConfigSortKeyType,
    NotebookInstanceLifecycleConfigSortOrderType,
    NotebookInstanceSortKeyType,
    NotebookInstanceSortOrderType,
    NotebookInstanceStatusType,
    NotebookOutputOptionType,
    ObjectiveStatusType,
    OfflineStoreStatusValueType,
    OperatorType,
    OptimizationJobDeploymentInstanceTypeType,
    OptimizationJobStatusType,
    OrderKeyType,
    OutputCompressionTypeType,
    ParameterTypeType,
    PipelineExecutionStatusType,
    PipelineStatusType,
    ProblemTypeType,
    ProcessingInstanceTypeType,
    ProcessingJobStatusType,
    ProcessingS3CompressionTypeType,
    ProcessingS3DataDistributionTypeType,
    ProcessingS3DataTypeType,
    ProcessingS3InputModeType,
    ProcessingS3UploadModeType,
    ProcessorType,
    ProductionVariantAcceleratorTypeType,
    ProductionVariantInstanceTypeType,
    ProfilingStatusType,
    ProjectSortByType,
    ProjectSortOrderType,
    ProjectStatusType,
    RecommendationJobStatusType,
    RecommendationJobSupportedEndpointTypeType,
    RecommendationJobTypeType,
    RecommendationStatusType,
    RecordWrapperType,
    RedshiftResultCompressionTypeType,
    RedshiftResultFormatType,
    RepositoryAccessModeType,
    ResourceCatalogSortOrderType,
    ResourceTypeType,
    RetentionTypeType,
    RootAccessType,
    RoutingStrategyType,
    RStudioServerProAccessStatusType,
    RStudioServerProUserGroupType,
    RuleEvaluationStatusType,
    S3DataDistributionType,
    S3DataTypeType,
    S3ModelDataTypeType,
    SagemakerServicecatalogStatusType,
    ScheduleStatusType,
    SearchSortOrderType,
    SecondaryStatusType,
    SharingTypeType,
    SkipModelValidationType,
    SortActionsByType,
    SortAssociationsByType,
    SortByType,
    SortContextsByType,
    SortExperimentsByType,
    SortInferenceExperimentsByType,
    SortLineageGroupsByType,
    SortOrderType,
    SortPipelineExecutionsByType,
    SortPipelinesByType,
    SortTrackingServerByType,
    SortTrialComponentsByType,
    SortTrialsByType,
    SpaceSortKeyType,
    SpaceStatusType,
    SplitTypeType,
    StageStatusType,
    StatisticType,
    StepStatusType,
    StorageTypeType,
    StudioLifecycleConfigAppTypeType,
    StudioLifecycleConfigSortKeyType,
    StudioWebPortalType,
    TableFormatType,
    TagPropagationType,
    TargetDeviceType,
    TargetPlatformAcceleratorType,
    TargetPlatformArchType,
    TargetPlatformOsType,
    ThroughputModeType,
    TrackingServerSizeType,
    TrackingServerStatusType,
    TrafficRoutingConfigTypeType,
    TrafficTypeType,
    TrainingInputModeType,
    TrainingInstanceTypeType,
    TrainingJobEarlyStoppingTypeType,
    TrainingJobSortByOptionsType,
    TrainingJobStatusType,
    TrainingRepositoryAccessModeType,
    TransformInstanceTypeType,
    TransformJobStatusType,
    TrialComponentPrimaryStatusType,
    TtlDurationUnitType,
    UserProfileSortKeyType,
    UserProfileStatusType,
    VariantPropertyTypeType,
    VariantStatusType,
    VendorGuidanceType,
    WarmPoolResourceStatusType,
    WorkforceStatusType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "ActionSourceTypeDef",
    "ActionSummaryTypeDef",
    "AddAssociationRequestRequestTypeDef",
    "AddAssociationResponseTypeDef",
    "AddTagsInputRequestTypeDef",
    "AddTagsOutputTypeDef",
    "AdditionalInferenceSpecificationDefinitionOutputTypeDef",
    "AdditionalInferenceSpecificationDefinitionTypeDef",
    "AdditionalInferenceSpecificationDefinitionUnionTypeDef",
    "AdditionalModelDataSourceTypeDef",
    "AdditionalS3DataSourceTypeDef",
    "AgentVersionTypeDef",
    "AlarmTypeDef",
    "AlgorithmSpecificationOutputTypeDef",
    "AlgorithmSpecificationTypeDef",
    "AlgorithmStatusDetailsTypeDef",
    "AlgorithmStatusItemTypeDef",
    "AlgorithmSummaryTypeDef",
    "AlgorithmValidationProfileOutputTypeDef",
    "AlgorithmValidationProfileTypeDef",
    "AlgorithmValidationProfileUnionTypeDef",
    "AlgorithmValidationSpecificationOutputTypeDef",
    "AlgorithmValidationSpecificationTypeDef",
    "AmazonQSettingsTypeDef",
    "AnnotationConsolidationConfigTypeDef",
    "AppDetailsTypeDef",
    "AppImageConfigDetailsTypeDef",
    "AppLifecycleManagementTypeDef",
    "AppSpecificationOutputTypeDef",
    "AppSpecificationTypeDef",
    "ArtifactSourceOutputTypeDef",
    "ArtifactSourceTypeDef",
    "ArtifactSourceTypeTypeDef",
    "ArtifactSummaryTypeDef",
    "AssociateTrialComponentRequestRequestTypeDef",
    "AssociateTrialComponentResponseTypeDef",
    "AssociationSummaryTypeDef",
    "AsyncInferenceClientConfigTypeDef",
    "AsyncInferenceConfigOutputTypeDef",
    "AsyncInferenceConfigTypeDef",
    "AsyncInferenceNotificationConfigOutputTypeDef",
    "AsyncInferenceNotificationConfigTypeDef",
    "AsyncInferenceNotificationConfigUnionTypeDef",
    "AsyncInferenceOutputConfigOutputTypeDef",
    "AsyncInferenceOutputConfigTypeDef",
    "AsyncInferenceOutputConfigUnionTypeDef",
    "AthenaDatasetDefinitionTypeDef",
    "AutoMLAlgorithmConfigOutputTypeDef",
    "AutoMLAlgorithmConfigTypeDef",
    "AutoMLAlgorithmConfigUnionTypeDef",
    "AutoMLCandidateGenerationConfigOutputTypeDef",
    "AutoMLCandidateGenerationConfigTypeDef",
    "AutoMLCandidateGenerationConfigUnionTypeDef",
    "AutoMLCandidateStepTypeDef",
    "AutoMLCandidateTypeDef",
    "AutoMLChannelTypeDef",
    "AutoMLComputeConfigTypeDef",
    "AutoMLContainerDefinitionTypeDef",
    "AutoMLDataSourceTypeDef",
    "AutoMLDataSplitConfigTypeDef",
    "AutoMLJobArtifactsTypeDef",
    "AutoMLJobChannelTypeDef",
    "AutoMLJobCompletionCriteriaTypeDef",
    "AutoMLJobConfigOutputTypeDef",
    "AutoMLJobConfigTypeDef",
    "AutoMLJobObjectiveTypeDef",
    "AutoMLJobStepMetadataTypeDef",
    "AutoMLJobSummaryTypeDef",
    "AutoMLOutputDataConfigTypeDef",
    "AutoMLPartialFailureReasonTypeDef",
    "AutoMLProblemTypeConfigOutputTypeDef",
    "AutoMLProblemTypeConfigTypeDef",
    "AutoMLProblemTypeResolvedAttributesTypeDef",
    "AutoMLResolvedAttributesTypeDef",
    "AutoMLS3DataSourceTypeDef",
    "AutoMLSecurityConfigOutputTypeDef",
    "AutoMLSecurityConfigTypeDef",
    "AutoMLSecurityConfigUnionTypeDef",
    "AutoParameterTypeDef",
    "AutoRollbackConfigOutputTypeDef",
    "AutoRollbackConfigTypeDef",
    "AutoRollbackConfigUnionTypeDef",
    "AutotuneTypeDef",
    "BatchDataCaptureConfigTypeDef",
    "BatchDeleteClusterNodesErrorTypeDef",
    "BatchDeleteClusterNodesRequestRequestTypeDef",
    "BatchDeleteClusterNodesResponseTypeDef",
    "BatchDescribeModelPackageErrorTypeDef",
    "BatchDescribeModelPackageInputRequestTypeDef",
    "BatchDescribeModelPackageOutputTypeDef",
    "BatchDescribeModelPackageSummaryTypeDef",
    "BatchTransformInputOutputTypeDef",
    "BatchTransformInputTypeDef",
    "BatchTransformInputUnionTypeDef",
    "BestObjectiveNotImprovingTypeDef",
    "BiasTypeDef",
    "BlueGreenUpdatePolicyTypeDef",
    "CacheHitResultTypeDef",
    "CallbackStepMetadataTypeDef",
    "CandidateArtifactLocationsTypeDef",
    "CandidateGenerationConfigOutputTypeDef",
    "CandidateGenerationConfigTypeDef",
    "CandidateGenerationConfigUnionTypeDef",
    "CandidatePropertiesTypeDef",
    "CanvasAppSettingsOutputTypeDef",
    "CanvasAppSettingsTypeDef",
    "CanvasAppSettingsUnionTypeDef",
    "CapacitySizeTypeDef",
    "CaptureContentTypeHeaderOutputTypeDef",
    "CaptureContentTypeHeaderTypeDef",
    "CaptureContentTypeHeaderUnionTypeDef",
    "CaptureOptionTypeDef",
    "CategoricalParameterOutputTypeDef",
    "CategoricalParameterRangeOutputTypeDef",
    "CategoricalParameterRangeSpecificationOutputTypeDef",
    "CategoricalParameterRangeSpecificationTypeDef",
    "CategoricalParameterRangeSpecificationUnionTypeDef",
    "CategoricalParameterRangeTypeDef",
    "CategoricalParameterRangeUnionTypeDef",
    "CategoricalParameterTypeDef",
    "CategoricalParameterUnionTypeDef",
    "ChannelOutputTypeDef",
    "ChannelSpecificationOutputTypeDef",
    "ChannelSpecificationTypeDef",
    "ChannelSpecificationUnionTypeDef",
    "ChannelTypeDef",
    "ChannelUnionTypeDef",
    "CheckpointConfigTypeDef",
    "ClarifyCheckStepMetadataTypeDef",
    "ClarifyExplainerConfigOutputTypeDef",
    "ClarifyExplainerConfigTypeDef",
    "ClarifyExplainerConfigUnionTypeDef",
    "ClarifyInferenceConfigOutputTypeDef",
    "ClarifyInferenceConfigTypeDef",
    "ClarifyInferenceConfigUnionTypeDef",
    "ClarifyShapBaselineConfigTypeDef",
    "ClarifyShapConfigTypeDef",
    "ClarifyTextConfigTypeDef",
    "ClusterEbsVolumeConfigTypeDef",
    "ClusterInstanceGroupDetailsTypeDef",
    "ClusterInstanceGroupSpecificationTypeDef",
    "ClusterInstancePlacementTypeDef",
    "ClusterInstanceStatusDetailsTypeDef",
    "ClusterInstanceStorageConfigTypeDef",
    "ClusterLifeCycleConfigTypeDef",
    "ClusterNodeDetailsTypeDef",
    "ClusterNodeSummaryTypeDef",
    "ClusterOrchestratorEksConfigTypeDef",
    "ClusterOrchestratorTypeDef",
    "ClusterSummaryTypeDef",
    "CodeEditorAppImageConfigOutputTypeDef",
    "CodeEditorAppImageConfigTypeDef",
    "CodeEditorAppSettingsOutputTypeDef",
    "CodeEditorAppSettingsTypeDef",
    "CodeEditorAppSettingsUnionTypeDef",
    "CodeRepositorySummaryTypeDef",
    "CodeRepositoryTypeDef",
    "CognitoConfigTypeDef",
    "CognitoMemberDefinitionTypeDef",
    "CollectionConfigTypeDef",
    "CollectionConfigurationOutputTypeDef",
    "CollectionConfigurationTypeDef",
    "CollectionConfigurationUnionTypeDef",
    "CompilationJobSummaryTypeDef",
    "ConditionStepMetadataTypeDef",
    "ContainerConfigOutputTypeDef",
    "ContainerConfigTypeDef",
    "ContainerConfigUnionTypeDef",
    "ContainerDefinitionOutputTypeDef",
    "ContainerDefinitionTypeDef",
    "ContainerDefinitionUnionTypeDef",
    "ContextSourceTypeDef",
    "ContextSummaryTypeDef",
    "ContinuousParameterRangeSpecificationTypeDef",
    "ContinuousParameterRangeTypeDef",
    "ConvergenceDetectedTypeDef",
    "CreateActionRequestRequestTypeDef",
    "CreateActionResponseTypeDef",
    "CreateAlgorithmInputRequestTypeDef",
    "CreateAlgorithmOutputTypeDef",
    "CreateAppImageConfigRequestRequestTypeDef",
    "CreateAppImageConfigResponseTypeDef",
    "CreateAppRequestRequestTypeDef",
    "CreateAppResponseTypeDef",
    "CreateArtifactRequestRequestTypeDef",
    "CreateArtifactResponseTypeDef",
    "CreateAutoMLJobRequestRequestTypeDef",
    "CreateAutoMLJobResponseTypeDef",
    "CreateAutoMLJobV2RequestRequestTypeDef",
    "CreateAutoMLJobV2ResponseTypeDef",
    "CreateClusterRequestRequestTypeDef",
    "CreateClusterResponseTypeDef",
    "CreateCodeRepositoryInputRequestTypeDef",
    "CreateCodeRepositoryOutputTypeDef",
    "CreateCompilationJobRequestRequestTypeDef",
    "CreateCompilationJobResponseTypeDef",
    "CreateContextRequestRequestTypeDef",
    "CreateContextResponseTypeDef",
    "CreateDataQualityJobDefinitionRequestRequestTypeDef",
    "CreateDataQualityJobDefinitionResponseTypeDef",
    "CreateDeviceFleetRequestRequestTypeDef",
    "CreateDomainRequestRequestTypeDef",
    "CreateDomainResponseTypeDef",
    "CreateEdgeDeploymentPlanRequestRequestTypeDef",
    "CreateEdgeDeploymentPlanResponseTypeDef",
    "CreateEdgeDeploymentStageRequestRequestTypeDef",
    "CreateEdgePackagingJobRequestRequestTypeDef",
    "CreateEndpointConfigInputRequestTypeDef",
    "CreateEndpointConfigOutputTypeDef",
    "CreateEndpointInputRequestTypeDef",
    "CreateEndpointOutputTypeDef",
    "CreateExperimentRequestRequestTypeDef",
    "CreateExperimentResponseTypeDef",
    "CreateFeatureGroupRequestRequestTypeDef",
    "CreateFeatureGroupResponseTypeDef",
    "CreateFlowDefinitionRequestRequestTypeDef",
    "CreateFlowDefinitionResponseTypeDef",
    "CreateHubContentReferenceRequestRequestTypeDef",
    "CreateHubContentReferenceResponseTypeDef",
    "CreateHubRequestRequestTypeDef",
    "CreateHubResponseTypeDef",
    "CreateHumanTaskUiRequestRequestTypeDef",
    "CreateHumanTaskUiResponseTypeDef",
    "CreateHyperParameterTuningJobRequestRequestTypeDef",
    "CreateHyperParameterTuningJobResponseTypeDef",
    "CreateImageRequestRequestTypeDef",
    "CreateImageResponseTypeDef",
    "CreateImageVersionRequestRequestTypeDef",
    "CreateImageVersionResponseTypeDef",
    "CreateInferenceComponentInputRequestTypeDef",
    "CreateInferenceComponentOutputTypeDef",
    "CreateInferenceExperimentRequestRequestTypeDef",
    "CreateInferenceExperimentResponseTypeDef",
    "CreateInferenceRecommendationsJobRequestRequestTypeDef",
    "CreateInferenceRecommendationsJobResponseTypeDef",
    "CreateLabelingJobRequestRequestTypeDef",
    "CreateLabelingJobResponseTypeDef",
    "CreateMlflowTrackingServerRequestRequestTypeDef",
    "CreateMlflowTrackingServerResponseTypeDef",
    "CreateModelBiasJobDefinitionRequestRequestTypeDef",
    "CreateModelBiasJobDefinitionResponseTypeDef",
    "CreateModelCardExportJobRequestRequestTypeDef",
    "CreateModelCardExportJobResponseTypeDef",
    "CreateModelCardRequestRequestTypeDef",
    "CreateModelCardResponseTypeDef",
    "CreateModelExplainabilityJobDefinitionRequestRequestTypeDef",
    "CreateModelExplainabilityJobDefinitionResponseTypeDef",
    "CreateModelInputRequestTypeDef",
    "CreateModelOutputTypeDef",
    "CreateModelPackageGroupInputRequestTypeDef",
    "CreateModelPackageGroupOutputTypeDef",
    "CreateModelPackageInputRequestTypeDef",
    "CreateModelPackageOutputTypeDef",
    "CreateModelQualityJobDefinitionRequestRequestTypeDef",
    "CreateModelQualityJobDefinitionResponseTypeDef",
    "CreateMonitoringScheduleRequestRequestTypeDef",
    "CreateMonitoringScheduleResponseTypeDef",
    "CreateNotebookInstanceInputRequestTypeDef",
    "CreateNotebookInstanceLifecycleConfigInputRequestTypeDef",
    "CreateNotebookInstanceLifecycleConfigOutputTypeDef",
    "CreateNotebookInstanceOutputTypeDef",
    "CreateOptimizationJobRequestRequestTypeDef",
    "CreateOptimizationJobResponseTypeDef",
    "CreatePipelineRequestRequestTypeDef",
    "CreatePipelineResponseTypeDef",
    "CreatePresignedDomainUrlRequestRequestTypeDef",
    "CreatePresignedDomainUrlResponseTypeDef",
    "CreatePresignedMlflowTrackingServerUrlRequestRequestTypeDef",
    "CreatePresignedMlflowTrackingServerUrlResponseTypeDef",
    "CreatePresignedNotebookInstanceUrlInputRequestTypeDef",
    "CreatePresignedNotebookInstanceUrlOutputTypeDef",
    "CreateProcessingJobRequestRequestTypeDef",
    "CreateProcessingJobResponseTypeDef",
    "CreateProjectInputRequestTypeDef",
    "CreateProjectOutputTypeDef",
    "CreateSpaceRequestRequestTypeDef",
    "CreateSpaceResponseTypeDef",
    "CreateStudioLifecycleConfigRequestRequestTypeDef",
    "CreateStudioLifecycleConfigResponseTypeDef",
    "CreateTrainingJobRequestRequestTypeDef",
    "CreateTrainingJobResponseTypeDef",
    "CreateTransformJobRequestRequestTypeDef",
    "CreateTransformJobResponseTypeDef",
    "CreateTrialComponentRequestRequestTypeDef",
    "CreateTrialComponentResponseTypeDef",
    "CreateTrialRequestRequestTypeDef",
    "CreateTrialResponseTypeDef",
    "CreateUserProfileRequestRequestTypeDef",
    "CreateUserProfileResponseTypeDef",
    "CreateWorkforceRequestRequestTypeDef",
    "CreateWorkforceResponseTypeDef",
    "CreateWorkteamRequestRequestTypeDef",
    "CreateWorkteamResponseTypeDef",
    "CustomFileSystemConfigTypeDef",
    "CustomFileSystemTypeDef",
    "CustomImageTypeDef",
    "CustomPosixUserConfigTypeDef",
    "CustomizedMetricSpecificationTypeDef",
    "DataCaptureConfigOutputTypeDef",
    "DataCaptureConfigSummaryTypeDef",
    "DataCaptureConfigTypeDef",
    "DataCatalogConfigTypeDef",
    "DataProcessingTypeDef",
    "DataQualityAppSpecificationOutputTypeDef",
    "DataQualityAppSpecificationTypeDef",
    "DataQualityBaselineConfigTypeDef",
    "DataQualityJobInputOutputTypeDef",
    "DataQualityJobInputTypeDef",
    "DataSourceOutputTypeDef",
    "DataSourceTypeDef",
    "DataSourceUnionTypeDef",
    "DatasetDefinitionTypeDef",
    "DebugHookConfigOutputTypeDef",
    "DebugHookConfigTypeDef",
    "DebugRuleConfigurationOutputTypeDef",
    "DebugRuleConfigurationTypeDef",
    "DebugRuleConfigurationUnionTypeDef",
    "DebugRuleEvaluationStatusTypeDef",
    "DefaultEbsStorageSettingsTypeDef",
    "DefaultSpaceSettingsOutputTypeDef",
    "DefaultSpaceSettingsTypeDef",
    "DefaultSpaceStorageSettingsTypeDef",
    "DeleteActionRequestRequestTypeDef",
    "DeleteActionResponseTypeDef",
    "DeleteAlgorithmInputRequestTypeDef",
    "DeleteAppImageConfigRequestRequestTypeDef",
    "DeleteAppRequestRequestTypeDef",
    "DeleteArtifactRequestRequestTypeDef",
    "DeleteArtifactResponseTypeDef",
    "DeleteAssociationRequestRequestTypeDef",
    "DeleteAssociationResponseTypeDef",
    "DeleteClusterRequestRequestTypeDef",
    "DeleteClusterResponseTypeDef",
    "DeleteCodeRepositoryInputRequestTypeDef",
    "DeleteCompilationJobRequestRequestTypeDef",
    "DeleteContextRequestRequestTypeDef",
    "DeleteContextResponseTypeDef",
    "DeleteDataQualityJobDefinitionRequestRequestTypeDef",
    "DeleteDeviceFleetRequestRequestTypeDef",
    "DeleteDomainRequestRequestTypeDef",
    "DeleteEdgeDeploymentPlanRequestRequestTypeDef",
    "DeleteEdgeDeploymentStageRequestRequestTypeDef",
    "DeleteEndpointConfigInputRequestTypeDef",
    "DeleteEndpointInputRequestTypeDef",
    "DeleteExperimentRequestRequestTypeDef",
    "DeleteExperimentResponseTypeDef",
    "DeleteFeatureGroupRequestRequestTypeDef",
    "DeleteFlowDefinitionRequestRequestTypeDef",
    "DeleteHubContentReferenceRequestRequestTypeDef",
    "DeleteHubContentRequestRequestTypeDef",
    "DeleteHubRequestRequestTypeDef",
    "DeleteHumanTaskUiRequestRequestTypeDef",
    "DeleteHyperParameterTuningJobRequestRequestTypeDef",
    "DeleteImageRequestRequestTypeDef",
    "DeleteImageVersionRequestRequestTypeDef",
    "DeleteInferenceComponentInputRequestTypeDef",
    "DeleteInferenceExperimentRequestRequestTypeDef",
    "DeleteInferenceExperimentResponseTypeDef",
    "DeleteMlflowTrackingServerRequestRequestTypeDef",
    "DeleteMlflowTrackingServerResponseTypeDef",
    "DeleteModelBiasJobDefinitionRequestRequestTypeDef",
    "DeleteModelCardRequestRequestTypeDef",
    "DeleteModelExplainabilityJobDefinitionRequestRequestTypeDef",
    "DeleteModelInputRequestTypeDef",
    "DeleteModelPackageGroupInputRequestTypeDef",
    "DeleteModelPackageGroupPolicyInputRequestTypeDef",
    "DeleteModelPackageInputRequestTypeDef",
    "DeleteModelQualityJobDefinitionRequestRequestTypeDef",
    "DeleteMonitoringScheduleRequestRequestTypeDef",
    "DeleteNotebookInstanceInputRequestTypeDef",
    "DeleteNotebookInstanceLifecycleConfigInputRequestTypeDef",
    "DeleteOptimizationJobRequestRequestTypeDef",
    "DeletePipelineRequestRequestTypeDef",
    "DeletePipelineResponseTypeDef",
    "DeleteProjectInputRequestTypeDef",
    "DeleteSpaceRequestRequestTypeDef",
    "DeleteStudioLifecycleConfigRequestRequestTypeDef",
    "DeleteTagsInputRequestTypeDef",
    "DeleteTrialComponentRequestRequestTypeDef",
    "DeleteTrialComponentResponseTypeDef",
    "DeleteTrialRequestRequestTypeDef",
    "DeleteTrialResponseTypeDef",
    "DeleteUserProfileRequestRequestTypeDef",
    "DeleteWorkforceRequestRequestTypeDef",
    "DeleteWorkteamRequestRequestTypeDef",
    "DeleteWorkteamResponseTypeDef",
    "DeployedImageTypeDef",
    "DeploymentConfigOutputTypeDef",
    "DeploymentConfigTypeDef",
    "DeploymentRecommendationTypeDef",
    "DeploymentStageStatusSummaryTypeDef",
    "DeploymentStageTypeDef",
    "DeregisterDevicesRequestRequestTypeDef",
    "DerivedInformationTypeDef",
    "DescribeActionRequestRequestTypeDef",
    "DescribeActionResponseTypeDef",
    "DescribeAlgorithmInputRequestTypeDef",
    "DescribeAlgorithmOutputTypeDef",
    "DescribeAppImageConfigRequestRequestTypeDef",
    "DescribeAppImageConfigResponseTypeDef",
    "DescribeAppRequestRequestTypeDef",
    "DescribeAppResponseTypeDef",
    "DescribeArtifactRequestRequestTypeDef",
    "DescribeArtifactResponseTypeDef",
    "DescribeAutoMLJobRequestRequestTypeDef",
    "DescribeAutoMLJobResponseTypeDef",
    "DescribeAutoMLJobV2RequestRequestTypeDef",
    "DescribeAutoMLJobV2ResponseTypeDef",
    "DescribeClusterNodeRequestRequestTypeDef",
    "DescribeClusterNodeResponseTypeDef",
    "DescribeClusterRequestRequestTypeDef",
    "DescribeClusterResponseTypeDef",
    "DescribeCodeRepositoryInputRequestTypeDef",
    "DescribeCodeRepositoryOutputTypeDef",
    "DescribeCompilationJobRequestRequestTypeDef",
    "DescribeCompilationJobResponseTypeDef",
    "DescribeContextRequestRequestTypeDef",
    "DescribeContextResponseTypeDef",
    "DescribeDataQualityJobDefinitionRequestRequestTypeDef",
    "DescribeDataQualityJobDefinitionResponseTypeDef",
    "DescribeDeviceFleetRequestRequestTypeDef",
    "DescribeDeviceFleetResponseTypeDef",
    "DescribeDeviceRequestRequestTypeDef",
    "DescribeDeviceResponseTypeDef",
    "DescribeDomainRequestRequestTypeDef",
    "DescribeDomainResponseTypeDef",
    "DescribeEdgeDeploymentPlanRequestRequestTypeDef",
    "DescribeEdgeDeploymentPlanResponseTypeDef",
    "DescribeEdgePackagingJobRequestRequestTypeDef",
    "DescribeEdgePackagingJobResponseTypeDef",
    "DescribeEndpointConfigInputRequestTypeDef",
    "DescribeEndpointConfigOutputTypeDef",
    "DescribeEndpointInputEndpointDeletedWaitTypeDef",
    "DescribeEndpointInputEndpointInServiceWaitTypeDef",
    "DescribeEndpointInputRequestTypeDef",
    "DescribeEndpointOutputTypeDef",
    "DescribeExperimentRequestRequestTypeDef",
    "DescribeExperimentResponseTypeDef",
    "DescribeFeatureGroupRequestRequestTypeDef",
    "DescribeFeatureGroupResponseTypeDef",
    "DescribeFeatureMetadataRequestRequestTypeDef",
    "DescribeFeatureMetadataResponseTypeDef",
    "DescribeFlowDefinitionRequestRequestTypeDef",
    "DescribeFlowDefinitionResponseTypeDef",
    "DescribeHubContentRequestRequestTypeDef",
    "DescribeHubContentResponseTypeDef",
    "DescribeHubRequestRequestTypeDef",
    "DescribeHubResponseTypeDef",
    "DescribeHumanTaskUiRequestRequestTypeDef",
    "DescribeHumanTaskUiResponseTypeDef",
    "DescribeHyperParameterTuningJobRequestRequestTypeDef",
    "DescribeHyperParameterTuningJobResponseTypeDef",
    "DescribeImageRequestImageCreatedWaitTypeDef",
    "DescribeImageRequestImageDeletedWaitTypeDef",
    "DescribeImageRequestImageUpdatedWaitTypeDef",
    "DescribeImageRequestRequestTypeDef",
    "DescribeImageResponseTypeDef",
    "DescribeImageVersionRequestImageVersionCreatedWaitTypeDef",
    "DescribeImageVersionRequestImageVersionDeletedWaitTypeDef",
    "DescribeImageVersionRequestRequestTypeDef",
    "DescribeImageVersionResponseTypeDef",
    "DescribeInferenceComponentInputRequestTypeDef",
    "DescribeInferenceComponentOutputTypeDef",
    "DescribeInferenceExperimentRequestRequestTypeDef",
    "DescribeInferenceExperimentResponseTypeDef",
    "DescribeInferenceRecommendationsJobRequestRequestTypeDef",
    "DescribeInferenceRecommendationsJobResponseTypeDef",
    "DescribeLabelingJobRequestRequestTypeDef",
    "DescribeLabelingJobResponseTypeDef",
    "DescribeLineageGroupRequestRequestTypeDef",
    "DescribeLineageGroupResponseTypeDef",
    "DescribeMlflowTrackingServerRequestRequestTypeDef",
    "DescribeMlflowTrackingServerResponseTypeDef",
    "DescribeModelBiasJobDefinitionRequestRequestTypeDef",
    "DescribeModelBiasJobDefinitionResponseTypeDef",
    "DescribeModelCardExportJobRequestRequestTypeDef",
    "DescribeModelCardExportJobResponseTypeDef",
    "DescribeModelCardRequestRequestTypeDef",
    "DescribeModelCardResponseTypeDef",
    "DescribeModelExplainabilityJobDefinitionRequestRequestTypeDef",
    "DescribeModelExplainabilityJobDefinitionResponseTypeDef",
    "DescribeModelInputRequestTypeDef",
    "DescribeModelOutputTypeDef",
    "DescribeModelPackageGroupInputRequestTypeDef",
    "DescribeModelPackageGroupOutputTypeDef",
    "DescribeModelPackageInputRequestTypeDef",
    "DescribeModelPackageOutputTypeDef",
    "DescribeModelQualityJobDefinitionRequestRequestTypeDef",
    "DescribeModelQualityJobDefinitionResponseTypeDef",
    "DescribeMonitoringScheduleRequestRequestTypeDef",
    "DescribeMonitoringScheduleResponseTypeDef",
    "DescribeNotebookInstanceInputNotebookInstanceDeletedWaitTypeDef",
    "DescribeNotebookInstanceInputNotebookInstanceInServiceWaitTypeDef",
    "DescribeNotebookInstanceInputNotebookInstanceStoppedWaitTypeDef",
    "DescribeNotebookInstanceInputRequestTypeDef",
    "DescribeNotebookInstanceLifecycleConfigInputRequestTypeDef",
    "DescribeNotebookInstanceLifecycleConfigOutputTypeDef",
    "DescribeNotebookInstanceOutputTypeDef",
    "DescribeOptimizationJobRequestRequestTypeDef",
    "DescribeOptimizationJobResponseTypeDef",
    "DescribePipelineDefinitionForExecutionRequestRequestTypeDef",
    "DescribePipelineDefinitionForExecutionResponseTypeDef",
    "DescribePipelineExecutionRequestRequestTypeDef",
    "DescribePipelineExecutionResponseTypeDef",
    "DescribePipelineRequestRequestTypeDef",
    "DescribePipelineResponseTypeDef",
    "DescribeProcessingJobRequestProcessingJobCompletedOrStoppedWaitTypeDef",
    "DescribeProcessingJobRequestRequestTypeDef",
    "DescribeProcessingJobResponseTypeDef",
    "DescribeProjectInputRequestTypeDef",
    "DescribeProjectOutputTypeDef",
    "DescribeSpaceRequestRequestTypeDef",
    "DescribeSpaceResponseTypeDef",
    "DescribeStudioLifecycleConfigRequestRequestTypeDef",
    "DescribeStudioLifecycleConfigResponseTypeDef",
    "DescribeSubscribedWorkteamRequestRequestTypeDef",
    "DescribeSubscribedWorkteamResponseTypeDef",
    "DescribeTrainingJobRequestRequestTypeDef",
    "DescribeTrainingJobRequestTrainingJobCompletedOrStoppedWaitTypeDef",
    "DescribeTrainingJobResponseTypeDef",
    "DescribeTransformJobRequestRequestTypeDef",
    "DescribeTransformJobRequestTransformJobCompletedOrStoppedWaitTypeDef",
    "DescribeTransformJobResponseTypeDef",
    "DescribeTrialComponentRequestRequestTypeDef",
    "DescribeTrialComponentResponseTypeDef",
    "DescribeTrialRequestRequestTypeDef",
    "DescribeTrialResponseTypeDef",
    "DescribeUserProfileRequestRequestTypeDef",
    "DescribeUserProfileResponseTypeDef",
    "DescribeWorkforceRequestRequestTypeDef",
    "DescribeWorkforceResponseTypeDef",
    "DescribeWorkteamRequestRequestTypeDef",
    "DescribeWorkteamResponseTypeDef",
    "DesiredWeightAndCapacityTypeDef",
    "DeviceDeploymentSummaryTypeDef",
    "DeviceFleetSummaryTypeDef",
    "DeviceSelectionConfigOutputTypeDef",
    "DeviceSelectionConfigTypeDef",
    "DeviceSelectionConfigUnionTypeDef",
    "DeviceStatsTypeDef",
    "DeviceSummaryTypeDef",
    "DeviceTypeDef",
    "DirectDeploySettingsTypeDef",
    "DisassociateTrialComponentRequestRequestTypeDef",
    "DisassociateTrialComponentResponseTypeDef",
    "DockerSettingsOutputTypeDef",
    "DockerSettingsTypeDef",
    "DockerSettingsUnionTypeDef",
    "DomainDetailsTypeDef",
    "DomainSettingsForUpdateTypeDef",
    "DomainSettingsOutputTypeDef",
    "DomainSettingsTypeDef",
    "DriftCheckBaselinesTypeDef",
    "DriftCheckBiasTypeDef",
    "DriftCheckExplainabilityTypeDef",
    "DriftCheckModelDataQualityTypeDef",
    "DriftCheckModelQualityTypeDef",
    "DynamicScalingConfigurationTypeDef",
    "EFSFileSystemConfigTypeDef",
    "EFSFileSystemTypeDef",
    "EMRStepMetadataTypeDef",
    "EbsStorageSettingsTypeDef",
    "EdgeDeploymentConfigTypeDef",
    "EdgeDeploymentModelConfigTypeDef",
    "EdgeDeploymentPlanSummaryTypeDef",
    "EdgeDeploymentStatusTypeDef",
    "EdgeModelStatTypeDef",
    "EdgeModelSummaryTypeDef",
    "EdgeModelTypeDef",
    "EdgeOutputConfigTypeDef",
    "EdgePackagingJobSummaryTypeDef",
    "EdgePresetDeploymentOutputTypeDef",
    "EdgeTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EmrServerlessComputeConfigTypeDef",
    "EmrServerlessSettingsTypeDef",
    "EmrSettingsOutputTypeDef",
    "EmrSettingsTypeDef",
    "EmrSettingsUnionTypeDef",
    "EndpointConfigStepMetadataTypeDef",
    "EndpointConfigSummaryTypeDef",
    "EndpointInfoTypeDef",
    "EndpointInputConfigurationOutputTypeDef",
    "EndpointInputConfigurationTypeDef",
    "EndpointInputConfigurationUnionTypeDef",
    "EndpointInputTypeDef",
    "EndpointMetadataTypeDef",
    "EndpointOutputConfigurationTypeDef",
    "EndpointPerformanceTypeDef",
    "EndpointStepMetadataTypeDef",
    "EndpointSummaryTypeDef",
    "EndpointTypeDef",
    "EnvironmentParameterRangesOutputTypeDef",
    "EnvironmentParameterRangesTypeDef",
    "EnvironmentParameterRangesUnionTypeDef",
    "EnvironmentParameterTypeDef",
    "ExperimentConfigTypeDef",
    "ExperimentSourceTypeDef",
    "ExperimentSummaryTypeDef",
    "ExperimentTypeDef",
    "ExplainabilityTypeDef",
    "ExplainerConfigOutputTypeDef",
    "ExplainerConfigTypeDef",
    "FailStepMetadataTypeDef",
    "FeatureDefinitionTypeDef",
    "FeatureGroupSummaryTypeDef",
    "FeatureGroupTypeDef",
    "FeatureMetadataTypeDef",
    "FeatureParameterTypeDef",
    "FileSourceTypeDef",
    "FileSystemConfigTypeDef",
    "FileSystemDataSourceTypeDef",
    "FilterTypeDef",
    "FinalAutoMLJobObjectiveMetricTypeDef",
    "FinalHyperParameterTuningJobObjectiveMetricTypeDef",
    "FlowDefinitionOutputConfigTypeDef",
    "FlowDefinitionSummaryTypeDef",
    "GenerativeAiSettingsTypeDef",
    "GetDeviceFleetReportRequestRequestTypeDef",
    "GetDeviceFleetReportResponseTypeDef",
    "GetLineageGroupPolicyRequestRequestTypeDef",
    "GetLineageGroupPolicyResponseTypeDef",
    "GetModelPackageGroupPolicyInputRequestTypeDef",
    "GetModelPackageGroupPolicyOutputTypeDef",
    "GetSagemakerServicecatalogPortfolioStatusOutputTypeDef",
    "GetScalingConfigurationRecommendationRequestRequestTypeDef",
    "GetScalingConfigurationRecommendationResponseTypeDef",
    "GetSearchSuggestionsRequestRequestTypeDef",
    "GetSearchSuggestionsResponseTypeDef",
    "GitConfigForUpdateTypeDef",
    "GitConfigTypeDef",
    "HiddenSageMakerImageOutputTypeDef",
    "HiddenSageMakerImageTypeDef",
    "HiddenSageMakerImageUnionTypeDef",
    "HolidayConfigAttributesTypeDef",
    "HubContentDependencyTypeDef",
    "HubContentInfoTypeDef",
    "HubInfoTypeDef",
    "HubS3StorageConfigTypeDef",
    "HumanLoopActivationConditionsConfigTypeDef",
    "HumanLoopActivationConfigTypeDef",
    "HumanLoopConfigOutputTypeDef",
    "HumanLoopConfigTypeDef",
    "HumanLoopRequestSourceTypeDef",
    "HumanTaskConfigOutputTypeDef",
    "HumanTaskConfigTypeDef",
    "HumanTaskUiSummaryTypeDef",
    "HyperParameterAlgorithmSpecificationOutputTypeDef",
    "HyperParameterAlgorithmSpecificationTypeDef",
    "HyperParameterAlgorithmSpecificationUnionTypeDef",
    "HyperParameterSpecificationOutputTypeDef",
    "HyperParameterSpecificationTypeDef",
    "HyperParameterSpecificationUnionTypeDef",
    "HyperParameterTrainingJobDefinitionOutputTypeDef",
    "HyperParameterTrainingJobDefinitionTypeDef",
    "HyperParameterTrainingJobDefinitionUnionTypeDef",
    "HyperParameterTrainingJobSummaryTypeDef",
    "HyperParameterTuningInstanceConfigTypeDef",
    "HyperParameterTuningJobCompletionDetailsTypeDef",
    "HyperParameterTuningJobConfigOutputTypeDef",
    "HyperParameterTuningJobConfigTypeDef",
    "HyperParameterTuningJobConsumedResourcesTypeDef",
    "HyperParameterTuningJobObjectiveTypeDef",
    "HyperParameterTuningJobSearchEntityTypeDef",
    "HyperParameterTuningJobStrategyConfigTypeDef",
    "HyperParameterTuningJobSummaryTypeDef",
    "HyperParameterTuningJobWarmStartConfigOutputTypeDef",
    "HyperParameterTuningJobWarmStartConfigTypeDef",
    "HyperParameterTuningResourceConfigOutputTypeDef",
    "HyperParameterTuningResourceConfigTypeDef",
    "HyperParameterTuningResourceConfigUnionTypeDef",
    "HyperbandStrategyConfigTypeDef",
    "IamIdentityTypeDef",
    "IamPolicyConstraintsTypeDef",
    "IdentityProviderOAuthSettingTypeDef",
    "IdleSettingsTypeDef",
    "ImageClassificationJobConfigTypeDef",
    "ImageConfigTypeDef",
    "ImageTypeDef",
    "ImageVersionTypeDef",
    "ImportHubContentRequestRequestTypeDef",
    "ImportHubContentResponseTypeDef",
    "InferenceComponentComputeResourceRequirementsTypeDef",
    "InferenceComponentContainerSpecificationSummaryTypeDef",
    "InferenceComponentContainerSpecificationTypeDef",
    "InferenceComponentRuntimeConfigSummaryTypeDef",
    "InferenceComponentRuntimeConfigTypeDef",
    "InferenceComponentSpecificationSummaryTypeDef",
    "InferenceComponentSpecificationTypeDef",
    "InferenceComponentStartupParametersTypeDef",
    "InferenceComponentSummaryTypeDef",
    "InferenceExecutionConfigTypeDef",
    "InferenceExperimentDataStorageConfigOutputTypeDef",
    "InferenceExperimentDataStorageConfigTypeDef",
    "InferenceExperimentScheduleOutputTypeDef",
    "InferenceExperimentScheduleTypeDef",
    "InferenceExperimentSummaryTypeDef",
    "InferenceHubAccessConfigTypeDef",
    "InferenceMetricsTypeDef",
    "InferenceRecommendationTypeDef",
    "InferenceRecommendationsJobStepTypeDef",
    "InferenceRecommendationsJobTypeDef",
    "InferenceSpecificationOutputTypeDef",
    "InferenceSpecificationTypeDef",
    "InfraCheckConfigTypeDef",
    "InputConfigTypeDef",
    "InstanceGroupTypeDef",
    "InstanceMetadataServiceConfigurationTypeDef",
    "IntegerParameterRangeSpecificationTypeDef",
    "IntegerParameterRangeTypeDef",
    "JupyterLabAppImageConfigOutputTypeDef",
    "JupyterLabAppImageConfigTypeDef",
    "JupyterLabAppSettingsOutputTypeDef",
    "JupyterLabAppSettingsTypeDef",
    "JupyterLabAppSettingsUnionTypeDef",
    "JupyterServerAppSettingsOutputTypeDef",
    "JupyterServerAppSettingsTypeDef",
    "JupyterServerAppSettingsUnionTypeDef",
    "KendraSettingsTypeDef",
    "KernelGatewayAppSettingsOutputTypeDef",
    "KernelGatewayAppSettingsTypeDef",
    "KernelGatewayAppSettingsUnionTypeDef",
    "KernelGatewayImageConfigOutputTypeDef",
    "KernelGatewayImageConfigTypeDef",
    "KernelSpecTypeDef",
    "LabelCountersForWorkteamTypeDef",
    "LabelCountersTypeDef",
    "LabelingJobAlgorithmsConfigOutputTypeDef",
    "LabelingJobAlgorithmsConfigTypeDef",
    "LabelingJobDataAttributesOutputTypeDef",
    "LabelingJobDataAttributesTypeDef",
    "LabelingJobDataAttributesUnionTypeDef",
    "LabelingJobDataSourceTypeDef",
    "LabelingJobForWorkteamSummaryTypeDef",
    "LabelingJobInputConfigOutputTypeDef",
    "LabelingJobInputConfigTypeDef",
    "LabelingJobOutputConfigTypeDef",
    "LabelingJobOutputTypeDef",
    "LabelingJobResourceConfigOutputTypeDef",
    "LabelingJobResourceConfigTypeDef",
    "LabelingJobResourceConfigUnionTypeDef",
    "LabelingJobS3DataSourceTypeDef",
    "LabelingJobSnsDataSourceTypeDef",
    "LabelingJobStoppingConditionsTypeDef",
    "LabelingJobSummaryTypeDef",
    "LambdaStepMetadataTypeDef",
    "LastUpdateStatusTypeDef",
    "LineageGroupSummaryTypeDef",
    "ListActionsRequestListActionsPaginateTypeDef",
    "ListActionsRequestRequestTypeDef",
    "ListActionsResponseTypeDef",
    "ListAlgorithmsInputListAlgorithmsPaginateTypeDef",
    "ListAlgorithmsInputRequestTypeDef",
    "ListAlgorithmsOutputTypeDef",
    "ListAliasesRequestListAliasesPaginateTypeDef",
    "ListAliasesRequestRequestTypeDef",
    "ListAliasesResponseTypeDef",
    "ListAppImageConfigsRequestListAppImageConfigsPaginateTypeDef",
    "ListAppImageConfigsRequestRequestTypeDef",
    "ListAppImageConfigsResponseTypeDef",
    "ListAppsRequestListAppsPaginateTypeDef",
    "ListAppsRequestRequestTypeDef",
    "ListAppsResponseTypeDef",
    "ListArtifactsRequestListArtifactsPaginateTypeDef",
    "ListArtifactsRequestRequestTypeDef",
    "ListArtifactsResponseTypeDef",
    "ListAssociationsRequestListAssociationsPaginateTypeDef",
    "ListAssociationsRequestRequestTypeDef",
    "ListAssociationsResponseTypeDef",
    "ListAutoMLJobsRequestListAutoMLJobsPaginateTypeDef",
    "ListAutoMLJobsRequestRequestTypeDef",
    "ListAutoMLJobsResponseTypeDef",
    "ListCandidatesForAutoMLJobRequestListCandidatesForAutoMLJobPaginateTypeDef",
    "ListCandidatesForAutoMLJobRequestRequestTypeDef",
    "ListCandidatesForAutoMLJobResponseTypeDef",
    "ListClusterNodesRequestListClusterNodesPaginateTypeDef",
    "ListClusterNodesRequestRequestTypeDef",
    "ListClusterNodesResponseTypeDef",
    "ListClustersRequestListClustersPaginateTypeDef",
    "ListClustersRequestRequestTypeDef",
    "ListClustersResponseTypeDef",
    "ListCodeRepositoriesInputListCodeRepositoriesPaginateTypeDef",
    "ListCodeRepositoriesInputRequestTypeDef",
    "ListCodeRepositoriesOutputTypeDef",
    "ListCompilationJobsRequestListCompilationJobsPaginateTypeDef",
    "ListCompilationJobsRequestRequestTypeDef",
    "ListCompilationJobsResponseTypeDef",
    "ListContextsRequestListContextsPaginateTypeDef",
    "ListContextsRequestRequestTypeDef",
    "ListContextsResponseTypeDef",
    "ListDataQualityJobDefinitionsRequestListDataQualityJobDefinitionsPaginateTypeDef",
    "ListDataQualityJobDefinitionsRequestRequestTypeDef",
    "ListDataQualityJobDefinitionsResponseTypeDef",
    "ListDeviceFleetsRequestListDeviceFleetsPaginateTypeDef",
    "ListDeviceFleetsRequestRequestTypeDef",
    "ListDeviceFleetsResponseTypeDef",
    "ListDevicesRequestListDevicesPaginateTypeDef",
    "ListDevicesRequestRequestTypeDef",
    "ListDevicesResponseTypeDef",
    "ListDomainsRequestListDomainsPaginateTypeDef",
    "ListDomainsRequestRequestTypeDef",
    "ListDomainsResponseTypeDef",
    "ListEdgeDeploymentPlansRequestListEdgeDeploymentPlansPaginateTypeDef",
    "ListEdgeDeploymentPlansRequestRequestTypeDef",
    "ListEdgeDeploymentPlansResponseTypeDef",
    "ListEdgePackagingJobsRequestListEdgePackagingJobsPaginateTypeDef",
    "ListEdgePackagingJobsRequestRequestTypeDef",
    "ListEdgePackagingJobsResponseTypeDef",
    "ListEndpointConfigsInputListEndpointConfigsPaginateTypeDef",
    "ListEndpointConfigsInputRequestTypeDef",
    "ListEndpointConfigsOutputTypeDef",
    "ListEndpointsInputListEndpointsPaginateTypeDef",
    "ListEndpointsInputRequestTypeDef",
    "ListEndpointsOutputTypeDef",
    "ListExperimentsRequestListExperimentsPaginateTypeDef",
    "ListExperimentsRequestRequestTypeDef",
    "ListExperimentsResponseTypeDef",
    "ListFeatureGroupsRequestListFeatureGroupsPaginateTypeDef",
    "ListFeatureGroupsRequestRequestTypeDef",
    "ListFeatureGroupsResponseTypeDef",
    "ListFlowDefinitionsRequestListFlowDefinitionsPaginateTypeDef",
    "ListFlowDefinitionsRequestRequestTypeDef",
    "ListFlowDefinitionsResponseTypeDef",
    "ListHubContentVersionsRequestRequestTypeDef",
    "ListHubContentVersionsResponseTypeDef",
    "ListHubContentsRequestRequestTypeDef",
    "ListHubContentsResponseTypeDef",
    "ListHubsRequestRequestTypeDef",
    "ListHubsResponseTypeDef",
    "ListHumanTaskUisRequestListHumanTaskUisPaginateTypeDef",
    "ListHumanTaskUisRequestRequestTypeDef",
    "ListHumanTaskUisResponseTypeDef",
    "ListHyperParameterTuningJobsRequestListHyperParameterTuningJobsPaginateTypeDef",
    "ListHyperParameterTuningJobsRequestRequestTypeDef",
    "ListHyperParameterTuningJobsResponseTypeDef",
    "ListImageVersionsRequestListImageVersionsPaginateTypeDef",
    "ListImageVersionsRequestRequestTypeDef",
    "ListImageVersionsResponseTypeDef",
    "ListImagesRequestListImagesPaginateTypeDef",
    "ListImagesRequestRequestTypeDef",
    "ListImagesResponseTypeDef",
    "ListInferenceComponentsInputListInferenceComponentsPaginateTypeDef",
    "ListInferenceComponentsInputRequestTypeDef",
    "ListInferenceComponentsOutputTypeDef",
    "ListInferenceExperimentsRequestListInferenceExperimentsPaginateTypeDef",
    "ListInferenceExperimentsRequestRequestTypeDef",
    "ListInferenceExperimentsResponseTypeDef",
    "ListInferenceRecommendationsJobStepsRequestListInferenceRecommendationsJobStepsPaginateTypeDef",
    "ListInferenceRecommendationsJobStepsRequestRequestTypeDef",
    "ListInferenceRecommendationsJobStepsResponseTypeDef",
    "ListInferenceRecommendationsJobsRequestListInferenceRecommendationsJobsPaginateTypeDef",
    "ListInferenceRecommendationsJobsRequestRequestTypeDef",
    "ListInferenceRecommendationsJobsResponseTypeDef",
    "ListLabelingJobsForWorkteamRequestListLabelingJobsForWorkteamPaginateTypeDef",
    "ListLabelingJobsForWorkteamRequestRequestTypeDef",
    "ListLabelingJobsForWorkteamResponseTypeDef",
    "ListLabelingJobsRequestListLabelingJobsPaginateTypeDef",
    "ListLabelingJobsRequestRequestTypeDef",
    "ListLabelingJobsResponseTypeDef",
    "ListLineageGroupsRequestListLineageGroupsPaginateTypeDef",
    "ListLineageGroupsRequestRequestTypeDef",
    "ListLineageGroupsResponseTypeDef",
    "ListMlflowTrackingServersRequestListMlflowTrackingServersPaginateTypeDef",
    "ListMlflowTrackingServersRequestRequestTypeDef",
    "ListMlflowTrackingServersResponseTypeDef",
    "ListModelBiasJobDefinitionsRequestListModelBiasJobDefinitionsPaginateTypeDef",
    "ListModelBiasJobDefinitionsRequestRequestTypeDef",
    "ListModelBiasJobDefinitionsResponseTypeDef",
    "ListModelCardExportJobsRequestListModelCardExportJobsPaginateTypeDef",
    "ListModelCardExportJobsRequestRequestTypeDef",
    "ListModelCardExportJobsResponseTypeDef",
    "ListModelCardVersionsRequestListModelCardVersionsPaginateTypeDef",
    "ListModelCardVersionsRequestRequestTypeDef",
    "ListModelCardVersionsResponseTypeDef",
    "ListModelCardsRequestListModelCardsPaginateTypeDef",
    "ListModelCardsRequestRequestTypeDef",
    "ListModelCardsResponseTypeDef",
    "ListModelExplainabilityJobDefinitionsRequestListModelExplainabilityJobDefinitionsPaginateTypeDef",
    "ListModelExplainabilityJobDefinitionsRequestRequestTypeDef",
    "ListModelExplainabilityJobDefinitionsResponseTypeDef",
    "ListModelMetadataRequestListModelMetadataPaginateTypeDef",
    "ListModelMetadataRequestRequestTypeDef",
    "ListModelMetadataResponseTypeDef",
    "ListModelPackageGroupsInputListModelPackageGroupsPaginateTypeDef",
    "ListModelPackageGroupsInputRequestTypeDef",
    "ListModelPackageGroupsOutputTypeDef",
    "ListModelPackagesInputListModelPackagesPaginateTypeDef",
    "ListModelPackagesInputRequestTypeDef",
    "ListModelPackagesOutputTypeDef",
    "ListModelQualityJobDefinitionsRequestListModelQualityJobDefinitionsPaginateTypeDef",
    "ListModelQualityJobDefinitionsRequestRequestTypeDef",
    "ListModelQualityJobDefinitionsResponseTypeDef",
    "ListModelsInputListModelsPaginateTypeDef",
    "ListModelsInputRequestTypeDef",
    "ListModelsOutputTypeDef",
    "ListMonitoringAlertHistoryRequestListMonitoringAlertHistoryPaginateTypeDef",
    "ListMonitoringAlertHistoryRequestRequestTypeDef",
    "ListMonitoringAlertHistoryResponseTypeDef",
    "ListMonitoringAlertsRequestListMonitoringAlertsPaginateTypeDef",
    "ListMonitoringAlertsRequestRequestTypeDef",
    "ListMonitoringAlertsResponseTypeDef",
    "ListMonitoringExecutionsRequestListMonitoringExecutionsPaginateTypeDef",
    "ListMonitoringExecutionsRequestRequestTypeDef",
    "ListMonitoringExecutionsResponseTypeDef",
    "ListMonitoringSchedulesRequestListMonitoringSchedulesPaginateTypeDef",
    "ListMonitoringSchedulesRequestRequestTypeDef",
    "ListMonitoringSchedulesResponseTypeDef",
    "ListNotebookInstanceLifecycleConfigsInputListNotebookInstanceLifecycleConfigsPaginateTypeDef",
    "ListNotebookInstanceLifecycleConfigsInputRequestTypeDef",
    "ListNotebookInstanceLifecycleConfigsOutputTypeDef",
    "ListNotebookInstancesInputListNotebookInstancesPaginateTypeDef",
    "ListNotebookInstancesInputRequestTypeDef",
    "ListNotebookInstancesOutputTypeDef",
    "ListOptimizationJobsRequestListOptimizationJobsPaginateTypeDef",
    "ListOptimizationJobsRequestRequestTypeDef",
    "ListOptimizationJobsResponseTypeDef",
    "ListPipelineExecutionStepsRequestListPipelineExecutionStepsPaginateTypeDef",
    "ListPipelineExecutionStepsRequestRequestTypeDef",
    "ListPipelineExecutionStepsResponseTypeDef",
    "ListPipelineExecutionsRequestListPipelineExecutionsPaginateTypeDef",
    "ListPipelineExecutionsRequestRequestTypeDef",
    "ListPipelineExecutionsResponseTypeDef",
    "ListPipelineParametersForExecutionRequestListPipelineParametersForExecutionPaginateTypeDef",
    "ListPipelineParametersForExecutionRequestRequestTypeDef",
    "ListPipelineParametersForExecutionResponseTypeDef",
    "ListPipelinesRequestListPipelinesPaginateTypeDef",
    "ListPipelinesRequestRequestTypeDef",
    "ListPipelinesResponseTypeDef",
    "ListProcessingJobsRequestListProcessingJobsPaginateTypeDef",
    "ListProcessingJobsRequestRequestTypeDef",
    "ListProcessingJobsResponseTypeDef",
    "ListProjectsInputRequestTypeDef",
    "ListProjectsOutputTypeDef",
    "ListResourceCatalogsRequestListResourceCatalogsPaginateTypeDef",
    "ListResourceCatalogsRequestRequestTypeDef",
    "ListResourceCatalogsResponseTypeDef",
    "ListSpacesRequestListSpacesPaginateTypeDef",
    "ListSpacesRequestRequestTypeDef",
    "ListSpacesResponseTypeDef",
    "ListStageDevicesRequestListStageDevicesPaginateTypeDef",
    "ListStageDevicesRequestRequestTypeDef",
    "ListStageDevicesResponseTypeDef",
    "ListStudioLifecycleConfigsRequestListStudioLifecycleConfigsPaginateTypeDef",
    "ListStudioLifecycleConfigsRequestRequestTypeDef",
    "ListStudioLifecycleConfigsResponseTypeDef",
    "ListSubscribedWorkteamsRequestListSubscribedWorkteamsPaginateTypeDef",
    "ListSubscribedWorkteamsRequestRequestTypeDef",
    "ListSubscribedWorkteamsResponseTypeDef",
    "ListTagsInputListTagsPaginateTypeDef",
    "ListTagsInputRequestTypeDef",
    "ListTagsOutputTypeDef",
    "ListTrainingJobsForHyperParameterTuningJobRequestListTrainingJobsForHyperParameterTuningJobPaginateTypeDef",
    "ListTrainingJobsForHyperParameterTuningJobRequestRequestTypeDef",
    "ListTrainingJobsForHyperParameterTuningJobResponseTypeDef",
    "ListTrainingJobsRequestListTrainingJobsPaginateTypeDef",
    "ListTrainingJobsRequestRequestTypeDef",
    "ListTrainingJobsResponseTypeDef",
    "ListTransformJobsRequestListTransformJobsPaginateTypeDef",
    "ListTransformJobsRequestRequestTypeDef",
    "ListTransformJobsResponseTypeDef",
    "ListTrialComponentsRequestListTrialComponentsPaginateTypeDef",
    "ListTrialComponentsRequestRequestTypeDef",
    "ListTrialComponentsResponseTypeDef",
    "ListTrialsRequestListTrialsPaginateTypeDef",
    "ListTrialsRequestRequestTypeDef",
    "ListTrialsResponseTypeDef",
    "ListUserProfilesRequestListUserProfilesPaginateTypeDef",
    "ListUserProfilesRequestRequestTypeDef",
    "ListUserProfilesResponseTypeDef",
    "ListWorkforcesRequestListWorkforcesPaginateTypeDef",
    "ListWorkforcesRequestRequestTypeDef",
    "ListWorkforcesResponseTypeDef",
    "ListWorkteamsRequestListWorkteamsPaginateTypeDef",
    "ListWorkteamsRequestRequestTypeDef",
    "ListWorkteamsResponseTypeDef",
    "MemberDefinitionOutputTypeDef",
    "MemberDefinitionTypeDef",
    "MemberDefinitionUnionTypeDef",
    "MetadataPropertiesTypeDef",
    "MetricDataTypeDef",
    "MetricDatumTypeDef",
    "MetricDefinitionTypeDef",
    "MetricSpecificationTypeDef",
    "MetricsSourceTypeDef",
    "ModelAccessConfigTypeDef",
    "ModelArtifactsTypeDef",
    "ModelBiasAppSpecificationOutputTypeDef",
    "ModelBiasAppSpecificationTypeDef",
    "ModelBiasBaselineConfigTypeDef",
    "ModelBiasJobInputOutputTypeDef",
    "ModelBiasJobInputTypeDef",
    "ModelCardExportArtifactsTypeDef",
    "ModelCardExportJobSummaryTypeDef",
    "ModelCardExportOutputConfigTypeDef",
    "ModelCardSecurityConfigTypeDef",
    "ModelCardSummaryTypeDef",
    "ModelCardTypeDef",
    "ModelCardVersionSummaryTypeDef",
    "ModelClientConfigTypeDef",
    "ModelCompilationConfigOutputTypeDef",
    "ModelCompilationConfigTypeDef",
    "ModelCompilationConfigUnionTypeDef",
    "ModelConfigurationTypeDef",
    "ModelDashboardEndpointTypeDef",
    "ModelDashboardIndicatorActionTypeDef",
    "ModelDashboardModelCardTypeDef",
    "ModelDashboardModelTypeDef",
    "ModelDashboardMonitoringScheduleTypeDef",
    "ModelDataQualityTypeDef",
    "ModelDataSourceTypeDef",
    "ModelDeployConfigTypeDef",
    "ModelDeployResultTypeDef",
    "ModelDigestsTypeDef",
    "ModelExplainabilityAppSpecificationOutputTypeDef",
    "ModelExplainabilityAppSpecificationTypeDef",
    "ModelExplainabilityBaselineConfigTypeDef",
    "ModelExplainabilityJobInputOutputTypeDef",
    "ModelExplainabilityJobInputTypeDef",
    "ModelInfrastructureConfigTypeDef",
    "ModelInputTypeDef",
    "ModelLatencyThresholdTypeDef",
    "ModelLifeCycleTypeDef",
    "ModelMetadataFilterTypeDef",
    "ModelMetadataSearchExpressionTypeDef",
    "ModelMetadataSummaryTypeDef",
    "ModelMetricsTypeDef",
    "ModelPackageContainerDefinitionOutputTypeDef",
    "ModelPackageContainerDefinitionTypeDef",
    "ModelPackageContainerDefinitionUnionTypeDef",
    "ModelPackageGroupSummaryTypeDef",
    "ModelPackageGroupTypeDef",
    "ModelPackageModelCardTypeDef",
    "ModelPackageSecurityConfigTypeDef",
    "ModelPackageStatusDetailsTypeDef",
    "ModelPackageStatusItemTypeDef",
    "ModelPackageSummaryTypeDef",
    "ModelPackageTypeDef",
    "ModelPackageValidationProfileOutputTypeDef",
    "ModelPackageValidationProfileTypeDef",
    "ModelPackageValidationProfileUnionTypeDef",
    "ModelPackageValidationSpecificationOutputTypeDef",
    "ModelPackageValidationSpecificationTypeDef",
    "ModelQualityAppSpecificationOutputTypeDef",
    "ModelQualityAppSpecificationTypeDef",
    "ModelQualityBaselineConfigTypeDef",
    "ModelQualityJobInputOutputTypeDef",
    "ModelQualityJobInputTypeDef",
    "ModelQualityTypeDef",
    "ModelQuantizationConfigOutputTypeDef",
    "ModelQuantizationConfigTypeDef",
    "ModelQuantizationConfigUnionTypeDef",
    "ModelRegisterSettingsTypeDef",
    "ModelShardingConfigOutputTypeDef",
    "ModelShardingConfigTypeDef",
    "ModelShardingConfigUnionTypeDef",
    "ModelStepMetadataTypeDef",
    "ModelSummaryTypeDef",
    "ModelTypeDef",
    "ModelVariantConfigSummaryTypeDef",
    "ModelVariantConfigTypeDef",
    "MonitoringAlertActionsTypeDef",
    "MonitoringAlertHistorySummaryTypeDef",
    "MonitoringAlertSummaryTypeDef",
    "MonitoringAppSpecificationOutputTypeDef",
    "MonitoringAppSpecificationTypeDef",
    "MonitoringAppSpecificationUnionTypeDef",
    "MonitoringBaselineConfigTypeDef",
    "MonitoringClusterConfigTypeDef",
    "MonitoringConstraintsResourceTypeDef",
    "MonitoringCsvDatasetFormatTypeDef",
    "MonitoringDatasetFormatOutputTypeDef",
    "MonitoringDatasetFormatTypeDef",
    "MonitoringDatasetFormatUnionTypeDef",
    "MonitoringExecutionSummaryTypeDef",
    "MonitoringGroundTruthS3InputTypeDef",
    "MonitoringInputOutputTypeDef",
    "MonitoringInputTypeDef",
    "MonitoringInputUnionTypeDef",
    "MonitoringJobDefinitionOutputTypeDef",
    "MonitoringJobDefinitionSummaryTypeDef",
    "MonitoringJobDefinitionTypeDef",
    "MonitoringJobDefinitionUnionTypeDef",
    "MonitoringJsonDatasetFormatTypeDef",
    "MonitoringNetworkConfigOutputTypeDef",
    "MonitoringNetworkConfigTypeDef",
    "MonitoringOutputConfigOutputTypeDef",
    "MonitoringOutputConfigTypeDef",
    "MonitoringOutputConfigUnionTypeDef",
    "MonitoringOutputTypeDef",
    "MonitoringResourcesTypeDef",
    "MonitoringS3OutputTypeDef",
    "MonitoringScheduleConfigOutputTypeDef",
    "MonitoringScheduleConfigTypeDef",
    "MonitoringScheduleSummaryTypeDef",
    "MonitoringScheduleTypeDef",
    "MonitoringStatisticsResourceTypeDef",
    "MonitoringStoppingConditionTypeDef",
    "MultiModelConfigTypeDef",
    "NeoVpcConfigOutputTypeDef",
    "NeoVpcConfigTypeDef",
    "NestedFiltersTypeDef",
    "NetworkConfigOutputTypeDef",
    "NetworkConfigTypeDef",
    "NetworkConfigUnionTypeDef",
    "NotebookInstanceLifecycleConfigSummaryTypeDef",
    "NotebookInstanceLifecycleHookTypeDef",
    "NotebookInstanceSummaryTypeDef",
    "NotificationConfigurationTypeDef",
    "ObjectiveStatusCountersTypeDef",
    "OfflineStoreConfigTypeDef",
    "OfflineStoreStatusTypeDef",
    "OidcConfigForResponseTypeDef",
    "OidcConfigTypeDef",
    "OidcMemberDefinitionOutputTypeDef",
    "OidcMemberDefinitionTypeDef",
    "OidcMemberDefinitionUnionTypeDef",
    "OnlineStoreConfigTypeDef",
    "OnlineStoreConfigUpdateTypeDef",
    "OnlineStoreSecurityConfigTypeDef",
    "OptimizationConfigOutputTypeDef",
    "OptimizationConfigTypeDef",
    "OptimizationConfigUnionTypeDef",
    "OptimizationJobModelSourceS3TypeDef",
    "OptimizationJobModelSourceTypeDef",
    "OptimizationJobOutputConfigTypeDef",
    "OptimizationJobSummaryTypeDef",
    "OptimizationModelAccessConfigTypeDef",
    "OptimizationOutputTypeDef",
    "OptimizationVpcConfigOutputTypeDef",
    "OptimizationVpcConfigTypeDef",
    "OutputConfigTypeDef",
    "OutputDataConfigTypeDef",
    "OutputParameterTypeDef",
    "OwnershipSettingsSummaryTypeDef",
    "OwnershipSettingsTypeDef",
    "PaginatorConfigTypeDef",
    "ParallelismConfigurationTypeDef",
    "ParameterRangeOutputTypeDef",
    "ParameterRangeTypeDef",
    "ParameterRangeUnionTypeDef",
    "ParameterRangesOutputTypeDef",
    "ParameterRangesTypeDef",
    "ParameterRangesUnionTypeDef",
    "ParameterTypeDef",
    "ParentHyperParameterTuningJobTypeDef",
    "ParentTypeDef",
    "PendingDeploymentSummaryTypeDef",
    "PendingProductionVariantSummaryTypeDef",
    "PhaseTypeDef",
    "PipelineDefinitionS3LocationTypeDef",
    "PipelineExecutionStepMetadataTypeDef",
    "PipelineExecutionStepTypeDef",
    "PipelineExecutionSummaryTypeDef",
    "PipelineExecutionTypeDef",
    "PipelineExperimentConfigTypeDef",
    "PipelineSummaryTypeDef",
    "PipelineTypeDef",
    "PredefinedMetricSpecificationTypeDef",
    "ProcessingClusterConfigTypeDef",
    "ProcessingFeatureStoreOutputTypeDef",
    "ProcessingInputTypeDef",
    "ProcessingJobStepMetadataTypeDef",
    "ProcessingJobSummaryTypeDef",
    "ProcessingJobTypeDef",
    "ProcessingOutputConfigOutputTypeDef",
    "ProcessingOutputConfigTypeDef",
    "ProcessingOutputTypeDef",
    "ProcessingResourcesTypeDef",
    "ProcessingS3InputTypeDef",
    "ProcessingS3OutputTypeDef",
    "ProcessingStoppingConditionTypeDef",
    "ProductionVariantCoreDumpConfigTypeDef",
    "ProductionVariantManagedInstanceScalingTypeDef",
    "ProductionVariantRoutingConfigTypeDef",
    "ProductionVariantServerlessConfigTypeDef",
    "ProductionVariantServerlessUpdateConfigTypeDef",
    "ProductionVariantStatusTypeDef",
    "ProductionVariantSummaryTypeDef",
    "ProductionVariantTypeDef",
    "ProfilerConfigForUpdateTypeDef",
    "ProfilerConfigOutputTypeDef",
    "ProfilerConfigTypeDef",
    "ProfilerRuleConfigurationOutputTypeDef",
    "ProfilerRuleConfigurationTypeDef",
    "ProfilerRuleConfigurationUnionTypeDef",
    "ProfilerRuleEvaluationStatusTypeDef",
    "ProjectSummaryTypeDef",
    "ProjectTypeDef",
    "PropertyNameQueryTypeDef",
    "PropertyNameSuggestionTypeDef",
    "ProvisioningParameterTypeDef",
    "PublicWorkforceTaskPriceTypeDef",
    "PutModelPackageGroupPolicyInputRequestTypeDef",
    "PutModelPackageGroupPolicyOutputTypeDef",
    "QualityCheckStepMetadataTypeDef",
    "QueryFiltersTypeDef",
    "QueryLineageRequestRequestTypeDef",
    "QueryLineageResponseTypeDef",
    "RSessionAppSettingsOutputTypeDef",
    "RSessionAppSettingsTypeDef",
    "RSessionAppSettingsUnionTypeDef",
    "RStudioServerProAppSettingsTypeDef",
    "RStudioServerProDomainSettingsForUpdateTypeDef",
    "RStudioServerProDomainSettingsTypeDef",
    "RealTimeInferenceConfigTypeDef",
    "RealTimeInferenceRecommendationTypeDef",
    "RecommendationJobCompiledOutputConfigTypeDef",
    "RecommendationJobContainerConfigOutputTypeDef",
    "RecommendationJobContainerConfigTypeDef",
    "RecommendationJobContainerConfigUnionTypeDef",
    "RecommendationJobInferenceBenchmarkTypeDef",
    "RecommendationJobInputConfigOutputTypeDef",
    "RecommendationJobInputConfigTypeDef",
    "RecommendationJobOutputConfigTypeDef",
    "RecommendationJobPayloadConfigOutputTypeDef",
    "RecommendationJobPayloadConfigTypeDef",
    "RecommendationJobPayloadConfigUnionTypeDef",
    "RecommendationJobResourceLimitTypeDef",
    "RecommendationJobStoppingConditionsOutputTypeDef",
    "RecommendationJobStoppingConditionsTypeDef",
    "RecommendationJobVpcConfigOutputTypeDef",
    "RecommendationJobVpcConfigTypeDef",
    "RecommendationJobVpcConfigUnionTypeDef",
    "RecommendationMetricsTypeDef",
    "RedshiftDatasetDefinitionTypeDef",
    "RegisterDevicesRequestRequestTypeDef",
    "RegisterModelStepMetadataTypeDef",
    "RemoteDebugConfigForUpdateTypeDef",
    "RemoteDebugConfigTypeDef",
    "RenderUiTemplateRequestRequestTypeDef",
    "RenderUiTemplateResponseTypeDef",
    "RenderableTaskTypeDef",
    "RenderingErrorTypeDef",
    "RepositoryAuthConfigTypeDef",
    "ResolvedAttributesTypeDef",
    "ResourceCatalogTypeDef",
    "ResourceConfigForUpdateTypeDef",
    "ResourceConfigOutputTypeDef",
    "ResourceConfigTypeDef",
    "ResourceConfigUnionTypeDef",
    "ResourceLimitsTypeDef",
    "ResourceSpecTypeDef",
    "ResponseMetadataTypeDef",
    "RetentionPolicyTypeDef",
    "RetryPipelineExecutionRequestRequestTypeDef",
    "RetryPipelineExecutionResponseTypeDef",
    "RetryStrategyTypeDef",
    "RollingUpdatePolicyTypeDef",
    "S3DataSourceOutputTypeDef",
    "S3DataSourceTypeDef",
    "S3DataSourceUnionTypeDef",
    "S3ModelDataSourceTypeDef",
    "S3PresignTypeDef",
    "S3StorageConfigTypeDef",
    "ScalingPolicyMetricTypeDef",
    "ScalingPolicyObjectiveTypeDef",
    "ScalingPolicyTypeDef",
    "ScheduleConfigTypeDef",
    "SearchExpressionPaginatorTypeDef",
    "SearchExpressionTypeDef",
    "SearchRecordTypeDef",
    "SearchRequestRequestTypeDef",
    "SearchRequestSearchPaginateTypeDef",
    "SearchResponseTypeDef",
    "SecondaryStatusTransitionTypeDef",
    "SelectedStepTypeDef",
    "SelectiveExecutionConfigOutputTypeDef",
    "SelectiveExecutionConfigTypeDef",
    "SelectiveExecutionResultTypeDef",
    "SendPipelineExecutionStepFailureRequestRequestTypeDef",
    "SendPipelineExecutionStepFailureResponseTypeDef",
    "SendPipelineExecutionStepSuccessRequestRequestTypeDef",
    "SendPipelineExecutionStepSuccessResponseTypeDef",
    "ServiceCatalogProvisionedProductDetailsTypeDef",
    "ServiceCatalogProvisioningDetailsOutputTypeDef",
    "ServiceCatalogProvisioningDetailsTypeDef",
    "ServiceCatalogProvisioningUpdateDetailsTypeDef",
    "SessionChainingConfigTypeDef",
    "ShadowModeConfigOutputTypeDef",
    "ShadowModeConfigTypeDef",
    "ShadowModelVariantConfigTypeDef",
    "SharingSettingsTypeDef",
    "ShuffleConfigTypeDef",
    "SourceAlgorithmSpecificationOutputTypeDef",
    "SourceAlgorithmSpecificationTypeDef",
    "SourceAlgorithmTypeDef",
    "SourceIpConfigOutputTypeDef",
    "SourceIpConfigTypeDef",
    "SpaceAppLifecycleManagementTypeDef",
    "SpaceCodeEditorAppSettingsTypeDef",
    "SpaceDetailsTypeDef",
    "SpaceIdleSettingsTypeDef",
    "SpaceJupyterLabAppSettingsOutputTypeDef",
    "SpaceJupyterLabAppSettingsTypeDef",
    "SpaceJupyterLabAppSettingsUnionTypeDef",
    "SpaceSettingsOutputTypeDef",
    "SpaceSettingsSummaryTypeDef",
    "SpaceSettingsTypeDef",
    "SpaceSharingSettingsSummaryTypeDef",
    "SpaceSharingSettingsTypeDef",
    "SpaceStorageSettingsTypeDef",
    "StairsTypeDef",
    "StartEdgeDeploymentStageRequestRequestTypeDef",
    "StartInferenceExperimentRequestRequestTypeDef",
    "StartInferenceExperimentResponseTypeDef",
    "StartMlflowTrackingServerRequestRequestTypeDef",
    "StartMlflowTrackingServerResponseTypeDef",
    "StartMonitoringScheduleRequestRequestTypeDef",
    "StartNotebookInstanceInputRequestTypeDef",
    "StartPipelineExecutionRequestRequestTypeDef",
    "StartPipelineExecutionResponseTypeDef",
    "StopAutoMLJobRequestRequestTypeDef",
    "StopCompilationJobRequestRequestTypeDef",
    "StopEdgeDeploymentStageRequestRequestTypeDef",
    "StopEdgePackagingJobRequestRequestTypeDef",
    "StopHyperParameterTuningJobRequestRequestTypeDef",
    "StopInferenceExperimentRequestRequestTypeDef",
    "StopInferenceExperimentResponseTypeDef",
    "StopInferenceRecommendationsJobRequestRequestTypeDef",
    "StopLabelingJobRequestRequestTypeDef",
    "StopMlflowTrackingServerRequestRequestTypeDef",
    "StopMlflowTrackingServerResponseTypeDef",
    "StopMonitoringScheduleRequestRequestTypeDef",
    "StopNotebookInstanceInputRequestTypeDef",
    "StopOptimizationJobRequestRequestTypeDef",
    "StopPipelineExecutionRequestRequestTypeDef",
    "StopPipelineExecutionResponseTypeDef",
    "StopProcessingJobRequestRequestTypeDef",
    "StopTrainingJobRequestRequestTypeDef",
    "StopTransformJobRequestRequestTypeDef",
    "StoppingConditionTypeDef",
    "StudioLifecycleConfigDetailsTypeDef",
    "StudioWebPortalSettingsOutputTypeDef",
    "StudioWebPortalSettingsTypeDef",
    "StudioWebPortalSettingsUnionTypeDef",
    "SubscribedWorkteamTypeDef",
    "SuggestionQueryTypeDef",
    "TabularJobConfigOutputTypeDef",
    "TabularJobConfigTypeDef",
    "TabularJobConfigUnionTypeDef",
    "TabularResolvedAttributesTypeDef",
    "TagTypeDef",
    "TargetPlatformTypeDef",
    "TargetTrackingScalingPolicyConfigurationTypeDef",
    "TensorBoardAppSettingsTypeDef",
    "TensorBoardOutputConfigTypeDef",
    "TextClassificationJobConfigTypeDef",
    "TextGenerationJobConfigOutputTypeDef",
    "TextGenerationJobConfigTypeDef",
    "TextGenerationJobConfigUnionTypeDef",
    "TextGenerationResolvedAttributesTypeDef",
    "ThroughputConfigDescriptionTypeDef",
    "ThroughputConfigTypeDef",
    "ThroughputConfigUpdateTypeDef",
    "TimeSeriesConfigOutputTypeDef",
    "TimeSeriesConfigTypeDef",
    "TimeSeriesConfigUnionTypeDef",
    "TimeSeriesForecastingJobConfigOutputTypeDef",
    "TimeSeriesForecastingJobConfigTypeDef",
    "TimeSeriesForecastingJobConfigUnionTypeDef",
    "TimeSeriesForecastingSettingsTypeDef",
    "TimeSeriesTransformationsOutputTypeDef",
    "TimeSeriesTransformationsTypeDef",
    "TimeSeriesTransformationsUnionTypeDef",
    "TimestampTypeDef",
    "TrackingServerSummaryTypeDef",
    "TrafficPatternOutputTypeDef",
    "TrafficPatternTypeDef",
    "TrafficPatternUnionTypeDef",
    "TrafficRoutingConfigTypeDef",
    "TrainingImageConfigTypeDef",
    "TrainingJobDefinitionOutputTypeDef",
    "TrainingJobDefinitionTypeDef",
    "TrainingJobDefinitionUnionTypeDef",
    "TrainingJobStatusCountersTypeDef",
    "TrainingJobStepMetadataTypeDef",
    "TrainingJobSummaryTypeDef",
    "TrainingJobTypeDef",
    "TrainingRepositoryAuthConfigTypeDef",
    "TrainingSpecificationOutputTypeDef",
    "TrainingSpecificationTypeDef",
    "TransformDataSourceTypeDef",
    "TransformInputTypeDef",
    "TransformJobDefinitionOutputTypeDef",
    "TransformJobDefinitionTypeDef",
    "TransformJobDefinitionUnionTypeDef",
    "TransformJobStepMetadataTypeDef",
    "TransformJobSummaryTypeDef",
    "TransformJobTypeDef",
    "TransformOutputTypeDef",
    "TransformResourcesTypeDef",
    "TransformS3DataSourceTypeDef",
    "TrialComponentArtifactTypeDef",
    "TrialComponentMetricSummaryTypeDef",
    "TrialComponentParameterValueTypeDef",
    "TrialComponentSimpleSummaryTypeDef",
    "TrialComponentSourceDetailTypeDef",
    "TrialComponentSourceTypeDef",
    "TrialComponentStatusTypeDef",
    "TrialComponentSummaryTypeDef",
    "TrialComponentTypeDef",
    "TrialSourceTypeDef",
    "TrialSummaryTypeDef",
    "TrialTypeDef",
    "TtlDurationTypeDef",
    "TuningJobCompletionCriteriaTypeDef",
    "TuningJobStepMetaDataTypeDef",
    "USDTypeDef",
    "UiConfigTypeDef",
    "UiTemplateInfoTypeDef",
    "UiTemplateTypeDef",
    "UpdateActionRequestRequestTypeDef",
    "UpdateActionResponseTypeDef",
    "UpdateAppImageConfigRequestRequestTypeDef",
    "UpdateAppImageConfigResponseTypeDef",
    "UpdateArtifactRequestRequestTypeDef",
    "UpdateArtifactResponseTypeDef",
    "UpdateClusterRequestRequestTypeDef",
    "UpdateClusterResponseTypeDef",
    "UpdateClusterSoftwareRequestRequestTypeDef",
    "UpdateClusterSoftwareResponseTypeDef",
    "UpdateCodeRepositoryInputRequestTypeDef",
    "UpdateCodeRepositoryOutputTypeDef",
    "UpdateContextRequestRequestTypeDef",
    "UpdateContextResponseTypeDef",
    "UpdateDeviceFleetRequestRequestTypeDef",
    "UpdateDevicesRequestRequestTypeDef",
    "UpdateDomainRequestRequestTypeDef",
    "UpdateDomainResponseTypeDef",
    "UpdateEndpointInputRequestTypeDef",
    "UpdateEndpointOutputTypeDef",
    "UpdateEndpointWeightsAndCapacitiesInputRequestTypeDef",
    "UpdateEndpointWeightsAndCapacitiesOutputTypeDef",
    "UpdateExperimentRequestRequestTypeDef",
    "UpdateExperimentResponseTypeDef",
    "UpdateFeatureGroupRequestRequestTypeDef",
    "UpdateFeatureGroupResponseTypeDef",
    "UpdateFeatureMetadataRequestRequestTypeDef",
    "UpdateHubRequestRequestTypeDef",
    "UpdateHubResponseTypeDef",
    "UpdateImageRequestRequestTypeDef",
    "UpdateImageResponseTypeDef",
    "UpdateImageVersionRequestRequestTypeDef",
    "UpdateImageVersionResponseTypeDef",
    "UpdateInferenceComponentInputRequestTypeDef",
    "UpdateInferenceComponentOutputTypeDef",
    "UpdateInferenceComponentRuntimeConfigInputRequestTypeDef",
    "UpdateInferenceComponentRuntimeConfigOutputTypeDef",
    "UpdateInferenceExperimentRequestRequestTypeDef",
    "UpdateInferenceExperimentResponseTypeDef",
    "UpdateMlflowTrackingServerRequestRequestTypeDef",
    "UpdateMlflowTrackingServerResponseTypeDef",
    "UpdateModelCardRequestRequestTypeDef",
    "UpdateModelCardResponseTypeDef",
    "UpdateModelPackageInputRequestTypeDef",
    "UpdateModelPackageOutputTypeDef",
    "UpdateMonitoringAlertRequestRequestTypeDef",
    "UpdateMonitoringAlertResponseTypeDef",
    "UpdateMonitoringScheduleRequestRequestTypeDef",
    "UpdateMonitoringScheduleResponseTypeDef",
    "UpdateNotebookInstanceInputRequestTypeDef",
    "UpdateNotebookInstanceLifecycleConfigInputRequestTypeDef",
    "UpdatePipelineExecutionRequestRequestTypeDef",
    "UpdatePipelineExecutionResponseTypeDef",
    "UpdatePipelineRequestRequestTypeDef",
    "UpdatePipelineResponseTypeDef",
    "UpdateProjectInputRequestTypeDef",
    "UpdateProjectOutputTypeDef",
    "UpdateSpaceRequestRequestTypeDef",
    "UpdateSpaceResponseTypeDef",
    "UpdateTrainingJobRequestRequestTypeDef",
    "UpdateTrainingJobResponseTypeDef",
    "UpdateTrialComponentRequestRequestTypeDef",
    "UpdateTrialComponentResponseTypeDef",
    "UpdateTrialRequestRequestTypeDef",
    "UpdateTrialResponseTypeDef",
    "UpdateUserProfileRequestRequestTypeDef",
    "UpdateUserProfileResponseTypeDef",
    "UpdateWorkforceRequestRequestTypeDef",
    "UpdateWorkforceResponseTypeDef",
    "UpdateWorkteamRequestRequestTypeDef",
    "UpdateWorkteamResponseTypeDef",
    "UserContextTypeDef",
    "UserProfileDetailsTypeDef",
    "UserSettingsOutputTypeDef",
    "UserSettingsTypeDef",
    "VariantPropertyTypeDef",
    "VectorConfigTypeDef",
    "VertexTypeDef",
    "VisibilityConditionsTypeDef",
    "VpcConfigOutputTypeDef",
    "VpcConfigTypeDef",
    "VpcConfigUnionTypeDef",
    "WaiterConfigTypeDef",
    "WarmPoolStatusTypeDef",
    "WorkerAccessConfigurationTypeDef",
    "WorkforceTypeDef",
    "WorkforceVpcConfigRequestTypeDef",
    "WorkforceVpcConfigResponseTypeDef",
    "WorkspaceSettingsTypeDef",
    "WorkteamTypeDef",
)


class ActionSourceTypeDef(TypedDict):
    SourceUri: str
    SourceType: NotRequired[str]
    SourceId: NotRequired[str]


class AddAssociationRequestRequestTypeDef(TypedDict):
    SourceArn: str
    DestinationArn: str
    AssociationType: NotRequired[AssociationEdgeTypeType]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class TagTypeDef(TypedDict):
    Key: str
    Value: str


class AdditionalS3DataSourceTypeDef(TypedDict):
    S3DataType: AdditionalS3DataSourceDataTypeType
    S3Uri: str
    CompressionType: NotRequired[CompressionTypeType]


class AgentVersionTypeDef(TypedDict):
    Version: str
    AgentCount: int


class AlarmTypeDef(TypedDict):
    AlarmName: NotRequired[str]


class MetricDefinitionTypeDef(TypedDict):
    Name: str
    Regex: str


class AlgorithmStatusItemTypeDef(TypedDict):
    Name: str
    Status: DetailedAlgorithmStatusType
    FailureReason: NotRequired[str]


class AlgorithmSummaryTypeDef(TypedDict):
    AlgorithmName: str
    AlgorithmArn: str
    CreationTime: datetime
    AlgorithmStatus: AlgorithmStatusType
    AlgorithmDescription: NotRequired[str]


class AmazonQSettingsTypeDef(TypedDict):
    Status: NotRequired[FeatureStatusType]
    QProfileArn: NotRequired[str]


class AnnotationConsolidationConfigTypeDef(TypedDict):
    AnnotationConsolidationLambdaArn: str


class ResourceSpecTypeDef(TypedDict):
    SageMakerImageArn: NotRequired[str]
    SageMakerImageVersionArn: NotRequired[str]
    SageMakerImageVersionAlias: NotRequired[str]
    InstanceType: NotRequired[AppInstanceTypeType]
    LifecycleConfigArn: NotRequired[str]


class IdleSettingsTypeDef(TypedDict):
    LifecycleManagement: NotRequired[LifecycleManagementType]
    IdleTimeoutInMinutes: NotRequired[int]
    MinIdleTimeoutInMinutes: NotRequired[int]
    MaxIdleTimeoutInMinutes: NotRequired[int]


class AppSpecificationOutputTypeDef(TypedDict):
    ImageUri: str
    ContainerEntrypoint: NotRequired[List[str]]
    ContainerArguments: NotRequired[List[str]]


class AppSpecificationTypeDef(TypedDict):
    ImageUri: str
    ContainerEntrypoint: NotRequired[Sequence[str]]
    ContainerArguments: NotRequired[Sequence[str]]


class ArtifactSourceTypeTypeDef(TypedDict):
    SourceIdType: ArtifactSourceIdTypeType
    Value: str


class AssociateTrialComponentRequestRequestTypeDef(TypedDict):
    TrialComponentName: str
    TrialName: str


class AsyncInferenceClientConfigTypeDef(TypedDict):
    MaxConcurrentInvocationsPerInstance: NotRequired[int]


class AsyncInferenceNotificationConfigOutputTypeDef(TypedDict):
    SuccessTopic: NotRequired[str]
    ErrorTopic: NotRequired[str]
    IncludeInferenceResponseIn: NotRequired[List[AsyncNotificationTopicTypesType]]


class AsyncInferenceNotificationConfigTypeDef(TypedDict):
    SuccessTopic: NotRequired[str]
    ErrorTopic: NotRequired[str]
    IncludeInferenceResponseIn: NotRequired[Sequence[AsyncNotificationTopicTypesType]]


class AthenaDatasetDefinitionTypeDef(TypedDict):
    Catalog: str
    Database: str
    QueryString: str
    OutputS3Uri: str
    OutputFormat: AthenaResultFormatType
    WorkGroup: NotRequired[str]
    KmsKeyId: NotRequired[str]
    OutputCompression: NotRequired[AthenaResultCompressionTypeType]


class AutoMLAlgorithmConfigOutputTypeDef(TypedDict):
    AutoMLAlgorithms: List[AutoMLAlgorithmType]


class AutoMLAlgorithmConfigTypeDef(TypedDict):
    AutoMLAlgorithms: Sequence[AutoMLAlgorithmType]


class AutoMLCandidateStepTypeDef(TypedDict):
    CandidateStepType: CandidateStepTypeType
    CandidateStepArn: str
    CandidateStepName: str


class AutoMLContainerDefinitionTypeDef(TypedDict):
    Image: str
    ModelDataUrl: str
    Environment: NotRequired[Dict[str, str]]


FinalAutoMLJobObjectiveMetricTypeDef = TypedDict(
    "FinalAutoMLJobObjectiveMetricTypeDef",
    {
        "MetricName": AutoMLMetricEnumType,
        "Value": float,
        "Type": NotRequired[AutoMLJobObjectiveTypeType],
        "StandardMetricName": NotRequired[AutoMLMetricEnumType],
    },
)


class EmrServerlessComputeConfigTypeDef(TypedDict):
    ExecutionRoleARN: str


class AutoMLS3DataSourceTypeDef(TypedDict):
    S3DataType: AutoMLS3DataTypeType
    S3Uri: str


class AutoMLDataSplitConfigTypeDef(TypedDict):
    ValidationFraction: NotRequired[float]


class AutoMLJobArtifactsTypeDef(TypedDict):
    CandidateDefinitionNotebookLocation: NotRequired[str]
    DataExplorationNotebookLocation: NotRequired[str]


class AutoMLJobCompletionCriteriaTypeDef(TypedDict):
    MaxCandidates: NotRequired[int]
    MaxRuntimePerTrainingJobInSeconds: NotRequired[int]
    MaxAutoMLJobRuntimeInSeconds: NotRequired[int]


class AutoMLJobObjectiveTypeDef(TypedDict):
    MetricName: AutoMLMetricEnumType


class AutoMLJobStepMetadataTypeDef(TypedDict):
    Arn: NotRequired[str]


class AutoMLPartialFailureReasonTypeDef(TypedDict):
    PartialFailureMessage: NotRequired[str]


class AutoMLOutputDataConfigTypeDef(TypedDict):
    S3OutputPath: str
    KmsKeyId: NotRequired[str]


class TabularResolvedAttributesTypeDef(TypedDict):
    ProblemType: NotRequired[ProblemTypeType]


class TextGenerationResolvedAttributesTypeDef(TypedDict):
    BaseModelName: NotRequired[str]


class VpcConfigOutputTypeDef(TypedDict):
    SecurityGroupIds: List[str]
    Subnets: List[str]


class AutoParameterTypeDef(TypedDict):
    Name: str
    ValueHint: str


class AutotuneTypeDef(TypedDict):
    Mode: Literal["Enabled"]


class BatchDataCaptureConfigTypeDef(TypedDict):
    DestinationS3Uri: str
    KmsKeyId: NotRequired[str]
    GenerateInferenceId: NotRequired[bool]


class BatchDeleteClusterNodesErrorTypeDef(TypedDict):
    Code: BatchDeleteClusterNodesErrorCodeType
    Message: str
    NodeId: str


class BatchDeleteClusterNodesRequestRequestTypeDef(TypedDict):
    ClusterName: str
    NodeIds: Sequence[str]


class BatchDescribeModelPackageErrorTypeDef(TypedDict):
    ErrorCode: str
    ErrorResponse: str


class BatchDescribeModelPackageInputRequestTypeDef(TypedDict):
    ModelPackageArnList: Sequence[str]


class BestObjectiveNotImprovingTypeDef(TypedDict):
    MaxNumberOfTrainingJobsNotImproving: NotRequired[int]


class MetricsSourceTypeDef(TypedDict):
    ContentType: str
    S3Uri: str
    ContentDigest: NotRequired[str]


class CacheHitResultTypeDef(TypedDict):
    SourcePipelineExecutionArn: NotRequired[str]


class OutputParameterTypeDef(TypedDict):
    Name: str
    Value: str


class CandidateArtifactLocationsTypeDef(TypedDict):
    Explainability: str
    ModelInsights: NotRequired[str]
    BacktestResults: NotRequired[str]


MetricDatumTypeDef = TypedDict(
    "MetricDatumTypeDef",
    {
        "MetricName": NotRequired[AutoMLMetricEnumType],
        "Value": NotRequired[float],
        "Set": NotRequired[MetricSetSourceType],
        "StandardMetricName": NotRequired[AutoMLMetricExtendedEnumType],
    },
)


class DirectDeploySettingsTypeDef(TypedDict):
    Status: NotRequired[FeatureStatusType]


class EmrServerlessSettingsTypeDef(TypedDict):
    ExecutionRoleArn: NotRequired[str]
    Status: NotRequired[FeatureStatusType]


class GenerativeAiSettingsTypeDef(TypedDict):
    AmazonBedrockRoleArn: NotRequired[str]


class IdentityProviderOAuthSettingTypeDef(TypedDict):
    DataSourceName: NotRequired[DataSourceNameType]
    Status: NotRequired[FeatureStatusType]
    SecretArn: NotRequired[str]


class KendraSettingsTypeDef(TypedDict):
    Status: NotRequired[FeatureStatusType]


class ModelRegisterSettingsTypeDef(TypedDict):
    Status: NotRequired[FeatureStatusType]
    CrossAccountModelRegisterRoleArn: NotRequired[str]


class TimeSeriesForecastingSettingsTypeDef(TypedDict):
    Status: NotRequired[FeatureStatusType]
    AmazonForecastRoleArn: NotRequired[str]


class WorkspaceSettingsTypeDef(TypedDict):
    S3ArtifactPath: NotRequired[str]
    S3KmsKeyId: NotRequired[str]


CapacitySizeTypeDef = TypedDict(
    "CapacitySizeTypeDef",
    {
        "Type": CapacitySizeTypeType,
        "Value": int,
    },
)


class CaptureContentTypeHeaderOutputTypeDef(TypedDict):
    CsvContentTypes: NotRequired[List[str]]
    JsonContentTypes: NotRequired[List[str]]


class CaptureContentTypeHeaderTypeDef(TypedDict):
    CsvContentTypes: NotRequired[Sequence[str]]
    JsonContentTypes: NotRequired[Sequence[str]]


class CaptureOptionTypeDef(TypedDict):
    CaptureMode: CaptureModeType


class CategoricalParameterOutputTypeDef(TypedDict):
    Name: str
    Value: List[str]


class CategoricalParameterRangeOutputTypeDef(TypedDict):
    Name: str
    Values: List[str]


class CategoricalParameterRangeSpecificationOutputTypeDef(TypedDict):
    Values: List[str]


class CategoricalParameterRangeSpecificationTypeDef(TypedDict):
    Values: Sequence[str]


class CategoricalParameterRangeTypeDef(TypedDict):
    Name: str
    Values: Sequence[str]


class CategoricalParameterTypeDef(TypedDict):
    Name: str
    Value: Sequence[str]


class ShuffleConfigTypeDef(TypedDict):
    Seed: int


class ChannelSpecificationOutputTypeDef(TypedDict):
    Name: str
    SupportedContentTypes: List[str]
    SupportedInputModes: List[TrainingInputModeType]
    Description: NotRequired[str]
    IsRequired: NotRequired[bool]
    SupportedCompressionTypes: NotRequired[List[CompressionTypeType]]


class ChannelSpecificationTypeDef(TypedDict):
    Name: str
    SupportedContentTypes: Sequence[str]
    SupportedInputModes: Sequence[TrainingInputModeType]
    Description: NotRequired[str]
    IsRequired: NotRequired[bool]
    SupportedCompressionTypes: NotRequired[Sequence[CompressionTypeType]]


class CheckpointConfigTypeDef(TypedDict):
    S3Uri: str
    LocalPath: NotRequired[str]


class ClarifyCheckStepMetadataTypeDef(TypedDict):
    CheckType: NotRequired[str]
    BaselineUsedForDriftCheckConstraints: NotRequired[str]
    CalculatedBaselineConstraints: NotRequired[str]
    ModelPackageGroupName: NotRequired[str]
    ViolationReport: NotRequired[str]
    CheckJobArn: NotRequired[str]
    SkipCheck: NotRequired[bool]
    RegisterNewBaseline: NotRequired[bool]


class ClarifyInferenceConfigOutputTypeDef(TypedDict):
    FeaturesAttribute: NotRequired[str]
    ContentTemplate: NotRequired[str]
    MaxRecordCount: NotRequired[int]
    MaxPayloadInMB: NotRequired[int]
    ProbabilityIndex: NotRequired[int]
    LabelIndex: NotRequired[int]
    ProbabilityAttribute: NotRequired[str]
    LabelAttribute: NotRequired[str]
    LabelHeaders: NotRequired[List[str]]
    FeatureHeaders: NotRequired[List[str]]
    FeatureTypes: NotRequired[List[ClarifyFeatureTypeType]]


class ClarifyInferenceConfigTypeDef(TypedDict):
    FeaturesAttribute: NotRequired[str]
    ContentTemplate: NotRequired[str]
    MaxRecordCount: NotRequired[int]
    MaxPayloadInMB: NotRequired[int]
    ProbabilityIndex: NotRequired[int]
    LabelIndex: NotRequired[int]
    ProbabilityAttribute: NotRequired[str]
    LabelAttribute: NotRequired[str]
    LabelHeaders: NotRequired[Sequence[str]]
    FeatureHeaders: NotRequired[Sequence[str]]
    FeatureTypes: NotRequired[Sequence[ClarifyFeatureTypeType]]


class ClarifyShapBaselineConfigTypeDef(TypedDict):
    MimeType: NotRequired[str]
    ShapBaseline: NotRequired[str]
    ShapBaselineUri: NotRequired[str]


class ClarifyTextConfigTypeDef(TypedDict):
    Language: ClarifyTextLanguageType
    Granularity: ClarifyTextGranularityType


class ClusterEbsVolumeConfigTypeDef(TypedDict):
    VolumeSizeInGB: int


class ClusterLifeCycleConfigTypeDef(TypedDict):
    SourceS3Uri: str
    OnCreate: str


class ClusterInstancePlacementTypeDef(TypedDict):
    AvailabilityZone: NotRequired[str]
    AvailabilityZoneId: NotRequired[str]


class ClusterInstanceStatusDetailsTypeDef(TypedDict):
    Status: ClusterInstanceStatusType
    Message: NotRequired[str]


class ClusterOrchestratorEksConfigTypeDef(TypedDict):
    ClusterArn: str


class ClusterSummaryTypeDef(TypedDict):
    ClusterArn: str
    ClusterName: str
    CreationTime: datetime
    ClusterStatus: ClusterStatusType


class ContainerConfigOutputTypeDef(TypedDict):
    ContainerArguments: NotRequired[List[str]]
    ContainerEntrypoint: NotRequired[List[str]]
    ContainerEnvironmentVariables: NotRequired[Dict[str, str]]


class FileSystemConfigTypeDef(TypedDict):
    MountPath: NotRequired[str]
    DefaultUid: NotRequired[int]
    DefaultGid: NotRequired[int]


class CustomImageTypeDef(TypedDict):
    ImageName: str
    AppImageConfigName: str
    ImageVersionNumber: NotRequired[int]


class GitConfigTypeDef(TypedDict):
    RepositoryUrl: str
    Branch: NotRequired[str]
    SecretArn: NotRequired[str]


class CodeRepositoryTypeDef(TypedDict):
    RepositoryUrl: str


class CognitoConfigTypeDef(TypedDict):
    UserPool: str
    ClientId: str


class CognitoMemberDefinitionTypeDef(TypedDict):
    UserPool: str
    UserGroup: str
    ClientId: str


class VectorConfigTypeDef(TypedDict):
    Dimension: int


class CollectionConfigurationOutputTypeDef(TypedDict):
    CollectionName: NotRequired[str]
    CollectionParameters: NotRequired[Dict[str, str]]


class CollectionConfigurationTypeDef(TypedDict):
    CollectionName: NotRequired[str]
    CollectionParameters: NotRequired[Mapping[str, str]]


class CompilationJobSummaryTypeDef(TypedDict):
    CompilationJobName: str
    CompilationJobArn: str
    CreationTime: datetime
    CompilationJobStatus: CompilationJobStatusType
    CompilationStartTime: NotRequired[datetime]
    CompilationEndTime: NotRequired[datetime]
    CompilationTargetDevice: NotRequired[TargetDeviceType]
    CompilationTargetPlatformOs: NotRequired[TargetPlatformOsType]
    CompilationTargetPlatformArch: NotRequired[TargetPlatformArchType]
    CompilationTargetPlatformAccelerator: NotRequired[TargetPlatformAcceleratorType]
    LastModifiedTime: NotRequired[datetime]


class ConditionStepMetadataTypeDef(TypedDict):
    Outcome: NotRequired[ConditionOutcomeType]


class ContainerConfigTypeDef(TypedDict):
    ContainerArguments: NotRequired[Sequence[str]]
    ContainerEntrypoint: NotRequired[Sequence[str]]
    ContainerEnvironmentVariables: NotRequired[Mapping[str, str]]


class MultiModelConfigTypeDef(TypedDict):
    ModelCacheSetting: NotRequired[ModelCacheSettingType]


class ContextSourceTypeDef(TypedDict):
    SourceUri: str
    SourceType: NotRequired[str]
    SourceId: NotRequired[str]


class ContinuousParameterRangeSpecificationTypeDef(TypedDict):
    MinValue: str
    MaxValue: str


class ContinuousParameterRangeTypeDef(TypedDict):
    Name: str
    MinValue: str
    MaxValue: str
    ScalingType: NotRequired[HyperParameterScalingTypeType]


class ConvergenceDetectedTypeDef(TypedDict):
    CompleteOnConvergence: NotRequired[CompleteOnConvergenceType]


class MetadataPropertiesTypeDef(TypedDict):
    CommitId: NotRequired[str]
    Repository: NotRequired[str]
    GeneratedBy: NotRequired[str]
    ProjectId: NotRequired[str]


class ModelDeployConfigTypeDef(TypedDict):
    AutoGenerateEndpointName: NotRequired[bool]
    EndpointName: NotRequired[str]


class VpcConfigTypeDef(TypedDict):
    SecurityGroupIds: Sequence[str]
    Subnets: Sequence[str]


class InputConfigTypeDef(TypedDict):
    S3Uri: str
    Framework: FrameworkType
    DataInputConfig: NotRequired[str]
    FrameworkVersion: NotRequired[str]


class NeoVpcConfigTypeDef(TypedDict):
    SecurityGroupIds: Sequence[str]
    Subnets: Sequence[str]


class StoppingConditionTypeDef(TypedDict):
    MaxRuntimeInSeconds: NotRequired[int]
    MaxWaitTimeInSeconds: NotRequired[int]
    MaxPendingTimeInSeconds: NotRequired[int]


class DataQualityAppSpecificationTypeDef(TypedDict):
    ImageUri: str
    ContainerEntrypoint: NotRequired[Sequence[str]]
    ContainerArguments: NotRequired[Sequence[str]]
    RecordPreprocessorSourceUri: NotRequired[str]
    PostAnalyticsProcessorSourceUri: NotRequired[str]
    Environment: NotRequired[Mapping[str, str]]


class MonitoringStoppingConditionTypeDef(TypedDict):
    MaxRuntimeInSeconds: int


class EdgeOutputConfigTypeDef(TypedDict):
    S3OutputLocation: str
    KmsKeyId: NotRequired[str]
    PresetDeploymentType: NotRequired[Literal["GreengrassV2Component"]]
    PresetDeploymentConfig: NotRequired[str]


class EdgeDeploymentModelConfigTypeDef(TypedDict):
    ModelHandle: str
    EdgePackagingJobName: str


class ThroughputConfigTypeDef(TypedDict):
    ThroughputMode: ThroughputModeType
    ProvisionedReadCapacityUnits: NotRequired[int]
    ProvisionedWriteCapacityUnits: NotRequired[int]


class FlowDefinitionOutputConfigTypeDef(TypedDict):
    S3OutputPath: str
    KmsKeyId: NotRequired[str]


class HumanLoopRequestSourceTypeDef(TypedDict):
    AwsManagedHumanLoopRequestSource: AwsManagedHumanLoopRequestSourceType


class HubS3StorageConfigTypeDef(TypedDict):
    S3OutputPath: NotRequired[str]


class UiTemplateTypeDef(TypedDict):
    Content: str


class CreateImageVersionRequestRequestTypeDef(TypedDict):
    BaseImage: str
    ClientToken: str
    ImageName: str
    Aliases: NotRequired[Sequence[str]]
    VendorGuidance: NotRequired[VendorGuidanceType]
    JobType: NotRequired[JobTypeType]
    MLFramework: NotRequired[str]
    ProgrammingLang: NotRequired[str]
    Processor: NotRequired[ProcessorType]
    Horovod: NotRequired[bool]
    ReleaseNotes: NotRequired[str]


class InferenceComponentRuntimeConfigTypeDef(TypedDict):
    CopyCount: int


class LabelingJobOutputConfigTypeDef(TypedDict):
    S3OutputPath: str
    KmsKeyId: NotRequired[str]
    SnsTopicArn: NotRequired[str]


class LabelingJobStoppingConditionsTypeDef(TypedDict):
    MaxHumanLabeledObjectCount: NotRequired[int]
    MaxPercentageOfInputDatasetLabeled: NotRequired[int]


class ModelBiasAppSpecificationTypeDef(TypedDict):
    ImageUri: str
    ConfigUri: str
    Environment: NotRequired[Mapping[str, str]]


class ModelCardExportOutputConfigTypeDef(TypedDict):
    S3OutputPath: str


class ModelCardSecurityConfigTypeDef(TypedDict):
    KmsKeyId: NotRequired[str]


class ModelExplainabilityAppSpecificationTypeDef(TypedDict):
    ImageUri: str
    ConfigUri: str
    Environment: NotRequired[Mapping[str, str]]


class InferenceExecutionConfigTypeDef(TypedDict):
    Mode: InferenceExecutionModeType


class ModelLifeCycleTypeDef(TypedDict):
    Stage: str
    StageStatus: str
    StageDescription: NotRequired[str]


class ModelPackageModelCardTypeDef(TypedDict):
    ModelCardContent: NotRequired[str]
    ModelCardStatus: NotRequired[ModelCardStatusType]


class ModelPackageSecurityConfigTypeDef(TypedDict):
    KmsKeyId: str


class ModelQualityAppSpecificationTypeDef(TypedDict):
    ImageUri: str
    ContainerEntrypoint: NotRequired[Sequence[str]]
    ContainerArguments: NotRequired[Sequence[str]]
    RecordPreprocessorSourceUri: NotRequired[str]
    PostAnalyticsProcessorSourceUri: NotRequired[str]
    ProblemType: NotRequired[MonitoringProblemTypeType]
    Environment: NotRequired[Mapping[str, str]]


class InstanceMetadataServiceConfigurationTypeDef(TypedDict):
    MinimumInstanceMetadataServiceVersion: str


class NotebookInstanceLifecycleHookTypeDef(TypedDict):
    Content: NotRequired[str]


class OptimizationJobOutputConfigTypeDef(TypedDict):
    S3OutputLocation: str
    KmsKeyId: NotRequired[str]


class OptimizationVpcConfigTypeDef(TypedDict):
    SecurityGroupIds: Sequence[str]
    Subnets: Sequence[str]


class ParallelismConfigurationTypeDef(TypedDict):
    MaxParallelExecutionSteps: int


class PipelineDefinitionS3LocationTypeDef(TypedDict):
    Bucket: str
    ObjectKey: str
    VersionId: NotRequired[str]


class CreatePresignedDomainUrlRequestRequestTypeDef(TypedDict):
    DomainId: str
    UserProfileName: str
    SessionExpirationDurationInSeconds: NotRequired[int]
    ExpiresInSeconds: NotRequired[int]
    SpaceName: NotRequired[str]
    LandingUri: NotRequired[str]


class CreatePresignedMlflowTrackingServerUrlRequestRequestTypeDef(TypedDict):
    TrackingServerName: str
    ExpiresInSeconds: NotRequired[int]
    SessionExpirationDurationInSeconds: NotRequired[int]


class CreatePresignedNotebookInstanceUrlInputRequestTypeDef(TypedDict):
    NotebookInstanceName: str
    SessionExpirationDurationInSeconds: NotRequired[int]


class ExperimentConfigTypeDef(TypedDict):
    ExperimentName: NotRequired[str]
    TrialName: NotRequired[str]
    TrialComponentDisplayName: NotRequired[str]
    RunName: NotRequired[str]


class ProcessingStoppingConditionTypeDef(TypedDict):
    MaxRuntimeInSeconds: int


class OwnershipSettingsTypeDef(TypedDict):
    OwnerUserProfileName: str


class SpaceSharingSettingsTypeDef(TypedDict):
    SharingType: SharingTypeType


class InfraCheckConfigTypeDef(TypedDict):
    EnableInfraCheck: NotRequired[bool]


class OutputDataConfigTypeDef(TypedDict):
    S3OutputPath: str
    KmsKeyId: NotRequired[str]
    CompressionType: NotRequired[OutputCompressionTypeType]


class ProfilerConfigTypeDef(TypedDict):
    S3OutputPath: NotRequired[str]
    ProfilingIntervalInMilliseconds: NotRequired[int]
    ProfilingParameters: NotRequired[Mapping[str, str]]
    DisableProfiler: NotRequired[bool]


class RemoteDebugConfigTypeDef(TypedDict):
    EnableRemoteDebug: NotRequired[bool]


class RetryStrategyTypeDef(TypedDict):
    MaximumRetryAttempts: int


class SessionChainingConfigTypeDef(TypedDict):
    EnableSessionTagChaining: NotRequired[bool]


class TensorBoardOutputConfigTypeDef(TypedDict):
    S3OutputPath: str
    LocalPath: NotRequired[str]


class DataProcessingTypeDef(TypedDict):
    InputFilter: NotRequired[str]
    OutputFilter: NotRequired[str]
    JoinSource: NotRequired[JoinSourceType]


class ModelClientConfigTypeDef(TypedDict):
    InvocationsTimeoutInSeconds: NotRequired[int]
    InvocationsMaxRetries: NotRequired[int]


class TransformOutputTypeDef(TypedDict):
    S3OutputPath: str
    Accept: NotRequired[str]
    AssembleWith: NotRequired[AssemblyTypeType]
    KmsKeyId: NotRequired[str]


class TransformResourcesTypeDef(TypedDict):
    InstanceType: TransformInstanceTypeType
    InstanceCount: int
    VolumeKmsKeyId: NotRequired[str]


TimestampTypeDef = Union[datetime, str]


class TrialComponentArtifactTypeDef(TypedDict):
    Value: str
    MediaType: NotRequired[str]


class TrialComponentParameterValueTypeDef(TypedDict):
    StringValue: NotRequired[str]
    NumberValue: NotRequired[float]


class TrialComponentStatusTypeDef(TypedDict):
    PrimaryStatus: NotRequired[TrialComponentPrimaryStatusType]
    Message: NotRequired[str]


class OidcConfigTypeDef(TypedDict):
    ClientId: str
    ClientSecret: str
    Issuer: str
    AuthorizationEndpoint: str
    TokenEndpoint: str
    UserInfoEndpoint: str
    LogoutEndpoint: str
    JwksUri: str
    Scope: NotRequired[str]
    AuthenticationRequestExtraParams: NotRequired[Mapping[str, str]]


class SourceIpConfigTypeDef(TypedDict):
    Cidrs: Sequence[str]


class WorkforceVpcConfigRequestTypeDef(TypedDict):
    VpcId: NotRequired[str]
    SecurityGroupIds: NotRequired[Sequence[str]]
    Subnets: NotRequired[Sequence[str]]


class NotificationConfigurationTypeDef(TypedDict):
    NotificationTopicArn: NotRequired[str]


class EFSFileSystemConfigTypeDef(TypedDict):
    FileSystemId: str
    FileSystemPath: NotRequired[str]


class EFSFileSystemTypeDef(TypedDict):
    FileSystemId: str


class CustomPosixUserConfigTypeDef(TypedDict):
    Uid: int
    Gid: int


class CustomizedMetricSpecificationTypeDef(TypedDict):
    MetricName: NotRequired[str]
    Namespace: NotRequired[str]
    Statistic: NotRequired[StatisticType]


class DataCaptureConfigSummaryTypeDef(TypedDict):
    EnableCapture: bool
    CaptureStatus: CaptureStatusType
    CurrentSamplingPercentage: int
    DestinationS3Uri: str
    KmsKeyId: str


class DataCatalogConfigTypeDef(TypedDict):
    TableName: str
    Catalog: str
    Database: str


class DataQualityAppSpecificationOutputTypeDef(TypedDict):
    ImageUri: str
    ContainerEntrypoint: NotRequired[List[str]]
    ContainerArguments: NotRequired[List[str]]
    RecordPreprocessorSourceUri: NotRequired[str]
    PostAnalyticsProcessorSourceUri: NotRequired[str]
    Environment: NotRequired[Dict[str, str]]


class MonitoringConstraintsResourceTypeDef(TypedDict):
    S3Uri: NotRequired[str]


class MonitoringStatisticsResourceTypeDef(TypedDict):
    S3Uri: NotRequired[str]


EndpointInputTypeDef = TypedDict(
    "EndpointInputTypeDef",
    {
        "EndpointName": str,
        "LocalPath": str,
        "S3InputMode": NotRequired[ProcessingS3InputModeType],
        "S3DataDistributionType": NotRequired[ProcessingS3DataDistributionTypeType],
        "FeaturesAttribute": NotRequired[str],
        "InferenceAttribute": NotRequired[str],
        "ProbabilityAttribute": NotRequired[str],
        "ProbabilityThresholdAttribute": NotRequired[float],
        "StartTimeOffset": NotRequired[str],
        "EndTimeOffset": NotRequired[str],
        "ExcludeFeaturesAttribute": NotRequired[str],
    },
)


class FileSystemDataSourceTypeDef(TypedDict):
    FileSystemId: str
    FileSystemAccessMode: FileSystemAccessModeType
    FileSystemType: FileSystemTypeType
    DirectoryPath: str


S3DataSourceOutputTypeDef = TypedDict(
    "S3DataSourceOutputTypeDef",
    {
        "S3DataType": S3DataTypeType,
        "S3Uri": str,
        "S3DataDistributionType": NotRequired[S3DataDistributionType],
        "AttributeNames": NotRequired[List[str]],
        "InstanceGroupNames": NotRequired[List[str]],
    },
)


class RedshiftDatasetDefinitionTypeDef(TypedDict):
    ClusterId: str
    Database: str
    DbUser: str
    QueryString: str
    ClusterRoleArn: str
    OutputS3Uri: str
    OutputFormat: RedshiftResultFormatType
    KmsKeyId: NotRequired[str]
    OutputCompression: NotRequired[RedshiftResultCompressionTypeType]


class DebugRuleConfigurationOutputTypeDef(TypedDict):
    RuleConfigurationName: str
    RuleEvaluatorImage: str
    LocalPath: NotRequired[str]
    S3OutputPath: NotRequired[str]
    InstanceType: NotRequired[ProcessingInstanceTypeType]
    VolumeSizeInGB: NotRequired[int]
    RuleParameters: NotRequired[Dict[str, str]]


class DebugRuleConfigurationTypeDef(TypedDict):
    RuleConfigurationName: str
    RuleEvaluatorImage: str
    LocalPath: NotRequired[str]
    S3OutputPath: NotRequired[str]
    InstanceType: NotRequired[ProcessingInstanceTypeType]
    VolumeSizeInGB: NotRequired[int]
    RuleParameters: NotRequired[Mapping[str, str]]


class DebugRuleEvaluationStatusTypeDef(TypedDict):
    RuleConfigurationName: NotRequired[str]
    RuleEvaluationJobArn: NotRequired[str]
    RuleEvaluationStatus: NotRequired[RuleEvaluationStatusType]
    StatusDetails: NotRequired[str]
    LastModifiedTime: NotRequired[datetime]


class DefaultEbsStorageSettingsTypeDef(TypedDict):
    DefaultEbsVolumeSizeInGb: int
    MaximumEbsVolumeSizeInGb: int


class DeleteActionRequestRequestTypeDef(TypedDict):
    ActionName: str


class DeleteAlgorithmInputRequestTypeDef(TypedDict):
    AlgorithmName: str


class DeleteAppImageConfigRequestRequestTypeDef(TypedDict):
    AppImageConfigName: str


class DeleteAppRequestRequestTypeDef(TypedDict):
    DomainId: str
    AppType: AppTypeType
    AppName: str
    UserProfileName: NotRequired[str]
    SpaceName: NotRequired[str]


class DeleteAssociationRequestRequestTypeDef(TypedDict):
    SourceArn: str
    DestinationArn: str


class DeleteClusterRequestRequestTypeDef(TypedDict):
    ClusterName: str


class DeleteCodeRepositoryInputRequestTypeDef(TypedDict):
    CodeRepositoryName: str


class DeleteCompilationJobRequestRequestTypeDef(TypedDict):
    CompilationJobName: str


class DeleteContextRequestRequestTypeDef(TypedDict):
    ContextName: str


class DeleteDataQualityJobDefinitionRequestRequestTypeDef(TypedDict):
    JobDefinitionName: str


class DeleteDeviceFleetRequestRequestTypeDef(TypedDict):
    DeviceFleetName: str


class RetentionPolicyTypeDef(TypedDict):
    HomeEfsFileSystem: NotRequired[RetentionTypeType]


class DeleteEdgeDeploymentPlanRequestRequestTypeDef(TypedDict):
    EdgeDeploymentPlanName: str


class DeleteEdgeDeploymentStageRequestRequestTypeDef(TypedDict):
    EdgeDeploymentPlanName: str
    StageName: str


class DeleteEndpointConfigInputRequestTypeDef(TypedDict):
    EndpointConfigName: str


class DeleteEndpointInputRequestTypeDef(TypedDict):
    EndpointName: str


class DeleteExperimentRequestRequestTypeDef(TypedDict):
    ExperimentName: str


class DeleteFeatureGroupRequestRequestTypeDef(TypedDict):
    FeatureGroupName: str


class DeleteFlowDefinitionRequestRequestTypeDef(TypedDict):
    FlowDefinitionName: str


class DeleteHubContentReferenceRequestRequestTypeDef(TypedDict):
    HubName: str
    HubContentType: HubContentTypeType
    HubContentName: str


class DeleteHubContentRequestRequestTypeDef(TypedDict):
    HubName: str
    HubContentType: HubContentTypeType
    HubContentName: str
    HubContentVersion: str


class DeleteHubRequestRequestTypeDef(TypedDict):
    HubName: str


class DeleteHumanTaskUiRequestRequestTypeDef(TypedDict):
    HumanTaskUiName: str


class DeleteHyperParameterTuningJobRequestRequestTypeDef(TypedDict):
    HyperParameterTuningJobName: str


class DeleteImageRequestRequestTypeDef(TypedDict):
    ImageName: str


class DeleteImageVersionRequestRequestTypeDef(TypedDict):
    ImageName: str
    Version: NotRequired[int]
    Alias: NotRequired[str]


class DeleteInferenceComponentInputRequestTypeDef(TypedDict):
    InferenceComponentName: str


class DeleteInferenceExperimentRequestRequestTypeDef(TypedDict):
    Name: str


class DeleteMlflowTrackingServerRequestRequestTypeDef(TypedDict):
    TrackingServerName: str


class DeleteModelBiasJobDefinitionRequestRequestTypeDef(TypedDict):
    JobDefinitionName: str


class DeleteModelCardRequestRequestTypeDef(TypedDict):
    ModelCardName: str


class DeleteModelExplainabilityJobDefinitionRequestRequestTypeDef(TypedDict):
    JobDefinitionName: str


class DeleteModelInputRequestTypeDef(TypedDict):
    ModelName: str


class DeleteModelPackageGroupInputRequestTypeDef(TypedDict):
    ModelPackageGroupName: str


class DeleteModelPackageGroupPolicyInputRequestTypeDef(TypedDict):
    ModelPackageGroupName: str


class DeleteModelPackageInputRequestTypeDef(TypedDict):
    ModelPackageName: str


class DeleteModelQualityJobDefinitionRequestRequestTypeDef(TypedDict):
    JobDefinitionName: str


class DeleteMonitoringScheduleRequestRequestTypeDef(TypedDict):
    MonitoringScheduleName: str


class DeleteNotebookInstanceInputRequestTypeDef(TypedDict):
    NotebookInstanceName: str


class DeleteNotebookInstanceLifecycleConfigInputRequestTypeDef(TypedDict):
    NotebookInstanceLifecycleConfigName: str


class DeleteOptimizationJobRequestRequestTypeDef(TypedDict):
    OptimizationJobName: str


class DeletePipelineRequestRequestTypeDef(TypedDict):
    PipelineName: str
    ClientRequestToken: str


class DeleteProjectInputRequestTypeDef(TypedDict):
    ProjectName: str


class DeleteSpaceRequestRequestTypeDef(TypedDict):
    DomainId: str
    SpaceName: str


class DeleteStudioLifecycleConfigRequestRequestTypeDef(TypedDict):
    StudioLifecycleConfigName: str


class DeleteTagsInputRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]


class DeleteTrialComponentRequestRequestTypeDef(TypedDict):
    TrialComponentName: str


class DeleteTrialRequestRequestTypeDef(TypedDict):
    TrialName: str


class DeleteUserProfileRequestRequestTypeDef(TypedDict):
    DomainId: str
    UserProfileName: str


class DeleteWorkforceRequestRequestTypeDef(TypedDict):
    WorkforceName: str


class DeleteWorkteamRequestRequestTypeDef(TypedDict):
    WorkteamName: str


class DeployedImageTypeDef(TypedDict):
    SpecifiedImage: NotRequired[str]
    ResolvedImage: NotRequired[str]
    ResolutionTime: NotRequired[datetime]


class RealTimeInferenceRecommendationTypeDef(TypedDict):
    RecommendationId: str
    InstanceType: ProductionVariantInstanceTypeType
    Environment: NotRequired[Dict[str, str]]


class DeviceSelectionConfigOutputTypeDef(TypedDict):
    DeviceSubsetType: DeviceSubsetTypeType
    Percentage: NotRequired[int]
    DeviceNames: NotRequired[List[str]]
    DeviceNameContains: NotRequired[str]


class EdgeDeploymentConfigTypeDef(TypedDict):
    FailureHandlingPolicy: FailureHandlingPolicyType


class EdgeDeploymentStatusTypeDef(TypedDict):
    StageStatus: StageStatusType
    EdgeDeploymentSuccessInStage: int
    EdgeDeploymentPendingInStage: int
    EdgeDeploymentFailedInStage: int
    EdgeDeploymentStatusMessage: NotRequired[str]
    EdgeDeploymentStageStartTime: NotRequired[datetime]


class DeregisterDevicesRequestRequestTypeDef(TypedDict):
    DeviceFleetName: str
    DeviceNames: Sequence[str]


class DerivedInformationTypeDef(TypedDict):
    DerivedDataInputConfig: NotRequired[str]


class DescribeActionRequestRequestTypeDef(TypedDict):
    ActionName: str


class DescribeAlgorithmInputRequestTypeDef(TypedDict):
    AlgorithmName: str


class DescribeAppImageConfigRequestRequestTypeDef(TypedDict):
    AppImageConfigName: str


class DescribeAppRequestRequestTypeDef(TypedDict):
    DomainId: str
    AppType: AppTypeType
    AppName: str
    UserProfileName: NotRequired[str]
    SpaceName: NotRequired[str]


class DescribeArtifactRequestRequestTypeDef(TypedDict):
    ArtifactArn: str


class DescribeAutoMLJobRequestRequestTypeDef(TypedDict):
    AutoMLJobName: str


class ModelDeployResultTypeDef(TypedDict):
    EndpointName: NotRequired[str]


class DescribeAutoMLJobV2RequestRequestTypeDef(TypedDict):
    AutoMLJobName: str


class DescribeClusterNodeRequestRequestTypeDef(TypedDict):
    ClusterName: str
    NodeId: str


class DescribeClusterRequestRequestTypeDef(TypedDict):
    ClusterName: str


class DescribeCodeRepositoryInputRequestTypeDef(TypedDict):
    CodeRepositoryName: str


class DescribeCompilationJobRequestRequestTypeDef(TypedDict):
    CompilationJobName: str


class ModelArtifactsTypeDef(TypedDict):
    S3ModelArtifacts: str


class ModelDigestsTypeDef(TypedDict):
    ArtifactDigest: NotRequired[str]


class NeoVpcConfigOutputTypeDef(TypedDict):
    SecurityGroupIds: List[str]
    Subnets: List[str]


class DescribeContextRequestRequestTypeDef(TypedDict):
    ContextName: str


class DescribeDataQualityJobDefinitionRequestRequestTypeDef(TypedDict):
    JobDefinitionName: str


class DescribeDeviceFleetRequestRequestTypeDef(TypedDict):
    DeviceFleetName: str


class DescribeDeviceRequestRequestTypeDef(TypedDict):
    DeviceName: str
    DeviceFleetName: str
    NextToken: NotRequired[str]


class EdgeModelTypeDef(TypedDict):
    ModelName: str
    ModelVersion: str
    LatestSampleTime: NotRequired[datetime]
    LatestInference: NotRequired[datetime]


class DescribeDomainRequestRequestTypeDef(TypedDict):
    DomainId: str


class DescribeEdgeDeploymentPlanRequestRequestTypeDef(TypedDict):
    EdgeDeploymentPlanName: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class DescribeEdgePackagingJobRequestRequestTypeDef(TypedDict):
    EdgePackagingJobName: str


EdgePresetDeploymentOutputTypeDef = TypedDict(
    "EdgePresetDeploymentOutputTypeDef",
    {
        "Type": Literal["GreengrassV2Component"],
        "Artifact": NotRequired[str],
        "Status": NotRequired[EdgePresetDeploymentStatusType],
        "StatusMessage": NotRequired[str],
    },
)


class DescribeEndpointConfigInputRequestTypeDef(TypedDict):
    EndpointConfigName: str


class WaiterConfigTypeDef(TypedDict):
    Delay: NotRequired[int]
    MaxAttempts: NotRequired[int]


class DescribeEndpointInputRequestTypeDef(TypedDict):
    EndpointName: str


class DescribeExperimentRequestRequestTypeDef(TypedDict):
    ExperimentName: str


class ExperimentSourceTypeDef(TypedDict):
    SourceArn: str
    SourceType: NotRequired[str]


class DescribeFeatureGroupRequestRequestTypeDef(TypedDict):
    FeatureGroupName: str
    NextToken: NotRequired[str]


class LastUpdateStatusTypeDef(TypedDict):
    Status: LastUpdateStatusValueType
    FailureReason: NotRequired[str]


class OfflineStoreStatusTypeDef(TypedDict):
    Status: OfflineStoreStatusValueType
    BlockedReason: NotRequired[str]


class ThroughputConfigDescriptionTypeDef(TypedDict):
    ThroughputMode: ThroughputModeType
    ProvisionedReadCapacityUnits: NotRequired[int]
    ProvisionedWriteCapacityUnits: NotRequired[int]


class DescribeFeatureMetadataRequestRequestTypeDef(TypedDict):
    FeatureGroupName: str
    FeatureName: str


class FeatureParameterTypeDef(TypedDict):
    Key: NotRequired[str]
    Value: NotRequired[str]


class DescribeFlowDefinitionRequestRequestTypeDef(TypedDict):
    FlowDefinitionName: str


class DescribeHubContentRequestRequestTypeDef(TypedDict):
    HubName: str
    HubContentType: HubContentTypeType
    HubContentName: str
    HubContentVersion: NotRequired[str]


class HubContentDependencyTypeDef(TypedDict):
    DependencyOriginPath: NotRequired[str]
    DependencyCopyPath: NotRequired[str]


class DescribeHubRequestRequestTypeDef(TypedDict):
    HubName: str


class DescribeHumanTaskUiRequestRequestTypeDef(TypedDict):
    HumanTaskUiName: str


class UiTemplateInfoTypeDef(TypedDict):
    Url: NotRequired[str]
    ContentSha256: NotRequired[str]


class DescribeHyperParameterTuningJobRequestRequestTypeDef(TypedDict):
    HyperParameterTuningJobName: str


class HyperParameterTuningJobCompletionDetailsTypeDef(TypedDict):
    NumberOfTrainingJobsObjectiveNotImproving: NotRequired[int]
    ConvergenceDetectedTime: NotRequired[datetime]


class HyperParameterTuningJobConsumedResourcesTypeDef(TypedDict):
    RuntimeInSeconds: NotRequired[int]


class ObjectiveStatusCountersTypeDef(TypedDict):
    Succeeded: NotRequired[int]
    Pending: NotRequired[int]
    Failed: NotRequired[int]


class TrainingJobStatusCountersTypeDef(TypedDict):
    Completed: NotRequired[int]
    InProgress: NotRequired[int]
    RetryableError: NotRequired[int]
    NonRetryableError: NotRequired[int]
    Stopped: NotRequired[int]


class DescribeImageRequestRequestTypeDef(TypedDict):
    ImageName: str


class DescribeImageVersionRequestRequestTypeDef(TypedDict):
    ImageName: str
    Version: NotRequired[int]
    Alias: NotRequired[str]


class DescribeInferenceComponentInputRequestTypeDef(TypedDict):
    InferenceComponentName: str


class InferenceComponentRuntimeConfigSummaryTypeDef(TypedDict):
    DesiredCopyCount: NotRequired[int]
    CurrentCopyCount: NotRequired[int]


class DescribeInferenceExperimentRequestRequestTypeDef(TypedDict):
    Name: str


class EndpointMetadataTypeDef(TypedDict):
    EndpointName: str
    EndpointConfigName: NotRequired[str]
    EndpointStatus: NotRequired[EndpointStatusType]
    FailureReason: NotRequired[str]


class InferenceExperimentScheduleOutputTypeDef(TypedDict):
    StartTime: NotRequired[datetime]
    EndTime: NotRequired[datetime]


class DescribeInferenceRecommendationsJobRequestRequestTypeDef(TypedDict):
    JobName: str


class DescribeLabelingJobRequestRequestTypeDef(TypedDict):
    LabelingJobName: str


class LabelCountersTypeDef(TypedDict):
    TotalLabeled: NotRequired[int]
    HumanLabeled: NotRequired[int]
    MachineLabeled: NotRequired[int]
    FailedNonRetryableError: NotRequired[int]
    Unlabeled: NotRequired[int]


class LabelingJobOutputTypeDef(TypedDict):
    OutputDatasetS3Uri: str
    FinalActiveLearningModelArn: NotRequired[str]


class DescribeLineageGroupRequestRequestTypeDef(TypedDict):
    LineageGroupName: str


class DescribeMlflowTrackingServerRequestRequestTypeDef(TypedDict):
    TrackingServerName: str


class DescribeModelBiasJobDefinitionRequestRequestTypeDef(TypedDict):
    JobDefinitionName: str


class ModelBiasAppSpecificationOutputTypeDef(TypedDict):
    ImageUri: str
    ConfigUri: str
    Environment: NotRequired[Dict[str, str]]


class DescribeModelCardExportJobRequestRequestTypeDef(TypedDict):
    ModelCardExportJobArn: str


class ModelCardExportArtifactsTypeDef(TypedDict):
    S3ExportArtifacts: str


class DescribeModelCardRequestRequestTypeDef(TypedDict):
    ModelCardName: str
    ModelCardVersion: NotRequired[int]


class DescribeModelExplainabilityJobDefinitionRequestRequestTypeDef(TypedDict):
    JobDefinitionName: str


class ModelExplainabilityAppSpecificationOutputTypeDef(TypedDict):
    ImageUri: str
    ConfigUri: str
    Environment: NotRequired[Dict[str, str]]


class DescribeModelInputRequestTypeDef(TypedDict):
    ModelName: str


class DescribeModelPackageGroupInputRequestTypeDef(TypedDict):
    ModelPackageGroupName: str


class DescribeModelPackageInputRequestTypeDef(TypedDict):
    ModelPackageName: str


class DescribeModelQualityJobDefinitionRequestRequestTypeDef(TypedDict):
    JobDefinitionName: str


class ModelQualityAppSpecificationOutputTypeDef(TypedDict):
    ImageUri: str
    ContainerEntrypoint: NotRequired[List[str]]
    ContainerArguments: NotRequired[List[str]]
    RecordPreprocessorSourceUri: NotRequired[str]
    PostAnalyticsProcessorSourceUri: NotRequired[str]
    ProblemType: NotRequired[MonitoringProblemTypeType]
    Environment: NotRequired[Dict[str, str]]


class DescribeMonitoringScheduleRequestRequestTypeDef(TypedDict):
    MonitoringScheduleName: str


class MonitoringExecutionSummaryTypeDef(TypedDict):
    MonitoringScheduleName: str
    ScheduledTime: datetime
    CreationTime: datetime
    LastModifiedTime: datetime
    MonitoringExecutionStatus: ExecutionStatusType
    ProcessingJobArn: NotRequired[str]
    EndpointName: NotRequired[str]
    FailureReason: NotRequired[str]
    MonitoringJobDefinitionName: NotRequired[str]
    MonitoringType: NotRequired[MonitoringTypeType]


class DescribeNotebookInstanceInputRequestTypeDef(TypedDict):
    NotebookInstanceName: str


class DescribeNotebookInstanceLifecycleConfigInputRequestTypeDef(TypedDict):
    NotebookInstanceLifecycleConfigName: str


class DescribeOptimizationJobRequestRequestTypeDef(TypedDict):
    OptimizationJobName: str


class OptimizationOutputTypeDef(TypedDict):
    RecommendedInferenceImage: NotRequired[str]


class OptimizationVpcConfigOutputTypeDef(TypedDict):
    SecurityGroupIds: List[str]
    Subnets: List[str]


class DescribePipelineDefinitionForExecutionRequestRequestTypeDef(TypedDict):
    PipelineExecutionArn: str


class DescribePipelineExecutionRequestRequestTypeDef(TypedDict):
    PipelineExecutionArn: str


class PipelineExperimentConfigTypeDef(TypedDict):
    ExperimentName: NotRequired[str]
    TrialName: NotRequired[str]


class DescribePipelineRequestRequestTypeDef(TypedDict):
    PipelineName: str


class DescribeProcessingJobRequestRequestTypeDef(TypedDict):
    ProcessingJobName: str


class DescribeProjectInputRequestTypeDef(TypedDict):
    ProjectName: str


class ServiceCatalogProvisionedProductDetailsTypeDef(TypedDict):
    ProvisionedProductId: NotRequired[str]
    ProvisionedProductStatusMessage: NotRequired[str]


class DescribeSpaceRequestRequestTypeDef(TypedDict):
    DomainId: str
    SpaceName: str


class DescribeStudioLifecycleConfigRequestRequestTypeDef(TypedDict):
    StudioLifecycleConfigName: str


class DescribeSubscribedWorkteamRequestRequestTypeDef(TypedDict):
    WorkteamArn: str


class SubscribedWorkteamTypeDef(TypedDict):
    WorkteamArn: str
    MarketplaceTitle: NotRequired[str]
    SellerName: NotRequired[str]
    MarketplaceDescription: NotRequired[str]
    ListingId: NotRequired[str]


class DescribeTrainingJobRequestRequestTypeDef(TypedDict):
    TrainingJobName: str


class MetricDataTypeDef(TypedDict):
    MetricName: NotRequired[str]
    Value: NotRequired[float]
    Timestamp: NotRequired[datetime]


class ProfilerConfigOutputTypeDef(TypedDict):
    S3OutputPath: NotRequired[str]
    ProfilingIntervalInMilliseconds: NotRequired[int]
    ProfilingParameters: NotRequired[Dict[str, str]]
    DisableProfiler: NotRequired[bool]


class ProfilerRuleConfigurationOutputTypeDef(TypedDict):
    RuleConfigurationName: str
    RuleEvaluatorImage: str
    LocalPath: NotRequired[str]
    S3OutputPath: NotRequired[str]
    InstanceType: NotRequired[ProcessingInstanceTypeType]
    VolumeSizeInGB: NotRequired[int]
    RuleParameters: NotRequired[Dict[str, str]]


class ProfilerRuleEvaluationStatusTypeDef(TypedDict):
    RuleConfigurationName: NotRequired[str]
    RuleEvaluationJobArn: NotRequired[str]
    RuleEvaluationStatus: NotRequired[RuleEvaluationStatusType]
    StatusDetails: NotRequired[str]
    LastModifiedTime: NotRequired[datetime]


class SecondaryStatusTransitionTypeDef(TypedDict):
    Status: SecondaryStatusType
    StartTime: datetime
    EndTime: NotRequired[datetime]
    StatusMessage: NotRequired[str]


class WarmPoolStatusTypeDef(TypedDict):
    Status: WarmPoolResourceStatusType
    ResourceRetainedBillableTimeInSeconds: NotRequired[int]
    ReusedByJob: NotRequired[str]


class DescribeTransformJobRequestRequestTypeDef(TypedDict):
    TransformJobName: str


class DescribeTrialComponentRequestRequestTypeDef(TypedDict):
    TrialComponentName: str


class TrialComponentMetricSummaryTypeDef(TypedDict):
    MetricName: NotRequired[str]
    SourceArn: NotRequired[str]
    TimeStamp: NotRequired[datetime]
    Max: NotRequired[float]
    Min: NotRequired[float]
    Last: NotRequired[float]
    Count: NotRequired[int]
    Avg: NotRequired[float]
    StdDev: NotRequired[float]


class TrialComponentSourceTypeDef(TypedDict):
    SourceArn: str
    SourceType: NotRequired[str]


class DescribeTrialRequestRequestTypeDef(TypedDict):
    TrialName: str


class TrialSourceTypeDef(TypedDict):
    SourceArn: str
    SourceType: NotRequired[str]


class DescribeUserProfileRequestRequestTypeDef(TypedDict):
    DomainId: str
    UserProfileName: str


class DescribeWorkforceRequestRequestTypeDef(TypedDict):
    WorkforceName: str


class DescribeWorkteamRequestRequestTypeDef(TypedDict):
    WorkteamName: str


class ProductionVariantServerlessUpdateConfigTypeDef(TypedDict):
    MaxConcurrency: NotRequired[int]
    ProvisionedConcurrency: NotRequired[int]


class DeviceDeploymentSummaryTypeDef(TypedDict):
    EdgeDeploymentPlanArn: str
    EdgeDeploymentPlanName: str
    StageName: str
    DeviceName: str
    DeviceArn: str
    DeployedStageName: NotRequired[str]
    DeviceFleetName: NotRequired[str]
    DeviceDeploymentStatus: NotRequired[DeviceDeploymentStatusType]
    DeviceDeploymentStatusMessage: NotRequired[str]
    Description: NotRequired[str]
    DeploymentStartTime: NotRequired[datetime]


class DeviceFleetSummaryTypeDef(TypedDict):
    DeviceFleetArn: str
    DeviceFleetName: str
    CreationTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]


class DeviceSelectionConfigTypeDef(TypedDict):
    DeviceSubsetType: DeviceSubsetTypeType
    Percentage: NotRequired[int]
    DeviceNames: NotRequired[Sequence[str]]
    DeviceNameContains: NotRequired[str]


class DeviceStatsTypeDef(TypedDict):
    ConnectedDeviceCount: int
    RegisteredDeviceCount: int


class EdgeModelSummaryTypeDef(TypedDict):
    ModelName: str
    ModelVersion: str


class DeviceTypeDef(TypedDict):
    DeviceName: str
    Description: NotRequired[str]
    IotThingName: NotRequired[str]


class DisassociateTrialComponentRequestRequestTypeDef(TypedDict):
    TrialComponentName: str
    TrialName: str


class DockerSettingsOutputTypeDef(TypedDict):
    EnableDockerAccess: NotRequired[FeatureStatusType]
    VpcOnlyTrustedAccounts: NotRequired[List[str]]


class DockerSettingsTypeDef(TypedDict):
    EnableDockerAccess: NotRequired[FeatureStatusType]
    VpcOnlyTrustedAccounts: NotRequired[Sequence[str]]


class DomainDetailsTypeDef(TypedDict):
    DomainArn: NotRequired[str]
    DomainId: NotRequired[str]
    DomainName: NotRequired[str]
    Status: NotRequired[DomainStatusType]
    CreationTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]
    Url: NotRequired[str]


class FileSourceTypeDef(TypedDict):
    S3Uri: str
    ContentType: NotRequired[str]
    ContentDigest: NotRequired[str]


class EMRStepMetadataTypeDef(TypedDict):
    ClusterId: NotRequired[str]
    StepId: NotRequired[str]
    StepName: NotRequired[str]
    LogFilePath: NotRequired[str]


class EbsStorageSettingsTypeDef(TypedDict):
    EbsVolumeSizeInGb: int


class EdgeDeploymentPlanSummaryTypeDef(TypedDict):
    EdgeDeploymentPlanArn: str
    EdgeDeploymentPlanName: str
    DeviceFleetName: str
    EdgeDeploymentSuccess: int
    EdgeDeploymentPending: int
    EdgeDeploymentFailed: int
    CreationTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]


class EdgeModelStatTypeDef(TypedDict):
    ModelName: str
    ModelVersion: str
    OfflineDeviceCount: int
    ConnectedDeviceCount: int
    ActiveDeviceCount: int
    SamplingDeviceCount: int


class EdgePackagingJobSummaryTypeDef(TypedDict):
    EdgePackagingJobArn: str
    EdgePackagingJobName: str
    EdgePackagingJobStatus: EdgePackagingJobStatusType
    CompilationJobName: NotRequired[str]
    ModelName: NotRequired[str]
    ModelVersion: NotRequired[str]
    CreationTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]


class EdgeTypeDef(TypedDict):
    SourceArn: NotRequired[str]
    DestinationArn: NotRequired[str]
    AssociationType: NotRequired[AssociationEdgeTypeType]


class EmrSettingsOutputTypeDef(TypedDict):
    AssumableRoleArns: NotRequired[List[str]]
    ExecutionRoleArns: NotRequired[List[str]]


class EmrSettingsTypeDef(TypedDict):
    AssumableRoleArns: NotRequired[Sequence[str]]
    ExecutionRoleArns: NotRequired[Sequence[str]]


class EndpointConfigStepMetadataTypeDef(TypedDict):
    Arn: NotRequired[str]


class EndpointConfigSummaryTypeDef(TypedDict):
    EndpointConfigName: str
    EndpointConfigArn: str
    CreationTime: datetime


class EndpointInfoTypeDef(TypedDict):
    EndpointName: NotRequired[str]


class ProductionVariantServerlessConfigTypeDef(TypedDict):
    MemorySizeInMB: int
    MaxConcurrency: int
    ProvisionedConcurrency: NotRequired[int]


class InferenceMetricsTypeDef(TypedDict):
    MaxInvocations: int
    ModelLatency: int


class EndpointStepMetadataTypeDef(TypedDict):
    Arn: NotRequired[str]


class EndpointSummaryTypeDef(TypedDict):
    EndpointName: str
    EndpointArn: str
    CreationTime: datetime
    LastModifiedTime: datetime
    EndpointStatus: EndpointStatusType


class EnvironmentParameterTypeDef(TypedDict):
    Key: str
    ValueType: str
    Value: str


class FailStepMetadataTypeDef(TypedDict):
    ErrorMessage: NotRequired[str]


class FilterTypeDef(TypedDict):
    Name: str
    Operator: NotRequired[OperatorType]
    Value: NotRequired[str]


FinalHyperParameterTuningJobObjectiveMetricTypeDef = TypedDict(
    "FinalHyperParameterTuningJobObjectiveMetricTypeDef",
    {
        "MetricName": str,
        "Value": float,
        "Type": NotRequired[HyperParameterTuningJobObjectiveTypeType],
    },
)


class FlowDefinitionSummaryTypeDef(TypedDict):
    FlowDefinitionName: str
    FlowDefinitionArn: str
    FlowDefinitionStatus: FlowDefinitionStatusType
    CreationTime: datetime
    FailureReason: NotRequired[str]


class GetDeviceFleetReportRequestRequestTypeDef(TypedDict):
    DeviceFleetName: str


class GetLineageGroupPolicyRequestRequestTypeDef(TypedDict):
    LineageGroupName: str


class GetModelPackageGroupPolicyInputRequestTypeDef(TypedDict):
    ModelPackageGroupName: str


class ScalingPolicyObjectiveTypeDef(TypedDict):
    MinInvocationsPerMinute: NotRequired[int]
    MaxInvocationsPerMinute: NotRequired[int]


class ScalingPolicyMetricTypeDef(TypedDict):
    InvocationsPerInstance: NotRequired[int]
    ModelLatency: NotRequired[int]


class PropertyNameSuggestionTypeDef(TypedDict):
    PropertyName: NotRequired[str]


class GitConfigForUpdateTypeDef(TypedDict):
    SecretArn: NotRequired[str]


class HiddenSageMakerImageOutputTypeDef(TypedDict):
    SageMakerImageName: NotRequired[Literal["sagemaker_distribution"]]
    VersionAliases: NotRequired[List[str]]


class HiddenSageMakerImageTypeDef(TypedDict):
    SageMakerImageName: NotRequired[Literal["sagemaker_distribution"]]
    VersionAliases: NotRequired[Sequence[str]]


class HolidayConfigAttributesTypeDef(TypedDict):
    CountryCode: NotRequired[str]


class HubContentInfoTypeDef(TypedDict):
    HubContentName: str
    HubContentArn: str
    HubContentVersion: str
    HubContentType: HubContentTypeType
    DocumentSchemaVersion: str
    HubContentStatus: HubContentStatusType
    CreationTime: datetime
    SageMakerPublicHubContentArn: NotRequired[str]
    HubContentDisplayName: NotRequired[str]
    HubContentDescription: NotRequired[str]
    SupportStatus: NotRequired[HubContentSupportStatusType]
    HubContentSearchKeywords: NotRequired[List[str]]
    OriginalCreationTime: NotRequired[datetime]


class HubInfoTypeDef(TypedDict):
    HubName: str
    HubArn: str
    HubStatus: HubStatusType
    CreationTime: datetime
    LastModifiedTime: datetime
    HubDisplayName: NotRequired[str]
    HubDescription: NotRequired[str]
    HubSearchKeywords: NotRequired[List[str]]


class HumanLoopActivationConditionsConfigTypeDef(TypedDict):
    HumanLoopActivationConditions: str


class UiConfigTypeDef(TypedDict):
    UiTemplateS3Uri: NotRequired[str]
    HumanTaskUiArn: NotRequired[str]


class HumanTaskUiSummaryTypeDef(TypedDict):
    HumanTaskUiName: str
    HumanTaskUiArn: str
    CreationTime: datetime


HyperParameterTuningJobObjectiveTypeDef = TypedDict(
    "HyperParameterTuningJobObjectiveTypeDef",
    {
        "Type": HyperParameterTuningJobObjectiveTypeType,
        "MetricName": str,
    },
)


class HyperParameterTuningInstanceConfigTypeDef(TypedDict):
    InstanceType: TrainingInstanceTypeType
    InstanceCount: int
    VolumeSizeInGB: int


class ResourceLimitsTypeDef(TypedDict):
    MaxParallelTrainingJobs: int
    MaxNumberOfTrainingJobs: NotRequired[int]
    MaxRuntimeInSeconds: NotRequired[int]


class HyperbandStrategyConfigTypeDef(TypedDict):
    MinResource: NotRequired[int]
    MaxResource: NotRequired[int]


class ParentHyperParameterTuningJobTypeDef(TypedDict):
    HyperParameterTuningJobName: NotRequired[str]


class IamIdentityTypeDef(TypedDict):
    Arn: NotRequired[str]
    PrincipalId: NotRequired[str]
    SourceIdentity: NotRequired[str]


class IamPolicyConstraintsTypeDef(TypedDict):
    SourceIp: NotRequired[EnabledOrDisabledType]
    VpcSourceIp: NotRequired[EnabledOrDisabledType]


class RepositoryAuthConfigTypeDef(TypedDict):
    RepositoryCredentialsProviderArn: str


class ImageTypeDef(TypedDict):
    CreationTime: datetime
    ImageArn: str
    ImageName: str
    ImageStatus: ImageStatusType
    LastModifiedTime: datetime
    Description: NotRequired[str]
    DisplayName: NotRequired[str]
    FailureReason: NotRequired[str]


class ImageVersionTypeDef(TypedDict):
    CreationTime: datetime
    ImageArn: str
    ImageVersionArn: str
    ImageVersionStatus: ImageVersionStatusType
    LastModifiedTime: datetime
    Version: int
    FailureReason: NotRequired[str]


class InferenceComponentComputeResourceRequirementsTypeDef(TypedDict):
    MinMemoryRequiredInMb: int
    NumberOfCpuCoresRequired: NotRequired[float]
    NumberOfAcceleratorDevicesRequired: NotRequired[float]
    MaxMemoryRequiredInMb: NotRequired[int]


class InferenceComponentContainerSpecificationTypeDef(TypedDict):
    Image: NotRequired[str]
    ArtifactUrl: NotRequired[str]
    Environment: NotRequired[Mapping[str, str]]


class InferenceComponentStartupParametersTypeDef(TypedDict):
    ModelDataDownloadTimeoutInSeconds: NotRequired[int]
    ContainerStartupHealthCheckTimeoutInSeconds: NotRequired[int]


class InferenceComponentSummaryTypeDef(TypedDict):
    CreationTime: datetime
    InferenceComponentArn: str
    InferenceComponentName: str
    EndpointArn: str
    EndpointName: str
    VariantName: str
    LastModifiedTime: datetime
    InferenceComponentStatus: NotRequired[InferenceComponentStatusType]


class InferenceHubAccessConfigTypeDef(TypedDict):
    HubContentArn: str


class RecommendationMetricsTypeDef(TypedDict):
    CostPerHour: NotRequired[float]
    CostPerInference: NotRequired[float]
    MaxInvocations: NotRequired[int]
    ModelLatency: NotRequired[int]
    CpuUtilization: NotRequired[float]
    MemoryUtilization: NotRequired[float]
    ModelSetupTime: NotRequired[int]


class InferenceRecommendationsJobTypeDef(TypedDict):
    JobName: str
    JobDescription: str
    JobType: RecommendationJobTypeType
    JobArn: str
    Status: RecommendationJobStatusType
    CreationTime: datetime
    RoleArn: str
    LastModifiedTime: datetime
    CompletionTime: NotRequired[datetime]
    FailureReason: NotRequired[str]
    ModelName: NotRequired[str]
    SamplePayloadUrl: NotRequired[str]
    ModelPackageVersionArn: NotRequired[str]


class InstanceGroupTypeDef(TypedDict):
    InstanceType: TrainingInstanceTypeType
    InstanceCount: int
    InstanceGroupName: str


class IntegerParameterRangeSpecificationTypeDef(TypedDict):
    MinValue: str
    MaxValue: str


class IntegerParameterRangeTypeDef(TypedDict):
    Name: str
    MinValue: str
    MaxValue: str
    ScalingType: NotRequired[HyperParameterScalingTypeType]


class KernelSpecTypeDef(TypedDict):
    Name: str
    DisplayName: NotRequired[str]


class LabelCountersForWorkteamTypeDef(TypedDict):
    HumanLabeled: NotRequired[int]
    PendingHuman: NotRequired[int]
    Total: NotRequired[int]


class LabelingJobDataAttributesOutputTypeDef(TypedDict):
    ContentClassifiers: NotRequired[List[ContentClassifierType]]


class LabelingJobDataAttributesTypeDef(TypedDict):
    ContentClassifiers: NotRequired[Sequence[ContentClassifierType]]


class LabelingJobS3DataSourceTypeDef(TypedDict):
    ManifestS3Uri: str


class LabelingJobSnsDataSourceTypeDef(TypedDict):
    SnsTopicArn: str


class LineageGroupSummaryTypeDef(TypedDict):
    LineageGroupArn: NotRequired[str]
    LineageGroupName: NotRequired[str]
    DisplayName: NotRequired[str]
    CreationTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListAliasesRequestRequestTypeDef(TypedDict):
    ImageName: str
    Alias: NotRequired[str]
    Version: NotRequired[int]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListAppsRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    SortOrder: NotRequired[SortOrderType]
    SortBy: NotRequired[Literal["CreationTime"]]
    DomainIdEquals: NotRequired[str]
    UserProfileNameEquals: NotRequired[str]
    SpaceNameEquals: NotRequired[str]


class ListCandidatesForAutoMLJobRequestRequestTypeDef(TypedDict):
    AutoMLJobName: str
    StatusEquals: NotRequired[CandidateStatusType]
    CandidateNameEquals: NotRequired[str]
    SortOrder: NotRequired[AutoMLSortOrderType]
    SortBy: NotRequired[CandidateSortByType]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class MonitoringJobDefinitionSummaryTypeDef(TypedDict):
    MonitoringJobDefinitionName: str
    MonitoringJobDefinitionArn: str
    CreationTime: datetime
    EndpointName: str


class ListDomainsRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListInferenceRecommendationsJobStepsRequestRequestTypeDef(TypedDict):
    JobName: str
    Status: NotRequired[RecommendationJobStatusType]
    StepType: NotRequired[Literal["BENCHMARK"]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class TrackingServerSummaryTypeDef(TypedDict):
    TrackingServerArn: NotRequired[str]
    TrackingServerName: NotRequired[str]
    CreationTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]
    TrackingServerStatus: NotRequired[TrackingServerStatusType]
    IsActive: NotRequired[IsTrackingServerActiveType]
    MlflowVersion: NotRequired[str]


class ModelCardExportJobSummaryTypeDef(TypedDict):
    ModelCardExportJobName: str
    ModelCardExportJobArn: str
    Status: ModelCardExportJobStatusType
    ModelCardName: str
    ModelCardVersion: int
    CreatedAt: datetime
    LastModifiedAt: datetime


class ModelCardVersionSummaryTypeDef(TypedDict):
    ModelCardName: str
    ModelCardArn: str
    ModelCardStatus: ModelCardStatusType
    ModelCardVersion: int
    CreationTime: datetime
    LastModifiedTime: NotRequired[datetime]


class ModelCardSummaryTypeDef(TypedDict):
    ModelCardName: str
    ModelCardArn: str
    ModelCardStatus: ModelCardStatusType
    CreationTime: datetime
    LastModifiedTime: NotRequired[datetime]


class ModelMetadataSummaryTypeDef(TypedDict):
    Domain: str
    Framework: str
    Task: str
    Model: str
    FrameworkVersion: str


class ModelPackageGroupSummaryTypeDef(TypedDict):
    ModelPackageGroupName: str
    ModelPackageGroupArn: str
    CreationTime: datetime
    ModelPackageGroupStatus: ModelPackageGroupStatusType
    ModelPackageGroupDescription: NotRequired[str]


class ModelPackageSummaryTypeDef(TypedDict):
    ModelPackageArn: str
    CreationTime: datetime
    ModelPackageStatus: ModelPackageStatusType
    ModelPackageName: NotRequired[str]
    ModelPackageGroupName: NotRequired[str]
    ModelPackageVersion: NotRequired[int]
    ModelPackageDescription: NotRequired[str]
    ModelApprovalStatus: NotRequired[ModelApprovalStatusType]


class ModelSummaryTypeDef(TypedDict):
    ModelName: str
    ModelArn: str
    CreationTime: datetime


class MonitoringAlertHistorySummaryTypeDef(TypedDict):
    MonitoringScheduleName: str
    MonitoringAlertName: str
    CreationTime: datetime
    AlertStatus: MonitoringAlertStatusType


class ListMonitoringAlertsRequestRequestTypeDef(TypedDict):
    MonitoringScheduleName: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class MonitoringScheduleSummaryTypeDef(TypedDict):
    MonitoringScheduleName: str
    MonitoringScheduleArn: str
    CreationTime: datetime
    LastModifiedTime: datetime
    MonitoringScheduleStatus: ScheduleStatusType
    EndpointName: NotRequired[str]
    MonitoringJobDefinitionName: NotRequired[str]
    MonitoringType: NotRequired[MonitoringTypeType]


class NotebookInstanceLifecycleConfigSummaryTypeDef(TypedDict):
    NotebookInstanceLifecycleConfigName: str
    NotebookInstanceLifecycleConfigArn: str
    CreationTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]


class NotebookInstanceSummaryTypeDef(TypedDict):
    NotebookInstanceName: str
    NotebookInstanceArn: str
    NotebookInstanceStatus: NotRequired[NotebookInstanceStatusType]
    Url: NotRequired[str]
    InstanceType: NotRequired[InstanceTypeType]
    CreationTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]
    NotebookInstanceLifecycleConfigName: NotRequired[str]
    DefaultCodeRepository: NotRequired[str]
    AdditionalCodeRepositories: NotRequired[List[str]]


class OptimizationJobSummaryTypeDef(TypedDict):
    OptimizationJobName: str
    OptimizationJobArn: str
    CreationTime: datetime
    OptimizationJobStatus: OptimizationJobStatusType
    DeploymentInstanceType: OptimizationJobDeploymentInstanceTypeType
    OptimizationTypes: List[str]
    OptimizationStartTime: NotRequired[datetime]
    OptimizationEndTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]


class ListPipelineExecutionStepsRequestRequestTypeDef(TypedDict):
    PipelineExecutionArn: NotRequired[str]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    SortOrder: NotRequired[SortOrderType]


class PipelineExecutionSummaryTypeDef(TypedDict):
    PipelineExecutionArn: NotRequired[str]
    StartTime: NotRequired[datetime]
    PipelineExecutionStatus: NotRequired[PipelineExecutionStatusType]
    PipelineExecutionDescription: NotRequired[str]
    PipelineExecutionDisplayName: NotRequired[str]
    PipelineExecutionFailureReason: NotRequired[str]


class ListPipelineParametersForExecutionRequestRequestTypeDef(TypedDict):
    PipelineExecutionArn: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ParameterTypeDef(TypedDict):
    Name: str
    Value: str


class PipelineSummaryTypeDef(TypedDict):
    PipelineArn: NotRequired[str]
    PipelineName: NotRequired[str]
    PipelineDisplayName: NotRequired[str]
    PipelineDescription: NotRequired[str]
    RoleArn: NotRequired[str]
    CreationTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]
    LastExecutionTime: NotRequired[datetime]


class ProcessingJobSummaryTypeDef(TypedDict):
    ProcessingJobName: str
    ProcessingJobArn: str
    CreationTime: datetime
    ProcessingJobStatus: ProcessingJobStatusType
    ProcessingEndTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]
    FailureReason: NotRequired[str]
    ExitMessage: NotRequired[str]


class ProjectSummaryTypeDef(TypedDict):
    ProjectName: str
    ProjectArn: str
    ProjectId: str
    CreationTime: datetime
    ProjectStatus: ProjectStatusType
    ProjectDescription: NotRequired[str]


class ResourceCatalogTypeDef(TypedDict):
    ResourceCatalogArn: str
    ResourceCatalogName: str
    Description: str
    CreationTime: datetime


class ListSpacesRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    SortOrder: NotRequired[SortOrderType]
    SortBy: NotRequired[SpaceSortKeyType]
    DomainIdEquals: NotRequired[str]
    SpaceNameContains: NotRequired[str]


class ListStageDevicesRequestRequestTypeDef(TypedDict):
    EdgeDeploymentPlanName: str
    StageName: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    ExcludeDevicesDeployedInOtherStage: NotRequired[bool]


class StudioLifecycleConfigDetailsTypeDef(TypedDict):
    StudioLifecycleConfigArn: NotRequired[str]
    StudioLifecycleConfigName: NotRequired[str]
    CreationTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]
    StudioLifecycleConfigAppType: NotRequired[StudioLifecycleConfigAppTypeType]


class ListSubscribedWorkteamsRequestRequestTypeDef(TypedDict):
    NameContains: NotRequired[str]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListTagsInputRequestTypeDef(TypedDict):
    ResourceArn: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListTrainingJobsForHyperParameterTuningJobRequestRequestTypeDef(TypedDict):
    HyperParameterTuningJobName: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    StatusEquals: NotRequired[TrainingJobStatusType]
    SortBy: NotRequired[TrainingJobSortByOptionsType]
    SortOrder: NotRequired[SortOrderType]


class TransformJobSummaryTypeDef(TypedDict):
    TransformJobName: str
    TransformJobArn: str
    CreationTime: datetime
    TransformJobStatus: TransformJobStatusType
    TransformEndTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]
    FailureReason: NotRequired[str]


class ListUserProfilesRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    SortOrder: NotRequired[SortOrderType]
    SortBy: NotRequired[UserProfileSortKeyType]
    DomainIdEquals: NotRequired[str]
    UserProfileNameContains: NotRequired[str]


class UserProfileDetailsTypeDef(TypedDict):
    DomainId: NotRequired[str]
    UserProfileName: NotRequired[str]
    Status: NotRequired[UserProfileStatusType]
    CreationTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]


class ListWorkforcesRequestRequestTypeDef(TypedDict):
    SortBy: NotRequired[ListWorkforcesSortByOptionsType]
    SortOrder: NotRequired[SortOrderType]
    NameContains: NotRequired[str]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListWorkteamsRequestRequestTypeDef(TypedDict):
    SortBy: NotRequired[ListWorkteamsSortByOptionsType]
    SortOrder: NotRequired[SortOrderType]
    NameContains: NotRequired[str]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class OidcMemberDefinitionOutputTypeDef(TypedDict):
    Groups: NotRequired[List[str]]


class PredefinedMetricSpecificationTypeDef(TypedDict):
    PredefinedMetricType: NotRequired[str]


class ModelAccessConfigTypeDef(TypedDict):
    AcceptEula: bool


class MonitoringGroundTruthS3InputTypeDef(TypedDict):
    S3Uri: NotRequired[str]


class ModelCompilationConfigOutputTypeDef(TypedDict):
    Image: NotRequired[str]
    OverrideEnvironment: NotRequired[Dict[str, str]]


class ModelCompilationConfigTypeDef(TypedDict):
    Image: NotRequired[str]
    OverrideEnvironment: NotRequired[Mapping[str, str]]


class ModelDashboardEndpointTypeDef(TypedDict):
    EndpointName: str
    EndpointArn: str
    CreationTime: datetime
    LastModifiedTime: datetime
    EndpointStatus: EndpointStatusType


class ModelDashboardIndicatorActionTypeDef(TypedDict):
    Enabled: NotRequired[bool]


class RealTimeInferenceConfigTypeDef(TypedDict):
    InstanceType: InstanceTypeType
    InstanceCount: int


class ModelInputTypeDef(TypedDict):
    DataInputConfig: str


class ModelLatencyThresholdTypeDef(TypedDict):
    Percentile: NotRequired[str]
    ValueInMilliseconds: NotRequired[int]


class ModelMetadataFilterTypeDef(TypedDict):
    Name: ModelMetadataFilterTypeType
    Value: str


class ModelPackageStatusItemTypeDef(TypedDict):
    Name: str
    Status: DetailedModelPackageStatusType
    FailureReason: NotRequired[str]


class ModelQuantizationConfigOutputTypeDef(TypedDict):
    Image: NotRequired[str]
    OverrideEnvironment: NotRequired[Dict[str, str]]


class ModelQuantizationConfigTypeDef(TypedDict):
    Image: NotRequired[str]
    OverrideEnvironment: NotRequired[Mapping[str, str]]


class ModelShardingConfigOutputTypeDef(TypedDict):
    Image: NotRequired[str]
    OverrideEnvironment: NotRequired[Dict[str, str]]


class ModelShardingConfigTypeDef(TypedDict):
    Image: NotRequired[str]
    OverrideEnvironment: NotRequired[Mapping[str, str]]


class ModelStepMetadataTypeDef(TypedDict):
    Arn: NotRequired[str]


class MonitoringAppSpecificationOutputTypeDef(TypedDict):
    ImageUri: str
    ContainerEntrypoint: NotRequired[List[str]]
    ContainerArguments: NotRequired[List[str]]
    RecordPreprocessorSourceUri: NotRequired[str]
    PostAnalyticsProcessorSourceUri: NotRequired[str]


class MonitoringAppSpecificationTypeDef(TypedDict):
    ImageUri: str
    ContainerEntrypoint: NotRequired[Sequence[str]]
    ContainerArguments: NotRequired[Sequence[str]]
    RecordPreprocessorSourceUri: NotRequired[str]
    PostAnalyticsProcessorSourceUri: NotRequired[str]


class MonitoringClusterConfigTypeDef(TypedDict):
    InstanceCount: int
    InstanceType: ProcessingInstanceTypeType
    VolumeSizeInGB: int
    VolumeKmsKeyId: NotRequired[str]


class MonitoringCsvDatasetFormatTypeDef(TypedDict):
    Header: NotRequired[bool]


class MonitoringJsonDatasetFormatTypeDef(TypedDict):
    Line: NotRequired[bool]


class MonitoringS3OutputTypeDef(TypedDict):
    S3Uri: str
    LocalPath: str
    S3UploadMode: NotRequired[ProcessingS3UploadModeType]


class ScheduleConfigTypeDef(TypedDict):
    ScheduleExpression: str
    DataAnalysisStartTime: NotRequired[str]
    DataAnalysisEndTime: NotRequired[str]


class S3StorageConfigTypeDef(TypedDict):
    S3Uri: str
    KmsKeyId: NotRequired[str]
    ResolvedOutputS3Uri: NotRequired[str]


class OidcConfigForResponseTypeDef(TypedDict):
    ClientId: NotRequired[str]
    Issuer: NotRequired[str]
    AuthorizationEndpoint: NotRequired[str]
    TokenEndpoint: NotRequired[str]
    UserInfoEndpoint: NotRequired[str]
    LogoutEndpoint: NotRequired[str]
    JwksUri: NotRequired[str]
    Scope: NotRequired[str]
    AuthenticationRequestExtraParams: NotRequired[Dict[str, str]]


class OidcMemberDefinitionTypeDef(TypedDict):
    Groups: NotRequired[Sequence[str]]


class OnlineStoreSecurityConfigTypeDef(TypedDict):
    KmsKeyId: NotRequired[str]


class TtlDurationTypeDef(TypedDict):
    Unit: NotRequired[TtlDurationUnitType]
    Value: NotRequired[int]


class OptimizationModelAccessConfigTypeDef(TypedDict):
    AcceptEula: bool


class TargetPlatformTypeDef(TypedDict):
    Os: TargetPlatformOsType
    Arch: TargetPlatformArchType
    Accelerator: NotRequired[TargetPlatformAcceleratorType]


class OwnershipSettingsSummaryTypeDef(TypedDict):
    OwnerUserProfileName: NotRequired[str]


class ParentTypeDef(TypedDict):
    TrialName: NotRequired[str]
    ExperimentName: NotRequired[str]


class ProductionVariantManagedInstanceScalingTypeDef(TypedDict):
    Status: NotRequired[ManagedInstanceScalingStatusType]
    MinInstanceCount: NotRequired[int]
    MaxInstanceCount: NotRequired[int]


class ProductionVariantRoutingConfigTypeDef(TypedDict):
    RoutingStrategy: RoutingStrategyType


class ProductionVariantStatusTypeDef(TypedDict):
    Status: VariantStatusType
    StatusMessage: NotRequired[str]
    StartTime: NotRequired[datetime]


class PhaseTypeDef(TypedDict):
    InitialNumberOfUsers: NotRequired[int]
    SpawnRate: NotRequired[int]
    DurationInSeconds: NotRequired[int]


class ProcessingJobStepMetadataTypeDef(TypedDict):
    Arn: NotRequired[str]


class QualityCheckStepMetadataTypeDef(TypedDict):
    CheckType: NotRequired[str]
    BaselineUsedForDriftCheckStatistics: NotRequired[str]
    BaselineUsedForDriftCheckConstraints: NotRequired[str]
    CalculatedBaselineStatistics: NotRequired[str]
    CalculatedBaselineConstraints: NotRequired[str]
    ModelPackageGroupName: NotRequired[str]
    ViolationReport: NotRequired[str]
    CheckJobArn: NotRequired[str]
    SkipCheck: NotRequired[bool]
    RegisterNewBaseline: NotRequired[bool]


class RegisterModelStepMetadataTypeDef(TypedDict):
    Arn: NotRequired[str]


class TrainingJobStepMetadataTypeDef(TypedDict):
    Arn: NotRequired[str]


class TransformJobStepMetadataTypeDef(TypedDict):
    Arn: NotRequired[str]


class TuningJobStepMetaDataTypeDef(TypedDict):
    Arn: NotRequired[str]


class SelectiveExecutionResultTypeDef(TypedDict):
    SourcePipelineExecutionArn: NotRequired[str]


class ProcessingClusterConfigTypeDef(TypedDict):
    InstanceCount: int
    InstanceType: ProcessingInstanceTypeType
    VolumeSizeInGB: int
    VolumeKmsKeyId: NotRequired[str]


class ProcessingFeatureStoreOutputTypeDef(TypedDict):
    FeatureGroupName: str


ProcessingS3InputTypeDef = TypedDict(
    "ProcessingS3InputTypeDef",
    {
        "S3Uri": str,
        "S3DataType": ProcessingS3DataTypeType,
        "LocalPath": NotRequired[str],
        "S3InputMode": NotRequired[ProcessingS3InputModeType],
        "S3DataDistributionType": NotRequired[ProcessingS3DataDistributionTypeType],
        "S3CompressionType": NotRequired[ProcessingS3CompressionTypeType],
    },
)


class ProcessingS3OutputTypeDef(TypedDict):
    S3Uri: str
    S3UploadMode: ProcessingS3UploadModeType
    LocalPath: NotRequired[str]


class ProductionVariantCoreDumpConfigTypeDef(TypedDict):
    DestinationS3Uri: str
    KmsKeyId: NotRequired[str]


class ProfilerConfigForUpdateTypeDef(TypedDict):
    S3OutputPath: NotRequired[str]
    ProfilingIntervalInMilliseconds: NotRequired[int]
    ProfilingParameters: NotRequired[Mapping[str, str]]
    DisableProfiler: NotRequired[bool]


class ProfilerRuleConfigurationTypeDef(TypedDict):
    RuleConfigurationName: str
    RuleEvaluatorImage: str
    LocalPath: NotRequired[str]
    S3OutputPath: NotRequired[str]
    InstanceType: NotRequired[ProcessingInstanceTypeType]
    VolumeSizeInGB: NotRequired[int]
    RuleParameters: NotRequired[Mapping[str, str]]


class PropertyNameQueryTypeDef(TypedDict):
    PropertyNameHint: str


class ProvisioningParameterTypeDef(TypedDict):
    Key: NotRequired[str]
    Value: NotRequired[str]


class USDTypeDef(TypedDict):
    Dollars: NotRequired[int]
    Cents: NotRequired[int]
    TenthFractionsOfACent: NotRequired[int]


class PutModelPackageGroupPolicyInputRequestTypeDef(TypedDict):
    ModelPackageGroupName: str
    ResourcePolicy: str


VertexTypeDef = TypedDict(
    "VertexTypeDef",
    {
        "Arn": NotRequired[str],
        "Type": NotRequired[str],
        "LineageType": NotRequired[LineageTypeType],
    },
)


class RStudioServerProAppSettingsTypeDef(TypedDict):
    AccessStatus: NotRequired[RStudioServerProAccessStatusType]
    UserGroup: NotRequired[RStudioServerProUserGroupType]


class RecommendationJobCompiledOutputConfigTypeDef(TypedDict):
    S3OutputUri: NotRequired[str]


class RecommendationJobPayloadConfigOutputTypeDef(TypedDict):
    SamplePayloadUrl: NotRequired[str]
    SupportedContentTypes: NotRequired[List[str]]


class RecommendationJobResourceLimitTypeDef(TypedDict):
    MaxNumberOfTests: NotRequired[int]
    MaxParallelOfTests: NotRequired[int]


class RecommendationJobVpcConfigOutputTypeDef(TypedDict):
    SecurityGroupIds: List[str]
    Subnets: List[str]


class RecommendationJobPayloadConfigTypeDef(TypedDict):
    SamplePayloadUrl: NotRequired[str]
    SupportedContentTypes: NotRequired[Sequence[str]]


class RecommendationJobVpcConfigTypeDef(TypedDict):
    SecurityGroupIds: Sequence[str]
    Subnets: Sequence[str]


class RemoteDebugConfigForUpdateTypeDef(TypedDict):
    EnableRemoteDebug: NotRequired[bool]


class RenderableTaskTypeDef(TypedDict):
    Input: str


class RenderingErrorTypeDef(TypedDict):
    Code: str
    Message: str


class ResourceConfigForUpdateTypeDef(TypedDict):
    KeepAlivePeriodInSeconds: int


S3DataSourceTypeDef = TypedDict(
    "S3DataSourceTypeDef",
    {
        "S3DataType": S3DataTypeType,
        "S3Uri": str,
        "S3DataDistributionType": NotRequired[S3DataDistributionType],
        "AttributeNames": NotRequired[Sequence[str]],
        "InstanceGroupNames": NotRequired[Sequence[str]],
    },
)


class VisibilityConditionsTypeDef(TypedDict):
    Key: NotRequired[str]
    Value: NotRequired[str]


class SelectedStepTypeDef(TypedDict):
    StepName: str


class SendPipelineExecutionStepFailureRequestRequestTypeDef(TypedDict):
    CallbackToken: str
    FailureReason: NotRequired[str]
    ClientRequestToken: NotRequired[str]


class ShadowModelVariantConfigTypeDef(TypedDict):
    ShadowModelVariantName: str
    SamplingPercentage: int


class SharingSettingsTypeDef(TypedDict):
    NotebookOutputOption: NotRequired[NotebookOutputOptionType]
    S3OutputPath: NotRequired[str]
    S3KmsKeyId: NotRequired[str]


class SourceIpConfigOutputTypeDef(TypedDict):
    Cidrs: List[str]


class SpaceIdleSettingsTypeDef(TypedDict):
    IdleTimeoutInMinutes: NotRequired[int]


class SpaceSharingSettingsSummaryTypeDef(TypedDict):
    SharingType: NotRequired[SharingTypeType]


class StairsTypeDef(TypedDict):
    DurationInSeconds: NotRequired[int]
    NumberOfSteps: NotRequired[int]
    UsersPerStep: NotRequired[int]


class StartEdgeDeploymentStageRequestRequestTypeDef(TypedDict):
    EdgeDeploymentPlanName: str
    StageName: str


class StartInferenceExperimentRequestRequestTypeDef(TypedDict):
    Name: str


class StartMlflowTrackingServerRequestRequestTypeDef(TypedDict):
    TrackingServerName: str


class StartMonitoringScheduleRequestRequestTypeDef(TypedDict):
    MonitoringScheduleName: str


class StartNotebookInstanceInputRequestTypeDef(TypedDict):
    NotebookInstanceName: str


class StopAutoMLJobRequestRequestTypeDef(TypedDict):
    AutoMLJobName: str


class StopCompilationJobRequestRequestTypeDef(TypedDict):
    CompilationJobName: str


class StopEdgeDeploymentStageRequestRequestTypeDef(TypedDict):
    EdgeDeploymentPlanName: str
    StageName: str


class StopEdgePackagingJobRequestRequestTypeDef(TypedDict):
    EdgePackagingJobName: str


class StopHyperParameterTuningJobRequestRequestTypeDef(TypedDict):
    HyperParameterTuningJobName: str


class StopInferenceRecommendationsJobRequestRequestTypeDef(TypedDict):
    JobName: str


class StopLabelingJobRequestRequestTypeDef(TypedDict):
    LabelingJobName: str


class StopMlflowTrackingServerRequestRequestTypeDef(TypedDict):
    TrackingServerName: str


class StopMonitoringScheduleRequestRequestTypeDef(TypedDict):
    MonitoringScheduleName: str


class StopNotebookInstanceInputRequestTypeDef(TypedDict):
    NotebookInstanceName: str


class StopOptimizationJobRequestRequestTypeDef(TypedDict):
    OptimizationJobName: str


class StopPipelineExecutionRequestRequestTypeDef(TypedDict):
    PipelineExecutionArn: str
    ClientRequestToken: str


class StopProcessingJobRequestRequestTypeDef(TypedDict):
    ProcessingJobName: str


class StopTrainingJobRequestRequestTypeDef(TypedDict):
    TrainingJobName: str


class StopTransformJobRequestRequestTypeDef(TypedDict):
    TransformJobName: str


class ThroughputConfigUpdateTypeDef(TypedDict):
    ThroughputMode: NotRequired[ThroughputModeType]
    ProvisionedReadCapacityUnits: NotRequired[int]
    ProvisionedWriteCapacityUnits: NotRequired[int]


class TimeSeriesConfigOutputTypeDef(TypedDict):
    TargetAttributeName: str
    TimestampAttributeName: str
    ItemIdentifierAttributeName: str
    GroupingAttributeNames: NotRequired[List[str]]


class TimeSeriesConfigTypeDef(TypedDict):
    TargetAttributeName: str
    TimestampAttributeName: str
    ItemIdentifierAttributeName: str
    GroupingAttributeNames: NotRequired[Sequence[str]]


class TimeSeriesTransformationsOutputTypeDef(TypedDict):
    Filling: NotRequired[Dict[str, Dict[FillingTypeType, str]]]
    Aggregation: NotRequired[Dict[str, AggregationTransformationValueType]]


class TimeSeriesTransformationsTypeDef(TypedDict):
    Filling: NotRequired[Mapping[str, Mapping[FillingTypeType, str]]]
    Aggregation: NotRequired[Mapping[str, AggregationTransformationValueType]]


class TrainingRepositoryAuthConfigTypeDef(TypedDict):
    TrainingRepositoryCredentialsProviderArn: str


class TransformS3DataSourceTypeDef(TypedDict):
    S3DataType: S3DataTypeType
    S3Uri: str


class UpdateActionRequestRequestTypeDef(TypedDict):
    ActionName: str
    Description: NotRequired[str]
    Status: NotRequired[ActionStatusType]
    Properties: NotRequired[Mapping[str, str]]
    PropertiesToRemove: NotRequired[Sequence[str]]


class UpdateArtifactRequestRequestTypeDef(TypedDict):
    ArtifactArn: str
    ArtifactName: NotRequired[str]
    Properties: NotRequired[Mapping[str, str]]
    PropertiesToRemove: NotRequired[Sequence[str]]


class UpdateClusterSoftwareRequestRequestTypeDef(TypedDict):
    ClusterName: str


class UpdateContextRequestRequestTypeDef(TypedDict):
    ContextName: str
    Description: NotRequired[str]
    Properties: NotRequired[Mapping[str, str]]
    PropertiesToRemove: NotRequired[Sequence[str]]


class VariantPropertyTypeDef(TypedDict):
    VariantPropertyType: VariantPropertyTypeType


class UpdateExperimentRequestRequestTypeDef(TypedDict):
    ExperimentName: str
    DisplayName: NotRequired[str]
    Description: NotRequired[str]


class UpdateHubRequestRequestTypeDef(TypedDict):
    HubName: str
    HubDescription: NotRequired[str]
    HubDisplayName: NotRequired[str]
    HubSearchKeywords: NotRequired[Sequence[str]]


class UpdateImageRequestRequestTypeDef(TypedDict):
    ImageName: str
    DeleteProperties: NotRequired[Sequence[str]]
    Description: NotRequired[str]
    DisplayName: NotRequired[str]
    RoleArn: NotRequired[str]


class UpdateImageVersionRequestRequestTypeDef(TypedDict):
    ImageName: str
    Alias: NotRequired[str]
    Version: NotRequired[int]
    AliasesToAdd: NotRequired[Sequence[str]]
    AliasesToDelete: NotRequired[Sequence[str]]
    VendorGuidance: NotRequired[VendorGuidanceType]
    JobType: NotRequired[JobTypeType]
    MLFramework: NotRequired[str]
    ProgrammingLang: NotRequired[str]
    Processor: NotRequired[ProcessorType]
    Horovod: NotRequired[bool]
    ReleaseNotes: NotRequired[str]


class UpdateMlflowTrackingServerRequestRequestTypeDef(TypedDict):
    TrackingServerName: str
    ArtifactStoreUri: NotRequired[str]
    TrackingServerSize: NotRequired[TrackingServerSizeType]
    AutomaticModelRegistration: NotRequired[bool]
    WeeklyMaintenanceWindowStart: NotRequired[str]


class UpdateModelCardRequestRequestTypeDef(TypedDict):
    ModelCardName: str
    Content: NotRequired[str]
    ModelCardStatus: NotRequired[ModelCardStatusType]


class UpdateMonitoringAlertRequestRequestTypeDef(TypedDict):
    MonitoringScheduleName: str
    MonitoringAlertName: str
    DatapointsToAlert: int
    EvaluationPeriod: int


class UpdateTrialRequestRequestTypeDef(TypedDict):
    TrialName: str
    DisplayName: NotRequired[str]


class WorkforceVpcConfigResponseTypeDef(TypedDict):
    VpcId: str
    SecurityGroupIds: List[str]
    Subnets: List[str]
    VpcEndpointId: NotRequired[str]


class ActionSummaryTypeDef(TypedDict):
    ActionArn: NotRequired[str]
    ActionName: NotRequired[str]
    Source: NotRequired[ActionSourceTypeDef]
    ActionType: NotRequired[str]
    Status: NotRequired[ActionStatusType]
    CreationTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]


class AddAssociationResponseTypeDef(TypedDict):
    SourceArn: str
    DestinationArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class AssociateTrialComponentResponseTypeDef(TypedDict):
    TrialComponentArn: str
    TrialArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateActionResponseTypeDef(TypedDict):
    ActionArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateAlgorithmOutputTypeDef(TypedDict):
    AlgorithmArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateAppImageConfigResponseTypeDef(TypedDict):
    AppImageConfigArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateAppResponseTypeDef(TypedDict):
    AppArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateArtifactResponseTypeDef(TypedDict):
    ArtifactArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateAutoMLJobResponseTypeDef(TypedDict):
    AutoMLJobArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateAutoMLJobV2ResponseTypeDef(TypedDict):
    AutoMLJobArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateClusterResponseTypeDef(TypedDict):
    ClusterArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateCodeRepositoryOutputTypeDef(TypedDict):
    CodeRepositoryArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateCompilationJobResponseTypeDef(TypedDict):
    CompilationJobArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateContextResponseTypeDef(TypedDict):
    ContextArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateDataQualityJobDefinitionResponseTypeDef(TypedDict):
    JobDefinitionArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateDomainResponseTypeDef(TypedDict):
    DomainArn: str
    Url: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateEdgeDeploymentPlanResponseTypeDef(TypedDict):
    EdgeDeploymentPlanArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateEndpointConfigOutputTypeDef(TypedDict):
    EndpointConfigArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateEndpointOutputTypeDef(TypedDict):
    EndpointArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateExperimentResponseTypeDef(TypedDict):
    ExperimentArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateFeatureGroupResponseTypeDef(TypedDict):
    FeatureGroupArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateFlowDefinitionResponseTypeDef(TypedDict):
    FlowDefinitionArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateHubContentReferenceResponseTypeDef(TypedDict):
    HubArn: str
    HubContentArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateHubResponseTypeDef(TypedDict):
    HubArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateHumanTaskUiResponseTypeDef(TypedDict):
    HumanTaskUiArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateHyperParameterTuningJobResponseTypeDef(TypedDict):
    HyperParameterTuningJobArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateImageResponseTypeDef(TypedDict):
    ImageArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateImageVersionResponseTypeDef(TypedDict):
    ImageVersionArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateInferenceComponentOutputTypeDef(TypedDict):
    InferenceComponentArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateInferenceExperimentResponseTypeDef(TypedDict):
    InferenceExperimentArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateInferenceRecommendationsJobResponseTypeDef(TypedDict):
    JobArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateLabelingJobResponseTypeDef(TypedDict):
    LabelingJobArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateMlflowTrackingServerResponseTypeDef(TypedDict):
    TrackingServerArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateModelBiasJobDefinitionResponseTypeDef(TypedDict):
    JobDefinitionArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateModelCardExportJobResponseTypeDef(TypedDict):
    ModelCardExportJobArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateModelCardResponseTypeDef(TypedDict):
    ModelCardArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateModelExplainabilityJobDefinitionResponseTypeDef(TypedDict):
    JobDefinitionArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateModelOutputTypeDef(TypedDict):
    ModelArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateModelPackageGroupOutputTypeDef(TypedDict):
    ModelPackageGroupArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateModelPackageOutputTypeDef(TypedDict):
    ModelPackageArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateModelQualityJobDefinitionResponseTypeDef(TypedDict):
    JobDefinitionArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateMonitoringScheduleResponseTypeDef(TypedDict):
    MonitoringScheduleArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateNotebookInstanceLifecycleConfigOutputTypeDef(TypedDict):
    NotebookInstanceLifecycleConfigArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateNotebookInstanceOutputTypeDef(TypedDict):
    NotebookInstanceArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateOptimizationJobResponseTypeDef(TypedDict):
    OptimizationJobArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreatePipelineResponseTypeDef(TypedDict):
    PipelineArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreatePresignedDomainUrlResponseTypeDef(TypedDict):
    AuthorizedUrl: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreatePresignedMlflowTrackingServerUrlResponseTypeDef(TypedDict):
    AuthorizedUrl: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreatePresignedNotebookInstanceUrlOutputTypeDef(TypedDict):
    AuthorizedUrl: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateProcessingJobResponseTypeDef(TypedDict):
    ProcessingJobArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateProjectOutputTypeDef(TypedDict):
    ProjectArn: str
    ProjectId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateSpaceResponseTypeDef(TypedDict):
    SpaceArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateStudioLifecycleConfigResponseTypeDef(TypedDict):
    StudioLifecycleConfigArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateTrainingJobResponseTypeDef(TypedDict):
    TrainingJobArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateTransformJobResponseTypeDef(TypedDict):
    TransformJobArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateTrialComponentResponseTypeDef(TypedDict):
    TrialComponentArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateTrialResponseTypeDef(TypedDict):
    TrialArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateUserProfileResponseTypeDef(TypedDict):
    UserProfileArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateWorkforceResponseTypeDef(TypedDict):
    WorkforceArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateWorkteamResponseTypeDef(TypedDict):
    WorkteamArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteActionResponseTypeDef(TypedDict):
    ActionArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteArtifactResponseTypeDef(TypedDict):
    ArtifactArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteAssociationResponseTypeDef(TypedDict):
    SourceArn: str
    DestinationArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteClusterResponseTypeDef(TypedDict):
    ClusterArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteContextResponseTypeDef(TypedDict):
    ContextArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteExperimentResponseTypeDef(TypedDict):
    ExperimentArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteInferenceExperimentResponseTypeDef(TypedDict):
    InferenceExperimentArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteMlflowTrackingServerResponseTypeDef(TypedDict):
    TrackingServerArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeletePipelineResponseTypeDef(TypedDict):
    PipelineArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteTrialComponentResponseTypeDef(TypedDict):
    TrialComponentArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteTrialResponseTypeDef(TypedDict):
    TrialArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteWorkteamResponseTypeDef(TypedDict):
    Success: bool
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeImageResponseTypeDef(TypedDict):
    CreationTime: datetime
    Description: str
    DisplayName: str
    FailureReason: str
    ImageArn: str
    ImageName: str
    ImageStatus: ImageStatusType
    LastModifiedTime: datetime
    RoleArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeImageVersionResponseTypeDef(TypedDict):
    BaseImage: str
    ContainerImage: str
    CreationTime: datetime
    FailureReason: str
    ImageArn: str
    ImageVersionArn: str
    ImageVersionStatus: ImageVersionStatusType
    LastModifiedTime: datetime
    Version: int
    VendorGuidance: VendorGuidanceType
    JobType: JobTypeType
    MLFramework: str
    ProgrammingLang: str
    Processor: ProcessorType
    Horovod: bool
    ReleaseNotes: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribePipelineDefinitionForExecutionResponseTypeDef(TypedDict):
    PipelineDefinition: str
    CreationTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeStudioLifecycleConfigResponseTypeDef(TypedDict):
    StudioLifecycleConfigArn: str
    StudioLifecycleConfigName: str
    CreationTime: datetime
    LastModifiedTime: datetime
    StudioLifecycleConfigContent: str
    StudioLifecycleConfigAppType: StudioLifecycleConfigAppTypeType
    ResponseMetadata: ResponseMetadataTypeDef


class DisassociateTrialComponentResponseTypeDef(TypedDict):
    TrialComponentArn: str
    TrialArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef


class GetLineageGroupPolicyResponseTypeDef(TypedDict):
    LineageGroupArn: str
    ResourcePolicy: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetModelPackageGroupPolicyOutputTypeDef(TypedDict):
    ResourcePolicy: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetSagemakerServicecatalogPortfolioStatusOutputTypeDef(TypedDict):
    Status: SagemakerServicecatalogStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class ImportHubContentResponseTypeDef(TypedDict):
    HubArn: str
    HubContentArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListAliasesResponseTypeDef(TypedDict):
    SageMakerImageVersionAliases: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class PutModelPackageGroupPolicyOutputTypeDef(TypedDict):
    ModelPackageGroupArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class RetryPipelineExecutionResponseTypeDef(TypedDict):
    PipelineExecutionArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class SendPipelineExecutionStepFailureResponseTypeDef(TypedDict):
    PipelineExecutionArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class SendPipelineExecutionStepSuccessResponseTypeDef(TypedDict):
    PipelineExecutionArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class StartInferenceExperimentResponseTypeDef(TypedDict):
    InferenceExperimentArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class StartMlflowTrackingServerResponseTypeDef(TypedDict):
    TrackingServerArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class StartPipelineExecutionResponseTypeDef(TypedDict):
    PipelineExecutionArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class StopInferenceExperimentResponseTypeDef(TypedDict):
    InferenceExperimentArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class StopMlflowTrackingServerResponseTypeDef(TypedDict):
    TrackingServerArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class StopPipelineExecutionResponseTypeDef(TypedDict):
    PipelineExecutionArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateActionResponseTypeDef(TypedDict):
    ActionArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateAppImageConfigResponseTypeDef(TypedDict):
    AppImageConfigArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateArtifactResponseTypeDef(TypedDict):
    ArtifactArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateClusterResponseTypeDef(TypedDict):
    ClusterArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateClusterSoftwareResponseTypeDef(TypedDict):
    ClusterArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateCodeRepositoryOutputTypeDef(TypedDict):
    CodeRepositoryArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateContextResponseTypeDef(TypedDict):
    ContextArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateDomainResponseTypeDef(TypedDict):
    DomainArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateEndpointOutputTypeDef(TypedDict):
    EndpointArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateEndpointWeightsAndCapacitiesOutputTypeDef(TypedDict):
    EndpointArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateExperimentResponseTypeDef(TypedDict):
    ExperimentArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateFeatureGroupResponseTypeDef(TypedDict):
    FeatureGroupArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateHubResponseTypeDef(TypedDict):
    HubArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateImageResponseTypeDef(TypedDict):
    ImageArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateImageVersionResponseTypeDef(TypedDict):
    ImageVersionArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateInferenceComponentOutputTypeDef(TypedDict):
    InferenceComponentArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateInferenceComponentRuntimeConfigOutputTypeDef(TypedDict):
    InferenceComponentArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateInferenceExperimentResponseTypeDef(TypedDict):
    InferenceExperimentArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateMlflowTrackingServerResponseTypeDef(TypedDict):
    TrackingServerArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateModelCardResponseTypeDef(TypedDict):
    ModelCardArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateModelPackageOutputTypeDef(TypedDict):
    ModelPackageArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateMonitoringAlertResponseTypeDef(TypedDict):
    MonitoringScheduleArn: str
    MonitoringAlertName: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateMonitoringScheduleResponseTypeDef(TypedDict):
    MonitoringScheduleArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdatePipelineExecutionResponseTypeDef(TypedDict):
    PipelineExecutionArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdatePipelineResponseTypeDef(TypedDict):
    PipelineArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateProjectOutputTypeDef(TypedDict):
    ProjectArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateSpaceResponseTypeDef(TypedDict):
    SpaceArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateTrainingJobResponseTypeDef(TypedDict):
    TrainingJobArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateTrialComponentResponseTypeDef(TypedDict):
    TrialComponentArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateTrialResponseTypeDef(TypedDict):
    TrialArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateUserProfileResponseTypeDef(TypedDict):
    UserProfileArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class AddTagsInputRequestTypeDef(TypedDict):
    ResourceArn: str
    Tags: Sequence[TagTypeDef]


class AddTagsOutputTypeDef(TypedDict):
    Tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateExperimentRequestRequestTypeDef(TypedDict):
    ExperimentName: str
    DisplayName: NotRequired[str]
    Description: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateHubContentReferenceRequestRequestTypeDef(TypedDict):
    HubName: str
    SageMakerPublicHubContentArn: str
    HubContentName: NotRequired[str]
    MinVersion: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateImageRequestRequestTypeDef(TypedDict):
    ImageName: str
    RoleArn: str
    Description: NotRequired[str]
    DisplayName: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateMlflowTrackingServerRequestRequestTypeDef(TypedDict):
    TrackingServerName: str
    ArtifactStoreUri: str
    RoleArn: str
    TrackingServerSize: NotRequired[TrackingServerSizeType]
    MlflowVersion: NotRequired[str]
    AutomaticModelRegistration: NotRequired[bool]
    WeeklyMaintenanceWindowStart: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateModelPackageGroupInputRequestTypeDef(TypedDict):
    ModelPackageGroupName: str
    ModelPackageGroupDescription: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateStudioLifecycleConfigRequestRequestTypeDef(TypedDict):
    StudioLifecycleConfigName: str
    StudioLifecycleConfigContent: str
    StudioLifecycleConfigAppType: StudioLifecycleConfigAppTypeType
    Tags: NotRequired[Sequence[TagTypeDef]]


class ImportHubContentRequestRequestTypeDef(TypedDict):
    HubContentName: str
    HubContentType: HubContentTypeType
    DocumentSchemaVersion: str
    HubName: str
    HubContentDocument: str
    HubContentVersion: NotRequired[str]
    HubContentDisplayName: NotRequired[str]
    HubContentDescription: NotRequired[str]
    HubContentMarkdown: NotRequired[str]
    HubContentSearchKeywords: NotRequired[Sequence[str]]
    Tags: NotRequired[Sequence[TagTypeDef]]


class ListTagsOutputTypeDef(TypedDict):
    Tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class AutoRollbackConfigOutputTypeDef(TypedDict):
    Alarms: NotRequired[List[AlarmTypeDef]]


class AutoRollbackConfigTypeDef(TypedDict):
    Alarms: NotRequired[Sequence[AlarmTypeDef]]


class HyperParameterAlgorithmSpecificationOutputTypeDef(TypedDict):
    TrainingInputMode: TrainingInputModeType
    TrainingImage: NotRequired[str]
    AlgorithmName: NotRequired[str]
    MetricDefinitions: NotRequired[List[MetricDefinitionTypeDef]]


class HyperParameterAlgorithmSpecificationTypeDef(TypedDict):
    TrainingInputMode: TrainingInputModeType
    TrainingImage: NotRequired[str]
    AlgorithmName: NotRequired[str]
    MetricDefinitions: NotRequired[Sequence[MetricDefinitionTypeDef]]


class AlgorithmStatusDetailsTypeDef(TypedDict):
    ValidationStatuses: NotRequired[List[AlgorithmStatusItemTypeDef]]
    ImageScanStatuses: NotRequired[List[AlgorithmStatusItemTypeDef]]


class ListAlgorithmsOutputTypeDef(TypedDict):
    AlgorithmSummaryList: List[AlgorithmSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class AppDetailsTypeDef(TypedDict):
    DomainId: NotRequired[str]
    UserProfileName: NotRequired[str]
    SpaceName: NotRequired[str]
    AppType: NotRequired[AppTypeType]
    AppName: NotRequired[str]
    Status: NotRequired[AppStatusType]
    CreationTime: NotRequired[datetime]
    ResourceSpec: NotRequired[ResourceSpecTypeDef]


class CreateAppRequestRequestTypeDef(TypedDict):
    DomainId: str
    AppType: AppTypeType
    AppName: str
    UserProfileName: NotRequired[str]
    SpaceName: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]
    ResourceSpec: NotRequired[ResourceSpecTypeDef]


class DescribeAppResponseTypeDef(TypedDict):
    AppArn: str
    AppType: AppTypeType
    AppName: str
    DomainId: str
    UserProfileName: str
    SpaceName: str
    Status: AppStatusType
    LastHealthCheckTimestamp: datetime
    LastUserActivityTimestamp: datetime
    CreationTime: datetime
    FailureReason: str
    ResourceSpec: ResourceSpecTypeDef
    BuiltInLifecycleConfigArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class RStudioServerProDomainSettingsForUpdateTypeDef(TypedDict):
    DomainExecutionRoleArn: str
    DefaultResourceSpec: NotRequired[ResourceSpecTypeDef]
    RStudioConnectUrl: NotRequired[str]
    RStudioPackageManagerUrl: NotRequired[str]


class RStudioServerProDomainSettingsTypeDef(TypedDict):
    DomainExecutionRoleArn: str
    RStudioConnectUrl: NotRequired[str]
    RStudioPackageManagerUrl: NotRequired[str]
    DefaultResourceSpec: NotRequired[ResourceSpecTypeDef]


class TensorBoardAppSettingsTypeDef(TypedDict):
    DefaultResourceSpec: NotRequired[ResourceSpecTypeDef]


class AppLifecycleManagementTypeDef(TypedDict):
    IdleSettings: NotRequired[IdleSettingsTypeDef]


class ArtifactSourceOutputTypeDef(TypedDict):
    SourceUri: str
    SourceTypes: NotRequired[List[ArtifactSourceTypeTypeDef]]


class ArtifactSourceTypeDef(TypedDict):
    SourceUri: str
    SourceTypes: NotRequired[Sequence[ArtifactSourceTypeTypeDef]]


class AsyncInferenceOutputConfigOutputTypeDef(TypedDict):
    KmsKeyId: NotRequired[str]
    S3OutputPath: NotRequired[str]
    NotificationConfig: NotRequired[AsyncInferenceNotificationConfigOutputTypeDef]
    S3FailurePath: NotRequired[str]


AsyncInferenceNotificationConfigUnionTypeDef = Union[
    AsyncInferenceNotificationConfigTypeDef, AsyncInferenceNotificationConfigOutputTypeDef
]


class AutoMLCandidateGenerationConfigOutputTypeDef(TypedDict):
    FeatureSpecificationS3Uri: NotRequired[str]
    AlgorithmsConfig: NotRequired[List[AutoMLAlgorithmConfigOutputTypeDef]]


class CandidateGenerationConfigOutputTypeDef(TypedDict):
    AlgorithmsConfig: NotRequired[List[AutoMLAlgorithmConfigOutputTypeDef]]


AutoMLAlgorithmConfigUnionTypeDef = Union[
    AutoMLAlgorithmConfigTypeDef, AutoMLAlgorithmConfigOutputTypeDef
]


class AutoMLComputeConfigTypeDef(TypedDict):
    EmrServerlessComputeConfig: NotRequired[EmrServerlessComputeConfigTypeDef]


class AutoMLDataSourceTypeDef(TypedDict):
    S3DataSource: AutoMLS3DataSourceTypeDef


class ImageClassificationJobConfigTypeDef(TypedDict):
    CompletionCriteria: NotRequired[AutoMLJobCompletionCriteriaTypeDef]


class TextClassificationJobConfigTypeDef(TypedDict):
    ContentColumn: str
    TargetLabelColumn: str
    CompletionCriteria: NotRequired[AutoMLJobCompletionCriteriaTypeDef]


class ResolvedAttributesTypeDef(TypedDict):
    AutoMLJobObjective: NotRequired[AutoMLJobObjectiveTypeDef]
    ProblemType: NotRequired[ProblemTypeType]
    CompletionCriteria: NotRequired[AutoMLJobCompletionCriteriaTypeDef]


class AutoMLJobSummaryTypeDef(TypedDict):
    AutoMLJobName: str
    AutoMLJobArn: str
    AutoMLJobStatus: AutoMLJobStatusType
    AutoMLJobSecondaryStatus: AutoMLJobSecondaryStatusType
    CreationTime: datetime
    LastModifiedTime: datetime
    EndTime: NotRequired[datetime]
    FailureReason: NotRequired[str]
    PartialFailureReasons: NotRequired[List[AutoMLPartialFailureReasonTypeDef]]


class AutoMLProblemTypeResolvedAttributesTypeDef(TypedDict):
    TabularResolvedAttributes: NotRequired[TabularResolvedAttributesTypeDef]
    TextGenerationResolvedAttributes: NotRequired[TextGenerationResolvedAttributesTypeDef]


class AutoMLSecurityConfigOutputTypeDef(TypedDict):
    VolumeKmsKeyId: NotRequired[str]
    EnableInterContainerTrafficEncryption: NotRequired[bool]
    VpcConfig: NotRequired[VpcConfigOutputTypeDef]


class LabelingJobResourceConfigOutputTypeDef(TypedDict):
    VolumeKmsKeyId: NotRequired[str]
    VpcConfig: NotRequired[VpcConfigOutputTypeDef]


class MonitoringNetworkConfigOutputTypeDef(TypedDict):
    EnableInterContainerTrafficEncryption: NotRequired[bool]
    EnableNetworkIsolation: NotRequired[bool]
    VpcConfig: NotRequired[VpcConfigOutputTypeDef]


class NetworkConfigOutputTypeDef(TypedDict):
    EnableInterContainerTrafficEncryption: NotRequired[bool]
    EnableNetworkIsolation: NotRequired[bool]
    VpcConfig: NotRequired[VpcConfigOutputTypeDef]


class BatchDeleteClusterNodesResponseTypeDef(TypedDict):
    Failed: List[BatchDeleteClusterNodesErrorTypeDef]
    Successful: List[str]
    ResponseMetadata: ResponseMetadataTypeDef


class BiasTypeDef(TypedDict):
    Report: NotRequired[MetricsSourceTypeDef]
    PreTrainingReport: NotRequired[MetricsSourceTypeDef]
    PostTrainingReport: NotRequired[MetricsSourceTypeDef]


class DriftCheckModelDataQualityTypeDef(TypedDict):
    Statistics: NotRequired[MetricsSourceTypeDef]
    Constraints: NotRequired[MetricsSourceTypeDef]


class DriftCheckModelQualityTypeDef(TypedDict):
    Statistics: NotRequired[MetricsSourceTypeDef]
    Constraints: NotRequired[MetricsSourceTypeDef]


class ExplainabilityTypeDef(TypedDict):
    Report: NotRequired[MetricsSourceTypeDef]


class ModelDataQualityTypeDef(TypedDict):
    Statistics: NotRequired[MetricsSourceTypeDef]
    Constraints: NotRequired[MetricsSourceTypeDef]


class ModelQualityTypeDef(TypedDict):
    Statistics: NotRequired[MetricsSourceTypeDef]
    Constraints: NotRequired[MetricsSourceTypeDef]


class CallbackStepMetadataTypeDef(TypedDict):
    CallbackToken: NotRequired[str]
    SqsQueueUrl: NotRequired[str]
    OutputParameters: NotRequired[List[OutputParameterTypeDef]]


class LambdaStepMetadataTypeDef(TypedDict):
    Arn: NotRequired[str]
    OutputParameters: NotRequired[List[OutputParameterTypeDef]]


class SendPipelineExecutionStepSuccessRequestRequestTypeDef(TypedDict):
    CallbackToken: str
    OutputParameters: NotRequired[Sequence[OutputParameterTypeDef]]
    ClientRequestToken: NotRequired[str]


class CandidatePropertiesTypeDef(TypedDict):
    CandidateArtifactLocations: NotRequired[CandidateArtifactLocationsTypeDef]
    CandidateMetrics: NotRequired[List[MetricDatumTypeDef]]


class CanvasAppSettingsOutputTypeDef(TypedDict):
    TimeSeriesForecastingSettings: NotRequired[TimeSeriesForecastingSettingsTypeDef]
    ModelRegisterSettings: NotRequired[ModelRegisterSettingsTypeDef]
    WorkspaceSettings: NotRequired[WorkspaceSettingsTypeDef]
    IdentityProviderOAuthSettings: NotRequired[List[IdentityProviderOAuthSettingTypeDef]]
    DirectDeploySettings: NotRequired[DirectDeploySettingsTypeDef]
    KendraSettings: NotRequired[KendraSettingsTypeDef]
    GenerativeAiSettings: NotRequired[GenerativeAiSettingsTypeDef]
    EmrServerlessSettings: NotRequired[EmrServerlessSettingsTypeDef]


class CanvasAppSettingsTypeDef(TypedDict):
    TimeSeriesForecastingSettings: NotRequired[TimeSeriesForecastingSettingsTypeDef]
    ModelRegisterSettings: NotRequired[ModelRegisterSettingsTypeDef]
    WorkspaceSettings: NotRequired[WorkspaceSettingsTypeDef]
    IdentityProviderOAuthSettings: NotRequired[Sequence[IdentityProviderOAuthSettingTypeDef]]
    DirectDeploySettings: NotRequired[DirectDeploySettingsTypeDef]
    KendraSettings: NotRequired[KendraSettingsTypeDef]
    GenerativeAiSettings: NotRequired[GenerativeAiSettingsTypeDef]
    EmrServerlessSettings: NotRequired[EmrServerlessSettingsTypeDef]


class RollingUpdatePolicyTypeDef(TypedDict):
    MaximumBatchSize: CapacitySizeTypeDef
    WaitIntervalInSeconds: int
    MaximumExecutionTimeoutInSeconds: NotRequired[int]
    RollbackMaximumBatchSize: NotRequired[CapacitySizeTypeDef]


TrafficRoutingConfigTypeDef = TypedDict(
    "TrafficRoutingConfigTypeDef",
    {
        "Type": TrafficRoutingConfigTypeType,
        "WaitIntervalInSeconds": int,
        "CanarySize": NotRequired[CapacitySizeTypeDef],
        "LinearStepSize": NotRequired[CapacitySizeTypeDef],
    },
)


class InferenceExperimentDataStorageConfigOutputTypeDef(TypedDict):
    Destination: str
    KmsKey: NotRequired[str]
    ContentType: NotRequired[CaptureContentTypeHeaderOutputTypeDef]


CaptureContentTypeHeaderUnionTypeDef = Union[
    CaptureContentTypeHeaderTypeDef, CaptureContentTypeHeaderOutputTypeDef
]


class DataCaptureConfigOutputTypeDef(TypedDict):
    InitialSamplingPercentage: int
    DestinationS3Uri: str
    CaptureOptions: List[CaptureOptionTypeDef]
    EnableCapture: NotRequired[bool]
    KmsKeyId: NotRequired[str]
    CaptureContentTypeHeader: NotRequired[CaptureContentTypeHeaderOutputTypeDef]


class EnvironmentParameterRangesOutputTypeDef(TypedDict):
    CategoricalParameterRanges: NotRequired[List[CategoricalParameterOutputTypeDef]]


CategoricalParameterRangeSpecificationUnionTypeDef = Union[
    CategoricalParameterRangeSpecificationTypeDef,
    CategoricalParameterRangeSpecificationOutputTypeDef,
]
CategoricalParameterRangeUnionTypeDef = Union[
    CategoricalParameterRangeTypeDef, CategoricalParameterRangeOutputTypeDef
]
CategoricalParameterUnionTypeDef = Union[
    CategoricalParameterTypeDef, CategoricalParameterOutputTypeDef
]
ChannelSpecificationUnionTypeDef = Union[
    ChannelSpecificationTypeDef, ChannelSpecificationOutputTypeDef
]
ClarifyInferenceConfigUnionTypeDef = Union[
    ClarifyInferenceConfigTypeDef, ClarifyInferenceConfigOutputTypeDef
]


class ClarifyShapConfigTypeDef(TypedDict):
    ShapBaselineConfig: ClarifyShapBaselineConfigTypeDef
    NumberOfSamples: NotRequired[int]
    UseLogit: NotRequired[bool]
    Seed: NotRequired[int]
    TextConfig: NotRequired[ClarifyTextConfigTypeDef]


class ClusterInstanceStorageConfigTypeDef(TypedDict):
    EbsVolumeConfig: NotRequired[ClusterEbsVolumeConfigTypeDef]


class ClusterNodeSummaryTypeDef(TypedDict):
    InstanceGroupName: str
    InstanceId: str
    InstanceType: ClusterInstanceTypeType
    LaunchTime: datetime
    InstanceStatus: ClusterInstanceStatusDetailsTypeDef


class ClusterOrchestratorTypeDef(TypedDict):
    Eks: ClusterOrchestratorEksConfigTypeDef


class ListClustersResponseTypeDef(TypedDict):
    NextToken: str
    ClusterSummaries: List[ClusterSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CodeEditorAppImageConfigOutputTypeDef(TypedDict):
    FileSystemConfig: NotRequired[FileSystemConfigTypeDef]
    ContainerConfig: NotRequired[ContainerConfigOutputTypeDef]


class JupyterLabAppImageConfigOutputTypeDef(TypedDict):
    FileSystemConfig: NotRequired[FileSystemConfigTypeDef]
    ContainerConfig: NotRequired[ContainerConfigOutputTypeDef]


class KernelGatewayAppSettingsOutputTypeDef(TypedDict):
    DefaultResourceSpec: NotRequired[ResourceSpecTypeDef]
    CustomImages: NotRequired[List[CustomImageTypeDef]]
    LifecycleConfigArns: NotRequired[List[str]]


class KernelGatewayAppSettingsTypeDef(TypedDict):
    DefaultResourceSpec: NotRequired[ResourceSpecTypeDef]
    CustomImages: NotRequired[Sequence[CustomImageTypeDef]]
    LifecycleConfigArns: NotRequired[Sequence[str]]


class RSessionAppSettingsOutputTypeDef(TypedDict):
    DefaultResourceSpec: NotRequired[ResourceSpecTypeDef]
    CustomImages: NotRequired[List[CustomImageTypeDef]]


class RSessionAppSettingsTypeDef(TypedDict):
    DefaultResourceSpec: NotRequired[ResourceSpecTypeDef]
    CustomImages: NotRequired[Sequence[CustomImageTypeDef]]


class CodeRepositorySummaryTypeDef(TypedDict):
    CodeRepositoryName: str
    CodeRepositoryArn: str
    CreationTime: datetime
    LastModifiedTime: datetime
    GitConfig: NotRequired[GitConfigTypeDef]


class CreateCodeRepositoryInputRequestTypeDef(TypedDict):
    CodeRepositoryName: str
    GitConfig: GitConfigTypeDef
    Tags: NotRequired[Sequence[TagTypeDef]]


class DescribeCodeRepositoryOutputTypeDef(TypedDict):
    CodeRepositoryName: str
    CodeRepositoryArn: str
    CreationTime: datetime
    LastModifiedTime: datetime
    GitConfig: GitConfigTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class JupyterServerAppSettingsOutputTypeDef(TypedDict):
    DefaultResourceSpec: NotRequired[ResourceSpecTypeDef]
    LifecycleConfigArns: NotRequired[List[str]]
    CodeRepositories: NotRequired[List[CodeRepositoryTypeDef]]


class JupyterServerAppSettingsTypeDef(TypedDict):
    DefaultResourceSpec: NotRequired[ResourceSpecTypeDef]
    LifecycleConfigArns: NotRequired[Sequence[str]]
    CodeRepositories: NotRequired[Sequence[CodeRepositoryTypeDef]]


class CollectionConfigTypeDef(TypedDict):
    VectorConfig: NotRequired[VectorConfigTypeDef]


class DebugHookConfigOutputTypeDef(TypedDict):
    S3OutputPath: str
    LocalPath: NotRequired[str]
    HookParameters: NotRequired[Dict[str, str]]
    CollectionConfigurations: NotRequired[List[CollectionConfigurationOutputTypeDef]]


CollectionConfigurationUnionTypeDef = Union[
    CollectionConfigurationTypeDef, CollectionConfigurationOutputTypeDef
]


class ListCompilationJobsResponseTypeDef(TypedDict):
    CompilationJobSummaries: List[CompilationJobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


ContainerConfigUnionTypeDef = Union[ContainerConfigTypeDef, ContainerConfigOutputTypeDef]


class ContextSummaryTypeDef(TypedDict):
    ContextArn: NotRequired[str]
    ContextName: NotRequired[str]
    Source: NotRequired[ContextSourceTypeDef]
    ContextType: NotRequired[str]
    CreationTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]


class CreateContextRequestRequestTypeDef(TypedDict):
    ContextName: str
    Source: ContextSourceTypeDef
    ContextType: str
    Description: NotRequired[str]
    Properties: NotRequired[Mapping[str, str]]
    Tags: NotRequired[Sequence[TagTypeDef]]


class TuningJobCompletionCriteriaTypeDef(TypedDict):
    TargetObjectiveMetricValue: NotRequired[float]
    BestObjectiveNotImproving: NotRequired[BestObjectiveNotImprovingTypeDef]
    ConvergenceDetected: NotRequired[ConvergenceDetectedTypeDef]


class CreateActionRequestRequestTypeDef(TypedDict):
    ActionName: str
    Source: ActionSourceTypeDef
    ActionType: str
    Description: NotRequired[str]
    Status: NotRequired[ActionStatusType]
    Properties: NotRequired[Mapping[str, str]]
    MetadataProperties: NotRequired[MetadataPropertiesTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateTrialRequestRequestTypeDef(TypedDict):
    TrialName: str
    ExperimentName: str
    DisplayName: NotRequired[str]
    MetadataProperties: NotRequired[MetadataPropertiesTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]


VpcConfigUnionTypeDef = Union[VpcConfigTypeDef, VpcConfigOutputTypeDef]


class CreateDeviceFleetRequestRequestTypeDef(TypedDict):
    DeviceFleetName: str
    OutputConfig: EdgeOutputConfigTypeDef
    RoleArn: NotRequired[str]
    Description: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]
    EnableIotRoleAlias: NotRequired[bool]


class CreateEdgePackagingJobRequestRequestTypeDef(TypedDict):
    EdgePackagingJobName: str
    CompilationJobName: str
    ModelName: str
    ModelVersion: str
    RoleArn: str
    OutputConfig: EdgeOutputConfigTypeDef
    ResourceKey: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]


class DescribeDeviceFleetResponseTypeDef(TypedDict):
    DeviceFleetName: str
    DeviceFleetArn: str
    OutputConfig: EdgeOutputConfigTypeDef
    Description: str
    CreationTime: datetime
    LastModifiedTime: datetime
    RoleArn: str
    IotRoleAlias: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateDeviceFleetRequestRequestTypeDef(TypedDict):
    DeviceFleetName: str
    OutputConfig: EdgeOutputConfigTypeDef
    RoleArn: NotRequired[str]
    Description: NotRequired[str]
    EnableIotRoleAlias: NotRequired[bool]


class CreateHubRequestRequestTypeDef(TypedDict):
    HubName: str
    HubDescription: str
    HubDisplayName: NotRequired[str]
    HubSearchKeywords: NotRequired[Sequence[str]]
    S3StorageConfig: NotRequired[HubS3StorageConfigTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]


class DescribeHubResponseTypeDef(TypedDict):
    HubName: str
    HubArn: str
    HubDisplayName: str
    HubDescription: str
    HubSearchKeywords: List[str]
    S3StorageConfig: HubS3StorageConfigTypeDef
    HubStatus: HubStatusType
    FailureReason: str
    CreationTime: datetime
    LastModifiedTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class CreateHumanTaskUiRequestRequestTypeDef(TypedDict):
    HumanTaskUiName: str
    UiTemplate: UiTemplateTypeDef
    Tags: NotRequired[Sequence[TagTypeDef]]


class UpdateInferenceComponentRuntimeConfigInputRequestTypeDef(TypedDict):
    InferenceComponentName: str
    DesiredRuntimeConfig: InferenceComponentRuntimeConfigTypeDef


class CreateModelCardExportJobRequestRequestTypeDef(TypedDict):
    ModelCardName: str
    ModelCardExportJobName: str
    OutputConfig: ModelCardExportOutputConfigTypeDef
    ModelCardVersion: NotRequired[int]


class CreateModelCardRequestRequestTypeDef(TypedDict):
    ModelCardName: str
    Content: str
    ModelCardStatus: ModelCardStatusType
    SecurityConfig: NotRequired[ModelCardSecurityConfigTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateNotebookInstanceInputRequestTypeDef(TypedDict):
    NotebookInstanceName: str
    InstanceType: InstanceTypeType
    RoleArn: str
    SubnetId: NotRequired[str]
    SecurityGroupIds: NotRequired[Sequence[str]]
    KmsKeyId: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]
    LifecycleConfigName: NotRequired[str]
    DirectInternetAccess: NotRequired[DirectInternetAccessType]
    VolumeSizeInGB: NotRequired[int]
    AcceleratorTypes: NotRequired[Sequence[NotebookInstanceAcceleratorTypeType]]
    DefaultCodeRepository: NotRequired[str]
    AdditionalCodeRepositories: NotRequired[Sequence[str]]
    RootAccess: NotRequired[RootAccessType]
    PlatformIdentifier: NotRequired[str]
    InstanceMetadataServiceConfiguration: NotRequired[InstanceMetadataServiceConfigurationTypeDef]


class DescribeNotebookInstanceOutputTypeDef(TypedDict):
    NotebookInstanceArn: str
    NotebookInstanceName: str
    NotebookInstanceStatus: NotebookInstanceStatusType
    FailureReason: str
    Url: str
    InstanceType: InstanceTypeType
    SubnetId: str
    SecurityGroups: List[str]
    RoleArn: str
    KmsKeyId: str
    NetworkInterfaceId: str
    LastModifiedTime: datetime
    CreationTime: datetime
    NotebookInstanceLifecycleConfigName: str
    DirectInternetAccess: DirectInternetAccessType
    VolumeSizeInGB: int
    AcceleratorTypes: List[NotebookInstanceAcceleratorTypeType]
    DefaultCodeRepository: str
    AdditionalCodeRepositories: List[str]
    RootAccess: RootAccessType
    PlatformIdentifier: str
    InstanceMetadataServiceConfiguration: InstanceMetadataServiceConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateNotebookInstanceInputRequestTypeDef(TypedDict):
    NotebookInstanceName: str
    InstanceType: NotRequired[InstanceTypeType]
    RoleArn: NotRequired[str]
    LifecycleConfigName: NotRequired[str]
    DisassociateLifecycleConfig: NotRequired[bool]
    VolumeSizeInGB: NotRequired[int]
    DefaultCodeRepository: NotRequired[str]
    AdditionalCodeRepositories: NotRequired[Sequence[str]]
    AcceleratorTypes: NotRequired[Sequence[NotebookInstanceAcceleratorTypeType]]
    DisassociateAcceleratorTypes: NotRequired[bool]
    DisassociateDefaultCodeRepository: NotRequired[bool]
    DisassociateAdditionalCodeRepositories: NotRequired[bool]
    RootAccess: NotRequired[RootAccessType]
    InstanceMetadataServiceConfiguration: NotRequired[InstanceMetadataServiceConfigurationTypeDef]


class CreateNotebookInstanceLifecycleConfigInputRequestTypeDef(TypedDict):
    NotebookInstanceLifecycleConfigName: str
    OnCreate: NotRequired[Sequence[NotebookInstanceLifecycleHookTypeDef]]
    OnStart: NotRequired[Sequence[NotebookInstanceLifecycleHookTypeDef]]


class DescribeNotebookInstanceLifecycleConfigOutputTypeDef(TypedDict):
    NotebookInstanceLifecycleConfigArn: str
    NotebookInstanceLifecycleConfigName: str
    OnCreate: List[NotebookInstanceLifecycleHookTypeDef]
    OnStart: List[NotebookInstanceLifecycleHookTypeDef]
    LastModifiedTime: datetime
    CreationTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateNotebookInstanceLifecycleConfigInputRequestTypeDef(TypedDict):
    NotebookInstanceLifecycleConfigName: str
    OnCreate: NotRequired[Sequence[NotebookInstanceLifecycleHookTypeDef]]
    OnStart: NotRequired[Sequence[NotebookInstanceLifecycleHookTypeDef]]


class RetryPipelineExecutionRequestRequestTypeDef(TypedDict):
    PipelineExecutionArn: str
    ClientRequestToken: str
    ParallelismConfiguration: NotRequired[ParallelismConfigurationTypeDef]


class UpdatePipelineExecutionRequestRequestTypeDef(TypedDict):
    PipelineExecutionArn: str
    PipelineExecutionDescription: NotRequired[str]
    PipelineExecutionDisplayName: NotRequired[str]
    ParallelismConfiguration: NotRequired[ParallelismConfigurationTypeDef]


class CreatePipelineRequestRequestTypeDef(TypedDict):
    PipelineName: str
    ClientRequestToken: str
    RoleArn: str
    PipelineDisplayName: NotRequired[str]
    PipelineDefinition: NotRequired[str]
    PipelineDefinitionS3Location: NotRequired[PipelineDefinitionS3LocationTypeDef]
    PipelineDescription: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]
    ParallelismConfiguration: NotRequired[ParallelismConfigurationTypeDef]


class UpdatePipelineRequestRequestTypeDef(TypedDict):
    PipelineName: str
    PipelineDisplayName: NotRequired[str]
    PipelineDefinition: NotRequired[str]
    PipelineDefinitionS3Location: NotRequired[PipelineDefinitionS3LocationTypeDef]
    PipelineDescription: NotRequired[str]
    RoleArn: NotRequired[str]
    ParallelismConfiguration: NotRequired[ParallelismConfigurationTypeDef]


class InferenceExperimentScheduleTypeDef(TypedDict):
    StartTime: NotRequired[TimestampTypeDef]
    EndTime: NotRequired[TimestampTypeDef]


class ListActionsRequestRequestTypeDef(TypedDict):
    SourceUri: NotRequired[str]
    ActionType: NotRequired[str]
    CreatedAfter: NotRequired[TimestampTypeDef]
    CreatedBefore: NotRequired[TimestampTypeDef]
    SortBy: NotRequired[SortActionsByType]
    SortOrder: NotRequired[SortOrderType]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListAlgorithmsInputRequestTypeDef(TypedDict):
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    MaxResults: NotRequired[int]
    NameContains: NotRequired[str]
    NextToken: NotRequired[str]
    SortBy: NotRequired[AlgorithmSortByType]
    SortOrder: NotRequired[SortOrderType]


class ListAppImageConfigsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    NameContains: NotRequired[str]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    ModifiedTimeBefore: NotRequired[TimestampTypeDef]
    ModifiedTimeAfter: NotRequired[TimestampTypeDef]
    SortBy: NotRequired[AppImageConfigSortKeyType]
    SortOrder: NotRequired[SortOrderType]


class ListArtifactsRequestRequestTypeDef(TypedDict):
    SourceUri: NotRequired[str]
    ArtifactType: NotRequired[str]
    CreatedAfter: NotRequired[TimestampTypeDef]
    CreatedBefore: NotRequired[TimestampTypeDef]
    SortBy: NotRequired[Literal["CreationTime"]]
    SortOrder: NotRequired[SortOrderType]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListAssociationsRequestRequestTypeDef(TypedDict):
    SourceArn: NotRequired[str]
    DestinationArn: NotRequired[str]
    SourceType: NotRequired[str]
    DestinationType: NotRequired[str]
    AssociationType: NotRequired[AssociationEdgeTypeType]
    CreatedAfter: NotRequired[TimestampTypeDef]
    CreatedBefore: NotRequired[TimestampTypeDef]
    SortBy: NotRequired[SortAssociationsByType]
    SortOrder: NotRequired[SortOrderType]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListAutoMLJobsRequestRequestTypeDef(TypedDict):
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    NameContains: NotRequired[str]
    StatusEquals: NotRequired[AutoMLJobStatusType]
    SortOrder: NotRequired[AutoMLSortOrderType]
    SortBy: NotRequired[AutoMLSortByType]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListClusterNodesRequestRequestTypeDef(TypedDict):
    ClusterName: str
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    InstanceGroupNameContains: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    SortBy: NotRequired[ClusterSortByType]
    SortOrder: NotRequired[SortOrderType]


class ListClustersRequestRequestTypeDef(TypedDict):
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    MaxResults: NotRequired[int]
    NameContains: NotRequired[str]
    NextToken: NotRequired[str]
    SortBy: NotRequired[ClusterSortByType]
    SortOrder: NotRequired[SortOrderType]


class ListCodeRepositoriesInputRequestTypeDef(TypedDict):
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    MaxResults: NotRequired[int]
    NameContains: NotRequired[str]
    NextToken: NotRequired[str]
    SortBy: NotRequired[CodeRepositorySortByType]
    SortOrder: NotRequired[CodeRepositorySortOrderType]


class ListCompilationJobsRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    NameContains: NotRequired[str]
    StatusEquals: NotRequired[CompilationJobStatusType]
    SortBy: NotRequired[ListCompilationJobsSortByType]
    SortOrder: NotRequired[SortOrderType]


class ListContextsRequestRequestTypeDef(TypedDict):
    SourceUri: NotRequired[str]
    ContextType: NotRequired[str]
    CreatedAfter: NotRequired[TimestampTypeDef]
    CreatedBefore: NotRequired[TimestampTypeDef]
    SortBy: NotRequired[SortContextsByType]
    SortOrder: NotRequired[SortOrderType]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListDataQualityJobDefinitionsRequestRequestTypeDef(TypedDict):
    EndpointName: NotRequired[str]
    SortBy: NotRequired[MonitoringJobDefinitionSortKeyType]
    SortOrder: NotRequired[SortOrderType]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    NameContains: NotRequired[str]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    CreationTimeAfter: NotRequired[TimestampTypeDef]


class ListDeviceFleetsRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    NameContains: NotRequired[str]
    SortBy: NotRequired[ListDeviceFleetsSortByType]
    SortOrder: NotRequired[SortOrderType]


class ListDevicesRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    LatestHeartbeatAfter: NotRequired[TimestampTypeDef]
    ModelName: NotRequired[str]
    DeviceFleetName: NotRequired[str]


class ListEdgeDeploymentPlansRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    NameContains: NotRequired[str]
    DeviceFleetNameContains: NotRequired[str]
    SortBy: NotRequired[ListEdgeDeploymentPlansSortByType]
    SortOrder: NotRequired[SortOrderType]


class ListEdgePackagingJobsRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    NameContains: NotRequired[str]
    ModelNameContains: NotRequired[str]
    StatusEquals: NotRequired[EdgePackagingJobStatusType]
    SortBy: NotRequired[ListEdgePackagingJobsSortByType]
    SortOrder: NotRequired[SortOrderType]


class ListEndpointConfigsInputRequestTypeDef(TypedDict):
    SortBy: NotRequired[EndpointConfigSortKeyType]
    SortOrder: NotRequired[OrderKeyType]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    NameContains: NotRequired[str]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    CreationTimeAfter: NotRequired[TimestampTypeDef]


class ListEndpointsInputRequestTypeDef(TypedDict):
    SortBy: NotRequired[EndpointSortKeyType]
    SortOrder: NotRequired[OrderKeyType]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    NameContains: NotRequired[str]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    StatusEquals: NotRequired[EndpointStatusType]


class ListExperimentsRequestRequestTypeDef(TypedDict):
    CreatedAfter: NotRequired[TimestampTypeDef]
    CreatedBefore: NotRequired[TimestampTypeDef]
    SortBy: NotRequired[SortExperimentsByType]
    SortOrder: NotRequired[SortOrderType]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListFeatureGroupsRequestRequestTypeDef(TypedDict):
    NameContains: NotRequired[str]
    FeatureGroupStatusEquals: NotRequired[FeatureGroupStatusType]
    OfflineStoreStatusEquals: NotRequired[OfflineStoreStatusValueType]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    SortOrder: NotRequired[FeatureGroupSortOrderType]
    SortBy: NotRequired[FeatureGroupSortByType]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListFlowDefinitionsRequestRequestTypeDef(TypedDict):
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    SortOrder: NotRequired[SortOrderType]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListHubContentVersionsRequestRequestTypeDef(TypedDict):
    HubName: str
    HubContentType: HubContentTypeType
    HubContentName: str
    MinVersion: NotRequired[str]
    MaxSchemaVersion: NotRequired[str]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    SortBy: NotRequired[HubContentSortByType]
    SortOrder: NotRequired[SortOrderType]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListHubContentsRequestRequestTypeDef(TypedDict):
    HubName: str
    HubContentType: HubContentTypeType
    NameContains: NotRequired[str]
    MaxSchemaVersion: NotRequired[str]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    SortBy: NotRequired[HubContentSortByType]
    SortOrder: NotRequired[SortOrderType]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListHubsRequestRequestTypeDef(TypedDict):
    NameContains: NotRequired[str]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    SortBy: NotRequired[HubSortByType]
    SortOrder: NotRequired[SortOrderType]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListHumanTaskUisRequestRequestTypeDef(TypedDict):
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    SortOrder: NotRequired[SortOrderType]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListHyperParameterTuningJobsRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    SortBy: NotRequired[HyperParameterTuningJobSortByOptionsType]
    SortOrder: NotRequired[SortOrderType]
    NameContains: NotRequired[str]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    StatusEquals: NotRequired[HyperParameterTuningJobStatusType]


class ListImageVersionsRequestRequestTypeDef(TypedDict):
    ImageName: str
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    SortBy: NotRequired[ImageVersionSortByType]
    SortOrder: NotRequired[ImageVersionSortOrderType]


class ListImagesRequestRequestTypeDef(TypedDict):
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    MaxResults: NotRequired[int]
    NameContains: NotRequired[str]
    NextToken: NotRequired[str]
    SortBy: NotRequired[ImageSortByType]
    SortOrder: NotRequired[ImageSortOrderType]


class ListInferenceComponentsInputRequestTypeDef(TypedDict):
    SortBy: NotRequired[InferenceComponentSortKeyType]
    SortOrder: NotRequired[OrderKeyType]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    NameContains: NotRequired[str]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    StatusEquals: NotRequired[InferenceComponentStatusType]
    EndpointNameEquals: NotRequired[str]
    VariantNameEquals: NotRequired[str]


ListInferenceExperimentsRequestRequestTypeDef = TypedDict(
    "ListInferenceExperimentsRequestRequestTypeDef",
    {
        "NameContains": NotRequired[str],
        "Type": NotRequired[Literal["ShadowMode"]],
        "StatusEquals": NotRequired[InferenceExperimentStatusType],
        "CreationTimeAfter": NotRequired[TimestampTypeDef],
        "CreationTimeBefore": NotRequired[TimestampTypeDef],
        "LastModifiedTimeAfter": NotRequired[TimestampTypeDef],
        "LastModifiedTimeBefore": NotRequired[TimestampTypeDef],
        "SortBy": NotRequired[SortInferenceExperimentsByType],
        "SortOrder": NotRequired[SortOrderType],
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)


class ListInferenceRecommendationsJobsRequestRequestTypeDef(TypedDict):
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    NameContains: NotRequired[str]
    StatusEquals: NotRequired[RecommendationJobStatusType]
    SortBy: NotRequired[ListInferenceRecommendationsJobsSortByType]
    SortOrder: NotRequired[SortOrderType]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    ModelNameEquals: NotRequired[str]
    ModelPackageVersionArnEquals: NotRequired[str]


class ListLabelingJobsForWorkteamRequestRequestTypeDef(TypedDict):
    WorkteamArn: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    JobReferenceCodeContains: NotRequired[str]
    SortBy: NotRequired[Literal["CreationTime"]]
    SortOrder: NotRequired[SortOrderType]


class ListLabelingJobsRequestRequestTypeDef(TypedDict):
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    NameContains: NotRequired[str]
    SortBy: NotRequired[SortByType]
    SortOrder: NotRequired[SortOrderType]
    StatusEquals: NotRequired[LabelingJobStatusType]


class ListLineageGroupsRequestRequestTypeDef(TypedDict):
    CreatedAfter: NotRequired[TimestampTypeDef]
    CreatedBefore: NotRequired[TimestampTypeDef]
    SortBy: NotRequired[SortLineageGroupsByType]
    SortOrder: NotRequired[SortOrderType]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListMlflowTrackingServersRequestRequestTypeDef(TypedDict):
    CreatedAfter: NotRequired[TimestampTypeDef]
    CreatedBefore: NotRequired[TimestampTypeDef]
    TrackingServerStatus: NotRequired[TrackingServerStatusType]
    MlflowVersion: NotRequired[str]
    SortBy: NotRequired[SortTrackingServerByType]
    SortOrder: NotRequired[SortOrderType]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListModelBiasJobDefinitionsRequestRequestTypeDef(TypedDict):
    EndpointName: NotRequired[str]
    SortBy: NotRequired[MonitoringJobDefinitionSortKeyType]
    SortOrder: NotRequired[SortOrderType]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    NameContains: NotRequired[str]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    CreationTimeAfter: NotRequired[TimestampTypeDef]


class ListModelCardExportJobsRequestRequestTypeDef(TypedDict):
    ModelCardName: str
    ModelCardVersion: NotRequired[int]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    ModelCardExportJobNameContains: NotRequired[str]
    StatusEquals: NotRequired[ModelCardExportJobStatusType]
    SortBy: NotRequired[ModelCardExportJobSortByType]
    SortOrder: NotRequired[ModelCardExportJobSortOrderType]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListModelCardVersionsRequestRequestTypeDef(TypedDict):
    ModelCardName: str
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    MaxResults: NotRequired[int]
    ModelCardStatus: NotRequired[ModelCardStatusType]
    NextToken: NotRequired[str]
    SortBy: NotRequired[Literal["Version"]]
    SortOrder: NotRequired[ModelCardSortOrderType]


class ListModelCardsRequestRequestTypeDef(TypedDict):
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    MaxResults: NotRequired[int]
    NameContains: NotRequired[str]
    ModelCardStatus: NotRequired[ModelCardStatusType]
    NextToken: NotRequired[str]
    SortBy: NotRequired[ModelCardSortByType]
    SortOrder: NotRequired[ModelCardSortOrderType]


class ListModelExplainabilityJobDefinitionsRequestRequestTypeDef(TypedDict):
    EndpointName: NotRequired[str]
    SortBy: NotRequired[MonitoringJobDefinitionSortKeyType]
    SortOrder: NotRequired[SortOrderType]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    NameContains: NotRequired[str]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    CreationTimeAfter: NotRequired[TimestampTypeDef]


class ListModelPackageGroupsInputRequestTypeDef(TypedDict):
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    MaxResults: NotRequired[int]
    NameContains: NotRequired[str]
    NextToken: NotRequired[str]
    SortBy: NotRequired[ModelPackageGroupSortByType]
    SortOrder: NotRequired[SortOrderType]
    CrossAccountFilterOption: NotRequired[CrossAccountFilterOptionType]


class ListModelPackagesInputRequestTypeDef(TypedDict):
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    MaxResults: NotRequired[int]
    NameContains: NotRequired[str]
    ModelApprovalStatus: NotRequired[ModelApprovalStatusType]
    ModelPackageGroupName: NotRequired[str]
    ModelPackageType: NotRequired[ModelPackageTypeType]
    NextToken: NotRequired[str]
    SortBy: NotRequired[ModelPackageSortByType]
    SortOrder: NotRequired[SortOrderType]


class ListModelQualityJobDefinitionsRequestRequestTypeDef(TypedDict):
    EndpointName: NotRequired[str]
    SortBy: NotRequired[MonitoringJobDefinitionSortKeyType]
    SortOrder: NotRequired[SortOrderType]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    NameContains: NotRequired[str]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    CreationTimeAfter: NotRequired[TimestampTypeDef]


class ListModelsInputRequestTypeDef(TypedDict):
    SortBy: NotRequired[ModelSortKeyType]
    SortOrder: NotRequired[OrderKeyType]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    NameContains: NotRequired[str]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    CreationTimeAfter: NotRequired[TimestampTypeDef]


class ListMonitoringAlertHistoryRequestRequestTypeDef(TypedDict):
    MonitoringScheduleName: NotRequired[str]
    MonitoringAlertName: NotRequired[str]
    SortBy: NotRequired[MonitoringAlertHistorySortKeyType]
    SortOrder: NotRequired[SortOrderType]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    StatusEquals: NotRequired[MonitoringAlertStatusType]


class ListMonitoringExecutionsRequestRequestTypeDef(TypedDict):
    MonitoringScheduleName: NotRequired[str]
    EndpointName: NotRequired[str]
    SortBy: NotRequired[MonitoringExecutionSortKeyType]
    SortOrder: NotRequired[SortOrderType]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    ScheduledTimeBefore: NotRequired[TimestampTypeDef]
    ScheduledTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    StatusEquals: NotRequired[ExecutionStatusType]
    MonitoringJobDefinitionName: NotRequired[str]
    MonitoringTypeEquals: NotRequired[MonitoringTypeType]


class ListMonitoringSchedulesRequestRequestTypeDef(TypedDict):
    EndpointName: NotRequired[str]
    SortBy: NotRequired[MonitoringScheduleSortKeyType]
    SortOrder: NotRequired[SortOrderType]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    NameContains: NotRequired[str]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    StatusEquals: NotRequired[ScheduleStatusType]
    MonitoringJobDefinitionName: NotRequired[str]
    MonitoringTypeEquals: NotRequired[MonitoringTypeType]


class ListNotebookInstanceLifecycleConfigsInputRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    SortBy: NotRequired[NotebookInstanceLifecycleConfigSortKeyType]
    SortOrder: NotRequired[NotebookInstanceLifecycleConfigSortOrderType]
    NameContains: NotRequired[str]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]


class ListNotebookInstancesInputRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    SortBy: NotRequired[NotebookInstanceSortKeyType]
    SortOrder: NotRequired[NotebookInstanceSortOrderType]
    NameContains: NotRequired[str]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    StatusEquals: NotRequired[NotebookInstanceStatusType]
    NotebookInstanceLifecycleConfigNameContains: NotRequired[str]
    DefaultCodeRepositoryContains: NotRequired[str]
    AdditionalCodeRepositoryEquals: NotRequired[str]


class ListOptimizationJobsRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    OptimizationContains: NotRequired[str]
    NameContains: NotRequired[str]
    StatusEquals: NotRequired[OptimizationJobStatusType]
    SortBy: NotRequired[ListOptimizationJobsSortByType]
    SortOrder: NotRequired[SortOrderType]


class ListPipelineExecutionsRequestRequestTypeDef(TypedDict):
    PipelineName: str
    CreatedAfter: NotRequired[TimestampTypeDef]
    CreatedBefore: NotRequired[TimestampTypeDef]
    SortBy: NotRequired[SortPipelineExecutionsByType]
    SortOrder: NotRequired[SortOrderType]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListPipelinesRequestRequestTypeDef(TypedDict):
    PipelineNamePrefix: NotRequired[str]
    CreatedAfter: NotRequired[TimestampTypeDef]
    CreatedBefore: NotRequired[TimestampTypeDef]
    SortBy: NotRequired[SortPipelinesByType]
    SortOrder: NotRequired[SortOrderType]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListProcessingJobsRequestRequestTypeDef(TypedDict):
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    NameContains: NotRequired[str]
    StatusEquals: NotRequired[ProcessingJobStatusType]
    SortBy: NotRequired[SortByType]
    SortOrder: NotRequired[SortOrderType]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListProjectsInputRequestTypeDef(TypedDict):
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    MaxResults: NotRequired[int]
    NameContains: NotRequired[str]
    NextToken: NotRequired[str]
    SortBy: NotRequired[ProjectSortByType]
    SortOrder: NotRequired[ProjectSortOrderType]


class ListResourceCatalogsRequestRequestTypeDef(TypedDict):
    NameContains: NotRequired[str]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    SortOrder: NotRequired[ResourceCatalogSortOrderType]
    SortBy: NotRequired[Literal["CreationTime"]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListStudioLifecycleConfigsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    NameContains: NotRequired[str]
    AppTypeEquals: NotRequired[StudioLifecycleConfigAppTypeType]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    ModifiedTimeBefore: NotRequired[TimestampTypeDef]
    ModifiedTimeAfter: NotRequired[TimestampTypeDef]
    SortBy: NotRequired[StudioLifecycleConfigSortKeyType]
    SortOrder: NotRequired[SortOrderType]


class ListTrainingJobsRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    NameContains: NotRequired[str]
    StatusEquals: NotRequired[TrainingJobStatusType]
    SortBy: NotRequired[SortByType]
    SortOrder: NotRequired[SortOrderType]
    WarmPoolStatusEquals: NotRequired[WarmPoolResourceStatusType]


class ListTransformJobsRequestRequestTypeDef(TypedDict):
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    NameContains: NotRequired[str]
    StatusEquals: NotRequired[TransformJobStatusType]
    SortBy: NotRequired[SortByType]
    SortOrder: NotRequired[SortOrderType]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListTrialComponentsRequestRequestTypeDef(TypedDict):
    ExperimentName: NotRequired[str]
    TrialName: NotRequired[str]
    SourceArn: NotRequired[str]
    CreatedAfter: NotRequired[TimestampTypeDef]
    CreatedBefore: NotRequired[TimestampTypeDef]
    SortBy: NotRequired[SortTrialComponentsByType]
    SortOrder: NotRequired[SortOrderType]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListTrialsRequestRequestTypeDef(TypedDict):
    ExperimentName: NotRequired[str]
    TrialComponentName: NotRequired[str]
    CreatedAfter: NotRequired[TimestampTypeDef]
    CreatedBefore: NotRequired[TimestampTypeDef]
    SortBy: NotRequired[SortTrialsByType]
    SortOrder: NotRequired[SortOrderType]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class QueryFiltersTypeDef(TypedDict):
    Types: NotRequired[Sequence[str]]
    LineageTypes: NotRequired[Sequence[LineageTypeType]]
    CreatedBefore: NotRequired[TimestampTypeDef]
    CreatedAfter: NotRequired[TimestampTypeDef]
    ModifiedBefore: NotRequired[TimestampTypeDef]
    ModifiedAfter: NotRequired[TimestampTypeDef]
    Properties: NotRequired[Mapping[str, str]]


class CreateTrialComponentRequestRequestTypeDef(TypedDict):
    TrialComponentName: str
    DisplayName: NotRequired[str]
    Status: NotRequired[TrialComponentStatusTypeDef]
    StartTime: NotRequired[TimestampTypeDef]
    EndTime: NotRequired[TimestampTypeDef]
    Parameters: NotRequired[Mapping[str, TrialComponentParameterValueTypeDef]]
    InputArtifacts: NotRequired[Mapping[str, TrialComponentArtifactTypeDef]]
    OutputArtifacts: NotRequired[Mapping[str, TrialComponentArtifactTypeDef]]
    MetadataProperties: NotRequired[MetadataPropertiesTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]


class UpdateTrialComponentRequestRequestTypeDef(TypedDict):
    TrialComponentName: str
    DisplayName: NotRequired[str]
    Status: NotRequired[TrialComponentStatusTypeDef]
    StartTime: NotRequired[TimestampTypeDef]
    EndTime: NotRequired[TimestampTypeDef]
    Parameters: NotRequired[Mapping[str, TrialComponentParameterValueTypeDef]]
    ParametersToRemove: NotRequired[Sequence[str]]
    InputArtifacts: NotRequired[Mapping[str, TrialComponentArtifactTypeDef]]
    InputArtifactsToRemove: NotRequired[Sequence[str]]
    OutputArtifacts: NotRequired[Mapping[str, TrialComponentArtifactTypeDef]]
    OutputArtifactsToRemove: NotRequired[Sequence[str]]


class CreateWorkforceRequestRequestTypeDef(TypedDict):
    WorkforceName: str
    CognitoConfig: NotRequired[CognitoConfigTypeDef]
    OidcConfig: NotRequired[OidcConfigTypeDef]
    SourceIpConfig: NotRequired[SourceIpConfigTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]
    WorkforceVpcConfig: NotRequired[WorkforceVpcConfigRequestTypeDef]


class UpdateWorkforceRequestRequestTypeDef(TypedDict):
    WorkforceName: str
    SourceIpConfig: NotRequired[SourceIpConfigTypeDef]
    OidcConfig: NotRequired[OidcConfigTypeDef]
    WorkforceVpcConfig: NotRequired[WorkforceVpcConfigRequestTypeDef]


class CustomFileSystemConfigTypeDef(TypedDict):
    EFSFileSystemConfig: NotRequired[EFSFileSystemConfigTypeDef]


class CustomFileSystemTypeDef(TypedDict):
    EFSFileSystem: NotRequired[EFSFileSystemTypeDef]


class ModelBiasBaselineConfigTypeDef(TypedDict):
    BaseliningJobName: NotRequired[str]
    ConstraintsResource: NotRequired[MonitoringConstraintsResourceTypeDef]


class ModelExplainabilityBaselineConfigTypeDef(TypedDict):
    BaseliningJobName: NotRequired[str]
    ConstraintsResource: NotRequired[MonitoringConstraintsResourceTypeDef]


class ModelQualityBaselineConfigTypeDef(TypedDict):
    BaseliningJobName: NotRequired[str]
    ConstraintsResource: NotRequired[MonitoringConstraintsResourceTypeDef]


class DataQualityBaselineConfigTypeDef(TypedDict):
    BaseliningJobName: NotRequired[str]
    ConstraintsResource: NotRequired[MonitoringConstraintsResourceTypeDef]
    StatisticsResource: NotRequired[MonitoringStatisticsResourceTypeDef]


class MonitoringBaselineConfigTypeDef(TypedDict):
    BaseliningJobName: NotRequired[str]
    ConstraintsResource: NotRequired[MonitoringConstraintsResourceTypeDef]
    StatisticsResource: NotRequired[MonitoringStatisticsResourceTypeDef]


class DataSourceOutputTypeDef(TypedDict):
    S3DataSource: NotRequired[S3DataSourceOutputTypeDef]
    FileSystemDataSource: NotRequired[FileSystemDataSourceTypeDef]


class DatasetDefinitionTypeDef(TypedDict):
    AthenaDatasetDefinition: NotRequired[AthenaDatasetDefinitionTypeDef]
    RedshiftDatasetDefinition: NotRequired[RedshiftDatasetDefinitionTypeDef]
    LocalPath: NotRequired[str]
    DataDistributionType: NotRequired[DataDistributionTypeType]
    InputMode: NotRequired[InputModeType]


DebugRuleConfigurationUnionTypeDef = Union[
    DebugRuleConfigurationTypeDef, DebugRuleConfigurationOutputTypeDef
]


class DefaultSpaceStorageSettingsTypeDef(TypedDict):
    DefaultEbsStorageSettings: NotRequired[DefaultEbsStorageSettingsTypeDef]


class DeleteDomainRequestRequestTypeDef(TypedDict):
    DomainId: str
    RetentionPolicy: NotRequired[RetentionPolicyTypeDef]


class InferenceComponentContainerSpecificationSummaryTypeDef(TypedDict):
    DeployedImage: NotRequired[DeployedImageTypeDef]
    ArtifactUrl: NotRequired[str]
    Environment: NotRequired[Dict[str, str]]


class DeploymentRecommendationTypeDef(TypedDict):
    RecommendationStatus: RecommendationStatusType
    RealTimeInferenceRecommendations: NotRequired[List[RealTimeInferenceRecommendationTypeDef]]


class DeploymentStageStatusSummaryTypeDef(TypedDict):
    StageName: str
    DeviceSelectionConfig: DeviceSelectionConfigOutputTypeDef
    DeploymentConfig: EdgeDeploymentConfigTypeDef
    DeploymentStatus: EdgeDeploymentStatusTypeDef


class DescribeDeviceResponseTypeDef(TypedDict):
    DeviceArn: str
    DeviceName: str
    Description: str
    DeviceFleetName: str
    IotThingName: str
    RegistrationTime: datetime
    LatestHeartbeat: datetime
    Models: List[EdgeModelTypeDef]
    MaxModels: int
    AgentVersion: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeEdgePackagingJobResponseTypeDef(TypedDict):
    EdgePackagingJobArn: str
    EdgePackagingJobName: str
    CompilationJobName: str
    ModelName: str
    ModelVersion: str
    RoleArn: str
    OutputConfig: EdgeOutputConfigTypeDef
    ResourceKey: str
    EdgePackagingJobStatus: EdgePackagingJobStatusType
    EdgePackagingJobStatusMessage: str
    CreationTime: datetime
    LastModifiedTime: datetime
    ModelArtifact: str
    ModelSignature: str
    PresetDeploymentOutput: EdgePresetDeploymentOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeEndpointInputEndpointDeletedWaitTypeDef(TypedDict):
    EndpointName: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeEndpointInputEndpointInServiceWaitTypeDef(TypedDict):
    EndpointName: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeImageRequestImageCreatedWaitTypeDef(TypedDict):
    ImageName: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeImageRequestImageDeletedWaitTypeDef(TypedDict):
    ImageName: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeImageRequestImageUpdatedWaitTypeDef(TypedDict):
    ImageName: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeImageVersionRequestImageVersionCreatedWaitTypeDef(TypedDict):
    ImageName: str
    Version: NotRequired[int]
    Alias: NotRequired[str]
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeImageVersionRequestImageVersionDeletedWaitTypeDef(TypedDict):
    ImageName: str
    Version: NotRequired[int]
    Alias: NotRequired[str]
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeNotebookInstanceInputNotebookInstanceDeletedWaitTypeDef(TypedDict):
    NotebookInstanceName: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeNotebookInstanceInputNotebookInstanceInServiceWaitTypeDef(TypedDict):
    NotebookInstanceName: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeNotebookInstanceInputNotebookInstanceStoppedWaitTypeDef(TypedDict):
    NotebookInstanceName: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeProcessingJobRequestProcessingJobCompletedOrStoppedWaitTypeDef(TypedDict):
    ProcessingJobName: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeTrainingJobRequestTrainingJobCompletedOrStoppedWaitTypeDef(TypedDict):
    TrainingJobName: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeTransformJobRequestTransformJobCompletedOrStoppedWaitTypeDef(TypedDict):
    TransformJobName: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class ExperimentSummaryTypeDef(TypedDict):
    ExperimentArn: NotRequired[str]
    ExperimentName: NotRequired[str]
    DisplayName: NotRequired[str]
    ExperimentSource: NotRequired[ExperimentSourceTypeDef]
    CreationTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]


class FeatureGroupSummaryTypeDef(TypedDict):
    FeatureGroupName: str
    FeatureGroupArn: str
    CreationTime: datetime
    FeatureGroupStatus: NotRequired[FeatureGroupStatusType]
    OfflineStoreStatus: NotRequired[OfflineStoreStatusTypeDef]


class DescribeFeatureMetadataResponseTypeDef(TypedDict):
    FeatureGroupArn: str
    FeatureGroupName: str
    FeatureName: str
    FeatureType: FeatureTypeType
    CreationTime: datetime
    LastModifiedTime: datetime
    Description: str
    Parameters: List[FeatureParameterTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class FeatureMetadataTypeDef(TypedDict):
    FeatureGroupArn: NotRequired[str]
    FeatureGroupName: NotRequired[str]
    FeatureName: NotRequired[str]
    FeatureType: NotRequired[FeatureTypeType]
    CreationTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]
    Description: NotRequired[str]
    Parameters: NotRequired[List[FeatureParameterTypeDef]]


class UpdateFeatureMetadataRequestRequestTypeDef(TypedDict):
    FeatureGroupName: str
    FeatureName: str
    Description: NotRequired[str]
    ParameterAdditions: NotRequired[Sequence[FeatureParameterTypeDef]]
    ParameterRemovals: NotRequired[Sequence[str]]


class DescribeHubContentResponseTypeDef(TypedDict):
    HubContentName: str
    HubContentArn: str
    HubContentVersion: str
    HubContentType: HubContentTypeType
    DocumentSchemaVersion: str
    HubName: str
    HubArn: str
    HubContentDisplayName: str
    HubContentDescription: str
    HubContentMarkdown: str
    HubContentDocument: str
    SageMakerPublicHubContentArn: str
    ReferenceMinVersion: str
    SupportStatus: HubContentSupportStatusType
    HubContentSearchKeywords: List[str]
    HubContentDependencies: List[HubContentDependencyTypeDef]
    HubContentStatus: HubContentStatusType
    FailureReason: str
    CreationTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeHumanTaskUiResponseTypeDef(TypedDict):
    HumanTaskUiArn: str
    HumanTaskUiName: str
    HumanTaskUiStatus: HumanTaskUiStatusType
    CreationTime: datetime
    UiTemplate: UiTemplateInfoTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


InferenceExperimentSummaryTypeDef = TypedDict(
    "InferenceExperimentSummaryTypeDef",
    {
        "Name": str,
        "Type": Literal["ShadowMode"],
        "Status": InferenceExperimentStatusType,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "Schedule": NotRequired[InferenceExperimentScheduleOutputTypeDef],
        "StatusReason": NotRequired[str],
        "Description": NotRequired[str],
        "CompletionTime": NotRequired[datetime],
        "RoleArn": NotRequired[str],
    },
)


class DescribeModelCardExportJobResponseTypeDef(TypedDict):
    ModelCardExportJobName: str
    ModelCardExportJobArn: str
    Status: ModelCardExportJobStatusType
    ModelCardName: str
    ModelCardVersion: int
    OutputConfig: ModelCardExportOutputConfigTypeDef
    CreatedAt: datetime
    LastModifiedAt: datetime
    FailureReason: str
    ExportArtifacts: ModelCardExportArtifactsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListMonitoringExecutionsResponseTypeDef(TypedDict):
    MonitoringExecutionSummaries: List[MonitoringExecutionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeSubscribedWorkteamResponseTypeDef(TypedDict):
    SubscribedWorkteam: SubscribedWorkteamTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListSubscribedWorkteamsResponseTypeDef(TypedDict):
    SubscribedWorkteams: List[SubscribedWorkteamTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class TrainingJobSummaryTypeDef(TypedDict):
    TrainingJobName: str
    TrainingJobArn: str
    CreationTime: datetime
    TrainingJobStatus: TrainingJobStatusType
    TrainingEndTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]
    SecondaryStatus: NotRequired[SecondaryStatusType]
    WarmPoolStatus: NotRequired[WarmPoolStatusTypeDef]


class TrialSummaryTypeDef(TypedDict):
    TrialArn: NotRequired[str]
    TrialName: NotRequired[str]
    DisplayName: NotRequired[str]
    TrialSource: NotRequired[TrialSourceTypeDef]
    CreationTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]


class DesiredWeightAndCapacityTypeDef(TypedDict):
    VariantName: str
    DesiredWeight: NotRequired[float]
    DesiredInstanceCount: NotRequired[int]
    ServerlessUpdateConfig: NotRequired[ProductionVariantServerlessUpdateConfigTypeDef]


class ListStageDevicesResponseTypeDef(TypedDict):
    DeviceDeploymentSummaries: List[DeviceDeploymentSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListDeviceFleetsResponseTypeDef(TypedDict):
    DeviceFleetSummaries: List[DeviceFleetSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


DeviceSelectionConfigUnionTypeDef = Union[
    DeviceSelectionConfigTypeDef, DeviceSelectionConfigOutputTypeDef
]


class DeviceSummaryTypeDef(TypedDict):
    DeviceName: str
    DeviceArn: str
    Description: NotRequired[str]
    DeviceFleetName: NotRequired[str]
    IotThingName: NotRequired[str]
    RegistrationTime: NotRequired[datetime]
    LatestHeartbeat: NotRequired[datetime]
    Models: NotRequired[List[EdgeModelSummaryTypeDef]]
    AgentVersion: NotRequired[str]


class RegisterDevicesRequestRequestTypeDef(TypedDict):
    DeviceFleetName: str
    Devices: Sequence[DeviceTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]


class UpdateDevicesRequestRequestTypeDef(TypedDict):
    DeviceFleetName: str
    Devices: Sequence[DeviceTypeDef]


DockerSettingsUnionTypeDef = Union[DockerSettingsTypeDef, DockerSettingsOutputTypeDef]


class ListDomainsResponseTypeDef(TypedDict):
    Domains: List[DomainDetailsTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DriftCheckBiasTypeDef(TypedDict):
    ConfigFile: NotRequired[FileSourceTypeDef]
    PreTrainingConstraints: NotRequired[MetricsSourceTypeDef]
    PostTrainingConstraints: NotRequired[MetricsSourceTypeDef]


class DriftCheckExplainabilityTypeDef(TypedDict):
    Constraints: NotRequired[MetricsSourceTypeDef]
    ConfigFile: NotRequired[FileSourceTypeDef]


class SpaceStorageSettingsTypeDef(TypedDict):
    EbsStorageSettings: NotRequired[EbsStorageSettingsTypeDef]


class ListEdgeDeploymentPlansResponseTypeDef(TypedDict):
    EdgeDeploymentPlanSummaries: List[EdgeDeploymentPlanSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class GetDeviceFleetReportResponseTypeDef(TypedDict):
    DeviceFleetArn: str
    DeviceFleetName: str
    OutputConfig: EdgeOutputConfigTypeDef
    Description: str
    ReportGenerated: datetime
    DeviceStats: DeviceStatsTypeDef
    AgentVersions: List[AgentVersionTypeDef]
    ModelStats: List[EdgeModelStatTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ListEdgePackagingJobsResponseTypeDef(TypedDict):
    EdgePackagingJobSummaries: List[EdgePackagingJobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


EmrSettingsUnionTypeDef = Union[EmrSettingsTypeDef, EmrSettingsOutputTypeDef]


class ListEndpointConfigsOutputTypeDef(TypedDict):
    EndpointConfigs: List[EndpointConfigSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class EndpointOutputConfigurationTypeDef(TypedDict):
    EndpointName: str
    VariantName: str
    InstanceType: NotRequired[ProductionVariantInstanceTypeType]
    InitialInstanceCount: NotRequired[int]
    ServerlessConfig: NotRequired[ProductionVariantServerlessConfigTypeDef]


class EndpointPerformanceTypeDef(TypedDict):
    Metrics: InferenceMetricsTypeDef
    EndpointInfo: EndpointInfoTypeDef


class ListEndpointsOutputTypeDef(TypedDict):
    Endpoints: List[EndpointSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ModelConfigurationTypeDef(TypedDict):
    InferenceSpecificationName: NotRequired[str]
    EnvironmentParameters: NotRequired[List[EnvironmentParameterTypeDef]]
    CompilationJobName: NotRequired[str]


class NestedFiltersTypeDef(TypedDict):
    NestedPropertyName: str
    Filters: Sequence[FilterTypeDef]


class HyperParameterTrainingJobSummaryTypeDef(TypedDict):
    TrainingJobName: str
    TrainingJobArn: str
    CreationTime: datetime
    TrainingJobStatus: TrainingJobStatusType
    TunedHyperParameters: Dict[str, str]
    TrainingJobDefinitionName: NotRequired[str]
    TuningJobName: NotRequired[str]
    TrainingStartTime: NotRequired[datetime]
    TrainingEndTime: NotRequired[datetime]
    FailureReason: NotRequired[str]
    FinalHyperParameterTuningJobObjectiveMetric: NotRequired[
        FinalHyperParameterTuningJobObjectiveMetricTypeDef
    ]
    ObjectiveStatus: NotRequired[ObjectiveStatusType]


class ListFlowDefinitionsResponseTypeDef(TypedDict):
    FlowDefinitionSummaries: List[FlowDefinitionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class GetScalingConfigurationRecommendationRequestRequestTypeDef(TypedDict):
    InferenceRecommendationsJobName: str
    RecommendationId: NotRequired[str]
    EndpointName: NotRequired[str]
    TargetCpuUtilizationPerCore: NotRequired[int]
    ScalingPolicyObjective: NotRequired[ScalingPolicyObjectiveTypeDef]


class GetSearchSuggestionsResponseTypeDef(TypedDict):
    PropertyNameSuggestions: List[PropertyNameSuggestionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateCodeRepositoryInputRequestTypeDef(TypedDict):
    CodeRepositoryName: str
    GitConfig: NotRequired[GitConfigForUpdateTypeDef]


class StudioWebPortalSettingsOutputTypeDef(TypedDict):
    HiddenMlTools: NotRequired[List[MlToolsType]]
    HiddenAppTypes: NotRequired[List[AppTypeType]]
    HiddenInstanceTypes: NotRequired[List[AppInstanceTypeType]]
    HiddenSageMakerImageVersionAliases: NotRequired[List[HiddenSageMakerImageOutputTypeDef]]


HiddenSageMakerImageUnionTypeDef = Union[
    HiddenSageMakerImageTypeDef, HiddenSageMakerImageOutputTypeDef
]


class ListHubContentVersionsResponseTypeDef(TypedDict):
    HubContentSummaries: List[HubContentInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListHubContentsResponseTypeDef(TypedDict):
    HubContentSummaries: List[HubContentInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListHubsResponseTypeDef(TypedDict):
    HubSummaries: List[HubInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class HumanLoopActivationConfigTypeDef(TypedDict):
    HumanLoopActivationConditionsConfig: HumanLoopActivationConditionsConfigTypeDef


class ListHumanTaskUisResponseTypeDef(TypedDict):
    HumanTaskUiSummaries: List[HumanTaskUiSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class HyperParameterTuningResourceConfigOutputTypeDef(TypedDict):
    InstanceType: NotRequired[TrainingInstanceTypeType]
    InstanceCount: NotRequired[int]
    VolumeSizeInGB: NotRequired[int]
    VolumeKmsKeyId: NotRequired[str]
    AllocationStrategy: NotRequired[Literal["Prioritized"]]
    InstanceConfigs: NotRequired[List[HyperParameterTuningInstanceConfigTypeDef]]


class HyperParameterTuningResourceConfigTypeDef(TypedDict):
    InstanceType: NotRequired[TrainingInstanceTypeType]
    InstanceCount: NotRequired[int]
    VolumeSizeInGB: NotRequired[int]
    VolumeKmsKeyId: NotRequired[str]
    AllocationStrategy: NotRequired[Literal["Prioritized"]]
    InstanceConfigs: NotRequired[Sequence[HyperParameterTuningInstanceConfigTypeDef]]


class HyperParameterTuningJobSummaryTypeDef(TypedDict):
    HyperParameterTuningJobName: str
    HyperParameterTuningJobArn: str
    HyperParameterTuningJobStatus: HyperParameterTuningJobStatusType
    Strategy: HyperParameterTuningJobStrategyTypeType
    CreationTime: datetime
    TrainingJobStatusCounters: TrainingJobStatusCountersTypeDef
    ObjectiveStatusCounters: ObjectiveStatusCountersTypeDef
    HyperParameterTuningEndTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]
    ResourceLimits: NotRequired[ResourceLimitsTypeDef]


class HyperParameterTuningJobStrategyConfigTypeDef(TypedDict):
    HyperbandStrategyConfig: NotRequired[HyperbandStrategyConfigTypeDef]


class HyperParameterTuningJobWarmStartConfigOutputTypeDef(TypedDict):
    ParentHyperParameterTuningJobs: List[ParentHyperParameterTuningJobTypeDef]
    WarmStartType: HyperParameterTuningJobWarmStartTypeType


class HyperParameterTuningJobWarmStartConfigTypeDef(TypedDict):
    ParentHyperParameterTuningJobs: Sequence[ParentHyperParameterTuningJobTypeDef]
    WarmStartType: HyperParameterTuningJobWarmStartTypeType


class UserContextTypeDef(TypedDict):
    UserProfileArn: NotRequired[str]
    UserProfileName: NotRequired[str]
    DomainId: NotRequired[str]
    IamIdentity: NotRequired[IamIdentityTypeDef]


class S3PresignTypeDef(TypedDict):
    IamPolicyConstraints: NotRequired[IamPolicyConstraintsTypeDef]


class ImageConfigTypeDef(TypedDict):
    RepositoryAccessMode: RepositoryAccessModeType
    RepositoryAuthConfig: NotRequired[RepositoryAuthConfigTypeDef]


class ListImagesResponseTypeDef(TypedDict):
    Images: List[ImageTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListImageVersionsResponseTypeDef(TypedDict):
    ImageVersions: List[ImageVersionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


InferenceComponentSpecificationTypeDef = TypedDict(
    "InferenceComponentSpecificationTypeDef",
    {
        "ModelName": NotRequired[str],
        "Container": NotRequired[InferenceComponentContainerSpecificationTypeDef],
        "StartupParameters": NotRequired[InferenceComponentStartupParametersTypeDef],
        "ComputeResourceRequirements": NotRequired[
            InferenceComponentComputeResourceRequirementsTypeDef
        ],
        "BaseInferenceComponentName": NotRequired[str],
    },
)


class ListInferenceComponentsOutputTypeDef(TypedDict):
    InferenceComponents: List[InferenceComponentSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListInferenceRecommendationsJobsResponseTypeDef(TypedDict):
    InferenceRecommendationsJobs: List[InferenceRecommendationsJobTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ResourceConfigOutputTypeDef(TypedDict):
    VolumeSizeInGB: int
    InstanceType: NotRequired[TrainingInstanceTypeType]
    InstanceCount: NotRequired[int]
    VolumeKmsKeyId: NotRequired[str]
    KeepAlivePeriodInSeconds: NotRequired[int]
    InstanceGroups: NotRequired[List[InstanceGroupTypeDef]]


class ResourceConfigTypeDef(TypedDict):
    VolumeSizeInGB: int
    InstanceType: NotRequired[TrainingInstanceTypeType]
    InstanceCount: NotRequired[int]
    VolumeKmsKeyId: NotRequired[str]
    KeepAlivePeriodInSeconds: NotRequired[int]
    InstanceGroups: NotRequired[Sequence[InstanceGroupTypeDef]]


class ParameterRangeOutputTypeDef(TypedDict):
    IntegerParameterRangeSpecification: NotRequired[IntegerParameterRangeSpecificationTypeDef]
    ContinuousParameterRangeSpecification: NotRequired[ContinuousParameterRangeSpecificationTypeDef]
    CategoricalParameterRangeSpecification: NotRequired[
        CategoricalParameterRangeSpecificationOutputTypeDef
    ]


class ParameterRangesOutputTypeDef(TypedDict):
    IntegerParameterRanges: NotRequired[List[IntegerParameterRangeTypeDef]]
    ContinuousParameterRanges: NotRequired[List[ContinuousParameterRangeTypeDef]]
    CategoricalParameterRanges: NotRequired[List[CategoricalParameterRangeOutputTypeDef]]
    AutoParameters: NotRequired[List[AutoParameterTypeDef]]


class KernelGatewayImageConfigOutputTypeDef(TypedDict):
    KernelSpecs: List[KernelSpecTypeDef]
    FileSystemConfig: NotRequired[FileSystemConfigTypeDef]


class KernelGatewayImageConfigTypeDef(TypedDict):
    KernelSpecs: Sequence[KernelSpecTypeDef]
    FileSystemConfig: NotRequired[FileSystemConfigTypeDef]


class LabelingJobForWorkteamSummaryTypeDef(TypedDict):
    JobReferenceCode: str
    WorkRequesterAccountId: str
    CreationTime: datetime
    LabelingJobName: NotRequired[str]
    LabelCounters: NotRequired[LabelCountersForWorkteamTypeDef]
    NumberOfHumanWorkersPerDataObject: NotRequired[int]


LabelingJobDataAttributesUnionTypeDef = Union[
    LabelingJobDataAttributesTypeDef, LabelingJobDataAttributesOutputTypeDef
]


class LabelingJobDataSourceTypeDef(TypedDict):
    S3DataSource: NotRequired[LabelingJobS3DataSourceTypeDef]
    SnsDataSource: NotRequired[LabelingJobSnsDataSourceTypeDef]


class ListLineageGroupsResponseTypeDef(TypedDict):
    LineageGroupSummaries: List[LineageGroupSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListActionsRequestListActionsPaginateTypeDef(TypedDict):
    SourceUri: NotRequired[str]
    ActionType: NotRequired[str]
    CreatedAfter: NotRequired[TimestampTypeDef]
    CreatedBefore: NotRequired[TimestampTypeDef]
    SortBy: NotRequired[SortActionsByType]
    SortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAlgorithmsInputListAlgorithmsPaginateTypeDef(TypedDict):
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    NameContains: NotRequired[str]
    SortBy: NotRequired[AlgorithmSortByType]
    SortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAliasesRequestListAliasesPaginateTypeDef(TypedDict):
    ImageName: str
    Alias: NotRequired[str]
    Version: NotRequired[int]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAppImageConfigsRequestListAppImageConfigsPaginateTypeDef(TypedDict):
    NameContains: NotRequired[str]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    ModifiedTimeBefore: NotRequired[TimestampTypeDef]
    ModifiedTimeAfter: NotRequired[TimestampTypeDef]
    SortBy: NotRequired[AppImageConfigSortKeyType]
    SortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAppsRequestListAppsPaginateTypeDef(TypedDict):
    SortOrder: NotRequired[SortOrderType]
    SortBy: NotRequired[Literal["CreationTime"]]
    DomainIdEquals: NotRequired[str]
    UserProfileNameEquals: NotRequired[str]
    SpaceNameEquals: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListArtifactsRequestListArtifactsPaginateTypeDef(TypedDict):
    SourceUri: NotRequired[str]
    ArtifactType: NotRequired[str]
    CreatedAfter: NotRequired[TimestampTypeDef]
    CreatedBefore: NotRequired[TimestampTypeDef]
    SortBy: NotRequired[Literal["CreationTime"]]
    SortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAssociationsRequestListAssociationsPaginateTypeDef(TypedDict):
    SourceArn: NotRequired[str]
    DestinationArn: NotRequired[str]
    SourceType: NotRequired[str]
    DestinationType: NotRequired[str]
    AssociationType: NotRequired[AssociationEdgeTypeType]
    CreatedAfter: NotRequired[TimestampTypeDef]
    CreatedBefore: NotRequired[TimestampTypeDef]
    SortBy: NotRequired[SortAssociationsByType]
    SortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAutoMLJobsRequestListAutoMLJobsPaginateTypeDef(TypedDict):
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    NameContains: NotRequired[str]
    StatusEquals: NotRequired[AutoMLJobStatusType]
    SortOrder: NotRequired[AutoMLSortOrderType]
    SortBy: NotRequired[AutoMLSortByType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListCandidatesForAutoMLJobRequestListCandidatesForAutoMLJobPaginateTypeDef(TypedDict):
    AutoMLJobName: str
    StatusEquals: NotRequired[CandidateStatusType]
    CandidateNameEquals: NotRequired[str]
    SortOrder: NotRequired[AutoMLSortOrderType]
    SortBy: NotRequired[CandidateSortByType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListClusterNodesRequestListClusterNodesPaginateTypeDef(TypedDict):
    ClusterName: str
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    InstanceGroupNameContains: NotRequired[str]
    SortBy: NotRequired[ClusterSortByType]
    SortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListClustersRequestListClustersPaginateTypeDef(TypedDict):
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    NameContains: NotRequired[str]
    SortBy: NotRequired[ClusterSortByType]
    SortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListCodeRepositoriesInputListCodeRepositoriesPaginateTypeDef(TypedDict):
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    NameContains: NotRequired[str]
    SortBy: NotRequired[CodeRepositorySortByType]
    SortOrder: NotRequired[CodeRepositorySortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListCompilationJobsRequestListCompilationJobsPaginateTypeDef(TypedDict):
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    NameContains: NotRequired[str]
    StatusEquals: NotRequired[CompilationJobStatusType]
    SortBy: NotRequired[ListCompilationJobsSortByType]
    SortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListContextsRequestListContextsPaginateTypeDef(TypedDict):
    SourceUri: NotRequired[str]
    ContextType: NotRequired[str]
    CreatedAfter: NotRequired[TimestampTypeDef]
    CreatedBefore: NotRequired[TimestampTypeDef]
    SortBy: NotRequired[SortContextsByType]
    SortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDataQualityJobDefinitionsRequestListDataQualityJobDefinitionsPaginateTypeDef(TypedDict):
    EndpointName: NotRequired[str]
    SortBy: NotRequired[MonitoringJobDefinitionSortKeyType]
    SortOrder: NotRequired[SortOrderType]
    NameContains: NotRequired[str]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDeviceFleetsRequestListDeviceFleetsPaginateTypeDef(TypedDict):
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    NameContains: NotRequired[str]
    SortBy: NotRequired[ListDeviceFleetsSortByType]
    SortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDevicesRequestListDevicesPaginateTypeDef(TypedDict):
    LatestHeartbeatAfter: NotRequired[TimestampTypeDef]
    ModelName: NotRequired[str]
    DeviceFleetName: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDomainsRequestListDomainsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListEdgeDeploymentPlansRequestListEdgeDeploymentPlansPaginateTypeDef(TypedDict):
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    NameContains: NotRequired[str]
    DeviceFleetNameContains: NotRequired[str]
    SortBy: NotRequired[ListEdgeDeploymentPlansSortByType]
    SortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListEdgePackagingJobsRequestListEdgePackagingJobsPaginateTypeDef(TypedDict):
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    NameContains: NotRequired[str]
    ModelNameContains: NotRequired[str]
    StatusEquals: NotRequired[EdgePackagingJobStatusType]
    SortBy: NotRequired[ListEdgePackagingJobsSortByType]
    SortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListEndpointConfigsInputListEndpointConfigsPaginateTypeDef(TypedDict):
    SortBy: NotRequired[EndpointConfigSortKeyType]
    SortOrder: NotRequired[OrderKeyType]
    NameContains: NotRequired[str]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListEndpointsInputListEndpointsPaginateTypeDef(TypedDict):
    SortBy: NotRequired[EndpointSortKeyType]
    SortOrder: NotRequired[OrderKeyType]
    NameContains: NotRequired[str]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    StatusEquals: NotRequired[EndpointStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListExperimentsRequestListExperimentsPaginateTypeDef(TypedDict):
    CreatedAfter: NotRequired[TimestampTypeDef]
    CreatedBefore: NotRequired[TimestampTypeDef]
    SortBy: NotRequired[SortExperimentsByType]
    SortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListFeatureGroupsRequestListFeatureGroupsPaginateTypeDef(TypedDict):
    NameContains: NotRequired[str]
    FeatureGroupStatusEquals: NotRequired[FeatureGroupStatusType]
    OfflineStoreStatusEquals: NotRequired[OfflineStoreStatusValueType]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    SortOrder: NotRequired[FeatureGroupSortOrderType]
    SortBy: NotRequired[FeatureGroupSortByType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListFlowDefinitionsRequestListFlowDefinitionsPaginateTypeDef(TypedDict):
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    SortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListHumanTaskUisRequestListHumanTaskUisPaginateTypeDef(TypedDict):
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    SortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListHyperParameterTuningJobsRequestListHyperParameterTuningJobsPaginateTypeDef(TypedDict):
    SortBy: NotRequired[HyperParameterTuningJobSortByOptionsType]
    SortOrder: NotRequired[SortOrderType]
    NameContains: NotRequired[str]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    StatusEquals: NotRequired[HyperParameterTuningJobStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListImageVersionsRequestListImageVersionsPaginateTypeDef(TypedDict):
    ImageName: str
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    SortBy: NotRequired[ImageVersionSortByType]
    SortOrder: NotRequired[ImageVersionSortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListImagesRequestListImagesPaginateTypeDef(TypedDict):
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    NameContains: NotRequired[str]
    SortBy: NotRequired[ImageSortByType]
    SortOrder: NotRequired[ImageSortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListInferenceComponentsInputListInferenceComponentsPaginateTypeDef(TypedDict):
    SortBy: NotRequired[InferenceComponentSortKeyType]
    SortOrder: NotRequired[OrderKeyType]
    NameContains: NotRequired[str]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    StatusEquals: NotRequired[InferenceComponentStatusType]
    EndpointNameEquals: NotRequired[str]
    VariantNameEquals: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


ListInferenceExperimentsRequestListInferenceExperimentsPaginateTypeDef = TypedDict(
    "ListInferenceExperimentsRequestListInferenceExperimentsPaginateTypeDef",
    {
        "NameContains": NotRequired[str],
        "Type": NotRequired[Literal["ShadowMode"]],
        "StatusEquals": NotRequired[InferenceExperimentStatusType],
        "CreationTimeAfter": NotRequired[TimestampTypeDef],
        "CreationTimeBefore": NotRequired[TimestampTypeDef],
        "LastModifiedTimeAfter": NotRequired[TimestampTypeDef],
        "LastModifiedTimeBefore": NotRequired[TimestampTypeDef],
        "SortBy": NotRequired[SortInferenceExperimentsByType],
        "SortOrder": NotRequired[SortOrderType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)


class ListInferenceRecommendationsJobStepsRequestListInferenceRecommendationsJobStepsPaginateTypeDef(
    TypedDict
):
    JobName: str
    Status: NotRequired[RecommendationJobStatusType]
    StepType: NotRequired[Literal["BENCHMARK"]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListInferenceRecommendationsJobsRequestListInferenceRecommendationsJobsPaginateTypeDef(
    TypedDict
):
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    NameContains: NotRequired[str]
    StatusEquals: NotRequired[RecommendationJobStatusType]
    SortBy: NotRequired[ListInferenceRecommendationsJobsSortByType]
    SortOrder: NotRequired[SortOrderType]
    ModelNameEquals: NotRequired[str]
    ModelPackageVersionArnEquals: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListLabelingJobsForWorkteamRequestListLabelingJobsForWorkteamPaginateTypeDef(TypedDict):
    WorkteamArn: str
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    JobReferenceCodeContains: NotRequired[str]
    SortBy: NotRequired[Literal["CreationTime"]]
    SortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListLabelingJobsRequestListLabelingJobsPaginateTypeDef(TypedDict):
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    NameContains: NotRequired[str]
    SortBy: NotRequired[SortByType]
    SortOrder: NotRequired[SortOrderType]
    StatusEquals: NotRequired[LabelingJobStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListLineageGroupsRequestListLineageGroupsPaginateTypeDef(TypedDict):
    CreatedAfter: NotRequired[TimestampTypeDef]
    CreatedBefore: NotRequired[TimestampTypeDef]
    SortBy: NotRequired[SortLineageGroupsByType]
    SortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListMlflowTrackingServersRequestListMlflowTrackingServersPaginateTypeDef(TypedDict):
    CreatedAfter: NotRequired[TimestampTypeDef]
    CreatedBefore: NotRequired[TimestampTypeDef]
    TrackingServerStatus: NotRequired[TrackingServerStatusType]
    MlflowVersion: NotRequired[str]
    SortBy: NotRequired[SortTrackingServerByType]
    SortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListModelBiasJobDefinitionsRequestListModelBiasJobDefinitionsPaginateTypeDef(TypedDict):
    EndpointName: NotRequired[str]
    SortBy: NotRequired[MonitoringJobDefinitionSortKeyType]
    SortOrder: NotRequired[SortOrderType]
    NameContains: NotRequired[str]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListModelCardExportJobsRequestListModelCardExportJobsPaginateTypeDef(TypedDict):
    ModelCardName: str
    ModelCardVersion: NotRequired[int]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    ModelCardExportJobNameContains: NotRequired[str]
    StatusEquals: NotRequired[ModelCardExportJobStatusType]
    SortBy: NotRequired[ModelCardExportJobSortByType]
    SortOrder: NotRequired[ModelCardExportJobSortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListModelCardVersionsRequestListModelCardVersionsPaginateTypeDef(TypedDict):
    ModelCardName: str
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    ModelCardStatus: NotRequired[ModelCardStatusType]
    SortBy: NotRequired[Literal["Version"]]
    SortOrder: NotRequired[ModelCardSortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListModelCardsRequestListModelCardsPaginateTypeDef(TypedDict):
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    NameContains: NotRequired[str]
    ModelCardStatus: NotRequired[ModelCardStatusType]
    SortBy: NotRequired[ModelCardSortByType]
    SortOrder: NotRequired[ModelCardSortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListModelExplainabilityJobDefinitionsRequestListModelExplainabilityJobDefinitionsPaginateTypeDef(
    TypedDict
):
    EndpointName: NotRequired[str]
    SortBy: NotRequired[MonitoringJobDefinitionSortKeyType]
    SortOrder: NotRequired[SortOrderType]
    NameContains: NotRequired[str]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListModelPackageGroupsInputListModelPackageGroupsPaginateTypeDef(TypedDict):
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    NameContains: NotRequired[str]
    SortBy: NotRequired[ModelPackageGroupSortByType]
    SortOrder: NotRequired[SortOrderType]
    CrossAccountFilterOption: NotRequired[CrossAccountFilterOptionType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListModelPackagesInputListModelPackagesPaginateTypeDef(TypedDict):
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    NameContains: NotRequired[str]
    ModelApprovalStatus: NotRequired[ModelApprovalStatusType]
    ModelPackageGroupName: NotRequired[str]
    ModelPackageType: NotRequired[ModelPackageTypeType]
    SortBy: NotRequired[ModelPackageSortByType]
    SortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListModelQualityJobDefinitionsRequestListModelQualityJobDefinitionsPaginateTypeDef(TypedDict):
    EndpointName: NotRequired[str]
    SortBy: NotRequired[MonitoringJobDefinitionSortKeyType]
    SortOrder: NotRequired[SortOrderType]
    NameContains: NotRequired[str]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListModelsInputListModelsPaginateTypeDef(TypedDict):
    SortBy: NotRequired[ModelSortKeyType]
    SortOrder: NotRequired[OrderKeyType]
    NameContains: NotRequired[str]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListMonitoringAlertHistoryRequestListMonitoringAlertHistoryPaginateTypeDef(TypedDict):
    MonitoringScheduleName: NotRequired[str]
    MonitoringAlertName: NotRequired[str]
    SortBy: NotRequired[MonitoringAlertHistorySortKeyType]
    SortOrder: NotRequired[SortOrderType]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    StatusEquals: NotRequired[MonitoringAlertStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListMonitoringAlertsRequestListMonitoringAlertsPaginateTypeDef(TypedDict):
    MonitoringScheduleName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListMonitoringExecutionsRequestListMonitoringExecutionsPaginateTypeDef(TypedDict):
    MonitoringScheduleName: NotRequired[str]
    EndpointName: NotRequired[str]
    SortBy: NotRequired[MonitoringExecutionSortKeyType]
    SortOrder: NotRequired[SortOrderType]
    ScheduledTimeBefore: NotRequired[TimestampTypeDef]
    ScheduledTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    StatusEquals: NotRequired[ExecutionStatusType]
    MonitoringJobDefinitionName: NotRequired[str]
    MonitoringTypeEquals: NotRequired[MonitoringTypeType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListMonitoringSchedulesRequestListMonitoringSchedulesPaginateTypeDef(TypedDict):
    EndpointName: NotRequired[str]
    SortBy: NotRequired[MonitoringScheduleSortKeyType]
    SortOrder: NotRequired[SortOrderType]
    NameContains: NotRequired[str]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    StatusEquals: NotRequired[ScheduleStatusType]
    MonitoringJobDefinitionName: NotRequired[str]
    MonitoringTypeEquals: NotRequired[MonitoringTypeType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListNotebookInstanceLifecycleConfigsInputListNotebookInstanceLifecycleConfigsPaginateTypeDef(
    TypedDict
):
    SortBy: NotRequired[NotebookInstanceLifecycleConfigSortKeyType]
    SortOrder: NotRequired[NotebookInstanceLifecycleConfigSortOrderType]
    NameContains: NotRequired[str]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListNotebookInstancesInputListNotebookInstancesPaginateTypeDef(TypedDict):
    SortBy: NotRequired[NotebookInstanceSortKeyType]
    SortOrder: NotRequired[NotebookInstanceSortOrderType]
    NameContains: NotRequired[str]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    StatusEquals: NotRequired[NotebookInstanceStatusType]
    NotebookInstanceLifecycleConfigNameContains: NotRequired[str]
    DefaultCodeRepositoryContains: NotRequired[str]
    AdditionalCodeRepositoryEquals: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListOptimizationJobsRequestListOptimizationJobsPaginateTypeDef(TypedDict):
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    OptimizationContains: NotRequired[str]
    NameContains: NotRequired[str]
    StatusEquals: NotRequired[OptimizationJobStatusType]
    SortBy: NotRequired[ListOptimizationJobsSortByType]
    SortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListPipelineExecutionStepsRequestListPipelineExecutionStepsPaginateTypeDef(TypedDict):
    PipelineExecutionArn: NotRequired[str]
    SortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListPipelineExecutionsRequestListPipelineExecutionsPaginateTypeDef(TypedDict):
    PipelineName: str
    CreatedAfter: NotRequired[TimestampTypeDef]
    CreatedBefore: NotRequired[TimestampTypeDef]
    SortBy: NotRequired[SortPipelineExecutionsByType]
    SortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListPipelineParametersForExecutionRequestListPipelineParametersForExecutionPaginateTypeDef(
    TypedDict
):
    PipelineExecutionArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListPipelinesRequestListPipelinesPaginateTypeDef(TypedDict):
    PipelineNamePrefix: NotRequired[str]
    CreatedAfter: NotRequired[TimestampTypeDef]
    CreatedBefore: NotRequired[TimestampTypeDef]
    SortBy: NotRequired[SortPipelinesByType]
    SortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListProcessingJobsRequestListProcessingJobsPaginateTypeDef(TypedDict):
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    NameContains: NotRequired[str]
    StatusEquals: NotRequired[ProcessingJobStatusType]
    SortBy: NotRequired[SortByType]
    SortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListResourceCatalogsRequestListResourceCatalogsPaginateTypeDef(TypedDict):
    NameContains: NotRequired[str]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    SortOrder: NotRequired[ResourceCatalogSortOrderType]
    SortBy: NotRequired[Literal["CreationTime"]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListSpacesRequestListSpacesPaginateTypeDef(TypedDict):
    SortOrder: NotRequired[SortOrderType]
    SortBy: NotRequired[SpaceSortKeyType]
    DomainIdEquals: NotRequired[str]
    SpaceNameContains: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListStageDevicesRequestListStageDevicesPaginateTypeDef(TypedDict):
    EdgeDeploymentPlanName: str
    StageName: str
    ExcludeDevicesDeployedInOtherStage: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListStudioLifecycleConfigsRequestListStudioLifecycleConfigsPaginateTypeDef(TypedDict):
    NameContains: NotRequired[str]
    AppTypeEquals: NotRequired[StudioLifecycleConfigAppTypeType]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    ModifiedTimeBefore: NotRequired[TimestampTypeDef]
    ModifiedTimeAfter: NotRequired[TimestampTypeDef]
    SortBy: NotRequired[StudioLifecycleConfigSortKeyType]
    SortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListSubscribedWorkteamsRequestListSubscribedWorkteamsPaginateTypeDef(TypedDict):
    NameContains: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListTagsInputListTagsPaginateTypeDef(TypedDict):
    ResourceArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListTrainingJobsForHyperParameterTuningJobRequestListTrainingJobsForHyperParameterTuningJobPaginateTypeDef(
    TypedDict
):
    HyperParameterTuningJobName: str
    StatusEquals: NotRequired[TrainingJobStatusType]
    SortBy: NotRequired[TrainingJobSortByOptionsType]
    SortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListTrainingJobsRequestListTrainingJobsPaginateTypeDef(TypedDict):
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    NameContains: NotRequired[str]
    StatusEquals: NotRequired[TrainingJobStatusType]
    SortBy: NotRequired[SortByType]
    SortOrder: NotRequired[SortOrderType]
    WarmPoolStatusEquals: NotRequired[WarmPoolResourceStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListTransformJobsRequestListTransformJobsPaginateTypeDef(TypedDict):
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    NameContains: NotRequired[str]
    StatusEquals: NotRequired[TransformJobStatusType]
    SortBy: NotRequired[SortByType]
    SortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListTrialComponentsRequestListTrialComponentsPaginateTypeDef(TypedDict):
    ExperimentName: NotRequired[str]
    TrialName: NotRequired[str]
    SourceArn: NotRequired[str]
    CreatedAfter: NotRequired[TimestampTypeDef]
    CreatedBefore: NotRequired[TimestampTypeDef]
    SortBy: NotRequired[SortTrialComponentsByType]
    SortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListTrialsRequestListTrialsPaginateTypeDef(TypedDict):
    ExperimentName: NotRequired[str]
    TrialComponentName: NotRequired[str]
    CreatedAfter: NotRequired[TimestampTypeDef]
    CreatedBefore: NotRequired[TimestampTypeDef]
    SortBy: NotRequired[SortTrialsByType]
    SortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListUserProfilesRequestListUserProfilesPaginateTypeDef(TypedDict):
    SortOrder: NotRequired[SortOrderType]
    SortBy: NotRequired[UserProfileSortKeyType]
    DomainIdEquals: NotRequired[str]
    UserProfileNameContains: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListWorkforcesRequestListWorkforcesPaginateTypeDef(TypedDict):
    SortBy: NotRequired[ListWorkforcesSortByOptionsType]
    SortOrder: NotRequired[SortOrderType]
    NameContains: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListWorkteamsRequestListWorkteamsPaginateTypeDef(TypedDict):
    SortBy: NotRequired[ListWorkteamsSortByOptionsType]
    SortOrder: NotRequired[SortOrderType]
    NameContains: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDataQualityJobDefinitionsResponseTypeDef(TypedDict):
    JobDefinitionSummaries: List[MonitoringJobDefinitionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListModelBiasJobDefinitionsResponseTypeDef(TypedDict):
    JobDefinitionSummaries: List[MonitoringJobDefinitionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListModelExplainabilityJobDefinitionsResponseTypeDef(TypedDict):
    JobDefinitionSummaries: List[MonitoringJobDefinitionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListModelQualityJobDefinitionsResponseTypeDef(TypedDict):
    JobDefinitionSummaries: List[MonitoringJobDefinitionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListMlflowTrackingServersResponseTypeDef(TypedDict):
    TrackingServerSummaries: List[TrackingServerSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListModelCardExportJobsResponseTypeDef(TypedDict):
    ModelCardExportJobSummaries: List[ModelCardExportJobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListModelCardVersionsResponseTypeDef(TypedDict):
    ModelCardVersionSummaryList: List[ModelCardVersionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListModelCardsResponseTypeDef(TypedDict):
    ModelCardSummaries: List[ModelCardSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListModelMetadataResponseTypeDef(TypedDict):
    ModelMetadataSummaries: List[ModelMetadataSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListModelPackageGroupsOutputTypeDef(TypedDict):
    ModelPackageGroupSummaryList: List[ModelPackageGroupSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListModelPackagesOutputTypeDef(TypedDict):
    ModelPackageSummaryList: List[ModelPackageSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListModelsOutputTypeDef(TypedDict):
    Models: List[ModelSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListMonitoringAlertHistoryResponseTypeDef(TypedDict):
    MonitoringAlertHistory: List[MonitoringAlertHistorySummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListMonitoringSchedulesResponseTypeDef(TypedDict):
    MonitoringScheduleSummaries: List[MonitoringScheduleSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListNotebookInstanceLifecycleConfigsOutputTypeDef(TypedDict):
    NotebookInstanceLifecycleConfigs: List[NotebookInstanceLifecycleConfigSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListNotebookInstancesOutputTypeDef(TypedDict):
    NotebookInstances: List[NotebookInstanceSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListOptimizationJobsResponseTypeDef(TypedDict):
    OptimizationJobSummaries: List[OptimizationJobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListPipelineExecutionsResponseTypeDef(TypedDict):
    PipelineExecutionSummaries: List[PipelineExecutionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListPipelineParametersForExecutionResponseTypeDef(TypedDict):
    PipelineParameters: List[ParameterTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListPipelinesResponseTypeDef(TypedDict):
    PipelineSummaries: List[PipelineSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListProcessingJobsResponseTypeDef(TypedDict):
    ProcessingJobSummaries: List[ProcessingJobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListProjectsOutputTypeDef(TypedDict):
    ProjectSummaryList: List[ProjectSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListResourceCatalogsResponseTypeDef(TypedDict):
    ResourceCatalogs: List[ResourceCatalogTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListStudioLifecycleConfigsResponseTypeDef(TypedDict):
    StudioLifecycleConfigs: List[StudioLifecycleConfigDetailsTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListTransformJobsResponseTypeDef(TypedDict):
    TransformJobSummaries: List[TransformJobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListUserProfilesResponseTypeDef(TypedDict):
    UserProfiles: List[UserProfileDetailsTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class MemberDefinitionOutputTypeDef(TypedDict):
    CognitoMemberDefinition: NotRequired[CognitoMemberDefinitionTypeDef]
    OidcMemberDefinition: NotRequired[OidcMemberDefinitionOutputTypeDef]


class MetricSpecificationTypeDef(TypedDict):
    Predefined: NotRequired[PredefinedMetricSpecificationTypeDef]
    Customized: NotRequired[CustomizedMetricSpecificationTypeDef]


class S3ModelDataSourceTypeDef(TypedDict):
    S3Uri: str
    S3DataType: S3ModelDataTypeType
    CompressionType: ModelCompressionTypeType
    ModelAccessConfig: NotRequired[ModelAccessConfigTypeDef]
    HubAccessConfig: NotRequired[InferenceHubAccessConfigTypeDef]
    ManifestS3Uri: NotRequired[str]


class TextGenerationJobConfigOutputTypeDef(TypedDict):
    CompletionCriteria: NotRequired[AutoMLJobCompletionCriteriaTypeDef]
    BaseModelName: NotRequired[str]
    TextGenerationHyperParameters: NotRequired[Dict[str, str]]
    ModelAccessConfig: NotRequired[ModelAccessConfigTypeDef]


class TextGenerationJobConfigTypeDef(TypedDict):
    CompletionCriteria: NotRequired[AutoMLJobCompletionCriteriaTypeDef]
    BaseModelName: NotRequired[str]
    TextGenerationHyperParameters: NotRequired[Mapping[str, str]]
    ModelAccessConfig: NotRequired[ModelAccessConfigTypeDef]


ModelCompilationConfigUnionTypeDef = Union[
    ModelCompilationConfigTypeDef, ModelCompilationConfigOutputTypeDef
]


class MonitoringAlertActionsTypeDef(TypedDict):
    ModelDashboardIndicator: NotRequired[ModelDashboardIndicatorActionTypeDef]


class ModelInfrastructureConfigTypeDef(TypedDict):
    InfrastructureType: Literal["RealTimeInference"]
    RealTimeInferenceConfig: RealTimeInferenceConfigTypeDef


class RecommendationJobStoppingConditionsOutputTypeDef(TypedDict):
    MaxInvocations: NotRequired[int]
    ModelLatencyThresholds: NotRequired[List[ModelLatencyThresholdTypeDef]]
    FlatInvocations: NotRequired[FlatInvocationsType]


class RecommendationJobStoppingConditionsTypeDef(TypedDict):
    MaxInvocations: NotRequired[int]
    ModelLatencyThresholds: NotRequired[Sequence[ModelLatencyThresholdTypeDef]]
    FlatInvocations: NotRequired[FlatInvocationsType]


class ModelMetadataSearchExpressionTypeDef(TypedDict):
    Filters: NotRequired[Sequence[ModelMetadataFilterTypeDef]]


class ModelPackageStatusDetailsTypeDef(TypedDict):
    ValidationStatuses: List[ModelPackageStatusItemTypeDef]
    ImageScanStatuses: NotRequired[List[ModelPackageStatusItemTypeDef]]


ModelQuantizationConfigUnionTypeDef = Union[
    ModelQuantizationConfigTypeDef, ModelQuantizationConfigOutputTypeDef
]


class OptimizationConfigOutputTypeDef(TypedDict):
    ModelQuantizationConfig: NotRequired[ModelQuantizationConfigOutputTypeDef]
    ModelCompilationConfig: NotRequired[ModelCompilationConfigOutputTypeDef]
    ModelShardingConfig: NotRequired[ModelShardingConfigOutputTypeDef]


ModelShardingConfigUnionTypeDef = Union[
    ModelShardingConfigTypeDef, ModelShardingConfigOutputTypeDef
]
MonitoringAppSpecificationUnionTypeDef = Union[
    MonitoringAppSpecificationTypeDef, MonitoringAppSpecificationOutputTypeDef
]


class MonitoringResourcesTypeDef(TypedDict):
    ClusterConfig: MonitoringClusterConfigTypeDef


class MonitoringDatasetFormatOutputTypeDef(TypedDict):
    Csv: NotRequired[MonitoringCsvDatasetFormatTypeDef]
    Json: NotRequired[MonitoringJsonDatasetFormatTypeDef]
    Parquet: NotRequired[Dict[str, Any]]


class MonitoringDatasetFormatTypeDef(TypedDict):
    Csv: NotRequired[MonitoringCsvDatasetFormatTypeDef]
    Json: NotRequired[MonitoringJsonDatasetFormatTypeDef]
    Parquet: NotRequired[Mapping[str, Any]]


class MonitoringOutputTypeDef(TypedDict):
    S3Output: MonitoringS3OutputTypeDef


class OfflineStoreConfigTypeDef(TypedDict):
    S3StorageConfig: S3StorageConfigTypeDef
    DisableGlueTableCreation: NotRequired[bool]
    DataCatalogConfig: NotRequired[DataCatalogConfigTypeDef]
    TableFormat: NotRequired[TableFormatType]


OidcMemberDefinitionUnionTypeDef = Union[
    OidcMemberDefinitionTypeDef, OidcMemberDefinitionOutputTypeDef
]


class OnlineStoreConfigTypeDef(TypedDict):
    SecurityConfig: NotRequired[OnlineStoreSecurityConfigTypeDef]
    EnableOnlineStore: NotRequired[bool]
    TtlDuration: NotRequired[TtlDurationTypeDef]
    StorageType: NotRequired[StorageTypeType]


class OnlineStoreConfigUpdateTypeDef(TypedDict):
    TtlDuration: NotRequired[TtlDurationTypeDef]


class OptimizationJobModelSourceS3TypeDef(TypedDict):
    S3Uri: NotRequired[str]
    ModelAccessConfig: NotRequired[OptimizationModelAccessConfigTypeDef]


class OutputConfigTypeDef(TypedDict):
    S3OutputLocation: str
    TargetDevice: NotRequired[TargetDeviceType]
    TargetPlatform: NotRequired[TargetPlatformTypeDef]
    CompilerOptions: NotRequired[str]
    KmsKeyId: NotRequired[str]


class PendingProductionVariantSummaryTypeDef(TypedDict):
    VariantName: str
    DeployedImages: NotRequired[List[DeployedImageTypeDef]]
    CurrentWeight: NotRequired[float]
    DesiredWeight: NotRequired[float]
    CurrentInstanceCount: NotRequired[int]
    DesiredInstanceCount: NotRequired[int]
    InstanceType: NotRequired[ProductionVariantInstanceTypeType]
    AcceleratorType: NotRequired[ProductionVariantAcceleratorTypeType]
    VariantStatus: NotRequired[List[ProductionVariantStatusTypeDef]]
    CurrentServerlessConfig: NotRequired[ProductionVariantServerlessConfigTypeDef]
    DesiredServerlessConfig: NotRequired[ProductionVariantServerlessConfigTypeDef]
    ManagedInstanceScaling: NotRequired[ProductionVariantManagedInstanceScalingTypeDef]
    RoutingConfig: NotRequired[ProductionVariantRoutingConfigTypeDef]


class ProductionVariantSummaryTypeDef(TypedDict):
    VariantName: str
    DeployedImages: NotRequired[List[DeployedImageTypeDef]]
    CurrentWeight: NotRequired[float]
    DesiredWeight: NotRequired[float]
    CurrentInstanceCount: NotRequired[int]
    DesiredInstanceCount: NotRequired[int]
    VariantStatus: NotRequired[List[ProductionVariantStatusTypeDef]]
    CurrentServerlessConfig: NotRequired[ProductionVariantServerlessConfigTypeDef]
    DesiredServerlessConfig: NotRequired[ProductionVariantServerlessConfigTypeDef]
    ManagedInstanceScaling: NotRequired[ProductionVariantManagedInstanceScalingTypeDef]
    RoutingConfig: NotRequired[ProductionVariantRoutingConfigTypeDef]


class ProcessingResourcesTypeDef(TypedDict):
    ClusterConfig: ProcessingClusterConfigTypeDef


class ProcessingOutputTypeDef(TypedDict):
    OutputName: str
    S3Output: NotRequired[ProcessingS3OutputTypeDef]
    FeatureStoreOutput: NotRequired[ProcessingFeatureStoreOutputTypeDef]
    AppManaged: NotRequired[bool]


class ProductionVariantTypeDef(TypedDict):
    VariantName: str
    ModelName: NotRequired[str]
    InitialInstanceCount: NotRequired[int]
    InstanceType: NotRequired[ProductionVariantInstanceTypeType]
    InitialVariantWeight: NotRequired[float]
    AcceleratorType: NotRequired[ProductionVariantAcceleratorTypeType]
    CoreDumpConfig: NotRequired[ProductionVariantCoreDumpConfigTypeDef]
    ServerlessConfig: NotRequired[ProductionVariantServerlessConfigTypeDef]
    VolumeSizeInGB: NotRequired[int]
    ModelDataDownloadTimeoutInSeconds: NotRequired[int]
    ContainerStartupHealthCheckTimeoutInSeconds: NotRequired[int]
    EnableSSMAccess: NotRequired[bool]
    ManagedInstanceScaling: NotRequired[ProductionVariantManagedInstanceScalingTypeDef]
    RoutingConfig: NotRequired[ProductionVariantRoutingConfigTypeDef]
    InferenceAmiVersion: NotRequired[Literal["al2-ami-sagemaker-inference-gpu-2"]]


ProfilerRuleConfigurationUnionTypeDef = Union[
    ProfilerRuleConfigurationTypeDef, ProfilerRuleConfigurationOutputTypeDef
]


class SuggestionQueryTypeDef(TypedDict):
    PropertyNameQuery: NotRequired[PropertyNameQueryTypeDef]


class ServiceCatalogProvisioningDetailsOutputTypeDef(TypedDict):
    ProductId: str
    ProvisioningArtifactId: NotRequired[str]
    PathId: NotRequired[str]
    ProvisioningParameters: NotRequired[List[ProvisioningParameterTypeDef]]


class ServiceCatalogProvisioningDetailsTypeDef(TypedDict):
    ProductId: str
    ProvisioningArtifactId: NotRequired[str]
    PathId: NotRequired[str]
    ProvisioningParameters: NotRequired[Sequence[ProvisioningParameterTypeDef]]


class ServiceCatalogProvisioningUpdateDetailsTypeDef(TypedDict):
    ProvisioningArtifactId: NotRequired[str]
    ProvisioningParameters: NotRequired[Sequence[ProvisioningParameterTypeDef]]


class PublicWorkforceTaskPriceTypeDef(TypedDict):
    AmountInUsd: NotRequired[USDTypeDef]


class QueryLineageResponseTypeDef(TypedDict):
    Vertices: List[VertexTypeDef]
    Edges: List[EdgeTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class RecommendationJobOutputConfigTypeDef(TypedDict):
    KmsKeyId: NotRequired[str]
    CompiledOutputConfig: NotRequired[RecommendationJobCompiledOutputConfigTypeDef]


class RecommendationJobContainerConfigOutputTypeDef(TypedDict):
    Domain: NotRequired[str]
    Task: NotRequired[str]
    Framework: NotRequired[str]
    FrameworkVersion: NotRequired[str]
    PayloadConfig: NotRequired[RecommendationJobPayloadConfigOutputTypeDef]
    NearestModelName: NotRequired[str]
    SupportedInstanceTypes: NotRequired[List[str]]
    SupportedEndpointType: NotRequired[RecommendationJobSupportedEndpointTypeType]
    DataInputConfig: NotRequired[str]
    SupportedResponseMIMETypes: NotRequired[List[str]]


RecommendationJobPayloadConfigUnionTypeDef = Union[
    RecommendationJobPayloadConfigTypeDef, RecommendationJobPayloadConfigOutputTypeDef
]
RecommendationJobVpcConfigUnionTypeDef = Union[
    RecommendationJobVpcConfigTypeDef, RecommendationJobVpcConfigOutputTypeDef
]


class RenderUiTemplateRequestRequestTypeDef(TypedDict):
    Task: RenderableTaskTypeDef
    RoleArn: str
    UiTemplate: NotRequired[UiTemplateTypeDef]
    HumanTaskUiArn: NotRequired[str]


class RenderUiTemplateResponseTypeDef(TypedDict):
    RenderedContent: str
    Errors: List[RenderingErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateTrainingJobRequestRequestTypeDef(TypedDict):
    TrainingJobName: str
    ProfilerConfig: NotRequired[ProfilerConfigForUpdateTypeDef]
    ProfilerRuleConfigurations: NotRequired[Sequence[ProfilerRuleConfigurationTypeDef]]
    ResourceConfig: NotRequired[ResourceConfigForUpdateTypeDef]
    RemoteDebugConfig: NotRequired[RemoteDebugConfigForUpdateTypeDef]


S3DataSourceUnionTypeDef = Union[S3DataSourceTypeDef, S3DataSourceOutputTypeDef]


class SelectiveExecutionConfigOutputTypeDef(TypedDict):
    SelectedSteps: List[SelectedStepTypeDef]
    SourcePipelineExecutionArn: NotRequired[str]


class SelectiveExecutionConfigTypeDef(TypedDict):
    SelectedSteps: Sequence[SelectedStepTypeDef]
    SourcePipelineExecutionArn: NotRequired[str]


class ShadowModeConfigOutputTypeDef(TypedDict):
    SourceModelVariantName: str
    ShadowModelVariants: List[ShadowModelVariantConfigTypeDef]


class ShadowModeConfigTypeDef(TypedDict):
    SourceModelVariantName: str
    ShadowModelVariants: Sequence[ShadowModelVariantConfigTypeDef]


class SpaceAppLifecycleManagementTypeDef(TypedDict):
    IdleSettings: NotRequired[SpaceIdleSettingsTypeDef]


class TrafficPatternOutputTypeDef(TypedDict):
    TrafficType: NotRequired[TrafficTypeType]
    Phases: NotRequired[List[PhaseTypeDef]]
    Stairs: NotRequired[StairsTypeDef]


class TrafficPatternTypeDef(TypedDict):
    TrafficType: NotRequired[TrafficTypeType]
    Phases: NotRequired[Sequence[PhaseTypeDef]]
    Stairs: NotRequired[StairsTypeDef]


TimeSeriesConfigUnionTypeDef = Union[TimeSeriesConfigTypeDef, TimeSeriesConfigOutputTypeDef]
TimeSeriesTransformationsUnionTypeDef = Union[
    TimeSeriesTransformationsTypeDef, TimeSeriesTransformationsOutputTypeDef
]


class TrainingImageConfigTypeDef(TypedDict):
    TrainingRepositoryAccessMode: TrainingRepositoryAccessModeType
    TrainingRepositoryAuthConfig: NotRequired[TrainingRepositoryAuthConfigTypeDef]


class TransformDataSourceTypeDef(TypedDict):
    S3DataSource: TransformS3DataSourceTypeDef


class WorkforceTypeDef(TypedDict):
    WorkforceName: str
    WorkforceArn: str
    LastUpdatedDate: NotRequired[datetime]
    SourceIpConfig: NotRequired[SourceIpConfigOutputTypeDef]
    SubDomain: NotRequired[str]
    CognitoConfig: NotRequired[CognitoConfigTypeDef]
    OidcConfig: NotRequired[OidcConfigForResponseTypeDef]
    CreateDate: NotRequired[datetime]
    WorkforceVpcConfig: NotRequired[WorkforceVpcConfigResponseTypeDef]
    Status: NotRequired[WorkforceStatusType]
    FailureReason: NotRequired[str]


class ListActionsResponseTypeDef(TypedDict):
    ActionSummaries: List[ActionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


AutoRollbackConfigUnionTypeDef = Union[AutoRollbackConfigTypeDef, AutoRollbackConfigOutputTypeDef]
HyperParameterAlgorithmSpecificationUnionTypeDef = Union[
    HyperParameterAlgorithmSpecificationTypeDef, HyperParameterAlgorithmSpecificationOutputTypeDef
]


class ListAppsResponseTypeDef(TypedDict):
    Apps: List[AppDetailsTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DomainSettingsOutputTypeDef(TypedDict):
    SecurityGroupIds: NotRequired[List[str]]
    RStudioServerProDomainSettings: NotRequired[RStudioServerProDomainSettingsTypeDef]
    ExecutionRoleIdentityConfig: NotRequired[ExecutionRoleIdentityConfigType]
    DockerSettings: NotRequired[DockerSettingsOutputTypeDef]
    AmazonQSettings: NotRequired[AmazonQSettingsTypeDef]


class CodeEditorAppSettingsOutputTypeDef(TypedDict):
    DefaultResourceSpec: NotRequired[ResourceSpecTypeDef]
    CustomImages: NotRequired[List[CustomImageTypeDef]]
    LifecycleConfigArns: NotRequired[List[str]]
    AppLifecycleManagement: NotRequired[AppLifecycleManagementTypeDef]
    BuiltInLifecycleConfigArn: NotRequired[str]


class CodeEditorAppSettingsTypeDef(TypedDict):
    DefaultResourceSpec: NotRequired[ResourceSpecTypeDef]
    CustomImages: NotRequired[Sequence[CustomImageTypeDef]]
    LifecycleConfigArns: NotRequired[Sequence[str]]
    AppLifecycleManagement: NotRequired[AppLifecycleManagementTypeDef]
    BuiltInLifecycleConfigArn: NotRequired[str]


class JupyterLabAppSettingsOutputTypeDef(TypedDict):
    DefaultResourceSpec: NotRequired[ResourceSpecTypeDef]
    CustomImages: NotRequired[List[CustomImageTypeDef]]
    LifecycleConfigArns: NotRequired[List[str]]
    CodeRepositories: NotRequired[List[CodeRepositoryTypeDef]]
    AppLifecycleManagement: NotRequired[AppLifecycleManagementTypeDef]
    EmrSettings: NotRequired[EmrSettingsOutputTypeDef]
    BuiltInLifecycleConfigArn: NotRequired[str]


class ArtifactSummaryTypeDef(TypedDict):
    ArtifactArn: NotRequired[str]
    ArtifactName: NotRequired[str]
    Source: NotRequired[ArtifactSourceOutputTypeDef]
    ArtifactType: NotRequired[str]
    CreationTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]


class CreateArtifactRequestRequestTypeDef(TypedDict):
    Source: ArtifactSourceTypeDef
    ArtifactType: str
    ArtifactName: NotRequired[str]
    Properties: NotRequired[Mapping[str, str]]
    MetadataProperties: NotRequired[MetadataPropertiesTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]


class DeleteArtifactRequestRequestTypeDef(TypedDict):
    ArtifactArn: NotRequired[str]
    Source: NotRequired[ArtifactSourceTypeDef]


class AsyncInferenceConfigOutputTypeDef(TypedDict):
    OutputConfig: AsyncInferenceOutputConfigOutputTypeDef
    ClientConfig: NotRequired[AsyncInferenceClientConfigTypeDef]


class AsyncInferenceOutputConfigTypeDef(TypedDict):
    KmsKeyId: NotRequired[str]
    S3OutputPath: NotRequired[str]
    NotificationConfig: NotRequired[AsyncInferenceNotificationConfigUnionTypeDef]
    S3FailurePath: NotRequired[str]


class TabularJobConfigOutputTypeDef(TypedDict):
    TargetAttributeName: str
    CandidateGenerationConfig: NotRequired[CandidateGenerationConfigOutputTypeDef]
    CompletionCriteria: NotRequired[AutoMLJobCompletionCriteriaTypeDef]
    FeatureSpecificationS3Uri: NotRequired[str]
    Mode: NotRequired[AutoMLModeType]
    GenerateCandidateDefinitionsOnly: NotRequired[bool]
    ProblemType: NotRequired[ProblemTypeType]
    SampleWeightAttributeName: NotRequired[str]


class TimeSeriesForecastingJobConfigOutputTypeDef(TypedDict):
    ForecastFrequency: str
    ForecastHorizon: int
    TimeSeriesConfig: TimeSeriesConfigOutputTypeDef
    FeatureSpecificationS3Uri: NotRequired[str]
    CompletionCriteria: NotRequired[AutoMLJobCompletionCriteriaTypeDef]
    ForecastQuantiles: NotRequired[List[str]]
    Transformations: NotRequired[TimeSeriesTransformationsOutputTypeDef]
    HolidayConfig: NotRequired[List[HolidayConfigAttributesTypeDef]]
    CandidateGenerationConfig: NotRequired[CandidateGenerationConfigOutputTypeDef]


class AutoMLCandidateGenerationConfigTypeDef(TypedDict):
    FeatureSpecificationS3Uri: NotRequired[str]
    AlgorithmsConfig: NotRequired[Sequence[AutoMLAlgorithmConfigUnionTypeDef]]


class CandidateGenerationConfigTypeDef(TypedDict):
    AlgorithmsConfig: NotRequired[Sequence[AutoMLAlgorithmConfigUnionTypeDef]]


class AutoMLChannelTypeDef(TypedDict):
    TargetAttributeName: str
    DataSource: NotRequired[AutoMLDataSourceTypeDef]
    CompressionType: NotRequired[CompressionTypeType]
    ContentType: NotRequired[str]
    ChannelType: NotRequired[AutoMLChannelTypeType]
    SampleWeightAttributeName: NotRequired[str]


class AutoMLJobChannelTypeDef(TypedDict):
    ChannelType: NotRequired[AutoMLChannelTypeType]
    ContentType: NotRequired[str]
    CompressionType: NotRequired[CompressionTypeType]
    DataSource: NotRequired[AutoMLDataSourceTypeDef]


class ListAutoMLJobsResponseTypeDef(TypedDict):
    AutoMLJobSummaries: List[AutoMLJobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class AutoMLResolvedAttributesTypeDef(TypedDict):
    AutoMLJobObjective: NotRequired[AutoMLJobObjectiveTypeDef]
    CompletionCriteria: NotRequired[AutoMLJobCompletionCriteriaTypeDef]
    AutoMLProblemTypeResolvedAttributes: NotRequired[AutoMLProblemTypeResolvedAttributesTypeDef]


class AutoMLJobConfigOutputTypeDef(TypedDict):
    CompletionCriteria: NotRequired[AutoMLJobCompletionCriteriaTypeDef]
    SecurityConfig: NotRequired[AutoMLSecurityConfigOutputTypeDef]
    CandidateGenerationConfig: NotRequired[AutoMLCandidateGenerationConfigOutputTypeDef]
    DataSplitConfig: NotRequired[AutoMLDataSplitConfigTypeDef]
    Mode: NotRequired[AutoMLModeType]


class LabelingJobAlgorithmsConfigOutputTypeDef(TypedDict):
    LabelingJobAlgorithmSpecificationArn: str
    InitialActiveLearningModelArn: NotRequired[str]
    LabelingJobResourceConfig: NotRequired[LabelingJobResourceConfigOutputTypeDef]


class ModelMetricsTypeDef(TypedDict):
    ModelQuality: NotRequired[ModelQualityTypeDef]
    ModelDataQuality: NotRequired[ModelDataQualityTypeDef]
    Bias: NotRequired[BiasTypeDef]
    Explainability: NotRequired[ExplainabilityTypeDef]


class PipelineExecutionStepMetadataTypeDef(TypedDict):
    TrainingJob: NotRequired[TrainingJobStepMetadataTypeDef]
    ProcessingJob: NotRequired[ProcessingJobStepMetadataTypeDef]
    TransformJob: NotRequired[TransformJobStepMetadataTypeDef]
    TuningJob: NotRequired[TuningJobStepMetaDataTypeDef]
    Model: NotRequired[ModelStepMetadataTypeDef]
    RegisterModel: NotRequired[RegisterModelStepMetadataTypeDef]
    Condition: NotRequired[ConditionStepMetadataTypeDef]
    Callback: NotRequired[CallbackStepMetadataTypeDef]
    Lambda: NotRequired[LambdaStepMetadataTypeDef]
    EMR: NotRequired[EMRStepMetadataTypeDef]
    QualityCheck: NotRequired[QualityCheckStepMetadataTypeDef]
    ClarifyCheck: NotRequired[ClarifyCheckStepMetadataTypeDef]
    Fail: NotRequired[FailStepMetadataTypeDef]
    AutoMLJob: NotRequired[AutoMLJobStepMetadataTypeDef]
    Endpoint: NotRequired[EndpointStepMetadataTypeDef]
    EndpointConfig: NotRequired[EndpointConfigStepMetadataTypeDef]


class AutoMLCandidateTypeDef(TypedDict):
    CandidateName: str
    ObjectiveStatus: ObjectiveStatusType
    CandidateSteps: List[AutoMLCandidateStepTypeDef]
    CandidateStatus: CandidateStatusType
    CreationTime: datetime
    LastModifiedTime: datetime
    FinalAutoMLJobObjectiveMetric: NotRequired[FinalAutoMLJobObjectiveMetricTypeDef]
    InferenceContainers: NotRequired[List[AutoMLContainerDefinitionTypeDef]]
    EndTime: NotRequired[datetime]
    FailureReason: NotRequired[str]
    CandidateProperties: NotRequired[CandidatePropertiesTypeDef]
    InferenceContainerDefinitions: NotRequired[
        Dict[AutoMLProcessingUnitType, List[AutoMLContainerDefinitionTypeDef]]
    ]


CanvasAppSettingsUnionTypeDef = Union[CanvasAppSettingsTypeDef, CanvasAppSettingsOutputTypeDef]


class BlueGreenUpdatePolicyTypeDef(TypedDict):
    TrafficRoutingConfiguration: TrafficRoutingConfigTypeDef
    TerminationWaitInSeconds: NotRequired[int]
    MaximumExecutionTimeoutInSeconds: NotRequired[int]


class DataCaptureConfigTypeDef(TypedDict):
    InitialSamplingPercentage: int
    DestinationS3Uri: str
    CaptureOptions: Sequence[CaptureOptionTypeDef]
    EnableCapture: NotRequired[bool]
    KmsKeyId: NotRequired[str]
    CaptureContentTypeHeader: NotRequired[CaptureContentTypeHeaderUnionTypeDef]


class InferenceExperimentDataStorageConfigTypeDef(TypedDict):
    Destination: str
    KmsKey: NotRequired[str]
    ContentType: NotRequired[CaptureContentTypeHeaderUnionTypeDef]


class EndpointInputConfigurationOutputTypeDef(TypedDict):
    InstanceType: NotRequired[ProductionVariantInstanceTypeType]
    ServerlessConfig: NotRequired[ProductionVariantServerlessConfigTypeDef]
    InferenceSpecificationName: NotRequired[str]
    EnvironmentParameterRanges: NotRequired[EnvironmentParameterRangesOutputTypeDef]


class ParameterRangeTypeDef(TypedDict):
    IntegerParameterRangeSpecification: NotRequired[IntegerParameterRangeSpecificationTypeDef]
    ContinuousParameterRangeSpecification: NotRequired[ContinuousParameterRangeSpecificationTypeDef]
    CategoricalParameterRangeSpecification: NotRequired[
        CategoricalParameterRangeSpecificationUnionTypeDef
    ]


class ParameterRangesTypeDef(TypedDict):
    IntegerParameterRanges: NotRequired[Sequence[IntegerParameterRangeTypeDef]]
    ContinuousParameterRanges: NotRequired[Sequence[ContinuousParameterRangeTypeDef]]
    CategoricalParameterRanges: NotRequired[Sequence[CategoricalParameterRangeUnionTypeDef]]
    AutoParameters: NotRequired[Sequence[AutoParameterTypeDef]]


class EnvironmentParameterRangesTypeDef(TypedDict):
    CategoricalParameterRanges: NotRequired[Sequence[CategoricalParameterUnionTypeDef]]


class ClarifyExplainerConfigOutputTypeDef(TypedDict):
    ShapConfig: ClarifyShapConfigTypeDef
    EnableExplanations: NotRequired[str]
    InferenceConfig: NotRequired[ClarifyInferenceConfigOutputTypeDef]


class ClarifyExplainerConfigTypeDef(TypedDict):
    ShapConfig: ClarifyShapConfigTypeDef
    EnableExplanations: NotRequired[str]
    InferenceConfig: NotRequired[ClarifyInferenceConfigUnionTypeDef]


class ClusterInstanceGroupDetailsTypeDef(TypedDict):
    CurrentCount: NotRequired[int]
    TargetCount: NotRequired[int]
    InstanceGroupName: NotRequired[str]
    InstanceType: NotRequired[ClusterInstanceTypeType]
    LifeCycleConfig: NotRequired[ClusterLifeCycleConfigTypeDef]
    ExecutionRole: NotRequired[str]
    ThreadsPerCore: NotRequired[int]
    InstanceStorageConfigs: NotRequired[List[ClusterInstanceStorageConfigTypeDef]]
    OnStartDeepHealthChecks: NotRequired[List[DeepHealthCheckTypeType]]
    OverrideVpcConfig: NotRequired[VpcConfigOutputTypeDef]


class ClusterNodeDetailsTypeDef(TypedDict):
    InstanceGroupName: NotRequired[str]
    InstanceId: NotRequired[str]
    InstanceStatus: NotRequired[ClusterInstanceStatusDetailsTypeDef]
    InstanceType: NotRequired[ClusterInstanceTypeType]
    LaunchTime: NotRequired[datetime]
    LifeCycleConfig: NotRequired[ClusterLifeCycleConfigTypeDef]
    OverrideVpcConfig: NotRequired[VpcConfigOutputTypeDef]
    ThreadsPerCore: NotRequired[int]
    InstanceStorageConfigs: NotRequired[List[ClusterInstanceStorageConfigTypeDef]]
    PrivatePrimaryIp: NotRequired[str]
    PrivateDnsHostname: NotRequired[str]
    Placement: NotRequired[ClusterInstancePlacementTypeDef]


class ListClusterNodesResponseTypeDef(TypedDict):
    NextToken: str
    ClusterNodeSummaries: List[ClusterNodeSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


KernelGatewayAppSettingsUnionTypeDef = Union[
    KernelGatewayAppSettingsTypeDef, KernelGatewayAppSettingsOutputTypeDef
]
RSessionAppSettingsUnionTypeDef = Union[
    RSessionAppSettingsTypeDef, RSessionAppSettingsOutputTypeDef
]


class ListCodeRepositoriesOutputTypeDef(TypedDict):
    CodeRepositorySummaryList: List[CodeRepositorySummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


JupyterServerAppSettingsUnionTypeDef = Union[
    JupyterServerAppSettingsTypeDef, JupyterServerAppSettingsOutputTypeDef
]


class FeatureDefinitionTypeDef(TypedDict):
    FeatureName: str
    FeatureType: FeatureTypeType
    CollectionType: NotRequired[CollectionTypeType]
    CollectionConfig: NotRequired[CollectionConfigTypeDef]


class DebugHookConfigTypeDef(TypedDict):
    S3OutputPath: str
    LocalPath: NotRequired[str]
    HookParameters: NotRequired[Mapping[str, str]]
    CollectionConfigurations: NotRequired[Sequence[CollectionConfigurationUnionTypeDef]]


class CodeEditorAppImageConfigTypeDef(TypedDict):
    FileSystemConfig: NotRequired[FileSystemConfigTypeDef]
    ContainerConfig: NotRequired[ContainerConfigUnionTypeDef]


class JupyterLabAppImageConfigTypeDef(TypedDict):
    FileSystemConfig: NotRequired[FileSystemConfigTypeDef]
    ContainerConfig: NotRequired[ContainerConfigUnionTypeDef]


class ListContextsResponseTypeDef(TypedDict):
    ContextSummaries: List[ContextSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class AutoMLSecurityConfigTypeDef(TypedDict):
    VolumeKmsKeyId: NotRequired[str]
    EnableInterContainerTrafficEncryption: NotRequired[bool]
    VpcConfig: NotRequired[VpcConfigUnionTypeDef]


class ClusterInstanceGroupSpecificationTypeDef(TypedDict):
    InstanceCount: int
    InstanceGroupName: str
    InstanceType: ClusterInstanceTypeType
    LifeCycleConfig: ClusterLifeCycleConfigTypeDef
    ExecutionRole: str
    ThreadsPerCore: NotRequired[int]
    InstanceStorageConfigs: NotRequired[Sequence[ClusterInstanceStorageConfigTypeDef]]
    OnStartDeepHealthChecks: NotRequired[Sequence[DeepHealthCheckTypeType]]
    OverrideVpcConfig: NotRequired[VpcConfigUnionTypeDef]


class LabelingJobResourceConfigTypeDef(TypedDict):
    VolumeKmsKeyId: NotRequired[str]
    VpcConfig: NotRequired[VpcConfigUnionTypeDef]


class MonitoringNetworkConfigTypeDef(TypedDict):
    EnableInterContainerTrafficEncryption: NotRequired[bool]
    EnableNetworkIsolation: NotRequired[bool]
    VpcConfig: NotRequired[VpcConfigUnionTypeDef]


class NetworkConfigTypeDef(TypedDict):
    EnableInterContainerTrafficEncryption: NotRequired[bool]
    EnableNetworkIsolation: NotRequired[bool]
    VpcConfig: NotRequired[VpcConfigUnionTypeDef]


class QueryLineageRequestRequestTypeDef(TypedDict):
    StartArns: NotRequired[Sequence[str]]
    Direction: NotRequired[DirectionType]
    IncludeEdges: NotRequired[bool]
    Filters: NotRequired[QueryFiltersTypeDef]
    MaxDepth: NotRequired[int]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


ChannelOutputTypeDef = TypedDict(
    "ChannelOutputTypeDef",
    {
        "ChannelName": str,
        "DataSource": DataSourceOutputTypeDef,
        "ContentType": NotRequired[str],
        "CompressionType": NotRequired[CompressionTypeType],
        "RecordWrapperType": NotRequired[RecordWrapperType],
        "InputMode": NotRequired[TrainingInputModeType],
        "ShuffleConfig": NotRequired[ShuffleConfigTypeDef],
    },
)


class ProcessingInputTypeDef(TypedDict):
    InputName: str
    AppManaged: NotRequired[bool]
    S3Input: NotRequired[ProcessingS3InputTypeDef]
    DatasetDefinition: NotRequired[DatasetDefinitionTypeDef]


InferenceComponentSpecificationSummaryTypeDef = TypedDict(
    "InferenceComponentSpecificationSummaryTypeDef",
    {
        "ModelName": NotRequired[str],
        "Container": NotRequired[InferenceComponentContainerSpecificationSummaryTypeDef],
        "StartupParameters": NotRequired[InferenceComponentStartupParametersTypeDef],
        "ComputeResourceRequirements": NotRequired[
            InferenceComponentComputeResourceRequirementsTypeDef
        ],
        "BaseInferenceComponentName": NotRequired[str],
    },
)


class DescribeEdgeDeploymentPlanResponseTypeDef(TypedDict):
    EdgeDeploymentPlanArn: str
    EdgeDeploymentPlanName: str
    ModelConfigs: List[EdgeDeploymentModelConfigTypeDef]
    DeviceFleetName: str
    EdgeDeploymentSuccess: int
    EdgeDeploymentPending: int
    EdgeDeploymentFailed: int
    Stages: List[DeploymentStageStatusSummaryTypeDef]
    CreationTime: datetime
    LastModifiedTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListExperimentsResponseTypeDef(TypedDict):
    ExperimentSummaries: List[ExperimentSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListFeatureGroupsResponseTypeDef(TypedDict):
    FeatureGroupSummaries: List[FeatureGroupSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListInferenceExperimentsResponseTypeDef(TypedDict):
    InferenceExperiments: List[InferenceExperimentSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListTrainingJobsResponseTypeDef(TypedDict):
    TrainingJobSummaries: List[TrainingJobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListTrialsResponseTypeDef(TypedDict):
    TrialSummaries: List[TrialSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class UpdateEndpointWeightsAndCapacitiesInputRequestTypeDef(TypedDict):
    EndpointName: str
    DesiredWeightsAndCapacities: Sequence[DesiredWeightAndCapacityTypeDef]


class DeploymentStageTypeDef(TypedDict):
    StageName: str
    DeviceSelectionConfig: DeviceSelectionConfigUnionTypeDef
    DeploymentConfig: NotRequired[EdgeDeploymentConfigTypeDef]


class ListDevicesResponseTypeDef(TypedDict):
    DeviceSummaries: List[DeviceSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DomainSettingsForUpdateTypeDef(TypedDict):
    RStudioServerProDomainSettingsForUpdate: NotRequired[
        RStudioServerProDomainSettingsForUpdateTypeDef
    ]
    ExecutionRoleIdentityConfig: NotRequired[ExecutionRoleIdentityConfigType]
    SecurityGroupIds: NotRequired[Sequence[str]]
    DockerSettings: NotRequired[DockerSettingsUnionTypeDef]
    AmazonQSettings: NotRequired[AmazonQSettingsTypeDef]


class DomainSettingsTypeDef(TypedDict):
    SecurityGroupIds: NotRequired[Sequence[str]]
    RStudioServerProDomainSettings: NotRequired[RStudioServerProDomainSettingsTypeDef]
    ExecutionRoleIdentityConfig: NotRequired[ExecutionRoleIdentityConfigType]
    DockerSettings: NotRequired[DockerSettingsUnionTypeDef]
    AmazonQSettings: NotRequired[AmazonQSettingsTypeDef]


class DriftCheckBaselinesTypeDef(TypedDict):
    Bias: NotRequired[DriftCheckBiasTypeDef]
    Explainability: NotRequired[DriftCheckExplainabilityTypeDef]
    ModelQuality: NotRequired[DriftCheckModelQualityTypeDef]
    ModelDataQuality: NotRequired[DriftCheckModelDataQualityTypeDef]


class SpaceSettingsSummaryTypeDef(TypedDict):
    AppType: NotRequired[AppTypeType]
    SpaceStorageSettings: NotRequired[SpaceStorageSettingsTypeDef]


class JupyterLabAppSettingsTypeDef(TypedDict):
    DefaultResourceSpec: NotRequired[ResourceSpecTypeDef]
    CustomImages: NotRequired[Sequence[CustomImageTypeDef]]
    LifecycleConfigArns: NotRequired[Sequence[str]]
    CodeRepositories: NotRequired[Sequence[CodeRepositoryTypeDef]]
    AppLifecycleManagement: NotRequired[AppLifecycleManagementTypeDef]
    EmrSettings: NotRequired[EmrSettingsUnionTypeDef]
    BuiltInLifecycleConfigArn: NotRequired[str]


class InferenceRecommendationTypeDef(TypedDict):
    EndpointConfiguration: EndpointOutputConfigurationTypeDef
    ModelConfiguration: ModelConfigurationTypeDef
    RecommendationId: NotRequired[str]
    Metrics: NotRequired[RecommendationMetricsTypeDef]
    InvocationEndTime: NotRequired[datetime]
    InvocationStartTime: NotRequired[datetime]


class RecommendationJobInferenceBenchmarkTypeDef(TypedDict):
    ModelConfiguration: ModelConfigurationTypeDef
    Metrics: NotRequired[RecommendationMetricsTypeDef]
    EndpointMetrics: NotRequired[InferenceMetricsTypeDef]
    EndpointConfiguration: NotRequired[EndpointOutputConfigurationTypeDef]
    FailureReason: NotRequired[str]
    InvocationEndTime: NotRequired[datetime]
    InvocationStartTime: NotRequired[datetime]


class SearchExpressionPaginatorTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    NestedFilters: NotRequired[Sequence[NestedFiltersTypeDef]]
    SubExpressions: NotRequired[Sequence[Mapping[str, Any]]]
    Operator: NotRequired[BooleanOperatorType]


class SearchExpressionTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    NestedFilters: NotRequired[Sequence[NestedFiltersTypeDef]]
    SubExpressions: NotRequired[Sequence[Mapping[str, Any]]]
    Operator: NotRequired[BooleanOperatorType]


class ListTrainingJobsForHyperParameterTuningJobResponseTypeDef(TypedDict):
    TrainingJobSummaries: List[HyperParameterTrainingJobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class StudioWebPortalSettingsTypeDef(TypedDict):
    HiddenMlTools: NotRequired[Sequence[MlToolsType]]
    HiddenAppTypes: NotRequired[Sequence[AppTypeType]]
    HiddenInstanceTypes: NotRequired[Sequence[AppInstanceTypeType]]
    HiddenSageMakerImageVersionAliases: NotRequired[Sequence[HiddenSageMakerImageUnionTypeDef]]


HyperParameterTuningResourceConfigUnionTypeDef = Union[
    HyperParameterTuningResourceConfigTypeDef, HyperParameterTuningResourceConfigOutputTypeDef
]


class ListHyperParameterTuningJobsResponseTypeDef(TypedDict):
    HyperParameterTuningJobSummaries: List[HyperParameterTuningJobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class AssociationSummaryTypeDef(TypedDict):
    SourceArn: NotRequired[str]
    DestinationArn: NotRequired[str]
    SourceType: NotRequired[str]
    DestinationType: NotRequired[str]
    AssociationType: NotRequired[AssociationEdgeTypeType]
    SourceName: NotRequired[str]
    DestinationName: NotRequired[str]
    CreationTime: NotRequired[datetime]
    CreatedBy: NotRequired[UserContextTypeDef]


class DescribeActionResponseTypeDef(TypedDict):
    ActionName: str
    ActionArn: str
    Source: ActionSourceTypeDef
    ActionType: str
    Description: str
    Status: ActionStatusType
    Properties: Dict[str, str]
    CreationTime: datetime
    CreatedBy: UserContextTypeDef
    LastModifiedTime: datetime
    LastModifiedBy: UserContextTypeDef
    MetadataProperties: MetadataPropertiesTypeDef
    LineageGroupArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeArtifactResponseTypeDef(TypedDict):
    ArtifactName: str
    ArtifactArn: str
    Source: ArtifactSourceOutputTypeDef
    ArtifactType: str
    Properties: Dict[str, str]
    CreationTime: datetime
    CreatedBy: UserContextTypeDef
    LastModifiedTime: datetime
    LastModifiedBy: UserContextTypeDef
    MetadataProperties: MetadataPropertiesTypeDef
    LineageGroupArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeContextResponseTypeDef(TypedDict):
    ContextName: str
    ContextArn: str
    Source: ContextSourceTypeDef
    ContextType: str
    Description: str
    Properties: Dict[str, str]
    CreationTime: datetime
    CreatedBy: UserContextTypeDef
    LastModifiedTime: datetime
    LastModifiedBy: UserContextTypeDef
    LineageGroupArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeExperimentResponseTypeDef(TypedDict):
    ExperimentName: str
    ExperimentArn: str
    DisplayName: str
    Source: ExperimentSourceTypeDef
    Description: str
    CreationTime: datetime
    CreatedBy: UserContextTypeDef
    LastModifiedTime: datetime
    LastModifiedBy: UserContextTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeLineageGroupResponseTypeDef(TypedDict):
    LineageGroupName: str
    LineageGroupArn: str
    DisplayName: str
    Description: str
    CreationTime: datetime
    CreatedBy: UserContextTypeDef
    LastModifiedTime: datetime
    LastModifiedBy: UserContextTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeMlflowTrackingServerResponseTypeDef(TypedDict):
    TrackingServerArn: str
    TrackingServerName: str
    ArtifactStoreUri: str
    TrackingServerSize: TrackingServerSizeType
    MlflowVersion: str
    RoleArn: str
    TrackingServerStatus: TrackingServerStatusType
    IsActive: IsTrackingServerActiveType
    TrackingServerUrl: str
    WeeklyMaintenanceWindowStart: str
    AutomaticModelRegistration: bool
    CreationTime: datetime
    CreatedBy: UserContextTypeDef
    LastModifiedTime: datetime
    LastModifiedBy: UserContextTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeModelCardResponseTypeDef(TypedDict):
    ModelCardArn: str
    ModelCardName: str
    ModelCardVersion: int
    Content: str
    ModelCardStatus: ModelCardStatusType
    SecurityConfig: ModelCardSecurityConfigTypeDef
    CreationTime: datetime
    CreatedBy: UserContextTypeDef
    LastModifiedTime: datetime
    LastModifiedBy: UserContextTypeDef
    ModelCardProcessingStatus: ModelCardProcessingStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeModelPackageGroupOutputTypeDef(TypedDict):
    ModelPackageGroupName: str
    ModelPackageGroupArn: str
    ModelPackageGroupDescription: str
    CreationTime: datetime
    CreatedBy: UserContextTypeDef
    ModelPackageGroupStatus: ModelPackageGroupStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class DescribePipelineResponseTypeDef(TypedDict):
    PipelineArn: str
    PipelineName: str
    PipelineDisplayName: str
    PipelineDefinition: str
    PipelineDescription: str
    RoleArn: str
    PipelineStatus: PipelineStatusType
    CreationTime: datetime
    LastModifiedTime: datetime
    LastRunTime: datetime
    CreatedBy: UserContextTypeDef
    LastModifiedBy: UserContextTypeDef
    ParallelismConfiguration: ParallelismConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeTrialComponentResponseTypeDef(TypedDict):
    TrialComponentName: str
    TrialComponentArn: str
    DisplayName: str
    Source: TrialComponentSourceTypeDef
    Status: TrialComponentStatusTypeDef
    StartTime: datetime
    EndTime: datetime
    CreationTime: datetime
    CreatedBy: UserContextTypeDef
    LastModifiedTime: datetime
    LastModifiedBy: UserContextTypeDef
    Parameters: Dict[str, TrialComponentParameterValueTypeDef]
    InputArtifacts: Dict[str, TrialComponentArtifactTypeDef]
    OutputArtifacts: Dict[str, TrialComponentArtifactTypeDef]
    MetadataProperties: MetadataPropertiesTypeDef
    Metrics: List[TrialComponentMetricSummaryTypeDef]
    LineageGroupArn: str
    Sources: List[TrialComponentSourceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeTrialResponseTypeDef(TypedDict):
    TrialName: str
    TrialArn: str
    DisplayName: str
    ExperimentName: str
    Source: TrialSourceTypeDef
    CreationTime: datetime
    CreatedBy: UserContextTypeDef
    LastModifiedTime: datetime
    LastModifiedBy: UserContextTypeDef
    MetadataProperties: MetadataPropertiesTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ExperimentTypeDef(TypedDict):
    ExperimentName: NotRequired[str]
    ExperimentArn: NotRequired[str]
    DisplayName: NotRequired[str]
    Source: NotRequired[ExperimentSourceTypeDef]
    Description: NotRequired[str]
    CreationTime: NotRequired[datetime]
    CreatedBy: NotRequired[UserContextTypeDef]
    LastModifiedTime: NotRequired[datetime]
    LastModifiedBy: NotRequired[UserContextTypeDef]
    Tags: NotRequired[List[TagTypeDef]]


class ModelCardTypeDef(TypedDict):
    ModelCardArn: NotRequired[str]
    ModelCardName: NotRequired[str]
    ModelCardVersion: NotRequired[int]
    Content: NotRequired[str]
    ModelCardStatus: NotRequired[ModelCardStatusType]
    SecurityConfig: NotRequired[ModelCardSecurityConfigTypeDef]
    CreationTime: NotRequired[datetime]
    CreatedBy: NotRequired[UserContextTypeDef]
    LastModifiedTime: NotRequired[datetime]
    LastModifiedBy: NotRequired[UserContextTypeDef]
    Tags: NotRequired[List[TagTypeDef]]
    ModelId: NotRequired[str]
    RiskRating: NotRequired[str]
    ModelPackageGroupName: NotRequired[str]


class ModelDashboardModelCardTypeDef(TypedDict):
    ModelCardArn: NotRequired[str]
    ModelCardName: NotRequired[str]
    ModelCardVersion: NotRequired[int]
    ModelCardStatus: NotRequired[ModelCardStatusType]
    SecurityConfig: NotRequired[ModelCardSecurityConfigTypeDef]
    CreationTime: NotRequired[datetime]
    CreatedBy: NotRequired[UserContextTypeDef]
    LastModifiedTime: NotRequired[datetime]
    LastModifiedBy: NotRequired[UserContextTypeDef]
    Tags: NotRequired[List[TagTypeDef]]
    ModelId: NotRequired[str]
    RiskRating: NotRequired[str]


class ModelPackageGroupTypeDef(TypedDict):
    ModelPackageGroupName: NotRequired[str]
    ModelPackageGroupArn: NotRequired[str]
    ModelPackageGroupDescription: NotRequired[str]
    CreationTime: NotRequired[datetime]
    CreatedBy: NotRequired[UserContextTypeDef]
    ModelPackageGroupStatus: NotRequired[ModelPackageGroupStatusType]
    Tags: NotRequired[List[TagTypeDef]]


class PipelineTypeDef(TypedDict):
    PipelineArn: NotRequired[str]
    PipelineName: NotRequired[str]
    PipelineDisplayName: NotRequired[str]
    PipelineDescription: NotRequired[str]
    RoleArn: NotRequired[str]
    PipelineStatus: NotRequired[PipelineStatusType]
    CreationTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]
    LastRunTime: NotRequired[datetime]
    CreatedBy: NotRequired[UserContextTypeDef]
    LastModifiedBy: NotRequired[UserContextTypeDef]
    ParallelismConfiguration: NotRequired[ParallelismConfigurationTypeDef]
    Tags: NotRequired[List[TagTypeDef]]


class TrialComponentSimpleSummaryTypeDef(TypedDict):
    TrialComponentName: NotRequired[str]
    TrialComponentArn: NotRequired[str]
    TrialComponentSource: NotRequired[TrialComponentSourceTypeDef]
    CreationTime: NotRequired[datetime]
    CreatedBy: NotRequired[UserContextTypeDef]


class TrialComponentSummaryTypeDef(TypedDict):
    TrialComponentName: NotRequired[str]
    TrialComponentArn: NotRequired[str]
    DisplayName: NotRequired[str]
    TrialComponentSource: NotRequired[TrialComponentSourceTypeDef]
    Status: NotRequired[TrialComponentStatusTypeDef]
    StartTime: NotRequired[datetime]
    EndTime: NotRequired[datetime]
    CreationTime: NotRequired[datetime]
    CreatedBy: NotRequired[UserContextTypeDef]
    LastModifiedTime: NotRequired[datetime]
    LastModifiedBy: NotRequired[UserContextTypeDef]


class WorkerAccessConfigurationTypeDef(TypedDict):
    S3Presign: NotRequired[S3PresignTypeDef]


class CreateInferenceComponentInputRequestTypeDef(TypedDict):
    InferenceComponentName: str
    EndpointName: str
    Specification: InferenceComponentSpecificationTypeDef
    VariantName: NotRequired[str]
    RuntimeConfig: NotRequired[InferenceComponentRuntimeConfigTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]


class UpdateInferenceComponentInputRequestTypeDef(TypedDict):
    InferenceComponentName: str
    Specification: NotRequired[InferenceComponentSpecificationTypeDef]
    RuntimeConfig: NotRequired[InferenceComponentRuntimeConfigTypeDef]


ResourceConfigUnionTypeDef = Union[ResourceConfigTypeDef, ResourceConfigOutputTypeDef]
HyperParameterSpecificationOutputTypeDef = TypedDict(
    "HyperParameterSpecificationOutputTypeDef",
    {
        "Name": str,
        "Type": ParameterTypeType,
        "Description": NotRequired[str],
        "Range": NotRequired[ParameterRangeOutputTypeDef],
        "IsTunable": NotRequired[bool],
        "IsRequired": NotRequired[bool],
        "DefaultValue": NotRequired[str],
    },
)


class HyperParameterTuningJobConfigOutputTypeDef(TypedDict):
    Strategy: HyperParameterTuningJobStrategyTypeType
    ResourceLimits: ResourceLimitsTypeDef
    StrategyConfig: NotRequired[HyperParameterTuningJobStrategyConfigTypeDef]
    HyperParameterTuningJobObjective: NotRequired[HyperParameterTuningJobObjectiveTypeDef]
    ParameterRanges: NotRequired[ParameterRangesOutputTypeDef]
    TrainingJobEarlyStoppingType: NotRequired[TrainingJobEarlyStoppingTypeType]
    TuningJobCompletionCriteria: NotRequired[TuningJobCompletionCriteriaTypeDef]
    RandomSeed: NotRequired[int]


class AppImageConfigDetailsTypeDef(TypedDict):
    AppImageConfigArn: NotRequired[str]
    AppImageConfigName: NotRequired[str]
    CreationTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]
    KernelGatewayImageConfig: NotRequired[KernelGatewayImageConfigOutputTypeDef]
    JupyterLabAppImageConfig: NotRequired[JupyterLabAppImageConfigOutputTypeDef]
    CodeEditorAppImageConfig: NotRequired[CodeEditorAppImageConfigOutputTypeDef]


class DescribeAppImageConfigResponseTypeDef(TypedDict):
    AppImageConfigArn: str
    AppImageConfigName: str
    CreationTime: datetime
    LastModifiedTime: datetime
    KernelGatewayImageConfig: KernelGatewayImageConfigOutputTypeDef
    JupyterLabAppImageConfig: JupyterLabAppImageConfigOutputTypeDef
    CodeEditorAppImageConfig: CodeEditorAppImageConfigOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListLabelingJobsForWorkteamResponseTypeDef(TypedDict):
    LabelingJobSummaryList: List[LabelingJobForWorkteamSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class LabelingJobInputConfigOutputTypeDef(TypedDict):
    DataSource: LabelingJobDataSourceTypeDef
    DataAttributes: NotRequired[LabelingJobDataAttributesOutputTypeDef]


class LabelingJobInputConfigTypeDef(TypedDict):
    DataSource: LabelingJobDataSourceTypeDef
    DataAttributes: NotRequired[LabelingJobDataAttributesUnionTypeDef]


class TargetTrackingScalingPolicyConfigurationTypeDef(TypedDict):
    MetricSpecification: NotRequired[MetricSpecificationTypeDef]
    TargetValue: NotRequired[float]


class AdditionalModelDataSourceTypeDef(TypedDict):
    ChannelName: str
    S3DataSource: S3ModelDataSourceTypeDef


class ModelDataSourceTypeDef(TypedDict):
    S3DataSource: NotRequired[S3ModelDataSourceTypeDef]


TextGenerationJobConfigUnionTypeDef = Union[
    TextGenerationJobConfigTypeDef, TextGenerationJobConfigOutputTypeDef
]


class MonitoringAlertSummaryTypeDef(TypedDict):
    MonitoringAlertName: str
    CreationTime: datetime
    LastModifiedTime: datetime
    AlertStatus: MonitoringAlertStatusType
    DatapointsToAlert: int
    EvaluationPeriod: int
    Actions: MonitoringAlertActionsTypeDef


class ModelVariantConfigSummaryTypeDef(TypedDict):
    ModelName: str
    VariantName: str
    InfrastructureConfig: ModelInfrastructureConfigTypeDef
    Status: ModelVariantStatusType


class ModelVariantConfigTypeDef(TypedDict):
    ModelName: str
    VariantName: str
    InfrastructureConfig: ModelInfrastructureConfigTypeDef


class ListModelMetadataRequestListModelMetadataPaginateTypeDef(TypedDict):
    SearchExpression: NotRequired[ModelMetadataSearchExpressionTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListModelMetadataRequestRequestTypeDef(TypedDict):
    SearchExpression: NotRequired[ModelMetadataSearchExpressionTypeDef]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class OptimizationConfigTypeDef(TypedDict):
    ModelQuantizationConfig: NotRequired[ModelQuantizationConfigUnionTypeDef]
    ModelCompilationConfig: NotRequired[ModelCompilationConfigUnionTypeDef]
    ModelShardingConfig: NotRequired[ModelShardingConfigUnionTypeDef]


BatchTransformInputOutputTypeDef = TypedDict(
    "BatchTransformInputOutputTypeDef",
    {
        "DataCapturedDestinationS3Uri": str,
        "DatasetFormat": MonitoringDatasetFormatOutputTypeDef,
        "LocalPath": str,
        "S3InputMode": NotRequired[ProcessingS3InputModeType],
        "S3DataDistributionType": NotRequired[ProcessingS3DataDistributionTypeType],
        "FeaturesAttribute": NotRequired[str],
        "InferenceAttribute": NotRequired[str],
        "ProbabilityAttribute": NotRequired[str],
        "ProbabilityThresholdAttribute": NotRequired[float],
        "StartTimeOffset": NotRequired[str],
        "EndTimeOffset": NotRequired[str],
        "ExcludeFeaturesAttribute": NotRequired[str],
    },
)
MonitoringDatasetFormatUnionTypeDef = Union[
    MonitoringDatasetFormatTypeDef, MonitoringDatasetFormatOutputTypeDef
]


class MonitoringOutputConfigOutputTypeDef(TypedDict):
    MonitoringOutputs: List[MonitoringOutputTypeDef]
    KmsKeyId: NotRequired[str]


class MonitoringOutputConfigTypeDef(TypedDict):
    MonitoringOutputs: Sequence[MonitoringOutputTypeDef]
    KmsKeyId: NotRequired[str]


class MemberDefinitionTypeDef(TypedDict):
    CognitoMemberDefinition: NotRequired[CognitoMemberDefinitionTypeDef]
    OidcMemberDefinition: NotRequired[OidcMemberDefinitionUnionTypeDef]


class OptimizationJobModelSourceTypeDef(TypedDict):
    S3: NotRequired[OptimizationJobModelSourceS3TypeDef]


class CreateCompilationJobRequestRequestTypeDef(TypedDict):
    CompilationJobName: str
    RoleArn: str
    OutputConfig: OutputConfigTypeDef
    StoppingCondition: StoppingConditionTypeDef
    ModelPackageVersionArn: NotRequired[str]
    InputConfig: NotRequired[InputConfigTypeDef]
    VpcConfig: NotRequired[NeoVpcConfigTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]


class DescribeCompilationJobResponseTypeDef(TypedDict):
    CompilationJobName: str
    CompilationJobArn: str
    CompilationJobStatus: CompilationJobStatusType
    CompilationStartTime: datetime
    CompilationEndTime: datetime
    StoppingCondition: StoppingConditionTypeDef
    InferenceImage: str
    ModelPackageVersionArn: str
    CreationTime: datetime
    LastModifiedTime: datetime
    FailureReason: str
    ModelArtifacts: ModelArtifactsTypeDef
    ModelDigests: ModelDigestsTypeDef
    RoleArn: str
    InputConfig: InputConfigTypeDef
    OutputConfig: OutputConfigTypeDef
    VpcConfig: NeoVpcConfigOutputTypeDef
    DerivedInformation: DerivedInformationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class PendingDeploymentSummaryTypeDef(TypedDict):
    EndpointConfigName: str
    ProductionVariants: NotRequired[List[PendingProductionVariantSummaryTypeDef]]
    StartTime: NotRequired[datetime]
    ShadowProductionVariants: NotRequired[List[PendingProductionVariantSummaryTypeDef]]


class ProcessingOutputConfigOutputTypeDef(TypedDict):
    Outputs: List[ProcessingOutputTypeDef]
    KmsKeyId: NotRequired[str]


class ProcessingOutputConfigTypeDef(TypedDict):
    Outputs: Sequence[ProcessingOutputTypeDef]
    KmsKeyId: NotRequired[str]


class GetSearchSuggestionsRequestRequestTypeDef(TypedDict):
    Resource: ResourceTypeType
    SuggestionQuery: NotRequired[SuggestionQueryTypeDef]


class DescribeProjectOutputTypeDef(TypedDict):
    ProjectArn: str
    ProjectName: str
    ProjectId: str
    ProjectDescription: str
    ServiceCatalogProvisioningDetails: ServiceCatalogProvisioningDetailsOutputTypeDef
    ServiceCatalogProvisionedProductDetails: ServiceCatalogProvisionedProductDetailsTypeDef
    ProjectStatus: ProjectStatusType
    CreatedBy: UserContextTypeDef
    CreationTime: datetime
    LastModifiedTime: datetime
    LastModifiedBy: UserContextTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ProjectTypeDef(TypedDict):
    ProjectArn: NotRequired[str]
    ProjectName: NotRequired[str]
    ProjectId: NotRequired[str]
    ProjectDescription: NotRequired[str]
    ServiceCatalogProvisioningDetails: NotRequired[ServiceCatalogProvisioningDetailsOutputTypeDef]
    ServiceCatalogProvisionedProductDetails: NotRequired[
        ServiceCatalogProvisionedProductDetailsTypeDef
    ]
    ProjectStatus: NotRequired[ProjectStatusType]
    CreatedBy: NotRequired[UserContextTypeDef]
    CreationTime: NotRequired[datetime]
    Tags: NotRequired[List[TagTypeDef]]
    LastModifiedTime: NotRequired[datetime]
    LastModifiedBy: NotRequired[UserContextTypeDef]


class CreateProjectInputRequestTypeDef(TypedDict):
    ProjectName: str
    ServiceCatalogProvisioningDetails: ServiceCatalogProvisioningDetailsTypeDef
    ProjectDescription: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]


class UpdateProjectInputRequestTypeDef(TypedDict):
    ProjectName: str
    ProjectDescription: NotRequired[str]
    ServiceCatalogProvisioningUpdateDetails: NotRequired[
        ServiceCatalogProvisioningUpdateDetailsTypeDef
    ]
    Tags: NotRequired[Sequence[TagTypeDef]]


class HumanLoopConfigOutputTypeDef(TypedDict):
    WorkteamArn: str
    HumanTaskUiArn: str
    TaskTitle: str
    TaskDescription: str
    TaskCount: int
    TaskAvailabilityLifetimeInSeconds: NotRequired[int]
    TaskTimeLimitInSeconds: NotRequired[int]
    TaskKeywords: NotRequired[List[str]]
    PublicWorkforceTaskPrice: NotRequired[PublicWorkforceTaskPriceTypeDef]


class HumanLoopConfigTypeDef(TypedDict):
    WorkteamArn: str
    HumanTaskUiArn: str
    TaskTitle: str
    TaskDescription: str
    TaskCount: int
    TaskAvailabilityLifetimeInSeconds: NotRequired[int]
    TaskTimeLimitInSeconds: NotRequired[int]
    TaskKeywords: NotRequired[Sequence[str]]
    PublicWorkforceTaskPrice: NotRequired[PublicWorkforceTaskPriceTypeDef]


class HumanTaskConfigOutputTypeDef(TypedDict):
    WorkteamArn: str
    UiConfig: UiConfigTypeDef
    TaskTitle: str
    TaskDescription: str
    NumberOfHumanWorkersPerDataObject: int
    TaskTimeLimitInSeconds: int
    PreHumanTaskLambdaArn: NotRequired[str]
    TaskKeywords: NotRequired[List[str]]
    TaskAvailabilityLifetimeInSeconds: NotRequired[int]
    MaxConcurrentTaskCount: NotRequired[int]
    AnnotationConsolidationConfig: NotRequired[AnnotationConsolidationConfigTypeDef]
    PublicWorkforceTaskPrice: NotRequired[PublicWorkforceTaskPriceTypeDef]


class HumanTaskConfigTypeDef(TypedDict):
    WorkteamArn: str
    UiConfig: UiConfigTypeDef
    TaskTitle: str
    TaskDescription: str
    NumberOfHumanWorkersPerDataObject: int
    TaskTimeLimitInSeconds: int
    PreHumanTaskLambdaArn: NotRequired[str]
    TaskKeywords: NotRequired[Sequence[str]]
    TaskAvailabilityLifetimeInSeconds: NotRequired[int]
    MaxConcurrentTaskCount: NotRequired[int]
    AnnotationConsolidationConfig: NotRequired[AnnotationConsolidationConfigTypeDef]
    PublicWorkforceTaskPrice: NotRequired[PublicWorkforceTaskPriceTypeDef]


class RecommendationJobContainerConfigTypeDef(TypedDict):
    Domain: NotRequired[str]
    Task: NotRequired[str]
    Framework: NotRequired[str]
    FrameworkVersion: NotRequired[str]
    PayloadConfig: NotRequired[RecommendationJobPayloadConfigUnionTypeDef]
    NearestModelName: NotRequired[str]
    SupportedInstanceTypes: NotRequired[Sequence[str]]
    SupportedEndpointType: NotRequired[RecommendationJobSupportedEndpointTypeType]
    DataInputConfig: NotRequired[str]
    SupportedResponseMIMETypes: NotRequired[Sequence[str]]


class DataSourceTypeDef(TypedDict):
    S3DataSource: NotRequired[S3DataSourceUnionTypeDef]
    FileSystemDataSource: NotRequired[FileSystemDataSourceTypeDef]


class DescribePipelineExecutionResponseTypeDef(TypedDict):
    PipelineArn: str
    PipelineExecutionArn: str
    PipelineExecutionDisplayName: str
    PipelineExecutionStatus: PipelineExecutionStatusType
    PipelineExecutionDescription: str
    PipelineExperimentConfig: PipelineExperimentConfigTypeDef
    FailureReason: str
    CreationTime: datetime
    LastModifiedTime: datetime
    CreatedBy: UserContextTypeDef
    LastModifiedBy: UserContextTypeDef
    ParallelismConfiguration: ParallelismConfigurationTypeDef
    SelectiveExecutionConfig: SelectiveExecutionConfigOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class PipelineExecutionTypeDef(TypedDict):
    PipelineArn: NotRequired[str]
    PipelineExecutionArn: NotRequired[str]
    PipelineExecutionDisplayName: NotRequired[str]
    PipelineExecutionStatus: NotRequired[PipelineExecutionStatusType]
    PipelineExecutionDescription: NotRequired[str]
    PipelineExperimentConfig: NotRequired[PipelineExperimentConfigTypeDef]
    FailureReason: NotRequired[str]
    CreationTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]
    CreatedBy: NotRequired[UserContextTypeDef]
    LastModifiedBy: NotRequired[UserContextTypeDef]
    ParallelismConfiguration: NotRequired[ParallelismConfigurationTypeDef]
    SelectiveExecutionConfig: NotRequired[SelectiveExecutionConfigOutputTypeDef]
    PipelineParameters: NotRequired[List[ParameterTypeDef]]


class StartPipelineExecutionRequestRequestTypeDef(TypedDict):
    PipelineName: str
    ClientRequestToken: str
    PipelineExecutionDisplayName: NotRequired[str]
    PipelineParameters: NotRequired[Sequence[ParameterTypeDef]]
    PipelineExecutionDescription: NotRequired[str]
    ParallelismConfiguration: NotRequired[ParallelismConfigurationTypeDef]
    SelectiveExecutionConfig: NotRequired[SelectiveExecutionConfigTypeDef]


class SpaceCodeEditorAppSettingsTypeDef(TypedDict):
    DefaultResourceSpec: NotRequired[ResourceSpecTypeDef]
    AppLifecycleManagement: NotRequired[SpaceAppLifecycleManagementTypeDef]


class SpaceJupyterLabAppSettingsOutputTypeDef(TypedDict):
    DefaultResourceSpec: NotRequired[ResourceSpecTypeDef]
    CodeRepositories: NotRequired[List[CodeRepositoryTypeDef]]
    AppLifecycleManagement: NotRequired[SpaceAppLifecycleManagementTypeDef]


class SpaceJupyterLabAppSettingsTypeDef(TypedDict):
    DefaultResourceSpec: NotRequired[ResourceSpecTypeDef]
    CodeRepositories: NotRequired[Sequence[CodeRepositoryTypeDef]]
    AppLifecycleManagement: NotRequired[SpaceAppLifecycleManagementTypeDef]


TrafficPatternUnionTypeDef = Union[TrafficPatternTypeDef, TrafficPatternOutputTypeDef]


class AlgorithmSpecificationOutputTypeDef(TypedDict):
    TrainingInputMode: TrainingInputModeType
    TrainingImage: NotRequired[str]
    AlgorithmName: NotRequired[str]
    MetricDefinitions: NotRequired[List[MetricDefinitionTypeDef]]
    EnableSageMakerMetricsTimeSeries: NotRequired[bool]
    ContainerEntrypoint: NotRequired[List[str]]
    ContainerArguments: NotRequired[List[str]]
    TrainingImageConfig: NotRequired[TrainingImageConfigTypeDef]


class AlgorithmSpecificationTypeDef(TypedDict):
    TrainingInputMode: TrainingInputModeType
    TrainingImage: NotRequired[str]
    AlgorithmName: NotRequired[str]
    MetricDefinitions: NotRequired[Sequence[MetricDefinitionTypeDef]]
    EnableSageMakerMetricsTimeSeries: NotRequired[bool]
    ContainerEntrypoint: NotRequired[Sequence[str]]
    ContainerArguments: NotRequired[Sequence[str]]
    TrainingImageConfig: NotRequired[TrainingImageConfigTypeDef]


class TransformInputTypeDef(TypedDict):
    DataSource: TransformDataSourceTypeDef
    ContentType: NotRequired[str]
    CompressionType: NotRequired[CompressionTypeType]
    SplitType: NotRequired[SplitTypeType]


class DescribeWorkforceResponseTypeDef(TypedDict):
    Workforce: WorkforceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListWorkforcesResponseTypeDef(TypedDict):
    Workforces: List[WorkforceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class UpdateWorkforceResponseTypeDef(TypedDict):
    Workforce: WorkforceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


CodeEditorAppSettingsUnionTypeDef = Union[
    CodeEditorAppSettingsTypeDef, CodeEditorAppSettingsOutputTypeDef
]


class DefaultSpaceSettingsOutputTypeDef(TypedDict):
    ExecutionRole: NotRequired[str]
    SecurityGroups: NotRequired[List[str]]
    JupyterServerAppSettings: NotRequired[JupyterServerAppSettingsOutputTypeDef]
    KernelGatewayAppSettings: NotRequired[KernelGatewayAppSettingsOutputTypeDef]
    JupyterLabAppSettings: NotRequired[JupyterLabAppSettingsOutputTypeDef]
    SpaceStorageSettings: NotRequired[DefaultSpaceStorageSettingsTypeDef]
    CustomPosixUserConfig: NotRequired[CustomPosixUserConfigTypeDef]
    CustomFileSystemConfigs: NotRequired[List[CustomFileSystemConfigTypeDef]]


class UserSettingsOutputTypeDef(TypedDict):
    ExecutionRole: NotRequired[str]
    SecurityGroups: NotRequired[List[str]]
    SharingSettings: NotRequired[SharingSettingsTypeDef]
    JupyterServerAppSettings: NotRequired[JupyterServerAppSettingsOutputTypeDef]
    KernelGatewayAppSettings: NotRequired[KernelGatewayAppSettingsOutputTypeDef]
    TensorBoardAppSettings: NotRequired[TensorBoardAppSettingsTypeDef]
    RStudioServerProAppSettings: NotRequired[RStudioServerProAppSettingsTypeDef]
    RSessionAppSettings: NotRequired[RSessionAppSettingsOutputTypeDef]
    CanvasAppSettings: NotRequired[CanvasAppSettingsOutputTypeDef]
    CodeEditorAppSettings: NotRequired[CodeEditorAppSettingsOutputTypeDef]
    JupyterLabAppSettings: NotRequired[JupyterLabAppSettingsOutputTypeDef]
    SpaceStorageSettings: NotRequired[DefaultSpaceStorageSettingsTypeDef]
    DefaultLandingUri: NotRequired[str]
    StudioWebPortal: NotRequired[StudioWebPortalType]
    CustomPosixUserConfig: NotRequired[CustomPosixUserConfigTypeDef]
    CustomFileSystemConfigs: NotRequired[List[CustomFileSystemConfigTypeDef]]
    StudioWebPortalSettings: NotRequired[StudioWebPortalSettingsOutputTypeDef]
    AutoMountHomeEFS: NotRequired[AutoMountHomeEFSType]


class ListArtifactsResponseTypeDef(TypedDict):
    ArtifactSummaries: List[ArtifactSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


AsyncInferenceOutputConfigUnionTypeDef = Union[
    AsyncInferenceOutputConfigTypeDef, AsyncInferenceOutputConfigOutputTypeDef
]


class AutoMLProblemTypeConfigOutputTypeDef(TypedDict):
    ImageClassificationJobConfig: NotRequired[ImageClassificationJobConfigTypeDef]
    TextClassificationJobConfig: NotRequired[TextClassificationJobConfigTypeDef]
    TimeSeriesForecastingJobConfig: NotRequired[TimeSeriesForecastingJobConfigOutputTypeDef]
    TabularJobConfig: NotRequired[TabularJobConfigOutputTypeDef]
    TextGenerationJobConfig: NotRequired[TextGenerationJobConfigOutputTypeDef]


AutoMLCandidateGenerationConfigUnionTypeDef = Union[
    AutoMLCandidateGenerationConfigTypeDef, AutoMLCandidateGenerationConfigOutputTypeDef
]
CandidateGenerationConfigUnionTypeDef = Union[
    CandidateGenerationConfigTypeDef, CandidateGenerationConfigOutputTypeDef
]


class PipelineExecutionStepTypeDef(TypedDict):
    StepName: NotRequired[str]
    StepDisplayName: NotRequired[str]
    StepDescription: NotRequired[str]
    StartTime: NotRequired[datetime]
    EndTime: NotRequired[datetime]
    StepStatus: NotRequired[StepStatusType]
    CacheHitResult: NotRequired[CacheHitResultTypeDef]
    FailureReason: NotRequired[str]
    Metadata: NotRequired[PipelineExecutionStepMetadataTypeDef]
    AttemptCount: NotRequired[int]
    SelectiveExecutionResult: NotRequired[SelectiveExecutionResultTypeDef]


class DescribeAutoMLJobResponseTypeDef(TypedDict):
    AutoMLJobName: str
    AutoMLJobArn: str
    InputDataConfig: List[AutoMLChannelTypeDef]
    OutputDataConfig: AutoMLOutputDataConfigTypeDef
    RoleArn: str
    AutoMLJobObjective: AutoMLJobObjectiveTypeDef
    ProblemType: ProblemTypeType
    AutoMLJobConfig: AutoMLJobConfigOutputTypeDef
    CreationTime: datetime
    EndTime: datetime
    LastModifiedTime: datetime
    FailureReason: str
    PartialFailureReasons: List[AutoMLPartialFailureReasonTypeDef]
    BestCandidate: AutoMLCandidateTypeDef
    AutoMLJobStatus: AutoMLJobStatusType
    AutoMLJobSecondaryStatus: AutoMLJobSecondaryStatusType
    GenerateCandidateDefinitionsOnly: bool
    AutoMLJobArtifacts: AutoMLJobArtifactsTypeDef
    ResolvedAttributes: ResolvedAttributesTypeDef
    ModelDeployConfig: ModelDeployConfigTypeDef
    ModelDeployResult: ModelDeployResultTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListCandidatesForAutoMLJobResponseTypeDef(TypedDict):
    Candidates: List[AutoMLCandidateTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DeploymentConfigOutputTypeDef(TypedDict):
    BlueGreenUpdatePolicy: NotRequired[BlueGreenUpdatePolicyTypeDef]
    RollingUpdatePolicy: NotRequired[RollingUpdatePolicyTypeDef]
    AutoRollbackConfiguration: NotRequired[AutoRollbackConfigOutputTypeDef]


class DeploymentConfigTypeDef(TypedDict):
    BlueGreenUpdatePolicy: NotRequired[BlueGreenUpdatePolicyTypeDef]
    RollingUpdatePolicy: NotRequired[RollingUpdatePolicyTypeDef]
    AutoRollbackConfiguration: NotRequired[AutoRollbackConfigUnionTypeDef]


class RecommendationJobInputConfigOutputTypeDef(TypedDict):
    ModelPackageVersionArn: NotRequired[str]
    ModelName: NotRequired[str]
    JobDurationInSeconds: NotRequired[int]
    TrafficPattern: NotRequired[TrafficPatternOutputTypeDef]
    ResourceLimit: NotRequired[RecommendationJobResourceLimitTypeDef]
    EndpointConfigurations: NotRequired[List[EndpointInputConfigurationOutputTypeDef]]
    VolumeKmsKeyId: NotRequired[str]
    ContainerConfig: NotRequired[RecommendationJobContainerConfigOutputTypeDef]
    Endpoints: NotRequired[List[EndpointInfoTypeDef]]
    VpcConfig: NotRequired[RecommendationJobVpcConfigOutputTypeDef]


ParameterRangeUnionTypeDef = Union[ParameterRangeTypeDef, ParameterRangeOutputTypeDef]
ParameterRangesUnionTypeDef = Union[ParameterRangesTypeDef, ParameterRangesOutputTypeDef]
EnvironmentParameterRangesUnionTypeDef = Union[
    EnvironmentParameterRangesTypeDef, EnvironmentParameterRangesOutputTypeDef
]


class ExplainerConfigOutputTypeDef(TypedDict):
    ClarifyExplainerConfig: NotRequired[ClarifyExplainerConfigOutputTypeDef]


ClarifyExplainerConfigUnionTypeDef = Union[
    ClarifyExplainerConfigTypeDef, ClarifyExplainerConfigOutputTypeDef
]


class DescribeClusterResponseTypeDef(TypedDict):
    ClusterArn: str
    ClusterName: str
    ClusterStatus: ClusterStatusType
    CreationTime: datetime
    FailureMessage: str
    InstanceGroups: List[ClusterInstanceGroupDetailsTypeDef]
    VpcConfig: VpcConfigOutputTypeDef
    Orchestrator: ClusterOrchestratorTypeDef
    NodeRecovery: ClusterNodeRecoveryType
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeClusterNodeResponseTypeDef(TypedDict):
    NodeDetails: ClusterNodeDetailsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateFeatureGroupRequestRequestTypeDef(TypedDict):
    FeatureGroupName: str
    RecordIdentifierFeatureName: str
    EventTimeFeatureName: str
    FeatureDefinitions: Sequence[FeatureDefinitionTypeDef]
    OnlineStoreConfig: NotRequired[OnlineStoreConfigTypeDef]
    OfflineStoreConfig: NotRequired[OfflineStoreConfigTypeDef]
    ThroughputConfig: NotRequired[ThroughputConfigTypeDef]
    RoleArn: NotRequired[str]
    Description: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]


class DescribeFeatureGroupResponseTypeDef(TypedDict):
    FeatureGroupArn: str
    FeatureGroupName: str
    RecordIdentifierFeatureName: str
    EventTimeFeatureName: str
    FeatureDefinitions: List[FeatureDefinitionTypeDef]
    CreationTime: datetime
    LastModifiedTime: datetime
    OnlineStoreConfig: OnlineStoreConfigTypeDef
    OfflineStoreConfig: OfflineStoreConfigTypeDef
    ThroughputConfig: ThroughputConfigDescriptionTypeDef
    RoleArn: str
    FeatureGroupStatus: FeatureGroupStatusType
    OfflineStoreStatus: OfflineStoreStatusTypeDef
    LastUpdateStatus: LastUpdateStatusTypeDef
    FailureReason: str
    Description: str
    NextToken: str
    OnlineStoreTotalSizeBytes: int
    ResponseMetadata: ResponseMetadataTypeDef


class FeatureGroupTypeDef(TypedDict):
    FeatureGroupArn: NotRequired[str]
    FeatureGroupName: NotRequired[str]
    RecordIdentifierFeatureName: NotRequired[str]
    EventTimeFeatureName: NotRequired[str]
    FeatureDefinitions: NotRequired[List[FeatureDefinitionTypeDef]]
    CreationTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]
    OnlineStoreConfig: NotRequired[OnlineStoreConfigTypeDef]
    OfflineStoreConfig: NotRequired[OfflineStoreConfigTypeDef]
    RoleArn: NotRequired[str]
    FeatureGroupStatus: NotRequired[FeatureGroupStatusType]
    OfflineStoreStatus: NotRequired[OfflineStoreStatusTypeDef]
    LastUpdateStatus: NotRequired[LastUpdateStatusTypeDef]
    FailureReason: NotRequired[str]
    Description: NotRequired[str]
    Tags: NotRequired[List[TagTypeDef]]


class UpdateFeatureGroupRequestRequestTypeDef(TypedDict):
    FeatureGroupName: str
    FeatureAdditions: NotRequired[Sequence[FeatureDefinitionTypeDef]]
    OnlineStoreConfig: NotRequired[OnlineStoreConfigUpdateTypeDef]
    ThroughputConfig: NotRequired[ThroughputConfigUpdateTypeDef]


class CreateAppImageConfigRequestRequestTypeDef(TypedDict):
    AppImageConfigName: str
    Tags: NotRequired[Sequence[TagTypeDef]]
    KernelGatewayImageConfig: NotRequired[KernelGatewayImageConfigTypeDef]
    JupyterLabAppImageConfig: NotRequired[JupyterLabAppImageConfigTypeDef]
    CodeEditorAppImageConfig: NotRequired[CodeEditorAppImageConfigTypeDef]


class UpdateAppImageConfigRequestRequestTypeDef(TypedDict):
    AppImageConfigName: str
    KernelGatewayImageConfig: NotRequired[KernelGatewayImageConfigTypeDef]
    JupyterLabAppImageConfig: NotRequired[JupyterLabAppImageConfigTypeDef]
    CodeEditorAppImageConfig: NotRequired[CodeEditorAppImageConfigTypeDef]


AutoMLSecurityConfigUnionTypeDef = Union[
    AutoMLSecurityConfigTypeDef, AutoMLSecurityConfigOutputTypeDef
]


class CreateClusterRequestRequestTypeDef(TypedDict):
    ClusterName: str
    InstanceGroups: Sequence[ClusterInstanceGroupSpecificationTypeDef]
    VpcConfig: NotRequired[VpcConfigTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]
    Orchestrator: NotRequired[ClusterOrchestratorTypeDef]
    NodeRecovery: NotRequired[ClusterNodeRecoveryType]


class UpdateClusterRequestRequestTypeDef(TypedDict):
    ClusterName: str
    InstanceGroups: Sequence[ClusterInstanceGroupSpecificationTypeDef]
    NodeRecovery: NotRequired[ClusterNodeRecoveryType]


LabelingJobResourceConfigUnionTypeDef = Union[
    LabelingJobResourceConfigTypeDef, LabelingJobResourceConfigOutputTypeDef
]
NetworkConfigUnionTypeDef = Union[NetworkConfigTypeDef, NetworkConfigOutputTypeDef]


class HyperParameterTrainingJobDefinitionOutputTypeDef(TypedDict):
    AlgorithmSpecification: HyperParameterAlgorithmSpecificationOutputTypeDef
    RoleArn: str
    OutputDataConfig: OutputDataConfigTypeDef
    StoppingCondition: StoppingConditionTypeDef
    DefinitionName: NotRequired[str]
    TuningObjective: NotRequired[HyperParameterTuningJobObjectiveTypeDef]
    HyperParameterRanges: NotRequired[ParameterRangesOutputTypeDef]
    StaticHyperParameters: NotRequired[Dict[str, str]]
    InputDataConfig: NotRequired[List[ChannelOutputTypeDef]]
    VpcConfig: NotRequired[VpcConfigOutputTypeDef]
    ResourceConfig: NotRequired[ResourceConfigOutputTypeDef]
    HyperParameterTuningResourceConfig: NotRequired[HyperParameterTuningResourceConfigOutputTypeDef]
    EnableNetworkIsolation: NotRequired[bool]
    EnableInterContainerTrafficEncryption: NotRequired[bool]
    EnableManagedSpotTraining: NotRequired[bool]
    CheckpointConfig: NotRequired[CheckpointConfigTypeDef]
    RetryStrategy: NotRequired[RetryStrategyTypeDef]
    Environment: NotRequired[Dict[str, str]]


class TrainingJobDefinitionOutputTypeDef(TypedDict):
    TrainingInputMode: TrainingInputModeType
    InputDataConfig: List[ChannelOutputTypeDef]
    OutputDataConfig: OutputDataConfigTypeDef
    ResourceConfig: ResourceConfigOutputTypeDef
    StoppingCondition: StoppingConditionTypeDef
    HyperParameters: NotRequired[Dict[str, str]]


class DescribeInferenceComponentOutputTypeDef(TypedDict):
    InferenceComponentName: str
    InferenceComponentArn: str
    EndpointName: str
    EndpointArn: str
    VariantName: str
    FailureReason: str
    Specification: InferenceComponentSpecificationSummaryTypeDef
    RuntimeConfig: InferenceComponentRuntimeConfigSummaryTypeDef
    CreationTime: datetime
    LastModifiedTime: datetime
    InferenceComponentStatus: InferenceComponentStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class CreateEdgeDeploymentPlanRequestRequestTypeDef(TypedDict):
    EdgeDeploymentPlanName: str
    ModelConfigs: Sequence[EdgeDeploymentModelConfigTypeDef]
    DeviceFleetName: str
    Stages: NotRequired[Sequence[DeploymentStageTypeDef]]
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateEdgeDeploymentStageRequestRequestTypeDef(TypedDict):
    EdgeDeploymentPlanName: str
    Stages: Sequence[DeploymentStageTypeDef]


class SpaceDetailsTypeDef(TypedDict):
    DomainId: NotRequired[str]
    SpaceName: NotRequired[str]
    Status: NotRequired[SpaceStatusType]
    CreationTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]
    SpaceSettingsSummary: NotRequired[SpaceSettingsSummaryTypeDef]
    SpaceSharingSettingsSummary: NotRequired[SpaceSharingSettingsSummaryTypeDef]
    OwnershipSettingsSummary: NotRequired[OwnershipSettingsSummaryTypeDef]
    SpaceDisplayName: NotRequired[str]


JupyterLabAppSettingsUnionTypeDef = Union[
    JupyterLabAppSettingsTypeDef, JupyterLabAppSettingsOutputTypeDef
]


class InferenceRecommendationsJobStepTypeDef(TypedDict):
    StepType: Literal["BENCHMARK"]
    JobName: str
    Status: RecommendationJobStatusType
    InferenceBenchmark: NotRequired[RecommendationJobInferenceBenchmarkTypeDef]


class SearchRequestSearchPaginateTypeDef(TypedDict):
    Resource: ResourceTypeType
    SearchExpression: NotRequired[SearchExpressionPaginatorTypeDef]
    SortBy: NotRequired[str]
    SortOrder: NotRequired[SearchSortOrderType]
    CrossAccountFilterOption: NotRequired[CrossAccountFilterOptionType]
    VisibilityConditions: NotRequired[Sequence[VisibilityConditionsTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class SearchRequestRequestTypeDef(TypedDict):
    Resource: ResourceTypeType
    SearchExpression: NotRequired[SearchExpressionTypeDef]
    SortBy: NotRequired[str]
    SortOrder: NotRequired[SearchSortOrderType]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    CrossAccountFilterOption: NotRequired[CrossAccountFilterOptionType]
    VisibilityConditions: NotRequired[Sequence[VisibilityConditionsTypeDef]]


StudioWebPortalSettingsUnionTypeDef = Union[
    StudioWebPortalSettingsTypeDef, StudioWebPortalSettingsOutputTypeDef
]


class ListAssociationsResponseTypeDef(TypedDict):
    AssociationSummaries: List[AssociationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class TrialTypeDef(TypedDict):
    TrialName: NotRequired[str]
    TrialArn: NotRequired[str]
    DisplayName: NotRequired[str]
    ExperimentName: NotRequired[str]
    Source: NotRequired[TrialSourceTypeDef]
    CreationTime: NotRequired[datetime]
    CreatedBy: NotRequired[UserContextTypeDef]
    LastModifiedTime: NotRequired[datetime]
    LastModifiedBy: NotRequired[UserContextTypeDef]
    MetadataProperties: NotRequired[MetadataPropertiesTypeDef]
    Tags: NotRequired[List[TagTypeDef]]
    TrialComponentSummaries: NotRequired[List[TrialComponentSimpleSummaryTypeDef]]


class ListTrialComponentsResponseTypeDef(TypedDict):
    TrialComponentSummaries: List[TrialComponentSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class WorkteamTypeDef(TypedDict):
    WorkteamName: str
    MemberDefinitions: List[MemberDefinitionOutputTypeDef]
    WorkteamArn: str
    Description: str
    WorkforceArn: NotRequired[str]
    ProductListingIds: NotRequired[List[str]]
    SubDomain: NotRequired[str]
    CreateDate: NotRequired[datetime]
    LastUpdatedDate: NotRequired[datetime]
    NotificationConfiguration: NotRequired[NotificationConfigurationTypeDef]
    WorkerAccessConfiguration: NotRequired[WorkerAccessConfigurationTypeDef]


class TrainingSpecificationOutputTypeDef(TypedDict):
    TrainingImage: str
    SupportedTrainingInstanceTypes: List[TrainingInstanceTypeType]
    TrainingChannels: List[ChannelSpecificationOutputTypeDef]
    TrainingImageDigest: NotRequired[str]
    SupportedHyperParameters: NotRequired[List[HyperParameterSpecificationOutputTypeDef]]
    SupportsDistributedTraining: NotRequired[bool]
    MetricDefinitions: NotRequired[List[MetricDefinitionTypeDef]]
    SupportedTuningJobObjectiveMetrics: NotRequired[List[HyperParameterTuningJobObjectiveTypeDef]]
    AdditionalS3DataSource: NotRequired[AdditionalS3DataSourceTypeDef]


class ListAppImageConfigsResponseTypeDef(TypedDict):
    AppImageConfigs: List[AppImageConfigDetailsTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class LabelingJobSummaryTypeDef(TypedDict):
    LabelingJobName: str
    LabelingJobArn: str
    CreationTime: datetime
    LastModifiedTime: datetime
    LabelingJobStatus: LabelingJobStatusType
    LabelCounters: LabelCountersTypeDef
    WorkteamArn: str
    PreHumanTaskLambdaArn: NotRequired[str]
    AnnotationConsolidationLambdaArn: NotRequired[str]
    FailureReason: NotRequired[str]
    LabelingJobOutput: NotRequired[LabelingJobOutputTypeDef]
    InputConfig: NotRequired[LabelingJobInputConfigOutputTypeDef]


class ScalingPolicyTypeDef(TypedDict):
    TargetTracking: NotRequired[TargetTrackingScalingPolicyConfigurationTypeDef]


class ContainerDefinitionOutputTypeDef(TypedDict):
    ContainerHostname: NotRequired[str]
    Image: NotRequired[str]
    ImageConfig: NotRequired[ImageConfigTypeDef]
    Mode: NotRequired[ContainerModeType]
    ModelDataUrl: NotRequired[str]
    ModelDataSource: NotRequired[ModelDataSourceTypeDef]
    AdditionalModelDataSources: NotRequired[List[AdditionalModelDataSourceTypeDef]]
    Environment: NotRequired[Dict[str, str]]
    ModelPackageName: NotRequired[str]
    InferenceSpecificationName: NotRequired[str]
    MultiModelConfig: NotRequired[MultiModelConfigTypeDef]


class ContainerDefinitionTypeDef(TypedDict):
    ContainerHostname: NotRequired[str]
    Image: NotRequired[str]
    ImageConfig: NotRequired[ImageConfigTypeDef]
    Mode: NotRequired[ContainerModeType]
    ModelDataUrl: NotRequired[str]
    ModelDataSource: NotRequired[ModelDataSourceTypeDef]
    AdditionalModelDataSources: NotRequired[Sequence[AdditionalModelDataSourceTypeDef]]
    Environment: NotRequired[Mapping[str, str]]
    ModelPackageName: NotRequired[str]
    InferenceSpecificationName: NotRequired[str]
    MultiModelConfig: NotRequired[MultiModelConfigTypeDef]


class ModelPackageContainerDefinitionOutputTypeDef(TypedDict):
    Image: str
    ContainerHostname: NotRequired[str]
    ImageDigest: NotRequired[str]
    ModelDataUrl: NotRequired[str]
    ModelDataSource: NotRequired[ModelDataSourceTypeDef]
    ProductId: NotRequired[str]
    Environment: NotRequired[Dict[str, str]]
    ModelInput: NotRequired[ModelInputTypeDef]
    Framework: NotRequired[str]
    FrameworkVersion: NotRequired[str]
    NearestModelName: NotRequired[str]
    AdditionalS3DataSource: NotRequired[AdditionalS3DataSourceTypeDef]


class ModelPackageContainerDefinitionTypeDef(TypedDict):
    Image: str
    ContainerHostname: NotRequired[str]
    ImageDigest: NotRequired[str]
    ModelDataUrl: NotRequired[str]
    ModelDataSource: NotRequired[ModelDataSourceTypeDef]
    ProductId: NotRequired[str]
    Environment: NotRequired[Mapping[str, str]]
    ModelInput: NotRequired[ModelInputTypeDef]
    Framework: NotRequired[str]
    FrameworkVersion: NotRequired[str]
    NearestModelName: NotRequired[str]
    AdditionalS3DataSource: NotRequired[AdditionalS3DataSourceTypeDef]


class SourceAlgorithmTypeDef(TypedDict):
    AlgorithmName: str
    ModelDataUrl: NotRequired[str]
    ModelDataSource: NotRequired[ModelDataSourceTypeDef]


class ListMonitoringAlertsResponseTypeDef(TypedDict):
    MonitoringAlertSummaries: List[MonitoringAlertSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


DescribeInferenceExperimentResponseTypeDef = TypedDict(
    "DescribeInferenceExperimentResponseTypeDef",
    {
        "Arn": str,
        "Name": str,
        "Type": Literal["ShadowMode"],
        "Schedule": InferenceExperimentScheduleOutputTypeDef,
        "Status": InferenceExperimentStatusType,
        "StatusReason": str,
        "Description": str,
        "CreationTime": datetime,
        "CompletionTime": datetime,
        "LastModifiedTime": datetime,
        "RoleArn": str,
        "EndpointMetadata": EndpointMetadataTypeDef,
        "ModelVariants": List[ModelVariantConfigSummaryTypeDef],
        "DataStorageConfig": InferenceExperimentDataStorageConfigOutputTypeDef,
        "ShadowModeConfig": ShadowModeConfigOutputTypeDef,
        "KmsKey": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateInferenceExperimentRequestRequestTypeDef = TypedDict(
    "CreateInferenceExperimentRequestRequestTypeDef",
    {
        "Name": str,
        "Type": Literal["ShadowMode"],
        "RoleArn": str,
        "EndpointName": str,
        "ModelVariants": Sequence[ModelVariantConfigTypeDef],
        "ShadowModeConfig": ShadowModeConfigTypeDef,
        "Schedule": NotRequired[InferenceExperimentScheduleTypeDef],
        "Description": NotRequired[str],
        "DataStorageConfig": NotRequired[InferenceExperimentDataStorageConfigTypeDef],
        "KmsKey": NotRequired[str],
        "Tags": NotRequired[Sequence[TagTypeDef]],
    },
)


class StopInferenceExperimentRequestRequestTypeDef(TypedDict):
    Name: str
    ModelVariantActions: Mapping[str, ModelVariantActionType]
    DesiredModelVariants: NotRequired[Sequence[ModelVariantConfigTypeDef]]
    DesiredState: NotRequired[InferenceExperimentStopDesiredStateType]
    Reason: NotRequired[str]


class UpdateInferenceExperimentRequestRequestTypeDef(TypedDict):
    Name: str
    Schedule: NotRequired[InferenceExperimentScheduleTypeDef]
    Description: NotRequired[str]
    ModelVariants: NotRequired[Sequence[ModelVariantConfigTypeDef]]
    DataStorageConfig: NotRequired[InferenceExperimentDataStorageConfigTypeDef]
    ShadowModeConfig: NotRequired[ShadowModeConfigTypeDef]


OptimizationConfigUnionTypeDef = Union[OptimizationConfigTypeDef, OptimizationConfigOutputTypeDef]


class DataQualityJobInputOutputTypeDef(TypedDict):
    EndpointInput: NotRequired[EndpointInputTypeDef]
    BatchTransformInput: NotRequired[BatchTransformInputOutputTypeDef]


class ModelBiasJobInputOutputTypeDef(TypedDict):
    GroundTruthS3Input: MonitoringGroundTruthS3InputTypeDef
    EndpointInput: NotRequired[EndpointInputTypeDef]
    BatchTransformInput: NotRequired[BatchTransformInputOutputTypeDef]


class ModelExplainabilityJobInputOutputTypeDef(TypedDict):
    EndpointInput: NotRequired[EndpointInputTypeDef]
    BatchTransformInput: NotRequired[BatchTransformInputOutputTypeDef]


class ModelQualityJobInputOutputTypeDef(TypedDict):
    GroundTruthS3Input: MonitoringGroundTruthS3InputTypeDef
    EndpointInput: NotRequired[EndpointInputTypeDef]
    BatchTransformInput: NotRequired[BatchTransformInputOutputTypeDef]


class MonitoringInputOutputTypeDef(TypedDict):
    EndpointInput: NotRequired[EndpointInputTypeDef]
    BatchTransformInput: NotRequired[BatchTransformInputOutputTypeDef]


BatchTransformInputTypeDef = TypedDict(
    "BatchTransformInputTypeDef",
    {
        "DataCapturedDestinationS3Uri": str,
        "DatasetFormat": MonitoringDatasetFormatUnionTypeDef,
        "LocalPath": str,
        "S3InputMode": NotRequired[ProcessingS3InputModeType],
        "S3DataDistributionType": NotRequired[ProcessingS3DataDistributionTypeType],
        "FeaturesAttribute": NotRequired[str],
        "InferenceAttribute": NotRequired[str],
        "ProbabilityAttribute": NotRequired[str],
        "ProbabilityThresholdAttribute": NotRequired[float],
        "StartTimeOffset": NotRequired[str],
        "EndTimeOffset": NotRequired[str],
        "ExcludeFeaturesAttribute": NotRequired[str],
    },
)
MonitoringOutputConfigUnionTypeDef = Union[
    MonitoringOutputConfigTypeDef, MonitoringOutputConfigOutputTypeDef
]
MemberDefinitionUnionTypeDef = Union[MemberDefinitionTypeDef, MemberDefinitionOutputTypeDef]


class UpdateWorkteamRequestRequestTypeDef(TypedDict):
    WorkteamName: str
    MemberDefinitions: NotRequired[Sequence[MemberDefinitionTypeDef]]
    Description: NotRequired[str]
    NotificationConfiguration: NotRequired[NotificationConfigurationTypeDef]
    WorkerAccessConfiguration: NotRequired[WorkerAccessConfigurationTypeDef]


class DescribeOptimizationJobResponseTypeDef(TypedDict):
    OptimizationJobArn: str
    OptimizationJobStatus: OptimizationJobStatusType
    OptimizationStartTime: datetime
    OptimizationEndTime: datetime
    CreationTime: datetime
    LastModifiedTime: datetime
    FailureReason: str
    OptimizationJobName: str
    ModelSource: OptimizationJobModelSourceTypeDef
    OptimizationEnvironment: Dict[str, str]
    DeploymentInstanceType: OptimizationJobDeploymentInstanceTypeType
    OptimizationConfigs: List[OptimizationConfigOutputTypeDef]
    OutputConfig: OptimizationJobOutputConfigTypeDef
    OptimizationOutput: OptimizationOutputTypeDef
    RoleArn: str
    StoppingCondition: StoppingConditionTypeDef
    VpcConfig: OptimizationVpcConfigOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeProcessingJobResponseTypeDef(TypedDict):
    ProcessingInputs: List[ProcessingInputTypeDef]
    ProcessingOutputConfig: ProcessingOutputConfigOutputTypeDef
    ProcessingJobName: str
    ProcessingResources: ProcessingResourcesTypeDef
    StoppingCondition: ProcessingStoppingConditionTypeDef
    AppSpecification: AppSpecificationOutputTypeDef
    Environment: Dict[str, str]
    NetworkConfig: NetworkConfigOutputTypeDef
    RoleArn: str
    ExperimentConfig: ExperimentConfigTypeDef
    ProcessingJobArn: str
    ProcessingJobStatus: ProcessingJobStatusType
    ExitMessage: str
    FailureReason: str
    ProcessingEndTime: datetime
    ProcessingStartTime: datetime
    LastModifiedTime: datetime
    CreationTime: datetime
    MonitoringScheduleArn: str
    AutoMLJobArn: str
    TrainingJobArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class ProcessingJobTypeDef(TypedDict):
    ProcessingInputs: NotRequired[List[ProcessingInputTypeDef]]
    ProcessingOutputConfig: NotRequired[ProcessingOutputConfigOutputTypeDef]
    ProcessingJobName: NotRequired[str]
    ProcessingResources: NotRequired[ProcessingResourcesTypeDef]
    StoppingCondition: NotRequired[ProcessingStoppingConditionTypeDef]
    AppSpecification: NotRequired[AppSpecificationOutputTypeDef]
    Environment: NotRequired[Dict[str, str]]
    NetworkConfig: NotRequired[NetworkConfigOutputTypeDef]
    RoleArn: NotRequired[str]
    ExperimentConfig: NotRequired[ExperimentConfigTypeDef]
    ProcessingJobArn: NotRequired[str]
    ProcessingJobStatus: NotRequired[ProcessingJobStatusType]
    ExitMessage: NotRequired[str]
    FailureReason: NotRequired[str]
    ProcessingEndTime: NotRequired[datetime]
    ProcessingStartTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]
    CreationTime: NotRequired[datetime]
    MonitoringScheduleArn: NotRequired[str]
    AutoMLJobArn: NotRequired[str]
    TrainingJobArn: NotRequired[str]
    Tags: NotRequired[List[TagTypeDef]]


class CreateProcessingJobRequestRequestTypeDef(TypedDict):
    ProcessingJobName: str
    ProcessingResources: ProcessingResourcesTypeDef
    AppSpecification: AppSpecificationTypeDef
    RoleArn: str
    ProcessingInputs: NotRequired[Sequence[ProcessingInputTypeDef]]
    ProcessingOutputConfig: NotRequired[ProcessingOutputConfigTypeDef]
    StoppingCondition: NotRequired[ProcessingStoppingConditionTypeDef]
    Environment: NotRequired[Mapping[str, str]]
    NetworkConfig: NotRequired[NetworkConfigTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]
    ExperimentConfig: NotRequired[ExperimentConfigTypeDef]


class DescribeFlowDefinitionResponseTypeDef(TypedDict):
    FlowDefinitionArn: str
    FlowDefinitionName: str
    FlowDefinitionStatus: FlowDefinitionStatusType
    CreationTime: datetime
    HumanLoopRequestSource: HumanLoopRequestSourceTypeDef
    HumanLoopActivationConfig: HumanLoopActivationConfigTypeDef
    HumanLoopConfig: HumanLoopConfigOutputTypeDef
    OutputConfig: FlowDefinitionOutputConfigTypeDef
    RoleArn: str
    FailureReason: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateFlowDefinitionRequestRequestTypeDef(TypedDict):
    FlowDefinitionName: str
    OutputConfig: FlowDefinitionOutputConfigTypeDef
    RoleArn: str
    HumanLoopRequestSource: NotRequired[HumanLoopRequestSourceTypeDef]
    HumanLoopActivationConfig: NotRequired[HumanLoopActivationConfigTypeDef]
    HumanLoopConfig: NotRequired[HumanLoopConfigTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]


class DescribeLabelingJobResponseTypeDef(TypedDict):
    LabelingJobStatus: LabelingJobStatusType
    LabelCounters: LabelCountersTypeDef
    FailureReason: str
    CreationTime: datetime
    LastModifiedTime: datetime
    JobReferenceCode: str
    LabelingJobName: str
    LabelingJobArn: str
    LabelAttributeName: str
    InputConfig: LabelingJobInputConfigOutputTypeDef
    OutputConfig: LabelingJobOutputConfigTypeDef
    RoleArn: str
    LabelCategoryConfigS3Uri: str
    StoppingConditions: LabelingJobStoppingConditionsTypeDef
    LabelingJobAlgorithmsConfig: LabelingJobAlgorithmsConfigOutputTypeDef
    HumanTaskConfig: HumanTaskConfigOutputTypeDef
    Tags: List[TagTypeDef]
    LabelingJobOutput: LabelingJobOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


RecommendationJobContainerConfigUnionTypeDef = Union[
    RecommendationJobContainerConfigTypeDef, RecommendationJobContainerConfigOutputTypeDef
]
DataSourceUnionTypeDef = Union[DataSourceTypeDef, DataSourceOutputTypeDef]


class SpaceSettingsOutputTypeDef(TypedDict):
    JupyterServerAppSettings: NotRequired[JupyterServerAppSettingsOutputTypeDef]
    KernelGatewayAppSettings: NotRequired[KernelGatewayAppSettingsOutputTypeDef]
    CodeEditorAppSettings: NotRequired[SpaceCodeEditorAppSettingsTypeDef]
    JupyterLabAppSettings: NotRequired[SpaceJupyterLabAppSettingsOutputTypeDef]
    AppType: NotRequired[AppTypeType]
    SpaceStorageSettings: NotRequired[SpaceStorageSettingsTypeDef]
    CustomFileSystems: NotRequired[List[CustomFileSystemTypeDef]]


SpaceJupyterLabAppSettingsUnionTypeDef = Union[
    SpaceJupyterLabAppSettingsTypeDef, SpaceJupyterLabAppSettingsOutputTypeDef
]


class DescribeTrainingJobResponseTypeDef(TypedDict):
    TrainingJobName: str
    TrainingJobArn: str
    TuningJobArn: str
    LabelingJobArn: str
    AutoMLJobArn: str
    ModelArtifacts: ModelArtifactsTypeDef
    TrainingJobStatus: TrainingJobStatusType
    SecondaryStatus: SecondaryStatusType
    FailureReason: str
    HyperParameters: Dict[str, str]
    AlgorithmSpecification: AlgorithmSpecificationOutputTypeDef
    RoleArn: str
    InputDataConfig: List[ChannelOutputTypeDef]
    OutputDataConfig: OutputDataConfigTypeDef
    ResourceConfig: ResourceConfigOutputTypeDef
    WarmPoolStatus: WarmPoolStatusTypeDef
    VpcConfig: VpcConfigOutputTypeDef
    StoppingCondition: StoppingConditionTypeDef
    CreationTime: datetime
    TrainingStartTime: datetime
    TrainingEndTime: datetime
    LastModifiedTime: datetime
    SecondaryStatusTransitions: List[SecondaryStatusTransitionTypeDef]
    FinalMetricDataList: List[MetricDataTypeDef]
    EnableNetworkIsolation: bool
    EnableInterContainerTrafficEncryption: bool
    EnableManagedSpotTraining: bool
    CheckpointConfig: CheckpointConfigTypeDef
    TrainingTimeInSeconds: int
    BillableTimeInSeconds: int
    DebugHookConfig: DebugHookConfigOutputTypeDef
    ExperimentConfig: ExperimentConfigTypeDef
    DebugRuleConfigurations: List[DebugRuleConfigurationOutputTypeDef]
    TensorBoardOutputConfig: TensorBoardOutputConfigTypeDef
    DebugRuleEvaluationStatuses: List[DebugRuleEvaluationStatusTypeDef]
    ProfilerConfig: ProfilerConfigOutputTypeDef
    ProfilerRuleConfigurations: List[ProfilerRuleConfigurationOutputTypeDef]
    ProfilerRuleEvaluationStatuses: List[ProfilerRuleEvaluationStatusTypeDef]
    ProfilingStatus: ProfilingStatusType
    Environment: Dict[str, str]
    RetryStrategy: RetryStrategyTypeDef
    RemoteDebugConfig: RemoteDebugConfigTypeDef
    InfraCheckConfig: InfraCheckConfigTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class TrainingJobTypeDef(TypedDict):
    TrainingJobName: NotRequired[str]
    TrainingJobArn: NotRequired[str]
    TuningJobArn: NotRequired[str]
    LabelingJobArn: NotRequired[str]
    AutoMLJobArn: NotRequired[str]
    ModelArtifacts: NotRequired[ModelArtifactsTypeDef]
    TrainingJobStatus: NotRequired[TrainingJobStatusType]
    SecondaryStatus: NotRequired[SecondaryStatusType]
    FailureReason: NotRequired[str]
    HyperParameters: NotRequired[Dict[str, str]]
    AlgorithmSpecification: NotRequired[AlgorithmSpecificationOutputTypeDef]
    RoleArn: NotRequired[str]
    InputDataConfig: NotRequired[List[ChannelOutputTypeDef]]
    OutputDataConfig: NotRequired[OutputDataConfigTypeDef]
    ResourceConfig: NotRequired[ResourceConfigOutputTypeDef]
    VpcConfig: NotRequired[VpcConfigOutputTypeDef]
    StoppingCondition: NotRequired[StoppingConditionTypeDef]
    CreationTime: NotRequired[datetime]
    TrainingStartTime: NotRequired[datetime]
    TrainingEndTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]
    SecondaryStatusTransitions: NotRequired[List[SecondaryStatusTransitionTypeDef]]
    FinalMetricDataList: NotRequired[List[MetricDataTypeDef]]
    EnableNetworkIsolation: NotRequired[bool]
    EnableInterContainerTrafficEncryption: NotRequired[bool]
    EnableManagedSpotTraining: NotRequired[bool]
    CheckpointConfig: NotRequired[CheckpointConfigTypeDef]
    TrainingTimeInSeconds: NotRequired[int]
    BillableTimeInSeconds: NotRequired[int]
    DebugHookConfig: NotRequired[DebugHookConfigOutputTypeDef]
    ExperimentConfig: NotRequired[ExperimentConfigTypeDef]
    DebugRuleConfigurations: NotRequired[List[DebugRuleConfigurationOutputTypeDef]]
    TensorBoardOutputConfig: NotRequired[TensorBoardOutputConfigTypeDef]
    DebugRuleEvaluationStatuses: NotRequired[List[DebugRuleEvaluationStatusTypeDef]]
    ProfilerConfig: NotRequired[ProfilerConfigOutputTypeDef]
    Environment: NotRequired[Dict[str, str]]
    RetryStrategy: NotRequired[RetryStrategyTypeDef]
    Tags: NotRequired[List[TagTypeDef]]


class CreateTransformJobRequestRequestTypeDef(TypedDict):
    TransformJobName: str
    ModelName: str
    TransformInput: TransformInputTypeDef
    TransformOutput: TransformOutputTypeDef
    TransformResources: TransformResourcesTypeDef
    MaxConcurrentTransforms: NotRequired[int]
    ModelClientConfig: NotRequired[ModelClientConfigTypeDef]
    MaxPayloadInMB: NotRequired[int]
    BatchStrategy: NotRequired[BatchStrategyType]
    Environment: NotRequired[Mapping[str, str]]
    DataCaptureConfig: NotRequired[BatchDataCaptureConfigTypeDef]
    DataProcessing: NotRequired[DataProcessingTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]
    ExperimentConfig: NotRequired[ExperimentConfigTypeDef]


class DescribeTransformJobResponseTypeDef(TypedDict):
    TransformJobName: str
    TransformJobArn: str
    TransformJobStatus: TransformJobStatusType
    FailureReason: str
    ModelName: str
    MaxConcurrentTransforms: int
    ModelClientConfig: ModelClientConfigTypeDef
    MaxPayloadInMB: int
    BatchStrategy: BatchStrategyType
    Environment: Dict[str, str]
    TransformInput: TransformInputTypeDef
    TransformOutput: TransformOutputTypeDef
    DataCaptureConfig: BatchDataCaptureConfigTypeDef
    TransformResources: TransformResourcesTypeDef
    CreationTime: datetime
    TransformStartTime: datetime
    TransformEndTime: datetime
    LabelingJobArn: str
    AutoMLJobArn: str
    DataProcessing: DataProcessingTypeDef
    ExperimentConfig: ExperimentConfigTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class TransformJobDefinitionOutputTypeDef(TypedDict):
    TransformInput: TransformInputTypeDef
    TransformOutput: TransformOutputTypeDef
    TransformResources: TransformResourcesTypeDef
    MaxConcurrentTransforms: NotRequired[int]
    MaxPayloadInMB: NotRequired[int]
    BatchStrategy: NotRequired[BatchStrategyType]
    Environment: NotRequired[Dict[str, str]]


class TransformJobDefinitionTypeDef(TypedDict):
    TransformInput: TransformInputTypeDef
    TransformOutput: TransformOutputTypeDef
    TransformResources: TransformResourcesTypeDef
    MaxConcurrentTransforms: NotRequired[int]
    MaxPayloadInMB: NotRequired[int]
    BatchStrategy: NotRequired[BatchStrategyType]
    Environment: NotRequired[Mapping[str, str]]


class TransformJobTypeDef(TypedDict):
    TransformJobName: NotRequired[str]
    TransformJobArn: NotRequired[str]
    TransformJobStatus: NotRequired[TransformJobStatusType]
    FailureReason: NotRequired[str]
    ModelName: NotRequired[str]
    MaxConcurrentTransforms: NotRequired[int]
    ModelClientConfig: NotRequired[ModelClientConfigTypeDef]
    MaxPayloadInMB: NotRequired[int]
    BatchStrategy: NotRequired[BatchStrategyType]
    Environment: NotRequired[Dict[str, str]]
    TransformInput: NotRequired[TransformInputTypeDef]
    TransformOutput: NotRequired[TransformOutputTypeDef]
    DataCaptureConfig: NotRequired[BatchDataCaptureConfigTypeDef]
    TransformResources: NotRequired[TransformResourcesTypeDef]
    CreationTime: NotRequired[datetime]
    TransformStartTime: NotRequired[datetime]
    TransformEndTime: NotRequired[datetime]
    LabelingJobArn: NotRequired[str]
    AutoMLJobArn: NotRequired[str]
    DataProcessing: NotRequired[DataProcessingTypeDef]
    ExperimentConfig: NotRequired[ExperimentConfigTypeDef]
    Tags: NotRequired[List[TagTypeDef]]


class DescribeDomainResponseTypeDef(TypedDict):
    DomainArn: str
    DomainId: str
    DomainName: str
    HomeEfsFileSystemId: str
    SingleSignOnManagedApplicationInstanceId: str
    SingleSignOnApplicationArn: str
    Status: DomainStatusType
    CreationTime: datetime
    LastModifiedTime: datetime
    FailureReason: str
    SecurityGroupIdForDomainBoundary: str
    AuthMode: AuthModeType
    DefaultUserSettings: UserSettingsOutputTypeDef
    DomainSettings: DomainSettingsOutputTypeDef
    AppNetworkAccessType: AppNetworkAccessTypeType
    HomeEfsFileSystemKmsKeyId: str
    SubnetIds: List[str]
    Url: str
    VpcId: str
    KmsKeyId: str
    AppSecurityGroupManagement: AppSecurityGroupManagementType
    TagPropagation: TagPropagationType
    DefaultSpaceSettings: DefaultSpaceSettingsOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeUserProfileResponseTypeDef(TypedDict):
    DomainId: str
    UserProfileArn: str
    UserProfileName: str
    HomeEfsFileSystemUid: str
    Status: UserProfileStatusType
    LastModifiedTime: datetime
    CreationTime: datetime
    FailureReason: str
    SingleSignOnUserIdentifier: str
    SingleSignOnUserValue: str
    UserSettings: UserSettingsOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class AsyncInferenceConfigTypeDef(TypedDict):
    OutputConfig: AsyncInferenceOutputConfigUnionTypeDef
    ClientConfig: NotRequired[AsyncInferenceClientConfigTypeDef]


class DescribeAutoMLJobV2ResponseTypeDef(TypedDict):
    AutoMLJobName: str
    AutoMLJobArn: str
    AutoMLJobInputDataConfig: List[AutoMLJobChannelTypeDef]
    OutputDataConfig: AutoMLOutputDataConfigTypeDef
    RoleArn: str
    AutoMLJobObjective: AutoMLJobObjectiveTypeDef
    AutoMLProblemTypeConfig: AutoMLProblemTypeConfigOutputTypeDef
    AutoMLProblemTypeConfigName: AutoMLProblemTypeConfigNameType
    CreationTime: datetime
    EndTime: datetime
    LastModifiedTime: datetime
    FailureReason: str
    PartialFailureReasons: List[AutoMLPartialFailureReasonTypeDef]
    BestCandidate: AutoMLCandidateTypeDef
    AutoMLJobStatus: AutoMLJobStatusType
    AutoMLJobSecondaryStatus: AutoMLJobSecondaryStatusType
    AutoMLJobArtifacts: AutoMLJobArtifactsTypeDef
    ResolvedAttributes: AutoMLResolvedAttributesTypeDef
    ModelDeployConfig: ModelDeployConfigTypeDef
    ModelDeployResult: ModelDeployResultTypeDef
    DataSplitConfig: AutoMLDataSplitConfigTypeDef
    SecurityConfig: AutoMLSecurityConfigOutputTypeDef
    AutoMLComputeConfig: AutoMLComputeConfigTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class TabularJobConfigTypeDef(TypedDict):
    TargetAttributeName: str
    CandidateGenerationConfig: NotRequired[CandidateGenerationConfigUnionTypeDef]
    CompletionCriteria: NotRequired[AutoMLJobCompletionCriteriaTypeDef]
    FeatureSpecificationS3Uri: NotRequired[str]
    Mode: NotRequired[AutoMLModeType]
    GenerateCandidateDefinitionsOnly: NotRequired[bool]
    ProblemType: NotRequired[ProblemTypeType]
    SampleWeightAttributeName: NotRequired[str]


class TimeSeriesForecastingJobConfigTypeDef(TypedDict):
    ForecastFrequency: str
    ForecastHorizon: int
    TimeSeriesConfig: TimeSeriesConfigUnionTypeDef
    FeatureSpecificationS3Uri: NotRequired[str]
    CompletionCriteria: NotRequired[AutoMLJobCompletionCriteriaTypeDef]
    ForecastQuantiles: NotRequired[Sequence[str]]
    Transformations: NotRequired[TimeSeriesTransformationsUnionTypeDef]
    HolidayConfig: NotRequired[Sequence[HolidayConfigAttributesTypeDef]]
    CandidateGenerationConfig: NotRequired[CandidateGenerationConfigUnionTypeDef]


class ListPipelineExecutionStepsResponseTypeDef(TypedDict):
    PipelineExecutionSteps: List[PipelineExecutionStepTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class CreateEndpointInputRequestTypeDef(TypedDict):
    EndpointName: str
    EndpointConfigName: str
    DeploymentConfig: NotRequired[DeploymentConfigTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]


class UpdateEndpointInputRequestTypeDef(TypedDict):
    EndpointName: str
    EndpointConfigName: str
    RetainAllVariantProperties: NotRequired[bool]
    ExcludeRetainedVariantProperties: NotRequired[Sequence[VariantPropertyTypeDef]]
    DeploymentConfig: NotRequired[DeploymentConfigTypeDef]
    RetainDeploymentConfig: NotRequired[bool]


class DescribeInferenceRecommendationsJobResponseTypeDef(TypedDict):
    JobName: str
    JobDescription: str
    JobType: RecommendationJobTypeType
    JobArn: str
    RoleArn: str
    Status: RecommendationJobStatusType
    CreationTime: datetime
    CompletionTime: datetime
    LastModifiedTime: datetime
    FailureReason: str
    InputConfig: RecommendationJobInputConfigOutputTypeDef
    StoppingConditions: RecommendationJobStoppingConditionsOutputTypeDef
    InferenceRecommendations: List[InferenceRecommendationTypeDef]
    EndpointPerformances: List[EndpointPerformanceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


HyperParameterSpecificationTypeDef = TypedDict(
    "HyperParameterSpecificationTypeDef",
    {
        "Name": str,
        "Type": ParameterTypeType,
        "Description": NotRequired[str],
        "Range": NotRequired[ParameterRangeUnionTypeDef],
        "IsTunable": NotRequired[bool],
        "IsRequired": NotRequired[bool],
        "DefaultValue": NotRequired[str],
    },
)


class HyperParameterTuningJobConfigTypeDef(TypedDict):
    Strategy: HyperParameterTuningJobStrategyTypeType
    ResourceLimits: ResourceLimitsTypeDef
    StrategyConfig: NotRequired[HyperParameterTuningJobStrategyConfigTypeDef]
    HyperParameterTuningJobObjective: NotRequired[HyperParameterTuningJobObjectiveTypeDef]
    ParameterRanges: NotRequired[ParameterRangesUnionTypeDef]
    TrainingJobEarlyStoppingType: NotRequired[TrainingJobEarlyStoppingTypeType]
    TuningJobCompletionCriteria: NotRequired[TuningJobCompletionCriteriaTypeDef]
    RandomSeed: NotRequired[int]


class EndpointInputConfigurationTypeDef(TypedDict):
    InstanceType: NotRequired[ProductionVariantInstanceTypeType]
    ServerlessConfig: NotRequired[ProductionVariantServerlessConfigTypeDef]
    InferenceSpecificationName: NotRequired[str]
    EnvironmentParameterRanges: NotRequired[EnvironmentParameterRangesUnionTypeDef]


class DescribeEndpointConfigOutputTypeDef(TypedDict):
    EndpointConfigName: str
    EndpointConfigArn: str
    ProductionVariants: List[ProductionVariantTypeDef]
    DataCaptureConfig: DataCaptureConfigOutputTypeDef
    KmsKeyId: str
    CreationTime: datetime
    AsyncInferenceConfig: AsyncInferenceConfigOutputTypeDef
    ExplainerConfig: ExplainerConfigOutputTypeDef
    ShadowProductionVariants: List[ProductionVariantTypeDef]
    ExecutionRoleArn: str
    VpcConfig: VpcConfigOutputTypeDef
    EnableNetworkIsolation: bool
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeEndpointOutputTypeDef(TypedDict):
    EndpointName: str
    EndpointArn: str
    EndpointConfigName: str
    ProductionVariants: List[ProductionVariantSummaryTypeDef]
    DataCaptureConfig: DataCaptureConfigSummaryTypeDef
    EndpointStatus: EndpointStatusType
    FailureReason: str
    CreationTime: datetime
    LastModifiedTime: datetime
    LastDeploymentConfig: DeploymentConfigOutputTypeDef
    AsyncInferenceConfig: AsyncInferenceConfigOutputTypeDef
    PendingDeploymentSummary: PendingDeploymentSummaryTypeDef
    ExplainerConfig: ExplainerConfigOutputTypeDef
    ShadowProductionVariants: List[ProductionVariantSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ExplainerConfigTypeDef(TypedDict):
    ClarifyExplainerConfig: NotRequired[ClarifyExplainerConfigUnionTypeDef]


class AutoMLJobConfigTypeDef(TypedDict):
    CompletionCriteria: NotRequired[AutoMLJobCompletionCriteriaTypeDef]
    SecurityConfig: NotRequired[AutoMLSecurityConfigUnionTypeDef]
    CandidateGenerationConfig: NotRequired[AutoMLCandidateGenerationConfigUnionTypeDef]
    DataSplitConfig: NotRequired[AutoMLDataSplitConfigTypeDef]
    Mode: NotRequired[AutoMLModeType]


class LabelingJobAlgorithmsConfigTypeDef(TypedDict):
    LabelingJobAlgorithmSpecificationArn: str
    InitialActiveLearningModelArn: NotRequired[str]
    LabelingJobResourceConfig: NotRequired[LabelingJobResourceConfigUnionTypeDef]


class DescribeHyperParameterTuningJobResponseTypeDef(TypedDict):
    HyperParameterTuningJobName: str
    HyperParameterTuningJobArn: str
    HyperParameterTuningJobConfig: HyperParameterTuningJobConfigOutputTypeDef
    TrainingJobDefinition: HyperParameterTrainingJobDefinitionOutputTypeDef
    TrainingJobDefinitions: List[HyperParameterTrainingJobDefinitionOutputTypeDef]
    HyperParameterTuningJobStatus: HyperParameterTuningJobStatusType
    CreationTime: datetime
    HyperParameterTuningEndTime: datetime
    LastModifiedTime: datetime
    TrainingJobStatusCounters: TrainingJobStatusCountersTypeDef
    ObjectiveStatusCounters: ObjectiveStatusCountersTypeDef
    BestTrainingJob: HyperParameterTrainingJobSummaryTypeDef
    OverallBestTrainingJob: HyperParameterTrainingJobSummaryTypeDef
    WarmStartConfig: HyperParameterTuningJobWarmStartConfigOutputTypeDef
    Autotune: AutotuneTypeDef
    FailureReason: str
    TuningJobCompletionDetails: HyperParameterTuningJobCompletionDetailsTypeDef
    ConsumedResources: HyperParameterTuningJobConsumedResourcesTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class HyperParameterTuningJobSearchEntityTypeDef(TypedDict):
    HyperParameterTuningJobName: NotRequired[str]
    HyperParameterTuningJobArn: NotRequired[str]
    HyperParameterTuningJobConfig: NotRequired[HyperParameterTuningJobConfigOutputTypeDef]
    TrainingJobDefinition: NotRequired[HyperParameterTrainingJobDefinitionOutputTypeDef]
    TrainingJobDefinitions: NotRequired[List[HyperParameterTrainingJobDefinitionOutputTypeDef]]
    HyperParameterTuningJobStatus: NotRequired[HyperParameterTuningJobStatusType]
    CreationTime: NotRequired[datetime]
    HyperParameterTuningEndTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]
    TrainingJobStatusCounters: NotRequired[TrainingJobStatusCountersTypeDef]
    ObjectiveStatusCounters: NotRequired[ObjectiveStatusCountersTypeDef]
    BestTrainingJob: NotRequired[HyperParameterTrainingJobSummaryTypeDef]
    OverallBestTrainingJob: NotRequired[HyperParameterTrainingJobSummaryTypeDef]
    WarmStartConfig: NotRequired[HyperParameterTuningJobWarmStartConfigOutputTypeDef]
    FailureReason: NotRequired[str]
    TuningJobCompletionDetails: NotRequired[HyperParameterTuningJobCompletionDetailsTypeDef]
    ConsumedResources: NotRequired[HyperParameterTuningJobConsumedResourcesTypeDef]
    Tags: NotRequired[List[TagTypeDef]]


class ListSpacesResponseTypeDef(TypedDict):
    Spaces: List[SpaceDetailsTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DefaultSpaceSettingsTypeDef(TypedDict):
    ExecutionRole: NotRequired[str]
    SecurityGroups: NotRequired[Sequence[str]]
    JupyterServerAppSettings: NotRequired[JupyterServerAppSettingsUnionTypeDef]
    KernelGatewayAppSettings: NotRequired[KernelGatewayAppSettingsUnionTypeDef]
    JupyterLabAppSettings: NotRequired[JupyterLabAppSettingsUnionTypeDef]
    SpaceStorageSettings: NotRequired[DefaultSpaceStorageSettingsTypeDef]
    CustomPosixUserConfig: NotRequired[CustomPosixUserConfigTypeDef]
    CustomFileSystemConfigs: NotRequired[Sequence[CustomFileSystemConfigTypeDef]]


class ListInferenceRecommendationsJobStepsResponseTypeDef(TypedDict):
    Steps: List[InferenceRecommendationsJobStepTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class UserSettingsTypeDef(TypedDict):
    ExecutionRole: NotRequired[str]
    SecurityGroups: NotRequired[Sequence[str]]
    SharingSettings: NotRequired[SharingSettingsTypeDef]
    JupyterServerAppSettings: NotRequired[JupyterServerAppSettingsUnionTypeDef]
    KernelGatewayAppSettings: NotRequired[KernelGatewayAppSettingsUnionTypeDef]
    TensorBoardAppSettings: NotRequired[TensorBoardAppSettingsTypeDef]
    RStudioServerProAppSettings: NotRequired[RStudioServerProAppSettingsTypeDef]
    RSessionAppSettings: NotRequired[RSessionAppSettingsUnionTypeDef]
    CanvasAppSettings: NotRequired[CanvasAppSettingsUnionTypeDef]
    CodeEditorAppSettings: NotRequired[CodeEditorAppSettingsUnionTypeDef]
    JupyterLabAppSettings: NotRequired[JupyterLabAppSettingsUnionTypeDef]
    SpaceStorageSettings: NotRequired[DefaultSpaceStorageSettingsTypeDef]
    DefaultLandingUri: NotRequired[str]
    StudioWebPortal: NotRequired[StudioWebPortalType]
    CustomPosixUserConfig: NotRequired[CustomPosixUserConfigTypeDef]
    CustomFileSystemConfigs: NotRequired[Sequence[CustomFileSystemConfigTypeDef]]
    StudioWebPortalSettings: NotRequired[StudioWebPortalSettingsUnionTypeDef]
    AutoMountHomeEFS: NotRequired[AutoMountHomeEFSType]


class DescribeWorkteamResponseTypeDef(TypedDict):
    Workteam: WorkteamTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListWorkteamsResponseTypeDef(TypedDict):
    Workteams: List[WorkteamTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class UpdateWorkteamResponseTypeDef(TypedDict):
    Workteam: WorkteamTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListLabelingJobsResponseTypeDef(TypedDict):
    LabelingJobSummaryList: List[LabelingJobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DynamicScalingConfigurationTypeDef(TypedDict):
    MinCapacity: NotRequired[int]
    MaxCapacity: NotRequired[int]
    ScaleInCooldown: NotRequired[int]
    ScaleOutCooldown: NotRequired[int]
    ScalingPolicies: NotRequired[List[ScalingPolicyTypeDef]]


class DescribeModelOutputTypeDef(TypedDict):
    ModelName: str
    PrimaryContainer: ContainerDefinitionOutputTypeDef
    Containers: List[ContainerDefinitionOutputTypeDef]
    InferenceExecutionConfig: InferenceExecutionConfigTypeDef
    ExecutionRoleArn: str
    VpcConfig: VpcConfigOutputTypeDef
    CreationTime: datetime
    ModelArn: str
    EnableNetworkIsolation: bool
    DeploymentRecommendation: DeploymentRecommendationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ModelTypeDef(TypedDict):
    ModelName: NotRequired[str]
    PrimaryContainer: NotRequired[ContainerDefinitionOutputTypeDef]
    Containers: NotRequired[List[ContainerDefinitionOutputTypeDef]]
    InferenceExecutionConfig: NotRequired[InferenceExecutionConfigTypeDef]
    ExecutionRoleArn: NotRequired[str]
    VpcConfig: NotRequired[VpcConfigOutputTypeDef]
    CreationTime: NotRequired[datetime]
    ModelArn: NotRequired[str]
    EnableNetworkIsolation: NotRequired[bool]
    Tags: NotRequired[List[TagTypeDef]]
    DeploymentRecommendation: NotRequired[DeploymentRecommendationTypeDef]


ContainerDefinitionUnionTypeDef = Union[
    ContainerDefinitionTypeDef, ContainerDefinitionOutputTypeDef
]


class AdditionalInferenceSpecificationDefinitionOutputTypeDef(TypedDict):
    Name: str
    Containers: List[ModelPackageContainerDefinitionOutputTypeDef]
    Description: NotRequired[str]
    SupportedTransformInstanceTypes: NotRequired[List[TransformInstanceTypeType]]
    SupportedRealtimeInferenceInstanceTypes: NotRequired[List[ProductionVariantInstanceTypeType]]
    SupportedContentTypes: NotRequired[List[str]]
    SupportedResponseMIMETypes: NotRequired[List[str]]


class InferenceSpecificationOutputTypeDef(TypedDict):
    Containers: List[ModelPackageContainerDefinitionOutputTypeDef]
    SupportedTransformInstanceTypes: NotRequired[List[TransformInstanceTypeType]]
    SupportedRealtimeInferenceInstanceTypes: NotRequired[List[ProductionVariantInstanceTypeType]]
    SupportedContentTypes: NotRequired[List[str]]
    SupportedResponseMIMETypes: NotRequired[List[str]]


ModelPackageContainerDefinitionUnionTypeDef = Union[
    ModelPackageContainerDefinitionTypeDef, ModelPackageContainerDefinitionOutputTypeDef
]


class SourceAlgorithmSpecificationOutputTypeDef(TypedDict):
    SourceAlgorithms: List[SourceAlgorithmTypeDef]


class SourceAlgorithmSpecificationTypeDef(TypedDict):
    SourceAlgorithms: Sequence[SourceAlgorithmTypeDef]


class CreateOptimizationJobRequestRequestTypeDef(TypedDict):
    OptimizationJobName: str
    RoleArn: str
    ModelSource: OptimizationJobModelSourceTypeDef
    DeploymentInstanceType: OptimizationJobDeploymentInstanceTypeType
    OptimizationConfigs: Sequence[OptimizationConfigUnionTypeDef]
    OutputConfig: OptimizationJobOutputConfigTypeDef
    StoppingCondition: StoppingConditionTypeDef
    OptimizationEnvironment: NotRequired[Mapping[str, str]]
    Tags: NotRequired[Sequence[TagTypeDef]]
    VpcConfig: NotRequired[OptimizationVpcConfigTypeDef]


class DescribeDataQualityJobDefinitionResponseTypeDef(TypedDict):
    JobDefinitionArn: str
    JobDefinitionName: str
    CreationTime: datetime
    DataQualityBaselineConfig: DataQualityBaselineConfigTypeDef
    DataQualityAppSpecification: DataQualityAppSpecificationOutputTypeDef
    DataQualityJobInput: DataQualityJobInputOutputTypeDef
    DataQualityJobOutputConfig: MonitoringOutputConfigOutputTypeDef
    JobResources: MonitoringResourcesTypeDef
    NetworkConfig: MonitoringNetworkConfigOutputTypeDef
    RoleArn: str
    StoppingCondition: MonitoringStoppingConditionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeModelBiasJobDefinitionResponseTypeDef(TypedDict):
    JobDefinitionArn: str
    JobDefinitionName: str
    CreationTime: datetime
    ModelBiasBaselineConfig: ModelBiasBaselineConfigTypeDef
    ModelBiasAppSpecification: ModelBiasAppSpecificationOutputTypeDef
    ModelBiasJobInput: ModelBiasJobInputOutputTypeDef
    ModelBiasJobOutputConfig: MonitoringOutputConfigOutputTypeDef
    JobResources: MonitoringResourcesTypeDef
    NetworkConfig: MonitoringNetworkConfigOutputTypeDef
    RoleArn: str
    StoppingCondition: MonitoringStoppingConditionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeModelExplainabilityJobDefinitionResponseTypeDef(TypedDict):
    JobDefinitionArn: str
    JobDefinitionName: str
    CreationTime: datetime
    ModelExplainabilityBaselineConfig: ModelExplainabilityBaselineConfigTypeDef
    ModelExplainabilityAppSpecification: ModelExplainabilityAppSpecificationOutputTypeDef
    ModelExplainabilityJobInput: ModelExplainabilityJobInputOutputTypeDef
    ModelExplainabilityJobOutputConfig: MonitoringOutputConfigOutputTypeDef
    JobResources: MonitoringResourcesTypeDef
    NetworkConfig: MonitoringNetworkConfigOutputTypeDef
    RoleArn: str
    StoppingCondition: MonitoringStoppingConditionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeModelQualityJobDefinitionResponseTypeDef(TypedDict):
    JobDefinitionArn: str
    JobDefinitionName: str
    CreationTime: datetime
    ModelQualityBaselineConfig: ModelQualityBaselineConfigTypeDef
    ModelQualityAppSpecification: ModelQualityAppSpecificationOutputTypeDef
    ModelQualityJobInput: ModelQualityJobInputOutputTypeDef
    ModelQualityJobOutputConfig: MonitoringOutputConfigOutputTypeDef
    JobResources: MonitoringResourcesTypeDef
    NetworkConfig: MonitoringNetworkConfigOutputTypeDef
    RoleArn: str
    StoppingCondition: MonitoringStoppingConditionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class MonitoringJobDefinitionOutputTypeDef(TypedDict):
    MonitoringInputs: List[MonitoringInputOutputTypeDef]
    MonitoringOutputConfig: MonitoringOutputConfigOutputTypeDef
    MonitoringResources: MonitoringResourcesTypeDef
    MonitoringAppSpecification: MonitoringAppSpecificationOutputTypeDef
    RoleArn: str
    BaselineConfig: NotRequired[MonitoringBaselineConfigTypeDef]
    StoppingCondition: NotRequired[MonitoringStoppingConditionTypeDef]
    Environment: NotRequired[Dict[str, str]]
    NetworkConfig: NotRequired[NetworkConfigOutputTypeDef]


BatchTransformInputUnionTypeDef = Union[
    BatchTransformInputTypeDef, BatchTransformInputOutputTypeDef
]


class CreateWorkteamRequestRequestTypeDef(TypedDict):
    WorkteamName: str
    MemberDefinitions: Sequence[MemberDefinitionUnionTypeDef]
    Description: str
    WorkforceName: NotRequired[str]
    NotificationConfiguration: NotRequired[NotificationConfigurationTypeDef]
    WorkerAccessConfiguration: NotRequired[WorkerAccessConfigurationTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]


ChannelTypeDef = TypedDict(
    "ChannelTypeDef",
    {
        "ChannelName": str,
        "DataSource": DataSourceUnionTypeDef,
        "ContentType": NotRequired[str],
        "CompressionType": NotRequired[CompressionTypeType],
        "RecordWrapperType": NotRequired[RecordWrapperType],
        "InputMode": NotRequired[TrainingInputModeType],
        "ShuffleConfig": NotRequired[ShuffleConfigTypeDef],
    },
)


class DescribeSpaceResponseTypeDef(TypedDict):
    DomainId: str
    SpaceArn: str
    SpaceName: str
    HomeEfsFileSystemUid: str
    Status: SpaceStatusType
    LastModifiedTime: datetime
    CreationTime: datetime
    FailureReason: str
    SpaceSettings: SpaceSettingsOutputTypeDef
    OwnershipSettings: OwnershipSettingsTypeDef
    SpaceSharingSettings: SpaceSharingSettingsTypeDef
    SpaceDisplayName: str
    Url: str
    ResponseMetadata: ResponseMetadataTypeDef


class SpaceSettingsTypeDef(TypedDict):
    JupyterServerAppSettings: NotRequired[JupyterServerAppSettingsUnionTypeDef]
    KernelGatewayAppSettings: NotRequired[KernelGatewayAppSettingsUnionTypeDef]
    CodeEditorAppSettings: NotRequired[SpaceCodeEditorAppSettingsTypeDef]
    JupyterLabAppSettings: NotRequired[SpaceJupyterLabAppSettingsUnionTypeDef]
    AppType: NotRequired[AppTypeType]
    SpaceStorageSettings: NotRequired[SpaceStorageSettingsTypeDef]
    CustomFileSystems: NotRequired[Sequence[CustomFileSystemTypeDef]]


class AlgorithmValidationProfileOutputTypeDef(TypedDict):
    ProfileName: str
    TrainingJobDefinition: TrainingJobDefinitionOutputTypeDef
    TransformJobDefinition: NotRequired[TransformJobDefinitionOutputTypeDef]


class ModelPackageValidationProfileOutputTypeDef(TypedDict):
    ProfileName: str
    TransformJobDefinition: TransformJobDefinitionOutputTypeDef


TransformJobDefinitionUnionTypeDef = Union[
    TransformJobDefinitionTypeDef, TransformJobDefinitionOutputTypeDef
]


class TrialComponentSourceDetailTypeDef(TypedDict):
    SourceArn: NotRequired[str]
    TrainingJob: NotRequired[TrainingJobTypeDef]
    ProcessingJob: NotRequired[ProcessingJobTypeDef]
    TransformJob: NotRequired[TransformJobTypeDef]


TabularJobConfigUnionTypeDef = Union[TabularJobConfigTypeDef, TabularJobConfigOutputTypeDef]
TimeSeriesForecastingJobConfigUnionTypeDef = Union[
    TimeSeriesForecastingJobConfigTypeDef, TimeSeriesForecastingJobConfigOutputTypeDef
]
HyperParameterSpecificationUnionTypeDef = Union[
    HyperParameterSpecificationTypeDef, HyperParameterSpecificationOutputTypeDef
]
EndpointInputConfigurationUnionTypeDef = Union[
    EndpointInputConfigurationTypeDef, EndpointInputConfigurationOutputTypeDef
]


class CreateEndpointConfigInputRequestTypeDef(TypedDict):
    EndpointConfigName: str
    ProductionVariants: Sequence[ProductionVariantTypeDef]
    DataCaptureConfig: NotRequired[DataCaptureConfigTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]
    KmsKeyId: NotRequired[str]
    AsyncInferenceConfig: NotRequired[AsyncInferenceConfigTypeDef]
    ExplainerConfig: NotRequired[ExplainerConfigTypeDef]
    ShadowProductionVariants: NotRequired[Sequence[ProductionVariantTypeDef]]
    ExecutionRoleArn: NotRequired[str]
    VpcConfig: NotRequired[VpcConfigTypeDef]
    EnableNetworkIsolation: NotRequired[bool]


class CreateAutoMLJobRequestRequestTypeDef(TypedDict):
    AutoMLJobName: str
    InputDataConfig: Sequence[AutoMLChannelTypeDef]
    OutputDataConfig: AutoMLOutputDataConfigTypeDef
    RoleArn: str
    ProblemType: NotRequired[ProblemTypeType]
    AutoMLJobObjective: NotRequired[AutoMLJobObjectiveTypeDef]
    AutoMLJobConfig: NotRequired[AutoMLJobConfigTypeDef]
    GenerateCandidateDefinitionsOnly: NotRequired[bool]
    Tags: NotRequired[Sequence[TagTypeDef]]
    ModelDeployConfig: NotRequired[ModelDeployConfigTypeDef]


class CreateLabelingJobRequestRequestTypeDef(TypedDict):
    LabelingJobName: str
    LabelAttributeName: str
    InputConfig: LabelingJobInputConfigTypeDef
    OutputConfig: LabelingJobOutputConfigTypeDef
    RoleArn: str
    HumanTaskConfig: HumanTaskConfigTypeDef
    LabelCategoryConfigS3Uri: NotRequired[str]
    StoppingConditions: NotRequired[LabelingJobStoppingConditionsTypeDef]
    LabelingJobAlgorithmsConfig: NotRequired[LabelingJobAlgorithmsConfigTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateDomainRequestRequestTypeDef(TypedDict):
    DomainName: str
    AuthMode: AuthModeType
    DefaultUserSettings: UserSettingsTypeDef
    SubnetIds: Sequence[str]
    VpcId: str
    DomainSettings: NotRequired[DomainSettingsTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]
    AppNetworkAccessType: NotRequired[AppNetworkAccessTypeType]
    HomeEfsFileSystemKmsKeyId: NotRequired[str]
    KmsKeyId: NotRequired[str]
    AppSecurityGroupManagement: NotRequired[AppSecurityGroupManagementType]
    TagPropagation: NotRequired[TagPropagationType]
    DefaultSpaceSettings: NotRequired[DefaultSpaceSettingsTypeDef]


class CreateUserProfileRequestRequestTypeDef(TypedDict):
    DomainId: str
    UserProfileName: str
    SingleSignOnUserIdentifier: NotRequired[str]
    SingleSignOnUserValue: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]
    UserSettings: NotRequired[UserSettingsTypeDef]


class UpdateDomainRequestRequestTypeDef(TypedDict):
    DomainId: str
    DefaultUserSettings: NotRequired[UserSettingsTypeDef]
    DomainSettingsForUpdate: NotRequired[DomainSettingsForUpdateTypeDef]
    AppSecurityGroupManagement: NotRequired[AppSecurityGroupManagementType]
    DefaultSpaceSettings: NotRequired[DefaultSpaceSettingsTypeDef]
    SubnetIds: NotRequired[Sequence[str]]
    AppNetworkAccessType: NotRequired[AppNetworkAccessTypeType]
    TagPropagation: NotRequired[TagPropagationType]


class UpdateUserProfileRequestRequestTypeDef(TypedDict):
    DomainId: str
    UserProfileName: str
    UserSettings: NotRequired[UserSettingsTypeDef]


class GetScalingConfigurationRecommendationResponseTypeDef(TypedDict):
    InferenceRecommendationsJobName: str
    RecommendationId: str
    EndpointName: str
    TargetCpuUtilizationPerCore: int
    ScalingPolicyObjective: ScalingPolicyObjectiveTypeDef
    Metric: ScalingPolicyMetricTypeDef
    DynamicScalingConfiguration: DynamicScalingConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateModelInputRequestTypeDef(TypedDict):
    ModelName: str
    PrimaryContainer: NotRequired[ContainerDefinitionTypeDef]
    Containers: NotRequired[Sequence[ContainerDefinitionUnionTypeDef]]
    InferenceExecutionConfig: NotRequired[InferenceExecutionConfigTypeDef]
    ExecutionRoleArn: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]
    VpcConfig: NotRequired[VpcConfigTypeDef]
    EnableNetworkIsolation: NotRequired[bool]


class BatchDescribeModelPackageSummaryTypeDef(TypedDict):
    ModelPackageGroupName: str
    ModelPackageArn: str
    CreationTime: datetime
    InferenceSpecification: InferenceSpecificationOutputTypeDef
    ModelPackageStatus: ModelPackageStatusType
    ModelPackageVersion: NotRequired[int]
    ModelPackageDescription: NotRequired[str]
    ModelApprovalStatus: NotRequired[ModelApprovalStatusType]


class AdditionalInferenceSpecificationDefinitionTypeDef(TypedDict):
    Name: str
    Containers: Sequence[ModelPackageContainerDefinitionUnionTypeDef]
    Description: NotRequired[str]
    SupportedTransformInstanceTypes: NotRequired[Sequence[TransformInstanceTypeType]]
    SupportedRealtimeInferenceInstanceTypes: NotRequired[
        Sequence[ProductionVariantInstanceTypeType]
    ]
    SupportedContentTypes: NotRequired[Sequence[str]]
    SupportedResponseMIMETypes: NotRequired[Sequence[str]]


class InferenceSpecificationTypeDef(TypedDict):
    Containers: Sequence[ModelPackageContainerDefinitionUnionTypeDef]
    SupportedTransformInstanceTypes: NotRequired[Sequence[TransformInstanceTypeType]]
    SupportedRealtimeInferenceInstanceTypes: NotRequired[
        Sequence[ProductionVariantInstanceTypeType]
    ]
    SupportedContentTypes: NotRequired[Sequence[str]]
    SupportedResponseMIMETypes: NotRequired[Sequence[str]]


class MonitoringScheduleConfigOutputTypeDef(TypedDict):
    ScheduleConfig: NotRequired[ScheduleConfigTypeDef]
    MonitoringJobDefinition: NotRequired[MonitoringJobDefinitionOutputTypeDef]
    MonitoringJobDefinitionName: NotRequired[str]
    MonitoringType: NotRequired[MonitoringTypeType]


class DataQualityJobInputTypeDef(TypedDict):
    EndpointInput: NotRequired[EndpointInputTypeDef]
    BatchTransformInput: NotRequired[BatchTransformInputUnionTypeDef]


class ModelBiasJobInputTypeDef(TypedDict):
    GroundTruthS3Input: MonitoringGroundTruthS3InputTypeDef
    EndpointInput: NotRequired[EndpointInputTypeDef]
    BatchTransformInput: NotRequired[BatchTransformInputUnionTypeDef]


class ModelExplainabilityJobInputTypeDef(TypedDict):
    EndpointInput: NotRequired[EndpointInputTypeDef]
    BatchTransformInput: NotRequired[BatchTransformInputUnionTypeDef]


class ModelQualityJobInputTypeDef(TypedDict):
    GroundTruthS3Input: MonitoringGroundTruthS3InputTypeDef
    EndpointInput: NotRequired[EndpointInputTypeDef]
    BatchTransformInput: NotRequired[BatchTransformInputUnionTypeDef]


class MonitoringInputTypeDef(TypedDict):
    EndpointInput: NotRequired[EndpointInputTypeDef]
    BatchTransformInput: NotRequired[BatchTransformInputUnionTypeDef]


ChannelUnionTypeDef = Union[ChannelTypeDef, ChannelOutputTypeDef]


class CreateSpaceRequestRequestTypeDef(TypedDict):
    DomainId: str
    SpaceName: str
    Tags: NotRequired[Sequence[TagTypeDef]]
    SpaceSettings: NotRequired[SpaceSettingsTypeDef]
    OwnershipSettings: NotRequired[OwnershipSettingsTypeDef]
    SpaceSharingSettings: NotRequired[SpaceSharingSettingsTypeDef]
    SpaceDisplayName: NotRequired[str]


class UpdateSpaceRequestRequestTypeDef(TypedDict):
    DomainId: str
    SpaceName: str
    SpaceSettings: NotRequired[SpaceSettingsTypeDef]
    SpaceDisplayName: NotRequired[str]


class AlgorithmValidationSpecificationOutputTypeDef(TypedDict):
    ValidationRole: str
    ValidationProfiles: List[AlgorithmValidationProfileOutputTypeDef]


class ModelPackageValidationSpecificationOutputTypeDef(TypedDict):
    ValidationRole: str
    ValidationProfiles: List[ModelPackageValidationProfileOutputTypeDef]


class ModelPackageValidationProfileTypeDef(TypedDict):
    ProfileName: str
    TransformJobDefinition: TransformJobDefinitionUnionTypeDef


class TrialComponentTypeDef(TypedDict):
    TrialComponentName: NotRequired[str]
    DisplayName: NotRequired[str]
    TrialComponentArn: NotRequired[str]
    Source: NotRequired[TrialComponentSourceTypeDef]
    Status: NotRequired[TrialComponentStatusTypeDef]
    StartTime: NotRequired[datetime]
    EndTime: NotRequired[datetime]
    CreationTime: NotRequired[datetime]
    CreatedBy: NotRequired[UserContextTypeDef]
    LastModifiedTime: NotRequired[datetime]
    LastModifiedBy: NotRequired[UserContextTypeDef]
    Parameters: NotRequired[Dict[str, TrialComponentParameterValueTypeDef]]
    InputArtifacts: NotRequired[Dict[str, TrialComponentArtifactTypeDef]]
    OutputArtifacts: NotRequired[Dict[str, TrialComponentArtifactTypeDef]]
    Metrics: NotRequired[List[TrialComponentMetricSummaryTypeDef]]
    MetadataProperties: NotRequired[MetadataPropertiesTypeDef]
    SourceDetail: NotRequired[TrialComponentSourceDetailTypeDef]
    LineageGroupArn: NotRequired[str]
    Tags: NotRequired[List[TagTypeDef]]
    Parents: NotRequired[List[ParentTypeDef]]
    RunName: NotRequired[str]


class AutoMLProblemTypeConfigTypeDef(TypedDict):
    ImageClassificationJobConfig: NotRequired[ImageClassificationJobConfigTypeDef]
    TextClassificationJobConfig: NotRequired[TextClassificationJobConfigTypeDef]
    TimeSeriesForecastingJobConfig: NotRequired[TimeSeriesForecastingJobConfigUnionTypeDef]
    TabularJobConfig: NotRequired[TabularJobConfigUnionTypeDef]
    TextGenerationJobConfig: NotRequired[TextGenerationJobConfigUnionTypeDef]


class TrainingSpecificationTypeDef(TypedDict):
    TrainingImage: str
    SupportedTrainingInstanceTypes: Sequence[TrainingInstanceTypeType]
    TrainingChannels: Sequence[ChannelSpecificationUnionTypeDef]
    TrainingImageDigest: NotRequired[str]
    SupportedHyperParameters: NotRequired[Sequence[HyperParameterSpecificationUnionTypeDef]]
    SupportsDistributedTraining: NotRequired[bool]
    MetricDefinitions: NotRequired[Sequence[MetricDefinitionTypeDef]]
    SupportedTuningJobObjectiveMetrics: NotRequired[
        Sequence[HyperParameterTuningJobObjectiveTypeDef]
    ]
    AdditionalS3DataSource: NotRequired[AdditionalS3DataSourceTypeDef]


class RecommendationJobInputConfigTypeDef(TypedDict):
    ModelPackageVersionArn: NotRequired[str]
    ModelName: NotRequired[str]
    JobDurationInSeconds: NotRequired[int]
    TrafficPattern: NotRequired[TrafficPatternUnionTypeDef]
    ResourceLimit: NotRequired[RecommendationJobResourceLimitTypeDef]
    EndpointConfigurations: NotRequired[Sequence[EndpointInputConfigurationUnionTypeDef]]
    VolumeKmsKeyId: NotRequired[str]
    ContainerConfig: NotRequired[RecommendationJobContainerConfigUnionTypeDef]
    Endpoints: NotRequired[Sequence[EndpointInfoTypeDef]]
    VpcConfig: NotRequired[RecommendationJobVpcConfigUnionTypeDef]


class BatchDescribeModelPackageOutputTypeDef(TypedDict):
    ModelPackageSummaries: Dict[str, BatchDescribeModelPackageSummaryTypeDef]
    BatchDescribeModelPackageErrorMap: Dict[str, BatchDescribeModelPackageErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


AdditionalInferenceSpecificationDefinitionUnionTypeDef = Union[
    AdditionalInferenceSpecificationDefinitionTypeDef,
    AdditionalInferenceSpecificationDefinitionOutputTypeDef,
]


class UpdateModelPackageInputRequestTypeDef(TypedDict):
    ModelPackageArn: str
    ModelApprovalStatus: NotRequired[ModelApprovalStatusType]
    ApprovalDescription: NotRequired[str]
    CustomerMetadataProperties: NotRequired[Mapping[str, str]]
    CustomerMetadataPropertiesToRemove: NotRequired[Sequence[str]]
    AdditionalInferenceSpecificationsToAdd: NotRequired[
        Sequence[AdditionalInferenceSpecificationDefinitionTypeDef]
    ]
    InferenceSpecification: NotRequired[InferenceSpecificationTypeDef]
    SourceUri: NotRequired[str]
    ModelCard: NotRequired[ModelPackageModelCardTypeDef]
    ModelLifeCycle: NotRequired[ModelLifeCycleTypeDef]
    ClientToken: NotRequired[str]


class DescribeMonitoringScheduleResponseTypeDef(TypedDict):
    MonitoringScheduleArn: str
    MonitoringScheduleName: str
    MonitoringScheduleStatus: ScheduleStatusType
    MonitoringType: MonitoringTypeType
    FailureReason: str
    CreationTime: datetime
    LastModifiedTime: datetime
    MonitoringScheduleConfig: MonitoringScheduleConfigOutputTypeDef
    EndpointName: str
    LastMonitoringExecutionSummary: MonitoringExecutionSummaryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ModelDashboardMonitoringScheduleTypeDef(TypedDict):
    MonitoringScheduleArn: NotRequired[str]
    MonitoringScheduleName: NotRequired[str]
    MonitoringScheduleStatus: NotRequired[ScheduleStatusType]
    MonitoringType: NotRequired[MonitoringTypeType]
    FailureReason: NotRequired[str]
    CreationTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]
    MonitoringScheduleConfig: NotRequired[MonitoringScheduleConfigOutputTypeDef]
    EndpointName: NotRequired[str]
    MonitoringAlertSummaries: NotRequired[List[MonitoringAlertSummaryTypeDef]]
    LastMonitoringExecutionSummary: NotRequired[MonitoringExecutionSummaryTypeDef]
    BatchTransformInput: NotRequired[BatchTransformInputOutputTypeDef]


class MonitoringScheduleTypeDef(TypedDict):
    MonitoringScheduleArn: NotRequired[str]
    MonitoringScheduleName: NotRequired[str]
    MonitoringScheduleStatus: NotRequired[ScheduleStatusType]
    MonitoringType: NotRequired[MonitoringTypeType]
    FailureReason: NotRequired[str]
    CreationTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]
    MonitoringScheduleConfig: NotRequired[MonitoringScheduleConfigOutputTypeDef]
    EndpointName: NotRequired[str]
    LastMonitoringExecutionSummary: NotRequired[MonitoringExecutionSummaryTypeDef]
    Tags: NotRequired[List[TagTypeDef]]


class CreateDataQualityJobDefinitionRequestRequestTypeDef(TypedDict):
    JobDefinitionName: str
    DataQualityAppSpecification: DataQualityAppSpecificationTypeDef
    DataQualityJobInput: DataQualityJobInputTypeDef
    DataQualityJobOutputConfig: MonitoringOutputConfigTypeDef
    JobResources: MonitoringResourcesTypeDef
    RoleArn: str
    DataQualityBaselineConfig: NotRequired[DataQualityBaselineConfigTypeDef]
    NetworkConfig: NotRequired[MonitoringNetworkConfigTypeDef]
    StoppingCondition: NotRequired[MonitoringStoppingConditionTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateModelBiasJobDefinitionRequestRequestTypeDef(TypedDict):
    JobDefinitionName: str
    ModelBiasAppSpecification: ModelBiasAppSpecificationTypeDef
    ModelBiasJobInput: ModelBiasJobInputTypeDef
    ModelBiasJobOutputConfig: MonitoringOutputConfigTypeDef
    JobResources: MonitoringResourcesTypeDef
    RoleArn: str
    ModelBiasBaselineConfig: NotRequired[ModelBiasBaselineConfigTypeDef]
    NetworkConfig: NotRequired[MonitoringNetworkConfigTypeDef]
    StoppingCondition: NotRequired[MonitoringStoppingConditionTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateModelExplainabilityJobDefinitionRequestRequestTypeDef(TypedDict):
    JobDefinitionName: str
    ModelExplainabilityAppSpecification: ModelExplainabilityAppSpecificationTypeDef
    ModelExplainabilityJobInput: ModelExplainabilityJobInputTypeDef
    ModelExplainabilityJobOutputConfig: MonitoringOutputConfigTypeDef
    JobResources: MonitoringResourcesTypeDef
    RoleArn: str
    ModelExplainabilityBaselineConfig: NotRequired[ModelExplainabilityBaselineConfigTypeDef]
    NetworkConfig: NotRequired[MonitoringNetworkConfigTypeDef]
    StoppingCondition: NotRequired[MonitoringStoppingConditionTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateModelQualityJobDefinitionRequestRequestTypeDef(TypedDict):
    JobDefinitionName: str
    ModelQualityAppSpecification: ModelQualityAppSpecificationTypeDef
    ModelQualityJobInput: ModelQualityJobInputTypeDef
    ModelQualityJobOutputConfig: MonitoringOutputConfigTypeDef
    JobResources: MonitoringResourcesTypeDef
    RoleArn: str
    ModelQualityBaselineConfig: NotRequired[ModelQualityBaselineConfigTypeDef]
    NetworkConfig: NotRequired[MonitoringNetworkConfigTypeDef]
    StoppingCondition: NotRequired[MonitoringStoppingConditionTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]


MonitoringInputUnionTypeDef = Union[MonitoringInputTypeDef, MonitoringInputOutputTypeDef]


class CreateTrainingJobRequestRequestTypeDef(TypedDict):
    TrainingJobName: str
    AlgorithmSpecification: AlgorithmSpecificationTypeDef
    RoleArn: str
    OutputDataConfig: OutputDataConfigTypeDef
    ResourceConfig: ResourceConfigTypeDef
    StoppingCondition: StoppingConditionTypeDef
    HyperParameters: NotRequired[Mapping[str, str]]
    InputDataConfig: NotRequired[Sequence[ChannelUnionTypeDef]]
    VpcConfig: NotRequired[VpcConfigTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]
    EnableNetworkIsolation: NotRequired[bool]
    EnableInterContainerTrafficEncryption: NotRequired[bool]
    EnableManagedSpotTraining: NotRequired[bool]
    CheckpointConfig: NotRequired[CheckpointConfigTypeDef]
    DebugHookConfig: NotRequired[DebugHookConfigTypeDef]
    DebugRuleConfigurations: NotRequired[Sequence[DebugRuleConfigurationUnionTypeDef]]
    TensorBoardOutputConfig: NotRequired[TensorBoardOutputConfigTypeDef]
    ExperimentConfig: NotRequired[ExperimentConfigTypeDef]
    ProfilerConfig: NotRequired[ProfilerConfigTypeDef]
    ProfilerRuleConfigurations: NotRequired[Sequence[ProfilerRuleConfigurationUnionTypeDef]]
    Environment: NotRequired[Mapping[str, str]]
    RetryStrategy: NotRequired[RetryStrategyTypeDef]
    RemoteDebugConfig: NotRequired[RemoteDebugConfigTypeDef]
    InfraCheckConfig: NotRequired[InfraCheckConfigTypeDef]
    SessionChainingConfig: NotRequired[SessionChainingConfigTypeDef]


class HyperParameterTrainingJobDefinitionTypeDef(TypedDict):
    AlgorithmSpecification: HyperParameterAlgorithmSpecificationUnionTypeDef
    RoleArn: str
    OutputDataConfig: OutputDataConfigTypeDef
    StoppingCondition: StoppingConditionTypeDef
    DefinitionName: NotRequired[str]
    TuningObjective: NotRequired[HyperParameterTuningJobObjectiveTypeDef]
    HyperParameterRanges: NotRequired[ParameterRangesUnionTypeDef]
    StaticHyperParameters: NotRequired[Mapping[str, str]]
    InputDataConfig: NotRequired[Sequence[ChannelUnionTypeDef]]
    VpcConfig: NotRequired[VpcConfigUnionTypeDef]
    ResourceConfig: NotRequired[ResourceConfigUnionTypeDef]
    HyperParameterTuningResourceConfig: NotRequired[HyperParameterTuningResourceConfigUnionTypeDef]
    EnableNetworkIsolation: NotRequired[bool]
    EnableInterContainerTrafficEncryption: NotRequired[bool]
    EnableManagedSpotTraining: NotRequired[bool]
    CheckpointConfig: NotRequired[CheckpointConfigTypeDef]
    RetryStrategy: NotRequired[RetryStrategyTypeDef]
    Environment: NotRequired[Mapping[str, str]]


class TrainingJobDefinitionTypeDef(TypedDict):
    TrainingInputMode: TrainingInputModeType
    InputDataConfig: Sequence[ChannelUnionTypeDef]
    OutputDataConfig: OutputDataConfigTypeDef
    ResourceConfig: ResourceConfigUnionTypeDef
    StoppingCondition: StoppingConditionTypeDef
    HyperParameters: NotRequired[Mapping[str, str]]


class DescribeAlgorithmOutputTypeDef(TypedDict):
    AlgorithmName: str
    AlgorithmArn: str
    AlgorithmDescription: str
    CreationTime: datetime
    TrainingSpecification: TrainingSpecificationOutputTypeDef
    InferenceSpecification: InferenceSpecificationOutputTypeDef
    ValidationSpecification: AlgorithmValidationSpecificationOutputTypeDef
    AlgorithmStatus: AlgorithmStatusType
    AlgorithmStatusDetails: AlgorithmStatusDetailsTypeDef
    ProductId: str
    CertifyForMarketplace: bool
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeModelPackageOutputTypeDef(TypedDict):
    ModelPackageName: str
    ModelPackageGroupName: str
    ModelPackageVersion: int
    ModelPackageArn: str
    ModelPackageDescription: str
    CreationTime: datetime
    InferenceSpecification: InferenceSpecificationOutputTypeDef
    SourceAlgorithmSpecification: SourceAlgorithmSpecificationOutputTypeDef
    ValidationSpecification: ModelPackageValidationSpecificationOutputTypeDef
    ModelPackageStatus: ModelPackageStatusType
    ModelPackageStatusDetails: ModelPackageStatusDetailsTypeDef
    CertifyForMarketplace: bool
    ModelApprovalStatus: ModelApprovalStatusType
    CreatedBy: UserContextTypeDef
    MetadataProperties: MetadataPropertiesTypeDef
    ModelMetrics: ModelMetricsTypeDef
    LastModifiedTime: datetime
    LastModifiedBy: UserContextTypeDef
    ApprovalDescription: str
    Domain: str
    Task: str
    SamplePayloadUrl: str
    CustomerMetadataProperties: Dict[str, str]
    DriftCheckBaselines: DriftCheckBaselinesTypeDef
    AdditionalInferenceSpecifications: List[AdditionalInferenceSpecificationDefinitionOutputTypeDef]
    SkipModelValidation: SkipModelValidationType
    SourceUri: str
    SecurityConfig: ModelPackageSecurityConfigTypeDef
    ModelCard: ModelPackageModelCardTypeDef
    ModelLifeCycle: ModelLifeCycleTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ModelPackageTypeDef(TypedDict):
    ModelPackageName: NotRequired[str]
    ModelPackageGroupName: NotRequired[str]
    ModelPackageVersion: NotRequired[int]
    ModelPackageArn: NotRequired[str]
    ModelPackageDescription: NotRequired[str]
    CreationTime: NotRequired[datetime]
    InferenceSpecification: NotRequired[InferenceSpecificationOutputTypeDef]
    SourceAlgorithmSpecification: NotRequired[SourceAlgorithmSpecificationOutputTypeDef]
    ValidationSpecification: NotRequired[ModelPackageValidationSpecificationOutputTypeDef]
    ModelPackageStatus: NotRequired[ModelPackageStatusType]
    ModelPackageStatusDetails: NotRequired[ModelPackageStatusDetailsTypeDef]
    CertifyForMarketplace: NotRequired[bool]
    ModelApprovalStatus: NotRequired[ModelApprovalStatusType]
    CreatedBy: NotRequired[UserContextTypeDef]
    MetadataProperties: NotRequired[MetadataPropertiesTypeDef]
    ModelMetrics: NotRequired[ModelMetricsTypeDef]
    LastModifiedTime: NotRequired[datetime]
    LastModifiedBy: NotRequired[UserContextTypeDef]
    ApprovalDescription: NotRequired[str]
    Domain: NotRequired[str]
    Task: NotRequired[str]
    SamplePayloadUrl: NotRequired[str]
    AdditionalInferenceSpecifications: NotRequired[
        List[AdditionalInferenceSpecificationDefinitionOutputTypeDef]
    ]
    SourceUri: NotRequired[str]
    SecurityConfig: NotRequired[ModelPackageSecurityConfigTypeDef]
    ModelCard: NotRequired[ModelPackageModelCardTypeDef]
    ModelLifeCycle: NotRequired[ModelLifeCycleTypeDef]
    Tags: NotRequired[List[TagTypeDef]]
    CustomerMetadataProperties: NotRequired[Dict[str, str]]
    DriftCheckBaselines: NotRequired[DriftCheckBaselinesTypeDef]
    SkipModelValidation: NotRequired[SkipModelValidationType]


ModelPackageValidationProfileUnionTypeDef = Union[
    ModelPackageValidationProfileTypeDef, ModelPackageValidationProfileOutputTypeDef
]


class CreateAutoMLJobV2RequestRequestTypeDef(TypedDict):
    AutoMLJobName: str
    AutoMLJobInputDataConfig: Sequence[AutoMLJobChannelTypeDef]
    OutputDataConfig: AutoMLOutputDataConfigTypeDef
    AutoMLProblemTypeConfig: AutoMLProblemTypeConfigTypeDef
    RoleArn: str
    Tags: NotRequired[Sequence[TagTypeDef]]
    SecurityConfig: NotRequired[AutoMLSecurityConfigTypeDef]
    AutoMLJobObjective: NotRequired[AutoMLJobObjectiveTypeDef]
    ModelDeployConfig: NotRequired[ModelDeployConfigTypeDef]
    DataSplitConfig: NotRequired[AutoMLDataSplitConfigTypeDef]
    AutoMLComputeConfig: NotRequired[AutoMLComputeConfigTypeDef]


class CreateInferenceRecommendationsJobRequestRequestTypeDef(TypedDict):
    JobName: str
    JobType: RecommendationJobTypeType
    RoleArn: str
    InputConfig: RecommendationJobInputConfigTypeDef
    JobDescription: NotRequired[str]
    StoppingConditions: NotRequired[RecommendationJobStoppingConditionsTypeDef]
    OutputConfig: NotRequired[RecommendationJobOutputConfigTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]


class ModelDashboardModelTypeDef(TypedDict):
    Model: NotRequired[ModelTypeDef]
    Endpoints: NotRequired[List[ModelDashboardEndpointTypeDef]]
    LastBatchTransformJob: NotRequired[TransformJobTypeDef]
    MonitoringSchedules: NotRequired[List[ModelDashboardMonitoringScheduleTypeDef]]
    ModelCard: NotRequired[ModelDashboardModelCardTypeDef]


class EndpointTypeDef(TypedDict):
    EndpointName: str
    EndpointArn: str
    EndpointConfigName: str
    EndpointStatus: EndpointStatusType
    CreationTime: datetime
    LastModifiedTime: datetime
    ProductionVariants: NotRequired[List[ProductionVariantSummaryTypeDef]]
    DataCaptureConfig: NotRequired[DataCaptureConfigSummaryTypeDef]
    FailureReason: NotRequired[str]
    MonitoringSchedules: NotRequired[List[MonitoringScheduleTypeDef]]
    Tags: NotRequired[List[TagTypeDef]]
    ShadowProductionVariants: NotRequired[List[ProductionVariantSummaryTypeDef]]


class MonitoringJobDefinitionTypeDef(TypedDict):
    MonitoringInputs: Sequence[MonitoringInputUnionTypeDef]
    MonitoringOutputConfig: MonitoringOutputConfigUnionTypeDef
    MonitoringResources: MonitoringResourcesTypeDef
    MonitoringAppSpecification: MonitoringAppSpecificationUnionTypeDef
    RoleArn: str
    BaselineConfig: NotRequired[MonitoringBaselineConfigTypeDef]
    StoppingCondition: NotRequired[MonitoringStoppingConditionTypeDef]
    Environment: NotRequired[Mapping[str, str]]
    NetworkConfig: NotRequired[NetworkConfigUnionTypeDef]


HyperParameterTrainingJobDefinitionUnionTypeDef = Union[
    HyperParameterTrainingJobDefinitionTypeDef, HyperParameterTrainingJobDefinitionOutputTypeDef
]
TrainingJobDefinitionUnionTypeDef = Union[
    TrainingJobDefinitionTypeDef, TrainingJobDefinitionOutputTypeDef
]


class ModelPackageValidationSpecificationTypeDef(TypedDict):
    ValidationRole: str
    ValidationProfiles: Sequence[ModelPackageValidationProfileUnionTypeDef]


class SearchRecordTypeDef(TypedDict):
    TrainingJob: NotRequired[TrainingJobTypeDef]
    Experiment: NotRequired[ExperimentTypeDef]
    Trial: NotRequired[TrialTypeDef]
    TrialComponent: NotRequired[TrialComponentTypeDef]
    Endpoint: NotRequired[EndpointTypeDef]
    ModelPackage: NotRequired[ModelPackageTypeDef]
    ModelPackageGroup: NotRequired[ModelPackageGroupTypeDef]
    Pipeline: NotRequired[PipelineTypeDef]
    PipelineExecution: NotRequired[PipelineExecutionTypeDef]
    FeatureGroup: NotRequired[FeatureGroupTypeDef]
    FeatureMetadata: NotRequired[FeatureMetadataTypeDef]
    Project: NotRequired[ProjectTypeDef]
    HyperParameterTuningJob: NotRequired[HyperParameterTuningJobSearchEntityTypeDef]
    ModelCard: NotRequired[ModelCardTypeDef]
    Model: NotRequired[ModelDashboardModelTypeDef]


MonitoringJobDefinitionUnionTypeDef = Union[
    MonitoringJobDefinitionTypeDef, MonitoringJobDefinitionOutputTypeDef
]


class CreateHyperParameterTuningJobRequestRequestTypeDef(TypedDict):
    HyperParameterTuningJobName: str
    HyperParameterTuningJobConfig: HyperParameterTuningJobConfigTypeDef
    TrainingJobDefinition: NotRequired[HyperParameterTrainingJobDefinitionTypeDef]
    TrainingJobDefinitions: NotRequired[Sequence[HyperParameterTrainingJobDefinitionUnionTypeDef]]
    WarmStartConfig: NotRequired[HyperParameterTuningJobWarmStartConfigTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]
    Autotune: NotRequired[AutotuneTypeDef]


class AlgorithmValidationProfileTypeDef(TypedDict):
    ProfileName: str
    TrainingJobDefinition: TrainingJobDefinitionUnionTypeDef
    TransformJobDefinition: NotRequired[TransformJobDefinitionUnionTypeDef]


class CreateModelPackageInputRequestTypeDef(TypedDict):
    ModelPackageName: NotRequired[str]
    ModelPackageGroupName: NotRequired[str]
    ModelPackageDescription: NotRequired[str]
    InferenceSpecification: NotRequired[InferenceSpecificationTypeDef]
    ValidationSpecification: NotRequired[ModelPackageValidationSpecificationTypeDef]
    SourceAlgorithmSpecification: NotRequired[SourceAlgorithmSpecificationTypeDef]
    CertifyForMarketplace: NotRequired[bool]
    Tags: NotRequired[Sequence[TagTypeDef]]
    ModelApprovalStatus: NotRequired[ModelApprovalStatusType]
    MetadataProperties: NotRequired[MetadataPropertiesTypeDef]
    ModelMetrics: NotRequired[ModelMetricsTypeDef]
    ClientToken: NotRequired[str]
    Domain: NotRequired[str]
    Task: NotRequired[str]
    SamplePayloadUrl: NotRequired[str]
    CustomerMetadataProperties: NotRequired[Mapping[str, str]]
    DriftCheckBaselines: NotRequired[DriftCheckBaselinesTypeDef]
    AdditionalInferenceSpecifications: NotRequired[
        Sequence[AdditionalInferenceSpecificationDefinitionUnionTypeDef]
    ]
    SkipModelValidation: NotRequired[SkipModelValidationType]
    SourceUri: NotRequired[str]
    SecurityConfig: NotRequired[ModelPackageSecurityConfigTypeDef]
    ModelCard: NotRequired[ModelPackageModelCardTypeDef]
    ModelLifeCycle: NotRequired[ModelLifeCycleTypeDef]


class SearchResponseTypeDef(TypedDict):
    Results: List[SearchRecordTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class MonitoringScheduleConfigTypeDef(TypedDict):
    ScheduleConfig: NotRequired[ScheduleConfigTypeDef]
    MonitoringJobDefinition: NotRequired[MonitoringJobDefinitionUnionTypeDef]
    MonitoringJobDefinitionName: NotRequired[str]
    MonitoringType: NotRequired[MonitoringTypeType]


AlgorithmValidationProfileUnionTypeDef = Union[
    AlgorithmValidationProfileTypeDef, AlgorithmValidationProfileOutputTypeDef
]


class CreateMonitoringScheduleRequestRequestTypeDef(TypedDict):
    MonitoringScheduleName: str
    MonitoringScheduleConfig: MonitoringScheduleConfigTypeDef
    Tags: NotRequired[Sequence[TagTypeDef]]


class UpdateMonitoringScheduleRequestRequestTypeDef(TypedDict):
    MonitoringScheduleName: str
    MonitoringScheduleConfig: MonitoringScheduleConfigTypeDef


class AlgorithmValidationSpecificationTypeDef(TypedDict):
    ValidationRole: str
    ValidationProfiles: Sequence[AlgorithmValidationProfileUnionTypeDef]


class CreateAlgorithmInputRequestTypeDef(TypedDict):
    AlgorithmName: str
    TrainingSpecification: TrainingSpecificationTypeDef
    AlgorithmDescription: NotRequired[str]
    InferenceSpecification: NotRequired[InferenceSpecificationTypeDef]
    ValidationSpecification: NotRequired[AlgorithmValidationSpecificationTypeDef]
    CertifyForMarketplace: NotRequired[bool]
    Tags: NotRequired[Sequence[TagTypeDef]]
