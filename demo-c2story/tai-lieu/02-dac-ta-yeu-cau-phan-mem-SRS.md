# 02 — Đặc tả yêu cầu phần mềm (SRS)

> Theo cấu trúc ISO/IEC/IEEE 29148:2018. Yêu cầu phi chức năng ở [07](07-yeu-cau-phi-chuc-nang.md). Quyết định nguồn ở [sổ quyết định](../quyet-dinh.md).
> Ưu tiên MoSCoW: **M** (Must) bắt buộc trong MVP; **S** (Should) làm nếu kịp trong MVP hoặc sau MVP; **C** (Could) sau MVP.
> **GĐ** (giai đoạn, [09 §1](09-ke-hoach-phat-trien.md)): **P0–P3** thuộc MVP; **Sau** là sau MVP (không làm trong đồ án trừ khi MVP xong sớm); **Bỏ** là đã loại khỏi phạm vi. Ký hiệu **✂n** là vị trí thứ n trong thứ tự cắt giảm khi trễ tiến độ: ✂1–✂5 tầng 1 (QĐ-05), ✂6–✂10 tầng 2 (QĐ-91), xem [09 §1.3](09-ke-hoach-phat-trien.md).
> Nguồn: **QS** (quan sát) / **SL** (suy luận) / **ĐX** (đề xuất) / **QĐ-xx** (quyết định đã chốt).

## 1. Giới thiệu

### 1.1 Tác nhân

| Tác nhân | Mô tả |
|---|---|
| Guest | Chưa đăng nhập; chỉ thấy trang giới thiệu, bảng giá và nút "Đăng nhập" (chuyển sang SSO) |
| User | Đã đăng nhập |
| Owner | User tạo dự án (kế thừa Editor). **MVP chỉ có Owner** thao tác trên dự án |
| Editor | User được mời vào dự án (sau MVP) |
| Admin | Quản trị hệ thống |
| AI Gateway | Tác nhân hệ thống phụ: LLM, Image, TTS, STT/Aligner |
| Payment Gateway | Cổng thanh toán, chế độ sandbox (tác nhân phụ) |
| SSO (Identity Provider) | Keycloak tự dựng (P0–P3) và **SSO Vbee** (bắt buộc trước khi bảo vệ, QĐ-21); quản lý toàn bộ đăng ký, đăng nhập, đăng xuất, mật khẩu (tác nhân phụ) |

Sơ đồ: `../so-do/01-use-case/uc-tong-quan.puml`, `../so-do/01-use-case/uc-studio-chi-tiet.puml`. Sơ đồ phân rã của từng phân hệ M01–M10 nằm ở `../so-do/01-use-case/phan-ra/uc-mXX-*.puml`; M05 tách làm hai (5a Storyboard, 5b Sinh ảnh & thuyết minh).

### 1.2 Quy ước mã
`FR-<phân hệ>-<số>`. Truy vết tới use case và test: [09](09-ke-hoach-phat-trien.md) §4.

### 1.3 Phạm vi MVP tóm tắt

| Phân hệ | Trong MVP | Sau MVP |
|---|---|---|
| M01 SSO | Đăng nhập, đăng xuất, hồ sơ (Keycloak → Vbee), danh sách mời beta, màn hình đồng ý xử lý dữ liệu | Back-channel logout, tự yêu cầu xóa dữ liệu (làm thủ công) |
| M02 Dự án | Danh sách, import, tạo trống, cài đặt, xóa, Map ✂1 | Link mời, thành viên, xung đột giữa nhiều người, realtime, nhân bản |
| M03 Bản thảo | Văn bản gốc, Workspace, chia/gộp/dời/sắp xếp chương, tái cấu trúc nguyên tử, dời ranh giới shot | Find & replace, Archives, Notes, lịch sử phiên bản chương |
| M04 Thế giới truyện | Phân tích tài sản, CRUD tài sản, ảnh tham chiếu, ảnh tải lên, style, Art Direction, Visual Rules, Timeline truyện ✂4, Relationships ✂3 | Thư viện, xuất ZIP |
| M05 Sinh tư liệu | Storyboard phủ kín, biên tập shot, sinh/sửa ảnh, TTS nguyên văn, quy tắc ký hiệu, từ điển phát âm ✂5, nghe & đánh dấu, "Sinh tư liệu", media bin | Quản lý nhiều bản nháp, chapter rules, re-direct, đa giọng, kiểm chứng ASR, ZIP ảnh |
| M06 Trình chỉnh sửa | Track video/thuyết minh/phụ đề/nhạc/SFX, Ken Burns, chuyển cảnh cơ bản (nâng cao ✂2), phụ đề (preset ✂2), tải nhạc lên, ducking, preview, render, tải MP4/SRT | Overlay, tinh chỉnh màu, keyframe, lịch sử phiên bản timeline, thư viện âm thanh, trộn âm nâng cao, chia video |
| M07 AI Director | — | Toàn bộ |
| M08 Thư viện cá nhân | — | Toàn bộ |
| M09 Ví & thanh toán | Ví USD, tiền dùng thử, giữ/trừ/hoàn, giới hạn Free, nạp tiền sandbox, lịch sử chi tiêu | Gói đăng ký, hóa đơn, portal |
| M10 Quản trị | Bảng giá, provider, style, giọng nạp bằng file cấu hình (seed); danh sách mời; trần chi tiêu ngày | Giao diện admin, giám sát job, điều chỉnh số dư, báo cáo |

---

## 2. Yêu cầu chức năng

### 2.1 M01 — Tích hợp SSO & hồ sơ (AUTH) · phụ trợ

> **Không phát triển lại** đăng ký, đăng nhập, đăng xuất, quên/đổi mật khẩu, xác minh email, MFA. Toàn bộ do SSO đảm nhiệm; ứng dụng là một *Relying Party (RP)* OIDC. Sơ đồ: `../so-do/04-tuan-tu/seq-dang-nhap-sso.puml`.

