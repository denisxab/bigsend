# Описание

Данный проект представляет собой набор кода на языке Python для загрузки большого файла на сервер с помощью asyncio и aiohttp.

Код включает в себя клиентскую и серверную части для загрузки файла. Клиентский код используется для отправки файла на сервер, а серверный код - для принятия и сохранения файла на сервере.

## Как использовать

### Сервер

Для запуска сервера, необходимо запустить моудль `bgserver`. При запуске он начнет слушать запросы на указанном хосте и порте.

Для настройки хоста и порта, можно использовать аргументы командной строки:

```bash
python -m bgserver <host> <port>
```

По умолчанию хост и порт будут равны "0.0.0.0" и 8083 соответственно.

### Клиент

Для отправки файла на сервер, необходимо запустить модуль  `bgclient`. При запуске он отправит файл на сервер с указанным URL, путем к локальному файлу и путем до файла на сервере.

Для настройки URL, пути к локальному файлу и пути до файла на сервере, можно использовать аргументы командной строки:

```bash
python -m bgclient <url> <file_path> <remote_path>
```

Например, чтобы отправить файл example.zip на сервер с адресом <http://example.com> и сохранить его в папке /uploads, нужно выполнить следующую команду:

```bash
python -m bgclient <http://example.com> /path/to/example.zip /uploads/example.zip
```

## Требования

Для работы данного проекта необходимо наличие интерпретатора Python версии 3.7 и выше, а также установленных библиотек aiohttp, requests и tqdm.
