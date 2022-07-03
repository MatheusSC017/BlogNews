from django.shortcuts import render
from django.views.generic import TemplateView


class Home(TemplateView):
    template_name = 'blog/home.html'


def about(request):
    return render(request, 'blog/about.html')
