# KỊCH BẢN THUYẾT TRÌNH PHẦN DAST & OWASP ZAP
**Môn học:** Seminar Software Testing  
**Ứng dụng thử nghiệm:** EShop (Node.js/Express Backend, React Single Page App Frontend)  
**Phạm vi slide:** Slide 16 đến Slide 30 (`submission/slide/index.html`)

---

## 📍 Slide 16: DAST Branch & OWASP ZAP (Tổng quan section)

* **Mục tiêu Slide:** Dẫn dắt người nghe chuyển tiếp từ phần Kiểm thử tĩnh (SAST - Semgrep) sang phần Kiểm thử động (DAST - OWASP ZAP).
* **Thời lượng dự kiến:** 45 - 60 giây.

### 🎙️ Kịch bản thuyết trình:
> *"Kính thưa thầy/cô và các bạn, sau khi nhóm đã phân tích tĩnh mã nguồn bằng Semgrep để tìm ra các rủi ro trong code, chúng ta sẽ chuyển sang **Phần DAST – Kiểm thử bảo mật động ứng dụng web với OWASP ZAP**.*
>
> *Nếu như SAST phân tích mã nguồn 'nằm yên' trên đĩa cứng, thì DAST sẽ trực tiếp tương tác với ứng dụng EShop khi nó đang **vận hành thật**.*
>
> *Trong phần này, nhóm sẽ lần lượt trình bày 6 nội dung chính:*
> 1. *Khái niệm DAST và vai trò của OWASP ZAP.*
> 2. *Hướng dẫn cài đặt ZAP GUI và chuẩn bị môi trường CLI.*
> 3. *Quy trình quét thủ công qua ZAP GUI (bao gồm cả Public scan và Authenticated scan).*
> 4. *Quy trình quét tự động hóa bằng ZAP CLI qua script Python.*
> 5. *Cơ chế AI Triage để xử lý và phân loại báo cáo ZAP JSON.*
> 6. *Quy trình xây dựng Testcase và Replay Request để kiểm chứng thủ công.*
>
> *Xin mời thầy/cô và các bạn cùng đi vào chi tiết khái niệm DAST ở slide tiếp theo."*

---

## 📍 Slide 17: Khái niệm DAST & Vai trò của OWASP ZAP

* **Mục tiêu Slide:** Định nghĩa DAST, phân biệt với SAST, giới thiệu OWASP ZAP và 2 chế độ chạy (GUI & CLI).
* **Thời lượng dự kiến:** 60 - 90 giây.

### 🎙️ Kịch bản thuyết trình:
> *"Trước tiên, **DAST (Dynamic Application Security Testing)** là phương pháp kiểm thử bảo mật 'Black-box' hay 'Gray-box'. DAST không hề đọc source code của ứng dụng. Thay vào đó, tool gửi các request HTTP, crawl các đường dẫn, phân tích response trả về, và chủ động gửi các chuỗi payload để phát hiện lỗ hổng runtime.*
>
> *Trong dự án này, nhóm lựa chọn **OWASP ZAP (Zed Attack Proxy)** – đây là công cụ DAST mã nguồn mở phổ biến hàng đầu thế giới.*
>
> *ZAP đóng vai trò thu thập các bằng chứng thời gian thực (Runtime Evidence) dựa trên các tương tác thực tế của EShop. Nhóm triển khai ZAP theo 2 phương thức:*
> * **ZAP GUI**: Phù hợp cho việc tương tác thủ công, proxy trình duyệt, cấu hình Context và phân tích sâu từng Request/Response.*
> * **ZAP CLI**: Sử dụng script `src/zap/scan_zap.py` để tự động hóa toàn bộ quá trình Spider, Active Scan và xuất báo cáo JSON/HTML phục vụ cho pipeline AI Triage."*

---

## 📍 Slide 18: Cài đặt OWASP ZAP GUI trên các Hệ điều hành

* **Mục tiêu Slide:** Trình bày rõ ràng yêu cầu môi trường (Java 17+) và các bước cài đặt ZAP GUI trên Windows, macOS và Linux.
* **Thời lượng dự kiến:** 60 - 90 giây.

