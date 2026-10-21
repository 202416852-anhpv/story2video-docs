# 10 — Thuật ngữ

> Thuật ngữ gom theo nhóm. Trong mỗi nhóm, thuật ngữ nghiệp vụ đứng trước, thuật ngữ kỹ thuật đứng sau. Mã tham chiếu (BR, ADR, QĐ…) giải thích ở §1.

## 1. Quy ước tài liệu và quản lý dự án

| Thuật ngữ | Định nghĩa |
|---|---|
| **BRD (Business Requirements Document)** | Tài liệu yêu cầu nghiệp vụ: mục tiêu, phạm vi, quy trình, chỉ số thành công (01) |
| **SRS (Software Requirements Specification)** | Đặc tả yêu cầu phần mềm: yêu cầu chức năng (FR) và giao diện ngoài (IF) (02) |
| **Use case (UC)** | Kịch bản tương tác giữa tác nhân và hệ thống để đạt một mục tiêu; mã `UC-<phân hệ>.<số>[chữ]` (03) |
| **Mẫu Cockburn "fully-dressed"** | Mẫu đặc tả use case đầy đủ: tác nhân, tiền/hậu điều kiện, kích hoạt, luồng chính, nhánh thay thế, truy vết |
| **NFR (Non-Functional Requirement)** | Yêu cầu phi chức năng: hiệu năng, bảo mật, độ tin cậy, chi phí…; mã `NFR-<nhóm>-NN` (07) |
| **ADR (Architecture Decision Record)** | Bản ghi một quyết định kiến trúc: lựa chọn, phương án đã loại, lý do; mã `ADR-NN` (05 §9) |
| **C4 model** | Cách mô tả kiến trúc theo 4 mức: Context → Container → Component → Code (05) |
| **MoSCoW** | Mức ưu tiên yêu cầu: **M** (Must) bắt buộc trong MVP; **S** (Should) làm nếu kịp; **C** (Could) sau MVP |
| **Tiền tố mã** | `FR` yêu cầu chức năng, `BR` quy tắc nghiệp vụ, `IC` ràng buộc dữ liệu, `WR` quy tắc ví (08 §4), `SYM` ký hiệu trình bày (08 §6), `IF` giao diện ngoài, `R` rủi ro, `BO` mục tiêu nghiệp vụ, `QĐ` quyết định |
| **Sổ quyết định (QĐ-xx)** | `quyet-dinh.md`; mọi thay đổi phạm vi/kế hoạch ghi ở đây trước, các tài liệu khác dẫn mã QĐ |
| **Nguồn thông tin `[QS]` / `[SL]` / `[ĐX]`** | Quan sát được trên hệ thống tham chiếu / suy luận / đề xuất của BA |
| **Truy vết** | Mục trong mỗi UC liệt kê FR, BR, IC, NFR, API, sơ đồ liên quan |
| **RTM (Requirements Traceability Matrix)** | Ma trận truy vết yêu cầu: UC ↔ FR ↔ BO ↔ sơ đồ ↔ mã test (09 §4) |
| **MVP** | Phạm vi sản phẩm tới hết giai đoạn P3 (QĐ-03) |
| **Giai đoạn P0–P3 / Sau** | Bốn giai đoạn phát triển thuộc MVP (P0 nền tảng & PoC … P3 editor, xuất video, thanh toán); `Sau` = sau MVP (09 §1) |
| **Mốc M0, M1, M2…** | Điểm kiểm tra kế hoạch (vd. M0 kết thúc P0 ở T4, M2 đo vận tốc ở T8) |
| **T1…T24** | Tuần làm việc thứ n trong kế hoạch 24 tuần |
| **PoC (Proof of Concept)** | Bản thử nhỏ để kiểm chứng tính khả thi kỹ thuật trước khi làm thật |
| **Thứ tự cắt giảm (✂n)** | Thứ tự bỏ tính năng khi trễ tiến độ. Tầng 1: nạp tiền sandbox (thay bằng Admin cộng tiền) → Map → phụ đề preset + chuyển cảnh nâng cao → Relationships → Timeline truyện → từ điển phát âm (QĐ-05, QĐ-116); tầng 2 ✂7–✂10 và tầng 3 ở 09 §1.3 (QĐ-91) |
| **PO (Product Owner)** | Người chịu trách nhiệm sản phẩm và ngân sách; đầu mối làm việc với Vbee |
| **Story / Epic** | Story: một hạng mục backlog làm trong một sprint (mỗi UC MVP là một story). Epic: nhóm story lớn (UC sau MVP gom thành epic) (11) |
| **Story point / Planning poker** | Đơn vị ước lượng độ lớn tương đối của story / cách cả nhóm cùng bỏ phiếu để chốt điểm |
| **Sprint / Vận tốc (velocity)** | Chu kỳ làm việc ngắn cố định / số story point hoàn thành trung bình mỗi sprint, dùng dự báo ngày xong |
| **Spike** | Khoảng thời gian thử nghiệm kỹ thuật có giới hạn để gỡ rủi ro (vd. spike editor ở P2) |
| **Gherkin** | Cú pháp kịch bản kiểm thử `Given / When / Then`; tiêu chí chấp nhận của story trong 11 |
| **Coding Agent** | Trợ lý AI lập trình nhóm dùng để tăng năng suất (giả định A-04, QĐ-81) |
| **Clean-room** | Phát triển lại từ hành vi quan sát được, không dùng mã, tài nguyên hay khóa của hệ thống gốc |

