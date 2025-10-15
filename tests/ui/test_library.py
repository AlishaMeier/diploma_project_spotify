import pytest
import allure
from spotify_project.pages.login_page import LoginPage
from spotify_project.pages.library_page import LibraryPage


@allure.epic("UI-тестирование")
@allure.feature("Библиотека и Плейлисты")
class TestPlaylistCRUD:

    @allure.story("Полный цикл: Создание плейлиста с дефолтным именем и удаление")
    @allure.tag("positive", "CRUD", "cleanup")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_successful_playlist_creation_and_deletion(self, credentials, login_page: LoginPage,
                                                       library_page: LibraryPage):
        # 1. Arrange: Авторизация и навигация
        with allure.step("1. Успешная авторизация"):
            login_page.open().login(credentials["username"], credentials["password"]).should_be_logged_in()


            # 2. Act (Создание)
        with allure.step("3. Нажатие на плитку 'Create playlist'"):
            # Метод создает плейлист и возвращает его динамическое имя
            playlist_name = library_page.create_playlist_via_tile()

        # 3. Assert (Проверка создания)
        with allure.step(f"4. Проверка, что создан плейлист с именем '{playlist_name}'"):
            library_page.should_be_on_playlist_page_with_name(playlist_name)

        # 4. Cleanup (Удаление)
        with allure.step(f"5. Очистка: Удаление тестового плейлиста '{playlist_name}'"):
            # Используем полученное динамическое имя для надежного удаления
            library_page.delete_playlist(playlist_name)

        # 5. Final Assert (Проверка удаления)
        with allure.step("6. Проверка, что плейлист успешно удален из списка"):
            library_page.should_not_have_playlist_in_list(playlist_name)