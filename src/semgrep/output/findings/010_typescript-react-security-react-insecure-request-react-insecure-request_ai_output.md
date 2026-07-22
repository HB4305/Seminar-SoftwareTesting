Tuyệt vời, tôi sẵn sàng đóng vai trò chuyên gia bảo mật ứng dụng để phân tích finding này.

### Triage Finding Bảo Mật SEMGREP-010

1.  **Phân loại:** Needs Human Review

2.  **Lý do phân loại dựa trên source evidence:**
    Semgrep rule phát hiện việc sử dụng `fetch` để gọi đến một URL bắt đầu bằng `${API_URL}/apply-coupon` có khả năng là HTTP thay vì HTTPS. Việc này khớp với mô tả "Unencrypted request over HTTP detected" và CWE-319.

    Tuy nhiên, dòng mã nguồn cho thấy `API_URL` là một biến được sử dụng. Để xác định chính xác đây có phải là True Positive hay False Positive, chúng ta cần biết giá trị thực tế của `API_URL` trong các môi trường khác nhau, đặc biệt là môi trường production.
    *   Nếu `API_URL` được cấu hình trỏ đến `http://localhost:PORT` hoặc một địa chỉ IP/hostname sử dụng HTTP trong môi trường phát triển (dev) hoặc lab, thì đây có thể là một cảnh báo cho phép phát triển và không phải là rủi ro bảo mật nghiêm trọng nếu không có dữ liệu nhạy cảm nào được truyền đi.
    *   Tuy nhiên, nếu `API_URL` được cấu hình trỏ đến một endpoint API mà **không** sử dụng TLS/SSL (HTTPS) trong môi trường production, thì đây là một lỗ hổng nghiêm trọng dẫn đến việc lộ lọt thông tin nhạy cảm (như `user_id`, mã giảm giá, tổng giá trị đơn hàng).
    *   Ngữ cảnh "EShop đang được quét như ứng dụng lab local" càng củng cố thêm khả năng đây là một môi trường để thử nghiệm, nơi việc sử dụng HTTP localhost là phổ biến.

    Do đó, để đưa ra kết luận cuối cùng, cần xác minh cách biến `API_URL` được định nghĩa và sử dụng trong các file cấu hình của EShop cho các môi trường khác nhau.

3.  **Tác động thực tế trong bối cảnh EShop:**
    Nếu `API_URL` trỏ đến một dịch vụ API chỉ dùng HTTP và ứng dụng EShop đang được triển khai trong môi trường production (hoặc nơi mà dữ liệu người dùng thực có thể bị ảnh hưởng), tác động có thể là:
    *   **Lộ lọt dữ liệu nhạy cảm:** Mã giảm giá, tổng giá trị đơn hàng, và thậm chí `user_id` có thể bị kẻ tấn công nghe lén trên mạng.
    *   **Thao túng dữ liệu:** Kẻ tấn công có thể sửa đổi các yêu cầu gửi đi, ví dụ như thay đổi mã giảm giá để nhận ưu đãi không hợp lệ hoặc làm gián đoạn quy trình áp dụng mã.
    *   **Đánh cắp thông tin tài khoản:** Nếu thông tin đăng nhập hoặc token xác thực được truyền đi trong các request tương tự, chúng có thể bị đánh cắp.

    Tuy nhiên, dữ liệu được gửi trong request này (`code`, `total_amount`, `user_id`) ở mức độ nhạy cảm trung bình. `user_id` có thể không quá nhạy cảm nếu nó chỉ là một định danh nội bộ, nhưng việc lộ lọt mã giảm giá và tổng giá trị đơn hàng có thể hữu ích cho kẻ tấn công trong việc lập kế hoạch tấn công tiếp theo hoặc hiểu quy luật mua sắm của người dùng.

4.  **Cách khắc phục cụ thể:**
    *   **Ưu tiên sử dụng HTTPS:** Đảm bảo rằng tất cả các backend API mà ứng dụng EShop giao tiếp đều được triển khai và cấu hình để sử dụng kết nối mã hóa TLS/SSL (HTTPS).
    *   **Cấu hình biến môi trường:** Định nghĩa `API_URL` thông qua biến môi trường. Trong môi trường production, biến này **phải** trỏ đến endpoint API sử dụng HTTPS. Trong môi trường phát triển/lab, nếu cần sử dụng HTTP cho `localhost`, cần có chính sách rõ ràng về việc chỉ sử dụng cho mục đích thử nghiệm và đảm bảo không có dữ liệu nhạy cảm thực sự nào được gửi đi.
    *   **Kiểm tra giá trị `API_URL`:**
        *   Tìm kiếm định nghĩa của `API_URL` trong mã nguồn hoặc các file cấu hình (ví dụ: `.env`, `config.js`, v.v.).
        *   Xác minh xem trong môi trường production, `API_URL` có luôn bắt đầu bằng `https://` hay không.
    *   **Phát triển code an toàn hơn:** Trong trường hợp có khả năng API vẫn được gọi qua HTTP (ví dụ: trong các trường hợp `localhost` cho dev), cân nhắc việc lọc hoặc mã hóa các trường dữ liệu nhạy cảm trước khi gửi đi nếu không thể đảm bảo HTTPS cho mọi endpoint. Tuy nhiên, giải pháp tốt nhất vẫn là **buộc sử dụng HTTPS**.

5.  **Ghi chú cần tester kiểm tra thêm:**
    *   **Xác định rõ mục đích sử dụng của `API_URL`:** Tester cần tìm file cấu hình hoặc định nghĩa của `API_URL` để xác định URL nó trỏ tới trong các môi trường khác nhau (development, staging, production).
    *   **Kiểm tra dữ liệu gửi đi:** Liệu `user_id` có thực sự là định danh nhạy cảm của người dùng hay chỉ là ID tạm thời? Liệu mã giảm giá có thể bị lợi dụng theo cách nào khác ngoài việc áp dụng?
    *   **Kiểm tra quy trình deploy:** Quy trình deploy của ứng dụng có cho phép người dùng cấu hình `API_URL` một cách linh hoạt theo môi trường không? Có cơ chế validation nào cho URL được cấu hình không?
    *   **Môi trường Lab:** Nếu đây là ứng dụng lab *chỉ* chạy với `localhost` và không bao giờ được deploy với dữ liệu thực, thì finding này có thể được đánh dấu là *giáo dục/cảnh báo lý thuyết* thay vì một lỗ hổng thực tế. Tuy nhiên, việc lặp lại thói quen này có thể dẫn đến sai lầm khi phát triển các ứng dụng khác nghiêm túc hơn.