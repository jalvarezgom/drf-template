from rest_framework.throttling import AnonRateThrottle


class LoginRateThrottle(AnonRateThrottle):
    scope = "login"


class RegisterRateThrottle(AnonRateThrottle):
    scope = "register"


class RecoverPasswordRateThrottle(AnonRateThrottle):
    scope = "recover_password"


class OTPRateThrottle(AnonRateThrottle):
    scope = "otp"
