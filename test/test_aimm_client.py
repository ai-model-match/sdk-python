import unittest
from unittest.mock import patch, MagicMock
import uuid
from ai_model_match.aimm_client import AIMMClient
from ai_model_match.dto.aimm_picker_dto import AIMMPickerDTO
from ai_model_match.dto.aimm_feedback_dto import AIMMFeedbackDTO

class TestAIMMClient(unittest.TestCase):

    def setUp(self):
        self.client = AIMMClient("http://ai-model-match.test", "test_api_key")
        self.correlation_id = uuid.uuid4()
        self.use_case_code = "test_use_case"
        self.step_code = "test_step"
        self.score = 4.5
        self.comment = "Great job!"

    @patch.object(AIMMClient, 'post')
    @patch('ai_model_match.dto.aimm_picker_dto.AIMMPickerDTO.from_dict')
    def test_pick_success(self, mock_from_dict, mock_post):
        mock_post.return_value = {"mock": "data"}
        mock_from_dict.return_value = "dto_instance"
        result = self.client.Pick(self.use_case_code, self.step_code, self.correlation_id)
        mock_post.assert_called_once_with(
            "api/v1/picker",
            {
                "useCaseCode": self.use_case_code,
                "useCaseStepCode": self.step_code,
                "correlationId": str(self.correlation_id)
            }
        )
        mock_from_dict.assert_called_once_with({"mock": "data"})
        self.assertEqual(result, "dto_instance")

    def test_pick_invalid_use_case_code(self):
        with self.assertRaises(ValueError):
            self.client.Pick("", self.step_code, self.correlation_id)
        with self.assertRaises(ValueError):
            self.client.Pick("a" * 256, self.step_code, self.correlation_id)

    def test_pick_invalid_step_code(self):
        with self.assertRaises(ValueError):
            self.client.Pick(self.use_case_code, "", self.correlation_id)
        with self.assertRaises(ValueError):
            self.client.Pick(self.use_case_code, "b" * 256, self.correlation_id)

    @patch.object(AIMMClient, 'post')
    @patch('ai_model_match.dto.aimm_feedback_dto.AIMMFeedbackDTO.from_dict')
    def test_send_feedback_success(self, mock_from_dict, mock_post):
        mock_post.return_value = {"feedback": "data"}
        mock_from_dict.return_value = "feedback_dto"
        result = self.client.SendFeedback(self.correlation_id, self.score, self.comment)
        mock_post.assert_called_once_with(
            "api/v1/feedbacks",
            {
                "correlationId": str(self.correlation_id),
                "score": self.score,
                "comment": self.comment
            }
        )
        mock_from_dict.assert_called_once_with({"feedback": "data"})
        self.assertEqual(result, "feedback_dto")

    def test_send_feedback_invalid_score(self):
        with self.assertRaises(ValueError):
            self.client.SendFeedback(self.correlation_id, 0, self.comment)
        with self.assertRaises(ValueError):
            self.client.SendFeedback(self.correlation_id, 6, self.comment)

    def test_send_feedback_comment_too_long(self):
        long_comment = "a" * 4097
        with self.assertRaises(ValueError):
            self.client.SendFeedback(self.correlation_id, self.score, long_comment)
    @patch.object(AIMMClient, 'post')
    @patch('ai_model_match.dto.aimm_feedback_dto.AIMMFeedbackDTO.from_dict')
    def test_send_feedback_valid_score_bounds(self, mock_from_dict, mock_post):
        # Test lower bound
        mock_post.return_value = {"feedback": "data"}
        mock_from_dict.return_value = "feedback_dto"
        result = self.client.SendFeedback(self.correlation_id, 1, self.comment)
        mock_post.assert_called_with(
            "api/v1/feedbacks",
            {
                "correlationId": str(self.correlation_id),
                "score": 1,
                "comment": self.comment
            }
        )
        self.assertEqual(result, "feedback_dto")

        # Test upper bound
        mock_post.reset_mock()
        mock_from_dict.reset_mock()
        mock_post.return_value = {"feedback": "data"}
        mock_from_dict.return_value = "feedback_dto"
        result = self.client.SendFeedback(self.correlation_id, 5, self.comment)
        mock_post.assert_called_with(
            "api/v1/feedbacks",
            {
                "correlationId": str(self.correlation_id),
                "score": 5,
                "comment": self.comment
            }
        )
        self.assertEqual(result, "feedback_dto")

    @patch.object(AIMMClient, 'post')
    @patch('ai_model_match.dto.aimm_feedback_dto.AIMMFeedbackDTO.from_dict')
    def test_send_feedback_comment_max_length(self, mock_from_dict, mock_post):
        max_length_comment = "a" * 4096
        mock_post.return_value = {"feedback": "data"}
        mock_from_dict.return_value = "feedback_dto"
        result = self.client.SendFeedback(self.correlation_id, self.score, max_length_comment)
        mock_post.assert_called_once_with(
            "api/v1/feedbacks",
            {
                "correlationId": str(self.correlation_id),
                "score": self.score,
                "comment": max_length_comment
            }
        )
        self.assertEqual(result, "feedback_dto")
if __name__ == "__main__":
    unittest.main()