# Danh sách test case kiểm chứng ZAP

Tài liệu này tổng hợp test case kiểm chứng cho các alert ZAP theo từng request runtime. Mỗi entry trỏ về alert gốc trong `zap_triage_report.md`.

## TC-ZAP-001

- Alert liên quan: ZAP-001
- Mục tiêu test: Kiểm chứng alert `CSP: Failure to Define Directive with No Fallback` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `backend_basic.json`

### Input

```http
GET http://localhost:3000
```

Headers:
```http
GET http://localhost:3000 HTTP/1.1
host: localhost:3000
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36
pragma: no-cache
cache-control: no-cache
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDkwNzV9.mOzLCI5uoLpBGWGMZ2PY7Y00zv3jSMAC2u4oQUHcVhc
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `default-src 'none'` hoặc hành vi runtime vẫn khớp alert `CSP: Failure to Define Directive with No Fallback`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-002

- Alert liên quan: ZAP-001
- Mục tiêu test: Kiểm chứng alert `CSP: Failure to Define Directive with No Fallback` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `backend_basic.json`

### Input

```http
GET http://localhost:3000/
```

Headers:
```http
GET http://localhost:3000/ HTTP/1.1
host: localhost:3000
User-Agent: python-requests/2.32.5
Accept: */*
Connection: keep-alive
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDkwNzV9.mOzLCI5uoLpBGWGMZ2PY7Y00zv3jSMAC2u4oQUHcVhc
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `default-src 'none'` hoặc hành vi runtime vẫn khớp alert `CSP: Failure to Define Directive with No Fallback`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-003

- Alert liên quan: ZAP-001
- Mục tiêu test: Kiểm chứng alert `CSP: Failure to Define Directive with No Fallback` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `backend_basic.json`

### Input

```http
GET http://localhost:3000/api
```

Headers:
```http
GET http://localhost:3000/api HTTP/1.1
host: localhost:3000
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36
pragma: no-cache
cache-control: no-cache
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDkwNzV9.mOzLCI5uoLpBGWGMZ2PY7Y00zv3jSMAC2u4oQUHcVhc
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `default-src 'none'` hoặc hành vi runtime vẫn khớp alert `CSP: Failure to Define Directive with No Fallback`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-004

- Alert liên quan: ZAP-001
- Mục tiêu test: Kiểm chứng alert `CSP: Failure to Define Directive with No Fallback` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `backend_basic.json`

### Input

```http
GET http://localhost:3000/robots.txt
```

Headers:
```http
GET http://localhost:3000/robots.txt HTTP/1.1
host: localhost:3000
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36
pragma: no-cache
cache-control: no-cache
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDkwNzV9.mOzLCI5uoLpBGWGMZ2PY7Y00zv3jSMAC2u4oQUHcVhc
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `default-src 'none'` hoặc hành vi runtime vẫn khớp alert `CSP: Failure to Define Directive with No Fallback`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-005

- Alert liên quan: ZAP-001
- Mục tiêu test: Kiểm chứng alert `CSP: Failure to Define Directive with No Fallback` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `backend_basic.json`

### Input

```http
GET http://localhost:3000/sitemap.xml
```

Headers:
```http
GET http://localhost:3000/sitemap.xml HTTP/1.1
host: localhost:3000
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36
pragma: no-cache
cache-control: no-cache
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDkwNzV9.mOzLCI5uoLpBGWGMZ2PY7Y00zv3jSMAC2u4oQUHcVhc
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `default-src 'none'` hoặc hành vi runtime vẫn khớp alert `CSP: Failure to Define Directive with No Fallback`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-006

- Alert liên quan: ZAP-002
- Mục tiêu test: Kiểm chứng alert `Cross-Domain Misconfiguration` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `backend_basic.json`

### Input

```http
GET http://localhost:3000
```

Headers:
```http
GET http://localhost:3000 HTTP/1.1
host: localhost:3000
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36
pragma: no-cache
cache-control: no-cache
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDkwNzV9.mOzLCI5uoLpBGWGMZ2PY7Y00zv3jSMAC2u4oQUHcVhc
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `Access-Control-Allow-Origin: *` hoặc hành vi runtime vẫn khớp alert `Cross-Domain Misconfiguration`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-007

- Alert liên quan: ZAP-002
- Mục tiêu test: Kiểm chứng alert `Cross-Domain Misconfiguration` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `backend_basic.json`

### Input

```http
GET http://localhost:3000/
```

Headers:
```http
GET http://localhost:3000/ HTTP/1.1
host: localhost:3000
User-Agent: python-requests/2.32.5
Accept: */*
Connection: keep-alive
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDkwNzV9.mOzLCI5uoLpBGWGMZ2PY7Y00zv3jSMAC2u4oQUHcVhc
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `Access-Control-Allow-Origin: *` hoặc hành vi runtime vẫn khớp alert `Cross-Domain Misconfiguration`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-008

- Alert liên quan: ZAP-002
- Mục tiêu test: Kiểm chứng alert `Cross-Domain Misconfiguration` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `backend_basic.json`

### Input

```http
GET http://localhost:3000/api/users/me
```

Headers:
```http
GET http://localhost:3000/api/users/me HTTP/1.1
host: localhost:3000
User-Agent: Python-urllib/3.14
Connection: close
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDkwNzV9.mOzLCI5uoLpBGWGMZ2PY7Y00zv3jSMAC2u4oQUHcVhc
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `Access-Control-Allow-Origin: *` hoặc hành vi runtime vẫn khớp alert `Cross-Domain Misconfiguration`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-009

- Alert liên quan: ZAP-002
- Mục tiêu test: Kiểm chứng alert `Cross-Domain Misconfiguration` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `backend_basic.json`

### Input

```http
GET http://localhost:3000/sitemap.xml
```

Headers:
```http
GET http://localhost:3000/sitemap.xml HTTP/1.1
host: localhost:3000
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36
pragma: no-cache
cache-control: no-cache
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDkwNzV9.mOzLCI5uoLpBGWGMZ2PY7Y00zv3jSMAC2u4oQUHcVhc
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `Access-Control-Allow-Origin: *` hoặc hành vi runtime vẫn khớp alert `Cross-Domain Misconfiguration`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-010

- Alert liên quan: ZAP-003
- Mục tiêu test: Kiểm chứng alert `Server Leaks Information via "X-Powered-By" HTTP Response Header Field(s)` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `backend_basic.json`

### Input

```http
GET http://localhost:3000
```

Headers:
```http
GET http://localhost:3000 HTTP/1.1
host: localhost:3000
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36
pragma: no-cache
cache-control: no-cache
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDkwNzV9.mOzLCI5uoLpBGWGMZ2PY7Y00zv3jSMAC2u4oQUHcVhc
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `X-Powered-By: Express` hoặc hành vi runtime vẫn khớp alert `Server Leaks Information via "X-Powered-By" HTTP Response Header Field(s)`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-011

- Alert liên quan: ZAP-003
- Mục tiêu test: Kiểm chứng alert `Server Leaks Information via "X-Powered-By" HTTP Response Header Field(s)` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `backend_basic.json`

### Input

```http
GET http://localhost:3000/
```

Headers:
```http
GET http://localhost:3000/ HTTP/1.1
host: localhost:3000
User-Agent: python-requests/2.32.5
Accept: */*
Connection: keep-alive
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDkwNzV9.mOzLCI5uoLpBGWGMZ2PY7Y00zv3jSMAC2u4oQUHcVhc
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `X-Powered-By: Express` hoặc hành vi runtime vẫn khớp alert `Server Leaks Information via "X-Powered-By" HTTP Response Header Field(s)`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-012

- Alert liên quan: ZAP-003
- Mục tiêu test: Kiểm chứng alert `Server Leaks Information via "X-Powered-By" HTTP Response Header Field(s)` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `backend_basic.json`

### Input

```http
GET http://localhost:3000/api/users/me
```

Headers:
```http
GET http://localhost:3000/api/users/me HTTP/1.1
host: localhost:3000
User-Agent: Python-urllib/3.14
Connection: close
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDkwNzV9.mOzLCI5uoLpBGWGMZ2PY7Y00zv3jSMAC2u4oQUHcVhc
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `X-Powered-By: Express` hoặc hành vi runtime vẫn khớp alert `Server Leaks Information via "X-Powered-By" HTTP Response Header Field(s)`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-013

- Alert liên quan: ZAP-003
- Mục tiêu test: Kiểm chứng alert `Server Leaks Information via "X-Powered-By" HTTP Response Header Field(s)` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `backend_basic.json`

### Input

```http
GET http://localhost:3000/robots.txt
```

Headers:
```http
GET http://localhost:3000/robots.txt HTTP/1.1
host: localhost:3000
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36
pragma: no-cache
cache-control: no-cache
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDkwNzV9.mOzLCI5uoLpBGWGMZ2PY7Y00zv3jSMAC2u4oQUHcVhc
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `X-Powered-By: Express` hoặc hành vi runtime vẫn khớp alert `Server Leaks Information via "X-Powered-By" HTTP Response Header Field(s)`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-014

- Alert liên quan: ZAP-003
- Mục tiêu test: Kiểm chứng alert `Server Leaks Information via "X-Powered-By" HTTP Response Header Field(s)` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `backend_basic.json`

### Input

```http
POST http://localhost:3000/api/login
```

Headers:
```http
POST http://localhost:3000/api/login HTTP/1.1
Content-Length: 52
host: localhost:3000
User-Agent: Python-urllib/3.14
Content-Type: application/json
Connection: close
```

Payload:
```json
{"email": "test@eshop.com", "password": "Test1234!"}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `X-Powered-By: Express` hoặc hành vi runtime vẫn khớp alert `Server Leaks Information via "X-Powered-By" HTTP Response Header Field(s)`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-015

- Alert liên quan: ZAP-004
- Mục tiêu test: Kiểm chứng alert `X-Content-Type-Options Header Missing` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `backend_basic.json`

### Input

```http
GET http://localhost:3000/api/users/me
```

Headers:
```http
GET http://localhost:3000/api/users/me HTTP/1.1
host: localhost:3000
User-Agent: Python-urllib/3.14
Connection: close
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDkwNzV9.mOzLCI5uoLpBGWGMZ2PY7Y00zv3jSMAC2u4oQUHcVhc
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `N/A` hoặc hành vi runtime vẫn khớp alert `X-Content-Type-Options Header Missing`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-016

- Alert liên quan: ZAP-004
- Mục tiêu test: Kiểm chứng alert `X-Content-Type-Options Header Missing` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `backend_basic.json`

### Input

```http
POST http://localhost:3000/api/login
```

Headers:
```http
POST http://localhost:3000/api/login HTTP/1.1
Content-Length: 52
host: localhost:3000
User-Agent: Python-urllib/3.14
Content-Type: application/json
Connection: close
```

Payload:
```json
{"email": "test@eshop.com", "password": "Test1234!"}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `N/A` hoặc hành vi runtime vẫn khớp alert `X-Content-Type-Options Header Missing`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-017

- Alert liên quan: ZAP-005
- Mục tiêu test: Kiểm chứng alert `Authentication Request Identified` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `backend_basic.json`

### Input

```http
POST http://localhost:3000/api/login
```

Headers:
```http
POST http://localhost:3000/api/login HTTP/1.1
Content-Length: 52
host: localhost:3000
User-Agent: Python-urllib/3.14
Content-Type: application/json
Connection: close
```

Payload:
```json
{"email": "test@eshop.com", "password": "Test1234!"}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `password` hoặc hành vi runtime vẫn khớp alert `Authentication Request Identified`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-018

- Alert liên quan: ZAP-006
- Mục tiêu test: Kiểm chứng alert `Session Management Response Identified` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `backend_basic.json`

### Input

```http
POST http://localhost:3000/api/login
```

Headers:
```http
POST http://localhost:3000/api/login HTTP/1.1
Content-Length: 52
host: localhost:3000
User-Agent: Python-urllib/3.14
Content-Type: application/json
Connection: close
```

Payload:
```json
{"email": "test@eshop.com", "password": "Test1234!"}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `token` hoặc hành vi runtime vẫn khớp alert `Session Management Response Identified`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-019

- Alert liên quan: ZAP-006
- Mục tiêu test: Kiểm chứng alert `Session Management Response Identified` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `backend_basic.json`

### Input

```http
POST http://localhost:3000/api/login
```

Headers:
```http
POST http://localhost:3000/api/login HTTP/1.1
Content-Length: 52
host: localhost:3000
User-Agent: Python-urllib/3.14
Content-Type: application/json
Connection: close
```

Payload:
```json
{"email": "test@eshop.com", "password": "Test1234!"}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `token` hoặc hành vi runtime vẫn khớp alert `Session Management Response Identified`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-020

- Alert liên quan: ZAP-007
- Mục tiêu test: Kiểm chứng alert `User Agent Fuzzer` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `backend_basic.json`

### Input

```http
GET http://localhost:3000/api/users/me
```

Headers:
```http
GET http://localhost:3000/api/users/me HTTP/1.1
host: localhost:3000
user-agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)
pragma: no-cache
cache-control: no-cache
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDkwNzV9.mOzLCI5uoLpBGWGMZ2PY7Y00zv3jSMAC2u4oQUHcVhc
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `N/A` hoặc hành vi runtime vẫn khớp alert `User Agent Fuzzer`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-021

- Alert liên quan: ZAP-007
- Mục tiêu test: Kiểm chứng alert `User Agent Fuzzer` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `backend_basic.json`

### Input

```http
GET http://localhost:3000/api/users/me
```

Headers:
```http
GET http://localhost:3000/api/users/me HTTP/1.1
host: localhost:3000
user-agent: Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1)
pragma: no-cache
cache-control: no-cache
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDkwNzV9.mOzLCI5uoLpBGWGMZ2PY7Y00zv3jSMAC2u4oQUHcVhc
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `N/A` hoặc hành vi runtime vẫn khớp alert `User Agent Fuzzer`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-022

- Alert liên quan: ZAP-007
- Mục tiêu test: Kiểm chứng alert `User Agent Fuzzer` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `backend_basic.json`

### Input

```http
POST http://localhost:3000/api/login
```

Headers:
```http
POST http://localhost:3000/api/login HTTP/1.1
Content-Length: 52
host: localhost:3000
user-agent: Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1)
Content-Type: application/json
Connection: close
```

Payload:
```json
{"email": "test@eshop.com", "password": "Test1234!"}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `N/A` hoặc hành vi runtime vẫn khớp alert `User Agent Fuzzer`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-023

- Alert liên quan: ZAP-008
- Mục tiêu test: Kiểm chứng alert `Path Traversal` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_user_basic.json`

### Input

```http
GET http://localhost:5173/node_modules/.vite/deps/chunk-CYJPkc-J.js?v=%2Fchunk-CYJPkc-J.js
```

Headers:
```http
GET http://localhost:5173/node_modules/.vite/deps/chunk-CYJPkc-J.js?v=%2Fchunk-CYJPkc-J.js HTTP/1.1
host: localhost:5173
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Connection: keep-alive
Referer: http://localhost:5173/node_modules/.vite/deps/react.js?v=82fd3d9d
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDk1NzF9.6xPB8cUE63QhefuiiRzG56zhdFE5lbB-b7dUFPwWED0
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `N/A` hoặc hành vi runtime vẫn khớp alert `Path Traversal`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-024

- Alert liên quan: ZAP-009
- Mục tiêu test: Kiểm chứng alert `Content Security Policy (CSP) Header Not Set` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_user_basic.json`

### Input

```http
GET http://localhost:5173
```

Headers:
```http
GET http://localhost:5173 HTTP/1.1
host: localhost:5173
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36
pragma: no-cache
cache-control: no-cache
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDk1NzF9.6xPB8cUE63QhefuiiRzG56zhdFE5lbB-b7dUFPwWED0
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `N/A` hoặc hành vi runtime vẫn khớp alert `Content Security Policy (CSP) Header Not Set`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-025

- Alert liên quan: ZAP-009
- Mục tiêu test: Kiểm chứng alert `Content Security Policy (CSP) Header Not Set` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_user_basic.json`

### Input

```http
GET http://localhost:5173/
```

Headers:
```http
GET http://localhost:5173/ HTTP/1.1
host: localhost:5173
User-Agent: python-requests/2.32.5
Accept: */*
Connection: keep-alive
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDk1NzF9.6xPB8cUE63QhefuiiRzG56zhdFE5lbB-b7dUFPwWED0
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `N/A` hoặc hành vi runtime vẫn khớp alert `Content Security Policy (CSP) Header Not Set`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-026

