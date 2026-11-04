# OrderFlow — Release Readiness & Production Release Pack

This repository contains the production-ready release pipeline, infrastructure configurations, and operational documentation for **OrderFlow v2.3.0**.

---

## Current Release
- **Version:** `v2.3.0`
- **Status:** Production-Ready & Approved
- **Branch:** `investigation/release-readiness`
- **Target Environment:** Production

---

## Application
OrderFlow is a containerized Node.js Express service designed for scalable, zero-downtime production deployment.

### Endpoints
- `GET /` — Service status & information
- `GET /health` — Health check returning JSON `{ status: 'ok', version: '2.3.0' }`

---

## Release Readiness Summary

### 1. Deployment Pipeline Repairs (`.github/workflows/release.yml`)
- Corrected pipeline stage execution order: `validate-release` runs strictly before `deploy-production`.
- Configured dependency guard: `deploy-production` requires `needs: validate-release`.
- Bound production environment protection rules (`environment: production`).
- Bound release version `v2.3.0` across all pipeline stages.
- Eliminated artificial failure triggers (`exit 1`).

### 2. Secure Release Configuration
- **Secret Management:** Eradicated all hardcoded credentials from manifests and config files. Migrated to Kubernetes `secretKeyRef` and environment injection.
- **Traceability:** Pinned all artifacts, manifests, packages, and docker files to immutable version `v2.3.0`.
- **Infrastructure Decision:** Standardized on Kubernetes container orchestration (`deployment/kubernetes/`) with RollingUpdate strategy (3 replicas) over unmanaged standalone EC2 instances.

### 3. Operational Documentation & Rollback
- Comprehensive documentation available in [`release/RELEASE_DOCUMENTATION.md`](release/RELEASE_DOCUMENTATION.md).
- Automated rollback procedures documented in [`release/rollback.yml`](release/rollback.yml) and executed via [`scripts/rollback.sh`](scripts/rollback.sh).
- Formal approvals and production sign-offs recorded in [`release/approvals.yml`](release/approvals.yml).

---

## Repository Structure
```
├── .github/
│   └── workflows/
│       └── release.yml            # Repaired production-safe deployment pipeline
├── app/
│   ├── package.json               # OrderFlow v2.3.0 package definition
│   └── server.js                  # Express API with /health endpoint
├── deployment/
│   ├── kubernetes/
│   │   ├── deployment.yaml        # RollingUpdate K8s deployment with secretKeyRef
│   │   └── service.yaml           # LoadBalancer Service
│   └── terraform/
│       ├── main.tf                # Hardened Terraform infrastructure
│       └── variables.tf           # Sensitive variable definitions
├── release/
│   ├── RELEASE_DOCUMENTATION.md   # Final Release Readiness Pack
│   ├── approvals.yml              # Production approval checklist & sign-offs
│   ├── deployment-config.yml      # Secured release deployment config
│   ├── release-summary.yml        # Release state & validation summary
│   ├── release.json               # Traceable release metadata (v2.3.0)
│   └── rollback.yml               # Automated rollback strategy
├── scripts/
│   ├── deploy.sh                  # Production deployment script
│   └── rollback.sh                # Emergency rollback execution script
├── Dockerfile                     # Production Node.js 18 container specification
├── docker-compose.yml             # Local orchestration specification
└── README.md
```
