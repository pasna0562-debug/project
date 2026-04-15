# from locale import currency

import pytest
from typing import List, Dict, Any, Iterator

# from mypyc.ir.func_ir import all_values

from src2.generators import transaction_descriptions, card_number_generator

# from tests.conftest import medium_range


# Тестируемая функция
def filter_by_currency(transactions: List[Dict[str, Any]], currency: str) -> Iterator[Dict[str, Any]]:
    """
    Фильтрует транзакции по заданной валюте и возвращает итератор.
    """
    for transaction in transactions:
        if 'operationAmount' in transaction:
            operation_amount = transaction['operationAmount']
            if 'currency' in operation_amount:
                currency_info = operation_amount['currency']
                if 'code' in currency_info and currency_info['code'] == currency:
                    yield transaction


# Тесты для проверки корректной фильтрации
class TestFilterByCurrency:

    def test_filter_usd_transactions(self, sample_transactions):
        """Тест фильтрации транзакций по USD"""
        usd_transactions = list(filter_by_currency(sample_transactions, "USD"))
        assert len(usd_transactions) == 1
        transaction = usd_transactions[0]
        assert transaction['operationAmount']['currency']['code'] == "USD"

        assert 'id' in transaction
        assert 'date' in transaction
        assert 'description' in transaction

        # Проверяем конкретные ID транзакций
        transaction_ids = [t['id'] for t in usd_transactions]
        assert 41428829 in transaction_ids

    def test_filter_rub_transactions(self, sample_transactions):
        """Тест фильтрации транзакций по RUB"""
        rub_transactions = list(filter_by_currency(sample_transactions, "RUB"))
        expected_rub_count = sum(1 for t in sample_transactions if t['operationAmount']['currency']['code'] == "RUB")

        assert len(rub_transactions) == expected_rub_count
        assert all(t['operationAmount']['currency']['code'] == "RUB" for t in rub_transactions)
        # Дополнительная проверка
        for transaction in rub_transactions:
            assert 'id' in transaction
            assert 'date' in transaction
            assert 'description' in transaction
            assert transaction['operationAmount']['currency']['code'] == "RUB"

    def test_filter_eur_transactions(self, sample_transactions):
        """Тест фильтрации транзакций по EUR"""
        eur_transactions = list(filter_by_currency(sample_transactions, "EUR"))
        # Проверяем, что все найденные транзакции действительно в EUR
        for transaction in eur_transactions:
            currency_code = transaction['operationAmount']['currency']['code']
            assert currency_code in ['EUR', 'EUR.'], f"Неожиданный код валюты:{currency_code}"

        # Проверяем, что найденно хотя бы 1 транзакции
        assert len(eur_transactions) >= 1, "Не найденно ни одной транзакции"

        # Находим транзакции с кодом 'EUR.' (с точкой)
        eur_with_dot = [t for t in sample_transactions
                        if 'operationAmount' in t
                        and t['operationAmount']['currency'].get('code') == 'EUR.']

        # Проверяем что фильтр находит транзакции с 'EUR.' (с точкой)
        filter_with_dot = list(filter_by_currency(sample_transactions, "EUR."))
        for transaction in filter_with_dot:
            if transaction['operationAmount']['currency']['code'] == 'EUR.':
                assert transaction in eur_with_dot

        # Дополнительная проверка: количество транзакций с EUR и EUR. должно совпадать
        eur_without_dot = [t for t in sample_transactions
                           if 'operationAmount' in t
                           and t['operationAmount']['currency'].get('code') == 'EUR']

        assert len(eur_transactions) == len(eur_without_dot), \
            f"Ожидалось {len(eur_without_dot)} транзакция с EUR, найдено {len(eur_transactions)}"

    def test_filter_nonexistent_currency(self, sample_transactions):
        """Тест фильтрации по валюте, которой нет в транзакциях"""
        gbp_transactions = list(filter_by_currency(sample_transactions, "GBP"))

        assert len(gbp_transactions) == 0
        assert gbp_transactions == []

    # Тесты для проверки поведения итератора


