# 02 — Đặc tả yêu cầu phần mềm (SRS)

> Theo cấu trúc ISO/IEC/IEEE 29148:2018. Yêu cầu phi chức năng ở [07](07-yeu-cau-phi-chuc-nang.md).
> Ưu tiên MoSCoW: **M** (Must), **S** (Should), **C** (Could). Nguồn: **QS** (quan sát) / **SL** (suy luận) / **ĐX** (đề xuất).

## 1. Giới thiệu

### 1.1 Tác nhân

| Tác nhân | Mô tả |
|---|---|
| Guest | Chưa đăng nhập; chỉ thấy trang giới thiệu, bảng giá và nút "Đăng nhập" (chuyển sang SSO) |
| User | Đã đăng nhập |
| Owner | User tạo dự án (kế thừa Editor) |
| Editor | User được mời vào dự án |
| Admin | Quản trị hệ thống |
| AI Gateway | Tác nhân hệ thống phụ: LLM, Image, TTS, STT/Aligner, Music |
| Payment Gateway | Cổng thanh toán (tác nhân phụ) |
| SSO (Identity Provider) | **SSO có sẵn** (vd. SSO Vbee), giao thức OIDC; quản lý toàn bộ đăng ký, đăng nhập, đăng xuất, mật khẩu (tác nhân phụ) |

Sơ đồ: `../so-do/01-use-case/uc-tong-quan.puml`, `../so-do/01-use-case/uc-studio-chi-tiet.puml`. Sơ đồ phân rã của từng phân hệ M01–M10 nằm ở `../so-do/01-use-case/phan-ra/uc-mXX-*.puml`; M05 tách làm hai (5a Storyboard, 5b Sinh ảnh & thuyết minh).

### 1.2 Quy ước mã
`FR-<phân hệ>-<số>`. Truy vết tới use case và test: [09](09-ke-hoach-phat-trien.md) §4.

---

## 2. Yêu cầu chức năng

### 2.1 M01 — Tích hợp SSO & hồ sơ (AUTH) · phụ trợ

> **Không phát triển lại** đăng ký, đăng nhập, đăng xuất, quên/đổi mật khẩu, xác minh email, MFA. Toàn bộ do **SSO có sẵn** đảm nhiệm; ứng dụng là một *Relying Party (RP)* OIDC. Sơ đồ: `../so-do/04-tuan-tu/seq-dang-nhap-sso.puml`.

| Mã | Yêu cầu | Ưu tiên | Nguồn |
|---|---|---|---|
| FR-AUTH-01 | Nút "Đăng nhập" chuyển người dùng sang trang đăng nhập của SSO (OIDC Authorization Code + PKCE, kèm `state` và `nonce`). Người chưa có tài khoản **đăng ký ngay trên SSO**; ứng dụng không có form đăng ký. | M | ĐX |
| FR-AUTH-02 | Callback: đổi `code` lấy token ở backend; xác thực ID token (chữ ký theo JWKS, `iss`, `aud`, `exp`, `nonce`); tạo phiên ứng dụng bằng cookie httpOnly. Token SSO chỉ lưu phía server (mẫu BFF), không bao giờ gửi cho trình duyệt. | M | ĐX |
| FR-AUTH-03 | Sau khi đăng nhập, chuyển về URL đã yêu cầu trước đó (vd. link mời dự án). URL đích chỉ được là đường dẫn nội bộ, để chống open redirect. | M | QS |
| FR-AUTH-04 | **Cấp hồ sơ tự động (JIT provisioning):** lần đăng nhập đầu, tạo `users` cục bộ gắn với `sub` của SSO; mỗi lần đăng nhập đồng bộ email, tên, avatar từ claims. Hồ sơ cục bộ chỉ chứa dữ liệu riêng của ứng dụng (locale giao diện, ví credit, dự án). | M | ĐX |
| FR-AUTH-05 | **Đăng xuất:** xóa phiên ứng dụng, sau đó gọi RP-initiated logout tới `end_session_endpoint` của SSO (kèm `id_token_hint`, `post_logout_redirect_uri`). Nếu SSO hỗ trợ back-channel logout, nhận `logout_token` để hủy mọi phiên của người dùng đó. | M | ĐX |
| FR-AUTH-06 | Gia hạn phiên: dùng refresh token của SSO ở backend; nếu SSO thu hồi hoặc tài khoản bị khóa thì phiên ứng dụng hết hiệu lực ở lần gia hạn kế tiếp (≤ 15 phút). | M | ĐX |
| FR-AUTH-07 | **Vai trò Admin** của ứng dụng lấy từ claim/nhóm của SSO (vd. `roles` chứa `story-studio:admin`); nếu SSO không có claim thì quản lý bằng danh sách cục bộ. | M | ĐX |
| FR-AUTH-08 | Đổi ngôn ngữ giao diện (vi, en), lưu ở hồ sơ cục bộ; mặc định lấy claim `locale` nếu có. | S | QS |
| FR-AUTH-09 | Dashboard hiển thị gói hiện tại, số dư credit, số dự án, lối tắt Manage Billing; link "Quản lý tài khoản" mở trang hồ sơ của SSO. | M | QS |
| FR-AUTH-10 | Khi SSO báo tài khoản bị xóa hoặc vô hiệu (webhook/SCIM, hoặc phát hiện ở lần đăng nhập), ứng dụng khóa hồ sơ cục bộ; dự án do người đó sở hữu bị xóa sau 30 ngày; tư cách Editor ở dự án khác bị gỡ ngay. Người dùng cũng có thể tự yêu cầu xóa dữ liệu của ứng dụng. | M | ĐX |

