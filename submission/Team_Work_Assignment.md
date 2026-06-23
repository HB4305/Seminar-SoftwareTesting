# Team Work Assignment - T09 Security Testing

## Trạng thái hiện tại

Nhóm đã qua **Stage S1** và **Stage S2**. Hiện nhóm đang ở **Stage S3 - Deep study & hands-on practice**.

Đề tài: `T09 - Security Testing (DAST / SAST)`

Workflow chung dự kiến:

1. Chạy Semgrep theo hướng SAST trên source code EShop.
2. Chạy OWASP ZAP baseline scan theo hướng DAST trên EShop đang chạy.
3. Dùng Gemini để triage finding, giải thích lỗi, draft PoC exploit và gợi ý fix.
4. Reproduce finding bằng test case hoặc PoC.
5. Tổng hợp evidence, report, slide, demo, worksheet và AI audit.

## Timeline, Stage và Output

| Stage | Trạng thái | Deadline / mốc | Output chính |
| --- | --- | --- | --- |
| S1 - Topic claim & tool survey | Đã xong | Week 6, Sat 23:59 hoặc trong 5 ngày làm việc sau khi claim topic | `Tool_Survey_Proposal.md`: shortlist tool, ma trận so sánh, lý do chọn Semgrep + ZAP + Gemini, AI disclosure |
| S2 - Instructor / TA review | Đã xong | Week 6 giữa tuần; TA/giảng viên phản hồi trong 2 ngày làm việc | Tool list và scope được duyệt để chuyển sang S3 |
| S3 - Deep study & hands-on practice | Đang làm | Weeks 6-10; nội bộ nên xong trước `T_seminar - 7 ngày làm việc` | Hoàn thành M1-M5: install/hello world, EShop scenario, 3 failure modes, AI-assisted variant, metrics |
| S4 - User guide + demo recording | Sắp làm | Trước S5; nội bộ nên xong trước `T_seminar - 5 ngày làm việc` | `User_Guide.md` >= 6 sections; `Demo_Screencast.mp4` 5-8 phút, <= 100 MB |
| S5 - Pre-seminar sharing | Chưa làm | Ít nhất 3 ngày làm việc trước `T_seminar` | Upload `User_Guide.md`, screencast, `Activity_Worksheet.md`, `Seminar_Slides.pptx` |
| S6 - Live seminar 45 phút | Chưa làm | `T_seminar`, Week 7-11 | Pitch 10 phút, live demo 10 phút, activity 20 phút, Q&A/debrief 5 phút |
| S7 - Audience activity & feedback | Chưa làm | Trong/cuối buổi seminar | Activity worksheet đã làm trên lớp, 1-minute paper feedback, rating 1-5 |
| S8 - Reflection + AI audit | Chưa làm | Trong 5 ngày làm việc sau `T_seminar` | `[AI-02]`, `[AI-03]`, `[AI-04]`, `Audience_Feedback_Aggregated.md`, `Final_Reflection.md` |

`T_seminar` là ngày seminar live cụ thể do giảng viên xếp lịch.

## S3 Deep Study Milestones

Các mốc dưới đây bám theo yêu cầu S3 trong `resources/Seminar_Workflow_Briefing.pptx` và được lồng vào 2 pha làm việc của nhóm.

| Milestone | Việc cần làm trong nhóm | Output bắt buộc |
| --- | --- | --- |
| M1 - Install tool + official hello world | Mỗi track cài/chạy công cụ chính: Track A chạy Semgrep sample/official quick start; Track B chạy ZAP baseline sample hoặc official quick start; cả nhóm thử Gemini prompt mẫu | Setup notes, command/screenshot hello world, lỗi cài đặt nếu có và cách xử lý |
| M2 - Run one end-to-end scenario against EShop | Mỗi thành viên chọn 1 testcase/finding ở Pha 2 và chạy qua workflow trên EShop | Evidence cho scenario: Semgrep/ZAP note, AI triage note, PoC/reproducer hoặc reasoning, report draft |
| M3 - Document 3 real failure modes observed | Nhóm ghi lại ít nhất 3 failure modes quan sát được khi dùng tool/AI/workflow | Failure modes list, ví dụ: false positive, ZAP thiếu endpoint/auth context, AI hallucination/fix sai ngữ cảnh |
| M4 - Reproduce same scenario with AI variant | Với cùng scenario, chạy luồng truyền thống trước rồi dùng Gemini để triage, sinh PoC/fix và audit output | So sánh traditional vs AI-assisted: AI giúp gì, sai gì, phần nào con người phải kiểm chứng |
| M5 - Capture metrics | Mỗi track/case ghi lại setup time, scan/run time và stability/flake note | Metrics table: setup time, run time, số findings/alerts, flake rate hoặc ghi chú kết quả có ổn định không |

