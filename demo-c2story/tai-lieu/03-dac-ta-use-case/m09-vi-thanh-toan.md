# M09 — Ví & thanh toán

> Sơ đồ: `../../so-do/01-use-case/phan-ra/uc-m09-vi-thanh-toan.puml`, `../../so-do/04-tuan-tu/seq-thanh-toan.puml`, `../../so-do/05-hoat-dong/act-giu-tru-tien.puml`, `../../so-do/06-trang-thai/state-subscription.puml` (sau MVP). Yêu cầu: FR-BIL-01..12. Quy tắc: BR-01, BR-02, BR-27, BR-28; quy tắc ví [08 §4](../08-quy-tac-nghiep-vu.md). Đơn vị tiền là **USD**, lưu micro-USD (QĐ-30). Thanh toán qua cổng (Stripe **test mode**, tài khoản của nhóm); hệ thống không lưu thẻ.

---

<a id="uc-0901"></a>
## UC-09.01 Xem bảng giá

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Guest |
| Mô tả | Xem cách tính giá, đơn giá tham khảo từng thao tác, giới hạn tài khoản Free và quyền lợi khi đã nạp tiền, FAQ |
| Tiền điều kiện | — |
| Hậu điều kiện | **Thành công:** hiển thị giá hiện hành từ cấu hình |
| Kích hoạt | Mở `/pricing` |
| Truy vết | FR-BIL-01; BR-01, BR-27, BR-28; 08 §3; API 2.8 `GET /pricing`; seq-thanh-toan, act-m09-vi-thanh-toan |
| Giai đoạn | P3 |

**Luồng chính**
1. Guest mở Pricing.
2. Hệ thống hiển thị: nguyên tắc "giá = chi phí thực của nhà cung cấp AI × 110%"; bảng đơn giá tham khảo theo thao tác (storyboard, ảnh, sửa ảnh, thuyết minh theo 1.000 ký tự) lấy từ `price_rules` và `ai_models`; ước lượng chi phí cho một chương mẫu 10.000 ký tự; so sánh **Free** (1 dự án, 3 chương, 3 lần render và 10 phút video mỗi tháng, 720p có watermark) và **Đã nạp tiền**; tiền dùng thử $2; FAQ.
3. Guest bấm "Bắt đầu" hoặc "Nạp tiền"; nếu chưa đăng nhập thì chuyển UC-01.01, sau đó tiếp UC-09.03.

**Luồng thay thế / ngoại lệ**
- **2a.** Người dùng chọn hiển thị VND: hệ thống quy đổi theo tỷ giá cấu hình (`system_settings.vnd_rate`), ghi chú "chỉ để tham khảo; thanh toán bằng USD".

---

<a id="uc-0902"></a>
## UC-09.02 Đăng ký gói

> **Sau MVP** (QĐ-35). MVP chỉ có hai trạng thái Free / Đã nạp tiền. Đặc tả giữ lại để làm hướng phát triển; quyền lợi gói cần định nghĩa lại theo mô hình tính phí thực tế.

| Mục | Nội dung |
|---|---|
| Tác nhân chính / phụ | User / Payment Gateway |
| Mô tả | Đăng ký gói tháng hoặc năm |
| Tiền điều kiện | Đã đăng nhập; chưa có gói trả phí đang hoạt động (đổi gói dùng UC-09.04) |
| Hậu điều kiện | **Thành công:** Subscription `ACTIVE`; quyền lợi gói có hiệu lực. **Tối thiểu:** không kích hoạt gói khi chưa nhận webhook thanh toán |
| Kích hoạt | Chọn gói trên Pricing |
| Quan hệ | include UC-09.03a |
| Truy vết | FR-BIL-02; seq-thanh-toan |
| Giai đoạn | Sau |

**Luồng chính**
1. User chọn gói và chu kỳ.
2. Hệ thống thực hiện **UC-09.03a**.
3. Sau khi cổng xác nhận, UC-09.08 cập nhật gói.
4. User quay lại Dashboard thấy gói mới.

**Luồng thay thế / ngoại lệ**
- **3a.** Webhook đến chậm: Dashboard hiện "Đang xử lý thanh toán" và tự làm mới qua SSE.

