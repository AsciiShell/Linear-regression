# -*- coding: utf-8 -*-
"""
Стандартная библиотека для обработки данных

Данный файл сожержит методы для обработки данных и датасетов

Авторы: Подчезерцев А.Е.
        Солодянкин А.А.
"""
from time import time

import pandas as pd
from statsmodels.formula.api import ols

DATASET_PATH = "Data/"


def load_dataset(name, sep=',', end=None):
    """
    Загружает датасет с диска

    :param name: Имя файла
    :param sep: Формат разделителя столбцов, по умолчанию ','
    :param end: Формат разделителя строк, по умолчанию '\n'
    :return: Датасет
    Автор: Подчезерцев А.Е.
    """
    return pd.read_csv(name, sep=sep, lineterminator=end, encoding='utf-8')


def handle_uploaded_file(f, sep=';', end=None):
    """
    Проверяет загруженный файл

    :param f: Структура файла
    :param sep: Разделитель символов
    :param end: Разделитель строк
    :return: Адрес для перенаправления: имя загруженного файла в случае успеха или '/' в обратном
    Автор: Подчезерцев А.Е.
    """
    filename = str(round(time())) + ".csv"
    if end is None:
        end = '\n'
    with open(DATASET_PATH + ".temp", 'wb') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    try:
        dataset = load_dataset(DATASET_PATH + ".temp", sep, end)
        dataset.to_csv(DATASET_PATH + filename, encoding='utf-8')
    except Exception:
        return "/"
    return filename


def handle_dataset(dataset, result, line, square):
    """
    Вычисляет параметры регрессии

    :param dataset: Датасет
    :param result: Номер результирующей переменной
    :param line: Логический массив переменных, которые должны быть обработаны линейно
    :param square: Логический массив переменных, которые должны быть обработаны квадратично
    :return: R квадрат и данные регрессии для переменных
    Автор: Солодянкин А.А.
    """
    statement = dataset.columns[result] + " ~ "
    variables = []
    for i in range(len(line)):
        if square[i]:
            dataset = dataset.assign(cp=lambda x: x[dataset.columns[i]] ** 2)
            dataset.rename(columns={"cp": dataset.columns[i] + "Квадрат"}, inplace=True)
            variables.append(dataset.columns[i] + "Квадрат")
        if line[i]:
            variables.append(dataset.columns[i])
    statement += " + ".join(variables)
    model = ols(statement, dataset).fit()
    return model.rsquared, [model.params.to_dict(),
                            model.bse.to_dict(),
                            model.tvalues.to_dict(),
                            model.pvalues.to_dict(), ]
