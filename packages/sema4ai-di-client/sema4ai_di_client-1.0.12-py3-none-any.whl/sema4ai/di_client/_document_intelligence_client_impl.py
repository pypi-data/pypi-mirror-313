import datetime
import logging
import os
import re
import typing
from typing import Optional, Union, List, Dict, Any

from sema4ai.di_client.document_intelligence_client.models.vector_search_request import VectorSearchRequest
from sema4ai.di_client.document_intelligence_client.models.search_document_fields_request_inner import SearchDocumentFieldsRequestInner
from sema4ai.di_client.document_intelligence_client.exceptions import ApiException
from sema4ai.di_client.document_intelligence_client.models import (
    ComputedDocumentContent,
    DocumentFormat,
    DocumentFormatState,
    DocumentWorkItem,
    ExtractedDocumentContent,
    RawDocumentContent,
    TransformedDocumentContent,
)
from sema4ai.di_client.document_intelligence_client.models.get_document_content200_response import (
    GetDocumentContent200Response,
)

if typing.TYPE_CHECKING:
    from sema4ai.di_client.document_intelligence_client.models.content_state import (
        ContentState,
    )
    from sema4ai.di_client.document_intelligence_client.models.doc_type import DocType


def _get_current_time_as_iso() -> str:
    return _datetime_to_iso(datetime.datetime.now(datetime.timezone.utc))


def _datetime_to_iso(d: datetime.datetime) -> str:
    """
    Accepts a datetime or a float with seconds from epoch.
    """
    return d.isoformat()


def _iso_to_datetime(isostr: str) -> datetime.datetime:
    import dateutil.parser

    return dateutil.parser.parse(isostr)


def _get_tenant_id_from_url(url: str) -> Optional[str]:
    """
    The workspace ID appears after the 'tenants/' part in the URL.

    Returns:
    - workspace ID (str): The extracted tenant ID.
    """
    # Use regex to extract the tenant ID
    match = re.search(r"tenants/([\w|-]+)(/|$)", url)
    if match:
        workspace_id = match.group(1)
        return workspace_id
    else:
        logging.info(f"`tenants` not found from URL: {url}")
        return None


def _should_renew(expires_at: Optional[datetime.datetime]) -> bool:
    """
    Decides if the token should be renewed based on the expiration time.
    """
    if expires_at is None:
        return False

    now = datetime.datetime.now(datetime.timezone.utc)
    # Renew 10 seconds before
    renew_if_expires_higher_than = now + datetime.timedelta(seconds=10)
    return expires_at <= renew_if_expires_higher_than


