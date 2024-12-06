# Shared Types

```python
from scale_gp.types import (
    Chunk,
    ChunkExtraInfoSchema,
    CompletionResponse,
    GenericDeleteResponse,
    ModelServerInfo,
    ModelUsage,
    ResultSchemaGeneration,
    StringExtraInfoSchema,
)
```

# KnowledgeBases

Types:

```python
from scale_gp.types import (
    CharacterChunkingStrategyConfig,
    ChunksResponse,
    CreateKnowledgeBaseResponse,
    CreateKnowledgeBaseUploadsFromFilesResponse,
    CustomChunkingStrategyConfig,
    DeleteKnowledgeBaseResponse,
    KnowledgeBase,
    PaginatedKnowledgeBaseUploads,
    PaginatedKnowledgeBases,
    TokenChunkingStrategyConfig,
    KnowledgeBaseUpdateResponse,
    KnowledgeBaseQueryResponse,
)
```

Methods:

- <code title="post /v4/knowledge-bases">client.knowledge_bases.<a href="./src/scale_gp/resources/knowledge_bases/knowledge_bases.py">create</a>(\*\*<a href="src/scale_gp/types/knowledge_base_create_params.py">params</a>) -> <a href="./src/scale_gp/types/create_knowledge_base_response.py">CreateKnowledgeBaseResponse</a></code>
- <code title="get /v4/knowledge-bases/{knowledge_base_id}">client.knowledge_bases.<a href="./src/scale_gp/resources/knowledge_bases/knowledge_bases.py">retrieve</a>(knowledge_base_id, \*\*<a href="src/scale_gp/types/knowledge_base_retrieve_params.py">params</a>) -> <a href="./src/scale_gp/types/knowledge_base.py">KnowledgeBase</a></code>
- <code title="patch /v4/knowledge-bases/{knowledge_base_id}">client.knowledge_bases.<a href="./src/scale_gp/resources/knowledge_bases/knowledge_bases.py">update</a>(knowledge_base_id, \*\*<a href="src/scale_gp/types/knowledge_base_update_params.py">params</a>) -> <a href="./src/scale_gp/types/knowledge_base_update_response.py">KnowledgeBaseUpdateResponse</a></code>
- <code title="get /v4/knowledge-bases">client.knowledge_bases.<a href="./src/scale_gp/resources/knowledge_bases/knowledge_bases.py">list</a>(\*\*<a href="src/scale_gp/types/knowledge_base_list_params.py">params</a>) -> <a href="./src/scale_gp/types/knowledge_base.py">SyncPageResponse[KnowledgeBase]</a></code>
- <code title="delete /v4/knowledge-bases/{knowledge_base_id}">client.knowledge_bases.<a href="./src/scale_gp/resources/knowledge_bases/knowledge_bases.py">delete</a>(knowledge_base_id) -> <a href="./src/scale_gp/types/delete_knowledge_base_response.py">DeleteKnowledgeBaseResponse</a></code>
- <code title="post /v4/knowledge-bases/{knowledge_base_id}/query">client.knowledge_bases.<a href="./src/scale_gp/resources/knowledge_bases/knowledge_bases.py">query</a>(knowledge_base_id, \*\*<a href="src/scale_gp/types/knowledge_base_query_params.py">params</a>) -> <a href="./src/scale_gp/types/knowledge_base_query_response.py">KnowledgeBaseQueryResponse</a></code>
- <code title="post /v4/knowledge-bases/{knowledge_base_id}/upload_files">client.knowledge_bases.<a href="./src/scale_gp/resources/knowledge_bases/knowledge_bases.py">upload_files</a>(knowledge_base_id, \*\*<a href="src/scale_gp/types/knowledge_base_upload_files_params.py">params</a>) -> <a href="./src/scale_gp/types/create_knowledge_base_uploads_from_files_response.py">CreateKnowledgeBaseUploadsFromFilesResponse</a></code>

## AsyncJobs

Types:

```python
from scale_gp.types.knowledge_bases import AsyncJobListResponse
```

Methods:

- <code title="get /v4/knowledge-bases/{knowledge_base_id}/async-jobs">client.knowledge_bases.async_jobs.<a href="./src/scale_gp/resources/knowledge_bases/async_jobs.py">list</a>(knowledge_base_id, \*\*<a href="src/scale_gp/types/knowledge_bases/async_job_list_params.py">params</a>) -> <a href="./src/scale_gp/types/knowledge_bases/async_job_list_response.py">SyncTopLevelArray[AsyncJobListResponse]</a></code>

## Chunks

Types:

```python
from scale_gp.types.knowledge_bases import ChunkListResponse
```

Methods:

- <code title="get /v4/knowledge-bases/{knowledge_base_id}/chunks">client.knowledge_bases.chunks.<a href="./src/scale_gp/resources/knowledge_bases/chunks.py">list</a>(knowledge_base_id, \*\*<a href="src/scale_gp/types/knowledge_bases/chunk_list_params.py">params</a>) -> <a href="./src/scale_gp/types/knowledge_bases/chunk_list_response.py">SyncChunkPagination[ChunkListResponse]</a></code>

## DataSourceConnections

Types:

```python
from scale_gp.types.knowledge_bases import DeleteKnowledgeBaseDataSourceConnectionResponse
```

Methods:

- <code title="post /v4/knowledge-bases/{knowledge_base_id}/data-source-connections/{knowledge_base_data_source_id}/delete">client.knowledge_bases.data_source_connections.<a href="./src/scale_gp/resources/knowledge_bases/data_source_connections.py">delete</a>(knowledge_base_data_source_id, \*, knowledge_base_id, \*\*<a href="src/scale_gp/types/knowledge_bases/data_source_connection_delete_params.py">params</a>) -> <a href="./src/scale_gp/types/knowledge_bases/delete_knowledge_base_data_source_connection_response.py">DeleteKnowledgeBaseDataSourceConnectionResponse</a></code>

## Uploads

Types:

```python
from scale_gp.types.knowledge_bases import (
    CancelKnowledgeBaseUploadResponse,
    CreateKnowledgeBaseUploadResponse,
    KnowledgeBaseUpload,
    UploadListResponse,
)
```

Methods:

- <code title="post /v4/knowledge-bases/{knowledge_base_id}/uploads">client.knowledge_bases.uploads.<a href="./src/scale_gp/resources/knowledge_bases/uploads.py">create</a>(knowledge_base_id, \*\*<a href="src/scale_gp/types/knowledge_bases/upload_create_params.py">params</a>) -> <a href="./src/scale_gp/types/knowledge_bases/create_knowledge_base_upload_response.py">CreateKnowledgeBaseUploadResponse</a></code>
- <code title="get /v4/knowledge-bases/{knowledge_base_id}/uploads/{upload_id}">client.knowledge_bases.uploads.<a href="./src/scale_gp/resources/knowledge_bases/uploads.py">retrieve</a>(upload_id, \*, knowledge_base_id, \*\*<a href="src/scale_gp/types/knowledge_bases/upload_retrieve_params.py">params</a>) -> <a href="./src/scale_gp/types/knowledge_bases/knowledge_base_upload.py">KnowledgeBaseUpload</a></code>
- <code title="get /v4/knowledge-bases/{knowledge_base_id}/uploads">client.knowledge_bases.uploads.<a href="./src/scale_gp/resources/knowledge_bases/uploads.py">list</a>(knowledge_base_id, \*\*<a href="src/scale_gp/types/knowledge_bases/upload_list_params.py">params</a>) -> <a href="./src/scale_gp/types/knowledge_bases/upload_list_response.py">SyncPageResponse[UploadListResponse]</a></code>
- <code title="post /v4/knowledge-bases/{knowledge_base_id}/uploads/{upload_id}/cancel">client.knowledge_bases.uploads.<a href="./src/scale_gp/resources/knowledge_bases/uploads.py">cancel</a>(upload_id, \*, knowledge_base_id) -> <a href="./src/scale_gp/types/knowledge_bases/cancel_knowledge_base_upload_response.py">CancelKnowledgeBaseUploadResponse</a></code>

## Artifacts

Types:

```python
from scale_gp.types.knowledge_bases import (
    Artifact,
    PaginatedArtifacts,
    ArtifactUpdateResponse,
    ArtifactListResponse,
    ArtifactDeleteResponse,
    ArtifactBatchDeleteResponse,
)
```

Methods:

- <code title="get /v4/knowledge-bases/{knowledge_base_id}/artifacts/{artifact_id}">client.knowledge_bases.artifacts.<a href="./src/scale_gp/resources/knowledge_bases/artifacts.py">retrieve</a>(artifact_id, \*, knowledge_base_id, \*\*<a href="src/scale_gp/types/knowledge_bases/artifact_retrieve_params.py">params</a>) -> <a href="./src/scale_gp/types/knowledge_bases/artifact.py">Artifact</a></code>
- <code title="patch /v4/knowledge-bases/{knowledge_base_id}/artifacts/{artifact_id}">client.knowledge_bases.artifacts.<a href="./src/scale_gp/resources/knowledge_bases/artifacts.py">update</a>(artifact_id, \*, knowledge_base_id, \*\*<a href="src/scale_gp/types/knowledge_bases/artifact_update_params.py">params</a>) -> <a href="./src/scale_gp/types/knowledge_bases/artifact_update_response.py">ArtifactUpdateResponse</a></code>
- <code title="get /v4/knowledge-bases/{knowledge_base_id}/artifacts">client.knowledge_bases.artifacts.<a href="./src/scale_gp/resources/knowledge_bases/artifacts.py">list</a>(knowledge_base_id, \*\*<a href="src/scale_gp/types/knowledge_bases/artifact_list_params.py">params</a>) -> <a href="./src/scale_gp/types/knowledge_bases/artifact_list_response.py">SyncPageResponse[ArtifactListResponse]</a></code>
- <code title="delete /v4/knowledge-bases/{knowledge_base_id}/artifacts/{artifact_id}">client.knowledge_bases.artifacts.<a href="./src/scale_gp/resources/knowledge_bases/artifacts.py">delete</a>(artifact_id, \*, knowledge_base_id) -> <a href="./src/scale_gp/types/knowledge_bases/artifact_delete_response.py">ArtifactDeleteResponse</a></code>
- <code title="post /v4/knowledge-bases/{knowledge_base_id}/artifacts/batch-delete">client.knowledge_bases.artifacts.<a href="./src/scale_gp/resources/knowledge_bases/artifacts.py">batch_delete</a>(knowledge_base_id, \*\*<a href="src/scale_gp/types/knowledge_bases/artifact_batch_delete_params.py">params</a>) -> <a href="./src/scale_gp/types/knowledge_bases/artifact_batch_delete_response.py">ArtifactBatchDeleteResponse</a></code>

## UploadSchedules

Types:

```python
from scale_gp.types.knowledge_bases import (
    PaginatedUploadScheduleWithViews,
    UploadSchedule,
    UploadScheduleWithViews,
)
```

Methods:

- <code title="post /v4/knowledge-bases/{knowledge_base_id}/upload-schedules">client.knowledge_bases.upload_schedules.<a href="./src/scale_gp/resources/knowledge_bases/upload_schedules.py">create</a>(knowledge_base_id, \*\*<a href="src/scale_gp/types/knowledge_bases/upload_schedule_create_params.py">params</a>) -> <a href="./src/scale_gp/types/knowledge_bases/upload_schedule.py">UploadSchedule</a></code>
- <code title="get /v4/knowledge-bases/{knowledge_base_id}/upload-schedules/{upload_schedule_id}">client.knowledge_bases.upload_schedules.<a href="./src/scale_gp/resources/knowledge_bases/upload_schedules.py">retrieve</a>(upload_schedule_id, \*, knowledge_base_id, \*\*<a href="src/scale_gp/types/knowledge_bases/upload_schedule_retrieve_params.py">params</a>) -> <a href="./src/scale_gp/types/knowledge_bases/upload_schedule_with_views.py">UploadScheduleWithViews</a></code>
- <code title="patch /v4/knowledge-bases/{knowledge_base_id}/upload-schedules/{upload_schedule_id}">client.knowledge_bases.upload_schedules.<a href="./src/scale_gp/resources/knowledge_bases/upload_schedules.py">update</a>(upload_schedule_id, \*, knowledge_base_id, \*\*<a href="src/scale_gp/types/knowledge_bases/upload_schedule_update_params.py">params</a>) -> <a href="./src/scale_gp/types/knowledge_bases/upload_schedule.py">UploadSchedule</a></code>
- <code title="get /v4/knowledge-bases/{knowledge_base_id}/upload-schedules">client.knowledge_bases.upload_schedules.<a href="./src/scale_gp/resources/knowledge_bases/upload_schedules.py">list</a>(knowledge_base_id, \*\*<a href="src/scale_gp/types/knowledge_bases/upload_schedule_list_params.py">params</a>) -> <a href="./src/scale_gp/types/knowledge_bases/upload_schedule_with_views.py">SyncPageResponse[UploadScheduleWithViews]</a></code>
- <code title="delete /v4/knowledge-bases/{knowledge_base_id}/upload-schedules/{upload_schedule_id}">client.knowledge_bases.upload_schedules.<a href="./src/scale_gp/resources/knowledge_bases/upload_schedules.py">delete</a>(upload_schedule_id, \*, knowledge_base_id) -> <a href="./src/scale_gp/types/shared/generic_delete_response.py">GenericDeleteResponse</a></code>

# KnowledgeBaseDataSources

Types:

```python
from scale_gp.types import (
    AzureBlobStorageDataSourceAuthConfig,
    AzureBlobStorageDataSourceConfig,
    ConfluenceDataSourceAuthConfig,
    ConfluenceDataSourceConfig,
    GoogleDriveDataSourceAuthConfig,
    GoogleDriveDataSourceConfig,
    KnowledgeBaseDataSource,
    LocalChunksSourceConfig,
    LocalFileSourceConfig,
    PaginatedKnowledgeBaseDataSources,
    S3DataSourceAuthConfig,
    S3DataSourceConfig,
    SharePointDataSourceAuthConfig,
    SharePointDataSourceConfig,
    SlackDataSourceAuthConfig,
    SlackDataSourceConfig,
    KnowledgeBaseDataSourceVerifyResponse,
)
```

Methods:

- <code title="post /v4/knowledge-base-data-sources">client.knowledge_base_data_sources.<a href="./src/scale_gp/resources/knowledge_base_data_sources.py">create</a>(\*\*<a href="src/scale_gp/types/knowledge_base_data_source_create_params.py">params</a>) -> <a href="./src/scale_gp/types/knowledge_base_data_source.py">KnowledgeBaseDataSource</a></code>
- <code title="get /v4/knowledge-base-data-sources/{knowledge_base_data_source_id}">client.knowledge_base_data_sources.<a href="./src/scale_gp/resources/knowledge_base_data_sources.py">retrieve</a>(knowledge_base_data_source_id) -> <a href="./src/scale_gp/types/knowledge_base_data_source.py">KnowledgeBaseDataSource</a></code>
- <code title="patch /v4/knowledge-base-data-sources/{knowledge_base_data_source_id}">client.knowledge_base_data_sources.<a href="./src/scale_gp/resources/knowledge_base_data_sources.py">update</a>(knowledge_base_data_source_id, \*\*<a href="src/scale_gp/types/knowledge_base_data_source_update_params.py">params</a>) -> <a href="./src/scale_gp/types/knowledge_base_data_source.py">KnowledgeBaseDataSource</a></code>
- <code title="get /v4/knowledge-base-data-sources">client.knowledge_base_data_sources.<a href="./src/scale_gp/resources/knowledge_base_data_sources.py">list</a>(\*\*<a href="src/scale_gp/types/knowledge_base_data_source_list_params.py">params</a>) -> <a href="./src/scale_gp/types/knowledge_base_data_source.py">SyncPageResponse[KnowledgeBaseDataSource]</a></code>
- <code title="delete /v4/knowledge-base-data-sources/{knowledge_base_data_source_id}">client.knowledge_base_data_sources.<a href="./src/scale_gp/resources/knowledge_base_data_sources.py">delete</a>(knowledge_base_data_source_id) -> <a href="./src/scale_gp/types/shared/generic_delete_response.py">GenericDeleteResponse</a></code>
- <code title="post /v4/knowledge-base-data-sources/{knowledge_base_data_source_id}/verify">client.knowledge_base_data_sources.<a href="./src/scale_gp/resources/knowledge_base_data_sources.py">verify</a>(knowledge_base_data_source_id) -> <a href="./src/scale_gp/types/knowledge_base_data_source_verify_response.py">object</a></code>

# Chunks

Types:

```python
from scale_gp.types import RankedChunksResponse, SynthesizeChunksResponse
```

Methods:

- <code title="post /v4/chunks/rank">client.chunks.<a href="./src/scale_gp/resources/chunks.py">rank</a>(\*\*<a href="src/scale_gp/types/chunk_rank_params.py">params</a>) -> <a href="./src/scale_gp/types/ranked_chunks_response.py">RankedChunksResponse</a></code>
- <code title="post /v4/chunks/synthesis">client.chunks.<a href="./src/scale_gp/resources/chunks.py">synthesis</a>(\*\*<a href="src/scale_gp/types/chunk_synthesis_params.py">params</a>) -> <a href="./src/scale_gp/types/synthesize_chunks_response.py">SynthesizeChunksResponse</a></code>

# Agents

Types:

```python
from scale_gp.types import ExecuteAgentResponse
```

Methods:

- <code title="post /v4/agents/execute">client.agents.<a href="./src/scale_gp/resources/agents.py">execute</a>(\*\*<a href="src/scale_gp/types/agent_execute_params.py">params</a>) -> <a href="./src/scale_gp/types/execute_agent_response.py">ExecuteAgentResponse</a></code>

# Completions

Types:

```python
from scale_gp.types import CompletionsResponse
```

Methods:

- <code title="post /v4/completions">client.completions.<a href="./src/scale_gp/resources/completions.py">create</a>(\*\*<a href="src/scale_gp/types/completion_create_params.py">params</a>) -> <a href="./src/scale_gp/types/completions_response.py">CompletionsResponse</a></code>

# ChatCompletions

Types:

```python
from scale_gp.types import ChatCompletionsResponse
```

Methods:

- <code title="post /v4/chat-completions">client.chat_completions.<a href="./src/scale_gp/resources/chat_completions.py">create</a>(\*\*<a href="src/scale_gp/types/chat_completion_create_params.py">params</a>) -> <a href="./src/scale_gp/types/chat_completions_response.py">ChatCompletionsResponse</a></code>

# Models

Types:

```python
from scale_gp.types import (
    EmbeddingResponse,
    GenericModelResponse,
    ModelInstance,
    ModelInstanceWithViews,
    PaginatedModelInstanceWithViews,
    ParameterBindings,
    RerankingResponse,
)
```

Methods:

- <code title="post /v4/models">client.models.<a href="./src/scale_gp/resources/models/models.py">create</a>(\*\*<a href="src/scale_gp/types/model_create_params.py">params</a>) -> <a href="./src/scale_gp/types/model_instance.py">ModelInstance</a></code>
- <code title="get /v4/models/{model_id}">client.models.<a href="./src/scale_gp/resources/models/models.py">retrieve</a>(model_id, \*\*<a href="src/scale_gp/types/model_retrieve_params.py">params</a>) -> <a href="./src/scale_gp/types/model_instance_with_views.py">ModelInstanceWithViews</a></code>
- <code title="patch /v4/models/{model_id}">client.models.<a href="./src/scale_gp/resources/models/models.py">update</a>(model_id, \*\*<a href="src/scale_gp/types/model_update_params.py">params</a>) -> <a href="./src/scale_gp/types/model_instance.py">ModelInstance</a></code>
- <code title="get /v4/models">client.models.<a href="./src/scale_gp/resources/models/models.py">list</a>(\*\*<a href="src/scale_gp/types/model_list_params.py">params</a>) -> <a href="./src/scale_gp/types/model_instance_with_views.py">SyncPageResponse[ModelInstanceWithViews]</a></code>
- <code title="delete /v4/models/{model_id}">client.models.<a href="./src/scale_gp/resources/models/models.py">delete</a>(model_id) -> <a href="./src/scale_gp/types/shared/generic_delete_response.py">GenericDeleteResponse</a></code>

## Deployments

Types:

```python
from scale_gp.types.models import ModelDeployment, PaginatedModelDeployments
```

Methods:

- <code title="post /v4/models/{model_instance_id}/deployments">client.models.deployments.<a href="./src/scale_gp/resources/models/deployments/deployments.py">create</a>(model_instance_id, \*\*<a href="src/scale_gp/types/models/deployment_create_params.py">params</a>) -> <a href="./src/scale_gp/types/models/model_deployment.py">ModelDeployment</a></code>
- <code title="get /v4/models/{model_instance_id}/deployments/{deployment_id}">client.models.deployments.<a href="./src/scale_gp/resources/models/deployments/deployments.py">retrieve</a>(deployment_id, \*, model_instance_id) -> <a href="./src/scale_gp/types/models/model_deployment.py">ModelDeployment</a></code>
- <code title="patch /v4/models/{model_instance_id}/deployments/{deployment_id}">client.models.deployments.<a href="./src/scale_gp/resources/models/deployments/deployments.py">update</a>(deployment_id, \*, model_instance_id, \*\*<a href="src/scale_gp/types/models/deployment_update_params.py">params</a>) -> <a href="./src/scale_gp/types/models/model_deployment.py">ModelDeployment</a></code>
- <code title="get /v4/models/{model_instance_id}/deployments">client.models.deployments.<a href="./src/scale_gp/resources/models/deployments/deployments.py">list</a>(model_instance_id, \*\*<a href="src/scale_gp/types/models/deployment_list_params.py">params</a>) -> <a href="./src/scale_gp/types/models/model_deployment.py">SyncPageResponse[ModelDeployment]</a></code>
- <code title="delete /v4/models/{model_instance_id}/deployments/{deployment_id}">client.models.deployments.<a href="./src/scale_gp/resources/models/deployments/deployments.py">delete</a>(deployment_id, \*, model_instance_id) -> <a href="./src/scale_gp/types/shared/generic_delete_response.py">GenericDeleteResponse</a></code>
- <code title="post /v4/models/{model_instance_id}/deployments/{model_deployment_id}/execute">client.models.deployments.<a href="./src/scale_gp/resources/models/deployments/deployments.py">execute</a>(model_deployment_id, \*, model_instance_id, \*\*<a href="src/scale_gp/types/models/deployment_execute_params.py">params</a>) -> <a href="./src/scale_gp/types/generic_model_response.py">GenericModelResponse</a></code>
- <code title="get /v4/model-deployments">client.models.deployments.<a href="./src/scale_gp/resources/models/deployments/deployments.py">list_all</a>(\*\*<a href="src/scale_gp/types/models/deployment_list_all_params.py">params</a>) -> <a href="./src/scale_gp/types/models/model_deployment.py">SyncPageResponse[ModelDeployment]</a></code>

