param(
  [string]$Image = "ghcr.io/your-org/docklens:latest"
)

$ErrorActionPreference = "Stop"
$env:IMAGE = $Image

docker compose -f deploy/docker-compose.prod.yml pull
docker compose -f deploy/docker-compose.prod.yml up -d
docker compose -f deploy/docker-compose.prod.yml ps
