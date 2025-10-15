import pytest
from selenium import webdriver
from selene import browser
from selene.support.shared import browser
from dotenv import load_dotenv
import os

import allure


# from spotify_project.utils import attach



load_dotenv()

SPOTIFY_USERNAME = os.getenv('SPOTIFY_USERNAME')
SPOTIFY_PASSWORD = os.getenv('SPOTIFY_PASSWORD')

# Настройки браузера
browser.config.base_url = "https://open.spotify.com/"
browser.config.timeout = 15.0  # Уменьшаем таймаут до разумного локального значения
browser.config.window_width = 1300
browser.config.window_height = 760



@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep


# --- ФИКСТУРА БРАУЗЕРА (ОСНОВА: ЛОКАЛЬНЫЙ РЕЖИМ) ---
@pytest.fixture(scope="function", autouse=True)
def setup_browser():

    driver = webdriver.Chrome()
    browser.config.driver = driver
    browser.open(browser.config.base_url)


    yield


    driver.quit()




@pytest.fixture
def login_page():
    from spotify_project.pages.login_page import LoginPage
    return LoginPage()


@pytest.fixture
def navigation_page():
    from spotify_project.pages.navigation_page import NavigationPage
    return NavigationPage()


@pytest.fixture
def library_page():
    from spotify_project.pages.library_page import LibraryPage
    return LibraryPage()


@pytest.fixture
def credentials():
    return {
        "username": SPOTIFY_USERNAME,
        "password": SPOTIFY_PASSWORD,
        "expected_name": "Alisha"
    }