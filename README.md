![example workflow](https://github.com/pencool/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)
# Проект "Продуктовый помощник."

Сайт Foodgram - это онлайн сервис и API для него. На этом сайте пользователи могут публиковать свои рецепты и просматривать рецепты других пользователей. Так же зарегистрированные пользователи могут подписываться друг на друга и добавлять рецепты в избранно. Так же пользователи могут искать рецепты по тегам и применять различные фильтры для поиска. У пользователей есть возможность добавлять рецепты в список покупок, тем самым формируя лист покупок в котором будет находится список продуктов для приготовления рецептов добавленных в корзину.

## Ссылки для доступа к проекту:

| Адрес| Описание |
|--|--|
| http://pencoolfoodgram.ddns.net/ | Главная страница |
|http://51.250.101.248/|Главная страница|
|http://pencoolfoodgram.ddns.net/api/docs/  | Документация |
|http://pencoolfoodgram.ddns.net/admin/|Админ зона|





# Технологии

 - [![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
 - [![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
 - [![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
 - [![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
 - [![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
 - [![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
 - [![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
 - [![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)

## Запуск проекта

Для запуска проекта необходимо выполнить следующие действия:

 1. Клонировать репозиторий `git clone https://github.com/pencool/foodgram-project-react.git`
 2. Установить виртуальное окружение `python3 -m venv venv`
 3. Запустить виртуальное окружение `source venv/bin/activate`
 4. Установить необходимые компоненты `pip install -r requrements.txt`
 5. Для запуска локального сервера выполнить команду `python manage.py runserver`

## Просмотр документации

 - Для просмотра локальной документации из папки infra выполнить команду `sudo docker-compose up -d`(Необходим Docker)
 - Перейти по адресу http://localhost/api/doc
  
## Сборка контейнеров
 - Установить docker
 - Находясь в директории проекта infra из терминала выполнить следующие команды
 - `docker compose up -d --buils` - запустит контейнеры описанные в файле docker-compose.yml
 - `sudo docker exec foodgram_backend_1 python manage.py makemigrations` - создаем миграции
 - `sudo docker exec foodgram_backend_1 python manage.py migrate` - применяем миграции
 - `sudo docker exec foodgram_backend_1 python manage.py collectstatic --no-input` - собираем статику
 - `sudo docker exec foodgram_backend_1 python manage.py importdata` - импортируем начальные данные
 - `sudo docker exec foodgram_backend_1 python manage.py createsuperuser` - создаем учетную запись администратора

## Примеры запросов:
**`POST` | Создание рецепта: `http://127.0.0.1:8000/api/recipes/`**
Запрос:

    {
      "ingredients": [
        {
          "id": 1123,
          "amount": 10
        }
      ],
      "tags": [
        1,
        2
      ],
      "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
      "name": "string",
      "text": "string",
      "cooking_time": 1
    }

 
Ответ:

     {   "id": 0,   
     "tags": [
        {
          "id": 0,
          "name": "Завтрак",
          "color": "#E26C2D",
          "slug": "breakfast"
        }   ],   
        "author": {
        "email": "user@example.com",
        "id": 0,
        "username": "string",
        "first_name": "Вася",
        "last_name": "Пупкин",
        "is_subscribed": false   },   "ingredients": [
        {
          "id": 0,
          "name": "Картофель отварной",
          "measurement_unit": "г",
          "amount": 1
        }   ],   
        "is_favorited": true,   
        "is_in_shopping_cart": true,   
        "name": "string",   
        "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",   
        "text": "string",   "cooking_time": 1 }


**`POST` | Регистрация пользователя: `http://127.0.0.1:8000/api/users/`**
Запрос

    {
      "email": "vpupkin@yandex.ru",
      "username": "vasya.pupkin",
      "first_name": "Вася",
      "last_name": "Пупкин",
      "password": "Qwerty123"
    }

Ответ:

     {
      "email": "vpupkin@yandex.ru",
      "id": 0,
      "username": "vasya.pupkin",
      "first_name": "Вася",
      "last_name": "Пупкин"
    }

Автор проекта: [Павел Корчилов](https://github.com/pencool)
