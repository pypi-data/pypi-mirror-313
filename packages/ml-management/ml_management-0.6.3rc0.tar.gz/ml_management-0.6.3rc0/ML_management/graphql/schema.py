import sgqlc.types


schema = sgqlc.types.Schema()


__docformat__ = 'markdown'


########################################################################
# Scalars and Enumerations
########################################################################
Boolean = sgqlc.types.Boolean

Float = sgqlc.types.Float

ID = sgqlc.types.ID

Int = sgqlc.types.Int

class JSON(sgqlc.types.Scalar):
    '''The `JSON` scalar type represents JSON values as specified by
    [ECMA-404](http://www.ecma-
    international.org/publications/files/ECMA-ST/ECMA-404.pdf).
    '''
    __schema__ = schema


class JobStatus(sgqlc.types.Enum):
    '''Enumeration Choices:

    * `CANCELED`None
    * `FAILED`None
    * `PLANNED`None
    * `RUNNING`None
    * `SUCCESSFUL`None
    * `UNKNOWN`None
    '''
    __schema__ = schema
    __choices__ = ('CANCELED', 'FAILED', 'PLANNED', 'RUNNING', 'SUCCESSFUL', 'UNKNOWN')


class JobsSortBy(sgqlc.types.Enum):
    '''Enumeration Choices:

    * `name`None
    * `registration_timestamp`None
    '''
    __schema__ = schema
    __choices__ = ('name', 'registration_timestamp')


class LONG(sgqlc.types.Scalar):
    '''The `LONG` scalar type represents long int type.'''
    __schema__ = schema


class ObjectSortBy(sgqlc.types.Enum):
    '''Enumeration Choices:

    * `creation_timestamp`None
    * `name`None
    '''
    __schema__ = schema
    __choices__ = ('creation_timestamp', 'name')


class ObjectVersionSortBy(sgqlc.types.Enum):
    '''Enumeration Choices:

    * `creation_timestamp`None
    * `name`None
    * `version`None
    '''
    __schema__ = schema
    __choices__ = ('creation_timestamp', 'name', 'version')


class PeriodicType(sgqlc.types.Enum):
    '''Enumeration Choices:

    * `ONCE`None
    * `PERIODIC`None
    '''
    __schema__ = schema
    __choices__ = ('ONCE', 'PERIODIC')


class SortDirection(sgqlc.types.Enum):
    '''Enumeration Choices:

    * `ascending`None
    * `descending`None
    '''
    __schema__ = schema
    __choices__ = ('ascending', 'descending')


String = sgqlc.types.String

class UploadModelType(sgqlc.types.Enum):
    '''Enumeration Choices:

    * `new_model`None
    * `new_version`None
    * `root`None
    '''
    __schema__ = schema
    __choices__ = ('new_model', 'new_version', 'root')



########################################################################
# Input Objects
########################################################################
class DataParamsInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('collector_method_params', 'collector_name', 'dataset_loader_version_choice', 'list_dataset_loader_method_params')
    collector_method_params = sgqlc.types.Field(sgqlc.types.non_null('MethodParamsInput'), graphql_name='collectorMethodParams')

    collector_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='collectorName')

    dataset_loader_version_choice = sgqlc.types.Field(sgqlc.types.non_null('ObjectVersionOptionalInput'), graphql_name='datasetLoaderVersionChoice')

    list_dataset_loader_method_params = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('MethodParamsInput'))), graphql_name='listDatasetLoaderMethodParams')



class ExecutorParamsInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('executor_method_params', 'executor_version_choice')
    executor_method_params = sgqlc.types.Field(sgqlc.types.non_null('MethodParamsInput'), graphql_name='executorMethodParams')

    executor_version_choice = sgqlc.types.Field(sgqlc.types.non_null('ObjectVersionOptionalInput'), graphql_name='executorVersionChoice')



class JobFilterSettings(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('dataset_loader_version', 'end_interval', 'executor_version', 'experiment_name', 'init_model_version', 'job_name', 'periodic_type', 'start_interval', 'status')
    dataset_loader_version = sgqlc.types.Field('ObjectVersionInput', graphql_name='datasetLoaderVersion')

    end_interval = sgqlc.types.Field('TimestampInterval', graphql_name='endInterval')

    executor_version = sgqlc.types.Field('ObjectVersionInput', graphql_name='executorVersion')

    experiment_name = sgqlc.types.Field(String, graphql_name='experimentName')

    init_model_version = sgqlc.types.Field('ObjectVersionInput', graphql_name='initModelVersion')

    job_name = sgqlc.types.Field(String, graphql_name='jobName')

    periodic_type = sgqlc.types.Field(PeriodicType, graphql_name='periodicType')

    start_interval = sgqlc.types.Field('TimestampInterval', graphql_name='startInterval')

    status = sgqlc.types.Field(JobStatus, graphql_name='status')



class JobParameters(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('additional_system_packages', 'cron_expression', 'executor_params', 'experiment_name', 'gpu', 'job_name', 'list_role_data_params', 'list_role_model_params', 'periodic_type')
    additional_system_packages = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='additionalSystemPackages')

    cron_expression = sgqlc.types.Field(String, graphql_name='cronExpression')

    executor_params = sgqlc.types.Field(sgqlc.types.non_null(ExecutorParamsInput), graphql_name='executorParams')

    experiment_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='experimentName')

    gpu = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='gpu')

    job_name = sgqlc.types.Field(String, graphql_name='jobName')

    list_role_data_params = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('RoleDataParamsInput')), graphql_name='listRoleDataParams')

    list_role_model_params = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('RoleModelParamsInput')), graphql_name='listRoleModelParams')

    periodic_type = sgqlc.types.Field(sgqlc.types.non_null(PeriodicType), graphql_name='periodicType')



class JobsSortBySortingInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('direction', 'sort_field')
    direction = sgqlc.types.Field(sgqlc.types.non_null(SortDirection), graphql_name='direction')

    sort_field = sgqlc.types.Field(sgqlc.types.non_null(JobsSortBy), graphql_name='sortField')



class MethodParamsInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('method_name', 'method_params')
    method_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='methodName')

    method_params = sgqlc.types.Field(sgqlc.types.non_null(JSON), graphql_name='methodParams')



class MetricInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('key', 'step', 'value')
    key = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='key')

    step = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='step')

    value = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='value')



class ModelParamsInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('description', 'list_model_method_params', 'model_version_choice', 'new_model_name', 'prepare_new_model_inference')
    description = sgqlc.types.Field(String, graphql_name='description')

    list_model_method_params = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(MethodParamsInput))), graphql_name='listModelMethodParams')

    model_version_choice = sgqlc.types.Field(sgqlc.types.non_null('ModelVersionChoice'), graphql_name='modelVersionChoice')

    new_model_name = sgqlc.types.Field(String, graphql_name='newModelName')

    prepare_new_model_inference = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='prepareNewModelInference')



class ModelServingInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('gpu', 'model_version')
    gpu = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='gpu')

    model_version = sgqlc.types.Field(sgqlc.types.non_null('ObjectVersionInput'), graphql_name='modelVersion')



class ModelVersionChoice(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('choice_criteria', 'name', 'version')
    choice_criteria = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='choiceCriteria')

    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')

    version = sgqlc.types.Field(Int, graphql_name='version')



class ObjectFilterSettings(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('name',)
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')



class ObjectSortBySortingInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('direction', 'sort_field')
    direction = sgqlc.types.Field(sgqlc.types.non_null(SortDirection), graphql_name='direction')

    sort_field = sgqlc.types.Field(sgqlc.types.non_null(ObjectSortBy), graphql_name='sortField')



class ObjectVersionFilterSettings(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('version',)
    version = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='version')



class ObjectVersionInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('name', 'version')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')

    version = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='version')



class ObjectVersionOptionalInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('name', 'version')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')

    version = sgqlc.types.Field(Int, graphql_name='version')



class ObjectVersionSortBySortingInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('direction', 'sort_field')
    direction = sgqlc.types.Field(sgqlc.types.non_null(SortDirection), graphql_name='direction')

    sort_field = sgqlc.types.Field(sgqlc.types.non_null(ObjectVersionSortBy), graphql_name='sortField')



class ParamInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('key', 'value')
    key = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='key')

    value = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='value')



class RoleDataParamsInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('data_params', 'role')
    data_params = sgqlc.types.Field(sgqlc.types.non_null(DataParamsInput), graphql_name='dataParams')

    role = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='role')



class RoleModelParamsInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('model_params', 'role')
    model_params = sgqlc.types.Field(sgqlc.types.non_null(ModelParamsInput), graphql_name='modelParams')

    role = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='role')



class RoleObjectVersionInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('object_version', 'role')
    object_version = sgqlc.types.Field(sgqlc.types.non_null(ObjectVersionInput), graphql_name='objectVersion')

    role = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='role')



class TimestampInterval(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('end', 'start')
    end = sgqlc.types.Field(LONG, graphql_name='end')

    start = sgqlc.types.Field(LONG, graphql_name='start')



class UpdateExperimentForm(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('new_description', 'new_name')
    new_description = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='newDescription')

    new_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='newName')




########################################################################
# Output Objects and Interfaces
########################################################################
class ArtifactPath(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('isdir', 'path', 'size')
    isdir = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='isdir')

    path = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='path')

    size = sgqlc.types.Field(LONG, graphql_name='size')



class BuildJob(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('build_object_name', 'end_timestamp', 'exception', 'id', 'start_timestamp', 'status')
    build_object_name = sgqlc.types.Field(String, graphql_name='buildObjectName')

    end_timestamp = sgqlc.types.Field(LONG, graphql_name='endTimestamp')

    exception = sgqlc.types.Field(String, graphql_name='exception')

    id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='id')

    start_timestamp = sgqlc.types.Field(LONG, graphql_name='startTimestamp')

    status = sgqlc.types.Field(sgqlc.types.non_null(JobStatus), graphql_name='status')



class DataParams(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('collector_method_params', 'collector_name', 'dataset_loader_version_choice', 'list_dataset_loader_method_params')
    collector_method_params = sgqlc.types.Field(sgqlc.types.non_null('MethodParams'), graphql_name='collectorMethodParams')

    collector_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='collectorName')

    dataset_loader_version_choice = sgqlc.types.Field(sgqlc.types.non_null('ObjectVersion'), graphql_name='datasetLoaderVersionChoice')

    list_dataset_loader_method_params = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('MethodParams'))), graphql_name='listDatasetLoaderMethodParams')



class DataSchema(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('collector_method_schema', 'dataset_loader_method_schemas', 'role')
    collector_method_schema = sgqlc.types.Field(sgqlc.types.non_null('MethodSchema'), graphql_name='collectorMethodSchema')

    dataset_loader_method_schemas = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('MethodSchema'))), graphql_name='datasetLoaderMethodSchemas')

    role = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='role')



