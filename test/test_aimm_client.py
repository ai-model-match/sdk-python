import uuid
import pytest
from unittest.mock import MagicMock, patch
from ai_model_match.aimm_client import AIMMClient
from ai_model_match.dto.aimm_picker_dto import AIMMPickerDTO
from ai_model_match.dto.aimm_feedback_dto import AIMMFeedbackDTO

@pytest.fixture
def client():
    # Patch AIMMBaseClient to avoid real HTTP calls
    with patch("ai_model_match.aimm_client.AIMMBaseClient.__init__", return_value=None):
        yield AIMMClient()

def picker_response_dict():
    return {
        "item": {
            "id": "item123",
            "useCaseId": "uc123",
            "useCaseStepId": "step123",
            "flowId": "flow123",
            "flowStepId": "flowstep123",
            "correlationId": "corr123",
            "isFirstCorrelation": True,
            "inputMessage": {
                "correlationId": "corr123",
                "useCaseCode": "ucode",
                "useCaseStepCode": "scode"
            },
            "outputMessage": {
                "modality": "text",
                "parameters": {"param1": "value1"}
            },
            "placeholders": ["ph1", "ph2"],
            "createdAt": "2024-06-01T00:00:00Z"
        }
    }

def feedback_response_dict():
    return {
        "item": {
            "id": "fbid123",
            "useCaseId": "ucid123",
            "flowId": "flowid123",
            "correlationId": "corrid123",
            "syntheticScore": 4.5,
            "comment": "Good job",
            "referenceLink": "http://example.com",
            "createdAt": "2024-06-01T00:00:00Z"
        }
    }

def test_pick_success(client):
    client.post = MagicMock(return_value=picker_response_dict())
    corr_id = uuid.uuid4()
    result = client.Pick("ucode", "scode", corr_id)
    assert isinstance(result, AIMMPickerDTO)
    assert result.item.id == "item123"
    assert result.item.input_message.use_case_code == "ucode"
    assert result.item.output_message.modality == "text"
    assert result.item.placeholders == ["ph1", "ph2"]

@pytest.mark.parametrize("use_case_code", ["", "a"*256])
def test_pick_invalid_use_case_code(client, use_case_code):
    corr_id = uuid.uuid4()
    with pytest.raises(ValueError):
        client.Pick(use_case_code, "validstep", corr_id)

@pytest.mark.parametrize("step_code", ["", "b"*256])
def test_pick_invalid_step_code(client, step_code):
    corr_id = uuid.uuid4()
    with pytest.raises(ValueError):
        client.Pick("validusecase", step_code, corr_id)

def test_pick_calls_post_with_correct_payload(client):
    client.post = MagicMock(return_value=picker_response_dict())
    corr_id = uuid.uuid4()
    client.Pick("ucode", "scode", corr_id)
    client.post.assert_called_once()
    args, kwargs = client.post.call_args
    assert args[0] == "api/v1/picker"
    payload = args[1]
    assert payload["useCaseCode"] == "ucode"
    assert payload["useCaseStepCode"] == "scode"
    assert payload["correlationId"] == str(corr_id)

def test_send_feedback_success(client):
    client.post = MagicMock(return_value=feedback_response_dict())
    corr_id = uuid.uuid4()
    result = client.SendFeedback(corr_id, 4.5, "Good job", "http://example.com")
    assert isinstance(result, AIMMFeedbackDTO)
    assert result.item.synthetic_score == 4.5
    assert result.item.comment == "Good job"
    assert result.item.reference_link == "http://example.com"

@pytest.mark.parametrize("score", [0.9, 5.1])
def test_send_feedback_invalid_score(client, score):
    corr_id = uuid.uuid4()
    with pytest.raises(ValueError):
        client.SendFeedback(corr_id, score)

def test_send_feedback_comment_too_long(client):
    corr_id = uuid.uuid4()
    comment = "a" * 4097
    with pytest.raises(ValueError):
        client.SendFeedback(corr_id, 4.0, comment)

def test_send_feedback_reference_link_too_long(client):
    corr_id = uuid.uuid4()
    link = "b" * 4097
    with pytest.raises(ValueError):
        client.SendFeedback(corr_id, 4.0, reference_link=link)

def test_send_feedback_calls_post_with_correct_payload(client):
    client.post = MagicMock(return_value=feedback_response_dict())
    corr_id = uuid.uuid4()
    client.SendFeedback(corr_id, 3.0, "Comment", "http://ref.com")
    client.post.assert_called_once()
    args, kwargs = client.post.call_args
    assert args[0] == "api/v1/feedbacks"
    payload = args[1]
    assert payload["correlationId"] == str(corr_id)
    assert payload["syntheticScore"] == 3.0
    assert payload["comment"] == "Comment"
    assert payload["referenceLink"] == "http://ref.com"

def test_send_feedback_optional_fields(client):
    client.post = MagicMock(return_value=feedback_response_dict())
    corr_id = uuid.uuid4()
    # comment and referenceLink omitted
    result = client.SendFeedback(corr_id, 5.0)
    assert isinstance(result, AIMMFeedbackDTO)
    client.post.assert_called_once()
    payload = client.post.call_args[0][1]
    assert payload["correlationId"] == str(corr_id)
    assert payload["syntheticScore"] == 5.0
    assert payload["comment"] is None
    assert payload["referenceLink"] is None