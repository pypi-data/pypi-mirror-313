from decimal import Decimal


def get_decimal_places(number) -> int:
    decimal_number = Decimal(str(number))
    return -int(decimal_number.as_tuple().exponent)