### 2.2 M02 — Quản lý dự án & cộng tác (PRJ) · lõi

| Mã | Yêu cầu | Ưu tiên | Nguồn |
|---|---|---|---|
| FR-PRJ-01 | Trang Projects liệt kê dự án mà User là Owner hoặc Editor, gồm tiêu đề, số chương, style, trạng thái (In Progress / Done), ngày cập nhật; Owner có nút xóa. | M | QS |
| FR-PRJ-02 | "Import your story": dán văn bản hoặc tải file .txt/.md/.docx (≤ 2 MB, ≤ 500.000 ký tự). | M | QS |
| FR-PRJ-03 | Import **luôn giữ nguyên văn**. Hệ thống chỉ chuẩn hóa kỹ thuật không làm đổi chữ: chuẩn Unicode NFC, thống nhất ký tự xuống dòng, bỏ ký tự điều khiển vô hình. Không có tùy chọn AI viết lại (BR-19, BR-21). *Khác với hệ thống tham chiếu.* | M | ĐX |
| FR-PRJ-04 | Tạo dự án trống rồi viết trực tiếp trong Workspace. | S | QS |
| FR-PRJ-05 | Bố cục Studio: thanh trái gồm các nhóm Write (Workspace, Split into chapters), Your world (Story Assets, Timeline, Relationships, Visual Rules), Make·Media (Sinh tư liệu, Storyboard, Ảnh, Thuyết minh theo chương), Make·Video (Trình chỉnh sửa, Renders), danh sách chương, Find & replace, Archives, Project Assets, Settings. Vùng giữa là các tab có thể đóng. Panel phải gồm Notes, Director, Assets, Book, Scene. Màn hình hiện tại thể hiện trên URL (`?v=<view>[:<id>]`) để chia sẻ link. | M | QS |
| FR-PRJ-06 | Map overview: sơ đồ chặng (1 Nhập truyện → 2 Chia chương → 3 Thế giới truyện → 4 Sinh tư liệu → 5 Chỉnh sửa video → 6 Xuất & tải), làm nổi bật chặng hiện tại; bấm một chặng để chuyển tới. | S | QS (điều chỉnh) |
| FR-PRJ-07 | Settings (chỉ Owner): style, mô hình ảnh, ngôn ngữ, thời lượng mục tiêu mỗi ảnh (mặc định 15 s đọc), hiển thị, **tỷ lệ khung hình video mục tiêu (16:9 / 9:16 / 1:1)**. Ảnh shot được sinh theo tỷ lệ này. Lưu ngay khi chọn. | M | QS + ĐX |
| FR-PRJ-08 | Share (chỉ Owner): tạo, sao chép và thu hồi link mời; ai mở link sẽ tham gia làm Editor. | M | QS |
| FR-PRJ-09 | Collaborators: Owner xem danh sách thành viên, xóa thành viên. | M | QS |
| FR-PRJ-10 | Ma trận quyền theo [08](08-quy-tac-nghiep-vu.md) §2. | M | QS |
| FR-PRJ-11 | Mỗi chương hiển thị người sửa cuối. Khi lưu bị xung đột phiên bản, hiện hộp thoại: "Lưu bản của tôi thành nháp" (đưa vào Archives) hoặc "Tải bản của họ". | M | QS |
| FR-PRJ-12 | Thay đổi của người khác được đẩy về theo thời gian thực (danh sách chương, trạng thái job). | S | ĐX |
| FR-PRJ-13 | Nhân bản dự án (Duplicate) cùng toàn bộ chương và tài sản, không kèm video. | C | ĐX |

### 2.3 M03 — Bản thảo & chương (MAN) · lõi

