# [AI-02] Báo Cáo Audit AI - Group 06

## 1. Thông Tin Nhóm

- Nhóm: Group 06 - KDBK
- Đề tài: T09 - Security Testing (DAST / SAST)
- Seminar track: Security testing với Semgrep/SAST, OWASP ZAP/DAST và AI-assisted triage.
- Thành viên:
  - Lê Trung Kiên
  - Mai Thị Kim Duyên
  - Lâm Hữu Khánh
  - Lê Mai Hoài Bảo
- Phạm vi audit: các nội dung AI hỗ trợ trong quá trình chọn công cụ, viết script Semgrep/ZAP, phân tích finding, tạo PoC/checklist kiểm chứng và biên tập report.
- Nguyên tắc đánh giá: AI output chỉ được xem là hợp lệ khi có human review và được đối chiếu với source code, output Semgrep/ZAP, unit test, request/response log, screenshot hoặc tài liệu chính thức.

## 2. Bảng Audit

### Mục 1 - Semgrep Hardcoded JWT Secret: PoC Forge Token

#### 1. Prompt + công cụ AI

- Công cụ theo W05:
  - ChatGPT/Gemini cho Lâm Hữu Khánh.
  - Google Gemini 3.1 Flash cho Lê Mai Hoài Bảo.
- Prompt theo weekly report:

```text
Yêu cầu AI hỗ trợ rà soát phần Semgrep SAST, kiểm tra finding `hardcoded-jwt-secret`, giải thích nguy cơ hardcoded JWT secret, gợi ý PoC tạo JWT giả mạo và đề xuất hướng khắc phục bằng biến môi trường.
```

```text
Yêu cầu AI phân tích finding `hardcoded-jwt-secret` từ kết quả Semgrep và hỗ trợ điền `Track_A_Semgrep_Template.md`.
```

- Prompt chi tiết lưu tại: `src/semgrep/output/findings/001_javascript-jsonwebtoken-security-jwt-hardcode-hardcoded-jwt-secret_prompt.md`

#### 2. Nội dung AI hỗ trợ

AI output gốc lưu tại:

- `src/semgrep/output/findings/001_javascript-jsonwebtoken-security-jwt-hardcode-hardcoded-jwt-secret_ai_output.md`
- `docs/semgrep/AI_Triage_hardcoded-jwt-secret.md`

Phần PoC/ý tưởng kiểm chứng AI gợi ý:

```text
Mục tiêu: Chứng minh rằng kẻ tấn công có thể sử dụng khóa bí mật bị lộ để tạo JWT giả mạo và xác thực thành công vào hệ thống.

Kịch bản:
1. Xác định khóa bí mật: Truy cập vào mã nguồn của EShop, tìm đến file `eshop-sut/backend/server.js` và lấy giá trị của `SECRET_KEY` tại dòng 51. Giả sử `SECRET_KEY` là `"mySuperSecretKey123!"`.
2. Tạo JWT giả mạo với payload `{"id": "999", "role": "admin"}`.
3. Gửi token trong header `Authorization` của request đến API EShop.

Kết quả mong đợi: Nếu ứng dụng không có các biện pháp kiểm tra bổ sung hoặc kiểm tra tính hợp lệ của `id`/`role` trước khi cấp quyền, token giả mạo có thể được xác thực là admin.
```

Screenshot: không có screenshot trực tiếp của AI output trong weekly report.

#### 3. Verdict

`INCOMPLETE`

Ý tưởng kiểm chứng đúng, nhưng bản AI ban đầu chưa đủ để dùng làm bằng chứng kiểm thử vì dùng secret giả định, endpoint kiểm chứng còn chung chung, và expected result có điều kiện "nếu..." nên oracle chưa dứt khoát.

#### 4. Lý do theo ISTQB

- Test objective rõ: kiểm tra authentication bypass/privilege escalation do hardcoded JWT secret.
- Test data chưa khớp SUT: AI dùng `"mySuperSecretKey123!"` thay vì secret thật trong evidence.
- Expected result chưa đo được bằng HTTP status/body cụ thể.
- Theo ISTQB, đây là phần đặc tả kiểm chứng chưa hoàn chỉnh: có ý tưởng kiểm thử, nhưng thiếu precondition, dữ liệu kiểm thử chính xác, bước execute cụ thể và oracle.
- Vì finding liên quan authentication/authorization, nên theo risk-based testing cần ưu tiên xác minh bằng PoC tái lập được.

#### 5. Nội dung đã được SV sửa hoặc bổ sung

Sinh viên đã sửa PoC bằng evidence thật trong `weekly-reports/Group06_05/evidence/semgrep/finding_hardcoded_jwt_secret.md` và `src/semgrep/exploit.js`:

```javascript
const jwt = require("jsonwebtoken");
const forgedToken = jwt.sign(
  { id: 1, role: "admin" },
  "super_secret_key_that_should_not_be_here"
);
console.log("Bearer " + forgedToken);
```

