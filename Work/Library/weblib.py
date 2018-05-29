# -*- coding: utf-8 -*-
"""
Библиотека функций загрузки и проверки настроек

Автор: Подчезерцев А.Е.
"""


def validate_port(port):
    """
    Проверяет является ли исходная строка валидным портом

    :param port: Строка для проверки
    :return: Логический результат проверки
    Автор: Подчезерцев А.Е.
    """
    if port.isdecimal():
        port = int(port)
        return 1 < port < 65536
    else:
        return False


def validate_ip(ip):
    """
    Проверяет является ли исходная строка валидным ip адресом

    :param ip: Строка для проверки
    :return: Логический результат проверки
    Автор: Подчезерцев А.Е.
    """
    byte = ip.split(".")
    if len(byte) == 4:
        for b in byte:
            if b.isdecimal():
                b = int(b)
                if not 0 <= b <= 255:
                    break
            else:
                break
        else:
            return True
    return False


def load_config(path="Scripts/settings.conf"):
    """
    Загружает настройки с диска, если они с ошибкой, то применит стандартные

    :param path: Путь к файлу настроек
    :return: ip адрес и порт, на котором необходимо запустить сервер
    Автор: Подчезерцев А.Е.
    """
    with open(path, "r") as f:
        for line in f.readlines():
            try:
                ip, port = line.strip().split(":")
                if validate_ip(ip) and validate_port(port):
                    return ":".join((ip, port))
            except ValueError:
                pass
            except Exception as e:
                raise e
        return "0.0.0.0:8080"
