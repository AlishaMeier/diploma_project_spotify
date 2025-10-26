from selene import browser, be, have
import allure
from selene.core.entity import Element


class LoginPage:
    username_input: Element = browser.element('[data-testid="login-username"]')
    password_input: Element = browser.element('[data-testid="login-password"]')
    PRIMARY_ACTION_BUTTON: Element = browser.element('[data-testid="login-button"]')
    switch_to_password_button: Element = browser.element('[data-encore-id="buttonTertiary"]')
    PROFILE_ICON: Element = browser.element("[data-testid='user-widget-link']")

    ERROR_NOT_LINKED_TEXT = "Адрес электронной почты или имя пользователя не связаны с аккаунтом Spotify"
    ERROR_NOT_LINKED_TEXT_ALT = "Адрес электронной почты или имя пользователя не привязаны к аккаунту Spotify"
    ERROR_INVALID_CREDS_TEXT = "Неправильное имя пользователя или пароль."
    ERROR_REQUIRED_FIELD_TEXT = "Введите имя пользователя или адрес электронной почты из аккаунта Spotify."

    @allure.step("Ввод имени пользователя и нажатие 'Продолжить'")
    def enter_username_and_continue(self, username):
        self.username_input.should(be.visible).type(username)
        self.PRIMARY_ACTION_BUTTON.click()
        return self

    @allure.step("Ввод имени пользователя и переход к паролю")
    def enter_username_and_switch_to_password(self, username):
        self.username_input.should(be.visible).type(username)
        self.PRIMARY_ACTION_BUTTON.click()

        with allure.step("Переключение на авторизацию по паролю"):
            self.switch_to_password_button.should(be.visible).click()
        return self

    @allure.step("Ввод пароля и нажатие 'Войти'")
    def enter_password_and_login(self, password):
        self.password_input.should(be.visible).type(password)
        self.PRIMARY_ACTION_BUTTON.click()
        return self

    @allure.step("Полная авторизация пользователя")
    def login(self, username, password):
        self.enter_username_and_switch_to_password(username)
        self.enter_password_and_login(password)
        return self

    @allure.step("Попытка отправки формы без заполнения username")
    def attempt_to_continue_with_empty_username(self):
        self.PRIMARY_ACTION_BUTTON.should(be.visible).click()
        return self

    @allure.step("Проверяем, что пользователь успешно залогинен")
    def should_be_logged_in(self, expected_user_name: str):
        with allure.step(f"Проверяем наличие иконки профиля с именем: {expected_user_name}"):
            self.PROFILE_ICON.should(be.visible).should(have.attribute('aria-label').value(expected_user_name))
        return self

    @allure.step("Проверяем отображение общего сообщения об ошибке: 'Неправильное имя...'")
    def should_see_invalid_creds_error(self):
        error_element = browser.element('[data-encore-id="banner"] span')
        error_element.should(be.visible).should(have.text(self.ERROR_INVALID_CREDS_TEXT))
        return self

    @allure.step("Проверяем отображение ошибки ПОД ПОЛЕМ: 'Обязательное поле'")
    def should_see_required_field_error(self):
        error_element = browser.element('[data-testid="username-error"] span')
        error_element.should(be.visible).should(have.text(self.ERROR_REQUIRED_FIELD_TEXT))
        return self

    @allure.step("Проверяем отображение ошибки ПОД ПОЛЕМ: 'Не связано с аккаунтом'")
    def should_see_not_linked_error(self):
        error_element = browser.element('[data-testid="username-error"] span')
        error_element.should(be.visible).should(have.any_text(
            self.ERROR_NOT_LINKED_TEXT,
            self.ERROR_NOT_LINKED_TEXT_ALT
        ))
        return self