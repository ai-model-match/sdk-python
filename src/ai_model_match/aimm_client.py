import uuid
from ai_model_match.aimm_base_client import AIMMBaseClient
from ai_model_match.dto.aimm_picker_dto import AIMMPickerDTO
from ai_model_match.dto.aimm_feedback_dto import AIMMFeedbackDTO

class AIMMClient(AIMMBaseClient):
    
    def Pick(self, use_case_code: str, step_code: str, correlation_id: uuid.UUID):
        """
        Selects and returns model prompt configuration for a given use case and step based on their code.

        Args:
            use_case_code (str): The code representing the use case. Must be between 1 and 255 characters.
            step_code (str): The code representing the specific step within the use case. Must be between 1 and 255 characters.
            correlation_id (uuid.UUID): A unique identifier for correlating the request.

        Returns:
            AIMMPickResponse: An object representing the response containing model prompt configuration.

        Raises:
            ValueError: If use_case_code or step_code are not within the required length.
            requests.HTTPError: If the HTTP request fails.
        """
        if not (1 <= len(use_case_code) <= 255):
            raise ValueError("use_case_code must be between 1 and 255 characters.")
        if not (1 <= len(step_code) <= 255):
            raise ValueError("step_code must be between 1 and 255 characters.")
        url = f"api/v1/picker"
        payload = {
            "useCaseCode": use_case_code,
            "useCaseStepCode": step_code,
            "correlationId": str(correlation_id)
        }
        data = self.post(url, payload)
        return AIMMPickerDTO.from_dict(data)
    
    def SendFeedback(self, correlation_id: uuid.UUID, score: float, comment: str):
        """
        Sends feedback data to AI Model Match for a given correlation ID request.

        Args:
            correlation_id (uuid.UUID): The unique identifier of the request.
            score (float): The feedback score to be submitted (must be between 1 and 5).
            comment (str): Additional comments or feedback (max 4096 chars).

        Returns:
            AIMMFeedbackDTO: The JSON response from the server after submitting the feedback.

        Raises:
            ValueError: If score is not between 1 and 5, or comment exceeds 4096 chars.
            requests.HTTPError: If the HTTP request to the server fails.
        """
        if not (1 <= score <= 5):
            raise ValueError("Score must be between 1 and 5.")
        if len(comment) > 4096:
            raise ValueError("Comment must not exceed 4096 characters.")
        url = f"api/v1/feedbacks"
        payload = {
            "correlationId": str(correlation_id),
            "score": score,
            "comment": comment
        }
        data = self.post(url, payload)
        return AIMMFeedbackDTO.from_dict(data)