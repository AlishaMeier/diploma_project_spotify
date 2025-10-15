from selene import browser, be, have
import allure
from selene.core.entity import Element
from selene.support.conditions import have
from selene.support.conditions import be


class LoginPage:
    # --- Селекторы элементов ---
    # NOTE: Используйте более специфичные селекторы, если Spotify их предоставляет
    URL = "/login"

    # Элементы формы
    username_input: Element = browser.element('#login-username')  # Уточненный ID или специфичный селектор
    password_input: Element = browser.element('#login-password')  # Уточненный ID или специфичный селектор
    login_button: Element = browser.element('#login-button')  # Уточненный ID или специфичный селектор

    # Элементы для проверок
    error_message_box: Element = browser.element(
        '.Alert-module-error')  # Селектор для системной ошибки (невалидные креды)

    # Селекторы для проверки валидации полей (зависит от конкретной реализации Spotify)
    # Предполагаем, что под полем появляется текст ошибки
    field_validation_error: Element = browser.element('.Text-module-error-message')

    # Элемент на главной странице, который подтверждает вход (требует уточнения)
    profile_name_element: Element = browser.element('.profile-name')

    # --- Методы действий (Act) ---

    @allure.step("Открываем страницу авторизации")
    def open(self):
        """Открывает страницу входа, используя base_url из конфигурации."""
        browser.open(self.URL)
        return self

    @allure.step("Ввод учетных данных и нажатие кнопки 'Войти'")
    def login(self, username, password):
        """Выполняет ввод логина/пароля и клик по кнопке."""
        # Selene не требует явных ожиданий, т.к. они встроены в .type()
        self.username_input.type(username)
        self.password_input.type(password)
        self.login_button.click()
        return self

    @allure.step("Отправка пустой формы")
    def submit_empty_form(self):
        """Нажимает 'Войти', не заполняя поля."""
        self.login_button.click()
        return self

    # --- Методы проверок (Assert) ---

    @allure.step("Проверяем, что пользователь успешно залогинен")
    def should_be_logged_in(self, expected_user_name="test_user"):
        """Проверяет успешный редирект и наличие элемента профиля."""

        # 1. Проверяем, что мы не на странице логина
        browser.should(have.no.url_containing(self.URL))

        # 2. Проверяем наличие элемента профиля на главной странице
        self.profile_name_element.should(be.visible)

        # 3. (Опционально) Проверяем имя пользователя
        self.profile_name_element.should(have.text(expected_user_name))
        return self

    @allure.step("Проверяем отображение системного сообщения об ошибке")
    def should_see_error_message(self, expected_error_text):
        """Проверяет ошибку при невалидных учетных данных."""
        # Ждем, пока сообщение об ошибке появится
        self.error_message_box.should(be.visible)

        # Проверяем, что текст сообщения соответствует ожидаемому
        self.error_message_box.should(have.text(expected_error_text))
        return self

    @allure.step("Проверяем наличие валидационного сообщения для полей")
    def should_see_field_required_error(self, expected_error_text):
        """
        Проверяет наличие ошибки 'Поле обязательно'
        (для сценария с пустыми полями).
        """
        # Ищем элемент, содержащий текст валидационной ошибки
        browser.element(self.field_validation_error.with_(text=expected_error_text)).should(be.visible)
        return self