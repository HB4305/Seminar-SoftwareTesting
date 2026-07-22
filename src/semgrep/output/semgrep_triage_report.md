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
Tuyệt vời! Với vai trò là chuyên gia bảo mật ứng dụng, tôi sẽ tiến hành phân loại (triage) finding SEMGREP-001 này.

```markdown
## Phân loại Finding Bảo mật - SEMGREP-001

**1. Phân loại:** True Positive

**2. Lý do phân loại dựa trên source evidence:**

Finding SEMGREP-001 với Rule ID `javascript.jsonwebtoken.security.jwt-hardcode.hardcoded-jwt-secret` đã phát hiện một credential bị hardcode trực tiếp trong mã nguồn tại file `eshop-sut/backend/server.js`, dòng 51: `const token = jwt.sign({ id: user.id, role: user.role }, SECRET_KEY);`.

*   **Mã nguồn chứng minh:** Dòng này rõ ràng sử dụng `SECRET_KEY` trực tiếp trong hàm `jwt.sign`. Dù giá trị cụ thể của `SECRET_KEY` không hiển thị trong đoạn trích bạn cung cấp, việc biến này không được khai báo là một biến môi trường, không được đọc từ file cấu hình bảo mật, hay không được lấy từ một dịch vụ quản lý bí mật (vault/HSM) cho thấy nó có khả năng cao là một chuỗi bí mật được định nghĩa trực tiếp trong file mã nguồn.
*   **Rule ID và CWE/OWASP:** Rule ID này nhắm đến việc mã hóa cứng bí mật (hardcoded credentials), tương ứng với CWE-798 (`Use of Hard-coded Credentials`) và nằm trong các hạng mục lỗ hổng liên quan đến Xác thực (Authentication Failures) của OWASP.
*   **Ngữ cảnh file:** File `server.js` được mô tả là "entrypoint runtime backend", có nghĩa là nó là một phần quan trọng của ứng dụng chạy ở phía server. Việc một bí mật quan trọng để ký và xác minh JWT (JSON Web Token) bị hardcode trong runtime code là một rủi ro bảo mật nghiêm trọng.

**3. Tác động thực tế trong bối cảnh EShop:**

*   **Chiếm đoạt phiên làm việc (Session Hijacking):** Nếu `SECRET_KEY` bị lộ, kẻ tấn công có thể giả mạo các token JWT hợp lệ để truy cập trái phép vào hệ thống dưới danh nghĩa người dùng hoặc quản trị viên. Họ có thể thay đổi thông tin người dùng, thực hiện các giao dịch độc hại, hoặc leo thang đặc quyền.
*   **Phân tích nguồn mở:** Nếu mã nguồn bị lộ ra bên ngoài (ví dụ: qua các kho mã công khai, lỗi cấu hình server, hoặc nội bộ), `SECRET_KEY` sẽ bị lộ ngay lập tức. Dù ứng dụng đang quét là "lab local", việc cho phép thực hành này tiềm ẩn nguy cơ khi phát triển lên môi trường production.
*   **Mất lòng tin:** Lỗ hổng này cho thấy sự thiếu cẩn trọng trong quản lý bí mật, có thể làm giảm niềm tin của người dùng và đối tác vào tính bảo mật của EShop.

**4. Cách khắc phục cụ thể:**

Thay vì hardcode `SECRET_KEY` trực tiếp trong mã nguồn, hãy áp dụng các phương pháp quản lý bí mật an toàn:

*   **Sử dụng Biến môi trường (Environment Variables):** Đây là phương pháp phổ biến và được khuyến khích.
    *   Khai báo biến môi trường trên server của bạn (ví dụ: `JWT_SECRET_KEY`).
    *   Trong code, đọc giá trị của biến môi trường này:
        ```javascript
        const SECRET_KEY = process.env.JWT_SECRET_KEY;
        
        // Kiểm tra xem biến môi trường có tồn tại không
        if (!SECRET_KEY) {
          console.error('FATAL ERROR: JWT_SECRET_KEY is not defined.');
          process.exit(1); // Thoát ứng dụng nếu bí mật không được cấu hình
        }
        
        // ... sau đó sử dụng SECRET_KEY như bình thường
        const token = jwt.sign({ id: user.id, role: user.role }, SECRET_KEY);
        ```
*   **Sử dụng Dịch vụ Quản lý Bí mật (Secrets Management Services):** Đối với các môi trường phức tạp hơn hoặc yêu cầu bảo mật cao hơn, hãy tích hợp với các hệ thống quản lý bí mật như:
    *   AWS Secrets Manager
    *   Azure Key Vault
    *   Google Cloud Secret Manager
    *   HashiCorp Vault
    *   Sử dụng Hardware Security Module (HSM) cho quản lý khóa bảo mật cao nhất.

**5. Ghi chú cần tester kiểm tra thêm nếu chưa đủ context:**

*   **Xác nhận giá trị của `SECRET_KEY`:** Mặc dù Semgrep cảnh báo về việc hardcode, tester nên kiểm tra xem `SECRET_KEY` có thực sự là một chuỗi bí mật được sử dụng để ký JWT hay chỉ là một biến tạm thời cho mục đích phát triển demo và có khả năng sẽ bị thay thế trong thực tế hay không. Tuy nhiên, ngay cả khi là demo, việc này vẫn không phải là Best Practice.
*   **Môi trường Deployment:** Vì hiện tại đang quét "ứng dụng lab local", tester cần xác nhận xem cấu hình deployment dự kiến cho môi trường **production** có xử lý `SECRET_KEY` một cách an toàn (qua biến môi trường, vault, v.v.) hay không. Nếu `server.js` chỉ chạy trong môi trường dev/lab và không bao giờ được deploy sang production, việc đánh giá rủi ro có thể thay đổi. Tuy nhiên, Semgrep với Severity `WARNING` và Confidence `HIGH` vẫn khuyến khích sửa lỗi này để áp dụng các thực hành tốt nhất ngay từ đầu.
*   **Tầm ảnh hưởng của `SECRET_KEY`:** Liệu `SECRET_KEY` này chỉ dùng để đóng dấu token cho các hoạt động đọc thông tin người dùng đơn giản, hay còn dùng để ký cho các token có quyền hành cao (ví dụ: token quản trị, token reset mật khẩu)? Tác động sẽ lớn hơn nếu nó dùng cho các hành động nhạy cảm.
```

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
Tuyệt vời! Với vai trò là chuyên gia bảo mật ứng dụng, tôi sẽ tiến hành **triage** cho finding SEMGREP-002 mà bạn cung cấp.

```markdown
### Triage Finding Bảo Mật SEMGREP-002

**1. Phân loại:** Needs Human Review

**2. Lý do phân loại dựa trên source evidence:**

Semgrep Rule ID `javascript.jsonwebtoken.security.jwt-hardcode.hardcoded-jwt-secret` đã phát hiện một chuỗi bí mật (credential) được nhúng trực tiếp trong mã nguồn tại dòng 105 của file `eshop-sut/backend/server.js`. Cụ thể, biến `SECRET_KEY` đang được truyền trực tiếp vào hàm `jwt.verify`. Rule này đánh dấu đây là một lỗ hổng bảo mật thuộc CWE-798 (Use of Hard-coded Credentials) và liên quan đến OWASP A07:2021/A07:2025.

Nhiều khả năng đây là một **True Positive** về mặt kỹ thuật vì mã nguồn rõ ràng là đang sử dụng một chuỗi có vẻ là bí mật để xác minh token JWT. Tuy nhiên, do ngữ cảnh được cung cấp là "ứng dụng lab local", chúng ta cần thêm thông tin để xác định mức độ rủi ro thực tế.

**3. Tác động thực tế trong bối cảnh EShop:**

*   **Nếu EShop là ứng dụng production (hoặc có nguy cơ bị tấn công trên môi trường không an toàn):** Việc nhúng `SECRET_KEY` trực tiếp trong mã nguồn là một rủi ro **MEDIUM** về **Impact**. Nếu mã nguồn bị lộ ra ngoài (ví dụ: qua ransomware, mã độc, hoặc nhà phát triển thiếu cẩn trọng), kẻ tấn công có thể dễ dàng truy cập vào khóa bí mật này. Với khóa bí mật này, kẻ tấn công có thể:
    *   Tạo ra các token JWT giả mạo, cho phép họ xác thực thành công với ứng dụng mà không cần biết bất kỳ thông tin xác thực hợp lệ nào.
    *   Thay đổi nội dung của các token JWT hiện có, dẫn đến việc ủy quyền trái phép (ví dụ: thay đổi thông tin người dùng, thực hiện giao dịch thay mặt người khác).
    *   Trong trường hợp xấu nhất, có thể leo thang quyền truy cập, truy cập dữ liệu nhạy cảm, hoặc thực hiện các hành động độc hại khác.
*   **Nếu EShop là ứng dụng chỉ chạy trong môi trường lab local an toàn và không bao giờ deploy ra ngoài (với mục đích demo):** Rủi ro tấn công từ bên ngoài là thấp. Tuy nhiên, vẫn tồn tại rủi ro từ nội bộ (ví dụ: nhà phát triển có ý đồ xấu hoặc vô ý làm lộ mã nguồn).

**4. Cách khắc phục cụ thể:**

1.  **Ưu tiên cao nhất:** Thay thế chuỗi `SECRET_KEY` nhúng cứng bằng cách lấy nó từ các nguồn an toàn hơn:
    *   **Biến môi trường (Environment Variables):** Đây là phương pháp phổ biến và được khuyến nghị. Thay vì:
        ```javascript
        const SECRET_KEY = "that_super_secret_key_that_should_never_be_hardcoded"; // Dòng 105 tương tự
        ```
        Hãy sử dụng:
        ```javascript
        const SECRET_KEY = process.env.JWT_SECRET_KEY;
        if (!SECRET_KEY) {
          // Xử lý lỗi khi biến môi trường không được thiết lập
          console.error("FATAL ERROR: JWT_SECRET_KEY is not defined.  Abort, or die.");
          process.exit(1); // Thoát ứng dụng nếu không có key
        }
        ```
        Và thiết lập biến môi trường `JWT_SECRET_KEY` trên server khi deploy.
    *   **Hệ thống quản lý bí mật (Secrets Management System):** Đối với các môi trường phức tạp hơn, sử dụng các dịch vụ như HashiCorp Vault, AWS Secrets Manager, Azure Key Vault để lưu trữ và truy xuất các khóa bí mật một cách an toàn.

2.  **Tạo biến môi trường riêng:** Tạo một file `.env` (và thêm nó vào `.gitignore` để tránh vô tình commit lên repo) để định nghĩa `JWT_SECRET_KEY` cho môi trường phát triển và staging.

3.  **Sử dụng thư viện quản lý cấu hình:** Cân nhắc sử dụng các thư viện như `dotenv` để dễ dàng tải cấu hình từ file `.env` trong môi trường phát triển.

**5. Ghi chú cần tester kiểm tra thêm nếu chưa đủ context:**

*   **Xác nhận môi trường deploy:** Đây là **ứng dụng lab local** hay là bản **staging/production**? Nếu là lab, mức độ ưu tiên khắc phục có thể giảm (nhưng vẫn nên làm), nếu là staging/production thì đây là lỗ hổng nghiêm trọng cần khắc phục ngay.
*   **Mục đích của `SECRET_KEY`:** Xác nhận rằng `SECRET_KEY` này *thực sự* được sử dụng để ký và xác minh token JWT của ứng dụng. Đôi khi, các chuỗi tương tự có thể là mẫu hoặc chưa được sử dụng.
*   **File nguồn:** `eshop-sut/backend/server.js` là entrypoint runtime backend. Việc nhúng secret ở đây có nghĩa là nó **rất có thể reachable** trong runtime.
*   **Trường hợp đặc biệt:** Tìm kiếm xem `SECRET_KEY` này có được khai báo trong một file cấu hình (config file) riêng biệt và được inject vào thông qua một cơ chế an toàn, hay nó thực sự là một hằng số hardcoded? (Tuy nhiên, dựa vào dòng code, nó có vẻ là hardcoded).
*   **Kiểm tra lại tất cả các findings tương tự:** Nếu có nhiều finding tương tự báo cáo về việc hardcoded secrets, chúng nên được xem xét cùng một lúc và có thể cùng một nguyên nhân gốc rễ (ví dụ: khai báo chung trong một file cấu hình, hoặc thiếu quy trình quản lý secret).
```

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
Tuyệt vời! Với vai trò là một chuyên gia bảo mật ứng dụng, tôi sẽ tiến hành triage finding SEMGREP-003 này một cách cẩn thận. Dưới đây là phân tích chi tiết:

