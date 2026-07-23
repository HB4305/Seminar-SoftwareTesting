# Checklist Kiểm Tra Hồ Sơ Nộp Bài - Group 06 T09

Cập nhật dựa trên các tài liệu trong `resources/`:

- `Seminar_Guide.docx`
- `T09_Security_Testing_(DAST_-_SAST).docx`
- `Seminar_Workflow_Briefing.pptx`
- `thaoluan1.md`
- `thaoluan2.md`
- `links.md`

Mục tiêu của checklist này là kiểm tra nhanh trong `submission/` còn thiếu gì trước khi đóng gói nộp bài.

## Tóm Tắt Yêu Cầu Bắt Buộc

- Seminar T09 phải thể hiện cả công cụ truyền thống và hướng AI-augmented.
- Demo live phải có ít nhất một feature truyền thống và một feature AI.
- Với T09, cần Semgrep/SAST, ZAP/DAST hoặc công cụ tương đương, AI triage/fuzzing/PoC/fix, và ít nhất 2 finding có thể tái lập bằng PoC hoặc testcase.
- `User_Guide.md` là Final Report theo trả lời của TA ngày 21/07/2026.
- Cần nộp Markdown để giảng viên/AI scan và PDF để giảng viên đọc trực tiếp.
- Cần có slide, video demo, báo cáo/User Guide, phân công công việc, AI Audit Report, AI Disclosure, Reflective Statement.
- Video demo được TA khuyến nghị upload YouTube, đánh số thứ tự hoặc thể hiện thứ tự demo trong slide. Lưu ý: bài đăng nộp cuối có dòng "No online links", nên nhóm cần xác nhận lại với TA nếu định chỉ nộp link YouTube.
- AI Audit Report đi theo template 5 phần: thông tin nhóm, bảng audit, tổng kết độ chính xác AI, kết luận, disclosure.
- Không dùng AI để bịa feedback, attendance, bằng chứng scan hoặc kết luận lỗ hổng.

## Trạng Thái Hiện Tại Trong `submission/`

| Hạng mục | File / Bằng chứng hiện có | Trạng thái | Còn thiếu / cần kiểm tra |
| --- | --- | --- | --- |
| Tool survey proposal S1 | `Tool_Survey_Proposal.md` | Có bản nội dung | Kiểm tra lại có đúng <= 1 trang khi xuất PDF không; bổ sung link nguồn chính thức nếu cần. |
| Phê duyệt S2 | Chưa thấy file/comment approval trong `submission/` | Thiếu bằng chứng | Thêm ghi chú/link/screenshot comment APPROVED hoặc scope note của TA/giảng viên. |
| Phân công nhóm | `Team_Work_Assignment.md` | Có | Cập nhật trạng thái không còn ở S3 nếu đã sang S4-S8; điền tên thật/người phụ trách cuối cho slide/video/worksheet. |
| User Guide / Final Report | `User_Guide.md` | Có, nội dung dài | Yêu cầu gốc ghi English; hiện file chủ yếu tiếng Việt. Nhóm cần quyết định dịch sang English hoặc xác nhận TA chấp nhận tiếng Việt. Cần xuất thêm PDF. |
| Demo screencast | `Demo_Screencast_Script.md` | Mới có kịch bản | Thiếu `Demo_Screencast.mp4` hoặc link YouTube đã xác nhận được phép nộp; cần 5-8 phút, 1080p ưu tiên, <= 100 MB nếu nộp file. |
| Slide seminar | `Seminar_Slides_Outline.md` | Mới có outline | Thiếu `Seminar_Slides.pptx`; slide <= 15, light theme/font dễ đọc, có thứ tự video/demo, thể hiện workflow Semgrep -> AI -> ZAP. |
| Activity worksheet | `Activity_Worksheet.md` | Có khung | Bảng 12 finding card còn trống; đáp án mới có 4 dòng. Cần điền đủ card, nhãn đúng, bằng chứng, ghi chú tái lập; bảo đảm làm được trong 20-25 phút. |
| Minute paper | `Minute_Paper_Template.md` | Có mẫu | In/phát hoặc chuẩn bị bản online; sau seminar cần thu feedback thật. |
| Audience feedback | `Audience_Feedback_Aggregated.md` | Có khung | Chỉ hoàn thành sau seminar; không được tự tạo dữ liệu nếu chưa thu thật. |
| Peer review | `Peer_Review.md` | Có mẫu | Chỉ nộp nếu lớp/TA yêu cầu hoặc đã có nhóm peer-review được phân công; cần >= 3 strengths, >= 3 suggestions, 1 câu hỏi khán giả. |
| AI Audit Report | `ai-audit/[AI-02]_AI_Audit_Report.md` | Có nội dung nhiều mục | Kiểm tra lại đúng 5 section template theo TA; các mục `INCOMPLETE` cần hoặc bổ sung evidence, hoặc ghi rõ là limitation được audit. |
| AI Disclosure | `ai-audit/[AI-03]_AI_Disclosure_Template.md` | Có nội dung cho 4 thành viên | Cần điền MSSV, chữ ký, ngày ký cuối; nếu nhóm thật có 5 thành viên thì thiếu thành viên 5; cần xuất `ai-audit/[AI-03]_AI_Disclosure.pdf`. |
| Reflective statement AI | `ai-audit/[AI-04]_Reflective_Statement.md` | Có | Kiểm tra độ dài khoảng 300 words English nếu bám guide gốc; hiện chủ yếu tiếng Việt. |
| Final reflection | `Final_Reflection.md` | Có khung | Nội dung còn trống; cần hoàn thành hoặc xác nhận với TA nếu được bỏ. |
| PDF bản nộp | Chỉ thấy PDF weekly reports ngoài `submission/` | Thiếu | Xuất PDF cho User Guide/Final Report và các phần bắt buộc khác nếu form yêu cầu PDF. |
| Đóng gói final | Chưa thấy file zip trong repo | Chưa làm | Kiểm tra giới hạn form: `GroupID.zip`, tối đa 20 files, mỗi file 20 MB; không commit API key hoặc `.env`. |

