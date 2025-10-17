import allure
import requests
from spotify_project.schemas.user import UserProfile

@allure.feature("API: Профиль пользователя")
@allure.story("Получение данных текущего пользователя")
@allure.label("owner", "AlishaMeier")
@allure.tag("positive", "api", "smoke")
@allure.severity(allure.severity_level.CRITICAL)
def test_get_current_user_profile(api_base_url, headers, expected_display_name):

    with allure.step("Отправляем GET-запрос на /v1/me"):
        response = requests.get(
            f"{api_base_url}/me",
            headers=headers
        )

    with allure.step("Проверяем, что код ответа 200 (OK)"):
        assert response.status_code == 200, \
            f"Ожидался код 200, получен {response.status_code}. Тело ответа: {response.text}"

    with allure.step("Валидируем структуру ответа с помощью Pydantic"):
        user_profile = UserProfile.model_validate(response.json())

    with allure.step("Проверяем, что display_name в ответе совпадает с ожидаемым"):
        assert user_profile.display_name == expected_display_name, \
            f"Имя пользователя в ответе ('{user_profile.display_name}') не совпадает с ожидаемым ('{expected_display_name}')"

    with allure.step("Проверяем, что поле email не пустое"):
        assert user_profile.email is not None and "@" in user_profile.email