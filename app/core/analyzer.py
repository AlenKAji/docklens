from app.core.models import ContainerInfo, FleetSummary


def score_container(container: ContainerInfo, image_stale_days: int = 90, require_owner_label: bool = True) -> ContainerInfo:
    score = 0
    reasons: list[str] = []

    status = container.status.lower()
    health = container.health.lower()

    if status in {"exited", "dead", "restarting"}:
        score += 30
        reasons.append(f"container status is {container.status}")

    if health == "unhealthy":
        score += 30
        reasons.append("health check is unhealthy")
    elif health == "starting":
        score += 10
        reasons.append("health check is still starting")

    if container.restart_count >= 10:
        score += 25
        reasons.append(f"restart count is high ({container.restart_count})")
    elif container.restart_count >= 3:
        score += 15
        reasons.append(f"restart count is elevated ({container.restart_count})")

    if container.image_created_days_ago is not None and container.image_created_days_ago >= image_stale_days:
        score += 15
        reasons.append(f"image is {container.image_created_days_ago} days old")

    if require_owner_label and not container.owner:
        score += 10
        reasons.append("missing owner label")

    if not container.compose_project:
        score += 10
        reasons.append("not attached to a Compose project")

    if container.privileged:
        score += 20
        reasons.append("runs in privileged mode")

    if container.mounts_docker_socket:
        score += 20
        reasons.append("mounts the Docker socket")

    container.risk_score = min(score, 100)
    container.risk_reasons = reasons or ["no obvious operational risk detected"]
    container.risk_level = _risk_level(container.risk_score)
    return container


def build_fleet_summary(containers: list[ContainerInfo], source: str = "docker") -> FleetSummary:
    ordered = sorted(containers, key=lambda item: item.risk_score, reverse=True)
    return FleetSummary(
        total_containers=len(containers),
        running=sum(1 for item in containers if item.status.lower() == "running"),
        unhealthy=sum(1 for item in containers if item.health.lower() == "unhealthy"),
        high_risk=sum(1 for item in containers if item.risk_level == "high"),
        medium_risk=sum(1 for item in containers if item.risk_level == "medium"),
        low_risk=sum(1 for item in containers if item.risk_level == "low"),
        source=source,
        top_risks=ordered[:5],
    )


def _risk_level(score: int) -> str:
    if score >= 70:
        return "high"
    if score >= 35:
        return "medium"
    return "low"
