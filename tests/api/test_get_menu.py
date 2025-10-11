import requests

BASE_URL = "https://papajohns.ru/api/"

def test_get_menu_returns_200():
    response = requests.get(f"{BASE_URL}menu")
    assert response.status_code == 200
    assert "products" in response.json()
