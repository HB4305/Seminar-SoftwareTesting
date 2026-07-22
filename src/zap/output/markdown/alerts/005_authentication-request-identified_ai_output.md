```markdown
### 1. Phân loại  
Needs Human Review

### 2. Lý do phân loại dựa trên runtime evidence của cả nhóm endpoint  
- Nhóm alert này đều phát hiện trên cùng một endpoint `/api/login` với method POST và payload chứa credential (`email`, `password`), thực hiện hành vi xác thực (authentication request).  
- Đây là một alert loại Informational, ZAP chỉ nhận biết đây là request xác thực mà không chỉ ra bất kỳ vấn đề bảo mật cụ thể nào trong request hoặc response.  
- Request/response runtime cho thấy endpoint hoạt động bình thường: trả về HTTP 200 OK và một token JWT hợp lệ.  
- Tuy nhiên, trong response body hiển thị **cleartext password** của user (`"password": "Test1234!"`), đây là dấu hiệu rò rỉ thông tin nhạy cảm nghiêm trọng.  
- ZAP không cảnh báo về việc lộ password hay issue bảo mật khác, chỉ phát hiện dạng Authentication Request.  
- Do đó, alert này tự nó không phải là lỗ hổng, nhưng response body chứa thông tin password không mã hóa/phải ẩn đi mới đúng. Việc này là dấu hiệu cần đánh giá thêm.  
- Vì vậy cần review thêm để đánh giá mức độ rò rỉ, phạm vi ảnh hưởng, và kiểm tra nguyên nhân tại source (API trả về password).

### 3. Tác động thực tế trong bối cảnh EShop  
- Việc trả về rõ ràng password trong response là hành vi rất nguy hiểm, làm lộ credential người dùng nếu attacker bắt được traffic hoặc có thể từ các module frontend/admin truy cập API.  
- Gây mất an toàn dữ liệu cá nhân, tăng nguy cơ tấn công tiếp theo như đánh cắp tài khoản, đặc biệt với các token JWT dùng để xác thực phiên làm việc.  
- Trong môi trường localhost/lab, có thể chỉ là môi trường test, nhưng nếu deploy production mà vẫn giữ hành vi này thì rất nghiêm trọng, ảnh hưởng trực tiếp đến bảo mật tài khoản người dùng.

### 4. Cách khắc phục cụ thể ở cấp cấu hình/root cause  
- Sửa backend API `/api/login` không trả về trường `password` trong response body, hoặc nếu cần thì chỉ trả về thông tin an toàn không nhạy cảm (id, role, email, name nhưng không có password).  
- Kiểm tra và kiểm soát luồng dữ liệu nhạy cảm đặc biệt với password, tuyệt đối không đưa password vào response cho client dưới mọi hình thức.  
- Đánh giá lại cấu trúc JWT và cách quản lý token để đảm bảo không dính thông tin mật hay không hợp lệ.  
- Tăng cường kiểm thử kiểm soát dữ liệu nhạy cảm trong API response ở vòng phát triển.

### 5. Ghi chú tester cần kiểm tra thêm nếu chưa đủ context  
- Xác nhận môi trường deploy thực tế có giống với lab/local này không để đánh giá mức độ nghiêm trọng trong thực tế.  
- Kiểm tra toàn bộ các endpoint khác có lặp lại lỗi tương tự (trả về password hay dữ liệu nhạy cảm không cần thiết).  
- Đánh giá xem token JWT có chứa thông tin nhạy cảm hay khả năng bị khai thác cao không.  
- Cần rà soát chính sách logging, caching, và cách frontend sử dụng response liệu có làm lộ thông tin nhạy cảm ở client-side hay không.  
- Phối hợp với dev để truy vết root cause API trả password trong response và xây dựng testcase ngăn lỗi này tái diễn.
```