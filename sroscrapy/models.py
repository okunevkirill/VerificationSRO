from typing import Optional
from abc import ABC, abstractmethod
import datetime
import pandas as pd
from pandas import DataFrame
import requests
import bs4

import sroscrapy.settings as settings


class Company:
    """
    Класс представления компании - члена участников СРО
    ...
    Атрибуты:
    name: str
        имя компании
    href: str
        ссылка на страницу с информацией о компании
    uid: Optional[str]
        идентификационный номер налогоплательщика
    audit_date: Optional[datetime.date]
        дата проведения последнего аудита
    about: str
        общие сведения о проведенных проверках
    date_change_flag: bool
        флаг наличия изменений даты последней проверки
    -------
    Методы
    is_name_match(name: str)
        Анализ совпадения переданного аргумента имени компании.
    is_audit_date_changed(date: datetime.date)
        Анализ изменения даты проведения последнего аудита.
    """

    def __init__(self, name: str, href: str = '', uid: Optional[str] = None,
                 audit_date: Optional[datetime.date] = None,
                 about: str = '', date_change_flag: bool = False):
        self.name = name
        self.href = href
        self.uid = uid
        self.audit_date = audit_date
        self.about = about
        self.date_change_flag = date_change_flag

    def __str__(self):
        return f"<class: '{self.__class__.__name__}'> name='{self.name}' audit_date='{self.audit_date}'"

    def is_name_match(self, name: str) -> bool:
        """
        Анализ совпадения переданного аргумента имени компании.
        :param name: Имя компании для сравнения.
        :return: Если имена совпадают (тождественны) - True, иначе - False
        """
        return self.name.strip().lower() == name.strip().lower()

    def is_audit_date_changed(self, date: datetime.date) -> bool:
        """
        Анализ изменения даты проведения последнего аудита.
        :param date: Дата проведения аудита для сравнения.
        :return: Если даты не совпадают (была изменена) - True, иначе - False.
        """
        return self.audit_date == date


class Website:
    """
    Класс представления вебсайта саморегулируемой организации.
    ...
    Атрибуты:
    name: str
        имя вебсайта
    url: str
        адрес ресурса в сети
    uri: Optional[str]
        адрес ресурса определяющий страницу списка членов СРО
    -------
    Методы
    get_uri(urn: str)
        Возвращает абсолютный адрес страницы
    """

    def __init__(self, name: str, url: str, uri: Optional[str] = None):
        self.name = name
        self.url = url
        self.uri = uri

    def __str__(self):
        return f"<class: '{self.__class__.__name__}'>\nname='{self.name}'\nurl={self.url}"

    def get_uri(self, urn: str) -> str:
        """
        Возвращает абсолютный адрес страницы.
        :param urn: Относительный адрес страницы.
        :return: Абсолютный адрес страницы
        """
        if urn.startswith('https://') or urn.startswith('http://'):
            return urn
        else:
            return f'{self.url}{urn}'


class File:
    """
    Класс представления для работы с файлами.
    ...
    Атрибуты:
    data_frame: Optional[DataFrame]
        Массив исходных данных
    -------
    Методы
    set_data_frame_from_xlsx(file: Optional[str], sheet_name: str)
        Устанавливает массив исходных данных из excel файла расположенного
        по пути `file` и имеющего имя рабочего листа `sheet_name`
        в атрибут `data_frame`.
    """

    def __init__(self, data_frame: Optional[DataFrame] = None):
        self.data_frame = data_frame

    def set_data_frame_from_xlsx(self, file: Optional[str] = None, sheet_name: str = 'list') -> None:
        """
        Устанавливает массив исходных данных из excel файла в атрибут `data_frame`.
        :param file: Путь к файлу.
        :param sheet_name: Имя рабочего листа.
        :return: None
        """
        if file is None:
            file = settings.DATA_FRAMES_IN
        try:
            self.data_frame = pd.read_excel(file, sheet_name=sheet_name)
        except FileNotFoundError as err:
            print(err)
            return

    def save_data_to_xlsx(self):
        pass


class Scrapper(ABC):
    """
    Класс представления сборщика информации с сайтов саморегулируемых организации.
    ...
    Атрибуты:
    request_headers
        заголовки веб запроса
    response_time
        предельное время ответа веб запроса в секундах
    html_parser
        парсер для разбора веб страниц
    -------
    Методы
    get_soup_page(uri: str, params)
        Получение древа объектов типа soup
    run()
        Запуск процесса веб-скрапинга сайтов компаний саморегулируемых организаций
    """

    def __init__(self, request_headers: Optional[dict] = None, response_time: Optional[int] = None,
                 html_parser: Optional[str] = None):
        if request_headers is None:
            request_headers = settings.REQUEST_HEADERS
        self.request_headers = request_headers

        if response_time is None:
            response_time = settings.RESPONSE_TIME
        elif response_time < 1:
            raise ValueError('Response time must be an integer greater than zero')
        self.response_time = response_time

        if html_parser is None:
            html_parser = settings.HTML_PARSER
        self.html_parser = html_parser

    def get_soup_page(self, uri: str, params=None) -> Optional[bs4.BeautifulSoup]:
        """
        Получение древа объектов типа soup
        :param uri: Абсолютный адрес страницы для парсинга.
        :param params: Словарь, список кортежей или байтов для отправки в строке запроса.
        :return: Древо объектов типа BeautifulSoup или None.
        """
        try:
            req = requests.get(uri, headers=self.request_headers, params=params, timeout=self.response_time)
        except requests.RequestException:
            return None
        if req.status_code != 200:
            return None
        return bs4.BeautifulSoup(req.text, self.html_parser)

    @abstractmethod
    def run(self):
        pass


if __name__ == '__main__':
    pass