---

##### Triage Finding Bảo Mật: SEMGREP-003

**1. Phân loại:** `Needs Human Review`

**2. Lý do phân loại dựa trên source evidence:**

*   **Mã nguồn vi phạm:** Dòng `4` trong file `eshop-sut/backend/test_profile.js` hiển thị rõ ràng việc sử dụng một chuỗi bí mật `super_secret_key_that_should_not_be_here` được mã hóa cứng trực tiếp trong mã nguồn để ký JWT.
*   **Rule ID và CWE/OWASP:** Rule `javascript.jsonwebtoken.security.jwt-hardcode.hardcoded-jwt-secret` và các liên kết đến `CWE-798` cùng `OWASP A07:2021 (Authentication Failures)` đều chỉ ra rằng mã hóa cứng thông tin xác thực là một vấn đề bảo mật nghiêm trọng.
*   **Ngữ cảnh file:** Thông tin quan trọng nhất ở đây là vai trò của file `test_profile.js`. Theo mô tả, đây là "mã test/helper". Điều này làm giảm mức độ nghiêm trọng ngay lập tức, vì mã test thường không được triển khai trong môi trường production và có thể có mức độ bảo mật khác với mã ứng dụng chính.
*   **Môi trường triển khai:** Finding này liên quan đến việc gọi một endpoint `http://localhost:3000`. Điều này gợi ý rằng mã này có thể chỉ đang chạy trong môi trường phát triển (development) hoặc môi trường lab cục bộ. Nếu EShop được quét *chỉ* là một ứng dụng lab local, thì rủi ro của việc này có thể thấp hơn. Tuy nhiên, rủi ro vẫn tồn tại nếu mã test này có khả năng được sử dụng hoặc tái sử dụng trong các ngữ cảnh khác nhạy cảm hơn.
*   **JWT Usage:** Việc secret này dùng để ký JWT cho mục đích gì (ví dụ: ký cho user đăng nhập, hay chỉ là một token test tạm thời) cần được làm rõ. Nếu secret này được dùng để ký các token xác thực người dùng thực sự trong môi trường production, thì mức độ nghiêm trọng sẽ tăng lên đáng kể. Tuy nhiên, với ngữ cảnh "test_profile.js", việc này có thể chỉ là để phục vụ kịch bản test.

Vì vai trò của file là "test/helper" và endpoint được gọi là `localhost`, chúng ta chưa thể kết luận `True Positive` ngay lập tức mà không có thêm thông tin về cách file này được sử dụng trong vòng đời phát triển và triển khai của ứng dụng. Tuy nhiên, nó cũng không hoàn toàn là `False Positive` vì bản thân việc mã hóa cứng secret **là** một lỗ hổng tiềm ẩn, chỉ là mức độ rủi ro phụ thuộc vào ngữ cảnh sử dụng thực tế.

**3. Tác động thực tế trong bối cảnh EShop:**

*   **Môi trường Development/Lab:** Nếu file `test_profile.js` chỉ chạy trong môi trường phát triển cục bộ để thực hiện các bài test, việc mã hóa cứng secret này ít gây ra rủi ro trực tiếp cho người dùng cuối hoặc hệ thống production. Tuy nhiên, nó tạo ra một tiền lệ xấu và có thể dẫn đến việc làm tương tự ở những nơi thực sự nhạy cảm hơn.
*   **Rò rỉ thông tin:** Nếu file mã nguồn này (bất kể vai trò của nó) bị lộ ra ngoài (ví dụ: qua một commit public nhầm, hoặc một lỗ hổng ở nơi lưu trữ mã nguồn), kẻ tấn công có thể lấy được secret này. Tùy thuộc vào cách secret được sử dụng (để ký hay chỉ để xác minh), kẻ tấn công có thể tạo ra các token giả mạo, mạo danh người dùng hợp lệ, hoặc thậm chí làm suy yếu cơ chế xác thực của ứng dụng nếu cùng một secret được dùng ở nhiều nơi.
*   **Rủi ro cho môi trường nhạy cảm hơn:** Nếu mã `test_profile.js` vô tình được import hoặc gọi bởi một phần khác của ứng dụng có thể chạy trong môi trường staging hoặc thậm chí production (mặc dù ít khả năng), thì secret này sẽ bị lộ ra ngoài môi trường production, gây ra rủi ro nghiêm trọng.

**4. Cách khắc phục cụ thể:**

*   **Loại bỏ secret khỏi mã nguồn:** Thay vì mã hóa cứng, hãy sử dụng các phương pháp quản lý bí mật an toàn.
*   **Sử dụng biến môi trường (Environment Variables):** Đây là phương pháp phổ biến và hiệu quả nhất. Thay đổi dòng code 4 thành:
    ```javascript
    const token = jwt.sign({ id: 2, role: 'user' }, process.env.JWT_SECRET);
    ```
    Sau đó, thiết lập biến môi trường `JWT_SECRET` với một chuỗi bí mật mạnh mẽ ở cấp độ hệ thống hoặc container trong môi trường triển khai.
*   **Sử dụng Vault/Secrets Manager:** Đối với các ứng dụng phức tạp hơn hoặc yêu cầu bảo mật cao, hãy cân nhắc việc sử dụng các dịch vụ quản lý bí mật như HashiCorp Vault, AWS Secrets Manager, Azure Key Vault, Google Secret Manager, hoặc HSM (Hardware Security Module). Secret sẽ được lưu trữ an toàn và ứng dụng sẽ truy xuất nó khi cần thiết.
*   **Xóa mã test không cần thiết:** Nếu `test_profile.js` là một phần của mã nguồn production hoặc là mã test không còn được sử dụng, hãy cân nhắc xóa nó để giảm thiểu bề mặt tấn công.

**5. Ghi chú cần tester kiểm tra thêm nếu chưa đủ context:**

*   **Vai trò và sự triển khai của `test_profile.js`:**
    *   File này có thực sự chỉ được sử dụng trong môi trường phát triển local hay không?
    *   Nó có được đưa vào bản build production hoặc có thể được gọi bởi các phần code khác của ứng dụng trong môi trường staging/production không?
    *   Ai là người chịu trách nhiệm quản lý và triển khai file này?
*   **Mục đích của việc tạo token trong file này:**
    *   Token này có dùng để test các chức năng xác thực liên quan đến JWT production hay chỉ là một token mock cho mục đích test độc lập?
    *   Secret `super_secret_key_that_should_not_be_here` có *duy nhất* trong file này hay có thể là secret chung được dùng ở đâu đó khác trong code base? (Semgrep có thể sẽ phát hiện các trường hợp tương tự ở các file khác).