### UsageStatistics

Methods:

- <code title="get /v4/model-deployments/{model_deployment_id}/usage-statistics">client.models.deployments.usage_statistics.<a href="./src/scale_gp/resources/models/deployments/usage_statistics.py">retrieve</a>(model_deployment_id, \*\*<a href="src/scale_gp/types/models/deployments/usage_statistic_retrieve_params.py">params</a>) -> <a href="./src/scale_gp/types/shared/model_usage.py">ModelUsage</a></code>

## Embeddings

Methods:

- <code title="post /v4/models/{model_deployment_id}/embeddings">client.models.embeddings.<a href="./src/scale_gp/resources/models/embeddings.py">create</a>(model_deployment_id, \*\*<a href="src/scale_gp/types/models/embedding_create_params.py">params</a>) -> <a href="./src/scale_gp/types/embedding_response.py">EmbeddingResponse</a></code>

## Rerankings

Methods:

- <code title="post /v4/models/{model_deployment_id}/rerankings">client.models.rerankings.<a href="./src/scale_gp/resources/models/rerankings.py">create</a>(model_deployment_id, \*\*<a href="src/scale_gp/types/models/reranking_create_params.py">params</a>) -> <a href="./src/scale_gp/types/reranking_response.py">RerankingResponse</a></code>

## Completions

Methods:

- <code title="post /v4/models/{model_deployment_id}/completions">client.models.completions.<a href="./src/scale_gp/resources/models/completions.py">create</a>(model_deployment_id, \*\*<a href="src/scale_gp/types/models/completion_create_params.py">params</a>) -> <a href="./src/scale_gp/types/shared/completion_response.py">CompletionResponse</a></code>

## ChatCompletions

Methods:

- <code title="post /v4/models/{model_deployment_id}/chat-completions">client.models.chat_completions.<a href="./src/scale_gp/resources/models/chat_completions.py">create</a>(model_deployment_id, \*\*<a href="src/scale_gp/types/models/chat_completion_create_params.py">params</a>) -> <a href="./src/scale_gp/types/shared/completion_response.py">CompletionResponse</a></code>

## UsageStatistics

Methods:

- <code title="get /v4/models/{model_name}/usage-statistics">client.models.usage_statistics.<a href="./src/scale_gp/resources/models/usage_statistics.py">retrieve</a>(model_name, \*\*<a href="src/scale_gp/types/models/usage_statistic_retrieve_params.py">params</a>) -> <a href="./src/scale_gp/types/shared/model_usage.py">ModelUsage</a></code>

# ModelGroups

Types:

```python
from scale_gp.types import ModelGroup, PaginatedModelGroups
```

Methods:

- <code title="post /v4/model-groups">client.model_groups.<a href="./src/scale_gp/resources/model_groups/model_groups.py">create</a>(\*\*<a href="src/scale_gp/types/model_group_create_params.py">params</a>) -> <a href="./src/scale_gp/types/model_group.py">ModelGroup</a></code>
- <code title="get /v4/model-groups/{model_group_id}">client.model_groups.<a href="./src/scale_gp/resources/model_groups/model_groups.py">retrieve</a>(model_group_id) -> <a href="./src/scale_gp/types/model_group.py">ModelGroup</a></code>
- <code title="patch /v4/model-groups/{model_group_id}">client.model_groups.<a href="./src/scale_gp/resources/model_groups/model_groups.py">update</a>(model_group_id, \*\*<a href="src/scale_gp/types/model_group_update_params.py">params</a>) -> <a href="./src/scale_gp/types/model_group.py">ModelGroup</a></code>
- <code title="get /v4/model-groups">client.model_groups.<a href="./src/scale_gp/resources/model_groups/model_groups.py">list</a>(\*\*<a href="src/scale_gp/types/model_group_list_params.py">params</a>) -> <a href="./src/scale_gp/types/model_group.py">SyncPageResponse[ModelGroup]</a></code>
- <code title="delete /v4/model-groups/{model_group_id}">client.model_groups.<a href="./src/scale_gp/resources/model_groups/model_groups.py">delete</a>(model_group_id) -> <a href="./src/scale_gp/types/shared/generic_delete_response.py">GenericDeleteResponse</a></code>

## Models

Methods:

- <code title="post /v4/model-groups/{model_group_id}/models/{model_instance_id}">client.model_groups.models.<a href="./src/scale_gp/resources/model_groups/models.py">create</a>(model_instance_id, \*, model_group_id) -> <a href="./src/scale_gp/types/model_instance.py">ModelInstance</a></code>

## UsageStatistics

Methods:

- <code title="get /v4/model-groups/{model_group_id}/usage-statistics">client.model_groups.usage_statistics.<a href="./src/scale_gp/resources/model_groups/usage_statistics.py">retrieve</a>(model_group_id, \*\*<a href="src/scale_gp/types/model_groups/usage_statistic_retrieve_params.py">params</a>) -> <a href="./src/scale_gp/types/shared/model_usage.py">ModelUsage</a></code>

# Users

Types:

```python
from scale_gp.types import UserInfo, UserRetrieveResponse
```

Methods:

- <code title="get /users/{user_id}">client.users.<a href="./src/scale_gp/resources/users.py">retrieve</a>(user_id) -> <a href="./src/scale_gp/types/user_retrieve_response.py">UserRetrieveResponse</a></code>
- <code title="get /user-info">client.users.<a href="./src/scale_gp/resources/users.py">info</a>() -> <a href="./src/scale_gp/types/user_info.py">UserInfo</a></code>

# Accounts

Types:

```python
from scale_gp.types import CreateAccountResponse
```

Methods:

- <code title="post /accounts">client.accounts.<a href="./src/scale_gp/resources/accounts.py">create</a>(\*\*<a href="src/scale_gp/types/account_create_params.py">params</a>) -> <a href="./src/scale_gp/types/create_account_response.py">CreateAccountResponse</a></code>

# QuestionSets

Types:

```python
from scale_gp.types import (
    PaginatedQuestionSets,
    QuestionSet,
    QuestionSetWithQuestions,
    QuestionSetListResponse,
)
```

Methods:

- <code title="post /v4/question-sets">client.question_sets.<a href="./src/scale_gp/resources/question_sets.py">create</a>(\*\*<a href="src/scale_gp/types/question_set_create_params.py">params</a>) -> <a href="./src/scale_gp/types/question_set.py">QuestionSet</a></code>
- <code title="get /v4/question-sets/{question_set_id}">client.question_sets.<a href="./src/scale_gp/resources/question_sets.py">retrieve</a>(question_set_id) -> <a href="./src/scale_gp/types/question_set_with_questions.py">QuestionSetWithQuestions</a></code>
- <code title="patch /v4/question-sets/{question_set_id}">client.question_sets.<a href="./src/scale_gp/resources/question_sets.py">update</a>(question_set_id, \*\*<a href="src/scale_gp/types/question_set_update_params.py">params</a>) -> <a href="./src/scale_gp/types/question_set.py">QuestionSet</a></code>
- <code title="get /v4/question-sets">client.question_sets.<a href="./src/scale_gp/resources/question_sets.py">list</a>(\*\*<a href="src/scale_gp/types/question_set_list_params.py">params</a>) -> <a href="./src/scale_gp/types/question_set_list_response.py">SyncPageResponse[QuestionSetListResponse]</a></code>
- <code title="delete /v4/question-sets/{question_set_id}">client.question_sets.<a href="./src/scale_gp/resources/question_sets.py">delete</a>(question_set_id) -> <a href="./src/scale_gp/types/shared/generic_delete_response.py">GenericDeleteResponse</a></code>

# Evaluations

Types:

```python
from scale_gp.types import (
    AnnotationConfig,
    Evaluation,
    EvaluationMetrics,
    EvaluationTraceSpan,
    EvaluationWithViews,
    HybridEvaluationMetrics,
    MultiturnAnnotationConfig,
    PaginatedEvaluations,
    SummarizationAnnotationConfig,
    Task,
    TranslationAnnotationConfig,
)
```

Methods:

- <code title="post /v4/evaluations">client.evaluations.<a href="./src/scale_gp/resources/evaluations/evaluations.py">create</a>(\*\*<a href="src/scale_gp/types/evaluation_create_params.py">params</a>) -> <a href="./src/scale_gp/types/evaluation.py">Evaluation</a></code>
- <code title="get /v4/evaluations/{evaluation_id}">client.evaluations.<a href="./src/scale_gp/resources/evaluations/evaluations.py">retrieve</a>(evaluation_id, \*\*<a href="src/scale_gp/types/evaluation_retrieve_params.py">params</a>) -> <a href="./src/scale_gp/types/evaluation_with_views.py">EvaluationWithViews</a></code>
- <code title="patch /v4/evaluations/{evaluation_id}">client.evaluations.<a href="./src/scale_gp/resources/evaluations/evaluations.py">update</a>(evaluation_id, \*\*<a href="src/scale_gp/types/evaluation_update_params.py">params</a>) -> <a href="./src/scale_gp/types/evaluation.py">Evaluation</a></code>
- <code title="get /v4/evaluations">client.evaluations.<a href="./src/scale_gp/resources/evaluations/evaluations.py">list</a>(\*\*<a href="src/scale_gp/types/evaluation_list_params.py">params</a>) -> <a href="./src/scale_gp/types/evaluation_with_views.py">SyncPageResponse[EvaluationWithViews]</a></code>
- <code title="delete /v4/evaluations/{evaluation_id}">client.evaluations.<a href="./src/scale_gp/resources/evaluations/evaluations.py">delete</a>(evaluation_id) -> <a href="./src/scale_gp/types/shared/generic_delete_response.py">GenericDeleteResponse</a></code>
- <code title="post /v4/evaluations/{evaluation_id}/claim-task">client.evaluations.<a href="./src/scale_gp/resources/evaluations/evaluations.py">claim_task</a>(evaluation_id, \*\*<a href="src/scale_gp/types/evaluation_claim_task_params.py">params</a>) -> <a href="./src/scale_gp/types/task.py">Optional[Task]</a></code>