class DatasetLoaderInfo(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('creation_timestamp', 'description', 'init_dataset_loader_version', 'last_updated_timestamp', 'latest_dataset_loader_version', 'list_dataset_loader_version', 'name', 'owner', 'pagination_dataset_loader_version', 'tags')
    creation_timestamp = sgqlc.types.Field(sgqlc.types.non_null(LONG), graphql_name='creationTimestamp')

    description = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='description')

    init_dataset_loader_version = sgqlc.types.Field(sgqlc.types.non_null('DatasetLoaderVersionInfo'), graphql_name='initDatasetLoaderVersion')

    last_updated_timestamp = sgqlc.types.Field(LONG, graphql_name='lastUpdatedTimestamp')

    latest_dataset_loader_version = sgqlc.types.Field(sgqlc.types.non_null('DatasetLoaderVersionInfo'), graphql_name='latestDatasetLoaderVersion')

    list_dataset_loader_version = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('DatasetLoaderVersionInfo'))), graphql_name='listDatasetLoaderVersion', args=sgqlc.types.ArgDict((
        ('sorting', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(ObjectVersionSortBySortingInput)), graphql_name='sorting', default=None)),
))
    )
    '''Arguments:

    * `sorting` (`[ObjectVersionSortBySortingInput!]`)None (default:
      `null`)
    '''

    name = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='name')

    owner = sgqlc.types.Field(sgqlc.types.non_null('User'), graphql_name='owner')

    pagination_dataset_loader_version = sgqlc.types.Field(sgqlc.types.non_null('DatasetLoaderVersionPagination'), graphql_name='paginationDatasetLoaderVersion', args=sgqlc.types.ArgDict((
        ('filter_settings', sgqlc.types.Arg(ObjectVersionFilterSettings, graphql_name='filterSettings', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('sorting', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(ObjectVersionSortBySortingInput)), graphql_name='sorting', default=None)),
))
    )
    '''Arguments:

    * `filter_settings` (`ObjectVersionFilterSettings`)None (default:
      `null`)
    * `limit` (`Int`)None (default: `null`)
    * `offset` (`Int`)None (default: `null`)
    * `sorting` (`[ObjectVersionSortBySortingInput!]`)None (default:
      `null`)
    '''

    tags = sgqlc.types.Field(sgqlc.types.non_null(JSON), graphql_name='tags')



class DatasetLoaderPagination(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('list_dataset_loader', 'total')
    list_dataset_loader = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(DatasetLoaderInfo))), graphql_name='listDatasetLoader')

    total = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='total')



class DatasetLoaderVersionInfo(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('creation_timestamp', 'dataset_loader', 'dataset_loader_method_schema_names', 'dataset_loader_method_schemas', 'description', 'get_conda_env', 'last_updated_timestamp', 'list_artifacts', 'list_deployed_jobs', 'list_requirements', 'name', 'pagination_deployed_jobs', 'source_path', 'tags', 'version')
    creation_timestamp = sgqlc.types.Field(sgqlc.types.non_null(LONG), graphql_name='creationTimestamp')

    dataset_loader = sgqlc.types.Field(sgqlc.types.non_null(DatasetLoaderInfo), graphql_name='datasetLoader')

    dataset_loader_method_schema_names = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='datasetLoaderMethodSchemaNames')

    dataset_loader_method_schemas = sgqlc.types.Field(sgqlc.types.non_null(JSON), graphql_name='datasetLoaderMethodSchemas')

    description = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='description')

    get_conda_env = sgqlc.types.Field(sgqlc.types.non_null(JSON), graphql_name='getCondaEnv')

    last_updated_timestamp = sgqlc.types.Field(LONG, graphql_name='lastUpdatedTimestamp')

    list_artifacts = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ArtifactPath))), graphql_name='listArtifacts', args=sgqlc.types.ArgDict((
        ('path', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='path', default='')),
))
    )
    '''Arguments:

    * `path` (`String!`)None (default: `""`)
    '''

    list_deployed_jobs = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('ExecutionJob'))), graphql_name='listDeployedJobs')

    list_requirements = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='listRequirements')

    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')

    pagination_deployed_jobs = sgqlc.types.Field(sgqlc.types.non_null('JobPagination'), graphql_name='paginationDeployedJobs', args=sgqlc.types.ArgDict((
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
))
    )
    '''Arguments:

    * `limit` (`Int`)None (default: `null`)
    * `offset` (`Int`)None (default: `null`)
    '''

    source_path = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='sourcePath')

    tags = sgqlc.types.Field(sgqlc.types.non_null(JSON), graphql_name='tags')

    version = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='version')



class DatasetLoaderVersionPagination(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('list_dataset_loader_version', 'total')
    list_dataset_loader_version = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(DatasetLoaderVersionInfo))), graphql_name='listDatasetLoaderVersion')

    total = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='total')



class ExecutionJob(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('available_metrics', 'build_job', 'end_timestamp', 'exception', 'executor_version', 'experiment', 'latest_metrics', 'list_artifacts', 'list_dataset_loader_versions', 'list_init_role_model_version', 'list_params', 'list_result_model_version', 'metric_history', 'name', 'params', 'periodic_type', 'registration_timestamp', 'start_timestamp', 'status')
    available_metrics = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='availableMetrics')

    build_job = sgqlc.types.Field(BuildJob, graphql_name='buildJob')

    end_timestamp = sgqlc.types.Field(LONG, graphql_name='endTimestamp')

    exception = sgqlc.types.Field(String, graphql_name='exception')

    executor_version = sgqlc.types.Field(sgqlc.types.non_null('ExecutorVersionInfo'), graphql_name='executorVersion')

    experiment = sgqlc.types.Field('Experiment', graphql_name='experiment')

    latest_metrics = sgqlc.types.Field(sgqlc.types.non_null(JSON), graphql_name='latestMetrics')

    list_artifacts = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ArtifactPath))), graphql_name='listArtifacts', args=sgqlc.types.ArgDict((
        ('path', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='path', default='')),
))
    )
    '''Arguments:

    * `path` (`String!`)None (default: `""`)
    '''

    list_dataset_loader_versions = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('RoleDatasetLoaderVersion'))), graphql_name='listDatasetLoaderVersions')

    list_init_role_model_version = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('RoleModelVersion'))), graphql_name='listInitRoleModelVersion')

    list_params = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('Param'))), graphql_name='listParams')

    list_result_model_version = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('ModelVersionInfo'))), graphql_name='listResultModelVersion', args=sgqlc.types.ArgDict((
        ('sorting', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(ObjectVersionSortBySortingInput)), graphql_name='sorting', default=None)),
))
    )
    '''Arguments:

    * `sorting` (`[ObjectVersionSortBySortingInput!]`)None (default:
      `null`)
    '''

    metric_history = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('Metric'))), graphql_name='metricHistory', args=sgqlc.types.ArgDict((
        ('metric', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='metric', default=None)),
))
    )
    '''Arguments:

    * `metric` (`String!`)None
    '''

    name = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='name')

    params = sgqlc.types.Field(sgqlc.types.non_null('JobParams'), graphql_name='params')

    periodic_type = sgqlc.types.Field(sgqlc.types.non_null(PeriodicType), graphql_name='periodicType')

    registration_timestamp = sgqlc.types.Field(sgqlc.types.non_null(LONG), graphql_name='registrationTimestamp')

    start_timestamp = sgqlc.types.Field(LONG, graphql_name='startTimestamp')

    status = sgqlc.types.Field(sgqlc.types.non_null(JobStatus), graphql_name='status')



class ExecutorInfo(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('creation_timestamp', 'description', 'init_executor_version', 'last_updated_timestamp', 'latest_executor_version', 'list_executor_version', 'name', 'owner', 'pagination_executor_version', 'tags')
    creation_timestamp = sgqlc.types.Field(sgqlc.types.non_null(LONG), graphql_name='creationTimestamp')

    description = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='description')

    init_executor_version = sgqlc.types.Field(sgqlc.types.non_null('ExecutorVersionInfo'), graphql_name='initExecutorVersion')

    last_updated_timestamp = sgqlc.types.Field(LONG, graphql_name='lastUpdatedTimestamp')

    latest_executor_version = sgqlc.types.Field(sgqlc.types.non_null('ExecutorVersionInfo'), graphql_name='latestExecutorVersion')

    list_executor_version = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('ExecutorVersionInfo'))), graphql_name='listExecutorVersion', args=sgqlc.types.ArgDict((
        ('sorting', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(ObjectVersionSortBySortingInput)), graphql_name='sorting', default=None)),
))
    )
    '''Arguments:

    * `sorting` (`[ObjectVersionSortBySortingInput!]`)None (default:
      `null`)
    '''

    name = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='name')

    owner = sgqlc.types.Field(sgqlc.types.non_null('User'), graphql_name='owner')

    pagination_executor_version = sgqlc.types.Field(sgqlc.types.non_null('ExecutorVersionPagination'), graphql_name='paginationExecutorVersion', args=sgqlc.types.ArgDict((
        ('filter_settings', sgqlc.types.Arg(ObjectVersionFilterSettings, graphql_name='filterSettings', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('sorting', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(ObjectVersionSortBySortingInput)), graphql_name='sorting', default=None)),
))
    )
    '''Arguments:

    * `filter_settings` (`ObjectVersionFilterSettings`)None (default:
      `null`)
    * `limit` (`Int`)None (default: `null`)
    * `offset` (`Int`)None (default: `null`)
    * `sorting` (`[ObjectVersionSortBySortingInput!]`)None (default:
      `null`)
    '''

    tags = sgqlc.types.Field(sgqlc.types.non_null(JSON), graphql_name='tags')



class ExecutorPagination(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('list_executor', 'total')
    list_executor = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ExecutorInfo))), graphql_name='listExecutor')

    total = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='total')