*   **Cấu hình JWT của ứng dụng:**
    *   Secret này có phải là secret *thực tế* được sử dụng để ký và xác minh token trong môi trường production hay chỉ là một giá trị thử nghiệm tạm thời trong file test?
    *   Làm thế nào ứng dụng EShop quản lý JWT secrets trong môi trường production? (Ví dụ: có sử dụng biến môi trường hoặc vault không).

Việc xác định rõ các yếu tố trên sẽ giúp đưa ra kết luận cuối cùng là `True Positive` hoặc `False Positive` và điều chỉnh mức độ ưu tiên xử lý. Tuy nhiên, đề xuất sửa đổi theo hướng an toàn hơn (sử dụng biến môi trường) luôn là một thực hành tốt.

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
Tuyệt vời! Với vai trò là chuyên gia bảo mật ứng dụng, tôi sẽ tiến hành triage finding này dựa trên thông tin bạn cung cấp.

```markdown
## Triage Finding Bảo Mật: SEMGREP-004

**1. Phân loại:** Needs Human Review

**2. Lý do phân loại dựa trên source evidence:**

Finding này chỉ ra **Unencrypted request over HTTP detected** tại dòng 174 trong file `App.js`, gửi request tới `${API_URL}/orders/my-orders`. Rule Semgrep và CWE đều liên quan đến việc truyền dữ liệu nhạy cảm qua kênh không mã hóa. Mã nguồn cho thấy việc sử dụng `fetch` API để gửi request đến `API_URL` với header `Authorization` chứa token.

Tuy nhiên, việc phân loại **False Positive** hay **True Positive** còn phụ thuộc nhiều vào ngữ cảnh triển khai và giá trị của `API_URL`.
*   Nếu `API_URL` trỏ đến một localhost hoặc một URL được cấu hình để chỉ sử dụng trong môi trường phát triển (dev/lab), nơi mà mạng nội bộ được kiểm soát và không có nguy cơ bị nghe lén, thì đây có thể được xem là **False Positive** đối với môi trường production.
*   Ngược lại, nếu `API_URL` có thể trỏ đến một endpoint của production hoặc staging mà vẫn sử dụng HTTP thay vì HTTPS, và dữ liệu nhạy cảm (như `currentToken` và thông tin đơn hàng) được truyền đi, thì đây sẽ là một **True Positive**.

Chúng ta chưa có đủ thông tin về cách `API_URL` được định nghĩa và cấu hình trong các môi trường khác nhau của EShop.

**3. Tác động thực tế trong bối cảnh EShop:**

Nếu `API_URL` thực sự đang gọi qua HTTP và truyền tải dữ liệu nhạy cảm, tác động có thể bao gồm:
*   **Lộ thông tin nhạy cảm:** Token xác thực (`currentToken`) và chi tiết đơn hàng có thể bị kẻ tấn công trong cùng một mạng (ví dụ: mạng Wi-Fi công cộng) đọc trộm.
*   **Giả mạo danh tính:** Kẻ tấn công có thể sử dụng token bị lộ để thực hiện các hành vi trái phép nhân danh người dùng.
*   **Can thiệp dữ liệu:** Dữ liệu truyền đi có thể bị thay đổi trên đường truyền (man-in-the-middle attack).

Tuy nhiên, do EShop được quét như ứng dụng lab local, nếu `API_URL` chỉ định có thể dẫn đến localhost hoặc URL dev, rủi ro cho môi trường production thực tế có thể thấp hoặc không tồn tại.

**4. Cách khắc phục cụ thể:**

*   **Ưu tiên sử dụng HTTPS:** Đảm bảo tất cả các endpoint API mà ứng dụng tương tác đều được truy cập thông qua HTTPS.
    *   **Cấu hình server:** Đảm bảo server backend của EShop được cấu hình để phục vụ API qua HTTPS.
    *   **Cấu hình client (ứng dụng mobile):** Mặc dù Semgrep đang báo cáo về phía client, nguyên nhân gốc rễ có thể nằm ở server. Tuy nhiên, trong trường hợp frontend mobile chủ động gửi request qua HTTP, cần kiểm tra lại cách `API_URL` được định nghĩa.
*   **Kiểm tra cấu hình `API_URL`:** Xác định giá trị của `API_URL` trong các môi trường khác nhau (dev, staging, production).
    *   Nếu ứng dụng mobile được phép sử dụng HTTP cho localhost, đây có thể là hành vi mong muốn cho môi trường dev, nhưng *cần đảm bảo rằng nó không bao giờ được sử dụng cho production*.
    *   Nếu `API_URL` được định nghĩa động dựa trên biến môi trường hoặc cấu hình, cần kiểm tra xem liệu có khả năng nó được trỏ đến một endpoint không an toàn trong production hay không.
*   **Strict Transport Security (HSTS) (nếu áp dụng cho web):** Mặc dù đây là ứng dụng mobile, nếu có liên quan đến tương tác web view, HSTS là một biện pháp giúp trình duyệt chỉ cho phép kết nối HTTPS.

**5. Ghi chú cần tester kiểm tra thêm nếu chưa đủ context:**

*   **Giá trị thực tế của `API_URL`:** Tester cần kiểm tra giá trị của biến `API_URL` trong code hoặc thông qua quá trình build/deploy các môi trường khác nhau của EShop.
*   **Môi trường triển khai:** Xác nhận EShop đang chạy trong môi trường lab local như mô tả hay có khả năng là môi trường staging/production được sử dụng để thử nghiệm.
*   **Cấu hình mạng:** Nếu EShop đang chạy trên môi trường mạng bị kiểm soát (isolated network) như trong lab, thì rủi ro nghe lén là rất thấp.
*   **Sensitive Data:** Kiểm tra xem token `currentToken` và thông tin trả về từ `my-orders` có thực sự chứa dữ liệu cực kỳ nhạy cảm cần bảo vệ tối đa hay không.
```

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
Tuyệt vời! Hãy cùng tôi phân tích finding bảo mật này.

##### Phân Tích Finding Bảo Mật SEMGREP-005

##### 1. Phân loại:
`Needs Human Review`

##### 2. Lý do phân loại dựa trên source evidence:
Semgrep rule `typescript.react.security.react-insecure-request.react-insecure-request` phát hiện một yêu cầu mạng được thực hiện qua giao thức HTTP thay vì HTTPS, cụ thể tại dòng 189 của file `eshop-sut/frontend-mobile/App.js`. Yêu cầu này đang gửi thông tin đăng nhập (email và password) tới endpoint `/login` của API.

Tuy nhiên, bằng chứng mã nguồn cho thấy biến `API_URL` được sử dụng để xây dựng URL cho request. Giá trị của `API_URL` không được hiển thị trong đoạn mã cung cấp. Trong bối cảnh "ứng dụng lab local" và việc tìm kiếm liên quan đến `localhost`, có khả năng `API_URL` được cấu hình chỉ để trỏ đến môi trường phát triển cục bộ, nơi mà việc sử dụng HTTP là phổ biến và chấp nhận được để giảm thiểu sự phức tạp trong quá trình phát triển.

Nếu `API_URL` chỉ đơn thuần là `http://localhost:PORT` hoặc `http://127.0.0.1:PORT`, và API server cũng đang chạy trên cùng môi trường này, thì việc truyền dữ liệu nhạy cảm qua HTTP trong môi trường lab cục bộ này có thể không gây ra rủi ro bảo mật đáng kể ngay lập tức, vì lưu lượng mạng không đi qua mạng công cộng.

Tuy nhiên, nếu `API_URL` có thể được cấu hình để trỏ đến một máy chủ API khác (thậm chí là trong mạng nội bộ nhưng có thể bị giám sát) hoặc nếu ứng dụng này có thể được triển khai trong một môi trường mà `API_URL` trỏ đến một máy chủ công cộng hoặc không đáng tin cậy, thì đây sẽ là một lỗ hổng bảo mật nghiêm trọng.

Do đó, việc xác định liệu `API_URL` có được cấu hình cho môi trường production hay không, và liệu server API có sử dụng HTTPS hay không, là rất quan trọng để đưa ra quyết định cuối cùng.

##### 3. Tác động thực tế trong bối cảnh EShop:
Nếu `API_URL` trỏ đến một endpoint không bảo mật qua HTTPS, thì thông tin đăng nhập của người dùng (email và password) sẽ được truyền dưới dạng văn bản thuần túy qua mạng. Điều này có thể dẫn đến:

*   **Nghe lén dữ liệu nhạy cảm:** Kẻ tấn công có thể chặn và đọc trộm thông tin đăng nhập, cho phép họ truy cập trái phép vào tài khoản của người dùng.
*   **Xác thực yếu:** Nếu thông tin đăng nhập bị lộ, kẻ tấn công có thể sử dụng chúng để thực hiện các hành vi gian lận hoặc chiếm đoạt tài khoản.
*   **Lỗ hổng liên quan đến OWASP:** Điều này trực tiếp vi phạm OWASP A03:2017 (Sensitive Data Exposure) và A02:2021 (Cryptographic Failures), cũng như A04:2025 (Cryptographic Failures).

Tuy nhiên, như đã đề cập, nếu đây chỉ là môi trường lab sử dụng `localhost`, tác động này bị giảm nhẹ đáng kể.

##### 4. Cách khắc phục cụ thể:
*   **Ưu tiên cấu hình API_URL sử dụng HTTPS:** Đảm bảo rằng tất cả các yêu cầu tới server API đều được thực hiện qua giao thức HTTPS. Điều này bao gồm việc cấu hình server API để sử dụng chứng chỉ SSL/TLS.
*   **Cập nhật biến API\_URL:** Nếu biến `API_URL` có thể được cấu hình, hãy đảm bảo rằng nó luôn trỏ đến một endpoint sử dụng HTTPS. Ví dụ, thay vì `http://api.example.com`, sử dụng `https://api.example.com`.
*   **Kiểm tra môi trường deploy:** Đối với các môi trường production, staging, và các môi trường không phải là lab local, **bắt buộc** phải sử dụng HTTPS.
*   **Sử dụng các thư viện HTTP an toàn:** Nếu có thể, hãy cân nhắc sử dụng các thư viện hoặc module trong React Native (hoặc framework khác) chuyên để quản lý các yêu cầu mạng, có thể có các cơ chế cấu hình an toàn mặc định hoặc dễ dàng hơn.