| Mã | Yêu cầu | Ưu tiên | GĐ | Nguồn |
|---|---|---|---|---|
| FR-AUTH-01 | Nút "Đăng nhập" chuyển người dùng sang trang đăng nhập của SSO (OIDC Authorization Code + PKCE, kèm `state` và `nonce`). Người chưa có tài khoản **đăng ký ngay trên SSO**; ứng dụng không có form đăng ký. | M | P0 | ĐX |
| FR-AUTH-02 | Callback: đổi `code` lấy token ở backend; xác thực ID token (chữ ký theo JWKS, `iss`, `aud`, `exp`, `nonce`); tạo phiên ứng dụng bằng cookie httpOnly. Token SSO chỉ lưu phía server (mẫu BFF), không bao giờ gửi cho trình duyệt. | M | P0 | ĐX |
| FR-AUTH-03 | Sau khi đăng nhập, chuyển về URL đã yêu cầu trước đó. URL đích chỉ được là đường dẫn nội bộ, để chống open redirect. | M | P0 | QS |
| FR-AUTH-04 | **Cấp hồ sơ tự động (JIT provisioning):** lần đăng nhập đầu, nếu email có trong danh sách mời (FR-AUTH-11) thì tạo `users` cục bộ gắn với `sub` của SSO, tạo ví và tặng tiền dùng thử (FR-BIL-10); mỗi lần đăng nhập đồng bộ email, tên, avatar từ claims. Hồ sơ cục bộ chỉ chứa dữ liệu riêng của ứng dụng (locale giao diện, ví, dự án). | M | P0 | ĐX, QĐ-25 |
| FR-AUTH-05 | **Đăng xuất:** xóa phiên ứng dụng, sau đó gọi RP-initiated logout tới `end_session_endpoint` của SSO (kèm `id_token_hint`, `post_logout_redirect_uri`). Nhận `logout_token` back-channel để hủy mọi phiên của người dùng: **sau MVP**. | M | P0 | ĐX |
| FR-AUTH-06 | Gia hạn phiên: dùng refresh token của SSO ở backend; nếu SSO thu hồi hoặc tài khoản bị khóa thì phiên ứng dụng hết hiệu lực ở lần gia hạn kế tiếp (≤ 15 phút). | M | P0 | ĐX, QĐ-24 |
| FR-AUTH-07 | **Vai trò Admin** của ứng dụng lấy từ claim/nhóm của SSO (vd. `roles` chứa `story-studio:admin`); nếu SSO không có claim thì quản lý bằng danh sách cục bộ. | M | P0 | ĐX |
| FR-AUTH-08 | Đổi ngôn ngữ giao diện (vi, en), lưu ở hồ sơ cục bộ; mặc định lấy claim `locale` nếu có. | S | P3 | QS |
| FR-AUTH-09 | Dashboard hiển thị trạng thái tài khoản (Free / Đã nạp tiền), số dư ví, phần Free đã dùng trong tháng (lượt render, phút video), số dự án; link "Quản lý tài khoản" mở trang hồ sơ của SSO. | M | P2 | QS, QĐ-35 |
| FR-AUTH-10 | Khi phát hiện tài khoản bị xóa hoặc vô hiệu ở SSO (lúc đăng nhập hoặc gia hạn phiên), ứng dụng khóa hồ sơ cục bộ. Người dùng **tự yêu cầu xóa dữ liệu** (lên lịch xóa dự án sau 30 ngày): sau MVP; trong đồ án, Admin xóa thủ công theo yêu cầu và xóa toàn bộ dữ liệu beta sau ngày bảo vệ. | M | P0 / Sau | ĐX, QĐ-24 |
| FR-AUTH-11 | **Danh sách mời closed beta:** Admin thêm/gỡ email được mời. Đăng nhập SSO thành công nhưng email không có trong danh sách và chưa có hồ sơ: hiện "Bạn chưa được mời tham gia beta", không tạo hồ sơ, không tặng tiền (BR-30). Tắt được bằng cấu hình khi mở rộng. | M | P0 | QĐ-25 |
| FR-AUTH-12 | **Đồng ý xử lý dữ liệu cá nhân:** lần đăng nhập đầu (hoặc khi đổi phiên bản thông báo) hiện màn hình nêu dữ liệu thu thập, mục đích, thời hạn xóa; lưu thời điểm và phiên bản đồng ý; không đồng ý thì đăng xuất (BR-31). | M | P0 | QĐ-26 |
| FR-AUTH-13 | **Kết nối SSO Vbee** thay Keycloak qua cùng cổng `IdentityProviderPort` (ADR-20): cấu hình discovery hoặc endpoint thủ công, ánh xạ claims. Nếu Vbee chỉ có OAuth 2.0: lấy thông tin qua userinfo, không có back-channel logout. Hạn có tài liệu từ Vbee: hết tháng thứ 2; quá hạn thì giữ Keycloak (QĐ-22). | M | P3 | QĐ-21, QĐ-23 |

### 2.2 M02 — Quản lý dự án & cộng tác (PRJ) · lõi

| Mã | Yêu cầu | Ưu tiên | GĐ | Nguồn |
|---|---|---|---|---|
| FR-PRJ-01 | Trang Projects liệt kê dự án mà User là Owner hoặc Editor, gồm tiêu đề, số chương, style, trạng thái (In Progress / Done), ngày cập nhật; Owner có nút xóa. Trạng thái **suy ra, không lưu cột**: *Done* khi dự án có ≥ 1 chương và mọi chương `EXPORTED`, ngược lại *In Progress*. Có ô tìm theo tiêu đề (không phân biệt hoa thường, dấu) và lọc theo trạng thái; danh sách phân trang. | M | P1 | QS + ĐX |
| FR-PRJ-02 | "Import your story": dán văn bản hoặc tải file .txt/.md/.docx (≤ 2 MB, ≤ 500.000 ký tự). Tài khoản Free tối đa 1 dự án (BR-27). | M | P1 | QS |
| FR-PRJ-03 | Import **luôn giữ nguyên văn**. Hệ thống chỉ chuẩn hóa kỹ thuật không làm đổi chữ: chuẩn Unicode NFC, thống nhất ký tự xuống dòng, bỏ ký tự điều khiển vô hình. Không có tùy chọn AI viết lại (BR-19, BR-21). *Khác với hệ thống tham chiếu.* | M | P1 | ĐX |
| FR-PRJ-04 | Tạo dự án trống rồi viết trực tiếp trong Workspace. | M | P1 | QS |
| FR-PRJ-05 | Bố cục Studio: thanh trái gồm các nhóm Write (Workspace, Split into chapters), Your world (Story Assets, Timeline, Relationships, Visual Rules), Make·Media (Sinh tư liệu, Storyboard, Ảnh, Thuyết minh theo chương), Make·Video (Trình chỉnh sửa, Renders), danh sách chương, Settings. Vùng giữa là các tab có thể đóng. Màn hình hiện tại thể hiện trên URL (`?v=<view>[:<id>]`) để chia sẻ link. Find & replace, Archives, Project Assets, panel Notes/Director: sau MVP. | M | P1 | QS |
| FR-PRJ-06 | Map overview: sơ đồ chặng (1 Nhập truyện → 2 Chia chương → 3 Thế giới truyện → 4 Sinh tư liệu → 5 Chỉnh sửa video → 6 Xuất & tải), làm nổi bật chặng hiện tại; bấm một chặng để chuyển tới. Trang tĩnh, khoảng 1–2 ngày công. | S | P3 ✂1 | QS (điều chỉnh), QĐ-61 |
| FR-PRJ-07 | Settings (chỉ Owner): style, mô hình ảnh, ngôn ngữ, thời lượng mục tiêu mỗi ảnh (mặc định 15 s đọc), hiển thị, **tỷ lệ khung hình video mục tiêu (16:9 / 9:16 / 1:1)**. Ảnh shot được sinh theo tỷ lệ này. Lưu ngay khi chọn. | M | P1 | QS + ĐX |
| FR-PRJ-08 | Share (chỉ Owner): tạo, sao chép và thu hồi link mời; ai mở link sẽ tham gia làm Editor. | S | Sau | QS, QĐ-04 |
| FR-PRJ-09 | Collaborators: Owner xem danh sách thành viên, xóa thành viên. | S | Sau | QS, QĐ-04 |
| FR-PRJ-10 | Ma trận quyền theo [08](08-quy-tac-nghiep-vu.md) §2. | M | P1 | QS |
| FR-PRJ-11 | Mỗi chương hiển thị người sửa cuối. Khi lưu bị xung đột phiên bản, hiện hộp thoại: "Lưu bản của tôi thành nháp" (đưa vào Archives) hoặc "Tải bản của họ". MVP chỉ báo xung đột và yêu cầu tải lại (BR-05). | S | Sau | QS, QĐ-04 |
| FR-PRJ-12 | Thay đổi của người khác được đẩy về theo thời gian thực (danh sách chương). Trạng thái job vẫn đẩy qua SSE trong MVP (FR-MED-02). | S | Sau | ĐX |
| FR-PRJ-13 | Nhân bản dự án (Duplicate) cùng toàn bộ chương và tài sản, không kèm video. | C | Sau | ĐX |

