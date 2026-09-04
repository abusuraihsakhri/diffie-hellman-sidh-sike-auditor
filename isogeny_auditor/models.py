"""
Data Models & Telemetry Definitions for Isogeny Cryptanalysis & SIDH/SIKE Vulnerability Auditor Agent.
Domain: Post-Quantum Cryptography & Zero-Knowledge
Standard: Supersingular Isogeny Cryptography
"""
import datetime
import math
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any


class ExecutionStatus(str, Enum):
    NOMINAL = "NOMINAL_OPTIMAL"
    ELEVATED_RISK = "ELEVATED_RISK_WARNING"
    CRITICAL_INTERVENTION = "CRITICAL_INTERVENTION_REQUIRED"


@dataclass
class FrontierPayload:
    task_id: str
    target_identifier: str
    primary_metric: float
    secondary_metric: float
    status_descriptor: str
    is_critical_flag: bool = False
    attributes: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())

    def __post_init__(self):
        """Validate field values after initialization."""
        if not math.isfinite(self.primary_metric):
            raise ValueError(f"primary_metric must be finite, got {self.primary_metric}")
        if not math.isfinite(self.secondary_metric):
            raise ValueError(f"secondary_metric must be finite, got {self.secondary_metric}")
        if not self.task_id or not self.task_id.strip():
            raise ValueError("task_id cannot be empty or whitespace-only")
        if not self.target_identifier or not self.target_identifier.strip():
            raise ValueError("target_identifier cannot be empty or whitespace-only")
        if not self.status_descriptor or not self.status_descriptor.strip():
            raise ValueError("status_descriptor cannot be empty or whitespace-only")


@dataclass
class AgentTelemetryAlert:
    alert_id: str
    origin_agent: str
    status: ExecutionStatus
    summary: str
    technical_details: str
    actionable_remediation: str
    standard_reference: str = "Supersingular Isogeny Cryptography"
    timestamp: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "alert_id": self.alert_id,
            "origin_agent": self.origin_agent,
            "status": self.status.value,
            "summary": self.summary,
            "technical_details": self.technical_details,
            "actionable_remediation": self.actionable_remediation,
            "standard_reference": self.standard_reference,
            "timestamp": self.timestamp,
        }
