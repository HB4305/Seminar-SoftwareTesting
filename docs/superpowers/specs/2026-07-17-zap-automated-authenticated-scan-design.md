# Thiết kế ZAP Automated Authenticated Scan

## Mục tiêu

Hoàn thiện các phần OWASP ZAP trong `src/zap` theo `src/combine/Security_Testing_Workflow_Plan.md`. Người dùng chỉ cần chạy Python script; script tự khởi động ZAP bằng Docker, đăng nhập EShop bằng JWT, thực hiện scan và xuất báo cáo. Đồng thời chuẩn hóa AI triage, test và tài liệu sử dụng.

## Phạm vi

- Sửa `scan_zap.py`, `ai_triage_zap.py` và các test trong `src/zap`.
- Thêm test riêng cho scan automation nếu cần.
- Thêm `src/zap/README.md`.
- Output mặc định nằm trong `src/zap/output` với tên `zap_scan_report.html` và `zap_ai_triage_report.md`.
- Không sửa source EShop, Semgrep hoặc combined report.

## Giao diện dòng lệnh

`scan_zap.py` hỗ trợ luồng mặc định tự quản lý Docker và các tùy chọn chính:

```bash
python src/zap/scan_zap.py \
  --target http://localhost:5173 \
  --auth-role user \
  --forced-user \
  --ajax-spider
```

- `--auth-role {none,user,admin}` chọn anonymous scan hoặc tài khoản seed tương ứng.
- `--external-zap` dùng daemon đã chạy thay vì tạo container.
- Các tùy chọn hiện có như `--target`, `--ajax-spider`, `--report-format` và `--report-file` tiếp tục được hỗ trợ.
- Credential có thể override bằng biến môi trường; script không in password hoặc JWT.

## Kiến trúc và data flow

1. Xác thực target thuộc allowlist EShop: `localhost`/`127.0.0.1` trên cổng `3000`, `5173` hoặc `5174`.
2. Nếu không có `--external-zap`, kiểm tra Docker, tạo container ZAP bằng host network và chờ API sẵn sàng.
3. Tạo hoặc tái sử dụng context `EShop`, include ba origin của hệ thống và đánh dấu in-scope.
4. Nếu chọn role, gửi `POST http://localhost:3000/api/login` với JSON credential qua proxy ZAP, đọc trường `token` và kiểm chứng bằng `GET /api/users/me`.
5. Tạo/enabled ZAP user cho email đã chọn. Cấu hình Replacer request-header để gắn `Authorization: Bearer <token>`; bật Forced User Mode khi có `--forced-user`.
6. Chạy Traditional Spider, AJAX Spider tùy chọn, đợi Passive Scan, rồi chạy Active Scan trong context.
7. Tổng hợp alert và ghi report vào `src/zap/output`.
8. Trong `finally`, xóa Replacer chứa token, tắt Forced User Mode và chỉ dừng container do script hiện tại tạo.

Replacer được chọn thay cho ZAP authentication script vì EShop lưu JWT trong JSON/localStorage. Cách này không phụ thuộc script-engine add-on và dễ kiểm thử tự động hơn, trong khi toàn bộ traffic scan vẫn do ZAP xử lý.

## AI triage

- Giữ model OpenRouter ở định dạng provider/model: `google/gemini-2.5-flash` và cập nhật test cho nhất quán.
- Chuẩn hóa xử lý path: input được resolve tuyệt đối; output mặc định là `src/zap/output/zap_ai_triage_report.md`; output truyền rõ ràng cũng được resolve tuyệt đối.
- Sửa các chuỗi hướng dẫn còn trỏ tới `docs/zap` thành `src/zap`.
- Giữ offline triage khi không có API key hoặc OpenRouter lỗi.

## Xử lý lỗi và an toàn

- Dừng sớm nếu thiếu Docker, daemon không sẵn sàng, target ngoài allowlist, login lỗi, response thiếu token hoặc verification thất bại.
- Không chạy Active Scan khi authenticated setup không hợp lệ.
- Báo lỗi ngắn gọn, có hành động khắc phục; trả exit code khác 0.
- Không ghi secret vào report, log hoặc file context.
- Active Scan chỉ dành cho EShop local được phép kiểm thử.

## Kiểm thử

- Unit test bằng mock cho role/credential selection, target validation, Docker lifecycle, daemon readiness, JWT extraction, verification, Replacer cleanup và context/user configuration.
- Sửa hai baseline failure hiện tại của `test_ai_triage_zap.py` và thêm assertion cho tên output chuẩn.
- Chạy `python -m unittest discover -s src/zap -p 'test_*.py'` và smoke-test `scan_zap.py --help`.
- Integration scan thật là bước tùy chọn vì cần EShop và Docker đang chạy; README cung cấp lệnh cho cả user và admin.

## README

`src/zap/README.md` giải thích ZAP/DAST, pipeline của script, prerequisites, cách chạy anonymous/user/admin, Docker tự động so với external daemon, output, AI/offline triage, biến môi trường, giới hạn và troubleshooting. README nhấn mạnh AI chỉ hỗ trợ triage; kết luận cuối cần evidence và human validation.
