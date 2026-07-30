# Booking API — контракт v0.1

## Модель Booking
| Поле | Тип | Обязательное | Ограничения |
|---|---|---|---|
| id | int | — | генерируется сервером |
| firstname | string | да | 1–50 символов |
| lastname | string | да | 1–50 символов |
| totalprice | int | да | >= 0 |
| depositpaid | bool | да | |
| checkin | date | да | формат YYYY-MM-DD |
| checkout | date | да | строго > checkin |
| additionalneeds | string \| null | нет | до 200 символов |

## POST /bookings
- 201 Created + объект Booking с id
- 400 Bad Request — нарушены ограничения
- 422 — тело не соответствует схеме

## GET /bookings/{id}
- 200 + объект
- 404 — не найдено