Bản đã sửa/bổ sung:

- Dùng secret thật: `super_secret_key_that_should_not_be_here`.
- Gộp các finding `server.js:9`, `server.js:51`, `server.js:105` thành 1 root cause.
- Bổ sung remediation: dùng `process.env.JWT_SECRET`, không commit `.env`, rotate token/secret cũ.
- Nên bổ sung thêm request runtime đến endpoint protected/admin với expected `200/403` trước và sau khi fix.

### Mục 2 - Semgrep Cleartext HTTP Request: Ý tưởng kiểm chứng bằng proxy

#### 1. Prompt + công cụ AI

- Công cụ theo W06: Codex/ChatGPT, OpenRouter, model Gemini qua OpenRouter `google/gemini-2.5-flash-lite`.
- Prompt theo weekly report:

```text
Yêu cầu AI sửa script để chạy tất cả findings theo số lượng lỗi trong JSON, không hardcode một lỗi.
```

```text
Yêu cầu AI đọc tài liệu Semgrep trong repo và hướng dẫn cách chạy Semgrep từ bước cài đặt, scan đến AI triage.
```

- Prompt chi tiết cho finding lưu tại: `src/semgrep/output/findings/004_typescript-react-security-react-insecure-request-react-insecure-request_prompt.md`

#### 2. Nội dung AI hỗ trợ

AI output gốc lưu tại:

- `src/semgrep/output/findings/004_typescript-react-security-react-insecure-request-react-insecure-request_ai_output.md`

Phần hướng dẫn kiểm chứng AI gợi ý:

```text
Yêu cầu công cụ:
* Một thiết bị chạy ứng dụng EShop hoặc trình giả lập.
* Một công cụ proxy mạng như Charles Proxy, mitmproxy, Fiddler.
* Cài đặt chứng chỉ của công cụ proxy trên thiết bị nếu cần xem HTTPS.

Các bước thực hiện:
1. Cấu hình proxy mạng.
2. Bật giám sát HTTP.
3. Chạy ứng dụng EShop và đăng nhập.
4. Truy cập màn hình danh sách đơn hàng.
5. Quan sát traffic trên proxy.
6. Nếu request gửi qua HTTP, kiểm tra header `Authorization`, query/body và response.
```

Screenshot: không có screenshot trực tiếp của AI output trong weekly report.

#### 3. Verdict

`INCOMPLETE`

Hướng kiểm chứng đúng nhưng chưa đủ để kết luận defect trong môi trường seminar. Weekly report chưa lưu giá trị runtime của `API_URL`, log proxy, screenshot request, hoặc expected result cụ thể.

#### 4. Lý do theo ISTQB

- Test objective có liên quan trực tiếp đến CWE-319 và nguy cơ lộ token qua HTTP.
- Precondition thiếu: chưa rõ build nào, `API_URL` nào, thiết bị/proxy nào, tài khoản test nào.
- Expected result chưa thành oracle: cần nêu rõ request phải dùng HTTPS hay HTTP, header nào được quan sát, response nào được coi là fail.
- Có nguy cơ false positive/environment noise vì local/dev có thể dùng HTTP có chủ đích.
- Cần bằng chứng confirmation testing: log proxy hoặc screenshot request/response.

#### 5. Nội dung đã được SV sửa hoặc bổ sung

Sinh viên đã bổ sung:

- `src/semgrep/output/semgrep_triage_report.md`: ghi 12 findings và để `Human Validation = Needs Manual Verification`.
- `weekly-reports/Group06_05/evidence/semgrep/failure_modes_metrics.md`: ghi rõ cần kết hợp DAST/ZAP và human audit.

Nội dung kiểm chứng nên chốt khi nộp:

```text
Verify mobile order API does not transmit Authorization token over cleartext HTTP
Precondition: EShop backend/frontend-mobile chạy với cấu hình demo; user test đã đăng nhập và có đơn hàng.
Steps:
1. Cấu hình emulator/device đi qua mitmproxy hoặc ZAP proxy.
2. Đăng nhập user test.
3. Mở màn hình My Orders.
4. Lọc request đến `/orders/my-orders`.
Expected:
- Với môi trường production/demo, request phải dùng HTTPS.
- Nếu request dùng HTTP và header `Authorization: Bearer ...` đọc được trên proxy thì mark Confirmed.
Evidence:
- Lưu proxy screenshot/log request + response header.
```

### Mục 3 - Semgrep AI Triage Workflow: Unit Tests Cho All Findings

#### 1. Prompt + công cụ AI

- Công cụ theo W06: Codex/ChatGPT, OpenRouter, model Gemini qua OpenRouter `google/gemini-2.5-flash-lite`.
- Prompt theo weekly report:

```text
Yêu cầu AI sửa cấu hình `.env.example` để dùng OpenRouter với model Gemini thay vì dùng trực tiếp `GEMINI_API_KEY`.
```

