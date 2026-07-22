# Báo cáo ZAP AI Triage

## Tổng quan

- Tổng số alert instance trong input: 154
- Tổng số alert sau khi gom nhóm: 14
- Source JSON: `backend_basic.json`, `frontend_admin_basic.json`, `frontend_user_basic.json`
- Scan target/site: `http://localhost:3000`, `http://localhost:5173`, `http://localhost:5174`
- Script đọc `site[].alerts[].instances[]` từ JSON ZAP, không hardcode số lượng alert.
- ZAP là DAST nên evidence chính là request/response runtime, không phải dòng code.
- Phân loại của AI là hỗ trợ triage; kết luận cuối cùng vẫn cần tester kiểm chứng.

## Bảng tổng hợp alerts

| # | Alert | Endpoints | Risk | Confidence | CWE | WASC | Phân loại AI | Kết quả AI | Trạng thái kiểm chứng thủ công |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `CSP: Failure to Define Directive with No Fallback` | 15 | Medium | High | CWE-693 | WASC-15 | True Positive | `alerts/001_csp-failure-to-define-directive-with-no-fallback_ai_output.md` | Chưa kiểm chứng |
| 2 | `Cross-Domain Misconfiguration` | 12 | Medium | Medium | CWE-264 | WASC-14 | True Positive | `alerts/002_cross-domain-misconfiguration_ai_output.md` | Chưa kiểm chứng |
| 3 | `Server Leaks Information via "X-Powered-By" HTTP Response Header Field(s)` | 15 | Low | Medium | CWE-497 | WASC-13 | True Positive | `alerts/003_server-leaks-information-via-x-powered-by-http-response-header-field-s_ai_output.md` | Chưa kiểm chứng |
| 4 | `X-Content-Type-Options Header Missing` | 27 | Low | Medium | CWE-693 | WASC-15 | True Positive | `alerts/004_x-content-type-options-header-missing_ai_output.md` | Chưa kiểm chứng |
| 5 | `Authentication Request Identified` | 3 | Informational | High | N/A | N/A | Needs Human Review | `alerts/005_authentication-request-identified_ai_output.md` | Chưa kiểm chứng |
| 6 | `Session Management Response Identified` | 6 | Informational | Medium | N/A | N/A | Needs Human Review | `alerts/006_session-management-response-identified_ai_output.md` | Chưa kiểm chứng |
| 7 | `User Agent Fuzzer` | 9 | Informational | Medium | N/A | N/A | Needs Human Review | `alerts/007_user-agent-fuzzer_ai_output.md` | Chưa kiểm chứng |
| 8 | `Path Traversal` | 3 | High | Low | CWE-22 | WASC-33 | Needs Human Review | `alerts/008_path-traversal_ai_output.md` | Chưa kiểm chứng |
| 9 | `Content Security Policy (CSP) Header Not Set` | 14 | Medium | High | CWE-693 | WASC-15 | True Positive | `alerts/009_content-security-policy-csp-header-not-set_ai_output.md` | Chưa kiểm chứng |
| 10 | `Missing Anti-clickjacking Header` | 14 | Medium | Medium | CWE-1021 | WASC-15 | True Positive | `alerts/010_missing-anti-clickjacking-header_ai_output.md` | Chưa kiểm chứng |
| 11 | `Timestamp Disclosure - Unix` | 3 | Low | Low | CWE-497 | WASC-13 | Needs Human Review | `alerts/011_timestamp-disclosure-unix_ai_output.md` | Chưa kiểm chứng |
| 12 | `Information Disclosure - Sensitive Information in URL` | 3 | Informational | Medium | CWE-598 | WASC-13 | Needs Human Review | `alerts/012_information-disclosure-sensitive-information-in-url_ai_output.md` | Chưa kiểm chứng |
| 13 | `Information Disclosure - Suspicious Comments` | 16 | Informational | Medium | CWE-615 | WASC-13 | Needs Human Review | `alerts/013_information-disclosure-suspicious-comments_ai_output.md` | Chưa kiểm chứng |
| 14 | `Modern Web Application` | 14 | Informational | Medium | N/A | N/A | Needs Human Review | `alerts/014_modern-web-application_ai_output.md` | Chưa kiểm chứng |

## Chi tiết từng alert

### ZAP-001: CSP: Failure to Define Directive with No Fallback

#### Tags lỗi
| Thuộc tính | Giá trị |
|---|---|
| Plugin ID | `10055` |
| Alert Ref | `10055-13` |
| Risk | `Medium` |
| Confidence | `High` |
| CWE | CWE-693 |
| WASC | WASC-15 |
| Tags | OWASP_2021_A05, POLICY_QA_STD, POLICY_PENTEST, SYSTEMIC, CWE-693, OWASP_2017_A06, OWASP_2025_A02, POLICY_DEV_STD |
| Source JSON | `backend_basic.json`, `frontend_admin_basic.json`, `frontend_user_basic.json` |
| Site | `http://localhost:3000` |

#### Thông tin alert nhóm
- Số endpoint/request instance bị ảnh hưởng: 15
- Phân loại AI: True Positive
- Trạng thái kiểm chứng thủ công: Chưa kiểm chứng

#### Endpoints bị ảnh hưởng
| # | Method | URL | Param | Evidence |
|---|---|---|---|---|
| 1 | GET | `http://localhost:3000` | `Content-Security-Policy` | `default-src 'none'` |
| 2 | GET | `http://localhost:3000/` | `Content-Security-Policy` | `default-src 'none'` |
| 3 | GET | `http://localhost:3000/api` | `Content-Security-Policy` | `default-src 'none'` |
| 4 | GET | `http://localhost:3000/robots.txt` | `Content-Security-Policy` | `default-src 'none'` |
| 5 | GET | `http://localhost:3000/sitemap.xml` | `Content-Security-Policy` | `default-src 'none'` |
| 52 | GET | `http://localhost:3000` | `Content-Security-Policy` | `default-src 'none'` |
| 53 | GET | `http://localhost:3000/` | `Content-Security-Policy` | `default-src 'none'` |
| 54 | GET | `http://localhost:3000/api` | `Content-Security-Policy` | `default-src 'none'` |
| 55 | GET | `http://localhost:3000/robots.txt` | `Content-Security-Policy` | `default-src 'none'` |
| 56 | GET | `http://localhost:3000/sitemap.xml` | `Content-Security-Policy` | `default-src 'none'` |
| 130 | GET | `http://localhost:3000` | `Content-Security-Policy` | `default-src 'none'` |
| 131 | GET | `http://localhost:3000/` | `Content-Security-Policy` | `default-src 'none'` |
| 132 | GET | `http://localhost:3000/api` | `Content-Security-Policy` | `default-src 'none'` |
| 133 | GET | `http://localhost:3000/robots.txt` | `Content-Security-Policy` | `default-src 'none'` |
| 134 | GET | `http://localhost:3000/sitemap.xml` | `Content-Security-Policy` | `default-src 'none'` |

#### Bằng chứng runtime đại diện

Request:
```http
GET http://localhost:3000 HTTP/1.1
host: localhost:3000
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36
pragma: no-cache
cache-control: no-cache
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDkwNzV9.mOzLCI5uoLpBGWGMZ2PY7Y00zv3jSMAC2u4oQUHcVhc
```

Request body:
```text
[Không có request body]
```

Response:
```http
HTTP/1.1 404 Not Found
X-Powered-By: Express
Access-Control-Allow-Origin: *
Content-Security-Policy: default-src 'none'
X-Content-Type-Options: nosniff
Content-Type: text/html; charset=utf-8
Content-Length: 139
Date: Wed, 22 Jul 2026 08:31:18 GMT
Connection: keep-alive
Keep-Alive: timeout=5
```

Response body excerpt:
```text
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Error</title>
</head>
<body>
<pre>Cannot GET /</pre>
</body>
</html>
```

#### Phân tích AI
##### 1. Phân loại  
**True Positive**

##### 2. Lý do phân loại dựa trên runtime evidence của cả nhóm endpoint  
- Tất cả 15 endpoint/quá trình response quan sát được đều trả về header `Content-Security-Policy` với giá trị duy nhất là `default-src 'none'`.  
- Theo CSP spec, directive `default-src` là directive fallback dùng để áp dụng cho các directive khác nếu chúng không được khai báo riêng lẻ. Tuy nhiên, cảnh báo từ ZAP chỉ ra rằng CSP hiện tại "fails to define directive with no fallback", nghĩa là một hoặc một số directive bắt buộc hoặc không có fallback (như `script-src`, `style-src`, `img-src`...) không được định nghĩa trong policy, dẫn đến việc trình duyệt có thể bỏ qua hoặc thực thi policy không đúng như mong đợi.  
- Ở đây, chỉ mỗi `default-src 'none'` được set, nhưng đoạn thông báo cảnh báo CSP còn thiếu các directive cụ thể cần thiết, có thể gây hiểu nhầm rằng policy không thực sự giới hạn một số tài nguyên như script hoặc style. Do đó, CSP thực tế không chặt chẽ như ý muốn, nguy cơ bypass policy giảm thiểu nguy cơ XSS bị gia tăng.  
- Ứng dụng trả về 404 cho các endpoint này, thể hiện các đường dẫn này không phục vụ nội dung hợp lệ. Tuy nhiên CSP vẫn được set trên tất cả các response đó, cho thấy policy này được áp cho toàn bộ ứng dụng hoặc server.  
- Kết luận: đây là một vấn đề hệ thống liên quan cách cấu hình CSP không đầy đủ, ảnh hưởng rộng cho toàn bộ ứng dụng chứ không riêng endpoint nào.

##### 3. Tác động thực tế trong bối cảnh EShop  
- CSP yếu/kém có thể tăng khả năng xảy ra các cuộc tấn công XSS (Cross-Site Scripting), đặc biệt trong các phần UI có tương tác người dùng hoặc tải các nội dung bên ngoài (script, style, hình ảnh).  
- Do CSP hiện tại chỉ đặt `default-src 'none'` mà không định nghĩa rõ ràng `script-src`, `style-src`, ... nên khi trình duyệt không hỗ trợ đầy đủ hoặc hiểu sai policy, có thể coi như không có hạn chế nào cho các nguồn tài nguyên này.  
- Ứng dụng EShop có thể bị lợi dụng qua kỹ thuật injection script hoặc tải tài nguyên nguy hiểm từ nguồn không đáng tin cậy, dẫn đến lộ dữ liệu người dùng, chiếm quyền session, hoặc thực thi mã độc.  
- Đây là điểm yếu bảo mật tương đối trung bình (Medium risk), đặc biệt trong trường hợp ứng dụng có thành phần front-end phức tạp.  
- Nếu trong bối cảnh này các endpoint trả 404 không phục vụ dữ liệu người dùng hay tài nguyên quan trọng, thì tác động trực tiếp trên các endpoint đó thấp, nhưng CSP áp chung cho toàn hệ thống có thể vẫn chưa đủ chặt chẽ.  
- Cần đánh giá thêm mức độ nội dung thực tế được phục vụ ở các endpoint khác không trong danh sách, nhất là các trang UI quan trọng.

##### 4. Cách khắc phục cụ thể ở cấp cấu hình/root cause  
- Cấu hình lại header `Content-Security-Policy` tại server hoặc bất cứ thành phần middleware nào:  
  - Định nghĩa đầy đủ các directive quan trọng như `script-src`, `style-src`, `img-src`, `connect-src` với các nguồn tin cậy rõ ràng.  
  - Tránh dùng chỉ duy nhất `default-src 'none'` mà không có các directive fallback khác hoặc bổ sung.  
  - Ví dụ:  
    ```http
    Content-Security-Policy: default-src 'none'; script-src 'self' cdn.trusted.com; style-src 'self'; img-src 'self' data:;
    ```  
  - Điều này đảm bảo CSP được trình duyệt áp dụng chính xác, hạn chế tài nguyên tải từ nguồn không tin cậy.  
- Kiểm tra và cập nhật CSP phù hợp cho từng môi trường (dev, staging, production).  
- Nếu có các endpoint trả lỗi 404 hoặc tĩnh (robots.txt, sitemap.xml) có thể không cần thiết lập CSP quá phức tạp, nhưng nên đồng nhất policy chung tránh sai lệch.  
- Thực hiện test lại CSP sau thay đổi bằng tools hỗ trợ hoặc trình duyệt để đảm bảo chính sách được áp dụng đúng.

##### 5. Ghi chú tester cần kiểm tra thêm nếu chưa đủ context  
- Xác nhận môi trường chạy thử hiện tại là môi trường development hay production để đánh giá mức độ nghiêm trọng thực tế. Ở localhost, policy thường có thể chưa hoàn chỉnh.  
- Kiểm tra các trang/endpoint khác có phục vụ nội dung người dùng hoặc UI tương tác để xác định CSP hiện tại có áp dụng cho chúng không, có đủ chặt chẽ hay không.  
- Kiểm định kỹ các directive CSP mà ứng dụng backend hoặc frontend có thể đang thiếu (như script-src, style-src, connect-src...) trong các phản hồi chính thức (200 OK).  
- Kiểm tra liệu có bất cứ CSP header thừa/nghịch lý (như `unsafe-inline`, `unsafe-eval`) nào được set trên các response khác ảnh hưởng đến an toàn toàn hệ thống.  
- Phối hợp với dev để cập nhật chính sách CSP chuẩn kinh nghiệm theo OWASP CSP recommendations cho từng thành phần frontend/backend ứng dụng.  
- Kiểm tra tương thích CSP trên các trình duyệt dùng phổ biến trong môi trường người dùng EShop.

---

**Tóm lại:** alert này là True Positive cho vấn đề cấu hình CSP chưa đầy đủ, cần bổ sung các directive cần thiết để chính sách bảo mật hiệu quả, giảm thiểu nguy cơ khai thác qua XSS cho toàn hệ thống EShop.

### ZAP-002: Cross-Domain Misconfiguration

#### Tags lỗi
| Thuộc tính | Giá trị |
|---|---|
| Plugin ID | `10098` |
| Alert Ref | `10098` |
| Risk | `Medium` |
| Confidence | `Medium` |
| CWE | CWE-264 |
| WASC | WASC-14 |
| Tags | OWASP_2021_A01, POLICY_QA_STD, POLICY_PENTEST, SYSTEMIC, OWASP_2025_A01, OWASP_2017_A05, CWE-264 |
| Source JSON | `backend_basic.json`, `frontend_admin_basic.json`, `frontend_user_basic.json` |
| Site | `http://localhost:3000` |

#### Thông tin alert nhóm
- Số endpoint/request instance bị ảnh hưởng: 12
- Phân loại AI: True Positive
- Trạng thái kiểm chứng thủ công: Chưa kiểm chứng

#### Endpoints bị ảnh hưởng
| # | Method | URL | Param | Evidence |
|---|---|---|---|---|
| 6 | GET | `http://localhost:3000` | `N/A` | `Access-Control-Allow-Origin: *` |
| 7 | GET | `http://localhost:3000/` | `N/A` | `Access-Control-Allow-Origin: *` |
| 8 | GET | `http://localhost:3000/api/users/me` | `N/A` | `Access-Control-Allow-Origin: *` |
| 9 | GET | `http://localhost:3000/sitemap.xml` | `N/A` | `Access-Control-Allow-Origin: *` |
| 57 | GET | `http://localhost:3000` | `N/A` | `Access-Control-Allow-Origin: *` |
| 58 | GET | `http://localhost:3000/` | `N/A` | `Access-Control-Allow-Origin: *` |
| 59 | GET | `http://localhost:3000/api/users/me` | `N/A` | `Access-Control-Allow-Origin: *` |
| 60 | GET | `http://localhost:3000/sitemap.xml` | `N/A` | `Access-Control-Allow-Origin: *` |
| 135 | GET | `http://localhost:3000` | `N/A` | `Access-Control-Allow-Origin: *` |
| 136 | GET | `http://localhost:3000/` | `N/A` | `Access-Control-Allow-Origin: *` |
| 137 | GET | `http://localhost:3000/api/users/me` | `N/A` | `Access-Control-Allow-Origin: *` |
| 138 | GET | `http://localhost:3000/sitemap.xml` | `N/A` | `Access-Control-Allow-Origin: *` |

#### Bằng chứng runtime đại diện

