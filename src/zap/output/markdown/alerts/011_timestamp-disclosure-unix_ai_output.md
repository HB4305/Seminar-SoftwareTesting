```markdown
# Triage alert ZAP-011: Timestamp Disclosure - Unix (Plugin ID: 10096)

---

## 1. Phân loại  
**Needs Human Review**

---

## 2. Lý do phân loại dựa trên runtime evidence của cả nhóm endpoint  

- Các endpoint bị phát hiện đều là các tài nguyên tĩnh (JS files) phục vụ frontend, nằm trong thư mục `/node_modules/.vite/deps/`.  
- Evidences cho thấy có một giá trị số dạng timestamp Unix (`2080374784`) xuất hiện trong response hoặc các tham số query (chẳng hạn trong `v=82fd3d9d`), tuy nhiên ZAP không chỉ rõ timestamp xuất hiện ở header hay body mà chủ yếu dựa trên tham số query (`v=`) dùng để cache/versioning assets.  
- Response header như `Date` không chứa timestamp Unix, mà chỉ dùng chuẩn dạng GMT thông thường, không gây rò rỉ thông tin đặc biệt.  
- Không thấy timestamp này đi kèm với thông tin nhạy cảm hoặc bất kỳ dữ liệu người dùng, server-side nào.  
- Đây là hành vi phổ biến trong frontend build tools (như vite, webpack) dùng cache-busting version hash hoặc phiên bản thời gian để điều khiển cache, không phải lỗi lộ thông tin nhạy cảm do backend.  
- Mức độ **Confidence: Low** và **Risk: Low** cho thấy nhiều khả năng đây là signal thông tin, không phải lỗ hổng bảo mật nghiêm trọng tại runtime.  
- Môi trường localhost có thể cho phép nhiều quá trình phát triển/debug nên cũng chưa chắc phản ánh môi trường production thực tế.  

---

## 3. Tác động thực tế trong bối cảnh EShop  

- Với ứng dụng EShop, nếu timestamp này thực sự chỉ dùng cho cache-control/versioning file tĩnh frontend thì tác động bảo mật là thấp, gần như không có rủi ro bị khai thác.  
- Thông tin timestamp dạng này không đủ để giúp attacker khai thác thêm (ví dụ không tiết lộ thời gian server hoạt động, history hoạt động của user, hoặc bất kỳ thời điểm nhạy cảm nào trong business logic).  
- Nếu môi trường production được cấu hình khác và không công khai tài nguyên như localhost, thì mức độ rủi ro càng thấp.  
- Tuy nhiên, cần kiểm tra thêm trong môi trường production có tình trạng tương tự hay không.  

---

## 4. Cách khắc phục cụ thể ở cấp cấu hình/root cause  

- Nếu đây là version hash hoặc timestamp dùng cho cache-busting frontend (vite, webpack...), có thể giữ nguyên để tối ưu cache nhưng nên:  
  - Kiểm tra không để lộ bất kỳ timestamp nhạy cảm (ví dụ thời gian phiên đăng nhập, sinh nhật user, internal server time) trong response body hoặc header.  
  - Đảm bảo các thông tin phiên, token, hoặc dữ liệu nhạy cảm không được inject kèm theo các asset tĩnh này.  
  - Với các timestamp trong query param hoặc header, chỉ nên dùng các giá trị không liên quan đến thông tin nhạy cảm (ví dụ hash ngẫu nhiên thay vì timestamp Unix rõ ràng).  
- Nếu timestamp hoặc thông tin này xuất phát từ server, cân nhắc cấu hình server hoặc CDN loại bỏ hoặc che chắn header/số liệu không cần thiết.  
- Đảm bảo deploy production không để debug hoặc source map assets công khai chứa thông tin hệ thống.  

---

## 5. Ghi chú tester cần kiểm tra thêm nếu chưa đủ context  

- Xác nhận xem `v=` param trong URL thực sự là cache buster do frontend build tool tạo ra hay timestamp có ý nghĩa runtime khác.  
- Kiểm tra kỹ response body, header ở production và dưới các quyền user khác (không chỉ localhost) có lộ timestamp tương tự không.  
- Đánh giá xem timestamp có thể được kết hợp với dữ liệu khác để rò rỉ thông tin nhạy cảm hay dùng vào mục đích tấn công (ví dụ side channel) không.  
- Kiểm tra các endpoint khác có lộ thông tin dạng timestamp Unix vào response không, đặc biệt trong API JSON có dữ liệu business.  
- Tham khảo với developers hoặc team DevOps về mục đích tạo timestamp/version param này.  
- Nếu có access kho mã nguồn hoặc CI/CD pipeline, rà soát cấu hình build để xác định nguồn gốc timestamp/version param.  

---

# Tổng kết  

Nhóm alert ZAP-011 với evidences runtime của 3 endpoint dạng tài nguyên frontend static file có tiết lộ timestamp Unix trong query param/version string, rất có khả năng là False Positive do đặc điểm kỹ thuật build frontend (cache busting). Tuy nhiên cần review thêm ở môi trường production, kiểm tra chi tiết để xác định chính xác tính nhạy cảm của timestamp này, tránh bỏ sót rò rỉ thông tin tiềm ẩn. Vì vậy đánh giá hiện tại là **Needs Human Review** với cảnh báo cảnh giác nhẹ.  
```