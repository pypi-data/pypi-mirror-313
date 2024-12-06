"""
Type annotations for sagemaker service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_sagemaker.client import SageMakerClient
    from mypy_boto3_sagemaker.paginator import (
        ListActionsPaginator,
        ListAlgorithmsPaginator,
        ListAliasesPaginator,
        ListAppImageConfigsPaginator,
        ListAppsPaginator,
        ListArtifactsPaginator,
        ListAssociationsPaginator,
        ListAutoMLJobsPaginator,
        ListCandidatesForAutoMLJobPaginator,
        ListClusterNodesPaginator,
        ListClustersPaginator,
        ListCodeRepositoriesPaginator,
        ListCompilationJobsPaginator,
        ListContextsPaginator,
        ListDataQualityJobDefinitionsPaginator,
        ListDeviceFleetsPaginator,
        ListDevicesPaginator,
        ListDomainsPaginator,
        ListEdgeDeploymentPlansPaginator,
        ListEdgePackagingJobsPaginator,
        ListEndpointConfigsPaginator,
        ListEndpointsPaginator,
        ListExperimentsPaginator,
        ListFeatureGroupsPaginator,
        ListFlowDefinitionsPaginator,
        ListHumanTaskUisPaginator,
        ListHyperParameterTuningJobsPaginator,
        ListImageVersionsPaginator,
        ListImagesPaginator,
        ListInferenceComponentsPaginator,
        ListInferenceExperimentsPaginator,
        ListInferenceRecommendationsJobStepsPaginator,
        ListInferenceRecommendationsJobsPaginator,
        ListLabelingJobsForWorkteamPaginator,
        ListLabelingJobsPaginator,
        ListLineageGroupsPaginator,
        ListMlflowTrackingServersPaginator,
        ListModelBiasJobDefinitionsPaginator,
        ListModelCardExportJobsPaginator,
        ListModelCardVersionsPaginator,
        ListModelCardsPaginator,
        ListModelExplainabilityJobDefinitionsPaginator,
        ListModelMetadataPaginator,
        ListModelPackageGroupsPaginator,
        ListModelPackagesPaginator,
        ListModelQualityJobDefinitionsPaginator,
        ListModelsPaginator,
        ListMonitoringAlertHistoryPaginator,
        ListMonitoringAlertsPaginator,
        ListMonitoringExecutionsPaginator,
        ListMonitoringSchedulesPaginator,
        ListNotebookInstanceLifecycleConfigsPaginator,
        ListNotebookInstancesPaginator,
        ListOptimizationJobsPaginator,
        ListPipelineExecutionStepsPaginator,
        ListPipelineExecutionsPaginator,
        ListPipelineParametersForExecutionPaginator,
        ListPipelinesPaginator,
        ListProcessingJobsPaginator,
        ListResourceCatalogsPaginator,
        ListSpacesPaginator,
        ListStageDevicesPaginator,
        ListStudioLifecycleConfigsPaginator,
        ListSubscribedWorkteamsPaginator,
        ListTagsPaginator,
        ListTrainingJobsForHyperParameterTuningJobPaginator,
        ListTrainingJobsPaginator,
        ListTransformJobsPaginator,
        ListTrialComponentsPaginator,
        ListTrialsPaginator,
        ListUserProfilesPaginator,
        ListWorkforcesPaginator,
        ListWorkteamsPaginator,
        SearchPaginator,
    )

    session = Session()
    client: SageMakerClient = session.client("sagemaker")

    list_actions_paginator: ListActionsPaginator = client.get_paginator("list_actions")
    list_algorithms_paginator: ListAlgorithmsPaginator = client.get_paginator("list_algorithms")
    list_aliases_paginator: ListAliasesPaginator = client.get_paginator("list_aliases")
    list_app_image_configs_paginator: ListAppImageConfigsPaginator = client.get_paginator("list_app_image_configs")
    list_apps_paginator: ListAppsPaginator = client.get_paginator("list_apps")
    list_artifacts_paginator: ListArtifactsPaginator = client.get_paginator("list_artifacts")
    list_associations_paginator: ListAssociationsPaginator = client.get_paginator("list_associations")
    list_auto_ml_jobs_paginator: ListAutoMLJobsPaginator = client.get_paginator("list_auto_ml_jobs")
    list_candidates_for_auto_ml_job_paginator: ListCandidatesForAutoMLJobPaginator = client.get_paginator("list_candidates_for_auto_ml_job")
    list_cluster_nodes_paginator: ListClusterNodesPaginator = client.get_paginator("list_cluster_nodes")
    list_clusters_paginator: ListClustersPaginator = client.get_paginator("list_clusters")
    list_code_repositories_paginator: ListCodeRepositoriesPaginator = client.get_paginator("list_code_repositories")
    list_compilation_jobs_paginator: ListCompilationJobsPaginator = client.get_paginator("list_compilation_jobs")
    list_contexts_paginator: ListContextsPaginator = client.get_paginator("list_contexts")
    list_data_quality_job_definitions_paginator: ListDataQualityJobDefinitionsPaginator = client.get_paginator("list_data_quality_job_definitions")
    list_device_fleets_paginator: ListDeviceFleetsPaginator = client.get_paginator("list_device_fleets")
    list_devices_paginator: ListDevicesPaginator = client.get_paginator("list_devices")
    list_domains_paginator: ListDomainsPaginator = client.get_paginator("list_domains")
    list_edge_deployment_plans_paginator: ListEdgeDeploymentPlansPaginator = client.get_paginator("list_edge_deployment_plans")
    list_edge_packaging_jobs_paginator: ListEdgePackagingJobsPaginator = client.get_paginator("list_edge_packaging_jobs")
    list_endpoint_configs_paginator: ListEndpointConfigsPaginator = client.get_paginator("list_endpoint_configs")
    list_endpoints_paginator: ListEndpointsPaginator = client.get_paginator("list_endpoints")
    list_experiments_paginator: ListExperimentsPaginator = client.get_paginator("list_experiments")
    list_feature_groups_paginator: ListFeatureGroupsPaginator = client.get_paginator("list_feature_groups")
    list_flow_definitions_paginator: ListFlowDefinitionsPaginator = client.get_paginator("list_flow_definitions")
    list_human_task_uis_paginator: ListHumanTaskUisPaginator = client.get_paginator("list_human_task_uis")
    list_hyper_parameter_tuning_jobs_paginator: ListHyperParameterTuningJobsPaginator = client.get_paginator("list_hyper_parameter_tuning_jobs")
    list_image_versions_paginator: ListImageVersionsPaginator = client.get_paginator("list_image_versions")
    list_images_paginator: ListImagesPaginator = client.get_paginator("list_images")
    list_inference_components_paginator: ListInferenceComponentsPaginator = client.get_paginator("list_inference_components")
    list_inference_experiments_paginator: ListInferenceExperimentsPaginator = client.get_paginator("list_inference_experiments")
    list_inference_recommendations_job_steps_paginator: ListInferenceRecommendationsJobStepsPaginator = client.get_paginator("list_inference_recommendations_job_steps")
    list_inference_recommendations_jobs_paginator: ListInferenceRecommendationsJobsPaginator = client.get_paginator("list_inference_recommendations_jobs")
    list_labeling_jobs_for_workteam_paginator: ListLabelingJobsForWorkteamPaginator = client.get_paginator("list_labeling_jobs_for_workteam")
    list_labeling_jobs_paginator: ListLabelingJobsPaginator = client.get_paginator("list_labeling_jobs")
    list_lineage_groups_paginator: ListLineageGroupsPaginator = client.get_paginator("list_lineage_groups")
    list_mlflow_tracking_servers_paginator: ListMlflowTrackingServersPaginator = client.get_paginator("list_mlflow_tracking_servers")
    list_model_bias_job_definitions_paginator: ListModelBiasJobDefinitionsPaginator = client.get_paginator("list_model_bias_job_definitions")
    list_model_card_export_jobs_paginator: ListModelCardExportJobsPaginator = client.get_paginator("list_model_card_export_jobs")
    list_model_card_versions_paginator: ListModelCardVersionsPaginator = client.get_paginator("list_model_card_versions")
    list_model_cards_paginator: ListModelCardsPaginator = client.get_paginator("list_model_cards")
    list_model_explainability_job_definitions_paginator: ListModelExplainabilityJobDefinitionsPaginator = client.get_paginator("list_model_explainability_job_definitions")
    list_model_metadata_paginator: ListModelMetadataPaginator = client.get_paginator("list_model_metadata")
    list_model_package_groups_paginator: ListModelPackageGroupsPaginator = client.get_paginator("list_model_package_groups")
    list_model_packages_paginator: ListModelPackagesPaginator = client.get_paginator("list_model_packages")
    list_model_quality_job_definitions_paginator: ListModelQualityJobDefinitionsPaginator = client.get_paginator("list_model_quality_job_definitions")
    list_models_paginator: ListModelsPaginator = client.get_paginator("list_models")
    list_monitoring_alert_history_paginator: ListMonitoringAlertHistoryPaginator = client.get_paginator("list_monitoring_alert_history")
    list_monitoring_alerts_paginator: ListMonitoringAlertsPaginator = client.get_paginator("list_monitoring_alerts")
    list_monitoring_executions_paginator: ListMonitoringExecutionsPaginator = client.get_paginator("list_monitoring_executions")
    list_monitoring_schedules_paginator: ListMonitoringSchedulesPaginator = client.get_paginator("list_monitoring_schedules")
    list_notebook_instance_lifecycle_configs_paginator: ListNotebookInstanceLifecycleConfigsPaginator = client.get_paginator("list_notebook_instance_lifecycle_configs")
    list_notebook_instances_paginator: ListNotebookInstancesPaginator = client.get_paginator("list_notebook_instances")
    list_optimization_jobs_paginator: ListOptimizationJobsPaginator = client.get_paginator("list_optimization_jobs")
    list_pipeline_execution_steps_paginator: ListPipelineExecutionStepsPaginator = client.get_paginator("list_pipeline_execution_steps")
    list_pipeline_executions_paginator: ListPipelineExecutionsPaginator = client.get_paginator("list_pipeline_executions")
    list_pipeline_parameters_for_execution_paginator: ListPipelineParametersForExecutionPaginator = client.get_paginator("list_pipeline_parameters_for_execution")
    list_pipelines_paginator: ListPipelinesPaginator = client.get_paginator("list_pipelines")
    list_processing_jobs_paginator: ListProcessingJobsPaginator = client.get_paginator("list_processing_jobs")
    list_resource_catalogs_paginator: ListResourceCatalogsPaginator = client.get_paginator("list_resource_catalogs")
    list_spaces_paginator: ListSpacesPaginator = client.get_paginator("list_spaces")
    list_stage_devices_paginator: ListStageDevicesPaginator = client.get_paginator("list_stage_devices")
    list_studio_lifecycle_configs_paginator: ListStudioLifecycleConfigsPaginator = client.get_paginator("list_studio_lifecycle_configs")
    list_subscribed_workteams_paginator: ListSubscribedWorkteamsPaginator = client.get_paginator("list_subscribed_workteams")
    list_tags_paginator: ListTagsPaginator = client.get_paginator("list_tags")
    list_training_jobs_for_hyper_parameter_tuning_job_paginator: ListTrainingJobsForHyperParameterTuningJobPaginator = client.get_paginator("list_training_jobs_for_hyper_parameter_tuning_job")
    list_training_jobs_paginator: ListTrainingJobsPaginator = client.get_paginator("list_training_jobs")
    list_transform_jobs_paginator: ListTransformJobsPaginator = client.get_paginator("list_transform_jobs")
    list_trial_components_paginator: ListTrialComponentsPaginator = client.get_paginator("list_trial_components")
    list_trials_paginator: ListTrialsPaginator = client.get_paginator("list_trials")
    list_user_profiles_paginator: ListUserProfilesPaginator = client.get_paginator("list_user_profiles")
    list_workforces_paginator: ListWorkforcesPaginator = client.get_paginator("list_workforces")
    list_workteams_paginator: ListWorkteamsPaginator = client.get_paginator("list_workteams")
    search_paginator: SearchPaginator = client.get_paginator("search")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListActionsRequestListActionsPaginateTypeDef,
    ListActionsResponseTypeDef,
    ListAlgorithmsInputListAlgorithmsPaginateTypeDef,
    ListAlgorithmsOutputTypeDef,
    ListAliasesRequestListAliasesPaginateTypeDef,
    ListAliasesResponseTypeDef,
    ListAppImageConfigsRequestListAppImageConfigsPaginateTypeDef,
    ListAppImageConfigsResponseTypeDef,
    ListAppsRequestListAppsPaginateTypeDef,
    ListAppsResponseTypeDef,
    ListArtifactsRequestListArtifactsPaginateTypeDef,
    ListArtifactsResponseTypeDef,
    ListAssociationsRequestListAssociationsPaginateTypeDef,
    ListAssociationsResponseTypeDef,
    ListAutoMLJobsRequestListAutoMLJobsPaginateTypeDef,
    ListAutoMLJobsResponseTypeDef,
    ListCandidatesForAutoMLJobRequestListCandidatesForAutoMLJobPaginateTypeDef,
    ListCandidatesForAutoMLJobResponseTypeDef,
    ListClusterNodesRequestListClusterNodesPaginateTypeDef,
    ListClusterNodesResponseTypeDef,
    ListClustersRequestListClustersPaginateTypeDef,
    ListClustersResponseTypeDef,
    ListCodeRepositoriesInputListCodeRepositoriesPaginateTypeDef,
    ListCodeRepositoriesOutputTypeDef,
    ListCompilationJobsRequestListCompilationJobsPaginateTypeDef,
    ListCompilationJobsResponseTypeDef,
    ListContextsRequestListContextsPaginateTypeDef,
    ListContextsResponseTypeDef,
    ListDataQualityJobDefinitionsRequestListDataQualityJobDefinitionsPaginateTypeDef,
    ListDataQualityJobDefinitionsResponseTypeDef,
    ListDeviceFleetsRequestListDeviceFleetsPaginateTypeDef,
    ListDeviceFleetsResponseTypeDef,
    ListDevicesRequestListDevicesPaginateTypeDef,
    ListDevicesResponseTypeDef,
    ListDomainsRequestListDomainsPaginateTypeDef,
    ListDomainsResponseTypeDef,
    ListEdgeDeploymentPlansRequestListEdgeDeploymentPlansPaginateTypeDef,
    ListEdgeDeploymentPlansResponseTypeDef,
    ListEdgePackagingJobsRequestListEdgePackagingJobsPaginateTypeDef,
    ListEdgePackagingJobsResponseTypeDef,
    ListEndpointConfigsInputListEndpointConfigsPaginateTypeDef,
    ListEndpointConfigsOutputTypeDef,
    ListEndpointsInputListEndpointsPaginateTypeDef,
    ListEndpointsOutputTypeDef,
    ListExperimentsRequestListExperimentsPaginateTypeDef,
    ListExperimentsResponseTypeDef,
    ListFeatureGroupsRequestListFeatureGroupsPaginateTypeDef,
    ListFeatureGroupsResponseTypeDef,
    ListFlowDefinitionsRequestListFlowDefinitionsPaginateTypeDef,
    ListFlowDefinitionsResponseTypeDef,
    ListHumanTaskUisRequestListHumanTaskUisPaginateTypeDef,
    ListHumanTaskUisResponseTypeDef,
    ListHyperParameterTuningJobsRequestListHyperParameterTuningJobsPaginateTypeDef,
    ListHyperParameterTuningJobsResponseTypeDef,
    ListImagesRequestListImagesPaginateTypeDef,
    ListImagesResponseTypeDef,
    ListImageVersionsRequestListImageVersionsPaginateTypeDef,
    ListImageVersionsResponseTypeDef,
    ListInferenceComponentsInputListInferenceComponentsPaginateTypeDef,
    ListInferenceComponentsOutputTypeDef,
    ListInferenceExperimentsRequestListInferenceExperimentsPaginateTypeDef,
    ListInferenceExperimentsResponseTypeDef,
    ListInferenceRecommendationsJobsRequestListInferenceRecommendationsJobsPaginateTypeDef,
    ListInferenceRecommendationsJobsResponseTypeDef,
    ListInferenceRecommendationsJobStepsRequestListInferenceRecommendationsJobStepsPaginateTypeDef,
    ListInferenceRecommendationsJobStepsResponseTypeDef,
    ListLabelingJobsForWorkteamRequestListLabelingJobsForWorkteamPaginateTypeDef,
    ListLabelingJobsForWorkteamResponseTypeDef,
    ListLabelingJobsRequestListLabelingJobsPaginateTypeDef,
    ListLabelingJobsResponseTypeDef,
    ListLineageGroupsRequestListLineageGroupsPaginateTypeDef,
    ListLineageGroupsResponseTypeDef,
    ListMlflowTrackingServersRequestListMlflowTrackingServersPaginateTypeDef,
    ListMlflowTrackingServersResponseTypeDef,
    ListModelBiasJobDefinitionsRequestListModelBiasJobDefinitionsPaginateTypeDef,
    ListModelBiasJobDefinitionsResponseTypeDef,
    ListModelCardExportJobsRequestListModelCardExportJobsPaginateTypeDef,
    ListModelCardExportJobsResponseTypeDef,
    ListModelCardsRequestListModelCardsPaginateTypeDef,
    ListModelCardsResponseTypeDef,
    ListModelCardVersionsRequestListModelCardVersionsPaginateTypeDef,
    ListModelCardVersionsResponseTypeDef,
    ListModelExplainabilityJobDefinitionsRequestListModelExplainabilityJobDefinitionsPaginateTypeDef,
    ListModelExplainabilityJobDefinitionsResponseTypeDef,
    ListModelMetadataRequestListModelMetadataPaginateTypeDef,
    ListModelMetadataResponseTypeDef,
    ListModelPackageGroupsInputListModelPackageGroupsPaginateTypeDef,
    ListModelPackageGroupsOutputTypeDef,
    ListModelPackagesInputListModelPackagesPaginateTypeDef,
    ListModelPackagesOutputTypeDef,
    ListModelQualityJobDefinitionsRequestListModelQualityJobDefinitionsPaginateTypeDef,
    ListModelQualityJobDefinitionsResponseTypeDef,
    ListModelsInputListModelsPaginateTypeDef,
    ListModelsOutputTypeDef,
    ListMonitoringAlertHistoryRequestListMonitoringAlertHistoryPaginateTypeDef,
    ListMonitoringAlertHistoryResponseTypeDef,
    ListMonitoringAlertsRequestListMonitoringAlertsPaginateTypeDef,
    ListMonitoringAlertsResponseTypeDef,
    ListMonitoringExecutionsRequestListMonitoringExecutionsPaginateTypeDef,
    ListMonitoringExecutionsResponseTypeDef,
    ListMonitoringSchedulesRequestListMonitoringSchedulesPaginateTypeDef,
    ListMonitoringSchedulesResponseTypeDef,
    ListNotebookInstanceLifecycleConfigsInputListNotebookInstanceLifecycleConfigsPaginateTypeDef,
    ListNotebookInstanceLifecycleConfigsOutputTypeDef,
    ListNotebookInstancesInputListNotebookInstancesPaginateTypeDef,
    ListNotebookInstancesOutputTypeDef,
    ListOptimizationJobsRequestListOptimizationJobsPaginateTypeDef,
    ListOptimizationJobsResponseTypeDef,
    ListPipelineExecutionsRequestListPipelineExecutionsPaginateTypeDef,
    ListPipelineExecutionsResponseTypeDef,
    ListPipelineExecutionStepsRequestListPipelineExecutionStepsPaginateTypeDef,
    ListPipelineExecutionStepsResponseTypeDef,
    ListPipelineParametersForExecutionRequestListPipelineParametersForExecutionPaginateTypeDef,
    ListPipelineParametersForExecutionResponseTypeDef,
    ListPipelinesRequestListPipelinesPaginateTypeDef,
    ListPipelinesResponseTypeDef,
    ListProcessingJobsRequestListProcessingJobsPaginateTypeDef,
    ListProcessingJobsResponseTypeDef,
    ListResourceCatalogsRequestListResourceCatalogsPaginateTypeDef,
    ListResourceCatalogsResponseTypeDef,
    ListSpacesRequestListSpacesPaginateTypeDef,
    ListSpacesResponseTypeDef,
    ListStageDevicesRequestListStageDevicesPaginateTypeDef,
    ListStageDevicesResponseTypeDef,
    ListStudioLifecycleConfigsRequestListStudioLifecycleConfigsPaginateTypeDef,
    ListStudioLifecycleConfigsResponseTypeDef,
    ListSubscribedWorkteamsRequestListSubscribedWorkteamsPaginateTypeDef,
    ListSubscribedWorkteamsResponseTypeDef,
    ListTagsInputListTagsPaginateTypeDef,
    ListTagsOutputTypeDef,
    ListTrainingJobsForHyperParameterTuningJobRequestListTrainingJobsForHyperParameterTuningJobPaginateTypeDef,
    ListTrainingJobsForHyperParameterTuningJobResponseTypeDef,
    ListTrainingJobsRequestListTrainingJobsPaginateTypeDef,
    ListTrainingJobsResponseTypeDef,
    ListTransformJobsRequestListTransformJobsPaginateTypeDef,
    ListTransformJobsResponseTypeDef,
    ListTrialComponentsRequestListTrialComponentsPaginateTypeDef,
    ListTrialComponentsResponseTypeDef,
    ListTrialsRequestListTrialsPaginateTypeDef,
    ListTrialsResponseTypeDef,
    ListUserProfilesRequestListUserProfilesPaginateTypeDef,
    ListUserProfilesResponseTypeDef,
    ListWorkforcesRequestListWorkforcesPaginateTypeDef,
    ListWorkforcesResponseTypeDef,
    ListWorkteamsRequestListWorkteamsPaginateTypeDef,
    ListWorkteamsResponseTypeDef,
    SearchRequestSearchPaginateTypeDef,
    SearchResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListActionsPaginator",
    "ListAlgorithmsPaginator",
    "ListAliasesPaginator",
    "ListAppImageConfigsPaginator",
    "ListAppsPaginator",
    "ListArtifactsPaginator",
    "ListAssociationsPaginator",
    "ListAutoMLJobsPaginator",
    "ListCandidatesForAutoMLJobPaginator",
    "ListClusterNodesPaginator",
    "ListClustersPaginator",
    "ListCodeRepositoriesPaginator",
    "ListCompilationJobsPaginator",
    "ListContextsPaginator",
    "ListDataQualityJobDefinitionsPaginator",
    "ListDeviceFleetsPaginator",
    "ListDevicesPaginator",
    "ListDomainsPaginator",
    "ListEdgeDeploymentPlansPaginator",
    "ListEdgePackagingJobsPaginator",
    "ListEndpointConfigsPaginator",
    "ListEndpointsPaginator",
    "ListExperimentsPaginator",
    "ListFeatureGroupsPaginator",
    "ListFlowDefinitionsPaginator",
    "ListHumanTaskUisPaginator",
    "ListHyperParameterTuningJobsPaginator",
    "ListImageVersionsPaginator",
    "ListImagesPaginator",
    "ListInferenceComponentsPaginator",
    "ListInferenceExperimentsPaginator",
    "ListInferenceRecommendationsJobStepsPaginator",
    "ListInferenceRecommendationsJobsPaginator",
    "ListLabelingJobsForWorkteamPaginator",
    "ListLabelingJobsPaginator",
    "ListLineageGroupsPaginator",
    "ListMlflowTrackingServersPaginator",
    "ListModelBiasJobDefinitionsPaginator",
    "ListModelCardExportJobsPaginator",
    "ListModelCardVersionsPaginator",
    "ListModelCardsPaginator",
    "ListModelExplainabilityJobDefinitionsPaginator",
    "ListModelMetadataPaginator",
    "ListModelPackageGroupsPaginator",
    "ListModelPackagesPaginator",
    "ListModelQualityJobDefinitionsPaginator",
    "ListModelsPaginator",
    "ListMonitoringAlertHistoryPaginator",
    "ListMonitoringAlertsPaginator",
    "ListMonitoringExecutionsPaginator",
    "ListMonitoringSchedulesPaginator",
    "ListNotebookInstanceLifecycleConfigsPaginator",
    "ListNotebookInstancesPaginator",
    "ListOptimizationJobsPaginator",
    "ListPipelineExecutionStepsPaginator",
    "ListPipelineExecutionsPaginator",
    "ListPipelineParametersForExecutionPaginator",
    "ListPipelinesPaginator",
    "ListProcessingJobsPaginator",
    "ListResourceCatalogsPaginator",
    "ListSpacesPaginator",
    "ListStageDevicesPaginator",
    "ListStudioLifecycleConfigsPaginator",
    "ListSubscribedWorkteamsPaginator",
    "ListTagsPaginator",
    "ListTrainingJobsForHyperParameterTuningJobPaginator",
    "ListTrainingJobsPaginator",
    "ListTransformJobsPaginator",
    "ListTrialComponentsPaginator",
    "ListTrialsPaginator",
    "ListUserProfilesPaginator",
    "ListWorkforcesPaginator",
    "ListWorkteamsPaginator",
    "SearchPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListActionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListActions.html#SageMaker.Paginator.ListActions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listactionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListActionsRequestListActionsPaginateTypeDef]
    ) -> _PageIterator[ListActionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListActions.html#SageMaker.Paginator.ListActions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listactionspaginator)
        """


class ListAlgorithmsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListAlgorithms.html#SageMaker.Paginator.ListAlgorithms)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listalgorithmspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListAlgorithmsInputListAlgorithmsPaginateTypeDef]
    ) -> _PageIterator[ListAlgorithmsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListAlgorithms.html#SageMaker.Paginator.ListAlgorithms.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listalgorithmspaginator)
        """


class ListAliasesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListAliases.html#SageMaker.Paginator.ListAliases)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listaliasespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListAliasesRequestListAliasesPaginateTypeDef]
    ) -> _PageIterator[ListAliasesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListAliases.html#SageMaker.Paginator.ListAliases.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listaliasespaginator)
        """


class ListAppImageConfigsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListAppImageConfigs.html#SageMaker.Paginator.ListAppImageConfigs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listappimageconfigspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListAppImageConfigsRequestListAppImageConfigsPaginateTypeDef]
    ) -> _PageIterator[ListAppImageConfigsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListAppImageConfigs.html#SageMaker.Paginator.ListAppImageConfigs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listappimageconfigspaginator)
        """


class ListAppsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListApps.html#SageMaker.Paginator.ListApps)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listappspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListAppsRequestListAppsPaginateTypeDef]
    ) -> _PageIterator[ListAppsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListApps.html#SageMaker.Paginator.ListApps.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listappspaginator)
        """


class ListArtifactsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListArtifacts.html#SageMaker.Paginator.ListArtifacts)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listartifactspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListArtifactsRequestListArtifactsPaginateTypeDef]
    ) -> _PageIterator[ListArtifactsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListArtifacts.html#SageMaker.Paginator.ListArtifacts.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listartifactspaginator)
        """


class ListAssociationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListAssociations.html#SageMaker.Paginator.ListAssociations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listassociationspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListAssociationsRequestListAssociationsPaginateTypeDef]
    ) -> _PageIterator[ListAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListAssociations.html#SageMaker.Paginator.ListAssociations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listassociationspaginator)
        """


class ListAutoMLJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListAutoMLJobs.html#SageMaker.Paginator.ListAutoMLJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listautomljobspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListAutoMLJobsRequestListAutoMLJobsPaginateTypeDef]
    ) -> _PageIterator[ListAutoMLJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListAutoMLJobs.html#SageMaker.Paginator.ListAutoMLJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listautomljobspaginator)
        """


class ListCandidatesForAutoMLJobPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListCandidatesForAutoMLJob.html#SageMaker.Paginator.ListCandidatesForAutoMLJob)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listcandidatesforautomljobpaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListCandidatesForAutoMLJobRequestListCandidatesForAutoMLJobPaginateTypeDef
        ],
    ) -> _PageIterator[ListCandidatesForAutoMLJobResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListCandidatesForAutoMLJob.html#SageMaker.Paginator.ListCandidatesForAutoMLJob.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listcandidatesforautomljobpaginator)
        """


class ListClusterNodesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListClusterNodes.html#SageMaker.Paginator.ListClusterNodes)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listclusternodespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListClusterNodesRequestListClusterNodesPaginateTypeDef]
    ) -> _PageIterator[ListClusterNodesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListClusterNodes.html#SageMaker.Paginator.ListClusterNodes.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listclusternodespaginator)
        """


class ListClustersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListClusters.html#SageMaker.Paginator.ListClusters)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listclusterspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListClustersRequestListClustersPaginateTypeDef]
    ) -> _PageIterator[ListClustersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListClusters.html#SageMaker.Paginator.ListClusters.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listclusterspaginator)
        """


class ListCodeRepositoriesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListCodeRepositories.html#SageMaker.Paginator.ListCodeRepositories)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listcoderepositoriespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListCodeRepositoriesInputListCodeRepositoriesPaginateTypeDef]
    ) -> _PageIterator[ListCodeRepositoriesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListCodeRepositories.html#SageMaker.Paginator.ListCodeRepositories.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listcoderepositoriespaginator)
        """


class ListCompilationJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListCompilationJobs.html#SageMaker.Paginator.ListCompilationJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listcompilationjobspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListCompilationJobsRequestListCompilationJobsPaginateTypeDef]
    ) -> _PageIterator[ListCompilationJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListCompilationJobs.html#SageMaker.Paginator.ListCompilationJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listcompilationjobspaginator)
        """


class ListContextsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListContexts.html#SageMaker.Paginator.ListContexts)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listcontextspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListContextsRequestListContextsPaginateTypeDef]
    ) -> _PageIterator[ListContextsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListContexts.html#SageMaker.Paginator.ListContexts.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listcontextspaginator)
        """


class ListDataQualityJobDefinitionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListDataQualityJobDefinitions.html#SageMaker.Paginator.ListDataQualityJobDefinitions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listdataqualityjobdefinitionspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListDataQualityJobDefinitionsRequestListDataQualityJobDefinitionsPaginateTypeDef
        ],
    ) -> _PageIterator[ListDataQualityJobDefinitionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListDataQualityJobDefinitions.html#SageMaker.Paginator.ListDataQualityJobDefinitions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listdataqualityjobdefinitionspaginator)
        """


class ListDeviceFleetsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListDeviceFleets.html#SageMaker.Paginator.ListDeviceFleets)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listdevicefleetspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListDeviceFleetsRequestListDeviceFleetsPaginateTypeDef]
    ) -> _PageIterator[ListDeviceFleetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListDeviceFleets.html#SageMaker.Paginator.ListDeviceFleets.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listdevicefleetspaginator)
        """


class ListDevicesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListDevices.html#SageMaker.Paginator.ListDevices)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listdevicespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListDevicesRequestListDevicesPaginateTypeDef]
    ) -> _PageIterator[ListDevicesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListDevices.html#SageMaker.Paginator.ListDevices.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listdevicespaginator)
        """


class ListDomainsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListDomains.html#SageMaker.Paginator.ListDomains)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listdomainspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListDomainsRequestListDomainsPaginateTypeDef]
    ) -> _PageIterator[ListDomainsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListDomains.html#SageMaker.Paginator.ListDomains.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listdomainspaginator)
        """


class ListEdgeDeploymentPlansPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListEdgeDeploymentPlans.html#SageMaker.Paginator.ListEdgeDeploymentPlans)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listedgedeploymentplanspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListEdgeDeploymentPlansRequestListEdgeDeploymentPlansPaginateTypeDef]
    ) -> _PageIterator[ListEdgeDeploymentPlansResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListEdgeDeploymentPlans.html#SageMaker.Paginator.ListEdgeDeploymentPlans.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listedgedeploymentplanspaginator)
        """


class ListEdgePackagingJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListEdgePackagingJobs.html#SageMaker.Paginator.ListEdgePackagingJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listedgepackagingjobspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListEdgePackagingJobsRequestListEdgePackagingJobsPaginateTypeDef]
    ) -> _PageIterator[ListEdgePackagingJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListEdgePackagingJobs.html#SageMaker.Paginator.ListEdgePackagingJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listedgepackagingjobspaginator)
        """


class ListEndpointConfigsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListEndpointConfigs.html#SageMaker.Paginator.ListEndpointConfigs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listendpointconfigspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListEndpointConfigsInputListEndpointConfigsPaginateTypeDef]
    ) -> _PageIterator[ListEndpointConfigsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListEndpointConfigs.html#SageMaker.Paginator.ListEndpointConfigs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listendpointconfigspaginator)
        """


class ListEndpointsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListEndpoints.html#SageMaker.Paginator.ListEndpoints)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listendpointspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListEndpointsInputListEndpointsPaginateTypeDef]
    ) -> _PageIterator[ListEndpointsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListEndpoints.html#SageMaker.Paginator.ListEndpoints.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listendpointspaginator)
        """


class ListExperimentsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListExperiments.html#SageMaker.Paginator.ListExperiments)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listexperimentspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListExperimentsRequestListExperimentsPaginateTypeDef]
    ) -> _PageIterator[ListExperimentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListExperiments.html#SageMaker.Paginator.ListExperiments.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listexperimentspaginator)
        """


class ListFeatureGroupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListFeatureGroups.html#SageMaker.Paginator.ListFeatureGroups)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listfeaturegroupspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListFeatureGroupsRequestListFeatureGroupsPaginateTypeDef]
    ) -> _PageIterator[ListFeatureGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListFeatureGroups.html#SageMaker.Paginator.ListFeatureGroups.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listfeaturegroupspaginator)
        """


class ListFlowDefinitionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListFlowDefinitions.html#SageMaker.Paginator.ListFlowDefinitions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listflowdefinitionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListFlowDefinitionsRequestListFlowDefinitionsPaginateTypeDef]
    ) -> _PageIterator[ListFlowDefinitionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListFlowDefinitions.html#SageMaker.Paginator.ListFlowDefinitions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listflowdefinitionspaginator)
        """


class ListHumanTaskUisPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListHumanTaskUis.html#SageMaker.Paginator.ListHumanTaskUis)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listhumantaskuispaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListHumanTaskUisRequestListHumanTaskUisPaginateTypeDef]
    ) -> _PageIterator[ListHumanTaskUisResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListHumanTaskUis.html#SageMaker.Paginator.ListHumanTaskUis.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listhumantaskuispaginator)
        """


class ListHyperParameterTuningJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListHyperParameterTuningJobs.html#SageMaker.Paginator.ListHyperParameterTuningJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listhyperparametertuningjobspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListHyperParameterTuningJobsRequestListHyperParameterTuningJobsPaginateTypeDef
        ],
    ) -> _PageIterator[ListHyperParameterTuningJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListHyperParameterTuningJobs.html#SageMaker.Paginator.ListHyperParameterTuningJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listhyperparametertuningjobspaginator)
        """


class ListImageVersionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListImageVersions.html#SageMaker.Paginator.ListImageVersions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listimageversionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListImageVersionsRequestListImageVersionsPaginateTypeDef]
    ) -> _PageIterator[ListImageVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListImageVersions.html#SageMaker.Paginator.ListImageVersions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listimageversionspaginator)
        """


class ListImagesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListImages.html#SageMaker.Paginator.ListImages)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listimagespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListImagesRequestListImagesPaginateTypeDef]
    ) -> _PageIterator[ListImagesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListImages.html#SageMaker.Paginator.ListImages.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listimagespaginator)
        """


class ListInferenceComponentsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListInferenceComponents.html#SageMaker.Paginator.ListInferenceComponents)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listinferencecomponentspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListInferenceComponentsInputListInferenceComponentsPaginateTypeDef]
    ) -> _PageIterator[ListInferenceComponentsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListInferenceComponents.html#SageMaker.Paginator.ListInferenceComponents.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listinferencecomponentspaginator)
        """


class ListInferenceExperimentsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListInferenceExperiments.html#SageMaker.Paginator.ListInferenceExperiments)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listinferenceexperimentspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[ListInferenceExperimentsRequestListInferenceExperimentsPaginateTypeDef],
    ) -> _PageIterator[ListInferenceExperimentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListInferenceExperiments.html#SageMaker.Paginator.ListInferenceExperiments.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listinferenceexperimentspaginator)
        """


class ListInferenceRecommendationsJobStepsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListInferenceRecommendationsJobSteps.html#SageMaker.Paginator.ListInferenceRecommendationsJobSteps)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listinferencerecommendationsjobstepspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListInferenceRecommendationsJobStepsRequestListInferenceRecommendationsJobStepsPaginateTypeDef
        ],
    ) -> _PageIterator[ListInferenceRecommendationsJobStepsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListInferenceRecommendationsJobSteps.html#SageMaker.Paginator.ListInferenceRecommendationsJobSteps.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listinferencerecommendationsjobstepspaginator)
        """


class ListInferenceRecommendationsJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListInferenceRecommendationsJobs.html#SageMaker.Paginator.ListInferenceRecommendationsJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listinferencerecommendationsjobspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListInferenceRecommendationsJobsRequestListInferenceRecommendationsJobsPaginateTypeDef
        ],
    ) -> _PageIterator[ListInferenceRecommendationsJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListInferenceRecommendationsJobs.html#SageMaker.Paginator.ListInferenceRecommendationsJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listinferencerecommendationsjobspaginator)
        """


class ListLabelingJobsForWorkteamPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListLabelingJobsForWorkteam.html#SageMaker.Paginator.ListLabelingJobsForWorkteam)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listlabelingjobsforworkteampaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListLabelingJobsForWorkteamRequestListLabelingJobsForWorkteamPaginateTypeDef
        ],
    ) -> _PageIterator[ListLabelingJobsForWorkteamResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListLabelingJobsForWorkteam.html#SageMaker.Paginator.ListLabelingJobsForWorkteam.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listlabelingjobsforworkteampaginator)
        """


class ListLabelingJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListLabelingJobs.html#SageMaker.Paginator.ListLabelingJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listlabelingjobspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListLabelingJobsRequestListLabelingJobsPaginateTypeDef]
    ) -> _PageIterator[ListLabelingJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListLabelingJobs.html#SageMaker.Paginator.ListLabelingJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listlabelingjobspaginator)
        """


class ListLineageGroupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListLineageGroups.html#SageMaker.Paginator.ListLineageGroups)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listlineagegroupspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListLineageGroupsRequestListLineageGroupsPaginateTypeDef]
    ) -> _PageIterator[ListLineageGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListLineageGroups.html#SageMaker.Paginator.ListLineageGroups.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listlineagegroupspaginator)
        """


class ListMlflowTrackingServersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListMlflowTrackingServers.html#SageMaker.Paginator.ListMlflowTrackingServers)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listmlflowtrackingserverspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[ListMlflowTrackingServersRequestListMlflowTrackingServersPaginateTypeDef],
    ) -> _PageIterator[ListMlflowTrackingServersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListMlflowTrackingServers.html#SageMaker.Paginator.ListMlflowTrackingServers.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listmlflowtrackingserverspaginator)
        """


class ListModelBiasJobDefinitionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModelBiasJobDefinitions.html#SageMaker.Paginator.ListModelBiasJobDefinitions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listmodelbiasjobdefinitionspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListModelBiasJobDefinitionsRequestListModelBiasJobDefinitionsPaginateTypeDef
        ],
    ) -> _PageIterator[ListModelBiasJobDefinitionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModelBiasJobDefinitions.html#SageMaker.Paginator.ListModelBiasJobDefinitions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listmodelbiasjobdefinitionspaginator)
        """


class ListModelCardExportJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModelCardExportJobs.html#SageMaker.Paginator.ListModelCardExportJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listmodelcardexportjobspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListModelCardExportJobsRequestListModelCardExportJobsPaginateTypeDef]
    ) -> _PageIterator[ListModelCardExportJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModelCardExportJobs.html#SageMaker.Paginator.ListModelCardExportJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listmodelcardexportjobspaginator)
        """


class ListModelCardVersionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModelCardVersions.html#SageMaker.Paginator.ListModelCardVersions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listmodelcardversionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListModelCardVersionsRequestListModelCardVersionsPaginateTypeDef]
    ) -> _PageIterator[ListModelCardVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModelCardVersions.html#SageMaker.Paginator.ListModelCardVersions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listmodelcardversionspaginator)
        """


class ListModelCardsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModelCards.html#SageMaker.Paginator.ListModelCards)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listmodelcardspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListModelCardsRequestListModelCardsPaginateTypeDef]
    ) -> _PageIterator[ListModelCardsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModelCards.html#SageMaker.Paginator.ListModelCards.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listmodelcardspaginator)
        """


class ListModelExplainabilityJobDefinitionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModelExplainabilityJobDefinitions.html#SageMaker.Paginator.ListModelExplainabilityJobDefinitions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listmodelexplainabilityjobdefinitionspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListModelExplainabilityJobDefinitionsRequestListModelExplainabilityJobDefinitionsPaginateTypeDef
        ],
    ) -> _PageIterator[ListModelExplainabilityJobDefinitionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModelExplainabilityJobDefinitions.html#SageMaker.Paginator.ListModelExplainabilityJobDefinitions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listmodelexplainabilityjobdefinitionspaginator)
        """


class ListModelMetadataPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModelMetadata.html#SageMaker.Paginator.ListModelMetadata)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listmodelmetadatapaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListModelMetadataRequestListModelMetadataPaginateTypeDef]
    ) -> _PageIterator[ListModelMetadataResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModelMetadata.html#SageMaker.Paginator.ListModelMetadata.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listmodelmetadatapaginator)
        """


class ListModelPackageGroupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModelPackageGroups.html#SageMaker.Paginator.ListModelPackageGroups)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listmodelpackagegroupspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListModelPackageGroupsInputListModelPackageGroupsPaginateTypeDef]
    ) -> _PageIterator[ListModelPackageGroupsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModelPackageGroups.html#SageMaker.Paginator.ListModelPackageGroups.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listmodelpackagegroupspaginator)
        """


class ListModelPackagesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModelPackages.html#SageMaker.Paginator.ListModelPackages)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listmodelpackagespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListModelPackagesInputListModelPackagesPaginateTypeDef]
    ) -> _PageIterator[ListModelPackagesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModelPackages.html#SageMaker.Paginator.ListModelPackages.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listmodelpackagespaginator)
        """


class ListModelQualityJobDefinitionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModelQualityJobDefinitions.html#SageMaker.Paginator.ListModelQualityJobDefinitions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listmodelqualityjobdefinitionspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListModelQualityJobDefinitionsRequestListModelQualityJobDefinitionsPaginateTypeDef
        ],
    ) -> _PageIterator[ListModelQualityJobDefinitionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModelQualityJobDefinitions.html#SageMaker.Paginator.ListModelQualityJobDefinitions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listmodelqualityjobdefinitionspaginator)
        """


class ListModelsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModels.html#SageMaker.Paginator.ListModels)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listmodelspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListModelsInputListModelsPaginateTypeDef]
    ) -> _PageIterator[ListModelsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModels.html#SageMaker.Paginator.ListModels.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listmodelspaginator)
        """


class ListMonitoringAlertHistoryPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListMonitoringAlertHistory.html#SageMaker.Paginator.ListMonitoringAlertHistory)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listmonitoringalerthistorypaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListMonitoringAlertHistoryRequestListMonitoringAlertHistoryPaginateTypeDef
        ],
    ) -> _PageIterator[ListMonitoringAlertHistoryResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListMonitoringAlertHistory.html#SageMaker.Paginator.ListMonitoringAlertHistory.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listmonitoringalerthistorypaginator)
        """


class ListMonitoringAlertsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListMonitoringAlerts.html#SageMaker.Paginator.ListMonitoringAlerts)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listmonitoringalertspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListMonitoringAlertsRequestListMonitoringAlertsPaginateTypeDef]
    ) -> _PageIterator[ListMonitoringAlertsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListMonitoringAlerts.html#SageMaker.Paginator.ListMonitoringAlerts.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listmonitoringalertspaginator)
        """


class ListMonitoringExecutionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListMonitoringExecutions.html#SageMaker.Paginator.ListMonitoringExecutions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listmonitoringexecutionspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[ListMonitoringExecutionsRequestListMonitoringExecutionsPaginateTypeDef],
    ) -> _PageIterator[ListMonitoringExecutionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListMonitoringExecutions.html#SageMaker.Paginator.ListMonitoringExecutions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listmonitoringexecutionspaginator)
        """


class ListMonitoringSchedulesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListMonitoringSchedules.html#SageMaker.Paginator.ListMonitoringSchedules)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listmonitoringschedulespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListMonitoringSchedulesRequestListMonitoringSchedulesPaginateTypeDef]
    ) -> _PageIterator[ListMonitoringSchedulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListMonitoringSchedules.html#SageMaker.Paginator.ListMonitoringSchedules.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listmonitoringschedulespaginator)
        """


class ListNotebookInstanceLifecycleConfigsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListNotebookInstanceLifecycleConfigs.html#SageMaker.Paginator.ListNotebookInstanceLifecycleConfigs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listnotebookinstancelifecycleconfigspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListNotebookInstanceLifecycleConfigsInputListNotebookInstanceLifecycleConfigsPaginateTypeDef
        ],
    ) -> _PageIterator[ListNotebookInstanceLifecycleConfigsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListNotebookInstanceLifecycleConfigs.html#SageMaker.Paginator.ListNotebookInstanceLifecycleConfigs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listnotebookinstancelifecycleconfigspaginator)
        """


class ListNotebookInstancesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListNotebookInstances.html#SageMaker.Paginator.ListNotebookInstances)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listnotebookinstancespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListNotebookInstancesInputListNotebookInstancesPaginateTypeDef]
    ) -> _PageIterator[ListNotebookInstancesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListNotebookInstances.html#SageMaker.Paginator.ListNotebookInstances.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listnotebookinstancespaginator)
        """


class ListOptimizationJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListOptimizationJobs.html#SageMaker.Paginator.ListOptimizationJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listoptimizationjobspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListOptimizationJobsRequestListOptimizationJobsPaginateTypeDef]
    ) -> _PageIterator[ListOptimizationJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListOptimizationJobs.html#SageMaker.Paginator.ListOptimizationJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listoptimizationjobspaginator)
        """


class ListPipelineExecutionStepsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListPipelineExecutionSteps.html#SageMaker.Paginator.ListPipelineExecutionSteps)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listpipelineexecutionstepspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListPipelineExecutionStepsRequestListPipelineExecutionStepsPaginateTypeDef
        ],
    ) -> _PageIterator[ListPipelineExecutionStepsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListPipelineExecutionSteps.html#SageMaker.Paginator.ListPipelineExecutionSteps.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listpipelineexecutionstepspaginator)
        """


class ListPipelineExecutionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListPipelineExecutions.html#SageMaker.Paginator.ListPipelineExecutions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listpipelineexecutionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListPipelineExecutionsRequestListPipelineExecutionsPaginateTypeDef]
    ) -> _PageIterator[ListPipelineExecutionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListPipelineExecutions.html#SageMaker.Paginator.ListPipelineExecutions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listpipelineexecutionspaginator)
        """


class ListPipelineParametersForExecutionPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListPipelineParametersForExecution.html#SageMaker.Paginator.ListPipelineParametersForExecution)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listpipelineparametersforexecutionpaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListPipelineParametersForExecutionRequestListPipelineParametersForExecutionPaginateTypeDef
        ],
    ) -> _PageIterator[ListPipelineParametersForExecutionResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListPipelineParametersForExecution.html#SageMaker.Paginator.ListPipelineParametersForExecution.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listpipelineparametersforexecutionpaginator)
        """


class ListPipelinesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListPipelines.html#SageMaker.Paginator.ListPipelines)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listpipelinespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListPipelinesRequestListPipelinesPaginateTypeDef]
    ) -> _PageIterator[ListPipelinesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListPipelines.html#SageMaker.Paginator.ListPipelines.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listpipelinespaginator)
        """


class ListProcessingJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListProcessingJobs.html#SageMaker.Paginator.ListProcessingJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listprocessingjobspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListProcessingJobsRequestListProcessingJobsPaginateTypeDef]
    ) -> _PageIterator[ListProcessingJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListProcessingJobs.html#SageMaker.Paginator.ListProcessingJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listprocessingjobspaginator)
        """


class ListResourceCatalogsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListResourceCatalogs.html#SageMaker.Paginator.ListResourceCatalogs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listresourcecatalogspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListResourceCatalogsRequestListResourceCatalogsPaginateTypeDef]
    ) -> _PageIterator[ListResourceCatalogsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListResourceCatalogs.html#SageMaker.Paginator.ListResourceCatalogs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listresourcecatalogspaginator)
        """


class ListSpacesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListSpaces.html#SageMaker.Paginator.ListSpaces)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listspacespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListSpacesRequestListSpacesPaginateTypeDef]
    ) -> _PageIterator[ListSpacesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListSpaces.html#SageMaker.Paginator.ListSpaces.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listspacespaginator)
        """


class ListStageDevicesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListStageDevices.html#SageMaker.Paginator.ListStageDevices)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#liststagedevicespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListStageDevicesRequestListStageDevicesPaginateTypeDef]
    ) -> _PageIterator[ListStageDevicesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListStageDevices.html#SageMaker.Paginator.ListStageDevices.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#liststagedevicespaginator)
        """


class ListStudioLifecycleConfigsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListStudioLifecycleConfigs.html#SageMaker.Paginator.ListStudioLifecycleConfigs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#liststudiolifecycleconfigspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListStudioLifecycleConfigsRequestListStudioLifecycleConfigsPaginateTypeDef
        ],
    ) -> _PageIterator[ListStudioLifecycleConfigsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListStudioLifecycleConfigs.html#SageMaker.Paginator.ListStudioLifecycleConfigs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#liststudiolifecycleconfigspaginator)
        """


class ListSubscribedWorkteamsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListSubscribedWorkteams.html#SageMaker.Paginator.ListSubscribedWorkteams)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listsubscribedworkteamspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListSubscribedWorkteamsRequestListSubscribedWorkteamsPaginateTypeDef]
    ) -> _PageIterator[ListSubscribedWorkteamsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListSubscribedWorkteams.html#SageMaker.Paginator.ListSubscribedWorkteams.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listsubscribedworkteamspaginator)
        """


class ListTagsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListTags.html#SageMaker.Paginator.ListTags)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listtagspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListTagsInputListTagsPaginateTypeDef]
    ) -> _PageIterator[ListTagsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListTags.html#SageMaker.Paginator.ListTags.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listtagspaginator)
        """


class ListTrainingJobsForHyperParameterTuningJobPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListTrainingJobsForHyperParameterTuningJob.html#SageMaker.Paginator.ListTrainingJobsForHyperParameterTuningJob)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listtrainingjobsforhyperparametertuningjobpaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListTrainingJobsForHyperParameterTuningJobRequestListTrainingJobsForHyperParameterTuningJobPaginateTypeDef
        ],
    ) -> _PageIterator[ListTrainingJobsForHyperParameterTuningJobResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListTrainingJobsForHyperParameterTuningJob.html#SageMaker.Paginator.ListTrainingJobsForHyperParameterTuningJob.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listtrainingjobsforhyperparametertuningjobpaginator)
        """


class ListTrainingJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListTrainingJobs.html#SageMaker.Paginator.ListTrainingJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listtrainingjobspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListTrainingJobsRequestListTrainingJobsPaginateTypeDef]
    ) -> _PageIterator[ListTrainingJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListTrainingJobs.html#SageMaker.Paginator.ListTrainingJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listtrainingjobspaginator)
        """


class ListTransformJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListTransformJobs.html#SageMaker.Paginator.ListTransformJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listtransformjobspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListTransformJobsRequestListTransformJobsPaginateTypeDef]
    ) -> _PageIterator[ListTransformJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListTransformJobs.html#SageMaker.Paginator.ListTransformJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listtransformjobspaginator)
        """


class ListTrialComponentsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListTrialComponents.html#SageMaker.Paginator.ListTrialComponents)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listtrialcomponentspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListTrialComponentsRequestListTrialComponentsPaginateTypeDef]
    ) -> _PageIterator[ListTrialComponentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListTrialComponents.html#SageMaker.Paginator.ListTrialComponents.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listtrialcomponentspaginator)
        """


class ListTrialsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListTrials.html#SageMaker.Paginator.ListTrials)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listtrialspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListTrialsRequestListTrialsPaginateTypeDef]
    ) -> _PageIterator[ListTrialsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListTrials.html#SageMaker.Paginator.ListTrials.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listtrialspaginator)
        """


class ListUserProfilesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListUserProfiles.html#SageMaker.Paginator.ListUserProfiles)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listuserprofilespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListUserProfilesRequestListUserProfilesPaginateTypeDef]
    ) -> _PageIterator[ListUserProfilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListUserProfiles.html#SageMaker.Paginator.ListUserProfiles.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listuserprofilespaginator)
        """


class ListWorkforcesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListWorkforces.html#SageMaker.Paginator.ListWorkforces)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listworkforcespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListWorkforcesRequestListWorkforcesPaginateTypeDef]
    ) -> _PageIterator[ListWorkforcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListWorkforces.html#SageMaker.Paginator.ListWorkforces.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listworkforcespaginator)
        """


class ListWorkteamsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListWorkteams.html#SageMaker.Paginator.ListWorkteams)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listworkteamspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListWorkteamsRequestListWorkteamsPaginateTypeDef]
    ) -> _PageIterator[ListWorkteamsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListWorkteams.html#SageMaker.Paginator.ListWorkteams.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listworkteamspaginator)
        """


class SearchPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/Search.html#SageMaker.Paginator.Search)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#searchpaginator)
    """

    def paginate(
        self, **kwargs: Unpack[SearchRequestSearchPaginateTypeDef]
    ) -> _PageIterator[SearchResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/Search.html#SageMaker.Paginator.Search.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#searchpaginator)
        """