##### 5. Ghi chú cần tester kiểm tra thêm nếu chưa đủ context:
*   **Xác định giá trị thực tế của `API_URL`:** Tester cần tìm hiểu xem biến `API_URL` được khởi tạo như thế nào và giá trị của nó là gì trong các ngữ cảnh triển khai khác nhau (dev, staging, production).
*   **Kiểm tra server API:** Xác nhận xem server API mà `eshop-sut` kết nối tới có hỗ trợ và được cấu hình để sử dụng HTTPS hay không. Nếu chỉ có HTTP, thì cần khắc phục ở phía server API trước.
*   **Chính sách bảo mật của tổ chức:** Tìm hiểu xem có các yêu cầu bảo mật cụ thể nào đối với việc truyền dữ liệu nhạy cảm trong môi trường của EShop không.

Việc phân loại `Needs Human Review` là phù hợp nhất cho đến khi các thông tin trên được làm rõ. Nếu sau khi kiểm tra, `API_URL` luôn trỏ đến `localhost` và không có ý định deploy ra môi trường bên ngoài, có thể phân loại lại thành `False Positive`. Ngược lại, nếu `API_URL` có thể trỏ đến các endpoint không bảo mật, nó sẽ là `True Positive`.

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
Tuyệt vời! Với vai trò là chuyên gia bảo mật ứng dụng, tôi sẽ phân tích finding SEMGREP-006 này.

---

##### Phân tích Finding Bảo mật SEMGREP-006

**1. Phân loại:** Needs Human Review

**2. Lý do phân loại dựa trên source evidence:**

*   **Bằng chứng mã nguồn (Source Evidence):** Dòng 222 trong file `eshop-sut/frontend-mobile/App.js` hiển thị một lời gọi `fetch` đến `${API_URL}/register`. Điều này rõ ràng là một yêu cầu mạng được thực hiện.
*   **Rule ID và Cảnh báo Semgrep:** Rule `typescript.react.security.react-insecure-request.react-insecure-request` và cảnh báo "Unencrypted request over HTTP detected" chỉ ra rằng vấn đề tiềm ẩn là yêu cầu này có thể được gửi qua HTTP thay vì HTTPS.
*   **CWE và OWASP:** Các liên kết đến CWE-319 (Cleartext Transmission of Sensitive Information) và các phiên bản OWASP về "Sensitive Data Exposure" hoặc "Cryptographic Failures" càng củng cố nhận định rằng việc truyền dữ liệu nhạy cảm qua kênh không mã hóa là một rủi ro bảo mật.
*   **Context "EShop đang được quét như ứng dụng lab local; finding liên quan localhost cần kiểm tra môi trường trước khi kết luận rủi ro cuối."**: Đây là yếu tố quan trọng nhất dẫn đến phân loại "Needs Human Review". Việc sử dụng `${API_URL}` mà không rõ giá trị thực tế của nó là nguyên nhân chính.
    *   Nếu `API_URL` được cấu hình để trỏ đến một server chạy trên `localhost` hoặc môi trường staging/dev và chỉ sử dụng HTTP, thì đây có thể **chỉ là một vấn đề trong môi trường lab/dev** và không ảnh hưởng đến môi trường production nếu production sử dụng HTTPS.
    *   Ngược lại, nếu `API_URL` có thể được cấu hình hoặc trỏ đến một endpoint trong môi trường production sử dụng HTTP, thì đây sẽ là **True Positive**.

Do đó, Semgrep đã phát hiện một mẫu mã *có tiềm năng* gây ra lỗ hổng dựa trên rule bảo mật. Tuy nhiên, để xác định xem nó có thực sự là một lỗ hổng (True Positive) hay không, chúng ta cần biết cách biến `API_URL` được cấu hình và sử dụng trong các môi trường khác nhau.

**3. Tác động thực tế trong bối cảnh EShop:**

*   **Nếu Production sử dụng HTTP cho `${API_URL}/register`:** Có thể xảy ra rủi ro lộ lọt thông tin đăng ký nhạy cảm (tên, email) của người dùng cho kẻ tấn công trong quá trình truyền dữ liệu. Đối với một ứng dụng thương mại điện tử (E-commerce), điều này có thể dẫn đến danh tính người dùng bị đánh cắp, spam hoặc các cuộc tấn công nhắm mục tiêu khác.
*   **Nếu Production sử dụng HTTPS cho `${API_URL}/register` (hoặc `API_URL` chỉ dùng cho môi trường dev/lab):** Tác động thực tế là rất thấp hoặc bằng không, vì dữ liệu đã được mã hóa bởi TLS/SSL. Tuy nhiên, việc có mã tiềm năng sử dụng HTTP có thể là dấu hiệu của quy trình quản lý cấu hình chưa chặt chẽ.

**4. Cách khắc phục cụ thể:**

1.  **Kiểm tra cấu hình `API_URL`:**
    *   Xác định giá trị của biến môi trường hoặc hằng số `API_URL`.
    *   Kiểm tra xem biến này được cấu hình như thế nào trong các môi trường (development, staging, production).
    *   **Quan trọng nhất:** Đảm bảo rằng trong môi trường production, `API_URL` luôn sử dụng giao thức `https://`.

