Tôi dùng công cụ Semgrep (SAST) để quét mã nguồn và phát hiện một finding bảo mật.
Bạn hãy đóng vai trò là chuyên gia bảo mật ứng dụng để triage finding này.
Hãy trả lời hoàn toàn bằng tiếng Việt, trừ các thuật ngữ chuẩn như True Positive, False Positive, Needs Human Review, CWE, OWASP.

Thông tin kỹ thuật:
- Mã finding: SEMGREP-002
- Rule ID: javascript.jsonwebtoken.security.jwt-hardcode.hardcoded-jwt-secret
- File nguồn: eshop-sut/backend/server.js
- Dòng: 105
- Severity: WARNING
- CWE: CWE-798: Use of Hard-coded Credentials
- OWASP: A07:2021 - Identification and Authentication Failures, A07:2025 - Authentication Failures
- Likelihood: HIGH
- Impact: MEDIUM
- Confidence: HIGH
- Cảnh báo Semgrep: A hard-coded credential was detected. It is not recommended to store credentials in source-code, as this risks secrets being leaked and used by either an internal or external malicious adversary. It is recommended to use environment variables to securely provide credentials or retrieve credentials from a secure vault or HSM (Hardware Security Module).

Source code context / bằng chứng mã nguồn:
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

Ngữ cảnh source cho triage tĩnh:
- Đọc và đối chiếu source evidence trước khi phân loại.
- Semgrep là SAST: phân loại dựa trên bằng chứng source code và ngữ cảnh deploy, không dựa trên HTTP response.
- EShop đang được quét như ứng dụng lab local; finding liên quan localhost cần kiểm tra môi trường trước khi kết luận rủi ro cuối.
- Vai trò file: entrypoint runtime backend.
- True Positive: source evidence khớp rule và code lỗi reachable trong runtime/ngữ cảnh ứng dụng liên quan.
- False Positive: source evidence hoặc vai trò file chứng minh finding không phải lỗ hổng thật của ứng dụng.
- Needs Human Review: chưa rõ config, deploy usage, runtime reachability hoặc độ nhạy cảm dữ liệu.
- Nếu đây là mã test/helper, không phân loại là True Positive trừ khi file được deploy hoặc được runtime code dùng lại.
- HTTP localhost có thể chỉ dùng cho dev/lab; chỉ phân loại False Positive khi source/config chứng minh production không bị ảnh hưởng.
- Nếu nhiều finding cùng một root cause, hãy nêu trong phần giải thích nhưng vẫn chọn một trong ba phân loại.
- Với finding JWT/secret, cần xác nhận secret có ký/xác minh token thật của ứng dụng hay không và file có thuộc runtime code hay không.

Hãy trả lời bằng Markdown với các mục:
1. Phân loại: True Positive / False Positive / Needs Human Review.
2. Lý do phân loại dựa trên source evidence.
3. Tác động thực tế trong bối cảnh EShop.
4. Cách khắc phục cụ thể.
5. Ghi chú cần tester kiểm tra thêm nếu chưa đủ context.
