Tôi dùng công cụ Semgrep (SAST) để quét mã nguồn và phát hiện một finding bảo mật.
Bạn hãy đóng vai trò là chuyên gia bảo mật ứng dụng để triage finding này.
Hãy trả lời hoàn toàn bằng tiếng Việt, trừ các thuật ngữ chuẩn như True Positive, False Positive, Needs Human Review, CWE, OWASP.

Thông tin kỹ thuật:
- Mã finding: SEMGREP-009
- Rule ID: typescript.react.security.react-insecure-request.react-insecure-request
- File nguồn: eshop-sut\frontend-mobile\App.js
- Dòng: 296
- Severity: ERROR
- CWE: CWE-319: Cleartext Transmission of Sensitive Information
- OWASP: A03:2017 - Sensitive Data Exposure, A02:2021 - Cryptographic Failures, A04:2025 - Cryptographic Failures
- Likelihood: LOW
- Impact: MEDIUM
- Confidence: MEDIUM
- Cảnh báo Semgrep: Unencrypted request over HTTP detected.

Source code context / bằng chứng mã nguồn:
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
