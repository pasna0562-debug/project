import pytest
from typing import List, Dict, Any
from src2.processing import filter_by_state, sort_by_date


# ===================== ТЕСТЫ ДЛЯ filter_by_state =====================


def test_filter_by_state() -> None:
    """Тест фильтрации транзакций по статусу"""
    transactions = [
        {"id": 1, "state": "EXECUTED", "date": "2024-01-15"},
        {"id": 2, "state": "PENDING", "date": "2024-01-20"},
        {"id": 3, "state": "EXECUTED", "date": "2024-01-10"},
        {"id": 4, "state": "CANCELED", "date": "2024-01-25"},
    ]

    result = filter_by_state(transactions)

    assert len(result) == 2
    assert all(t["state"] == "EXECUTED" for t in result)
    assert result[0]["id"] == 1
    assert result[1]["id"] == 3


def test_filter_by_state_with_custom_state() -> None:
    """Тест фильтрации с пользовательским статусом"""
    transactions = [
        {"id": 1, "state": "EXECUTED", "date": "2024-01-15"},
        {"id": 2, "state": "PENDING", "date": "2024-01-20"},
        {"id": 3, "state": "CANCELED", "date": "2024-01-10"},
    ]

    result = filter_by_state(transactions, "PENDING")

    assert len(result) == 1
    assert result[0]["id"] == 2
    assert result[0]["state"] == "PENDING"


def test_filter_by_state_empty_list() -> None:
    """Тест фильтрации пустого списка"""
    result = filter_by_state([])
    assert result == []


def test_filter_by_state_no_matches() -> None:
    """Тест фильтрации без совпадений"""
    transactions = [
        {"id": 1, "state": "PENDING", "date": "2024-01-15"},
        {"id": 2, "state": "CANCELED", "date": "2024-01-20"},
    ]

    result = filter_by_state(transactions, "EXECUTED")

    assert result == []


def test_filter_by_state_with_missing_state() -> None:
    """Тест фильтрации с отсутствующим статусом"""
    transactions = [
        {"id": 1, "state": "EXECUTED", "date": "2024-01-15"},
        {"id": 2, "date": "2024-01-20"},  # отсутствует state
        {"id": 3, "state": "EXECUTED", "date": "2024-01-10"},
    ]

    result = filter_by_state(transactions)

    assert len(result) == 2
    assert result[0]["id"] == 1
    assert result[1]["id"] == 3


# ===================== ТЕСТЫ ДЛЯ sort_by_date =====================


def test_sort_by_date_descending() -> None:
    """Тест сортировки по дате по убыванию"""
    transactions = [
        {"id": 1, "date": "2024-01-15"},
        {"id": 2, "date": "2024-01-20"},
        {"id": 3, "date": "2024-01-10"},
        {"id": 4, "date": "2024-01-25"},
    ]

    result = sort_by_date(transactions, reverse=True)

    assert len(result) == 4
    assert result[0]["id"] == 4  # 2024-01-25
    assert result[1]["id"] == 2  # 2024-01-20
    assert result[2]["id"] == 1  # 2024-01-15
    assert result[3]["id"] == 3  # 2024-01-10


def test_sort_by_date_ascending() -> None:
    """Тест сортировки по дате по возрастанию"""
    transactions = [
        {"id": 1, "date": "2024-01-15"},
        {"id": 2, "date": "2024-01-20"},
        {"id": 3, "date": "2024-01-10"},
    ]

    result = sort_by_date(transactions, reverse=False)

    assert result[0]["id"] == 3  # 2024-01-10
    assert result[1]["id"] == 1  # 2024-01-15
    assert result[2]["id"] == 2  # 2024-01-20


def test_sort_by_date_empty_list() -> None:
    """Тест сортировки пустого списка"""
    result = sort_by_date([])
    assert result == []


def test_sort_by_date_missing_date() -> None:
    """Тест сортировки с отсутствующей датой"""
    data: List[Dict[str, Any]] = [
        {"id": 1, "date": "2024-01-15"},
        {"id": 2},  # отсутствует date
        {"id": 3, "date": "2024-01-10"},
        {"id": 4, "date": "2024-01-20"},
    ]

    result = sort_by_date(data)

    # Элементы с отсутствующей датой должны быть в конце
    assert result[-1]["id"] == 2
    assert result[0]["id"] == 3  # самая поздняя дата
    assert result[1]["id"] == 1
    assert result[2]["id"] == 4

