import pytest
import allure
from spotify_project.pages.web.login_page import LoginPage
from spotify_project.pages.web.navigation_page import NavigationPage

ERROR_NOT_LINKED = "Адрес электронной почты или имя пользователя не связаны с аккаунтом Spotify" or "Адрес электронной почты или имя пользователя не привязаны к аккаунту Spotify"
ERROR_INVALID_CREDS = "Неправильное имя пользователя или пароль."
ERROR_REQUIRED_FIELD = "Введите имя пользователя или адрес электронной почты из аккаунта Spotify."

INVALID_LOGIN_DATA = [
    ("no_at_sign.com", "любой_пароль", ERROR_NOT_LINKED)
]

@allure.feature("Авторизация")
@allure.story("Тест на успешную авторизацию")
@allure.label("owner", "AlishaMeier")
@allure.tag("positive", "critical")
@allure.severity(allure.severity_level.CRITICAL)
def test_login(credentials, login_page: LoginPage, navigation_page: NavigationPage):
    with allure.step("Переход на страницу авторизации с главной"):
        navigation_page.navigate_to_login()
    with allure.step("Выполнение полной авторизации"):
        login_page.login(credentials["username"], credentials["password"])
    with allure.step("Проверка успешного входа"):
        login_page.should_be_logged_in()


@allure.feature("Авторизация")
@allure.story("Негативная авторизация: неверный пароль")
@allure.label("owner", "AlishaMeier")
@allure.tag("negative", "login_creds")
@allure.severity(allure.severity_level.NORMAL)
def test_invalid_password(credentials, login_page: LoginPage, navigation_page: NavigationPage):
    valid_username = credentials["username"]
    wrong_password = "wrong_password_123"

    with allure.step("Переход на страницу авторизации"):
        navigation_page.navigate_to_login()
    with allure.step("Выполняем полную авторизацию с НЕВЕРНЫМ паролем"):
        login_page.login(valid_username, wrong_password)
    with allure.step("Проверить отображение системной ошибки"):
        login_page.should_see_error_message(ERROR_INVALID_CREDS)

@allure.feature("Авторизация")
@allure.story("Негативная авторизация: пустые поля")
@allure.label("owner", "AlishaMeier")
@allure.tag("negative", "UI_validation")
@allure.severity(allure.severity_level.MINOR)
def test_login_with_empty_fields(login_page: LoginPage, navigation_page: NavigationPage):
    with allure.step("Переход на страницу авторизации"):
        navigation_page.navigate_to_login()
    with allure.step("Нажать кнопку 'Continue', оставив поле пустым"):
        login_page.attempt_to_continue_with_empty_username()
    with allure.step("Проверить отображение сообщений о необходимости заполнения"):
        login_page.should_see_error_message(ERROR_REQUIRED_FIELD)


@allure.feature("Авторизация")
@allure.story("Негативная авторизация: невалидные данные")
@allure.label("owner", "AlishaMeier")
@allure.tag("negative", "UI_validation")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.parametrize(
    "username, password, expected_error", INVALID_LOGIN_DATA
)
def test_invalid_login_with_parameters(username, password, expected_error, login_page: LoginPage,
                                       navigation_page: NavigationPage):
    with allure.step("Переход на страницу авторизации"):
        navigation_page.navigate_to_login()
    with allure.step("Ввести логин и нажать 'Продолжить': {username}"):
        login_page.enter_username_and_continue(username)
    with allure.step("Проверить отображение сообщения об ошибке: '{expected_error}'"):
        login_page.should_see_error_message(expected_error)