from time import time

from django import forms
from django.shortcuts import render, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt



class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()


def handle_uploaded_file(f):
    filename = str(round(time())) + ".csv"
    with open("files/" + filename, 'wb') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return filename


@csrf_exempt
def uploadFile(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        file = handle_uploaded_file(request.FILES['file'])
        return HttpResponseRedirect(file)
    else:
        form = UploadFileForm()
    return render(request, 'index.html', {'form': form})

@csrf_exempt
def calculate(request, num):
    """
    View function for home page of site.
    """
    try:
        with open("files/" + str(num) + ".csv", "r") as f:
            head = f.readline()[:-1].split(";")
            lines = f.readlines()
            dataset = []
            for line in lines:
                items = line.split(";")
                if len(head) != len(items):
                    dataset = None
                    break
                dataset.append([float(i) for i in items])
    except FileNotFoundError:
        dataset = None
    return render(
        request,
        'calculate.html',
        {'num': num, 'dataset': dataset, 'head': head}
    )