```text
Yêu cầu AI sửa script để đọc `OPENROUTER_API_KEY`/`OPENROUTER_BASE_URL`.
```

```text
Yêu cầu AI sửa script để chạy tất cả findings theo số lượng lỗi trong JSON, không hardcode một lỗi.
```

#### 2. Nội dung AI hỗ trợ

Nội dung liên quan được audit trong `src/semgrep/test_semgrep_ai_triage.py`:

```python
def test_collect_finding_records_keeps_all_findings_and_metadata(self):
    ...
    self.assertEqual(len(records), 2)
    self.assertEqual(records[0].rule_id, "rule.one")
    self.assertEqual(records[0].cwe, "CWE-798")
    self.assertEqual(records[0].owasp, "A07:2025")
    self.assertIn("SECRET_KEY", records[0].code)
    self.assertEqual(records[1].severity, "ERROR")

def test_get_ai_settings_supports_openrouter_variables(self):
    ...
    self.assertEqual(settings.provider, "openai-compatible")
    self.assertEqual(settings.model, "google/gemini-2.5-flash-lite")
    self.assertEqual(settings.api_key, "openrouter-key")
    self.assertEqual(settings.base_url, "https://openrouter.ai/api/v1")

def test_write_triage_outputs_creates_summary_and_per_finding_files(self):
    ...
    self.assertIn("semgrep_triage_report", report_path.name)
    self.assertIn("Human Validation", report)
    self.assertIn("const SECRET_KEY", prompt)
    self.assertIn("AI output body", ai_output)
```

Screenshot: không có screenshot trực tiếp của AI output trong weekly report.

#### 3. Verdict

`VALID`

Nhóm unit tests này hợp lệ ở mức component/unit testing. Test không gọi API thật, có fixture tối thiểu, có assertion rõ ràng và kiểm tra đúng regression quan trọng: không hardcode một finding, giữ metadata, tạo output prompt/AI-output riêng.

#### 4. Lý do theo ISTQB

- Test level phù hợp: component test cho parser/config/output writer.
- Test độc lập với external services, credentials và network.
- Có expected result cụ thể bằng assertions.
- Có regression value cao cho lỗi W06: script phải xử lý đủ số lượng findings trong JSON.
- Giới hạn còn lại: chưa phải system test với OpenRouter live, nhưng điều này chấp nhận được cho unit test.

#### 5. Nội dung đã được SV sửa hoặc bổ sung

Sinh viên đã bổ sung:

- `src/semgrep/test_semgrep_ai_triage.py`
- `src/semgrep/output/semgrep_triage_report.md`
- `src/semgrep/output/findings/*_prompt.md`
- `src/semgrep/output/findings/*_ai_output.md`

Kết quả kỳ vọng của bản đã sửa:

- Input có 12 findings thì report ghi `Total findings in input: 12`.
- Mỗi finding có prompt và AI output riêng.
- Finding chưa được human validate thì giữ trạng thái `Needs Manual Verification`, không tự động kết luận confirmed.

### Mục 4 - ZAP Offline AI Triage: HTML Parsing, XSS/CORS

#### 1. Prompt + công cụ AI

- Công cụ theo W05: ChatGPT, model GPT-5.5 cho Lê Trung Kiên.
- Prompt theo weekly report:

```text
Yêu cầu AI hỗ trợ viết script đọc output scan OWASP ZAP, tạo báo cáo AI triage và gợi ý prompt phân tích alert/impact/PoC/fix.
```

- Evidence liên quan:
  - `docs/zap/test_ai_triage_zap.py`
  - `docs/zap/ai_triage_zap.py`
  - `docs/zap/output/backend_report_ai_triage.md`

#### 2. Nội dung AI hỗ trợ

Nội dung liên quan được audit trong `docs/zap/test_ai_triage_zap.py`:

```python
def test_parse_zap_html_extracts_alert_from_table_report(self):
    alerts = parse_zap_html(SAMPLE_REPORT)
    self.assertEqual(len(alerts), 1)
    self.assertEqual(alerts[0].name, "Cross Site Scripting (DOM Based)")
    self.assertEqual(alerts[0].risk, "High")
    self.assertEqual(alerts[0].confidence, "High")
    self.assertEqual(alerts[0].method, "GET")
    self.assertEqual(alerts[0].parameter, "name")
    self.assertIn("onerror=alert(1)", alerts[0].evidence)

def test_offline_triage_includes_poc_and_testcase_for_xss(self):
    ...
    self.assertIn("DOM XSS", triage)
    self.assertIn("PoC", triage)
    self.assertIn("Testcase", triage)

def test_parse_zap_html_extracts_alert_from_classic_report(self):
    ...
    self.assertEqual(alerts[0].name, "Cross-Domain Misconfiguration")
    self.assertEqual(alerts[0].risk, "Medium")
    self.assertEqual(alerts[0].parameter, "Access-Control-Allow-Origin")
    self.assertEqual(alerts[0].evidence, "Access-Control-Allow-Origin: *")
```

