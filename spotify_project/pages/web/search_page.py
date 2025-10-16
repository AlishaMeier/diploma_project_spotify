from selene import browser, have, be
import allure
from selene.core.entity import Element


class SearchPage:
    SEARCH_INPUT_NAVBAR: Element = browser.element('[data-testid="search-input"]')
    TOP_RESULT_CARD: Element = browser.element('[data-testid="top-result-card"]')
    TOP_RESULT_TITLE: Element = TOP_RESULT_CARD.element('div[data-encore-id="text"]')
    TOP_RESULT_COVER_ART: Element = TOP_RESULT_CARD.element('img[data-testid="card-image"]')
    TOP_RESULT_ARTIST: Element = TOP_RESULT_CARD.element('a[href*="/artist/"]')
    NO_RESULTS_MESSAGE: Element = browser.element('[data-testid="no-results-message"]')


    @allure.step("Выполнение поиска с главной страницы: '{query}'")
    def search_from_main_page(self, query: str):
        self.SEARCH_INPUT_NAVBAR.should(be.visible).type(query).press_enter()
        return self

    @allure.step("Проверка, что топ-результат имеет заголовок '{expected_title}'")
    def should_have_top_result_with_title(self, expected_title: str):
        """
        Проверяет, что заголовок в карточке "Top result" соответствует исправленному запросу.
        """
        self.TOP_RESULT_TITLE.should(be.visible).should(have.text(expected_title))
        return self

    @allure.step("Проверка, что у топ-результата есть обложка и исполнитель")
    def should_have_top_result_details(self, artist_name: str):
        self.TOP_RESULT_CARD.should(be.visible)
        self.TOP_RESULT_COVER_ART.should(be.visible)
        self.TOP_RESULT_ARTIST.should(be.visible).should(have.text(artist_name))
        return self

    @allure.step("Проверка отображения сообщения: '{message_text}'")
    def should_see_message(self, message_text: str):
        browser.element(f"//*[contains(., '{message_text}')]").should(be.visible)
        return self