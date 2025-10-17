import os
import random
import string
import pytest
import allure
from spotify_project.pages.web.login_page import LoginPage
from spotify_project.pages.web.library_page import LibraryPage
from spotify_project.pages.web.navigation_page import NavigationPage


@allure.epic("UI-тестирование")
@allure.feature("Библиотека и Плейлисты")
class TestPlaylistCRUD:

    @allure.story("E2E-сценарий работы с плейлистом")
    @allure.label("owner", "AlishaMeier")
    @allure.tag("positive", "CRUD", "smoke")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_full_playlist_lifecycle(self, credentials, login_page: LoginPage, library_page: LibraryPage,
                                     navigation_page: NavigationPage):
        random_suffix = ''.join(random.choices(string.digits, k=2))
        new_playlist_name = f"Spotify Project {random_suffix}"
        song_to_add = "Devil in Disguise"

        cover_image_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', '..', 'resources', 'cover.jpeg')
        )
        assert os.path.exists(cover_image_path), f"Файл обложки не найден по пути: {cover_image_path}"

        with allure.step("Авторизация"):
            navigation_page.navigate_to_login()
            login_page.login(credentials["username"], credentials["password"]).should_be_logged_in()

        with allure.step("Создание плейлиста"):
            original_playlist_name = library_page.create_playlist()
            library_page.should_be_on_playlist_page_with_name(original_playlist_name)

        with allure.step("Редактирование деталей плейлиста"):
            library_page.open_edit_details_modal()
            library_page.set_playlist_name(new_playlist_name)
            library_page.set_playlist_cover_image(cover_image_path)
            library_page.save_playlist_details()

        #with allure.step("Проверка, что название и обложка обновились"):
            # СНАЧАЛА проверяем заголовок на открытой странице плейлиста.
            # Это даст уверенность, что сохранение прошло успешно.
            #library_page.should_be_on_playlist_page_with_name(new_playlist_name)

            # ТЕПЕРЬ проверяем наличие плейлиста в списке слева.
            #library_page.should_have_playlist_in_list(new_playlist_name)

        #with allure.step("Проверка, что плейлист с новым именем появился в боковом меню"):
        #    library_page.should_have_playlist_in_list(new_playlist_name)

        with allure.step(f"Поиск и добавление песни '{song_to_add}'"):
            # Кликаем по плейлисту в списке, чтобы снова на него перейти
        #    library_page.playlist_item_by_name(new_playlist_name).click()

            library_page.add_song_to_playlist(song_to_add)

        with allure.step("Проверка, что песня добавлена в плейлист"):
            library_page.should_have_song_in_playlist(song_to_add)

        with allure.step("Очистка: Удаление тестового плейлиста"):
            library_page.delete_playlist(new_playlist_name)