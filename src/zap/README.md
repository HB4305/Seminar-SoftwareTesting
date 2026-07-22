# ZAP + AI triage cho EShop

Thư mục này dùng để chạy OWASP ZAP trên EShop local, sinh report JSON/HTML, và (tùy chọn) dùng AI để triage alert.

## 1. Điều kiện cần thiết

- Python 3.10+
- EShop đang chạy local:
  - Backend: http://localhost:3000
  - Frontend user: http://localhost:5173
  - Frontend admin: http://localhost:5174
- ZAP daemon đang chạy tại http://localhost:8090

Nếu chưa chạy ZAP, khởi động bằng Docker:

```bash
docker run --rm -d --name eshop-zap --network host \
  -v $(pwd):$(pwd) \
  ghcr.io/zaproxy/zaproxy:stable zap.sh -daemon \
  -port 8090 -host 0.0.0.0 -config api.disablekey=true
```

## 2. Cấu hình biến môi trường

Sao chép file mẫu rồi chỉnh lại:

```bash
cp .env.example .env
```

Ví dụ các biến quan trọng:

```env
ZAP_TARGET=http://localhost:3000
ZAP_URL=http://localhost:8090
ZAP_AUTH_ROLE=none
ZAP_MAX_URLS=300

OPENAI_API_KEY=your_openai_key
OPENAI_MODEL=gpt-4o-mini

# Nếu không dùng OpenAI, có thể dùng OpenRouter
# OPENROUTER_API_KEY=your_openrouter_key
# OPENROUTER_MODEL=google/gemini-2.5-flash
```

## 3. Chạy scan ZAP

### Backend

```bash
python3 scan_zap.py \
  --target http://localhost:3000 \
  --auth-role user \
  --forced-user \
  --report-format json \
  --output-file output/backend_basic.json
```

### Frontend user

```bash
python3 scan_zap.py \
  --target http://localhost:5173 \
  --auth-role user \
  --forced-user \
  --ajax-spider \
  --report-format json \
  --output-file output/frontend_user_basic.json
```

### Frontend admin

```bash
python3 scan_zap.py \
  --target http://localhost:5174 \
  --auth-role admin \
  --forced-user \
  --ajax-spider \
  --report-format json \
  --output-file output/frontend_admin_basic.json
```

### Chỉ quét OWASP Top 10 2025

Script có thêm mode `--scan-mode owasp-top10-2025` để tự tạo scan policy và chỉ bật các active scanner thuộc OWASP Top 10 2025:

```bash
python3 scan_zap.py \
  --target http://localhost:3000 \
  --auth-role user \
  --forced-user \
  --scan-mode owasp-top10-2025 \
  --report-format json \
  --output-file output/backend_top10_2025.json
```

Mode này ưu tiên lọc theo tag `OWASP_2025_*` nếu ZAP API trả tag. Với ZAP 2.17, API `ascan.scanners()` thường không trả tag, nên script fallback sang danh sách scanner ID OWASP 2025 đã biết và chỉ enable những ID có trong bản ZAP đang chạy.

### Giới hạn URL khi scan frontend

Frontend React/SPA có thể làm AJAX Spider ghi nhận rất nhiều URL, nhất là các route dev server, asset Vite hoặc request lặp theo state. Dùng `--max-urls` để đặt ngân sách trước active scan:

```bash
python3 scan_zap.py \
  --target http://localhost:5173 \
  --auth-role user \
  --forced-user \
  --ajax-spider \
  --report-format json \
  --output-file output/frontend_user_basic.json
```

Nếu số URL đã crawl vượt giới hạn, script vẫn giữ kết quả spider/passive scan và ghi report, nhưng bỏ qua active scan để tránh quá tải RAM. Khi cần active scan sâu, ưu tiên scan backend/API `http://localhost:3000` hoặc giảm scope frontend trước.

## 4. Chạy AI triage và tạo Markdown report

Sau khi có các report JSON từ ZAP, chạy script triage để sinh Markdown theo flow riêng của ZAP. Script nhận một hoặc nhiều input JSON, gom triage theo alert group, liệt kê endpoint trong từng alert, và vẫn tạo test case cho từng endpoint/request instance.

```bash
python3 zap_ai_triage.py \
  output/backend_basic.json \
  output/frontend_user_basic.json \
  output/frontend_admin_basic.json \
  --output-dir output/markdown \
  --target-prefix http://localhost:3000 \
  --target-prefix http://localhost:5173 \
  --target-prefix http://localhost:5174
```

Nếu chỉ muốn sinh prompt/report skeleton để kiểm tra format mà chưa gọi AI provider:

```bash
python3 zap_ai_triage.py \
  output/backend_basic.json \
  output/frontend_user_basic.json \
  output/frontend_admin_basic.json \
  --output-dir output/markdown \
  --target-prefix http://localhost:3000 \
  --target-prefix http://localhost:5173 \
  --target-prefix http://localhost:5174 \
  --offline
```

Ý nghĩa các argument/flag:

| Argument/flag | Ý nghĩa |
|---|---|
| `output/backend_basic.json output/frontend_user_basic.json output/frontend_admin_basic.json` | Danh sách một hoặc nhiều file JSON report của ZAP. Đây là positional arguments, không dùng `--input`. |
| `--output-dir output/markdown` | Thư mục output cho toàn bộ Markdown ZAP triage. Script sẽ tạo `zap_triage_report.md`, `zap_test_cases.md` và thư mục `alerts/` bên trong thư mục này. |
| `--target-prefix http://localhost:3000` | Chỉ giữ các instance có URL bắt đầu bằng prefix này. Dùng để lọc đúng backend target. |
| `--target-prefix http://localhost:5173` | Chỉ giữ các instance thuộc frontend user target. Flag này có thể truyền nhiều lần. |
| `--target-prefix http://localhost:5174` | Chỉ giữ các instance thuộc frontend admin target. Nếu không truyền `--target-prefix`, script sẽ lấy tất cả URL có trong JSON ZAP. |
| `--offline` | Không gọi OpenAI/OpenRouter. Script chỉ sinh prompt, skeleton AI output và Markdown testcase để reviewer đọc hoặc chạy lại sau. |
| `--limit N` | Tùy chọn debug. Giới hạn số alert instance được đọc từ input JSON trước khi gom nhóm. Không dùng flag này khi tạo report nộp chính thức. |

## 5. File đầu ra

- `output/backend_basic.json`
- `output/frontend_user_basic.json`
- `output/frontend_admin_basic.json`
- `output/markdown/zap_triage_report.md`: báo cáo AI triage theo alert group.
- `output/markdown/zap_test_cases.md`: danh sách test case theo từng endpoint/request instance.
- `output/markdown/alerts/*_prompt.md`: prompt gửi AI cho từng alert group.
- `output/markdown/alerts/*_ai_output.md`: output AI cho từng alert group.

## 6. Ghi chú

- Nếu có `OPENAI_API_KEY`, script ưu tiên dùng OpenAI.
- Nếu không có OpenAI key mà có `OPENROUTER_API_KEY`, script dùng OpenRouter.
- Nếu thiếu cả hai key, script báo lỗi cấu hình AI. Dùng `--offline` nếu chỉ cần tạo prompt/report skeleton mà chưa gọi AI.
- ZAP là DAST nên report dùng runtime evidence từ request/response, không dùng source evidence như Semgrep.
