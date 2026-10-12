"""문서 자동 생성에 사용되는 Pydantic 데이터 모델 정의."""

from pydantic import BaseModel, Field


# 1. 회의록 데이터 모델
class ActionItem(BaseModel):
    task: str = Field(..., description="수행 과제")
    assignee: str = Field(..., description="담당자")
    due_date: str = Field(..., description="완료 목표일")


class MeetingData(BaseModel):
    title: str = Field("주간 업무 회의", description="회의 제목")
    date: str = Field(..., description="회의 일시 (예: 2026-10-12)")
    location: str = Field("대회의실 / 온라인", description="회의 장소")
    attendees: list[str] = Field(default_factory=list, description="참석자 명단")
    agenda: list[str] = Field(default_factory=list, description="회의 안건")
    discussions: list[str] = Field(default_factory=list, description="주요 논의 내용")
    decisions: list[str] = Field(default_factory=list, description="결정 사항")
    action_items: list[ActionItem] = Field(default_factory=list, description="향후 실행 과제")


# 2. PPT 발표자료 데이터 모델
class SlideContent(BaseModel):
    title: str = Field(..., description="슬라이드 제목")
    points: list[str] = Field(default_factory=list, description="핵심 내용 불릿포인트")
    notes: str | None = Field(None, description="발표자 노트")


class PresentationData(BaseModel):
    title: str = Field(..., description="발표 제목")
    subtitle: str = Field("", description="부제목")
    presenter: str = Field("", description="발표자 / 소속 부서")
    date: str = Field("", description="발표 날짜")
    slides: list[SlideContent] = Field(default_factory=list, description="슬라이드 목록")


# 3. 구매사양서 데이터 모델
class PurchaseItem(BaseModel):
    item_no: int = Field(1, description="순번")
    name: str = Field(..., description="품명")
    spec: str = Field(..., description="규격 및 세부 사양")
    quantity: int = Field(1, description="수량")
    unit: str = Field("EA", description="단위")
    estimated_price: int | None = Field(0, description="예상 단가")
    remarks: str | None = Field("", description="비고")


class PurchaseSpecData(BaseModel):
    doc_no: str = Field(..., description="문서 번호")
    title: str = Field(..., description="구매 건명")
    department: str = Field(..., description="요청 부서")
    requester: str = Field(..., description="요청자")
    request_date: str = Field(..., description="요청 일자")
    purpose: str = Field(..., description="구매 목적 및 필요성")
    delivery_date: str = Field(..., description="희망 납기일")
    delivery_place: str = Field("본사 전산실", description="납품 장소")
    items: list[PurchaseItem] = Field(default_factory=list, description="구매 품목 리스트")
    special_requirements: list[str] = Field(default_factory=list, description="특기 및 검수 조건")


# 4. 계약서 데이터 모델
class PartyInfo(BaseModel):
    company_name: str = Field(..., description="회사명/상호")
    representative: str = Field(..., description="대표자명")
    business_no: str = Field(..., description="사업자등록번호")
    address: str = Field(..., description="주소")


class ContractData(BaseModel):
    title: str = Field("표준 업무 위탁 계약서", description="계약명")
    contract_no: str = Field(..., description="계약 번호")
    contract_date: str = Field(..., description="계약 체결일")
    party_a: PartyInfo = Field(..., description="갑 정보")
    party_b: PartyInfo = Field(..., description="을 정보")
    purpose: str = Field(..., description="계약 목적")
    total_amount: str = Field(..., description="총 계약 금액 (예: 일금 일천만원정 (10,000,000원))")
    payment_terms: str = Field("계약금 30%, 잔금 검수 후 70%", description="대금 지급 조건")
    start_date: str = Field(..., description="계약 시작일")
    end_date: str = Field(..., description="계약 만료일")
    articles: list[str] = Field(default_factory=list, description="추가 특약 조항")
