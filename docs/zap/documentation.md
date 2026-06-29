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
1. Vị trí và Tầm quan trọng
    - Xếp hạng: Giảm 2 bậc từ vị trí số 4 (2021) xuống số 6 trong OWASP Top 10:2025 (do A02 và A03 vượt lên).
    - Dữ liệu nền: Ngành công nghiệp đã có những bước tiến đáng kể về mô hình hóa mối đe dọa (threat modeling) và chú trọng hơn vào thiết kế an toàn. Các CWE nổi bật được ánh xạ bao gồm CWE-256 (Unprotected Storage of Credentials), CWE-269 (Improper Privilege Management), CWE-434 (Unrestricted Upload of File with Dangerous Type), CWE-501 (Trust Boundary Violation), và CWE-522 (Insufficiently Protected Credentials).
    - Định hướng: Nhấn mạnh sự cần thiết phải dịch chuyển vượt ra ngoài khái niệm "shift-left" trong giai đoạn lập trình (coding) để tiến tới các hoạt động trước khi viết code như khảo sát yêu cầu và thiết kế kiến trúc theo nguyên tắc Secure by Design.
2. Bản chất
    - Insecure Design là một danh mục rộng đại diện cho các điểm yếu mang tính "thiếu sót hoặc thiết kế biện pháp kiểm soát không hiệu quả" (missing or ineffective control design).
    - Phân biệt Rạch ròi: Có sự khác biệt cốt lõi giữa Thiết kế không an toàn (Insecure Design) và Triển khai không an toàn (Insecure Implementation). Một thiết kế an toàn vẫn có thể bị lỗi triển khai; nhưng một thiết kế không an toàn thì không thể khắc phục bằng một bản code hoàn hảo, do các biện pháp bảo mật cần thiết ban đầu đã không được thiết kế để phòng thủ trước các kịch bản tấn công.
    - Nguyên nhân gốc rễ: Thiếu việc lập hồ sơ rủi ro nghiệp vụ (business risk profiling) cho hệ thống, dẫn đến việc không xác định đúng mức độ thiết kế bảo mật cần thiết. Bao gồm 3 khía cạnh chính: Quản lý yêu cầu & tài nguyên, Thiết kế an toàn, và Vòng đời phát triển an toàn (SDLC).
3. Kịch bản và Tác động
    - Kịch bản 1 (Quy trình khôi phục danh tính): Luồng khôi phục tài khoản sử dụng "câu hỏi và câu trả lời bảo mật". Cơ chế này bị NIST 800-63b, OWASP ASVS cấm vì nhiều người có thể biết hoặc đoán được câu trả lời. Tác động: Chiếm đoạt tài khoản trái phép.
    - Kịch bản 2 (Lỗi logic nghiệp vụ trong đặt chỗ): Chuỗi rạp chiếu phim cho phép giảm giá đặt vé nhóm (tối đa 15 người mới cần đặt cọc). Kẻ tấn công lợi dụng lỗ hổng trong logic nghiệp vụ để đặt đồng loạt 600 ghế ở tất cả các rạp trong vài request mà không thanh toán. Tác động: Chiếm dụng tài nguyên, gây thất thoát doanh thu khổng lồ.
    - Kịch bản 3 (Thiếu kiểm soát luồng tự động/bot): Trang web thương mại điện tử không có cơ chế chống bot/scalper mua vét các sản phẩm giới hạn (như card đồ họa cao cấp) để bán lại. Tác động: Ảnh hưởng nghiêm trọng đến uy tín thương hiệu và làm mất niềm tin của khách hàng.
4. Cơ chế Zap phát hiện
    - Do bản chất của Insecure Design nằm ở khâu thiết kế kiến trúc và logic nghiệp vụ, các công cụ quét tự động như `zap-baseline.py` hay DAST thông thường không thể trực tiếp hiểu được luồng logic nghiệp vụ hoặc tự động đánh giá được toàn bộ kiến trúc hệ thống.
    - Tuy nhiên, ZAP có thể phát hiện các triệu chứng hoặc chỉ dấu gián tiếp của thiết kế kém thông qua các rule passive/active:
      - Thiếu kiểm soát luồng/chống tự động hóa: Phát hiện việc thiếu CSRF token, thiếu security headers hoặc kiểm tra giới hạn tần suất (rate limiting) thông qua Fuzzer / Active Scan.
      - Vi phạm ranh giới tin cậy (Trust boundary): Phát hiện việc lộ lọt thông tin nhạy cảm hoặc truyền tham số quản trị/quyền qua client-side (ví dụ: `10031` User Controllable HTML Attribute, `10027` Information Disclosure).
    - Để phát hiện hiệu quả A06, kiểm thử viên cần sử dụng ZAP như một công cụ hỗ trợ kiểm thử thủ công (Mô hình MitM Proxy Intercept) kết hợp Fuzzing để thử nghiệm các kịch bản thao tác sai logic nghiệp vụ hoặc vượt rào quy trình.
