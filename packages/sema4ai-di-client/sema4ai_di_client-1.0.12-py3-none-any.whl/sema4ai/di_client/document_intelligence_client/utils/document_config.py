import logging
import pandas as pd
from typing import List, Dict, Any, Tuple, Optional
from sema4ai.di_client.document_intelligence_client.models.doc_type import DocType
from sema4ai.di_client.document_intelligence_client.models.document_format import DocumentFormat
from sema4ai.di_client.document_intelligence_client.utils.agent_insight_context_manager import AgentInsightContextManager


class DocumentIntelligenceUtility:
    """
    A utility class for working with DocumentType and DocumentFormat mappings and data processing.

    Terminology:
    - DocumentType (or Type): The standardized schema that defines the structure of the document data.
    - DocumentFormat (or Format): The specific format of a document, which may vary between different sources or systems.

    Mapping Directions:
    - Type to Format: Mapping from the standardized DocumentType fields to the specific DocumentFormat fields.
    - Format to Type: Mapping from the specific DocumentFormat fields to the standardized DocumentType fields.

    This utility provides methods for:
    1. Checking field mappings between DocumentType and DocumentFormat.
    2. Identifying mapped and unmapped fields.
    3. Mapping data between DocumentFormat and DocumentType.
    4. Extracting tables from raw document content.
    5. Accessing custom configuration.

    Note: This utility assumes that field names are unique across all tables and non-table fields within a DocumentType.
    When a method doesn't explicitly mention Type or Format in its name, it typically works with 
    DocumentType as the base and checks for mappings to DocumentFormat.
    """

    def __init__(self, document_type: DocType, document_format: DocumentFormat, insight_tracker: AgentInsightContextManager) -> None:
        # Initialize the utility with DocumentType, DocumentFormat, and an insight tracker
        self._document_type: DocType = document_type
        self._document_format: DocumentFormat = document_format
        self._logger: logging.Logger = logging.getLogger(__name__)
        self.insight_tracker: AgentInsightContextManager = insight_tracker

    @AgentInsightContextManager.track_method_execution(method_name="has_field_mapping")
    def has_field_mapping(self, field_name: str) -> bool:
        """
        Check if a field has a mapping between DocumentType and DocumentFormat.

        This method checks both non-table fields and table fields for a mapping.

        Args:
            field_name (str): The name of the field in DocumentType to check.

        Returns:
            bool: True if the DocumentType field has a mapping to a DocumentFormat field, False otherwise.
        """
        self.insight_tracker.add_event("Field Mapping Check", f"Checking mapping for field: {field_name}")

        # Check non-table fields
        for field_mapping in self._document_format.non_tbl_fields_mapping:
            if field_mapping.field_name == field_name:
                self._logger.debug(f"Field '{field_name}' has a non-table mapping")
                self.insight_tracker.add_event("Field Mapping Found", f"Field '{field_name}' has a non-table mapping")
                return True

        # Check table fields
        for table in self._document_format.tables:
            for tbl_field_mapping in table.tbl_fields_mapping:
                if tbl_field_mapping.source == field_name:
                    if tbl_field_mapping.output:  # Check if the output is not empty
                        self._logger.debug(f"Field '{field_name}' has a table mapping")
                        self.insight_tracker.add_event("Field Mapping Found", f"Field '{field_name}' has a table mapping")
                        return True
                    else:
                        self.insight_tracker.add_warning(f"Field '{field_name}' has an empty output mapping")

        self.insight_tracker.add_event("Field Mapping Not Found", f"Field '{field_name}' has no mapping")
        return False

    @AgentInsightContextManager.track_method_execution(method_name="is_field_required")
    def is_field_required(self, field_name: str) -> bool:
        """
        Check if a field (either non-table or table) is configured to be required.

        Args:
            field_name (str): The name of the field to check.

        Returns:
            bool: True if the field is required, False otherwise.
        """
        self.insight_tracker.add_event("Field Requirement Check", f"Checking if field '{field_name}' is required")

        # Check non-table fields
        for field in self._document_type.non_tbl_fields or []:
            if field.name == field_name:
                is_required = field.requirement == "Required"
                self.insight_tracker.add_event("Field Requirement Result", f"Non-table field '{field_name}' is {'required' if is_required else 'not required'}")
                return is_required

        # Check table fields
        for table in self._document_type.tbl_fields or []:
            for tbl_field in table.table_definition:
                if tbl_field.column == field_name:
                    is_required = tbl_field.requirement == "Required"
                    self.insight_tracker.add_event("Field Requirement Result", f"Table field '{field_name}' is {'required' if is_required else 'not required'}")
                    return is_required

        self.insight_tracker.add_warning(f"Field '{field_name}' not found in DocumentType")
        return False

    @AgentInsightContextManager.track_method_execution(method_name="get_unmapped_fields")
    def get_unmapped_fields(self) -> Tuple[List[str], List[str]]:
        """
        Get all DocumentType fields that do not have a mapping to DocumentFormat fields.

        This method checks both non-table fields and table fields for mappings.

        Returns:
            Tuple[List[str], List[str]]: A tuple containing:
                - A list of unmapped non-table DocumentType fields
                - A list of unmapped table DocumentType fields
        """
        unmapped_non_table: List[str] = [
            field.name for field in self._document_type.non_tbl_fields or [] if not self.has_field_mapping(field.name)
        ]
        unmapped_table: List[str] = []
        for table in self._document_type.tbl_fields or []:
            unmapped_table.extend(
                [field.column for field in table.table_definition if not self.has_field_mapping(field.column)]
            )
        return unmapped_non_table, unmapped_table

    @AgentInsightContextManager.track_method_execution(method_name="get_mapped_fields")
    def get_mapped_fields(self) -> Tuple[List[str], List[str]]:
        """
        Get all DocumentType fields that have a mapping to DocumentFormat fields.

        This method checks both non-table fields and table fields for mappings.

        Returns:
            Tuple[List[str], List[str]]: A tuple containing:
                - A list of mapped non-table DocumentType fields
                - A list of mapped table DocumentType fields
        """
        mapped_non_table: List[str] = [
            field.name for field in self._document_type.non_tbl_fields or [] if self.has_field_mapping(field.name)
        ]
        mapped_table: List[str] = []
        for table in self._document_type.tbl_fields or []:
            mapped_table.extend(
                [field.column for field in table.table_definition if self.has_field_mapping(field.column)]
            )
        return mapped_non_table, mapped_table

    @AgentInsightContextManager.track_method_execution(method_name="map_format_to_type_field")
    def map_format_to_type_field(self, format_field: str) -> Optional[str]:
        """
        Map a DocumentFormat field name to its corresponding DocumentType field name.

        This method checks both non-table fields and table fields for the mapping.

        Args:
            format_field (str): The name of the field in DocumentFormat.

        Returns:
            Optional[str]: The corresponding DocumentType field name, or None if not found.
        """
        for field_mapping in self._document_format.non_tbl_fields_mapping:
            if field_mapping.field_identifier == format_field:
                return field_mapping.field_name
        for table in self._document_format.tables:
            for tbl_field_mapping in table.tbl_fields_mapping:
                if tbl_field_mapping.output == format_field:
                    return tbl_field_mapping.source
        return None

    @AgentInsightContextManager.track_method_execution(method_name="map_type_to_format_field")
    def map_type_to_format_field(self, type_field: str) -> Optional[str]:
        """
        Map a DocumentType field name to its corresponding DocumentFormat field name.

        This method checks both non-table fields and table fields for the mapping.

        Args:
            type_field (str): The name of the field in DocumentType.

        Returns:
            Optional[str]: The corresponding DocumentFormat field name, or None if not found.
        """
        self.insight_tracker.add_event("Field Mapping", f"Mapping DocumentType field '{type_field}' to DocumentFormat")

        # Check non-table fields
        for field_mapping in self._document_format.non_tbl_fields_mapping:
            if field_mapping.field_name == type_field:
                self.insight_tracker.add_event("Field Mapping Result", f"Mapped '{type_field}' to '{field_mapping.field_identifier}'")
                return field_mapping.field_identifier

        # Check table fields
        for table in self._document_format.tables:
            for tbl_field_mapping in table.tbl_fields_mapping:
                if tbl_field_mapping.source == type_field:
                    self.insight_tracker.add_event("Field Mapping Result", f"Mapped '{type_field}' to '{tbl_field_mapping.output}'")
                    return tbl_field_mapping.output

        self.insight_tracker.add_warning(f"No mapping found for DocumentType field '{type_field}'")
        return None

    @AgentInsightContextManager.track_method_execution(method_name="process_format_data")
    def process_format_data(
        self, format_data: Dict[str, Any], format_tables: Dict[str, pd.DataFrame]
    ) -> Tuple[Dict[str, Any], Dict[str, pd.DataFrame]]:
        """
        Process the DocumentFormat data and tables, mapping them to DocumentType format.
        
        This method handles both non-table data and table data, mapping field names from
        DocumentFormat to DocumentType.

        Args:
            format_data (Dict[str, Any]): Non-table field data in DocumentFormat.
            format_tables (Dict[str, pd.DataFrame]): Table data in DocumentFormat.

        Returns:
            Tuple[Dict[str, Any], Dict[str, pd.DataFrame]]: A tuple containing:
                - Non-table data mapped to DocumentType
                - Table data mapped to DocumentType
        """
        type_data: Dict[str, Any] = {
            key: value
            for field, value in format_data.items()
            if (key := self.map_format_to_type_field(field)) is not None
        }
        type_tables: Dict[str, pd.DataFrame] = {}
        for table_name, table_data in format_tables.items():
            mapped_columns = {
                col: self.map_format_to_type_field(col) for col in table_data.columns if self.map_format_to_type_field(col)
            }
            type_tables[table_name] = table_data.rename(columns=mapped_columns)
        return type_data, type_tables

    @AgentInsightContextManager.track_method_execution(method_name="get_custom_config")
    def get_custom_config(self) -> Dict[str, Any]:
        """
        Retrieve the custom configuration for this DocumentFormat.

        Returns:
            Dict[str, Any]: A dictionary containing the custom configuration.
        """
        return self._document_format.custom_config

    @AgentInsightContextManager.track_method_execution(method_name="get_custom_config_value")
    def get_custom_config_value(self, key: str, default: Optional[Any] = None) -> Any:
        """
        Retrieve a specific value from the custom configuration for this DocumentFormat.

        Args:
            key (str): The key for the custom configuration value.
            default (Optional[Any]): The default value to return if the key is not found.

        Returns:
            Any: The value associated with the key, or the default value if the key is not found.
        """
        self.insight_tracker.add_event("Custom Config Retrieval", f"Retrieving custom config value for key: {key}")
        custom_config = self._document_format.custom_config
        value = custom_config.get(key, default)
        if value is not None:
            self.insight_tracker.add_event("Custom Config Result", f"Found value for key '{key}'")
        else:
            self.insight_tracker.add_warning(f"No value found for custom config key '{key}', using default")
        return value
