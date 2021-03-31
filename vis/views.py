from django.shortcuts import render
from django.views.generic import TemplateView
from scripts import test_plot
from django.conf import settings
from scripts import panda_converter
from scripts import zip_script

# Create your views here.


def vis_view(request):
    path = settings.MEDIA_ROOT
    test_plot.plot_test(path + '/test_graph.png')
    zip_script.unzip_all_files(path)
    panda_converter.output_csv(path)
    return render(request, 'vis.html', {'paths': path})
