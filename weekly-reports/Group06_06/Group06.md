# Weekly Report - W06

## 1. Thông tin chung

- ID Nhóm: **06**
- Tên nhóm: **KDBK**
- Tên project: **T09 - Security Testing (DAST / SAST)**
- Thời gian làm: 2026-07-12 - 2026-07-18

## 2. Nhiệm vụ đã hoàn thành tuần này

### 2.1. Bảng nhiệm vụ

| **Nhiệm vụ** | **Họ tên** |
| :--- | :--- |
| Hoàn thiện cấu hình chạy Semgrep AI Triage bằng OpenRouter với model Gemini. | Lê Mai Hoài Bảo |
| Sửa script AI Triage để xử lý toàn bộ findings theo số lượng lỗi trong file JSON, không hardcode một lỗi đầu tiên. | Lê Mai Hoài Bảo |
| Sắp xếp lại cấu trúc Track Semgrep: tài liệu để trong `docs/semgrep/`, script/pipeline/runtime để trong `src/semgrep/`. | Lê Mai Hoài Bảo |
| Bổ sung pipeline chạy từ root, output Semgrep và AI Triage vào `src/semgrep/output/`. | Lê Mai Hoài Bảo |
| Kiểm thử lại script, pipeline và luồng offline triage để xác nhận xử lý đủ 12 findings từ Semgrep. | Lê Mai Hoài Bảo |

### 2.2. Minh chứng

### 2.2.1. Các file/script liên quan

- `src/semgrep/.env.example`: cấu hình mẫu cho OpenRouter dùng model Gemini.
- `src/semgrep/semgrep_ai_triage.py`: script đọc kết quả Semgrep JSON và gửi từng finding sang AI để triage.
- `src/semgrep/test_semgrep_ai_triage.py`: unit test cho cấu hình OpenRouter và luồng xử lý findings.
- `src/semgrep/run_semgrep_pipeline.sh`: pipeline chạy Semgrep scan và AI triage từ root project.
- `src/semgrep/requirements.txt`: dependency Python cho Track Semgrep.
- `src/semgrep/exploit.js`: PoC minh họa khai thác hardcoded JWT secret.
- `docs/semgrep/README.md`: hướng dẫn chạy Semgrep từ root, trỏ về script trong `src/semgrep/`.
- `docs/semgrep/scan.md`: cập nhật hướng dẫn dùng script trong `src/semgrep/` thay vì đặt code trong `docs`.

### 2.2.2. Kết quả kiểm thử/verification

- Chạy unit test:
  ```bash
  python3 -m unittest src/semgrep/test_semgrep_ai_triage.py
  ```
  Kết quả: `Ran 4 tests ... OK`.

- Kiểm tra cú pháp pipeline:
  ```bash
  bash -n src/semgrep/run_semgrep_pipeline.sh
  ```
  Kết quả: không có lỗi cú pháp.

- Chạy offline triage trên file Semgrep JSON mẫu:
  ```bash
  python3 src/semgrep/semgrep_ai_triage.py src/semgrep/sg_rs.json --offline --output-dir /private/tmp/semgrep-output-check-2
  ```
  Kết quả: script đọc và xử lý đủ **12 findings**, tạo report tổng hợp `semgrep_triage_report.md`.

- Kiểm tra lỗi whitespace trong diff:
  ```bash
  git diff --check
  ```
  Kết quả: không phát hiện lỗi whitespace.

### 2.3. Nội dung Lê Mai Hoài Bảo đã thực hiện

