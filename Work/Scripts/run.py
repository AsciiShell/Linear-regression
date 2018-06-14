# -*- coding: utf-8 -*-
"""
Главный исполняемый файл для запуска WEB сервера

Автор: Создан автоматически
Изменен: Подчезерцев А.Е.
"""
import os
import sys
import webbrowser
import _locale

if __name__ == "__main__":
    os.chdir("..")
    sys.path.append(os.path.abspath(os.path.curdir))
    from Library.weblib import load_config
    address = load_config()
    sys.argv.append("runserver")
    sys.argv.append(address)
    sys.argv.append("--noreload")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
    # Исравление стандартной кодировки
    _locale._getdefaultlocale = (lambda *args: ['en_US', 'utf-8'])
    print("\nЗапуск сервера\n")
    # Открытие браузера
    try:
        webbrowser.get().open("http://127.0.0.1:" + address.split(":")[1], new=2)
    except webbrowser.Error:
        print("Не удалось открыть браузер. Продолжение загрузки")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
