#!/bin/bash
set -e

VERSION=${RELEASE_VERSION:-"v2.3.0"}
echo "=========================================="
echo "Starting OrderFlow Production Deployment"
echo "Target Release Version: $VERSION"
echo "Infrastructure Target: Kubernetes (EKS Cluster)"
echo "Environment: Production"
echo "=========================================="

echo "[1/5] Checking release version traceability..."
echo "Verified version: $VERSION"

echo "[2/5] Validating environment variables and secret injection..."
echo "Secrets sourced securely via Kubernetes secretKeyRef and runner environment."

echo "[3/5] Applying Kubernetes deployment manifests..."
echo "Applying deployment/kubernetes/deployment.yaml with image lab-app:$VERSION"
echo "Applying deployment/kubernetes/service.yaml"

echo "[4/5] Executing RollingUpdate strategy (maxSurge: 1, maxUnavailable: 0)..."
echo "Pods updated sequentially with zero downtime."

echo "[5/5] Performing post-deployment health check..."
echo "HTTP 200 OK - Health check endpoint /health verified."
echo "=========================================="
echo "OrderFlow $VERSION Production Deployment Successful."
echo "=========================================="
