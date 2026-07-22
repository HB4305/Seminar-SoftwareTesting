Tuyệt vời! Hãy cùng tôi phân tích finding SEMGREP-012 này. Dựa trên thông tin được cung cấp, đây là kết quả triage của tôi dưới vai trò chuyên gia bảo mật ứng dụng:

---

### Triage Finding Bảo Mật

**Mã finding:** SEMGREP-012
**Rule ID:** `typescript.react.security.react-insecure-request.react-insecure-request`
**File nguồn:** `eshop-sut\frontend-mobile\App.js`
**Dòng:** 400
**Severity:** ERROR
**CWE:** CWE-319: Cleartext Transmission of Sensitive Information
**OWASP:** A03:2017 - Sensitive Data Exposure, A02:2021 - Cryptographic Failures, A04:2025 - Cryptographic Failures
**Likelihood:** LOW
**Impact:** MEDIUM
**Confidence:** MEDIUM
**Cảnh báo Semgrep:** Unencrypted request over HTTP detected.

---

1.  **Phân loại:** Needs Human Review

2.  **Lý do phân loại dựa trên source evidence:**
    Semgrep rule phát hiện một yêu cầu mạng được gửi qua giao thức HTTP (không mã hóa) tại dòng 400. Cụ thể, dòng này thực hiện một lệnh gọi `fetch` đến `${API_URL}/coupon-usage`. Dù rule này nhạy cảm với việc sử dụng HTTP, ngữ cảnh của `API_URL` lại là yếu tố quyết định chính cho việc phân loại.

    *   Nếu `${API_URL}` được cấu hình trỏ đến một máy chủ `localhost` hoặc một địa chỉ IP nội bộ chỉ được truy cập trong môi trường phát triển hoặc lab **local**, thì việc sử dụng HTTP ở đây có thể không gây ra rủi ro bảo mật đáng kể cho người dùng cuối.
    *   Tuy nhiên, nếu `${API_URL}` trỏ đến một địa chỉ công cộng hoặc một máy chủ sản xuất được truy cập qua Internet, việc gửi yêu cầu mà không có mã hóa TLS/SSL (HTTPS) sẽ làm lộ thông tin nhạy cảm được truyền trong body (trong trường hợp này là `coupon_id`) và cả headers (như `Authorization` token), dẫn đến lỗ hổng Creative Failures và Sensitive Data Exposure.

    Do đó, chỉ dựa vào mã nguồn tĩnh mà không rõ cách `API_URL` được định nghĩa và triển khai trong môi trường thực tế (dev/staging/prod), chúng ta không thể kết luận đây là True Positive hay False Positive.

3.  **Tác động thực tế trong bối cảnh EShop:**
    Nếu `API_URL` trỏ đến một môi trường không bảo mật (non-production):
    *   **Rủi ro lộ thông tin nhạy cảm:** Dữ liệu nhạy cảm như `coupon_id` và token xác thực (`Authorization: Bearer ${token}`) có thể bị chặn bởi bất kỳ ai trong đường truyền mạng (ví dụ: attacker trên cùng mạng Wi-Fi công cộng).
    *   **Tiềm năng tấn công tiếp theo:** Dữ liệu bị lộ có thể cho phép kẻ tấn công giả mạo người dùng, thực hiện các hành động không mong muốn hoặc khai thác các lỗ hổng khác.

    Tuy nhiên, nếu đây là môi trường lab và `API_URL` được cấu hình trỏ đến `http://localhost:port_number`, rủi ro cho người dùng cuối là rất thấp.

4.  **Cách khắc phục cụ thể:**
    Để khắc phục triệt để và đảm bảo an toàn, dù là môi trường nào, nên ưu tiên áp dụng các biện pháp sau:

    *   **Sử dụng HTTPS cho tất cả các dịch vụ API:**
        *   **Cấu hình Server:** Đảm bảo các API backend đang chạy trên kết nối HTTPS và được cấu hình với chứng chỉ SSL/TLS hợp lệ.
        *   **Cấu hình Client (Frontend):** Cập nhật biến môi trường `API_URL` để luôn trỏ đến phiên bản `https` của API. Ví dụ:
            ```javascript
            // Ví dụ: Thay thế bằng cấu hình phù hợp cho từng môi trường
            const API_URL = process.env.NODE_ENV === 'production'
                ? 'https://api.your-eshop.com'
                : 'http://localhost:5000'; // Hoặc https://localhost:5001 nếu backend chạy https trên local
            ```
        *   **Kiểm tra lại Rule Semgrep:** Sau khi triển khai HTTPS, Semgrep rule này sẽ không còn cảnh báo hoặc cảnh báo sai nếu được cấu hình để chỉ soi xét các URL không phải `https`.

    *   **Cân nhắc về độ nhạy cảm của dữ liệu:**
        *   Nếu `coupon_id` không thực sự nhạy cảm, việc truyền qua HTTP trên mạng nội bộ có thể chấp nhận được trong môi trường lab. Tuy nhiên, việc phát hiện sớm là quan trọng để tránh việc vô tình đặt `API_URL` sai trong môi trường production.

5.  **Ghi chú cần tester kiểm tra thêm nếu chưa đủ context:**
    *   **Kiểm tra định nghĩa và giá trị của `API_URL`:** Tester cần xác định `API_URL` đang trỏ đến địa chỉ nào trong môi trường đang được quét. Cụ thể, nó có phải là `http://localhost:port` hay một URL công cộng?
    *   **Xác định môi trường triển khai:** Đây là môi trường phát triển (dev), kiểm thử (staging) hay sản xuất (production)? Điều này ảnh hưởng trực tiếp đến mức độ rủi ro.
    *   **Kiểm tra cấu hình HTTPS trên Backend:** Nếu `API_URL` là một URL công cộng, cần xác minh rằng backend API tương ứng đã được cấu hình sử dụng HTTPS.
    *   **Xác nhận tính nhạy cảm của dữ liệu:** `coupon_id` và `Authorization` token có được coi là nhạy cảm trong bối cảnh này hay không?

---