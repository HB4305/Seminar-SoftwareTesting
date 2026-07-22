Tôi dùng OWASP ZAP (DAST) để quét runtime của ứng dụng EShop và phát hiện một nhóm alert bảo mật cùng loại.
Bạn hãy đóng vai trò là chuyên gia bảo mật ứng dụng để triage alert này ở cấp nhóm, không lặp lại phân tích riêng cho từng endpoint nếu cùng root cause.
Hãy trả lời hoàn toàn bằng tiếng Việt, trừ các thuật ngữ chuẩn như True Positive, False Positive, Needs Human Review, CWE, WASC, OWASP, HTTP, header, payload.

Thông tin kỹ thuật:
- Mã alert: ZAP-004
- Alert name: X-Content-Type-Options Header Missing
- Plugin ID: 10021
- Alert Ref: 10021
- Source JSON: backend_basic.json, frontend_admin_basic.json, frontend_user_basic.json
- Site: http://localhost:3000, http://localhost:5173, http://localhost:5174
- Số endpoint/request instance bị ảnh hưởng: 27
- Risk: Low
- Confidence: Medium
- CWE: CWE-693
- WASC: WASC-15
- Tags: OWASP_2021_A05, POLICY_QA_STD, POLICY_PENTEST, SYSTEMIC, CWE-693, OWASP_2017_A06, OWASP_2025_A02

Danh sách endpoint bị ảnh hưởng:
| # | Method | URL | Param | Evidence | Source JSON |
|---|---|---|---|---|---|
| 15 | GET | `http://localhost:3000/api/users/me` | `x-content-type-options` | `N/A` | `backend_basic.json` |
| 16 | POST | `http://localhost:3000/api/login` | `x-content-type-options` | `N/A` | `backend_basic.json` |
| 35 | GET | `http://localhost:5173` | `x-content-type-options` | `N/A` | `frontend_user_basic.json` |
| 36 | GET | `http://localhost:5173/` | `x-content-type-options` | `N/A` | `frontend_user_basic.json` |
| 37 | GET | `http://localhost:5173/favicon.svg` | `x-content-type-options` | `N/A` | `frontend_user_basic.json` |
| 38 | GET | `http://localhost:5173/robots.txt` | `x-content-type-options` | `N/A` | `frontend_user_basic.json` |
| 39 | GET | `http://localhost:5173/sitemap.xml` | `x-content-type-options` | `N/A` | `frontend_user_basic.json` |
| 66 | GET | `http://localhost:3000/api/products?search=` | `x-content-type-options` | `N/A` | `frontend_user_basic.json` |
| 67 | GET | `http://localhost:3000/api/products/1` | `x-content-type-options` | `N/A` | `frontend_user_basic.json` |
| 68 | GET | `http://localhost:3000/api/products/2` | `x-content-type-options` | `N/A` | `frontend_user_basic.json` |
| 69 | GET | `http://localhost:3000/api/users/me` | `x-content-type-options` | `N/A` | `frontend_user_basic.json` |
| 70 | POST | `http://localhost:3000/api/login` | `x-content-type-options` | `N/A` | `frontend_user_basic.json` |
| 87 | GET | `http://localhost:5174` | `x-content-type-options` | `N/A` | `frontend_admin_basic.json` |
| 88 | GET | `http://localhost:5174/` | `x-content-type-options` | `N/A` | `frontend_admin_basic.json` |
| 89 | GET | `http://localhost:5174/robots.txt` | `x-content-type-options` | `N/A` | `frontend_admin_basic.json` |
| 90 | GET | `http://localhost:5174/sitemap.xml` | `x-content-type-options` | `N/A` | `frontend_admin_basic.json` |
| 91 | GET | `http://localhost:5174/src/main.jsx` | `x-content-type-options` | `N/A` | `frontend_admin_basic.json` |
| 113 | GET | `http://localhost:5173` | `x-content-type-options` | `N/A` | `frontend_admin_basic.json` |
| 114 | GET | `http://localhost:5173/` | `x-content-type-options` | `N/A` | `frontend_admin_basic.json` |
| 115 | GET | `http://localhost:5173/favicon.svg` | `x-content-type-options` | `N/A` | `frontend_admin_basic.json` |
| 116 | GET | `http://localhost:5173/robots.txt` | `x-content-type-options` | `N/A` | `frontend_admin_basic.json` |
| 117 | GET | `http://localhost:5173/sitemap.xml` | `x-content-type-options` | `N/A` | `frontend_admin_basic.json` |
| 144 | GET | `http://localhost:3000/api/products?search=` | `x-content-type-options` | `N/A` | `frontend_admin_basic.json` |
| 145 | GET | `http://localhost:3000/api/products/1` | `x-content-type-options` | `N/A` | `frontend_admin_basic.json` |
| 146 | GET | `http://localhost:3000/api/products/2` | `x-content-type-options` | `N/A` | `frontend_admin_basic.json` |
| 147 | GET | `http://localhost:3000/api/users/me` | `x-content-type-options` | `N/A` | `frontend_admin_basic.json` |
| 148 | POST | `http://localhost:3000/api/login` | `x-content-type-options` | `N/A` | `frontend_admin_basic.json` |

Bằng chứng request/response runtime đại diện:
### Endpoint 15: GET http://localhost:3000/api/users/me

Request:
```http
GET http://localhost:3000/api/users/me HTTP/1.1
host: localhost:3000
User-Agent: Python-urllib/3.14
Connection: close
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDkwNzV9.mOzLCI5uoLpBGWGMZ2PY7Y00zv3jSMAC2u4oQUHcVhc
```

