# ZAP cho EShop: Lý thuyết, Thực hành và Kiểm chứng

Tài liệu này giải thích **ZAP đang làm gì**, **cách chạy đúng**, **cách biết mình đã dùng ZAP đúng hay sai**, và **so sánh GUI vs script** (`scan_zap.py`).

Liên quan:

- Hướng dẫn vận hành: [`src/zap/README.md`](../../src/zap/README.md)
- User Guide seminar: [`submission/User_Guide.md`](../../submission/User_Guide.md)

---

## 1. Lý thuyết nền

### 1.1 ZAP thuộc loại kiểm thử nào?

OWASP ZAP là công cụ **DAST** (Dynamic Application Security Testing):

- Kiểm thử trên **ứng dụng đang chạy** (HTTP request/response thật).
- Không đọc source code như Semgrep (SAST).
- Giả lập góc nhìn **attacker từ bên ngoài**: gửi request, quan sát phản hồi, tìm dấu hiệu lỗ hổng.

Trong workflow seminar:

```text
Semgrep (SAST, đọc code)  →  ZAP (DAST, chạy app)  →  PoC thủ công  →  so sánh AI vs fix thật
```

Hai công cụ **bổ sung**, không thay thế nhau:

- Semgrep có thể thấy SQLi trong code mà ZAP không báo.
- ZAP có thể thấy CORS/header sai mà Semgrep không thấy.

### 1.2 ZAP hoạt động theo mô hình gì?

ZAP có hai vai trò chính:

| Vai trò | Ý nghĩa |
| --- | --- |
| **Proxy** | Mọi HTTP request đi qua ZAP → ZAP ghi History, phân tích passive |
| **Scanner** | Spider crawl URL → passive scan → (tùy chọn) active scan bắn payload |

Luồng tổng quát:

```text
Target EShop
    → ZAP Proxy/Daemon
    → Traditional Spider
    → AJAX Spider (tùy chọn, SPA)
    → Passive Scan
    → Active Scan (tùy chọn)
    → Alerts + Report
```

### 1.3 Ba lớp scan — hiểu đúng để không nhầm “baseline”

| Lớp | Làm gì | An toàn? | Phát hiện gì |
| --- | --- | --- | --- |
| **Spider** | Crawl link, form, endpoint | An toàn | Mở rộng phạm vi URL |
| **Passive scan** | Phân tích traffic đã thu, **không** gửi payload tấn công | An toàn | Header thiếu, CORS, cookie, lộ thông tin |
| **Active scan** | Gửi payload SQLi/XSS/command… | **Có thể ảnh hưởng app** | Injection, XSS, lỗ hổng cần “đánh thử” |

**“ZAP baseline”** (OWASP chính thức, `zap-baseline.py`):

- Chỉ **Spider + Passive** — không active scan.
- Dùng cho CI/CD, sàng lọc nhanh.

**Script `scan_zap.py` trong repo**:

- Luôn chạy **Spider → Passive → Active**.
- **Không phải baseline thuần** — mạnh hơn, lâu hơn, có thể tạo thêm alert (và side effect).

| Cách chạy | Spider | Passive | Active |
| --- | --- | --- | --- |
| `zap-baseline.py` | ✓ | ✓ | ✗ |
| `scan_zap.py --scan-mode basic` | ✓ | ✓ | ✓ |

Hai cách **không cho cùng số alert** — đừng so sánh chéo mà không ghi rõ loại scan.

### 1.4 Context, Scope, Authentication

**Context** = phạm vi được phép scan. Script tạo context `EShop`, chỉ cho phép:

- Host: `localhost` / `127.0.0.1`
- Port: `3000`, `5173`, `5174`

→ Tránh ZAP scan nhầm ra internet hoặc port khác.

**Authentication** (frontend user/admin):

EShop dùng **JWT**. Script `scan_zap.py` làm:

1. POST `/api/login` qua ZAP proxy → lấy token.
2. Cấu hình **Replacer** gắn `Authorization: Bearer <token>` vào mọi request trong scope.
3. Bật **Forced User Mode** → ZAP luôn scan dưới user đó.

Nếu thiếu bước này, frontend SPA sau login **không được crawl** → alert ít, scan “sai” dù lệnh chạy thành công.

**AJAX Spider**:

React/Vite là SPA — nhiều route/API chỉ xuất hiện sau JavaScript chạy. Traditional spider không đủ → cần `--ajax-spider` cho `:5173` / `:5174`.

### 1.5 Alert là gì?

Mỗi **alert** = ZAP nghi ngờ một vấn đề bảo mật tại URL/parameter cụ thể.

