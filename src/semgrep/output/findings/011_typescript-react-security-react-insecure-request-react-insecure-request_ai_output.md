Tuyệt vời! Với vị thế chuyên gia bảo mật ứng dụng, tôi sẽ tiến hành triage finding SEMGREP-011 một cách chi tiết.

---

## Triage Finding Bảo Mật: SEMGREP-011

### 1. Phân loại:
Needs Human Review

### 2. Lý do phân loại dựa trên source evidence:

Bằng chứng mã nguồn tại dòng 384 cho thấy một lệnh gọi `fetch` tới `${API_URL}/checkout`. Cảnh báo của Semgrep chỉ ra rằng đây là một "Unencrypted request over HTTP detected". Tuy nhiên, việc phân loại thành True Positive hay False Positive phụ thuộc vào giá trị của biến `API_URL` và cách ứng dụng này được triển khai trong môi trường production thực tế.

*   **Nếu `API_URL` trỏ tới một địa chỉ `http://localhost:PORT` hoặc một địa chỉ IP nội bộ dùng cho mục đích phát triển/lab:** Thì đây có khả năng là **False Positive** vì lưu lượng mạng nội bộ hoặc trong môi trường lab thường không cần thiết phải mã hóa. Mặc dù về mặt kỹ thuật là HTTP, nhưng rủi ro lộ lọt dữ liệu trên mạng cục bộ bị giới hạn.
*   **Nếu `API_URL` trỏ tới một tên miền hoặc IP có thể truy cập từ bên ngoài và sử dụng giao thức `http:` thay vì `https:`:** Thì đây là một **True Positive** nghiêm trọng. Việc truyền dữ liệu nhạy cảm qua HTTP là vi phạm bảo mật nghiêm trọng, có thể dẫn đến lộ lọt thông tin.
*   **Ngữ cảnh triển khai chưa rõ ràng:** Với thông tin hiện tại, chúng ta không biết `API_URL` được cấu hình như thế nào ở môi trường production hoặc môi trường mà `eshop-sut/frontend-mobile/App.js` sẽ chạy. Thông tin này rất quan trọng để đánh giá mức độ rủi ro thực tế.

### 3. Tác động thực tế trong bối cảnh EShop:

Nếu `API_URL` thực sự sử dụng HTTP cho một endpoint liên quan đến xử lý thanh toán (`/checkout`), tác động có thể rất nghiêm trọng:

*   **Lộ lọt thông tin nhạy cảm:** Dữ liệu như chi tiết đơn hàng, số tiền thanh toán, thông tin nhận hàng, và có thể cả các token xác thực (`Authorization: Bearer ${token}`) có thể bị kẻ tấn công trên cùng mạng chặn bắt.
*   **Tấn công Man-in-the-Middle (MITM):** Kẻ tấn công có thể sửa đổi dữ liệu truyền đi, ví dụ như thay đổi số tiền thanh toán, gây thiệt hại tài chính cho cả người dùng và doanh nghiệp.
*   **Vi phạm tuân thủ:** Các quy định về bảo mật dữ liệu (như GDPR, PCI DSS nếu liên quan đến thanh toán thẻ) có thể bị vi phạm nếu thông tin nhạy cảm không được bảo vệ.

Tuy nhiên, tác động thực tế sẽ bị giảm thiểu đáng kể nếu như endpoint này chỉ được gọi trên môi trường local development hoặc lab testing.

### 4. Cách khắc phục cụ thể:

1.  **Kiểm tra cấu hình `API_URL`:**
    *   Xác định giá trị thực tế của biến `API_URL` trong các môi trường khác nhau (development, staging, production).
    *   Đảm bảo rằng tất cả các endpoint được gọi từ frontend mobile đều sử dụng giao thức `https:` và trỏ tới một máy chủ đã được cấu hình SSL/TLS hợp lệ.
2.  **Cập nhật mã nguồn (nếu cần):**
    *   Nếu `API_URL` vẫn đang sử dụng `http:`, hãy sửa đổi nó để sử dụng `https:` và cấu hình chứng chỉ SSL/TLS cho backend API.
    *   Ví dụ (chỉ mang tính minh họa, cần điều chỉnh theo cách quản lý biến môi trường của dự án):
        ```javascript
        // Giả định API_URL được quản lý qua environment variables
        // Backend API nên expose qua HTTPS
        // const API_URL = process.env.REACT_APP_API_URL; 
        // Nếu API_URL vẫn là http://..., cần kiểm tra backend config
        const API_URL = "https://your-api-domain.com"; // Ví dụ của HTTPS
        
        const handleConfirmCheckout = async () => {
          setCheckoutLoading(true);
          try {
            const finalAmount = couponResult ? couponResult.final_amount : cartTotal;
            // Đảm bảo API_URL đã là https
            const response = await fetch(`${API_URL}/checkout`, { 
              method: "POST",
              headers: {
                "Content-Type": "application/json",
                ...(token ? { Authorization: `Bearer ${token}` } : {}),
              },
            });
            // ... xử lý response
          } catch (error) {
            // ... xử lý lỗi
          } finally {
            setCheckoutLoading(false);
          }
        };
        ```
3.  **Thực thi chính sách cho phép giao thức:** Kể từ React Native 0.60, sử dụng `android:usesCleartextTraffic="false"` trong `AndroidManifest.xml` cho Android để ngăn chặn các yêu cầu HTTP không mã hóa. Tương tự, cần kiểm tra cấu hình cho iOS.

### 5. Ghi chú cần tester kiểm tra thêm nếu chưa đủ context:

*   **Cấu hình `API_URL`:** Cần kiểm tra cách biến `API_URL` được định nghĩa và quản lý trong các môi trường khác nhau (local development, staging, production). Liệu có sử dụng file `.env` hay cấu hình build nào khác không?
*   **Môi trường triển khai:** Xác nhận xem ứng dụng này có được triển khai ở môi trường production hay chỉ đang chạy trong lab/development. Nếu là lab, cần có sự xác nhận từ người quản lý hạ tầng hoặc devops về việc liệu `http://localhost` có được xem là rủi ro chấp nhận được trong môi trường đó hay không.
*   **Độ nhạy cảm của dữ liệu:** Dữ liệu được gửi trong request `POST` đến `/checkout` có chứa các thông tin cực kỳ nhạy cảm (ví dụ: chi tiết thẻ tín dụng trực tiếp) hay không? Dù cách nào cũng không nên truyền qua HTTP, nhưng mức độ nhạy cảm sẽ ảnh hưởng đến mức độ ưu tiên vá lỗi.
*   **Cơ chế CORS/Network Security Configurations:** Kiểm tra các cấu hình bảo mật mạng ở phía client (Android/iOS) có thể ảnh hưởng đến việc cho phép hoặc chặn các kết nối HTTP.