class ExecutorParams(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('executor_method_params', 'executor_version_choice')
    executor_method_params = sgqlc.types.Field(sgqlc.types.non_null('MethodParams'), graphql_name='executorMethodParams')

    executor_version_choice = sgqlc.types.Field(sgqlc.types.non_null('ObjectVersion'), graphql_name='executorVersionChoice')



class ExecutorVersionInfo(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('available_collectors', 'available_dataset_loader_versions', 'available_dataset_loaders', 'available_model_versions', 'available_models', 'build_job', 'creation_timestamp', 'description', 'desired_dataset_loader_methods', 'desired_model_methods', 'desired_model_patterns', 'executor', 'executor_method_schema', 'executor_method_schema_name', 'get_conda_env', 'job_json_schema', 'job_json_schema_for_dataset_loaders', 'job_json_schema_for_models', 'job_json_schema_for_role_dataset_loader', 'job_json_schema_for_role_model', 'last_updated_timestamp', 'list_artifacts', 'list_deployed_jobs', 'list_requirements', 'name', 'pagination_available_collectors', 'pagination_available_dataset_loader_versions', 'pagination_available_dataset_loaders', 'pagination_available_model_versions', 'pagination_available_models', 'pagination_deployed_jobs', 'source_path', 'tags', 'upload_model_modes', 'version')
    available_collectors = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('InlineObject'))), graphql_name='availableCollectors')

    available_dataset_loader_versions = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('InlineObjectVersion'))), graphql_name='availableDatasetLoaderVersions', args=sgqlc.types.ArgDict((
        ('dataset_loader_name', sgqlc.types.Arg(String, graphql_name='datasetLoaderName', default=None)),
        ('role', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='role', default=None)),
))
    )
    '''Arguments:

    * `dataset_loader_name` (`String`)None (default: `null`)
    * `role` (`String!`)None
    '''

    available_dataset_loaders = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('InlineObject'))), graphql_name='availableDatasetLoaders', args=sgqlc.types.ArgDict((
        ('role', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='role', default=None)),
))
    )
    '''Arguments:

    * `role` (`String!`)None
    '''

    available_model_versions = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('InlineObjectVersion'))), graphql_name='availableModelVersions', args=sgqlc.types.ArgDict((
        ('model_name', sgqlc.types.Arg(String, graphql_name='modelName', default=None)),
        ('role', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='role', default=None)),
))
    )
    '''Arguments:

    * `model_name` (`String`)None (default: `null`)
    * `role` (`String!`)None
    '''

    available_models = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('InlineObject'))), graphql_name='availableModels', args=sgqlc.types.ArgDict((
        ('role', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='role', default=None)),
))
    )
    '''Arguments:

    * `role` (`String!`)None
    '''

    build_job = sgqlc.types.Field(BuildJob, graphql_name='buildJob')

    creation_timestamp = sgqlc.types.Field(sgqlc.types.non_null(LONG), graphql_name='creationTimestamp')

    description = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='description')

    desired_dataset_loader_methods = sgqlc.types.Field(sgqlc.types.non_null(JSON), graphql_name='desiredDatasetLoaderMethods')

    desired_model_methods = sgqlc.types.Field(sgqlc.types.non_null(JSON), graphql_name='desiredModelMethods')

    desired_model_patterns = sgqlc.types.Field(sgqlc.types.non_null(JSON), graphql_name='desiredModelPatterns')

    executor = sgqlc.types.Field(sgqlc.types.non_null(ExecutorInfo), graphql_name='executor')

    executor_method_schema = sgqlc.types.Field(sgqlc.types.non_null(JSON), graphql_name='executorMethodSchema')

    executor_method_schema_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='executorMethodSchemaName')

    get_conda_env = sgqlc.types.Field(sgqlc.types.non_null(JSON), graphql_name='getCondaEnv')

    job_json_schema = sgqlc.types.Field(sgqlc.types.non_null('JobSchema'), graphql_name='jobJsonSchema', args=sgqlc.types.ArgDict((
        ('dataset_loaders', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(RoleObjectVersionInput))), graphql_name='datasetLoaders', default=None)),
        ('models', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(RoleObjectVersionInput))), graphql_name='models', default=None)),
))
    )
    '''Arguments:

    * `dataset_loaders` (`[RoleObjectVersionInput!]!`)None
    * `models` (`[RoleObjectVersionInput!]!`)None
    '''

    job_json_schema_for_dataset_loaders = sgqlc.types.Field(sgqlc.types.non_null('JobDatasetLoadersSchema'), graphql_name='jobJsonSchemaForDatasetLoaders', args=sgqlc.types.ArgDict((
        ('dataset_loaders', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(RoleObjectVersionInput))), graphql_name='datasetLoaders', default=None)),
))
    )
    '''Arguments:

    * `dataset_loaders` (`[RoleObjectVersionInput!]!`)None
    '''

    job_json_schema_for_models = sgqlc.types.Field(sgqlc.types.non_null('JobModelsSchema'), graphql_name='jobJsonSchemaForModels', args=sgqlc.types.ArgDict((
        ('models', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(RoleObjectVersionInput))), graphql_name='models', default=None)),
))
    )
    '''Arguments:

    * `models` (`[RoleObjectVersionInput!]!`)None
    '''

    job_json_schema_for_role_dataset_loader = sgqlc.types.Field(sgqlc.types.non_null(DataSchema), graphql_name='jobJsonSchemaForRoleDatasetLoader', args=sgqlc.types.ArgDict((
        ('collector_name', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='collectorName', default=None)),
        ('dataset_loader', sgqlc.types.Arg(sgqlc.types.non_null(RoleObjectVersionInput), graphql_name='datasetLoader', default=None)),
))
    )
    '''Arguments:

    * `collector_name` (`String!`)None
    * `dataset_loader` (`RoleObjectVersionInput!`)None
    '''

    job_json_schema_for_role_model = sgqlc.types.Field(sgqlc.types.non_null('RoleMethodSchema'), graphql_name='jobJsonSchemaForRoleModel', args=sgqlc.types.ArgDict((
        ('model', sgqlc.types.Arg(sgqlc.types.non_null(RoleObjectVersionInput), graphql_name='model', default=None)),
))
    )
    '''Arguments:

    * `model` (`RoleObjectVersionInput!`)None
    '''

    last_updated_timestamp = sgqlc.types.Field(LONG, graphql_name='lastUpdatedTimestamp')

    list_artifacts = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ArtifactPath))), graphql_name='listArtifacts', args=sgqlc.types.ArgDict((
        ('path', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='path', default='')),
))
    )
    '''Arguments:

    * `path` (`String!`)None (default: `""`)
    '''

    list_deployed_jobs = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ExecutionJob))), graphql_name='listDeployedJobs')

    list_requirements = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='listRequirements')

    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')

    pagination_available_collectors = sgqlc.types.Field(sgqlc.types.non_null('InlineObjectPagination'), graphql_name='paginationAvailableCollectors', args=sgqlc.types.ArgDict((
        ('filter_settings', sgqlc.types.Arg(ObjectFilterSettings, graphql_name='filterSettings', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
))
    )
    '''Arguments:

    * `filter_settings` (`ObjectFilterSettings`)None (default: `null`)
    * `limit` (`Int`)None (default: `null`)
    * `offset` (`Int`)None (default: `null`)
    '''

    pagination_available_dataset_loader_versions = sgqlc.types.Field(sgqlc.types.non_null('InlineObjectVersionPagination'), graphql_name='paginationAvailableDatasetLoaderVersions', args=sgqlc.types.ArgDict((
        ('dataset_loader_name', sgqlc.types.Arg(String, graphql_name='datasetLoaderName', default=None)),
        ('filter_settings', sgqlc.types.Arg(ObjectVersionFilterSettings, graphql_name='filterSettings', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('role', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='role', default=None)),
        ('sorting', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(ObjectVersionSortBySortingInput)), graphql_name='sorting', default=None)),
))
    )
    '''Arguments:

    * `dataset_loader_name` (`String`)None (default: `null`)
    * `filter_settings` (`ObjectVersionFilterSettings`)None (default:
      `null`)
    * `limit` (`Int`)None (default: `null`)
    * `offset` (`Int`)None (default: `null`)
    * `role` (`String!`)None
    * `sorting` (`[ObjectVersionSortBySortingInput!]`)None (default:
      `null`)
    '''

    pagination_available_dataset_loaders = sgqlc.types.Field(sgqlc.types.non_null('InlineObjectPagination'), graphql_name='paginationAvailableDatasetLoaders', args=sgqlc.types.ArgDict((
        ('filter_settings', sgqlc.types.Arg(ObjectFilterSettings, graphql_name='filterSettings', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('role', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='role', default=None)),
        ('sorting', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(ObjectSortBySortingInput)), graphql_name='sorting', default=None)),
))
    )
    '''Arguments:

    * `filter_settings` (`ObjectFilterSettings`)None (default: `null`)
    * `limit` (`Int`)None (default: `null`)
    * `offset` (`Int`)None (default: `null`)
    * `role` (`String!`)None
    * `sorting` (`[ObjectSortBySortingInput!]`)None (default: `null`)
    '''

    pagination_available_model_versions = sgqlc.types.Field(sgqlc.types.non_null('InlineObjectVersionPagination'), graphql_name='paginationAvailableModelVersions', args=sgqlc.types.ArgDict((
        ('filter_settings', sgqlc.types.Arg(ObjectVersionFilterSettings, graphql_name='filterSettings', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('model_name', sgqlc.types.Arg(String, graphql_name='modelName', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('role', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='role', default=None)),
        ('sorting', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(ObjectVersionSortBySortingInput)), graphql_name='sorting', default=None)),
))
    )
    '''Arguments:

    * `filter_settings` (`ObjectVersionFilterSettings`)None (default:
      `null`)
    * `limit` (`Int`)None (default: `null`)
    * `model_name` (`String`)None (default: `null`)
    * `offset` (`Int`)None (default: `null`)
    * `role` (`String!`)None
    * `sorting` (`[ObjectVersionSortBySortingInput!]`)None (default:
      `null`)
    '''

    pagination_available_models = sgqlc.types.Field(sgqlc.types.non_null('InlineObjectPagination'), graphql_name='paginationAvailableModels', args=sgqlc.types.ArgDict((
        ('filter_settings', sgqlc.types.Arg(ObjectFilterSettings, graphql_name='filterSettings', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('role', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='role', default=None)),
        ('sorting', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(ObjectSortBySortingInput)), graphql_name='sorting', default=None)),
))
    )
    '''Arguments:

    * `filter_settings` (`ObjectFilterSettings`)None (default: `null`)
    * `limit` (`Int`)None (default: `null`)
    * `offset` (`Int`)None (default: `null`)
    * `role` (`String!`)None
    * `sorting` (`[ObjectSortBySortingInput!]`)None (default: `null`)
    '''

    pagination_deployed_jobs = sgqlc.types.Field(sgqlc.types.non_null('JobPagination'), graphql_name='paginationDeployedJobs', args=sgqlc.types.ArgDict((
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
))
    )
    '''Arguments:

    * `limit` (`Int`)None (default: `null`)
    * `offset` (`Int`)None (default: `null`)
    '''

    source_path = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='sourcePath')

    tags = sgqlc.types.Field(sgqlc.types.non_null(JSON), graphql_name='tags')

    upload_model_modes = sgqlc.types.Field(sgqlc.types.non_null(JSON), graphql_name='uploadModelModes')

    version = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='version')



class ExecutorVersionPagination(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('list_executor_version', 'total')
    list_executor_version = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ExecutorVersionInfo))), graphql_name='listExecutorVersion')

    total = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='total')



