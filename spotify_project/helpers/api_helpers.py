import allure
import requests


class PlaylistApi:
    def __init__(self, base_url, headers):
        self.base_url = base_url
        self.headers = headers


    @allure.step("API: Получить плейлист по ID: {playlist_id}")
    def get_playlist(self, playlist_id: str):

        response = requests.get(
            f"{self.base_url}/playlists/{playlist_id}",
            headers=self.headers
        )
        return response

    @allure.step("API: Добавить трек {track_uri} в плейлист {playlist_id}")
    def add_track_to_playlist(self, playlist_id: str, track_uri: str):

        return requests.post(
            f"{self.base_url}/playlists/{playlist_id}/tracks",
            headers=self.headers,
            json={
                "uris": [track_uri]
            }
        )

    @allure.step("API: Удалить трек из плейлиста {playlist_id}")
    def delete_track_from_playlist(self, playlist_id: str, track_uri: str):

        body = {"tracks": [{"uri": track_uri}]}
        return requests.delete(
            f"{self.base_url}/playlists/{playlist_id}/tracks",
            headers=self.headers,
            json=body
        )

    @allure.step("API: Создать плейлист для пользователя {user_id}")
    def create_playlist(self, user_id: str, name: str, description: str, public: bool = True):

        return requests.post(
            f"{self.base_url}/users/{user_id}/playlists",
            headers=self.headers,
            json={
                "name": name,
                "description": description,
                "public": public
            }
        )

    @allure.step("API: Удалить плейлист {playlist_id}")
    def unfollow_playlist(self, playlist_id: str):

        return requests.delete(
            f"{self.base_url}/playlists/{playlist_id}/followers",
            headers=self.headers
        )

class LibraryApi:
    def __init__(self, base_url, headers):
        self.base_url = base_url
        self.headers = headers

    @allure.step("API: Сохранить альбом с ID {album_id} в медиатеку")
    def save_album(self, album_id: str):

        return requests.put(
            f"{self.base_url}/me/albums",
            headers=self.headers,
            json={"ids": [album_id]}
        )

    @allure.step("API: Получить сохраненные альбомы")
    def get_saved_albums(self):

        return requests.get(
            f"{self.base_url}/me/albums",
            headers=self.headers
        )

    @allure.step("API: Удалить альбом с ID {album_id} из медиатеки")
    def remove_album(self, album_id: str):

        return requests.delete(
            f"{self.base_url}/me/albums",
            headers=self.headers,
            json={"ids": [album_id]}
        )

    @allure.step("API: Подписаться на артиста с ID {artist_id}")
    def follow_artist(self, artist_id: str):
        return requests.put(
            f"{self.base_url}/me/following?type=artist",
            headers=self.headers,
            json={"ids": [artist_id]}
        )

    @allure.step("API: Отписаться от артиста с ID {artist_id}")
    def unfollow_artist(self, artist_id: str):
        return requests.delete(
            f"{self.base_url}/me/following?type=artist",
            headers=self.headers,
            json={"ids": [artist_id]}
        )