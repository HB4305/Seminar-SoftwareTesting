# Dàn Ý Slide Seminar

> Mục tiêu: dựng deck seminar theo mạch workflow thực tế của nhóm trên EShop. Slide 1-3 đã có nội dung mở đầu; các slide sau bám theo `submission/User_Guide.md`. Các phần dài như cài đặt, setup, scan, AI triage và testcase được tách slide riêng để tránh nhồi chữ.

## Cấu Trúc Tổng Thể

| Slide | Trạng thái | Tiêu đề đề xuất | Mục tiêu thuyết trình | Evidence / nội dung cần chèn |
| --- | --- | --- | --- | --- |
| 1 | Đã làm | Seminar: Security Testing with DAST + SAST | Mở đầu seminar, nêu đề tài, nhóm, bộ công cụ chính. | Title centered, badge nhóm 06, tags `Semgrep`, `OWASP ZAP`, `OpenAI / Gemini`, `DAST + SAST`. |
| 2 | Đã làm | Giảng viên & Thành viên nhóm | Giới thiệu mentor và các thành viên trước khi vào nội dung kỹ thuật. | Danh sách mentor, thành viên, MSSV. |
| 3 | Đã làm | Security Testing Workflow | Nói sơ quy trình tổng thể: scan source, scan runtime, AI triage, kiểm chứng và báo cáo. | Ảnh chính `submission/slide/image/workflow-diagram.png`. |
| 4 | Đã làm | OWASP Top 10 làm khung rủi ro | Đặt nền tảng phân loại lỗi theo OWASP Top 10 để người nghe hiểu ruleset và scan policy. | Đủ A01-A10 theo `User_Guide.md`. |
| 5 | Đã làm | SAST & Semgrep trong workflow | Giải thích SAST là phân tích mã nguồn/config khi chưa cần chạy app và vì sao Semgrep phù hợp với EShop. | Định nghĩa SAST, Semgrep CLI, rule pattern, ruleset `p/owasp-top-ten`. |
| 6 | Đã làm | Cài đặt Semgrep | Cho người nghe thấy Semgrep CLI và Python triage dependency cần được cài trước khi scan. | `.venv`, `src/semgrep/requirements.txt`, `python3 -m pip install semgrep`, `brew install semgrep`, `semgrep --version`. |
| 7 | Đã làm | Chuẩn bị Semgrep: source root và môi trường | Tách phần source root/setup khỏi slide scan để người nghe thấy điều kiện chạy đúng. | `./eshop-sut`, `SOURCE_ROOT`, exclude `node_modules/dist/build/.next`. |
| 8 | Đã làm | Semgrep Scan: lệnh chính và output gốc | Trình bày lệnh scan bắt buộc theo đề T09 và file JSON evidence ban đầu. | `semgrep scan --config "p/owasp-top-ten" ... -o src/semgrep/output/semgrep_results.json ./eshop-sut`. |
| 9 | Đã làm | Semgrep Scan mở rộng theo công nghệ | Nói ngắn về scan bổ sung để tăng coverage nhưng không thay thế flow OWASP Top 10. | `p/nodejs`, `p/javascript`, `p/react`, `src/semgrep/rules/eshop-security.yml`, output `semgrep_results_extended.json`. |
| 10 | Đã làm | AI Provider cho Semgrep Triage | Làm rõ cấu hình AI, API key và chế độ offline để tránh hiểu nhầm report là tự sinh magic. | `src/semgrep/.env`, `AI_PROVIDER`, `AI_MODEL`, `OPENROUTER_API_KEY`, `AI_MAX_TOKENS`, `--offline`. |
| 11 | Đã làm | Semgrep AI Triage: từ JSON sang report | Giải thích script của nhóm biến finding thô thành báo cáo có source context, phân loại và testcase. | `semgrep_results.json -> semgrep_ai_triage.py -> semgrep_triage_report.md + semgrep_test_cases.md + findings/`. |
| 12 | Đã làm | Đọc Semgrep Report đúng cách | Nhấn mạnh tester phải kiểm chứng lại AI và phân biệt code thật với dependency/build output. | 12 findings hiện có, status `True Positive / False Positive / Needs Human Review`, source evidence. |
| 13 | Đã làm | Semgrep Finding Mẫu: Hardcoded JWT Secret | Demo finding cụ thể để người nghe thấy SAST bắt lỗi từ code như thế nào. | Rule `javascript.jsonwebtoken.security.jwt-hardcode.hardcoded-jwt-secret`, file `backend/server.js`, CWE-798, OWASP A07. |
| 14 | Đã làm | Kiểm chứng PoC từ Semgrep | Chứng minh finding không dừng ở report: tester phải tái lập bằng request/runtime. | `TC-SEMGREP-001`, PoC `exploit.js`, request `GET /api/users/me` với forged JWT. |
| 15 | Đã làm | DAST & OWASP ZAP trong workflow | Giải thích DAST là scan ứng dụng đang chạy và evidence đến từ request/response runtime. | Backend `3000`, frontend user `5173`, frontend admin `5174`, ZAP GUI hoặc CLI. |
| 16 | Đã làm | Cài đặt OWASP ZAP | Cho người nghe thấy ZAP có hai phần: GUI để thao tác thủ công và daemon/Python client cho CLI flow. | Java 17+, `winget`, `brew --cask`, `flatpak`, `python-owasp-zap-v2.4`, Docker daemon `localhost:8090`. |
| 17 | Đã làm | Chuẩn bị ZAP: env, daemon và scope | Tách cấu hình ZAP khỏi phần scan vì có nhiều điều kiện môi trường dễ lỗi. | `src/zap/.env`, `ZAP_TARGET`, `ZAP_URL`, `ZAP_MAX_URLS`, user `test@eshop.com / Test1234!`, admin `admin@eshop.com / Admin123!`. |
| 18 | Đã làm | ZAP GUI Flow: public và authenticated | Tóm tắt cách dùng GUI để proxy browser, login, tạo context và lấy evidence thủ công. | Quick Start Automated Scan, Firefox proxy `localhost:8080`, context auth, `POST /api/login`, Forced User Mode. |
| 19 | Đã làm | ZAP CLI Flow: public scan | Trình bày scan tự động cho endpoint public và lý do xuất JSON để pipeline xử lý. | `scan_zap.py --target http://localhost:3000 --report-format json --output-file src/zap/output/backend_basic.json`; frontend public với `--ajax-spider`. |
| 20 | Đã làm | ZAP CLI Flow: authenticated scan | Tách authenticated scan thành slide riêng vì có role, forced user và giới hạn URL cho SPA. | User/admin commands, `--auth-role user/admin`, `--forced-user`, `--ajax-spider`, `--max-urls`, lỗi `401/403`. |
| 21 | Đã làm | Đọc ZAP Output và quản lý scope | Nhấn mạnh report chỉ có giá trị khi đúng target, đúng session và không bị lẫn dữ liệu. | `backend_basic.json`, `frontend_user_basic.json`, `frontend_admin_basic.json`; kiểm tra alert thuộc EShop, public/auth, local HTTP noise. |
| 22 | Đã làm | ZAP AI Triage: gom nhóm alert runtime | Giải thích script đọc nhiều JSON report, lọc target prefix và sinh Markdown/testcase theo endpoint. | `zap_ai_triage.py`, `--target-prefix`, output `zap_triage_report.md`, `zap_test_cases.md`, `alerts/*_prompt.md`, `alerts/*_ai_output.md`. |
| 23 | Đã làm | ZAP Alert Mẫu: CSP Misconfiguration | Demo một alert runtime có evidence từ response header và testcase replay. | Alert `CSP: Failure to Define Directive with No Fallback`, evidence `Content-Security-Policy: default-src 'none'`. |
| 24 | Đã làm | Ranh giới trách nhiệm sau khi có finding | Làm rõ tool và AI không thay thế tester/developer/SOC; mỗi bên có output khác nhau. | Bảng 3 vai trò: Tester chứng minh lỗi, Developer sửa và test chống tái diễn, SOC theo dõi production. |
| 25 | Đã làm | Troubleshooting thường gặp | Gom các failure modes từ User Guide để chuẩn bị trả lời khi demo lỗi hoặc môi trường khác. | `.venv`, sai `SOURCE_ROOT`, OpenRouter `402`, ZAP daemon/Docker, auth `401/403`, report lẫn target. |
| 26 | Đã làm | Kết luận | Chốt seminar bằng một quote chính: tool tạo evidence, tester chịu trách nhiệm kiểm chứng. | Quote conclusion, SAST + DAST + AI triage, evidence before conclusion. |
| 27 | Đã làm | Cảm ơn và Q&A | Kết thúc phần trình bày và chuyển sang nhận câu hỏi. | Cảm ơn mọi người đã theo dõi, Nhóm 06 / KDBK, Q&A. |

