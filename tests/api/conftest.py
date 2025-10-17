import pytest
import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = "https://api.spotify.com/v1"
AUTH_URL = "https://accounts.spotify.com/api/token"
USER_ID = os.getenv('SPOTIFY_USER_ID')
CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')


@pytest.fixture(scope="session")
def access_token():
    """
    Получает токен доступа перед началом сессии тестов.
    """
    if not CLIENT_ID or not CLIENT_SECRET:
        raise ValueError("SPOTIFY_CLIENT_ID и SPOTIFY_CLIENT_SECRET должны быть установлены в .env")

    response = requests.post(
        AUTH_URL,
        data={
            "grant_type": "client_credentials",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    response.raise_for_status()  # Вызовет ошибку, если запрос не удался
    return response.json()["access_token"]


@pytest.fixture(scope="session")
def api_base_url():
    """Возвращает базовый URL для API."""
    return API_BASE_URL


@pytest.fixture(scope="session")
def user_id():
    """Возвращает ID пользователя из .env."""
    return USER_ID


@pytest.fixture(scope="session")
def headers(access_token):
    """
    Формирует заголовки для всех запросов к API, используя полученный токен.
    """
    return {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }


@pytest.fixture(scope="session")
def expected_display_name():
    """Возвращает ожидаемое имя пользователя из .env."""
    return os.getenv('SPOTIFY_DISPLAY_NAME')