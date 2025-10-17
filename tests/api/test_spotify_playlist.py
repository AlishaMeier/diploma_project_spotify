import allure
import pytest
from spotify_project.helpers.api_helpers import PlaylistApi
from spotify_project.schemas.playlist import Playlist


@pytest.fixture(scope="function")
def playlist_api(api_base_url, headers):
    """Фикстура для инициализации нашего API-клиента."""
    return PlaylistApi(base_url=api_base_url, headers=headers)


@allure.feature("API: Плейлисты")
@allure.story("Получение публичного плейлиста")
@allure.label("owner", "AlishaMeier")
@allure.tag("positive", "api", "smoke")
def test_get_public_playlist(playlist_api):
    playlist_id = "5IhFrrDDvOuc1wNEmdy6EK"
    expected_playlist_name = "Spotify Project 53"
    response = playlist_api.get_playlist(playlist_id)

    with allure.step("Проверяем, что код ответа 200 (OK)"):
        assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"
    with allure.step("Валидируем схему ответа и проверяем данные"):
        playlist = Playlist.model_validate(response.json())
        assert playlist.name == expected_playlist_name


@allure.feature("API: Плейлисты")
@allure.story("Негативный кейс: поиск несуществующего плейлиста")
@allure.label("owner", "AlishaMeier")
@allure.tag("negative", "api")
def test_get_non_existent_playlist(playlist_api):
    invalid_playlist_id = "invalid_playlist_id_12345"
    response = playlist_api.get_playlist(invalid_playlist_id)

    with allure.step("Проверяем, что код ответа 400 (Bad Request)"):
        assert response.status_code == 400, f"Ожидался код 400, получен {response.status_code}"

