Tuyệt vời! Với vai trò là chuyên gia bảo mật ứng dụng, tôi sẽ tiến hành triage finding này dựa trên thông tin bạn cung cấp.

```markdown
## Triage Finding Bảo Mật: SEMGREP-004

**1. Phân loại:** Needs Human Review

**2. Lý do phân loại dựa trên source evidence:**

Finding này chỉ ra **Unencrypted request over HTTP detected** tại dòng 174 trong file `App.js`, gửi request tới `${API_URL}/orders/my-orders`. Rule Semgrep và CWE đều liên quan đến việc truyền dữ liệu nhạy cảm qua kênh không mã hóa. Mã nguồn cho thấy việc sử dụng `fetch` API để gửi request đến `API_URL` với header `Authorization` chứa token.

Tuy nhiên, việc phân loại **False Positive** hay **True Positive** còn phụ thuộc nhiều vào ngữ cảnh triển khai và giá trị của `API_URL`.
*   Nếu `API_URL` trỏ đến một localhost hoặc một URL được cấu hình để chỉ sử dụng trong môi trường phát triển (dev/lab), nơi mà mạng nội bộ được kiểm soát và không có nguy cơ bị nghe lén, thì đây có thể được xem là **False Positive** đối với môi trường production.
*   Ngược lại, nếu `API_URL` có thể trỏ đến một endpoint của production hoặc staging mà vẫn sử dụng HTTP thay vì HTTPS, và dữ liệu nhạy cảm (như `currentToken` và thông tin đơn hàng) được truyền đi, thì đây sẽ là một **True Positive**.

Chúng ta chưa có đủ thông tin về cách `API_URL` được định nghĩa và cấu hình trong các môi trường khác nhau của EShop.

**3. Tác động thực tế trong bối cảnh EShop:**

Nếu `API_URL` thực sự đang gọi qua HTTP và truyền tải dữ liệu nhạy cảm, tác động có thể bao gồm:
*   **Lộ thông tin nhạy cảm:** Token xác thực (`currentToken`) và chi tiết đơn hàng có thể bị kẻ tấn công trong cùng một mạng (ví dụ: mạng Wi-Fi công cộng) đọc trộm.
*   **Giả mạo danh tính:** Kẻ tấn công có thể sử dụng token bị lộ để thực hiện các hành vi trái phép nhân danh người dùng.
*   **Can thiệp dữ liệu:** Dữ liệu truyền đi có thể bị thay đổi trên đường truyền (man-in-the-middle attack).

Tuy nhiên, do EShop được quét như ứng dụng lab local, nếu `API_URL` chỉ định có thể dẫn đến localhost hoặc URL dev, rủi ro cho môi trường production thực tế có thể thấp hoặc không tồn tại.

**4. Cách khắc phục cụ thể:**

*   **Ưu tiên sử dụng HTTPS:** Đảm bảo tất cả các endpoint API mà ứng dụng tương tác đều được truy cập thông qua HTTPS.
    *   **Cấu hình server:** Đảm bảo server backend của EShop được cấu hình để phục vụ API qua HTTPS.
    *   **Cấu hình client (ứng dụng mobile):** Mặc dù Semgrep đang báo cáo về phía client, nguyên nhân gốc rễ có thể nằm ở server. Tuy nhiên, trong trường hợp frontend mobile chủ động gửi request qua HTTP, cần kiểm tra lại cách `API_URL` được định nghĩa.
*   **Kiểm tra cấu hình `API_URL`:** Xác định giá trị của `API_URL` trong các môi trường khác nhau (dev, staging, production).
    *   Nếu ứng dụng mobile được phép sử dụng HTTP cho localhost, đây có thể là hành vi mong muốn cho môi trường dev, nhưng *cần đảm bảo rằng nó không bao giờ được sử dụng cho production*.
    *   Nếu `API_URL` được định nghĩa động dựa trên biến môi trường hoặc cấu hình, cần kiểm tra xem liệu có khả năng nó được trỏ đến một endpoint không an toàn trong production hay không.
*   **Strict Transport Security (HSTS) (nếu áp dụng cho web):** Mặc dù đây là ứng dụng mobile, nếu có liên quan đến tương tác web view, HSTS là một biện pháp giúp trình duyệt chỉ cho phép kết nối HTTPS.

**5. Ghi chú cần tester kiểm tra thêm nếu chưa đủ context:**

*   **Giá trị thực tế của `API_URL`:** Tester cần kiểm tra giá trị của biến `API_URL` trong code hoặc thông qua quá trình build/deploy các môi trường khác nhau của EShop.
*   **Môi trường triển khai:** Xác nhận EShop đang chạy trong môi trường lab local như mô tả hay có khả năng là môi trường staging/production được sử dụng để thử nghiệm.
*   **Cấu hình mạng:** Nếu EShop đang chạy trên môi trường mạng bị kiểm soát (isolated network) như trong lab, thì rủi ro nghe lén là rất thấp.
*   **Sensitive Data:** Kiểm tra xem token `currentToken` và thông tin trả về từ `my-orders` có thực sự chứa dữ liệu cực kỳ nhạy cảm cần bảo vệ tối đa hay không.
```