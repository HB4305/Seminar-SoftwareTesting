#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chuyển đổi báo cáo JSON của OWASP ZAP thành file Postman Collection JSON (v2.1).

Công dụng:
    Giúp tạo nhanh các API requests trên Postman chứa đúng Method, Endpoint
    và Payload (Attack) mà ZAP đã dùng để phát hiện lỗ hổng. Phục vụ cho việc
    tái lập lỗi thủ công và đối chiếu chéo (cross-check) với kết quả Semgrep.

Cách chạy:
    python src/zap/zap_to_postman.py --input src/zap/output/backend_basic.json --output src/zap/output/zap_replay_collection.json
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from urllib.parse import urlparse, parse_qsl, urlencode


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Convert ZAP JSON report to a Postman Collection (v2.1.0)"
    )
    parser.add_argument(
        "-i", "--input",
        required=True,
        help="Đường dẫn tới file JSON report của ZAP (ví dụ: src/zap/output/backend_basic.json)"
    )
    parser.add_argument(
        "-o", "--output",
        help="Đường dẫn lưu file Postman Collection JSON (mặc định lưu cùng thư mục file input)"
    )
    return parser


def parse_zap_report(json_path: Path) -> list[dict]:
    """Đọc ZAP JSON report và trích xuất danh sách các alert cùng các request instances."""
    try:
        data = json.loads(json_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        print(f"[!] Không thể đọc hoặc parse file JSON: {exc}", file=sys.stderr)
        sys.exit(1)

    alerts_extracted = []
    
    # ZAP JSON report có cấu trúc gốc chứa key "site" là list
    sites = data.get("site", [])
    if isinstance(sites, dict):  # Đôi khi ZAP trả về dict thay vì list nếu chỉ có 1 site
        sites = [sites]

    for site in sites:
        alerts = site.get("alerts", [])
        for alert in alerts:
            alert_name = alert.get("alert", alert.get("name", "Unknown Alert"))
            cwe_id = alert.get("cweid", "")
            cwe_str = f"CWE-{cwe_id}" if cwe_id and cwe_id != "-1" else "N/A"
            
            # Trích xuất các tag OWASP từ alert
            owasp_tags = []
            tags_data = alert.get("tags")
            if isinstance(tags_data, dict):
                for key in tags_data.keys():
                    if "owasp" in key.lower():
                        owasp_tags.append(key)
            elif isinstance(tags_data, list):
                for tag in tags_data:
                    if "owasp" in str(tag).lower():
                        owasp_tags.append(str(tag))
            
            owasp_str = ", ".join(owasp_tags) if owasp_tags else "N/A"
            description = alert.get("desc", "")
            solution = alert.get("solution", "")

            # Duyệt qua các request instances cụ thể của alert này
            instances = alert.get("instances", [])
            for inst in instances:
                uri = inst.get("uri", "")
                method = inst.get("method", "GET").upper()
                param = inst.get("param", "")
                attack = inst.get("attack", "")
                evidence = inst.get("evidence", "")

                if not uri:
                    continue

                alerts_extracted.append({
                    "alert_name": alert_name,
                    "cwe": cwe_str,
                    "owasp": owasp_str,
                    "uri": uri,
                    "method": method,
                    "param": param,
                    "attack": attack,
                    "evidence": evidence,
                    "description": description,
                    "solution": solution
                })

    return alerts_extracted


def generate_postman_item(alert: dict) -> dict:
    """Tạo cấu trúc một Request Item chuẩn Postman Collection v2.1.0."""
    uri = alert["uri"]
    method = alert["method"]
    param = alert["param"]
    attack = alert["attack"]
    
    parsed_url = urlparse(uri)
    protocol = parsed_url.scheme or "http"
    host_parts = parsed_url.hostname.split(".") if parsed_url.hostname else ["localhost"]
    port = str(parsed_url.port) if parsed_url.port else ""
    path_parts = [p for p in parsed_url.path.split("/") if p]

    # Xử lý Query Parameters
    query_params = dict(parse_qsl(parsed_url.query))
    if method == "GET" and param and attack:
        query_params[param] = attack

    postman_query = []
    for k, v in query_params.items():
        postman_query.append({"key": k, "value": v})

    # Reconstruct raw URL
    if query_params:
        raw_url = parsed_url._replace(query=urlencode(query_params)).geturl()
    else:
        raw_url = uri

    # Xử lý Request Body (Cho POST/PUT/PATCH)
    body = {}
    headers = [
        {
            "key": "Content-Type",
            "value": "application/json"
        }
    ]

    if method in ("POST", "PUT", "PATCH") and param and attack:
        # Giả định API của EShop nhận JSON payload
        raw_body_dict = {param: attack}
        body = {
            "mode": "raw",
            "raw": json.dumps(raw_body_dict, indent=2),
            "options": {
                "raw": {
                    "language": "json"
                }
            }
        }

    # Nội dung mô tả chi tiết của request trên Postman để SV theo dõi
    postman_description = (
        f"### 🚨 {alert['alert_name']}\n\n"
        f"- **OWASP Category:** {alert['owasp']}\n"
        f"- **CWE:** {alert['cwe']}\n"
        f"- **Method & URL:** `{method} {uri}`\n"
        f"- **Vulnerable Parameter:** `{param}`\n"
        f"- **Attack Payload (PoC):** `{attack}`\n"
        f"- **ZAP Evidence:** `{alert['evidence']}`\n\n"
        f"#### Mô tả lỗi:\n{alert['description']}\n\n"
        f"#### Khuyến nghị sửa chữa:\n{alert['solution']}"
    )

    # Đặt tên dễ đọc hiển thị trên danh sách Postman
    request_name = f"[{alert['cwe']}] {alert['alert_name']} ({method} /{'/'.join(path_parts[-2:]) if path_parts else ''})"

    return {
        "name": request_name,
        "request": {
            "method": method,
            "header": headers,
            "url": {
                "raw": raw_url,
                "protocol": protocol,
                "host": host_parts,
                "port": port,
                "path": path_parts,
                "query": postman_query
            },
            "body": body,
            "description": postman_description
        },
        "response": []
    }


def main() -> int:
    args = build_parser().parse_args()
    input_path = Path(args.input)
    
    if not input_path.exists():
        print(f"[!] Không tìm thấy file báo cáo ZAP: {input_path}", file=sys.stderr)
        return 1

    # Xác định đường dẫn file đầu ra
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = input_path.with_name(f"{input_path.stem}_postman_collection.json")

    print(f"[*] Đang parse báo cáo ZAP: {input_path}")
    alerts = parse_zap_report(input_path)
    
    if not alerts:
        print("[!] Không tìm thấy lỗ hổng/request instance nào trong báo cáo ZAP.")
        return 0

    print(f"[+] Tìm thấy {len(alerts)} request instances có lỗi từ ZAP.")

    # Xây dựng cấu trúc Postman Collection v2.1.0
    postman_items = [generate_postman_item(alert) for alert in alerts]
    
    collection = {
        "info": {
            "_postman_id": f"zap-replay-{input_path.stem}",
            "name": f"ZAP Replay Collection - {input_path.stem.replace('_', ' ').title()}",
            "description": f"Bộ testcases được tạo tự động từ báo cáo quét bảo mật ZAP: {input_path.name} để đối chiếu với Semgrep.",
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
        },
        "item": postman_items
    }

    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(collection, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"[+] Đã tạo thành công Postman Collection tại: {output_path}")
        print(f"[i] Hướng dẫn: Mở Postman -> Chọn Import -> Kéo thả file trên vào để tái lập các lỗ hổng.")
    except OSError as exc:
        print(f"[!] Không thể ghi file kết quả: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
