Tôi dùng OWASP ZAP (DAST) để quét runtime của ứng dụng EShop và phát hiện một nhóm alert bảo mật cùng loại.
Bạn hãy đóng vai trò là chuyên gia bảo mật ứng dụng để triage alert này ở cấp nhóm, không lặp lại phân tích riêng cho từng endpoint nếu cùng root cause.
Hãy trả lời hoàn toàn bằng tiếng Việt, trừ các thuật ngữ chuẩn như True Positive, False Positive, Needs Human Review, CWE, WASC, OWASP, HTTP, header, payload.

Thông tin kỹ thuật:
- Mã alert: ZAP-012
- Alert name: Information Disclosure - Sensitive Information in URL
- Plugin ID: 10024
- Alert Ref: 10024
- Source JSON: frontend_admin_basic.json, frontend_user_basic.json
- Site: http://localhost:5173, http://localhost:5174
- Số endpoint/request instance bị ảnh hưởng: 3
- Risk: Informational
- Confidence: Medium
- CWE: CWE-598
- WASC: WASC-13
- Tags: CWE-598, OWASP_2021_A01, POLICY_QA_STD, POLICY_PENTEST, SYSTEMIC, OWASP_2017_A03, OWASP_2025_A01, POLICY_DEV_STD

Danh sách endpoint bị ảnh hưởng:
| # | Method | URL | Param | Evidence | Source JSON |
|---|---|---|---|---|---|
| 40 | GET | `http://localhost:5173/?token=7NvYDWb8HNrK` | `token` | `token` | `frontend_user_basic.json` |
| 92 | GET | `http://localhost:5174/?token=-LYBc--RLYE6` | `token` | `token` | `frontend_admin_basic.json` |
| 118 | GET | `http://localhost:5173/?token=7NvYDWb8HNrK` | `token` | `token` | `frontend_admin_basic.json` |

Bằng chứng request/response runtime đại diện:
### Endpoint 40: GET http://localhost:5173/?token=7NvYDWb8HNrK

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

### Endpoint 92: GET http://localhost:5174/?token=-LYBc--RLYE6

Request:
```http
GET http://localhost:5174/?token=-LYBc--RLYE6 HTTP/1.1
host: localhost:5174
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Sec-WebSocket-Version: 13
Origin: http://localhost:5174
Sec-WebSocket-Protocol: vite-hmr
Sec-WebSocket-Key: uk3FWrFnEOIA81mQHh5Ztw==
Connection: Upgrade
Pragma: no-cache
Cache-Control: no-cache
Upgrade: websocket
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwicm9sZSI6ImFkbWluIiwiaWF0IjoxNzg0NzEwMjQ3fQ.4xCcBJucuQGSSMaZk6kIQ6yq2kqhbQn6WLb0s-kCOEU
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
Sec-WebSocket-Accept: N9ytJ78N72Eqg/lKs1SCs0BuTPk=
Sec-WebSocket-Protocol: vite-hmr
```

Response body excerpt:
```text
[Không có response body]
```

### Endpoint 118: GET http://localhost:5173/?token=7NvYDWb8HNrK

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

Mô tả ZAP:
The request appeared to contain sensitive information leaked in the URL. This can violate PCI and most organizational compliance policies. You can configure the list of strings for this check to add or remove values specific to your environment.

Khuyến nghị ZAP:
Do not pass sensitive information in URIs.

Tham khảo:
N/A

Ngữ cảnh runtime cho triage động:
- ZAP là DAST: phân loại dựa trên request/response runtime mà scanner quan sát được.
- ZAP không chỉ ra dòng code. Không suy đoán root cause trong code nếu evidence HTTP chưa đủ.
- True Positive: runtime evidence cho thấy cấu hình/hành vi lỗi tồn tại trên endpoint được quét.
- False Positive: request/response cho thấy alert không áp dụng trong ngữ cảnh này hoặc là endpoint ngoài phạm vi.
- Needs Human Review: evidence thiếu auth context, thiếu business impact, hoặc chỉ là informational signal.
- Với alert Informational, chỉ nâng mức nghiêm trọng nếu response cho thấy dữ liệu nhạy cảm hoặc hành vi có thể khai thác.
- Với endpoint localhost/lab, vẫn đánh giá theo hành vi quan sát được nhưng ghi rõ cần xác nhận môi trường deploy.
- Evidence của ZAP phải được đối chiếu trực tiếp với response header/body trong report.

Hãy trả lời bằng Markdown với các mục:
1. Phân loại: True Positive / False Positive / Needs Human Review.
2. Lý do phân loại dựa trên runtime evidence của cả nhóm endpoint.
3. Tác động thực tế trong bối cảnh EShop.
4. Cách khắc phục cụ thể ở cấp cấu hình/root cause.
5. Ghi chú tester cần kiểm tra thêm nếu chưa đủ context.
