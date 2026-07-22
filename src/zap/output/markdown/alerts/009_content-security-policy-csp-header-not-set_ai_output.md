```markdown
## 1. Phân loại  
**True Positive**

## 2. Lý do phân loại dựa trên runtime evidence của cả nhóm endpoint  
- Tất cả 14 endpoint đều trả response HTTP không có header `Content-Security-Policy` (CSP).  
- Đây không phải là false positive vì ZAP quan sát trực tiếp từ response runtime nên xác nhận header này hoàn toàn thiếu.  
- Endpoint đa phần là các giao diện frontend (HTML), tập trung ở các URL cơ bản như `/`, `/forgot-password`, `robots.txt`, `sitemap.xml` thuộc hai source JSON khác nhau đại diện cho user lẫn admin.  
- Header CSP là một chính sách bảo mật quan trọng giúp ngăn các cuộc tấn công XSS và injection trên client, việc thiếu header này tạo điều kiện cho attacker tiềm năng khai thác các lỗ hổng phía client.  
- Scanner có confidence cao, alert Medium risk, phù hợp với mức độ cảnh báo vì thiếu CSP là một lỗ hổng bảo mật "systemic" (toàn hệ thống) chứ không chỉ ở một endpoint riêng lẻ.  
- Không có evidence cho thấy server đã cấu hình CSP hoặc có policy thay thế khác.  
- Môi trường `localhost` tuy thuộc dạng lab/dev nhưng vẫn đáng quan tâm vì dễ bị tấn công nếu deploy ra môi trường thật mà quên cấu hình.

## 3. Tác động thực tế trong bối cảnh EShop  
- Ứng dụng EShop, dù là frontend, thường chứa các kịch bản nhập liệu, hiển thị nội dung người dùng, hoặc tích hợp script từ nhiều nguồn.  
- Thiếu CSP tăng khả năng tấn công Cross-Site Scripting (XSS), có thể dẫn đến đánh cắp session, thao túng giao diện, thực hiện hành vi giả mạo (phishing), hoặc tiêm mã độc hại.  
- Ảnh hưởng nghiêm trọng hơn nếu site này xử lý thông tin nhạy cảm khách hàng hoặc có quyền admin (frontend_admin_basic.json).  
- Dù chưa phát hiện dấu hiệu bị khai thác hoặc chứa dữ liệu quan trọng trong response, việc không có CSP làm giảm rõ rệt mức độ an toàn của toàn bộ frontend, mất một lớp phòng vệ bổ sung.

## 4. Cách khắc phục cụ thể ở cấp cấu hình/root cause  
- Cấu hình web server (nghĩa là HTTP server như Nginx, Apache hoặc reverse proxy, hoặc application server) bổ sung HTTP header `Content-Security-Policy`.  
- Xác định chính sách CSP phù hợp với tính năng ứng dụng, ví dụ:  
  - `default-src 'self'` để giới hạn tài nguyên chỉ được load từ chính domain.  
  - Thêm các chỉ thị cho phép script, style, hình ảnh… theo nhu cầu (cẩn trọng với `'unsafe-inline'`, `'unsafe-eval'`).  
- Ví dụ header đơn giản ban đầu có thể như:  
  ```
  Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self'
  ```  
- Kiểm thử kỹ CSP để tránh làm đứt gãy tính năng frontend, đặc biệt với các frontend framework như React, Angular, Vite…  
- Đảm bảo CSP áp dụng đồng bộ cho tất cả endpoint trả về content HTML hoặc có nội dung được tải trên trình duyệt.

## 5. Ghi chú tester cần kiểm tra thêm nếu chưa đủ context  
- Xác nhận môi trường deploy thực tế (production) có nhận header CSP hay không, vì hiện tại đang scan trên localhost có thể chưa phản ánh cấu hình thực tế.  
- Kiểm tra kỹ các response trả về tài nguyên tĩnh (JS, CSS, fonts, images...) có cần chính sách CSP phức tạp hơn để tránh lỗi load tài nguyên.  
- Nếu đang dùng CDN, kiểm tra cấu hình chính sách CSP trên tầng CDN, proxy.  
- Đảm bảo rằng các chính sách CSP không ảnh hưởng đến chức năng nội bộ như hot reload (ví dụ đoạn script `/@vite/client` trong response cần đánh giá).  
- Xem xét bổ sung các header bảo mật khác bổ trợ như `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy` để nâng cao tổng thể an toàn frontend.

---

**Kết luận:** nhóm alert `ZAP-009 Content Security Policy (CSP) Header Not Set` thực sự tồn tại trên toàn bộ nhóm endpoint test, cần khẩn trương bổ sung CSP header với policy phù hợp nhằm hạn chế rủi ro XSS/Injection trên frontend của ứng dụng EShop.
```