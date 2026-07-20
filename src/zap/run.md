# Chuẩn bị môi trường 
- cd Seminar-SoftwareTesting
- python -m venv venv (tạo moi truong ao)
- pip install python-owasp-zap-v2.4 (tai library)
- docker pull ghcr.io/zaproxy/zaproxy:stable 
- mkdir -p src/zap/output (tao folder luu ket qua)
- tao file env dua tren thong tin o file .env.example

- bat eshop (chay runserver trong repo eshop)
- check lai
```bash
curl -s -o /dev/null -w "backend: %{http_code}\n" http://localhost:3000/api/products
curl -s -o /dev/null -w "frontend user: %{http_code}\n" http://localhost:5173/
curl -s -o /dev/null -w "frontend admin: %{http_code}\n" http://localhost:5174/
```
Kỳ vọng: mã khác 000 (thường 200). Nếu 000 → EShop chưa chạy, mọi thứ phía sau đều sai.

# Chay bang script
## bước 1 - BACKEND (Ko auth)
```bash
python src/zap/scan_zap.py \
  --target http://localhost:3000 \
  --scan-mode basic \
  --report-format json \
  --output-file src/zap/output/backend_basic.json
``` 
- Nếu gặp lỗi: [!] [Errno 13] Permission denied: '/home/melyen/Documents/class/testing/seminar/Seminar-SoftwareTesting/src/zap/output/backend_basic.json'
- Cách xử lí: sudo chown -R $(id -u):$(id -g) src/zap/output

Check:
| Check | Đúng | Sai |
| --- | --- | --- |
| Terminal in [+] Connected to ZAP | ✓ | Docker/ZAP lỗi |
| Thấy [1/4] TRADITIONAL SPIDER → 100% | ✓ | Target không reachable |
| Thấy Skipping AJAX Spider | ✓ (backend không cần) | — |
| Thấy [4/4] ACTIVE SCAN → 100% | ✓ | Active scan treo/timeout |
| Block ZAP SCAN SUMMARY với Total alerts | ✓ | Không có summary = scan chưa xong |
| File src/zap/output/backend_basic.json tồn tại | ✓ | Report generation fail |

## Bước 2: Frontend user (SPA + auth)
```bash
python src/zap/scan_zap.py \
  --target http://localhost:5173 \
  --auth-role user \
  --forced-user \
  --ajax-spider \
  --scan-mode basic \
  --report-format json \
  --output-file src/zap/output/frontend_user_basic.json
```
- Nếu gặp lỗi: [!] EShop login failed: HTTP Error 401: Unauthorized
- Cách xử lí: Kiểm tra kĩ lại file env đã điền đúng thông tin tài khoản, mật khẩu user hay chưa

Check
| Check | Đúng | Sai |
| --- | --- | --- |
| Không lỗi EShop login failed | ✓ | Sai password hoặc backend :3000 down |
| Không lỗi Authentication verification failed | ✓ | JWT/Replacer hỏng |
| Thấy AJAX Spider chạy (không skip) | ✓ | Thiếu --ajax-spider → coverage SPA thấp |
| Alert có URL :5173 | ✓ | Chỉ có :3000 → scan nhầm target/session cũ |

## Bước 3: Frontend admin (tùy chọn)
```bash
python src/zap/scan_zap.py \
  --target http://localhost:5174 \
  --auth-role admin \
  --forced-user \
  --ajax-spider \
  --scan-mode basic \
  --report-format json \
  --output-file src/zap/output/frontend_admin_basic.json
```

