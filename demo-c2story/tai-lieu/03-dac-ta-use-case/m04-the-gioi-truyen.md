# M04 — Thế giới truyện

> Bước 3 của luồng chính. Sơ đồ: `../../so-do/01-use-case/phan-ra/uc-m04-the-gioi-truyen.puml`. Yêu cầu: FR-WLD-01..11. Thứ tự chỉ dẫn hình ảnh: BR-08.

---

<a id="uc-0401"></a>
## UC-04.01 Phân tích tài sản bằng AI

| Mục | Nội dung |
|---|---|
| Tác nhân chính / phụ | Editor / LLM |
| Mô tả | AI đọc mọi chương, đề xuất nhân vật, địa điểm, đạo cụ **lặp lại** kèm mô tả và facts |
| Tiền điều kiện | Có ≥ 1 chương có văn bản |
| Hậu điều kiện | **Thành công:** danh sách đề xuất được duyệt, tài sản được tạo. **Tối thiểu:** không tạo tài sản khi Editor chưa duyệt |
| Kích hoạt | Bấm "Analyze" trong Story Assets |
| Quan hệ | include UC-04.01a |
| Truy vết | FR-WLD-01 |

**Luồng chính**
1. Editor bấm "Analyze".
2. Hệ thống tạo job `ANALYZE_ASSETS`: LLM đọc từng chương (map), hợp nhất kết quả (reduce), trả danh sách tài sản kèm loại, tên, bí danh, mô tả ngoại hình, facts, các chương xuất hiện.
3. Hệ thống đánh dấu mục trùng với tài sản đã có.
4. Hệ thống thực hiện **UC-04.01a**.
5. Hệ thống tạo các StoryAsset đã duyệt, đề nghị sinh ảnh tham chiếu (UC-04.03) kèm tổng giá.

**Luồng thay thế / ngoại lệ**
- **2a.** Không có tài sản lặp lại: báo "No recurring cast or places to design".
- **2b.** Dự án rất dài: phân tích theo lô chương, hiển thị tiến độ.
- **5a.** Editor từ chối sinh ảnh ngay: tài sản được tạo chưa có ảnh.

### UC-04.01a Duyệt tài sản đề xuất
<a id="uc-0401a"></a>
- **Loại:** include (bước 4).
- **Các bước:** Editor bỏ chọn mục không cần, sửa tên/loại, gộp mục trùng (bí danh của nhau), rồi bấm "Thêm vào dự án".
- **Kết quả:** danh sách tài sản cuối cùng do Editor quyết định.

---

<a id="uc-0402"></a>
## UC-04.02 Quản lý Story Assets

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Editor |
| Mô tả | Xem và quản lý nhân vật, địa điểm, đạo cụ, nhóm của dự án |
| Tiền điều kiện | Là thành viên dự án |
| Hậu điều kiện | **Thành công:** Story Assets phản ánh đúng thế giới truyện |
| Kích hoạt | Mở `?v=assets` |
| Quan hệ | được mở rộng bởi UC-04.02a..e |
| Truy vết | FR-WLD-02, FR-WLD-05, FR-WLD-11 |

**Luồng chính**
1. Editor mở Story Assets; hệ thống hiển thị 3 nhóm (Characters, Locations, Props) và các Group, mỗi tài sản có ảnh tham chiếu và trạng thái.
2. Editor chọn một tài sản để xem chi tiết hoặc thực hiện một use case con.

### UC-04.02a Tạo nhân vật / địa điểm / đạo cụ
<a id="uc-0402a"></a>
- **Loại:** extend. **Các bước:** (1) chọn loại; (2) nhập tên, bí danh, mô tả ngoại hình, facts; (3) chọn sinh ảnh (UC-04.03, include) hoặc tải ảnh (UC-04.04). **Kết quả:** StoryAsset mới.

### UC-04.02b Tạo nhóm nhân vật
<a id="uc-0402b"></a>
- **Loại:** extend. **Các bước:** đặt tên nhóm, chọn ≥ 2 nhân vật thành viên, tùy chọn sinh ảnh nhóm. **Kết quả:** StoryAsset loại `GROUP`.

### UC-04.02c Thêm từ thư viện cá nhân
<a id="uc-0402c"></a>
- **Loại:** extend. **Các bước:** mở thư viện (M08), chọn tài sản; hệ thống tạo StoryAsset dùng chung ảnh gốc (`source_library_asset_id`). **Kết quả:** tài sản có trong dự án, không tốn credit; sửa trong dự án không ảnh hưởng thư viện (FR-LIB-05).

### UC-04.02d Gỡ khỏi dự án
<a id="uc-0402d"></a>
- **Loại:** extend. **Các bước:** chọn "Remove from project", xác nhận. **Kết quả:** tài sản bị gỡ; shot đang tham chiếu giữ `raw_name` và chuyển "chưa liên kết" (BR-16); ảnh shot đã sinh không đổi.

