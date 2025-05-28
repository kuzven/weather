from django.db import models


class CitySearchHistory(models.Model):
    city_name = models.CharField(max_length=100, unique=True, verbose_name="Название города")
    search_count = models.IntegerField(default=1, verbose_name="Количество запросов")

    def __str__(self):
        return f"{self.city_name} ({self.search_count} запросов)"

    class Meta:
        verbose_name = 'История поиска городов'
        verbose_name_plural = 'Истории поиска городов'
