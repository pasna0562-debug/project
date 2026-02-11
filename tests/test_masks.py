import pytest

from src.masks import get_mask_account, get_mask_card_number


def test_get_mask_card_number() -> None:
    """Тест маскировки номера карты"""
    # Проверка работы со стракой
    assert get_mask_card_number("7000792289606361") == "7000 79** **** 6361"

    # проверка формата (длина и начало.конец)
    result = get_mask_card_number("1234567890123456")
    assert result == "1234 56** **** 3456"
    assert len(result) == 19

    # Туст с некоректным номером
    with pytest.raises(ValueError):
        get_mask_card_number("12345")


def test_get_mask_account() -> None:
    """Тест маскировки номера счета"""
    # Проверка работы со строкой
    assert get_mask_account("73654108430135874305") == "**4305"

    # Дополнительная проверка формата
    result = get_mask_account("1234567890")
    assert result == "**7890"
    assert result.startswith("**")
    assert len(result) == 6

    # Тест с коротким номером
    with pytest.raises(ValueError):
        get_mask_account("123")
