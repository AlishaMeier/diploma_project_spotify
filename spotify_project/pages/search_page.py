from selene import browser, have, be
import allure
from selene.core.entity import Element


class SearchPage:
    SEARCH_INPUT_NAVBAR: Element = browser.element('[data-testid="search-input"]')

    TOP_RESULT_CARD: Element = browser.element('[data-testid="top-result-card"]')
    TOP_RESULT_TITLE: Element = TOP_RESULT_CARD.element('div[data-encore-id="text"]')
    TOP_RESULT_COVER_ART: Element = TOP_RESULT_CARD.element('img[data-testid="card-image"]')
    TOP_RESULT_ARTIST: Element = TOP_RESULT_CARD.element('a[href*="/artist/"]')
    TOP_RESULT_SUBTITLE_CONTAINER: Element = TOP_RESULT_CARD.element('a + div[data-encore-id="text"]')

    NO_RESULTS_MESSAGE: Element = browser.element('[data-testid="no-results-message"]')

    FILTER_BUTTON_TRACKS: Element = browser.element('//button[.//span[text()="Треки"]]')
    FILTER_BUTTON_ALBUMS: Element = browser.element('//button[.//span[text()="Альбомы"]]')
    FILTER_BUTTON_ARTISTS: Element = browser.element('//button[.//span[text()="Исполнители"]]')
    FILTER_BUTTON_PLAYLISTS: Element = browser.element('//button[.//span[text()="Плейлисты"]]')
    FILTER_BUTTON_PODCASTS: Element = browser.element('//button[.//span[text()="Подкасты и шоу"]]')

    MAIN_RESULTS_SECTION: Element = browser.element('[data-testid="grid-container"]')
    FIRST_MAIN_RESULT_TITLE: Element = MAIN_RESULTS_SECTION.element('p[data-encore-id="cardTitle"]')
    FIRST_MAIN_RESULT_SUBTITLE: Element = MAIN_RESULTS_SECTION.element('div[data-encore-id="cardSubtitle"]')

    @allure.step("Выполнение поиска с главной страницы: '{query}'")
    def search_from_main_page(self, query: str):
        self.SEARCH_INPUT_NAVBAR.should(be.visible).type(query).press_enter()
        return self

    @allure.step("Проверка, что топ-результат имеет заголовок '{expected_title}'")
    def should_have_top_result_with_title(self, expected_title: str):
        self.TOP_RESULT_TITLE.should(be.visible).should(have.text(expected_title))
        return self

    @allure.step("Проверка отображения сообщения: '{message_text}'")
    def should_see_message(self, message_text: str):
        browser.element(f"//*[contains(., '{message_text}')]").should(be.visible)
        return self

    @allure.step("Нажатие на фильтр: {filter_element}")
    def click_filter_button(self, filter_element: Element):
        filter_element.should(be.visible).click()
        self.MAIN_RESULTS_SECTION.should(be.visible)
        return self

    @allure.step("Проверка первого основного результата: заголовок '{expected_title}', подзаголовок '{expected_subtitle}'")
    def should_have_first_main_result(self, expected_title: str, expected_subtitle: str):
        self.FIRST_MAIN_RESULT_TITLE.should(be.visible).should(have.text(expected_title))
        self.FIRST_MAIN_RESULT_SUBTITLE.should(be.visible).should(have.text(expected_subtitle))
        return self

    @allure.step("Проверка, что топ-результат - это альбом с обложкой, типом 'Album' и исполнителем '{artist_name}'")
    def should_have_top_result_as_album(self, artist_name: str):
        self.TOP_RESULT_CARD.should(be.visible)
        self.TOP_RESULT_COVER_ART.should(be.visible)
        self.TOP_RESULT_SUBTITLE_CONTAINER.should(be.visible)
        self.TOP_RESULT_SUBTITLE_CONTAINER.element('span').should(have.text("Альбом"))
        self.TOP_RESULT_SUBTITLE_CONTAINER.element('a').should(have.text(artist_name))
        return self

    @allure.step("Проверка, что у топ-результата есть обложка и подзаголовок содержит '{expected_text}'")
    def should_have_top_result_card_details(self, expected_text: str):
        self.TOP_RESULT_CARD.should(be.visible)
        self.TOP_RESULT_COVER_ART.should(be.visible)
        self.TOP_RESULT_SUBTITLE_CONTAINER.should(be.visible).should(have.text(expected_text))
        return self