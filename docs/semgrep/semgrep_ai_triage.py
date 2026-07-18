import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Mapping, NamedTuple, Optional

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

class AiSettings(NamedTuple):
    provider: str
    model: str
    api_key: str
    base_url: Optional[str] = None

def load_env_file(env_file):
    """
    Đọc file .env đơn giản theo định dạng KEY=VALUE.
    Hàm này cố ý không ghi đè trực tiếp os.environ để dễ test và tránh side effect.
    """
    if not env_file:
        return {}

    env_path = Path(env_file)
    if not env_path.exists():
        return {}

    values = {}
    for raw_line in env_path.read_text(encoding='utf-8').splitlines():
        line = raw_line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        key, value = line.split('=', 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values

def find_default_env_file():
    """Tìm .env ở thư mục đang chạy hoặc cùng thư mục với script."""
    candidates = [
        Path.cwd() / '.env',
        Path(__file__).with_name('.env'),
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None

def get_ai_settings(env: Optional[Mapping[str, str]] = None, env_file=None):
    """
    Tạo cấu hình AI từ .env và biến môi trường.
    Biến môi trường thật được ưu tiên hơn file .env để dễ override khi chạy CI/terminal.
    """
    merged_env = {}
    default_env_file = find_default_env_file() if env_file is None else env_file
    merged_env.update(load_env_file(default_env_file))
    merged_env.update(dict(os.environ if env is None else env))

    provider = merged_env.get('AI_PROVIDER', 'gemini').strip().lower()
    default_model = 'gemini-2.5-flash' if provider == 'gemini' else ''
    model = merged_env.get('AI_MODEL', default_model).strip()

    if provider == 'gemini':
        api_key = merged_env.get('AI_API_KEY') or merged_env.get('GEMINI_API_KEY')
        base_url = None
    elif provider in {'openai-compatible', 'openai'}:
        provider = 'openai-compatible'
        api_key = (
            merged_env.get('AI_API_KEY')
            or merged_env.get('OPENROUTER_API_KEY')
            or merged_env.get('OPENAI_API_KEY')
        )
        base_url = (
            merged_env.get('OPENROUTER_BASE_URL')
            or merged_env.get('OPENAI_BASE_URL')
            or ''
        ).rstrip('/')
    else:
        raise ValueError("AI_PROVIDER chỉ hỗ trợ 'gemini' hoặc 'openai-compatible'.")

    if not model:
        raise ValueError('Chưa thiết lập AI_MODEL cho provider đã chọn.')
    if not api_key:
        if provider == 'gemini':
            raise ValueError('Chưa thiết lập AI_API_KEY hoặc GEMINI_API_KEY.')
        raise ValueError('Chưa thiết lập AI_API_KEY, OPENROUTER_API_KEY hoặc OPENAI_API_KEY.')
    if provider == 'openai-compatible' and not base_url:
        raise ValueError('Chưa thiết lập OPENROUTER_BASE_URL hoặc OPENAI_BASE_URL cho provider openai-compatible.')

    return AiSettings(provider=provider, model=model, api_key=api_key, base_url=base_url)

def generate_ai_response(prompt, settings):
    """Gọi provider AI đã cấu hình và trả về nội dung Markdown."""
    if settings.provider == 'gemini':
        try:
            from google import genai
        except ImportError as exc:
            raise RuntimeError("Vui lòng cài đặt thư viện mới nhất: pip install google-genai") from exc

        client = genai.Client(api_key=settings.api_key)
        response = client.models.generate_content(
            model=settings.model,
            contents=prompt
        )
        return response.text

    if settings.provider == 'openai-compatible':
        request_body = json.dumps(
            {
                'model': settings.model,
                'messages': [
                    {
                        'role': 'user',
                        'content': prompt,
                    }
                ],
            }
        ).encode('utf-8')
        request = urllib.request.Request(
            f"{settings.base_url}/chat/completions",
            data=request_body,
            headers={
                'Authorization': f"Bearer {settings.api_key}",
                'Content-Type': 'application/json',
            },
            method='POST',
        )
        try:
            with urllib.request.urlopen(request, timeout=90) as response:
                payload = json.loads(response.read().decode('utf-8'))
        except urllib.error.HTTPError as exc:
            body = exc.read().decode('utf-8', errors='replace')
            raise RuntimeError(f"Lỗi OpenAI-compatible API ({exc.code}): {body}") from exc

        return payload['choices'][0]['message']['content']

    raise ValueError(f"Provider không được hỗ trợ: {settings.provider}")

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

def make_report_slug(rule_id):
    """Tạo phần tên file an toàn từ rule id của Semgrep."""
    raw_slug = (rule_id or 'unknown-rule').split('.')[-1]
    return ''.join(char if char.isalnum() or char in {'-', '_'} else '-' for char in raw_slug)

def build_triage_prompt(finding):
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
    return rule_id, file_path, line, prompt

def triage_findings(findings, settings):
    """Gửi từng finding sang AI và ghi mỗi finding thành một report riêng."""
    output_files = []
    total = len(findings)

    for index, finding in enumerate(findings, start=1):
        rule_id, file_path, line, prompt = build_triage_prompt(finding)
        print(f"[{index}/{total}] Đang gửi dữ liệu phân tích cho lỗi [{rule_id}] tại {file_path} (dòng {line})...")
        print(f"Provider: {settings.provider} | Model: {settings.model}")
        try:
            ai_text = generate_ai_response(prompt, settings)
            output_file = f"AI_Triage_{index:03d}_{make_report_slug(rule_id)}.md"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"# AI Triage Report: {rule_id}\n\n")
                f.write(ai_text)

            output_files.append(output_file)
            print(f"[THÀNH CÔNG] Đã tạo báo cáo: {output_file}\n")
        except Exception as e:
            print(f"[THẤT BẠI] Lỗi khi gọi AI API cho finding {index}/{total}: {e}\n")

    return output_files

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

    # 2. Cấu hình AI provider/model/API key từ .env hoặc biến môi trường.
    try:
        settings = get_ai_settings()
    except ValueError as e:
        print(f"Lỗi cấu hình AI: {e}")
        print("Gợi ý: copy docs/semgrep/.env.example thành docs/semgrep/.env rồi điền API key.")
        sys.exit(1)
    
    output_files = triage_findings(findings, settings)
    print(f"Hoàn tất AI Triage: tạo {len(output_files)}/{len(findings)} báo cáo.")

if __name__ == "__main__":
    main()
