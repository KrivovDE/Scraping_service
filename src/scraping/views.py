from django.shortcuts import render
from .models import Vacancy


def home_view(request):
    gs = Vacancy.objects.all()
    return render(request, 'scraping/home.html', {'object_list': gs})
