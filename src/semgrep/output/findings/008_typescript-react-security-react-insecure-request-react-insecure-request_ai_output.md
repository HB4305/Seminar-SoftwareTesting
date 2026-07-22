Tuyệt vời, tôi sẽ đóng vai trò là chuyên gia bảo mật ứng dụng để triage finding này từ Semgrep.

---

## Triage Finding Bảo Mật SEMGREP-008

### 1. Phân loại: **Needs Human Review**

### 2. Lý do phân loại dựa trên source evidence:

Finding SEMGREP-008 chỉ ra rằng có một yêu cầu mạng không được mã hóa (HTTP) được thực hiện đến API endpoint `/reset-password` từ file `App.js` dòng 272. Rule `react-insecure-request` của Semgrep đã phát hiện việc sử dụng `fetch` với một URL được xây dựng từ biến `API_URL`.

Tuy nhiên, ngữ cảnh `API_URL` không rõ ràng trong đoạn mã cung cấp. Nếu `API_URL` được cấu hình là `localhost` hoặc một địa chỉ IP nội bộ cho môi trường phát triển/dev, thì yêu cầu này có thể không phải là một lỗ hổng bảo mật trong môi trường production (nếu production sử dụng HTTPS). Bản thân việc sử dụng HTTP đến `localhost` khi phát triển là khá phổ biến và thường không tiềm ẩn rủi ro ngay lập tức nếu không có dữ liệu nhạy cảm được truyền đi và môi trường đó được kiểm soát.

Rule Semgrep Cảnh báo: "Unencrypted request over HTTP detected."

CWE-319: Cleartext Transmission of Sensitive Information và OWASP A03:2017/A02:2021/A04:2025 đều nhấn mạnh rủi ro khi truyền thông tin nhạy cảm qua kênh không được mã hóa. Dữ liệu nhạy cảm được truyền trong yêu cầu này bao gồm `email`, `resetToken`, và `newPassword`, những thông tin này chắc chắn cần được bảo vệ.

Vì vậy, mặc dù code rõ ràng thực hiện một yêu cầu HTTP, nhưng **rủi ro thực tế phụ thuộc hoàn toàn vào cách `API_URL` được cấu hình và sử dụng trong các môi trường khác nhau (development, staging, production).**

### 3. Tác động thực tế trong bối cảnh EShop:

**Nếu `API_URL` trỏ đến một địa chỉ không phải localhost hoặc IP nội bộ, và sử dụng HTTP thay vì HTTPS:**

*   **Lộ thông tin nhạy cảm:** Kẻ tấn công có thể nghe lén lưu lượng mạng và đánh cắp thông tin đăng nhập người dùng (email, token reset mật khẩu, mật khẩu mới), dẫn đến việc tài khoản bị chiếm đoạt. Điều này trực tiếp vi phạm CWE-319 và các khuyến cáo của OWASP.
*   **Tấn công Man-in-the-Middle (MITM):** Kẻ tấn công có thể thay đổi dữ liệu truyền đi, chẳng hạn như thay đổi mật khẩu mới của người dùng bằng một mật khẩu do kẻ tấn công kiểm soát, hoặc chèn mã độc vào phản hồi từ server.

**Nếu `API_URL` trỏ đến `localhost` hoặc IP nội bộ và chỉ sử dụng trong môi trường dev/lab:**

*   Trong môi trường này, rủi ro về việc bị nghe lén từ mạng bên ngoài là rất thấp. Tuy nhiên, vẫn tồn tại rủi ro nếu môi trường phát triển bị xâm nhập hoặc có các tiến trình độc hại khác trên máy đó.
*   Việc truyền mật khẩu qua HTTP ngay cả trên localhost cũng là một thực hành tồi, vì vậy việc khắc phục vẫn cần thiết để đảm bảo code có thể tái sử dụng an toàn trong các ngữ cảnh khác.

### 4. Cách khắc phục cụ thể:

Ưu tiên hàng đầu là đảm bảo tất cả các yêu cầu đến API đều sử dụng **HTTPS**.

1.  **Cấu hình môi trường:**
    *   Xác định cách `API_URL` được định nghĩa và cung cấp cho ứng dụng mobile.
    *   Trong môi trường **production**, đảm bảo rằng `API_URL` luôn trỏ đến một endpoint sử dụng **HTTPS**.
    *   Nếu API server không hỗ trợ HTTPS, cần triển khai chứng chỉ SSL/TLS cho API server ngay lập tức.

2.  **Sử dụng HTTPS:** Thay đổi cách gọi `fetch` để đảm bảo URL luôn bắt đầu bằng `https://` nếu kết nối với server production.
    ```javascript
    // Ví dụ: giả định API_URL được quản lý thông qua biến môi trường hoặc cấu hình
    // Nếu API_URL có thể là http hoặc https, cần logic kiểm tra.
    
    // Cách tiếp cận an toàn hơn: Luôn dùng HTTPS cho production
    // Có thể xem xét cấu hình API_URL như sau:
    // const API_URL = process.env.NODE_ENV === 'production' ? 'https://api.your-eshop.com' : 'http://localhost:3000';
    
    // Trong trường hợp này, gọi fetch sẽ là:
    const apiUrlWithHttps = API_URL.startsWith('http://') && process.env.NODE_ENV === 'production' 
        ? API_URL.replace('http://', 'https://') 
        : API_URL;
        
    const response = await fetch(`${apiUrlWithHttps}/reset-password`, { // Sử dụng API_URL đã được đảm bảo là HTTPS
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: forgotEmail, resetToken, newPassword }),
    });
    ```
    Hoặc cách đơn giản hơn là định nghĩa `API_URL` cho production luôn là URL HTTPS.

3.  **An toàn cho cả môi trường Localhost (nếu có yêu cầu):**
    *   Nếu sau này bạn có ý định chạy API của EShop trên HTTPS cho môi trường localhost (ví dụ: sử dụng `localhost:3000` với HTTPS), bạn cần cấu hình chứng chỉ cho server này. Tuy nhiên, việc này thường phức tạp hơn cho môi trường local và có thể không cần thiết nếu chỉ là dev thông thường. **Ưu tiên là cho production.**

### 5. Ghi chú cần tester kiểm tra thêm nếu chưa đủ context:

*   **Xác định giá trị của biến `API_URL`:** Tester cần kiểm tra giá trị thực tế của `API_URL` trong các môi trường khác nhau (development, staging, production). Đặc biệt quan trọng là nó được định nghĩa ở đâu và như thế nào.
*   **Cấu hình chứng chỉ SSL/TLS cho API Server:** Tester cần xác nhận xem API Server mà ứng dụng mobile này kết nối đến có đang sử dụng HTTPS với chứng chỉ hợp lệ hay không.
*   **Quy trình deploy:** Tester cần hiểu cách ứng dụng mobile được build và deploy cho mỗi môi trường, và làm thế nào các biến môi trường hoặc cấu hình liên quan đến `API_URL` được áp dụng. Nếu ứng dụng được build sẵn với một `API_URL` cứng nhắc (ví dụ: `http://localhost:3000`), thì nó sẽ luôn gửi yêu cầu HTTP ngay cả khi deploy lên môi trường không mong muốn.

---