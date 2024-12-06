from pathlib import Path
from typing import Optional

import typer
from django.apps import apps

from auto_ninja.cases import snake_case, kebab_case
from auto_ninja.django_services import (
    modify_django_urls,
    get_settings_module,
    setup_django_environment,
)
from auto_ninja.services import find_auto_ninja_templates, file, folder


def main(
    title: Optional[str] = "Auto Ninja",
    description: Optional[str] = "Automatically generated API",
):  # Variables
    settings_module = get_settings_module()
    settings = Path(settings_module.replace(".", "/")).parent
    setup_django_environment(settings_module)
    templates = find_auto_ninja_templates()
    installed_apps = [(Path(app.name), app) for app in apps.get_app_configs() if Path(app.name).exists()]

    # Settings
    api = folder(settings / "api")
    file(api / "__init__.py")
    file(api / "services.py/", templates / "services.py.txt")
    file(api / "utils.py/", templates / "utils.py.txt")
    file(
        api / "main.py/",
        templates / "main.py.txt",
        {"apps": installed_apps, "title": title, "description": description},
    )
    modify_django_urls(settings / "urls.py")

    # Apps
    for app_path, app in installed_apps:
        app_api = folder(app_path / "api")
        file(app_api / "__init__.py")
        endpoints = folder(app_api / "endpoints")
        schemas = folder(app_api / "schemas")

        models = [model.__name__ for model in app.get_models()]
        model_modules = [snake_case(model) for model in models]
        model_paths_modules = [(kebab_case(model), snake_case(model)) for model in models]

        file(
            endpoints / "__init__.py",
            templates / "endpoint_init.py.txt",
            {
                "path_modules": model_paths_modules,
                "app": app,
                "settings": str(settings),
            },
        )
        file(
            schemas / "__init__.py",
            templates / "schema_init.py.txt",
            {"models": model_modules},
        )

        for model in models:
            context = {
                "app": app,
                "model": model,
                "settings": str(settings),
            }
            file(
                endpoints / f"{snake_case(model)}.py",
                templates / "endpoint.py.txt",
                context,
            )
            file(
                schemas / f"{snake_case(model)}.py",
                templates / "schema.py.txt",
                context,
            )


if __name__ == "__main__":
    typer.run(main)
