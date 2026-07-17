# ZAP Automated Authenticated Scan Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a one-command OWASP ZAP scan that manages its Docker daemon, authenticates to EShop as user or admin with JWT, scans only the local EShop scope, writes standardized reports, and documents the workflow.

**Architecture:** Keep CLI orchestration in `scan_zap.py` and place reusable, mockable Docker/auth/context behavior in a new `zap_runtime.py`. JWT login traffic passes through ZAP; a temporary Replacer rule injects the bearer token during crawling and scanning, while cleanup removes secrets and stops only the container created by this run.

**Tech Stack:** Python 3 standard library, `python-owasp-zap-v2.4`, OWASP ZAP Docker image, `unittest`/`unittest.mock`, Markdown.

---

## File map

- Create `src/zap/zap_runtime.py`: target validation, credentials, proxied JSON requests, Docker lifecycle, ZAP context/user/JWT setup and cleanup.
- Create `src/zap/test_zap_runtime.py`: isolated unit tests for the runtime module.
- Modify `src/zap/scan_zap.py`: CLI parsing and scan orchestration using the runtime module.
- Create `src/zap/test_scan_zap.py`: orchestration and parser tests using mocks.
- Modify `src/zap/ai_triage_zap.py`: standardized model/path/documentation references.
- Modify `src/zap/test_ai_triage_zap.py`: corrected expectations and output naming coverage.
- Create `src/zap/README.md`: user-facing explanation and commands.

### Task 1: Stabilize and standardize AI triage

**Files:**
- Modify: `src/zap/test_ai_triage_zap.py`
- Modify: `src/zap/ai_triage_zap.py`

- [ ] **Step 1: Change the existing tests to express the approved behavior**

Replace the model and output-path tests with:

```python
def test_default_model_uses_openrouter_model_identifier(self):
    self.assertEqual(DEFAULT_MODEL, "google/gemini-2.5-flash")

def test_resolve_output_path_uses_standard_output_name(self):
    report_path = Path("src/zap/output/backend_report.html")
    output_path = resolve_output_path(report_path, None)

    self.assertEqual(
        output_path,
        (Path.cwd() / "src/zap/output/zap_ai_triage_report.md").resolve(),
    )

def test_resolve_output_path_resolves_explicit_relative_path(self):
    output_path = resolve_output_path(
        Path("src/zap/output/backend_report.html"),
        Path("tmp/custom.md"),
    )

    self.assertEqual(output_path, (Path.cwd() / "tmp/custom.md").resolve())
```

- [ ] **Step 2: Run the tests and confirm the standardized output test fails**

Run: `rtk python -m unittest src/zap/test_ai_triage_zap.py`

Expected: one failure because `resolve_output_path()` still derives `backend_report_ai_triage.md`.

- [ ] **Step 3: Implement the standardized triage output**

In `ai_triage_zap.py`, define:

```python
DEFAULT_OUTPUT = DEFAULT_INPUT_DIR / "zap_ai_triage_report.md"
```

Change `resolve_output_path()` to:

```python
def resolve_output_path(report_path: Path, output_path: Path | None) -> Path:
    del report_path
    selected = output_path or DEFAULT_OUTPUT
    return selected if selected.is_absolute() else (Path.cwd() / selected).resolve()
```

Update CLI help, module examples, submission text and evidence paths from `docs/zap` to `src/zap`. In `main()`, pass `None` only when the parser value equals `DEFAULT_OUTPUT`, retaining explicit `--output` behavior.

- [ ] **Step 4: Run AI triage tests**

Run: `rtk python -m unittest src/zap/test_ai_triage_zap.py`

Expected: all tests pass.

- [ ] **Step 5: Commit AI triage stabilization**

```bash
rtk git add src/zap/ai_triage_zap.py src/zap/test_ai_triage_zap.py
rtk git commit -m "fix(zap): standardize AI triage output"
```

### Task 2: Add target validation and role credentials

