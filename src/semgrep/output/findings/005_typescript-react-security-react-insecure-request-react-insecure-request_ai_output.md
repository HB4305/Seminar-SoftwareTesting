Tuyệt vời! Hãy cùng tôi phân tích finding bảo mật này.

## Phân Tích Finding Bảo Mật SEMGREP-005

### 1. Phân loại:
`Needs Human Review`

### 2. Lý do phân loại dựa trên source evidence:
Semgrep rule `typescript.react.security.react-insecure-request.react-insecure-request` phát hiện một yêu cầu mạng được thực hiện qua giao thức HTTP thay vì HTTPS, cụ thể tại dòng 189 của file `eshop-sut/frontend-mobile/App.js`. Yêu cầu này đang gửi thông tin đăng nhập (email và password) tới endpoint `/login` của API.

Tuy nhiên, bằng chứng mã nguồn cho thấy biến `API_URL` được sử dụng để xây dựng URL cho request. Giá trị của `API_URL` không được hiển thị trong đoạn mã cung cấp. Trong bối cảnh "ứng dụng lab local" và việc tìm kiếm liên quan đến `localhost`, có khả năng `API_URL` được cấu hình chỉ để trỏ đến môi trường phát triển cục bộ, nơi mà việc sử dụng HTTP là phổ biến và chấp nhận được để giảm thiểu sự phức tạp trong quá trình phát triển.

Nếu `API_URL` chỉ đơn thuần là `http://localhost:PORT` hoặc `http://127.0.0.1:PORT`, và API server cũng đang chạy trên cùng môi trường này, thì việc truyền dữ liệu nhạy cảm qua HTTP trong môi trường lab cục bộ này có thể không gây ra rủi ro bảo mật đáng kể ngay lập tức, vì lưu lượng mạng không đi qua mạng công cộng.

Tuy nhiên, nếu `API_URL` có thể được cấu hình để trỏ đến một máy chủ API khác (thậm chí là trong mạng nội bộ nhưng có thể bị giám sát) hoặc nếu ứng dụng này có thể được triển khai trong một môi trường mà `API_URL` trỏ đến một máy chủ công cộng hoặc không đáng tin cậy, thì đây sẽ là một lỗ hổng bảo mật nghiêm trọng.

Do đó, việc xác định liệu `API_URL` có được cấu hình cho môi trường production hay không, và liệu server API có sử dụng HTTPS hay không, là rất quan trọng để đưa ra quyết định cuối cùng.

### 3. Tác động thực tế trong bối cảnh EShop:
Nếu `API_URL` trỏ đến một endpoint không bảo mật qua HTTPS, thì thông tin đăng nhập của người dùng (email và password) sẽ được truyền dưới dạng văn bản thuần túy qua mạng. Điều này có thể dẫn đến:

*   **Nghe lén dữ liệu nhạy cảm:** Kẻ tấn công có thể chặn và đọc trộm thông tin đăng nhập, cho phép họ truy cập trái phép vào tài khoản của người dùng.
*   **Xác thực yếu:** Nếu thông tin đăng nhập bị lộ, kẻ tấn công có thể sử dụng chúng để thực hiện các hành vi gian lận hoặc chiếm đoạt tài khoản.
*   **Lỗ hổng liên quan đến OWASP:** Điều này trực tiếp vi phạm OWASP A03:2017 (Sensitive Data Exposure) và A02:2021 (Cryptographic Failures), cũng như A04:2025 (Cryptographic Failures).

Tuy nhiên, như đã đề cập, nếu đây chỉ là môi trường lab sử dụng `localhost`, tác động này bị giảm nhẹ đáng kể.

### 4. Cách khắc phục cụ thể:
*   **Ưu tiên cấu hình API_URL sử dụng HTTPS:** Đảm bảo rằng tất cả các yêu cầu tới server API đều được thực hiện qua giao thức HTTPS. Điều này bao gồm việc cấu hình server API để sử dụng chứng chỉ SSL/TLS.
*   **Cập nhật biến API\_URL:** Nếu biến `API_URL` có thể được cấu hình, hãy đảm bảo rằng nó luôn trỏ đến một endpoint sử dụng HTTPS. Ví dụ, thay vì `http://api.example.com`, sử dụng `https://api.example.com`.
*   **Kiểm tra môi trường deploy:** Đối với các môi trường production, staging, và các môi trường không phải là lab local, **bắt buộc** phải sử dụng HTTPS.
*   **Sử dụng các thư viện HTTP an toàn:** Nếu có thể, hãy cân nhắc sử dụng các thư viện hoặc module trong React Native (hoặc framework khác) chuyên để quản lý các yêu cầu mạng, có thể có các cơ chế cấu hình an toàn mặc định hoặc dễ dàng hơn.

### 5. Ghi chú cần tester kiểm tra thêm nếu chưa đủ context:
*   **Xác định giá trị thực tế của `API_URL`:** Tester cần tìm hiểu xem biến `API_URL` được khởi tạo như thế nào và giá trị của nó là gì trong các ngữ cảnh triển khai khác nhau (dev, staging, production).
*   **Kiểm tra server API:** Xác nhận xem server API mà `eshop-sut` kết nối tới có hỗ trợ và được cấu hình để sử dụng HTTPS hay không. Nếu chỉ có HTTP, thì cần khắc phục ở phía server API trước.
*   **Chính sách bảo mật của tổ chức:** Tìm hiểu xem có các yêu cầu bảo mật cụ thể nào đối với việc truyền dữ liệu nhạy cảm trong môi trường của EShop không.

Việc phân loại `Needs Human Review` là phù hợp nhất cho đến khi các thông tin trên được làm rõ. Nếu sau khi kiểm tra, `API_URL` luôn trỏ đến `localhost` và không có ý định deploy ra môi trường bên ngoài, có thể phân loại lại thành `False Positive`. Ngược lại, nếu `API_URL` có thể trỏ đến các endpoint không bảo mật, nó sẽ là `True Positive`.