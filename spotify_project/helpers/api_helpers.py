import allure
from spotify_project.utils.attach_api import api_request

class PlaylistApi:
    def __init__(self, base_url, headers):
        self.base_url = base_url
        self.headers = headers

    @allure.step("API: Получить плейлист по ID: {playlist_id}")
    def get_playlist(self, playlist_id: str):
        endpoint = f"/playlists/{playlist_id}"
        return api_request(self.base_url, endpoint, headers=self.headers)

    @allure.step("API: Добавить трек {track_uri} в плейлист {playlist_id}")
    def add_track_to_playlist(self, playlist_id: str, track_uri: str):
        endpoint = f"/playlists/{playlist_id}/tracks"
        return api_request(self.base_url, endpoint, method="POST", headers=self.headers, json_body={"uris": [track_uri]})

    @allure.step("API: Удалить трек из плейлиста {playlist_id}")
    def delete_track_from_playlist(self, playlist_id: str, track_uri: str):
        endpoint = f"/playlists/{playlist_id}/tracks"
        body = {"tracks": [{"uri": track_uri}]}
        return api_request(self.base_url, endpoint, method="DELETE", headers=self.headers, json_body=body)

    @allure.step("API: Создать плейлист для пользователя {user_id}")
    def create_playlist(self, user_id: str, name: str, description: str, public: bool = True):
        endpoint = f"/users/{user_id}/playlists"
        body = {"name": name, "description": description, "public": public}
        return api_request(self.base_url, endpoint, method="POST", headers=self.headers, json_body=body)

    @allure.step("API: Удалить плейлист {playlist_id}")
    def unfollow_playlist(self, playlist_id: str):
        endpoint = f"/playlists/{playlist_id}/followers"
        return api_request(self.base_url, endpoint, method="DELETE", headers=self.headers)

class LibraryApi:
    def __init__(self, base_url, headers):
        self.base_url = base_url
        self.headers = headers

    @allure.step("API: Сохранить альбом с ID {album_id} в медиатеку")
    def save_album(self, album_id: str):
        endpoint = "/me/albums"
        return api_request(self.base_url, endpoint, method="PUT", headers=self.headers, json_body={"ids": [album_id]})

    @allure.step("API: Получить сохраненные альбомы")
    def get_saved_albums(self):
        endpoint = "/me/albums"
        return api_request(self.base_url, endpoint, headers=self.headers)

    @allure.step("API: Удалить альбом с ID {album_id} из медиатеки")
    def remove_album(self, album_id: str):
        endpoint = "/me/albums"
        return api_request(self.base_url, endpoint, method="DELETE", headers=self.headers, json_body={"ids": [album_id]})

    @allure.step("API: Подписаться на артиста с ID {artist_id}")
    def follow_artist(self, artist_id: str):
        endpoint = "/me/following?type=artist"
        return api_request(self.base_url, endpoint, method="PUT", headers=self.headers, json_body={"ids": [artist_id]})

    @allure.step("API: Отписаться от артиста с ID {artist_id}")
    def unfollow_artist(self, artist_id: str):
        endpoint = "/me/following?type=artist"
        return api_request(self.base_url, endpoint, method="DELETE", headers=self.headers, json_body={"ids": [artist_id]})