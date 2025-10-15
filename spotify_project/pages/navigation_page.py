from selene import browser, be, have
from selene.core.entity import Element
import allure


class NavigationPage:
    """Содержит общие элементы навигации (шапка, боковая панель)."""

    LOGIN_BUTTON_NAV: Element = browser.element("[data-testid='login-button']")

    @allure.step("Переход на страницу авторизации через кнопку в навбаре")
    def navigate_to_login(self):
        """Кликает на кнопку Log In в шапке."""

        with allure.step("Клик по кнопке 'Log In'"):
            self.LOGIN_BUTTON_NAV.should(be.visible).click()

        # !!! УДАЛЕНА ПРОВЕРКА URL !!!

        return self