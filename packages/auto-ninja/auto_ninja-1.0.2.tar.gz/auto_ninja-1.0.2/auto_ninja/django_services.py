import ast
import os
import re
import sys
from pathlib import Path

import django

from auto_ninja.services import file


def extract_django_settings_module(manage_py_path: Path) -> str:
    content = manage_py_path.read_text()

    pattern = r"os\.environ\.setdefault\(\s*['\"]DJANGO_SETTINGS_MODULE['\"]\s*,\s*['\"](?P<settings>[\w\.]+)['\"]\s*\)"
    match = re.search(pattern, content)

    if not match:
        raise ValueError("DJANGO_SETTINGS_MODULE not found in manage.py")
    return match.group("settings")


def get_settings_module():
    manage_py_path = Path("manage.py")
    return extract_django_settings_module(manage_py_path)


def setup_django_environment(settings_module: str):
    file(Path("__init__.py"))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)
    sys.path.insert(0, os.getcwd())
    django.setup()


class ImportInjector(ast.NodeTransformer):
    def __init__(self, urls_path: Path):
        self.urls_path = urls_path
        self.import_found = False
        self.urlpatterns_found = False

    def visit_ImportFrom(self, node):
        # Check if the import already exists
        if node.module == f"{self.urls_path.parent.name}.api.main" and any(alias.name == "api" for alias in node.names):
            self.import_found = True
        return node

    def visit_Assign(self, node):
        # Look for the 'urlpatterns' assignment
        if any(isinstance(target, ast.Name) and target.id == "urlpatterns" for target in node.targets):
            # Check if 'api/' path is already present
            for elt in node.value.elts:
                if (
                    isinstance(elt, ast.Call)
                    and len(elt.args) > 0
                    and (isinstance(elt.args[0], ast.Constant) and elt.args[0].value == "api/")
                ):
                    self.urlpatterns_found = True
                    break

            # If not found, add it to the urlpatterns list
            if not self.urlpatterns_found:
                new_call = ast.Call(
                    func=ast.Name(id="path", ctx=ast.Load()),
                    args=[
                        ast.Constant(value="api/"),
                        ast.Attribute(
                            value=ast.Name(id="api", ctx=ast.Load()),
                            attr="urls",
                            ctx=ast.Load(),
                        ),
                    ],
                    keywords=[],
                )
                node.value.elts.append(new_call)
                self.urlpatterns_found = True
        return node


def modify_django_urls(urls_path: Path):
    tree = ast.parse(urls_path.read_text())

    injector = ImportInjector(urls_path)
    injector.visit(tree)

    # Add the import statement if it wasn't found
    if not injector.import_found:
        new_import = ast.ImportFrom(
            module=f"{urls_path.parent.name}.api.main",
            names=[ast.alias(name="api", asname=None)],
            level=0,
        )
        # Insert at the start, after initial module docstring if any
        if isinstance(tree.body[0], ast.Expr) and isinstance(tree.body[0].value, ast.Constant):
            tree.body.insert(1, new_import)
        else:
            tree.body.insert(0, new_import)

    # Write changes back to the file using ast.unparse
    urls_path.write_text(ast.unparse(tree))
