"""회사 업무 효율 개선 통합 CLI 진입점."""

import typer
from rich.table import Table

from office_efficiency.core.logger import console
from office_efficiency.modules import REGISTERED_MODULES

app = typer.Typer(
    name="office-efficiency",
    help="사내 업무 효율 개선 및 문서/작업 자동화 통합 프레임워크",
    add_completion=False,
)

# 등록된 모든 모듈의 CLI 명령어 동적 바인딩
for module in REGISTERED_MODULES:
    module.register_cli(app)


@app.command("modules")
def list_modules() -> None:
    """현재 시스템에 등록된 업무 효율 개선 모듈 목록을 조회합니다."""
    table = Table(title="[bold blue]등록된 업무 효율화 모듈 목록[/bold blue]")
    table.add_column("명령어", style="cyan", no_wrap=True)
    table.add_column("설명", style="magenta")
    table.add_column("클래스", style="dim")

    for mod in REGISTERED_MODULES:
        table.add_row(mod.name, mod.description, mod.__class__.__name__)

    console.print(table)


def main() -> None:
    """CLI 애플리케이션 실행 메인 함수."""
    app()


if __name__ == "__main__":
    main()
