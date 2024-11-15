# API для Yatube

## Описание

Яндекс Практикум. Спринт 11. Итоговый проект. API для Yatube.

### Технологии:

Python 3.10, Django 3.2.16, DRF, JWT

## Функционал

- Подписка и отписка от авторизованного пользователя;
- Авторизованный пользователь просматривает посты, создавёт новые, удаляет и изменяет их;
- Просмотр сообществ;
- Комментирование, просмотр, удаление и обновление комментариев;
- Фльтрация по полям.

## Установка

1. Клонировать репозиторий:

   ```python
   git clone https://github.com/Osipova228/api_final_yatube.git
   ```

2. Перейти в папку с проектом:

   ```python
   cd api_final_yatube/
   ```

3. Установить виртуальное окружение для проекта:

   ```python
   python -m venv venv
   ```

4. Активировать виртуальное окружение для проекта:

   ```python
   source venv/Scripts/activate
   ```

5. Установить зависимости:

   ```python
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

6. Выполнить миграции на уровне проекта:

   ```python
   cd yatube
   python manage.py makemigrations
   python manage.py migrate
   ```

7. Запустить проект:

   `python manage.py runserver`

## Примеры запросов

Получение токена

Отправить POST-запрос на адрес `api/v1/jwt/create/` и передать 2 поля в `data`:

1. `username` - имя пользователя.
2. `password` - пароль пользователя.

Создание поста

Отправить POST-запрос на адрес `api/v1/posts/` и необходимо указать обязательное поле `text`, в заголовке указать `Authorization`:`Bearer <токен>`.

1. Пример запроса:

   ```json
   {
     "text": "Мой пост №1."
   }
   ```

2. Пример ответа:

   ```json
   {
     "id": 1,
     "author": "Xenia",
     "text": "Мой пост #1.",
     "pub_date": "2023-11-22T12:00:22.021094Z",
     "image": null,
     "group": null
   }
   ```

Комментирование поста пользователя

Отправить POST-запрос на адрес `api/v1/posts/{post_id}/comments/` и необходимо указать обязательные поля `post` и `text`, в заголовке указать `Authorization`:`Bearer <токен>`.

1. Пример запроса:

   ```json
   {
     "post": 1,
     "text": "Тестовый комментарий"
   }
   ```

2. Пример ответа:

   ```json
   {
     "id": 1,
     "author": "Xenia",
     "text": "Тестовый комментарий",
     "created": "2023-11-22T12:06:13.146875Z",
     "post": 1
   }
   ```

### Author
[Osipova_Xenia](https://github.com/Osipova228)