| Mã | Yêu cầu | Ưu tiên | Nguồn |
|---|---|---|---|
| FR-MAN-01 | Màn hình Write (source) hiển thị văn bản gốc, số ký tự, số chương; có Copy text, Re-import, Suggest chapter splits; mỗi đoạn văn có nút "Split here". | M | QS |
| FR-MAN-02 | Workspace: trình soạn thảo liền mạch cho mọi chương (cuộn một trang); mỗi chương có tiêu đề sửa được, số ký tự, nút Storyboard, Sinh tư liệu, Mở trình chỉnh sửa, Chapter actions. | M | QS |
| FR-MAN-03 | Chia chương tại vị trí con trỏ hoặc giữa hai đoạn. | M | QS |
| FR-MAN-04 | AI gợi ý điểm chia chương (vị trí đoạn + tiêu đề); áp dụng toàn bộ hoặc từng điểm; nếu đã khớp thì báo "Your current chapters already match". | M | QS |
| FR-MAN-05 | Thêm chương (cuối hoặc chèn giữa), xóa, đổi tên, sắp xếp lại (kéo thả hoặc chọn vị trí), gộp vào chương trước, dời ranh giới từng đoạn văn. | M | QS |
| FR-MAN-06 | Mọi thao tác tái cấu trúc chương chạy trong **một giao dịch**; thất bại thì rollback toàn bộ. | M | ĐX |
| FR-MAN-07 | Find & replace trên tiêu đề và nội dung mọi chương có thể sửa, khớp chính xác, phân biệt hoa thường; xem trước số kết quả. | S | QS |
| FR-MAN-08 | Archives: đặt tên và lưu ảnh chụp chỉ đọc của toàn bộ bản thảo; xem, sao chép và xóa. | M | QS |
| FR-MAN-09 | Notes: ghi chú cấp dự án; có thể gắn vào chương hoặc shot; Director được phép thêm "Director note". | S | QS |
| FR-MAN-10 | Lịch sử phiên bản chương: xem, khôi phục. | S | QS |
| FR-MAN-11 | Chương có thể bị khóa (locked) trong khi job đang chạy trên nó; giao diện báo "This chapter is locked". | S | QS |

### 2.4 M04 — Thế giới truyện (WLD) · lõi

| Mã | Yêu cầu | Ưu tiên | Nguồn |
|---|---|---|---|
| FR-WLD-01 | Analyze assets: AI đọc mọi chương, đề xuất nhân vật, địa điểm, đạo cụ **lặp lại**; danh sách "Recommended assets" cho người dùng chọn thêm hoặc bỏ. | M | QS |
| FR-WLD-02 | Story Assets gồm 3 nhóm Characters / Locations / Props, hỗ trợ Group (nhóm nhân vật). Thuộc tính: tên, bí danh, mô tả ngoại hình, facts bất biến, ảnh tham chiếu. | M | QS |
| FR-WLD-03 | Tạo tài sản mới (New character / location / prop); sinh hoặc sinh lại ảnh tham chiếu; địa điểm có reference sheet nhiều góc nhìn. | M | QS |
| FR-WLD-04 | Dùng ảnh tải lên làm tài sản, không vẽ lại ("Use this exact image"). | S | QS |
| FR-WLD-05 | Thêm tài sản có sẵn từ thư viện cá nhân (M08); gỡ khỏi Story Assets / khỏi dự án; xóa vĩnh viễn khỏi thư viện (xác nhận 2 bước). | M | QS |
| FR-WLD-06 | Set style cho dự án; "Regenerate all (n)" sinh lại mọi ảnh tham chiếu theo style hiện tại (hiện tổng giá trước khi chạy). | M | QS |
| FR-WLD-07 | Art direction: văn bản phong cách bổ sung lên style dự án, áp cho mọi tài sản và mọi ảnh. | M | QS |
| FR-WLD-08 | Story timeline: AI gán cho mỗi chương nhãn ngày, mùa và tóm tắt; hiển thị theo tỷ lệ thời gian; Re-analyse. Director dùng dữ liệu này để dựng bối cảnh cảnh. | S | QS |
| FR-WLD-09 | Relationship graph: AI trích cặp nhân vật, nhãn quan hệ và diễn biến; hiển thị dạng đồ thị; Re-analyse. | S | QS |
| FR-WLD-10 | Visual Rules: tạo, sửa, xóa luật (tên, nội dung, phạm vi toàn dự án hoặc chương); áp theo BR-08. | S | QS |
| FR-WLD-11 | Project Assets (hộp thoại quản trị đầy đủ): thêm, gỡ, bí danh, nhóm; xuất ZIP ảnh tài sản. | S | QS |

### 2.5 M05 — Sinh tư liệu: ảnh + thuyết minh nguyên văn (MED) · lõi

> Bước 4 của luồng chính. Đầu ra **chỉ gồm ảnh minh họa và audio thuyết minh nguyên văn** của từng shot. Nhạc nền và SFX **không** sinh ở bước này; chúng được thêm trong trình chỉnh sửa video (M06). Storyboard chạy **tự động** bên trong bước này; màn hình Storyboard chỉ dùng để tinh chỉnh khi cần (quyết định A1).

#### 2.5.1 Điều phối sinh tư liệu

