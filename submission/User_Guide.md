# Hướng Dẫn Sử Dụng: Security Testing cho EShop

Tài liệu này hướng dẫn chạy quy trình kiểm thử bảo mật của nhóm 06 cho EShop, kết hợp SAST bằng Semgrep và DAST bằng OWASP ZAP. Mục tiêu là phát hiện lỗi từ hai góc nhìn khác nhau: mã nguồn và hành vi runtime của ứng dụng.

## 1. Giới thiệu ngắn OWASP Top 10 2025

OWASP Top 10 là danh sách các nhóm rủi ro bảo mật web phổ biến và quan trọng nhất. Trong workflow này, nhóm dùng danh sách này để chọn ruleset Semgrep và scan policy ZAP.

| Mã | Nhóm rủi ro | Ý nghĩa ngắn |
| --- | --- | --- |
| A01 | Broken Access Control | Ứng dụng kiểm soát quyền truy cập không chặt, cho phép user truy cập dữ liệu hoặc chức năng ngoài quyền. |
| A02 | Security Misconfiguration | Cấu hình server, framework, CORS, header hoặc môi trường triển khai không an toàn. |
| A03 | Software Supply Chain Failures | Rủi ro từ thư viện, dependency, build pipeline, artifact hoặc thành phần bên thứ ba. |
| A04 | Cryptographic Failures | Mã hóa, truyền dữ liệu, lưu secret hoặc bảo vệ dữ liệu nhạy cảm không đúng cách. |
| A05 | Injection | Dữ liệu đầu vào bị đưa vào SQL, command, template hoặc interpreter mà không kiểm soát đúng. |
| A06 | Insecure Design | Thiết kế nghiệp vụ hoặc kiến trúc thiếu cơ chế phòng vệ ngay từ đầu. |
| A07 | Authentication Failures | Xác thực, token, session, reset password hoặc quản lý tài khoản có lỗi. |
| A08 | Software or Data Integrity Failures | Không kiểm chứng tính toàn vẹn của dữ liệu, update, CI/CD hoặc code được nạp vào hệ thống. |
| A09 | Logging and Alerting Failures | Thiếu log, monitoring hoặc cảnh báo khiến việc phát hiện sự cố bị chậm. |
| A10 | Mishandling of Exceptional Conditions | Xử lý lỗi/ngoại lệ không an toàn, làm lộ thông tin hoặc tạo trạng thái hệ thống khó kiểm soát. |

Lưu ý: OWASP Top 10 là nhóm rủi ro, không phải một checklist tự động hoàn chỉnh. Một tool có nhãn OWASP vẫn có thể bỏ sót lỗi thật hoặc báo lỗi cần kiểm chứng thủ công.

## 2. SAST và Semgrep

SAST (Static Application Security Testing) là kiểm thử bảo mật bằng cách phân tích mã nguồn hoặc file cấu hình mà không cần chạy ứng dụng. SAST phù hợp để phát hiện sớm hardcoded secret, pattern gọi API không an toàn, code injection, lỗi framework phổ biến và một số cấu hình rủi ro.

Semgrep là công cụ SAST chạy bằng CLI, dùng rule dạng pattern để tìm đoạn code có dấu hiệu nguy hiểm. Theo đề T09, flow chính dùng ruleset `p/owasp-top-ten` để quét EShop, sau đó output JSON được đưa vào script AI triage để sinh báo cáo kiểm chứng.

## 3. Cài đặt Semgrep

Chạy từ root repo `Seminar-SoftwareTesting`.

### 3.1. Tạo môi trường Python cho script triage

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r src/semgrep/requirements.txt
```

Nếu dùng Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r src/semgrep/requirements.txt
```

### 3.2. Cài Semgrep CLI

Linux/macOS:

```bash
python3 -m pip install semgrep
semgrep --version
```

macOS có Homebrew:

```bash
brew install semgrep
semgrep --version
```

Windows PowerShell:

```powershell
python3 -m pip install semgrep
$env:PYTHONUTF8='1'
chcp 65001
semgrep --version
```

Nếu terminal báo `semgrep: command not found`, thêm thư mục user package vào `PATH`, ví dụ:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

## 4. Chạy Semgrep cơ bản

Giả sử source EShop nằm trong repo seminar tại `./eshop-sut`:

```text
Seminar-SoftwareTesting/
├── eshop-sut/
└── src/semgrep/
```

Quét nhanh EShop theo OWASP Top 10:

```bash
semgrep scan --config "p/owasp-top-ten" ./eshop-sut
```

