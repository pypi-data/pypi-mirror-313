# Transforms

Types:

```python
from trellis.types import (
    TransformCreateResponse,
    TransformUpdateResponse,
    TransformListResponse,
    TransformDeleteResponse,
    TransformAutoschemaResponse,
    TransformDuplicateResponse,
    TransformReferenceResponse,
    TransformSummarizeResponse,
    TransformWakeUpResponse,
)
```

Methods:

- <code title="post /v1/transforms/create">client.transforms.<a href="./src/trellis/resources/transforms/transforms.py">create</a>(\*\*<a href="src/trellis/types/transform_create_params.py">params</a>) -> <a href="./src/trellis/types/transform_create_response.py">TransformCreateResponse</a></code>
- <code title="patch /v1/transforms/{transform_id}">client.transforms.<a href="./src/trellis/resources/transforms/transforms.py">update</a>(transform_id, \*\*<a href="src/trellis/types/transform_update_params.py">params</a>) -> <a href="./src/trellis/types/transform_update_response.py">TransformUpdateResponse</a></code>
- <code title="get /v1/transforms">client.transforms.<a href="./src/trellis/resources/transforms/transforms.py">list</a>(\*\*<a href="src/trellis/types/transform_list_params.py">params</a>) -> <a href="./src/trellis/types/transform_list_response.py">TransformListResponse</a></code>
- <code title="delete /v1/transforms/{transform_id}">client.transforms.<a href="./src/trellis/resources/transforms/transforms.py">delete</a>(transform_id) -> <a href="./src/trellis/types/transform_delete_response.py">TransformDeleteResponse</a></code>
- <code title="get /v1/transforms/{transform_id}/autoschema">client.transforms.<a href="./src/trellis/resources/transforms/transforms.py">autoschema</a>(transform_id) -> <a href="./src/trellis/types/transform_autoschema_response.py">TransformAutoschemaResponse</a></code>
- <code title="post /v1/transforms/{transform_id}/duplicate">client.transforms.<a href="./src/trellis/resources/transforms/transforms.py">duplicate</a>(transform_id) -> <a href="./src/trellis/types/transform_duplicate_response.py">TransformDuplicateResponse</a></code>
- <code title="post /v1/transforms/reference">client.transforms.<a href="./src/trellis/resources/transforms/transforms.py">reference</a>(\*\*<a href="src/trellis/types/transform_reference_params.py">params</a>) -> <a href="./src/trellis/types/transform_reference_response.py">TransformReferenceResponse</a></code>
- <code title="post /v1/transforms/{transform_id}/summarize">client.transforms.<a href="./src/trellis/resources/transforms/transforms.py">summarize</a>(transform_id, \*\*<a href="src/trellis/types/transform_summarize_params.py">params</a>) -> <a href="./src/trellis/types/transform_summarize_response.py">TransformSummarizeResponse</a></code>
- <code title="get /v1/transforms/wake_up">client.transforms.<a href="./src/trellis/resources/transforms/transforms.py">wake_up</a>() -> <a href="./src/trellis/types/transform_wake_up_response.py">object</a></code>

## Results

Types:

```python
from trellis.types.transforms import ResultUpdateResponse, ResultExportResponse
```

Methods:

- <code title="patch /v1/transforms/{transform_id}/results/{result_id}">client.transforms.results.<a href="./src/trellis/resources/transforms/results.py">update</a>(result_id, \*, transform_id, \*\*<a href="src/trellis/types/transforms/result_update_params.py">params</a>) -> <a href="./src/trellis/types/transforms/result_update_response.py">ResultUpdateResponse</a></code>
- <code title="post /v1/transforms/{transform_id}/results/export">client.transforms.results.<a href="./src/trellis/resources/transforms/results.py">export</a>(transform_id, \*\*<a href="src/trellis/types/transforms/result_export_params.py">params</a>) -> <a href="./src/trellis/types/transforms/result_export_response.py">ResultExportResponse</a></code>

## Validations

Types:

```python
from trellis.types.transforms import (
    ValidationRetrieveResponse,
    ValidationUpdateResponse,
    ValidationDeleteResponse,
)
```

Methods:

