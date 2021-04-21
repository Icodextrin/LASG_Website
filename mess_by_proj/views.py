from django.shortcuts import render
from django.conf import settings
from scripts import message_by_year
import os

# Create your views here.


def message_by_proj_view(request):
    path = settings.MEDIA_ROOT
    message_by_year.message_by_project_by_year()
    files = os.listdir(path + '/graphs/mess_by_proj/')
    return render(request, 'message_by_proj.html', {'files': files})
