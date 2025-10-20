import allure
import requests
import json
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)


def api_request(base_url, endpoint, method="GET", headers=None, params=None, json_body=None, data=None):
    url = f"{base_url}{endpoint}"
    method = method.upper()

    with allure.step(f"{method} {endpoint}"):

        request_body_log = {}
        if json_body:
            request_body_log = json_body
        elif data:
            request_body_log = f"<{len(data)} bytes of data (e.g., image). Truncated view: {str(data[:100])}...>"

        allure.attach(
            json.dumps({
                "url": url,
                "method": method,
                "params": params,
                "body": request_body_log,
                "headers": headers
            }, indent=2, ensure_ascii=False),
            name="Request",
            attachment_type=allure.attachment_type.JSON
        )

        start_time = datetime.now()

        # Поддержка json/data
        response = requests.request(
            method,
            url,
            headers=headers,
            params=params,
            json=json_body,
            data=data
        )

        elapsed = (datetime.now() - start_time).total_seconds()

        logger.info(f"{method} {url} -> {response.status_code} ({elapsed:.2f}s)")

        try:
            response_json = response.json()
        except requests.exceptions.JSONDecodeError:
            response_json = {"raw_text": response.text if response.text else "No Content"} #вдруг тело пустое

        allure.attach(
            json.dumps({
                "status_code": response.status_code,
                "elapsed": f"{elapsed:.2f}s",
                "response": response_json
            }, indent=2, ensure_ascii=False),
            name="Response",
            attachment_type=allure.attachment_type.JSON
        )

        return response