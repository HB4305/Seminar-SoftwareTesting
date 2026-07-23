# [AI-03] Công Bố Sử Dụng AI

## Tuyên bố chung

Nhóm 06 - KDBK sử dụng AI trong seminar **T09 - Security Testing (DAST / SAST)** với vai trò hỗ trợ học tập, soạn thảo, rà soát kỹ thuật, phân tích kết quả scan và chuẩn hóa tài liệu. AI không được xem là nguồn kết luận cuối cùng. Mọi nội dung đưa vào sản phẩm nộp bài đều đã được thành viên phụ trách đọc lại, chỉnh sửa, đối chiếu với source code, output công cụ, tài liệu chính thức hoặc bằng chứng trong repository.

Nhóm không nộp nguyên văn output AI khi chưa kiểm chứng. Các phần liên quan đến lỗ hổng bảo mật, PoC, remediation, ZAP/Semgrep report và AI triage đều cần được human validation trước khi dùng làm bằng chứng chính thức.

## Thành viên 1 - Lê Trung Kiên

- MSSV: 23127075
- Nhóm: Group 06 - KDBK
- Đề tài: T09 - Security Testing (DAST / SAST)

### Tóm tắt sử dụng AI

| Công cụ | Mục đích | Đầu vào đã cung cấp | Nội dung đã sử dụng | Cách tự kiểm chứng |
| --- | --- | --- | --- | --- |
| ChatGPT GPT-5.5 | Hỗ trợ viết script đọc output OWASP ZAP và tạo báo cáo AI triage. | ZAP report, yêu cầu parse alert, impact, PoC, fix và output Markdown. | Draft logic xử lý ZAP report, draft prompt triage alert, một phần nội dung mô tả trong output triage mẫu. | Chỉnh sửa script để gọi API qua OpenRouter, kiểm tra luồng đọc input/xuất Markdown, đối chiếu nội dung triage với evidence từ ZAP report. |
| Codex GPT-5.4/GPT-5.5 | Hỗ trợ mở rộng CLI ZAP. | Yêu cầu thêm `--scan-mode`, `--report-format`, `--output-file`, hỗ trợ JSON report và cập nhật README. | Bản nháp parser CLI, gợi ý dùng ZAP Report Generation add-on, ví dụ command cho backend/frontend. | Đọc lại `scan_zap.py`, chỉ giữ format `html`/`json`, đối chiếu tài liệu official của ZAP, chạy unit/parser test và kiểm tra README. |

### Xác nhận

Tôi xác nhận các nội dung AI hỗ trợ đã được tôi đọc lại, chỉnh sửa và kiểm chứng trước khi đưa vào tài liệu nhóm.

- Ngày: 21/07/2026
- Chữ ký:

## Thành viên 2 - Mai Thị Kim Duyên

- MSSV: 23127185
- Nhóm: Group 06 - KDBK
- Đề tài: T09 - Security Testing (DAST / SAST)

### Tóm tắt sử dụng AI

| Công cụ | Mục đích | Đầu vào đã cung cấp | Nội dung đã sử dụng | Cách tự kiểm chứng |
| --- | --- | --- | --- | --- |
| Gemini 3.1 Pro | Hỗ trợ viết mã Python gọi API OWASP ZAP và biên tập báo cáo OWASP Top 10. | Yêu cầu tự động hóa Spider, Active Scan, lấy alerts và chuẩn hóa nội dung báo cáo. | Bản nháp mã dùng thư viện `zaproxy`, logic gọi endpoint scan, xử lý danh sách alerts, bản nháp nội dung OWASP Top 10. | Kiểm tra lại nội dung OWASP ZAP, chạy thử script qua API, rà soát kết quả trả về. |
| Gemini 3.1 Pro | Hỗ trợ cấu hình authenticated scan cho ZAP trên EShop. | Yêu cầu đăng nhập lấy JWT, tạo context/user/forced-user, gắn `Authorization: Bearer ...`, dùng AJAX Spider và giới hạn local scope. | Bản nháp logic đăng nhập qua proxy ZAP, trích xuất JWT, tạo context/user, bật Forced User Mode, thêm Replacer rule, gợi ý AJAX Spider. | Đọc lại `zap_runtime.py`, sửa credential mặc định, validate chỉ scan local EShop, đối chiếu tài liệu official của ZAP về authentication, users, Replacer và AJAX Spider. |

### Xác nhận

Tôi xác nhận các nội dung AI hỗ trợ đã được tôi đọc lại, chỉnh sửa và kiểm chứng trước khi đưa vào tài liệu nhóm.

- Ngày: 21/07/2026
- Chữ ký:

## Thành viên 3 - Lâm Hữu Khánh

