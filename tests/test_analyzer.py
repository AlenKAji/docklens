import unittest

from app.core.analyzer import build_fleet_summary, score_container
from app.core.docker_provider import _parse_docker_timestamp
from app.core.models import ContainerInfo


class AnalyzerTest(unittest.TestCase):
    def test_score_container_marks_restart_loop_as_high_risk(self) -> None:
        container = ContainerInfo(
            id="abc123",
            name="worker",
            image="example/worker:old",
            image_created_days_ago=130,
            status="running",
            health="unhealthy",
            restart_count=12,
        )

        scored = score_container(container, image_stale_days=90, require_owner_label=True)

        self.assertEqual(scored.risk_level, "high")
        self.assertGreaterEqual(scored.risk_score, 70)
        self.assertIn("health check is unhealthy", scored.risk_reasons)
        self.assertIn("missing owner label", scored.risk_reasons)

    def test_score_container_keeps_owned_healthy_service_low_risk(self) -> None:
        container = ContainerInfo(
            id="def456",
            name="api",
            image="example/api:latest",
            image_created_days_ago=3,
            status="running",
            health="healthy",
            restart_count=0,
            compose_project="shop",
            owner="platform",
        )

        scored = score_container(container)

        self.assertEqual(scored.risk_level, "low")
        self.assertEqual(scored.risk_score, 0)

    def test_build_fleet_summary_orders_top_risks(self) -> None:
        low = score_container(
            ContainerInfo(
                id="1",
                name="api",
                image="example/api:latest",
                status="running",
                health="healthy",
                compose_project="shop",
                owner="platform",
            )
        )
        high = score_container(
            ContainerInfo(
                id="2",
                name="debug",
                image="ubuntu:22.04",
                status="running",
                health="unknown",
                privileged=True,
                mounts_docker_socket=True,
            )
        )

        summary = build_fleet_summary([low, high])

        self.assertEqual(summary.total_containers, 2)
        self.assertEqual(summary.top_risks[0].name, "debug")
        self.assertEqual(summary.high_risk, 0)
        self.assertEqual(summary.medium_risk, 1)

    def test_parse_docker_timestamp_accepts_nanoseconds(self) -> None:
        parsed = _parse_docker_timestamp("2026-06-10T09:12:11.123456789Z")

        self.assertEqual(parsed.microsecond, 123456)
        self.assertIsNotNone(parsed.tzinfo)


if __name__ == "__main__":
    unittest.main()
