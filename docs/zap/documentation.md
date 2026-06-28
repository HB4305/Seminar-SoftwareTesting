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
    - Xếp hạng: Giữ vị trí số 1 trong OWASP Top 10:2025.
    - Dữ liệu nền: 100% ứng dụng được kiểm thử có ít nhất một biểu hiện liên quan; nhóm này có 40 CWE được ánh xạ, tỷ lệ xuất hiện trung bình 3,74% và số lần xuất hiện rất cao.
    - Điểm đáng chú ý: OWASP đưa cả SSRF vào phạm vi của Broken Access Control trong bản 2025.
2. Bản chất
    - Lỗi xảy ra khi backend không cưỡng chế đúng chính sách phân quyền, khiến user hoặc client có thể đọc, sửa, xóa hoặc gọi chức năng vượt quá quyền được cấp.
    - Các dạng phổ biến gồm IDOR, force browsing, leo thang đặc quyền, bỏ sót kiểm tra quyền ở API `POST/PUT/DELETE`, giả mạo hoặc tái sử dụng JWT/cookie, và CORS mở sai đối tượng.
3. Kịch bản và Tác động
    - Kẻ tấn công đổi tham số `acct`, `userId` hoặc đường dẫn tài nguyên để xem dữ liệu của người khác. Tác động là lộ dữ liệu trái phép và phá vỡ tính riêng tư.
    - User thường hoặc user chưa đăng nhập truy cập được URL quản trị nhờ đoán endpoint hoặc gọi API trực tiếp thay vì đi qua UI. Tác động là leo thang đặc quyền và thao tác nghiệp vụ trái phép.
    - Token/cookie bị replay sau logout hoặc bị sửa metadata để tăng quyền. Tác động là chiếm phiên, thay đổi dữ liệu hoặc thực hiện hành động nhạy cảm.
4. Cơ chế Zap phát hiện
    - `zap-baseline.py` chỉ spider và passive scan nên không đủ để kết luận Broken Access Control; nó chủ yếu phát hiện chỉ dấu gián tiếp như thiếu CSRF token, CORS quá rộng, session ID trên URL.
    - ZAP Access Control Testing add-on cho phép khai báo `Context`, `User`, `Access Rules`, sau đó thử truy cập từng URL dưới góc nhìn từng user để tìm lỗi Improper Authentication `10101` và Improper Authorization `10102`.
    - Forced Browse giúp lộ các URL/đường dẫn bị quên bảo vệ; authenticated spider giúp thu thập thêm các route chỉ hiện sau đăng nhập.
5. Cấu hình baseline
    - Dùng baseline có context và user để crawl đúng vùng cần kiểm thử:
      - `zap-baseline.py -t <target> -n <context_file> -U <user> -j`
    - Nên giữ hoặc nâng mức cảnh báo cho các rule gợi ý lỗi truy cập:
      - `100202 WARN` hoặc `FAIL` cho `CSRF Countermeasures`
      - `10098 WARN` cho `Cross Domain Misconfiguration`
      - `3 FAIL` cho `Session ID in URL Rewrite`
      - `10057 INFO` cho `Username Hash Found` vì có thể gợi ý IDOR
    - Chỉ dùng baseline như lớp phát hiện sớm; để xác nhận A01 cần thêm authenticated scan hoặc Access Control Testing.
6. Sàng lọc cảnh báo (Triage)
    - Kiểm tra endpoint có thật sự là tài nguyên nhạy cảm hay chỉ là tài nguyên public/read-only.
    - So sánh phản hồi giữa user thường, user đặc quyền và user chưa đăng nhập; nếu chỉ khác giao diện nhưng backend vẫn trả dữ liệu thì là lỗ hổng thật.
    - Với CSRF/CORS, xác minh form hoặc origin đó có thuộc luồng hợp lệ hay là ngoại lệ an toàn đã biết.
7. Cách khắc phục
    - Áp dụng nguyên tắc `deny by default` và kiểm tra quyền ở backend cho mọi request.
    - Tập trung hóa cơ chế authorization bằng middleware, policy hoặc framework chuẩn thay vì rải rác trong controller/UI.
    - Ràng buộc quyền theo record ownership, role và business limit; không tin vào tham số do client gửi lên.
    - Thu hồi session phía server khi logout; với JWT nên dùng token ngắn hạn, refresh token và cơ chế revoke phù hợp.
    - Ghi log các lần bị từ chối truy cập và thêm test phân quyền ở mức unit/integration.
