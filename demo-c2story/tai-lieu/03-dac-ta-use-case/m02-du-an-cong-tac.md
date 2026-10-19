# M02 — Quản lý dự án & cộng tác

> Sơ đồ: `../../so-do/01-use-case/phan-ra/uc-m02-du-an-cong-tac.puml`, `../../so-do/04-tuan-tu/seq-import-chia-chuong.puml`, `../../so-do/04-tuan-tu/seq-cong-tac-xung-dot.puml`. Yêu cầu: FR-PRJ-01..13. Quyền: [08 §2](../08-quy-tac-nghiep-vu.md).

---

<a id="uc-0201"></a>
## UC-02.01 Xem danh sách dự án

| Mục | Nội dung |
|---|---|
| Tác nhân chính | User |
| Mô tả | Xem các dự án mình sở hữu hoặc tham gia để mở tiếp |
| Tiền điều kiện | Đã đăng nhập |
| Hậu điều kiện | **Thành công:** danh sách hiển thị đúng quyền |
| Kích hoạt | Mở `/projects` |
| Truy vết | FR-PRJ-01 |

**Luồng chính**
1. User mở trang Projects.
2. Hệ thống trả các dự án mà User là Owner hoặc Editor, sắp theo ngày cập nhật: tiêu đề, ảnh đại diện, số chương, style, bước hiện tại của luồng (1–6), trạng thái, vai trò của User.
3. User chọn một dự án; hệ thống mở Studio ở màn hình của bước hiện tại.

**Luồng thay thế / ngoại lệ**
- **2a.** Chưa có dự án nào: hiện trạng thái trống với hai nút "Import truyện" (UC-02.02) và "Tạo dự án trống" (UC-02.03).
- **2b.** Dự án đang chờ xóa (soft delete): không hiển thị.

---

<a id="uc-0202"></a>
## UC-02.02 Import truyện (giữ nguyên văn)

| Mục | Nội dung |
|---|---|
| Tác nhân chính | User (trở thành Owner) |
| Mô tả | Bước 1 của luồng chính: đưa văn bản truyện vào hệ thống để tạo dự án, **giữ nguyên từng chữ** |
| Tiền điều kiện | Đã đăng nhập |
| Hậu điều kiện | **Thành công:** có Project, ProjectMember(OWNER), SourceText (kèm `sha256`), Chapter #1 chứa toàn văn. **Tối thiểu:** không tạo dự án dở dang khi lỗi |
| Kích hoạt | Bấm "Import your story" |
| Quan hệ | include UC-02.02a |
| Truy vết | FR-PRJ-02, FR-PRJ-03; BR-19, BR-21 |

**Luồng chính**
1. User dán văn bản hoặc chọn file (.txt, .md, .docx).
2. Hệ thống thực hiện **UC-02.02a** và hiển thị bản xem trước (số ký tự, số đoạn).
3. User nhập tiêu đề, chọn style và tỷ lệ khung hình video (16:9 / 9:16 / 1:1).
4. Hệ thống tạo trong **một giao dịch**: Project, ProjectMember(OWNER), SourceText, Chapter #1 (`version = 1`).
5. Hệ thống mở Studio ở màn hình Write và gợi ý bước 2 "Chia chương" (UC-03.03).

**Luồng thay thế / ngoại lệ**
- **2a.** File sai định dạng, > 2 MB hoặc > 500.000 ký tự: báo lỗi, giữ nguyên form.
- **2b.** File .docx có định dạng (đậm, nghiêng, bảng): chỉ giữ văn bản, không bỏ chữ nào.
- **4a.** Lỗi DB: rollback, hiện lỗi, giữ nội dung trên form để thử lại.
- Ghi chú: **không** có tùy chọn "AI viết lại" (BR-19, BR-21).

