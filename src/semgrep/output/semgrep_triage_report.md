# Báo cáo Semgrep AI Triage

## Tổng quan

- Tổng số finding trong input: 12
- Script đọc toàn bộ mảng `results` từ JSON Semgrep, không hardcode số lượng finding.
- Phân loại của AI là hỗ trợ triage; kết luận cuối cùng vẫn cần tester kiểm chứng.

## Bảng tổng hợp findings

| # | Quy tắc | Tệp | Dòng | Mức độ | CWE | OWASP | Kết quả AI | Trạng thái kiểm chứng |
|---|---|---|---:|---|---|---|---|---|
| 1 | `javascript.jsonwebtoken.security.jwt-hardcode.hardcoded-jwt-secret` | `eshop-sut/backend/server.js` | 51 | WARNING | CWE-798: Use of Hard-coded Credentials | A07:2021 - Identification and Authentication Failures, A07:2025 - Authentication Failures | `findings/001_javascript-jsonwebtoken-security-jwt-hardcode-hardcoded-jwt-secret_ai_output.md` | Cần người kiểm chứng |
| 2 | `javascript.jsonwebtoken.security.jwt-hardcode.hardcoded-jwt-secret` | `eshop-sut/backend/server.js` | 105 | WARNING | CWE-798: Use of Hard-coded Credentials | A07:2021 - Identification and Authentication Failures, A07:2025 - Authentication Failures | `findings/002_javascript-jsonwebtoken-security-jwt-hardcode-hardcoded-jwt-secret_ai_output.md` | Cần người kiểm chứng |
| 3 | `javascript.jsonwebtoken.security.jwt-hardcode.hardcoded-jwt-secret` | `eshop-sut/backend/test_profile.js` | 4 | WARNING | CWE-798: Use of Hard-coded Credentials | A07:2021 - Identification and Authentication Failures, A07:2025 - Authentication Failures | `findings/003_javascript-jsonwebtoken-security-jwt-hardcode-hardcoded-jwt-secret_ai_output.md` | Cần người kiểm chứng |
| 4 | `typescript.react.security.react-insecure-request.react-insecure-request` | `eshop-sut/frontend-mobile/App.js` | 174 | ERROR | CWE-319: Cleartext Transmission of Sensitive Information | A03:2017 - Sensitive Data Exposure, A02:2021 - Cryptographic Failures, A04:2025 - Cryptographic Failures | `findings/004_typescript-react-security-react-insecure-request-react-insecure-request_ai_output.md` | Cần người kiểm chứng |
| 5 | `typescript.react.security.react-insecure-request.react-insecure-request` | `eshop-sut/frontend-mobile/App.js` | 189 | ERROR | CWE-319: Cleartext Transmission of Sensitive Information | A03:2017 - Sensitive Data Exposure, A02:2021 - Cryptographic Failures, A04:2025 - Cryptographic Failures | `findings/005_typescript-react-security-react-insecure-request-react-insecure-request_ai_output.md` | Cần người kiểm chứng |
| 6 | `typescript.react.security.react-insecure-request.react-insecure-request` | `eshop-sut/frontend-mobile/App.js` | 222 | ERROR | CWE-319: Cleartext Transmission of Sensitive Information | A03:2017 - Sensitive Data Exposure, A02:2021 - Cryptographic Failures, A04:2025 - Cryptographic Failures | `findings/006_typescript-react-security-react-insecure-request-react-insecure-request_ai_output.md` | Cần người kiểm chứng |
| 7 | `typescript.react.security.react-insecure-request.react-insecure-request` | `eshop-sut/frontend-mobile/App.js` | 244 | ERROR | CWE-319: Cleartext Transmission of Sensitive Information | A03:2017 - Sensitive Data Exposure, A02:2021 - Cryptographic Failures, A04:2025 - Cryptographic Failures | `findings/007_typescript-react-security-react-insecure-request-react-insecure-request_ai_output.md` | Cần người kiểm chứng |
| 8 | `typescript.react.security.react-insecure-request.react-insecure-request` | `eshop-sut/frontend-mobile/App.js` | 272 | ERROR | CWE-319: Cleartext Transmission of Sensitive Information | A03:2017 - Sensitive Data Exposure, A02:2021 - Cryptographic Failures, A04:2025 - Cryptographic Failures | `findings/008_typescript-react-security-react-insecure-request-react-insecure-request_ai_output.md` | Cần người kiểm chứng |
| 9 | `typescript.react.security.react-insecure-request.react-insecure-request` | `eshop-sut/frontend-mobile/App.js` | 296 | ERROR | CWE-319: Cleartext Transmission of Sensitive Information | A03:2017 - Sensitive Data Exposure, A02:2021 - Cryptographic Failures, A04:2025 - Cryptographic Failures | `findings/009_typescript-react-security-react-insecure-request-react-insecure-request_ai_output.md` | Cần người kiểm chứng |
| 10 | `typescript.react.security.react-insecure-request.react-insecure-request` | `eshop-sut/frontend-mobile/App.js` | 362 | ERROR | CWE-319: Cleartext Transmission of Sensitive Information | A03:2017 - Sensitive Data Exposure, A02:2021 - Cryptographic Failures, A04:2025 - Cryptographic Failures | `findings/010_typescript-react-security-react-insecure-request-react-insecure-request_ai_output.md` | Cần người kiểm chứng |
| 11 | `typescript.react.security.react-insecure-request.react-insecure-request` | `eshop-sut/frontend-mobile/App.js` | 384 | ERROR | CWE-319: Cleartext Transmission of Sensitive Information | A03:2017 - Sensitive Data Exposure, A02:2021 - Cryptographic Failures, A04:2025 - Cryptographic Failures | `findings/011_typescript-react-security-react-insecure-request-react-insecure-request_ai_output.md` | Cần người kiểm chứng |
| 12 | `typescript.react.security.react-insecure-request.react-insecure-request` | `eshop-sut/frontend-mobile/App.js` | 400 | ERROR | CWE-319: Cleartext Transmission of Sensitive Information | A03:2017 - Sensitive Data Exposure, A02:2021 - Cryptographic Failures, A04:2025 - Cryptographic Failures | `findings/012_typescript-react-security-react-insecure-request-react-insecure-request_ai_output.md` | Cần người kiểm chứng |

## Chi tiết từng finding

### SEMGREP-001: javascript.jsonwebtoken.security.jwt-hardcode.hardcoded-jwt-secret

#### Tags lỗi
| Thuộc tính | Giá trị |
|---|---|
| Rule ID | `javascript.jsonwebtoken.security.jwt-hardcode.hardcoded-jwt-secret` |
| Severity | `WARNING` |
| CWE | CWE-798: Use of Hard-coded Credentials |
| OWASP | A07:2021 - Identification and Authentication Failures, A07:2025 - Authentication Failures |
| Likelihood | `HIGH` |
| Impact | `MEDIUM` |
| Confidence | `HIGH` |

#### Thông tin finding
- File: `eshop-sut/backend/server.js`
- Dòng: 51
- Trạng thái kiểm chứng: Needs Human Review

#### Bằng chứng mã nguồn
```text
   46:     if (user.password === password) {
   47:       db.run(
   48:         "UPDATE users SET login_attempts = 0, locked_until = NULL WHERE id = ?",
   49:         [user.id],
   50:       );
=> 51:       const token = jwt.sign({ id: user.id, role: user.role }, SECRET_KEY);
   52:       res.json({ message: "Login successful", token, user });
   53:     } else {
   54:       const newAttempts = user.login_attempts + 2;
   55:       let lockedUntil = null;
   56:       if (newAttempts >= 3) {
```

#### Phân tích AI
Tuyệt vời! Tôi sẵn sàng đóng vai trò chuyên gia bảo mật ứng dụng để triage finding này từ Semgrep. Dưới đây là phân tích chi tiết:

---

##### Triage Finding: SEMGREP-001

##### 1. Phân loại: True Positive

##### 2. Lý do phân loại dựa trên source evidence:

Finding này được phân loại là **True Positive** dựa trên các lý do sau:

*   **Rule ID và Mô tả:** The rule `javascript.jsonwebtoken.security.jwt-hardcode.hardcoded-jwt-secret` được thiết kế chính xác để phát hiện việc hardcode các thông tin nhạy cảm như bí mật dùng để ký JWT. Mô tả của Semgrep cũng cảnh báo rõ ràng: "A hard-coded credential was detected. It is not recommended to store credentials in source-code... It is recommended to use environment variables... or retrieve credentials from a secure vault".
*   **Source Code Context:** Tại dòng 51 của file `eshop-sut/backend/server.js`, chúng ta thấy dòng mã `const token = jwt.sign({ id: user.id, role: user.role }, SECRET_KEY);`. Biến `SECRET_KEY` rõ ràng được khai báo và sử dụng trực tiếp trong mã nguồn để ký (sign) token JWT.
*   **CWE và OWASP:** Việc hardcode `SECRET_KEY` trực tiếp vào mã nguồn là một lỗ hổng bảo mật nghiêm trọng, trùng khớp với CWE-798 (Use of Hard-coded Credentials) và các hạng mục của OWASP A07:2021/A07:2025 (Authentication Failures).
*   **Vai trò của File:** File `eshop-sut/backend/server.js` là một phần của "entrypoint runtime backend", nghĩa là nó được thực thi trong quá trình hoạt động của ứng dụng. Do đó, việc hardcode bí mật này có thể bị lộ khi mã nguồn bị truy cập trái phép.
*   **Likelihood và Confidence:** Semgrep đưa ra `Likelihood: HIGH` và `Confidence: HIGH`, cho thấy công cụ có độ tin cậy cao rằng đây là một vấn đề bảo mật thực tế và có khả năng xảy ra cao.

##### 3. Tác động thực tế trong bối cảnh EShop:

Nếu `SECRET_KEY` bị lộ, kẻ tấn công có thể:

*   **Tạo token giả mạo:** Kẻ tấn công có thể tạo ra các token JWT giả mạo với các vai trò và ID người dùng tùy ý, cho phép họ "đăng nhập" vào hệ thống với quyền mà họ không mong muốn.
*   **Thao túng dữ liệu:** Với khả năng tạo token giả mạo, kẻ tấn công có thể thay đổi thông tin người dùng, thực hiện các giao dịch gian lận hoặc truy cập các tài nguyên nhạy cảm.
*   **Tiếm quyền kiểm soát:** Trong trường hợp xấu nhất, kẻ tấn công có thể chiếm quyền kiểm soát tài khoản quản trị, dẫn đến việc toàn bộ hệ thống bị ảnh hưởng.

Mặc dù EShop đang được quét như ứng dụng lab local và việc tìm thấy lỗ hổng trên `localhost` có thể không phản ánh nguy cơ trực tiếp trong môi trường production, tuy nhiên, **nếu ứng dụng này được deploy lên production (dù là production của môi trường lab hoặc môi trường thật), thì toàn bộ dữ liệu và tính bảo mật của EShop sẽ gặp rủi ro nghiêm trọng**. Việc hardcode bí mật là một nguyên tắc bảo mật cơ bản cần phải tuân thủ chặt chẽ trong mọi môi trường.

##### 4. Cách khắc phục cụ thể:

Để khắc phục lỗ hổng này, chúng ta cần loại bỏ việc hardcode `SECRET_KEY` và quản lý nó một cách an toàn:

