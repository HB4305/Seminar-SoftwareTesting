Tuyệt vời! Hãy cùng nhau tiến hành phân tích và triage finding SEMGREP-012 này.

## Phân tích Finding Bảo Mật SEMGREP-012

### 1. Phân loại:
Needs Human Review

### 2. Lý do phân loại dựa trên source evidence:

Dựa trên bằng chứng mã nguồn và ngữ cảnh được cung cấp, chúng ta thấy dòng 400 trong file `App.js` thực hiện một yêu cầu `fetch` đến một endpoint `/coupon-usage` tại `${API_URL}/coupon-usage`. Quan trọng là, chúng ta không có thông tin rõ ràng về cách biến `API_URL` được định nghĩa và sử dụng.

*   **Khả năng True Positive:** Nếu `API_URL` được định nghĩa để trỏ đến một máy chủ sử dụng giao thức HTTP không mã hóa (ví dụ: `http://localhost:3000`), và token được gửi đi chứa thông tin nhạy cảm, thì đây có thể là một lỗ hổng thực sự. `fetch` mặc định sẽ sử dụng giao thức được chỉ định trong URL.
*   **Khả năng False Positive:** Nếu `API_URL` được định nghĩa để luôn trỏ đến một máy chủ sử dụng giao thức HTTPS (ví dụ: `https://api.eshop.com`), hoặc nếu `API_URL` đang trỏ đến một môi trường development/lab chỉ sử dụng HTTP và được cho phép trong ngữ cảnh này, thì việc tìm thấy này có thể là một `False Positive`. Việc ứng dụng của bạn đang được quét như một ứng dụng lab local là một yếu tố quan trọng.
*   **Lý do "Needs Human Review":** Semgrep đã phát hiện một yêu cầu qua HTTP không mã hóa. Tuy nhiên, để kết luận chính xác, chúng ta cần xác định:
    *   **Giá trị thực tế của `API_URL` trong bối cảnh triển khai được quét:** Nó đang trỏ tới đâu? `http://` hay `https://`?
    *   **Tính nhạy cảm của dữ liệu trong `token`:** Token này có chứa thông tin cá nhân, thông tin xác thực nhạy cảm hay không?
    *   **Ngữ cảnh triển khai:** Đây là môi trường production, staging, hay chỉ là local development / lab? Nếu là lab local và không có dữ liệu nhạy cảm được truyền đi, thì rủi ro có thể thấp.

### 3. Tác động thực tế trong bối cảnh EShop:

Nếu `API_URL` trỏ đến một máy chủ sử dụng HTTP và thông tin trong `token` là nhạy cảm, việc truyền nó qua kết nối không mã hóa có thể dẫn đến:

*   **Rò rỉ thông tin nhạy cảm (Sensitive Data Exposure):** Kẻ tấn công có thể chặn gói tin trên mạng để đánh cắp `token`. Nếu `token` này có thể được sử dụng để giả mạo người dùng hoặc truy cập vào các tài nguyên nhạy cảm khác, thì tác động sẽ là **MEDIUM**.
*   **Tấn công chiếm đoạt tài khoản (Account Takeover):** Nếu `token` đó có thể được tái sử dụng để xác thực, kẻ tấn công có thể sử dụng nó để đăng nhập vào tài khoản của người dùng hợp pháp.

Tuy nhiên, do `Likelihood` là `LOW` và `Impact` là `MEDIUM`, và ngữ cảnh đang là ứng dụng lab local, tác động thực tế có thể bị giảm thiểu nếu đây chỉ là môi trường thử nghiệm hoặc URL được cấu hình an toàn trong các môi trường khác.

### 4. Cách khắc phục cụ thể:

1.  **Ưu tiên sử dụng HTTPS:** Đảm bảo rằng `API_URL` luôn được cấu hình để sử dụng giao thức HTTPS cho tất cả các môi trường, đặc biệt là production. Nếu `API_URL` của bạn là một biến môi trường (environment variable), hãy đảm bảo nó được thiết lập đúng với `https://`.
2.  **Kiểm tra định nghĩa `API_URL`:** Xem lại cách biến `API_URL` được định nghĩa trong mã nguồn hoặc thông qua cấu hình ứng dụng. Nếu nó đang trỏ đến `http://localhost` hoặc một địa chỉ IP không có SSL/TLS, hãy cập nhật nó.
3.  **Xem xét mã token:** Xác minh xem `token` được truyền trong header `Authorization` có chứa thông tin nhạy cảm có thể bị lạm dụng hay không. Nếu có, việc sử dụng HTTPS là bắt buộc.

### 5. Ghi chú cần tester kiểm tra thêm nếu chưa đủ context:

*   **Kiểm tra giá trị `API_URL`:** Tester cần kiểm tra giá trị thực tế của biến `API_URL` trong các cấu hình/môi trường khác nhau (local, staging, production) mà ứng dụng được triển khai.
*   **Xác định tính nhạy cảm của `token`:** Cần hiểu rõ `token` này là loại token gì (ví dụ: JWT, refresh token, session token) và nó được sử dụng để làm gì. Nếu nó là một token truy cập có thể dùng để thực hiện các hành động nhạy cảm, thì lỗ hổng này cần được xem xét nghiêm túc.
*   **Vai trò của `coupon-usage` endpoint:** Endpoint này xử lý thông tin gì? Nó có liên quan đến dữ liệu người dùng nhạy cảm không?
*   **Môi trường `localhost`:** Nếu `localhost` chỉ được sử dụng cho mục đích phát triển và không có dữ liệu nhạy cảm được truyền đi, thì việc tìm thấy này có thể được coi là một cảnh báo thông tin thay vì một lỗ hổng bảo mật nghiêm trọng cho môi trường đó. Tuy nhiên, cần đảm bảo quy tắc này không bị bỏ qua cho các môi trường production.