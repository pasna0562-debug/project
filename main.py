from src2 import get_mask_account, get_mask_card_number


def main() -> None:
    """Пример использования функции маскировки"""

    # Пример с картой
    card_number = 7000792289606361
    print(get_mask_card_number(card_number))

    # Пример со счетом
    account = 73654108430135874305
    print(get_mask_account(account))


if __name__ == "__main__":
    main()