class Experiment(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('description', 'experiment_id', 'list_job', 'list_model', 'list_model_version', 'name', 'pagination_job', 'pagination_model', 'pagination_model_version', 'tags')
    description = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='description')

    experiment_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='experimentId')

    list_job = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ExecutionJob))), graphql_name='listJob')

    list_model = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('ModelInfo'))), graphql_name='listModel')

    list_model_version = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('ModelVersionInfo'))), graphql_name='listModelVersion', args=sgqlc.types.ArgDict((
        ('model_name', sgqlc.types.Arg(String, graphql_name='modelName', default=None)),
))
    )
    '''Arguments:

    * `model_name` (`String`)None (default: `null`)
    '''

    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')

    pagination_job = sgqlc.types.Field(sgqlc.types.non_null('JobPagination'), graphql_name='paginationJob', args=sgqlc.types.ArgDict((
        ('filter_settings', sgqlc.types.Arg(JobFilterSettings, graphql_name='filterSettings', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('sorting', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(JobsSortBySortingInput)), graphql_name='sorting', default=None)),
))
    )
    '''Arguments:

    * `filter_settings` (`JobFilterSettings`)None (default: `null`)
    * `limit` (`Int`)None (default: `null`)
    * `offset` (`Int`)None (default: `null`)
    * `sorting` (`[JobsSortBySortingInput!]`)None (default: `null`)
    '''

    pagination_model = sgqlc.types.Field(sgqlc.types.non_null('ModelPagination'), graphql_name='paginationModel', args=sgqlc.types.ArgDict((
        ('filter_settings', sgqlc.types.Arg(ObjectFilterSettings, graphql_name='filterSettings', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('sorting', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(ObjectSortBySortingInput)), graphql_name='sorting', default=None)),
))
    )
    '''Arguments:

    * `filter_settings` (`ObjectFilterSettings`)None (default: `null`)
    * `limit` (`Int`)None (default: `null`)
    * `offset` (`Int`)None (default: `null`)
    * `sorting` (`[ObjectSortBySortingInput!]`)None (default: `null`)
    '''

    pagination_model_version = sgqlc.types.Field(sgqlc.types.non_null('ModelVersionPagination'), graphql_name='paginationModelVersion', args=sgqlc.types.ArgDict((
        ('filter_settings', sgqlc.types.Arg(ObjectVersionFilterSettings, graphql_name='filterSettings', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('model_name', sgqlc.types.Arg(String, graphql_name='modelName', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('sorting', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(ObjectVersionSortBySortingInput)), graphql_name='sorting', default=None)),
))
    )
    '''Arguments:

    * `filter_settings` (`ObjectVersionFilterSettings`)None (default:
      `null`)
    * `limit` (`Int`)None (default: `null`)
    * `model_name` (`String`)None (default: `null`)
    * `offset` (`Int`)None (default: `null`)
    * `sorting` (`[ObjectVersionSortBySortingInput!]`)None (default:
      `null`)
    '''

    tags = sgqlc.types.Field(sgqlc.types.non_null(JSON), graphql_name='tags')



class ExperimentPagination(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('list_experiment', 'total')
    list_experiment = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Experiment))), graphql_name='listExperiment')

    total = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='total')



class GraphNode(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('creation_timestamp', 'list_next_node', 'name', 'root_run_id', 'run_id', 'source_name', 'source_run_id', 'source_version', 'upload_model_type', 'version')
    creation_timestamp = sgqlc.types.Field(sgqlc.types.non_null(LONG), graphql_name='creationTimestamp')

    list_next_node = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('GraphNode')), graphql_name='listNextNode', args=sgqlc.types.ArgDict((
        ('sorting', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(ObjectVersionSortBySortingInput)), graphql_name='sorting', default=None)),
))
    )
    '''Arguments:

    * `sorting` (`[ObjectVersionSortBySortingInput!]`)None (default:
      `null`)
    '''

    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')

    root_run_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='rootRunId')

    run_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='runId')

    source_name = sgqlc.types.Field(String, graphql_name='sourceName')

    source_run_id = sgqlc.types.Field(ID, graphql_name='sourceRunId')

    source_version = sgqlc.types.Field(Int, graphql_name='sourceVersion')

    upload_model_type = sgqlc.types.Field(sgqlc.types.non_null(UploadModelType), graphql_name='uploadModelType')

    version = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='version')



class InlineObject(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('name',)
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')



class InlineObjectPagination(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('list_inline_object', 'total')
    list_inline_object = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(InlineObject))), graphql_name='listInlineObject')

    total = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='total')



class InlineObjectVersion(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('name', 'version')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')

    version = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='version')



class InlineObjectVersionPagination(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('list_inline_object_version', 'total')
    list_inline_object_version = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(InlineObjectVersion))), graphql_name='listInlineObjectVersion')

    total = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='total')



class JobDatasetLoadersSchema(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('list_role_dataset_loader_method_schemas',)
    list_role_dataset_loader_method_schemas = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('RoleMethodSchema'))), graphql_name='listRoleDatasetLoaderMethodSchemas')



class JobModelsSchema(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('list_role_model_method_schemas',)
    list_role_model_method_schemas = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('RoleMethodSchema'))), graphql_name='listRoleModelMethodSchemas')



class JobPagination(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('list_job', 'total')
    list_job = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ExecutionJob))), graphql_name='listJob')

    total = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='total')



class JobParams(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('additional_system_packages', 'cron_expression', 'executor_params', 'experiment_id', 'experiment_name', 'gpu', 'list_role_data_params', 'list_role_model_params', 'periodic_type')
    additional_system_packages = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='additionalSystemPackages')

    cron_expression = sgqlc.types.Field(String, graphql_name='cronExpression')

    executor_params = sgqlc.types.Field(sgqlc.types.non_null(ExecutorParams), graphql_name='executorParams')

    experiment_id = sgqlc.types.Field(Int, graphql_name='experimentId')

    experiment_name = sgqlc.types.Field(String, graphql_name='experimentName')

    gpu = sgqlc.types.Field(Boolean, graphql_name='gpu')

    list_role_data_params = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('RoleDataParams')), graphql_name='listRoleDataParams')

    list_role_model_params = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('RoleModelParams')), graphql_name='listRoleModelParams')

    periodic_type = sgqlc.types.Field(PeriodicType, graphql_name='periodicType')



class JobSchema(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('executor_method_schema', 'list_role_dataset_loader_method_schemas', 'list_role_model_method_schemas')
    executor_method_schema = sgqlc.types.Field(sgqlc.types.non_null('MethodSchema'), graphql_name='executorMethodSchema')

    list_role_dataset_loader_method_schemas = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('RoleMethodSchema'))), graphql_name='listRoleDatasetLoaderMethodSchemas')

    list_role_model_method_schemas = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('RoleMethodSchema'))), graphql_name='listRoleModelMethodSchemas')



class MethodParams(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('method_name', 'method_params')
    method_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='methodName')

    method_params = sgqlc.types.Field(sgqlc.types.non_null(JSON), graphql_name='methodParams')



class MethodSchema(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('json_schema', 'schema_name')
    json_schema = sgqlc.types.Field(sgqlc.types.non_null(JSON), graphql_name='jsonSchema')

    schema_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='schemaName')



class Metric(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('key', 'step', 'timestamp', 'value')
    key = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='key')

    step = sgqlc.types.Field(Int, graphql_name='step')

    timestamp = sgqlc.types.Field(sgqlc.types.non_null(LONG), graphql_name='timestamp')

    value = sgqlc.types.Field(Float, graphql_name='value')



class ModelInfo(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('creation_timestamp', 'description', 'init_model_version', 'last_updated_timestamp', 'latest_model_version', 'list_model_version', 'name', 'owner', 'pagination_model_version', 'tags')
    creation_timestamp = sgqlc.types.Field(sgqlc.types.non_null(LONG), graphql_name='creationTimestamp')

    description = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='description')

    init_model_version = sgqlc.types.Field(sgqlc.types.non_null('ModelVersionInfo'), graphql_name='initModelVersion')

    last_updated_timestamp = sgqlc.types.Field(sgqlc.types.non_null(LONG), graphql_name='lastUpdatedTimestamp')

    latest_model_version = sgqlc.types.Field(sgqlc.types.non_null('ModelVersionInfo'), graphql_name='latestModelVersion')

    list_model_version = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('ModelVersionInfo'))), graphql_name='listModelVersion', args=sgqlc.types.ArgDict((
        ('sorting', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(ObjectVersionSortBySortingInput)), graphql_name='sorting', default=None)),
))
    )
    '''Arguments:

    * `sorting` (`[ObjectVersionSortBySortingInput!]`)None (default:
      `null`)
    '''

    name = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='name')

    owner = sgqlc.types.Field(sgqlc.types.non_null('User'), graphql_name='owner')

    pagination_model_version = sgqlc.types.Field(sgqlc.types.non_null('ModelVersionPagination'), graphql_name='paginationModelVersion', args=sgqlc.types.ArgDict((
        ('filter_settings', sgqlc.types.Arg(ObjectVersionFilterSettings, graphql_name='filterSettings', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('sorting', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(ObjectVersionSortBySortingInput)), graphql_name='sorting', default=None)),
))
    )
    '''Arguments:

    * `filter_settings` (`ObjectVersionFilterSettings`)None (default:
      `null`)
    * `limit` (`Int`)None (default: `null`)
    * `offset` (`Int`)None (default: `null`)
    * `sorting` (`[ObjectVersionSortBySortingInput!]`)None (default:
      `null`)
    '''

    tags = sgqlc.types.Field(JSON, graphql_name='tags')



class ModelPagination(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('list_model', 'total')
    list_model = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ModelInfo))), graphql_name='listModel')

    total = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='total')



class ModelParams(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('description', 'list_model_method_params', 'model_version_choice', 'new_model_name', 'prepare_new_model_inference')
    description = sgqlc.types.Field(String, graphql_name='description')

    list_model_method_params = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(MethodParams))), graphql_name='listModelMethodParams')

    model_version_choice = sgqlc.types.Field(sgqlc.types.non_null('ModelVersionChoiceParams'), graphql_name='modelVersionChoice')

    new_model_name = sgqlc.types.Field(String, graphql_name='newModelName')

    prepare_new_model_inference = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='prepareNewModelInference')



class ModelVersionChoiceParams(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('choice_criteria', 'name', 'version')
    choice_criteria = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='choiceCriteria')

    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')

    version = sgqlc.types.Field(Int, graphql_name='version')



