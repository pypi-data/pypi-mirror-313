# Document Intelligence Client

This Python package offers a robust client for seamless interaction with the Document Intelligence API. It enables you to efficiently retrieve, manage, and process document data within your workspace.

## Installation

To install the package directly from GitHub using `pip`, run the following command:

```sh
pip install sema4ai-di-client
```

## Usage

After installing the package, you can import it and start using the `DocumentIntelligenceClient` class.

### Importing the Package

```python
from sema4ai.di_client import DocumentIntelligenceClient
```

### Getting a Document Work Item

To retrieve a document work item, make sure you've set the required environment variables before initializing the client. Specifically, ensure that `DOCUMENT_INTELLIGENCE_SERVICE_URL` and `AGENTS_EVENTS_SERVICE_URL` is set.

When running in Sema4.ai Control Room these are all handled by the platform.

- **Environment Variables:** Make sure the required environment variables (`DOCUMENT_INTELLIGENCE_SERVICE_URL`, `AGENTS_EVENTS_SERVICE_URL`) are set in your environment before running the code.
- **Workspace ID:** If you are developing on local, then make sure to set workspace_id in `DocumentIntelligenceClient(workspace_id='<your_workspace_id>')`, which is optional and deduced on non-local environments from the URL passed.
- **Initialize the Client:** The client will automatically read the environment variables and initialize the connection.
- **Error Handling:** The example includes error handling and ensures the client is properly closed at the end.

Here's an example:

```python
from sema4ai.di_client import DocumentIntelligenceClient

# Ensure environment variables are set for the service URLs
# Example:
# export DOCUMENT_INTELLIGENCE_SERVICE_URL='https://api.yourdomain.com'
# export AGENTS_EVENTS_SERVICE_URL='https://agents.yourdomain.com'

# Initialize the client
client = DocumentIntelligenceClient()

# Specify the document ID you want to retrieve
document_id = 'your_document_id'

# Get the document work item
try:
    document_work_item = client.get_document_work_item(document_id)
    if document_work_item:
        print("Document Work Item:")
        print(document_work_item)
    else:
        print("No document work item found for the given document ID.")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    client.close()  # Make sure to close the client connection
```

### Available Methods

The `DocumentIntelligenceClient` offers several methods to interact with the Document Intelligence API and manage work items. Below are examples of the available operations:

- **Get Document Type:** Retrieve details about a specific document type.

  ```python
  document_type = client.get_document_type(document_type_name)
  ```

- **Get Document Format:** Fetch the format of a document based on its type and class.

  ```python
  document_format = client.get_document_format(document_type_name, document_class_name)
  ```

- **Store Extracted Content:** Store extracted content after processing a document.

  ```python
  client.store_extracted_content(extracted_content)
  ```

- **Store Transformed Content:** Save content that has been transformed by a process.

  ```python
  client.store_transformed_content(transformed_content)
  ```

- **Store Computed Content:** Submit content that has been computed after analysis.

  ```python
  client.store_computed_content(computed_content)
  ```

- **Get Document Content:** Retrieve document content in various states, such as raw, extracted, transformed, or computed.

  ```python
  content = client.get_document_content(document_id, content_state)
  ```

- **Remove Document Content:** Delete content for a document in a specific state.

  ```python
  client.remove_document_content(document_id, content_state)
  ```

- **Complete Work Item Stage:** Mark a work item’s current stage as complete and move to the next stage.

  ```python
  response = client.work_items_complete_stage(
      work_item_id='your_work_item_id',
      status='SUCCESS',  # or 'FAILURE'
      status_reason='optional_reason',  # Optional
      log_details_path='optional_log_path'  # Optional
  )
  ```

## Dependencies

The package requires the following dependencies:

- `urllib3 >= 1.25.3, < 2.1.0`
- `python-dateutil`
- `pydantic >= 2`
- `typing-extensions >= 4.7.1`

These should be installed automatically when you install the package via `pip`.

### Example Code Snippet

Below is an example code snippet if you are testing on prod.

```python
from sema4ai.di_client import DocumentIntelligenceClient

client = DocumentIntelligenceClient()

# Fetch and print the document type
try:
    document_type = client.get_document_type("CounterParty Reconciliation")
    print(document_type)
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    client.close()  # Ensure proper resource cleanup
```

Below is an example code snippet if you are testing on local.

```python
from sema4ai.di_client import DocumentIntelligenceClient
import os

# Set the required environment variables within the Python code
os.environ['DOCUMENT_INTELLIGENCE_SERVICE_URL'] = 'http://127.0.0.1:9080'
os.environ['AGENTS_EVENTS_SERVICE_URL'] = 'http://127.0.0.1:9080'

workspace_id = "<your Sema4.ai Control Room Workspace ID>"
client = DocumentIntelligenceClient(workspace_id=workspace_id)

# Fetch and print the document type
try:
    document_type = client.get_document_type("CounterParty Reconciliation")
    print(document_type)
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    client.close()  # Ensure proper resource cleanup
```