def test_sort_by_date_same_dates() -> None:
    """Тест сортировки с одинаковыми датами"""
    transactions = [
        {"id": 1, "date": "2024-01-15"},
        {"id": 2, "date": "2024-01-15"},
        {"id": 3, "date": "2024-01-10"},
    ]

    result = sort_by_date(transactions)

    assert result[0]["id"] == 3
    assert result[1]["id"] in [1, 2]  # оба с датой 2024-01-15
    assert result[2]["id"] in [1, 2]
    assert result[1]["id"] != result[2]["id"]


# ===================== ПАРАМЕТРИЗОВАННЫЕ ТЕСТЫ =====================


@pytest.mark.parametrize("state,expected_count", [
    ("EXECUTED", 2),
    ("PENDING", 1),
    ("CANCELED", 1),
    ("UNKNOWN", 0),
])
def test_filter_by_state_parametrized(state: str, expected_count: int) -> None:
    """Параметризованный тест фильтрации"""
    transactions = [
        {"id": 1, "state": "EXECUTED", "date": "2024-01-15"},
        {"id": 2, "state": "PENDING", "date": "2024-01-20"},
        {"id": 3, "state": "EXECUTED", "date": "2024-01-10"},
        {"id": 4, "state": "CANCELED", "date": "2024-01-25"},
    ]

    result = filter_by_state(transactions, state)

    assert len(result) == expected_count


@pytest.mark.parametrize("reverse,expected_order", [
    (True, [4, 2, 1, 3]),  # по убыванию
    (False, [3, 1, 2, 4]),  # по возрастанию
])
def test_sort_by_date_parametrized(reverse: bool, expected_order: List[int]) -> None:
    """Параметризованный тест сортировки по дате"""
    transactions = [
        {"id": 1, "date": "2024-01-15"},
        {"id": 2, "date": "2024-01-20"},
        {"id": 3, "date": "2024-01-10"},
        {"id": 4, "date": "2024-01-25"},
    ]

    result = sort_by_date(transactions, reverse=reverse)

    assert [t["id"] for t in result] == expected_order


@pytest.mark.parametrize("transactions,expected_count", [
    ([], 0),
    ([{"id": 1, "state": "EXECUTED"}], 1),
    ([{"id": 1, "state": "PENDING"}], 0),
])
def test_filter_by_state_various_inputs(
        transactions: List[Dict[str, Any]],
        expected_count: int
) -> None:
    """Тест фильтрации с различными входными данными"""
    result = filter_by_state(transactions)
    assert len(result) == expected_count


def test_sort_by_date_with_fixture(transactions_with_different_dates: List[Dict[str, Any]]) -> None:
    """
    Тест сортировки транзакций по дате с использованием фикстуры.

    Args:
        transactions_with_different_dates: Фикстура с транзакциями
    """
    # Сортируем по убыванию даты (новые сначала)
    sorted_desc = sort_by_date(transactions_with_different_dates, reverse=True)

    # Проверяем, что самая новая дата первой
    assert sorted_desc[0]["date"] > sorted_desc[1]["date"], \
        f"Первая дата {sorted_desc[0]['date']} должна быть новее вторй {sorted_desc[1]['date']}"

    # Проверяем, что вторая дата больше третьей
    assert sorted_desc[1]["date"], \
    f"Вторая дата {sorted_desc[1]['date']} должна быть новее третьей {sorted_desc[2]['date']}"


def test_sort_by_date_ascending_with_fixture(transactions_with_different_dates: List[Dict[str, Any]]) -> None:
    """
    Тест сортировки по возрастанию даты (старые сначала).

    Args:
        transactions_with_different_dates: Фикстура с транзакциями
    """
    sorted_asc = sort_by_date(transactions_with_different_dates)
    dates = [t['date'] for t in sorted_asc]
    # Проверяем, что даты идут хронологическом порядке
    for i in range(len(dates) - 1):
        assert dates[i] < dates[i + 1], f"Даты не в порядке: {dates[i]} >= {dates[i + 1]}"
    # Или проще - сравниваем со встроенной сортировкой
    original_dates = [t['date'] for t in transactions_with_different_dates]
    assert dates == sorted(original_dates)