Request:
```http
GET http://localhost:3000 HTTP/1.1
host: localhost:3000
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36
pragma: no-cache
cache-control: no-cache
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDkwNzV9.mOzLCI5uoLpBGWGMZ2PY7Y00zv3jSMAC2u4oQUHcVhc
```

Request body:
```text
[Không có request body]
```

Response:
```http
HTTP/1.1 404 Not Found
X-Powered-By: Express
Access-Control-Allow-Origin: *
Content-Security-Policy: default-src 'none'
X-Content-Type-Options: nosniff
Content-Type: text/html; charset=utf-8
Content-Length: 139
Date: Wed, 22 Jul 2026 08:31:18 GMT
Connection: keep-alive
Keep-Alive: timeout=5
```

Response body excerpt:
```text
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Error</title>
</head>
<body>
<pre>Cannot GET /</pre>
</body>
</html>
```

#### Phân tích AI
##### Triage Alert ZAP-002: Cross-Domain Misconfiguration (Plugin ID 10098)

##### 1. Phân loại  
**True Positive**

##### 2. Lý do phân loại dựa trên runtime evidence của cả nhóm endpoint  
- Tất cả 12 endpoint được quét đều trả về header `Access-Control-Allow-Origin: *` bất kể endpoint trả về 200 OK hay 404 Not Found.  
- Header CORS này cho phép mọi domain có thể thực hiện các request từ trình duyệt đến API/frontend backend của ứng dụng mà không bị chặn bởi chính sách Same Origin Policy (SOP).  
- Endpoint `/api/users/me` trả về dữ liệu nhạy cảm (thông tin người dùng, bao gồm email, role, thậm chí password dạng chuỗi thường), và vẫn cho phép `Access-Control-Allow-Origin: *`.  
- Việc này hoàn toàn vi phạm nguyên tắc bảo mật về CORS, tạo điều kiện cho các trang web xấu sử dụng JavaScript thực hiện các request lấy dữ liệu người dùng với token hiện tại (Authorization header được gửi theo), dẫn đến rò rỉ dữ liệu.  
- Khả năng giả mạo, đánh cắp dữ liệu người dùng từ nguồn khác (cross-site scripting + CORS) là hiện hữu.  
- Môi trường localhost nhưng behavior này nếu deploy tương tự trên môi trường production thì rất đáng lo ngại.  

##### 3. Tác động thực tế trong bối cảnh EShop  
- Có thể dẫn đến lộ thông tin nhạy cảm của người dùng (như tên, email, role, thậm chí mật khẩu ở dạng text—dấu hiệu cấu hình backend không tốt vì trả pass thẳng ra API).  
- Kẻ tấn công đặt trang web có payload độc hại, dụ người dùng có token đang login truy cập. JavaScript trên trang đó sẽ "tự do" lấy dữ liệu từ API do header CORS cho phép, gây rò rỉ thông tin cá nhân/nhạy cảm.  
- Ảnh hưởng đến bảo mật người dùng, gây ảnh hưởng uy tín hệ thống, tăng khả năng tấn công tiếp theo (phishing, chiếm quyền,...).  
- Với các endpoint trả 404 (Không tìm thấy), tuy có CORS mở nhưng không gây rủi ro trực tiếp. Nhưng nhìn chung vẫn thể hiện cấu hình lỏng lẻo, không phân quyền chặt chẽ.  

##### 4. Cách khắc phục cụ thể ở cấp cấu hình/root cause  
- **Hạn chế lại giá trị header `Access-Control-Allow-Origin`**:   
  - Không dùng dấu `*`. Chỉ cho phép những origin tin cậy, ví dụ domain frontend chính thức (`https://admin.eshop.com`, `https://www.eshop.com`, hoặc các domain cần thiết).  
  - Có thể dùng dynamic whitelist để phục vụ nhiều origin tùy theo môi trường.  
- **Không gửi header CORS** trên các endpoint không cần thiết hoặc trả 404, để tránh cung cấp kênh Cross-Domain không cần thiết.  
- **Xác thực và phân quyền kỹ càng** cho từng endpoint, đặc biệt endpoint trả dữ liệu người dùng (ví dụ `GET /api/users/me`).  
- **Kiểm soát kỹ thông tin trả về**: tuyệt đối không trả mật khẩu (dù đã hash hay chưa) trong response API.  
- Kiểm tra lại middleware CORS trên backend, cấu hình lại phù hợp theo chính sách bảo mật của tổ chức, tránh cấu hình mở mặc định trong framework.  
- Có thể áp dụng thêm các header bảo mật khác (ví dụ `Access-Control-Allow-Credentials: true` khi dùng cookie, nhưng phải phối hợp với origin whitelist).  

##### 5. Ghi chú tester cần kiểm tra thêm nếu chưa đủ context  
- Xác nhận môi trường deploy có giống môi trường runtime được scan không (dev/local hay production). Trường hợp chỉ là localhost dev, vẫn đánh giá để cảnh báo cho production.  
- Kiểm thử xem có khả năng exploit qua trình duyệt hay không: giả lập trang web bên ngoài gọi API để kiểm tra phản hồi có bị lộ dữ liệu nhạy cảm hay không.  
- Kiểm tra header CORS trên các thành phần khác (API admin, các microservices phụ trợ) để đánh giá tổng quan phạm vi lỏng lẻo của cấu hình.  
- Trao đổi với developer để kiểm tra luồng xử lý Authorization header và kiểm soát dữ liệu nhạy cảm có đang bị lộ qua API như trường hợp mật khẩu trong response.  
- Đánh giá thêm về các header bảo mật khác (Content-Security-Policy, X-Frame-Options,...) để đảm bảo tổng thể an toàn ứng dụng.  
- Xác minh việc cấu hình CORS trong code là tĩnh hay động, có xác thực origin request không.  

---

**Tóm lại:** Alert này là **True Positive** với rủi ro trung bình đến nghiêm trọng (medium) do cấu hình CORS quá mở, đặc biệt là khi dữ liệu nhạy cảm trả về API được áp dụng cho cả origin `*`. Đây là lỗ hổng phổ biến nhưng rất cần được xử lý để bảo vệ dữ liệu và người dùng của EShop.

### ZAP-003: Server Leaks Information via "X-Powered-By" HTTP Response Header Field(s)

#### Tags lỗi
| Thuộc tính | Giá trị |
|---|---|
| Plugin ID | `10037` |
| Alert Ref | `10037` |
| Risk | `Low` |
| Confidence | `Medium` |
| CWE | CWE-497 |
| WASC | WASC-13 |
| Tags | OWASP_2021_A01, WSTG-v42-INFO-08, POLICY_QA_STD, POLICY_PENTEST, SYSTEMIC, OWASP_2017_A03, OWASP_2025_A01, CWE-497 |
| Source JSON | `backend_basic.json`, `frontend_admin_basic.json`, `frontend_user_basic.json` |
| Site | `http://localhost:3000` |

#### Thông tin alert nhóm
- Số endpoint/request instance bị ảnh hưởng: 15
- Phân loại AI: True Positive
- Trạng thái kiểm chứng thủ công: Chưa kiểm chứng

#### Endpoints bị ảnh hưởng
| # | Method | URL | Param | Evidence |
|---|---|---|---|---|
| 10 | GET | `http://localhost:3000` | `N/A` | `X-Powered-By: Express` |
| 11 | GET | `http://localhost:3000/` | `N/A` | `X-Powered-By: Express` |
| 12 | GET | `http://localhost:3000/api/users/me` | `N/A` | `X-Powered-By: Express` |
| 13 | GET | `http://localhost:3000/robots.txt` | `N/A` | `X-Powered-By: Express` |
| 14 | POST | `http://localhost:3000/api/login` | `N/A` | `X-Powered-By: Express` |
| 61 | GET | `http://localhost:3000` | `N/A` | `X-Powered-By: Express` |
| 62 | GET | `http://localhost:3000/` | `N/A` | `X-Powered-By: Express` |
| 63 | GET | `http://localhost:3000/api/users/me` | `N/A` | `X-Powered-By: Express` |
| 64 | GET | `http://localhost:3000/robots.txt` | `N/A` | `X-Powered-By: Express` |
| 65 | POST | `http://localhost:3000/api/login` | `N/A` | `X-Powered-By: Express` |
| 139 | GET | `http://localhost:3000` | `N/A` | `X-Powered-By: Express` |
| 140 | GET | `http://localhost:3000/` | `N/A` | `X-Powered-By: Express` |
| 141 | GET | `http://localhost:3000/api/users/me` | `N/A` | `X-Powered-By: Express` |
| 142 | GET | `http://localhost:3000/robots.txt` | `N/A` | `X-Powered-By: Express` |
| 143 | POST | `http://localhost:3000/api/login` | `N/A` | `X-Powered-By: Express` |

#### Bằng chứng runtime đại diện

Request:
```http
GET http://localhost:3000 HTTP/1.1
host: localhost:3000
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36
pragma: no-cache
cache-control: no-cache
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDkwNzV9.mOzLCI5uoLpBGWGMZ2PY7Y00zv3jSMAC2u4oQUHcVhc
```

Request body:
```text
[Không có request body]
```

Response:
```http
HTTP/1.1 404 Not Found
X-Powered-By: Express
Access-Control-Allow-Origin: *
Content-Security-Policy: default-src 'none'
X-Content-Type-Options: nosniff
Content-Type: text/html; charset=utf-8
Content-Length: 139
Date: Wed, 22 Jul 2026 08:31:18 GMT
Connection: keep-alive
Keep-Alive: timeout=5
```

Response body excerpt:
```text
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Error</title>
</head>
<body>
<pre>Cannot GET /</pre>
</body>
</html>
```

#### Phân tích AI
##### Đánh giá nhóm alert ZAP-003: Server Leaks Information via "X-Powered-By" HTTP Response Header Field(s)

---

##### 1. Phân loại  
**True Positive**

---

##### 2. Lý do phân loại dựa trên runtime evidence của cả nhóm endpoint  
- Tất cả 15 endpoint (bao gồm backend và frontend, user và admin) đều trả về HTTP response header có trường `X-Powered-By: Express`.  
- Đây là hành vi cấu hình server/framework mặc định chưa được tắt, trực tiếp tiết lộ rõ ràng tên framework backend đang sử dụng.  
- ZAP thu thập trực tiếp header qua HTTP response runtime, không phải suy đoán hay giả định.  
- Đã kiểm tra request có Authorization token, response vẫn leak header, chứng tỏ không được hạn chế theo context auth hay role.  
- Mức độ confidence: Medium (áp dụng cho cấu hình chung, không phải lỗi logic phức tạp).  
- Không phải trường hợp False Positive vì header thực sự xuất hiện trên mọi response, bao gồm cả response lỗi (404) và response thành công (200).  
- Không chỉ là informational đơn thuần vì dễ bị attacker dùng để fingerprint framework, từ đó xác định vector tấn công tiềm năng hoặc khai thác lỗ hổng known của Express phiên bản cụ thể.

---

##### 3. Tác động thực tế trong bối cảnh EShop  
- Rò rỉ thông tin framework backend (Express) giúp attacker:  
  - Hiểu được thành phần công nghệ sử dụng, định hướng tấn công được hiệu quả hơn.  
  - Có thể kiểm tra nhanh các lỗ hổng bảo mật đã biết, phiên bản framework, plugin đang dùng.  
  - Trong trường hợp EShop dùng phiên bản Express cũ, có lỗ hổng thì rất dễ bị khai thác.  

- Tuy mức độ risk được đánh giá là Low theo OWASP ZAP, nhưng đây là một vector thu thập thông tin cơ bản, thuộc phạm vi **reconnaissance phase** của attacker.  
- Nếu kết hợp với các lỗ hổng khác thì nguy cơ gia tăng.  
- Ở môi trường localhost/lab, vẫn đánh giá tồn tại vấn đề nhưng cần xác nhận môi trường production có giữ header này hay không.

---

##### 4. Cách khắc phục cụ thể ở cấp cấu hình/root cause  
- Tắt header `X-Powered-By` trên server Express bằng cách cấu hình trong source code hoặc config server:  
  - Với Express, thêm dòng sau trong code:  
    ```js
    app.disable('x-powered-by');
    ```  
  - Hoặc tương đương cấu hình cho các server/proxy (nginx, Apache, load balancer) nếu có pass header này.  
- Kiểm tra các middleware, framework hoặc plugin có thể tự động thêm `X-Powered-By` và tắt/bỏ header tương ứng.  
- Triển khai chính sách bảo mật header (security headers) để loại bỏ thông tin không cần thiết.  
- Thực hiện kiểm tra lại các môi trường phát triển, staging hoặc production để đồng bộ cấu hình.

---

##### 5. Ghi chú tester cần kiểm tra thêm nếu chưa đủ context  
- Xác nhận môi trường đang quét là dev/local hoặc staging hay production. Nếu production thì ưu tiên xử lý ngay.  
- Kiểm tra xem có proxy, load balancer hoặc CDN phía trước có thêm lại header này không (có thể ZAP chỉ thấy header do proxy add).  
- Xem xét phiên bản Express đang sử dụng có liên quan tới các lỗ hổng đã biết nào không để đánh giá tác động bảo mật tổng thể.  
- Nếu có policy bảo mật nội bộ hay yêu cầu compliance, cần đối chiếu với chính sách đó về việc leak header.  
- Tham khảo thêm log server để chắc chắn không có các header tương tự phát sinh khi có các loại request khác (PUT, DELETE...).  
- Đánh giá kết hợp với các alert bảo mật khác từ ZAP để đưa ra mức độ ưu tiên xử lý tổng thể.

---

**Kết luận**: Đây là alert dạng True Positive, nên ưu tiên xử lý bằng cách tắt header `X-Powered-By` trên Express ngay để giảm việc rò rỉ thông tin framework backend, ngăn chặn attacker thu thập dữ liệu dùng để định hướng tấn công.

### ZAP-004: X-Content-Type-Options Header Missing

#### Tags lỗi
| Thuộc tính | Giá trị |
|---|---|
| Plugin ID | `10021` |
| Alert Ref | `10021` |
| Risk | `Low` |
| Confidence | `Medium` |
| CWE | CWE-693 |
| WASC | WASC-15 |
| Tags | OWASP_2021_A05, POLICY_QA_STD, POLICY_PENTEST, SYSTEMIC, CWE-693, OWASP_2017_A06, OWASP_2025_A02 |
| Source JSON | `backend_basic.json`, `frontend_admin_basic.json`, `frontend_user_basic.json` |
| Site | `http://localhost:3000`, `http://localhost:5173`, `http://localhost:5174` |

#### Thông tin alert nhóm
- Số endpoint/request instance bị ảnh hưởng: 27
- Phân loại AI: True Positive
- Trạng thái kiểm chứng thủ công: Chưa kiểm chứng

#### Endpoints bị ảnh hưởng
| # | Method | URL | Param | Evidence |
|---|---|---|---|---|
| 15 | GET | `http://localhost:3000/api/users/me` | `x-content-type-options` | `N/A` |
| 16 | POST | `http://localhost:3000/api/login` | `x-content-type-options` | `N/A` |
| 35 | GET | `http://localhost:5173` | `x-content-type-options` | `N/A` |
| 36 | GET | `http://localhost:5173/` | `x-content-type-options` | `N/A` |
| 37 | GET | `http://localhost:5173/favicon.svg` | `x-content-type-options` | `N/A` |
| 38 | GET | `http://localhost:5173/robots.txt` | `x-content-type-options` | `N/A` |
| 39 | GET | `http://localhost:5173/sitemap.xml` | `x-content-type-options` | `N/A` |
| 66 | GET | `http://localhost:3000/api/products?search=` | `x-content-type-options` | `N/A` |
| 67 | GET | `http://localhost:3000/api/products/1` | `x-content-type-options` | `N/A` |
| 68 | GET | `http://localhost:3000/api/products/2` | `x-content-type-options` | `N/A` |
| 69 | GET | `http://localhost:3000/api/users/me` | `x-content-type-options` | `N/A` |
| 70 | POST | `http://localhost:3000/api/login` | `x-content-type-options` | `N/A` |
| 87 | GET | `http://localhost:5174` | `x-content-type-options` | `N/A` |
| 88 | GET | `http://localhost:5174/` | `x-content-type-options` | `N/A` |
| 89 | GET | `http://localhost:5174/robots.txt` | `x-content-type-options` | `N/A` |
| 90 | GET | `http://localhost:5174/sitemap.xml` | `x-content-type-options` | `N/A` |
| 91 | GET | `http://localhost:5174/src/main.jsx` | `x-content-type-options` | `N/A` |
| 113 | GET | `http://localhost:5173` | `x-content-type-options` | `N/A` |
| 114 | GET | `http://localhost:5173/` | `x-content-type-options` | `N/A` |
| 115 | GET | `http://localhost:5173/favicon.svg` | `x-content-type-options` | `N/A` |
| 116 | GET | `http://localhost:5173/robots.txt` | `x-content-type-options` | `N/A` |
| 117 | GET | `http://localhost:5173/sitemap.xml` | `x-content-type-options` | `N/A` |
| 144 | GET | `http://localhost:3000/api/products?search=` | `x-content-type-options` | `N/A` |
| 145 | GET | `http://localhost:3000/api/products/1` | `x-content-type-options` | `N/A` |
| 146 | GET | `http://localhost:3000/api/products/2` | `x-content-type-options` | `N/A` |
| 147 | GET | `http://localhost:3000/api/users/me` | `x-content-type-options` | `N/A` |
| 148 | POST | `http://localhost:3000/api/login` | `x-content-type-options` | `N/A` |

