# 진행상황

> 컴퓨터를 옮겨 작업할 때 이 문서만 보고 현재 상태를 파악할 수 있도록 유지한다. 날짜 기록은 남기지 않고 항상 "지금 상태"만 담는다.

## 완료된 작업

- React + TypeScript + Vite 프런트엔드 초기 구성 (`frontend/`)
  - 고정 버전: React 19.2.8, Vite 8.2.2, TypeScript 6.0.2
  - `/api` 개발 프록시로 백엔드 8080 포트 연결, 연결 상태 확인 화면 포함
- Spring Boot + Java 21 + Gradle Kotlin DSL 백엔드 초기 구성 (`backend/`)
  - 고정 버전: Spring Boot 4.1.1, Gradle Wrapper 9.7.1
  - `/api/health` 최소 API와 HTTP 통합 테스트 작성
- 명령 래퍼(`scripts/`, `Makefile`) 제거 — npm·gradlew·docker compose를 직접 실행하는 방식으로 전환
- 실행/종료 명령만 추린 `COMMANDS.md` 작성 (인프라 전체·개별, 프런트엔드, 백엔드)
- 프로젝트 지침 및 문서 정리: `AGENTS.md`, `CLAUDE.md`, 한국어 `README.md`
- Kafka / Redis / RabbitMQ 로컬 컨테이너 구성 (`docker-compose.yaml`)
  - 고정 버전: Kafka 4.3.1(KRaft 단일 노드), Redis 8.2.9(LTS 라인), RabbitMQ 4.2.9-management(LTS 시리즈)
  - `docker compose up -d --wait` / `down` / `down -v`로 제어
  - 호스트·컨테이너 리스너 분리, 이름 있는 볼륨으로 데이터 유지, 포트·버전·비밀번호는 `.env`로 덮어쓰기
- GitHub 원격 저장소 연결 및 최초 푸시
  - 원격: https://github.com/jkchappydev/kafka-redis-rabbitmq
  - `main`을 기본 브랜치로 사용

## 다음 진행 예정

- Kafka / Redis / RabbitMQ 백엔드 연동
  - 브로커 컨테이너는 준비됐고 Spring Boot 쪽 의존성·설정은 아직 없는 상태
  - 실제 사용 시나리오(메시지 흐름, 캐시 대상)를 정한 뒤 `spring-kafka`, `spring-data-redis`, `spring-boot-starter-amqp`를 추가한다
  - 백엔드를 호스트에서 실행하므로 접속 주소는 `localhost:9092 / 6379 / 5672` 기준
- RabbitMQ 버전 정책 재검토
  - 4.2는 LTS 시리즈지만 커뮤니티 지원이 2026-07-31에 종료됐다. LTS 요건을 우선해 4.2로 두었고, 커뮤니티 지원이 필요하면 `.env`에서 4.3으로 올린다
- 비즈니스 기능 추가 시 Controller → Service → Repository 계층과 DTO 도입
  - 현재 health API는 비즈니스 로직과 DB가 없어 불필요한 계층을 만들지 않았다
- CI 구성 검토 (`.github/workflows/`가 비어 있음) — README의 검증 명령을 그대로 옮긴 워크플로 작성
