"""업무 효율 개선 모듈의 기본 추상 인터페이스.

향후 새로운 업무 유형(웹 스크래핑, 결재 연동, 데이터 정제 등)을 추가할 때
BaseModule을 상속받아 일관된 구조로 확장할 수 있습니다.
"""

from abc import ABC, abstractmethod
from typing import Any

import typer


class BaseModule(ABC):
    """업무 효율화 기능 모듈의 기본 클래스."""

    name: str = "base"
    description: str = "기본 모듈 설명"

    @abstractmethod
    def register_cli(self, app: typer.Typer) -> None:
        """메인 CLI 앱에 모듈별 명령어를 등록합니다."""
        pass

    @abstractmethod
    def run(self, **kwargs: Any) -> Any:
        """모듈의 핵심 비즈니스 로직을 실행합니다."""
        pass
