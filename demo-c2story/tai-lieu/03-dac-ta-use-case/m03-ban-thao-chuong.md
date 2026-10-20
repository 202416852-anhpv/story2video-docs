# M03 — Bản thảo & chương

> Bước 2 của luồng chính. Sơ đồ: `../../so-do/01-use-case/phan-ra/uc-m03-ban-thao-chuong.puml`, `../../so-do/04-tuan-tu/seq-import-chia-chuong.puml`, `seq-doi-ranh-gioi-shot.puml`, `seq-quan-ly-du-an.puml` (xem văn bản gốc). Yêu cầu: FR-MAN-01..11. Văn bản truyện **chỉ do tác giả sửa** (BR-21).

---

<a id="uc-0301"></a>
## UC-03.01 Xem văn bản gốc

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Editor |
| Mô tả | Xem toàn văn đã import, kèm số ký tự, số chương và ranh giới chương hiện tại |
| Tiền điều kiện | Dự án có SourceText |
| Hậu điều kiện | **Thành công:** hiển thị văn bản và các điểm chia |
| Kích hoạt | Mở `?v=source` |
| Quan hệ | được mở rộng bởi UC-03.01a, UC-03.01b |
| Truy vết | FR-MAN-01; seq-quan-ly-du-an, act-m03-ban-thao-chuong |
| Giai đoạn | P1 |

**Luồng chính**
1. Editor mở màn hình Write.
2. Hệ thống hiển thị toàn văn ghép từ các chương theo thứ tự, đánh dấu ranh giới chương; mỗi khoảng giữa hai đoạn có nút "Split here".
3. Editor đọc, có thể chuyển sang UC-03.03, UC-03.04.

### UC-03.01a Sao chép toàn văn
<a id="uc-0301a"></a>

| Mục | Nội dung |
|---|---|
| Loại | extend của UC-03.01 |
| Tác nhân | Editor |
| Mô tả | Sao chép toàn bộ văn bản truyện vào clipboard |
| Tiền điều kiện | Dự án có văn bản; đang ở màn hình Write (`?v=source`) |
| Hậu điều kiện | **Thành công:** clipboard chứa toàn văn. **Tối thiểu:** không thay đổi dữ liệu dự án |
| Kích hoạt | Bấm "Copy text" ở UC-03.01 bước 3 |
| Truy vết | FR-MAN-01; API 2.3 `GET /projects/{pid}/source`; seq-quan-ly-du-an |
| Giai đoạn | P2 |

**Luồng chính**
1. Editor bấm "Copy text".
2. Hệ thống ghép tiêu đề và nội dung từng chương theo `order_index`, mỗi chương cách nhau một dòng trống [ĐX].
3. Hệ thống ghi chuỗi vào clipboard của trình duyệt.
4. Giao diện báo "Đã sao chép N ký tự".

**Luồng thay thế / ngoại lệ**
- **3a.** Trình duyệt chặn quyền clipboard: hiện hộp văn bản đã chọn sẵn toàn bộ để Editor tự sao chép.
- **2a.** Dữ liệu chương chưa tải đủ ở client: tải từ `GET /source` rồi mới ghép.

### UC-03.01b Nhập lại (Re-import)
<a id="uc-0301b"></a>

| Mục | Nội dung |
|---|---|
| Loại | extend của UC-03.01 |
| Tác nhân | Editor |
| Mô tả | Thay toàn bộ văn bản truyện bằng một bản mới; bản cũ vẫn còn trong Archive nếu Editor lưu |
| Tiền điều kiện | Dự án có văn bản; không chương nào đang bị khóa bởi job (BR-12) |
| Hậu điều kiện | **Thành công:** dự án có SourceText mới và đúng một Chapter #1 chứa toàn văn mới; tư liệu và timeline của các chương cũ chuyển `OUTDATED`. **Tối thiểu:** lỗi thì rollback, văn bản cũ giữ nguyên |
| Kích hoạt | Bấm "Re-import" ở UC-03.01 |
| Truy vết | FR-PRJ-02, FR-PRJ-03; BR-06, BR-12, BR-19, BR-21; API 2.3 `PUT /projects/{pid}/source`; seq-import-chia-chuong |
| Giai đoạn | P2 |