## 2. A02:2025 - Security Misconfiguration
1. Vị trí và Tầm quan trọng
    - Xếp hạng: Tăng từ vị trí số 5 lên số 2 trong bản 2025.
    - Dữ liệu nền: 100% ứng dụng được kiểm thử có ít nhất một biểu hiện; tỷ lệ xuất hiện trung bình 3,00% với hơn 719 nghìn occurrence trong dữ liệu OWASP.
    - Xu hướng: Phần mềm, cloud service và framework ngày càng nhiều tuỳ chọn cấu hình nên sai cấu hình trở thành rủi ro nổi bật hơn.
2. Bản chất
    - Đây là nhóm lỗi phát sinh khi hệ thống, ứng dụng hoặc dịch vụ cloud được cấu hình không an toàn.
    - Các biểu hiện điển hình gồm bật tính năng không cần thiết, giữ tài khoản mặc định, lộ stack trace, thiếu security headers, quyền cloud storage quá rộng hoặc giữ cấu hình cũ vì ưu tiên tương thích ngược.
3. Kịch bản và Tác động
    - Ứng dụng mẫu hoặc admin console còn tồn tại trên production và vẫn dùng mật khẩu mặc định. Tác động là bị takeover hệ thống.
    - Directory listing không bị tắt khiến attacker duyệt thư mục, tải class/file cấu hình rồi lần ngược mã nguồn. Tác động là lộ thông tin kỹ thuật và mở đường cho tấn công sâu hơn.
    - Server trả stack trace hoặc thông tin phiên bản chi tiết khi lỗi. Tác động là lộ công nghệ, component dễ bị khai thác.
    - Cloud bucket hoặc tài nguyên chia sẻ ra Internet ngoài ý muốn. Tác động là rò rỉ dữ liệu nhạy cảm trên diện rộng.
4. Cơ chế Zap phát hiện
    - Đây là nhóm mà baseline scan phát huy hiệu quả nhất vì ZAP có nhiều passive rules kiểm tra security headers, cache control, mixed content, lỗi ứng dụng và dấu hiệu lộ thông tin.
    - Các alert hữu ích gồm `10020` Anti-clickjacking Header, `10021` X-Content-Type-Options, `10035` HSTS, `10038` CSP Header Not Set, `90022` Application Errors, `10023` Debug Errors, `10036/10037` lộ thông tin phiên bản server/framework.
    - Active scan có thể bổ sung kiểm tra directory browsing, file lộ thông tin hoặc cấu hình nguy hiểm cụ thể, nhưng baseline thường đã đủ tốt cho vòng sàng lọc ban đầu.
5. Cấu hình baseline
    - Nên chuyển một số rule cấu hình cốt lõi sang mức `FAIL` trong CI/CD:
      - `10020 FAIL`
      - `10021 FAIL`
      - `10035 FAIL`
      - `10038 WARN` hoặc `FAIL` tùy chính sách CSP của dự án
      - `90022 WARN`
      - `10023 WARN`
    - Nếu ứng dụng có form tìm kiếm hoặc trang đặc biệt dễ gây nhiễu, có thể dùng `OUTOFSCOPE` hoặc alert filter thay vì tắt rule toàn cục.
6. Sàng lọc cảnh báo (Triage)
    - Xác nhận alert xuất hiện trên endpoint thật của ứng dụng chứ không phải static asset hoặc redirect trung gian.
    - Với header thiếu, kiểm tra có cơ chế thay thế tương đương hay không, ví dụ `frame-ancestors` trong CSP thay cho `X-Frame-Options`.
    - Với error disclosure, phân biệt lỗi thực sự lộ stack trace/phiên bản với thông báo nghiệp vụ bình thường.
    - Với tài nguyên cloud hoặc sample app, cần xác minh môi trường đích là production hay môi trường học tập/lab được cố ý mở.
7. Cách khắc phục
    - Thiết lập quy trình hardening lặp lại được cho mọi môi trường và tự động hóa càng nhiều càng tốt.
    - Gỡ bỏ tính năng, service, sample app, tài khoản và framework không dùng.
    - Chuẩn hóa security headers, cấu hình error handling tập trung và review quyền cloud storage định kỳ.
    - Cập nhật cấu hình cùng vòng patch management; giữ dev/QA/prod đồng nhất về cấu trúc nhưng dùng credential khác nhau.
    - Dùng xác thực liên kết danh tính, short-lived credential hoặc role của nền tảng thay vì nhúng secret tĩnh trong code và pipeline.
