# React + Spring Boot 기본 프로젝트

React 화면에서 Spring Boot의 `/api/health`에 연결하는 최소 프로젝트입니다.

## 개발 환경

- Node.js 24 LTS, npm 11 (`nvm use`)
- JDK 21 LTS (`JAVA_HOME`도 JDK 21로 설정)
- Docker Desktop (로컬 인프라 컨테이너용)
- Gradle은 저장소의 Wrapper 사용, 별도 설치 불필요

버전 확인:

```sh
node --version    # v24.x
java -version     # 21.x
```

## 시작

설치 (최초 1회, 또는 의존성이 바뀌었을 때):

```sh
cd frontend && npm ci
cd backend && ./gradlew classes testClasses
```

개발 서버 실행 (터미널 두 개에서 각각):

```sh
cd backend && ./gradlew bootRun     # 8080
cd frontend && npm run dev          # 5173
```

화면: http://localhost:5173
백엔드: http://localhost:8080/api/health
응답: `{"status":"UP"}`

Vite가 `/api` 요청을 8080 포트로 전달합니다. 서버 시작 전에 화면을 열었다면 백엔드 준비 후 새로고침하세요. 5173·8080 포트는 비어 있어야 합니다. 개발 프록시는 프로덕션 빌드에 포함되지 않으므로 배포 시 동일 경로의 reverse proxy가 필요합니다.

## 로컬 인프라 (Kafka / Redis / RabbitMQ)

Docker 컨테이너로 메시징·캐시 브로커를 띄웁니다. Docker Desktop이 실행 중이어야 합니다.

```sh
docker compose up -d --wait    # 기동, 세 서비스가 healthy가 될 때까지 대기
docker compose ps              # 컨테이너 상태
docker compose logs -f kafka   # 특정 서비스 로그
docker compose down            # 종료 (데이터 볼륨 유지)
docker compose down -v         # 종료 및 데이터 볼륨 삭제
```

동작 확인:

```sh
docker compose exec kafka /opt/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --list
docker compose exec redis redis-cli -a localredis --no-auth-warning ping
docker compose exec rabbitmq rabbitmq-diagnostics -q check_running
```

`--wait`는 헬스체크가 통과할 때까지 기다립니다. 기동에 실패하면 `docker compose logs <서비스>`로 원인을 봅니다. 9092·6379·5672·15672 포트가 비어 있어야 합니다.

| 서비스 | 호스트 접속 | 컨테이너 내부 | 기본 인증 |
| --- | --- | --- | --- |
| Kafka | `localhost:9092` | `kafka:19092` | 없음 (PLAINTEXT) |
| Redis | `localhost:6379` | `redis:6379` | password `localredis` |
| RabbitMQ | `localhost:5672` | `rabbitmq:5672` | `local` / `localrabbit` |
| RabbitMQ 관리 콘솔 | http://localhost:15672 | - | `local` / `localrabbit` |

포트·버전·비밀번호를 바꾸려면 `cp .env.example .env` 후 수정합니다. `.env`는 커밋되지 않으며, 위 값은 로컬 개발 전용이므로 운영 환경에 그대로 사용하지 않습니다.

Kafka는 4.x부터 ZooKeeper가 제거되어 KRaft 단일 노드(broker + controller 겸용)로 실행합니다. 호스트용 리스너와 컨테이너용 리스너를 분리해 두었으므로, 백엔드를 호스트에서 실행하면 `localhost:9092`, 컨테이너에서 실행하면 `kafka:19092`를 사용합니다.

데이터는 이름 있는 볼륨(`krr-infra_kafka-data`, `krr-infra_redis-data`, `krr-infra_rabbitmq-data`)에 보관되어 `docker compose down` 후 재기동해도 유지됩니다. 초기화가 필요하면 `docker compose down -v`를 사용합니다.

## 검증

정적 검사·타입 검사·빌드·테스트:

```sh
cd frontend && npm run lint && npm run build   # Oxlint, TypeScript, Vite 빌드
cd backend && ./gradlew check bootJar          # Spring 테스트 및 실행 JAR 생성
```

HTTP 연동 확인 (개발 서버를 띄운 상태에서):

```sh
curl -s http://localhost:8080/api/health   # {"status":"UP"}
curl -s http://localhost:5173/api/health   # Vite 프록시 경유, 같은 응답
```

