# ZAP AI Triage Report

- Source report: `/home/melyen/Documents/class/testing/seminar/Seminar-SoftwareTesting/src/zap/output/backend_basic.json`
- AI/model mode: `offline-template`
- Alerts parsed: `12`

## Risk Summary

- Unknown: 12

## Parsed Alerts

| Risk | Confidence | Alert | Request |
| --- | --- | --- | --- |
| Unknown | 3 | CSP: Failure to Define Directive with No Fallback | `GET http://localhost:3000` |
| Unknown | 3 | CSP: Failure to Define Directive with No Fallback | `GET http://localhost:3000/` |
| Unknown | 3 | CSP: Failure to Define Directive with No Fallback | `GET http://localhost:3000/robots.txt` |
| Unknown | 3 | CSP: Failure to Define Directive with No Fallback | `GET http://localhost:3000/sitemap.xml` |
| Unknown | 2 | Cross-Domain Misconfiguration | `GET http://localhost:3000` |
| Unknown | 2 | Cross-Domain Misconfiguration | `GET http://localhost:3000/` |
| Unknown | 2 | Cross-Domain Misconfiguration | `GET http://localhost:3000/robots.txt` |
| Unknown | 2 | Cross-Domain Misconfiguration | `GET http://localhost:3000/sitemap.xml` |
| Unknown | 2 | Server Leaks Information via "X-Powered-By" HTTP Response Header Field(s) | `GET http://localhost:3000` |
| Unknown | 2 | Server Leaks Information via "X-Powered-By" HTTP Response Header Field(s) | `GET http://localhost:3000/` |
| Unknown | 2 | Server Leaks Information via "X-Powered-By" HTTP Response Header Field(s) | `GET http://localhost:3000/robots.txt` |
| Unknown | 2 | Server Leaks Information via "X-Powered-By" HTTP Response Header Field(s) | `GET http://localhost:3000/sitemap.xml` |

## AI Triage Note
Nguồn dữ liệu: `/home/melyen/Documents/class/testing/seminar/Seminar-SoftwareTesting/src/zap/output/backend_basic.json`. Bản này dùng offline template vì chưa gọi AI hoặc AI không khả dụng.

### Ưu tiên xử lý
#### Unknown - CSP: Failure to Define Directive with No Fallback
- ZAP Alert Note: `GET http://localhost:3000`
- Confidence: 3
- Parameter: Content-Security-Policy
- Evidence: default-src 'none'
- Triage: Cần reproduce thủ công.
- Impact: Cần đánh giá theo evidence và dữ liệu endpoint trả về.

**PoC / Testcase kiểm chứng**:
        - **Loại lỗi**: CSP: Failure to Define Directive with No Fallback (Unknown)
        - **Chi tiết lỗi**: <p>The Content Security Policy fails to define one of the directives that has no fallback. Missing/excluding them is the same as allowing anything.</p> (Parameter: `Content-Security-Policy`, Evidence: `default-src 'none'`)
        - **Tag**: OWASP_2021_A05, POLICY_QA_STD, POLICY_PENTEST, SYSTEMIC, CWE-693, OWASP_2017_A06, OWASP_2025_A02, POLICY_DEV_STD
        - **Cách check (script)**:
          ```bash
          curl -i -X GET http://localhost:3000
          ```
        - **Cách verify**:
          - **Expected**: Ứng dụng xử lý an toàn, không trả về thông tin nhạy cảm hoặc cấu hình sai.
- **Actual theo ZAP**: Phát hiện bằng chứng: `default-src 'none'`.

- Fix suggestion: <p>Ensure that your web server, application server, load balancer, etc. is properly configured to set the Content-Security-Policy header.</p>

#### Unknown - CSP: Failure to Define Directive with No Fallback
- ZAP Alert Note: `GET http://localhost:3000/`
- Confidence: 3
- Parameter: Content-Security-Policy
- Evidence: default-src 'none'
- Triage: Cần reproduce thủ công.
- Impact: Cần đánh giá theo evidence và dữ liệu endpoint trả về.

**PoC / Testcase kiểm chứng**:
        - **Loại lỗi**: CSP: Failure to Define Directive with No Fallback (Unknown)
        - **Chi tiết lỗi**: <p>The Content Security Policy fails to define one of the directives that has no fallback. Missing/excluding them is the same as allowing anything.</p> (Parameter: `Content-Security-Policy`, Evidence: `default-src 'none'`)
        - **Tag**: OWASP_2021_A05, POLICY_QA_STD, POLICY_PENTEST, SYSTEMIC, CWE-693, OWASP_2017_A06, OWASP_2025_A02, POLICY_DEV_STD
        - **Cách check (script)**:
          ```bash
          curl -i -X GET http://localhost:3000/
          ```
        - **Cách verify**:
          - **Expected**: Ứng dụng xử lý an toàn, không trả về thông tin nhạy cảm hoặc cấu hình sai.