## 3. A03:2025 - Software Supply Chain Failures
1. Vị trí và Tầm quan trọng
    - Xếp hạng: Đứng thứ 3 trong OWASP Top 10:2025 và là nhóm được cộng đồng xếp rất cao trong khảo sát.
    - Dữ liệu nền: Theo score table của OWASP, đây là nhóm có tỷ lệ xuất hiện trung bình cao nhất trong dữ liệu được báo cáo, dù số CVE liên quan trực tiếp không nhiều.
    - Phạm vi: Không chỉ còn là “dùng component có lỗ hổng đã biết” mà bao phủ toàn bộ chuỗi build, phân phối và cập nhật phần mềm.
2. Bản chất
    - Lỗi xảy ra khi tổ chức không kiểm soát tốt dependency, toolchain, artifact repository, IDE extension, CI/CD, image registry hoặc nguồn cung phần mềm khác.
    - Rủi ro đến từ component lỗi thời, không được duy trì, nguồn không tin cậy, thiếu SBOM, thiếu theo dõi dependency bắc cầu và thiếu kiểm soát thay đổi trong pipeline.
3. Kịch bản và Tác động
    - Dự án dùng thư viện hoặc framework cũ có lỗ hổng đã công bố nhưng không được cập nhật đúng hạn. Tác động là bị khai thác gián tiếp từ dependency.
    - Pipeline CI/CD hoặc kho artifact có quyền quá rộng, một cá nhân có thể đưa thay đổi từ code tới production mà không có giám sát. Tác động là cài mã độc hoặc backdoor vào bản phát hành.
    - Ứng dụng tải JS từ CDN hoặc package source không tin cậy. Tác động là mã phía client/server bị thay thế hoặc tiêm payload độc hại.
4. Cơ chế Zap phát hiện
    - Baseline scan không nhìn thấy toàn bộ supply chain backend, dependency bắc cầu hay SBOM nên độ phủ trực tiếp bị giới hạn.
    - ZAP có Retire.js add-on với passive rule `10003` để phát hiện JavaScript package lỗi thời hoặc có lỗ hổng đã biết.
    - Các rule `90003` Subresource Integrity Attribute Missing và `10115` Script Served From Malicious Domain (polyfill) giúp phát hiện rủi ro từ tài nguyên bên thứ ba ở frontend.
    - Kết luận A03 vẫn cần kết hợp thêm SCA/SBOM, kiểm kê dependency và review pipeline ngoài ZAP.
5. Cấu hình baseline
    - Với ứng dụng web có tải thư viện JS, nên giữ các rule sau ở mức nghiêm:
      - `10003 FAIL` cho Retire.js
      - `90003 WARN` hoặc `FAIL` cho thiếu SRI với tài nguyên bên ngoài
      - `10115 FAIL` cho script từ domain polyfill độc hại
      - `10036 INFO` và `10037 INFO` để ghi nhận lộ công nghệ có thể giúp fingerprint dependency
    - Không nên xem baseline là bằng chứng đủ để kết luận an toàn supply chain; nó chỉ là một lớp quan sát runtime phía trình duyệt.
6. Sàng lọc cảnh báo (Triage)
    - Xác minh thư viện bị nêu có thật sự được ứng dụng tải ở runtime hay chỉ còn trong code cũ/chưa dùng.
    - Với alert SRI, kiểm tra xem script đó có cùng origin hay không; SRI quan trọng nhất với tài nguyên từ CDN hoặc domain ngoài.
    - Với alert polyfill hoặc thư viện lỗi thời, đối chiếu phiên bản thực tế và mức ảnh hưởng trong luồng nghiệp vụ đang chạy.
    - Nếu ứng dụng backend không phục vụ JS ra trình duyệt, cần tránh hiểu nhầm rằng baseline đã bao phủ supply chain server-side.
7. Cách khắc phục
    - Duy trì SBOM tập trung, theo dõi cả dependency trực tiếp và dependency bắc cầu.
    - Chỉ lấy component từ nguồn chính thức, ưu tiên package có chữ ký và đường truyền an toàn.
    - Loại bỏ dependency không dùng, vá theo mức rủi ro và theo dõi tình trạng maintain của thư viện.
    - Tăng cường bảo mật CI/CD, repository, artifact store và phân tách nhiệm vụ trong phát hành.
    - Triển khai rollout theo giai đoạn hoặc canary để giảm bán kính ảnh hưởng nếu nhà cung cấp bị compromise.
