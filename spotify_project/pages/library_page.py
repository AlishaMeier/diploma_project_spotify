from selene import browser, have, be
import allure
from selene.core.entity import Element
from selene.support import by
from selene.core import query

class LibraryPage:
    """Page Object для страницы 'Your Library' (Библиотека)."""


    CREATE_PLAYLIST_TILE_BUTTON: Element = browser.element('//button[text()="Create playlist"]')


    PLAYLIST_ITEM_BY_NAME = lambda name: browser.element(f'[aria-label*="{name}"]').with_(have.text(name))


    PLAYLIST_PAGE_TITLE: Element = browser.element(by.xpath('//h1')).with_(have.css_property('font-size'))


    CONTEXT_MENU_DELETE_OPTION: Element = browser.element('//span[text()="Delete"]')
    CONFIRM_DELETE_BUTTON: Element = browser.element('//button[text()="Delete"]').with_(be.visible)



    @allure.step("Создание плейлиста через плитку 'Create playlist' и получение его имени")
    def create_playlist_via_tile(self) -> str:
        """
        Нажимает на плитку, ожидает перехода на страницу плейлиста
        и возвращает его дефолтное имя (например, 'My Playlist #2').
        """
        self.CREATE_PLAYLIST_TILE_BUTTON.should(be.visible).click()

        browser.should(have.url_containing("/playlist/"))


        self.PLAYLIST_PAGE_TITLE.should(be.visible) # Ждем, пока элемент станет видимым
        default_name = self.PLAYLIST_PAGE_TITLE.get(query.text)

        return default_name

    @allure.step("Удаление плейлиста по имени: {name}")
    def delete_playlist(self, name: str):
        """
        Открывает контекстное меню для плейлиста в списке и удаляет его.
        """
        with allure.step(f"1. Клик правой кнопкой по плейлисту '{name}'"):

            self.PLAYLIST_ITEM_BY_NAME(name).should(be.visible).context_click()

        with allure.step("2. Выбор опции 'Удалить'"):
            self.CONTEXT_MENU_DELETE_OPTION.should(be.visible).click()

        with allure.step("3. Подтверждение удаления"):
            self.CONFIRM_DELETE_BUTTON.click()

        self.should_not_have_playlist_in_list(name)

        return self



    @allure.step("Проверка, что плейлист {name} отображается на странице")
    def should_be_on_playlist_page_with_name(self, name: str):
        """Проверяет, что заголовок на текущей странице соответствует имени."""
        self.PLAYLIST_PAGE_TITLE.should(have.text(name))
        return self

    @allure.step("Проверка отсутствия плейлиста {name} в списке библиотеки")
    def should_not_have_playlist_in_list(self, name: str):
        """Проверяет, что плейлиста нет в боковой панели."""
        self.PLAYLIST_ITEM_BY_NAME(name).should(be.not_.present)
        return self