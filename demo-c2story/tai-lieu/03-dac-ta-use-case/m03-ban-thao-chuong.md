# M03 — Bản thảo & chương

> Bước 2 của luồng chính. Sơ đồ: `../../so-do/01-use-case/phan-ra/uc-m03-ban-thao-chuong.puml`, `../../so-do/04-tuan-tu/seq-import-chia-chuong.puml`. Yêu cầu: FR-MAN-01..11. Văn bản truyện **chỉ do tác giả sửa** (BR-21).

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
| Truy vết | FR-MAN-01 |

**Luồng chính**
1. Editor mở màn hình Write.
2. Hệ thống hiển thị toàn văn ghép từ các chương theo thứ tự, đánh dấu ranh giới chương; mỗi khoảng giữa hai đoạn có nút "Split here".
3. Editor đọc, có thể chuyển sang UC-03.03, UC-03.04.

### UC-03.01a Sao chép toàn văn
<a id="uc-0301a"></a>
- **Loại:** extend. **Các bước:** bấm "Copy text"; hệ thống ghép toàn văn (có tiêu đề chương) vào clipboard. **Kết quả:** văn bản trong clipboard.

### UC-03.01b Nhập lại (Re-import)
<a id="uc-0301b"></a>
- **Loại:** extend. **Điều kiện:** Editor muốn thay toàn bộ văn bản.
- **Các bước:** (1) hệ thống gợi ý lưu Archive trước (UC-03.11); (2) Editor dán hoặc tải file mới; (3) chuẩn hóa như UC-02.02a; (4) tạo SourceText mới, thay chương thành một Chapter #1 mới; (5) mọi tư liệu và timeline của các chương cũ chuyển `OUTDATED`.
- **Kết quả:** dự án có văn bản mới; bản cũ còn trong Archive.

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
| Quan hệ | được mở rộng bởi UC-03.04, UC-03.05, UC-03.06 |
| Truy vết | FR-MAN-02; BR-05, BR-06, BR-21 |

**Luồng chính**
1. Editor mở Workspace; hệ thống tải mọi chương kèm ETag.
2. Editor sửa văn bản hoặc tiêu đề một chương.
3. Hệ thống tự lưu sau 2 s không gõ (`PATCH` + If-Match).
4. Hệ thống tăng version, lưu snapshot, cập nhật "người sửa cuối", phát `chapter.updated`.
5. Nếu chương đã có tư liệu, hệ thống so hash đoạn nguồn từng shot và đánh dấu shot `OUTDATED`.

**Luồng thay thế / ngoại lệ**
- **3a.** `409`: chuyển sang UC-02.10.
- **3b.** Chương đang bị khóa bởi job: `423`, editor ở chế độ chỉ đọc, hiện "Chương đang được xử lý".
- **5a.** Thay đổi làm đoạn nguồn của nhiều shot lệch: hiện banner "N shot cần sinh lại thuyết minh" với nút đi tới UC-05.07c.

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
| Truy vết | FR-MAN-04; BR-21 |

**Luồng chính**
1. Editor bấm "Suggest chapter splits".
2. Hệ thống tạo job `SUGGEST_SPLITS`. LLM nhận văn bản đã đánh số đoạn, trả `[{startParagraph, title}]`. LLM **không** trả lại văn bản.
3. Hệ thống đánh dấu các điểm chia đề xuất trên màn hình Write.
4. Editor bỏ chọn điểm không muốn, sửa tiêu đề đề xuất.
5. Editor bấm "Áp dụng"; hệ thống thực hiện **UC-03.09**.

**Luồng thay thế / ngoại lệ**
- **2a.** Cách chia hiện tại đã khớp: báo "Your current chapters already match".
- **2b.** LLM lỗi hoặc trả sai schema sau 2 lần thử: báo lỗi, gợi ý chia thủ công (UC-03.04).
- **5a.** Các chương bị ảnh hưởng đã có tư liệu hoặc timeline: hiện cảnh báo trước khi áp dụng (xem UC-03.09).

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
| Truy vết | FR-MAN-03 |

**Luồng chính**
1. Editor chọn vị trí giữa hai đoạn.
2. Editor nhập tiêu đề cho chương mới (mặc định "Chương N+1").
3. Hệ thống thực hiện UC-03.09 với thao tác `SPLIT`.

**Luồng thay thế / ngoại lệ**
- **1a.** Vị trí ở giữa một đoạn: hệ thống dời về ranh giới đoạn gần nhất và hỏi xác nhận.

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
| Truy vết | FR-MAN-05 |

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
| Truy vết | FR-MAN-05 |

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
| Truy vết | FR-MAN-05 |

**Luồng chính**
1. Editor chọn thao tác.
2. *Thêm:* hệ thống tạo chương trống tại vị trí chọn. *Đổi tên:* lưu tiêu đề (If-Match). *Xóa:* hệ thống hiện hệ quả (văn bản, tư liệu, clip timeline bị xóa theo) và yêu cầu xác nhận.
3. Hệ thống ghi, phát sự kiện realtime.

**Luồng thay thế / ngoại lệ**
- **2a.** Xóa chương: có nút "Hoàn tác" trong 10 s (NFR-USA-03); văn bản luôn có trong `chapter_versions`.
- **2b.** Xóa chương duy nhất của dự án: bị chặn.

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
| Truy vết | FR-MAN-05 |

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
| Truy vết | FR-MAN-06; IC-02; BR-05, BR-06, BR-12 |

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
- **Loại:** include. **Các bước:** gọi `POST :find-replace {dryRun: true}`; hiển thị số kết quả theo chương và ngữ cảnh từng kết quả. **Kết quả:** danh sách kết quả, chưa thay đổi dữ liệu.

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

**Luồng chính**
1. Editor chọn một archive; hệ thống hiển thị nội dung chỉ đọc.
2. Editor chọn "Copy this archive's full text" để dán vào Workspace, hoặc "Xóa" (xác nhận).

---

<a id="uc-0313"></a>
## UC-03.13 Ghi chú (Notes)

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Editor |
| Mô tả | Viết ghi chú cấp dự án; xem ghi chú của Director |
| Tiền điều kiện | Là thành viên dự án |
| Hậu điều kiện | **Thành công:** ghi chú được lưu và đồng bộ cho thành viên khác |
| Kích hoạt | Mở panel Notes |
| Quan hệ | được mở rộng bởi UC-03.13a |
| Truy vết | FR-MAN-09 |

**Luồng chính**
1. Editor mở panel Notes; hệ thống hiển thị ghi chú theo thời gian (của người dùng và "Director note").
2. Editor thêm, sửa hoặc xóa ghi chú của mình.

### UC-03.13a Gắn ghi chú vào chương / shot
<a id="uc-0313a"></a>
- **Loại:** extend. **Các bước:** chọn chương hoặc shot đích khi tạo ghi chú. **Kết quả:** ghi chú hiện cạnh đối tượng trong Workspace/Storyboard.

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

**Luồng chính**
1. Editor mở lịch sử; hệ thống liệt kê phiên bản (thời gian, người sửa, số ký tự).
2. Editor chọn một phiên bản để xem so sánh với hiện tại.
3. Editor bấm "Khôi phục"; hệ thống lưu thành phiên bản mới (không xóa lịch sử).