Quét EShop theo OWASP Top 10 và bỏ qua dependency/build output:

```bash
semgrep scan \
  --config "p/owasp-top-ten" \
  --exclude node_modules \
  --exclude dist \
  --exclude build \
  --exclude .next \
  ./eshop-sut
```

Lưu ý: Đây là lệnh chính theo yêu cầu đề T09: chạy Semgrep với `p/owasp-top-ten`.

Option khác là dùng file `.semgrepignore` để Semgrep tự bỏ qua các thư mục/file không cần scan. Cách này gọn hơn khi phải chạy nhiều lần hoặc dùng chung với pipeline.

Tạo file ignore trong root source EShop:

```bash
cat > ./eshop-sut/.semgrepignore <<'EOF'
node_modules/
dist/
build/
.next/
coverage/
*.min.js
EOF
```

Sau đó có thể bỏ các flag `--exclude` khỏi lệnh scan:

```bash
semgrep scan \
  --config "p/owasp-top-ten" \
  ./eshop-sut
```

Chỉ nên ignore các thư mục generated, dependency, build output hoặc file nhiễu. Không nên ignore source chính như `backend/`, `frontend/src/` vì có thể làm mất finding thật.

Xuất JSON để xử lý tiếp:

```bash
mkdir -p src/semgrep/output
semgrep scan \
  --config "p/owasp-top-ten" \
  --exclude node_modules \
  --exclude dist \
  --exclude build \
  --exclude .next \
  --json \
  -o src/semgrep/output/semgrep_results.json \
  ./eshop-sut
```

Nếu đã tạo `./eshop-sut/.semgrepignore`, có thể dùng lệnh JSON ngắn hơn:

```bash
mkdir -p src/semgrep/output
semgrep scan \
  --config "p/owasp-top-ten" \
  --json \
  -o src/semgrep/output/semgrep_results.json \
  ./eshop-sut
```

Nếu source EShop nằm ở path khác, đặt biến `SOURCE_ROOT` rồi dùng lại biến đó trong lệnh scan:

```bash
SOURCE_ROOT="/path/to/eshop-sut"
semgrep scan \
  --config "p/owasp-top-ten" \
  --exclude node_modules \
  --exclude dist \
  --exclude build \
  --exclude .next \
  --json \
  -o src/semgrep/output/semgrep_results.json \
  "$SOURCE_ROOT"
```

## 5. Flow Semgrep của nhóm

Flow đầy đủ bắt đầu từ quét mã nguồn bằng Semgrep, sau đó xuất kết quả JSON, kiểm tra finding thô, đưa vào AI triage, kiểm chứng lại bằng source context và cuối cùng ghi báo cáo.

### 5.1. Xác định source code cần quét

Chạy các lệnh từ root repo `Seminar-SoftwareTesting`. Theo README Semgrep hiện tại, mặc định nhóm đặt source EShop trong repo seminar tại `./eshop-sut`:

```text
Seminar-SoftwareTesting/
├── eshop-sut/
└── src/semgrep/
```

Nếu source nằm đúng vị trí trên, đường dẫn scan là `./eshop-sut`. Nếu source nằm nơi khác, đặt biến `SOURCE_ROOT` bằng đường dẫn thật, ví dụ `/Users/mac/projects/eshop-sut`.

Trước khi quét, kiểm tra nhanh thư mục source:

```bash
ls ./eshop-sut
```

Không quét các thư mục dependency hoặc build output như `node_modules`, `dist`, `build`, `.next` vì chúng làm kết quả nhiễu và tốn thời gian.

### 5.2. Chọn source root khi source nằm nơi khác

Git Bash/Bash:

```bash
SOURCE_ROOT="/path/to/eshop-sut"
```

Windows PowerShell:

```powershell
$env:SOURCE_ROOT="C:\path\to\eshop-sut"
```

### 5.3. Quét mã nguồn và xuất kết quả JSON

Trong flow chính, nhóm chạy Semgrep với `p/owasp-top-ten` theo đúng yêu cầu đề T09, đồng thời xuất kết quả ra JSON.

Nếu source nằm trong repo tại `./eshop-sut`:

```bash
mkdir -p src/semgrep/output
semgrep scan \
  --config "p/owasp-top-ten" \
  --exclude node_modules \
  --exclude dist \
  --exclude build \
  --exclude .next \
  --json \
  -o src/semgrep/output/semgrep_results.json \
  ./eshop-sut
```

Nếu source đã có `.semgrepignore`, lệnh flow chính có thể rút gọn:

