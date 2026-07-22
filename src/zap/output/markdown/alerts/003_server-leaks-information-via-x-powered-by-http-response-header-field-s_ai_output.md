```markdown
# Đánh giá nhóm alert ZAP-003: Server Leaks Information via "X-Powered-By" HTTP Response Header Field(s)

---

## 1. Phân loại  
**True Positive**

---

## 2. Lý do phân loại dựa trên runtime evidence của cả nhóm endpoint  
- Tất cả 15 endpoint (bao gồm backend và frontend, user và admin) đều trả về HTTP response header có trường `X-Powered-By: Express`.  
- Đây là hành vi cấu hình server/framework mặc định chưa được tắt, trực tiếp tiết lộ rõ ràng tên framework backend đang sử dụng.  
- ZAP thu thập trực tiếp header qua HTTP response runtime, không phải suy đoán hay giả định.  
- Đã kiểm tra request có Authorization token, response vẫn leak header, chứng tỏ không được hạn chế theo context auth hay role.  
- Mức độ confidence: Medium (áp dụng cho cấu hình chung, không phải lỗi logic phức tạp).  
- Không phải trường hợp False Positive vì header thực sự xuất hiện trên mọi response, bao gồm cả response lỗi (404) và response thành công (200).  
- Không chỉ là informational đơn thuần vì dễ bị attacker dùng để fingerprint framework, từ đó xác định vector tấn công tiềm năng hoặc khai thác lỗ hổng known của Express phiên bản cụ thể.

---

## 3. Tác động thực tế trong bối cảnh EShop  
- Rò rỉ thông tin framework backend (Express) giúp attacker:  
  - Hiểu được thành phần công nghệ sử dụng, định hướng tấn công được hiệu quả hơn.  
  - Có thể kiểm tra nhanh các lỗ hổng bảo mật đã biết, phiên bản framework, plugin đang dùng.  
  - Trong trường hợp EShop dùng phiên bản Express cũ, có lỗ hổng thì rất dễ bị khai thác.  

- Tuy mức độ risk được đánh giá là Low theo OWASP ZAP, nhưng đây là một vector thu thập thông tin cơ bản, thuộc phạm vi **reconnaissance phase** của attacker.  
- Nếu kết hợp với các lỗ hổng khác thì nguy cơ gia tăng.  
- Ở môi trường localhost/lab, vẫn đánh giá tồn tại vấn đề nhưng cần xác nhận môi trường production có giữ header này hay không.

---

## 4. Cách khắc phục cụ thể ở cấp cấu hình/root cause  
- Tắt header `X-Powered-By` trên server Express bằng cách cấu hình trong source code hoặc config server:  
  - Với Express, thêm dòng sau trong code:  
    ```js
    app.disable('x-powered-by');
    ```  
  - Hoặc tương đương cấu hình cho các server/proxy (nginx, Apache, load balancer) nếu có pass header này.  
- Kiểm tra các middleware, framework hoặc plugin có thể tự động thêm `X-Powered-By` và tắt/bỏ header tương ứng.  
- Triển khai chính sách bảo mật header (security headers) để loại bỏ thông tin không cần thiết.  
- Thực hiện kiểm tra lại các môi trường phát triển, staging hoặc production để đồng bộ cấu hình.

---

## 5. Ghi chú tester cần kiểm tra thêm nếu chưa đủ context  
- Xác nhận môi trường đang quét là dev/local hoặc staging hay production. Nếu production thì ưu tiên xử lý ngay.  
- Kiểm tra xem có proxy, load balancer hoặc CDN phía trước có thêm lại header này không (có thể ZAP chỉ thấy header do proxy add).  
- Xem xét phiên bản Express đang sử dụng có liên quan tới các lỗ hổng đã biết nào không để đánh giá tác động bảo mật tổng thể.  
- Nếu có policy bảo mật nội bộ hay yêu cầu compliance, cần đối chiếu với chính sách đó về việc leak header.  
- Tham khảo thêm log server để chắc chắn không có các header tương tự phát sinh khi có các loại request khác (PUT, DELETE...).  
- Đánh giá kết hợp với các alert bảo mật khác từ ZAP để đưa ra mức độ ưu tiên xử lý tổng thể.

---

**Kết luận**: Đây là alert dạng True Positive, nên ưu tiên xử lý bằng cách tắt header `X-Powered-By` trên Express ngay để giảm việc rò rỉ thông tin framework backend, ngăn chặn attacker thu thập dữ liệu dùng để định hướng tấn công.  
```