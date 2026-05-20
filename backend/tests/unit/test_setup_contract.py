from __future__ import annotations

import json
import py_compile
from pathlib import Path

from app.main import app, create_app


ROOT = Path(__file__).resolve().parents[3]


def test_backend_skeleton_files_exist_and_compile() -> None:
    required_files = [
        ROOT / "backend/app/main.py",
        ROOT / "backend/app/api/__init__.py",
        ROOT / "backend/app/schemas/__init__.py",
        ROOT / "backend/app/services/__init__.py",
        ROOT / "backend/tests/conftest.py",
    ]

    for path in required_files:
        assert path.exists(), f"Missing required backend skeleton file: {path}"

    py_compile.compile(str(ROOT / "backend/app/main.py"), doraise=True)
    assert create_app().title == "Configurable FAQ Knowledge Assistant"
    assert app.title == "Configurable FAQ Knowledge Assistant"


def test_backend_dependency_and_pytest_configuration() -> None:
    requirements = (ROOT / "backend/requirements.txt").read_text()
    dev_requirements = (ROOT / "backend/requirements-dev.txt").read_text()
    pyproject = (ROOT / "backend/pyproject.toml").read_text()

    assert "fastapi" in requirements
    assert "pydantic" in requirements
    assert "pytest" in dev_requirements
    assert "pytest-cov" in dev_requirements
    assert "--cov=app" in pyproject
    assert "--cov-fail-under=70" in pyproject


def test_frontend_skeleton_and_build_scripts() -> None:
    package_json = json.loads((ROOT / "frontend/package.json").read_text())

    assert (ROOT / "frontend/src/App.tsx").exists()
    assert (ROOT / "frontend/src/main.tsx").exists()
    assert (ROOT / "frontend/src/styles/index.css").exists()
    assert (ROOT / "frontend/tailwind.config.js").exists()
    assert package_json["scripts"]["build"]
    assert package_json["scripts"]["test"]
    assert "tailwindcss" in package_json["devDependencies"]
    assert "react" in package_json["dependencies"]


def test_environment_examples_do_not_commit_real_secrets() -> None:
    backend_env = (ROOT / "backend/.env.example").read_text()
    frontend_env = (ROOT / "frontend/.env.example").read_text()
    combined = f"{backend_env}\n{frontend_env}".lower()

    assert "example" in combined
    assert "placeholder" in combined
    assert "sk-" not in combined
    assert "real" not in combined
    assert "secret=" not in combined


def test_development_docs_and_gitignore_cover_setup_rules() -> None:
    development = (ROOT / "docs/development.md").read_text()
    gitignore = (ROOT / ".gitignore").read_text()

    assert "pytest" in development
    assert "pytest --cov=app --cov-report=term-missing" in development
    assert "npm run build" in development
    assert "Do not call real LLM APIs in automated tests" in development
    assert ".venv/" in gitignore
    assert "__pycache__/" in gitignore
    assert "*.sqlite3" in gitignore
    assert "node_modules/" in gitignore
