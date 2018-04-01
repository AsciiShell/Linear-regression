# -*- coding: utf-8 -*-
"""
Решает квадратное уравнение
\tАвтор Подчезерцев А.Е.\n
"""
from math import sqrt

a = int(input("Введите A "))
b = int(input("Введите B "))
c = int(input("Введите C "))
d = b * b - 4 * a * c
x1 = (- b + sqrt(d)) / (2 * a)
x2 = (- b - sqrt(d)) / (2 * a)

print("Резульатат", x1, x2)
