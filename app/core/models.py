from dataclasses import asdict, dataclass, field


@dataclass
class ContainerInfo:
    id: str
    name: str
    image: str
    status: str
    image_created_days_ago: int | None = None
    health: str = "unknown"
    restart_count: int = 0
    compose_project: str | None = None
    owner: str | None = None
    service: str | None = None
    runbook: str | None = None
    ports: list[str] = field(default_factory=list)
    networks: list[str] = field(default_factory=list)
    privileged: bool = False
    mounts_docker_socket: bool = False
    labels: dict[str, str] = field(default_factory=dict)
    risk_score: int = 0
    risk_level: str = "low"
    risk_reasons: list[str] = field(default_factory=list)

    def model_dump(self) -> dict[str, object]:
        return asdict(self)


@dataclass
class FleetSummary:
    total_containers: int
    running: int
    unhealthy: int
    high_risk: int
    medium_risk: int
    low_risk: int
    source: str
    top_risks: list[ContainerInfo]

    def model_dump(self) -> dict[str, object]:
        return asdict(self)
