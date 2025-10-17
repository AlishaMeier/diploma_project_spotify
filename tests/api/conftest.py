import pytest
import os
from dotenv import load_dotenv
from spotify_project.helpers.api_helpers import LibraryApi, PlaylistApi

load_dotenv()

@pytest.fixture(scope="session")
def api_base_url():

    return "https://api.spotify.com/v1"

@pytest.fixture(scope="session")
def user_id():

    return os.getenv('SPOTIFY_USER_ID')

@pytest.fixture(scope="session")
def headers():
    token = os.getenv('SPOTIFY_API_TOKEN')

    print(f"DEBUG: Read token from .env: {token}")

    if not token:
        raise ValueError("SPOTIFY_API_TOKEN не найден в .env. Пожалуйста, получите и добавьте его.")
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

@pytest.fixture(scope="session")
def expected_display_name():

    return os.getenv('SPOTIFY_DISPLAY_NAME')

@pytest.fixture(scope="module")
def library_api(api_base_url, headers):

    return LibraryApi(base_url=api_base_url, headers=headers)


@pytest.fixture(scope="function")
def playlist_api(api_base_url, headers):

    return PlaylistApi(base_url=api_base_url, headers=headers)