## Bước 4 — Thu alert counts (mục seminar)
Ghi bảng từ block terminal:
```bash
Target       : http://localhost:3000
Total alerts : N
 - High       : ...
 - Medium     : ...
```
Mỗi target một dòng — không cộng chung nếu chưa chắc scope sạch.
Triage offline (tùy chọn):
```bash
python ai_triage_zap.py --input output/backend_basic.json --output output/zap_ai_triage_report.md
```
- Nếu gặp lỗi: `[!] Cannot read ZAP report: [Errno 2] No such file or directory: '/home/melyen/Documents/class/testing/seminar/Seminar-SoftwareTesting/src/zap/output/backend_basic.html'` (hoặc `.json`)
- Cách xử lí: 
  1. Kiểm tra xem file report đã thực sự được sinh ra trong thư mục `src/zap/output/` chưa. Nếu chưa có, hãy chạy lại lệnh scan ZAP ở **Bước 1** để tạo file.
  2. Kiểm tra lại đường dẫn truyền vào tham số `--input`. Đảm bảo khớp chính xác tên và phần mở rộng (ví dụ: dùng `.json` nếu scan xuất JSON, `.html` nếu scan xuất HTML).
  3. Nếu chạy script `ai_triage_zap.py` không có tham số `--input`, script sẽ tự động tìm kiếm file mới nhất trong thư mục `output`. Nếu thư mục rỗng, hãy chạy lệnh scan trước.

# Phần 4 — Chạy bằng GUI (để đối chiếu)
Mục tiêu: làm tương đương một phần script, rồi so sánh.
## 4.1 Backend — tương đương script không auth
Mở ZAP → session mới (không dùng session cũ).
Quick Start → Automated Scan.
URL: http://localhost:3000 → Attack.
Đợi Spider + Passive + Active xong.
Tab Alerts → đếm theo risk.
Report → Generate Report → export HTML/JSON.
So với script:

| Tiêu chí | GUI | Script |
| --- | --- | --- |
| Spider + Active | Có (Automated Scan) | Có |
| Context EShop tự giới hạn scope | Không tự — phải cấu hình tay | Có sẵn |
| Auth JWT cho frontend | Khó hơn | --auth-role tự làm |
| AJAX Spider cho SPA | Phải bật riêng | --ajax-spider |
| Alert summary tự động | Đếm tay trên Alerts | In sẵn cuối log |
| Reproduce | Khó | Một command |

## 4.2 Frontend user — GUI gần với script (phức tạp hơn)
Để GUI “đúng” như script, cần thêm:
- Context tên EShop, include regex http://localhost:5173.*
- Manual Explore hoặc AJAX Spider sau khi đã có auth
- Replacer rule: thêm header Authorization: Bearer <token>
- Lấy token:
```bash
curl -s -X POST http://localhost:3000/api/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@eshop.com","password":"Test1234!"}'
```
- Chạy spider/active trong context đó.
Nếu GUI chỉ Automated Scan :5173 không auth → thường ít alert hơn script — đó là hành vi đúng, không phải script sai.

# Phần 5 — Tiếp tục công việc Check ZAP & viết PoC kiểm chứng

Mục tiêu tiếp theo của nhóm là chạy quét ZAP trên toàn bộ các target (Backend, Frontend Web, Frontend Admin), thu thập report dạng JSON, sử dụng AI để triage và đề xuất PoC, sau đó thực hiện kiểm chứng thủ công.

## 5.1 Quy trình thực hiện quét và Triage tự động bằng AI

1. **Khởi chạy hệ thống EShop (SUT)**:
   Di chuyển sang thư mục dự án `eshop-sut` và chạy file bash khởi động tất cả server:
   ```bash
   cd ../eshop-sut
   ./run_servers.sh
   ```
   *Lưu ý: Nếu chưa chạy npm install lần nào ở các folder backend/frontend, hãy vào từng folder và cài đặt trước.*

