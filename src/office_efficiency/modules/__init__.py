"""업무 효율 개선 모듈 레지스트리."""

from office_efficiency.modules.base import BaseModule
from office_efficiency.modules.docgen import DocGenModule

# 활성화된 모듈 목록
# 새로운 업무 효율화 모듈을 만들면 이 리스트에 추가하기만 하면 됩니다.
REGISTERED_MODULES: list[BaseModule] = [
    DocGenModule(),
]