- MSSV: 23127205
- Nhóm: Group 06 - KDBK
- Đề tài: T09 - Security Testing (DAST / SAST)

### Tóm tắt sử dụng AI

| Công cụ | Mục đích | Đầu vào đã cung cấp | Nội dung đã sử dụng | Cách tự kiểm chứng |
| --- | --- | --- | --- | --- |
| ChatGPT/Gemini | Hỗ trợ rà soát Semgrep SAST và finding `hardcoded-jwt-secret`. | Semgrep finding, source evidence, yêu cầu giải thích nguy cơ, PoC JWT giả mạo và remediation. | Nhận xét root cause `SECRET_KEY` hardcode, phân tích impact, draft PoC dùng `jsonwebtoken`, checklist kiểm chứng rule ID/file/dòng code, gợi ý dùng `process.env.JWT_SECRET`. | Đối chiếu output Semgrep với evidence, kiểm tra các vị trí `jwt.sign` và `jwt.verify`, rà soát PoC, gộp duplicate findings cùng root cause. |
| Codex GPT-5 | Hỗ trợ soạn README chạy basic scan bằng ZAP. | Yêu cầu giải thích CLI flags `--target`, `--scan-mode`, `--report-format`, `--output-file` và ví dụ lệnh HTML/JSON. | Dự thảo cấu trúc mục "Chạy scan", giải thích tham số CLI, ví dụ command chạy từ root project. | Đối chiếu cờ CLI với `scan_zap.py`, chỉnh đường dẫn theo repo, chạy thử basic scan local và kiểm tra file output. |

### Xác nhận

Tôi xác nhận các nội dung AI hỗ trợ đã được tôi đọc lại, chỉnh sửa và kiểm chứng trước khi đưa vào tài liệu nhóm.

- Ngày: 21/07/2026
- Chữ ký:

## Thành viên 4 - Lê Mai Hoài Bảo

- MSSV: 23127326
- Nhóm: Group 06 - KDBK
- Đề tài: T09 - Security Testing (DAST / SAST)

### Tóm tắt sử dụng AI

| Công cụ | Mục đích | Đầu vào đã cung cấp | Nội dung đã sử dụng | Cách tự kiểm chứng |
| --- | --- | --- | --- | --- |
| Google Gemini 3.1 Flash | Hỗ trợ sửa script Semgrep AI triage và phân tích finding `hardcoded-jwt-secret`. | Yêu cầu chuyển từ `google-generativeai` sang `google-genai`, xử lý lỗi model/503, phân tích finding và điền template Track A. | Bản nháp mã gọi Gemini bằng `genai.Client`, retry khi API quá tải, báo cáo triage hardcoded JWT secret gồm giải thích, PoC, impact và remediation. | Cài `google-genai`, chạy lại script với `semgrep_results.json`, xác nhận xuất Markdown, đối chiếu rule ID/vị trí finding với `backend/server.js`, kiểm tra PoC JWT và remediation. |
| Codex/ChatGPT, OpenRouter Gemini `google/gemini-2.5-flash-lite` | Hỗ trợ hoàn thiện Semgrep AI Triage workflow. | Yêu cầu đọc tài liệu Semgrep, cấu hình OpenRouter, sửa env/script, giải thích lỗi `externally-managed-environment`, lỗi OpenRouter `402`, xử lý toàn bộ findings, sắp xếp lại repo. | Đề xuất `.env.example`, logic đọc `OPENROUTER_API_KEY`/`OPENROUTER_BASE_URL`, xử lý toàn bộ `results`, pipeline `run_semgrep_pipeline.sh`, hướng dẫn chạy và unit test liên quan. | Kiểm tra cấu trúc `docs/semgrep` và `src/semgrep`, chạy cài đặt trong `.venv`, scan Semgrep, chạy triage, xác nhận 12 findings được xử lý, kiểm tra lỗi `402` là do credit/token limit, chạy unit test và kiểm tra diff. |

### Xác nhận

Tôi xác nhận các nội dung AI hỗ trợ đã được tôi đọc lại, chỉnh sửa và kiểm chứng trước khi đưa vào tài liệu nhóm.

- Ngày: 21/07/2026
- Chữ ký:

## Cam kết của nhóm

Nhóm cam kết:

- Không sử dụng AI để thay thế việc hiểu công cụ, chạy kiểm thử hoặc xác minh kỹ thuật.
- Không đưa API key, `.env` thật, credential nhạy cảm hoặc scan target không được phép vào prompt.
- Không kết luận lỗ hổng chỉ dựa trên AI; mọi kết luận cần source evidence, output Semgrep/ZAP, PoC hoặc human validation.
- Ghi nhận rõ các giới hạn của AI, gồm placeholder, duplicate findings, sai taxonomy/tag OWASP, hoặc output thiếu precondition/expected result.
