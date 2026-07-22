Tôi dùng OWASP ZAP (DAST) để quét runtime của ứng dụng EShop và phát hiện một nhóm alert bảo mật cùng loại.
Bạn hãy đóng vai trò là chuyên gia bảo mật ứng dụng để triage alert này ở cấp nhóm, không lặp lại phân tích riêng cho từng endpoint nếu cùng root cause.
Hãy trả lời hoàn toàn bằng tiếng Việt, trừ các thuật ngữ chuẩn như True Positive, False Positive, Needs Human Review, CWE, WASC, OWASP, HTTP, header, payload.

Thông tin kỹ thuật:
- Mã alert: ZAP-001
- Alert name: CSP: Failure to Define Directive with No Fallback
- Plugin ID: 10055
- Alert Ref: 10055-13
- Source JSON: backend_basic.json, frontend_admin_basic.json, frontend_user_basic.json
- Site: http://localhost:3000
- Số endpoint/request instance bị ảnh hưởng: 15
- Risk: Medium
- Confidence: High
- CWE: CWE-693
- WASC: WASC-15
- Tags: OWASP_2021_A05, POLICY_QA_STD, POLICY_PENTEST, SYSTEMIC, CWE-693, OWASP_2017_A06, OWASP_2025_A02, POLICY_DEV_STD

Danh sách endpoint bị ảnh hưởng:
| # | Method | URL | Param | Evidence | Source JSON |
|---|---|---|---|---|---|
| 1 | GET | `http://localhost:3000` | `Content-Security-Policy` | `default-src 'none'` | `backend_basic.json` |
| 2 | GET | `http://localhost:3000/` | `Content-Security-Policy` | `default-src 'none'` | `backend_basic.json` |
| 3 | GET | `http://localhost:3000/api` | `Content-Security-Policy` | `default-src 'none'` | `backend_basic.json` |
| 4 | GET | `http://localhost:3000/robots.txt` | `Content-Security-Policy` | `default-src 'none'` | `backend_basic.json` |
| 5 | GET | `http://localhost:3000/sitemap.xml` | `Content-Security-Policy` | `default-src 'none'` | `backend_basic.json` |
| 52 | GET | `http://localhost:3000` | `Content-Security-Policy` | `default-src 'none'` | `frontend_user_basic.json` |
| 53 | GET | `http://localhost:3000/` | `Content-Security-Policy` | `default-src 'none'` | `frontend_user_basic.json` |
| 54 | GET | `http://localhost:3000/api` | `Content-Security-Policy` | `default-src 'none'` | `frontend_user_basic.json` |
| 55 | GET | `http://localhost:3000/robots.txt` | `Content-Security-Policy` | `default-src 'none'` | `frontend_user_basic.json` |
| 56 | GET | `http://localhost:3000/sitemap.xml` | `Content-Security-Policy` | `default-src 'none'` | `frontend_user_basic.json` |
| 130 | GET | `http://localhost:3000` | `Content-Security-Policy` | `default-src 'none'` | `frontend_admin_basic.json` |
| 131 | GET | `http://localhost:3000/` | `Content-Security-Policy` | `default-src 'none'` | `frontend_admin_basic.json` |
| 132 | GET | `http://localhost:3000/api` | `Content-Security-Policy` | `default-src 'none'` | `frontend_admin_basic.json` |
| 133 | GET | `http://localhost:3000/robots.txt` | `Content-Security-Policy` | `default-src 'none'` | `frontend_admin_basic.json` |
| 134 | GET | `http://localhost:3000/sitemap.xml` | `Content-Security-Policy` | `default-src 'none'` | `frontend_admin_basic.json` |

Bằng chứng request/response runtime đại diện:
### Endpoint 1: GET http://localhost:3000

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

### Endpoint 2: GET http://localhost:3000/

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

### Endpoint 3: GET http://localhost:3000/api

Request:
```http
GET http://localhost:3000/api HTTP/1.1
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
Content-Length: 142
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
<pre>Cannot GET /api</pre>
</body>
</html>
```

...[12 endpoint còn lại được liệt kê trong bảng endpoint]

Mô tả ZAP:
The Content Security Policy fails to define one of the directives that has no fallback. Missing/excluding them is the same as allowing anything.

Khuyến nghị ZAP:
Ensure that your web server, application server, load balancer, etc. is properly configured to set the Content-Security-Policy header.

Tham khảo:
https://www.w3.org/TR/CSP/https://caniuse.com/#search=content+security+policyhttps://content-security-policy.com/https://github.com/HtmlUnit/htmlunit-csphttps://web.dev/articles/csp#resource-options

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
