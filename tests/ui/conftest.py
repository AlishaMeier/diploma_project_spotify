import pytest
from selenium import webdriver
from selene import browser, be
from selene.support.shared import browser
from dotenv import load_dotenv
import os
from spotify_project.utils import attach_web

load_dotenv()

SPOTIFY_USERNAME = os.getenv('SPOTIFY_USERNAME')
SPOTIFY_PASSWORD = os.getenv('SPOTIFY_PASSWORD')

# Настройки браузера
browser.config.base_url = "https://open.spotify.com/"
browser.config.timeout = 10.0
browser.config.window_width = 1728
browser.config.window_height = 1117



@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        try:
            attach_web.add_screenshot(browser)
            attach_web.add_logs(browser)
            attach_web.add_html(browser)
        except Exception as e:
            print(f"Failed to attach Allure report: {e}")


@pytest.fixture(scope="function", autouse=True)
def setup_browser():
    driver = webdriver.Chrome()
    browser.config.driver = driver

    browser.open('')

    cookie_accept_button = browser.element('#onetrust-reject-all-handler')
    if cookie_accept_button.with_(timeout=2).wait_until(be.visible):
        cookie_accept_button.click()

    yield

    driver.quit()

@pytest.fixture
def login_page():
    from spotify_project.pages.web.login_page import LoginPage
    return LoginPage()


@pytest.fixture
def navigation_page():
    from spotify_project.pages.web.navigation_page import NavigationPage
    return NavigationPage()


@pytest.fixture
def library_page():
    from spotify_project.pages.web.library_page import LibraryPage
    return LibraryPage()

@pytest.fixture
def search_page():
    from spotify_project.pages.web.search_page import SearchPage
    return SearchPage()


@pytest.fixture
def credentials():
    return {
        "username": SPOTIFY_USERNAME,
        "password": SPOTIFY_PASSWORD,
        "expected_name": "Alisha"
    }
