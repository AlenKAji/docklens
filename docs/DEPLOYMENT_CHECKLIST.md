# Deployment Checklist

Use this checklist before publishing DockLens as a portfolio project or deploying it on a VM.

## Repository

- [ ] Create GitHub repository.
- [ ] Push the code to `main`.
- [ ] If using Windows and tools are not on PATH, call `C:\Program Files\Git\cmd\git.exe` and `C:\Program Files\GitHub CLI\gh.exe` directly.
- [ ] Authenticate GitHub CLI with `gh auth login --hostname github.com --git-protocol https --web`.
- [ ] Or run `.\deploy\publish-github.ps1 -RepoName docklens` after authentication.
- [ ] Confirm GitHub Actions test job passes.
- [ ] Confirm Docker image job publishes to GHCR.
- [ ] Add screenshots to `docs/images/`.
- [ ] Update README image links after screenshots are committed.

## Host

- [ ] Install Docker and Docker Compose plugin.
- [ ] Confirm `docker info` works for the deployment user.
- [ ] Set `IMAGE=ghcr.io/<owner>/docklens:<tag>`.
- [ ] Set `DOCKER_GID=$(getent group docker | cut -d: -f3)`.
- [ ] Run `docker compose -f deploy/docker-compose.prod.yml up -d`.
- [ ] Confirm `/healthz`, `/readyz`, `/api/summary`, and `/metrics`.

## Security

- [ ] Keep DockLens on a private network or behind a reverse proxy.
- [ ] Enable basic auth, VPN, or SSO in front of the dashboard.
- [ ] Do not expose Docker metadata publicly.
- [ ] Rotate any demo credentials before publishing.

## Observability

- [ ] Run Prometheus and Grafana profile or connect existing Prometheus.
- [ ] Import or use the provisioned DockLens Grafana dashboard.
- [ ] Add alerts for high-risk and unhealthy containers.
