# React + Spring Boot 기본 프로젝트

React 화면에서 Spring Boot의 `/api/health`에 연결하는 최소 프로젝트입니다.

## 개발 환경

- Node.js 24 LTS, npm 11 (`nvm use`)
- JDK 21 LTS (`JAVA_HOME`도 JDK 21로 설정)
- Python 3.10 이상, Make, macOS 또는 Linux
- Gradle은 저장소의 Wrapper 사용, 별도 설치 불필요

## 시작

```sh
make doctor   # Node·Java 확인
make setup    # 잠금 파일로 npm 설치, Java 의존성 및 테스트 코드 컴파일
make dev      # 두 개발 서버 실행, Ctrl+C로 함께 종료
```

화면: http://localhost:5173
백엔드: http://localhost:8080/api/health
응답: `{"status":"UP"}`

Vite가 `/api` 요청을 8080 포트로 전달합니다. 서버 시작 전에 화면을 열었다면 백엔드 준비 후 새로고침하세요. 5173·8080 포트는 비어 있어야 합니다. 개발 프록시는 프로덕션 빌드에 포함되지 않으므로 배포 시 동일 경로의 reverse proxy가 필요합니다.

## 검증

```sh
make verify   # Oxlint, TypeScript, Vite 빌드, Spring 테스트 및 실행 JAR 생성
make smoke    # 서버 임시 실행 → 직접 API·Vite 프록시·HTML 응답 확인 → 서버 종료
```

`smoke`는 HTTP 수준 검증이며 브라우저 DOM 테스트는 아닙니다. Gradle·npm 캐시는 `.cache/`에 저장합니다. 첫 설치에는 인터넷이 필요합니다.

프런트엔드 결과물: `frontend/dist/`
백엔드 결과물: `backend/build/libs/backend-0.0.1-SNAPSHOT.jar`

## 구성

- `frontend/`: React + TypeScript + Vite, API 연결 상태 화면
- `backend/`: Spring Web MVC, Validation, Actuator, health DTO 및 HTTP 통합 테스트
- `scripts/harness.py`: 설치·실행·검증과 프로세스 정리
- `AGENTS.md`, `CLAUDE.md`: 두 에이전트가 공유하는 프로젝트 지침

비즈니스 기능 추가 시 Controller → Service → Repository로 나누고 DTO를 사용합니다. 현재 health API에는 비즈니스 로직과 DB가 없어 불필요한 계층을 추가하지 않았습니다.

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
