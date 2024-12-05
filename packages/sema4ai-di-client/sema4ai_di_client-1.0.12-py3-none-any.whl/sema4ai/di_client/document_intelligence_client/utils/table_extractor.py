import logging
import re
import pandas as pd

from io import StringIO
from typing import List, Dict, Optional
from sema4ai.di_client.document_intelligence_client.models.raw_document_content_all_of_raw_content import RawDocumentContentAllOfRawContent
from sema4ai.di_client.document_intelligence_client.models.source_document import SourceDocument
from sema4ai.di_client.document_intelligence_client.utils.agent_insight_context_manager import AgentInsightContextManager

# Define the regex pattern for extracting table sections
TABLE_REGEX_PATTERN = r'<!--SOT-->(.*?)<!--EOT-->'


class TableExtractor:
    def __init__(self, document: SourceDocument, insight_tracker: AgentInsightContextManager):
        self._logger: logging.Logger = logging.getLogger(__name__)
        self.document: SourceDocument = document
        self.insight_tracker: AgentInsightContextManager = insight_tracker

    @AgentInsightContextManager.track_method_execution(method_name="extract_tables_from_pages")
    def extract_tables_from_pages(
        self, raw_content_pages: List[RawDocumentContentAllOfRawContent]
    ) -> List[Dict[str, object]]:
        self.insight_tracker.add_event(
            "Table Extraction Start", f"Beginning extraction from {len(raw_content_pages)} pages"
        )

        all_tables: List[Dict[str, object]] = []

        for page in raw_content_pages:
            # Check for None and ensure page.text is a string before calling _extract_tables_from_page
            if page.text is not None and page.page_num is not None:
                tables = self._extract_tables_from_page(page.text, page.page_num)
                all_tables.append({
                    "page_num": page.page_num,
                    "tables": tables
                })
            else:
                self._logger.warning(f"Page {page.page_num} has no text content, skipping table extraction.")

        return all_tables

    @AgentInsightContextManager.track_method_execution(method_name="_extract_tables_from_page")
    def _extract_tables_from_page(self, page_text: str, page_num: str) -> List[List[Dict[str, object]]]:
        # Ensure page_text is a string
        if not isinstance(page_text, str):
            self._logger.error(f"Invalid page text on page {page_num}: Expected a string, got {type(page_text)}")
            return []

        self.insight_tracker.add_event(
            "Page Processing Start", f"Processing page {page_num}"
        )

        table_sections: List[str] = re.findall(TABLE_REGEX_PATTERN, page_text, re.DOTALL)
        self.insight_tracker.add_event(
            "Table Sections Found", f"Found {len(table_sections)} table sections on page {page_num}"
        )

        tables: List[List[Dict[str, object]]] = []

        for i, table_section in enumerate(table_sections, 1):
            df = self._process_table_section(table_section, page_num, i)
            if df is not None and not df.empty:
                self._logger.info(
                    f"Found Table {i} on page {page_num} with {len(df)} rows and {len(df.columns)} columns"
                )
                tables.append([dict((str(k), v) for k, v in row.items()) for row in df.to_dict(orient="records")])
            else:
                self._logger.info(f"Table {i} on page {page_num} is empty")

        self.insight_tracker.add_event(
            "Page Processing Complete", f"Found {len(tables)} valid tables from page {page_num}"
        )
        return tables

    def _process_table_section(self, table_section: str, page_num: str, table_num: int) -> Optional[pd.DataFrame]:
        try:
            df: pd.DataFrame = pd.read_csv(
                StringIO(table_section),
                sep="|",
                skipinitialspace=True,
                dtype=object,
                on_bad_lines="skip",
                escapechar="\\",
            ).iloc[1:]
            df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x) # type: ignore 
            df.columns = df.columns.str.strip("*_ ")  # Remove md formatting and white space
            df = df.iloc[:, 1:-1]  # Drop first and last column since they are always empty
            df = df.apply(lambda col: col.where(pd.notna(col), None))

            self.insight_tracker.add_event(
                "Table Processed", f"Processed table {table_num} from page {page_num} with {len(df)} rows and {len(df.columns)} columns"
            )
            return df
        except Exception as e:
            self._logger.error(f"Error processing table {table_num} on page {page_num}: {e}")
            return None
