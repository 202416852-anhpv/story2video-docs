# M04 — Thế giới truyện

> Bước 3 của luồng chính. Sơ đồ: `../../so-do/01-use-case/phan-ra/uc-m04-the-gioi-truyen.puml`, `../../so-do/04-tuan-tu/seq-the-gioi-truyen.puml`, `seq-tai-san-phong-cach.puml`. Yêu cầu: FR-WLD-01..11. Thứ tự chỉ dẫn hình ảnh: BR-08.

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
| Quan hệ | extend UC-04.02; include UC-04.01a, UC-05.17 |
| Truy vết | FR-WLD-01; BR-01, BR-02; 08 §3.2 (`ANALYZE_ASSETS`); seq-the-gioi-truyen |
| Giai đoạn | P1 |

**Luồng chính**
1. Editor bấm "Analyze".
2. Hệ thống hiện giá ước tính (theo số chương); Editor xác nhận; hệ thống giữ tiền (UC-05.17) và tạo job `ANALYZE_ASSETS`: LLM đọc từng chương (map), hợp nhất kết quả (reduce), trả danh sách tài sản kèm loại, tên, bí danh, mô tả ngoại hình, facts, các chương xuất hiện.
3. Hệ thống đánh dấu mục trùng với tài sản đã có.
4. Hệ thống thực hiện **UC-04.01a**.
5. Hệ thống tạo các StoryAsset đã duyệt, đề nghị sinh ảnh tham chiếu (UC-04.03) kèm tổng giá.

**Luồng thay thế / ngoại lệ**
- **2a.** Không có tài sản lặp lại: báo "No recurring cast or places to design".
- **2b.** Dự án rất dài: phân tích theo lô chương, hiển thị tiến độ.
- **2c.** Không đủ số dư: `402`; chạm trần chi tiêu ngày: `503 DAILY_BUDGET_EXCEEDED`.
- **5a.** Editor từ chối sinh ảnh ngay: tài sản được tạo chưa có ảnh.

### UC-04.01a Duyệt tài sản đề xuất
<a id="uc-0401a"></a>

| Mục | Nội dung |
|---|---|
| Loại | include của UC-04.01 (bước 4) |
| Tác nhân | Editor |
| Mô tả | Editor quyết định tài sản nào được tạo từ danh sách AI đề xuất; AI không tự tạo gì |
| Tiền điều kiện | Job `ANALYZE_ASSETS` đã trả danh sách đề xuất (UC-04.01 bước 2–3) |
| Hậu điều kiện | **Thành công:** có danh sách tài sản cuối cùng do Editor chốt. **Tối thiểu:** nếu Editor đóng mà không xác nhận thì không tạo tài sản nào |
| Kích hoạt | UC-04.01 bước 4 |
| Truy vết | FR-WLD-01; 08 §5 (tên 1–80 ký tự, bí danh ≤ 10, ≤ 200 Story Assets); seq-the-gioi-truyen |
| Giai đoạn | P1 |

**Luồng chính**
1. Hệ thống hiển thị "Recommended assets" nhóm theo Characters, Locations, Props; mỗi mục có tên, bí danh, mô tả ngoại hình, facts và các chương xuất hiện; mục trùng với tài sản đã có được gắn nhãn.
2. Editor bỏ chọn mục không cần.
3. Editor sửa tên hoặc loại của mục nếu cần.
4. Editor gộp các mục trùng: tên của mục này trở thành bí danh của mục kia.
5. Editor bấm "Thêm vào dự án"; hệ thống trả danh sách đã chốt cho UC-04.01 bước 5.

**Luồng thay thế / ngoại lệ**
- **4a.** Mục trùng với tài sản đã có: mặc định bỏ chọn; Editor có thể chọn "gộp vào tài sản hiện có" (thêm tên mới thành bí danh).
- **5a.** Tên rỗng hoặc dài hơn 80 ký tự, hoặc bí danh vượt 10 mục: báo lỗi tại mục đó, không cho xác nhận.
- **5b.** Tổng số tài sản sau khi thêm vượt 200: chặn và yêu cầu bỏ bớt.
- ***a.** Editor đóng hộp thoại: không tạo gì; có thể mở lại danh sách đề xuất bằng cách phân tích lại.

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
| Quan hệ | được mở rộng bởi UC-04.01, UC-04.02a..e |
| Truy vết | FR-WLD-02, FR-WLD-05, FR-WLD-11; seq-tai-san-phong-cach |
| Giai đoạn | P1 |

