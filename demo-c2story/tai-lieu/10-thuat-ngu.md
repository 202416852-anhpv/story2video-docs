# 10 — Thuật ngữ

| Thuật ngữ | Định nghĩa |
|---|---|
| **Project (Dự án)** | Không gian làm việc chuyển thể một truyện dài, gồm bản thảo, chương, thế giới truyện, tư liệu và video |
| **SSO (Single Sign-On)** | Hệ thống đăng nhập một lần có sẵn, dùng chung cho nhiều ứng dụng; ứng dụng này chỉ tích hợp, không tự xây đăng nhập. Đồ án dùng Keycloak tự dựng, chuyển sang SSO Vbee trước khi bảo vệ |
| **Keycloak** | Máy chủ SSO mã nguồn mở, nhóm tự dựng để làm SSO cho môi trường dev và closed beta |
| **IdentityProviderPort** | Cổng xác thực trong module `auth`, có adapter OIDC và adapter OAuth 2.0 + userinfo để đổi SSO bằng cấu hình (ADR-20) |
| **OIDC (OpenID Connect)** | Chuẩn xác thực trên nền OAuth 2.0; ứng dụng là *Relying Party*, SSO là *OpenID Provider* |
| **PKCE** | Cơ chế chống đánh cắp authorization code trong luồng Authorization Code |
| **BFF (Backend-for-Frontend)** | Mẫu thiết kế giữ token SSO ở server; trình duyệt chỉ giữ cookie phiên |
| **JIT provisioning** | Tự tạo hồ sơ cục bộ ở lần đăng nhập đầu tiên từ thông tin (claims) của SSO |
| **Back-channel logout** | SSO gọi trực tiếp tới server ứng dụng để báo đăng xuất |
| **Owner / Editor** | Vai trò trong dự án: chủ sở hữu (toàn quyền) / cộng tác viên (sửa nội dung, sinh nội dung). MVP chỉ có Owner |
| **Source text (Văn bản gốc)** | Văn bản người dùng import, trước khi chia chương |
| **Workspace** | Trình soạn thảo liền mạch hiển thị mọi chương trên một trang cuộn |
| **Chapter (Chương)** | Phần văn bản liên tục; đơn vị để lập storyboard, sinh tư liệu và dựng video |
| **Restructure** | Thao tác thay đổi cấu trúc chương (chia, gộp, dời ranh giới, sắp xếp) thực hiện nguyên tử |
| **Archive** | Ảnh chụp chỉ đọc của toàn bộ bản thảo tại một thời điểm |
| **Story Assets** | Tài sản thế giới truyện của dự án: nhân vật (Character), địa điểm (Location), đạo cụ (Prop), nhóm (Group) |
| **Reference image (Ảnh tham chiếu)** | Ảnh chuẩn của tài sản, đính kèm khi sinh mọi ảnh shot để giữ nhất quán |
| **Facts** | Đặc điểm bất biến của tài sản (vd. "tóc đen ngang vai", "sẹo ở má trái") luôn được chèn vào prompt |
| **Giai đoạn ngoại hình** *(sau MVP)* | Một bộ mô tả, facts, ảnh tham chiếu của tài sản áp từ một chương trở đi, cho nhân vật đổi ngoại hình theo mạch truyện (QĐ-142). MVP: tạo tài sản riêng cho mỗi giai đoạn |
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
| **Sẵn sàng dựng** | Trạng thái chương khi mọi shot có ảnh `DONE` và thuyết minh `DONE` |
| **Đoạn nguồn (Source segment)** | Khoảng văn bản `[sourceStart, sourceEnd)` của chương gắn với một shot; là thứ được đọc trong video |
| **Phủ kín (Full coverage)** | Bất biến: các đoạn nguồn của storyboard hiện hành nối lại đúng bằng văn bản chương |
| **Thuyết minh nguyên văn (Verbatim narration)** | Audio đọc đúng từng chữ của đoạn nguồn; không chỉnh sửa, không tóm tắt |
| **Bản đọc (Spoken form)** | Biểu diễn dùng cho TTS (SSML, cách đọc số, từ điển phát âm, bỏ ký hiệu trình bày); không đổi nội dung chữ |
| **Ký hiệu trình bày** | Ký hiệu định dạng trong truyện (`*Bố*`, `[…]`, `# …`, `---`). Khi đọc thì bỏ ký hiệu, giữ chữ; phụ đề hiện nguyên (08 §6) |
| **Từ điển phát âm** | Cặp *từ viết → cách đọc* theo dự án; chỉ ảnh hưởng audio |
| **Forced alignment** | Căn timestamp từng từ giữa audio và văn bản đã biết |
| **WER (Word Error Rate)** | Tỷ lệ lỗi từ giữa văn bản gốc và nội dung STT nghe được từ audio; dùng để chọn provider TTS ở P0 và kiểm chứng từng shot (sau MVP) |
| **Đánh dấu cần sinh lại** | Cờ người dùng đặt trên shot sau khi nghe thấy đọc sai (kiểm chứng thủ công, UC-05.18); không chặn xuất video |
| **NEEDS_REVIEW / ACCEPTED** | Trạng thái thuyết minh vượt ngưỡng WER / đã được người dùng chấp nhận thủ công (sau MVP; MVP dùng `DONE`) |
| **Trình chỉnh sửa video (Editor)** | Công cụ dựng video trên timeline nhiều track: ảnh, thuyết minh (khóa), phụ đề, nhạc nền, SFX, overlay |
| **Timeline / Track / Clip (item)** | Trục thời gian của video; mỗi track chứa các clip cùng loại |
| **SFX (Sound effect)** | Hiệu ứng âm thanh ngắn (tiếng mưa, bước chân, pháo hoa…) đặt tại thời điểm cụ thể |
| **Khóa thuyết minh** | Ràng buộc BR-24: clip thuyết minh không thể cắt, xóa, đảo thứ tự; chỉ dời thời điểm và chỉnh âm lượng; tốc độ đọc đặt cho cả dự án |
| **Loudness (LUFS)** | Độ to cảm nhận của âm thanh; chuẩn hóa về −14 LUFS cho mạng xã hội |
| **Ken Burns** | Hiệu ứng zoom/lia chậm trên ảnh tĩnh |
| **Chuyển cảnh (Transition)** | Hiệu ứng nối hai clip ảnh (fade, crossfade, wipe…) |
| **Ducking** | Tự giảm âm lượng nhạc nền khi có lời đọc |
| **Timeline snapshot** | JSON mô tả đầy đủ một phiên bản timeline, dùng để xuất video |
| **Render** | Bản MP4 xuất từ timeline (có phiên bản) |
| **AI Director** | Trợ lý AI điều phối quy trình, nhận lệnh bằng ngôn ngữ tự nhiên và chạy chế độ tự động có điểm duyệt (sau MVP) |
| **Điểm duyệt (Checkpoint)** | Bước Director dừng chờ người dùng quyết định (chọn style, duyệt cast, xác nhận chi phí) |
| **Ví (Wallet)** | Số dư USD của người dùng (lưu micro-USD); thay cho khái niệm credit của bản trước |
| **Micro-USD (µUSD)** | 1/1.000.000 USD; đơn vị lưu mọi số tiền để không sai số làm tròn |
| **Chi phí thực × 110%** | Cách tính giá mọi thao tác AI: chi phí provider ghi ở `ai_usage_records` cộng 10% phí |
| **Giá ước tính tối đa** | Số tiền hiện trước khi chạy và được giữ, tính từ độ dài đầu vào và giới hạn đầu ra; phần dư được hoàn sau khi chạy |
| **Tiền dùng thử** | $2 tặng một lần khi tạo hồ sơ (bút toán `TRIAL_GRANT`), không làm tài khoản thành "Đã nạp tiền" |
| **Free / Đã nạp tiền** | Hai trạng thái tài khoản trong MVP; "Đã nạp tiền" khi tổng nạp tiền thật > 0 (BR-27) |
| **Trần chi tiêu ngày** | Giới hạn tổng chi phí AI thật toàn hệ thống mỗi ngày ($10 trong closed beta, BR-29) |
| **Closed beta** | Đợt UAT 10–20 người dùng được mời riêng, khoảng 3 tuần |
| **Danh sách mời** | Email được Admin cho phép tạo hồ sơ trong closed beta (BR-30) |
| **MVP** | Phạm vi sản phẩm tới hết giai đoạn P3 (QĐ-03) |
| **Thứ tự cắt giảm (✂n)** | Thứ tự bỏ tính năng khi trễ tiến độ. Tầng 1: nạp tiền sandbox (thay bằng Admin cộng tiền) → Map → phụ đề preset + chuyển cảnh nâng cao → Relationships → Timeline truyện → từ điển phát âm (QĐ-05, QĐ-116); tầng 2 ✂7–✂10 và tầng 3 ở 09 §1.3 (QĐ-91) |
| **Golden set** | Bộ chương mẫu nhóm tự chuẩn bị (tác phẩm hết thời hạn bảo hộ, Project Gutenberg, chương tự viết) để chọn provider và chạy eval |
| **Mock adapter** | Adapter giả lập provider AI, trả fixture, dùng cho dev và CI để không tốn tiền |
| **Hold / Capture / Release** | Giữ giá ước tính / trừ chi phí thực × 110% / hoàn phần dư của một job |
| **Ledger (Sổ cái)** | Bảng ghi thêm (append-only) mọi biến động số dư ví |
| **Job** | Tác vụ bất đồng bộ (thường gọi AI) có vòng đời và chi phí. **Job gốc** giữ và quyết toán tiền; **job con** trong một Flow chỉ ghi chi phí (WR-05) |
| **AI Gateway** | Lớp nội bộ chuẩn hóa việc gọi nhiều nhà cung cấp AI |
| **Adapter / Port** | Mẫu thiết kế tách interface (port) khỏi cài đặt theo provider (adapter) |
| **TTS Server** | Dịch vụ nội bộ chạy model TTS mã nguồn mở trên GPU của nhóm, dùng cho thuyết minh trong MVP (ADR-30); sau MVP thay bằng Vbee AIVoice |
| **Outbox pattern** | Ghi sự kiện vào DB trong cùng giao dịch, sau đó mới đẩy ra queue, để không mất job. Sau MVP; MVP enqueue sau commit + reconciler (ADR-23) |
| **Reconciler** | Tác vụ định kỳ ở Scheduler: đẩy lại job `QUEUED` bị sót, cho job mất heartbeat về `FAILED` và quyết toán, mở khóa chương, đối soát sổ cái và trần chi tiêu ngày |
| **Semaphore theo người dùng** | Bộ đếm Redis giới hạn số job ảnh / TTS chạy đồng thời của một người (ADR-28); sau MVP, MVP chỉ dùng `concurrency` của queue |
| **Code unit UTF-16** | Đơn vị đếm offset và độ dài văn bản (chỉ số chuỗi JavaScript) trên văn bản NFC (ADR-26) |
| **SSE (Server-Sent Events)** | Kênh một chiều server → trình duyệt để đẩy trạng thái job, tư liệu, timeline, render (06 §3) |
| **Idempotency-Key** | Khóa giúp gửi lại cùng request mà không tạo trùng job hoặc trừ tiền hai lần |
| **Clean-room** | Phát triển lại từ hành vi quan sát được, không dùng mã, tài nguyên hay khóa của hệ thống gốc |
