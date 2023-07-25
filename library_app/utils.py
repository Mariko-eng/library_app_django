import random
from uuid import UUID, uuid4 as real_uuid4

default_generator = real_uuid4


def uuid4() -> UUID:
    return default_generator()


def generate_otp():
    otp = random.randint(100000, 999999)
    return otp
