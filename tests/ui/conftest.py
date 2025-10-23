import pytest
import os
import itertools
from dotenv import load_dotenv
from selene import browser, be
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from spotify_project.utils import attach_web


def pytest_addoption(parser):
    parser.addoption(
        '--browser_version',
        default='128.0'
    )
    parser.addoption(
        '--language',
        default='ru',
        help='Choose browser language: ru, en, etc.'
    )


@pytest.fixture(scope='session')
def browser_version(request):
    return request.config.getoption('--browser_version')


@pytest.fixture(scope='session')
def browser_language(request):
    return request.config.getoption('--language')


@pytest.fixture(scope="session", autouse=True)
def load_env():
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

browser.config.base_url = "https://spotify.com"
browser.config.timeout = 10.0
browser.config.window_width = 1628
browser.config.window_height = 1017


@pytest.fixture(scope="function", autouse=True)
def setup_browser(browser_version, browser_language):  # <--- Добавлен 'browser_language'

    login = os.getenv("SELENOID_LOGIN")
    password = os.getenv("SELENOID_PASS")
    selenoid_base_url = os.getenv("SELENOID_URL")  # https://selenoid.autotests.cloud/wd/hub

    if not selenoid_base_url:
        raise ValueError("Переменная SELENOID_URL не найдена в .env!")

    try:
        if not selenoid_base_url.startswith("https://"):
            raise ValueError(f"SELENOID_URL должен начинаться с https://, получено: {selenoid_base_url}")
        url_parts = selenoid_base_url.split("https://")
        if len(url_parts) < 2 or not url_parts[1]:
            raise ValueError(f"Некорректный формат SELENOID_URL после https://: {selenoid_base_url}")
        url_without_protocol = url_parts[1]

        remote_url = f"https://{login}:{password}@{url_without_protocol}"

    except Exception as e:
        raise ValueError(f"Ошибка при формировании URL для Selenoid: {e}")

    print(f"DEBUG: Попытка подключения к Selenoid по URL: {remote_url}")
    print(f"DEBUG: Запрашиваемая версия браузера: {browser_version}")
    print(f"DEBUG: Запрашиваемый язык браузера: {browser_language}")  # <--- Строка для отладки

    options = Options()

    options.add_argument(f'--lang={browser_language}')
    options.add_experimental_option('prefs', {
        'intl.accept_languages': browser_language
    })

    selenoid_capabilities = {
        "browserName": "chrome",
        "browserVersion": browser_version,
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": True
        }
    }

    options.capabilities.update(selenoid_capabilities)

    driver = webdriver.Remote(
        command_executor=remote_url,
        options=options
    )

    browser.config.driver = driver
    browser.open("/")

    try:
        cookie_button = browser.element('#onetrust-reject-all-handler')
        if cookie_button.with_(timeout=2).wait_until(be.visible):
            cookie_button.click()
    except Exception as e:
        print(f"Не удалось нажать кнопку cookie: {e}")

    yield

    try:
        attach_web.add_screenshot_page(browser)
    except Exception as e:
        print(f"Failed to attach screenshot: {e}")
    try:
        attach_web.add_browser_logs(browser)
    except Exception as e:
        print(f"Failed to attach logs: {e}")
    try:
        attach_web.add_html_page_source(browser)
    except Exception as e:
        print(f"Failed to attach html: {e}")
    try:
        attach_web.add_video_from_selenoid(browser)
    except Exception as e:
        print(f"Failed to attach video: {e}")

    browser.quit()


@pytest.fixture
def login_page():
    from spotify_project.pages.login_page import LoginPage
    return LoginPage()


@pytest.fixture
def navigation_page():
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