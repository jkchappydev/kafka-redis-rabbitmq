# 프로젝트 개발 지침

- frontend/: React + TypeScript + Vite. backend/: Spring Boot + Java 21.
- 설치·실행·검증은 각 디렉터리에서 직접 실행한다: `npm ci` / `npm run dev` / `npm run lint` / `npm run build`, `./gradlew classes testClasses` / `bootRun` / `check bootJar`.
- 로컬 인프라(Kafka·Redis·RabbitMQ)는 `docker compose up -d --wait`로 띄운다. 구성은 `docker-compose.yaml` 참고.
- 버전 및 문서 확인 기록은 README.md 참고.
- API는 /api 아래에 배치한다. 비즈니스 기능 추가 시 Controller → Service → Repository와 DTO를 사용한다.
- 공통 사용자 지침을 따르고 프로젝트 변경 후 관련 검증을 수행한다.
