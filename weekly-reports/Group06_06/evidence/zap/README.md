# OWASP ZAP Workflow for EShop

## ZAP đang làm gì?

OWASP ZAP được dùng để chạy DAST (Dynamic Application Security Testing): kiểm thử bảo mật trên ứng dụng đang chạy thật, từ góc nhìn HTTP/browser, thay vì chỉ đọc mã nguồn.

Pipeline hiện tại:

1. Khởi động ZAP bằng Docker, trừ khi dùng `--external-zap`.
2. Tạo context `EShop` và chỉ đưa các URL local được phép vào scope.
3. Nếu chọn `--auth-role user` hoặc `--auth-role admin`, script đăng nhập EShop, lấy JWT và cấu hình ZAP Replacer để tự gắn header `Authorization: Bearer ...`.
4. Nếu có `--forced-user`, bật Forced User Mode để ZAP scan dưới user đã cấu hình.
5. Chọn scan mode:
   - `basic`: dùng các ZAP scanner/rule mặc định đang được enable trong daemon.
   - `owasp-top10-2025`: tạo active scan policy riêng từ các scanner có tag `OWASP_2025_A*`; nếu ZAP API không trả metadata tag, script fallback sang danh sách active rule ID tương ứng OWASP Top 10 2025.
6. Chạy traditional spider, tùy chọn AJAX Spider cho SPA, chờ passive scan xử lý, rồi chạy active scan.
7. Ghi report HTML hoặc JSON bằng official ZAP Report Generation add-on ra file do người dùng chọn, mặc định là `src/zap/output/zap_scan_report.html`.
8. Sau khi scan xong, có thể dùng report HTML để đọc thủ công hoặc report JSON cho pipeline/AI đọc và đối chiếu PoC.

## Yêu cầu

- Python 3
- Docker daemon đang chạy, nếu không dùng `--external-zap`
- ZAP Report Generation add-on; image `ghcr.io/zaproxy/zaproxy:stable` thường đã có sẵn add-on này. Nếu daemon ngoài không có add-on, script fallback sang core report cũ.
- Cài thư viện ZAP API:

```bash
pip install python-owasp-zap-v2.4
```

- EShop backend chạy trên cổng `3000`
- Frontend chạy trên cổng phù hợp với mục tiêu scan, ví dụ `5173` cho user hoặc `5174` cho admin

## Cấu hình `.env`

Copy file mẫu rồi sửa giá trị local/CI nếu cần:

```bash
cp src/zap/.env.example src/zap/.env
```

Script tự đọc `src/zap/.env`. Thứ tự ưu tiên là CLI flag > biến môi trường/`.env` > default trong code. Không commit `.env` thật.

## Chạy scan

Anonymous scan backend mặc định:

```bash
python src/zap/scan_zap.py --target http://localhost:3000
```

Backend scan theo OWASP Top 10 2025, output riêng:

```bash
python src/zap/scan_zap.py --target http://localhost:3000 --scan-mode owasp-top10-2025 --output-file src/zap/output/backend_owasp2025.html
```

User scan cho frontend user/SPA:

```bash
python src/zap/scan_zap.py --target http://localhost:5173 --auth-role user --forced-user --ajax-spider --output-file src/zap/output/frontend_user.html
```

Admin scan cho frontend admin/SPA:

```bash
python src/zap/scan_zap.py --target http://localhost:5174 --auth-role admin --forced-user --ajax-spider --output-file src/zap/output/frontend_admin.html
```

Frontend user/admin theo OWASP Top 10 2025:

```bash
python src/zap/scan_zap.py --target http://localhost:5173 --auth-role user --forced-user --ajax-spider --scan-mode owasp-top10-2025 --output-file src/zap/output/frontend_user_owasp2025.html
python src/zap/scan_zap.py --target http://localhost:5174 --auth-role admin --forced-user --ajax-spider --scan-mode owasp-top10-2025 --output-file src/zap/output/frontend_admin_owasp2025.html
```

Scan với ZAP daemon tự quản lý bên ngoài:

```bash
python src/zap/scan_zap.py --target http://localhost:5173 --auth-role user --forced-user --ajax-spider --external-zap --zap-url http://localhost:8090
```

Nếu external ZAP daemon bật bảo vệ API key, truyền thêm `--api-key ...`.

Khi dùng `--external-zap` cùng `--auth-role`, chỉ trỏ `--zap-url` đến ZAP daemon local (`http://localhost...` hoặc `http://127.0.0.1...`). ZAP bên ngoài có thể lưu request đăng nhập và JWT trong history/session; hãy dùng session/container ZAP local dùng một lần, hoặc tự clear session/history sau khi scan. Script chỉ tự dọn secret cho ZAP container do script quản lý, không đảm bảo xóa sạch history/session của ZAP external.

Tùy chỉnh report:

```bash
python src/zap/scan_zap.py --target http://localhost:3000 --report-format json --report-file src/zap/output/zap_scan_report.json
```

`--output-file` là alias rõ nghĩa của `--report-file`, dùng khi muốn đặt path/tên file theo target demo:

```bash
python src/zap/scan_zap.py --target http://localhost:3000 --output-file src/zap/output/backend_basic.html
python src/zap/scan_zap.py --target http://localhost:3000 --report-format json --output-file src/zap/output/backend_basic.json
```

