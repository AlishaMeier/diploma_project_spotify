import pytest
import allure
from spotify_project.pages.login_page import LoginPage

INVALID_LOGIN_DATA = [
    ("wrong@email.com", "any_password", "Неверное имя пользователя или пароль."),
    ("valid@spotify.com", "wrong_password", "Неверное имя пользователя или пароль."),
    ("no_at_sign.com", "any_password", "Введите действительный адрес электронной почты."),
]

@allure.feature("Авторизация")
@allure.story("Тест на успешную авторизацию")
@allure.tag("positive", "critical")
@allure.severity(allure.severity_level.CRITICAL)
def test_login(credentials, login_page):
    login_page.open()
    login_page.login(credentials["username"], credentials["password"])
    login_page.should_be_logged_in()


@allure.feature("Авторизация")
@allure.story("Негативная авторизация: невалидные данные")
@allure.tag("negative", "parametrize")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.parametrize(
    "username, password, expected_error", INVALID_LOGIN_DATA
)
def test_invalid_login_with_parameters(username, password, expected_error, login_page):
    """Тест проверяет отображение ошибки при вводе невалидных учетных данных."""
    with allure.step(f"1. Открыть страницу авторизации"):
        login_page.open()

    with allure.step(f"2. Попытаться авторизоваться с логином: {username}"):
        # NOTE: В методе login не должно быть проверки, только действие (Act)
        login_page.login(username, password)

    with allure.step(f"3. Проверить отображение сообщения об ошибке: '{expected_error}'"):
        # ASSURE: Проверка, что на странице появилось ожидаемое сообщение об ошибке
        login_page.should_see_error_message(expected_error)


@allure.feature("Авторизация")
@allure.story("Негативная авторизация: пустые поля")
@allure.tag("negative", "UI_validation")
@allure.severity(allure.severity_level.MINOR)
def test_login_with_empty_fields(login_page):
    """Тест проверяет сообщение об ошибке при отправке пустой формы."""
    with allure.step("1. Открыть страницу авторизации"):
        login_page.open()

    with allure.step("2. Нажать кнопку 'Войти', оставив поля пустыми"):
        # Кликаем по кнопке без ввода данных
        login_page.submit_empty_form()

    with allure.step("3. Проверить отображение сообщений о необходимости заполнения"):
        # Появилось ли валидационное сообщение для логина
        login_page.should_see_field_required_error("Введите имя пользователя Spotify.")
        # И для пароля (если это требуется)
        login_page.should_see_field_required_error("Введите пароль.")