### 🎙️ Kịch bản thuyết trình:
> *"Để sử dụng giao diện đồ họa ZAP GUI, nhóm đã đóng gói hướng dẫn cài đặt chuẩn cho cả 3 hệ điều hành chính trong file `src/zap/installation.md`:*
>
> * **Về điều kiện tiên quyết**: ZAP GUI bắt buộc cần môi trường **Java 17 trở lên**.
> * **Trên Windows**: Người dùng có thể tải file `.exe` Installer chính thức từ `zaproxy.org`, hoặc cài nhanh qua Package Manager với lệnh `winget install --id=ZAP.ZAP -e` hoặc `scoop install zaproxy`.*
> * **Trên macOS**: Bản cài ZAP cho Mac đã được **bundle sẵn Java**, giúp thao tác rất thuận tiện. Cách nhanh nhất là dùng Homebrew Cask: `brew install --cask zap`. Nếu cài từ file `.dmg`, lưu ý chọn đúng kiến trúc chip Intel (`amd64`) hoặc Apple Silicon (`aarch64`), và nên mở *System Preferences > Security & Privacy* để cho phép chạy ứng dụng nếu bị Gatekeeper chặn.*
> * **Trên Linux**: Có thể cài qua kho Flatpak hoặc Snap với quyền root (`sudo snap install zaproxy --classic`). Nếu dùng bản nén thủ công (`zap.sh`), cần đảm bảo cài **Java 17 OpenJDK bản GUI** (tránh dùng bản `headless`). Riêng môi trường Wayland nếu gặp sự cố cửa sổ trắng, ta chỉ cần truyền thêm biến môi trường `_JAVA_AWT_WM_NONREPARENTING=1 GDK_BACKEND=x11 ./zap.sh`."*

---

## 📍 Slide 19: Quy trình ZAP GUI Scan không Đăng nhập (Public Scan)

* **Mục tiêu Slide:** Hướng dẫn luồng quét GUI đơn giản cho các endpoint công khai (Public routes).
* **Thời lượng dự kiến:** 60 giây.

### 🎙️ Kịch bản thuyết trình:
> *"Sau khi cài đặt, nhóm tiến hành luồng quét GUI đầu tiên: **Public Scan (không cần xác thực)**.*
>
> *Luồng này áp dụng cho các route công khai như trang chủ, danh sách sản phẩm, hoặc các endpoint API không yêu cầu token authorization. Môi trường thử nghiệm EShop gồm 3 target:*
> * Backend API tại port `3000`
> * User Frontend tại port `5173`
> * Admin Frontend tại port `5174`
>
> *Các bước thực hiện rất đơn giản:*
> 1. *Mở ZAP GUI, chọn không lưu Session nếu chỉ demo nhanh.*
> 2. *Vào thẻ **Quick Start > Automated Scan**, nhập URL target (ví dụ `http://localhost:3000`) và bấm **Attack**.*
> 3. *Theo dõi ZAP tự động crawl cây thư mục tại thẻ **Sites**, ghi nhận request trong **History** và liệt kê các rủi ro phát hiện được tại thẻ **Alerts**.*
> 4. *Cuối cùng, tester nhấp vào từng Alert để xem chi tiết Request/Response runtime làm bằng chứng."*

---

## 📍 Slide 20: Cấu hình Browser Proxy qua ZAP GUI

* **Mục tiêu Slide:** Giải thích nguyên lý và các bước proxy Firefox qua ZAP GUI để bắt traffic người dùng.
* **Thời lượng dự kiến:** 60 - 90 giây.