### UC-04.02e Quản lý bí danh & facts
<a id="uc-0402e"></a>
- **Loại:** extend. **Các bước:** thêm/xóa bí danh (≤ 10), sửa facts bất biến (vd. "tóc đen ngang vai"). **Kết quả:** prompt các lần sinh sau dùng facts mới; storyboard khớp tên theo bí danh mới.

---

<a id="uc-0403"></a>
## UC-04.03 Sinh ảnh tham chiếu

| Mục | Nội dung |
|---|---|
| Tác nhân chính / phụ | Editor / Image Provider |
| Mô tả | Sinh ảnh chuẩn cho tài sản theo style + Art Direction để giữ nhất quán |
| Tiền điều kiện | Dự án có style; tài sản có mô tả; đủ credit |
| Hậu điều kiện | **Thành công:** `asset_images` mới, đặt làm ảnh hiện hành; credit bị trừ. **Tối thiểu:** lỗi thì hoàn credit |
| Kích hoạt | "Generate" / "Regenerate" trên tài sản |
| Quan hệ | được include bởi UC-04.02a; được mở rộng bởi UC-04.03a |
| Truy vết | FR-WLD-03; BR-01, BR-02, BR-08, BR-14 |

**Luồng chính**
1. Editor bấm "Generate" (hiện giá 1 credit).
2. Hệ thống giữ credit, tạo job `GENERATE_ASSET_IMAGE`.
3. Worker ghép prompt: style + Art Direction + Visual Rules + mô tả + facts; địa điểm sinh reference sheet nhiều góc nhìn.
4. Image Provider trả ảnh; moderation đầu ra; lưu ảnh; trừ credit.
5. Giao diện hiển thị ảnh mới; phiên bản cũ vẫn xem được.

**Luồng thay thế / ngoại lệ**
- **1a.** Tài sản dùng ảnh nguyên bản (BR-14): nút bị ẩn.
- **4a.** Lỗi hoặc vi phạm chính sách: hoàn credit, gợi ý sửa mô tả.

### UC-04.03a Sinh lại tất cả (Regenerate all)
<a id="uc-0403a"></a>
- **Loại:** extend. **Điều kiện:** sau khi đổi style/Art Direction. **Các bước:** hệ thống đếm tài sản (bỏ qua tài sản "use exact"), hiện tổng giá, Editor xác nhận, tạo job hàng loạt. **Kết quả:** mọi tài sản có ảnh theo style mới.

---

<a id="uc-0404"></a>
## UC-04.04 Dùng ảnh tải lên nguyên bản

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Editor |
| Mô tả | Dùng ảnh người dùng tải lên làm ảnh tham chiếu, không cho AI vẽ lại |
| Tiền điều kiện | Ảnh PNG/JPEG/WebP ≤ 10 MB, cạnh ngắn ≥ 512 px |
| Hậu điều kiện | **Thành công:** tài sản có `use_exact_image = true` |
| Kích hoạt | "Use this exact image" khi tạo/sửa tài sản |
| Quan hệ | extend UC-04.02a |
| Truy vết | FR-WLD-04; BR-14; NFR-SEC-10 |

**Luồng chính**
1. Editor tải ảnh lên.
2. Hệ thống kiểm tra MIME, kích thước, quét malware, bỏ EXIF, moderation.
3. Hệ thống lưu ảnh làm tham chiếu, gắn cờ "use exact".

**Luồng thay thế / ngoại lệ**
- **2a.** Ảnh không đạt: báo lý do cụ thể.

---

<a id="uc-0405"></a>
## UC-04.05 Chọn style dự án

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Editor (Owner khi đổi; xem thêm UC-02.04) |
| Mô tả | Chọn phong cách nghệ thuật từ danh mục |
| Tiền điều kiện | Là Owner (đổi) hoặc dự án chưa có style (lần đầu, Editor được chọn) |
| Hậu điều kiện | **Thành công:** `projects.style_id` cập nhật |
| Kích hoạt | "Set style" hoặc điểm duyệt UC-07.03 |
| Truy vết | FR-WLD-06 |

**Luồng chính**
1. Hệ thống mở Styles Library (ảnh mẫu, tên, mô tả).
2. Người dùng chọn style; hệ thống lưu.
3. Nếu đã có ảnh tham chiếu, hệ thống đề xuất UC-04.03a.

---

<a id="uc-0406"></a>
## UC-04.06 Thiết lập Art Direction

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Editor |
| Mô tả | Viết chỉ dẫn phong cách bổ sung lên style của dự án |
| Tiền điều kiện | Là thành viên dự án |
| Hậu điều kiện | **Thành công:** `projects.art_direction` cập nhật; áp cho mọi lần sinh ảnh sau |
| Kích hoạt | Ô "Art direction" trong Story Assets |
| Truy vết | FR-WLD-07; BR-08 |