1.  **Sử dụng Biến Môi Trường (Environment Variables):**
    *   Thay thế dòng 51 bằng cách đọc `SECRET_KEY` từ biến môi trường:
        ```javascript
        const SECRET_KEY = process.env.JWT_SECRET;
        // ...
        const token = jwt.sign({ id: user.id, role: user.role }, SECRET_KEY);
        ```
    *   Đảm bảo rằng biến môi trường `JWT_SECRET` được thiết lập trong môi trường chạy ứng dụng (ví dụ: trong file `.env` hoặc cấu hình của nền tảng deploy).

2.  **Sử dụng Hệ Thống Quản Lý Bí Mật (Secret Management System):**
    *   Nếu có thể, tích hợp với các dịch vụ quản lý bí mật như HashiCorp Vault, AWS Secrets Manager, Azure Key Vault, GitLab CI/CD Variables, GitHub Secrets, v.v. để lưu trữ và truy xuất `SECRET_KEY` một cách an toàn.

3.  **Đảm bảo Tính Ngẫu Nhiên và Độ Dài của Bí Mật:**
    *   Khi cấu hình bí mật mới (dù là qua biến môi trường hay hệ thống quản lý), hãy đảm bảo nó là một chuỗi ngẫu nhiên, dài và phức tạp để tăng cường khả năng chống lại các cuộc tấn công đoán mật khẩu hoặc brute-force.

##### 5. Ghi chú cần tester kiểm tra thêm nếu chưa đủ context:

*   **Môi trường Deploy của EShop:** Mặc dù là "ứng dụng lab local", hãy xác nhận rõ ràng EShop có được deploy lên bất kỳ môi trường nào khác ngoài localhost hay không. Nếu có, khả năng bị khai thác là rất cao.
*   **Mục đích của `SECRET_KEY`:** Xác nhận `SECRET_KEY` này chỉ dùng để ký/xác minh token JWT của *chính EShop* hay nó còn được sử dụng ở đâu khác hoặc có liên quan đến các ứng dụng/hệ thống khác.
*   **Quy trình CI/CD:** Nếu EShop có quy trình CI/CD tự động, hãy kiểm tra xem việc quản lý bí mật trong pipeline có được áp dụng hay chưa. Việc hardcode ở đây có thể là lỗi còn sót lại từ thời kỳ đầu phát triển hoặc do thiếu sự tích hợp chặt chẽ với quy trình deploy an toàn.

---

### SEMGREP-002: javascript.jsonwebtoken.security.jwt-hardcode.hardcoded-jwt-secret

#### Tags lỗi
| Thuộc tính | Giá trị |
|---|---|
| Rule ID | `javascript.jsonwebtoken.security.jwt-hardcode.hardcoded-jwt-secret` |
| Severity | `WARNING` |
| CWE | CWE-798: Use of Hard-coded Credentials |
| OWASP | A07:2021 - Identification and Authentication Failures, A07:2025 - Authentication Failures |
| Likelihood | `HIGH` |
| Impact | `MEDIUM` |
| Confidence | `HIGH` |

#### Thông tin finding
- File: `eshop-sut/backend/server.js`
- Dòng: 105
- Trạng thái kiểm chứng: Needs Human Review

#### Bằng chứng mã nguồn
```text
   100: const authenticateToken = (req, res, next) => {
   101:   const authHeader = req.headers["authorization"];
   102:   const token = authHeader && authHeader.split(" ")[1];
   103:   if (token == null) return res.status(401).json({ error: "Unauthorized" });
   104: 
=> 105:   jwt.verify(token, SECRET_KEY, (err, user) => {
   106:     if (err) return res.status(403).json({ error: "Forbidden" });
   107:     req.user = user;
   108:     next();
   109:   });
   110: };
```

#### Phân tích AI
Tuyệt vời, chúng ta hãy cùng nhau phân tích finding này một cách chi tiết. Dưới đây là bản triage theo vai trò chuyên gia bảo mật ứng dụng:

---

##### Phân tích Finding Bảo mật (SEMGREP-002)

**1. Phân loại:** Needs Human Review

**2. Lý do phân loại dựa trên source evidence:**

*   **Bằng chứng mã nguồn:** Dòng 105 trong file `eshop-sut/backend/server.js` cho thấy một biến cấu hình `SECRET_KEY` đang được sử dụng trực tiếp trong hàm `jwt.verify`. Semgrep rule `javascript.jsonwebtoken.security.jwt-hardcode.hardcoded-jwt-secret` đã phát hiện ra điều này và đưa ra cảnh báo.
*   **Chủ đề CWE/OWASP:** Vi phạm CWE-798 (Sử dụng thông tin đăng nhập bị mã hóa cứng) và thuộc nhóm OWASP A07 (Lỗi nhận dạng và xác thực). Điều này cho thấy đây là một vấn đề bảo mật tiềm ẩn nghiêm trọng.
*   **Ngữ cảnh ứng dụng:** Ứng dụng EShop đang được quét trong bối cảnh "ứng dụng lab local". Tuy nhiên, file `server.js` được mô tả là "entrypoint runtime backend", cho thấy nó đóng vai trò quan trọng trong hoạt động của backend.
*   **Sự không chắc chắn về ngữ cảnh deploy/runtime:** Mặc dù `SECRET_KEY` được mã hóa cứng trong code, việc phân loại **True Positive** hoặc **False Positive** phụ thuộc vào cách thức `SECRET_KEY` này được sử dụng và môi trường triển khai thực tế.
    *   Nếu `SECRET_KEY` này **chỉ dùng cho các token nội bộ, không quan trọng, hoặc chỉ phục vụ cho môi trường dev/lab được cô lập hoàn toàn** và sẽ không bao giờ được deploy ra môi trường production, thì nó có thể được xem là **False Positive** hoặc ít nhất là rủi ro thấp.
    *   Tuy nhiên, nếu `SECRET_KEY` này **được sử dụng để ký/xác minh các token thực sự của ứng dụng** (ngay cả trong môi trường lab) và có khả năng bị lộ ra ngoài (ví dụ: nếu mã nguồn lab bị rò rỉ công khai), thì đây là một **True Positive** với rủi ro cao.
*   **Thiếu thông tin về cấu hình và cách sử dụng:** Chúng ta chưa biết `SECRET_KEY` này được định nghĩa ở đâu. Nó có thể là một biến toàn cục được định nghĩa ở đầu file, hoặc được import từ một file cấu hình khác (lúc này, việc tìm kiếm nguyên nhân gốc có thể sâu hơn).

Do đó, để kết luận chính xác, cần có thêm thông tin về môi trường triển khai và cách thức biến `SECRET_KEY` được quản lý.

**3. Tác động thực tế trong bối cảnh EShop:**

Trong bối cảnh EShop, việc lưu trữ `SECRET_KEY` (được sử dụng để ký hoặc xác minh JWT) trực tiếp trong mã nguồn có thể dẫn đến các vấn đề bảo mật nghiêm trọng:

*   **Chiếm đoạt quyền truy cập:** Nếu kẻ tấn công có thể truy cập mã nguồn (dù là phiên bản lab), chúng có thể trích xuất `SECRET_KEY`. Với khóa bí mật này, kẻ tấn công có thể giả mạo hoặc sửa đổi các token JWT, từ đó thực hiện các hành động trái phép như:
    *   Đăng nhập với vai trò người dùng khác (kể cả quản trị viên).
    *   Truy cập vào các tài nguyên nhạy cảm.
    *   Thực hiện các giao dịch giả mạo.
*   **Rò rỉ thông tin nhạy cảm:** Nếu token được ký chứa thông tin nhạy cảm của người dùng, việc lộ khóa bí mật sẽ dẫn đến rò rỉ các thông tin này.

Ngay cả khi EShop đang ở giai đoạn lab, việc phát hiện lỗi này cũng rất quan trọng vì nó thiết lập một tiền lệ xấu và có nguy cơ cao bị vô tình đưa vào môi trường production.

**4. Cách khắc phục cụ thể:**

Để khắc phục lỗ hổng này một cách an toàn, chúng ta cần loại bỏ `SECRET_KEY` khỏi mã nguồn và sử dụng các phương pháp quản lý bí mật an toàn hơn:

*   **Sử dụng biến môi trường (Environment Variables):** Đây là cách phổ biến và được khuyến nghị rộng rãi.
    *   **Trong mã nguồn:** Thay thế `SECRET_KEY` bằng một biến nhận giá trị từ biến môi trường, ví dụ: `process.env.JWT_SECRET`.
        ```javascript
        // Thay vì: const SECRET_KEY = "your_super_secret_key_here";
        const SECRET_KEY = process.env.JWT_SECRET; 
        
        // Dòng 105:
        jwt.verify(token, SECRET_KEY, (err, user) => { ... });
        ```
    *   **Trong cấu hình triển khai:** Định nghĩa biến môi trường `JWT_SECRET` với một chuỗi ngẫu nhiên và mạnh mẽ trên server hoặc trong file cấu hình của hệ thống container/orchestration (Docker, Kubernetes).
*   **Sử dụng dịch vụ quản lý bí mật (Secrets Management Services):** Đối với các ứng dụng nghiêm ngặt hơn, có thể tích hợp với các dịch vụ như HashiCorp Vault, AWS Secrets Manager, Azure Key Vault. Các dịch vụ này cung cấp API để lấy bí mật một cách an toàn trong thời gian chạy.
*   **Sử dụng HSM (Hardware Security Module):** Đối với các yêu cầu bảo mật cao nhất, khóa bí mật có thể được lưu trữ trong HSM, một thiết bị phần cứng chuyên dụng để quản lý khóa.

**Giải pháp ưu tiên cho môi trường lab/dev:** Sử dụng biến môi trường là cách nhanh chóng và hiệu quả.

**5. Ghi chú cần tester kiểm tra thêm nếu chưa đủ context:**

*   **Xác định nguồn gốc của `SECRET_KEY`:** Biến này được định nghĩa ở đâu? Nó có được import từ một file cấu hình riêng không? Nếu là import, cần kiểm tra file cấu hình đó có bị lộ hoặc được quản lý an toàn không.
*   **Mục đích sử dụng của `SECRET_KEY`:** `SECRET_KEY` này có phải là khóa thực sự dùng để ký/xác minh JWT cho các API của EShop hay chỉ là một khóa thử nghiệm/dummy cho mục đích demo lab mà không có giá trị thực tế?
*   **Môi trường triển khai dự kiến:** Mặc dù đây là lab, có kế hoạch triển khai EShop này ra môi trường staging hoặc production không? Nếu có, việc fix hoàn toàn là bắt buộc.
*   **Phạm vi của token JWT:** Các token JWT được tạo và xác minh bằng `SECRET_KEY` này có chứa thông tin nhạy cảm hoặc có quyền truy cập vào các chức năng quan trọng của hệ thống không?

Việc làm rõ các điểm trên sẽ giúp xác định xem đây là **True Positive** (cần sửa ngay và coi như lỗ hổng nghiêm trọng) hay **False Positive** (có thể hạ mức ưu tiên hoặc bỏ qua nếu đảm bảo hoàn toàn không bị ảnh hưởng trong production). Tuy nhiên, với nguyên tắc phòng ngừa, **luôn ưu tiên coi nó là một vấn đề cần giải quyết**.

### SEMGREP-003: javascript.jsonwebtoken.security.jwt-hardcode.hardcoded-jwt-secret

#### Tags lỗi
| Thuộc tính | Giá trị |
|---|---|
| Rule ID | `javascript.jsonwebtoken.security.jwt-hardcode.hardcoded-jwt-secret` |
| Severity | `WARNING` |
| CWE | CWE-798: Use of Hard-coded Credentials |
| OWASP | A07:2021 - Identification and Authentication Failures, A07:2025 - Authentication Failures |
| Likelihood | `HIGH` |
| Impact | `MEDIUM` |
| Confidence | `HIGH` |