- <code title="get /v1/transforms/{transform_id}/validations">client.transforms.validations.<a href="./src/trellis/resources/transforms/validations/validations.py">retrieve</a>(transform_id, \*\*<a href="src/trellis/types/transforms/validation_retrieve_params.py">params</a>) -> <a href="./src/trellis/types/transforms/validation_retrieve_response.py">ValidationRetrieveResponse</a></code>
- <code title="patch /v1/transforms/validations/{validation_id}">client.transforms.validations.<a href="./src/trellis/resources/transforms/validations/validations.py">update</a>(validation_id, \*\*<a href="src/trellis/types/transforms/validation_update_params.py">params</a>) -> <a href="./src/trellis/types/transforms/validation_update_response.py">ValidationUpdateResponse</a></code>
- <code title="delete /v1/transforms/validations/{validation_id}">client.transforms.validations.<a href="./src/trellis/resources/transforms/validations/validations.py">delete</a>(validation_id) -> <a href="./src/trellis/types/transforms/validation_delete_response.py">ValidationDeleteResponse</a></code>

### Params

Types:

```python
from trellis.types.transforms.validations import (
    ParamCreateResponse,
    ParamRetrieveResponse,
    ParamUpdateResponse,
    ParamDeleteResponse,
)
```

Methods:

- <code title="post /v1/transforms/{transform_id}/validations/params">client.transforms.validations.params.<a href="./src/trellis/resources/transforms/validations/params.py">create</a>(transform_id, \*\*<a href="src/trellis/types/transforms/validations/param_create_params.py">params</a>) -> <a href="./src/trellis/types/transforms/validations/param_create_response.py">ParamCreateResponse</a></code>
- <code title="get /v1/transforms/{transform_id}/validations/params">client.transforms.validations.params.<a href="./src/trellis/resources/transforms/validations/params.py">retrieve</a>(transform_id) -> <a href="./src/trellis/types/transforms/validations/param_retrieve_response.py">ParamRetrieveResponse</a></code>
- <code title="put /v1/transforms/{transform_id}/validations/params/{validation_param_id}">client.transforms.validations.params.<a href="./src/trellis/resources/transforms/validations/params.py">update</a>(validation_param_id, \*, transform_id, \*\*<a href="src/trellis/types/transforms/validations/param_update_params.py">params</a>) -> <a href="./src/trellis/types/transforms/validations/param_update_response.py">ParamUpdateResponse</a></code>
- <code title="delete /v1/transforms/{transform_id}/validations/params/{validation_param_id}">client.transforms.validations.params.<a href="./src/trellis/resources/transforms/validations/params.py">delete</a>(validation_param_id, \*, transform_id) -> <a href="./src/trellis/types/transforms/validations/param_delete_response.py">ParamDeleteResponse</a></code>

# Customers

Types:

```python
from trellis.types import Usage
```

Methods:

- <code title="get /v1/customers/usage">client.customers.<a href="./src/trellis/resources/customers.py">usage</a>(\*\*<a href="src/trellis/types/customer_usage_params.py">params</a>) -> <a href="./src/trellis/types/usage.py">Usage</a></code>

# Projects

Types:

```python
from trellis.types import (
    ProjectCreateResponse,
    ProjectListResponse,
    ProjectDeleteResponse,
    ProjectTransferResponse,
)
```

Methods:

- <code title="post /v1/projects/create">client.projects.<a href="./src/trellis/resources/projects.py">create</a>(\*\*<a href="src/trellis/types/project_create_params.py">params</a>) -> <a href="./src/trellis/types/project_create_response.py">ProjectCreateResponse</a></code>
- <code title="get /v1/projects">client.projects.<a href="./src/trellis/resources/projects.py">list</a>(\*\*<a href="src/trellis/types/project_list_params.py">params</a>) -> <a href="./src/trellis/types/project_list_response.py">ProjectListResponse</a></code>
- <code title="delete /v1/projects/{proj_id}">client.projects.<a href="./src/trellis/resources/projects.py">delete</a>(proj_id) -> <a href="./src/trellis/types/project_delete_response.py">ProjectDeleteResponse</a></code>
- <code title="post /v1/projects/{proj_id}/transfer">client.projects.<a href="./src/trellis/resources/projects.py">transfer</a>(proj_id, \*\*<a href="src/trellis/types/project_transfer_params.py">params</a>) -> <a href="./src/trellis/types/project_transfer_response.py">ProjectTransferResponse</a></code>

# Assets

Types:

```python
from trellis.types import Assets, AssetDeleteResponse, AssetExtractResponse
```

Methods:

- <code title="get /v1/assets">client.assets.<a href="./src/trellis/resources/assets.py">list</a>(\*\*<a href="src/trellis/types/asset_list_params.py">params</a>) -> <a href="./src/trellis/types/assets.py">Assets</a></code>
- <code title="delete /v1/assets/{asset_id}">client.assets.<a href="./src/trellis/resources/assets.py">delete</a>(asset_id) -> <a href="./src/trellis/types/asset_delete_response.py">AssetDeleteResponse</a></code>
- <code title="get /v1/assets/{asset_id}/extract">client.assets.<a href="./src/trellis/resources/assets.py">extract</a>(asset_id, \*\*<a href="src/trellis/types/asset_extract_params.py">params</a>) -> <a href="./src/trellis/types/asset_extract_response.py">AssetExtractResponse</a></code>
- <code title="post /v1/assets/upload">client.assets.<a href="./src/trellis/resources/assets.py">upload</a>(\*\*<a href="src/trellis/types/asset_upload_params.py">params</a>) -> <a href="./src/trellis/types/assets.py">Assets</a></code>