**Luồng chính**
1. Editor chọn "Re-import". Hệ thống cảnh báo hậu quả (mọi storyboard, ảnh, thuyết minh và timeline của các chương hiện có sẽ `OUTDATED`) và gợi ý lưu Archive trước (UC-03.11).
2. Editor dán văn bản hoặc tải file mới (.txt, .md, .docx).
3. Hệ thống thực hiện **UC-02.02a** và hiển thị bản xem trước (số ký tự, số đoạn).
4. Editor xác nhận đã hiểu hậu quả.
5. Trong **một giao dịch**, hệ thống tạo SourceText mới, thay các chương hiện có bằng một Chapter #1 chứa toàn văn mới, cập nhật `projects.current_source_id`.
6. Hệ thống đánh dấu mọi tư liệu và timeline của các chương cũ là `OUTDATED`, phát `chapters.restructured`.
7. Hệ thống mở màn hình Write và gợi ý bước "Chia chương" (UC-03.03).

**Luồng thay thế / ngoại lệ**
- **1a.** Có chương đang bị khóa bởi job: `423 RESOURCE_LOCKED`, nêu job đang chạy.
- **3a.** File không đạt UC-02.02a: báo lỗi, giữ nguyên văn bản hiện tại.
- **5a.** Dự án đã thay đổi (phiên bản khác) trong lúc Editor xem trước: `409`, yêu cầu tải lại rồi làm lại [ĐX].
- **5b.** Lỗi ghi dữ liệu: rollback toàn bộ, giữ nội dung đã nhập trên form.

---

<a id="uc-0302"></a>
## UC-03.02 Soạn thảo trong Workspace

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Editor |
| Mô tả | Viết và sửa văn bản mọi chương trong một trình soạn thảo cuộn liền mạch |
| Tiền điều kiện | Là thành viên dự án; chương không bị khóa |
| Hậu điều kiện | **Thành công:** chương được lưu với version mới; `chapter_versions` có snapshot; thuyết minh của shot có đoạn nguồn bị đổi chuyển `OUTDATED` (BR-06) |
| Kích hoạt | Mở `?v=workspace` và gõ |
| Quan hệ | được mở rộng bởi UC-03.02a, UC-03.04, UC-03.05, UC-03.06 |
| Truy vết | FR-MAN-02, 11; FR-NAR-09; BR-05, BR-06, BR-21; seq-doi-ranh-gioi-shot, act-m03-ban-thao-chuong |
| Giai đoạn | P1 |

**Luồng chính**
1. Editor mở Workspace; hệ thống tải mọi chương kèm ETag. Chương đã có storyboard hiện hành hiển thị **vạch ranh giới shot** mảnh giữa các câu, kèm số shot (`GET …/shot-boundaries`).
2. Editor sửa văn bản hoặc tiêu đề một chương.
3. Hệ thống tự lưu sau 2 s không gõ (`PATCH` + If-Match).
4. Hệ thống tăng version, lưu snapshot, cập nhật "người sửa cuối", phát `chapter.updated`.
5. Nếu chương đã có tư liệu, hệ thống so hash đoạn nguồn từng shot và đánh dấu shot `OUTDATED`.

**Luồng thay thế / ngoại lệ**
- **3a.** `409`: chuyển sang UC-02.10.
- **3b.** Chương đang bị khóa bởi job: `423`, editor ở chế độ chỉ đọc, hiện "Chương đang được xử lý".
- **5a.** Thay đổi làm đoạn nguồn của nhiều shot lệch: hiện banner "N shot cần sinh lại thuyết minh" với nút đi tới UC-05.07c.
- **\*a.** Editor muốn dời vạch ranh giới shot: UC-03.02a.

### UC-03.02a Dời ranh giới shot
<a id="uc-0302a"></a>

