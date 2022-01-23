from iso3166 import countries_by_name
from yfa.exceptions import InvalidCountry, InvalidPassword


def validate_country(country: str):
    country = country.upper()
    if country not in countries_by_name:
        raise InvalidCountry()

    return country


def validate_password(pwd: str, throw=False):
    """
    - 8 <= len(pwd) <= 40
    - numbers
    - alpha numerics
    - 1 symbol
    """
    import re

    length_error = not (8 <= len(pwd) <= 40)
    digit_error = re.search(r"\d", pwd) is None
    uppercase_error = re.search(r"[A-Z]", pwd) is None
    lowercase_error = re.search(r"[a-z]", pwd) is None
    symbol_error = re.search(
        r"[ !#$%&'()*+,-./[\\\]^_`{|}~"+r'"]', pwd) is None

    pwd_ok = not (
        length_error or digit_error or uppercase_error or lowercase_error or symbol_error)

    result = {
        'pwd_ok': pwd_ok,
        'length_error': length_error,
        'digit_error': digit_error,
        'uppercase_error': uppercase_error,
        'lowercase_error': lowercase_error,
        'symbol_error': symbol_error,
    }

    if not pwd_ok and throw:
        raise InvalidPassword(result)

    return result


def hash_password(pwd: str):
    import bcrypt
    if not isinstance(pwd, bytes):
        pwd = pwd.encode("utf-8")
    return bcrypt.hashpw(
        pwd, bcrypt.gensalt()
    ).decode("utf-8")


def verify_password(pwd: str, hash: str):
    import bcrypt
    return bcrypt.checkpw(
        pwd.encode("utf-8"), hash.encode("utf-8")
    )


def generate_random(length: int):
    import random
    import string
    return "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))
