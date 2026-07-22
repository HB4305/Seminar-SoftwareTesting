# Danh sách test case kiểm chứng Semgrep

Tài liệu này tổng hợp test case kiểm chứng cho các finding Semgrep theo từng entry riêng. Mỗi entry có liên kết về finding gốc để reviewer biết test case đang xác minh cảnh báo nào.

## TC-SEMGREP-001

- Finding liên quan: SEMGREP-001
- Mục tiêu test: Kiểm tra backend có chấp nhận JWT giả được ký bằng hardcoded secret hay không.

### Input

```http
GET http://localhost:3000/api/users/me
```

Headers:
```http
Authorization: Bearer <forged_admin_jwt>
Content-Type: application/json
```

Payload:
Không có request body.

- Nguồn payload: Suy luận từ HTTP method không sử dụng request body.
- Độ tin cậy payload: High

### Thao tác

1. Dùng `src/semgrep/exploit.js` để tạo JWT giả.
2. Copy token sinh ra vào header Authorization.
3. Đảm bảo backend EShop đang chạy tại port 3000.

Gửi request và ghi nhận status code, response body.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Server trả `200 OK` và chấp nhận token giả.
- Nếu đã an toàn: Server trả `401 Unauthorized` hoặc `403 Forbidden`.

### Trạng thái

Chưa kiểm chứng

## TC-SEMGREP-002

- Finding liên quan: SEMGREP-002
- Mục tiêu test: Kiểm tra backend có chấp nhận JWT giả được ký bằng hardcoded secret hay không.

### Input

```http
GET http://localhost:3000/api/users/me
```

Headers:
```http
Authorization: Bearer <forged_admin_jwt>
Content-Type: application/json
```

Payload:
Không có request body.

- Nguồn payload: Suy luận từ HTTP method không sử dụng request body.
- Độ tin cậy payload: High

### Thao tác

1. Dùng `src/semgrep/exploit.js` để tạo JWT giả.
2. Copy token sinh ra vào header Authorization.
3. Đảm bảo backend EShop đang chạy tại port 3000.

Gửi request và ghi nhận status code, response body.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Server trả `200 OK` và chấp nhận token giả.
- Nếu đã an toàn: Server trả `401 Unauthorized` hoặc `403 Forbidden`.

### Trạng thái

Chưa kiểm chứng

## TC-SEMGREP-003

- Finding liên quan: SEMGREP-003
- Mục tiêu test: Kiểm tra backend có chấp nhận JWT giả được ký bằng hardcoded secret hay không.

### Input

```http
GET http://localhost:3000/api/users/me
```

Headers:
```http
Authorization: Bearer <forged_admin_jwt>
Content-Type: application/json
```

Payload:
Không có request body.

- Nguồn payload: Suy luận từ HTTP method không sử dụng request body.
- Độ tin cậy payload: High

### Thao tác

1. Dùng `src/semgrep/exploit.js` để tạo JWT giả.
2. Copy token sinh ra vào header Authorization.
3. Đảm bảo backend EShop đang chạy tại port 3000.

Gửi request và ghi nhận status code, response body.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Server trả `200 OK` và chấp nhận token giả.
- Nếu đã an toàn: Server trả `401 Unauthorized` hoặc `403 Forbidden`.

### Trạng thái

Chưa kiểm chứng

## TC-SEMGREP-004

- Finding liên quan: SEMGREP-004
- Mục tiêu test: Kiểm tra request đang dùng HTTP cleartext thay vì HTTPS.

### Input

```http
GET http://localhost:3000/api/orders/my-orders
```

Headers:
```http
Content-Type: application/json
```

Payload:
Không có request body.

- Nguồn payload: Suy luận từ HTTP method không sử dụng request body.
- Độ tin cậy payload: High

### Thao tác

1. Mở source line được Semgrep báo để xác nhận API path.
2. Đảm bảo backend/frontend local đang chạy.
3. Gửi request bằng Postman và ghi nhận URL đang dùng HTTP.

Gửi request và ghi nhận status code, response body.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Request gọi thành công qua `http://` hoặc dữ liệu nhạy cảm đi qua kênh không mã hóa.
- Nếu đã an toàn: Ứng dụng dùng `https://` hoặc cấu hình base URL an toàn theo môi trường.

### Trạng thái

Chưa kiểm chứng

## TC-SEMGREP-005

- Finding liên quan: SEMGREP-005
- Mục tiêu test: Kiểm tra request đang dùng HTTP cleartext thay vì HTTPS.

### Input

```http
POST http://localhost:3000/api/login
```

Headers:
```http
Content-Type: application/json
```

Payload mẫu:
```json
{
  "email": "{{test_email}}",
  "password": "{{test_password}}"
}
```

- Nguồn payload: Tự động suy luận từ `body: JSON.stringify(...)` trong source.
- Độ tin cậy payload: High
- Thay các biến `{{...}}` bằng giá trị Postman environment trước khi chạy PoC.

