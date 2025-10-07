from dataclasses import dataclass

@dataclass
class FeedbackItemDTO:
    id: str
    use_case_id: str
    flow_id: str
    correlation_id: str
    score: float
    comment: str
    created_at: str

    @staticmethod
    def from_dict(data: dict) -> "FeedbackItemDTO":
        return FeedbackItemDTO(
            id=data["id"],
            use_case_id=data["useCaseId"],
            flow_id=data["flowId"],
            correlation_id=data["correlationId"],
            score=data["score"],
            comment=data["comment"],
            created_at=data["createdAt"]
        )

@dataclass
class AIMMFeedbackDTO:
    item: FeedbackItemDTO

    @staticmethod
    def from_dict(data: dict) -> "AIMMFeedbackDTO":
        print(data)
        item = FeedbackItemDTO.from_dict(data["item"])
        return AIMMFeedbackDTO(item=item)