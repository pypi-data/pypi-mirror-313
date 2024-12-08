# Shared Types

```python
from senso_developers.types import ListDocument, Message
```

# Utils

Methods:

- <code title="get /health">client.utils.<a href="./src/senso_developers/resources/utils.py">health_check</a>() -> <a href="./src/senso_developers/types/shared/message.py">Message</a></code>
- <code title="get /">client.utils.<a href="./src/senso_developers/resources/utils.py">index</a>() -> <a href="./src/senso_developers/types/shared/message.py">Message</a></code>

# Orgs

Types:

```python
from senso_developers.types import Org, OrgList
```

Methods:

- <code title="post /orgs">client.orgs.<a href="./src/senso_developers/resources/orgs/orgs.py">create</a>(\*\*<a href="src/senso_developers/types/org_create_params.py">params</a>) -> <a href="./src/senso_developers/types/org.py">Org</a></code>
- <code title="get /orgs/{org_id}">client.orgs.<a href="./src/senso_developers/resources/orgs/orgs.py">retrieve</a>(org_id) -> <a href="./src/senso_developers/types/org.py">Org</a></code>
- <code title="put /orgs/{org_id}">client.orgs.<a href="./src/senso_developers/resources/orgs/orgs.py">update</a>(org_id, \*\*<a href="src/senso_developers/types/org_update_params.py">params</a>) -> <a href="./src/senso_developers/types/org.py">Org</a></code>
- <code title="get /orgs">client.orgs.<a href="./src/senso_developers/resources/orgs/orgs.py">list</a>() -> <a href="./src/senso_developers/types/org_list.py">OrgList</a></code>
- <code title="delete /orgs/{org_id}">client.orgs.<a href="./src/senso_developers/resources/orgs/orgs.py">delete</a>(org_id) -> <a href="./src/senso_developers/types/shared/message.py">Message</a></code>

## Collections

Types:

```python
from senso_developers.types.orgs import Collection, CollectionList
```

Methods:

- <code title="post /orgs/{org_id}/collections">client.orgs.collections.<a href="./src/senso_developers/resources/orgs/collections/collections.py">create</a>(org_id, \*\*<a href="src/senso_developers/types/orgs/collection_create_params.py">params</a>) -> <a href="./src/senso_developers/types/orgs/collection.py">Collection</a></code>
- <code title="get /orgs/{org_id}/collections/{collection_id}">client.orgs.collections.<a href="./src/senso_developers/resources/orgs/collections/collections.py">retrieve</a>(collection_id, \*, org_id) -> <a href="./src/senso_developers/types/orgs/collection.py">Collection</a></code>
- <code title="put /orgs/{org_id}/collections/{collection_id}">client.orgs.collections.<a href="./src/senso_developers/resources/orgs/collections/collections.py">update</a>(collection_id, \*, org_id, \*\*<a href="src/senso_developers/types/orgs/collection_update_params.py">params</a>) -> <a href="./src/senso_developers/types/orgs/collection.py">Collection</a></code>
- <code title="get /orgs/{org_id}/collections">client.orgs.collections.<a href="./src/senso_developers/resources/orgs/collections/collections.py">list</a>(org_id) -> <a href="./src/senso_developers/types/orgs/collection_list.py">CollectionList</a></code>
- <code title="delete /orgs/{org_id}/collections/{collection_id}">client.orgs.collections.<a href="./src/senso_developers/resources/orgs/collections/collections.py">delete</a>(collection_id, \*, org_id) -> <a href="./src/senso_developers/types/shared/message.py">Message</a></code>

### Documents

Types:

```python
from senso_developers.types.orgs.collections import DocumentListResponse
```

Methods:

- <code title="get /orgs/{org_id}/collections/{collection_id}/documents">client.orgs.collections.documents.<a href="./src/senso_developers/resources/orgs/collections/documents.py">list</a>(collection_id, \*, org_id) -> <a href="./src/senso_developers/types/orgs/collections/document_list_response.py">DocumentListResponse</a></code>
- <code title="post /orgs/{org_id}/collections/{collection_id}/documents/{document_id}">client.orgs.collections.documents.<a href="./src/senso_developers/resources/orgs/collections/documents.py">add</a>(document_id, \*, org_id, collection_id) -> <a href="./src/senso_developers/types/shared/message.py">Message</a></code>
- <code title="delete /orgs/{org_id}/collections/{collection_id}/documents/{document_id}">client.orgs.collections.documents.<a href="./src/senso_developers/resources/orgs/collections/documents.py">remove</a>(document_id, \*, org_id, collection_id) -> <a href="./src/senso_developers/types/shared/message.py">Message</a></code>

## Documents

Types:

```python
from senso_developers.types.orgs import Document, DocumentListResponse
```

Methods:

