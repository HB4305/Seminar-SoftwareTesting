Tuyệt vời! Với vai trò là chuyên gia bảo mật ứng dụng, tôi sẽ tiến hành triage finding SEMGREP-005 này dựa trên thông tin bạn cung cấp.

## Triage Finding SEMGREP-005

### 1. Phân loại: Needs Human Review

### 2. Lý do phân loại dựa trên source evidence.

Finding SEMGREP-005 chỉ ra rằng có một request được gửi đi qua giao thức HTTP (không mã hóa) tới endpoint `/login` trên `API_URL`. Dựa trên bằng chứng mã nguồn, dòng 189 trong file `eshop-sut/frontend-mobile/App.js` cho thấy việc sử dụng `fetch` để gửi thông tin đăng nhập (email, password) đến `API_URL`.

Tuy nhiên, việc phân loại mức độ rủi ro của việc sử dụng HTTP thay vì HTTPS phụ thuộc **hoàn toàn vào giá trị của biến `API_URL` và ngữ cảnh triển khai thực tế của ứng dụng EShop**.

*   Nếu `API_URL` trỏ đến một địa chỉ `localhost` hoặc một IP private trong môi trường phát triển/testing cục bộ, request này có thể không gây ra rủi ro bảo mật nghiêm trọng vì lưu lượng mạng được giới hạn trong một môi trường kiểm soát được.
*   Ngược lại, nếu `API_URL` trỏ đến một endpoint công cộng hoặc có thể truy cập được từ bên ngoài mạng nội bộ, việc gửi thông tin nhạy cảm (email và password) qua HTTP là **rất nguy hiểm**, tiềm ẩn nguy cơ bị kẻ tấn công nghe lén (man-in-the-middle attacks) và đánh cắp thông tin đăng nhập.

Semgrep, với vai trò là một công cụ SAST, chỉ có thể phân tích mã nguồn tĩnh và không có thông tin về môi trường runtime hoặc cấu hình mạng. Do đó, mặc dù phát hiện ra một hành vi có khả năng gây rủi ro, chúng ta cần thêm thông tin để xác định xem đây có phải là một lỗ hổng thực sự (True Positive) hay chỉ là một cảnh báo trong môi trường an toàn (False Positive).

### 3. Tác động thực tế trong bối cảnh EShop.

Trong bối cảnh EShop, việc dữ liệu đăng nhập bị lộ có thể dẫn đến các tác động nghiêm trọng:

*   **Chiếm đoạt tài khoản người dùng:** Kẻ tấn công có thể sử dụng thông tin đăng nhập bị đánh cắp để truy cập vào tài khoản của người dùng, từ đó thực hiện các hành vi độc hại như đặt hàng giả, thay đổi thông tin cá nhân, hoặc sử dụng thông tin thanh toán (nếu có).
*   **Mất lòng tin của người dùng:** Nếu ứng dụng bị phát hiện gửi dữ liệu nhạy cảm qua kênh không an toàn, người dùng sẽ mất lòng tin vào khả năng bảo mật của EShop, dẫn đến việc giảm tỷ lệ người dùng và ảnh hưởng tiêu cực đến danh tiếng của thương hiệu.
*   **Vi phạm quy định về bảo mật dữ liệu:** Tùy thuộc vào khu vực địa lý và loại dữ liệu được xử lý, việc truyền thông tin nhạy cảm qua kênh không mã hóa có thể vi phạm các quy định về bảo vệ dữ liệu (ví dụ: GDPR).

Tuy nhiên, **mức độ tác động thực tế là NGHI VẤN** và cần được làm rõ dựa trên giá trị `API_URL`.

### 4. Cách khắc phục cụ thể.

Cách khắc phục chính là đảm bảo tất cả các giao tiếp giữa client (ứng dụng EShop) và server API đều được mã hóa bằng HTTPS.

*   **Ưu tiên sử dụng HTTPS cho API_URL:** Cấu hình `API_URL` để trỏ đến một endpoint API sử dụng HTTPS. Nếu bạn đang phát triển trên môi trường local, hãy thiết lập một máy chủ API local có hỗ trợ HTTPS (ví dụ: sử dụng self-signed certificate cho mục đích phát triển).
*   **Cập nhật biến môi trường hoặc cấu hình:** Đảm bảo rằng biến `API_URL` luôn được thiết lập với scheme `https://`.
*   **Kiểm tra lại tất cả các request API khác:** Lỗ hổng này có thể không chỉ xuất hiện tại endpoint `/login` mà còn ở các endpoint khác mà ứng dụng EShop gọi tới. Cần rà soát lại toàn bộ các request API để đảm bảo tính nhất quán về bảo mật.

### 5. Ghi chú cần tester kiểm tra thêm nếu chưa đủ context.

Để có thể đưa ra kết luận cuối cùng (True Positive hay False Positive), **tester cần kiểm tra thêm các thông tin sau**:

*   **Giá trị thực tế của biến `API_URL`:** Đây là yếu tố quan trọng nhất. Tester cần xác định `API_URL` đang trỏ đến địa chỉ nào trong môi trường triển khai hiện tại.
    *   **Nếu là `http://localhost:xxxx` hoặc `http://127.0.0.1:xxxx`:** Cần xác nhận đây là môi trường phát triển/lab và không có người dùng thật nào bị ảnh hưởng. Tuy nhiên, vẫn khuyến khích sử dụng HTTPS ngay cả trong môi trường local để hình thành thói quen bảo mật tốt.
    *   **Nếu là một địa chỉ IP công cộng hoặc tên miền có thể truy cập từ Internet:** Vui lòng XÁC NHẬN NGAY LẬP TỨC rằng API đang sử dụng HTTPS. Nếu không, đây là **True Positive** với mức độ rủi ro cao.
*   **Ngữ cảnh triển khai:** Ứng dụng EShop này đang được triển khai ở đâu (môi trường dev, staging, production)? Ai là người dùng của ứng dụng này? Dữ liệu đăng nhập có chứa thông tin nhạy cảm đặc biệt không (ví dụ: thông tin y tế, tài chính)?
*   **Cấu hình SSL/TLS trên server API:** Nếu API đang chạy trên một server riêng, hãy kiểm tra xem server đó có cấu hình SSL/TLS đầy đủ và chính xác hay không.

Sau khi có thêm thông tin từ các điểm kiểm tra này, việc phân loại cuối cùng sẽ dễ dàng hơn.