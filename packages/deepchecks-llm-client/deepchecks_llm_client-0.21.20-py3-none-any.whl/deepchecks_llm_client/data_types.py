import enum
import logging
from dataclasses import dataclass

__all__ = ["EnvType", "AnnotationType", "Interaction", "Step", "StepType", "Application",
           "ApplicationType", "ApplicationVersion", "ApplicationVersionSchema", "LogInteractionType",
           "PropertyColumnType", "CustomPropertyType", "InteractionCompleteEvents"]

from datetime import datetime
from typing import Any, Dict, List, Optional, Union

import pytz

logging.basicConfig()
logger = logging.getLogger(__name__)


class EnvType(str, enum.Enum):
    PROD = "PROD"
    EVAL = "EVAL"
    PENTEST = "PENTEST"


class AnnotationType(str, enum.Enum):
    GOOD = "good"
    BAD = "bad"
    UNKNOWN = "unknown"


class PropertyColumnType(str, enum.Enum):
    CATEGORICAL = "categorical"
    NUMERIC = "numeric"


@dataclass
class Interaction:
    user_interaction_id: str
    input: str
    information_retrieval: str
    history: str
    full_prompt: str
    output: str
    topic: str
    output_properties: Dict[str, Any]
    input_properties: Dict[str, Any]
    custom_properties: Dict[str, Any]
    llm_properties: Dict[str, Any]
    llm_properties_reasons: Dict[str, Any]
    created_at: datetime
    interaction_datetime: datetime
    is_completed: bool


class StepType(str, enum.Enum):
    LLM = "LLM"
    INFORMATION_RETRIEVAL = "INFORMATION_RETRIEVAL"
    TRANSFORMATION = "TRANSFORMATION"
    FILTER = "FILTER"
    FINE_TUNING = "FINE_TUNING"
    PII_REMOVAL = "PII_REMOVAL"
    UDF = "UDF"


@dataclass
class Step:
    name: str
    type: Union[StepType, None] = None
    attributes: Union[Dict[str, Any], None] = None
    started_at: Union[datetime, float, None] = None
    annotation: Union[AnnotationType, str, None] = None
    finished_at: Union[datetime, float, None] = None
    input: Union[str, None] = None
    output: Union[str, None] = None
    error: Union[str, None] = None

    def to_json(self):
        return {
            "name": self.name,
            "annotation": (
                None if self.annotation is None else
                self.annotation.value if isinstance(self.annotation, AnnotationType) else self.annotation.lower().strip()
            ),
            "type": self.type.value if isinstance(self.type, StepType) else self.type,
            "attributes": self.attributes,
            "started_at": self.started_at.timestamp() if isinstance(self.started_at, datetime) else self.started_at,
            "finished_at": self.finished_at.timestamp() if isinstance(self.finished_at, datetime) else self.finished_at,
            "input": self.input,
            "output": self.output,
            "error": self.error,
        }

    @classmethod
    def as_jsonl(cls, steps):
        if steps is None:
            return None
        return [step.to_json() for step in steps]


