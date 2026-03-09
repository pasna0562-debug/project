from typing import List, Dict, Any

from black import datetime


def filter_by_state(list_data: List[Dict[str, Any]], state: str = 'EXECUTED') -> List[Dict[str, Any]]:
    """
    Фильтрует список словарей по значению ключа 'state'.

    :param data: Список словарей, каждый из которых содержит ключь 'state'.
    :param state:Значение состояния для фильтрации (по умолчанию 'EXECUTED').
    :return: Новый список словарей, у которых значение ключа 'state' совпадает с аргументом.
    """

    return [item for item in list_data if item.get('state') == state]


List_data = [
    {'id': 414288290, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
    {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
    {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
    {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
]


print(filter_by_state(List_data))


def sort_by_date(transactions: List[Dict[str, Any]], reverse: bool = False) -> List[Dict[str, Any]]:
    """
    Сортирует список словарей по дате.

    :param data: Список словарей, каждый из которых содержит ключ 'date'.
    :param reverse: Порядок сортировки. True-по убыванию (по умолчанию),
    False-по возрастанию.
    :return: Новый отсортированный список.
    """
    def parse_date(transactions: Dict[str, Any]) -> datetime:
        """Преобразуем строку с датой в обьект datetime"""
        date_str = transactions.get('date', '')
        # Если дата отсутствует или пустая строка
        if not date_str:
            return datetime.max if not reverse else datetime.min

        try:
            # Для формата ISO с временем (2028-03-07Т15:52:26.666660)
            return datetime.fromisoformat(date_str)
        except (ValueError, AttributeError):
            try:
                # Для формата без времени (2026-03-07)
                return datetime.fromisoformat(date_str)
            except (ValueError, AttributeError):
                try:
                    # Для формата без времени (2026-03-07)

                    return datetime.strftime(date_str, '%Y-%m-%d')
                except (ValueError, AttributeError):
                    # Если дата невалидна, возврашаем минимальную дату
                    return datetime.max if not reverse else datetime.min

    return sorted(transactions, key=parse_date, reverse=reverse)


data = [{'id': 41428829, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'}]


print(sort_by_date(data))