## Mạch Kể Chuyện Khi Thuyết Trình

1. **Mở bài bằng bối cảnh nhóm**: slide 1-2 nói nhanh, tạo context seminar.
2. **Đưa workflow lên trước**: slide 3 cho người nghe thấy toàn bộ pipeline trước khi vào từng tool.
3. **Đặt khung rủi ro**: slide 4 dùng OWASP Top 10 để giải thích cách nhóm chọn ruleset/policy.
4. **Đi theo nhánh Semgrep**: slide 5-14 đi từ khái niệm SAST, cài đặt, setup, scan, AI triage, đọc report, finding mẫu và PoC.
5. **Đi theo nhánh ZAP**: slide 15-23 đi từ khái niệm DAST, cài đặt, setup, GUI, CLI public/auth, scope output, AI triage và testcase mẫu.
6. **Chốt bằng trách nhiệm và giới hạn**: slide 24-26 nhấn mạnh alert không tự động là lỗi đã xác nhận, nêu troubleshooting và Q&A.

## Ghi Chú Nội Dung Từng Slide

### Slide 1 - Seminar: Security Testing with DAST + SAST

- Nói trong 20-30 giây.
- Thông điệp chính: seminar trình bày workflow kiểm thử bảo mật cho EShop bằng Semgrep, OWASP ZAP và AI triage.

