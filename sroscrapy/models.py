from typing import Optional
import datetime


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


if __name__ == '__main__':
    pass