**Files:**
- Create: `src/zap/zap_runtime.py`
- Create: `src/zap/test_zap_runtime.py`

- [ ] **Step 1: Write failing tests for target scope and role selection**

Create tests covering the exact public API:

```python
import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))

from zap_runtime import Credential, get_credential, validate_target


class ZapRuntimeTests(unittest.TestCase):
    def test_validate_target_accepts_eshop_local_ports(self):
        for url in (
            "http://localhost:3000",
            "http://localhost:5173/",
            "http://127.0.0.1:5174/admin",
        ):
            with self.subTest(url=url):
                self.assertEqual(validate_target(url), url)

    def test_validate_target_rejects_external_or_unknown_port(self):
        for url in ("https://example.com", "http://localhost:8080"):
            with self.subTest(url=url):
                with self.assertRaisesRegex(ValueError, "local EShop"):
                    validate_target(url)

    def test_get_credential_uses_seed_user(self):
        self.assertEqual(
            get_credential("user"),
            Credential("test@eshop.com", "Test1234!"),
        )

    @patch.dict(
        os.environ,
        {"ZAP_ADMIN_EMAIL": "scan-admin@example.test", "ZAP_ADMIN_PASSWORD": "secret"},
        clear=False,
    )
    def test_get_credential_allows_environment_override(self):
        self.assertEqual(
            get_credential("admin"),
            Credential("scan-admin@example.test", "secret"),
        )

    def test_get_credential_returns_none_for_anonymous(self):
        self.assertIsNone(get_credential("none"))
```

- [ ] **Step 2: Run the new tests and verify import failure**

Run: `rtk python -m unittest src/zap/test_zap_runtime.py`

Expected: ERROR because `zap_runtime` does not exist.

- [ ] **Step 3: Implement target and credential helpers**

Create `zap_runtime.py` with constants and functions:

```python
from __future__ import annotations

import dataclasses
import os
from urllib.parse import urlparse

ALLOWED_HOSTS = {"localhost", "127.0.0.1"}
ALLOWED_PORTS = {3000, 5173, 5174}
CONTEXT_NAME = "EShop"
CONTEXT_REGEX = r"http://(?:localhost|127\.0\.0\.1):(?:3000|5173|5174)(?:/.*)?"
REPLACER_RULE = "EShop JWT Authorization"


@dataclasses.dataclass(frozen=True)
class Credential:
    email: str
    password: str


def validate_target(target: str) -> str:
    parsed = urlparse(target)
    if parsed.scheme != "http" or parsed.hostname not in ALLOWED_HOSTS or parsed.port not in ALLOWED_PORTS:
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
```

- [ ] **Step 4: Run target and credential tests**

Run: `rtk python -m unittest src/zap/test_zap_runtime.py`

Expected: all current runtime tests pass.

- [ ] **Step 5: Commit target and credential helpers**

```bash
rtk git add src/zap/zap_runtime.py src/zap/test_zap_runtime.py
rtk git commit -m "feat(zap): add EShop target and role configuration"
```

### Task 3: Add managed Docker lifecycle

**Files:**
- Modify: `src/zap/zap_runtime.py`
- Modify: `src/zap/test_zap_runtime.py`

- [ ] **Step 1: Write failing Docker lifecycle tests**

Add:

```python
from unittest.mock import call, patch

from zap_runtime import ZapDockerManager


@patch("zap_runtime.subprocess.run")
def test_docker_manager_starts_expected_container(self, run):
    run.return_value.returncode = 0
    manager = ZapDockerManager(port=8090, container_name="test-zap")

    manager.start()

    run.assert_any_call(["docker", "version"], check=True, capture_output=True, text=True)
    run.assert_any_call(
        [
            "docker", "run", "--rm", "-d", "--name", "test-zap",
            "--network", "host", "ghcr.io/zaproxy/zaproxy:stable",
            "zap.sh", "-daemon", "-port", "8090", "-host", "0.0.0.0",
            "-config", "api.disablekey=true",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    self.assertTrue(manager.started)

@patch("zap_runtime.subprocess.run")
def test_docker_manager_stops_only_after_start(self, run):
    manager = ZapDockerManager(container_name="test-zap")
    manager.stop()
    run.assert_not_called()

    manager.started = True
    manager.stop()
    run.assert_called_once_with(
        ["docker", "stop", "test-zap"],
        check=False,
        capture_output=True,
        text=True,
    )
```

