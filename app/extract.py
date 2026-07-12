import re

def extract_car_id(href: str) -> int:
    match = re.search(r"/a/show/(\d+)", href)

    if match is None:
        raise ValueError(f"Не удалось извлечь car_id из ссылки: {href}")

    return int(match.group(1))