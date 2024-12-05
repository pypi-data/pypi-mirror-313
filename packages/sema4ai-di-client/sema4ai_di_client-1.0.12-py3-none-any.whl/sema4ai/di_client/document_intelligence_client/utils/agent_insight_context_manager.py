import time
from contextlib import contextmanager
import logging
from typing import Optional, Any, Dict, Callable, TypeVar
from sema4ai.di_client.document_intelligence_client.utils.models import ProcessingPhase, ProcessingEvent, ProcessingSummary, AgentInsightContext, ProcessingContext
from datetime import datetime
import functools

F = TypeVar("F", bound=Callable[..., Any])

class AgentInsightContextManager:
    """
    Manages the tracking of insights, metrics, and events throughout the document processing lifecycle.

    This class provides agents with real-time contextual information during document processing,
    enabling them to diagnose issues, identify discrepancies, and offer recommendations or resolutions.
    It tracks key processing phases (e.g., extraction, transformation, validation), logs events, 
    manages metrics, and streams relevant information back to the agent.

    Use Case:
    - Track processing phases and metrics across a document’s lifecycle.
    - Provide agents with insights to help diagnose issues when extractions fail or discrepancies occur.
    - Stream processing events and logs to the agent in real-time to support informed decision-making.

    Attributes:
        agent_insight (AgentInsightContext): 
            Stores the contextual insights gathered during the document's processing.
        current_phase (Optional[ProcessingPhase]): 
            Keeps track of the current processing phase.
        logger (logging.Logger): 
            Logger used for recording events and warnings.

    Methods:
        start_phase(phase): Begin tracking a processing phase.
        end_phase(): Mark the end of the current phase.
        add_event(event_type, description, details): Log an event during the current phase.
        update_metrics(metrics_update): Update metrics associated with the current phase.
        add_warning(warning): Log a warning during the current phase.
        add_error(error): Log an error during the current phase.
        track_method_execution(method_name): Decorator to track the execution time of methods.
        phase_context(phase): Context manager to automatically start and end phases.
        get_agent_context(): Retrieve the collected insights for the processed document.
    """

    def __init__(self, document_id: str, document_name: str):
        self.agent_insight = AgentInsightContext(document_id=document_id, document_name=document_name)
        self.current_phase: Optional[ProcessingPhase] = None
        self.logger = logging.getLogger(__name__)

    def start_phase(self, phase: ProcessingPhase):
        """
        Start tracking a new processing phase.

        Args:
            phase (ProcessingPhase): The phase of the document processing to begin.
        """
        self.current_phase = phase
        context = ProcessingContext(
            document_id=self.agent_insight.document_id,
            document_name=self.agent_insight.document_name,
            processing_phase=phase,
            summary=ProcessingSummary(phase=phase, start_time=datetime.utcnow())
        )
        setattr(self.agent_insight, f"{phase.value.lower()}_context", context)

    def end_phase(self):
        """End the current processing phase and record its end time."""
        if self.current_phase:
            context_name = f"{self.current_phase.value.lower()}_context"
            context = getattr(self.agent_insight, context_name, None)
            if context and context.summary:
                context.summary.end_time = datetime.utcnow()
            self.current_phase = None

    def add_event(self, event_type: str, description: str, details: Optional[Dict[str, Any]] = None):
        """Log an event within the current processing phase."""
        if self.current_phase:
            context = getattr(self.agent_insight, f"{self.current_phase.value.lower()}_context")
            if context and context.summary:
                context.summary.processing_events.append(
                    ProcessingEvent(event_type=event_type, description=description, details=details)
                )

    def update_metrics(self, metrics_update: Dict[str, Any]):
        """Update metrics associated with the current phase."""
        if self.current_phase:
            context_name = f"{self.current_phase.value.lower()}_context"
            context = getattr(self.agent_insight, context_name, None)
            if context and context.summary and context.summary.data_metrics:
                for key, value in metrics_update.items():
                    setattr(context.summary.data_metrics, key, value)
            else:
                self.logger.warning(f"Unable to update metrics: {context_name} not found or incomplete")
        else:
            self.logger.warning("Unable to update metrics: No current phase set")

    def add_warning(self, warning: str):
        """Log a warning within the current phase."""
        if self.current_phase:
            context = getattr(self.agent_insight, f"{self.current_phase.value.lower()}_context")
            if context and context.summary:
                context.summary.warnings.append(warning)

    def add_error(self, error: str):
        """Log an error within the current phase."""
        if self.current_phase:
            context = getattr(self.agent_insight, f"{self.current_phase.value.lower()}_context")
            if context and context.summary:
                context.summary.errors.append(error)

    @classmethod
    def track_method_execution(cls, method_name: str) -> Callable[[F], F]:
        """
        Decorator to track the execution time of methods.

        Args:
            method_name (str): The name of the method being tracked.

        Returns:
            A wrapped function that logs its execution time as an event.
        """
        def decorator(func: F) -> F:
            @functools.wraps(func)
            def wrapper(self, *args, **kwargs):
                start_time = time.time()
                result = func(self, *args, **kwargs)
                end_time = time.time()
                execution_time = end_time - start_time

                if hasattr(self, 'insight_tracker'):
                    self.insight_tracker.add_event(
                        f"{method_name} execution", f"Executed in {execution_time:.2f} seconds"
                    )

                return result
            return wrapper # type: ignore 
        return decorator

    @contextmanager
    def phase_context(self, phase: ProcessingPhase):
        """Context manager to automatically start and end a phase."""
        self.start_phase(phase)
        try:
            yield
        finally:
            self.end_phase()

    def get_agent_insight_context(self) -> AgentInsightContext:
        """
        Retrieve the collected insights for the processed document.

        Returns:
            AgentInsightContext: The context object containing all relevant insights 
            and events for the document's processing lifecycle.
        """
        return self.agent_insight