- **Actual theo ZAP**: Phát hiện bằng chứng: `default-src 'none'`.

- Fix suggestion: <p>Ensure that your web server, application server, load balancer, etc. is properly configured to set the Content-Security-Policy header.</p>

#### Unknown - CSP: Failure to Define Directive with No Fallback
- ZAP Alert Note: `GET http://localhost:3000/robots.txt`
- Confidence: 3
- Parameter: Content-Security-Policy
- Evidence: default-src 'none'
- Triage: Cần reproduce thủ công.
- Impact: Cần đánh giá theo evidence và dữ liệu endpoint trả về.

**PoC / Testcase kiểm chứng**:
        - **Loại lỗi**: CSP: Failure to Define Directive with No Fallback (Unknown)
        - **Chi tiết lỗi**: <p>The Content Security Policy fails to define one of the directives that has no fallback. Missing/excluding them is the same as allowing anything.</p> (Parameter: `Content-Security-Policy`, Evidence: `default-src 'none'`)
        - **Tag**: OWASP_2021_A05, POLICY_QA_STD, POLICY_PENTEST, SYSTEMIC, CWE-693, OWASP_2017_A06, OWASP_2025_A02, POLICY_DEV_STD
        - **Cách check (script)**:
          ```bash
          curl -i -X GET http://localhost:3000/robots.txt
          ```
        - **Cách verify**:
          - **Expected**: Ứng dụng xử lý an toàn, không trả về thông tin nhạy cảm hoặc cấu hình sai.
- **Actual theo ZAP**: Phát hiện bằng chứng: `default-src 'none'`.

- Fix suggestion: <p>Ensure that your web server, application server, load balancer, etc. is properly configured to set the Content-Security-Policy header.</p>

#### Unknown - CSP: Failure to Define Directive with No Fallback
- ZAP Alert Note: `GET http://localhost:3000/sitemap.xml`
- Confidence: 3
- Parameter: Content-Security-Policy
- Evidence: default-src 'none'
- Triage: Cần reproduce thủ công.
- Impact: Cần đánh giá theo evidence và dữ liệu endpoint trả về.

**PoC / Testcase kiểm chứng**:
        - **Loại lỗi**: CSP: Failure to Define Directive with No Fallback (Unknown)
        - **Chi tiết lỗi**: <p>The Content Security Policy fails to define one of the directives that has no fallback. Missing/excluding them is the same as allowing anything.</p> (Parameter: `Content-Security-Policy`, Evidence: `default-src 'none'`)
        - **Tag**: OWASP_2021_A05, POLICY_QA_STD, POLICY_PENTEST, SYSTEMIC, CWE-693, OWASP_2017_A06, OWASP_2025_A02, POLICY_DEV_STD
        - **Cách check (script)**:
          ```bash
          curl -i -X GET http://localhost:3000/sitemap.xml
          ```
        - **Cách verify**:
          - **Expected**: Ứng dụng xử lý an toàn, không trả về thông tin nhạy cảm hoặc cấu hình sai.
- **Actual theo ZAP**: Phát hiện bằng chứng: `default-src 'none'`.

- Fix suggestion: <p>Ensure that your web server, application server, load balancer, etc. is properly configured to set the Content-Security-Policy header.</p>

#### Unknown - Cross-Domain Misconfiguration
- ZAP Alert Note: `GET http://localhost:3000`
- Confidence: 2
- Parameter: N/A
- Evidence: Access-Control-Allow-Origin: *
- Triage: Cần reproduce thủ công.
- Impact: Origin không tin cậy có thể đọc dữ liệu API nếu endpoint trả dữ liệu nhạy cảm hoặc được bảo vệ bằng mạng nội bộ.

**PoC / Testcase kiểm chứng**:
        - **Loại lỗi**: Cross-Domain Misconfiguration (Unknown)
        - **Chi tiết lỗi**: <p>Web browser data loading may be possible, due to a Cross Origin Resource Sharing (CORS) misconfiguration on the web server.</p> (Parameter: `N/A`, Evidence: `Access-Control-Allow-Origin: *`)
        - **Tag**: OWASP_2021_A01, POLICY_QA_STD, POLICY_PENTEST, SYSTEMIC, OWASP_2025_A01, OWASP_2017_A05, CWE-264
        - **Cách check (script)**:
          ```bash
          curl -i -H "Origin: http://evil.example" http://localhost:3000
          ```
        - **Cách verify**:
          - **Expected**: Không phản hồi header `Access-Control-Allow-Origin: *` đối với các domain ngoài danh sách trắng.
