from time import time

from django.shortcuts import render, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt


def handle_uploaded_file(f, sep=';'):
    filename = str(round(time())) + ".csv"
    with open("files/.temp", 'wb') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    try:
        with open("files/.temp", "r") as source, open("files/" + filename, 'w') as destination:

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


@csrf_exempt
def calculate(request, num):
    """
    View function for home page of site.
    """
    try:
        with open("files/" + str(num) + ".csv", "r") as f:
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
    return render(
        request,
        'calculate.html',
        {'num': num, 'dataset': dataset, 'head': head}
    )