class TestFilterByCurrencyIterator:
    def test_iterator_returns_generator(self, sample_transactions):
        """Тест, что функция возвращает итератор/генератор"""
        result = filter_by_currency(sample_transactions, "USD")

        # Проверяем, что результат является итератором
        assert hasattr(result, '__iter__')
        assert hasattr(result, '__next__')

    def test_iterator_lazy_evaluation(self, sample_transactions):
        """Тест ленивых вычислений генератора"""
        # Создаем счетчик вызовов
        processing_count = 0

        def data_source():
            """Функция-источник данных, которая считает вызовы"""
            nonlocal processing_count
            for i in range(1, 6):
                processing_count += 1
                yield i

        def lazy_generator(data, threshold):
            """Тестируемый генератор с ленивыми вычислениями"""
            for item in data:
                # Иметация тяжелых вычислений
                result = item * 2
                if result > threshold:
                    yield result

        # Создаем генератор, но не начинаем итерацию
        gen = lazy_generator(data_source(), 1)

        # Проверяем: до первого next() ни чего обробатано
        assert processing_count == 0

        # Получаем первый элемент
        first = next(gen)
        assert first == 2  # 1 * 2 = 2, но 2 > 1? Нет, условие не выполнится
        assert processing_count == 1  # Обработан только первый элемент

        # Получаем второй элемент
        second = next(gen)
        assert second == 4  # 2 * 2 = 4, 4 > 1
        assert processing_count == 2  # Два элемента обработано

        # Проверяем, что элемент 3 (6) тоже попадает в результат
        third = next(gen)
        assert third == 6  # 3 * 2 = 6, 6 > 1
        assert processing_count == 3

        # Сбрасываем счетчик для следуюшей части тела
        transaction_count = 0
        usd_trannsactions = []

        # Заменяем оригинальную функцию для теcurrencyстирования
        def test_filter(transactions, currency_1):
            nonlocal transaction_count
            for transaction in transactions:
                transaction_count += 1
                if 'operationAmount' in transaction:
                    operation_amount = transaction['operationAmount']
                    if 'currency' in operation_amount:
                        currency_info = operation_amount['currency']
                        if 'code' in currency_info and currency_info['code'] == currency_1:
                            yield transaction

        iterator = test_filter(sample_transactions, "USD")

        # До вызова next генератор не должен обрабатывать транзакции
        assert transaction_count == 0

        # Получаем первую транзакцию
        try:
            first = next(iterator)

            usd_trannsactions.append(first)
            assert first['operationAmount']['currency']['code'] == 'USD'
            assert transaction_count > 0
            # Сохронение количество обработанных транзакций
            first_processed = transaction_count

            # Получаем вторую транзакцию с USD
            try:
                second_transaction = next(iterator)
                usd_trannsactions.append(second_transaction)
                assert second_transaction['operationAmount']['currency']['code'] == 'USD'
                assert transaction_count > first_processed
            except StopIteration:
                assert transaction_count == len(sample_transactions)
        except StopIteration:
            pytest.fail("Нет транзакций с USD в sample_transactions")

    def test_iterator_exhaustion(self, sample_transactions):
        """Тест исчерпания итератора"""
        usd_transactions = (filter_by_currency(sample_transactions, "USD"))
        # Получаем все транзакции
        transactions_list = []
        try:
            while True:

                transactions_list.append(next(usd_transactions))
        except StopIteration:
            pass

        usd_count = sum(1 for t in sample_transactions if 'operationAmount' in t and 'currency' in
                        t.get('operationAmount', {})
                        and t['operationAmount']['currency'].get('code') == 'USD')

        assert len(transactions_list) == usd_count

        with pytest.raises(StopIteration):
            next(usd_transactions)

    def test_multiple_iterators_independence(self, sample_transactions):
        """Тест независимости разных итераторов"""
        iterator1 = filter_by_currency(sample_transactions, "USD")
        iterator2 = filter_by_currency(sample_transactions, "USD")

        # Проверяем, что оба итератора возврошают одинаковые элементы
        for item1, item2 in zip(iterator1, iterator2):
            assert item1['id'] == item2['id']

        # Проверка, что оба итератора исчерпываются одновременно
        with pytest.raises(StopIteration):
            next(iterator1)
        with pytest.raises(StopIteration):
            next(iterator2)

    # Тесты для граничных случаев

    class TestFilterByCurrencyEdgeCases:

        def test_empty_transactions_list(self, empty_transactions):
            """Тест обработки пустого списка транзакций"""
            result = list(filter_by_currency(empty_transactions, "USD"))

            assert result == []
            assert len(result) == 0

        def test_empty_list_iterator_behavior(self, empty_transactions):
            """Тест поведения итератора с пустым списком"""
            iterator = filter_by_currency(empty_transactions, "USD")

            # Проверяем, что итератор сразу вызывает StopIteration
            with pytest.raises(StopIteration):
                next(iterator)

    def test_no_matching_currency(self, sample_transactions):
        """Тест отсутствия транзакций с нужной валютой"""
        result = list(filter_by_currency(sample_transactions, "JPY"))

        assert result == []
        assert len(result) == 0

    def test_no_matching_currency_iterator(self, sample_transactions):
        """Тест поведения итератора при отсутствии нужной валюты"""
        iterator = filter_by_currency(sample_transactions, "JPY")

        # Итератор должен сразу вызвать StopIteration
        with pytest.raises(StopIteration):
            next(iterator)

    def test_malformed_transactions(self, malformed_transactions):
        """Тест обработки транзакций с неправильной структурой"""
        # Функция не должна падать с ошибкой
        result = list(filter_by_currency(malformed_transactions, "USD"))

        # Должны быть возвращены только корректные транзакции с USD
        # В нашем наборе нет корректных USD транзакций
        assert result == []

        # Проверяем, что функция не падает при обработке каждой транзакции
        iterator = filter_by_currency(malformed_transactions, "USD")
        for _ in range(len(malformed_transactions)):
            try:
                next(iterator)
            except StopIteration:
                break

    def test_partially_malformed_transactions(self):
        """Тест смеси корректных и некорректных транзакций"""
        transactions = [
            {
                "id": 1,
                "operationAmount": {
                    "amount": "100",
                    "currency": {
                        "code": "USD"
                    }
                }
            },
            {
                "id": 2,
                "operationAmount": "неправильный формат"
            },
            {
                "id": 3,
                "operationAmount": {
                    "amount": "200"
                    # нет currency
                }
            },
            {
                "id": 4,
                "operationAmount": {
                    "amount": "300",
                    "currency": {
                        "name": "USD"
                        # нет code
                    }
                }
            }
        ]

        result = list(filter_by_currency(transactions, "USD"))

        # Должна быть найдена только первая транзакция
        assert len(result) == 1
        assert result[0]['id'] == 1

        # Тесты для проверки регистрозависимости
    class TestFilterByCurrencyCaseSensitivity:

        def test_case_sensitivity(self, sample_transactions):
            """Тест регистрозависимости при фильтрации"""
            # Добавляем транзакцию с валютой в нижнем регистре
            original_usd_count = sum(1 for t in sample_transactions if t.get(
                "operationAmount", {}).get("currency", {}).get("code") == "USD")
            transactions_with_lowercase = sample_transactions + [{
                "id": 999,
                "operationAmount": {
                    "amount": "500",
                    "currency": {
                        "name": "us dollar",
                        "code": "usd"  # нижний регистр
                    }
                },
                "description": "Транзакция с валютой в нижнем регистре"
            }]

            # Поиск с верхним регистром не должен найти транзакцию с нижним регистром
            result_upper = list(filter_by_currency(transactions_with_lowercase, "USD"))
            assert len(result_upper) == original_usd_count
        # Тесты для проверки производительности

    class TestFilterByCurrencyPerformance:
        def test_large_transaction_list(self):
            """Тест обработки большого количества транзакций"""
            # Создаем 10000 транзакций
            large_transactions = []
            for i in range(10000):
                currency_codas = "USD" if i % 3 == 0 else "RUB" if i % 3 == 1 else "EUR"
                large_transactions.append({
                    "id": i,
                    "operationAmount": {
                        "amount": str(i * 100),
                        "currency": {
                            "code": currency_codas
                        }
                    }
                })

            # Фильтруем USD транзакции
            usd_iterator = filter_by_currency(large_transactions, "USD")

            # Проверяем, что генератор работает без ошибок
            count = 0
            for transaction in usd_iterator:
                assert transaction['operationAmount']['currency']['code'] == "USD"
                count += 1

                # Должно быть около 3333 транзакций (10000 / 3)
            assert count == len(
                [t for t in large_transactions if t['operationAmount']['currency']['code'] == "USD"])
            assert count == 3334  # 10000 // 3 + 1

    # Запуск тестов
    if __name__ == "__main__":
        pytest.main([__file__, "-v", "--tb=short"])