- **Actual theo ZAP**: Response trả về header `Access-Control-Allow-Origin: *` (Evidence: `Access-Control-Allow-Origin: *`).

- Fix suggestion: Giới hạn `Access-Control-Allow-Origin` theo allowlist frontend, không dùng `*` cho API có dữ liệu nghiệp vụ.

#### Unknown - Cross-Domain Misconfiguration
- ZAP Alert Note: `GET http://localhost:3000/`
- Confidence: 2
- Parameter: N/A
- Evidence: Access-Control-Allow-Origin: *
- Triage: Cần reproduce thủ công.
- Impact: Origin không tin cậy có thể đọc dữ liệu API nếu endpoint trả dữ liệu nhạy cảm hoặc được bảo vệ bằng mạng nội bộ.

**PoC / Testcase kiểm chứng**:
        - **Loại lỗi**: Cross-Domain Misconfiguration (Unknown)
        - **Chi tiết lỗi**: <p>Web browser data loading may be possible, due to a Cross Origin Resource Sharing (CORS) misconfiguration on the web server.</p> (Parameter: `N/A`, Evidence: `Access-Control-Allow-Origin: *`)
        - **Tag**: OWASP_2021_A01, POLICY_QA_STD, POLICY_PENTEST, SYSTEMIC, OWASP_2025_A01, OWASP_2017_A05, CWE-264
        - **Cách check (script)**:
          ```bash
          curl -i -H "Origin: http://evil.example" http://localhost:3000/
          ```
        - **Cách verify**:
          - **Expected**: Không phản hồi header `Access-Control-Allow-Origin: *` đối với các domain ngoài danh sách trắng.
- **Actual theo ZAP**: Response trả về header `Access-Control-Allow-Origin: *` (Evidence: `Access-Control-Allow-Origin: *`).

- Fix suggestion: Giới hạn `Access-Control-Allow-Origin` theo allowlist frontend, không dùng `*` cho API có dữ liệu nghiệp vụ.

#### Unknown - Cross-Domain Misconfiguration
- ZAP Alert Note: `GET http://localhost:3000/robots.txt`
- Confidence: 2
- Parameter: N/A
- Evidence: Access-Control-Allow-Origin: *
- Triage: Cần reproduce thủ công.
- Impact: Origin không tin cậy có thể đọc dữ liệu API nếu endpoint trả dữ liệu nhạy cảm hoặc được bảo vệ bằng mạng nội bộ.

**PoC / Testcase kiểm chứng**:
        - **Loại lỗi**: Cross-Domain Misconfiguration (Unknown)
        - **Chi tiết lỗi**: <p>Web browser data loading may be possible, due to a Cross Origin Resource Sharing (CORS) misconfiguration on the web server.</p> (Parameter: `N/A`, Evidence: `Access-Control-Allow-Origin: *`)
        - **Tag**: OWASP_2021_A01, POLICY_QA_STD, POLICY_PENTEST, SYSTEMIC, OWASP_2025_A01, OWASP_2017_A05, CWE-264
        - **Cách check (script)**:
          ```bash
          curl -i -H "Origin: http://evil.example" http://localhost:3000/robots.txt
          ```
        - **Cách verify**:
          - **Expected**: Không phản hồi header `Access-Control-Allow-Origin: *` đối với các domain ngoài danh sách trắng.
- **Actual theo ZAP**: Response trả về header `Access-Control-Allow-Origin: *` (Evidence: `Access-Control-Allow-Origin: *`).

- Fix suggestion: Giới hạn `Access-Control-Allow-Origin` theo allowlist frontend, không dùng `*` cho API có dữ liệu nghiệp vụ.

#### Unknown - Cross-Domain Misconfiguration
- ZAP Alert Note: `GET http://localhost:3000/sitemap.xml`
- Confidence: 2
- Parameter: N/A
- Evidence: Access-Control-Allow-Origin: *
- Triage: Cần reproduce thủ công.
- Impact: Origin không tin cậy có thể đọc dữ liệu API nếu endpoint trả dữ liệu nhạy cảm hoặc được bảo vệ bằng mạng nội bộ.

**PoC / Testcase kiểm chứng**:
        - **Loại lỗi**: Cross-Domain Misconfiguration (Unknown)
        - **Chi tiết lỗi**: <p>Web browser data loading may be possible, due to a Cross Origin Resource Sharing (CORS) misconfiguration on the web server.</p> (Parameter: `N/A`, Evidence: `Access-Control-Allow-Origin: *`)
        - **Tag**: OWASP_2021_A01, POLICY_QA_STD, POLICY_PENTEST, SYSTEMIC, OWASP_2025_A01, OWASP_2017_A05, CWE-264
        - **Cách check (script)**:
          ```bash
          curl -i -H "Origin: http://evil.example" http://localhost:3000/sitemap.xml
          ```
        - **Cách verify**:
          - **Expected**: Không phản hồi header `Access-Control-Allow-Origin: *` đối với các domain ngoài danh sách trắng.
