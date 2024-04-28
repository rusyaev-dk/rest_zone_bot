import random
import string


def generate_random_id(length: int) -> str:
    """
    Generates random combination of symbols for questionnaire_id in database
    """

    symbols = string.ascii_lowercase + string.ascii_uppercase + string.digits
    return ''.join(random.choice(symbols) for _ in range(length))


def generate_int_id() -> int:
    return random.randint(100, 1000)