class ModelVersionInfo(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('available_collectors', 'available_dataset_loader_versions', 'available_dataset_loaders', 'available_executor_versions', 'available_executors', 'build_job', 'creation_timestamp', 'description', 'experiment', 'experiment_name', 'get_conda_env', 'group_job_run_id', 'last_updated_timestamp', 'list_artifacts', 'list_deployed_jobs', 'list_job', 'list_lineage_model_version', 'list_new_model_from_version', 'list_new_version_from_version', 'list_next_graph_nodes', 'list_next_model_version', 'list_requirements', 'model', 'model_method_schemas', 'name', 'pagination_available_collectors', 'pagination_available_dataset_loader_versions', 'pagination_available_dataset_loaders', 'pagination_available_executor_versions', 'pagination_available_executors', 'pagination_deployed_jobs', 'pagination_job', 'pagination_lineage_model_version', 'pagination_new_model_from_version', 'pagination_new_version_from_version', 'pagination_next_model_version', 'parent_job', 'root_model_version', 'source_executor_version', 'source_model_version', 'source_path', 'tags', 'upload_model_type', 'venv_build_job', 'version')
    available_collectors = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(InlineObject))), graphql_name='availableCollectors')

    available_dataset_loader_versions = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(InlineObjectVersion))), graphql_name='availableDatasetLoaderVersions', args=sgqlc.types.ArgDict((
        ('dataset_loader_name', sgqlc.types.Arg(String, graphql_name='datasetLoaderName', default=None)),
))
    )
    '''Arguments:

    * `dataset_loader_name` (`String`)None (default: `null`)
    '''

    available_dataset_loaders = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(InlineObject))), graphql_name='availableDatasetLoaders')

    available_executor_versions = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(InlineObjectVersion))), graphql_name='availableExecutorVersions', args=sgqlc.types.ArgDict((
        ('executor_name', sgqlc.types.Arg(String, graphql_name='executorName', default=None)),
))
    )
    '''Arguments:

    * `executor_name` (`String`)None (default: `null`)
    '''

    available_executors = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(InlineObject))), graphql_name='availableExecutors')

    build_job = sgqlc.types.Field(BuildJob, graphql_name='buildJob')

    creation_timestamp = sgqlc.types.Field(sgqlc.types.non_null(LONG), graphql_name='creationTimestamp')

    description = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='description')

    experiment = sgqlc.types.Field(sgqlc.types.non_null(Experiment), graphql_name='experiment')

    experiment_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='experimentName')

    get_conda_env = sgqlc.types.Field(sgqlc.types.non_null(JSON), graphql_name='getCondaEnv')

    group_job_run_id = sgqlc.types.Field(String, graphql_name='groupJobRunId')

    last_updated_timestamp = sgqlc.types.Field(LONG, graphql_name='lastUpdatedTimestamp')

    list_artifacts = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ArtifactPath))), graphql_name='listArtifacts', args=sgqlc.types.ArgDict((
        ('path', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='path', default='')),
))
    )
    '''Arguments:

    * `path` (`String!`)None (default: `""`)
    '''

    list_deployed_jobs = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ExecutionJob))), graphql_name='listDeployedJobs')

    list_job = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ExecutionJob))), graphql_name='listJob')

    list_lineage_model_version = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('ModelVersionInfo'))), graphql_name='listLineageModelVersion')

    list_new_model_from_version = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('ModelVersionInfo'))), graphql_name='listNewModelFromVersion', args=sgqlc.types.ArgDict((
        ('sorting', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(ObjectVersionSortBySortingInput)), graphql_name='sorting', default=None)),
))
    )
    '''Arguments:

    * `sorting` (`[ObjectVersionSortBySortingInput!]`)None (default:
      `null`)
    '''

    list_new_version_from_version = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('ModelVersionInfo'))), graphql_name='listNewVersionFromVersion', args=sgqlc.types.ArgDict((
        ('sorting', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(ObjectVersionSortBySortingInput)), graphql_name='sorting', default=None)),
))
    )
    '''Arguments:

    * `sorting` (`[ObjectVersionSortBySortingInput!]`)None (default:
      `null`)
    '''

    list_next_graph_nodes = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(GraphNode))), graphql_name='listNextGraphNodes', args=sgqlc.types.ArgDict((
        ('sorting', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(ObjectVersionSortBySortingInput)), graphql_name='sorting', default=None)),
))
    )
    '''Arguments:

    * `sorting` (`[ObjectVersionSortBySortingInput!]`)None (default:
      `null`)
    '''

    list_next_model_version = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('ModelVersionInfo'))), graphql_name='listNextModelVersion', args=sgqlc.types.ArgDict((
        ('sorting', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(ObjectVersionSortBySortingInput)), graphql_name='sorting', default=None)),
))
    )
    '''Arguments:

    * `sorting` (`[ObjectVersionSortBySortingInput!]`)None (default:
      `null`)
    '''

    list_requirements = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='listRequirements')

    model = sgqlc.types.Field(sgqlc.types.non_null(ModelInfo), graphql_name='model')

    model_method_schemas = sgqlc.types.Field(sgqlc.types.non_null(JSON), graphql_name='modelMethodSchemas')

    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')

    pagination_available_collectors = sgqlc.types.Field(sgqlc.types.non_null(InlineObjectPagination), graphql_name='paginationAvailableCollectors', args=sgqlc.types.ArgDict((
        ('filter_settings', sgqlc.types.Arg(ObjectFilterSettings, graphql_name='filterSettings', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
))
    )
    '''Arguments:

    * `filter_settings` (`ObjectFilterSettings`)None (default: `null`)
    * `limit` (`Int`)None (default: `null`)
    * `offset` (`Int`)None (default: `null`)
    '''

    pagination_available_dataset_loader_versions = sgqlc.types.Field(sgqlc.types.non_null(InlineObjectVersionPagination), graphql_name='paginationAvailableDatasetLoaderVersions', args=sgqlc.types.ArgDict((
        ('dataset_loader_name', sgqlc.types.Arg(String, graphql_name='datasetLoaderName', default=None)),
        ('filter_settings', sgqlc.types.Arg(ObjectVersionFilterSettings, graphql_name='filterSettings', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('sorting', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(ObjectVersionSortBySortingInput)), graphql_name='sorting', default=None)),
))
    )
    '''Arguments:

    * `dataset_loader_name` (`String`)None (default: `null`)
    * `filter_settings` (`ObjectVersionFilterSettings`)None (default:
      `null`)
    * `limit` (`Int`)None (default: `null`)
    * `offset` (`Int`)None (default: `null`)
    * `sorting` (`[ObjectVersionSortBySortingInput!]`)None (default:
      `null`)
    '''

    pagination_available_dataset_loaders = sgqlc.types.Field(sgqlc.types.non_null(InlineObjectPagination), graphql_name='paginationAvailableDatasetLoaders', args=sgqlc.types.ArgDict((
        ('filter_settings', sgqlc.types.Arg(ObjectFilterSettings, graphql_name='filterSettings', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('sorting', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(ObjectSortBySortingInput)), graphql_name='sorting', default=None)),
))
    )
    '''Arguments:

    * `filter_settings` (`ObjectFilterSettings`)None (default: `null`)
    * `limit` (`Int`)None (default: `null`)
    * `offset` (`Int`)None (default: `null`)
    * `sorting` (`[ObjectSortBySortingInput!]`)None (default: `null`)
    '''

    pagination_available_executor_versions = sgqlc.types.Field(sgqlc.types.non_null(InlineObjectVersionPagination), graphql_name='paginationAvailableExecutorVersions', args=sgqlc.types.ArgDict((
        ('executor_name', sgqlc.types.Arg(String, graphql_name='executorName', default=None)),
        ('filter_settings', sgqlc.types.Arg(ObjectVersionFilterSettings, graphql_name='filterSettings', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('sorting', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(ObjectVersionSortBySortingInput)), graphql_name='sorting', default=None)),
))
    )
    '''Arguments:

    * `executor_name` (`String`)None (default: `null`)
    * `filter_settings` (`ObjectVersionFilterSettings`)None (default:
      `null`)
    * `limit` (`Int`)None (default: `null`)
    * `offset` (`Int`)None (default: `null`)
    * `sorting` (`[ObjectVersionSortBySortingInput!]`)None (default:
      `null`)
    '''

    pagination_available_executors = sgqlc.types.Field(sgqlc.types.non_null(InlineObjectPagination), graphql_name='paginationAvailableExecutors', args=sgqlc.types.ArgDict((
        ('filter_settings', sgqlc.types.Arg(ObjectFilterSettings, graphql_name='filterSettings', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('sorting', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(ObjectSortBySortingInput)), graphql_name='sorting', default=None)),
))
    )
    '''Arguments:

    * `filter_settings` (`ObjectFilterSettings`)None (default: `null`)
    * `limit` (`Int`)None (default: `null`)
    * `offset` (`Int`)None (default: `null`)
    * `sorting` (`[ObjectSortBySortingInput!]`)None (default: `null`)
    '''

    pagination_deployed_jobs = sgqlc.types.Field(sgqlc.types.non_null(JobPagination), graphql_name='paginationDeployedJobs', args=sgqlc.types.ArgDict((
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
))
    )
    '''Arguments:

    * `limit` (`Int`)None (default: `null`)
    * `offset` (`Int`)None (default: `null`)
    '''

    pagination_job = sgqlc.types.Field(sgqlc.types.non_null(JobPagination), graphql_name='paginationJob', args=sgqlc.types.ArgDict((
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
))
    )
    '''Arguments:

    * `limit` (`Int`)None (default: `null`)
    * `offset` (`Int`)None (default: `null`)
    '''

    pagination_lineage_model_version = sgqlc.types.Field(sgqlc.types.non_null('ModelVersionPagination'), graphql_name='paginationLineageModelVersion', args=sgqlc.types.ArgDict((
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
))
    )
    '''Arguments:

    * `limit` (`Int`)None (default: `null`)
    * `offset` (`Int`)None (default: `null`)
    '''

    pagination_new_model_from_version = sgqlc.types.Field(sgqlc.types.non_null('ModelVersionPagination'), graphql_name='paginationNewModelFromVersion', args=sgqlc.types.ArgDict((
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('sorting', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(ObjectVersionSortBySortingInput)), graphql_name='sorting', default=None)),
))
    )
    '''Arguments:

    * `limit` (`Int`)None (default: `null`)
    * `offset` (`Int`)None (default: `null`)
    * `sorting` (`[ObjectVersionSortBySortingInput!]`)None (default:
      `null`)
    '''

    pagination_new_version_from_version = sgqlc.types.Field(sgqlc.types.non_null('ModelVersionPagination'), graphql_name='paginationNewVersionFromVersion', args=sgqlc.types.ArgDict((
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('sorting', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(ObjectVersionSortBySortingInput)), graphql_name='sorting', default=None)),
))
    )
    '''Arguments:

    * `limit` (`Int`)None (default: `null`)
    * `offset` (`Int`)None (default: `null`)
    * `sorting` (`[ObjectVersionSortBySortingInput!]`)None (default:
      `null`)
    '''

    pagination_next_model_version = sgqlc.types.Field(sgqlc.types.non_null('ModelVersionPagination'), graphql_name='paginationNextModelVersion', args=sgqlc.types.ArgDict((
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('sorting', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(ObjectVersionSortBySortingInput)), graphql_name='sorting', default=None)),
))
    )
    '''Arguments:

    * `limit` (`Int`)None (default: `null`)
    * `offset` (`Int`)None (default: `null`)
    * `sorting` (`[ObjectVersionSortBySortingInput!]`)None (default:
      `null`)
    '''

    parent_job = sgqlc.types.Field(ExecutionJob, graphql_name='parentJob')

    root_model_version = sgqlc.types.Field(sgqlc.types.non_null('ModelVersionInfo'), graphql_name='rootModelVersion')

    source_executor_version = sgqlc.types.Field(ExecutorVersionInfo, graphql_name='sourceExecutorVersion')

    source_model_version = sgqlc.types.Field('ModelVersionInfo', graphql_name='sourceModelVersion')

    source_path = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='sourcePath')

    tags = sgqlc.types.Field(sgqlc.types.non_null(JSON), graphql_name='tags')

    upload_model_type = sgqlc.types.Field(sgqlc.types.non_null(UploadModelType), graphql_name='uploadModelType')

    venv_build_job = sgqlc.types.Field(BuildJob, graphql_name='venvBuildJob')

    version = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='version')



