Tôi dùng công cụ Semgrep (SAST) để quét mã nguồn và phát hiện một finding bảo mật.
Bạn hãy đóng vai trò là chuyên gia bảo mật ứng dụng để triage finding này.
Hãy trả lời hoàn toàn bằng tiếng Việt, trừ các thuật ngữ chuẩn như True Positive, False Positive, Needs Human Review, CWE, OWASP.

Thông tin kỹ thuật:
- Mã finding: SEMGREP-008
- Rule ID: typescript.react.security.react-insecure-request.react-insecure-request
- File nguồn: eshop-sut\frontend-mobile\App.js
- Dòng: 272
- Severity: ERROR
- CWE: CWE-319: Cleartext Transmission of Sensitive Information
- OWASP: A03:2017 - Sensitive Data Exposure, A02:2021 - Cryptographic Failures, A04:2025 - Cryptographic Failures
- Likelihood: LOW
- Impact: MEDIUM
- Confidence: MEDIUM
- Cảnh báo Semgrep: Unencrypted request over HTTP detected.

Source code context / bằng chứng mã nguồn:
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

Ngữ cảnh source cho triage tĩnh:
- Đọc và đối chiếu source evidence trước khi phân loại.
- Semgrep là SAST: phân loại dựa trên bằng chứng source code và ngữ cảnh deploy, không dựa trên HTTP response.
- EShop đang được quét như ứng dụng lab local; finding liên quan localhost cần kiểm tra môi trường trước khi kết luận rủi ro cuối.
- Vai trò file: mã runtime của ứng dụng.
- True Positive: source evidence khớp rule và code lỗi reachable trong runtime/ngữ cảnh ứng dụng liên quan.
- False Positive: source evidence hoặc vai trò file chứng minh finding không phải lỗ hổng thật của ứng dụng.
- Needs Human Review: chưa rõ config, deploy usage, runtime reachability hoặc độ nhạy cảm dữ liệu.
- Nếu đây là mã test/helper, không phân loại là True Positive trừ khi file được deploy hoặc được runtime code dùng lại.
- HTTP localhost có thể chỉ dùng cho dev/lab; chỉ phân loại False Positive khi source/config chứng minh production không bị ảnh hưởng.
- Nếu nhiều finding cùng một root cause, hãy nêu trong phần giải thích nhưng vẫn chọn một trong ba phân loại.

Hãy trả lời bằng Markdown với các mục:
1. Phân loại: True Positive / False Positive / Needs Human Review.
2. Lý do phân loại dựa trên source evidence.
3. Tác động thực tế trong bối cảnh EShop.
4. Cách khắc phục cụ thể.
5. Ghi chú cần tester kiểm tra thêm nếu chưa đủ context.
