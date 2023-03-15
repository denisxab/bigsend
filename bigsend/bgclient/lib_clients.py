import asyncio

import os
import re
from pathlib import Path
from typing import AsyncGenerator

import aiohttp
import requests
from tqdm.asyncio import tqdm


class FileSender:
    def __init__(
        self,
        url: str,
        file_path: str,
        remote_path: str,
        block_size: int = 1024 * 1024,
    ):
        """
        :param url: адрес сервера
        :param file_path: путь до локального файла
        :param remote_path: путь до файла на сервере
        :param block_size: размер блока, в котором будет отправляться файл
        :param num_coroutine: количество одновременных запросов
        """
        self.url_upload = url + "/upload"
        self.url_create_file = url + "/create_file"
        self.file_path: Path = Path(file_path)
        self.block_size = block_size

        if re.match(r"[A-Z]:\\", remote_path):
            # Windows
            remote_path = str(Path(remote_path)) + "\\" + self.file_path.name
        else:
            # Unix
            remote_path = Path(remote_path) / self.file_path.name

        self.remote_path: Path = Path(remote_path)

    def _create_empty_file(self):
        """
        Создает пустой файл на сервере
        """
        response = requests.post(
            self.url_create_file,
            data={
                "remote_path": self.remote_path,
            },
        )
        if not response.ok:
            raise ValueError("Файл не создан на сервере. Отправка прекращена")

    def _block_generator(self) -> AsyncGenerator[bytes, None]:
        """
        Асинхронный генератор блоков файла
        """
        with open(self.file_path, "rb") as f:
            while True:
                block = f.read(self.block_size)
                if not block:
                    break
                yield block

    async def send(self) -> None:
        """
        Получение размера файла, создание пустого файла на сервере и отправка блоков файла в несколько потоков.
        """
        file_size = os.path.getsize(self.file_path)
        self._create_empty_file()
        loop = asyncio.get_running_loop()
        number_block = 0
        with tqdm(total=file_size, unit="B", unit_scale=True, miniters=1) as pbar:
            for block in self._block_generator():
                future = loop.create_task(
                    self._send_block(
                        block,
                        self.remote_path,
                        file_size,
                        pbar,
                        number_block,
                    )
                )
                await asyncio.gather(future)
                number_block += 1

    async def _send_block(
        self,
        block: bytes,
        remote_path: str,
        file_size: int,
        pbar: tqdm,
        number_block: int,
    ) -> bool:
        """
        Отправляет блок файла на сервер.

        Args:
            block (bytes): Блок файла, который необходимо отправить.
            remote_path (str): Путь на сервере, куда необходимо отправить файл.
            file_size (int): Размер файла, в байтах.
            pbar (tqdm): Индикатор прогресса.
            number_block (int): Номер текущего блока файла.

        Returns:
            bool: Результат выполнения запроса.

        """

        async with aiohttp.ClientSession() as session:
            form = aiohttp.FormData()
            form.add_field("file", block)
            form.add_field("remote_path", str(remote_path))
            form.add_field("file_size", str(file_size))
            form.add_field("number_block", str(number_block))
            async with session.post(self.url_upload, data=form) as response:
                pbar.set_description(f"Block={number_block}")
                pbar.update(len(block))
                return response.ok


if __name__ == "__main__":

    asyncio.run(
        FileSender(
            url="http://192.168.10.63:8000",
            # file_path="/home/denis/DISK/VM/kvm/data/pp.txt",
            file_path="/home/denis/DISK/VM/kvm/data/doc.zip",
            # remote_path=r"/home/denis/DISK/VM/kvm/data/pp.txt",
            remote_path=r"D:\VM",
        ).send()
    )
