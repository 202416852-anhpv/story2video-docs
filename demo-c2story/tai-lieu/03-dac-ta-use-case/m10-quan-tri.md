# M10 — Quản trị

> Sơ đồ: `../../so-do/01-use-case/phan-ra/uc-m10-quan-tri.puml`. Yêu cầu: FR-ADM-01..07, FR-AUTH-11. Tác nhân chính của mọi use case: **Admin** (vai trò lấy từ claim SSO hoặc danh sách cục bộ, FR-AUTH-07). Mọi thay đổi cấu hình và số dư đều ghi audit log (UC-10.09).
> **MVP không có giao diện quản trị** (QĐ-04): bảng giá, provider, style, giọng và `system_settings` nạp từ file seed (`pnpm seed`); danh sách mời quản lý bằng CLI (UC-10.11). Các bước "mở `/admin/...`" dưới đây mô tả giao diện sau MVP; trong MVP Admin sửa file seed rồi chạy lại lệnh nạp, hệ thống vẫn kiểm tra và ghi audit như nhau.

---

<a id="uc-1001"></a>
## UC-10.01 Cấu hình bảng giá

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Admin |
| Mô tả | Đặt công thức giá cho từng loại thao tác AI (storyboard, ảnh, sửa ảnh, TTS…): hệ số trên chi phí thực (mặc định 1,10), đơn giá provider và giới hạn đầu ra dùng để ước tính |
| Tiền điều kiện | Là Admin |
| Hậu điều kiện | **Thành công:** `price_rules` phiên bản mới với ngày hiệu lực; job tạo trước đó giữ giá cũ |
| Kích hoạt | MVP: sửa `seed/price-rules.yaml` và chạy `pnpm seed`. Sau MVP: mở `/admin/price-rules` |
| Quan hệ | include UC-10.09 |
| Truy vết | FR-ADM-01; BR-01; 08 §3 |
| Giai đoạn | P1 |

**Luồng chính**
1. Admin xem bảng giá hiện hành cùng chi phí AI thực tế trung bình (từ `ai_usage_records`) và tỷ lệ job bị trừ kịch số đã giữ (ước tính thấp).
2. Admin sửa công thức hoặc giới hạn đầu ra của một thao tác, đặt ngày hiệu lực.
3. Hệ thống kiểm tra công thức, lưu phiên bản mới, thực hiện UC-10.09.

**Luồng thay thế / ngoại lệ**
- **2a.** Hệ số nhỏ hơn 1,00 (bán dưới chi phí thực): cảnh báo, yêu cầu xác nhận lần hai.

---

<a id="uc-1002"></a>
## UC-10.02 Cấu hình gói đăng ký

| Mục | Nội dung |
|---|---|
| Tác nhân chính / phụ | Admin / Payment Gateway |
| Mô tả | *(Sau MVP)* Tạo/sửa gói (giá, quyền lợi), đồng bộ price id với cổng |
| Tiền điều kiện | Là Admin |
| Hậu điều kiện | **Thành công:** `plans` cập nhật, khớp với cổng |
| Kích hoạt | Mở `/admin/plans` |
| Truy vết | FR-ADM-02 |
| Giai đoạn | Sau |

**Luồng chính**
1. Admin sửa gói.
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
| Mô tả | Bật/tắt provider (LLM, Image, TTS, STT, Aligner), chọn adapter thật hay mock, thứ tự ưu tiên, mô hình cho người dùng chọn, chi phí đơn vị |
| Tiền điều kiện | Là Admin; secret của provider đã có trong secret manager |
| Hậu điều kiện | **Thành công:** `ai_providers`/`ai_models` cập nhật; ProviderRouter dùng cấu hình mới |
| Kích hoạt | MVP: `seed/ai-providers.yaml` + `pnpm seed`. Sau MVP: mở `/admin/ai-providers` |
| Truy vết | FR-ADM-03; ADR-03 |
| Giai đoạn | P1 |

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
| Kích hoạt | MVP: `seed/styles.yaml` + `pnpm seed`. Sau MVP: mở `/admin/styles` |
| Truy vết | FR-ADM-03 |
| Giai đoạn | P1 |

