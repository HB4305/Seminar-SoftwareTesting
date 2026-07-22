# Flow Demo Semgrep: Từ Cài Đặt Đến Kiểm Chứng PoC

Tài liệu này dùng làm kịch bản quay video demo quy trình Semgrep cho EShop: giới thiệu Semgrep, cài đặt, quét mã nguồn, chạy AI triage, đọc report, tạo test case Postman và kiểm chứng PoC.

## 1. Mục Tiêu Demo

Trong video, trình bày quy trình:

1. Giới thiệu ngắn Semgrep và vai trò của SAST.
2. Cài Semgrep CLI.
3. Chuẩn bị môi trường Python cho AI triage.
4. Quét source EShop bằng Semgrep.
5. Xuất kết quả scan ra JSON.
6. Chạy AI triage để sinh report Markdown.
7. Đọc finding và test case Postman được sinh ra.
8. Chạy EShop backend.
9. Kiểm chứng PoC bằng Postman hoặc command line.

Lời dẫn gợi ý:

```text
Trong video này, em sẽ demo toàn bộ flow Semgrep của nhóm cho hệ thống EShop.
Flow bắt đầu từ giới thiệu nhanh Semgrep, cài đặt CLI, chạy scan mã nguồn, xuất kết quả JSON, đưa kết quả vào AI triage, sau đó dùng report sinh ra để kiểm chứng bằng Postman.
Mục tiêu không chỉ là xem Semgrep báo lỗi gì, mà còn chứng minh finding đó có thể được map thành PoC runtime để tester kiểm chứng lại.
```

## 2. Giới Thiệu Ngắn Về Semgrep

Semgrep là công cụ SAST, tức là phân tích bảo mật tĩnh trên mã nguồn mà không cần chạy ứng dụng. Công cụ này dùng các ruleset để tìm những pattern code có dấu hiệu rủi ro, ví dụ:

- Hardcoded secret hoặc hardcoded JWT secret.
- Request dùng HTTP không mã hóa.
- Pattern injection.
- Cấu hình hoặc API usage không an toàn.
- Một số lỗi framework phổ biến theo ngôn ngữ/công nghệ.

Trong flow này, Semgrep được dùng để quét source EShop và xuất finding ra JSON. Sau đó script AI triage của nhóm đọc JSON này, bổ sung source context, format lại finding thành báo cáo dễ đọc và sinh test case Postman để kiểm chứng.

Lưu ý quan trọng:

```text
Semgrep phát hiện dấu hiệu lỗi từ source code.
Kết quả Semgrep cần được kiểm chứng lại bằng source context và PoC runtime.
AI triage chỉ hỗ trợ phân tích và format report, không thay thế kết luận của tester.
```

Lời dẫn gợi ý:

```text
Trước khi chạy demo, em giới thiệu nhanh về Semgrep. Semgrep là công cụ SAST, nghĩa là nó đọc source code để tìm các pattern có rủi ro bảo mật mà không cần chạy ứng dụng.
Trong project này, Semgrep giúp phát hiện các vấn đề như hardcoded JWT secret, request HTTP không mã hóa hoặc các pattern code nguy hiểm khác.
Tuy nhiên, kết quả Semgrep không nên được xem là kết luận cuối ngay lập tức. Sau khi scan, nhóm vẫn cần đọc source evidence, chạy AI triage để format finding, rồi kiểm chứng lại bằng Postman/PoC.
```

## 3. Chuẩn Bị Repository

Chạy từ root repo `Seminar-SoftwareTesting`.

```powershell
pwd
dir
dir eshop-sut
dir src\semgrep
```

Cấu trúc mong đợi:

```text
Seminar-SoftwareTesting/
├── eshop-sut/
└── src/semgrep/
```

Nếu source EShop nằm ngoài repo, dùng biến `SOURCE_ROOT`:

```powershell
$env:SOURCE_ROOT="C:\path\to\eshop-sut"
```

Lời dẫn gợi ý:

