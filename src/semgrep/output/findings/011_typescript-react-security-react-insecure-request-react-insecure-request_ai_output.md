Dưới đây là kết quả triage cho finding bảo mật SEMGREP-011:

## Kết quả Triage Finding Bảo mật SEMGREP-011

### 1. Phân loại:

False Positive

### 2. Lý do phân loại dựa trên source evidence:

*   **Ngữ cảnh mã nguồn:** Dòng 384 (`fetch(\`${API_URL}/checkout\`, ...`) sử dụng biến `API_URL`. Trong ngữ cảnh ứng dụng lab local mà Semgrep đang quét, `API_URL` có khả năng cao được cấu hình để trỏ đến `http://localhost:<port>` hoặc một địa chỉ IP cục bộ tương tự, phục vụ cho môi trường phát triển (dev/lab).
*   **Bản chất của `fetch`:** Semgrep rule phát hiện việc sử dụng `fetch` mà không có chỉ dẫn về HTTPS, cảnh báo về "Unencrypted request over HTTP detected". Tuy nhiên, việc sử dụng HTTP cho các yêu cầu đến `localhost` trong môi trường lab không trực tiếp gây ra rủi ro cho dữ liệu nhạy cảm của người dùng cuối.
*   **Thiếu bằng chứng về việc lộ lọt dữ liệu nhạy cảm:** Dữ liệu được gửi trong "/checkout" bao gồm `items`, `total_amount`, `coupon_id`. Mặc dù `token` (trong header `Authorization`) là dữ liệu nhạy cảm, việc gửi token đến `localhost` trong môi trường lab không giống với việc lộ lọt nó ra mạng công cộng.

### 3. Tác động thực tế trong bối cảnh EShop:

Trong nhiều trường hợp, `API_URL` được cấu hình động dựa trên môi trường deploy. Nếu `API_URL` *chỉ* được sử dụng với các dịch vụ chạy trên máy local hoặc trong một mạng nội bộ an toàn (môi trường dev/lab), thì việc này không tạo ra rủi ro đáng kể.

Tuy nhiên, nếu `API_URL` có thể được cấu hình để trỏ tới một máy chủ bên ngoài và kết nối không sử dụng TLS/SSL (HTTPS), thì đây sẽ là một lỗ hổng nghiêm trọng (True Positive). Nhưng dựa trên thông tin hiện tại (ứng dụng lab local, ghi chú về việc kiểm tra môi trường), chúng ta giả định trường hợp an toàn hơn.

### 4. Cách khắc phục cụ thể:

*   **Đối với môi trường Production:** Luôn đảm bảo rằng `API_URL` được cấu hình để sử dụng HTTPS khi kết nối tới backend. Điều này có thể liên quan đến việc chỉnh sửa file cấu hình (ví dụ: `.env`, file cấu hình ứng dụng) để biến `API_URL` luôn bắt đầu bằng `https://`.
*   **Đối với môi trường Dev/Lab:** Nếu đây là ứng dụng lab, việc sử dụng `http://localhost` là chấp nhận được cho mục đích demo. Tuy nhiên, nếu có thể, nên cấu hình backend để chạy với HTTPS ngay cả trên local để phản ánh quy trình production.

### 5. Ghi chú cần tester kiểm tra thêm:

Để **chắc chắn** đây là False Positive, tester cần kiểm tra giá trị thực tế của biến `API_URL` trong các cấu hình môi trường khác nhau, đặc biệt là cấu hình production.

*   **Kiểm tra cấu hình API URL:** Xác định file hoặc cách thức mà biến `API_URL` được định nghĩa và giá trị của nó trong môi trường production.
*   **Kiểm tra trạng thái của Backend:**backend mà `/checkout` gọi tới có được cấu hình để chấp nhận kết nối HTTPS không, và liệu nó có được truy cập qua HTTPS hay không trong production.
*   **Kiểm tra các dữ liệu nhạy cảm khác:** Hãy kiểm tra xem còn có những API call nào khác sử dụng HTTP cho các endpoint quan trọng hoặc gửi dữ liệu nhạy cảm không.

Nếu `API_URL` *luôn* trỏ đến một endpoint HTTPS trong môi trường production, thì việc Semgrep cảnh báo là do nó không phân tích được biến `API_URL` để biết rằng nó sẽ được dùng với HTTPS. Rule này có thể cần tinh chỉnh hoặc cần bổ sung logic sau khi khai báo (ví dụ: kiểm tra `API_URL.startsWith('https')`).