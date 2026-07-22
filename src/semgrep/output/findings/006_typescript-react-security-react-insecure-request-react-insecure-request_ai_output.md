Tuyệt vời! Với vai trò là chuyên gia bảo mật ứng dụng, đây là kết quả triage cho finding SEMGREP-006:

---

## Triage Finding Bảo mật - SEMGREP-006

**1. Phân loại:** Needs Human Review

**2. Lý do phân loại dựa trên source evidence:**

*   **Rule ID:** `typescript.react.security.react-insecure-request.react-insecure-request`
*   **Mô tả Semgrep:** Phát hiện yêu cầu không mã hóa qua HTTP.
*   **Source evidence:** Dòng 222 trong file `eshop-sut\frontend-mobile\App.js` có đoạn mã:
    ```typescript
    const response = await fetch(`${API_URL}/register`, { ... });
    ```
    Trong đó, `API_URL` có thể là một biến môi trường hoặc được định nghĩa ở đâu đó trong dự án. Việc sử dụng `fetch` để thực hiện request tới `${API_URL}/register` mà không có bằng chứng rõ ràng về việc sử dụng HTTPS là điểm Semgrep cảnh báo.
*   **Ngữ cảnh:** Semgrep đang phân tích mã nguồn của ứng dụng EShop, được mô tả là "ứng dụng lab local". Môi trường "lab local" thường có thể sử dụng HTTP cho các API nội bộ hoặc khi kết nối với localhost để phát triển. Tuy nhiên, vấn đề bảo mật ở đây là việc truyền dữ liệu nhạy cảm (mật khẩu) qua một kênh không mã hóa.
*   **Lý do cho "Needs Human Review":** Mặc dù Semgrep cảnh báo về request không mã hóa, chúng ta cần làm rõ:
    *   **Giá trị thực tế của `API_URL`:** Biến `API_URL` được định nghĩa ở đâu? Nếu `API_URL` luôn trỏ tới một endpoint `http://localhost:<port>` hoặc một địa chỉ IP nội bộ *chỉ dùng trong mạng local* và *không bao giờ tiếp cận qua internet công cộng*, thì rủi ro thực tế có thể thấp hơn. Tuy nhiên, nếu `API_URL` có thể cấu hình để trỏ tới một server công cộng qua HTTP, đây là một lỗ hổng nghiêm trọng.
    *   **Môi trường triển khai:** Ứng dụng này chỉ dùng cho mục đích demo lab hay có khả năng được triển khai ra môi trường production? Nếu triển khai production, việc sử dụng HTTP là không thể chấp nhận cho bất kỳ request nào gửi dữ liệu nhạy cảm.
    *   **Dữ liệu nhạy cảm:** Việc đăng ký tài khoản liên quan đến email và mật khẩu, đây rõ ràng là thông tin nhạy cảm.

**3. Tác động thực tế trong bối cảnh EShop:**

Nếu `API_URL` trỏ tới một endpoint đang chạy trên giao thức HTTP và có thể truy cập được qua mạng (kể cả mạng nội bộ nếu không được bảo mật đúng cách), kẻ tấn công có thể nghe lén (sniffing) luồng dữ liệu truyền đi và đánh cắp thông tin đăng ký, bao gồm tên, email và mật khẩu người dùng. Điều này dẫn đến nguy cơ:

*   **Chiếm đoạt tài khoản:** Kẻ tấn công có thể sử dụng thông tin đăng ký để truy cập vào tài khoản người dùng, lấy cắp thông tin cá nhân, đơn hàng, hoặc thực hiện các hành vi gian lận.
*   **Phơi nhiễm thông tin nhạy cảm:** Dữ liệu cá nhân của người dùng bị lộ.
*   **Tấn công liên hoàn:** Thông tin đăng nhập bị lộ có thể được sử dụng để tấn công các dịch vụ khác mà người dùng sử dụng chung mật khẩu.

Tác động này được đánh giá là **MEDIUM** vì nó liên quan trực tiếp đến việc bảo vệ thông tin người dùng, mặc dù `Likelihood` (Khả năng xảy ra) có thể thấp nếu môi trường triển khai được kiểm soát chặt chẽ.

**4. Cách khắc phục cụ thể:**

*   **Ưu tiên hàng đầu:** Bắt buộc sử dụng HTTPS cho tất cả các giao tiếp từ frontend đến backend.
    *   **Backend:** Đảm bảo API của EShop được triển khai với chứng chỉ SSL/TLS hợp lệ và lắng nghe trên cổng HTTPS.
    *   **Frontend (`API_URL`):** Cập nhật cấu hình `API_URL` để luôn bắt đầu bằng `https://` thay vì `http://`. Nếu `API_URL` là biến môi trường, hãy đảm bảo nó được đặt đúng cách trong môi trường triển khai.
*   **Kiểm soát `API_URL`:** Nếu bắt buộc phải có fallback về HTTP cho môi trường dev cục bộ (ví dụ: `http://localhost:3000`), cần có cơ chế để đảm bảo rằng phiên bản sản xuất (production) **luôn luôn** sử dụng HTTPS. Điều này có thể được quản lý thông qua biến môi trường khác nhau cho các môi trường (dev, staging, prod).
*   **Cập nhật Dependency (nếu có):** Trong một số trường hợp, thư viện network có thể có các cấu hình mặc định không an toàn. Tuy nhiên, với `fetch` API gốc, vấn đề nằm ở URL được gọi.

**5. Ghi chú cần tester kiểm tra thêm nếu chưa đủ context:**

*   **Xác định giá trị và nguồn gốc của biến `API_URL`:** Tester cần tìm kiếm cách `API_URL` được định nghĩa và sử dụng trong toàn bộ dự án. Kiểm tra xem có các backend server khác nhau cho các môi trường khác nhau hay không và cấu hình `API_URL` cho môi trường production là gì.
*   **Kiểm tra cấu hình server backend:** Xác nhận rằng API endpoint mà `API_URL` trỏ tới đã được cấu hình để sử dụng HTTPS và có chứng chỉ SSL/TLS hợp lệ.
*   **Môi trường triển khai:** Làm rõ mục đích sử dụng của mã nguồn này. Nếu đây chỉ là mã test hoặc môi trường lab, cần đánh giá lại mức độ ưu tiên xử lý, nhưng vẫn nên cảnh báo về best practice. Nếu có khả năng được triển khai ra môi trường có người dùng thật, việc khắc phục là **khẩn cấp**.

---