### Slide 2 - Giảng viên & Thành viên nhóm

- Nói trong 20-30 giây.
- Không cần thêm nội dung kỹ thuật.

### Slide 3 - Security Testing Workflow

- Dùng ảnh `submission/slide/image/workflow-diagram.png` làm nội dung chính.
- Lời dẫn ngắn: workflow có hai nguồn evidence, source code từ Semgrep và runtime request/response từ ZAP; cả hai đi qua bước AI triage nhưng kết luận cuối vẫn cần tester kiểm chứng.

### Slide 4 - OWASP Top 10 làm khung rủi ro

- OWASP Top 10 là khung nhóm rủi ro, không phải checklist tự động hoàn chỉnh.
- Nhóm dùng OWASP Top 10 để chọn ruleset Semgrep và scan policy ZAP.
- Slide cần đủ A01-A10 theo `submission/User_Guide.md`.

### Slide 5 - SAST & Semgrep trong workflow

- SAST phân tích mã nguồn hoặc cấu hình mà không cần chạy ứng dụng.
- Semgrep dùng rule pattern để phát hiện hardcoded secret, HTTP không mã hóa, injection pattern hoặc lỗi framework phổ biến.
- Trong flow nhóm, Semgrep tạo evidence ban đầu cho nhánh source-code scan.

### Slide 6 - Cài đặt Semgrep

- Chạy từ root repo `Seminar-SoftwareTesting`.
- Tạo `.venv`, activate và cài `src/semgrep/requirements.txt` cho script triage.
- Cài Semgrep CLI theo hệ điều hành: Linux/Windows dùng `pip`, macOS dùng `brew`.
- Chạy `semgrep --version` để xác nhận tool đã sẵn sàng.

### Slide 7 - Chuẩn bị Semgrep: source root và môi trường

- Source mặc định là `./eshop-sut`; nếu khác vị trí, đặt `SOURCE_ROOT`.
- Không quét dependency/build output: `node_modules`, `dist`, `build`, `.next`.
- Thông điệp chính: sai source root hoặc quét nhầm dependency sẽ làm report nhiễu.

### Slide 8 - Semgrep Scan: lệnh chính và output gốc

```bash
semgrep scan --config "p/owasp-top-ten" --exclude node_modules --exclude dist --exclude build --exclude .next --json -o src/semgrep/output/semgrep_results.json ./eshop-sut
```