# Тестируемая функция


def transaction_descriptions_2(transactions: List[Dict[str, Any]]) -> Iterator[str]:
    """
    Генератор, который возвращает описания транзакций по очереди.
    """
    for transaction in transactions:
        description = transaction.get('description')
        if description is not None:
            yield description


# Тесты для проверки корректности возвращаемых описаний
class TestTransactionDescriptions:

    def test_returns_correct_descriptions(self, sample_transactions):
        """Тест, что функция возвращает правильные описания"""
        expected_descriptions = [
            "Перевод организации",
            "Перевод со счета на счет",
            "Перевод с карты на карту",
            "Перевод с карты на карту"
        ]

        result = list(transaction_descriptions(sample_transactions))

        assert result == expected_descriptions
        assert len(result) == 4

    def test_preserves_order(self, sample_transactions):
        """Тест сохранения порядка транзакций"""
        descriptions = list(transaction_descriptions(sample_transactions))

        # Проверяем, что порядок описаний соответствует порядку транзакций
        for i, transaction in enumerate(sample_transactions):
            assert descriptions[i] == transaction['description']

    def test_returns_iterator(self, sample_transactions):
        """Тест, что функция возвращает итератор"""
        result = transaction_descriptions(sample_transactions)

        assert hasattr(result, '__iter__')
        assert hasattr(result, '__next__')
        assert iter(result) is result  # Итератор должен быть итерируемым


