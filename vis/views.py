from django.shortcuts import render
from django.views.generic import TemplateView
import scripts
from django.conf import settings

# Create your views here.

def vis_view(request):
    path = settings.MEDIA_ROOT
    return render(request, 'vis.html', {'paths': path})
