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
python3 docs/zap/scan_zap.py --target http://localhost:3000 --report-file docs/zap/output/backend_report.html
```

### 2.2 Scan frontend

```bash
python3 docs/zap/scan_zap.py --target http://localhost:5173 --ajax-spider --report-file docs/zap/output/frontend_report.html
```

### 2.3 Scan admin

```bash
python3 docs/zap/scan_zap.py --target http://localhost:5174 --ajax-spider --report-file docs/zap/output/admin_report.html
```

## 3. Chạy AI triage cho report

### 3.1 Nếu có Gemini API key
Tạo file docs/zap/.env với nội dung:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Sau đó chạy:

```bash
python3 docs/zap/ai_triage_zap.py --input docs/zap/output/backend_report.html --use-ai
```

### 3.2 Nếu không dùng Gemini

```bash
python3 docs/zap/ai_triage_zap.py --input docs/zap/output/backend_report.html
```

## 4. Kết quả đầu ra

Sau khi chạy xong, các file sẽ được sinh ra tại:
- Report HTML: docs/zap/output/*.html
- AI triage markdown: docs/zap/output/*_ai_triage.md

Ví dụ:
- docs/zap/output/backend_report.html
- docs/zap/output/backend_report_ai_triage.md

## 5. Ghi chú quan trọng

- ZAP scan có thể mất vài phút tùy số lượng endpoint.
- Nếu đang chạy trên dev server, một số alert có thể là false positive/noise.
- AI triage chỉ hỗ trợ draft, cần kiểm chứng lại bằng evidence thực tế từ report và ứng dụng đang chạy.
