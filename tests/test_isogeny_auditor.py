import sys
import os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from isogeny_auditor.models import FrontierPayload, ExecutionStatus
from isogeny_auditor.engine import FrontierDomainEngine
from isogeny_auditor.agents import IsogenyGraphPathAgent, TorsionPointAttackScannerAgent, SQISignCompatibilityAgent, IsogenySecurityCoordinator
from isogeny_auditor.cli import main


def test_sub_agents():
    a1 = IsogenyGraphPathAgent()
    p1 = FrontierPayload("T1", "KEY-01", primary_metric=35.0, secondary_metric=4.0, status_descriptor="NOMINAL")
    alerts1 = a1.audit(p1)
    assert len(alerts1) == 1
    assert alerts1[0].status == ExecutionStatus.ELEVATED_RISK

    a2 = TorsionPointAttackScannerAgent()
    p2 = FrontierPayload("T2", "KEY-02", primary_metric=10.0, secondary_metric=15.0, status_descriptor="NOMINAL", is_critical_flag=True)
    alerts2 = a2.audit(p2)
    assert len(alerts2) == 1
    assert alerts2[0].status == ExecutionStatus.CRITICAL_INTERVENTION

    a3 = SQISignCompatibilityAgent()
    p3 = FrontierPayload("T3", "KEY-03", primary_metric=10.0, secondary_metric=4.0, status_descriptor="DISCORDANT_ANOMALY")
    alerts3 = a3.audit(p3)
    assert len(alerts3) == 1


def test_coordinator():
    coord = IsogenySecurityCoordinator()
    p_nominal = FrontierPayload("T4", "KEY-04", primary_metric=12.0, secondary_metric=4.0, status_descriptor="NOMINAL")
    dossier = coord.process(p_nominal)
    assert dossier["overall_status"] == ExecutionStatus.NOMINAL.value
    assert dossier["total_alerts"] == 0

    ans = coord.query_supervisory_chat("What standard is applied?")
    assert "Supersingular Isogeny Cryptography" in ans or "specifications" in ans


def test_cli():
    assert main(["audit", "--task-id", "CLI-01"]) == 0
    assert main(["chat", "What", "is", "the", "system", "status?"]) == 0


def test_frontier_payload_validation():
    """FrontierPayload should reject invalid values."""
    import math

    # Reject NaN
    with pytest.raises(ValueError, match="finite"):
        FrontierPayload("T1", "KEY-01", primary_metric=float("nan"), secondary_metric=4.0, status_descriptor="NOMINAL")

    # Reject Inf
    with pytest.raises(ValueError, match="finite"):
        FrontierPayload("T1", "KEY-01", primary_metric=10.0, secondary_metric=float("inf"), status_descriptor="NOMINAL")

    # Reject empty task_id
    with pytest.raises(ValueError, match="empty"):
        FrontierPayload("", "KEY-01", primary_metric=10.0, secondary_metric=4.0, status_descriptor="NOMINAL")

    # Reject whitespace-only target_identifier
    with pytest.raises(ValueError, match="empty"):
        FrontierPayload("T1", "   ", primary_metric=10.0, secondary_metric=4.0, status_descriptor="NOMINAL")


def test_batch_processing_with_missing_file():
    """Batch command should handle missing input file gracefully."""
    result = main(["batch", "-i", "nonexistent_file_12345.csv"])
    assert result == 1


def test_batch_processing_with_sample_csv():
    """Batch command should process sample CSV successfully."""
    result = main(["batch", "-i", "sample.csv", "-o", "test_output_iso.csv"])
    assert result == 0

    # Verify output file was created
    assert os.path.isfile("test_output_iso.csv")

    # Clean up
    os.remove("test_output_iso.csv")