## 2. Tài khoản, xác thực và bảo mật

| Thuật ngữ | Định nghĩa |
|---|---|
| **Guest / User / Admin** | Khách chưa đăng nhập / người dùng đã đăng nhập / quản trị viên vận hành hệ thống (danh sách mời, cấu hình, điều chỉnh số dư) |
| **SSO (Single Sign-On)** | Hệ thống đăng nhập một lần có sẵn, dùng chung cho nhiều ứng dụng; ứng dụng này chỉ tích hợp, không tự xây đăng nhập. Đồ án dùng Keycloak tự dựng, chuyển sang SSO Vbee trước khi bảo vệ |
| **Keycloak** | Máy chủ SSO mã nguồn mở, nhóm tự dựng để làm SSO cho môi trường dev và closed beta |
| **Realm** | Không gian cấu hình riêng trong Keycloak (người dùng, client, role); môi trường local dùng *dev realm* |
| **IdentityProviderPort** | Cổng xác thực trong module `auth`, có adapter OIDC và adapter OAuth 2.0 + userinfo để đổi SSO bằng cấu hình (ADR-20) |
| **OAuth 2.0** | Chuẩn ủy quyền: ứng dụng nhận token từ máy chủ ủy quyền thay vì giữ mật khẩu người dùng |
| **OIDC (OpenID Connect)** | Chuẩn xác thực trên nền OAuth 2.0; ứng dụng là *Relying Party*, SSO là *OpenID Provider* |
| **Authorization Code** | Luồng OIDC: SSO trả một mã ngắn hạn qua redirect, server ứng dụng đổi mã lấy token |
| **PKCE** | Cơ chế chống đánh cắp authorization code trong luồng Authorization Code |
| **`state` / `nonce`** | Giá trị ngẫu nhiên chống giả mạo callback (CSRF) / chống phát lại ID token |
| **ID token / Refresh token / Logout token** | Token chứng minh danh tính / token dùng lấy token mới (lưu mã hóa ở server) / token SSO gửi khi đăng xuất back-channel |
| **Claims** | Các trường thông tin trong token (sub, email, tên…) |
| **JWKS (JSON Web Key Set)** | Tập khóa công khai của SSO để kiểm chữ ký token |
| **BFF (Backend-for-Frontend)** | Mẫu thiết kế giữ token SSO ở server; trình duyệt chỉ giữ cookie phiên |
| **Cookie `HttpOnly; Secure; SameSite=Lax`** | Cookie phiên JavaScript không đọc được, chỉ gửi qua HTTPS, không gửi kèm request chéo trang (trừ điều hướng) |
| **CSRF / Double-submit token** | Tấn công giả mạo request từ trang khác / cách chống: gửi cùng một token ở cả cookie và header, server so khớp |
| **MFA (Multi-Factor Authentication)** | Xác thực nhiều yếu tố (mật khẩu + OTP…); thuộc SSO, ứng dụng không làm |
| **JIT provisioning** | Tự tạo hồ sơ cục bộ ở lần đăng nhập đầu tiên từ thông tin (claims) của SSO |
| **Back-channel logout** | SSO gọi trực tiếp tới server ứng dụng để báo đăng xuất |
| **Đồng ý xử lý dữ liệu (consent)** | Màn hình đồng ý ở lần đăng nhập đầu theo Nghị định 13/2023/NĐ-CP; lưu thời điểm và phiên bản (BR-31). Chưa đồng ý → `403 CONSENT_REQUIRED` |
| **Audit log** | Nhật ký hành động của Admin, không sửa xóa được (NFR-PRV-04) |
| **Presigned URL (link ký)** | URL tạm thời có chữ ký, cho tải/xem một file private trong thời hạn ngắn (vd. 15 phút) |
| **Kiểm tra MIME thật / quét malware** | Xác định loại file theo nội dung thay vì đuôi file / quét virus (ClamAV) với mọi file tải lên |