## Tasks

Methods:

- <code title="patch /v4/evaluations/{evaluation_id}/tasks/{task_id}">client.evaluations.tasks.<a href="./src/scale_gp/resources/evaluations/tasks.py">update</a>(task_id, \*, evaluation_id, \*\*<a href="src/scale_gp/types/evaluations/task_update_params.py">params</a>) -> <a href="./src/scale_gp/types/task.py">Optional[Task]</a></code>

## ContributorMetrics

Types:

```python
from scale_gp.types.evaluations import ContributorMetrics, PaginatedContributorMetrics
```

Methods:

- <code title="get /v4/evaluations/{evaluation_id}/contributor-metrics/{contributor_id}">client.evaluations.contributor_metrics.<a href="./src/scale_gp/resources/evaluations/contributor_metrics.py">retrieve</a>(contributor_id, \*, evaluation_id) -> <a href="./src/scale_gp/types/evaluations/contributor_metrics.py">Optional[ContributorMetrics]</a></code>
- <code title="get /v4/evaluations/{evaluation_id}/contributor-metrics">client.evaluations.contributor_metrics.<a href="./src/scale_gp/resources/evaluations/contributor_metrics.py">list</a>(evaluation_id, \*\*<a href="src/scale_gp/types/evaluations/contributor_metric_list_params.py">params</a>) -> <a href="./src/scale_gp/types/evaluations/contributor_metrics.py">SyncPageResponse[ContributorMetrics]</a></code>

## EvaluationMetrics

Methods:

- <code title="get /v4/evaluations/{evaluation_id}/evaluation-metrics">client.evaluations.evaluation_metrics.<a href="./src/scale_gp/resources/evaluations/evaluation_metrics.py">retrieve</a>(evaluation_id) -> <a href="./src/scale_gp/types/evaluation_metrics.py">EvaluationMetrics</a></code>

## HybridEvalMetrics

Methods:

- <code title="get /v4/evaluations/{evaluation_id}/hybrid-eval-metrics">client.evaluations.hybrid_eval_metrics.<a href="./src/scale_gp/resources/evaluations/hybrid_eval_metrics.py">retrieve</a>(evaluation_id) -> <a href="./src/scale_gp/types/hybrid_evaluation_metrics.py">HybridEvaluationMetrics</a></code>

## TestCaseResults

Types:

```python
from scale_gp.types.evaluations import (
    PaginatedTestCaseResultWithViews,
    TestCaseResult,
    TestCaseResultWithViews,
    TestCaseResultBatchResponse,
)
```

Methods:

- <code title="post /v4/evaluations/{evaluation_id}/test-case-results">client.evaluations.test_case_results.<a href="./src/scale_gp/resources/evaluations/test_case_results/test_case_results.py">create</a>(evaluation_id, \*\*<a href="src/scale_gp/types/evaluations/test_case_result_create_params.py">params</a>) -> <a href="./src/scale_gp/types/evaluations/test_case_result.py">TestCaseResult</a></code>
- <code title="get /v4/evaluations/{evaluation_id}/test-case-results/{test_case_result_id}">client.evaluations.test_case_results.<a href="./src/scale_gp/resources/evaluations/test_case_results/test_case_results.py">retrieve</a>(test_case_result_id, \*, evaluation_id, \*\*<a href="src/scale_gp/types/evaluations/test_case_result_retrieve_params.py">params</a>) -> <a href="./src/scale_gp/types/evaluations/test_case_result_with_views.py">TestCaseResultWithViews</a></code>
- <code title="patch /v4/evaluations/{evaluation_id}/test-case-results/{test_case_result_id}">client.evaluations.test_case_results.<a href="./src/scale_gp/resources/evaluations/test_case_results/test_case_results.py">update</a>(test_case_result_id, \*, evaluation_id, \*\*<a href="src/scale_gp/types/evaluations/test_case_result_update_params.py">params</a>) -> <a href="./src/scale_gp/types/evaluations/test_case_result.py">TestCaseResult</a></code>
- <code title="get /v4/evaluations/{evaluation_id}/test-case-results">client.evaluations.test_case_results.<a href="./src/scale_gp/resources/evaluations/test_case_results/test_case_results.py">list</a>(evaluation_id, \*\*<a href="src/scale_gp/types/evaluations/test_case_result_list_params.py">params</a>) -> <a href="./src/scale_gp/types/evaluations/test_case_result_with_views.py">SyncPageResponse[TestCaseResultWithViews]</a></code>
- <code title="post /v4/evaluations/{evaluation_id}/test-case-results/batch">client.evaluations.test_case_results.<a href="./src/scale_gp/resources/evaluations/test_case_results/test_case_results.py">batch</a>(evaluation_id, \*\*<a href="src/scale_gp/types/evaluations/test_case_result_batch_params.py">params</a>) -> <a href="./src/scale_gp/types/evaluations/test_case_result_batch_response.py">TestCaseResultBatchResponse</a></code>

### History

Types:

```python
from scale_gp.types.evaluations.test_case_results import PaginatedTestCaseResults
```

Methods:

- <code title="get /v4/evaluations/{evaluation_id}/test-case-results/{test_case_result_id}/history/{num}">client.evaluations.test_case_results.history.<a href="./src/scale_gp/resources/evaluations/test_case_results/history.py">retrieve</a>(num, \*, evaluation_id, test_case_result_id) -> <a href="./src/scale_gp/types/evaluations/test_case_result.py">TestCaseResult</a></code>
- <code title="get /v4/evaluations/{evaluation_id}/test-case-results/history/{num}">client.evaluations.test_case_results.history.<a href="./src/scale_gp/resources/evaluations/test_case_results/history.py">list</a>(num, \*, evaluation_id, \*\*<a href="src/scale_gp/types/evaluations/test_case_results/history_list_params.py">params</a>) -> <a href="./src/scale_gp/types/evaluations/test_case_result.py">SyncPageResponse[TestCaseResult]</a></code>

# EvaluationConfigs

Types:

```python
from scale_gp.types import EvaluationConfig, PaginatedEvaluationConfigs
```

Methods:

- <code title="post /v4/evaluation-configs">client.evaluation_configs.<a href="./src/scale_gp/resources/evaluation_configs.py">create</a>(\*\*<a href="src/scale_gp/types/evaluation_config_create_params.py">params</a>) -> <a href="./src/scale_gp/types/evaluation_config.py">EvaluationConfig</a></code>
- <code title="get /v4/evaluation-configs/{evaluation_config_id}">client.evaluation_configs.<a href="./src/scale_gp/resources/evaluation_configs.py">retrieve</a>(evaluation_config_id) -> <a href="./src/scale_gp/types/evaluation_config.py">EvaluationConfig</a></code>
- <code title="get /v4/evaluation-configs">client.evaluation_configs.<a href="./src/scale_gp/resources/evaluation_configs.py">list</a>(\*\*<a href="src/scale_gp/types/evaluation_config_list_params.py">params</a>) -> <a href="./src/scale_gp/types/evaluation_config.py">SyncPageResponse[EvaluationConfig]</a></code>
- <code title="delete /v4/evaluation-configs/{evaluation_config_id}">client.evaluation_configs.<a href="./src/scale_gp/resources/evaluation_configs.py">delete</a>(evaluation_config_id) -> <a href="./src/scale_gp/types/shared/generic_delete_response.py">GenericDeleteResponse</a></code>

# EvaluationDatasets

Types:

```python
from scale_gp.types import (
    AutoGeneratedDraftTestCaseApproveBatchResponse,
    AutoGeneratedDraftTestCaseMissingChunkInfo,
    EvaluationDataset,
    PaginatedEvaluationDatasets,
    PublishEvaluationDatasetDraftResponse,
    EvaluationDatasetRetrieveResponse,
    EvaluationDatasetListResponse,
)
```

Methods:

- <code title="post /v4/evaluation-datasets">client.evaluation_datasets.<a href="./src/scale_gp/resources/evaluation_datasets/evaluation_datasets.py">create</a>(\*\*<a href="src/scale_gp/types/evaluation_dataset_create_params.py">params</a>) -> <a href="./src/scale_gp/types/evaluation_dataset.py">EvaluationDataset</a></code>
- <code title="get /v4/evaluation-datasets/{evaluation_dataset_id}">client.evaluation_datasets.<a href="./src/scale_gp/resources/evaluation_datasets/evaluation_datasets.py">retrieve</a>(evaluation_dataset_id, \*\*<a href="src/scale_gp/types/evaluation_dataset_retrieve_params.py">params</a>) -> <a href="./src/scale_gp/types/evaluation_dataset_retrieve_response.py">EvaluationDatasetRetrieveResponse</a></code>
- <code title="patch /v4/evaluation-datasets/{evaluation_dataset_id}">client.evaluation_datasets.<a href="./src/scale_gp/resources/evaluation_datasets/evaluation_datasets.py">update</a>(evaluation_dataset_id, \*\*<a href="src/scale_gp/types/evaluation_dataset_update_params.py">params</a>) -> <a href="./src/scale_gp/types/evaluation_dataset.py">EvaluationDataset</a></code>
- <code title="get /v4/evaluation-datasets">client.evaluation_datasets.<a href="./src/scale_gp/resources/evaluation_datasets/evaluation_datasets.py">list</a>(\*\*<a href="src/scale_gp/types/evaluation_dataset_list_params.py">params</a>) -> <a href="./src/scale_gp/types/evaluation_dataset_list_response.py">SyncPageResponse[EvaluationDatasetListResponse]</a></code>
- <code title="post /v4/evaluation-datasets/{evaluation_dataset_id}/approve-batch">client.evaluation_datasets.<a href="./src/scale_gp/resources/evaluation_datasets/evaluation_datasets.py">approve_batch</a>(evaluation_dataset_id, \*\*<a href="src/scale_gp/types/evaluation_dataset_approve_batch_params.py">params</a>) -> <a href="./src/scale_gp/types/auto_generated_draft_test_case_approve_batch_response.py">AutoGeneratedDraftTestCaseApproveBatchResponse</a></code>
- <code title="post /v4/evaluation-datasets/{evaluation_dataset_id}/publish">client.evaluation_datasets.<a href="./src/scale_gp/resources/evaluation_datasets/evaluation_datasets.py">publish</a>(evaluation_dataset_id, \*\*<a href="src/scale_gp/types/evaluation_dataset_publish_params.py">params</a>) -> <a href="./src/scale_gp/types/publish_evaluation_dataset_draft_response.py">PublishEvaluationDatasetDraftResponse</a></code>
- <code title="delete /v4/evaluation-datasets/{evaluation_dataset_id}">client.evaluation_datasets.<a href="./src/scale_gp/resources/evaluation_datasets/evaluation_datasets.py">remove</a>(evaluation_dataset_id) -> <a href="./src/scale_gp/types/shared/generic_delete_response.py">GenericDeleteResponse</a></code>

