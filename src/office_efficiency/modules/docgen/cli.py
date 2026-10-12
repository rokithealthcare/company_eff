"""문서 자동 생성 모듈 CLI 명령어 정의."""

from pathlib import Path

import typer

from office_efficiency.config import TEMPLATES_DIR
from office_efficiency.core.logger import console, get_logger
from office_efficiency.modules.docgen.generators import (
    generate_contract,
    generate_meeting_minutes,
    generate_presentation,
    generate_purchase_spec,
)
from office_efficiency.modules.docgen.generators.contract_generator import (
    create_default_contract_template,
)
from office_efficiency.modules.docgen.generators.meeting_generator import (
    create_default_meeting_template,
)
from office_efficiency.modules.docgen.generators.spec_generator import create_default_spec_template
from office_efficiency.modules.docgen.models import (
    ActionItem,
    ContractData,
    MeetingData,
    PartyInfo,
    PresentationData,
    PurchaseItem,
    PurchaseSpecData,
    SlideContent,
)

docgen_app = typer.Typer(
    name="doc",
    help="서식 기반 사내 문서 자동 생성 (회의록, PPT, 구매사양서, 계약서)",
)
logger = get_logger("cli.docgen")


@docgen_app.command("init-templates")
def init_templates() -> None:
    """기본 서식 템플릿(Word/PPT)을 templates 디렉터리에 일괄 생성합니다."""
    console.print("[bold cyan]기본 문서 서식 템플릿을 생성합니다...[/bold cyan]")

    meeting_tpl = TEMPLATES_DIR / "meeting" / "meeting_template.docx"
    spec_tpl = TEMPLATES_DIR / "spec" / "spec_template.docx"
    contract_tpl = TEMPLATES_DIR / "contract" / "contract_template.docx"

    create_default_meeting_template(meeting_tpl)
    create_default_spec_template(spec_tpl)
    create_default_contract_template(contract_tpl)

    console.print("[bold green][완료] 모든 기본 템플릿이 성공적으로 준비되었습니다![/bold green]")
    console.print(f"템플릿 경로: [yellow]{TEMPLATES_DIR}[/yellow]")
    console.print(
        "이 템플릿 파일들을 열어 회사 고유의 로고, 폰트, 색상 및 표 서식을 편집할 수 있습니다."
    )


@docgen_app.command("meeting")
def create_meeting(
    input_file: Path | None = typer.Option(
        None, "--input", "-i", help="회의록 내용이 작성된 JSON 파일 경로"
    ),
    sample: bool = typer.Option(False, "--sample", "-s", help="샘플 데이터로 즉시 생성 테스트"),
) -> None:
    """회의록(.docx) 문서를 자동 생성합니다."""
    if input_file and input_file.exists():
        with open(input_file, encoding="utf-8") as f:
            data = MeetingData.model_validate_json(f.read())
    elif sample:
        data = MeetingData(
            title="2026년 4분기 업무 효율화 프로젝트 킥오프",
            date="2026-10-12",
            location="본관 5층 중회의실",
            attendees=["김철수 팀장", "이영희 과장", "박지민 대리"],
            agenda=[
                "uv 기반 파이썬 개발 환경 표준화 현황 공유",
                "사내 문서 자동 생성 시스템 요구사항 검토",
                "1차 배포 일정 및 역할 분담",
            ],
            discussions=[
                "기존 수작업으로 작성하던 회의록/구매사양서/계약서 서식을 템플릿화하기로 합의함",
                "차후 기능 확장을 고려하여 플러그인 모듈 구조를 채택하기로 결정함",
            ],
            decisions=[
                "10월 중 핵심 문서 4종 자동화 1차 검증 완료",
                "팀 내 공용 템플릿 디렉터리 구축",
            ],
            action_items=[
                ActionItem(
                    task="사내 표준 계약서 서식 파일 등록",
                    assignee="이영희 과장",
                    due_date="2026-10-16",
                ),
                ActionItem(
                    task="구매사양서 자동화 테스트 데이터셋 작성",
                    assignee="박지민 대리",
                    due_date="2026-10-18",
                ),
            ],
        )
    else:
        console.print("[red]오류: --input <JSON파일> 또는 --sample 옵션을 지정해야 합니다.[/red]")
        raise typer.Exit(code=1)

    result_path = generate_meeting_minutes(data)
    console.print(f"[bold green][완료] 회의록 생성 완료:[/bold green] {result_path}")


