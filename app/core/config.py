import os
from dataclasses import dataclass


def _env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    app_name: str = "DockLens"
    app_env: str = "development"
    demo_mode: bool = False
    docker_host: str = "unix:///var/run/docker.sock"
    image_stale_days: int = 90
    require_owner_label: bool = True
    log_level: str = "INFO"

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            app_name=os.getenv("APP_NAME", cls.app_name),
            app_env=os.getenv("APP_ENV", cls.app_env),
            demo_mode=_env_bool("DEMO_MODE", cls.demo_mode),
            docker_host=os.getenv("DOCKER_HOST", cls.docker_host),
            image_stale_days=int(os.getenv("IMAGE_STALE_DAYS", str(cls.image_stale_days))),
            require_owner_label=_env_bool("REQUIRE_OWNER_LABEL", cls.require_owner_label),
            log_level=os.getenv("LOG_LEVEL", cls.log_level),
        )