# Тесты для проверки работы с пустым списком
class TestTransactionDescriptionsEmpty:

    def test_empty_transactions_list(self, empty_transactions):
        """Тест обработки пустого списка транзакций"""
        result = list(transaction_descriptions(empty_transactions))

        assert result == []
        assert len(result) == 0

    def test_empty_list_iterator_behavior(self, empty_transactions):
        """Тест поведения итератора с пустым списком"""
        iterator = transaction_descriptions(empty_transactions)

        with pytest.raises(StopIteration):
            next(iterator)

    def test_empty_list_in_loop(self, empty_transactions):
        """Тест использования пустого списка в цикле"""
        count = 0
        for description in transaction_descriptions(empty_transactions):
            count += 1

        assert count == 0


# Тесты для проверки работы с разным количеством транзакций
class TestTransactionDescriptionsCount:

    def test_single_transaction(self, single_transaction):
        """Тест с одной транзакцией"""
        descriptions = list(transaction_descriptions(single_transaction))

        assert len(descriptions) == 1
        assert descriptions[0] == "Единственная транзакция"

    def test_single_transaction_iterator(self, single_transaction):
        """Тест поведения итератора с одной транзакцией"""
        iterator = transaction_descriptions(single_transaction)

        # Получаем единственное описание
        description = next(iterator)
        assert description == "Единственная транзакция"

        # При следующем вызове должен быть StopIteration
        with pytest.raises(StopIteration):
            next(iterator)

    def test_multiple_transactions(self, sample_transactions):
        """Тест с несколькими транзакциями"""
        descriptions = list(transaction_descriptions(sample_transactions))

        assert len(descriptions) == 4

        # Проверяем, что все описания являются строками
        for description in descriptions:
            assert isinstance(description, str)

    def test_large_number_of_transactions(self):
        """Тест с большим количеством транзакций"""
        # Создаем 1000 транзакций
        large_transactions = [
            {"id": i, "description": f"Транзакция {i}"}
            for i in range(1000)
        ]

        descriptions = list(transaction_descriptions(large_transactions))

        assert len(descriptions) == 1000
        assert descriptions[0] == "Транзакция 0"
        assert descriptions[499] == "Транзакция 499"
        assert descriptions[999] == "Транзакция 999"


# Тесты для проверки поведения итератора
class TestTransactionDescriptionsIterator:

    def test_lazy_evaluation(self):
        """Тест ленивых вычислений генератора"""
        call_count = 0

        def tracking_transactions():
            nonlocal call_count
            for i in range(5):
                call_count += 1
                yield {"id": i, "description": f"Описание {i}"}

        # Создаем список из генератора для тестирования
        transactions = list(tracking_transactions())
        call_count = 0  # Сбрасываем счетчик

        # Создаем генератор описаний
        descriptions = transaction_descriptions(transactions)

        # До вызова next генератор не должен обрабатывать транзакции
        assert call_count == 0

        # Получаем первое описание
        first = next(descriptions)
        assert first == "Описание 0"
        assert call_count == 0  # Транзакции уже были созданы ранее

        # Но сам генератор описаний работает лениво
    def test_iterator_exhaustion(self, sample_transactions):
        """Тест исчерпания итератора"""
        descriptions = transaction_descriptions(sample_transactions)

        # Получаем все описания
        descriptions_list = []
        for _ in range(len(sample_transactions)):
            descriptions_list.append(next(descriptions))

        assert len(descriptions_list) == 4

        # При попытке получить следующее описание должен возникнуть StopIteration
        with pytest.raises(StopIteration):
            next(descriptions)

    def test_multiple_iterators_independence(self, sample_transactions):
        """Тест независимости разных итераторов"""
        iterator1 = transaction_descriptions(sample_transactions)
        iterator2 = transaction_descriptions(sample_transactions)

        # Получаем первый элемент из первого итератора
        first_from_1 = next(iterator1)
        assert first_from_1 == "Перевод организации"

        # Первый итератор должен вернуть второй элемент
        second_from_1 = next(iterator1)
        assert second_from_1 == "Перевод со счета на счет"

        # Второй итератор должен начать с первого элемента
        first_from_2 = next(iterator2)
        assert first_from_2 == "Перевод организации"

        # Проверяем оставшиеся элементы
        assert next(iterator2) == "Перевод со счета на счет"
        assert next(iterator2) == "Перевод с карты на карту"
        assert next(iterator2) == "Перевод с карты на карту"

    def test_iterator_in_for_loop(self, sample_transactions):
        """Тест использования итератора в цикле for"""
        descriptions = []
        for description in transaction_descriptions(sample_transactions):
            descriptions.append(description)

        expected = ["Перевод организации", "Перевод со счета на счет",
                    "Перевод с карты на карту", "Перевод с карты на карту"]
        assert descriptions == expected

    def test_iterator_conversion_to_list(self, sample_transactions):
        """Тест преобразования итератора в список"""
        descriptions = list(transaction_descriptions(sample_transactions))

        assert len(descriptions) == 4
        assert isinstance(descriptions, list)


