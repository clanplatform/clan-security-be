# Clan Security Backend

Enterprise-grade security microservices platform built with Python FastAPI.

## Architecture

29 microservices across 7 security domains:

| Domain | Services | Ports |
|--------|----------|-------|
| compliance-and-governance | audit-trail, gdpr, pci, policy-mgmt, sox | 8001–8005 |
| data-security | backup-enc, data-class, dlp, data-masking | 8006–8009 |
| encryption-and-keys | cert-mgmt, encryption, hsm, key-mgmt | 8010–8013 |
| identity-and-access | access-ctrl, identity-verif, priv-esc, session-sec | 8014–8017 |
| monitoring-and-audit | audit, forensics, log-analysis, monitoring | 8018–8021 |
| network-security | ddos, firewall, ids, net-monitor | 8022–8025 |
| threat-management | incident, pentest, threat-detect, threat-intel, vuln-scan | 8026–8030 |

## Quick Start

```bash
cp .env.example .env
make build
make up
```

## Development

```bash
# Run individual service
cd services/security-audit-trail-service
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001

# Run all tests
make test

# Lint all services
make lint
```

## Stack

- **Framework**: FastAPI + Uvicorn
- **Database**: PostgreSQL 16 (asyncpg)
- **Cache**: Redis 7
- **Auth**: JWT (python-jose)
- **Validation**: Pydantic v2
- **ORM**: SQLAlchemy 2.0 (async)
- **Container**: Docker + Kubernetes (Helm)
- **CI/CD**: GitHub Actions