| Trường | Ý nghĩa |
| --- | --- |
| Risk | High / Medium / Low / Informational |
| Confidence | Mức tin cậy của rule |
| URL + Parameter | Nơi phát hiện |
| Evidence | Header/body làm ZAP kết luận |

**Alert ≠ lỗi đã xác nhận.** Dev server (Vite HMR, thiếu CSP trên `robots.txt`…) thường tạo noise. Seminar yêu cầu **triage + PoC thủ công** vì lý do này.

### 1.6 GUI vs Script — cùng ZAP, khác cách điều khiển

| | ZAP GUI | `scan_zap.py` |
| --- | --- | --- |
| Khởi động ZAP | Bạn mở app | Script tự `docker run` (hoặc `--external-zap`) |
| Crawl | Automated Scan / Manual Explore | Spider + AJAX Spider qua API |
| Auth JWT | Phải cấu hình Context/Replacer thủ công | Script tự login + Replacer |
| Active scan | Quick Start “Attack” | Luôn chạy ở cuối pipeline |
| Report | Export thủ công | Tự ghi HTML/JSON + in alert summary |
| Evidence | Dễ xem History/Alerts trực quan | Log terminal + file output |
| Lặp lại | Khó reproduce y hệt | Command + `.env` reproduce được |

**Cùng engine ZAP** — khác workflow và mức tự động hóa.

### 1.7 Khi nào coi là “dùng ZAP đúng”?

Đúng không chỉ là “chạy xong không lỗi”, mà còn:

1. **Target đúng** — backend `:3000`, frontend user `:5173`, admin `:5174`.
2. **Scope đúng** — alert thuộc target vừa scan, không lẫn session cũ.
3. **Coverage đúng** — SPA có auth thì phải có login + AJAX Spider.
4. **Scan type đúng** — biết mình đang chạy passive-only hay có active.
5. **Kết quả có thể kiểm chứng** — có report, alert counts, và ít nhất 1 alert được PoC lại.

---

## 2. Chuẩn bị môi trường

Chạy từ root repo `Seminar-SoftwareTesting`:

```bash
cd Seminar-SoftwareTesting
source .venv/bin/activate
python -m pip install python-owasp-zap-v2.4
docker pull ghcr.io/zaproxy/zaproxy:stable
mkdir -p src/zap/output
cp src/zap/.env.example src/zap/.env   # nếu chưa có
```

**Bật EShop** trước mọi scan:

| Service | URL |
| --- | --- |
| Backend API | `http://localhost:3000` |
| Frontend user | `http://localhost:5173` |
| Frontend admin | `http://localhost:5174` |

Kiểm tra nhanh:

```bash
curl -s -o /dev/null -w "backend: %{http_code}\n" http://localhost:3000/api/products
curl -s -o /dev/null -w "frontend user: %{http_code}\n" http://localhost:5173/
curl -s -o /dev/null -w "frontend admin: %{http_code}\n" http://localhost:5174/
```

Kỳ vọng: mã **khác `000`**. Nếu `000` → EShop chưa chạy.

Credential mặc định (có thể override trong `.env`):

| Role | Email | Password |
| --- | --- | --- |
| user | `test@eshop.com` | `Test1234!` |
| admin | `admin@eshop.com` | `Admin123!` |

---

## 3. Chạy bằng Script (flow chính)

### 3.1 Backend (API, không auth)

```bash
python src/zap/scan_zap.py \
  --target http://localhost:3000 \
  --scan-mode basic \
  --report-format json \
  --output-file src/zap/output/backend_basic.json
```

**Check sau bước này:**

| Check | Đúng | Sai |
| --- | --- | --- |
| Terminal in `[+] Connected to ZAP` | ✓ | Docker/ZAP lỗi |
| Thấy `[1/4] TRADITIONAL SPIDER` → 100% | ✓ | Target không reachable |
| Thấy `Skipping AJAX Spider` | ✓ (backend không cần) | — |
| Thấy `[4/4] ACTIVE SCAN` → 100% | ✓ | Active scan treo/timeout |
| Block `ZAP SCAN SUMMARY` với Total alerts | ✓ | Scan chưa xong |
| File `src/zap/output/backend_basic.json` tồn tại | ✓ | Report generation fail |

### 3.2 Frontend user (SPA + auth)

```bash
python src/zap/scan_zap.py \
  --target http://localhost:5173 \
  --auth-role user \
  --forced-user \
  --ajax-spider \
  --scan-mode basic \
  --report-format json \
  --output-file src/zap/output/frontend_user_basic.json
```

**Check thêm so với backend:**

| Check | Đúng | Sai |
| --- | --- | --- |
| Không lỗi `EShop login failed` | ✓ | Sai password hoặc backend down |
| Không lỗi `Authentication verification failed` | ✓ | JWT/Replacer hỏng |
| Thấy `AJAX Spider` chạy (không skip) | ✓ | Thiếu `--ajax-spider` |
| Alert có URL `:5173` | ✓ | Chỉ có `:3000` → session/target sai |

