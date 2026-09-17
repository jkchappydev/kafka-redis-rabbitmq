# 진행상황

> 컴퓨터를 옮겨 작업할 때 이 문서만 보고 현재 상태를 파악할 수 있도록 유지한다. 날짜 기록은 남기지 않고 항상 "지금 상태"만 담는다.

## 완료된 작업

- React + TypeScript + Vite 프런트엔드 초기 구성 (`frontend/`)
  - 고정 버전: React 19.2.8, Vite 8.2.2, TypeScript 6.0.2
  - `/api` 개발 프록시로 백엔드 8080 포트 연결, 연결 상태 확인 화면 포함
- Spring Boot + Java 21 + Gradle Kotlin DSL 백엔드 초기 구성 (`backend/`)
  - 고정 버전: Spring Boot 4.1.1, Gradle Wrapper 9.7.1
  - `/api/health` 최소 API와 HTTP 통합 테스트 작성
- 공통 명령 체계 구성: `make doctor / setup / dev / verify / smoke` (`scripts/harness.py`)
- 프로젝트 지침 및 문서 정리: `AGENTS.md`, `CLAUDE.md`, 한국어 `README.md`
- GitHub 원격 저장소 연결 및 최초 푸시
  - 원격: https://github.com/jkchappydev/kafka-redis-rabbitmq
  - `main`을 기본 브랜치로 사용

## 다음 진행 예정

- Kafka / Redis / RabbitMQ 연동 설계
  - 저장소 이름에 포함되어 있으나 아직 요구사항이 확정되지 않아 구성하지 않은 상태
  - 실제 사용 시나리오(메시지 흐름, 캐시 대상)를 정한 뒤 의존성을 추가한다
- 비즈니스 기능 추가 시 Controller → Service → Repository 계층과 DTO 도입
  - 현재 health API는 비즈니스 로직과 DB가 없어 불필요한 계층을 만들지 않았다
- CI 구성 검토 (`.github/workflows/`가 비어 있음) — `make verify` 기준의 워크플로 작성
