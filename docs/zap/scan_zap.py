#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kịch bản Tự động hóa Kiểm thử Bảo mật DAST với OWASP ZAP cho EShop (System Under Test)

Cài đặt thư viện:
    pip install python-owasp-zap-v2.4

Hướng dẫn khởi chạy ZAP (Docker):
    docker run -u zap
    --network host -d ghcr.io/zaproxy/zaproxy:stable zap.sh -daemon -port 8090 -host 0.0.0.0 -config api.disablekey=true
        
Chạy ứng dụng:
    ./run_server.sh

Cách chạy kịch bản quét cho các phân hệ của EShop:
    1. Quét Backend API (Mặc định):
        python zap_scan.py --target http://localhost:3000 --report-file zap_report_backend.html

    2. Quét Frontend Web (Nên bật AJAX Spider cho ứng dụng React/SPA):
        python zap_scan.py --target http://localhost:5173 --ajax-spider --report-file zap_report_frontend_web.html

    3. Quét Web Admin (SPA):
        python zap_scan.py --target http://localhost:5174 --ajax-spider --report-file zap_report_frontend_admin.html
"""

import argparse
import os
import sys
import time
from pathlib import Path

from zapv2 import ZAPv2

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_REPORT_PATH = SCRIPT_DIR / "zap_report.html"

def check_scan_status(zap, scan_id, scan_type="Spider"):
    """Vòng lặp kiểm tra tiến độ quét của ZAP"""
    print(f"[*] Đang khởi chạy {scan_type} (Scan ID: {scan_id})...")
    while True:
        if scan_type == "Spider":
            status = int(zap.spider.status(scan_id))
        elif scan_type == "Active Scan":
            status = int(zap.ascan.status(scan_id))
        elif scan_type == "AJAX Spider":
            status = zap.ajaxSpider.status
            if status == "stopped":
                print(f"\n[+] {scan_type} đã hoàn thành.")
                break
            print(f"\r[*] Tiến độ {scan_type}: đang chạy...", end="")
            time.sleep(5)
            continue
        
        print(f"\r[*] Tiến độ {scan_type}: {status}%", end="")
        if status >= 100:
            print(f"\n[+] {scan_type} đã hoàn thành.")
            break
        time.sleep(5)

def main():
    parser = argparse.ArgumentParser(description="Kịch bản quét bảo mật tự động ZAP API cho EShop")
    parser.add_argument("--target", default="http://localhost:3000", help="URL mục tiêu (Mặc định: http://localhost:3000 cho Backend)")
    parser.add_argument("--zap-url", default="http://localhost:8090", help="URL của ZAP Daemon (Mặc định: http://localhost:8090)")
    parser.add_argument("--api-key", default="", help="ZAP API Key (nếu có cấu hình)")
    parser.add_argument("--ajax-spider", action="store_true", help="Sử dụng AJAX Spider (Dành cho Frontend Single Page App)")
    parser.add_argument("--report-format", default="html", choices=["html", "json", "xml", "md"], help="Định dạng báo cáo output")
    parser.add_argument("--report-file", default=str(DEFAULT_REPORT_PATH), help="Tên file báo cáo output")
    
    args = parser.parse_args()
    target_url = args.target
    zap_url = args.zap_url
    api_key = args.api_key

    print(f"[*] Đang kết nối tới ZAP Proxy tại: {zap_url}")
    # Khởi tạo đối tượng ZAP
    zap = ZAPv2(apikey=api_key, proxies={'http': zap_url, 'https': zap_url})

    try:
        # Kiểm tra kết nối tới ZAP
        core_version = zap.core.version
        print(f"[+] Kết nối thành công! Phiên bản ZAP: {core_version}")
    except Exception as e:
        print(f"[!] Lỗi kết nối tới ZAP Proxy ({zap_url}). Vui lòng đảm bảo ZAP đang chạy ở chế độ daemon.")
        print(f"Chi tiết lỗi: {e}")
        sys.exit(1)

    print(f"[*] Mở URL mục tiêu: {target_url}")
    zap.urlopen(target_url)
    time.sleep(2)

    # 1. Bắt đầu Traditional Spider
    print(f"\n--- [1/4] DÒ QUÉT CẤU TRÚC (TRADITIONAL SPIDER) ---")
    scan_id = zap.spider.scan(target_url)
    check_scan_status(zap, scan_id, scan_type="Spider")

    # 2. Bắt đầu AJAX Spider (Nếu được bật)
    if args.ajax_spider:
        print(f"\n--- [2/4] DÒ QUÉT ỨNG DỤNG SPA (AJAX SPIDER) ---")
        zap.ajaxSpider.scan(target_url)
        check_scan_status(zap, None, scan_type="AJAX Spider")
    else:
        print(f"\n--- [2/4] DÒ QUÉT ỨNG DỤNG SPA (AJAX SPIDER) ---")
        print("[*] Bỏ qua AJAX Spider (Sử dụng cờ --ajax-spider nếu quét Frontend Web/Admin).")

    # 3. Chờ Passive Scan xử lý các request
    print(f"\n--- [3/4] PHÂN TÍCH THỤ ĐỘNG (PASSIVE SCAN) ---")
    while int(zap.pscan.records_to_scan) > 0:
        print(f"\r[*] Đang chờ Passive Scan xử lý {zap.pscan.records_to_scan} bản ghi...", end="")
        time.sleep(2)
    print("\n[+] Passive Scan đã hoàn tất.")

    # 4. Bắt đầu Active Scan (Quét lỗ hổng)
    print(f"\n--- [4/4] QUÉT LỖ HỔNG CHỦ ĐỘNG (ACTIVE SCAN) ---")
    ascan_id = zap.ascan.scan(target_url)
    check_scan_status(zap, ascan_id, scan_type="Active Scan")

    # Tổng hợp danh sách cảnh báo
    print(f"\n[*] Đang tổng hợp kết quả cảnh báo lỗ hổng...")
    alerts = zap.core.alerts(baseurl=target_url)
    
    alert_summary = {}
    for alert in alerts:
        risk = alert.get('risk', 'Informational')
        name = alert.get('name', 'Unknown')
        alert_summary[risk] = alert_summary.get(risk, 0) + 1

    print("\n" + "="*40)
    print("      TỔNG QUAN KẾT QUẢ QUÉT ZAP      ")
    print("="*40)
    print(f"Mục tiêu    : {target_url}")
    print(f"Tổng số lỗi : {len(alerts)}")
    for risk_level, count in alert_summary.items():
        print(f" - {risk_level:<12}: {count}")
    print("="*40)

    report_path = Path(args.report_file)
    if not report_path.is_absolute():
        report_path = (Path.cwd() / report_path).resolve()
    report_path.parent.mkdir(parents=True, exist_ok=True)

    # Xuất báo cáo
    print(f"\n[*] Đang xuất báo cáo định dạng {args.report_format.upper()} ra file: {report_path}")
    try:
        if args.report_format == "html":
            report = zap.core.htmlreport()
        elif args.report_format == "json":
            report = zap.core.jsonreport()
        elif args.report_format == "xml":
            report = zap.core.xmlreport()
        elif args.report_format == "md":
            report = zap.core.mdreport()
        
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"[+] Xuất báo cáo thành công tại: {report_path}")
    except Exception as e:
        print(f"[!] Có lỗi xảy ra khi xuất báo cáo: {e}")

if __name__ == "__main__":
    main()