```text
Đầu tiên em kiểm tra cấu trúc project. Repo seminar chứa thư mục `src/semgrep` là nơi đặt script triage, rules và output. Source code cần quét là EShop, hiện đang nằm trong thư mục `eshop-sut`.
Nếu source nằm ngoài repo thì có thể dùng biến `SOURCE_ROOT`, nhưng trong demo này em dùng trực tiếp `./eshop-sut`.
```

## 4. Cài Đặt Semgrep CLI

Semgrep CLI là công cụ chạy trực tiếp trên terminal để quét source code. Trong demo này, CLI nhận thư mục `eshop-sut` làm input, tải ruleset từ Semgrep Registry, phân tích mã nguồn và xuất kết quả ra JSON.

Windows PowerShell:

```powershell
python -m pip install --user pipx
python -m pipx ensurepath
```

Đóng và mở lại PowerShell, sau đó chạy:

```powershell
pipx install semgrep
semgrep --version
```

Giải thích lệnh Windows:

| Lệnh                                | Ý nghĩa                                                                     |
| ----------------------------------- | --------------------------------------------------------------------------- |
| `python -m pip install --user pipx` | Cài`pipx` vào user Python environment.                                      |
| `python -m pipx ensurepath`         | Thêm thư mục binary của`pipx` vào `PATH` để gọi được command đã cài.        |
| `pipx install semgrep`              | Cài Semgrep CLI vào môi trường riêng, không trộn với package Python global. |
| `semgrep --version`                 | Kiểm tra Semgrep CLI đã cài thành công và có thể gọi từ terminal.           |

Lý do dùng `pipx` trên Windows:

- Tránh lỗi khi cài Semgrep trực tiếp bằng `pip` vào global Python.
- Giảm rủi ro xung đột dependency với Anaconda hoặc Python project khác.
- Semgrep được đặt trong môi trường riêng nhưng vẫn gọi được như một command bình thường.
- Nếu cần gỡ hoặc nâng cấp, thao tác đơn giản hơn:

```powershell
pipx upgrade semgrep
pipx uninstall semgrep
```

macOS:

```bash
brew install semgrep
semgrep --version
```

Linux:

```bash
python3 -m pip install semgrep
semgrep --version
```

Lời dẫn gợi ý:

```text
Tiếp theo là cài Semgrep CLI. Đây là command line tool dùng để quét source code. Trong demo, Semgrep CLI sẽ đọc thư mục `eshop-sut`, áp ruleset bảo mật và xuất kết quả scan ra JSON.
Trên Windows, nhóm ưu tiên dùng `pipx` thay vì cài trực tiếp bằng pip global. `pipx` tạo môi trường riêng cho Semgrep, giúp tránh xung đột dependency với Anaconda hoặc Python project khác, đồng thời hạn chế lỗi build package native.
Sau khi cài xong, em chạy `semgrep --version` để xác nhận terminal đã nhận command Semgrep.
Với macOS có thể dùng Homebrew, còn Linux có thể cài bằng pip hoặc pipx tùy môi trường.
```

## 5. Chuẩn Bị Python Environment Cho AI Triage

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r src/semgrep/requirements.txt
```

Git Bash/Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r src/semgrep/requirements.txt
```

Lời dẫn gợi ý:

```text
Semgrep CLI dùng để scan, còn script AI triage là Python script riêng của nhóm. Vì vậy em tạo virtual environment `.venv` và cài dependency trong `src/semgrep/requirements.txt`.
Việc tách venv giúp môi trường demo ổn định hơn và không phụ thuộc vào Python global.
```

## 6. Chạy Semgrep Scan

Tạo thư mục output:

```powershell
New-Item -ItemType Directory -Force src/semgrep/output
```

Scan chính theo OWASP Top 10:

```powershell
semgrep scan --config "p/owasp-top-ten" --exclude node_modules --exclude dist --exclude build --exclude .next --json -o src/semgrep/output/semgrep_results.json ./eshop-sut
```

Nếu source nằm ở path khác:

```powershell
semgrep scan --config "p/owasp-top-ten" --exclude node_modules --exclude dist --exclude build --exclude .next --json -o src/semgrep/output/semgrep_results.json $env:SOURCE_ROOT
```

Kiểm tra output:

