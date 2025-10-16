from selene import browser, be, have
import allure
from selene.core.entity import Element


class LoginPage:

    username_input: Element = browser.element('[data-testid="login-username"]')
    PRIMARY_ACTION_BUTTON: Element = browser.element('[data-testid="login-button"]')
    switch_to_password_button: Element = browser.element("//button[contains(text(), 'Войти с помощью пароля')]")
    password_input: Element = browser.element('#password')
    ACTUAL_USERNAME_TEXT: Element = browser.element('//div[text()="Alisha"]')
    PROFILE_ICON: Element = browser.element("[data-testid='user-widget-link']")
    ERROR_VALIDATION_CONTAINER: Element = browser.element('[data-testid="username-error"]')
    ERROR_VALIDATION_TEXT: Element = ERROR_VALIDATION_CONTAINER.element('.e-91132-form-help-text__text')
    ERROR_BANNER_PASSWORD_SCREEN: Element = browser.element('div[role="alert"]').element('.e-91132-banner__message')


    @allure.step("Ввод имени пользователя и нажатие 'Продолжить'")
    def enter_username_and_continue(self, username):
        """Выполняет ввод username и клик по PRIMARY_ACTION_BUTTON, оставаясь на первом экране."""
        self.username_input.should(be.visible).type(username)
        self.PRIMARY_ACTION_BUTTON.click()
        return self

    @allure.step("Ввод имени пользователя и переход к паролю")
    def enter_username_and_switch_to_password(self, username):
        """
        Выполняет Шаг 1 и Шаг 2 (переключение с кода на пароль).
        Используется ТОЛЬКО для ПОЗИТИВНОГО СЦЕНАРИЯ.
        """
        self.username_input.should(be.visible).type(username)
        self.PRIMARY_ACTION_BUTTON.click()

        with allure.step("Переключение на авторизацию по паролю"):
            self.switch_to_password_button.should(be.visible).click()
        return self

    @allure.step("Ввод пароля и нажатие 'Войти'")
    def enter_password_and_login(self, password):
        """Выполняет Шаг 3: ввод пароля и финальный клик."""
        self.password_input.should(be.visible).type(password)
        self.PRIMARY_ACTION_BUTTON.click()
        return self

    @allure.step("Полная авторизация пользователя")
    def login(self, username, password):
        """Комбинирует шаги для выполнения полной авторизации."""
        self.enter_username_and_switch_to_password(username)
        self.enter_password_and_login(password)
        return self

    @allure.step("Попытка отправки формы без заполнения username")
    def attempt_to_continue_with_empty_username(self):
        """Нажимает 'Continue', не заполняя username, для проверки валидации."""
        self.PRIMARY_ACTION_BUTTON.should(be.visible).click()
        return self

    @allure.step("Проверяем, что пользователь успешно залогинен")
    def should_be_logged_in(self, expected_user_name="Alisha"):
        """Проверяет успешный вход, ожидая появления элементов на главной странице Web Player."""

        with allure.step("1. Проверяем наличие иконки профиля с именем пользователя"):
            # Проверяем, что иконка видна И что её атрибут 'aria-label' совпадает с именем пользователя
            self.PROFILE_ICON.should(be.visible).should(have.attribute('aria-label', expected_user_name))
        return self

    @allure.step("Проверяем отображение сообщения об ошибке password")
    def should_see_error_message_password(self, expected_error_text):
        self.ERROR_BANNER_PASSWORD_SCREEN.should(be.visible).should(have.text(expected_error_text))
        return self

    @allure.step("Проверяем отображение сообщения об ошибке email")
    def should_see_error_message_email(self, expected_error_text):
        self.ERROR_VALIDATION_CONTAINER.should(be.visible)
        self.ERROR_VALIDATION_TEXT.should(have.text(expected_error_text))
        return self

    @allure.step("Проверяем наличие валидационного сообщения для полей")
    def should_see_field_required_error(self, expected_error_text):
        """Проверяет наличие ошибки 'Поле обязательно'."""
        self.ERROR_VALIDATION_CONTAINER.should(be.visible)
        self.ERROR_VALIDATION_TEXT.should(have.text(expected_error_text))
        return self