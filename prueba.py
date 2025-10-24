"""Utility script for scaffolding a Django project with a clean architecture layout."""
from __future__ import annotations

import argparse
from pathlib import Path
from textwrap import dedent


DIRECTORIES = [
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
]


FILES = {
    Path("README.md"): dedent(
        """
        # {project_name}

        Este proyecto fue generado automáticamente utilizando el script de plantilla.
        El objetivo es proporcionar una estructura inicial basada en Clean Architecture
        para un proyecto de Django, separando las responsabilidades en capas bien definidas.
        """
    ).strip()
    + "\n",
    Path("manage.py"): dedent(
        '''
        #!/usr/bin/env python
        """Punto de entrada para las tareas administrativas de Django."""

        import os
        import sys


        def main() -> None:
            os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.config.settings.base")
            try:
                from django.core.management import execute_from_command_line
            except ImportError as exc:  # pragma: no cover - Django puede no estar instalado durante las pruebas
                raise ImportError(
                    "No se pudo importar Django. Asegúrate de que esté instalado en tu entorno."
                ) from exc
            execute_from_command_line(sys.argv)


        if __name__ == "__main__":
            main()
        '''
    ).strip()
    + "\n",
    Path("pyproject.toml"): dedent(
        """
        [build-system]
        requires = ["setuptools", "wheel"]
        build-backend = "setuptools.build_meta"

        [project]
        name = "{project_name}"
        version = "0.1.0"
        description = "Plantilla base de Django con Clean Architecture"
        readme = "README.md"
        requires-python = ">=3.10"
        authors = [
            { name = "Plantilla Automática", email = "dev@example.com" }
        ]
        dependencies = [
            "django>=4.2",
        ]
        """
    ).strip()
    + "\n",
    Path("src/__init__.py"): "\n",
    Path("src/config/__init__.py"): "\n",
    Path("src/config/settings/__init__.py"): "\n",
    Path("src/config/settings/base.py"): dedent(
        '''
        """Configuración base del proyecto Django."""

        from pathlib import Path

        BASE_DIR = Path(__file__).resolve().parent.parent.parent

        SECRET_KEY = "django-insecure-change-me"
        DEBUG = True
        ALLOWED_HOSTS: list[str] = []

        INSTALLED_APPS = [
            "django.contrib.admin",
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sessions",
            "django.contrib.messages",
            "django.contrib.staticfiles",
        ]

        MIDDLEWARE = [
            "django.middleware.security.SecurityMiddleware",
            "django.contrib.sessions.middleware.SessionMiddleware",
            "django.middleware.common.CommonMiddleware",
            "django.middleware.csrf.CsrfViewMiddleware",
            "django.contrib.auth.middleware.AuthenticationMiddleware",
            "django.contrib.messages.middleware.MessageMiddleware",
            "django.middleware.clickjacking.XFrameOptionsMiddleware",
        ]

        ROOT_URLCONF = "src.config.urls"
        WSGI_APPLICATION = "src.config.wsgi.application"

        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": BASE_DIR / "db.sqlite3",
            }
        }

        AUTH_PASSWORD_VALIDATORS = []

        LANGUAGE_CODE = "es-es"
        TIME_ZONE = "UTC"
        USE_I18N = True
        USE_TZ = True

        STATIC_URL = "static/"

        DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
        '''
    ).strip()
    + "\n",
    Path("src/config/urls.py"): dedent(
        '''
        """Configuración de URLs del proyecto."""

        from django.contrib import admin
        from django.urls import path

        urlpatterns = [
            path("admin/", admin.site.urls),
        ]
        '''
    ).strip()
    + "\n",
    Path("src/config/wsgi.py"): dedent(
        '''
        """Configuración WSGI para el proyecto."""

        import os
        from django.core.wsgi import get_wsgi_application

        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.config.settings.base")

        application = get_wsgi_application()
        '''
    ).strip()
    + "\n",
    Path("src/config/asgi.py"): dedent(
        '''
        """Configuración ASGI para el proyecto."""

        import os
        from django.core.asgi import get_asgi_application

        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.config.settings.base")

        application = get_asgi_application()
        '''
    ).strip()
    + "\n",
    Path("src/apps/__init__.py"): "\n",
    Path("src/core/__init__.py"): "\n",
    Path("src/core/application/__init__.py"): "\n",
    Path("src/core/domain/__init__.py"): "\n",
    Path("src/core/infrastructure/__init__.py"): "\n",
    Path("src/core/presentation/__init__.py"): "\n",
    Path("tests/__init__.py"): "\n",
}


def create_structure(destination: Path, project_name: str) -> None:
    """Create the directory structure and files for the project."""
    destination.mkdir(parents=True, exist_ok=True)
    for directory in DIRECTORIES:
        target_dir = destination / directory
        target_dir.mkdir(parents=True, exist_ok=True)

    for relative_path, content in FILES.items():
        target_file = destination / relative_path
        target_file.parent.mkdir(parents=True, exist_ok=True)
        target_file.write_text(content.replace("{project_name}", project_name), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Genera la estructura básica de un proyecto Django con Clean Architecture."
    )
    parser.add_argument(
        "destination",
        nargs="?",
        default=".",
        help="Directorio donde se generará la plantilla (por defecto el directorio actual).",
    )
    parser.add_argument(
        "--project-name",
        default="django_clean_architecture",
        help="Nombre del proyecto que se usará en los archivos generados.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    destination = Path(args.destination).resolve()
    create_structure(destination, args.project_name)
    print(f"Estructura de proyecto creada en: {destination}")


if __name__ == "__main__":
    main()
