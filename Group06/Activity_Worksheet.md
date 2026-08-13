# Phiếu Hoạt Động Trên Lớp

| STT | Tên nhóm      | Tên đề tài                       |
| --- | --------------- | ------------------------------------ |
| T09 | Nhóm 06 - KDBK | T09 - Security Testing (DAST / SAST) |

## Thông tin nhóm

- Group:
- Danh sách thành viên (MSSV - Họ và tên):

## Số lượng finding/alert

| Công cụ           | Output dùng để tổng hợp                | Số lượng |
| ------------------- | ------------------------------------------- | ----------- |
| Semgrep             | `src/semgrep/output/semgrep_results.json` |             |
| ZAP automation scan |                                             |             |

## Thực hành Semgrep

### Thực hành quá trình chạy Semgrep và tổng hợp Alert

Dựa vào kết quả của Semgrep (file `src/semgrep/output/semgrep_results.json` hoặc chạy lệnh scan), hãy liệt kê 5 alert đại diện:

| STT | Quy tắc (Rule ID) | File & Dòng lỗi | Mức độ (Severity) | Tag lỗi / CWE / OWASP |
| --- | ------------------ | ----------------- | -------------------- | ---------------------- |
| 1   |                    |                   |                      |                        |
| 2   |                    |                   |                      |                        |
| 3   |                    |                   |                      |                        |
| 4   |                    |                   |                      |                        |
| 5   |                    |                   |                      |                        |

### Thực hành quá trình phân loại và thẩm định Cảnh báo (Semgrep Triage)

Dựa vào mã nguồn và tài liệu hướng dẫn (Guideline), hãy tiến hành phân loại các alert đại diện (gồm True Positive - Lỗi thật, False Positive - Cảnh báo giả, Duplicate - Trùng lặp):

| STT | Quy tắc (Rule ID)         | File & Dòng lỗi     | Phân loại (TP / FP / Duplicate) | Lý do đánh giá |
| --- | -------------------------- | --------------------- | --------------------------------- | ------------------ |
| 1   | `hardcoded-jwt-secret`   | `server.js:51`      |                                   |                    |
| 2   | `hardcoded-jwt-secret`   | `test_profile.js:4` |                                   |                    |
| 3   | `hardcoded-jwt-secret`   | `server.js:105`     |                                   |                    |
| 4   | `react-insecure-request` | `App.js:174`        |                                   |                    |
| 5   | `react-insecure-request` | `App.js:189`        |                                   |                    |

### Thực hành quá trình kiểm chứng lỗ hổng bằng PoC

Dựa vào kết quả AI Triage cho lỗi `hardcoded-jwt-secret`, hãy dùng script PoC (`exploit.js`) để kiểm chứng thủ công trên hệ thống đang chạy:

| ID | Alert / Lỗi kiểm chứng               | Đầu vào (Payload / Script PoC)          | Thao tác thực hiện (Replay Step)                                             | Kết quả thực tế | Kết luận |
| -- | --------------------------------------- | ------------------------------------------ | ------------------------------------------------------------------------------- | ------------------- | ---------- |
| 1  | Hardcoded JWT Secret (`server.js:51`) | Script`exploit.js` sinh admin token giả | Gửi request`GET /api/users/me` kèm Header `Authorization: Bearer <token>` |                     |            |

## Thực hành ZAP

### Ý nghĩa các bước scan của ZAP

| Bước scan | Ý nghĩa |
| ----------- | --------- |
| Spider      |           |
| Ajax Spider |           |
| Active Scan |           |

### Thực hành quá trình chạy ZAP và tổng hợp Alert

Dựa vào kết quả của ZAP, hãy liệt kê 5 alert đại diện:

| STT | Tên Alert | Độ nghiêm trọng | Tag lỗi / CWE | Số endpoint |
| --- | ---------- | ------------------- | -------------- | ------------ |
|     |            |                     |                |              |
|     |            |                     |                |              |
|     |            |                     |                |              |
|     |            |                     |                |              |
|     |            |                     |                |              |

### Thực hành quá trình kiểm chứng các alert

Dựa vào kết quả của ZAP, hãy liệt kê 5 alert đại diện (gồm 3 lỗi được liệt kê đúng - True Positive và 2 lỗi được liệt kê sai - False Positive):

| STT | Tên Alert                                  | Độ nghiêm trọng | Tag lỗi                            | Số endpoint |
| --- | ------------------------------------------- | ------------------- | ----------------------------------- | ------------ |
| 1   | Cross-Domain Misconfiguration               | Medium              | CWE-264, WASC-14, OWASP_2025_A01  | 12           |
| 2   | Server Leaks Information via "X-Powered-By" | Low                 | CWE-497, WASC-13, OWASP_2025_A01, | 15           |
| 3   | Missing Anti-clickjacking Header            | Medium              | CWE-1021, WASC-15, OWASP_2025_A02 | 14           |
| 4   | Path Traversal                              | High                | CWE-22, WASC-33, OWASP_2025_A01   | 3            |
| 5   | Timestamp Disclosure - Unix                 | Low                 | CWE-497, WASC-13, OWASP_2025_A01  | 3            |

**Yêu cầu:** Cho danh sách 5 lỗi được trích ra từ report. Hãy sử dụng AI (Prompting LLM) để sinh ra testcase chi tiết và PoC (câu lệnh `curl` / HTTP Replay/ Sử dụng Postman). Tiến hành kiểm chứng thủ công (Manual Verify) trên hệ thống web đang khởi chạy để điền kết quả thực tế vào bảng:

| ID | Mục tiêu (PoC & Alert) | Đầu vào (URL / Payload) | Tiền điều kiện | Thao tác (Replay Step) | Kết quả mong muốn (AI Gen) | Kết quả thực tế (Manual Verify) | Kết luận |
| -- | ------------------------ | -------------------------- | ------------------ | ----------------------- | ----------------------------- | ----------------------------------- | ---------- |
|    |                          |                            |                    |                         |                               |                                     |            |
|    |                          |                            |                    |                         |                               |                                     |            |
|    |                          |                            |                    |                         |                               |                                     |            |
|    |                          |                            |                    |                         |                               |                                     |            |
|    |                          |                            |                    |                         |                               |                                     |            |