class ModelVersionPagination(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('list_model_version', 'total')
    list_model_version = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ModelVersionInfo))), graphql_name='listModelVersion')

    total = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='total')



class Mutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('add_ml_job', 'cancel_build_job_for_executor_version', 'cancel_build_job_for_model_version', 'cancel_job', 'cancel_venv_build_job_for_model_version', 'delete_dataset_loader', 'delete_dataset_loader_tag', 'delete_dataset_loader_version_from_name_version', 'delete_dataset_loader_version_tag', 'delete_executor', 'delete_executor_tag', 'delete_executor_version_from_name_version', 'delete_executor_version_tag', 'delete_experiment_tag', 'delete_model', 'delete_model_tag', 'delete_model_version_from_name_version', 'delete_model_version_tag', 'log_metric', 'log_metrics', 'log_param', 'log_params', 'rebuild_model_version_image', 'rebuild_no_model_executor_version_image', 'rename_experiment', 'serve_model', 'set_dataset_loader_description', 'set_dataset_loader_tag', 'set_dataset_loader_version_description', 'set_dataset_loader_version_tag', 'set_executor_description', 'set_executor_tag', 'set_executor_version_description', 'set_executor_version_tag', 'set_experiment_description', 'set_experiment_tag', 'set_model_description', 'set_model_tag', 'set_model_version_description', 'set_model_version_tag', 'stop_model_serving', 'update_experiment')
    add_ml_job = sgqlc.types.Field(sgqlc.types.non_null(ExecutionJob), graphql_name='addMlJob', args=sgqlc.types.ArgDict((
        ('form', sgqlc.types.Arg(sgqlc.types.non_null(JobParameters), graphql_name='form', default=None)),
))
    )
    '''Arguments:

    * `form` (`JobParameters!`)None
    '''

    cancel_build_job_for_executor_version = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='cancelBuildJobForExecutorVersion', args=sgqlc.types.ArgDict((
        ('name', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='name', default=None)),
        ('version', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='version', default=None)),
))
    )
    '''Arguments:

    * `name` (`String!`)None
    * `version` (`Int!`)None
    '''

    cancel_build_job_for_model_version = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='cancelBuildJobForModelVersion', args=sgqlc.types.ArgDict((
        ('name', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='name', default=None)),
        ('version', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='version', default=None)),
))
    )
    '''Arguments:

    * `name` (`String!`)None
    * `version` (`Int!`)None
    '''

    cancel_job = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='cancelJob', args=sgqlc.types.ArgDict((
        ('job_name', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='jobName', default=None)),
))
    )
    '''Arguments:

    * `job_name` (`String!`)None
    '''

    cancel_venv_build_job_for_model_version = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='cancelVenvBuildJobForModelVersion', args=sgqlc.types.ArgDict((
        ('name', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='name', default=None)),
        ('version', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='version', default=None)),
))
    )
    '''Arguments:

    * `name` (`String!`)None
    * `version` (`Int!`)None
    '''

    delete_dataset_loader = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='deleteDatasetLoader', args=sgqlc.types.ArgDict((
        ('name', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='name', default=None)),
))
    )
    '''Arguments:

    * `name` (`String!`)None
    '''

    delete_dataset_loader_tag = sgqlc.types.Field(sgqlc.types.non_null(DatasetLoaderInfo), graphql_name='deleteDatasetLoaderTag', args=sgqlc.types.ArgDict((
        ('key', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='key', default=None)),
        ('name', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='name', default=None)),
))
    )
    '''Arguments:

    * `key` (`String!`)None
    * `name` (`String!`)None
    '''

    delete_dataset_loader_version_from_name_version = sgqlc.types.Field(Boolean, graphql_name='deleteDatasetLoaderVersionFromNameVersion', args=sgqlc.types.ArgDict((
        ('dataset_loader_version', sgqlc.types.Arg(sgqlc.types.non_null(ObjectVersionInput), graphql_name='datasetLoaderVersion', default=None)),
))
    )
    '''Arguments:

    * `dataset_loader_version` (`ObjectVersionInput!`)None
    '''

    delete_dataset_loader_version_tag = sgqlc.types.Field(sgqlc.types.non_null(DatasetLoaderVersionInfo), graphql_name='deleteDatasetLoaderVersionTag', args=sgqlc.types.ArgDict((
        ('dataset_loader_version', sgqlc.types.Arg(sgqlc.types.non_null(ObjectVersionInput), graphql_name='datasetLoaderVersion', default=None)),
        ('key', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='key', default=None)),
))
    )
    '''Arguments:

    * `dataset_loader_version` (`ObjectVersionInput!`)None
    * `key` (`String!`)None
    '''

    delete_executor = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='deleteExecutor', args=sgqlc.types.ArgDict((
        ('name', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='name', default=None)),
))
    )
    '''Arguments:

    * `name` (`String!`)None
    '''

    delete_executor_tag = sgqlc.types.Field(sgqlc.types.non_null(ExecutorInfo), graphql_name='deleteExecutorTag', args=sgqlc.types.ArgDict((
        ('key', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='key', default=None)),
        ('name', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='name', default=None)),
))
    )
    '''Arguments:

    * `key` (`String!`)None
    * `name` (`String!`)None
    '''

    delete_executor_version_from_name_version = sgqlc.types.Field(Boolean, graphql_name='deleteExecutorVersionFromNameVersion', args=sgqlc.types.ArgDict((
        ('executor_version', sgqlc.types.Arg(sgqlc.types.non_null(ObjectVersionInput), graphql_name='executorVersion', default=None)),
))
    )
    '''Arguments:

    * `executor_version` (`ObjectVersionInput!`)None
    '''

    delete_executor_version_tag = sgqlc.types.Field(sgqlc.types.non_null(ExecutorVersionInfo), graphql_name='deleteExecutorVersionTag', args=sgqlc.types.ArgDict((
        ('executor_version', sgqlc.types.Arg(sgqlc.types.non_null(ObjectVersionInput), graphql_name='executorVersion', default=None)),
        ('key', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='key', default=None)),
))
    )
    '''Arguments:

    * `executor_version` (`ObjectVersionInput!`)None
    * `key` (`String!`)None
    '''

    delete_experiment_tag = sgqlc.types.Field(sgqlc.types.non_null(Experiment), graphql_name='deleteExperimentTag', args=sgqlc.types.ArgDict((
        ('experiment_id', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='experimentId', default=None)),
        ('key', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='key', default=None)),
))
    )
    '''Arguments:

    * `experiment_id` (`Int!`)None
    * `key` (`String!`)None
    '''

    delete_model = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='deleteModel', args=sgqlc.types.ArgDict((
        ('name', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='name', default=None)),
))
    )
    '''Arguments:

    * `name` (`String!`)None
    '''

    delete_model_tag = sgqlc.types.Field(sgqlc.types.non_null(ModelInfo), graphql_name='deleteModelTag', args=sgqlc.types.ArgDict((
        ('key', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='key', default=None)),
        ('name', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='name', default=None)),
))
    )
    '''Arguments:

    * `key` (`String!`)None
    * `name` (`String!`)None
    '''

    delete_model_version_from_name_version = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='deleteModelVersionFromNameVersion', args=sgqlc.types.ArgDict((
        ('model_version', sgqlc.types.Arg(sgqlc.types.non_null(ObjectVersionInput), graphql_name='modelVersion', default=None)),
))
    )
    '''Arguments:

    * `model_version` (`ObjectVersionInput!`)None
    '''

    delete_model_version_tag = sgqlc.types.Field(sgqlc.types.non_null(ModelVersionInfo), graphql_name='deleteModelVersionTag', args=sgqlc.types.ArgDict((
        ('key', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='key', default=None)),
        ('model_version', sgqlc.types.Arg(sgqlc.types.non_null(ObjectVersionInput), graphql_name='modelVersion', default=None)),
))
    )
    '''Arguments:

    * `key` (`String!`)None
    * `model_version` (`ObjectVersionInput!`)None
    '''

    log_metric = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='logMetric', args=sgqlc.types.ArgDict((
        ('job_run_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='jobRunId', default=None)),
        ('metric', sgqlc.types.Arg(sgqlc.types.non_null(MetricInput), graphql_name='metric', default=None)),
))
    )
    '''Arguments:

    * `job_run_id` (`String!`)None
    * `metric` (`MetricInput!`)None
    '''

    log_metrics = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='logMetrics', args=sgqlc.types.ArgDict((
        ('job_run_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='jobRunId', default=None)),
        ('metrics', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(MetricInput))), graphql_name='metrics', default=None)),
))
    )
    '''Arguments:

    * `job_run_id` (`String!`)None
    * `metrics` (`[MetricInput!]!`)None
    '''

    log_param = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='logParam', args=sgqlc.types.ArgDict((
        ('job_run_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='jobRunId', default=None)),
        ('param', sgqlc.types.Arg(sgqlc.types.non_null(ParamInput), graphql_name='param', default=None)),
))
    )
    '''Arguments:

    * `job_run_id` (`String!`)None
    * `param` (`ParamInput!`)None
    '''

    log_params = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='logParams', args=sgqlc.types.ArgDict((
        ('job_run_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='jobRunId', default=None)),
        ('params', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ParamInput))), graphql_name='params', default=None)),
))
    )
    '''Arguments:

    * `job_run_id` (`String!`)None
    * `params` (`[ParamInput!]!`)None
    '''

    rebuild_model_version_image = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='rebuildModelVersionImage', args=sgqlc.types.ArgDict((
        ('model_version', sgqlc.types.Arg(sgqlc.types.non_null(ObjectVersionInput), graphql_name='modelVersion', default=None)),
))
    )
    '''Arguments:

    * `model_version` (`ObjectVersionInput!`)None
    '''

    rebuild_no_model_executor_version_image = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='rebuildNoModelExecutorVersionImage', args=sgqlc.types.ArgDict((
        ('executor_version', sgqlc.types.Arg(sgqlc.types.non_null(ObjectVersionInput), graphql_name='executorVersion', default=None)),
))
    )
    '''Arguments:

    * `executor_version` (`ObjectVersionInput!`)None
    '''

    rename_experiment = sgqlc.types.Field(sgqlc.types.non_null(Experiment), graphql_name='renameExperiment', args=sgqlc.types.ArgDict((
        ('experiment_id', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='experimentId', default=None)),
        ('new_name', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='newName', default=None)),
))
    )
    '''Arguments:

    * `experiment_id` (`Int!`)None
    * `new_name` (`String!`)None
    '''

    serve_model = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='serveModel', args=sgqlc.types.ArgDict((
        ('serving_parameters', sgqlc.types.Arg(sgqlc.types.non_null(ModelServingInput), graphql_name='servingParameters', default=None)),
))
    )
    '''Arguments:

    * `serving_parameters` (`ModelServingInput!`)None
    '''

    set_dataset_loader_description = sgqlc.types.Field(sgqlc.types.non_null(DatasetLoaderInfo), graphql_name='setDatasetLoaderDescription', args=sgqlc.types.ArgDict((
        ('description', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='description', default=None)),
        ('name', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='name', default=None)),
))
    )
    '''Arguments:

    * `description` (`String!`)None
    * `name` (`String!`)None
    '''

    set_dataset_loader_tag = sgqlc.types.Field(sgqlc.types.non_null(DatasetLoaderInfo), graphql_name='setDatasetLoaderTag', args=sgqlc.types.ArgDict((
        ('key', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='key', default=None)),
        ('name', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='name', default=None)),
        ('value', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='value', default=None)),
))
    )
    '''Arguments:

    * `key` (`String!`)None
    * `name` (`String!`)None
    * `value` (`String!`)None
    '''

    set_dataset_loader_version_description = sgqlc.types.Field(sgqlc.types.non_null(DatasetLoaderVersionInfo), graphql_name='setDatasetLoaderVersionDescription', args=sgqlc.types.ArgDict((
        ('dataset_loader_version', sgqlc.types.Arg(sgqlc.types.non_null(ObjectVersionInput), graphql_name='datasetLoaderVersion', default=None)),
        ('description', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='description', default=None)),
))
    )
    '''Arguments:

    * `dataset_loader_version` (`ObjectVersionInput!`)None
    * `description` (`String!`)None
    '''

    set_dataset_loader_version_tag = sgqlc.types.Field(sgqlc.types.non_null(DatasetLoaderVersionInfo), graphql_name='setDatasetLoaderVersionTag', args=sgqlc.types.ArgDict((
        ('dataset_loader_version', sgqlc.types.Arg(sgqlc.types.non_null(ObjectVersionInput), graphql_name='datasetLoaderVersion', default=None)),
        ('key', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='key', default=None)),
        ('value', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='value', default=None)),
))
    )
    '''Arguments:

    * `dataset_loader_version` (`ObjectVersionInput!`)None
    * `key` (`String!`)None
    * `value` (`String!`)None
    '''

    set_executor_description = sgqlc.types.Field(sgqlc.types.non_null(ExecutorInfo), graphql_name='setExecutorDescription', args=sgqlc.types.ArgDict((
        ('description', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='description', default=None)),
        ('name', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='name', default=None)),
))
    )
    '''Arguments:

    * `description` (`String!`)None
    * `name` (`String!`)None
    '''

    set_executor_tag = sgqlc.types.Field(sgqlc.types.non_null(ExecutorInfo), graphql_name='setExecutorTag', args=sgqlc.types.ArgDict((
        ('key', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='key', default=None)),
        ('name', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='name', default=None)),
        ('value', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='value', default=None)),
))
    )
    '''Arguments:

    * `key` (`String!`)None
    * `name` (`String!`)None
    * `value` (`String!`)None
    '''

    set_executor_version_description = sgqlc.types.Field(sgqlc.types.non_null(ExecutorVersionInfo), graphql_name='setExecutorVersionDescription', args=sgqlc.types.ArgDict((
        ('description', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='description', default=None)),
        ('executor_version', sgqlc.types.Arg(sgqlc.types.non_null(ObjectVersionInput), graphql_name='executorVersion', default=None)),
))
    )
    '''Arguments:

    * `description` (`String!`)None
    * `executor_version` (`ObjectVersionInput!`)None
    '''

    set_executor_version_tag = sgqlc.types.Field(sgqlc.types.non_null(ExecutorVersionInfo), graphql_name='setExecutorVersionTag', args=sgqlc.types.ArgDict((
        ('executor_version', sgqlc.types.Arg(sgqlc.types.non_null(ObjectVersionInput), graphql_name='executorVersion', default=None)),
        ('key', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='key', default=None)),
        ('value', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='value', default=None)),
))
    )
    '''Arguments:

    * `executor_version` (`ObjectVersionInput!`)None
    * `key` (`String!`)None
    * `value` (`String!`)None
    '''

    set_experiment_description = sgqlc.types.Field(sgqlc.types.non_null(Experiment), graphql_name='setExperimentDescription', args=sgqlc.types.ArgDict((
        ('description', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='description', default=None)),
        ('experiment_id', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='experimentId', default=None)),
))
    )
    '''Arguments:

    * `description` (`String!`)None
    * `experiment_id` (`Int!`)None
    '''

    set_experiment_tag = sgqlc.types.Field(sgqlc.types.non_null(Experiment), graphql_name='setExperimentTag', args=sgqlc.types.ArgDict((
        ('experiment_id', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='experimentId', default=None)),
        ('key', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='key', default=None)),
        ('value', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='value', default=None)),
))
    )
    '''Arguments:

    * `experiment_id` (`Int!`)None
    * `key` (`String!`)None
    * `value` (`String!`)None
    '''

    set_model_description = sgqlc.types.Field(sgqlc.types.non_null(ModelInfo), graphql_name='setModelDescription', args=sgqlc.types.ArgDict((
        ('description', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='description', default=None)),
        ('name', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='name', default=None)),
))
    )
    '''Arguments:

    * `description` (`String!`)None
    * `name` (`String!`)None
    '''

    set_model_tag = sgqlc.types.Field(sgqlc.types.non_null(ModelInfo), graphql_name='setModelTag', args=sgqlc.types.ArgDict((
        ('key', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='key', default=None)),
        ('name', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='name', default=None)),
        ('value', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='value', default=None)),
))
    )
    '''Arguments:

    * `key` (`String!`)None
    * `name` (`String!`)None
    * `value` (`String!`)None
    '''

    set_model_version_description = sgqlc.types.Field(sgqlc.types.non_null(ModelVersionInfo), graphql_name='setModelVersionDescription', args=sgqlc.types.ArgDict((
        ('description', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='description', default=None)),
        ('model_version', sgqlc.types.Arg(sgqlc.types.non_null(ObjectVersionInput), graphql_name='modelVersion', default=None)),
))
    )
    '''Arguments:

    * `description` (`String!`)None
    * `model_version` (`ObjectVersionInput!`)None
    '''

    set_model_version_tag = sgqlc.types.Field(sgqlc.types.non_null(ModelVersionInfo), graphql_name='setModelVersionTag', args=sgqlc.types.ArgDict((
        ('key', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='key', default=None)),
        ('model_version', sgqlc.types.Arg(sgqlc.types.non_null(ObjectVersionInput), graphql_name='modelVersion', default=None)),
        ('value', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='value', default=None)),
))
    )
    '''Arguments:

    * `key` (`String!`)None
    * `model_version` (`ObjectVersionInput!`)None
    * `value` (`String!`)None
    '''

    stop_model_serving = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='stopModelServing', args=sgqlc.types.ArgDict((
        ('model_version', sgqlc.types.Arg(sgqlc.types.non_null(ObjectVersionInput), graphql_name='modelVersion', default=None)),
))
    )
    '''Arguments:

    * `model_version` (`ObjectVersionInput!`)None
    '''

    update_experiment = sgqlc.types.Field(sgqlc.types.non_null(Experiment), graphql_name='updateExperiment', args=sgqlc.types.ArgDict((
        ('experiment_id', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='experimentId', default=None)),
        ('update_experiment_form', sgqlc.types.Arg(sgqlc.types.non_null(UpdateExperimentForm), graphql_name='updateExperimentForm', default=None)),
))
    )
    '''Arguments:

    * `experiment_id` (`Int!`)None
    * `update_experiment_form` (`UpdateExperimentForm!`)None
    '''



