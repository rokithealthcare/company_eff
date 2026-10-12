"""터미널 및 파일 출력을 위한 Rich 기반 로거 설정."""

import logging
import sys

from rich.console import Console
from rich.logging import RichHandler

# Windows cp949 환경에서도 깨짐 및 인코딩 오류가 없도록 표준 출력 스트림 설정 보정
if sys.platform == "win32":
    try:
        if sys.stdout and hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
        if sys.stderr and hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

console = Console(safe_box=True)


def get_logger(name: str = "office_efficiency") -> logging.Logger:
    """Rich 포맷이 적용된 로거 인스턴스를 반환합니다."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = RichHandler(
            console=console,
            rich_tracebacks=True,
            show_time=True,
            show_level=True,
            show_path=False,
        )
        formatter = logging.Formatter("%(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger
