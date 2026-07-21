# ZAP OpenRouter JSON Extract Result

- Source files: `frontend_admin_basic.json`
- Render Mode: `Local Security Triage Engine`

Dưới đây là báo cáo các lỗ hổng bảo mật được trích xuất từ dữ liệu ZAP:

---

### 1. Path Traversal
- **Nguồn phát hiện (Source)**: `frontend_admin_basic.json`
- **Độ nguy hiểm (Risk) & Độ tin cậy (Confidence)**: `High` & `1`
- **Các URL bị ảnh hưởng (Affected URLs)**:
- `GET http://localhost:5174/node_modules/.vite/deps/chunk-nbk3hphP.js?v=%2Fchunk-nbk3hphP.js`
- `GET http://localhost:5173/node_modules/.vite/deps/chunk-CYJPkc-J.js?v=%2Fchunk-CYJPkc-J.js`
- **Bản chất lỗi**: Ứng dụng có thể bị tấn công Path Traversal, cho phép truy cập các tệp và thư mục ngoài thư mục gốc của web.
- **Tag OWASP**: OWASP_2021_A01, OWASP_2025_A01, OWASP_2017_A05
- **PoC**: `GET http://localhost:5174/node_modules/.vite/deps/chunk-nbk3hphP.js?v=%2Fchunk-nbk3hphP.js`?v=/chunk-nbk3hphP.js
- **Cách verify PoC**:
  * **Expected**: Không thể truy cập các tệp ngoài phạm vi cho phép hoặc nhận mã lỗi.
  * **Actual**: Yêu cầu trả về nội dung của tệp tin nguồn.
- **Ghi chú**: Có thể là noise do dev server.

---

### 2. Content Security Policy (CSP) Header Not Set
- **Nguồn phát hiện (Source)**: `frontend_admin_basic.json`
- **Độ nguy hiểm (Risk) & Độ tin cậy (Confidence)**: `Medium` & `3`
- **Các URL bị ảnh hưởng (Affected URLs)**:
- `GET http://localhost:5174`
- `GET http://localhost:5174/`
- `GET http://localhost:5174/?token=OK9FS_0dWL1i`
- `GET http://localhost:5174/robots.txt`
- `GET http://localhost:5174/sitemap.xml`
- `GET http://localhost:5173`
- `GET http://localhost:5173/`
- `GET http://localhost:5173/forgot-password`
- `GET http://localhost:5173/robots.txt`
- `GET http://localhost:5173/sitemap.xml`
- **Bản chất lỗi**: Header CSP không được thiết lập, thiếu lớp bảo mật chống XSS và các cuộc tấn công injection.
- **Tag OWASP**: OWASP_2021_A05, OWASP_2017_A06, OWASP_2025_A02
- **PoC**: `GET http://localhost:5174`
- **Cách verify PoC**:
  * **Expected**: Header `Content-Security-Policy` được thiết lập.
  * **Actual**: Không có header `Content-Security-Policy` trong phản hồi.

---

### 3. Missing Anti-clickjacking Header
- **Nguồn phát hiện (Source)**: `frontend_admin_basic.json`
- **Độ nguy hiểm (Risk) & Độ tin cậy (Confidence)**: `Medium` & `2`
- **Các URL bị ảnh hưởng (Affected URLs)**:
- `GET http://localhost:5174`
- `GET http://localhost:5174/`
- `GET http://localhost:5174/?token=OK9FS_0dWL1i`
- `GET http://localhost:5174/robots.txt`
- `GET http://localhost:5174/sitemap.xml`
- `GET http://localhost:5173`
- `GET http://localhost:5173/`
- `GET http://localhost:5173/forgot-password`
- `GET http://localhost:5173/robots.txt`
- `GET http://localhost:5173/sitemap.xml`
- **Bản chất lỗi**: Phản hồi thiếu header chống Clickjacking (`X-Frame-Options` hoặc `Content-Security-Policy` với `frame-ancestors`).
- **Tag OWASP**: OWASP_2021_A05, OWASP_2017_A06, OWASP_2025_A02
- **PoC**: `GET http://localhost:5174`
- **Cách verify PoC**:
  * **Expected**: Header `X-Frame-Options` hoặc `Content-Security-Policy` với `frame-ancestors` được thiết lập.
  * **Actual**: Không có các header chống Clickjacking trong phản hồi.

