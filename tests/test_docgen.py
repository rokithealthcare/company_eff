"""문서 자동 생성 기능 단위 테스트."""

from pathlib import Path

from office_efficiency.modules.docgen.generators import (
    generate_contract,
    generate_meeting_minutes,
    generate_presentation,
    generate_purchase_spec,
)
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


def test_generate_meeting_minutes(tmp_path: Path) -> None:
    data = MeetingData(
        title="단위 테스트 회의",
        date="2026-10-12",
        location="테스트실",
        attendees=["테스터1", "테스터2"],
        agenda=["안건 1"],
        discussions=["논의 내용 1"],
        decisions=["결정 사항 1"],
        action_items=[ActionItem(task="과제1", assignee="테스터1", due_date="2026-10-15")],
    )
    output_file = generate_meeting_minutes(data, output_filename="test_meeting.docx")
    assert output_file.exists()
    assert output_file.stat().st_size > 0


def test_generate_presentation(tmp_path: Path) -> None:
    data = PresentationData(
        title="테스트 발표",
        subtitle="테스트 부제",
        presenter="테스터",
        date="2026-10-12",
        slides=[
            SlideContent(title="슬라이드 1", points=["항목 1", "항목 2"]),
        ],
    )
    output_file = generate_presentation(data, output_filename="test_pres.pptx")
    assert output_file.exists()
    assert output_file.stat().st_size > 0


def test_generate_purchase_spec(tmp_path: Path) -> None:
    data = PurchaseSpecData(
        doc_no="TEST-001",
        title="테스트 구매",
        department="품질관리팀",
        requester="테스터",
        request_date="2026-10-12",
        purpose="테스트 목적",
        delivery_date="2026-10-20",
        items=[PurchaseItem(item_no=1, name="테스트장비", spec="Spec-A", quantity=1)],
        special_requirements=["조건 1"],
    )
    output_file = generate_purchase_spec(data, output_filename="test_spec.docx")
    assert output_file.exists()
    assert output_file.stat().st_size > 0


def test_generate_contract(tmp_path: Path) -> None:
    data = ContractData(
        title="테스트 계약서",
        contract_no="TEST-CTR-01",
        contract_date="2026-10-12",
        party_a=PartyInfo(
            company_name="갑사",
            representative="김대표",
            business_no="111-11-11111",
            address="서울",
        ),
        party_b=PartyInfo(
            company_name="을사",
            representative="박대표",
            business_no="222-22-22222",
            address="경기",
        ),
        purpose="계약 목적 테스트",
        total_amount="1,000,000원",
        start_date="2026-10-12",
        end_date="2026-12-31",
    )
    output_file = generate_contract(data, output_filename="test_contract.docx")
    assert output_file.exists()
    assert output_file.stat().st_size > 0
