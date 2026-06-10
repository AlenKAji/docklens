from app.core.analyzer import score_container
from app.core.config import Settings
from app.core.models import ContainerInfo


def demo_containers(settings: Settings) -> list[ContainerInfo]:
    containers = [
        ContainerInfo(
            id="84f7c1",
            name="payments-api",
            image="ghcr.io/example/payments-api:2026.06.1",
            image_created_days_ago=7,
            status="running",
            health="healthy",
            restart_count=0,
            compose_project="commerce",
            owner="platform",
            service="payments",
            runbook="https://wiki.example.com/runbooks/payments",
            ports=["8080/tcp -> 10.0.1.20:8080"],
            networks=["commerce_backend"],
        ),
        ContainerInfo(
            id="f1302b",
            name="legacy-worker",
            image="registry.example.com/jobs/legacy-worker:1.4.2",
            image_created_days_ago=184,
            status="running",
            health="unhealthy",
            restart_count=14,
            compose_project="batch",
            service="legacy-worker",
            ports=[],
            networks=["batch_default"],
        ),
        ContainerInfo(
            id="a92bd0",
            name="admin-debug-shell",
            image="ubuntu:22.04",
            image_created_days_ago=121,
            status="running",
            health="unknown",
            restart_count=0,
            owner="unknown",
            service="debug",
            privileged=True,
            mounts_docker_socket=True,
            networks=["bridge"],
        ),
        ContainerInfo(
            id="19dabc",
            name="postgres",
            image="postgres:16",
            image_created_days_ago=33,
            status="running",
            health="healthy",
            restart_count=1,
            compose_project="commerce",
            owner="data",
            service="postgres",
            ports=["5432/tcp"],
            networks=["commerce_backend"],
        ),
    ]
    return [
        score_container(
            container,
            image_stale_days=settings.image_stale_days,
            require_owner_label=settings.require_owner_label,
        )
        for container in containers
    ]
