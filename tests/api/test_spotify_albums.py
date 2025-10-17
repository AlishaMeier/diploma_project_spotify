import allure
from spotify_project.schemas.album import GetSavedAlbumsResponse


@allure.feature("API: Медиатека")
@allure.story("Добавление, проверка и удаление альбома")
@allure.label("owner", "AlishaMeier")
@allure.tag("positive", "api", "smoke")
@allure.severity(allure.severity_level.CRITICAL)
def test_album_save_check_and_remove(library_api):
    album_id = "3DmDoHxAeEiDFNWrHSKAdQ"

    with allure.step(f"Добавление альбома {album_id} в медиатеку"):
        save_response = library_api.save_album(album_id)
        assert save_response.status_code == 200, "Ожидался код 200 при сохранении альбома"

    try:
        with allure.step("Проверка наличия альбома в списке сохраненных"):
            get_response = library_api.get_saved_albums()
            assert get_response.status_code == 200

            saved_albums_data = GetSavedAlbumsResponse.model_validate(get_response.json())
            saved_album_ids = [item.album.id for item in saved_albums_data.items]
            assert album_id in saved_album_ids, "Добавленный альбом не найден в медиатеке"

    finally:
        with allure.step("Очистка: удаление альбома из медиатеки"):
            remove_response = library_api.remove_album(album_id)
            assert remove_response.status_code == 200, "Ожидался код 200 при удалении альбома"

@allure.feature("API: Медиатека")
@allure.story("Негативный кейс: сохранение несуществующего альбома")
@allure.label("owner", "AlishaMeier")
@allure.tag("negative", "api")
def test_save_non_existent_album(library_api):
    invalid_album_id = "invalid_album_id_12345"

    response = library_api.save_album(invalid_album_id)

    with allure.step("Проверяем, что код ответа 400 (Bad Request)"):
        assert response.status_code == 400, "Ожидался код 400 при сохранении несуществующего альбома"