- [ ] **Step 2: Run the tests and confirm the class is missing**

Run: `rtk python -m unittest src/zap/test_zap_runtime.py`

Expected: ERROR importing `ZapDockerManager`.

- [ ] **Step 3: Implement Docker lifecycle**

Add imports and class:

```python
import subprocess

ZAP_IMAGE = "ghcr.io/zaproxy/zaproxy:stable"


class ZapDockerManager:
    def __init__(self, port: int = 8090, container_name: str | None = None) -> None:
        self.port = port
        self.container_name = container_name or f"eshop-zap-{os.getpid()}"
        self.started = False

    def start(self) -> None:
        subprocess.run(["docker", "version"], check=True, capture_output=True, text=True)
        command = [
            "docker", "run", "--rm", "-d", "--name", self.container_name,
            "--network", "host", ZAP_IMAGE, "zap.sh", "-daemon",
            "-port", str(self.port), "-host", "0.0.0.0",
            "-config", "api.disablekey=true",
        ]
        subprocess.run(command, check=True, capture_output=True, text=True)
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
```

Catch `FileNotFoundError` and `subprocess.CalledProcessError` in `start()` and raise `RuntimeError` with a message that says Docker must be installed/running.

- [ ] **Step 4: Run runtime tests**

Run: `rtk python -m unittest src/zap/test_zap_runtime.py`

Expected: all tests pass.

- [ ] **Step 5: Commit Docker management**

```bash
rtk git add src/zap/zap_runtime.py src/zap/test_zap_runtime.py
rtk git commit -m "feat(zap): manage ZAP Docker lifecycle"
```

### Task 4: Add JWT login and verification through ZAP

**Files:**
- Modify: `src/zap/zap_runtime.py`
- Modify: `src/zap/test_zap_runtime.py`

- [ ] **Step 1: Write failing tests for token extraction and verification**

Add a fake response context manager and tests:

```python
import json
from unittest.mock import MagicMock, patch

from zap_runtime import login_for_token, verify_authenticated_session


class FakeResponse:
    def __init__(self, payload, status=200):
        self.payload = json.dumps(payload).encode("utf-8")
        self.status = status

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self):
        return self.payload


@patch("zap_runtime.urllib.request.build_opener")
def test_login_for_token_extracts_jwt_without_logging_it(self, build_opener):
    build_opener.return_value.open.return_value = FakeResponse({"token": "jwt-value"})
    token = login_for_token("http://localhost:8090", Credential("a@b.test", "secret"))
    self.assertEqual(token, "jwt-value")

@patch("zap_runtime.urllib.request.build_opener")
def test_login_for_token_rejects_missing_token(self, build_opener):
    build_opener.return_value.open.return_value = FakeResponse({"message": "ok"})
    with self.assertRaisesRegex(RuntimeError, "token"):
        login_for_token("http://localhost:8090", Credential("a@b.test", "secret"))

@patch("zap_runtime.urllib.request.build_opener")
def test_verify_authenticated_session_requires_success(self, build_opener):
    build_opener.return_value.open.return_value = FakeResponse({"email": "a@b.test"}, status=200)
    verify_authenticated_session("http://localhost:8090")
```

- [ ] **Step 2: Run tests and verify functions are missing**

Run: `rtk python -m unittest src/zap/test_zap_runtime.py`

Expected: ERROR importing login/verification functions.

- [ ] **Step 3: Implement proxied login and verification**

Add:

