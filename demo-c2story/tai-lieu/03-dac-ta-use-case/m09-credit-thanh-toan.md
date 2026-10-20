# M09 — Credit & thanh toán

> Sơ đồ: `../../so-do/01-use-case/phan-ra/uc-m09-credit-thanh-toan.puml`, `../../so-do/04-tuan-tu/seq-thanh-toan.puml`, `../../so-do/06-trang-thai/state-subscription.puml`. Yêu cầu: FR-BIL-01..09. Quy tắc ví: [08 §4](../08-quy-tac-nghiep-vu.md). Thanh toán qua cổng (Stripe, tài khoản của nhóm); hệ thống không lưu thẻ.

---

<a id="uc-0901"></a>
## UC-09.01 Xem bảng giá

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Guest |
| Mô tả | Xem gói Monthly/Annual, credit pack, bảng giá thao tác, FAQ |
| Tiền điều kiện | — |
| Hậu điều kiện | **Thành công:** hiển thị giá hiện hành từ cấu hình |
| Kích hoạt | Mở `/pricing` |
| Truy vết | FR-BIL-01 |

**Luồng chính**
1. Guest mở Pricing.
2. Hệ thống hiển thị tab Monthly / Annual (−17%) / Credit Packs; mỗi gói có giá, credit/tháng, quyền lợi; bảng chi phí thao tác (ảnh, TTS, AI âm thanh); FAQ.
3. Guest bấm "Đăng ký" hoặc "Mua"; nếu chưa đăng nhập thì chuyển UC-01.01, sau đó tiếp UC-09.02 / UC-09.03.

---

<a id="uc-0902"></a>
## UC-09.02 Đăng ký gói

| Mục | Nội dung |
|---|---|
| Tác nhân chính / phụ | User / Payment Gateway |
| Mô tả | Đăng ký gói Starter / Creator / Studio theo tháng hoặc năm |
| Tiền điều kiện | Đã đăng nhập; chưa có gói trả phí đang hoạt động (đổi gói dùng UC-09.04) |
| Hậu điều kiện | **Thành công:** Subscription `ACTIVE`; credit kỳ đầu được cấp. **Tối thiểu:** không cấp credit khi chưa nhận webhook thanh toán |
| Kích hoạt | Chọn gói trên Pricing |
| Quan hệ | include UC-09.03a |
| Truy vết | FR-BIL-02 |

**Luồng chính**
1. User chọn gói và chu kỳ.
2. Hệ thống thực hiện **UC-09.03a**.
3. Sau khi cổng xác nhận, UC-09.08 cập nhật gói và cấp credit.
4. User quay lại Dashboard thấy gói mới.

**Luồng thay thế / ngoại lệ**
- **3a.** Webhook đến chậm: Dashboard hiện "Đang xử lý thanh toán" và tự làm mới qua SSE.

---

<a id="uc-0903"></a>
## UC-09.03 Mua gói credit

| Mục | Nội dung |
|---|---|
| Tác nhân chính / phụ | User / Payment Gateway |
| Mô tả | Mua credit một lần, không hết hạn |
| Tiền điều kiện | Đã đăng nhập |
| Hậu điều kiện | **Thành công:** bucket PACK tăng đúng số credit |
| Kích hoạt | Chọn pack trên Pricing, hoặc từ thông báo thiếu credit (`402`) |
| Quan hệ | include UC-09.03a |
| Truy vết | FR-BIL-03 |

**Luồng chính**
1. User chọn pack.
2. Hệ thống thực hiện **UC-09.03a**.
3. UC-09.08 ghi ledger PURCHASE vào bucket PACK.
4. Nếu User đến từ thông báo thiếu credit, hệ thống đưa User về đúng thao tác đang dở.

### UC-09.03a Thanh toán qua checkout
<a id="uc-0903a"></a>

| Mục | Nội dung |
|---|---|
| Loại | include của UC-09.02 và UC-09.03 |
| Tác nhân | User / Payment Gateway (Stripe Checkout) |
| Mô tả | Đưa User sang trang thanh toán của cổng để trả tiền; ứng dụng không bao giờ nhận hay lưu thông tin thẻ |
| Tiền điều kiện | Đã đăng nhập; gói hoặc credit pack được chọn còn hoạt động |
| Hậu điều kiện | **Thành công:** User hoàn tất thanh toán trên cổng và cổng phát webhook cho UC-09.08. **Tối thiểu:** hủy hoặc thất bại thì không có thay đổi nào về gói hay credit |
| Kích hoạt | UC-09.02 bước 2; UC-09.03 bước 2 |
| Truy vết | ADR-08; FR-BIL-02, FR-BIL-03; NFR-SEC-07; API 2.8 `POST /billing/checkout-sessions` |