```bash
mkdir -p src/semgrep/output
semgrep scan \
  --config "p/owasp-top-ten" \
  --json \
  -o src/semgrep/output/semgrep_results.json \
  ./eshop-sut
```

Nếu source nằm ở path khác:

```bash
semgrep scan \
  --config "p/owasp-top-ten" \
  --exclude node_modules \
  --exclude dist \
  --exclude build \
  --exclude .next \
  --json \
  -o src/semgrep/output/semgrep_results.json \
  "$SOURCE_ROOT"
```

Ở bước này, đọc nhanh output trên terminal để nắm:

- File và dòng code có cảnh báo.
- Rule ID, severity và message của Semgrep.
- Đoạn code bị đánh dấu.
- Nhóm lỗi OWASP hoặc loại lỗi tương ứng, ví dụ secret hardcoded, HTTP không mã hóa, injection pattern.

Kiểm tra file kết quả đã được tạo:

```bash
ls src/semgrep/output/semgrep_results.json
```

File `semgrep_results.json` là bằng chứng scan gốc theo OWASP Top 10, nên giữ lại để đối chiếu với báo cáo triage và kết quả demo.

### 5.3.1. Quét mở rộng theo công nghệ EShop

Sau khi đã có kết quả bắt buộc theo `p/owasp-top-ten`, có thể chạy thêm ruleset theo công nghệ EShop để phân tích sâu hơn và phục vụ phần failure modes/rule coverage.

```bash
mkdir -p src/semgrep/output
semgrep scan \
  --config "p/owasp-top-ten" \
  --config "p/nodejs" \
  --config "p/javascript" \
  --config "p/react" \
  --config "src/semgrep/rules/eshop-security.yml" \
  --exclude node_modules \
  --exclude dist \
  --exclude build \
  --exclude .next \
  --json \
  -o src/semgrep/output/semgrep_results_extended.json \
  ./eshop-sut
```

Lệnh mở rộng này không thay thế lệnh OWASP Top 10 trong flow chính; nó dùng để đối chiếu thêm khi cần phân tích vì sao ruleset mặc định có thể bỏ sót một số pattern trong EShop.

### 5.4. Cấu hình AI provider cho bước triage

Git Bash/Bash:

```bash
cp src/semgrep/.env.example src/semgrep/.env
```

Windows PowerShell:

```powershell
copy src\semgrep\.env.example src\semgrep\.env
```

Điền key thật vào `src/semgrep/.env` nếu muốn gọi AI qua OpenRouter:

```env
AI_PROVIDER=openai-compatible
AI_MODEL=google/gemini-2.5-flash-lite
OPENROUTER_API_KEY=sk-or-v1-...
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
```

Không commit file `.env` thật vì có chứa API key.

### 5.5. Chạy AI triage trên kết quả Semgrep

Sau khi có `src/semgrep/output/semgrep_results.json`, chạy script triage. Nếu source nằm trong repo tại `./eshop-sut`:

```bash
python src/semgrep/semgrep_ai_triage.py \
  src/semgrep/output/semgrep_results.json \
  --source-root eshop-sut \
  --output-dir src/semgrep/output
```

Nếu source nằm ở path khác:

```bash
python src/semgrep/semgrep_ai_triage.py \
  src/semgrep/output/semgrep_results.json \
  --source-root "$SOURCE_ROOT" \
  --output-dir src/semgrep/output
```

Script sẽ đọc từng finding trong JSON, lấy source context từ `--source-root`, tạo prompt phân tích và sinh báo cáo tổng hợp. Nếu không có API key, vẫn có thể chạy triage offline để sinh prompt, skeleton output và báo cáo tổng hợp. Ví dụ với source trong repo:

```bash
python src/semgrep/semgrep_ai_triage.py \
  src/semgrep/output/semgrep_results.json \
  --source-root eshop-sut \
  --output-dir src/semgrep/output \
  --offline
```

### 5.6. Kiểm tra output triage

Sau khi triage xong, kiểm tra các file chính:

```bash
ls src/semgrep/output
ls src/semgrep/output/findings
```

Output cần nộp hoặc dùng khi demo:

- `src/semgrep/output/semgrep_results.json`: kết quả scan gốc từ Semgrep.
- `src/semgrep/output/semgrep_triage_report.md`: báo cáo tổng hợp sau triage.
- `src/semgrep/output/semgrep_postman_validation_report.md`: format lỗi dùng để đối chiếu Postman/ZAP comparison.
- `src/semgrep/output/findings/`: prompt và output riêng cho từng finding.