## 3. Dự án và bản thảo

| Thuật ngữ | Định nghĩa |
|---|---|
| **Project (Dự án)** | Không gian làm việc chuyển thể một truyện dài, gồm bản thảo, chương, thế giới truyện, tư liệu và video |
| **Owner / Editor** | Vai trò trong dự án: chủ sở hữu (toàn quyền) / cộng tác viên (sửa nội dung, sinh nội dung). MVP chỉ có Owner |
| **Source text (Văn bản gốc)** | Văn bản người dùng import, trước khi chia chương |
| **Workspace** | Trình soạn thảo liền mạch hiển thị mọi chương trên một trang cuộn |
| **Chapter (Chương)** | Phần văn bản liên tục; đơn vị để lập storyboard, sinh tư liệu và dựng video |
| **Restructure** | Thao tác thay đổi cấu trúc chương (chia, gộp, dời ranh giới, sắp xếp) thực hiện nguyên tử |
| **Archive** | Ảnh chụp chỉ đọc của toàn bộ bản thảo tại một thời điểm |
| **Khóa chương** | Chương bị khóa sửa khi có job đang xử lý (`chapters.locked_by_job_id`); Reconciler mở khóa nếu job đã kết thúc |
| **Soft delete / Xóa cứng** | Đánh dấu đã xóa, ẩn ngay nhưng còn dữ liệu (dự án giữ 30 ngày) / xóa hẳn dữ liệu và media |
| **Khóa lạc quan (optimistic lock)** | Mỗi bản ghi có `version`; client gửi `If-Match` kèm phiên bản đã đọc, server trả `409` nếu đã có người sửa trước, không ghi đè ngầm (ADR-06, BR-05) |
| **ETag / If-Match** | Header HTTP: phiên bản hiện tại server trả về / phiên bản client gửi lên khi sửa |
| **Code unit UTF-16** | Đơn vị đếm offset và độ dài văn bản (chỉ số chuỗi JavaScript) trên văn bản NFC (ADR-26) |
| **NFC (Unicode Normalization Form C)** | Dạng chuẩn hóa Unicode gộp chữ và dấu thành một ký tự (vd. "ế" là 1 ký tự thay vì "e" + dấu); mọi văn bản được chuẩn hóa NFC trước khi lưu |

## 4. Thế giới truyện

| Thuật ngữ | Định nghĩa |
|---|---|
| **Story Assets** | Tài sản thế giới truyện của dự án: nhân vật (Character), địa điểm (Location), đạo cụ (Prop), nhóm (Group) |
| **Reference image (Ảnh tham chiếu)** | Ảnh chuẩn của tài sản, đính kèm khi sinh mọi ảnh shot để giữ nhất quán |
| **Facts** | Đặc điểm bất biến của tài sản (vd. "tóc đen ngang vai", "sẹo ở má trái") luôn được chèn vào prompt |
| **Giai đoạn ngoại hình** *(sau MVP)* | Một bộ mô tả, facts, ảnh tham chiếu của tài sản áp từ một chương trở đi, cho nhân vật đổi ngoại hình theo mạch truyện (QĐ-142). MVP: tạo tài sản riêng cho mỗi giai đoạn |
| **Style (Phong cách)** | Phong cách hình ảnh chung của dự án, áp cho mọi ảnh sinh ra; Art Direction và Visual Rules bổ sung lên trên |
| **Art Direction** | Chỉ dẫn phong cách bổ sung lên style của dự án |
| **Visual Rules** | Luật hình ảnh có điều kiện, áp toàn dự án hoặc theo chương |
| **Chapter rules** | Chỉ dẫn cố định cho một chương, Director tuân theo khi viết brief |
| **Story timeline** | Dòng thời gian truyện (ngày, mùa) gán cho từng chương |
| **Relationship graph** | Đồ thị quan hệ giữa các nhân vật và diễn biến quan hệ |
| **Map** | Bản đồ địa điểm của thế giới truyện (✂2) |

## 5. Storyboard và sinh tư liệu

