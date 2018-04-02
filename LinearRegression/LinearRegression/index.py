from django import forms
from django.shortcuts import render, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from time import time
from os import mkdir

def index(request):
    """
    View function for home page of site.
    """
    # Render the HTML template index.html with the data in the context variable.
    return render(
        request,
        'index.html'
    )


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
