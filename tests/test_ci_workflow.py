from pathlib import Path


WORKFLOW_PATH = Path(__file__).resolve().parents[1] / ".github" / "workflows" / "ci.yml"


def read_workflow() -> str:
    return WORKFLOW_PATH.read_text(encoding="utf-8")


def test_ci_workflow_defines_required_triggers_and_single_pytest_job():
    workflow = read_workflow()

    assert "name: CI" in workflow
    assert "on:\n  push:\n  pull_request:" in workflow
    assert "jobs:\n  test:" in workflow
    assert "runs-on: ubuntu-latest" in workflow
    assert "python-version: \"3.13\"" in workflow


def test_ci_workflow_installs_dependencies_before_running_pytest():
    workflow = read_workflow()

    install_position = workflow.index("- name: Install dependencies")
    pytest_position = workflow.index("- name: Run pytest")

    assert install_position < pytest_position
    assert "python -m pip install --upgrade pip" in workflow
    assert "pip install -r requirements.txt" in workflow
    assert "run: python -m pytest" in workflow
    assert "cache: pip" in workflow
    assert "cache-dependency-path: requirements.txt" in workflow


def test_ci_workflow_runs_pytest_with_safe_hydro_environment():
    workflow = read_workflow()

    assert "HYDRO_DATABASE_PATH: tests/.tmp_hydro_test.db" in workflow
    assert "HYDRO_DATABASE_PATH: hydro.db" not in workflow
    assert "HYDRO_SESSION_SECRET: test-session-secret-with-enough-entropy" in workflow
    assert "HYDRO_BOOTSTRAP_ADMIN_PASSWORD: test-admin-password" in workflow
    assert "HYDRO_SESSION_COOKIE_SECURE: \"0\"" in workflow


def test_ci_workflow_remains_limited_to_basic_pytest_scope():
    workflow = read_workflow().lower()

    excluded_quality_gates = ["ruff", "mypy", "coverage", "codecov", "deploy", "trivy"]

    for gate in excluded_quality_gates:
        assert gate not in workflow
