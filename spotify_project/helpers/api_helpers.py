import allure
import requests
from typing import Optional
from spotify_project.utils.attach_api import api_request
from spotify_project.schemas.playlist import Playlist, AddTrackResponse
from spotify_project.schemas.album import GetSavedAlbumsResponse


class PlaylistApi:
    def __init__(self, base_url, headers):
        self.base_url = base_url
        self.headers = headers

    @allure.step("API: Получить плейлист по ID: {playlist_id}")
    def get_playlist(self, playlist_id: str, expected_status_code: int = 200) -> tuple[requests.Response,
    Optional[Playlist]]:
        endpoint = f"/playlists/{playlist_id}"
        response = api_request(self.base_url, endpoint, headers=self.headers)

        assert response.status_code == expected_status_code, \
            f"Ожидался код {expected_status_code}, получен {response.status_code}. Тело: {response.text}"

        model = None
        if expected_status_code < 400:
            model = Playlist.model_validate(response.json())

        return response, model

    @allure.step("API: Добавить трек {track_uri} в плейлист {playlist_id}")
    # [ИСПРАВЛЕНИЕ Type hint] -> tuple[]
    def add_track_to_playlist(self, playlist_id: str, track_uri: str, expected_status_code: int = 201) -> tuple[
        requests.Response, Optional[AddTrackResponse]]:
        endpoint = f"/playlists/{playlist_id}/tracks"
        response = api_request(self.base_url, endpoint, method="POST", headers=self.headers,
                               json_body={"uris": [track_uri]})

        assert response.status_code == expected_status_code, \
            f"Ожидался код {expected_status_code}, получен {response.status_code}. Тело: {response.text}"

        model = None
        if expected_status_code < 400:
            model = AddTrackResponse.model_validate(response.json())

        return response, model

    @allure.step("API: Удалить трек из плейлиста {playlist_id}")
    def delete_track_from_playlist(self, playlist_id: str, track_uri: str, expected_status_code: int = 200) -> tuple[
        requests.Response, Optional[AddTrackResponse]]:
        endpoint = f"/playlists/{playlist_id}/tracks"
        body = {"tracks": [{"uri": track_uri}]}
        response = api_request(self.base_url, endpoint, method="DELETE", headers=self.headers, json_body=body)

        assert response.status_code == expected_status_code, \
            f"Ожидался код {expected_status_code}, получен {response.status_code}. Тело: {response.text}"

        model = None
        if expected_status_code < 400:
            model = AddTrackResponse.model_validate(response.json())

        return response, model

    @allure.step("API: Создать плейлист для пользователя {user_id}")
    def create_playlist(self, user_id: str, name: str, description: str, public: bool = True,
                        expected_status_code: int = 201) -> tuple[requests.Response, Optional[Playlist]]:
        endpoint = f"/users/{user_id}/playlists"
        body = {"name": name, "description": description, "public": public}
        response = api_request(self.base_url, endpoint, method="POST", headers=self.headers, json_body=body)

        assert response.status_code == expected_status_code, \
            f"Ожидался код {expected_status_code}, получен {response.status_code}. Тело: {response.text}"

        model = None
        if expected_status_code < 400:
            model = Playlist.model_validate(response.json())

        return response, model

    @allure.step("API: Удалить плейлист {playlist_id}")
    def unfollow_playlist(self, playlist_id: str, expected_status_code: int = 200) -> requests.Response:
        endpoint = f"/playlists/{playlist_id}/followers"
        response = api_request(self.base_url, endpoint, method="DELETE", headers=self.headers)

        assert response.status_code == expected_status_code, \
            f"Ожидался код {expected_status_code}, получен {response.status_code}. Тело: {response.text}"

        return response

    @allure.step("API: Загрузить обложку для плейлиста {playlist_id}")
    def upload_playlist_cover(self, playlist_id: str, image_base64_bytes: bytes,
                              expected_status_code: int = 202) -> requests.Response:
        endpoint = f"/playlists/{playlist_id}/images"
        upload_headers = self.headers.copy()
        upload_headers['Content-Type'] = 'image/jpeg'
        response = api_request(
            self.base_url,
            endpoint,
            method="PUT",
            headers=upload_headers,
            data=image_base64_bytes
        )
        assert response.status_code == expected_status_code, \
            f"Ожидался код {expected_status_code}, получен {response.status_code}. Тело: {response.text}"
        return response


class LibraryApi:
    def __init__(self, base_url, headers):
        self.base_url = base_url
        self.headers = headers

    @allure.step("API: Сохранить альбом с ID {album_id} в медиатеку")
    def save_album(self, album_id: str, expected_status_code: int = 200) -> requests.Response:
        endpoint = "/me/albums"
        response = api_request(self.base_url, endpoint, method="PUT", headers=self.headers,
                               json_body={"ids": [album_id]})
        assert response.status_code == expected_status_code, \
            f"Ожидался код {expected_status_code}, получен {response.status_code}. Тело: {response.text}"
        return response

    @allure.step("API: Получить сохраненные альбомы")
    def get_saved_albums(self, expected_status_code: int = 200) -> tuple[
        requests.Response, Optional[GetSavedAlbumsResponse]]:
        endpoint = "/me/albums"
        response = api_request(self.base_url, endpoint, headers=self.headers)

        assert response.status_code == expected_status_code, \
            f"Ожидался код {expected_status_code}, получен {response.status_code}. Тело: {response.text}"

        model = None
        if expected_status_code < 400:
            model = GetSavedAlbumsResponse.model_validate(response.json())

        return response, model

    @allure.step("API: Удалить альбом с ID {album_id} из медиатеки")
    def remove_album(self, album_id: str, expected_status_code: int = 200) -> requests.Response:
        endpoint = "/me/albums"
        response = api_request(self.base_url, endpoint, method="DELETE", headers=self.headers,
                               json_body={"ids": [album_id]})
        assert response.status_code == expected_status_code, \
            f"Ожидался код {expected_status_code}, получен {response.status_code}. Тело: {response.text}"
        return response

    @allure.step("API: Подписаться на артиста с ID {artist_id}")
    def follow_artist(self, artist_id: str, expected_status_code: int = 204) -> requests.Response:
        endpoint = "/me/following?type=artist"
        response = api_request(self.base_url, endpoint, method="PUT", headers=self.headers,
                               json_body={"ids": [artist_id]})
        assert response.status_code == expected_status_code, \
            f"Ожидался код {expected_status_code}, получен {response.status_code}. Тело: {response.text}"
        return response

    @allure.step("API: Отписаться от артиста с ID {artist_id}")
    def unfollow_artist(self, artist_id: str, expected_status_code: int = 204) -> requests.Response:
        endpoint = "/me/following?type=artist"
        response = api_request(self.base_url, endpoint, method="DELETE", headers=self.headers,
                               json_body={"ids": [artist_id]})
        assert response.status_code == expected_status_code, \
            f"Ожидался код {expected_status_code}, получен {response.status_code}. Тело: {response.text}"
        return response