#### Thông tin finding
- File: `eshop-sut/backend/test_profile.js`
- Dòng: 4
- Trạng thái kiểm chứng: Needs Human Review

#### Bằng chứng mã nguồn
```text
   1: const axios = require('axios');
   2: const jwt = require('jsonwebtoken');
   3: 
=> 4: const token = jwt.sign({ id: 2, role: 'user' }, 'super_secret_key_that_should_not_be_here');
   5: console.log("Token:", token);
   6: axios.get('http://localhost:3000/api/users/me', { headers: { Authorization: 'Bearer ' + token }})
   7: .then(res => console.log("Profile ok:", res.data))
   8: .catch(err => console.log("Lỗi:", err.message));
```

#### Phân tích AI
Tuyệt vời! Hãy cùng tôi phân tích finding này với vai trò là chuyên gia bảo mật ứng dụng.

##### Triage Finding SEMGREP-003

##### 1. Phân loại: False Positive

##### 2. Lý do phân loại dựa trên source evidence:

Finding này chỉ ra một hard-coded JWT secret (`'super_secret_key_that_should_not_be_here'`) trong file `eshop-sut/backend/test_profile.js` tại dòng 4. Tuy nhiên, vai trò của file này theo ngữ cảnh được cung cấp là "mã test/helper".

Quan sát đoạn mã nguồn:
```javascript
const token = jwt.sign({ id: 2, role: 'user' }, 'super_secret_key_that_should_not_be_here');
console.log("Token:", token);
axios.get('http://localhost:3000/api/users/me', { headers: { Authorization: 'Bearer ' + token }})
```
Đoạn mã này rõ ràng đang tạo ra một token JWT với một secret được mã hóa cứng và sau đó sử dụng token này để gọi một API endpoint `http://localhost:3000/api/users/me`. Việc gọi một API trên `localhost` thường chỉ diễn ra trong môi trường phát triển cục bộ (local development) hoặc các kịch bản kiểm thử (testing scenarios) nội bộ.

Với bản chất của Semgrep là một công cụ SAST, nó phân tích mã tĩnh. Trong trường hợp này, việc hard-code secret trong một file test/helper không đại diện cho một lỗ hổng bảo mật **thực tế** trong môi trường production của ứng dụng EShop, trừ khi file này **bị deploy chung với mã nguồn production** hoặc được **runtime code tương tác trực tiếp và sử dụng secret này cho mục đích xác minh token thật của ứng dụng**. Dựa vào thông tin "Vai trò file: mã test/helper", ta có thể suy luận rằng nó không nằm trong luồng xử lý production.

Rule ID `javascript.jsonwebtoken.security.jwt-hardcode.hardcoded-jwt-secret` và CWE `CWE-798` là chính xác cho việc phát hiện secret mã hóa cứng. Tuy nhiên, **reachability** và **ngữ cảnh sử dụng** là yếu tố then chốt để phân loại. Trong trường hợp này, việc sử dụng secret là trong một kịch bản test/lab trên `localhost`, không ảnh hưởng đến bảo mật của API production.

##### 3. Tác động thực tế trong bối cảnh EShop:

Trong bối cảnh của EShop là một ứng dụng **lab local**, việc tìm thấy secret này trong file `test_profile.js` không tạo ra rủi ro bảo mật **ngay lập tức** hoặc **thực tế** cho ứng dụng đó ngoài môi trường lab. Nếu file này được deploy như một phần của ứng dụng production, tác động sẽ là **MEDIUM** (như Semgrep đã đánh giá), vì kẻ tấn công có thể lợi dụng secret này để giả mạo token và truy cập trái phép vào hệ thống. Tuy nhiên, với thông tin vai trò file là "test/helper", chúng ta giả định nó không bị deploy production.

##### 4. Cách khắc phục cụ thể:

Mặc dù đây là **False Positive** trong ngữ cảnh lab, nhưng quy tắc chung về việc không hard-code credentials là đúng đắn. Nếu cần phải gỡ bỏ cảnh báo này một cách triệt để (ví dụ, nếu có quy định tuân thủ chặt chẽ), và nếu **chắc chắn** file này chỉ dùng cho mục đích test:

1.  **Xóa hoặc Comment out mã nguồn:** Đối với file chỉ dùng cho test, cách đơn giản nhất là xóa hoàn toàn phần mã tạo token hoặc comment nó lại nếu phần đó có thể cần thiết cho các test sau này.
2.  **Sử dụng biến môi trường (cho các trường hợp cần thiết):** Nếu trong một kịch bản test phức tạp hơn mà cần một secret, hãy cấu hình nó qua biến môi trường hoặc một file config riêng biệt chỉ dùng cho môi trường dev/test.
3.  **Refactor mã test:** Tạo một hàm hoặc service riêng để sinh token trong môi trường test, và cấu hình secret này ở một nơi an toàn hơn (ví dụ: trong CI/CD pipeline cho các test tự động).

##### 5. Ghi chú cần tester kiểm tra thêm nếu chưa đủ context:

*   **Môi trường deploy của EShop:** Cần xác nhận EShop này là ứng dụng lab chạy cục bộ hay là một phần của quy trình build/deploy nghiêm ngặt hơn (ví dụ: CI/CD pipeline có thể đẩy mã này lên, dù là chỉ cho môi trường staging/test).
*   **Sử dụng thực tế của file `test_profile.js`:** Tuy được mô tả là "test/helper", cần xác nhận chắc chắn rằng file này **không bao giờ** được chạy trong môi trường production hoặc bất kỳ môi trường nào tương tự production sau khi build.
*   **Root cause của các finding khác:** Tìm hiểu xem có các finding tương tự (liên quan đến secret hard-coded hoặc JWT) trong các file khác hoặc các phần khác của ứng dụng EShop không. Nếu có, cần xem xét lại toàn bộ chiến lược quản lý secrets.
*   **Mục đích sinh token trên localhost:** Kiểm tra mục đích chính xác của việc gọi `http://localhost:3000/api/users/me` từ file test này. Nó là để kiểm tra chức năng API nội bộ trong quá trình phát triển hay là một phần của smoke test? Điều này giúp củng cố thêm lý do phân loại là False Positive trong bối cảnh lab.

### SEMGREP-004: typescript.react.security.react-insecure-request.react-insecure-request

#### Tags lỗi
| Thuộc tính | Giá trị |
|---|---|
| Rule ID | `typescript.react.security.react-insecure-request.react-insecure-request` |
| Severity | `ERROR` |
| CWE | CWE-319: Cleartext Transmission of Sensitive Information |
| OWASP | A03:2017 - Sensitive Data Exposure, A02:2021 - Cryptographic Failures, A04:2025 - Cryptographic Failures |
| Likelihood | `LOW` |
| Impact | `MEDIUM` |
| Confidence | `MEDIUM` |

#### Thông tin finding
- File: `eshop-sut/frontend-mobile/App.js`
- Dòng: 174
- Trạng thái kiểm chứng: Needs Human Review

#### Bằng chứng mã nguồn
```text
   169:   };
   170: 
   171:   const fetchOrders = async (currentToken = token) => {
   172:     if (!currentToken) return;
   173:     try {
=> 174:       const response = await fetch(`${API_URL}/orders/my-orders`, {
   175:         headers: { Authorization: `Bearer ${currentToken}` },
   176:       });
   177:       const data = await response.json();
   178:       const parsedOrders = Array.isArray(data) ? data : data.orders || [];
   179:       setOrders(parsedOrders);
```

#### Phân tích AI
Tuyệt vời! Tôi sẽ đóng vai trò chuyên gia bảo mật ứng dụng để triage finding SEMGREP-004 này.

---

##### Triage Finding: SEMGREP-004

1.  **Phân loại:** `Needs Human Review`

2.  **Lý do phân loại dựa trên source evidence:**
    *   **Phân tích source evidence:** Đoạn mã tại dòng 174 trong file `App.js` sử dụng hàm `fetch` để gửi yêu cầu đến `${API_URL}/orders/my-orders`. Header `Authorization: Bearer ${currentToken}` được đính kèm, cho thấy việc truyền token xác thực.
    *   **Phân tích rule Semgrep:** Rule `typescript.react.security.react-insecure-request.react-insecure-request` phát hiện các yêu cầu không mã hóa qua HTTP.
    *   **Đối chiếu và nhận định:** Rule này đúng là đã phát hiện một yêu cầu được thực hiện qua HTTP (chưa rõ là HTTP hay HTTPS). Tuy nhiên, việc xác định rõ ràng đây là lỗ hổng bảo mật thực tế hay không phụ thuộc nhiều vào cách `API_URL` được định nghĩa và môi trường triển khai.
    *   **Ngữ cảnh bổ sung:**
        *   `API_URL` có thể được định cấu hình để trỏ đến `http://localhost:xxxx` trong môi trường phát triển hoặc lab, nơi kết nối thường không yêu cầu mã hóa và dữ liệu nhạy cảm ở mức độ thấp cho mục đích thử nghiệm.
        *   Nếu `API_URL` trong môi trường production thực sự trỏ đến một URL HTTP thay vì HTTPS, thì đây là **True Positive**.
        *   Tuy nhiên, nếu `API_URL` được cấu hình để sử dụng HTTPS trong production, hoặc việc yêu cầu này chỉ diễn ra trong môi trường dev/lab mà không ảnh hưởng đến production, thì đây có thể là **False Positive** đối với môi trường production.
        *   Độ nhạy cảm của thông tin được truyền đi (token xác thực) là **Medium**, và khả năng bị khai thác **Low**, nhưng nếu lỗ hổng tồn tại thì tác động sẽ đáng kể.
    *   Vì vậy, dựa trên thông tin hiện có, chúng ta chưa thể kết luận chắc chắn đây là True Positive hay False Positive mà cần thêm thông tin về cấu hình `API_URL` và môi trường triển khai thực tế.

3.  **Tác động thực tế trong bối cảnh EShop:**
    *   Nếu `API_URL` trỏ đến một máy chủ qua giao thức HTTP không mã hóa trong môi trường Production:
        *   Token xác thực của người dùng (`currentToken`) có thể bị kẻ tấn công nghe lén trên đường truyền mạng (Man-in-the-Middle attack).
        *   Kẻ tấn công có thể sử dụng token bị đánh cắp để mạo danh người dùng, truy cập trái phép vào thông tin đơn hàng của họ, gây ra **Sensitive Data Exposure** và ảnh hưởng đến sự tin cậy của ứng dụng.
    *   Nếu `API_URL` chỉ là `localhost` trong môi trường Lab/Dev:
        *   Tác động thực tế là rất thấp, vì lưu lượng mạng thường chỉ diễn ra trong cùng một máy và không có kẻ tấn công bên ngoài có thể can thiệp. Tuy nhiên, đây vẫn là một "bad practice" về mặt bảo mật cần khắc phục trước khi đưa ra Production.

4.  **Cách khắc phục cụ thể:**
    *   **Ưu tiên hàng đầu:** Đảm bảo rằng tất cả các kết nối đến API đều sử dụng giao thức HTTPS, ngay cả trong môi trường phát triển nếu có thể.
    *   **Cập nhật cấu hình `API_URL`:** Xác minh và cập nhật biến `API_URL` trong các file cấu hình môi trường (`.env`, `config.js`, v.v.) để luôn trỏ đến một URL sử dụng HTTPS, ví dụ: `https://api.yourdomain.com`.
    *   **Cấu hình SSL/TLS cho Server:** Đảm bảo máy chủ API được cấu hình đúng với chứng chỉ SSL/TLS hợp lệ và luôn phục vụ các yêu cầu qua HTTPS.
    *   **Theo dõi việc sử dụng `fetch`:** Kiểm tra các lần gọi `fetch` khác trong ứng dụng để đảm bảo tương tự các yêu cầu đều được gửi qua HTTPS.

