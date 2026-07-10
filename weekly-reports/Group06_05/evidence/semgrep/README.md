# Semgrep Evidence

Thư mục này chứa các evidence có thể chạy/đối chiếu cho phần Semgrep SAST của Group06_05.

## Nội dung

- `scan.md`: quy trình cài đặt, chạy scan và ảnh output.
- `scan_ai_triage_guide.md`: cách chạy Semgrep JSON output kết hợp AI triage.
- `finding_hardcoded_jwt_secret.md`: finding report cho lỗi hardcoded JWT secret.
- `failure_modes_metrics.md`: failure modes, hạn chế và metrics thực nghiệm.
- `semgrep_ai_triage.py`: script sinh báo cáo AI triage từ kết quả Semgrep JSON.
- `exploit.js`: PoC tạo JWT giả mạo bằng secret bị hardcode.
- `image/scan/`: ảnh minh chứng output Semgrep lấy từ `resources`.

## Luồng sử dụng nhanh

```bash
semgrep scan --config "p/owasp-top-ten" --json -o semgrep_results.json .
python weekly-reports/Group06_05/evidence/semgrep/semgrep_ai_triage.py semgrep_results.json
node weekly-reports/Group06_05/evidence/semgrep/exploit.js
```

Không commit `.env`, API key hoặc kết quả scan có thông tin nhạy cảm.