## EvaluationDatasetVersions

Types:

```python
from scale_gp.types.evaluation_datasets import (
    EvaluationDatasetVersion,
    PaginatedEvaluationDatasetVersions,
)
```

Methods:

- <code title="post /v4/evaluation-datasets/{evaluation_dataset_id}/evaluation-dataset-versions">client.evaluation_datasets.evaluation_dataset_versions.<a href="./src/scale_gp/resources/evaluation_datasets/evaluation_dataset_versions.py">create</a>(evaluation_dataset_id, \*\*<a href="src/scale_gp/types/evaluation_datasets/evaluation_dataset_version_create_params.py">params</a>) -> <a href="./src/scale_gp/types/evaluation_datasets/evaluation_dataset_version.py">EvaluationDatasetVersion</a></code>
- <code title="get /v4/evaluation-datasets/{evaluation_dataset_id}/evaluation-dataset-versions/{evaluation_dataset_version_id}">client.evaluation_datasets.evaluation_dataset_versions.<a href="./src/scale_gp/resources/evaluation_datasets/evaluation_dataset_versions.py">retrieve</a>(evaluation_dataset_version_id, \*, evaluation_dataset_id) -> <a href="./src/scale_gp/types/evaluation_datasets/evaluation_dataset_version.py">EvaluationDatasetVersion</a></code>
- <code title="get /v4/evaluation-datasets/{evaluation_dataset_id}/evaluation-dataset-versions">client.evaluation_datasets.evaluation_dataset_versions.<a href="./src/scale_gp/resources/evaluation_datasets/evaluation_dataset_versions.py">list</a>(evaluation_dataset_id, \*\*<a href="src/scale_gp/types/evaluation_datasets/evaluation_dataset_version_list_params.py">params</a>) -> <a href="./src/scale_gp/types/evaluation_datasets/evaluation_dataset_version.py">SyncPageResponse[EvaluationDatasetVersion]</a></code>
- <code title="post /v4/evaluation-datasets/{evaluation_dataset_id}/evaluation-dataset-versions/{evaluation_dataset_version_id}/publish">client.evaluation_datasets.evaluation_dataset_versions.<a href="./src/scale_gp/resources/evaluation_datasets/evaluation_dataset_versions.py">publish</a>(evaluation_dataset_version_id, \*, evaluation_dataset_id, \*\*<a href="src/scale_gp/types/evaluation_datasets/evaluation_dataset_version_publish_params.py">params</a>) -> <a href="./src/scale_gp/types/publish_evaluation_dataset_draft_response.py">PublishEvaluationDatasetDraftResponse</a></code>

## TestCases

Types:

```python
from scale_gp.types.evaluation_datasets import (
    ArtifactSchemaGeneration,
    FlexibleChunk,
    FlexibleMessage,
    FlexibleTestCaseSchema,
    GenerationTestCaseSchema,
    PaginatedTestCases,
    TestCase,
    TestCaseBatchResponse,
)
```

Methods:

- <code title="post /v4/evaluation-datasets/{evaluation_dataset_id}/test-cases">client.evaluation_datasets.test_cases.<a href="./src/scale_gp/resources/evaluation_datasets/test_cases/test_cases.py">create</a>(evaluation_dataset_id, \*\*<a href="src/scale_gp/types/evaluation_datasets/test_case_create_params.py">params</a>) -> <a href="./src/scale_gp/types/evaluation_datasets/test_case.py">TestCase</a></code>
- <code title="get /v4/evaluation-datasets/{evaluation_dataset_id}/test-cases/{test_case_id}">client.evaluation_datasets.test_cases.<a href="./src/scale_gp/resources/evaluation_datasets/test_cases/test_cases.py">retrieve</a>(test_case_id, \*, evaluation_dataset_id) -> <a href="./src/scale_gp/types/evaluation_datasets/test_case.py">TestCase</a></code>
- <code title="patch /v4/evaluation-datasets/{evaluation_dataset_id}/test-cases/{test_case_id}">client.evaluation_datasets.test_cases.<a href="./src/scale_gp/resources/evaluation_datasets/test_cases/test_cases.py">update</a>(test_case_id, \*, evaluation_dataset_id, \*\*<a href="src/scale_gp/types/evaluation_datasets/test_case_update_params.py">params</a>) -> <a href="./src/scale_gp/types/evaluation_datasets/test_case.py">TestCase</a></code>
- <code title="get /v4/evaluation-datasets/{evaluation_dataset_id}/test-cases">client.evaluation_datasets.test_cases.<a href="./src/scale_gp/resources/evaluation_datasets/test_cases/test_cases.py">list</a>(evaluation_dataset_id, \*\*<a href="src/scale_gp/types/evaluation_datasets/test_case_list_params.py">params</a>) -> <a href="./src/scale_gp/types/evaluation_datasets/test_case.py">SyncPageResponse[TestCase]</a></code>
- <code title="delete /v4/evaluation-datasets/{evaluation_dataset_id}/test-cases/{test_case_id}">client.evaluation_datasets.test_cases.<a href="./src/scale_gp/resources/evaluation_datasets/test_cases/test_cases.py">delete</a>(test_case_id, \*, evaluation_dataset_id) -> <a href="./src/scale_gp/types/shared/generic_delete_response.py">GenericDeleteResponse</a></code>
- <code title="post /v4/evaluation-datasets/{evaluation_dataset_id}/test-cases/batch">client.evaluation_datasets.test_cases.<a href="./src/scale_gp/resources/evaluation_datasets/test_cases/test_cases.py">batch</a>(evaluation_dataset_id, \*\*<a href="src/scale_gp/types/evaluation_datasets/test_case_batch_params.py">params</a>) -> <a href="./src/scale_gp/types/evaluation_datasets/test_case_batch_response.py">TestCaseBatchResponse</a></code>

### History

Methods:

- <code title="get /v4/evaluation-datasets/{evaluation_dataset_id}/test-cases/{test_case_id}/history/{num}">client.evaluation_datasets.test_cases.history.<a href="./src/scale_gp/resources/evaluation_datasets/test_cases/history.py">retrieve</a>(num, \*, evaluation_dataset_id, test_case_id) -> <a href="./src/scale_gp/types/evaluation_datasets/test_case.py">TestCase</a></code>
- <code title="get /v4/evaluation-datasets/{evaluation_dataset_id}/test-cases/history/{num}">client.evaluation_datasets.test_cases.history.<a href="./src/scale_gp/resources/evaluation_datasets/test_cases/history.py">list</a>(num, \*, evaluation_dataset_id, \*\*<a href="src/scale_gp/types/evaluation_datasets/test_cases/history_list_params.py">params</a>) -> <a href="./src/scale_gp/types/evaluation_datasets/test_case.py">SyncPageResponse[TestCase]</a></code>
- <code title="delete /v4/evaluation-datasets/{evaluation_dataset_id}/test-cases/{test_case_id}/history">client.evaluation_datasets.test_cases.history.<a href="./src/scale_gp/resources/evaluation_datasets/test_cases/history.py">delete</a>(test_case_id, \*, evaluation_dataset_id) -> <a href="./src/scale_gp/types/shared/generic_delete_response.py">GenericDeleteResponse</a></code>

## AutogeneratedDraftTestCases

Types:

```python
from scale_gp.types.evaluation_datasets import (
    ApproveAutoGeneratedDraftTestCaseResponse,
    AutoGeneratedDraftTestCase,
    AutoGeneratedDraftTestCasesList,
    AutogeneratedDraftTestCaseListResponse,
)
```

Methods:

- <code title="post /v4/evaluation-datasets/{evaluation_dataset_id}/autogenerated-draft-test-cases">client.evaluation_datasets.autogenerated_draft_test_cases.<a href="./src/scale_gp/resources/evaluation_datasets/autogenerated_draft_test_cases.py">create</a>(evaluation_dataset_id, \*\*<a href="src/scale_gp/types/evaluation_datasets/autogenerated_draft_test_case_create_params.py">params</a>) -> <a href="./src/scale_gp/types/evaluation_datasets/auto_generated_draft_test_case.py">AutoGeneratedDraftTestCase</a></code>
- <code title="get /v4/evaluation-datasets/{evaluation_dataset_id}/autogenerated-draft-test-cases/{autogenerated_draft_test_case_id}">client.evaluation_datasets.autogenerated_draft_test_cases.<a href="./src/scale_gp/resources/evaluation_datasets/autogenerated_draft_test_cases.py">retrieve</a>(autogenerated_draft_test_case_id, \*, evaluation_dataset_id) -> <a href="./src/scale_gp/types/evaluation_datasets/auto_generated_draft_test_case.py">AutoGeneratedDraftTestCase</a></code>
- <code title="patch /v4/evaluation-datasets/{evaluation_dataset_id}/autogenerated-draft-test-cases/{autogenerated_draft_test_case_id}">client.evaluation_datasets.autogenerated_draft_test_cases.<a href="./src/scale_gp/resources/evaluation_datasets/autogenerated_draft_test_cases.py">update</a>(autogenerated_draft_test_case_id, \*, evaluation_dataset_id, \*\*<a href="src/scale_gp/types/evaluation_datasets/autogenerated_draft_test_case_update_params.py">params</a>) -> <a href="./src/scale_gp/types/evaluation_datasets/auto_generated_draft_test_case.py">AutoGeneratedDraftTestCase</a></code>
- <code title="get /v4/evaluation-datasets/{evaluation_dataset_id}/autogenerated-draft-test-cases">client.evaluation_datasets.autogenerated_draft_test_cases.<a href="./src/scale_gp/resources/evaluation_datasets/autogenerated_draft_test_cases.py">list</a>(evaluation_dataset_id, \*\*<a href="src/scale_gp/types/evaluation_datasets/autogenerated_draft_test_case_list_params.py">params</a>) -> <a href="./src/scale_gp/types/evaluation_datasets/autogenerated_draft_test_case_list_response.py">SyncPageResponse[AutogeneratedDraftTestCaseListResponse]</a></code>
- <code title="delete /v4/evaluation-datasets/{evaluation_dataset_id}/autogenerated-draft-test-cases/{autogenerated_draft_test_case_id}">client.evaluation_datasets.autogenerated_draft_test_cases.<a href="./src/scale_gp/resources/evaluation_datasets/autogenerated_draft_test_cases.py">delete</a>(autogenerated_draft_test_case_id, \*, evaluation_dataset_id) -> <a href="./src/scale_gp/types/shared/generic_delete_response.py">GenericDeleteResponse</a></code>
- <code title="post /v4/evaluation-datasets/{evaluation_dataset_id}/autogenerated-draft-test-cases/{autogenerated_draft_test_case_id}/approve">client.evaluation_datasets.autogenerated_draft_test_cases.<a href="./src/scale_gp/resources/evaluation_datasets/autogenerated_draft_test_cases.py">approve</a>(autogenerated_draft_test_case_id, \*, evaluation_dataset_id, \*\*<a href="src/scale_gp/types/evaluation_datasets/autogenerated_draft_test_case_approve_params.py">params</a>) -> <a href="./src/scale_gp/types/evaluation_datasets/approve_auto_generated_draft_test_case_response.py">ApproveAutoGeneratedDraftTestCaseResponse</a></code>

