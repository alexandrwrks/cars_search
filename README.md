# Cars Search API

REST API для поиска автомобилей, просмотра информации об автомобилях и получения статистики.


## Описание проекта

---
Cars Search API — REST API, разработанный на FastAPI.

Проект собирает данные об автомобилях с kolesa.kz, сохраняет их в PostgreSQL 
и предоставляет API для поиска автомобилей, просмотра информации, 
статистики и работы с избранным.

## Стэк технологий

---
- Python 3.12
- FastAPI
- Pydantic
- SQLAlchemy
- httpx
- BeautifulSoup4
- PyJWT
- Redis
- PyTest
- PostgreSQL

## Возможности

---
- Регистрация пользователей
- Авторизация пользователей
- Получение списка автомобилей
- Получение информации об автомобиле
- Добавление автомобилей в избранное
- Просмотр статистики
- Получение самой просматриваемой машины
- Кэширование запросов с Redis
- Интеграционные тесты
- Проект включает собственный парсер объявлений автомобилей

## Основные возможности

---
- JWT авторизация
- Repository Pattern
- Service Layer
- Redis Cache
- Async SQLAlchemy
- Интеграционные тесты
- Парсинг данных

## Запуск

---
```shell

git clone https://github.com/alexandrwrks/cars_search.git

uv venv

uv sync

# Создать .env 
cp .env.example .env

alembic upgrade head

uvicorn app.main:app --port 8000 --host 0.0.0.0
```

## Альтернативный запуск

---
```shell
python -m app.main
```

## Запуск тестов

---
```shell
pytest
```