2. **Chạy các lệnh quét tương ứng**:
   Quay lại thư mục `Seminar-SoftwareTesting`:
   ```bash
   cd ../Seminar-SoftwareTesting
   ```
   Chạy scan cho Backend (không auth):
   ```bash
   python src/zap/scan_zap.py --target http://localhost:3000 --report-format json --output-file src/zap/output/backend_basic.json
   ```
   Chạy scan cho Frontend Web User (có auth, AJAX Spider):
   ```bash
   python src/zap/scan_zap.py --target http://localhost:5173 --auth-role user --forced-user --ajax-spider --report-format json --output-file src/zap/output/frontend_user_basic.json
   ```
   Chạy scan cho Frontend Admin (có auth, AJAX Spider):
   ```bash
   python src/zap/scan_zap.py --target http://localhost:5174 --auth-role admin --forced-user --ajax-spider --report-format json --output-file src/zap/output/frontend_admin_basic.json
   ```

3. **Chạy AI Triage trực tuyến (Online Triage)**:
   Nếu muốn gọi OpenRouter để AI phân tích chi tiết và đề xuất PoC tự động, hãy thiết lập `OPENROUTER_API_KEY` trong `.env` và chạy script triage với tham số `--use-ai`:
   ```bash
   python src/zap/ai_triage_zap.py --input src/zap/output/backend_basic.json --use-ai
   ```
   Báo cáo chi tiết sẽ được ghi đè vào file `src/zap/output/zap_ai_triage_report.md`.

---

## 5.2 Viết Proof of Concept (PoC) kiểm chứng thủ công bằng Curl

Từ báo cáo triage của Backend API (`backend_basic.json`), ZAP đã phát hiện 3 lỗ hổng/cấu hình sai ở mức độ Medium/Low/Info. Dưới đây là cách dùng AI hỗ trợ viết PoC và cách tự chạy lệnh `curl` để tái hiện, phục vụ cho việc làm báo cáo seminar.

### Lỗ hổng 1: Cross-Domain Misconfiguration (CORS quá rộng - `Access-Control-Allow-Origin: *`)
- **Nguyên nhân**: API Backend trả về header CORS cho phép mọi nguồn (`*`) truy cập, có thể dẫn đến rò rỉ dữ liệu nhạy cảm qua trình duyệt nếu endpoint không được bảo vệ đúng cách.
- **Lệnh PoC (Curl)**:
  ```bash
  curl -i -H "Origin: http://evil.com" http://localhost:3000/api/products
  ```
- **Cách AI hỗ trợ viết PoC**: Hỏi AI: *"Backend Node.js Express của tôi cấu hình CORS thế nào khiến ZAP báo lỗi Cross-Domain Misconfiguration? Cho tôi xin lệnh curl test và code Express để fix."*
- **Kết quả kiểm chứng (Expected vs Actual)**:
  - **Expected**: Backend chỉ cho phép các origin hợp lệ (như `http://localhost:5173`) hoặc không trả về header này đối với các request từ nguồn không tin cậy.
  - **Actual**: Response trả về có header `Access-Control-Allow-Origin: *`, chứng minh bất kỳ trang web nào (kể cả trang giả mạo) cũng có thể đọc dữ liệu API này bằng JavaScript.

### Lỗ hổng 2: CSP: Failure to Define Directive with No Fallback (Thiếu Directive CSP quan trọng)
- **Nguyên nhân**: Response header `Content-Security-Policy: default-src 'none'` thiếu cấu hình cho các directive như `frame-ancestors` hoặc `form-action` (các directive này không kế thừa từ `default-src`).
- **Lệnh PoC (Curl)**:
  ```bash
  curl -i http://localhost:3000/api/products
  ```
- **Cách AI hỗ trợ viết PoC**: Hỏi AI: *"ZAP báo lỗi CSP directive no fallback khi trả về default-src 'none'. Hãy giải thích lỗi này và viết cấu hình CSP đầy đủ cho ứng dụng Express."*
- **Kết quả kiểm chứng (Expected vs Actual)**:
  - **Expected**: Header `Content-Security-Policy` chứa đầy đủ cấu hình hạn chế frame nhúng hoặc submit form, ví dụ: `Content-Security-Policy: default-src 'none'; frame-ancestors 'none'; form-action 'none';`
  - **Actual**: Response header chỉ chứa `Content-Security-Policy: default-src 'none'`, để lộ nguy cơ bị nhúng clickjacking qua form hoặc iframe từ các domain khác.