`--report-format` chỉ nhận `html` hoặc `json`. Report HTML mặc định dùng official template `modern` để đọc thủ công. Report JSON dùng official template `traditional-json-plus` để pipeline/AI parse ổn định hơn. Cả hai template có thể chứa metadata/tag của alert, nên các tag dạng `OWASP_2021_Axx` hoặc `OWASP_2025_Axx` sẽ hiện trong report nếu scanner/alert của ZAP daemon có metadata đó. Với `--external-zap` chạy trong Docker riêng, hãy mount thư mục output vào container ZAP; với container do script tự chạy, script tự mount thư mục chứa report.

## Tài khoản và biến môi trường

Các biến trong `src/zap/.env.example` có thể điều khiển scan mà không cần sửa code:

- `ZAP_TARGET`
- `ZAP_URL`
- `ZAP_API_KEY`
- `ZAP_IMAGE`
- `ZAP_AUTH_ROLE` (`none`, `user`, `admin`)
- `ZAP_FORCED_USER`
- `ZAP_AJAX_SPIDER`
- `ZAP_EXTERNAL_ZAP`
- `ZAP_SCAN_MODE` (`basic`, `owasp-top10-2025`)
- `ZAP_REPORT_FORMAT`
- `ZAP_REPORT_FILE`
- `ZAP_USER_EMAIL`
- `ZAP_USER_PASSWORD`
- `ZAP_ADMIN_EMAIL`
- `ZAP_ADMIN_PASSWORD`
- `OPENROUTER_API_KEY`
- `OPENROUTER_MODEL`

Script có tài khoản test mặc định cho `user` và `admin`, nhưng nên override bằng `.env`, biến môi trường shell, hoặc CI secret. Không in hoặc commit giá trị thật của các biến secret.

Ví dụ chạy sau khi đã export biến trong shell/CI secret:

```bash
python src/zap/scan_zap.py --target http://localhost:5173 --auth-role user --forced-user --ajax-spider
```

Ví dụ chạy hoàn toàn bằng `.env`:

```bash
python src/zap/scan_zap.py
```

Ví dụ `.env` cho backend theo OWASP Top 10 2025:

```env
ZAP_TARGET=http://localhost:3000
ZAP_SCAN_MODE=owasp-top10-2025
ZAP_REPORT_FILE=src/zap/output/backend_owasp2025.html
```

## Output và AI triage

Report scan mặc định:

- `src/zap/output/zap_scan_report.html`

Report JSON cho pipeline/AI:

```bash
python src/zap/scan_zap.py --target http://localhost:3000 --report-format json --output-file src/zap/output/backend_zap.json
```

Chạy triage offline từ report HTML:

```bash
python src/zap/ai_triage_zap.py --input src/zap/output/zap_scan_report.html
```

Nếu bỏ `--input`, `ai_triage_zap.py` sẽ dùng report HTML mới nhất trong `src/zap/output/*.html`.

Output triage mặc định:

- `src/zap/output/zap_ai_triage_report.md`

Mặc định triage chạy offline, không gọi AI. Muốn dùng OpenRouter, cấu hình `OPENROUTER_API_KEY` trong secret/shell rồi thêm `--use-ai`:

```bash
python src/zap/ai_triage_zap.py --input src/zap/output/zap_scan_report.html --use-ai
```

## Giới hạn và an toàn

- Script chỉ allowlist target local EShop: `http://localhost` hoặc `http://127.0.0.1` trên cổng `3000`, `5173`, `5174`.
- Với authenticated scan, `--zap-url` cũng phải là ZAP daemon HTTP local để tránh gửi credentials qua proxy từ xa hoặc không tin cậy.
- `owasp-top10-2025` chỉ giới hạn active scan vào các scanner OWASP 2025 mà ZAP daemon hiện tại có cài; nếu daemon không trả `alertTags`, script dùng fallback theo active rule ID. Chế độ này không chứng minh tự động rằng toàn bộ OWASP Top 10 đã được cover đầy đủ.
- Chỉ scan hệ thống bạn được phép kiểm thử.
- Active Scan có thể gửi payload tấn công, tạo dữ liệu rác, khóa tài khoản test hoặc thay đổi trạng thái ứng dụng.
- Kết quả ZAP và AI triage là tín hiệu hỗ trợ; cần con người xác thực lại trước khi kết luận hoặc tạo issue bảo mật.

## Khắc phục lỗi

- Docker unavailable: kiểm tra Docker đã cài, daemon đang chạy và user hiện tại có quyền chạy `docker`.
- ZAP timeout hoặc image pull chậm: kiểm tra mạng, pull trước image `ghcr.io/zaproxy/zaproxy:stable`, hoặc chạy ZAP riêng rồi dùng `--external-zap --zap-url http://localhost:8090`.
- EShop login failure: đảm bảo backend ở `http://localhost:3000`, tài khoản/password đúng, API `/api/login` trả token và biến môi trường không bị cấu hình sai.
- Locked test account: reset dữ liệu test hoặc đổi sang tài khoản test khác qua `ZAP_USER_EMAIL`/`ZAP_USER_PASSWORD` hoặc `ZAP_ADMIN_EMAIL`/`ZAP_ADMIN_PASSWORD`.
- Missing Replacer/API: đảm bảo ZAP daemon bật API và hỗ trợ Replacer; với Docker mặc định script chạy ZAP bằng `api.disablekey=true`.
- Missing OWASP tags trong report: đảm bảo dùng report HTML official add-on, không phải core report fallback; kiểm tra log không có dòng `Official Report Generation failed`.
- Empty AJAX coverage: xác nhận frontend đúng port, SPA đã build/chạy ổn định, route cần scan reachable sau đăng nhập, và command có `--ajax-spider`.
