import unittest
from unittest.mock import patch, MagicMock
from tangbao.apollo import Apollo

class TestApollo(unittest.TestCase):

    @patch('tangbao.apollo.requests.get')
    def test_get_monthly_costs(self, mock_get):
        # Arrange
        mock_response = MagicMock()
        mock_response.json.return_value = {"cost": 100}
        mock_get.return_value = mock_response
        
        apollo = Apollo()
        
        # Act
        result = apollo.get_monthly_costs()
        
        # Assert
        self.assertEqual(result, {"cost": 100})
        mock_get.assert_called_once_with(f'{apollo._base_url}/application/cost', headers=apollo._api_headers)

    @patch('tangbao.apollo.requests.get')
    def test_get_model_info(self, mock_get):
        # Arrange
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": {"model": "gpt-4o-mini"}}
        mock_get.return_value = mock_response
        
        apollo = Apollo()
        
        # Act
        result = apollo.get_model_info()
        
        # Assert
        self.assertEqual(result, {"model": "gpt-4o-mini"})
        mock_get.assert_called_once_with(f"{apollo._base_url}/model/info", headers=apollo._api_headers)

    @patch('tangbao.apollo.OAuth2Session.fetch_token')
    def test_refresh_token(self, mock_fetch_token):
        # Arrange
        mock_fetch_token.return_value = {
            'access_token': 'new_token',
            'expires_in': 3600
        }
        
        apollo = Apollo()
        apollo._token_data['access_token'] = None  # Simulate expired token
        
        # Act
        apollo._refresh_token()
        
        # Assert
        self.assertEqual(apollo._token_data['access_token'], 'new_token')

    @patch('tangbao.apollo.openai.OpenAI')
    def test_initialize_client(self, mock_openai):
        # Arrange
        apollo = Apollo()
        apollo._token_data['access_token'] = 'valid_token'
        
        # Act
        client = apollo._initialize_client()
        
        # Assert
        mock_openai.assert_called_once_with(api_key='valid_token', base_url=apollo._base_url)

    @patch('tangbao.apollo.requests.post')
    def test_query_index(self, mock_post):
        # Arrange
        mock_response = MagicMock()
        mock_response.json.return_value = {"result": "success"}
        mock_post.return_value = mock_response
        
        apollo = Apollo()
        
        # Act
        result = apollo.query_index("What is the capital of France?", 5, "user_index", "openai-text-embedding-3-large")
        
        # Assert
        self.assertEqual(result, {"result": "success"})
        mock_post.assert_called_once()

    @patch('tangbao.apollo.requests.get')
    def test_iam(self, mock_get):
        # Arrange
        mock_response = MagicMock()
        mock_response.json.return_value = {"iam": "success"}
        mock_get.return_value = mock_response
        
        apollo = Apollo()
        
        # Act
        result = apollo.iam()
        
        # Assert
        self.assertEqual(result, {"iam": "success"})
        mock_get.assert_called_once_with(f'{apollo._base_url}/application/iam', headers=apollo._api_headers)

# Integration Tests
class TestApolloIntegration(unittest.TestCase):

    def setUp(self):
        self.apollo = Apollo()

    def test_get_monthly_costs(self):
        response = self.apollo.get_monthly_costs()
        self.assertIsInstance(response, dict)  # Check if response is a dictionary
        self.assertIn('spend', response)  # Check if cost key is in the response

    def test_get_model_info(self):
        response = self.apollo.get_model_info()
        self.assertIsInstance(response, list)
        self.assertIn('model_name', response[0])  # Check if 'model_name' key is in the response

    def test_iam(self):
        response = self.apollo.iam()
        self.assertIsInstance(response, dict)  # Check if response is a dictionary
        self.assertIn('id', response)  # Check if 'id' key is in the response

if __name__ == '__main__':
    unittest.main()