# Finding Report: Hardcoded JWT Secret Key

## 1. Thông tin chung

- **Công cụ phát hiện:** Semgrep SAST.
- **Rule ID:** `javascript.jsonwebtoken.security.jwt-hardcode.hardcoded-jwt-secret`.
- **Severity từ công cụ:** `WARNING`.
- **CWE:** CWE-798: Use of Hard-coded Credentials.
- **OWASP:** A07:2021 - Identification and Authentication Failures.
- **Target:** EShop backend.

## 2. Mô tả

Backend Node.js đang lưu khóa bí mật dùng để ký và xác thực JWT trực tiếp trong mã nguồn. Khi secret bị hardcode, bất kỳ người nào đọc được source code hoặc lấy được bản backup/source bị rò rỉ đều có thể tự tạo token hợp lệ.

Source evidence:

```javascript
// backend/server.js
const SECRET_KEY = "super_secret_key_that_should_not_be_here";

const token = jwt.sign({ id: user.id, role: user.role }, SECRET_KEY);

jwt.verify(token, SECRET_KEY, (err, user) => {
  // verify token
});
```

## 3. Triage

Semgrep có thể báo nhiều vị trí liên quan đến cùng một secret:

- `server.js:9`: khai báo `SECRET_KEY` hardcoded.
- `server.js:51`: dùng secret để ký JWT bằng `jwt.sign`.
- `server.js:105`: dùng secret để xác thực JWT bằng `jwt.verify`.

Các cảnh báo này nên được gộp thành **1 root cause**: secret JWT bị hardcode trong source code.

## 4. Proof of Concept

PoC đã được lưu trong file `exploit.js`.

Cách chạy:

```bash
node weekly-reports/Group06_05/evidence/semgrep/exploit.js
```

Ý tưởng khai thác:

```javascript
const jwt = require("jsonwebtoken");
const forgedToken = jwt.sign(
  { id: 1, role: "admin" },
  "super_secret_key_that_should_not_be_here"
);
console.log("Bearer " + forgedToken);
```

Token sinh ra có thể được gắn vào header:

```http
Authorization: Bearer <forged_token>
```

Nếu backend dùng cùng secret để verify, request sẽ được chấp nhận như token hợp lệ.

## 5. Impact

Mức độ thực tế nên được đánh giá là **High/Critical** vì lỗi có thể dẫn đến:

- Authentication bypass.
- Privilege escalation lên quyền admin.
- Truy cập, sửa đổi hoặc xóa dữ liệu trái phép.
- Làm mất tính toàn vẹn của toàn bộ cơ chế JWT.

## 6. Remediation

Không lưu secret trong source code. Chuyển sang biến môi trường và đảm bảo `.env` không được commit.

```javascript
require("dotenv").config();

const SECRET_KEY = process.env.JWT_SECRET;

if (!SECRET_KEY) {
  console.error("Missing JWT_SECRET");
  process.exit(1);
}

const token = jwt.sign({ id: user.id, role: user.role }, SECRET_KEY);
```

Checklist khắc phục:

- Tạo secret mới đủ dài và ngẫu nhiên.
- Lưu secret qua biến môi trường hoặc secret manager.
- Thêm `.env` vào `.gitignore`.
- Rotate toàn bộ JWT/token cũ sau khi thay secret.
- Chạy lại Semgrep để xác nhận không còn hardcoded secret.
