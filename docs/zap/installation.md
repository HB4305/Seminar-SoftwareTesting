# Hướng dẫn Cài đặt OWASP ZAP
*Tham khảo từ tài liệu chính thức: [ZAP Getting Started](https://www.zaproxy.org/getting-started/#install-and-configure-zap) & [ZAP Download](https://www.zaproxy.org/download/)*

## ⚠️ Yêu cầu hệ thống (Rất quan trọng)
* ZAP bắt buộc phải có **Java 17 trở lên** để có thể chạy được (ngoại trừ khi bạn dùng Docker).
* **Đối với macOS:** Trình cài đặt (.dmg) đã bao gồm sẵn một phiên bản Java phù hợp, bạn không cần cài riêng.
* **Đối với Windows và Linux:** Bạn bắt buộc phải tự cài đặt Java 17+ độc lập trước khi chạy ZAP. 
* *Lưu ý:* Các file cài đặt cốt lõi (Core package) hoặc đa nền tảng (Cross Platform package) cũng cần có Java 17+.

---

## 1. Cài đặt trên Windows
Có 2 cách để cài đặt ZAP trên Windows: cài bằng file trực tiếp hoặc dùng trình quản lý gói.

### Cách 1: Sử dụng File Cài đặt (Installer) - Phổ biến nhất
1. Truy cập trang [Download](https://www.zaproxy.org/download/).
2. Tải file **Windows (64) Installer** (hoặc 32-bit tùy máy bạn).
3. Nháy đúp vào file tải về để mở trình cài đặt.
4. Đọc thỏa thuận cấp phép (License agreement) -> Chọn `Accept` -> Chọn `Standard` (Cài mặc định) -> Click `Finish`.

### Cách 2: Sử dụng các công cụ dòng lệnh (Dành cho Dev)
Nếu bạn thích dùng command line, bạn có thể cài thông qua một số kho lưu trữ chính thức:
* **Windows Package Manager (winget):** `winget install --id=ZAP.ZAP -e`
* **Scoop:** `scoop install zaproxy`

---

## 2. Cài đặt trên macOS
Bạn cần chọn đúng bản cài đặt tương ứng với dòng chip của máy Mac (Intel hoặc Apple Silicon).

### Cách 1: Sử dụng File Cài đặt (Installer)
1. Tải bản **macOS Installer** phù hợp với máy của bạn (Intel - amd64 hoặc Apple Silicon - aarch64) từ trang chủ.
2. Mở file để cài đặt bình thường.

### Cách 2: Sử dụng Homebrew Cask
Đây là cách nhanh nhất trên Mac. Chỉ cần mở Terminal và gõ:
```bash
brew install --cask zap
```

## 3. Cài đặt trên Linux

Với Linux, ZAP hỗ trợ nhiều phương thức cài đặt, từ dùng kho lưu trữ chính thức cho đến cài thủ công bằng file tải về.

### Cách 1: Sử dụng kho lưu trữ chính thức

Đây là cách đơn giản và khuyến nghị nếu bạn muốn tránh lỗi cấu hình Java.

- Cài qua Flathub:
```bash
flatpak install flathub org.zaproxy.ZAP
```

- Chạy ZAP sau khi cài:
```bash
flatpak run org.zaproxy.ZAP
```

- Cài qua Snapcraft:
```bash
sudo snap install zaproxy --classic
```

- Chạy ZAP sau khi cài:
```bash
zaproxy
```

### Cách 2: Cài thủ công bằng file tải về

1. Tải file cài đặt phù hợp cho Linux từ trang chủ. Dưới đây là hướng dẫn để chọn bản phù hợp:
   - **Linux Installer (.sh):** Khuyên dùng cho người mới hoặc các hệ điều hành họ **Debian/Ubuntu** (như Ubuntu, Linux Mint, Kali Linux...). File này sẽ mở trình cài đặt đồ họa từng bước và tự động tạo shortcut Ứng dụng.
   - **Linux Package (.tar.gz):** Dạng Portable (giải nén và chạy trực tiếp). Khuyên dùng cho các hệ điều hành họ **RedHat** (như **Fedora**, CentOS, RHEL, Rocky Linux), họ **Arch** (như Arch Linux, Manjaro) hoặc những môi trường ưu tiên sử dụng Wayland. Nguyên nhân là do trình cài đặt `.sh` có thể gặp lỗi phân quyền hoặc không thể hiển thị giao diện đồ họa trên các hệ điều hành này.
2. Nếu bạn dùng bản Installer, chạy file .sh và làm theo hướng dẫn trên màn hình.
3. Nếu bạn dùng bản Package (.tar.gz) trên các môi trường như Fedora, đầu tiên hãy giải nén file (ví dụ: `tar -xf ZAP_2.15.0_Linux.tar.gz`) và truy cập vào thư mục vừa giải nén. Khởi chạy ZAP bình thường bằng lệnh:
   ```bash
   ./zap.sh
   ```
   > *(Lưu ý: Nếu bạn khởi chạy trên môi trường Wayland và gặp lỗi hiển thị, vui lòng xem mục 4.4 bên dưới)*

## 4. Các lỗi và cảnh báo thường gặp khi cài đặt

### 4.1. Cảnh báo bảo mật khi tải file trên Windows
- **Dấu hiệu:** Trình duyệt cảnh báo file cài đặt ZAP "không an toàn" hoặc "ít được tải xuống".
- **Cách khắc phục:** Trên trình duyệt, click vào dấu `...` (hoặc Tùy chọn) -> Chọn **Keep** -> Chọn **Show more** -> Chọn **Keep anyway**.

### 4.2. Lỗi "ZAP.app cannot be opened" trên macOS
- **Dấu hiệu:** Máy Mac hiện thông báo lỗi chặn mở app do ZAP không phải là ứng dụng được Apple xác minh (verified developer).
- **Cách khắc phục:** Vào **System Preferences (Cài đặt hệ thống)** > **Security & Privacy (Bảo mật & Quyền riêng tư)** > Tìm dòng thông báo ZAP bị chặn và bấm nút **Open anyway (Vẫn mở)**.

### 4.3. Lỗi "ZAP GUI is not supported on a headless environment" trên Linux

**1. Dấu hiệu nhận biết lỗi**
   - Khi chạy lệnh `./zap.sh` trên Linux (Fedora, Ubuntu, ...), ZAP bị văng ngay lập tức và Terminal trả về thông báo:
```text
FATAL org.zaproxy.zap.GuiBootstrap - ZAP GUI is not supported on a headless environment.
```

**2. Nguyên nhân**
   - Hệ thống đang dùng phiên bản Java headless làm mặc định. Đây là bản Java rút gọn dành cho máy chủ, không có thư viện hỗ trợ giao diện đồ họa nên OWASP ZAP không thể mở cửa sổ GUI.

**3. Cách khắc phục**
   - Bước 1: Cài đặt gói Java đầy đủ (có hỗ trợ đồ họa)
```bash
sudo dnf install java-25-openjdk -y
```
   - Bước 2: Cấu hình lại Java mặc định
```bash
sudo alternatives --config java
```
   - Bước 3: Chọn phiên bản không chứa chữ `headless` rồi khởi động lại ZAP
```bash
./zap.sh
```

> Sau khi chọn đúng phiên bản Java, giao diện OWASP ZAP sẽ hiển thị bình thường.

### 4.4. Lỗi hiển thị giao diện (cửa sổ trắng, không click được) trên Wayland (Linux)

- **Dấu hiệu:** Ứng dụng ZAP mở lên nhưng giao diện trống trơn, cửa sổ trắng xóa hoặc không thể tương tác (click) vào bất kỳ đâu.
- **Nguyên nhân:** Các ứng dụng Java sử dụng giao diện AWT/Swing như ZAP thường bị lỗi hiển thị khi chạy trực tiếp (native) trên môi trường Wayland.
- **Cách khắc phục:** Cần khởi chạy ZAP kèm các biến môi trường để ép ứng dụng chạy qua lớp tương thích XWayland và hỗ trợ vẽ cửa sổ tốt hơn. Thay vì chạy `./zap.sh`, hãy dùng lệnh sau:
```bash
_JAVA_AWT_WM_NONREPARENTING=1 GDK_BACKEND=x11 ./zap.sh
```