- Alert liên quan: ZAP-009
- Mục tiêu test: Kiểm chứng alert `Content Security Policy (CSP) Header Not Set` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_user_basic.json`

### Input

```http
GET http://localhost:5173/forgot-password
```

Headers:
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

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `N/A` hoặc hành vi runtime vẫn khớp alert `Content Security Policy (CSP) Header Not Set`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-027

- Alert liên quan: ZAP-009
- Mục tiêu test: Kiểm chứng alert `Content Security Policy (CSP) Header Not Set` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_user_basic.json`

### Input

```http
GET http://localhost:5173/robots.txt
```

Headers:
```http
GET http://localhost:5173/robots.txt HTTP/1.1
host: localhost:5173
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36
pragma: no-cache
cache-control: no-cache
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDk1NzF9.6xPB8cUE63QhefuiiRzG56zhdFE5lbB-b7dUFPwWED0
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `N/A` hoặc hành vi runtime vẫn khớp alert `Content Security Policy (CSP) Header Not Set`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-028

- Alert liên quan: ZAP-009
- Mục tiêu test: Kiểm chứng alert `Content Security Policy (CSP) Header Not Set` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_user_basic.json`

### Input

```http
GET http://localhost:5173/sitemap.xml
```

Headers:
```http
GET http://localhost:5173/sitemap.xml HTTP/1.1
host: localhost:5173
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36
pragma: no-cache
cache-control: no-cache
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDk1NzF9.6xPB8cUE63QhefuiiRzG56zhdFE5lbB-b7dUFPwWED0
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `N/A` hoặc hành vi runtime vẫn khớp alert `Content Security Policy (CSP) Header Not Set`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-029

- Alert liên quan: ZAP-010
- Mục tiêu test: Kiểm chứng alert `Missing Anti-clickjacking Header` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_user_basic.json`

### Input

```http
GET http://localhost:5173
```

Headers:
```http
GET http://localhost:5173 HTTP/1.1
host: localhost:5173
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36
pragma: no-cache
cache-control: no-cache
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDk1NzF9.6xPB8cUE63QhefuiiRzG56zhdFE5lbB-b7dUFPwWED0
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `N/A` hoặc hành vi runtime vẫn khớp alert `Missing Anti-clickjacking Header`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-030

- Alert liên quan: ZAP-010
- Mục tiêu test: Kiểm chứng alert `Missing Anti-clickjacking Header` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_user_basic.json`

### Input

```http
GET http://localhost:5173/
```

Headers:
```http
GET http://localhost:5173/ HTTP/1.1
host: localhost:5173
User-Agent: python-requests/2.32.5
Accept: */*
Connection: keep-alive
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDk1NzF9.6xPB8cUE63QhefuiiRzG56zhdFE5lbB-b7dUFPwWED0
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `N/A` hoặc hành vi runtime vẫn khớp alert `Missing Anti-clickjacking Header`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-031

- Alert liên quan: ZAP-010
- Mục tiêu test: Kiểm chứng alert `Missing Anti-clickjacking Header` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_user_basic.json`

### Input

```http
GET http://localhost:5173/forgot-password
```

Headers:
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

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `N/A` hoặc hành vi runtime vẫn khớp alert `Missing Anti-clickjacking Header`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-032

- Alert liên quan: ZAP-010
- Mục tiêu test: Kiểm chứng alert `Missing Anti-clickjacking Header` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_user_basic.json`

### Input

```http
GET http://localhost:5173/robots.txt
```

Headers:
```http
GET http://localhost:5173/robots.txt HTTP/1.1
host: localhost:5173
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36
pragma: no-cache
cache-control: no-cache
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDk1NzF9.6xPB8cUE63QhefuiiRzG56zhdFE5lbB-b7dUFPwWED0
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `N/A` hoặc hành vi runtime vẫn khớp alert `Missing Anti-clickjacking Header`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-033

- Alert liên quan: ZAP-010
- Mục tiêu test: Kiểm chứng alert `Missing Anti-clickjacking Header` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_user_basic.json`

### Input

```http
GET http://localhost:5173/sitemap.xml
```

Headers:
```http
GET http://localhost:5173/sitemap.xml HTTP/1.1
host: localhost:5173
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36
pragma: no-cache
cache-control: no-cache
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDk1NzF9.6xPB8cUE63QhefuiiRzG56zhdFE5lbB-b7dUFPwWED0
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `N/A` hoặc hành vi runtime vẫn khớp alert `Missing Anti-clickjacking Header`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-034

- Alert liên quan: ZAP-011
- Mục tiêu test: Kiểm chứng alert `Timestamp Disclosure - Unix` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_user_basic.json`

### Input

```http
GET http://localhost:5173/node_modules/.vite/deps/react-dom_client.js?v=82fd3d9d
```

Headers:
```http
GET http://localhost:5173/node_modules/.vite/deps/react-dom_client.js?v=82fd3d9d HTTP/1.1
host: localhost:5173
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Connection: keep-alive
Referer: http://localhost:5173/src/main.jsx
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDk1NzF9.6xPB8cUE63QhefuiiRzG56zhdFE5lbB-b7dUFPwWED0
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `2080374784` hoặc hành vi runtime vẫn khớp alert `Timestamp Disclosure - Unix`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-035

- Alert liên quan: ZAP-004
- Mục tiêu test: Kiểm chứng alert `X-Content-Type-Options Header Missing` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_user_basic.json`

### Input

```http
GET http://localhost:5173
```

Headers:
```http
GET http://localhost:5173 HTTP/1.1
host: localhost:5173
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36
pragma: no-cache
cache-control: no-cache
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDk1NzF9.6xPB8cUE63QhefuiiRzG56zhdFE5lbB-b7dUFPwWED0
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `N/A` hoặc hành vi runtime vẫn khớp alert `X-Content-Type-Options Header Missing`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-036