## Yêu cầu năng lực từ brief T09

Đến cuối seminar, **mỗi thành viên** phải có thể:

- Run OWASP ZAP baseline scan against EShop và triage report.
- Configure Semgrep với OWASP Top-10 ruleset trên EShop repo.
- Reproduce 2 real findings dưới dạng test cases, ưu tiên SQLi, XSS hoặc weak auth.
- Use AI tools để draft PoC exploit và fix, sau đó audit cả PoC lẫn fix.
- Discuss responsibility line: tester vs developer vs SOC.

Vì vậy S3 được chia thành 2 pha: học công cụ trước, sau đó mỗi người làm một nhóm testcase end-to-end.

## Pha 1 - Học công cụ theo 2 track và seminar nội bộ

Mục tiêu: 4 thành viên chia thành 2 cặp để tìm hiểu sâu 2 luồng chính. Mỗi cặp không chỉ học tool scan, mà phải đi qua luôn AI triage và report để tạo playbook có thể dùng lại ở Pha 2.

| Track | Thành viên | Mảng tìm hiểu sâu | Demo ngắn cần có | Output Pha 1 |
| --- | --- | --- | --- | --- |
| Track A - Semgrep flow | Thành viên 1 + Thành viên 3 | Semgrep/SAST + AI triage + report | Chạy Semgrep với OWASP Top-10 ruleset, chọn 1 finding, đưa vào Gemini triage, viết report ngắn | Semgrep command, Semgrep finding note, AI triage note, report template mẫu cho source-level finding |
| Track B - ZAP flow | Thành viên 2 + Thành viên 4 | ZAP/DAST + AI triage + report | Chạy hoặc mở ZAP baseline report, chọn 1 alert, đưa vào Gemini triage, viết report ngắn | ZAP target config, ZAP alert note, AI triage note, report template mẫu cho runtime alert |

Sau Pha 1, nhóm phải chốt workflow chi tiết:

`Semgrep/ZAP finding -> AI triage -> PoC/reproducer hoặc reasoning -> source/runtime evidence -> conclusion -> report/finding card`

Mỗi thành viên cần ghi lại:

- Thao tác tối thiểu để dùng từng công cụ.
- Output cần đọc và cách nhận biết output đáng tin.
- Prompt AI triage đã dùng và cách audit output AI.
- Report format để người khác làm theo.
- Ít nhất 1 failure mode của track mình phụ trách.

Output Pha 1 phải đủ 3 phần để các thành viên khác dùng lại ở Pha 2:

| Track | Nội dung tìm hiểu | Workflow thao tác cần bàn giao | Format đầu ra/template |
| --- | --- | --- | --- |
| Track A - Semgrep + AI triage + report | SAST, Semgrep OWASP Top-10 ruleset, cách đọc finding, false positive, prompt triage cho source finding, report source-level issue | Cài/chạy Semgrep -> chọn config `p/owasp-top-ten` -> scan EShop repo -> chọn finding -> prompt Gemini -> audit PoC/fix -> ghi source evidence -> report | `Semgrep Finding Note`, `AI Triage Note`, `Finding Report` cho source-level finding |
| Track B - ZAP + AI triage + report | DAST, ZAP baseline/passive/active scan, target config, alert triage, prompt triage cho runtime alert, report runtime issue | Chạy EShop -> cấu hình target -> chạy ZAP baseline -> chọn alert -> prompt Gemini -> audit PoC/fix -> ghi runtime evidence -> report | `ZAP Alert Note`, `AI Triage Note`, `Finding Report` cho runtime alert |

