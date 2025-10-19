import pytest
import allure
from spotify_project.pages.web.search_page import SearchPage
from selene import be, have, browser

INVALID_SEARCH_DATA = [
    (" ", "По запросу « » ничего не найдено"),
]

@allure.epic("UI-тестирование")
@allure.feature("Поиск")
class TestSearchFunctionality:

    @allure.story("Визуальная проверка карточки трека в поиске")
    @allure.label("owner", "AlishaMeier")
    @allure.tag("positive", "visual", "smoke")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_result_has_visual_details(self, search_page: SearchPage):
        song_name = "Louder than bombs"
        expected_artist = "BTS"

        with allure.step(f"1. Выполнить поиск песни '{song_name}'"):
            search_page.search_from_main_page(song_name)

        with allure.step("2. Проверить, что у топ-результата есть обложка и имя исполнителя"):
            search_page.should_have_top_result_card_details(expected_artist)


    @allure.story("Переход на страницу артиста из результатов поиска")
    @allure.label("owner", "AlishaMeier")
    @allure.tag("public", "regression")  # Добавим тег public
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_and_navigate_to_artist(self, search_page: SearchPage):
        artist_name = "BTS"

        with allure.step(f"Выполнить поиск артиста '{artist_name}'"):
            search_page.search_from_main_page(artist_name)

        with allure.step("Проверить, что в топе есть карточка артиста"):
            search_page.should_have_top_result_with_title(artist_name)
            search_page.TOP_RESULT_CARD.element('a[href*="/artist/"]').should(be.visible)

        with allure.step("Кликнуть по карточке артиста"):
            search_page.TOP_RESULT_CARD.click()

        with allure.step("Проверка, что открылась страница артиста"):
            browser.should(have.url_containing('/artist/'))
            browser.element('[data-testid="entityTitle"] h1').should(have.text(artist_name))


    @allure.story("Поиск альбома и проверка карточки")
    @allure.label("owner", "AlishaMeier")
    @allure.tag("public", "regression")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_finds_album(self, search_page: SearchPage):
        album_name = "2 Cool 4 Skool"
        expected_artist = "BTS"

        with allure.step(f"Выполнить поиск альбома '{album_name}'"):
            search_page.search_from_main_page(album_name)

        with allure.step("Проверить, что топ-результат - это альбом с правильными деталями"):
            search_page.should_have_top_result_with_title(album_name)
            search_page.should_have_top_result_as_album(expected_artist)


    @allure.story("Проверка работы фильтра Исполнитель на странице результатов поиска")
    @allure.label("owner", "AlishaMeier")
    @allure.tag("public", "regression")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_filters(self, search_page: SearchPage):
        query = "Queen"
        expected_artist_type = "Исполнитель"

        with allure.step(f"Выполнить поиск по запросу '{query}'"):
            search_page.search_from_main_page(query)

        with allure.step("Нажать на фильтр 'Исполнители'"):
            search_page.FILTER_BUTTON_ARTISTS.should(be.visible).click()

        with allure.step("Проверить, что первый основной результат - это исполнитель 'Queen'"):
            search_page.MAIN_RESULTS_SECTION.should(be.visible)
            search_page.FIRST_MAIN_RESULT_TITLE.should(be.visible).should(have.text(query))
            search_page.FIRST_MAIN_RESULT_SUBTITLE.should(be.visible).should(have.text(expected_artist_type))


    @allure.story("Поиск с опечаткой")
    @allure.label("owner", "AlishaMeier")
    @allure.tag("positive", "regression")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_with_typo_shows_corrected_results(self, search_page: SearchPage):
        query_with_typo = "Nirvna"
        corrected_artist = "Nirvana"

        with allure.step("Выполнить поиск с опечаткой '{query_with_typo}'"):
            search_page.search_from_main_page(query_with_typo)

        with allure.step("Проверить, что в топ-результате отображается исправленное название"):
            search_page.should_have_top_result_with_title(corrected_artist)


    @allure.story("Негативный поиск: не найдено результатов")
    @allure.label("owner", "AlishaMeier")
    @allure.tag("negative", "parametrize")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.parametrize("query, expected_message", INVALID_SEARCH_DATA)
    def test_search_no_results_found(self, query, expected_message, search_page: SearchPage):
        with allure.step("Ввод невалидного запроса: '{query}'"):
            search_page.search_from_main_page(query)

        with allure.step("Проверка, что отображается сообщение об отсутствии результатов"):
            search_page.should_see_message(expected_message)

