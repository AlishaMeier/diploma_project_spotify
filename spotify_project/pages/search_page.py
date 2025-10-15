from selene import browser, have, be
import allure
from selene.core.entity import Element
from selene.support.conditions import have


class SearchPage:
    NAV_SEARCH_ICON: Element = browser.element('[data-testid="nav-link-search"]')
    SEARCH_INPUT_FIELD: Element = browser.element('[data-testid="search-input"]')

    # Элементы на странице результатов
    PLAYLIST_SECTION_TITLE: Element = browser.element('h2').with_(text='Playlists')
    NO_RESULTS_MESSAGE: Element = browser.element('[data-testid="no-results-message"]')

    # Селектор для первой найденной песни/трека
    FIRST_TRACK_RESULT: Element = browser.element('[data-testid="track-row"] a')


    @allure.step("Переход на страницу поиска")
    def open_search_page(self):
        """Переход на вкладку поиска, если она не открыта."""
        self.NAV_SEARCH_ICON.should(be.visible).click()
        self.SEARCH_INPUT_FIELD.should(be.visible)
        return self

    @allure.step("Ввод поискового запроса: {query}")
    def type_search_query(self, query: str):
        """Вводит текст в поле поиска. В Spotify результаты появляются динамически."""
        self.SEARCH_INPUT_FIELD.type(query)
        return self


    @allure.step("Проверка, что результаты поиска отображаются (секция Playlists)")
    def should_show_results(self):
        """Проверяет наличие заголовка секции 'Playlists' (для позитивного поиска)."""
        self.PLAYLIST_SECTION_TITLE.should(be.visible).should(have.text('Playlists'))
        return self

    @allure.step("Проверка наличия искомого текста в первом результате")
    def should_have_first_result_with_text(self, expected_text: str):
        """Проверяет, что первый найденный трек содержит искомое название."""
        self.FIRST_TRACK_RESULT.should(be.visible).should(have.text(expected_text))
        return self

    @allure.step("Проверка отображения сообщения 'Ничего не найдено'")
    def should_show_no_results_message(self, expected_message: str):
        """Проверяет наличие сообщения об отсутствии результатов (для негативного поиска)."""
        self.NO_RESULTS_MESSAGE.should(be.visible).should(have.text(expected_message))
        return self