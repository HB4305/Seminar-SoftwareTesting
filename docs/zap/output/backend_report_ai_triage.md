# ZAP AI Triage Report

- Source report: `/home/tkin/Documents/hcmus/software-testing/Seminar-SoftwareTesting/docs/zap/output/backend_report.html`
- AI/model mode: `offline-template`
- Alerts parsed: `13`

## Risk Summary

- Medium: 9
- Low: 4

## Parsed Alerts

| Risk | Confidence | Alert | Request |
| --- | --- | --- | --- |
| Medium | N/A | CSP: Failure to Define Directive with No Fallback | `GET http://localhost:3000` |
| Medium | N/A | CSP: Failure to Define Directive with No Fallback | `GET http://localhost:3000/` |
| Medium | N/A | CSP: Failure to Define Directive with No Fallback | `GET http://localhost:3000/robots.txt` |
| Medium | N/A | CSP: Failure to Define Directive with No Fallback | `GET http://localhost:3000/sitemap.xml` |
| Medium | N/A | Cross-Domain Misconfiguration | `GET http://localhost:3000` |
| Medium | N/A | Cross-Domain Misconfiguration | `GET http://localhost:3000/` |
| Medium | N/A | Cross-Domain Misconfiguration | `GET http://localhost:3000/robots.txt` |
| Medium | N/A | Cross-Domain Misconfiguration | `GET http://localhost:3000/sitemap.xml` |
| Medium | N/A | HTTP Only Site | `GET http://localhost:3000/` |
| Low | N/A | Server Leaks Information via "X-Powered-By" HTTP Response Header Field(s) | `GET http://localhost:3000` |
| Low | N/A | Server Leaks Information via "X-Powered-By" HTTP Response Header Field(s) | `GET http://localhost:3000/` |
| Low | N/A | Server Leaks Information via "X-Powered-By" HTTP Response Header Field(s) | `GET http://localhost:3000/robots.txt` |

## AI Triage Note
Nguồn dữ liệu: `/home/tkin/Documents/hcmus/software-testing/Seminar-SoftwareTesting/docs/zap/output/backend_report.html`. Bản này dùng offline template vì chưa gọi AI hoặc AI không khả dụng.

### Ưu tiên xử lý
#### Medium - CSP: Failure to Define Directive with No Fallback
- ZAP Alert Note: `GET http://localhost:3000`
- Confidence: N/A
- Parameter: Content-Security-Policy
- Evidence: default-src 'none'
- Triage: Cần reproduce thủ công.
- Impact: Cần đánh giá theo evidence và dữ liệu endpoint trả về.

**PoC/Reproducer**
1. Gửi request `GET http://localhost:3000` trong môi trường lab.
2. So sánh response header/body với evidence của ZAP.

**Testcase**
- Expected: không xuất hiện evidence rủi ro.
- Actual theo ZAP: `default-src 'none'`.

- Fix suggestion: Áp dụng khuyến nghị ZAP và kiểm chứng lại bằng scan.

#### Medium - CSP: Failure to Define Directive with No Fallback
- ZAP Alert Note: `GET http://localhost:3000/`
- Confidence: N/A
- Parameter: Content-Security-Policy
- Evidence: default-src 'none'
- Triage: Cần reproduce thủ công.
- Impact: Cần đánh giá theo evidence và dữ liệu endpoint trả về.

**PoC/Reproducer**
1. Gửi request `GET http://localhost:3000/` trong môi trường lab.
2. So sánh response header/body với evidence của ZAP.

**Testcase**
- Expected: không xuất hiện evidence rủi ro.
- Actual theo ZAP: `default-src 'none'`.

- Fix suggestion: Áp dụng khuyến nghị ZAP và kiểm chứng lại bằng scan.

#### Medium - CSP: Failure to Define Directive with No Fallback
- ZAP Alert Note: `GET http://localhost:3000/robots.txt`
- Confidence: N/A
- Parameter: Content-Security-Policy
- Evidence: default-src 'none'
- Triage: Cần reproduce thủ công.
- Impact: Cần đánh giá theo evidence và dữ liệu endpoint trả về.

**PoC/Reproducer**
1. Gửi request `GET http://localhost:3000/robots.txt` trong môi trường lab.
2. So sánh response header/body với evidence của ZAP.

**Testcase**
- Expected: không xuất hiện evidence rủi ro.
- Actual theo ZAP: `default-src 'none'`.

- Fix suggestion: Áp dụng khuyến nghị ZAP và kiểm chứng lại bằng scan.

#### Medium - CSP: Failure to Define Directive with No Fallback
- ZAP Alert Note: `GET http://localhost:3000/sitemap.xml`
- Confidence: N/A
- Parameter: Content-Security-Policy
- Evidence: default-src 'none'
- Triage: Cần reproduce thủ công.
- Impact: Cần đánh giá theo evidence và dữ liệu endpoint trả về.

**PoC/Reproducer**
1. Gửi request `GET http://localhost:3000/sitemap.xml` trong môi trường lab.
2. So sánh response header/body với evidence của ZAP.

**Testcase**
- Expected: không xuất hiện evidence rủi ro.
- Actual theo ZAP: `default-src 'none'`.

- Fix suggestion: Ensure that your web server, application server, load balancer, etc. is properly configured to set the Content-Security-Policy header.

#### Medium - Cross-Domain Misconfiguration
- ZAP Alert Note: `GET http://localhost:3000`
- Confidence: N/A
- Parameter: N/A
- Evidence: Access-Control-Allow-Origin: *
- Triage: Cần reproduce thủ công.
- Impact: Origin không tin cậy có thể đọc dữ liệu API nếu endpoint trả dữ liệu nhạy cảm hoặc được bảo vệ bằng mạng nội bộ.