# AssetsExtract

Types:

```python
from trellis.types import Extract, AssetsExtractUpdateStatusResponse
```

Methods:

- <code title="post /v1/assets/extract">client.assets_extract.<a href="./src/trellis/resources/assets_extract.py">extract</a>(\*\*<a href="src/trellis/types/assets_extract_extract_params.py">params</a>) -> <a href="./src/trellis/types/extract.py">Extract</a></code>
- <code title="put /v1/assets/update_status">client.assets_extract.<a href="./src/trellis/resources/assets_extract.py">update_status</a>(\*\*<a href="src/trellis/types/assets_extract_update_status_params.py">params</a>) -> <a href="./src/trellis/types/assets_extract_update_status_response.py">object</a></code>

# Events

## Subscriptions

Types:

```python
from trellis.types.events import (
    EventSubscription,
    SubscriptionUpdateResponse,
    SubscriptionListResponse,
    SubscriptionDeleteResponse,
)
```

Methods:

- <code title="post /v1/events/subscriptions">client.events.subscriptions.<a href="./src/trellis/resources/events/subscriptions/subscriptions.py">create</a>(\*\*<a href="src/trellis/types/events/subscription_create_params.py">params</a>) -> <a href="./src/trellis/types/events/event_subscription.py">EventSubscription</a></code>
- <code title="put /v1/events/subscriptions/{event_subscription_id}">client.events.subscriptions.<a href="./src/trellis/resources/events/subscriptions/subscriptions.py">update</a>(event_subscription_id, \*\*<a href="src/trellis/types/events/subscription_update_params.py">params</a>) -> <a href="./src/trellis/types/events/subscription_update_response.py">SubscriptionUpdateResponse</a></code>
- <code title="get /v1/events/subscriptions">client.events.subscriptions.<a href="./src/trellis/resources/events/subscriptions/subscriptions.py">list</a>(\*\*<a href="src/trellis/types/events/subscription_list_params.py">params</a>) -> <a href="./src/trellis/types/events/subscription_list_response.py">SubscriptionListResponse</a></code>
- <code title="delete /v1/events/subscriptions">client.events.subscriptions.<a href="./src/trellis/resources/events/subscriptions/subscriptions.py">delete</a>(\*\*<a href="src/trellis/types/events/subscription_delete_params.py">params</a>) -> <a href="./src/trellis/types/events/subscription_delete_response.py">SubscriptionDeleteResponse</a></code>

### Actions

Types:

```python
from trellis.types.events.subscriptions import EventSubscriptionAction
```

Methods:

- <code title="post /v1/events/subscriptions/{event_subscription_id}/actions">client.events.subscriptions.actions.<a href="./src/trellis/resources/events/subscriptions/actions.py">create</a>(event_subscription_id, \*\*<a href="src/trellis/types/events/subscriptions/action_create_params.py">params</a>) -> <a href="./src/trellis/types/events/subscriptions/event_subscription_action.py">EventSubscriptionAction</a></code>

## Actions

Types:

```python
from trellis.types.events import EventAction
```

Methods:

- <code title="delete /v1/events/actions">client.events.actions.<a href="./src/trellis/resources/events/actions.py">delete</a>(\*\*<a href="src/trellis/types/events/action_delete_params.py">params</a>) -> <a href="./src/trellis/types/events/event_action.py">EventAction</a></code>

## Jobs

Types:

```python
from trellis.types.events import Jobs
```

Methods:

- <code title="get /v1/events/jobs">client.events.jobs.<a href="./src/trellis/resources/events/jobs.py">list</a>(\*\*<a href="src/trellis/types/events/job_list_params.py">params</a>) -> <a href="./src/trellis/types/events/jobs.py">Jobs</a></code>

# Templates

Types:

```python
from trellis.types import (
    Template,
    TemplateList,
    TemplateUpdateResponse,
    TemplateDeleteResponse,
    TemplateCopyResponse,
)
```

Methods:

