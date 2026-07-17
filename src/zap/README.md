# OWASP ZAP Workflow for EShop

## ZAP đang làm gì?

OWASP ZAP được dùng để chạy DAST (Dynamic Application Security Testing): kiểm thử bảo mật trên ứng dụng đang chạy thật, từ góc nhìn HTTP/browser, thay vì chỉ đọc mã nguồn.

Pipeline hiện tại:

1. Khởi động ZAP bằng Docker, trừ khi dùng `--external-zap`.
2. Tạo context `EShop` và chỉ đưa các URL local được phép vào scope.
3. Nếu chọn `--auth-role user` hoặc `--auth-role admin`, script đăng nhập EShop, lấy JWT và cấu hình ZAP Replacer để tự gắn header `Authorization: Bearer ...`.
4. Nếu có `--forced-user`, bật Forced User Mode để ZAP scan dưới user đã cấu hình.
5. Chạy traditional spider, tùy chọn AJAX Spider cho SPA, chờ passive scan xử lý, rồi chạy active scan.
6. Ghi report ra file, mặc định là `src/zap/output/zap_scan_report.html`.
7. Chạy AI triage từ report HTML để tạo bản tóm tắt ưu tiên xử lý.

## Yêu cầu

- Python 3
- Docker daemon đang chạy, nếu không dùng `--external-zap`
- Cài thư viện ZAP API:

```bash
pip install python-owasp-zap-v2.4
```

- EShop backend chạy trên cổng `3000`
- Frontend chạy trên cổng phù hợp với mục tiêu scan, ví dụ `5173` cho user hoặc `5174` cho admin

## Chạy scan

Anonymous scan backend mặc định:

```bash
rtk python src/zap/scan_zap.py --target http://localhost:3000
```

User scan cho frontend user/SPA:

```bash
rtk python src/zap/scan_zap.py --target http://localhost:5173 --auth-role user --forced-user --ajax-spider
```

Admin scan cho frontend admin/SPA:

```bash
rtk python src/zap/scan_zap.py --target http://localhost:5174 --auth-role admin --forced-user --ajax-spider
```

Scan với ZAP daemon tự quản lý bên ngoài:

```bash
rtk python src/zap/scan_zap.py --target http://localhost:5173 --auth-role user --forced-user --ajax-spider --external-zap --zap-url http://localhost:8090
```

Tùy chỉnh report:

```bash
rtk python src/zap/scan_zap.py --target http://localhost:3000 --report-format md --report-file src/zap/output/zap_scan_report.md
```

## Tài khoản và biến môi trường

Script có tài khoản test mặc định cho `user` và `admin`, nhưng nên override bằng biến môi trường khi chạy trên máy/CI riêng. Không in hoặc commit giá trị thật của các biến này.

- `ZAP_USER_EMAIL`
- `ZAP_USER_PASSWORD`
- `ZAP_ADMIN_EMAIL`
- `ZAP_ADMIN_PASSWORD`

Ví dụ chạy sau khi đã export biến trong shell/CI secret:

```bash
rtk python src/zap/scan_zap.py --target http://localhost:5173 --auth-role user --forced-user --ajax-spider
```

## Output và AI triage

Report scan mặc định:

- `src/zap/output/zap_scan_report.html`

Chạy triage offline từ report HTML:

```bash
rtk python src/zap/ai_triage_zap.py --input src/zap/output/zap_scan_report.html
```

Output triage mặc định:

- `src/zap/output/zap_ai_triage_report.md`

Mặc định triage chạy offline, không gọi AI. Muốn dùng OpenRouter, cấu hình `OPENROUTER_API_KEY` trong secret/shell rồi thêm `--use-ai`:

```bash
rtk python src/zap/ai_triage_zap.py --input src/zap/output/zap_scan_report.html --use-ai
```

## Giới hạn và an toàn

- Script chỉ allowlist target local EShop: `http://localhost` hoặc `http://127.0.0.1` trên cổng `3000`, `5173`, `5174`.
- Chỉ scan hệ thống bạn được phép kiểm thử.
- Active Scan có thể gửi payload tấn công, tạo dữ liệu rác, khóa tài khoản test hoặc thay đổi trạng thái ứng dụng.
- Kết quả ZAP và AI triage là tín hiệu hỗ trợ; cần con người xác thực lại trước khi kết luận hoặc tạo issue bảo mật.

## Khắc phục lỗi

- Docker unavailable: kiểm tra Docker đã cài, daemon đang chạy và user hiện tại có quyền chạy `docker`.
- ZAP timeout hoặc image pull chậm: kiểm tra mạng, pull trước image `ghcr.io/zaproxy/zaproxy:stable`, hoặc chạy ZAP riêng rồi dùng `--external-zap --zap-url http://localhost:8090`.
- EShop login failure: đảm bảo backend ở `http://localhost:3000`, tài khoản/password đúng, API `/api/login` trả token và biến môi trường không bị cấu hình sai.
- Locked test account: reset dữ liệu test hoặc đổi sang tài khoản test khác qua `ZAP_USER_EMAIL`/`ZAP_USER_PASSWORD` hoặc `ZAP_ADMIN_EMAIL`/`ZAP_ADMIN_PASSWORD`.
- Missing Replacer/API: đảm bảo ZAP daemon bật API và hỗ trợ Replacer; với Docker mặc định script chạy ZAP bằng `api.disablekey=true`.
- Empty AJAX coverage: xác nhận frontend đúng port, SPA đã build/chạy ổn định, route cần scan reachable sau đăng nhập, và command có `--ajax-spider`.
