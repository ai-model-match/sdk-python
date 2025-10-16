from dataclasses import dataclass
from typing import Optional

@dataclass
class FeedbackItemDTO:
    id: str
    use_case_id: str
    flow_id: str
    correlation_id: str
    synthetic_score: float
    comment: Optional[str]
    reference_link: Optional[str]
    created_at: str

    @staticmethod
    def from_dict(data: dict) -> "FeedbackItemDTO":
        return FeedbackItemDTO(
            id=data["id"],
            use_case_id=data["useCaseId"],
            flow_id=data["flowId"],
            correlation_id=data["correlationId"],
            synthetic_score=data["syntheticScore"],
            comment=data.get("comment"),
            reference_link=data.get("referenceLink"),
            created_at=data["createdAt"]
        )

@dataclass
class AIMMFeedbackDTO:
    item: FeedbackItemDTO

    @staticmethod
    def from_dict(data: dict) -> "AIMMFeedbackDTO":
        item = FeedbackItemDTO.from_dict(data["item"])
        return AIMMFeedbackDTO(item=item)