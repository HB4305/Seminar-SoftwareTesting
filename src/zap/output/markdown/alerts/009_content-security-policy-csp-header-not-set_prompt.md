Tôi dùng OWASP ZAP (DAST) để quét runtime của ứng dụng EShop và phát hiện một nhóm alert bảo mật cùng loại.
Bạn hãy đóng vai trò là chuyên gia bảo mật ứng dụng để triage alert này ở cấp nhóm, không lặp lại phân tích riêng cho từng endpoint nếu cùng root cause.
Hãy trả lời hoàn toàn bằng tiếng Việt, trừ các thuật ngữ chuẩn như True Positive, False Positive, Needs Human Review, CWE, WASC, OWASP, HTTP, header, payload.

Thông tin kỹ thuật:
- Mã alert: ZAP-009
- Alert name: Content Security Policy (CSP) Header Not Set
- Plugin ID: 10038
- Alert Ref: 10038-1
- Source JSON: frontend_admin_basic.json, frontend_user_basic.json
- Site: http://localhost:5173, http://localhost:5174
- Số endpoint/request instance bị ảnh hưởng: 14
- Risk: Medium
- Confidence: High
- CWE: CWE-693
- WASC: WASC-15
- Tags: OWASP_2021_A05, POLICY_QA_STD, POLICY_PENTEST, SYSTEMIC, CWE-693, OWASP_2017_A06, OWASP_2025_A02

Danh sách endpoint bị ảnh hưởng:
| # | Method | URL | Param | Evidence | Source JSON |
|---|---|---|---|---|---|
| 24 | GET | `http://localhost:5173` | `N/A` | `N/A` | `frontend_user_basic.json` |
| 25 | GET | `http://localhost:5173/` | `N/A` | `N/A` | `frontend_user_basic.json` |
| 26 | GET | `http://localhost:5173/forgot-password` | `N/A` | `N/A` | `frontend_user_basic.json` |
| 27 | GET | `http://localhost:5173/robots.txt` | `N/A` | `N/A` | `frontend_user_basic.json` |
| 28 | GET | `http://localhost:5173/sitemap.xml` | `N/A` | `N/A` | `frontend_user_basic.json` |
| 78 | GET | `http://localhost:5174` | `N/A` | `N/A` | `frontend_admin_basic.json` |
| 79 | GET | `http://localhost:5174/` | `N/A` | `N/A` | `frontend_admin_basic.json` |
| 80 | GET | `http://localhost:5174/robots.txt` | `N/A` | `N/A` | `frontend_admin_basic.json` |
| 81 | GET | `http://localhost:5174/sitemap.xml` | `N/A` | `N/A` | `frontend_admin_basic.json` |
| 102 | GET | `http://localhost:5173` | `N/A` | `N/A` | `frontend_admin_basic.json` |
| 103 | GET | `http://localhost:5173/` | `N/A` | `N/A` | `frontend_admin_basic.json` |
| 104 | GET | `http://localhost:5173/forgot-password` | `N/A` | `N/A` | `frontend_admin_basic.json` |
| 105 | GET | `http://localhost:5173/robots.txt` | `N/A` | `N/A` | `frontend_admin_basic.json` |
| 106 | GET | `http://localhost:5173/sitemap.xml` | `N/A` | `N/A` | `frontend_admin_basic.json` |

Bằng chứng request/response runtime đại diện:
### Endpoint 24: GET http://localhost:5173

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

### Endpoint 25: GET http://localhost:5173/

Request:
```http
GET http://localhost:5173/ HTTP/1.1
host: localhost:5173
User-Agent: python-requests/2.32.5
Accept: */*
Connection: keep-alive
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
Date: Wed, 22 Jul 2026 08:39:31 GMT
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

### Endpoint 26: GET http://localhost:5173/forgot-password

Request:
```http
GET http://localhost:5173/forgot-password HTTP/1.1
host: localhost:5173
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Connection: keep-alive
Referer: http://localhost:5173/login
Upgrade-Insecure-Requests: 1
Priority: u=0, i
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
Date: Wed, 22 Jul 2026 08:39:57 GMT
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

...[11 endpoint còn lại được liệt kê trong bảng endpoint]

Mô tả ZAP:
Content Security Policy (CSP) is an added layer of security that helps to detect and mitigate certain types of attacks, including Cross Site Scripting (XSS) and data injection attacks. These attacks are used for everything from data theft to site defacement or distribution of malware. CSP provides a set of standard HTTP headers that allow website owners to declare approved sources of content that browsers should be allowed to load on that page — covered types are JavaScript, CSS, HTML frames, fonts, images and embeddable objects such as Java applets, ActiveX, audio and video files.

Khuyến nghị ZAP:
Ensure that your web server, application server, load balancer, etc. is configured to set the Content-Security-Policy header.

Tham khảo:
https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSPhttps://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.htmlhttps://www.w3.org/TR/CSP/https://w3c.github.io/webappsec-csp/https://web.dev/articles/csphttps://caniuse.com/#feat=contentsecuritypolicyhttps://content-security-policy.com/

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