### 2.3 M03 — Bản thảo & chương (MAN) · lõi

| Mã | Yêu cầu | Ưu tiên | GĐ | Nguồn |
|---|---|---|---|---|
| FR-MAN-01 | Màn hình Write (source) hiển thị văn bản gốc, số ký tự, số chương; có Copy text, Re-import, Suggest chapter splits; mỗi đoạn văn có nút "Split here". | M | P1 | QS |
| FR-MAN-02 | Workspace: trình soạn thảo liền mạch cho mọi chương (cuộn một trang); mỗi chương có tiêu đề sửa được, số ký tự, nút Storyboard, Sinh tư liệu, Mở trình chỉnh sửa, Chapter actions. Chương đã có storyboard hiện hành thì hiện **vạch ranh giới shot** (FR-BOK-01b). | M | P1 | QS, QĐ-52 |
| FR-MAN-03 | Chia chương tại vị trí con trỏ hoặc giữa hai đoạn. Tài khoản Free tối đa 3 chương (BR-27). | M | P1 | QS |
| FR-MAN-04 | AI gợi ý điểm chia chương (vị trí đoạn + tiêu đề); áp dụng toàn bộ hoặc từng điểm; nếu đã khớp thì báo "Your current chapters already match". Tính phí theo BR-01. | M | P1 | QS |
| FR-MAN-05 | Thêm chương (cuối hoặc chèn giữa), xóa, đổi tên, sắp xếp lại (kéo thả hoặc chọn vị trí), gộp vào chương trước, dời ranh giới từng đoạn văn. | M | P1 | QS |
| FR-MAN-06 | Mọi thao tác tái cấu trúc chương chạy trong **một giao dịch**; thất bại thì rollback toàn bộ. | M | P1 | ĐX |
| FR-MAN-07 | Find & replace trên tiêu đề và nội dung mọi chương có thể sửa, khớp chính xác, phân biệt hoa thường; xem trước số kết quả. | S | Sau | QS |
| FR-MAN-08 | Archives: đặt tên và lưu ảnh chụp chỉ đọc của toàn bộ bản thảo; xem, sao chép và xóa. | S | Sau | QS, QĐ-04 |
| FR-MAN-09 | Notes: ghi chú cấp dự án; có thể gắn vào chương hoặc shot; Director được phép thêm "Director note". | S | Sau | QS |
| FR-MAN-10 | Lịch sử phiên bản chương: xem, khôi phục. | S | Sau | QS |
| FR-MAN-11 | Chương có thể bị khóa (locked) trong khi job đang chạy trên nó; giao diện báo "This chapter is locked". | S | P2 | QS |

### 2.4 M04 — Thế giới truyện (WLD) · lõi

| Mã | Yêu cầu | Ưu tiên | GĐ | Nguồn |
|---|---|---|---|---|
| FR-WLD-01 | Analyze assets: AI đọc mọi chương, đề xuất nhân vật, địa điểm, đạo cụ **lặp lại**; danh sách "Recommended assets" cho người dùng chọn thêm hoặc bỏ. Tính phí theo BR-01. | M | P1 | QS |
| FR-WLD-02 | Story Assets gồm 3 nhóm Characters / Locations / Props, hỗ trợ Group (nhóm nhân vật). Thuộc tính: tên, bí danh, mô tả ngoại hình, facts bất biến, ảnh tham chiếu. | M | P1 | QS |
| FR-WLD-03 | Tạo tài sản mới (New character / location / prop); sinh hoặc sinh lại ảnh tham chiếu; địa điểm có reference sheet nhiều góc nhìn. | M | P1 | QS |
| FR-WLD-04 | Dùng ảnh tải lên làm tài sản, không vẽ lại ("Use this exact image"). | S | P1 | QS |
| FR-WLD-05 | Gỡ tài sản khỏi Story Assets / khỏi dự án (BR-16). | M | P1 | QS, QĐ-59 |
| FR-WLD-06 | Set style cho dự án; "Regenerate all (n)" sinh lại mọi ảnh tham chiếu theo style hiện tại (hiện tổng giá trước khi chạy). | M | P1 | QS |
| FR-WLD-07 | Art direction: văn bản phong cách bổ sung lên style dự án, áp cho mọi tài sản và mọi ảnh. | M | P1 | QS |
| FR-WLD-08 | Story timeline: AI gán cho mỗi chương nhãn ngày, mùa và tóm tắt; hiển thị theo tỷ lệ thời gian; Re-analyse. Hai chế độ xem: **theo mạch truyện** (thứ tự chương) và **theo thứ tự thời gian** (theo nhãn ngày/mùa, cho truyện có hồi tưởng). Prompt storyboard dùng dữ liệu này để dựng bối cảnh. | M | P2 ✂4 | QS + ĐX, QĐ-04 |
| FR-WLD-09 | Relationship graph: AI trích cặp nhân vật, nhãn quan hệ và diễn biến; hiển thị dạng đồ thị; Re-analyse. | M | P2 ✂3 | QS, QĐ-04 |
| FR-WLD-10 | Visual Rules: tạo, sửa, xóa luật (tên, nội dung, phạm vi toàn dự án hoặc chương); áp theo BR-08. | M | P1 | QS |
| FR-WLD-11 | Project Assets (hộp thoại quản trị đầy đủ): thêm, gỡ, bí danh, nhóm; xuất ZIP ảnh tài sản. | S | Sau | QS |
| FR-WLD-12 | Thêm tài sản có sẵn từ thư viện cá nhân (M08); xóa vĩnh viễn khỏi thư viện (xác nhận 2 bước). | S | Sau | QS, QĐ-59 |

