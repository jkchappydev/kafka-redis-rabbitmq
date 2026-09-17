# 명령어 모음

## 인프라 (Kafka / Redis / RabbitMQ)

전체

- 실행 — `docker compose up -d`
- 종료 — `docker compose down`

개별

- Kafka 실행 — `docker compose up -d kafka`
- Kafka 종료 — `docker compose stop kafka`
- Redis 실행 — `docker compose up -d redis`
- Redis 종료 — `docker compose stop redis`
- RabbitMQ 실행 — `docker compose up -d rabbitmq`
- RabbitMQ 종료 — `docker compose stop rabbitmq`

## 프론트엔드

- 실행 — `cd frontend && npm run dev`
- 종료 — 실행한 터미널에서 `Ctrl+C`

## 백엔드

- 실행 — `cd backend && ./gradlew bootRun`
- 종료 — 실행한 터미널에서 `Ctrl+C`