| Mã | Yêu cầu | Ưu tiên | Nguồn |
|---|---|---|---|
| FR-MED-01 | Nút **"Sinh tư liệu"** cho một chương, nhiều chương hoặc cả dự án. Hệ thống hiện **một** báo giá tổng (ảnh + TTS), người dùng xác nhận một lần, rồi hệ thống chạy tuần tự: tạo storyboard tự động (nếu chương chưa có bản hiện hành), sau đó với mỗi shot sinh **song song** ảnh minh họa và thuyết minh nguyên văn. | M | ĐX |
| FR-MED-02 | Bảng tiến độ theo chương và shot: trạng thái ảnh (pending / generating / done / failed) và thuyết minh (pending / generating / verified / needs_review / failed); cập nhật realtime. | M | ĐX |
| FR-MED-03 | **Tư liệu dự án (Media bin):** danh sách theo chương → shot, hiển thị ảnh hiện hành, audio thuyết minh (nghe thử), đoạn văn nguồn, thời lượng, WER. Đây là **đầu vào duy nhất** của trình chỉnh sửa video. | M | ĐX |
| FR-MED-04 | Sinh lại có chọn lọc: chỉ phần thiếu hoặc lỗi; chỉ ảnh hoặc chỉ thuyết minh của một shot; cả chương. | M | ĐX |
| FR-MED-05 | Khi mọi shot của chương có ảnh `DONE` và thuyết minh `VERIFIED`/`ACCEPTED`, chương ở trạng thái **"Sẵn sàng dựng"** và hệ thống tự tạo **bản nháp timeline** cho chương (FR-EDT-01). | M | ĐX |

#### 2.5.2 Storyboard (tự động, tinh chỉnh tùy chọn)

| Mã | Yêu cầu | Ưu tiên | Nguồn |
|---|---|---|---|
| FR-BOK-01 | Tạo bản nháp storyboard cho chương: AI chia **toàn bộ** văn bản chương thành N shot liên tục. Mỗi shot gắn với một **đoạn nguồn** `[sourceStart, sourceEnd)` (offset ký tự, ranh giới tại cuối câu). N mặc định suy từ độ dài chương và mục tiêu "thời lượng mục tiêu mỗi ảnh" (mặc định 8–20 s đọc). | M | QS + ĐX |
| FR-BOK-01a | **Validator phủ kín (BR-20):** khi lưu bản nháp, server kiểm tra các đoạn nguồn sắp theo thứ tự, liên tục, không chồng lấn, phủ `[0, len(chapter))`. Nếu LLM trả sai, server **sửa ranh giới tất định**: snap về ranh giới câu gần nhất; khoảng hở gộp vào shot trước; chồng lấn cắt theo shot sau. Không bao giờ đổi chữ. Sơ đồ `act-phu-kin-van-ban.puml`. | M | ĐX |
| FR-BOK-01b | Giao diện hiển thị đoạn nguồn của mỗi shot (nguyên văn, chỉ đọc). Người dùng **dời ranh giới** giữa hai shot liền kề theo câu (kéo hoặc nút ◀ ▶); thao tác này không làm đổi văn bản. | M | ĐX |
| FR-BOK-02 | Quản lý bản nháp: chọn, đổi tên, nhân bản, xóa, so sánh hai bản; "Set as current" (BR-07). | M | QS |
| FR-BOK-03 | Re-split shots: nhiều hơn (mỗi nhịp truyện một shot) hoặc ít hơn; luôn tạo bản nháp mới. | S | QS |
| FR-BOK-04 | Chapter rules: chỉ dẫn cố định cho chương mà Director tuân theo. | S | QS |
| FR-BOK-05 | Shot gồm: số thứ tự, tiêu đề, focus, cast, item, location, thời điểm, ngày, illustration brief (Subject / Environment / Composition / Camera / Lighting / Mood / Details, một khung hình tĩnh), caption 1–2 câu, đoạn văn nguồn. | M | QS |
| FR-BOK-06 | Thao tác shot: sửa trường minh họa (title, focus, brief, caption, cast/item/location, thời điểm, ngày); gộp với shot trên/dưới (đoạn nguồn được nối lại); tách đôi tại một ranh giới câu; "Rewrite this shot" (AI viết lại **brief minh họa**, không động vào đoạn nguồn). **Xóa shot** không làm mất văn bản: đoạn nguồn của nó gộp vào shot liền trước, hoặc shot liền sau nếu là shot đầu tiên. | M | QS (điều chỉnh) |
| FR-BOK-07 | Re-direct: AI viết lại brief minh họa cho mọi shot (vd. sau khi đổi Chapter rules); đoạn nguồn giữ nguyên. | S | QS |
| FR-BOK-08 | Tên cast/item/location chưa khớp tài sản bị cảnh báo; "Scan the chapter text and auto-match" để tự khớp. | S | QS |

#### 2.5.3 Ảnh minh họa

| Mã | Yêu cầu | Ưu tiên | Nguồn |
|---|---|---|---|
| FR-BOK-09 | Sinh ảnh cho một shot hoặc mọi shot; trạng thái từng ảnh (pending, generating, done, failed); Regenerate. | M | QS |
| FR-BOK-10 | Sửa ảnh: Describe→Edit (mô tả thay đổi), Fix a spot (tô vùng + mô tả), Retry khi lỗi; lưu lịch sử phiên bản ảnh để khôi phục. | M | QS |
| FR-BOK-13 | Lưới ảnh theo chương và shot; lối tắt "Sinh lại" và "Sửa ảnh". | M | QS (điều chỉnh) |
| FR-BOK-16 | Tải ZIP ảnh minh họa theo chương hoặc cả dự án. | S | QS (điều chỉnh) |