Screenshot: không có screenshot trực tiếp của AI output trong weekly report.

#### 3. Verdict

`VALID`

Nhóm unit tests này hợp lệ để kiểm tra parser và renderer của ZAP AI triage. Mẫu HTML nhỏ nhưng có coverage cho hai dạng report, có assert field-level và có assert triage offline tạo PoC/checklist kiểm chứng cho XSS.

#### 4. Lý do theo ISTQB

- Test objective rõ: verify HTML parser extract đúng alert fields và offline triage tạo nội dung cần thiết.
- Test data có tính đại diện: table report và classic report.
- Expected result cụ thể: số lượng alert, field-level assertions, output markdown sections.
- Không cần live ZAP vì mục tiêu là component parser test.
- Giới hạn: chưa kiểm tra hết các biến thể HTML report thật của ZAP, nên cần thêm regression test nếu template report thay đổi.

#### 5. Nội dung đã được SV sửa hoặc bổ sung

Sinh viên đã bổ sung:

- `docs/zap/test_ai_triage_zap.py`
- `docs/zap/output/backend_report_ai_triage.md`
- `docs/zap/scan_ai_triage_guide.md`

Bản đã sửa giữ offline triage khi không có API key, giúp test deterministic và repeatable theo đúng kỳ vọng của automated regression test.

### Mục 5 - ZAP CLI Scan Mode, Report Format, Output Path

#### 1. Prompt + công cụ AI

- Công cụ theo W06: Codex, model GPT-5.4 và GPT-5.5.
- Prompt theo weekly report:

```text
Yêu cầu AI thêm cờ để ZAP chạy theo `basic` hoặc `owasp-top10-2025`, nhưng vẫn giữ nguyên nguyên tắc ZAP scan toàn bộ và chỉ lọc active policy theo tag/rule tương ứng khi cần.
```

```text
Yêu cầu AI thêm tùy chọn cho người dùng tự chọn path và tên file output, phục vụ tách report cho frontend user, frontend admin hoặc backend.
```

```text
Yêu cầu AI đổi output report từ chỉ HTML sang cho phép xuất JSON để pipeline sau này có thể đọc bằng AI và đối chiếu với PoC từ Semgrep.
```

#### 2. Nội dung AI hỗ trợ

Nội dung liên quan được audit trong `src/zap/test_scan_zap.py`:

```python
def test_output_file_alias_selects_report_path(self):
    args = build_parser(load_env=False).parse_args(
        ["--output-file", "src/zap/output/frontend_user.html"]
    )
    self.assertEqual(args.report_file, "src/zap/output/frontend_user.html")

def test_parser_rejects_non_pipeline_report_formats(self):
    for report_format in ("xml", "md"):
        with self.subTest(report_format=report_format):
            with self.assertRaises(SystemExit):
                build_parser(load_env=False).parse_args(
                    ["--report-format", report_format]
                )

def test_configure_scan_policy_creates_owasp_top10_2025_policy_from_alert_tags(self):
    ...
    zap.ascan.enable_scanners.assert_called_once_with(
        "40012,40018",
        scanpolicyname=OWASP_TOP10_2025_POLICY_NAME,
    )
```

Screenshot: không có screenshot trực tiếp của AI output trong weekly report.

#### 3. Verdict

`VALID`

Đây là nhóm regression tests hợp lệ cho CLI behavior và scan policy configuration. Test có oracle rõ, dùng mock ZAP API, không cần live daemon, và trace được tới yêu cầu W06 về `basic`, `owasp-top10-2025`, `html/json`, `--output-file`.

#### 4. Lý do theo ISTQB

- Có traceability giữa requirement và test.
- Có negative testing: reject `xml`, `md`; reject trường hợp không có scanner OWASP matching.
- Có robustness testing: fallback khi ZAP API không trả alert tags.
- Mock giúp test nhanh, ổn định, không phụ thuộc ZAP daemon.
- Cần thêm smoke/system test với ZAP daemon thật để xác nhận official template có sẵn trong image.

#### 5. Nội dung đã được SV sửa hoặc bổ sung

Sinh viên đã bổ sung:

- `src/zap/test_scan_zap.py`
- `src/zap/scan_zap.py`
- `src/zap/README.md`

Bản đã sửa:

- `--report-format` chỉ nhận `html` hoặc `json`.
- `--output-file` là alias của `--report-file`.
- `basic` giữ default enabled rules.
- `owasp-top10-2025` lọc active scanner theo tag `OWASP_2025_A*`, có fallback theo rule ID nếu ZAP API không trả tag.

### Mục 6 - ZAP Authenticated Scan: JWT, Context, Replacer, Cleanup

#### 1. Prompt + công cụ AI

- Công cụ theo W06: Google Gemini, model Gemini 3.1 Pro.
- Prompt theo weekly report:

```text
Yêu cầu AI sinh mã cấu hình authenticated scan cho ZAP trên EShop, bao gồm đăng nhập lấy JWT, cấu hình context, user, forced-user và gắn `Authorization: Bearer ...` khi scan.
```

```text
Yêu cầu AI gợi ý cách dùng AJAX Spider cho frontend SPA và cách giới hạn scope chỉ trong các URL local của EShop.
```

```text
Yêu cầu AI giải thích vì sao login qua ZAP có thể trả `401` hoặc `403`, sau đó đối chiếu lại với tài khoản test và cơ chế proxy của ZAP.
```

#### 2. Nội dung AI hỗ trợ

Nội dung liên quan được audit trong `src/zap/test_zap_runtime.py` và `src/zap/test_scan_zap.py`:

```python
def test_validate_target_accepts_eshop_local_ports(self):
    for url in (
        "http://localhost:3000",
        "http://localhost:5173/",
        "http://127.0.0.1:5174/admin",
    ):
        with self.subTest(url=url):
            self.assertEqual(validate_target(url), url)

def test_validate_target_rejects_external_or_unknown_port(self):
    for url in ("https://example.com", "http://localhost:8080"):
        with self.subTest(url=url):
            with self.assertRaisesRegex(ValueError, "local EShop"):
                validate_target(url)

def test_configure_authenticated_context_creates_scoped_user_and_replacer(self):
    ...
    zap.replacer.add_rule.assert_called_once_with(
        REPLACER_RULE,
        "true",
        "REQ_HEADER",
        "false",
        "Authorization",
        "Bearer jwt-value",
        url=CONTEXT_REGEX,
    )

def test_cleanup_removes_secret_and_disables_forced_user(self):
    cleanup_authenticated_context(zap, forced_user=True)
    zap.replacer.remove_rule.assert_called_once_with(REPLACER_RULE)
    zap.forcedUser.set_forced_user_mode_enabled.assert_called_once_with("false")
```

Screenshot: không có screenshot trực tiếp của AI output trong weekly report.

#### 3. Verdict

`VALID`

Nhóm unit tests hợp lệ cho component/integration-with-mocks. Test kiểm tra các đường an toàn quan trọng: chỉ scan target local, không đẩy credential qua remote ZAP, inject JWT qua Replacer, bật/tắt Forced User Mode và cleanup secret.

#### 4. Lý do theo ISTQB

- Test objective gắn với security control: authenticated scan phải đúng context/scope và không làm lộ credential.
- Có negative testing cho URL ngoài, malformed port, remote ZAP URL.
- Có oracle cụ thể trên API call của ZAP mock.
- Có test cleanup, quan trọng vì JWT là sensitive test data.
- Cần manual/live verification riêng cho lỗi `401/403` và coverage AJAX Spider.

#### 5. Nội dung đã được SV sửa hoặc bổ sung

Sinh viên đã bổ sung:

- `src/zap/zap_runtime.py`
- `src/zap/test_zap_runtime.py`
- `src/zap/test_scan_zap.py`
- `src/zap/README.md`

Bản đã sửa:

- `validate_target()` chỉ cho `localhost`/`127.0.0.1` trên port `3000`, `5173`, `5174`.
- Authenticated scan chỉ chấp nhận ZAP daemon local HTTP.
- `login_for_token()` đi qua ZAP proxy và không in JWT ra stdout/stderr.
- `cleanup_authenticated_context()` xóa Replacer rule và tắt Forced User Mode.

### Mục 7 - ZAP JSON -> OpenRouter: PoC Extraction Và AI Report

#### 1. Prompt + công cụ AI

- Công cụ: Codex/OpenRouter, model `google/gemini-2.5-flash`.
- Prompt trong design/source:

```text
Create a CLI script that reads one or more OWASP ZAP JSON reports from `src/zap/output`, sends the parsed alert instances to OpenRouter using a Gemini model, and writes a user-selected Markdown or HTML report.
```

- Evidence:
  - `src/zap/test_zap_ai_triage.py`
  - `src/zap/output/zap_ai_triage_report.md`

#### 2. Nội dung AI hỗ trợ

Nội dung liên quan được audit trong `src/zap/test_zap_ai_triage.py`:

```python
def test_parse_multiple_json_files_extracts_every_alert_instance_and_tags(self):
    ...
    alerts = parse_zap_json_files([first, second])
    self.assertEqual(len(alerts), 3)
    self.assertEqual(alerts[0].alert_name, "SQL Injection")
    self.assertEqual(alerts[0].risk, "High")
    self.assertEqual(alerts[0].owasp_tags, ["OWASP_2021_A03"])
    self.assertEqual(alerts[0].poc["method"], "GET")
    self.assertEqual(alerts[0].poc["payload"], "' OR '1'='1")

def test_build_prompt_contains_required_sections_for_ai(self):
    ...
    self.assertIn("Chi tiết + giải thích lỗi", prompt)
    self.assertIn("Tag OWASP", prompt)
    self.assertIn("PoC", prompt)
    self.assertIn("Cách verify PoC", prompt)
    self.assertIn("OWASP_2021_A01", prompt)
    self.assertNotIn("CWE-264", prompt)
```