**Luồng chính**
1. Admin tạo hoặc sửa style, sinh ảnh mẫu thử.
2. Admin kích hoạt; style xuất hiện trong Styles Library.

---

<a id="uc-1005"></a>
## UC-10.05 Quản lý danh mục giọng đọc

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Admin |
| Mô tả | Quản lý giọng TTS cho người dùng chọn (ngôn ngữ, giới tính, audio mẫu); giọng được chọn ở P0 theo WER trên golden set |
| Tiền điều kiện | Là Admin; provider TTS đang bật |
| Hậu điều kiện | **Thành công:** `voices` cập nhật |
| Kích hoạt | MVP: `seed/voices.yaml` + `pnpm seed`. Sau MVP: mở `/admin/voices` |
| Truy vết | FR-ADM-03 |
| Giai đoạn | P1 |

**Luồng chính**
1. Admin đồng bộ danh sách giọng từ provider hoặc thêm thủ công.
2. Admin sinh audio mẫu (câu chuẩn tiếng Việt/Anh), đánh giá WER mẫu.
3. Admin bật giọng (gán cho gói tiêu chuẩn / cao cấp: sau MVP).

**Luồng thay thế / ngoại lệ**
- **2a.** WER mẫu > 3%: cảnh báo, không khuyến nghị bật.

---

<a id="uc-1006"></a>
## UC-10.06 Quản lý thư viện nhạc & SFX có license

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Admin |
| Mô tả | *(Sau MVP)* Nhập bộ nhạc nền, SFX CC0/CC-BY tuyển chọn (Pixabay, Freesound) kèm thông tin license và dòng ghi công |
| Tiền điều kiện | Là Admin; có quyền sử dụng hợp lệ |
| Hậu điều kiện | **Thành công:** `audio_assets` (owner `SYSTEM`) cập nhật, tìm được trong UC-06.11 |
| Kích hoạt | Mở `/admin/audio-library` |
| Truy vết | FR-ADM-03; BR-26; C-04 |
| Giai đoạn | Sau |

**Luồng chính**
1. Admin tải lên (đơn lẻ hoặc theo lô) file nhạc/SFX.
2. Admin nhập tiêu đề, loại, thể loại, tâm trạng, tag, nguồn, loại license (CC0 / CC-BY) và tác giả cần ghi công.
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
| Truy vết | FR-ADM-04 (sau MVP; trong MVP xem bằng BullMQ dashboard và log) |
| Giai đoạn | Sau |

**Luồng chính**
1. Admin lọc job (trạng thái, loại, provider, thời gian, người dùng, dự án).
2. Hệ thống hiển thị danh sách, độ dài hàng đợi, tỷ lệ lỗi.
3. Admin mở một job: tham số, kết quả, mã lỗi, số lần thử, `ai_usage_records`, số đã giữ, đã trừ, đã hoàn.

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
| Truy vết | FR-ADM-04; BR-18; WR-08; UC-10.09; API 2.9 `/admin/jobs:retry` |
| Giai đoạn | Sau |

**Luồng chính**
1. Admin mở job `FAILED` (UC-10.07 bước 3) và bấm "Retry".
2. Admin chọn cách tính tiền: như thao tác thường (trừ ví người dùng) hoặc miễn phí vì "Do lỗi hệ thống", kèm lý do.
3. Hệ thống tạo job mới cùng loại, đối tượng và tham số, với `Idempotency-Key` mới.
4. Chế độ thường: hệ thống giữ tiền của người dùng (UC-05.17). Chế độ miễn phí: không giữ tiền; chi phí vẫn tính vào trần chi tiêu ngày (BR-29).
5. Hệ thống thực hiện UC-10.09 (audit) trong cùng giao dịch và đưa job vào hàng đợi.

