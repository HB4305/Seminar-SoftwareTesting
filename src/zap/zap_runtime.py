from __future__ import annotations

import dataclasses
import json
import os
import subprocess
import urllib.error
import urllib.request
from urllib.parse import urlparse

ALLOWED_HOSTS = {"localhost", "127.0.0.1"}
ALLOWED_PORTS = {3000, 5173, 5174}
CONTEXT_NAME = "EShop"
CONTEXT_REGEX = r"^http://(?:localhost|127\.0\.0\.1):(?:3000|5173|5174)(?:[/?#].*)?$"
LOGIN_URL = "http://localhost:3000/api/login"
REPLACER_RULE = "EShop JWT Authorization"
VERIFY_URL = "http://localhost:3000/api/users/me"
ZAP_IMAGE = "ghcr.io/zaproxy/zaproxy:stable"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def _format_command(command: object) -> str:
    if isinstance(command, (list, tuple)):
        return " ".join(str(part) for part in command)
    return str(command)


def load_dotenv(env_path: str | os.PathLike[str] | None = None) -> None:
    candidate = os.fspath(env_path) if env_path is not None else os.path.join(SCRIPT_DIR, ".env")
    if not os.path.exists(candidate):
        return
    with open(candidate, encoding="utf-8") as env_file:
        for raw_line in env_file:
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            os.environ.setdefault(key, value)


def _docker_start_error(command: object, exc: Exception) -> str:
    parts = [
        "Docker must be installed/running to start ZAP",
        f"command failed: {_format_command(command)}",
    ]
    stderr = getattr(exc, "stderr", None)
    stdout = getattr(exc, "stdout", None)
    if stderr:
        parts.append(f"stderr: {stderr}")
    if stdout:
        parts.append(f"stdout: {stdout}")
    if not stderr and not stdout and str(exc):
        parts.append(str(exc))
    return "; ".join(parts)


@dataclasses.dataclass(frozen=True)
class Credential:
    email: str
    password: str


@dataclasses.dataclass(frozen=True)
class AuthState:
    context_id: str
    user_id: str


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


def ensure_context(zap) -> str:
    if CONTEXT_NAME not in zap.context.context_list:
        context_id = str(zap.context.new_context(CONTEXT_NAME))
        zap.context.include_in_context(CONTEXT_NAME, CONTEXT_REGEX)
    else:
        context_id = str(zap.context.context(CONTEXT_NAME)["id"])
        if list(zap.context.include_regexs(CONTEXT_NAME)) != [CONTEXT_REGEX]:
            zap.context.set_context_regexs(
                CONTEXT_NAME,
                json.dumps([CONTEXT_REGEX]),
                "[]",
            )
    zap.context.set_context_in_scope(CONTEXT_NAME, "true")
    return context_id


def _user_id(zap, context_id: str, email: str) -> str:
    for user in zap.users.users_list(context_id):
        if user.get("name") == email:
            user_id = str(user["id"])
            break
    else:
        user_id = str(zap.users.new_user(context_id, email))
    zap.users.set_user_enabled(context_id, user_id, "true")
    return user_id


def configure_authenticated_context(
    zap,
    credential: Credential,
    token: str,
    forced_user: bool,
) -> AuthState:
    context_id = ensure_context(zap)
    user_id = _user_id(zap, context_id, credential.email)
    try:
        zap.replacer.remove_rule(REPLACER_RULE)
    except Exception:
        pass
    try:
        zap.replacer.add_rule(
            REPLACER_RULE,
            "true",
            "REQ_HEADER",
            "false",
            "Authorization",
            f"Bearer {token}",
            url=CONTEXT_REGEX,
        )
    except Exception as exc:
        raise RuntimeError("ZAP Replacer API is unavailable; cannot inject JWT") from exc
    if forced_user:
        try:
            zap.forcedUser.set_forced_user(context_id, user_id)
            zap.forcedUser.set_forced_user_mode_enabled("true")
        except Exception as exc:
            try:
                zap.replacer.remove_rule(REPLACER_RULE)
            except Exception:
                pass
            raise RuntimeError("ZAP forced user setup failed") from exc
    return AuthState(context_id, user_id)


def cleanup_authenticated_context(zap, forced_user: bool) -> None:
    try:
        zap.replacer.remove_rule(REPLACER_RULE)
    finally:
        if forced_user:
            zap.forcedUser.set_forced_user_mode_enabled("false")


def _proxy_opener(zap_url: str):
    return urllib.request.build_opener(
        urllib.request.ProxyHandler({"http": zap_url, "https": zap_url})
    )


def login_for_token(zap_url: str, credential: Credential, timeout: int = 15) -> str:
    request = urllib.request.Request(
        LOGIN_URL,
        data=json.dumps(dataclasses.asdict(credential)).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with _proxy_opener(zap_url).open(request, timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (
        OSError,
        urllib.error.URLError,
        json.JSONDecodeError,
    ) as exc:
        raise RuntimeError(f"EShop login failed: {exc}") from exc
    if not isinstance(payload, dict):
        raise RuntimeError("EShop login response did not contain a token")
    token = payload.get("token")
    if not isinstance(token, str) or not token:
        raise RuntimeError("EShop login response did not contain a token")
    return token


def verify_authenticated_session(zap_url: str, timeout: int = 15) -> None:
    request = urllib.request.Request(VERIFY_URL, method="GET")
    try:
        with _proxy_opener(zap_url).open(request, timeout=timeout) as response:
            if response.status != 200:
                raise RuntimeError(
                    f"Authentication verification returned HTTP {response.status}"
                )
    except (OSError, urllib.error.URLError) as exc:
        raise RuntimeError(f"Authentication verification failed: {exc}") from exc


class ZapDockerManager:
    def __init__(
        self,
        port: int = 8090,
        container_name: str | None = None,
        image: str | None = None,
    ) -> None:
        self.port = port
        self.container_name = container_name or f"eshop-zap-{os.getpid()}"
        self.image = image or os.getenv("ZAP_IMAGE", ZAP_IMAGE)
        self.started = False

    def start(self) -> None:
        command = ["docker", "version"]
        try:
            subprocess.run(command, check=True, capture_output=True, text=True)
            command = [
                "docker", "run", "--rm", "-d", "--name", self.container_name,
                "--network", "host", self.image, "zap.sh", "-daemon",
                "-port", str(self.port), "-host", "0.0.0.0",
                "-config", "api.disablekey=true",
            ]
            subprocess.run(command, check=True, capture_output=True, text=True)
        except (FileNotFoundError, subprocess.CalledProcessError) as exc:
            failed_command = getattr(exc, "cmd", None) or command
            raise RuntimeError(_docker_start_error(failed_command, exc)) from exc
        self.started = True

    def stop(self) -> None:
        if not self.started:
            return
        try:
            result = subprocess.run(
                ["docker", "stop", self.container_name],
                check=False,
                capture_output=True,
                text=True,
            )
            returncode = getattr(result, "returncode", 0)
            if (
                isinstance(returncode, int)
                and not isinstance(returncode, bool)
                and returncode != 0
            ):
                parts = [
                    f"docker stop failed for ZAP container {self.container_name}",
                    f"exit code: {returncode}",
                ]
                stderr = getattr(result, "stderr", None)
                stdout = getattr(result, "stdout", None)
                if stderr:
                    parts.append(f"stderr: {stderr}")
                if stdout:
                    parts.append(f"stdout: {stdout}")
                raise RuntimeError("; ".join(parts))
        finally:
            self.started = False
