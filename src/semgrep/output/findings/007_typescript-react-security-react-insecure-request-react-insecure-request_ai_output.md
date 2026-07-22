Tuyệt vời, tôi sẽ đóng vai trò là chuyên gia bảo mật ứng dụng để tiến hành triage finding của Semgrep này.

---

## Triage Finding Bảo Mật

**Mã finding:** SEMGREP-007
**Rule ID:** typescript.react.security.react-insecure-request.react-insecure-request
**File nguồn:** eshop-sut/frontend-mobile/App.js
**Dòng:** 244
**Severity:** ERROR
**CWE:** CWE-319: Cleartext Transmission of Sensitive Information
**OWASP:** A03:2017 - Sensitive Data Exposure, A02:2021 - Cryptographic Failures, A04:2025 - Cryptographic Failures
**Likelihood:** LOW
**Impact:** MEDIUM
**Confidence:** MEDIUM
**Cảnh báo Semgrep:** Unencrypted request over HTTP detected.

---

### 1. Phân loại:

Needs Human Review

### 2. Lý do phân loại dựa trên source evidence:

Rule của Semgrep phát hiện việc sử dụng `fetch` để gửi request đến `${API_URL}/forgot-password` mà không có ngữ cảnh rõ ràng về giao thức (`http` hay `https`). Tuy nhiên, **bằng chứng mã nguồn (source evidence)** chỉ hiển thị cách tạo URL request mà không cho thấy nội dung hoặc cách `API_URL` được định nghĩa.

Vì Semgrep là SAST, nó chỉ phân tích mã nguồn tĩnh. Trong bối cảnh ứng dụng EShop đang được quét như một lab local trên `localhost`, việc sử dụng `http` cho các request nội bộ có thể là hành vi mong muốn trong môi trường phát triển và không nhất thiết dẫn đến rủi ro bảo mật ở môi trường đó. Tuy nhiên, chúng ta không có đủ thông tin về cách `API_URL` được cấu hình cho các môi trường khác nhau (ví dụ: staging, production).

Nếu `API_URL` có thể được cấu hình để trỏ đến máy chủ HTTP bên ngoài môi trường lab và người dùng có thể tương tác với tính năng này trên môi trường đó, thì đây sẽ là một lỗ hổng **True Positive**. Ngược lại, nếu `API_URL` luôn được cấu hình với `https` ở môi trường production hoặc chỉ sử dụng cho mục đích test nội bộ không có dữ liệu nhạy cảm, thì đây có thể là **False Positive**.

### 3. Tác động thực tế trong bối cảnh EShop:

Nếu `API_URL` đang sử dụng protocol HTTP (không mã hóa) để gửi dữ liệu, đặc biệt là dữ liệu liên quan đến việc khôi phục mật khẩu (ví dụ: địa chỉ email người dùng, token khôi phục mật khẩu), thì thông tin này có thể bị đánh cắp bởi kẻ tấn công nghe lén trên mạng (man-in-the-middle attack). Điều này sẽ dẫn đến **Sensitive Data Exposure** (OWASP A03:2017) và **Cryptographic Failures** (OWASP A02:2021, A04:2025) nếu email chứa thông tin nhạy cảm.

Tuy nhiên, trong bối cảnh "ứng dụng lab local" và việc finding liên quan đến `localhost`, tác động thực tế có thể thấp nếu môi trường lab này không có bất kỳ người dùng thật nào và chỉ dùng cho mục đích thử nghiệm. Rủi ro chỉ tăng lên khi `API_URL` được cấu hình cho môi trường production hoặc các môi trường khác có người dùng thực.

### 4. Cách khắc phục cụ thể:

1.  **Cấu hình HTTPS cho API Server:** Đảm bảo rằng API server mà `API_URL` trỏ tới luôn sử dụng HTTPS để mã hóa tất cả các giao tiếp.
2.  **Cập nhật cấu hình `API_URL`:**
    *   Nếu `API_URL` là một biến môi trường hoặc được lấy từ file cấu hình, hãy kiểm tra và đảm bảo nó luôn bắt đầu bằng `https://` cho các môi trường ngoài local development.
    *   Trong môi trường local development, có thể có các lựa chọn:
        *   Tự cấu hình HTTPS cho server local (khuyến khích).
        *   Chấp nhận sử dụng HTTP cho API local, nhưng đảm bảo **không bao giờ** gửi dữ liệu nhạy cảm qua đó, hoặc chỉ sử dụng cho các endpoint không nhạy cảm.
3.  **Kiểm tra định nghĩa `API_URL`:** Tìm kiếm trong toàn bộ project để xác định nơi `API_URL` được định nghĩa và cách nó được cấu hình cho các môi trường khác nhau. Sử dụng các biến môi trường hoặc hệ thống quản lý cấu hình để đảm bảo URL được sử dụng là an toàn.

**Ví dụ minh họa cho việc sử dụng template string an toàn hơn:**

```javascript
// Giả định: API_URL_BASE được định nghĩa trong file cấu hình hoặc biến môi trường
// và có thể khác nhau giữa các môi trường
const API_URL_BASE = process.env.API_URL_BASE || "http://localhost:3000"; // Giá trị mặc định cho local dev
const API_ENDPOINT = "forgot-password";

// Luôn đảm bảo API_URL_BASE bắt đầu bằng https cho production/staging
const fullApiUrl = `${API_URL_BASE.endsWith('/') ? API_URL_BASE.slice(0, -1) : API_URL_BASE}/${API_ENDPOINT}`;

// ...
      const response = await fetch(fullApiUrl, {
// ...
```

### 5. Ghi chú cần tester kiểm tra thêm:

*   **Kiểm tra cấu hình `API_URL`:** Cần xác định chính xác `API_URL` được định nghĩa ở đâu trong ứng dụng và cách nó được cấu hình cho các **môi trường production, staging, và development**. Tester cần kiểm tra tất cả các nơi `API_URL` có thể được thiết lập.
*   **Môi trường deploy:** Xác nhận xem ứng dụng có được deploy trên các môi trường nào và `http` có thực sự được sử dụng cho các request bên ngoài môi trường local dev hay không.
*   **Dữ liệu nhạy cảm:** Mặc dù việc khôi phục mật khẩu thường liên quan đến email, cần xác nhận xem dữ liệu nào được gửi đi trong `body` của request này. Nếu có thêm các trường thông tin nhạy cảm khác, tác động sẽ cao hơn.
*   **Phạm vi của `localhost`:** Nếu `API_URL` chỉ trỏ đến `localhost` và server API của EShop cũng chạy trên `localhost` trong môi trường dev, thì rủi ro có thể thấp nếu đây là một lab riêng biệt. Tuy nhiên, nếu `localhost` có thể được proxy hoặc truy cập từ xa, rủi ro sẽ tăng lên.

---