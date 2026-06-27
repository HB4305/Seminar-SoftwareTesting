# 1. Nội dung cần tìm hiểu
- DAST (Dynamic Application Security Testing)
- ZAP Baseline / Passive / Active scan
- Cấu hình Target (Target config)
- Phân tích cảnh báo (Alert triage) & Prompt triage cho runtime alert
- Báo cáo vấn đề runtime (Report runtime issue)

# 2. Output 
**1. Quy trình thực hiện (Workflow):**
1. Chạy EShop
2. Cấu hình target
3. Chạy ZAP baseline
4. Chọn alert
5. Prompt Gemini (AI Triage)
6. Audit PoC / Fix
7. Ghi nhận runtime evidence
8. Xuất report

**2. Tài liệu đầu ra:**
- ZAP Alert Note
- AI Triage Note
- Finding Report cho runtime alert

---

# 3. DAST

## 1. Khái niệm
**Dynamic Application Security Testing (DAST)**
- Là một phương pháp kiểm thử bảo mật “Black-Box”. Kiểm tra các lỗ hổng từ bên ngoài vào các API đang chạy mà không cần tiếp cận source code. 
- Giả lập các cuộc tấn công, thu thập phản hồi, phân tích để phát hiện lỗ hổng khi ứng dụng ở trạng thái đang chạy (running state). 

## 2. Cơ chế hoạt động
- **Phương pháp hộp đen:** Không cần truy cập hay phân tích source code.
- **Mô phỏng tấn công:** Giả lập các payload tấn công thực tế vào các API/endpoint đang hoạt động và đánh giá phản hồi.
- **Phân tích trong thời gian chạy (Runtime):** Đánh giá chính xác các lỗ hổng khi ứng dụng thực sự đang thực thi trong môi trường runtime.

## 3. Các lỗ hổng thường được phát hiện
- **SQL Injection:** Lỗ hổng cho phép hacker chèn các đoạn mã SQL vào input của user, từ đó can thiệp và thao tác trái phép với database của ứng dụng.
- **Cross-Site Scripting (XSS):** Lỗ hổng cho phép hacker chèn mã độc (thường là JavaScript) vào trang web. Khi user truy cập vào trang chứa mã độc, đoạn mã đó sẽ thực thi trên trình duyệt của user để đánh cắp thông tin (cookie, session).
- **Authentication / Authorization (Bao gồm Cross-Site Request Forgery - CSRF):** Các lỗ hổng liên quan đến xác thực và phân quyền. Hacker có thể giả mạo user, mượn quyền user hoặc nâng quyền để thực hiện các hành động trái phép.
- **Server Misconfigurations:** Lỗ hổng phát sinh do cấu hình server không an toàn, dẫn đến việc để lộ các thông tin nhạy cảm (như thông báo lỗi chi tiết, thư mục hệ thống).
- **Lỗi logic nghiệp vụ (Business Logic Flaws):** Lỗ hổng phát sinh từ logic nghiệp vụ của ứng dụng khi user tương tác. Ví dụ: User sử dụng công cụ chặn bắt gói tin để sửa giá trị đơn hàng từ 100.000.000 đồng thành 100.000 đồng khi thanh toán.

## 4. Các công cụ DAST phổ biến 
- **OWASP ZAP:** Mã nguồn mở, miễn phí, chuyên dụng để quét lỗ hổng ứng dụng web.
- **Burp Suite:** Công cụ phổ biến nhất trong ngành bảo mật, mạnh mẽ và hỗ trợ kho extension đa dạng.
- **StackHawk:** Công cụ hiện đại, được thiết kế tối ưu để dễ dàng tích hợp vào quy trình CI/CD.

## 5. Reference
- https://devops.vn/posts/dast-la-gi-cach-dung-trong-devops/
- https://www.stackhawk.com/blog/what-is-dast/

---
# 4. OWASP

## 1. OWASP - Open Web Application Security Project
- Là tổ chức phi lợi nhuận quốc tế với mục tiêu cốt lõi là cải thiện an ninh phần mềm.
- Sứ mệnh: Nâng cao tính an toàn của phần mềm thông qua các sáng kiến mã nguồn mở do cộng đồng dẫn dắt và các chương trình giáo dục cộng đồng.
- Cộng đồng: Mạng lưới rộng lớn bao gồm hàng trăm chi nhánh (chapters) trên toàn thế giới, hàng chục nghìn thành viên và thường xuyên tổ chức các hội nghị bảo mật quy mô địa phương cũng như toàn cầu (như Global AppSec).
- Tính trung lập: Duy trì sự trung lập với các nhà cung cấp (vendor-neutral), tận dụng trí tuệ tập thể của các chuyên gia bảo mật hàng đầu thế giới để đưa ra các hướng dẫn khách quan.
- Các dự án tiêu biểu:
    - OWASP Top Ten: Danh sách 10 rủi ro bảo mật ứng dụng web quan trọng nhất.
    - ASVS (Application Security Verification Standard): Tiêu chuẩn xác minh bảo mật ứng dụng.
    - SAMM (Software Assurance Maturity Model): Mô hình đánh giá mức độ trưởng thành của quy trình bảo mật phần mềm.
    - OWASP Juice Shop: Một ứng dụng web được thiết kế sẵn các lỗ hổng để phục vụ đào tạo.
