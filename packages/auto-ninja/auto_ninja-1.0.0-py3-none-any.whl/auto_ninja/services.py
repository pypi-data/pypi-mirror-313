import importlib
from pathlib import Path

from django.template import Engine, Context


def folder(dest: Path) -> Path:
    dest.mkdir(parents=True, exist_ok=True)
    return dest


def file(dest: Path, template_file: Path = None, context: dict = None):
    context = context or {}
    if template_file:
        template = Engine(dirs=[], app_dirs=True).from_string(template_file.read_text())
        dest.write_text(template.render(Context(context)))
    else:
        dest.touch(exist_ok=True)


def find_auto_ninja_templates() -> Path:
    spec = importlib.util.find_spec("auto_ninja")
    if spec is None or spec.origin is None:
        raise ImportError("auto_ninja package not found")
    package_path = Path(spec.origin).parent
    return package_path / "templates"