5. Cấu hình baseline
    - Mặc dù baseline scan tập trung vào cấu hình và passive scan, ta có thể thiết lập để rà soát các chỉ dấu bề mặt của thiết kế thiếu an toàn:
      - Đặt mức cảnh báo `WARN` hoặc `FAIL` cho các rule liên quan đến rò rỉ thông tin hoặc thiếu biện pháp bảo vệ luồng:
        - `100202 WARN` hoặc `FAIL` cho `CSRF Countermeasures` (chỉ dấu thiếu kiểm soát luồng thao tác)
        - `10027 INFO` hoặc `WARN` cho `Information Disclosure`
        - `10040 FAIL` cho `Mixed Content` và `10011 FAIL` cho `Cookie Secure Flag` (thiết kế luồng truyền tải thiếu đồng nhất)
    - Cần ghi nhận rõ trong quy trình CI/CD rằng baseline scan chỉ mang tính chất rà soát bề mặt, không thể thay thế cho Threat Modeling và kiểm thử logic nghiệp vụ chuyên sâu.
6. Sàng lọc cảnh báo (Triage)
    - Phân biệt rõ giữa cảnh báo về lỗi cấu hình thông thường (A02) và dấu hiệu của lỗ hổng thiết kế (A06). Ví dụ: Việc thiếu CSRF token trên một form tìm kiếm công khai là False Positive, nhưng trên form chuyển khoản hoặc đổi mật khẩu thì là lỗ hổng thiết kế/logic nghiêm trọng.
    - Đánh giá theo góc nhìn mô hình hóa mối đe dọa (Threat Modeling): Khi phân tích gói tin ZAP, kiểm tra xem API có đang tin tưởng mù quáng vào dữ liệu từ client (như giá tiền, số lượng, trạng thái thanh toán) mà không kiểm tra tính hợp lệ (plausibility check) ở backend hay không.
    - Đánh giá khả năng chống lạm dụng (abuse): Nếu endpoint không có cảnh báo lỗi tự động nhưng có thể bị gửi request hàng nghìn lần mà không bị chặn (thiếu rate limiting/bot protection), đó là lỗ hổng thiết kế thực sự.
7. Cách khắc phục
    - Thiết lập và duy trì Vòng đời phát triển phần mềm an toàn (Secure Development Lifecycle - SDLC) với sự tham gia của các chuyên gia AppSec ngay từ giai đoạn khảo sát yêu cầu và thiết kế kiến trúc.
    - Tích hợp mô hình hóa mối đe dọa (Threat Modeling) cho các thành phần quan trọng như xác thực, phân quyền, logic nghiệp vụ và các luồng dữ liệu then chốt.
    - Sử dụng thư viện các mẫu thiết kế an toàn (secure design patterns) hoặc các thành phần chuẩn hóa đã được kiểm chứng (paved-road components).
    - Bổ sung các biện pháp kiểm tra tính hợp lệ (plausibility checks) ở từng tầng (tier) của ứng dụng, từ frontend đến backend.
    - Phân lập các tầng hệ thống và mạng (segregate tier layers) tùy theo nhu cầu bảo vệ; phân tách rõ ràng dữ liệu giữa các tenant (tenant segregation) ngay trong thiết kế kiến trúc.
    - Đưa các yêu cầu bảo mật vào User Story; viết các bài kiểm thử unit và integration test dựa trên các use-case và misuse-case để kiểm chứng khả năng chống chịu của hệ thống trước các kịch bản tấn công.
## 7. A07:2025 - Authentication Failures
1. Vị trí và Tầm quan trọng
    - Xếp hạng: Giữ nguyên vị trí số 7 trong OWASP Top 10:2025 (tương tự bản 2021).
    - Tên gọi và Phạm vi: Có sự điều chỉnh nhẹ trong tên gọi (Authentication Failures thay vì Identification and Authentication Failures) để phản ánh chính xác hơn 36 CWE thuộc nhóm này.
    - Các CWE nổi bật: CWE-259 (Use of Hard-coded Password), CWE-297 (Improper Validation of Certificate with Host Mismatch), CWE-287 (Improper Authentication), CWE-384 (Session Fixation), và CWE-798 (Use of Hard-coded Credentials).
2. Bản chất
    - Lỗi xảy ra khi kẻ tấn công có thể đánh lừa hệ thống công nhận một user không hợp lệ hoặc sai danh tính thành user hợp lệ.
    - Các nguyên nhân và biểu hiện chính:
      - Cho phép tấn công tự động như credential stuffing (nhồi thông tin xác thực bị lộ) hoặc tấn công kết hợp/password spray (thử nghiệm các biến thể mật khẩu phổ biến như `Password1!`, `Password2!`).
      - Không có cơ chế chặn brute force hoặc các script tấn công tự động nhanh chóng.
      - Cho phép đặt hoặc giữ mật khẩu mặc định, yếu, hoặc dễ đoán (như `admin`/`admin`, `Password1`).
      - Cho phép đăng ký tài khoản mới với mật khẩu đã từng bị lộ lọt (breached credentials).
      - Quy trình khôi phục danh tính/quên mật khẩu yếu kém (ví dụ: dùng "câu hỏi bảo mật").
      - Mật khẩu lưu trữ dạng plaintext hoặc băm yếu (liên quan A04).
      - Thiếu xác thực đa yếu tố (MFA) hoặc cơ chế dự phòng (fallback) không an toàn khi MFA gặp sự cố.
      - Xử lý phiên (Session) kém: Lộ Session ID trên URL hoặc hidden field, tái sử dụng Session ID sau khi đăng nhập (Session Fixation), không hủy hoàn toàn session/SSO token khi logout hoặc hết hạn, không xác minh chính xác scope/audience của thông tin xác thực (như `aud`, `iss` trong JWT).
3. Kịch bản và Tác động
    - Kịch bản 1 (Credential stuffing & Password spray): Kẻ tấn công sử dụng danh sách tài khoản bị lộ lọt hoặc thử các chuỗi tăng tiến (ví dụ: đổi `Winter2025` thành `Winter2026`). Nếu ứng dụng thiếu cơ chế chặn tự động/bot, nó sẽ bị lợi dụng làm "bài kiểm tra mật khẩu" (password oracle) để dò danh tính hợp lệ. Tác động: Chiếm đoạt tài khoản hàng loạt.
    - Kịch bản 2 (Lạm dụng mật khẩu làm yếu tố xác thực duy nhất): Đòi hỏi đổi mật khẩu thường xuyên (password rotation) và độ phức tạp cao khiến user có xu hướng tái sử dụng hoặc chọn mật khẩu yếu theo quy luật. Tác động: Hệ thống bị tổn thương trước các cuộc tấn công dò mật khẩu; NIST 800-63 khuyến cáo dừng ép buộc đổi mật khẩu định kỳ và chuyển sang bắt buộc dùng MFA.
    - Kịch bản 3 (Quản lý phiên & Single Sign-On yếu kém): User sử dụng máy tính công cộng, thay vì chọn "logout", họ chỉ đóng tab trình duyệt. Hoặc hệ thống SSO không hỗ trợ Single Logout (SLO) (đăng xuất khỏi hệ thống hiện tại nhưng vẫn còn phiên ở ứng dụng mail, tài liệu). Khi người khác dùng tiếp trình duyệt hoặc máy tính đó, họ có thể truy cập tài khoản của nạn nhân. Tác động: Chiếm đoạt phiên làm việc trái phép.
4. Cơ chế Zap phát hiện
    - ZAP có thể hỗ trợ kiểm tra xác thực và quản lý phiên thông qua các cơ chế quét tự động và thủ công:
      - ZAP Passive Scan phát hiện các dấu hiệu quản lý phiên kém an toàn: Lộ Session ID trên URL (`Session ID in URL Rewrite`), Cookie thiếu cờ an toàn (`10011` Cookie No Secure Flag, `10010` Cookie No HttpOnly Flag, `10054` Cookie SameSite Attribute), hoặc thiếu tiêu đề bảo mật.
      - ZAP Active Scan & Fuzzing:
        - Fuzzing form đăng nhập với danh sách mật khẩu phổ biến để kiểm tra cơ chế chống Brute Force / Account Lockout.
        - ZAP Forced User / Authentication Add-on: Kiểm tra cơ chế xử lý phiên, cụ thể là kiểm tra lỗi Session Fixation (xác nhận xem Session ID có được làm mới sau khi đăng nhập thành công hay không).
      - Kiểm thử thủ công (MitM Proxy): Can thiệp và chỉnh sửa các token JWT (sửa claim `aud`, `iss`, `sub` hoặc hạ thuật toán `alg: none`) để kiểm tra backend có xác minh tính hợp lệ của token hay không.
5. Cấu hình baseline
    - Baseline Scan là công cụ giám sát cấu hình bảo mật phiên hiệu quả trong quy trình CI/CD:
      - Thiết lập mức `FAIL` đối với các rule quản lý Cookie và Session:
        - `10010 FAIL` cho `Cookie No HttpOnly Flag` (phòng chống trộm cookie qua XSS)
        - `10011 FAIL` cho `Cookie No Secure Flag` (bảo vệ cookie trên đường truyền HTTPS)
        - `10054 WARN` hoặc `FAIL` cho `Cookie SameSite Attribute` (giảm thiểu rủi ro CSRF)
        - `3 FAIL` cho `Session ID in URL Rewrite` (chặn rò rỉ Session ID qua URL/Referer)
    - Với kiểm tra Brute Force hay xác minh JWT, baseline scan không thực hiện tự động; cần tích hợp thêm ZAP Fuzzer hoặc kịch bản kiểm thử API chuyên biệt.
6. Sàng lọc cảnh báo (Triage)
    - Phân biệt cờ Cookie trên tài nguyên tĩnh/tracking với Cookie định danh: Nếu ZAP báo lỗi thiếu `HttpOnly`/`Secure` trên một cookie quảng cáo hoặc tùy chọn giao diện (UI preference), đó là False Positive. Nhưng nếu thiếu trên `JSESSIONID`, `PHPSESSID`, hoặc `access_token`, đó là lỗ hổng nghiêm trọng.
    - Xác minh cơ chế hết hạn phiên (Session Expiration): Kiểm tra xem việc logout hoặc hết hạn phiên chỉ đơn thuần là xóa token ở client-side (trình duyệt) hay backend thực sự đã thu hồi/đánh dấu vô hiệu hóa (revoke) token đó.
    - Kiểm tra cơ chế chống dò thông báo (Account Enumeration): Phân tích phản hồi từ API đăng nhập/khôi phục mật khẩu. Nếu API trả về thông báo khác nhau giữa "Tài khoản không tồn tại" và "Sai mật khẩu", đó là lỗ hổng cho phép dò quét danh sách tài khoản.
