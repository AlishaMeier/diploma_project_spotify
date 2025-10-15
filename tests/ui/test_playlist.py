import pytest
import allure
from spotify_project.pages.playlist_page import PlaylistPage

@allure.feature("Управление плейлистом")
@allure.story("Тест на добавление песни в плейлист")
def test_add_song_to_playlist(playlist_page):
    playlist_page.add_song_to_playlist("Dope")
    playlist_page.should_contain_song("Dope")
