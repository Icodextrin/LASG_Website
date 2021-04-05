from django.shortcuts import render
from django.conf import settings
from scripts import message_by_year

# Create your views here.


def message_by_year_view(request):
    message_by_year.message_by_year_graph()
    return render(request, 'message_by_year.html')
