import allure

@allure.feature("API: Медиатека")
@allure.story("Подписка и отписка от артиста")
@allure.label("owner", "AlishaMeier")
@allure.tag("positive", "api")
def test_follow_and_unfollow_artist(library_api):
    # ID Jin of BTS
    artist_id = "5vV3bFXnN6D6N3Nj4xRvaV"

    with allure.step(f"Подписка на артиста с ID {artist_id}"):
        follow_response = library_api.follow_artist(artist_id)

    with allure.step("Проверяем код ответа 204 No Content"):
        assert follow_response.status_code == 204, "Ожидался код 204 при подписке на артиста"

    with allure.step("Очистка: отписка от артиста"):
        unfollow_response = library_api.unfollow_artist(artist_id)
        assert unfollow_response.status_code == 204, "Ожидался код 204 при отписке от артиста"

@allure.feature("API: Медиатека")
@allure.story("Негативный кейс: подписка на несуществующего артиста")
@allure.label("owner", "AlishaMeier")
@allure.tag("negative", "api")
def test_follow_non_existent_artist(library_api):
    invalid_artist_id = "invalid_artist_id_12345"

    response = library_api.follow_artist(invalid_artist_id)

    with allure.step("Проверяем, что код ответа 400 (Bad Request)"):
        assert response.status_code == 400, "Ожидался код 400 при подписке на несуществующего артиста"