7. Cách khắc phục
    - Triển khai Xác thực đa yếu tố (MFA): Bắt buộc áp dụng MFA để ngăn chặn hiệu quả các cuộc tấn công credential stuffing, brute force và tái sử dụng thông tin xác thực.
    - Tuân thủ tiêu chuẩn mật khẩu hiện đại (NIST 800-63B): Bỏ yêu cầu đổi mật khẩu định kỳ (trừ khi nghi ngờ lộ lọt); kiểm tra và chặn đăng ký/đổi mật khẩu với danh sách mật khẩu yếu hoặc đã bị lộ (ví dụ: tích hợp API HaveIBeenPwned); khuyến khích sử dụng trình quản lý mật khẩu.
    - Chống dò quét danh tính & Cấu hình hạn chế truy cập: Chuẩn hóa thông báo trả về chung chung (ví dụ: "Tài khoản hoặc mật khẩu không chính xác"); triển khai cơ chế rate limiting, captcha hoặc account lockout sau nhiều lần đăng nhập thất bại; ghi log và cảnh báo quản trị viên khi phát hiện tấn công.
    - Quản lý phiên an toàn phía Server: Sử dụng trình quản lý phiên chuẩn của framework, tạo Session ID mới với độ ngẫu nhiên cao sau khi đăng nhập thành công. Lưu Session ID trong Cookie an toàn (`HttpOnly`, `Secure`, `SameSite`), tuyệt đối không để trên URL.
    - Huỷ phiên triệt để & Quản lý Single Sign-On (SLO): Huỷ hiệu lực phiên làm việc ở backend khi user logout, hết thời gian chờ (idle timeout) hoặc hết thời gian sống tuyệt đối (absolute timeout). Triển khai Single Logout cho các hệ thống SSO.
    - Xác minh chặt chẽ JWT/Token: Backend phải xác thực toàn bộ chữ ký, scope, cũng như các claim `aud` (audience) và `iss` (issuer) của token trước khi chấp nhận yêu cầu.
## 8. A08:2025 - Software or Data Integrity Failures
1. Vị trí và Tầm quan trọng
    - Xếp hạng: Giữ nguyên vị trí số 8 trong OWASP Top 10:2025 (tương tự bản 2021).
    - Tên gọi và Phạm vi: Đổi tên nhẹ từ "Software and Data Integrity Failures" thành "Software or Data Integrity Failures". Nhóm này tập trung vào sự thất bại trong việc bảo vệ ranh giới tin cậy (trust boundaries) và xác minh tính toàn vẹn của mã nguồn, phần mềm cũng như dữ liệu ở mức độ thấp hơn so với Software Supply Chain Failures (A03).
    - Các CWE nổi bật: CWE-829 (Inclusion of Functionality from Untrusted Control Sphere), CWE-915 (Improperly Controlled Modification of Dynamically-Determined Object Attributes), và CWE-502 (Deserialization of Untrusted Data).
2. Bản chất
    - Lỗi xảy ra khi mã nguồn và hạ tầng không bảo vệ hệ thống trước các đoạn mã hoặc dữ liệu không đáng tin cậy/không hợp lệ, dẫn đến việc xử lý chúng như dữ liệu hợp lệ và đáng tin cậy.
    - Các nguyên nhân và biểu hiện chính:
      - Phụ thuộc vào các plugin, thư viện hoặc module từ nguồn, kho lưu trữ hoặc CDN không tin cậy.
      - Pipeline CI/CD thiếu an toàn, kéo code hoặc artifact từ nơi không tin cậy và không kiểm tra chữ ký/tính hợp lệ trước khi triển khai, tạo cơ hội cho mã độc thâm nhập.
      - Chức năng tự động cập nhật (auto-update) tải xuống và áp dụng bản cập nhật mà không kiểm tra chữ ký/tính toàn vẹn.
      - Việc giải mã (decode) hoặc giải nén/giải tuần tự hóa (deserialize) dữ liệu cấu trúc trực tiếp từ user mà không xác minh tính hợp lệ (Insecure Deserialization).
3. Kịch bản và Tác động
    - Kịch bản 1 (Sử dụng tiện ích web từ nguồn ngoài): Công ty trỏ DNS `support.myCompany.com` sang nhà cung cấp bên thứ ba `myCompany.SupportProvider.com`. Hệ quả là mọi cookie xác thực thuộc `myCompany.com` đều bị gửi sang máy chủ bên ngoài, khiến attacker chiếm đoạt cơ sở hạ tầng bên thứ ba có thể trộm cookie và chiếm phiên của user.
    - Kịch bản 2 (Cập nhật firmware/phần mềm không ký số): Các thiết bị, router, hoặc phần mềm tải và chạy bản cập nhật firmware không ký số (unsigned firmware). Attacker chặn bắt đường truyền (MitM) và đẩy firmware độc hại vào thiết bị. Tác động: Chiếm quyền điều khiển thiết bị/hệ thống.
    - Kịch bản 3 (Insecure Deserialization): Ứng dụng React gọi Spring Boot microservice và truyền tải trạng thái user dạng serialized Java object (`rO0...` trong base64). Attacker chỉnh sửa gói dữ liệu và dùng công cụ quét lỗi để đạt quyền thực thi mã từ xa (RCE) trên máy chủ.