- Alert liên quan: ZAP-004
- Mục tiêu test: Kiểm chứng alert `X-Content-Type-Options Header Missing` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_user_basic.json`

### Input

```http
GET http://localhost:5173/
```

Headers:
```http
GET http://localhost:5173/ HTTP/1.1
host: localhost:5173
User-Agent: python-requests/2.32.5
Accept: */*
Connection: keep-alive
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDk1NzF9.6xPB8cUE63QhefuiiRzG56zhdFE5lbB-b7dUFPwWED0
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `N/A` hoặc hành vi runtime vẫn khớp alert `X-Content-Type-Options Header Missing`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-037

- Alert liên quan: ZAP-004
- Mục tiêu test: Kiểm chứng alert `X-Content-Type-Options Header Missing` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_user_basic.json`

### Input

```http
GET http://localhost:5173/favicon.svg
```

Headers:
```http
GET http://localhost:5173/favicon.svg HTTP/1.1
host: localhost:5173
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36
pragma: no-cache
cache-control: no-cache
referer: http://localhost:5173
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDk1NzF9.6xPB8cUE63QhefuiiRzG56zhdFE5lbB-b7dUFPwWED0
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `N/A` hoặc hành vi runtime vẫn khớp alert `X-Content-Type-Options Header Missing`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-038

- Alert liên quan: ZAP-004
- Mục tiêu test: Kiểm chứng alert `X-Content-Type-Options Header Missing` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_user_basic.json`

### Input

```http
GET http://localhost:5173/robots.txt
```

Headers:
```http
GET http://localhost:5173/robots.txt HTTP/1.1
host: localhost:5173
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36
pragma: no-cache
cache-control: no-cache
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDk1NzF9.6xPB8cUE63QhefuiiRzG56zhdFE5lbB-b7dUFPwWED0
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `N/A` hoặc hành vi runtime vẫn khớp alert `X-Content-Type-Options Header Missing`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-039

- Alert liên quan: ZAP-004
- Mục tiêu test: Kiểm chứng alert `X-Content-Type-Options Header Missing` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_user_basic.json`

### Input

```http
GET http://localhost:5173/sitemap.xml
```

Headers:
```http
GET http://localhost:5173/sitemap.xml HTTP/1.1
host: localhost:5173
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36
pragma: no-cache
cache-control: no-cache
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDk1NzF9.6xPB8cUE63QhefuiiRzG56zhdFE5lbB-b7dUFPwWED0
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `N/A` hoặc hành vi runtime vẫn khớp alert `X-Content-Type-Options Header Missing`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-040

- Alert liên quan: ZAP-012
- Mục tiêu test: Kiểm chứng alert `Information Disclosure - Sensitive Information in URL` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_user_basic.json`

### Input

```http
GET http://localhost:5173/?token=7NvYDWb8HNrK
```

Headers:
```http
GET http://localhost:5173/?token=7NvYDWb8HNrK HTTP/1.1
host: localhost:5173
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Sec-WebSocket-Version: 13
Origin: http://localhost:5173
Sec-WebSocket-Protocol: vite-hmr
Sec-WebSocket-Key: /z+7rhddK1vlqzbW2Q9bEg==
Connection: Upgrade
Pragma: no-cache
Cache-Control: no-cache
Upgrade: websocket
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDk1NzF9.6xPB8cUE63QhefuiiRzG56zhdFE5lbB-b7dUFPwWED0
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `token` hoặc hành vi runtime vẫn khớp alert `Information Disclosure - Sensitive Information in URL`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-041

- Alert liên quan: ZAP-013
- Mục tiêu test: Kiểm chứng alert `Information Disclosure - Suspicious Comments` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_user_basic.json`

### Input

```http
GET http://localhost:5173/@react-refresh
```

Headers:
```http
GET http://localhost:5173/@react-refresh HTTP/1.1
host: localhost:5173
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Connection: keep-alive
Referer: http://localhost:5173/
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDk1NzF9.6xPB8cUE63QhefuiiRzG56zhdFE5lbB-b7dUFPwWED0
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `// TODO: rename these field` hoặc hành vi runtime vẫn khớp alert `Information Disclosure - Suspicious Comments`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-042

- Alert liên quan: ZAP-013
- Mục tiêu test: Kiểm chứng alert `Information Disclosure - Suspicious Comments` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_user_basic.json`

### Input

```http
GET http://localhost:5173/@react-refresh
```

Headers:
```http
GET http://localhost:5173/@react-refresh HTTP/1.1
host: localhost:5173
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Connection: keep-alive
Referer: http://localhost:5173/
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDk1NzF9.6xPB8cUE63QhefuiiRzG56zhdFE5lbB-b7dUFPwWED0
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `ogic is copy-pasted from similar logic in th` hoặc hành vi runtime vẫn khớp alert `Information Disclosure - Suspicious Comments`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-043

- Alert liên quan: ZAP-013
- Mục tiêu test: Kiểm chứng alert `Information Disclosure - Suspicious Comments` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_user_basic.json`

### Input

```http
GET http://localhost:5173/node_modules/.vite/deps/axios.js?v=82fd3d9d
```

Headers:
```http
GET http://localhost:5173/node_modules/.vite/deps/axios.js?v=82fd3d9d HTTP/1.1
host: localhost:5173
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Connection: keep-alive
Referer: http://localhost:5173/src/pages/Home.jsx
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDk1NzF9.6xPB8cUE63QhefuiiRzG56zhdFE5lbB-b7dUFPwWED0
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `to copy properties from
* @param {Object} t` hoặc hành vi runtime vẫn khớp alert `Information Disclosure - Suspicious Comments`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-044

- Alert liên quan: ZAP-013
- Mục tiêu test: Kiểm chứng alert `Information Disclosure - Suspicious Comments` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_user_basic.json`

### Input

```http
GET http://localhost:5173/node_modules/.vite/deps/axios.js?v=82fd3d9d
```

Headers:
```http
GET http://localhost:5173/node_modules/.vite/deps/axios.js?v=82fd3d9d HTTP/1.1
host: localhost:5173
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Connection: keep-alive
Referer: http://localhost:5173/src/pages/Home.jsx
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDk1NzF9.6xPB8cUE63QhefuiiRzG56zhdFE5lbB-b7dUFPwWED0
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `in the same key the later object in
* the arg` hoặc hành vi runtime vẫn khớp alert `Information Disclosure - Suspicious Comments`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-045

- Alert liên quan: ZAP-013
- Mục tiêu test: Kiểm chứng alert `Information Disclosure - Suspicious Comments` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_user_basic.json`

### Input

```http
GET http://localhost:5173/node_modules/.vite/deps/react-router-dom.js?v=82fd3d9d
```

Headers:
```http
GET http://localhost:5173/node_modules/.vite/deps/react-router-dom.js?v=82fd3d9d HTTP/1.1
host: localhost:5173
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Connection: keep-alive
Referer: http://localhost:5173/src/App.jsx
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDk1NzF9.6xPB8cUE63QhefuiiRzG56zhdFE5lbB-b7dUFPwWED0
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `*
	* Access a value from the context. If no` hoặc hành vi runtime vẫn khớp alert `Information Disclosure - Suspicious Comments`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-046

- Alert liên quan: ZAP-013
- Mục tiêu test: Kiểm chứng alert `Information Disclosure - Suspicious Comments` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_user_basic.json`

### Input

```http
GET http://localhost:5173/node_modules/.vite/deps/react-router-dom.js?v=82fd3d9d
```

Headers:
```http
GET http://localhost:5173/node_modules/.vite/deps/react-router-dom.js?v=82fd3d9d HTTP/1.1
host: localhost:5173
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Connection: keep-alive
Referer: http://localhost:5173/src/App.jsx
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDk1NzF9.6xPB8cUE63QhefuiiRzG56zhdFE5lbB-b7dUFPwWED0
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `, will
	* cause the user agent to ignore the` hoặc hành vi runtime vẫn khớp alert `Information Disclosure - Suspicious Comments`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-047

- Alert liên quan: ZAP-014
- Mục tiêu test: Kiểm chứng alert `Modern Web Application` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_user_basic.json`

### Input

```http
GET http://localhost:5173
```

Headers:
```http
GET http://localhost:5173 HTTP/1.1
host: localhost:5173
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36
pragma: no-cache
cache-control: no-cache
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDk1NzF9.6xPB8cUE63QhefuiiRzG56zhdFE5lbB-b7dUFPwWED0
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `<script type="module">import { injectIntoGlobalHook } from "/@react-refresh";
injectIntoGlobalHook(window);
window.$RefreshReg$ = () => {};
window.$RefreshSig$ = () => (type) => type;</script>` hoặc hành vi runtime vẫn khớp alert `Modern Web Application`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-048

- Alert liên quan: ZAP-014
- Mục tiêu test: Kiểm chứng alert `Modern Web Application` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_user_basic.json`

### Input

```http
GET http://localhost:5173/
```

Headers:
```http
GET http://localhost:5173/ HTTP/1.1
host: localhost:5173
User-Agent: python-requests/2.32.5
Accept: */*
Connection: keep-alive
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDk1NzF9.6xPB8cUE63QhefuiiRzG56zhdFE5lbB-b7dUFPwWED0
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `<script type="module">import { injectIntoGlobalHook } from "/@react-refresh";
injectIntoGlobalHook(window);
window.$RefreshReg$ = () => {};
window.$RefreshSig$ = () => (type) => type;</script>` hoặc hành vi runtime vẫn khớp alert `Modern Web Application`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-049

- Alert liên quan: ZAP-014
- Mục tiêu test: Kiểm chứng alert `Modern Web Application` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_user_basic.json`

### Input

```http
GET http://localhost:5173/forgot-password
```

Headers:
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

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `<script type="module">import { injectIntoGlobalHook } from "/@react-refresh";
injectIntoGlobalHook(window);
window.$RefreshReg$ = () => {};
window.$RefreshSig$ = () => (type) => type;</script>` hoặc hành vi runtime vẫn khớp alert `Modern Web Application`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-050

- Alert liên quan: ZAP-014
- Mục tiêu test: Kiểm chứng alert `Modern Web Application` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_user_basic.json`

### Input

```http
GET http://localhost:5173/robots.txt
```

Headers:
```http
GET http://localhost:5173/robots.txt HTTP/1.1
host: localhost:5173
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36
pragma: no-cache
cache-control: no-cache
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDk1NzF9.6xPB8cUE63QhefuiiRzG56zhdFE5lbB-b7dUFPwWED0
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `<script type="module">import { injectIntoGlobalHook } from "/@react-refresh";
injectIntoGlobalHook(window);
window.$RefreshReg$ = () => {};
window.$RefreshSig$ = () => (type) => type;</script>` hoặc hành vi runtime vẫn khớp alert `Modern Web Application`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-051

- Alert liên quan: ZAP-014
- Mục tiêu test: Kiểm chứng alert `Modern Web Application` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_user_basic.json`

### Input

```http
GET http://localhost:5173/sitemap.xml
```

Headers:
```http
GET http://localhost:5173/sitemap.xml HTTP/1.1
host: localhost:5173
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36
pragma: no-cache
cache-control: no-cache
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDk1NzF9.6xPB8cUE63QhefuiiRzG56zhdFE5lbB-b7dUFPwWED0
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `<script type="module">import { injectIntoGlobalHook } from "/@react-refresh";
injectIntoGlobalHook(window);
window.$RefreshReg$ = () => {};
window.$RefreshSig$ = () => (type) => type;</script>` hoặc hành vi runtime vẫn khớp alert `Modern Web Application`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-052

- Alert liên quan: ZAP-001
- Mục tiêu test: Kiểm chứng alert `CSP: Failure to Define Directive with No Fallback` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_user_basic.json`

### Input

```http
GET http://localhost:3000
```

Headers:
```http
GET http://localhost:3000 HTTP/1.1
host: localhost:3000
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36
pragma: no-cache
cache-control: no-cache
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDkwNzV9.mOzLCI5uoLpBGWGMZ2PY7Y00zv3jSMAC2u4oQUHcVhc
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `default-src 'none'` hoặc hành vi runtime vẫn khớp alert `CSP: Failure to Define Directive with No Fallback`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-053

- Alert liên quan: ZAP-001
- Mục tiêu test: Kiểm chứng alert `CSP: Failure to Define Directive with No Fallback` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_user_basic.json`

### Input

```http
GET http://localhost:3000/
```

Headers:
```http
GET http://localhost:3000/ HTTP/1.1
host: localhost:3000
User-Agent: python-requests/2.32.5
Accept: */*
Connection: keep-alive
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDkwNzV9.mOzLCI5uoLpBGWGMZ2PY7Y00zv3jSMAC2u4oQUHcVhc
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `default-src 'none'` hoặc hành vi runtime vẫn khớp alert `CSP: Failure to Define Directive with No Fallback`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-054

- Alert liên quan: ZAP-001
- Mục tiêu test: Kiểm chứng alert `CSP: Failure to Define Directive with No Fallback` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_user_basic.json`

### Input

```http
GET http://localhost:3000/api
```

Headers:
```http
GET http://localhost:3000/api HTTP/1.1
host: localhost:3000
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36
pragma: no-cache
cache-control: no-cache
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDkwNzV9.mOzLCI5uoLpBGWGMZ2PY7Y00zv3jSMAC2u4oQUHcVhc
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `default-src 'none'` hoặc hành vi runtime vẫn khớp alert `CSP: Failure to Define Directive with No Fallback`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-055

- Alert liên quan: ZAP-001
- Mục tiêu test: Kiểm chứng alert `CSP: Failure to Define Directive with No Fallback` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_user_basic.json`

### Input

```http
GET http://localhost:3000/robots.txt
```

Headers:
```http
GET http://localhost:3000/robots.txt HTTP/1.1
host: localhost:3000
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36
pragma: no-cache
cache-control: no-cache
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDkwNzV9.mOzLCI5uoLpBGWGMZ2PY7Y00zv3jSMAC2u4oQUHcVhc
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `default-src 'none'` hoặc hành vi runtime vẫn khớp alert `CSP: Failure to Define Directive with No Fallback`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-056

- Alert liên quan: ZAP-001
- Mục tiêu test: Kiểm chứng alert `CSP: Failure to Define Directive with No Fallback` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_user_basic.json`

### Input

```http
GET http://localhost:3000/sitemap.xml
```

Headers:
```http
GET http://localhost:3000/sitemap.xml HTTP/1.1
host: localhost:3000
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36
pragma: no-cache
cache-control: no-cache
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDkwNzV9.mOzLCI5uoLpBGWGMZ2PY7Y00zv3jSMAC2u4oQUHcVhc
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `default-src 'none'` hoặc hành vi runtime vẫn khớp alert `CSP: Failure to Define Directive with No Fallback`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-057

- Alert liên quan: ZAP-002
- Mục tiêu test: Kiểm chứng alert `Cross-Domain Misconfiguration` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_user_basic.json`

### Input

```http
GET http://localhost:3000
```

Headers:
```http
GET http://localhost:3000 HTTP/1.1
host: localhost:3000
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36
pragma: no-cache
cache-control: no-cache
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDkwNzV9.mOzLCI5uoLpBGWGMZ2PY7Y00zv3jSMAC2u4oQUHcVhc
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `Access-Control-Allow-Origin: *` hoặc hành vi runtime vẫn khớp alert `Cross-Domain Misconfiguration`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-058

- Alert liên quan: ZAP-002
- Mục tiêu test: Kiểm chứng alert `Cross-Domain Misconfiguration` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_user_basic.json`

### Input

```http
GET http://localhost:3000/
```

Headers:
```http
GET http://localhost:3000/ HTTP/1.1
host: localhost:3000
User-Agent: python-requests/2.32.5
Accept: */*
Connection: keep-alive
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDkwNzV9.mOzLCI5uoLpBGWGMZ2PY7Y00zv3jSMAC2u4oQUHcVhc
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `Access-Control-Allow-Origin: *` hoặc hành vi runtime vẫn khớp alert `Cross-Domain Misconfiguration`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-059

- Alert liên quan: ZAP-002
- Mục tiêu test: Kiểm chứng alert `Cross-Domain Misconfiguration` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_user_basic.json`

### Input

```http
GET http://localhost:3000/api/users/me
```

Headers:
```http
GET http://localhost:3000/api/users/me HTTP/1.1
host: localhost:3000
User-Agent: Python-urllib/3.14
Connection: close
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDkwNzV9.mOzLCI5uoLpBGWGMZ2PY7Y00zv3jSMAC2u4oQUHcVhc
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `Access-Control-Allow-Origin: *` hoặc hành vi runtime vẫn khớp alert `Cross-Domain Misconfiguration`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-060

- Alert liên quan: ZAP-002
- Mục tiêu test: Kiểm chứng alert `Cross-Domain Misconfiguration` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_user_basic.json`

### Input

```http
GET http://localhost:3000/sitemap.xml
```

Headers:
```http
GET http://localhost:3000/sitemap.xml HTTP/1.1
host: localhost:3000
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36
pragma: no-cache
cache-control: no-cache
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDkwNzV9.mOzLCI5uoLpBGWGMZ2PY7Y00zv3jSMAC2u4oQUHcVhc
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `Access-Control-Allow-Origin: *` hoặc hành vi runtime vẫn khớp alert `Cross-Domain Misconfiguration`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-061

- Alert liên quan: ZAP-003
- Mục tiêu test: Kiểm chứng alert `Server Leaks Information via "X-Powered-By" HTTP Response Header Field(s)` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_user_basic.json`

