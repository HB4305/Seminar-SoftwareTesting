Tôi dùng công cụ Semgrep (SAST) để quét mã nguồn và phát hiện một finding bảo mật.
Bạn hãy đóng vai trò là chuyên gia bảo mật ứng dụng để triage finding này.
Hãy trả lời hoàn toàn bằng tiếng Việt, trừ các thuật ngữ chuẩn như True Positive, False Positive, Needs Human Review, CWE, OWASP.

Thông tin kỹ thuật:
- Mã finding: SEMGREP-011
- Rule ID: typescript.react.security.react-insecure-request.react-insecure-request
- File nguồn: eshop-sut\frontend-mobile\App.js
- Dòng: 384
- Severity: ERROR
- CWE: CWE-319: Cleartext Transmission of Sensitive Information
- OWASP: A03:2017 - Sensitive Data Exposure, A02:2021 - Cryptographic Failures, A04:2025 - Cryptographic Failures
- Likelihood: LOW
- Impact: MEDIUM
- Confidence: MEDIUM
- Cảnh báo Semgrep: Unencrypted request over HTTP detected.

Source code context / bằng chứng mã nguồn:
```text
   369:         }),
   370:       });
   371:       const data = await response.json();
   372:       if (!response.ok) throw new Error(data.error || "Không thể áp dụng mã");
   373:       setCouponResult(data);
   374:     } catch (error) {
   375:       setCouponError(error.message || "Không thể áp dụng mã");
   376:     }
   377:     setApplyingCoupon(false);
   378:   };
   379:
   380:   const handleConfirmCheckout = async () => {
   381:     setCheckoutLoading(true);
   382:     try {
   383:       const finalAmount = couponResult ? couponResult.final_amount : cartTotal;
=> 384:       const response = await fetch(`${API_URL}/checkout`, {
   385:         method: "POST",
   386:         headers: {
   387:           "Content-Type": "application/json",
   388:           ...(token ? { Authorization: `Bearer ${token}` } : {}),
   389:         },
   390:         body: JSON.stringify({
   391:           items: cart.length > 1 ? cart.slice(0, -1) : cart,
   392:           total_amount: finalAmount,
   393:           coupon_id: couponResult?.coupon_id || null,
   394:         }),
   395:       });
   396:       const data = await response.json().catch(() => ({}));
   397:       if (!response.ok) throw new Error(data.error || "Lỗi khi thanh toán.");
   398:
   399:       if (couponResult?.coupon_id && token) {
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