5.  **Ghi chú cần tester kiểm tra thêm nếu chưa đủ context:**
    *   Kiểm tra giá trị và cách định nghĩa của biến `API_URL` trong các file cấu hình khác nhau (ví dụ: `.env`, `config.js`) và đối chiếu với môi trường triển khai (Development, Staging, Production).
    *   Xác nhận liệu ứng dụng có được deploy với cấu hình `localhost` hay một tên miền thực tế.
    *   Kiểm tra xem máy chủ backend có sẵn sàng phục vụ các yêu cầu qua HTTPS hay không.
    *   Nếu có thể, hãy xem xét toàn bộ các URL mà `fetch` hoặc thư viện HTTP khác sử dụng trong ứng dụng để phát hiện các điểm không nhất quán.

---

### SEMGREP-005: typescript.react.security.react-insecure-request.react-insecure-request

#### Tags lỗi
| Thuộc tính | Giá trị |
|---|---|
| Rule ID | `typescript.react.security.react-insecure-request.react-insecure-request` |
| Severity | `ERROR` |
| CWE | CWE-319: Cleartext Transmission of Sensitive Information |
| OWASP | A03:2017 - Sensitive Data Exposure, A02:2021 - Cryptographic Failures, A04:2025 - Cryptographic Failures |
| Likelihood | `LOW` |
| Impact | `MEDIUM` |
| Confidence | `MEDIUM` |

#### Thông tin finding
- File: `eshop-sut/frontend-mobile/App.js`
- Dòng: 189
- Trạng thái kiểm chứng: Needs Human Review

#### Bằng chứng mã nguồn
```text
   184:   };
   185: 
   186:   const handleLogin = async () => {
   187:     setLoginError("");
   188:     try {
=> 189:       const response = await fetch(`${API_URL}/login`, {
   190:         method: "POST",
   191:         headers: { "Content-Type": "application/json" },
   192:         body: JSON.stringify({ email, password }),
   193:       });
   194:       const data = await response.json();
```

#### Phân tích AI
Tuyệt vời! Với vai trò là chuyên gia bảo mật ứng dụng, tôi sẽ tiến hành triage finding SEMGREP-005 này dựa trên thông tin bạn cung cấp.

##### Triage Finding SEMGREP-005

##### 1. Phân loại: Needs Human Review

##### 2. Lý do phân loại dựa trên source evidence.

Finding SEMGREP-005 chỉ ra rằng có một request được gửi đi qua giao thức HTTP (không mã hóa) tới endpoint `/login` trên `API_URL`. Dựa trên bằng chứng mã nguồn, dòng 189 trong file `eshop-sut/frontend-mobile/App.js` cho thấy việc sử dụng `fetch` để gửi thông tin đăng nhập (email, password) đến `API_URL`.

Tuy nhiên, việc phân loại mức độ rủi ro của việc sử dụng HTTP thay vì HTTPS phụ thuộc **hoàn toàn vào giá trị của biến `API_URL` và ngữ cảnh triển khai thực tế của ứng dụng EShop**.

*   Nếu `API_URL` trỏ đến một địa chỉ `localhost` hoặc một IP private trong môi trường phát triển/testing cục bộ, request này có thể không gây ra rủi ro bảo mật nghiêm trọng vì lưu lượng mạng được giới hạn trong một môi trường kiểm soát được.
*   Ngược lại, nếu `API_URL` trỏ đến một endpoint công cộng hoặc có thể truy cập được từ bên ngoài mạng nội bộ, việc gửi thông tin nhạy cảm (email và password) qua HTTP là **rất nguy hiểm**, tiềm ẩn nguy cơ bị kẻ tấn công nghe lén (man-in-the-middle attacks) và đánh cắp thông tin đăng nhập.

Semgrep, với vai trò là một công cụ SAST, chỉ có thể phân tích mã nguồn tĩnh và không có thông tin về môi trường runtime hoặc cấu hình mạng. Do đó, mặc dù phát hiện ra một hành vi có khả năng gây rủi ro, chúng ta cần thêm thông tin để xác định xem đây có phải là một lỗ hổng thực sự (True Positive) hay chỉ là một cảnh báo trong môi trường an toàn (False Positive).

##### 3. Tác động thực tế trong bối cảnh EShop.

Trong bối cảnh EShop, việc dữ liệu đăng nhập bị lộ có thể dẫn đến các tác động nghiêm trọng:

*   **Chiếm đoạt tài khoản người dùng:** Kẻ tấn công có thể sử dụng thông tin đăng nhập bị đánh cắp để truy cập vào tài khoản của người dùng, từ đó thực hiện các hành vi độc hại như đặt hàng giả, thay đổi thông tin cá nhân, hoặc sử dụng thông tin thanh toán (nếu có).
*   **Mất lòng tin của người dùng:** Nếu ứng dụng bị phát hiện gửi dữ liệu nhạy cảm qua kênh không an toàn, người dùng sẽ mất lòng tin vào khả năng bảo mật của EShop, dẫn đến việc giảm tỷ lệ người dùng và ảnh hưởng tiêu cực đến danh tiếng của thương hiệu.
*   **Vi phạm quy định về bảo mật dữ liệu:** Tùy thuộc vào khu vực địa lý và loại dữ liệu được xử lý, việc truyền thông tin nhạy cảm qua kênh không mã hóa có thể vi phạm các quy định về bảo vệ dữ liệu (ví dụ: GDPR).

Tuy nhiên, **mức độ tác động thực tế là NGHI VẤN** và cần được làm rõ dựa trên giá trị `API_URL`.

##### 4. Cách khắc phục cụ thể.

Cách khắc phục chính là đảm bảo tất cả các giao tiếp giữa client (ứng dụng EShop) và server API đều được mã hóa bằng HTTPS.

*   **Ưu tiên sử dụng HTTPS cho API_URL:** Cấu hình `API_URL` để trỏ đến một endpoint API sử dụng HTTPS. Nếu bạn đang phát triển trên môi trường local, hãy thiết lập một máy chủ API local có hỗ trợ HTTPS (ví dụ: sử dụng self-signed certificate cho mục đích phát triển).
*   **Cập nhật biến môi trường hoặc cấu hình:** Đảm bảo rằng biến `API_URL` luôn được thiết lập với scheme `https://`.
*   **Kiểm tra lại tất cả các request API khác:** Lỗ hổng này có thể không chỉ xuất hiện tại endpoint `/login` mà còn ở các endpoint khác mà ứng dụng EShop gọi tới. Cần rà soát lại toàn bộ các request API để đảm bảo tính nhất quán về bảo mật.

##### 5. Ghi chú cần tester kiểm tra thêm nếu chưa đủ context.

Để có thể đưa ra kết luận cuối cùng (True Positive hay False Positive), **tester cần kiểm tra thêm các thông tin sau**:

*   **Giá trị thực tế của biến `API_URL`:** Đây là yếu tố quan trọng nhất. Tester cần xác định `API_URL` đang trỏ đến địa chỉ nào trong môi trường triển khai hiện tại.
    *   **Nếu là `http://localhost:xxxx` hoặc `http://127.0.0.1:xxxx`:** Cần xác nhận đây là môi trường phát triển/lab và không có người dùng thật nào bị ảnh hưởng. Tuy nhiên, vẫn khuyến khích sử dụng HTTPS ngay cả trong môi trường local để hình thành thói quen bảo mật tốt.
    *   **Nếu là một địa chỉ IP công cộng hoặc tên miền có thể truy cập từ Internet:** Vui lòng XÁC NHẬN NGAY LẬP TỨC rằng API đang sử dụng HTTPS. Nếu không, đây là **True Positive** với mức độ rủi ro cao.
*   **Ngữ cảnh triển khai:** Ứng dụng EShop này đang được triển khai ở đâu (môi trường dev, staging, production)? Ai là người dùng của ứng dụng này? Dữ liệu đăng nhập có chứa thông tin nhạy cảm đặc biệt không (ví dụ: thông tin y tế, tài chính)?
*   **Cấu hình SSL/TLS trên server API:** Nếu API đang chạy trên một server riêng, hãy kiểm tra xem server đó có cấu hình SSL/TLS đầy đủ và chính xác hay không.

Sau khi có thêm thông tin từ các điểm kiểm tra này, việc phân loại cuối cùng sẽ dễ dàng hơn.

### SEMGREP-006: typescript.react.security.react-insecure-request.react-insecure-request

#### Tags lỗi
| Thuộc tính | Giá trị |
|---|---|
| Rule ID | `typescript.react.security.react-insecure-request.react-insecure-request` |
| Severity | `ERROR` |
| CWE | CWE-319: Cleartext Transmission of Sensitive Information |
| OWASP | A03:2017 - Sensitive Data Exposure, A02:2021 - Cryptographic Failures, A04:2025 - Cryptographic Failures |
| Likelihood | `LOW` |
| Impact | `MEDIUM` |
| Confidence | `MEDIUM` |

#### Thông tin finding
- File: `eshop-sut/frontend-mobile/App.js`
- Dòng: 222
- Trạng thái kiểm chứng: Needs Human Review

#### Bằng chứng mã nguồn
```text
   217:       );
   218:       return;
   219:     }
   220: 
   221:     try {
=> 222:       const response = await fetch(`${API_URL}/register`, {
   223:         method: "POST",
   224:         headers: { "Content-Type": "application/json" },
   225:         body: JSON.stringify({
   226:           name: registerName,
   227:           email: registerEmail,
```

#### Phân tích AI
Tuyệt vời! Với vai trò là chuyên gia bảo mật ứng dụng, tôi sẽ tiến hành triage finding SEMGREP-006 dựa trên thông tin bạn cung cấp.

---

##### Triage Finding: SEMGREP-006

**1. Phân loại:** Needs Human Review

**2. Lý do phân loại dựa trên source evidence:**

Semgrep rule phát hiện một yêu cầu mạng không được mã hóa (`HTTP`) được thực hiện bằng hàm `fetch` tới endpoint `/register` của API. `API_URL` được sử dụng ở đây. Về mặt kỹ thuật, đây là một lỗ hổng tiềm ẩn thuộc về CWE-319 (Cleartext Transmission of Sensitive Information) và liên quan đến OWASP A03:2017/A02:2021/A04:2025.

Tuy nhiên, để xác định đây là True Positive hay False Positive, chúng ta cần thêm thông tin về ngữ cảnh triển khai của `API_URL` và cách ứng dụng EShop này được sử dụng. Cụ thể:

*   **Ngữ cảnh `API_URL`:** Nếu `API_URL` luôn trỏ đến `localhost` hoặc một địa chỉ IP nội bộ trong môi trường development/lab, và không bao giờ được triển khai lên môi trường production với endpoint không có TLS, thì đây có thể là False Positive. Tuy nhiên, nếu `API_URL` có thể được cấu hình để trỏ tới một server API thực tế trên Internet mà không sử dụng HTTPS, thì đó là một True Positive.
*   **Tính nhạy cảm của dữ liệu:** Dữ liệu được gửi đi là `name`, `email`, `password` (từ ngữ cảnh của việc đăng ký người dùng) và các thông tin khác có thể được bao gồm trong body của request. Các thông tin này có thể được coi là nhạy cảm.
*   **Khả năng reachable:** Code này nằm trong một hàm `try...catch` và dường như là một phần của luồng logic đăng ký người dùng, do đó có khả năng được thực thi trong quá trình runtime của ứng dụng.

