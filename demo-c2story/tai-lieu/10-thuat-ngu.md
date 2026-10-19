# 10 — Thuật ngữ

| Thuật ngữ | Định nghĩa |
|---|---|
| **Project (Dự án)** | Không gian làm việc chuyển thể một truyện dài, gồm bản thảo, chương, thế giới truyện, tư liệu và video |
| **SSO (Single Sign-On)** | Hệ thống đăng nhập một lần có sẵn, dùng chung cho nhiều ứng dụng; ứng dụng này chỉ tích hợp, không tự xây đăng nhập |
| **OIDC (OpenID Connect)** | Chuẩn xác thực trên nền OAuth 2.0; ứng dụng là *Relying Party*, SSO là *OpenID Provider* |
| **PKCE** | Cơ chế chống đánh cắp authorization code trong luồng Authorization Code |
| **BFF (Backend-for-Frontend)** | Mẫu thiết kế giữ token SSO ở server; trình duyệt chỉ giữ cookie phiên |
| **JIT provisioning** | Tự tạo hồ sơ cục bộ ở lần đăng nhập đầu tiên từ thông tin (claims) của SSO |
| **Back-channel logout** | SSO gọi trực tiếp tới server ứng dụng để báo đăng xuất |
| **Owner / Editor** | Vai trò trong dự án: chủ sở hữu (toàn quyền) / cộng tác viên (sửa nội dung, sinh nội dung) |
| **Source text (Văn bản gốc)** | Văn bản người dùng import, trước khi chia chương |
| **Workspace** | Trình soạn thảo liền mạch hiển thị mọi chương trên một trang cuộn |
| **Chapter (Chương)** | Phần văn bản liên tục; đơn vị để lập storyboard, sinh tư liệu và dựng video |
| **Restructure** | Thao tác thay đổi cấu trúc chương (chia, gộp, dời ranh giới, sắp xếp) thực hiện nguyên tử |
| **Archive** | Ảnh chụp chỉ đọc của toàn bộ bản thảo tại một thời điểm |
| **Story Assets** | Tài sản thế giới truyện của dự án: nhân vật (Character), địa điểm (Location), đạo cụ (Prop), nhóm (Group) |
| **Reference image (Ảnh tham chiếu)** | Ảnh chuẩn của tài sản, đính kèm khi sinh mọi ảnh shot để giữ nhất quán |
| **Facts** | Đặc điểm bất biến của tài sản (vd. "tóc đen ngang vai", "sẹo ở má trái") luôn được chèn vào prompt |
| **Art Direction** | Chỉ dẫn phong cách bổ sung lên style của dự án |
| **Visual Rules** | Luật hình ảnh có điều kiện, áp toàn dự án hoặc theo chương |
| **Chapter rules** | Chỉ dẫn cố định cho một chương, Director tuân theo khi viết brief |
| **Story timeline** | Dòng thời gian truyện (ngày, mùa) gán cho từng chương |
| **Relationship graph** | Đồ thị quan hệ giữa các nhân vật và diễn biến quan hệ |
| **Storyboard draft (Bản nháp storyboard)** | Một phương án chia chương thành các shot; mỗi chương có nhiều bản nháp, một bản hiện hành |
| **Shot** | Một ảnh minh họa gắn với một đoạn văn nguồn; trên timeline là 1 clip ảnh + 1 clip thuyết minh |
| **Illustration brief** | Mô tả có cấu trúc để sinh ảnh: Subject / Environment / Composition / Camera / Lighting / Mood / Details |
| **Caption** | Mô tả ngắn 1–2 câu của shot, dùng trong storyboard (không dùng cho audio) |
| **Re-direct** | Viết lại brief mọi shot của chương |
| **Sinh tư liệu** | Bước 4 của luồng: storyboard tự động, rồi sinh ảnh + thuyết minh nguyên văn cho từng shot |
| **Media bin (Tư liệu dự án)** | Danh sách ảnh và audio thuyết minh theo chương/shot; đầu vào của trình chỉnh sửa |
| **Sẵn sàng dựng** | Trạng thái chương khi mọi shot có ảnh và thuyết minh đạt |
| **Đoạn nguồn (Source segment)** | Khoảng văn bản `[sourceStart, sourceEnd)` của chương gắn với một shot; là thứ được đọc trong video |
| **Phủ kín (Full coverage)** | Bất biến: các đoạn nguồn của storyboard hiện hành nối lại đúng bằng văn bản chương |
| **Thuyết minh nguyên văn (Verbatim narration)** | Audio đọc đúng từng chữ của đoạn nguồn; không chỉnh sửa, không tóm tắt |
| **Bản đọc (Spoken form)** | Biểu diễn dùng cho TTS (SSML, cách đọc số, từ điển phát âm); không đổi nội dung chữ |
| **Từ điển phát âm** | Cặp *từ viết → cách đọc* theo dự án; chỉ ảnh hưởng audio |
| **Forced alignment** | Căn timestamp từng từ giữa audio và văn bản đã biết |
| **WER (Word Error Rate)** | Tỷ lệ lỗi từ giữa văn bản gốc và nội dung STT nghe được từ audio; dùng để kiểm chứng TTS |
| **NEEDS_REVIEW / ACCEPTED** | Trạng thái thuyết minh vượt ngưỡng WER / đã được người dùng chấp nhận thủ công |
| **Trình chỉnh sửa video (Editor)** | Công cụ dựng video trên timeline nhiều track: ảnh, thuyết minh (khóa), phụ đề, nhạc nền, SFX, overlay |
| **Timeline / Track / Clip (item)** | Trục thời gian của video; mỗi track chứa các clip cùng loại |
| **SFX (Sound effect)** | Hiệu ứng âm thanh ngắn (tiếng mưa, bước chân, pháo hoa…) đặt tại thời điểm cụ thể |
| **Khóa thuyết minh** | Ràng buộc BR-24: clip thuyết minh không thể cắt, xóa, đảo, đổi tốc độ |
| **Loudness (LUFS)** | Độ to cảm nhận của âm thanh; chuẩn hóa về −14 LUFS cho mạng xã hội |
| **Ken Burns** | Hiệu ứng zoom/lia chậm trên ảnh tĩnh |
| **Chuyển cảnh (Transition)** | Hiệu ứng nối hai clip ảnh (fade, crossfade, wipe…) |
| **Ducking** | Tự giảm âm lượng nhạc nền khi có lời đọc |
| **Timeline snapshot** | JSON mô tả đầy đủ một phiên bản timeline, dùng để xuất video |
| **Render** | Bản MP4 xuất từ timeline (có phiên bản) |
| **AI Director** | Trợ lý AI điều phối quy trình, nhận lệnh bằng ngôn ngữ tự nhiên và chạy chế độ tự động có điểm duyệt |
| **Điểm duyệt (Checkpoint)** | Bước Director dừng chờ người dùng quyết định (chọn style, duyệt cast, xác nhận chi phí) |
| **Credit** | Đơn vị thanh toán nội bộ cho thao tác AI |
| **Hold / Capture / Release** | Giữ / trừ thật / hoàn credit của một job |
| **Ledger (Sổ cái)** | Bảng ghi thêm (append-only) mọi biến động credit |
| **Job** | Tác vụ bất đồng bộ (thường gọi AI) có vòng đời và chi phí |
| **AI Gateway** | Lớp nội bộ chuẩn hóa việc gọi nhiều nhà cung cấp AI |
| **Adapter / Port** | Mẫu thiết kế tách interface (port) khỏi cài đặt theo provider (adapter) |
| **Outbox pattern** | Ghi sự kiện vào DB trong cùng giao dịch, sau đó mới đẩy ra queue, để không mất job |
| **Idempotency-Key** | Khóa giúp gửi lại cùng request mà không tạo trùng job hoặc trừ trùng credit |
| **Clean-room** | Phát triển lại từ hành vi quan sát được, không dùng mã, tài nguyên hay khóa của hệ thống gốc |
