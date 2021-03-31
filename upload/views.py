from django.shortcuts import render
from django.conf import settings
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage
from scripts import test
import os


def upload_view(request):
    if request.method == 'POST':
        uploaded_files = request.FILES.getlist('documents')
        if len(request.FILES) == 0:  # if no files are uploaded display nofile.html
            return render(request, 'nofile.html')
        fs = FileSystemStorage()
        for ufile in uploaded_files:
            if fs.exists(ufile.name):  # if file exists, overwrite with new file
                os.remove(os.path.join(settings.MEDIA_ROOT, ufile.name))
            name = fs.save(ufile.name, ufile)

        file_list = os.listdir(settings.MEDIA_ROOT)
        return render(request, 'uploaded.html', {'files': file_list})

    # test.woot()
    return render(request, 'upload.html')
