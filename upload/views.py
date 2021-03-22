from django.shortcuts import render
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage

def upload(request):
    if request.method == 'POST':
        uploaded_files = request.FILES.getlist('documents')
        fs = FileSystemStorage()
        for ufile in uploaded_files:
            name = fs.save(ufile.name, ufile)
    return render(request, 'upload.html')
