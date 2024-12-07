from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Extra
from pydantic.alias_generators import to_camel


class DefaultModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,  # 필드명을 camelCase로 자동 변환
        populate_by_name=True,
        frozen=True,  # 모델 인스턴스를 불변(immutable)으로 설정
        extra=Extra.allow  # forbid: 정의되지 않은 추가 필드를 허용하지 않음 allow: 추가 필드 허용
    )