HTTP 수준 검증이며 브라우저 DOM 테스트는 아닙니다. 첫 설치에는 인터넷이 필요합니다.

프런트엔드 결과물: `frontend/dist/`
백엔드 결과물: `backend/build/libs/backend-0.0.1-SNAPSHOT.jar`

## 구성

- `frontend/`: React + TypeScript + Vite, API 연결 상태 화면
- `backend/`: Spring Web MVC, Validation, Actuator, health DTO 및 HTTP 통합 테스트
- `docker-compose.yaml`: Kafka·Redis·RabbitMQ 로컬 컨테이너 구성
- `.env.example`: 인프라 버전·포트·인증 정보 덮어쓰기 예시
- `COMMANDS.md`: 자주 쓰는 명령어 한 줄 요약 모음
- `AGENTS.md`, `CLAUDE.md`: 두 에이전트가 공유하는 프로젝트 지침

비즈니스 기능 추가 시 Controller → Service → Repository로 나누고 DTO를 사용합니다. 현재 health API에는 비즈니스 로직과 DB가 없어 불필요한 계층을 추가하지 않았습니다.

## 인프라 버전 확인 (2026-09-17)

| 항목 | 고정 버전 | 선정 근거 |
| --- | --- | --- |
| Kafka | `apache/kafka:4.3.1` | Apache Kafka는 LTS 지정이 없어 최신 안정 버전 사용 |
| Redis | `redis:8.2.9-alpine` | 8.2가 Redis 8의 LTS 라인, 지원 종료 2030-09-01 |
| RabbitMQ | `rabbitmq:4.2.9-management-alpine` | 4.2가 공식 LTS 시리즈 (커뮤니티 지원 2026-07-31 종료, 상용 지원 2030-06-30까지) |

Docker Hub 태그 목록과 각 프로젝트의 지원 주기 문서를 조회해 선정했습니다. RabbitMQ 4.2는 LTS 시리즈지만 커뮤니티 지원 기간은 이미 끝났습니다. 커뮤니티 지원을 우선한다면 최신 시리즈인 4.3(지원 2026-11-30까지)으로 `.env`의 `RABBITMQ_VERSION`을 바꿔 쓸 수 있습니다. Redis는 오픈소스 배포판 자체에 LTS 표기가 없고, 8.2가 5년 지원이 명시된 라인이라 이를 LTS로 보았습니다.

- [RabbitMQ 릴리스 지원 현황](https://www.rabbitmq.com/release-information)
- [Redis 지원 주기 (endoflife.date)](https://endoflife.date/redis)
- [Apache Kafka 지원 현황 (endoflife.date)](https://endoflife.date/apache-kafka)
- [apache/kafka 이미지](https://hub.docker.com/r/apache/kafka)

## 버전 및 문서 확인 (2026-09-09)

| 항목 | 고정 버전 |
| --- | --- |
| React / React DOM | 19.2.8 |
| Vite | 8.2.2 |
| TypeScript | 6.0.2 |
| Spring Boot | 4.1.1 |
| Gradle Wrapper | 9.7.1 |

이 대화에서 npm 레지스트리와 Spring Initializr 메타데이터를 조회해 안정 버전을 확인했습니다. 공식 `create-vite@9.2.0`의 `react-ts` 템플릿과 Spring Initializr의 Java 21 / Gradle Kotlin DSL 프로젝트를 기반으로 구성했습니다. npm 직접 의존성과 lockfile, Gradle Wrapper·Spring Boot 버전을 고정했습니다. 애플리케이션 자체의 `0.0.1-SNAPSHOT`은 Spring Boot의 안정 버전과 별개입니다.

Context7 MCP는 현재 세션에 노출되지 않았습니다. Context7 공개 React·Vite 문서와 원문을 조회했으며, Spring Boot의 Context7 페이지는 조회 실패하여 공식 자료로 보완했습니다.

- [Context7 React](https://context7.com/websites/react_dev)
- [Context7 Vite](https://context7.com/vitejs/vite)
- [React 공식 초기 구성](https://react.dev/learn/build-a-react-app-from-scratch)
- [Vite 공식 가이드](https://vite.dev/guide/)
- [Spring Initializr](https://start.spring.io/)
- [Spring Boot 공식 시작 가이드](https://spring.io/guides/gs/spring-boot/)
