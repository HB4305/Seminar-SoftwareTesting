from __future__ import annotations

import dataclasses
import os
from urllib.parse import urlparse

ALLOWED_HOSTS = {"localhost", "127.0.0.1"}
ALLOWED_PORTS = {3000, 5173, 5174}
CONTEXT_NAME = "EShop"
CONTEXT_REGEX = r"^http://(?:localhost|127\.0\.0\.1):(?:3000|5173|5174)(?:[/?#].*)?$"
REPLACER_RULE = "EShop JWT Authorization"


@dataclasses.dataclass(frozen=True)
class Credential:
    email: str
    password: str


def validate_target(target: str) -> str:
    parsed = urlparse(target)
    try:
        port = parsed.port
    except ValueError:
        port = None
    if (
        parsed.scheme != "http"
        or parsed.hostname not in ALLOWED_HOSTS
        or port not in ALLOWED_PORTS
    ):
        raise ValueError("Target must be a local EShop URL on port 3000, 5173, or 5174")
    return target


def get_credential(role: str) -> Credential | None:
    if role == "none":
        return None
    defaults = {
        "user": ("test@eshop.com", "Test1234!"),
        "admin": ("admin@eshop.com", "Admin123!"),
    }
    if role not in defaults:
        raise ValueError(f"Unsupported auth role: {role}")
    email, password = defaults[role]
    prefix = f"ZAP_{role.upper()}"
    return Credential(
        os.getenv(f"{prefix}_EMAIL", email),
        os.getenv(f"{prefix}_PASSWORD", password),
    )