> Đã bỏ theo quyết định B1: Compile book, Pages, trình đọc sách Flip/Scroll, xuất PDF (FR-BOK-11, 12, 14, 15 và phần PDF của FR-BOK-16 cũ).

#### 2.5.4 Thuyết minh nguyên văn

| Mã | Yêu cầu | Ưu tiên | Nguồn |
|---|---|---|---|
| FR-NAR-01 | Cài đặt thuyết minh của dự án: ngôn ngữ (Auto theo truyện hoặc chọn), **giọng đọc** (chọn từ danh mục, nghe thử), tốc độ (0,8–1,3×), cao độ, khoảng nghỉ giữa câu và giữa đoạn. | M |
| FR-NAR-02 | **Văn bản TTS = đúng đoạn nguồn của shot** (`chapter.content[sourceStart:sourceEnd]`). Người dùng không có ô nào để sửa lời đọc trong phân hệ này; muốn đổi lời thì phải sửa chính văn bản chương (BR-19, BR-21). | M |
| FR-NAR-03 | **Chuẩn hóa chỉ cho phát âm, không đổi văn bản:** quy tắc tất định áp lên *bản đọc* (bỏ ký hiệu markdown như `*`, `[ ]`; đọc số, ngày, đơn vị; ngắt nghỉ theo dấu câu). Văn bản hiển thị và phụ đề vẫn là nguyên văn. Mọi quy tắc được ghi log để truy vết. | M |
| FR-NAR-04 | **Từ điển phát âm theo dự án:** cặp *từ viết → cách đọc* (tên riêng, từ mượn, từ Hán Việt). Chỉ ảnh hưởng audio (SSML alias/phoneme), không đổi chữ. | S |
| FR-NAR-05 | **Đa giọng (tùy chọn):** gán giọng riêng cho lời thoại trong ngoặc kép của từng nhân vật (nhận diện bằng LLM, người dùng duyệt). Nội dung đọc vẫn nguyên văn; chỉ đổi giọng. | C |
| FR-NAR-06 | Sinh thuyết minh cho một shot, một chương hoặc cả dự án; hiện tổng giá theo số ký tự trước khi chạy. Đoạn vượt giới hạn provider được chia theo câu rồi nối audio. | M |
| FR-NAR-07 | **Kiểm chứng lời đọc:** sau TTS, chạy forced alignment / STT so với văn bản nguồn, tính WER và đánh dấu các từ lệch. Nếu WER ≤ ngưỡng (mặc định 3%) thì `VERIFIED`, ngược lại `NEEDS_REVIEW` và hiện các từ nghi sai. | M |
| FR-NAR-08 | Với shot `NEEDS_REVIEW`: nghe lại, thêm mục vào từ điển phát âm và sinh lại, hoặc **chấp nhận thủ công** (ghi người chấp nhận và thời điểm). | M |
| FR-NAR-09 | Sửa văn bản chương hoặc dời ranh giới shot thì thuyết minh của các shot bị ảnh hưởng chuyển `OUTDATED` (so sánh hash đoạn nguồn). | M |

### 2.6 M06 — Trình chỉnh sửa & xuất video (EDT) · lõi

> Bước 5–6 của luồng chính (quyết định D2). Trình chỉnh sửa **timeline nhiều track**, dựng từ tư liệu của M05. Nhạc nền và SFX được thêm tại đây. Track thuyết minh bị **khóa nội dung** để bảo đảm thuyết minh nguyên văn (BR-19, BR-24). Sơ đồ: `../so-do/04-tuan-tu/seq-chinh-sua-xuat-video.puml`.

#### 2.6.1 Timeline & track

| Mã | Yêu cầu | Ưu tiên | Nguồn |
|---|---|---|---|
| FR-EDT-01 | Mở trình chỉnh sửa cho một chương hoặc cả dự án (các chương nối tiếp). **Bản nháp timeline** được dựng tự động từ tư liệu: track **Video** (mỗi shot một clip ảnh, thời lượng = audio + đệm 0,3 s / 0,5 s), track **Thuyết minh** (mỗi shot một clip audio, theo thứ tự), track **Phụ đề** (nguyên văn), track **Nhạc nền** và **SFX** để trống; mặc định Ken Burns luân phiên và crossfade 0,5 s. | M | ĐX |
| FR-EDT-02 | Loại track: Video (ảnh), Overlay (chữ, logo, hình), Phụ đề, Thuyết minh (khóa), Nhạc nền, SFX (có thể nhiều track). Thêm, xóa, đổi tên, ẩn, tắt tiếng track (trừ track Thuyết minh: không xóa được). | M | ĐX |
| FR-EDT-03 | Thao tác timeline: kéo thả, di chuyển, cắt (split), trim đầu/cuối, nhân bản, xóa clip; chọn nhiều; zoom và cuộn timeline; snap theo playhead và mép clip; thước thời gian; phím tắt; **undo/redo** tối thiểu 100 bước. | M | ĐX |
| FR-EDT-04 | **Ràng buộc nguyên văn (BR-24):** clip thuyết minh **không** được cắt, trim, xóa, đổi thứ tự, đổi tốc độ hay chồng lên nhau. Chỉ được (a) dời thời điểm bắt đầu để chèn khoảng lặng và (b) chỉnh âm lượng hoặc keyframe âm lượng. Clip ảnh của một shot phải hiển thị **suốt** thời gian đọc đoạn của shot đó; được dài hơn, không được ngắn hơn. | M | ĐX |
| FR-EDT-05 | Clip tiêu đề (tên truyện, tên chương, tác giả) và clip kết (credit) dạng overlay trên nền màu hoặc ảnh; không có thuyết minh trừ khi bật "đọc tên chương". | S | ĐX |

