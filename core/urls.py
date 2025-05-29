from django.urls import path
from .views import (
    index, autocomplete_city, get_weather, get_last_city,
    get_search_history, search_history, search_city
)


urlpatterns = [
    path("", index, name="index"),
    path("autocomplete_city/", autocomplete_city, name="autocomplete_city"),
    path("get_weather/", get_weather, name="get_weather"),
    path("get_last_city/", get_last_city, name="get_last_city"),
    path("get_search_history/", get_search_history, name="get_search_history"),
    path("search_history/", search_history, name="search_history"),
    path("search_city/", search_city, name="search_city"),
]