**Luồng thay thế / ngoại lệ**
- **1a.** Job không ở `FAILED`: ẩn nút Retry.
- **2a.** Job gốc lỗi do `CONTENT_POLICY`: cảnh báo nội dung đã bị moderation chặn; chạy lại có thể lỗi lại (BR-18) [ĐX].
- **4a.** Chế độ thường nhưng người dùng không đủ số dư: `402`; Admin chuyển sang miễn phí hoặc hủy.
- **3a.** Đối tượng đích đã đổi (chương đã sửa, shot đã xóa, `source_hash` lệch): job mới kết thúc `OUTDATED` hoặc bị từ chối `422`.

### UC-10.07b Hoàn tiền thủ công
<a id="uc-1007b"></a>

| Mục | Nội dung |
|---|---|
| Loại | extend của UC-10.07; include UC-10.09 |
| Tác nhân | Admin |
| Mô tả | Hoàn tiền cho một job đã trừ tiền nhưng kết quả hỏng |
| Tiền điều kiện | Là Admin; job đã CAPTURE chi phí thực × 110% |
| Hậu điều kiện | **Thành công:** sổ cái có bút toán `ADJUST` dương; người dùng được hoàn tiền; có audit log. **Tối thiểu:** không hoàn nhiều hơn số đã trừ |
| Kích hoạt | Bấm "Hoàn tiền" trong chi tiết job |
| Truy vết | FR-ADM-04, FR-ADM-05; WR-04, WR-08; UC-10.09; API 2.9 `/admin/jobs:refund` |
| Giai đoạn | Sau |

**Luồng chính**
1. Admin mở job đã CAPTURE (UC-10.07 bước 3) và bấm "Hoàn tiền".
2. Admin nhập số tiền (mặc định bằng `charged_micro`, không vượt số đã trừ) và **lý do bắt buộc**.
3. Hệ thống ghi `wallet_ledger_entries` `ADJUST` dương, kèm `reason`, `actor_id`, `job_id`.
4. Hệ thống cập nhật `wallets` cùng giao dịch và thực hiện UC-10.09.
5. Hệ thống thông báo cho người dùng.

**Luồng thay thế / ngoại lệ**
- **2a.** Tổng số đã hoàn cho job này cộng số mới vượt số đã trừ: chặn để không hoàn trùng [ĐX].
- **4a.** Không ghi được audit: rollback cả hoàn tiền (UC-10.09 nhánh 2a).

---

<a id="uc-1008"></a>
## UC-10.08 Điều chỉnh số dư người dùng

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Admin |
| Mô tả | Cộng hoặc trừ số dư ví của người dùng (bồi thường, xử lý gian lận) |
| Tiền điều kiện | Là Admin |
| Hậu điều kiện | **Thành công:** sổ cái có `ADJUST` kèm `reason` và `actor_id`; số dư cập nhật; `topup_total_micro` không đổi (điều chỉnh không làm tài khoản thành "Đã nạp tiền") |
| Kích hoạt | Mở hồ sơ người dùng trong `/admin/users` |
| Quan hệ | include UC-10.09 |
| Truy vết | FR-ADM-05; WR-08 |
| Giai đoạn | Sau |

**Luồng chính**
1. Admin tìm người dùng (email, `sso_subject`).
2. Admin nhập số tiền (±) và **lý do bắt buộc**.
3. Hệ thống ghi `ADJUST`, cập nhật số dư, thực hiện UC-10.09, thông báo cho người dùng.

**Luồng thay thế / ngoại lệ**
- **2a.** Trừ làm số dư âm: chặn, trừ khi Admin chọn "Xử lý chargeback" (WR-07).

---

