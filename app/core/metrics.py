from app.core.models import ContainerInfo


def render_prometheus_metrics(containers: list[ContainerInfo]) -> str:
    lines = [
        "# HELP docklens_container_risk_score Operational risk score for a Docker container.",
        "# TYPE docklens_container_risk_score gauge",
    ]

    for container in containers:
        labels = _labels(container)
        lines.append(f"docklens_container_risk_score{{{labels}}} {container.risk_score}")

    lines.extend(
        [
            "# HELP docklens_containers_total Number of containers observed by DockLens.",
            "# TYPE docklens_containers_total gauge",
            f"docklens_containers_total {len(containers)}",
            "# HELP docklens_unhealthy_containers_total Number of unhealthy containers.",
            "# TYPE docklens_unhealthy_containers_total gauge",
            f"docklens_unhealthy_containers_total {sum(1 for item in containers if item.health == 'unhealthy')}",
            "# HELP docklens_high_risk_containers_total Number of high-risk containers.",
            "# TYPE docklens_high_risk_containers_total gauge",
            f"docklens_high_risk_containers_total {sum(1 for item in containers if item.risk_level == 'high')}",
        ]
    )
    return "\n".join(lines) + "\n"


def _labels(container: ContainerInfo) -> str:
    values = {
        "container": container.name,
        "image": container.image,
        "service": container.service or "unknown",
        "owner": container.owner or "unknown",
        "risk_level": container.risk_level,
    }
    return ",".join(f'{key}="{_escape(value)}"' for key, value in values.items())


def _escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
