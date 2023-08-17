#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import json
import os
import sys


def startapp(argv):
    app_name = argv[2]

    from distutils.dir_util import copy_tree
    copy_tree("base/start_app_template", app_name)
    with open(f"{app_name}/models/main.py", "r") as f:
        content = f.read()
        content = content.replace("base.start_app_template", app_name)
        content = content.replace("MainModel", f"{app_name.capitalize()}Model")
        content = content.replace(
            "MainSerializer", f"{app_name.capitalize()}Serializer"
        )
        content = content.replace("mainView", f"{app_name.capitalize()}View")
    with open(f"{app_name}/models/main.py", "w") as f:
        f.write(content)

    with open(f"{app_name}/models/__init__.py", "w") as f:
        f.write(f"from .main import {app_name.capitalize()}Model")

    with open(f"{app_name}/serializers/main.py", "r") as f:
        content = f.read()
        content = f"from {app_name}.models.main import {app_name.capitalize()}Model\n{content}"
        content = content.replace("Main", f"{app_name.capitalize()}")
        content = content.replace("object", f"{app_name.capitalize()}Model")
    with open(f"{app_name}/serializers/main.py", "w") as f:
        f.write(content)

    with open(f"{app_name}/apis/main.py", "r") as f:
        content = f.read()
        content = content.replace("base.start_app_template", app_name)
        content = content.replace("MainModel", f"{app_name.capitalize()}Model")
        content = content.replace(
            "MainModelSerializer", f"{app_name.capitalize()}ModelSerializer"
        )
    with open(f"{app_name}/apis/main.py", "w") as f:
        f.write(content)

    with open(f"{app_name}/admin.py", "r") as f:
        content = f.read()
        content = f"""from django.contrib import admin
from .models.main import {app_name.capitalize()}Model
admin.site.register({app_name.capitalize()}Model)
        """
    with open(f"{app_name}/admin.py", "w") as f:
        f.write(content)

    with open("conf/config.json") as f:
        config = json.load(f)
        config["INSTALLED_APPS"].append(
            f"{app_name}.apps.{app_name.capitalize()}Config"
        )
    with open("conf/config.json", "w") as f:
        json.dump(config, f, indent=4)


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    execute_from_command_line(sys.argv)
    if len(sys.argv) >=2 and sys.argv[1] == "startapp":
        startapp(sys.argv)


if __name__ == "__main__":
    main()
