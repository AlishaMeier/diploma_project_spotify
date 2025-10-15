from selene import browser, have
import allure

class PlaylistPage:
    def __init__(self):
        self.playlist_title = browser.element('[data-testid="playlist-title"]')
        self.add_song_button = browser.element('[data-testid="add-song"]')

    @allure.step("Добавляем песню в плейлист")
    def add_song_to_playlist(self, song_name):
        self.add_song_button.click()
        browser.element('[data-testid="song-search"]').type(song_name)
        browser.element('[data-testid="add-song-button"]').click()

    @allure.step("Проверяем, что песня добавлена в плейлист")
    def should_contain_song(self, song_name):
        self.playlist_title.should(have.text(song_name))
