# M01 — Tích hợp SSO & hồ sơ

> Sơ đồ: `../../so-do/01-use-case/phan-ra/uc-m01-tich-hop-sso.puml`, `../../so-do/04-tuan-tu/seq-dang-nhap-sso.puml`. Yêu cầu: FR-AUTH-01..13. Quy tắc: BR-28, BR-30, BR-31. Đăng ký, mật khẩu và MFA thuộc SSO; ứng dụng **không** phát triển lại (C-05).
> **SSO:** Keycloak tự dựng từ P0; SSO Vbee ở P3 qua cùng `IdentityProviderPort` (ADR-20). Nếu Vbee chỉ có OAuth 2.0, bước xác thực ID token (UC-01.01a) được thay bằng gọi userinfo với access token (QĐ-23).

---

<a id="uc-0101"></a>
## UC-01.01 Đăng nhập qua SSO

| Mục | Nội dung |
|---|---|
| Tác nhân chính / phụ | Guest / SSO có sẵn (OIDC Provider) |
| Mô tả | Người dùng đăng nhập vào ứng dụng bằng tài khoản SSO có sẵn, nhận phiên làm việc và hồ sơ cục bộ |
| Tiền điều kiện | Chưa có phiên hợp lệ; ứng dụng đã được đăng ký `client_id` với SSO |
| Hậu điều kiện | **Thành công:** có phiên ứng dụng (cookie httpOnly); `users` tồn tại, đồng bộ với claims và đã đồng ý xử lý dữ liệu; người dùng ở trang đã yêu cầu. **Tối thiểu:** không tạo phiên khi xác thực thất bại hoặc email chưa được mời; mọi lỗi bảo mật được ghi log |
| Kích hoạt | Bấm "Đăng nhập" hoặc truy cập trang yêu cầu đăng nhập (vd. link mời) |
| Quan hệ | include UC-01.01a, UC-01.01b, UC-01.01c, UC-01.01d |
| Truy vết | FR-AUTH-01..04, 06, 07, 11, 12; BR-30, BR-31; NFR-SEC-02 |
| Giai đoạn | P0 |

**Luồng chính**
1. Guest bấm "Đăng nhập" hoặc mở một trang cần đăng nhập.
2. Hệ thống ghi nhớ `returnTo` (chỉ đường dẫn nội bộ), tạo `state`, `nonce`, `code_verifier` và chuyển hướng tới `authorization_endpoint` của SSO.
3. Người dùng đăng nhập trên trang SSO. Nếu chưa có tài khoản thì đăng ký ngay trên SSO; nếu SSO đã có phiên thì bước này được bỏ qua.
4. SSO chuyển về `/auth/callback?code&state`.
5. Hệ thống thực hiện **UC-01.01a** (xác thực ID token).
6. Hệ thống thực hiện **UC-01.01b** (tạo hoặc đồng bộ hồ sơ).
7. Hệ thống tạo phiên (cookie `HttpOnly; Secure; SameSite=Lax`), lưu refresh token đã mã hóa phía server.
8. Nếu người dùng chưa đồng ý xử lý dữ liệu (hoặc thông báo đã đổi phiên bản), hệ thống thực hiện **UC-01.01d**.
9. Hệ thống thực hiện **UC-01.01c** (quay về trang đã yêu cầu).

**Luồng thay thế / ngoại lệ**
- **3a.** Người dùng hủy trên SSO hoặc SSO trả `error`: quay về trang chủ, hiện "Đăng nhập không thành công".
- **5a.** `state` không khớp, token sai chữ ký hoặc hết hạn: từ chối, ghi log bảo mật, không tạo phiên.
- **6a.** Hồ sơ cục bộ ở trạng thái `LOCKED` (vi phạm chính sách hoặc tài khoản SSO bị khóa): hiện thông báo, không tạo phiên.
- **6b.** Lần đầu đăng nhập và email không có trong danh sách mời (BR-30): hiện "Bạn chưa được mời tham gia beta", không tạo hồ sơ, không tạo phiên (UC-01.01b nhánh 2a).
- **8a.** Người dùng không đồng ý: đăng xuất (UC-01.01d nhánh 3a).
- **\*a.** SSO không phản hồi (timeout 10 s): hiện trang lỗi thân thiện, gợi ý thử lại sau.

### UC-01.01a Xác thực ID token
<a id="uc-0101a"></a>

