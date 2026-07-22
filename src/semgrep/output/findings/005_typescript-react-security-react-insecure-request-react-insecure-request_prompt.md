Tôi dùng công cụ Semgrep (SAST) để quét mã nguồn và phát hiện một finding bảo mật.
Bạn hãy đóng vai trò là chuyên gia bảo mật ứng dụng để triage finding này.
Hãy trả lời hoàn toàn bằng tiếng Việt, trừ các thuật ngữ chuẩn như True Positive, False Positive, Needs Human Review, CWE, OWASP.

Thông tin kỹ thuật:
- Mã finding: SEMGREP-005
- Rule ID: typescript.react.security.react-insecure-request.react-insecure-request
- File nguồn: eshop-sut\frontend-mobile\App.js
- Dòng: 189
- Severity: ERROR
- CWE: CWE-319: Cleartext Transmission of Sensitive Information
- OWASP: A03:2017 - Sensitive Data Exposure, A02:2021 - Cryptographic Failures, A04:2025 - Cryptographic Failures
- Likelihood: LOW
- Impact: MEDIUM
- Confidence: MEDIUM
- Cảnh báo Semgrep: Unencrypted request over HTTP detected.

Source code context / bằng chứng mã nguồn:
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
