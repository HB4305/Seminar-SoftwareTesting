import json
import os
import sys

# Yêu cầu cài đặt thư viện mới nhất trước khi chạy: pip install google-genai
try:
    from google import genai
except ImportError:
    print("Vui lòng cài đặt thư viện mới nhất: pip install google-genai")
    sys.exit(1)

def resolve_file_path(original_path):
    """
    Hàm giải quyết đường dẫn tuyệt đối hoặc không nhất quán trong JSON kết quả quét
    để tìm ra file thực tế trên đĩa của máy đang chạy hiện tại.
    """
    # 1. Thử đường dẫn gốc nếu nó tồn tại trực tiếp
    if os.path.exists(original_path):
        return original_path

    # 2. Chuẩn hóa đường dẫn gốc (thay \ bằng /)
    normalized = original_path.replace('\\', '/')
    parts = normalized.split('/')
    
    # 3. Trích xuất phần đuôi tương đối từ 'eshop-sut' hoặc 'backend'
    subpath = None
    if 'eshop-sut' in parts:
        idx = parts.index('eshop-sut')
        subpath = os.path.join(*parts[idx:])
    elif 'backend' in parts:
        idx = parts.index('backend')
        subpath = os.path.join('eshop-sut', *parts[idx:])
        
    if subpath:
        # Danh sách các vị trí tương đối phổ biến từ thư mục chạy script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        candidates = [
            # Chạy từ root của Seminar-SoftwareTesting: '../../EShop/eshop-sut/...'
            os.path.abspath(os.path.join(os.getcwd(), '..', 'EShop', subpath)),
            # Chạy từ docs/semgrep/: '../../../EShop/eshop-sut/...'
            os.path.abspath(os.path.join(os.getcwd(), '..', '..', 'EShop', subpath)),
            # Tương đối so với file script: '../../../EShop/eshop-sut/...'
            os.path.abspath(os.path.join(script_dir, '..', '..', '..', 'EShop', subpath)),
            # Tương đối trực tiếp nếu EShop nằm cùng cấp thư mục gốc học tập
            os.path.abspath(os.path.join(script_dir, '..', '..', '..', 'Kiểm thử phần mềm', 'EShop', subpath)),
            os.path.abspath(os.path.join(script_dir, '..', '..', '..', 'Kiß╗âm thß╗¡ phß║ºn mß╗üm', 'EShop', subpath))
        ]
        for candidate in candidates:
            if os.path.exists(candidate):
                return candidate
                
    # 4. Fallback cuối: Thử tìm theo tên file trong toàn thư mục cha
    filename = os.path.basename(normalized)
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
    for root, dirs, files in os.walk(parent_dir):
        if filename in files:
            full_path = os.path.join(root, filename)
            if 'eshop-sut' in full_path or 'EShop' in full_path:
                return full_path
                
    return None

def get_source_code_snippet(file_path, line_number, context_lines=5):
    """
    Đọc file nguồn trên đĩa và trích xuất đoạn mã xung quanh dòng lỗi.
    """
    if not file_path or not os.path.exists(file_path):
        return None
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        
        start_idx = max(0, line_number - context_lines - 1)
        end_idx = min(len(lines), line_number + context_lines)
        
        snippet_lines = []
        for i in range(start_idx, end_idx):
            line_num = i + 1
            marker = "=> " if line_num == line_number else "   "
            snippet_lines.append(f"{marker}{line_num}: {lines[i].rstrip()}")
            
        return '\n'.join(snippet_lines)
    except Exception as e:
        print(f"Lỗi khi đọc file nguồn {file_path}: {e}")
        return None