4. Cơ chế Zap phát hiện
    - ZAP Passive Scan phát hiện các dấu hiệu rủi ro liên quan đến ranh giới tin cậy và tải tài nguyên ngoài: ví dụ `90003` Subresource Integrity Attribute Missing (thiếu SRI trên thẻ script tải từ CDN), Cookie không phân định SameSite/Secure.
    - ZAP Active Scan & Fuzzing:
      - ZAP hỗ trợ các rule quét Insecure Deserialization và Mass Assignment (thông qua Active Scan bám sát các luồng dữ liệu JSON/XML hoặc custom serialized headers).
      - Sử dụng ZAP Fuzzer để sửa đổi thông tin trong các serialized token hoặc chèn các gadget payload phổ biến (ví dụ: Ysoserial) để quan sát phản hồi lỗi từ server.
    - Kiểm thử thủ công (MitM Proxy Intercept): Bắt các gói tin chứa cấu trúc dữ liệu nối tiếp, can thiệp thay đổi thuộc tính đối tượng (object attributes) để kiểm tra lỗi Mass Assignment (CWE-915) hoặc Deserialization.
5. Cấu hình baseline
    - Baseline Scan trong CI/CD giúp rà soát cấu hình tính toàn vẹn ở tầng frontend và giao tiếp mạng:
      - Đặt mức `FAIL` đối với rule kiểm tra SRI và tài nguyên ngoài:
        - `90003 WARN` hoặc `FAIL` cho `Subresource Integrity Attribute Missing` (bắt buộc kiểm tra tính toàn vẹn của thư viện JS/CSS từ CDN)
        - `10098 WARN` hoặc `FAIL` cho `Cross Domain Misconfiguration` (ngăn chặn chia sẻ dữ liệu hoặc thao tác từ nguồn ngoài sai chính sách)
    - Đối với rà soát quy trình CI/CD và giải tuần tự hóa an toàn, baseline scan không tự động hóa hoàn toàn; cần bổ sung các công cụ kiểm tra chữ ký và review kiến trúc.
6. Sàng lọc cảnh báo (Triage)
    - Kiểm tra thuộc tính SRI: Nếu tài nguyên được tải từ cùng một origin (chính máy chủ ứng dụng), việc thiếu SRI có thể là False Positive. Tuy nhiên, nếu tải từ CDN hoặc third-party domain, đây là rủi ro thực sự cần khắc phục.
    - Đối chiếu ranh giới phân quyền khi báo lỗi Mass Assignment: Kiểm tra xem các model/DTO ở backend có gán dữ liệu tự động từ request vào object database (binding) mà không có danh sách trắng (allow-list) hay không.
    - Xem xét luồng deserialization: Bất kỳ endpoint nào nhận stream/object nối tiếp từ client mà không yêu cầu mã hóa HMAC hoặc chữ ký số trước khi parse đều là lỗ hổng toàn vẹn dữ liệu.
7. Cách khắc phục
    - Kiểm tra chữ ký số: Dùng chữ ký số hoặc các cơ chế mã hóa HMAC tương đương để xác minh phần mềm, bản cập nhật hoặc dữ liệu đến từ nguồn hợp lệ và không bị chỉnh sửa.
    - Quản lý kho phụ thuộc tin cậy: Đảm bảo các công cụ như npm, Maven, Gradle chỉ kéo thư viện từ các kho chính thức; với hệ thống rủi ro cao, nên triển khai kho lưu trữ nội bộ (internal repository) đã qua kiểm duyệt.
    - Thiết lập quy trình review chặt chẽ: Áp dụng kiểm duyệt bắt buộc (code & configuration review) đối với mọi thay đổi trong pipeline phần mềm.
    - Bảo mật CI/CD Pipeline: Áp dụng phân lập quyền, quản lý cấu hình và kiểm soát truy cập nghiêm ngặt trong CI/CD để bảo đảm tính toàn vẹn của mã nguồn từ khâu build đến deploy.
    - Bảo vệ dữ liệu tuần tự hóa: Không tiếp nhận hoặc xử lý dữ liệu tuần tự hóa (serialized data) từ client mà không có kiểm tra tính toàn vẹn (integrity check) hoặc mã hóa để ngăn chặn giả mạo và tấn công phát lại (replay attack).
## 9. A09:2025 - Security Logging and Alerting Failures
1. Vị trí và Tầm quan trọng
    - Xếp hạng: Giữ nguyên vị trí số 9 trong OWASP Top 10:2025.
    - Tên gọi và Phạm vi: Được đổi tên từ "Security Logging and Monitoring Failures" thành "Security Logging and Alerting Failures" nhằm nhấn mạnh chức năng cảnh báo (alerting) để kích hoạt hành động ứng phó kịp thời từ các sự kiện log.
    - Đặc điểm: Đây là nhóm thường bị định giá thấp trong dữ liệu CVE (chỉ 723 CVE) và rất khó kiểm thử tự động, nhưng được cộng đồng bầu chọn cao vì ảnh hưởng cực lớn đến việc giám sát, cảnh báo sự cố và điều tra số (forensics). Các CWE tiêu biểu gồm CWE-117 (Improper Output Neutralization for Logs), CWE-532 (Insertion of Sensitive Information into Log File), và CWE-778 (Insufficient Logging).