AI output report có ví dụ verify PoC trong `src/zap/output/zap_ai_triage_report.md`:

```text
PoC (Proof of Concept):
- Method: `GET`
- Endpoint: `http://localhost:3000`
- Payload: (Không có payload cụ thể)
- Notes: Thực hiện lại yêu cầu GET và kiểm tra các header/body phản hồi.

Cách verify PoC:
1. Mở Postman hoặc công cụ tương tự.
2. Tạo một yêu cầu `GET` đến `http://localhost:3000`.
3. Gửi yêu cầu.
4. Expected: Trong phần header phản hồi, tìm kiếm header `Access-Control-Allow-Origin`. Giá trị của nó là `*`.
5. Actual: Header `Access-Control-Allow-Origin: *` được tìm thấy.
6. Header/Body cần kiểm tra: `Access-Control-Allow-Origin` trong response header.
```

Screenshot: không có screenshot trực tiếp của AI output trong weekly report.

#### 3. Verdict

`INCOMPLETE`

Unit tests cho parser/prompt/rendering là tốt, nhưng AI-generated report vẫn cần audit lại trước khi dùng làm evidence cuối. Output có tag `OWASP_22021_A01` sai chính tả, nhiều CSP alerts bị lặp root cause, và phần "Actual" được ghi như đã verify nhưng không kèm log/screenshot Postman.

#### 4. Lý do theo ISTQB

- Parser unit tests có expected result rõ, nhưng report AI là test procedure/bug report nên cần evidence execute riêng.
- Theo ISTQB, actual result chỉ được ghi sau khi đã execute test.
- Cần traceability từ ZAP JSON instance -> PoC -> request/response log -> observed header.
- Cần defect deduplication: nhiều CSP alerts trên nhiều URL có thể là một root cause header policy.
- Sai taxonomy/tag OWASP là lỗi chất lượng dữ liệu trong output AI.

#### 5. Nội dung đã được SV sửa hoặc bổ sung

Sinh viên đã bổ sung:

- `src/zap/test_zap_ai_triage.py`
- `src/zap/zap_ai_triage.py`
- `src/zap/output/zap_ai_triage_report.md`

Nội dung kiểm chứng nên sửa trước khi nộp:

```text
Verify CORS wildcard header on backend
Precondition: backend EShop running at http://localhost:3000; ZAP/Postman available.
Steps:
1. Send GET http://localhost:3000 with Origin: http://evil.example.
2. Inspect response header.
Expected:
- If Access-Control-Allow-Origin is `*`, finding is Confirmed only when endpoint can expose sensitive data or credentials are allowed in a risky way.
- If no wildcard header or endpoint is public/static only, mark Needs Manual Verification or Environment Noise.
Evidence:
- Attach raw request/response headers or screenshot.
```

### Mục 8 - Semgrep AI Triage Refinement Trong Phiên Chat: Source Context, Fail-Fast, Report Format

#### 1. Prompt + công cụ AI

- Công cụ: Codex/ChatGPT trong phiên làm việc trực tiếp với repository.
- Các yêu cầu chính từ phiên chat:

```text
Sửa context là đọc source sau đó phân loại true/false/need human review.
```

```text
Nếu gọi AI bị lỗi thì cho nó fail hoặc stop chứ không cho gen ra các finding.
```

```text
Hãy xem xét các output của AI là tiếng Việt nhé.
```

```text
Hãy bỏ script tạo postman validation, thêm script tạo bảng test case có include tới finding nào.
```

```text
Test case làm theo từng entry chứ không sinh ra bảng.
```

```text
Mỗi entry trong semgrep_triage_report thêm tag lỗi CWE/OWASP.
```

```text
Format lại semgrep_triage_report để heading AI kiểu ## Triage Finding không làm mất cân đối.
```

```text
Bảng trong semgrep_triage_report dùng tiếng Việt, trừ tên tag lỗi.
```

#### 2. Nội dung AI hỗ trợ

AI đã hỗ trợ chỉnh workflow Semgrep trong `src/semgrep/semgrep_ai_triage.py` và tài liệu `submission/User_Guide.md`.

Các thay đổi kỹ thuật chính:

- Prompt AI yêu cầu đọc source evidence trước khi phân loại.
- Chỉ dùng ba trạng thái triage: `True Positive`, `False Positive`, `Needs Human Review`.
- AI output yêu cầu viết bằng tiếng Việt, trừ thuật ngữ chuẩn như `CWE`, `OWASP`, `True Positive`.
- Thêm giới hạn `AI_MAX_TOKENS` để tránh lỗi request quá lớn qua OpenRouter.
- Nếu AI provider lỗi, ví dụ OpenRouter `402`, script dừng với exit code `1` và không sinh report thiếu phân tích.
- Bỏ report Postman validation cũ, thay bằng `semgrep_test_cases.md` dạng từng entry test case.
- `semgrep_triage_report.md` có tag lỗi trong từng finding entry: `Rule`, `Severity`, `CWE`, `OWASP`, `Likelihood`, `Impact`, `Confidence`.
- Heading do AI sinh ra khi nhúng inline vào report được hạ cấp để không phá hierarchy Markdown.
- Bảng tổng hợp trong `semgrep_triage_report.md` dùng tiếng Việt: `Quy tắc`, `Tệp`, `Mức độ`, `Kết quả AI`, `Trạng thái kiểm chứng`.

Các regression tests liên quan trong `src/semgrep/test_semgrep_ai_triage.py`:

```python
def test_build_prompt_includes_source_first_three_state_classification_context(self):
    ...
    self.assertIn("Đọc và đối chiếu source evidence trước khi phân loại", prompt)
    self.assertIn("Phân loại: True Positive / False Positive / Needs Human Review", prompt)
    self.assertNotIn("PoC hoặc testcase kiểm chứng", prompt)

