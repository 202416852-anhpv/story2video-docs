# M08 — Thư viện tài sản cá nhân

> Sơ đồ: `../../so-do/01-use-case/phan-ra/uc-m08-thu-vien-tai-san.puml`. Yêu cầu: FR-LIB-01..05.

---

<a id="uc-0801"></a>
## UC-08.01 Xem thư viện

| Mục | Nội dung |
|---|---|
| Tác nhân chính | User |
| Mô tả | Xem các nhân vật, địa điểm, đạo cụ đã lưu để tái sử dụng giữa các dự án |
| Tiền điều kiện | Đã đăng nhập |
| Hậu điều kiện | **Thành công:** hiển thị thư viện theo tab |
| Kích hoạt | Mở `/characters` |
| Quan hệ | được mở rộng bởi UC-08.01a |
| Truy vết | FR-LIB-01 |

**Luồng chính**
1. User mở thư viện; hệ thống hiển thị 3 tab Characters / Locations / Items kèm số lượng.
2. User chọn một tài sản để xem chi tiết (ảnh, mô tả, facts, các dự án đang dùng).

**Luồng thay thế / ngoại lệ**
- **1a.** Thư viện trống: hiện hướng dẫn tạo tài sản (UC-08.02) hoặc lưu từ dự án (UC-08.04).

### UC-08.01a Lọc & tìm kiếm
<a id="uc-0801a"></a>
- **Loại:** extend. **Các bước:** lọc All / My Created / From Projects; tìm theo tên hoặc bí danh; sắp xếp Recent. **Kết quả:** danh sách thu hẹp.

---

<a id="uc-0802"></a>
## UC-08.02 Tạo tài sản từ ảnh hoặc mô tả

| Mục | Nội dung |
|---|---|
| Tác nhân chính / phụ | User / Image Provider |
| Mô tả | Tạo tài sản trong thư viện, ngoài bất kỳ dự án nào |
| Tiền điều kiện | Đã đăng nhập |
| Hậu điều kiện | **Thành công:** `library_assets` mới có ảnh tham chiếu |
| Kích hoạt | "New character / location / item" |
| Quan hệ | include UC-08.02a |
| Truy vết | FR-LIB-03 |

**Luồng chính**
1. User chọn loại, nhập tên, bí danh, mô tả, facts.
2. User tải ảnh (kiểm tra như UC-04.04, có tùy chọn dùng nguyên bản) hoặc chọn sinh ảnh.
3. Nếu sinh ảnh, thực hiện **UC-08.02a**.
4. Hệ thống lưu tài sản.

### UC-08.02a Sinh ảnh tham chiếu
<a id="uc-0802a"></a>
- **Loại:** include. **Các bước:** User chọn style cho ảnh tham chiếu (vì tài sản thư viện không thuộc dự án nào); hệ thống hiện giá 1 credit, giữ credit (UC-05.17), sinh ảnh, lưu. **Kết quả:** tài sản có ảnh; lỗi thì hoàn credit.

---

<a id="uc-0803"></a>
## UC-08.03 Sửa / xóa tài sản

| Mục | Nội dung |
|---|---|
| Tác nhân chính | User |
| Mô tả | Sửa thông tin hoặc xóa vĩnh viễn tài sản khỏi thư viện |
| Tiền điều kiện | Là chủ tài sản |
| Hậu điều kiện | **Thành công:** tài sản cập nhật hoặc bị xóa; **bản sao trong các dự án không bị ảnh hưởng** (FR-LIB-05) |
| Kích hoạt | "Edit" / "Delete permanently from library" |
| Truy vết | FR-LIB-05, FR-WLD-05 |

**Luồng chính**
1. User sửa tên, bí danh, mô tả, facts, ảnh; hệ thống lưu.
2. Hoặc User chọn xóa; hệ thống cảnh báo "This cannot be undone" và liệt kê dự án đang có bản sao; User xác nhận hai bước.

---

<a id="uc-0804"></a>
## UC-08.04 Lưu tài sản từ dự án vào thư viện

| Mục | Nội dung |
|---|---|
| Tác nhân chính | User (là thành viên dự án) |
| Mô tả | Lưu một Story Asset của dự án vào thư viện cá nhân để dùng cho dự án khác |
| Tiền điều kiện | Là thành viên dự án chứa tài sản |
| Hậu điều kiện | **Thành công:** `library_assets` mới dùng chung ảnh gốc (không nhân đôi file) |
| Kích hoạt | "Save to library" trên Story Asset |
| Truy vết | FR-LIB-04 |

**Luồng chính**
1. User chọn "Lưu vào thư viện".
2. Hệ thống sao chép thông tin, tham chiếu ảnh hiện hành.
3. Hệ thống báo thành công; tài sản xuất hiện ở tab "From Projects".

**Luồng thay thế / ngoại lệ**
- **2a.** Thư viện đã có tài sản cùng tên và cùng ảnh: hỏi cập nhật hay tạo mới.

---

<a id="uc-0805"></a>
## UC-08.05 Thêm tài sản vào dự án

| Mục | Nội dung |
|---|---|
| Tác nhân chính | User (là Editor của dự án đích) |
| Mô tả | Đưa tài sản từ thư viện vào Story Assets của dự án |
| Tiền điều kiện | Là thành viên dự án đích |
| Hậu điều kiện | **Thành công:** StoryAsset mới trong dự án (`source_library_asset_id`), **không tốn credit** |
| Kích hoạt | "Add to project" ở thư viện, hoặc UC-04.02c từ dự án |
| Truy vết | FR-LIB-05, FR-WLD-05 |

**Luồng chính**
1. User chọn tài sản và dự án đích.
2. Hệ thống tạo StoryAsset dùng chung ảnh gốc.
3. Nếu style của tài sản khác style dự án, hệ thống gợi ý sinh lại ảnh tham chiếu theo style dự án (UC-04.03, tính phí).