### Thao tác

1. Mở source line được Semgrep báo để xác nhận API path.
2. Đảm bảo backend/frontend local đang chạy.
3. Gửi request bằng Postman và ghi nhận URL đang dùng HTTP.

Gửi request và ghi nhận status code, response body.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Request gọi thành công qua `http://` hoặc dữ liệu nhạy cảm đi qua kênh không mã hóa.
- Nếu đã an toàn: Ứng dụng dùng `https://` hoặc cấu hình base URL an toàn theo môi trường.

### Trạng thái

Chưa kiểm chứng

## TC-SEMGREP-006

- Finding liên quan: SEMGREP-006
- Mục tiêu test: Kiểm tra request đang dùng HTTP cleartext thay vì HTTPS.

### Input

```http
POST http://localhost:3000/api/register
```

Headers:
```http
Content-Type: application/json
```

Payload mẫu:
```json
{
  "name": "{{test_name}}",
  "email": "{{test_email}}",
  "password": "{{test_password}}"
}
```

- Nguồn payload: Tự động suy luận từ `body: JSON.stringify(...)` trong source.
- Độ tin cậy payload: High
- Thay các biến `{{...}}` bằng giá trị Postman environment trước khi chạy PoC.

### Thao tác

1. Mở source line được Semgrep báo để xác nhận API path.
2. Đảm bảo backend/frontend local đang chạy.
3. Gửi request bằng Postman và ghi nhận URL đang dùng HTTP.

Gửi request và ghi nhận status code, response body.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Request gọi thành công qua `http://` hoặc dữ liệu nhạy cảm đi qua kênh không mã hóa.
- Nếu đã an toàn: Ứng dụng dùng `https://` hoặc cấu hình base URL an toàn theo môi trường.

### Trạng thái

Chưa kiểm chứng

## TC-SEMGREP-007

- Finding liên quan: SEMGREP-007
- Mục tiêu test: Kiểm tra request đang dùng HTTP cleartext thay vì HTTPS.

### Input

```http
POST http://localhost:3000/api/forgot-password
```

Headers:
```http
Content-Type: application/json
```

Payload mẫu:
```json
{
  "email": "{{test_email}}"
}
```

- Nguồn payload: Tự động suy luận từ `body: JSON.stringify(...)` trong source.
- Độ tin cậy payload: High
- Thay các biến `{{...}}` bằng giá trị Postman environment trước khi chạy PoC.

### Thao tác

1. Mở source line được Semgrep báo để xác nhận API path.
2. Đảm bảo backend/frontend local đang chạy.
3. Gửi request bằng Postman và ghi nhận URL đang dùng HTTP.

Gửi request và ghi nhận status code, response body.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Request gọi thành công qua `http://` hoặc dữ liệu nhạy cảm đi qua kênh không mã hóa.
- Nếu đã an toàn: Ứng dụng dùng `https://` hoặc cấu hình base URL an toàn theo môi trường.

### Trạng thái

Chưa kiểm chứng

## TC-SEMGREP-008

- Finding liên quan: SEMGREP-008
- Mục tiêu test: Kiểm tra request đang dùng HTTP cleartext thay vì HTTPS.

### Input

```http
POST http://localhost:3000/api/reset-password
```

Headers:
```http
Content-Type: application/json
```

Payload mẫu:
```json
{
  "email": "{{test_email}}",
  "resetToken": "{{reset_token}}",
  "newPassword": "{{new_password}}"
}
```

- Nguồn payload: Tự động suy luận từ `body: JSON.stringify(...)` trong source.
- Độ tin cậy payload: High
- Thay các biến `{{...}}` bằng giá trị Postman environment trước khi chạy PoC.

### Thao tác

1. Mở source line được Semgrep báo để xác nhận API path.
2. Đảm bảo backend/frontend local đang chạy.
3. Gửi request bằng Postman và ghi nhận URL đang dùng HTTP.

Gửi request và ghi nhận status code, response body.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Request gọi thành công qua `http://` hoặc dữ liệu nhạy cảm đi qua kênh không mã hóa.
- Nếu đã an toàn: Ứng dụng dùng `https://` hoặc cấu hình base URL an toàn theo môi trường.

### Trạng thái

Chưa kiểm chứng

## TC-SEMGREP-009

- Finding liên quan: SEMGREP-009
- Mục tiêu test: Kiểm tra request đang dùng HTTP cleartext thay vì HTTPS.

### Input

```http
PUT http://localhost:3000/api/users/me
```

Headers:
```http
Content-Type: application/json
```

Payload mẫu:
```json
{
  "name": "{{test_name}}",
  "phone": "{{test_phone}}",
  "shippingAddress": "{{shipping_address}}"
}
```

- Nguồn payload: Tự động suy luận từ `body: JSON.stringify(...)` trong source.
- Độ tin cậy payload: High
- Thay các biến `{{...}}` bằng giá trị Postman environment trước khi chạy PoC.

