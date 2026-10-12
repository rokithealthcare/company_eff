"""프로젝트 전역 설정 및 경로 관리 모듈."""

import os
from pathlib import Path

from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 프로젝트 루트 경로 (pyproject.toml이 위치한 곳)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# 템플릿 및 출력 디렉터리 경로
TEMPLATES_DIR = Path(os.getenv("TEMPLATES_DIR", str(PROJECT_ROOT / "templates"))).resolve()
OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", str(PROJECT_ROOT / "output"))).resolve()

# 필수 디렉터리 자동 생성 보장
TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
