```markdown
# Triage Alert OWASP ZAP - ZAP-004: X-Content-Type-Options Header Missing

---

## 1. Phân loại  
**True Positive**

---

## 2. Lý do phân loại dựa trên runtime evidence của cả nhóm endpoint  
- Qua quan sát các response ở đa số các endpoint (backend, frontend user, frontend admin), header `X-Content-Type-Options` không được thiết lập, hoặc thiếu hoàn toàn, theo như alert chỉ ra.  
- ZAP-004 là alert cảnh báo thiếu header bảo mật `X-Content-Type-Options: nosniff`, một header quan trọng để ngăn chặn trình duyệt thực hiện MIME-sniffing, tức là dựa vào nội dung thực tế của payload để đoán kiểu MIME, gây ra nguy cơ hiểu nhầm loại nội dung, dẫn đến một số khai thác cross-site scripting (XSS) hoặc tấn công chèn mã khác có thể xảy ra.  
- Header `Content-Type` được server trả về tương đối đầy đủ (ví dụ: `application/json; charset=utf-8`, `text/html`), nhưng thiếu `X-Content-Type-Options` là thiếu sót cấu hình bảo mật phổ biến.  
- Số lượng endpoint bị ảnh hưởng lớn (27 endpoints), trải khắp backend và frontend, là dấu hiệu của lỗi cấu hình mang tính hệ thống.  
- Không có bằng chứng _false positive_ hoặc ngoại lệ liên quan đến môi trường localhost kiểm tra.  
- Mức độ cảnh báo của ZAP là Low, confidence Medium phù hợp với mức độ và ảnh hưởng của header này.

---

## 3. Tác động thực tế trong bối cảnh EShop  
- Tác động chính:  
  - Nếu thiếu header `X-Content-Type-Options: nosniff`, các trình duyệt cũ (IE, Chrome legacy) có thể thực hiện MIME-sniffing dẫn đến việc tải và thực thi tài nguyên theo kiểu không mong muốn (ví dụ: thực thi script từ file văn bản, hình ảnh).  
  - Điều này làm tăng nguy cơ khai thác XSS hoặc drive-by-download, đặc biệt trong điều kiện có kẽ hở khác hoặc payload phản hồi chứa nội dung có thể bị lợi dụng.  
  - Tuy nhiên, trong bối cảnh EShop:  
    - Phần lớn response đã trả đúng `Content-Type`.  
    - Mức độ rủi ro được đánh giá là thấp (Low) vì ứng dụng không để lộ payload có thể khai thác cao trong response và không là môi trường công khai có rủi ro mạng phức tạp cao.  
    - Tác động sẽ tăng nếu có các kẽ hở mã hóa XSS, injection, nhưng đây là vấn đề riêng biệt.  
- Do đó, đây là một điểm cấu hình bảo mật hệ thống cần được khắc phục để hoàn thiện, không phải lỗi critical nghiêm trọng ngay lập tức.

---

## 4. Cách khắc phục cụ thể ở cấp cấu hình/root cause  
- Cấu hình server hoặc reverse proxy (ví dụ Nginx, Apache, Express middleware) thêm header HTTP:  
  ```
  X-Content-Type-Options: nosniff
  ```  
- Cụ thể:  
  - Với Express (Node.js), dùng middleware như `helmet` với dòng:  
    ```js
    app.use(helmet.noSniff());
    ```  
  - Với Nginx, thêm vào block `server` hoặc `location`:  
    ```
    add_header X-Content-Type-Options nosniff;
    ```  
  - Với Apache, thêm directive:  
    ```
    Header set X-Content-Type-Options "nosniff"
    ```  
- Đảm bảo header này được set cho tất cả các response trả về (API backend, frontend, static resources)  
- Kiểm tra lại cấu hình để header không bị ghi đè hoặc xóa bỏ bởi middleware khác.  

---

## 5. Ghi chú tester cần kiểm tra thêm nếu chưa đủ context  
- Xác nhận môi trường triển khai thực tế (production hoặc staging) có cấu hình tương đồng với môi trường localhost được scan.  
- Kiểm tra log server hoặc cấu hình middleware để đảm bảo header thực sự chưa được set, tránh trường hợp header bị chặn bởi proxy hoặc công cụ scan không đọc đúng response.  
- Đánh giá lại các endpoint có trả payload dạng đặc biệt (vd: file download, HTML upload, dữ liệu được user upload) xem có nguy cơ khai thác cao hơn từ việc thiếu header này không.  
- Kiểm tra khả năng tương thích với các trình duyệt hiện tại khách hàng sử dụng (nếu chủ yếu dùng trình duyệt hiện đại, tác động có thể thấp hơn).  
- Đánh giá biện pháp bảo vệ bổ trợ khác như CSP, CORS để phối hợp với khắc phục này.

---

**Tóm lại:** đây là một vulnerability bảo mật cấu hình hệ thống với xác suất thực sự xảy ra rủi ro trên các rủi ro thứ cấp. Việc bổ sung header `X-Content-Type-Options: nosniff` cho tất cả response được khuyến cáo để tăng cường an toàn chống lại các tấn công dựa trên MIME sniffing.  
```