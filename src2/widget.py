from src2.masks import get_mask_card_number, get_mask_account


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
    if len(date_str) < 10:
        raise ValueError("Некорректный формат даты")

    return f"{date_str[8:10]}.{date_str[5:7]}.{date_str[:4]}"


print(get_date("2024-03-11T02:26:18.671407"))
