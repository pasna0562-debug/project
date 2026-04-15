from typing import Iterator, Dict, Any, List


def filter_by_currency(transactions: List[Dict[str, Any]], currency: str) -> Iterator[Dict[str, Any]]:
    """
    Фильтрует транзакции по заданной валюте и возвращает итератор.

    Args:
        transactions: Список словарей с транзакциями
        currency: Код валюты для фильтрации (например, "USD", "RUB")

    Returns:
        Итератор, который выдает транзакции с указанной валютой
    """
    currency_code = "USD"
    target_code = currency_code.replace('.', '').upper()
    for transaction in transactions:
        # Проверяем, что транзакция содержит необходимые поля
        if 'operationAmount' in transaction:
            corrency = transaction['operationAmount'].get('currecy', {})
            code = corrency.get('code', '')
            normalized_code = code.strip().replace('.', '').upper()
            if normalized_code == target_code:
                yield transaction


# Пример использования
if __name__ == "__main__":
    transactions = [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702"
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188"
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {
                "amount": "43318.34",
                "currency": {
                    "name": "руб",
                    "code": "RUB"
                }
            },
            "description": "Перевод с карты на карту",
            "from": "Visa Classic 6831982476737658",
            "to": "Visa Platinum 8990922113665229"
        }
    ]

    # Фильтруем транзакции по USD
    usd_transactions = filter_by_currency(transactions, "USD")

    # Выводим первые две транзакции
    for _ in range(2):
        try:
            transaction = next(usd_transactions)
            print(transaction)
            print()
        except StopIteration:
            print("Нет больше транзакций")
            break


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Iterator[str]:
    """
    Генератор, который возвращает описания транзакций по очереди.

    Args:
        transactions: Список словарей с транзакциями

    Returns:
        Итератор, который выдает описания транзакций
    """
    for transaction in transactions:
        # Проверяем наличие поля 'description' в транзакции
        description = transaction.get('description')
        if description:
            yield description


# Пример использования
if __name__ == "__main__":
    transactions = [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702"
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188"
        },
        {
            "id": 895315941,
            "state": "EXECUTED",
            "date": "2018-08-19T04:27:37.904916",
            "operationAmount": {
                "amount": "56883.54",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 90817634362080076778",
            "to": "Счет 94237739715982558238"
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {
                "amount": "43318.34",
                "currency": {
                    "name": "руб",
                    "code": "RUB"
                }
            },
            "description": "Перевод с карты на карту",
            "from": "Visa Classic 6831982476737658",
            "to": "Visa Platinum 8990922113665229"
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {
                "amount": "67314.70",
                "currency": {
                    "name": "руб",
                    "code": "RUB"
                }
            },
            "description": "Перевод организации",
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211994348492008167"
        }
    ]

    # Получаем генератор описаний
    descriptions = transaction_descriptions(transactions)

    # Выводим первые 5 описаний
    print("Первые 5 описаний транзакций:")
    for i in range(5):
        try:
            description = next(descriptions)
            print(f"{i + 1}. {description}")
        except StopIteration:
            print("Нет больше описаний")
            break

    # Демонстрация работы генератора в цикле for
    print("\nВсе описания транзакций:")
    descriptions = transaction_descriptions(transactions)  # Создаем новый генератор
    for description in descriptions:
        print(f"- {description}")


def card_number_generator(start: int, end: int):
    """
    Генератор номеров банковских карт в заданном диапазоне.

    Args:
        start: Начальное значение (от 1 до 9999 9999 9999 9999)
        end: Конечное значение (от 1 до 9999 9999 9999 9999)

    Returns:
        Итератор, который выдает номера карт в формате "XXXX XXXX XXXX XXXX"
    """

    # Генерация номера
    if start < 1:
        raise ValueError("Некорректный диапазон номеров карт")

    if start > end:
        raise ValueError("Некорректный диапазон номеров карт")

    for number in range(start, end + 1):
        num_str = f"{number:016d}"
        formatted = f"{num_str[0:4]} {num_str[4:8]} {num_str[8:12]} {num_str[12:16]}"
        # Форматируем номер: 16 цифр с ведушими нулями
        yield formatted


# Пример использования
if __name__ == "__main__":
    print("Пример 1: Генерация номеров с 1 по 5")
    for card_number in card_number_generator(1, 5):
        print(card_number)

    print("\nПример 2: Генерация номеров с 9999999999999990 по 9999999999999995")
    for card_number in card_number_generator(9999_9999_9999_9990, 9999_9999_9999_9995):
        print(card_number)

    print("\nПример 3: Использование next() для пошагового получения номеров")
    generator = card_number_generator(100, 103)
    print(next(generator))  # 0000 0000 0000 0100
    print(next(generator))  # 0000 0000 0000 0101
    print(next(generator))  # 0000 0000 0000 0102
    print(next(generator))  # 0000 0000 0000 0103

    print("\nПример 4: Генерация нескольких номеров в цикле")
    for i, card_number in enumerate(card_number_generator(1000, 1005), 1):
        print(f"{i}: {card_number}")

    # Демонстрация обработки больших диапазонов
    print("\nПример 5: Генерация номеров с 9999999999999990 по 9999999999999995")
    for card_number in card_number_generator(9999_9999_9999_9990, 9999_9999_9999_9995):
        print(card_number)

    # Пример с обработкой ошибок
    print("\nПример 6: Обработка некорректного диапазона")
    try:
        for card_number in card_number_generator(10, 5):
            print(card_number)
    except ValueError as e:
        print(f"Ошибка: {e}")
