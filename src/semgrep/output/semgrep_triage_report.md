# Báo cáo Semgrep AI Triage

## Tổng quan

- Tổng số finding trong input: 12
- Script đọc toàn bộ mảng `results` từ JSON Semgrep, không hardcode số lượng finding.
- Phân loại của AI là hỗ trợ triage; kết luận cuối cùng vẫn cần tester kiểm chứng.

## Bảng tổng hợp findings

| # | Quy tắc | Tệp | Dòng | Mức độ | CWE | OWASP | Kết quả AI | Trạng thái kiểm chứng |
|---|---|---|---:|---|---|---|---|---|
| 1 | `javascript.jsonwebtoken.security.jwt-hardcode.hardcoded-jwt-secret` | `eshop-sut\backend\server.js` | 51 | WARNING | CWE-798: Use of Hard-coded Credentials | A07:2021 - Identification and Authentication Failures, A07:2025 - Authentication Failures | `findings\001_javascript-jsonwebtoken-security-jwt-hardcode-hardcoded-jwt-secret_ai_output.md` | Cần người kiểm chứng |
| 2 | `javascript.jsonwebtoken.security.jwt-hardcode.hardcoded-jwt-secret` | `eshop-sut\backend\server.js` | 105 | WARNING | CWE-798: Use of Hard-coded Credentials | A07:2021 - Identification and Authentication Failures, A07:2025 - Authentication Failures | `findings\002_javascript-jsonwebtoken-security-jwt-hardcode-hardcoded-jwt-secret_ai_output.md` | Cần người kiểm chứng |
| 3 | `javascript.jsonwebtoken.security.jwt-hardcode.hardcoded-jwt-secret` | `eshop-sut\backend\test_profile.js` | 4 | WARNING | CWE-798: Use of Hard-coded Credentials | A07:2021 - Identification and Authentication Failures, A07:2025 - Authentication Failures | `findings\003_javascript-jsonwebtoken-security-jwt-hardcode-hardcoded-jwt-secret_ai_output.md` | Cần người kiểm chứng |
| 4 | `typescript.react.security.react-insecure-request.react-insecure-request` | `eshop-sut\frontend-mobile\App.js` | 174 | ERROR | CWE-319: Cleartext Transmission of Sensitive Information | A03:2017 - Sensitive Data Exposure, A02:2021 - Cryptographic Failures, A04:2025 - Cryptographic Failures | `findings\004_typescript-react-security-react-insecure-request-react-insecure-request_ai_output.md` | Cần người kiểm chứng |
| 5 | `typescript.react.security.react-insecure-request.react-insecure-request` | `eshop-sut\frontend-mobile\App.js` | 189 | ERROR | CWE-319: Cleartext Transmission of Sensitive Information | A03:2017 - Sensitive Data Exposure, A02:2021 - Cryptographic Failures, A04:2025 - Cryptographic Failures | `findings\005_typescript-react-security-react-insecure-request-react-insecure-request_ai_output.md` | Cần người kiểm chứng |
| 6 | `typescript.react.security.react-insecure-request.react-insecure-request` | `eshop-sut\frontend-mobile\App.js` | 222 | ERROR | CWE-319: Cleartext Transmission of Sensitive Information | A03:2017 - Sensitive Data Exposure, A02:2021 - Cryptographic Failures, A04:2025 - Cryptographic Failures | `findings\006_typescript-react-security-react-insecure-request-react-insecure-request_ai_output.md` | Cần người kiểm chứng |
| 7 | `typescript.react.security.react-insecure-request.react-insecure-request` | `eshop-sut\frontend-mobile\App.js` | 244 | ERROR | CWE-319: Cleartext Transmission of Sensitive Information | A03:2017 - Sensitive Data Exposure, A02:2021 - Cryptographic Failures, A04:2025 - Cryptographic Failures | `findings\007_typescript-react-security-react-insecure-request-react-insecure-request_ai_output.md` | Cần người kiểm chứng |
| 8 | `typescript.react.security.react-insecure-request.react-insecure-request` | `eshop-sut\frontend-mobile\App.js` | 272 | ERROR | CWE-319: Cleartext Transmission of Sensitive Information | A03:2017 - Sensitive Data Exposure, A02:2021 - Cryptographic Failures, A04:2025 - Cryptographic Failures | `findings\008_typescript-react-security-react-insecure-request-react-insecure-request_ai_output.md` | Cần người kiểm chứng |
| 9 | `typescript.react.security.react-insecure-request.react-insecure-request` | `eshop-sut\frontend-mobile\App.js` | 296 | ERROR | CWE-319: Cleartext Transmission of Sensitive Information | A03:2017 - Sensitive Data Exposure, A02:2021 - Cryptographic Failures, A04:2025 - Cryptographic Failures | `findings\009_typescript-react-security-react-insecure-request-react-insecure-request_ai_output.md` | Cần người kiểm chứng |
| 10 | `typescript.react.security.react-insecure-request.react-insecure-request` | `eshop-sut\frontend-mobile\App.js` | 362 | ERROR | CWE-319: Cleartext Transmission of Sensitive Information | A03:2017 - Sensitive Data Exposure, A02:2021 - Cryptographic Failures, A04:2025 - Cryptographic Failures | `findings\010_typescript-react-security-react-insecure-request-react-insecure-request_ai_output.md` | Cần người kiểm chứng |
| 11 | `typescript.react.security.react-insecure-request.react-insecure-request` | `eshop-sut\frontend-mobile\App.js` | 384 | ERROR | CWE-319: Cleartext Transmission of Sensitive Information | A03:2017 - Sensitive Data Exposure, A02:2021 - Cryptographic Failures, A04:2025 - Cryptographic Failures | `findings\011_typescript-react-security-react-insecure-request-react-insecure-request_ai_output.md` | Cần người kiểm chứng |
| 12 | `typescript.react.security.react-insecure-request.react-insecure-request` | `eshop-sut\frontend-mobile\App.js` | 400 | ERROR | CWE-319: Cleartext Transmission of Sensitive Information | A03:2017 - Sensitive Data Exposure, A02:2021 - Cryptographic Failures, A04:2025 - Cryptographic Failures | `findings\012_typescript-react-security-react-insecure-request-react-insecure-request_ai_output.md` | Cần người kiểm chứng |

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
- File: `eshop-sut\backend\server.js`
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

#### Postman/PoC tự động
- Mục tiêu test: Kiểm tra backend có chấp nhận JWT giả được ký bằng hardcoded secret hay không.
- Feature ảnh hưởng: Xác thực JWT / phân quyền admin
- Method: `GET`
- URL: `http://localhost:3000/api/users/me`
- Độ tin cậy mapping: Medium
- Ghi chú mapping: Endpoint được suy luận từ cách backend verify JWT, cần xác nhận khi test.

Headers:
```http
Authorization: Bearer <forged_admin_jwt>
Content-Type: application/json
```

Payload:
Không có request body.

- Nguồn payload: Suy luận từ HTTP method không sử dụng request body.
- Độ tin cậy payload: High

Pre-test setup:
```text
1. Dùng `src/semgrep/exploit.js` để tạo JWT giả.
2. Copy token sinh ra vào header Authorization.
3. Đảm bảo backend EShop đang chạy tại port 3000.
```

Kết quả kỳ vọng:
- Nếu còn lỗi: Server trả `200 OK` và chấp nhận token giả.
- Nếu đã an toàn: Server trả `401 Unauthorized` hoặc `403 Forbidden`.

#### Phân tích AI
Tuyệt vời! Với vai trò chuyên gia bảo mật ứng dụng, tôi sẽ tiến hành triage finding SEMGREP-001 này.

---

##### Triage Finding: SEMGREP-001

**1. Phân loại:** True Positive

**2. Lý do phân loại dựa trên source evidence:**

*   **Khớp Rule ID và Mô tả:** Rule `javascript.jsonwebtoken.security.jwt-hardcode.hardcoded-jwt-secret` rõ ràng chỉ ra việc sử dụng một chuỗi bí mật (secret) được nhúng trực tiếp vào mã nguồn, điều này hoàn toàn phù hợp với dòng 51 trong `server.js`: `const token = jwt.sign({ id: user.id, role: user.role }, SECRET_KEY);`. Biến `SECRET_KEY` có khả năng cao là một chuỗi cố định được định nghĩa ở đâu đó trong file hoặc import từ một module hardcode khác, không qua cấu hình hoặc biến môi trường.
*   **Ngữ cảnh file:** File `server.js` được xác định là `entrypoint runtime backend`. Điều này có nghĩa là đoạn mã này sẽ được thực thi khi server backend khởi chạy và hoạt động, tức là nó là một phần của logic xử lý chính của ứng dụng.
*   **CWE và OWASP:** Việc nhúng cứng bí mật (CWE-798) trực tiếp liên quan đến lỗ hổng A07:2021/A07:2025 (Identification and Authentication Failures/Authentication Failures) vì bí mật này có thể bị lộ và làm suy yếu cơ chế xác thực và ủy quyền của ứng dụng (ví dụ: cho phép kẻ tấn công giả mạo token).
*   **Nguyên tắc SAST:** Dựa trên bằng chứng mã nguồn tĩnh, việc tìm thấy `SECRET_KEY` được sử dụng trực tiếp trong quá trình ký JWT là một dấu hiệu rõ ràng của việc lưu trữ mã thông báo bí mật không an toàn. Semgrep phát hiện một mã nguồn lỗi có thể đạt được trong runtime.

**3. Tác động thực tế trong bối cảnh EShop:**

*   **Rò rỉ bí mật:** Nếu mã nguồn này bị lộ cho kẻ tấn công (ví dụ: thông qua một lỗ hổng khác, truy cập trái phép vào kho mã nguồn, hoặc do vô tình chia sẻ), kẻ tấn công sẽ có được `SECRET_KEY`.
*   **Giả mạo Token:** Với `SECRET_KEY` đã biết, kẻ tấn công có thể tạo ra các JSON Web Token (JWT) hợp lệ cho bất kỳ người dùng nào, hoặc sửa đổi các thông tin trong token hiện có (như `role`, `id`). Điều này cho phép họ thực hiện các hành động với quyền của người dùng đó, bao gồm:
    *   Bỏ qua quy trình đăng nhập.
    *   Truy cập vào các tài khoản người dùng khác.
    *   Thực hiện các hành động quản trị (nếu `role` là admin).
*   **Tác động từ "lab local":** Mặc dù EShop đang quét như một ứng dụng lab local, việc tìm thấy lỗ hổng bảo mật "nghiêm trọng" như thế này tại bước đầu tiên cũng là lý do cần cảnh giác. Nếu sau này ứng dụng được triển khai lên môi trường production, lỗ hổng này sẽ trở thành một mối đe dọa thực sự, ngay cả khi nó chỉ đơn giản là do dev/lab chưa cập nhật cấu hình.

**4. Cách khắc phục cụ thể:**

*   **Thay thế bằng Biến Môi Trường:**
    *   Loại bỏ `SECRET_KEY` khỏi mã nguồn.
    *   Trong `server.js` hoặc một file cấu hình tương ứng, thay thế dòng khai báo `SECRET_KEY` bằng cách đọc giá trị từ biến môi trường. Ví dụ:
        ```javascript
        const SECRET_KEY = process.env.JWT_SECRET;
        ```
    *   Đảm bảo rằng biến môi trường `JWT_SECRET` được thiết lập an toàn trên môi trường triển khai (server, container, dịch vụ cloud).
*   **Sử dụng Hệ thống Quản lý Bí mật (Secret Management System):**
    *   Đối với môi trường production, nên cân nhắc tích hợp với các hệ thống quản lý bí mật chuyên dụng như HashiCorp Vault, AWS Secrets Manager, Azure Key Vault, hoặc sử dụng Hardware Security Module (HSM) nếu yêu cầu bảo mật cao.
    *   Mã ứng dụng sẽ truy vấn bí mật này từ dịch vụ quản lý bí mật trong runtime.

**5. Ghi chú cần tester kiểm tra thêm nếu chưa đủ context:**

*   **Xác định nguồn gốc `SECRET_KEY`:** Tester cần kiểm tra xem `SECRET_KEY` được định nghĩa ở đâu trong mã nguồn. Nó có thể được định nghĩa trực tiếp trong file `server.js`, hoặc được import từ một file cấu hình khác được *nhúng cứng* vào ứng dụng. Nếu nó import từ một file cấu hình, cần kiểm tra file đó xem có phải cũng bị nhúng cứng bí mật hay không.
*   **Kiểm tra cấu hình hệ thống:** Khi triển khai demo hoặc lab, liệu có cách nào để thiết lập biến môi trường `JWT_SECRET` mà không cần sửa đổi mã nguồn không? (Dù vậy, việc tìm thấy nó trong source vẫn là một vấn đề cần ưu tiên khắc phục).
*   **Vai trò của file:** Với thông tin "entrypoint runtime backend", có thể khẳng định đây là mã chạy trong production. Tuy nhiên, nếu có bất kỳ tình huống nào mà file này chỉ dùng cho mục đích test đơn lẻ và *tuyệt đối không bao giờ* được deploy, thì việc phân loại có thể xem xét lại. Tuy nhiên, theo quy tắc, là "entrypoint runtime" thì mặc định là có thể được deploy.

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
- File: `eshop-sut\backend\server.js`
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

