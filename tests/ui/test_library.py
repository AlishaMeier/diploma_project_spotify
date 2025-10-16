import os
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
        new_playlist_name = "Spotify Project 2"
        song_to_add = "Devil in Disguise"

        cover_image_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', '..', 'resources', 'cover.jpeg')
        )

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

        with allure.step("Проверка, что название и обложка обновились"):
            library_page.should_be_on_playlist_page_with_name(new_playlist_name)
            library_page.should_have_playlist_in_list(new_playlist_name)

        with allure.step("Поиск и добавление песни '{song_to_add}'"):
            library_page.add_song_to_playlist(song_to_add)

        with allure.step("Проверка, что песня добавлена в плейлист"):
            library_page.should_have_song_in_playlist(song_to_add)

        with allure.step("Очистка: Удаление тестового плейлиста"):
            library_page.delete_playlist(new_playlist_name)