import pytest
import allure
from spotify_project.pages.web.search_page import SearchPage

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
        song_name = "Dope"
        expected_artist = "BTS"

        with allure.step(f"1. Выполнить поиск песни '{song_name}'"):
            search_page.search_from_main_page(song_name)

        with allure.step("2. Проверить, что у топ-результата есть обложка и имя исполнителя"):
            search_page.should_have_top_result_details(expected_artist)


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