| Mục | Nội dung |
|---|---|
| Loại | include của UC-01.01 (bước 5) |
| Tác nhân | Hệ thống (BFF) / SSO có sẵn (`token_endpoint`, `jwks_uri`) |
| Mô tả | Đổi authorization code lấy token và xác thực ID token trước khi tin bất kỳ claim nào |
| Tiền điều kiện | Có `code` và `state` ở callback; phiên đăng nhập tạm (UC-01.01 bước 2) còn lưu `state`, `nonce`, `code_verifier`, `returnTo` |
| Hậu điều kiện | **Thành công:** claims hợp lệ (`sub`, `email`, `name`, `picture`, `locale`, `roles`) được chuyển cho UC-01.01b. **Tối thiểu:** không dùng code hoặc token chưa xác thực; mọi lỗi được ghi log bảo mật; không tạo phiên |
| Kích hoạt | SSO chuyển trình duyệt về `/auth/callback?code&state` |
| Truy vết | FR-AUTH-01..04; NFR-SEC-02; API 2.1 `/auth/callback` |
| Giai đoạn | P0 |

**Luồng chính**
1. Hệ thống so `state` ở callback với `state` đã lưu trong phiên đăng nhập tạm, rồi xóa giá trị này (chỉ dùng một lần).
2. Hệ thống gửi `code` cùng `code_verifier` (PKCE) tới `token_endpoint` của SSO và nhận token.
3. Hệ thống lấy JWKS từ `jwks_uri` (có cache; tự làm mới khi gặp `kid` chưa biết).
4. Hệ thống kiểm tra chữ ký, `iss`, `aud` (= `client_id`), `exp`, `iat` và `nonce` khớp với giá trị đã lưu.
5. Hệ thống trả claims đã xác thực cho UC-01.01b.

**Luồng thay thế / ngoại lệ**
- **1a.** `state` thiếu, không khớp hoặc đã dùng: từ chối, ghi log bảo mật, không gọi SSO (UC-01.01 nhánh 5a).
- **2a.** `token_endpoint` trả lỗi (code hết hạn hoặc đã dùng) hoặc quá 10 s không phản hồi: dừng, báo "Đăng nhập không thành công, hãy thử lại".
- **3a.** Không tải được JWKS và chưa có cache: dừng; **không** bỏ qua bước kiểm tra chữ ký.
- **4a.** Bất kỳ kiểm tra nào ở bước 4 thất bại: từ chối, ghi log, không lưu token.

### UC-01.01b Tạo / đồng bộ hồ sơ cục bộ (JIT)
<a id="uc-0101b"></a>

| Mục | Nội dung |
|---|---|
| Loại | include của UC-01.01 (bước 6) |
| Tác nhân | Hệ thống |
| Mô tả | Tạo hồ sơ cục bộ ở lần đăng nhập đầu (JIT) cho người được mời, hoặc đồng bộ hồ sơ theo claims ở các lần sau; không bao giờ lưu mật khẩu |
| Tiền điều kiện | Claims đã xác thực từ UC-01.01a |
| Hậu điều kiện | **Thành công:** có đúng một `users` ứng với `sso_subject = sub`, dữ liệu khớp claims; người dùng mới có ví với tiền dùng thử $2 (`TRIAL_GRANT`), trạng thái Free. **Tối thiểu:** email chưa được mời thì không tạo gì; lỗi ghi dữ liệu thì rollback, không tạo phiên |
| Kích hoạt | UC-01.01 bước 6 |
| Truy vết | FR-AUTH-04, 07, 11; FR-BIL-05, 10; BR-28, BR-30; IC-16; D-08; API 2.1 `/auth/callback`, `/me` |
| Giai đoạn | P0 |

**Luồng chính**
1. Hệ thống tìm `users` theo `sso_subject = sub`.
2. Chưa có: hệ thống kiểm tra `email` (chữ thường) có trong `beta_invites` chưa bị thu hồi (BR-30). Có: trong một giao dịch, tạo `users` (chưa đồng ý dữ liệu), tạo `wallets` (số dư 0), ghi bút toán `TRIAL_GRANT` $2 vào ví (BR-28) và đặt `beta_invites.used_by_user_id`.
3. Đã có: cập nhật `email`, `display_name`, `avatar_url` theo claims; `locale` chỉ lấy từ claim khi người dùng chưa tự đổi trong ứng dụng [ĐX].
4. Đặt `role = ADMIN` nếu claim `roles` chứa vai trò quản trị, ngược lại `USER` (FR-AUTH-07).
5. Cập nhật `last_login_at` và trả hồ sơ cho UC-01.01 bước 7.

