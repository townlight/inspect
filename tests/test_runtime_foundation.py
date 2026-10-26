from pathlib import Path
import re
import tomllib

from fastapi.testclient import TestClient

import civicinspect
from civicinspect.main import app


client = TestClient(app)
ROOT = Path(__file__).resolve().parents[1]


def test_package_version_is_100() -> None:
    assert civicinspect.__version__ == "0.3.0+dev.1"


def test_root_endpoint_states_runtime_boundary() -> None:
    response = client.get("/")
    assert response.status_code == 200
    payload = response.json()

    assert payload["name"] == "CivicInspect"
    assert payload["version"] == "0.3.0+dev.1"
    assert payload["status"] == "inspection support product with staff review queues"
    assert "staff review queues" in payload["message"]
    assert "Townlight Code context packets" in payload["message"]
    assert "official findings" in payload["message"]
    assert "not implemented" in payload["message"]
    assert "CIVICINSPECT_STAFF_API_KEY" in payload["next_step"]


def test_health_endpoint_reports_versions() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    payload = response.json()

    assert payload["status"] == "ok"
    assert payload["service"] == "civicinspect"
    assert payload["version"] == "0.3.0+dev.1"
    assert re.fullmatch(r"\d+\.\d+\.\d+", payload["civiccore_version"])


def test_release_script_prefers_python3_before_python_for_wsl_native_proof() -> None:
    lines = (ROOT / "scripts" / "verify-release.sh").read_text(encoding="utf-8").splitlines()
    python3_line = next(index for index, line in enumerate(lines) if "command -v python3" in line)
    python_line = next(index for index, line in enumerate(lines) if "command -v python >/dev/null" in line)

    assert python3_line < python_line


def test_pyproject_uses_published_civiccore_release_wheel() -> None:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))

    dependencies = pyproject["project"]["dependencies"]
    assert any(
        dependency
        == "civiccore @ https://github.com/townlight/core/releases/download/v1.2.1/civiccore-1.2.1-py3-none-any.whl#sha256=8dde29408e206048bde63ec14156a8e6329382af4d16b12710d12aa5c27f3f59"
        for dependency in dependencies
    )
    assert pyproject["tool"]["hatch"]["metadata"]["allow-direct-references"] is True


def test_docs_gate_rejects_stale_markers() -> None:
    text = (ROOT / "scripts" / "verify-docs.sh").read_text(encoding="utf-8")

    assert '"Shipping v0.1.1"' in text
    assert '"production-ready"' in text
    assert '"official findings are available"' in text


def test_docs_index_marks_v1_label_without_mojibake() -> None:
    text = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")

    assert "v0.2.2 inspection support + staff review queues" in text
    assert "staff review queues" in text
    assert "official findings" in text
    assert "Ãƒ" not in text


def test_recovery_status_records_v1_scope() -> None:
    text = (ROOT / "docs" / "release-recovery-status.md").read_text(encoding="utf-8")

    assert "v0.2.2" in text
    assert "staff review queues" in text