## 2. Reference
- https://owasp.org/about/
---

# 5. OWASP ZAP

## 1. Khái niệm
**OWASP ZAP (Zed Attack Proxy)** là một công cụ hỗ trợ phát hiện các lỗ hổng bảo mật trong ứng dụng web, được phát triển bởi cộng đồng Open Web Application Security Project (OWASP) và hoàn toàn mã nguồn mở. 

Hoạt động cốt lõi của ZAP tương tự như một proxy server, thường được gọi là mô hình **Manipulator-in-the-middle (MitM)**. Khi trình duyệt được cấu hình để gửi lưu lượng mạng (HTTP/HTTPS) đi qua ZAP, công cụ này có khả năng chặn bắt (intercept), phân tích (inspect) và chỉnh sửa (modify) bất kỳ gói tin request hay response nào theo thời gian thực.

## 2. Các tính năng
- **Proxy Intercept:** Nằm giữa trình duyệt và ứng dụng web. Cho phép kiểm thử viên đặt điểm dừng (breakpoint) để tạm dừng gói tin, chỉnh sửa tham số (ví dụ: sửa đổi dữ liệu form, header hoặc token) trước khi chuyển tiếp đến server để kiểm tra phản ứng của hệ thống.
- **Spider:** Trước khi tiến hành quét lỗ hổng, ZAP cần khám phá và sơ đồ hóa cấu trúc ứng dụng:
  - **Traditional Spider:** Khám phá ứng dụng bằng cách phân tích cú pháp mã HTML và đi theo các thẻ liên kết tĩnh (`<a href="...">`). Tốc độ nhanh, hiệu quả nhưng chỉ phù hợp với các trang web tĩnh truyền thống.
  - **AJAX Spider:** Khởi chạy một trình duyệt thực tế ngầm để tương tác (click, cuộn trang, điền form), từ đó phát hiện các endpoint động được tạo ra bởi JavaScript/AJAX.
- **Passive Scan:** Quét bị động, hoàn toàn không can thiệp vào traffic (không chỉnh sửa gói tin và không gửi các request tấn công tới server). Mục đích chính là tìm ra các lỗ hổng cấu hình hoặc rò rỉ thông tin (ví dụ: thiếu HTTP Security Headers, lộ thông tin nhạy cảm qua response header).
- **Active Scan:** Quét chủ động, tự tạo và gửi các request chứa payload độc hại đến server để dò tìm các lỗ hổng như SQL Injection, XSS, CSRF...
- **Baseline Scan:** Là kịch bản kiểm thử tự động hóa đóng gói sẵn (automation script), thường được thực thi thông qua Docker hoặc CLI. Script này kết hợp chạy Spider nhanh và Passive Scan để đánh giá nhanh bảo mật.
- **Fuzzing:** Kỹ thuật thay thế một hoặc nhiều tham số trong gói tin request bằng danh sách lớn các dữ liệu thử nghiệm (Ví dụ: Thay thế tham số email bằng danh sách 1 triệu email hoặc chuỗi ký tự đặc biệt để kiểm tra tính ổn định/lỗi của hệ thống).
- **Report:** Tự động tạo báo cáo chi tiết về các lỗ hổng bảo mật được tìm thấy. Hỗ trợ xuất ra nhiều định dạng khác nhau như: HTML, XML, JSON, PDF...

> **Note**: Có 2 cách chính để sử dụng ZAP: thông qua giao diện người dùng (Desktop App) hoặc thông qua API/CLI. Phương pháp dùng API/CLI thường được áp dụng để tích hợp tự động hóa vào các pipeline CI/CD trong DevOps.

## 3. Target config

## 4. Alert Triage (Phân tích cảnh báo)

## 5. Audit PoC & Runtime Evidence

## 6. Reference
- https://viblo.asia/p/huong-dan-sercurity-testing-bang-tool-owasp-zap-cho-penetration-tester-kiem-thu-xam-nhap-PwlVmg8rJ5Z
- https://www.zaproxy.org/
- https://www.hackerone.com/knowledge-center/owasp-zap-6-key-capabilities-and-quick-tutorial


---

# 6. OWASP Top 10 rule-set
OWASP Top 10 là một tài liệu nâng cao nhận thức tiêu chuẩn dành cho các nhà phát triển và chuyên gia bảo mật ứng dụng web, liệt kê 10 rủi ro bảo mật quan trọng nhất

## 1. A01:2025 - Broken Access Control
1. Vị trí và Tầm quan trọng
    - Xếp hạng: Tiếp tục giữ vị trí số 1 trong danh sách các rủi ro bảo mật ứng dụng web nghiêm trọng nhất.
    - Tỷ lệ xuất hiện: Dữ liệu cho thấy trung bình 3,73% các ứng dụng được kiểm thử có ít nhất một trong 40 Danh mục Điểm yếu Phổ biến (CWEs) thuộc nhóm này.