```powershell
dir src\semgrep\output
```

File quan trọng:

```text
src/semgrep/output/semgrep_results.json
```

Lưu ý khi quay video: PowerShell không dùng dấu `\` để xuống dòng như Git Bash. Nên dùng lệnh một dòng trên Windows để tránh Semgrep chạy sai hoặc load rules lâu bất thường.

Lời dẫn gợi ý:

```text
Bây giờ em chạy Semgrep scan với ruleset `p/owasp-top-ten` theo yêu cầu của đề. Lệnh này quét thư mục `eshop-sut`, loại trừ các thư mục dependency và build output như `node_modules`, `dist`, `build`, `.next`.
Kết quả được xuất ra file JSON `semgrep_results.json`. Đây là evidence scan gốc, dùng làm input cho bước AI triage và đối chiếu sau này.
Một lưu ý quan trọng là trên PowerShell nên dùng lệnh một dòng. Nếu copy lệnh Bash có dấu backslash xuống dòng thì command có thể chạy sai.
```

## 7. Chạy Scan Mở Rộng Nếu Cần

Lệnh này dùng thêm ruleset theo công nghệ EShop và custom rules:

```powershell
semgrep scan --config "p/owasp-top-ten" --config "p/nodejs" --config "p/javascript" --config "p/react" --config "src/semgrep/rules/eshop-security.yml" --exclude node_modules --exclude dist --exclude build --exclude .next --json -o src/semgrep/output/semgrep_results_extended.json ./eshop-sut
```

Lệnh mở rộng không thay thế scan chính `p/owasp-top-ten`; nó dùng để phân tích sâu hơn và đối chiếu coverage.

Lời dẫn gợi ý:

```text
Ngoài scan chính theo OWASP Top 10, nhóm có thể chạy thêm scan mở rộng với các ruleset Node.js, JavaScript, React và custom rule của EShop.
Phần này không thay thế kết quả chính, mà dùng để phân tích thêm coverage và các trường hợp ruleset mặc định có thể bỏ sót.
Trong video nếu cần ngắn gọn, em có thể chỉ giới thiệu lệnh này và không chạy lại.
```

## 8. Cấu Hình AI Triage

Copy file env mẫu:

```powershell
copy src\semgrep\.env.example src\semgrep\.env
notepad src\semgrep\.env
```

Ví dụ cấu hình OpenRouter:

```env
AI_PROVIDER=openai-compatible
AI_MODEL=google/gemini-2.5-flash-lite
AI_MAX_TOKENS=1800
OPENROUTER_API_KEY=sk-or-v1-...
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
```

Không commit file `.env` thật vì có API key. `AI_MAX_TOKENS` dùng để giới hạn độ dài output AI, giảm rủi ro lỗi credit/token.

Lời dẫn gợi ý:

```text
Sau khi có kết quả Semgrep JSON, em cấu hình AI provider để script triage có thể phân tích từng finding. File `.env.example` là mẫu, còn `.env` thật sẽ chứa API key nên không được commit.
Trong demo này nhóm dùng provider OpenAI-compatible qua OpenRouter. Biến `AI_MAX_TOKENS` dùng để giới hạn độ dài câu trả lời, giúp tránh tốn token quá nhiều hoặc lỗi credit.
```

## 9. Chạy AI Triage

Nếu source nằm trong repo tại `./eshop-sut`:

```powershell
python src/semgrep/semgrep_ai_triage.py src/semgrep/output/semgrep_results.json --source-root eshop-sut --output-dir src/semgrep/output
```

Nếu source nằm ở path khác:

```powershell
python src/semgrep/semgrep_ai_triage.py src/semgrep/output/semgrep_results.json --source-root $env:SOURCE_ROOT --output-dir src/semgrep/output
```

Nếu chưa có API key hoặc chỉ muốn sinh skeleton report:

```powershell
python src/semgrep/semgrep_ai_triage.py src/semgrep/output/semgrep_results.json --source-root eshop-sut --output-dir src/semgrep/output --offline
```

Kiểm tra output:

```powershell
dir src\semgrep\output
dir src\semgrep\output\findings
```

Output chính:

```text
src/semgrep/output/semgrep_triage_report.md
src/semgrep/output/semgrep_test_cases.md
src/semgrep/output/findings/
```

Lời dẫn gợi ý:

```text
Bước này em chạy script `semgrep_ai_triage.py`. Script đọc file `semgrep_results.json`, lấy thêm source context từ `eshop-sut`, sau đó gửi từng finding cho AI phân tích.
Output chính gồm report tổng hợp `semgrep_triage_report.md`, danh sách test case `semgrep_test_cases.md`, và thư mục `findings` chứa prompt/output riêng cho từng finding.
Nếu chưa có API key, script vẫn có chế độ `--offline` để sinh skeleton report và prompt cho reviewer đọc thủ công.
```

## 10. Đọc Báo Cáo Triage

Mở `src/semgrep/output/semgrep_triage_report.md`.

Các phần cần chỉ ra trong video:

- `Tags lỗi`: Rule ID, Severity, CWE, OWASP, Likelihood, Impact, Confidence.
- `Thông tin finding`: file, dòng, trạng thái kiểm chứng.
- `Bằng chứng mã nguồn`: source evidence Semgrep tìm thấy.
- `Postman/PoC tự động`: method, URL, headers, payload mẫu, expected result.
- `Phân tích AI`: phân loại và lý do triage bằng tiếng Việt.

Giải thích ngắn:

```text
Semgrep là SAST nên không tự có request/response runtime.
Endpoint, header và payload trong report được suy luận từ source code.
Tester vẫn phải kiểm chứng lại bằng Postman hoặc runtime evidence.
```

Lời dẫn gợi ý:

```text
Ở report triage, mỗi finding không chỉ còn là rule, file và line nữa. Script đã format lại thành một entry dễ đọc hơn: có tags lỗi, bằng chứng mã nguồn, phần Postman/PoC tự động và phân tích AI.
Điểm quan trọng là Semgrep là SAST, nên nó không tự có request/response runtime. Method, endpoint, header và payload ở đây được suy luận từ source code, vì vậy tester vẫn phải kiểm chứng lại bằng Postman.
```

## 11. Đọc Test Case Postman

Mở `src/semgrep/output/semgrep_test_cases.md`.

Mỗi test case có format:

```markdown
## TC-SEMGREP-001