- <code title="post /orgs/{org_id}/documents">client.orgs.documents.<a href="./src/senso_developers/resources/orgs/documents.py">create</a>(org_id, \*\*<a href="src/senso_developers/types/orgs/document_create_params.py">params</a>) -> <a href="./src/senso_developers/types/orgs/document.py">Document</a></code>
- <code title="get /orgs/{org_id}/documents/{document_id}">client.orgs.documents.<a href="./src/senso_developers/resources/orgs/documents.py">retrieve</a>(document_id, \*, org_id) -> <a href="./src/senso_developers/types/orgs/document.py">Document</a></code>
- <code title="put /orgs/{org_id}/documents/{document_id}">client.orgs.documents.<a href="./src/senso_developers/resources/orgs/documents.py">update</a>(document_id, \*, org_id, \*\*<a href="src/senso_developers/types/orgs/document_update_params.py">params</a>) -> <a href="./src/senso_developers/types/orgs/document.py">Document</a></code>
- <code title="get /orgs/{org_id}/documents">client.orgs.documents.<a href="./src/senso_developers/resources/orgs/documents.py">list</a>(org_id) -> <a href="./src/senso_developers/types/orgs/document_list_response.py">DocumentListResponse</a></code>
- <code title="delete /orgs/{org_id}/documents/{document_id}">client.orgs.documents.<a href="./src/senso_developers/resources/orgs/documents.py">delete</a>(document_id, \*, org_id) -> <a href="./src/senso_developers/types/shared/message.py">Message</a></code>

## Categories

Types:

```python
from senso_developers.types.orgs import Category, CategoryListResponse
```

Methods:

- <code title="post /orgs/{org_id}/categories">client.orgs.categories.<a href="./src/senso_developers/resources/orgs/categories/categories.py">create</a>(org_id, \*\*<a href="src/senso_developers/types/orgs/category_create_params.py">params</a>) -> <a href="./src/senso_developers/types/orgs/category.py">Category</a></code>
- <code title="get /orgs/{org_id}/categories/{category_id}">client.orgs.categories.<a href="./src/senso_developers/resources/orgs/categories/categories.py">retrieve</a>(category_id, \*, org_id) -> <a href="./src/senso_developers/types/orgs/category.py">Category</a></code>
- <code title="put /orgs/{org_id}/categories/{category_id}">client.orgs.categories.<a href="./src/senso_developers/resources/orgs/categories/categories.py">update</a>(category_id, \*, org_id, \*\*<a href="src/senso_developers/types/orgs/category_update_params.py">params</a>) -> <a href="./src/senso_developers/types/orgs/category.py">Category</a></code>
- <code title="get /orgs/{org_id}/categories">client.orgs.categories.<a href="./src/senso_developers/resources/orgs/categories/categories.py">list</a>(org_id) -> <a href="./src/senso_developers/types/orgs/category_list_response.py">CategoryListResponse</a></code>
- <code title="delete /orgs/{org_id}/categories/{category_id}">client.orgs.categories.<a href="./src/senso_developers/resources/orgs/categories/categories.py">delete</a>(category_id, \*, org_id) -> <a href="./src/senso_developers/types/shared/message.py">Message</a></code>

### Tags

Types:

```python
from senso_developers.types.orgs.categories import Tag, TagListResponse
```

Methods:

- <code title="post /orgs/{org_id}/categories/{category_id}/tags">client.orgs.categories.tags.<a href="./src/senso_developers/resources/orgs/categories/tags.py">create</a>(category_id, \*, org_id, \*\*<a href="src/senso_developers/types/orgs/categories/tag_create_params.py">params</a>) -> <a href="./src/senso_developers/types/orgs/categories/tag.py">Tag</a></code>
- <code title="get /orgs/{org_id}/categories/{category_id}/tags/{tag_id}">client.orgs.categories.tags.<a href="./src/senso_developers/resources/orgs/categories/tags.py">retrieve</a>(tag_id, \*, org_id, category_id) -> <a href="./src/senso_developers/types/orgs/categories/tag.py">Tag</a></code>
- <code title="put /orgs/{org_id}/categories/{category_id}/tags/{tag_id}">client.orgs.categories.tags.<a href="./src/senso_developers/resources/orgs/categories/tags.py">update</a>(tag_id, \*, org_id, category_id, \*\*<a href="src/senso_developers/types/orgs/categories/tag_update_params.py">params</a>) -> <a href="./src/senso_developers/types/orgs/categories/tag.py">Tag</a></code>
- <code title="get /orgs/{org_id}/categories/{category_id}/tags">client.orgs.categories.tags.<a href="./src/senso_developers/resources/orgs/categories/tags.py">list</a>(category_id, \*, org_id) -> <a href="./src/senso_developers/types/orgs/categories/tag_list_response.py">TagListResponse</a></code>
- <code title="delete /orgs/{org_id}/categories/{category_id}/tags/{tag_id}">client.orgs.categories.tags.<a href="./src/senso_developers/resources/orgs/categories/tags.py">delete</a>(tag_id, \*, org_id, category_id) -> <a href="./src/senso_developers/types/shared/message.py">Message</a></code>

## Search

Types:

```python
from senso_developers.types.orgs import (
    ChunkPages,
    DocPages,
    SearchChunksResponse,
    SearchDocumentsResponse,
)
```

Methods:

- <code title="post /orgs/{org_id}/search/chunks">client.orgs.search.<a href="./src/senso_developers/resources/orgs/search.py">chunks</a>(org_id, \*\*<a href="src/senso_developers/types/orgs/search_chunks_params.py">params</a>) -> <a href="./src/senso_developers/types/orgs/search_chunks_response.py">SearchChunksResponse</a></code>
- <code title="post /orgs/{org_id}/search/documents">client.orgs.search.<a href="./src/senso_developers/resources/orgs/search.py">documents</a>(org_id, \*\*<a href="src/senso_developers/types/orgs/search_documents_params.py">params</a>) -> <a href="./src/senso_developers/types/orgs/search_documents_response.py">SearchDocumentsResponse</a></code>
