from django.shortcuts import render
from django.views.generic import TemplateView
from django.conf import settings
from scripts import panda_converter
from scripts import zip_script

# Create your views here.


def vis_view(request):
    path = settings.MEDIA_ROOT
    return render(request, 'vis.html', {'paths': path})