#### Bằng chứng runtime đại diện

Request:
```http
GET http://localhost:3000/api/users/me HTTP/1.1
host: localhost:3000
User-Agent: Python-urllib/3.14
Connection: close
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDkwNzV9.mOzLCI5uoLpBGWGMZ2PY7Y00zv3jSMAC2u4oQUHcVhc
```

Request body:
```text
[Không có request body]
```

Response:
```http
HTTP/1.1 200 OK
X-Powered-By: Express
Access-Control-Allow-Origin: *
Content-Type: application/json; charset=utf-8
Content-Length: 184
ETag: W/"b8-jiz57PnCcXs0o7g11CVR0uf+SKE"
Date: Wed, 22 Jul 2026 08:31:15 GMT
Connection: close
```

Response body excerpt:
```text
{"id":2,"name":"Test User","email":"test@eshop.com","password":"Test1234!","role":"user","login_attempts":0,"locked_until":null,"reset_token":null,"shipping_address":null,"phone":null}
```

#### Phân tích AI
##### Triage Alert OWASP ZAP - ZAP-004: X-Content-Type-Options Header Missing

---

##### 1. Phân loại  
**True Positive**

---

##### 2. Lý do phân loại dựa trên runtime evidence của cả nhóm endpoint  
- Qua quan sát các response ở đa số các endpoint (backend, frontend user, frontend admin), header `X-Content-Type-Options` không được thiết lập, hoặc thiếu hoàn toàn, theo như alert chỉ ra.  
- ZAP-004 là alert cảnh báo thiếu header bảo mật `X-Content-Type-Options: nosniff`, một header quan trọng để ngăn chặn trình duyệt thực hiện MIME-sniffing, tức là dựa vào nội dung thực tế của payload để đoán kiểu MIME, gây ra nguy cơ hiểu nhầm loại nội dung, dẫn đến một số khai thác cross-site scripting (XSS) hoặc tấn công chèn mã khác có thể xảy ra.  
- Header `Content-Type` được server trả về tương đối đầy đủ (ví dụ: `application/json; charset=utf-8`, `text/html`), nhưng thiếu `X-Content-Type-Options` là thiếu sót cấu hình bảo mật phổ biến.  
- Số lượng endpoint bị ảnh hưởng lớn (27 endpoints), trải khắp backend và frontend, là dấu hiệu của lỗi cấu hình mang tính hệ thống.  
- Không có bằng chứng _false positive_ hoặc ngoại lệ liên quan đến môi trường localhost kiểm tra.  
- Mức độ cảnh báo của ZAP là Low, confidence Medium phù hợp với mức độ và ảnh hưởng của header này.

---

##### 3. Tác động thực tế trong bối cảnh EShop  
- Tác động chính:  
  - Nếu thiếu header `X-Content-Type-Options: nosniff`, các trình duyệt cũ (IE, Chrome legacy) có thể thực hiện MIME-sniffing dẫn đến việc tải và thực thi tài nguyên theo kiểu không mong muốn (ví dụ: thực thi script từ file văn bản, hình ảnh).  
  - Điều này làm tăng nguy cơ khai thác XSS hoặc drive-by-download, đặc biệt trong điều kiện có kẽ hở khác hoặc payload phản hồi chứa nội dung có thể bị lợi dụng.  
  - Tuy nhiên, trong bối cảnh EShop:  
    - Phần lớn response đã trả đúng `Content-Type`.  
    - Mức độ rủi ro được đánh giá là thấp (Low) vì ứng dụng không để lộ payload có thể khai thác cao trong response và không là môi trường công khai có rủi ro mạng phức tạp cao.  
    - Tác động sẽ tăng nếu có các kẽ hở mã hóa XSS, injection, nhưng đây là vấn đề riêng biệt.  
- Do đó, đây là một điểm cấu hình bảo mật hệ thống cần được khắc phục để hoàn thiện, không phải lỗi critical nghiêm trọng ngay lập tức.

---

##### 4. Cách khắc phục cụ thể ở cấp cấu hình/root cause  
- Cấu hình server hoặc reverse proxy (ví dụ Nginx, Apache, Express middleware) thêm header HTTP:  
  ```
  X-Content-Type-Options: nosniff
  ```  
- Cụ thể:  
  - Với Express (Node.js), dùng middleware như `helmet` với dòng:  
    ```js
    app.use(helmet.noSniff());
    ```  
  - Với Nginx, thêm vào block `server` hoặc `location`:  
    ```
    add_header X-Content-Type-Options nosniff;
    ```  
  - Với Apache, thêm directive:  
    ```
    Header set X-Content-Type-Options "nosniff"
    ```  
- Đảm bảo header này được set cho tất cả các response trả về (API backend, frontend, static resources)  
- Kiểm tra lại cấu hình để header không bị ghi đè hoặc xóa bỏ bởi middleware khác.  

---

##### 5. Ghi chú tester cần kiểm tra thêm nếu chưa đủ context  
- Xác nhận môi trường triển khai thực tế (production hoặc staging) có cấu hình tương đồng với môi trường localhost được scan.  
- Kiểm tra log server hoặc cấu hình middleware để đảm bảo header thực sự chưa được set, tránh trường hợp header bị chặn bởi proxy hoặc công cụ scan không đọc đúng response.  
- Đánh giá lại các endpoint có trả payload dạng đặc biệt (vd: file download, HTML upload, dữ liệu được user upload) xem có nguy cơ khai thác cao hơn từ việc thiếu header này không.  
- Kiểm tra khả năng tương thích với các trình duyệt hiện tại khách hàng sử dụng (nếu chủ yếu dùng trình duyệt hiện đại, tác động có thể thấp hơn).  
- Đánh giá biện pháp bảo vệ bổ trợ khác như CSP, CORS để phối hợp với khắc phục này.

---

**Tóm lại:** đây là một vulnerability bảo mật cấu hình hệ thống với xác suất thực sự xảy ra rủi ro trên các rủi ro thứ cấp. Việc bổ sung header `X-Content-Type-Options: nosniff` cho tất cả response được khuyến cáo để tăng cường an toàn chống lại các tấn công dựa trên MIME sniffing.

### ZAP-005: Authentication Request Identified

#### Tags lỗi
| Thuộc tính | Giá trị |
|---|---|
| Plugin ID | `10111` |
| Alert Ref | `10111` |
| Risk | `Informational` |
| Confidence | `High` |
| CWE | N/A |
| WASC | N/A |
| Tags | N/A |
| Source JSON | `backend_basic.json`, `frontend_admin_basic.json`, `frontend_user_basic.json` |
| Site | `http://localhost:3000` |

#### Thông tin alert nhóm
- Số endpoint/request instance bị ảnh hưởng: 3
- Phân loại AI: Needs Human Review
- Trạng thái kiểm chứng thủ công: Chưa kiểm chứng

#### Endpoints bị ảnh hưởng
| # | Method | URL | Param | Evidence |
|---|---|---|---|---|
| 17 | POST | `http://localhost:3000/api/login` | `email` | `password` |
| 71 | POST | `http://localhost:3000/api/login` | `email` | `password` |
| 149 | POST | `http://localhost:3000/api/login` | `email` | `password` |

#### Bằng chứng runtime đại diện

Request:
```http
POST http://localhost:3000/api/login HTTP/1.1
Content-Length: 52
host: localhost:3000
User-Agent: Python-urllib/3.14
Content-Type: application/json
Connection: close
```

Request body:
```text
{"email": "test@eshop.com", "password": "Test1234!"}
```

Response:
```http
HTTP/1.1 200 OK
X-Powered-By: Express
Access-Control-Allow-Origin: *
Content-Type: application/json; charset=utf-8
Content-Length: 366
ETag: W/"16e-sNg9siE/HSfYKD9jdJXvPnui8jU"
Date: Wed, 22 Jul 2026 08:31:15 GMT
Connection: close
```

Response body excerpt:
```text
{"message":"Login successful","token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDkwNzV9.mOzLCI5uoLpBGWGMZ2PY7Y00zv3jSMAC2u4oQUHcVhc","user":{"id":2,"name":"Test User","email":"test@eshop.com","password":"Test1234!","role":"user","login_attempts":0,"locked_until":null,"reset_token":null,"shipping_address":null,"phone":null}}
```

#### Phân tích AI
##### 1. Phân loại  
Needs Human Review

##### 2. Lý do phân loại dựa trên runtime evidence của cả nhóm endpoint  
- Nhóm alert này đều phát hiện trên cùng một endpoint `/api/login` với method POST và payload chứa credential (`email`, `password`), thực hiện hành vi xác thực (authentication request).  
- Đây là một alert loại Informational, ZAP chỉ nhận biết đây là request xác thực mà không chỉ ra bất kỳ vấn đề bảo mật cụ thể nào trong request hoặc response.  
- Request/response runtime cho thấy endpoint hoạt động bình thường: trả về HTTP 200 OK và một token JWT hợp lệ.  
- Tuy nhiên, trong response body hiển thị **cleartext password** của user (`"password": "Test1234!"`), đây là dấu hiệu rò rỉ thông tin nhạy cảm nghiêm trọng.  
- ZAP không cảnh báo về việc lộ password hay issue bảo mật khác, chỉ phát hiện dạng Authentication Request.  
- Do đó, alert này tự nó không phải là lỗ hổng, nhưng response body chứa thông tin password không mã hóa/phải ẩn đi mới đúng. Việc này là dấu hiệu cần đánh giá thêm.  
- Vì vậy cần review thêm để đánh giá mức độ rò rỉ, phạm vi ảnh hưởng, và kiểm tra nguyên nhân tại source (API trả về password).

##### 3. Tác động thực tế trong bối cảnh EShop  
- Việc trả về rõ ràng password trong response là hành vi rất nguy hiểm, làm lộ credential người dùng nếu attacker bắt được traffic hoặc có thể từ các module frontend/admin truy cập API.  
- Gây mất an toàn dữ liệu cá nhân, tăng nguy cơ tấn công tiếp theo như đánh cắp tài khoản, đặc biệt với các token JWT dùng để xác thực phiên làm việc.  
- Trong môi trường localhost/lab, có thể chỉ là môi trường test, nhưng nếu deploy production mà vẫn giữ hành vi này thì rất nghiêm trọng, ảnh hưởng trực tiếp đến bảo mật tài khoản người dùng.

##### 4. Cách khắc phục cụ thể ở cấp cấu hình/root cause  
- Sửa backend API `/api/login` không trả về trường `password` trong response body, hoặc nếu cần thì chỉ trả về thông tin an toàn không nhạy cảm (id, role, email, name nhưng không có password).  
- Kiểm tra và kiểm soát luồng dữ liệu nhạy cảm đặc biệt với password, tuyệt đối không đưa password vào response cho client dưới mọi hình thức.  
- Đánh giá lại cấu trúc JWT và cách quản lý token để đảm bảo không dính thông tin mật hay không hợp lệ.  
- Tăng cường kiểm thử kiểm soát dữ liệu nhạy cảm trong API response ở vòng phát triển.

##### 5. Ghi chú tester cần kiểm tra thêm nếu chưa đủ context  
- Xác nhận môi trường deploy thực tế có giống với lab/local này không để đánh giá mức độ nghiêm trọng trong thực tế.  
- Kiểm tra toàn bộ các endpoint khác có lặp lại lỗi tương tự (trả về password hay dữ liệu nhạy cảm không cần thiết).  
- Đánh giá xem token JWT có chứa thông tin nhạy cảm hay khả năng bị khai thác cao không.  
- Cần rà soát chính sách logging, caching, và cách frontend sử dụng response liệu có làm lộ thông tin nhạy cảm ở client-side hay không.  
- Phối hợp với dev để truy vết root cause API trả password trong response và xây dựng testcase ngăn lỗi này tái diễn.

### ZAP-006: Session Management Response Identified

#### Tags lỗi
| Thuộc tính | Giá trị |
|---|---|
| Plugin ID | `10112` |
| Alert Ref | `10112` |
| Risk | `Informational` |
| Confidence | `Medium` |
| CWE | N/A |
| WASC | N/A |
| Tags | N/A |
| Source JSON | `backend_basic.json`, `frontend_admin_basic.json`, `frontend_user_basic.json` |
| Site | `http://localhost:3000` |

#### Thông tin alert nhóm
- Số endpoint/request instance bị ảnh hưởng: 6
- Phân loại AI: Needs Human Review
- Trạng thái kiểm chứng thủ công: Chưa kiểm chứng

#### Endpoints bị ảnh hưởng
| # | Method | URL | Param | Evidence |
|---|---|---|---|---|
| 18 | POST | `http://localhost:3000/api/login` | `token` | `token` |
| 19 | POST | `http://localhost:3000/api/login` | `token` | `token` |
| 72 | POST | `http://localhost:3000/api/login` | `token` | `token` |
| 73 | POST | `http://localhost:3000/api/login` | `token` | `token` |
| 150 | POST | `http://localhost:3000/api/login` | `token` | `token` |
| 151 | POST | `http://localhost:3000/api/login` | `token` | `token` |

#### Bằng chứng runtime đại diện

Request:
```http
POST http://localhost:3000/api/login HTTP/1.1
Content-Length: 52
host: localhost:3000
User-Agent: Python-urllib/3.14
Content-Type: application/json
Connection: close
```

Request body:
```text
{"email": "test@eshop.com", "password": "Test1234!"}
```

Response:
```http
HTTP/1.1 200 OK
X-Powered-By: Express
Access-Control-Allow-Origin: *
Content-Type: application/json; charset=utf-8
Content-Length: 366
ETag: W/"16e-sNg9siE/HSfYKD9jdJXvPnui8jU"
Date: Wed, 22 Jul 2026 08:31:15 GMT
Connection: close
```

Response body excerpt:
```text
{"message":"Login successful","token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDkwNzV9.mOzLCI5uoLpBGWGMZ2PY7Y00zv3jSMAC2u4oQUHcVhc","user":{"id":2,"name":"Test User","email":"test@eshop.com","password":"Test1234!","role":"user","login_attempts":0,"locked_until":null,"reset_token":null,"shipping_address":null,"phone":null}}
```

#### Phân tích AI
1. **Phân loại:** Needs Human Review

2. **Lý do phân loại dựa trên runtime evidence của cả nhóm endpoint:**
- Tất cả các alert đều liên quan đến endpoint `/api/login` trả về response chứa trường JSON `token` (JWT).
- ZAP phát hiện đây là dạng "Session Management Response Identified" dựa trên việc response trả về token được dùng để quản lý phiên người dùng.
- Đây là alert mang tính **informational**, không phải lỗi bảo mật trực tiếp mà chỉ cảnh báo phát hiện token phiên dạng Header Based hoặc trả về trong payload.
- Response header không cho thấy lỗi cấu hình bảo mật nghiêm trọng như thiếu Secure/HttpOnly cookie hoặc thông tin nhạy cảm bị rò rỉ qua header.
- Response body lộ một số dữ liệu nhạy cảm (như `password` trong user object) nhưng alert này không phản ánh vấn đề đó (đó là vấn đề khác).
- Do scanner dựa vào heuristic token, chưa có dấu hiệu cho thấy cấu hình session management trên server sai hoặc lỏng lẻo.
- Đây là môi trường localhost/lab, chưa xác định chính xác môi trường deploy thực tế để đánh giá rủi ro trong môi trường production.

