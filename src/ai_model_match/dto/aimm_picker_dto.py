from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class InputMessageDTO:
    correlation_id: str
    use_case_code: str
    use_case_step_code: str

    @staticmethod
    def from_dict(data: dict) -> "InputMessageDTO":
        return InputMessageDTO(
            correlation_id=data["correlationId"],
            use_case_code=data["useCaseCode"],
            use_case_step_code=data["useCaseStepCode"]
        )

@dataclass
class OutputMessageDTO:
    modality: str
    parameters: Dict[str, Any]

    @staticmethod
    def from_dict(data: dict) -> "OutputMessageDTO":
        return OutputMessageDTO(
            modality=data["modality"],
            parameters=data.get("parameters", {})
        )

@dataclass
class ItemDTO:
    id: str
    use_case_id: str
    use_case_step_id: str
    flow_id: str
    flow_step_id: str
    correlation_id: str
    is_first_correlation: bool
    input_message: InputMessageDTO
    output_message: OutputMessageDTO
    placeholders: List[str]
    created_at: str

    @staticmethod
    def from_dict(data: dict) -> "ItemDTO":
        input_msg = InputMessageDTO.from_dict(data["inputMessage"])
        output_msg = OutputMessageDTO.from_dict(data["outputMessage"])
        return ItemDTO(
            id=data["id"],
            use_case_id=data["useCaseId"],
            use_case_step_id=data["useCaseStepId"],
            flow_id=data["flowId"],
            flow_step_id=data["flowStepId"],
            correlation_id=data["correlationId"],
            is_first_correlation=data["isFirstCorrelation"],
            input_message=input_msg,
            output_message=output_msg,
            placeholders=data.get("placeholders", []),
            created_at=data["createdAt"]
        )

@dataclass
class AIMMPickerDTO:
    item: ItemDTO

    @staticmethod
    def from_dict(data: dict) -> "AIMMPickerDTO":
        item = ItemDTO.from_dict(data["item"])
        return AIMMPickerDTO(item=item)