| Mục | Nội dung |
|---|---|
| Loại | extend của UC-03.02; include UC-05.01a, UC-05.06e |
| Tác nhân | Editor / LLM |
| Mô tả | Kéo vạch ranh giới giữa hai shot liền kề ngay trên văn bản chương trong Workspace, theo từng câu; sau đó AI viết lại brief của 2 shot bị ảnh hưởng để ảnh khớp đoạn văn mới |
| Tiền điều kiện | Chương có storyboard hiện hành; không bị khóa (BR-12); đủ số dư cho giá ước tính |
| Hậu điều kiện | **Thành công:** hai shot đổi đoạn nguồn, phủ kín vẫn 100% (IC-08); brief của hai shot được viết lại; thuyết minh của hai shot `OUTDATED`; ảnh hiện tại được đánh dấu "brief đã đổi". **Tối thiểu:** Editor hủy hoặc lỗi trước khi dời thì ranh giới và tiền không đổi |
| Kích hoạt | Kéo vạch ranh giới shot sang câu khác trong Workspace |
| Truy vết | FR-BOK-01b, FR-NAR-09; BR-01, BR-06, BR-20, BR-33; IC-08, IC-09; 08 §3.2 (`REWRITE_SHOT`); API 2.5 `POST …/storyboards/{did}:move-boundary`, 06 §4.7; seq-doi-ranh-gioi-shot |
| Giai đoạn | P2 ✂8 |

**Luồng chính**
1. Editor kéo vạch giữa shot trái và shot phải; vạch chỉ dừng ở ranh giới câu.
2. Khi thả, client gọi `:move-boundary?dryRun=true {leftShotId, rightShotId, deltaSentences}`.
3. Hệ thống hiện hộp xác nhận: câu nào chuyển sang shot nào, thời lượng đọc ước tính mới của hai shot, giá ước tính viết lại 2 brief (BR-01).
4. Editor bấm "Dời và viết lại brief".
5. Trong một giao dịch, hệ thống cập nhật `source_start`, `source_end` của hai shot, thực hiện **UC-05.01a**, giữ tiền (UC-05.17) và tạo 2 job `REWRITE_SHOT` (UC-05.06e, ghi chú "đoạn nguồn đã đổi").
6. Thuyết minh của hai shot chuyển `OUTDATED` (IC-09); hệ thống phát `shot.updated` và đồng bộ timeline (UC-06.15).
7. Khi job xong, brief mới được lưu; hệ thống gợi ý sinh lại ảnh và thuyết minh cho hai shot (UC-05.07c) kèm giá.

**Luồng thay thế / ngoại lệ**
- **1a.** Kéo làm một shot không còn câu nào: vạch bật về vị trí cũ, hiện "Mỗi shot cần ít nhất một câu".
- **1b.** Kéo vượt qua vạch kế bên: chặn; chỉ dời giữa hai shot liền kề.
- **3a.** Đoạn nguồn mới của một shot đọc quá 30 giây (khoảng 450 ký tự tiếng Việt): cảnh báo, vẫn cho phép.
- **4a.** Editor bấm "Hủy": vạch bật về vị trí cũ, không thay đổi gì (BR-33).
- **5a.** Không đủ số dư: `402`; vạch bật về, gợi ý nạp tiền (UC-09.03).
- **5b.** Chạm trần chi tiêu ngày: `503 DAILY_BUDGET_EXCEEDED`; không dời (BR-29).
- **5c.** `409` (chương hoặc shot vừa đổi ở tab khác): tải lại vạch ranh giới (BR-05).
- **5d.** Chương đang bị khóa: `423 RESOURCE_LOCKED`.
- **7a.** Job viết lại brief lỗi: ranh giới đã dời vẫn giữ, brief cũ giữ nguyên, tiền giữ được hoàn; shot có nút "Viết lại brief" (UC-05.06e).

---

<a id="uc-0303"></a>
## UC-03.03 Gợi ý chia chương bằng AI

| Mục | Nội dung |
|---|---|
| Tác nhân chính / phụ | Editor / LLM |
| Mô tả | AI đề xuất vị trí chia chương và tiêu đề; Editor duyệt rồi áp dụng |
| Tiền điều kiện | Dự án có văn bản |
| Hậu điều kiện | **Thành công:** danh sách chương mới được ghi nguyên tử qua UC-03.09. **Tối thiểu:** văn bản không đổi |
| Kích hoạt | Bấm "Suggest chapter splits" |
| Quan hệ | include UC-03.09 |
| Truy vết | FR-MAN-04; BR-01, BR-21, BR-27; 08 §3.2 (`SUGGEST_SPLITS`); seq-import-chia-chuong, act-m03-ban-thao-chuong |
| Giai đoạn | P1 |