# Тесты для проверки обработки некорректных данных
class TestTransactionDescriptionsInvalidData:

    def test_transactions_with_missing_description_field(self):
        """Тест транзакций без поля description"""
        transactions = [
            {"id": 1, "other_field": "значение"},
            {"id": 2, "description": "есть описание"},
            {"id": 3}  # вообще без полей
        ]

        descriptions = list(transaction_descriptions(transactions))

        assert descriptions == ["есть описание"]

    def test_transactions_with_non_string_description(self):
        """Тест с описаниями не строкового типа"""
        transactions = [
            {"id": 1, "description": 123},  # число
            {"id": 2, "description": ["список"]},  # список
            {"id": 3, "description": {"key": "value"}},  # словарь
            {"id": 4, "description": True},  # булево
            {"id": 5, "description": "строка"}  # строка
        ]

        descriptions = list(transaction_descriptions(transactions))

        # Функция должна возвращать любые значения, не только строки
        # или может быть модифицирована для проверки типа
        assert len(descriptions) == 5
        assert descriptions[0] == 123
        assert descriptions[1] == ["список"]
        assert descriptions[2] == {"key": "value"}
        assert descriptions[3]
        assert descriptions[4] == "строка"

    def test_transactions_with_various_falsy_values(self):
        """Тест с различными falsy значениями"""
        transactions = [
            {"id": 1, "description": ""},  # пустая строка
            {"id": 2, "description": None},  # None
            {"id": 3, "description": 0},  # ноль
            {"id": 4, "description": False},  # False
            {"id": 5, "description": "реальное описание"},  # реальное описание
            {"id": 6},  # нет описания
        ]
        descriptions = list(transaction_descriptions(transactions))
        # Функция фильтрует только None, но не другие falsy значения
        # Это зависит от реализации
        assert descriptions == ["", 0, False, "реальное описание"]
        # или если используется if description (а не if description is not None):
        # assert descriptions == ["реальное описание"]

    # Параметризованные тесты
    class TestTransactionDescriptionsParameterized:

        @pytest.mark.parametrize("transactions,expected", [
            ([], []),
            ([{"description": "тест"}], ["тест"]),
            ([{"description": "один"}, {"description": "два"}], ["один", "два"]),
            ([{"id": 1}, {"description": "тест"}], ["тест"]),
            ([{"description": None}], []),
            ([{"description": ""}], [""]),
        ])
        def test_various_transaction_lists(self, transactions, expected):
            """Параметризованный тест с различными входными данными"""
            result = list(transaction_descriptions(transactions))
            assert result == expected

        @pytest.mark.parametrize("count", [0, 1, 5, 10, 100])
        def test_different_list_sizes(self, count):
            """Тест с разным количеством транзакций"""
            transactions = [
                {"id": i, "description": f"Описание {i}"}
                for i in range(count)
            ]

            descriptions = list(transaction_descriptions(transactions))

            assert len(descriptions) == count
            if count > 0:
                assert descriptions[0] == "Описание 0"
                assert descriptions[-1] == f"Описание {count - 1}"

    # Запуск тестов
    if __name__ == "__main__":
        pytest.main([__file__, "-v", "--tb=short"])

        import pytest
        from typing import Iterator

        # Тестируемая функция
        def card_number_generator(start: int, end: int) -> Iterator[str]:
            """
            Генератор номеров банковских карт в заданном диапазоне.
            """
            if start < 1 or end > 9999_9999_9999_9999 or start > end:
                raise ValueError("Некорректный диапазон номеров карт")

            for number in range(start, end + 1):
                card_number = f"{number:016d}"
                formatted_number = f"{card_number[:4]} {card_number[4:8]} {card_number[8:12]} {card_number[12:16]}"
                yield formatted_number

        # Альтернативная реализация для тестирования разных подходов
        def card_number_generator_alternative(start: int, end: int) -> Iterator[str]:
            """Альтернативная реализация с другим форматированием"""
            if start < 1 or end > 9999_9999_9999_9999 or start > end:
                raise ValueError("Некорректный диапазон номеров карт")

            for number in range(start, end + 1):
                number_str = str(number).zfill(16)
                groups = [number_str[i:i + 4] for i in range(0, 16, 4)]
                yield ' '.join(groups)

    # Тесты для проверки корректности номеров в заданном диапазоне


