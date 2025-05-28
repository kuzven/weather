from django.urls import path
from .views import autocomplete_city, get_weather


urlpatterns = [
    path("autocomplete_city/", autocomplete_city, name="autocomplete_city"),
    path("get_weather/", get_weather, name="get_weather"),
]
