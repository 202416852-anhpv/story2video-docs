# M10 — Quản trị

> Sơ đồ: `../../so-do/01-use-case/phan-ra/uc-m10-quan-tri.puml`. Yêu cầu: FR-ADM-01..06. Tác nhân chính của mọi use case: **Admin** (vai trò lấy từ claim SSO hoặc danh sách cục bộ, FR-AUTH-07). Mọi thay đổi cấu hình và credit đều ghi audit log (UC-10.09).

---

<a id="uc-1001"></a>
## UC-10.01 Cấu hình bảng giá credit

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Admin |
| Mô tả | Đặt giá credit cho từng loại thao tác (ảnh, sửa ảnh, TTS, AI âm thanh…) |
| Tiền điều kiện | Là Admin |
| Hậu điều kiện | **Thành công:** `price_rules` phiên bản mới với ngày hiệu lực; job tạo trước đó giữ giá cũ |
| Kích hoạt | Mở `/admin/price-rules` |
| Quan hệ | include UC-10.09 |
| Truy vết | FR-ADM-01; 08 §3 |

**Luồng chính**
1. Admin xem bảng giá hiện hành cùng chi phí AI thực tế trung bình (từ `ai_usage_records`) và biên lợi nhuận.
2. Admin sửa giá/công thức một thao tác, đặt ngày hiệu lực.
3. Hệ thống kiểm tra công thức, lưu phiên bản mới, thực hiện UC-10.09.

**Luồng thay thế / ngoại lệ**
- **2a.** Giá mới làm biên lợi nhuận âm: cảnh báo, yêu cầu xác nhận lần hai.

---

<a id="uc-1002"></a>
## UC-10.02 Cấu hình gói & credit pack

| Mục | Nội dung |
|---|---|
| Tác nhân chính / phụ | Admin / Payment Gateway |
| Mô tả | Tạo/sửa gói (giá, credit/tháng, quyền lợi) và pack, đồng bộ price id với cổng |
| Tiền điều kiện | Là Admin |
| Hậu điều kiện | **Thành công:** `plans`/`credit_packs` cập nhật, khớp với cổng |
| Kích hoạt | Mở `/admin/plans` |
| Truy vết | FR-ADM-02 |

**Luồng chính**
1. Admin sửa gói hoặc pack.
2. Hệ thống tạo/cập nhật price tương ứng trên cổng, lưu `gateway_price_ids`.
3. Pricing hiển thị cấu hình mới; ghi audit log.

**Luồng thay thế / ngoại lệ**
- **2a.** Đổi giá gói đang có người đăng ký: tạo price mới cho người đăng ký mới; người cũ giữ giá cũ đến khi được di chuyển có chủ đích.

---

<a id="uc-1003"></a>
## UC-10.03 Quản lý provider & mô hình AI

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Admin |
| Mô tả | Bật/tắt provider (LLM, Image, TTS, STT, Aligner, Music), thứ tự ưu tiên, mô hình cho người dùng chọn, chi phí đơn vị |
| Tiền điều kiện | Là Admin; secret của provider đã có trong secret manager |
| Hậu điều kiện | **Thành công:** `ai_providers`/`ai_models` cập nhật; ProviderRouter dùng cấu hình mới |
| Kích hoạt | Mở `/admin/ai-providers` |
| Truy vết | FR-ADM-03; ADR-03 |

**Luồng chính**
1. Admin xem danh sách provider: trạng thái, tỷ lệ lỗi, độ trễ, chi phí 24 giờ.
2. Admin bật/tắt, đổi thứ tự ưu tiên, nhập **tên** secret (không nhập key).
3. Admin bấm "Kiểm tra kết nối"; hệ thống gọi thử.
4. Hệ thống lưu, ghi audit log.

**Luồng thay thế / ngoại lệ**
- **3a.** Kiểm tra thất bại: không cho bật provider.
- **2a.** Tắt provider đang là duy nhất của một loại: chặn.

---

<a id="uc-1004"></a>
## UC-10.04 Quản lý danh mục style

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Admin |
| Mô tả | Thêm/sửa/ẩn style nghệ thuật (tên, mô tả, đoạn prompt, ảnh mẫu) |
| Tiền điều kiện | Là Admin |
| Hậu điều kiện | **Thành công:** `styles` cập nhật; dự án đang dùng style bị ẩn không bị ảnh hưởng |
| Kích hoạt | Mở `/admin/styles` |
| Truy vết | FR-ADM-03 |

**Luồng chính**
1. Admin tạo hoặc sửa style, sinh ảnh mẫu thử.
2. Admin kích hoạt; style xuất hiện trong Styles Library.

---

<a id="uc-1005"></a>
## UC-10.05 Quản lý danh mục giọng đọc

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Admin |
| Mô tả | Quản lý giọng TTS cho người dùng chọn (ngôn ngữ, giới tính, audio mẫu, gói được dùng) |
| Tiền điều kiện | Là Admin; provider TTS đang bật |
| Hậu điều kiện | **Thành công:** `voices` cập nhật |
| Kích hoạt | Mở `/admin/voices` |
| Truy vết | FR-ADM-03 |

**Luồng chính**
1. Admin đồng bộ danh sách giọng từ provider hoặc thêm thủ công.
2. Admin sinh audio mẫu (câu chuẩn tiếng Việt/Anh), đánh giá WER mẫu.
3. Admin bật giọng, gán cho gói (tiêu chuẩn / cao cấp).

**Luồng thay thế / ngoại lệ**
- **2a.** WER mẫu > 3%: cảnh báo, không khuyến nghị bật.

---

<a id="uc-1006"></a>
## UC-10.06 Quản lý thư viện nhạc & SFX có license

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Admin |
| Mô tả | Nhập và quản lý nhạc nền, SFX của hệ thống kèm thông tin license |
| Tiền điều kiện | Là Admin; có quyền sử dụng hợp lệ |
| Hậu điều kiện | **Thành công:** `audio_assets` (owner `SYSTEM`) cập nhật, tìm được trong UC-06.11 |
| Kích hoạt | Mở `/admin/audio-library` |
| Truy vết | FR-ADM-03; BR-26; C-04 |

**Luồng chính**
1. Admin tải lên (đơn lẻ hoặc theo lô) file nhạc/SFX.
2. Admin nhập tiêu đề, loại, thể loại, tâm trạng, tag, nguồn license và điều khoản.
3. Hệ thống tạo waveform, chuẩn hóa loudness bản nghe thử, xuất bản vào thư viện.
4. Admin có thể gỡ một mục; timeline đang dùng mục đó được cảnh báo.

**Luồng thay thế / ngoại lệ**
- **2a.** Thiếu thông tin license: không cho xuất bản.

---

<a id="uc-1007"></a>
## UC-10.07 Giám sát job

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Admin |
| Mô tả | Theo dõi job theo trạng thái, loại, provider, người dùng; xem lỗi |
| Tiền điều kiện | Là Admin |
| Hậu điều kiện | **Thành công:** hiển thị job và chi tiết |
| Kích hoạt | Mở `/admin/jobs` |
| Quan hệ | được mở rộng bởi UC-10.07a, UC-10.07b |
| Truy vết | FR-ADM-04 |

**Luồng chính**
1. Admin lọc job (trạng thái, loại, provider, thời gian, người dùng, dự án).
2. Hệ thống hiển thị danh sách, độ dài hàng đợi, tỷ lệ lỗi.
3. Admin mở một job: tham số, kết quả, mã lỗi, số lần thử, `ai_usage_records`, bút toán credit.

### UC-10.07a Chạy lại job
<a id="uc-1007a"></a>

| Mục | Nội dung |
|---|---|
| Loại | extend của UC-10.07 |
| Tác nhân | Admin |
| Mô tả | Chạy lại một job đã lỗi với cùng tham số, có thể miễn phí khi lỗi do hệ thống |
| Tiền điều kiện | Là Admin; job ở trạng thái `FAILED` |
| Hậu điều kiện | **Thành công:** có job mới vào hàng đợi; hành động được ghi audit log. **Tối thiểu:** job gốc và bút toán của nó không bị sửa |
| Kích hoạt | Bấm "Retry" trong chi tiết job |
| Truy vết | FR-ADM-04; BR-18; CR-08; UC-10.09; API 2.9 `/admin/jobs:retry` |

**Luồng chính**
1. Admin mở job `FAILED` (UC-10.07 bước 3) và bấm "Retry".
2. Admin chọn cách tính credit: như thao tác thường (trừ ví người dùng) hoặc miễn phí vì "Do lỗi hệ thống", kèm lý do.
3. Hệ thống tạo job mới cùng loại, đối tượng và tham số, với `Idempotency-Key` mới.
4. Chế độ thường: hệ thống giữ credit của người dùng (UC-05.17). Chế độ miễn phí: không giữ credit.
5. Hệ thống thực hiện UC-10.09 (audit) trong cùng giao dịch và đưa job vào hàng đợi.

**Luồng thay thế / ngoại lệ**
- **1a.** Job không ở `FAILED`: ẩn nút Retry.
- **2a.** Job gốc lỗi do `CONTENT_POLICY`: cảnh báo nội dung đã bị moderation chặn; chạy lại có thể lỗi lại (BR-18) [ĐX].
- **4a.** Chế độ thường nhưng người dùng không đủ credit: `402`; Admin chuyển sang miễn phí hoặc hủy.
- **3a.** Đối tượng đích đã đổi (chương đã sửa, shot đã xóa, `source_hash` lệch): job mới kết thúc `OUTDATED` hoặc bị từ chối `422`.