### 🎙️ Kịch bản thuyết trình:
> *"Quick Start chỉ crawl được các đường dẫn tĩnh. Để ZAP có thể ghi nhận đúng toàn bộ hành vi thực tế khi người dùng click trên giao diện Web, ta cần **Cấu hình Browser Proxy**.*
>
> *Ở đây, nhóm sử dụng Firefox và định tuyến toàn bộ traffic đi qua ZAP Proxy:*
> 1. *Trong ZAP GUI, xác nhận cổng lắng nghe mặc định tại `Tools > Options > Network > Local Servers/Proxies` là `localhost:8080`.*
> 2. *Trong Firefox, truy cập **Settings > Network Settings**, chọn *Manual proxy configuration*, điền HTTP Proxy là `localhost` và Port là `8080`.*
> 3. *Một điểm kỹ thuật rất quan trọng: Mặc định Firefox chặn proxy các địa chỉ `localhost`. Do đó, ta phải mở `about:config` trong Firefox và chuyển flag `network.proxy.allow_hijacking_localhost` thành `true`.*
>
> *Sau khi cấu hình xong, mọi thao tác lướt web trên Firefox đều sẽ được ZAP bắt trọn vẹn vào tab History, làm cơ sở cho bước quét nâng cao."*

---

## 📍 Slide 21: Authenticated ZAP GUI Scan (Quét có Đăng nhập)

* **Mục tiêu Slide:** Hướng dẫn thiết lập Context, JSON Login Request và Forced User Mode trong GUI cho các vùng ứng dụng yêu cầu Auth.
* **Thời lượng dự kiến:** 90 giây.

### 🎙️ Kịch bản thuyết trình:
> *"Đối với các vùng chức năng bảo mật như giỏ hàng, thông tin cá nhân hay trang quản trị Admin, request bắt buộc phải có Token hoặc Cookie hợp lệ. Nhóm thực hiện **Authenticated GUI Scan** qua 4 bước:*
>
> 1. *Thực hiện đăng nhập EShop trên trình duyệt Firefox đã proxy để ZAP ghi nhận request `POST /api/login`.*
> 2. *Tạo một **Context** mới trong ZAP (bao gồm cả frontend và backend vào Scope). Tại mục **Authentication**, chọn kiểu *JSON-based Authentication*, trỏ đến request login và đánh dấu hai trường `username` và `password` trong JSON body.*
> 3. *Tại mục **Users**, thêm tài khoản test, điền credential và bật biểu tượng **Forced User Mode** (hình khóa màu xanh trên thanh công cụ).*
> 4. *Tiến hành chạy **Spider / AJAX Spider** và **Active Scan** trên Context đó. Lúc này, ZAP sẽ tự động duy trì session đăng nhập và gắn token vào mọi request kiểm thử.*
>
> *Nhờ vậy, ta có thể phát hiện các lỗ hổng sâu bên trong các API yêu cầu quyền User hoặc Admin."*

---

## 📍 Slide 22: Môi trường & Dependencies cho ZAP CLI Flow

* **Mục tiêu Slide:** Giới thiệu kiến trúc quét tự động bằng CLI (Python client kết nối ZAP Daemon Docker).
* **Thời lượng dự kiến:** 60 giây.

### 🎙️ Kịch bản thuyết trình:
> *"Bên cạnh việc dùng GUI thủ công, nhóm đã xây dựng **Luồng quét tự động ZAP CLI** để phục vụ việc tích hợp CI/CD.*
>
> *Cần lưu ý rằng: Script Python không trực tiếp thực hiện quét, mà nó đóng vai trò là Client điều khiển **ZAP Engine (Daemon)** chạy ngầm:*
> * **Khởi tạo Virtual Environment**: Tạo venv isolated để cài thư viện `python-owasp-zap-v2.4`.*
> * **Khởi động ZAP Daemon bằng Docker**: Nhóm chạy container ZAP headless chính thức từ OWASP (`ghcr.io/zaproxy/zaproxy:stable`), mở cổng API `8090` và thiết lập `api.disablekey=true` để các script nội bộ dễ dàng ra lệnh cho ZAP mà không bị vướng API Key.*
>
> *Mô hình này giúp quá trình quét diễn ra hoàn toàn tự động và nhất quán trên mọi máy dev."*

---

## 📍 Slide 23: Cấu hình Tập tin `src/zap/.env`

* **Mục tiêu Slide:** Giải thích các thông số cấu hình môi trường trong `src/zap/.env`.
* **Thời lượng dự kiến:** 60 giây.