### 2.5 M05 — Sinh tư liệu: ảnh + thuyết minh nguyên văn (MED) · lõi

> Bước 4 của luồng chính. Đầu ra **chỉ gồm ảnh minh họa và audio thuyết minh nguyên văn** của từng shot. Nhạc nền và SFX **không** sinh ở bước này; chúng được thêm trong trình chỉnh sửa video (M06). Storyboard chạy **tự động** bên trong bước này; màn hình Storyboard chỉ dùng để tinh chỉnh khi cần.

#### 2.5.1 Điều phối sinh tư liệu

| Mã | Yêu cầu | Ưu tiên | GĐ | Nguồn |
|---|---|---|---|---|
| FR-MED-01 | Nút **"Sinh tư liệu"** cho một chương, nhiều chương hoặc cả dự án. Hệ thống hiện **một** giá ước tính tổng (storyboard + ảnh + TTS), người dùng xác nhận một lần, rồi hệ thống chạy tuần tự: tạo storyboard tự động (nếu chương chưa có bản hiện hành), sau đó với mỗi shot sinh **song song** ảnh minh họa và thuyết minh nguyên văn. | M | P2 | ĐX |
| FR-MED-02 | Bảng tiến độ theo chương và shot: trạng thái ảnh (pending / generating / done / failed) và thuyết minh (pending / generating / done / failed / outdated, kèm cờ "cần sinh lại"); cập nhật realtime qua SSE. | M | P2 | ĐX |
| FR-MED-03 | **Tư liệu dự án (Media bin):** danh sách theo chương → shot, hiển thị ảnh hiện hành, audio thuyết minh (nghe thử), đoạn văn nguồn, thời lượng. Đây là **đầu vào duy nhất** của trình chỉnh sửa video. | M | P1 | ĐX |
| FR-MED-04 | Sinh lại có chọn lọc: chỉ phần thiếu, lỗi, lỗi thời hoặc được đánh dấu cần sinh lại; chỉ ảnh hoặc chỉ thuyết minh của một shot; cả chương. | M | P2 | ĐX |
| FR-MED-05 | Khi mọi shot của chương có ảnh `DONE` và thuyết minh `DONE`, chương ở trạng thái **"Sẵn sàng dựng"** và hệ thống tự tạo **bản nháp timeline** cho chương (FR-EDT-01). | M | P2 | ĐX, QĐ-54 |

#### 2.5.2 Storyboard (tự động, tinh chỉnh tùy chọn)

| Mã | Yêu cầu | Ưu tiên | GĐ | Nguồn |
|---|---|---|---|---|
| FR-BOK-01 | Tạo bản nháp storyboard cho chương: AI chia **toàn bộ** văn bản chương thành N shot liên tục. Mỗi shot gắn với một **đoạn nguồn** `[sourceStart, sourceEnd)` (offset ký tự, ranh giới tại cuối câu). N mặc định suy từ độ dài chương và mục tiêu "thời lượng mục tiêu mỗi ảnh" (mặc định 8–20 s đọc). | M | P1 | QS + ĐX |
| FR-BOK-01a | **Validator phủ kín (BR-20):** khi lưu bản nháp, server kiểm tra các đoạn nguồn sắp theo thứ tự, liên tục, không chồng lấn, phủ `[0, len(chapter))`. Nếu LLM trả sai, server **sửa ranh giới tất định**: snap về ranh giới câu gần nhất; khoảng hở gộp vào shot trước; chồng lấn cắt theo shot sau. Không bao giờ đổi chữ. Sơ đồ `act-phu-kin-van-ban.puml`. | M | P1 | ĐX |
| FR-BOK-01b | Màn hình storyboard hiển thị đoạn nguồn của mỗi shot (nguyên văn, chỉ đọc). **Dời ranh giới** giữa hai shot liền kề làm ở **Workspace** (M03): vạch ranh giới shot hiện trên văn bản chương khi chương có storyboard hiện hành; kéo vạch theo câu. Sau khi dời, AI viết lại brief của 2 shot bị ảnh hưởng (có phí: hiện giá ước tính, chờ xác nhận, BR-33). Không có nút ◀ ▶ trong storyboard. | M | P2 ✂8 | ĐX, QĐ-52 |
| FR-BOK-02 | Quản lý bản nháp: chọn, đổi tên, nhân bản, xóa, so sánh hai bản; "Set as current" (BR-07). | S | Sau | QS |
| FR-BOK-03 | Re-split shots: nhiều hơn (mỗi nhịp truyện một shot) hoặc ít hơn. Trong MVP, bản chia lại sau khi Editor xác nhận thay thế bản hiện hành (bản cũ được giữ, chưa có giao diện quản lý nhiều bản). | M | P1 | QS |
| FR-BOK-04 | Chapter rules: chỉ dẫn cố định cho chương mà AI tuân theo khi viết brief. | S | Sau | QS |
| FR-BOK-05 | Shot gồm: số thứ tự, tiêu đề, focus, cast, item, location, thời điểm, ngày, illustration brief (Subject / Environment / Composition / Camera / Lighting / Mood / Details, một khung hình tĩnh), caption 1–2 câu, đoạn văn nguồn. | M | P1 | QS |
| FR-BOK-06 | Thao tác shot: sửa trường minh họa (title, focus, brief, caption, cast/item/location, thời điểm, ngày); gộp với shot trên/dưới (đoạn nguồn được nối lại); tách đôi tại một ranh giới câu; "Rewrite this shot" (AI viết lại **brief minh họa**, không động vào đoạn nguồn, tính phí). **Xóa shot** không làm mất văn bản: đoạn nguồn của nó gộp vào shot liền trước, hoặc shot liền sau nếu là shot đầu tiên. | M | P1 | QS (điều chỉnh) |
| FR-BOK-07 | Re-direct: AI viết lại brief minh họa cho mọi shot (vd. sau khi đổi Chapter rules); đoạn nguồn giữ nguyên. | S | Sau | QS |
| FR-BOK-08 | Tên cast/item/location chưa khớp tài sản bị cảnh báo; "Scan the chapter text and auto-match" để tự khớp. | M | P1 | QS |

#### 2.5.3 Ảnh minh họa

