

from src2 import get_mask_account, get_mask_card_number


def mask_account_card(info: str) -> str:
    """Маскирует номер карты или счета в зависимости
    от типа входных данных.
    """

    parts = info.split()
    number = parts[-1]
    name = " ".join(parts[:-1])

    if name.lower() == "счет":
        masked_number = get_mask_account(number)
    else:
        masked_number = get_mask_card_number(number)
    return f"{name} {masked_number}"


if __name__ == "__main__":
    print(mask_account_card("Visa Platinum 7000792289606361"))
    print(mask_account_card("Maestro 7000792289606361"))
    print(mask_account_card("счет 73654108430135874305"))


def get_date(date_str: str) -> str:
    """Принимает строку с датой в формате "2024-03-11Т02:26:18.671407"
    и возвращает строку в формате "11.03.2024".
    """
    year = date_str[0:4]
    month = date_str[5:7]
    day = date_str[8:10]

    return f"{day}.{month}.{year}"


print(get_date("2024-03-11T02:26:18.671407"))
