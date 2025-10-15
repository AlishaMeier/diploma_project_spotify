import pytest
from selenium import webdriver
from selene import browser
import allure
from dotenv import load_dotenv
import os

# Загружаем переменные из .env
load_dotenv()

# Извлекаем креды из переменных окружения
SPOTIFY_USERNAME = os.getenv('SPOTIFY_USERNAME')
SPOTIFY_PASSWORD = os.getenv('SPOTIFY_PASSWORD')

# Фикстура для инициализации браузера и работы с ним
@pytest.fixture(scope="session", autouse=True)
def setup_browser():
    # Настроим браузер и базовый URL
    browser.config.base_url = 'https://spotify.com'
    browser.config.driver = webdriver.Chrome()

    # Устанавливаем размер окна браузера
    browser.config.driver.set_window_size(1920, 1080)

    yield
    browser.quit()

# Фикстуры для страниц
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

# Фикстура для получения данных пользователей
@pytest.fixture
def credentials():
    return {
        "username": SPOTIFY_USERNAME,
        "password": SPOTIFY_PASSWORD
    }