#### Postman/PoC tự động
- Mục tiêu test: Kiểm tra backend có chấp nhận JWT giả được ký bằng hardcoded secret hay không.
- Feature ảnh hưởng: Xác thực JWT / phân quyền admin
- Method: `GET`
- URL: `http://localhost:3000/api/users/me`
- Độ tin cậy mapping: Medium
- Ghi chú mapping: Endpoint được suy luận từ cách backend verify JWT, cần xác nhận khi test.

Headers:
```http
Authorization: Bearer <forged_admin_jwt>
Content-Type: application/json
```

Payload:
Không có request body.

- Nguồn payload: Suy luận từ HTTP method không sử dụng request body.
- Độ tin cậy payload: High

Pre-test setup:
```text
1. Dùng `src/semgrep/exploit.js` để tạo JWT giả.
2. Copy token sinh ra vào header Authorization.
3. Đảm bảo backend EShop đang chạy tại port 3000.
```

Kết quả kỳ vọng:
- Nếu còn lỗi: Server trả `200 OK` và chấp nhận token giả.
- Nếu đã an toàn: Server trả `401 Unauthorized` hoặc `403 Forbidden`.

#### Phân tích AI
Tuyệt vời! Với vai trò là chuyên gia bảo mật ứng dụng, tôi sẽ tiến hành Triage cho finding SEMGREP-002 này.

##### Triage Finding Bảo Mật: SEMGREP-002

##### 1. Phân loại: NEEDS HUMAN REVIEW

##### 2. Lý do phân loại dựa trên source evidence:

*   **Mã nguồn minh chứng:** Dòng 105 của file `eshop-sut\backend\server.js` hiển thị `jwt.verify(token, SECRET_KEY, (err, user) => { ... });`. Rõ ràng là một biến `SECRET_KEY` đang được sử dụng trực tiếp để xác minh (verify) token JWT.
*   **Nguyên tắc của Rule:** Rule `javascript.jsonwebtoken.security.jwt-hardcode.hardcoded-jwt-secret` được thiết kế để cảnh báo về việc lưu trữ các thông tin nhạy cảm (credentials) trực tiếp trong mã nguồn. Điều này vi phạm nguyên tắc bảo mật cơ bản, vì bất kỳ ai có quyền truy cập vào mã nguồn đều có thể lấy cắp secret này.
*   **Context của ứng dụng:** EShop đang được quét như là một ứng dụng lab local. Điều này đặt ra câu hỏi về ngữ cảnh sử dụng thực tế của `SECRET_KEY`. Nếu đây là biến được định nghĩa ở một file cấu hình khác, hoặc được inject từ biến môi trường *trước khi* chạy `server.js`, thì việc Semgrep phát hiện ra nó ở đây có thể là một cảnh báo giả (False Positive) hoặc cần xem xét thêm. Tuy nhiên, nếu `SECRET_KEY` được định nghĩa trực tiếp trong `server.js` hoặc một file khác không được quản lý an toàn, thì đây là một lỗ hổng nghiêm trọng.
*   **Thiếu thông tin về `SECRET_KEY`:** Dựa trên đoạn mã được cung cấp, chúng ta không thấy định nghĩa của `SECRET_KEY`. Việc không có định nghĩa này trong context hiển thị làm tăng sự không chắc chắn.

Do đó, chúng ta cần thêm thông tin để xác nhận xem `SECRET_KEY` có thực sự được hard-coded trong mã nguồn hay không và vai trò của nó trong ngữ cảnh deploy thực tế của EShop.

##### 3. Tác động thực tế trong bối cảnh EShop:

Nếu `SECRET_KEY` thực sự được hard-coded và có thể bị lộ, tác động có thể rất nghiêm trọng:

*   **Giả mạo token:** Kẻ tấn công có thể sử dụng `SECRET_KEY` bị lộ để tạo ra các token JWT giả mạo có hiệu lực thay mặt cho bất kỳ người dùng nào, bao gồm cả người dùng quản trị.
*   **Truy cập trái phép:** Với token giả mạo, kẻ tấn công có thể vượt qua cơ chế xác thực và truy cập vào các tài nguyên nhạy cảm hoặc thực hiện các hành động mà họ không có quyền.
*   **Tiếm đoạt tài khoản:** Trong trường hợp xấu nhất, kẻ tấn công có thể hoàn toàn chiếm quyền kiểm soát tài khoản người dùng.

Tuy nhiên, vì đây là ứng dụng lab local, mức độ rủi ro *hiện tại* có thể bị giảm nhẹ nếu nó không được triển khai ra môi trường production. Nhưng nguyên tắc bảo mật vẫn cần được tuân thủ.

##### 4. Cách khắc phục cụ thể:

*   **Sử dụng Biến Môi Trường (Environment Variables):** Đây là phương pháp được khuyến nghị. Thay vì hard-code `SECRET_KEY` trong mã nguồn, hãy lưu trữ nó dưới dạng biến môi trường trên server. Sau đó, ứng dụng của bạn sẽ đọc giá trị này từ biến môi trường khi khởi động.
    *   Ví dụ (trong Node.js):
        ```javascript
        const SECRET_KEY = process.env.JWT_SECRET_KEY;
        if (!SECRET_KEY) {
            console.error("JWT_SECRET_KEY is not set. Please set it in your environment variables.");
            process.exit(1); // Thoát ứng dụng nếu secret chưa được cấu hình
        }
        // ... sau đó sử dụng SECRET_KEY
        jwt.verify(token, SECRET_KEY, ...);
        ```
*   **Sử dụng Hệ Thống Quản Lý Bí Mật (Secrets Management System):** Đối với các ứng dụng phức tạp hơn hoặc trong môi trường production, nên sử dụng các giải pháp chuyên dụng như HashiCorp Vault, AWS Secrets Manager, hoặc Azure Key Vault để lưu trữ và quản lý các bí mật.
*   **Kiểm tra việc định nghĩa `SECRET_KEY`:** Quan trọng nhất là phải xác định *chính xác* `SECRET_KEY` đang được định nghĩa ở đâu. Nếu nó được định nghĩa ở một file cấu hình hoặc được inject từ biến môi trường, thì Semgrep có thể đang đưa ra một cảnh báo không phù hợp hoặc cần phải cấu hình Semgrep để bỏ qua những trường hợp đó (nếu đó là một trường hợp được chấp nhận).

##### 5. Ghi chú cần tester kiểm tra thêm nếu chưa đủ context:

*   **Xác định vị trí định nghĩa `SECRET_KEY`:** Tester cần truy tìm nguồn gốc của biến `SECRET_KEY`. Nó có được định nghĩa trực tiếp trong `server.js` không? Hay nó được import từ một file cấu hình khác? Hay nó được truyền vào thông qua biến môi trường khi ứng dụng khởi chạy?
*   **Kiểm tra cách deploy:** Tìm hiểu xem trong môi trường lab local, `SECRET_KEY` này có được thiết lập thông qua biến môi trường hay không. Điều này sẽ giúp xác định liệu Semgrep báo đúng hay sai.
*   **Đánh giá độ nhạy cảm của file:** Mặc dù `server.js` là entrypoint runtime, việc xác định liệu nó có được deploy dưới dạng code tĩnh (e.g., trong một package có thể truy cập được) hay không cũng quan trọng.

Chỉ khi có đầy đủ các thông tin trên, chúng ta mới có thể đưa ra phân loại cuối cùng là True Positive, False Positive, hoặc giữ nguyên là Needs Human Review.

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
- File: `eshop-sut\backend\test_profile.js`
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

#### Postman/PoC tự động
- Mục tiêu test: Kiểm tra backend có chấp nhận JWT giả được ký bằng hardcoded secret hay không.
- Feature ảnh hưởng: Xác thực JWT / phân quyền admin
- Method: `GET`
- URL: `http://localhost:3000/api/users/me`
- Độ tin cậy mapping: Medium
- Ghi chú mapping: Endpoint được suy luận từ cách backend verify JWT, cần xác nhận khi test.

Headers:
```http
Authorization: Bearer <forged_admin_jwt>
Content-Type: application/json
```

Payload:
Không có request body.

- Nguồn payload: Suy luận từ HTTP method không sử dụng request body.
- Độ tin cậy payload: High

Pre-test setup:
```text
1. Dùng `src/semgrep/exploit.js` để tạo JWT giả.
2. Copy token sinh ra vào header Authorization.
3. Đảm bảo backend EShop đang chạy tại port 3000.
```

Kết quả kỳ vọng:
- Nếu còn lỗi: Server trả `200 OK` và chấp nhận token giả.
- Nếu đã an toàn: Server trả `401 Unauthorized` hoặc `403 Forbidden`.

#### Phân tích AI
##### Triage Finding Bảo mật SEMGREP-003

##### 1. Phân loại: False Positive

##### 2. Lý do phân loại dựa trên source evidence

*   **Vai trò của file:** Dựa trên ngữ cảnh `test_profile.js`, file này rõ ràng là một đoạn mã được sử dụng cho mục đích *testing* hoặc *helper script* trong môi trường phát triển cục bộ.
*   **Mật khẩu cứng:** Mặc dù `super_secret_key_that_should_not_be_here` là một secret được mã hóa cứng và vi phạm nguyên tắc chung về bảo mật (CWE-798, OWASP A07:2021), nhưng việc nó xuất hiện trong một file test không trực tiếp gây ra rủi ro bảo mật cho *ứng dụng EShop đang chạy ở môi trường production* nếu file này không được deploy hoặc sử dụng trong pipeline CI/CD của production.
*   **Endpoint HTTP cục bộ:** Lệnh gọi `axios.get('http://localhost:3000/api/users/me')` chỉ ra rằng đoạn mã này tương tác với một service chạy trên `localhost`. Điều này càng khẳng định tính chất cục bộ và dành cho mục đích thử nghiệm của file. Secret `super_secret_key_that_should_not_be_here` chỉ được sử dụng để tạo token cho việc gọi API nội bộ này trong môi trường test, không phải là secret dùng để ký các JWT xác thực phiên làm việc thực tế của người dùng với production server.

##### 3. Tác động thực tế trong bối cảnh EShop

Trong bối cảnh của một ứng dụng lab local như EShop đang được quét, việc phát hiện secret cứng trong file test không tạo ra tác động bảo mật trực tiếp đến **production environment** của EShop. Tuy nhiên, nó cho thấy một thói quen mã hóa không tốt và cần được chấn chỉnh để tránh rủi ro tiềm ẩn nếu file này vô tình bị đưa vào các môi trường nhạy cảm hơn. Rủi ro chính sẽ là nếu mã này, hoặc cách tạo token này, bị lặp lại hoặc sử dụng trong mã nguồn production mà không có sự thay đổi.

##### 4. Cách khắc phục cụ thể

Mặc dù phân loại là False Positive trong bối cảnh hiện tại, các bước sau đây nên được thực hiện để cải thiện chất lượng mã và ngăn ngừa rủi ro tái diễn:

*   **Xóa hoặc cập nhật mã test:** Nếu đoạn mã này không còn cần thiết cho việc test (ví dụ: một test cũ đã được thay thế), hãy xóa nó. Nếu nó vẫn cần thiết, hãy thay thế khóa bí mật cứng bằng một biến môi trường hoặc một cách quản lý secret an toàn hơn, ngay cả trong môi trường test. Ví dụ, sử dụng `process.env.JWT_SECRET_TEST` thay vì `'super_secret_key_that_should_not_be_here'`.
*   **Cập nhật quy tắc trong Semgrep (tùy chọn):** Nếu bạn muốn Semgrep thông minh hơn trong việc phân biệt mã test và mã production, bạn có thể xem xét việc tinh chỉnh rule để nó ít nhạy cảm hơn với các file có tên hoặc vị trí cụ thể (ví dụ: nằm trong thư mục `test/` hoặc có tên kết thúc bằng `_test.js`). Tuy nhiên, điều này cần được thực hiện cẩn thận để không bỏ sót các lỗ hổng thực sự.
*   **Giáo dục đội ngũ phát triển:** Tăng cường nhận thức về tầm quan trọng của việc không mã hóa cứng secret trong bất kỳ ngữ cảnh nào, bao gồm cả mã test, để ngăn ngừa các vấn đề bảo mật tương tự trong tương lai.

##### 5. Ghi chú cần tester kiểm tra thêm nếu chưa đủ context

