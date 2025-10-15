from selene import browser, be, have
import allure
from selene.core.entity import Element


class LoginPage:


    username_input: Element = browser.element('#username')
    PRIMARY_ACTION_BUTTON: Element = browser.element("button[class*='e-91132-button-primary']")
    switch_to_password_button: Element = browser.element("button[class*='Button-sc-1dqy6lx-0']")

    password_input: Element = browser.element('#password')


    LOGGED_IN_TITLE: Element = browser.element('//div[@data-testid="user-info"]//h2')
    ACTUAL_USERNAME_TEXT: Element = browser.element('//div[text()="Alisha"]')
    WEB_PLAYER_LINK: Element = browser.element("[data-testid='web-player-link']")

    ERROR_VALIDATION_CONTAINER: Element = browser.element('[data-testid="username-error"]')
    ERROR_VALIDATION_TEXT: Element = ERROR_VALIDATION_CONTAINER.element('.e-91132-form-help-text__text')



    @allure.step("Ввод имени пользователя и нажатие 'Продолжить'")
    def enter_username_and_continue(self, username):  # <<< НОВЫЙ МЕТОД ДЛЯ НЕГАТИВНЫХ ТЕСТОВ
        """Выполняет ввод username и клик по PRIMARY_ACTION_BUTTON, оставаясь на первом экране."""
        self.username_input.should(be.visible).type(username)
        self.PRIMARY_ACTION_BUTTON.click()
        return self

    @allure.step("Ввод имени пользователя и переход к паролю")
    def enter_username_and_switch_to_password(self, username):
        """
        Выполняет Шаг 1 (ввод username) и Шаг 2 (переключение с кода на пароль).
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



    @allure.step("Проверяем, что пользователь успешно залогинен и переходим в Web Player")
    def should_be_logged_in(self, expected_user_name="Alisha"):
        """Проверяет успешный вход, ища элементы на странице подтверждения и переходит в основной интерфейс."""
        with allure.step("1. Проверяем наличие заголовка 'Выполнен вход'"):
            self.LOGGED_IN_TITLE.should(be.visible).should(have.text("Выполнен вход"))

        with allure.step(f"2. Проверяем, что отображается имя пользователя '{expected_user_name}'"):
            browser.element(f'//div[text()="{expected_user_name}"]').should(be.visible)

        with allure.step("3. Переход в Web Player"):
            self.WEB_PLAYER_LINK.should(be.visible).click()

        browser.element("[data-testid='home-page-title']").should(be.visible)
        return self

    @allure.step("Проверяем отображение системного сообщения об ошибке")
    def should_see_error_message(self, expected_error_text):
        """Проверяет ошибку при невалидных учетных данных."""
        self.ERROR_VALIDATION_CONTAINER.should(be.visible)
        self.ERROR_VALIDATION_TEXT.should(have.text(expected_error_text))
        return self

    @allure.step("Проверяем наличие валидационного сообщения для полей")
    def should_see_field_required_error(self, expected_error_text):
        """Проверяет наличие ошибки 'Поле обязательно'."""
        self.ERROR_VALIDATION_CONTAINER.should(be.visible)
        self.ERROR_VALIDATION_TEXT.should(have.text(expected_error_text))
        return self