## GenerationJobs

Types:

```python
from scale_gp.types.evaluation_datasets import (
    EvaluationDatasetGenerationJob,
    EvaluationDatasetGenerationJobResponse,
    EvaluationDatasetGenerationJobsList,
    GenerationJobCancelResponse,
)
```

Methods:

- <code title="post /v4/evaluation-datasets/{evaluation_dataset_id}/generation-jobs">client.evaluation_datasets.generation_jobs.<a href="./src/scale_gp/resources/evaluation_datasets/generation_jobs.py">create</a>(evaluation_dataset_id, \*\*<a href="src/scale_gp/types/evaluation_datasets/generation_job_create_params.py">params</a>) -> <a href="./src/scale_gp/types/evaluation_datasets/evaluation_dataset_generation_job_response.py">EvaluationDatasetGenerationJobResponse</a></code>
- <code title="get /v4/evaluation-datasets/{evaluation_dataset_id}/generation-jobs/{generation_job_id}">client.evaluation_datasets.generation_jobs.<a href="./src/scale_gp/resources/evaluation_datasets/generation_jobs.py">retrieve</a>(generation_job_id, \*, evaluation_dataset_id) -> <a href="./src/scale_gp/types/evaluation_datasets/evaluation_dataset_generation_job.py">EvaluationDatasetGenerationJob</a></code>
- <code title="get /v4/evaluation-datasets/{evaluation_dataset_id}/generation-jobs">client.evaluation_datasets.generation_jobs.<a href="./src/scale_gp/resources/evaluation_datasets/generation_jobs.py">list</a>(evaluation_dataset_id) -> <a href="./src/scale_gp/types/evaluation_datasets/evaluation_dataset_generation_job.py">SyncGenerationJobsPagination[EvaluationDatasetGenerationJob]</a></code>
- <code title="post /v4/evaluation-datasets/{evaluation_dataset_id}/generation-jobs/{generation_job_id}/cancel">client.evaluation_datasets.generation_jobs.<a href="./src/scale_gp/resources/evaluation_datasets/generation_jobs.py">cancel</a>(generation_job_id, \*, evaluation_dataset_id) -> <a href="./src/scale_gp/types/evaluation_datasets/generation_job_cancel_response.py">object</a></code>

# StudioProjects

Types:

```python
from scale_gp.types import PaginatedStudioProjects, StudioProject
```

Methods:

- <code title="post /v4/studio-projects">client.studio_projects.<a href="./src/scale_gp/resources/studio_projects.py">create</a>(\*\*<a href="src/scale_gp/types/studio_project_create_params.py">params</a>) -> <a href="./src/scale_gp/types/studio_project.py">StudioProject</a></code>
- <code title="get /v4/studio-projects/{studio_project_id}">client.studio_projects.<a href="./src/scale_gp/resources/studio_projects.py">retrieve</a>(studio_project_id) -> <a href="./src/scale_gp/types/studio_project.py">StudioProject</a></code>
- <code title="patch /v4/studio-projects/{studio_project_id}">client.studio_projects.<a href="./src/scale_gp/resources/studio_projects.py">update</a>(studio_project_id, \*\*<a href="src/scale_gp/types/studio_project_update_params.py">params</a>) -> <a href="./src/scale_gp/types/studio_project.py">StudioProject</a></code>
- <code title="get /v4/studio-projects">client.studio_projects.<a href="./src/scale_gp/resources/studio_projects.py">list</a>(\*\*<a href="src/scale_gp/types/studio_project_list_params.py">params</a>) -> <a href="./src/scale_gp/types/studio_project.py">SyncPageResponse[StudioProject]</a></code>
- <code title="delete /v4/studio-projects/{studio_project_id}">client.studio_projects.<a href="./src/scale_gp/resources/studio_projects.py">delete</a>(studio_project_id) -> <a href="./src/scale_gp/types/shared/generic_delete_response.py">GenericDeleteResponse</a></code>

# ApplicationSpecs

Types:

```python
from scale_gp.types import ApplicationSpec, PaginatedApplicationSpecs
```

Methods:

- <code title="post /v4/application-specs">client.application_specs.<a href="./src/scale_gp/resources/application_specs.py">create</a>(\*\*<a href="src/scale_gp/types/application_spec_create_params.py">params</a>) -> <a href="./src/scale_gp/types/application_spec.py">ApplicationSpec</a></code>
- <code title="get /v4/application-specs/{application_spec_id}">client.application_specs.<a href="./src/scale_gp/resources/application_specs.py">retrieve</a>(application_spec_id) -> <a href="./src/scale_gp/types/application_spec.py">ApplicationSpec</a></code>
- <code title="patch /v4/application-specs/{application_spec_id}">client.application_specs.<a href="./src/scale_gp/resources/application_specs.py">update</a>(application_spec_id, \*\*<a href="src/scale_gp/types/application_spec_update_params.py">params</a>) -> <a href="./src/scale_gp/types/application_spec.py">ApplicationSpec</a></code>
- <code title="get /v4/application-specs">client.application_specs.<a href="./src/scale_gp/resources/application_specs.py">list</a>(\*\*<a href="src/scale_gp/types/application_spec_list_params.py">params</a>) -> <a href="./src/scale_gp/types/application_spec.py">SyncPageResponse[ApplicationSpec]</a></code>
- <code title="delete /v4/application-specs/{application_spec_id}">client.application_specs.<a href="./src/scale_gp/resources/application_specs.py">delete</a>(application_spec_id) -> <a href="./src/scale_gp/types/shared/generic_delete_response.py">GenericDeleteResponse</a></code>

# Questions

Types:

```python
from scale_gp.types import PaginatedQuestions, Question
```

Methods:

- <code title="post /v4/questions">client.questions.<a href="./src/scale_gp/resources/questions.py">create</a>(\*\*<a href="src/scale_gp/types/question_create_params.py">params</a>) -> <a href="./src/scale_gp/types/question.py">Question</a></code>
- <code title="get /v4/questions/{question_id}">client.questions.<a href="./src/scale_gp/resources/questions.py">retrieve</a>(question_id) -> <a href="./src/scale_gp/types/question.py">Question</a></code>
- <code title="get /v4/questions">client.questions.<a href="./src/scale_gp/resources/questions.py">list</a>(\*\*<a href="src/scale_gp/types/question_list_params.py">params</a>) -> <a href="./src/scale_gp/types/question.py">SyncPageResponse[Question]</a></code>

# ModelTemplates

Types:

```python
from scale_gp.types import (
    ModelTemplate,
    PaginatedModelTemplates,
    ParameterSchema,
    ParameterSchemaField,
)
```

Methods:

- <code title="post /v4/model-templates">client.model_templates.<a href="./src/scale_gp/resources/model_templates.py">create</a>(\*\*<a href="src/scale_gp/types/model_template_create_params.py">params</a>) -> <a href="./src/scale_gp/types/model_template.py">ModelTemplate</a></code>
- <code title="get /v4/model-templates/{model_template_id}">client.model_templates.<a href="./src/scale_gp/resources/model_templates.py">retrieve</a>(model_template_id) -> <a href="./src/scale_gp/types/model_template.py">ModelTemplate</a></code>
- <code title="get /v4/model-templates">client.model_templates.<a href="./src/scale_gp/resources/model_templates.py">list</a>(\*\*<a href="src/scale_gp/types/model_template_list_params.py">params</a>) -> <a href="./src/scale_gp/types/model_template.py">SyncPageResponse[ModelTemplate]</a></code>
- <code title="delete /v4/model-templates/{model_template_id}">client.model_templates.<a href="./src/scale_gp/resources/model_templates.py">delete</a>(model_template_id) -> <a href="./src/scale_gp/types/shared/generic_delete_response.py">GenericDeleteResponse</a></code>

# FineTuningJobs

Types:

```python
from scale_gp.types import FineTuningJob, FineTuningJobEvent, PaginatedFineTuningJobs
```

Methods:

- <code title="post /v4/fine-tuning-jobs">client.fine_tuning_jobs.<a href="./src/scale_gp/resources/fine_tuning_jobs/fine_tuning_jobs.py">create</a>(\*\*<a href="src/scale_gp/types/fine_tuning_job_create_params.py">params</a>) -> <a href="./src/scale_gp/types/fine_tuning_job.py">FineTuningJob</a></code>
- <code title="get /v4/fine-tuning-jobs/{fine_tuning_job_id}">client.fine_tuning_jobs.<a href="./src/scale_gp/resources/fine_tuning_jobs/fine_tuning_jobs.py">retrieve</a>(fine_tuning_job_id) -> <a href="./src/scale_gp/types/fine_tuning_job.py">FineTuningJob</a></code>
- <code title="get /v4/fine-tuning-jobs">client.fine_tuning_jobs.<a href="./src/scale_gp/resources/fine_tuning_jobs/fine_tuning_jobs.py">list</a>(\*\*<a href="src/scale_gp/types/fine_tuning_job_list_params.py">params</a>) -> <a href="./src/scale_gp/types/fine_tuning_job.py">SyncPageResponse[FineTuningJob]</a></code>
- <code title="delete /v4/fine-tuning-jobs/{fine_tuning_job_id}">client.fine_tuning_jobs.<a href="./src/scale_gp/resources/fine_tuning_jobs/fine_tuning_jobs.py">delete</a>(fine_tuning_job_id) -> <a href="./src/scale_gp/types/shared/generic_delete_response.py">GenericDeleteResponse</a></code>

## Events

Methods:

- <code title="get /v4/fine-tuning-jobs/{fine_tuning_job_id}/events">client.fine_tuning_jobs.events.<a href="./src/scale_gp/resources/fine_tuning_jobs/events.py">list</a>(fine_tuning_job_id) -> <a href="./src/scale_gp/types/fine_tuning_job_event.py">SyncTopLevelArray[FineTuningJobEvent]</a></code>

# TrainingDatasets

Types:

```python
from scale_gp.types import PaginatedTrainingDatasets, TrainingDataset, TrainingDatasetGenerationItem
```

Methods:

- <code title="post /v4/training-datasets">client.training_datasets.<a href="./src/scale_gp/resources/training_datasets/training_datasets.py">create</a>(\*\*<a href="src/scale_gp/types/training_dataset_create_params.py">params</a>) -> <a href="./src/scale_gp/types/training_dataset.py">TrainingDataset</a></code>
- <code title="get /v4/training-datasets/{training_dataset_id}">client.training_datasets.<a href="./src/scale_gp/resources/training_datasets/training_datasets.py">retrieve</a>(training_dataset_id) -> <a href="./src/scale_gp/types/training_dataset.py">TrainingDataset</a></code>
- <code title="get /v4/training-datasets">client.training_datasets.<a href="./src/scale_gp/resources/training_datasets/training_datasets.py">list</a>(\*\*<a href="src/scale_gp/types/training_dataset_list_params.py">params</a>) -> <a href="./src/scale_gp/types/training_dataset.py">SyncPageResponse[TrainingDataset]</a></code>
- <code title="delete /v4/training-datasets/{training_dataset_id}">client.training_datasets.<a href="./src/scale_gp/resources/training_datasets/training_datasets.py">delete</a>(training_dataset_id) -> <a href="./src/scale_gp/types/shared/generic_delete_response.py">GenericDeleteResponse</a></code>

