# Diffie Hellman SIDH SIKE Auditor

> **Domain:** Post-Quantum Cryptography & Isogeny-Based Cryptanalysis
> **Standard:** Supersingular Isogeny Cryptography

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3776AB.svg?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688.svg?logo=fastapi&logoColor=white)
![Audit Trail](https://img.shields.io/badge/Audit-HMAC--SHA256_Tamper--Evident-brightgreen.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker&logoColor=white)

</div>

---

## What It Does

**Diffie Hellman SIDH SIKE Auditor** is an analytical platform implementing isogeny cryptanalysis, Castryck-Decru torsion attack auditing, and SQISign validation. It provides a multi-agent evaluation framework for assessing cryptographic parameters against defined security thresholds.

---

## Key Capabilities

- **Multi-Agent Evaluation**: Specialized workers assess parameters against primary, secondary, and conformance boundaries
- **PHI Outbound Guard**: Active pattern detection blocking sensitive identifiers (SSNs, MRNs, phone numbers)
- **HMAC-SHA256 Audit Trail**: Cryptographically chained, tamper-evident logging with full signature verification
- **FastAPI REST API**: OpenAPI-compatible endpoints for programmatic access
- **Batch Processing**: CSV-based bulk evaluation with error handling

---

## Installation

```bash
# Clone the repository
git clone https://github.com/abusuraihsakhri/diffie-hellman-sidh-sike-auditor.git
cd diffie-hellman-sidh-sike-auditor

# Install dependencies
pip install fastapi uvicorn pydantic pytest
```

---

## CLI Usage

### 1. Single Task Evaluation
```bash
python cli.py audit --task-id TASK-001 --target KEY-01 --primary 28.5 --secondary 14.2 --critical --status DISCORDANT
```

### 2. Batch CSV Processing
```bash
python cli.py batch -i sample.csv -o results.csv
```

### 3. Supervisory Chat
```bash
python cli.py chat "What is the system status?"
```

### 4. Verify Audit Trail Integrity
```bash
python cli.py verify-audit
```

### 5. Launch REST API Server
```bash
python cli.py serve --host 127.0.0.1 --port 8000
```

---

## REST API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Service health check |
| GET | `/metrics` | Operational metrics |
| POST | `/api/audit` | Submit task for evaluation |
| POST | `/api/chat` | Query supervisory intelligence |
| GET | `/api/audit/logs` | Retrieve audit trail with integrity status |

---

## Input Data Schema

| Field | Type | Description | Requirement |
|:------|:-----|:------------|:------------|
| `task_id` | str | Unique task identifier | Required |
| `target_identifier` | str | Target entity or key | Required |
| `primary_metric` | float | Primary measurement value | Required |
| `secondary_metric` | float | Secondary measurement value | Optional (default: 0.0) |
| `is_critical_flag` | bool | Emergency escalation flag | Optional (default: false) |
| `status_descriptor` | str | Status code or descriptor | Optional (default: "NOMINAL") |

**Validation Rules:**
- Metric values must be finite (no NaN or Inf)
- String fields must be non-empty after stripping whitespace

---

## Security Features

### Audit Trail Integrity
The HMAC-SHA256 audit trail provides cryptographic verification:
- Each entry includes a chained hash linking to the previous entry
- HMAC signatures are verified using constant-time comparison
- Tampering detection validates both chain linkage and signature validity

### Configuration
Set the `AUDIT_SECRET_KEY` environment variable for persistent audit trail signing:
```bash
export AUDIT_SECRET_KEY="your-secure-random-key"
```

---

## Testing

```bash
# Run full test suite
pytest -v

# Run with coverage
pytest -v --cov=agents --cov=isogeny_auditor
```

---

## Container Deployment

```bash
docker build -t diffie-hellman-sidh-sike-auditor .
docker run -p 8000:8000 -e AUDIT_SECRET_KEY="your-key" diffie-hellman-sidh-sike-auditor
```

---

## Project Structure

```
diffie-hellman-sidh-sike-auditor/
├── agents/                    # Core agent framework
│   ├── base.py               # Security, PHI guard, audit trail
│   ├── models.py             # Pydantic data models with validation
│   ├── supervisor.py         # Multi-agent orchestration
│   ├── workers.py            # Specialized evaluation workers
│   ├── api.py                # FastAPI REST endpoints
│   └── ...
├── isogeny_auditor/          # Isogeny cryptanalysis module
│   ├── models.py             # Frontier payload definitions
│   ├── engine.py             # Core evaluation engine
│   ├── agents.py             # Specialized sub-agents
│   ├── cli.py                # CLI interface
│   └── server.py             # FastAPI server factory
├── tests/                    # Test suite
├── cli.py                    # Main CLI entry point
├── pyproject.toml            # Project configuration
└── Dockerfile                # Container definition
```
