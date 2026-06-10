# Demo Guide

Use this guide when presenting DockLens in a portfolio, interview, or recorded demo.

## Local Demo

Start DockLens on a free port:

```bash
PORT=8081 docker compose up --build
```

PowerShell:

```powershell
$env:PORT = "8081"
docker compose up --build
```

Open:

- Dashboard: http://localhost:8081
- API: http://localhost:8081/api/summary
- Metrics: http://localhost:8081/metrics

## Observability Demo

```bash
PORT=8081 docker compose --profile observability up --build
```

Open:

- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000

Grafana login:

```text
admin / admin
```

The local observability profile also enables anonymous read-only access so screenshots can be captured without storing a login session.

Open the `Docker Operations / DockLens Docker Operations` dashboard.

## Screenshot Checklist

Save screenshots in `docs/images/`:

- `dashboard.png`: DockLens dashboard with real containers.
- `summary-api.png`: `/api/summary` JSON response.
- `metrics.png`: `/metrics` endpoint.
- `grafana.png`: Grafana dashboard.
- `github-actions.png`: successful CI run.
- `trivy.png`: image scan result or Security tab.

## Talking Track

DockLens solves the operational blind spot that appears when teams run important services on Docker Compose hosts. It reads Docker metadata, computes explainable risk scores, exposes metrics for Prometheus, and ships with hardened Docker runtime settings plus a CI/CD pipeline.
