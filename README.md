# Synthetic API Stream Generator

Проект генерирует **поток синтетических API-событий** из вымышленных сервисов и публикует их в Kafka с рандомной периодичностью.

## Что делает приложение

- эмулирует запросы к вымышленным сервисам (`nebula-pay`, `astro-cart`, `galaxy-identity`, `orbit-delivery`);
- на каждом цикле формирует событие API (endpoint, метод, статус, latency, размер payload);
- публикует JSON-события в Kafka topic `synthetic-api-events`;
- интервал между событиями случайный в диапазоне `INTERVAL_MIN_SEC..INTERVAL_MAX_SEC`.

Это учебный проект для тренировки обработки стриминговых данных (Kafka, stream processing, аналитика, мониторинг).

## Состав

- `generator/message.py` — генератор синтетических API-событий;
- `generator/publication.py` — Kafka producer с бесконечным real-time циклом;
- `app/main.py` — минимальный HTTP health-check сервис;
- `docker-compose.yml` — локальный стек Kafka + генератор + HTTP API;
- `scripts/local-deploy.sh` — скрипт запуска/остановки/логов.

## Быстрый старт

### Вариант 1: скрипт

```bash
./scripts/local-deploy.sh up
```

Логи генератора:

```bash
./scripts/local-deploy.sh logs
```

Остановить:

```bash
./scripts/local-deploy.sh down
```

### Вариант 2: docker compose

```bash
docker compose up -d --build
```

## Проверка

- API health-check: `http://localhost:8000/health`
- События в Kafka: `docker compose logs -f generator`

Пример события:

```json
{
  "event_id": "f3bbf063-1a55-4d4d-bf0a-9fbbd5ff83e1",
  "created_at": "2026-04-20T12:30:45.351533+00:00",
  "source_service": "nebula-pay",
  "endpoint": "/payments/1324",
  "method": "GET",
  "status_code": 200,
  "latency_ms": 284,
  "payload_size_bytes": 1024
}
```

## Переменные окружения (generator)

- `KAFKA_BOOTSTRAP_SERVERS` (default: `kafka:9092`)
- `KAFKA_TOPIC` (default: `synthetic-api-events`)
- `INTERVAL_MIN_SEC` (default: `0.3`)
- `INTERVAL_MAX_SEC` (default: `2.5`)
- `LOG_LEVEL` (default: `INFO`)

