#!/usr/bin/env bash
set -euo pipefail

IMAGE="${1:-${IMAGE:-ghcr.io/your-org/docklens:latest}}"
export IMAGE

if [[ -z "${DOCKER_GID:-}" ]] && command -v getent >/dev/null 2>&1; then
  DOCKER_GID="$(getent group docker | cut -d: -f3 || true)"
  DOCKER_GID="${DOCKER_GID:-0}"
  export DOCKER_GID
fi

docker compose -f deploy/docker-compose.prod.yml pull
docker compose -f deploy/docker-compose.prod.yml up -d
docker compose -f deploy/docker-compose.prod.yml ps
