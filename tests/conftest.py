import pytest
from datetime import datetime, timedelta
from typing import List, Tuple, Dict, Any, Union


# ===================== ФИКСТУРЫ ДЛЯ КАРТ =====================


@pytest.fixture
def valid_card_numbers() -> List[Tuple[str, str]]:
    """Фикстура с валидными номерами карт и ожидаемыми результатами"""
    return [
        ("7000792289606361", "7000 79** **** 6361"),
        ("1234567890123456", "1234 56** **** 3456"),
        ("1111222233334444", "1111 22** **** 4444"),
    ]


@pytest.fixture
def invalid_card_numbers() -> List[str]:
    """Фикстура с невалидными номерами карт"""
    return [
        "123",
        "12345678901234567890",
        "",
        "abcd1234efgh5678",
    ]


# ===================== ФИКСТУРЫ ДЛЯ СЧЕТОВ =====================


@pytest.fixture
def valid_account_numbers() -> List[Tuple[str, str]]:
    """Фикстура с валидными номерами счетов и ожидаемыми результатами"""
    return [
        ("73654108430135874305", "**4305"),
        ("1234567890", "**7890"),
        ("40817810099910004312", "**4312"),
    ]


@pytest.fixture
def invalid_account_numbers() -> List[str]:
    """Фикстура с невалидными номерами счетов"""
    return [
        "12",
        "123456789012345678901",
        "",
        "abcd1234",
    ]


# ===================== ФИКСТУРЫ ДЛЯ ДАТ =====================


@pytest.fixture
def valid_date_strings() -> List[Tuple[str, str]]:
    """Фикстура с валидными строками дат и ожидаемыми результатами"""
    return [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2023-12-31T23:59:59.999999", "31.12.2023"),
        ("2024-01-01T00:00:00.000000", "01.01.2024"),
    ]


@pytest.fixture
def invalid_date_strings() -> List[str]:
    """Фикстура с невалидными строками дат"""
    return [
        "2024",
        "2024-03",
        "",
        "invalid-date",
    ]


# ===================== ФИКСТУРЫ ДЛЯ ТРАНЗАКЦИЙ =====================


@pytest.fixture
def sample_transactions() -> List[Dict[str, Any]]:
    """Базовая фикстура с различными транзакциями"""
    return [
        {
            "id": 1,
            "state": "EXECUTED",
            "date": "2024-01-15T10:30:00.000",
            "amount": 1000,
            "currency": "RUB",
            "description": "Перевод организации"
        },
        {
            "id": 2,
            "state": "PENDING",
            "date": "2024-01-20T14:45:00.000",
            "amount": 2500,
            "currency": "USD",
            "description": "Перевод с карты на карту"
        },
    ]


@pytest.fixture
def mixed_state_transactions() -> List[Dict[str, Union[int, str]]]:
    """Фикстура с различными статусами для фильтрации"""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2024-01-15"},
        {"id": 2, "state": "PENDING", "date": "2024-01-20"},
        {"id": 3, "state": "CANCELED", "date": "2024-01-10"},
    ]


@pytest.fixture
def transactions_with_different_dates() -> List[Dict[str, Any]]:
    """Фикстура с транзакциями разных дат для тестирования сортировки"""
    today = datetime.now()

    return [
        {
            "id": 1,
            "state": "EXECUTED",
            "date": (today - timedelta(days=5)).isoformat(),
            "amount": 1000
        },
        {
            "id": 2,
            "state": "EXECUTED",
            "date": (today - timedelta(days=1)).isoformat(),
            "amount": 2000
        },
        {
            "id": 3,
            "state": "EXECUTED",
            "date": (today - timedelta(days=10)).isoformat(),
            "amount": 500
        },
        {
            "id": 4,
            "state": "EXECUTED",
            "date": today.isoformat(),
            "amount": 3000
        }
    ]


@pytest.fixture
def empty_transactions() -> List:
    """Фикстура с пустым списком"""
    return []


@pytest.fixture
def card_account_test_data() -> List[Tuple[str, str]]:
    """Фикстура с данными для тестирования функции mask_account_card"""
    return [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("MasterCard 5555666677778888", "MasterCard 5555 66** **** 8888"),
        ("Счет 73654108430135874305", "Счет **4305"),
        ("American Express 123456789012345", "American Express 1234 56** **** 3456"),
    ]


