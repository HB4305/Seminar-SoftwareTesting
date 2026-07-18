# Hướng dẫn chạy Semgrep từ root

Tài liệu này chỉ mô tả cách chạy. Script, test, requirements, pipeline và output runtime nằm trong `src/semgrep/`.

## 1. Chuẩn bị môi trường Python

Chạy từ root repo `Seminar-SoftwareTesting`:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r src/semgrep/requirements.txt
```

Nếu đã tạo `.venv` trước đó thì chỉ cần:

```bash
source .venv/bin/activate
python -m pip install -r src/semgrep/requirements.txt
```

## 2. Cấu hình OpenRouter

```bash
cp src/semgrep/.env.example src/semgrep/.env
```

Mở `src/semgrep/.env` và điền API key thật:

```env
AI_PROVIDER=openai-compatible
AI_MODEL=google/gemini-2.5-flash-lite
OPENROUTER_API_KEY=sk-or-v1-...
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
```

Không commit file `src/semgrep/.env`.

## 3. Chạy scan + AI triage

Mặc định pipeline quét source ở `../eshop-sut` và xuất toàn bộ kết quả vào `src/semgrep/output/`.

```bash
bash src/semgrep/run_semgrep_pipeline.sh
```

Nếu source nằm chỗ khác:

```bash
SOURCE_ROOT="/path/to/eshop-sut" bash src/semgrep/run_semgrep_pipeline.sh
```

## 4. Output

```bash
ls src/semgrep/output
ls src/semgrep/output/findings
```

Các output chính:

- `src/semgrep/output/semgrep_results.json`: kết quả Semgrep JSON.
- `src/semgrep/output/semgrep_triage_report.md`: báo cáo tổng hợp.
- `src/semgrep/output/findings/`: prompt và AI output riêng cho từng finding.

## 5. Chạy thủ công từng bước

```bash
mkdir -p src/semgrep/output
semgrep scan --config "p/owasp-top-ten" --config "p/nodejs" \
  --exclude node_modules --exclude dist --exclude build --exclude .next \
  --json -o src/semgrep/output/semgrep_results.json ../eshop-sut

python src/semgrep/semgrep_ai_triage.py \
  src/semgrep/output/semgrep_results.json \
  --source-root ../eshop-sut \
  --output-dir src/semgrep/output
```
