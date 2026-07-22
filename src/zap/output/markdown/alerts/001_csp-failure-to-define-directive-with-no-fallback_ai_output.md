```markdown
## 1. Phân loại  
**True Positive**

## 2. Lý do phân loại dựa trên runtime evidence của cả nhóm endpoint  
- Tất cả 15 endpoint/quá trình response quan sát được đều trả về header `Content-Security-Policy` với giá trị duy nhất là `default-src 'none'`.  
- Theo CSP spec, directive `default-src` là directive fallback dùng để áp dụng cho các directive khác nếu chúng không được khai báo riêng lẻ. Tuy nhiên, cảnh báo từ ZAP chỉ ra rằng CSP hiện tại "fails to define directive with no fallback", nghĩa là một hoặc một số directive bắt buộc hoặc không có fallback (như `script-src`, `style-src`, `img-src`...) không được định nghĩa trong policy, dẫn đến việc trình duyệt có thể bỏ qua hoặc thực thi policy không đúng như mong đợi.  
- Ở đây, chỉ mỗi `default-src 'none'` được set, nhưng đoạn thông báo cảnh báo CSP còn thiếu các directive cụ thể cần thiết, có thể gây hiểu nhầm rằng policy không thực sự giới hạn một số tài nguyên như script hoặc style. Do đó, CSP thực tế không chặt chẽ như ý muốn, nguy cơ bypass policy giảm thiểu nguy cơ XSS bị gia tăng.  
- Ứng dụng trả về 404 cho các endpoint này, thể hiện các đường dẫn này không phục vụ nội dung hợp lệ. Tuy nhiên CSP vẫn được set trên tất cả các response đó, cho thấy policy này được áp cho toàn bộ ứng dụng hoặc server.  
- Kết luận: đây là một vấn đề hệ thống liên quan cách cấu hình CSP không đầy đủ, ảnh hưởng rộng cho toàn bộ ứng dụng chứ không riêng endpoint nào.

## 3. Tác động thực tế trong bối cảnh EShop  
- CSP yếu/kém có thể tăng khả năng xảy ra các cuộc tấn công XSS (Cross-Site Scripting), đặc biệt trong các phần UI có tương tác người dùng hoặc tải các nội dung bên ngoài (script, style, hình ảnh).  
- Do CSP hiện tại chỉ đặt `default-src 'none'` mà không định nghĩa rõ ràng `script-src`, `style-src`, ... nên khi trình duyệt không hỗ trợ đầy đủ hoặc hiểu sai policy, có thể coi như không có hạn chế nào cho các nguồn tài nguyên này.  
- Ứng dụng EShop có thể bị lợi dụng qua kỹ thuật injection script hoặc tải tài nguyên nguy hiểm từ nguồn không đáng tin cậy, dẫn đến lộ dữ liệu người dùng, chiếm quyền session, hoặc thực thi mã độc.  
- Đây là điểm yếu bảo mật tương đối trung bình (Medium risk), đặc biệt trong trường hợp ứng dụng có thành phần front-end phức tạp.  
- Nếu trong bối cảnh này các endpoint trả 404 không phục vụ dữ liệu người dùng hay tài nguyên quan trọng, thì tác động trực tiếp trên các endpoint đó thấp, nhưng CSP áp chung cho toàn hệ thống có thể vẫn chưa đủ chặt chẽ.  
- Cần đánh giá thêm mức độ nội dung thực tế được phục vụ ở các endpoint khác không trong danh sách, nhất là các trang UI quan trọng.

## 4. Cách khắc phục cụ thể ở cấp cấu hình/root cause  
- Cấu hình lại header `Content-Security-Policy` tại server hoặc bất cứ thành phần middleware nào:  
  - Định nghĩa đầy đủ các directive quan trọng như `script-src`, `style-src`, `img-src`, `connect-src` với các nguồn tin cậy rõ ràng.  
  - Tránh dùng chỉ duy nhất `default-src 'none'` mà không có các directive fallback khác hoặc bổ sung.  
  - Ví dụ:  
    ```http
    Content-Security-Policy: default-src 'none'; script-src 'self' cdn.trusted.com; style-src 'self'; img-src 'self' data:;
    ```  
  - Điều này đảm bảo CSP được trình duyệt áp dụng chính xác, hạn chế tài nguyên tải từ nguồn không tin cậy.  
- Kiểm tra và cập nhật CSP phù hợp cho từng môi trường (dev, staging, production).  
- Nếu có các endpoint trả lỗi 404 hoặc tĩnh (robots.txt, sitemap.xml) có thể không cần thiết lập CSP quá phức tạp, nhưng nên đồng nhất policy chung tránh sai lệch.  
- Thực hiện test lại CSP sau thay đổi bằng tools hỗ trợ hoặc trình duyệt để đảm bảo chính sách được áp dụng đúng.

## 5. Ghi chú tester cần kiểm tra thêm nếu chưa đủ context  
- Xác nhận môi trường chạy thử hiện tại là môi trường development hay production để đánh giá mức độ nghiêm trọng thực tế. Ở localhost, policy thường có thể chưa hoàn chỉnh.  
- Kiểm tra các trang/endpoint khác có phục vụ nội dung người dùng hoặc UI tương tác để xác định CSP hiện tại có áp dụng cho chúng không, có đủ chặt chẽ hay không.  
- Kiểm định kỹ các directive CSP mà ứng dụng backend hoặc frontend có thể đang thiếu (như script-src, style-src, connect-src...) trong các phản hồi chính thức (200 OK).  
- Kiểm tra liệu có bất cứ CSP header thừa/nghịch lý (như `unsafe-inline`, `unsafe-eval`) nào được set trên các response khác ảnh hưởng đến an toàn toàn hệ thống.  
- Phối hợp với dev để cập nhật chính sách CSP chuẩn kinh nghiệm theo OWASP CSP recommendations cho từng thành phần frontend/backend ứng dụng.  
- Kiểm tra tương thích CSP trên các trình duyệt dùng phổ biến trong môi trường người dùng EShop.

---

**Tóm lại:** alert này là True Positive cho vấn đề cấu hình CSP chưa đầy đủ, cần bổ sung các directive cần thiết để chính sách bảo mật hiệu quả, giảm thiểu nguy cơ khai thác qua XSS cho toàn hệ thống EShop.