@pytest.fixture
def transactions_with_missing_fields() -> List[Dict[str, Any]]:
    """Фикстура с пропущенными полями"""
    return [
        {"id": 1, "state": "EXECUTED"},  # отсутствует date
        {"id": 2, "date": "2024-01-20"},  # отсутствует state
        {"state": "PENDING", "date": "2024-01-10"},  # отсутствует id
        {},  # пустой словарь
    ]


# ===================== ПАРАМЕТРИЗОВАННЫЕ ФИКСТУРЫ =====================


@pytest.fixture(params=[
    ("7000792289606361", "7000 79** **** 6361"),
    ("1234567890123456", "1234 56** **** 3456"),
])
def card_parametrized_data(request: Any) -> str:
    """Параметризованная фикстура для карт"""
    return str(request.param)


@pytest.fixture(params=[
    ("73654108430135874305", "**4305"),
    ("1234567890", "**7890"),
])
def account_parametrized_data(request: Any) -> str:
    """Параметризованная фикстура для счетов"""
    return str(request.param)


@pytest.fixture(params=[
    ("2024-03-11T02:26:18.671407", "11.03.2024"),
    ("2023-12-31T23:59:59.999999", "31.12.2023"),
])
def date_parametrized_data(request: Any) -> str:
    """Параметризованная фикстура для дат"""
    return str(request.param)


@pytest.fixture(params=[
    "EXECUTED",
    "PENDING",
    "CANCELED",
])
def transaction_state(request: Any) -> str:
    """Параметризованная фикстура для статусов транзакций"""
    return str(request.param)


# ===================== КОМБИНИРОВАННЫЕ ФИКСТУРЫ =====================


@pytest.fixture
def all_test_data(
    valid_card_numbers: List[Tuple[str, str]],
    valid_account_numbers: List[Tuple[str, str]],
    valid_date_strings: List[Tuple[str, str]]
) -> Dict[str, List[Tuple[str, str]]]:
    """Комбинированная фикстура со всеми тестовыми данными"""
    return {
        "cards": valid_card_numbers,
        "accounts": valid_account_numbers,
        "dates": valid_date_strings
    }


@pytest.fixture
def malformed_transactions():
    """Фикстура с транзакциями, имеющими неправильную структуру"""
    return [
        {
            "id": 1,
            "description": "Транзакция без operationAmount",
            "state": "EXECUTED"
        },
        {
            "id": 2,
            "operationAmount": {
                "amount": "100.00"
                # Отсутствует поле currency
            },
            "description": "Транзакция без currency"
        },
        {
            "id": 3,
            "operationAmount": {
                "amount": "200.00",
                "currency": {
                    "name": "USD"
                    # Отсутствует поле code
                }
            },
            "description": "Транзакция без code"
        },
        {
            "id": 4,
            "operationAmount": "это строка, а не словарь",
            "description": "Некорректный тип operationAmount"
        }
    ]


@pytest.fixture
def transactions_without_descriptions():
    """Фикстура с транзакциями, у которых нет описаний"""
    return [
        {
            "id": 1,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            # Отсутствует поле description
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702"
        },
        {
            "id": 2,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": None,  # Описание равно None
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188"
        },
        {
            "id": 3,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {
                "amount": "43318.34",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "",  # Пустое описание
            "from": "Visa Classic 6831982476737658",
            "to": "Visa Platinum 8990922113665229"
        }
    ]


@pytest.fixture
def mixed_transactions():
    """Фикстура со смешанными транзакциями (с описаниями и без)"""
    return [
        {
            "id": 1,
            "description": "Транзакция с описанием 1"
        },
        {
            "id": 2
            # Нет описания
        },
        {
            "id": 3,
            "description": "Транзакция с описанием 2"
        },
        {
            "id": 4,
            "description": None  # Описание равно None
        },
        {
            "id": 5,
            "description": ""  # Пустое описание
        },
        {
            "id": 6,
            "description": "Транзакция с описанием 3"
        }
    ]


@pytest.fixture
def single_transaction():
    """Фикстура с одной транзакцией"""
    return [
        {
            "id": 1,
            "description": "Единственная транзакция"
        }
    ]


# Фикстуры
@pytest.fixture
def small_range():
    """Фикстура с малым диапазоном номеров"""
    return (1, 5)


@pytest.fixture
def medium_range():
    """Фикстура со средним диапазоном номеров"""
    return (1000, 1010)


@pytest.fixture
def edge_range_start():
    """Фикстура с начальными значениями диапазона"""
    return (1, 10)


@pytest.fixture
def edge_range_end():
    """Фикстура с конечными значениями диапазона"""
    return (9999_9999_9999_9990, 9999_9999_9999_9995)
