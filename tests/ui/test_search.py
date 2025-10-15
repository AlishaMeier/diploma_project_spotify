import pytest
import allure
from spotify_project.pages.search_page import SearchPage

INVALID_SEARCH_DATA = [
    ("asdlfjkglhjklasd", "Ничего не найдено"),
    ("111222333444", "Возможно, вы ввели неправильный запрос"),
]

@allure.epic("UI-тестирование")
@allure.feature("Поиск")
class TestSearchFunctionality:

    @allure.story("Поиск песни по названию и проверка первого результата")
    @allure.tag("positive", "high_priority")
    @allure.severity(allure.severity_level.NORMAL)
    def test_successful_song_search(self, search_page: SearchPage):
        song_name = "Dope"  # Используем уникальное название

        with allure.step("1. Переход на страницу поиска"):
            search_page.open_search_page()

        with allure.step(f"2. Ввод поискового запроса: {song_name}"):
            search_page.type_search_query(song_name)

        with allure.step("3. Проверка, что секции результатов отображаются"):
            search_page.should_show_results()

        with allure.step("4. Проверка, что первый результат содержит название песни"):
            search_page.should_have_first_result_with_text(song_name)

    @allure.story("Негативный поиск: не найдено результатов")
    @allure.tag("negative", "parametrize")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.parametrize("query, expected_message", INVALID_SEARCH_DATA)
    def test_search_no_results_found(self, query, expected_message, search_page: SearchPage):
        with allure.step("1. Переход на страницу поиска"):
            search_page.open_search_page()

        with allure.step(f"2. Ввод невалидного запроса: {query}"):
            search_page.type_search_query(query)

        with allure.step("3. Проверка, что отображается сообщение об отсутствии результатов"):
            search_page.should_show_no_results_message(expected_message)