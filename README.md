# 사내 업무 효율 개선 자동화 시스템 (Office Efficiency Automation)

본 프로젝트는 사내에서 반복적으로 발생하는 비효율적인 업무를 자동화하고 지속적으로 기능을 확장할 수 있는 **`uv` 기반의 모듈형 Python 프레임워크**입니다.

초기에는 기존 회사 서식에 맞춰 내용을 기반으로 **PPT 발표자료, 회의록, 구매사양서, 계약서** 등의 문서를 자동 생성하는 기능부터 제공하며, 새로운 업무 개선 아이디어가 발굴될 때마다 플러그인 형태로 손쉽게 기능을 추가할 수 있도록 설계되었습니다.

---

## 1. 기술 스택 및 개발 환경

- **패키지 및 가상환경 관리**: [uv](https://github.com/astral-sh/uv) (Astral 고성능 파이썬 도구)
- **런타임 버전**: Python 3.12 (라이브러리 바이너리 휠 호환성 보장)
- **문서 처리 엔진**: `python-docx`, `docxtpl` (Jinja2 기반 서식 채우기), `python-pptx` (발표자료 생성), `openpyxl` (엑셀)
- **CLI & 인터페이스**: `typer`, `rich`
- **데이터 검증**: `pydantic v2`
- **코드 품질 관리**: `ruff` (Linter & Formatter), `pytest`

---

## 2. 빠른 시작 (Quick Start)

### 1) 기본 서식 템플릿 초기화
기본 제공되는 Word 및 PPT 템플릿 파일을 `templates/` 디렉터리에 생성합니다:
```powershell
uv run office-efficiency doc init-templates
```
> **서식 커스터마이징**: 생성된 `templates/meeting/meeting_template.docx`, `templates/contract/contract_template.docx`, `templates/spec/spec_template.docx` 파일을 열어 회사 로고, 워터마크, 폰트 및 스타일을 자유롭게 수정할 수 있습니다. (Jinja2 태그: `{{ title }}`, `{% for item in ... %}` 유지)

### 2) 문서 자동 생성 테스트 (샘플 데이터 모드)
CLI 명령어 뒤에 `--sample` 플래그를 붙여 즉시 생성 결과를 확인할 수 있습니다:

- **회의록 자동 생성**:
  ```powershell
  uv run office-efficiency doc meeting --sample
  ```
- **PPT 발표자료 자동 생성**:
  ```powershell
  uv run office-efficiency doc ppt --sample
  ```
- **구매사양서 자동 생성**:
  ```powershell
  uv run office-efficiency doc spec --sample
  ```
- **계약서 자동 생성**:
  ```powershell
  uv run office-efficiency doc contract --sample
  ```
> 생성된 모든 결과물은 프로젝트 루트의 `output/` 폴더에 자동으로 저장됩니다.

### 3) 사용자 JSON 데이터로 문서 생성하기
실제 업무에서는 데이터 파일(`.json`)을 전달하여 문서를 생성합니다:
```powershell
uv run office-efficiency doc meeting --input my_meeting_data.json
```

---

## 3. 프로젝트 디렉터리 구조

```
회사업무효율개선/
├── .python-version          # Python 3.12 고정
├── pyproject.toml           # 의존성 및 Ruff/Pytest 설정
├── uv.lock                  # 재현 가능한 패키지 잠금 파일
├── .env.example             # 환경변수 템플릿
├── .vscode/settings.json    # IDE 연동 설정
│
├── templates/               # 회사 공식 서식 템플릿 저장소
│   ├── meeting/             # 회의록 서식 (.docx)
│   ├── ppt/                 # 발표자료 템플릿 (.pptx)
│   ├── spec/                # 구매사양서 서식 (.docx)
│   └── contract/            # 계약서 서식 (.docx)
│
├── output/                  # 생성된 결과 문서 저장소 (.gitignore 대상)
│
├── src/
│   └── office_efficiency/
│       ├── config.py        # 프로젝트 전역 경로 및 설정
│       ├── cli.py           # 통합 CLI 진입점
│       ├── core/            # 로깅, 콘솔 유틸리티
│       └── modules/         # 업무 효율화 기능 모듈들 (확장 영역)
│           ├── base.py      # BaseModule 인터페이스 (플러그인 규격)
│           └── docgen/      # 1단계: 서식 기반 문서 자동 생성 모듈
│               ├── cli.py
│               ├── models.py     # Pydantic 데이터 모델
│               └── generators/   # 세부 문서 생성기 (Word, PPT, Spec, Contract)
│
└── tests/                   # 단위 테스트
    └── test_docgen.py
```

---

## 4. 새로운 업무 효율화 기능 확장 방법 (How to Extend)

새로운 업무 자동화 영역(예: 웹 크롤러, 엑셀 통합 취합기, 메신저 알림 등)이 생기면 기존 코드를 수정하지 않고 아래 3단계로 확장할 수 있습니다:

1. **`src/office_efficiency/modules/` 아래에 신규 폴더 생성** (예: `excel_tools/`)
2. **`BaseModule` 상속 구현**:
   ```python
   from office_efficiency.modules.base import BaseModule
   import typer

   class ExcelToolModule(BaseModule):
       name = "excel"
       description = "사내 엑셀 원장 취합 및 결산 자동화"

       def register_cli(self, app: typer.Typer) -> None:
           excel_app = typer.Typer(name=self.name, help=self.description)
           @excel_app.command("merge")
           def merge_files():
               # 취합 로직 구현
               pass
           app.add_typer(excel_app, name=self.name)

       def run(self, **kwargs):
           pass
   ```
3. **`src/office_efficiency/modules/__init__.py`의 `REGISTERED_MODULES`에 인스턴스 등록**:
   ```python
   REGISTERED_MODULES = [
       DocGenModule(),
       ExcelToolModule(),  # 추가
   ]
   ```
   등록 즉시 `uv run office-efficiency modules` 및 `uv run office-efficiency excel merge`로 사용 가능합니다.

---

## 5. 일상 개발 명령어

- **새 라이브러리 추가**: `uv add <패키지명>`
- **코드 검사 및 포맷팅**:
  ```powershell
  uv run ruff check --fix .
  uv run ruff format .
  ```
- **테스트 실행**:
  ```powershell
  uv run pytest
  ```
