import allure
import requests
from pydantic import BaseModel, Field


class UserProfile(BaseModel):
    id: str
    display_name: str = Field(..., alias='display_name')
    email: str
    country: str

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

    @allure.step("API: Добавить трек в плейлист {playlist_id}")
    def add_track_to_playlist(self, playlist_id: str, track_uri: str):

        body = {"uris": [track_uri]}
        return requests.post(
            f"{self.base_url}/playlists/{playlist_id}/tracks",
            headers=self.headers,
            json=body
        )

    @allure.step("API: Удалить трек из плейлиста {playlist_id}")
    def delete_track_from_playlist(self, playlist_id: str, track_uri: str):

        body = {"tracks": [{"uri": track_uri}]}
        return requests.delete(
            f"{self.base_url}/playlists/{playlist_id}/tracks",
            headers=self.headers,
            json=body
        )