3. **Tác động thực tế trong bối cảnh EShop:**
- Alert thể hiện rằng backend trả về token (JWT) trong response body, đây là cách phổ biến để thực hiện xác thực phiên (token-based auth).
- Việc ZAP nhận diện token có thể hỗ trợ cấu hình session management trong quá trình thử nghiệm.
- Tuy nhiên, response body lộ `password` người dùng rõ ràng là rủi ro nghiêm trọng, cần tách riêng alert/kiểm tra khác (không nằm trong phạm vi alert này).
- Nếu token JWT được giữ an toàn (https, không lưu trữ không an toàn), rủi ro từ alert này là thấp.
- Cần đánh giá thêm cách client lưu trữ và gửi token (ví dụ localStorage, cookie) để xác định rủi ro thực tế.

4. **Cách khắc phục cụ thể ở cấp cấu hình/root cause:**
- Do alert chỉ mang tính thông báo việc phát hiện token trong response, không cần fix theo alert này.
- Tuy nhiên, để tối ưu bảo mật session management:
  - Xem xét dùng cookie với cờ Secure, HttpOnly thay vì trả token trong body response nếu có thể.
  - Nếu dùng JWT trong body, nên bảo vệ kênh truyền (HTTPS bắt buộc).
  - Không đưa dữ liệu nhạy cảm (như `password`) trong response.
  - Kiểm tra và cấu hình chính xác session management method cho ZAP hoặc các công cụ khác (nếu dùng tự động).
- Tổng thể, alert này không yêu cầu fix nhưng là dấu hiệu cho thấy hệ thống dùng token-based session.

5. **Ghi chú tester cần kiểm tra thêm nếu chưa đủ context:**
- Xác nhận môi trường deployment (local hay production) để đánh giá mức độ ảnh hưởng.
- Kiểm tra thêm cách client nhận và lưu trữ token (localStorage hay cookie) để đánh giá khả năng rò rỉ token.
- Đánh giá chi tiết response body có chứa thông tin nhạy cảm không (như password), đây mới là rủi ro cần ưu tiên xử lý.
- Xác minh giao thức truyền thông có sử dụng HTTPS không để bảo đảm an toàn truyền token.
- Kiểm tra cấu hình session management trên server từ góc độ xác thực (authentication) và quản lý phiên (session) để có định hướng remediation cụ thể hơn.
- Có thể bổ sung tìm kiếm alert liên quan đến rò rỉ dữ liệu hoặc cấu hình bảo mật token/session để có cái nhìn tổng thể hơn.

### ZAP-007: User Agent Fuzzer

#### Tags lỗi
| Thuộc tính | Giá trị |
|---|---|
| Plugin ID | `10104` |
| Alert Ref | `10104` |
| Risk | `Informational` |
| Confidence | `Medium` |
| CWE | N/A |
| WASC | N/A |
| Tags | CUSTOM_PAYLOADS, POLICY_PENTEST, SYSTEMIC |
| Source JSON | `backend_basic.json`, `frontend_admin_basic.json`, `frontend_user_basic.json` |
| Site | `http://localhost:3000` |

#### Thông tin alert nhóm
- Số endpoint/request instance bị ảnh hưởng: 9
- Phân loại AI: Needs Human Review
- Trạng thái kiểm chứng thủ công: Chưa kiểm chứng

#### Endpoints bị ảnh hưởng
| # | Method | URL | Param | Evidence |
|---|---|---|---|---|
| 20 | GET | `http://localhost:3000/api/users/me` | `Header User-Agent` | `N/A` |
| 21 | GET | `http://localhost:3000/api/users/me` | `Header User-Agent` | `N/A` |
| 22 | POST | `http://localhost:3000/api/login` | `Header User-Agent` | `N/A` |
| 74 | GET | `http://localhost:3000/api/users/me` | `Header User-Agent` | `N/A` |
| 75 | GET | `http://localhost:3000/api/users/me` | `Header User-Agent` | `N/A` |
| 76 | POST | `http://localhost:3000/api/login` | `Header User-Agent` | `N/A` |
| 152 | GET | `http://localhost:3000/api/users/me` | `Header User-Agent` | `N/A` |
| 153 | GET | `http://localhost:3000/api/users/me` | `Header User-Agent` | `N/A` |
| 154 | POST | `http://localhost:3000/api/login` | `Header User-Agent` | `N/A` |

#### Bằng chứng runtime đại diện

Request:
```http
GET http://localhost:3000/api/users/me HTTP/1.1
host: localhost:3000
user-agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)
pragma: no-cache
cache-control: no-cache
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDkwNzV9.mOzLCI5uoLpBGWGMZ2PY7Y00zv3jSMAC2u4oQUHcVhc
```

Request body:
```text
[Không có request body]
```

Response:
```http
HTTP/1.1 200 OK
X-Powered-By: Express
Access-Control-Allow-Origin: *
Content-Type: application/json; charset=utf-8
Content-Length: 206
ETag: W/"ce-2wm+uxdWRy5jVdzR8SspSiM8oHk"
Date: Wed, 22 Jul 2026 08:32:14 GMT
Connection: keep-alive
Keep-Alive: timeout=5
```

Response body excerpt:
```text
{"id":2,"name":"Test User","email":"test@eshop.com","password":"Test1234!","role":"user","login_attempts":4,"locked_until":"2026-07-22T08:34:58.363Z","reset_token":null,"shipping_address":null,"phone":null}
```

#### Phân tích AI
##### Triage Alert OWASP ZAP-007: User Agent Fuzzer (Plugin ID: 10104)

---

##### 1. Phân loại  
**Needs Human Review**

---

##### 2. Lý do phân loại dựa trên runtime evidence của cả nhóm endpoint

- ZAP-007 kiểm tra sự khác biệt response khi thay đổi header User-Agent nhằm phát hiện các hành vi đặc biệt (ví dụ: trang mobile, bot crawler, phân quyền dựa trên UA...).  
- 9 endpoint trên đều phản hồi HTTP status và body tương đồng, không thay đổi logic, không trả về thông tin khác biệt hay lỗi ngoài ý muốn khi dùng payload fuzzed User-Agent.  
- Độ tin cậy confidence là Medium, mức risk chỉ **Informational**, không phát hiện yếu tố gây lỗi hay rò rỉ dữ liệu rõ ràng.  
- Phản hồi chứa dữ liệu user (có password hoặc reset_token...) nhưng không có thay đổi khác biệt khi fuzz User-Agent, chứng tỏ hệ thống không phân biệt hành vi dựa trên User-Agent.  
- Các endpoint nằm trên `localhost` (môi trường test/lab), cần xác nhận với môi trường deploy thực tế, vì tình huống này chỉ thể hiện là tín hiệu để kiểm tra thêm chứ chưa phải lỗ hổng bảo mật thực sự.  
- Do thiếu thông tin về cách backend xử lý nội dung header User-Agent (vd. có chặn bot, hay thay đổi UI, feature) và không quan sát được thay đổi lớn đáng kể nên cần con người đánh giá thêm.  

---

##### 3. Tác động thực tế trong bối cảnh EShop

- Không có dấu hiệu backend xử lý sai lệch hoặc rò rỉ dữ liệu nhạy cảm do User-Agent nên về cơ bản không thấy tác động bảo mật nghiêm trọng.  
- Dữ liệu user nhạy cảm (password, token) trả về trong API `/api/users/me` là điểm cần lưu ý riêng, nhưng không liên quan trực tiếp tới alert User Agent Fuzzer.  
- Có thể cảnh báo này giúp tester nhận biết backend phản hồi đồng nhất với các UA khác nhau, điều này tốt với mặt bảo mật (không phân biệt dựa trên UA gây bypass).  
- Nếu môi trường production có dùng User-Agent để điều hướng hoặc quản lý quyền truy cập đặc biệt, alert này có thể cần đánh giá thêm.

---

##### 4. Cách khắc phục cụ thể ở cấp cấu hình/root cause

- Nếu thử nghiệm thực tế không thấy hành vi phân biệt dựa trên User-Agent là cần thiết, có thể giữ nguyên.  
- Nếu có nhu cầu bảo vệ hệ thống khỏi các bot hoặc crawlers không mong muốn (ví dụ attack tự động), nên cấu hình tường lửa ứng dụng (WAF) hoặc backend xử lý chặt chẽ các header này.  
- Kiểm tra và loại bỏ/ẩn các dữ liệu nhạy cảm, đặc biệt là "password" hoặc "reset_token" trong response JSON nếu không cần thiết (đây là điểm khác biệt và quan trọng hơn alert này).  
- Định nghĩa lại các chính sách chấp nhận header User-Agent hoặc giới hạn kích thước, cấu hình rate limit theo user agent để tránh lạm dụng fuzz.  
- Đảm bảo log lại tất cả request có User-Agent bất thường nếu có mục đích theo dõi tấn công.  

---

##### 5. Ghi chú tester cần kiểm tra thêm nếu chưa đủ context

- Xác nhận môi trường deploy thực tế (production test) có phản hồi tương tự không, tránh đánh giá sai môi trường lab/local.  
- Kiểm tra chi tiết code backend có logic phân biệt nội dung/đáp ứng dựa vào User-Agent không, nhất là các module frontend hoặc API phân quyền.  
- Đánh giá lại mức độ nhạy cảm và xử lý dữ liệu "password" và các trường nhạy cảm trả về từ API, đảm bảo không lộ thông tin mật.  
- Xác nhận thêm với đội phát triển về chính sách xử lý các user agents khác (web crawlers, mobile, bots).  
- Kiểm tra các logs hoặc WAF để phát hiện các request User-Agent bất thường có thể liên quan đến tấn công thực tế.  
- Có thể cần bổ sung test case fuzz User-Agent với payload đa dạng hơn để phát hiện lỗi tiềm ẩn về handle HTTP header hoặc session.

---

**Tóm lại, alert User Agent Fuzzer lần này cung cấp tín hiệu informational hữu ích về cách backend phản hồi nhưng chưa đủ bằng chứng lỗi bảo mật thực sự (True Positive) hay không hiệu quả (False Positive). Cần người kiểm thử hoặc developer đánh giá sâu hơn để xác định giá trị và rủi ro thực tế trong bối cảnh ứng dụng EShop.**

### ZAP-008: Path Traversal

#### Tags lỗi
| Thuộc tính | Giá trị |
|---|---|
| Plugin ID | `6` |
| Alert Ref | `6-5` |
| Risk | `High` |
| Confidence | `Low` |
| CWE | CWE-22 |
| WASC | WASC-33 |
| Tags | OWASP_2021_A01, POLICY_SEQUENCE, CWE-22, PCI_DSS, OWASP_2025_A01, WSTG-v42-ATHZ-01, POLICY_DEV_FULL, POLICY_QA_STD, POLICY_QA_FULL, POLICY_PENTEST, HIPAA, OWASP_2017_A05, POLICY_DEV_STD |
| Source JSON | `frontend_admin_basic.json`, `frontend_user_basic.json` |
| Site | `http://localhost:5173`, `http://localhost:5174` |

#### Thông tin alert nhóm
- Số endpoint/request instance bị ảnh hưởng: 3
- Phân loại AI: Needs Human Review
- Trạng thái kiểm chứng thủ công: Chưa kiểm chứng

#### Endpoints bị ảnh hưởng
| # | Method | URL | Param | Evidence |
|---|---|---|---|---|
| 23 | GET | `http://localhost:5173/node_modules/.vite/deps/chunk-CYJPkc-J.js?v=%2Fchunk-CYJPkc-J.js` | `v` | `N/A` |
| 77 | GET | `http://localhost:5174/node_modules/.vite/deps/chunk-nbk3hphP.js?v=%2Fchunk-nbk3hphP.js` | `v` | `N/A` |
| 101 | GET | `http://localhost:5173/node_modules/.vite/deps/chunk-CYJPkc-J.js?v=%2Fchunk-CYJPkc-J.js` | `v` | `N/A` |

#### Bằng chứng runtime đại diện

Request:
```http
GET http://localhost:5173/node_modules/.vite/deps/chunk-CYJPkc-J.js?v=%2Fchunk-CYJPkc-J.js HTTP/1.1
host: localhost:5173
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Connection: keep-alive
Referer: http://localhost:5173/node_modules/.vite/deps/react.js?v=82fd3d9d
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDk1NzF9.6xPB8cUE63QhefuiiRzG56zhdFE5lbB-b7dUFPwWED0
```

Request body:
```text
[Không có request body]
```

Response:
```http
HTTP/1.1 200 OK
Vary: Origin
Content-Type: text/javascript
Cache-Control: max-age=31536000,immutable
Etag: W/"57f-BbpnINpWDE4VpHrFzxGXLPGUN6Q"
Date: Wed, 22 Jul 2026 08:41:49 GMT
Connection: keep-alive
Keep-Alive: timeout=5
Content-Length: 7630
```

