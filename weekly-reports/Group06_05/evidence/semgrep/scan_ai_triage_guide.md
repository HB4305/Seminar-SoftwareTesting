# Hướng dẫn chạy Semgrep Scan + AI Triage

## 1. Chuẩn bị

Cài thư viện Python cần thiết cho script AI triage:

```bash
pip install -r weekly-reports/Group06_05/evidence/semgrep/requirements.txt
```

Tạo file `.env` hoặc cấu hình biến môi trường từ `.env.example`:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Trên PowerShell có thể set trực tiếp:

```powershell
$env:GEMINI_API_KEY="your_gemini_api_key_here"
```

## 2. Chạy Semgrep và tạo input JSON

```bash
semgrep scan --config "p/owasp-top-ten" --json -o semgrep_results.json .
```

## 3. Chạy AI triage

```bash
python weekly-reports/Group06_05/evidence/semgrep/semgrep_ai_triage.py semgrep_results.json
```

Script sẽ đọc finding đầu tiên trong file JSON, lấy thông tin rule, file, dòng code và gửi sang Gemini để tạo báo cáo Markdown.

## 4. Kết quả đầu ra

Các artefact chính trong thư mục evidence:

- `scan.md`: evidence cách cài đặt, scan và finding chính.
- `semgrep_ai_triage.py`: script AI triage dùng Gemini.
- `exploit.js`: PoC tạo JWT giả mạo từ secret bị hardcode.
- `finding_hardcoded_jwt_secret.md`: báo cáo finding đã triage.
- `failure_modes_metrics.md`: failure modes và metrics thực nghiệm.
- `image/scan/*.png`: ảnh minh chứng output Semgrep.

## 5. Lưu ý khi audit AI

- AI triage chỉ là bản phân tích hỗ trợ, không thay thế kiểm chứng thủ công.
- Cần kiểm tra lại tên file, dòng code, rule ID và khả năng chạy được của PoC.
- Cần deduplicate finding có cùng root cause trước khi đưa vào báo cáo cuối.
- Không commit `.env`, API key hoặc file output có secret thật.
