Dưới đây là kết quả triage cho finding SEMGREP-007:

---

## Triage Finding Bảo Mật: SEMGREP-007

**Mã finding:** SEMGREP-007
**Rule ID:** `typescript.react.security.react-insecure-request.react-insecure-request`
**File nguồn:** `eshop-sut/frontend-mobile/App.js`
**Dòng:** 244
**Severity:** ERROR
**CWE:** CWE-319: Cleartext Transmission of Sensitive Information
**OWASP:** A03:2017 - Sensitive Data Exposure, A02:2021 - Cryptographic Failures, A04:2025 - Cryptographic Failures
**Likelihood:** LOW
**Impact:** MEDIUM
**Confidence:** MEDIUM
**Cảnh báo Semgrep:** Unencrypted request over HTTP detected.

---

### 1. Phân loại: Needs Human Review

### 2. Lý do phân loại dựa trên source evidence.

Bằng chứng mã nguồn tại dòng 244 cho thấy một yêu cầu `fetch` được gửi đến `API_URL` với endpoint `/forgot-password`. Semgrep đã phát hiện rằng yêu cầu này có thể đang được gửi qua giao thức HTTP không được mã hóa, dựa trên việc không có dấu hiệu rõ ràng của việc sử dụng HTTPS hoặc các cơ chế mã hóa khác tại thời điểm gửi request. Rule `react-insecure-request` được thiết kế để cảnh báo về các yêu cầu HTTP không an toàn, đặc biệt là khi có khả năng lộ lọt thông tin nhạy cảm.

Tuy nhiên, điều quan trọng là `API_URL` là một biến môi trường hoặc hằng số được định nghĩa ở nơi khác. Bối cảnh "EShop đang được quét như ứng dụng lab local; finding liên quan localhost cần kiểm tra môi trường trước khi kết luận rủi ro cuối." là yếu tố then chốt cho việc phân loại này. Nếu `API_URL` được cấu hình trỏ đến `localhost` hoặc một URL nội bộ chỉ sử dụng trong môi trường development hoặc lab, việc sử dụng HTTP có thể chấp nhận được và không gây ra rủi ro bảo mật thực tế cho người dùng cuối. Ngược lại, nếu `API_URL` có thể được cấu hình để trỏ đến một endpoint public hoặc trong môi trường production mà không sử dụng HTTPS, đây sẽ là một lỗ hổng nghiêm trọng.

Do Semgrep là SAST và không có khả năng kiểm tra cấu hình `API_URL` hoặc ngữ cảnh triển khai cụ thể (như đã nêu trong ghi chú "chưa rõ config, deploy usage..."), chúng ta chưa thể đưa ra kết luận cuối cùng về việc đây là *True Positive* hay *False Positive* chỉ dựa trên mã nguồn tĩnh.

### 3. Tác động thực tế trong bối cảnh EShop.

Trong bối cảnh một ứng dụng EShop, chức năng "Quên mật khẩu" thường liên quan đến việc xử lý địa chỉ email của người dùng, một loại thông tin cá nhân có thể được coi là nhạy cảm (đặc biệt khi kết hợp với các dữ liệu khác). Nếu URL `API_URL` thực sự trỏ đến một máy chủ không sử dụng HTTPS, thông tin email được gửi đi có thể bị chặn và đọc bởi kẻ tấn công trong mạng (ví dụ: tấn công man-in-the-middle).

Tuy nhiên, vì đây là ứng dụng lab local, tác động thực tế *tại thời điểm này* có thể là **thấp**, chủ yếu dừng lại ở việc minh họa một sai lầm trong cấu hình hoặc thiết kế có thể dẫn đến rủi ro nếu được triển khai sai trong môi trường production. Nếu tiến trình forgot-password được thực hiện trên một mạng không tin cậy và không được mã hóa, Impact có thể **trung bình** vì lộ lọt email có thể dẫn đến các cuộc tấn công giả mạo hoặc phishing sau này.

### 4. Cách khắc phục cụ thể.

1.  **Ưu tiên Hàng đầu (Nếu `API_URL` dẫn đến endpoint public/production):**
    *   **Đảm bảo sử dụng HTTPS:** Cập nhật cấu hình `API_URL` để luôn sử dụng `https://` thay vì `http://`. Điều này yêu cầu máy chủ API phải được cấu hình để hỗ trợ TLS/SSL.
    *   **Kiểm tra cấu hình `API_URL`:** Xác minh cách `API_URL` được định nghĩa và truyền vào ứng dụng. Nếu nó là một biến môi trường, hãy đảm bảo biến môi trường đó được thiết lập đúng với giao thức HTTPS trong mọi môi trường, đặc biệt là production.
    *   **Cập nhật mã nguồn:** Thay đổi dòng 244 (và bất kỳ nơi nào khác sử dụng `API_URL` cho các yêu cầu không mã hóa) để đảm bảo giao thức là HTTPS. Ví dụ: `const response = await fetch(`https://${API_URL}/forgot-password`...` hoặc tốt hơn là cấu hình `API_URL` bao gồm cả giao thức.

2.  **Nếu `API_URL` chỉ dành cho môi trường Local/Dev/Lab:**
    *   **Giữ nguyên như hiện tại nhưng ghi chú rõ ràng:** Document hóa rõ ràng rằng việc sử dụng HTTP tại đây là có chủ ý cho môi trường lab và không nên được sử dụng cho production.
    *   **Cân nhắc sử dụng các công cụ proxy hoặc debugger mật mã:** Trong môi trường lab, đôi khi người ta cố tình sử dụng HTTP để dễ dàng theo dõi lưu lượng. Tuy nhiên, cần lưu ý về rủi ro tiềm ẩn.

### 5. Ghi chú cần tester kiểm tra thêm nếu chưa đủ context.

*   **Xác định giá trị thực tế của `API_URL`:** Phỏng vấn hoặc kiểm tra file cấu hình/biến môi trường để biết `API_URL` đang trỏ đến đâu trong môi trường quét hiện tại.
    *   Nếu là `http://localhost:...` hoặc một địa chỉ IP nội bộ
    *   Nếu là một tên miền public hoặc có thể truy cập qua Internet.
*   **Kiểm tra mục đích của mã nguồn:** File `App.js` là file runtime chính của ứng dụng. Do đó, các dòng code ở đây có khả năng cao được thực thi trong quá trình sử dụng ứng dụng.
*   **Môi trường triển khai:** Tuy nhiên, do ngữ cảnh "ứng dụng lab local", cần làm rõ xem "lab" có bao gồm cả việc mô phỏng môi trường production hay chỉ là một môi trường phát triển đơn giản.
*   **Kiểm tra các API calls khác:** Xem xét liệu có các yêu cầu HTTP không mã hóa khác trong ứng dụng hay không, đặc biệt là những yêu cầu có thể gửi thông tin nhạy cảm hơn.