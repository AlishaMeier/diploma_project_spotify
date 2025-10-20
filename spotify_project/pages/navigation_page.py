from selene import browser, be, have
from selene.core.entity import Element
import allure


class NavigationPage:
    LOGIN_BUTTON_NAV: Element = browser.element("[data-testid='login-button']")
    HOME_BUTTON_NAV: Element = browser.element('[data-testid="home-button"]')

    @allure.step("Переход на страницу авторизации через кнопку в навбаре")
    def navigate_to_login(self):
        with allure.step("Клик по кнопке 'Войти"):
            self.LOGIN_BUTTON_NAV.should(be.visible).click()
        return self

    @allure.step("Возвращение на главную страницу")
    def return_to_home_page(self):
        self.HOME_BUTTON_NAV.should(be.visible).click()
        return self