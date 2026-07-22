Tôi dùng công cụ Semgrep (SAST) để quét mã nguồn và phát hiện một finding bảo mật.
Bạn hãy đóng vai trò là chuyên gia bảo mật ứng dụng để triage finding này.
Hãy trả lời hoàn toàn bằng tiếng Việt, trừ các thuật ngữ chuẩn như True Positive, False Positive, Needs Human Review, CWE, OWASP.

Thông tin kỹ thuật:
- Mã finding: SEMGREP-007
- Rule ID: typescript.react.security.react-insecure-request.react-insecure-request
- File nguồn: eshop-sut\frontend-mobile\App.js
- Dòng: 244
- Severity: ERROR
- CWE: CWE-319: Cleartext Transmission of Sensitive Information
- OWASP: A03:2017 - Sensitive Data Exposure, A02:2021 - Cryptographic Failures, A04:2025 - Cryptographic Failures
- Likelihood: LOW
- Impact: MEDIUM
- Confidence: MEDIUM
- Cảnh báo Semgrep: Unencrypted request over HTTP detected.

Source code context / bằng chứng mã nguồn:
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