**Luồng chính**
1. Editor mở Story Assets; hệ thống hiển thị 3 nhóm (Characters, Locations, Props) và các Group, mỗi tài sản có ảnh tham chiếu và trạng thái.
2. Editor chọn một tài sản để xem chi tiết hoặc thực hiện một use case con; để AI đề xuất tài sản từ các chương, Editor bấm "Analyze" (UC-04.01).

### UC-04.02a Tạo nhân vật / địa điểm / đạo cụ
<a id="uc-0402a"></a>

| Mục | Nội dung |
|---|---|
| Loại | extend của UC-04.02 |
| Tác nhân | Editor / Image Provider (khi chọn sinh ảnh) |
| Mô tả | Tạo mới một nhân vật, địa điểm hoặc đạo cụ thủ công |
| Tiền điều kiện | Là thành viên dự án; dự án có dưới 200 Story Assets |
| Hậu điều kiện | **Thành công:** có StoryAsset mới (`kind` = `CHARACTER`, `LOCATION` hoặc `PROP`, `version = 1`). **Tối thiểu:** tạo tài sản không phụ thuộc việc có ảnh hay không |
| Kích hoạt | Bấm "New character / location / prop" |
| Truy vết | FR-WLD-02, FR-WLD-03; BR-14; 08 §5; API 2.4 `POST /projects/{pid}/story-assets`; seq-the-gioi-truyen |
| Giai đoạn | P1 |

**Luồng chính**
1. Editor chọn loại tài sản.
2. Editor nhập tên (1–80 ký tự), bí danh (≤ 10), mô tả ngoại hình, facts bất biến.
3. Editor chọn một trong ba cách có ảnh tham chiếu: sinh bằng AI (**UC-04.03**, include, tính phí); tải ảnh lên (**UC-04.04**, dùng nguyên bản); hoặc bỏ qua.
4. Hệ thống lưu StoryAsset và hiển thị trong nhóm tương ứng.

**Luồng thay thế / ngoại lệ**
- **2a.** Tên trùng với tên hoặc bí danh của tài sản khác: cảnh báo vì sẽ gây khớp mơ hồ ở UC-05.06f; Editor có thể vẫn tạo.
- **3a.** Chọn sinh ảnh nhưng không đủ số dư: `402`; tài sản vẫn được tạo, chưa có ảnh.
- **3b.** Sinh ảnh lỗi: hoàn tiền (UC-04.03 nhánh 4a); tài sản vẫn được tạo.
- **4a.** Đã có 200 tài sản: chặn tạo thêm.

### UC-04.02b Tạo nhóm nhân vật
<a id="uc-0402b"></a>

| Mục | Nội dung |
|---|---|
| Loại | extend của UC-04.02 |
| Tác nhân | Editor / Image Provider (khi chọn sinh ảnh nhóm) |
| Mô tả | Gom nhiều nhân vật thành một nhóm (vd. gia đình, băng nhóm) để dùng như một thực thể trong shot |
| Tiền điều kiện | Dự án có ít nhất 2 nhân vật (`CHARACTER`) |
| Hậu điều kiện | **Thành công:** có StoryAsset `kind = GROUP` với ≥ 2 thành viên. **Tối thiểu:** không tạo nhóm vi phạm IC-13 |
| Kích hoạt | Bấm "New group" |
| Truy vết | FR-WLD-02; IC-13; 04 §3.3 `story_asset_group_members`; seq-tai-san-phong-cach |
| Giai đoạn | P1 |

**Luồng chính**
1. Editor đặt tên nhóm (1–80 ký tự).
2. Editor chọn các nhân vật thành viên (tối thiểu 2).
3. Editor có thể chọn sinh ảnh nhóm (UC-04.03, tính phí).
4. Hệ thống lưu StoryAsset `GROUP` và các dòng `story_asset_group_members`.

**Luồng thay thế / ngoại lệ**
- **2a.** Chọn dưới 2 thành viên, thành viên không phải `CHARACTER`, thành viên thuộc dự án khác hoặc chọn chính nhóm: từ chối (IC-13).
- **3a.** Không đủ số dư hoặc sinh ảnh lỗi: nhóm vẫn được tạo, chưa có ảnh.
- ***a.** Sau này thành viên bị gỡ khỏi dự án (UC-04.02d) và nhóm còn dưới 2 thành viên: hệ thống cảnh báo Editor bổ sung hoặc xóa nhóm [ĐX].