### 🎙️ Kịch bản thuyết trình:
> *"Mọi tham số chạy cho script CLI đều được quản lý tập trung qua file `src/zap/.env` (được sao chép từ `.env.example`):*
>
> * `ZAP_TARGET`: Định vị URL mục tiêu (`http://localhost:3000` cho Backend API).*
> * `ZAP_URL`: Trỏ tới ZAP Daemon (`http://localhost:8090`).*
> * `ZAP_AUTH_ROLE`: Chọn vai trò quét (`none`, `user`, hoặc `admin`).*
> * `ZAP_MAX_URLS`: Ngân sách đặt giới hạn số lượng URL được phép Active Scan (ví dụ `300`). Điều này cực kỳ quan trọng đối với các ứng dụng Single Page App như React để tránh trường hợp Crawler duyệt vô tận làm cạn kẹt tài nguyên RAM.*
> * `ZAP_REPORT_FORMAT`: Chọn xuất file `json` cho pipeline AI Triage hoặc `html` cho người đọc thủ công.*
> * *Cùng các thông tin tài khoản test cho User và Admin.*"

---

## 📍 Slide 24: Public ZAP CLI Scan (`scan_zap.py`)

* **Mục tiêu Slide:** Trình bày câu lệnh quét tự động không đăng nhập cho Backend API và Frontend SPA.
* **Thời lượng dự kiến:** 60 giây.

### 🎙️ Kịch bản thuyết trình:
> *"Trên slide là câu lệnh chạy quét Public bằng script `src/zap/scan_zap.py`:*
>
> * **Khi quét Backend API (`localhost:3000`)**: Ta chỉ cần chỉ định `--target` và `--report-format json`. Script sẽ mở URL, chạy Traditional Spider, chờ Passive Scan phân tích và tiến hành Active Scan để xuất ra file `backend_basic.json`.*
> * **Khi quét Frontend User (`localhost:5173`)**: Do giao diện được viết bằng React SPA, các đường dẫn (route) không tồn tại sẵn trong HTML mà chỉ được sinh ra khi JavaScript chạy. Do đó, ta truyền thêm flag `--ajax-spider`. Flag này sẽ mở một trình duyệt ngầm (Headless Browser) để click vào các thành phần trên trang, giúp ZAP khám phá trọn vẹn các API endpoint ngầm.*"

---

## 📍 Slide 25: Authenticated ZAP CLI Scan theo Role

* **Mục tiêu Slide:** Trình bày câu lệnh quét tự động có đăng nhập phân biệt theo phân quyền User và Admin.
* **Thời lượng dự kiến:** 60 - 90 giây.

### 🎙️ Kịch bản thuyết trình:
> *"Để tự động hóa quá trình quét các chức năng có đăng nhập, script `scan_zap.py` hỗ trợ cơ chế nạp sẵn ngữ cảnh xác thực qua các flag CLI:*
>
> * **Quét Frontend User (`localhost:5173`)**: Ta truyền `--auth-role user` và `--forced-user`. Script sẽ tự động gọi API `/api/login` lấy JWT token, cấu hình Context trong ZAP Daemon và bật Forced User Mode trước khi chạy AJAX Spider và Active Scan.*
> * **Quét Frontend Admin (`localhost:5174`)**: Tương tự, ta chuyển `--auth-role admin` để quét riêng các API quản trị.*
>
> *Kết quả xuất ra các file JSON riêng biệt (`frontend_user_basic.json`, `frontend_admin_basic.json`), giúp nhóm dễ dàng so sánh phạm vi rủi ro giữa tài khoản khách, tài khoản người dùng và tài khoản quản trị.*"

---

## 📍 Slide 26: Bảng Tổng hợp các Flag CLI chính trong `scan_zap.py`

* **Mục tiêu Slide:** Hệ thống hóa toàn bộ các tùy chọn CLI quan trọng của công cụ scan ZAP.
* **Thời lượng dự kiến:** 60 giây.

