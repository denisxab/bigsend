import logging

import aiohttp
from aiohttp import web

# Настройки логирования
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)


async def handle_upload(request: web.Request) -> web.Response:
    """
    Заполнить файл
    :param request: объект запроса
    :return: объект ответа
    """
    # Получение информации о файле из POST-запроса
    post_data: aiohttp.web.MultiDictProxy = await request.post()
    remote_path: str = post_data["remote_path"]
    number_block: str = post_data["number_block"]
    file: aiohttp.web.FileField = post_data["file"]

    logging.info(f"[LOG]: Write number block = {number_block}")

    # Записываем данные в файл
    with open(remote_path, "ab") as f:
        f.write(file.file.read())

    # Отправка ответа об успешной загрузке файла
    return web.Response(text=f"Кусок успешно загружен number block = {number_block}")


async def handle_create_file(request: web.Request) -> web.Response:
    """
    Создать файл пустой по указанному пути
    :param request: объект запроса
    :return: объект ответа
    """
    # Получение информации о файле из POST-запроса
    post_data: aiohttp.web.MultiDictProxy = await request.post()
    remote_path: str = post_data["remote_path"]

    # Создаем пустой файл
    with open(remote_path, "wb") as f:
        pass
    logging.info(f"[LOG]: Файл успешно создан = {remote_path}")
    # Отправка ответа об успешной загрузке файла
    return web.Response(text=f"Файл успешно создан на сервере = {remote_path}")


def run(host="0.0.0.0", port=8000):
    app = web.Application()
    app.add_routes([web.post("/upload", handle_upload)])
    app.add_routes([web.post("/create_file", handle_create_file)])
    web.run_app(app, host=host, port=port)


if __name__ == "__main__":
    run()
