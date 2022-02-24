from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Restaurants, RestaurantMenu
from datetime import date
from .tasks import run_scrapy_task

today = date.today()

def manual_run(request):
    run_scrapy_task.delay()
    return HttpResponseRedirect("/")

def menu_view(request, restaurant_id):
    content = {
        "restaurants": Restaurants.objects.all(),
        "menu": RestaurantMenu.objects.filter(restaurant=restaurant_id, date=today).first()
    }
    return render(request, "menu.html", context=content)