*   **Xác nhận môi trường deploy:** Tester cần xác nhận rằng file `test_profile.js` **không bao giờ** được deploy cùng với ứng dụng EShop lên môi trường production hoặc staging.
*   **Kiểm tra vai trò thực tế của token:** Mặc dù evidence cho thấy đây là token tạo cho mục đích test (ký với secret cứng và dùng cho `localhost`), tester nên kiểm tra xem có bất kỳ logic nào khác trong EShop có thể vô tình sử dụng secret `super_secret_key_that_should_not_be_here` để ký hoặc xác minh các token thực sự của ứng dụng hay không. Điều này bao gồm việc quét toàn bộ codebase cho việc sử dụng của biến hoặc chuỗi `'super_secret_key_that_should_not_be_here'`.
*   **Kiểm tra pipeline CI/CD:** Đảm bảo rằng file `test_profile.js` không được bao gồm trong bất kỳ artifact hoặc bước nào của pipeline CI/CD có thể dẫn đến việc nó bị triển khai hoặc tiết lộ.

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
- File: `eshop-sut\frontend-mobile\App.js`
- Dòng: 174
- Trạng thái kiểm chứng: Needs Human Review

#### Bằng chứng mã nguồn
```text
   159:   };
   160:
   161:   const logout = () => {
   162:     setToken("");
   163:     setUser(null);
   164:     setName("");
   165:     setPhone("");
   166:     setShippingAddress("");
   167:     setOrders([]);
   168:     goHome();
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
   180:     } catch (error) {
   181:       console.error("Lỗi lấy đơn hàng:", error);
   182:       setOrders([]);
   183:     }
   184:   };
   185:
   186:   const handleLogin = async () => {
   187:     setLoginError("");
   188:     try {
   189:       const response = await fetch(`${API_URL}/login`, {
```

#### Postman/PoC tự động
- Mục tiêu test: Kiểm tra request đang dùng HTTP cleartext thay vì HTTPS.
- Feature ảnh hưởng: Bảo mật truyền tải frontend/API
- Method: `GET`
- URL: `http://localhost:3000/api/orders/my-orders`
- Độ tin cậy mapping: High
- Ghi chú mapping: Endpoint được trích từ source snippet nếu có; nếu thiếu path cần reviewer map thủ công.

Headers:
```http
Content-Type: application/json
```

Payload:
Không có request body.

- Nguồn payload: Suy luận từ HTTP method không sử dụng request body.
- Độ tin cậy payload: High

Pre-test setup:
```text
1. Mở source line được Semgrep báo để xác nhận API path.
2. Đảm bảo backend/frontend local đang chạy.
3. Gửi request bằng Postman và ghi nhận URL đang dùng HTTP.
```

Kết quả kỳ vọng:
- Nếu còn lỗi: Request gọi thành công qua `http://` hoặc dữ liệu nhạy cảm đi qua kênh không mã hóa.
- Nếu đã an toàn: Ứng dụng dùng `https://` hoặc cấu hình base URL an toàn theo môi trường.

#### Phân tích AI
Tuyệt vời, tôi sẽ đóng vai trò chuyên gia bảo mật ứng dụng để phân tích finding này. Dưới đây là kết quả triage của tôi:

##### Triage Finding SEMGREP-004

* **Mã finding:** SEMGREP-004
* **Rule ID:** typescript.react.security.react-insecure-request.react-insecure-request
* **File nguồn:** eshop-sut\frontend-mobile\App.js
* **Dòng:** 174
* **Severity:** ERROR
* **CWE:** CWE-319: Cleartext Transmission of Sensitive Information
* **OWASP:** A03:2017 - Sensitive Data Exposure, A02:2021 - Cryptographic Failures, A04:2025 - Cryptographic Failures
* **Likelihood:** LOW
* **Impact:** MEDIUM
* **Confidence:** MEDIUM
* **Cảnh báo Semgrep:** Unencrypted request over HTTP detected.

---

##### 1. Phân loại:

Needs Human Review

##### 2. Lý do phân loại dựa trên source evidence:

Bằng chứng mã nguồn cho thấy dòng 174:
```typescript
const response = await fetch(`${API_URL}/orders/my-orders`, {
```
Trong đó `API_URL` được định nghĩa ở đâu đó (không hiển thị trong đoạn trích) và được sử dụng để tạo một yêu cầu HTTP. Rule Semgrep phát hiện rằng việc sử dụng giao thức HTTP (không phải HTTPS) có thể dẫn đến việc truyền tải thông tin nhạy cảm dưới dạng văn bản rõ ràng (cleartext), điều này được chỉ ra bởi thông tin về CWE và OWASP.

Tuy nhiên, để đưa ra kết luận cuối cùng, chúng ta cần xem xét ngữ cảnh triển khai và cách `API_URL` được cấu hình:

*   **Ngữ cảnh Lab/Local:** Thông báo "EShop đang được quét như ứng dụng lab local; finding liên quan localhost cần kiểm tra môi trường trước khi kết luận rủi ro cuối." là rất quan trọng. Nếu `API_URL` trỏ đến `localhost` hoặc một địa chỉ IP nội bộ trong môi trường phát triển/thử nghiệm, thì rủi ro truyền tải dữ liệu nhạy cảm qua mạng công cộng có thể không tồn tại. Giao tiếp giữa frontend và backend trong cùng một môi trường local thường không qua mạng không tin cậy.
*   **Cấu hình API_URL:** Việc xác định giá trị thực tế của `API_URL` là cực kỳ cần thiết. Nếu `API_URL` luôn được cấu hình để sử dụng HTTPS trong môi trường production, thì finding này có thể là **False Positive**. Ngược lại, nếu `API_URL` có thể cấu hình để sử dụng HTTP trong môi trường production, hoặc nếu có khả năng người dùng có thể truy cập ứng dụng qua HTTP, thì đây là một **True Positive**.

##### 3. Tác động thực tế trong bối cảnh EShop:

Nếu `API_URL` trỏ đến một máy chủ mà yêu cầu được gửi qua HTTP (không phải HTTPS) **trong một môi trường mà dữ liệu có thể bị giám sát (ví dụ: mạng công cộng, mạng Wi-Fi không an toàn)**, thì thông tin như `currentToken` (được gửi trong header Authorization) và dữ liệu đơn hàng có thể bị lộ. Điều này có thể dẫn đến:

*   **Chiếm đoạt tài khoản:** Kẻ tấn công có thể đánh cắp "currentToken" và mạo danh người dùng để thực hiện các hành động trái phép.
*   **Lộ thông tin cá nhân:** Thông tin chi tiết về đơn hàng, địa chỉ giao hàng, v.v. có thể bị truy cập.

Tuy nhiên, trong bối cảnh là ứng dụng lab local, tác động này có thể được giảm thiểu đáng kể nếu không có ai khác truy cập vào môi trường lab đó.

##### 4. Cách khắc phục cụ thể:

Cách khắc phục mạnh mẽ nhất và khuyến nghị là **luôn luôn sử dụng HTTPS cho tất cả các yêu cầu API, bất kể môi trường phát triển hay production.**

Các bước cụ thể:

1.  **Cấu hình Server/Backend:** Đảm bảo rằng backend API của EShop luôn được truy cập thông qua HTTPS.
2.  **Cấu hình Frontend (nếu cần):**
    *   Kiểm tra cách `API_URL` được khởi tạo. Nếu nó được định nghĩa tĩnh trong code, hãy đảm bảo nó bắt đầu bằng `https://`.
    *   Nếu `API_URL` được cấu hình từ một file `.env` hoặc biến môi trường, hãy đảm bảo các giá trị này được đặt thành HTTPS cho môi trường production.
    *   Sửa đổi dòng 174 và các lệnh gọi `fetch` khác (như dòng 189) để luôn sử dụng URL có HTTPS. Ví dụ:
        ```typescript
        // Giả định API_URL có thể được định nghĩa lại hoặc kiểm tra
        const secureApiUrl = API_URL.startsWith('http://') ? API_URL.replace('http://', 'https://') : API_URL;
        const response = await fetch(`${secureApiUrl}/orders/my-orders`, {
            // ...
        });
        ```
        Hoặc tốt hơn nữa, nếu `API_URL` là miền (`domain.com`), hãy đảm bảo bạn sử dụng `https://domain.com`.

##### 5. Ghi chú cần tester kiểm tra thêm nếu chưa đủ context:

Để hoàn thành việc triage này, tôi cần tester kiểm tra và cung cấp thông tin chi tiết về các điểm sau:

*   **Giá trị thực tế của `API_URL`:** Tester cần xác định giá trị được sử dụng bởi `API_URL` trong **môi trường mà EShop đang chạy (lab local)**.
*   **Cấu hình triển khai production:** Nếu có thể, hãy cung cấp thông tin về cách EShop (frontend mobile) và API backend của nó được **triển khai trong môi trường production**. `API_URL` có được cấu hình luôn là HTTPS trong production không?
*   **Mục đích của việc sử dụng HTTP trong lab:** Nếu việc sử dụng HTTP cho `API_URL` trong lab là có chủ đích (ví dụ: do hạn chế của môi trường lab, hoặc các server API lab không hỗ trợ HTTPS), tester cần xác nhận rằng **không có dữ liệu nhạy cảm** nào khác được xử lý qua kết nối HTTP này, hoặc rằng việc này chỉ là tạm thời và sẽ không bao giờ xảy ra trong production.
*   **Các Request khác:** Có thể có các request khác trong ứng dụng cũng sử dụng `API_URL` với HTTP. Kiểm tra xem có các finding tương tự với các `fetch` call khác trong codebase không.

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
- File: `eshop-sut\frontend-mobile\App.js`
- Dòng: 189
- Trạng thái kiểm chứng: Needs Human Review

#### Bằng chứng mã nguồn
```text
   174:       const response = await fetch(`${API_URL}/orders/my-orders`, {
   175:         headers: { Authorization: `Bearer ${currentToken}` },
   176:       });
   177:       const data = await response.json();
   178:       const parsedOrders = Array.isArray(data) ? data : data.orders || [];
   179:       setOrders(parsedOrders);
   180:     } catch (error) {
   181:       console.error("Lỗi lấy đơn hàng:", error);
   182:       setOrders([]);
   183:     }
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
   195:       if (!response.ok) throw new Error(data.error || "Đăng nhập thất bại.");
   196:
   197:       setToken(data.token);
   198:       setUser(data.user);
   199:       setName(data.user?.name || "");
   200:       setPhone(data.user?.phone || "");
   201:       setShippingAddress(data.user?.shipping_address || "");
   202:       fetchOrders(data.token);
   203:       goHome();
   204:     } catch (error) {
```

#### Postman/PoC tự động
- Mục tiêu test: Kiểm tra request đang dùng HTTP cleartext thay vì HTTPS.
- Feature ảnh hưởng: Bảo mật truyền tải frontend/API
- Method: `POST`
- URL: `http://localhost:3000/api/login`
- Độ tin cậy mapping: High
- Ghi chú mapping: Endpoint được trích từ source snippet nếu có; nếu thiếu path cần reviewer map thủ công.

Headers:
```http
Content-Type: application/json
```

Payload mẫu:
```json
{
  "email": "{{test_email}}",
  "password": "{{test_password}}"
}
```

- Nguồn payload: Tự động suy luận từ `body: JSON.stringify(...)` trong source.
- Độ tin cậy payload: High
- Thay các biến `{{...}}` bằng giá trị Postman environment trước khi chạy PoC.

Pre-test setup:
```text
1. Mở source line được Semgrep báo để xác nhận API path.
2. Đảm bảo backend/frontend local đang chạy.
3. Gửi request bằng Postman và ghi nhận URL đang dùng HTTP.
```

Kết quả kỳ vọng:
- Nếu còn lỗi: Request gọi thành công qua `http://` hoặc dữ liệu nhạy cảm đi qua kênh không mã hóa.
- Nếu đã an toàn: Ứng dụng dùng `https://` hoặc cấu hình base URL an toàn theo môi trường.

#### Phân tích AI
Tuyệt vời! Dưới đây là kết quả triage cho finding SEMGREP-005 dưới vai trò chuyên gia bảo mật ứng dụng:

---

##### **Triage Finding Bảo Mật**

**1. Phân loại:** Needs Human Review

**2. Lý do phân loại dựa trên source evidence:**

Semgrep đã phát hiện việc sử dụng `fetch` để thực hiện các yêu cầu mạng đến `${API_URL}/orders/my-orders` và `${API_URL}/login` (dòng 174 và 189). Rule này cảnh báo về việc truyền dữ liệu nhạy cảm qua HTTP không được mã hóa (CWE-319). Tuy nhiên, điểm mấu chốt nằm ở cách sử dụng biến `${API_URL}`.

*   **Ngữ cảnh biến `${API_URL}`:** Bằng chứng mã nguồn cho thấy `${API_URL}` là một biến môi trường hoặc hằng số được định nghĩa ở đâu đó trong project. Nếu `${API_URL}` được cấu hình trỏ đến `http://localhost:<port>` hoặc một địa chỉ IP nội bộ trong môi trường phát triển/testing, thì việc sử dụng HTTP có thể chấp nhận được và không phải là lỗ hổng bảo mật trong bối cảnh đó.
*   **Thiếu ngữ cảnh về môi trường deploy:** Chúng ta không có thông tin về cách biến `${API_URL}` được định nghĩa và cách ứng dụng này sẽ được deploy. Nếu `${API_URL}` được cấu hình để trỏ đến một dịch vụ backend bên ngoài thông qua HTTP trong môi trường production, đây sẽ là một lỗ hổng nghiêm trọng.
*   **Độ nhạy cảm của dữ liệu gửi qua API:**
    *   Yêu cầu `/orders/my-orders` có thể trả về thông tin đơn hàng, bao gồm chi tiết sản phẩm, địa chỉ giao hàng, v.v.
    *   Yêu cầu `/login` gửi thông tin đăng nhập (email, password) và nhận về token, thông tin người dùng. Đây là những dữ liệu cực kỳ nhạy cảm.

