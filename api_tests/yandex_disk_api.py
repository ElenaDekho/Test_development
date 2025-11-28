import requests

BASE_URL = "https://cloud-api.yandex.net/v1/disk/resources"

def create_folder(token: str, folder_name: str) -> bool:
    """Создаёт папку на Яндекс.Диске. Возвращает True при успехе."""
    headers = {"Authorization": f"OAuth {token}"}
    response = requests.put(
        BASE_URL,
        headers=headers,
        params={"path": f"disk:/{folder_name}"}
    )
    return response.status_code in (201, 409)