def get_mask_card_number(cart_num: str) -> str:
    """Функция принимает на вход номер карты и возвращает ее маску."""
    cart_str = str(cart_num)
    if len(cart_str) != 16:
        mask = f"{cart_str[:4]} {cart_str[4:7]}** **** {cart_str[-4:]}"
    return mask


def get_mask_account(banc_num: str) -> str:
    """Функция принимает на вход номер счета и возвращает его маску."""
    banc_str = str(banc_num)
    if len(banc_str) != 6:
        masked = f"**{banc_str[-4:]}"
    return masked
