## Triage Finding Bảo mật SEMGREP-003

### 1. Phân loại: False Positive

### 2. Lý do phân loại dựa trên source evidence

*   **Vai trò của file:** Dựa trên ngữ cảnh `test_profile.js`, file này rõ ràng là một đoạn mã được sử dụng cho mục đích *testing* hoặc *helper script* trong môi trường phát triển cục bộ.
*   **Mật khẩu cứng:** Mặc dù `super_secret_key_that_should_not_be_here` là một secret được mã hóa cứng và vi phạm nguyên tắc chung về bảo mật (CWE-798, OWASP A07:2021), nhưng việc nó xuất hiện trong một file test không trực tiếp gây ra rủi ro bảo mật cho *ứng dụng EShop đang chạy ở môi trường production* nếu file này không được deploy hoặc sử dụng trong pipeline CI/CD của production.
*   **Endpoint HTTP cục bộ:** Lệnh gọi `axios.get('http://localhost:3000/api/users/me')` chỉ ra rằng đoạn mã này tương tác với một service chạy trên `localhost`. Điều này càng khẳng định tính chất cục bộ và dành cho mục đích thử nghiệm của file. Secret `super_secret_key_that_should_not_be_here` chỉ được sử dụng để tạo token cho việc gọi API nội bộ này trong môi trường test, không phải là secret dùng để ký các JWT xác thực phiên làm việc thực tế của người dùng với production server.

### 3. Tác động thực tế trong bối cảnh EShop

Trong bối cảnh của một ứng dụng lab local như EShop đang được quét, việc phát hiện secret cứng trong file test không tạo ra tác động bảo mật trực tiếp đến **production environment** của EShop. Tuy nhiên, nó cho thấy một thói quen mã hóa không tốt và cần được chấn chỉnh để tránh rủi ro tiềm ẩn nếu file này vô tình bị đưa vào các môi trường nhạy cảm hơn. Rủi ro chính sẽ là nếu mã này, hoặc cách tạo token này, bị lặp lại hoặc sử dụng trong mã nguồn production mà không có sự thay đổi.

### 4. Cách khắc phục cụ thể

Mặc dù phân loại là False Positive trong bối cảnh hiện tại, các bước sau đây nên được thực hiện để cải thiện chất lượng mã và ngăn ngừa rủi ro tái diễn:

*   **Xóa hoặc cập nhật mã test:** Nếu đoạn mã này không còn cần thiết cho việc test (ví dụ: một test cũ đã được thay thế), hãy xóa nó. Nếu nó vẫn cần thiết, hãy thay thế khóa bí mật cứng bằng một biến môi trường hoặc một cách quản lý secret an toàn hơn, ngay cả trong môi trường test. Ví dụ, sử dụng `process.env.JWT_SECRET_TEST` thay vì `'super_secret_key_that_should_not_be_here'`.
*   **Cập nhật quy tắc trong Semgrep (tùy chọn):** Nếu bạn muốn Semgrep thông minh hơn trong việc phân biệt mã test và mã production, bạn có thể xem xét việc tinh chỉnh rule để nó ít nhạy cảm hơn với các file có tên hoặc vị trí cụ thể (ví dụ: nằm trong thư mục `test/` hoặc có tên kết thúc bằng `_test.js`). Tuy nhiên, điều này cần được thực hiện cẩn thận để không bỏ sót các lỗ hổng thực sự.
*   **Giáo dục đội ngũ phát triển:** Tăng cường nhận thức về tầm quan trọng của việc không mã hóa cứng secret trong bất kỳ ngữ cảnh nào, bao gồm cả mã test, để ngăn ngừa các vấn đề bảo mật tương tự trong tương lai.

### 5. Ghi chú cần tester kiểm tra thêm nếu chưa đủ context

*   **Xác nhận môi trường deploy:** Tester cần xác nhận rằng file `test_profile.js` **không bao giờ** được deploy cùng với ứng dụng EShop lên môi trường production hoặc staging.
*   **Kiểm tra vai trò thực tế của token:** Mặc dù evidence cho thấy đây là token tạo cho mục đích test (ký với secret cứng và dùng cho `localhost`), tester nên kiểm tra xem có bất kỳ logic nào khác trong EShop có thể vô tình sử dụng secret `super_secret_key_that_should_not_be_here` để ký hoặc xác minh các token thực sự của ứng dụng hay không. Điều này bao gồm việc quét toàn bộ codebase cho việc sử dụng của biến hoặc chuỗi `'super_secret_key_that_should_not_be_here'`.
*   **Kiểm tra pipeline CI/CD:** Đảm bảo rằng file `test_profile.js` không được bao gồm trong bất kỳ artifact hoặc bước nào của pipeline CI/CD có thể dẫn đến việc nó bị triển khai hoặc tiết lộ.