**Luồng chính**
1. Client gọi `POST /billing/checkout-sessions` với `{planCode, cycle}` hoặc `{packCode}`.
2. Hệ thống kiểm tra gói hoặc pack còn `active`, tạo (nếu chưa có) khách hàng ở cổng và lưu `users.gateway_customer_id`.
3. Hệ thống tạo Checkout Session với `client_reference_id = userId`, mã giá lấy từ `plans.gateway_price_ids` hoặc `credit_packs.gateway_price_id`, cùng `success_url` và `cancel_url`.
4. API trả `{ url }`; client chuyển hướng trình duyệt tới trang thanh toán của cổng.
5. User thanh toán; cổng chuyển về `success_url` (Dashboard hiện "Đang xử lý thanh toán").
6. Cổng phát webhook; UC-09.08 cập nhật gói và credit.

**Luồng thay thế / ngoại lệ**
- **2a.** Mã gói hoặc pack không tồn tại hoặc đã ngừng bán: `404` hoặc `422`.
- **2b.** Đăng ký gói mới khi đã có gói trả phí đang hoạt động: chặn, hướng tới UC-09.04.
- **4a.** Cổng không phản hồi: báo lỗi, không tạo dữ liệu nào.
- **5a.** User hủy: cổng chuyển về `cancel_url` (Pricing); không có thay đổi.
- **5b.** Thanh toán thất bại tại cổng: User ở lại trang của cổng để thử lại.
- **6a.** Webhook đến chậm: không cấp credit trước khi webhook xử lý xong (UC-09.02 nhánh 3a).

---

<a id="uc-0904"></a>
## UC-09.04 Quản lý thanh toán

| Mục | Nội dung |
|---|---|
| Tác nhân chính / phụ | User / Payment Gateway |
| Mô tả | Nâng/hạ gói, đổi thẻ, xem hóa đơn, hủy gói qua cổng |
| Tiền điều kiện | Có khách hàng trên cổng |
| Hậu điều kiện | **Thành công:** thay đổi được đồng bộ qua webhook (UC-09.08) |
| Kích hoạt | "Manage Billing" |
| Truy vết | FR-BIL-04 |

**Luồng chính**
1. User bấm "Manage Billing".
2. Hệ thống tạo phiên customer portal và chuyển hướng.
3. User thực hiện thay đổi trên trang của cổng.
4. Webhook cập nhật Subscription (UC-09.08).

**Luồng thay thế / ngoại lệ**
- **3a.** Hủy gói: hiệu lực cuối kỳ (`CANCEL_AT_PERIOD_END`); credit kỳ hiện tại dùng được đến hết kỳ.
- **3b.** Hạ gói: áp dụng từ kỳ sau.

---

<a id="uc-0905"></a>
## UC-09.05 Xem số dư credit

| Mục | Nội dung |
|---|---|
| Tác nhân chính | User |
| Mô tả | Xem số dư theo bucket (gói, pack, thưởng), phần đang giữ, ngày hết hạn |
| Tiền điều kiện | Đã đăng nhập |
| Hậu điều kiện | **Thành công:** số liệu khớp `credit_balances` |
| Kích hoạt | Badge credit ở thanh trên, hoặc Dashboard |
| Truy vết | FR-BIL-05 |

**Luồng chính**
1. User bấm badge credit.
2. Hệ thống hiển thị: khả dụng theo bucket, đang giữ (job chạy), ngày hết hạn credit gói.

---

<a id="uc-0906"></a>
## UC-09.06 Xem lịch sử tiêu credit

| Mục | Nội dung |
|---|---|
| Tác nhân chính | User |
| Mô tả | Xem sổ cái credit, lọc theo dự án và loại thao tác |
| Tiền điều kiện | Đã đăng nhập |
| Hậu điều kiện | **Thành công:** hiển thị các bút toán (append-only) |
| Kích hoạt | "Lịch sử credit" |
| Truy vết | FR-BIL-06, 08 |

**Luồng chính**
1. User mở lịch sử.
2. Hệ thống liệt kê bút toán: thời gian, loại (GRANT, PURCHASE, HOLD, CAPTURE, RELEASE, EXPIRE, ADJUST), số credit, dự án, thao tác.
3. User lọc theo dự án/thao tác/thời gian, xem tổng.

