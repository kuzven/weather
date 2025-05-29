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

    function formatDate(isoDate) {
        let [year, month, day] = isoDate.split("-");
        return `${day}.${month}.${year}`;
    }

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
                let weatherTitle = $("#weather-title");
                let weatherTableBody = $("#weather-table-body");
                let weatherCards = $("#weather-cards");
                weatherTableBody.empty();  // Очищаем таблицу перед добавлением новых данных
                weatherCards.empty(); // Очищаем карточки перед добавлением новых данных

                if (data.error) {
                    alert(data.error);  // Выводим ошибку, если город не найден
                    weatherTitle.hide();
                    $("#weather-table").hide();
                    return;
                }

                // Обновляем заголовок с названием города
                weatherTitle.text(`Прогноз погоды в городе ${data.city} на 3 ближайших дня`).show();

                // Добавляем прогноз погоды на 3 дня
                data.weather.forEach(day => {
                    let formattedDate = formatDate(day.date);

                    // Заполняем таблицу (если экран >767px)
                    weatherTableBody.append(`
                        <tr>
                            <td>${formattedDate}</td>
                            <td>${day.temperature_min}°C</td>
                            <td>${day.temperature_max}°C</td>
                            <td>${day.wind_speed} м/с</td>
                            <td>${day.precipitation} мм</td>
                            <td>${day.cloud_cover}%</td>
                        </tr>
                    `);

                    // Создаём карточку (если экран ≤767px)
                    let card = `
                        <div class="weather-card p-3 mb-2">
                            <h4>${formattedDate}</h4>
                            <p>🌡️ Мин t: ${day.temperature_min}°C</p>
                            <p>🔥 Макс t: ${day.temperature_max}°C</p>
                            <p>💨 Ветер: ${day.wind_speed} м/с</p>
                            <p>🌧️ Осадки: ${day.precipitation} мм</p>
                            <p>☁️ Облачность: ${day.cloud_cover}%</p>
                        </div>
                    `;
                    weatherCards.append(card);
                });

                // Показываем нужный блок в зависимости от размера экрана
                if ($(window).width() <= 767) { 
                    weatherCards.removeClass("d-none").addClass("d-block"); // Убираем d-none
                    $("#weather-table").hide();
                } else {
                    weatherCards.addClass("d-none").removeClass("d-block"); // Возвращаем d-none
                    $("#weather-table").show();
                }                
            }
        });
    }
});