---

<a id="uc-0903"></a>
## UC-09.03 Nạp tiền vào ví

| Mục | Nội dung |
|---|---|
| Tác nhân chính / phụ | User / Payment Gateway (sandbox) |
| Mô tả | Nạp một số tiền USD vào ví để dùng cho các thao tác AI; lần nạp đầu chuyển tài khoản sang "Đã nạp tiền" |
| Tiền điều kiện | Đã đăng nhập và đã đồng ý xử lý dữ liệu |
| Hậu điều kiện | **Thành công:** `wallets.available_micro` và `topup_total_micro` tăng đúng số tiền; sổ cái có bút toán `TOPUP`; tài khoản ở trạng thái "Đã nạp tiền" (BR-27). **Tối thiểu:** không cộng tiền khi chưa có webhook xác nhận |
| Kích hoạt | Bấm "Nạp tiền" trên Pricing, Dashboard, hoặc từ thông báo thiếu số dư (`402`) hay vượt giới hạn Free (`403 FREE_LIMIT_REACHED`) |
| Quan hệ | include UC-09.03a |
| Truy vết | FR-BIL-03; BR-27; WR-06; API 2.8 `POST /billing/topup-sessions`; seq-thanh-toan, act-m09-vi-thanh-toan |
| Giai đoạn | P3 ✂1 |

**Luồng chính**
1. User chọn số tiền (gợi ý $2, $5, $10 hoặc nhập số khác).
2. Hệ thống thực hiện **UC-09.03a**.
3. UC-09.08 ghi bút toán `TOPUP`, cộng `available_micro` và `topup_total_micro`.
4. Hệ thống phát `wallet.updated`; nếu đây là lần nạp đầu, hiện "Tài khoản đã bỏ giới hạn Free. Video đã render trước đó vẫn có watermark; render lại để có bản không watermark."
5. Nếu User đến từ thông báo thiếu số dư hoặc vượt giới hạn, hệ thống đưa User về đúng thao tác đang dở.

**Luồng thay thế / ngoại lệ**
- **1a.** Số tiền ngoài khoảng $1–$100: báo lỗi, không tạo phiên thanh toán [ĐX].

### UC-09.03a Thanh toán qua checkout
<a id="uc-0903a"></a>

| Mục | Nội dung |
|---|---|
| Loại | include của UC-09.03 (và UC-09.02, sau MVP) |
| Tác nhân | User / Payment Gateway (Stripe Checkout, test mode) |
| Mô tả | Đưa User sang trang thanh toán của cổng để trả tiền; ứng dụng không bao giờ nhận hay lưu thông tin thẻ |
| Tiền điều kiện | Đã đăng nhập; số tiền hợp lệ |
| Hậu điều kiện | **Thành công:** User hoàn tất thanh toán trên cổng và cổng phát webhook cho UC-09.08. **Tối thiểu:** hủy hoặc thất bại thì không có thay đổi nào về ví |
| Kích hoạt | UC-09.03 bước 2 |
| Truy vết | ADR-08; FR-BIL-03; NFR-SEC-07; API 2.8 `POST /billing/topup-sessions`; seq-thanh-toan |
| Giai đoạn | P3 ✂1 |

**Luồng chính**
1. Client gọi `POST /billing/topup-sessions` với `{amountUsd}`.
2. Hệ thống kiểm tra số tiền, tạo (nếu chưa có) khách hàng ở cổng và lưu `users.gateway_customer_id`.
3. Hệ thống tạo `payments (kind = TOPUP, status = PENDING)` và Checkout Session dạng thanh toán một lần với `client_reference_id = userId`, `metadata.paymentId`, số tiền tương ứng, `success_url` và `cancel_url`.
4. API trả `{ url }`; client chuyển hướng trình duyệt tới trang thanh toán của cổng (môi trường sandbox, dùng thẻ thử).
5. User thanh toán; cổng chuyển về `success_url` (Dashboard hiện "Đang xử lý thanh toán").
6. Cổng phát webhook; UC-09.08 cộng tiền vào ví.

