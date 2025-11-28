import unittest
from unittest.mock import patch, Mock
from api_tests.yandex_disk_api import create_folder


class TestYandexDiskAPI(unittest.TestCase):

    @patch("api_tests.yandex_disk_api.requests.put")
    def test_create_folder_success(self, mock_put):
        # Эмулируем успешный ответ (201)
        mock_response = Mock()
        mock_response.status_code = 201
        mock_put.return_value = mock_response

        result = create_folder("valid_token", "test_folder")
        self.assertTrue(result)
        mock_put.assert_called_once()

    @patch("api_tests.yandex_disk_api.requests.put")
    def test_create_folder_already_exists(self, mock_put):
        # Эмулируем "папка уже существует" (409)
        mock_response = Mock()
        mock_response.status_code = 409
        mock_put.return_value = mock_response

        result = create_folder("valid_token", "test_folder")
        self.assertTrue(result)

    @patch("api_tests.yandex_disk_api.requests.put")
    def test_create_folder_invalid_token(self, mock_put):
        # Эмулируем ошибку авторизации (401)
        mock_response = Mock()
        mock_response.status_code = 401
        mock_put.return_value = mock_response

        result = create_folder("invalid_token", "test_folder")
        self.assertFalse(result)

    @patch("api_tests.yandex_disk_api.requests.put")
    def test_create_folder_invalid_name(self, mock_put):
        # Эмулируем недопустимое имя (404)
        mock_response = Mock()
        mock_response.status_code = 404
        mock_put.return_value = mock_response

        result = create_folder("valid_token", "/////")
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()