class ObjectVersion(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('name', 'version')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')

    version = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='version')



class Param(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('key', 'value')
    key = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='key')

    value = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='value')



class Query(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('dataset_loader_from_name', 'dataset_loader_version_from_name_version', 'dataset_loader_version_from_run_id', 'executor_from_name', 'executor_version_from_name_version', 'executor_version_from_run_id', 'experiment_from_id', 'experiment_from_name', 'graph_node', 'is_inference_model_ready', 'job_from_name', 'list_build_job', 'list_dataset_loader', 'list_executor', 'list_experiment', 'list_graph_node', 'list_initial_executor_version', 'list_initial_model_version', 'list_job', 'list_model', 'list_subtree_graph_node', 'model_from_name', 'model_version_from_name_version', 'model_version_from_run_id', 'pagination_dataset_loader', 'pagination_executor', 'pagination_experiment', 'pagination_initial_executor_version', 'pagination_initial_model_version', 'pagination_job', 'pagination_model', 'warning_delete_model_query')
    dataset_loader_from_name = sgqlc.types.Field(sgqlc.types.non_null(DatasetLoaderInfo), graphql_name='datasetLoaderFromName', args=sgqlc.types.ArgDict((
        ('name', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='name', default=None)),
))
    )
    '''Arguments:

    * `name` (`String!`)None
    '''

    dataset_loader_version_from_name_version = sgqlc.types.Field(sgqlc.types.non_null(DatasetLoaderVersionInfo), graphql_name='datasetLoaderVersionFromNameVersion', args=sgqlc.types.ArgDict((
        ('dataset_loader_version', sgqlc.types.Arg(sgqlc.types.non_null(ObjectVersionOptionalInput), graphql_name='datasetLoaderVersion', default=None)),
))
    )
    '''Arguments:

    * `dataset_loader_version` (`ObjectVersionOptionalInput!`)None
    '''

    dataset_loader_version_from_run_id = sgqlc.types.Field(sgqlc.types.non_null(DatasetLoaderVersionInfo), graphql_name='datasetLoaderVersionFromRunId', args=sgqlc.types.ArgDict((
        ('run_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='runId', default=None)),
))
    )
    '''Arguments:

    * `run_id` (`String!`)None
    '''

    executor_from_name = sgqlc.types.Field(sgqlc.types.non_null(ExecutorInfo), graphql_name='executorFromName', args=sgqlc.types.ArgDict((
        ('name', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='name', default=None)),
))
    )
    '''Arguments:

    * `name` (`String!`)None
    '''

    executor_version_from_name_version = sgqlc.types.Field(sgqlc.types.non_null(ExecutorVersionInfo), graphql_name='executorVersionFromNameVersion', args=sgqlc.types.ArgDict((
        ('executor_version', sgqlc.types.Arg(sgqlc.types.non_null(ObjectVersionOptionalInput), graphql_name='executorVersion', default=None)),
))
    )
    '''Arguments:

    * `executor_version` (`ObjectVersionOptionalInput!`)None
    '''

    executor_version_from_run_id = sgqlc.types.Field(sgqlc.types.non_null(ExecutorVersionInfo), graphql_name='executorVersionFromRunId', args=sgqlc.types.ArgDict((
        ('run_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='runId', default=None)),
))
    )
    '''Arguments:

    * `run_id` (`String!`)None
    '''

    experiment_from_id = sgqlc.types.Field(sgqlc.types.non_null(Experiment), graphql_name='experimentFromId', args=sgqlc.types.ArgDict((
        ('experiment_id', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='experimentId', default=None)),
))
    )
    '''Arguments:

    * `experiment_id` (`Int!`)None
    '''

    experiment_from_name = sgqlc.types.Field(sgqlc.types.non_null(Experiment), graphql_name='experimentFromName', args=sgqlc.types.ArgDict((
        ('name', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='name', default=None)),
))
    )
    '''Arguments:

    * `name` (`String!`)None
    '''

    graph_node = sgqlc.types.Field(sgqlc.types.non_null(GraphNode), graphql_name='graphNode', args=sgqlc.types.ArgDict((
        ('run_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='runId', default=None)),
))
    )
    '''Arguments:

    * `run_id` (`String!`)None
    '''

    is_inference_model_ready = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='isInferenceModelReady', args=sgqlc.types.ArgDict((
        ('model_version', sgqlc.types.Arg(sgqlc.types.non_null(ObjectVersionInput), graphql_name='modelVersion', default=None)),
))
    )
    '''Arguments:

    * `model_version` (`ObjectVersionInput!`)None
    '''

    job_from_name = sgqlc.types.Field(sgqlc.types.non_null(ExecutionJob), graphql_name='jobFromName', args=sgqlc.types.ArgDict((
        ('name', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='name', default=None)),
))
    )
    '''Arguments:

    * `name` (`String!`)None
    '''

    list_build_job = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(BuildJob))), graphql_name='listBuildJob', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Int))), graphql_name='ids', default=None)),
))
    )
    '''Arguments:

    * `ids` (`[Int!]!`)None
    '''

    list_dataset_loader = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(DatasetLoaderInfo))), graphql_name='listDatasetLoader', args=sgqlc.types.ArgDict((
        ('sorting', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(ObjectSortBySortingInput)), graphql_name='sorting', default=None)),
))
    )
    '''Arguments:

    * `sorting` (`[ObjectSortBySortingInput!]`)None (default: `null`)
    '''

    list_executor = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ExecutorInfo))), graphql_name='listExecutor', args=sgqlc.types.ArgDict((
        ('sorting', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(ObjectSortBySortingInput)), graphql_name='sorting', default=None)),
))
    )
    '''Arguments:

    * `sorting` (`[ObjectSortBySortingInput!]`)None (default: `null`)
    '''

    list_experiment = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Experiment))), graphql_name='listExperiment')

    list_graph_node = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(GraphNode))), graphql_name='listGraphNode')

    list_initial_executor_version = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ExecutorVersionInfo))), graphql_name='listInitialExecutorVersion')

    list_initial_model_version = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ModelVersionInfo))), graphql_name='listInitialModelVersion')

    list_job = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ExecutionJob))), graphql_name='listJob')

    list_model = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ModelInfo))), graphql_name='listModel', args=sgqlc.types.ArgDict((
        ('sorting', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(ObjectSortBySortingInput)), graphql_name='sorting', default=None)),
))
    )
    '''Arguments:

    * `sorting` (`[ObjectSortBySortingInput!]`)None (default: `null`)
    '''

    list_subtree_graph_node = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(GraphNode))), graphql_name='listSubtreeGraphNode', args=sgqlc.types.ArgDict((
        ('root_run_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='rootRunId', default=None)),
))
    )
    '''Arguments:

    * `root_run_id` (`String!`)None
    '''

    model_from_name = sgqlc.types.Field(sgqlc.types.non_null(ModelInfo), graphql_name='modelFromName', args=sgqlc.types.ArgDict((
        ('name', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='name', default=None)),
))
    )
    '''Arguments:

    * `name` (`String!`)None
    '''

    model_version_from_name_version = sgqlc.types.Field(sgqlc.types.non_null(ModelVersionInfo), graphql_name='modelVersionFromNameVersion', args=sgqlc.types.ArgDict((
        ('model_version', sgqlc.types.Arg(sgqlc.types.non_null(ObjectVersionOptionalInput), graphql_name='modelVersion', default=None)),
))
    )
    '''Arguments:

    * `model_version` (`ObjectVersionOptionalInput!`)None
    '''

    model_version_from_run_id = sgqlc.types.Field(sgqlc.types.non_null(ModelVersionInfo), graphql_name='modelVersionFromRunId', args=sgqlc.types.ArgDict((
        ('run_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='runId', default=None)),
))
    )
    '''Arguments:

    * `run_id` (`String!`)None
    '''

    pagination_dataset_loader = sgqlc.types.Field(sgqlc.types.non_null(DatasetLoaderPagination), graphql_name='paginationDatasetLoader', args=sgqlc.types.ArgDict((
        ('filter_settings', sgqlc.types.Arg(ObjectFilterSettings, graphql_name='filterSettings', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('sorting', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(ObjectSortBySortingInput)), graphql_name='sorting', default=None)),
))
    )
    '''Arguments:

    * `filter_settings` (`ObjectFilterSettings`)None (default: `null`)
    * `limit` (`Int`)None (default: `null`)
    * `offset` (`Int`)None (default: `null`)
    * `sorting` (`[ObjectSortBySortingInput!]`)None (default: `null`)
    '''

    pagination_executor = sgqlc.types.Field(sgqlc.types.non_null(ExecutorPagination), graphql_name='paginationExecutor', args=sgqlc.types.ArgDict((
        ('filter_settings', sgqlc.types.Arg(ObjectFilterSettings, graphql_name='filterSettings', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('sorting', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(ObjectSortBySortingInput)), graphql_name='sorting', default=None)),
))
    )
    '''Arguments:

    * `filter_settings` (`ObjectFilterSettings`)None (default: `null`)
    * `limit` (`Int`)None (default: `null`)
    * `offset` (`Int`)None (default: `null`)
    * `sorting` (`[ObjectSortBySortingInput!]`)None (default: `null`)
    '''

    pagination_experiment = sgqlc.types.Field(sgqlc.types.non_null(ExperimentPagination), graphql_name='paginationExperiment', args=sgqlc.types.ArgDict((
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
))
    )
    '''Arguments:

    * `limit` (`Int`)None (default: `null`)
    * `offset` (`Int`)None (default: `null`)
    '''

    pagination_initial_executor_version = sgqlc.types.Field(sgqlc.types.non_null(ExecutorVersionPagination), graphql_name='paginationInitialExecutorVersion', args=sgqlc.types.ArgDict((
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
))
    )
    '''Arguments:

    * `limit` (`Int`)None (default: `null`)
    * `offset` (`Int`)None (default: `null`)
    '''

    pagination_initial_model_version = sgqlc.types.Field(sgqlc.types.non_null(ModelVersionPagination), graphql_name='paginationInitialModelVersion', args=sgqlc.types.ArgDict((
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
))
    )
    '''Arguments:

    * `limit` (`Int`)None (default: `null`)
    * `offset` (`Int`)None (default: `null`)
    '''

    pagination_job = sgqlc.types.Field(sgqlc.types.non_null(JobPagination), graphql_name='paginationJob', args=sgqlc.types.ArgDict((
        ('filter_settings', sgqlc.types.Arg(JobFilterSettings, graphql_name='filterSettings', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('sorting', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(JobsSortBySortingInput)), graphql_name='sorting', default=None)),
))
    )
    '''Arguments:

    * `filter_settings` (`JobFilterSettings`)None (default: `null`)
    * `limit` (`Int`)None (default: `null`)
    * `offset` (`Int`)None (default: `null`)
    * `sorting` (`[JobsSortBySortingInput!]`)None (default: `null`)
    '''

    pagination_model = sgqlc.types.Field(sgqlc.types.non_null(ModelPagination), graphql_name='paginationModel', args=sgqlc.types.ArgDict((
        ('filter_settings', sgqlc.types.Arg(ObjectFilterSettings, graphql_name='filterSettings', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('sorting', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(ObjectSortBySortingInput)), graphql_name='sorting', default=None)),
))
    )
    '''Arguments:

    * `filter_settings` (`ObjectFilterSettings`)None (default: `null`)
    * `limit` (`Int`)None (default: `null`)
    * `offset` (`Int`)None (default: `null`)
    * `sorting` (`[ObjectSortBySortingInput!]`)None (default: `null`)
    '''

    warning_delete_model_query = sgqlc.types.Field(sgqlc.types.non_null('WarningDeleteModel'), graphql_name='warningDeleteModelQuery', args=sgqlc.types.ArgDict((
        ('name', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='name', default=None)),
))
    )
    '''Arguments:

    * `name` (`String!`)None
    '''