- Đọc lại tài liệu Semgrep hiện có trong `docs/semgrep/` để xác định luồng chạy đúng cho nhóm.
- Cấu hình lại `.env.example` để dùng OpenRouter thay vì gọi Gemini trực tiếp, với model Gemini qua endpoint OpenAI-compatible.
- Sửa script để đọc `OPENROUTER_API_KEY` và `OPENROUTER_BASE_URL`, đồng thời giữ fallback `OPENAI_API_KEY`/`OPENAI_BASE_URL` cho cấu hình cũ.
- Điều tra lỗi khi chạy `pip install` trong môi trường Python bị quản lý bởi Homebrew/Conda (`externally-managed-environment`) và chuyển sang dùng `.venv`.
- Điều tra lỗi OpenRouter `402` do request có giới hạn token quá cao so với credit hiện có, sau đó đổi hướng dùng model nhẹ hơn `google/gemini-2.5-flash-lite`.
- Phát hiện script cũ chỉ gửi một lỗi đầu tiên vì hardcode `findings[0]`; sửa logic để lặp qua toàn bộ `results` trong file Semgrep JSON.
- Điều chỉnh output để mỗi finding có prompt/AI output riêng và report tổng hợp, tránh ghi đè kết quả.
- Sắp xếp lại ranh giới thư mục: tài liệu trong `docs/semgrep/`, code/script/pipeline/output trong `src/semgrep/`.
- Viết lại hướng dẫn chạy từ root trong `docs/semgrep/README.md`.
- Kiểm thử lại bằng unit test, kiểm tra shell script và chạy offline triage với 12 findings.

## 3. Khai báo sử dụng AI

### 3.1. Lê Trung Kiên

- Chưa cập nhật trong tuần này.

### 3.2. Mai Thị Kim Duyên

- Chưa cập nhật trong tuần này.

### 3.3. Lâm Hữu Khánh

- Chưa cập nhật trong tuần này.

### 3.4. Lê Mai Hoài Bảo

- Công cụ: Codex/ChatGPT, OpenRouter, model Gemini qua OpenRouter (`google/gemini-2.5-flash-lite`).
- Prompt đã sử dụng:
  - Yêu cầu AI đọc tài liệu Semgrep trong repo và hướng dẫn cách chạy Semgrep từ bước cài đặt, scan đến AI triage.
  - Yêu cầu AI sửa cấu hình `.env.example` để dùng OpenRouter với model Gemini thay vì dùng trực tiếp `GEMINI_API_KEY`.
  - Yêu cầu AI sửa script để đọc `OPENROUTER_API_KEY`/`OPENROUTER_BASE_URL`.
  - Yêu cầu AI giải thích lỗi `externally-managed-environment` khi cài package Python và hướng dẫn chuyển sang virtual environment.
  - Yêu cầu AI giải thích lỗi OpenRouter `402` và đề xuất model/token phù hợp hơn.
  - Yêu cầu AI sửa script để chạy tất cả findings theo số lượng lỗi trong JSON, không hardcode một lỗi.
  - Yêu cầu AI sắp xếp lại repo: tài liệu ở `docs/semgrep/`, script/pipeline/runtime ở `src/semgrep/`, đồng thời viết hướng dẫn chạy từ root.
- Mục đích sử dụng: Hỗ trợ hoàn thiện workflow Semgrep AI Triage cho dự án EShop, chuẩn hóa cấu hình OpenRouter, sửa lỗi runtime, tự động hóa xử lý nhiều findings và làm rõ cấu trúc tài liệu/script trong repo.
- Nội dung AI tạo ra:
  - Đề xuất cấu hình `.env.example` dùng OpenRouter với model Gemini.
  - Bản sửa logic đọc API key/base URL từ `OPENROUTER_API_KEY` và `OPENROUTER_BASE_URL`.
  - Bản sửa script để lặp qua toàn bộ findings trong `results` thay vì chỉ xử lý `findings[0]`.
  - Pipeline `run_semgrep_pipeline.sh` để chạy scan và AI triage từ root.
  - Hướng dẫn chạy trong `docs/semgrep/README.md`.
  - Unit test kiểm tra cấu hình OpenRouter và luồng xử lý findings.
- Nội dung tự thực hiện/kiểm chứng:
  - Kiểm tra lại cấu trúc thư mục để đảm bảo tài liệu nằm trong `docs/semgrep/`, code/script nằm trong `src/semgrep/`.
  - Tự chạy lệnh cài đặt trong `.venv`, scan Semgrep và chạy script triage.
  - Đối chiếu log Semgrep cho thấy có 12 findings và kiểm tra script xử lý đủ 12 findings trong chế độ offline.
  - Kiểm tra lỗi OpenRouter `402` không phải lỗi code mà do credit/token limit, sau đó đổi model sang bản nhẹ hơn.
  - Chạy unit test, kiểm tra cú pháp shell script và kiểm tra diff không có lỗi whitespace.