## 4. A04:2025 - Cryptographic Failures
1. Vị trí và Tầm quan trọng
    - Xếp hạng: Đứng thứ 4 trong OWASP Top 10:2025.
    - Dữ liệu nền: 32 CWE được ánh xạ, tỷ lệ xuất hiện trung bình 3,80%.
    - Phạm vi: Nhóm này bao trùm việc không mã hóa khi cần, dùng thuật toán yếu, quản lý khóa kém, random yếu hoặc làm rò rỉ dữ liệu nhạy cảm do thiết kế mã hóa sai.
2. Bản chất
    - Lỗ hổng xuất hiện khi dữ liệu nhạy cảm không được bảo vệ đúng ở trạng thái truyền, lưu trữ hoặc xử lý.
    - Các lỗi hay gặp gồm dùng HTTP/SSL/TLS yếu, hash cũ như MD5/SHA1, thiếu HSTS, dùng PRNG yếu, IV lặp lại, khóa mặc định hoặc lưu khóa ngay trong repo.
3. Kịch bản và Tác động
    - Website không cưỡng bức TLS hoặc cho phép mã hóa yếu, attacker trên mạng có thể chặn traffic và chiếm session. Tác động là mất bí mật và toàn vẹn dữ liệu.
    - Database mật khẩu lưu bằng hash nhanh hoặc không salt, khi bị lộ attacker có thể crack hàng loạt. Tác động là chiếm tài khoản diện rộng.
    - Dữ liệu nhạy cảm được cache hoặc xuất hiện trên URL/referrer. Tác động là rò rỉ PII hoặc thông tin thanh toán qua log, proxy và browser history.
4. Cơ chế Zap phát hiện
    - Baseline/passive scan phát hiện tốt các dấu hiệu runtime như cookie thiếu `Secure`, mixed content, thiếu HSTS, form chuyển từ HTTPS sang HTTP và thông tin nhạy cảm trên URL/referrer.
    - Các rule hữu ích gồm `10011` Cookie Secure Flag, `10035` Strict Transport Security Header, `10040` Mixed Content, `10041/10042` chuyển tiếp form không an toàn, `10024/10025` lộ thông tin nhạy cảm trong URL hoặc Referrer.
    - ZAP không thể tự đánh giá đầy đủ thuật toán mã hóa lưu trữ, độ mạnh của key derivation hoặc HSM; phần đó cần review code/config và kiểm thử chuyên sâu hơn.
5. Cấu hình baseline
    - Nên đặt mức nghiêm với các rule phản ánh bảo vệ đường truyền:
      - `10011 FAIL`
      - `10035 FAIL`
      - `10040 FAIL`
      - `10041 FAIL`
      - `10042 FAIL`
      - `10024 WARN`
      - `10025 WARN`
    - Nếu có endpoint xử lý dữ liệu nhạy cảm, nên xuất báo cáo HTML/JSON để lưu evidence cho audit.
6. Sàng lọc cảnh báo (Triage)
    - Xác minh endpoint có thật sự xử lý dữ liệu nhạy cảm hay chỉ là nội dung công khai.
    - Với mixed content, kiểm tra tài nguyên HTTP đó có đang tải trong ngữ cảnh production hay chỉ còn trong tài liệu/demo.
    - Với HSTS hoặc cookie Secure, tách môi trường local/dev khỏi prod để tránh false positive do môi trường lab chưa bật HTTPS.
    - Với lộ thông tin trên URL/referrer, kiểm tra có phải dữ liệu thực như email, token, mã giao dịch hay chỉ là giá trị giả lập.
7. Cách khắc phục
    - Phân loại dữ liệu nhạy cảm và mã hóa dữ liệu khi truyền cũng như khi lưu trữ.
    - Chỉ dùng thuật toán, protocol và key hiện đại; quản lý khóa đúng cách, ưu tiên HSM hoặc dịch vụ quản lý khóa đáng tin cậy.
    - Cưỡng bức HTTPS, bật HSTS, bỏ giao thức/plaintext cũ và tắt mixed content.
    - Không lưu mật khẩu bằng mã hóa thuận nghịch; dùng hash thích nghi có salt như Argon2, scrypt hoặc PBKDF2-HMAC-SHA-512.
    - Hạn chế giữ dữ liệu nhạy cảm quá lâu, tắt cache cho response nhạy cảm và tránh đưa bí mật vào URL.
