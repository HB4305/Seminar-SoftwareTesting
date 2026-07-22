Tuyệt vời! Với vai trò là chuyên gia bảo mật ứng dụng, tôi sẽ thực hiện phân tích kỹ lưỡng finding SEMGREP-008 này.

## Triage Finding Bảo Mật: SEMGREP-008

### 1. Phân loại
**Needs Human Review**

### 2. Lý do phân loại dựa trên source evidence
Dựa trên bằng chứng mã nguồn được cung cấp, Semgrep đã phát hiện ra một yêu cầu HTTP được thực hiện thông qua `fetch` tới endpoint `${API_URL}/reset-password` tại dòng 272 của file `App.js`. Rule ID `typescript.react.security.react-insecure-request.react-insecure-request` và mô tả "Unencrypted request over HTTP detected" chỉ ra rằng yêu cầu này có khả năng được gửi qua giao thức HTTP không mã hóa, vi phạm nguyên tắc về bảo vệ dữ liệu nhạy cảm (CWE-319, OWASP A03:2017, A02:2021, A04:2025).

Tuy nhiên, để đưa ra phân loại cuối cùng, chúng ta cần xem xét thêm một số yếu tố:

*   **Ngữ cảnh của `API_URL`:** Giá trị của biến `API_URL` không được cung cấp trong bằng chứng mã nguồn. Nếu `API_URL` trỏ đến `http://localhost` hoặc một địa chỉ IP nội bộ trong môi trường phát triển/lab, thì yêu cầu này có thể không mang rủi ro đáng kể *cho mục đích thử nghiệm ban đầu*. Tuy nhiên, trong môi trường production, nếu `API_URL` được cấu hình là một server chạy HTTP thay vì HTTPS, đó sẽ là một lỗ hổng nghiêm trọng.
*   **Môi trường triển khai:** Như đã đề cập trong ngữ cảnh cho triage tĩnh, "EShop đang được quét như ứng dụng lab local; finding liên quan localhost cần kiểm tra môi trường trước khi kết luận rủi ro cuối." Điều này cho thấy cần xác định liệu `API_URL` có được cấu hình để sử dụng HTTPS trên production hay không.
*   **Độ nhạy cảm của dữ liệu:** Mặc dù việc gửi thông tin reset mật khẩu qua kênh không mã hóa là nhạy cảm, nhưng mức độ rủi ro còn phụ thuộc vào việc dữ liệu này có bị chặn lại bởi bên thứ ba hay không, và mức độ bảo mật tổng thể của hệ thống.

Do đó, trong khi mã nguồn rõ ràng cho thấy một yêu cầu có khả năng không mã hóa, ngữ cảnh triển khai và cấu hình của `API_URL` là yếu tố quyết định để phân loại đây là True Positive hay False Positive.

### 3. Tác động thực tế trong bối cảnh EShop
Nếu `API_URL` được cấu hình sử dụng HTTP trong môi trường production, tác động thực tế có thể bao gồm:

*   **Lộ thông tin nhạy cảm:** Token reset mật khẩu và mật khẩu mới khi được gửi đi có thể bị kẻ tấn công nghe lén, dẫn đến việc chiếm quyền truy cập vào tài khoản người dùng.
*   **Tấn công "Man-in-the-Middle" (MitM):** Kẻ tấn công có thể chèn dữ liệu độc hại hoặc thay đổi thông tin yêu cầu, có khả năng gây ra các hành vi không mong muốn hoặc lợi dụng lỗ hổng.

Tuy nhiên, nếu `API_URL` chỉ dùng cho môi trường dev/lab và luôn được truy cập qua HTTPS trong production, thì rủi ro thực tế có thể thấp hoặc không tồn tại.

### 4. Cách khắc phục cụ thể
1.  **Ưu tiên sử dụng HTTPS:** Đảm bảo rằng tất cả các yêu cầu API, đặc biệt là những yêu cầu liên quan đến dữ liệu nhạy cảm như reset mật khẩu, luôn được thực hiện qua giao thức HTTPS thay vì HTTP.
2.  **Kiểm tra và cấu hình `API_URL`:**
    *   Nếu `API_URL` được định nghĩa trong một file cấu hình (ví dụ: `.env`, `config.js`), hãy kiểm tra xem nó có đang trỏ đến một endpoint HTTPS hay không.
    *   Trong môi trường production, cấu hình `API_URL` bắt buộc phải là một URL bắt đầu bằng `https://`.
3.  **Sử dụng thư viện HTTP an toàn:** Nếu đang sử dụng một thư viện HTTP tùy chỉnh hoặc cấu hình `fetch` một cách phức tạp, hãy đảm bảo nó tuân thủ các tiêu chuẩn an ninh mạng. Tuy nhiên, trong trường hợp này, vấn đề chính là giao thức, không phải bản thân thư viện `fetch`.
4.  **Cập nhật giá trị `API_URL`:**
    Chỉnh sửa biến `API_URL` để luôn sử dụng giao thức `https`. Ví dụ, nếu trước đây là `http://api.example.com`, thì đổi thành `https://api.example.com`.

### 5. Ghi chú cần tester kiểm tra thêm nếu chưa đủ context
Để hoàn tất việc phân loại và đánh giá đúng rủi ro, vui lòng kiểm tra và cung cấp thêm thông tin về:

*   **Giá trị thực tế của `API_URL`:** Cần xác định giá trị của biến `API_URL` trong các môi trường khác nhau (development, staging, production).
*   **Cơ chế cấu hình biến môi trường:** Nếu `API_URL` được quản lý bằng biến môi trường, hãy kiểm tra cách biến này được thiết lập và áp dụng trên các môi trường triển khai.
*   **Môi trường triển khai:** Xác nhận rằng các API server mà ứng dụng mobile kết nối tới luôn được cấu hình để sử dụng HTTPS, đặc biệt là trong môi trường production.

Sau khi có được những thông tin này, chúng ta có thể đưa ra quyết định cuối cùng là True Positive (nếu rủi ro tồn tại trong production) hoặc False Positive (nếu môi trường dev/lab và production đều được bảo vệ đúng cách).