### 🎙️ Kịch bản thuyết trình:
> *"Để thầy/cô và các bạn tiện tra cứu, slide này tổng hợp 7 flag CLI cốt lõi của script `scan_zap.py`:*
> * `--target`: Định nghĩa URL mục tiêu.*
> * `--auth-role`: Chọn loại tài khoản thử nghiệm (`none`, `user`, `admin`).*
> * `--forced-user`: Ép buộc mọi request phải đi dưới danh nghĩa tài khoản đã xác thực.*
> * `--ajax-spider`: Kích hoạt trình duyệt ngầm để crawl các ứng dụng Single Page App.*
> * `--scan-mode`: Cho phép chọn chế độ quét `basic` (mặc định) hoặc `owasp-top10-2025` (chế độ đặc biệt chỉ bật các rule Active Scanner thuộc bảng xếp hạng OWASP Top 10 năm 2025).*
> * `--max-urls`: Giới hạn ngân sách URL để bảo vệ hệ thống không bị ngợp RAM.*
> * `--report-format`: Định dạng báo cáo đầu ra (`json` hoặc `html`).*"

---

## 📍 Slide 27: AI Triage cho ZAP Report (Tổng quan)

* **Mục tiêu Slide:** Giới thiệu cơ chế AI Triage xử lý báo cáo ZAP JSON và lý do tách riêng luồng DAST với SAST.
* **Thời lượng dự kiến:** 60 - 90 giây.

### 🎙️ Kịch bản thuyết trình:
> *"Báo cáo JSON do ZAP xuất ra thường chứa hàng trăm Alert Instance với lượng thông tin Request/Response rất đồ sộ. Để giúp Tester không bị quá tải, nhóm đã xây dựng luồng **ZAP AI Triage** tự động.*
>
> *Cần nhấn mạnh rằng: Luồng AI Triage của ZAP được tách biệt hoàn toàn với Semgrep. Vì ZAP là DAST, bằng chứng của nó là **Runtime HTTP Request/Response**, chứ không phải dòng mã nguồn.*
>
> *Script `zap_ai_triage.py` sẽ thực hiện:*
> 1. *Gom nhóm các alert trùng loại (Alert Group).*
> 2. *Trích xuất bằng chứng HTTP đại diện (Headers, Body, Attack Payload).*
> 3. *Tạo ra 3 file báo cáo chuẩn Markdown:*
>    * `zap_triage_report.md`: Báo cáo phân tích AI tổng hợp theo nhóm lỗi.
>    * `zap_test_cases.md`: Danh sách testcase sinh ra cho từng endpoint.
>    * Thư mục `alerts/`: Lưu trữ các file prompt và kết quả phân tích AI chi tiết cho từng nhóm alert.*"

---

## 📍 Slide 28: Cấu hình AI Provider cho ZAP Triage

* **Mục tiêu Slide:** Hướng dẫn cấu hình API Key cho OpenAI / OpenRouter và chế độ `--offline`.
* **Thời lượng dự kiến:** 45 - 60 giây.

### 🎙️ Kịch bản thuyết trình:
> *"Cơ chế AI Triage của ZAP được thiết kế rất linh hoạt, hỗ trợ 2 AI Provider chính qua file `.env`:*
> * **OpenAI**: Sử dụng mô hình `gpt-4o-mini` hoặc các bản tương đương.*
> * **OpenRouter**: Sử dụng các mô hình như `google/gemini-2.5-flash`.*
>
> *Đặc biệt, script tích hợp chế độ `--offline`. Khi bật flag này, script sẽ không gọi API (không tốn chi phí token), mà vẫn tự động gom nhóm, sinh các file Prompt tiếng Việt chuẩn và tạo khung báo cáo Skeleton. Nhờ đó, Tester có thể xem trước nội dung hoặc tự đưa vào các mô hình AI nội bộ mà không lo lộ API Key.*"

---

## 📍 Slide 29: Lệnh chạy Multi-Report AI Triage (`zap_ai_triage.py`)

* **Mục tiêu Slide:** Phân tích câu lệnh thực thi AI Triage trên nhiều file JSON báo cáo cùng lúc.
* **Thời lượng dự kiến:** 60 giây.