### 3.3 Frontend admin (tùy chọn)

```bash
python src/zap/scan_zap.py \
  --target http://localhost:5174 \
  --auth-role admin \
  --forced-user \
  --ajax-spider \
  --scan-mode basic \
  --report-format json \
  --output-file src/zap/output/frontend_admin_basic.json
```

### 3.4 Thu alert counts

Ghi bảng từ block terminal:

```text
========================================
          ZAP SCAN SUMMARY
========================================
Target       : http://localhost:3000
Total alerts : N
 - High       : ...
 - Medium     : ...
========================================
```

Mỗi target **một dòng** trong bảng evidence — không cộng chung nếu chưa chắc scope sạch.

Triage offline (tùy chọn):

```bash
python src/zap/ai_triage_zap.py \
  --input src/zap/output/backend_basic.json \
  --offline
```

Output mặc định: `src/zap/output/zap_ai_triage_report.md`

---

## 4. Chạy với `--external-zap`

Khi dùng `--external-zap`, **bạn tự khởi động ZAP trước** — script chỉ kết nối, không tự `docker run`.

### 4.1 Khởi động ZAP daemon

**Docker (daemon nền):**

```bash
mkdir -p src/zap/output

docker run --rm -d --name eshop-zap-external \
  --network host \
  -v "$(pwd)/src/zap/output:/zap/wrk" \
  ghcr.io/zaproxy/zaproxy:stable \
  zap.sh -daemon -port 8090 -host 0.0.0.0 -config api.disablekey=true
```

**ZAP Desktop GUI:** mở ZAP → session mới → API mặc định tại `http://localhost:8090`.

Kiểm tra ZAP sẵn sàng:

```bash
curl -s http://localhost:8090/JSON/core/view/version/
```

### 4.2 Chạy scan

```bash
python src/zap/scan_zap.py \
  --target http://localhost:5173 \
  --auth-role user \
  --forced-user \
  --ajax-spider \
  --external-zap \
  --zap-url http://localhost:8090 \
  --output-file src/zap/output/frontend_user_basic.json
```

Nếu ZAP bật API key:

```bash
python src/zap/scan_zap.py \
  --target http://localhost:3000 \
  --external-zap \
  --zap-url http://localhost:8090 \
  --api-key YOUR_ZAP_API_KEY \
  --output-file src/zap/output/backend_basic.json
```

**Cách lấy API Key từ ZAP Desktop GUI:**

1. **Tools** → **Options...**
2. Mục **API** bên trái
3. Copy **API Key** (hoặc bấm *Generate*)

### 4.3 Khác biệt so với flow mặc định

| | Mặc định | `--external-zap` |
| --- | --- | --- |
| Ai start ZAP? | Script | Bạn |
| Cần Docker khi scan? | Có | Không (trừ khi bạn dùng Docker cho ZAP) |
| API key | Tự tắt | Tùy cấu hình ZAP |
| Mount output | Script tự mount | Bạn mount nếu ZAP chạy trong Docker |
| Dọn JWT sau auth | Script cleanup | JWT có thể còn trong history/session |
| Report sạch | Container mới mỗi lần | Nên session mới hoặc clear history |

---

## 5. Chạy bằng GUI (đối chiếu)

### 5.1 Backend — tương đương script không auth

1. Mở ZAP → session mới.
2. **Quick Start → Automated Scan**.
3. URL: `http://localhost:3000` → **Attack**.
4. Đợi Spider + Passive + Active xong.
5. Tab **Alerts** → đếm theo risk.
6. **Report → Generate Report** → export HTML/JSON.

### 5.2 Frontend user — cần thêm auth

Automated Scan `:5173` **không auth** thường **ít alert hơn script** — đó là hành vi đúng.

Để GUI gần với script:

1. Tạo **Context** `EShop`, include `http://localhost:5173.*`
2. Lấy JWT:

```bash
curl -s -X POST http://localhost:3000/api/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@eshop.com","password":"Test1234!"}'
```

3. **Replacer**: thêm header `Authorization: Bearer <token>`
4. Chạy **AJAX Spider** + active scan trong context
5. Bật **Forced User Mode** nếu đã cấu hình user trong context

### 5.3 So sánh GUI vs Script

| Tiêu chí | GUI | Script |
| --- | --- | --- |
| Spider + Active | Có (Automated Scan) | Có |
| Context scope tự giới hạn | Phải cấu hình tay | Có sẵn |
| Auth JWT | Phức tạp | `--auth-role` |
| AJAX Spider SPA | Bật riêng | `--ajax-spider` |
| Alert summary | Đếm tay | In sẵn cuối log |
| Reproduce | Khó | Một command |

