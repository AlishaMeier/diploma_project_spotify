import allure
from spotify_project.schemas.playlist import Playlist, AddTrackResponse
import base64
import os


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
    non_existing_playlist_id = "5IhFrrSSvOuc1wNEmdy6EK"
    response = playlist_api.get_playlist(non_existing_playlist_id)

    with allure.step("Проверяем, что код ответа 404 (Not Founded)"):
        assert response.status_code == 404, f"Ожидался код 404, получен {response.status_code}"


@allure.feature("API: Плейлисты")
@allure.story("Негативный кейс: невалидный поиск")
@allure.label("owner", "AlishaMeier")
@allure.tag("negative", "api")
def test_get_invalid_playlist_id(playlist_api):
    invalid_playlist_id = "non_valid"
    response = playlist_api.get_playlist(invalid_playlist_id)

    with allure.step("Проверяем, что код ответа 400 (Bad Request)"):
        assert response.status_code == 400, f"Ожидался код 400, получен {response.status_code}"


@allure.feature("API: Плейлисты")
@allure.story("Создание и удаление плейлиста")
@allure.label("owner", "AlishaMeier")
@allure.tag("positive", "api", "smoke")
@allure.severity(allure.severity_level.CRITICAL)
def test_create_and_delete_playlist(playlist_api, user_id):
    playlist_id = None
    try:
        playlist_name = "My New Autotest Playlist"
        playlist_desc = "Blah-blah-blah"

        response = playlist_api.create_playlist(
            user_id=user_id,
            name=playlist_name,
            description=playlist_desc
        )

        with allure.step("Проверяем, что плейлист успешно создан (код 201)"):
            assert response.status_code == 201, "Ожидался код 201 (Created)"
            created_playlist = Playlist.model_validate(response.json())
            playlist_id = created_playlist.id  # Сохранию ID для удаления
            assert created_playlist.name == playlist_name

    finally:
        if playlist_id:
            with allure.step("Очистка: удаление плейлиста с ID {playlist_id}"):
                delete_response = playlist_api.unfollow_playlist(playlist_id)
                assert delete_response.status_code == 200, "Не удалось удалить плейлист при очистке"


@allure.feature("API: Плейлисты")
@allure.story("Добавление трека в существующий плейлист")
@allure.label("owner", "AlishaMeier")
@allure.tag("positive", "api")
@allure.severity(allure.severity_level.NORMAL)
def test_add_track_to_playlist(playlist_api, user_id):
    playlist_id = None
    try:
        with allure.step("Создание временного плейлиста"):
            create_response = playlist_api.create_playlist(
                user_id=user_id,
                name="Playlist for Adding Tracks",
                description="Temporary test playlist"
            )
            assert create_response.status_code == 201
            playlist_id = create_response.json()["id"]

        with allure.step("Добавление трека в плейлист"):
            track_uri = "spotify:track:4cOdK2wGLETOMsVUpgjoEi"
            add_response = playlist_api.add_track_to_playlist(playlist_id, track_uri)

        with allure.step("Проверяем, что трек успешно добавлен (код 201)"):
            assert add_response.status_code == 201, "Ожидался код 201 (Created) при добавлении трека"
            AddTrackResponse.model_validate(add_response.json())

    finally:
        if playlist_id:
            with allure.step(f"Очистка: удаление временного плейлиста"):
                playlist_api.unfollow_playlist(playlist_id)


@allure.feature("API: Плейлисты")
@allure.story("Добавление и удаление выбранного трека")
@allure.label("owner", "AlishaMeier")
@allure.tag("positive", "api", "smoke")
def test_add_and_delete_specific_track(playlist_api):
    playlist_id = "5IhFrrDDvOuc1wNEmdy6EK"
    track_uri = f"spotify:track:5Sk3k49SNCH8ytqHBLIq61"

    with allure.step(f"Добавление трека {track_uri} в плейлист {playlist_id}"):
        add_response = playlist_api.add_track_to_playlist(playlist_id, track_uri)

    with allure.step("Проверяем код ответа 201 и валидируем схему"):
        assert add_response.status_code == 201, "Ожидался код 201 (Created) при добавлении трека"
        AddTrackResponse.model_validate(add_response.json())

    with allure.step("Очистка: удаление добавленного трека из плейлиста"):
        delete_response = playlist_api.delete_track_from_playlist(playlist_id, track_uri)
        assert delete_response.status_code == 200, "Ожидался код 200 при удалении трека"

@allure.feature("API: Плейлисты")
@allure.story("Негативный кейс: создание плейлиста без имени")
@allure.label("owner", "AlishaMeier")
@allure.tag("negative", "api")
def test_create_playlist_without_name(playlist_api, user_id):
    response = playlist_api.create_playlist(
        user_id=user_id,
        name="",  # Отправляю пустоту
        description="Test description"
    )

    with allure.step("Проверяем, что код ответа 400 (Bad Request)"):
        assert response.status_code == 400, "Ожидался код 400 при создании плейлиста без имени"


@allure.feature("API: Плейлисты")
@allure.story("Негативный кейс: добавление несуществующего трека")
@allure.label("owner", "AlishaMeier")
@allure.tag("negative", "api")
def test_add_non_existent_track(playlist_api):
    playlist_id = "5IhFrrDDvOuc1wNEmdy6EK"
    invalid_track_uri = "spotify:track:invalid_uri_12345"

    response = playlist_api.add_track_to_playlist(playlist_id, invalid_track_uri)

    with allure.step("Проверяем, что код ответа 400 (Bad Request)"):
        assert response.status_code == 400, "Ожидался код 400 при добавлении несуществующего трека"


@allure.feature("API: Плейлисты")
@allure.story("Работа с файлами: Загрузка обложки плейлиста")
@allure.label("owner", "AlishaMeier")
@allure.tag("positive", "api", "file_upload")
@allure.severity(allure.severity_level.NORMAL)
def test_upload_custom_playlist_cover(playlist_api, user_id):
    playlist_id = None
    try:
        with allure.step("Создание временного плейлиста для теста"):
            create_response = playlist_api.create_playlist(
                user_id=user_id,
                name="Playlist for Cover Upload",
                description="Test playlist for file upload"
            )
            assert create_response.status_code == 201
            playlist_id = create_response.json()["id"]

        with allure.step("Чтение и кодирование нашей картинки в Base64)"):
            image_path = os.path.abspath(
                os.path.join(os.path.dirname(__file__), '..', 'resources', 'cover.jpg')
            )
            assert os.path.exists(image_path), f"Файл не найден: {image_path}"

            with open(image_path, 'rb') as image_file:
                image_data = image_file.read()
                image_base64_bytes = base64.b64encode(image_data)

        with allure.step("Загрузка обложки в плейлист"):
            upload_response = playlist_api.upload_playlist_cover(
                playlist_id,
                image_base64_bytes  # Передаем БАЙТЫ
            )

        with allure.step("Проверяем, что обложка успешно загружена (код 202)"):
            assert upload_response.status_code == 202, \
                "Ожидался код 202 (Accepted) при загрузке обложки. " \
                f"Тело ответа: {upload_response.text}"

    finally:
        if playlist_id:
            with allure.step(f"Очистка: удаление временного плейлиста"):
                delete_response = playlist_api.unfollow_playlist(playlist_id)
                assert delete_response.status_code == 200, "Не удалось удалить плейлист при очистке"