## 4. AI Audit

### 4.1. Prompt/AI output được sử dụng

AI được dùng chủ yếu để hỗ trợ lập trình và biên tập tài liệu kỹ thuật cho Track Semgrep. Các prompt tập trung vào:

- Hướng dẫn chạy Semgrep từ root project.
- Sửa cấu hình OpenRouter/Gemini.
- Sửa lỗi cài dependency Python bằng `.venv`.
- Sửa lỗi AI triage chỉ xử lý một finding.
- Tách đúng trách nhiệm giữa `docs/semgrep/` và `src/semgrep/`.
- Viết lại hướng dẫn và weekly report.

### 4.2. Điểm AI hỗ trợ đúng

- AI giúp xác định nguyên nhân script chỉ gửi một lỗi là do dòng `finding = findings[0]`.
- AI giúp đề xuất cách sửa để lặp qua toàn bộ danh sách findings.
- AI giúp giải thích lỗi `externally-managed-environment` và đưa hướng xử lý đúng bằng virtual environment thay vì dùng `--break-system-packages`.
- AI giúp phân tích lỗi OpenRouter `402` là do giới hạn credit/token, không phải lỗi API key.
- AI hỗ trợ chuẩn hóa command chạy từ root và gom output runtime vào `src/semgrep/output/`.

### 4.3. Điểm cần con người kiểm chứng/chỉnh sửa

- AI ban đầu có lúc đặt hướng dẫn tài liệu vào root `README.md`, trong khi yêu cầu đúng là tài liệu phải nằm trong `docs/semgrep/`. Con người đã kiểm tra và yêu cầu sửa lại ranh giới này.
- AI cần được nhắc rõ rằng `docs` chỉ chứa tài liệu, còn script/pipeline/code phải nằm trong `src/semgrep/`.
- Các kết quả AI triage vẫn cần được kiểm tra thủ công với source code EShop, vì AI có thể mô tả impact/PoC quá rộng nếu không đối chiếu runtime.
- Lỗi OpenRouter `402` cần được phân biệt với lỗi logic script để tránh sửa sai code.

### 4.4. Kết luận AI Audit

AI hữu ích trong việc tăng tốc sửa lỗi, viết script và chuẩn hóa hướng dẫn, nhưng kết quả chỉ đáng tin sau khi được kiểm chứng bằng lệnh chạy thật, unit test và đối chiếu với cấu trúc repo. Trong tuần này, phần do AI đề xuất đã được Lê Mai Hoài Bảo kiểm tra lại bằng các lệnh verification và chỉnh sửa theo đúng yêu cầu tổ chức file của nhóm.

## 5. Task tuần sau

| **Id** | **Task name** | **Member** |
| :---: | :--- | :--- |
| 1 | Chạy lại pipeline Semgrep với OpenRouter sau khi đảm bảo đủ credit/API quota. | Lê Mai Hoài Bảo |
| 2 | Đọc và đánh dấu từng finding trong report là `Confirmed`, `False Positive`, `Needs Manual Verification` hoặc `Environment Noise`. | Lê Mai Hoài Bảo |
| 3 | Đồng bộ evidence Semgrep đã tạo vào weekly report/submission nếu nhóm cần nộp bản cuối. | Lâm Hữu Khánh, Lê Mai Hoài Bảo |
| 4 | Cập nhật phần ZAP tương ứng nếu có thay đổi cấu trúc docs/src giống Track Semgrep. | Lê Trung Kiên, Mai Thị Kim Duyên |

## 6. Vấn đề phát sinh

- Môi trường Python global bị chặn cài package do cơ chế `externally-managed-environment`, đã xử lý bằng `.venv`.
- OpenRouter trả lỗi `402` do credit/token limit, cần dùng model nhẹ hơn hoặc bổ sung credit nếu muốn chạy toàn bộ findings bằng AI thật.
- Cần giữ rõ ranh giới repo: tài liệu trong `docs/`, script và pipeline trong `src/`.