## Contents

Methods:

- <code title="get /v4/training-datasets/{training_dataset_id}/contents">client.training_datasets.contents.<a href="./src/scale_gp/resources/training_datasets/contents.py">list</a>(training_dataset_id) -> <a href="./src/scale_gp/types/training_dataset_generation_item.py">SyncTopLevelArray[TrainingDatasetGenerationItem]</a></code>

# DeploymentPackages

Types:

```python
from scale_gp.types import DeploymentPackageJob, InstallDeploymentPackageResponse
```

Methods:

- <code title="post /v4/deployment-packages/{account_id}/install">client.deployment_packages.<a href="./src/scale_gp/resources/deployment_packages.py">install</a>(account_id, \*\*<a href="src/scale_gp/types/deployment_package_install_params.py">params</a>) -> <a href="./src/scale_gp/types/install_deployment_package_response.py">InstallDeploymentPackageResponse</a></code>
- <code title="post /v4/deployment-packages/{account_id}/install_async">client.deployment_packages.<a href="./src/scale_gp/resources/deployment_packages.py">install_async</a>(account_id, \*\*<a href="src/scale_gp/types/deployment_package_install_async_params.py">params</a>) -> <a href="./src/scale_gp/types/deployment_package_job.py">DeploymentPackageJob</a></code>

# ApplicationVariants

Types:

```python
from scale_gp.types import (
    ApplicationAgentGraphNode,
    ApplicationConfiguration,
    ApplicationEdge,
    ApplicationNode,
    PaginatedApplicationVariants,
    ApplicationVariantCreateResponse,
    ApplicationVariantRetrieveResponse,
    ApplicationVariantListResponse,
    ApplicationVariantPatchResponse,
    ApplicationVariantProcessResponse,
)
```

Methods:

- <code title="post /v4/application-variants">client.application_variants.<a href="./src/scale_gp/resources/application_variants.py">create</a>(\*\*<a href="src/scale_gp/types/application_variant_create_params.py">params</a>) -> <a href="./src/scale_gp/types/application_variant_create_response.py">ApplicationVariantCreateResponse</a></code>
- <code title="get /v4/application-variants/{application_variant_id}">client.application_variants.<a href="./src/scale_gp/resources/application_variants.py">retrieve</a>(application_variant_id) -> <a href="./src/scale_gp/types/application_variant_retrieve_response.py">ApplicationVariantRetrieveResponse</a></code>
- <code title="get /v4/application-variants">client.application_variants.<a href="./src/scale_gp/resources/application_variants.py">list</a>(\*\*<a href="src/scale_gp/types/application_variant_list_params.py">params</a>) -> <a href="./src/scale_gp/types/application_variant_list_response.py">SyncPageResponse[ApplicationVariantListResponse]</a></code>
- <code title="delete /v4/application-variants/{application_variant_id}">client.application_variants.<a href="./src/scale_gp/resources/application_variants.py">delete</a>(application_variant_id) -> <a href="./src/scale_gp/types/shared/generic_delete_response.py">GenericDeleteResponse</a></code>
- <code title="patch /v4/application-variants/{application_variant_id}">client.application_variants.<a href="./src/scale_gp/resources/application_variants.py">patch</a>(application_variant_id, \*\*<a href="src/scale_gp/types/application_variant_patch_params.py">params</a>) -> <a href="./src/scale_gp/types/application_variant_patch_response.py">ApplicationVariantPatchResponse</a></code>
- <code title="post /v4/applications/{application_variant_id}/process">client.application_variants.<a href="./src/scale_gp/resources/application_variants.py">process</a>(application_variant_id, \*\*<a href="src/scale_gp/types/application_variant_process_params.py">params</a>) -> <a href="./src/scale_gp/types/application_variant_process_response.py">object</a></code>

# ApplicationDeployments

Types:

```python
from scale_gp.types import ApplicationDeployment, PaginatedApplicationDeployments
```

Methods:

- <code title="post /v4/application-deployments">client.application_deployments.<a href="./src/scale_gp/resources/application_deployments.py">create</a>(\*\*<a href="src/scale_gp/types/application_deployment_create_params.py">params</a>) -> <a href="./src/scale_gp/types/application_deployment.py">ApplicationDeployment</a></code>
- <code title="get /v4/application-deployments/{application_deployment_id}">client.application_deployments.<a href="./src/scale_gp/resources/application_deployments.py">retrieve</a>(application_deployment_id) -> <a href="./src/scale_gp/types/application_deployment.py">ApplicationDeployment</a></code>
- <code title="patch /v4/application-deployments/{application_deployment_id}">client.application_deployments.<a href="./src/scale_gp/resources/application_deployments.py">update</a>(application_deployment_id, \*\*<a href="src/scale_gp/types/application_deployment_update_params.py">params</a>) -> <a href="./src/scale_gp/types/application_deployment.py">ApplicationDeployment</a></code>
- <code title="get /v4/application-deployments">client.application_deployments.<a href="./src/scale_gp/resources/application_deployments.py">list</a>(\*\*<a href="src/scale_gp/types/application_deployment_list_params.py">params</a>) -> <a href="./src/scale_gp/types/application_deployment.py">SyncPageResponse[ApplicationDeployment]</a></code>

# ApplicationVariantReports

Types:

```python
from scale_gp.types import ApplicationVariantWithScores, ApplicationVariantWithScoresAndViews
```

Methods:

- <code title="post /v4/application-variant-reports">client.application_variant_reports.<a href="./src/scale_gp/resources/application_variant_reports.py">create</a>(\*\*<a href="src/scale_gp/types/application_variant_report_create_params.py">params</a>) -> <a href="./src/scale_gp/types/application_variant_with_scores.py">ApplicationVariantWithScores</a></code>
- <code title="get /v4/application-variant-reports/{application_variant_report_id}">client.application_variant_reports.<a href="./src/scale_gp/resources/application_variant_reports.py">retrieve</a>(application_variant_report_id, \*\*<a href="src/scale_gp/types/application_variant_report_retrieve_params.py">params</a>) -> <a href="./src/scale_gp/types/application_variant_with_scores_and_views.py">ApplicationVariantWithScoresAndViews</a></code>
- <code title="get /v4/application-variant-reports">client.application_variant_reports.<a href="./src/scale_gp/resources/application_variant_reports.py">list</a>(\*\*<a href="src/scale_gp/types/application_variant_report_list_params.py">params</a>) -> <a href="./src/scale_gp/types/application_variant_with_scores_and_views.py">SyncPageResponse[ApplicationVariantWithScoresAndViews]</a></code>

# ApplicationTestCaseOutputs

Types:

```python
from scale_gp.types import (
    ApplicationMetricScore,
    ApplicationTestCaseOutput,
    PaginatedApplicationTestCaseOutputWithViews,
    ResultSchemaFlexible,
    ApplicationTestCaseOutputRetrieveResponse,
    ApplicationTestCaseOutputListResponse,
    ApplicationTestCaseOutputBatchResponse,
)
```

Methods:

- <code title="get /v4/application-test-case-outputs/{application_test_case_output_id}">client.application_test_case_outputs.<a href="./src/scale_gp/resources/application_test_case_outputs.py">retrieve</a>(application_test_case_output_id, \*\*<a href="src/scale_gp/types/application_test_case_output_retrieve_params.py">params</a>) -> <a href="./src/scale_gp/types/application_test_case_output_retrieve_response.py">ApplicationTestCaseOutputRetrieveResponse</a></code>
- <code title="get /v4/application-test-case-outputs">client.application_test_case_outputs.<a href="./src/scale_gp/resources/application_test_case_outputs.py">list</a>(\*\*<a href="src/scale_gp/types/application_test_case_output_list_params.py">params</a>) -> <a href="./src/scale_gp/types/application_test_case_output_list_response.py">SyncPageResponse[ApplicationTestCaseOutputListResponse]</a></code>
- <code title="post /v4/application-test-case-outputs/batch">client.application_test_case_outputs.<a href="./src/scale_gp/resources/application_test_case_outputs.py">batch</a>(\*\*<a href="src/scale_gp/types/application_test_case_output_batch_params.py">params</a>) -> <a href="./src/scale_gp/types/application_test_case_output_batch_response.py">ApplicationTestCaseOutputBatchResponse</a></code>

# ApplicationSchemas

Types:

```python
from scale_gp.types import ApplicationNodeSchemaRegistryRecord, ApplicationSchemaRetrieveResponse
```

Methods:

- <code title="get /v4/application-schemas">client.application_schemas.<a href="./src/scale_gp/resources/application_schemas.py">retrieve</a>(\*\*<a href="src/scale_gp/types/application_schema_retrieve_params.py">params</a>) -> <a href="./src/scale_gp/types/application_schema_retrieve_response.py">ApplicationSchemaRetrieveResponse</a></code>

# Interactions

Types:

```python
from scale_gp.types import InteractionCreateResponse
```

Methods:

- <code title="post /v4/interactions/">client.interactions.<a href="./src/scale_gp/resources/interactions.py">create</a>(\*\*<a href="src/scale_gp/types/interaction_create_params.py">params</a>) -> <a href="./src/scale_gp/types/interaction_create_response.py">InteractionCreateResponse</a></code>

# Applications

Types:

```python
from scale_gp.types import (
    ApplicationFile,
    ChatThread,
    Dashboard,
    ScalarData,
    TimeseriesData,
    ApplicationProcessResponse,
    ApplicationUploadFilesResponse,
    ApplicationValidateResponse,
)
```

Methods:

- <code title="post /v4/applications/process">client.applications.<a href="./src/scale_gp/resources/applications/applications.py">process</a>(\*\*<a href="src/scale_gp/types/application_process_params.py">params</a>) -> <a href="./src/scale_gp/types/application_process_response.py">object</a></code>
- <code title="post /v4/applications/upload-files">client.applications.<a href="./src/scale_gp/resources/applications/applications.py">upload_files</a>(\*\*<a href="src/scale_gp/types/application_upload_files_params.py">params</a>) -> <a href="./src/scale_gp/types/application_upload_files_response.py">ApplicationUploadFilesResponse</a></code>
- <code title="post /v4/applications/validate">client.applications.<a href="./src/scale_gp/resources/applications/applications.py">validate</a>(\*\*<a href="src/scale_gp/types/application_validate_params.py">params</a>) -> <a href="./src/scale_gp/types/application_validate_response.py">object</a></code>