```python
import json
import urllib.error
import urllib.request

LOGIN_URL = "http://localhost:3000/api/login"
VERIFY_URL = "http://localhost:3000/api/users/me"


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
    except (OSError, urllib.error.URLError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"EShop login failed: {exc}") from exc
    token = payload.get("token")
    if not isinstance(token, str) or not token:
        raise RuntimeError("EShop login response did not contain a token")
    return token


def verify_authenticated_session(zap_url: str, timeout: int = 15) -> None:
    request = urllib.request.Request(VERIFY_URL, method="GET")
    try:
        with _proxy_opener(zap_url).open(request, timeout=timeout) as response:
            if response.status != 200:
                raise RuntimeError(f"Authentication verification returned HTTP {response.status}")
    except (OSError, urllib.error.URLError) as exc:
        raise RuntimeError(f"Authentication verification failed: {exc}") from exc
```

- [ ] **Step 4: Run runtime tests**

Run: `rtk python -m unittest src/zap/test_zap_runtime.py`

Expected: all tests pass.

- [ ] **Step 5: Commit JWT bootstrap**

```bash
rtk git add src/zap/zap_runtime.py src/zap/test_zap_runtime.py
rtk git commit -m "feat(zap): bootstrap EShop JWT authentication"
```

### Task 5: Configure context, ZAP user, Replacer and Forced User Mode

**Files:**
- Modify: `src/zap/zap_runtime.py`
- Modify: `src/zap/test_zap_runtime.py`

- [ ] **Step 1: Write failing ZAP configuration tests**

Use `MagicMock` and assert the API contract:

```python
from zap_runtime import configure_authenticated_context, cleanup_authenticated_context


def test_configure_authenticated_context_creates_scoped_user_and_replacer(self):
    zap = MagicMock()
    zap.context.context_list = []
    zap.context.new_context.return_value = "7"
    zap.users.users_list.return_value = []
    zap.users.new_user.return_value = "3"

    state = configure_authenticated_context(
        zap, Credential("test@eshop.com", "secret"), "jwt-value", forced_user=True
    )

    self.assertEqual(state.context_id, "7")
    self.assertEqual(state.user_id, "3")
    zap.context.include_in_context.assert_called_once_with("EShop", CONTEXT_REGEX)
    zap.context.set_context_in_scope.assert_called_once_with("EShop", "true")
    zap.users.set_user_enabled.assert_called_once_with("7", "3", "true")
    zap.replacer.add_rule.assert_called_once_with(
        REPLACER_RULE, "true", "REQ_HEADER", "false", "Authorization", "Bearer jwt-value"
    )
    zap.forcedUser.set_forced_user.assert_called_once_with("7", "3")
    zap.forcedUser.set_forced_user_mode_enabled.assert_called_once_with("true")

def test_cleanup_removes_secret_and_disables_forced_user(self):
    zap = MagicMock()
    cleanup_authenticated_context(zap, forced_user=True)
    zap.replacer.remove_rule.assert_called_once_with(REPLACER_RULE)
    zap.forcedUser.set_forced_user_mode_enabled.assert_called_once_with("false")
```

- [ ] **Step 2: Run tests and verify configuration functions are missing**

Run: `rtk python -m unittest src/zap/test_zap_runtime.py`

Expected: ERROR importing configuration helpers.

- [ ] **Step 3: Implement context/user/auth state**

Add:

```python
@dataclasses.dataclass(frozen=True)
class AuthState:
    context_id: str
    user_id: str


def ensure_context(zap) -> str:
    if CONTEXT_NAME not in zap.context.context_list:
        context_id = str(zap.context.new_context(CONTEXT_NAME))
        zap.context.include_in_context(CONTEXT_NAME, CONTEXT_REGEX)
    else:
        context_id = str(zap.context.context(CONTEXT_NAME)["id"])
        if CONTEXT_REGEX not in zap.context.include_regexs(CONTEXT_NAME):
            zap.context.include_in_context(CONTEXT_NAME, CONTEXT_REGEX)
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


def configure_authenticated_context(zap, credential: Credential, token: str, forced_user: bool) -> AuthState:
    context_id = ensure_context(zap)
    user_id = _user_id(zap, context_id, credential.email)
    try:
        zap.replacer.remove_rule(REPLACER_RULE)
    except Exception:
        pass
    zap.replacer.add_rule(
        REPLACER_RULE, "true", "REQ_HEADER", "false", "Authorization", f"Bearer {token}"
    )
    if forced_user:
        zap.forcedUser.set_forced_user(context_id, user_id)
        zap.forcedUser.set_forced_user_mode_enabled("true")
    return AuthState(context_id, user_id)


def cleanup_authenticated_context(zap, forced_user: bool) -> None:
    try:
        zap.replacer.remove_rule(REPLACER_RULE)
    finally:
        if forced_user:
            zap.forcedUser.set_forced_user_mode_enabled("false")
```

Ensure `configure_authenticated_context()` raises `RuntimeError` if the Replacer add-on/API is unavailable; do not continue without JWT injection.

- [ ] **Step 4: Run runtime tests**

Run: `rtk python -m unittest src/zap/test_zap_runtime.py`

Expected: all tests pass.

- [ ] **Step 5: Commit authenticated context support**

```bash
rtk git add src/zap/zap_runtime.py src/zap/test_zap_runtime.py
rtk git commit -m "feat(zap): configure authenticated scan context"
```

### Task 6: Refactor scan orchestration into the one-command workflow

**Files:**
- Modify: `src/zap/scan_zap.py`
- Create: `src/zap/test_scan_zap.py`

- [ ] **Step 1: Write failing parser and orchestration tests**

Create:

```python
import unittest
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent))

from scan_zap import build_parser, run


class ScanZapTests(unittest.TestCase):
    def test_parser_defaults_to_managed_anonymous_scan(self):
        args = build_parser().parse_args([])
        self.assertEqual(args.auth_role, "none")
        self.assertFalse(args.external_zap)
        self.assertEqual(
            Path(args.report_file),
            Path(__file__).resolve().parent / "output" / "zap_scan_report.html",
        )

    @patch("scan_zap.ZAPv2")
    @patch("scan_zap.ZapDockerManager")
    @patch("scan_zap.wait_for_zap")
    def test_run_stops_managed_container_on_connection_failure(self, wait_for_zap, manager_cls, zap_cls):
        manager = manager_cls.return_value
        wait_for_zap.side_effect = RuntimeError("not ready")
        args = build_parser().parse_args([])

        self.assertEqual(run(args), 1)
        manager.start.assert_called_once()
        manager.stop.assert_called_once()
```

Add this authenticated-flow test:

```python
    @patch("scan_zap.write_report")
    @patch("scan_zap.execute_scan")
    @patch("scan_zap.verify_authenticated_session")
    @patch("scan_zap.cleanup_authenticated_context")
    @patch("scan_zap.configure_authenticated_context")
    @patch("scan_zap.login_for_token", return_value="jwt-value")
    @patch("scan_zap.get_credential")
    @patch("scan_zap.ensure_context", return_value="7")
    @patch("scan_zap.wait_for_zap", return_value="2.16.1")
    @patch("scan_zap.ZapDockerManager")
    @patch("scan_zap.ZAPv2")
    def test_run_configures_and_cleans_authenticated_scan(
        self,
        zap_cls,
        manager_cls,
        wait_for_zap,
        ensure_context,
        get_credential,
        login_for_token,
        configure_authenticated_context,
        cleanup_authenticated_context,
        verify_authenticated_session,
        execute_scan,
        write_report,
    ):
        credential = MagicMock(email="test@eshop.com", password="secret")
        get_credential.return_value = credential
        configure_authenticated_context.return_value.context_id = "7"
        args = build_parser().parse_args(["--auth-role", "user", "--forced-user"])

        self.assertEqual(run(args), 0)

        login_for_token.assert_called_once_with(args.zap_url, credential)
        configure_authenticated_context.assert_called_once_with(
            zap_cls.return_value, credential, "jwt-value", True
        )
        verify_authenticated_session.assert_called_once_with(args.zap_url)
        execute_scan.assert_called_once_with(
            zap_cls.return_value, args.target, "7", False
        )
        cleanup_authenticated_context.assert_called_once_with(zap_cls.return_value, True)
        manager_cls.return_value.stop.assert_called_once()
```