### UC-02.02a Kiểm tra & chuẩn hóa kỹ thuật
<a id="uc-0202a"></a>
- **Loại:** include (bước 2).
- **Các bước:** (1) kiểm tra MIME thật và kích thước; (2) trích văn bản thuần; (3) chuẩn hóa Unicode NFC, thống nhất xuống dòng về `\n`, bỏ ký tự điều khiển vô hình; (4) ghi `normalization_log`; (5) tính `sha256`.
- **Kết quả:** văn bản sạch về kỹ thuật, **không đổi chữ**.

---

<a id="uc-0203"></a>
## UC-02.03 Tạo dự án trống

| Mục | Nội dung |
|---|---|
| Tác nhân chính | User |
| Mô tả | Tạo dự án không có văn bản để viết trực tiếp trong Workspace |
| Tiền điều kiện | Đã đăng nhập; chưa vượt giới hạn số dự án của gói |
| Hậu điều kiện | **Thành công:** Project + ProjectMember(OWNER) + một chương trống |
| Kích hoạt | Bấm "Tạo dự án trống" |
| Truy vết | FR-PRJ-04 |

**Luồng chính**
1. User nhập tiêu đề, chọn style và tỷ lệ khung hình.
2. Hệ thống tạo dự án và Chapter #1 trống.
3. Hệ thống mở Workspace (UC-03.02).

**Luồng thay thế / ngoại lệ**
- **1a.** Gói Free đã có 1 dự án: hiện thông báo giới hạn và gợi ý nâng gói (UC-09.02).

---

<a id="uc-0204"></a>
## UC-02.04 Cài đặt dự án

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Owner |
| Mô tả | Đổi style, mô hình ảnh, ngôn ngữ, thời lượng mục tiêu mỗi ảnh, tỷ lệ khung hình, hiển thị |
| Tiền điều kiện | Là Owner của dự án |
| Hậu điều kiện | **Thành công:** `projects` cập nhật (version tăng); thay đổi áp dụng cho các lần sinh **sau** |
| Kích hoạt | Mở Settings |
| Truy vết | FR-PRJ-07; BR-04 |

**Luồng chính**
1. Owner mở Settings.
2. Owner đổi một thuộc tính.
3. Hệ thống lưu ngay (If-Match) và thông báo "Đã lưu".

**Luồng thay thế / ngoại lệ**
- **2a.** Đổi style khi đã có ảnh: hệ thống hỏi có muốn "Sinh lại tất cả ảnh tham chiếu" (UC-04.03a) và hiện giá; ảnh shot cũ giữ nguyên cho đến khi sinh lại.
- **2b.** Đổi tỷ lệ khung hình khi đã có timeline: cảnh báo ảnh sẽ được crop/fit theo khung mới (UC-06.06).
- **3a.** Xung đột version: tải lại cài đặt mới nhất, yêu cầu chọn lại.
- **\*a.** Editor mở Settings: chỉ xem, không sửa được.

---

<a id="uc-0205"></a>
## UC-02.05 Xóa dự án

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Owner |
| Mô tả | Xóa dự án và toàn bộ dữ liệu liên quan |
| Tiền điều kiện | Là Owner; không có job đang chạy (hoặc chấp nhận hủy) |
| Hậu điều kiện | **Thành công:** dự án soft delete, mọi thành viên mất quyền ngay; xóa cứng cùng media sau 30 ngày. **Tối thiểu:** không xóa khi chưa xác nhận |
| Kích hoạt | Chọn "Xóa" ở danh sách dự án hoặc Settings |
| Truy vết | FR-PRJ-01; BR-04; 04 §5 |

**Luồng chính**
1. Owner chọn "Xóa dự án".
2. Hệ thống hiện hệ quả (số chương, tư liệu, bản xuất, thành viên bị ảnh hưởng).
3. Owner nhập tên dự án để xác nhận.
4. Hệ thống hủy các job `QUEUED` (hoàn credit), đặt `deleted_at`, thông báo cho thành viên.