Khi đọc báo cáo, nhóm cần kiểm chứng lại từng finding bằng source code thật:

- Finding có nằm trong code tự viết của EShop hay chỉ nằm trong dependency/build output.
- Dữ liệu người dùng có đi tới sink nguy hiểm hay không.
- Secret, token, URL HTTP hoặc cấu hình yếu có dùng ở runtime hay chỉ là sample/test.
- AI có giải thích đúng file, dòng code, impact và remediation hay không.
- Kết luận cuối cùng là `True Positive`, `False Positive`, `Needs Manual Review` hoặc `Not Applicable`.

Trong output hiện có, Semgrep ghi nhận 12 findings, gồm hardcoded JWT secret trong `backend/server.js` và nhiều request HTTP không mã hóa trong `frontend-mobile/App.js`.

## 6. DAST và OWASP ZAP

DAST (Dynamic Application Security Testing) là kiểm thử bảo mật trên ứng dụng đang chạy thật. DAST không cần đọc source code; thay vào đó, tool gửi request HTTP, quan sát response, crawl trang, chạy passive scan và có thể active scan bằng payload kiểm thử.

OWASP ZAP là công cụ DAST mã nguồn mở. Trong project này, ZAP được dùng theo hai cách:

- Chạy bằng GUI để proxy trình duyệt, quan sát request/response, tạo context và cấu hình authentication thủ công.
- Chạy bằng CLI qua `src/zap/scan_zap.py` để tự động hóa scan, xuất report JSON/HTML và đưa JSON vào bước AI triage.

## 7. Cài đặt OWASP ZAP

Chạy từ root repo `Seminar-SoftwareTesting`.

### 7.1. Cài ZAP GUI

ZAP GUI cần Java 17 trở lên, trừ khi bản cài đặt đã bundle Java hoặc chạy bằng Docker.

Windows:

```powershell
winget install --id=ZAP.ZAP -e
```

macOS:

```bash
brew install --cask zap
```

Linux qua Flatpak:

```bash
flatpak install flathub org.zaproxy.ZAP
flatpak run org.zaproxy.ZAP
```

Linux qua Snap:

```bash
sudo snap install zaproxy --classic
zaproxy
```

Qua trang chủ bằng package:

1. Mở https://www.zaproxy.org/download/.
2. Tải **Linux Package** nếu dùng Linux, hoặc **Cross Platform Package** nếu cần bản chạy đa nền tảng.
3. Giải nén file tải về, ví dụ:

```bash
tar -xf ZAP_<version>_Linux.tar.gz
cd ZAP_<version>
./zap.sh
```

Với Windows/macOS, trang Download cũng có installer riêng cho từng hệ điều hành. Windows và Linux package cần Java 17+ đã cài sẵn; macOS installer đã bundle Java.

Nếu ZAP GUI trên Linux báo môi trường headless hoặc cửa sổ trắng, kiểm tra lại Java bản đầy đủ và dùng hướng dẫn chi tiết trong `src/zap/installation.md`.

### 7.2. Cài dependency cho CLI flow

Tạo hoặc kích hoạt virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install python-owasp-zap-v2.4
```

Nếu dùng Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install python-owasp-zap-v2.4
```

CLI flow cần ZAP daemon tại `http://localhost:8090`. Có thể chạy bằng Docker:

```bash
docker run --rm -d --name eshop-zap --network host \
  -v $(pwd):$(pwd) \
  ghcr.io/zaproxy/zaproxy:stable zap.sh -daemon \
  -port 8090 -host 0.0.0.0 -config api.disablekey=true
```

### 7.3. Chuẩn bị cấu hình ZAP

```bash
cp src/zap/.env.example src/zap/.env
```

Các biến quan trọng trong `src/zap/.env`:

```env
ZAP_TARGET=http://localhost:3000
ZAP_URL=http://localhost:8090
ZAP_AUTH_ROLE=none
ZAP_MAX_URLS=300
ZAP_REPORT_FORMAT=json
ZAP_REPORT_FILE=src/zap/output/backend_basic.json
```

`ZAP_MAX_URLS` là giới hạn số URL trước khi chạy active scan. Nếu spider/AJAX Spider crawl vượt giới hạn này, script vẫn giữ kết quả spider/passive scan và xuất report, nhưng bỏ qua active scan để tránh quá tải RAM. Có thể bỏ trống biến này nếu muốn active scan không bị giới hạn.

