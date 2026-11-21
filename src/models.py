from dataclasses import dataclass, field, fields, is_dataclass
from datetime import date, datetime, timezone
from enum import Enum
from typing import Any, Dict, Optional, Tuple


def to_dict(obj: Any) -> Any:
    """Recursively convert CRS dataclasses, enums, and dates to JSON-safe values."""
    if isinstance(obj, Enum):
        return obj.value
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    if is_dataclass(obj):
        return {f.name: to_dict(getattr(obj, f.name)) for f in fields(obj)}
    if isinstance(obj, dict):
        return {str(k): to_dict(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple, set)):
        return [to_dict(v) for v in obj]
    return obj


class EpistemicState(str, Enum):
    OBSERVED = "OBSERVED"
    REPORTED = "REPORTED"
    INTERPRETED = "INTERPRETED"
    HYPOTHESIZED = "HYPOTHESIZED"
    INFERRED = "INFERRED"
    SUPPORTED = "SUPPORTED"
    CONTESTED = "CONTESTED"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    UNKNOWN = "UNKNOWN"


class Polarity(str, Enum):
    POSITIVE = "POSITIVE"
    NEGATIVE = "NEGATIVE"
    UNKNOWN = "UNKNOWN"


class ActorRole(str, Enum):
    BOOTSTRAP = "BOOTSTRAP"
    LANGUAGE_ADAPTER = "LANGUAGE_ADAPTER"
    REASONING_ENGINE = "REASONING_ENGINE"
    COGNITIVE_SUPERVISOR = "COGNITIVE_SUPERVISOR"
    CONCEPT_EVOLUTION = "CONCEPT_EVOLUTION"
    AEE = "AEE"  # Architecture Evolution Engine (blocked from direct writes)


@dataclass(frozen=True)
class TemporalWindow:
    valid_from: Optional[date] = None
    valid_to: Optional[date] = None
    knowledge_time: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    def is_valid_on(self, target: date) -> bool:
        if self.valid_from and target < self.valid_from:
            return False
        if self.valid_to and target > self.valid_to:
            return False
        return True


@dataclass(frozen=True)
class Concept:
    id: str
    canonical: str
    version: int = 1
    labels: Dict[str, Tuple[str, ...]] = field(default_factory=dict)
    defaults: Tuple[str, ...] = field(default_factory=tuple)
    exceptions: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class Entity:
    id: str
    concept_id: str
    labels: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class Event:
    id: str
    event_type: str
    participants: Dict[str, str]
    temporal: TemporalWindow
    source_id: str


@dataclass(frozen=True)
class Source:
    id: str
    source_type: str
    name: str
    reliability: str = "unassessed"


@dataclass(frozen=True)
class ProvenanceNode:
    id: str
    kind: str  # source, observation, claim, inference
    summary: str
    derived_from: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class Claim:
    id: str
    subject_id: str
    relation: str
    object_value: Any
    epistemic_state: EpistemicState
    polarity: Polarity = Polarity.POSITIVE
    source_id: Optional[str] = None
    context: Dict[str, str] = field(default_factory=dict)
    temporal: TemporalWindow = field(default_factory=TemporalWindow)
    uncertainty: Dict[str, str] = field(default_factory=dict)
    provenance_id: Optional[str] = None


@dataclass(frozen=True)
class EpistemicLink:
    id: str
    relation: str  # supports, contradicts, derived-from
    from_id: str
    to_id: str
    note: str = ""


@dataclass(frozen=True)
class LineageEdge:
    from_concept_id: str
    to_concept_id: str
    operation: str  # REFINE, SPLIT, MERGE, DEPRECATE
    reason: str


@dataclass(frozen=True)
class VectorAttachment:
    vector_id: str
    object_id: str
    model: str
    values: Tuple[float, ...]
