from fastapi import APIRouter, Response, status

from app.core.analyzer import build_fleet_summary
from app.core.config import Settings
from app.core.docker_provider import DockerInventoryProvider
from app.core.metrics import render_prometheus_metrics

router = APIRouter()
settings = Settings.from_env()
provider = DockerInventoryProvider(settings)


@router.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/readyz", status_code=status.HTTP_200_OK)
def readyz(response: Response) -> dict[str, str]:
    readiness = provider.readiness()
    if readiness["status"] != "ready":
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return readiness


@router.get("/api/containers")
def containers() -> dict[str, object]:
    return {
        "source": provider.source_name,
        "containers": [item.model_dump() for item in provider.list_containers()],
    }


@router.get("/api/summary")
def summary() -> dict[str, object]:
    containers = provider.list_containers()
    return build_fleet_summary(containers, source=provider.source_name).model_dump()


@router.get("/metrics")
def metrics() -> Response:
    containers = provider.list_containers()
    content = render_prometheus_metrics(containers)
    return Response(content=content, media_type="text/plain; version=0.0.4")