Nếu scan có authentication, điền credential test tương ứng:

```env
ZAP_USER_EMAIL=test@eshop.com
ZAP_USER_PASSWORD=Test1234!
ZAP_ADMIN_EMAIL=admin@eshop.com
ZAP_ADMIN_PASSWORD=Admin123!
```

Không commit file `.env` thật vì có thể chứa credential hoặc API key.

## 8. Chạy ZAP bằng GUI

Chỉ scan hệ thống local/lab mà nhóm có quyền kiểm thử. Trước khi chạy GUI, khởi động EShop:

- Backend: `http://localhost:3000`
- Frontend Web/User: `http://localhost:5173`
- Frontend Admin: `http://localhost:5174`

### 8.1. GUI scan không login

Flow này dùng để scan phần public như trang sản phẩm, endpoint public hoặc backend API không cần token.

1. Mở OWASP ZAP GUI.
2. Ở màn hình session, chọn không lưu session nếu demo nhanh, hoặc lưu session nếu cần evidence.
3. Vào `Quick Start` -> `Automated Scan`.
4. Nhập target public, ví dụ `http://localhost:3000` hoặc `http://localhost:5173` hoặc `http://localhost:5174`.
5. Nhấn `Attack`.
6. Sau khi scan xong, xem:
   - `Sites`: URL đã crawl được.
   - `History`: request/response runtime.
   - `Alerts`: danh sách cảnh báo.
   - `Request`/`Response`: evidence của từng alert.

Với frontend SPA, nên dùng thêm `Manual Explore` hoặc `AJAX Spider` vì nhiều route/API chỉ xuất hiện sau khi JavaScript chạy.

### 8.2. Cấu hình browser proxy cho GUI

Để ZAP bắt được traffic thực từ người dùng, cấu hình Firefox đi qua ZAP proxy:

1. Trong ZAP, vào `Tools` -> `Options...` -> `Network` -> `Local Servers/Proxies`.
2. Xác nhận main proxy là `localhost:8080`.
3. Trong Firefox, vào `Settings` -> `Network Settings`.
4. Chọn manual proxy và nhập HTTP proxy `localhost`, port `8080`.
5. Nếu traffic `localhost` không xuất hiện trong ZAP, mở `about:config` và đặt `network.proxy.allow_hijacking_localhost=true`.

Hình minh họa chi tiết nằm trong `src/zap/gui_scan.md`.

### 8.3. GUI scan có authentication

Flow này dùng để scan các chức năng cần đăng nhập như giỏ hàng, profile hoặc API user/admin.

1. Mở EShop trong Firefox đã cấu hình proxy.
2. Đăng nhập hoặc đăng ký bằng tài khoản test để ZAP ghi nhận request login.
3. Trong cây `Sites`, đưa cả frontend `http://localhost:5173` và backend `http://localhost:3000` vào cùng context.
4. Chọn request `POST /api/login`, click chuột phải và chọn `Flag as Context` -> context tương ứng -> `JSON-based Auth Login Request`.
5. Trong context, mở phần `Authentication` và kiểm tra login URL, method, payload JSON và dấu hiệu đăng nhập thành công.
6. Mở tab `Users`, tạo user test và nhập username/password.
7. Bật `Forced User Mode` để ZAP gắn user đã cấu hình vào request trong context.
8. Chạy `Spider...` hoặc `AJAX Spider...` trên context. Với frontend React/SPA, ưu tiên bật AJAX Spider.
9. Chỉ chạy `Active Scan...` sau khi scope đúng, số URL trong `Sites` không quá lớn, và tài khoản test có thể bị thay đổi dữ liệu mà không ảnh hưởng môi trường thật. Nếu AJAX Spider tạo hàng trăm hoặc hàng nghìn URL, nên dừng ở passive scan cho frontend rồi active scan backend/API riêng.

Kết quả cần lưu lại:

- Host frontend/backend trong `Sites`.
- Request login và request xác minh user như `/api/users/me`.
- Alert trong tab `Alerts`.
- Request/response evidence cho từng alert quan trọng.

## 9. Chạy ZAP bằng CLI trong `src/zap`

Script `src/zap/scan_zap.py` tự động kết nối ZAP daemon, chuẩn bị context/auth nếu cần, chạy spider, tùy chọn AJAX Spider, passive scan, active scan và export report. Script hiện hỗ trợ target local trên các cổng `3000`, `5173`, `5174`. Với frontend SPA, dùng thêm `--max-urls` để đặt ngân sách URL trước active scan; nếu crawl vượt ngân sách, script sẽ bỏ qua active scan để tránh tràn RAM.