**Luồng chính**
1. Editor bấm "Suggest chapter splits".
2. Hệ thống hiện giá ước tính; Editor xác nhận; hệ thống giữ tiền (UC-05.17) và tạo job `SUGGEST_SPLITS`. LLM nhận văn bản đã đánh số đoạn, trả `[{startParagraph, title}]`. LLM **không** trả lại văn bản.
3. Hệ thống đánh dấu các điểm chia đề xuất trên màn hình Write.
4. Editor bỏ chọn điểm không muốn, sửa tiêu đề đề xuất.
5. Editor bấm "Áp dụng"; hệ thống thực hiện **UC-03.09**.

**Luồng thay thế / ngoại lệ**
- **2a.** Cách chia hiện tại đã khớp: báo "Your current chapters already match".
- **2b.** LLM lỗi hoặc trả sai schema sau 2 lần thử: báo lỗi, gợi ý chia thủ công (UC-03.04).
- **5a.** Các chương bị ảnh hưởng đã có tư liệu hoặc timeline: hiện cảnh báo trước khi áp dụng (xem UC-03.09).
- **5b.** Tài khoản Free và cách chia cho ra quá 3 chương: chỉ áp được tối đa 3 chương, hiện thông báo giới hạn và gợi ý nạp tiền (BR-27).

---

<a id="uc-0304"></a>
## UC-03.04 Chia chương tại vị trí

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Editor |
| Mô tả | Chia một chương thành hai tại vị trí giữa hai đoạn văn |
| Tiền điều kiện | Chương có ít nhất 2 đoạn |
| Hậu điều kiện | **Thành công:** hai chương liền nhau, nối lại bằng đúng chương cũ |
| Kích hoạt | Bấm "Split here" hoặc đặt con trỏ rồi chọn "Chia tại đây" |
| Quan hệ | extend UC-03.02; include UC-03.09 |
| Truy vết | FR-MAN-03; BR-27; seq-import-chia-chuong, act-m03-ban-thao-chuong |
| Giai đoạn | P1 |

**Luồng chính**
1. Editor chọn vị trí giữa hai đoạn.
2. Editor nhập tiêu đề cho chương mới (mặc định "Chương N+1").
3. Hệ thống thực hiện UC-03.09 với thao tác `SPLIT`.

**Luồng thay thế / ngoại lệ**
- **1a.** Vị trí ở giữa một đoạn: hệ thống dời về ranh giới đoạn gần nhất và hỏi xác nhận.
- **3a.** Tài khoản Free đã có 3 chương: `403 FREE_LIMIT_REACHED`, gợi ý nạp tiền (BR-27).

---

<a id="uc-0305"></a>
## UC-03.05 Gộp chương vào chương trước

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Editor |
| Mô tả | Nối chương k vào cuối chương k−1 |
| Tiền điều kiện | k > 1 |
| Hậu điều kiện | **Thành công:** chương k−1 chứa văn bản của cả hai; chương k bị xóa |
| Kích hoạt | "Merge into previous" trên chương k |
| Quan hệ | extend UC-03.02; include UC-03.09 |
| Truy vết | FR-MAN-05; seq-import-chia-chuong, act-m03-ban-thao-chuong |
| Giai đoạn | P1 |

**Luồng chính**
1. Editor chọn "Gộp vào chương trước" và xác nhận.
2. Hệ thống thực hiện UC-03.09 với thao tác `MERGE_INTO_PREVIOUS`.

**Luồng thay thế / ngoại lệ**
- **1a.** k là chương đầu: thao tác bị vô hiệu.

---

<a id="uc-0306"></a>
## UC-03.06 Dời ranh giới chương

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Editor |
| Mô tả | Dời điểm bắt đầu của chương lên hoặc xuống từng đoạn văn |
| Tiền điều kiện | Có ít nhất 2 chương |
| Hậu điều kiện | **Thành công:** hai chương liền kề thay đổi độ dài, tổng văn bản không đổi |
| Kích hoạt | "Move where this chapter begins" ◀ ▶ |
| Quan hệ | extend UC-03.02; include UC-03.09 |
| Truy vết | FR-MAN-05; seq-import-chia-chuong, act-m03-ban-thao-chuong |
| Giai đoạn | P1 |

**Luồng chính**
1. Editor bấm ◀ (đưa đoạn cuối chương trước sang) hoặc ▶ (đưa đoạn đầu chương này sang chương trước).
2. Hệ thống thực hiện UC-03.09 với thao tác `MOVE_BOUNDARY`.

