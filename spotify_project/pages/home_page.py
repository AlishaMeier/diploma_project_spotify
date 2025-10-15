from selene import browser, have
import allure

class HomePage:
    def __init__(self):
        self.search_input = browser.element('[data-testid="search-input"]')
        self.playlist_section = browser.element('[aria-label="Playlists"]')

    @allure.step("Ищем песню по имени")
    def search_for_song(self, song_name):
        self.search_input.type(song_name)
        browser.element('[data-testid="search-submit"]').click()

    @allure.step("Проверяем, что результаты поиска отображаются")
    def should_show_results(self):
        self.playlist_section.should(have.text('Playlists'))