Response body excerpt:
```text
//#region \0rolldown/runtime.js
var __create = Object.create;
var __defProp = Object.defineProperty;
var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
var __getOwnPropNames = Object.getOwnPropertyNames;
var __getProtoOf = Object.getPrototypeOf;
var __hasOwnProp = Object.prototype.hasOwnProperty;
var __commonJSMin = (cb, mod) => () => (mod || (cb((mod = { exports: {} }).exports, mod), cb = null), mod.exports);
var __exportAll = (all, no_symbols) => {
	let target = {};
	for (var name in all) __defProp(target, name, {
		get: all[name],
		enumerable: true
	});
	if (!no_symbols) __defProp(target, Symbol.toStringTag, { value: "Module" });
	return target;
};
var __copyProps = (to, from, except, desc) => {
	if (from && typeof from === "object" || typeof from === "function") for (var keys = __getOwnPropNames(from), i = 0, n = keys.length, key; i < n; i++) {
		key = keys[i];
		if (!__hasOwnProp.call(to, key) && key !== except) __defProp(to, key, {
			get: ((k) => from[k]).bind(null, key),
			enumerable: !(desc = __getOwnPropDesc(from, key)) || desc.enumerable
		});
	}
	return to;
};
var __toESM = (mod, isNodeMode, target) => (target = mod != null ? __create(__getProtoOf(mod)) : {}, __copyProps(isNodeMode || !mod || !mod.__esModule ? __defProp(target, "default", {
	value: mod,
	enumerable: true
}) : target, mod));
//#endregion
export { __exportAll as n, __toESM as r, __commonJSMin as t };

//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbImNodW5rLUNZSlBrYy1KLmpzP3Y9JTJGY2h1bmstQ1lKUGtjLUouanMiXSwic291cmNlc0NvbnRlbnQiOlsiLy8jcmVnaW9uIFxcMHJvbGxkb3duL3J1bnRpbWUuanNcbnZhciBfX2NyZWF0ZSA9IE9iamVjdC5jcmVhdGU7XG52YXIgX19kZWZQcm9wID0gT2JqZWN0LmRlZmluZVByb3BlcnR5O1xudmFyIF9fZ2V0T3duUHJvcERlc2MgPSBPYmplY3QuZ2V0T3duUHJvcGVydHlEZXNjcmlwdG9yO1xudmFyIF9fZ2V0T3duUHJvcE5hbWVzID0gT2JqZWN0LmdldE93blByb3BlcnR5TmFtZXM7XG52YXIgX19nZXRQcm90b09mID0gT2JqZWN0LmdldFByb3RvdHlwZU9mO1xudmFyIF9faGFzT3duUHJvcCA9IE9iamVjdC5wcm90b3R5cGUuaGFzT3duUHJvcGVydHk7XG52YXIgX19jb21tb25KU01pbiA9IChjYiwgbW9kKSA9PiAoKSA9PiAobW9kIHx8IChjYigobW9kID0geyBleHBvcnRzOiB7fSB9KS5leHBvcnRzLCBtb2QpLCBjYiA9IG51bGwpLCBtb2QuZXhwb3J0cyk7XG52YXIgX19leHBvcnRBbGwgPSAoYWxsLCBub19zeW1ib2xzKSA9PiB7XG5cdGxldCB0YXJnZXQgPSB7fTtcblx0Zm9yICh2YXIgbmFtZSBpbiBhbGwpIF9fZGVmUHJvcCh0YXJnZXQsIG5hbWUsIHtcblx0XHRnZXQ6IGFsbFtuYW1lXSxcblx0XHRlbnVtZXJhYmxlOiB0cnVlXG5cdH0pO1xuXHRpZiAoIW5vX3N5bWJvbHMpIF9fZGVmUHJvcCh0YXJnZXQsIFN5bWJvbC50b1N0cmluZ1RhZywgeyB2YWx1ZTogXCJNb2R1bGVcIiB9KTtcblx0cmV0dXJuIHRhcmdldDtcbn07XG52YXIgX19jb3B5UHJvcHMgPSAodG8sIGZyb20sIGV4Y2VwdCwgZGVzYykgPT4ge1xuXHRpZiAoZnJvbSAmJiB0eXBlb2YgZnJvbSA9PT0gXCJvYmplY3RcIiB8fCB0eXBlb2YgZnJvbSA9PT0gXCJmdW5jdGlvblwiKSBmb3IgKHZhciBrZXlzID0gX19nZXRPd25Qcm9wTmFtZXMoZnJvbSksIGkgPSAwLCBuID0ga2V5cy5sZW5ndGgsIGtleTsgaSA8IG47IGkrKykge1xuXHRcdGtleSA9IGtleXNbaV07XG5cdFx0aWYgKCFfX2hhc093blByb3AuY2FsbCh0bywga2V5KSAmJiBrZXkgIT09IGV4Y2VwdCkgX19kZWZQcm9wKHRvLCBrZXksIHtcblx0XHRcdGdldDogKChrKSA9PiBmcm9tW2tdKS5iaW5kKG51bGwsIGtleSksXG5cdFx0XHRlbnVtZXJhYmxlOiAhKGRlc2MgPSBfX2dldE93blByb3BEZXNjKGZyb20sIGtleSkpIHx8IGRlc2MuZW51bWVyYWJsZVxuXHRcdH0pO1xuXHR9XG5cdHJldHVybiB0bztcbn07XG52YXIgX190b0VTTSA9IChtb2QsIGlzTm9kZU1vZGUsIHRhcmdldCkgPT4gKHRhcmdldCA9IG1vZCAhPSBudWxsID8gX19jcmVhdGUoX19nZXRQcm90b09mKG1vZCkpIDoge30sIF9fY29weVByb3BzKGlzTm9kZU1vZGUgfHwgIW1vZCB8fCAhbW9kLl9fZXNNb2R1bGUgPyBfX2RlZlByb3AodGFyZ2V0LCBcImRlZmF1bHRcIiwge1xuXHR2YWx1ZTogbW9kLFxuXHRlbnVtZXJhYmxlOiB0cnVlXG59KSA6IHRhcmdldCwgbW9kKSk7XG4vLyNlbmRyZWdpb25cbmV4cG9ydCB7IF9fZXhwb3J0QWxsIGFzIG4sIF9fdG9FU00gYXMgciwgX19jb21tb25KU01pbiBhcyB0IH07XG4iXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IkFBQUEsQ0FBQyxDQUFDLENBQUMsTUFBTSxDQUFDLENBQUMsU0FBUyxDQUFDLE9BQU8sQ0FBQztBQUM3QixHQUFHLENBQUMsUUFBUSxDQUFDLENBQUMsQ0FBQyxNQUFNLENBQUMsTUFBTTtBQUM1QixHQUFHLENBQUMsU0FBUyxDQUFDLENBQUMsQ0FBQyxNQUFNLENBQUMsY0FBYztBQUNyQyxHQUFHLENBQUMsZ0JBQWdCLENBQUMsQ0FBQyxDQUFDLE1BQU0sQ0FBQyx3QkFBd0I7QUFDdEQsR0FBRyxDQUFDLGlCQUFpQixDQUFDLENBQUMsQ0FBQyxNQUFNLENBQUMsbUJBQW1CO0FBQ2xELEdBQUcsQ0FBQyxZQUFZLENBQUMsQ0FBQyxDQUFDLE1BQU0sQ0FBQyxjQUFjO0
...[đã rút gọn]
```

#### Phân tích AI
##### 1. Phân loại:
Needs Human Review

##### 2. Lý do phân loại dựa trên runtime evidence của cả nhóm endpoint:
- Tất cả 3 endpoint bị quét đều liên quan đến static resource (file `.js` trong thư mục `node_modules/.vite/deps/`), với cùng tham số query `v` chứa giá trị dạng encoded path như `%2Fchunk-...js`.
- Các request đều trả về HTTP 200 OK, body là mã JavaScript hợp lệ, không có dấu hiệu response khác biệt khi thay đổi payload, không có lỗi server, không có leak file ngoài phạm vi.
- Payload ZAP dùng kiểm tra Path Traversal (chuỗi `%2F` tương đương `/`) nhưng không làm thay đổi phản hồi, không cho thấy truy cập file ngoài vùng tĩnh được phép, hay dữ liệu bí mật bị tiết lộ.
- Confidence được ZAP đánh giá là Low (độ tin cậy thấp).
- Không có dấu hiệu thay đổi header, status code hay response body theo chiều hướng nguy hiểm khi thử payload.
- Endpoint chạy trên môi trường localhost (localhost:5173, 5174), khả năng đây là môi trường phát triển/lab.
- ZAP cảnh báo dựa trên quy tắc phát hiện tiềm năng Path Traversal dựa trên tham số đầu vào dạng file path, tuy nhiên runtime cho thấy ứng dụng vẫn chỉ phục vụ các file static đã định nghĩa rõ ràng.
- Có thể tham số `v` là cơ chế cache-busting hash hoặc xác định phiên bản tài nguyên, không phải input điều khiển trực tiếp đường dẫn file server.

##### 3. Tác động thực tế trong bối cảnh EShop:
- Nếu ứng dụng thực tế chỉ cung cấp tĩnh tài nguyên frontend, với cơ chế cache versioning an toàn, không cho phép người dùng truy vấn tập tin ngoài thư mục web root, rủi ro Path Traversal trên những endpoint này thấp.
- Ngược lại, nếu tham số `v` có thể được lợi dụng để truy cập file nhạy cảm (cấu hình, mã nguồn, dữ liệu người dùng...), thì nguy cơ rất cao.
- Do chưa đủ bằng chứng runtime chỉ ra lỗ hổng thực sự, tác động cụ thể khó xác định.
- Ở môi trường localhost hoặc staging, vấn đề có thể không hiện hữu ở prod nhưng vẫn cần xác nhận.
- Với mức risk High do tính chất CWE-22 Path Traversal, cần lưu ý khi mở rộng chức năng xử lý file.

##### 4. Cách khắc phục cụ thể ở cấp cấu hình/root cause:
- Xác thực nghiêm ngặt tham số `v`, chỉ chấp nhận các giá trị dạng hash/version predefined trong allow list, không cho phép giá trị chứa dấu `/`, `\`, hoặc ký tự làm thay đổi cấu trúc đường dẫn.
- Sử dụng hàm canonicalization (ví dụ: realpath, Path.normalize) để chuẩn hóa đường dẫn đầu vào và đảm bảo không vượt ra khỏi thư mục cấp phép.
- Nếu tham số dùng để tham chiếu file, map bằng cơ chế ID hoặc hash cố định tương ứng đường dẫn file cụ thể, thay vì cho phép nhập trực tiếp đường dẫn.
- Triệt tiêu hoặc reject các chuỗi có khả năng thực hiện traversal như `../`, `%2e%2e/`, `%c0%af`... qua bước validate.
- Giới hạn quyền truy cập file system của server để chỉ đọc được thư mục tài nguyên tĩnh, không để web process có quyền truy xuất file hệ thống khác.
- Nếu có, bổ sung sandbox/chroot hoặc thiết lập AppArmor/SELinux hạn chế.
- Xem xét thiết lập CSP để giảm thiểu việc tải tài nguyên độc hại.

##### 5. Ghi chú tester cần kiểm tra thêm nếu chưa đủ context:
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

### ZAP-009: Content Security Policy (CSP) Header Not Set

#### Tags lỗi
| Thuộc tính | Giá trị |
|---|---|
| Plugin ID | `10038` |
| Alert Ref | `10038-1` |
| Risk | `Medium` |
| Confidence | `High` |
| CWE | CWE-693 |
| WASC | WASC-15 |
| Tags | OWASP_2021_A05, POLICY_QA_STD, POLICY_PENTEST, SYSTEMIC, CWE-693, OWASP_2017_A06, OWASP_2025_A02 |
| Source JSON | `frontend_admin_basic.json`, `frontend_user_basic.json` |
| Site | `http://localhost:5173`, `http://localhost:5174` |

#### Thông tin alert nhóm
- Số endpoint/request instance bị ảnh hưởng: 14
- Phân loại AI: True Positive
- Trạng thái kiểm chứng thủ công: Chưa kiểm chứng

#### Endpoints bị ảnh hưởng
| # | Method | URL | Param | Evidence |
|---|---|---|---|---|
| 24 | GET | `http://localhost:5173` | `N/A` | `N/A` |
| 25 | GET | `http://localhost:5173/` | `N/A` | `N/A` |
| 26 | GET | `http://localhost:5173/forgot-password` | `N/A` | `N/A` |
| 27 | GET | `http://localhost:5173/robots.txt` | `N/A` | `N/A` |
| 28 | GET | `http://localhost:5173/sitemap.xml` | `N/A` | `N/A` |
| 78 | GET | `http://localhost:5174` | `N/A` | `N/A` |
| 79 | GET | `http://localhost:5174/` | `N/A` | `N/A` |
| 80 | GET | `http://localhost:5174/robots.txt` | `N/A` | `N/A` |
| 81 | GET | `http://localhost:5174/sitemap.xml` | `N/A` | `N/A` |
| 102 | GET | `http://localhost:5173` | `N/A` | `N/A` |
| 103 | GET | `http://localhost:5173/` | `N/A` | `N/A` |
| 104 | GET | `http://localhost:5173/forgot-password` | `N/A` | `N/A` |
| 105 | GET | `http://localhost:5173/robots.txt` | `N/A` | `N/A` |
| 106 | GET | `http://localhost:5173/sitemap.xml` | `N/A` | `N/A` |

#### Bằng chứng runtime đại diện

Request:
```http
GET http://localhost:5173 HTTP/1.1
host: localhost:5173
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36
pragma: no-cache
cache-control: no-cache
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDk1NzF9.6xPB8cUE63QhefuiiRzG56zhdFE5lbB-b7dUFPwWED0
```

Request body:
```text
[Không có request body]
```

Response:
```http
HTTP/1.1 200 OK
Vary: Origin
Content-Type: text/html
Cache-Control: no-cache
Etag: W/"26b-Z6hN2DmQRHNqdtv4bv5lcx2QtJk"
Date: Wed, 22 Jul 2026 08:39:33 GMT
Connection: keep-alive
Keep-Alive: timeout=5
Content-Length: 619
```

Response body excerpt:
```text
<!doctype html>
<html lang="en">
  <head>
    <script type="module">import { injectIntoGlobalHook } from "/@react-refresh";
injectIntoGlobalHook(window);
window.$RefreshReg$ = () => {};
window.$RefreshSig$ = () => (type) => type;</script>

    <script type="module" src="/@vite/client"></script>

    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>frontend-web</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
```

#### Phân tích AI
##### 1. Phân loại  
**True Positive**

##### 2. Lý do phân loại dựa trên runtime evidence của cả nhóm endpoint  
- Tất cả 14 endpoint đều trả response HTTP không có header `Content-Security-Policy` (CSP).  
- Đây không phải là false positive vì ZAP quan sát trực tiếp từ response runtime nên xác nhận header này hoàn toàn thiếu.  
- Endpoint đa phần là các giao diện frontend (HTML), tập trung ở các URL cơ bản như `/`, `/forgot-password`, `robots.txt`, `sitemap.xml` thuộc hai source JSON khác nhau đại diện cho user lẫn admin.  
- Header CSP là một chính sách bảo mật quan trọng giúp ngăn các cuộc tấn công XSS và injection trên client, việc thiếu header này tạo điều kiện cho attacker tiềm năng khai thác các lỗ hổng phía client.  
- Scanner có confidence cao, alert Medium risk, phù hợp với mức độ cảnh báo vì thiếu CSP là một lỗ hổng bảo mật "systemic" (toàn hệ thống) chứ không chỉ ở một endpoint riêng lẻ.  
- Không có evidence cho thấy server đã cấu hình CSP hoặc có policy thay thế khác.  
- Môi trường `localhost` tuy thuộc dạng lab/dev nhưng vẫn đáng quan tâm vì dễ bị tấn công nếu deploy ra môi trường thật mà quên cấu hình.

##### 3. Tác động thực tế trong bối cảnh EShop  
- Ứng dụng EShop, dù là frontend, thường chứa các kịch bản nhập liệu, hiển thị nội dung người dùng, hoặc tích hợp script từ nhiều nguồn.  
- Thiếu CSP tăng khả năng tấn công Cross-Site Scripting (XSS), có thể dẫn đến đánh cắp session, thao túng giao diện, thực hiện hành vi giả mạo (phishing), hoặc tiêm mã độc hại.  
- Ảnh hưởng nghiêm trọng hơn nếu site này xử lý thông tin nhạy cảm khách hàng hoặc có quyền admin (frontend_admin_basic.json).  
- Dù chưa phát hiện dấu hiệu bị khai thác hoặc chứa dữ liệu quan trọng trong response, việc không có CSP làm giảm rõ rệt mức độ an toàn của toàn bộ frontend, mất một lớp phòng vệ bổ sung.

##### 4. Cách khắc phục cụ thể ở cấp cấu hình/root cause  
- Cấu hình web server (nghĩa là HTTP server như Nginx, Apache hoặc reverse proxy, hoặc application server) bổ sung HTTP header `Content-Security-Policy`.  
- Xác định chính sách CSP phù hợp với tính năng ứng dụng, ví dụ:  
  - `default-src 'self'` để giới hạn tài nguyên chỉ được load từ chính domain.  
  - Thêm các chỉ thị cho phép script, style, hình ảnh… theo nhu cầu (cẩn trọng với `'unsafe-inline'`, `'unsafe-eval'`).  
- Ví dụ header đơn giản ban đầu có thể như:  
  ```
  Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self'
  ```  
- Kiểm thử kỹ CSP để tránh làm đứt gãy tính năng frontend, đặc biệt với các frontend framework như React, Angular, Vite…  
- Đảm bảo CSP áp dụng đồng bộ cho tất cả endpoint trả về content HTML hoặc có nội dung được tải trên trình duyệt.

##### 5. Ghi chú tester cần kiểm tra thêm nếu chưa đủ context  
- Xác nhận môi trường deploy thực tế (production) có nhận header CSP hay không, vì hiện tại đang scan trên localhost có thể chưa phản ánh cấu hình thực tế.  
- Kiểm tra kỹ các response trả về tài nguyên tĩnh (JS, CSS, fonts, images...) có cần chính sách CSP phức tạp hơn để tránh lỗi load tài nguyên.  
- Nếu đang dùng CDN, kiểm tra cấu hình chính sách CSP trên tầng CDN, proxy.  
- Đảm bảo rằng các chính sách CSP không ảnh hưởng đến chức năng nội bộ như hot reload (ví dụ đoạn script `/@vite/client` trong response cần đánh giá).  
- Xem xét bổ sung các header bảo mật khác bổ trợ như `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy` để nâng cao tổng thể an toàn frontend.

---

**Kết luận:** nhóm alert `ZAP-009 Content Security Policy (CSP) Header Not Set` thực sự tồn tại trên toàn bộ nhóm endpoint test, cần khẩn trương bổ sung CSP header với policy phù hợp nhằm hạn chế rủi ro XSS/Injection trên frontend của ứng dụng EShop.

### ZAP-010: Missing Anti-clickjacking Header

#### Tags lỗi
| Thuộc tính | Giá trị |
|---|---|
| Plugin ID | `10020` |
| Alert Ref | `10020-1` |
| Risk | `Medium` |
| Confidence | `Medium` |
| CWE | CWE-1021 |
| WASC | WASC-15 |
| Tags | OWASP_2021_A05, POLICY_QA_STD, POLICY_PENTEST, CWE-1021, SYSTEMIC, WSTG-v42-CLNT-09, OWASP_2017_A06, OWASP_2025_A02 |
| Source JSON | `frontend_admin_basic.json`, `frontend_user_basic.json` |
| Site | `http://localhost:5173`, `http://localhost:5174` |

