```markdown
# Triaging Alert ZAP-013: Information Disclosure - Suspicious Comments (Plugin ID 10027)

---

## 1. Phân loại  
**Needs Human Review**

---

## 2. Lý do phân loại dựa trên runtime evidence của cả nhóm endpoint  
- Nhóm alert phát hiện trên 16 endpoint đều trả về response chứa các comment (commented code hoặc chú thích trong file JavaScript), chủ yếu là các comment dạng TODO hoặc giải thích về chức năng của các đoạn code/biblioteca (ví dụ React Refresh, axios...).  
- Các comment này không tiết lộ dữ liệu nhạy cảm hoặc thông tin cấu hình quan trọng của ứng dụng EShop mà chỉ liên quan đến code nguồn phía client (JS bundles, thư viện bên thứ ba).  
- Response header và body không có dấu hiệu rò rỉ thông tin cá nhân, thông tin session, cấu trúc backend hay các chi tiết backend phục vụ việc khai thác thực tế.  
- Các resource này chạy trên localhost, thường là môi trường phát triển hoặc staging, không phải production.  
- Đây là dạng alert with Risk: Informational và Confidence: Medium – báo hiệu tín hiệu cảnh báo nhẹ, có thể không phải lỗi nghiêm trọng nhưng cần đánh giá kỹ.  
- Việc giữ comment trong file JS bundle là bình thường trong môi trường dev, ít phổ biến trong production, nhưng có thể không trực tiếp gây hại nếu không lộ thông tin nhạy cảm.  
- Do ZAP không có khả năng phân biệt môi trường deploy (dev hay prod) và không rõ cấu hình build bundling của dự án, rất khó xác định ngay đây là cấu hình không an toàn hay chỉ là "đặc điểm dev".  
- Vì vậy, cần human review đánh giá môi trường, chính sách build/deploy và mức độ nhạy cảm của comment để phân loại chính xác hơn (True Positive hay False Positive).

---

## 3. Tác động thực tế trong bối cảnh EShop  
- Nếu đây là môi trường phát triển hoặc staging, nguy cơ thực tế rất thấp, hầu như không gây ảnh hưởng đến bảo mật.  
- Nếu các file này được deploy lên môi trường production mở ra cho người dùng cuối, có thể ít nhiều gây lộ thông tin về kiến trúc, thư viện sử dụng hoặc kế hoạch phát triển (TODOs), giúp attacker hiểu sâu hơn về system và tìm kẽ hở khác.  
- Trường hợp có comment mô tả chi tiết kỹ thuật, kiến trúc hoặc các điểm chưa hoàn thiện có thể hỗ trợ attacker trong tấn công nâng cao.  
- Tuy nhiên, trong evidence chưa nhận thấy comment chứa dữ liệu nhạy cảm (mật khẩu, API keys, thông tin user, cấu hình bảo mật) nên mức độ ảnh hưởng trực tiếp là hạn chế.  
- Tổng thể, đây là vấn đề về vệ sinh code/source control hơn là lỗi bảo mật có thể khai thác ngay.

---

## 4. Cách khắc phục cụ thể ở cấp cấu hình/root cause  
- **Build Process:**  
  - Cấu hình build frontend (vite, webpack, ...) cần bật chế độ loại bỏ comment (minify + strip comments) trong môi trường sản xuất (production build).  
  - Đảm bảo bundle JS không chứa comment dạng TODO, giải thích chi tiết code hoặc chú thích phát triển.  

- **Triaging môi trường deploy:**  
  - Không deploy debug JS bundles có nhiều comment lên môi trường production hoặc các môi trường tiếp xúc trực tiếp với người dùng cuối.  
  - Sử dụng cách phân phối resource khác biệt giữa dev và prod để tránh rò rỉ thông tin phát triển.  

- **Kiểm tra lại chính sách release:**  
  - Định kỳ review code, comment, chú thích trên source nhằm loại bỏ các thông tin không cần thiết trước khi ra production.  
  - Áp dụng quy trình kiểm duyệt source code (code review) nhấn mạnh vào loại bỏ comment nhạy cảm.

---

## 5. Ghi chú tester cần kiểm tra thêm nếu chưa đủ context  
- Xác nhận chính xác môi trường ứng dụng đang chạy (dev, staging, production) và chính sách deploy code frontend tại từng môi trường.  
- Kiểm tra cấu hình build frontend để xác định có bật minify và loại bỏ comment hay không trong production.  
- Đánh giá các comment khác, nếu có comment chứa thông tin cấu hình bí mật, credential, hoặc thông tin nhạy cảm cần báo cáo nâng mức alert.  
- Thử kiểm tra theo cách manual hoặc với quyền không auth xem các resource này có bị phơi bày ra ngoài không (open access).  
- Đánh giá nguy cơ khi attacker có thể kết hợp các thông tin từ comment này với các lỗ hổng khác để khai thác sâu hơn.

---

**Tổng kết:**  
Alert này không phải lỗi bảo mật nghiêm trọng nhưng là dấu hiệu cảnh báo về việc vệ sinh code và cấu hình môi trường deploy frontend. Cần đánh giá kỹ tình huống thực tế để quyết định hành động tiếp theo.  
```