@docgen_app.command("ppt")
def create_ppt(
    input_file: Path | None = typer.Option(
        None, "--input", "-i", help="발표 내용이 작성된 JSON 파일 경로"
    ),
    sample: bool = typer.Option(False, "--sample", "-s", help="샘플 데이터로 즉시 생성 테스트"),
) -> None:
    """발표자료 PPT(.pptx)를 자동 생성합니다."""
    if input_file and input_file.exists():
        with open(input_file, encoding="utf-8") as f:
            data = PresentationData.model_validate_json(f.read())
    elif sample:
        data = PresentationData(
            title="업무 효율 개선 자동화 추진 계획",
            subtitle="반복 업무 제거 및 서식 기반 문서 자동화",
            presenter="업무혁신TF",
            date="2026-10-12",
            slides=[
                SlideContent(
                    title="추진 배경 및 목적",
                    points=[
                        "매주/매월 반복되는 양식 기반 문서 작성의 시간 낭비 해결",
                        "서식 오작성 방지 및 데이터 일관성 확보",
                        "향후 추가적인 사내 업무 자동화의 기반 프레임워크 구축",
                    ],
                    notes="도입 효과를 중심으로 강조하여 설명할 것",
                ),
                SlideContent(
                    title="1단계 적용 대상 문서",
                    points=[
                        "PPT 발표자료: 보고용 골격 슬라이드 자동 구성",
                        "회의록: 참석자/안건/Action Items 서식 자동화",
                        "구매사양서: 품목 스펙 테이블 및 검수 조건 자동 렌더링",
                        "계약서: 갑/을 정보 및 계약 조항 자동 매핑",
                    ],
                ),
                SlideContent(
                    title="향후 확장 로드맵",
                    points=[
                        "2단계: 사내 웹/시스템 연동 및 데이터 크롤링",
                        "3단계: 결재 연동 및 메신저(Slack/Teams) 알림",
                        "4단계: 생성형 AI 기반 초안 작성 어시스턴트 접목",
                    ],
                ),
            ],
        )
    else:
        console.print("[red]오류: --input <JSON파일> 또는 --sample 옵션을 지정해야 합니다.[/red]")
        raise typer.Exit(code=1)

    result_path = generate_presentation(data)
    console.print(f"[bold green][완료] PPT 발표자료 생성 완료:[/bold green] {result_path}")


@docgen_app.command("spec")
def create_spec(
    input_file: Path | None = typer.Option(
        None, "--input", "-i", help="구매사양서 내용이 작성된 JSON 파일 경로"
    ),
    sample: bool = typer.Option(False, "--sample", "-s", help="샘플 데이터로 즉시 생성 테스트"),
) -> None:
    """구매사양서(.docx) 문서를 자동 생성합니다."""
    if input_file and input_file.exists():
        with open(input_file, encoding="utf-8") as f:
            data = PurchaseSpecData.model_validate_json(f.read())
    elif sample:
        data = PurchaseSpecData(
            doc_no="SPEC-2026-0042",
            title="개발팀 개발용 워크스테이션 및 모니터 구매",
            department="디지털혁신팀",
            requester="홍길동 수석",
            request_date="2026-10-12",
            purpose="신규 프로젝트 수행을 위한 고성능 개발 환경 구축",
            delivery_date="2026-11-05",
            delivery_place="본사 IT연구소 3층",
            items=[
                PurchaseItem(
                    item_no=1,
                    name="AI 개발용 고성능 워크스테이션",
                    spec="CPU: i9 / RAM: 64GB / GPU: RTX 4080 / SSD: 2TB",
                    quantity=3,
                    unit="대",
                    remarks="정품 윈도우 OS 포함",
                ),
                PurchaseItem(
                    item_no=2,
                    name="4K 32인치 듀얼 모니터",
                    spec="IPS 패널 / UHD 3840x2160 / USB-C PD 90W 지원",
                    quantity=6,
                    unit="대",
                    remarks="모니터 암 거치 가능 규격",
                ),
            ],
            special_requirements=[
                "납품 후 현장 설치 및 정상 부팅 테스트를 완료해야 함.",
                "무상 유지보수 보증기간은 납품 검수일로부터 2년으로 함.",
            ],
        )
    else:
        console.print("[red]오류: --input <JSON파일> 또는 --sample 옵션을 지정해야 합니다.[/red]")
        raise typer.Exit(code=1)

    result_path = generate_purchase_spec(data)
    console.print(f"[bold green][완료] 구매사양서 생성 완료:[/bold green] {result_path}")


@docgen_app.command("contract")
def create_contract(
    input_file: Path | None = typer.Option(
        None, "--input", "-i", help="계약서 내용이 작성된 JSON 파일 경로"
    ),
    sample: bool = typer.Option(False, "--sample", "-s", help="샘플 데이터로 즉시 생성 테스트"),
) -> None:
    """표준 계약서(.docx) 문서를 자동 생성합니다."""
    if input_file and input_file.exists():
        with open(input_file, encoding="utf-8") as f:
            data = ContractData.model_validate_json(f.read())
    elif sample:
        data = ContractData(
            title="사내 업무 효율화 솔루션 개발 용역 계약서",
            contract_no="CTR-2026-1001",
            contract_date="2026-10-12",
            party_a=PartyInfo(
                company_name="(주)알파비즈니스",
                representative="김대표",
                business_no="123-45-67890",
                address="서울특별시 강남구 테헤란로 123 알파빌딩 8층",
            ),
            party_b=PartyInfo(
                company_name="(주)스마트소프트",
                representative="이개발",
                business_no="987-65-43210",
                address="경기도 성남시 분당구 판교역로 456 판교타워 5층",
            ),
            purpose="사내 수작업 문서 작성 및 반복 업무 자동화 시스템 개발 용역",
            total_amount="일금 삼천만원정 (₩30,000,000, 부가세 별도)",
            payment_terms="착수금 30%, 중간 검수 30%, 최종 검수 완료 후 40%",
            start_date="2026-10-15",
            end_date="2026-12-31",
            articles=[
                "을은 계약 기간 내 계약 목적물을 성실히 개발하여 납품하여야 한다.",
                "결과물에 대한 지식재산권은 잔금 지급 완료 시 갑에게 귀속된다.",
            ],
        )
    else:
        console.print("[red]오류: --input <JSON파일> 또는 --sample 옵션을 지정해야 합니다.[/red]")
        raise typer.Exit(code=1)

    result_path = generate_contract(data)
    console.print(f"[bold green][완료] 계약서 생성 완료:[/bold green] {result_path}")