### Input

```http
GET http://localhost:3000
```

Headers:
```http
GET http://localhost:3000 HTTP/1.1
host: localhost:3000
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36
pragma: no-cache
cache-control: no-cache
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDkwNzV9.mOzLCI5uoLpBGWGMZ2PY7Y00zv3jSMAC2u4oQUHcVhc
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `X-Powered-By: Express` hoặc hành vi runtime vẫn khớp alert `Server Leaks Information via "X-Powered-By" HTTP Response Header Field(s)`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-062

- Alert liên quan: ZAP-003
- Mục tiêu test: Kiểm chứng alert `Server Leaks Information via "X-Powered-By" HTTP Response Header Field(s)` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_user_basic.json`

### Input

```http
GET http://localhost:3000/
```

Headers:
```http
GET http://localhost:3000/ HTTP/1.1
host: localhost:3000
User-Agent: python-requests/2.32.5
Accept: */*
Connection: keep-alive
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDkwNzV9.mOzLCI5uoLpBGWGMZ2PY7Y00zv3jSMAC2u4oQUHcVhc
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `X-Powered-By: Express` hoặc hành vi runtime vẫn khớp alert `Server Leaks Information via "X-Powered-By" HTTP Response Header Field(s)`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-063

- Alert liên quan: ZAP-003
- Mục tiêu test: Kiểm chứng alert `Server Leaks Information via "X-Powered-By" HTTP Response Header Field(s)` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_user_basic.json`

### Input

```http
GET http://localhost:3000/api/users/me
```

Headers:
```http
GET http://localhost:3000/api/users/me HTTP/1.1
host: localhost:3000
User-Agent: Python-urllib/3.14
Connection: close
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDkwNzV9.mOzLCI5uoLpBGWGMZ2PY7Y00zv3jSMAC2u4oQUHcVhc
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `X-Powered-By: Express` hoặc hành vi runtime vẫn khớp alert `Server Leaks Information via "X-Powered-By" HTTP Response Header Field(s)`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-064

- Alert liên quan: ZAP-003
- Mục tiêu test: Kiểm chứng alert `Server Leaks Information via "X-Powered-By" HTTP Response Header Field(s)` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_user_basic.json`

### Input

```http
GET http://localhost:3000/robots.txt
```

Headers:
```http
GET http://localhost:3000/robots.txt HTTP/1.1
host: localhost:3000
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36
pragma: no-cache
cache-control: no-cache
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDkwNzV9.mOzLCI5uoLpBGWGMZ2PY7Y00zv3jSMAC2u4oQUHcVhc
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `X-Powered-By: Express` hoặc hành vi runtime vẫn khớp alert `Server Leaks Information via "X-Powered-By" HTTP Response Header Field(s)`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-065

- Alert liên quan: ZAP-003
- Mục tiêu test: Kiểm chứng alert `Server Leaks Information via "X-Powered-By" HTTP Response Header Field(s)` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_user_basic.json`

### Input

```http
POST http://localhost:3000/api/login
```

Headers:
```http
POST http://localhost:3000/api/login HTTP/1.1
Content-Length: 52
host: localhost:3000
User-Agent: Python-urllib/3.14
Content-Type: application/json
Connection: close
```

Payload:
```json
{"email": "test@eshop.com", "password": "Test1234!"}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `X-Powered-By: Express` hoặc hành vi runtime vẫn khớp alert `Server Leaks Information via "X-Powered-By" HTTP Response Header Field(s)`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-066

- Alert liên quan: ZAP-004
- Mục tiêu test: Kiểm chứng alert `X-Content-Type-Options Header Missing` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_user_basic.json`

### Input

```http
GET http://localhost:3000/api/products?search=
```

Headers:
```http
GET http://localhost:3000/api/products?search= HTTP/1.1
host: localhost:3000
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0
Accept: application/json, text/plain, */*
Accept-Language: en-US,en;q=0.5
Origin: http://localhost:5173
Connection: keep-alive
Referer: http://localhost:5173/
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDk1NzF9.6xPB8cUE63QhefuiiRzG56zhdFE5lbB-b7dUFPwWED0
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `N/A` hoặc hành vi runtime vẫn khớp alert `X-Content-Type-Options Header Missing`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-067

- Alert liên quan: ZAP-004
- Mục tiêu test: Kiểm chứng alert `X-Content-Type-Options Header Missing` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_user_basic.json`

### Input

```http
GET http://localhost:3000/api/products/1
```

Headers:
```http
GET http://localhost:3000/api/products/1 HTTP/1.1
host: localhost:3000
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0
Accept: application/json, text/plain, */*
Accept-Language: en-US,en;q=0.5
Origin: http://localhost:5173
Connection: keep-alive
Referer: http://localhost:5173/
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDk1NzF9.6xPB8cUE63QhefuiiRzG56zhdFE5lbB-b7dUFPwWED0
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `N/A` hoặc hành vi runtime vẫn khớp alert `X-Content-Type-Options Header Missing`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-068

- Alert liên quan: ZAP-004
- Mục tiêu test: Kiểm chứng alert `X-Content-Type-Options Header Missing` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_user_basic.json`

### Input

```http
GET http://localhost:3000/api/products/2
```

Headers:
```http
GET http://localhost:3000/api/products/2 HTTP/1.1
host: localhost:3000
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0
Accept: application/json, text/plain, */*
Accept-Language: en-US,en;q=0.5
Origin: http://localhost:5173
Connection: keep-alive
Referer: http://localhost:5173/
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDk1NzF9.6xPB8cUE63QhefuiiRzG56zhdFE5lbB-b7dUFPwWED0
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `N/A` hoặc hành vi runtime vẫn khớp alert `X-Content-Type-Options Header Missing`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-069

- Alert liên quan: ZAP-004
- Mục tiêu test: Kiểm chứng alert `X-Content-Type-Options Header Missing` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_user_basic.json`

### Input

```http
GET http://localhost:3000/api/users/me
```

Headers:
```http
GET http://localhost:3000/api/users/me HTTP/1.1
host: localhost:3000
User-Agent: Python-urllib/3.14
Connection: close
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDkwNzV9.mOzLCI5uoLpBGWGMZ2PY7Y00zv3jSMAC2u4oQUHcVhc
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `N/A` hoặc hành vi runtime vẫn khớp alert `X-Content-Type-Options Header Missing`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-070

- Alert liên quan: ZAP-004
- Mục tiêu test: Kiểm chứng alert `X-Content-Type-Options Header Missing` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_user_basic.json`

### Input

```http
POST http://localhost:3000/api/login
```

Headers:
```http
POST http://localhost:3000/api/login HTTP/1.1
Content-Length: 52
host: localhost:3000
User-Agent: Python-urllib/3.14
Content-Type: application/json
Connection: close
```

Payload:
```json
{"email": "test@eshop.com", "password": "Test1234!"}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `N/A` hoặc hành vi runtime vẫn khớp alert `X-Content-Type-Options Header Missing`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-071

- Alert liên quan: ZAP-005
- Mục tiêu test: Kiểm chứng alert `Authentication Request Identified` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_user_basic.json`

### Input

```http
POST http://localhost:3000/api/login
```

Headers:
```http
POST http://localhost:3000/api/login HTTP/1.1
Content-Length: 52
host: localhost:3000
User-Agent: Python-urllib/3.14
Content-Type: application/json
Connection: close
```

Payload:
```json
{"email": "test@eshop.com", "password": "Test1234!"}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `password` hoặc hành vi runtime vẫn khớp alert `Authentication Request Identified`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-072

- Alert liên quan: ZAP-006
- Mục tiêu test: Kiểm chứng alert `Session Management Response Identified` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_user_basic.json`

### Input

```http
POST http://localhost:3000/api/login
```

Headers:
```http
POST http://localhost:3000/api/login HTTP/1.1
Content-Length: 52
host: localhost:3000
User-Agent: Python-urllib/3.14
Content-Type: application/json
Connection: close
```

Payload:
```json
{"email": "test@eshop.com", "password": "Test1234!"}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `token` hoặc hành vi runtime vẫn khớp alert `Session Management Response Identified`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-073

- Alert liên quan: ZAP-006
- Mục tiêu test: Kiểm chứng alert `Session Management Response Identified` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_user_basic.json`

### Input

```http
POST http://localhost:3000/api/login
```

Headers:
```http
POST http://localhost:3000/api/login HTTP/1.1
Content-Length: 52
host: localhost:3000
User-Agent: Python-urllib/3.14
Content-Type: application/json
Connection: close
```

Payload:
```json
{"email": "test@eshop.com", "password": "Test1234!"}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `token` hoặc hành vi runtime vẫn khớp alert `Session Management Response Identified`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-074

- Alert liên quan: ZAP-007
- Mục tiêu test: Kiểm chứng alert `User Agent Fuzzer` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_user_basic.json`

### Input

```http
GET http://localhost:3000/api/users/me
```

Headers:
```http
GET http://localhost:3000/api/users/me HTTP/1.1
host: localhost:3000
user-agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)
pragma: no-cache
cache-control: no-cache
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDkwNzV9.mOzLCI5uoLpBGWGMZ2PY7Y00zv3jSMAC2u4oQUHcVhc
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `N/A` hoặc hành vi runtime vẫn khớp alert `User Agent Fuzzer`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-075

- Alert liên quan: ZAP-007
- Mục tiêu test: Kiểm chứng alert `User Agent Fuzzer` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_user_basic.json`

### Input

```http
GET http://localhost:3000/api/users/me
```

Headers:
```http
GET http://localhost:3000/api/users/me HTTP/1.1
host: localhost:3000
user-agent: Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1)
pragma: no-cache
cache-control: no-cache
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDkwNzV9.mOzLCI5uoLpBGWGMZ2PY7Y00zv3jSMAC2u4oQUHcVhc
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `N/A` hoặc hành vi runtime vẫn khớp alert `User Agent Fuzzer`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-076

- Alert liên quan: ZAP-007
- Mục tiêu test: Kiểm chứng alert `User Agent Fuzzer` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_user_basic.json`

### Input

```http
POST http://localhost:3000/api/login
```

Headers:
```http
POST http://localhost:3000/api/login HTTP/1.1
Content-Length: 52
host: localhost:3000
user-agent: Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1)
Content-Type: application/json
Connection: close
```

Payload:
```json
{"email": "test@eshop.com", "password": "Test1234!"}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `N/A` hoặc hành vi runtime vẫn khớp alert `User Agent Fuzzer`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-077

- Alert liên quan: ZAP-008
- Mục tiêu test: Kiểm chứng alert `Path Traversal` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_admin_basic.json`

### Input

```http
GET http://localhost:5174/node_modules/.vite/deps/chunk-nbk3hphP.js?v=%2Fchunk-nbk3hphP.js
```

Headers:
```http
GET http://localhost:5174/node_modules/.vite/deps/chunk-nbk3hphP.js?v=%2Fchunk-nbk3hphP.js HTTP/1.1
host: localhost:5174
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Connection: keep-alive
Referer: http://localhost:5174/node_modules/.vite/deps/react.js?v=1cc4e6b1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwicm9sZSI6ImFkbWluIiwiaWF0IjoxNzg0NzEwMjQ3fQ.4xCcBJucuQGSSMaZk6kIQ6yq2kqhbQn6WLb0s-kCOEU
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `N/A` hoặc hành vi runtime vẫn khớp alert `Path Traversal`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-078

- Alert liên quan: ZAP-009
- Mục tiêu test: Kiểm chứng alert `Content Security Policy (CSP) Header Not Set` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_admin_basic.json`

### Input

```http
GET http://localhost:5174
```

Headers:
```http
GET http://localhost:5174 HTTP/1.1
host: localhost:5174
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36
pragma: no-cache
cache-control: no-cache
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwicm9sZSI6ImFkbWluIiwiaWF0IjoxNzg0NzEwMjQ3fQ.4xCcBJucuQGSSMaZk6kIQ6yq2kqhbQn6WLb0s-kCOEU
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `N/A` hoặc hành vi runtime vẫn khớp alert `Content Security Policy (CSP) Header Not Set`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-079

- Alert liên quan: ZAP-009
- Mục tiêu test: Kiểm chứng alert `Content Security Policy (CSP) Header Not Set` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_admin_basic.json`

### Input

```http
GET http://localhost:5174/
```

Headers:
```http
GET http://localhost:5174/ HTTP/1.1
host: localhost:5174
User-Agent: python-requests/2.32.5
Accept: */*
Connection: keep-alive
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwicm9sZSI6ImFkbWluIiwiaWF0IjoxNzg0NzEwMjQ3fQ.4xCcBJucuQGSSMaZk6kIQ6yq2kqhbQn6WLb0s-kCOEU
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `N/A` hoặc hành vi runtime vẫn khớp alert `Content Security Policy (CSP) Header Not Set`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-080

- Alert liên quan: ZAP-009
- Mục tiêu test: Kiểm chứng alert `Content Security Policy (CSP) Header Not Set` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_admin_basic.json`

### Input

```http
GET http://localhost:5174/robots.txt
```