| Mã | Yêu cầu | Ưu tiên | GĐ | Nguồn |
|---|---|---|---|---|
| FR-BOK-09 | Sinh ảnh cho một shot hoặc mọi shot; trạng thái từng ảnh (pending, generating, done, failed); Regenerate. | M | P1 | QS |
| FR-BOK-10 | Sửa ảnh: Describe→Edit (mô tả thay đổi), Retry khi lỗi; lưu lịch sử phiên bản ảnh để khôi phục. Ngoài ra có thể **thay ảnh shot bằng ảnh tự tải lên** (miễn phí, tạo phiên bản ảnh mới, không bị sinh hàng loạt ghi đè, BR-14). | M | P1 | QS + ĐX, QĐ-51 |
| FR-BOK-13 | Lưới ảnh theo chương và shot; lối tắt "Sinh lại" và "Sửa ảnh". | M | P1 | QS (điều chỉnh) |
| FR-BOK-16 | Tải ZIP ảnh minh họa theo chương hoặc cả dự án. | S | Sau | QS (điều chỉnh) |

> Đã bỏ: Compile book, Pages, trình đọc sách Flip/Scroll, xuất PDF (FR-BOK-11, 12, 14, 15 và phần PDF của FR-BOK-16 cũ); **Fix a spot** (sửa vùng tô, inpainting) theo QĐ-51.

#### 2.5.4 Thuyết minh nguyên văn

| Mã | Yêu cầu | Ưu tiên | GĐ | Nguồn |
|---|---|---|---|---|
| FR-NAR-01 | Cài đặt thuyết minh của dự án: ngôn ngữ (Auto theo truyện hoặc chọn; tiếng Việt, tiếng Anh), **giọng đọc** (chọn từ danh mục, nghe mẫu), tốc độ (0,8–1,3×), cao độ, khoảng nghỉ giữa câu và giữa đoạn, **bật/tắt từng quy tắc ký hiệu** ([08 §6](08-quy-tac-nghiep-vu.md)). | M | P2 | ĐX, QĐ-56 |
| FR-NAR-02 | **Văn bản TTS = đúng đoạn nguồn của shot** (`chapter.content[sourceStart:sourceEnd]`). Người dùng không có ô nào để sửa lời đọc trong phân hệ này; muốn đổi lời thì phải sửa chính văn bản chương (BR-19, BR-21). | M | P2 | ĐX |
| FR-NAR-03 | **Chuẩn hóa chỉ cho phát âm, không đổi văn bản:** quy tắc tất định áp lên *bản đọc*: bỏ ký hiệu trình bày theo [08 §6](08-quy-tac-nghiep-vu.md) nhưng **giữ chữ bên trong** (`*Bố*` đọc "Bố"); dòng phân cách thành khoảng lặng 0,5 s; đọc số, ngày, đơn vị; ngắt nghỉ theo dấu câu. Văn bản hiển thị và phụ đề vẫn là nguyên văn. Mọi quy tắc được ghi log để truy vết. | M | P2 | ĐX, QĐ-56 |
| FR-NAR-04 | **Từ điển phát âm theo dự án:** cặp *từ viết → cách đọc* (tên riêng, từ mượn, từ Hán Việt). Chỉ ảnh hưởng audio (SSML alias/phoneme), không đổi chữ. | S | P2 ✂5 | ĐX |
| FR-NAR-05 | **Đa giọng (tùy chọn):** gán giọng riêng cho lời thoại trong ngoặc kép của từng nhân vật (nhận diện bằng LLM, người dùng duyệt). Nội dung đọc vẫn nguyên văn; chỉ đổi giọng. MVP đọc một giọng kể. | C | Sau | ĐX, QĐ-60 |
| FR-NAR-06 | Sinh thuyết minh cho một shot, một chương hoặc cả dự án; hiện giá ước tính theo số ký tự trước khi chạy. Đoạn vượt giới hạn provider được chia theo câu rồi nối audio. Lấy timestamp từng từ (từ TTS hoặc forced alignment) để dựng phụ đề. | M | P2 | ĐX |
| FR-NAR-07 | **Kiểm chứng lời đọc bằng ASR:** sau TTS, chạy STT so với văn bản nguồn, tính WER và đánh dấu các từ lệch. WER ≤ ngưỡng (mặc định 3%) thì `VERIFIED`, ngược lại `NEEDS_REVIEW`; shot `NEEDS_REVIEW` được nghe lại, sửa từ điển và sinh lại, hoặc **chấp nhận thủ công** (ghi người và thời điểm). Trong MVP, WER ≤ 3% được bảo đảm ở khâu chọn provider (`EVAL-wer-golden`). | S | Sau | ĐX, QĐ-54 |
| FR-NAR-08 | **Kiểm chứng thủ công:** mỗi shot có nút "Nghe" và "Đánh dấu cần sinh lại" (bỏ đánh dấu được); danh sách lọc theo shot đã đánh dấu. **Không bắt buộc** nghe hết mới được xuất (BR-34). | M | P2 | QĐ-54 |
| FR-NAR-09 | Sửa văn bản chương, dời ranh giới chương hoặc thay đổi storyboard (tách, gộp, xóa shot, dời ranh giới shot) thì thuyết minh của các shot bị ảnh hưởng chuyển `OUTDATED` (so sánh hash đoạn nguồn). | M | P2 | ĐX |

### 2.6 M06 — Trình chỉnh sửa & xuất video (EDT) · lõi

> Bước 5–6 của luồng chính. Trình chỉnh sửa **timeline nhiều track**, dựng từ tư liệu của M05. Nhạc nền và SFX được thêm tại đây. Track thuyết minh bị **khóa nội dung** để bảo đảm thuyết minh nguyên văn (BR-19, BR-24). Sơ đồ: `../so-do/04-tuan-tu/seq-chinh-sua-xuat-video.puml`.

#### 2.6.1 Timeline & track

