# Notion Clone Project Directory Structure

```plaintext
notion-clone/                          # 프로젝트 루트 디렉토리
│
├── backend/                           # 백엔드 애플리케이션
│   ├── app/                          # 메인 애플리케이션 코드
│   │   ├── api/                     # API 관련 코드
│   │   │   └── v1/                 # API 버전 1
│   │   │       ├── endpoints/      # API 엔드포인트
│   │   │       │   ├── __init__.py
│   │   │       │   ├── auth.py       # 인증 관련 엔드포인트
│   │   │       │   ├── databases.py  # 데이터베이스 관련 엔드포인트
│   │   │       │   ├── pages.py      # 페이지 관련 엔드포인트
│   │   │       │   ├── share.py      # 공유 관련 엔드포인트
│   │   │       │   └── views.py      # 뷰 관련 엔드포인트
│   │   │       ├── __init__.py
│   │   │       └── api.py          # API 라우터 설정
│   │   │
│   │   ├── core/                    # 핵심 설정 및 유틸리티
│   │   │   ├── __init__.py
│   │   │   ├── config.py            # 환경 설정
│   │   │   ├── security.py          # 보안 관련 유틸리티
│   │   │   └── dependencies.py      # 의존성 주입
│   │   │
│   │   ├── crud/                    # 데이터베이스 CRUD 작업
│   │   │   ├── __init__.py
│   │   │   ├── base.py              # 기본 CRUD 작업
│   │   │   ├── database.py          # 데이터베이스 CRUD
│   │   │   ├── page.py              # 페이지 CRUD
│   │   │   └── share.py             # 공유 CRUD
│   │   │
│   │   ├── db/                      # 데이터베이스 설정
│   │   │   ├── __init__.py
│   │   │   ├── base.py              # 기본 DB 설정
│   │   │   └── session.py           # DB 세션 관리
│   │   │
│   │   ├── models/                  # SQLAlchemy 모델
│   │   │   ├── __init__.py
│   │   │   ├── base.py              # 기본 모델
│   │   │   ├── database.py          # 데이터베이스 모델
│   │   │   ├── page.py              # 페이지 모델
│   │   │   └── share.py             # 공유 모델
│   │   │
│   │   ├── schemas/                 # Pydantic 스키마
│   │   │   ├── __init__.py
│   │   │   ├── database.py          # 데이터베이스 스키마
│   │   │   ├── page.py              # 페이지 스키마
│   │   │   └── share.py             # 공유 스키마
│   │   │
│   │   ├── services/                # 비즈니스 로직
│   │   │   ├── __init__.py
│   │   │   ├── database_compute.py   # 데이터베이스 계산
│   │   │   ├── database_filter.py    # 필터링 로직
│   │   │   ├── database_formula.py   # 수식 처리
│   │   │   ├── database_rollup.py    # 롤업 처리
│   │   │   └── database_sort.py      # 정렬 로직
│   │   │
│   │   └── main.py                  # 애플리케이션 진입점
│   │
│   ├── tests/                       # 테스트 코드
│   │   ├── api/                     # API 테스트
│   │   │   ├── __init__.py
│   │   │   ├── test_database.py
│   │   │   ├── test_pages.py
│   │   │   └── test_views.py
│   │   ├── services/                # 서비스 테스트
│   │   │   ├── __init__.py
│   │   │   ├── test_formula.py
│   │   │   └── test_rollup.py
│   │   ├── __init__.py
│   │   ├── conftest.py              # pytest 설정
│   │   └── utils.py                 # 테스트 유틸리티
│   │
│   ├── alembic/                     # 데이터베이스 마이그레이션
│   │   ├── versions/                # 마이그레이션 파일들
│   │   │   ├── 001_create_pages_table.py
│   │   │   └── 002_create_database_tables.py
│   │   ├── env.py                   # Alembic 환경 설정
│   │   └── alembic.ini             # Alembic 설정 파일
│   │
│   ├── requirements.txt            # Python 패키지 의존성
│   └── .env                        # 환경 변수
│
├── frontend/                        # 프론트엔드
│   ├── static/                     # 정적 파일
│   │   ├── css/                    # 스타일시트
│   │   │   ├── main.css            # 메인 스타일
│   │   │   └── style.css           # 추가 스타일
│   │   │
│   │   ├── js/                     # JavaScript 파일
│   │   │   ├── main.js             # 메인 스크립트
│   │   │   ├── editor.js           # 에디터 기능
│   │   │   ├── database.js         # 데이터베이스 기능
│   │   │   ├── database-views.js    # 데이터베이스 뷰
│   │   │   ├── database-filters.js  # 필터링 기능
│   │   │   ├── database-sorting.js  # 정렬 기능
│   │   │   ├── view-sharing.js      # 공유 기능
│   │   │   ├── property-types/      # 속성 타입별 구현
│   │   │   │   ├── formula.js       # 수식 필드
│   │   │   │   └── rollup.js        # 롤업 필드
│   │   │   └── shared-view.js       # 공유 뷰
│   │   │
│   │   └── images/                 # 이미지 파일
│   │
│   ├── templates/                  # HTML 템플릿
│   │   ├── base.html               # 기본 템플릿
│   │   ├── shared.html             # 공유 페이지 템플릿
│   │   ├── pages/                  # 페이지 관련 템플릿
│   │   │   ├── index.html          # 메인 페이지
│   │   │   └── editor.html         # 에디터 페이지
│   │   │
│   │   ├── databases/              # 데이터베이스 관련 템플릿
│   │   │   ├── index.html          # 데이터베이스 목록
│   │   │   ├── view.html           # 데이터베이스 뷰
│   │   │   ├── new.html            # 새 데이터베이스
│   │   │   └── property_types/     # 속성 타입별 템플릿
│   │   │       ├── formula.html     # 수식 필드
│   │   │       └── rollup.html      # 롤업 필드
│   │   │
│   │   └── automation/             # 자동화 관련 템플릿
│   │       ├── index.html          # 자동화 목록
│   │       ├── editor.html         # 자동화 편집
│   │       └── logs.html           # 자동화 로그
│   │
│   ├── tests/                      # 프론트엔드 테스트
│   │   ├── test_editor.js
│   │   └── test_database.js
│   │
│   └── package.json               # NPM 패키지 설정
│
├── deploy.sh                       # 배포 스크립트
├── notion-clone.conf              # Supervisor 설정
├── nginx.conf                     # Nginx 설정
├── requirements.txt               # 프로젝트 전체 의존성
├── README.md                      # 프로젝트 문서
└── directory_structure.md         # 현재 파일
```

## 주요 디렉토리 및 파일 설명

### Backend
- `app/`: 메인 애플리케이션 코드
  - `api/`: API 엔드포인트 및 라우팅
  - `core/`: 핵심 설정 및 유틸리티
  - `crud/`: 데이터베이스 CRUD 작업
  - `models/`: 데이터베이스 모델
  - `schemas/`: 데이터 검증 스키마
  - `services/`: 비즈니스 로직

### Frontend
- `static/`: 정적 파일 (CSS, JavaScript, 이미지)
- `templates/`: HTML 템플릿
  - `pages/`: 페이지 관련 템플릿
  - `databases/`: 데이터베이스 관련 템플릿
  - `automation/`: 자동화 관련 템플릿

### 설정 파일
- `deploy.sh`: 배포 스크립트
- `notion-clone.conf`: Supervisor 설정
- `nginx.conf`: Nginx 설정
- `requirements.txt`: Python 패키지 의존성
- `.env`: 환경 변수

## 주의사항
- 모든 Python 파일에는 `__init__.py`가 포함되어 있어야 합니다.
- 환경 변수는 `.env` 파일에서 관리됩니다.
- 정적 파일은 `frontend/static/` 디렉토리에 위치해야 합니다.