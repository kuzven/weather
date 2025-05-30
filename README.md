# Weather - Сайт получения прогноза погоды по названию города

## Описание  
Проект **Weather** — это Django-приложение для получения прогноза погоды по названию города.

---

## Функции
✅ Корректный вывод прогноза погоды по названию города на 3 ближайших дня в удобочитаемом формате с информацией о температуре, осадках, ветре и облачности.

✅ Адаптивный дизайн для удобного просмотра на мобильных и десктопных устройствах.

✅ Использование Open-Meteo API для получения данных о погоде:
- Сначала выполняется запрос к Open-Meteo Geocoding API, чтобы получить координаты города по его названию.
- Затем запрашивается прогноз погоды, используя полученные координаты (широта и долгота).

✅ Автодополнение названий городов при вводе в поле поиска.

✅ Сохранение истории поиска для каждого пользователя по session_key.

✅ Статистика запросов: показывает, сколько раз вводили каждый город для каждого пользователя по session_key.

✅ При повторном посещении сайта (обновлении страницы) предлагается посмотреть погоду в последнем просмотренном городе.

✅ Помещено в Docker-контейнер для удобного развёртывания.

---

## ⚙ Использованные технологии
🔹 Backend: Python 3, Django 5

🔹 Frontend: JavaScript (jQuery), HTML/CSS, Bootstrap

🔹 База данных: PostgreSQL

🔹 API для погоды: Open-Meteo API

🔹 Контейнеризация: Docker, Docker Compose

🔹 Web-server: Nginx, Nginx Proxy Manager

---

## 🛠 Системные требования  
Перед установкой убедитесь, что на сервере **уже запущены контейнеры**:  
- **PostgreSQL** → [Инструкция по установке](https://github.com/kuzven/postgres)  
- **Nginx Proxy Manager** → [Инструкция по установке](https://github.com/kuzven/nginxproxymanager)

---

## Инструкция по установке и запуску на сервере с Docker

### **1️⃣ Клонирование репозитория**

```bash
cd ~
git clone https://github.com/kuzven/weather.git
cd weather
```

### **2️⃣ Создание .env файла**
- Создаём .env на основе шаблона:

```bash
cp .env.example .env
nano .env
```

- Сгенерируйте DJANGO_SECRET_KEY с помощью любого онлайн-генератора, например:

```
https://djecrety.ir/
```

- Скопируйте ключ и вставьте его в .env.
- Укажите значения для следующих параметров, например:

```
DJANGO_SECRET_KEY=n-v24$r$nmfhume8aeho@04nto(34$ir#_%4h1hx4xug&m71s7
DEBUG=False
ALLOWED_HOSTS=['domain.com','www.domain.com','127.0.0.1']
CSRF_TRUSTED_ORIGINS=http://domain.com,http://www.domain.com,https://domain.com,https://www.domain.com
MY_DOMAIN=http://domain.com
USE_POSTGRES=False
PG_DATABASE=domain_db
PG_USER=domain_user
PG_PASSWORD=SecurePassword
DB_HOST=postgres
DB_PORT=5432
USE_STATICFILES_DIRS=False
```

### **3️⃣ Настройка nginx.conf**

```bash
nano nginx.conf
```

- Укажите реальные домены в строке:

```
server_name domain.com www.domain.com;
```

### **4️⃣ Подготовка базы данных PostgreSQL**
Создаём базу данных weather_db и пользователя weather_user с доступом.

```bash
docker exec -it postgres psql -U admin -c "CREATE DATABASE weather_db;"
docker exec -it postgres psql -U admin -c "CREATE USER weather_user WITH LOGIN PASSWORD 'SecurePassword';"
docker exec -it postgres psql -U admin -c "ALTER DATABASE weather_db OWNER TO weather_user;"
docker exec -it postgres psql -U admin -c "GRANT ALL PRIVILEGES ON DATABASE weather_db TO weather_user;"
```

### **5️⃣ Запуск контейнера с weather**
Запускаем контейнеры weather-web и weather-nginx в фоне.

```bash
docker-compose up --build -d
```

### **6️⃣ Проверка запущенных контейнеров**

```bash
docker ps
```

Если weather-web и weather-nginx запущены, то переходим к настройке Django.

### **7️⃣ Применение миграций**

```bash
docker exec -it weather-web python manage.py migrate
```

### **8️⃣ Создание суперпользователя**

```bash
docker exec -it weather-web python manage.py createsuperuser
```

### **9️⃣ Сборка статических файлов**

```bash
docker exec -it weather-web python manage.py collectstatic --noinput
```

### **🔟 Настройка Nginx Proxy Manager**

Создайте Proxy Hosts для проекта, в поле Domain Names укажите домен, в Scheme укажите http, в Forward Hostname / IP укажите weather-nginx, в Forward Port укажите 80. При необходимости можно создать SSL сертификат в разделе SSL Certificates.

Теперь проект weather успешно запущен и должен быть доступен по указанному домену 🎉