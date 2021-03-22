from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def upload_view(request, *args, **kwargs):
    return HttpResponse("<h1>Upload</h1>")
