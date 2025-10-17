<p align="center">
  <img src="https://raw.githubusercontent.com/AlishaMeier/diploma_project_spotify/main/assets/img/spotify_automation_project.svg" width="80%" alt="Spotify Automation Testing Project"/>
</p>
<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Pytest-Testing-green?logo=pytest&logoColor=white"/>
  <img src="https://img.shields.io/badge/Allure-Report-ff69b4?logo=allure&logoColor=white"/>
  <img src="https://img.shields.io/badge/Spotify-API-1DB954?logo=spotify&logoColor=white"/>
  <img src="https://img.shields.io/badge/Selene-UI%20Tests-orange?logo=selenium&logoColor=white"/>
</p>

## 📘 О проекте

Spotify Automation Testing Project — дипломный проект, направленный на демонстрацию навыков автоматизации тестирования API и UI реального веб-приложения. (Mobile in progress)

Цель проекта — проверить корректность работы функционала Spotify (в рамках открытого Spotify Web API
) и пользовательского интерфейса (веб-версия Spotify) с использованием современных инструментов автоматизации.


### 🧩 **UI тесты**

| 🔍 Тест | 💡 Статус |
|---------------------------------------------|:--------:|
| Успешная авторизация пользователя | ✅ |
| Попытка входа с неверным паролем | ✅ |
| Попытка входа с пустыми полями | ✅ |
| Попытка входа с невалидным форматом логина | ✅ |
| Проверка отображения деталей трека в результатах поиска | ✅ |
| Проверка исправления опечаток в поисковых запросах | ✅ |
| Проверка сообщения при отсутствии результатов поиска | ✅ |
| Полный E2E-сценарий (создание плейлиста, его редактирование, добавление трека, удаление) | ✅ |


### ⚙️ **API тесты**

| 🔍 Тест | 💡 Статус |
|---------------------------------------------|:--------:|
| Получение данных текущего пользователя | ✅ |
| Получение данных публичного плейлиста | ✅ |
| [Негативный] Запрос несуществующего плейлиста | ✅ |
| [Негативный] Запрос плейлиста по невалидному ID | ✅ |
| Создание и последующее удаление плейлиста | ✅ |
| Добавление трека во временно созданный плейлист | ✅ |
| Добавление и последующее удаление трека из существующего плейлиста | ✅ |
| [Негативный] Создание плейлиста без имени | ✅ |
| [Негативный] Добавление трека с невалидным URI | ✅ |
| Добавление, проверка и удаление альбома из медиатеки | ✅ |
| [Негативный] Сохранение несуществующего альбома | ✅ |
| Подписка и отписка от артиста | ✅ |
| [Негативный] Подписка на несуществующего артиста | ✅ |





## 🔐 Авторизация в Spotify API 
<details>
<summary>Инструкция по авторизации в Spotify API </summary>


<br>Для запуска тестов, изменяющих данные пользователя (создание плейлистов, добавление треков, подписки), требуется `access_token` с определенными скоупами (scopes).

### Как получить токен:

1.  **Настройте приложение в Spotify Dashboard** (делается один раз):
    * Перейдите в [Dashboard](https://api.spotify.com/v1/me) и создайте новое приложение.
    * В настройках приложения (`Settings`) добавьте `https://example.com/callback` в поле **Redirect URIs** и сохраните изменения.

2.  **Сформируйте и перейдите по ссылке для авторизации**:
    * Соберите URL, подставив ваш `client_id` и необходимые `scopes`. [Пример ссылки со всеми нужными правами]([https://www.google.com/search?q=https://api.spotify.com/v14](https://accounts.spotify.com/authorize?response_type=code&client_id=19889471979142c990ed44cbc9982d57&scope=playlist-modify-public%20playlist-modify-private%20user-read-private%20user-follow-modify%20user-library-modify%20user-follow-modify%20user-read-email&redirect_uri=https://aboba:33/callback)).
    * Перейдите по ссылке, войдите в Spotify и разрешите доступ.

3.  **Обменяйте `code` на `access_token`**:
    * После подтверждения вас перенаправит на `example.com`. Скопируйте значение параметра `code` из адресной строки.
    * Выполните `curl`-запрос в терминале/postman, подставив ваш `code`, `client_id` и `client_secret`, чтобы получить `access_token`.

4.  **Сохраните токен**:
    * Вставьте полученный `access_token` в Jenkins в переменную `SPOTIFY_API_TOKEN`.

> **Важно**: `access_token` действует около 1 часа. Если тесты начнут падать с ошибкой 401, просто повторите процедуру для получения нового токена.

</details>

## 📚 Полезные ресурсы

- [Spotify Web API Reference](https://developer.spotify.com/documentation/web-api)
- [Spotify API Console](https://developer.spotify.com/console)
- [Allure Pytest Documentation](https://docs.qameta.io/allure/#_pytest)
- [Selene Documentation](https://yashaka.github.io/selene/)


## 👩‍💻 Автор

**Alisha Meier**  
QA Automation Engineer | Python + Pytest + Allure  
💬 [Написать в Telegram](https://t.me/cyber_neko)  


