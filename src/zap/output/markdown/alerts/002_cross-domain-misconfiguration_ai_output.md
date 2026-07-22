```markdown
# Triage Alert ZAP-002: Cross-Domain Misconfiguration (Plugin ID 10098)

## 1. Phân loại  
**True Positive**

## 2. Lý do phân loại dựa trên runtime evidence của cả nhóm endpoint  
- Tất cả 12 endpoint được quét đều trả về header `Access-Control-Allow-Origin: *` bất kể endpoint trả về 200 OK hay 404 Not Found.  
- Header CORS này cho phép mọi domain có thể thực hiện các request từ trình duyệt đến API/frontend backend của ứng dụng mà không bị chặn bởi chính sách Same Origin Policy (SOP).  
- Endpoint `/api/users/me` trả về dữ liệu nhạy cảm (thông tin người dùng, bao gồm email, role, thậm chí password dạng chuỗi thường), và vẫn cho phép `Access-Control-Allow-Origin: *`.  
- Việc này hoàn toàn vi phạm nguyên tắc bảo mật về CORS, tạo điều kiện cho các trang web xấu sử dụng JavaScript thực hiện các request lấy dữ liệu người dùng với token hiện tại (Authorization header được gửi theo), dẫn đến rò rỉ dữ liệu.  
- Khả năng giả mạo, đánh cắp dữ liệu người dùng từ nguồn khác (cross-site scripting + CORS) là hiện hữu.  
- Môi trường localhost nhưng behavior này nếu deploy tương tự trên môi trường production thì rất đáng lo ngại.  

## 3. Tác động thực tế trong bối cảnh EShop  
- Có thể dẫn đến lộ thông tin nhạy cảm của người dùng (như tên, email, role, thậm chí mật khẩu ở dạng text—dấu hiệu cấu hình backend không tốt vì trả pass thẳng ra API).  
- Kẻ tấn công đặt trang web có payload độc hại, dụ người dùng có token đang login truy cập. JavaScript trên trang đó sẽ "tự do" lấy dữ liệu từ API do header CORS cho phép, gây rò rỉ thông tin cá nhân/nhạy cảm.  
- Ảnh hưởng đến bảo mật người dùng, gây ảnh hưởng uy tín hệ thống, tăng khả năng tấn công tiếp theo (phishing, chiếm quyền,...).  
- Với các endpoint trả 404 (Không tìm thấy), tuy có CORS mở nhưng không gây rủi ro trực tiếp. Nhưng nhìn chung vẫn thể hiện cấu hình lỏng lẻo, không phân quyền chặt chẽ.  

## 4. Cách khắc phục cụ thể ở cấp cấu hình/root cause  
- **Hạn chế lại giá trị header `Access-Control-Allow-Origin`**:   
  - Không dùng dấu `*`. Chỉ cho phép những origin tin cậy, ví dụ domain frontend chính thức (`https://admin.eshop.com`, `https://www.eshop.com`, hoặc các domain cần thiết).  
  - Có thể dùng dynamic whitelist để phục vụ nhiều origin tùy theo môi trường.  
- **Không gửi header CORS** trên các endpoint không cần thiết hoặc trả 404, để tránh cung cấp kênh Cross-Domain không cần thiết.  
- **Xác thực và phân quyền kỹ càng** cho từng endpoint, đặc biệt endpoint trả dữ liệu người dùng (ví dụ `GET /api/users/me`).  
- **Kiểm soát kỹ thông tin trả về**: tuyệt đối không trả mật khẩu (dù đã hash hay chưa) trong response API.  
- Kiểm tra lại middleware CORS trên backend, cấu hình lại phù hợp theo chính sách bảo mật của tổ chức, tránh cấu hình mở mặc định trong framework.  
- Có thể áp dụng thêm các header bảo mật khác (ví dụ `Access-Control-Allow-Credentials: true` khi dùng cookie, nhưng phải phối hợp với origin whitelist).  

## 5. Ghi chú tester cần kiểm tra thêm nếu chưa đủ context  
- Xác nhận môi trường deploy có giống môi trường runtime được scan không (dev/local hay production). Trường hợp chỉ là localhost dev, vẫn đánh giá để cảnh báo cho production.  
- Kiểm thử xem có khả năng exploit qua trình duyệt hay không: giả lập trang web bên ngoài gọi API để kiểm tra phản hồi có bị lộ dữ liệu nhạy cảm hay không.  
- Kiểm tra header CORS trên các thành phần khác (API admin, các microservices phụ trợ) để đánh giá tổng quan phạm vi lỏng lẻo của cấu hình.  
- Trao đổi với developer để kiểm tra luồng xử lý Authorization header và kiểm soát dữ liệu nhạy cảm có đang bị lộ qua API như trường hợp mật khẩu trong response.  
- Đánh giá thêm về các header bảo mật khác (Content-Security-Policy, X-Frame-Options,...) để đảm bảo tổng thể an toàn ứng dụng.  
- Xác minh việc cấu hình CORS trong code là tĩnh hay động, có xác thực origin request không.  

---

**Tóm lại:** Alert này là **True Positive** với rủi ro trung bình đến nghiêm trọng (medium) do cấu hình CORS quá mở, đặc biệt là khi dữ liệu nhạy cảm trả về API được áp dụng cho cả origin `*`. Đây là lỗ hổng phổ biến nhưng rất cần được xử lý để bảo vệ dữ liệu và người dùng của EShop.  
```