Headers:
```http
GET http://localhost:5174/robots.txt HTTP/1.1
host: localhost:5174
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36
pragma: no-cache
cache-control: no-cache
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwicm9sZSI6ImFkbWluIiwiaWF0IjoxNzg0NzEwMjQ3fQ.4xCcBJucuQGSSMaZk6kIQ6yq2kqhbQn6WLb0s-kCOEU
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `N/A` hoặc hành vi runtime vẫn khớp alert `Content Security Policy (CSP) Header Not Set`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-081

- Alert liên quan: ZAP-009
- Mục tiêu test: Kiểm chứng alert `Content Security Policy (CSP) Header Not Set` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_admin_basic.json`

### Input

```http
GET http://localhost:5174/sitemap.xml
```

Headers:
```http
GET http://localhost:5174/sitemap.xml HTTP/1.1
host: localhost:5174
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36
pragma: no-cache
cache-control: no-cache
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwicm9sZSI6ImFkbWluIiwiaWF0IjoxNzg0NzEwMjQ3fQ.4xCcBJucuQGSSMaZk6kIQ6yq2kqhbQn6WLb0s-kCOEU
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `N/A` hoặc hành vi runtime vẫn khớp alert `Content Security Policy (CSP) Header Not Set`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-082

- Alert liên quan: ZAP-010
- Mục tiêu test: Kiểm chứng alert `Missing Anti-clickjacking Header` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_admin_basic.json`

### Input

```http
GET http://localhost:5174
```

Headers:
```http
GET http://localhost:5174 HTTP/1.1
host: localhost:5174
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36
pragma: no-cache
cache-control: no-cache
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwicm9sZSI6ImFkbWluIiwiaWF0IjoxNzg0NzEwMjQ3fQ.4xCcBJucuQGSSMaZk6kIQ6yq2kqhbQn6WLb0s-kCOEU
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `N/A` hoặc hành vi runtime vẫn khớp alert `Missing Anti-clickjacking Header`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-083

- Alert liên quan: ZAP-010
- Mục tiêu test: Kiểm chứng alert `Missing Anti-clickjacking Header` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_admin_basic.json`

### Input

```http
GET http://localhost:5174/
```

Headers:
```http
GET http://localhost:5174/ HTTP/1.1
host: localhost:5174
User-Agent: python-requests/2.32.5
Accept: */*
Connection: keep-alive
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwicm9sZSI6ImFkbWluIiwiaWF0IjoxNzg0NzEwMjQ3fQ.4xCcBJucuQGSSMaZk6kIQ6yq2kqhbQn6WLb0s-kCOEU
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `N/A` hoặc hành vi runtime vẫn khớp alert `Missing Anti-clickjacking Header`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-084

- Alert liên quan: ZAP-010
- Mục tiêu test: Kiểm chứng alert `Missing Anti-clickjacking Header` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_admin_basic.json`

### Input

```http
GET http://localhost:5174/robots.txt
```

Headers:
```http
GET http://localhost:5174/robots.txt HTTP/1.1
host: localhost:5174
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36
pragma: no-cache
cache-control: no-cache
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwicm9sZSI6ImFkbWluIiwiaWF0IjoxNzg0NzEwMjQ3fQ.4xCcBJucuQGSSMaZk6kIQ6yq2kqhbQn6WLb0s-kCOEU
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `N/A` hoặc hành vi runtime vẫn khớp alert `Missing Anti-clickjacking Header`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-085

- Alert liên quan: ZAP-010
- Mục tiêu test: Kiểm chứng alert `Missing Anti-clickjacking Header` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_admin_basic.json`

### Input

```http
GET http://localhost:5174/sitemap.xml
```

Headers:
```http
GET http://localhost:5174/sitemap.xml HTTP/1.1
host: localhost:5174
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36
pragma: no-cache
cache-control: no-cache
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwicm9sZSI6ImFkbWluIiwiaWF0IjoxNzg0NzEwMjQ3fQ.4xCcBJucuQGSSMaZk6kIQ6yq2kqhbQn6WLb0s-kCOEU
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `N/A` hoặc hành vi runtime vẫn khớp alert `Missing Anti-clickjacking Header`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-086

- Alert liên quan: ZAP-011
- Mục tiêu test: Kiểm chứng alert `Timestamp Disclosure - Unix` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_admin_basic.json`

### Input

```http
GET http://localhost:5174/node_modules/.vite/deps/react-dom_client.js?v=1cc4e6b1
```

Headers:
```http
GET http://localhost:5174/node_modules/.vite/deps/react-dom_client.js?v=1cc4e6b1 HTTP/1.1
host: localhost:5174
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Connection: keep-alive
Referer: http://localhost:5174/src/main.jsx
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwicm9sZSI6ImFkbWluIiwiaWF0IjoxNzg0NzEwMjQ3fQ.4xCcBJucuQGSSMaZk6kIQ6yq2kqhbQn6WLb0s-kCOEU
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `2080374784` hoặc hành vi runtime vẫn khớp alert `Timestamp Disclosure - Unix`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-087

- Alert liên quan: ZAP-004
- Mục tiêu test: Kiểm chứng alert `X-Content-Type-Options Header Missing` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_admin_basic.json`

### Input

```http
GET http://localhost:5174
```

Headers:
```http
GET http://localhost:5174 HTTP/1.1
host: localhost:5174
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36
pragma: no-cache
cache-control: no-cache
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwicm9sZSI6ImFkbWluIiwiaWF0IjoxNzg0NzEwMjQ3fQ.4xCcBJucuQGSSMaZk6kIQ6yq2kqhbQn6WLb0s-kCOEU
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `N/A` hoặc hành vi runtime vẫn khớp alert `X-Content-Type-Options Header Missing`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-088

- Alert liên quan: ZAP-004
- Mục tiêu test: Kiểm chứng alert `X-Content-Type-Options Header Missing` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_admin_basic.json`

### Input

```http
GET http://localhost:5174/
```

Headers:
```http
GET http://localhost:5174/ HTTP/1.1
host: localhost:5174
User-Agent: python-requests/2.32.5
Accept: */*
Connection: keep-alive
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwicm9sZSI6ImFkbWluIiwiaWF0IjoxNzg0NzEwMjQ3fQ.4xCcBJucuQGSSMaZk6kIQ6yq2kqhbQn6WLb0s-kCOEU
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `N/A` hoặc hành vi runtime vẫn khớp alert `X-Content-Type-Options Header Missing`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-089

- Alert liên quan: ZAP-004
- Mục tiêu test: Kiểm chứng alert `X-Content-Type-Options Header Missing` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_admin_basic.json`

### Input

```http
GET http://localhost:5174/robots.txt
```

Headers:
```http
GET http://localhost:5174/robots.txt HTTP/1.1
host: localhost:5174
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36
pragma: no-cache
cache-control: no-cache
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwicm9sZSI6ImFkbWluIiwiaWF0IjoxNzg0NzEwMjQ3fQ.4xCcBJucuQGSSMaZk6kIQ6yq2kqhbQn6WLb0s-kCOEU
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `N/A` hoặc hành vi runtime vẫn khớp alert `X-Content-Type-Options Header Missing`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-090

- Alert liên quan: ZAP-004
- Mục tiêu test: Kiểm chứng alert `X-Content-Type-Options Header Missing` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_admin_basic.json`

### Input

```http
GET http://localhost:5174/sitemap.xml
```

Headers:
```http
GET http://localhost:5174/sitemap.xml HTTP/1.1
host: localhost:5174
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36
pragma: no-cache
cache-control: no-cache
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwicm9sZSI6ImFkbWluIiwiaWF0IjoxNzg0NzEwMjQ3fQ.4xCcBJucuQGSSMaZk6kIQ6yq2kqhbQn6WLb0s-kCOEU
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `N/A` hoặc hành vi runtime vẫn khớp alert `X-Content-Type-Options Header Missing`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-091

- Alert liên quan: ZAP-004
- Mục tiêu test: Kiểm chứng alert `X-Content-Type-Options Header Missing` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_admin_basic.json`

### Input

```http
GET http://localhost:5174/src/main.jsx
```

Headers:
```http
GET http://localhost:5174/src/main.jsx HTTP/1.1
host: localhost:5174
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36
pragma: no-cache
cache-control: no-cache
referer: http://localhost:5174
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwicm9sZSI6ImFkbWluIiwiaWF0IjoxNzg0NzEwMjQ3fQ.4xCcBJucuQGSSMaZk6kIQ6yq2kqhbQn6WLb0s-kCOEU
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `N/A` hoặc hành vi runtime vẫn khớp alert `X-Content-Type-Options Header Missing`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-092

- Alert liên quan: ZAP-012
- Mục tiêu test: Kiểm chứng alert `Information Disclosure - Sensitive Information in URL` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_admin_basic.json`

### Input

```http
GET http://localhost:5174/?token=-LYBc--RLYE6
```

Headers:
```http
GET http://localhost:5174/?token=-LYBc--RLYE6 HTTP/1.1
host: localhost:5174
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Sec-WebSocket-Version: 13
Origin: http://localhost:5174
Sec-WebSocket-Protocol: vite-hmr
Sec-WebSocket-Key: uk3FWrFnEOIA81mQHh5Ztw==
Connection: Upgrade
Pragma: no-cache
Cache-Control: no-cache
Upgrade: websocket
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwicm9sZSI6ImFkbWluIiwiaWF0IjoxNzg0NzEwMjQ3fQ.4xCcBJucuQGSSMaZk6kIQ6yq2kqhbQn6WLb0s-kCOEU
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `token` hoặc hành vi runtime vẫn khớp alert `Information Disclosure - Sensitive Information in URL`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-093

- Alert liên quan: ZAP-013
- Mục tiêu test: Kiểm chứng alert `Information Disclosure - Suspicious Comments` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_admin_basic.json`

### Input

```http
GET http://localhost:5174/@react-refresh
```

Headers:
```http
GET http://localhost:5174/@react-refresh HTTP/1.1
host: localhost:5174
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Connection: keep-alive
Referer: http://localhost:5174/
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwicm9sZSI6ImFkbWluIiwiaWF0IjoxNzg0NzEwMjQ3fQ.4xCcBJucuQGSSMaZk6kIQ6yq2kqhbQn6WLb0s-kCOEU
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `// TODO: rename these field` hoặc hành vi runtime vẫn khớp alert `Information Disclosure - Suspicious Comments`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-094

- Alert liên quan: ZAP-013
- Mục tiêu test: Kiểm chứng alert `Information Disclosure - Suspicious Comments` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_admin_basic.json`

### Input

```http
GET http://localhost:5174/@react-refresh
```

Headers:
```http
GET http://localhost:5174/@react-refresh HTTP/1.1
host: localhost:5174
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Connection: keep-alive
Referer: http://localhost:5174/
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwicm9sZSI6ImFkbWluIiwiaWF0IjoxNzg0NzEwMjQ3fQ.4xCcBJucuQGSSMaZk6kIQ6yq2kqhbQn6WLb0s-kCOEU
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `ogic is copy-pasted from similar logic in th` hoặc hành vi runtime vẫn khớp alert `Information Disclosure - Suspicious Comments`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-095

- Alert liên quan: ZAP-013
- Mục tiêu test: Kiểm chứng alert `Information Disclosure - Suspicious Comments` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_admin_basic.json`

### Input

```http
GET http://localhost:5174/node_modules/.vite/deps/axios.js?v=1cc4e6b1
```

Headers:
```http
GET http://localhost:5174/node_modules/.vite/deps/axios.js?v=1cc4e6b1 HTTP/1.1
host: localhost:5174
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Connection: keep-alive
Referer: http://localhost:5174/src/App.jsx
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwicm9sZSI6ImFkbWluIiwiaWF0IjoxNzg0NzEwMjQ3fQ.4xCcBJucuQGSSMaZk6kIQ6yq2kqhbQn6WLb0s-kCOEU
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `to copy properties from
* @param {Object} t` hoặc hành vi runtime vẫn khớp alert `Information Disclosure - Suspicious Comments`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-096

- Alert liên quan: ZAP-013
- Mục tiêu test: Kiểm chứng alert `Information Disclosure - Suspicious Comments` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_admin_basic.json`

### Input

```http
GET http://localhost:5174/node_modules/.vite/deps/axios.js?v=1cc4e6b1
```

Headers:
```http
GET http://localhost:5174/node_modules/.vite/deps/axios.js?v=1cc4e6b1 HTTP/1.1
host: localhost:5174
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Connection: keep-alive
Referer: http://localhost:5174/src/App.jsx
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwicm9sZSI6ImFkbWluIiwiaWF0IjoxNzg0NzEwMjQ3fQ.4xCcBJucuQGSSMaZk6kIQ6yq2kqhbQn6WLb0s-kCOEU
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `in the same key the later object in
* the arg` hoặc hành vi runtime vẫn khớp alert `Information Disclosure - Suspicious Comments`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-097

- Alert liên quan: ZAP-014
- Mục tiêu test: Kiểm chứng alert `Modern Web Application` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_admin_basic.json`

### Input

```http
GET http://localhost:5174
```

Headers:
```http
GET http://localhost:5174 HTTP/1.1
host: localhost:5174
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36
pragma: no-cache
cache-control: no-cache
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwicm9sZSI6ImFkbWluIiwiaWF0IjoxNzg0NzEwMjQ3fQ.4xCcBJucuQGSSMaZk6kIQ6yq2kqhbQn6WLb0s-kCOEU
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `<script type="module">import { injectIntoGlobalHook } from "/@react-refresh";
injectIntoGlobalHook(window);
window.$RefreshReg$ = () => {};
window.$RefreshSig$ = () => (type) => type;</script>` hoặc hành vi runtime vẫn khớp alert `Modern Web Application`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-098

