import random
import string

min_value_randon_number = 1111111111
max_value_randon_number = 9999999999


def check_required_keys(keys: tuple, element: dict):
    return all(element.get(key) for key in keys)


def get_random_number(min_value_randon_number, max_value_randon_number) -> int:
    return random.randint(min_value_randon_number, max_value_randon_number)


def get_random_price() -> str:
    return get_random_number(1, 10)


def get_random_string() -> str:
    letters = list(string.ascii_lowercase)
    random.shuffle(letters)
    return ''.join(letters[:10])
