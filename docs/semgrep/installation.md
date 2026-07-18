# Hướng dẫn Cài đặt Semgrep (SAST)
*Tham khảo từ tài liệu chính thức: [Semgrep Quickstart](https://semgrep.dev/docs/getting-started/)*

Semgrep là một công cụ phân tích mã nguồn tĩnh (SAST) gọn nhẹ, chạy trực tiếp trên CLI. Do đó, việc cài đặt rất nhanh chóng và linh hoạt trên nhiều hệ điều hành khác nhau.

---

## ⚠️ Yêu cầu hệ thống
* **Python:** Cần cài đặt **Python 3.8 trở lên** và trình quản lý gói `pip` (ngoại trừ khi bạn sử dụng Docker).
* **Git:** Cần thiết nếu bạn muốn chạy Semgrep trên các dự án đang quản lý bằng Git (Semgrep mặc định sẽ ưu tiên quét các file được Git quản lý).
* **Docker:** (Tùy chọn) Chỉ cần nếu bạn chọn chạy Semgrep thông qua container.

---

## 1. Cài đặt trên Windows

Windows không phải là môi trường gốc được hỗ trợ hoàn hảo nhất của Semgrep CLI, nhưng bạn vẫn có 3 cách cài đặt phổ biến từ đơn giản đến chuyên nghiệp dưới đây:

### Cách 1: Cài đặt trực tiếp qua Python Pip (Đơn giản nhất)
*Yêu cầu: Máy tính của bạn đã được cài đặt sẵn Python 3.8+ và đã cấu hình biến môi trường cho Python.*

1. Mở Terminal (PowerShell hoặc Command Prompt) với quyền Administrator.
2. Chạy lệnh cài đặt:
   ```powershell
   pip install semgrep
   ```
3. **⚠️ Cấu hình bắt buộc trên Windows (Tránh lỗi mã hóa):**
   Mặc định Windows sử dụng bảng mã CP1252. Khi Semgrep phân tích và xuất kết quả (JSON/Markdown) chứa ký tự tiếng Việt hoặc Unicode, hệ thống sẽ gặp lỗi `UnicodeEncodeError`. 
   Trước khi chạy lệnh quét, bạn bắt buộc phải khai báo biến môi trường sử dụng UTF-8:
   * **Trên PowerShell:**
     ```powershell
     $env:PYTHONUTF8='1'
     chcp 65001
     ```
   * **Trên Command Prompt (CMD):**
     ```cmd
     set PYTHONUTF8=1
     chcp 65001
     ```

### Cách 2: Sử dụng WSL (Windows Subsystem for Linux - Khuyến nghị)
Nếu bạn thường xuyên phát triển phần mềm trên Windows, sử dụng WSL là cách tốt nhất để Semgrep hoạt động mượt mà và tối ưu hiệu suất.

1. Mở Ubuntu/Debian trên WSL.
2. Cài đặt bằng pip giống hướng dẫn Linux:
   ```bash
   sudo apt update
   sudo apt install python3-pip -y
   python3 -m pip install --user semgrep
   ```
3. Sau khi cài đặt xong, bạn có thể gọi trực tiếp lệnh `semgrep` trong môi trường WSL.

### Cách 3: Chạy qua Docker Container (Không cần cài đặt)
Nếu bạn không muốn cài đặt bất cứ thư viện nào vào máy, bạn có thể chạy Semgrep thông qua Docker.

1. Đảm bảo Docker Desktop đã được cài đặt và đang chạy.
2. Mở terminal tại thư mục gốc dự án của bạn và chạy lệnh tương ứng với môi trường:
   * **Trên Windows (PowerShell):**
     ```powershell
     docker run --rm -v "${pwd}:/src" returntocorp/semgrep semgrep scan --config "p/owasp-top-ten"
     ```
   * **Trên Windows (Command Prompt - CMD):**
     ```cmd
     docker run --rm -v "%cd%:/src" returntocorp/semgrep semgrep scan --config "p/owasp-top-ten"
     ```
   * **Trên macOS / Linux (Bash/Zsh):**
     ```bash
     docker run --rm -v "$(pwd):/src" returntocorp/semgrep semgrep scan --config "p/owasp-top-ten"
     ```
   *(Tham số mount volume `-v` sẽ ánh xạ thư mục hiện tại của bạn vào thư mục `/src` trong container để quét)*

---

## 2. Cài đặt trên macOS

Trên macOS, bạn có thể dễ dàng cài đặt thông qua trình quản lý gói Homebrew hoặc công cụ Pip.

### Cách 1: Sử dụng Homebrew (Khuyến nghị)
Đây là cách cài đặt sạch sẽ, dễ nâng cấp và ít gặp lỗi nhất trên macOS.

1. Mở Terminal.
2. Chạy lệnh:
   ```bash
   brew install semgrep
   ```

### Cách 2: Sử dụng Pip
1. Mở Terminal.
2. Chạy lệnh:
   ```bash
   pip3 install semgrep
   ```

---

## 3. Cài đặt trên Linux

Đối với Linux, nhóm khuyến nghị cài Semgrep bằng `pip` thay vì script `curl -fsSL https://semgrep.dev/get | sh`, vì script tải tự động có thể trả về HTML hoặc lỗi redirect trên một số môi trường như Fedora.

### Ubuntu / Debian
1. Cài đặt Python pip nếu máy chưa có:
   ```bash
   sudo apt update
   sudo apt install python3-pip -y
   ```
2. Cài đặt Semgrep:
   ```bash
   python3 -m pip install --user semgrep
   ```

### Fedora
1. Cài đặt Python pip nếu máy chưa có:
   ```bash
   sudo dnf install python3-pip -y
   ```
2. Cài đặt Semgrep:
   ```bash
   python3 -m pip install --user semgrep
   ```

### Arch Linux
1. Cài đặt Python pip nếu máy chưa có:
   ```bash
   sudo pacman -S python-pip
   ```
2. Cài đặt Semgrep:
   ```bash
   python3 -m pip install --user semgrep
   ```

### Cấu hình PATH sau khi cài bằng pip
Nếu terminal báo `semgrep: command not found`, thêm thư mục cài package của user vào `PATH`:
```bash
export PATH="$HOME/.local/bin:$PATH"
```
Sau đó chạy lại:
```bash
semgrep --version
```

---

## 4. Kiểm tra cài đặt thành công (Verify Installation)

Sau khi hoàn tất quá trình cài đặt, bạn mở Terminal mới và chạy lệnh sau để kiểm tra:

```bash
semgrep --version
```

Nếu màn hình hiển thị số phiên bản (Ví dụ: `1.168.0` hoặc mới hơn) nghĩa là Semgrep đã được cài đặt thành công và sẵn sàng để quét mã nguồn!

---

## 5. Khắc phục sự cố thường gặp (Troubleshooting)

### Lỗi 1: Lệnh `semgrep` không được nhận diện (Command not found)
* **Nguyên nhân:** Thư mục cài đặt script của Python (`Scripts` trên Windows hoặc `.local/bin` trên Linux/macOS) chưa được thêm vào biến môi trường `PATH`.
* **Cách khắc phục:**
  * **Trên Windows:** Thêm thư mục `AppData\Local\Programs\Python\PythonXX\Scripts` (với XX là phiên bản Python) vào biến môi trường `Path` của hệ thống.
  * **Trên Linux/macOS:** Thêm dòng sau vào file cấu hình shell của bạn (`~/.bashrc` hoặc `~/.zshrc`):
    ```bash
    export PATH=$PATH:$HOME/.local/bin
    ```
    Sau đó chạy `source ~/.bashrc` hoặc `source ~/.zshrc` để cập nhật cấu hình.

### Lỗi 2: Lỗi mã hóa `UnicodeEncodeError: 'charmap' codec can't encode...` trên Windows
* **Nguyên nhân:** Môi trường Windows Command Prompt/PowerShell mặc định dùng bộ mã hóa không phải UTF-8.
* **Cách khắc phục:** Đọc kỹ hướng dẫn cấu hình biến môi trường `PYTHONUTF8='1'` và lệnh đổi bảng mã `chcp 65001` ở **Mục 1 (Cách 1)**.

### Lỗi 3: Script cài Linux trả về `<!doctype html>`
* **Nguyên nhân:** Lệnh tải tự động `curl -fsSL https://semgrep.dev/get | sh` không lấy được nội dung shell script hợp lệ trong môi trường mạng/distro hiện tại.
* **Cách khắc phục:** Không dùng script này trong báo cáo của nhóm. Chuyển sang cách cài bằng pip theo distro ở **Mục 3**:
  ```bash
  python3 -m pip install --user semgrep
  ```
