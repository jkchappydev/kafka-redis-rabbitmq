# 프로젝트 개발 지침

- frontend/: React + TypeScript + Vite. backend/: Spring Boot + Java 21.
- 설치: `make setup`, 실행: `make dev`, 검증: `make verify`, HTTP 연동: `make smoke`.
- 버전 및 문서 확인 기록은 README.md 참고.
- API는 /api 아래에 배치한다. 비즈니스 기능 추가 시 Controller → Service → Repository와 DTO를 사용한다.
- 공통 사용자 지침을 따르고 프로젝트 변경 후 관련 검증을 수행한다.