**Luồng thay thế / ngoại lệ**
- **1a.** Thao tác làm một chương rỗng: bị chặn, gợi ý dùng gộp chương.

---

<a id="uc-0307"></a>
## UC-03.07 Thêm / xóa / đổi tên chương

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Editor |
| Mô tả | Thêm chương trống (cuối hoặc chèn giữa), xóa chương, đổi tiêu đề |
| Tiền điều kiện | Là thành viên dự án |
| Hậu điều kiện | **Thành công:** danh sách chương cập nhật; `order_index` liên tục |
| Kích hoạt | "Add chapter", "Delete chapter", sửa tiêu đề |
| Truy vết | FR-MAN-05; seq-import-chia-chuong, act-m03-ban-thao-chuong |
| Giai đoạn | P1 |

**Luồng chính**
1. Editor chọn thao tác.
2. *Thêm:* hệ thống tạo chương trống tại vị trí chọn. *Đổi tên:* lưu tiêu đề (If-Match). *Xóa:* hệ thống hiện hệ quả (văn bản, tư liệu, clip timeline bị xóa theo) và yêu cầu xác nhận.
3. Hệ thống ghi, phát sự kiện realtime.

**Luồng thay thế / ngoại lệ**
- **2a.** Xóa chương: có nút "Hoàn tác" trong 10 s (NFR-USA-03); văn bản luôn có trong `chapter_versions`.
- **2b.** Xóa chương duy nhất của dự án: bị chặn.
- **2c.** Thêm chương khi tài khoản Free đã có 3 chương: `403 FREE_LIMIT_REACHED` (BR-27).

---

<a id="uc-0308"></a>
## UC-03.08 Sắp xếp lại chương

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Editor |
| Mô tả | Đổi thứ tự chương bằng kéo thả hoặc chọn vị trí |
| Tiền điều kiện | Có ≥ 2 chương |
| Hậu điều kiện | **Thành công:** thứ tự mới được ghi nguyên tử; timeline cấp dự án đổi thứ tự khối chương tương ứng |
| Kích hoạt | Kéo thả ở thanh bên |
| Quan hệ | include UC-03.09 |
| Truy vết | FR-MAN-05; seq-import-chia-chuong, act-m03-ban-thao-chuong |
| Giai đoạn | P1 |

**Luồng chính**
1. Editor kéo chương tới vị trí mới.
2. Hệ thống thực hiện UC-03.09 với thao tác `REORDER`.

---

<a id="uc-0309"></a>
## UC-03.09 Tái cấu trúc nguyên tử

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Hệ thống (được gọi từ UC-03.03..08) |
| Mức | Chức năng con |
| Mô tả | Áp một hoặc nhiều thao tác chia, gộp, dời ranh giới, sắp xếp trong **một giao dịch** |
| Tiền điều kiện | Có danh sách thao tác kèm `ifMatch` từng chương |
| Hậu điều kiện | **Thành công:** danh sách chương mới ghi trọn vẹn; tư liệu của shot bị ảnh hưởng chuyển `OUTDATED`. **Tối thiểu:** lỗi bất kỳ thì rollback toàn bộ, không đổi gì |
| Kích hoạt | `POST /chapters:restructure` |
| Truy vết | FR-MAN-06; IC-02; BR-05, BR-06, BR-12; seq-import-chia-chuong, act-m03-ban-thao-chuong |
| Giai đoạn | P1 |

**Luồng chính**
1. Hệ thống mở giao dịch, `SELECT … FOR UPDATE` các chương liên quan.
2. Kiểm tra version từng chương và chương không bị khóa.
3. Áp thao tác; cập nhật `order_index` (unique deferrable); tăng version.
4. Với các chương đã có storyboard: tính lại tập shot bị ảnh hưởng, đánh dấu thuyết minh `OUTDATED`, đánh dấu clip timeline cần cập nhật.
5. Commit; phát `chapters.restructured`.

**Luồng thay thế / ngoại lệ**
- **2a.** Sai version: rollback, `409` → UC-02.10.
- **2b.** Chương bị khóa: rollback, `423`.
- **3a.** Bất biến "nối các chương = văn bản cũ" bị vi phạm (lỗi lập trình): rollback, `500`, cảnh báo P1.

