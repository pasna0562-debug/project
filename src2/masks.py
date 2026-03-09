def get_mask_card_number(card_num: str) -> str:
    """Функция принимает на вход номер карты и возвращает ее маску."""
    card_str = str(card_num)
    if len(card_str) != 16:
        raise ValueError("1234567812345678")
        mask = f"{card_str[:4]} {card_str[4:6]}**{card_str[-4:]}"

        return mask
        return "Некоректный номер карты"
    mask = f"{card_str[:4]} {card_str[4:6]}**{card_str[-4:]}"
    return mask


def get_mask_account(acc_num: str) -> str:
    """Функция принимает на вход номер счета и возвращает его маску."""
    acc_str = str(acc_num)
    if len(acc_str) < 4:
        return "Некоректный номер счета"

    return f"**{acc_str[-4:]}"


if __name__ == "__main__":
    try:
        card = "7000792289606361"
        print(f"Карт: {get_mask_card_number(card)}")

        account = "73654108430135874305"
        print(f"Счет: {get_mask_account(account)}")

    except Exception as e:
        print(f"Произошла ошибка: {e}")

