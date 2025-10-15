import pytest
import allure
from spotify_project.pages.login_page import LoginPage

@allure.feature("Авторизация")
@allure.story("Тест на успешную авторизацию")
def test_login(credentials, login_page):
    login_page.open()
    login_page.login(credentials["username"], credentials["password"])
    login_page.should_be_logged_in()