**Luồng thay thế / ngoại lệ**
- **1a.** Hai callback đồng thời cho cùng `sub`: ràng buộc duy nhất của `sso_subject` bảo đảm chỉ một bản ghi; giao dịch thua thực hiện lại bước 1 và đi theo nhánh "đã có".
- **2a.** Email không có trong danh sách mời, hoặc lời mời đã bị thu hồi: không tạo `users`, trả `403 NOT_INVITED` cho UC-01.01 nhánh 6b. Ghi log để Admin xem ai đã thử đăng nhập [ĐX].
- **2b.** Claim `email` trống hoặc chưa được SSO xác minh: coi như chưa được mời.
- **2c.** Lời mời đã được dùng bởi một hồ sơ khác (cùng email, khác `sub`): không tặng thêm tiền dùng thử (IC-16); Admin xử lý thủ công.
- **2d.** Cấu hình `beta_invite_only = false` (mở rộng sau beta): bỏ qua kiểm tra danh sách mời.
- **3a.** `users.status = LOCKED`: trả về cho UC-01.01 nhánh 6a (không tạo phiên).
- **3b.** Người dùng đã có hồ sơ nhưng bị gỡ khỏi danh sách mời: vẫn đăng nhập bình thường (BR-30).
- ***a.** Lỗi ghi dữ liệu: rollback toàn bộ (kể cả ví và tiền dùng thử), báo lỗi chung, người dùng có thể đăng nhập lại.

### UC-01.01c Quay về trang đã yêu cầu
<a id="uc-0101c"></a>

| Mục | Nội dung |
|---|---|
| Loại | include của UC-01.01 (bước 8) |
| Tác nhân | Hệ thống |
| Mô tả | Đưa người dùng về đúng trang họ yêu cầu trước khi đăng nhập, đồng thời chặn open redirect |
| Tiền điều kiện | Phiên ứng dụng vừa được tạo; có thể có `returnTo` đã lưu ở UC-01.01 bước 2 |
| Hậu điều kiện | **Thành công:** người dùng ở trang đã yêu cầu hoặc `/projects`. **Tối thiểu:** không bao giờ chuyển hướng ra ngoài miền ứng dụng |
| Kích hoạt | UC-01.01 bước 8 |
| Truy vết | NFR-SEC-02 (`returnTo` chỉ cho phép đường dẫn nội bộ); API 2.1 `/auth/login` |
| Giai đoạn | P0 |