---

## 6. Baseline official (passive only)

Nếu cần đúng nghĩa **baseline** (không active scan):

```bash
docker run --rm --network host \
  -v "$(pwd)/src/zap/output:/zap/wrk:rw" \
  ghcr.io/zaproxy/zaproxy:stable \
  zap-baseline.py \
    -t http://localhost:3000 \
    -J /zap/wrk/backend_baseline.json \
    -r /zap/wrk/backend_baseline.html
```

Lưu ý: baseline **không đăng nhập SPA tốt** — frontend authenticated vẫn nên dùng `scan_zap.py`.

---

## 7. Checklist “đúng hay sai”

### A. Trước khi scan

- [ ] EShop trả HTTP (không `000`)
- [ ] Docker chạy (nếu không dùng `--external-zap`)
- [ ] Mỗi target có file output riêng
- [ ] Frontend scan có `--auth-role` + `--forced-user` + `--ajax-spider`

### B. Trong lúc scan (script)

- [ ] `Connected to ZAP`
- [ ] Spider 100%
- [ ] Passive scan completed
- [ ] Active scan 100%
- [ ] `ZAP SCAN SUMMARY` in ra
- [ ] Report file được tạo

### C. Sau khi scan

- [ ] Alert URL khớp target (`:3000` / `:5173` / `:5174`)
- [ ] Với frontend: có request `/api/...` kèm `Authorization` (nếu xem GUI/external ZAP)
- [ ] Không trộn alert từ lần scan cũ
- [ ] Chọn 1–2 alert → PoC bằng curl/browser

### D. Dấu hiệu “chạy xong nhưng sai”

| Triệu chứng | Nguyên nhân thường gặp |
| --- | --- |
| Total alerts = 0 hoặc rất ít trên frontend | Thiếu auth hoặc thiếu AJAX Spider |
| Alert toàn `:3000` khi scan `:5173` | Session ZAP cũ / external ZAP chưa clear |
| `EShop login failed` | Backend down hoặc sai password trong `.env` |
| `Replacer API unavailable` | ZAP daemon thiếu add-on |
| Report rỗng / không tạo file | Mount path sai (external Docker) |
| Nhiều CSP/HSTS trên Vite dev | Noise dev server — ghi chú môi trường |

---

## 8. So sánh ba cách chạy

| Cách | Passive only? | Active? | Auth JWT | Reproduce | Phù hợp seminar |
| --- | --- | --- | --- | --- | --- |
| `zap-baseline.py` | ✓ | ✗ | Khó | Cao | Mục “baseline” thuần |
| `scan_zap.py` | ✓ | ✓ | ✓ (flag) | Rất cao | **Flow chính nhóm** |
| ZAP GUI Automated Scan | ✓ | ✓ | Phải làm tay | Trung bình | Học + demo trực quan |

---

## 9. Luồng kiểm chứng đầy đủ (4 mục yêu cầu seminar)

```text
1. ZAP (script)     → alert counts + report JSON
2. Semgrep          → classify findings (p/owasp-top-ten)
3. PoC thủ công     → SQLi hoặc stored-XSS
4. So sánh          → AI triage vs fix code thật
```

Thứ tự gợi ý:

1. Bật EShop
2. `scan_zap.py` backend → ghi alert counts
3. `scan_zap.py` frontend user → ghi alert counts
4. Semgrep `p/owasp-top-ten` trên `../eshop-sut`
5. Chọn 1 finding → PoC → fix
6. Chạy lại PoC / scan ngắn để chứng minh “after fix”
7. Đối chiếu `zap_ai_triage_report.md` / `semgrep_triage_report.md` với diff code

### PoC SQLi (tham khảo)

```bash
curl -i "http://localhost:3000/api/products?search=' OR '1'='1"
```

### Bảng evidence mẫu

| Target | Scan type | Total | High | Medium | Low | Info | Report file |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `:3000` | basic | | | | | | `backend_basic.json` |
| `:5173` | basic + auth | | | | | | `frontend_user_basic.json` |
| `:5174` | basic + auth | | | | | | `frontend_admin_basic.json` |

---

## 10. Tóm tắt

**Dùng ZAP đúng** = target + auth + spider phù hợp (AJAX cho SPA) + hiểu passive vs active + alert được triage bằng PoC — không chỉ là “chạy lệnh không crash”.

**Script vs GUI:** cùng engine ZAP; script của repo tự động hóa context, JWT, AJAX Spider và export report — phù hợp reproduce và nộp evidence seminar hơn GUI Quick Start đơn giản.
