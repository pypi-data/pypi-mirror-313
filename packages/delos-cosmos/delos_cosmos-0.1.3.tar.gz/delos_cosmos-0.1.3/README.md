# Delos Cosmos

Cosmos client for interacting with the Cosmos API.

# Installation

To install the package, use `poetry`:

```bash
poetry add delos-cosmos
```

Or if you use the default `pip`:

```bash
pip install delos-cosmos
```

# Client Initialization

You can create an **API key** to access all services through the **Dashboard** in **CosmosPlatform**
`https://platform.cosmos-suite.ai`.

To create a `Cosmos` client instance, you need to initialize it with your API key, and optionally the server URL:

```python
from cosmos import CosmosClient

client = CosmosClient("your-api-key") # will be equivalent to:
client = CosmosClient("your-api-key", "https://platform.cosmos-suite.ai", debug_mode=False)
```

# Endpoints

This `delos-cosmos` client provides access to the following endpoints:

**Status Endpoints**

- `status_health_request`: Check the health of the server.

**Translate Endpoints**

- `translate_text_request`: Translate text.
- `translate_file_request`: Translate a file.

**Web Endpoints**

- `web_search_request`: Perform a web search.

**LLM Endpoints**

- `chat`: Chat with the LLM.
- `embed`: Embed data into the LLM.

**Files Endpoints**

A single file can be read and parsed with the universal parser endpoint:

- `files_parse_request`: Parse a file to extract the pages, chunks or subchunks.

An **index** groups a set of files in order to be able to query them using natural language. There are several
operations regarding **index management**:

- `files_index_create_request`: Create an index.
- `files_index_add_files_request`: Add files to an index.
- `files_index_delete_files_request`: Delete files from an index.
- `files_index_delete_request`: Delete an index.
- `files_index_restore_request`: Restore a deleted index.
- `files_index_rename_request`: Rename an index.

And regarding **index querying**

- `files_index_ask_request`: Ask a question about the index documents (it requires that your `index.status.vectorized`
  is set to `True`).
- `files_index_embed_request`: Embed data into an index.
- `files_index_list_request`: List all indexes.
- `files_index_details_request`: Get details of an index.

These endpoints are accessible through `delos-cosmos` client methods.

> ℹ️ **Info:** For all the **endpoints**, there are specific **parameters** that are required regarding the data to be
> sent to the API.
>
> Endpoints may expect `text` or `files` to operate with, the `output_language` for your result, the `index_uuid` that
> identifies the set of documents, the `model` to use for the LLM operations, etc.
>
> You can find the standarized parameters like `FileTranslationReturnType` and `ParserExtractionType` in the
> `delos_cosmos.models` module.

---

## Status Endpoints

### Status Health Request

To **check the health** of the server and the validity of your API key:

```python
response = client.status_health_request()
if response:
    print(f"Response: {response}")
```

---

## Translate Endpoints

### 1. Translate Text Request

To **translate text**, you can use the `translate_text_request` method:

```python
response = client.translate_text_request(text="Hello, world!", output_language="fr")
if response:
    print(f"Translated Text: {response}")
```

### 2. Translate File Request

To **translate a file**, use the `translate_file_request` method:

```python
local_filepath_1 = Path("/path/to/file1.pdf")

response = client.translate_file_request(filepath=local_filepath_1, output_language="fr")
```

According to the type of file translation you prefer, you can choose the `return_type` parameter to:

| FileTranslationReturnType |                                                     |
| ------------------------- | --------------------------------------------------- |
| raw_text `Default`        | Returns the translated text only                    |
| url                       | Return the translated file with its layout as a URL |
| file                      | Returns a FastaAPI FileResponse type                |

> 💡 **Tip:** For faster and economical translations, set the `return_type` to `raw_text` to request to translate only
> the **text content**, without the file layout.

```python
local_filepath_1 = Path("/path/to/file1.pdf")
local_filepath_2 = Path("/path/to/file2.pdf")

# You can set the return type to be 'raw_text' (only the translated text will be returned) or 'url' (which will return a link to the translated file keeping original file's layout):
response = client.translate_file_request(filepath=local_filepath_1, output_language="fr", return_type="raw_text")

response = client.translate_file_request(filepath=local_filepath_2, output_language="fr", return_type="url")

if response:
    print(f"Translated File Response: {response}")
```

---

## Web Endpoints

### Web Search Request

To perform a **web search**:

```python
response = client.web_search_request(text="What is the capital of France?")

# Or, if you want to specify the output_language and filter results
response = client.web_search_request(text="What is the capital of France?", output_language="fr")
if response:
    print(f"Search Results: {response}")
```