---

### 4. Timestamp Disclosure - Unix
- **Nguồn phát hiện (Source)**: `frontend_admin_basic.json`
- **Độ nguy hiểm (Risk) & Độ tin cậy (Confidence)**: `Low` & `1`
- **Các URL bị ảnh hưởng (Affected URLs)**:
- `GET http://localhost:5174/node_modules/.vite/deps/react-dom_client.js?v=1cc4e6b1`
- `GET http://localhost:5173/node_modules/.vite/deps/react-dom_client.js?v=82fd3d9d`
- **Bản chất lỗi**: Ứng dụng/máy chủ web tiết lộ dấu thời gian Unix, có thể cung cấp thông tin nhạy cảm cho kẻ tấn công.
- **Tag OWASP**: OWASP_2021_A01, OWASP_2017_A03, OWASP_2025_A01
- **PoC**: `GET http://localhost:5174/node_modules/.vite/deps/react-dom_client.js?v=1cc4e6b1`
- **Cách verify PoC**:
  * **Expected**: Không có dấu thời gian Unix hiển thị trong phản hồi.
  * **Actual**: Giá trị dấu thời gian xuất hiện trong phản hồi.
- **Ghi chú**: Có thể là noise do dev server.

---

### 5. X-Content-Type-Options Header Missing
- **Nguồn phát hiện (Source)**: `frontend_admin_basic.json`
- **Độ nguy hiểm (Risk) & Độ tin cậy (Confidence)**: `Low` & `2`
- **Các URL bị ảnh hưởng (Affected URLs)**:
- `GET http://localhost:5174`
- `GET http://localhost:5174/`
- `GET http://localhost:5174/favicon.svg`
- `GET http://localhost:5174/robots.txt`
- `GET http://localhost:5174/sitemap.xml`
- `GET http://localhost:5173`
- `GET http://localhost:5173/`
- `GET http://localhost:5173/favicon.svg`
- `GET http://localhost:5173/robots.txt`
- `GET http://localhost:5173/sitemap.xml`
- `GET http://localhost:3000/api/products?search=`
- `GET http://localhost:3000/api/products/1`
- `GET http://localhost:3000/api/products/2`
- `GET http://localhost:3000/api/users/me`
- `POST http://localhost:3000/api/login`
- **Bản chất lỗi**: Header `X-Content-Type-Options` không được đặt thành 'nosniff', cho phép MIME-sniffing.
- **Tag OWASP**: OWASP_2021_A05, OWASP_2017_A06, OWASP_2025_A02
- **PoC**: `GET http://localhost:5174`
- **Cách verify PoC**:
  * **Expected**: Header `X-Content-Type-Options: nosniff` được thiết lập.
  * **Actual**: Không có header `X-Content-Type-Options` trong phản hồi.

---

### 6. Cross Site Scripting (DOM Based)
- **Nguồn phát hiện (Source)**: `frontend_admin_basic.json`
- **Độ nguy hiểm (Risk) & Độ tin cậy (Confidence)**: `High` & `3`
- **Các URL bị ảnh hưởng (Affected URLs)**:
- `GET http://localhost:5173?name=abc#<img src="random.gif" onerror=alert(5397)>`
- `GET http://localhost:5173/?name=abc#<img src="random.gif" onerror=alert(5397)>`
- `GET http://localhost:5173/?token=zO5GHMi7gwIk?name=abc#<img src="random.gif" onerror=alert(5397)>`
- **Bản chất lỗi**: Ứng dụng dễ bị tấn công XSS dựa trên DOM, cho phép kẻ tấn công thực thi mã độc trong trình duyệt người dùng.
- **Tag OWASP**: OWASP_2025_A05, OWASP_2021_A03, OWASP_2017_A07
- **PoC**: `GET http://localhost:5173?name=abc#<img src="random.gif" onerror=alert(5397)>`
- **Cách verify PoC**:
  * **Expected**: Không có cửa sổ `alert` bật lên hoặc mã JavaScript không được thực thi.
  * **Actual**: Cửa sổ `alert` bật lên trong trình duyệt khi truy cập URL.

