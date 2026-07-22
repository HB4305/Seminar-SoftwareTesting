Tuyệt vời, tôi sẽ đóng vai trò chuyên gia bảo mật ứng dụng để triage finding này cho bạn.

---

## Triage Finding Bảo Mật: SEMGREP-010

### 1. Phân loại: Needs Human Review

### 2. Lý do phân loại dựa trên source evidence:

*   **Bằng chứng Source Code:** Semgrep phát hiện một yêu cầu `fetch` được thực hiện đến `${API_URL}/apply-coupon` sử dụng phương thức `POST` với `Content-Type: application/json`. Rule `react-insecure-request` trong Semgrep được thiết kế để cảnh báo khi có các yêu cầu truyền dữ liệu nhạy cảm qua HTTP không mã hóa.
*   **Ngữ cảnh `API_URL`:** Biến `API_URL` không được hiển thị trong đoạn trích mã nguồn. Đây là yếu tố then chốt để xác định xem yêu cầu có thực sự đang được gửi qua HTTP hay không. Nếu `API_URL` được cấu hình là `http://localhost:<port>` hoặc `http://127.0.0.1:<port>` trong môi trường phát triển (dev/lab), thì yêu cầu này có thể không gây ra rủi ro bảo mật thực sự cho người dùng cuối, vì nó chỉ tương tác với server cục bộ. Tuy nhiên, nếu `API_URL` được cấu hình là một tên miền hoặc địa chỉ IP không sử dụng HTTPS, hoặc nếu cấu hình này có thể thay đổi trong môi trường production, thì đây là một lỗ hổng nghiêm trọng.
*   **Độ nhạy cảm Dữ liệu:** Dữ liệu được gửi đi bao gồm `couponCode` (mã giảm giá) và `cartTotal` (tổng giỏ hàng). Mặc dù không phải là thông tin nhạy cảm cực kỳ cao như mật khẩu hay thông tin thẻ tín dụng, nhưng việc lộ mã giảm giá và tổng giá trị đơn hàng cũng có thể gây ra một số rủi ro phụ như:
    *   Kẻ tấn công có thể lợi dụng để tìm hiểu các mã giảm giá hiện có hoặc đang hoạt động.
    *   Trong một số kịch bản phức tạp hơn, thông tin này có thể là một phần của chuỗi tấn công để hiểu hành vi người dùng hoặc cấu trúc giao dịch.
*   **Context Deploy:** Việc EShop đang được quét như ứng dụng lab local là một điểm quan trọng. Tuy nhiên, Semgrep là SAST, nó phân tích mã tĩnh. Kết luận về rủi ro thực tế phụ thuộc rất nhiều vào cách `API_URL` được định cấu hình và triển khai trong các môi trường khác nhau (dev, staging, production).

Do thiếu thông tin về cấu hình thực tế của `API_URL` và môi trường triển khai, chúng ta không thể kết luận ngay đây là True Positive hay False Positive.

### 3. Tác động thực tế trong bối cảnh EShop:

*   **Nếu `API_URL` trỏ đến `http://localhost`:** Tác động bảo mật trong môi trường lab local là rất thấp hoặc không có, vì lưu lượng truy cập chỉ diễn ra giữa ứng dụng frontend trên thiết bị và server API chạy trên máy tính của nhà phát triển. Tuy nhiên, nếu cấu hình này vô tình được giữ nguyên hoặc lặp lại trong môi trường production mà không sử dụng HTTPS, thì tác động sẽ **trung bình (MEDIUM)**.
*   **Nếu `API_URL` trỏ đến một endpoint không sử dụng HTTPS (không phải localhost):** Tác động sẽ là **trung bình (MEDIUM)**. Kẻ tấn công có thể nghe lén (eavesdrop) trên mạng để đọc được mã giảm giá và tổng giỏ hàng khi chúng được gửi đi. Điều này có thể tạo điều kiện cho các hoạt động gian lận liên quan đến khuyến mãi hoặc cung cấp thông tin cho các cuộc tấn công nhắm mục tiêu sâu hơn.
*   **Rủi ro cho dữ liệu nhạy cảm:** Theo CWE-319 và OWASP A03:2017/A02:2021, việc truyền dữ liệu nhạy cảm qua kênh không mã hóa là một lỗ hổng chính. Mặc dù `couponCode` và `cartTotal` có thể không được coi là "nhạy cảm tối đa", chúng vẫn là thông tin có thể bị khai thác.

### 4. Cách khắc phục cụ thể:

1.  **Xác định và kiểm tra cấu hình `API_URL`:**
    *   Tìm kiếm biến `API_URL` trong toàn bộ mã nguồn dự án, bao gồm cả các file cấu hình môi trường (ví dụ: `.env`, `config.js`, v.v.).
    *   Xác minh xem `API_URL` có đang sử dụng giao thức `https` hay không.

2.  **Ưu tiên sử dụng HTTPS:**
    *   Nếu `API_URL` được cấu hình cho môi trường production, hãy đảm bảo nó luôn được đặt thành một URL sử dụng `https`.
    *   Nếu `API_URL` có thể là `http://localhost` cho môi trường dev, xem xét việc:
        *   Đảm bảo server API local cũng chạy qua HTTPS (sử dụng certificate tự ký cho môi trường dev).
        *   Hoặc, nếu chỉ cho mục đích test thuần túy, hãy chấp nhận rủi ro thấp này nhưng **tuyệt đối không được để nó tồn tại trong môi trường staging hoặc production**.

3.  **Cập nhật Rule (nếu cần):**
    *   Trong trường hợp `API_URL` trỏ đến `http://localhost` và được coi là an toàn trong ngữ cảnh dev, bạn có thể cần điều chỉnh các rule Semgrep hoặc thêm logic để loại trừ các yêu cầu tới `localhost` hoặc `127.0.0.1` khỏi việc cảnh báo cho rule này, tùy thuộc vào chính sách bảo mật của bạn. Tuy nhiên, hãy cân nhắc kỹ lưỡng để tránh che giấu các lỗ hổng thực sự.

4.  **Sử dụng Content Security Policy (CSP) và các biện pháp bảo mật mạng khác:**
    *   Tuy không trực tiếp khắc phục cách thức truyền dữ liệu, việc áp dụng CSP có thể giúp hạn chế các truy cập không mong muốn đến các endpoint API, giảm thiểu nguy cơ bị tấn công Man-in-the-Middle (MITM) nếu có khai thác nào khác.

### 5. Ghi chú cần tester kiểm tra thêm nếu chưa đủ context:

*   **Yêu cầu Tester/DevOps:** Cần làm rõ cách thức triển khai biến `API_URL` cho từng môi trường (Development, Staging, Production).
*   **Kiểm tra Trực quan:** Nếu có thể, tiến hành kiểm tra trực quan bằng cách thử nghiệm chức năng áp dụng mã giảm giá trong ứng dụng và sử dụng công cụ network inspector (trên trình duyệt nếu là web app hoặc các công cụ proxy như Charles Proxy, mitmproxy cho mobile app) để xem request thực tế được gửi đi có sử dụng HTTPS hay không.
*   **Đánh giá Độ nhạy cảm Dữ liệu:** Cần có một đánh giá chính thức về mức độ nhạy cảm của thông tin `couponCode` và `cartTotal` trong bối cảnh kinh doanh cụ thể của EShop để có thể ưu tiên xử lý. Tuy nhiên, theo nguyên tắc phòng ngừa, việc truyền bất kỳ dữ liệu nào có thể nhận dạng người dùng hoặc giao dịch qua kênh không mã hóa đều là điều nên tránh.