2. Bản chất
    - Nếu không có log và giám sát, các cuộc tấn công và vi phạm không thể bị phát hiện; nếu không có cảnh báo (alerting), tổ chức không thể phản ứng nhanh chóng và hiệu quả trước sự cố bảo mật.
    - Các biểu hiện và thiếu sót phổ biến:
      - Bỏ sót hoặc ghi log không nhất quán các sự kiện quan trọng (như đăng nhập thành công/thất bại, giao dịch giá trị cao).
      - Lỗi và cảnh báo sinh ra thông báo log mơ hồ, thiếu chi tiết hoặc không ghi log.
      - Log không được bảo vệ vẹn toàn trước nguy cơ bị chỉnh sửa/xóa bỏ, hoặc chỉ lưu cục bộ mà không sao lưu độc lập.
      - Log không được theo dõi và thiếu ngưỡng cảnh báo (alerting thresholds) hoặc quy trình leo thang ứng phó sự cố.
      - Các đợt quét kiểm thử DAST (như ZAP, Burp Suite) không hề kích hoạt cảnh báo an ninh trên hệ thống.
      - Lộ lọt thông tin nhạy cảm (PII, PHI, thông tin hệ thống) vào file log hoặc hiển thị chi tiết log cho user/attacker.
      - Lỗ hổng tấn công tiêm mã vào hệ thống log (Log injection/Log4Shell) do không mã hóa/kiểm soát dữ liệu trước khi ghi log.
      - Quá nhiều cảnh báo giả (false positives) khiến đội ngũ SOC quá tải và bỏ qua cảnh báo quan trọng.
3. Kịch bản và Tác động
    - Kịch bản 1 (Thiếu log dẫn đến rò rỉ kéo dài): Website bảo hiểm sức khỏe trẻ em bị tấn công và sửa đổi dữ liệu nhạy cảm của hơn 3,5 triệu trẻ em. Do hoàn toàn không có cơ chế log và giám sát, vụ vi phạm diễn ra ngầm trong hơn 7 năm mà không hề bị phát hiện cho đến khi có bên thứ ba thông báo.
    - Kịch bản 2 (Rò rỉ phía nhà cung cấp cloud): Một hãng hàng không lớn bị trộm 10 năm dữ liệu hành khách (hộ chiếu, thẻ tín dụng) lưu trên cloud bên thứ ba; sự chậm trễ trong giám sát và cảnh báo khiến vụ việc kéo dài trước khi được phát hiện.
    - Kịch bản 3 (Tấn công ứng dụng thanh toán): Attacker khai thác lỗ hổng thanh toán thu thập hơn 400.000 dữ liệu thẻ. Cơ chế giám sát kém dẫn đến không kịp ngắt kết nối, hậu quả là doanh nghiệp bị phạt 20 triệu bảng theo chuẩn GDPR.
4. Cơ chế Zap phát hiện
    - ZAP Passive Scan giúp phát hiện chỉ dấu lộ thông tin nhạy cảm: Các rule `10023` Debug Error Information Disclosure, `10027` Information Disclosure có thể báo hiệu ứng dụng đang để lộ thông tin debug/log ra ngoài response.
    - Kiểm chứng khả năng kích hoạt cảnh báo (DAST Alert Test):
      - Cách kiểm tra thực tế nhất là thực hiện Active Scan hoặc Fuzzing cường độ cao bằng ZAP vào ứng dụng. Nếu sau đợt quét dữ dội của ZAP mà hệ thống SIEM/SOC/Firewall của tổ chức không hề sinh ra cảnh báo (alert) hoặc khóa IP, điều đó chứng tỏ ứng dụng mắc lỗi A09 nghiêm trọng.
    - Kiểm tra Log Injection: Sử dụng ZAP Fuzzer gửi các chuỗi payload đặc thù (chứa ký tự newline `\r\n` hoặc cú pháp macro/lookup như `${jndi:...}`) vào các trường input thường được log (như `User-Agent`, `username`, `X-Forwarded-For`) để kiểm tra hệ thống log có bị bẻ gãy hoặc chèn dòng giả mạo hay không.
5. Cấu hình baseline
    - Baseline Scan tập trung vào việc ngăn chặn rò rỉ thông tin lỗi/debug trên bề mặt ứng dụng:
      - Thiết lập mức `WARN` hoặc `FAIL` cho các rule:
        - `10023 WARN` cho `Debug Error Information Disclosure` (ngăn chặn in thông tin log nhạy cảm ra client)
        - `90022 WARN` cho `Application Errors` (cảnh báo xử lý lỗi kém sinh ra thông tin nhạy cảm)
    - Trong CI/CD, nên bổ sung kịch bản kiểm tra tự động: gửi các luồng DAST độc hại mẫu và xác minh hệ thống SIEM có nhận được log/alert tương ứng hay không.
6. Sàng lọc cảnh báo (Triage)
    - Đối chiếu thông tin rò rỉ: Khi ZAP báo lỗi rò rỉ thông tin, kiểm tra xem đó là thông tin nghiệp vụ thông thường hay là thông tin nhạy cảm (session, key, PII) thực sự bị đẩy nhầm ra log/response.
    - Đánh giá ngưỡng cảnh báo (Threshold Triage): Nếu hệ thống có sinh log nhưng sinh hàng nghìn log vô nghĩa cho một lỗi lặp lại mà không gom cụm (aggregation), hoặc cảnh báo không được phân loại đúng mức nghiêm trọng, đó là thiếu sót về kiến trúc alerting.
    - Đánh giá tính sẵn sàng của SOC: Kiểm tra xem các luồng cảnh báo có playbook xử lý tương ứng hay không. Nếu có cảnh báo nhưng không ai nhận hoặc không biết xử lý, hệ thống vẫn mang lỗi A09.