Request body:
```text
[Không có request body]
```

Response:
```http
HTTP/1.1 200 OK
X-Powered-By: Express
Access-Control-Allow-Origin: *
Content-Type: application/json; charset=utf-8
Content-Length: 184
ETag: W/"b8-jiz57PnCcXs0o7g11CVR0uf+SKE"
Date: Wed, 22 Jul 2026 08:31:15 GMT
Connection: close
```

Response body excerpt:
```text
{"id":2,"name":"Test User","email":"test@eshop.com","password":"Test1234!","role":"user","login_attempts":0,"locked_until":null,"reset_token":null,"shipping_address":null,"phone":null}
```

### Endpoint 16: POST http://localhost:3000/api/login

Request:
```http
POST http://localhost:3000/api/login HTTP/1.1
Content-Length: 52
host: localhost:3000
User-Agent: Python-urllib/3.14
Content-Type: application/json
Connection: close
```

Request body:
```text
{"email": "test@eshop.com", "password": "Test1234!"}
```

Response:
```http
HTTP/1.1 200 OK
X-Powered-By: Express
Access-Control-Allow-Origin: *
Content-Type: application/json; charset=utf-8
Content-Length: 366
ETag: W/"16e-sNg9siE/HSfYKD9jdJXvPnui8jU"
Date: Wed, 22 Jul 2026 08:31:15 GMT
Connection: close
```

Response body excerpt:
```text
{"message":"Login successful","token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDkwNzV9.mOzLCI5uoLpBGWGMZ2PY7Y00zv3jSMAC2u4oQUHcVhc","user":{"id":2,"name":"Test User","email":"test@eshop.com","password":"Test1234!","role":"user","login_attempts":0,"locked_until":null,"reset_token":null,"shipping_address":null,"phone":null}}
```

### Endpoint 35: GET http://localhost:5173

Request:
```http
GET http://localhost:5173 HTTP/1.1
host: localhost:5173
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36
pragma: no-cache
cache-control: no-cache
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDk1NzF9.6xPB8cUE63QhefuiiRzG56zhdFE5lbB-b7dUFPwWED0
```

Request body:
```text
[Không có request body]
```

Response:
```http
HTTP/1.1 200 OK
Vary: Origin
Content-Type: text/html
Cache-Control: no-cache
Etag: W/"26b-Z6hN2DmQRHNqdtv4bv5lcx2QtJk"
Date: Wed, 22 Jul 2026 08:39:33 GMT
Connection: keep-alive
Keep-Alive: timeout=5
Content-Length: 619
```

Response body excerpt:
```text
<!doctype html>
<html lang="en">
  <head>
    <script type="module">import { injectIntoGlobalHook } from "/@react-refresh";
injectIntoGlobalHook(window);
window.$RefreshReg$ = () => {};
window.$RefreshSig$ = () => (type) => type;</script>

    <script type="module" src="/@vite/client"></script>

    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>frontend-web</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
```

...[24 endpoint còn lại được liệt kê trong bảng endpoint]

Mô tả ZAP:
The Anti-MIME-Sniffing header X-Content-Type-Options was not set to 'nosniff'. This allows older versions of Internet Explorer and Chrome to perform MIME-sniffing on the response body, potentially causing the response body to be interpreted and displayed as a content type other than the declared content type. Current (early 2014) and legacy versions of Firefox will use the declared content type (if one is set), rather than performing MIME-sniffing.

Khuyến nghị ZAP:
Ensure that the application/web server sets the Content-Type header appropriately, and that it sets the X-Content-Type-Options header to 'nosniff' for all web pages.If possible, ensure that the end user uses a standards-compliant and modern web browser that does not perform MIME-sniffing at all, or that can be directed by the web application/web server to not perform MIME-sniffing.

Tham khảo:
https://learn.microsoft.com/en-us/previous-versions/windows/internet-explorer/ie-developer/compatibility/gg622941(v=vs.85)https://owasp.org/www-community/Security_Headers

Ngữ cảnh runtime cho triage động:
- ZAP là DAST: phân loại dựa trên request/response runtime mà scanner quan sát được.
- ZAP không chỉ ra dòng code. Không suy đoán root cause trong code nếu evidence HTTP chưa đủ.
- True Positive: runtime evidence cho thấy cấu hình/hành vi lỗi tồn tại trên endpoint được quét.
- False Positive: request/response cho thấy alert không áp dụng trong ngữ cảnh này hoặc là endpoint ngoài phạm vi.
- Needs Human Review: evidence thiếu auth context, thiếu business impact, hoặc chỉ là informational signal.
- Với alert Informational, chỉ nâng mức nghiêm trọng nếu response cho thấy dữ liệu nhạy cảm hoặc hành vi có thể khai thác.
- Với endpoint localhost/lab, vẫn đánh giá theo hành vi quan sát được nhưng ghi rõ cần xác nhận môi trường deploy.

Hãy trả lời bằng Markdown với các mục:
1. Phân loại: True Positive / False Positive / Needs Human Review.
2. Lý do phân loại dựa trên runtime evidence của cả nhóm endpoint.
3. Tác động thực tế trong bối cảnh EShop.
4. Cách khắc phục cụ thể ở cấp cấu hình/root cause.
5. Ghi chú tester cần kiểm tra thêm nếu chưa đủ context.