### UC-04.02c Thêm từ thư viện cá nhân
<a id="uc-0402c"></a>

| Mục | Nội dung |
|---|---|
| Loại | extend của UC-04.02 |
| Tác nhân | Editor |
| Mô tả | Đưa tài sản từ thư viện cá nhân (M08) vào dự án mà không tốn phí |
| Tiền điều kiện | Editor có thư viện cá nhân; dự án có dưới 200 Story Assets |
| Hậu điều kiện | **Thành công:** có StoryAsset mới trỏ `source_library_asset_id` và dùng chung ảnh gốc. **Tối thiểu:** thư viện không bị đổi |
| Kích hoạt | Bấm "Add from library" |
| Truy vết | FR-WLD-02, FR-LIB-05; UC-08.05; API 2.4 `POST /projects/{pid}/story-assets` với `{libraryAssetId}` |
| Giai đoạn | Sau |

**Luồng chính**
1. Hệ thống mở thư viện (UC-08.01) trong chế độ chọn; Editor tìm, lọc (UC-08.01a) và chọn một hoặc nhiều tài sản.
2. Editor bấm "Add to project".
3. Hệ thống tạo StoryAsset cho mỗi tài sản đã chọn: sao chép loại, tên, bí danh, mô tả, facts, cờ `use_exact_image`; dùng chung file ảnh tham chiếu (không nhân bản file).
4. Hệ thống không tốn phí; tài sản xuất hiện ngay trong Story Assets.

**Luồng thay thế / ngoại lệ**
- **1a.** Thư viện trống: gợi ý tạo tài sản ở thư viện (UC-08.02) hoặc lưu từ dự án (UC-08.04).
- **3a.** Tài sản đó đã có trong dự án (cùng `source_library_asset_id`): báo và không thêm bản trùng [ĐX].
- **3b.** Ảnh thư viện khác style dự án: cảnh báo và gợi ý "Regenerate" (UC-04.03, tính phí) [ĐX].
- **3c.** Vượt 200 tài sản: chặn phần vượt.
- ***a.** Sửa tài sản trong dự án **không** đổi bản ở thư viện và ngược lại (FR-LIB-05).

### UC-04.02d Gỡ khỏi dự án
<a id="uc-0402d"></a>

| Mục | Nội dung |
|---|---|
| Loại | extend của UC-04.02 |
| Tác nhân | Editor |
| Mô tả | Gỡ một tài sản khỏi dự án mà không làm hỏng các shot và ảnh đã sinh |
| Tiền điều kiện | Tài sản thuộc dự án |
| Hậu điều kiện | **Thành công:** StoryAsset bị gỡ; các shot từng tham chiếu giữ `raw_name` và chuyển "chưa liên kết"; ảnh shot đã sinh không đổi. **Tối thiểu:** không xóa gì khi Editor chưa xác nhận |
| Kích hoạt | Chọn "Remove from project" |
| Truy vết | BR-16; 04 §3.3, §3.4 (`shot_asset_refs.story_asset_id` cho phép NULL); API 2.4 `DELETE /projects/{pid}/story-assets/{sid}`; seq-tai-san-phong-cach |
| Giai đoạn | P1 |

**Luồng chính**
1. Editor chọn "Remove from project".
2. Hệ thống hiển thị số shot đang tham chiếu tài sản, các nhóm chứa nó và các quan hệ liên quan; yêu cầu xác nhận.
3. Editor xác nhận.
4. Hệ thống xóa StoryAsset khỏi dự án trong một giao dịch: đặt `shot_asset_refs.story_asset_id = NULL` (giữ `raw_name`), gỡ khỏi các nhóm, xóa các quan hệ (`relationships`) có tài sản này [ĐX].
5. Hệ thống không động tới ảnh shot đã sinh và không xóa tài sản gốc ở thư viện cá nhân.

**Luồng thay thế / ngoại lệ**
- **3a.** Editor hủy: không đổi gì.
- **4a.** `409`: tài sản vừa được người khác sửa; tải lại và xác nhận lại (UC-02.10).
- ***a.** Về sau thêm lại tài sản cùng tên: UC-05.06f có thể tự khớp lại các tham chiếu "chưa liên kết".

### UC-04.02e Chỉnh sửa tài sản
<a id="uc-0402e"></a>

| Mục | Nội dung |
|---|---|
| Loại | extend của UC-04.02 |
| Tác nhân | Editor |
| Mô tả | Sửa tại chỗ một nhân vật, địa điểm, đạo cụ hoặc nhóm: tên, bí danh (để khớp tên trong shot), mô tả ngoại hình, facts bất biến (đưa vào prompt sinh ảnh), thành viên nhóm, ảnh tham chiếu. Sửa **không** phải tạo lại: giữ nguyên định danh nên mọi tham chiếu shot, nhóm, quan hệ vẫn còn |
| Tiền điều kiện | Tài sản thuộc dự án |
| Hậu điều kiện | **Thành công:** StoryAsset được cập nhật, giữ nguyên `id`, `version` tăng 1; `shot_asset_refs`, nhóm và `relationships` trỏ tới tài sản không đổi. **Tối thiểu:** ảnh đã sinh không bị đổi; không tốn phí nếu Editor không chọn sinh lại |
| Kích hoạt | Mở chi tiết tài sản, bấm "Edit" |
| Quan hệ | được mở rộng bởi UC-04.04 (thay ảnh bằng ảnh tải lên) |
| Truy vết | FR-WLD-02, FR-WLD-13; BR-08, BR-14; IC-13; 08 §5 (tên 1–80 ký tự, bí danh ≤ 10); API 2.4 `PATCH /projects/{pid}/story-assets/{sid}` (If-Match); seq-tai-san-phong-cach |
| Giai đoạn | P1 |

**Luồng chính**
1. Editor mở chi tiết tài sản và bấm "Edit"; hệ thống hiển thị biểu mẫu với giá trị hiện tại và `version`.
2. Editor sửa một hoặc nhiều trường: tên, bí danh (thêm/xóa, tối đa 10), mô tả ngoại hình, facts bất biến (mỗi fact là một đặc điểm cố định, vd. "tóc đen ngang vai"). Với nhóm (`GROUP`): thêm hoặc bớt nhân vật thành viên.
3. Editor lưu; hệ thống gửi `PATCH` kèm `If-Match`, cập nhật các trường đã đổi và tăng `version`.
4. Giá trị cũ bị ghi đè (không lưu lịch sử; giá trị lúc sinh còn trong `prompt_snapshot` của ảnh đã sinh). Ảnh đã sinh không đổi. Mọi lần sinh ảnh sau, kể cả sinh lại ảnh ở chương phía trước, dùng mô tả và facts mới trong prompt (UC-04.03, UC-05.09); storyboard và UC-05.06f khớp tên theo tên và bí danh mới.

**Luồng thay thế / ngoại lệ**
- **2a.** Tên hoặc bí danh trùng tên hoặc bí danh của tài sản khác trong dự án: cảnh báo khớp mơ hồ (UC-05.06f); Editor có thể vẫn lưu.
- **2b.** Tên rỗng hoặc dài hơn 80 ký tự, hoặc vượt 10 bí danh: báo lỗi, không lưu.
- **2c.** Nhóm còn dưới 2 thành viên, thành viên không phải `CHARACTER`, thuộc dự án khác hoặc chính nhóm: từ chối (IC-13).
- **2d.** Editor muốn thay ảnh tham chiếu bằng ảnh tải lên: thực hiện UC-04.04 (extend); ảnh cũ vẫn xem được trong lịch sử `asset_images`.
- **2e.** Editor tắt "use exact" của tài sản đang dùng ảnh nguyên bản: nút "Generate" hiện lại; ảnh hiện hành giữ nguyên cho tới khi Editor chủ động sinh (UC-04.03) [ĐX].
- **2f.** Đổi loại tài sản (`kind`) không được hỗ trợ: Editor gỡ (UC-04.02d) rồi tạo mới (UC-04.02a) [ĐX].
- **3a.** `409`: tài sản vừa được người khác sửa; xử lý theo UC-02.10.
- **4a.** Sau khi sửa mô tả, facts hoặc thành viên nhóm, hệ thống gợi ý "Regenerate" kèm giá thay vì tự sinh lại (UC-04.03); tài sản "use exact" không có gợi ý này (BR-14).
- **4b.** Nhân vật đổi ngoại hình theo mạch truyện (vd. cắt tóc từ chương 6): không sửa facts của tài sản đang dùng cho các chương trước, vì sinh lại ảnh ở các chương đó sẽ ra ngoại hình mới. Editor tạo tài sản riêng cho từng giai đoạn (UC-04.02a, vd. "An (trưởng thành)") và gán shot bằng UC-05.06b; trùng tên hoặc bí danh xử lý như 2a. Sau MVP: giai đoạn ngoại hình (FR-WLD-13, QĐ-142).
- ***a.** Tài sản thêm từ thư viện cá nhân: sửa chỉ đổi bản trong dự án, không đổi bản ở thư viện (FR-LIB-05).