**Luồng thay thế / ngoại lệ**
- **4a.** Cổng không phản hồi: báo lỗi; `payments` giữ `PENDING` rồi hết hạn, không cộng tiền.
- **5a.** User hủy: cổng chuyển về `cancel_url`; không có thay đổi.
- **5b.** Thanh toán thất bại tại cổng: User ở lại trang của cổng để thử lại.
- **6a.** Webhook đến chậm: không cộng tiền trước khi webhook xử lý xong.

---

<a id="uc-0904"></a>
## UC-09.04 Quản lý thanh toán

> **Sau MVP** (đi cùng gói đăng ký, UC-09.02).

| Mục | Nội dung |
|---|---|
| Tác nhân chính / phụ | User / Payment Gateway |
| Mô tả | Nâng/hạ gói, đổi thẻ, xem hóa đơn, hủy gói qua cổng |
| Tiền điều kiện | Có khách hàng trên cổng |
| Hậu điều kiện | **Thành công:** thay đổi được đồng bộ qua webhook (UC-09.08) |
| Kích hoạt | "Manage Billing" |
| Truy vết | FR-BIL-04; seq-thanh-toan |
| Giai đoạn | Sau |

**Luồng chính**
1. User bấm "Manage Billing".
2. Hệ thống tạo phiên customer portal và chuyển hướng.
3. User thực hiện thay đổi trên trang của cổng.
4. Webhook cập nhật Subscription (UC-09.08).

**Luồng thay thế / ngoại lệ**
- **3a.** Hủy gói: hiệu lực cuối kỳ (`CANCEL_AT_PERIOD_END`).
- **3b.** Hạ gói: áp dụng từ kỳ sau.

---

<a id="uc-0905"></a>
## UC-09.05 Xem số dư ví

| Mục | Nội dung |
|---|---|
| Tác nhân chính | User |
| Mô tả | Xem số dư khả dụng, phần đang giữ cho job đang chạy, trạng thái tài khoản và phần Free đã dùng trong tháng |
| Tiền điều kiện | Đã đăng nhập |
| Hậu điều kiện | **Thành công:** số liệu khớp `wallets` và sổ cái |
| Kích hoạt | Badge số dư ở thanh trên, hoặc Dashboard |
| Truy vết | FR-BIL-05, FR-BIL-12; BR-27; API 2.8 `GET /me/wallet`; seq-thanh-toan, act-m09-vi-thanh-toan |
| Giai đoạn | P2 |

**Luồng chính**
1. User bấm badge số dư.
2. Hệ thống hiển thị: số dư khả dụng (USD, 4 chữ số thập phân khi < $1), đang giữ, trạng thái Free / Đã nạp tiền; với Free thêm phần đã dùng trong tháng (số lần render, phút video) và nút "Nạp tiền".
3. Số dư tự cập nhật qua sự kiện `wallet.updated` khi job giữ, trừ hoặc hoàn tiền.

**Luồng thay thế / ngoại lệ**
- **2a.** Số dư khả dụng dưới giá ước tính của một chương mẫu: hiện gợi ý nạp thêm.

---

<a id="uc-0906"></a>
## UC-09.06 Xem lịch sử chi tiêu

| Mục | Nội dung |
|---|---|
| Tác nhân chính | User |
| Mô tả | Xem sổ cái ví, lọc theo dự án và loại thao tác, thấy rõ chi phí thực và phí 10% |
| Tiền điều kiện | Đã đăng nhập |
| Hậu điều kiện | **Thành công:** hiển thị các bút toán (append-only) |
| Kích hoạt | "Lịch sử chi tiêu" |
| Truy vết | FR-BIL-06, 08; API 2.8 `GET /me/wallet/ledger`; seq-thanh-toan, act-m09-vi-thanh-toan |
| Giai đoạn | P3 |

**Luồng chính**
1. User mở lịch sử.
2. Hệ thống liệt kê bút toán: thời gian, loại (`TRIAL_GRANT`, `TOPUP`, `HOLD`, `CAPTURE`, `RELEASE`), số tiền, dự án, thao tác; mỗi job hiển thị một dòng gộp "giữ $x → trừ $y (chi phí thực $z + phí 10%) → hoàn $x−y".
3. User lọc theo dự án, loại thao tác, khoảng thời gian; xem tổng.

