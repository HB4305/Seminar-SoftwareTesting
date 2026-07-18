# Kế hoạch hoàn thiện Security Testing Workflow

Tài liệu này đề xuất các bước tiếp theo để hoàn thiện workflow trong `Security_Testing_Workflow.md`, dựa trên mã nguồn hiện có trong `src/semgrep` và `src/zap`.

## Mục tiêu

Hoàn thiện pipeline kiểm thử bảo mật end-to-end:

```text
Semgrep SAST -> AI triage -> PoC/testcase -> OWASP ZAP DAST -> đối chiếu chéo -> báo cáo tổng hợp
```

## Hiện trạng trong `src`

- `src/semgrep/sg_rs.json`: kết quả scan Semgrep hiện tại; số findings phụ thuộc vào nội dung mảng `results`.
- `src/semgrep/semgrep_ai_triage.py`: script gửi toàn bộ findings Semgrep sang provider AI đã cấu hình để phân tích.
- `src/zap/scan_zap.py`: script chạy OWASP ZAP scan và xuất report.
- `src/zap/ai_triage_zap.py`: script parse ZAP HTML report, tạo AI/offline triage markdown và block cho submission.
- `src/zap/test_ai_triage_zap.py`: unit test cho parser và renderer của ZAP AI triage.

## Việc cần làm tiếp theo

### 1. Ổn định test và cấu hình ZAP AI triage

- Sửa `DEFAULT_MODEL` hoặc test để thống nhất model giữa `ai_triage_zap.py` và `test_ai_triage_zap.py`.
- Sửa kỳ vọng của `resolve_output_path()` để thống nhất dùng path tuyệt đối hoặc tương đối.
- Chạy lại:

```bash
rtk python -m unittest src/zap/test_ai_triage_zap.py
```

### 2. Mở rộng Semgrep AI triage

- Script Semgrep phải xử lý toàn bộ `results`, không hardcode số lượng findings theo một report cụ thể.
- Sinh một file tổng hợp theo rule, file, dòng, severity, CWE, OWASP, likelihood, impact, confidence.
- Với mỗi finding, lưu prompt, output AI, nhận định true positive/false positive và phần human validation.
- Khi `extra.lines` là `requires login`, fallback đọc source code bằng `path` và `start.line`.

### 3. Chuẩn hóa output giữa Semgrep và ZAP

- Đặt output Semgrep AI triage vào một thư mục cố định, ví dụ `src/semgrep/output`.
- Đặt output ZAP scan và ZAP AI triage vào `src/zap/output`.
- Dùng naming thống nhất:

```text
semgrep_triage_report.md
zap_scan_report.html
zap_ai_triage_report.md
combined_security_report.md
```

### 4. Cấu hình ZAP để quét sau đăng nhập

- Tạo ZAP Context riêng cho EShop, chỉ include các URL thuộc lab như `http://localhost:3000`, `http://localhost:5173` và `http://localhost:5174`.
- Cấu hình Authentication theo cơ chế app đang dùng:
  - Nếu login bằng form/session cookie: khai báo login URL, username field, password field và POST data.
  - Nếu login trả JWT/token: tạo script hoặc thủ tục lấy token rồi gắn vào header `Authorization: Bearer <token>`.
- Cấu hình Logged-in Indicator và Logged-out Indicator để ZAP biết request còn đang authenticated hay đã rớt session. Ví dụ: response có `Logout`, `Profile`, `user`, hoặc không còn redirect về `/login`.
- Tạo User trong Context với tài khoản test riêng, ví dụ `student_test@example.com`, không dùng tài khoản thật hoặc tài khoản admin nếu chưa cần.
- Bật Forced User Mode khi spider/active scan để ZAP luôn gửi request dưới danh tính user đã đăng nhập.
- Với frontend SPA, chạy AJAX Spider sau khi auth để ZAP thấy các route và API được gọi sau đăng nhập.
- Lưu evidence cấu hình gồm screenshot Context/Auth/User, request login thành công, cookie/token, và danh sách endpoint sau đăng nhập mà ZAP đã crawl được.

Ví dụ hướng cấu hình cần hỗ trợ trong script:

```text
--context-file src/zap/context/eshop.context
--user student_test@example.com
--forced-user
--ajax-spider
```

### 5. Tạo bước đối chiếu chéo

- Tạo script hoặc tài liệu trong `src/combine` để map findings từ Semgrep với alert từ ZAP.
- Tiêu chí đối chiếu gồm loại lỗi, endpoint/runtime behavior, file nguồn, PoC và evidence.
- Kết luận mỗi finding theo trạng thái:

```text
Confirmed | False Positive | Needs Manual Verification | Environment Noise
```

### 6. Bổ sung kiểm chứng thủ công

- Với hardcoded JWT secret: kiểm tra secret có ảnh hưởng đến signing/verification token không.
- Với HTTP request không mã hóa: kiểm tra app mobile/frontend có dùng HTTP trong môi trường production không.
- Với ZAP findings: reproduce bằng request/response thật, screenshot hoặc log.
- Với endpoint yêu cầu đăng nhập: xác nhận ZAP request có cookie/token hợp lệ và không bị redirect về trang login.

### 7. Hoàn thiện báo cáo tổng hợp

- Báo cáo cuối nên có: tổng quan risk, bảng findings, PoC, evidence, fix suggestion, human validation và trạng thái sau khi vá.
- Gắn link đến input/output gốc: `sg_rs.json`, ZAP HTML report, AI triage markdown và screenshot/log kiểm chứng.
- Ghi rõ giới hạn: AI chỉ hỗ trợ triage và draft; kết luận cuối cùng dựa trên kiểm chứng của nhóm.

## Thứ tự ưu tiên đề xuất

1. Sửa test ZAP AI triage để có baseline xanh.
2. Mở rộng Semgrep triage để xử lý toàn bộ findings.
3. Chuẩn hóa thư mục output và tên file.
4. Bổ sung ZAP authenticated scan bằng Context, User và Forced User Mode.
5. Tạo combined report trong `src/combine`.
6. Chạy lại Semgrep, ZAP, AI triage và cập nhật evidence cho submission.