class _DocumentIntelligenceClient:
    _workspace_id: str
    _token: Optional[str] = None
    _token_expires_at: Optional[datetime.datetime] = None

    def __init__(self):
        self._initialize()

    def _initialize(self):
        credential_api_url = os.getenv("SEMA4AI_CREDENTIAL_API")
        if credential_api_url:
            import sema4ai_http

            # When running locally the credential API should be defined and then
            # it needs to be queried to get the other urls.
            #
            # The x-document-intelligence-client header should be set when requesting it.
            response = sema4ai_http.get(
                credential_api_url, headers={"x-document-intelligence-client": "true"}
            )
            if response.status != 200:
                raise RuntimeError(
                    f"Error getting credentials from {credential_api_url}: {response.data.decode('utf-8', 'replace')}"
                )
            credential = response.json()
            if not credential.get("success"):
                raise RuntimeError(
                    f'Error getting credentials from {credential_api_url}: {credential.get("error")}'
                )
            data = credential["data"]
            token = data["access_token"]["token"]
            expires_at = data["access_token"]["expiresAt"]
            self._token_expires_at = _iso_to_datetime(expires_at)
            self._token = token

            # On local machine the workspace id we get from
            workspace_id = data["id"]
            di_service_url = data["services"]["documents"]["url"]
            agents_events_service_url = data["services"]["work_items"]["url"]
            if not workspace_id:
                msg = f"Unable to get workspace ID from credential API: {credential_api_url}"
                logging.error(msg)
                raise ValueError(msg)

        else:
            # This is what is done when running in ACE
            di_service_url = os.getenv("SEMA4AI_DOCUMENT_INTELLIGENCE_SERVICE_URL")
            if not di_service_url:
                di_service_url = os.getenv("DOCUMENT_INTELLIGENCE_SERVICE_URL")

            agents_events_service_url = os.getenv("SEMA4AI_AGENTS_EVENTS_SERVICE_URL")
            if not agents_events_service_url:
                agents_events_service_url = os.getenv("AGENTS_EVENTS_SERVICE_URL")

            token = None

            # Check if required environment variables are set, throw error if not
            if not di_service_url:
                raise ValueError(
                    "Environment variable 'SEMA4AI_DOCUMENT_INTELLIGENCE_SERVICE_URL' is not set."
                )
            if not agents_events_service_url:
                raise ValueError(
                    "Environment variable 'SEMA4AI_AGENTS_EVENTS_SERVICE_URL' is not set."
                )

            # In ACE the workspace id is derived from the url
            workspace_id = _get_tenant_id_from_url(di_service_url)

            if not workspace_id:
                msg = f"Unable to get workspace ID from URL: {di_service_url}"
                logging.error(msg)
                raise ValueError(msg)

        self._workspace_id = workspace_id

        # Initialize the clients
        from sema4ai.di_client.document_intelligence_client.api.default_api import (
            DefaultApi as DocumentIntelligenceDefaultApi,
        )

        self._documents_data_client = DocumentIntelligenceDefaultApi()

        from sema4ai.di_client.agents_events_publisher.api.default_api import (
            DefaultApi as WorkItemsDefaultApi,
        )

        self._work_items_client = WorkItemsDefaultApi()

        # Set the base URLs for the clients
        self._documents_data_client.api_client.configuration.host = di_service_url
        self._work_items_client.api_client.configuration.host = (
            agents_events_service_url
        )
        logging.info(f"Documents Data Client URL set to: {di_service_url}")
        logging.info(f"Work Items Client URL set to: {agents_events_service_url}")

    @property
    def _headers(self) -> Optional[dict[str, str]]:
        """
        The headers to be passed on each request.
        """
        if self._token_expires_at is not None:
            if _should_renew(self._token_expires_at):
                logging.info(
                    "Refreshing token (expires at: %s, current time: %s)",
                    _datetime_to_iso(self._token_expires_at),
                    _get_current_time_as_iso(),
                )
                # Reinitialized everything to get the new token.
                self._initialize()

        headers = {}
        if self._token:
            headers["Authorization"] = f"Bearer {self._token}"

        # If the action context is available, pass the x-action-context header.

        # TODO: The actions package should have a public API to
        # get the required information (maybe using some for of dependency injection)
        from sema4ai.actions import _action

        action_context = _action.get_current_action_context()
        if action_context:
            headers["X-Action-Context"] = action_context.initial_data

        return headers if headers else None

    def close(self):
        pass

    def get_document_work_item(self, document_id: str) -> Optional[DocumentWorkItem]:
        try:
            # Directly call the API method
            data = self._documents_data_client.get_document_work_item(
                workspace_id=self._workspace_id,
                document_id=document_id,
                _headers=self._headers,
            )
            if data:
                logging.debug(f"Received data for document_id {document_id}: {data}")
                return data
            else:
                logging.warning(f"No data received for document_id {document_id}")
                return None
        except ApiException as e:
            logging.error(f"API error occurred while getting document work item: {e}")
            return None
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            return None

    def get_document_type(self, document_type_name: str) -> Optional["DocType"]:
        try:
            data = self._documents_data_client.get_document_type(
                workspace_id=self._workspace_id,
                document_type_name=document_type_name,
                _headers=self._headers,
            )
            if data:
                logging.debug(f"Received document type: {data}")
                return data
            else:
                logging.warning(
                    f"No data received for document_type_name {document_type_name}"
                )
                return None
        except ApiException as e:
            logging.error(f"API error occurred while getting document type: {e}")
            return None
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            return None

    def get_document_format(
        self, document_type_name: str, document_class_name: str
    ) -> Optional[DocumentFormat]:
        try:
            data = self._documents_data_client.get_document_format(
                workspace_id=self._workspace_id,
                document_type_name=document_type_name,
                document_format_name=document_class_name,
                _headers=self._headers,
            )
            if data:
                # Ensure that the state is parsed correctly
                data.state = DocumentFormatState(data.state)
                logging.debug(f"Received document format: {data}")
                return data
            else:
                logging.warning(
                    f"No data received for document_type_name {document_type_name} and document_class_name {document_class_name}"
                )
                return None
        except ApiException as e:
            logging.error(f"API error occurred while getting document format: {e}")
            return None
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            return None

    def store_extracted_content(self, content: ExtractedDocumentContent) -> None:
        try:
            self._documents_data_client.post_store_extracted_content(
                workspace_id=self._workspace_id,
                extracted_document_content=content,
                _headers=self._headers,
            )
            logging.info(
                f"Successfully stored extracted content for workspace {self._workspace_id}"
            )
        except ApiException as e:
            logging.error(f"API error occurred while storing extracted content: {e}")
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")

    def store_transformed_content(self, content: TransformedDocumentContent) -> None:
        try:
            self._documents_data_client.post_store_transformed_content(
                workspace_id=self._workspace_id,
                transformed_document_content=content,
                _headers=self._headers,
            )
            logging.info(
                f"Successfully stored transformed content for workspace {self._workspace_id}"
            )
        except ApiException as e:
            logging.error(f"API error occurred while storing transformed content: {e}")
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")

    def get_document_content(
        self, document_id: str, content_state: "ContentState"
    ) -> Optional[
        Union[
            RawDocumentContent,
            ExtractedDocumentContent,
            TransformedDocumentContent,
            ComputedDocumentContent,
        ]
    ]:
        try:
            response: GetDocumentContent200Response = (
                self._documents_data_client.get_document_content(
                    workspace_id=self._workspace_id,
                    document_id=document_id,
                    content_state=content_state.value,
                    _headers=self._headers,
                )
            )
            return response.actual_instance
        except ApiException as e:
            logging.error(f"API error occurred while getting document content: {e}")
            return None
        except Exception as e:
            logging.error(
                f"An unexpected error occurred while getting document content: {e}"
            )
            return None

    def remove_document_content(
        self, document_id: str, content_state: "ContentState"
    ) -> None:
        try:
            self._documents_data_client.remove_document_content(
                workspace_id=self._workspace_id,
                document_id=document_id,
                content_state=content_state.value,
                _headers=self._headers,
            )
            logging.info(
                f"Document content removed successfully for document_id {document_id} and content_state {content_state}"
            )
        except ApiException as e:
            logging.error(f"API error occurred while removing document content: {e}")
        except Exception as e:
            logging.error(
                f"An unexpected error occurred while removing document content: {e}"
            )

    def store_computed_content(self, content: ComputedDocumentContent) -> None:
        try:
            self._documents_data_client.post_store_computed_content(
                workspace_id=self._workspace_id,
                computed_document_content=content,
                _headers=self._headers,
            )
            logging.info(
                f"Successfully stored computed content for workspace {self._workspace_id}"
            )
        except ApiException as e:
            logging.error(f"API error occurred while storing computed content: {e}")
        except Exception as e:
            logging.error(
                f"An unexpected error occurred while storing computed content: {e}"
            )

    def work_items_complete_stage(
        self,
        work_item_id: str,
        status: str,
        status_reason: Optional[str] = None,
        log_details_path: Optional[str] = None,
    ):
        """Completes the current stage of a work item and initiates the next stage."""

        # Validate that the status is either 'SUCCESS' or 'FAILURE'
        if status not in ["SUCCESS", "FAILURE"]:
            logging.error(f"Invalid status: {status}. Must be 'SUCCESS' or 'FAILURE'.")
            return None

        # Create the request data with the required fields
        from sema4ai.di_client.agents_events_publisher.models import (
            PostWorkItemsCompleteStageRequest,
        )

        request_data = PostWorkItemsCompleteStageRequest(
            tenant_id=self._workspace_id,
            work_item_id=work_item_id,
            status=status,
            status_reason=status_reason,
            log_details_path=log_details_path,
        )

        try:
            # Call the generated API method to complete the work item stage
            response = self._work_items_client.post_work_items_complete_stage(
                post_work_items_complete_stage_request=request_data,
                _headers=self._headers,
            )
            logging.info(
                f"Successfully completed stage for work_item_id {work_item_id}, moving to next stage."
            )
            return response
        except ApiException as e:
            logging.error(
                f"API error occurred while completing stage for work_item_id {work_item_id}: {e}"
            )
            return None
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            return None
    
    def search_document_fields(
        self, document_id: str, fields_to_search: List[Dict[str, str]]
    ) -> Optional[Dict[str, str]]:
        try:
            # Convert input fields to the required format
            search_request = [
                SearchDocumentFieldsRequestInner(**field) for field in fields_to_search
            ]

            # Call the auto-generated method
            result = self._documents_data_client.search_document_fields(
                workspace_id=self._workspace_id,
                document_id=document_id,
                search_document_fields_request_inner=search_request,
                _headers=self._headers,
            )

            logging.info("Document fields search completed successfully.")
            return result

        except Exception:
            logging.error(f"An error occurred while searching document fields:", exc_info=True)
            return None
    
    def vector_search(
        self, document_id: str, query: str, min_score: Optional[float] = None
    ) -> Optional[List[Dict[str, Any]]]:
        try:
            # Create the request object
            vector_search_request = VectorSearchRequest(query=query, min_score=min_score)

            # Call the auto-generated method
            results = self._documents_data_client.vector_search(
                workspace_id=self._workspace_id,
                document_id=document_id,
                vector_search_request=vector_search_request,
                _headers=self._headers,
            )

            logging.info("Vector search completed successfully.")
            # Convert PageResult objects to dictionaries for easier handling
            return [result.to_dict() for result in results]

        except Exception:
            logging.error(f"An error occurred during vector search:", exc_info=True)
            return None
