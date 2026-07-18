import logging

logger = logging.getLogger("My Logger")

logger.setLevel(logging.DEBUG)

handler = logging.FileHandler(filename="cars.log", encoding="utf-8")
handler.setLevel(logging.INFO)

handler_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(handler_format)

logger.addHandler(handler)