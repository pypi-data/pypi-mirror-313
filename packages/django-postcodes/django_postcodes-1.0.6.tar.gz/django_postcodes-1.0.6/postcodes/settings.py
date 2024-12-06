from django.conf import settings

def default_parameter_formatter(**kwargs):
    return "&".join([f"{key}={value}" for key, value in kwargs.items()])

ADDRESS_CHECK_API_KEY = getattr(settings, "ADDR_VALIDATOR_API_KEY", None)
ADDRESS_CHECK_API_URL = getattr(settings, "ADDR_VALIDATOR_API_URL", "https://postcode.go-dev.nl/api")
URL_PARAMETER_FORMAT = getattr(settings, "ADDR_VALIDATOR_PARAMETER_FORMAT", default_parameter_formatter)
ERROR_ATTRIBUTE = getattr(settings, "ADDR_VALIDATOR_ERROR_ATTRIBUTE", "error")
ADDRESS_CACHE_TIMEOUT = getattr(settings, "ADDR_VALIDATOR_CACHE_TIMEOUT", 60 * 60 * 24 * 7) # 1 week
API_KEY_ATTRIBUTE = getattr(settings, "ADDR_VALIDATOR_API_KEY_ATTRIBUTE", "X-API-Token")
REQUIRES_AUTH = getattr(settings, "ADDR_VALIDATOR_REQUIRES_AUTH", False)
