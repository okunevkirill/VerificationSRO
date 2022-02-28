from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Путь к файлу с ИД о компаниях для которых проводиться аудит
DATA_FRAMES_IN = Path(BASE_DIR, 'data_frames', 'DATA_FRAMES_IN.xlsx')
DATA_FRAMES_OUT = Path(BASE_DIR, 'data_frames', 'DATA_FRAMES_OUT.xlsx')

# Заголовки таблицы в файле `*.xlsx`
TABLE_HEADER_FIELDS = {
    'name': 'Компания',
    'uid': 'ИНН',
    'about': 'Информация о проверках',
    'audit_date': 'Дата последней проверки',
    'href': 'Адрес источника',
}

# Заголовки веб запроса
REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0",
    "Accept": "*/*",
}

# Предельное время ответа веб запроса в секундах
RESPONSE_TIME = 10

# Парсер для разбора веб страниц
HTML_PARSER = 'lxml'

# Число параллельных процессов парсинга
NUMBER_OF_PROCESSES = 42
