from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory


EXPECTED_DIRECTORIES = {
    Path("src"),
    Path("src/apps"),
    Path("src/config"),
    Path("src/config/settings"),
    Path("src/core"),
    Path("src/core/application"),
    Path("src/core/domain"),
    Path("src/core/infrastructure"),
    Path("src/core/presentation"),
    Path("tests"),
}

EXPECTED_FILES = {
    Path("README.md"),
    Path("manage.py"),
    Path("pyproject.toml"),
    Path("src/__init__.py"),
    Path("src/config/__init__.py"),
    Path("src/config/settings/__init__.py"),
    Path("src/config/settings/base.py"),
    Path("src/config/urls.py"),
    Path("src/config/wsgi.py"),
    Path("src/config/asgi.py"),
    Path("src/apps/__init__.py"),
    Path("src/core/__init__.py"),
    Path("src/core/application/__init__.py"),
    Path("src/core/domain/__init__.py"),
    Path("src/core/infrastructure/__init__.py"),
    Path("src/core/presentation/__init__.py"),
    Path("tests/__init__.py"),
}


def test_scaffold_creates_expected_structure() -> None:
    script_path = Path(__file__).resolve().parents[1] / "prueba.py"

    with TemporaryDirectory() as tmp_dir:
        destination = Path(tmp_dir)
        completed = subprocess.run(
            [sys.executable, str(script_path), str(destination), "--project-name", "mi_proyecto"],
            check=True,
            capture_output=True,
            text=True,
        )

        assert "Estructura de proyecto creada" in completed.stdout

        for directory in EXPECTED_DIRECTORIES:
            assert (destination / directory).is_dir(), f"No se creó el directorio {directory}"

        for file_path in EXPECTED_FILES:
            assert (destination / file_path).is_file(), f"No se creó el archivo {file_path}"

        manage_content = (destination / "manage.py").read_text(encoding="utf-8")
        assert "DJANGO_SETTINGS_MODULE" in manage_content

        pyproject_content = (destination / "pyproject.toml").read_text(encoding="utf-8")
        assert 'name = "mi_proyecto"' in pyproject_content

    # El contexto de TemporaryDirectory garantiza que los recursos se limpien
