from datetime import UTC, datetime
from typing import Any

from app.core.analyzer import score_container
from app.core.config import Settings
from app.core.demo_data import demo_containers
from app.core.models import ContainerInfo


class DockerInventoryProvider:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.source_name = "demo" if settings.demo_mode else "docker"
        self._last_error: str | None = None

    def readiness(self) -> dict[str, str]:
        if self.settings.demo_mode:
            return {"status": "ready", "source": "demo"}

        try:
            client = self._client()
            client.ping()
            return {"status": "ready", "source": "docker"}
        except Exception as exc:  # pragma: no cover - depends on local Docker host
            self._last_error = str(exc)
            return {"status": "not_ready", "source": "docker", "error": str(exc)}

    def list_containers(self) -> list[ContainerInfo]:
        if self.settings.demo_mode:
            self.source_name = "demo"
            return demo_containers(self.settings)

        try:
            client = self._client()
            containers = client.containers.list(all=True)
            self.source_name = "docker"
            return [self._from_docker_container(container) for container in containers]
        except Exception as exc:  # pragma: no cover - depends on local Docker host
            self._last_error = str(exc)
            self.source_name = "demo"
            return demo_containers(self.settings)

    def _client(self) -> Any:
        import docker

        return docker.DockerClient(base_url=self.settings.docker_host)

    def _from_docker_container(self, container: Any) -> ContainerInfo:
        container.reload()
        attrs = container.attrs
        state = attrs.get("State", {})
        config = attrs.get("Config", {})
        host_config = attrs.get("HostConfig", {})
        labels = config.get("Labels") or {}

        info = ContainerInfo(
            id=container.short_id,
            name=container.name,
            image=_image_name(container),
            image_created_days_ago=_image_age_days(container),
            status=state.get("Status", container.status),
            health=(state.get("Health") or {}).get("Status", "unknown"),
            restart_count=int(state.get("RestartCount", 0) or 0),
            compose_project=labels.get("com.docker.compose.project"),
            owner=labels.get("com.docklens.owner") or labels.get("org.opencontainers.image.authors"),
            service=labels.get("com.docklens.service") or labels.get("com.docker.compose.service"),
            runbook=labels.get("com.docklens.runbook"),
            ports=_format_ports(attrs),
            networks=list((attrs.get("NetworkSettings", {}).get("Networks") or {}).keys()),
            privileged=bool(host_config.get("Privileged", False)),
            mounts_docker_socket=_mounts_docker_socket(attrs),
            labels={str(key): str(value) for key, value in labels.items()},
        )

        return score_container(
            info,
            image_stale_days=self.settings.image_stale_days,
            require_owner_label=self.settings.require_owner_label,
        )


def _image_name(container: Any) -> str:
    tags = getattr(container.image, "tags", [])
    return tags[0] if tags else getattr(container.image, "short_id", "unknown")


def _image_age_days(container: Any) -> int | None:
    created = getattr(container.image, "attrs", {}).get("Created")
    if not created:
        return None
    created_at = _parse_docker_timestamp(created)
    return max((datetime.now(UTC) - created_at).days, 0)


def _parse_docker_timestamp(value: str) -> datetime:
    normalized = value.replace("Z", "+00:00")
    if "." in normalized:
        prefix, suffix = normalized.split(".", 1)
        for separator in ["+", "-"]:
            if separator in suffix:
                fraction, timezone = suffix.split(separator, 1)
                normalized = f"{prefix}.{fraction[:6]}{separator}{timezone}"
                break
    return datetime.fromisoformat(normalized)


def _format_ports(attrs: dict[str, Any]) -> list[str]:
    ports = attrs.get("NetworkSettings", {}).get("Ports") or {}
    formatted: list[str] = []
    for container_port, bindings in ports.items():
        if not bindings:
            formatted.append(container_port)
            continue
        for binding in bindings:
            host_ip = binding.get("HostIp", "0.0.0.0")
            host_port = binding.get("HostPort", "")
            formatted.append(f"{container_port} -> {host_ip}:{host_port}")
    return formatted


def _mounts_docker_socket(attrs: dict[str, Any]) -> bool:
    mounts = attrs.get("Mounts") or []
    for mount in mounts:
        source = mount.get("Source", "")
        destination = mount.get("Destination", "")
        if "docker.sock" in source or "docker.sock" in destination:
            return True
    return False
