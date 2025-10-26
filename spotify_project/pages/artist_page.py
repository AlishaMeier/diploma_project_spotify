from selene import browser, have, be
import allure
from selene.core.entity import Element
import logging

logger = logging.getLogger(__name__)


class ArtistPage:

    artist_name_title: Element = browser.element('[data-testid="entityTitle"] h1')

    @allure.step("Проверить, что открылась страница артиста '{artist_name}'")
    def should_be_on_artist_page(self, artist_name: str):

        try:
            browser.should(have.url_containing('/artist/'), timeout=10)
        except Exception as e:
            logger.error(f"Не дождались URL, содержащего '/artist/': {e}")
            allure.attach(
                browser.driver.get_screenshot_as_png(),
                name="screenshot_on_url_fail",
                attachment_type=allure.attachment_type.PNG
            )

        self.artist_name_title.should(be.visible).should(have.text(artist_name))

        return self