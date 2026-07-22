Tuyệt vời! Hãy cùng tôi tiến hành triage finding SEMGREP-012 này.

---

### Triage Finding: SEMGREP-012

**1. Phân loại:** Needs Human Review

**2. Lý do phân loại dựa trên source evidence:**

Dựa trên bằng chứng mã nguồn được cung cấp, Semgrep đã phát hiện một yêu cầu `fetch` được thực hiện thông qua HTTP (không có HTTPS) đến một endpoint `/coupon-usage` với `API_URL` không rõ ràng, nhưng dòng 400 chỉ ra rằng nó có thể là một endpoint API của ứng dụng. Rule Semgrep cảnh báo về việc "Unencrypted request over HTTP detected", phù hợp với CWE-319.

Tuy nhiên, việc phân loại đây là `True Positive` hay `False Positive` phụ thuộc vào ngữ cảnh triển khai và cách biến `API_URL` được định nghĩa và sử dụng:

*   **Ngữ cảnh `localhost` và `lab local`:** Thông tin cho biết "EShop đang được quét như ứng dụng lab local; finding liên quan localhost cần kiểm tra môi trường trước khi kết luận rủi ro cuối." và "HTTP localhost có thể chỉ dùng cho dev/lab; chỉ phân loại False Positive khi source/config chứng minh production không bị ảnh hưởng." Điều này rất quan trọng. Nếu `API_URL` chỉ trỏ đến `localhost` hoặc một môi trường phát triển/thử nghiệm nội bộ mà không truyền dữ liệu nhạy cảm, hoặc dữ liệu đó đã được bảo vệ bằng các biện pháp khác tại cấp độ mạng nội bộ, thì rủi ro có thể không cao như mô tả.
*   **Độ nhạy cảm của dữ liệu:** Yêu cầu này gửi kèm theo `token` trong header `Authorization`. Token này, nếu là token xác thực người dùng, có thể được coi là dữ liệu nhạy cảm. Việc truyền token này qua HTTP không mã hóa có thể khiến nó bị lộ cho kẻ tấn công trong cùng mạng.
*   **Khả năng `API_URL` là HTTPS:** Chúng ta không có định nghĩa của `API_URL` trong đoạn mã cung cấp. Nếu `API_URL` được định nghĩa và luôn sử dụng `https://` trong môi trường production, thì đây sẽ là `False Positive` ở môi trường đó. Tuy nhiên, nếu nó có thể bao gồm `http://` trong môi trường production hoặc các môi trường khác, thì rủi ro là có thật.

Do sự không chắc chắn về cách `API_URL` được cấu hình và môi trường triển khai thực tế (sử dụng `http` hay `https`), việc phân loại là `Needs Human Review` là phù hợp nhất.

**3. Tác động thực tế trong bối cảnh EShop:**

Nếu `API_URL` trỏ đến một endpoint hợp lệ và được truy cập qua HTTP không mã hóa, tác động có thể là:

*   **Rò rỉ thông tin xác thực (Token):** Token được truyền trong header `Authorization` có thể bị nghe lén (man-in-the-middle attack) bởi bất kỳ ai có thể truy cập vào cùng mạng với thiết bị người dùng hoặc máy chủ API. Nếu token này là token xác thực người dùng, kẻ tấn công có thể sử dụng nó để mạo danh người dùng và thực hiện các hành động thay mặt họ, ví dụ như truy cập tài khoản, thực hiện giao dịch trái phép (nếu token cho phép).
*   **Rò rỉ dữ liệu thanh toán (Coupon):** Mặc dù không thấy thông tin thanh toán trực tiếp trong request này, nhưng nó liên quan đến việc sử dụng coupon. Nếu dữ liệu coupon hoặc thông tin liên quan đến giao dịch trong tương lai được truyền qua kênh không mã hóa này, chúng cũng có thể bị lộ.
*   **Rủi ro từ OWASP A03:2017 (Sensitive Data Exposure) và A02/A04:2021/2025 (Cryptographic Failures):** Mã này trực tiếp vi phạm nguyên tắc tránh lộ dữ liệu nhạy cảm và sử dụng mã hóa không đầy đủ.

Tuy nhiên, nếu đây chỉ là môi trường dev/lab với `localhost` và không có dữ liệu nhạy cảm thực, tác động thực tế có thể là **THẤP** hoặc **KHÔNG CÓ TÁC ĐỘNG** đến người dùng cuối của ứng dụng production.

**4. Cách khắc phục cụ thể:**

*   **Ưu tiên sử dụng HTTPS cho tất cả các request API:** Đây là cách khắc phục cơ bản và hiệu quả nhất. Đảm bảo rằng `API_URL` luôn được cấu hình để sử dụng giao thức `https://`.
    *   Kiểm tra định nghĩa và cách sử dụng của biến `API_URL`. Nếu biến này được lấy từ file cấu hình, biến môi trường, hoặc hardcode, hãy đảm bảo nó luôn bắt đầu bằng `https://`.
    *   Trong môi trường mobile, việc cấu hình cho phép các kết nối HTTPS là tiêu chuẩn và an toàn.
*   **Giới hạn scope của `API_URL`:** Nếu `API_URL` là biến môi trường, hãy đảm bảo nó chỉ được trỏ đến các endpoint an toàn trong môi trường production. Đối với môi trường local/dev, có thể sử dụng `http://localhost:PORT` nhưng cần hiểu rõ rủi ro và chỉ dùng cho mục đích phát triển.
*   **Kiểm tra các request khác:** Rà soát toàn bộ codebase để tìm kiếm các `fetch` hoặc các cuộc gọi mạng tương tự khác có khả năng sử dụng HTTP không mã hóa, đặc biệt là những request gửi kèm dữ liệu nhạy cảm (token, thông tin người dùng, thông tin thanh toán).

**5. Ghi chú cần tester kiểm tra thêm nếu chưa đủ context:**

Để có thể phân loại cuối cùng và đánh giá đúng mức độ rủi ro, tester cần kiểm tra thêm các điểm sau:

*   **Định nghĩa và giá trị của `API_URL`:** Tester cần tìm định nghĩa của biến `API_URL` và xác định giá trị thực tế của nó trong các môi trường khác nhau (development, staging, production).
    *   Nếu `API_URL` là một biến môi trường, cần kiểm tra cách nó được thiết lập.
    *   Kiểm tra xem `API_URL` có thể bao gồm `http://` hay không trong bất kỳ môi trường nào.
*   **Ngữ cảnh sử dụng `API_URL`:** Biến `API_URL` này có thể được sử dụng cho mục đích gì? Nó trỏ đến server API nội bộ, server bên thứ ba hay chỉ là server local cho mục đích debug?
*   **Tính nhạy cảm của Token:** Token được gửi trong header `Authorization` là loại token gì (ví dụ: JWT, session token)? Nó có thời hạn sử dụng không? Token này có được lưu trữ an toàn trên thiết bị không?
*   **Cấu hình lắng nghe của Server:** Nếu `API_URL` chỉ là `localhost` hoặc một IP nội bộ, liệu server API (nếu có) có đang lắng nghe trên cổng HTTP hay HTTPS?
*   **Tác động lên Production Environment:** Xác định xem phiên bản production của EShop có sử dụng `API_URL` này hay không và liệu nó có khả năng bị ảnh hưởng bởi traffic over HTTP không mã hóa hay không.

---