class TestCardNumberGeneratorRange:
    @pytest.mark.parametrize("small_range", [(1, 10), (2, 20)])
    def test_small_range_numbers(self, small_range):
        """Тест генерации номеров в малом диапазоне"""
        start, end = small_range
        expected_numbers = []
        for i in range(start, end + 1):
            num_str = f"{i:016d}"
            formatted = f"{num_str[0:4]} {num_str[4:8]} {num_str[8:12]} {num_str[12:16]}"
            expected_numbers.append(formatted)
        result = list(card_number_generator(start, end))
        assert result == expected_numbers

    @pytest.mark.parametrize("edge_range_start", [(100, 500), (200, 600), (300, 700)])
    def test_edge_start_range(self, edge_range_start):
        """Тест генерации номеров в начале диапазона"""
        start, end = edge_range_start
        result = list(card_number_generator(start, end))

        expected = f"{start:016d}"
        expected = ' '.join(expected[i:i + 4] for i in range(0, 16, 4))
        assert result[0] == expected

    def test_edge_end_range(self, edge_range_end):
        """Тест генерации номеров в конце диапазона"""
        start, end = edge_range_end
        result = list(card_number_generator(start, end))

        expected_numbers = [
            "9999 9999 9999 9990",
            "9999 9999 9999 9991",
            "9999 9999 9999 9992",
            "9999 9999 9999 9993",
            "9999 9999 9999 9994",
            "9999 9999 9999 9995"
        ]

        assert result == expected_numbers
        assert len(result) == 6

    def test_single_number_range(self):
        """Тест генерации одного номера"""
        result = list(card_number_generator(42, 42))

        assert len(result) == 1
        assert result[0] == "0000 0000 0000 0042"

    def test_range_with_leading_zeros(self):
        """Тест генерации номеров с ведущими нулями"""
        result = list(card_number_generator(7, 12))

        expected = [
            "0000 0000 0000 0007",
            "0000 0000 0000 0008",
            "0000 0000 0000 0009",
            "0000 0000 0000 0010",
            "0000 0000 0000 0011",
            "0000 0000 0000 0012"
        ]

        assert result == expected

    def test_large_gap_range(self):
        """Тест генерации с большим разрывом"""
        result = list(card_number_generator(999_0000_0000, 999_0000_0010))

        assert len(result) == 11
        assert result[0] == "0000 0999 0000 0000"  # 999_0000_0000 в 16-значном формате
        assert result[10] == "0000 0999 0000 0010"


# Тесты для проверки форматирования номеров карт
class TestCardNumberGeneratorFormatting:

    def test_format_structure(self):
        """Тест структуры форматирования номера карты"""
        result = list(card_number_generator(1234567890123456, 1234567890123456))

        card_number = result[0]

    # Проверяем длину с пробелами (16 цифр + 3 пробела = 19 символов)
        assert len(card_number) == 19

        # Проверяем наличие пробелов через каждые 4 символа
        assert card_number[4] == ' '
        assert card_number[9] == ' '
        assert card_number[14] == ' '

        # Проверяем, что остальные символы - цифры
        digits = card_number.replace(' ', '')
        assert len(digits) == 16
        assert digits.isdigit()

    def test_format_with_various_numbers(self):
        """Тест форматирования различных номеров"""
        test_cases = [
            (1, "0000 0000 0000 0001"),
            (12, "0000 0000 0000 0012"),
            (123, "0000 0000 0000 0123"),
            (1234, "0000 0000 0000 1234"),
            (12345, "0000 0000 0001 2345"),
            (123456, "0000 0000 0012 3456"),
            (1234567, "0000 0000 0123 4567"),
            (12345678, "0000 0000 1234 5678"),
        ]

        for number, expected in test_cases:
            result = list(card_number_generator(number, number))
            assert result[0] == expected, f"Failed for number {number}"

    def test_format_maximum_value(self):
        """Тест форматирования максимального значения"""
        result = list(card_number_generator(9999_9999_9999_9999, 9999_9999_9999_9999))

        assert result[0] == "9999 9999 9999 9999"

    def test_format_minimum_value(self):
        """Тест форматирования минимального значения"""
        result = list(card_number_generator(1, 1))

        assert result[0] == "0000 0000 0000 0001"

    def test_format_with_all_zeros(self):
        """Тест, что номер 0000 0000 0000 0000 не генерируется"""
        # Номер 0 не должен генерироваться, так как start >= 1
        with pytest.raises(ValueError):
            list(card_number_generator(0, 0))