---

<a id="uc-0310"></a>
## UC-03.10 Tìm & thay thế

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Editor |
| Mô tả | Tìm và thay chuỗi trong tiêu đề và nội dung mọi chương |
| Tiền điều kiện | Có ít nhất một chương không bị khóa |
| Hậu điều kiện | **Thành công:** các chương có thay đổi được lưu với version mới; shot bị ảnh hưởng `OUTDATED` |
| Kích hoạt | Mở "Find & replace" |
| Quan hệ | include UC-03.10a |
| Truy vết | FR-MAN-07; BR-21 |
| Giai đoạn | Sau |

**Luồng chính**
1. Editor nhập chuỗi tìm và chuỗi thay (khớp chính xác, phân biệt hoa thường).
2. Hệ thống thực hiện **UC-03.10a**.
3. Editor bỏ chọn kết quả không muốn thay và bấm "Thay".
4. Hệ thống ghi mọi chương có thay đổi trong một giao dịch.

**Luồng thay thế / ngoại lệ**
- **2a.** Không có kết quả: báo "No matches in editable chapters".
- **4a.** Một chương bị sửa bởi người khác trong lúc đó: rollback, yêu cầu tìm lại.

### UC-03.10a Xem trước số kết quả
<a id="uc-0310a"></a>

| Mục | Nội dung |
|---|---|
| Loại | include của UC-03.10 (bước 2) |
| Tác nhân | Hệ thống |
| Mô tả | Đếm và liệt kê các kết quả khớp của "Tìm & thay thế" mà **chưa thay đổi dữ liệu** |
| Tiền điều kiện | Editor đã nhập chuỗi tìm (không rỗng) |
| Hậu điều kiện | **Thành công:** danh sách kết quả theo chương, mỗi kết quả kèm ngữ cảnh. **Tối thiểu:** dữ liệu không đổi |
| Kích hoạt | UC-03.10 bước 2 (mỗi lần Editor đổi chuỗi tìm) |
| Truy vết | FR-MAN-07; BR-12, BR-21; API 2.3 `POST /projects/{pid}:find-replace` với `dryRun: true` |
| Giai đoạn | Sau |

**Luồng chính**
1. Hệ thống gọi `POST :find-replace {find, replace, dryRun: true}`. Khớp chính xác, phân biệt hoa thường.
2. Hệ thống duyệt tiêu đề và nội dung của mọi chương **không bị khóa**; chương đang bị khóa (BR-12) được bỏ qua và liệt kê riêng.
3. Hệ thống trả tổng số kết quả, số kết quả theo chương, và với mỗi kết quả: vị trí và đoạn trích ngữ cảnh quanh vị trí đó.
4. Giao diện hiển thị danh sách có hộp chọn cho từng kết quả (mặc định chọn hết) để UC-03.10 bước 3 dùng.

**Luồng thay thế / ngoại lệ**
- **1a.** Chuỗi tìm rỗng: `400 VALIDATION_ERROR`, không tìm.
- **3a.** Không có kết quả: báo "No matches in editable chapters" (UC-03.10 nhánh 2a).
- **3b.** Rất nhiều kết quả: trả theo trang (cursor), tổng số vẫn hiển thị đầy đủ.

---

<a id="uc-0311"></a>
## UC-03.11 Lưu Archive

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Editor |
| Mô tả | Lưu ảnh chụp chỉ đọc của toàn bộ bản thảo trước khi thay đổi lớn |
| Tiền điều kiện | Dự án có văn bản |
| Hậu điều kiện | **Thành công:** có Archive bất biến (BR-10) |
| Kích hoạt | "Save archive" ở Archives hoặc Workspace |
| Truy vết | FR-MAN-08 |
| Giai đoạn | Sau |

**Luồng chính**
1. Editor nhập tên archive.
2. Hệ thống ghép toàn văn (có tiêu đề chương), lưu Archive (`source = MANUAL`), hiển thị trong danh sách.

---

<a id="uc-0312"></a>
## UC-03.12 Xem / sao chép / xóa Archive

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Editor |
| Mô tả | Đọc lại archive, sao chép văn bản về Workspace, hoặc xóa archive |
| Tiền điều kiện | Có ít nhất một archive |
| Hậu điều kiện | **Thành công:** archive được hiển thị, sao chép hoặc xóa; archive không bao giờ bị sửa |
| Kích hoạt | Mở Archives |
| Truy vết | FR-MAN-08; BR-10 |
| Giai đoạn | Sau |

