# AI Triage Report: javascript.jsonwebtoken.security.jwt-hardcode.hardcoded-jwt-secret

Báo cáo phân tích tự động bằng AI (mô hình `gemini-2.5-flash`) cho lỗ hổng phát hiện bởi Semgrep SAST.

---

### 1. Giải thích lỗ hổng (Vulnerability Explanation)

- **Mã lỗi Semgrep:** `javascript.jsonwebtoken.security.jwt-hardcode.hardcoded-jwt-secret`
- **CWE phân loại:** [CWE-798: Use of Hard-coded Credentials](https://cwe.mitre.org/data/definitions/798.html)
- **OWASP Category:** [A07:2021 - Identification and Authentication Failures](https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/)

**Nguyên nhân:**
Lỗ hổng xảy ra do khóa bí mật (`SECRET_KEY`) dùng để ký và xác thực mã thông báo JSON Web Token (JWT) được khai báo tĩnh (hardcode) trực tiếp trong mã nguồn của ứng dụng tại file `backend/server.js`:
```javascript
const SECRET_KEY = "super_secret_key_that_should_not_be_here";
```
JWT dựa trên chữ ký mật mã để đảm bảo tính toàn vẹn của dữ liệu (không bị thay đổi bởi phía client). Chữ ký này chỉ an toàn nếu khóa bí mật được giữ kín hoàn toàn. Khi khóa bí mật bị lưu trữ trực tiếp trong mã nguồn, bất cứ ai có quyền tiếp cận mã nguồn (nhà phát triển, kiểm thử viên, hoặc kẻ tấn công có được mã nguồn thông qua lỗ hổng khác như LFI, rò rỉ git, backup...) đều có thể lấy được khóa này.

---

### 2. Proof of Concept (PoC)

Khi có được chuỗi `super_secret_key_that_should_not_be_here`, kẻ tấn công không cần biết mật khẩu của tài khoản Admin vẫn có thể tự tạo ra một JWT Token hợp lệ bằng cách chạy đoạn mã Node.js độc lập sau (chi tiết tại file [exploit.js](file:///d:/LEARNING/CNTT_CLC(2023-2027)/NamBa/HK3/Kiểm thử phần mềm/SEMINAR/Seminar-SoftwareTesting/docs/semgrep/exploit.js)):

```javascript
const jwt = require('jsonwebtoken');

// Sử dụng khóa bí mật thu được từ việc rò rỉ mã nguồn
const LEAKED_SECRET = "super_secret_key_that_should_not_be_here";

// Tạo payload giả danh quản trị viên
const payload = {
    id: 1,
    role: "admin",
    email: "admin@eshop.local",
    iat: Math.floor(Date.now() / 1000),
    exp: Math.floor(Date.now() / 1000) + 3600
};

// Tự ký token
const forgedToken = jwt.sign(payload, LEAKED_SECRET);
console.log("Bearer " + forgedToken);
```

**Kịch bản khai thác:**
1. Kẻ tấn công chạy mã trên để sinh ra chuỗi token giả mạo quyền `admin`.
2. Gửi HTTP Request lên hệ thống EShop kèm header sau:
   ```http
   Authorization: Bearer <forged_token>
   ```
3. Backend EShop sử dụng cùng khóa `super_secret_key_that_should_not_be_here` để giải mã và kiểm tra chữ ký. Chữ ký sẽ khớp hoàn toàn, hệ thống tin tưởng token này là do chính mình ký ra và cho phép kẻ tấn công thực thi các quyền quản trị tối cao trên hệ thống.

---

### 3. Mức độ ảnh hưởng (Impact)

- **Mức độ nghiêm trọng:** **CRITICAL / HIGH**
- **Hậu quả:**
  - **Authentication Bypass (Vượt qua cơ chế xác thực):** Kẻ tấn công truy cập trực tiếp vào hệ thống mà không cần cung cấp thông tin đăng nhập hợp lệ.
  - **Privilege Escalation (Leo thang đặc quyền):** Do có thể tùy ý sửa đổi payload của JWT (nhéo thay đổi `role` từ `user` thành `admin`), kẻ tấn công có thể nâng quyền của mình lên quyền hạn cao nhất.
  - **Data Breach (Rò rỉ/Phá hủy dữ liệu):** Chiếm quyền admin cho phép kẻ tấn công sửa đổi cơ sở dữ liệu, đánh cắp thông tin người dùng, đơn hàng hoặc xóa bỏ dữ liệu hệ thống EShop.

---

### 4. Khuyến nghị khắc phục (Remediation)

Không được phép lưu trữ khóa bí mật hoặc thông tin nhạy cảm trực tiếp trong mã nguồn. Khóa bí mật phải được cấu hình thông qua **Biến môi trường (Environment Variables)** và tệp `.env` (phải được đưa vào `.gitignore` để tránh bị commit lên git).

#### Bước 1: Di chuyển khóa vào file cấu hình môi trường `.env`
Tạo file `.env` tại thư mục gốc của backend (không commit file này):
```env
JWT_SECRET=Thay_The_Bang_Mot_Chuoi_Ngau_Nhien_Dai_Va_Phuc_Tap_Nhat_Co_The_12345!
```

#### Bước 2: Cài đặt thư viện `dotenv` để nạp biến môi trường
```bash
npm install dotenv
```

#### Bước 3: Cập nhật mã nguồn trong `backend/server.js`
Thay đổi cách khởi tạo `SECRET_KEY` bằng cách đọc từ biến môi trường `process.env`:

```javascript
// Nạp cấu hình từ file .env ở đầu file server.js
require('dotenv').config();

const jwt = require("jsonwebtoken");

// Đọc khóa bí mật từ biến môi trường
const SECRET_KEY = process.env.JWT_SECRET;

// Ràng buộc bảo mật: Dừng server ngay nếu chưa cấu hình JWT_SECRET
if (!SECRET_KEY) {
    console.error("CRITICAL ERROR: Biến môi trường JWT_SECRET chưa được cấu hình!");
    process.exit(1);
}

// ... các logic ký và xác thực token giữ nguyên cấu trúc
const token = jwt.sign({ id: user.id, role: user.role }, SECRET_KEY);
```
