from selene import browser, be, have
import allure

class LoginPage:
    def __init__(self):
        self.url = "/login"
        self.username_input = browser.element('[name="username"]')
        self.password_input = browser.element('[name="password"]')
        self.login_button = browser.element('[type="submit"]')

    @allure.step("Открываем страницу логина")
    def open(self):
        browser.open(self.url)

    @allure.step("Вводим имя пользователя и пароль")
    def login(self, username, password):
        self.username_input.type(username)
        self.password_input.type(password)
        self.login_button.click()

    @allure.step("Проверяем, что пользователь залогинен")
    def should_be_logged_in(self):
        browser.element('.profile-name').should(have.text("test_user"))
