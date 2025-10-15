import os
import allure
from allure_commons.types import AttachmentType


# Скриншоты
def add_screenshot(browser):
    png = browser.driver.get_screenshot_as_png()
    allure.attach(body=png, name='screenshot', attachment_type=AttachmentType.PNG, extension='.png')

# логи
def add_logs(browser):
    try:

        logs = browser.driver.get_log('browser')
        log_text = "".join(f"{entry['message']}\n" for entry in logs)
    except Exception:

        log_text = "Browser logs are not available."


    import allure
    from allure_commons.types import AttachmentType
    allure.attach(log_text, name='browser_logs', attachment_type=AttachmentType.TEXT, extension='.log')


def add_html(browser):
    html = browser.driver.page_source
    allure.attach(html, 'page_source', AttachmentType.HTML, '.html')


def add_video(browser):
    selenoid_video_url = os.getenv("SELENOID_VIDEO_URL", "")
    if not selenoid_video_url:
        return  # если не задано в .env → не прикрепляем видео

    video_url = f"{selenoid_video_url}/{browser.driver.session_id}.mp4"

    html = (
        "<html><body>"
        f"<video width='100%' height='100%' controls autoplay>"
        f"<source src='{video_url}' type='video/mp4'>"
        "</video>"
        "</body></html>"
    )

    allure.attach(
        html,
        name="Video",
        attachment_type=AttachmentType.HTML,
        extension=".html"
    )