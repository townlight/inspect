from pathlib import Path
import re
import tomllib

from fastapi.testclient import TestClient

import townlight_inspections
from townlight_inspections.main import app


client = TestClient(app)
ROOT = Path(__file__).resolve().parents[1]


def test_package_version_is_100() -> None:
    assert townlight_inspections.__version__ == "0.3.0+dev.2"


def test_root_endpoint_states_runtime_boundary() -> None:
    response = client.get("/")
    assert response.status_code == 200
    payload = response.json()

    assert payload["name"] == "TownlightInspections"
    assert payload["version"] == "0.3.0+dev.2"
    assert payload["status"] == "inspection support product with staff review queues"
    assert "staff review queues" in payload["message"]
    assert "Townlight Code context packets" in payload["message"]
    assert "official findings" in payload["message"]
    assert "not implemented" in payload["message"]
    assert "TOWNLIGHT_INSPECTIONS_STAFF_API_KEY" in payload["next_step"]


def test_health_endpoint_reports_versions() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    payload = response.json()

    assert payload["status"] == "ok"
    assert payload["service"] == "townlight_inspections"
    assert payload["version"] == "0.3.0+dev.2"
    # Reports the Core that is actually imported; the exact published-wheel pin
    # is asserted separately, unchanged, below.
    import townlight_core

    assert payload["townlight_core_version"] == townlight_core.__version__
    assert re.fullmatch(r"\d+\.\d+\.\d+(\.(dev|post|a|b|rc)\d+)?([.+].*)?",
                        payload["townlight_core_version"])


def test_release_script_prefers_python3_before_python_for_wsl_native_proof() -> None:
    lines = (ROOT / "scripts" / "verify-release.sh").read_text(encoding="utf-8").splitlines()
    python3_line = next(index for index, line in enumerate(lines) if "command -v python3" in line)
    python_line = next(index for index, line in enumerate(lines) if "command -v python >/dev/null" in line)

    assert python3_line < python_line


def test_pyproject_uses_published_townlight_core_release_wheel() -> None:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))

    dependencies = pyproject["project"]["dependencies"]
    assert "townlight-core==1.3.0.dev2" in dependencies
    assert not any("civiccore" in dependency or "@main" in dependency for dependency in dependencies)
    assert pyproject["tool"]["hatch"]["metadata"]["allow-direct-references"] is True


def test_docs_gate_rejects_stale_markers() -> None:
    text = (ROOT / "scripts" / "verify-docs.sh").read_text(encoding="utf-8")

    assert '"Shipping v0.1.1"' in text
    assert '"production-ready"' in text
    assert '"official findings are available"' in text


def test_docs_index_marks_v1_label_without_mojibake() -> None:
    text = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")

    assert "Townlight Beta 1" in text
    assert "0.3.0+dev.2" in text
    assert "review" in text
    assert "AGPL-3.0" in text
    assert "ÃƒÆ’" not in text


def test_recovery_status_records_v1_scope() -> None:
    text = (ROOT / "docs" / "release-recovery-status.md").read_text(encoding="utf-8")

    assert "v0.2.2" in text
    assert "staff review queues" in text