Do Semgrep chỉ phân tích mã tĩnh và không có đủ ngữ cảnh về môi trường chạy thực tế của `${API_URL}`, chúng ta cần thêm thông tin để xác định liệu đây có phải là True Positive (lỗ hổng có thật) hay False Positive (không phải lỗ hổng trong bối cảnh deploy).

**3. Tác động thực tế trong bối cảnh EShop:**

*   **Nếu API_URL là HTTP trong production:**
    *   **A03:2017 - Sensitive Data Exposure / A02:2021 - Cryptographic Failures / A04:2025 - Cryptographic Failures:** Kẻ tấn công có thể nghe lén lưu lượng mạng để đánh cắp thông tin đăng nhập, token xác thực, và chi tiết đơn hàng. Điều này có thể dẫn đến việc chiếm đoạt tài khoản người dùng, thực hiện các giao dịch trái phép, lộ thông tin cá nhân của người dùng. Tác động này là **MEDIUM** đến **HIGH** tùy thuộc vào mức độ nhạy cảm của dữ liệu giao dịch.
*   **Nếu API_URL là HTTP trong môi trường dev/lab (ví dụ: localhost):**
    *   Rủi ro thấp hơn nhiều vì chỉ có thể bị tấn công bởi kẻ tấn công có quyền truy cập mạng cục bộ và có ý đồ xấu. Tuy nhiên, vẫn có thể là một thói quen code không tốt nếu không được xử lý khi deploy lên production.

**4. Cách khắc phục cụ thể:**

Đảm bảo tất cả các yêu cầu mạng đến backend đều sử dụng HTTPS.

1.  **Cấu hình môi trường:**
    *   **Kiểm tra định nghĩa `${API_URL}`:** Tìm file hoặc biến môi trường nơi `${API_URL}` được khởi tạo.
    *   **Đối với môi trường production:** Luôn cấu hình `${API_URL}` để trỏ đến một điểm cuối sử dụng HTTPS (ví dụ: `https://api.eshop.com`).
    *   **Đối với môi trường phát triển/dev/lab:** Nếu phát triển trên localhost, việc sử dụng `http://localhost:<port>` có thể tạm chấp nhận được cho mục đích thử nghiệm, nhưng cần có cơ chế để đảm bảo tự động chuyển sang HTTPS khi deploy lên staging hoặc production. Có thể sử dụng biến môi trường `NODE_ENV` hoặc một biến cấu hình riêng để phân biệt.

2.  **Cập nhật mã nguồn (nếu cần thiết):**
    *   Nếu rule Semgrep vẫn báo dù đã cấu hình HTTPS ở API URL, có thể do một số phần khác của ứng dụng chưa được xử lý. Tuy nhiên, trong trường hợp này, vấn đề chính là cấu hình biến `${API_URL}`.
    *   **Ví dụ minh họa cách xử lý linh hoạt biến API_URL (trong một file cấu hình hoặc file .env):**
        ```javascript
        // Ví dụ trong file cấu hình config.js hoặc tương tự
        const API_URL = process.env.NODE_ENV === 'production'
          ? 'https://api.your-eshop.com'
          : 'http://localhost:3000'; // Hoặc cấu hình HTTPS cho local dev nếu có
        ```

**5. Ghi chú cần tester kiểm tra thêm:**

*   **Xác định giá trị thực tế của `${API_URL}`:** Tester cần điều tra cách biến `${API_URL}` được định nghĩa trong dự án. Có thể kiểm tra các file cấu hình, biến môi trường, hoặc file `.env`.
*   **Chuyển đổi sang HTTPS:** Yêu cầu backend API của EShop hỗ trợ HTTPS và đảm bảo rằng môi trường deploy production luôn trỏ `${API_URL}` đến phiên bản HTTPS của API.
*   **Môi trường Lab/Local:** Nếu EShop chỉ là ứng dụng lab chạy lokal, hãy xác nhận rằng việc sử dụng HTTP ở localhost là cố ý và không ảnh hưởng đến các phiên bản deploy khác. Tuy nhiên, vẫn khuyến khích phát triển với tư duy bảo mật và sử dụng HTTPS cho localhost nếu có thể.

---

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
- File: `eshop-sut\frontend-mobile\App.js`
- Dòng: 222
- Trạng thái kiểm chứng: Needs Human Review

#### Bằng chứng mã nguồn
```text
   207:   };
   208:
   209:   const handleRegister = async () => {
   210:     setRegisterError("");
   211:     const strongPasswordRegex =
   212:       /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z\d]).{8,}$/;
   213:
   214:     if (!strongPasswordRegex.test(registerPassword)) {
   215:       setRegisterError(
   216:         "Mật khẩu quá yếu! Phải dài tối thiểu 8 ký tự, gồm chữ hoa, chữ thường, số và KÝ TỰ ĐẶC BIỆT.",
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
   228:           password: registerPassword,
   229:         }),
   230:       });
   231:       const data = await response.json().catch(() => ({}));
   232:       if (!response.ok) throw new Error(data.error || "Đăng ký thất bại.");
   233:       Alert.alert("Thành công", "Đăng ký tài khoản thành công.");
   234:       setEmail(registerEmail);
   235:       setPassword("");
   236:       setView("login");
   237:     } catch (error) {
```

#### Postman/PoC tự động
- Mục tiêu test: Kiểm tra request đang dùng HTTP cleartext thay vì HTTPS.
- Feature ảnh hưởng: Bảo mật truyền tải frontend/API
- Method: `POST`
- URL: `http://localhost:3000/api/register`
- Độ tin cậy mapping: High
- Ghi chú mapping: Endpoint được trích từ source snippet nếu có; nếu thiếu path cần reviewer map thủ công.

Headers:
```http
Content-Type: application/json
```

Payload mẫu:
```json
{
  "name": "{{test_name}}",
  "email": "{{test_email}}",
  "password": "{{test_password}}"
}
```

- Nguồn payload: Tự động suy luận từ `body: JSON.stringify(...)` trong source.
- Độ tin cậy payload: High
- Thay các biến `{{...}}` bằng giá trị Postman environment trước khi chạy PoC.

Pre-test setup:
```text
1. Mở source line được Semgrep báo để xác nhận API path.
2. Đảm bảo backend/frontend local đang chạy.
3. Gửi request bằng Postman và ghi nhận URL đang dùng HTTP.
```

Kết quả kỳ vọng:
- Nếu còn lỗi: Request gọi thành công qua `http://` hoặc dữ liệu nhạy cảm đi qua kênh không mã hóa.
- Nếu đã an toàn: Ứng dụng dùng `https://` hoặc cấu hình base URL an toàn theo môi trường.

#### Phân tích AI
Tuyệt vời! Với vai trò là chuyên gia bảo mật ứng dụng, đây là kết quả triage cho finding SEMGREP-006:

---

##### Triage Finding Bảo mật - SEMGREP-006

**1. Phân loại:** Needs Human Review

**2. Lý do phân loại dựa trên source evidence:**

*   **Rule ID:** `typescript.react.security.react-insecure-request.react-insecure-request`
*   **Mô tả Semgrep:** Phát hiện yêu cầu không mã hóa qua HTTP.
*   **Source evidence:** Dòng 222 trong file `eshop-sut\frontend-mobile\App.js` có đoạn mã:
    ```typescript
    const response = await fetch(`${API_URL}/register`, { ... });
    ```
    Trong đó, `API_URL` có thể là một biến môi trường hoặc được định nghĩa ở đâu đó trong dự án. Việc sử dụng `fetch` để thực hiện request tới `${API_URL}/register` mà không có bằng chứng rõ ràng về việc sử dụng HTTPS là điểm Semgrep cảnh báo.
*   **Ngữ cảnh:** Semgrep đang phân tích mã nguồn của ứng dụng EShop, được mô tả là "ứng dụng lab local". Môi trường "lab local" thường có thể sử dụng HTTP cho các API nội bộ hoặc khi kết nối với localhost để phát triển. Tuy nhiên, vấn đề bảo mật ở đây là việc truyền dữ liệu nhạy cảm (mật khẩu) qua một kênh không mã hóa.
*   **Lý do cho "Needs Human Review":** Mặc dù Semgrep cảnh báo về request không mã hóa, chúng ta cần làm rõ:
    *   **Giá trị thực tế của `API_URL`:** Biến `API_URL` được định nghĩa ở đâu? Nếu `API_URL` luôn trỏ tới một endpoint `http://localhost:<port>` hoặc một địa chỉ IP nội bộ *chỉ dùng trong mạng local* và *không bao giờ tiếp cận qua internet công cộng*, thì rủi ro thực tế có thể thấp hơn. Tuy nhiên, nếu `API_URL` có thể cấu hình để trỏ tới một server công cộng qua HTTP, đây là một lỗ hổng nghiêm trọng.
    *   **Môi trường triển khai:** Ứng dụng này chỉ dùng cho mục đích demo lab hay có khả năng được triển khai ra môi trường production? Nếu triển khai production, việc sử dụng HTTP là không thể chấp nhận cho bất kỳ request nào gửi dữ liệu nhạy cảm.
    *   **Dữ liệu nhạy cảm:** Việc đăng ký tài khoản liên quan đến email và mật khẩu, đây rõ ràng là thông tin nhạy cảm.

**3. Tác động thực tế trong bối cảnh EShop:**

Nếu `API_URL` trỏ tới một endpoint đang chạy trên giao thức HTTP và có thể truy cập được qua mạng (kể cả mạng nội bộ nếu không được bảo mật đúng cách), kẻ tấn công có thể nghe lén (sniffing) luồng dữ liệu truyền đi và đánh cắp thông tin đăng ký, bao gồm tên, email và mật khẩu người dùng. Điều này dẫn đến nguy cơ:

*   **Chiếm đoạt tài khoản:** Kẻ tấn công có thể sử dụng thông tin đăng ký để truy cập vào tài khoản người dùng, lấy cắp thông tin cá nhân, đơn hàng, hoặc thực hiện các hành vi gian lận.
*   **Phơi nhiễm thông tin nhạy cảm:** Dữ liệu cá nhân của người dùng bị lộ.
*   **Tấn công liên hoàn:** Thông tin đăng nhập bị lộ có thể được sử dụng để tấn công các dịch vụ khác mà người dùng sử dụng chung mật khẩu.

Tác động này được đánh giá là **MEDIUM** vì nó liên quan trực tiếp đến việc bảo vệ thông tin người dùng, mặc dù `Likelihood` (Khả năng xảy ra) có thể thấp nếu môi trường triển khai được kiểm soát chặt chẽ.

**4. Cách khắc phục cụ thể:**

*   **Ưu tiên hàng đầu:** Bắt buộc sử dụng HTTPS cho tất cả các giao tiếp từ frontend đến backend.
    *   **Backend:** Đảm bảo API của EShop được triển khai với chứng chỉ SSL/TLS hợp lệ và lắng nghe trên cổng HTTPS.
    *   **Frontend (`API_URL`):** Cập nhật cấu hình `API_URL` để luôn bắt đầu bằng `https://` thay vì `http://`. Nếu `API_URL` là biến môi trường, hãy đảm bảo nó được đặt đúng cách trong môi trường triển khai.
*   **Kiểm soát `API_URL`:** Nếu bắt buộc phải có fallback về HTTP cho môi trường dev cục bộ (ví dụ: `http://localhost:3000`), cần có cơ chế để đảm bảo rằng phiên bản sản xuất (production) **luôn luôn** sử dụng HTTPS. Điều này có thể được quản lý thông qua biến môi trường khác nhau cho các môi trường (dev, staging, prod).
*   **Cập nhật Dependency (nếu có):** Trong một số trường hợp, thư viện network có thể có các cấu hình mặc định không an toàn. Tuy nhiên, với `fetch` API gốc, vấn đề nằm ở URL được gọi.

**5. Ghi chú cần tester kiểm tra thêm nếu chưa đủ context:**

*   **Xác định giá trị và nguồn gốc của biến `API_URL`:** Tester cần tìm kiếm cách `API_URL` được định nghĩa và sử dụng trong toàn bộ dự án. Kiểm tra xem có các backend server khác nhau cho các môi trường khác nhau hay không và cấu hình `API_URL` cho môi trường production là gì.
*   **Kiểm tra cấu hình server backend:** Xác nhận rằng API endpoint mà `API_URL` trỏ tới đã được cấu hình để sử dụng HTTPS và có chứng chỉ SSL/TLS hợp lệ.
*   **Môi trường triển khai:** Làm rõ mục đích sử dụng của mã nguồn này. Nếu đây chỉ là mã test hoặc môi trường lab, cần đánh giá lại mức độ ưu tiên xử lý, nhưng vẫn nên cảnh báo về best practice. Nếu có khả năng được triển khai ra môi trường có người dùng thật, việc khắc phục là **khẩn cấp**.