---

## LLM Endpoints

LLM Endpoints provide a way to interact with several Large Language Models and Embedders in an unified way. Supported
`model`s are:

| Chat Models               | Embedding Models       |
| ------------------------- | ---------------------- |
| _gpt-3.5_ `Legacy`        | **ada-v2** `Default`   |
| gpt-4                     | text-embedding-3-large |
| gpt-4-turbo               | text-embedding-3-small |
| gpt-4o                    |                        |
| **gpt-4o-mini** `Default` |                        |
| whisper-1                 |                        |
| o1-preview                |                        |
| command-r                 |                        |
| command-r-plus            |                        |
| llama-3-70b-instruct      |                        |
| mistral-large             |                        |
| mistral-small             |                        |

### 1. Chat Request

To **chat** with the LLM:

```python
response = client.chat(text="Hello, how are you?")

# Default model is handled, so that request is equivalent to:
response = client.chat(text="Hello, how are you?", model="gpt-4o-mini")
if response:
    print(f"Chat Response: {response}")
```

### 2. Embed Request

To **embed** data using a LLM:

```python
embed_data = EmbedData(text="Hello, how are you?")

# Default model is handled, so that request is equivalent to:
embed_data = EmbedData(text="Hello, how are you?", model="ada-v2")
response = client.embed(embed_data)
if response:
    print(f"Embed Response: {response}")
```

---

## Files Endpoints

### Universal Reader and Parser

The Universal reader and parser allows to open many textual **file** formats and extract the content in a **standarized
structure**. In order to parse a file:

```python
local_filepath_1 = Path("/path/to/file1.docx")
local_filepath_2 = Path("/path/to/file2.pdf")

response = client.files_parse_request(filepath=local_filepath_1)

if response:
    print(f"Parsed File Response: {response}")
```

Previous request can be further contolled by providing the **optional parameters**:

```python
response = client.files_parse_request(
            filepath=local_filepath_1,
            extract_type=ParserExtractType.chunks,
            k_min=5000,
            k_max=1000,
            overlap=10,
            filter_pages="[1,2]", # string containing the list of pages you want to select
        )
if response:
    print(f"Parsed File Response: {response}")
```

| ParserExtractType |                                                                                                            |
| ----------------- | ---------------------------------------------------------------------------------------------------------- |
| chunks `Default`  | Returns the chunks of the file. You can custom its tokens size by setting `k_min`, `k_max`, `overlap`      |
| subchunks         | Returns the subchunks of the file (minimal blocks in the file, usually containing around 20 or 30 tokens). |
| pages             | Returns the content of the file parsed as pages                                                            |
| file              | Returns the the whole file contents                                                                        |

> 💡 **Tip:** When using `ParserExtractType.chunks`, you can define the `k_min`, `k_max` and `overlap` parameters to
> control the size of the chunks. Default values are `k_min=500`, `k_max=1200`, and `overlap=0`.

### Files Index

Index group a set of files in order to be able to query them using natural language. The **Index attributes** are:

| Index attribute | Meaning                                                                                                                                        |
| --------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| index_uuid      | Unique identifier of the index. It is randomly generated when the index is created and cannot be altered.                                      |
| name            | Human-friendly name for the index, can be modified through the `rename_index` endpoint.                                                        |
| created_at      | Creation date                                                                                                                                  |
| updated_at      | Last operation performed in index                                                                                                              |
| expires_at      | Expiration date of the index. It will only be set once the `delete_index` request is explictly performed. (Default: None)                      |
| status          | Status of the index. It will be `active`, and only when programmed for deletion it will be `countdown` (2h timeout before effective deletion). |
| vectorized      | Boolean status of the index. When `True`, the index is ready to be queried.                                                                    |
| files           | List of files in the index. Contains their filehash, filename and size                                                                         |
| storage         | Storage details of the index: total size in bytes and MB, number of files.                                                                     |
|                 |

The following **Index operations** are available:

- `INDEX_LIST`: List all indexes.
- `INDEX_DETAILS`: Get details of an index.
- `INDEX_CREATE`: Create a new index and parse files.
- `INDEX_ADD_FILES`: Add files to an existing index.
- `INDEX_DELETE_FILES`: Delete files from an index.
- `INDEX_DELETE`: Delete an index. **Warning**: _This is a delayed (2h) operation, allowed to be reverted with
  `INDEX_RESTORE`. After 2h, the index will be **deleted and not recoverable**._
