# Semgrep Failure Modes & Metrics

## 1. Failure Modes

### FM-1: False Negative - SQL Injection không được phát hiện

Semgrep với ruleset `p/owasp-top-ten` có thể bỏ sót SQL Injection trong đoạn code dùng template literal:

```javascript
const query = `SELECT * FROM products WHERE name LIKE '%${searchQuery}%'`;
db.all(query, (err, rows) => { ... });
```

Nguyên nhân: ruleset mặc định chưa có rule taint-analysis chuyên biệt cho luồng `req.query` đến `sqlite3 db.all()` trong ngữ cảnh này.

Khuyến nghị:

- Bổ sung `p/javascript`, `p/nodejs`.
- Viết custom rule dùng `mode: taint`.
- Kết hợp DAST bằng ZAP để kiểm chứng runtime.

### FM-2: False Negative - Plaintext Password không được cảnh báo

Semgrep có thể không phát hiện việc lưu và so sánh password plaintext:

```javascript
db.run("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", [name, email, password]);
if (user.password === password) { ... }
```

Nguyên nhân: đây là lỗi thiếu cơ chế bảo vệ, tức "absence of security control". SAST dễ tìm pattern nguy hiểm có mặt trong code, nhưng khó kết luận một bước bảo mật đang bị thiếu nếu không có rule rất cụ thể.

Khuyến nghị:

- Review thủ công luồng authentication.
- Viết custom Semgrep rule để cảnh báo insert password không đi qua `bcrypt.hash`.
- Thêm test bảo mật cho login/register.

### FM-3: Duplicate Finding - nhiều cảnh báo cùng root cause

Semgrep có thể báo nhiều finding cho cùng một secret:

- `jwt.sign(..., SECRET_KEY)`.
- `jwt.verify(..., SECRET_KEY)`.
- File test hardcode lại cùng secret.

Nguyên nhân gốc vẫn chỉ là một: secret bị hardcode. Khi viết report cần deduplicate để tránh phóng đại số lượng lỗi.

## 2. Metrics thực nghiệm

| Metric | Giá trị ghi nhận |
| --- | --- |
| Semgrep version | `1.168.0` |
| Config | `p/owasp-top-ten` |
| Target | EShop backend |
| Files scanned | 6 |
| Rules applicable | 73 / 560 |
| Findings | 3 |
| True Positive | 3 / 3 |
| False Positive | 0 / 3 |
| False Negative đã biết | SQLi, plaintext password, weak OTP, mass assignment |
| Core scan time | khoảng 3.17 giây |
| Total scan time | khoảng 4.25 giây |
| Peak memory | khoảng 733 MB |
| Lỗi kỹ thuật gặp | Windows encoding CP1252 khi xuất JSON/Unicode |

## 3. Bài học

Semgrep phù hợp để screening nhanh và chỉ rõ dòng code rủi ro, nhưng không nên dùng đơn độc. Luồng làm việc hiệu quả hơn là:

```text
Semgrep scan -> AI triage -> human audit -> deduplicate -> report -> verify remediation
```

AI triage giúp rút ngắn thời gian giải thích lỗi, tạo PoC và đề xuất fix, nhưng mọi kết quả vẫn cần kiểm chứng lại bằng source code và hành vi thực tế của ứng dụng.
