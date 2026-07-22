```markdown
## 1. Phân loại:
Needs Human Review

## 2. Lý do phân loại dựa trên runtime evidence của cả nhóm endpoint:
- Tất cả 3 endpoint bị quét đều liên quan đến static resource (file `.js` trong thư mục `node_modules/.vite/deps/`), với cùng tham số query `v` chứa giá trị dạng encoded path như `%2Fchunk-...js`.
- Các request đều trả về HTTP 200 OK, body là mã JavaScript hợp lệ, không có dấu hiệu response khác biệt khi thay đổi payload, không có lỗi server, không có leak file ngoài phạm vi.
- Payload ZAP dùng kiểm tra Path Traversal (chuỗi `%2F` tương đương `/`) nhưng không làm thay đổi phản hồi, không cho thấy truy cập file ngoài vùng tĩnh được phép, hay dữ liệu bí mật bị tiết lộ.
- Confidence được ZAP đánh giá là Low (độ tin cậy thấp).
- Không có dấu hiệu thay đổi header, status code hay response body theo chiều hướng nguy hiểm khi thử payload.
- Endpoint chạy trên môi trường localhost (localhost:5173, 5174), khả năng đây là môi trường phát triển/lab.
- ZAP cảnh báo dựa trên quy tắc phát hiện tiềm năng Path Traversal dựa trên tham số đầu vào dạng file path, tuy nhiên runtime cho thấy ứng dụng vẫn chỉ phục vụ các file static đã định nghĩa rõ ràng.
- Có thể tham số `v` là cơ chế cache-busting hash hoặc xác định phiên bản tài nguyên, không phải input điều khiển trực tiếp đường dẫn file server.

## 3. Tác động thực tế trong bối cảnh EShop:
- Nếu ứng dụng thực tế chỉ cung cấp tĩnh tài nguyên frontend, với cơ chế cache versioning an toàn, không cho phép người dùng truy vấn tập tin ngoài thư mục web root, rủi ro Path Traversal trên những endpoint này thấp.
- Ngược lại, nếu tham số `v` có thể được lợi dụng để truy cập file nhạy cảm (cấu hình, mã nguồn, dữ liệu người dùng...), thì nguy cơ rất cao.
- Do chưa đủ bằng chứng runtime chỉ ra lỗ hổng thực sự, tác động cụ thể khó xác định.
- Ở môi trường localhost hoặc staging, vấn đề có thể không hiện hữu ở prod nhưng vẫn cần xác nhận.
- Với mức risk High do tính chất CWE-22 Path Traversal, cần lưu ý khi mở rộng chức năng xử lý file.

## 4. Cách khắc phục cụ thể ở cấp cấu hình/root cause:
- Xác thực nghiêm ngặt tham số `v`, chỉ chấp nhận các giá trị dạng hash/version predefined trong allow list, không cho phép giá trị chứa dấu `/`, `\`, hoặc ký tự làm thay đổi cấu trúc đường dẫn.
- Sử dụng hàm canonicalization (ví dụ: realpath, Path.normalize) để chuẩn hóa đường dẫn đầu vào và đảm bảo không vượt ra khỏi thư mục cấp phép.
- Nếu tham số dùng để tham chiếu file, map bằng cơ chế ID hoặc hash cố định tương ứng đường dẫn file cụ thể, thay vì cho phép nhập trực tiếp đường dẫn.
- Triệt tiêu hoặc reject các chuỗi có khả năng thực hiện traversal như `../`, `%2e%2e/`, `%c0%af`... qua bước validate.
- Giới hạn quyền truy cập file system của server để chỉ đọc được thư mục tài nguyên tĩnh, không để web process có quyền truy xuất file hệ thống khác.
- Nếu có, bổ sung sandbox/chroot hoặc thiết lập AppArmor/SELinux hạn chế.
- Xem xét thiết lập CSP để giảm thiểu việc tải tài nguyên độc hại.

## 5. Ghi chú tester cần kiểm tra thêm nếu chưa đủ context:
- Xác minh xem tham số `v` có bị dùng để load file trực tiếp trên server hay chỉ là token version hóa.
- Thử payload path traversal khác đa dạng hơn (../, ..\\, double-encoding, NULL byte, Unicode trick) xem có thể vượt giới hạn thư mục hay không.
- Thử các payload có thể truy xuất tập tin nhạy cảm (ví dụ `/etc/passwd`, `web.config`, file cấu hình) để xác định phạm vi truy cập file.
- Kiểm tra quyền truy cập file của tiến trình web server ở môi trường thật (production).
- Đánh giá xem các hàm xử lý tham số và truy xuất file có validate hoặc canonicalize đúng cách không (nếu có source code).
- Xác nhận mục đích và tính chất tham số `v` trong hệ thống.
- Kiểm tra xem những URL tương tự có bị ảnh hưởng tương tự hay không (không chỉ test trên các tài nguyên static này).
- Xem lại log server để phát hiện các lỗi hoặc bất thường liên quan đến truy cập file khi payload được gửi.
- Đánh giá tác động nếu attacker có thể đọc được nội dung file nhạy cảm từ endpoint.

---

**Tóm lại:** Mặc dù ZAP báo cáo Path Traversal với mức độ cảnh báo Cao, nhưng dựa trên evidence runtime không có chỉ dấu lỗ hổng thực thi hay leak dữ liệu, vì vậy cần review kỹ hơn trước khi kích hoạt biện pháp hoặc chuyển sang True Positive.
```