from selene import browser, be, have
from selene.core.entity import Element
import allure
import logging

logger = logging.getLogger(__name__)

class NavigationPage:
    LOGIN_BUTTON_NAV: Element = browser.element("[data-testid='login-button']")
    HOME_BUTTON_NAV: Element = browser.element('[data-testid="home-button"]')
    COOKIE_REJECT_BUTTON = browser.element('#onetrust-reject-all-handler')

    @allure.step("Открыть главную страницу и закрыть баннер cookie")
    def open_main_page(self):
        browser.open("/")

        try:
            if self.COOKIE_REJECT_BUTTON.with_(timeout=5).wait_until(be.visible):
                self.COOKIE_REJECT_BUTTON.click()
                logger.info("Cookie-баннер нажат.")
        except Exception as e:
            # Если баннера нет, то залогируем
            logger.warning(f"Баннер cookie не найден или не нажат: {e}")

        return self

    @allure.step("Переход на страницу авторизации через кнопку в навбаре")
    def navigate_to_login(self):
        self.LOGIN_BUTTON_NAV.should(be.visible).click()
        return self

    @allure.step("Возвращение на главную страницу")
    def return_to_home_page(self):
        self.HOME_BUTTON_NAV.should(be.visible).click()
        return self