def main():
    # Kiểm tra xem người dùng có truyền file json vào không
    if len(sys.argv) < 2:
        print("Cách sử dụng: python semgrep_ai_triage.py <file_json_semgrep>")
        print("Ví dụ: python semgrep_ai_triage.py semgrep_results.json")
        sys.exit(1)

    json_file = sys.argv[1]
    
    # 1. Đọc file kết quả JSON do Semgrep xuất ra
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Lỗi khi đọc file {json_file}: {e}")
        sys.exit(1)
        
    findings = data.get("results", [])
    if not findings:
        print("Không tìm thấy lỗi bảo mật nào trong file JSON.")
        sys.exit(0)
        
    print(f"Tìm thấy {len(findings)} lỗi từ Semgrep. Bắt đầu quá trình AI Triage...\n")

    # 2. Cấu hình Gemini API
    # Lấy API Key từ biến môi trường để bảo mật, KHÔNG hardcode API Key vào source code!
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Lỗi: Chưa thiết lập biến môi trường GEMINI_API_KEY.")
        print("Vui lòng chạy lệnh sau trên Terminal trước khi chạy script:")
        print("export GEMINI_API_KEY='thay_api_key_cua_ban_vao_day'")
        sys.exit(1)
        
    try:
        client = genai.Client(api_key=api_key)
    except Exception as e:
        print(f"Lỗi khởi tạo Gemini Client: {e}")
        sys.exit(1)
        
    # Sử dụng model gemini-2.5-flash (model tiêu chuẩn mới nhất)
    model_name = 'gemini-2.5-flash'
    
    # 3. Tiến hành phân tích (Triage)
    # Trong demo, chúng ta sẽ Triage lỗi đầu tiên tìm được để tránh tốn quá nhiều request.
    # Trong thực tế, bạn có thể dùng vòng lặp `for finding in findings:` để xử lý tất cả.
    finding = findings[0]
    rule_id = finding.get("check_id")
    file_path = finding.get("path")
    line = finding.get("start", {}).get("line")
    message = finding.get("extra", {}).get("message")
    code_lines = finding.get("extra", {}).get("lines", "")

    # Fallback nếu code_lines bị ẩn ("requires login") hoặc trống
    if not code_lines or code_lines == "requires login":
        resolved_path = resolve_file_path(file_path)
        if resolved_path:
            print(f"-> Phát hiện trường 'lines' bị ẩn hoặc trống. Đang đọc trực tiếp từ file: {resolved_path}")
            code_lines = get_source_code_snippet(resolved_path, line)
        else:
            print(f"-> Cảnh báo: Không thể định vị file nguồn '{file_path}' trên hệ thống để fallback đọc trực tiếp.")
    
    # Chuẩn bị Prompt y hệt như những gì một Tester thực thụ cung cấp cho chuyên gia bảo mật
    prompt = f"""
Tôi dùng công cụ Semgrep (SAST) để quét mã nguồn và phát hiện một lỗ hổng bảo mật.
Bạn hãy đóng vai trò là một chuyên gia bảo mật ứng dụng (Application Security Expert) để thực hiện Triage (phân tích) lỗi này.

Thông tin kỹ thuật trích xuất từ Semgrep:
- Rule ID (Mã lỗi): {rule_id}
- Tệp tin: {file_path}
- Dòng báo lỗi: {line}
- Cảnh báo của Semgrep: {message}
- Đoạn mã nguồn bị lỗi (Source Code):
```
{code_lines}
```

Hãy cung cấp một báo cáo đánh giá chi tiết với các mục sau (Trình bày bằng Markdown):
1. **Giải thích lỗ hổng**: Giải thích ngắn gọn lỗi này là gì, tại sao đoạn code trên lại mắc lỗi.
2. **Proof of Concept (PoC)**: Viết một kịch bản/payload giả định để khai thác lỗi này.
3. **Mức độ ảnh hưởng (Impact)**: Nếu bị khai thác thì hậu quả là gì.
4. **Khuyến nghị khắc phục (Remediation)**: Viết lại đoạn code an toàn nhất để sửa lỗi trên.
"""
    
    print(f"Đang gửi dữ liệu phân tích cho lỗi [{rule_id}] tại {file_path} (dòng {line})...")
    try:
        # Gọi API của Gemini
        response = client.models.generate_content(
            model=model_name,
            contents=prompt
        )
        
        # 4. Lưu kết quả ra file Markdown
        output_file = f"AI_Triage_{rule_id.split('.')[-1]}.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# AI Triage Report: {rule_id}\n\n")
            f.write(response.text)
            
        print(f"\n[THÀNH CÔNG] Báo cáo AI Triage đã được tạo và lưu tại: {output_file}")
        print("Mở file Markdown trên để xem kết quả đánh giá, PoC và Code fix!")
        
    except Exception as e:
        print(f"Lỗi khi gọi Gemini API: {e}")

if __name__ == "__main__":
    main()