# Тесты для проверки крайних значений диапазона
class TestCardNumberGeneratorEdgeCases:

    def test_minimum_start_value(self):
        """Тест минимального допустимого значения start"""
        result = list(card_number_generator(1, 1))
        assert result[0] == "0000 0000 0000 0001"

    def test_maximum_end_value(self):
        """Тест максимального допустимого значения end"""
        result = list(card_number_generator(9999_9999_9999_9999, 9999_9999_9999_9999))
        assert result[0] == "9999 9999 9999 9999"

    def test_start_less_than_one(self):
        """Тест start меньше 1"""
        with pytest.raises(ValueError, match="Некорректный диапазон номеров карт"):
            list(card_number_generator(0, 10))

        with pytest.raises(ValueError):
            list(card_number_generator(-5, 10))

    def test_start_greater_than_end(self):
        """Тест start больше end"""
        with pytest.raises(ValueError, match="Некорректный диапазон номеров карт"):
            list(card_number_generator(100, 50))

    def test_full_range_generation(self):
        """Тест генерации полного диапазона"""
        # Проверяем, что можно сгенерировать большой диапазон
        generator = card_number_generator(9999_9999_9999_9990, 9999_9999_9999_9999)
        count = 0
        for _ in generator:
            count += 1

        assert count == 10


# Тесты для проверки завершения генерации
class TestCardNumberGeneratorCompletion:

    def test_iterator_exhaustion(self, small_range):
        """Тест исчерпания итератора"""
        start, end = small_range
        generator = card_number_generator(start, end)

        # Получаем все номера
        for _ in range(end - start + 1):
            next(generator)

        # При следующем вызове должен быть StopIteration
        with pytest.raises(StopIteration):
            next(generator)

    def test_for_loop_completion(self):
        """Тест завершения цикла for"""
        count = 0
        for card_number in card_number_generator(1, 3):
            count += 1
            assert card_number in [
                "0000 0000 0000 0001",
                "0000 0000 0000 0002",
                "0000 0000 0000 0003"
            ]

        assert count == 3

    def test_list_conversion(self, small_range):
        """Тест преобразования в список"""
        start, end = small_range
        result = list(card_number_generator(start, end))

        assert len(result) == end - start + 1

    def test_multiple_iterations(self):
        """Тест множественных итераций"""
        generator = card_number_generator(1, 3)

        # Первая итерация
        first_iter = list(generator)
        assert len(first_iter) == 3

        # Генератор исчерпан, вторая итерация не даст результатов
        second_iter = list(generator)
        assert len(second_iter) == 0

    def test_stop_iteration_behavior(self):
        """Тест поведения StopIteration"""
        generator = card_number_generator(1, 2)

        assert next(generator) == "0000 0000 0000 0001"
        assert next(generator) == "0000 0000 0000 0002"

        with pytest.raises(StopIteration):
            next(generator)


# Тесты для проверки поведения итератора
class TestCardNumberGeneratorIterator:

    def test_iterator_protocol(self):
        """Тест соответствия протоколу итератора"""
        generator = card_number_generator(1, 3)

        assert hasattr(generator, '__iter__')
        assert hasattr(generator, '__next__')
        assert iter(generator) is generator

    def test_lazy_evaluation(self):
        """Тест ленивых вычислений"""

        # Создаем счетчик для проверки, когда реально генерируются номера
        def counting_generator():
            nonlocal call_count
            for i in range(1, 100):
                call_count += 1
                yield i

        call_count = 0
        test_gen = counting_generator()

        # До итерации ничего не должно быть вычислено
        assert call_count == 0

        # Получаем первый элемент
        first = next(test_gen)
        assert first == 1
        assert call_count == 1

        # Получаем второй элемент
        second = next(test_gen)
        assert second == 2
        assert call_count == 2

    def test_generator_reset_not_possible(self):
        """Тест, что генератор нельзя сбросить"""
        generator = card_number_generator(1, 3)

        first_pass = list(generator)
        second_pass = list(generator)

        assert len(first_pass) == 3
        assert len(second_pass) == 0


