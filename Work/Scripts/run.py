# -*- coding: utf-8 -*-
"""
Главный исполняемый файл для запуска WEB сервера

Автор: Создан автоматически
"""
import os
import sys

os.chdir("..")
sys.path.append(os.path.abspath(os.path.curdir))
sys.argv.append("runserver")
sys.argv.append("0.0.0.0:8080")
sys.argv.append("--noreload")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
try:
    from django.core.management import execute_from_command_line
except ImportError as exc:
    raise ImportError(
        "Couldn't import Django. Are you sure it's installed and "
        "available on your PYTHONPATH environment variable? Did you "
        "forget to activate a virtual environment?"
    ) from exc
execute_from_command_line(sys.argv)