- Alert liên quan: ZAP-014
- Mục tiêu test: Kiểm chứng alert `Modern Web Application` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_admin_basic.json`

### Input

```http
GET http://localhost:5174/
```

Headers:
```http
GET http://localhost:5174/ HTTP/1.1
host: localhost:5174
User-Agent: python-requests/2.32.5
Accept: */*
Connection: keep-alive
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwicm9sZSI6ImFkbWluIiwiaWF0IjoxNzg0NzEwMjQ3fQ.4xCcBJucuQGSSMaZk6kIQ6yq2kqhbQn6WLb0s-kCOEU
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `<script type="module">import { injectIntoGlobalHook } from "/@react-refresh";
injectIntoGlobalHook(window);
window.$RefreshReg$ = () => {};
window.$RefreshSig$ = () => (type) => type;</script>` hoặc hành vi runtime vẫn khớp alert `Modern Web Application`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-099

- Alert liên quan: ZAP-014
- Mục tiêu test: Kiểm chứng alert `Modern Web Application` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_admin_basic.json`

### Input

```http
GET http://localhost:5174/robots.txt
```

Headers:
```http
GET http://localhost:5174/robots.txt HTTP/1.1
host: localhost:5174
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36
pragma: no-cache
cache-control: no-cache
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwicm9sZSI6ImFkbWluIiwiaWF0IjoxNzg0NzEwMjQ3fQ.4xCcBJucuQGSSMaZk6kIQ6yq2kqhbQn6WLb0s-kCOEU
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `<script type="module">import { injectIntoGlobalHook } from "/@react-refresh";
injectIntoGlobalHook(window);
window.$RefreshReg$ = () => {};
window.$RefreshSig$ = () => (type) => type;</script>` hoặc hành vi runtime vẫn khớp alert `Modern Web Application`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-100

- Alert liên quan: ZAP-014
- Mục tiêu test: Kiểm chứng alert `Modern Web Application` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_admin_basic.json`

### Input

```http
GET http://localhost:5174/sitemap.xml
```

Headers:
```http
GET http://localhost:5174/sitemap.xml HTTP/1.1
host: localhost:5174
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36
pragma: no-cache
cache-control: no-cache
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwicm9sZSI6ImFkbWluIiwiaWF0IjoxNzg0NzEwMjQ3fQ.4xCcBJucuQGSSMaZk6kIQ6yq2kqhbQn6WLb0s-kCOEU
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `<script type="module">import { injectIntoGlobalHook } from "/@react-refresh";
injectIntoGlobalHook(window);
window.$RefreshReg$ = () => {};
window.$RefreshSig$ = () => (type) => type;</script>` hoặc hành vi runtime vẫn khớp alert `Modern Web Application`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-101

- Alert liên quan: ZAP-008
- Mục tiêu test: Kiểm chứng alert `Path Traversal` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_admin_basic.json`

### Input

```http
GET http://localhost:5173/node_modules/.vite/deps/chunk-CYJPkc-J.js?v=%2Fchunk-CYJPkc-J.js
```

Headers:
```http
GET http://localhost:5173/node_modules/.vite/deps/chunk-CYJPkc-J.js?v=%2Fchunk-CYJPkc-J.js HTTP/1.1
host: localhost:5173
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Connection: keep-alive
Referer: http://localhost:5173/node_modules/.vite/deps/react.js?v=82fd3d9d
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDk1NzF9.6xPB8cUE63QhefuiiRzG56zhdFE5lbB-b7dUFPwWED0
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `N/A` hoặc hành vi runtime vẫn khớp alert `Path Traversal`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-102

- Alert liên quan: ZAP-009
- Mục tiêu test: Kiểm chứng alert `Content Security Policy (CSP) Header Not Set` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_admin_basic.json`

### Input

```http
GET http://localhost:5173
```

Headers:
```http
GET http://localhost:5173 HTTP/1.1
host: localhost:5173
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36
pragma: no-cache
cache-control: no-cache
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDk1NzF9.6xPB8cUE63QhefuiiRzG56zhdFE5lbB-b7dUFPwWED0
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `N/A` hoặc hành vi runtime vẫn khớp alert `Content Security Policy (CSP) Header Not Set`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-103

- Alert liên quan: ZAP-009
- Mục tiêu test: Kiểm chứng alert `Content Security Policy (CSP) Header Not Set` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_admin_basic.json`

### Input

```http
GET http://localhost:5173/
```

Headers:
```http
GET http://localhost:5173/ HTTP/1.1
host: localhost:5173
User-Agent: python-requests/2.32.5
Accept: */*
Connection: keep-alive
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDk1NzF9.6xPB8cUE63QhefuiiRzG56zhdFE5lbB-b7dUFPwWED0
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `N/A` hoặc hành vi runtime vẫn khớp alert `Content Security Policy (CSP) Header Not Set`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-104

- Alert liên quan: ZAP-009
- Mục tiêu test: Kiểm chứng alert `Content Security Policy (CSP) Header Not Set` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_admin_basic.json`

### Input

```http
GET http://localhost:5173/forgot-password
```

Headers:
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

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `N/A` hoặc hành vi runtime vẫn khớp alert `Content Security Policy (CSP) Header Not Set`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-105

- Alert liên quan: ZAP-009
- Mục tiêu test: Kiểm chứng alert `Content Security Policy (CSP) Header Not Set` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_admin_basic.json`

### Input

```http
GET http://localhost:5173/robots.txt
```

Headers:
```http
GET http://localhost:5173/robots.txt HTTP/1.1
host: localhost:5173
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36
pragma: no-cache
cache-control: no-cache
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDk1NzF9.6xPB8cUE63QhefuiiRzG56zhdFE5lbB-b7dUFPwWED0
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `N/A` hoặc hành vi runtime vẫn khớp alert `Content Security Policy (CSP) Header Not Set`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-106

- Alert liên quan: ZAP-009
- Mục tiêu test: Kiểm chứng alert `Content Security Policy (CSP) Header Not Set` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_admin_basic.json`

### Input

```http
GET http://localhost:5173/sitemap.xml
```

Headers:
```http
GET http://localhost:5173/sitemap.xml HTTP/1.1
host: localhost:5173
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36
pragma: no-cache
cache-control: no-cache
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDk1NzF9.6xPB8cUE63QhefuiiRzG56zhdFE5lbB-b7dUFPwWED0
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `N/A` hoặc hành vi runtime vẫn khớp alert `Content Security Policy (CSP) Header Not Set`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-107

- Alert liên quan: ZAP-010
- Mục tiêu test: Kiểm chứng alert `Missing Anti-clickjacking Header` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_admin_basic.json`

### Input

```http
GET http://localhost:5173
```

Headers:
```http
GET http://localhost:5173 HTTP/1.1
host: localhost:5173
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36
pragma: no-cache
cache-control: no-cache
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDk1NzF9.6xPB8cUE63QhefuiiRzG56zhdFE5lbB-b7dUFPwWED0
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `N/A` hoặc hành vi runtime vẫn khớp alert `Missing Anti-clickjacking Header`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-108

- Alert liên quan: ZAP-010
- Mục tiêu test: Kiểm chứng alert `Missing Anti-clickjacking Header` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_admin_basic.json`

### Input

```http
GET http://localhost:5173/
```

Headers:
```http
GET http://localhost:5173/ HTTP/1.1
host: localhost:5173
User-Agent: python-requests/2.32.5
Accept: */*
Connection: keep-alive
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDk1NzF9.6xPB8cUE63QhefuiiRzG56zhdFE5lbB-b7dUFPwWED0
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `N/A` hoặc hành vi runtime vẫn khớp alert `Missing Anti-clickjacking Header`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-109

- Alert liên quan: ZAP-010
- Mục tiêu test: Kiểm chứng alert `Missing Anti-clickjacking Header` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_admin_basic.json`

### Input

```http
GET http://localhost:5173/forgot-password
```

Headers:
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

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `N/A` hoặc hành vi runtime vẫn khớp alert `Missing Anti-clickjacking Header`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-110

- Alert liên quan: ZAP-010
- Mục tiêu test: Kiểm chứng alert `Missing Anti-clickjacking Header` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_admin_basic.json`

### Input

```http
GET http://localhost:5173/robots.txt
```

Headers:
```http
GET http://localhost:5173/robots.txt HTTP/1.1
host: localhost:5173
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36
pragma: no-cache
cache-control: no-cache
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDk1NzF9.6xPB8cUE63QhefuiiRzG56zhdFE5lbB-b7dUFPwWED0
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `N/A` hoặc hành vi runtime vẫn khớp alert `Missing Anti-clickjacking Header`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-111

- Alert liên quan: ZAP-010
- Mục tiêu test: Kiểm chứng alert `Missing Anti-clickjacking Header` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_admin_basic.json`

### Input

```http
GET http://localhost:5173/sitemap.xml
```

Headers:
```http
GET http://localhost:5173/sitemap.xml HTTP/1.1
host: localhost:5173
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36
pragma: no-cache
cache-control: no-cache
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDk1NzF9.6xPB8cUE63QhefuiiRzG56zhdFE5lbB-b7dUFPwWED0
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `N/A` hoặc hành vi runtime vẫn khớp alert `Missing Anti-clickjacking Header`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-112

- Alert liên quan: ZAP-011
- Mục tiêu test: Kiểm chứng alert `Timestamp Disclosure - Unix` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_admin_basic.json`

### Input

```http
GET http://localhost:5173/node_modules/.vite/deps/react-dom_client.js?v=82fd3d9d
```

Headers:
```http
GET http://localhost:5173/node_modules/.vite/deps/react-dom_client.js?v=82fd3d9d HTTP/1.1
host: localhost:5173
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Connection: keep-alive
Referer: http://localhost:5173/src/main.jsx
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDk1NzF9.6xPB8cUE63QhefuiiRzG56zhdFE5lbB-b7dUFPwWED0
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `2080374784` hoặc hành vi runtime vẫn khớp alert `Timestamp Disclosure - Unix`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-113

- Alert liên quan: ZAP-004
- Mục tiêu test: Kiểm chứng alert `X-Content-Type-Options Header Missing` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_admin_basic.json`

### Input

```http
GET http://localhost:5173
```

Headers:
```http
GET http://localhost:5173 HTTP/1.1
host: localhost:5173
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36
pragma: no-cache
cache-control: no-cache
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDk1NzF9.6xPB8cUE63QhefuiiRzG56zhdFE5lbB-b7dUFPwWED0
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `N/A` hoặc hành vi runtime vẫn khớp alert `X-Content-Type-Options Header Missing`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-114

