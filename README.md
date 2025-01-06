# Notion Clone Project

## 📌 프로젝트 개요

Notion과 유사한 개인용 지식 관리 시스템으로, NAS 환경에 최적화된 솔루션입니다. 데이터베이스 기능을 중심으로 한 문서 관리와 정보 조직화에 중점을 두었습니다.

### 주요 기능
- 📝 페이지 관리 및 실시간 편집
- 📊 다양한 데이터베이스 뷰 (테이블, 보드, 캘린더, 갤러리)
- 🔄 관계형 데이터베이스와 롤업 기능
- 📊 고급 필터링 및 정렬
- 🔗 공유 및 협업 기능

## 🛠 기술 스택

### Backend
- Python 3.9+
- FastAPI
- SQLAlchemy
- Alembic (마이그레이션)
- MariaDB/MySQL

### Frontend
- HTML5/CSS3
- JavaScript (ES6+)
- Tailwind CSS

### 배포 환경
- Synology NAS (DSM 7.2+)
- Web Station
- Python 3
- MariaDB 10

## 📁 프로젝트 구조
```
notion-clone/
├── backend/
│   ├── app/
│   │   ├── api/           # API 엔드포인트
│   │   ├── core/          # 핵심 설정
│   │   ├── crud/          # 데이터베이스 작업
│   │   ├── models/        # 데이터 모델
│   │   ├── schemas/       # 데이터 검증
│   │   └── services/      # 비즈니스 로직
│   ├── tests/             # 테스트 코드
│   └── alembic/           # DB 마이그레이션
└── frontend/
    ├── static/
    │   ├── css/
    │   ├── js/
    │   └── images/
    └── templates/
        ├── pages/
        ├── databases/
        └── automation/
```

## ⚙️ 설치 및 실행 방법

1. 필수 패키지 설치
```bash
# Python 가상환경 생성
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt
```

2. 데이터베이스 설정
```sql
CREATE DATABASE notion_clone CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'notion_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON notion_clone.* TO 'notion_user'@'localhost';
```

3. 환경 변수 설정
```bash
# .env 파일 생성
cp .env.example .env
# 필요한 설정 수정
```

4. 데이터베이스 마이그레이션
```bash
alembic upgrade head
```

5. 서버 실행
```bash
uvicorn app.main:app --reload
```

## 🔍 주요 기능 설명

### 1. 페이지 관리
- 실시간 자동 저장
- 마크다운 스타일 에디터
- 드래그 앤 드롭 지원
- 계층형 페이지 구조

### 2. 데이터베이스 기능
- 다양한 필드 타입 지원
  - 텍스트, 숫자, 날짜
  - 선택, 다중 선택
  - 관계형, 롤업
  - 수식
- 뷰 타입
  - 테이블 뷰
  - 보드 뷰 (칸반)
  - 캘린더 뷰
  - 갤러리 뷰
  - 리스트 뷰
- 고급 기능
  - 필터링
  - 정렬
  - 그룹화
  - 계산 및 집계

### 3. 공유 및 협업
- 뷰 단위 공유
- 만료 시간 설정
- 권한 관리
- 데이터 내보내기

## 🔧 개발 과정

### Phase 1: 기본 기능 구현
- [x] 프로젝트 구조 설계
- [x] 데이터베이스 모델 설계
- [x] 기본 페이지 편집 기능
- [x] 테이블 뷰 구현

### Phase 2: 고급 기능 구현
- [x] 추가 뷰 타입 구현
- [x] 관계형 데이터베이스 기능
- [x] 롤업 및 수식 기능
- [x] 필터링 및 정렬 시스템

### Phase 3: 최적화 및 추가 기능
- [x] 성능 최적화
- [x] 공유 기능 구현
- [x] 데이터 내보내기
- [x] UI/UX 개선

## 🔒 보안 기능
- IP 기반 접근 제어
- 암호화된 데이터 저장
- 안전한 공유 링크 시스템

## 📈 성능 최적화
- 데이터베이스 인덱싱
- 캐싱 시스템 구현
- 지연 로딩
- 이미지 최적화

## 🔄 백업 및 복구
- 자동 백업 시스템
- 증분 백업 지원
- 간편한 복구 프로세스

## 🔍 모니터링
- 시스템 리소스 모니터링
- 에러 로깅
- 성능 메트릭 수집

## 📋 테스트
```bash
# 백엔드 테스트 실행
cd backend
pytest

# 프론트엔드 테스트 실행
cd frontend
npm test
```

## 🚀 배포
```bash
# 배포 스크립트 실행
./deploy.sh
```

## 📝 라이선스
MIT License

## 👥 기여
1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request