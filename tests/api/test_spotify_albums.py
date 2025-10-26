import allure
import pytest
from spotify_project.schemas.album import GetSavedAlbumsResponse

ALBUM_ID_FOR_TESTS = "3DmDoHxAeEiDFNWrHSKAdQ"


@pytest.mark.api
@allure.feature("API: Медиатека")
@allure.label("owner", "AlishaMeier")
class TestAlbums: 

    @allure.story("Добавление и проверка альбома")
    @allure.tag("positive", "api", "smoke")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_album_save_and_check(self, library_api, ensure_album_is_removed):
        album_id = ALBUM_ID_FOR_TESTS

        with allure.step(f"Добавление альбома {album_id} в медиатеку"):
            library_api.save_album(album_id, expected_status_code=200)

        with allure.step("Проверка наличия альбома в списке сохраненных"):
            response, saved_albums_data = library_api.get_saved_albums()

            saved_album_ids = [item.album.id for item in saved_albums_data.items]
            assert album_id in saved_album_ids, "Добавленный альбом не найден в медиатеке"


    @allure.story("Удаление альбома")
    @allure.tag("positive", "api")
    def test_album_remove_and_check(self, library_api, ensure_album_is_added):

        album_id = ALBUM_ID_FOR_TESTS

        with allure.step(f"Удаление альбома {album_id} из медиатеки"):
            library_api.remove_album(album_id, expected_status_code=200)

        with allure.step("Проверка отсутствия альбома в списке сохраненных"):
            _, saved_albums_data = library_api.get_saved_albums()
            saved_album_ids = [item.album.id for item in saved_albums_data.items]
            assert album_id not in saved_album_ids, "Удаленный альбом все еще в медиатеке"


    @allure.story("Негативный кейс: сохранение несуществующего альбома")
    @allure.tag("negative", "api")
    def test_save_non_existent_album(self, library_api):
        invalid_album_id = "invalid_album_id_12345"

        response = library_api.save_album(
            invalid_album_id,
            expected_status_code=400 # <-- [Пункт 12]
        )