- Finding liên quan: SEMGREP-001
- Mục tiêu test: ...

### Input

Request, headers và payload.

### Thao tác

Gửi request và ghi nhận status code, response body.

### Kết quả cần ghi nhận

Nếu còn lỗi và nếu đã an toàn.

### Trạng thái

Chưa kiểm chứng
```

Ví dụ payload mẫu được sinh từ source:

```json
{
  "email": "{{test_email}}",
  "password": "{{test_password}}"
}
```

Các biến `{{...}}` là biến Postman environment hoặc giá trị mẫu tester cần thay trước khi chạy PoC.

Lời dẫn gợi ý:

```text
File `semgrep_test_cases.md` là phần dùng trực tiếp cho demo Postman. Mỗi finding được chuyển thành một test case riêng, có method, URL, headers, payload mẫu, thao tác test và kết quả cần ghi nhận.
Payload mẫu không phải dữ liệu thật cố định. Nó được sinh từ source code, ví dụ từ `body: JSON.stringify({ email, password })`, sau đó tester thay các biến mẫu bằng dữ liệu test thật.
```

## 12. Chạy EShop Backend

Mở terminal riêng:

```powershell
cd eshop-sut\backend
npm install
node server.js
```

Kiểm tra backend:

```powershell
curl http://localhost:3000/api/products
```

Nếu API trả dữ liệu sản phẩm, backend đã sẵn sàng để test Postman/PoC.

Lời dẫn gợi ý:

```text
Để kiểm chứng PoC, em cần chạy backend EShop thật ở port 3000. Sau khi chạy `node server.js`, em gọi thử `/api/products` để xác nhận backend đã sẵn sàng.
Từ đây các test case trong `semgrep_test_cases.md` có thể được chạy bằng Postman.
```

## 13. Chọn 3 PoC Từ File Test Case

Trong video, lấy trực tiếp PoC từ `src/semgrep/output/semgrep_test_cases.md` để chứng minh test case được sinh ra sau AI triage có thể dùng ngay trong Postman.

Nên chọn 3 case sau:

| PoC   | Test case        | Lý do chọn                                                                 |
| ----- | ---------------- | -------------------------------------------------------------------------- |
| PoC 1 | `TC-SEMGREP-001` | Kiểm chứng hardcoded JWT secret bằng forged token.                         |
| PoC 2 | `TC-SEMGREP-005` | Kiểm chứng login request đi qua HTTP và có payload mẫu`email/password`.    |
| PoC 3 | `TC-SEMGREP-006` | Kiểm chứng register request đi qua HTTP và có payload mẫu nhiều field hơn. |

Khi quay, mở `semgrep_test_cases.md`, chỉ rõ mỗi PoC đều có đủ:

- Method và URL.
- Headers.
- Payload hoặc ghi chú không có request body.
- Thao tác kiểm chứng.
- Kết quả cần ghi nhận.

Lời dẫn gợi ý:

```text
Trong phần PoC, em sẽ không tự nghĩ request mới mà lấy trực tiếp từ file test case được sinh ra. Như vậy demo chứng minh được output của pipeline Semgrep có thể chuyển thành test case Postman.
Em chọn 3 case: một case JWT secret để kiểm chứng khả năng khai thác, một case login HTTP có payload email/password, và một case register HTTP có payload nhiều field hơn.
```

## 14. PoC 1: Hardcoded JWT Secret

Nguồn trong test case:

```text
TC-SEMGREP-001
```

Semgrep finding:

```text
javascript.jsonwebtoken.security.jwt-hardcode.hardcoded-jwt-secret
```

Chạy script tạo forged token:

```powershell
cd src\semgrep
npm install jsonwebtoken
node exploit.js
```

Copy chuỗi:

```text
Bearer <forged_admin_jwt>
```

Trong Postman, tạo request:

```http
GET http://localhost:3000/api/users/me
```

Headers:

```http
Authorization: Bearer <forged_admin_jwt>
Content-Type: application/json
```

Payload:

```text
Không có request body.
```

Kết quả cần ghi nhận:

- Nếu server trả `200 OK` và chấp nhận token giả: finding được xác nhận runtime.
- Nếu server trả `401 Unauthorized` hoặc `403 Forbidden`: không tái lập được hoặc đã được chặn ở runtime.

Lời dẫn gợi ý:

```text
PoC đầu tiên là hardcoded JWT secret. Semgrep phát hiện secret trong source code, còn Postman dùng để kiểm tra backend có thật sự chấp nhận token giả hay không.
Em chạy `exploit.js` để tạo JWT giả bằng secret bị lộ, copy token vào header Authorization, sau đó gọi `/api/users/me`.
Nếu server trả 200 thì finding được xác nhận ở runtime. Nếu server trả 401 hoặc 403 thì cần ghi là không tái lập được hoặc đã được chặn.
```

## 15. PoC 2: Login Request Dùng HTTP

Nguồn trong test case:

```text
TC-SEMGREP-005
```

Tạo request:

```http
POST http://localhost:3000/api/login
```

Headers:

```http
Content-Type: application/json
```

Body:

```json
{
  "email": "admin@eshop.com",
  "password": "Admin123!"
}
```

Ghi nhận:

- Status code.
- Response body.
- JWT token nếu login thành công.
- Screenshot Postman để làm evidence.

Kết luận khi quay:

- Request dùng `http://localhost:3000`, đúng với finding cleartext HTTP.
- Nếu login thành công, ghi nhận response và token làm runtime evidence.
- Nếu login thất bại do credential, vẫn ghi nhận endpoint HTTP đã được gọi và kiểm tra lại tài khoản seed.