2. Thay đổi chính trong phiên bản 2025
    - Hợp nhất SSRF: Lỗi Server-Side Request Forgery (SSRF) hiện đã được gộp chung vào danh mục Kiểm soát Truy cập bị Phá vỡ.
3. Bản chất của lỗ hổng
    - Kiểm soát truy cập thực thi các chính sách để người dùng không thể thực hiện các hành động nằm ngoài phạm vi quyền hạn được phép. Khi các rào cản này bị phá vỡ, nó thường dẫn đến việc lộ lọt dữ liệu trái phép, sửa đổi hoặc hủy hoại dữ liệu, hoặc thực hiện các chức năng nghiệp vụ ngoài tầm kiểm soát.
4. Các ví dụ điển hình (Dựa trên hệ thống EShop trong tài liệu) (Phần này test xong validate lại)
    - Rò rỉ phiên làm việc (Stateless Session Replay): Ứng dụng EShop sử dụng cookie để quản lý phiên nhưng không thu hồi token trên máy chủ khi đăng xuất. Điều này cho phép kẻ tấn công sử dụng lại cookie đã đánh cắp để truy cập trái phép vào giỏ hàng của người dùng khác.
    - Ghi đè tệp tin tùy ý (Arbitrary File Overwrite): Thiếu kiểm soát quyền hạn trong việc tải lên tệp tin, cho phép kẻ tấn công sử dụng các đường dẫn như ../ để ghi đè lên các tệp tin hệ thống.
    - Thiếu bảo vệ CSRF: Các điểm cuối thay đổi trạng thái (như tạo mã khôi phục MFA) không có mã kiểm soát chống giả mạo, dẫn đến việc người dùng bị lừa thực hiện hành động ngoài ý muốn.
5. Cách phòng tránh và Khắc phục
    - Nguyên tắc đặc quyền tối thiểu (Least Privilege): Chỉ cấp quyền vừa đủ cho người dùng hoặc các định danh không phải con người (như AI agents) để thực hiện công việc của họ.
    - Cơ chế thu hồi phía máy chủ: Đối với các ứng dụng sử dụng cookie stateless, cần triển khai lớp lưu trữ (như Redis) để danh sách đen các token đã đăng xuất cho đến khi chúng hết hạn tự nhiên.
    - Kiểm soát tập trung: Tránh việc thực thi kiểm soát truy cập phân tán ở nhiều nơi trong mã nguồn; thay vào đó nên sử dụng các framework hoặc middleware chuẩn hóa.
    - Sử dụng công cụ hỗ trợ:
        - SAST (Semgrep): Quét mã nguồn để tìm các mô hình khởi tạo cookie không an toàn (thiếu cờ HttpOnly).
        - DAST (OWASP ZAP): Rà quét động để xác thực xem các trang nhạy cảm có thực sự được bảo vệ sau cổng đăng nhập hay không.
        - AI (Gemini): Hỗ trợ phân tích bối cảnh để lọc bỏ các lỗi giả (False Positives) và gợi ý các đoạn mã vá lỗi an toàn.
## 2. A02:2025 - Security Misconfiguration
## 3. A03:2025 - Software Supply Chain Failures
## 4. A04:2025 - Cryptographic Failures
## 5. A05:2025 - Injection
## 6. A06:2025 - Insecure Design
## 7. A07:2025 - Authentication Failures
## 8. A08:2025 - Software or Data Integrity Failures
## 9. A09:2025 - Security Logging and Alerting Failures
## 10. A10:2025 - Mishandling of Exceptional Conditions

**Note (Mẫu sử dụng)**
- **1. Khái niệm & Nguyên nhân:** Lỗ hổng xảy ra khi ứng dụng không kiểm tra quyền truy cập của user tại backend trước khi thực hiện hành động.
- **2. Kịch bản & Tác động:** User A (ID=1) đổi tham số trên URL thành `?user_id=2` và xem được thông tin tài khoản của User B. Tác động: Lộ lọt dữ liệu trái phép, leo thang đặc quyền.
- **3. Cơ chế ZAP phát hiện:** Baseline Scan (Passive) thường KHÔNG phát hiện được lỗi này hiệu quả. Cần sử dụng Active Scan kết hợp cấu hình User Session (Access Control Add-on trong ZAP).
- **4. Cấu hình Baseline (zap-baseline.conf):** 
  - Yêu cầu phải cấu hình ZAP Authenticated Scan (cung cấp session/token của 2 user khác nhau).
  - Rule ID liên quan (nếu có bổ sung add-on): Set thành `FAIL` trong CI/CD.
- **5. Sàng lọc cảnh báo (Triage):** Kiểm tra xem API đó có thực sự chứa dữ liệu nhạy cảm hay chỉ là API public (nếu public thì là False Positive).
- **6. Cách khắc phục:** Bắt buộc kiểm tra quyền (Authorization check) dựa vào Token/Session của user tại Backend ở mọi endpoint, không phụ thuộc vào ẩn/hiện UI trên Frontend.

## 11. Reference
- https://www.cloudflare.com/learning/security/threats/owasp-top-10/
- https://owasp.org/Top10/2025/