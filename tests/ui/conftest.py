import pytest
from selenium import webdriver
from selene import browser, be
from selene.support.shared import browser
from dotenv import load_dotenv
import os
from spotify_project.utils import attach_web
import itertools
from selenium.webdriver.chrome.options import Options

load_dotenv()

SPOTIFY_USERNAME = os.getenv('SPOTIFY_USERNAME')
SPOTIFY_PASSWORD = os.getenv('SPOTIFY_PASSWORD')
SPOTIFY_EXPECTED_NAME = os.getenv('SPOTIFY_EXPECTED_NAME', 'Alisha')

SPOTIFY_USERNAME_ALT = os.getenv('SPOTIFY_USERNAME_ALT')
SPOTIFY_PASSWORD_ALT = os.getenv('SPOTIFY_PASSWORD_ALT')
SPOTIFY_EXPECTED_NAME_ALT = os.getenv('SPOTIFY_EXPECTED_NAME_ALT', 'Alisha')

_credentials_list = []
# Добавляем основной аккаунт, если он есть
if SPOTIFY_USERNAME and SPOTIFY_PASSWORD:
    _credentials_list.append({
        "username": SPOTIFY_USERNAME,
        "password": SPOTIFY_PASSWORD,
        "expected_name": SPOTIFY_EXPECTED_NAME # Используем имя из .env
    })
# Добавляем альтернативный аккаунт, если он есть
if SPOTIFY_USERNAME_ALT and SPOTIFY_PASSWORD_ALT:
     _credentials_list.append({
        "username": SPOTIFY_USERNAME_ALT,
        "password": SPOTIFY_PASSWORD_ALT,
        "expected_name": SPOTIFY_EXPECTED_NAME_ALT # Используем имя из .env
    })

_credential_cycler = itertools.cycle(_credentials_list) if _credentials_list else None


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
            attach_web.add_video(browser)
        except Exception as e:
            print(f"Failed to attach Allure report: {e}")


@pytest.fixture(scope="function", autouse=True)
def setup_browser():
    # 👈 3. Вся фикстура setup_browser заменена на эту

    # Конфигурация опций для Selenoid
    options = Options()
    # Используем версию 120.0, как указано в config/browsers.json
    options.browser_version = "120.0"

    # Selenoid-опции для VNC (просмотр) и записи видео
    options.set_capability("selenoid:options", {
        "enableVNC": True,
        "enableVideo": True
    })

    selenoid_url = os.getenv("SELENOID_URL", "http://localhost:4444/wd/hub")

    driver = webdriver.Remote(
        command_executor=selenoid_url,
        options=options
    )
    browser.config.driver = driver

    browser.open('')

    cookie_accept_button = browser.element('#onetrust-reject-all-handler')
    if cookie_accept_button.with_(timeout=2).wait_until(be.visible):
        cookie_accept_button.click()

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
def search_page():
    from spotify_project.pages.search_page import SearchPage
    return SearchPage()


@pytest.fixture
def credentials():

    if not _credential_cycler:
        pytest.fail("Не найдены валидные учетные данные Spotify (USERNAME, PASSWORD) в .env файле.")

    # Получаем вторые креды
    creds = next(_credential_cycler)
    print(f"\nDEBUG: Используются учетные данные для пользователя: {creds['username']}")
    return creds
