#!/usr/bin/env bash
set -euo pipefail

ACTION="${1:-up}"

case "$ACTION" in
  up)
    echo "[local-deploy] Building and starting Kafka + generator + API..."
    docker compose up -d --build
    echo "[local-deploy] Done. API: http://localhost:8000/health"
    ;;
  down)
    echo "[local-deploy] Stopping and removing stack..."
    docker compose down
    ;;
  logs)
    docker compose logs -f generator
    ;;
  *)
    echo "Usage: $0 [up|down|logs]"
    exit 1
    ;;
esac