---

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
- File: `eshop-sut\frontend-mobile\App.js`
- Dòng: 244
- Trạng thái kiểm chứng: Needs Human Review

#### Bằng chứng mã nguồn
```text
   229:         }),
   230:       });
   231:       const data = await response.json().catch(() => ({}));
   232:       if (!response.ok) throw new Error(data.error || "Đăng ký thất bại.");
   233:       Alert.alert("Thành công", "Đăng ký tài khoản thành công.");
   234:       setEmail(registerEmail);
   235:       setPassword("");
   236:       setView("login");
   237:     } catch (error) {
   238:       setRegisterError(error.message || "Đăng ký thất bại.");
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
   250:       if (!response.ok) throw new Error(data.error || "Không lấy được OTP.");
   251:       setForgotMessage(
   252:         "Nếu email tồn tại trong hệ thống, mã OTP đã được gửi đến email của bạn.",
   253:       );
   254:       setForgotStep(2);
   255:     } catch (error) {
   256:       Alert.alert("Lỗi", error.message || "Có lỗi xảy ra.");
   257:     }
   258:   };
   259:
```

#### Postman/PoC tự động
- Mục tiêu test: Kiểm tra request đang dùng HTTP cleartext thay vì HTTPS.
- Feature ảnh hưởng: Bảo mật truyền tải frontend/API
- Method: `POST`
- URL: `http://localhost:3000/api/forgot-password`
- Độ tin cậy mapping: High
- Ghi chú mapping: Endpoint được trích từ source snippet nếu có; nếu thiếu path cần reviewer map thủ công.

Headers:
```http
Content-Type: application/json
```

Payload mẫu:
```json
{
  "email": "{{test_email}}"
}
```

- Nguồn payload: Tự động suy luận từ `body: JSON.stringify(...)` trong source.
- Độ tin cậy payload: High
- Thay các biến `{{...}}` bằng giá trị Postman environment trước khi chạy PoC.

Pre-test setup:
```text
1. Mở source line được Semgrep báo để xác nhận API path.
2. Đảm bảo backend/frontend local đang chạy.
3. Gửi request bằng Postman và ghi nhận URL đang dùng HTTP.
```

Kết quả kỳ vọng:
- Nếu còn lỗi: Request gọi thành công qua `http://` hoặc dữ liệu nhạy cảm đi qua kênh không mã hóa.
- Nếu đã an toàn: Ứng dụng dùng `https://` hoặc cấu hình base URL an toàn theo môi trường.

#### Phân tích AI
Tuyệt vời! Với vai trò là chuyên gia bảo mật ứng dụng, tôi sẽ tiến hành triage finding SEMGREP-007 này. Dưới đây là phân tích chi tiết:

---

##### Phân loại: Needs Human Review

##### Lý do phân loại dựa trên source evidence

Bằng chứng mã nguồn cho thấy hàm `handleForgotPasswordRequest` trong file `App.js` thực hiện một yêu cầu `fetch` tới endpoint `/forgot-password`. Quan trọng là, URL này được định nghĩa bởi biến `API_URL`. Dòng 244 (`const response = await fetch(`${API_URL}/forgot-password`, { ... });`) trực tiếp chỉ ra rằng giao thức được sử dụng cho yêu cầu này sẽ phụ thuộc hoàn toàn vào giá trị của `API_URL`.

Semgrep Rule `react-insecure-request` đã phát hiện hành vi gọi `fetch` tới một URL được xây dựng từ biến, và nếu `API_URL` được cấu hình hoặc gán giá trị bắt đầu bằng `http://` (thay vì `https://`), thì việc truyền thông tin (trong trường hợp này là email của người dùng) sẽ không được mã hóa.

Tuy nhiên, việc kết luận đây là **True Positive** hay **False Positive** phụ thuộc vào cách `API_URL` được định nghĩa và sử dụng trong môi trường thực tế (production, staging, development).

*   **Khả năng là True Positive:** Nếu `API_URL` *có thể* được cấu hình thành một URL sử dụng `http://` trong môi trường production hoặc staging, hoặc nếu biến này không được quản lý cẩn thận trong quá trình build, thì đây là một lỗ hổng nghiêm trọng.
*   **Khả năng là False Positive:** Nếu `API_URL` *luôn luôn* được cấu hình để sử dụng `https://` (ví dụ: được hardcode là `https://api.eshop.com` hoặc được lấy từ biến môi trường được đảm bảo là `https://`), hoặc nếu đoạn mã này chỉ chạy trong môi trường local development với mục đích thử nghiệm và không bao giờ được deploy lên môi trường production dưới dạng không an toàn, thì đây có thể là False Positive.

Do đó, chúng ta cần thêm thông tin về cách `API_URL` được định nghĩa và quản lý để đưa ra kết luận cuối cùng.

##### Tác động thực tế trong bối cảnh EShop

Nếu `API_URL` trỏ đến một máy chủ qua giao thức HTTP insecure, thì yêu cầu gửi email cho tính năng quên mật khẩu sẽ truyền thông tin nhạy cảm (địa chỉ email) dưới dạng văn bản rõ ràng. Điều này có thể dẫn đến:

*   **Lộ lọt thông tin cá nhân:** Kẻ tấn công có thể nghe lén lưu lượng mạng và đánh cắp địa chỉ email của người dùng.
*   **Tấn công Account Takeover:** Nếu địa chỉ email bị lộ, kẻ tấn công có thể kết hợp với các kỹ thuật khác (như phishing) để cố gắng chiếm đoạt tài khoản người dùng.
*   **Vi phạm quy định về bảo vệ dữ liệu:** Như GDPR, CCPA,... nếu ứng dụng thu thập và xử lý dữ liệu nhạy cảm mà không có biện pháp bảo vệ đầy đủ.

Mức độ **Impact: MEDIUM** là hợp lý bởi việc lộ email có thể ảnh hưởng đến tài khoản người dùng.

##### Cách khắc phục cụ thể

Để khắc phục lỗ hổng này, cần đảm bảo rằng tất cả các yêu cầu mạng đều được thực hiện qua HTTPS:

1.  **Kiểm tra định nghĩa `API_URL`:** Tìm kiếm nơi `API_URL` được định nghĩa và đảm bảo rằng nó luôn được gán giá trị bắt đầu bằng `https://`.
    *   Nếu `API_URL` được lấy từ biến môi trường (ví dụ: `process.env.REACT_APP_API_URL`), hãy kiểm tra kỹ cấu hình của các biến môi trường trong các môi trường khác nhau (development, staging, production).
    *   Nếu `API_URL` được định nghĩa trực tiếp trong mã nguồn, hãy đảm bảo nó là một URL HTTPS.

2.  **Cập nhật mã nguồn (nếu cần):** Nếu việc kiểm tra cho thấy `API_URL` có thể được cấu hình thành HTTP, hãy cập nhật mã nguồn để kiểm tra và/hoặc buộc sử dụng HTTPS. Ví dụ:
    ```javascript
    // Trong file App.js hoặc file cấu hình API
    const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:3000'; // Ví dụ default
    const SECURE_API_URL = API_URL.startsWith('http://') ? API_URL.replace('http://', 'https://') : API_URL;

    // Trong hàm handleForgotPasswordRequest và các hàm tương tự
    const response = await fetch(`${SECURE_API_URL}/forgot-password`, {
      // ...
    });
    ```
    Tuy nhiên, cách tốt nhất là quản lý `API_URL` ở tầng cấu hình thay vì hardcode logic chuyển đổi trong code ứng dụng.

3.  **Cấu hình máy chủ API:** Đảm bảo rằng máy chủ API mà `API_URL` trỏ tới đã được cấu hình để nhận các yêu cầu qua HTTPS và đã cài đặt chứng chỉ SSL/TLS hợp lệ.

##### Ghi chú cần tester kiểm tra thêm nếu chưa đủ context

*   **Xác định nguồn gốc `API_URL`:** Tester cần điều tra xem biến `API_URL` được định nghĩa và cấu hình như thế nào trong các môi trường khác nhau (development, staging, production). Đặc biệt quan tâm đến các file cấu hình, biến môi trường, hoặc script build.
*   **Môi trường lab local:** Dòng "EShop đang được quét như ứng dụng lab local; finding liên quan localhost cần kiểm tra môi trường trước khi kết luận rủi ro cuối" là rất quan trọng. Nếu `API_URL` được thiết lập để trỏ đến `http://localhost:PORT` chỉ trong môi trường dev khi chạy trên máy local của developer, thì rủi ro thực tế đối với người dùng cuối là **thấp hoặc bằng không**. Tuy nhiên, vẫn cần xác nhận rằng không có cách nào `API_URL` bị ghi đè hoặc sử dụng giá trị `http://localhost` trong các bản build deploy.
*   **Sử dụng HTTPS trong các yêu cầu khác:** Kiểm tra xem có các yêu cầu `fetch` hoặc các thư viện HTTP khác trong ứng dụng sử dụng `API_URL` hay không, và liệu chúng có *tất cả* đều tuân thủ quy tắc sử dụng HTTPS. Nếu có nhiều yêu cầu tương tự, chúng có thể cùng một root cause và cách khắc phục sẽ áp dụng cho tất cả.

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
- File: `eshop-sut\frontend-mobile\App.js`
- Dòng: 272
- Trạng thái kiểm chứng: Needs Human Review

#### Bằng chứng mã nguồn
```text
   257:     }
   258:   };
   259:
   260:   const handleResetPassword = async () => {
   261:     const strongPasswordRegex =
   262:       /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z\d]).{8,}$/;
   263:     if (!strongPasswordRegex.test(newPassword)) {
   264:       Alert.alert(
   265:         "Lỗi",
   266:         "Mật khẩu quá yếu! Phải dài tối thiểu 8 ký tự, gồm chữ hoa, chữ thường, số và KÝ TỰ ĐẶC BIỆT.",
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
   278:         throw new Error("Mã OTP không đúng hoặc có lỗi xảy ra.");
   279:       Alert.alert("Thành công", "Đổi mật khẩu thành công!");
   280:       setView("login");
   281:     } catch (error) {
   282:       Alert.alert("Lỗi", "Mã OTP không đúng hoặc có lỗi xảy ra.");
   283:     }
   284:   };
   285:
   286:   const handleUpdateProfile = async () => {
   287:     if (!/^[1-9][0-9]{8,9}$/.test(phone)) {
```

#### Postman/PoC tự động
- Mục tiêu test: Kiểm tra request đang dùng HTTP cleartext thay vì HTTPS.
- Feature ảnh hưởng: Bảo mật truyền tải frontend/API
- Method: `POST`
- URL: `http://localhost:3000/api/reset-password`
- Độ tin cậy mapping: High
- Ghi chú mapping: Endpoint được trích từ source snippet nếu có; nếu thiếu path cần reviewer map thủ công.

Headers:
```http
Content-Type: application/json
```

Payload mẫu:
```json
{
  "email": "{{test_email}}",
  "resetToken": "{{reset_token}}",
  "newPassword": "{{new_password}}"
}
```

- Nguồn payload: Tự động suy luận từ `body: JSON.stringify(...)` trong source.
- Độ tin cậy payload: High
- Thay các biến `{{...}}` bằng giá trị Postman environment trước khi chạy PoC.

Pre-test setup:
```text
1. Mở source line được Semgrep báo để xác nhận API path.
2. Đảm bảo backend/frontend local đang chạy.
3. Gửi request bằng Postman và ghi nhận URL đang dùng HTTP.
```

Kết quả kỳ vọng:
- Nếu còn lỗi: Request gọi thành công qua `http://` hoặc dữ liệu nhạy cảm đi qua kênh không mã hóa.
- Nếu đã an toàn: Ứng dụng dùng `https://` hoặc cấu hình base URL an toàn theo môi trường.

#### Phân tích AI
Tuyệt vời, tôi sẽ đóng vai trò là chuyên gia bảo mật ứng dụng để triage finding này từ Semgrep.

---

##### Triage Finding Bảo Mật SEMGREP-008

##### 1. Phân loại: **Needs Human Review**

##### 2. Lý do phân loại dựa trên source evidence:

Finding SEMGREP-008 chỉ ra rằng có một yêu cầu mạng không được mã hóa (HTTP) được thực hiện đến API endpoint `/reset-password` từ file `App.js` dòng 272. Rule `react-insecure-request` của Semgrep đã phát hiện việc sử dụng `fetch` với một URL được xây dựng từ biến `API_URL`.

Tuy nhiên, ngữ cảnh `API_URL` không rõ ràng trong đoạn mã cung cấp. Nếu `API_URL` được cấu hình là `localhost` hoặc một địa chỉ IP nội bộ cho môi trường phát triển/dev, thì yêu cầu này có thể không phải là một lỗ hổng bảo mật trong môi trường production (nếu production sử dụng HTTPS). Bản thân việc sử dụng HTTP đến `localhost` khi phát triển là khá phổ biến và thường không tiềm ẩn rủi ro ngay lập tức nếu không có dữ liệu nhạy cảm được truyền đi và môi trường đó được kiểm soát.