| Mã | Yêu cầu | Ưu tiên | GĐ | Nguồn |
|---|---|---|---|---|
| FR-EDT-01 | Mở trình chỉnh sửa cho một chương hoặc cả dự án (các chương nối tiếp). **Bản nháp timeline** được dựng tự động từ tư liệu: track **Video** (mỗi shot một clip ảnh, thời lượng = audio + đệm 0,3 s / 0,5 s), track **Thuyết minh** (mỗi shot một clip audio, theo thứ tự), track **Phụ đề** (nguyên văn), track **Nhạc nền** và **SFX** để trống; mặc định Ken Burns luân phiên và crossfade 0,5 s. | M | P3 | ĐX |
| FR-EDT-02 | Loại track: Video (ảnh), Phụ đề, Thuyết minh (khóa), Nhạc nền (có thể nhiều track), SFX (có thể nhiều track); Overlay (chữ, logo, hình) sau MVP. Thêm, xóa, đổi tên, ẩn, tắt tiếng track (trừ track Thuyết minh: không xóa được). | M | P3 (một phần ✂10) | ĐX |
| FR-EDT-03 | Thao tác timeline: kéo thả, di chuyển, cắt (split), trim đầu/cuối, nhân bản, xóa clip; chọn nhiều; zoom và cuộn timeline; snap theo playhead và mép clip; thước thời gian; phím tắt; **undo/redo** tối thiểu 100 bước. | M | P3 (một phần ✂10) | ĐX |
| FR-EDT-04 | **Ràng buộc nguyên văn (BR-24):** clip thuyết minh **không** được cắt, trim, xóa, đổi thứ tự hay chồng lên nhau. Chỉ được (a) dời thời điểm bắt đầu để chèn khoảng lặng, (b) chỉnh âm lượng hoặc keyframe âm lượng, (c) **đổi tốc độ 0,8×–1,25×**, giữ cao độ; clip ảnh và phụ đề của shot co giãn theo. Clip ảnh của một shot phải hiển thị **suốt** thời gian đọc đoạn của shot đó; được dài hơn, không được ngắn hơn. | M | P3 | ĐX, QĐ-53 |
| FR-EDT-05 | Clip tiêu đề (tên truyện, tên chương, tác giả) và clip kết (credit) dạng overlay trên nền màu hoặc ảnh; không có thuyết minh (tiêu đề chương không đọc, QĐ-60). | S | Sau | ĐX |

#### 2.6.2 Hình ảnh & chuyển cảnh

| Mã | Yêu cầu | Ưu tiên | GĐ | Nguồn |
|---|---|---|---|---|
| FR-EDT-06 | **Hiệu ứng chuyển động ảnh (Ken Burns):** none, zoom in/out, pan bốn hướng; cường độ; điểm tập trung chọn trên ảnh; nhiều pha cho clip dài. Keyframe vị trí/tỷ lệ (nâng cao): sau MVP. | M | P3 (một phần ✂10) | ĐX |
| FR-EDT-07 | **Chuyển cảnh** giữa hai clip ảnh: cơ bản cut, crossfade; nâng cao fade, fade-to-black/white, slide, wipe, zoom; thời lượng 0–1,5 s; kéo thả từ thư viện chuyển cảnh; áp hàng loạt. Chuyển cảnh không làm thay đổi vị trí clip thuyết minh. | M | P3 (nâng cao ✂2) | ĐX |
| FR-EDT-08 | **Khung hình:** ảnh lệch tỷ lệ video thì crop (theo điểm tập trung), fit (viền màu) hoặc nền mờ; tỷ lệ video 16:9 / 9:16 / 1:1 theo dự án. Preview có công tắc bật/tắt **vùng an toàn và lưới căn chỉnh** (chỉ hiển thị khi chỉnh sửa, không vẽ vào video xuất). | M | P3 | ĐX |
| FR-EDT-09 | **Tinh chỉnh hình ảnh:** độ sáng, tương phản, bão hòa, nhiệt độ màu, bộ lọc màu (preset); áp cho một clip, nhiều clip hoặc toàn video. | C | Sau | ĐX |
| FR-EDT-10 | **Overlay chữ:** nội dung, font (hỗ trợ tiếng Việt), cỡ, màu, viền/bóng, vị trí, hiệu ứng xuất hiện/biến mất; overlay hình (logo). | S | Sau | ĐX |
| FR-EDT-11 | **Phụ đề:** bật/tắt; luôn hiển thị **nguyên văn kể cả ký hiệu trình bày** (BR-22), ngắt dòng theo timestamp (≤ 2 dòng, ≤ 42 ký tự/dòng, theo chuẩn Netflix); kiểu cả câu; font, cỡ, màu, nền, vị trí trong vùng an toàn. **Mẫu preset** dựng sẵn (hằng số trong package TS dùng chung, không lưu DB) để áp một lần rồi tinh chỉnh tiếp; áp preset chỉ sao chép giá trị vào `subtitle_style`. Nội dung phụ đề **không sửa được** trong trình chỉnh sửa, chỉ sửa kiểu. | M | P3 (preset ✂2) | ĐX, QĐ-56 |

#### 2.6.3 Âm thanh: nhạc nền & SFX

| Mã | Yêu cầu | Ưu tiên | GĐ | Nguồn |
|---|---|---|---|---|
| FR-EDT-12 | **Thư viện âm thanh hệ thống:** nạp sẵn bộ nhạc nền và SFX CC0/CC-BY tuyển chọn từ Pixabay/Freesound; tìm theo từ khóa, thể loại, tâm trạng, thời lượng; nghe thử; nhạc CC-BY tự sinh dòng ghi công (BR-26). | S | Sau | ĐX, QĐ-58 |
| FR-EDT-13 | **Nhạc nền:** kéo vào track Nhạc nền; nhiều đoạn nối tiếp; cắt, trim, lặp; fade in/out; âm lượng và keyframe âm lượng; **ducking tự động** dưới thuyết minh (mức giảm dB chỉnh được). | M | P3 | ĐX |
| FR-EDT-14 | **SFX:** kéo vào track SFX tại thời điểm bất kỳ; nhiều SFX chồng nhau trên nhiều track; cắt, trim, fade, âm lượng. | M | P3 | ĐX |
| FR-EDT-15 | **Trộn âm:** âm lượng từng track, tắt tiếng hoặc solo track, đồng hồ mức. Render luôn chuẩn hóa loudness đầu ra (−14 LUFS) và chống clipping theo mặc định, kể cả trong MVP. | S | Sau | ĐX |
| FR-EDT-27 | **Tải nhạc/SFX lên** (MP3/WAV/M4A, ≤ 100 MB, ≤ 15 phút) vào "âm thanh của tôi"; danh sách, tìm theo tên, nghe thử, xóa. Người tải lên tự chịu trách nhiệm bản quyền; không có ô cam kết (BR-26). | M | P3 | QĐ-58 |

> Đã bỏ: FR-EDT-16 (AI sinh nhạc/SFX và gợi ý SFX theo đoạn văn), theo QĐ-57.

#### 2.6.4 Xem trước, lưu & đồng bộ

