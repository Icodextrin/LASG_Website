from django.shortcuts import render
from django.conf import settings


# Create your views here.


def sent_analysis_view(request):
    path = settings.MEDIA_ROOT
    return render(request, 'sent_analysis.html')