**3. Tác động thực tế trong bối cảnh EShop:**

Nếu `API_URL` trỏ đến một server API không sử dụng HTTPS và ứng dụng được triển khai trong môi trường không tin cậy (ví dụ: mạng công cộng), thông tin đăng ký nhạy cảm của người dùng (tên, email, mật khẩu) có thể bị kẻ tấn công đọc trộm khi truyền qua mạng. Điều này có thể dẫn đến việc tài khoản người dùng bị chiếm đoạt, đánh cắp danh tính hoặc các hành vi lạm dụng khác. Tuy nhiên, do EShop đang được quét như ứng dụng lab local và `API_URL` thường được cấu hình cho localhost trong môi trường dev/lab, khả năng tác động thực tế có thể thấp trong giai đoạn hiện tại.

**4. Cách khắc phục cụ thể:**

Cách khắc phục **khuyến nghị** là đảm bảo rằng tất cả các yêu cầu API từ frontend mobile đến backend đều được thực hiện qua HTTPS.

*   **Ưu tiên:** Thay đổi `API_URL` để sử dụng `https://` thay vì `http://` khi gọi tới server API của EShop. Ví dụ: `${process.env.REACT_APP_API_URL}` và đảm bảo biến môi trường này được cấu hình với schema `https://`. Nếu `API_URL` là một hằng số cố định, hãy cập nhật nó thành `https://localhost:port` hoặc `https://your-api-domain.com`.
*   **Cấu hình server:** Đảm bảo rằng server API mà `API_URL` trỏ tới đã được cấu hình TLS/SSL đúng cách và phục vụ các yêu cầu qua cổng 443.

**5. Ghi chú cần tester kiểm tra thêm nếu chưa đủ context:**

Để phân loại dứt điểm, tester cần xác định:

*   **Giá trị hiện tại của `API_URL`:** Nó trỏ tới đâu trong môi trường dev/lab?
*   **Cấu hình triển khai:** `API_URL` được cấu hình như thế nào trong các môi trường (dev, staging, production)? Liệu nó có thể bị thay đổi để trỏ tới một server API công cộng không sử dụng HTTPS không?
*   **Vai trò của file `App.js`:** Đây có phải là mã chính của ứng dụng hay là một phần của script test/demo? Nếu là lab, liệu có cần thực sự triển khai với HTTPS hay không? (Tuy nhiên, theo nguyên tắc, việc sử dụng HTTP cho dữ liệu nhạy cảm luôn là một rủi ro tiềm ẩn).

Dựa trên những kiểm tra này, chúng ta có thể đưa ra kết luận cuối cùng là `True Positive` hoặc `False Positive`. Hiện tại, `Needs Human Review` là phân loại phù hợp nhất.

### SEMGREP-007: typescript.react.security.react-insecure-request.react-insecure-request

#### Tags lỗi
| Thuộc tính | Giá trị |
|---|---|
| Rule ID | `typescript.react.security.react-insecure-request.react-insecure-request` |
| Severity | `ERROR` |
| CWE | CWE-319: Cleartext Transmission of Sensitive Information |
| OWASP | A03:2017 - Sensitive Data Exposure, A02:2021 - Cryptographic Failures, A04:2025 - Cryptographic Failures |
| Likelihood | `LOW` |
| Impact | `MEDIUM` |
| Confidence | `MEDIUM` |

#### Thông tin finding
- File: `eshop-sut/frontend-mobile/App.js`
- Dòng: 244
- Trạng thái kiểm chứng: Needs Human Review

#### Bằng chứng mã nguồn
```text
   239:     }
   240:   };
   241: 
   242:   const handleForgotPasswordRequest = async () => {
   243:     try {
=> 244:       const response = await fetch(`${API_URL}/forgot-password`, {
   245:         method: "POST",
   246:         headers: { "Content-Type": "application/json" },
   247:         body: JSON.stringify({ email: forgotEmail }),
   248:       });
   249:       const data = await response.json();
```

#### Phân tích AI
Tuyệt vời, tôi sẽ đóng vai trò là chuyên gia bảo mật ứng dụng để tiến hành triage finding của Semgrep này.

---

##### Triage Finding Bảo Mật

**Mã finding:** SEMGREP-007
**Rule ID:** typescript.react.security.react-insecure-request.react-insecure-request
**File nguồn:** eshop-sut/frontend-mobile/App.js
**Dòng:** 244
**Severity:** ERROR
**CWE:** CWE-319: Cleartext Transmission of Sensitive Information
**OWASP:** A03:2017 - Sensitive Data Exposure, A02:2021 - Cryptographic Failures, A04:2025 - Cryptographic Failures
**Likelihood:** LOW
**Impact:** MEDIUM
**Confidence:** MEDIUM
**Cảnh báo Semgrep:** Unencrypted request over HTTP detected.

---

##### 1. Phân loại:

Needs Human Review

##### 2. Lý do phân loại dựa trên source evidence:

Rule của Semgrep phát hiện việc sử dụng `fetch` để gửi request đến `${API_URL}/forgot-password` mà không có ngữ cảnh rõ ràng về giao thức (`http` hay `https`). Tuy nhiên, **bằng chứng mã nguồn (source evidence)** chỉ hiển thị cách tạo URL request mà không cho thấy nội dung hoặc cách `API_URL` được định nghĩa.

Vì Semgrep là SAST, nó chỉ phân tích mã nguồn tĩnh. Trong bối cảnh ứng dụng EShop đang được quét như một lab local trên `localhost`, việc sử dụng `http` cho các request nội bộ có thể là hành vi mong muốn trong môi trường phát triển và không nhất thiết dẫn đến rủi ro bảo mật ở môi trường đó. Tuy nhiên, chúng ta không có đủ thông tin về cách `API_URL` được cấu hình cho các môi trường khác nhau (ví dụ: staging, production).

Nếu `API_URL` có thể được cấu hình để trỏ đến máy chủ HTTP bên ngoài môi trường lab và người dùng có thể tương tác với tính năng này trên môi trường đó, thì đây sẽ là một lỗ hổng **True Positive**. Ngược lại, nếu `API_URL` luôn được cấu hình với `https` ở môi trường production hoặc chỉ sử dụng cho mục đích test nội bộ không có dữ liệu nhạy cảm, thì đây có thể là **False Positive**.

##### 3. Tác động thực tế trong bối cảnh EShop:

Nếu `API_URL` đang sử dụng protocol HTTP (không mã hóa) để gửi dữ liệu, đặc biệt là dữ liệu liên quan đến việc khôi phục mật khẩu (ví dụ: địa chỉ email người dùng, token khôi phục mật khẩu), thì thông tin này có thể bị đánh cắp bởi kẻ tấn công nghe lén trên mạng (man-in-the-middle attack). Điều này sẽ dẫn đến **Sensitive Data Exposure** (OWASP A03:2017) và **Cryptographic Failures** (OWASP A02:2021, A04:2025) nếu email chứa thông tin nhạy cảm.

Tuy nhiên, trong bối cảnh "ứng dụng lab local" và việc finding liên quan đến `localhost`, tác động thực tế có thể thấp nếu môi trường lab này không có bất kỳ người dùng thật nào và chỉ dùng cho mục đích thử nghiệm. Rủi ro chỉ tăng lên khi `API_URL` được cấu hình cho môi trường production hoặc các môi trường khác có người dùng thực.

##### 4. Cách khắc phục cụ thể:

1.  **Cấu hình HTTPS cho API Server:** Đảm bảo rằng API server mà `API_URL` trỏ tới luôn sử dụng HTTPS để mã hóa tất cả các giao tiếp.
2.  **Cập nhật cấu hình `API_URL`:**
    *   Nếu `API_URL` là một biến môi trường hoặc được lấy từ file cấu hình, hãy kiểm tra và đảm bảo nó luôn bắt đầu bằng `https://` cho các môi trường ngoài local development.
    *   Trong môi trường local development, có thể có các lựa chọn:
        *   Tự cấu hình HTTPS cho server local (khuyến khích).
        *   Chấp nhận sử dụng HTTP cho API local, nhưng đảm bảo **không bao giờ** gửi dữ liệu nhạy cảm qua đó, hoặc chỉ sử dụng cho các endpoint không nhạy cảm.
3.  **Kiểm tra định nghĩa `API_URL`:** Tìm kiếm trong toàn bộ project để xác định nơi `API_URL` được định nghĩa và cách nó được cấu hình cho các môi trường khác nhau. Sử dụng các biến môi trường hoặc hệ thống quản lý cấu hình để đảm bảo URL được sử dụng là an toàn.

**Ví dụ minh họa cho việc sử dụng template string an toàn hơn:**

```javascript
// Giả định: API_URL_BASE được định nghĩa trong file cấu hình hoặc biến môi trường
// và có thể khác nhau giữa các môi trường
const API_URL_BASE = process.env.API_URL_BASE || "http://localhost:3000"; // Giá trị mặc định cho local dev
const API_ENDPOINT = "forgot-password";

// Luôn đảm bảo API_URL_BASE bắt đầu bằng https cho production/staging
const fullApiUrl = `${API_URL_BASE.endsWith('/') ? API_URL_BASE.slice(0, -1) : API_URL_BASE}/${API_ENDPOINT}`;

// ...
      const response = await fetch(fullApiUrl, {
// ...
```

##### 5. Ghi chú cần tester kiểm tra thêm:

*   **Kiểm tra cấu hình `API_URL`:** Cần xác định chính xác `API_URL` được định nghĩa ở đâu trong ứng dụng và cách nó được cấu hình cho các **môi trường production, staging, và development**. Tester cần kiểm tra tất cả các nơi `API_URL` có thể được thiết lập.
*   **Môi trường deploy:** Xác nhận xem ứng dụng có được deploy trên các môi trường nào và `http` có thực sự được sử dụng cho các request bên ngoài môi trường local dev hay không.
*   **Dữ liệu nhạy cảm:** Mặc dù việc khôi phục mật khẩu thường liên quan đến email, cần xác nhận xem dữ liệu nào được gửi đi trong `body` của request này. Nếu có thêm các trường thông tin nhạy cảm khác, tác động sẽ cao hơn.
*   **Phạm vi của `localhost`:** Nếu `API_URL` chỉ trỏ đến `localhost` và server API của EShop cũng chạy trên `localhost` trong môi trường dev, thì rủi ro có thể thấp nếu đây là một lab riêng biệt. Tuy nhiên, nếu `localhost` có thể được proxy hoặc truy cập từ xa, rủi ro sẽ tăng lên.

---

### SEMGREP-008: typescript.react.security.react-insecure-request.react-insecure-request

#### Tags lỗi
| Thuộc tính | Giá trị |
|---|---|
| Rule ID | `typescript.react.security.react-insecure-request.react-insecure-request` |
| Severity | `ERROR` |
| CWE | CWE-319: Cleartext Transmission of Sensitive Information |
| OWASP | A03:2017 - Sensitive Data Exposure, A02:2021 - Cryptographic Failures, A04:2025 - Cryptographic Failures |
| Likelihood | `LOW` |
| Impact | `MEDIUM` |
| Confidence | `MEDIUM` |

#### Thông tin finding
- File: `eshop-sut/frontend-mobile/App.js`
- Dòng: 272
- Trạng thái kiểm chứng: Needs Human Review

#### Bằng chứng mã nguồn
```text
   267:       );
   268:       return;
   269:     }
   270: 
   271:     try {
=> 272:       const response = await fetch(`${API_URL}/reset-password`, {
   273:         method: "POST",
   274:         headers: { "Content-Type": "application/json" },
   275:         body: JSON.stringify({ email: forgotEmail, resetToken, newPassword }),
   276:       });
   277:       if (!response.ok)
```