| Mã | Yêu cầu | Ưu tiên | GĐ | Nguồn |
|---|---|---|---|---|
| FR-EDT-17 | **Xem trước** theo thời gian thực trong trình duyệt (không cần render): play/pause, tua, scrub; hình, thuyết minh, nhạc, SFX, phụ đề đồng bộ. | M | P3 ✂9 | ĐX |
| FR-EDT-18 | **Tự động lưu** (debounce ≤ 2 s) với khóa lạc quan theo version. Lịch sử phiên bản timeline (đặt tên, khôi phục) và xử lý xung đột giữa nhiều người: sau MVP. | M | P3 | ĐX |
| FR-EDT-19 | **Đồng bộ với tư liệu:** khi shot được sinh lại ảnh hoặc thuyết minh, hoặc storyboard thay đổi (tách/gộp shot, dời ranh giới), trình chỉnh sửa cập nhật clip tương ứng và **giữ** các chỉnh sửa của người dùng (hiệu ứng, chuyển cảnh, tốc độ, nhạc, SFX); clip bị ảnh hưởng được đánh dấu để người dùng kiểm tra. | M | P3 | ĐX |
| FR-EDT-20 | Mọi thao tác chỉnh sửa trên timeline miễn phí. | M | P3 | ĐX |

#### 2.6.5 Xuất & tải video

| Mã | Yêu cầu | Ưu tiên | GĐ | Nguồn |
|---|---|---|---|---|
| FR-EDT-21 | Xuất MP4 (H.264 + AAC, 30 fps) theo tỷ lệ dự án: 1920×1080, 1080×1920 hoặc 1080×1080; tùy chọn 720p. Tài khoản Free: chỉ 720p, có **watermark** (các đường kẻ kèm logo), tối đa 3 lần render và 10 phút video mỗi tháng (BR-27). | M | P3 | ĐX, QĐ-36 |
| FR-EDT-22 | **Điều kiện xuất (BR-23):** track Thuyết minh đầy đủ mọi shot, đúng thứ tự, trạng thái `DONE`; không clip nào `OUTDATED`; mọi ảnh `DONE`; **độ phủ văn bản 100%**. Thiếu điều kiện thì liệt kê vị trí chưa đạt trên timeline. Shot "cần sinh lại" chỉ hiện cảnh báo, không chặn. | M | P3 | ĐX, QĐ-55 |
| FR-EDT-23 | Tiến độ xuất theo % qua SSE; có thể hủy. | M | P3 | ĐX |
| FR-EDT-24 | Mỗi lần xuất tạo **phiên bản** render; danh sách Renders theo chương hoặc dự án; đặt bản chính; xóa. | M | P3 | ĐX |
| FR-EDT-25 | **Tải xuống** MP4, phụ đề SRT/VTT và audio thuyết minh (MP3/WAV) qua link ký có thời hạn. | M | P3 | ĐX |
| FR-EDT-26 | Chia video dài theo chương hoặc theo giới hạn thời lượng (vd. ≤ 10 phút), cắt tại ranh giới shot. | S | Sau | ĐX |

### 2.7 M07 — AI Director (DIR) · sau MVP

> Toàn bộ M07 nằm **ngoài MVP** (QĐ-04); chỉ làm nếu MVP xong sớm. Giữ đặc tả để làm hướng phát triển.

| Mã | Yêu cầu | Ưu tiên | GĐ | Nguồn |
|---|---|---|---|---|
| FR-DIR-01 | Panel Director dạng chat; người dùng hỏi hoặc ra lệnh bằng ngôn ngữ tự nhiên ("làm lại shot 3 chương 2", "thêm bóng mờ cho quản lý"). | S | Sau | QS |
| FR-DIR-02 | Director gọi các thao tác hệ thống qua **công cụ có kiểm soát** (tool calling), dùng cùng quyền và cùng bảng giá như người dùng thao tác tay. **Bộ tool không có thao tác ghi vào văn bản chương** (BR-21). Nếu người dùng yêu cầu "tóm tắt" hay "viết lại" truyện, Director từ chối và giải thích nguyên tắc nguyên văn. | S | Sau | ĐX |
| FR-DIR-03 | Lệnh mơ hồ thì hỏi lại ("Chương nào?", "Shot số mấy?"). | S | Sau | QS |
| FR-DIR-04 | Chế độ tự động chạy theo luồng chính: pickStyle → split (chia chương) → cast (thế giới truyện) → pickVoice → media (storyboard tự động + ảnh + thuyết minh) → verify (duyệt thuyết minh) → draftTimeline (dựng bản nháp timeline). Sau đó Director **dừng** để người dùng chỉnh sửa video; xuất video chỉ chạy khi người dùng yêu cầu. | S | Sau | QS (điều chỉnh) |
| FR-DIR-05 | Điểm duyệt bắt buộc: chọn style và duyệt cast trước khi sinh ảnh; **chọn giọng đọc** trước khi sinh thuyết minh; duyệt thuyết minh trước khi dựng timeline (BR-09, BR-23). Trước mỗi bước tốn phí, hiển thị tổng giá ước tính. | S | Sau | QS + ĐX |
| FR-DIR-06 | Pause / Continue / Exit auto; trạng thái kế hoạch lưu bền vững và tiếp tục được sau khi tải lại trang. | S | Sau | QS |
| FR-DIR-07 | Bước nào đã xong thì bỏ qua (vd. chương đã có đủ tư liệu). Khi hoàn tất báo "Mọi chương đã sẵn sàng dựng video". | S | Sau | QS (điều chỉnh) |
| FR-DIR-08 | Director có thể viết nội dung giúp người dùng (prompt ảnh, caption, Visual Rule) và ghi Director note. | S | Sau | QS |
| FR-DIR-09 | Review: Director đánh giá kết quả một bước (vd. shot lệch nhân vật) và đề xuất sửa. | C | Sau | SL |

### 2.8 M08 — Thư viện tài sản cá nhân (LIB) · sau MVP

| Mã | Yêu cầu | Ưu tiên | GĐ | Nguồn |
|---|---|---|---|---|
| FR-LIB-01 | Thư viện gồm 3 tab Characters / Locations / Items, có đếm; tìm kiếm; sắp xếp Recent. | S | Sau | QS |
| FR-LIB-02 | Lọc All / My Created / From Projects. | S | Sau | QS |
| FR-LIB-03 | Tạo nhân vật từ ảnh hoặc mô tả ngoài dự án. | S | Sau | QS |
| FR-LIB-04 | Tài sản tạo trong dự án có tùy chọn "Lưu vào thư viện" để tái sử dụng. | S | Sau | ĐX |
| FR-LIB-05 | Tài sản thư viện khi thêm vào dự án được **sao chép tham chiếu** (dùng chung ảnh gốc), sửa trong dự án không ảnh hưởng thư viện. | S | Sau | ĐX |

### 2.9 M09 — Ví & thanh toán (BIL) · phụ trợ