---

<a id="uc-0908"></a>
## UC-09.08 Xử lý webhook thanh toán

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Payment Gateway |
| Mô tả | Nhận sự kiện thanh toán và cập nhật ví (và gói, sau MVP) một cách idempotent |
| Tiền điều kiện | Webhook có chữ ký hợp lệ |
| Hậu điều kiện | **Thành công:** mỗi event xử lý đúng một lần. **Tối thiểu:** event trùng hoặc sai chữ ký không làm thay đổi dữ liệu |
| Kích hoạt | `POST /webhooks/stripe` |
| Quan hệ | include UC-09.08a |
| Truy vết | FR-BIL-09; NFR-SEC-07; IC-07; seq-thanh-toan, act-m09-vi-thanh-toan |
| Giai đoạn | P3 ✂1 |

**Luồng chính**
1. Cổng gửi event.
2. Hệ thống xác thực chữ ký và timestamp (≤ 5 phút).
3. Hệ thống ghi `payment_events` (unique `gateway_event_id`).
4. Event mới: thực hiện **UC-09.08a**; đánh dấu `processed_at`.
5. Trả `200`.

**Luồng thay thế / ngoại lệ**
- **2a.** Chữ ký sai: `400`, ghi log bảo mật.
- **3a.** Event trùng: bỏ qua, trả `200`.
- **4a.** Lỗi xử lý: trả `500` để cổng gửi lại; giao dịch DB rollback.

### UC-09.08a Ghi nạp tiền vào sổ cái
<a id="uc-0908a"></a>

| Mục | Nội dung |
|---|---|
| Loại | include của UC-09.08 (bước 4) |
| Tác nhân | Hệ thống |
| Mô tả | Biến mỗi sự kiện thanh toán thành thay đổi đúng ở `payments` và ví, với đầy đủ bút toán sổ cái |
| Tiền điều kiện | Event mới đã qua kiểm tra chữ ký và chống trùng (UC-09.08 bước 2–3) |
| Hậu điều kiện | **Thành công:** `payments` và ví khớp với cổng; mọi thay đổi số dư có bút toán. **Tối thiểu:** lỗi thì rollback toàn bộ để cổng gửi lại |
| Kích hoạt | UC-09.08 bước 4 |
| Truy vết | FR-BIL-03, FR-BIL-09; WR-01..08; IC-06, IC-07; seq-thanh-toan |
| Giai đoạn | P3 ✂1 |

**Luồng chính**
1. Hệ thống xác định người dùng và `payments` từ `client_reference_id` và `metadata.paymentId` của event.
2. Hệ thống xử lý trong **một giao dịch** theo loại event (các nhánh 2a–2d).
3. Hệ thống cập nhật `wallets` và ghi `wallet_ledger_entries` kèm `payment_id` cùng giao dịch.
4. Hệ thống phát `wallet.updated` để Dashboard làm mới.

**Luồng thay thế / ngoại lệ**
- **2a.** `checkout.session.completed` với `payment_status = paid` cho nạp tiền: `payments.status = SUCCEEDED`; ghi `TOPUP`; `available_micro += x`, `topup_total_micro += x` (WR-06).
- **2b.** Số tiền trong event khác `payments.amount_micro`: không cộng tiền, ghi cảnh báo P1 để kiểm tra thủ công [ĐX].
- **2c.** Loại event không hỗ trợ: chỉ ghi `payment_events`, không đổi dữ liệu khác, trả `200`.
- **2d.** *(Sau MVP)* Sự kiện gói (`invoice.paid`, `invoice.payment_failed`, `customer.subscription.deleted`): cập nhật Subscription theo `state-subscription`; refund hoặc chargeback ghi `REFUND` âm, số dư âm thì khóa thao tác tốn phí đến khi bù (WR-07).
- ***a.** Lỗi xử lý: rollback; UC-09.08 trả `500` để cổng gửi lại.

---

> **Đã bỏ:** UC-09.07 "Nhận credit hằng ngày" (FR-BIL-07), thay bằng tiền dùng thử $2 một lần khi tạo hồ sơ ở UC-01.01b (QĐ-37).