**Luồng chính**
1. Editor nhập chỉ dẫn (vd. "tông ấm, bão hòa thấp, nét vẽ mềm").
2. Hệ thống lưu (If-Match) và gợi ý sinh lại ảnh nếu cần.

---

<a id="uc-0407"></a>
## UC-04.07 Xem dòng thời gian truyện

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Editor |
| Mô tả | Xem dòng thời gian (ngày, mùa, tóm tắt) theo chương do AI dựng |
| Tiền điều kiện | Đã chạy phân tích (UC-04.09) ít nhất một lần |
| Hậu điều kiện | **Thành công:** hiển thị timeline truyện theo tỷ lệ thời gian |
| Kích hoạt | Mở `?v=timeline` |
| Quan hệ | được mở rộng bởi UC-04.09 |
| Truy vết | FR-WLD-08 |

**Luồng chính**
1. Editor mở Story timeline.
2. Hệ thống hiển thị các mốc (nhãn ngày, mùa, chương, tóm tắt).
3. Editor bấm một mốc để mở chương tương ứng.

**Luồng thay thế / ngoại lệ**
- **2a.** Chưa có dữ liệu: hiện nút "Phân tích" (UC-04.09).

---

<a id="uc-0408"></a>
## UC-04.08 Xem đồ thị quan hệ

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Editor |
| Mô tả | Xem đồ thị quan hệ giữa các nhân vật và diễn biến |
| Tiền điều kiện | Đã chạy phân tích |
| Hậu điều kiện | **Thành công:** hiển thị đồ thị |
| Kích hoạt | Mở `?v=relationships` |
| Quan hệ | được mở rộng bởi UC-04.09 |
| Truy vết | FR-WLD-09 |

**Luồng chính**
1. Editor mở Relationship graph.
2. Hệ thống vẽ nút (nhân vật) và cạnh (nhãn quan hệ, diễn biến, chương bắt đầu).
3. Editor bấm một cạnh để đọc diễn biến.

---

<a id="uc-0409"></a>
## UC-04.09 Phân tích lại (Re-analyse)

| Mục | Nội dung |
|---|---|
| Tác nhân chính / phụ | Editor / LLM |
| Mô tả | Dựng lại Timeline và Relationships sau khi văn bản hoặc tài sản thay đổi |
| Tiền điều kiện | Có văn bản |
| Hậu điều kiện | **Thành công:** `timeline_events` và `relationships` được thay mới |
| Kích hoạt | "Re-analyse" |
| Quan hệ | extend UC-04.07, UC-04.08 |
| Truy vết | FR-WLD-08, FR-WLD-09 |

**Luồng chính**
1. Editor bấm "Re-analyse".
2. Hệ thống tạo job `STORY_META`; LLM trả mốc thời gian theo chương và cặp quan hệ (theo tên/bí danh tài sản).
3. Hệ thống thay dữ liệu cũ, hiển thị kết quả.

**Luồng thay thế / ngoại lệ**
- **2a.** Tên nhân vật không khớp tài sản: bỏ qua cạnh đó, liệt kê để Editor thêm tài sản.

---

<a id="uc-0410"></a>
## UC-04.10 Quản lý Visual Rules

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Editor |
| Mô tả | Tạo, sửa, bật/tắt, xóa luật hình ảnh áp toàn dự án hoặc theo chương |
| Tiền điều kiện | Là thành viên dự án |
| Hậu điều kiện | **Thành công:** luật được áp vào prompt các lần sinh ảnh sau theo thứ tự BR-08 |
| Kích hoạt | Mở `?v=visual-rules` |
| Truy vết | FR-WLD-10; BR-08 |

**Luồng chính**
1. Editor bấm "New rule", nhập tên, nội dung, phạm vi.
2. Hệ thống lưu; danh sách luật hiển thị theo phạm vi.
3. Editor có thể sửa, tắt tạm hoặc xóa (xác nhận).

**Luồng thay thế / ngoại lệ**
- **1a.** Nội dung > 1.000 ký tự hoặc tên > 80 ký tự: báo lỗi kiểm tra.

---

<a id="uc-0411"></a>
## UC-04.11 Xuất ZIP ảnh tài sản

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Editor |
| Mô tả | Tải toàn bộ ảnh tham chiếu tài sản thành một file ZIP |
| Tiền điều kiện | Có ít nhất một tài sản có ảnh |
| Hậu điều kiện | **Thành công:** link tải ZIP (hết hạn 15 phút) |
| Kích hoạt | "Export assets" trong Project Assets |
| Truy vết | FR-WLD-11 |

**Luồng chính**
1. Editor bấm "Export assets".
2. Hệ thống tạo job `EXPORT_ZIP` (miễn phí), đặt tên file theo loại/tên tài sản.
3. Khi xong, hệ thống cung cấp link tải.

**Luồng thay thế / ngoại lệ**
- **1a.** Chưa có ảnh nào: báo "No generated asset images to export yet".