- <code title="post /v1/templates">client.templates.<a href="./src/trellis/resources/templates/templates.py">create</a>(\*\*<a href="src/trellis/types/template_create_params.py">params</a>) -> <a href="./src/trellis/types/template.py">Template</a></code>
- <code title="put /v1/templates/{template_id}">client.templates.<a href="./src/trellis/resources/templates/templates.py">update</a>(template_id, \*\*<a href="src/trellis/types/template_update_params.py">params</a>) -> <a href="./src/trellis/types/template_update_response.py">TemplateUpdateResponse</a></code>
- <code title="get /v1/templates">client.templates.<a href="./src/trellis/resources/templates/templates.py">list</a>(\*\*<a href="src/trellis/types/template_list_params.py">params</a>) -> <a href="./src/trellis/types/template_list.py">TemplateList</a></code>
- <code title="delete /v1/templates/{template_id}">client.templates.<a href="./src/trellis/resources/templates/templates.py">delete</a>(template_id) -> <a href="./src/trellis/types/template_delete_response.py">TemplateDeleteResponse</a></code>
- <code title="post /v1/templates/{template_id}/copy">client.templates.<a href="./src/trellis/resources/templates/templates.py">copy</a>(template_id, \*\*<a href="src/trellis/types/template_copy_params.py">params</a>) -> <a href="./src/trellis/types/template_copy_response.py">TemplateCopyResponse</a></code>

## Image

Types:

```python
from trellis.types.templates import TemplateImage, ImageDeleteResponse
```

Methods:

- <code title="put /v1/templates/{template_id}/image">client.templates.image.<a href="./src/trellis/resources/templates/image.py">update</a>(template_id, \*\*<a href="src/trellis/types/templates/image_update_params.py">params</a>) -> <a href="./src/trellis/types/templates/template_image.py">TemplateImage</a></code>
- <code title="delete /v1/templates/{template_id}/image">client.templates.image.<a href="./src/trellis/resources/templates/image.py">delete</a>(template_id) -> <a href="./src/trellis/types/templates/image_delete_response.py">ImageDeleteResponse</a></code>

## Categories

Types:

```python
from trellis.types.templates import (
    TemplateCategory,
    CategoryUpdateResponse,
    CategoryListResponse,
    CategoryDeleteResponse,
)
```

Methods:

- <code title="post /v1/templates/categories">client.templates.categories.<a href="./src/trellis/resources/templates/categories.py">create</a>(\*\*<a href="src/trellis/types/templates/category_create_params.py">params</a>) -> <a href="./src/trellis/types/templates/template_category.py">TemplateCategory</a></code>
- <code title="put /v1/templates/categories/{category_id}">client.templates.categories.<a href="./src/trellis/resources/templates/categories.py">update</a>(category_id, \*\*<a href="src/trellis/types/templates/category_update_params.py">params</a>) -> <a href="./src/trellis/types/templates/category_update_response.py">CategoryUpdateResponse</a></code>
- <code title="get /v1/templates/categories">client.templates.categories.<a href="./src/trellis/resources/templates/categories.py">list</a>(\*\*<a href="src/trellis/types/templates/category_list_params.py">params</a>) -> <a href="./src/trellis/types/templates/category_list_response.py">CategoryListResponse</a></code>
- <code title="delete /v1/templates/categories/{category_id}">client.templates.categories.<a href="./src/trellis/resources/templates/categories.py">delete</a>(category_id) -> <a href="./src/trellis/types/templates/category_delete_response.py">CategoryDeleteResponse</a></code>

# DataSources

Types:

```python
from trellis.types import Source, DataSourceRetrieveResponse
```

Methods:

- <code title="post /v1/data_source">client.data_sources.<a href="./src/trellis/resources/data_sources/data_sources.py">create</a>(\*\*<a href="src/trellis/types/data_source_create_params.py">params</a>) -> <a href="./src/trellis/types/source.py">Source</a></code>
- <code title="get /v1/data_source">client.data_sources.<a href="./src/trellis/resources/data_sources/data_sources.py">retrieve</a>(\*\*<a href="src/trellis/types/data_source_retrieve_params.py">params</a>) -> <a href="./src/trellis/types/data_source_retrieve_response.py">DataSourceRetrieveResponse</a></code>

## Metadata

Types:

```python
from trellis.types.data_sources import SourceMetadata, MetadataRetrieveResponse
```

Methods:

- <code title="get /v1/data_source/{source_id}/metadata">client.data_sources.metadata.<a href="./src/trellis/resources/data_sources/metadata.py">retrieve</a>(source_id, \*\*<a href="src/trellis/types/data_sources/metadata_retrieve_params.py">params</a>) -> <a href="./src/trellis/types/data_sources/metadata_retrieve_response.py">MetadataRetrieveResponse</a></code>
