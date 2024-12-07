from os import getenv
from typing import Literal

HEALTH_CHECK_TIMEOUT = int(getenv("EDRI_HEALTH_CHECK_TIMEOUT", 10))
TOKEN_LENGTH = int(getenv("EDRI_TOKEN_LENGTH", 64))
API_RESPONSE_TIMEOUT = int(getenv("EDRI_API_RESPONSE_TIMEOUT", 60))
ENVIRONMENT: Literal["development", "production"] = "production" if getenv("ENVIRONMENT") == "production" else "development"

SWITCH_KEY_LENGTH = int(getenv("EDRI_SWITCH_KEY_LENGTH ", 8))
SWITCH_HOST = getenv("EDRI_SWITCH_HOST", "localhost")
SWITCH_PORT = int(getenv("EDRI_SWITCH_PORT", 8899))

UPLOAD_FILES_PREFIX = getenv("EDRI_UPLOAD_FILES_PREFIX", "edri_")
UPLOAD_FILES_KEEP_DAYS = int(getenv("EDRI_UPLOAD_FILES_KEEP_DAYS", 0))
UPLOAD_FILES_PATH = getenv("EDRI_UPLOAD_FILES_PATH", "/tmp/edri")

CACHE_TIMEOUT = int(getenv("EDRI_CACHE_TIMEOUT", 30))
CACHE_INFO_MESSAGE = int(getenv("EDRI_CACHE_INFO_MESSAGE", 60))

HOST = getenv("EDRI_HOST", "localhost")
PORT = int(getenv("EDRI_PORT", 8080))
API_WORKERS = int(getenv("EDRI_API_WORKERS", 8))
SSL_KEY = getenv("EDRI_SSL_KEY")
SSL_CERTIFICATE = getenv("EDRI_SSL_CERTIFICATE")

TEMPLATE_PATH = getenv("EDRI_TEMPLATE_PATH", "templates")
ASSETS_PATH = getenv("EDRI_ASSETS_PATH", "assets")
MAX_BODY_SIZE = int(getenv("EDRI_MAX_BODY_SIZE", 4096 * 1024))