<a id="uc-1009"></a>
## UC-10.09 Ghi audit log

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Hệ thống (được include) |
| Mức | Chức năng con |
| Mô tả | Ghi lại mọi hành động quản trị: thay đổi cấu hình, danh sách mời, điều chỉnh số dư |
| Tiền điều kiện | Có hành động cần kiểm toán |
| Hậu điều kiện | **Thành công:** bản ghi bất biến: ai, khi nào, đối tượng, giá trị trước/sau, lý do, IP. Giữ 2 năm |
| Kích hoạt | UC-10.01, UC-10.07b, UC-10.08, UC-10.11, UC-10.12 và mọi thay đổi cấu hình |
| Truy vết | NFR-PRV-04 |
| Giai đoạn | P1 |

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
| Mô tả | Báo cáo chi tiêu, tiền nạp (sandbox), chi phí AI theo provider, biên lợi nhuận, tỷ lệ job lỗi, chỉ số luồng (số chương "Sẵn sàng dựng", số video xuất) |
| Tiền điều kiện | Là Admin |
| Hậu điều kiện | **Thành công:** hiển thị báo cáo theo khoảng thời gian; tải CSV |
| Kích hoạt | Mở `/admin/reports` |
| Truy vết | FR-ADM-06; BO-01..06 |
| Giai đoạn | Sau |

**Luồng chính**
1. Admin chọn báo cáo và khoảng thời gian.
2. Hệ thống tổng hợp từ ledger, `payments`, `ai_usage_records`, `jobs`, `renders`.
3. Admin xem biểu đồ, bảng, tải CSV.

---

<a id="uc-1011"></a>
## UC-10.11 Quản lý danh sách mời beta

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Admin |
| Mô tả | Thêm, gỡ và xem email được mời tham gia closed beta; chỉ email trong danh sách mới tạo được hồ sơ (BR-30) |
| Tiền điều kiện | Là Admin; truy cập được môi trường chạy lệnh quản trị |
| Hậu điều kiện | **Thành công:** `beta_invites` cập nhật; có audit log. **Tối thiểu:** gỡ lời mời không xóa hồ sơ đã tạo |
| Kích hoạt | MVP: lệnh `pnpm admin:invites add\|remove\|list <email> [--note]`. Sau MVP: `/admin/invites` |
| Quan hệ | include UC-10.09 |
| Truy vết | FR-AUTH-11; BR-30; QĐ-25; 04 §3.1 `beta_invites` |
| Giai đoạn | P0 |

**Luồng chính**
1. Admin chạy `add` với một hoặc nhiều email (hoặc file CSV), kèm ghi chú (ví dụ "nhóm khảo sát 1").
2. Hệ thống chuẩn hóa email (bỏ khoảng trắng, chữ thường), kiểm tra định dạng, tạo `beta_invites` cho email chưa có.
3. Hệ thống thực hiện UC-10.09 và in kết quả: số email thêm mới, số đã có, số lỗi.
4. Admin gửi lời mời cho người dùng qua kênh riêng (email, nhóm chat) kèm link ứng dụng.
5. Lệnh `list` hiển thị email, ngày mời, đã tạo hồ sơ chưa (`used_by_user_id`), đã thu hồi chưa.

**Luồng thay thế / ngoại lệ**
- **2a.** Email sai định dạng: bỏ qua email đó, báo trong kết quả.
- **2b.** Email đã có và đang hiệu lực: không tạo trùng.
- **2c.** Email đã bị thu hồi trước đó: `add` mở lại lời mời (xóa `revoked_at`).
- **\*a.** `remove`: đặt `revoked_at`; người chưa tạo hồ sơ không vào được nữa; người đã có hồ sơ vẫn đăng nhập được (BR-30). Muốn chặn hẳn thì Admin khóa hồ sơ (`users.status = LOCKED`).
- **\*b.** Kết thúc beta, mở rộng: Admin đặt `system_settings.beta_invite_only = false`.

---

