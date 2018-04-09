# -*- coding: utf-8 -*-
"""
Библиотека функций обработчиков web запросов

Данный файл сожержит методы для обработки данных и запросов web сервера

Автор: Подчезерцев А.Е.
"""
from time import time
from random import random
from django.http import JsonResponse
from django.shortcuts import render, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
import statsmodels.api as sm
from sklearn.datasets import load_boston


def handle_uploaded_file(f, sep=';'):
    """
    Проверяет загруженный файл
    :param f: Структура файла
    :param sep: Разделитель символов
    :return: Адрес для перенаправления: имя загруженного файла в случае успеха или '/' в обратном
    Автор: Подчезерцев А.Е.
    """
    filename = str(round(time())) + ".csv"
    with open("files/.temp", 'wb') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    try:
        with open("files/.temp", "r", encoding="utf-8") as source, open("files/" + filename, 'w',
                                                                        encoding="utf-8") as destination:

            data = source.read().splitlines()
            count = len(data[0].split(sep))
            types = [int for _ in range(count)]
            result = data[0] + "\n"
            data = data[1:]
            for line in data:
                items = line.split(sep)
                if len(items) != count:
                    return "/"
                for i in range(len(items)):
                    try:
                        types[i](items[i])
                    except ValueError:
                        types[i] = float
                    except Exception:
                        return "/"
                result += ";".join(items) + "\n"
            types = ";".join(["int" if _ == int else "float" for _ in types]) + "\n"
            destination.write(types + result)
    except Exception as e:
        return "/"
    return filename


@csrf_exempt
def uploadFile(request):
    """
    Обрабатывает web запрос загрузки файла
    :param request: Web-запрос
    :return: Перенаправление при отправке файла, иначе страницу
    Автор: Подчезерцев А.Е.
    """
    if request.method == 'POST':
        file = handle_uploaded_file(request.FILES['file'], request.POST['sep'])
        return HttpResponseRedirect(file)
    return render(request, 'index.html')


def load_dataset(name):
    """
    Загружает датасет с диска
    :param name: Имя файла
    :return: Датасет и Имена переменных, None в случае ошибки
    Автор: Подчезерцев А.Е.
    """
    dataset = None
    head = None
    try:
        with open("files/" + name + ".csv", "r", encoding="utf-8") as f:
            types = [int if _ == "int" else float for _ in f.readline()[:-1].split(";")]
            head = f.readline()[:-1].split(";")
            lines = f.readlines()
            dataset = []
            for line in lines:
                items = line.split(";")
                if len(head) != len(items):
                    dataset = None
                    break
                dataset.append([types[i](items[i]) for i in range(len(items))])
    except FileNotFoundError:
        dataset = None
    finally:
        return dataset, head


def handle_dataset(dataset, result, line, square):
    """
    Вычисляет параметры регрессии
    :param dataset: Датасет
    :param result: Номер результирующей переменной
    :param line: Логический массив переменных, которые должны быть обработаны линейно
    :param square: Логический массив переменных, которые должны быть обработаны квадратично
    :return: R квадрат и данные регрессии для переменных
    Автор: Подчезерцев А.Е.
    """
    arr = [[random(), random(), random(), random()] for _ in range(len(dataset[0]))]
    return random(), arr


@csrf_exempt
def calculate(request, num):
    """
    Обрабатывает web запрос вычисления регрессии
    :param request: Web-запрос
    :param num: номер файла
    :return: Данные регрессии при отправке запроса, иначе страницу
    Автор: Подчезерцев А.Е.
    """
    dataset, head = load_dataset(str(num))
    if request.method == "POST":
        result = None
        line = [False for _ in range(len(head))]
        square = [False for _ in range(len(head))]
        for key, value in request.POST.items():
            if key == 'result':
                result = head.index(value)
            elif key.startswith("variable-line-"):
                line[head.index(value)] = True
            elif key.startswith("variable-square-"):
                square[head.index(value)] = True
        if result is None or (True not in line and True not in square):
            return JsonResponse({'status': False})
        r, k = handle_dataset(dataset, result, line, square)
        return JsonResponse({'status': True, 'r': r, 'k': k, 'name': head})

    return render(
        request,
        'calculate.html',
        {'num': num, 'dataset': dataset, 'head': head}
    )