### Lỗ hổng 3: Server Leaks Information via "X-Powered-By" HTTP Header
- **Nguyên nhân**: Response header tiết lộ thông tin công nghệ sử dụng bên dưới (`X-Powered-By: Express`), giúp kẻ tấn công thu hẹp phạm vi thử nghiệm lỗ hổng bảo mật.
- **Lệnh PoC (Curl)**:
  ```bash
  curl -i http://localhost:3000/
  ```
- **Cách AI hỗ trợ viết PoC**: Hỏi AI: *"Làm cách nào để ẩn header X-Powered-By trong Express JS?"*
- **Kết quả kiểm chứng (Expected vs Actual)**:
  - **Expected**: Response header không chứa trường thông tin `X-Powered-By`.
  - **Actual**: Header trả về có dòng `X-Powered-By: Express`.

---

## 5.3 Sử dụng AI để sinh mã PoC tự động bằng Python

Nếu nhóm muốn viết script tự động kiểm tra lại (Regression Test) các header cấu hình sai này thay vì chạy lệnh curl thủ công, có thể dùng AI để sinh mã Python sử dụng thư viện `requests` như sau:

**Prompt đưa cho AI:**
> *"Hãy viết một script Python sử dụng thư viện `requests` để kiểm thử tự động (reproduce) 3 lỗi cấu hình header sau trên endpoint `http://localhost:3000/api/products`:
> 1. Kiểm tra xem có header `X-Powered-By` hay không. Nếu có, báo lỗi.
> 2. Gửi request kèm `Origin: http://evil.com` và kiểm tra xem response header `Access-Control-Allow-Origin` có trả về `*` hay không. Nếu có, báo lỗi CORS quá rộng.
> 3. Kiểm tra xem header `Content-Security-Policy` có chứa `frame-ancestors` hoặc `form-action` hay không. Nếu thiếu, báo lỗi bảo mật CSP."*

**Mã Python sinh ra bởi AI và lưu tại `src/zap/verify_headers.py`**:
*(Đoạn code này có thể chạy sau mỗi lần dev team sửa lỗi để kiểm tra xem đã cấu hình đúng chưa).*
```python
import requests

url = "http://localhost:3000/api/products"

def test_x_powered_by():
    resp = requests.get(url)
    if "X-Powered-By" in resp.headers:
        print(f"[FAIL] Information Leak: X-Powered-By header is present: {resp.headers['X-Powered-By']}")
    else:
        print("[PASS] X-Powered-By header is hidden.")

def test_cors_origin():
    headers = {"Origin": "http://evil.com"}
    resp = requests.get(url, headers=headers)
    allow_origin = resp.headers.get("Access-Control-Allow-Origin")
    if allow_origin == "*":
        print("[FAIL] CORS Misconfiguration: Access-Control-Allow-Origin is '*'")
    else:
        print(f"[PASS] CORS is restricted (Origin header value: {allow_origin})")

def test_csp_directives():
    resp = requests.get(url)
    csp = resp.headers.get("Content-Security-Policy", "")
    if not csp:
        print("[FAIL] CSP header is missing completely.")
        return
    
    missing = []
    if "frame-ancestors" not in csp:
        missing.append("frame-ancestors")
    if "form-action" not in csp:
        missing.append("form-action")
        
    if missing:
        print(f"[FAIL] CSP directive missing without fallback: {missing} (Current CSP: {csp})")
    else:
        print("[PASS] CSP directives are configured correctly.")

if __name__ == "__main__":
    print("--- Running Verification PoC Tests ---")
    test_x_powered_by()
    test_cors_origin()
    test_csp_directives()
```