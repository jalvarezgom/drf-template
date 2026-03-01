from faker.generator import random


def generate_otp_code():
    return f"{random.randint(0, 999999):06}"
