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
IN PROGRESS

## 📚 Полезные ресурсы

- [Spotify Web API Reference](https://developer.spotify.com/documentation/web-api)
- [Spotify API Console](https://developer.spotify.com/console)
- [Allure Pytest Documentation](https://docs.qameta.io/allure/#_pytest)
- [Selene Documentation](https://yashaka.github.io/selene/)


## 👩‍💻 Автор

**Alisha Meier**  
QA Automation Engineer | Python + Pytest + Allure  
💬 [Написать в Telegram](https://t.me/cyber_neko)  


