import secrets


def generate_otp_code():
    return f"{secrets.randbelow(1_000_000):06}"