- [ ] **Step 2: Run scan tests and verify parser/run are missing**

Run: `rtk python -m unittest src/zap/test_scan_zap.py`

Expected: ERROR importing `build_parser` or `run`.

- [ ] **Step 3: Implement CLI parser**

Refactor constants and parser:

```python
SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_REPORT_PATH = SCRIPT_DIR / "output" / "zap_scan_report.html"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run an automated OWASP ZAP scan for local EShop")
    parser.add_argument("--target", default="http://localhost:3000")
    parser.add_argument("--zap-url", default="http://localhost:8090")
    parser.add_argument("--api-key", default="")
    parser.add_argument("--auth-role", choices=["none", "user", "admin"], default="none")
    parser.add_argument("--forced-user", action="store_true")
    parser.add_argument("--ajax-spider", action="store_true")
    parser.add_argument("--external-zap", action="store_true")
    parser.add_argument("--report-format", default="html", choices=["html", "json", "xml", "md"])
    parser.add_argument("--report-file", default=str(DEFAULT_REPORT_PATH))
    return parser
```

- [ ] **Step 4: Implement daemon wait and scan helpers**

Add a bounded readiness loop:

```python
def wait_for_zap(zap, timeout: int = 60) -> str:
    deadline = time.monotonic() + timeout
    last_error = None
    while time.monotonic() < deadline:
        try:
            return zap.core.version
        except Exception as exc:
            last_error = exc
            time.sleep(1)
    raise RuntimeError(f"ZAP daemon was not ready within {timeout}s: {last_error}")
```

Update Traditional Spider to call `zap.spider.scan(target, contextname=CONTEXT_NAME)` and Active Scan to call `zap.ascan.scan(target, contextid=context_id)`. Call AJAX Spider as `zap.ajaxSpider.scan(target, inscope="true", contextname=CONTEXT_NAME)` and normalize its status with `.lower() == "stopped"`.

- [ ] **Step 5: Implement `run(args)` with guaranteed cleanup**

Use this control structure:

```python
def run(args) -> int:
    manager = None if args.external_zap else ZapDockerManager(port=urlparse(args.zap_url).port or 8090)
    zap = None
    auth_configured = False
    try:
        target = validate_target(args.target)
        if manager:
            manager.start()
        zap = ZAPv2(apikey=args.api_key, proxies={"http": args.zap_url, "https": args.zap_url})
        version = wait_for_zap(zap)
        credential = get_credential(args.auth_role)
        context_id = ensure_context(zap)
        if credential:
            token = login_for_token(args.zap_url, credential)
            state = configure_authenticated_context(zap, credential, token, args.forced_user)
            auth_configured = True
            context_id = state.context_id
            verify_authenticated_session(args.zap_url)
        execute_scan(zap, target, context_id, args.ajax_spider)
        write_report(zap, args.report_format, Path(args.report_file))
        return 0
    except (OSError, RuntimeError, ValueError, subprocess.SubprocessError) as exc:
        print(f"[!] {exc}", file=sys.stderr)
        return 1
    finally:
        try:
            if zap is not None and auth_configured:
                cleanup_authenticated_context(zap, args.forced_user)
        finally:
            if manager is not None:
                manager.stop()
```

Use the public `ensure_context(zap) -> str` from Task 5 in both authenticated and anonymous runs. Keep alert summary/report generation from the original script, but make report exceptions return failure rather than printing success.

- [ ] **Step 6: Run scan orchestration tests**

Run: `rtk python -m unittest src/zap/test_scan_zap.py`

Expected: all tests pass.

