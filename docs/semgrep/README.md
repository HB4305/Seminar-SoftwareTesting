# Hướng dẫn chạy Semgrep từ root

Tài liệu này mô tả cách chạy Semgrep thủ công từng bước. Script, test, requirements và output runtime nằm trong `src/semgrep/`.

## 1. Chuẩn bị môi trường

Chạy từ root repo `Seminar-SoftwareTesting`. Chọn lệnh activate theo terminal đang dùng.

**Option 1: PowerShell**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r src/semgrep/requirements.txt
```

**Option 2: Git Bash/Bash**

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r src/semgrep/requirements.txt
```

Cài Semgrep CLI nếu máy chưa có:

```bash
python3 -m pip install semgrep
```

Kiểm tra Semgrep:

```bash
semgrep --version
```

## 2. Cấu hình AI triage

Nếu muốn gọi AI online, tạo file cấu hình:

```powershell
copy src\semgrep\.env.example src\semgrep\.env
```

Điền API key thật vào `src/semgrep/.env`:

```env
AI_PROVIDER=openai-compatible
AI_MODEL=google/gemini-2.5-flash-lite
OPENROUTER_API_KEY=sk-or-v1-...
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
```

Không commit file `src/semgrep/.env`.

Nếu chỉ muốn sinh report/prompt mà không gọi AI, không cần cấu hình `.env`; thêm `--offline` ở bước triage.

## 3. Chạy Semgrep scan

Tạo thư mục output:

```bash
mkdir -p src/semgrep/output
```

Chọn source root theo vị trí source EShop.

**Option 1: Source nằm trong repo tại `eshop-sut/`**

PowerShell:

```powershell
semgrep scan --config "p/owasp-top-ten" --exclude node_modules --exclude dist --exclude build --exclude .next --json -o src/semgrep/output/semgrep_results.json ./eshop-sut
```

Git Bash/Bash:

```bash
semgrep scan \
  --config "p/owasp-top-ten" \
  --exclude node_modules \
  --exclude dist \
  --exclude build \
  --exclude .next \
  --json \
  -o src/semgrep/output/semgrep_results.json \
  ./eshop-sut
```

**Option 2: Source nằm ở path khác**

Đặt biến `SOURCE_ROOT` rồi dùng lại biến đó trong lệnh scan:

PowerShell:

```powershell
$env:SOURCE_ROOT="C:\path\to\eshop-sut"
semgrep scan --config "p/owasp-top-ten" --exclude node_modules --exclude dist --exclude build --exclude .next --json -o src/semgrep/output/semgrep_results.json $env:SOURCE_ROOT
```

Git Bash/Bash:

```bash
SOURCE_ROOT="/path/to/eshop-sut"

semgrep scan \
  --config "p/owasp-top-ten" \
  --exclude node_modules \
  --exclude dist \
  --exclude build \
  --exclude .next \
  --json \
  -o src/semgrep/output/semgrep_results.json \
  "$SOURCE_ROOT"
```

Lưu ý: Theo đề T09, lệnh scan chính dùng `p/owasp-top-ten` để quét EShop theo OWASP Top 10.

**Quét mở rộng cho EShop**

Sau khi đã có kết quả bắt buộc theo OWASP Top 10, có thể chạy thêm ruleset theo công nghệ của EShop để phân tích sâu hơn:

```bash
semgrep scan \
  --config "p/owasp-top-ten" \
  --config "p/nodejs" \
  --config "p/javascript" \
  --config "p/react" \
  --config "src/semgrep/rules/eshop-security.yml" \
  --exclude node_modules \
  --exclude dist \
  --exclude build \
  --exclude .next \
  --json \
  -o src/semgrep/output/semgrep_results_extended.json \
  ./eshop-sut
```

Lệnh mở rộng này không thay thế lệnh OWASP Top 10 trong yêu cầu chính; nó dùng để đối chiếu rule coverage và phân tích failure modes.

## 4. Chạy AI triage

Chạy triage từ file JSON vừa tạo. Dùng cùng source root đã chọn ở bước scan.

**Option 1: Source nằm trong repo tại `eshop-sut/`**

```PowerShell
python src/semgrep/semgrep_ai_triage.py src/semgrep/output/semgrep_results.json --source-root eshop-sut --output-dir src/semgrep/output
```

**Option 2: Source nằm ở path khác**

```bash
python src/semgrep/semgrep_ai_triage.py \
  src/semgrep/output/semgrep_results.json \
  --source-root "$SOURCE_ROOT" \
  --output-dir src/semgrep/output
```

Chạy offline nếu chưa cần gọi AI. Ví dụ với source trong repo:

```bash
python src/semgrep/semgrep_ai_triage.py \
  src/semgrep/output/semgrep_results.json \
  --source-root eshop-sut \
  --output-dir src/semgrep/output \
  --offline
```

## 5. Output

Sau khi chạy xong, kiểm tra:

```bash
ls src/semgrep/output
ls src/semgrep/output/findings
```

Các output chính:

- `src/semgrep/output/semgrep_results.json`: kết quả Semgrep JSON.
- `src/semgrep/output/semgrep_triage_report.md`: báo cáo tổng hợp findings và AI output.
- `src/semgrep/output/semgrep_postman_validation_report.md`: format lỗi theo Postman/ZAP comparison.
- `src/semgrep/output/findings/`: prompt và AI output riêng cho từng finding.