#### Thông tin alert nhóm
- Số endpoint/request instance bị ảnh hưởng: 14
- Phân loại AI: True Positive
- Trạng thái kiểm chứng thủ công: Chưa kiểm chứng

#### Endpoints bị ảnh hưởng
| # | Method | URL | Param | Evidence |
|---|---|---|---|---|
| 29 | GET | `http://localhost:5173` | `x-frame-options` | `N/A` |
| 30 | GET | `http://localhost:5173/` | `x-frame-options` | `N/A` |
| 31 | GET | `http://localhost:5173/forgot-password` | `x-frame-options` | `N/A` |
| 32 | GET | `http://localhost:5173/robots.txt` | `x-frame-options` | `N/A` |
| 33 | GET | `http://localhost:5173/sitemap.xml` | `x-frame-options` | `N/A` |
| 82 | GET | `http://localhost:5174` | `x-frame-options` | `N/A` |
| 83 | GET | `http://localhost:5174/` | `x-frame-options` | `N/A` |
| 84 | GET | `http://localhost:5174/robots.txt` | `x-frame-options` | `N/A` |
| 85 | GET | `http://localhost:5174/sitemap.xml` | `x-frame-options` | `N/A` |
| 107 | GET | `http://localhost:5173` | `x-frame-options` | `N/A` |
| 108 | GET | `http://localhost:5173/` | `x-frame-options` | `N/A` |
| 109 | GET | `http://localhost:5173/forgot-password` | `x-frame-options` | `N/A` |
| 110 | GET | `http://localhost:5173/robots.txt` | `x-frame-options` | `N/A` |
| 111 | GET | `http://localhost:5173/sitemap.xml` | `x-frame-options` | `N/A` |

#### Bằng chứng runtime đại diện

Request:
```http
GET http://localhost:5173 HTTP/1.1
host: localhost:5173
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36
pragma: no-cache
cache-control: no-cache
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDk1NzF9.6xPB8cUE63QhefuiiRzG56zhdFE5lbB-b7dUFPwWED0
```

Request body:
```text
[Không có request body]
```

Response:
```http
HTTP/1.1 200 OK
Vary: Origin
Content-Type: text/html
Cache-Control: no-cache
Etag: W/"26b-Z6hN2DmQRHNqdtv4bv5lcx2QtJk"
Date: Wed, 22 Jul 2026 08:39:33 GMT
Connection: keep-alive
Keep-Alive: timeout=5
Content-Length: 619
```

Response body excerpt:
```text
<!doctype html>
<html lang="en">
  <head>
    <script type="module">import { injectIntoGlobalHook } from "/@react-refresh";
injectIntoGlobalHook(window);
window.$RefreshReg$ = () => {};
window.$RefreshSig$ = () => (type) => type;</script>

    <script type="module" src="/@vite/client"></script>

    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>frontend-web</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
```

#### Phân tích AI
##### Triage Alert ZAP-010: Missing Anti-clickjacking Header (Plugin ID: 10020)

---

##### 1. Phân loại  
**True Positive**

---

##### 2. Lý do phân loại dựa trên runtime evidence của cả nhóm endpoint  
- Toàn bộ 14 endpoint của ứng dụng EShop (gồm giao diện user và admin, đa phần các trang trả về HTML) đều không có header `X-Frame-Options` cũng như không có header `Content-Security-Policy` với directive `frame-ancestors`.  
- ZAP scan runtime ghi nhận rõ ràng HTTP response trả về thiếu các header bảo vệ chống clickjacking.  
- Đặc biệt, các trang HTML chính (gốc `/`, `/forgot-password`) đều bị ảnh hưởng.  
- Không có evidence cho thấy có header thay thế hoặc chính sách CSP frame-ancestors.  
- Các resource như `robots.txt`, `sitemap.xml` không bắt buộc phải có nhưng vẫn không ảnh hưởng tới việc bảo vệ chống iframe ít nhất ở các trang giao diện chính.  
- Môi trường là localhost nhưng thông tin này chỉ làm rõ thêm ngữ cảnh, không làm giảm mức độ thực tế của lỗ hổng nếu triển khai tương tự trên môi trường sản xuất.

---

##### 3. Tác động thực tế trong bối cảnh EShop  
- Thiếu header chống clickjacking tạo điều kiện cho attacker sử dụng kỹ thuật clickjacking, bẫy người dùng tương tác với trang EShop thông qua iframe độc hại từ trang khác, dẫn đến việc thực hiện các hành động không mong muốn (ví dụ: chuyển khoản, thay đổi thông tin, đặt hàng).  
- Trang `/forgot-password` hoặc các trang nhạy cảm khác nếu bị clickjacked sẽ có nguy cơ cao bị lợi dụng làm lừa đảo hoặc chiếm quyền tài khoản.  
- Mức độ rủi ro được đánh giá là Medium phù hợp, do đây là một lớp bảo vệ tiêu chuẩn cơ bản trong chính sách bảo mật web, không thuộc lỗi nghiêm trọng nhưng dễ khai thác nếu kết hợp với social engineering.  
- Ảnh hưởng đến độ tin cậy và an toàn tổng thể của ứng dụng, làm giảm sự tin tưởng người dùng và uy tín thương hiệu EShop.

---

##### 4. Cách khắc phục cụ thể ở cấp cấu hình/root cause  
- Thêm header HTTP bảo vệ iframe trong response của ứng dụng trên tất cả các trang HTML:  
  - Sử dụng header `X-Frame-Options` với giá trị phù hợp:  
    - `DENY` nếu trang không nên được nhúng bởi bất kỳ trang nào khác.  
    - `SAMEORIGIN` nếu chỉ cho phép nhúng trong cùng origin.  
  - Hoặc thay thế/quyết định sử dụng `Content-Security-Policy` với directive:  
    ```http
    Content-Security-Policy: frame-ancestors 'self'
    ```  
- Cập nhật cấu hình server (Apache, Nginx, hay backend framework) hoặc áp dụng tại lớp trung gian (proxy, CDN, WAF) để đảm bảo tất cả response HTML trả về đều có header này.  
- Kiểm tra lại các trang critical như login, forgot-password, user profile, thanh toán để đảm bảo nhất quán.  
- Tài liệu tham khảo chuẩn và công cụ hỗ trợ:  
  - Mozilla Doc: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options  
  - OWASP Cheat Sheet về Clickjacking Defense.

---

##### 5. Ghi chú tester cần kiểm tra thêm nếu chưa đủ context  
- Xác nhận môi trường triển khai thực tế (production, staging) có cấu hình header tương tự hay khác so với dev/localhost.  
- Kiểm tra hiện trạng có sử dụng CSP frame-ancestors ở ngoài scope ZAP scan (ví dụ các response khác hoặc thông qua meta tag).  
- Đánh giá business impact chi tiết hơn với bộ phận nghiệp vụ, nhất là với các trang có giao dịch nhạy cảm hoặc chứa dữ liệu quan trọng.  
- Kiểm tra ảnh hưởng khi trang có nhúng iframe hợp pháp có thể bị header này chặn, để có lựa chọn cấu hình phù hợp (ví dụ dùng CSP frame-ancestors tinh chỉnh hơn).  
- Nếu sử dụng CDN hoặc proxy layer, xác nhận không bị strip header khi response qua các lớp trung gian.

---

**Tóm lại:** hiện tại các alert ZAP-010 đều phản ánh tình trạng thiếu header chống clickjacking trên nhiều endpoint quan trọng, do đó đánh giá là True Positive, cần ưu tiên bổ sung header bảo vệ ngay để giảm thiểu rủi ro clickjacking cho ứng dụng EShop.

### ZAP-011: Timestamp Disclosure - Unix

#### Tags lỗi
| Thuộc tính | Giá trị |
|---|---|
| Plugin ID | `10096` |
| Alert Ref | `10096` |
| Risk | `Low` |
| Confidence | `Low` |
| CWE | CWE-497 |
| WASC | WASC-13 |
| Tags | OWASP_2021_A01, POLICY_PENTEST, SYSTEMIC, OWASP_2017_A03, OWASP_2025_A01, CWE-497 |
| Source JSON | `frontend_admin_basic.json`, `frontend_user_basic.json` |
| Site | `http://localhost:5173`, `http://localhost:5174` |

#### Thông tin alert nhóm
- Số endpoint/request instance bị ảnh hưởng: 3
- Phân loại AI: Needs Human Review
- Trạng thái kiểm chứng thủ công: Chưa kiểm chứng

#### Endpoints bị ảnh hưởng
| # | Method | URL | Param | Evidence |
|---|---|---|---|---|
| 34 | GET | `http://localhost:5173/node_modules/.vite/deps/react-dom_client.js?v=82fd3d9d` | `N/A` | `2080374784` |
| 86 | GET | `http://localhost:5174/node_modules/.vite/deps/react-dom_client.js?v=1cc4e6b1` | `N/A` | `2080374784` |
| 112 | GET | `http://localhost:5173/node_modules/.vite/deps/react-dom_client.js?v=82fd3d9d` | `N/A` | `2080374784` |

#### Bằng chứng runtime đại diện

Request:
```http
GET http://localhost:5173/node_modules/.vite/deps/react-dom_client.js?v=82fd3d9d HTTP/1.1
host: localhost:5173
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Connection: keep-alive
Referer: http://localhost:5173/src/main.jsx
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDk1NzF9.6xPB8cUE63QhefuiiRzG56zhdFE5lbB-b7dUFPwWED0
```

Request body:
```text
[Không có request body]
```

Response:
```http
HTTP/1.1 200 OK
Vary: Origin
Content-Type: text/javascript
Cache-Control: max-age=31536000,immutable
Etag: W/"c86f6-Hwics9k2qc5cCKaA6olSjs9VceE"
Date: Wed, 22 Jul 2026 08:39:40 GMT
Connection: keep-alive
Keep-Alive: timeout=5
Content-Length: 820982
```

Response body excerpt:
```text
import { t as __commonJSMin } from "/node_modules/.vite/deps/chunk-CYJPkc-J.js?v=82fd3d9d";
import { t as require_react } from "/node_modules/.vite/deps/react.js?v=82fd3d9d";
import { t as require_react_dom } from "/node_modules/.vite/deps/react-dom.js?v=82fd3d9d";
//#region node_modules/scheduler/cjs/scheduler.development.js
/**
* @license React
* scheduler.development.js
*
* Copyright (c) Meta Platforms, Inc. and affiliates.
*
* This source code is licensed under the MIT license found in the
* LICENSE file in the root directory of this source tree.
*/
var require_scheduler_development = /* @__PURE__ */ __commonJSMin(((exports) => {
	(function() {
		function performWorkUntilDeadline() {
			needsPaint = !1;
			if (isMessageLoopRunning) {
				var currentTime = exports.unstable_now();
				startTime = currentTime;
				var hasMoreWork = !0;
				try {
					a: {
						isHostCallbackScheduled = !1;
						isHostTimeoutScheduled && (isHostTimeoutScheduled = !1, localClearTimeout(taskTimeoutID), taskTimeoutID = -1);
						isPerformingWork = !0;
						var previousPriorityLevel = currentPriorityLevel;
						try {
							b: {
								advanceTimers(currentTime);
								for (currentTask = peek(taskQueue); null !== currentTask && !(currentTask.expirationTime > currentTime && shouldYieldToHost());) {
									var callback = currentTask.callback;
									if ("function" === typeof callback) {
										currentTask.callback = null;
										currentPriorityLevel = currentTask.priorityLevel;
										var continuationCallback = callback(currentTask.expirationTime <= currentTime);
										currentTime = exports.unstable_now();
										if ("function" === typeof continuationCallback) {
											currentTask.callback = continuationCallback;
											advanceTimers(currentTime);
											hasMoreWork = !0;
											break b;
										}
										currentTask === peek(taskQueue) && pop(taskQueue);
										advanceTimers(currentTime);
									} else pop(taskQueue);
									currentTask = peek(taskQueue);
								}
								if (null !== currentTask) hasMoreWork = !0;
								else {
									var firstTimer = peek(timerQueue);
									null !== firstTimer && requestHostTimeout(handleTimeout, firstTimer.startTime - currentTime);
									hasMoreWork = !1;
								}
							}
							break a;
						} finally {
							currentTask = null, currentPriorityLevel = previousPriorityLevel, isPerformingWork = !1;
						}
						hasMoreWork = void 0;
					}
				} finally {
					hasMoreWork ? schedulePerformWorkUntilDeadline() : isMessageLoopRunning = !1;
				}
			}
		}
		function push(heap, node) {
			var index = heap.length;
			heap.push(node);
			a: for (; 0 < index;) {
				var parentIndex = index - 1 >>> 1, parent = heap[parentIndex];
				if (0 < compare(parent, node)) heap[parentIndex] = node, heap[index] = parent, index = parentIndex;
				else break a;
			}
		}
		function peek(heap) {
			return 0 === heap.length ? null : heap[0];
		}
		function pop(heap) {
			if (0 === heap.length) return null;
			var first = heap[0], last = heap.pop();
			if (last !== first) {
				heap[0] = last;
				a: for (var index = 0, length = heap.length, halfLength = length >>> 1; index < halfLength;) {
					var leftIndex = 2 * (index + 1) - 1, left = heap[leftIndex], rightIndex = leftIndex + 1, right = heap[rightIndex];
					if (0 > compare(left, last)) rightIndex < length && 0 > compare(right, left) ? (heap[index] = right, heap[rightIndex] = last, index = rightIndex) : (heap[index] = left, heap[leftIndex] = last, index = leftIndex);
					else if (rightIndex < length && 0 > compare(right, last)) heap[index] = right, heap[rightIndex] = last, index = rightIndex;
					else break a;
				}
			}
			return first;
		}
		function compare(a, b) {
			var diff = a.sortIndex - b.sortIndex;
			return 0 !== diff ? diff : a.id - b.id;
		}
		function advanceTimers(currentTime) {
			for (var timer = peek(timerQueue); null !== timer;) {
				if (null === timer.callback) pop(timerQueue);
				else if (t
...[đã rút gọn]
```

#### Phân tích AI
##### Triage alert ZAP-011: Timestamp Disclosure - Unix (Plugin ID: 10096)

---

##### 1. Phân loại  
**Needs Human Review**

---

##### 2. Lý do phân loại dựa trên runtime evidence của cả nhóm endpoint  

- Các endpoint bị phát hiện đều là các tài nguyên tĩnh (JS files) phục vụ frontend, nằm trong thư mục `/node_modules/.vite/deps/`.  
- Evidences cho thấy có một giá trị số dạng timestamp Unix (`2080374784`) xuất hiện trong response hoặc các tham số query (chẳng hạn trong `v=82fd3d9d`), tuy nhiên ZAP không chỉ rõ timestamp xuất hiện ở header hay body mà chủ yếu dựa trên tham số query (`v=`) dùng để cache/versioning assets.  
- Response header như `Date` không chứa timestamp Unix, mà chỉ dùng chuẩn dạng GMT thông thường, không gây rò rỉ thông tin đặc biệt.  
- Không thấy timestamp này đi kèm với thông tin nhạy cảm hoặc bất kỳ dữ liệu người dùng, server-side nào.  
- Đây là hành vi phổ biến trong frontend build tools (như vite, webpack) dùng cache-busting version hash hoặc phiên bản thời gian để điều khiển cache, không phải lỗi lộ thông tin nhạy cảm do backend.  
- Mức độ **Confidence: Low** và **Risk: Low** cho thấy nhiều khả năng đây là signal thông tin, không phải lỗ hổng bảo mật nghiêm trọng tại runtime.  
- Môi trường localhost có thể cho phép nhiều quá trình phát triển/debug nên cũng chưa chắc phản ánh môi trường production thực tế.  

---

##### 3. Tác động thực tế trong bối cảnh EShop  