| Thuật ngữ | Định nghĩa |
|---|---|
| **Storyboard draft (Bản nháp storyboard)** | Một phương án chia chương thành các shot; mỗi chương có nhiều bản nháp, một bản hiện hành |
| **Shot** | Một ảnh minh họa gắn với một đoạn văn nguồn; trên timeline là 1 clip ảnh + 1 clip thuyết minh |
| **Cast / Items / Location (của shot)** | Nhân vật / đạo cụ / địa điểm (lấy từ Story Assets) xuất hiện trong shot; ảnh tham chiếu của chúng được đính kèm khi sinh ảnh |
| **Vạch ranh giới shot** | Vạch mảnh giữa các câu trong Workspace, cho biết chỗ chia shot; kéo để dời ranh giới |
| **Illustration brief** | Mô tả có cấu trúc để sinh ảnh: Subject / Environment / Composition / Camera / Lighting / Mood / Details |
| **Caption** | Mô tả ngắn 1–2 câu của shot, dùng trong storyboard (không dùng cho audio) |
| **Re-direct** | Viết lại brief mọi shot của chương |
| **Mật độ ảnh** | Số ảnh trên mỗi phút audio (mặc định 3 ảnh/phút, QĐ-112) |
| **Sinh tư liệu** | Bước 4 của luồng: storyboard tự động, rồi sinh ảnh + thuyết minh nguyên văn cho từng shot |
| **Media bin (Tư liệu dự án)** | Danh sách ảnh và audio thuyết minh theo chương/shot; đầu vào của trình chỉnh sửa |
| **Sẵn sàng dựng (`READY_TO_EDIT`)** | Trạng thái chương khi mọi shot có ảnh `DONE` và thuyết minh `DONE` |
| **Prompt** | Văn bản chỉ dẫn gửi cho mô hình AI; hệ thống ghép từ brief, style, facts, Art Direction, Visual Rules. `prompt_version` ghi phiên bản mẫu prompt đã dùng |
| **Seed** | Số khởi tạo ngẫu nhiên của mô hình sinh ảnh; cùng seed + cùng prompt cho kết quả gần giống nhau, ghi lại để tái hiện |
| **Moderation (kiểm duyệt nội dung)** | Bộ lọc an toàn chặn nội dung vi phạm chính sách. MVP dùng bộ lọc có sẵn của Gemini; bị chặn → job `FAILED` với `CONTENT_POLICY`, hoàn toàn bộ tiền (BR-18) |

## 6. Thuyết minh và âm thanh

| Thuật ngữ | Định nghĩa |
|---|---|
| **Đoạn nguồn (Source segment)** | Khoảng văn bản `[sourceStart, sourceEnd)` của chương gắn với một shot; là thứ được đọc trong video |
| **Phủ kín (Full coverage)** | Bất biến: các đoạn nguồn của storyboard hiện hành nối lại đúng bằng văn bản chương |
| **Thuyết minh nguyên văn (Verbatim narration)** | Audio đọc đúng từng chữ của đoạn nguồn; không chỉnh sửa, không tóm tắt |
| **Bản đọc (Spoken form)** | Biểu diễn dùng cho TTS (SSML, cách đọc số, từ điển phát âm, bỏ ký hiệu trình bày); không đổi nội dung chữ |
| **Ký hiệu trình bày** | Ký hiệu định dạng trong truyện (`*Bố*`, `[…]`, `# …`, `---`). Khi đọc thì bỏ ký hiệu, giữ chữ; phụ đề hiện nguyên (08 §6) |
| **Từ điển phát âm** | Cặp *từ viết → cách đọc* theo dự án; chỉ ảnh hưởng audio |
| **`ALIAS` / `PHONEME`** | Hai kiểu mục từ điển phát âm: thay bằng chữ đọc khác (MVP) / phiên âm theo ký hiệu ngữ âm qua SSML (sau MVP, Vbee AIVoice) |
| **Tốc độ đọc** | Một tốc độ duy nhất cho cả dự án (0,8–1,3×), áp ở bước TTS; không có tốc độ riêng từng clip (QĐ-140) |
| **Nghe thử phát âm** | Gọi TTS đồng bộ cho đoạn ≤ 200 ký tự, miễn phí, không tạo job (QĐ-136) |
| **TTS (Text-to-Speech)** | Chuyển văn bản thành giọng đọc. MVP dùng model tự host (TTS Server) |
| **SSML (Speech Synthesis Markup Language)** | Ngôn ngữ đánh dấu XML điều khiển TTS: ngắt nghỉ, cách đọc, phiên âm |
| **`NormalizationMap`** | Bảng ánh xạ vị trí giữa bản đọc và văn bản gốc, để đưa timestamp từ audio về đúng chữ trong chương (12 §2) |
| **STT / ASR (Speech-to-Text)** | Nhận dạng giọng nói thành chữ; dùng để căn timestamp và đo WER |
| **Aligner** | Thành phần làm forced alignment (WhisperX tự host, chạy ở Alignment Worker) |
| **WhisperX** | Công cụ mã nguồn mở dựa trên Whisper, nhận dạng giọng nói và trả timestamp từng từ |
| **Forced alignment** | Căn timestamp từng từ giữa audio và văn bản đã biết |
| **WER (Word Error Rate)** | Tỷ lệ lỗi từ giữa văn bản gốc và nội dung STT nghe được từ audio; dùng để chọn provider TTS ở P0 và kiểm chứng từng shot (sau MVP) |
| **WER nền / WER hiệu chỉnh** | Lỗi do chính ASR gây ra (đo trên audio người đọc chuẩn) / WER của TTS sau khi trừ WER nền (QĐ-111) |
| **Đánh dấu cần sinh lại** | Cờ người dùng đặt trên shot sau khi nghe thấy đọc sai (kiểm chứng thủ công, UC-05.18); không chặn xuất video |
| **NEEDS_REVIEW / ACCEPTED** | Trạng thái thuyết minh vượt ngưỡng WER / đã được người dùng chấp nhận thủ công (sau MVP; MVP dùng `DONE`) |

