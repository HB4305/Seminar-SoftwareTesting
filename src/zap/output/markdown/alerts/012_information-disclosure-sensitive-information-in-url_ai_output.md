```markdown
### 1. Phân loại  
**Needs Human Review**

---

### 2. Lý do phân loại dựa trên runtime evidence của cả nhóm endpoint  
- ZAP phát hiện tham số `token` chứa dữ liệu dạng sensitive information được truyền trong URL (query string) ở 3 endpoint có request GET trên hostname `localhost` (dev/lab environment).  
- Evidence chỉ thể hiện token nằm trong URL request, nhưng response không trả về dữ liệu nhạy cảm, cũng không có thông tin cho thấy token bị rò rỉ ra ngoài (như qua response body hay header). Response 101 Switching Protocols chỉ là giai đoạn thiết lập websocket, không có dữ liệu thực thi hay phản hồi chứa sensitive info.  
- Alert có confidence **Medium**, risk level **Informational**, thuộc CWE-598 (Exposure of Sensitive Information to an Unauthorized Actor) và WASC-13 (Information Leakage).  
- Việc truyền `token` trong URL tiềm ẩn nguy cơ bị lộ thông tin nhạy cảm qua logs, cache, browser history,... nhưng trên runtime này chưa xác định được token có phải là credential thực sự, token đó có thể là session token hoặc token truy cập (bearer token đã nằm trong header riêng, riêng biệt) và chưa đủ bằng chứng cho exploit cụ thể.  
- Môi trường localhost/lab có thể không áp dụng mật độ bảo mật cao như production, cần kiểm tra kỹ môi trường triển khai thực tế.  
- Do alert mang tính cảnh báo/khuyến nghị (informational) và chưa có bằng chứng thực tế về leak hay khai thác, nên không nâng mức severity thành cao hơn mà chỉ needs review thêm.  

---

### 3. Tác động thực tế trong bối cảnh EShop  
- Nếu token truyền trong URL là credential hoặc session token, có thể dẫn đến rò rỉ khi URL bị ghi log hoặc lộ cho bên thứ ba (referrer headers, browser history).  
- Mức độ ảnh hưởng trực tiếp ở runtime chưa thấy rõ exploit nhưng về mặt best practice bảo mật, truyền sensitive thông tin qua URL là không an toàn.  
- Với ứng dụng EShop có phân quyền user và admin, token trong URL có thể là attack vector nếu bị đánh cắp phục vụ truy cập trái phép.  
- Tuy nhiên, ở môi trường localhost/lab, đây có thể là đoạn dev/debug hoặc chưa finalize cấu hình bảo mật, nên cần xác nhận lại môi trường thực thi.  

---

### 4. Cách khắc phục cụ thể ở cấp cấu hình/root cause  
- Không truyền thông tin nhạy cảm như token, mật khẩu, session ID qua URL (query string).  
- Sử dụng header HTTP (ví dụ: Authorization header hoặc custom header) để gửi token/bearer token an toàn hơn, tránh ghi lại trong logs hoặc bị lộ qua referrer.  
- Nếu buộc phải truyền một số tham số qua URL, hãy đảm bảo token chỉ là một giá trị temporary, ngắn hạn, hoặc mã hóa/hashing an toàn để giảm rủi ro lộ thông tin.  
- Cấu hình server/application không ghi log đầy đủ query string chứa token, hoặc filter logs để tránh ghi lại các tham số nhạy cảm.  
- Đào tạo developer tuân thủ chính sách bảo mật OWASP và các chuẩn về bảo vệ thông tin nhạy cảm qua giao thức HTTP.  

---

### 5. Ghi chú tester cần kiểm tra thêm nếu chưa đủ context  
- Xác nhận token trong URL có phải là thông tin nhạy cảm thực sự (ví dụ: session token, access token, hoặc một dạng ID nhạy cảm) hay chỉ là code tạm/không dùng cho auth.  
- Kiểm tra môi trường deploy có phải là môi trường production hay staging/localhost để đánh giá mức độ ảnh hưởng thực tế và khuyến cáo phù hợp.  
- Đánh giá xem ứng dụng có ghi lại logs request bao gồm token trong URL hay không, xem logs có bị rò rỉ ra bên ngoài (vd: hệ thống giám sát, firewall, proxy).  
- Kiểm thử trường hợp token bị lộ qua referer header đến website thứ ba khi ứng dụng thực hiện các redirect/external link.  
- Đánh giá cách token được tạo và expires như thế nào, độ an toàn khi lưu trữ/mã hóa token.  
- Tham khảo team phát triển để kiểm tra kế hoạch cải thiện bảo mật HTTP API theo chính sách OWASP hoặc quy định nội bộ.  
```