---

<a id="uc-0403"></a>
## UC-04.03 Sinh ảnh tham chiếu

| Mục | Nội dung |
|---|---|
| Tác nhân chính / phụ | Editor / Image Provider |
| Mô tả | Sinh ảnh chuẩn cho tài sản theo style + Art Direction để giữ nhất quán |
| Tiền điều kiện | Dự án có style; tài sản có mô tả; đủ số dư |
| Hậu điều kiện | **Thành công:** `asset_images` mới, đặt làm ảnh hiện hành; tiền bị trừ. **Tối thiểu:** lỗi thì hoàn tiền |
| Kích hoạt | "Generate" / "Regenerate" trên tài sản |
| Quan hệ | được include bởi UC-04.02a; được mở rộng bởi UC-04.03a |
| Truy vết | FR-WLD-03; BR-01, BR-02, BR-08, BR-14; seq-the-gioi-truyen |
| Giai đoạn | P1 |

**Luồng chính**
1. Editor bấm "Generate" (hiện giá ước tính).
2. Hệ thống giữ tiền, tạo job `GENERATE_ASSET_IMAGE`.
3. Worker ghép prompt: style + Art Direction + Visual Rules + mô tả + facts; địa điểm sinh reference sheet nhiều góc nhìn.
4. Image Provider trả ảnh; moderation đầu ra; lưu ảnh; trừ tiền.
5. Giao diện hiển thị ảnh mới; phiên bản cũ vẫn xem được.

**Luồng thay thế / ngoại lệ**
- **1a.** Tài sản dùng ảnh nguyên bản (BR-14): nút bị ẩn.
- **4a.** Lỗi hoặc vi phạm chính sách: hoàn tiền, gợi ý sửa mô tả.

### UC-04.03a Sinh lại tất cả (Regenerate all)
<a id="uc-0403a"></a>

| Mục | Nội dung |
|---|---|
| Loại | extend của UC-04.03 |
| Tác nhân | Editor / Image Provider |
| Mô tả | Sinh lại ảnh tham chiếu của mọi tài sản sau khi đổi style hoặc Art Direction, bỏ qua tài sản dùng ảnh nguyên bản |
| Tiền điều kiện | Dự án có style; có ít nhất một tài sản không dùng "use exact"; đủ số dư cho toàn bộ |
| Hậu điều kiện | **Thành công:** mọi tài sản đủ điều kiện có `asset_images` mới theo style mới. **Tối thiểu:** tài sản "use exact" không bao giờ bị vẽ lại; job lỗi được hoàn toàn bộ tiền đã giữ của nó |
| Kích hoạt | Bấm "Regenerate all" (thường sau khi đổi style, UC-04.05, hoặc Art Direction, UC-04.06) |
| Truy vết | BR-01, BR-02, BR-14, BR-15; WR-05; API 2.4 `POST /projects/{pid}/story-assets:regenerate-all`; seq-the-gioi-truyen |
| Giai đoạn | P1 |

**Luồng chính**
1. Editor bấm "Regenerate all".
2. Hệ thống đếm các tài sản đủ điều kiện (bỏ tài sản có `use_exact_image = true`) và hiển thị tổng giá (theo đơn giá ảnh tham chiếu).
3. Editor xác nhận.
4. Trong **một giao dịch**, hệ thống tạo mỗi tài sản một job `GENERATE_ASSET_IMAGE` và giữ tiền riêng cho từng job (WR-05); thiếu tiền cho bất kỳ job nào thì không tạo job nào.
5. Mỗi job chạy như UC-04.03 bước 3–4 và CAPTURE hoặc RELEASE tiền của chính nó.
6. Tiến độ gửi qua SSE (`job.updated`, `asset.updated`); khi xong, mọi tài sản đủ điều kiện có ảnh theo style mới. Ảnh cũ được giữ như phiên bản trước.

