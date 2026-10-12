"""문서 자동 생성 모듈."""

from typing import Any

import typer

from office_efficiency.modules.base import BaseModule
from office_efficiency.modules.docgen.cli import docgen_app


class DocGenModule(BaseModule):
    """서식 기반 사내 문서 자동 생성 모듈."""

    name: str = "doc"
    description: str = "회의록, PPT, 구매사양서, 계약서 자동 생성"

    def register_cli(self, app: typer.Typer) -> None:
        """메인 CLI에 docgen 서브커맨드를 추가합니다."""
        app.add_typer(docgen_app, name=self.name)

    def run(self, **kwargs: Any) -> Any:
        pass
