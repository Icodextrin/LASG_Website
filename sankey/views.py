from django.shortcuts import render
from django.conf import settings
from scripts import sankey

# Create your views here.


def sankey_view(request):
    sankey.sankey_graph()
    return render(request, 'sankey.html')
