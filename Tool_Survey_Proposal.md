# THÔNG TIN CHUNG (TOPIC METADATA)

- **Topic Code & Name:** T09 - Security Testing (DAST / SAST)
- **Nhóm:** Group 06

## 1. DANH SÁCH CÔNG CỤ ĐỀ XUẤT

- **Traditional Tool:** Semgrep (Công cụ SAST gọn nhẹ, có khả năng quét lỗ hổng trực tiếp từ source code dựa trên ruleset OWASP Top-10).
- **AI-Augmented Tool:** Semgrep Pro AI / ChatGPT & Claude (Kết hợp LLM để tự động lọc lỗi giả - AI triage, giải thích chi tiết lỗ hổng và tự động gợi ý code fix).
- **Backup Tool:** OWASP ZAP (Công cụ DAST dự phòng và bổ trợ — quét trực tiếp trên các endpoint đang vận hành của EShop để xác minh runtime vulnerability nhanh hơn).

## 2. MA TRẬN SO SÁNH (COMPARISON MATRIX)

| Tiêu chí | Semgrep (Traditional SAST) | Semgrep Pro AI / ChatGPT & Claude (AI-Augmented) | OWASP ZAP (Backup DAST) | Nguồn tham chiếu |
| :--- | :--- | :--- | :--- | :--- |
| **Licence cost** | Miễn phí (Mã nguồn mở, Community Edition hoàn toàn đủ cho sinh viên). | Semgrep Pro: Có phí. ChatGPT/Claude: Miễn phí hoặc có phí (bản Plus/Pro). | Miễn phí hoàn toàn (Mã nguồn mở). | [Semgrep Pricing](https://semgrep.dev/pricing), [ZAP FAQ](https://www.zaproxy.org/faq/) |
| **Learning curve** | Thấp - Trung bình (Dễ cài đặt qua CLI, dễ đọc và tự viết rule tĩnh). | Thấp (Tương tác qua giao diện chat tự nhiên, AI tự phân tích ngữ cảnh). | Trung bình - Cao (Đòi hỏi hiểu biết về proxy, HTTP request/response). | [Semgrep Docs](https://semgrep.dev/docs/), [ZAP Getting Started](https://www.zaproxy.org/getting-started/) |
| **EShop fit** | Rất cao (Tích hợp tốt để quét mã nguồn hệ thống tìm SQL injection, weak hashing). | Cao (Phân tích chuyên sâu các đoạn code lỗi đặc thù của EShop và hướng dẫn sửa). | Cao (Rà quét trực tiếp trên các endpoint thực tế khi EShop đang chạy). | [Semgrep Usecases](https://semgrep.dev/docs/getting-started/), [ZAP DAST](https://www.zaproxy.org/docs/desktop/) |
| **AI capability** | Không có (Hoạt động dựa trên pattern-matching và ruleset có sẵn). | Rất cao (Có khả năng AI Triage, giải thích lỗi, gợi ý bản vá bảo mật tự động). | Thấp (Chưa tích hợp AI native mạnh mẽ, chủ yếu quét truyền thống). | [Semgrep AI](https://semgrep.dev/products/semgrep-assistant/), [OpenAI Docs](https://platform.openai.com/docs/) |
| **Community size** | Lớn (Cộng đồng DevSecOps hoạt động mạnh, chia sẻ nhiều bộ ruleset mở). | Rất lớn (Cộng đồng sử dụng LLM cho Security Testing đang phát triển mạnh mẽ). | Rất lớn (Dự án flagship của OWASP, tài liệu phong phú, nhiều plugin). | [Semgrep Registry](https://semgrep.dev/explore), [OWASP ZAP Repo](https://github.com/zaproxy/zaproxy) |

## 3. LÝ DO CHỌN CẶP CÔNG CỤ (RECOMMENDED PICK & RATIONALE)

**Đề xuất lựa chọn:** Bộ ba Semgrep (Traditional) + OWASP ZAP (Backup/Supplementary) + ChatGPT/Claude (AI-Augmented)

- **Phủ sóng toàn diện (SAST + DAST):** Semgrep cung cấp tốc độ quét tĩnh nhanh từ source code, trong khi OWASP ZAP đóng vai trò bổ trợ quét động (DAST) trực tiếp trên các endpoint, giúp phát hiện nhanh các lỗi runtime (như broken auth, CORS) mà SAST thường bỏ sót.
- **Giảm thiểu False-Positive & Tăng tốc kiểm chứng:** Semgrep dễ sinh ra lỗi giả. Bằng cách kết hợp kết quả từ cả SAST (Semgrep) và DAST (ZAP), AI sẽ đóng vai trò bộ lọc (triage) thứ cấp. Nếu lỗ hổng được cả hai công cụ report, AI sẽ xác nhận rủi ro thực tế rất cao, tiết kiệm thời gian kiểm tra thủ công.
- **Tối ưu hóa quy trình vá lỗi & Khai thác (PoC):** Dựa trên cảnh báo từ Semgrep và ZAP, AI tự động sinh ra các kịch bản khai thác thử (PoC exploit) và gợi ý bản vá bảo mật trực tiếp, tạo thành luồng kiểm thử khép kín: Phát hiện (Semgrep/ZAP) -> Xác thực & Gợi ý (AI) -> Áp dụng (Dev).

## 4. CÔNG BỐ SỬ DỤNG AI (AI DISCLOSURE)

**Tuyên bố sử dụng AI:** Nhóm 06 có sử dụng các mô hình ngôn ngữ lớn (LLM - ChatGPT/Gemini) để hỗ trợ quá trình nghiên cứu tổng quan, xây dựng cấu trúc ma trận so sánh các công cụ và biên tập văn phong kỹ thuật. Tuy nhiên, để đảm bảo tính chính xác và tránh hiện tượng "ảo tưởng thông tin" (AI hallucination), toàn bộ các tính năng, chi phí bản quyền và khả năng tích hợp của công cụ đều được nhóm tra cứu chéo và kiểm chứng trực tiếp với các nguồn tài liệu chính thức từ nhà phát hành (Semgrep Documentation, OWASP Official Website, OWASP ZAP Docs) trước khi đưa vào báo cáo.