- Alert liên quan: ZAP-004
- Mục tiêu test: Kiểm chứng alert `X-Content-Type-Options Header Missing` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_admin_basic.json`

### Input

```http
GET http://localhost:5173/
```

Headers:
```http
GET http://localhost:5173/ HTTP/1.1
host: localhost:5173
User-Agent: python-requests/2.32.5
Accept: */*
Connection: keep-alive
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDk1NzF9.6xPB8cUE63QhefuiiRzG56zhdFE5lbB-b7dUFPwWED0
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `N/A` hoặc hành vi runtime vẫn khớp alert `X-Content-Type-Options Header Missing`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-115

- Alert liên quan: ZAP-004
- Mục tiêu test: Kiểm chứng alert `X-Content-Type-Options Header Missing` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_admin_basic.json`

### Input

```http
GET http://localhost:5173/favicon.svg
```

Headers:
```http
GET http://localhost:5173/favicon.svg HTTP/1.1
host: localhost:5173
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36
pragma: no-cache
cache-control: no-cache
referer: http://localhost:5173
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDk1NzF9.6xPB8cUE63QhefuiiRzG56zhdFE5lbB-b7dUFPwWED0
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `N/A` hoặc hành vi runtime vẫn khớp alert `X-Content-Type-Options Header Missing`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-116

- Alert liên quan: ZAP-004
- Mục tiêu test: Kiểm chứng alert `X-Content-Type-Options Header Missing` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_admin_basic.json`

### Input

```http
GET http://localhost:5173/robots.txt
```

Headers:
```http
GET http://localhost:5173/robots.txt HTTP/1.1
host: localhost:5173
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36
pragma: no-cache
cache-control: no-cache
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDk1NzF9.6xPB8cUE63QhefuiiRzG56zhdFE5lbB-b7dUFPwWED0
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `N/A` hoặc hành vi runtime vẫn khớp alert `X-Content-Type-Options Header Missing`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-117

- Alert liên quan: ZAP-004
- Mục tiêu test: Kiểm chứng alert `X-Content-Type-Options Header Missing` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_admin_basic.json`

### Input

```http
GET http://localhost:5173/sitemap.xml
```

Headers:
```http
GET http://localhost:5173/sitemap.xml HTTP/1.1
host: localhost:5173
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36
pragma: no-cache
cache-control: no-cache
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDk1NzF9.6xPB8cUE63QhefuiiRzG56zhdFE5lbB-b7dUFPwWED0
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `N/A` hoặc hành vi runtime vẫn khớp alert `X-Content-Type-Options Header Missing`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-118

- Alert liên quan: ZAP-012
- Mục tiêu test: Kiểm chứng alert `Information Disclosure - Sensitive Information in URL` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_admin_basic.json`

### Input

```http
GET http://localhost:5173/?token=7NvYDWb8HNrK
```

Headers:
```http
GET http://localhost:5173/?token=7NvYDWb8HNrK HTTP/1.1
host: localhost:5173
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Sec-WebSocket-Version: 13
Origin: http://localhost:5173
Sec-WebSocket-Protocol: vite-hmr
Sec-WebSocket-Key: /z+7rhddK1vlqzbW2Q9bEg==
Connection: Upgrade
Pragma: no-cache
Cache-Control: no-cache
Upgrade: websocket
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDk1NzF9.6xPB8cUE63QhefuiiRzG56zhdFE5lbB-b7dUFPwWED0
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `token` hoặc hành vi runtime vẫn khớp alert `Information Disclosure - Sensitive Information in URL`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-119

- Alert liên quan: ZAP-013
- Mục tiêu test: Kiểm chứng alert `Information Disclosure - Suspicious Comments` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_admin_basic.json`

### Input

```http
GET http://localhost:5173/@react-refresh
```

Headers:
```http
GET http://localhost:5173/@react-refresh HTTP/1.1
host: localhost:5173
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Connection: keep-alive
Referer: http://localhost:5173/
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDk1NzF9.6xPB8cUE63QhefuiiRzG56zhdFE5lbB-b7dUFPwWED0
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `// TODO: rename these field` hoặc hành vi runtime vẫn khớp alert `Information Disclosure - Suspicious Comments`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-120

- Alert liên quan: ZAP-013
- Mục tiêu test: Kiểm chứng alert `Information Disclosure - Suspicious Comments` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_admin_basic.json`

### Input

```http
GET http://localhost:5173/@react-refresh
```

Headers:
```http
GET http://localhost:5173/@react-refresh HTTP/1.1
host: localhost:5173
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Connection: keep-alive
Referer: http://localhost:5173/
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDk1NzF9.6xPB8cUE63QhefuiiRzG56zhdFE5lbB-b7dUFPwWED0
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `ogic is copy-pasted from similar logic in th` hoặc hành vi runtime vẫn khớp alert `Information Disclosure - Suspicious Comments`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-121

- Alert liên quan: ZAP-013
- Mục tiêu test: Kiểm chứng alert `Information Disclosure - Suspicious Comments` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_admin_basic.json`

### Input

```http
GET http://localhost:5173/node_modules/.vite/deps/axios.js?v=82fd3d9d
```

Headers:
```http
GET http://localhost:5173/node_modules/.vite/deps/axios.js?v=82fd3d9d HTTP/1.1
host: localhost:5173
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Connection: keep-alive
Referer: http://localhost:5173/src/pages/Home.jsx
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDk1NzF9.6xPB8cUE63QhefuiiRzG56zhdFE5lbB-b7dUFPwWED0
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `to copy properties from
* @param {Object} t` hoặc hành vi runtime vẫn khớp alert `Information Disclosure - Suspicious Comments`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-122

- Alert liên quan: ZAP-013
- Mục tiêu test: Kiểm chứng alert `Information Disclosure - Suspicious Comments` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_admin_basic.json`

### Input

```http
GET http://localhost:5173/node_modules/.vite/deps/axios.js?v=82fd3d9d
```

Headers:
```http
GET http://localhost:5173/node_modules/.vite/deps/axios.js?v=82fd3d9d HTTP/1.1
host: localhost:5173
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Connection: keep-alive
Referer: http://localhost:5173/src/pages/Home.jsx
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDk1NzF9.6xPB8cUE63QhefuiiRzG56zhdFE5lbB-b7dUFPwWED0
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `in the same key the later object in
* the arg` hoặc hành vi runtime vẫn khớp alert `Information Disclosure - Suspicious Comments`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-123

- Alert liên quan: ZAP-013
- Mục tiêu test: Kiểm chứng alert `Information Disclosure - Suspicious Comments` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_admin_basic.json`

### Input

```http
GET http://localhost:5173/node_modules/.vite/deps/react-router-dom.js?v=82fd3d9d
```

Headers:
```http
GET http://localhost:5173/node_modules/.vite/deps/react-router-dom.js?v=82fd3d9d HTTP/1.1
host: localhost:5173
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Connection: keep-alive
Referer: http://localhost:5173/src/App.jsx
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDk1NzF9.6xPB8cUE63QhefuiiRzG56zhdFE5lbB-b7dUFPwWED0
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `*
	* Access a value from the context. If no` hoặc hành vi runtime vẫn khớp alert `Information Disclosure - Suspicious Comments`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-124

- Alert liên quan: ZAP-013
- Mục tiêu test: Kiểm chứng alert `Information Disclosure - Suspicious Comments` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_admin_basic.json`

### Input

```http
GET http://localhost:5173/node_modules/.vite/deps/react-router-dom.js?v=82fd3d9d
```

Headers:
```http
GET http://localhost:5173/node_modules/.vite/deps/react-router-dom.js?v=82fd3d9d HTTP/1.1
host: localhost:5173
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Connection: keep-alive
Referer: http://localhost:5173/src/App.jsx
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDk1NzF9.6xPB8cUE63QhefuiiRzG56zhdFE5lbB-b7dUFPwWED0
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `, will
	* cause the user agent to ignore the` hoặc hành vi runtime vẫn khớp alert `Information Disclosure - Suspicious Comments`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-125

- Alert liên quan: ZAP-014
- Mục tiêu test: Kiểm chứng alert `Modern Web Application` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_admin_basic.json`

### Input

```http
GET http://localhost:5173
```

Headers:
```http
GET http://localhost:5173 HTTP/1.1
host: localhost:5173
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36
pragma: no-cache
cache-control: no-cache
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDk1NzF9.6xPB8cUE63QhefuiiRzG56zhdFE5lbB-b7dUFPwWED0
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `<script type="module">import { injectIntoGlobalHook } from "/@react-refresh";
injectIntoGlobalHook(window);
window.$RefreshReg$ = () => {};
window.$RefreshSig$ = () => (type) => type;</script>` hoặc hành vi runtime vẫn khớp alert `Modern Web Application`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-126

- Alert liên quan: ZAP-014
- Mục tiêu test: Kiểm chứng alert `Modern Web Application` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_admin_basic.json`

### Input

```http
GET http://localhost:5173/
```

Headers:
```http
GET http://localhost:5173/ HTTP/1.1
host: localhost:5173
User-Agent: python-requests/2.32.5
Accept: */*
Connection: keep-alive
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDk1NzF9.6xPB8cUE63QhefuiiRzG56zhdFE5lbB-b7dUFPwWED0
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `<script type="module">import { injectIntoGlobalHook } from "/@react-refresh";
injectIntoGlobalHook(window);
window.$RefreshReg$ = () => {};
window.$RefreshSig$ = () => (type) => type;</script>` hoặc hành vi runtime vẫn khớp alert `Modern Web Application`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-127

- Alert liên quan: ZAP-014
- Mục tiêu test: Kiểm chứng alert `Modern Web Application` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_admin_basic.json`

### Input

```http
GET http://localhost:5173/forgot-password
```

Headers:
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

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `<script type="module">import { injectIntoGlobalHook } from "/@react-refresh";
injectIntoGlobalHook(window);
window.$RefreshReg$ = () => {};
window.$RefreshSig$ = () => (type) => type;</script>` hoặc hành vi runtime vẫn khớp alert `Modern Web Application`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-128

- Alert liên quan: ZAP-014
- Mục tiêu test: Kiểm chứng alert `Modern Web Application` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_admin_basic.json`

### Input

```http
GET http://localhost:5173/robots.txt
```

Headers:
```http
GET http://localhost:5173/robots.txt HTTP/1.1
host: localhost:5173
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36
pragma: no-cache
cache-control: no-cache
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDk1NzF9.6xPB8cUE63QhefuiiRzG56zhdFE5lbB-b7dUFPwWED0
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `<script type="module">import { injectIntoGlobalHook } from "/@react-refresh";
injectIntoGlobalHook(window);
window.$RefreshReg$ = () => {};
window.$RefreshSig$ = () => (type) => type;</script>` hoặc hành vi runtime vẫn khớp alert `Modern Web Application`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-129

- Alert liên quan: ZAP-014
- Mục tiêu test: Kiểm chứng alert `Modern Web Application` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_admin_basic.json`

### Input

```http
GET http://localhost:5173/sitemap.xml
```

Headers:
```http
GET http://localhost:5173/sitemap.xml HTTP/1.1
host: localhost:5173
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36
pragma: no-cache
cache-control: no-cache
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDk1NzF9.6xPB8cUE63QhefuiiRzG56zhdFE5lbB-b7dUFPwWED0
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `<script type="module">import { injectIntoGlobalHook } from "/@react-refresh";
injectIntoGlobalHook(window);
window.$RefreshReg$ = () => {};
window.$RefreshSig$ = () => (type) => type;</script>` hoặc hành vi runtime vẫn khớp alert `Modern Web Application`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-130

- Alert liên quan: ZAP-001
- Mục tiêu test: Kiểm chứng alert `CSP: Failure to Define Directive with No Fallback` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_admin_basic.json`

### Input

```http
GET http://localhost:3000
```

Headers:
```http
GET http://localhost:3000 HTTP/1.1
host: localhost:3000
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36
pragma: no-cache
cache-control: no-cache
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDkwNzV9.mOzLCI5uoLpBGWGMZ2PY7Y00zv3jSMAC2u4oQUHcVhc
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `default-src 'none'` hoặc hành vi runtime vẫn khớp alert `CSP: Failure to Define Directive with No Fallback`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-131

- Alert liên quan: ZAP-001
- Mục tiêu test: Kiểm chứng alert `CSP: Failure to Define Directive with No Fallback` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_admin_basic.json`

### Input

```http
GET http://localhost:3000/
```

Headers:
```http
GET http://localhost:3000/ HTTP/1.1
host: localhost:3000
User-Agent: python-requests/2.32.5
Accept: */*
Connection: keep-alive
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDkwNzV9.mOzLCI5uoLpBGWGMZ2PY7Y00zv3jSMAC2u4oQUHcVhc
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `default-src 'none'` hoặc hành vi runtime vẫn khớp alert `CSP: Failure to Define Directive with No Fallback`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-132

- Alert liên quan: ZAP-001
- Mục tiêu test: Kiểm chứng alert `CSP: Failure to Define Directive with No Fallback` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_admin_basic.json`

### Input

```http
GET http://localhost:3000/api
```

Headers:
```http
GET http://localhost:3000/api HTTP/1.1
host: localhost:3000
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36
pragma: no-cache
cache-control: no-cache
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDkwNzV9.mOzLCI5uoLpBGWGMZ2PY7Y00zv3jSMAC2u4oQUHcVhc
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `default-src 'none'` hoặc hành vi runtime vẫn khớp alert `CSP: Failure to Define Directive with No Fallback`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-133

- Alert liên quan: ZAP-001
- Mục tiêu test: Kiểm chứng alert `CSP: Failure to Define Directive with No Fallback` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_admin_basic.json`

### Input

```http
GET http://localhost:3000/robots.txt
```

Headers:
```http
GET http://localhost:3000/robots.txt HTTP/1.1
host: localhost:3000
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36
pragma: no-cache
cache-control: no-cache
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDkwNzV9.mOzLCI5uoLpBGWGMZ2PY7Y00zv3jSMAC2u4oQUHcVhc
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `default-src 'none'` hoặc hành vi runtime vẫn khớp alert `CSP: Failure to Define Directive with No Fallback`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-134

- Alert liên quan: ZAP-001
- Mục tiêu test: Kiểm chứng alert `CSP: Failure to Define Directive with No Fallback` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_admin_basic.json`

### Input

```http
GET http://localhost:3000/sitemap.xml
```

Headers:
```http
GET http://localhost:3000/sitemap.xml HTTP/1.1
host: localhost:3000
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36
pragma: no-cache
cache-control: no-cache
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDkwNzV9.mOzLCI5uoLpBGWGMZ2PY7Y00zv3jSMAC2u4oQUHcVhc
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `default-src 'none'` hoặc hành vi runtime vẫn khớp alert `CSP: Failure to Define Directive with No Fallback`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-135

- Alert liên quan: ZAP-002
- Mục tiêu test: Kiểm chứng alert `Cross-Domain Misconfiguration` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_admin_basic.json`

### Input

```http
GET http://localhost:3000
```

Headers:
```http
GET http://localhost:3000 HTTP/1.1
host: localhost:3000
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36
pragma: no-cache
cache-control: no-cache
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDkwNzV9.mOzLCI5uoLpBGWGMZ2PY7Y00zv3jSMAC2u4oQUHcVhc
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `Access-Control-Allow-Origin: *` hoặc hành vi runtime vẫn khớp alert `Cross-Domain Misconfiguration`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-136

- Alert liên quan: ZAP-002
- Mục tiêu test: Kiểm chứng alert `Cross-Domain Misconfiguration` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_admin_basic.json`

### Input

```http
GET http://localhost:3000/
```