**PoC CORS**
1. Gửi request đến `http://localhost:3000` với header `Origin: http://evil.example`.
2. Kiểm tra response header.

**Testcase**
- Expected: backend chỉ cho phép origin tin cậy như frontend EShop.
- Actual theo ZAP: response có bằng chứng `Access-Control-Allow-Origin: *`.

- Fix suggestion: Giới hạn `Access-Control-Allow-Origin` theo allowlist frontend, không dùng `*` cho API có dữ liệu nghiệp vụ.

#### Medium - Cross-Domain Misconfiguration
- ZAP Alert Note: `GET http://localhost:3000/`
- Confidence: N/A
- Parameter: N/A
- Evidence: Access-Control-Allow-Origin: *
- Triage: Cần reproduce thủ công.
- Impact: Origin không tin cậy có thể đọc dữ liệu API nếu endpoint trả dữ liệu nhạy cảm hoặc được bảo vệ bằng mạng nội bộ.

**PoC CORS**
1. Gửi request đến `http://localhost:3000/` với header `Origin: http://evil.example`.
2. Kiểm tra response header.

**Testcase**
- Expected: backend chỉ cho phép origin tin cậy như frontend EShop.
- Actual theo ZAP: response có bằng chứng `Access-Control-Allow-Origin: *`.

- Fix suggestion: Giới hạn `Access-Control-Allow-Origin` theo allowlist frontend, không dùng `*` cho API có dữ liệu nghiệp vụ.

#### Medium - Cross-Domain Misconfiguration
- ZAP Alert Note: `GET http://localhost:3000/robots.txt`
- Confidence: N/A
- Parameter: N/A
- Evidence: Access-Control-Allow-Origin: *
- Triage: Cần reproduce thủ công.
- Impact: Origin không tin cậy có thể đọc dữ liệu API nếu endpoint trả dữ liệu nhạy cảm hoặc được bảo vệ bằng mạng nội bộ.

**PoC CORS**
1. Gửi request đến `http://localhost:3000/robots.txt` với header `Origin: http://evil.example`.
2. Kiểm tra response header.

**Testcase**
- Expected: backend chỉ cho phép origin tin cậy như frontend EShop.
- Actual theo ZAP: response có bằng chứng `Access-Control-Allow-Origin: *`.

- Fix suggestion: Giới hạn `Access-Control-Allow-Origin` theo allowlist frontend, không dùng `*` cho API có dữ liệu nghiệp vụ.

#### Medium - Cross-Domain Misconfiguration
- ZAP Alert Note: `GET http://localhost:3000/sitemap.xml`
- Confidence: N/A
- Parameter: N/A
- Evidence: Access-Control-Allow-Origin: *
- Triage: Cần reproduce thủ công.
- Impact: Origin không tin cậy có thể đọc dữ liệu API nếu endpoint trả dữ liệu nhạy cảm hoặc được bảo vệ bằng mạng nội bộ.

**PoC CORS**
1. Gửi request đến `http://localhost:3000/sitemap.xml` với header `Origin: http://evil.example`.
2. Kiểm tra response header.

**Testcase**
- Expected: backend chỉ cho phép origin tin cậy như frontend EShop.
- Actual theo ZAP: response có bằng chứng `Access-Control-Allow-Origin: *`.

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

- Input: `/home/tkin/Documents/hcmus/software-testing/Seminar-SoftwareTesting/docs/zap/output/backend_report.html`
- Tool: OWASP ZAP report + Gemini/offline AI triage script `docs/zap/ai_triage_zap.py`
- Tổng alert đã parse: 13
- Medium: 9
- Low: 4

Kết quả triage chính:
- `Medium` `CSP: Failure to Define Directive with No Fallback` tại `http://localhost:3000`: Cần đánh giá theo evidence và dữ liệu endpoint trả về.
- `Medium` `CSP: Failure to Define Directive with No Fallback` tại `http://localhost:3000/`: Cần đánh giá theo evidence và dữ liệu endpoint trả về.
- `Medium` `CSP: Failure to Define Directive with No Fallback` tại `http://localhost:3000/robots.txt`: Cần đánh giá theo evidence và dữ liệu endpoint trả về.
- `Medium` `CSP: Failure to Define Directive with No Fallback` tại `http://localhost:3000/sitemap.xml`: Cần đánh giá theo evidence và dữ liệu endpoint trả về.
- `Medium` `Cross-Domain Misconfiguration` tại `http://localhost:3000`: Origin không tin cậy có thể đọc dữ liệu API nếu endpoint trả dữ liệu nhạy cảm hoặc được bảo vệ bằng mạng nội bộ.

PoC/reproducer ưu tiên:
**PoC/Reproducer**
1. Gửi request `GET http://localhost:3000` trong môi trường lab.
2. So sánh response header/body với evidence của ZAP.

**Testcase**
- Expected: không xuất hiện evidence rủi ro.
- Actual theo ZAP: `default-src 'none'`.

Testcase/evidence cần nộp:
- ZAP report gốc trong `docs/zap/output` hoặc `zap_report.html`.
- AI triage output trong `docs/zap/ai_triage_output.md`.
- Screenshot/log khi reproduce finding ưu tiên cao nhất.
- Human audit note: AI chỉ hỗ trợ draft; nhóm kiểm chứng bằng request/response thật và source/runtime evidence.

Failure modes quan sát được:
- ZAP có thể báo noise trên Vite/dev server, ví dụ dependency trong `/node_modules/.vite` hoặc `@react-refresh`.
- AI có thể gợi ý fix quá chung; cần đối chiếu source code/backend config.
- Nếu ZAP không có auth context, scan có thể bỏ sót endpoint sau đăng nhập.
```
