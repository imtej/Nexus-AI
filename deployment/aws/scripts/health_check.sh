#!/usr/bin/env bash
# ========================================================
# Nexus AI — Deployment Health Check Script
# Validates API endpoint accessibility and returns status
# ========================================================

set -euo pipefail

TARGET_URL="${1:-http://localhost:8000}"
HEALTH_ENDPOINT="${TARGET_URL}/health"
EVOLUTION_ENDPOINT="${TARGET_URL}/api/v1/evolution"

echo "🔍 Running Health Checks on: ${TARGET_URL}"

# Check Core Health Endpoint
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "${HEALTH_ENDPOINT}" || echo "000")

if [ "${HTTP_STATUS}" -eq 200 ]; then
    echo "✅ Core Health Check Passed: HTTP ${HTTP_STATUS}"
else
    echo "❌ Core Health Check Failed: HTTP ${HTTP_STATUS}"
    exit 1
fi

# Check Evolution API Endpoint
EVO_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "${EVOLUTION_ENDPOINT}" || echo "000")

if [ "${EVO_STATUS}" -eq 200 ]; then
    echo "✅ Evolution Engine Endpoint Check Passed: HTTP ${EVO_STATUS}"
else
    echo "⚠️ Evolution Engine Endpoint Returned: HTTP ${EVO_STATUS}"
fi

echo "🚀 All Health Checks Completed Successfully."
