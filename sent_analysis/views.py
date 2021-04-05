from django.shortcuts import render
from django.conf import settings
from scripts import sentimental_analysis

# Create your views here.


def sent_analysis_view(request):
    path = settings.MEDIA_ROOT
    sentimental_analysis.make_graphs()
    return render(request, 'sent_analysis.html')
