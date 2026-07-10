# Weekly Report - W05

## 1. Thông tin chung

- ID Nhóm: **06**
- Tên nhóm: **KDBK**
- Tên project: **T09 - Security Testing (DAST / SAST)**
- Thời gian làm: 2026-07-06 - 2026-07-11

## 2. Nhiệm vụ đã hoàn thành tuần này

### 2.1. Bảng nhiệm vụ

| **Nhiệm vụ**                                                          | **Họ tên**                   |
| :---------------------------------------------------------------------------- | :----------------------------------- |
| Track Semgrep: Cài đặt và chạy Semgrep.                                  | Lâm Hữu Khánh, Lê Mai Hoài Bảo |
| Track Semgrep: Tạo flow Test với Semgrep, AI Triage (có báo cáo output). | Lâm Hữu Khánh, Lê Mai Hoài Bảo |
| Track Zap: Cài đặt và chạy Zap.                                          | Lê Trung Kiên, Mai Thị Kim Duyên |
| Track Zap: Tạo flow Test với Zap, AI Triage (có báo cáo output).         | Lê Trung Kiên, Mai Thị Kim Duyên |

### 2.2. Minh chứng

### 2.2.1. Phân công trên Jira

![1783694468293](image/Group06/1783694468293.png)

- **Track Semgrep: Cài đặt và chạy Semgrep**

  - Mô tả:
  - Thành viên: Lâm Hữu Khánh, Lê Mai Hoài Bảo
- **Track Semgrep: Tạo flow Test với Semgrep, AI Triage (có báo cáo output)**

  - Mô tả:
  - Thành viên: Lâm Hữu Khánh, Lê Mai Hoài Bảo
- **Track Zap: Cài đặt và chạy Zap**

  - Mô tả:
  - Thành viên: Lê Trung Kiên, Mai Thị Kim Duyên
- **Track Zap: Tạo flow Test với ZAP, AI Triage (có báo cáo output)**

  - Mô tả:
  - Thành viên: Lê Trung Kiên, Mai Thị Kim Duyên

### 2.2.2. Các document liên quan

Evidence tuần này gồm:

- Phần ZAP đã được đặt trong thư mục`./evidence/zap`
- Phần Semgrep đã được đặt trong thư mục`./evidence/semgrep/`

## 3. Khai báo sử dụng AI

### 3.1. Lê Trung Kiên

- Công cụ: ChatGPT, model GPT-5.5
- Prompt đã sử dụng: Yêu cầu AI hỗ trợ viết script đọc output scan OWASP ZAP, tạo báo cáo AI triage và gợi ý prompt phân tích alert/impact/PoC/fix.
- Mục đích sử dụng: Hỗ trợ xây dựng script chuyển output scan ZAP thành báo cáo AI triage.
- Nội dung AI tạo ra: Draft logic xử lý ZAP report, draft prompt gửi alert cho AI và một phần nội dung mô tả trong output triage mẫu.
- Nội dung tự thực hiện/kiểm chứng: Chỉnh sửa script để gửi API qua OpenRouter, kiểm tra luồng đọc input/xuất markdown và đối chiếu nội dung triage với evidence từ ZAP report.

### 3.2. Mai Thị Kim Duyên

- Chưa bổ sung thông tin khai báo sử dụng AI.

### 3.3. Lâm Hữu Khánh

- Chưa bổ sung thông tin khai báo sử dụng AI.

### 3.4. Lê Mai Hoài Bảo

- Chưa bổ sung thông tin khai báo sử dụng AI.

## 4. Task tuần sau

| **Id** | **Task name**                                                                                          | **Member**                     |
| :----------: | :----------------------------------------------------------------------------------------------------------- | :----------------------------------- |
|      1      | Cài đặt và chạy cơ bản Track Zap theo hướng dẫn đã viết                                         | Lâm Hữu Khánh, Lê Mai Hoài Bảo |
|      2      | Cài đặt và chạy cơ bản Semgrep theo hướng dẫn đã viết                                          | Lê Trung Kiên, Mai Thị Kim Duyên |
|      3      | Hoàn thiện Track Semgrep trên EShop, bổ sung evidence, output scan, AI triage và ghi chú kiểm chứng. | Lâm Hữu Khánh, Lê Mai Hoài Bảo |
|      4      | Hoàn thiện Track Zap trên EShop, bổ sung evidence, output scan, AI triage và ghi chú kiểm chứng.     | Lê Trung Kiên, Mai Thị Kim Duyên |

## 5. Vấn đề phát sinh

Không có
