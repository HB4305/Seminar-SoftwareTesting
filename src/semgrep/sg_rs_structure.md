# Cấu trúc JSON của `sg_rs.json`

Tài liệu này mô tả cấu trúc chính của file kết quả Semgrep tại `src/semgrep/sg_rs.json`. File này là đầu vào cho bước AI triage trong workflow SAST.

## Tổng quan dữ liệu hiện tại

- `version`: phiên bản Semgrep đã tạo report.
- `results`: danh sách findings Semgrep phát hiện được.
- `errors`: lỗi/cảnh báo trong quá trình Semgrep phân tích.
- `paths.scanned`: danh sách file đã được scan.
- `time`: thông tin profiling, thời gian parse/scan và timeout.
- `engine_requested`: engine Semgrep được dùng, hiện là `OSS`.
- `skipped_rules`: danh sách rule bị bỏ qua.
- `profiling_results`: kết quả profiling bổ sung.

Trong report hiện tại có `12` findings, gồm `3` cảnh báo hardcoded JWT secret và `9` cảnh báo HTTP request không mã hóa.

## Schema rút gọn

```json
{
  "version": "string",
  "results": [
    {
      "check_id": "string",
      "path": "string",
      "start": {
        "line": "number",
        "col": "number",
        "offset": "number"
      },
      "end": {
        "line": "number",
        "col": "number",
        "offset": "number"
      },
      "extra": {
        "message": "string",
        "metadata": {
          "cwe": ["string"],
          "references": ["string"],
          "owasp": ["string"],
          "asvs": {
            "control_id": "string",
            "control_url": "string",
            "section": "string",
            "version": "string"
          },
          "category": "string",
          "technology": ["string"],
          "cwe2022-top25": "boolean",
          "cwe2021-top25": "boolean",
          "subcategory": ["string"],
          "likelihood": "string",
          "impact": "string",
          "confidence": "string",
          "license": "string",
          "vulnerability_class": ["string"],
          "source": "string",
          "shortlink": "string"
        },
        "severity": "string",
        "fingerprint": "string",
        "lines": "string",
        "validation_state": "string",
        "engine_kind": "string"
      }
    }
  ],
  "errors": [
    {
      "code": "number",
      "level": "string",
      "type": "string",
      "message": "string",
      "path": "string"
    }
  ],
  "paths": {
    "scanned": ["string"]
  },
  "time": {
    "rules": [],
    "rules_parse_time": "number",
    "profiling_times": {},
    "parsing_time": {},
    "scanning_time": {},
    "matching_time": {},
    "tainting_time": {},
    "fixpoint_timeouts": [],
    "prefiltering": {},
    "targets": [],
    "total_bytes": "number",
    "max_memory_bytes": "number"
  },
  "engine_requested": "string",
  "skipped_rules": [],
  "profiling_results": []
}
```

## Các trường quan trọng cho AI triage

- `results[].check_id`: mã rule Semgrep, dùng để nhóm finding theo loại lỗi.
- `results[].path`: file nguồn chứa cảnh báo.
- `results[].start.line` và `results[].end.line`: vị trí code cần trích xuất để kiểm chứng.
- `results[].extra.message`: mô tả cảnh báo gốc của Semgrep.
- `results[].extra.metadata.cwe`: mã CWE để mapping với chuẩn bảo mật.
- `results[].extra.metadata.owasp`: nhóm OWASP liên quan.
- `results[].extra.metadata.likelihood`, `impact`, `confidence`: tín hiệu ưu tiên triage.
- `results[].extra.severity`: mức độ Semgrep gán cho finding.
- `results[].extra.lines`: đoạn code Semgrep trả về; trong report hiện tại nhiều giá trị là `requires login`, nên script cần fallback đọc trực tiếp source code.

## Nhóm finding hiện tại

| Rule | Số lượng | File liên quan | Ý nghĩa |
| --- | ---: | --- | --- |
| `javascript.jsonwebtoken.security.jwt-hardcode.hardcoded-jwt-secret` | 3 | `backend/server.js`, `backend/test_profile.js` | Phát hiện secret/JWT key hardcode trong source code. |
| `typescript.react.security.react-insecure-request.react-insecure-request` | 9 | `frontend-mobile/App.js` | Phát hiện request dùng HTTP không mã hóa. |

