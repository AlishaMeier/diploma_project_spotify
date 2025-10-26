import allure
import pytest
from spotify_project.helpers.file_helpers import encode_image_to_base64


@pytest.mark.api
@allure.feature("API: Плейлисты")
@allure.label("owner", "AlishaMeier")
class TestPlaylists:

    @allure.story("Получение публичного плейлиста")
    @allure.tag("positive", "api", "smoke")
    def test_get_public_playlist(self, playlist_api):
        playlist_id = "5IhFrrDDvOuc1wNEmdy6EK"
        expected_playlist_name = "Spotify Project 53"

        _, playlist = playlist_api.get_playlist(playlist_id, expected_status_code=200)

        with allure.step("Валидируем схему ответа и проверяем данные"):
            assert playlist.name == expected_playlist_name

    @allure.story("Негативный кейс: поиск несуществующего плейлиста")
    @allure.tag("negative", "api")
    def test_get_non_existent_playlist(self, playlist_api):
        non_existing_playlist_id = "5IhFrrSSvOuc1wNEmdy6EK"

        playlist_api.get_playlist(
            non_existing_playlist_id,
            expected_status_code=404
        )

    @allure.story("Негативный кейс: невалидный поиск")
    @allure.tag("negative", "api")
    def test_get_invalid_playlist_id(self, playlist_api):
        invalid_playlist_id = "non_valid"

        playlist_api.get_playlist(
            invalid_playlist_id,
            expected_status_code=400
        )

    @allure.story("Создание и удаление плейлиста (через фикстуру)")
    @allure.tag("positive", "api", "smoke")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_and_delete_playlist_via_fixture(self, playlist_api, create_temp_playlist, user_id):
        playlist_id = create_temp_playlist

        with allure.step("Проверяем, что плейлист действительно создан"):
            assert playlist_id is not None, "Фикстура не вернула playlist_id"
            _, model = playlist_api.get_playlist(playlist_id, expected_status_code=200)
            assert model.name == "Temp Test Playlist"


    @allure.story("Добавление трека в существующий плейлист")
    @allure.tag("positive", "api")
    @allure.severity(allure.severity_level.NORMAL)
    def test_add_track_to_playlist(self, playlist_api, create_temp_playlist):
        playlist_id = create_temp_playlist


        with allure.step("Добавление трека в плейлист"):
            track_uri = "spotify:track:4cOdK2wGLETOMsVUpgjoEi"
            _, add_model = playlist_api.add_track_to_playlist(
                playlist_id,
                track_uri,
                expected_status_code=201
            )

        assert add_model.snapshot_id is not None, "Не получен snapshot_id"


    @allure.story("Добавление и удаление выбранного трека")
    @allure.tag("positive", "api", "smoke")
    def test_add_and_delete_specific_track(self, playlist_api):
        playlist_id = "5IhFrrDDvOuc1wNEmdy6EK"
        track_uri = f"spotify:track:5Sk3k49SNCH8ytqHBLIq61"

        with allure.step(f"Добавление трека {track_uri} в плейлист {playlist_id}"):
                _ = playlist_api.add_track_to_playlist(
                playlist_id,
                track_uri,
                expected_status_code=201
            )

        with allure.step("Очистка: удаление добавленного трека из плейлиста"):
                _ = playlist_api.delete_track_from_playlist(
                playlist_id,
                track_uri,
                expected_status_code=200
            )

    @allure.story("Негативный кейс: создание плейлиста без имени")
    @allure.tag("negative", "api")
    def test_create_playlist_without_name(self, playlist_api, user_id):
            _ = playlist_api.create_playlist(
            user_id=user_id,
            name="",
            description="Test description",
            expected_status_code=400
        )

    @allure.story("Негативный кейс: добавление несуществующего трека")
    @allure.tag("negative", "api")
    def test_add_non_existent_track(self, playlist_api):
        playlist_id = "5IhFrrDDvOuc1wNEmdy6EK"
        invalid_track_uri = "spotify:track:invalid_uri_12345"

        _, _ = playlist_api.add_track_to_playlist(
            playlist_id,
            invalid_track_uri,
            expected_status_code=400
        )

    @allure.story("Работа с файлами: Загрузка обложки плейлиста")
    @allure.tag("positive", "api", "file_upload")
    @allure.severity(allure.severity_level.NORMAL)
    def test_upload_custom_playlist_cover(self, playlist_api, create_temp_playlist):
        playlist_id = create_temp_playlist
        image_base64_bytes = encode_image_to_base64('cover.jpg')

        with allure.step("Загрузка обложки в плейлист"):
            _ = playlist_api.upload_playlist_cover(
                playlist_id,
                image_base64_bytes,
                expected_status_code=202
            )