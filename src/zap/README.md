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
  --max-urls 300 \
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
  --max-urls 300 \
  --report-format json \
  --output-file output/frontend_admin_basic.json
```

### Giới hạn URL khi scan frontend

Frontend React/SPA có thể làm AJAX Spider ghi nhận rất nhiều URL, nhất là các route dev server, asset Vite hoặc request lặp theo state. Dùng `--max-urls` để đặt ngân sách trước active scan:

```bash
python3 scan_zap.py \
  --target http://localhost:5173 \
  --auth-role user \
  --forced-user \
  --ajax-spider \
  --max-urls 300 \
  --report-format json \
  --output-file output/frontend_user_basic.json
```

Nếu số URL đã crawl vượt giới hạn, script vẫn giữ kết quả spider/passive scan và ghi report, nhưng bỏ qua active scan để tránh quá tải RAM. Khi cần active scan sâu, ưu tiên scan backend/API `http://localhost:3000` hoặc giảm scope frontend trước.

## 4. Chạy AI triage

Nếu có OpenAI hoặc OpenRouter key, chạy:

```bash
python3 openrouter_zap_json_extract.py \
  --input output/backend_basic.json output/frontend_user_basic.json output/frontend_admin_basic.json \
  --format markdown \
  --output output/zap_openrouter_result.md
```

Nếu API lỗi, script sẽ tự fallback sang local triager.

## 5. File đầu ra

- output/backend_basic.json
- output/frontend_user_basic.json
- output/frontend_admin_basic.json
- output/zap_openrouter_result.md

## 6. Ghi chú

- Nếu có OPENAI_API_KEY, script sẽ ưu tiên dùng OpenAI.
- Nếu không có OpenAI key mà có OPENROUTER_API_KEY, script sẽ dùng OpenRouter.
- Nếu không có key nào, script vẫn có thể tạo report local triage.