### Thao tác

1. Mở source line được Semgrep báo để xác nhận API path.
2. Đảm bảo backend/frontend local đang chạy.
3. Gửi request bằng Postman và ghi nhận URL đang dùng HTTP.

Gửi request và ghi nhận status code, response body.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Request gọi thành công qua `http://` hoặc dữ liệu nhạy cảm đi qua kênh không mã hóa.
- Nếu đã an toàn: Ứng dụng dùng `https://` hoặc cấu hình base URL an toàn theo môi trường.

### Trạng thái

Chưa kiểm chứng

## TC-SEMGREP-010

- Finding liên quan: SEMGREP-010
- Mục tiêu test: Kiểm tra request đang dùng HTTP cleartext thay vì HTTPS.

### Input

```http
POST http://localhost:3000/api/apply-coupon
```

Headers:
```http
Content-Type: application/json
```

Payload mẫu:
```json
{
  "code": "{{coupon_code}}",
  "total_amount": 100000,
  "user_id": "{{user_id}}"
}
```

- Nguồn payload: Tự động suy luận từ `body: JSON.stringify(...)` trong source.
- Độ tin cậy payload: High
- Thay các biến `{{...}}` bằng giá trị Postman environment trước khi chạy PoC.

### Thao tác

1. Mở source line được Semgrep báo để xác nhận API path.
2. Đảm bảo backend/frontend local đang chạy.
3. Gửi request bằng Postman và ghi nhận URL đang dùng HTTP.

Gửi request và ghi nhận status code, response body.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Request gọi thành công qua `http://` hoặc dữ liệu nhạy cảm đi qua kênh không mã hóa.
- Nếu đã an toàn: Ứng dụng dùng `https://` hoặc cấu hình base URL an toàn theo môi trường.

### Trạng thái

Chưa kiểm chứng

## TC-SEMGREP-011

- Finding liên quan: SEMGREP-011
- Mục tiêu test: Kiểm tra request đang dùng HTTP cleartext thay vì HTTPS.

### Input

```http
POST http://localhost:3000/api/checkout
```

Headers:
```http
Content-Type: application/json
```

Payload mẫu:
```json
{
  "items": [
    {
      "product_id": "{{product_id}}",
      "quantity": 1,
      "price": 100000
    }
  ],
  "total_amount": 100000,
  "coupon_id": null
}
```

- Nguồn payload: Tự động suy luận từ `body: JSON.stringify(...)` trong source.
- Độ tin cậy payload: High
- Thay các biến `{{...}}` bằng giá trị Postman environment trước khi chạy PoC.

### Thao tác

1. Mở source line được Semgrep báo để xác nhận API path.
2. Đảm bảo backend/frontend local đang chạy.
3. Gửi request bằng Postman và ghi nhận URL đang dùng HTTP.

Gửi request và ghi nhận status code, response body.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Request gọi thành công qua `http://` hoặc dữ liệu nhạy cảm đi qua kênh không mã hóa.
- Nếu đã an toàn: Ứng dụng dùng `https://` hoặc cấu hình base URL an toàn theo môi trường.

### Trạng thái

Chưa kiểm chứng

## TC-SEMGREP-012

- Finding liên quan: SEMGREP-012
- Mục tiêu test: Kiểm tra request đang dùng HTTP cleartext thay vì HTTPS.

### Input

```http
POST http://localhost:3000/api/coupon-usage
```

Headers:
```http
Content-Type: application/json
```

Payload mẫu:
```json
{
  "coupon_id": "{{coupon_id}}"
}
```

- Nguồn payload: Tự động suy luận từ `body: JSON.stringify(...)` trong source.
- Độ tin cậy payload: High
- Thay các biến `{{...}}` bằng giá trị Postman environment trước khi chạy PoC.

### Thao tác

1. Mở source line được Semgrep báo để xác nhận API path.
2. Đảm bảo backend/frontend local đang chạy.
3. Gửi request bằng Postman và ghi nhận URL đang dùng HTTP.

Gửi request và ghi nhận status code, response body.

### Kết quả cần ghi nhận

- Nếu còn lỗi: Request gọi thành công qua `http://` hoặc dữ liệu nhạy cảm đi qua kênh không mã hóa.
- Nếu đã an toàn: Ứng dụng dùng `https://` hoặc cấu hình base URL an toàn theo môi trường.

### Trạng thái

Chưa kiểm chứng

## Ghi chú sử dụng

- `Finding liên quan` trỏ về ID finding trong `semgrep_triage_report.md`.
- Với finding chưa map được endpoint thật, tester cần đọc source evidence rồi điền lại URL/header/payload trước khi kiểm chứng.
- Kết quả cuối cùng vẫn phân loại theo `True Positive`, `False Positive`, hoặc `Needs Human Review`.