### 🎙️ Kịch bản thuyết trình:
> *"Trên slide là câu lệnh chạy AI Triage hoàn chỉnh. Script `zap_ai_triage.py` hỗ trợ nhận đồng thời nhiều file JSON báo cáo đầu vào (như `backend_basic.json`, `frontend_user_basic.json`, `frontend_admin_basic.json`).*
>
> *Các flag quan trọng gồm có:*
> * `Positional Arguments`: Danh sách các file JSON báo cáo cần phân tích.*
> * `--output-dir`: Thư mục đích chứa các file Markdown báo cáo.*
> * `--target-prefix`: Flag lọc scope. Ta có thể truyền nhiều lần `--target-prefix` để script chỉ giữ lại các alert thuộc đúng các domain backend (`:3000`), user frontend (`:5173`) hoặc admin frontend (`:5174`), đồng thời loại bỏ các request tạp do trình duyệt truy cập các dịch vụ bên ngoài.*"

---

## 📍 Slide 30: ZAP Testcase & Quy trình Kiểm chứng Thủ công

* **Mục tiêu Slide:** Trình bày cấu trúc một Testcase Replay Request và chốt lại thông điệp: "Bằng chứng đến từ tool, kết luận thuộc về Tester".
* **Thời lượng dự kiến:** 90 giây.

### 🎙️ Kịch bản thuyết trình:
> *"Slide cuối cùng của phần ZAP trình bày về **Testcase Replay Request** (`TC-ZAP-001`) được sinh ra tự động trong file `zap_test_cases.md`.*
>
> *Mỗi testcase cung cấp đầy đủ thông tin để Tester có thể tái lập (replay) lại cảnh báo của ZAP:*
> * HTTP Method, Target URL, Request Headers và Auth Token mà ZAP đã ghi nhận.
> * Quy trình 5 bước kiểm chứng thủ công: Đảm bảo app chạy -> Chuẩn bị Auth -> Replay Request -> Ghi nhận Response -> So sánh bằng chứng với Alert gốc.
>
> * **Thông điệp cốt lõi của phần DAST**: AI hay ZAP chỉ đóng vai trò hỗ trợ phát hiện và gom nhóm cảnh báo. Kết luận cuối cùng về một lỗ hổng (True Positive hay False Positive) **bắt buộc phải do Tester trực tiếp replay request và xác nhận trên môi trường thực tế**.*
>
> *Xin cảm ơn thầy/cô và các bạn đã lắng nghe phần trình bày về DAST & OWASP ZAP. Sau đây xin mời phần tiếp theo!"*

---

## 💡 Ghi chú dành cho Speaker (Q&A Checklist):

1. **Nếu Thầy/Cô hỏi: "Tại sao không quét ZAP GUI thôi mà lại làm thêm ZAP CLI?"**
   * *Trả lời*: ZAP GUI phù hợp cho phân tích thủ công ban đầu. ZAP CLI kết hợp script Python giúp tự động hóa quá trình kiểm thử trong pipeline CI/CD, giúp quét lặp lại định kỳ mà không mất thời gian cấu hình lại bằng tay.

2. **Nếu Thầy/Cô hỏi: "Tại sao ZAP lại cần AJAX Spider mà Traditional Spider chưa đủ?"**
   * *Trả lời*: Traditional Spider chỉ đọc được các thẻ `<a href="...">` trong HTML tĩnh. Với các ứng dụng hiện đại sử dụng React/Vue (SPA), giao diện và đường dẫn API được dựng bằng JavaScript ở client-side. AJAX Spider mở trình duyệt ngầm thực thi JS nên mới tìm thấy các route và request ẩn này.

3. **Nếu Thầy/Cô hỏi: "AI Triage của ZAP đánh giá False Positive dựa trên cơ sở nào?"**
   * *Trả lời*: AI phân tích dựa trên sự tương quan giữa Request header/body và Response header/body mà ZAP ghi nhận. Ví dụ: ZAP báo thiếu header bảo mật nhưng Response trả về từ CDN/Proxy đã có header đó, hoặc alert chỉ là cảnh báo thông tin (Informational) không có khả năng khai thác trong ngữ cảnh EShop.
