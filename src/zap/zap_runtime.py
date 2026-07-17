from __future__ import annotations

import dataclasses
import os
import subprocess
from urllib.parse import urlparse

ALLOWED_HOSTS = {"localhost", "127.0.0.1"}
ALLOWED_PORTS = {3000, 5173, 5174}
CONTEXT_NAME = "EShop"
CONTEXT_REGEX = r"^http://(?:localhost|127\.0\.0\.1):(?:3000|5173|5174)(?:[/?#].*)?$"
REPLACER_RULE = "EShop JWT Authorization"
ZAP_IMAGE = "ghcr.io/zaproxy/zaproxy:stable"


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


class ZapDockerManager:
    def __init__(self, port: int = 8090, container_name: str | None = None) -> None:
        self.port = port
        self.container_name = container_name or f"eshop-zap-{os.getpid()}"
        self.started = False

    def start(self) -> None:
        try:
            subprocess.run(["docker", "version"], check=True, capture_output=True, text=True)
            command = [
                "docker", "run", "--rm", "-d", "--name", self.container_name,
                "--network", "host", ZAP_IMAGE, "zap.sh", "-daemon",
                "-port", str(self.port), "-host", "0.0.0.0",
                "-config", "api.disablekey=true",
            ]
            subprocess.run(command, check=True, capture_output=True, text=True)
        except (FileNotFoundError, subprocess.CalledProcessError) as exc:
            raise RuntimeError("Docker must be installed and running to start ZAP") from exc
        self.started = True

    def stop(self) -> None:
        if not self.started:
            return
        subprocess.run(
            ["docker", "stop", self.container_name],
            check=False,
            capture_output=True,
            text=True,
        )
        self.started = False
