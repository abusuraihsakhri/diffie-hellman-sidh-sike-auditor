"""Regression coverage for truthful results and audit-log safety."""
import pytest
from fastapi import HTTPException

from agents.api import api_audit
from agents.base import AuditTrail
from agents.llm_factory import MockLLM
from agents.models import SystemTaskPayload
from isogeny_auditor.agents import IsogenySecurityCoordinator
from isogeny_auditor.models import FrontierPayload


def test_audit_trail_read_returns_defensive_copy():
    trail = AuditTrail(secret_key="unit-test-secret")
    trail.log("tester", "auditor", "CHECK", {"value": 1})
    exposed = trail.get_trail()
    exposed[0]["current_hash"] = "modified"
    exposed.append({})
    assert len(trail.get_trail()) == 1
    assert trail.verify_integrity()


def test_malformed_audit_entries_are_invalid_not_exceptions():
    trail = AuditTrail(secret_key="unit-test-secret")
    trail.log("tester", "auditor", "CHECK", {"value": 1})
    del trail.logs[0]["payload_hash"]
    assert trail.verify_integrity() is False


def test_primary_api_does_not_claim_cryptographic_assurance():
    payload = SystemTaskPayload(
        task_id="TASK-1", target_identifier="KEY-1", primary_metric=10
    )
    result = api_audit(payload)
    assert result["cryptographic_assurance"] == "NOT_ASSESSED"
    assert "insecure" in result["security_notice"].lower()


def test_identifier_guard_returns_client_error_not_server_error():
    payload = SystemTaskPayload(
        task_id="MRN-123456", target_identifier="KEY-1", primary_metric=10
    )
    with pytest.raises(HTTPException) as exc:
        api_audit(payload)
    assert exc.value.status_code == 422
    assert "MRN" not in str(exc.value.detail)


def test_isogeny_api_data_contains_security_caveat():
    payload = FrontierPayload("TASK-2", "KEY-2", 10.0, 4.0, "NOMINAL")
    result = IsogenySecurityCoordinator().process(payload)
    assert result["cryptographic_assurance"] == "NOT_ASSESSED"
    assert result["total_alerts"] == 0


def test_mock_does_not_falsely_report_validation():
    result = MockLLM().invoke("Check status")
    assert "No cryptographic analysis performed" in result