## 5. A05:2025 - Injection
1. Vị trí và Tầm quan trọng
    - Xếp hạng: Đứng thứ 5 trong OWASP Top 10:2025.
    - Dữ liệu nền: 100% ứng dụng được kiểm thử có ít nhất một dạng kiểm tra liên quan; nhóm này có 37 CWE, số CVE cao nhất trong toàn bộ Top 10.
    - Đặc điểm: Bao gồm cả XSS tần suất cao và SQL Injection tác động nặng, nên vừa phổ biến vừa nguy hiểm.
2. Bản chất
    - Lỗi injection xảy ra khi dữ liệu do user kiểm soát đi thẳng vào interpreter như SQL engine, shell, template engine, LDAP hoặc trình duyệt và bị thực thi như lệnh/cú pháp.
    - Nguồn gốc thường là không validate/filter input, dùng query động không tham số hóa, nối chuỗi trực tiếp hoặc escape theo cách không đúng ngữ cảnh.
3. Kịch bản và Tác động
    - Tham số `id` bị chèn payload SQL như `' OR '1'='1` làm truy vấn trả về toàn bộ bản ghi. Tác động là lộ hoặc phá hủy dữ liệu.
    - HQL/ORM query vẫn nối chuỗi với input, dẫn đến bypass bộ lọc và đọc dữ liệu ngoài quyền cho phép.
    - Ứng dụng nối input người dùng vào lệnh OS như `nslookup <domain>`. Tác động là thực thi lệnh tùy ý trên máy chủ.
    - Input được phản xạ hoặc lưu rồi render lại mà không encode đúng ngữ cảnh. Tác động là XSS, chiếm session hoặc thay đổi hành vi trình duyệt.
4. Cơ chế Zap phát hiện
    - Đây là nhóm mà active scan có giá trị lớn hơn baseline. ZAP có rule `40018` cho SQL Injection, `40012` Reflected XSS, `40014` Persistent XSS, `90037` Command Injection, `90035/90036` cho SSTI.
    - Passive scan vẫn hữu ích để tìm hotspot như `10031` User Controllable HTML Attribute, `10043` User Controllable Javascript Event, `10023` Debug Errors hoặc CSP yếu.
    - Fuzzing, authenticated scan và review request parameter là các kỹ thuật nên kết hợp khi nghi ngờ injection ở API hoặc luồng nhiều bước.
5. Cấu hình baseline
    - Baseline không “đánh” payload tấn công nên không đủ để khẳng định A05, nhưng có thể giữ các rule hotspot sau:
      - `10031 WARN`
      - `10043 WARN`
      - `10030 INFO`
      - `10023 WARN`
      - `10055 WARN`
    - Sau baseline, nên chạy active scan có kiểm soát phạm vi đối với endpoint nhập liệu, tìm kiếm, lọc dữ liệu, template và shell wrapper.
6. Sàng lọc cảnh báo (Triage)
    - Với XSS hotspot, kiểm tra dữ liệu có thật sự đi vào HTML/JS theo ngữ cảnh khai thác được hay chỉ xuất hiện ở dạng đã encode an toàn.
    - Với SQLi/command injection, xác nhận request mẫu, payload, sai khác response và khả năng tái hiện trước khi kết luận.
    - Phân biệt lỗi ở endpoint test/demo khỏi luồng thật trên production; nhiều false positive xuất hiện khi tham số chỉ được phản xạ đơn thuần.
    - Nếu ứng dụng dùng WAF hoặc generic error page, cần xem request/response gốc trong ZAP để tránh bỏ sót false negative hoặc hiểu nhầm kết quả.
7. Cách khắc phục
    - Tách dữ liệu khỏi lệnh bằng prepared statement, query parameterization hoặc API an toàn.
    - Validate input phía server theo allow-list; chỉ escape khi thật sự không thể tránh interpreter và phải escape đúng ngữ cảnh.
    - Không nối chuỗi vào SQL, shell, template, LDAP hoặc biểu thức động.
    - Encode output đúng ngữ cảnh HTML/attribute/JS/URL để chặn XSS.
    - Bổ sung SAST, DAST và fuzzing trong CI/CD cho các bề mặt nhập liệu chính.
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
- https://owasp.org/Top10/2025/A01_2025-Broken_Access_Control/
- https://owasp.org/Top10/2025/A02_2025-Security_Misconfiguration/
- https://owasp.org/Top10/2025/A03_2025-Software_Supply_Chain_Failures/
- https://owasp.org/Top10/2025/A04_2025-Cryptographic_Failures/
- https://owasp.org/Top10/2025/A05_2025-Injection/