### 9.1. Chạy CLI không login

Dùng khi scan backend public hoặc frontend public, không cần token/cookie.

Backend API, xuất JSON để đưa vào AI:

```bash
python src/zap/scan_zap.py \
  --target http://localhost:3000 \
  --report-format json \
  --output-file src/zap/output/backend_basic.json
```

Frontend user public, có AJAX Spider để khám phá route SPA:

```bash
python src/zap/scan_zap.py \
  --target http://localhost:5173 \
  --ajax-spider \
  --max-urls 300 \
  --report-format json \
  --output-file src/zap/output/frontend_public_basic.json
```

Nếu chỉ cần đọc thủ công, đổi `--report-format html` và đặt output `.html`.

### 9.2. Chạy CLI có authentication

Dùng khi cần scan dưới quyền user hoặc admin. Trước khi chạy, đảm bảo `src/zap/.env` có credential đúng và backend đang chạy.

Frontend user:

```bash
python src/zap/scan_zap.py \
  --target http://localhost:5173 \
  --auth-role user \
  --forced-user \
  --ajax-spider \
  --max-urls 300 \
  --report-format json \
  --output-file src/zap/output/frontend_user_basic.json
```

Frontend admin:

```bash
python src/zap/scan_zap.py \
  --target http://localhost:5174 \
  --auth-role admin \
  --forced-user \
  --ajax-spider \
  --max-urls 300 \
  --report-format json \
  --output-file src/zap/output/frontend_admin_basic.json
```

Backend authenticated API scan dưới quyền user:

```bash
python src/zap/scan_zap.py \
  --target http://localhost:3000 \
  --auth-role user \
  --forced-user \
  --report-format json \
  --output-file src/zap/output/backend_user_basic.json
```

Nếu scan authenticated báo `401/403`, kiểm tra credential trong `.env`, endpoint login `http://localhost:3000/api/login`, và endpoint verify `http://localhost:3000/api/users/me`.

Khi thấy log dạng `URL budget: discovered 13055/300 URLs for active scan`, nghĩa là frontend đã crawl vượt `--max-urls`; lúc đó report vẫn có dữ liệu spider/passive scan, nhưng sẽ không có bằng chứng active scan cho target đó. Nếu cần active scan, ưu tiên chạy trên backend/API `http://localhost:3000` hoặc giảm scope frontend trước khi tăng giới hạn.

### 9.3. Ý nghĩa flag chính

| Flag | Ý nghĩa |
| --- | --- |
| `--target` | URL cần scan: backend `3000`, frontend user `5173`, frontend admin `5174`. |
| `--zap-url` | URL ZAP daemon, mặc định `http://localhost:8090`. |
| `--api-key` | API key nếu ZAP daemon bật key. Lab mặc định dùng `api.disablekey=true`. |
| `--auth-role` | Chọn tài khoản seed để đăng nhập: `none`, `user`, `admin`. |
| `--forced-user` | Bật Forced User Mode để scan dưới user đã cấu hình. |
| `--ajax-spider` | Dùng AJAX Spider, cần thiết cho frontend React/SPA. |
| `--max-urls` | Giới hạn số URL trước active scan; nếu vượt giới hạn thì bỏ qua active scan để tránh quá tải RAM. |
| `--report-format` | `html` để đọc thủ công, `json` để pipeline/AI xử lý. |
| `--output-file` | Đường dẫn file report đầu ra. |

### 9.4. Kiểm tra output scan

Sau khi chạy CLI, kiểm tra file report:

```bash
ls src/zap/output
```

Output chính thường dùng:

- `src/zap/output/backend_basic.json`: report backend public.
- `src/zap/output/frontend_user_basic.json`: report frontend dưới quyền user.
- `src/zap/output/frontend_admin_basic.json`: report frontend dưới quyền admin.

Khi đọc report, nhóm cần kiểm chứng:

- Alert thuộc đúng target và scope EShop.
- Endpoint có public hay cần authentication.
- Evidence trong request/response có đủ để kết luận lỗi thật.
- Alert là lỗi runtime thật hay noise do môi trường local HTTP/dev server.

## 10. Sử dụng AI để phân tích ZAP report

Script `src/zap/zap_ai_triage.py` đọc report JSON của ZAP, lọc alert có risk đáng chú ý, chuẩn hóa endpoint/evidence và sinh báo cáo Markdown. Script ưu tiên OpenAI nếu có `OPENAI_API_KEY`, nếu không thì dùng OpenRouter khi có `OPENROUTER_API_KEY`. Nếu API lỗi, script fallback sang local deterministic triager.

