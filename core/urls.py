from django.urls import path
from .views import index, autocomplete_city, get_weather, get_last_city


urlpatterns = [
    path("", index, name="index"),
    path("autocomplete_city/", autocomplete_city, name="autocomplete_city"),
    path("get_weather/", get_weather, name="get_weather"),
    path("get_last_city/", get_last_city, name="get_last_city"),
]