Rule Semgrep Cảnh báo: "Unencrypted request over HTTP detected."

CWE-319: Cleartext Transmission of Sensitive Information và OWASP A03:2017/A02:2021/A04:2025 đều nhấn mạnh rủi ro khi truyền thông tin nhạy cảm qua kênh không được mã hóa. Dữ liệu nhạy cảm được truyền trong yêu cầu này bao gồm `email`, `resetToken`, và `newPassword`, những thông tin này chắc chắn cần được bảo vệ.

Vì vậy, mặc dù code rõ ràng thực hiện một yêu cầu HTTP, nhưng **rủi ro thực tế phụ thuộc hoàn toàn vào cách `API_URL` được cấu hình và sử dụng trong các môi trường khác nhau (development, staging, production).**

##### 3. Tác động thực tế trong bối cảnh EShop:

**Nếu `API_URL` trỏ đến một địa chỉ không phải localhost hoặc IP nội bộ, và sử dụng HTTP thay vì HTTPS:**

*   **Lộ thông tin nhạy cảm:** Kẻ tấn công có thể nghe lén lưu lượng mạng và đánh cắp thông tin đăng nhập người dùng (email, token reset mật khẩu, mật khẩu mới), dẫn đến việc tài khoản bị chiếm đoạt. Điều này trực tiếp vi phạm CWE-319 và các khuyến cáo của OWASP.
*   **Tấn công Man-in-the-Middle (MITM):** Kẻ tấn công có thể thay đổi dữ liệu truyền đi, chẳng hạn như thay đổi mật khẩu mới của người dùng bằng một mật khẩu do kẻ tấn công kiểm soát, hoặc chèn mã độc vào phản hồi từ server.

**Nếu `API_URL` trỏ đến `localhost` hoặc IP nội bộ và chỉ sử dụng trong môi trường dev/lab:**

*   Trong môi trường này, rủi ro về việc bị nghe lén từ mạng bên ngoài là rất thấp. Tuy nhiên, vẫn tồn tại rủi ro nếu môi trường phát triển bị xâm nhập hoặc có các tiến trình độc hại khác trên máy đó.
*   Việc truyền mật khẩu qua HTTP ngay cả trên localhost cũng là một thực hành tồi, vì vậy việc khắc phục vẫn cần thiết để đảm bảo code có thể tái sử dụng an toàn trong các ngữ cảnh khác.

##### 4. Cách khắc phục cụ thể:

Ưu tiên hàng đầu là đảm bảo tất cả các yêu cầu đến API đều sử dụng **HTTPS**.

1.  **Cấu hình môi trường:**
    *   Xác định cách `API_URL` được định nghĩa và cung cấp cho ứng dụng mobile.
    *   Trong môi trường **production**, đảm bảo rằng `API_URL` luôn trỏ đến một endpoint sử dụng **HTTPS**.
    *   Nếu API server không hỗ trợ HTTPS, cần triển khai chứng chỉ SSL/TLS cho API server ngay lập tức.

2.  **Sử dụng HTTPS:** Thay đổi cách gọi `fetch` để đảm bảo URL luôn bắt đầu bằng `https://` nếu kết nối với server production.
    ```javascript
    // Ví dụ: giả định API_URL được quản lý thông qua biến môi trường hoặc cấu hình
    // Nếu API_URL có thể là http hoặc https, cần logic kiểm tra.
    
    // Cách tiếp cận an toàn hơn: Luôn dùng HTTPS cho production
    // Có thể xem xét cấu hình API_URL như sau:
    // const API_URL = process.env.NODE_ENV === 'production' ? 'https://api.your-eshop.com' : 'http://localhost:3000';
    
    // Trong trường hợp này, gọi fetch sẽ là:
    const apiUrlWithHttps = API_URL.startsWith('http://') && process.env.NODE_ENV === 'production' 
        ? API_URL.replace('http://', 'https://') 
        : API_URL;
        
    const response = await fetch(`${apiUrlWithHttps}/reset-password`, { // Sử dụng API_URL đã được đảm bảo là HTTPS
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: forgotEmail, resetToken, newPassword }),
    });
    ```
    Hoặc cách đơn giản hơn là định nghĩa `API_URL` cho production luôn là URL HTTPS.

3.  **An toàn cho cả môi trường Localhost (nếu có yêu cầu):**
    *   Nếu sau này bạn có ý định chạy API của EShop trên HTTPS cho môi trường localhost (ví dụ: sử dụng `localhost:3000` với HTTPS), bạn cần cấu hình chứng chỉ cho server này. Tuy nhiên, việc này thường phức tạp hơn cho môi trường local và có thể không cần thiết nếu chỉ là dev thông thường. **Ưu tiên là cho production.**

##### 5. Ghi chú cần tester kiểm tra thêm nếu chưa đủ context:

*   **Xác định giá trị của biến `API_URL`:** Tester cần kiểm tra giá trị thực tế của `API_URL` trong các môi trường khác nhau (development, staging, production). Đặc biệt quan trọng là nó được định nghĩa ở đâu và như thế nào.
*   **Cấu hình chứng chỉ SSL/TLS cho API Server:** Tester cần xác nhận xem API Server mà ứng dụng mobile này kết nối đến có đang sử dụng HTTPS với chứng chỉ hợp lệ hay không.
*   **Quy trình deploy:** Tester cần hiểu cách ứng dụng mobile được build và deploy cho mỗi môi trường, và làm thế nào các biến môi trường hoặc cấu hình liên quan đến `API_URL` được áp dụng. Nếu ứng dụng được build sẵn với một `API_URL` cứng nhắc (ví dụ: `http://localhost:3000`), thì nó sẽ luôn gửi yêu cầu HTTP ngay cả khi deploy lên môi trường không mong muốn.

---

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
- File: `eshop-sut\frontend-mobile\App.js`
- Dòng: 296
- Trạng thái kiểm chứng: Needs Human Review

#### Bằng chứng mã nguồn
```text
   281:     } catch (error) {
   282:       Alert.alert("Lỗi", "Mã OTP không đúng hoặc có lỗi xảy ra.");
   283:     }
   284:   };
   285:
   286:   const handleUpdateProfile = async () => {
   287:     if (!/^[1-9][0-9]{8,9}$/.test(phone)) {
   288:       Alert.alert(
   289:         "Lỗi",
   290:         "Số điện thoại không hợp lệ. Vui lòng nhập đúng 9-10 chữ số.",
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
   302:         body: JSON.stringify({ name, phone, shippingAddress }),
   303:       });
   304:       if (!response.ok) throw new Error("Lỗi cập nhật");
   305:       Alert.alert("Thành công", "Cập nhật thành công!");
   306:       setUser({ ...user, name, phone, shipping_address: shippingAddress });
   307:     } catch (error) {
   308:       Alert.alert("Lỗi", "Lỗi cập nhật");
   309:     }
   310:   };
   311:
```

#### Postman/PoC tự động
- Mục tiêu test: Kiểm tra request đang dùng HTTP cleartext thay vì HTTPS.
- Feature ảnh hưởng: Bảo mật truyền tải frontend/API
- Method: `PUT`
- URL: `http://localhost:3000/api/users/me`
- Độ tin cậy mapping: High
- Ghi chú mapping: Endpoint được trích từ source snippet nếu có; nếu thiếu path cần reviewer map thủ công.

Headers:
```http
Content-Type: application/json
```

Payload mẫu:
```json
{
  "name": "{{test_name}}",
  "phone": "{{test_phone}}",
  "shippingAddress": "{{shipping_address}}"
}
```

- Nguồn payload: Tự động suy luận từ `body: JSON.stringify(...)` trong source.
- Độ tin cậy payload: High
- Thay các biến `{{...}}` bằng giá trị Postman environment trước khi chạy PoC.

Pre-test setup:
```text
1. Mở source line được Semgrep báo để xác nhận API path.
2. Đảm bảo backend/frontend local đang chạy.
3. Gửi request bằng Postman và ghi nhận URL đang dùng HTTP.
```

Kết quả kỳ vọng:
- Nếu còn lỗi: Request gọi thành công qua `http://` hoặc dữ liệu nhạy cảm đi qua kênh không mã hóa.
- Nếu đã an toàn: Ứng dụng dùng `https://` hoặc cấu hình base URL an toàn theo môi trường.

#### Phân tích AI
Tuyệt vời, tôi sẵn sàng đóng vai trò chuyên gia bảo mật để triage finding này. Dưới đây là phân tích chi tiết:

---

##### Triage Finding Bảo Mật - SEMGREP-009

##### 1. Phân loại:
Needs Human Review

##### 2. Lý do phân loại dựa trên source evidence:

Dựa trên bằng chứng mã nguồn được cung cấp, rule SEMGREP-009 chỉ ra rằng có một yêu cầu mạng không được mã hóa thông qua HTTP (`fetch(`${API_URL}/users/me`, { ... })`). Rule này nhắm vào lỗ hổng **CWE-319: Cleartext Transmission of Sensitive Information**, và các Category **OWASP A03:2017 - Sensitive Data Exposure, A02:2021 - Cryptographic Failures, A04:2025 - Cryptographic Failures**.

Tuy nhiên, để đưa ra kết luận cuối cùng (True Positive hay False Positive), chúng ta cần xem xét ngữ cảnh deploy:

*   **`API_URL` không rõ ràng:** Chúng ta không biết giá trị thực tế của `API_URL` trong môi trường deploy.
    *   Nếu `API_URL` là một domain hoặc IP mà ứng dụng giao tiếp **không phải qua `localhost` hoặc `127.0.0.1` và không sử dụng HTTPS**, thì đây **gần như chắc chắn là một True Positive**. Dữ liệu nhạy cảm (như token xác thực - `Authorization: Bearer ${token}` - và dữ liệu profile) sẽ bị truyền đi dưới dạng plain text, dễ dàng bị nghe lén.
    *   Nếu `API_URL` trỏ đến **`localhost` hoặc `127.0.0.1` và đang chạy một backend development server không yêu cầu HTTPS cho mục đích debug/lab**, thì rủi ro thực tế có thể thấp hơn nhiều, có thể xem xét là **False Positive** do môi trường không mang tính production.
    *   Nếu `API_URL` được cấu hình để sử dụng **HTTPS** trong môi trường production, thì phát hiện HTTP này có thể là từ cấu hình cho môi trường development/testing và không ảnh hưởng đến production, hoặc là một lỗi cấu hình cần xem xét.

*   **Môi trường Lab/Local:** Giả định `EShop` đang được quét như "ứng dụng lab local" làm tăng khả năng `API_URL` có thể trỏ đến một endpoint localhost hoặc nội bộ mà không sử dụng HTTPS. Tuy nhiên, ngay cả trong môi trường lab, việc sử dụng HTTP cho các yêu cầu chứa thông tin nhạy cảm (như token) vẫn là một thực hành bảo mật kém.

Rule phát hiện một điểm truy cập tiềm năng cho lỗ hổng, nhưng *khả năng khai thác thực tế* và *mức độ nghiêm trọng* phụ thuộc lớn vào cách `API_URL` được định nghĩa và sử dụng trong các môi trường khác nhau.

##### 3. Tác động thực tế trong bối cảnh EShop:

Nếu `API_URL` dẫn đến một endpoint trên mạng công cộng hoặc mạng không đáng tin cậy mà không sử dụng HTTPS, thì tác động thực tế sẽ như sau:

*   **Lộ thông tin nhạy cảm:** Token xác thực (`Authorization: Bearer ${token}`) có thể bị kẻ tấn công bắt được, cho phép chúng mạo danh người dùng và truy cập, thay đổi hoặc xóa thông tin cá nhân (tên, số điện thoại, địa chỉ giao hàng) của ứng dụng.
*   **Tấn công Man-in-the-Middle (MITM):** Dữ liệu cá nhân được gửi đi dưới dạng plain text có thể bị đọc, sửa đổi hoặc chèn dữ liệu độc hại.
*   **Ảnh hưởng đến niềm tin người dùng:** Nếu dữ liệu người dùng không được bảo vệ, điều này có thể gây tổn hại nghiêm trọng đến uy tín và lòng tin của khách hàng đối với EShop.

Tuy nhiên, nếu `API_URL` chỉ là `localhost` và được sử dụng cho mục đích dev/test với backend không yêu cầu HTTPS, thì rủi ro này **chỉ tồn tại trong môi trường đó** và không ảnh hưởng đến người dùng cuối.

##### 4. Cách khắc phục cụ thể:

1.  **Cấu hình môi trường:**
    *   **Ưu tiên hàng đầu:** Đảm bảo rằng tất cả các yêu cầu đến backend, đặc biệt là các yêu cầu chứa thông tin nhạy cảm, **luôn sử dụng HTTPS**.
    *   **Xác định giá trị `API_URL`:** Kiểm tra xem biến `API_URL` được định nghĩa như thế nào trong các file cấu hình khác nhau cho các môi trường (development, staging, production).
    *   **Sử dụng HTTPS:** Nếu backend API hỗ trợ HTTPS, hãy cập nhật `API_URL` để sử dụng `https://` thay vì `http://`. Ví dụ: `const API_URL = "https://your-api-domain.com";` hoặc `const API_URL = "https://localhost:port";` nếu backend dev cũng chạy trên HTTPS.

