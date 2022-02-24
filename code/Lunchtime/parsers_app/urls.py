from django.urls import path
from parsers_app.views import menu_view, manual_run

app_name = "parsers_app"

urlpatterns = [
    path("<int:restaurant_id>/", menu_view, name="menu"),
    path("manual", manual_run, name="manual_spider_run")
]