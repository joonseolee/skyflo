# MCP 테스트 가이드

이 디렉토리는 MCP (Model Context Protocol) 서버의 테스트 코드를 포함합니다.

## 테스트 구조

```
tests/
├── __init__.py                    # 테스트 패키지 초기화
├── conftest.py                    # pytest 설정 및 픽스처
├── test_config_server.py          # MCP 서버 설정 테스트
├── test_main.py                   # 메인 모듈 테스트
├── test_tools_kubectl_simple.py   # kubectl 도구 테스트
├── test_utils_commands.py         # 명령어 실행 유틸리티 테스트
├── test_utils_types.py            # 타입 정의 테스트
└── README.md                      # 이 파일
```

## 테스트 실행

### 모든 테스트 실행
```bash
cd /Users/nhn/Documents/private-repository/skyflo/mcp
source test_env/bin/activate
python -m pytest tests/ -v
```

### 특정 테스트 파일 실행
```bash
python -m pytest tests/test_utils_commands.py -v
```

### 커버리지와 함께 실행
```bash
python -m pytest tests/ --cov=. --cov-report=html --cov-report=term
```

### 특정 테스트 클래스 실행
```bash
python -m pytest tests/test_utils_commands.py::TestRunCommand -v
```

### 특정 테스트 함수 실행
```bash
python -m pytest tests/test_utils_commands.py::TestRunCommand::test_run_command_success -v
```

## 테스트 종류

### 1. 유틸리티 테스트 (`test_utils_*.py`)
- **commands.py**: 비동기 명령어 실행 함수 테스트
- **types.py**: ToolOutput 타입 정의 테스트

### 2. 메인 모듈 테스트 (`test_main.py`)
- CLI 인자 파싱 테스트
- SSE/HTTP 전송 방식 테스트
- 서버 설정 테스트

### 3. 설정 테스트 (`test_config_server.py`)
- MCP 서버 인스턴스 생성 테스트
- 의존성 설정 테스트
- 도구 모듈 임포트 테스트

### 4. kubectl 도구 테스트 (`test_tools_kubectl_simple.py`)
- kubectl 명령어 실행 함수 테스트
- 명령어 인자 빌딩 로직 테스트
- 다양한 kubectl 명령어 조합 테스트

## 테스트 작성 가이드

### 1. 테스트 파일 명명 규칙
- `test_*.py` 형식으로 명명
- 테스트할 모듈명을 포함

### 2. 테스트 클래스 명명 규칙
- `Test*` 형식으로 명명
- 테스트할 기능을 명확히 표현

### 3. 테스트 함수 명명 규칙
- `test_*` 형식으로 명명
- 테스트 시나리오를 명확히 표현

### 4. 픽스처 사용
- `conftest.py`에 공통 픽스처 정의
- `@pytest.fixture` 데코레이터 사용

### 5. 모킹 사용
- `unittest.mock.patch` 사용
- 외부 의존성 모킹
- 비동기 함수는 `AsyncMock` 사용

## 현재 테스트 커버리지

```
Name                Stmts   Miss Branch BrPart  Cover
-----------------------------------------------------
config/server.py        6      0      0      0   100%
main.py                20      0      2      0   100%
tools/__init__.py       0      0      0      0   100%
tools/argo.py         105     73     44      0    21%
tools/helm.py         123     85     46      0    22%
tools/jenkins.py      227    184     46      0    16%
tools/kubectl.py      127     59     46      0    49%
utils/commands.py      22      0      6      0   100%
utils/types.py          4      0      0      0   100%
-----------------------------------------------------
TOTAL                 634    401    190      0    31%
```

## 향후 개선 사항

1. **도구 모듈 테스트 확장**
   - `tools/argo.py` 테스트 추가
   - `tools/helm.py` 테스트 추가
   - `tools/jenkins.py` 테스트 추가

2. **통합 테스트 추가**
   - 전체 워크플로우 테스트
   - 실제 kubectl 명령어 실행 테스트

3. **성능 테스트 추가**
   - 대용량 데이터 처리 테스트
   - 동시 요청 처리 테스트

4. **에러 처리 테스트 강화**
   - 네트워크 오류 시나리오
   - 잘못된 입력 처리

## 의존성

- `pytest`: 테스트 프레임워크
- `pytest-mock`: 모킹 지원
- `pytest-cov`: 커버리지 측정
- `pytest-asyncio`: 비동기 테스트 지원

## 참고사항

- 모든 테스트는 가상환경에서 실행해야 합니다
- kubectl 명령어는 실제 클러스터 없이도 테스트할 수 있도록 모킹되어 있습니다
- 테스트 실행 시 경고 메시지가 나타날 수 있지만 테스트 자체에는 영향을 주지 않습니다