2.  **Sửa đổi mã nguồn (nếu cần):**
    *   Trong trường hợp không thể ngay lập tức cập nhật sang HTTPS cho tất cả các môi trường, có thể xem xét việc thêm logic kiểm tra môi trường để chỉ áp dụng các biện pháp bảo mật nghiêm ngặt cho môi trường production. Tuy nhiên, cách này chỉ là tạm thời và không nên là giải pháp lâu dài.

3.  **Kiểm tra lại Semgrep rules:**
    *   Nếu `API_URL` được cấu hình chính xác là HTTPS cho production, chúng ta có thể cần tinh chỉnh rule của Semgrep hoặc cấu hình của nó để bỏ qua các đường dẫn sử dụng `localhost` hoặc các quy tắc riêng cho môi trường dev.

##### 5. Ghi chú cần tester kiểm tra thêm nếu chưa đủ context:

*   **Kiểm tra file cấu hình:** Yêu cầu tester kiểm tra các file cấu hình khác liên quan đến `API_URL` (ví dụ: `.env`, `config.js`, v.v.) để xác định giá trị thực tế của `API_URL` trong các môi trường deploy khác nhau (đặc biệt là production).
*   **Kiểm tra backend API:** Xác nhận xem backend API của EShop có hỗ trợ và đang chạy trên HTTPS hay không.
*   **Môi trường deploy:** Làm rõ môi trường mà EShop đang được deploy. Nếu đây là môi trường development/lab, cần xác nhận liệu `localhost` HTTP có phải là một config chấp nhận được cho môi trường đó và không ảnh hưởng đến production hay không.
*   **Kiểm tra các thành phần khác của ứng dụng:** Tìm xem liệu có các yêu cầu HTTP không được mã hóa nào khác trong ứng dụng hay không, đặc biệt là ở các phần xử lý thông tin nhạy cảm khác.

---

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
- File: `eshop-sut\frontend-mobile\App.js`
- Dòng: 362
- Trạng thái kiểm chứng: Needs Human Review

#### Bằng chứng mã nguồn
```text
   347:     }
   348:     setEditableTotal(cartTotal);
   349:     setCouponCode("");
   350:     setCouponResult(null);
   351:     setCouponError("");
   352:     setCheckoutSuccess(false);
   353:     setView("checkout");
   354:   };
   355:
   356:   const handleApplyCoupon = async () => {
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
   368:           user_id: user?.id || null,
   369:         }),
   370:       });
   371:       const data = await response.json();
   372:       if (!response.ok) throw new Error(data.error || "Không thể áp dụng mã");
   373:       setCouponResult(data);
   374:     } catch (error) {
   375:       setCouponError(error.message || "Không thể áp dụng mã");
   376:     }
   377:     setApplyingCoupon(false);
```

#### Postman/PoC tự động
- Mục tiêu test: Kiểm tra request đang dùng HTTP cleartext thay vì HTTPS.
- Feature ảnh hưởng: Bảo mật truyền tải frontend/API
- Method: `POST`
- URL: `http://localhost:3000/api/apply-coupon`
- Độ tin cậy mapping: High
- Ghi chú mapping: Endpoint được trích từ source snippet nếu có; nếu thiếu path cần reviewer map thủ công.

Headers:
```http
Content-Type: application/json
```

Payload mẫu:
```json
{
  "code": "{{coupon_code}}",
  "total_amount": 100000,
  "user_id": "{{user_id}}"
}
```

- Nguồn payload: Tự động suy luận từ `body: JSON.stringify(...)` trong source.
- Độ tin cậy payload: High
- Thay các biến `{{...}}` bằng giá trị Postman environment trước khi chạy PoC.

Pre-test setup:
```text
1. Mở source line được Semgrep báo để xác nhận API path.
2. Đảm bảo backend/frontend local đang chạy.
3. Gửi request bằng Postman và ghi nhận URL đang dùng HTTP.
```

Kết quả kỳ vọng:
- Nếu còn lỗi: Request gọi thành công qua `http://` hoặc dữ liệu nhạy cảm đi qua kênh không mã hóa.
- Nếu đã an toàn: Ứng dụng dùng `https://` hoặc cấu hình base URL an toàn theo môi trường.

#### Phân tích AI
Tuyệt vời, tôi sẵn sàng đóng vai trò chuyên gia bảo mật ứng dụng để phân tích finding này.

##### Triage Finding Bảo Mật SEMGREP-010

1.  **Phân loại:** Needs Human Review

2.  **Lý do phân loại dựa trên source evidence:**
    Semgrep rule phát hiện việc sử dụng `fetch` để gọi đến một URL bắt đầu bằng `${API_URL}/apply-coupon` có khả năng là HTTP thay vì HTTPS. Việc này khớp với mô tả "Unencrypted request over HTTP detected" và CWE-319.

    Tuy nhiên, dòng mã nguồn cho thấy `API_URL` là một biến được sử dụng. Để xác định chính xác đây có phải là True Positive hay False Positive, chúng ta cần biết giá trị thực tế của `API_URL` trong các môi trường khác nhau, đặc biệt là môi trường production.
    *   Nếu `API_URL` được cấu hình trỏ đến `http://localhost:PORT` hoặc một địa chỉ IP/hostname sử dụng HTTP trong môi trường phát triển (dev) hoặc lab, thì đây có thể là một cảnh báo cho phép phát triển và không phải là rủi ro bảo mật nghiêm trọng nếu không có dữ liệu nhạy cảm nào được truyền đi.
    *   Tuy nhiên, nếu `API_URL` được cấu hình trỏ đến một endpoint API mà **không** sử dụng TLS/SSL (HTTPS) trong môi trường production, thì đây là một lỗ hổng nghiêm trọng dẫn đến việc lộ lọt thông tin nhạy cảm (như `user_id`, mã giảm giá, tổng giá trị đơn hàng).
    *   Ngữ cảnh "EShop đang được quét như ứng dụng lab local" càng củng cố thêm khả năng đây là một môi trường để thử nghiệm, nơi việc sử dụng HTTP localhost là phổ biến.

    Do đó, để đưa ra kết luận cuối cùng, cần xác minh cách biến `API_URL` được định nghĩa và sử dụng trong các file cấu hình của EShop cho các môi trường khác nhau.

3.  **Tác động thực tế trong bối cảnh EShop:**
    Nếu `API_URL` trỏ đến một dịch vụ API chỉ dùng HTTP và ứng dụng EShop đang được triển khai trong môi trường production (hoặc nơi mà dữ liệu người dùng thực có thể bị ảnh hưởng), tác động có thể là:
    *   **Lộ lọt dữ liệu nhạy cảm:** Mã giảm giá, tổng giá trị đơn hàng, và thậm chí `user_id` có thể bị kẻ tấn công nghe lén trên mạng.
    *   **Thao túng dữ liệu:** Kẻ tấn công có thể sửa đổi các yêu cầu gửi đi, ví dụ như thay đổi mã giảm giá để nhận ưu đãi không hợp lệ hoặc làm gián đoạn quy trình áp dụng mã.
    *   **Đánh cắp thông tin tài khoản:** Nếu thông tin đăng nhập hoặc token xác thực được truyền đi trong các request tương tự, chúng có thể bị đánh cắp.

    Tuy nhiên, dữ liệu được gửi trong request này (`code`, `total_amount`, `user_id`) ở mức độ nhạy cảm trung bình. `user_id` có thể không quá nhạy cảm nếu nó chỉ là một định danh nội bộ, nhưng việc lộ lọt mã giảm giá và tổng giá trị đơn hàng có thể hữu ích cho kẻ tấn công trong việc lập kế hoạch tấn công tiếp theo hoặc hiểu quy luật mua sắm của người dùng.

4.  **Cách khắc phục cụ thể:**
    *   **Ưu tiên sử dụng HTTPS:** Đảm bảo rằng tất cả các backend API mà ứng dụng EShop giao tiếp đều được triển khai và cấu hình để sử dụng kết nối mã hóa TLS/SSL (HTTPS).
    *   **Cấu hình biến môi trường:** Định nghĩa `API_URL` thông qua biến môi trường. Trong môi trường production, biến này **phải** trỏ đến endpoint API sử dụng HTTPS. Trong môi trường phát triển/lab, nếu cần sử dụng HTTP cho `localhost`, cần có chính sách rõ ràng về việc chỉ sử dụng cho mục đích thử nghiệm và đảm bảo không có dữ liệu nhạy cảm thực sự nào được gửi đi.
    *   **Kiểm tra giá trị `API_URL`:**
        *   Tìm kiếm định nghĩa của `API_URL` trong mã nguồn hoặc các file cấu hình (ví dụ: `.env`, `config.js`, v.v.).
        *   Xác minh xem trong môi trường production, `API_URL` có luôn bắt đầu bằng `https://` hay không.
    *   **Phát triển code an toàn hơn:** Trong trường hợp có khả năng API vẫn được gọi qua HTTP (ví dụ: trong các trường hợp `localhost` cho dev), cân nhắc việc lọc hoặc mã hóa các trường dữ liệu nhạy cảm trước khi gửi đi nếu không thể đảm bảo HTTPS cho mọi endpoint. Tuy nhiên, giải pháp tốt nhất vẫn là **buộc sử dụng HTTPS**.

5.  **Ghi chú cần tester kiểm tra thêm:**
    *   **Xác định rõ mục đích sử dụng của `API_URL`:** Tester cần tìm file cấu hình hoặc định nghĩa của `API_URL` để xác định URL nó trỏ tới trong các môi trường khác nhau (development, staging, production).
    *   **Kiểm tra dữ liệu gửi đi:** Liệu `user_id` có thực sự là định danh nhạy cảm của người dùng hay chỉ là ID tạm thời? Liệu mã giảm giá có thể bị lợi dụng theo cách nào khác ngoài việc áp dụng?
    *   **Kiểm tra quy trình deploy:** Quy trình deploy của ứng dụng có cho phép người dùng cấu hình `API_URL` một cách linh hoạt theo môi trường không? Có cơ chế validation nào cho URL được cấu hình không?
    *   **Môi trường Lab:** Nếu đây là ứng dụng lab *chỉ* chạy với `localhost` và không bao giờ được deploy với dữ liệu thực, thì finding này có thể được đánh dấu là *giáo dục/cảnh báo lý thuyết* thay vì một lỗ hổng thực tế. Tuy nhiên, việc lặp lại thói quen này có thể dẫn đến sai lầm khi phát triển các ứng dụng khác nghiêm túc hơn.

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
- File: `eshop-sut\frontend-mobile\App.js`
- Dòng: 384
- Trạng thái kiểm chứng: Needs Human Review

#### Bằng chứng mã nguồn
```text
   369:         }),
   370:       });
   371:       const data = await response.json();
   372:       if (!response.ok) throw new Error(data.error || "Không thể áp dụng mã");
   373:       setCouponResult(data);
   374:     } catch (error) {
   375:       setCouponError(error.message || "Không thể áp dụng mã");
   376:     }
   377:     setApplyingCoupon(false);
   378:   };
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
   390:         body: JSON.stringify({
   391:           items: cart.length > 1 ? cart.slice(0, -1) : cart,
   392:           total_amount: finalAmount,
   393:           coupon_id: couponResult?.coupon_id || null,
   394:         }),
   395:       });
   396:       const data = await response.json().catch(() => ({}));
   397:       if (!response.ok) throw new Error(data.error || "Lỗi khi thanh toán.");
   398:
   399:       if (couponResult?.coupon_id && token) {
```

#### Postman/PoC tự động
- Mục tiêu test: Kiểm tra request đang dùng HTTP cleartext thay vì HTTPS.
- Feature ảnh hưởng: Bảo mật truyền tải frontend/API
- Method: `POST`
- URL: `http://localhost:3000/api/checkout`
- Độ tin cậy mapping: High
- Ghi chú mapping: Endpoint được trích từ source snippet nếu có; nếu thiếu path cần reviewer map thủ công.

Headers:
```http
Content-Type: application/json
```

Payload mẫu:
```json
{
  "items": [
    {
      "product_id": "{{product_id}}",
      "quantity": 1,
      "price": 100000
    }
  ],
  "total_amount": 100000,
  "coupon_id": null
}
```

- Nguồn payload: Tự động suy luận từ `body: JSON.stringify(...)` trong source.
- Độ tin cậy payload: High
- Thay các biến `{{...}}` bằng giá trị Postman environment trước khi chạy PoC.

Pre-test setup:
```text
1. Mở source line được Semgrep báo để xác nhận API path.
2. Đảm bảo backend/frontend local đang chạy.
3. Gửi request bằng Postman và ghi nhận URL đang dùng HTTP.
```

Kết quả kỳ vọng:
- Nếu còn lỗi: Request gọi thành công qua `http://` hoặc dữ liệu nhạy cảm đi qua kênh không mã hóa.
- Nếu đã an toàn: Ứng dụng dùng `https://` hoặc cấu hình base URL an toàn theo môi trường.

