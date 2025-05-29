from django.contrib import admin
from .models import CitySearchHistory

@admin.register(CitySearchHistory)
class CitySearchHistoryAdmin(admin.ModelAdmin):
    list_display = ('session_key', 'city_name', 'search_count')  # Показываем поля в списке записей
    search_fields = ('city_name',)  # Добавляем поиск по названию города
    ordering = ('-search_count',)  # Сортируем по количеству запросов (по убыванию)