#### 2.6.2 Hình ảnh & chuyển cảnh

| Mã | Yêu cầu | Ưu tiên | Nguồn |
|---|---|---|---|
| FR-EDT-06 | **Hiệu ứng chuyển động ảnh (Ken Burns):** none, zoom in/out, pan bốn hướng; cường độ; điểm tập trung chọn trên ảnh; nhiều pha cho clip dài; keyframe vị trí/tỷ lệ (nâng cao). | M | ĐX |
| FR-EDT-07 | **Chuyển cảnh** giữa hai clip ảnh: cut, fade, crossfade, fade-to-black/white, slide, wipe, zoom; thời lượng 0–1,5 s; kéo thả từ thư viện chuyển cảnh; áp hàng loạt. Chuyển cảnh không làm thay đổi vị trí clip thuyết minh. | M | ĐX |
| FR-EDT-08 | **Khung hình:** ảnh lệch tỷ lệ video thì crop (theo điểm tập trung), fit (viền màu) hoặc nền mờ; tỷ lệ video 16:9 / 9:16 / 1:1 theo dự án. | M | ĐX |
| FR-EDT-09 | **Tinh chỉnh hình ảnh:** độ sáng, tương phản, bão hòa, nhiệt độ màu, bộ lọc màu (preset); áp cho một clip, nhiều clip hoặc toàn video. | S | ĐX |
| FR-EDT-10 | **Overlay chữ:** nội dung, font (hỗ trợ tiếng Việt), cỡ, màu, viền/bóng, vị trí, hiệu ứng xuất hiện/biến mất; overlay hình (logo, watermark). | S | ĐX |
| FR-EDT-11 | **Phụ đề:** bật/tắt; luôn hiển thị **nguyên văn** (BR-22), ngắt dòng theo timestamp alignment (≤ 2 dòng, ≤ 42 ký tự/dòng); kiểu cả câu hoặc karaoke; font, cỡ, màu, nền, vị trí trong vùng an toàn. Nội dung phụ đề **không sửa được** trong trình chỉnh sửa, chỉ sửa kiểu. | M | ĐX |

#### 2.6.3 Âm thanh: nhạc nền & SFX

| Mã | Yêu cầu | Ưu tiên | Nguồn |
|---|---|---|---|
| FR-EDT-12 | **Thư viện âm thanh:** nhạc nền và SFX của hệ thống, có license; tìm theo từ khóa, thể loại, tâm trạng, thời lượng; nghe thử. Người dùng tải lên nhạc/SFX riêng (MP3/WAV/M4A, kèm cam kết bản quyền, BR-26). | M | ĐX |
| FR-EDT-13 | **Nhạc nền:** kéo vào track Nhạc nền; nhiều đoạn nối tiếp; cắt, trim, lặp; fade in/out; âm lượng và keyframe âm lượng; **ducking tự động** dưới thuyết minh (mức giảm dB chỉnh được). | M | ĐX |
| FR-EDT-14 | **SFX:** kéo vào track SFX tại thời điểm bất kỳ; nhiều SFX chồng nhau trên nhiều track; cắt, trim, fade, âm lượng. | M | ĐX |
| FR-EDT-15 | **Trộn âm:** âm lượng từng track, tắt tiếng hoặc solo track; chuẩn hóa loudness đầu ra (mặc định −14 LUFS cho mạng xã hội); chống clipping. | S | ĐX |
| FR-EDT-16 | **AI âm thanh trong trình chỉnh sửa (tùy chọn):** sinh nhạc nền hoặc SFX từ mô tả; **gợi ý SFX** theo đoạn văn của từng shot (AI đề xuất, người dùng duyệt mới chèn). Tốn credit theo bảng giá. | C | ĐX |

#### 2.6.4 Xem trước, lưu & đồng bộ