- `INDEX_RESTORE`: Restore a deleted index _(within the 2h after it was marked for deletion)_.
- `INDEX_EMBED`: Embed data into an index.
- `INDEX_ASK`: Ask a question to the index. It requires that `INDEX_EMBED` is performed to allow index contents
  querying.

### Files Index Requests

#### 1. Existing Index Overview

To **list all indexes** in your organization, files included and storage details:

```python
response = client.files_index_list_request()
if response:
    print(f"List Indexes Response: {response}")
```

With **get details** of an index you can see the list of files in the index, their filehashes, their size, the `status`
of the index and the `vectorized` boolean status (find more details about the Index fields above):

```python
response = client.files_index_details_request(index_uuid="index-uuid")
if response:
    print(f"Index Details Response: {response}")
```

#### 2. Index Management

To **create a new index** and parse files, provide the list of **filepaths** you want to parse:

```python
local_filepaths = [Path("/path/to/file1.docx"), Path("/path/to/file2.pdf")]

response = client.files_index_create_request(filepaths=local_filepaths, name="Cooking Recipes")
if response:
    print(f"Index Create Response: {response}")
```

Let's say the new index has been created with the UUID `d55a285b-0a0d-4ba5-a918-857f63bc9063`. This UUID will be used in
the following requests, particularly in the `index_details` whenever some information about the index is needed.

You can **rename the index** with the `rename_index` method:

````python
index_uuid = "d55a285b-0a0d-4ba5-a918-857f63bc9063"
response = client.files_index_rename_request(index_uuid=index_uuid, name="Best Recipes")
if response:
    print(f"Rename Index Response: {response}")

To **add files** to an existing index, provide the list of **filepaths** you want to add:

```python
index_uuid = "d55a285b-0a0d-4ba5-a918-857f63bc9063"
local_filepath_3 = [Path("/path/to/file3.txt")]
response = client.files_index_add_files_request(index_uuid="existing-index-uuid", filepaths=local_filepath_3)
if response:
    print(f"Add Files to Index Response: {response}")
````

To **delete files** from an existing index, specify the **filehashes** of the files you want to delete:

```python
index_uuid = "d55a285b-0a0d-4ba5-a918-857f63bc9063"
filehashes_to_delete = ["2fa92ab4627c199a2827a363469bf4e513c67b758c34d1e316c2968ed68b9634"]
response = client.files_index_delete_files_request(index_uuid=index_uuid, files_hashes=filehashes_to_delete)
if response:
    print(f"Delete Files from Index Response: {response}")
```

To **delete an index** (it will be marked for deletion which will become effective **after 2h**):

```python
index_operation_data = IndexOperationData(index_uuid="index-to-delete-uuid")
response = client.files_index_operation_request(index_operation_data, FileEndpoints.INDEX_DELETE)
if response:
    print(f"Delete Index Response: {response}")
```

To **restore an index** marked for deletion (only possible during the 2h after the `INDEX_DELETE` was requested):

```python
index_operation_data = IndexOperationData(index_uuid="index-to-restore-uuid")
response = client.files_index_operation_request(index_operation_data, FileEndpoints.INDEX_RESTORE)
if response:
    print(f"Restore Index Response: {response}")
```

#### 3. Index Querying

To **embed** or **vectorize index contents** in order to allow the query operations:

```python
index_operation_data = IndexOperationData(index_uuid="index-uuid", data_to_embed=my_data)
response = client.files_index_operation_request(index_operation_data, FileEndpoints.INDEX_EMBED)
if response:
    print(f"Embed Data Response: {response}")
```

To **ask a question** about the index documents (it requires that your `index.status.vectorized` is set to `True`):

```python
index_operation_data = IndexOperationData(index_uuid="index-uuid", question="What is Cosmos?")
response = client.files_index_operation_request(index_operation_data, FileEndpoints.INDEX_ASK)
if response:
    print(f"Ask Index Response: {response}")
```

## Requests Usage and Storage

All request responses show the **number of tokens** and **cost** consumed by the request. The **storage** for index
documents is **limited** up to your organization's quota and is shared between all indexes within your organization.
Contents **do not expire**, but they can be deleted by performing an explicit request through the API endpoints or
through the **CosmosPlatform** at `https://platform.cosmos-suite.ai/`.

In the **CosmosPlatform**, you can monitor the requests performed by your organization with your API Key and the files
stored in the Index Storage.

Through both the native requests towards Cosmos and the Python client, you can handle and delete files directly from the
Cosmos Platform.