#### Phân tích AI
Dưới đây là kết quả triage cho finding bảo mật SEMGREP-011:

##### Kết quả Triage Finding Bảo mật SEMGREP-011

##### 1. Phân loại:

False Positive

##### 2. Lý do phân loại dựa trên source evidence:

*   **Ngữ cảnh mã nguồn:** Dòng 384 (`fetch(\`${API_URL}/checkout\`, ...`) sử dụng biến `API_URL`. Trong ngữ cảnh ứng dụng lab local mà Semgrep đang quét, `API_URL` có khả năng cao được cấu hình để trỏ đến `http://localhost:<port>` hoặc một địa chỉ IP cục bộ tương tự, phục vụ cho môi trường phát triển (dev/lab).
*   **Bản chất của `fetch`:** Semgrep rule phát hiện việc sử dụng `fetch` mà không có chỉ dẫn về HTTPS, cảnh báo về "Unencrypted request over HTTP detected". Tuy nhiên, việc sử dụng HTTP cho các yêu cầu đến `localhost` trong môi trường lab không trực tiếp gây ra rủi ro cho dữ liệu nhạy cảm của người dùng cuối.
*   **Thiếu bằng chứng về việc lộ lọt dữ liệu nhạy cảm:** Dữ liệu được gửi trong "/checkout" bao gồm `items`, `total_amount`, `coupon_id`. Mặc dù `token` (trong header `Authorization`) là dữ liệu nhạy cảm, việc gửi token đến `localhost` trong môi trường lab không giống với việc lộ lọt nó ra mạng công cộng.

##### 3. Tác động thực tế trong bối cảnh EShop:

Trong nhiều trường hợp, `API_URL` được cấu hình động dựa trên môi trường deploy. Nếu `API_URL` *chỉ* được sử dụng với các dịch vụ chạy trên máy local hoặc trong một mạng nội bộ an toàn (môi trường dev/lab), thì việc này không tạo ra rủi ro đáng kể.

Tuy nhiên, nếu `API_URL` có thể được cấu hình để trỏ tới một máy chủ bên ngoài và kết nối không sử dụng TLS/SSL (HTTPS), thì đây sẽ là một lỗ hổng nghiêm trọng (True Positive). Nhưng dựa trên thông tin hiện tại (ứng dụng lab local, ghi chú về việc kiểm tra môi trường), chúng ta giả định trường hợp an toàn hơn.

##### 4. Cách khắc phục cụ thể:

*   **Đối với môi trường Production:** Luôn đảm bảo rằng `API_URL` được cấu hình để sử dụng HTTPS khi kết nối tới backend. Điều này có thể liên quan đến việc chỉnh sửa file cấu hình (ví dụ: `.env`, file cấu hình ứng dụng) để biến `API_URL` luôn bắt đầu bằng `https://`.
*   **Đối với môi trường Dev/Lab:** Nếu đây là ứng dụng lab, việc sử dụng `http://localhost` là chấp nhận được cho mục đích demo. Tuy nhiên, nếu có thể, nên cấu hình backend để chạy với HTTPS ngay cả trên local để phản ánh quy trình production.

##### 5. Ghi chú cần tester kiểm tra thêm:

Để **chắc chắn** đây là False Positive, tester cần kiểm tra giá trị thực tế của biến `API_URL` trong các cấu hình môi trường khác nhau, đặc biệt là cấu hình production.

*   **Kiểm tra cấu hình API URL:** Xác định file hoặc cách thức mà biến `API_URL` được định nghĩa và giá trị của nó trong môi trường production.
*   **Kiểm tra trạng thái của Backend:**backend mà `/checkout` gọi tới có được cấu hình để chấp nhận kết nối HTTPS không, và liệu nó có được truy cập qua HTTPS hay không trong production.
*   **Kiểm tra các dữ liệu nhạy cảm khác:** Hãy kiểm tra xem còn có những API call nào khác sử dụng HTTP cho các endpoint quan trọng hoặc gửi dữ liệu nhạy cảm không.

Nếu `API_URL` *luôn* trỏ đến một endpoint HTTPS trong môi trường production, thì việc Semgrep cảnh báo là do nó không phân tích được biến `API_URL` để biết rằng nó sẽ được dùng với HTTPS. Rule này có thể cần tinh chỉnh hoặc cần bổ sung logic sau khi khai báo (ví dụ: kiểm tra `API_URL.startsWith('https')`).

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
- File: `eshop-sut\frontend-mobile\App.js`
- Dòng: 400
- Trạng thái kiểm chứng: Needs Human Review

#### Bằng chứng mã nguồn
```text
   385:         method: "POST",
   386:         headers: {
   387:           "Content-Type": "application/json",
   388:           ...(token ? { Authorization: `Bearer ${token}` } : {}),
   389:         },
   390:         body: JSON.stringify({
   391:           items: cart.length > 1 ? cart.slice(0, -1) : cart,
   392:           total_amount: finalAmount,
   393:           coupon_id: couponResult?.coupon_id || null,
   394:         }),
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
   406:           body: JSON.stringify({ coupon_id: couponResult.coupon_id }),
   407:         });
   408:       }
   409:
   410:       setCheckoutSuccess(true);
   411:       setCart([]);
   412:       setCouponCode("");
   413:       setCouponResult(null);
   414:       setEditableTotal(0);
   415:       fetchOrders(token);
```

#### Postman/PoC tự động
- Mục tiêu test: Kiểm tra request đang dùng HTTP cleartext thay vì HTTPS.
- Feature ảnh hưởng: Bảo mật truyền tải frontend/API
- Method: `POST`
- URL: `http://localhost:3000/api/coupon-usage`
- Độ tin cậy mapping: High
- Ghi chú mapping: Endpoint được trích từ source snippet nếu có; nếu thiếu path cần reviewer map thủ công.

Headers:
```http
Content-Type: application/json
```

Payload mẫu:
```json
{
  "coupon_id": "{{coupon_id}}"
}
```

- Nguồn payload: Tự động suy luận từ `body: JSON.stringify(...)` trong source.
- Độ tin cậy payload: High
- Thay các biến `{{...}}` bằng giá trị Postman environment trước khi chạy PoC.

Pre-test setup:
```text
1. Mở source line được Semgrep báo để xác nhận API path.
2. Đảm bảo backend/frontend local đang chạy.
3. Gửi request bằng Postman và ghi nhận URL đang dùng HTTP.
```

Kết quả kỳ vọng:
- Nếu còn lỗi: Request gọi thành công qua `http://` hoặc dữ liệu nhạy cảm đi qua kênh không mã hóa.
- Nếu đã an toàn: Ứng dụng dùng `https://` hoặc cấu hình base URL an toàn theo môi trường.

#### Phân tích AI
Tuyệt vời! Hãy cùng tôi phân tích finding SEMGREP-012 này. Dựa trên thông tin được cung cấp, đây là kết quả triage của tôi dưới vai trò chuyên gia bảo mật ứng dụng:

---

##### Triage Finding Bảo Mật

**Mã finding:** SEMGREP-012
**Rule ID:** `typescript.react.security.react-insecure-request.react-insecure-request`
**File nguồn:** `eshop-sut\frontend-mobile\App.js`
**Dòng:** 400
**Severity:** ERROR
**CWE:** CWE-319: Cleartext Transmission of Sensitive Information
**OWASP:** A03:2017 - Sensitive Data Exposure, A02:2021 - Cryptographic Failures, A04:2025 - Cryptographic Failures
**Likelihood:** LOW
**Impact:** MEDIUM
**Confidence:** MEDIUM
**Cảnh báo Semgrep:** Unencrypted request over HTTP detected.

---

1.  **Phân loại:** Needs Human Review

2.  **Lý do phân loại dựa trên source evidence:**
    Semgrep rule phát hiện một yêu cầu mạng được gửi qua giao thức HTTP (không mã hóa) tại dòng 400. Cụ thể, dòng này thực hiện một lệnh gọi `fetch` đến `${API_URL}/coupon-usage`. Dù rule này nhạy cảm với việc sử dụng HTTP, ngữ cảnh của `API_URL` lại là yếu tố quyết định chính cho việc phân loại.

    *   Nếu `${API_URL}` được cấu hình trỏ đến một máy chủ `localhost` hoặc một địa chỉ IP nội bộ chỉ được truy cập trong môi trường phát triển hoặc lab **local**, thì việc sử dụng HTTP ở đây có thể không gây ra rủi ro bảo mật đáng kể cho người dùng cuối.
    *   Tuy nhiên, nếu `${API_URL}` trỏ đến một địa chỉ công cộng hoặc một máy chủ sản xuất được truy cập qua Internet, việc gửi yêu cầu mà không có mã hóa TLS/SSL (HTTPS) sẽ làm lộ thông tin nhạy cảm được truyền trong body (trong trường hợp này là `coupon_id`) và cả headers (như `Authorization` token), dẫn đến lỗ hổng Creative Failures và Sensitive Data Exposure.

    Do đó, chỉ dựa vào mã nguồn tĩnh mà không rõ cách `API_URL` được định nghĩa và triển khai trong môi trường thực tế (dev/staging/prod), chúng ta không thể kết luận đây là True Positive hay False Positive.

3.  **Tác động thực tế trong bối cảnh EShop:**
    Nếu `API_URL` trỏ đến một môi trường không bảo mật (non-production):
    *   **Rủi ro lộ thông tin nhạy cảm:** Dữ liệu nhạy cảm như `coupon_id` và token xác thực (`Authorization: Bearer ${token}`) có thể bị chặn bởi bất kỳ ai trong đường truyền mạng (ví dụ: attacker trên cùng mạng Wi-Fi công cộng).
    *   **Tiềm năng tấn công tiếp theo:** Dữ liệu bị lộ có thể cho phép kẻ tấn công giả mạo người dùng, thực hiện các hành động không mong muốn hoặc khai thác các lỗ hổng khác.

    Tuy nhiên, nếu đây là môi trường lab và `API_URL` được cấu hình trỏ đến `http://localhost:port_number`, rủi ro cho người dùng cuối là rất thấp.

4.  **Cách khắc phục cụ thể:**
    Để khắc phục triệt để và đảm bảo an toàn, dù là môi trường nào, nên ưu tiên áp dụng các biện pháp sau:

    *   **Sử dụng HTTPS cho tất cả các dịch vụ API:**
        *   **Cấu hình Server:** Đảm bảo các API backend đang chạy trên kết nối HTTPS và được cấu hình với chứng chỉ SSL/TLS hợp lệ.
        *   **Cấu hình Client (Frontend):** Cập nhật biến môi trường `API_URL` để luôn trỏ đến phiên bản `https` của API. Ví dụ:
            ```javascript
            // Ví dụ: Thay thế bằng cấu hình phù hợp cho từng môi trường
            const API_URL = process.env.NODE_ENV === 'production'
                ? 'https://api.your-eshop.com'
                : 'http://localhost:5000'; // Hoặc https://localhost:5001 nếu backend chạy https trên local
            ```
        *   **Kiểm tra lại Rule Semgrep:** Sau khi triển khai HTTPS, Semgrep rule này sẽ không còn cảnh báo hoặc cảnh báo sai nếu được cấu hình để chỉ soi xét các URL không phải `https`.

    *   **Cân nhắc về độ nhạy cảm của dữ liệu:**
        *   Nếu `coupon_id` không thực sự nhạy cảm, việc truyền qua HTTP trên mạng nội bộ có thể chấp nhận được trong môi trường lab. Tuy nhiên, việc phát hiện sớm là quan trọng để tránh việc vô tình đặt `API_URL` sai trong môi trường production.

5.  **Ghi chú cần tester kiểm tra thêm nếu chưa đủ context:**
    *   **Kiểm tra định nghĩa và giá trị của `API_URL`:** Tester cần xác định `API_URL` đang trỏ đến địa chỉ nào trong môi trường đang được quét. Cụ thể, nó có phải là `http://localhost:port` hay một URL công cộng?
    *   **Xác định môi trường triển khai:** Đây là môi trường phát triển (dev), kiểm thử (staging) hay sản xuất (production)? Điều này ảnh hưởng trực tiếp đến mức độ rủi ro.
    *   **Kiểm tra cấu hình HTTPS trên Backend:** Nếu `API_URL` là một URL công cộng, cần xác minh rằng backend API tương ứng đã được cấu hình sử dụng HTTPS.
    *   **Xác nhận tính nhạy cảm của dữ liệu:** `coupon_id` và `Authorization` token có được coi là nhạy cảm trong bối cảnh này hay không?

---

## Checklist kiểm chứng thủ công

- Xác nhận finding có nằm trong code được chạy/deploy thật hay không.
- Kiểm tra các finding trùng root cause để gom lại khi viết báo cáo cuối.
- Reproduce bằng PoC hoặc runtime request nếu finding phụ thuộc hành vi chạy thật.
- Chỉ chốt `True Positive`, `False Positive`, hoặc `Needs Human Review` sau khi có đủ context.
- Gắn source evidence, log, screenshot hoặc ZAP/Postman evidence nếu có.
