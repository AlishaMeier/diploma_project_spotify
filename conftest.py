import pytest
from selenium import webdriver
from selene import browser
import allure
import requests
from dotenv import load_dotenv
import os
from selenium.webdriver.chrome.options import Options

load_dotenv()

SPOTIFY_USERNAME = os.getenv('SPOTIFY_USERNAME')
SPOTIFY_PASSWORD = os.getenv('SPOTIFY_PASSWORD')
# URL Selenoid
SELENOID_URL = "http://localhost:4444/wd/hub"
SELENOID_HOST = "localhost"  # Хост для получения видео



def attach_video(session_id):

    try:
        # Формируем URL для скачивания видео (стандартный путь Selenoid)
        video_url = f"http://{SELENOID_HOST}:4444/video/{session_id}.mp4"

        response = requests.get(video_url, timeout=10)

        if response.status_code == 200:
            allure.attach(
                response.content,
                name="video_" + session_id,
                attachment_type=allure.attachment_type.MP4
            )
        else:
            print(f"Ошибка при получении видео (статус: {response.status_code})")


    except requests.exceptions.RequestException as e:
        print(f"Ошибка HTTP-запроса при получении видео: {e}")



@pytest.fixture(scope="function", autouse=True)
def setup_browser(request):
    options = Options()
    session_id = None  # Переменная для хранения ID сессии

    selenoid_capabilities = {
        "browserName": "chrome",
        "browserVersion": "128.0",
        "enableVNC": True,
        "enableVideo": True,  # Включение записи видео
    }
    options.capabilities.update(selenoid_capabilities)

    driver = webdriver.Remote(
        command_executor=SELENOID_URL,
        options=options
    )

    browser.config.driver = driver
    session_id = driver.session_id

    browser.config.base_url = 'https://spotify.com'
    browser.config.driver.set_window_size(1920, 1080)


    yield


    allure.attach(
        browser.driver.get_screenshot_as_png(),
        name='screenshot',
        attachment_type=allure.attachment_type.PNG
    )

    for log_type, logs in browser.driver.get_logs().items():
        log_content = '\n'.join(f'{log["timestamp"]} {log["level"]}: {log["message"]}' for log in logs)
        allure.attach(
            log_content,
            name=f'{log_type} logs',
            attachment_type=allure.attachment_type.TEXT
        )

    # 3. ОБЯЗАТЕЛЬНОЕ ДОБАВЛЕНИЕ ВИДЕО (ВО ВСЕХ СЛУЧАЯХ)
    if session_id:
        attach_video(session_id)

    # --- 4. Закрытие браузера ---
    browser.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_make_report(item, call):

    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep


@pytest.fixture
def login_page():
    from spotify_project.pages.login_page import LoginPage
    return LoginPage()


@pytest.fixture
def home_page():
    from spotify_project.pages.home_page import HomePage
    return HomePage()


@pytest.fixture
def playlist_page():
    from spotify_project.pages.playlist_page import PlaylistPage
    return PlaylistPage()


@pytest.fixture
def credentials():
    return {
        "username": SPOTIFY_USERNAME,
        "password": SPOTIFY_PASSWORD
    }