| Mã | Yêu cầu | Ưu tiên | Nguồn |
|---|---|---|---|
| FR-EDT-17 | **Xem trước** theo thời gian thực trong trình duyệt (không cần render): play/pause, tua, scrub; hình, thuyết minh, nhạc, SFX, phụ đề đồng bộ. | M | ĐX |
| FR-EDT-18 | **Tự động lưu** (debounce ≤ 2 s) với khóa lạc quan theo version; lịch sử phiên bản timeline, đặt tên phiên bản, khôi phục. Hai người cùng sửa một timeline thì áp dụng cơ chế xung đột như FR-PRJ-11. | M | ĐX |
| FR-EDT-19 | **Đồng bộ với tư liệu:** khi shot được sinh lại ảnh hoặc thuyết minh, hoặc storyboard thay đổi (tách/gộp shot), trình chỉnh sửa cập nhật clip tương ứng và **giữ** các chỉnh sửa của người dùng (hiệu ứng, chuyển cảnh, nhạc, SFX); clip bị ảnh hưởng được đánh dấu để người dùng kiểm tra. | M | ĐX |
| FR-EDT-20 | Mọi thao tác chỉnh sửa (trừ FR-EDT-16) không tốn credit. | M | ĐX |

#### 2.6.5 Xuất & tải video

| Mã | Yêu cầu | Ưu tiên | Nguồn |
|---|---|---|---|
| FR-EDT-21 | Xuất MP4 (H.264 + AAC, 30 fps) theo tỷ lệ dự án: 1920×1080, 1080×1920 hoặc 1080×1080; tùy chọn 720p để xuất nháp nhanh. | M | ĐX |
| FR-EDT-22 | **Điều kiện xuất (BR-23):** track Thuyết minh đầy đủ mọi shot, đúng thứ tự, trạng thái `VERIFIED`/`ACCEPTED`; không clip nào `OUTDATED`; mọi ảnh `DONE`; **độ phủ văn bản 100%**. Thiếu điều kiện thì liệt kê vị trí chưa đạt trên timeline. | M | ĐX |
| FR-EDT-23 | Tiến độ xuất theo % qua SSE; có thể hủy. | M | ĐX |
| FR-EDT-24 | Mỗi lần xuất tạo **phiên bản** render; danh sách Renders theo chương hoặc dự án; đặt bản chính; xóa. | M | ĐX |
| FR-EDT-25 | **Tải xuống** MP4, phụ đề SRT/VTT và audio thuyết minh (MP3/WAV) qua link ký có thời hạn. | M | ĐX |
| FR-EDT-26 | Chia video dài theo chương hoặc theo giới hạn thời lượng (vd. ≤ 10 phút), cắt tại ranh giới shot. | S | ĐX |

### 2.7 M07 — AI Director (DIR) · lõi

| Mã | Yêu cầu | Ưu tiên | Nguồn |
|---|---|---|---|
| FR-DIR-01 | Panel Director dạng chat; người dùng hỏi hoặc ra lệnh bằng ngôn ngữ tự nhiên ("làm lại shot 3 chương 2", "thêm bóng mờ cho quản lý"). | M | QS |
| FR-DIR-02 | Director gọi các thao tác hệ thống qua **công cụ có kiểm soát** (tool calling), dùng cùng quyền và cùng bảng giá như người dùng thao tác tay. **Bộ tool không có thao tác ghi vào văn bản chương** (BR-21). Nếu người dùng yêu cầu "tóm tắt" hay "viết lại" truyện, Director từ chối và giải thích nguyên tắc nguyên văn. | M | ĐX |
| FR-DIR-03 | Lệnh mơ hồ thì hỏi lại ("Chương nào?", "Shot số mấy?"). | S | QS |
| FR-DIR-04 | Chế độ tự động chạy theo luồng chính: pickStyle → split (chia chương) → cast (thế giới truyện) → pickVoice → media (storyboard tự động + ảnh + thuyết minh) → verify (duyệt thuyết minh) → draftTimeline (dựng bản nháp timeline). Sau đó Director **dừng** để người dùng chỉnh sửa video; xuất video chỉ chạy khi người dùng yêu cầu. | M | QS (điều chỉnh) |
| FR-DIR-05 | Điểm duyệt bắt buộc: chọn style và duyệt cast trước khi sinh ảnh; **chọn giọng đọc** trước khi sinh thuyết minh; **duyệt các shot `NEEDS_REVIEW`** trước khi dựng timeline (BR-09, BR-23). Trước mỗi bước tốn phí, hiển thị tổng giá ước tính. | M | QS + ĐX |
| FR-DIR-06 | Pause / Continue / Exit auto; trạng thái kế hoạch lưu bền vững và tiếp tục được sau khi tải lại trang. | M | QS |
| FR-DIR-07 | Bước nào đã xong thì bỏ qua (vd. chương đã có đủ tư liệu). Khi hoàn tất báo "Mọi chương đã sẵn sàng dựng video". | M | QS (điều chỉnh) |
| FR-DIR-08 | Director có thể viết nội dung giúp người dùng (prompt ảnh, caption, Visual Rule) và ghi Director note. | S | QS |
| FR-DIR-09 | Review: Director đánh giá kết quả một bước (vd. shot lệch nhân vật) và đề xuất sửa. | C | SL |

### 2.8 M08 — Thư viện tài sản cá nhân (LIB) · phụ trợ

