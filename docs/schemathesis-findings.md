#	Чек	Категория	Действие
1	not_a_server_error	баг реализации	
2	negative_data_rejection	баг реализации	
3	positive_data_acceptance	ограничение схемы	документировать
4-6	status_code_conformance	дефект спеки	добавить responses
7	unsupported_method	баг реализации
8   Response violates schema баг реализации

## SCH-009. API rejected schema-compliant request

**Чек:** `positive_data_acceptance`
**Операция:** `POST /bookings`
**Вердикт:** ложное срабатывание, обосновано

**Причина.** Schemathesis генерирует данные, валидные по OpenAPI-схеме,
но нарушающие бизнес-правило `checkout > checkin`. Правило не выразимо
средствами JSON Schema — она не поддерживает зависимости между полями.

**Что сделано.**
1. Правило задокументировано в `description` операции.
2. В `schemathesis.toml` для чека `positive_data_acceptance`
   разрешён статус 422.
3. Правило покрыто ручным тестом
   `test_create_booking_with_checkout_before_checkin_returns_422`.

**Что НЕ сделано и почему.** Ослаблять валидацию на стороне API
нельзя — правило отражает предметную область (нельзя выехать
раньше, чем заехал) и продублировано check-constraint'ом в БД.

## SCH-010. GET /bookings/{id} возвращает 404 на валидный id

**Чек:** positive_data_acceptance
**Вердикт:** ложное срабатывание

404 — корректный ответ на запрос несуществующего ресурса.
Схема описывает валидность идентификатора, но не его существование.
Разрешено в schemathesis.toml.