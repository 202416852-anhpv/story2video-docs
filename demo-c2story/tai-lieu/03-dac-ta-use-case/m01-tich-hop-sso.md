# M01 — Tích hợp SSO & hồ sơ

> Sơ đồ: `../../so-do/01-use-case/phan-ra/uc-m01-tich-hop-sso.puml`, `../../so-do/04-tuan-tu/seq-dang-nhap-sso.puml`. Yêu cầu: FR-AUTH-01..10. Đăng ký, mật khẩu và MFA thuộc SSO có sẵn; ứng dụng **không** phát triển lại (C-05).

---

<a id="uc-0101"></a>
## UC-01.01 Đăng nhập qua SSO

| Mục | Nội dung |
|---|---|
| Tác nhân chính / phụ | Guest / SSO có sẵn (OIDC Provider) |
| Mô tả | Người dùng đăng nhập vào ứng dụng bằng tài khoản SSO có sẵn, nhận phiên làm việc và hồ sơ cục bộ |
| Tiền điều kiện | Chưa có phiên hợp lệ; ứng dụng đã được đăng ký `client_id` với SSO |
| Hậu điều kiện | **Thành công:** có phiên ứng dụng (cookie httpOnly); `users` tồn tại và đồng bộ với claims; người dùng ở trang đã yêu cầu. **Tối thiểu:** không tạo phiên khi xác thực thất bại; mọi lỗi bảo mật được ghi log |
| Kích hoạt | Bấm "Đăng nhập" hoặc truy cập trang yêu cầu đăng nhập (vd. link mời) |
| Quan hệ | include UC-01.01a, UC-01.01b, UC-01.01c |
| Truy vết | FR-AUTH-01..04, FR-AUTH-07; NFR-SEC-02 |

**Luồng chính**
1. Guest bấm "Đăng nhập" hoặc mở một trang cần đăng nhập.
2. Hệ thống ghi nhớ `returnTo` (chỉ đường dẫn nội bộ), tạo `state`, `nonce`, `code_verifier` và chuyển hướng tới `authorization_endpoint` của SSO.
3. Người dùng đăng nhập trên trang SSO. Nếu chưa có tài khoản thì đăng ký ngay trên SSO; nếu SSO đã có phiên thì bước này được bỏ qua.
4. SSO chuyển về `/auth/callback?code&state`.
5. Hệ thống thực hiện **UC-01.01a** (xác thực ID token).
6. Hệ thống thực hiện **UC-01.01b** (tạo hoặc đồng bộ hồ sơ).
7. Hệ thống tạo phiên (cookie `HttpOnly; Secure; SameSite=Lax`), lưu refresh token đã mã hóa phía server.
8. Hệ thống thực hiện **UC-01.01c** (quay về trang đã yêu cầu).

**Luồng thay thế / ngoại lệ**
- **3a.** Người dùng hủy trên SSO hoặc SSO trả `error`: quay về trang chủ, hiện "Đăng nhập không thành công".
- **5a.** `state` không khớp, token sai chữ ký hoặc hết hạn: từ chối, ghi log bảo mật, không tạo phiên.
- **6a.** Hồ sơ cục bộ ở trạng thái `LOCKED` (vi phạm chính sách): hiện thông báo, không tạo phiên.
- **\*a.** SSO không phản hồi (timeout 10 s): hiện trang lỗi thân thiện, gợi ý thử lại sau.

### UC-01.01a Xác thực ID token
<a id="uc-0101a"></a>
- **Loại:** include (bước 5).
- **Các bước:** (1) kiểm tra `state`; (2) đổi `code` + `code_verifier` lấy token tại `token_endpoint`; (3) lấy JWKS (có cache, tự làm mới khi gặp `kid` lạ); (4) kiểm tra chữ ký, `iss`, `aud`, `exp`, `iat`, `nonce`.
- **Kết quả:** claims hợp lệ (`sub`, `email`, `name`, `picture`, `locale`, `roles`) hoặc lỗi xác thực.

### UC-01.01b Tạo / đồng bộ hồ sơ cục bộ (JIT)
<a id="uc-0101b"></a>
- **Loại:** include (bước 6).
- **Các bước:** (1) tìm `users` theo `sso_subject = sub`; (2) chưa có thì tạo hồ sơ mới, tạo ví credit với bucket rỗng, cấp gói Free; (3) có rồi thì cập nhật email, tên, avatar và vai trò Admin theo claim `roles` (FR-AUTH-07); (4) cập nhật `last_login_at`.
- **Kết quả:** hồ sơ cục bộ đồng bộ với SSO; không lưu mật khẩu.