## ChatThreads

Types:

```python
from scale_gp.types.applications import ChatThreadHistory
```

Methods:

- <code title="get /v4/applications/{application_variant_id}/threads">client.applications.chat_threads.<a href="./src/scale_gp/resources/applications/chat_threads/chat_threads.py">list</a>(application_variant_id) -> <a href="./src/scale_gp/types/chat_thread.py">SyncTopLevelArray[ChatThread]</a></code>

### Messages

Types:

```python
from scale_gp.types.applications.chat_threads import ChatThreadFeedback
```

## Dashboards

Methods:

- <code title="get /v4/applications/{application_spec_id}/dashboards/{dashboard_id}">client.applications.dashboards.<a href="./src/scale_gp/resources/applications/dashboards.py">retrieve</a>(dashboard_id, \*, application_spec_id) -> <a href="./src/scale_gp/types/dashboard.py">Dashboard</a></code>

## Metrics

### Scalar

Methods:

- <code title="get /v4/applications/{application_spec_id}/metrics/scalar/{metric_id}">client.applications.metrics.scalar.<a href="./src/scale_gp/resources/applications/metrics/scalar.py">retrieve</a>(metric_id, \*, application_spec_id, \*\*<a href="src/scale_gp/types/applications/metrics/scalar_retrieve_params.py">params</a>) -> <a href="./src/scale_gp/types/scalar_data.py">ScalarData</a></code>

### Timeseries

Methods:

- <code title="get /v4/applications/{application_spec_id}/metrics/timeseries/{metric_id}">client.applications.metrics.timeseries.<a href="./src/scale_gp/resources/applications/metrics/timeseries.py">retrieve</a>(metric_id, \*, application_spec_id, \*\*<a href="src/scale_gp/types/applications/metrics/timesery_retrieve_params.py">params</a>) -> <a href="./src/scale_gp/types/timeseries_data.py">TimeseriesData</a></code>

# ApplicationThreads

Types:

```python
from scale_gp.types import ApplicationThreadProcessResponse
```

Methods:

- <code title="post /v4/applications/{application_variant_id}/threads/{thread_id}/process">client.application_threads.<a href="./src/scale_gp/resources/application_threads.py">process</a>(thread_id, \*, application_variant_id, \*\*<a href="src/scale_gp/types/application_thread_process_params.py">params</a>) -> <a href="./src/scale_gp/types/application_thread_process_response.py">object</a></code>

# ChatThreads

Types:

```python
from scale_gp.types import ChatThreadDeleteResponse
```

Methods:

- <code title="patch /v4/threads/{thread_id}">client.chat_threads.<a href="./src/scale_gp/resources/chat_threads/chat_threads.py">update</a>(thread_id, \*\*<a href="src/scale_gp/types/chat_thread_update_params.py">params</a>) -> <a href="./src/scale_gp/types/chat_thread.py">ChatThread</a></code>
- <code title="delete /v4/threads/{thread_id}">client.chat_threads.<a href="./src/scale_gp/resources/chat_threads/chat_threads.py">delete</a>(thread_id) -> <a href="./src/scale_gp/types/chat_thread_delete_response.py">object</a></code>

## Messages

Types:

```python
from scale_gp.types.chat_threads import MessageUpdateResponse
```

Methods:

- <code title="get /v4/threads/{thread_id}/messages">client.chat_threads.messages.<a href="./src/scale_gp/resources/chat_threads/messages/messages.py">retrieve</a>(thread_id, \*\*<a href="src/scale_gp/types/chat_threads/message_retrieve_params.py">params</a>) -> <a href="./src/scale_gp/types/applications/chat_thread_history.py">ChatThreadHistory</a></code>
- <code title="patch /v4/threads/{thread_id}/messages/{application_interaction_id}">client.chat_threads.messages.<a href="./src/scale_gp/resources/chat_threads/messages/messages.py">update</a>(application_interaction_id, \*, thread_id, \*\*<a href="src/scale_gp/types/chat_threads/message_update_params.py">params</a>) -> <a href="./src/scale_gp/types/chat_threads/message_update_response.py">MessageUpdateResponse</a></code>

### Feedback

Types:

```python
from scale_gp.types.chat_threads.messages import FeedbackDeleteResponse
```

Methods:

- <code title="delete /v4/threads/{thread_id}/messages/{application_interaction_id}/feedback">client.chat_threads.messages.feedback.<a href="./src/scale_gp/resources/chat_threads/messages/feedback.py">delete</a>(application_interaction_id, \*, thread_id) -> <a href="./src/scale_gp/types/chat_threads/messages/feedback_delete_response.py">object</a></code>

# Themes

Types:

```python
from scale_gp.types import PaginatedThemes, Theme
```

Methods:

- <code title="post /v4/themes">client.themes.<a href="./src/scale_gp/resources/themes.py">create</a>(\*\*<a href="src/scale_gp/types/theme_create_params.py">params</a>) -> <a href="./src/scale_gp/types/theme.py">Theme</a></code>
- <code title="get /v4/themes/{theme_id}">client.themes.<a href="./src/scale_gp/resources/themes.py">retrieve</a>(theme_id) -> <a href="./src/scale_gp/types/theme.py">Theme</a></code>
- <code title="get /v4/themes">client.themes.<a href="./src/scale_gp/resources/themes.py">list</a>(\*\*<a href="src/scale_gp/types/theme_list_params.py">params</a>) -> <a href="./src/scale_gp/types/theme.py">SyncPageResponse[Theme]</a></code>

# Beta

## Completions

Types:

```python
from scale_gp.types.beta import (
    Completion,
    CompletionChunk,
    CompletionRequest,
    CompletionCreateResponse,
)
```

Methods:

- <code title="post /v4/beta/completions">client.beta.completions.<a href="./src/scale_gp/resources/beta/completions.py">create</a>(\*\*<a href="src/scale_gp/types/beta/completion_create_params.py">params</a>) -> <a href="./src/scale_gp/types/beta/completion_create_response.py">CompletionCreateResponse</a></code>

## Chat

### Completions

Types:

```python
from scale_gp.types.beta.chat import (
    ChatCompletion,
    ChatCompletionChunk,
    ChatCompletionRequest,
    CompletionCreateResponse,
)
```

Methods:

- <code title="post /v4/beta/chat/completions">client.beta.chat.completions.<a href="./src/scale_gp/resources/beta/chat/completions.py">create</a>(\*\*<a href="src/scale_gp/types/beta/chat/completion_create_params.py">params</a>) -> <a href="./src/scale_gp/types/beta/chat/completion_create_response.py">CompletionCreateResponse</a></code>

## Files

Types:

```python
from scale_gp.types.beta import File, FileDelete, FileList
```

Methods:

- <code title="post /v4/beta/files">client.beta.files.<a href="./src/scale_gp/resources/beta/files.py">create</a>(\*\*<a href="src/scale_gp/types/beta/file_create_params.py">params</a>) -> <a href="./src/scale_gp/types/beta/file.py">File</a></code>
- <code title="get /v4/beta/files/{file_id}">client.beta.files.<a href="./src/scale_gp/resources/beta/files.py">retrieve</a>(file_id) -> <a href="./src/scale_gp/types/beta/file.py">File</a></code>
- <code title="get /v4/beta/files">client.beta.files.<a href="./src/scale_gp/resources/beta/files.py">list</a>(\*\*<a href="src/scale_gp/types/beta/file_list_params.py">params</a>) -> <a href="./src/scale_gp/types/beta/file.py">SyncCursorPage[File]</a></code>
- <code title="delete /v4/beta/files/{file_id}">client.beta.files.<a href="./src/scale_gp/resources/beta/files.py">delete</a>(file_id) -> <a href="./src/scale_gp/types/beta/file_delete.py">FileDelete</a></code>
- <code title="get /v4/beta/files/{file_id}/content">client.beta.files.<a href="./src/scale_gp/resources/beta/files.py">content</a>(file_id) -> BinaryAPIResponse</code>

# ModelServers

Types:

```python
from scale_gp.types import ModelServerRollbackResponse, ModelServerUpdateBackendResponse
```

Methods:

- <code title="post /v4/serving">client.model_servers.<a href="./src/scale_gp/resources/model_servers/model_servers.py">create</a>(\*\*<a href="src/scale_gp/types/model_server_create_params.py">params</a>) -> <a href="./src/scale_gp/types/shared/model_server_info.py">ModelServerInfo</a></code>
- <code title="get /v4/serving/{model_server_id}">client.model_servers.<a href="./src/scale_gp/resources/model_servers/model_servers.py">retrieve</a>(model_server_id) -> <a href="./src/scale_gp/types/shared/model_server_info.py">ModelServerInfo</a></code>
- <code title="get /v4/serving">client.model_servers.<a href="./src/scale_gp/resources/model_servers/model_servers.py">list</a>() -> <a href="./src/scale_gp/types/shared/model_server_info.py">SyncTopLevelArray[ModelServerInfo]</a></code>
- <code title="post /v4/serving/{model_server_id}/execute">client.model_servers.<a href="./src/scale_gp/resources/model_servers/model_servers.py">execute</a>(model_server_id, \*\*<a href="src/scale_gp/types/model_server_execute_params.py">params</a>) -> <a href="./src/scale_gp/types/generic_model_response.py">GenericModelResponse</a></code>
- <code title="post /v4/serving/{model_server_id}/rollback">client.model_servers.<a href="./src/scale_gp/resources/model_servers/model_servers.py">rollback</a>(model_server_id) -> <a href="./src/scale_gp/types/model_server_rollback_response.py">ModelServerRollbackResponse</a></code>
- <code title="put /v4/serving/{model_server_id}/backend">client.model_servers.<a href="./src/scale_gp/resources/model_servers/model_servers.py">update_backend</a>(model_server_id, \*\*<a href="src/scale_gp/types/model_server_update_backend_params.py">params</a>) -> <a href="./src/scale_gp/types/model_server_update_backend_response.py">ModelServerUpdateBackendResponse</a></code>

## Deployment

Types:

```python
from scale_gp.types.model_servers import DeploymentRetrieveResponse
```

Methods:

- <code title="get /v4/serving/{model_server_id}/deployment">client.model_servers.deployment.<a href="./src/scale_gp/resources/model_servers/deployment.py">retrieve</a>(model_server_id) -> <a href="./src/scale_gp/types/model_servers/deployment_retrieve_response.py">DeploymentRetrieveResponse</a></code>

# Alias

Methods:

- <code title="get /v4/serving/a/{alias}">client.alias.<a href="./src/scale_gp/resources/alias.py">retrieve</a>(alias) -> <a href="./src/scale_gp/types/shared/model_server_info.py">ModelServerInfo</a></code>
- <code title="post /v4/serving/a/{alias}/execute">client.alias.<a href="./src/scale_gp/resources/alias.py">execute</a>(alias, \*\*<a href="src/scale_gp/types/alias_execute_params.py">params</a>) -> <a href="./src/scale_gp/types/generic_model_response.py">GenericModelResponse</a></code>
