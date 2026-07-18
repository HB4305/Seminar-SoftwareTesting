# Hướng dẫn chạy AI Triage cho kết quả quét Semgrep trên eShop

Tài liệu này hướng dẫn bạn cách thiết lập môi trường và chạy script `semgrep_ai_triage.py` để dùng trí tuệ nhân tạo (AI) tự động phân tích (triage) các lỗi bảo mật được Semgrep tìm thấy trong dự án `eshop`. Script mặc định dùng Gemini, đồng thời hỗ trợ provider OpenAI-compatible thông qua cấu hình `.env`.

## 1. Yêu cầu hệ thống

*   Python 3.8 trở lên.
*   Công cụ Semgrep đã được cài đặt (để quét mã nguồn eShop và tạo ra file kết quả JSON).
*   API Key của provider AI bạn muốn dùng, ví dụ Google Gemini hoặc một endpoint OpenAI-compatible.

## 2. Cài đặt các thư viện phụ thuộc

Mở Terminal/Command Prompt và di chuyển đến thư mục chứa file `requirements.txt` (thư mục `docs/semgrep/`), sau đó chạy lệnh:

```bash
pip install -r requirements.txt
```
*(Thư viện chính được sử dụng cho provider mặc định là `google-genai`. Provider OpenAI-compatible dùng thư viện chuẩn của Python.)*

## 3. Cấu hình `.env` cho API Key, Provider và Model

Script đọc cấu hình từ file `.env` hoặc biến môi trường thật của hệ điều hành. Tuyệt đối không hardcode API key vào source code và không commit file `.env`.

1. Copy file mẫu:
```bash
cp docs/semgrep/.env.example docs/semgrep/.env
```
2. Mở `docs/semgrep/.env` và điền API key thật.

### Cấu hình Gemini mặc định

```env
AI_PROVIDER=gemini
AI_MODEL=gemini-2.5-flash
GEMINI_API_KEY=thay_api_key_cua_ban_vao_day
```

> **Lưu ý:** Bạn có thể lấy API Key miễn phí tại [Google AI Studio](https://aistudio.google.com/app/apikey).

### Cấu hình OpenAI-compatible

```env
AI_PROVIDER=openai-compatible
AI_MODEL=deepseek/deepseek-chat
OPENAI_API_KEY=thay_api_key_cua_ban_vao_day
OPENAI_BASE_URL=https://openrouter.ai/api/v1
```

Bạn có thể dùng `AI_API_KEY` thay cho `GEMINI_API_KEY` hoặc `OPENAI_API_KEY` nếu muốn đặt tên biến thống nhất giữa các provider.

## 4. Quét mã nguồn eShop bằng Semgrep

Trước khi chạy AI Triage, bạn cần dùng Semgrep để quét thư mục chứa mã nguồn của hệ thống `eshop-sut` (hoặc bất kỳ thư mục mã nguồn nào) và xuất kết quả ra định dạng JSON.

Di chuyển đến thư mục gốc của dự án `eshop` và chạy lệnh (ví dụ sử dụng bộ luật `p/owasp-top-ten`):

```bash
semgrep scan --config "p/owasp-top-ten" --json -o semgrep_results.json .
```
Lệnh trên sẽ tạo ra một file tên là `semgrep_results.json` tại thư mục hiện tại.

## 5. Chạy Script AI Triage

Khi đã có file `semgrep_results.json` và đã thiết lập `.env` hoặc biến môi trường cho provider AI, bạn có thể chạy script triage:

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
2. Gửi thông tin lỗi, đoạn mã nguồn, luật báo lỗi cho provider/model được cấu hình trong `.env`.
3. Nhận phản hồi và tự động tạo ra một file báo cáo Markdown, ví dụ: `AI_Triage_hardcoded-jwt-secret.md`.

File báo cáo này sẽ bao gồm:
*   **Giải thích lỗ hổng:** Nguyên nhân tại sao đoạn code lại mắc lỗi.
*   **Proof of Concept (PoC):** Kịch bản giả định để khai thác lỗi.
*   **Mức độ ảnh hưởng (Impact):** Hậu quả nếu lỗi bị khai thác.
*   **Khuyến nghị khắc phục (Remediation):** Đoạn code an toàn được đề xuất để thay thế.