| Mã | Yêu cầu | Ưu tiên | GĐ | Nguồn |
|---|---|---|---|---|
| FR-BIL-01 | Trang Pricing: cách tính giá (chi phí thực × 110%), đơn giá tham khảo từng thao tác, giới hạn Free và quyền lợi khi đã nạp tiền, tiền dùng thử $2, FAQ. | M | P3 | QS, QĐ-31 |
| FR-BIL-02 | Đăng ký gói tháng/năm qua checkout có host của cổng thanh toán. | S | Sau | QS, QĐ-35 |
| FR-BIL-03 | **Nạp tiền vào ví** (USD, $1–$100 mỗi lần) qua checkout có host của cổng thanh toán ở **chế độ sandbox**. Tiền chỉ vào ví khi webhook xác nhận. | M | P3 ✂6 | QS, QĐ-30 |
| FR-BIL-04 | Manage Billing qua portal của cổng: nâng/hạ gói, đổi thẻ, hóa đơn, hủy gói. | S | Sau | QS |
| FR-BIL-05 | **Ví USD** một số dư cho mỗi người dùng: khả dụng, đang giữ, tổng đã nạp thật; lưu bằng micro-USD; hiển thị USD (tùy chọn quy đổi VND). Trạng thái tài khoản Free / Đã nạp tiền suy từ tổng đã nạp (BR-27). | M | P1 | ĐX, QĐ-30 |
| FR-BIL-06 | Sổ cái ví chỉ ghi thêm (append-only); mỗi bút toán có loại (`TRIAL_GRANT`, `TOPUP`, `HOLD`, `CAPTURE`, `RELEASE`, …), số tiền, job hoặc thanh toán liên quan, dự án, người thực hiện. | M | P1 | ĐX, QĐ-38 |
| FR-BIL-08 | Người dùng xem lịch sử chi tiêu theo dự án và theo loại thao tác, kèm chi phí thực và phí 10%. | S | P3 | ĐX |
| FR-BIL-09 | Webhook thanh toán xử lý idempotent theo event id; xác thực chữ ký. | M | P3 ✂6 | ĐX |
| FR-BIL-10 | **Tiền dùng thử $2** một lần khi tạo hồ sơ, bút toán `TRIAL_GRANT`, không làm tài khoản thành "Đã nạp tiền" (BR-28). | M | P1 | QĐ-37 |
| FR-BIL-11 | **Giữ / trừ / hoàn** cho mọi job AI: giữ giá ước tính tối đa, trừ chi phí thực × 110%, hoàn phần dư; job lỗi hoàn toàn bộ (BR-02). | M | P1 | QĐ-32 |
| FR-BIL-12 | **Giới hạn tài khoản Free:** 1 dự án, 3 chương, 3 lần render/tháng, 10 phút video/tháng, 720p có watermark; vượt giới hạn thì báo rõ và gợi ý nạp tiền (BR-27). | M | P1, P3 ✂7 | QĐ-36 |

> Đã bỏ: FR-BIL-07 (credit miễn phí hằng ngày), thay bằng FR-BIL-10 (QĐ-37).

### 2.10 M10 — Quản trị (ADM) · phụ trợ [ĐX]

| Mã | Yêu cầu | Ưu tiên | GĐ | Nguồn |
|---|---|---|---|---|
| FR-ADM-01 | Cấu hình bảng giá theo loại thao tác (xem [08](08-quy-tac-nghiep-vu.md) §3): công thức, đơn giá provider, giới hạn đầu ra để ước tính; có phiên bản và ngày hiệu lực. MVP nạp bằng file cấu hình (seed); giao diện sau MVP. | M | P1 | ĐX, QĐ-04 |
| FR-ADM-02 | Cấu hình gói (giá, quyền lợi) đồng bộ với cổng thanh toán. | S | Sau | ĐX |
| FR-ADM-03 | Quản lý provider và mô hình AI: bật/tắt, thứ tự ưu tiên, chi phí thực mỗi đơn vị; danh mục style, **danh mục giọng đọc** (kèm audio mẫu). MVP nạp bằng file cấu hình (seed); giao diện và thư viện nhạc & SFX sau MVP. | M | P1 | ĐX, QĐ-04 |
| FR-ADM-04 | Giám sát job: lọc theo trạng thái, provider, người dùng; xem lỗi; chạy lại hoặc hoàn tiền thủ công. | S | Sau | ĐX |
| FR-ADM-05 | Điều chỉnh số dư người dùng (bắt buộc ghi lý do, ghi vào sổ cái). | S | Sau | ĐX |
| FR-ADM-06 | Báo cáo: chi tiêu, chi phí AI theo provider, phí thu, tỷ lệ job lỗi. | S | Sau | ĐX |
| FR-ADM-07 | **Trần chi tiêu AI toàn hệ thống mỗi ngày** (mặc định $10, cấu hình được): vượt trần thì từ chối job tốn phí mới, job đang chạy vẫn xong, gửi email cảnh báo cho Admin (BR-29). | M | P2 | QĐ-39 |

---

## 3. Yêu cầu giao diện ngoài

| Mã | Giao diện | Năng lực cần có |
|---|---|---|
| IF-01 | Web UI | Responsive; Studio tối ưu desktop ≥ 1280px; tablet ≥ 768px chỉ đọc và chỉnh nhẹ |
| IF-02 | LLM | Chat completion, structured output (JSON Schema), tool calling, streaming, context ≥ 128k token; trả số token dùng để tính chi phí thực |
| IF-03 | Image | Text-to-image có ảnh tham chiếu (≥ 3 ảnh), edit theo hướng dẫn bằng lời |
| IF-04 | Forced aligner / STT | Timestamp cấp từ cho audio + văn bản đã biết (tiếng Việt, tiếng Anh) khi TTS không trả timestamp; STT để tính WER (bộ đánh giá ở P0; kiểm chứng từng shot sau MVP) |
| IF-05 | TTS | TTS chất lượng cao tiếng Việt và tiếng Anh, hỗ trợ SSML (alias/phoneme/break), trả timestamp nếu có, đọc **đúng văn bản đầu vào** (không "cải biên"). Ứng viên P0 gồm cả Vbee AIVoice (QĐ-62) |
| IF-09 | Render engine | FFmpeg (zoompan, xfade, subtitles/ASS, sidechaincompress để ducking, rubberband/atempo để đổi tốc độ giữ cao độ) hoặc Remotion; chạy trong hạ tầng của hệ thống |
| IF-06 | Payment | Checkout có host ở chế độ sandbox, webhook có chữ ký; portal sau MVP |
| IF-07 | Object storage | S3-compatible, presigned URL |
| IF-08 | Email | Email giao dịch (cảnh báo trần chi tiêu cho Admin, thông báo xuất video) |
| IF-10 | SSO | OIDC (Keycloak; Vbee nếu hỗ trợ) hoặc OAuth 2.0 + userinfo (Vbee nếu chỉ có OAuth 2.0) |

Lựa chọn nhà cung cấp cụ thể và lớp adapter xem [05](05-kien-truc-he-thong.md) §7.
