import pytest
import os
from dotenv import load_dotenv
from selene import browser, be
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from spotify_project.utils import attach_web

browser.config.base_url = "https://spotify.com"
browser.config.timeout = 15.0
browser.config.window_width = 1628
browser.config.window_height = 1017


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
    parser.addoption(
        '--driver-type',
        help='Choose driver type: selenoid or local',
        default='selenoid'  # Selenoid по умолчанию
    )


@pytest.fixture(scope='session')
def browser_version(request):
    return request.config.getoption('--browser_version')


@pytest.fixture(scope='session')
def browser_language(request):
    return request.config.getoption('--language')


@pytest.fixture(scope='session')
def driver_type(request):
    return request.config.getoption('--driver-type')


@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv()


@pytest.fixture(scope="function", autouse=True)
def setup_browser(browser_version, browser_language, driver_type):
    # Общие опции для Chrome
    options = Options()
    options.add_argument(f'--lang={browser_language}')
    options.add_experimental_option('prefs', {
        'intl.accept_languages': browser_language
    })

    if driver_type == 'selenoid':
        print("\nDEBUG: Запуск тестов в Selenoid")
        login = os.getenv("SELENOID_LOGIN")
        password = os.getenv("SELENOID_PASS")
        selenoid_base_url = os.getenv("SELENOID_URL")

        if not all([login, password, selenoid_base_url]):
            raise ValueError("SELENOID_LOGIN, SELENOID_PASS или SELENOID_URL не найдены в .env для Selenoid")

        try:
            url_without_protocol = selenoid_base_url.split("https://")[1]
            remote_url = f"https://{login}:{password}@{url_without_protocol}"
        except Exception as e:
            raise ValueError(f"Ошибка при формировании URL для Selenoid: {e}")

        print(f"DEBUG: Подключение к Selenoid по URL: {remote_url}")

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

    elif driver_type == 'local':
        print("\nDEBUG: Запуск тестов в локальном Chrome")
        # Убедитесь, что chromedriver установлен и доступен в PATH
        driver = webdriver.Chrome(options=options)

    else:
        raise ValueError(f"Неизвестный --driver-type: {driver_type}. Доступны: local, selenoid")

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

    # Видео аттачим ТОЛЬКО если это был Selenoid
    if driver_type == 'selenoid':
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
    username = os.getenv('SPOTIFY_USERNAME')
    password = os.getenv('SPOTIFY_PASSWORD')
    expected_name = os.getenv('SPOTIFY_EXPECTED_NAME', 'Alisha')

    if not username or not password:
        pytest.fail(
            "ОШИБКА: Не найдены SPOTIFY_USERNAME или SPOTIFY_PASSWORD в переменных окружения (.env файле)."
        )

    creds = {
        "username": username,
        "password": password,
        "expected_name": expected_name
    }

    print(f"\nDEBUG: Используются учетные данные: {creds['username']}")
    return creds