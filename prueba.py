"""Utilities to scaffold a basic Django project."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional


class DjangoAdminNotFoundError(RuntimeError):
    """Raised when ``django-admin`` command cannot be located."""


class ProjectAlreadyExistsError(RuntimeError):
    """Raised when the target project directory already exists."""


def generate_django_project(project_name: str, destination: Optional[str] = None) -> Path:
    """Generate a new Django project using ``django-admin``.

    Parameters
    ----------
    project_name:
        Name of the Django project to create.
    destination:
        Optional directory where the project will be created. When ``None`` the
        current working directory is used.

    Returns
    -------
    Path
        The directory where the project was generated.

    Raises
    ------
    DjangoAdminNotFoundError
        If the ``django-admin`` executable cannot be found in ``PATH``.
    ProjectAlreadyExistsError
        If the output directory already contains the project folder.
    subprocess.CalledProcessError
        If ``django-admin`` exits with a non-zero status code.
    """

    django_admin_path = shutil.which("django-admin")
    if django_admin_path is None:
        raise DjangoAdminNotFoundError(
            "No se encontró 'django-admin'. Asegúrate de tener Django instalado."
        )

    target_root = Path(destination or Path.cwd()).resolve()
    project_path = target_root / project_name

    if project_path.exists():
        raise ProjectAlreadyExistsError(
            f"El directorio de proyecto '{project_path}' ya existe."
        )

    command = [django_admin_path, "startproject", project_name, str(target_root)]
    subprocess.run(command, check=True)

    return project_path


def main(argv: Optional[list[str]] = None) -> int:
    """Entrypoint for the CLI generator."""

    parser = argparse.ArgumentParser(
        description="Genera la estructura base de un proyecto Django."
    )
    parser.add_argument(
        "project_name",
        help="Nombre del proyecto Django a crear.",
    )
    parser.add_argument(
        "--dest",
        dest="destination",
        default=None,
        help=(
            "Directorio donde se generará el proyecto. Por defecto se usa el "
            "directorio actual."
        ),
    )

    args = parser.parse_args(argv)

    try:
        project_path = generate_django_project(args.project_name, args.destination)
    except DjangoAdminNotFoundError as exc:
        parser.error(str(exc))
    except ProjectAlreadyExistsError as exc:
        parser.error(str(exc))
    except subprocess.CalledProcessError as exc:
        parser.error(
            "La ejecución de 'django-admin' falló con el código de salida "
            f"{exc.returncode}."
        )

    print(f"Proyecto Django creado en: {project_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
