Tôi dùng công cụ Semgrep (SAST) để quét mã nguồn và phát hiện một finding bảo mật.
Bạn hãy đóng vai trò là chuyên gia bảo mật ứng dụng để triage finding này.
Hãy trả lời hoàn toàn bằng tiếng Việt, trừ các thuật ngữ chuẩn như True Positive, False Positive, Needs Human Review, CWE, OWASP.

Thông tin kỹ thuật:
- Mã finding: SEMGREP-010
- Rule ID: typescript.react.security.react-insecure-request.react-insecure-request
- File nguồn: eshop-sut\frontend-mobile\App.js
- Dòng: 362
- Severity: ERROR
- CWE: CWE-319: Cleartext Transmission of Sensitive Information
- OWASP: A03:2017 - Sensitive Data Exposure, A02:2021 - Cryptographic Failures, A04:2025 - Cryptographic Failures
- Likelihood: LOW
- Impact: MEDIUM
- Confidence: MEDIUM
- Cảnh báo Semgrep: Unencrypted request over HTTP detected.

Source code context / bằng chứng mã nguồn:
```text
   347:     }
   348:     setEditableTotal(cartTotal);
   349:     setCouponCode("");
   350:     setCouponResult(null);
   351:     setCouponError("");
   352:     setCheckoutSuccess(false);
   353:     setView("checkout");
   354:   };
   355:
   356:   const handleApplyCoupon = async () => {
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
   368:           user_id: user?.id || null,
   369:         }),
   370:       });
   371:       const data = await response.json();
   372:       if (!response.ok) throw new Error(data.error || "Không thể áp dụng mã");
   373:       setCouponResult(data);
   374:     } catch (error) {
   375:       setCouponError(error.message || "Không thể áp dụng mã");
   376:     }
   377:     setApplyingCoupon(false);
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
