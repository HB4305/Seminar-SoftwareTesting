# Hướng dẫn chạy ZAP Scan + AI Triage

## 1. Chuẩn bị

### 1.1 Chạy ứng dụng mục tiêu
Bật backend hoặc frontend mà bạn muốn scan. Ví dụ:

```bash
# Nếu app chạy local bằng Node/Express
npm run dev
```

Sau đó kiểm tra ứng dụng đang chạy tại:
- Backend: http://localhost:3000
- Frontend: http://localhost:5173

### 1.2 Chạy ZAP daemon

```bash
docker run -u zap --network host -d ghcr.io/zaproxy/zaproxy:stable zap.sh -daemon -port 8090 -host 0.0.0.0 -config api.disablekey=true
```

## 2. Chạy ZAP scan

### 2.1 Scan backend

```bash
python3 src/zap/scan_zap.py --target http://localhost:3000 --report-format json --output-file src/zap/output/backend_basic.json
```

### 2.2 Scan frontend

```bash
python3 src/zap/scan_zap.py --target http://localhost:5173 --auth-role user --forced-user --ajax-spider --report-format json --output-file src/zap/output/frontend_user_basic.json
```

### 2.3 Scan admin

```bash
python3 src/zap/scan_zap.py --target http://localhost:5174 --auth-role admin --forced-user --ajax-spider --report-format json --output-file src/zap/output/frontend_admin_basic.json
```

## 3. Chạy AI triage cho report

### 3.1 Cấu hình AI provider
Mở file `src/zap/.env` và điền:

```env
OPENROUTER_API_KEY=your_openrouter_key
```

Sau đó chạy:

```bash
python3 src/zap/zap_ai_triage.py \
  --input src/zap/output/backend_basic.json \
  --format markdown \
  --output src/zap/output/zap_ai_triage_report.md
```

## 4. Kết quả đầu ra

Sau khi chạy xong, các file sẽ được sinh ra tại:
- Report JSON: src/zap/output/*.json
- AI triage markdown: src/zap/output/zap_ai_triage_report.md

## 5. Ghi chú quan trọng

- ZAP scan có thể mất vài phút tùy số lượng endpoint.
- Nếu đang chạy trên dev server, một số alert có thể là false positive/noise.
- AI triage chỉ hỗ trợ draft, cần kiểm chứng lại bằng evidence thực tế từ report và ứng dụng đang chạy.