@dataclass
class LogInteractionType:
    """A dataclass representing an interaction.

    Attributes
    ----------
    input : str
        Input data
    output : str
        Output data
    full_prompt : str, optional
        Full prompt data, defaults to None
    annotation : AnnotationType, optional
        Annotation type of the interaction, defaults to None
    user_interaction_id : str, optional
        Unique identifier of the interaction, defaults to None
    steps : list of Step, optional
        List of steps taken during the interaction, defaults to None
    custom_props : dict, optional
        Additional custom properties, defaults to None
    information_retrieval : str, optional
        Information retrieval, defaults to None
    history : str, optional
        History (for instance "chat history"), defaults to None
    annotation_reason : str, optional
        Reason for the annotation, defaults to None
    started_at : datetime or float, optional
        Timestamp the interaction started at. Datetime format is deprecated, use timestamp instead
    finished_at : datetime or float, optional
        Timestamp the interaction finished at. Datetime format is deprecated, use timestamp instead
    vuln_type : str, optional
        Type of vulnerability (Only used in case of EnvType.PENTEST and must be sent there), defaults to None
    vuln_trigger_str : str, optional
        Vulnerability trigger string (Only used in case of EnvType.PENTEST and is optional there), defaults to None
    """

    input: Optional[str] = None
    output: Optional[str] = None
    full_prompt: Optional[str] = None
    annotation: Optional[Union[AnnotationType, str]] = None
    user_interaction_id: Optional[str] = None
    steps: Optional[List[Step]] = None
    custom_props: Optional[Dict[str, Any]] = None
    information_retrieval: Optional[Union[str, List[str]]] = None
    history: Optional[Union[str, List[str]]] = None
    annotation_reason: Optional[str] = None
    started_at: Optional[Union[datetime, float]] = None
    finished_at: Optional[Union[datetime, float]] = None
    vuln_type: Optional[str] = None
    vuln_trigger_str: Optional[str] = None
    topic: Optional[str] = None
    is_completed: bool = True

    def to_json(self):
        if isinstance(self.started_at, datetime) or isinstance(self.finished_at, datetime):
            logger.warning(
                "Deprecation Warning: Usage of datetime for started_at/finished_at is deprecated, use timestamp instead."
            )
            self.started_at = self.started_at.timestamp() if self.started_at else datetime.now(tz=pytz.UTC).timestamp()
            self.finished_at = self.finished_at.timestamp() if self.finished_at else None

        data = {
            "input": self.input,
            "output": self.output,
            "full_prompt": self.full_prompt,
            "information_retrieval": self.information_retrieval \
                if self.information_retrieval is None or isinstance(self.information_retrieval, list) \
                else [self.information_retrieval],
            "history": self.history \
                if self.history is None or isinstance(self.history, list) \
                else [self.history],
            "annotation": self.annotation.value if isinstance(self.annotation, AnnotationType) else self.annotation,
            "user_interaction_id": self.user_interaction_id,
            "steps": [step.to_json() for step in self.steps] if self.steps else None,
            "custom_props": self.custom_props,
            "annotation_reason": self.annotation_reason,
            "vuln_type": self.vuln_type,
            "vuln_trigger_str": self.vuln_trigger_str,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "is_completed": self.is_completed,
        }
        if self.topic is not None:
            data["topic"] = self.topic

        return data


@dataclass
class CustomPropertyType:
    display_name: str
    type: PropertyColumnType
    description: str


class ApplicationType(str, enum.Enum):
    QA = "Q&A"
    OTHER = "OTHER"
    SUMMARIZATION = "SUMMARIZATION"
    GENERATION = "GENERATION"
    CLASSIFICATION = "CLASSIFICATION"


class InteractionCompleteEvents(str, enum.Enum):
    TOPICS_COMPLETED = "topics_completed"
    PROPERTIES_COMPLETED = "properties_completed"
    SIMILARITY_COMPLETED = "similarity_completed"
    LLM_PROPERTIES_COMPLETED = "llm_properties_completed"
    ANNOTATION_COMPLETED = "annotation_completed"
    DC_EVALUATION_COMPLETED = "dc_evaluation_completed"


@dataclass
class ApplicationVersionSchema:
    name: str
    description: Optional[str] = None
    additional_fields: Optional[Dict[str, Any]] = None

    def to_json(self):
        return {
            "name": self.name,
            "description": self.description,
            "custom": [{key: value} for key, value in self.additional_fields.items()] if self.additional_fields else []
        }


@dataclass
class ApplicationVersion:
    id: int
    name: str
    ai_model: str
    created_at: datetime
    updated_at: datetime
    description: Optional[str] = None
    custom: Optional[List[Dict[str, Any]]] = None


@dataclass
class Application:
    id: int
    name: str
    kind: ApplicationType
    created_at: datetime
    updated_at: datetime
    in_progress: bool
    versions: List[ApplicationVersion]
    description: Optional[str] = None
    log_latest_insert_time_epoch: Optional[int] = None
    n_of_llm_properties: Optional[int] = None
    n_of_interactions: Optional[int] = None
    notifications_enabled: Optional[bool] = None
