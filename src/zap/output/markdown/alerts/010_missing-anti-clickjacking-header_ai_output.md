```markdown
# Triage Alert ZAP-010: Missing Anti-clickjacking Header (Plugin ID: 10020)

---

## 1. Phân loại  
**True Positive**

---

## 2. Lý do phân loại dựa trên runtime evidence của cả nhóm endpoint  
- Toàn bộ 14 endpoint của ứng dụng EShop (gồm giao diện user và admin, đa phần các trang trả về HTML) đều không có header `X-Frame-Options` cũng như không có header `Content-Security-Policy` với directive `frame-ancestors`.  
- ZAP scan runtime ghi nhận rõ ràng HTTP response trả về thiếu các header bảo vệ chống clickjacking.  
- Đặc biệt, các trang HTML chính (gốc `/`, `/forgot-password`) đều bị ảnh hưởng.  
- Không có evidence cho thấy có header thay thế hoặc chính sách CSP frame-ancestors.  
- Các resource như `robots.txt`, `sitemap.xml` không bắt buộc phải có nhưng vẫn không ảnh hưởng tới việc bảo vệ chống iframe ít nhất ở các trang giao diện chính.  
- Môi trường là localhost nhưng thông tin này chỉ làm rõ thêm ngữ cảnh, không làm giảm mức độ thực tế của lỗ hổng nếu triển khai tương tự trên môi trường sản xuất.

---

## 3. Tác động thực tế trong bối cảnh EShop  
- Thiếu header chống clickjacking tạo điều kiện cho attacker sử dụng kỹ thuật clickjacking, bẫy người dùng tương tác với trang EShop thông qua iframe độc hại từ trang khác, dẫn đến việc thực hiện các hành động không mong muốn (ví dụ: chuyển khoản, thay đổi thông tin, đặt hàng).  
- Trang `/forgot-password` hoặc các trang nhạy cảm khác nếu bị clickjacked sẽ có nguy cơ cao bị lợi dụng làm lừa đảo hoặc chiếm quyền tài khoản.  
- Mức độ rủi ro được đánh giá là Medium phù hợp, do đây là một lớp bảo vệ tiêu chuẩn cơ bản trong chính sách bảo mật web, không thuộc lỗi nghiêm trọng nhưng dễ khai thác nếu kết hợp với social engineering.  
- Ảnh hưởng đến độ tin cậy và an toàn tổng thể của ứng dụng, làm giảm sự tin tưởng người dùng và uy tín thương hiệu EShop.

---

## 4. Cách khắc phục cụ thể ở cấp cấu hình/root cause  
- Thêm header HTTP bảo vệ iframe trong response của ứng dụng trên tất cả các trang HTML:  
  - Sử dụng header `X-Frame-Options` với giá trị phù hợp:  
    - `DENY` nếu trang không nên được nhúng bởi bất kỳ trang nào khác.  
    - `SAMEORIGIN` nếu chỉ cho phép nhúng trong cùng origin.  
  - Hoặc thay thế/quyết định sử dụng `Content-Security-Policy` với directive:  
    ```http
    Content-Security-Policy: frame-ancestors 'self'
    ```  
- Cập nhật cấu hình server (Apache, Nginx, hay backend framework) hoặc áp dụng tại lớp trung gian (proxy, CDN, WAF) để đảm bảo tất cả response HTML trả về đều có header này.  
- Kiểm tra lại các trang critical như login, forgot-password, user profile, thanh toán để đảm bảo nhất quán.  
- Tài liệu tham khảo chuẩn và công cụ hỗ trợ:  
  - Mozilla Doc: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options  
  - OWASP Cheat Sheet về Clickjacking Defense.

---

## 5. Ghi chú tester cần kiểm tra thêm nếu chưa đủ context  
- Xác nhận môi trường triển khai thực tế (production, staging) có cấu hình header tương tự hay khác so với dev/localhost.  
- Kiểm tra hiện trạng có sử dụng CSP frame-ancestors ở ngoài scope ZAP scan (ví dụ các response khác hoặc thông qua meta tag).  
- Đánh giá business impact chi tiết hơn với bộ phận nghiệp vụ, nhất là với các trang có giao dịch nhạy cảm hoặc chứa dữ liệu quan trọng.  
- Kiểm tra ảnh hưởng khi trang có nhúng iframe hợp pháp có thể bị header này chặn, để có lựa chọn cấu hình phù hợp (ví dụ dùng CSP frame-ancestors tinh chỉnh hơn).  
- Nếu sử dụng CDN hoặc proxy layer, xác nhận không bị strip header khi response qua các lớp trung gian.

---

**Tóm lại:** hiện tại các alert ZAP-010 đều phản ánh tình trạng thiếu header chống clickjacking trên nhiều endpoint quan trọng, do đó đánh giá là True Positive, cần ưu tiên bổ sung header bảo vệ ngay để giảm thiểu rủi ro clickjacking cho ứng dụng EShop.
```