- Output gốc `semgrep_results.json` phải được giữ lại làm evidence scan.
- Khi đọc terminal output, chú ý file, line, rule ID, severity, message, CWE/OWASP nếu có.

### Slide 9 - Semgrep Scan mở rộng theo công nghệ

- Sau scan bắt buộc bằng `p/owasp-top-ten`, có thể scan thêm theo công nghệ EShop.
- Ruleset bổ sung: `p/nodejs`, `p/javascript`, `p/react`, custom rule `src/semgrep/rules/eshop-security.yml`.
- Output đề xuất: `src/semgrep/output/semgrep_results_extended.json`.

### Slide 10 - AI Provider cho Semgrep Triage

- Cấu hình AI nằm trong `src/semgrep/.env`.
- Không commit `.env` thật vì chứa API key.
- Nếu hết credit/token, giảm `AI_MAX_TOKENS` hoặc chạy `--offline`.

### Slide 11 - Semgrep AI Triage: từ JSON sang report

- Script `src/semgrep/semgrep_ai_triage.py` đọc JSON, lấy thêm source context từ `--source-root`, rồi sinh report.
- Ba trạng thái phân loại: `True Positive`, `False Positive`, `Needs Human Review`.
- Output chính: `semgrep_triage_report.md`, `semgrep_test_cases.md`, `findings/`.

### Slide 12 - Đọc Semgrep Report đúng cách

- Report hiện có ghi nhận 12 findings.
- Khi đọc report, kiểm tra finding có nằm trong code tự viết hay dependency/build output.
- Kết luận cuối cùng cần được tester xác nhận, không chỉ dựa vào nhãn AI.

### Slide 13 - Semgrep Finding Mẫu: Hardcoded JWT Secret

- Finding mẫu từ User Guide: hardcoded JWT secret trong `backend/server.js`.
- Rule ID: `javascript.jsonwebtoken.security.jwt-hardcode.hardcoded-jwt-secret`.
- CWE: CWE-798.
- OWASP: A07 Authentication Failures.

### Slide 14 - Kiểm chứng PoC từ Semgrep

- Testcase mẫu: `TC-SEMGREP-001`.
- Request kiểm chứng dùng `GET http://localhost:3000/api/users/me` với `Authorization: Bearer <forged_token>`.
- Nếu backend trả `200 OK`, finding được xác nhận runtime; nếu `401/403`, ghi nhận không tái lập được hoặc đã bị chặn.

### Slide 15 - DAST & OWASP ZAP trong workflow

- DAST kiểm thử ứng dụng đang chạy thật, không đọc source code.
- ZAP gửi request HTTP, crawl trang, passive scan và có thể active scan bằng payload kiểm thử.
- Target demo: backend `http://localhost:3000`, frontend user `http://localhost:5173`, frontend admin `http://localhost:5174`.

### Slide 16 - Cài đặt OWASP ZAP

- ZAP GUI cần Java 17+ nếu bản cài không bundle Java.
- Windows dùng `winget install --id=ZAP.ZAP -e`.
- macOS dùng `brew install --cask zap`.
- Linux có thể dùng Flatpak, Snap hoặc package từ trang chủ ZAP.
- CLI flow cần Python package `python-owasp-zap-v2.4` và ZAP daemon tại `http://localhost:8090`.

### Slide 17 - Chuẩn bị ZAP: env, daemon và scope

- Cấu hình trong `src/zap/.env`: `ZAP_TARGET`, `ZAP_URL`, `ZAP_AUTH_ROLE`, `ZAP_MAX_URLS`, `ZAP_REPORT_FORMAT`, `ZAP_REPORT_FILE`.
- Nếu scan auth, điền credential test: user `test@eshop.com / Test1234!`, admin `admin@eshop.com / Admin123!`.
- Không commit `.env` thật.

### Slide 18 - ZAP GUI Flow: public và authenticated

- Public GUI scan: Quick Start -> Automated Scan -> nhập target -> Attack.
- Với frontend SPA, dùng thêm Manual Explore hoặc AJAX Spider.
- Authenticated GUI scan: login qua browser, flag request `POST /api/login`, tạo context, tạo user, bật Forced User Mode.

### Slide 19 - ZAP CLI Flow: public scan

