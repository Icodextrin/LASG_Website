from django.shortcuts import render
from django.conf import settings
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage
from scripts import test
import os

def upload_view(request):
    if request.method == 'POST':
        uploaded_files = request.FILES.getlist('documents')
        fs = FileSystemStorage()
        for ufile in uploaded_files:
            name = fs.save(ufile.name, ufile)
    test.woot()
    file_list = os.listdir(settings.MEDIA_ROOT)
    return render(request, 'upload.html', {'files':file_list})
