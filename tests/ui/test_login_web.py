import pytest
import allure
from spotify_project.pages.login_page import LoginPage
from spotify_project.pages.navigation_page import NavigationPage
from selene import browser
from spotify_project.data.login_data import LoginData


@pytest.mark.ui
@allure.feature("Авторизация")
@allure.label("owner", "AlishaMeier")
class TestLogin:

    @allure.story("Тест на успешную авторизацию")
    @allure.tag("positive", "critical")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login(self, credentials, login_page: LoginPage, navigation_page: NavigationPage):
        navigation_page.open_main_page()
        navigation_page.navigate_to_login()
        current_url = browser.driver.current_url
        print(f"DEBUG: Current URL after navigate_to_login: {current_url}")

        login_page.login(credentials["username"], credentials["password"])
        login_page.should_be_logged_in(credentials["expected_name"])

    @allure.story("Негативная авторизация: неверный пароль")
    @allure.tag("negative", "login_creds")
    @allure.severity(allure.severity_level.NORMAL)
    def test_invalid_password(self, login_page: LoginPage, navigation_page: NavigationPage):
        valid_username = LoginData.VALID_USERNAME
        wrong_password = LoginData.WRONG_PASSWORD

        navigation_page.open_main_page()
        navigation_page.navigate_to_login()
        login_page.login(valid_username, wrong_password)
        login_page.should_see_invalid_creds_error()

    @allure.story("Негативная авторизация: пустые поля")
    @allure.tag("negative", "UI_validation")
    @allure.severity(allure.severity_level.MINOR)
    def test_login_with_empty_fields(self, login_page: LoginPage, navigation_page: NavigationPage):
        navigation_page.open_main_page()
        navigation_page.navigate_to_login()
        login_page.attempt_to_continue_with_empty_username()
        login_page.should_see_required_field_error()

    @allure.story("Негативная авторизация: невалидные данные")
    @allure.tag("negative", "UI_validation")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize(
        "username, password",
        [(LoginData.NOT_LINKED_USERNAME, LoginData.NOT_LINKED_PASSWORD)]
    )
    def test_invalid_login_with_parameters(self, username, password,
                                           login_page: LoginPage,
                                           navigation_page: NavigationPage):
        navigation_page.open_main_page()
        navigation_page.navigate_to_login()
        login_page.enter_username_and_continue(username)
        login_page.should_see_not_linked_error()