- Với ứng dụng EShop, nếu timestamp này thực sự chỉ dùng cho cache-control/versioning file tĩnh frontend thì tác động bảo mật là thấp, gần như không có rủi ro bị khai thác.  
- Thông tin timestamp dạng này không đủ để giúp attacker khai thác thêm (ví dụ không tiết lộ thời gian server hoạt động, history hoạt động của user, hoặc bất kỳ thời điểm nhạy cảm nào trong business logic).  
- Nếu môi trường production được cấu hình khác và không công khai tài nguyên như localhost, thì mức độ rủi ro càng thấp.  
- Tuy nhiên, cần kiểm tra thêm trong môi trường production có tình trạng tương tự hay không.  

---

##### 4. Cách khắc phục cụ thể ở cấp cấu hình/root cause  

- Nếu đây là version hash hoặc timestamp dùng cho cache-busting frontend (vite, webpack...), có thể giữ nguyên để tối ưu cache nhưng nên:  
  - Kiểm tra không để lộ bất kỳ timestamp nhạy cảm (ví dụ thời gian phiên đăng nhập, sinh nhật user, internal server time) trong response body hoặc header.  
  - Đảm bảo các thông tin phiên, token, hoặc dữ liệu nhạy cảm không được inject kèm theo các asset tĩnh này.  
  - Với các timestamp trong query param hoặc header, chỉ nên dùng các giá trị không liên quan đến thông tin nhạy cảm (ví dụ hash ngẫu nhiên thay vì timestamp Unix rõ ràng).  
- Nếu timestamp hoặc thông tin này xuất phát từ server, cân nhắc cấu hình server hoặc CDN loại bỏ hoặc che chắn header/số liệu không cần thiết.  
- Đảm bảo deploy production không để debug hoặc source map assets công khai chứa thông tin hệ thống.  

---

##### 5. Ghi chú tester cần kiểm tra thêm nếu chưa đủ context  

- Xác nhận xem `v=` param trong URL thực sự là cache buster do frontend build tool tạo ra hay timestamp có ý nghĩa runtime khác.  
- Kiểm tra kỹ response body, header ở production và dưới các quyền user khác (không chỉ localhost) có lộ timestamp tương tự không.  
- Đánh giá xem timestamp có thể được kết hợp với dữ liệu khác để rò rỉ thông tin nhạy cảm hay dùng vào mục đích tấn công (ví dụ side channel) không.  
- Kiểm tra các endpoint khác có lộ thông tin dạng timestamp Unix vào response không, đặc biệt trong API JSON có dữ liệu business.  
- Tham khảo với developers hoặc team DevOps về mục đích tạo timestamp/version param này.  
- Nếu có access kho mã nguồn hoặc CI/CD pipeline, rà soát cấu hình build để xác định nguồn gốc timestamp/version param.  

---

##### Tổng kết  

Nhóm alert ZAP-011 với evidences runtime của 3 endpoint dạng tài nguyên frontend static file có tiết lộ timestamp Unix trong query param/version string, rất có khả năng là False Positive do đặc điểm kỹ thuật build frontend (cache busting). Tuy nhiên cần review thêm ở môi trường production, kiểm tra chi tiết để xác định chính xác tính nhạy cảm của timestamp này, tránh bỏ sót rò rỉ thông tin tiềm ẩn. Vì vậy đánh giá hiện tại là **Needs Human Review** với cảnh báo cảnh giác nhẹ.

### ZAP-012: Information Disclosure - Sensitive Information in URL

#### Tags lỗi
| Thuộc tính | Giá trị |
|---|---|
| Plugin ID | `10024` |
| Alert Ref | `10024` |
| Risk | `Informational` |
| Confidence | `Medium` |
| CWE | CWE-598 |
| WASC | WASC-13 |
| Tags | CWE-598, OWASP_2021_A01, POLICY_QA_STD, POLICY_PENTEST, SYSTEMIC, OWASP_2017_A03, OWASP_2025_A01, POLICY_DEV_STD |
| Source JSON | `frontend_admin_basic.json`, `frontend_user_basic.json` |
| Site | `http://localhost:5173`, `http://localhost:5174` |

#### Thông tin alert nhóm
- Số endpoint/request instance bị ảnh hưởng: 3
- Phân loại AI: Needs Human Review
- Trạng thái kiểm chứng thủ công: Chưa kiểm chứng

#### Endpoints bị ảnh hưởng
| # | Method | URL | Param | Evidence |
|---|---|---|---|---|
| 40 | GET | `http://localhost:5173/?token=7NvYDWb8HNrK` | `token` | `token` |
| 92 | GET | `http://localhost:5174/?token=-LYBc--RLYE6` | `token` | `token` |
| 118 | GET | `http://localhost:5173/?token=7NvYDWb8HNrK` | `token` | `token` |

#### Bằng chứng runtime đại diện

Request:
```http
GET http://localhost:5173/?token=7NvYDWb8HNrK HTTP/1.1
host: localhost:5173
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Sec-WebSocket-Version: 13
Origin: http://localhost:5173
Sec-WebSocket-Protocol: vite-hmr
Sec-WebSocket-Key: /z+7rhddK1vlqzbW2Q9bEg==
Connection: Upgrade
Pragma: no-cache
Cache-Control: no-cache
Upgrade: websocket
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDk1NzF9.6xPB8cUE63QhefuiiRzG56zhdFE5lbB-b7dUFPwWED0
```

Request body:
```text
[Không có request body]
```

Response:
```http
HTTP/1.1 101 Switching Protocols
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Accept: lstVjRKKpne83EJmnYy5/PNEtcY=
Sec-WebSocket-Protocol: vite-hmr
```

Response body excerpt:
```text
[Không có response body]
```

#### Phân tích AI
##### 1. Phân loại  
**Needs Human Review**

---

##### 2. Lý do phân loại dựa trên runtime evidence của cả nhóm endpoint  
- ZAP phát hiện tham số `token` chứa dữ liệu dạng sensitive information được truyền trong URL (query string) ở 3 endpoint có request GET trên hostname `localhost` (dev/lab environment).  
- Evidence chỉ thể hiện token nằm trong URL request, nhưng response không trả về dữ liệu nhạy cảm, cũng không có thông tin cho thấy token bị rò rỉ ra ngoài (như qua response body hay header). Response 101 Switching Protocols chỉ là giai đoạn thiết lập websocket, không có dữ liệu thực thi hay phản hồi chứa sensitive info.  
- Alert có confidence **Medium**, risk level **Informational**, thuộc CWE-598 (Exposure of Sensitive Information to an Unauthorized Actor) và WASC-13 (Information Leakage).  
- Việc truyền `token` trong URL tiềm ẩn nguy cơ bị lộ thông tin nhạy cảm qua logs, cache, browser history,... nhưng trên runtime này chưa xác định được token có phải là credential thực sự, token đó có thể là session token hoặc token truy cập (bearer token đã nằm trong header riêng, riêng biệt) và chưa đủ bằng chứng cho exploit cụ thể.  
- Môi trường localhost/lab có thể không áp dụng mật độ bảo mật cao như production, cần kiểm tra kỹ môi trường triển khai thực tế.  
- Do alert mang tính cảnh báo/khuyến nghị (informational) và chưa có bằng chứng thực tế về leak hay khai thác, nên không nâng mức severity thành cao hơn mà chỉ needs review thêm.  

---

##### 3. Tác động thực tế trong bối cảnh EShop  
- Nếu token truyền trong URL là credential hoặc session token, có thể dẫn đến rò rỉ khi URL bị ghi log hoặc lộ cho bên thứ ba (referrer headers, browser history).  
- Mức độ ảnh hưởng trực tiếp ở runtime chưa thấy rõ exploit nhưng về mặt best practice bảo mật, truyền sensitive thông tin qua URL là không an toàn.  
- Với ứng dụng EShop có phân quyền user và admin, token trong URL có thể là attack vector nếu bị đánh cắp phục vụ truy cập trái phép.  
- Tuy nhiên, ở môi trường localhost/lab, đây có thể là đoạn dev/debug hoặc chưa finalize cấu hình bảo mật, nên cần xác nhận lại môi trường thực thi.  

---

##### 4. Cách khắc phục cụ thể ở cấp cấu hình/root cause  
- Không truyền thông tin nhạy cảm như token, mật khẩu, session ID qua URL (query string).  
- Sử dụng header HTTP (ví dụ: Authorization header hoặc custom header) để gửi token/bearer token an toàn hơn, tránh ghi lại trong logs hoặc bị lộ qua referrer.  
- Nếu buộc phải truyền một số tham số qua URL, hãy đảm bảo token chỉ là một giá trị temporary, ngắn hạn, hoặc mã hóa/hashing an toàn để giảm rủi ro lộ thông tin.  
- Cấu hình server/application không ghi log đầy đủ query string chứa token, hoặc filter logs để tránh ghi lại các tham số nhạy cảm.  
- Đào tạo developer tuân thủ chính sách bảo mật OWASP và các chuẩn về bảo vệ thông tin nhạy cảm qua giao thức HTTP.  

---

##### 5. Ghi chú tester cần kiểm tra thêm nếu chưa đủ context  
- Xác nhận token trong URL có phải là thông tin nhạy cảm thực sự (ví dụ: session token, access token, hoặc một dạng ID nhạy cảm) hay chỉ là code tạm/không dùng cho auth.  
- Kiểm tra môi trường deploy có phải là môi trường production hay staging/localhost để đánh giá mức độ ảnh hưởng thực tế và khuyến cáo phù hợp.  
- Đánh giá xem ứng dụng có ghi lại logs request bao gồm token trong URL hay không, xem logs có bị rò rỉ ra bên ngoài (vd: hệ thống giám sát, firewall, proxy).  
- Kiểm thử trường hợp token bị lộ qua referer header đến website thứ ba khi ứng dụng thực hiện các redirect/external link.  
- Đánh giá cách token được tạo và expires như thế nào, độ an toàn khi lưu trữ/mã hóa token.  
- Tham khảo team phát triển để kiểm tra kế hoạch cải thiện bảo mật HTTP API theo chính sách OWASP hoặc quy định nội bộ.

### ZAP-013: Information Disclosure - Suspicious Comments

#### Tags lỗi
| Thuộc tính | Giá trị |
|---|---|
| Plugin ID | `10027` |
| Alert Ref | `10027` |
| Risk | `Informational` |
| Confidence | `Medium` |
| CWE | CWE-615 |
| WASC | WASC-13 |
| Tags | OWASP_2021_A01, POLICY_PENTEST, CWE-615, WSTG-v42-INFO-05, OWASP_2017_A03, OWASP_2025_A01 |
| Source JSON | `frontend_admin_basic.json`, `frontend_user_basic.json` |
| Site | `http://localhost:5173`, `http://localhost:5174` |

#### Thông tin alert nhóm
- Số endpoint/request instance bị ảnh hưởng: 16
- Phân loại AI: Needs Human Review
- Trạng thái kiểm chứng thủ công: Chưa kiểm chứng

#### Endpoints bị ảnh hưởng
| # | Method | URL | Param | Evidence |
|---|---|---|---|---|
| 41 | GET | `http://localhost:5173/@react-refresh` | `N/A` | `// TODO: rename these field` |
| 42 | GET | `http://localhost:5173/@react-refresh` | `N/A` | `ogic is copy-pasted from similar logic in th` |
| 43 | GET | `http://localhost:5173/node_modules/.vite/deps/axios.js?v=82fd3d9d` | `N/A` | `to copy properties from * @param {Object} t` |
| 44 | GET | `http://localhost:5173/node_modules/.vite/deps/axios.js?v=82fd3d9d` | `N/A` | `in the same key the later object in * the arg` |
| 45 | GET | `http://localhost:5173/node_modules/.vite/deps/react-router-dom.js?v=82fd3d9d` | `N/A` | `* 	* Access a value from the context. If no` |
| 46 | GET | `http://localhost:5173/node_modules/.vite/deps/react-router-dom.js?v=82fd3d9d` | `N/A` | `, will 	* cause the user agent to ignore the` |
| 93 | GET | `http://localhost:5174/@react-refresh` | `N/A` | `// TODO: rename these field` |
| 94 | GET | `http://localhost:5174/@react-refresh` | `N/A` | `ogic is copy-pasted from similar logic in th` |
| 95 | GET | `http://localhost:5174/node_modules/.vite/deps/axios.js?v=1cc4e6b1` | `N/A` | `to copy properties from * @param {Object} t` |
| 96 | GET | `http://localhost:5174/node_modules/.vite/deps/axios.js?v=1cc4e6b1` | `N/A` | `in the same key the later object in * the arg` |
| 119 | GET | `http://localhost:5173/@react-refresh` | `N/A` | `// TODO: rename these field` |
| 120 | GET | `http://localhost:5173/@react-refresh` | `N/A` | `ogic is copy-pasted from similar logic in th` |
| 121 | GET | `http://localhost:5173/node_modules/.vite/deps/axios.js?v=82fd3d9d` | `N/A` | `to copy properties from * @param {Object} t` |
| 122 | GET | `http://localhost:5173/node_modules/.vite/deps/axios.js?v=82fd3d9d` | `N/A` | `in the same key the later object in * the arg` |
| 123 | GET | `http://localhost:5173/node_modules/.vite/deps/react-router-dom.js?v=82fd3d9d` | `N/A` | `* 	* Access a value from the context. If no` |
| 124 | GET | `http://localhost:5173/node_modules/.vite/deps/react-router-dom.js?v=82fd3d9d` | `N/A` | `, will 	* cause the user agent to ignore the` |

#### Bằng chứng runtime đại diện

Request:
```http
GET http://localhost:5173/@react-refresh HTTP/1.1
host: localhost:5173
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Connection: keep-alive
Referer: http://localhost:5173/
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDk1NzF9.6xPB8cUE63QhefuiiRzG56zhdFE5lbB-b7dUFPwWED0
```

Request body:
```text
[Không có request body]
```

Response:
```http
HTTP/1.1 200 OK
Vary: Origin
Content-Type: text/javascript
Cache-Control: no-cache
Etag: W/"5367-h8iO905IyT3hT92qDTgpgcseDiA"
Date: Wed, 22 Jul 2026 08:39:40 GMT
Connection: keep-alive
Keep-Alive: timeout=5
Content-Length: 111894
```

Response body excerpt:
```text
import { injectQuery as __vite__injectQuery } from "/@vite/client";/* global window */
/* eslint-disable eqeqeq, prefer-const, @typescript-eslint/no-empty-function */

/*! Copyright (c) Meta Platforms, Inc. and affiliates. **/
/**
 * This is simplified pure-js version of https://github.com/facebook/react/blob/main/packages/react-refresh/src/ReactFreshRuntime.js
 * without IE11 compatibility and verbose isDev checks.
 * Some utils are appended at the bottom for HMR integration.
 */

const REACT_FORWARD_REF_TYPE = Symbol.for('react.forward_ref')
const REACT_MEMO_TYPE = Symbol.for('react.memo')

// We never remove these associations.
// It's OK to reference families, but use WeakMap/Set for types.
let allFamiliesByID = new Map()
let allFamiliesByType = new WeakMap()
let allSignaturesByType = new WeakMap()

// This WeakMap is read by React, so we only put families
// that have actually been edited here. This keeps checks fast.
const updatedFamiliesByType = new WeakMap()

// This is cleared on every performReactRefresh() call.
// It is an array of [Family, NextType] tuples.
let pendingUpdates = []

// This is injected by the renderer via DevTools global hook.
const helpersByRendererID = new Map()

const helpersByRoot = new Map()

// We keep track of mounted roots so we can schedule updates.
const mountedRoots = new Set()
// If a root captures an error, we remember it so we can retry on edit.
const failedRoots = new Set()

// We also remember the last element for every root.
// It needs to be weak because we do this even for roots that failed to mount.
// If there is no WeakMap, we won't attempt to do retrying.
let rootElements = new WeakMap()
let isPerformingRefresh = false

function computeFullKey(signature) {
  if (signature.fullKey !== null) {
    return signature.fullKey
  }

  let fullKey = signature.ownKey
  let hooks
  try {
    hooks = signature.getCustomHooks()
  } catch (err) {
    // This can happen in an edge case, e.g. if expression like Foo.useSomething
    // depends on Foo which is lazily initialized during rendering.
    // In that case just assume we'll have to remount.
    signature.forceReset = true
    signature.fullKey = fullKey
    return fullKey
  }

  for (let i = 0; i < hooks.length; i++) {
    const hook = hooks[i]
    if (typeof hook !== 'function') {
      // Something's wrong. Assume we need to remount.
      signature.forceReset = true
      signature.fullKey = fullKey
      return fullKey
    }
    const nestedHookSignature = allSignaturesByType.get(hook)
    if (nestedHookSignature === undefined) {
      // No signature means Hook wasn't in the source code, e.g. in a library.
      // We'll skip it because we can assume it won't change during this session.
      continue
    }
    const nestedHookKey = computeFullKey(nestedHookSignature)
    if (nestedHookSignature.forceReset) {
      signature.forceReset = true
    }
    fullKey += '\n---\n' + nestedHookKey
  }

  signature.fullKey = fullKey
  return fullKey
}

function haveEqualSignatures(prevType, nextType) {
  const prevSignature = allSignaturesByType.get(prevType)
  const nextSignature = allSignaturesByType.get(nextType)

  if (prevSignature === undefined && nextSignature === undefined) {
    return true
  }
  if (prevSignature === undefined || nextSignature === undefined) {
    return false
  }
  if (computeFullKey(prevSignature) !== computeFullKey(nextSignature)) {
    return false
  }
  if (nextSignature.forceReset) {
    return false
  }

  return true
}

function isReactClass(type) {
  return type.prototype && type.prototype.isReactComponent
}

function canPreserveStateBetween(prevType, nextType) {
  if (isReactClass(prevType) || isReactClass(nextType)) {
    return false
  }
  if (haveEqualSignatures(prevType, nextType)) {
    return true
  }
  return false
}

function resolveFamily(type) {
  // Only check updated types to keep lookups fast.
  return updatedFamiliesByType.get(type)
}

// This is a safety mechanism to protect against rogue
...[đã rút gọn]
```

