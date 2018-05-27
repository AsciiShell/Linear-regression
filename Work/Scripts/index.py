# -*- coding: utf-8 -*-
"""
Библиотека функций обработчиков web запросов

Данный файл сожержит методы для обработки данных и запросов web сервера

Авторы: Подчезерцев А.Е.
        Солодянкин А.А.
"""

from django.http import JsonResponse
from django.shortcuts import render, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from Library.reglib import *


@csrf_exempt
def upload_file(request):
    """
    Обрабатывает web запрос загрузки файла

    :param request: Web-запрос
    :return: Перенаправление при отправке файла, иначе страницу
    Автор: Подчезерцев А.Е.
    """
    if request.method == 'POST':
        end = None
        if request.POST['end'] == 'LF':
            end = '\n'
        elif request.POST['end'] == 'CR':
            end = '\r'
        elif request.POST['end'] == 'CRLF':
            end = '\r\n'
        file = handle_uploaded_file(request.FILES['file'], request.POST['sep'], end)
        return HttpResponseRedirect(file)
    return render(request, 'index.html')


@csrf_exempt
def calculate(request, num):
    """
    Обрабатывает web запрос вычисления регрессии

    :param request: Web-запрос
    :param num: номер файла
    :return: Данные регрессии при отправке запроса, иначе страницу
    Автор: Солодянкин А.А.
    """
    dataset = load_dataset(DATASET_PATH + str(num) + ".csv")
    if request.method == "POST":
        result = None
        line = [False for _ in range(len(dataset.columns))]
        square = [False for _ in range(len(dataset.columns))]
        for key, value in request.POST.items():
            if key == 'result':
                result = dataset.columns.get_indexer_for([value])[0]
            elif key.startswith("variable-line-"):
                line[dataset.columns.get_indexer_for([value])[0]] = True
            elif key.startswith("variable-square-"):
                square[dataset.columns.get_indexer_for([value])[0]] = True
        if result is None or (True not in line and True not in square):
            return JsonResponse({'status': False})
        r, k = handle_dataset(dataset, result, line, square)
        return JsonResponse({'status': True, 'r': r, 'k': k})

    return render(
        request,
        'calculate.html',
        {'num': num, 'dataset': dataset, 'head': dataset.columns.tolist()[1:]}
    )
