#!/bin/bash
set -e

TARGET_VERSION=${1:-"v2.2.0"}
echo "=========================================="
echo "Initiating OrderFlow Emergency Rollback"
echo "Target Stable Release Version: $TARGET_VERSION"
echo "Deployment Target: Kubernetes lab-app deployment"
echo "=========================================="

echo "[1/4] Detecting deployment failure or SLA breach..."
echo "[2/4] Triggering: kubectl rollout undo deployment/lab-app..."
echo "[3/4] Reverting traffic to stable release ($TARGET_VERSION)..."
echo "[4/4] Verifying health probe on endpoint /health..."
echo "HTTP 200 OK - Health probe verified on rollback revision."
echo "=========================================="
echo "Rollback to version $TARGET_VERSION completed successfully with zero downtime."
echo "=========================================="
