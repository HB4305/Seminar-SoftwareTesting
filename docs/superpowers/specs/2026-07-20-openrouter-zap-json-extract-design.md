# OpenRouter ZAP JSON Extract Design

## Goal

Create a CLI script that reads one or more OWASP ZAP JSON reports from `src/zap/output`, sends the parsed alert instances to OpenRouter using a Gemini model, and writes a user-selected Markdown or HTML report.

## Requirements

- Accept one or more JSON input files.
- Let the user choose output format: `markdown` or `html`.
- Require a user-selected output path.
- Read runtime parameters from `src/zap/.env` and environment variables.
- Use OpenRouter with a Gemini model, defaulting to `google/gemini-2.5-flash`.
- Fail with a clear non-zero error if the API key is missing or OpenRouter cannot be called.
- Include every alert instance in the result.
- For each alert instance, include:
  - alert details and explanation,
  - OWASP tags, with emphasis on OWASP Top 10 mapping,
  - PoC method, endpoint, and payload/body/query/header fields where available,
  - instructions to verify the PoC in Postman or curl.

## Architecture

Add a new focused script at `src/zap/openrouter_zap_json_extract.py`. It will not replace the existing ZAP scanner or Postman converter. The script owns five responsibilities: dotenv loading, ZAP JSON parsing, prompt construction, OpenRouter calling, and Markdown/HTML rendering.

The parser will normalize ZAP's `site[] -> alerts[] -> instances[]` structure into a simple `ExtractedAlert` dataclass. Each instance becomes one report item, because ZAP alerts often group multiple endpoints under one finding.

## CLI

```bash
python src/zap/openrouter_zap_json_extract.py \
  --input src/zap/output/backend_basic.json src/zap/output/frontend_user_basic.json \
  --format markdown \
  --output src/zap/output/zap_openrouter_result.md
```

```bash
python src/zap/openrouter_zap_json_extract.py \
  --input src/zap/output/backend_basic.json \
  --format html \
  --output src/zap/output/backend_openrouter_result.html
```

## Environment

The script reads `src/zap/.env` first without overriding existing shell variables.

- `OPENROUTER_API_KEY`: required.
- `OPENROUTER_MODEL`: optional, default `google/gemini-2.5-flash`.
- `OPENROUTER_BASE_URL`: optional, default `https://openrouter.ai/api/v1/chat/completions`.
- `OPENROUTER_TIMEOUT`: optional integer seconds, default `60`.

## Output

The OpenRouter prompt will request Vietnamese structured Markdown. Markdown output is written directly. HTML output wraps the generated Markdown-like content in escaped HTML with headings and preformatted blocks, avoiding extra dependencies.

## Error Handling

Missing input files, invalid JSON, missing API key, network errors, HTTP errors, malformed OpenRouter responses, and unwritable output paths all return non-zero CLI failures with direct error messages.

## Testing

Add `src/zap/test_openrouter_zap_json_extract.py` using `unittest`, matching the existing test style. Tests will cover parsing multiple files, tag extraction, prompt content, missing API key failures, Markdown rendering, and HTML rendering without real network calls.