- [ ] **Step 7: Commit one-command scan orchestration**

```bash
rtk git add src/zap/scan_zap.py src/zap/test_scan_zap.py src/zap/zap_runtime.py src/zap/test_zap_runtime.py
rtk git commit -m "feat(zap): automate authenticated Docker scan"
```

### Task 7: Add the ZAP README

**Files:**
- Create: `src/zap/README.md`

- [ ] **Step 1: Write README content**

Include these sections with executable examples:

```markdown
# OWASP ZAP Workflow for EShop

## ZAP đang làm gì?
Giải thích DAST và pipeline Docker → context → JWT → spider → passive → active → report → AI triage.

## Yêu cầu
- Python 3
- Docker daemon
- `pip install python-owasp-zap-v2.4`
- EShop chạy trên cổng 3000 và frontend tùy mục tiêu

## Chạy scan
Anonymous, user, admin, SPA/AJAX và external-daemon examples.

## Tài khoản và biến môi trường
Document `ZAP_USER_EMAIL`, `ZAP_USER_PASSWORD`, `ZAP_ADMIN_EMAIL`, `ZAP_ADMIN_PASSWORD` without printing their values.

## Output và AI triage
Document `zap_scan_report.html`, `zap_ai_triage_report.md`, offline mode and `OPENROUTER_API_KEY`.

## Giới hạn và an toàn
Local allowlist, authorized targets only, Active Scan side effects, human validation.

## Khắc phục lỗi
Docker unavailable, ZAP timeout/image pull, EShop login failure, locked test account, missing Replacer/API and empty AJAX coverage.
```

Commands must use repository paths:

```bash
rtk python src/zap/scan_zap.py --target http://localhost:5173 --auth-role user --forced-user --ajax-spider
rtk python src/zap/scan_zap.py --target http://localhost:5174 --auth-role admin --forced-user --ajax-spider
rtk python src/zap/ai_triage_zap.py --input src/zap/output/zap_scan_report.html
```

- [ ] **Step 2: Verify every documented CLI flag exists**

Run: `rtk python src/zap/scan_zap.py --help`

Expected: help lists `--auth-role`, `--forced-user`, `--ajax-spider`, `--external-zap`, report and ZAP connection flags.

- [ ] **Step 3: Commit README**

```bash
rtk git add src/zap/README.md
rtk git commit -m "docs(zap): explain automated scan workflow"
```

### Task 8: Full verification and consistency pass

**Files:**
- Modify only if verification reveals an in-scope defect.

- [ ] **Step 1: Run the entire ZAP unit suite**

Run: `rtk python -m unittest discover -s src/zap -p 'test_*.py' -v`

Expected: all tests pass, with no network or Docker required because external behavior is mocked.

- [ ] **Step 2: Compile all ZAP Python files**

Run: `rtk python -m compileall -q src/zap`

Expected: exit code 0 and no output.

- [ ] **Step 3: Smoke-test both CLIs**

Run: `rtk python src/zap/scan_zap.py --help`

Run: `rtk python src/zap/ai_triage_zap.py --help`

Expected: both exit 0 and show paths under `src/zap`.

- [ ] **Step 4: Check formatting and unintended changes**

Run: `rtk git diff --check`

Run: `rtk git status --short`

Expected: no whitespace errors; pre-existing `eshop-sut/` and `src/zap/output/` remain untouched/untracked.

- [ ] **Step 5: Optional real integration scan**

Only when EShop backend/frontend and Docker are running:

```bash
rtk python src/zap/scan_zap.py \
  --target http://localhost:5173 \
  --auth-role user \
  --forced-user \
  --ajax-spider
```

Expected: ZAP container starts, `/api/users/me` verifies authentication, the report is written, and the managed container stops. If the environment is unavailable, report the integration test as not run rather than claiming it passed.

- [ ] **Step 6: Commit any verification-only fixes**

If Task 8 required code changes:

```bash
rtk git add src/zap
rtk git commit -m "test(zap): complete workflow verification"
```