### 10.1. Cấu hình AI provider

Mở `src/zap/.env` và điền một trong hai nhóm cấu hình.

OpenAI:

```env
OPENAI_API_KEY=your_openai_key
OPENAI_MODEL=gpt-4o-mini
```

OpenRouter:

```env
OPENROUTER_API_KEY=your_openrouter_key
OPENROUTER_MODEL=google/gemini-2.5-flash
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1/chat/completions
OPENROUTER_TIMEOUT=60
OPENROUTER_MAX_TOKENS=4096
```

Không commit API key thật vào repository.

### 10.2. Chạy AI triage cho một hoặc nhiều report

```bash
python src/zap/zap_ai_triage.py \
  --input \
    src/zap/output/backend_basic.json \
    src/zap/output/frontend_user_basic.json \
    src/zap/output/frontend_admin_basic.json \
  --format markdown \
  --output src/zap/output/zap_ai_triage_report.md
```

Nếu chỉ có một report:

```bash
python src/zap/zap_ai_triage.py \
  --input src/zap/output/backend_basic.json \
  --format markdown \
  --output src/zap/output/zap_backend_ai_triage.md
```

## 11. Test endpoint để đối chiếu ZAP với Semgrep

Mục tiêu phần này là dùng runtime evidence từ ZAP hoặc `curl` để kiểm tra finding từ Semgrep có biểu hiện trên ứng dụng đang chạy hay không.

### 11.1. Chuẩn bị token đăng nhập

Đăng nhập admin:

```bash
curl -s -X POST http://localhost:3000/api/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@eshop.com","password":"Admin123!"}'
```

Đăng nhập user:

```bash
curl -s -X POST http://localhost:3000/api/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@eshop.com","password":"Test1234!"}'
```

Copy giá trị `token` trong response để dùng ở các bước sau:

```bash
TOKEN="paste_token_here"
```

### 11.2. Đối chiếu hardcoded JWT secret

Semgrep finding:

- Rule: `javascript.jsonwebtoken.security.jwt-hardcode.hardcoded-jwt-secret`
- File: `backend/server.js`
- OWASP: A07 Authentication Failures

Kiểm tra runtime:

```bash
curl -i http://localhost:3000/api/users/me \
  -H "Authorization: Bearer $TOKEN"
```

Kết quả cần ghi nhận:

- Nếu token hợp lệ trả `200`, endpoint đang tin vào JWT.
- Nếu tạo được token giả bằng secret hardcode trong PoC và backend vẫn trả `200`, finding được xác nhận là lỗi nghiêm trọng.
- Nếu backend đã đổi secret qua biến môi trường hoặc verify thất bại, cập nhật trạng thái finding thành đã khắc phục hoặc không tái lập được.

### 11.3. Đối chiếu cleartext HTTP request

Semgrep finding:

- Rule: `typescript.react.security.react-insecure-request.react-insecure-request`
- File: `frontend-mobile/App.js`
- OWASP: A04 Cryptographic Failures

Kiểm tra runtime:

```bash
curl -i http://localhost:3000/api/users/me \
  -H "Authorization: Bearer $TOKEN"
```

Kết quả cần ghi nhận:

- Nếu ứng dụng đang chạy production mà vẫn dùng `http://`, đây là rủi ro truyền dữ liệu nhạy cảm không mã hóa.
- Nếu chỉ là lab local, đánh dấu là finding hợp lệ về pattern nhưng cần phân loại theo môi trường.
- Trong ZAP report, đối chiếu alert `HTTP Only Site` hoặc các request đi qua `http://localhost:3000`.

### 11.4. Đối chiếu CORS/Cross-Domain Misconfiguration

ZAP thường phát hiện `Access-Control-Allow-Origin: *` trên backend.

```bash
curl -i http://localhost:3000/api/products?search=iphone \
  -H "Origin: http://evil.local"
```

Kết quả cần ghi nhận:

- Nếu response có `Access-Control-Allow-Origin: *`, alert ZAP có evidence rõ.
- Nếu endpoint trả dữ liệu công khai, impact thấp hơn endpoint trả dữ liệu cá nhân.
- Nếu endpoint cần đăng nhập, chạy lại với `Authorization: Bearer $TOKEN` để đánh giá rủi ro đọc dữ liệu từ origin lạ.