| Mã | Yêu cầu | Ưu tiên | Nguồn |
|---|---|---|---|
| FR-LIB-01 | Thư viện gồm 3 tab Characters / Locations / Items, có đếm; tìm kiếm; sắp xếp Recent. | M | QS |
| FR-LIB-02 | Lọc All / My Created / From Projects. | M | QS |
| FR-LIB-03 | Tạo nhân vật từ ảnh hoặc mô tả ngoài dự án. | S | QS |
| FR-LIB-04 | Tài sản tạo trong dự án có tùy chọn "Lưu vào thư viện" để tái sử dụng. | M | ĐX |
| FR-LIB-05 | Tài sản thư viện khi thêm vào dự án được **sao chép tham chiếu** (dùng chung ảnh gốc), sửa trong dự án không ảnh hưởng thư viện. | M | ĐX |

### 2.9 M09 — Credit & thanh toán (BIL) · phụ trợ

| Mã | Yêu cầu | Ưu tiên | Nguồn |
|---|---|---|---|
| FR-BIL-01 | Trang Pricing: tab Monthly / Annual / Credit Packs; danh sách gói; FAQ về credit. | M | QS |
| FR-BIL-02 | Đăng ký gói qua checkout có host của cổng thanh toán. | M | QS |
| FR-BIL-03 | Mua credit pack một lần, không hết hạn. | M | QS |
| FR-BIL-04 | Manage Billing qua portal của cổng: nâng/hạ gói, đổi thẻ, hóa đơn, hủy gói. | M | QS |
| FR-BIL-05 | Ví credit có hai nguồn, trừ theo thứ tự: subscription (hết hạn cuối kỳ) trước, pack sau. | M | ĐX |
| FR-BIL-06 | Sổ cái credit chỉ ghi thêm (append-only); mỗi bút toán có loại, số lượng, job hoặc hóa đơn liên quan, người thực hiện. | M | ĐX |
| FR-BIL-07 | Credit miễn phí hằng ngày (daily claim) cho tài khoản free. | C | QS |
| FR-BIL-08 | Người dùng xem lịch sử tiêu credit theo dự án và theo loại thao tác. | S | ĐX |
| FR-BIL-09 | Webhook thanh toán xử lý idempotent theo event id; xác thực chữ ký. | M | ĐX |

### 2.10 M10 — Quản trị (ADM) · phụ trợ [ĐX]

| Mã | Yêu cầu | Ưu tiên |
|---|---|---|
| FR-ADM-01 | Cấu hình bảng giá credit theo loại thao tác (xem [08](08-quy-tac-nghiep-vu.md) §3); có phiên bản và ngày hiệu lực. | M |
| FR-ADM-02 | Cấu hình gói (giá, credit/tháng, quyền lợi) đồng bộ với cổng thanh toán. | M |
| FR-ADM-03 | Quản lý provider và mô hình AI: bật/tắt, thứ tự ưu tiên, chi phí thực mỗi đơn vị; danh mục style, **danh mục giọng đọc** (kèm audio mẫu), **thư viện nhạc & SFX có license**. | M |
| FR-ADM-04 | Giám sát job: lọc theo trạng thái, provider, người dùng; xem lỗi; chạy lại hoặc hoàn credit thủ công. | M |
| FR-ADM-05 | Điều chỉnh credit người dùng (bắt buộc ghi lý do, ghi vào ledger). | M |
| FR-ADM-06 | Báo cáo: credit tiêu thụ, chi phí AI theo provider, biên lợi nhuận, tỷ lệ job lỗi. | S |

---

## 3. Yêu cầu giao diện ngoài

| Mã | Giao diện | Năng lực cần có |
|---|---|---|
| IF-01 | Web UI | Responsive; Studio tối ưu desktop ≥ 1280px; tablet ≥ 768px chỉ đọc và chỉnh nhẹ |
| IF-02 | LLM | Chat completion, structured output (JSON Schema), tool calling, streaming, context ≥ 128k token |
| IF-03 | Image | Text-to-image có ảnh tham chiếu (≥ 3 ảnh), edit theo hướng dẫn, inpainting theo mask |
| IF-04 | STT / Forced aligner | Timestamp cấp từ cho audio + văn bản đã biết (tiếng Việt, tiếng Anh); STT để tính WER |
| IF-05 | TTS / Music & SFX (tùy chọn) | TTS đa ngôn ngữ chất lượng cao (tiếng Việt bắt buộc), hỗ trợ SSML (alias/phoneme/break), trả timestamp nếu có, đọc **đúng văn bản đầu vào** (không "cải biên"); nhạc nền theo mô tả và thời lượng (tùy chọn) |
| IF-09 | Render engine | FFmpeg (zoompan, xfade, subtitles/ASS, sidechaincompress để ducking) hoặc Remotion; chạy trong hạ tầng của hệ thống |
| IF-06 | Payment | Checkout, customer portal, webhook có chữ ký |
| IF-07 | Object storage | S3-compatible, presigned URL |
| IF-08 | Email | Email giao dịch (xác minh, hóa đơn, lời mời) |

Lựa chọn nhà cung cấp cụ thể và lớp adapter xem [05](05-kien-truc-he-thong.md) §5.