7. Cách khắc phục
    - Ghi log đầy đủ và chuẩn hóa: Ghi log mọi thao tác đăng nhập, phân quyền, các giao dịch và kiểm tra xác thực thất bại kèm ngữ cảnh rõ ràng (người dùng, IP, thời gian) với thời gian lưu trữ đủ lâu để phục vụ điều tra số.
    - Tránh rò rỉ và tiêm mã log: Mã hóa hoặc kiểm soát chặt chẽ dữ liệu trước khi ghi log để phòng chống Log Injection; tuyệt đối không ghi log các thôngế thông tin nhạy cảm (mật khẩu dạng plaintext, số thẻ tín dụng, PII).
    - Đồng bộ định dạng log: Sử dụng các định dạng chuẩn (như JSON) để các hệ thống quản lý log (ELK Stack, Splunk, SIEM) dễ dàng thu thập và phân tích.
    - Bảo vệ tính toàn vẹn của Log: Implement cơ chế bảo vệ log (như bảng database chỉ cho phép ghi tiếp/append-only, hoặc đẩy log ngay sang máy chủ lưu trữ độc lập).
    - Xây dựng quy trình giám sát & Alerting hiệu quả: Thiết lập các use-case và ngưỡng cảnh báo (alerting thresholds) hợp lý kèm Playbook để đội ngũ SOC xử lý tức thời; tích hợp các công cụ Observability hiện đại.
    - Triển khai Honeytoken & Phân tích hành vi: Bẫy kẻ tấn công bằng các "honeytoken" (tài khoản, bảng dữ liệu, mồi giả). Vì user thật không bao giờ chạm vào mồi này, bất kỳ tương tác nào diễn ra cũng sẽ tạo cảnh báo với tỷ lệ false positive gần như bằng 0.
## 10. A10:2025 - Mishandling of Exceptional Conditions
1. Vị trí và Tầm quan trọng
    - Xếp hạng: Là danh mục hoàn toàn mới xuất hiện ở vị trí số 10 trong OWASP Top 10:2025.
    - Tên gọi và Phạm vi: Thay thế các mảng trôi nổi trước đây về chất lượng code, nhóm này chứa 24 CWE và tập trung vào việc xử lý lỗi sai quy cách (improper error handling), lỗi logic, mở rộng lối đi khi gặp sự cố (failing open), và các sai sót khi hệ thống đối mặt với điều kiện bất thường.
    - Các CWE nổi bật: CWE-209 (Generation of Error Message Containing Sensitive Information), CWE-234 (Failure to Handle Missing Parameter), CWE-274 (Improper Handling of Insufficient Privileges), CWE-476 (NULL Pointer Dereference), và CWE-636 (Not Failing Securely / 'Failing Open').
2. Bản chất
    - Lỗi xử lý các điều kiện bất thường xảy ra khi phần mềm không phòng ngừa, phát hiện và phản ứng đúng cách trước các tình huống bất ngờ hoặc không dự đoán trước, dẫn đến sập nguồn (crash), hành vi sai lệch và tạo ra lỗ hổng.
    - Các khía cạnh thất bại chính: (1) Ứng dụng không ngăn chặn tình huống bất thường xảy ra; (2) Không nhận diện được tình huống khi nó đang diễn ra; (3) Bỏ mặc hoặc phản ứng kém sau khi tình huống xảy ra.
    - Nguyên nhân cốt lõi: Thiếu kiểm tra dữ liệu đầu vào (input validation), bắt exception chung chung ở tầng trên cùng thay vì xử lý ngay tại hàm xảy ra lỗi, bỏ sót exception (uncaught exceptions), hoặc khi gặp lỗi hệ thống không thu hồi quyền/giao dịch mà lại cho phép tiếp tục thao tác (Failing Open thay vì Failing Closed).
3. Kịch bản và Tác động
    - Kịch bản 1 (Cạn kiệt tài nguyên - DoS): Ứng dụng bắt exception khi upload file thất bại nhưng không giải phóng tài nguyên (file handle, bộ nhớ) sau đó. Cứ mỗi lần phát sinh exception, tài nguyên tiếp tục bị khóa cho đến khi sập toàn bộ dịch vụ.
    - Kịch bản 2 (Lộ lọt thông tin nhạy cảm qua thông báo lỗi): Khi truy vấn database gặp điều kiện dị biệt, hệ thống in toàn bộ câu lệnh SQL và stack trace ra ngoài. Attacker cố tình đưa tham số dị dạng để ép hệ thống nhả lỗi, dùng thông tin đó làm trinh sát (reconnaissance) để tấn công SQL Injection chính xác.
    - Kịch bản 3 (Hỏng trạng thái giao dịch tài chính): Giao dịch chuyển tiền gồm 3 bước: trừ tiền người gửi, cộng tiền người nhận, ghi log. Khi mạng gián đoạn ở bước 2, nếu hệ thống không roll back toàn bộ giao dịch (fail closed), attacker có thể vắt kiệt tiền tài khoản hoặc khai thác race condition để nhận tiền nhiều lần.