def test_main_stops_without_writing_reports_when_ai_call_fails(self):
    ...
    self.assertEqual(exit_code, 1)
    write_mock.assert_not_called()

def test_write_triage_outputs_creates_test_case_entries_report(self):
    ...
    self.assertIn("## TC-SEMGREP-001", report)
    self.assertIn("### Input", report)
    self.assertIn("### Thao tác", report)
    self.assertNotIn("### Expected output", report)
    self.assertNotIn("### Actual output", report)

def test_triage_report_detail_entries_include_security_tags(self):
    ...
    self.assertIn("#### Tags lỗi", report)
    self.assertIn("`CWE-798: Use of Hard-coded Credentials`", report)
    self.assertIn("`A07:2021 - Identification and Authentication Failures`", report)

def test_triage_report_demotes_ai_headings_inside_finding_details(self):
    ...
    self.assertNotIn("\n## Triage Finding Bảo Mật SEMGREP-001", report)
    self.assertIn("\n##### Triage Finding Bảo Mật SEMGREP-001", report)
```

Verification đã chạy trong phiên:

```bash
python3 -m unittest discover -s src/semgrep -p 'test_*.py'
```

Kết quả cuối cùng: `Ran 15 tests ... OK`.

#### 3. Verdict

`VALID`

Các chỉnh sửa này hợp lệ ở mức workflow/component regression vì có test tự động bảo vệ những yêu cầu chính: source-first context, phân loại ba trạng thái, fail-fast khi AI lỗi, không sinh Postman validation report cũ, test case dạng entry, tag CWE/OWASP trong report và format Markdown không bị lệch heading.

#### 4. Lý do theo ISTQB

- Traceability rõ từ yêu cầu trong phiên chat đến test case tự động.
- Có negative/regression testing cho lỗi provider: script không sinh report khi AI lỗi.
- Có test oracle cụ thể bằng assertion trên output Markdown.
- Giảm nguy cơ false evidence: AI không tự sinh "Actual result" hoặc finding khi provider lỗi.
- Tách vai trò hợp lý: AI phân tích finding, còn test case kiểm chứng nằm ở file riêng để tester thực thi và điền kết quả.
- Giới hạn còn lại: regression tests xác minh format/script, chưa thay thế manual validation bằng runtime request, source review và evidence thật.

#### 5. Nội dung đã được SV sửa hoặc bổ sung

Sinh viên đã bổ sung/cập nhật:

- `src/semgrep/semgrep_ai_triage.py`
- `src/semgrep/test_semgrep_ai_triage.py`
- `submission/User_Guide.md`

Kết quả workflow hiện tại:

- `semgrep_triage_report.md`: báo cáo tổng hợp all findings, có bảng tiếng Việt, tag lỗi, source evidence và AI analysis đã normalize heading.
- `semgrep_test_cases.md`: danh sách test case theo từng entry, có `Finding liên quan`, `Input`, `Thao tác`, `Kết quả cần ghi nhận`, `Trạng thái`.
- `findings/*_prompt.md`: prompt từng finding, yêu cầu AI đọc source và phân loại ba trạng thái.
- `findings/*_ai_output.md`: raw output từng finding, giữ nguyên để đối chiếu.

## 3. Tổng Kết Độ Chính Xác AI

| ID | Nhóm test | Verdict | Ghi chú chính |
| --- | --- | --- | --- |
| Mục 1 | Semgrep hardcoded JWT PoC | INCOMPLETE | Ý tưởng đúng nhưng AI dùng placeholder secret/endpoint; SV đã sửa bằng `exploit.js`. |
| Mục 2 | Semgrep cleartext HTTP proxy verification | INCOMPLETE | Cần runtime config, proxy log và oracle rõ. |
| Mục 3 | Semgrep all-findings/unit workflow | VALID | Unit tests deterministic, có oracle, không phụ thuộc API. |
| Mục 4 | ZAP HTML parser/offline triage | VALID | Parser/renderer tests có fixture và expected result rõ. |
| Mục 5 | ZAP CLI scan mode/report format | VALID | Có positive/negative tests và traceability với yêu cầu W06. |
| Mục 6 | ZAP authenticated scan | VALID | Kiểm tra target allowlist, JWT Replacer, Forced User Mode, cleanup. |
| Mục 7 | ZAP JSON/OpenRouter report | INCOMPLETE | Parser tests tốt nhưng AI report cần dedup, sửa tag sai và thêm evidence execute. |
| Mục 8 | Semgrep AI triage refinement trong phiên chat | VALID | Có regression tests cho source-first prompt, fail-fast AI, report tiếng Việt, test case entry, tag CWE/OWASP và format heading. |

Tổng cộng có 8 nhóm nội dung AI được audit:

- 5/8 mục được đánh giá `VALID` ở mức unit/component/regression testing hoặc workflow có mock rõ ràng.
- 3/8 mục được đánh giá `INCOMPLETE` vì còn thiếu runtime evidence, precondition, test data đúng SUT, request/response log hoặc screenshot xác minh.
- Tỉ lệ nội dung có thể dùng trực tiếp sau human review: khoảng 62,5%.
- Tỉ lệ nội dung cần bổ sung bằng chứng trước khi dùng làm kết luận cuối: khoảng 37,5%.

AI hữu ích nhất khi hỗ trợ cấu trúc hóa script, test, prompt và report. AI kém tin cậy hơn khi phải tự suy ra dữ liệu runtime, endpoint thật, taxonomy OWASP hoặc trạng thái "Actual" nếu nhóm chưa cung cấp bằng chứng execute.

## 4. Kết Luận

AI hỗ trợ tốt nhất ở các việc:

- Hỗ trợ rà soát parser, CLI, config và luồng AI triage.
- Gợi ý PoC và remediation cho hardcoded JWT secret.
- Tạo prompt/report format cho AI triage.

Các lỗi hoặc hạn chế đã audit được:

- Một số PoC thiếu precondition, test data hoặc expected result.
- Có placeholder thay cho dữ liệu thật của SUT.
- Có nguy cơ ghi "Actual" khi chưa có bằng chứng execution.
- Có duplicate findings cùng root cause.
- Có sai sót taxonomy/tag OWASP trong output AI.
- Có nguy cơ format report bị lệch nếu nhúng raw AI Markdown trực tiếp; đã giảm rủi ro bằng cách normalize heading trong `semgrep_triage_report.md`.
- Có nguy cơ report thiếu phân tích khi provider lỗi; đã giảm rủi ro bằng fail-fast thay vì sinh output lỗi như finding hợp lệ.

Kết luận về mức độ tin cậy: các unit tests đã được sinh viên sửa/bổ sung trong `src/semgrep` và `src/zap` có thể xem là hợp lệ ở mức component/regression testing. Các PoC, hướng kiểm chứng và security report có AI hỗ trợ cần tiếp tục human validation bằng source evidence, request/response log, screenshot hoặc report ZAP/Semgrep trước khi dùng làm bằng chứng chính thức.

## 5. Disclosure

Nhóm có sử dụng các công cụ AI như ChatGPT/Codex, Google Gemini và Gemini qua OpenRouter để hỗ trợ học công cụ, viết nháp script, tạo prompt triage, giải thích finding, đề xuất PoC, đề xuất remediation và rà soát nội dung báo cáo.

Nhóm không xem AI là nguồn bằng chứng cuối cùng. Các kết luận trong báo cáo chỉ được giữ lại khi đã được thành viên phụ trách đọc lại, chỉnh sửa và đối chiếu với ít nhất một trong các nguồn sau:

- Source code EShop hoặc script trong repository.
- Output Semgrep/ZAP đã lưu.
- Unit test hoặc mock test trong `src/semgrep` và `src/zap`.
- PoC/testcase, request/response log, screenshot hoặc evidence trong weekly reports.
- Tài liệu chính thức của Semgrep, OWASP ZAP, OWASP Top 10 hoặc provider liên quan.

Các phần còn `INCOMPLETE` được giữ nguyên trạng thái để minh bạch rằng AI output hoặc report chưa đủ bằng chứng kiểm thử cuối cùng. Nhóm không sử dụng AI để tạo giả feedback, attendance, log chạy tool, screenshot hoặc kết quả scan.

Chi tiết công bố theo từng thành viên được ghi trong `ai-audit/[AI-03]_AI_Disclosure_Template.md` và cần được ký/xuất thành `ai-audit/[AI-03]_AI_Disclosure.pdf` trước khi nộp.
