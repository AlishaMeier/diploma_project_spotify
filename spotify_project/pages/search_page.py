from selene import browser, have, be
import allure
from selene.core.entity import Element


class SearchPage:
    search_input_navbar: Element = browser.element('[data-testid="search-input"]')

    top_result_card: Element = browser.element('[data-testid="top-result-card"]')
    top_result_title: Element = top_result_card.element('div[data-encore-id="text"]')
    top_result_cover_art: Element = top_result_card.element('img[data-testid="card-image"]')
    top_result_artist: Element = top_result_card.element('a[href*="/artist/"]')
    top_result_subtitle_container: Element = top_result_card.element('a + div[data-encore-id="text"]')

    no_results_message: Element = browser.element('[data-testid="no-results-message"]')

    filter_button_tracks: Element = browser.element('//button[.//span[text()="Треки"]]')
    filter_button_albums: Element = browser.element('//button[.//span[text()="Альбомы"]]')
    filter_button_artists: Element = browser.element('//button[.//span[text()="Исполнители"]]')
    filter_button_playlists: Element = browser.element('//button[.//span[text()="Плейлисты"]]')
    filter_button_podcasts: Element = browser.element('//button[.//span[text()="Подкасты и шоу"]]')

    main_results_section: Element = browser.element('[data-testid="grid-container"]')
    first_main_result_title: Element = main_results_section.element('p[data-encore-id="cardTitle"]')
    first_main_result_subtitle: Element = main_results_section.element('div[data-encore-id="cardSubtitle"]')

    @allure.step("Выполнение поиска с главной страницы: '{query}'")
    def search_from_main_page(self, query: str):
        self.search_input_navbar.should(be.visible).type(query).press_enter()
        return self

    @allure.step("Проверка, что топ-результат имеет заголовок '{expected_title}'")
    def should_have_top_result_with_title(self, expected_title: str):
        self.top_result_title.should(be.visible).should(have.text(expected_title))
        return self

    @allure.step("Проверка, что топ-результат - это карточка артиста '{artist_name}'")
    def should_have_top_result_as_artist(self, artist_name: str):
        self.should_have_top_result_with_title(artist_name)
        # Проверяем, что внутри карточки есть ссылка на артиста (как было в тесте)
        self.top_result_card.element('a[href*="/artist/"]').should(be.visible)
        return self

    @allure.step("Кликнуть по карточке топ-результата")
    def click_top_result_card(self):
        self.top_result_card.click()

    @allure.step("Проверка отображения сообщения: '{message_text}'")
    def should_see_message(self, message_text: str):
        browser.element(f"//*[contains(., '{message_text}')]").should(be.visible)
        return self

    @allure.step("Нажатие на фильтр: {filter_element}")
    def click_filter_button(self, filter_element: Element):
        filter_element.should(be.visible).click()
        self.main_results_section.should(be.visible)
        return self

    @allure.step(
        "Проверка первого основного результата: заголовок '{expected_title}', подзаголовок '{expected_subtitle}'")
    def should_have_first_main_result(self, expected_title: str, expected_subtitle: str):
        self.first_main_result_title.should(be.visible).should(have.text(expected_title))
        self.first_main_result_subtitle.should(be.visible).should(have.text(expected_subtitle))
        return self

    @allure.step("Проверка, что топ-результат - это альбом с обложкой, типом 'Album' и исполнителем '{artist_name}'")
    def should_have_top_result_as_album(self, artist_name: str):
        self.top_result_card.should(be.visible)
        self.top_result_cover_art.should(be.visible)
        self.top_result_subtitle_container.should(be.visible)
        self.top_result_subtitle_container.element('span').should(have.text("Альбом"))
        self.top_result_subtitle_container.element('a').should(have.text(artist_name))
        return self

    @allure.step("Проверка, что у топ-результата есть обложка и подзаголовок содержит '{expected_text}'")
    def should_have_top_result_card_details(self, expected_text: str):
        self.top_result_card.should(be.visible)
        self.top_result_cover_art.should(be.visible)
        self.top_result_subtitle_container.should(be.visible).should(have.text(expected_text))
        return self