Lời dẫn gợi ý:

```text
PoC thứ hai lấy từ `TC-SEMGREP-005`. Finding này liên quan đến request HTTP không mã hóa trong frontend.
Report đã sinh sẵn method POST, URL `/api/login`, header Content-Type và payload email/password. Em thay biến mẫu bằng tài khoản seed `admin@eshop.com` và `Admin123!`, rồi gửi request bằng Postman.
Evidence cần ghi là request đang dùng `http://`, status code và response body.
```

## 16. PoC 3: Register Request Dùng HTTP

Nguồn trong test case:

```text
TC-SEMGREP-006
```

Tạo request:

```http
POST http://localhost:3000/api/register
```

Headers:

```http
Content-Type: application/json
```

Body mẫu từ test case:

```json
{
  "name": "Demo Semgrep User",
  "email": "demo.semgrep@example.com",
  "password": "Demo123!"
}
```

Ý nghĩa kiểm chứng:

- Payload `name/email/password` được sinh từ `body: JSON.stringify(...)` trong source.
- Request vẫn đi qua `http://localhost:3000`, đúng với finding cleartext HTTP.
- Nếu backend trả tạo tài khoản thành công hoặc báo email đã tồn tại, vẫn ghi nhận được evidence runtime của endpoint.

Kết luận cần ghi theo môi trường:

- Lab/local HTTP: finding hợp lệ về pattern, impact phụ thuộc môi trường.
- Production vẫn dùng HTTP: xác nhận rủi ro truyền dữ liệu không mã hóa.

Lời dẫn gợi ý:

```text
PoC thứ ba lấy từ `TC-SEMGREP-006`, là request register. Case này giúp chứng minh payload mẫu không chỉ có email/password mà có thể tự sinh nhiều field như name, email và password.
Em gửi request register qua `http://localhost:3000/api/register`. Nếu tạo tài khoản thành công hoặc backend báo email đã tồn tại, điều quan trọng vẫn là có runtime evidence rằng endpoint đang được gọi qua HTTP.
Khi kết luận, cần nói rõ đây là môi trường lab/local. Nếu production vẫn dùng HTTP thì impact cao hơn; còn ở lab thì finding hợp lệ về pattern nhưng cần ghi chú theo môi trường.
```

## 17. Kết Luận Demo

Tóm tắt lại flow đã demo:

1. Semgrep quét source code EShop.
2. Kết quả scan được lưu vào `semgrep_results.json`.
3. Script AI triage đọc JSON và source context để sinh report Markdown.
4. Report triage giúp đọc finding theo format rõ ràng hơn.
5. `semgrep_test_cases.md` chuyển finding thành test case Postman.
6. Tester chạy PoC và ghi nhận status code, response body, screenshot.

Kết luận demo:

```text
Semgrep giúp phát hiện sớm dấu hiệu lỗi bảo mật trong source code.
AI triage giúp chuẩn hóa finding thành report tiếng Việt và test case dễ kiểm chứng.
Postman/PoC là bước xác nhận runtime để xem finding có tái hiện được trong môi trường chạy thật hay không.
Kết luận cuối cùng vẫn cần tester kiểm chứng thủ công dựa trên source evidence và kết quả PoC.
```

Lời dẫn gợi ý:

```text
Như vậy em đã hoàn tất flow Semgrep từ cài đặt đến kiểm chứng PoC. Điểm chính của flow là Semgrep phát hiện dấu hiệu lỗi từ source code, AI triage giúp format và giải thích finding, còn Postman dùng để kiểm chứng lại bằng request runtime.
Với mỗi finding, nhóm không kết luận chỉ dựa trên AI mà cần ghi nhận evidence thực tế như status code, response body và screenshot Postman.
```

## 18. Checklist Khi Kết Thúc Video

- Đã show `semgrep --version`.
- Đã show lệnh scan và file `semgrep_results.json`.
- Đã chạy AI triage hoặc offline triage.
- Đã mở `semgrep_triage_report.md`.
- Đã mở `semgrep_test_cases.md`.
- Đã chạy backend EShop.
- Đã test `TC-SEMGREP-001` bằng forged JWT.
- Đã test `TC-SEMGREP-005` bằng login request.
- Đã test `TC-SEMGREP-006` bằng register request.
- Đã kết luận flow Semgrep, AI triage và Postman/PoC.