- **Actual theo ZAP**: Response trả về header `Access-Control-Allow-Origin: *` (Evidence: `Access-Control-Allow-Origin: *`).

- Fix suggestion: Giới hạn `Access-Control-Allow-Origin` theo allowlist frontend, không dùng `*` cho API có dữ liệu nghiệp vụ.

### Human Audit Checklist
- Đối chiếu URL/request trong ZAP với app EShop đang chạy.
- Reproduce lại finding trên localhost và ghi screenshot/log.
- Kiểm tra source code hoặc cấu hình server tương ứng trước khi kết luận fix.
- Đánh dấu false positive nếu finding chỉ xuất hiện trên Vite/dev dependency.

### Metrics / Failure Modes
- Metrics cần ghi: thời gian scan, số alert theo risk, số finding reproduce được.
- Failure mode 1: ZAP có thể báo security header thiếu trên dev server thay vì production server.
- Failure mode 2: AI có thể viết PoC/fix quá chung, cần kiểm chứng bằng request/response thật.
- Failure mode 3: Nếu ZAP thiếu auth context, các endpoint sau đăng nhập có thể bị bỏ sót.

## Submission Block

Dán phần này vào `submission/Team_Work_Assignment.md` dưới Track B - ZAP flow hoặc Pha 2:

```markdown
### AI-Triage cho ZAP Track

- Input: `/home/melyen/Documents/class/testing/seminar/Seminar-SoftwareTesting/src/zap/output/backend_basic.json`
- Tool: OWASP ZAP report + OpenRouter/offline AI triage script `src/zap/ai_triage_zap.py`
- Tổng alert đã parse: 12
- Unknown: 12

Kết quả triage chính:
- `Unknown` `CSP: Failure to Define Directive with No Fallback` tại `http://localhost:3000`: Cần đánh giá theo evidence và dữ liệu endpoint trả về.
- `Unknown` `CSP: Failure to Define Directive with No Fallback` tại `http://localhost:3000/`: Cần đánh giá theo evidence và dữ liệu endpoint trả về.
- `Unknown` `CSP: Failure to Define Directive with No Fallback` tại `http://localhost:3000/robots.txt`: Cần đánh giá theo evidence và dữ liệu endpoint trả về.
- `Unknown` `CSP: Failure to Define Directive with No Fallback` tại `http://localhost:3000/sitemap.xml`: Cần đánh giá theo evidence và dữ liệu endpoint trả về.
- `Unknown` `Cross-Domain Misconfiguration` tại `http://localhost:3000`: Origin không tin cậy có thể đọc dữ liệu API nếu endpoint trả dữ liệu nhạy cảm hoặc được bảo vệ bằng mạng nội bộ.

PoC/reproducer ưu tiên:
**PoC / Testcase kiểm chứng**:
        - **Loại lỗi**: CSP: Failure to Define Directive with No Fallback (Unknown)
        - **Chi tiết lỗi**: <p>The Content Security Policy fails to define one of the directives that has no fallback. Missing/excluding them is the same as allowing anything.</p> (Parameter: `Content-Security-Policy`, Evidence: `default-src 'none'`)
        - **Tag**: OWASP_2021_A05, POLICY_QA_STD, POLICY_PENTEST, SYSTEMIC, CWE-693, OWASP_2017_A06, OWASP_2025_A02, POLICY_DEV_STD
        - **Cách check (script)**:
          ```bash
          curl -i -X GET http://localhost:3000
          ```
        - **Cách verify**:
          - **Expected**: Ứng dụng xử lý an toàn, không trả về thông tin nhạy cảm hoặc cấu hình sai.
- **Actual theo ZAP**: Phát hiện bằng chứng: `default-src 'none'`.

Testcase/evidence cần nộp:
- ZAP report gốc trong `src/zap/output` hoặc `zap_report.html`.
- AI triage output trong `src/zap/output/zap_ai_triage_report.md`.
- Screenshot/log khi reproduce finding ưu tiên cao nhất.
- Human audit note: AI chỉ hỗ trợ draft; nhóm kiểm chứng bằng request/response thật và source/runtime evidence.

Failure modes quan sát được:
- ZAP có thể báo noise trên Vite/dev server, ví dụ dependency trong `/node_modules/.vite` hoặc `@react-refresh`.
- AI có thể gợi ý fix quá chung; cần đối chiếu source code/backend config.
- Nếu ZAP không có auth context, scan có thể bỏ sót endpoint sau đăng nhập.
```
