## Wanted 파이썬 개발자 [코어강화팀] 과제

### 개발 환경
- Python 3.12.2 + Poetry


### 구현 아키텍쳐
- FastAPI를 사용하여 REST API 구현
- Pydantic을 사용하여 Request, Response 모델 정의
- SQLAlchemy를 사용하여 ORM 구현
- DependencyInjection을 사용하여 의존성 주입
- Service Layer를 사용하여 비즈니스 로직 분리
- Database Repository 방식을 사용하여 테이블별 커스텀 쿼리 관리
- .env 파일로 환경변수 관리(+Pydantic-settings)


### 참고한 자료
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://docs.sqlalchemy.org/en/20/)
- [Dependency Injection](https://python-dependency-injector.ets-labs.org/index.html)


### 구동 방법
- 로컬 구동 시
  - poetry로 가상환경 구성
  - src 디렉토리를 source root로 설정
  - src/config/base.env 파일의 mysql, redis 정보를 수정해야 합니다.
    - Swagger URL: http://localhost:8000/docs
- 혹은 docker compose 로 일괄 구동할 수 있습니다.
  - docker 환경의 설정파일은 src/config/docker.env 파일입니다.
  - Swagger URL: http://localhost:5000/docs 
- [GET] /data_insert 를 통해 초기 DB데이터를 밀어넣습니다.


### 디렉토리 구조
- src
  - main.py: FastAPI app
  - containers.py: DI 컨테이너
  - apps: 기능별 모듈화
    - companies: company API
    - search: 검색 API
    - apps 내 디렉토리 구조
      - dto.py: DTO
      - model.py: DB 모델
      - router.py: API 라우터
      - service.py: 비즈니스 로직
      - repository.py: DB 레포지토리
  - core
    - db.py: DB 모델
    - repository.py: DB 레포지토리 기본 클래스
    - exception.py: 예외 처리
    - date.py: 날짜 유틸
  - config
    - __init__.py: 환경변수 Settings() 구성
    - base.env: 기본 환경변수
    - docker.env: 로컬 도커용 환경변수
- tests
  - conftest.py: pytest 설정용
  - test_senior_app.py: 테스트 파일
- Dockerfile
- docker-compose.yml
- pyproject.toml: 프로젝트 의존성 관련 설정정보
- 전처리.ipynb: 제공받은 .csv 파일을 회사 생성을 위한 json 으로 변환
- company_tag_sample.json: 회사 생성용 json 파일


### 과제 해결 방법
- 사명 검색에서 db 컬럼을 MySQL FULLTEXT 인덱스로 설정하여 검색처리 하였습니다.


### 놓친 부분
- 주어지는 `tag_name` 셋이 하나의 그룹으로 묶이는 부분을 놓쳤습니다.
- 태그 추가/삭제시 언어별로만 처리되어, 그룹 삭제가 수행되지 않습니다.
- improve 브랜치에서 놓친 부분을 보강하려 하였으나, 시간이 부족하여 완성하지 못하였습니다.