```bash
python src/zap/scan_zap.py --target http://localhost:3000 --report-format json --output-file src/zap/output/backend_basic.json
```

- Frontend public scan nên thêm `--ajax-spider`.
- Nếu chỉ đọc thủ công, dùng `--report-format html`; nếu đưa vào AI triage, dùng JSON.

### Slide 20 - ZAP CLI Flow: authenticated scan

```bash
python src/zap/scan_zap.py --target http://localhost:5173 --auth-role user --forced-user --ajax-spider --report-format json --output-file src/zap/output/frontend_user_basic.json
```

- Admin tương tự với target `http://localhost:5174` và `--auth-role admin`.
- Nếu log báo crawl vượt `--max-urls`, giữ spider/passive evidence và ưu tiên active scan backend/API.

### Slide 21 - Đọc ZAP Output và quản lý scope

- Output chính: `backend_basic.json`, `frontend_user_basic.json`, `frontend_admin_basic.json`.
- Khi đọc report, kiểm tra alert thuộc đúng target và scope EShop.
- Nếu report backend lẫn frontend, tạo session mới/clear history hoặc dùng output riêng cho từng target.

### Slide 22 - ZAP AI Triage: gom nhóm alert runtime

- Script `src/zap/zap_ai_triage.py` đọc một hoặc nhiều ZAP JSON report.
- Dùng `--target-prefix` nhiều lần để lọc đúng scope.
- Output chính: `zap_triage_report.md`, `zap_test_cases.md`, `alerts/*_prompt.md`, `alerts/*_ai_output.md`.

### Slide 23 - ZAP Alert Mẫu: CSP Misconfiguration

- Alert: `CSP: Failure to Define Directive with No Fallback`.
- Evidence đại diện: `Content-Security-Policy: default-src 'none'`.
- Testcase replay request để kiểm tra response hiện tại còn CSP evidence tương tự hay không.

### Slide 24 - Ranh giới trách nhiệm sau khi có finding

- Tester chạy tool, triage, tái hiện lỗi, phân loại trạng thái và bàn giao evidence.
- Developer đọc report, xác định root cause trong code/config, sửa lỗi, bổ sung test chống tái diễn.
- SOC theo dõi production, phát hiện dấu hiệu khai thác qua log/alert và xử lý incident.

### Slide 25 - Troubleshooting thường gặp

- Không cài được package Python global: dùng `.venv` thay vì system Python.
- Semgrep không tìm thấy source: kiểm tra `./eshop-sut` hoặc đặt lại `SOURCE_ROOT`.
- OpenRouter trả `402`: hết credit hoặc request quá tốn token; giảm token, đổi model hoặc chạy `--offline`.
- ZAP không khởi động: kiểm tra Docker daemon, image ZAP hoặc chạy GUI/daemon thủ công tại `localhost:8090`.
- Authenticated ZAP scan lỗi `401/403`: kiểm tra credential, `/api/login`, `/api/users/me`, backend `3000`.
- Report backend lẫn frontend: clear ZAP session/history hoặc tách output theo target.

### Slide 26 - Kết luận

- Main content dạng quote: "Evidence đến từ tool, nhưng kết luận phải đến từ kiểm chứng."
- SAST chỉ ra rủi ro trong source code.
- DAST xác nhận hành vi runtime.
- AI giúp tăng tốc đọc report, nhưng tester vẫn chịu trách nhiệm xác nhận bằng evidence.

### Slide 27 - Cảm ơn và Q&A

- Cảm ơn mọi người đã theo dõi.
- Hiển thị thông tin nhóm: Nhóm 06 / KDBK.
- Dừng ở phần Q&A để nhận câu hỏi.

## Checklist Khi Dựng Slide

- Mỗi slide chỉ nên có 1 thông điệp chính.
- Với các section dài trong `User_Guide.md`, ưu tiên chia thành slide nhỏ thay vì giảm font hoặc nhồi bullet.
- Cài đặt Semgrep và ZAP phải xuất hiện trước các slide scan tương ứng.
- Ưu tiên ảnh chụp report, terminal hoặc file output thật thay vì copy quá nhiều command.
- Command dài chỉ để trong speaker notes hoặc code block nhỏ.
- Các slide demo nên có đường dẫn file evidence rõ ràng.