### UC-01.01c Quay về trang đã yêu cầu
<a id="uc-0101c"></a>
- **Loại:** include (bước 8).
- **Các bước:** đọc `returnTo` đã lưu; nếu là đường dẫn nội bộ hợp lệ thì chuyển tới đó, ngược lại về `/projects`.
- **Kết quả:** người dùng tiếp tục đúng tác vụ (vd. chấp nhận lời mời dự án, UC-02.08). Chặn open redirect.

---

<a id="uc-0102"></a>
## UC-01.02 Đăng xuất

| Mục | Nội dung |
|---|---|
| Tác nhân chính / phụ | User / SSO có sẵn |
| Mô tả | Kết thúc phiên ứng dụng và phiên SSO |
| Tiền điều kiện | Đang có phiên |
| Hậu điều kiện | **Thành công:** phiên ứng dụng bị thu hồi, token đã lưu bị xóa, phiên SSO kết thúc. **Tối thiểu:** phiên ứng dụng luôn bị thu hồi kể cả khi SSO lỗi |
| Kích hoạt | Bấm "Đăng xuất" |
| Quan hệ | include UC-01.02a |
| Truy vết | FR-AUTH-05 |

**Luồng chính**
1. User bấm "Đăng xuất".
2. Hệ thống thu hồi `user_sessions` hiện tại và xóa cookie.
3. Hệ thống thực hiện **UC-01.02a**.
4. SSO kết thúc phiên và chuyển về trang chủ ứng dụng.

**Luồng thay thế / ngoại lệ**
- **3a.** SSO không có `end_session_endpoint`: chỉ đăng xuất cục bộ, hiện ghi chú "Bạn vẫn đăng nhập ở các ứng dụng khác dùng chung SSO".

### UC-01.02a Kết thúc phiên SSO (RP-initiated logout)
<a id="uc-0102a"></a>
- **Loại:** include (bước 3).
- **Các bước:** dựng URL `end_session_endpoint?id_token_hint&post_logout_redirect_uri`; chuyển hướng trình duyệt.
- **Kết quả:** phiên SSO kết thúc; người dùng về trang chủ.

---

<a id="uc-0103"></a>
## UC-01.03 Xem Dashboard

| Mục | Nội dung |
|---|---|
| Tác nhân chính | User |
| Mô tả | Xem tổng quan tài khoản: gói, số dư credit, số dự án, lối tắt |
| Tiền điều kiện | Đã đăng nhập |
| Hậu điều kiện | **Thành công:** hiển thị số liệu mới nhất |
| Kích hoạt | Mở `/dashboard` |
| Quan hệ | được mở rộng bởi UC-01.05 |
| Truy vết | FR-AUTH-09 |

**Luồng chính**
1. User mở Dashboard.
2. Hệ thống trả về gói hiện tại, số dư credit theo bucket, số dự án (sở hữu / tham gia), lối tắt "Manage Billing", "Projects", "Pricing".
3. User chọn một lối tắt để đi tiếp.

**Luồng thay thế / ngoại lệ**
- **2a.** Không lấy được số dư (lỗi tạm thời): hiển thị phần còn lại, ô số dư hiện "Đang cập nhật".

---

<a id="uc-0104"></a>
## UC-01.04 Đổi ngôn ngữ giao diện

| Mục | Nội dung |
|---|---|
| Tác nhân chính | User |
| Mô tả | Chọn ngôn ngữ giao diện (vi, en) |
| Tiền điều kiện | Đã đăng nhập (Guest đổi được tạm thời qua cookie) |
| Hậu điều kiện | **Thành công:** `users.locale` cập nhật; giao diện hiển thị theo ngôn ngữ mới |
| Kích hoạt | Chọn ngôn ngữ ở menu |
| Truy vết | FR-AUTH-08 |

**Luồng chính**
1. User mở menu ngôn ngữ và chọn "Tiếng Việt" hoặc "English".
2. Hệ thống lưu `locale` vào hồ sơ và tải lại chuỗi giao diện.

