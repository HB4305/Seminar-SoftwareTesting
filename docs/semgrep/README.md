# Hướng dẫn chạy AI Triage cho kết quả quét Semgrep trên eShop

Tài liệu này hướng dẫn bạn cách thiết lập môi trường và chạy script `semgrep_ai_triage.py` để dùng trí tuệ nhân tạo (AI - cụ thể là mô hình Gemini) tự động phân tích (triage) các lỗi bảo mật được Semgrep tìm thấy trong dự án `eshop`.

## 1. Yêu cầu hệ thống

*   Python 3.7 trở lên.
*   Công cụ Semgrep đã được cài đặt (để quét mã nguồn eShop và tạo ra file kết quả JSON).
*   API Key của Google Gemini.

## 2. Cài đặt các thư viện phụ thuộc

Mở Terminal/Command Prompt và di chuyển đến thư mục chứa file `requirements.txt` (thư mục `docs/semgrep/`), sau đó chạy lệnh:

```bash
pip install -r requirements.txt
```
*(Thư viện chính được sử dụng là `google-genai`)*

## 3. Cấu hình biến môi trường cho API Key

Script yêu cầu bạn phải cung cấp API Key của Google Gemini thông qua biến môi trường `GEMINI_API_KEY` để đảm bảo bảo mật, tuyệt đối không hardcode key vào source code.

**Trên macOS/Linux:**
```bash
export GEMINI_API_KEY="thay_api_key_cua_ban_vao_day"
```

**Trên Windows (Command Prompt):**
```cmd
set GEMINI_API_KEY="thay_api_key_cua_ban_vao_day"
```

**Trên Windows (PowerShell):**
```powershell
$env:GEMINI_API_KEY="thay_api_key_cua_ban_vao_day"
```

> **Lưu ý:** Bạn có thể lấy API Key miễn phí tại [Google AI Studio](https://aistudio.google.com/app/apikey).

## 4. Quét mã nguồn eShop bằng Semgrep

Trước khi chạy AI Triage, bạn cần dùng Semgrep để quét thư mục chứa mã nguồn của hệ thống `eshop-sut` (hoặc bất kỳ thư mục mã nguồn nào) và xuất kết quả ra định dạng JSON.

Di chuyển đến thư mục gốc của dự án `eshop` và chạy lệnh (ví dụ sử dụng bộ luật `p/owasp-top-ten`):

```bash
semgrep scan --config "p/owasp-top-ten" --json -o semgrep_results.json .
```
Lệnh trên sẽ tạo ra một file tên là `semgrep_results.json` tại thư mục hiện tại.

## 5. Chạy Script AI Triage

Khi đã có file `semgrep_results.json` và đã thiết lập biến môi trường `GEMINI_API_KEY`, bạn có thể chạy script triage:

```bash
python path/to/semgrep_ai_triage.py path/to/semgrep_results.json
```
*Thay thế `path/to/...` bằng đường dẫn thực tế đến file script và file JSON trên máy của bạn.*

**Ví dụ, nếu bạn đang đứng cùng thư mục với script và file JSON:**
```bash
python semgrep_ai_triage.py semgrep_results.json
```

## 6. Kết quả đầu ra

Sau khi chạy thành công, script sẽ:
1. Đọc lỗi đầu tiên từ file kết quả Semgrep.
2. Gửi thông tin lỗi, đoạn mã nguồn, luật báo lỗi cho Google Gemini (mô hình `gemini-2.5-flash`).
3. Nhận phản hồi và tự động tạo ra một file báo cáo Markdown, ví dụ: `AI_Triage_hardcoded-jwt-secret.md`.

File báo cáo này sẽ bao gồm:
*   **Giải thích lỗ hổng:** Nguyên nhân tại sao đoạn code lại mắc lỗi.
*   **Proof of Concept (PoC):** Kịch bản giả định để khai thác lỗi.
*   **Mức độ ảnh hưởng (Impact):** Hậu quả nếu lỗi bị khai thác.
*   **Khuyến nghị khắc phục (Remediation):** Đoạn code an toàn được đề xuất để thay thế.