## 7. Trình chỉnh sửa và xuất video

| Thuật ngữ | Định nghĩa |
|---|---|
| **Trình chỉnh sửa video (Editor)** | Công cụ dựng video trên timeline nhiều track: ảnh, thuyết minh (khóa), phụ đề, nhạc nền, SFX, overlay |
| **Timeline / Track / Clip (item)** | Trục thời gian của video; mỗi track chứa các clip cùng loại |
| **SFX (Sound effect)** | Hiệu ứng âm thanh ngắn (tiếng mưa, bước chân, pháo hoa…) đặt tại thời điểm cụ thể |
| **Overlay** | Lớp hình chồng lên video (logo, chữ) |
| **Khóa thuyết minh** | Ràng buộc BR-24: clip thuyết minh không thể cắt, xóa, đảo thứ tự; chỉ dời thời điểm và chỉnh âm lượng; tốc độ đọc đặt cho cả dự án |
| **Trim** | Cắt bớt đầu hoặc cuối một clip |
| **Keyframe** | Điểm mốc trên clip đặt giá trị (âm lượng, vị trí…) tại một thời điểm; giá trị giữa hai mốc được nội suy |
| **Waveform** | Hình sóng biểu diễn biên độ âm thanh, hiển thị trên clip audio |
| **Loudness (LUFS)** | Độ to cảm nhận của âm thanh; chuẩn hóa về −14 LUFS cho mạng xã hội |
| **Ken Burns** | Hiệu ứng zoom/lia chậm trên ảnh tĩnh |
| **Chuyển cảnh (Transition)** | Hiệu ứng nối hai clip ảnh (fade, crossfade, wipe…) |
| **Ducking** | Tự giảm âm lượng nhạc nền khi có lời đọc |
| **Tỷ lệ khung hình (aspect ratio)** | Tỷ lệ rộng : cao của video (16:9, 9:16, 1:1) |
| **Framing `CROP` / `FIT` / `BLUR`** | Cách đặt ảnh khác tỷ lệ vào khung: cắt cho đầy / thu cho vừa (có viền) / vừa khung trên nền là chính ảnh làm mờ |
| **Vùng an toàn (safe area)** | Phần khung hình không bị giao diện mạng xã hội che, phụ đề phải nằm trong đó |
| **Preset phụ đề** | Mẫu kiểu phụ đề dựng sẵn (font, màu, nền, vị trí) (✂3) |
| **SRT / VTT** | Hai định dạng file phụ đề phổ biến (SubRip / WebVTT), tải kèm MP4 |
| **Preview** | Xem trước video trong trình duyệt, dùng chung component Remotion với render (ADR-13) |
| **`apply-ops`** | API nhận một lô thao tác sửa timeline; server kiểm IC-10 rồi lưu từng item (ADR-14) |
| **Debounce** | Chờ người dùng ngừng thao tác một khoảng (1–2 s) rồi mới gửi, để gom nhiều thay đổi thành một request |
| **Timeline snapshot** | JSON mô tả đầy đủ một phiên bản timeline, dùng để xuất video |
| **Render** | Bản MP4 xuất từ timeline (có phiên bản) |
| **Watermark** | Dấu nhận diện in trên video của tài khoản Free (720p) |
| **Remotion** | Thư viện React dựng video theo khung hình; dùng cho cả preview và render |
| **FFmpeg** | Công cụ xử lý audio/video dòng lệnh: trộn âm, ducking, chuẩn hóa loudness, mã hóa MP4 |

