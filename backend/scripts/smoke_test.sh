#!/usr/bin/env bash
set -euo pipefail

BASE_URL=${1:-http://localhost:8000}

curl -s "$BASE_URL/health" | grep -q 'ok'
echo "Health endpoint OK"
