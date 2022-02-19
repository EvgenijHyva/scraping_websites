from django.urls import path
from parsers_app.views import menu_view, manualrun

app_name = "parsers_app"

urlpatterns = [
    path("<int:restaurant_id>/", menu_view, name="menu"),
    path("manual", manualrun, name="manual_spider_run")
]