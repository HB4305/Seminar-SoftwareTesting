# Phiếu Hoạt Động Trên Lớp

| STT | Tên nhóm      | Tên đề tài                       |
| --- | --------------- | ------------------------------------ |
| T09 | Nhóm 06 - KDBK | T09 - Security Testing (DAST / SAST) |

## Thông tin nhóm

- Group:
- Danh sách thành viên (MSSV - Họ và tên):

## Số lượng finding/alert

| Công cụ           | Output dùng để tổng hợp | Số lượng |
| ------------------- | ---------------------------- | ----------- |
| Semgrep             |                              |             |
| ZAP automation scan |                              |             |

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

| ID | Mục tiêu (PoC & Alert) | Đầu vào (URL / Payload) | Thao tác (Replay Step) | Kết quả mong muốn (AI Gen) | Kết quả thực tế (Manual Verify) |
| -- | ------------------------ | -------------------------- | ----------------------- | ----------------------------- | ----------------------------------- |
|    |                          |                            |                         |                               |                                     |
|    |                          |                            |                         |                               |                                     |
|    |                          |                            |                         |                               |                                     |
|    |                          |                            |                         |                               |                                     |
|    |                          |                            |                         |                               |                                     |
