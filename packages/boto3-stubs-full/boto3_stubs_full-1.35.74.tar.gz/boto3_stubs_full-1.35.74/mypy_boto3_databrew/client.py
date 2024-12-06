"""
Type annotations for databrew service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_databrew/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_databrew.client import GlueDataBrewClient

    session = Session()
    client: GlueDataBrewClient = session.client("databrew")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ListDatasetsPaginator,
    ListJobRunsPaginator,
    ListJobsPaginator,
    ListProjectsPaginator,
    ListRecipesPaginator,
    ListRecipeVersionsPaginator,
    ListRulesetsPaginator,
    ListSchedulesPaginator,
)
from .type_defs import (
    BatchDeleteRecipeVersionRequestRequestTypeDef,
    BatchDeleteRecipeVersionResponseTypeDef,
    CreateDatasetRequestRequestTypeDef,
    CreateDatasetResponseTypeDef,
    CreateProfileJobRequestRequestTypeDef,
    CreateProfileJobResponseTypeDef,
    CreateProjectRequestRequestTypeDef,
    CreateProjectResponseTypeDef,
    CreateRecipeJobRequestRequestTypeDef,
    CreateRecipeJobResponseTypeDef,
    CreateRecipeRequestRequestTypeDef,
    CreateRecipeResponseTypeDef,
    CreateRulesetRequestRequestTypeDef,
    CreateRulesetResponseTypeDef,
    CreateScheduleRequestRequestTypeDef,
    CreateScheduleResponseTypeDef,
    DeleteDatasetRequestRequestTypeDef,
    DeleteDatasetResponseTypeDef,
    DeleteJobRequestRequestTypeDef,
    DeleteJobResponseTypeDef,
    DeleteProjectRequestRequestTypeDef,
    DeleteProjectResponseTypeDef,
    DeleteRecipeVersionRequestRequestTypeDef,
    DeleteRecipeVersionResponseTypeDef,
    DeleteRulesetRequestRequestTypeDef,
    DeleteRulesetResponseTypeDef,
    DeleteScheduleRequestRequestTypeDef,
    DeleteScheduleResponseTypeDef,
    DescribeDatasetRequestRequestTypeDef,
    DescribeDatasetResponseTypeDef,
    DescribeJobRequestRequestTypeDef,
    DescribeJobResponseTypeDef,
    DescribeJobRunRequestRequestTypeDef,
    DescribeJobRunResponseTypeDef,
    DescribeProjectRequestRequestTypeDef,
    DescribeProjectResponseTypeDef,
    DescribeRecipeRequestRequestTypeDef,
    DescribeRecipeResponseTypeDef,
    DescribeRulesetRequestRequestTypeDef,
    DescribeRulesetResponseTypeDef,
    DescribeScheduleRequestRequestTypeDef,
    DescribeScheduleResponseTypeDef,
    ListDatasetsRequestRequestTypeDef,
    ListDatasetsResponseTypeDef,
    ListJobRunsRequestRequestTypeDef,
    ListJobRunsResponseTypeDef,
    ListJobsRequestRequestTypeDef,
    ListJobsResponseTypeDef,
    ListProjectsRequestRequestTypeDef,
    ListProjectsResponseTypeDef,
    ListRecipesRequestRequestTypeDef,
    ListRecipesResponseTypeDef,
    ListRecipeVersionsRequestRequestTypeDef,
    ListRecipeVersionsResponseTypeDef,
    ListRulesetsRequestRequestTypeDef,
    ListRulesetsResponseTypeDef,
    ListSchedulesRequestRequestTypeDef,
    ListSchedulesResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    PublishRecipeRequestRequestTypeDef,
    PublishRecipeResponseTypeDef,
    SendProjectSessionActionRequestRequestTypeDef,
    SendProjectSessionActionResponseTypeDef,
    StartJobRunRequestRequestTypeDef,
    StartJobRunResponseTypeDef,
    StartProjectSessionRequestRequestTypeDef,
    StartProjectSessionResponseTypeDef,
    StopJobRunRequestRequestTypeDef,
    StopJobRunResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateDatasetRequestRequestTypeDef,
    UpdateDatasetResponseTypeDef,
    UpdateProfileJobRequestRequestTypeDef,
    UpdateProfileJobResponseTypeDef,
    UpdateProjectRequestRequestTypeDef,
    UpdateProjectResponseTypeDef,
    UpdateRecipeJobRequestRequestTypeDef,
    UpdateRecipeJobResponseTypeDef,
    UpdateRecipeRequestRequestTypeDef,
    UpdateRecipeResponseTypeDef,
    UpdateRulesetRequestRequestTypeDef,
    UpdateRulesetResponseTypeDef,
    UpdateScheduleRequestRequestTypeDef,
    UpdateScheduleResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("GlueDataBrewClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class GlueDataBrewClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_databrew/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        GlueDataBrewClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_databrew/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_databrew/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_databrew/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/client/close.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_databrew/client/#close)
        """

    def batch_delete_recipe_version(
        self, **kwargs: Unpack[BatchDeleteRecipeVersionRequestRequestTypeDef]
    ) -> BatchDeleteRecipeVersionResponseTypeDef:
        """
        Deletes one or more versions of a recipe at a time.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/client/batch_delete_recipe_version.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_databrew/client/#batch_delete_recipe_version)
        """

    def create_dataset(
        self, **kwargs: Unpack[CreateDatasetRequestRequestTypeDef]
    ) -> CreateDatasetResponseTypeDef:
        """
        Creates a new DataBrew dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/client/create_dataset.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_databrew/client/#create_dataset)
        """

    def create_profile_job(
        self, **kwargs: Unpack[CreateProfileJobRequestRequestTypeDef]
    ) -> CreateProfileJobResponseTypeDef:
        """
        Creates a new job to analyze a dataset and create its data profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/client/create_profile_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_databrew/client/#create_profile_job)
        """

    def create_project(
        self, **kwargs: Unpack[CreateProjectRequestRequestTypeDef]
    ) -> CreateProjectResponseTypeDef:
        """
        Creates a new DataBrew project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/client/create_project.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_databrew/client/#create_project)
        """

    def create_recipe(
        self, **kwargs: Unpack[CreateRecipeRequestRequestTypeDef]
    ) -> CreateRecipeResponseTypeDef:
        """
        Creates a new DataBrew recipe.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/client/create_recipe.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_databrew/client/#create_recipe)
        """

    def create_recipe_job(
        self, **kwargs: Unpack[CreateRecipeJobRequestRequestTypeDef]
    ) -> CreateRecipeJobResponseTypeDef:
        """
        Creates a new job to transform input data, using steps defined in an existing
        Glue DataBrew recipe.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/client/create_recipe_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_databrew/client/#create_recipe_job)
        """

    def create_ruleset(
        self, **kwargs: Unpack[CreateRulesetRequestRequestTypeDef]
    ) -> CreateRulesetResponseTypeDef:
        """
        Creates a new ruleset that can be used in a profile job to validate the data
        quality of a dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/client/create_ruleset.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_databrew/client/#create_ruleset)
        """

    def create_schedule(
        self, **kwargs: Unpack[CreateScheduleRequestRequestTypeDef]
    ) -> CreateScheduleResponseTypeDef:
        """
        Creates a new schedule for one or more DataBrew jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/client/create_schedule.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_databrew/client/#create_schedule)
        """

    def delete_dataset(
        self, **kwargs: Unpack[DeleteDatasetRequestRequestTypeDef]
    ) -> DeleteDatasetResponseTypeDef:
        """
        Deletes a dataset from DataBrew.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/client/delete_dataset.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_databrew/client/#delete_dataset)
        """

    def delete_job(
        self, **kwargs: Unpack[DeleteJobRequestRequestTypeDef]
    ) -> DeleteJobResponseTypeDef:
        """
        Deletes the specified DataBrew job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/client/delete_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_databrew/client/#delete_job)
        """

    def delete_project(
        self, **kwargs: Unpack[DeleteProjectRequestRequestTypeDef]
    ) -> DeleteProjectResponseTypeDef:
        """
        Deletes an existing DataBrew project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/client/delete_project.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_databrew/client/#delete_project)
        """

    def delete_recipe_version(
        self, **kwargs: Unpack[DeleteRecipeVersionRequestRequestTypeDef]
    ) -> DeleteRecipeVersionResponseTypeDef:
        """
        Deletes a single version of a DataBrew recipe.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/client/delete_recipe_version.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_databrew/client/#delete_recipe_version)
        """

    def delete_ruleset(
        self, **kwargs: Unpack[DeleteRulesetRequestRequestTypeDef]
    ) -> DeleteRulesetResponseTypeDef:
        """
        Deletes a ruleset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/client/delete_ruleset.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_databrew/client/#delete_ruleset)
        """

    def delete_schedule(
        self, **kwargs: Unpack[DeleteScheduleRequestRequestTypeDef]
    ) -> DeleteScheduleResponseTypeDef:
        """
        Deletes the specified DataBrew schedule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/client/delete_schedule.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_databrew/client/#delete_schedule)
        """

    def describe_dataset(
        self, **kwargs: Unpack[DescribeDatasetRequestRequestTypeDef]
    ) -> DescribeDatasetResponseTypeDef:
        """
        Returns the definition of a specific DataBrew dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/client/describe_dataset.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_databrew/client/#describe_dataset)
        """

    def describe_job(
        self, **kwargs: Unpack[DescribeJobRequestRequestTypeDef]
    ) -> DescribeJobResponseTypeDef:
        """
        Returns the definition of a specific DataBrew job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/client/describe_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_databrew/client/#describe_job)
        """

    def describe_job_run(
        self, **kwargs: Unpack[DescribeJobRunRequestRequestTypeDef]
    ) -> DescribeJobRunResponseTypeDef:
        """
        Represents one run of a DataBrew job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/client/describe_job_run.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_databrew/client/#describe_job_run)
        """

    def describe_project(
        self, **kwargs: Unpack[DescribeProjectRequestRequestTypeDef]
    ) -> DescribeProjectResponseTypeDef:
        """
        Returns the definition of a specific DataBrew project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/client/describe_project.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_databrew/client/#describe_project)
        """

    def describe_recipe(
        self, **kwargs: Unpack[DescribeRecipeRequestRequestTypeDef]
    ) -> DescribeRecipeResponseTypeDef:
        """
        Returns the definition of a specific DataBrew recipe corresponding to a
        particular version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/client/describe_recipe.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_databrew/client/#describe_recipe)
        """

    def describe_ruleset(
        self, **kwargs: Unpack[DescribeRulesetRequestRequestTypeDef]
    ) -> DescribeRulesetResponseTypeDef:
        """
        Retrieves detailed information about the ruleset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/client/describe_ruleset.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_databrew/client/#describe_ruleset)
        """

    def describe_schedule(
        self, **kwargs: Unpack[DescribeScheduleRequestRequestTypeDef]
    ) -> DescribeScheduleResponseTypeDef:
        """
        Returns the definition of a specific DataBrew schedule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/client/describe_schedule.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_databrew/client/#describe_schedule)
        """

    def list_datasets(
        self, **kwargs: Unpack[ListDatasetsRequestRequestTypeDef]
    ) -> ListDatasetsResponseTypeDef:
        """
        Lists all of the DataBrew datasets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/client/list_datasets.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_databrew/client/#list_datasets)
        """

    def list_job_runs(
        self, **kwargs: Unpack[ListJobRunsRequestRequestTypeDef]
    ) -> ListJobRunsResponseTypeDef:
        """
        Lists all of the previous runs of a particular DataBrew job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/client/list_job_runs.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_databrew/client/#list_job_runs)
        """

    def list_jobs(self, **kwargs: Unpack[ListJobsRequestRequestTypeDef]) -> ListJobsResponseTypeDef:
        """
        Lists all of the DataBrew jobs that are defined.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/client/list_jobs.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_databrew/client/#list_jobs)
        """

    def list_projects(
        self, **kwargs: Unpack[ListProjectsRequestRequestTypeDef]
    ) -> ListProjectsResponseTypeDef:
        """
        Lists all of the DataBrew projects that are defined.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/client/list_projects.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_databrew/client/#list_projects)
        """

    def list_recipe_versions(
        self, **kwargs: Unpack[ListRecipeVersionsRequestRequestTypeDef]
    ) -> ListRecipeVersionsResponseTypeDef:
        """
        Lists the versions of a particular DataBrew recipe, except for
        <code>LATEST_WORKING</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/client/list_recipe_versions.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_databrew/client/#list_recipe_versions)
        """

    def list_recipes(
        self, **kwargs: Unpack[ListRecipesRequestRequestTypeDef]
    ) -> ListRecipesResponseTypeDef:
        """
        Lists all of the DataBrew recipes that are defined.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/client/list_recipes.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_databrew/client/#list_recipes)
        """

    def list_rulesets(
        self, **kwargs: Unpack[ListRulesetsRequestRequestTypeDef]
    ) -> ListRulesetsResponseTypeDef:
        """
        List all rulesets available in the current account or rulesets associated with
        a specific resource (dataset).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/client/list_rulesets.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_databrew/client/#list_rulesets)
        """

    def list_schedules(
        self, **kwargs: Unpack[ListSchedulesRequestRequestTypeDef]
    ) -> ListSchedulesResponseTypeDef:
        """
        Lists the DataBrew schedules that are defined.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/client/list_schedules.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_databrew/client/#list_schedules)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists all the tags for a DataBrew resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/client/list_tags_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_databrew/client/#list_tags_for_resource)
        """

    def publish_recipe(
        self, **kwargs: Unpack[PublishRecipeRequestRequestTypeDef]
    ) -> PublishRecipeResponseTypeDef:
        """
        Publishes a new version of a DataBrew recipe.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/client/publish_recipe.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_databrew/client/#publish_recipe)
        """

    def send_project_session_action(
        self, **kwargs: Unpack[SendProjectSessionActionRequestRequestTypeDef]
    ) -> SendProjectSessionActionResponseTypeDef:
        """
        Performs a recipe step within an interactive DataBrew session that's currently
        open.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/client/send_project_session_action.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_databrew/client/#send_project_session_action)
        """

    def start_job_run(
        self, **kwargs: Unpack[StartJobRunRequestRequestTypeDef]
    ) -> StartJobRunResponseTypeDef:
        """
        Runs a DataBrew job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/client/start_job_run.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_databrew/client/#start_job_run)
        """

    def start_project_session(
        self, **kwargs: Unpack[StartProjectSessionRequestRequestTypeDef]
    ) -> StartProjectSessionResponseTypeDef:
        """
        Creates an interactive session, enabling you to manipulate data in a DataBrew
        project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/client/start_project_session.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_databrew/client/#start_project_session)
        """

    def stop_job_run(
        self, **kwargs: Unpack[StopJobRunRequestRequestTypeDef]
    ) -> StopJobRunResponseTypeDef:
        """
        Stops a particular run of a job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/client/stop_job_run.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_databrew/client/#stop_job_run)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Adds metadata tags to a DataBrew resource, such as a dataset, project, recipe,
        job, or schedule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/client/tag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_databrew/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes metadata tags from a DataBrew resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/client/untag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_databrew/client/#untag_resource)
        """

    def update_dataset(
        self, **kwargs: Unpack[UpdateDatasetRequestRequestTypeDef]
    ) -> UpdateDatasetResponseTypeDef:
        """
        Modifies the definition of an existing DataBrew dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/client/update_dataset.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_databrew/client/#update_dataset)
        """

    def update_profile_job(
        self, **kwargs: Unpack[UpdateProfileJobRequestRequestTypeDef]
    ) -> UpdateProfileJobResponseTypeDef:
        """
        Modifies the definition of an existing profile job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/client/update_profile_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_databrew/client/#update_profile_job)
        """

    def update_project(
        self, **kwargs: Unpack[UpdateProjectRequestRequestTypeDef]
    ) -> UpdateProjectResponseTypeDef:
        """
        Modifies the definition of an existing DataBrew project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/client/update_project.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_databrew/client/#update_project)
        """

    def update_recipe(
        self, **kwargs: Unpack[UpdateRecipeRequestRequestTypeDef]
    ) -> UpdateRecipeResponseTypeDef:
        """
        Modifies the definition of the <code>LATEST_WORKING</code> version of a
        DataBrew recipe.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/client/update_recipe.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_databrew/client/#update_recipe)
        """

    def update_recipe_job(
        self, **kwargs: Unpack[UpdateRecipeJobRequestRequestTypeDef]
    ) -> UpdateRecipeJobResponseTypeDef:
        """
        Modifies the definition of an existing DataBrew recipe job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/client/update_recipe_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_databrew/client/#update_recipe_job)
        """

    def update_ruleset(
        self, **kwargs: Unpack[UpdateRulesetRequestRequestTypeDef]
    ) -> UpdateRulesetResponseTypeDef:
        """
        Updates specified ruleset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/client/update_ruleset.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_databrew/client/#update_ruleset)
        """

    def update_schedule(
        self, **kwargs: Unpack[UpdateScheduleRequestRequestTypeDef]
    ) -> UpdateScheduleResponseTypeDef:
        """
        Modifies the definition of an existing DataBrew schedule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/client/update_schedule.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_databrew/client/#update_schedule)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_datasets"]) -> ListDatasetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_databrew/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_job_runs"]) -> ListJobRunsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_databrew/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_jobs"]) -> ListJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_databrew/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_projects"]) -> ListProjectsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_databrew/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_recipe_versions"]
    ) -> ListRecipeVersionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_databrew/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_recipes"]) -> ListRecipesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_databrew/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_rulesets"]) -> ListRulesetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_databrew/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_schedules"]) -> ListSchedulesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_databrew/client/#get_paginator)
        """