**Luồng thay thế / ngoại lệ**
- **2a.** Có job đang `RUNNING`: chờ job kết thúc rồi mới xóa, hoặc Owner chọn "Hủy và xóa".
- **\*a.** Owner muốn khôi phục trong 30 ngày: liên hệ hỗ trợ hoặc dùng mục "Dự án đã xóa" [ĐX].

---

<a id="uc-0206"></a>
## UC-02.06 Tạo / thu hồi link mời

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Owner |
| Mô tả | Tạo link để người khác tham gia làm Editor, hoặc thu hồi link |
| Tiền điều kiện | Là Owner; số thành viên chưa vượt giới hạn gói |
| Hậu điều kiện | **Thành công:** có InviteLink hiệu lực (DB chỉ lưu SHA-256 token), hoặc link bị thu hồi |
| Kích hoạt | Bấm "Share" |
| Truy vết | FR-PRJ-08; NFR-SEC-04 |

**Luồng chính**
1. Owner bấm "Share".
2. Hệ thống tạo (hoặc lấy) link với token ngẫu nhiên 256-bit, hiển thị URL và nút sao chép.
3. Owner sao chép link và gửi cho người cần mời.

**Luồng thay thế / ngoại lệ**
- **2a.** Owner chọn "Thu hồi link": link cũ vô hiệu ngay; thành viên hiện có không bị ảnh hưởng; Owner có thể tạo link mới.
- **2b.** Đã đạt giới hạn thành viên của gói: hiện thông báo và gợi ý nâng gói.

---

<a id="uc-0207"></a>
## UC-02.07 Quản lý thành viên

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Owner |
| Mô tả | Xem danh sách cộng tác viên và xóa thành viên |
| Tiền điều kiện | Là Owner |
| Hậu điều kiện | **Thành công:** thành viên bị xóa mất quyền ở lần gọi API kế tiếp (`403`) |
| Kích hoạt | Mở "Collaborators" |
| Truy vết | FR-PRJ-09; BR-17 |

**Luồng chính**
1. Owner mở danh sách thành viên (tên, email, vai trò, ngày tham gia, lần sửa cuối).
2. Owner chọn "Xóa" một Editor và xác nhận.
3. Hệ thống xóa ProjectMember, phát sự kiện `member.changed`, gửi email thông báo.

**Luồng thay thế / ngoại lệ**
- **2a.** Editor bị xóa đang có job chạy: job hoàn tất, credit tính cho Editor đó, nhưng người đó không xem được kết quả (BR-17).
- **2b.** Owner không thể tự xóa chính mình; muốn rời thì phải xóa dự án.

---

<a id="uc-0208"></a>
## UC-02.08 Tham gia dự án qua link

| Mục | Nội dung |
|---|---|
| Tác nhân chính | User |
| Mô tả | Người được mời mở link để trở thành Editor của dự án |
| Tiền điều kiện | Có link mời |
| Hậu điều kiện | **Thành công:** ProjectMember(EDITOR) được tạo; người dùng vào Studio |
| Kích hoạt | Mở `/invite/{token}` |
| Truy vết | FR-PRJ-08, FR-AUTH-03 |

**Luồng chính**
1. User mở link mời.
2. Nếu chưa đăng nhập, thực hiện UC-01.01 rồi quay lại link (UC-01.01c).
3. Hệ thống tìm link theo SHA-256 của token, kiểm tra còn hiệu lực.
4. Hệ thống hiện tên dự án, Owner, vai trò Editor; User bấm "Tham gia".
5. Hệ thống tạo ProjectMember(EDITOR), ghi nhật ký, mở Studio.

**Luồng thay thế / ngoại lệ**
- **3a.** Link bị thu hồi hoặc hết hạn: `410 Gone`, hiện "Link không còn hiệu lực".
- **3b.** User đã là thành viên: mở thẳng Studio.

---

<a id="uc-0209"></a>
## UC-02.09 Xem bản đồ quy trình (Map)

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Editor |
| Mô tả | Xem 6 bước của luồng chính và vị trí hiện tại của dự án |
| Tiền điều kiện | Là thành viên dự án |
| Hậu điều kiện | **Thành công:** hiển thị tiến độ từng bước; điều hướng tới bước được chọn |
| Kích hoạt | Mở `?v=map` |
| Truy vết | FR-PRJ-06 |