#### Phân tích AI
##### Triaging Alert ZAP-013: Information Disclosure - Suspicious Comments (Plugin ID 10027)

---

##### 1. Phân loại  
**Needs Human Review**

---

##### 2. Lý do phân loại dựa trên runtime evidence của cả nhóm endpoint  
- Nhóm alert phát hiện trên 16 endpoint đều trả về response chứa các comment (commented code hoặc chú thích trong file JavaScript), chủ yếu là các comment dạng TODO hoặc giải thích về chức năng của các đoạn code/biblioteca (ví dụ React Refresh, axios...).  
- Các comment này không tiết lộ dữ liệu nhạy cảm hoặc thông tin cấu hình quan trọng của ứng dụng EShop mà chỉ liên quan đến code nguồn phía client (JS bundles, thư viện bên thứ ba).  
- Response header và body không có dấu hiệu rò rỉ thông tin cá nhân, thông tin session, cấu trúc backend hay các chi tiết backend phục vụ việc khai thác thực tế.  
- Các resource này chạy trên localhost, thường là môi trường phát triển hoặc staging, không phải production.  
- Đây là dạng alert with Risk: Informational và Confidence: Medium – báo hiệu tín hiệu cảnh báo nhẹ, có thể không phải lỗi nghiêm trọng nhưng cần đánh giá kỹ.  
- Việc giữ comment trong file JS bundle là bình thường trong môi trường dev, ít phổ biến trong production, nhưng có thể không trực tiếp gây hại nếu không lộ thông tin nhạy cảm.  
- Do ZAP không có khả năng phân biệt môi trường deploy (dev hay prod) và không rõ cấu hình build bundling của dự án, rất khó xác định ngay đây là cấu hình không an toàn hay chỉ là "đặc điểm dev".  
- Vì vậy, cần human review đánh giá môi trường, chính sách build/deploy và mức độ nhạy cảm của comment để phân loại chính xác hơn (True Positive hay False Positive).

---

##### 3. Tác động thực tế trong bối cảnh EShop  
- Nếu đây là môi trường phát triển hoặc staging, nguy cơ thực tế rất thấp, hầu như không gây ảnh hưởng đến bảo mật.  
- Nếu các file này được deploy lên môi trường production mở ra cho người dùng cuối, có thể ít nhiều gây lộ thông tin về kiến trúc, thư viện sử dụng hoặc kế hoạch phát triển (TODOs), giúp attacker hiểu sâu hơn về system và tìm kẽ hở khác.  
- Trường hợp có comment mô tả chi tiết kỹ thuật, kiến trúc hoặc các điểm chưa hoàn thiện có thể hỗ trợ attacker trong tấn công nâng cao.  
- Tuy nhiên, trong evidence chưa nhận thấy comment chứa dữ liệu nhạy cảm (mật khẩu, API keys, thông tin user, cấu hình bảo mật) nên mức độ ảnh hưởng trực tiếp là hạn chế.  
- Tổng thể, đây là vấn đề về vệ sinh code/source control hơn là lỗi bảo mật có thể khai thác ngay.

---

##### 4. Cách khắc phục cụ thể ở cấp cấu hình/root cause  
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

##### 5. Ghi chú tester cần kiểm tra thêm nếu chưa đủ context  
- Xác nhận chính xác môi trường ứng dụng đang chạy (dev, staging, production) và chính sách deploy code frontend tại từng môi trường.  
- Kiểm tra cấu hình build frontend để xác định có bật minify và loại bỏ comment hay không trong production.  
- Đánh giá các comment khác, nếu có comment chứa thông tin cấu hình bí mật, credential, hoặc thông tin nhạy cảm cần báo cáo nâng mức alert.  
- Thử kiểm tra theo cách manual hoặc với quyền không auth xem các resource này có bị phơi bày ra ngoài không (open access).  
- Đánh giá nguy cơ khi attacker có thể kết hợp các thông tin từ comment này với các lỗ hổng khác để khai thác sâu hơn.

---

**Tổng kết:**  
Alert này không phải lỗi bảo mật nghiêm trọng nhưng là dấu hiệu cảnh báo về việc vệ sinh code và cấu hình môi trường deploy frontend. Cần đánh giá kỹ tình huống thực tế để quyết định hành động tiếp theo.

### ZAP-014: Modern Web Application

#### Tags lỗi
| Thuộc tính | Giá trị |
|---|---|
| Plugin ID | `10109` |
| Alert Ref | `10109` |
| Risk | `Informational` |
| Confidence | `Medium` |
| CWE | N/A |
| WASC | N/A |
| Tags | POLICY_QA_STD, POLICY_PENTEST, SYSTEMIC, POLICY_DEV_STD |
| Source JSON | `frontend_admin_basic.json`, `frontend_user_basic.json` |
| Site | `http://localhost:5173`, `http://localhost:5174` |

#### Thông tin alert nhóm
- Số endpoint/request instance bị ảnh hưởng: 14
- Phân loại AI: Needs Human Review
- Trạng thái kiểm chứng thủ công: Chưa kiểm chứng

#### Endpoints bị ảnh hưởng
| # | Method | URL | Param | Evidence |
|---|---|---|---|---|
| 47 | GET | `http://localhost:5173` | `N/A` | `<script type="module">import { injectIntoGlobalHook } from "/@react-refresh"; injectIntoGlobalHook(window); window.$RefreshReg$ = () => {}; window.$RefreshSig$ = () => (type) => type;</script>` |
| 48 | GET | `http://localhost:5173/` | `N/A` | `<script type="module">import { injectIntoGlobalHook } from "/@react-refresh"; injectIntoGlobalHook(window); window.$RefreshReg$ = () => {}; window.$RefreshSig$ = () => (type) => type;</script>` |
| 49 | GET | `http://localhost:5173/forgot-password` | `N/A` | `<script type="module">import { injectIntoGlobalHook } from "/@react-refresh"; injectIntoGlobalHook(window); window.$RefreshReg$ = () => {}; window.$RefreshSig$ = () => (type) => type;</script>` |
| 50 | GET | `http://localhost:5173/robots.txt` | `N/A` | `<script type="module">import { injectIntoGlobalHook } from "/@react-refresh"; injectIntoGlobalHook(window); window.$RefreshReg$ = () => {}; window.$RefreshSig$ = () => (type) => type;</script>` |
| 51 | GET | `http://localhost:5173/sitemap.xml` | `N/A` | `<script type="module">import { injectIntoGlobalHook } from "/@react-refresh"; injectIntoGlobalHook(window); window.$RefreshReg$ = () => {}; window.$RefreshSig$ = () => (type) => type;</script>` |
| 97 | GET | `http://localhost:5174` | `N/A` | `<script type="module">import { injectIntoGlobalHook } from "/@react-refresh"; injectIntoGlobalHook(window); window.$RefreshReg$ = () => {}; window.$RefreshSig$ = () => (type) => type;</script>` |
| 98 | GET | `http://localhost:5174/` | `N/A` | `<script type="module">import { injectIntoGlobalHook } from "/@react-refresh"; injectIntoGlobalHook(window); window.$RefreshReg$ = () => {}; window.$RefreshSig$ = () => (type) => type;</script>` |
| 99 | GET | `http://localhost:5174/robots.txt` | `N/A` | `<script type="module">import { injectIntoGlobalHook } from "/@react-refresh"; injectIntoGlobalHook(window); window.$RefreshReg$ = () => {}; window.$RefreshSig$ = () => (type) => type;</script>` |
| 100 | GET | `http://localhost:5174/sitemap.xml` | `N/A` | `<script type="module">import { injectIntoGlobalHook } from "/@react-refresh"; injectIntoGlobalHook(window); window.$RefreshReg$ = () => {}; window.$RefreshSig$ = () => (type) => type;</script>` |
| 125 | GET | `http://localhost:5173` | `N/A` | `<script type="module">import { injectIntoGlobalHook } from "/@react-refresh"; injectIntoGlobalHook(window); window.$RefreshReg$ = () => {}; window.$RefreshSig$ = () => (type) => type;</script>` |
| 126 | GET | `http://localhost:5173/` | `N/A` | `<script type="module">import { injectIntoGlobalHook } from "/@react-refresh"; injectIntoGlobalHook(window); window.$RefreshReg$ = () => {}; window.$RefreshSig$ = () => (type) => type;</script>` |
| 127 | GET | `http://localhost:5173/forgot-password` | `N/A` | `<script type="module">import { injectIntoGlobalHook } from "/@react-refresh"; injectIntoGlobalHook(window); window.$RefreshReg$ = () => {}; window.$RefreshSig$ = () => (type) => type;</script>` |
| 128 | GET | `http://localhost:5173/robots.txt` | `N/A` | `<script type="module">import { injectIntoGlobalHook } from "/@react-refresh"; injectIntoGlobalHook(window); window.$RefreshReg$ = () => {}; window.$RefreshSig$ = () => (type) => type;</script>` |
| 129 | GET | `http://localhost:5173/sitemap.xml` | `N/A` | `<script type="module">import { injectIntoGlobalHook } from "/@react-refresh"; injectIntoGlobalHook(window); window.$RefreshReg$ = () => {}; window.$RefreshSig$ = () => (type) => type;</script>` |

#### Bằng chứng runtime đại diện

Request:
```http
GET http://localhost:5173 HTTP/1.1
host: localhost:5173
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36
pragma: no-cache
cache-control: no-cache
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Miwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODQ3MDk1NzF9.6xPB8cUE63QhefuiiRzG56zhdFE5lbB-b7dUFPwWED0
```

Request body:
```text
[Không có request body]
```

Response:
```http
HTTP/1.1 200 OK
Vary: Origin
Content-Type: text/html
Cache-Control: no-cache
Etag: W/"26b-Z6hN2DmQRHNqdtv4bv5lcx2QtJk"
Date: Wed, 22 Jul 2026 08:39:33 GMT
Connection: keep-alive
Keep-Alive: timeout=5
Content-Length: 619
```

Response body excerpt:
```text
<!doctype html>
<html lang="en">
  <head>
    <script type="module">import { injectIntoGlobalHook } from "/@react-refresh";
injectIntoGlobalHook(window);
window.$RefreshReg$ = () => {};
window.$RefreshSig$ = () => (type) => type;</script>

    <script type="module" src="/@vite/client"></script>

    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>frontend-web</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
```

#### Phân tích AI
1. **Phân loại:** Needs Human Review

2. **Lý do phân loại dựa trên runtime evidence của cả nhóm endpoint:**

   - Tất cả các endpoint bị quét đều trả về HTML dạng trang web hiện đại sử dụng React với Vite, có chứa script liên quan đến `/@react-refresh` (đây là cơ chế hỗ trợ hot-reload trong dev environment của Vite).
   - Alert ZAP-014 "Modern Web Application" là dạng cảnh báo mang tính thông tin (Informational), chỉ báo ứng dụng đang sử dụng công nghệ frontend hiện đại.
   - Không có bằng chứng nào cho thấy phản hồi chứa dữ liệu nhạy cảm hay hành vi có thể khai thác.
   - Các endpoint có cả `/robots.txt` và `/sitemap.xml` cũng được trả về một HTML có chứa script dev, điều này không phải là hành vi chuẩn khi cung cấp tệp cấu hình cho robot tìm kiếm.
   - Các response header và body cho thấy đây là môi trường localhost, rất có thể là environment dev hoặc staging, khi Vite dev server đang bật feature hot-reload.
   - Mức độ rủi ro được ZAP đánh giá là Informational và độ tin cậy Medium.
   - Từ evidence không đủ khẳng định đây là lỗ hổng bảo mật kiểu True Positive, cũng không phải là False Positive vì không xác định được hành vi của hệ thống trong môi trường production.
   - Cần xác nhận thêm thông tin về môi trường triển khai (dev/prod) để định hướng xử lý.

3. **Tác động thực tế trong bối cảnh EShop:**

   - Nếu đây là môi trường development hoặc staging thì việc xuất hiện các script hot-reload như vậy là bình thường, không phải vấn đề bảo mật.
   - Nếu môi trường production cũng trả về các trang chứa script dev như trên thì có thể lộ thông tin nội bộ, gây ảnh hưởng về mặt bảo mật (ví dụ attacker biết được framework dev, dễ dàng khai thác).
   - Việc trả về script hot-reload trên các endpoint không liên quan như `/robots.txt` và `/sitemap.xml` là bất thường, có thể gây nhầm lẫn cho bot tìm kiếm hoặc client.
   - Không có dấu hiệu rò rỉ thông tin nhạy cảm hoặc lỗi cấu hình nghiêm trọng khác.

4. **Cách khắc phục cụ thể ở cấp cấu hình/root cause:**

   - Xác định rõ môi trường deploy:
     - Môi trường production phải build frontend ở chế độ production (`vite build`) để loại bỏ các script dev như `/@react-refresh` và `/@vite/client`.
     - Đảm bảo server trả đúng nội dung tĩnh cho các endpoint đặc thù như `/robots.txt`, `/sitemap.xml` theo chuẩn định dạng text/plain hoặc xml chuẩn, không trả HTML chứa script dev.
   - Tắt hoặc giới hạn truy cập các tính năng dev server khi deploy ngoài môi trường local.
   - Kiểm soát chính xác `Content-Type` header trong response cho các file đặc thù.
   - Thiết lập cơ chế cache phù hợp ở production để tránh việc tải lại script dev không cần thiết.

5. **Ghi chú tester cần kiểm tra thêm nếu chưa đủ context:**

   - Xác nhận môi trường deploy hiện tại của EShop có phải là production hay chưa; alert này có thể không áp dụng nếu đang chạy ở môi trường local/dev.
   - Kiểm tra chi tiết cách build/upload frontend cho môi trường sản xuất, cụ thể xem các endpoint có trả về đúng file tĩnh đã build hay vẫn đang phục vụ dev server.
   - Kiểm tra thêm response header `Content-Type` và các header bảo mật khác (Content-Security-Policy, X-Frame-Options...) để đánh giá mặt bảo mật tổng thể.
   - Đánh giá liệu việc để các file dev tồn tại trên môi trường ngoài local có khả năng bị attacker khai thác không (ví dụ: từ các thông tin framework, phiên bản, công cụ debug).
   - Đối chiếu thêm với team phát triển frontend để xác định quy trình build/deploy đã đúng chuẩn chưa.

## Checklist kiểm chứng thủ công

- Xác nhận URL có thuộc target scan cần báo cáo hay không.
- Replay request với cùng method, headers, payload và auth context.
- Đối chiếu evidence trong response mới với evidence mà ZAP đã ghi nhận.
- Kiểm tra các alert trùng root cause để gom lại khi viết báo cáo cuối.
- Chỉ chốt `True Positive`, `False Positive`, hoặc `Needs Human Review` sau khi có đủ runtime context.
