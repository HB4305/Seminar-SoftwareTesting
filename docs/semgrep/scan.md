# Hướng dẫn Quét Mã nguồn (Scanning) bằng Semgrep

Tài liệu này hướng dẫn cách thực hiện quét mã nguồn tĩnh (SAST) sử dụng Semgrep từ mức cơ bản đến nâng cao, cũng như cách chuẩn bị đầu ra phục vụ cho quá trình phân tích bằng trí tuệ nhân tạo (AI Triage).

---

## 1. Khái quát Quy trình Quét (Scan Flow)

Quy trình quét mã nguồn bằng Semgrep gồm các bước chính:
1. **Chuẩn bị:** Di chuyển vào thư mục dự án cần quét.
2. **Chọn Ruleset (Bộ luật):** Định nghĩa các quy tắc kiểm tra bảo mật (ví dụ: OWASP Top 10).
3. **Thực thi:** Chạy lệnh quét và tùy chỉnh cấu hình bỏ qua các thư mục phụ (bằng `.semgrepignore`).
4. **Xuất kết quả:** Xuất kết quả ra file JSON để phục vụ bước phân tích tiếp theo hoặc xuất định dạng text dễ đọc trên Terminal.

---

## 2. Các lệnh quét cơ bản

### 2.1 Quét nhanh với cấu hình mặc định (Semgrep Registry)
Semgrep cung cấp các bộ luật cộng đồng (Community Rulesets) được cập nhật thường xuyên. Lệnh cơ bản nhất sử dụng bộ luật OWASP Top 10 là:

* **Trên macOS / Linux:**
  ```bash
  semgrep scan --config "p/owasp-top-ten" <đường_dẫn_đến_source_code>
  ```
  *Ví dụ quét thư mục hiện tại:*
  ```bash
  semgrep scan --config "p/owasp-top-ten" .
  ```

* **Trên Windows (PowerShell - Lưu ý chcp để tránh lỗi hiển thị Unicode):**
  ```powershell
  chcp 65001
  $env:PYTHONUTF8='1'
  semgrep scan --config "p/owasp-top-ten" .
  ```

### 2.2 Các Ruleset phổ biến khuyến nghị cho Web / Node.js
Tùy vào công nghệ của dự án (ví dụ dự án EShop sử dụng Node.js & Javascript ở backend), bạn nên bổ sung các ruleset chuyên biệt sau:
- **`p/javascript`**: Bộ quy tắc bảo mật và code quality dành riêng cho JavaScript.
- **`p/nodejs`**: Bộ quy tắc tối ưu hóa cho bảo mật ứng dụng Node.js.
- **`p/owasp-top-ten`**: Quét các lỗ hổng thuộc danh mục 10 rủi ro bảo mật hàng đầu của OWASP.

*Để chạy kết hợp nhiều cấu hình cùng lúc:*
```bash
semgrep scan --config "p/owasp-top-ten" --config "p/nodejs" .
```

---

## 3. Cấu hình bỏ qua tệp tin & thư mục (`.semgrepignore`)

Khi quét một dự án lớn, Semgrep có thể tốn nhiều thời gian quét các file thư viện bên thứ ba (như `node_modules`), file build (`dist`, `build`) hoặc các file test. Điều này không cần thiết vì chúng ta chỉ muốn quét code nghiệp vụ do chính mình viết.

### Cách thực hiện:
Tạo một tệp tên là `.semgrepignore` tại thư mục gốc của dự án cần quét với nội dung mẫu:

```text
# Bỏ qua thư mục thư viện node.js
node_modules/

# Bỏ qua kết quả build
dist/
build/
.next/

# Bỏ qua thư mục test nếu không muốn quét code test
tests/
*.test.js
*.spec.js

# Bỏ qua các file cấu hình và dữ liệu cục bộ
.env
.git/
*.db
*.sqlite
```

> **Lưu ý:** Semgrep mặc định sẽ tự động đọc tệp `.semgrepignore` này khi bạn thực hiện quét từ thư mục chứa file.

---

## 4. Xuất kết quả định dạng JSON phục vụ AI Triage

Để script AI Triage (`semgrep_ai_triage.py`) có thể đọc và gửi dữ liệu sang provider AI đã cấu hình, kết quả quét của Semgrep cần phải được định dạng theo chuẩn JSON.

### Lệnh xuất JSON:
```bash
semgrep scan --config "p/owasp-top-ten" --json -o semgrep_results.json .
```
* **`--json`**: Yêu cầu Semgrep trả về kết quả quét dạng cấu trúc JSON.
* **`-o semgrep_results.json`**: Chỉ định xuất kết quả ra tệp tin có tên là `semgrep_results.json` thay vì in ra màn hình Terminal.

---

## 5. Kết hợp chạy AI Triage

Sau khi đã tạo thành công tệp `semgrep_results.json`, bạn có thể chạy script phân tích tự động bằng trí tuệ nhân tạo (AI Triage) để thẩm định các lỗi phát hiện được.

1. **Thiết lập provider/model/API key:**
   ```bash
   cp docs/semgrep/.env.example docs/semgrep/.env
   ```
   Sau đó mở `docs/semgrep/.env` và điền cấu hình thật. Mặc định:
   ```env
   AI_PROVIDER=gemini
   AI_MODEL=gemini-2.5-flash
   GEMINI_API_KEY=api_key_cua_ban
   ```
   Nếu dùng endpoint OpenAI-compatible:
   ```env
   AI_PROVIDER=openai-compatible
   AI_MODEL=deepseek/deepseek-chat
   OPENAI_API_KEY=api_key_cua_ban
   OPENAI_BASE_URL=https://openrouter.ai/api/v1
   ```
2. **Chạy script triage:**
   ```bash
   python docs/semgrep/semgrep_ai_triage.py semgrep_results.json
   ```
3. **Đầu ra:** Script sẽ tự động sinh ra tệp báo cáo chi tiết định dạng Markdown chứa:
   - **Giải thích lỗ hổng**
   - **Mã khai thác thử nghiệm (PoC)**
   - **Mức độ ảnh hưởng (Impact)**
   - **Mã sửa lỗi an toàn (Remediation)**

---

## 6. Xem kết quả trực tiếp từ Terminal

Nếu bạn chỉ muốn rà soát nhanh các lỗi hiển thị trực quan dạng văn bản, chỉ cần chạy lệnh quét thông thường (không dùng `-o`):

![Semgrep Scan Output Sample](../../resources/semgrep_test1.png)

Mỗi lỗi hiển thị trên Terminal sẽ bao gồm:
- **Tên tệp và dòng code mắc lỗi.**
- **Rule ID** và **Mức độ nghiêm trọng (Severity)** (Ví dụ: `WARNING`, `ERROR`).
- **Thông điệp mô tả chi tiết lỗi** từ Semgrep.
- **Đoạn code thực tế** bị bắt lỗi trực quan.