**Luồng thay thế / ngoại lệ**
- **\*a.** Lần đăng nhập đầu: mặc định lấy claim `locale` của SSO nếu có.
- Ghi chú: đổi ngôn ngữ giao diện **không** thay đổi ngôn ngữ thuyết minh của dự án (UC-05.11).

---

<a id="uc-0105"></a>
## UC-01.05 Mở trang quản lý tài khoản SSO

| Mục | Nội dung |
|---|---|
| Tác nhân chính / phụ | User / SSO có sẵn |
| Mô tả | Chuyển tới trang hồ sơ của SSO để đổi mật khẩu, email, MFA |
| Tiền điều kiện | Đang ở Dashboard |
| Hậu điều kiện | **Thành công:** trang SSO mở trong tab mới |
| Kích hoạt | Bấm "Quản lý tài khoản" |
| Quan hệ | extend UC-01.03 |
| Truy vết | FR-AUTH-09, C-05 |

**Luồng chính**
1. User bấm "Quản lý tài khoản" trên Dashboard.
2. Hệ thống mở URL trang tài khoản của SSO (cấu hình) trong tab mới.
3. Thay đổi email/tên trên SSO được đồng bộ ở lần đăng nhập kế tiếp (UC-01.01b).

---

<a id="uc-0106"></a>
## UC-01.06 Yêu cầu xóa dữ liệu ứng dụng

| Mục | Nội dung |
|---|---|
| Tác nhân chính | User |
| Mô tả | Xóa dữ liệu của người dùng trong ứng dụng (không xóa tài khoản SSO) |
| Tiền điều kiện | Đã đăng nhập |
| Hậu điều kiện | **Thành công:** hồ sơ `DELETED`; dự án sở hữu được lên lịch xóa sau 30 ngày; tư cách Editor ở dự án khác bị gỡ ngay; ledger và hóa đơn giữ theo luật kế toán (ẩn danh hóa). **Tối thiểu:** không xóa gì khi chưa xác nhận |
| Kích hoạt | Chọn "Xóa dữ liệu của tôi" |
| Truy vết | FR-AUTH-10, NFR-PRV-01 |

**Luồng chính**
1. User chọn "Xóa dữ liệu của tôi".
2. Hệ thống liệt kê hệ quả: số dự án sẽ bị xóa, dự án tham gia sẽ rời, credit còn lại sẽ mất, gói đang hoạt động cần hủy.
3. User nhập lại email để xác nhận.
4. Hệ thống hủy gói (nếu có), đánh dấu hồ sơ, lên lịch xóa, đăng xuất mọi phiên, gửi email xác nhận.

**Luồng thay thế / ngoại lệ**
- **2a.** User đang là Owner của dự án có Editor khác: gợi ý xuất dữ liệu (ZIP) trước; dự án vẫn bị xóa theo lịch.
- **4a.** User đăng nhập lại trong 30 ngày: hiện tùy chọn khôi phục.

---

<a id="uc-0107"></a>
## UC-01.07 Nhận đăng xuất back-channel

| Mục | Nội dung |
|---|---|
| Tác nhân chính | SSO có sẵn |
| Mô tả | SSO thông báo trực tiếp cho server ứng dụng rằng một phiên SSO đã kết thúc |
| Tiền điều kiện | SSO hỗ trợ OIDC Back-Channel Logout; ứng dụng đã đăng ký `backchannel_logout_uri` |
| Hậu điều kiện | **Thành công:** mọi phiên ứng dụng có `sso_sid`/`sub` tương ứng bị thu hồi. **Tối thiểu:** token không hợp lệ bị bỏ qua và ghi log |
| Kích hoạt | `POST /auth/backchannel-logout` với `logout_token` |
| Truy vết | FR-AUTH-05, NFR-SEC-02b |

**Luồng chính**
1. SSO gửi `logout_token`.
2. Hệ thống xác thực token theo JWKS (chữ ký, `iss`, `aud`, `events`, không có `nonce`).
3. Hệ thống thu hồi các `user_sessions` khớp `sid` (hoặc toàn bộ phiên của `sub`).
4. Hệ thống trả `200`.

**Luồng thay thế / ngoại lệ**
- **2a.** Token không hợp lệ: trả `400`, ghi log bảo mật.
- **\*a.** SSO không hỗ trợ back-channel: phiên tự hết hạn ở chu kỳ refresh kế tiếp (≤ 15 phút, FR-AUTH-06).
