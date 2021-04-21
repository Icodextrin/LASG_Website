from django.shortcuts import render
from django.conf import settings
from scripts import sankey
from scripts import panda_converter

# Create your views here.


def sankey_view(request):
    panda_converter.count_interactions()
    sankey.sankey_graph()
    return render(request, 'sankey.html')
