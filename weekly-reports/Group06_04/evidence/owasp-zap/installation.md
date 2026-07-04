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

> **⚠️ Xử lý cảnh báo bảo mật trên Windows:** > Trình duyệt có thể cảnh báo file ZAP "không an toàn" hoặc "ít được tải xuống". Để bỏ qua: Click vào dấu `...` (hoặc Tùy chọn) -> Chọn **Keep** -> Chọn **Show more** -> Chọn **Keep anyway**.

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

> **⚠️ Xử lý cảnh báo nhà phát triển trên macOS:** > Vì ZAP không phải là ứng dụng được Apple xác minh (verified developer), máy sẽ hiện thông báo *"ZAP.app cannot be opened..."*. Để mở được phần mềm: 
> Vào **System Preferences (Cài đặt hệ thống)** > **Security & Privacy (Bảo mật & Quyền riêng tư)** > Tìm dòng thông báo ZAP bị chặn và bấm nút **Open anyway (Vẫn mở)**.

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

1. Tải file cài đặt phù hợp cho Linux từ trang chủ, gồm:
   - Linux Installer (.sh)
   - Linux Package (.tar.gz)
2. Nếu bạn dùng bản Installer, chạy file .sh và làm theo hướng dẫn trên màn hình.
3. Nếu bạn dùng bản Package, giải nén thư mục, vào thư mục vừa giải nén và chạy lệnh khởi động:
```bash
./zap.sh
```

### Lưu ý & Khắc phục lỗi: "ZAP GUI is not supported on a headless environment"

1. Dấu hiệu nhận biết lỗi
   - Khi chạy lệnh `./zap.sh` trên Linux (Fedora, Ubuntu, ...), ZAP bị văng ngay lập tức và Terminal trả về thông báo:
```text
FATAL org.zaproxy.zap.GuiBootstrap - ZAP GUI is not supported on a headless environment.
```

2. Nguyên nhân
   - Hệ thống đang dùng phiên bản Java headless làm mặc định. Đây là bản Java rút gọn dành cho máy chủ, không có thư viện hỗ trợ giao diện đồ họa nên OWASP ZAP không thể mở cửa sổ GUI.

3. Cách khắc phục
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