#### Phân tích AI
Tuyệt vời! Với vai trò là chuyên gia bảo mật ứng dụng, tôi sẽ thực hiện phân tích kỹ lưỡng finding SEMGREP-008 này.

##### Triage Finding Bảo Mật: SEMGREP-008

##### 1. Phân loại
**Needs Human Review**

##### 2. Lý do phân loại dựa trên source evidence
Dựa trên bằng chứng mã nguồn được cung cấp, Semgrep đã phát hiện ra một yêu cầu HTTP được thực hiện thông qua `fetch` tới endpoint `${API_URL}/reset-password` tại dòng 272 của file `App.js`. Rule ID `typescript.react.security.react-insecure-request.react-insecure-request` và mô tả "Unencrypted request over HTTP detected" chỉ ra rằng yêu cầu này có khả năng được gửi qua giao thức HTTP không mã hóa, vi phạm nguyên tắc về bảo vệ dữ liệu nhạy cảm (CWE-319, OWASP A03:2017, A02:2021, A04:2025).

Tuy nhiên, để đưa ra phân loại cuối cùng, chúng ta cần xem xét thêm một số yếu tố:

*   **Ngữ cảnh của `API_URL`:** Giá trị của biến `API_URL` không được cung cấp trong bằng chứng mã nguồn. Nếu `API_URL` trỏ đến `http://localhost` hoặc một địa chỉ IP nội bộ trong môi trường phát triển/lab, thì yêu cầu này có thể không mang rủi ro đáng kể *cho mục đích thử nghiệm ban đầu*. Tuy nhiên, trong môi trường production, nếu `API_URL` được cấu hình là một server chạy HTTP thay vì HTTPS, đó sẽ là một lỗ hổng nghiêm trọng.
*   **Môi trường triển khai:** Như đã đề cập trong ngữ cảnh cho triage tĩnh, "EShop đang được quét như ứng dụng lab local; finding liên quan localhost cần kiểm tra môi trường trước khi kết luận rủi ro cuối." Điều này cho thấy cần xác định liệu `API_URL` có được cấu hình để sử dụng HTTPS trên production hay không.
*   **Độ nhạy cảm của dữ liệu:** Mặc dù việc gửi thông tin reset mật khẩu qua kênh không mã hóa là nhạy cảm, nhưng mức độ rủi ro còn phụ thuộc vào việc dữ liệu này có bị chặn lại bởi bên thứ ba hay không, và mức độ bảo mật tổng thể của hệ thống.

Do đó, trong khi mã nguồn rõ ràng cho thấy một yêu cầu có khả năng không mã hóa, ngữ cảnh triển khai và cấu hình của `API_URL` là yếu tố quyết định để phân loại đây là True Positive hay False Positive.

##### 3. Tác động thực tế trong bối cảnh EShop
Nếu `API_URL` được cấu hình sử dụng HTTP trong môi trường production, tác động thực tế có thể bao gồm:

*   **Lộ thông tin nhạy cảm:** Token reset mật khẩu và mật khẩu mới khi được gửi đi có thể bị kẻ tấn công nghe lén, dẫn đến việc chiếm quyền truy cập vào tài khoản người dùng.
*   **Tấn công "Man-in-the-Middle" (MitM):** Kẻ tấn công có thể chèn dữ liệu độc hại hoặc thay đổi thông tin yêu cầu, có khả năng gây ra các hành vi không mong muốn hoặc lợi dụng lỗ hổng.

Tuy nhiên, nếu `API_URL` chỉ dùng cho môi trường dev/lab và luôn được truy cập qua HTTPS trong production, thì rủi ro thực tế có thể thấp hoặc không tồn tại.

##### 4. Cách khắc phục cụ thể
1.  **Ưu tiên sử dụng HTTPS:** Đảm bảo rằng tất cả các yêu cầu API, đặc biệt là những yêu cầu liên quan đến dữ liệu nhạy cảm như reset mật khẩu, luôn được thực hiện qua giao thức HTTPS thay vì HTTP.
2.  **Kiểm tra và cấu hình `API_URL`:**
    *   Nếu `API_URL` được định nghĩa trong một file cấu hình (ví dụ: `.env`, `config.js`), hãy kiểm tra xem nó có đang trỏ đến một endpoint HTTPS hay không.
    *   Trong môi trường production, cấu hình `API_URL` bắt buộc phải là một URL bắt đầu bằng `https://`.
3.  **Sử dụng thư viện HTTP an toàn:** Nếu đang sử dụng một thư viện HTTP tùy chỉnh hoặc cấu hình `fetch` một cách phức tạp, hãy đảm bảo nó tuân thủ các tiêu chuẩn an ninh mạng. Tuy nhiên, trong trường hợp này, vấn đề chính là giao thức, không phải bản thân thư viện `fetch`.
4.  **Cập nhật giá trị `API_URL`:**
    Chỉnh sửa biến `API_URL` để luôn sử dụng giao thức `https`. Ví dụ, nếu trước đây là `http://api.example.com`, thì đổi thành `https://api.example.com`.

##### 5. Ghi chú cần tester kiểm tra thêm nếu chưa đủ context
Để hoàn tất việc phân loại và đánh giá đúng rủi ro, vui lòng kiểm tra và cung cấp thêm thông tin về:

*   **Giá trị thực tế của `API_URL`:** Cần xác định giá trị của biến `API_URL` trong các môi trường khác nhau (development, staging, production).
*   **Cơ chế cấu hình biến môi trường:** Nếu `API_URL` được quản lý bằng biến môi trường, hãy kiểm tra cách biến này được thiết lập và áp dụng trên các môi trường triển khai.
*   **Môi trường triển khai:** Xác nhận rằng các API server mà ứng dụng mobile kết nối tới luôn được cấu hình để sử dụng HTTPS, đặc biệt là trong môi trường production.

Sau khi có được những thông tin này, chúng ta có thể đưa ra quyết định cuối cùng là True Positive (nếu rủi ro tồn tại trong production) hoặc False Positive (nếu môi trường dev/lab và production đều được bảo vệ đúng cách).

### SEMGREP-009: typescript.react.security.react-insecure-request.react-insecure-request

#### Tags lỗi
| Thuộc tính | Giá trị |
|---|---|
| Rule ID | `typescript.react.security.react-insecure-request.react-insecure-request` |
| Severity | `ERROR` |
| CWE | CWE-319: Cleartext Transmission of Sensitive Information |
| OWASP | A03:2017 - Sensitive Data Exposure, A02:2021 - Cryptographic Failures, A04:2025 - Cryptographic Failures |
| Likelihood | `LOW` |
| Impact | `MEDIUM` |
| Confidence | `MEDIUM` |

#### Thông tin finding
- File: `eshop-sut/frontend-mobile/App.js`
- Dòng: 296
- Trạng thái kiểm chứng: Needs Human Review

#### Bằng chứng mã nguồn
```text
   291:       );
   292:       return;
   293:     }
   294: 
   295:     try {
=> 296:       const response = await fetch(`${API_URL}/users/me`, {
   297:         method: "PUT",
   298:         headers: {
   299:           "Content-Type": "application/json",
   300:           Authorization: `Bearer ${token}`,
   301:         },
```

#### Phân tích AI
Tuyệt vời! Với vai trò chuyên gia bảo mật ứng dụng, tôi sẽ tiến hành triage finding SEMGREP-009 này dựa trên thông tin bạn cung cấp.

##### Triage Finding Bảo Mật SEMGREP-009

1.  **Phân loại:** Needs Human Review

2.  **Lý do phân loại dựa trên source evidence:**
    Bằng chứng mã nguồn cho thấy ứng dụng đang thực hiện một yêu cầu `PUT` đến `"${API_URL}/users/me"` không sử dụng HTTPS. Rule của Semgrep phát hiện việc sử dụng HTTP thay vì HTTPS, dẫn đến nguy cơ truyền thông tin nhạy cảm dưới dạng văn bản rõ (cleartext). API endpoint này (`/users/me`) có khả năng trả về hoặc xử lý thông tin người dùng, và header `Authorization: Bearer ${token}` rõ ràng cho thấy token xác thực đang được gửi đi.

    Tuy nhiên, điểm mấu chốt khiến tôi phân loại là "Needs Human Review" nằm ở cách định nghĩa `API_URL`. Semgrep là SAST, nó chỉ phân tích cấu trúc mã nguồn mà không biết môi trường chạy thực tế.
    *   Nếu `API_URL` được cấu hình động và có thể trỏ đến một server *production* không sử dụng HTTPS, thì đây là một **True Positive** nghiêm trọng.
    *   Nếu `API_URL` luôn trỏ đến `localhost` hoặc một địa chỉ IP được sử dụng *chỉ trong môi trường phát triển (dev/lab)* nơi kết nối HTTP có thể được chấp nhận cho mục đích thử nghiệm hoặc do hạ tầng mạng nội bộ đảm bảo an toàn, thì đây có thể là một **False Positive** trong ngữ cảnh production.

    Việc thiếu thông tin về cách `API_URL` được định nghĩa và cách ứng dụng được triển khai (dev, staging, prod) khiến tôi không thể kết luận chắc chắn về rủi ro thực tế.

3.  **Tác động thực tế trong bối cảnh EShop:**
    Tác động tiềm ẩn có thể là **MEDIUM** như Semgrep đánh giá. Nếu yêu cầu này thực sự được thực hiện qua HTTP trong một môi trường không tin cậy (ví dụ: mạng Wi-Fi công cộng), kẻ tấn công có thể nghe lén (eavesdrop) và đánh cắp token xác thực của người dùng. Token này có thể được kẻ tấn công sử dụng để giả mạo người dùng, truy cập trái phép vào thông tin cá nhân của họ trên `/users/me` hoặc thực hiện các hành động khác nhân danh người dùng đó.

    Tuy nhiên, tác động chỉ trở nên *thực tế* nếu:
    *   `API_URL` trỏ đến một server mà kết nối đó có thể bị theo dõi.
    *   Thông tin trong yêu cầu/phản hồi của `/users/me` đủ nhạy cảm để bị khai thác.endswith
    *   Token có thời gian sống dài hoặc không được quản lý chặt chẽ.

4.  **Cách khắc phục cụ thể:**
    *   **Ưu tiên hàng đầu:** Đảm bảo *tất cả* các yêu cầu đến API, đặc biệt là những yêu cầu chứa thông tin xác thực hoặc dữ liệu nhạy cảm, đều sử dụng HTTPS.
        *   **Với backend:** Kiểm tra và cấu hình server API để luôn chấp nhận và sử dụng HTTPS.
        *   **Với frontend:**
            *   Nếu `API_URL` được hardcode, hãy đảm bảo nó đang sử dụng `https://`.
            *   Nếu `API_URL` được cấu hình động (ví dụ: qua biến môi trường, file cấu hình), hãy đảm bảo biến này được đặt với schema `https://` cho môi trường production và staging.
    *   **Kiểm tra khai báo `API_URL`:** Tìm kiếm định nghĩa của `API_URL` trong toàn bộ codebase. Xác định xem nó được định nghĩa *như thế nào* và *cho môi trường nào* nó được sử dụng.
    *   **Môi trường dev/lab:** Nếu việc sử dụng HTTP chỉ xảy ra trong môi trường phát triển cục bộ (localhost) và hạ tầng mạng nội bộ được kiểm soát, có thể cân nhắc chấp nhận rủi ro này cho *môi trường dev*, nhưng *không bao giờ* cho staging hoặc production.

