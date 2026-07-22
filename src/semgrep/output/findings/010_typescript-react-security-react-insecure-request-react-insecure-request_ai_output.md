Tuyệt vời! Với vai trò là chuyên gia bảo mật ứng dụng, tôi sẽ tiến hành phân tích finding này theo yêu cầu của bạn.

---

## Phân tích Finding Bảo Mật SEMGREP-010

**1. Phân loại:** False Positive

**2. Lý do phân loại dựa trên source evidence:**

*   **Bằng chứng mã nguồn (Source Evidence):** Dòng mã `const response = await fetch(\`${API_URL}/apply-coupon\`, { ... });` cho thấy ứng dụng đang thực hiện một yêu cầu HTTP đến một URL được định nghĩa bởi biến `API_URL`.
*   **Ngữ cảnh môi trường (Deployment Context):** Thông tin cung cấp cho biết "EShop đang được quét như ứng dụng lab local; finding liên quan localhost cần kiểm tra môi trường trước khi kết luận rủi ro cuối." Điều này ngụ ý rằng `API_URL` *có thể* đang trỏ đến `http://localhost:PORT` hoặc một địa chỉ local tương tự.
*   **Phân tích:**
    *   Rule ID `typescript.react.security.react-insecure-request.react-insecure-request` và CWE-319 nhắm đến việc truyền tải thông tin nhạy cảm qua các kênh không mã hóa (HTTP).
    *   Tuy nhiên, việc sử dụng HTTP cho các yêu cầu đến `localhost` trong môi trường phát triển (dev/lab) là rất phổ biến và thường không mang rủi ro bảo mật nghiêm trọng *cho chính môi trường đó*. Các giao tiếp này thường chỉ diễn ra trong cùng một máy tính lập trình viên hoặc trong một mạng nội bộ được kiểm soát chặt chẽ, không phải là giao tiếp với người dùng cuối hoặc trên mạng công cộng.
    *   Semgrep phát hiện "Unencrypted request over HTTP detected", nhưng nó chưa đủ ngữ cảnh để xác định liệu `API_URL` có thực sự là một endpoint "nhạy cảm" trên môi trường *production* hay không. Nếu `API_URL` chỉ trỏ đến localhost của môi trường dev, thì việc truyền dữ liệu coupon code qua HTTP ở đây không phải là một lỗ hổng thực tế của ứng dụng khi deploy ra môi trường production.
    *   Chúng ta chưa có bằng chứng cho thấy `API_URL` sẽ trỏ đến một máy chủ ngoài (public) sử dụng HTTP mà lại gửi thông tin nhạy cảm.

**3. Tác động thực tế trong bối cảnh EShop:**

Trong bối cảnh "ứng dụng lab local", việc phát hiện này ít có tác động thực tế về mặt bảo mật. Nếu `API_URL` được cấu hình để trỏ đến `localhost` hoặc một địa chỉ IP nội bộ cho mục đích phát triển và kiểm thử, thì nguy cơ bị nghe lén (interception) bởi các bên không mong muốn là rất thấp. Rủi ro chỉ thực sự phát sinh nếu ứng dụng này được deploy lên môi trường production và `API_URL` lại trỏ đến một máy chủ thực tế qua HTTP để xử lý các yêu cầu coupon code.

**4. Cách khắc phục cụ thể:**

Để đảm bảo tính bảo mật cao nhất, ngay cả trong môi trường phát triển nếu có thể:

*   **Ưu tiên sử dụng HTTPS:** Ngay cả với `localhost`, việc cấu hình server local để sử dụng HTTPS (ví dụ: với các chứng chỉ tự ký) sẽ giúp mô phỏng tốt hơn môi trường production và loại bỏ hoàn toàn nguy cơ này.
*   **Kiểm tra biến môi trường/cấu hình:** Xác định cách biến `API_URL` được thiết lập. Nếu nó là một biến môi trường hoặc tệp cấu hình, đảm bảo rằng trong môi trường production, nó luôn trỏ đến một endpoint sử dụng HTTPS.
*   **Cập nhật Rule Detection (Nếu quan ngại):** Nếu có lo ngại rằng biến `API_URL` có thể bị cấu hình sai trong production và gây ra rủi ro, có thể xem xét việc cập nhật rule Semgrep để kiểm tra giá trị của `API_URL`, ví dụ như kiểm tra nó có bắt đầu bằng `http://` hay không. Tuy nhiên, việc này có thể dẫn đến nhiều False Positive hơn nếu `http://` được cho phép cho các endpoint không nhạy cảm.

**5. Ghi chú cần tester kiểm tra thêm nếu chưa đủ context:**

*   **Xác định giá trị thực tế của `API_URL`:** Yêu cầu tester kiểm tra giá trị của biến `API_URL` trong các cấu hình môi trường khác nhau (development, staging, production) để xác nhận liệu nó có bao giờ trỏ đến một máy chủ thực tế bằng giao thức HTTP hay không.
*   **Tính nhạy cảm của dữ liệu coupon code:** Tuy coupon code có thể không quá nhạy cảm, nhưng nếu nó liên quan đến các chương trình khuyến mãi lớn hoặc có thể bị lạm dụng, thì việc bảo vệ nó sẽ quan trọng hơn. Điều này cần được làm rõ bởi chủ sở hữu ứng dụng.
*   **Kiểm tra cách xử lý lỗi khi áp dụng coupon:** Mặc dù không trực tiếp liên quan đến finding này, nhưng nên kiểm tra xem lỗi mạng hoặc lỗi từ server có được xử lý tốt hay không để người dùng không bị lộ thông tin hoặc gặp trải nghiệm xấu.

---