## 8. AI

| Thuật ngữ | Định nghĩa |
|---|---|
| **AI Director** | Trợ lý AI điều phối quy trình, nhận lệnh bằng ngôn ngữ tự nhiên và chạy chế độ tự động có điểm duyệt (sau MVP) |
| **Điểm duyệt (Checkpoint)** | Bước Director dừng chờ người dùng quyết định (chọn style, duyệt cast, xác nhận chi phí) |
| **DirectorPlan** | Kế hoạch nhiều bước Director lập cho một yêu cầu, có trạng thái (`RUNNING`…) (sau MVP) |
| **Tool call / Tool proposal** | LLM yêu cầu gọi một hàm của hệ thống (vd. `rewrite_shot`) / thẻ đề xuất người dùng phải xác nhận trước khi thao tác tốn phí chạy (ADR-19, sau MVP) |
| **LLM (Large Language Model)** | Mô hình ngôn ngữ lớn; dùng chia chương, phân tích tài sản, storyboard, viết brief |
| **Google Gemini (Flash / Pro)** | Nhà cung cấp LLM và ảnh của MVP: Flash là mô hình nhanh, rẻ cho tác vụ thường; Pro là mô hình mạnh cho storyboard, phân tích dài (QĐ-119, QĐ-120) |
| **Vbee AIVoice** | Dịch vụ TTS thương mại của Vbee, thay TTS Server sau MVP (QĐ-121) |
| **Provider** | Nhà cung cấp dịch vụ AI bên ngoài (hoặc model tự host) mà hệ thống gọi |
| **AI Gateway** | Lớp nội bộ chuẩn hóa việc gọi nhiều nhà cung cấp AI |
| **Adapter / Port** | Mẫu thiết kế tách interface (port) khỏi cài đặt theo provider (adapter) |
| **Mock adapter** | Adapter giả lập provider AI, trả fixture, dùng cho dev và CI để không tốn tiền |
| **Fixture** | Dữ liệu mẫu cố định (vd. kết quả provider đã ghi lại) dùng trong test |
| **`ProviderRouter`** | Thành phần chọn provider/mô hình theo loại tác vụ, đặt timeout, phân loại lỗi |
| **Fallback** | Chuyển sang mô hình dự phòng khi mô hình chính lỗi; chỉ áp cho LLM, giữa các mô hình Gemini không đắt hơn (QĐ-124, QĐ-125) |
| **Lỗi tạm thời / vĩnh viễn** | Lỗi có thể hết khi thử lại (timeout, 5xx, 429) / lỗi thử lại vô ích (sai đầu vào, bị moderation chặn) (13 §7.1) |
| **TTS Server** | Dịch vụ nội bộ chạy model TTS mã nguồn mở trên GPU của nhóm, dùng cho thuyết minh trong MVP (ADR-30); sau MVP thay bằng Vbee AIVoice |
| **GPU / VRAM** | Card đồ họa chạy model tự host / bộ nhớ của GPU, quyết định số job TTS chạy đồng thời |
| **Golden set** | Bộ chương mẫu nhóm tự chuẩn bị (tác phẩm hết thời hạn bảo hộ, Project Gutenberg, chương tự viết) để chọn provider và chạy eval |
| **Eval (`EVAL-*`)** | Bài đánh giá chất lượng AI có số đo và ngưỡng, chạy trên golden set ở P0 (vd. `EVAL-wer-golden`, `EVAL-consistency`, `EVAL-cost-per-minute`) |
| **Rubric** | Bảng tiêu chí chấm điểm thủ công (vd. độ nhất quán nhân vật, 2 người chấm) |
| **Ablation** | Thí nghiệm bỏ lần lượt từng thành phần (ảnh tham chiếu, facts…) để đo mức đóng góp của nó, đưa vào báo cáo |

## 9. Ví và thanh toán