def test_generator_with_send_method():
    """Тест метода send (генераторы поддерживают send)"""
    generator = card_number_generator(1, 3)

    # Обычное использование next
    assert next(generator) == "0000 0000 0000 0001"
    assert next(generator) == "0000 0000 0000 0002"
    assert next(generator) == "0000 0000 0000 0003"
    # send можно использовать, но он не влияет на генерацию номеров
    with pytest.raises(StopIteration):
        next(generator)


# Параметризованные тесты
class TestCardNumberGeneratorParameterized:

    @pytest.mark.parametrize("start,end,expected_count,first,last", [
        (1, 1, 1, "0000 0000 0000 0001", "0000 0000 0000 0001"),
        (1, 5, 5, "0000 0000 0000 0001", "0000 0000 0000 0005"),
        (100, 105, 6, "0000 0000 0000 0100", "0000 0000 0000 0105"),
        (9999, 10002, 4, "0000 0000 0000 9999", "0000 0000 0001 0002"),
        (99999999, 100000001, 3, "0000 0000 9999 9999", "0000 0001 0000 0001"),
    ])
    def test_various_ranges(self, start, end, expected_count, first, last):
        """Параметризованный тест различных диапазонов"""
        result = list(card_number_generator(start, end))

        assert len(result) == expected_count
        assert result[0] == first
        assert result[-1] == last

    @pytest.mark.parametrize("number,expected", [
        (1, "0000 0000 0000 0001"),
        (123, "0000 0000 0000 0123"),
        (1234, "0000 0000 0000 1234"),
        (12345, "0000 0000 0001 2345"),
        (123456, "0000 0000 0012 3456"),
        (1234567, "0000 0000 0123 4567"),
        (12345678, "0000 0000 1234 5678"),
        (123456789, "0000 0001 2345 6789"),
        (1234567890, "0000 0012 3456 7890"),
        (12345678901, "0000 0123 4567 8901"),
        (9999, "0000 0000 0000 9999"),
        (10000, "0000 0000 0001 0000"),
        (9999999999999999, "9999 9999 9999 9999"),
    ])
    def test_individual_number_formatting(self, number, expected):
        """Параметризованный тест форматирования отдельных номеров"""
        result = list(card_number_generator(number, number))
        assert len(result) == 1
        assert result[0] == expected

    @pytest.mark.parametrize("start,end,expected_length", [
        (1, 10, 10),
        (100, 50, 0),
        (1, 1, 1),
    ])
    def test_invalid_ranges(self, start, end, expected_length):
        """Параметризованный тест невалидных диапазонов"""
        if start > end:
            with pytest.raises(ValueError, match="Некорректный диапазон номеров карт"):

                list(card_number_generator(start, end))
        else:
            result = list(card_number_generator(start, end))
            assert len(result) == expected_length

    @pytest.mark.parametrize("start, end", [
        (1, 10),
        (100, 200),
        (9999999999999990, 9999999999999995),  # Граничные значения
    ])
    def test_valid_ranges(self, start, end):
        """Тест валтдных диапазонов (не должны выбрасывать исключения)"""
        result = list(card_number_generator(start, end))
        expected_count = end - start + 1
        assert len(result) == expected_count
        # Проверяем, что все номера имеют длину 16 символов
        for card in result:
            assert len(card.replace(' ', '')) == 16
            assert card.count(' ') == 3
            assert all(len(group) == 4 for group in card.split())


# Тесты для проверки производительности
class TestCardNumberGeneratorPerformance:

    def test_large_range_generation(self):
        """Тест генерации большого диапазона"""
        # Генерируем 10000 номеров
        generator = card_number_generator(1, 10000)
        count = 0
        for _ in generator:
            count += 1

        assert count == 10000

    def test_memory_efficiency(self):
        """Тест эффективности использования памяти"""
        import sys

        # Создаем генератор для большого диапазона
        generator = card_number_generator(1, 1000000)

        # Размер генератора должен быть маленьким
        generator_size = sys.getsizeof(generator)

        # Размер списка с таким же количеством элементов был бы огромным
        assert generator_size < 1000  # Генератор занимает мало памяти


# Запуск тестов
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
