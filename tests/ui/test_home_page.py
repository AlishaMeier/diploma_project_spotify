import pytest
import allure
from spotify_project.pages.home_page import HomePage

@allure.feature("Поиск песен")
@allure.story("Тест на поиск песни по названию")
def test_search_functionality(home_page):
    home_page.search_for_song("Dope")
    home_page.should_show_results()
