import pytest
import allure
from spotify_project.pages.search_page import SearchPage
from spotify_project.pages.navigation_page import NavigationPage
from spotify_project.pages.artist_page import ArtistPage
from selene import be, have, browser

INVALID_SEARCH_DATA = [
    (' ', "По запросу « » ничего не найдено"),
]

@allure.epic("UI-тестирование")
@allure.feature("Поиск")
class TestSearchFunctionality:

    @pytest.mark.ui
    @allure.story("Визуальная проверка карточки трека в поиске")
    @allure.label("owner", "AlishaMeier")
    @allure.tag("positive", "visual", "smoke")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_result_has_visual_details(self, navigation_page: NavigationPage, search_page: SearchPage):
        song_name = "Louder than bombs"
        expected_artist = "BTS"
        navigation_page.open_main_page() # <-- [Пункт 2]
        search_page.search_from_main_page(song_name)
        search_page.should_have_top_result_card_details(expected_artist)

    @pytest.mark.ui
    @allure.story("Переход на страницу артиста из результатов поиска")
    @allure.label("owner", "AlishaMeier")
    @allure.tag("public", "regression")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_and_navigate_to_artist(self, navigation_page: NavigationPage, search_page: SearchPage, artist_page: ArtistPage):
        artist_name = "BTS"
        navigation_page.open_main_page()
        search_page.search_from_main_page(artist_name)
        search_page.should_have_top_result_as_artist(artist_name)
        search_page.click_top_result_card()
        artist_page.should_be_on_artist_page(artist_name)

    @pytest.mark.ui
    @allure.story("Поиск альбома и проверка карточки")
    @allure.label("owner", "AlishaMeier")
    @allure.tag("public", "regression")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_finds_album(self, navigation_page: NavigationPage, search_page: SearchPage):
        album_name = "2 Cool 4 Skool"
        expected_artist = "BTS"
        navigation_page.open_main_page()
        search_page.search_from_main_page(album_name)
        search_page.should_have_top_result_with_title(album_name)
        search_page.should_have_top_result_as_album(expected_artist)

    @pytest.mark.ui
    @allure.story("Проверка работы фильтра Исполнитель на странице результатов поиска")
    @allure.label("owner", "AlishaMeier")
    @allure.tag("public", "regression")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_filters(self, navigation_page: NavigationPage, search_page: SearchPage):
        query = "Queen"
        expected_artist_type = "Исполнитель"
        navigation_page.open_main_page()
        search_page.search_from_main_page(query)
        search_page.filter_button_artists.should(be.visible).click()
        search_page.main_results_section.should(be.visible)
        search_page.first_main_result_title.should(be.visible).should(have.text(query))
        search_page.first_main_result_subtitle.should(be.visible).should(have.text(expected_artist_type))

    @pytest.mark.ui
    @allure.story("Поиск с опечаткой")
    @allure.label("owner", "AlishaMeier")
    @allure.tag("positive", "regression")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_with_typo_shows_corrected_results(self, navigation_page: NavigationPage, search_page: SearchPage):
        query_with_typo = "Nirvna"
        corrected_artist = "Nirvana"
        navigation_page.open_main_page()
        search_page.search_from_main_page(query_with_typo)
        search_page.top_result_card.should(be.visible)
        search_page.top_result_artist.should(be.visible).should(have.text(corrected_artist))

    @pytest.mark.ui
    @allure.story("Негативный поиск: не найдено результатов")
    @allure.label("owner", "AlishaMeier")
    @allure.tag("negative", "parametrize")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.parametrize("query, expected_message", INVALID_SEARCH_DATA)
    def test_search_no_results_found(self, query, expected_message, navigation_page: NavigationPage,
                                     search_page: SearchPage):
            navigation_page.open_main_page()
            search_page.search_from_main_page(query)
            search_page.should_see_message(expected_message)