class RoleDataParams(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('data_params', 'role')
    data_params = sgqlc.types.Field(sgqlc.types.non_null(DataParams), graphql_name='dataParams')

    role = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='role')



class RoleDatasetLoaderVersion(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('dataset_loader_version', 'role')
    dataset_loader_version = sgqlc.types.Field(sgqlc.types.non_null(DatasetLoaderVersionInfo), graphql_name='datasetLoaderVersion')

    role = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='role')



class RoleMethodSchema(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('list_method_schemas', 'role')
    list_method_schemas = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(MethodSchema))), graphql_name='listMethodSchemas')

    role = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='role')



class RoleModelParams(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('model_params', 'role')
    model_params = sgqlc.types.Field(sgqlc.types.non_null(ModelParams), graphql_name='modelParams')

    role = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='role')



class RoleModelVersion(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('model_version', 'role')
    model_version = sgqlc.types.Field(sgqlc.types.non_null(ModelVersionInfo), graphql_name='modelVersion')

    role = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='role')



class Subscription(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('build_job_status', 'job_status')
    build_job_status = sgqlc.types.Field(sgqlc.types.non_null(JobStatus), graphql_name='buildJobStatus', args=sgqlc.types.ArgDict((
        ('name', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='name', default=None)),
))
    )
    '''Arguments:

    * `name` (`String!`)None
    '''

    job_status = sgqlc.types.Field(sgqlc.types.non_null(JobStatus), graphql_name='jobStatus', args=sgqlc.types.ArgDict((
        ('name', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='name', default=None)),
))
    )
    '''Arguments:

    * `name` (`String!`)None
    '''



class User(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('id',)
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')



class WarningDeleteModel(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('delete_possible', 'list_model_version')
    delete_possible = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='deletePossible')

    list_model_version = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ModelVersionInfo))), graphql_name='listModelVersion')




########################################################################
# Unions
########################################################################

########################################################################
# Schema Entry Points
########################################################################
schema.query_type = Query
schema.mutation_type = Mutation
schema.subscription_type = Subscription

