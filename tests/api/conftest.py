import pytest
import os
import allure
from dotenv import load_dotenv
from spotify_project.helpers.api_helpers import LibraryApi, PlaylistApi

load_dotenv()

ALBUM_ID_FOR_TESTS = "3DmDoHxAeEiDFNWrHSKAdQ"


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


def _is_album_saved(library_api: LibraryApi) -> bool:
    """[Пункт 9] Внутренний хелпер для проверки, сохранен ли тестовый альбом."""
    try:
        _, model = library_api.get_saved_albums()
        if model is None:
            return False

        saved_album_ids = [item.album.id for item in model.items]
        return ALBUM_ID_FOR_TESTS in saved_album_ids
    except Exception as e:
        allure.attach(
            body=f"Ошибка при проверке альбома: {e}",
            name="album_check_error",
            attachment_type=allure.attachment_type.TEXT
        )
        return False


@pytest.fixture(scope="function")
def ensure_album_is_removed(library_api):

    with allure.step(f"[Fixture Setup] Проверка и удаление альбома {ALBUM_ID_FOR_TESTS}"):
        if _is_album_saved(library_api):
            library_api.remove_album(ALBUM_ID_FOR_TESTS, expected_status_code=200)

    yield

    with allure.step(f"[Fixture Teardown] Очистка: удаление альбома {ALBUM_ID_FOR_TESTS}"):
        if _is_album_saved(library_api):
            library_api.remove_album(ALBUM_ID_FOR_TESTS, expected_status_code=200)


@pytest.fixture(scope="function")
def ensure_album_is_added(library_api, ensure_album_is_removed):

    with allure.step(f"[Fixture Setup] Добавление альбома {ALBUM_ID_FOR_TESTS}"):
        if not _is_album_saved(library_api):
            library_api.save_album(ALBUM_ID_FOR_TESTS, expected_status_code=200)

    yield


@pytest.fixture(scope="function")
def create_temp_playlist(playlist_api, user_id):

    playlist_id = None
    with allure.step("[Fixture Setup] Создание временного плейлиста"):
        response, model = playlist_api.create_playlist(
            user_id=user_id,
            name="Temp Test Playlist",
            description="Temporary test playlist by autotest",
            expected_status_code=201
        )
        playlist_id = model.id

    yield playlist_id

    with allure.step(f"[Fixture Teardown] Очистка: удаление плейлиста {playlist_id}"):
        if playlist_id:
            playlist_api.unfollow_playlist(playlist_id, expected_status_code=200)