**Luồng chính**
1. Editor mở Map.
2. Hệ thống tính trạng thái 6 bước: (1) đã nhập truyện; (2) số chương; (3) số tài sản có ảnh tham chiếu; (4) số chương "Sẵn sàng dựng"; (5) số timeline đã chỉnh; (6) số bản xuất.
3. Hệ thống làm nổi bật bước kế tiếp nên làm.
4. Editor bấm một bước; hệ thống mở màn hình tương ứng.

---

<a id="uc-0210"></a>
## UC-02.10 Xử lý xung đột khi lưu

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Editor |
| Mô tả | Hai người cùng sửa một đối tượng (chương, shot, timeline); người lưu sau chọn cách xử lý, không mất dữ liệu |
| Tiền điều kiện | Editor A và B cùng mở đối tượng ở `version = n` |
| Hậu điều kiện | **Thành công:** không có ghi đè ngầm; dữ liệu của cả hai được giữ. **Tối thiểu:** bản của người lưu sau không bị mất |
| Kích hoạt | API trả `409 VERSION_CONFLICT` khi lưu |
| Quan hệ | được mở rộng bởi UC-02.10a, UC-02.10b; được mở rộng từ UC-03.04..08 |
| Truy vết | FR-PRJ-11, FR-EDT-18; BR-05 |

**Luồng chính**
1. B lưu đối tượng với `If-Match: n`. Hệ thống ghi, tăng `version = n+1`, phát sự kiện realtime.
2. Giao diện của A hiện nhãn "B vừa sửa".
3. A lưu với `If-Match: n`; hệ thống trả `409` kèm bản hiện tại và tên người sửa cuối.
4. Giao diện của A hiện hộp thoại với hai lựa chọn UC-02.10a và UC-02.10b.

### UC-02.10a Lưu bản của tôi thành nháp
<a id="uc-0210a"></a>
- **Loại:** extend (bước 4).
- **Các bước:** hệ thống tạo Archive nguồn `CONFLICT` tên "Conflict draft — <đối tượng> — <thời gian>" chứa bản của A; với timeline thì tạo `timeline_versions` có tên. Sau đó tải bản `n+1`.
- **Kết quả:** bản của A được lưu an toàn; A làm việc tiếp trên bản mới nhất.

### UC-02.10b Tải bản của người khác
<a id="uc-0210b"></a>
- **Loại:** extend (bước 4).
- **Các bước:** A xác nhận bỏ thay đổi chưa lưu; hệ thống nạp bản `n+1`.
- **Kết quả:** A làm việc trên bản mới nhất; thay đổi chưa lưu của A bị bỏ theo lựa chọn của A.

---

<a id="uc-0211"></a>
## UC-02.11 Nhân bản dự án

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Owner |
| Mô tả | Tạo bản sao dự án để thử hướng khác |
| Tiền điều kiện | Là Owner; chưa vượt giới hạn số dự án |
| Hậu điều kiện | **Thành công:** dự án mới (User là Owner) có cùng văn bản, chương, Story Assets (dùng chung ảnh gốc), storyboard, ảnh và thuyết minh; **không** sao chép timeline đã chỉnh, bản xuất và thành viên |
| Kích hoạt | Chọn "Duplicate" |
| Truy vết | FR-PRJ-13 (C) |

**Luồng chính**
1. Owner chọn "Nhân bản" và đặt tên mới.
2. Hệ thống tạo job sao chép (miễn phí): sao chép bản ghi, tham chiếu lại media (không nhân đôi file).
3. Khi xong, hệ thống mở dự án mới.

**Luồng thay thế / ngoại lệ**
- **2a.** Dự án nguồn có job đang chạy: chụp trạng thái tại thời điểm bắt đầu nhân bản.
