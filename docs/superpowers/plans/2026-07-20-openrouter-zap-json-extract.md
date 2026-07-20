# OpenRouter ZAP JSON Extract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a CLI tool that sends one or more ZAP JSON reports to OpenRouter/Gemini and outputs a Markdown or HTML report containing alert explanations, tags, PoCs, and verification steps.

**Architecture:** Add one focused Python module under `src/zap`. Keep tests in the existing `unittest` style. Avoid external Markdown/HTML dependencies.

**Tech Stack:** Python 3 standard library, `unittest`, OWASP ZAP JSON report schema, OpenRouter chat completions API.

---

## File Structure

- Create `src/zap/openrouter_zap_json_extract.py`: CLI, dotenv loading, ZAP JSON parsing, prompt building, OpenRouter call, report rendering.
- Create `src/zap/test_openrouter_zap_json_extract.py`: unit tests for parser, prompt, rendering, and API-key error handling.
- Modify `src/zap/.env.example`: document OpenRouter settings used by the new script.

### Task 1: Parser and Prompt Tests

**Files:**
- Create: `src/zap/test_openrouter_zap_json_extract.py`
- Create later: `src/zap/openrouter_zap_json_extract.py`

- [ ] **Step 1: Write failing parser/prompt tests**

Create tests that import `parse_zap_json_files`, `build_prompt`, and `ExtractedAlert`. Use two temporary JSON files. Assert that every ZAP instance becomes an alert, OWASP/CWE/WASC tags are normalized, PoC fields include method/endpoint/payload, and the prompt contains the required Vietnamese sections.

- [ ] **Step 2: Run parser/prompt tests to verify failure**

Run: `rtk python -m unittest src.zap.test_openrouter_zap_json_extract -v`

Expected: fail with `ModuleNotFoundError` or missing imported functions.

- [ ] **Step 3: Implement minimal parser and prompt code**

Create `src/zap/openrouter_zap_json_extract.py` with:
- `ExtractedAlert` dataclass.
- `load_dotenv`.
- `parse_zap_json_files`.
- `parse_zap_report`.
- `extract_tags`.
- `build_poc_fields`.
- `build_prompt`.

- [ ] **Step 4: Run parser/prompt tests to verify pass**

Run: `rtk python -m unittest src.zap.test_openrouter_zap_json_extract -v`

Expected: parser/prompt tests pass.

### Task 2: OpenRouter and Render Tests

**Files:**
- Modify: `src/zap/test_openrouter_zap_json_extract.py`
- Modify: `src/zap/openrouter_zap_json_extract.py`

- [ ] **Step 1: Write failing API/render tests**

Add tests for:
- missing `OPENROUTER_API_KEY` raises a runtime error,
- `render_markdown` includes AI content and source names,
- `render_html` escapes generated content and creates HTML,
- CLI argument parser accepts multiple `--input` values plus required `--format` and `--output`.

- [ ] **Step 2: Run API/render tests to verify failure**

Run: `rtk python -m unittest src.zap.test_openrouter_zap_json_extract -v`

Expected: fail because API/render/CLI functions are missing.

- [ ] **Step 3: Implement API/render/CLI code**

Add:
- `OpenRouterConfig`.
- `config_from_env`.
- `call_openrouter`.
- `render_markdown`.
- `render_html`.
- `build_parser`.
- `main`.

Do not call the real network in unit tests; test config and rendering only.

- [ ] **Step 4: Run tests to verify pass**

Run: `rtk python -m unittest src.zap.test_openrouter_zap_json_extract -v`

Expected: all tests in the new file pass.

### Task 3: Env Documentation and Full Verification

**Files:**
- Modify: `src/zap/.env.example`
- Verify: `src/zap/test_openrouter_zap_json_extract.py`
- Verify: existing ZAP tests that may be affected.

- [ ] **Step 1: Update `.env.example`**

Add:
- `OPENROUTER_BASE_URL=https://openrouter.ai/api/v1/chat/completions`
- `OPENROUTER_TIMEOUT=60`

- [ ] **Step 2: Run focused tests**

Run: `rtk python -m unittest src.zap.test_openrouter_zap_json_extract -v`

Expected: all tests pass.

- [ ] **Step 3: Run related ZAP tests**

Run: `rtk python -m unittest discover -s src/zap -p 'test*.py' -v`

Expected: unrelated pre-existing failures, if any, are reported clearly; new extractor tests pass.

- [ ] **Step 4: Review git diff**

Run: `rtk git diff -- docs/superpowers/specs/2026-07-20-openrouter-zap-json-extract-design.md docs/superpowers/plans/2026-07-20-openrouter-zap-json-extract.md src/zap/openrouter_zap_json_extract.py src/zap/test_openrouter_zap_json_extract.py src/zap/.env.example`

Expected: only intended files changed.