**Luồng thay thế / ngoại lệ**
- **2a.** Không có tài sản nào đủ điều kiện: báo "Không có tài sản cần sinh lại", không tạo job.
- **4a.** Không đủ số dư: `402` kèm số còn thiếu; gợi ý nạp tiền (UC-09.03) hoặc sinh lại từng tài sản.
- **5a.** Một số job lỗi sau retry: RELEASE tiền của chúng, liệt kê tài sản lỗi và cho phép thử lại riêng từng cái.
- ***a.** Đổi style sau khi đã có ảnh **không** tự sinh lại; hệ thống chỉ gợi ý hành động này kèm giá.

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
| Quan hệ | extend UC-04.02a, UC-04.02e |
| Truy vết | FR-WLD-04; BR-14; NFR-SEC-10; seq-the-gioi-truyen |
| Giai đoạn | P1 |

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
| Truy vết | FR-WLD-06; seq-tai-san-phong-cach |
| Giai đoạn | P1 |

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
| Truy vết | FR-WLD-07; BR-08; seq-tai-san-phong-cach |
| Giai đoạn | P1 |

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
| Truy vết | FR-WLD-08; seq-the-gioi-truyen |
| Giai đoạn | P2 ✂5 |

**Luồng chính**
1. Editor mở Story timeline.
2. Hệ thống hiển thị các mốc (nhãn ngày, mùa, chương, tóm tắt).
3. Editor bấm một mốc để mở chương tương ứng.

**Luồng thay thế / ngoại lệ**
- **2a.** Chưa có dữ liệu: hiện nút "Phân tích" (UC-04.09).
- **2b.** Editor đổi chế độ xem: "Theo mạch truyện" (thứ tự chương, mặc định) hoặc "Theo thứ tự thời gian" (sắp theo nhãn ngày/mùa, dùng cho truyện có hồi tưởng). Hệ thống sắp theo `chrono_index`; mốc chưa có (NULL) xếp cuối nhóm "Chưa xác định".

---

<a id="uc-0408"></a>
## UC-04.08 Xem đồ thị quan hệ

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Editor |
| Mô tả | Xem đồ thị quan hệ giữa các nhân vật và diễn biến; quan hệ thay đổi theo giai đoạn truyện (QĐ-143) |
| Tiền điều kiện | Đã chạy phân tích |
| Hậu điều kiện | **Thành công:** hiển thị đồ thị |
| Kích hoạt | Mở `?v=relationships` |
| Quan hệ | được mở rộng bởi UC-04.09 |
| Truy vết | FR-WLD-09; IC-14, IC-19; seq-the-gioi-truyen |
| Giai đoạn | P2 ✂4 |

**Luồng chính**
1. Editor mở Relationship graph.
2. Hệ thống vẽ nút (nhân vật) và cạnh (nhãn quan hệ, diễn biến, chương bắt đầu) **hiệu lực ở chương đang chọn** trên thanh chọn chương (mặc định chương cuối).
3. Editor kéo thanh chọn chương; cạnh đổi theo giai đoạn của từng cặp.
4. Editor bấm một cạnh để đọc diễn biến và các giai đoạn trước của cặp đó (chương bắt đầu, nhãn).

**Luồng thay thế / ngoại lệ**
- **2a.** Cặp chưa có giai đoạn nào bắt đầu trước chương đang chọn: không vẽ cạnh của cặp đó.

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
| Truy vết | FR-WLD-08, FR-WLD-09; BR-01, BR-02; IC-19; 08 §3.2 (`STORY_META`); seq-the-gioi-truyen |
| Giai đoạn | P2 ✂4 ✂5 |

**Luồng chính**
1. Editor bấm "Re-analyse".
2. Hệ thống hiện giá ước tính; Editor xác nhận; hệ thống giữ tiền (UC-05.17) và tạo job `STORY_META`; LLM trả mốc thời gian theo chương (kèm thứ hạng thời gian trong truyện, lưu `chrono_index`) và cặp quan hệ (theo tên/bí danh tài sản) kèm chương bắt đầu.
3. Hệ thống hợp nhất quan hệ theo thứ tự chương: cùng cặp, nhãn không đổi thì giữ giai đoạn trước; nhãn đổi thì tạo giai đoạn mới bắt đầu từ chương đó (QĐ-143, IC-19).
4. Hệ thống thay dữ liệu cũ, hiển thị kết quả.

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
| Truy vết | FR-WLD-10; BR-08; seq-tai-san-phong-cach |
| Giai đoạn | P1 |

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
| Giai đoạn | Sau |

**Luồng chính**
1. Editor bấm "Export assets".
2. Hệ thống tạo job `EXPORT_ZIP` (miễn phí), đặt tên file theo loại/tên tài sản.
3. Khi xong, hệ thống cung cấp link tải.

**Luồng thay thế / ngoại lệ**
- **1a.** Chưa có ảnh nào: báo "No generated asset images to export yet".
