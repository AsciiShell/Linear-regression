from time import time
from random import random
from django.http import JsonResponse
from django.shortcuts import render, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt


def handle_uploaded_file(f, sep=';'):
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
    if request.method == 'POST':
        file = handle_uploaded_file(request.FILES['file'], request.POST['sep'])
        return HttpResponseRedirect(file)
    return render(request, 'index.html')


def load_dataset(name):
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
    arr = [[random(), random(), random(), random()] for _ in range(len(dataset[0]))]
    return random(), arr


@csrf_exempt
def calculate(request, num):
    """
    View function for home page of site.
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