5.  **Ghi chú cần tester kiểm tra thêm nếu chưa đủ context:**
    *   **Kiểm tra định nghĩa và sử dụng `API_URL`:** Tester cần tìm file hoặc biến môi trường chứa định nghĩa của `API_URL` và xác định giá trị của nó trong các môi trường khác nhau (dev, staging, production).
    *   **Mục đích của endpoint `/users/me`:** Làm rõ thông tin gì được gửi đi và nhận về từ endpoint này. Nếu nó chỉ trả về thông tin không nhạy cảm (ví dụ: ID người dùng đã được mã hóa/hash), thì mức độ rủi ro sẽ giảm đi.
    *   **Môi trường triển khai:** Xác nhận ứng dụng eShop được triển khai trong ngữ cảnh nào (lab) và liệu các quy định về an ninh mạng cho phép sử dụng HTTP cho kết nối API trong môi trường đó hay không.
    *   **Cơ chế quản lý token:** Kiểm tra cách token được lưu trữ và quản lý trong ứng dụng di động để đánh giá thêm rủi ro bị lộ token.

### SEMGREP-010: typescript.react.security.react-insecure-request.react-insecure-request

#### Tags lỗi
| Thuộc tính | Giá trị |
|---|---|
| Rule ID | `typescript.react.security.react-insecure-request.react-insecure-request` |
| Severity | `ERROR` |
| CWE | CWE-319: Cleartext Transmission of Sensitive Information |
| OWASP | A03:2017 - Sensitive Data Exposure, A02:2021 - Cryptographic Failures, A04:2025 - Cryptographic Failures |
| Likelihood | `LOW` |
| Impact | `MEDIUM` |
| Confidence | `MEDIUM` |

#### Thông tin finding
- File: `eshop-sut/frontend-mobile/App.js`
- Dòng: 362
- Trạng thái kiểm chứng: Needs Human Review

#### Bằng chứng mã nguồn
```text
   357:     if (!couponCode.trim()) return;
   358:     setCouponError("");
   359:     setCouponResult(null);
   360:     setApplyingCoupon(true);
   361:     try {
=> 362:       const response = await fetch(`${API_URL}/apply-coupon`, {
   363:         method: "POST",
   364:         headers: { "Content-Type": "application/json" },
   365:         body: JSON.stringify({
   366:           code: couponCode.trim().toUpperCase(),
   367:           total_amount: cartTotal,
```

#### Phân tích AI
Tuyệt vời! Với vai trò là chuyên gia bảo mật ứng dụng, tôi sẽ tiến hành phân tích finding này theo yêu cầu của bạn.

---

##### Phân tích Finding Bảo Mật SEMGREP-010

**1. Phân loại:** False Positive

**2. Lý do phân loại dựa trên source evidence:**

*   **Bằng chứng mã nguồn (Source Evidence):** Dòng mã `const response = await fetch(\`${API_URL}/apply-coupon\`, { ... });` cho thấy ứng dụng đang thực hiện một yêu cầu HTTP đến một URL được định nghĩa bởi biến `API_URL`.
*   **Ngữ cảnh môi trường (Deployment Context):** Thông tin cung cấp cho biết "EShop đang được quét như ứng dụng lab local; finding liên quan localhost cần kiểm tra môi trường trước khi kết luận rủi ro cuối." Điều này ngụ ý rằng `API_URL` *có thể* đang trỏ đến `http://localhost:PORT` hoặc một địa chỉ local tương tự.
*   **Phân tích:**
    *   Rule ID `typescript.react.security.react-insecure-request.react-insecure-request` và CWE-319 nhắm đến việc truyền tải thông tin nhạy cảm qua các kênh không mã hóa (HTTP).
    *   Tuy nhiên, việc sử dụng HTTP cho các yêu cầu đến `localhost` trong môi trường phát triển (dev/lab) là rất phổ biến và thường không mang rủi ro bảo mật nghiêm trọng *cho chính môi trường đó*. Các giao tiếp này thường chỉ diễn ra trong cùng một máy tính lập trình viên hoặc trong một mạng nội bộ được kiểm soát chặt chẽ, không phải là giao tiếp với người dùng cuối hoặc trên mạng công cộng.
    *   Semgrep phát hiện "Unencrypted request over HTTP detected", nhưng nó chưa đủ ngữ cảnh để xác định liệu `API_URL` có thực sự là một endpoint "nhạy cảm" trên môi trường *production* hay không. Nếu `API_URL` chỉ trỏ đến localhost của môi trường dev, thì việc truyền dữ liệu coupon code qua HTTP ở đây không phải là một lỗ hổng thực tế của ứng dụng khi deploy ra môi trường production.
    *   Chúng ta chưa có bằng chứng cho thấy `API_URL` sẽ trỏ đến một máy chủ ngoài (public) sử dụng HTTP mà lại gửi thông tin nhạy cảm.

**3. Tác động thực tế trong bối cảnh EShop:**

Trong bối cảnh "ứng dụng lab local", việc phát hiện này ít có tác động thực tế về mặt bảo mật. Nếu `API_URL` được cấu hình để trỏ đến `localhost` hoặc một địa chỉ IP nội bộ cho mục đích phát triển và kiểm thử, thì nguy cơ bị nghe lén (interception) bởi các bên không mong muốn là rất thấp. Rủi ro chỉ thực sự phát sinh nếu ứng dụng này được deploy lên môi trường production và `API_URL` lại trỏ đến một máy chủ thực tế qua HTTP để xử lý các yêu cầu coupon code.

**4. Cách khắc phục cụ thể:**

Để đảm bảo tính bảo mật cao nhất, ngay cả trong môi trường phát triển nếu có thể:

*   **Ưu tiên sử dụng HTTPS:** Ngay cả với `localhost`, việc cấu hình server local để sử dụng HTTPS (ví dụ: với các chứng chỉ tự ký) sẽ giúp mô phỏng tốt hơn môi trường production và loại bỏ hoàn toàn nguy cơ này.
*   **Kiểm tra biến môi trường/cấu hình:** Xác định cách biến `API_URL` được thiết lập. Nếu nó là một biến môi trường hoặc tệp cấu hình, đảm bảo rằng trong môi trường production, nó luôn trỏ đến một endpoint sử dụng HTTPS.
*   **Cập nhật Rule Detection (Nếu quan ngại):** Nếu có lo ngại rằng biến `API_URL` có thể bị cấu hình sai trong production và gây ra rủi ro, có thể xem xét việc cập nhật rule Semgrep để kiểm tra giá trị của `API_URL`, ví dụ như kiểm tra nó có bắt đầu bằng `http://` hay không. Tuy nhiên, việc này có thể dẫn đến nhiều False Positive hơn nếu `http://` được cho phép cho các endpoint không nhạy cảm.

**5. Ghi chú cần tester kiểm tra thêm nếu chưa đủ context:**

*   **Xác định giá trị thực tế của `API_URL`:** Yêu cầu tester kiểm tra giá trị của biến `API_URL` trong các cấu hình môi trường khác nhau (development, staging, production) để xác nhận liệu nó có bao giờ trỏ đến một máy chủ thực tế bằng giao thức HTTP hay không.
*   **Tính nhạy cảm của dữ liệu coupon code:** Tuy coupon code có thể không quá nhạy cảm, nhưng nếu nó liên quan đến các chương trình khuyến mãi lớn hoặc có thể bị lạm dụng, thì việc bảo vệ nó sẽ quan trọng hơn. Điều này cần được làm rõ bởi chủ sở hữu ứng dụng.
*   **Kiểm tra cách xử lý lỗi khi áp dụng coupon:** Mặc dù không trực tiếp liên quan đến finding này, nhưng nên kiểm tra xem lỗi mạng hoặc lỗi từ server có được xử lý tốt hay không để người dùng không bị lộ thông tin hoặc gặp trải nghiệm xấu.

---

### SEMGREP-011: typescript.react.security.react-insecure-request.react-insecure-request

#### Tags lỗi
| Thuộc tính | Giá trị |
|---|---|
| Rule ID | `typescript.react.security.react-insecure-request.react-insecure-request` |
| Severity | `ERROR` |
| CWE | CWE-319: Cleartext Transmission of Sensitive Information |
| OWASP | A03:2017 - Sensitive Data Exposure, A02:2021 - Cryptographic Failures, A04:2025 - Cryptographic Failures |
| Likelihood | `LOW` |
| Impact | `MEDIUM` |
| Confidence | `MEDIUM` |

#### Thông tin finding
- File: `eshop-sut/frontend-mobile/App.js`
- Dòng: 384
- Trạng thái kiểm chứng: Needs Human Review

#### Bằng chứng mã nguồn
```text
   379: 
   380:   const handleConfirmCheckout = async () => {
   381:     setCheckoutLoading(true);
   382:     try {
   383:       const finalAmount = couponResult ? couponResult.final_amount : cartTotal;
=> 384:       const response = await fetch(`${API_URL}/checkout`, {
   385:         method: "POST",
   386:         headers: {
   387:           "Content-Type": "application/json",
   388:           ...(token ? { Authorization: `Bearer ${token}` } : {}),
   389:         },
```

#### Phân tích AI
Tuyệt vời! Với vị thế chuyên gia bảo mật ứng dụng, tôi sẽ tiến hành triage finding SEMGREP-011 một cách chi tiết.

---

##### Triage Finding Bảo Mật: SEMGREP-011

##### 1. Phân loại:
Needs Human Review

##### 2. Lý do phân loại dựa trên source evidence:

Bằng chứng mã nguồn tại dòng 384 cho thấy một lệnh gọi `fetch` tới `${API_URL}/checkout`. Cảnh báo của Semgrep chỉ ra rằng đây là một "Unencrypted request over HTTP detected". Tuy nhiên, việc phân loại thành True Positive hay False Positive phụ thuộc vào giá trị của biến `API_URL` và cách ứng dụng này được triển khai trong môi trường production thực tế.

*   **Nếu `API_URL` trỏ tới một địa chỉ `http://localhost:PORT` hoặc một địa chỉ IP nội bộ dùng cho mục đích phát triển/lab:** Thì đây có khả năng là **False Positive** vì lưu lượng mạng nội bộ hoặc trong môi trường lab thường không cần thiết phải mã hóa. Mặc dù về mặt kỹ thuật là HTTP, nhưng rủi ro lộ lọt dữ liệu trên mạng cục bộ bị giới hạn.
*   **Nếu `API_URL` trỏ tới một tên miền hoặc IP có thể truy cập từ bên ngoài và sử dụng giao thức `http:` thay vì `https:`:** Thì đây là một **True Positive** nghiêm trọng. Việc truyền dữ liệu nhạy cảm qua HTTP là vi phạm bảo mật nghiêm trọng, có thể dẫn đến lộ lọt thông tin.
*   **Ngữ cảnh triển khai chưa rõ ràng:** Với thông tin hiện tại, chúng ta không biết `API_URL` được cấu hình như thế nào ở môi trường production hoặc môi trường mà `eshop-sut/frontend-mobile/App.js` sẽ chạy. Thông tin này rất quan trọng để đánh giá mức độ rủi ro thực tế.

##### 3. Tác động thực tế trong bối cảnh EShop:

Nếu `API_URL` thực sự sử dụng HTTP cho một endpoint liên quan đến xử lý thanh toán (`/checkout`), tác động có thể rất nghiêm trọng:

