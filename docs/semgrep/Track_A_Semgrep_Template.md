# Pha 1 Track A: Semgrep Flow & AI Triage Template

## 1. M1 - Setup & Hello World

### Setup Notes
- **Môi trường / Hệ điều hành:** [VD: macOS / Ubuntu / Windows WSL]
- **Cách cài đặt:**
  + macos
    ```bash
    brew install semgrep
    ```
### Hello World / Quick Start
- **Lệnh chạy thử:**
  ```bash
  semgrep scan --config "p/owasp-top-ten" <đường_dẫn_đến_source_code>
  ```
- **Kết quả (Screenshot hoặc Output log):**
  ![SemgrepCode1](../../resources/semgrep_test1.png)
  ![SemgrepCode2](../../resources/semgrep_test2.png)

---

## 2. Pha 1 - Semgrep Finding Note

- **Mục tiêu scan:** [VD: EShop repo]
- **Lệnh scan thực tế:**
  ```bash
  semgrep scan --config "p/owasp-top-ten" <đường_dẫn_đến_source_code>
  ```
- **Chi tiết lỗi được chọn (The Finding):**
  - **Rule ID:** [VD: python.django.security.injection.sql-injection]
  - **Mức độ (Severity):** [VD: ERROR / WARNING]
  - **File:** [Đường dẫn file bị lỗi]
  - **Dòng code (Line):** [Số dòng]
  - **Mô tả của công cụ:** [Copy mô tả lỗi từ Semgrep]
  - **Đoạn code bị lỗi (Source evidence):**
    ```python
    # Dán đoạn code bị đánh dấu lỗi vào đây
    ```

---

## 3. Pha 1 - AI Triage Note

### Prompt sử dụng
*Hãy ghi lại câu lệnh bạn đã dùng để hỏi AI (Gemini).*
> **Prompt:** "Tôi dùng Semgrep quét source code dự án EShop và phát hiện một lỗi bảo mật. Chi tiết mã lỗi là [Rule ID], tại file [Tên file], dòng [Số dòng]. Đoạn code bị lỗi là: [Dán code]. Hãy giải thích lỗi này, viết một PoC (Proof of Concept) nháp để khai thác và gợi ý cách sửa code (fix)."

### Phản hồi của AI (Tóm tắt)
- **Giải thích lỗi:** [Tóm tắt ngắn gọn lý do AI đưa ra]
- **PoC do AI tạo:**
  ```text
  [PoC AI gợi ý]
  ```
- **Cách fix do AI tạo:**
  ```text
  [Code fix AI gợi ý]
  ```

### AI Audit (Kiểm chứng kết quả của AI)
- [ ] Lời giải thích của AI có đúng với bối cảnh dự án không? (Có/Không - Giải thích ngắn)
- [ ] PoC có thực tế và áp dụng được vào app không? Nếu không, cần điều chỉnh gì?
- [ ] Đoạn code fix có giải quyết được vấn đề mà không làm hỏng tính năng (hallucination) không?

---

## 4. Pha 1 - Finding Report Template (Source-level)

*Mẫu report này có thể dùng lại cho các case ở Pha 2.*

### Tiêu đề lỗi: [VD: SQL Injection in User Login]
- **Người báo cáo:** [Tên của bạn]
- **Công cụ phát hiện:** Semgrep (SAST)
- **CWE / OWASP Category:** [VD: CWE-89 / OWASP A3: Injection]

### Mô tả chi tiết (Description)
[Mô tả lỗ hổng là gì, nằm ở đâu, do dòng code nào gây ra. Có thể lấy từ phần giải thích đã audit của AI.]

### Bằng chứng (Evidence / Reproducer)
- **Source Code Evidence:**
  ```text
  [Dán đoạn code lỗi]
  ```
- **PoC (Proof of Concept):**
  ```text
  [Các bước khai thác hoặc payload để khai thác lỗ hổng]
  ```

### Mức độ ảnh hưởng (Impact)
[Hậu quả nếu lỗ hổng bị khai thác là gì? VD: Rò rỉ dữ liệu, chiếm quyền tài khoản...]

### Khuyến nghị khắc phục (Remediation)
- **Cách sửa lỗi:**
  ```text
  [Gợi ý code an toàn - lấy từ kết quả AI đã qua kiểm chứng]
  ```