<a id="uc-1012"></a>
## UC-10.12 Áp trần chi tiêu AI hằng ngày

| Mục | Nội dung |
|---|---|
| Tác nhân chính / phụ | Hệ thống (`BudgetGuard`, Scheduler) / Admin, Email service |
| Mức | Chức năng con |
| Mô tả | Giữ tổng chi phí AI thật của toàn hệ thống trong một ngày không vượt trần (closed beta: $10); chạm trần thì tạm dừng job mới và báo Admin |
| Tiền điều kiện | `system_settings.daily_ai_budget_usd` đã cấu hình |
| Hậu điều kiện | **Thành công:** tại mọi thời điểm `spent + reserved ≤ cap` của ngày (IC-18), kể cả khi nhiều yêu cầu đồng thời; chi phí thực chỉ có thể vượt trần một lượng bằng phần các job đang chạy tốn hơn ước tính; Admin nhận đúng một cảnh báo cho mỗi ngưỡng mỗi ngày. **Tối thiểu:** job đang chạy không bị hủy giữa chừng |
| Kích hoạt | Mỗi lần tạo job tốn phí (UC-05.17 bước 3); Scheduler chạy mỗi 5 phút |
| Quan hệ | được include bởi UC-05.17 |
| Truy vết | FR-ADM-07; BR-29; IC-18; ADR-25; QĐ-39; NFR-COST-02; 04 `daily_ai_budgets`; API `503 DAILY_BUDGET_EXCEEDED` |
| Giai đoạn | P2 |

**Luồng chính**
1. Khi có yêu cầu tạo job tốn phí, trong giao dịch của UC-05.17, `BudgetGuard` tạo dòng `daily_ai_budgets` của hôm nay nếu chưa có (`cap_micro` lấy từ `system_settings`), rồi chạy **một câu** `UPDATE … SET reserved_micro = reserved_micro + x WHERE day = hôm nay AND spent_micro + reserved_micro + x <= cap_micro` với `x` là chi phí provider ước tính.
2. Câu lệnh trúng một dòng: chỗ đã được giữ, UC-05.17 tiếp bước 4. Khóa dòng của `UPDATE` bảo đảm các yêu cầu đồng thời được xếp hàng, không thể cùng vượt trần.
3. Khi job kết thúc: `reserved −= x`, `spent += chi phí thực` (UC-05.17 bước 5–6).
4. Scheduler mỗi 5 phút đọc dòng của hôm nay; `spent + reserved ≥ 80%` trần và `alert_80_sent_at` rỗng thì gửi email cảnh báo sớm và ghi thời điểm; chạm trần thì làm tương tự với `alert_100_sent_at`.
5. Sang ngày mới (00:00 giờ Việt Nam) dùng dòng mới; job tạo hôm trước vẫn trả chỗ vào dòng của ngày tạo (`jobs.budget_day`).
6. Reconciler hằng ngày đối chiếu `spent_micro` với Σ `ai_usage_records.cost_usd` của ngày; lệch thì sửa và cảnh báo.

**Luồng thay thế / ngoại lệ**
- **2a.** Câu lệnh không trúng dòng nào (vượt trần): ROLLBACK, `503 DAILY_BUDGET_EXCEEDED`; giao diện hiện "Hệ thống tạm dừng tác vụ AI mới đến 00:00 do đạt giới hạn chi phí trong ngày"; email cho Admin (một lần, theo `alert_100_sent_at`) kèm tổng chi phí và 5 người dùng chi nhiều nhất.
- **2b.** Thao tác miễn phí (render, chỉnh sửa, tải lên): không bị ảnh hưởng.
- **\*a.** Admin nâng trần tạm thời: sửa `daily_ai_budget_usd` (seed hoặc CLI); lệnh đồng thời cập nhật `cap_micro` của dòng hôm nay nên có hiệu lực ngay; ghi audit (UC-10.09).
