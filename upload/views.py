from django.shortcuts import render
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage
import os
from django.conf import settings
from scripts import panda_converter
from scripts import zip_script


def upload_view(request):
    # if page is requested via upload button press do file upload
    if request.method == 'POST':
        uploaded_files = request.FILES.getlist('documents')
        if len(request.FILES) == 0:  # if no files are uploaded display nofile.html
            return render(request, 'nofile.html')
        fs = FileSystemStorage()
        for ufile in uploaded_files:
            if fs.exists(ufile.name):  # if file exists, overwrite with new file
                os.remove(os.path.join(settings.MEDIA_ROOT, ufile.name))
            name = fs.save(ufile.name, ufile)

        file_list = uploaded_files
        path = settings.MEDIA_ROOT
        zip_script.unzip_all_files(path) # unzip
        panda_converter.output_csv(path)
        return render(request, 'uploaded.html', {'files': file_list}) # pass render request with file names

    return render(request, 'upload.html')


def loading_view(request):
    return render(request, "loading.html")

