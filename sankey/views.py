from django.shortcuts import render
from django.conf import settings
from scripts import sankey
from scripts import panda_converter
import os

# Create your views here.


def sankey_view(request):
    path = settings.MEDIA_ROOT
    panda_converter.count_interactions()
    sankey.sankey_graph()
    files = os.listdir(path + '/graphs/sankey/')
    return render(request, 'sankey.html', {'files': files})