## Checklist Ưu Tiên Cao Trước Khi Nộp

- [ ] Tạo `Seminar_Slides.pptx` từ `Seminar_Slides_Outline.md`, tối đa 15 slide.
- [ ] Quay `Demo_Screencast.mp4` 5-8 phút hoặc chuẩn bị link YouTube sau khi xác nhận quy định link.
- [ ] Điền đủ 12 finding card và answer key trong `Activity_Worksheet.md`.
- [ ] Xuất `User_Guide.md` thành PDF vì TA yêu cầu có Markdown + PDF.
- [ ] Hoàn thiện `Final_Reflection.md` hoặc xác nhận được bỏ.
- [ ] Điền MSSV và chữ ký trong `[AI-03]`, sau đó xuất PDF.
- [ ] Bổ sung bằng chứng approval S2 của TA/giảng viên.
- [ ] Cập nhật `Team_Work_Assignment.md` sang trạng thái hiện tại và phân vai thuyết trình/demo/facilitator/timekeeper.
- [ ] Rà lại các mục `INCOMPLETE` trong `[AI-02]`: bổ sung log, screenshot, request/response, source evidence hoặc ghi rõ limitation.
- [ ] Kiểm tra ngôn ngữ yêu cầu: User Guide, Screencast narration, Reflective Statement trong guide gốc yêu cầu English.

## Checklist Nội Dung T09

- [ ] Có quy trình rõ: Semgrep scan source -> AI triage -> PoC/testcase -> ZAP/runtime validation -> report/fix.
- [ ] Có ít nhất 2 finding được tái lập bằng PoC hoặc testcase.
- [ ] Có Semgrep với OWASP Top-10 ruleset hoặc rule tương đương.
- [ ] Có ZAP baseline/passive/active/authenticated scan tùy scope đã duyệt.
- [ ] Có phần so sánh traditional vs AI-assisted: AI giúp gì, sai gì, con người kiểm chứng thế nào.
- [ ] Có ít nhất 3 troubleshooting items trong User Guide.
- [ ] Có ít nhất 3 failure modes thật: false positive, thiếu auth context, AI hallucination/fix sai, scan scope sai, duplicate findings.
- [ ] Mọi kết luận lỗ hổng đều có nguồn: Semgrep/ZAP output, source line, request/response log, screenshot hoặc testcase.

## Checklist Slide Và Demo Theo Feedback TA

- [ ] Dùng light theme hoặc bảo đảm contrast/font size dễ đọc.
- [ ] Không đưa thuật ngữ bất ngờ; giải thích SAST, DAST, false positive, triage, PoC trước khi dùng sâu.
- [ ] Slide phải cho thấy các file report/video liên kết với nhau theo thứ tự trình bày.
- [ ] Demo không hardcode quá đặc thù mà không giải thích cách áp dụng cho project khác.
- [ ] Nếu có nhiều video, đánh số thứ tự video hoặc thể hiện thứ tự trong slide.
- [ ] Có backup recording cho live demo.
- [ ] Có phân vai: presenter, demoer, facilitator, timekeeper.

## Checklist Đóng Gói Cuối

- [ ] `Tool_Survey_Proposal.md`
- [ ] `User_Guide.md`
- [ ] `User_Guide.pdf` hoặc `Final_Report.pdf`
- [ ] `Demo_Screencast.mp4` hoặc file/link theo quy định TA xác nhận
- [ ] `Activity_Worksheet.md`
- [ ] `Seminar_Slides.pptx`
- [ ] `Team_Work_Assignment.md`
- [ ] `Audience_Feedback_Aggregated.md` sau seminar
- [ ] `ai-audit/[AI-02]_AI_Audit_Report.md`
- [ ] `ai-audit/[AI-03]_AI_Disclosure.pdf`
- [ ] `ai-audit/[AI-04]_Reflective_Statement.md`
- [ ] `Final_Reflection.md` nếu không được bỏ
- [ ] Không có `.env`, API key, credential, target nhạy cảm trong gói nộp.
- [ ] Tên zip đúng format form nộp, ví dụ `Group06.zip`.
