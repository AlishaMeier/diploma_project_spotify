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


def api_request(base_url, endpoint, method="GET", headers=None, params=None, json_body=None):

    url = f"{base_url}{endpoint}"
    method = method.upper()

    with allure.step(f"{method} {endpoint}"):
        allure.attach(
            json.dumps({
                "url": url,
                "method": method,
                "params": params,
                "body": json_body,
                "headers": headers
            }, indent=2, ensure_ascii=False),
            name="Request",
            attachment_type=allure.attachment_type.JSON
        )

        start_time = datetime.now()
        response = requests.request(method, url, headers=headers, params=params, json=json_body)
        elapsed = (datetime.now() - start_time).total_seconds()

        # консоль
        logger.info(f"{method} {url} -> {response.status_code} ({elapsed:.2f}s)")

        # allure
        try:
            response_json = response.json()
        except Exception:
            response_json = {"raw_text": response.text}

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