### UC-10.07b Hoàn credit thủ công
<a id="uc-1007b"></a>

| Mục | Nội dung |
|---|---|
| Loại | extend của UC-10.07; include UC-10.09 |
| Tác nhân | Admin |
| Mô tả | Hoàn credit cho một job đã trừ credit nhưng kết quả hỏng |
| Tiền điều kiện | Là Admin; job đã CAPTURE credit |
| Hậu điều kiện | **Thành công:** ledger có bút toán ADJUST dương vào đúng bucket; người dùng được hoàn credit; có audit log. **Tối thiểu:** không hoàn nhiều hơn số đã trừ |
| Kích hoạt | Bấm "Hoàn credit" trong chi tiết job |
| Truy vết | FR-ADM-04, FR-ADM-05; CR-04, CR-08; UC-10.09; API 2.9 `/admin/jobs:refund` |

**Luồng chính**
1. Admin mở job đã CAPTURE (UC-10.07 bước 3) và bấm "Hoàn credit".
2. Admin nhập số credit (mặc định bằng `credit_cost`, không vượt số đã trừ) và **lý do bắt buộc**.
3. Hệ thống ghi `credit_ledger_entries` ADJUST dương vào đúng bucket đã bị trừ, kèm `reason`, `actor_id`, `job_id`.
4. Hệ thống cập nhật `credit_balances` cùng giao dịch và thực hiện UC-10.09.
5. Hệ thống thông báo cho người dùng.

**Luồng thay thế / ngoại lệ**
- **2a.** Tổng số đã hoàn cho job này cộng số mới vượt số đã trừ: chặn để không hoàn trùng [ĐX].
- **3a.** Bucket gốc đã hết hạn: Admin chọn bucket thay thế (ví dụ `BONUS` kèm hạn dùng) [ĐX].
- **4a.** Không ghi được audit: rollback cả hoàn credit (UC-10.09 nhánh 2a).

---

<a id="uc-1008"></a>
## UC-10.08 Điều chỉnh credit người dùng

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Admin |
| Mô tả | Cộng hoặc trừ credit cho người dùng (khuyến mãi, bồi thường, xử lý gian lận) |
| Tiền điều kiện | Là Admin |
| Hậu điều kiện | **Thành công:** ledger ADJUST có `reason` và `actor_id`; số dư cập nhật |
| Kích hoạt | Mở hồ sơ người dùng trong `/admin/users` |
| Quan hệ | include UC-10.09 |
| Truy vết | FR-ADM-05; CR-08 |

**Luồng chính**
1. Admin tìm người dùng (email, `sso_subject`).
2. Admin nhập số credit (±), bucket, hạn dùng (với BONUS) và **lý do bắt buộc**.
3. Hệ thống ghi ledger ADJUST, cập nhật số dư, thực hiện UC-10.09, thông báo cho người dùng.

**Luồng thay thế / ngoại lệ**
- **2a.** Trừ làm số dư âm: chặn, trừ khi Admin chọn "Xử lý chargeback" (CR-07).

---

<a id="uc-1009"></a>
## UC-10.09 Ghi audit log

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Hệ thống (được include) |
| Mức | Chức năng con |
| Mô tả | Ghi lại mọi hành động quản trị và điều chỉnh credit |
| Tiền điều kiện | Có hành động cần kiểm toán |
| Hậu điều kiện | **Thành công:** bản ghi bất biến: ai, khi nào, đối tượng, giá trị trước/sau, lý do, IP. Giữ 2 năm |
| Kích hoạt | UC-10.01, UC-10.07b, UC-10.08 và mọi thay đổi cấu hình |
| Truy vết | NFR-PRV-04 |

**Luồng chính**
1. Use case gọi ghi audit trong cùng giao dịch với thay đổi.
2. Hệ thống lưu bản ghi chỉ thêm (append-only).

**Luồng thay thế / ngoại lệ**
- **2a.** Không ghi được audit: rollback cả thay đổi.

---

<a id="uc-1010"></a>
## UC-10.10 Xem báo cáo

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Admin |
| Mô tả | Báo cáo credit tiêu thụ, doanh thu, chi phí AI theo provider, biên lợi nhuận, tỷ lệ job lỗi, chỉ số luồng (số chương "Sẵn sàng dựng", số video xuất) |
| Tiền điều kiện | Là Admin |
| Hậu điều kiện | **Thành công:** hiển thị báo cáo theo khoảng thời gian; tải CSV |
| Kích hoạt | Mở `/admin/reports` |
| Truy vết | FR-ADM-06; BO-01..06 |

**Luồng chính**
1. Admin chọn báo cáo và khoảng thời gian.
2. Hệ thống tổng hợp từ ledger, `payments`, `ai_usage_records`, `jobs`, `renders`.
3. Admin xem biểu đồ, bảng, tải CSV.
