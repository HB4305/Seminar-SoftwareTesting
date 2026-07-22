Tôi dùng OWASP ZAP (DAST) để quét runtime của ứng dụng EShop và phát hiện một nhóm alert bảo mật cùng loại.
Bạn hãy đóng vai trò là chuyên gia bảo mật ứng dụng để triage alert này ở cấp nhóm, không lặp lại phân tích riêng cho từng endpoint nếu cùng root cause.
Hãy trả lời hoàn toàn bằng tiếng Việt, trừ các thuật ngữ chuẩn như True Positive, False Positive, Needs Human Review, CWE, WASC, OWASP, HTTP, header, payload.

Thông tin kỹ thuật:
- Mã alert: ZAP-003
- Alert name: Server Leaks Information via "X-Powered-By" HTTP Response Header Field(s)
- Plugin ID: 10037
- Alert Ref: 10037
- Source JSON: backend_basic.json, frontend_admin_basic.json, frontend_user_basic.json
- Site: http://localhost:3000
- Số endpoint/request instance bị ảnh hưởng: 15
- Risk: Low
- Confidence: Medium
- CWE: CWE-497
- WASC: WASC-13
- Tags: OWASP_2021_A01, WSTG-v42-INFO-08, POLICY_QA_STD, POLICY_PENTEST, SYSTEMIC, OWASP_2017_A03, OWASP_2025_A01, CWE-497

Danh sách endpoint bị ảnh hưởng:
| # | Method | URL | Param | Evidence | Source JSON |
|---|---|---|---|---|---|
| 10 | GET | `http://localhost:3000` | `N/A` | `X-Powered-By: Express` | `backend_basic.json` |
| 11 | GET | `http://localhost:3000/` | `N/A` | `X-Powered-By: Express` | `backend_basic.json` |
| 12 | GET | `http://localhost:3000/api/users/me` | `N/A` | `X-Powered-By: Express` | `backend_basic.json` |
| 13 | GET | `http://localhost:3000/robots.txt` | `N/A` | `X-Powered-By: Express` | `backend_basic.json` |
| 14 | POST | `http://localhost:3000/api/login` | `N/A` | `X-Powered-By: Express` | `backend_basic.json` |
| 61 | GET | `http://localhost:3000` | `N/A` | `X-Powered-By: Express` | `frontend_user_basic.json` |
| 62 | GET | `http://localhost:3000/` | `N/A` | `X-Powered-By: Express` | `frontend_user_basic.json` |
| 63 | GET | `http://localhost:3000/api/users/me` | `N/A` | `X-Powered-By: Express` | `frontend_user_basic.json` |
| 64 | GET | `http://localhost:3000/robots.txt` | `N/A` | `X-Powered-By: Express` | `frontend_user_basic.json` |
| 65 | POST | `http://localhost:3000/api/login` | `N/A` | `X-Powered-By: Express` | `frontend_user_basic.json` |
| 139 | GET | `http://localhost:3000` | `N/A` | `X-Powered-By: Express` | `frontend_admin_basic.json` |
| 140 | GET | `http://localhost:3000/` | `N/A` | `X-Powered-By: Express` | `frontend_admin_basic.json` |
| 141 | GET | `http://localhost:3000/api/users/me` | `N/A` | `X-Powered-By: Express` | `frontend_admin_basic.json` |
| 142 | GET | `http://localhost:3000/robots.txt` | `N/A` | `X-Powered-By: Express` | `frontend_admin_basic.json` |
| 143 | POST | `http://localhost:3000/api/login` | `N/A` | `X-Powered-By: Express` | `frontend_admin_basic.json` |

Bằng chứng request/response runtime đại diện:
### Endpoint 10: GET http://localhost:3000

Request:
```http
GET http://localhost:3000 HTTP/1.1
host: localhost:3000
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36
pragma: no-cache
cache-control: no-cache
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDkwNzV9.mOzLCI5uoLpBGWGMZ2PY7Y00zv3jSMAC2u4oQUHcVhc
```

Request body:
```text
[Không có request body]
```

Response:
```http
HTTP/1.1 404 Not Found
X-Powered-By: Express
Access-Control-Allow-Origin: *
Content-Security-Policy: default-src 'none'
X-Content-Type-Options: nosniff
Content-Type: text/html; charset=utf-8
Content-Length: 139
Date: Wed, 22 Jul 2026 08:31:18 GMT
Connection: keep-alive
Keep-Alive: timeout=5
```

Response body excerpt:
```text
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Error</title>
</head>
<body>
<pre>Cannot GET /</pre>
</body>
</html>
```

### Endpoint 11: GET http://localhost:3000/

Request:
```http
GET http://localhost:3000/ HTTP/1.1
host: localhost:3000
User-Agent: python-requests/2.32.5
Accept: */*
Connection: keep-alive
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDkwNzV9.mOzLCI5uoLpBGWGMZ2PY7Y00zv3jSMAC2u4oQUHcVhc
```

Request body:
```text
[Không có request body]
```

Response:
```http
HTTP/1.1 404 Not Found
X-Powered-By: Express
Access-Control-Allow-Origin: *
Content-Security-Policy: default-src 'none'
X-Content-Type-Options: nosniff
Content-Type: text/html; charset=utf-8
Content-Length: 139
Date: Wed, 22 Jul 2026 08:31:15 GMT
Connection: keep-alive
Keep-Alive: timeout=5
```

Response body excerpt:
```text
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Error</title>
</head>
<body>
<pre>Cannot GET /</pre>
</body>
</html>
```

### Endpoint 12: GET http://localhost:3000/api/users/me

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

...[12 endpoint còn lại được liệt kê trong bảng endpoint]

Mô tả ZAP:
The web/application server is leaking information via one or more "X-Powered-By" HTTP response headers. Access to such information may facilitate attackers identifying other frameworks/components your web application is reliant upon and the vulnerabilities such components may be subject to.

Khuyến nghị ZAP:
Ensure that your web server, application server, load balancer, etc. is configured to suppress "X-Powered-By" headers.

Tham khảo:
https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/01-Information_Gathering/08-Fingerprint_Web_Application_Frameworkhttps://www.troyhunt.com/shhh-dont-let-your-response-headers/

Ngữ cảnh runtime cho triage động:
- ZAP là DAST: phân loại dựa trên request/response runtime mà scanner quan sát được.
- ZAP không chỉ ra dòng code. Không suy đoán root cause trong code nếu evidence HTTP chưa đủ.
- True Positive: runtime evidence cho thấy cấu hình/hành vi lỗi tồn tại trên endpoint được quét.
- False Positive: request/response cho thấy alert không áp dụng trong ngữ cảnh này hoặc là endpoint ngoài phạm vi.
- Needs Human Review: evidence thiếu auth context, thiếu business impact, hoặc chỉ là informational signal.
- Với alert Informational, chỉ nâng mức nghiêm trọng nếu response cho thấy dữ liệu nhạy cảm hoặc hành vi có thể khai thác.
- Với endpoint localhost/lab, vẫn đánh giá theo hành vi quan sát được nhưng ghi rõ cần xác nhận môi trường deploy.
- Evidence của ZAP phải được đối chiếu trực tiếp với response header/body trong report.

Hãy trả lời bằng Markdown với các mục:
1. Phân loại: True Positive / False Positive / Needs Human Review.
2. Lý do phân loại dựa trên runtime evidence của cả nhóm endpoint.
3. Tác động thực tế trong bối cảnh EShop.
4. Cách khắc phục cụ thể ở cấp cấu hình/root cause.
5. Ghi chú tester cần kiểm tra thêm nếu chưa đủ context.
