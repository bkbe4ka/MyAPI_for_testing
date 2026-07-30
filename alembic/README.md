# Booking API

Учебный проект: REST API бронирования на FastAPI + PostgreSQL.
Разрабатывается вместе с тестовым фреймворком для практики API-тестирования.

## Запуск

cp .env.example .env        # заполнить значения
docker compose up -d
docker compose exec api alembic upgrade head

- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- OpenAPI: http://localhost:8000/openapi.json

## Стек

FastAPI · SQLAlchemy 2.0 · Alembic · PostgreSQL 16 · Docker Compose

## Контракт

Спецификация зафиксирована в [SPEC.md](SPEC.md) **до** реализации —
чтобы тесты проверяли требования, а не то, что получилось.