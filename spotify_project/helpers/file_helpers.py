import base64
import os
import allure


@allure.step("Подготовка изображения '{file_name}' для загрузки (Base64)")
def encode_image_to_base64(file_name: str) -> bytes:

    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    image_path = os.path.join(base_dir, 'tests', 'resources', file_name)

    if not os.path.exists(image_path):
        image_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', '..', 'tests', 'resources', file_name)
        )

    assert os.path.exists(image_path), f"Файл не найден по пути: {image_path}"

    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()
        image_base64_bytes = base64.b64encode(image_data)

    return image_base64_bytes