---

### 7. CSP: Failure to Define Directive with No Fallback
- **Nguồn phát hiện (Source)**: `frontend_admin_basic.json`
- **Độ nguy hiểm (Risk) & Độ tin cậy (Confidence)**: `Medium` & `3`
- **Các URL bị ảnh hưởng (Affected URLs)**:
- `GET http://localhost:3000`
- `GET http://localhost:3000/api`
- `GET http://localhost:3000/api/login`
- `GET http://localhost:3000/api/users`
- `GET http://localhost:3000/sitemap.xml`
- **Bản chất lỗi**: Chính sách bảo mật nội dung (CSP) không định nghĩa các chỉ thị bắt buộc, có thể dẫn đến việc cho phép mọi thứ.
- **Tag OWASP**: OWASP_2021_A05, OWASP_2017_A06, OWASP_2025_A02
- **PoC**: `GET http://localhost:3000`
- **Cách verify PoC**:
  * **Expected**: Header `Content-Security-Policy` có các chỉ thị đầy đủ.
  * **Actual**: Header `Content-Security-Policy: default-src 'none'` thiếu các chỉ thị khác.

---

### 8. Cross-Domain Misconfiguration
- **Nguồn phát hiện (Source)**: `frontend_admin_basic.json`
- **Độ nguy hiểm (Risk) & Độ tin cậy (Confidence)**: `Medium` & `2`
- **Các URL bị ảnh hưởng (Affected URLs)**:
- `GET http://localhost:3000`
- `GET http://localhost:3000/api`
- `GET http://localhost:3000/api/login`
- `GET http://localhost:3000/api/users/me`
- `POST http://localhost:3000/api/login`
- **Bản chất lỗi**: Cấu hình CORS cho phép `Access-Control-Allow-Origin: *`, có thể dẫn đến việc tải dữ liệu trình duyệt từ các miền không mong muốn.
- **Tag OWASP**: OWASP_2021_A01, OWASP_2025_A01, OWASP_2017_A05
- **PoC**: `GET http://localhost:3000`
- **Cách verify PoC**:
  * **Expected**: Header `Access-Control-Allow-Origin` chỉ cho phép các miền cụ thể.
  * **Actual**: Header `Access-Control-Allow-Origin: *` trong phản hồi.

---

### 9. Server Leaks Information via "X-Powered-By" HTTP Response Header Field(s)
- **Nguồn phát hiện (Source)**: `frontend_admin_basic.json`
- **Độ nguy hiểm (Risk) & Độ tin cậy (Confidence)**: `Low` & `2`
- **Các URL bị ảnh hưởng (Affected URLs)**:
- `GET http://localhost:3000`
- `GET http://localhost:3000/api`
- `GET http://localhost:3000/api/login`
- `GET http://localhost:3000/api/users/me`
- `POST http://localhost:3000/api/login`
- **Bản chất lỗi**: Header `X-Powered-By` tiết lộ thông tin về công nghệ máy chủ (`Express`), có thể giúp kẻ tấn công tìm kiếm lỗ hổng.
- **Tag OWASP**: OWASP_2021_A01, OWASP_2017_A03, OWASP_2025_A01
- **PoC**: `GET http://localhost:3000`
- **Cách verify PoC**:
  * **Expected**: Không có header `X-Powered-By` trong phản hồi.
  * **Actual**: Header `X-Powered-By: Express` xuất hiện trong phản hồi.

---
