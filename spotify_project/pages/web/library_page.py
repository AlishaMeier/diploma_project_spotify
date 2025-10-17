import os
from selene import browser, have, be
import allure
from selene.core.entity import Element
from selene.core import query
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class LibraryPage:
    CREATE_BUTTON: Element = browser.element('[aria-label="Создать"]')
    CREATE_PLAYLIST_MENU_ITEM: Element = browser.element('//p[text()="Плейлист"]')
    PLAYLIST_PAGE_TITLE: Element = browser.element('[data-testid="entityTitle"] h1')
    PLAYLIST_TITLE_INPUT: Element = browser.element('[data-testid="playlist-edit-details-name-input"]')
    PLAYLIST_SAVE_BUTTON: Element = browser.element('[data-testid="playlist-edit-details-save-button"]')
    PLAYLIST_IMAGE_INPUT: Element = browser.element('input[type="file"]')
    SEARCH_SONG_INPUT_ON_PLAYLIST_PAGE: Element = browser.element('[placeholder="Поиск треков и выпусков"]')
    SONG_SEARCH_RESULTS_CONTAINER: Element = browser.element('[data-testid="playlist-inline-curation-results"]')
    ADD_SONG_BUTTON: Element = SONG_SEARCH_RESULTS_CONTAINER.element('[data-testid="add-button"]')
    CONTEXT_MENU_DELETE_OPTION: Element = browser.element('//span[text()="Удалить"]')
    CONFIRM_DELETE_BUTTON: Element = browser.element('//button[text()="Удалить"]').with_(be.visible)

    def track_in_playlist_by_name(self, name: str) -> Element:
        return browser.element(f'//div[@data-testid="tracklist-row"]//a[text()="{name}"]')

    def playlist_item_by_name(self, name: str) -> Element:
        return browser.element(f'[aria-label="{name}"]')

    @allure.step("Создание нового плейлиста")
    def create_playlist(self) -> str:
        self.CREATE_BUTTON.should(be.visible).click()
        self.CREATE_PLAYLIST_MENU_ITEM.should(be.visible).click()
        browser.should(have.url_containing("/playlist/"))
        self.PLAYLIST_PAGE_TITLE.should(be.visible)
        return self.PLAYLIST_PAGE_TITLE.get(query.text)

    @allure.step("Открытие модального окна для редактирования деталей плейлиста")
    def open_edit_details_modal(self):
        self.PLAYLIST_PAGE_TITLE.should(be.visible).click()
        return self

    @allure.step("Ввод нового имени плейлиста: '{new_name}'")
    def set_playlist_name(self, new_name: str):
        self.PLAYLIST_TITLE_INPUT.should(be.visible).clear().type(new_name).press_tab()
        return self

    @allure.step("Выбор обложки для плейлиста")
    def set_playlist_cover_image(self, image_path: str):
        self.PLAYLIST_IMAGE_INPUT.send_keys(image_path)
        return self

    @allure.step("Сохранение изменений в деталях плейлиста")
    def save_playlist_details(self):
        self.PLAYLIST_SAVE_BUTTON.with_(timeout=4).should(be.clickable)
        browser.driver.execute_script("arguments[0].click();", self.PLAYLIST_SAVE_BUTTON.locate())
        return self

    @allure.step("Добавление песни '{song_name}' в плейлист")
    def add_song_to_playlist(self, song_name: str):
        self.SEARCH_SONG_INPUT_ON_PLAYLIST_PAGE.should(be.visible).type(song_name)
        # ИСПРАВЛЕНИЕ: Ждем появления контейнера с результатами
        self.SONG_SEARCH_RESULTS_CONTAINER.should(be.visible)
        # Теперь кликаем по кнопке, которая гарантированно находится внутри этого контейнера
        self.ADD_SONG_BUTTON.should(be.visible).click()
        return self

    @allure.step("Удаление плейлиста по имени: {name}")
    def delete_playlist(self, name: str):
        browser.open('')
        self.playlist_item_by_name(name).should(be.visible).context_click()
        self.CONTEXT_MENU_DELETE_OPTION.should(be.visible).click()
        self.CONFIRM_DELETE_BUTTON.click()
        self.should_not_have_playlist_in_list(name)
        return self


    @allure.step("Проверка, что текущая страница - это плейлист с именем '{name}'")
    def should_be_on_playlist_page_with_name(self, name: str):
        self.PLAYLIST_PAGE_TITLE.should(have.text(name))
        return self

    @allure.step("Проверка, что песня '{song_name}' добавлена в плейлист")
    def should_have_song_in_playlist(self, song_name: str):
        self.track_in_playlist_by_name(song_name).should(be.visible)
        return self

    @allure.step("Проверка, что плейлист '{name}' есть в боковом меню")
    def should_have_playlist_in_list(self, name: str):
        self.playlist_item_by_name(name).should(be.visible)
        return self

    @allure.step("Проверка отсутствия плейлиста '{name}' в списке")
    def should_not_have_playlist_in_list(self, name: str):
        self.playlist_item_by_name(name).should(be.not_.present)
        return self