| Thuật ngữ | Định nghĩa |
|---|---|
| **Ví (Wallet)** | Số dư USD của người dùng (lưu micro-USD); thay cho khái niệm credit của bản trước |
| **Micro-USD (µUSD)** | 1/1.000.000 USD; đơn vị lưu mọi số tiền để không sai số làm tròn |
| **Chi phí thực × 110%** | Cách tính giá mọi thao tác AI: chi phí provider ghi ở `ai_usage_records` cộng 10% phí |
| **Giá ước tính tối đa** | Số tiền hiện trước khi chạy và được giữ, tính từ độ dài đầu vào và giới hạn đầu ra; phần dư được hoàn sau khi chạy |
| **Hold / Capture / Release** | Giữ giá ước tính / trừ chi phí thực × 110% / hoàn phần dư của một job |
| **Ledger (Sổ cái)** | Bảng ghi thêm (append-only) mọi biến động số dư ví |
| **Append-only** | Chỉ được thêm dòng mới, không sửa hay xóa dòng cũ |
| **Tiền dùng thử** | $2 tặng một lần khi tạo hồ sơ (bút toán `TRIAL_GRANT`), không làm tài khoản thành "Đã nạp tiền" |
| **Free / Đã nạp tiền** | Hai trạng thái tài khoản trong MVP; "Đã nạp tiền" khi tổng nạp tiền thật > 0 (BR-27) |
| **Trần chi tiêu ngày** | Giới hạn tổng chi phí AI thật toàn hệ thống mỗi ngày ($10 trong closed beta, BR-29) |
| **Payment Gateway (Stripe)** | Cổng thanh toán; MVP dùng Stripe ở test mode bằng tài khoản của nhóm |
| **Sandbox / Test mode** | Chế độ thử của cổng thanh toán: giao dịch giả, không trừ tiền thật (QĐ-30) |
| **Checkout có host** | Trang thanh toán do cổng thanh toán cung cấp; ứng dụng không chạm vào thông tin thẻ |
| **Webhook** | Cổng thanh toán gọi ngược vào server để báo sự kiện (thanh toán thành công…); tiền chỉ vào ví khi webhook xác nhận, chữ ký được kiểm tra |
| **Danh sách mời** | Email được Admin cho phép tạo hồ sơ trong closed beta (BR-30) |
| **Closed beta** | Đợt UAT 10–20 người dùng được mời riêng, khoảng 3 tuần |

## 10. Hạ tầng, job và tích hợp