4. Cơ chế Zap phát hiện
    - ZAP Passive Scan phát hiện mạnh mẽ các hệ quả bề mặt của xử lý lỗi kém: `10023` Debug Error Information Disclosure, `90022` Application Errors (phát hiện server trả về HTTP 500 kèm stack trace hoặc chuỗi lỗi cụ thể).
    - ZAP Active Scan & Fuzzing:
      - ZAP Fuzzer là vũ khí tối thượng để phát hiện A10: Quét chèn các tham số dị biệt (giá trị null, bỏ sót tham số, số âm, ký tự đặc biệt, chuỗi cực dài) vào các API/endpoint để ép hệ thống rơi vào trạng thái ngoại lệ (Exceptional Conditions).
      - Đánh giá phản hồi Fuzzing: Quan sát xem ứng dụng phản hồi bằng HTTP 500 (lộ stack trace), bị crash (kết nối timeout/từ chối dịch vụ), hay rơi vào trạng thái Fail Open (ví dụ: mất tham số xác thực nhưng server vẫn cho đi tiếp).
5. Cấu hình baseline
    - Baseline Scan theo dõi chặt chẽ các hành vi rò rỉ thông tin qua thông báo lỗi:
      - Đặt mức cảnh báo nghiêm `WARN` hoặc `FAIL` cho các rule phát hiện xử lý lỗi kém:
        - `90022 WARN` hoặc `FAIL` cho `Application Errors` (kiểm tra rò rỉ thông báo lỗi ứng dụng)
        - `10023 WARN` hoặc `FAIL` cho `Debug Error Information Disclosure` (phát hiện lộ thông tin debug)
        - `10055 INFO` hoặc `WARN` (rà soát bề mặt cấu hình an toàn)
    - Để đánh giá toàn diện A10 trong CI/CD, nên kết hợp ZAP Baseline với các test case Fuzzing chuyên biệt kiểm tra sức chịu đựng và cơ chế rollback.
6. Sàng lọc cảnh báo (Triage)
    - Đánh giá thông báo lỗi phản hồi: Phân biệt rõ giữa việc server trả về mã HTTP 400/500 kèm thông điệp thân thiện ("Đã xảy ra lỗi, vui lòng thử lại") với việc trả về stack trace chứa mã nguồn/tên database. Trường hợp đầu là xử lý đúng, trường hợp sau là lỗ hổng A10.
    - Phân tích cơ chế Rollback: Khi phát hiện một API trả về lỗi giữa chừng, kiểm tra xem dữ liệu trong database có bị ghi nhận dở dang (dirty state) hay không. Nếu có, đây là lỗ hổng nghiêm trọng về toàn vẹn giao dịch.
    - Đánh giá cơ chế Fail Securely: Kiểm tra các luồng kiểm tra quyền/xác thực. Nếu hệ thống không thể kết nối tới dịch vụ xác thực (SSO/Redis) mà lại cho phép bypass qua cổng (Failing Open), đó là lỗi A10 nguy hiểm nhất.
7. Cách khắc phục
    - Thiết lập nguyên tắc Fail Securely (Failing Closed): Khi xảy ra ngoại lệ hoặc sự cố trong bất kỳ giao dịch nào, hệ thống phải tự động đóng luồng truy cập, khôi phục (roll back) toàn bộ trạng thái dữ liệu về điểm bắt đầu.
    - Xử lý Exception triệt để tại chỗ: Bắt và xử lý mọi ngoại lệ (try-catch) ngay tại vị trí hàm/module xảy ra sự cố; thực hiện hành động khắc phục cụ thể, giải phóng tài nguyên (finally block) và thông báo lỗi thân thiện cho user.
    - Xây dựng Global Exception Handler: Thiết lập trình xử lý ngoại lệ toàn cục ở tầng cao nhất của ứng dụng để đảm bảo không có exception nào bị bỏ sót (uncaught exception) gây sập hệ thống hoặc lộ stack trace.
    - Áp dụng giới hạn tài nguyên (Rate Limiting & Quotas): Không có tài nguyên nào trong IT là vô hạn. Cấu hình rate limiting, throttling và giới hạn dung lượng/bộ nhớ để ngăn chặn nghẽn tải, tấn công DoS và cạn kiệt tài nguyên.
    - Validate dữ liệu nghiêm ngặt & Gom cụm Log lỗi: Kiểm tra tính hợp lệ của mọi dữ liệu đầu vào. Với các lỗi lặp lại liên tục do bạo lực mạng (brute force/bot), hệ thống nên gộp cụm thông kê thay vì sinh log ngập lụt (tránh gây lỗi A09). Đảm bảo toàn bộ tổ chức tuân thủ chung một chuẩn xử lý ngoại lệ.

## 11. Reference

- https://www.cloudflare.com/learning/security/threats/owasp-top-10/
- https://owasp.org/Top10/2025/
- https://owasp.org/Top10/2025/A01_2025-Broken_Access_Control/
- https://owasp.org/Top10/2025/A02_2025-Security_Misconfiguration/
- https://owasp.org/Top10/2025/A03_2025-Software_Supply_Chain_Failures/
- https://owasp.org/Top10/2025/A04_2025-Cryptographic_Failures/
- https://owasp.org/Top10/2025/A05_2025-Injection/
- https://owasp.org/Top10/2025/A06_2025-Insecure_Design/
- https://owasp.org/Top10/2025/A07_2025-Authentication_Failures/
- https://owasp.org/Top10/2025/A08_2025-Software_or_Data_Integrity_Failures/
- https://owasp.org/Top10/2025/A09_2025-Security_Logging_and_Alerting_Failures/
- https://owasp.org/Top10/2025/A10_2025-Mishandling_of_Exceptional_Conditions/