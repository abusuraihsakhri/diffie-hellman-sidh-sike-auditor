# Diffie Hellman SIDH/SIKE Auditor

> **Security limitation:** SIDH and SIKE are insecure following the 2022 key-recovery attacks. This repository does **not** implement isogeny computations, the Castryck–Decru attack, key recovery, SQISign validation, or cryptographic security certification. A nominal threshold result must never be interpreted as a secure cryptosystem.
>
> Reference: [SIKE team's security notice hosted by NIST](https://csrc.nist.gov/csrc/media/Projects/post-quantum-cryptography/documents/round-4/submissions/sike-team-note-insecure.pdf).

## Overview

This project contains two **illustrative numerical rule evaluators** with separate Python CLIs, a FastAPI interface, CSV processing, in-memory audit bookkeeping, and an offline browser demonstration. It is suitable for inspecting the project's example classification rules, not for security-critical decision-making.

- **Primary `agents/` implementation:** three workers classify inputs using `primary_metric > 25`, `secondary_metric > 12` (or an explicit critical flag), and keywords in `status_descriptor`.
- **Alternate `isogeny_auditor/` implementation:** separate three-agent evaluator; the secondary threshold is **10**, not 12. It has its own CLI and API factory.
- **Browser demonstration (`web/`):** JavaScript mirrors the primary `agents/` thresholds. No backend, signing key, external service, or Python runtime is necessary.
- **Audit log:** the primary API maintains an HMAC-SHA256 chain **in process memory only**. It is neither a persistent ledger nor an independent security attestation. The browser does not create signatures.

## Use in the browser

Open `web/index.html` or run:

```bash
python -m http.server 8080 --directory web
# Open http://localhost:8080/
```

Enter a task ID, target label, both numeric metrics, descriptor, and optional critical flag. Select **Evaluate thresholds** to see the JSON result. All evaluation stays in the browser tab; no information is uploaded or persisted by the page. Use only non-sensitive, synthetic identifiers.

A GitHub Pages deployment workflow is included. A public URL will be added here only after successful live deployment is verified.

## Python setup

Requires Python 3.9 or later. The CI suite checks Python 3.10, 3.11, and 3.12.

```bash
git clone https://github.com/abusuraihsakhri/diffie-hellman-sidh-sike-auditor.git
cd diffie-hellman-sidh-sike-auditor
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[api,test]'
```

Primary command-line interface:

```bash
python cli.py audit --task-id DEMO-001 --target KEY-01 --primary 29.4 --secondary 14.8 --critical --status DISCORDANT
python cli.py batch --input sample.csv --output results.csv
python cli.py chat "What is the status?"
python cli.py verify-audit
python cli.py serve --host 127.0.0.1 --port 8000
```

The `verify-audit` command inspects only the current process's in-memory log; launching it separately may verify an **empty log**. For the alternate implementation run `python -m isogeny_auditor.cli audit` or the installed `diffie-hellman-sidh-sike-auditor audit` command.

## API and containers

The root CLI serves `agents.api:app` with `GET /health`, `GET /metrics`, `POST /api/audit`, `POST /api/chat`, and `GET /api/audit/logs`. Visit `http://127.0.0.1:8000/docs` for its generated OpenAPI documentation.

The API is **not authenticated** and must not be exposed directly to an untrusted network. The built-in identifier guard is a limited regex heuristic, **not** validated PHI de-identification or regulatory compliance. Avoid real patient data and production secrets.

For a localhost-only Docker Compose run, first set a **new** secret. Do not reuse the formerly committed example key.

```bash
cp .env.example .env
python -c "import secrets; print(secrets.token_urlsafe(32))"
# Paste the generated value after AUDIT_SECRET_KEY= in .env
docker compose --env-file .env up --build
```

The container uses port `127.0.0.1:8000` by default. `.env` is ignored by Git. Docker and the Python server require a runtime; **GitHub Pages hosts only the static browser demonstration**, not these APIs.

## Tests

```bash
python -m pytest -v
python -m compileall -q agents isogeny_auditor cli.py enrichment.py simulator.py
python -m pip check
node --check web/audit.js
node --test web/audit.test.cjs
```

The project uses Python, Pydantic v2, optional FastAPI/Uvicorn, standard HTML/CSS/JavaScript, and GitHub Actions. The browser page targets current desktop and mobile browsers with modern JavaScript support. No service-side analytics are implemented in the page.

## License

[MIT](LICENSE).
