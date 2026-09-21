#!/usr/bin/env python
import os
import sys


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "biblioteca_project.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError("Django no esta instalado. Instala requirements.txt primero.") from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
