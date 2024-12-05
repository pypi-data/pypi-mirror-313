from enum import Enum
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field
from datetime import datetime
from sema4ai.di_client.document_intelligence_client.models.extracted_document_content import ExtractedDocumentContent
from sema4ai.di_client.document_intelligence_client.models.transformed_document_content import TransformedDocumentContent
from sema4ai.di_client.document_intelligence_client.models.computed_document_content import ComputedDocumentContent

class ProcessingPhase(str, Enum):
    EXTRACTION = "Extraction"
    TRANSFORMATION = "Transformation"
    VALIDATION = "Validation"

class ValidationSeverity(str, Enum):
    ERROR = "Error"
    WARNING = "Warning"
    INFO = "Info"

class ProcessingEvent(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    event_type: Optional[str] = None
    description: Optional[str] = None
    details: Optional[Dict[str, Any]] = None

class DataMetrics(BaseModel):
    metrics: Dict[str, Any] = Field(default_factory=dict)

    def __setattr__(self, name: str, value: Any) -> None:
        if name == "metrics":
            super().__setattr__(name, value)
        else:
            self.metrics[name] = value

    def __getattr__(self, name: str) -> Any:
        return self.metrics.get(name)

class PreprocessingSummary(BaseModel):
    page_patterns_compiled: Optional[bool] = False
    header_identification_method: Optional[str] = None
    charge_type_sections_identified: Optional[List[str]] = Field(default=None)

class TableExtractionMetrics(BaseModel):
    tables_per_page: Optional[Dict[int, int]] = Field(default=None)
    empty_columns_dropped: Optional[List[str]] = Field(default=None)
    columns_renamed: Optional[Dict[str, str]] = Field(default=None)

class ValidationCheckpoint(BaseModel):
    stage: Optional[str] = None
    checks_performed: Optional[List[str]] = Field(default=None)
    checks_passed: Optional[List[str]] = Field(default=None)
    checks_failed: Optional[List[str]] = Field(default=None)

class TransformationStep(BaseModel):
    step_name: Optional[str] = None
    rows_affected: Optional[int] = 0
    calculation_performed: Optional[str] = None

class DataQualityIndicators(BaseModel):
    completeness: float = Field(0.0, ge=0, le=1)
    consistency: float = Field(0.0, ge=0, le=1)
    accuracy: float = Field(0.0, ge=0, le=1)

class ValidationResult(BaseModel):
    rule_id: str
    passed: bool
    message: str
    severity: ValidationSeverity
    details: Dict[str, Any] = Field(default_factory=dict)

class ValidationResults(BaseModel):
    overall_status: Optional[bool] = None
    rules_passed: int = 0
    rules_failed: int = 0
    results: List[ValidationResult] = Field(default_factory=list)

    def add_result(self, rule_id: str, passed: bool, message: str, severity: ValidationSeverity, details: Optional[Dict[str, Any]] = None):
        self.results.append(ValidationResult(
            rule_id=rule_id,
            passed=passed,
            message=message,
            severity=severity,
            details=details or {}
        ))
        if passed:
            self.rules_passed += 1
        else:
            self.rules_failed += 1
        self.overall_status = self.rules_failed == 0

class ProcessingSummary(BaseModel):
    phase: Optional[ProcessingPhase] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    processing_events: List[ProcessingEvent] = Field(default_factory=list)
    data_metrics: DataMetrics = Field(default_factory=DataMetrics)
    warnings: List[str] = Field(default_factory=list)
    errors: List[str] = Field(default_factory=list)
    preprocessing_summary: Optional[PreprocessingSummary] = None
    table_extraction_metrics: Optional[TableExtractionMetrics] = None
    validation_checkpoints: List[ValidationCheckpoint] = Field(default_factory=list)
    transformation_steps: List[TransformationStep] = Field(default_factory=list)
    performance_metrics: Dict[str, float] = Field(default_factory=dict)
    data_quality_indicators: DataQualityIndicators = Field(default_factory=lambda: DataQualityIndicators()) # type: ignore 

class ProcessingContext(BaseModel):
    document_id: Optional[str] = None
    document_name: Optional[str] = None
    processing_phase: Optional[ProcessingPhase] = None
    summary: ProcessingSummary = Field(default_factory=lambda: ProcessingSummary())
    validation_results: ValidationResults = Field(default_factory=ValidationResults)
    configuration_used: Dict[str, Any] = Field(default_factory=dict)
    additional_context: Dict[str, Any] = Field(default_factory=dict)

class AgentInsightContext(BaseModel):
    document_id: Optional[str] = None
    document_name: Optional[str] = None
    extraction_context: Optional[ProcessingContext] = None
    transformation_context: Optional[ProcessingContext] = None
    validation_context: Optional[ProcessingContext] = None
    final_validation_results: Optional[ValidationResults] = None
    overall_processing_time: float = 0.0
    overall_status: Optional[str] = None

class PhaseResult(BaseModel):
    agent_insight_context: Optional[AgentInsightContext] = None
    content: Optional[Union[ExtractedDocumentContent, TransformedDocumentContent, ComputedDocumentContent]] = None

class ExtractionResult(PhaseResult):
    content: Optional[ExtractedDocumentContent] = None

class TransformationResult(PhaseResult):
    content: Optional[TransformedDocumentContent] = None

class ValidationFinalResult(PhaseResult):
    content: Optional[ComputedDocumentContent] = None