---

<a id="uc-0907"></a>
## UC-09.07 Nhận credit hằng ngày

| Mục | Nội dung |
|---|---|
| Tác nhân chính | User (gói Free) |
| Mô tả | Nhận credit miễn phí mỗi ngày |
| Tiền điều kiện | Chưa nhận trong ngày (theo múi giờ người dùng); bucket BONUS chưa đạt mức tích tối đa |
| Hậu điều kiện | **Thành công:** ledger GRANT vào bucket BONUS |
| Kích hoạt | Bấm "Nhận credit hôm nay" |
| Truy vết | FR-BIL-07 (C) |

**Luồng chính**
1. User bấm "Nhận".
2. Hệ thống kiểm tra điều kiện, ghi GRANT (vd. 3 credit, tối đa tích 10).
3. Hệ thống hiển thị số dư mới.

**Luồng thay thế / ngoại lệ**
- **2a.** Đã nhận hôm nay: hiện thời gian còn lại đến lượt sau.

---

<a id="uc-0908"></a>
## UC-09.08 Xử lý webhook thanh toán

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Payment Gateway |
| Mô tả | Nhận sự kiện thanh toán và cập nhật gói/credit một cách idempotent |
| Tiền điều kiện | Webhook có chữ ký hợp lệ |
| Hậu điều kiện | **Thành công:** mỗi event xử lý đúng một lần. **Tối thiểu:** event trùng hoặc sai chữ ký không làm thay đổi dữ liệu |
| Kích hoạt | `POST /webhooks/stripe` |
| Quan hệ | include UC-09.08a |
| Truy vết | FR-BIL-09; NFR-SEC-07; IC-07 |

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

### UC-09.08a Cập nhật gói & nạp credit (ledger)
<a id="uc-0908a"></a>

| Mục | Nội dung |
|---|---|
| Loại | include của UC-09.08 (bước 4) |
| Tác nhân | Hệ thống |
| Mô tả | Biến mỗi sự kiện thanh toán thành thay đổi đúng ở gói, thanh toán và ví credit, với đầy đủ bút toán ledger |
| Tiền điều kiện | Event mới đã qua kiểm tra chữ ký và chống trùng (UC-09.08 bước 2–3) |
| Hậu điều kiện | **Thành công:** `subscriptions`, `payments` và ví credit khớp với cổng; mọi thay đổi credit có bút toán ledger. **Tối thiểu:** lỗi thì rollback toàn bộ để cổng gửi lại |
| Kích hoạt | UC-09.08 bước 4 |
| Truy vết | FR-BIL-09; CR-01..08; IC-06, IC-07; `so-do/06-trang-thai/state-subscription.puml` |

**Luồng chính**
1. Hệ thống xác định người dùng và đối tượng từ `client_reference_id`, `gateway_subscription_id` hoặc `gateway_customer_id` của event.
2. Hệ thống xử lý trong **một giao dịch** theo loại event (các nhánh 2a–2g).
3. Hệ thống ghi `payments` (đúng một trong `plan_id` hoặc `credit_pack_id`) và các bút toán `credit_ledger_entries` kèm `payment_id`.
4. Hệ thống cập nhật `credit_balances` cùng giao dịch và phát sự kiện realtime để Dashboard làm mới.

**Luồng thay thế / ngoại lệ**
- **2a.** `checkout.session.completed` hoặc `invoice.paid` (gói): Subscription `ACTIVE`; EXPIRE phần `SUBSCRIPTION` còn lại (trừ phần đang held); GRANT credit kỳ mới (CR-06).
- **2b.** `checkout.session.completed` (credit pack): PURCHASE vào bucket `PACK` (không hết hạn).
- **2c.** `invoice.payment_failed`: Subscription `PAST_DUE`, gửi email nhắc.
- **2d.** `customer.subscription.deleted`: Subscription `CANCELED`, EXPIRE credit gói.
- **2e.** Refund hoặc chargeback: ADJUST âm; nếu số dư âm thì khóa thao tác tốn phí đến khi bù (CR-07).
- **2f.** Loại event không hỗ trợ: chỉ ghi `payment_events`, không đổi dữ liệu khác, trả `200`.
- **2g.** Event đến sai thứ tự (ví dụ `invoice.paid` trước `checkout.session.completed`): xử lý theo `gateway_subscription_id` để kết quả cuối giống nhau [ĐX].
- ***a.** Lỗi xử lý: rollback; UC-09.08 trả `500` để cổng gửi lại.