Headers:
```http
GET http://localhost:3000/ HTTP/1.1
host: localhost:3000
User-Agent: python-requests/2.32.5
Accept: */*
Connection: keep-alive
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDkwNzV9.mOzLCI5uoLpBGWGMZ2PY7Y00zv3jSMAC2u4oQUHcVhc
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `Access-Control-Allow-Origin: *` hoặc hành vi runtime vẫn khớp alert `Cross-Domain Misconfiguration`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-137

- Alert liên quan: ZAP-002
- Mục tiêu test: Kiểm chứng alert `Cross-Domain Misconfiguration` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_admin_basic.json`

### Input

```http
GET http://localhost:3000/api/users/me
```

Headers:
```http
GET http://localhost:3000/api/users/me HTTP/1.1
host: localhost:3000
User-Agent: Python-urllib/3.14
Connection: close
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDkwNzV9.mOzLCI5uoLpBGWGMZ2PY7Y00zv3jSMAC2u4oQUHcVhc
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `Access-Control-Allow-Origin: *` hoặc hành vi runtime vẫn khớp alert `Cross-Domain Misconfiguration`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-138

- Alert liên quan: ZAP-002
- Mục tiêu test: Kiểm chứng alert `Cross-Domain Misconfiguration` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_admin_basic.json`

### Input

```http
GET http://localhost:3000/sitemap.xml
```

Headers:
```http
GET http://localhost:3000/sitemap.xml HTTP/1.1
host: localhost:3000
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36
pragma: no-cache
cache-control: no-cache
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDkwNzV9.mOzLCI5uoLpBGWGMZ2PY7Y00zv3jSMAC2u4oQUHcVhc
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `Access-Control-Allow-Origin: *` hoặc hành vi runtime vẫn khớp alert `Cross-Domain Misconfiguration`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-139

- Alert liên quan: ZAP-003
- Mục tiêu test: Kiểm chứng alert `Server Leaks Information via "X-Powered-By" HTTP Response Header Field(s)` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_admin_basic.json`

### Input

```http
GET http://localhost:3000
```

Headers:
```http
GET http://localhost:3000 HTTP/1.1
host: localhost:3000
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36
pragma: no-cache
cache-control: no-cache
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDkwNzV9.mOzLCI5uoLpBGWGMZ2PY7Y00zv3jSMAC2u4oQUHcVhc
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `X-Powered-By: Express` hoặc hành vi runtime vẫn khớp alert `Server Leaks Information via "X-Powered-By" HTTP Response Header Field(s)`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-140

- Alert liên quan: ZAP-003
- Mục tiêu test: Kiểm chứng alert `Server Leaks Information via "X-Powered-By" HTTP Response Header Field(s)` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_admin_basic.json`

### Input

```http
GET http://localhost:3000/
```

Headers:
```http
GET http://localhost:3000/ HTTP/1.1
host: localhost:3000
User-Agent: python-requests/2.32.5
Accept: */*
Connection: keep-alive
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDkwNzV9.mOzLCI5uoLpBGWGMZ2PY7Y00zv3jSMAC2u4oQUHcVhc
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `X-Powered-By: Express` hoặc hành vi runtime vẫn khớp alert `Server Leaks Information via "X-Powered-By" HTTP Response Header Field(s)`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-141

- Alert liên quan: ZAP-003
- Mục tiêu test: Kiểm chứng alert `Server Leaks Information via "X-Powered-By" HTTP Response Header Field(s)` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_admin_basic.json`

### Input

```http
GET http://localhost:3000/api/users/me
```

Headers:
```http
GET http://localhost:3000/api/users/me HTTP/1.1
host: localhost:3000
User-Agent: Python-urllib/3.14
Connection: close
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDkwNzV9.mOzLCI5uoLpBGWGMZ2PY7Y00zv3jSMAC2u4oQUHcVhc
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `X-Powered-By: Express` hoặc hành vi runtime vẫn khớp alert `Server Leaks Information via "X-Powered-By" HTTP Response Header Field(s)`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-142

- Alert liên quan: ZAP-003
- Mục tiêu test: Kiểm chứng alert `Server Leaks Information via "X-Powered-By" HTTP Response Header Field(s)` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_admin_basic.json`

### Input

```http
GET http://localhost:3000/robots.txt
```

Headers:
```http
GET http://localhost:3000/robots.txt HTTP/1.1
host: localhost:3000
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36
pragma: no-cache
cache-control: no-cache
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDkwNzV9.mOzLCI5uoLpBGWGMZ2PY7Y00zv3jSMAC2u4oQUHcVhc
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `X-Powered-By: Express` hoặc hành vi runtime vẫn khớp alert `Server Leaks Information via "X-Powered-By" HTTP Response Header Field(s)`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-143

- Alert liên quan: ZAP-003
- Mục tiêu test: Kiểm chứng alert `Server Leaks Information via "X-Powered-By" HTTP Response Header Field(s)` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_admin_basic.json`

### Input

```http
POST http://localhost:3000/api/login
```

Headers:
```http
POST http://localhost:3000/api/login HTTP/1.1
Content-Length: 52
host: localhost:3000
User-Agent: Python-urllib/3.14
Content-Type: application/json
Connection: close
```

Payload:
```json
{"email": "test@eshop.com", "password": "Test1234!"}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `X-Powered-By: Express` hoặc hành vi runtime vẫn khớp alert `Server Leaks Information via "X-Powered-By" HTTP Response Header Field(s)`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-144

- Alert liên quan: ZAP-004
- Mục tiêu test: Kiểm chứng alert `X-Content-Type-Options Header Missing` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_admin_basic.json`

### Input

```http
GET http://localhost:3000/api/products?search=
```

Headers:
```http
GET http://localhost:3000/api/products?search= HTTP/1.1
host: localhost:3000
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0
Accept: application/json, text/plain, */*
Accept-Language: en-US,en;q=0.5
Origin: http://localhost:5173
Connection: keep-alive
Referer: http://localhost:5173/
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDk1NzF9.6xPB8cUE63QhefuiiRzG56zhdFE5lbB-b7dUFPwWED0
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `N/A` hoặc hành vi runtime vẫn khớp alert `X-Content-Type-Options Header Missing`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-145

- Alert liên quan: ZAP-004
- Mục tiêu test: Kiểm chứng alert `X-Content-Type-Options Header Missing` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_admin_basic.json`

### Input

```http
GET http://localhost:3000/api/products/1
```

Headers:
```http
GET http://localhost:3000/api/products/1 HTTP/1.1
host: localhost:3000
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0
Accept: application/json, text/plain, */*
Accept-Language: en-US,en;q=0.5
Origin: http://localhost:5173
Connection: keep-alive
Referer: http://localhost:5173/
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDk1NzF9.6xPB8cUE63QhefuiiRzG56zhdFE5lbB-b7dUFPwWED0
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `N/A` hoặc hành vi runtime vẫn khớp alert `X-Content-Type-Options Header Missing`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-146

- Alert liên quan: ZAP-004
- Mục tiêu test: Kiểm chứng alert `X-Content-Type-Options Header Missing` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_admin_basic.json`

### Input

```http
GET http://localhost:3000/api/products/2
```

Headers:
```http
GET http://localhost:3000/api/products/2 HTTP/1.1
host: localhost:3000
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0
Accept: application/json, text/plain, */*
Accept-Language: en-US,en;q=0.5
Origin: http://localhost:5173
Connection: keep-alive
Referer: http://localhost:5173/
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDk1NzF9.6xPB8cUE63QhefuiiRzG56zhdFE5lbB-b7dUFPwWED0
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `N/A` hoặc hành vi runtime vẫn khớp alert `X-Content-Type-Options Header Missing`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-147

- Alert liên quan: ZAP-004
- Mục tiêu test: Kiểm chứng alert `X-Content-Type-Options Header Missing` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_admin_basic.json`

### Input

```http
GET http://localhost:3000/api/users/me
```

Headers:
```http
GET http://localhost:3000/api/users/me HTTP/1.1
host: localhost:3000
User-Agent: Python-urllib/3.14
Connection: close
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDkwNzV9.mOzLCI5uoLpBGWGMZ2PY7Y00zv3jSMAC2u4oQUHcVhc
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `N/A` hoặc hành vi runtime vẫn khớp alert `X-Content-Type-Options Header Missing`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-148

- Alert liên quan: ZAP-004
- Mục tiêu test: Kiểm chứng alert `X-Content-Type-Options Header Missing` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_admin_basic.json`

### Input

```http
POST http://localhost:3000/api/login
```

Headers:
```http
POST http://localhost:3000/api/login HTTP/1.1
Content-Length: 52
host: localhost:3000
User-Agent: Python-urllib/3.14
Content-Type: application/json
Connection: close
```

Payload:
```json
{"email": "test@eshop.com", "password": "Test1234!"}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `N/A` hoặc hành vi runtime vẫn khớp alert `X-Content-Type-Options Header Missing`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-149

- Alert liên quan: ZAP-005
- Mục tiêu test: Kiểm chứng alert `Authentication Request Identified` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_admin_basic.json`

### Input

```http
POST http://localhost:3000/api/login
```

Headers:
```http
POST http://localhost:3000/api/login HTTP/1.1
Content-Length: 52
host: localhost:3000
User-Agent: Python-urllib/3.14
Content-Type: application/json
Connection: close
```

Payload:
```json
{"email": "test@eshop.com", "password": "Test1234!"}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `password` hoặc hành vi runtime vẫn khớp alert `Authentication Request Identified`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-150

- Alert liên quan: ZAP-006
- Mục tiêu test: Kiểm chứng alert `Session Management Response Identified` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_admin_basic.json`

### Input

```http
POST http://localhost:3000/api/login
```

Headers:
```http
POST http://localhost:3000/api/login HTTP/1.1
Content-Length: 52
host: localhost:3000
User-Agent: Python-urllib/3.14
Content-Type: application/json
Connection: close
```

Payload:
```json
{"email": "test@eshop.com", "password": "Test1234!"}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `token` hoặc hành vi runtime vẫn khớp alert `Session Management Response Identified`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-151

- Alert liên quan: ZAP-006
- Mục tiêu test: Kiểm chứng alert `Session Management Response Identified` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_admin_basic.json`

### Input

```http
POST http://localhost:3000/api/login
```

Headers:
```http
POST http://localhost:3000/api/login HTTP/1.1
Content-Length: 52
host: localhost:3000
User-Agent: Python-urllib/3.14
Content-Type: application/json
Connection: close
```

Payload:
```json
{"email": "test@eshop.com", "password": "Test1234!"}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `token` hoặc hành vi runtime vẫn khớp alert `Session Management Response Identified`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-152

- Alert liên quan: ZAP-007
- Mục tiêu test: Kiểm chứng alert `User Agent Fuzzer` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_admin_basic.json`

### Input

```http
GET http://localhost:3000/api/users/me
```

Headers:
```http
GET http://localhost:3000/api/users/me HTTP/1.1
host: localhost:3000
user-agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)
pragma: no-cache
cache-control: no-cache
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDkwNzV9.mOzLCI5uoLpBGWGMZ2PY7Y00zv3jSMAC2u4oQUHcVhc
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `N/A` hoặc hành vi runtime vẫn khớp alert `User Agent Fuzzer`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-153

- Alert liên quan: ZAP-007
- Mục tiêu test: Kiểm chứng alert `User Agent Fuzzer` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_admin_basic.json`

### Input

```http
GET http://localhost:3000/api/users/me
```

Headers:
```http
GET http://localhost:3000/api/users/me HTTP/1.1
host: localhost:3000
user-agent: Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1)
pragma: no-cache
cache-control: no-cache
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDkwNzV9.mOzLCI5uoLpBGWGMZ2PY7Y00zv3jSMAC2u4oQUHcVhc
```

Payload:
```json
{}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `N/A` hoặc hành vi runtime vẫn khớp alert `User Agent Fuzzer`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## TC-ZAP-154

- Alert liên quan: ZAP-007
- Mục tiêu test: Kiểm chứng alert `User Agent Fuzzer` bằng cách replay request runtime mà ZAP đã ghi nhận.
- Source JSON: `frontend_admin_basic.json`

### Input

```http
POST http://localhost:3000/api/login
```

Headers:
```http
POST http://localhost:3000/api/login HTTP/1.1
Content-Length: 52
host: localhost:3000
user-agent: Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1)
Content-Type: application/json
Connection: close
```

Payload:
```json
{"email": "test@eshop.com", "password": "Test1234!"}
```

### Thao tác

1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.
2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.
3. Replay request theo method, URL, headers từ ZAP.
4. Ghi nhận status code, response headers và response body.
5. So sánh kết quả mới với evidence ZAP trong triage report.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Response vẫn chứa evidence `N/A` hoặc hành vi runtime vẫn khớp alert `User Agent Fuzzer`.
- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.

### Trạng thái

Chưa kiểm chứng

## Ghi chú sử dụng

- `Alert liên quan` trỏ về ID alert trong `zap_triage_report.md`.
- ZAP có thể ghi nhận endpoint ngoài phạm vi nếu browser hoặc môi trường runtime gọi domain khác; dùng `--target-prefix` để lọc target chính.
- Với endpoint yêu cầu đăng nhập, tester cần tái tạo auth context trước khi replay request.
- Kết luận cuối cùng vẫn phân loại theo `True Positive`, `False Positive`, hoặc `Needs Human Review`.
