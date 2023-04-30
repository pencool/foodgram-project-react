# Проект "Продуктовый помощник."

Сайт Foodgram - это онлайн сервис и API для него. На этом сайте пользователи могут публиковать свои рецепты и просматривать рецепты других пользователей. Так же зарегистрированные пользователи могут подписываться друг на друга и добавлять рецепты в избранно. Так же пользователи могут искать рецепты по тегам и применять различные фильтры для поиска. У пользователей есть возможность добавлять рецепты в список покупок, тем самым формируя лист покупок в котором будет находится список продуктов для приготовления рецептов добавленных в корзину.

## Ссылки для доступа к проекту:

    inprogress..




# Технологии

 - Python
 - Django
 - Docker
 - Django Rest Framework
 - Gunicorn
 - NGINX

## Запуск проекта

Для запуска проекта необходимо выполнить следующие действия:

 1. Клонировать репозиторий `git clone https://github.com/pencool/foodgram-project-react.git`
 2. Установить виртуальное окружение `python3 -m venv venv`
 3. Запустить виртуальное окружение `source venv/bin/activate`
 4. Установить необходимые компоненты `pip install -r requrements.txt`
 5. Для запуска локального сервера выполнить команду `python manage.py runserver`

## Просмотр документации

 1. Для просмотра локальной документации из папки infra выполнить команду `sudo docker-compose up -d`(Необходим Docker)
 2. Перейти по адресу http://localhost/api/doc
  
## Сборка контейнеров
in progress...

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