### 11.5. Đối chiếu SQL Injection trên search sản phẩm

Trong tài liệu Semgrep, nhóm từng ghi nhận trường hợp SQL Injection ở `backend/server.js` có thể bị ruleset mặc định bỏ sót. Vì vậy cần test thủ công:

```bash
curl -i "http://localhost:3000/api/products?search=' OR '1'='1"
```

Kết quả cần ghi nhận:

- Nếu response trả danh sách sản phẩm bất thường hoặc lỗi SQL, cần mở source kiểm tra query có nối chuỗi trực tiếp không.
- Nếu response được parameterize và không thay đổi bất thường, ghi nhận là không tái lập được.
- So sánh với ZAP: active scan có thể tạo alert Injection hoặc không; nếu ZAP không báo nhưng test tay tái lập được, đó là false negative của DAST.

### 11.6. Mẫu bảng đối chiếu

| Finding/Alert | Nguồn | Endpoint/File | Evidence runtime | Kết luận |
| --- | --- | --- | --- | --- |
| Hardcoded JWT Secret | Semgrep | `backend/server.js`, `/api/users/me` | Token hợp lệ/giả mạo được backend chấp nhận hoặc bị từ chối | Confirmed / Fixed / Needs Verification |
| Cleartext HTTP | Semgrep + ZAP | `frontend-mobile/App.js`, `http://localhost:3000` | Request dùng HTTP, ZAP có `HTTP Only Site` | Confirmed / Dev-only |
| CORS `*` | ZAP | `/api/products?search=` | Header `Access-Control-Allow-Origin` | Confirmed / Low impact / Needs Auth Check |
| SQL Injection search | Manual + ZAP | `/api/products?search=` | Response bất thường hoặc lỗi SQL | Confirmed / False Negative / Not Reproducible |

## 12. Xử lý sự cố

| Vấn đề | Dấu hiệu | Nguyên nhân thường gặp | Cách xử lý |
| --- | --- | --- | --- |
| Không cài được package Python global | `externally-managed-environment` | Distro chặn cài pip vào system Python | Dùng `.venv` rồi cài dependency trong virtual environment. |
| Semgrep không tìm thấy source | Lệnh scan báo không có `./eshop-sut` hoặc `$SOURCE_ROOT` | Source EShop nằm khác vị trí mặc định hoặc biến `SOURCE_ROOT` sai | Kiểm tra `ls ./eshop-sut`; nếu source nằm nơi khác, đặt lại `SOURCE_ROOT` bằng đường dẫn source thật. |
| OpenRouter trả `402` | AI triage lỗi billing/credit | Hết credit hoặc model quá tốn token | Dùng model nhẹ hơn, nạp credit hoặc chạy/đọc output offline. |
| ZAP không khởi động | Docker unavailable hoặc image pull lỗi | Docker chưa chạy, thiếu quyền, mạng chậm | Kiểm tra Docker daemon, pull trước image ZAP hoặc dùng ZAP GUI/daemon tự chạy tại `localhost:8090`. |
| Authenticated ZAP scan lỗi `401/403` | Login hoặc `/api/users/me` fail | Sai credential, account bị khóa, backend chưa chạy | Reset dữ liệu test, đổi credential trong `.env`, kiểm tra backend `3000`. |
| Report backend lẫn frontend | JSON/HTML có nhiều `site` khác target | ZAP daemon giữ session cũ hoặc output file đặt nhầm | Tạo session mới/clear history trong ZAP, hoặc dùng file output riêng cho từng target. |

## 13. Tài liệu tham khảo

- OWASP Top 10 2025: https://owasp.org/www-project-top-ten/
- Semgrep documentation: https://semgrep.dev/docs/
- OWASP ZAP Getting Started: https://www.zaproxy.org/getting-started/
- OWASP ZAP Download: https://www.zaproxy.org/download/
- OWASP ZAP Report Generation: https://www.zaproxy.org/docs/desktop/addons/report-generation/
- Tài liệu trong repo: `docs/semgrep/`, `src/semgrep/`, `docs/zap/`, `src/zap/`, `weekly-reports/Group06_06/Group06.md`.

## 14. Công bố sử dụng AI

Nhóm có sử dụng AI để hỗ trợ soạn thảo hướng dẫn, phân tích Semgrep findings và triage ZAP alerts. Các command, flag CLI, đường dẫn output và nhận định kỹ thuật cần được thành viên nhóm kiểm tra lại bằng source code, report JSON/HTML và request runtime trước khi đưa vào kết luận cuối cùng.