| Thuật ngữ | Định nghĩa |
|---|---|
| **Job** | Tác vụ bất đồng bộ (thường gọi AI) có vòng đời và chi phí. **Job gốc** giữ và quyết toán tiền; **job con** trong một Flow chỉ ghi chi phí (WR-05) |
| **Flow** | Nhóm job cha – con của BullMQ; job cha chỉ xong khi mọi job con xong |
| **Queue (hàng đợi)** | Danh sách job chờ xử lý, chia theo loại (`llm`, `image`, `tts`, `align`, `render`…) |
| **Worker** | Tiến trình lấy job từ queue và xử lý (gọi AI, căn timestamp, render…) |
| **BullMQ** | Thư viện hàng đợi job trên Redis cho Node.js; chỉ vận chuyển job, bảng `jobs` là nguồn sự thật |
| **Redis / Pub/Sub** | Kho dữ liệu trong bộ nhớ, dùng cho queue và bộ đếm / cơ chế phát–nhận tin nhắn của Redis, dùng đẩy sự kiện SSE giữa các instance (ADR-05) |
| **PostgreSQL** | Hệ quản trị cơ sở dữ liệu quan hệ chính của hệ thống |
| **Object storage (S3-compatible) / MinIO** | Kho lưu file (ảnh, audio, video) theo bucket, tương thích API Amazon S3 / phần mềm object storage mã nguồn mở dùng ở local và test |
| **Bucket private** | Bucket không truy cập công khai; chỉ xem qua presigned URL |
| **Scheduler / Repeatable job** | Tiến trình chạy tác vụ định kỳ / job BullMQ tự lặp theo lịch (QĐ-137) |
| **Heartbeat** | Tín hiệu định kỳ worker gửi để báo job còn đang chạy |
| **Reconciler** | Tác vụ định kỳ ở Scheduler: đẩy lại job `QUEUED` bị sót, cho job mất heartbeat về `FAILED` và quyết toán, mở khóa chương, đối soát sổ cái và trần chi tiêu ngày |
| **Outbox pattern** | Ghi sự kiện vào DB trong cùng giao dịch, sau đó mới đẩy ra queue, để không mất job. Sau MVP; MVP enqueue sau commit + reconciler (ADR-23) |
| **Giao dịch (transaction)** | Nhóm thao tác DB thực hiện trọn vẹn hoặc không gì cả |
| **`SELECT … FOR UPDATE`** | Khóa các dòng đang đọc tới hết giao dịch để giao dịch khác không sửa đồng thời |
| **Deadlock** | Hai giao dịch chờ khóa của nhau mãi mãi; tránh bằng thứ tự khóa cố định (ngân sách ngày → ví) |
| **Retry / Backoff / Jitter** | Thử lại khi lỗi tạm thời / tăng dần thời gian chờ giữa các lần (2 s / 8 s / 30 s) / cộng thêm độ trễ ngẫu nhiên để các job không thử lại cùng lúc |
| **Timeout** | Thời gian tối đa chờ một lời gọi; quá hạn tính là lỗi tạm thời (QĐ-126) |
| **Circuit breaker** | Cơ chế tạm ngừng gọi provider đang lỗi liên tục để tránh dồn tải (sau MVP, QĐ-133) |
| **Rate limit / `429`** | Giới hạn số request trong một khoảng thời gian / mã HTTP báo đã vượt giới hạn |
| **Concurrency** | Số job một queue xử lý đồng thời; MVP dùng để giới hạn tải toàn hệ thống |
| **Semaphore theo người dùng** | Bộ đếm Redis giới hạn số job ảnh / TTS chạy đồng thời của một người (ADR-28); sau MVP, MVP chỉ dùng `concurrency` của queue |
| **REST / OpenAPI** | Kiểu thiết kế API theo tài nguyên qua HTTP / chuẩn mô tả API bằng file YAML (`openapi.yaml`, bản 3.1) |
| **`202 Accepted`** | Mã HTTP trả khi API đã nhận tạo job, kết quả có sau qua SSE |
| **SSE (Server-Sent Events)** | Kênh một chiều server → trình duyệt để đẩy trạng thái job, tư liệu, timeline, render (06 §3) |
| **WebSocket / CRDT** | Kênh hai chiều thời gian thực / cấu trúc dữ liệu cho nhiều người sửa đồng thời tự hợp nhất (vd. Yjs); cả hai đã cân nhắc và không chọn (ADR-05, ADR-06) |
| **Idempotency-Key** | Khóa giúp gửi lại cùng request mà không tạo trùng job hoặc trừ tiền hai lần |
| **NestJS / Kysely** | Framework backend Node.js của API / thư viện viết truy vấn SQL có kiểu TypeScript và chạy migration |
| **Migration** | Script thay đổi cấu trúc DB có phiên bản, chạy theo thứ tự |
| **Log có cấu trúc / Correlation id** | Log dạng JSON có trường cố định / mã chung (`jobId`) gắn vào mọi log của một luồng để lần theo xuyên API → queue → worker → provider |
| **Sentry / OpenTelemetry** | Dịch vụ thu lỗi ứng dụng (MVP) / chuẩn tracing phân tán (sau MVP) |
| **Docker / Container** | Công cụ đóng gói ứng dụng cùng môi trường chạy; mỗi thành phần chạy trong một container |
| **Môi trường dev / staging** | Máy local của lập trình viên / môi trường giống production để demo và đo hiệu năng |

## 11. Kiểm thử và chất lượng

| Thuật ngữ | Định nghĩa |
|---|---|
| **CI/CD** | Tích hợp liên tục (tự chạy build và test mỗi lần đẩy code) / triển khai liên tục |
| **UT / IT / E2E** | Unit test (một hàm, lớp) / integration test (nhiều thành phần với DB, Redis thật) / end-to-end test (toàn luồng qua giao diện) |
| **PBT (Property-based test)** | Kiểm thử bằng cách sinh ngẫu nhiên rất nhiều đầu vào và kiểm một tính chất luôn đúng (vd. phủ kín); dùng thư viện fast-check |
| **Vitest / Testcontainers** | Framework chạy test JavaScript/TypeScript / thư viện bật PostgreSQL, Redis, MinIO thật trong container cho integration test |
| **Contract test (`IT-openapi-contract`)** | Test so spec sinh từ code với file OpenAPI viết tay; khác nhau thì CI thất bại |
| **UAT (User Acceptance Testing)** | Kiểm thử chấp nhận bởi người dùng thật; ở đồ án là closed beta |
| **p95 / p99** | Phân vị 95 / 99: 95% / 99% request nhanh hơn giá trị này |
| **RPS** | Số request mỗi giây |
| **k6 / APM** | Công cụ kiểm thử tải / công cụ giám sát hiệu năng ứng dụng |
| **Benchmark** | Đo hiệu năng hoặc chất lượng theo bộ dữ liệu và cách đo cố định để so sánh |
