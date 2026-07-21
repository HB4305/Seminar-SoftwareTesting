"""Các helper runtime dùng chung cho workflow OWASP ZAP của EShop.

File này gom các phần không thuộc CLI: validate target local, đọc `.env`,
cấu hình context/auth trong ZAP, đăng nhập lấy JWT, xác minh session, và quản
lý container ZAP khi script tự khởi động Docker.
"""

from __future__ import annotations

import dataclasses
import json
import os
import re
import urllib.error
import urllib.request
from urllib.parse import urlparse

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def load_dotenv(env_path: str | os.PathLike[str] | None = None) -> None:
    """Đọc file `.env` đơn giản mà không ghi đè biến môi trường đã có."""
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


# Nạp biến môi trường từ file .env trước khi định nghĩa các hằng số
load_dotenv()

# Các cấu hình cho phép ghi đè từ file .env
ALLOWED_HOSTS = set(os.getenv("ZAP_ALLOWED_HOSTS", "localhost,127.0.0.1").split(","))

allowed_ports_env = os.getenv("ZAP_ALLOWED_PORTS", "3000,5173,5174")
try:
    ALLOWED_PORTS = {int(p.strip()) for p in allowed_ports_env.split(",") if p.strip()}
except ValueError:
    ALLOWED_PORTS = {3000, 5173, 5174}

CONTEXT_NAME = os.getenv("ZAP_CONTEXT_NAME", "EShop")

# Tạo regex cho context dựa trên các host và port được cấu hình
allowed_hosts_regex = "|".join(re.escape(h) for h in ALLOWED_HOSTS)
allowed_ports_regex = "|".join(str(p) for p in ALLOWED_PORTS)
DEFAULT_CONTEXT_REGEX = rf"^http://(?:{allowed_hosts_regex}):(?:{allowed_ports_regex})(?:[/?#].*)?$"
CONTEXT_REGEX = os.getenv("ZAP_CONTEXT_REGEX", DEFAULT_CONTEXT_REGEX)

LOGIN_URL = os.getenv("ESHOP_LOGIN_URL", "http://localhost:3000/api/login")
REPLACER_RULE = os.getenv("ZAP_REPLACER_RULE", "EShop JWT Authorization")
VERIFY_URL = os.getenv("ESHOP_VERIFY_URL", "http://localhost:3000/api/users/me")
ZAP_IMAGE = os.getenv("ZAP_IMAGE", "ghcr.io/zaproxy/zaproxy:stable")


@dataclasses.dataclass(frozen=True)
class Credential:
    """Thông tin đăng nhập seed user/admin dùng cho authenticated scan."""

    email: str
    password: str


@dataclasses.dataclass(frozen=True)
class AuthState:
    """ID context và user sau khi cấu hình authentication trong ZAP."""

    context_id: str
    user_id: str


def validate_target(target: str) -> str:
    """Chỉ cho phép scan EShop local trên các port đã định nghĩa trước."""
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
    """Lấy credential theo role, ưu tiên biến môi trường nếu có cấu hình."""
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
    """Tạo hoặc reset ZAP context để scope chỉ bao gồm URL local EShop."""
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
    """Tìm hoặc tạo ZAP user tương ứng với email trong context hiện tại."""
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
    """Cấu hình ZAP để tự gắn JWT Authorization header khi scan có đăng nhập."""
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
    """Xóa rule chứa JWT và tắt Forced User Mode sau authenticated scan."""
    try:
        zap.replacer.remove_rule(REPLACER_RULE)
    finally:
        if forced_user:
            zap.forcedUser.set_forced_user_mode_enabled("false")


def _proxy_opener(zap_url: str):
    """Tạo urllib opener gửi request qua ZAP proxy để request được ghi vào ZAP."""
    return urllib.request.build_opener(
        urllib.request.ProxyHandler({"http": zap_url, "https": zap_url})
    )


def login_for_token(zap_url: str, credential: Credential, timeout: int = 15) -> str:
    """Đăng nhập EShop qua ZAP proxy và trích xuất JWT từ response."""
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
    """Gửi request `/api/users/me` qua ZAP proxy để xác nhận JWT hoạt động."""
    request = urllib.request.Request(VERIFY_URL, method="GET")
    try:
        with _proxy_opener(zap_url).open(request, timeout=timeout) as response:
            if response.status != 200:
                raise RuntimeError(
                    f"Authentication verification returned HTTP {response.status}"
                )
    except (OSError, urllib.error.URLError) as exc:
        raise RuntimeError(f"Authentication verification failed: {exc}") from exc

