Tuyệt vời! Với vai trò là chuyên gia bảo mật ứng dụng, tôi sẽ tiến hành triage finding SEMGREP-011 này một cách cẩn trọng.

## Triage Finding SEMGREP-011

### 1. Phân loại

```
Needs Human Review
```

### 2. Lý do phân loại dựa trên source evidence.

Dựa trên bằng chứng mã nguồn và ngữ cảnh được cung cấp, việc phân loại ban đầu là "Needs Human Review" xuất phát từ các lý do sau:

*   **API_URL là biến môi trường:** Dòng code `fetch(${API_URL}/checkout, ...)` sử dụng biến `API_URL`. Semgrep SAST chỉ phân tích tĩnh mã nguồn và không thể xác định giá trị thực tế của `API_URL` lúc runtime. Nếu `API_URL` được cấu hình là một endpoint sử dụng HTTP (không mã hóa) và có thể truy cập từ bên ngoài môi trường tin cậy (ví dụ: production), thì đây có thể là một lỗ hổng thực sự. Ngược lại, nếu `API_URL` luôn trỏ đến `localhost` hoặc một endpoint nội bộ được phục vụ qua HTTPS, thì rủi ro sẽ giảm đáng kể.
*   **Ngữ cảnh EShop là ứng dụng lab local:** Thông tin này rất quan trọng. Việc Semgrep phát hiện request qua HTTP tới `localhost` có thể chỉ phản ánh môi trường phát triển hoặc lab, nơi mà bảo mật hạ tầng (như SSL/TLS) có thể chưa được áp dụng đầy đủ hoặc không cần thiết trong môi trường kiểm thử nội bộ. Tuy nhiên, điều này cần được xác nhận.

Semgrep đã chính xác phát hiện hành vi sử dụng giao thức HTTP cho một request, và quy tắc này được thiết kế để cảnh báo về việc truyền dữ liệu nhạy cảm qua kênh không mã hóa. Tuy nhiên, mức độ rủi ro thực tế phụ thuộc hoàn toàn vào cách `API_URL` được định cấu hình và loại mạng mà ứng dụng EShop đang hoạt động.

### 3. Tác động thực tế trong bối cảnh EShop.

Nếu `API_URL` trỏ đến một endpoint HTTP bên ngoài mạng nội bộ tin cậy, và dữ liệu truyền đi (`finalAmount`, `token`) là nhạy cảm, thì tác động có thể bao gồm:

*   **Nghe lén thông tin nhạy cảm:** Kẻ tấn công có thể chặn và đọc các thông tin như:
    *   Tổng số tiền cuối cùng (`finalAmount`) có thể tiết lộ thông tin về giá trị đơn hàng, hành vi mua sắm của người dùng.
    *   Token xác thực (`token` trong header `Authorization`) nếu bị lộ có thể cho phép kẻ tấn công mạo danh người dùng, thực hiện các hành động trái phép thay mặt người dùng, hoặc truy cập vào các tài nguyên nhạy cảm khác.
*   **Tấn công Man-in-the-Middle (MiTM):** Kẻ tấn công có thể sửa đổi dữ liệu truyền đi, ví dụ: thay đổi `finalAmount` để gây gian lận.
*   **Lộ lọt dữ liệu theo OWASP A03:2017 và A02:2021:** Việc truyền thông tin nhạy cảm qua kênh không mã hóa trực tiếp vi phạm các nguyên tắc về bảo mật dữ liệu nhạy cảm và mã hóa.

Tuy nhiên, nếu EShop chỉ chạy trong môi trường lab local và `API_URL` luôn là `localhost`, tác động thực tế có thể rất thấp hoặc bằng không, miễn là không có ai khác truy cập vào mạng local đó một cách trái phép và có ý đồ xấu.

### 4. Cách khắc phục cụ thể.

Cách khắc phục được đề xuất chủ yếu tập trung vào việc đảm bảo tất cả các giao tiếp mạng đều được mã hóa, đặc biệt là khi truyền dữ liệu nhạy cảm.

*   **Sử dụng HTTPS cho API_URL:**
    *   **Cấu hình mã hóa ở Backend:** Đảm bảo rằng API backend tại `${API_URL}/checkout` được triển khai với HTTPS và chứng chỉ SSL/TLS hợp lệ.
    *   **Cấu hình biến môi trường:** Trong môi trường production, biến môi trường `API_URL` **phải** được thiết lập để trỏ đến một endpoint sử dụng HTTPS. Ví dụ: `https://api.eshop.com/`.
*   **Kiểm tra kỹ cấu hình biến môi trường:**
    *   **Trong môi trường Production:** Xác nhận rằng `API_URL` được thiết lập thành một endpoint HTTPS.
    *   **Trong môi trường Dev/Lab:** Nếu việc sử dụng HTTP là cần thiết cho mục đích phát triển/lab và bạn có thể đảm bảo rằng môi trường này được cách ly và không có nguy cơ bị tấn công từ bên ngoài, thì cần có ghi chú rõ ràng cho việc này. Tuy nhiên, nên hướng tới việc sử dụng HTTPS ngay cả trong môi trường lab để giảm thiểu thói quen sử dụng kênh không mã hóa.
*   **Xử lý lỗi kết nối HTTPS:** Đảm bảo ứng dụng có cơ chế xử lý lỗi khi không thể kết nối qua HTTPS.

### 5. Ghi chú cần tester kiểm tra thêm nếu chưa đủ context.

Để có thể đưa ra kết luận phân loại cuối cùng (True Positive hay False Positive), các điểm sau cần được tester kiểm tra chi tiết:

*   **Giá trị thực tế của `API_URL` trong môi trường Production:** Tester cần xác định giá trị cụ thể mà biến môi trường `API_URL` nhận được khi triển khai ứng dụng EShop ở môi trường Production.
*   **Cấu hình SSL/TLS cho Endpoint Backend:** Kiểm tra xem endpoint API backend mà `API_URL` trỏ tới có đang sử dụng HTTPS hay không. Nếu có, chứng chỉ có hợp lệ và được tin cậy không?
*   **Ngữ cảnh mạng của EShop:** EShop đang chạy trong môi trường mạng nào? Nó có được triển khai trong một mạng nội bộ (VLAN) được kiểm soát an ninh, hay nó có khả năng bị truy cập từ Internet công cộng? Nếu là môi trường production, việc sử dụng HTTP cho bất kỳ request nào (ngay cả `localhost`) cần được xem xét kỹ lưỡng hơn, vì các công cụ hoặc dịch vụ khác có thể can thiệp.
*   **Tính nhạy cảm của dữ liệu truyền đi:** Mặc dù `finalAmount` và `token` có vẻ nhạy cảm, tester nên xác nhận xem có bất kỳ dữ liệu nhạy cảm khác nào khác được gửi trong request `POST /checkout` hoặc ngầm hiểu qua ngữ cảnh của `cartTotal` và `couponResult` hay không.

Sau khi có những thông tin này, chúng ta sẽ có đủ cơ sở để xác định đây là True Positive (lỗ hổng thực sự cần khắc phục) hay False Positive (không phải là rủi ro trong ngữ cảnh triển khai).