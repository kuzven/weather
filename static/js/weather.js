$(document).ready(function () {
    /**
     * Обработчик ввода текста в поле поиска города.
     * Отправляет AJAX-запрос в Django API /autocomplete_city/, получая список подходящих городов.
     */
    $("#city-input").on("input", function () {
        let query = $(this).val().trim();  // Убираем пробелы

        if (query.length > 1) {  // Начинаем поиск после 2 символов
            $.ajax({
                url: "/autocomplete_city",
                type: "GET",
                data: { query: query },
                success: function (data) {
                    let suggestions = $("#suggestions");
                    suggestions.empty();  // Очищаем предыдущие подсказки
                    
                    // Добавляем города в список
                    data.cities.forEach(city => {
                        suggestions.append(`<li class="list-group-item city-option">${city.name}</li>`);
                    });

                    // При клике на подсказку выбираем город и загружаем прогноз
                    $(".city-option").on("click", function () {
                        let cityName = $(this).text();
                        $("#city-input").val(cityName);
                        suggestions.empty();  // Очищаем список после выбора
                        getWeather(cityName);  // Запрос прогноза погоды
                    });
                }
            });
        }
    });

    /**
     * Запрашивает прогноз погоды для выбранного города через API Django /get_weather/.
     * Динамически обновляет таблицу с прогнозом на 3 дня.
     * 
     * @param {string} cityName - Название выбранного города
     */
    function getWeather(cityName) {
        $.ajax({
            url: "/get_weather",
            type: "GET",
            data: { city: cityName },
            success: function (data) {
                let weatherTableBody = $("#weather-table-body");
                weatherTableBody.empty();  // Очищаем таблицу перед добавлением новых данных

                if (data.error) {
                    alert(data.error);  // Выводим ошибку, если город не найден
                    return;
                }

                // Добавляем прогноз погоды на 3 дня в таблицу
                data.weather.forEach(day => {
                    weatherTableBody.append(`
                        <tr>
                            <td>${day.date}</td>
                            <td>${day.temperature_min}°C</td>
                            <td>${day.temperature_max}°C</td>
                            <td>${day.wind_speed} м/с</td>
                            <td>${day.precipitation} мм</td>
                            <td>${day.cloud_cover}%</td>
                        </tr>
                    `);
                });
            }
        });
    }
});