## Pha 2 - Thực hiện end-to-end nhóm testcase

Mục tiêu: mỗi thành viên sở hữu một nhóm testcase/finding riêng và tự đi qua workflow end-to-end. Nếu tool không phát hiện được case đó, phải ghi rõ đã chạy gì, output là gì và vì sao không áp dụng được.

| Thành viên | Nhóm testcase đề xuất | Output Pha 2 |
| --- | --- | --- |
| Thành viên 1 | SQL Injection hoặc insecure query pattern | Semgrep/ZAP notes, AI triage, PoC/reproducer, fix audit, report, 2 finding cards, slide/demo |
| Thành viên 2 | XSS, input validation hoặc runtime alert | ZAP/Semgrep notes, AI triage, PoC/reproducer, fix audit, report, 2 finding cards, slide/demo |
| Thành viên 3 | Weak auth, OTP, session hoặc auth-related finding | Source/ZAP/Semgrep evidence, AI triage sâu, PoC/fix audit, report, 2 finding cards, slide/demo |
| Thành viên 4 | Weak hashing, secret/config exposure hoặc false positive case | Semgrep evidence cho weak hashing/secret/config, ZAP baseline note hoặc lý do ZAP không detect, AI triage/audit, PoC/reproducer hoặc reasoning, evidence chain, severity/impact, report, 2 finding cards, slide/demo |

Mọi case ở Pha 2 đều phải có ít nhất `Semgrep Finding Note` và `ZAP Alert Note` hoặc ghi rõ tool không phát hiện/không phù hợp với case đó.

Mỗi thành viên phải reproduce ít nhất 2 findings:

- 1 finding thuộc testcase của mình.
- 1 finding thuộc testcase của người mình validate chéo.

## Validate chéo

| Case owner | Người validate | Nội dung validate |
| --- | --- | --- |
| Thành viên 1 | Thành viên 2 | Command scan, evidence, AI triage, PoC/reproducer, report conclusion |
| Thành viên 2 | Thành viên 4 | ZAP/runtime evidence, source/runtime đối chiếu, severity, expected/actual result |
| Thành viên 3 | Thành viên 1 | Prompt, PoC/fix suggestion, source evidence, AI hallucination audit |
| Thành viên 4 | Thành viên 3 | Evidence chain, reproducibility checklist, severity/impact, conclusion |

Người validate phải để lại bằng chứng: checklist, command/output, screenshot, comment hoặc ghi chú vì sao không tái lập được.

## Output chung cần hoàn thành

- `User_Guide.md`: mỗi người viết phần liên quan đến công cụ/case của mình.
- `Seminar_Slides.pptx`: mỗi người 2-3 slide, tổng slide <= 15.
- `Activity_Worksheet.md`: mỗi người đóng góp ít nhất 2 finding cards; thành viên 4 tổng hợp layout.
- `Demo_Screencast.mp4`: 5-8 phút, có traditional tool và AI tool.
- AI audit/disclosure: mỗi người ghi lại tool, prompt summary, output, phần đã kiểm chứng.

## Lịch làm việc nội bộ đề xuất cho S3

| Buổi | Mục tiêu | Output |
| --- | --- | --- |
| Buổi 1 | Chốt scope, chia 2 track Pha 1, thống nhất format notes/screenshot/evidence; bắt đầu M1 | Danh sách thành viên theo track, checklist học sơ track còn lại, setup/hello-world notes |
| Buổi 2 | Seminar nội bộ 2 track; hoàn tất M1 và chốt workflow cho M2/M4 | Playbook từng track, demo ngắn, workflow chi tiết, prompt/report templates |
| Buổi 3 | Chia nhóm testcase và làm end-to-end song song; thực hiện M2/M4/M5 | Evidence, PoC/reproducer, AI triage, report draft, finding cards, metrics table |
| Buổi 4 | Validate chéo, ghi M3 failure modes, ghép tài liệu, chạy thử seminar/activity | Bản gần hoàn chỉnh của guide, slide, worksheet, AI audit notes, failure modes list |
