# Evidence: Semgrep Scan

Tài liệu này ghi lại phần evidence có thể thực hiện được với Semgrep dựa trên nội dung trong `docs/semgrep` và ảnh minh chứng trong `resources`.

## 1. Mục tiêu

- **Công cụ:** Semgrep SAST.
- **Target:** mã nguồn EShop backend.
- **Ruleset chính:** `p/owasp-top-ten`.
- **Mục đích:** quét mã nguồn tĩnh để phát hiện lỗi bảo mật, xuất kết quả JSON để phục vụ AI triage và ghi nhận finding có thể khai thác.

## 2. Chuẩn bị môi trường

### Windows PowerShell

```powershell
pip install semgrep
chcp 65001
$env:PYTHONUTF8='1'
```

### macOS / Linux

```bash
pip3 install semgrep
# hoặc
curl -fsSL https://semgrep.dev/get | sh
```

Kiểm tra cài đặt:

```bash
semgrep --version
```

## 3. Chạy scan cơ bản

Đứng tại thư mục source code cần kiểm thử, chạy:

```bash
semgrep scan --config "p/owasp-top-ten" .
```

Evidence output terminal:

![Semgrep scan output 1](image/scan/semgrep_test1.png)

![Semgrep scan output 2](image/scan/semgrep_test2.png)

## 4. Chạy scan và xuất JSON

Để dùng cho AI triage, cần xuất kết quả scan ra file JSON:

```bash
semgrep scan --config "p/owasp-top-ten" --json -o semgrep_results.json .
```

Có thể bổ sung ruleset cho dự án Node.js:

```bash
semgrep scan --config "p/owasp-top-ten" --config "p/nodejs" --json -o semgrep_results.json .
```

## 5. Kết quả finding chính

Finding được chọn để phân tích:

| Trường | Giá trị |
| --- | --- |
| Rule ID | `javascript.jsonwebtoken.security.jwt-hardcode.hardcoded-jwt-secret` |
| Severity | `WARNING` |
| File | `backend/server.js` |
| Dòng liên quan | `9`, `51`, `105` |
| CWE | CWE-798: Use of Hard-coded Credentials |
| OWASP | A07:2021 - Identification and Authentication Failures |

Source evidence:

```javascript
const SECRET_KEY = "super_secret_key_that_should_not_be_here";
const token = jwt.sign({ id: user.id, role: user.role }, SECRET_KEY);
jwt.verify(token, SECRET_KEY, (err, user) => { ... });
```

## 6. Nhận xét

Semgrep phát hiện được hardcoded JWT secret rất nhanh và chỉ rõ dòng code liên quan. Tuy nhiên, kết quả cần được triage để gộp các finding trùng root cause và xác định impact thực tế trước khi viết report cuối.
