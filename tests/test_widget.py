import pytest

from unittest.mock import patch, MagicMock
from src2.widget import mask_account_card, get_date


def test_get_date_valid() -> None:
    """Тест коректного приоброзования даты"""
    result = get_date("2024-03-11T02:26:18.671407")
    assert result == "11.03.2024"


def test_get_date_short_string() -> None:
    """Проверка, что функция работает по индексам
    (если передать строку короче нужного, будет ошибка)"""
    with pytest.raises(ValueError, match="Некорректный формат даты"):
        get_date("2024")


# Тест для функции mask_account_card

@patch("src2.widget.get_mask_card_number")
def test_mask_account_card_visa(mosk_get_mask_card: MagicMock) -> None:
    """Тест маскировки карты (Visa Platinum)"""
    mosk_get_mask_card.return_value = "7000 79** **** 6361"
    result = mask_account_card("Visa Platinum 7000792289606361")
    assert result == "Visa Platinum 7000 79** **** 6361"

    mosk_get_mask_card.assert_called_once_with("7000792289606361")


@patch("src2.widget.get_mask_card_number")
def test_mask_account_card_maestro(mosk_get_mask_card: MagicMock) -> None:
    """Тест маскировки карты с одним словом в названии (Maestro)"""
    mosk_get_mask_card.return_value = "7000 79** **** 6361"
    result = mask_account_card("Maestro 7000792289606361")
    assert result == "Maestro 7000 79** **** 6361"


@patch("src2.widget.get_mask_account")
def test_mask_account_card_account(mosk_get_mask_account: MagicMock) -> None:
    """Тест маркировки счета"""
    mosk_get_mask_account.return_value = "4305"
    result = mask_account_card("счет 73654108430135874305")
    assert result == "счет 4305"

    mosk_get_mask_account.assert_called_once_with("73654108430135874305")


def test_mask_account_card_logis_separation() -> None:
    """Тест правильности разделения строки на имя и номер"""
    with patch("src2.widget.get_mask_card_number") as mosk_card:
        mosk_card.return_value = "7000 79** **** 6361"

        result = mask_account_card("Visa Platinum 7000792289606361")
        assert result == "Visa Platinum 7000 79** **** 6361"
        mosk_card.assert_called_once_with("7000792289606361")