**Luồng chính**
1. Hệ thống đọc `returnTo` đã lưu và xóa khỏi phiên đăng nhập tạm.
2. Hệ thống kiểm tra lại `returnTo` (đã kiểm tra một lần ở lúc lưu): phải bắt đầu bằng một dấu `/`, không bắt đầu bằng `//`, không chứa scheme, host hoặc `\`.
3. Hợp lệ: trả `302` tới `returnTo` (vd. `/invites/{token}` để chấp nhận lời mời, UC-02.08).
4. Không hợp lệ hoặc không có: trả `302` tới `/projects`.

**Luồng thay thế / ngoại lệ**
- **2a.** `returnTo` trỏ tới trang người dùng không còn quyền truy cập: trang đích tự hiển thị lỗi `404` (không tiết lộ sự tồn tại), người dùng dùng điều hướng bình thường.

### UC-01.01d Đồng ý xử lý dữ liệu cá nhân
<a id="uc-0101d"></a>

| Mục | Nội dung |
|---|---|
| Loại | include của UC-01.01 (bước 8) |
| Tác nhân | User |
| Mô tả | Người dùng đọc thông báo xử lý dữ liệu cá nhân và đồng ý trước khi dùng ứng dụng, theo Nghị định 13/2023 |
| Tiền điều kiện | Có phiên ứng dụng; `users.consented_at` rỗng hoặc `consent_version` khác phiên bản thông báo hiện hành |
| Hậu điều kiện | **Thành công:** `users.consented_at` và `consent_version` được ghi; người dùng vào được ứng dụng. **Tối thiểu:** chưa đồng ý thì mọi API ngoài `/auth/*`, `/me`, `/me:consent` trả `403 CONSENT_REQUIRED` |
| Kích hoạt | UC-01.01 bước 8 |
| Truy vết | FR-AUTH-12; BR-31; C-02; NFR-PRV-01; API 2.1 `GET /me`, `POST /me:consent` |
| Giai đoạn | P0 |

**Luồng chính**
1. Hệ thống hiện màn hình thông báo (phiên bản lấy từ `system_settings.consent_notice_version`): dữ liệu thu thập (email, tên, ảnh đại diện từ SSO; truyện, ảnh, nhạc tải lên; video tạo ra; nhật ký sử dụng), mục đích (thử nghiệm đồ án tốt nghiệp, phiếu khảo sát), nơi xử lý (nhà cung cấp AI và lưu trữ), thời hạn (xóa toàn bộ sau ngày bảo vệ), quyền yêu cầu xóa sớm và kênh liên hệ.
2. Người dùng tích "Tôi đã đọc và đồng ý" rồi bấm "Tiếp tục".
3. Hệ thống gọi `POST /me:consent {noticeVersion}`, ghi `consented_at = now()` và `consent_version`.
4. Hệ thống quay về UC-01.01 bước 9.

**Luồng thay thế / ngoại lệ**
- **2a.** Chưa tích ô đồng ý: nút "Tiếp tục" bị vô hiệu hóa.
- **3a.** Người dùng bấm "Không đồng ý": hệ thống đăng xuất (UC-01.02); hồ sơ và ví vẫn giữ để lần sau đồng ý thì dùng tiếp.
- **3b.** `noticeVersion` gửi lên khác phiên bản hiện hành (thông báo vừa đổi): `409`, tải lại thông báo mới.
- ***a.** Thông báo đổi phiên bản sau khi người dùng đã đồng ý: lần đăng nhập hoặc gia hạn phiên kế tiếp hiện lại màn hình này.

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
| Giai đoạn | P0 |

**Luồng chính**
1. User bấm "Đăng xuất".
2. Hệ thống thu hồi `user_sessions` hiện tại và xóa cookie.
3. Hệ thống thực hiện **UC-01.02a**.
4. SSO kết thúc phiên và chuyển về trang chủ ứng dụng.

**Luồng thay thế / ngoại lệ**
- **3a.** SSO không có `end_session_endpoint`: chỉ đăng xuất cục bộ, hiện ghi chú "Bạn vẫn đăng nhập ở các ứng dụng khác dùng chung SSO".

### UC-01.02a Kết thúc phiên SSO
<a id="uc-0102a"></a>

| Mục | Nội dung |
|---|---|
| Loại | include của UC-01.02 (bước 3) |
| Tác nhân | Hệ thống / SSO có sẵn |
| Mô tả | Báo cho SSO kết thúc phiên (RP-initiated logout) để người dùng không còn đăng nhập ở SSO sau khi đăng xuất khỏi ứng dụng |
| Tiền điều kiện | Phiên ứng dụng vừa bị thu hồi (UC-01.02 bước 2); còn `id_token_hint` đã mã hóa của phiên đó |
| Hậu điều kiện | **Thành công:** phiên SSO kết thúc; trình duyệt về trang chủ. **Tối thiểu:** token đã lưu bị xóa dù SSO có lỗi |
| Kích hoạt | UC-01.02 bước 3 |
| Truy vết | FR-AUTH-05; API 2.1 `POST /auth/logout` |
| Giai đoạn | P0 |

**Luồng chính**
1. Hệ thống giải mã `id_token_hint` của phiên vừa thu hồi, rồi xóa mọi token đã lưu của phiên.
2. Hệ thống lấy `end_session_endpoint` từ metadata (discovery) của SSO.
3. Hệ thống dựng URL `end_session_endpoint?id_token_hint=…&post_logout_redirect_uri=…` (địa chỉ trang chủ đã đăng ký với SSO).
4. API trả `{ logoutUrl }`; client chuyển hướng trình duyệt tới URL này.
5. SSO kết thúc phiên và chuyển về trang chủ ứng dụng.

**Luồng thay thế / ngoại lệ**
- **2a.** SSO không có `end_session_endpoint`: chỉ đăng xuất cục bộ, hiện ghi chú "Bạn vẫn đăng nhập ở các ứng dụng khác dùng chung SSO" (UC-01.02 nhánh 3a).
- **3a.** Không còn `id_token_hint` (hết hạn hoặc mất): vẫn gọi `end_session_endpoint` không kèm hint; SSO có thể hỏi xác nhận đăng xuất.
- **5a.** SSO báo lỗi hoặc không phản hồi: người dùng vẫn ở trạng thái đã đăng xuất khỏi ứng dụng; không thử lại tự động.

---

<a id="uc-0103"></a>
## UC-01.03 Xem Dashboard

| Mục | Nội dung |
|---|---|
| Tác nhân chính | User |
| Mô tả | Xem tổng quan tài khoản: trạng thái (Free / Đã nạp tiền), số dư ví, phần Free đã dùng trong tháng, số dự án, lối tắt |
| Tiền điều kiện | Đã đăng nhập |
| Hậu điều kiện | **Thành công:** hiển thị số liệu mới nhất |
| Kích hoạt | Mở `/dashboard` |
| Quan hệ | được mở rộng bởi UC-01.05 |
| Truy vết | FR-AUTH-09; FR-BIL-05, 12; API 2.1 `GET /me/dashboard` |
| Giai đoạn | P2 |

**Luồng chính**
1. User mở Dashboard.
2. Hệ thống trả về trạng thái tài khoản, số dư khả dụng và đang giữ, với tài khoản Free thêm số lần render và phút video đã dùng trong tháng (BR-27); số dự án; lối tắt "Nạp tiền", "Lịch sử chi tiêu", "Projects", "Pricing".
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
| Giai đoạn | P3 |

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
| Giai đoạn | P2 |

**Luồng chính**
1. User bấm "Quản lý tài khoản" trên Dashboard.
2. Hệ thống mở URL trang tài khoản của SSO (cấu hình) trong tab mới.
3. Thay đổi email/tên trên SSO được đồng bộ ở lần đăng nhập kế tiếp (UC-01.01b).

---

<a id="uc-0106"></a>
## UC-01.06 Yêu cầu xóa dữ liệu ứng dụng

> **Sau MVP.** Trong closed beta, người dùng yêu cầu xóa qua kênh liên hệ ở thông báo đồng ý (UC-01.01d); Admin xóa thủ công. Toàn bộ dữ liệu beta bị xóa sau ngày bảo vệ (BR-31).

| Mục | Nội dung |
|---|---|
| Tác nhân chính | User |
| Mô tả | Xóa dữ liệu của người dùng trong ứng dụng (không xóa tài khoản SSO) |
| Tiền điều kiện | Đã đăng nhập |
| Hậu điều kiện | **Thành công:** hồ sơ `DELETED`; dự án sở hữu được lên lịch xóa sau 30 ngày; tư cách Editor ở dự án khác bị gỡ ngay; ledger và hóa đơn giữ theo luật kế toán (ẩn danh hóa). **Tối thiểu:** không xóa gì khi chưa xác nhận |
| Kích hoạt | Chọn "Xóa dữ liệu của tôi" |
| Truy vết | FR-AUTH-10, NFR-PRV-01 |
| Giai đoạn | Sau |

**Luồng chính**
1. User chọn "Xóa dữ liệu của tôi".
2. Hệ thống liệt kê hệ quả: số dự án sẽ bị xóa, dự án tham gia sẽ rời, số dư ví còn lại sẽ mất.
3. User nhập lại email để xác nhận.
4. Hệ thống đánh dấu hồ sơ, lên lịch xóa, đăng xuất mọi phiên, gửi email xác nhận.

**Luồng thay thế / ngoại lệ**
- **2a.** User đang là Owner của dự án có Editor khác: gợi ý xuất dữ liệu (ZIP) trước; dự án vẫn bị xóa theo lịch.
- **4a.** User đăng nhập lại trong 30 ngày: hiện tùy chọn khôi phục.

---

<a id="uc-0107"></a>
## UC-01.07 Nhận đăng xuất back-channel

> **Sau MVP.** Không có nếu Vbee chỉ hỗ trợ OAuth 2.0 (QĐ-23); khi đó phiên hết hạn theo chu kỳ gia hạn (FR-AUTH-06).

| Mục | Nội dung |
|---|---|
| Tác nhân chính | SSO có sẵn |
| Mô tả | SSO thông báo trực tiếp cho server ứng dụng rằng một phiên SSO đã kết thúc |
| Tiền điều kiện | SSO hỗ trợ OIDC Back-Channel Logout; ứng dụng đã đăng ký `backchannel_logout_uri` |
| Hậu điều kiện | **Thành công:** mọi phiên ứng dụng có `sso_sid`/`sub` tương ứng bị thu hồi. **Tối thiểu:** token không hợp lệ bị bỏ qua và ghi log |
| Kích hoạt | `POST /auth/backchannel-logout` với `logout_token` |
| Truy vết | FR-AUTH-05, NFR-SEC-02b |
| Giai đoạn | Sau |

**Luồng chính**
1. SSO gửi `logout_token`.
2. Hệ thống xác thực token theo JWKS (chữ ký, `iss`, `aud`, `events`, không có `nonce`).
3. Hệ thống thu hồi các `user_sessions` khớp `sid` (hoặc toàn bộ phiên của `sub`).
4. Hệ thống trả `200`.

**Luồng thay thế / ngoại lệ**
- **2a.** Token không hợp lệ: trả `400`, ghi log bảo mật.
- **\*a.** SSO không hỗ trợ back-channel: phiên tự hết hạn ở chu kỳ refresh kế tiếp (≤ 15 phút, FR-AUTH-06).