2.  **Cập nhật mã nguồn (Nếu cần):**
    *   Nếu `API_URL` có thể bị cấu hình sai để sử dụng HTTP trong production, nên có cơ chế kiểm tra hoặc sử dụng một biến khác rõ ràng hơn cho production.
    *   Trong trường hợp lý tưởng, mã nguồn nên được viết theo cách luôn ưu tiên HTTPS hoặc có logic để tự động chuyển đổi dựa trên cấu hình môi trường. Ví dụ:

    ```javascript
    // Giả định API_URL là một biến có thể bị cấu hình là http://localhost:port
    const useHTTPS = process.env.NODE_ENV !== 'development'; // Hoặc kiểm tra biến môi trường khác
    const protocol = useHTTPS ? 'https' : 'http';
    const apiBase = `${protocol}://${API_URL}`; // API_URL có thể chỉ là domain:port

    // Hoặc đơn giản hơn nếu API_URL đã bao gồm cả scheme
    const finalApiUrl = API_URL.startsWith('http://') ? API_URL.replace('http://', 'https://') : API_URL;

    const response = await fetch(`${finalApiUrl}/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
        name: registerName,
        email: registerEmail,
        }),
    });
    ```
    Tuy nhiên, cách kiểm tra cấu hình `API_URL` là ưu tiên hàng đầu.

**5. Ghi chú cần tester kiểm tra thêm:**

*   **Kiểm tra môi trường Development/Lab:** Xác nhận liệu `API_URL` có đang trỏ tới một server local qua HTTP hay không. Nếu có, đây là hành vi dự kiến cho môi trường test/lab và cần được hiểu là không phải rủi ro cho production.
*   **Kiểm tra cấu hình Production:** Xác minh các biến môi trường hoặc file cấu hình cho môi trường production để đảm bảo `API_URL` được thiết lập với giao thức `https://`.
*   **Văn hóa phát triển:** Đánh giá xem có các đoạn mã tương tự khác trong dự án có thể tiềm ẩn cùng một vấn đề hay không. Việc này giúp đảm bảo tính nhất quán trong việc áp dụng các biện pháp bảo mật.

Sau khi có thêm thông tin về cấu hình thực tế của `API_URL`, chúng ta có thể đưa ra phân loại cuối cùng là True Positive hoặc False Positive. Hiện tại, "Needs Human Review" là lựa chọn phù hợp nhất.

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
Dưới đây là kết quả triage cho finding SEMGREP-007:

---

##### Triage Finding Bảo Mật: SEMGREP-007

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

##### 1. Phân loại: Needs Human Review

##### 2. Lý do phân loại dựa trên source evidence.

Bằng chứng mã nguồn tại dòng 244 cho thấy một yêu cầu `fetch` được gửi đến `API_URL` với endpoint `/forgot-password`. Semgrep đã phát hiện rằng yêu cầu này có thể đang được gửi qua giao thức HTTP không được mã hóa, dựa trên việc không có dấu hiệu rõ ràng của việc sử dụng HTTPS hoặc các cơ chế mã hóa khác tại thời điểm gửi request. Rule `react-insecure-request` được thiết kế để cảnh báo về các yêu cầu HTTP không an toàn, đặc biệt là khi có khả năng lộ lọt thông tin nhạy cảm.

Tuy nhiên, điều quan trọng là `API_URL` là một biến môi trường hoặc hằng số được định nghĩa ở nơi khác. Bối cảnh "EShop đang được quét như ứng dụng lab local; finding liên quan localhost cần kiểm tra môi trường trước khi kết luận rủi ro cuối." là yếu tố then chốt cho việc phân loại này. Nếu `API_URL` được cấu hình trỏ đến `localhost` hoặc một URL nội bộ chỉ sử dụng trong môi trường development hoặc lab, việc sử dụng HTTP có thể chấp nhận được và không gây ra rủi ro bảo mật thực tế cho người dùng cuối. Ngược lại, nếu `API_URL` có thể được cấu hình để trỏ đến một endpoint public hoặc trong môi trường production mà không sử dụng HTTPS, đây sẽ là một lỗ hổng nghiêm trọng.

Do Semgrep là SAST và không có khả năng kiểm tra cấu hình `API_URL` hoặc ngữ cảnh triển khai cụ thể (như đã nêu trong ghi chú "chưa rõ config, deploy usage..."), chúng ta chưa thể đưa ra kết luận cuối cùng về việc đây là *True Positive* hay *False Positive* chỉ dựa trên mã nguồn tĩnh.

##### 3. Tác động thực tế trong bối cảnh EShop.

Trong bối cảnh một ứng dụng EShop, chức năng "Quên mật khẩu" thường liên quan đến việc xử lý địa chỉ email của người dùng, một loại thông tin cá nhân có thể được coi là nhạy cảm (đặc biệt khi kết hợp với các dữ liệu khác). Nếu URL `API_URL` thực sự trỏ đến một máy chủ không sử dụng HTTPS, thông tin email được gửi đi có thể bị chặn và đọc bởi kẻ tấn công trong mạng (ví dụ: tấn công man-in-the-middle).

Tuy nhiên, vì đây là ứng dụng lab local, tác động thực tế *tại thời điểm này* có thể là **thấp**, chủ yếu dừng lại ở việc minh họa một sai lầm trong cấu hình hoặc thiết kế có thể dẫn đến rủi ro nếu được triển khai sai trong môi trường production. Nếu tiến trình forgot-password được thực hiện trên một mạng không tin cậy và không được mã hóa, Impact có thể **trung bình** vì lộ lọt email có thể dẫn đến các cuộc tấn công giả mạo hoặc phishing sau này.

##### 4. Cách khắc phục cụ thể.

1.  **Ưu tiên Hàng đầu (Nếu `API_URL` dẫn đến endpoint public/production):**
    *   **Đảm bảo sử dụng HTTPS:** Cập nhật cấu hình `API_URL` để luôn sử dụng `https://` thay vì `http://`. Điều này yêu cầu máy chủ API phải được cấu hình để hỗ trợ TLS/SSL.
    *   **Kiểm tra cấu hình `API_URL`:** Xác minh cách `API_URL` được định nghĩa và truyền vào ứng dụng. Nếu nó là một biến môi trường, hãy đảm bảo biến môi trường đó được thiết lập đúng với giao thức HTTPS trong mọi môi trường, đặc biệt là production.
    *   **Cập nhật mã nguồn:** Thay đổi dòng 244 (và bất kỳ nơi nào khác sử dụng `API_URL` cho các yêu cầu không mã hóa) để đảm bảo giao thức là HTTPS. Ví dụ: `const response = await fetch(`https://${API_URL}/forgot-password`...` hoặc tốt hơn là cấu hình `API_URL` bao gồm cả giao thức.

2.  **Nếu `API_URL` chỉ dành cho môi trường Local/Dev/Lab:**
    *   **Giữ nguyên như hiện tại nhưng ghi chú rõ ràng:** Document hóa rõ ràng rằng việc sử dụng HTTP tại đây là có chủ ý cho môi trường lab và không nên được sử dụng cho production.
    *   **Cân nhắc sử dụng các công cụ proxy hoặc debugger mật mã:** Trong môi trường lab, đôi khi người ta cố tình sử dụng HTTP để dễ dàng theo dõi lưu lượng. Tuy nhiên, cần lưu ý về rủi ro tiềm ẩn.

##### 5. Ghi chú cần tester kiểm tra thêm nếu chưa đủ context.

*   **Xác định giá trị thực tế của `API_URL`:** Phỏng vấn hoặc kiểm tra file cấu hình/biến môi trường để biết `API_URL` đang trỏ đến đâu trong môi trường quét hiện tại.
    *   Nếu là `http://localhost:...` hoặc một địa chỉ IP nội bộ
    *   Nếu là một tên miền public hoặc có thể truy cập qua Internet.
*   **Kiểm tra mục đích của mã nguồn:** File `App.js` là file runtime chính của ứng dụng. Do đó, các dòng code ở đây có khả năng cao được thực thi trong quá trình sử dụng ứng dụng.
*   **Môi trường triển khai:** Tuy nhiên, do ngữ cảnh "ứng dụng lab local", cần làm rõ xem "lab" có bao gồm cả việc mô phỏng môi trường production hay chỉ là một môi trường phát triển đơn giản.
*   **Kiểm tra các API calls khác:** Xem xét liệu có các yêu cầu HTTP không mã hóa khác trong ứng dụng hay không, đặc biệt là những yêu cầu có thể gửi thông tin nhạy cảm hơn.

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
Tuyệt vời, tôi sẽ đóng vai trò là chuyên gia bảo mật ứng dụng để phân tích finding này từ Semgrep.

Dưới đây là kết quả triage:

---

##### Triage Finding SEMGREP-008

**1. Phân loại:** Needs Human Review

**2. Lý do phân loại dựa trên source evidence:**

*   **Bằng chứng mã nguồn:** Rule `typescript.react.security.react-insecure-request.react-insecure-request` phát hiện một lệnh gọi `fetch` đến `${API_URL}/reset-password` mà không có yếu tố mã hóa (HTTP thay vì HTTPS).
*   **Ngữ cảnh `API_URL`:** Biến `API_URL` này được định nghĩa ở đâu đó trong ứng dụng. Nếu `API_URL` được cấu hình để trỏ đến `http://localhost:<port>` hoặc một URL tương tự trên môi trường phát triển (dev) hoặc lab, thì việc sử dụng HTTP là chấp nhận được trong môi trường đó, vì lưu lượng mạng được cách ly và không dễ bị nghe lén bởi kẻ tấn công bên ngoài.
*   **Môi trường EShop:** Thông tin cho biết EShop đang được quét như một ứng dụng lab local. Điều này củng cố khả năng `API_URL` đang trỏ đến localhost.
*   **Chưa rõ ràng về Production:** Tuy nhiên, Semgrep SAST chỉ phân tích mã tĩnh. Chúng ta không có thông tin đầy đủ về cách `API_URL` được cấu hình trong môi trường production. Nếu `API_URL` có thể được cấu hình để trỏ đến một máy chủ không được mã hóa trong môi trường production, thì đây sẽ là một lỗ hổng thực sự.
*   **Độ nhạy cảm của dữ liệu:** Việc gửi token reset mật khẩu và mật khẩu mới qua mạng không được mã hóa là một rủi ro bảo mật đáng kể. Nếu kẻ tấn công có thể nghe lén lưu lượng truy cập, họ có thể chiếm đoạt tài khoản người dùng.

**3. Tác động thực tế trong bối cảnh EShop:**

*   **Môi trường Lab/Dev:** Nếu `API_URL` chỉ trỏ đến localhost trong môi trường lab/dev, tác động thực tế là rất thấp. Điều này chủ yếu phục vụ mục đích kiểm tra nội bộ.
*   **Môi trường Production:** Nếu `API_URL` trỏ đến một endpoint không sử dụng HTTPS trong môi trường production, tác động có thể là **Medium** (theo đánh giá của Semgrep). Điều này có nghĩa là dữ liệu nhạy cảm (email, reset token, mật khẩu mới) có thể bị lộ cho kẻ tấn công nghe lén mạng (man-in-the-middle attack). Điều này có thể dẫn đến việc chiếm đoạt tài khoản người dùng, dẫn đến các tổn thất về tài chính hoặc danh tiếng.

**4. Cách khắc phục cụ thể:**

*   **Xác minh cấu hình `API_URL`:** Kiểm tra cách biến `API_URL` được cấu hình cho môi trường production.
*   **Ưu tiên HTTPS:** Đảm bảo rằng tất cả các yêu cầu mạng từ ứng dụng di động đến API backend **luôn** sử dụng HTTPS. Điều này bao gồm cả môi trường phát triển, staging và production càng sớm càng tốt.
*   **Cập nhật mã nguồn (nếu cần):**
    *   Nếu `API_URL` đang được định nghĩa sai hoặc có khả năng bị cấu hình sai trong production, hãy **buộc sử dụng URL có HTTPS** hoặc thêm logic kiểm tra để đảm bảo protocol là HTTPS.
    *   Trong trường hợp một môi trường phát triển cụ thể yêu cầu IP nội bộ thay vì tên miền, hãy cân nhắc sử dụng một biến cấu hình riêng cho môi trường đó và đảm bảo rằng nó cũng được bảo vệ (ví dụ: thông qua VPN hoặc các biện pháp bảo mật khác của mạng nội bộ).
*   **Sử dụng thư viện để quản lý API requests:** Nâng cao trên việc sử dụng `fetch` đơn giản, xem xét sử dụng các thư viện như Axios với cấu hình mặc định cho HTTPS và các interceptor để xử lý lỗi hoặc thêm header bảo mật.

**5. Ghi chú cần tester kiểm tra thêm nếu chưa đủ context:**

*   **Nguồn gốc của `API_URL`:** Cần xác định rõ biến `API_URL` được khai báo và cấu hình ở đâu, và cách nó được quản lý qua các môi trường (dev, staging, production).
    *   Có file cấu hình riêng cho từng môi trường không?
    *   Biến môi trường (environment variables) có được sử dụng không? Nếu có, cách nó được thiết lập trên server/build pipeline?
*   **Cấu hình của máy chủ API backend:** Máy chủ backend mà `API_URL` trỏ tới có đang lắng nghe trên cổng HTTPS không?
*   **Purpose của `http://localhost` trong môi trường Dev/Lab:** Nếu `API_URL` được định nghĩa cố định là `http://localhost...` cho môi trường dev, thì việc *không* sử dụng HTTPS ở đây có thể là một **False Positive** nếu việc truy cập được kiểm soát chặt chẽ trong môi trường phát triển đó. Tuy nhiên, vẫn cần **cảnh báo** về thói quen này và khuyến khích sử dụng HTTPS ngay cả khi dev.
*   **Kiểm tra lại các finding tương tự:** Nếu Semgrep đưa ra nhiều cảnh báo tương tự cho các endpoint API khác, chúng có thể có cùng một nguyên nhân gốc rễ.

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
Tuyệt vời! Với vai trò là chuyên gia bảo mật ứng dụng, tôi sẽ tiến hành triage finding SEMGREP-009 này.

##### Triage Finding Bảo Mật - SEMGREP-009

##### 1. Phân loại:
Needs Human Review

##### 2. Lý do phân loại dựa trên source evidence:

Bằng chứng mã nguồn tại dòng 296 của file `eshop-sut/frontend-mobile/App.js` cho thấy một lời gọi `fetch` đến `${API_URL}/users/me` với phương thức `PUT`. Cùng với đó, chúng ta thấy rằng `API_URL` đang được sử dụng và có thể không phải lúc nào cũng là `https`.

Tuy nhiên, việc phân loại là `True Positive` hay `False Positive` còn phụ thuộc vào ngữ cảnh triển khai cụ thể của `API_URL` và môi trường mà ứng dụng EShop đang chạy.

*   **Nguy cơ tiềm ẩn:** Rule Semgrep cảnh báo về việc truyền thông tin nhạy cảm qua HTTP không mã hóa (CWE-319). Nếu `API_URL` được cấu hình để trỏ đến một endpoint không sử dụng HTTPS, thông tin nhạy cảm như token có thể bị lộ.
*   **Thiếu ngữ cảnh:**
    *   Chúng ta không biết giá trị thực tế của biến `$API_URL` trong môi trường triển khai. Nếu `$API_URL` luôn được cấu hình với `https://` (ví dụ: `https://localhost:3000` hoặc một URL sản phẩm), thì cảnh báo này có thể là `False Positive` cho vấn đề truyền dữ liệu không mã hóa.
    *   Do đây là ứng dụng "lab local", việc sử dụng `http://localhost` có thể chỉ phục vụ mục đích phát triển ban đầu và không được kỳ vọng sử dụng trong môi trường sản phẩm. Tuy nhiên, việc kiểm tra xem môi trường sản phẩm có bị ảnh hưởng hay không là rất quan trọng.
    *   Chúng ta không có thông tin về cách thức cấu hình `API_URL`. Nó có thể được hardcode, lấy từ biến môi trường, hoặc cấu hình từ một file khác.
    *   Độ nhạy cảm của dữ liệu truyền tải trong request `PUT .../users/me` cần được xác minh rõ ràng. Token `Authorization: Bearer ${token}` chắc chắn là nhạy cảm, nhưng bản thân payload của request đó là gì (nếu có) cũng cần được xem xét.

Do những yếu tố thiếu ngữ cảnh này, việc đưa ra quyết định cuối cùng mà không có thêm thông tin là không thể, do đó `Needs Human Review` là lựa chọn phù hợp nhất.

##### 3. Tác động thực tế trong bối cảnh EShop:

Nếu `API_URL` trỏ đến một endpoint sử dụng giao thức **HTTP** thay vì **HTTPS**, và thông tin nhạy cảm (như token xác thực) được truyền đi unsecured, tác động có thể bao gồm:

*   **Lộ thông tin xác thực:** Kẻ tấn công có thể chặn và đọc token xác thực của người dùng, cho phép họ mạo danh người dùng đó truy cập vào tài khoản.
*   **Lộ dữ liệu người dùng:** Nếu request `PUT` này bao gồm các thông tin cá nhân khác của người dùng, những thông tin đó cũng có thể bị lộ.
*   **Mất lòng tin của người dùng:** Lộ thông tin bảo mật sẽ gây ảnh hưởng nghiêm trọng đến uy tín của ứng dụng và doanh nghiệp.

Tuy nhiên, như đã phân tích ở trên, nếu ứng dụng chỉ giao tiếp qua HTTPS hoặc môi trường lab dùng HTTP không truyền data nhạy cảm hoặc không đi ra ngoài môi trường được cô lập chặt chẽ, thì tác động thực tế có thể bị giảm thiểu hoặc không tồn tại.

##### 4. Cách khắc phục cụ thể:

1.  **Xác minh cấu hình `API_URL`:**
    *   Kiểm tra cách biến `API_URL` được định nghĩa và cấu hình trong ứng dụng EShop.
    *   Ưu tiên sử dụng **HTTPS** cho mọi endpoint API. Cập nhật `API_URL` để luôn bắt đầu bằng `https://`.
2.  **Áp dụng HTTPS:** Đảm bảo rằng cả máy chủ backend (nơi API được host) và giao tiếp mạng được cấu hình để sử dụng TLS/SSL (HTTPS).
3.  **Kiểm tra chính sách mạng (nếu có):** Nếu ứng dụng chạy trong một môi trường mạng cụ thể, hãy đảm bảo rằng các yêu cầu không bị chặn và được cho phép đi qua các cổng HTTPS tiêu chuẩn.
4.  **Lấy lại hoặc cập nhật Access Token:** Sau khi áp dụng HTTPS, người dùng có thể cần đăng nhập lại để nhận được một token mới, đảm bảo rằng các giao dịch tiếp theo được bảo mật.
5.  **Re-triage:** Sau khi đã áp dụng các biện pháp này, chạy lại quét Semgrep để xác nhận rằng finding đã được khắc phục.

##### 5. Ghi chú cần tester kiểm tra thêm nếu chưa đủ context:

*   **Kiểm tra giá trị của `API_URL`:** Yêu cầu tester hoặc người chịu trách nhiệm kiểm tra giá trị thực tế của biến `API_URL` trong các môi trường khác nhau (dev, staging, production). Đặc biệt chú trọng xem nó có bắt đầu bằng `http://` hay không.
*   **Môi trường Lab Local:** Xác nhận xem ứng dụng EShop có được dự định triển khai trên môi trường production thực tế hay chỉ là môi trường lab để thử nghiệm. Nếu chỉ là lab, cần làm rõ liệu việc sử dụng HTTP có tạo ra rủi ro bảo mật trong môi trường đó hay không (ví dụ: nếu lab này có thể truy cập từ bên ngoài hoặc chứa dữ liệu nhạy cảm).
*   **Kiểm tra Request Payload:** Nếu có thể (thường cần debug runtime), hãy kiểm tra xem request `PUT ${API_URL}/users/me` này có bao gồm bất kỳ dữ liệu nhạy cảm nào khác ngoài token hay không.
*   **Chính sách bảo mật của EShop:** Tìm hiểu xem EShop có quy định bắt buộc sử dụng HTTPS cho tất cả các giao tiếp mạng hay không.

Việc thu thập thêm thông tin từ các điểm trên sẽ giúp đưa ra phân loại chính xác và đưa ra hành động khắc phục hiệu quả nhất.

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
Tuyệt vời, tôi sẽ đóng vai trò chuyên gia bảo mật ứng dụng để triage finding này cho bạn.

---

##### Triage Finding Bảo Mật: SEMGREP-010

##### 1. Phân loại: Needs Human Review

##### 2. Lý do phân loại dựa trên source evidence:

*   **Bằng chứng Source Code:** Semgrep phát hiện một yêu cầu `fetch` được thực hiện đến `${API_URL}/apply-coupon` sử dụng phương thức `POST` với `Content-Type: application/json`. Rule `react-insecure-request` trong Semgrep được thiết kế để cảnh báo khi có các yêu cầu truyền dữ liệu nhạy cảm qua HTTP không mã hóa.
*   **Ngữ cảnh `API_URL`:** Biến `API_URL` không được hiển thị trong đoạn trích mã nguồn. Đây là yếu tố then chốt để xác định xem yêu cầu có thực sự đang được gửi qua HTTP hay không. Nếu `API_URL` được cấu hình là `http://localhost:<port>` hoặc `http://127.0.0.1:<port>` trong môi trường phát triển (dev/lab), thì yêu cầu này có thể không gây ra rủi ro bảo mật thực sự cho người dùng cuối, vì nó chỉ tương tác với server cục bộ. Tuy nhiên, nếu `API_URL` được cấu hình là một tên miền hoặc địa chỉ IP không sử dụng HTTPS, hoặc nếu cấu hình này có thể thay đổi trong môi trường production, thì đây là một lỗ hổng nghiêm trọng.
*   **Độ nhạy cảm Dữ liệu:** Dữ liệu được gửi đi bao gồm `couponCode` (mã giảm giá) và `cartTotal` (tổng giỏ hàng). Mặc dù không phải là thông tin nhạy cảm cực kỳ cao như mật khẩu hay thông tin thẻ tín dụng, nhưng việc lộ mã giảm giá và tổng giá trị đơn hàng cũng có thể gây ra một số rủi ro phụ như:
    *   Kẻ tấn công có thể lợi dụng để tìm hiểu các mã giảm giá hiện có hoặc đang hoạt động.
    *   Trong một số kịch bản phức tạp hơn, thông tin này có thể là một phần của chuỗi tấn công để hiểu hành vi người dùng hoặc cấu trúc giao dịch.
*   **Context Deploy:** Việc EShop đang được quét như ứng dụng lab local là một điểm quan trọng. Tuy nhiên, Semgrep là SAST, nó phân tích mã tĩnh. Kết luận về rủi ro thực tế phụ thuộc rất nhiều vào cách `API_URL` được định cấu hình và triển khai trong các môi trường khác nhau (dev, staging, production).

Do thiếu thông tin về cấu hình thực tế của `API_URL` và môi trường triển khai, chúng ta không thể kết luận ngay đây là True Positive hay False Positive.

##### 3. Tác động thực tế trong bối cảnh EShop:

*   **Nếu `API_URL` trỏ đến `http://localhost`:** Tác động bảo mật trong môi trường lab local là rất thấp hoặc không có, vì lưu lượng truy cập chỉ diễn ra giữa ứng dụng frontend trên thiết bị và server API chạy trên máy tính của nhà phát triển. Tuy nhiên, nếu cấu hình này vô tình được giữ nguyên hoặc lặp lại trong môi trường production mà không sử dụng HTTPS, thì tác động sẽ **trung bình (MEDIUM)**.
*   **Nếu `API_URL` trỏ đến một endpoint không sử dụng HTTPS (không phải localhost):** Tác động sẽ là **trung bình (MEDIUM)**. Kẻ tấn công có thể nghe lén (eavesdrop) trên mạng để đọc được mã giảm giá và tổng giỏ hàng khi chúng được gửi đi. Điều này có thể tạo điều kiện cho các hoạt động gian lận liên quan đến khuyến mãi hoặc cung cấp thông tin cho các cuộc tấn công nhắm mục tiêu sâu hơn.
*   **Rủi ro cho dữ liệu nhạy cảm:** Theo CWE-319 và OWASP A03:2017/A02:2021, việc truyền dữ liệu nhạy cảm qua kênh không mã hóa là một lỗ hổng chính. Mặc dù `couponCode` và `cartTotal` có thể không được coi là "nhạy cảm tối đa", chúng vẫn là thông tin có thể bị khai thác.

##### 4. Cách khắc phục cụ thể:

1.  **Xác định và kiểm tra cấu hình `API_URL`:**
    *   Tìm kiếm biến `API_URL` trong toàn bộ mã nguồn dự án, bao gồm cả các file cấu hình môi trường (ví dụ: `.env`, `config.js`, v.v.).
    *   Xác minh xem `API_URL` có đang sử dụng giao thức `https` hay không.

2.  **Ưu tiên sử dụng HTTPS:**
    *   Nếu `API_URL` được cấu hình cho môi trường production, hãy đảm bảo nó luôn được đặt thành một URL sử dụng `https`.
    *   Nếu `API_URL` có thể là `http://localhost` cho môi trường dev, xem xét việc:
        *   Đảm bảo server API local cũng chạy qua HTTPS (sử dụng certificate tự ký cho môi trường dev).
        *   Hoặc, nếu chỉ cho mục đích test thuần túy, hãy chấp nhận rủi ro thấp này nhưng **tuyệt đối không được để nó tồn tại trong môi trường staging hoặc production**.

3.  **Cập nhật Rule (nếu cần):**
    *   Trong trường hợp `API_URL` trỏ đến `http://localhost` và được coi là an toàn trong ngữ cảnh dev, bạn có thể cần điều chỉnh các rule Semgrep hoặc thêm logic để loại trừ các yêu cầu tới `localhost` hoặc `127.0.0.1` khỏi việc cảnh báo cho rule này, tùy thuộc vào chính sách bảo mật của bạn. Tuy nhiên, hãy cân nhắc kỹ lưỡng để tránh che giấu các lỗ hổng thực sự.

4.  **Sử dụng Content Security Policy (CSP) và các biện pháp bảo mật mạng khác:**
    *   Tuy không trực tiếp khắc phục cách thức truyền dữ liệu, việc áp dụng CSP có thể giúp hạn chế các truy cập không mong muốn đến các endpoint API, giảm thiểu nguy cơ bị tấn công Man-in-the-Middle (MITM) nếu có khai thác nào khác.

##### 5. Ghi chú cần tester kiểm tra thêm nếu chưa đủ context:

*   **Yêu cầu Tester/DevOps:** Cần làm rõ cách thức triển khai biến `API_URL` cho từng môi trường (Development, Staging, Production).
*   **Kiểm tra Trực quan:** Nếu có thể, tiến hành kiểm tra trực quan bằng cách thử nghiệm chức năng áp dụng mã giảm giá trong ứng dụng và sử dụng công cụ network inspector (trên trình duyệt nếu là web app hoặc các công cụ proxy như Charles Proxy, mitmproxy cho mobile app) để xem request thực tế được gửi đi có sử dụng HTTPS hay không.
*   **Đánh giá Độ nhạy cảm Dữ liệu:** Cần có một đánh giá chính thức về mức độ nhạy cảm của thông tin `couponCode` và `cartTotal` trong bối cảnh kinh doanh cụ thể của EShop để có thể ưu tiên xử lý. Tuy nhiên, theo nguyên tắc phòng ngừa, việc truyền bất kỳ dữ liệu nào có thể nhận dạng người dùng hoặc giao dịch qua kênh không mã hóa đều là điều nên tránh.

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
Tuyệt vời! Với vai trò là chuyên gia bảo mật ứng dụng, tôi sẽ tiến hành triage finding SEMGREP-011 này một cách cẩn trọng.

##### Triage Finding SEMGREP-011

##### 1. Phân loại

```
Needs Human Review
```

##### 2. Lý do phân loại dựa trên source evidence.

Dựa trên bằng chứng mã nguồn và ngữ cảnh được cung cấp, việc phân loại ban đầu là "Needs Human Review" xuất phát từ các lý do sau:

*   **API_URL là biến môi trường:** Dòng code `fetch(${API_URL}/checkout, ...)` sử dụng biến `API_URL`. Semgrep SAST chỉ phân tích tĩnh mã nguồn và không thể xác định giá trị thực tế của `API_URL` lúc runtime. Nếu `API_URL` được cấu hình là một endpoint sử dụng HTTP (không mã hóa) và có thể truy cập từ bên ngoài môi trường tin cậy (ví dụ: production), thì đây có thể là một lỗ hổng thực sự. Ngược lại, nếu `API_URL` luôn trỏ đến `localhost` hoặc một endpoint nội bộ được phục vụ qua HTTPS, thì rủi ro sẽ giảm đáng kể.
*   **Ngữ cảnh EShop là ứng dụng lab local:** Thông tin này rất quan trọng. Việc Semgrep phát hiện request qua HTTP tới `localhost` có thể chỉ phản ánh môi trường phát triển hoặc lab, nơi mà bảo mật hạ tầng (như SSL/TLS) có thể chưa được áp dụng đầy đủ hoặc không cần thiết trong môi trường kiểm thử nội bộ. Tuy nhiên, điều này cần được xác nhận.

Semgrep đã chính xác phát hiện hành vi sử dụng giao thức HTTP cho một request, và quy tắc này được thiết kế để cảnh báo về việc truyền dữ liệu nhạy cảm qua kênh không mã hóa. Tuy nhiên, mức độ rủi ro thực tế phụ thuộc hoàn toàn vào cách `API_URL` được định cấu hình và loại mạng mà ứng dụng EShop đang hoạt động.

##### 3. Tác động thực tế trong bối cảnh EShop.

Nếu `API_URL` trỏ đến một endpoint HTTP bên ngoài mạng nội bộ tin cậy, và dữ liệu truyền đi (`finalAmount`, `token`) là nhạy cảm, thì tác động có thể bao gồm:

*   **Nghe lén thông tin nhạy cảm:** Kẻ tấn công có thể chặn và đọc các thông tin như:
    *   Tổng số tiền cuối cùng (`finalAmount`) có thể tiết lộ thông tin về giá trị đơn hàng, hành vi mua sắm của người dùng.
    *   Token xác thực (`token` trong header `Authorization`) nếu bị lộ có thể cho phép kẻ tấn công mạo danh người dùng, thực hiện các hành động trái phép thay mặt người dùng, hoặc truy cập vào các tài nguyên nhạy cảm khác.
*   **Tấn công Man-in-the-Middle (MiTM):** Kẻ tấn công có thể sửa đổi dữ liệu truyền đi, ví dụ: thay đổi `finalAmount` để gây gian lận.
*   **Lộ lọt dữ liệu theo OWASP A03:2017 và A02:2021:** Việc truyền thông tin nhạy cảm qua kênh không mã hóa trực tiếp vi phạm các nguyên tắc về bảo mật dữ liệu nhạy cảm và mã hóa.

Tuy nhiên, nếu EShop chỉ chạy trong môi trường lab local và `API_URL` luôn là `localhost`, tác động thực tế có thể rất thấp hoặc bằng không, miễn là không có ai khác truy cập vào mạng local đó một cách trái phép và có ý đồ xấu.

##### 4. Cách khắc phục cụ thể.

Cách khắc phục được đề xuất chủ yếu tập trung vào việc đảm bảo tất cả các giao tiếp mạng đều được mã hóa, đặc biệt là khi truyền dữ liệu nhạy cảm.

*   **Sử dụng HTTPS cho API_URL:**
    *   **Cấu hình mã hóa ở Backend:** Đảm bảo rằng API backend tại `${API_URL}/checkout` được triển khai với HTTPS và chứng chỉ SSL/TLS hợp lệ.
    *   **Cấu hình biến môi trường:** Trong môi trường production, biến môi trường `API_URL` **phải** được thiết lập để trỏ đến một endpoint sử dụng HTTPS. Ví dụ: `https://api.eshop.com/`.
*   **Kiểm tra kỹ cấu hình biến môi trường:**
    *   **Trong môi trường Production:** Xác nhận rằng `API_URL` được thiết lập thành một endpoint HTTPS.
    *   **Trong môi trường Dev/Lab:** Nếu việc sử dụng HTTP là cần thiết cho mục đích phát triển/lab và bạn có thể đảm bảo rằng môi trường này được cách ly và không có nguy cơ bị tấn công từ bên ngoài, thì cần có ghi chú rõ ràng cho việc này. Tuy nhiên, nên hướng tới việc sử dụng HTTPS ngay cả trong môi trường lab để giảm thiểu thói quen sử dụng kênh không mã hóa.
*   **Xử lý lỗi kết nối HTTPS:** Đảm bảo ứng dụng có cơ chế xử lý lỗi khi không thể kết nối qua HTTPS.

##### 5. Ghi chú cần tester kiểm tra thêm nếu chưa đủ context.

Để có thể đưa ra kết luận phân loại cuối cùng (True Positive hay False Positive), các điểm sau cần được tester kiểm tra chi tiết:

*   **Giá trị thực tế của `API_URL` trong môi trường Production:** Tester cần xác định giá trị cụ thể mà biến môi trường `API_URL` nhận được khi triển khai ứng dụng EShop ở môi trường Production.
*   **Cấu hình SSL/TLS cho Endpoint Backend:** Kiểm tra xem endpoint API backend mà `API_URL` trỏ tới có đang sử dụng HTTPS hay không. Nếu có, chứng chỉ có hợp lệ và được tin cậy không?
*   **Ngữ cảnh mạng của EShop:** EShop đang chạy trong môi trường mạng nào? Nó có được triển khai trong một mạng nội bộ (VLAN) được kiểm soát an ninh, hay nó có khả năng bị truy cập từ Internet công cộng? Nếu là môi trường production, việc sử dụng HTTP cho bất kỳ request nào (ngay cả `localhost`) cần được xem xét kỹ lưỡng hơn, vì các công cụ hoặc dịch vụ khác có thể can thiệp.
*   **Tính nhạy cảm của dữ liệu truyền đi:** Mặc dù `finalAmount` và `token` có vẻ nhạy cảm, tester nên xác nhận xem có bất kỳ dữ liệu nhạy cảm khác nào khác được gửi trong request `POST /checkout` hoặc ngầm hiểu qua ngữ cảnh của `cartTotal` và `couponResult` hay không.

Sau khi có những thông tin này, chúng ta sẽ có đủ cơ sở để xác định đây là True Positive (lỗ hổng thực sự cần khắc phục) hay False Positive (không phải là rủi ro trong ngữ cảnh triển khai).

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
Tuyệt vời! Hãy cùng tôi tiến hành triage finding SEMGREP-012 này.

---

##### Triage Finding: SEMGREP-012

**1. Phân loại:** Needs Human Review

**2. Lý do phân loại dựa trên source evidence:**

Dựa trên bằng chứng mã nguồn được cung cấp, Semgrep đã phát hiện một yêu cầu `fetch` được thực hiện thông qua HTTP (không có HTTPS) đến một endpoint `/coupon-usage` với `API_URL` không rõ ràng, nhưng dòng 400 chỉ ra rằng nó có thể là một endpoint API của ứng dụng. Rule Semgrep cảnh báo về việc "Unencrypted request over HTTP detected", phù hợp với CWE-319.

Tuy nhiên, việc phân loại đây là `True Positive` hay `False Positive` phụ thuộc vào ngữ cảnh triển khai và cách biến `API_URL` được định nghĩa và sử dụng:

*   **Ngữ cảnh `localhost` và `lab local`:** Thông tin cho biết "EShop đang được quét như ứng dụng lab local; finding liên quan localhost cần kiểm tra môi trường trước khi kết luận rủi ro cuối." và "HTTP localhost có thể chỉ dùng cho dev/lab; chỉ phân loại False Positive khi source/config chứng minh production không bị ảnh hưởng." Điều này rất quan trọng. Nếu `API_URL` chỉ trỏ đến `localhost` hoặc một môi trường phát triển/thử nghiệm nội bộ mà không truyền dữ liệu nhạy cảm, hoặc dữ liệu đó đã được bảo vệ bằng các biện pháp khác tại cấp độ mạng nội bộ, thì rủi ro có thể không cao như mô tả.
*   **Độ nhạy cảm của dữ liệu:** Yêu cầu này gửi kèm theo `token` trong header `Authorization`. Token này, nếu là token xác thực người dùng, có thể được coi là dữ liệu nhạy cảm. Việc truyền token này qua HTTP không mã hóa có thể khiến nó bị lộ cho kẻ tấn công trong cùng mạng.
*   **Khả năng `API_URL` là HTTPS:** Chúng ta không có định nghĩa của `API_URL` trong đoạn mã cung cấp. Nếu `API_URL` được định nghĩa và luôn sử dụng `https://` trong môi trường production, thì đây sẽ là `False Positive` ở môi trường đó. Tuy nhiên, nếu nó có thể bao gồm `http://` trong môi trường production hoặc các môi trường khác, thì rủi ro là có thật.

Do sự không chắc chắn về cách `API_URL` được cấu hình và môi trường triển khai thực tế (sử dụng `http` hay `https`), việc phân loại là `Needs Human Review` là phù hợp nhất.

**3. Tác động thực tế trong bối cảnh EShop:**

Nếu `API_URL` trỏ đến một endpoint hợp lệ và được truy cập qua HTTP không mã hóa, tác động có thể là:

*   **Rò rỉ thông tin xác thực (Token):** Token được truyền trong header `Authorization` có thể bị nghe lén (man-in-the-middle attack) bởi bất kỳ ai có thể truy cập vào cùng mạng với thiết bị người dùng hoặc máy chủ API. Nếu token này là token xác thực người dùng, kẻ tấn công có thể sử dụng nó để mạo danh người dùng và thực hiện các hành động thay mặt họ, ví dụ như truy cập tài khoản, thực hiện giao dịch trái phép (nếu token cho phép).
*   **Rò rỉ dữ liệu thanh toán (Coupon):** Mặc dù không thấy thông tin thanh toán trực tiếp trong request này, nhưng nó liên quan đến việc sử dụng coupon. Nếu dữ liệu coupon hoặc thông tin liên quan đến giao dịch trong tương lai được truyền qua kênh không mã hóa này, chúng cũng có thể bị lộ.
*   **Rủi ro từ OWASP A03:2017 (Sensitive Data Exposure) và A02/A04:2021/2025 (Cryptographic Failures):** Mã này trực tiếp vi phạm nguyên tắc tránh lộ dữ liệu nhạy cảm và sử dụng mã hóa không đầy đủ.

Tuy nhiên, nếu đây chỉ là môi trường dev/lab với `localhost` và không có dữ liệu nhạy cảm thực, tác động thực tế có thể là **THẤP** hoặc **KHÔNG CÓ TÁC ĐỘNG** đến người dùng cuối của ứng dụng production.

**4. Cách khắc phục cụ thể:**

*   **Ưu tiên sử dụng HTTPS cho tất cả các request API:** Đây là cách khắc phục cơ bản và hiệu quả nhất. Đảm bảo rằng `API_URL` luôn được cấu hình để sử dụng giao thức `https://`.
    *   Kiểm tra định nghĩa và cách sử dụng của biến `API_URL`. Nếu biến này được lấy từ file cấu hình, biến môi trường, hoặc hardcode, hãy đảm bảo nó luôn bắt đầu bằng `https://`.
    *   Trong môi trường mobile, việc cấu hình cho phép các kết nối HTTPS là tiêu chuẩn và an toàn.
*   **Giới hạn scope của `API_URL`:** Nếu `API_URL` là biến môi trường, hãy đảm bảo nó chỉ được trỏ đến các endpoint an toàn trong môi trường production. Đối với môi trường local/dev, có thể sử dụng `http://localhost:PORT` nhưng cần hiểu rõ rủi ro và chỉ dùng cho mục đích phát triển.
*   **Kiểm tra các request khác:** Rà soát toàn bộ codebase để tìm kiếm các `fetch` hoặc các cuộc gọi mạng tương tự khác có khả năng sử dụng HTTP không mã hóa, đặc biệt là những request gửi kèm dữ liệu nhạy cảm (token, thông tin người dùng, thông tin thanh toán).

**5. Ghi chú cần tester kiểm tra thêm nếu chưa đủ context:**

Để có thể phân loại cuối cùng và đánh giá đúng mức độ rủi ro, tester cần kiểm tra thêm các điểm sau:

*   **Định nghĩa và giá trị của `API_URL`:** Tester cần tìm định nghĩa của biến `API_URL` và xác định giá trị thực tế của nó trong các môi trường khác nhau (development, staging, production).
    *   Nếu `API_URL` là một biến môi trường, cần kiểm tra cách nó được thiết lập.
    *   Kiểm tra xem `API_URL` có thể bao gồm `http://` hay không trong bất kỳ môi trường nào.
*   **Ngữ cảnh sử dụng `API_URL`:** Biến `API_URL` này có thể được sử dụng cho mục đích gì? Nó trỏ đến server API nội bộ, server bên thứ ba hay chỉ là server local cho mục đích debug?
*   **Tính nhạy cảm của Token:** Token được gửi trong header `Authorization` là loại token gì (ví dụ: JWT, session token)? Nó có thời hạn sử dụng không? Token này có được lưu trữ an toàn trên thiết bị không?
*   **Cấu hình lắng nghe của Server:** Nếu `API_URL` chỉ là `localhost` hoặc một IP nội bộ, liệu server API (nếu có) có đang lắng nghe trên cổng HTTP hay HTTPS?
*   **Tác động lên Production Environment:** Xác định xem phiên bản production của EShop có sử dụng `API_URL` này hay không và liệu nó có khả năng bị ảnh hưởng bởi traffic over HTTP không mã hóa hay không.

---

## Checklist kiểm chứng thủ công

- Xác nhận finding có nằm trong code được chạy/deploy thật hay không.
- Kiểm tra các finding trùng root cause để gom lại khi viết báo cáo cuối.
- Reproduce bằng PoC hoặc runtime request nếu finding phụ thuộc hành vi chạy thật.
- Chỉ chốt `True Positive`, `False Positive`, hoặc `Needs Human Review` sau khi có đủ context.
- Gắn source evidence, log, screenshot hoặc ZAP/Postman evidence nếu có.