**Luồng chính**
1. Editor chọn một archive; hệ thống hiển thị nội dung chỉ đọc.
2. Editor chọn "Copy this archive's full text" để dán vào Workspace, hoặc "Xóa" (xác nhận).

---

<a id="uc-0313"></a>
## UC-03.13 Quản lý ghi chú (Notes)

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Editor |
| Mô tả | Viết ghi chú cấp dự án; xem ghi chú của Director |
| Tiền điều kiện | Là thành viên dự án |
| Hậu điều kiện | **Thành công:** ghi chú được lưu và đồng bộ cho thành viên khác |
| Kích hoạt | Mở panel Notes |
| Quan hệ | được mở rộng bởi UC-03.13a |
| Truy vết | FR-MAN-09 |
| Giai đoạn | Sau |

**Luồng chính**
1. Editor mở panel Notes; hệ thống hiển thị ghi chú theo thời gian (của người dùng và "Director note").
2. Editor thêm, sửa hoặc xóa ghi chú của mình.

### UC-03.13a Gắn ghi chú vào chương / shot
<a id="uc-0313a"></a>

| Mục | Nội dung |
|---|---|
| Loại | extend của UC-03.13 |
| Tác nhân | Editor |
| Mô tả | Gắn một ghi chú với một chương hoặc một shot cụ thể thay vì để ở cấp dự án |
| Tiền điều kiện | Editor đang tạo hoặc sửa ghi chú của chính mình trong panel Notes |
| Hậu điều kiện | **Thành công:** ghi chú có `target_type` (`CHAPTER` hoặc `SHOT`) và `target_id`; hiện cạnh đối tượng đích. **Tối thiểu:** không gắn được thì ghi chú vẫn lưu ở cấp dự án |
| Kích hoạt | Editor chọn "Gắn vào…" khi tạo hoặc sửa ghi chú |
| Truy vết | FR-MAN-09; 04 §3.2 `notes`; API 2.3 `/projects/{pid}/notes` |
| Giai đoạn | Sau |

**Luồng chính**
1. Editor chọn loại đích: Dự án (mặc định), Chương hoặc Shot.
2. Chương: Editor chọn từ danh sách chương. Shot: Editor chọn chương, rồi chọn shot trong storyboard hiện hành của chương đó.
3. Editor lưu ghi chú; hệ thống ghi `target_type`, `target_id`.
4. Ghi chú hiển thị trong panel Notes (kèm nhãn đích) và dưới dạng biểu tượng cạnh chương trong Workspace hoặc cạnh shot trong Storyboard; thành viên khác thấy qua đồng bộ.

**Luồng thay thế / ngoại lệ**
- **2a.** Chương chưa có storyboard hiện hành: chỉ cho chọn đích Dự án hoặc Chương.
- **4a.** Đích về sau bị xóa (chương bị xóa, shot bị gộp hoặc xóa): ghi chú vẫn còn trong panel Notes với nhãn "đích đã bị xóa" [ĐX].
- ***a.** Chỉ tác giả được sửa hoặc xóa ghi chú của mình; ghi chú của Director (`author_kind = DIRECTOR`) chỉ đọc.

---

<a id="uc-0314"></a>
## UC-03.14 Xem & khôi phục phiên bản chương

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Editor |
| Mô tả | Xem lịch sử và khôi phục văn bản chương về phiên bản trước |
| Tiền điều kiện | Chương có ≥ 2 phiên bản |
| Hậu điều kiện | **Thành công:** chương có phiên bản mới với nội dung cũ; shot bị ảnh hưởng `OUTDATED` |
| Kích hoạt | "Versions" trong Chapter actions |
| Truy vết | FR-MAN-10 |
| Giai đoạn | Sau |

**Luồng chính**
1. Editor mở lịch sử; hệ thống liệt kê phiên bản (thời gian, người sửa, số ký tự).
2. Editor chọn một phiên bản để xem so sánh với hiện tại.
3. Editor bấm "Khôi phục"; hệ thống lưu thành phiên bản mới (không xóa lịch sử).
