from django.shortcuts import render
from parsers_app.models import Restaurants

def index(request):
    content = {"restaurants": Restaurants.objects.all()}
    return render(request, "index.html", context=content)
