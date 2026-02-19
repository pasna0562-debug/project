from typing import List, Dict, Any


def filter_by_state(list_data: List[Dict[str, Any]], state: str = 'EXECUTED') -> List[Dict[str, Any]]:
    """
    Фильтрует список словарей по значению ключа 'state'.

    :param data: Список словарей, каждый из которых содержит ключь 'state'.
    :param state:Значение состояния для фильтрации (по умолчанию 'EXECUTED').
    :return: Новый список словарей, у которых значение ключа 'state' совпадает с аргументом.
    """

    return [item for item in list_data if item.get('state') == state]


List_data = [{'id': 414288290, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}]


print(filter_by_state(List_data))


def sort_by_date(data: List[Dict[str, Any]], reverse: bool = True) -> List[Dict[str, Any]]:
    """
    Сортирует список словарей по дате.

    :param data: Список словарей, каждый из которых содержит ключ 'date'.
    :param reverse: Порядок сортировки. True-по убыванию (по умолчанию),
    False-по возрастанию.
    :return: Новый отсортированный список.
    """
    return sorted(data, key=lambda x: x['data'], reverse=reverse)


data = [{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}]


print(sort_by_date(data))