*   **Lộ lọt thông tin nhạy cảm:** Dữ liệu như chi tiết đơn hàng, số tiền thanh toán, thông tin nhận hàng, và có thể cả các token xác thực (`Authorization: Bearer ${token}`) có thể bị kẻ tấn công trên cùng mạng chặn bắt.
*   **Tấn công Man-in-the-Middle (MITM):** Kẻ tấn công có thể sửa đổi dữ liệu truyền đi, ví dụ như thay đổi số tiền thanh toán, gây thiệt hại tài chính cho cả người dùng và doanh nghiệp.
*   **Vi phạm tuân thủ:** Các quy định về bảo mật dữ liệu (như GDPR, PCI DSS nếu liên quan đến thanh toán thẻ) có thể bị vi phạm nếu thông tin nhạy cảm không được bảo vệ.

Tuy nhiên, tác động thực tế sẽ bị giảm thiểu đáng kể nếu như endpoint này chỉ được gọi trên môi trường local development hoặc lab testing.

##### 4. Cách khắc phục cụ thể:

1.  **Kiểm tra cấu hình `API_URL`:**
    *   Xác định giá trị thực tế của biến `API_URL` trong các môi trường khác nhau (development, staging, production).
    *   Đảm bảo rằng tất cả các endpoint được gọi từ frontend mobile đều sử dụng giao thức `https:` và trỏ tới một máy chủ đã được cấu hình SSL/TLS hợp lệ.
2.  **Cập nhật mã nguồn (nếu cần):**
    *   Nếu `API_URL` vẫn đang sử dụng `http:`, hãy sửa đổi nó để sử dụng `https:` và cấu hình chứng chỉ SSL/TLS cho backend API.
    *   Ví dụ (chỉ mang tính minh họa, cần điều chỉnh theo cách quản lý biến môi trường của dự án):
        ```javascript
        // Giả định API_URL được quản lý qua environment variables
        // Backend API nên expose qua HTTPS
        // const API_URL = process.env.REACT_APP_API_URL; 
        // Nếu API_URL vẫn là http://..., cần kiểm tra backend config
        const API_URL = "https://your-api-domain.com"; // Ví dụ của HTTPS
        
        const handleConfirmCheckout = async () => {
          setCheckoutLoading(true);
          try {
            const finalAmount = couponResult ? couponResult.final_amount : cartTotal;
            // Đảm bảo API_URL đã là https
            const response = await fetch(`${API_URL}/checkout`, { 
              method: "POST",
              headers: {
                "Content-Type": "application/json",
                ...(token ? { Authorization: `Bearer ${token}` } : {}),
              },
            });
            // ... xử lý response
          } catch (error) {
            // ... xử lý lỗi
          } finally {
            setCheckoutLoading(false);
          }
        };
        ```
3.  **Thực thi chính sách cho phép giao thức:** Kể từ React Native 0.60, sử dụng `android:usesCleartextTraffic="false"` trong `AndroidManifest.xml` cho Android để ngăn chặn các yêu cầu HTTP không mã hóa. Tương tự, cần kiểm tra cấu hình cho iOS.

##### 5. Ghi chú cần tester kiểm tra thêm nếu chưa đủ context:

*   **Cấu hình `API_URL`:** Cần kiểm tra cách biến `API_URL` được định nghĩa và quản lý trong các môi trường khác nhau (local development, staging, production). Liệu có sử dụng file `.env` hay cấu hình build nào khác không?
*   **Môi trường triển khai:** Xác nhận xem ứng dụng này có được triển khai ở môi trường production hay chỉ đang chạy trong lab/development. Nếu là lab, cần có sự xác nhận từ người quản lý hạ tầng hoặc devops về việc liệu `http://localhost` có được xem là rủi ro chấp nhận được trong môi trường đó hay không.
*   **Độ nhạy cảm của dữ liệu:** Dữ liệu được gửi trong request `POST` đến `/checkout` có chứa các thông tin cực kỳ nhạy cảm (ví dụ: chi tiết thẻ tín dụng trực tiếp) hay không? Dù cách nào cũng không nên truyền qua HTTP, nhưng mức độ nhạy cảm sẽ ảnh hưởng đến mức độ ưu tiên vá lỗi.
*   **Cơ chế CORS/Network Security Configurations:** Kiểm tra các cấu hình bảo mật mạng ở phía client (Android/iOS) có thể ảnh hưởng đến việc cho phép hoặc chặn các kết nối HTTP.

### SEMGREP-012: typescript.react.security.react-insecure-request.react-insecure-request

#### Tags lỗi
| Thuộc tính | Giá trị |
|---|---|
| Rule ID | `typescript.react.security.react-insecure-request.react-insecure-request` |
| Severity | `ERROR` |
| CWE | CWE-319: Cleartext Transmission of Sensitive Information |
| OWASP | A03:2017 - Sensitive Data Exposure, A02:2021 - Cryptographic Failures, A04:2025 - Cryptographic Failures |
| Likelihood | `LOW` |
| Impact | `MEDIUM` |
| Confidence | `MEDIUM` |

#### Thông tin finding
- File: `eshop-sut/frontend-mobile/App.js`
- Dòng: 400
- Trạng thái kiểm chứng: Needs Human Review

#### Bằng chứng mã nguồn
```text
   395:       });
   396:       const data = await response.json().catch(() => ({}));
   397:       if (!response.ok) throw new Error(data.error || "Lỗi khi thanh toán.");
   398: 
   399:       if (couponResult?.coupon_id && token) {
=> 400:         await fetch(`${API_URL}/coupon-usage`, {
   401:           method: "POST",
   402:           headers: {
   403:             "Content-Type": "application/json",
   404:             Authorization: `Bearer ${token}`,
   405:           },
```

#### Phân tích AI
Tuyệt vời! Hãy cùng nhau tiến hành phân tích và triage finding SEMGREP-012 này.

##### Phân tích Finding Bảo Mật SEMGREP-012

##### 1. Phân loại:
Needs Human Review

##### 2. Lý do phân loại dựa trên source evidence:

Dựa trên bằng chứng mã nguồn và ngữ cảnh được cung cấp, chúng ta thấy dòng 400 trong file `App.js` thực hiện một yêu cầu `fetch` đến một endpoint `/coupon-usage` tại `${API_URL}/coupon-usage`. Quan trọng là, chúng ta không có thông tin rõ ràng về cách biến `API_URL` được định nghĩa và sử dụng.

*   **Khả năng True Positive:** Nếu `API_URL` được định nghĩa để trỏ đến một máy chủ sử dụng giao thức HTTP không mã hóa (ví dụ: `http://localhost:3000`), và token được gửi đi chứa thông tin nhạy cảm, thì đây có thể là một lỗ hổng thực sự. `fetch` mặc định sẽ sử dụng giao thức được chỉ định trong URL.
*   **Khả năng False Positive:** Nếu `API_URL` được định nghĩa để luôn trỏ đến một máy chủ sử dụng giao thức HTTPS (ví dụ: `https://api.eshop.com`), hoặc nếu `API_URL` đang trỏ đến một môi trường development/lab chỉ sử dụng HTTP và được cho phép trong ngữ cảnh này, thì việc tìm thấy này có thể là một `False Positive`. Việc ứng dụng của bạn đang được quét như một ứng dụng lab local là một yếu tố quan trọng.
*   **Lý do "Needs Human Review":** Semgrep đã phát hiện một yêu cầu qua HTTP không mã hóa. Tuy nhiên, để kết luận chính xác, chúng ta cần xác định:
    *   **Giá trị thực tế của `API_URL` trong bối cảnh triển khai được quét:** Nó đang trỏ tới đâu? `http://` hay `https://`?
    *   **Tính nhạy cảm của dữ liệu trong `token`:** Token này có chứa thông tin cá nhân, thông tin xác thực nhạy cảm hay không?
    *   **Ngữ cảnh triển khai:** Đây là môi trường production, staging, hay chỉ là local development / lab? Nếu là lab local và không có dữ liệu nhạy cảm được truyền đi, thì rủi ro có thể thấp.

##### 3. Tác động thực tế trong bối cảnh EShop:

Nếu `API_URL` trỏ đến một máy chủ sử dụng HTTP và thông tin trong `token` là nhạy cảm, việc truyền nó qua kết nối không mã hóa có thể dẫn đến:

*   **Rò rỉ thông tin nhạy cảm (Sensitive Data Exposure):** Kẻ tấn công có thể chặn gói tin trên mạng để đánh cắp `token`. Nếu `token` này có thể được sử dụng để giả mạo người dùng hoặc truy cập vào các tài nguyên nhạy cảm khác, thì tác động sẽ là **MEDIUM**.
*   **Tấn công chiếm đoạt tài khoản (Account Takeover):** Nếu `token` đó có thể được tái sử dụng để xác thực, kẻ tấn công có thể sử dụng nó để đăng nhập vào tài khoản của người dùng hợp pháp.

Tuy nhiên, do `Likelihood` là `LOW` và `Impact` là `MEDIUM`, và ngữ cảnh đang là ứng dụng lab local, tác động thực tế có thể bị giảm thiểu nếu đây chỉ là môi trường thử nghiệm hoặc URL được cấu hình an toàn trong các môi trường khác.

##### 4. Cách khắc phục cụ thể:

1.  **Ưu tiên sử dụng HTTPS:** Đảm bảo rằng `API_URL` luôn được cấu hình để sử dụng giao thức HTTPS cho tất cả các môi trường, đặc biệt là production. Nếu `API_URL` của bạn là một biến môi trường (environment variable), hãy đảm bảo nó được thiết lập đúng với `https://`.
2.  **Kiểm tra định nghĩa `API_URL`:** Xem lại cách biến `API_URL` được định nghĩa trong mã nguồn hoặc thông qua cấu hình ứng dụng. Nếu nó đang trỏ đến `http://localhost` hoặc một địa chỉ IP không có SSL/TLS, hãy cập nhật nó.
3.  **Xem xét mã token:** Xác minh xem `token` được truyền trong header `Authorization` có chứa thông tin nhạy cảm có thể bị lạm dụng hay không. Nếu có, việc sử dụng HTTPS là bắt buộc.

##### 5. Ghi chú cần tester kiểm tra thêm nếu chưa đủ context:

*   **Kiểm tra giá trị `API_URL`:** Tester cần kiểm tra giá trị thực tế của biến `API_URL` trong các cấu hình/môi trường khác nhau (local, staging, production) mà ứng dụng được triển khai.
*   **Xác định tính nhạy cảm của `token`:** Cần hiểu rõ `token` này là loại token gì (ví dụ: JWT, refresh token, session token) và nó được sử dụng để làm gì. Nếu nó là một token truy cập có thể dùng để thực hiện các hành động nhạy cảm, thì lỗ hổng này cần được xem xét nghiêm túc.
*   **Vai trò của `coupon-usage` endpoint:** Endpoint này xử lý thông tin gì? Nó có liên quan đến dữ liệu người dùng nhạy cảm không?
*   **Môi trường `localhost`:** Nếu `localhost` chỉ được sử dụng cho mục đích phát triển và không có dữ liệu nhạy cảm được truyền đi, thì việc tìm thấy này có thể được coi là một cảnh báo thông tin thay vì một lỗ hổng bảo mật nghiêm trọng cho môi trường đó. Tuy nhiên, cần đảm bảo quy tắc này không bị bỏ qua cho các môi trường production.

## Checklist kiểm chứng thủ công

- Xác nhận finding có nằm trong code được chạy/deploy thật hay không.
- Kiểm tra các finding trùng root cause để gom lại khi viết báo cáo cuối.
- Reproduce bằng PoC hoặc runtime request nếu finding phụ thuộc hành vi chạy thật.
- Chỉ chốt `True Positive`, `False Positive`, hoặc `Needs Human Review` sau khi có đủ context.
- Gắn source evidence, log, screenshot hoặc ZAP/Postman evidence nếu có.
