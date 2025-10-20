import pytest
import os
import itertools
from dotenv import load_dotenv
from selene import browser, be
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from spotify_project.utils import attach_web

load_dotenv()

SPOTIFY_USERNAME = os.getenv('SPOTIFY_USERNAME')
SPOTIFY_PASSWORD = os.getenv('SPOTIFY_PASSWORD')
SPOTIFY_EXPECTED_NAME = os.getenv('SPOTIFY_EXPECTED_NAME', 'Alisha')

SPOTIFY_USERNAME_ALT = os.getenv('SPOTIFY_USERNAME_ALT')
SPOTIFY_PASSWORD_ALT = os.getenv('SPOTIFY_PASSWORD_ALT')
SPOTIFY_EXPECTED_NAME_ALT = os.getenv('SPOTIFY_EXPECTED_NAME_ALT', 'Alisha')

_credentials_list = []
if SPOTIFY_USERNAME and SPOTIFY_PASSWORD:
    _credentials_list.append({
        "username": SPOTIFY_USERNAME,
        "password": SPOTIFY_PASSWORD,
        "expected_name": SPOTIFY_EXPECTED_NAME
    })
if SPOTIFY_USERNAME_ALT and SPOTIFY_PASSWORD_ALT:
    _credentials_list.append({
        "username": SPOTIFY_USERNAME_ALT,
        "password": SPOTIFY_PASSWORD_ALT,
        "expected_name": SPOTIFY_EXPECTED_NAME_ALT
    })

_credential_cycler = itertools.cycle(_credentials_list) if _credentials_list else None

browser.config.base_url = "https://open.spotify.com/"
browser.config.timeout = 10.0
browser.config.window_width = 1728
browser.config.window_height = 1117


@pytest.fixture(scope="function", autouse=True)
def setup_browser():
    options = Options()

    capabilities = {
        "browserName": "chrome",
        "browserVersion": "128",   # ✅ без цифр
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": True
        }
    }
    options.set_capability("selenoid:options", capabilities["selenoid:options"])
    options.set_capability("browserName", "chrome")
    options.set_capability("browserVersion", "128")

    login = os.getenv("SELENOID_LOGIN")
    password = os.getenv("SELENOID_PASS")
    base_url = os.getenv("SELENOID_URL")  # https://selenoid.autotests.cloud/wd/hub

    remote_url = base_url.replace(
        "https://",
        f"https://{login}:{password}@"
    )

    driver = webdriver.Remote(
        command_executor=remote_url,
        options=options
    )

    browser.config.driver = driver
    browser.open('/')

    try:
        cookie_button = browser.element('#onetrust-reject-all-handler')
        if cookie_button.with_(timeout=2).wait_until(be.visible):
            cookie_button.click()
    except:
        pass

    yield

    driver.quit()


@pytest.fixture
def login_page():
    from spotify_project.pages.login_page import LoginPage
    return LoginPage()


@pytest.fixture
def navigation_page():
    # Убедись, что путь к NavigationPage правильный
    from spotify_project.pages.navigation_page import NavigationPage
    return NavigationPage()


@pytest.fixture
def search_page():
    from spotify_project.pages.search_page import SearchPage
    return SearchPage()


@pytest.fixture
def credentials():
    if not _credential_cycler:
        pytest.fail("Не найдены валидные учетные данные Spotify (USERNAME, PASSWORD) в .env файле.")

    creds = next(_credential_cycler)
    print(f"\nDEBUG: Используются учетные данные: {creds['username']}")
    return creds