# 11 — Product backlog (nháp)

> **Sinh tự động** bởi `tools/gen_backlog.py` từ [đặc tả use case](03-dac-ta-use-case/00-muc-luc.md); không sửa tay. Sửa đặc tả rồi chạy lại `python3 tools/gen_backlog.py`.
> Quy ước (QĐ-10..12): mỗi use case thuộc MVP (gốc hoặc con) là một story; Gherkin là **bản nháp** sinh từ tiền điều kiện, luồng chính, hậu điều kiện và từng nhánh thay thế, nhóm rà lại trước khi chép sang GitHub Projects. Story point để trống, điền sau planning poker. Use case sau MVP gom thành epic ở §3.

## 1. Tổng hợp

| Giai đoạn | Số story | Use case |
|---|---|---|
| P0 | 6 | UC-01.01, UC-01.01a, UC-01.01b, UC-01.01c, UC-01.02, UC-01.02a |
| P1 | 51 | UC-01.01d, UC-02.01, UC-02.02, UC-02.02a, UC-02.03, UC-02.04, UC-02.05, UC-03.01, UC-03.02, UC-03.03, UC-03.04, UC-03.05, UC-03.06, UC-03.07, UC-03.08, UC-03.09, UC-04.01, UC-04.01a, UC-04.02, UC-04.02a, UC-04.02b, UC-04.02d, UC-04.02e, UC-04.03, UC-04.03a, UC-04.04, UC-04.05, UC-04.06, UC-04.10, UC-05.01, UC-05.01a, UC-05.02c, UC-05.03, UC-05.06, UC-05.06a, UC-05.06b, UC-05.06c, UC-05.06e, UC-05.06f, UC-05.08, UC-05.09, UC-05.10, UC-05.10a, UC-05.10c, UC-05.17, UC-10.01, UC-10.03, UC-10.04, UC-10.05, UC-10.09, UC-10.11 |
| P2 | 21 | UC-01.03, UC-01.05, UC-03.01a, UC-03.01b, UC-03.02a, UC-04.07, UC-04.08, UC-04.09, UC-05.07, UC-05.07a, UC-05.07b, UC-05.07c, UC-05.11, UC-05.11a, UC-05.12, UC-05.13, UC-05.13a, UC-05.13b, UC-05.18, UC-09.05, UC-10.12 |
| P3 | 26 | UC-01.04, UC-02.09, UC-06.01, UC-06.01a, UC-06.02, UC-06.02a, UC-06.03, UC-06.04, UC-06.05, UC-06.06, UC-06.08, UC-06.09, UC-06.10, UC-06.11, UC-06.11a, UC-06.13, UC-06.15, UC-06.16, UC-06.16a, UC-06.17, UC-09.01, UC-09.03, UC-09.03a, UC-09.06, UC-09.08, UC-09.08a |
| **MVP** | **104** | |
| Sau MVP (epic) | 61 use case | §3 |

## 2. Story thuộc MVP

### Giai đoạn P0

#### ST-01-01 Đăng nhập qua SSO

| Mục | Nội dung |
|---|---|
| Story | Là **Guest**, tôi muốn đăng nhập qua SSO |
| Mô tả | Người dùng đăng nhập vào ứng dụng bằng tài khoản SSO có sẵn, nhận phiên làm việc và hồ sơ cục bộ |
| Use case | [UC-01.01](03-dac-ta-use-case/m01-tich-hop-sso.md#uc-0101) · M01 — Tích hợp SSO & hồ sơ |
| Giai đoạn | P0 |
| Truy vết | FR-AUTH-01..04, 06, 07, 11, 12; BR-30, BR-31; NFR-SEC-02; seq-dang-nhap-sso |
| Story point | |

```gherkin
Feature: UC-01.01 Đăng nhập qua SSO
  Background:
    Given Chưa có phiên hợp lệ; ứng dụng đã được đăng ký client_id với SSO

  Scenario: Luồng chính
    When Guest bấm "Đăng nhập" hoặc mở một trang cần đăng nhập
    And Hệ thống ghi nhớ returnTo (chỉ đường dẫn nội bộ), tạo state, nonce, code_verifier và chuyển hướng tới authorization_endpoint của SSO
    And Người dùng đăng nhập trên trang SSO. Nếu chưa có tài khoản thì đăng ký ngay trên SSO; nếu SSO đã có phiên thì bước này được bỏ qua
    And SSO chuyển về /auth/callback?code&state
    And Hệ thống thực hiện UC-01.01a (xác thực ID token)
    And Hệ thống thực hiện UC-01.01b (tạo hoặc đồng bộ hồ sơ)
    And Hệ thống tạo phiên (cookie HttpOnly; Secure; SameSite=Lax), lưu refresh token đã mã hóa phía server
    And Nếu người dùng chưa đồng ý xử lý dữ liệu (hoặc thông báo đã đổi phiên bản), hệ thống thực hiện UC-01.01d
    And Hệ thống thực hiện UC-01.01c (quay về trang đã yêu cầu)
    Then có phiên ứng dụng (cookie httpOnly); users tồn tại, đồng bộ với claims và đã đồng ý xử lý dữ liệu; người dùng ở trang đã yêu cầu

  Scenario: 3a Người dùng hủy trên SSO hoặc SSO trả error
    Given luồng chính đã tới bước 3
    When Người dùng hủy trên SSO hoặc SSO trả error
    Then quay về trang chủ, hiện "Đăng nhập không thành công"

  Scenario: 5a state không khớp, token sai chữ ký hoặc hết hạn
    Given luồng chính đã tới bước 5
    When state không khớp, token sai chữ ký hoặc hết hạn
    Then từ chối, ghi log bảo mật, không tạo phiên

  Scenario: 6a Hồ sơ cục bộ ở trạng thái LOCKED (vi phạm chính sách hoặc tài khoản SSO bị khóa)
    Given luồng chính đã tới bước 6
    When Hồ sơ cục bộ ở trạng thái LOCKED (vi phạm chính sách hoặc tài khoản SSO bị khóa)
    Then hiện thông báo, không tạo phiên

  Scenario: 6b Lần đầu đăng nhập và email không có trong danh sách mời (BR-30)
    Given luồng chính đã tới bước 6
    When Lần đầu đăng nhập và email không có trong danh sách mời (BR-30)
    Then hiện "Bạn chưa được mời tham gia beta", không tạo hồ sơ, không tạo phiên (UC-01.01b nhánh 2a)

  Scenario: 8a Người dùng không đồng ý
    Given luồng chính đã tới bước 8
    When Người dùng không đồng ý
    Then đăng xuất (UC-01.01d nhánh 3a)

  Scenario: *a SSO không phản hồi (timeout 10 s)
    When SSO không phản hồi (timeout 10 s)
    Then hiện trang lỗi thân thiện, gợi ý thử lại sau
```

#### ST-01-01a Xác thực ID token

| Mục | Nội dung |
|---|---|
| Story | Là **Hệ thống (BFF)**, tôi muốn xác thực ID token |
| Mô tả | Đổi authorization code lấy token và xác thực ID token trước khi tin bất kỳ claim nào |
| Use case | [UC-01.01a](03-dac-ta-use-case/m01-tich-hop-sso.md#uc-0101a) · M01 — Tích hợp SSO & hồ sơ |
| Giai đoạn | P0 |
| Truy vết | FR-AUTH-01..04; NFR-SEC-02; API 2.1 `/auth/callback`; seq-dang-nhap-sso |
| Story point | |

```gherkin
Feature: UC-01.01a Xác thực ID token
  Background:
    Given Có code và state ở callback; phiên đăng nhập tạm (UC-01.01 bước 2) còn lưu state, nonce, code_verifier, returnTo

  Scenario: Luồng chính
    When Hệ thống so state ở callback với state đã lưu trong phiên đăng nhập tạm, rồi xóa giá trị này (chỉ dùng một lần)
    And Hệ thống gửi code cùng code_verifier (PKCE) tới token_endpoint của SSO và nhận token
    And Hệ thống lấy JWKS từ jwks_uri (có cache; tự làm mới khi gặp kid chưa biết)
    And Hệ thống kiểm tra chữ ký, iss, aud (= client_id), exp, iat và nonce khớp với giá trị đã lưu
    And Hệ thống trả claims đã xác thực cho UC-01.01b
    Then claims hợp lệ (sub, email, name, picture, locale, roles) được chuyển cho UC-01.01b

  Scenario: 1a state thiếu, không khớp hoặc đã dùng
    When state thiếu, không khớp hoặc đã dùng
    Then từ chối, ghi log bảo mật, không gọi SSO (UC-01.01 nhánh 5a)

  Scenario: 2a token_endpoint trả lỗi (code hết hạn hoặc đã dùng) hoặc quá 10 s không phản hồi
    Given luồng chính đã tới bước 2
    When token_endpoint trả lỗi (code hết hạn hoặc đã dùng) hoặc quá 10 s không phản hồi
    Then dừng, báo "Đăng nhập không thành công, hãy thử lại"

  Scenario: 3a Không tải được JWKS và chưa có cache
    Given luồng chính đã tới bước 3
    When Không tải được JWKS và chưa có cache
    Then dừng; không bỏ qua bước kiểm tra chữ ký

  Scenario: 4a Bất kỳ kiểm tra nào ở bước 4 thất bại
    Given luồng chính đã tới bước 4
    When Bất kỳ kiểm tra nào ở bước 4 thất bại
    Then từ chối, ghi log, không lưu token
```

#### ST-01-01b Tạo / đồng bộ hồ sơ cục bộ (JIT)

| Mục | Nội dung |
|---|---|
| Story | Là **Hệ thống**, tôi muốn tạo / đồng bộ hồ sơ cục bộ (JIT) |
| Mô tả | Tạo hồ sơ cục bộ ở lần đăng nhập đầu (JIT) cho người được mời, hoặc đồng bộ hồ sơ theo claims ở các lần sau; không bao giờ lưu mật khẩu |
| Use case | [UC-01.01b](03-dac-ta-use-case/m01-tich-hop-sso.md#uc-0101b) · M01 — Tích hợp SSO & hồ sơ |
| Giai đoạn | P0 |
| Truy vết | FR-AUTH-04, 07, 11; FR-BIL-05, 10; BR-28, BR-30; IC-16; D-08; API 2.1 `/auth/callback`, `/me`; seq-dang-nhap-sso |
| Story point | |

```gherkin
Feature: UC-01.01b Tạo / đồng bộ hồ sơ cục bộ (JIT)
  Background:
    Given Claims đã xác thực từ UC-01.01a

  Scenario: Luồng chính
    When Hệ thống tìm users theo sso_subject = sub
    And Chưa có: hệ thống kiểm tra email (chữ thường) có trong beta_invites chưa bị thu hồi (BR-30). Có: trong một giao dịch, tạo users (chưa đồng ý dữ liệu), tạo wallets (số dư 0), ghi bút toán TRIAL_GRANT $2 vào ví (BR-28) và đặt beta_invites.used_by_user_id
    And Đã có: cập nhật email, display_name, avatar_url theo claims; locale chỉ lấy từ claim khi người dùng chưa tự đổi trong ứng dụng [ĐX]
    And Đặt role = ADMIN nếu claim roles chứa vai trò quản trị, ngược lại USER (FR-AUTH-07)
    And Cập nhật last_login_at và trả hồ sơ cho UC-01.01 bước 7
    Then có đúng một users ứng với sso_subject = sub, dữ liệu khớp claims; người dùng mới có ví với tiền dùng thử $2 (TRIAL_GRANT), trạng thái Free

  Scenario: 1a Hai callback đồng thời cho cùng sub
    When Hai callback đồng thời cho cùng sub
    Then ràng buộc duy nhất của sso_subject bảo đảm chỉ một bản ghi; giao dịch thua thực hiện lại bước 1 và đi theo nhánh "đã có"

  Scenario: 2a Email không có trong danh sách mời, hoặc lời mời đã bị thu hồi
    Given luồng chính đã tới bước 2
    When Email không có trong danh sách mời, hoặc lời mời đã bị thu hồi
    Then không tạo users, trả 403 NOT_INVITED cho UC-01.01 nhánh 6b. Ghi log để Admin xem ai đã thử đăng nhập [ĐX]

  Scenario: 2b Claim email trống hoặc chưa được SSO xác minh
    Given luồng chính đã tới bước 2
    When Claim email trống hoặc chưa được SSO xác minh
    Then coi như chưa được mời

  Scenario: 2c Lời mời đã được dùng bởi một hồ sơ khác (cùng email, khác sub)
    Given luồng chính đã tới bước 2
    When Lời mời đã được dùng bởi một hồ sơ khác (cùng email, khác sub)
    Then không tặng thêm tiền dùng thử (IC-16); Admin xử lý thủ công

  Scenario: 2d Cấu hình beta_invite_only = false (mở rộng sau beta)
    Given luồng chính đã tới bước 2
    When Cấu hình beta_invite_only = false (mở rộng sau beta)
    Then bỏ qua kiểm tra danh sách mời

  Scenario: 3a users.status = LOCKED
    Given luồng chính đã tới bước 3
    When users.status = LOCKED
    Then trả về cho UC-01.01 nhánh 6a (không tạo phiên)

  Scenario: 3b Người dùng đã có hồ sơ nhưng bị gỡ khỏi danh sách mời
    Given luồng chính đã tới bước 3
    When Người dùng đã có hồ sơ nhưng bị gỡ khỏi danh sách mời
    Then vẫn đăng nhập bình thường (BR-30)

  Scenario: *a Lỗi ghi dữ liệu
    When Lỗi ghi dữ liệu
    Then rollback toàn bộ (kể cả ví và tiền dùng thử), báo lỗi chung, người dùng có thể đăng nhập lại
```

#### ST-01-01c Quay về trang đã yêu cầu

| Mục | Nội dung |
|---|---|
| Story | Là **Hệ thống**, tôi muốn quay về trang đã yêu cầu |
| Mô tả | Đưa người dùng về đúng trang họ yêu cầu trước khi đăng nhập, đồng thời chặn open redirect |
| Use case | [UC-01.01c](03-dac-ta-use-case/m01-tich-hop-sso.md#uc-0101c) · M01 — Tích hợp SSO & hồ sơ |
| Giai đoạn | P0 |
| Truy vết | NFR-SEC-02 (`returnTo` chỉ cho phép đường dẫn nội bộ); API 2.1 `/auth/login`; seq-dang-nhap-sso |
| Story point | |

```gherkin
Feature: UC-01.01c Quay về trang đã yêu cầu
  Background:
    Given Phiên ứng dụng vừa được tạo; có thể có returnTo đã lưu ở UC-01.01 bước 2

  Scenario: Luồng chính
    When Hệ thống đọc returnTo đã lưu và xóa khỏi phiên đăng nhập tạm
    And Hệ thống kiểm tra lại returnTo (đã kiểm tra một lần ở lúc lưu): phải bắt đầu bằng một dấu /, không bắt đầu bằng //, không chứa scheme, host hoặc \
    And Hợp lệ: trả 302 tới returnTo (vd. /invites/{token} để chấp nhận lời mời, UC-02.08)
    And Không hợp lệ hoặc không có: trả 302 tới /projects
    Then người dùng ở trang đã yêu cầu hoặc /projects

  Scenario: 2a returnTo trỏ tới trang người dùng không còn quyền truy cập
    Given luồng chính đã tới bước 2
    When returnTo trỏ tới trang người dùng không còn quyền truy cập
    Then trang đích tự hiển thị lỗi 404 (không tiết lộ sự tồn tại), người dùng dùng điều hướng bình thường
```

#### ST-01-02 Đăng xuất

| Mục | Nội dung |
|---|---|
| Story | Là **User**, tôi muốn đăng xuất |
| Mô tả | Kết thúc phiên ứng dụng và phiên SSO |
| Use case | [UC-01.02](03-dac-ta-use-case/m01-tich-hop-sso.md#uc-0102) · M01 — Tích hợp SSO & hồ sơ |
| Giai đoạn | P0 |
| Truy vết | FR-AUTH-05; seq-dang-nhap-sso |
| Story point | |

```gherkin
Feature: UC-01.02 Đăng xuất
  Background:
    Given Đang có phiên

  Scenario: Luồng chính
    When User bấm "Đăng xuất"
    And Hệ thống thu hồi user_sessions hiện tại và xóa cookie
    And Hệ thống thực hiện UC-01.02a
    And SSO kết thúc phiên và chuyển về trang chủ ứng dụng
    Then phiên ứng dụng bị thu hồi, token đã lưu bị xóa, phiên SSO kết thúc

  Scenario: 3a SSO không có end_session_endpoint
    Given luồng chính đã tới bước 3
    When SSO không có end_session_endpoint
    Then chỉ đăng xuất cục bộ, hiện ghi chú "Bạn vẫn đăng nhập ở các ứng dụng khác dùng chung SSO"
```

#### ST-01-02a Kết thúc phiên SSO

| Mục | Nội dung |
|---|---|
| Story | Là **Hệ thống**, tôi muốn kết thúc phiên SSO |
| Mô tả | Báo cho SSO kết thúc phiên (RP-initiated logout) để người dùng không còn đăng nhập ở SSO sau khi đăng xuất khỏi ứng dụng |
| Use case | [UC-01.02a](03-dac-ta-use-case/m01-tich-hop-sso.md#uc-0102a) · M01 — Tích hợp SSO & hồ sơ |
| Giai đoạn | P0 |
| Truy vết | FR-AUTH-05; API 2.1 `POST /auth/logout`; seq-dang-nhap-sso |
| Story point | |

```gherkin
Feature: UC-01.02a Kết thúc phiên SSO
  Background:
    Given Phiên ứng dụng vừa bị thu hồi (UC-01.02 bước 2); còn id_token_hint đã mã hóa của phiên đó

  Scenario: Luồng chính
    When Hệ thống giải mã id_token_hint của phiên vừa thu hồi, rồi xóa mọi token đã lưu của phiên
    And Hệ thống lấy end_session_endpoint từ metadata (discovery) của SSO
    And Hệ thống dựng URL end_session_endpoint?id_token_hint=…&post_logout_redirect_uri=… (địa chỉ trang chủ đã đăng ký với SSO)
    And API trả { logoutUrl }; client chuyển hướng trình duyệt tới URL này
    And SSO kết thúc phiên và chuyển về trang chủ ứng dụng
    Then phiên SSO kết thúc; trình duyệt về trang chủ

  Scenario: 2a SSO không có end_session_endpoint
    Given luồng chính đã tới bước 2
    When SSO không có end_session_endpoint
    Then chỉ đăng xuất cục bộ, hiện ghi chú "Bạn vẫn đăng nhập ở các ứng dụng khác dùng chung SSO" (UC-01.02 nhánh 3a)

  Scenario: 3a Không còn id_token_hint (hết hạn hoặc mất)
    Given luồng chính đã tới bước 3
    When Không còn id_token_hint (hết hạn hoặc mất)
    Then vẫn gọi end_session_endpoint không kèm hint; SSO có thể hỏi xác nhận đăng xuất

  Scenario: 5a SSO báo lỗi hoặc không phản hồi
    Given luồng chính đã tới bước 5
    When SSO báo lỗi hoặc không phản hồi
    Then người dùng vẫn ở trạng thái đã đăng xuất khỏi ứng dụng; không thử lại tự động
```

### Giai đoạn P1

#### ST-01-01d Đồng ý xử lý dữ liệu cá nhân

| Mục | Nội dung |
|---|---|
| Story | Là **User**, tôi muốn đồng ý xử lý dữ liệu cá nhân |
| Mô tả | Người dùng đọc thông báo xử lý dữ liệu cá nhân và đồng ý trước khi dùng ứng dụng, theo Nghị định 13/2023 |
| Use case | [UC-01.01d](03-dac-ta-use-case/m01-tich-hop-sso.md#uc-0101d) · M01 — Tích hợp SSO & hồ sơ |
| Giai đoạn | P1 |
| Truy vết | FR-AUTH-12; BR-31; C-02; NFR-PRV-01; API 2.1 `GET /me`, `POST /me:consent`; seq-dang-nhap-sso |
| Story point | |

```gherkin
Feature: UC-01.01d Đồng ý xử lý dữ liệu cá nhân
  Background:
    Given Có phiên ứng dụng; users.consented_at rỗng hoặc consent_version khác phiên bản thông báo hiện hành

  Scenario: Luồng chính
    When Hệ thống hiện màn hình thông báo (phiên bản lấy từ system_settings.consent_notice_version): dữ liệu thu thập (email, tên, ảnh đại diện từ SSO; truyện, ảnh, nhạc tải lên; video tạo ra; nhật ký sử dụng), mục đích (thử nghiệm đồ án tốt nghiệp, phiếu khảo sát), nơi xử lý (nhà cung cấp AI và lưu trữ), thời hạn (xóa toàn bộ sau ngày bảo vệ), quyền yêu cầu xóa sớm và kênh liên hệ
    And Người dùng tích "Tôi đã đọc và đồng ý" rồi bấm "Tiếp tục"
    And Hệ thống gọi POST /me:consent {noticeVersion}, ghi consented_at = now() và consent_version
    And Hệ thống quay về UC-01.01 bước 9
    Then users.consented_at và consent_version được ghi; người dùng vào được ứng dụng

  Scenario: 2a Chưa tích ô đồng ý
    Given luồng chính đã tới bước 2
    When Chưa tích ô đồng ý
    Then nút "Tiếp tục" bị vô hiệu hóa

  Scenario: 3a Người dùng bấm "Không đồng ý"
    Given luồng chính đã tới bước 3
    When Người dùng bấm "Không đồng ý"
    Then hệ thống đăng xuất (UC-01.02); hồ sơ và ví vẫn giữ để lần sau đồng ý thì dùng tiếp

  Scenario: 3b noticeVersion gửi lên khác phiên bản hiện hành (thông báo vừa đổi)
    Given luồng chính đã tới bước 3
    When noticeVersion gửi lên khác phiên bản hiện hành (thông báo vừa đổi)
    Then 409, tải lại thông báo mới

  Scenario: *a Thông báo đổi phiên bản sau khi người dùng đã đồng ý
    When Thông báo đổi phiên bản sau khi người dùng đã đồng ý
    Then lần đăng nhập hoặc gia hạn phiên kế tiếp hiện lại màn hình này
```

#### ST-02-01 Xem danh sách dự án

| Mục | Nội dung |
|---|---|
| Story | Là **User**, tôi muốn xem danh sách dự án |
| Mô tả | Xem các dự án mình sở hữu hoặc tham gia để mở tiếp |
| Use case | [UC-02.01](03-dac-ta-use-case/m02-du-an-cong-tac.md#uc-0201) · M02 — Quản lý dự án & cộng tác |
| Giai đoạn | P1 |
| Truy vết | FR-PRJ-01 |
| Story point | |

```gherkin
Feature: UC-02.01 Xem danh sách dự án
  Background:
    Given Đã đăng nhập

  Scenario: Luồng chính
    When User mở trang Projects
    And Hệ thống trả các dự án mà User là Owner hoặc Editor, sắp theo ngày cập nhật: tiêu đề, ảnh đại diện, số chương, style, bước hiện tại của luồng (1–6), trạng thái, vai trò của User
    And User chọn một dự án; hệ thống mở Studio ở màn hình của bước hiện tại
    Then danh sách hiển thị đúng quyền

  Scenario: 2c User nhập từ khóa vào ô tìm hoặc chọn bộ lọc trạng thái
    Given luồng chính đã tới bước 2
    When User nhập từ khóa vào ô tìm hoặc chọn bộ lọc trạng thái
    Then hệ thống lọc theo tiêu đề (không phân biệt hoa thường, dấu) và trạng thái *In Progress* / *Done* (suy ra từ trạng thái chương, FR-PRJ-01); danh sách phân trang. Không có kết quả: hiện "Không tìm thấy dự án"

  Scenario: 2a Chưa có dự án nào
    Given luồng chính đã tới bước 2
    When Chưa có dự án nào
    Then hiện trạng thái trống với hai nút "Import truyện" (UC-02.02) và "Tạo dự án trống" (UC-02.03)

  Scenario: 2b Dự án đang chờ xóa (soft delete)
    Given luồng chính đã tới bước 2
    When Dự án đang chờ xóa (soft delete)
    Then không hiển thị
```

#### ST-02-02 Nhập truyện giữ nguyên văn (Import)

| Mục | Nội dung |
|---|---|
| Story | Là **User (trở thành Owner)**, tôi muốn nhập truyện giữ nguyên văn (Import) |
| Mô tả | Bước 1 của luồng chính: đưa văn bản truyện vào hệ thống để tạo dự án, giữ nguyên từng chữ |
| Use case | [UC-02.02](03-dac-ta-use-case/m02-du-an-cong-tac.md#uc-0202) · M02 — Quản lý dự án & cộng tác |
| Giai đoạn | P1 |
| Truy vết | FR-PRJ-02, FR-PRJ-03; FR-BIL-12; BR-19, BR-21, BR-27; seq-import-chia-chuong |
| Story point | |

```gherkin
Feature: UC-02.02 Nhập truyện giữ nguyên văn (Import)
  Background:
    Given Đã đăng nhập; chưa vượt giới hạn số dự án của tài khoản Free (BR-27)

  Scenario: Luồng chính
    When User dán văn bản hoặc chọn file (.txt, .md, .docx)
    And Hệ thống thực hiện UC-02.02a và hiển thị bản xem trước (số ký tự, số đoạn)
    And User nhập tiêu đề, chọn style và tỷ lệ khung hình video (16:9 / 9:16 / 1:1)
    And Hệ thống tạo trong một giao dịch: Project, ProjectMember(OWNER), SourceText, Chapter #1 (version = 1)
    And Hệ thống mở Studio ở màn hình Write và gợi ý bước 2 "Chia chương" (UC-03.03)
    Then có Project, ProjectMember(OWNER), SourceText (kèm sha256), Chapter #1 chứa toàn văn

  Scenario: 2a File sai định dạng, > 2 MB hoặc > 500.000 ký tự
    Given luồng chính đã tới bước 2
    When File sai định dạng, > 2 MB hoặc > 500.000 ký tự
    Then báo lỗi, giữ nguyên form

  Scenario: 1a Tài khoản Free đã có 1 dự án
    When Tài khoản Free đã có 1 dự án
    Then 403 FREE_LIMIT_REACHED, hiện thông báo giới hạn và gợi ý nạp tiền (UC-09.03)

  Scenario: 2b File .docx có định dạng (đậm, nghiêng, bảng)
    Given luồng chính đã tới bước 2
    When File .docx có định dạng (đậm, nghiêng, bảng)
    Then chỉ giữ văn bản, không bỏ chữ nào

  Scenario: 2c Văn bản có ký hiệu trình bày (*Bố*, […], # …, ---)
    Given luồng chính đã tới bước 2
    When Văn bản có ký hiệu trình bày (*Bố*, […], # …, ---)
    Then giữ nguyên trong chương; chỉ bỏ khi đọc (08 §6)

  Scenario: 4a Lỗi DB
    Given luồng chính đã tới bước 4
    When Lỗi DB
    Then rollback, hiện lỗi, giữ nội dung trên form để thử lại
```

#### ST-02-02a Kiểm tra & chuẩn hóa kỹ thuật

| Mục | Nội dung |
|---|---|
| Story | Là **Hệ thống**, tôi muốn kiểm tra & chuẩn hóa kỹ thuật |
| Mô tả | Kiểm tra file hoặc văn bản đưa vào và chuẩn hóa ở mức kỹ thuật, không đổi một chữ nào (BR-19, BR-21) |
| Use case | [UC-02.02a](03-dac-ta-use-case/m02-du-an-cong-tac.md#uc-0202a) · M02 — Quản lý dự án & cộng tác |
| Giai đoạn | P1 |
| Truy vết | FR-PRJ-02, FR-PRJ-03; BR-19, BR-21; NFR-SEC-10, NFR-INT-05; 08 §5; seq-import-chia-chuong |
| Story point | |

```gherkin
Feature: UC-02.02a Kiểm tra & chuẩn hóa kỹ thuật
  Background:
    Given Có văn bản dán hoặc file .txt, .md, .docx

  Scenario: Luồng chính
    When Hệ thống kiểm tra MIME thật (không tin phần mở rộng), kích thước file ≤ 2 MB, số ký tự ≤ 500.000
    And Hệ thống trích văn bản thuần: .txt và .md giữ nguyên nội dung (không bỏ ký hiệu markdown); .docx chỉ lấy chữ, bỏ định dạng, bảng và hình
    And Hệ thống chuẩn hóa Unicode NFC, thống nhất ký tự xuống dòng về \n, bỏ ký tự điều khiển vô hình
    And Hệ thống ghi normalization_log: loại biến đổi và số lần (không ghi lại nội dung văn bản)
    And Hệ thống tính sha256 của văn bản đã chuẩn hóa và trả về số ký tự, số đoạn cho bản xem trước
    Then có văn bản sạch về kỹ thuật kèm char_count, sha256, normalization_log

  Scenario: 1a Sai định dạng, MIME không khớp phần mở rộng, file hỏng hoặc có mật khẩu
    When Sai định dạng, MIME không khớp phần mở rộng, file hỏng hoặc có mật khẩu
    Then báo lỗi cụ thể, giữ nguyên form

  Scenario: 1b Vượt 2 MB hoặc 500.000 ký tự
    When Vượt 2 MB hoặc 500.000 ký tự
    Then báo lỗi và nêu giới hạn

  Scenario: 2a Không giải mã được sang UTF-8
    Given luồng chính đã tới bước 2
    When Không giải mã được sang UTF-8
    Then báo lỗi, không đoán bảng mã

  Scenario: 3a Văn bản không đổi sau chuẩn hóa
    Given luồng chính đã tới bước 3
    When Văn bản không đổi sau chuẩn hóa
    Then normalization_log ghi 0 biến đổi (round-trip giống byte, NFR-INT-05)
```

#### ST-02-03 Tạo dự án trống

| Mục | Nội dung |
|---|---|
| Story | Là **User**, tôi muốn tạo dự án trống |
| Mô tả | Tạo dự án không có văn bản để viết trực tiếp trong Workspace |
| Use case | [UC-02.03](03-dac-ta-use-case/m02-du-an-cong-tac.md#uc-0203) · M02 — Quản lý dự án & cộng tác |
| Giai đoạn | P1 |
| Truy vết | FR-PRJ-04; FR-BIL-12; BR-27; seq-import-chia-chuong |
| Story point | |

```gherkin
Feature: UC-02.03 Tạo dự án trống
  Background:
    Given Đã đăng nhập; chưa vượt giới hạn số dự án của tài khoản Free (BR-27)

  Scenario: Luồng chính
    When User nhập tiêu đề, chọn style và tỷ lệ khung hình
    And Hệ thống tạo dự án và Chapter #1 trống
    And Hệ thống mở Workspace (UC-03.02)
    Then Project + ProjectMember(OWNER) + một chương trống

  Scenario: 1a Tài khoản Free đã có 1 dự án
    When Tài khoản Free đã có 1 dự án
    Then 403 FREE_LIMIT_REACHED, hiện thông báo giới hạn và gợi ý nạp tiền (UC-09.03)
```

#### ST-02-04 Cài đặt dự án

| Mục | Nội dung |
|---|---|
| Story | Là **Owner**, tôi muốn cài đặt dự án |
| Mô tả | Đổi style, mô hình ảnh, ngôn ngữ, thời lượng mục tiêu mỗi ảnh, tỷ lệ khung hình, hiển thị |
| Use case | [UC-02.04](03-dac-ta-use-case/m02-du-an-cong-tac.md#uc-0204) · M02 — Quản lý dự án & cộng tác |
| Giai đoạn | P1 |
| Truy vết | FR-PRJ-07; BR-04 |
| Story point | |

```gherkin
Feature: UC-02.04 Cài đặt dự án
  Background:
    Given Là Owner của dự án

  Scenario: Luồng chính
    When Owner mở Settings
    And Owner đổi một thuộc tính
    And Hệ thống lưu ngay (If-Match) và thông báo "Đã lưu"
    Then projects cập nhật (version tăng); thay đổi áp dụng cho các lần sinh sau

  Scenario: 2a Đổi style khi đã có ảnh
    Given luồng chính đã tới bước 2
    When Đổi style khi đã có ảnh
    Then hệ thống hỏi có muốn "Sinh lại tất cả ảnh tham chiếu" (UC-04.03a) và hiện giá; ảnh shot cũ giữ nguyên cho đến khi sinh lại

  Scenario: 2b Đổi tỷ lệ khung hình khi đã có timeline
    Given luồng chính đã tới bước 2
    When Đổi tỷ lệ khung hình khi đã có timeline
    Then cảnh báo ảnh sẽ được crop/fit theo khung mới (UC-06.06)

  Scenario: 3a Xung đột version
    Given luồng chính đã tới bước 3
    When Xung đột version
    Then tải lại cài đặt mới nhất, yêu cầu chọn lại

  Scenario: *a Editor mở Settings
    When Editor mở Settings
    Then chỉ xem, không sửa được
```

#### ST-02-05 Xóa dự án

| Mục | Nội dung |
|---|---|
| Story | Là **Owner**, tôi muốn xóa dự án |
| Mô tả | Xóa dự án và toàn bộ dữ liệu liên quan |
| Use case | [UC-02.05](03-dac-ta-use-case/m02-du-an-cong-tac.md#uc-0205) · M02 — Quản lý dự án & cộng tác |
| Giai đoạn | P1 |
| Truy vết | FR-PRJ-01; BR-04; 04 §5 |
| Story point | |

```gherkin
Feature: UC-02.05 Xóa dự án
  Background:
    Given Là Owner; không có job đang chạy (hoặc chấp nhận hủy)

  Scenario: Luồng chính
    When Owner chọn "Xóa dự án"
    And Hệ thống hiện hệ quả (số chương, tư liệu, bản xuất, thành viên bị ảnh hưởng)
    And Owner nhập tên dự án để xác nhận
    And Hệ thống hủy các job QUEUED (RELEASE toàn bộ tiền đang giữ), đặt deleted_at, thông báo cho thành viên (khi có cộng tác, sau MVP). Tài khoản Free được tạo dự án mới sau khi xóa
    Then dự án soft delete, mọi thành viên mất quyền ngay; xóa cứng cùng media sau 30 ngày

  Scenario: 2a Có job đang RUNNING
    Given luồng chính đã tới bước 2
    When Có job đang RUNNING
    Then chờ job kết thúc rồi mới xóa, hoặc Owner chọn "Hủy và xóa"

  Scenario: *a Owner muốn khôi phục trong 30 ngày
    When Owner muốn khôi phục trong 30 ngày
    Then liên hệ hỗ trợ hoặc dùng mục "Dự án đã xóa" [ĐX]
```

#### ST-03-01 Xem văn bản gốc

| Mục | Nội dung |
|---|---|
| Story | Là **Owner**, tôi muốn xem văn bản gốc |
| Mô tả | Xem toàn văn đã import, kèm số ký tự, số chương và ranh giới chương hiện tại |
| Use case | [UC-03.01](03-dac-ta-use-case/m03-ban-thao-chuong.md#uc-0301) · M03 — Bản thảo & chương |
| Giai đoạn | P1 |
| Truy vết | FR-MAN-01 |
| Story point | |

```gherkin
Feature: UC-03.01 Xem văn bản gốc
  Background:
    Given Dự án có SourceText

  Scenario: Luồng chính
    When Editor mở màn hình Write
    And Hệ thống hiển thị toàn văn ghép từ các chương theo thứ tự, đánh dấu ranh giới chương; mỗi khoảng giữa hai đoạn có nút "Split here"
    And Editor đọc, có thể chuyển sang UC-03.03, UC-03.04
    Then hiển thị văn bản và các điểm chia
```

#### ST-03-02 Soạn thảo trong Workspace

| Mục | Nội dung |
|---|---|
| Story | Là **Owner**, tôi muốn soạn thảo trong Workspace |
| Mô tả | Viết và sửa văn bản mọi chương trong một trình soạn thảo cuộn liền mạch |
| Use case | [UC-03.02](03-dac-ta-use-case/m03-ban-thao-chuong.md#uc-0302) · M03 — Bản thảo & chương |
| Giai đoạn | P1 |
| Truy vết | FR-MAN-02, 11; FR-NAR-09; BR-05, BR-06, BR-21; seq-doi-ranh-gioi-shot |
| Story point | |

```gherkin
Feature: UC-03.02 Soạn thảo trong Workspace
  Background:
    Given Là thành viên dự án; chương không bị khóa

  Scenario: Luồng chính
    When Editor mở Workspace; hệ thống tải mọi chương kèm ETag. Chương đã có storyboard hiện hành hiển thị vạch ranh giới shot mảnh giữa các câu, kèm số shot (GET …/shot-boundaries)
    And Editor sửa văn bản hoặc tiêu đề một chương
    And Hệ thống tự lưu sau 2 s không gõ (PATCH + If-Match)
    And Hệ thống tăng version, lưu snapshot, cập nhật "người sửa cuối", phát chapter.updated
    And Nếu chương đã có tư liệu, hệ thống so hash đoạn nguồn từng shot và đánh dấu shot OUTDATED
    Then chương được lưu với version mới; chapter_versions có snapshot; thuyết minh của shot có đoạn nguồn bị đổi chuyển OUTDATED (BR-06)

  Scenario: 3a 409
    Given luồng chính đã tới bước 3
    When 409
    Then chuyển sang UC-02.10

  Scenario: 3b Chương đang bị khóa bởi job
    Given luồng chính đã tới bước 3
    When Chương đang bị khóa bởi job
    Then 423, editor ở chế độ chỉ đọc, hiện "Chương đang được xử lý"

  Scenario: 5a Thay đổi làm đoạn nguồn của nhiều shot lệch
    Given luồng chính đã tới bước 5
    When Thay đổi làm đoạn nguồn của nhiều shot lệch
    Then hiện banner "N shot cần sinh lại thuyết minh" với nút đi tới UC-05.07c

  Scenario: *a Editor muốn dời vạch ranh giới shot
    When Editor muốn dời vạch ranh giới shot
    Then UC-03.02a
```

#### ST-03-03 Gợi ý chia chương bằng AI

| Mục | Nội dung |
|---|---|
| Story | Là **Owner**, tôi muốn gợi ý chia chương bằng AI |
| Mô tả | AI đề xuất vị trí chia chương và tiêu đề; Editor duyệt rồi áp dụng |
| Use case | [UC-03.03](03-dac-ta-use-case/m03-ban-thao-chuong.md#uc-0303) · M03 — Bản thảo & chương |
| Giai đoạn | P1 |
| Truy vết | FR-MAN-04; BR-01, BR-21, BR-27; 08 §3.2 (`SUGGEST_SPLITS`); seq-import-chia-chuong |
| Story point | |

```gherkin
Feature: UC-03.03 Gợi ý chia chương bằng AI
  Background:
    Given Dự án có văn bản

  Scenario: Luồng chính
    When Editor bấm "Suggest chapter splits"
    And Hệ thống hiện giá ước tính; Editor xác nhận; hệ thống giữ tiền (UC-05.17) và tạo job SUGGEST_SPLITS. LLM nhận văn bản đã đánh số đoạn, trả [{startParagraph, title}]. LLM không trả lại văn bản
    And Hệ thống đánh dấu các điểm chia đề xuất trên màn hình Write
    And Editor bỏ chọn điểm không muốn, sửa tiêu đề đề xuất
    And Editor bấm "Áp dụng"; hệ thống thực hiện UC-03.09
    Then danh sách chương mới được ghi nguyên tử qua UC-03.09

  Scenario: 2a Cách chia hiện tại đã khớp
    Given luồng chính đã tới bước 2
    When Cách chia hiện tại đã khớp
    Then báo "Your current chapters already match"

  Scenario: 2b LLM lỗi hoặc trả sai schema sau 2 lần thử
    Given luồng chính đã tới bước 2
    When LLM lỗi hoặc trả sai schema sau 2 lần thử
    Then báo lỗi, gợi ý chia thủ công (UC-03.04)

  Scenario: 5a Các chương bị ảnh hưởng đã có tư liệu hoặc timeline
    Given luồng chính đã tới bước 5
    When Các chương bị ảnh hưởng đã có tư liệu hoặc timeline
    Then hiện cảnh báo trước khi áp dụng (xem UC-03.09)

  Scenario: 5b Tài khoản Free và cách chia cho ra quá 3 chương
    Given luồng chính đã tới bước 5
    When Tài khoản Free và cách chia cho ra quá 3 chương
    Then chỉ áp được tối đa 3 chương, hiện thông báo giới hạn và gợi ý nạp tiền (BR-27)
```

#### ST-03-04 Chia chương tại vị trí

| Mục | Nội dung |
|---|---|
| Story | Là **Owner**, tôi muốn chia chương tại vị trí |
| Mô tả | Chia một chương thành hai tại vị trí giữa hai đoạn văn |
| Use case | [UC-03.04](03-dac-ta-use-case/m03-ban-thao-chuong.md#uc-0304) · M03 — Bản thảo & chương |
| Giai đoạn | P1 |
| Truy vết | FR-MAN-03; BR-27; seq-import-chia-chuong |
| Story point | |

```gherkin
Feature: UC-03.04 Chia chương tại vị trí
  Background:
    Given Chương có ít nhất 2 đoạn

  Scenario: Luồng chính
    When Editor chọn vị trí giữa hai đoạn
    And Editor nhập tiêu đề cho chương mới (mặc định "Chương N+1")
    And Hệ thống thực hiện UC-03.09 với thao tác SPLIT
    Then hai chương liền nhau, nối lại bằng đúng chương cũ

  Scenario: 1a Vị trí ở giữa một đoạn
    When Vị trí ở giữa một đoạn
    Then hệ thống dời về ranh giới đoạn gần nhất và hỏi xác nhận

  Scenario: 3a Tài khoản Free đã có 3 chương
    Given luồng chính đã tới bước 3
    When Tài khoản Free đã có 3 chương
    Then 403 FREE_LIMIT_REACHED, gợi ý nạp tiền (BR-27)
```

#### ST-03-05 Gộp chương vào chương trước

| Mục | Nội dung |
|---|---|
| Story | Là **Owner**, tôi muốn gộp chương vào chương trước |
| Mô tả | Nối chương k vào cuối chương k−1 |
| Use case | [UC-03.05](03-dac-ta-use-case/m03-ban-thao-chuong.md#uc-0305) · M03 — Bản thảo & chương |
| Giai đoạn | P1 |
| Truy vết | FR-MAN-05; seq-import-chia-chuong |
| Story point | |

```gherkin
Feature: UC-03.05 Gộp chương vào chương trước
  Background:
    Given k > 1

  Scenario: Luồng chính
    When Editor chọn "Gộp vào chương trước" và xác nhận
    And Hệ thống thực hiện UC-03.09 với thao tác MERGE_INTO_PREVIOUS
    Then chương k−1 chứa văn bản của cả hai; chương k bị xóa

  Scenario: 1a k là chương đầu
    When k là chương đầu
    Then thao tác bị vô hiệu
```

#### ST-03-06 Dời ranh giới chương

| Mục | Nội dung |
|---|---|
| Story | Là **Owner**, tôi muốn dời ranh giới chương |
| Mô tả | Dời điểm bắt đầu của chương lên hoặc xuống từng đoạn văn |
| Use case | [UC-03.06](03-dac-ta-use-case/m03-ban-thao-chuong.md#uc-0306) · M03 — Bản thảo & chương |
| Giai đoạn | P1 |
| Truy vết | FR-MAN-05; seq-import-chia-chuong |
| Story point | |

```gherkin
Feature: UC-03.06 Dời ranh giới chương
  Background:
    Given Có ít nhất 2 chương

  Scenario: Luồng chính
    When Editor bấm ◀ (đưa đoạn cuối chương trước sang) hoặc ▶ (đưa đoạn đầu chương này sang chương trước)
    And Hệ thống thực hiện UC-03.09 với thao tác MOVE_BOUNDARY
    Then hai chương liền kề thay đổi độ dài, tổng văn bản không đổi

  Scenario: 1a Thao tác làm một chương rỗng
    When Thao tác làm một chương rỗng
    Then bị chặn, gợi ý dùng gộp chương
```

#### ST-03-07 Thêm / xóa / đổi tên chương

| Mục | Nội dung |
|---|---|
| Story | Là **Owner**, tôi muốn thêm / xóa / đổi tên chương |
| Mô tả | Thêm chương trống (cuối hoặc chèn giữa), xóa chương, đổi tiêu đề |
| Use case | [UC-03.07](03-dac-ta-use-case/m03-ban-thao-chuong.md#uc-0307) · M03 — Bản thảo & chương |
| Giai đoạn | P1 |
| Truy vết | FR-MAN-05; seq-import-chia-chuong |
| Story point | |

```gherkin
Feature: UC-03.07 Thêm / xóa / đổi tên chương
  Background:
    Given Là thành viên dự án

  Scenario: Luồng chính
    When Editor chọn thao tác
    And *Thêm:* hệ thống tạo chương trống tại vị trí chọn. *Đổi tên:* lưu tiêu đề (If-Match). *Xóa:* hệ thống hiện hệ quả (văn bản, tư liệu, clip timeline bị xóa theo) và yêu cầu xác nhận
    And Hệ thống ghi, phát sự kiện realtime
    Then danh sách chương cập nhật; order_index liên tục

  Scenario: 2a Xóa chương
    Given luồng chính đã tới bước 2
    When Xóa chương
    Then có nút "Hoàn tác" trong 10 s (NFR-USA-03); văn bản luôn có trong chapter_versions

  Scenario: 2b Xóa chương duy nhất của dự án
    Given luồng chính đã tới bước 2
    When Xóa chương duy nhất của dự án
    Then bị chặn

  Scenario: 2c Thêm chương khi tài khoản Free đã có 3 chương
    Given luồng chính đã tới bước 2
    When Thêm chương khi tài khoản Free đã có 3 chương
    Then 403 FREE_LIMIT_REACHED (BR-27)
```

#### ST-03-08 Sắp xếp lại chương

| Mục | Nội dung |
|---|---|
| Story | Là **Owner**, tôi muốn sắp xếp lại chương |
| Mô tả | Đổi thứ tự chương bằng kéo thả hoặc chọn vị trí |
| Use case | [UC-03.08](03-dac-ta-use-case/m03-ban-thao-chuong.md#uc-0308) · M03 — Bản thảo & chương |
| Giai đoạn | P1 |
| Truy vết | FR-MAN-05; seq-import-chia-chuong |
| Story point | |

```gherkin
Feature: UC-03.08 Sắp xếp lại chương
  Background:
    Given Có ≥ 2 chương

  Scenario: Luồng chính
    When Editor kéo chương tới vị trí mới
    And Hệ thống thực hiện UC-03.09 với thao tác REORDER
    Then thứ tự mới được ghi nguyên tử; timeline cấp dự án đổi thứ tự khối chương tương ứng
```

#### ST-03-09 Tái cấu trúc nguyên tử

| Mục | Nội dung |
|---|---|
| Story | Là **Hệ thống (được gọi từ UC-03.03..08)**, tôi muốn tái cấu trúc nguyên tử |
| Mô tả | Áp một hoặc nhiều thao tác chia, gộp, dời ranh giới, sắp xếp trong một giao dịch |
| Use case | [UC-03.09](03-dac-ta-use-case/m03-ban-thao-chuong.md#uc-0309) · M03 — Bản thảo & chương |
| Giai đoạn | P1 |
| Truy vết | FR-MAN-06; IC-02; BR-05, BR-06, BR-12; seq-import-chia-chuong |
| Story point | |

```gherkin
Feature: UC-03.09 Tái cấu trúc nguyên tử
  Background:
    Given Có danh sách thao tác kèm ifMatch từng chương

  Scenario: Luồng chính
    When Hệ thống mở giao dịch, SELECT … FOR UPDATE các chương liên quan
    And Kiểm tra version từng chương và chương không bị khóa
    And Áp thao tác; cập nhật order_index (unique deferrable); tăng version
    And Với các chương đã có storyboard: tính lại tập shot bị ảnh hưởng, đánh dấu thuyết minh OUTDATED, đánh dấu clip timeline cần cập nhật
    And Commit; phát chapters.restructured
    Then danh sách chương mới ghi trọn vẹn; tư liệu của shot bị ảnh hưởng chuyển OUTDATED

  Scenario: 2a Sai version
    Given luồng chính đã tới bước 2
    When Sai version
    Then rollback, 409 → UC-02.10

  Scenario: 2b Chương bị khóa
    Given luồng chính đã tới bước 2
    When Chương bị khóa
    Then rollback, 423

  Scenario: 3a Bất biến "nối các chương = văn bản cũ" bị vi phạm (lỗi lập trình)
    Given luồng chính đã tới bước 3
    When Bất biến "nối các chương = văn bản cũ" bị vi phạm (lỗi lập trình)
    Then rollback, 500, cảnh báo P1
```

#### ST-04-01 Phân tích tài sản bằng AI

| Mục | Nội dung |
|---|---|
| Story | Là **Owner**, tôi muốn phân tích tài sản bằng AI |
| Mô tả | AI đọc mọi chương, đề xuất nhân vật, địa điểm, đạo cụ lặp lại kèm mô tả và facts |
| Use case | [UC-04.01](03-dac-ta-use-case/m04-the-gioi-truyen.md#uc-0401) · M04 — Thế giới truyện |
| Giai đoạn | P1 |
| Truy vết | FR-WLD-01; BR-01, BR-02; 08 §3.2 (`ANALYZE_ASSETS`); seq-the-gioi-truyen |
| Story point | |

```gherkin
Feature: UC-04.01 Phân tích tài sản bằng AI
  Background:
    Given Có ≥ 1 chương có văn bản

  Scenario: Luồng chính
    When Editor bấm "Analyze"
    And Hệ thống hiện giá ước tính (theo số chương); Editor xác nhận; hệ thống giữ tiền (UC-05.17) và tạo job ANALYZE_ASSETS: LLM đọc từng chương (map), hợp nhất kết quả (reduce), trả danh sách tài sản kèm loại, tên, bí danh, mô tả ngoại hình, facts, các chương xuất hiện
    And Hệ thống đánh dấu mục trùng với tài sản đã có
    And Hệ thống thực hiện UC-04.01a
    And Hệ thống tạo các StoryAsset đã duyệt, đề nghị sinh ảnh tham chiếu (UC-04.03) kèm tổng giá
    Then danh sách đề xuất được duyệt, tài sản được tạo

  Scenario: 2a Không có tài sản lặp lại
    Given luồng chính đã tới bước 2
    When Không có tài sản lặp lại
    Then báo "No recurring cast or places to design"

  Scenario: 2b Dự án rất dài
    Given luồng chính đã tới bước 2
    When Dự án rất dài
    Then phân tích theo lô chương, hiển thị tiến độ

  Scenario: 2c Không đủ số dư
    Given luồng chính đã tới bước 2
    When Không đủ số dư
    Then 402; chạm trần chi tiêu ngày: 503 DAILY_BUDGET_EXCEEDED

  Scenario: 5a Editor từ chối sinh ảnh ngay
    Given luồng chính đã tới bước 5
    When Editor từ chối sinh ảnh ngay
    Then tài sản được tạo chưa có ảnh
```

#### ST-04-01a Duyệt tài sản đề xuất

| Mục | Nội dung |
|---|---|
| Story | Là **Owner**, tôi muốn duyệt tài sản đề xuất |
| Mô tả | Editor quyết định tài sản nào được tạo từ danh sách AI đề xuất; AI không tự tạo gì |
| Use case | [UC-04.01a](03-dac-ta-use-case/m04-the-gioi-truyen.md#uc-0401a) · M04 — Thế giới truyện |
| Giai đoạn | P1 |
| Truy vết | FR-WLD-01; 08 §5 (tên 1–80 ký tự, bí danh ≤ 10, ≤ 200 Story Assets); seq-the-gioi-truyen |
| Story point | |

```gherkin
Feature: UC-04.01a Duyệt tài sản đề xuất
  Background:
    Given Job ANALYZE_ASSETS đã trả danh sách đề xuất (UC-04.01 bước 2–3)

  Scenario: Luồng chính
    When Hệ thống hiển thị "Recommended assets" nhóm theo Characters, Locations, Props; mỗi mục có tên, bí danh, mô tả ngoại hình, facts và các chương xuất hiện; mục trùng với tài sản đã có được gắn nhãn
    And Editor bỏ chọn mục không cần
    And Editor sửa tên hoặc loại của mục nếu cần
    And Editor gộp các mục trùng: tên của mục này trở thành bí danh của mục kia
    And Editor bấm "Thêm vào dự án"; hệ thống trả danh sách đã chốt cho UC-04.01 bước 5
    Then có danh sách tài sản cuối cùng do Editor chốt

  Scenario: 4a Mục trùng với tài sản đã có
    Given luồng chính đã tới bước 4
    When Mục trùng với tài sản đã có
    Then mặc định bỏ chọn; Editor có thể chọn "gộp vào tài sản hiện có" (thêm tên mới thành bí danh)

  Scenario: 5a Tên rỗng hoặc dài hơn 80 ký tự, hoặc bí danh vượt 10 mục
    Given luồng chính đã tới bước 5
    When Tên rỗng hoặc dài hơn 80 ký tự, hoặc bí danh vượt 10 mục
    Then báo lỗi tại mục đó, không cho xác nhận

  Scenario: 5b Tổng số tài sản sau khi thêm vượt 200
    Given luồng chính đã tới bước 5
    When Tổng số tài sản sau khi thêm vượt 200
    Then chặn và yêu cầu bỏ bớt

  Scenario: *a Editor đóng hộp thoại
    When Editor đóng hộp thoại
    Then không tạo gì; có thể mở lại danh sách đề xuất bằng cách phân tích lại
```

#### ST-04-02 Quản lý Story Assets

| Mục | Nội dung |
|---|---|
| Story | Là **Owner**, tôi muốn quản lý Story Assets |
| Mô tả | Xem và quản lý nhân vật, địa điểm, đạo cụ, nhóm của dự án |
| Use case | [UC-04.02](03-dac-ta-use-case/m04-the-gioi-truyen.md#uc-0402) · M04 — Thế giới truyện |
| Giai đoạn | P1 |
| Truy vết | FR-WLD-02, FR-WLD-05, FR-WLD-11 |
| Story point | |

```gherkin
Feature: UC-04.02 Quản lý Story Assets
  Background:
    Given Là thành viên dự án

  Scenario: Luồng chính
    When Editor mở Story Assets; hệ thống hiển thị 3 nhóm (Characters, Locations, Props) và các Group, mỗi tài sản có ảnh tham chiếu và trạng thái
    And Editor chọn một tài sản để xem chi tiết hoặc thực hiện một use case con; để AI đề xuất tài sản từ các chương, Editor bấm "Analyze" (UC-04.01)
    Then Story Assets phản ánh đúng thế giới truyện
```

#### ST-04-02a Tạo nhân vật / địa điểm / đạo cụ

| Mục | Nội dung |
|---|---|
| Story | Là **Owner**, tôi muốn tạo nhân vật / địa điểm / đạo cụ |
| Mô tả | Tạo mới một nhân vật, địa điểm hoặc đạo cụ thủ công |
| Use case | [UC-04.02a](03-dac-ta-use-case/m04-the-gioi-truyen.md#uc-0402a) · M04 — Thế giới truyện |
| Giai đoạn | P1 |
| Truy vết | FR-WLD-02, FR-WLD-03; BR-14; 08 §5; API 2.4 `POST /projects/{pid}/story-assets`; seq-the-gioi-truyen |
| Story point | |

```gherkin
Feature: UC-04.02a Tạo nhân vật / địa điểm / đạo cụ
  Background:
    Given Là thành viên dự án; dự án có dưới 200 Story Assets

  Scenario: Luồng chính
    When Editor chọn loại tài sản
    And Editor nhập tên (1–80 ký tự), bí danh (≤ 10), mô tả ngoại hình, facts bất biến
    And Editor chọn một trong ba cách có ảnh tham chiếu: sinh bằng AI (UC-04.03, include, tính phí); tải ảnh lên (UC-04.04, dùng nguyên bản); hoặc bỏ qua
    And Hệ thống lưu StoryAsset và hiển thị trong nhóm tương ứng
    Then có StoryAsset mới (kind = CHARACTER, LOCATION hoặc PROP, version = 1)

  Scenario: 2a Tên trùng với tên hoặc bí danh của tài sản khác
    Given luồng chính đã tới bước 2
    When Tên trùng với tên hoặc bí danh của tài sản khác
    Then cảnh báo vì sẽ gây khớp mơ hồ ở UC-05.06f; Editor có thể vẫn tạo

  Scenario: 3a Chọn sinh ảnh nhưng không đủ số dư
    Given luồng chính đã tới bước 3
    When Chọn sinh ảnh nhưng không đủ số dư
    Then 402; tài sản vẫn được tạo, chưa có ảnh

  Scenario: 3b Sinh ảnh lỗi
    Given luồng chính đã tới bước 3
    When Sinh ảnh lỗi
    Then hoàn tiền (UC-04.03 nhánh 4a); tài sản vẫn được tạo

  Scenario: 4a Đã có 200 tài sản
    Given luồng chính đã tới bước 4
    When Đã có 200 tài sản
    Then chặn tạo thêm
```

#### ST-04-02b Tạo nhóm nhân vật

| Mục | Nội dung |
|---|---|
| Story | Là **Owner**, tôi muốn tạo nhóm nhân vật |
| Mô tả | Gom nhiều nhân vật thành một nhóm (vd. gia đình, băng nhóm) để dùng như một thực thể trong shot |
| Use case | [UC-04.02b](03-dac-ta-use-case/m04-the-gioi-truyen.md#uc-0402b) · M04 — Thế giới truyện |
| Giai đoạn | P1 |
| Truy vết | FR-WLD-02; IC-13; 04 §3.3 `story_asset_group_members` |
| Story point | |

```gherkin
Feature: UC-04.02b Tạo nhóm nhân vật
  Background:
    Given Dự án có ít nhất 2 nhân vật (CHARACTER)

  Scenario: Luồng chính
    When Editor đặt tên nhóm (1–80 ký tự)
    And Editor chọn các nhân vật thành viên (tối thiểu 2)
    And Editor có thể chọn sinh ảnh nhóm (UC-04.03, tính phí)
    And Hệ thống lưu StoryAsset GROUP và các dòng story_asset_group_members
    Then có StoryAsset kind = GROUP với ≥ 2 thành viên

  Scenario: 2a Chọn dưới 2 thành viên, thành viên không phải CHARACTER, thành viên thuộc dự án 
    Given luồng chính đã tới bước 2
    When Chọn dưới 2 thành viên, thành viên không phải CHARACTER, thành viên thuộc dự án khác hoặc chọn chính nhóm
    Then từ chối (IC-13)

  Scenario: 3a Không đủ số dư hoặc sinh ảnh lỗi
    Given luồng chính đã tới bước 3
    When Không đủ số dư hoặc sinh ảnh lỗi
    Then nhóm vẫn được tạo, chưa có ảnh

  Scenario: *a Sau này thành viên bị gỡ khỏi dự án (UC-04.02d) và nhóm còn dưới 2 thành viên
    When Sau này thành viên bị gỡ khỏi dự án (UC-04.02d) và nhóm còn dưới 2 thành viên
    Then hệ thống cảnh báo Editor bổ sung hoặc xóa nhóm [ĐX]
```

#### ST-04-02d Gỡ khỏi dự án

| Mục | Nội dung |
|---|---|
| Story | Là **Owner**, tôi muốn gỡ khỏi dự án |
| Mô tả | Gỡ một tài sản khỏi dự án mà không làm hỏng các shot và ảnh đã sinh |
| Use case | [UC-04.02d](03-dac-ta-use-case/m04-the-gioi-truyen.md#uc-0402d) · M04 — Thế giới truyện |
| Giai đoạn | P1 |
| Truy vết | BR-16; 04 §3.3, §3.4 (`shot_asset_refs.story_asset_id` cho phép NULL); API 2.4 `DELETE /projects/{pid}/story-assets/{sid}` |
| Story point | |

```gherkin
Feature: UC-04.02d Gỡ khỏi dự án
  Background:
    Given Tài sản thuộc dự án

  Scenario: Luồng chính
    When Editor chọn "Remove from project"
    And Hệ thống hiển thị số shot đang tham chiếu tài sản, các nhóm chứa nó và các quan hệ liên quan; yêu cầu xác nhận
    And Editor xác nhận
    And Hệ thống xóa StoryAsset khỏi dự án trong một giao dịch: đặt shot_asset_refs.story_asset_id = NULL (giữ raw_name), gỡ khỏi các nhóm, xóa các quan hệ (relationships) có tài sản này [ĐX]
    And Hệ thống không động tới ảnh shot đã sinh và không xóa tài sản gốc ở thư viện cá nhân
    Then StoryAsset bị gỡ; các shot từng tham chiếu giữ raw_name và chuyển "chưa liên kết"; ảnh shot đã sinh không đổi

  Scenario: 3a Editor hủy
    Given luồng chính đã tới bước 3
    When Editor hủy
    Then không đổi gì

  Scenario: 4a 409
    Given luồng chính đã tới bước 4
    When 409
    Then tài sản vừa được người khác sửa; tải lại và xác nhận lại (UC-02.10)

  Scenario: *a Về sau thêm lại tài sản cùng tên
    When Về sau thêm lại tài sản cùng tên
    Then UC-05.06f có thể tự khớp lại các tham chiếu "chưa liên kết"
```

#### ST-04-02e Chỉnh sửa tài sản

| Mục | Nội dung |
|---|---|
| Story | Là **Owner**, tôi muốn chỉnh sửa tài sản |
| Mô tả | Sửa tại chỗ một nhân vật, địa điểm, đạo cụ hoặc nhóm: tên, bí danh (để khớp tên trong shot), mô tả ngoại hình, facts bất biến (đưa vào prompt sinh ảnh), thành viên nhóm, ảnh tham chiếu. Sửa không phải tạo lại: giữ nguyên định danh nên mọi tham chiếu shot, nhóm, quan hệ vẫn còn |
| Use case | [UC-04.02e](03-dac-ta-use-case/m04-the-gioi-truyen.md#uc-0402e) · M04 — Thế giới truyện |
| Giai đoạn | P1 |
| Truy vết | FR-WLD-02; BR-08, BR-14; IC-13; 08 §5 (tên 1–80 ký tự, bí danh ≤ 10); API 2.4 `PATCH /projects/{pid}/story-assets/{sid}` (If-Match) |
| Story point | |

```gherkin
Feature: UC-04.02e Chỉnh sửa tài sản
  Background:
    Given Tài sản thuộc dự án

  Scenario: Luồng chính
    When Editor mở chi tiết tài sản và bấm "Edit"; hệ thống hiển thị biểu mẫu với giá trị hiện tại và version
    And Editor sửa một hoặc nhiều trường: tên, bí danh (thêm/xóa, tối đa 10), mô tả ngoại hình, facts bất biến (mỗi fact là một đặc điểm cố định, vd. "tóc đen ngang vai"). Với nhóm (GROUP): thêm hoặc bớt nhân vật thành viên
    And Editor lưu; hệ thống gửi PATCH kèm If-Match, cập nhật các trường đã đổi và tăng version
    And Lần sinh ảnh sau dùng mô tả và facts mới trong prompt (UC-04.03, UC-05.09); storyboard và UC-05.06f khớp tên theo tên và bí danh mới
    Then StoryAsset được cập nhật, giữ nguyên id, version tăng 1; shot_asset_refs, nhóm và relationships trỏ tới tài sản không đổi

  Scenario: 2a Tên hoặc bí danh trùng tên hoặc bí danh của tài sản khác trong dự án
    Given luồng chính đã tới bước 2
    When Tên hoặc bí danh trùng tên hoặc bí danh của tài sản khác trong dự án
    Then cảnh báo khớp mơ hồ (UC-05.06f); Editor có thể vẫn lưu

  Scenario: 2b Tên rỗng hoặc dài hơn 80 ký tự, hoặc vượt 10 bí danh
    Given luồng chính đã tới bước 2
    When Tên rỗng hoặc dài hơn 80 ký tự, hoặc vượt 10 bí danh
    Then báo lỗi, không lưu

  Scenario: 2c Nhóm còn dưới 2 thành viên, thành viên không phải CHARACTER, thuộc dự án khác ho
    Given luồng chính đã tới bước 2
    When Nhóm còn dưới 2 thành viên, thành viên không phải CHARACTER, thuộc dự án khác hoặc chính nhóm
    Then từ chối (IC-13)

  Scenario: 2d Editor muốn thay ảnh tham chiếu bằng ảnh tải lên
    Given luồng chính đã tới bước 2
    When Editor muốn thay ảnh tham chiếu bằng ảnh tải lên
    Then thực hiện UC-04.04 (extend); ảnh cũ vẫn xem được trong lịch sử asset_images

  Scenario: 2e Editor tắt "use exact" của tài sản đang dùng ảnh nguyên bản
    Given luồng chính đã tới bước 2
    When Editor tắt "use exact" của tài sản đang dùng ảnh nguyên bản
    Then nút "Generate" hiện lại; ảnh hiện hành giữ nguyên cho tới khi Editor chủ động sinh (UC-04.03) [ĐX]

  Scenario: 2f Đổi loại tài sản (kind) không được hỗ trợ
    Given luồng chính đã tới bước 2
    When Đổi loại tài sản (kind) không được hỗ trợ
    Then Editor gỡ (UC-04.02d) rồi tạo mới (UC-04.02a) [ĐX]

  Scenario: 3a 409
    Given luồng chính đã tới bước 3
    When 409
    Then tài sản vừa được người khác sửa; xử lý theo UC-02.10

  Scenario: 4a Sau khi sửa mô tả, facts hoặc thành viên nhóm, hệ thống gợi ý "Regenerate" kèm g
    Given luồng chính đã tới bước 4
    When Sau khi sửa mô tả, facts hoặc thành viên nhóm, hệ thống gợi ý "Regenerate" kèm giá thay vì tự sinh lại (UC-04.03); tài sản "use exact" không có gợi ý này (BR-14)
    Then hệ thống xử lý như mô tả

  Scenario: *a Tài sản thêm từ thư viện cá nhân
    When Tài sản thêm từ thư viện cá nhân
    Then sửa chỉ đổi bản trong dự án, không đổi bản ở thư viện (FR-LIB-05)
```

#### ST-04-03 Sinh ảnh tham chiếu

| Mục | Nội dung |
|---|---|
| Story | Là **Owner**, tôi muốn sinh ảnh tham chiếu |
| Mô tả | Sinh ảnh chuẩn cho tài sản theo style + Art Direction để giữ nhất quán |
| Use case | [UC-04.03](03-dac-ta-use-case/m04-the-gioi-truyen.md#uc-0403) · M04 — Thế giới truyện |
| Giai đoạn | P1 |
| Truy vết | FR-WLD-03; BR-01, BR-02, BR-08, BR-14; seq-the-gioi-truyen |
| Story point | |

```gherkin
Feature: UC-04.03 Sinh ảnh tham chiếu
  Background:
    Given Dự án có style; tài sản có mô tả; đủ số dư

  Scenario: Luồng chính
    When Editor bấm "Generate" (hiện giá ước tính)
    And Hệ thống giữ tiền, tạo job GENERATE_ASSET_IMAGE
    And Worker ghép prompt: style + Art Direction + Visual Rules + mô tả + facts; địa điểm sinh reference sheet nhiều góc nhìn
    And Image Provider trả ảnh; moderation đầu ra; lưu ảnh; trừ tiền
    And Giao diện hiển thị ảnh mới; phiên bản cũ vẫn xem được
    Then asset_images mới, đặt làm ảnh hiện hành; tiền bị trừ

  Scenario: 1a Tài sản dùng ảnh nguyên bản (BR-14)
    When Tài sản dùng ảnh nguyên bản (BR-14)
    Then nút bị ẩn

  Scenario: 4a Lỗi hoặc vi phạm chính sách
    Given luồng chính đã tới bước 4
    When Lỗi hoặc vi phạm chính sách
    Then hoàn tiền, gợi ý sửa mô tả
```

#### ST-04-03a Sinh lại tất cả (Regenerate all)

| Mục | Nội dung |
|---|---|
| Story | Là **Owner**, tôi muốn sinh lại tất cả (Regenerate all) |
| Mô tả | Sinh lại ảnh tham chiếu của mọi tài sản sau khi đổi style hoặc Art Direction, bỏ qua tài sản dùng ảnh nguyên bản |
| Use case | [UC-04.03a](03-dac-ta-use-case/m04-the-gioi-truyen.md#uc-0403a) · M04 — Thế giới truyện |
| Giai đoạn | P1 |
| Truy vết | BR-01, BR-02, BR-14, BR-15; WR-05; API 2.4 `POST /projects/{pid}/story-assets:regenerate-all`; seq-the-gioi-truyen |
| Story point | |

```gherkin
Feature: UC-04.03a Sinh lại tất cả (Regenerate all)
  Background:
    Given Dự án có style; có ít nhất một tài sản không dùng "use exact"; đủ số dư cho toàn bộ

  Scenario: Luồng chính
    When Editor bấm "Regenerate all"
    And Hệ thống đếm các tài sản đủ điều kiện (bỏ tài sản có use_exact_image = true) và hiển thị tổng giá (theo đơn giá ảnh tham chiếu)
    And Editor xác nhận
    And Trong một giao dịch, hệ thống tạo mỗi tài sản một job GENERATE_ASSET_IMAGE và giữ tiền riêng cho từng job (WR-05); thiếu tiền cho bất kỳ job nào thì không tạo job nào
    And Mỗi job chạy như UC-04.03 bước 3–4 và CAPTURE hoặc RELEASE tiền của chính nó
    And Tiến độ gửi qua SSE (job.updated, asset.updated); khi xong, mọi tài sản đủ điều kiện có ảnh theo style mới. Ảnh cũ được giữ như phiên bản trước
    Then mọi tài sản đủ điều kiện có asset_images mới theo style mới

  Scenario: 2a Không có tài sản nào đủ điều kiện
    Given luồng chính đã tới bước 2
    When Không có tài sản nào đủ điều kiện
    Then báo "Không có tài sản cần sinh lại", không tạo job

  Scenario: 4a Không đủ số dư
    Given luồng chính đã tới bước 4
    When Không đủ số dư
    Then 402 kèm số còn thiếu; gợi ý nạp tiền (UC-09.03) hoặc sinh lại từng tài sản

  Scenario: 5a Một số job lỗi sau retry
    Given luồng chính đã tới bước 5
    When Một số job lỗi sau retry
    Then RELEASE tiền của chúng, liệt kê tài sản lỗi và cho phép thử lại riêng từng cái

  Scenario: *a Đổi style sau khi đã có ảnh không tự sinh lại; hệ thống chỉ gợi ý hành động này 
    When Đổi style sau khi đã có ảnh không tự sinh lại; hệ thống chỉ gợi ý hành động này kèm giá
    Then hệ thống xử lý như mô tả
```

#### ST-04-04 Dùng ảnh tải lên nguyên bản

| Mục | Nội dung |
|---|---|
| Story | Là **Owner**, tôi muốn dùng ảnh tải lên nguyên bản |
| Mô tả | Dùng ảnh người dùng tải lên làm ảnh tham chiếu, không cho AI vẽ lại |
| Use case | [UC-04.04](03-dac-ta-use-case/m04-the-gioi-truyen.md#uc-0404) · M04 — Thế giới truyện |
| Giai đoạn | P1 |
| Truy vết | FR-WLD-04; BR-14; NFR-SEC-10; seq-the-gioi-truyen |
| Story point | |

```gherkin
Feature: UC-04.04 Dùng ảnh tải lên nguyên bản
  Background:
    Given Ảnh PNG/JPEG/WebP ≤ 10 MB, cạnh ngắn ≥ 512 px

  Scenario: Luồng chính
    When Editor tải ảnh lên
    And Hệ thống kiểm tra MIME, kích thước, quét malware, bỏ EXIF, moderation
    And Hệ thống lưu ảnh làm tham chiếu, gắn cờ "use exact"
    Then tài sản có use_exact_image = true

  Scenario: 2a Ảnh không đạt
    Given luồng chính đã tới bước 2
    When Ảnh không đạt
    Then báo lý do cụ thể
```

#### ST-04-05 Chọn style dự án

| Mục | Nội dung |
|---|---|
| Story | Là **Owner (Owner khi đổi; xem thêm UC-02.04)**, tôi muốn chọn style dự án |
| Mô tả | Chọn phong cách nghệ thuật từ danh mục |
| Use case | [UC-04.05](03-dac-ta-use-case/m04-the-gioi-truyen.md#uc-0405) · M04 — Thế giới truyện |
| Giai đoạn | P1 |
| Truy vết | FR-WLD-06 |
| Story point | |

```gherkin
Feature: UC-04.05 Chọn style dự án
  Background:
    Given Là Owner (đổi) hoặc dự án chưa có style (lần đầu, Editor được chọn)

  Scenario: Luồng chính
    When Hệ thống mở Styles Library (ảnh mẫu, tên, mô tả)
    And Người dùng chọn style; hệ thống lưu
    And Nếu đã có ảnh tham chiếu, hệ thống đề xuất UC-04.03a
    Then projects.style_id cập nhật
```

#### ST-04-06 Thiết lập Art Direction

| Mục | Nội dung |
|---|---|
| Story | Là **Owner**, tôi muốn thiết lập Art Direction |
| Mô tả | Viết chỉ dẫn phong cách bổ sung lên style của dự án |
| Use case | [UC-04.06](03-dac-ta-use-case/m04-the-gioi-truyen.md#uc-0406) · M04 — Thế giới truyện |
| Giai đoạn | P1 |
| Truy vết | FR-WLD-07; BR-08 |
| Story point | |

```gherkin
Feature: UC-04.06 Thiết lập Art Direction
  Background:
    Given Là thành viên dự án

  Scenario: Luồng chính
    When Editor nhập chỉ dẫn (vd. "tông ấm, bão hòa thấp, nét vẽ mềm")
    And Hệ thống lưu (If-Match) và gợi ý sinh lại ảnh nếu cần
    Then projects.art_direction cập nhật; áp cho mọi lần sinh ảnh sau
```

#### ST-04-10 Quản lý Visual Rules

| Mục | Nội dung |
|---|---|
| Story | Là **Owner**, tôi muốn quản lý Visual Rules |
| Mô tả | Tạo, sửa, bật/tắt, xóa luật hình ảnh áp toàn dự án hoặc theo chương |
| Use case | [UC-04.10](03-dac-ta-use-case/m04-the-gioi-truyen.md#uc-0410) · M04 — Thế giới truyện |
| Giai đoạn | P1 |
| Truy vết | FR-WLD-10; BR-08 |
| Story point | |

```gherkin
Feature: UC-04.10 Quản lý Visual Rules
  Background:
    Given Là thành viên dự án

  Scenario: Luồng chính
    When Editor bấm "New rule", nhập tên, nội dung, phạm vi
    And Hệ thống lưu; danh sách luật hiển thị theo phạm vi
    And Editor có thể sửa, tắt tạm hoặc xóa (xác nhận)
    Then luật được áp vào prompt các lần sinh ảnh sau theo thứ tự BR-08

  Scenario: 1a Nội dung > 1.000 ký tự hoặc tên > 80 ký tự
    When Nội dung > 1.000 ký tự hoặc tên > 80 ký tự
    Then báo lỗi kiểm tra
```

#### ST-05-01 Tạo bản nháp storyboard

| Mục | Nội dung |
|---|---|
| Story | Là **Owner (hoặc hệ thống qua UC-05.07a)**, tôi muốn tạo bản nháp storyboard |
| Mô tả | Chia toàn bộ văn bản chương thành các shot liên tục; mỗi shot = 1 ảnh + 1 đoạn văn nguồn |
| Use case | [UC-05.01](03-dac-ta-use-case/m05-sinh-tu-lieu.md#uc-0501) · M05 — Sinh tư liệu: storyboard, ảnh, thuyết minh nguyên văn |
| Giai đoạn | P1 |
| Truy vết | FR-BOK-01, 01a, 05; BR-20; ADR-11; seq-storyboard-sinh-anh |
| Story point | |

```gherkin
Feature: UC-05.01 Tạo bản nháp storyboard
  Background:
    Given Chương có văn bản, không bị khóa

  Scenario: Luồng chính
    When Hệ thống dựng ngữ cảnh: văn bản chương, Story Assets (tên, bí danh, facts), timeline truyện, Visual Rules, Chapter rules, thời lượng mục tiêu mỗi ảnh
    And Hệ thống tách câu tất định và đánh số câu
    And Job STORYBOARD_DRAFT (tính phí theo BR-01; khi chạy trong UC-05.07 thì nằm trong giá ước tính tổng): LLM nhận danh sách câu, trả Shot[] gồm startSentence, endSentence, title, focus, cast, items, location, thời điểm, ngày, brief (Subject/Environment/Composition/Camera/Lighting/Mood/Details), caption. LLM không chép lại văn bản
    And Hệ thống thực hiện UC-05.01a
    And Hệ thống ánh xạ tên sang tài sản (tên + bí danh); tên không khớp đánh dấu "chưa liên kết"
    And Hệ thống lưu bản nháp, các shot (source_start, source_end, source_hash) và hiển thị đoạn nguồn nguyên văn bên cạnh mỗi shot
    Then StoryboardDraft có N shot, concat(đoạn nguồn) == chapter.content; nếu là bản đầu tiên thì đặt làm hiện hành

  Scenario: 3a LLM trả sai schema
    Given luồng chính đã tới bước 3
    When LLM trả sai schema
    Then thử lại kèm thông báo lỗi, tối đa 2 lần; vẫn lỗi thì job FAILED

  Scenario: 4a Phải sửa > 20% ranh giới
    Given luồng chính đã tới bước 4
    When Phải sửa > 20% ranh giới
    Then lưu kèm Director note cảnh báo chất lượng, gợi ý tạo lại

  Scenario: 5a Có tên chưa liên kết
    Given luồng chính đã tới bước 5
    When Có tên chưa liên kết
    Then hiện "Some names here aren't linked to an asset yet" kèm nút thêm tài sản (UC-04.02a) hoặc tự khớp (UC-05.06f)
```

#### ST-05-01a Tách câu & kiểm tra phủ kín

| Mục | Nội dung |
|---|---|
| Story | Là **Hệ thống (CoverageValidator)**, tôi muốn tách câu & kiểm tra phủ kín |
| Mô tả | Đổi chỉ số câu do LLM hoặc Editor đưa ra thành ranh giới ký tự và bảo đảm các shot phủ kín 100% văn bản chương (IC-08, BR-20) |
| Use case | [UC-05.01a](03-dac-ta-use-case/m05-sinh-tu-lieu.md#uc-0501a) · M05 — Sinh tư liệu: storyboard, ảnh, thuyết minh nguyên văn |
| Giai đoạn | P1 |
| Truy vết | BR-20; IC-08; NFR-INT-01; ADR-11; 12 §1 (`SentenceSegmenter`, SEG-R1..R7); API 2.5 `…/storyboards/{did}/coverage`; `so-do/05-hoat-dong/act-phu-kin-van-ban.puml`; seq-storyboard-sinh-anh |
| Story point | |

```gherkin
Feature: UC-05.01a Tách câu & kiểm tra phủ kín
  Background:
    Given Chương có văn bản; có danh sách shot với chỉ số câu (từ LLM ở UC-05.01 bước 3, hoặc từ thao tác của Editor ở UC-05.03, UC-05.06c, UC-03.02a)

  Scenario: Luồng chính
    When Hệ thống lấy bảng câu của chương bằng SentenceSegmenter (tách tất định theo 12 §1, mỗi câu có offset [start, end)); ghi segmenter_version vào bản nháp
    And Hệ thống đổi startSentence, endSentence của từng shot thành source_start, source_end
    And Hệ thống sắp shot theo thứ tự, kẹp chỉ số vào phạm vi hợp lệ và bỏ shot rỗng
    And Khoảng hở giữa hai shot được gộp vào shot trước (khoảng hở ở đầu chương gộp vào shot đầu); phần chồng lấn được cắt theo shot sau
    And Hệ thống dời mọi ranh giới về đầu câu; khoảng trắng giữa các câu gán cho shot trước
    And Hệ thống kiểm tra IC-08: shot[0].source_start = 0, shot[i].source_end = shot[i+1].source_start, shot[cuối].source_end bằng độ dài chương, và concat(đoạn nguồn) == chapter.content (so sánh byte)
    And Hệ thống tính source_hash (sha256) từng đoạn nguồn và ghi boundary_fixes (số ranh giới đã sửa ở bước 3–5)
    Then các shot phủ kín chương, không chồng lấn, không sót; mỗi shot có source_start, source_end, source_hash

  Scenario: 6a Bất biến vẫn sai sau khi sửa (lỗi lập trình)
    Given luồng chính đã tới bước 6
    When Bất biến vẫn sai sau khi sửa (lỗi lập trình)
    Then từ chối lưu, không ghi gì, phát cảnh báo P1

  Scenario: 7a boundary_fixes vượt 20% số ranh giới
    Given luồng chính đã tới bước 7
    When boundary_fixes vượt 20% số ranh giới
    Then lưu bản nháp kèm Director note cảnh báo chất lượng và gợi ý tạo lại (UC-05.01 nhánh 4a)

  Scenario: *a Nội dung chương đổi trong lúc xử lý (phiên bản khác)
    When Nội dung chương đổi trong lúc xử lý (phiên bản khác)
    Then hủy kết quả và chạy lại từ bước 1

  Scenario: 3a Bỏ shot rỗng làm số shot giảm
    Given luồng chính đã tới bước 3
    When Bỏ shot rỗng làm số shot giảm
    Then chấp nhận; số shot cuối cùng nằm trong 1–40 (08 §5)
```

#### ST-05-02c Đặt bản nháp hiện hành

| Mục | Nội dung |
|---|---|
| Story | Là **Owner**, tôi muốn đặt bản nháp hiện hành |
| Mô tả | Chọn bản nháp làm storyboard hiện hành của chương; tư liệu và timeline được cập nhật theo |
| Use case | [UC-05.02c](03-dac-ta-use-case/m05-sinh-tu-lieu.md#uc-0502c) · M05 — Sinh tư liệu: storyboard, ảnh, thuyết minh nguyên văn |
| Giai đoạn | P1 |
| Truy vết | BR-07, BR-12; IC-03; UC-06.15; API 2.5 `POST …/storyboards/{did}:set-current`; seq-storyboard-sinh-anh |
| Story point | |

```gherkin
Feature: UC-05.02c Đặt bản nháp hiện hành
  Background:
    Given Bản nháp thuộc chương và chưa phải bản hiện hành; chương không bị khóa (BR-12)

  Scenario: Luồng chính
    When Editor chọn một bản nháp và bấm "Set as current"
    And Nếu chương đã có timeline được chỉnh sửa, hệ thống cảnh báo các clip sẽ được đồng bộ theo bản mới và hỏi xác nhận
    And Hệ thống cập nhật chapters.current_storyboard_id trong một giao dịch; bản cũ thôi là hiện hành
    And Các shot của bản mới chưa có ảnh hoặc thuyết minh được đánh dấu cần sinh; hệ thống gợi ý UC-05.07c kèm giá. Trạng thái media của chương được tính lại theo bản mới
    And Hệ thống thực hiện UC-06.15 để đồng bộ timeline và phát shot.updated, timeline.updated
    Then chapters.current_storyboard_id trỏ bản mới (đúng một bản hiện hành, BR-07, IC-03)

  Scenario: 2a Editor không xác nhận
    Given luồng chính đã tới bước 2
    When Editor không xác nhận
    Then không đổi gì

  Scenario: 3a Chương đang bị job khóa
    Given luồng chính đã tới bước 3
    When Chương đang bị job khóa
    Then 423 RESOURCE_LOCKED

  Scenario: 3b Có xung đột phiên bản
    Given luồng chính đã tới bước 3
    When Có xung đột phiên bản
    Then 409, xử lý theo UC-02.10
```

#### ST-05-03 Chia lại shot (nhiều / ít hơn)

| Mục | Nội dung |
|---|---|
| Story | Là **Owner**, tôi muốn chia lại shot (nhiều / ít hơn) |
| Mô tả | Tạo bản nháp mới với nhiều shot hơn (mỗi nhịp truyện một ảnh) hoặc ít hơn |
| Use case | [UC-05.03](03-dac-ta-use-case/m05-sinh-tu-lieu.md#uc-0503) · M05 — Sinh tư liệu: storyboard, ảnh, thuyết minh nguyên văn |
| Giai đoạn | P1 |
| Truy vết | FR-BOK-03; seq-storyboard-sinh-anh |
| Story point | |

```gherkin
Feature: UC-05.03 Chia lại shot (nhiều / ít hơn)
  Background:
    Given Chương có văn bản

  Scenario: Luồng chính
    When Editor chọn "Nhiều hơn" hoặc "Ít hơn"
    And Hệ thống hiện giá ước tính; Editor xác nhận; hệ thống chạy UC-05.01 bước 1–6 với tham số tương ứng, tạo bản nháp mới (chưa hiện hành)
    And Hệ thống hiện bản mới cạnh bản hiện hành; Editor chọn "Dùng bản này" (đặt hiện hành, UC-05.02c) hoặc "Giữ bản cũ". Bản không dùng vẫn được lưu. So sánh chi tiết (UC-05.02b) và quản lý nhiều bản nháp: sau MVP
    Then bản nháp mới (RESPLIT_MORE/RESPLIT_FEWER), bản cũ giữ nguyên
```

#### ST-05-06 Biên tập shot

| Mục | Nội dung |
|---|---|
| Story | Là **Owner**, tôi muốn biên tập shot |
| Mô tả | Chỉnh nội dung minh họa và cấu trúc của từng shot |
| Use case | [UC-05.06](03-dac-ta-use-case/m05-sinh-tu-lieu.md#uc-0506) · M05 — Sinh tư liệu: storyboard, ảnh, thuyết minh nguyên văn |
| Giai đoạn | P1 |
| Truy vết | FR-BOK-01b, 05, 06 |
| Story point | |

```gherkin
Feature: UC-05.06 Biên tập shot
  Background:
    Given Bản nháp tồn tại

  Scenario: Luồng chính
    When Editor chọn shot; hệ thống hiển thị các trường minh họa và đoạn nguồn (chỉ đọc). Dời ranh giới giữa hai shot làm ở Workspace (UC-03.02a), không có nút ◀ ▶ ở đây
    And Editor thực hiện một use case con; hệ thống lưu
    Then shot cập nhật (If-Match); phủ kín vẫn 100%

  Scenario: 2a 409
    Given luồng chính đã tới bước 2
    When 409
    Then UC-02.10
```

#### ST-05-06a Sửa brief, thời điểm, caption

| Mục | Nội dung |
|---|---|
| Story | Là **Owner**, tôi muốn sửa brief, thời điểm, caption |
| Mô tả | Sửa các trường minh họa của shot; đoạn nguồn (văn bản truyện) chỉ đọc |
| Use case | [UC-05.06a](03-dac-ta-use-case/m05-sinh-tu-lieu.md#uc-0506a) · M05 — Sinh tư liệu: storyboard, ảnh, thuyết minh nguyên văn |
| Giai đoạn | P1 |
| Truy vết | FR-BOK-05, FR-BOK-06; BR-21; 08 §5; API 2.5 `PATCH …/shots/{shid}` (If-Match); seq-storyboard-sinh-anh |
| Story point | |

```gherkin
Feature: UC-05.06a Sửa brief, thời điểm, caption
  Background:
    Given Shot thuộc bản nháp; Editor đã chọn shot

  Scenario: Luồng chính
    When Editor sửa một hoặc nhiều trường: tiêu đề, focus, 7 trường của brief (Subject, Environment, Composition, Camera, Lighting, Mood, Details), thời điểm trong ngày, ngày trong truyện, caption (≤ 300 ký tự)
    And Hệ thống gửi PATCH kèm If-Match, kiểm tra schema và giới hạn độ dài
    And Hệ thống ghi shot, tăng version, phát shot.updated
    And Nếu brief đổi, ảnh hiện tại được đánh dấu "brief đã đổi" (illustrations.shot_version < shots.version) và hệ thống gợi ý sinh lại ảnh (UC-05.09) kèm giá
    Then shot được lưu với version mới

  Scenario: 2a Caption dài hơn 300 ký tự hoặc sai schema
    Given luồng chính đã tới bước 2
    When Caption dài hơn 300 ký tự hoặc sai schema
    Then 400 VALIDATION_ERROR

  Scenario: 3a 409 VERSION_CONFLICT
    Given luồng chính đã tới bước 3
    When 409 VERSION_CONFLICT
    Then xử lý theo UC-02.10

  Scenario: *a Editor cố sửa đoạn nguồn
    When Editor cố sửa đoạn nguồn
    Then trường chỉ đọc, hướng dẫn sửa văn bản chương trong Workspace (UC-03.02)
```

#### ST-05-06b Gắn cast / item / location

| Mục | Nội dung |
|---|---|
| Story | Là **Owner**, tôi muốn gắn cast / item / location |
| Mô tả | Chọn nhân vật, đạo cụ và địa điểm xuất hiện trong shot để ảnh tham chiếu tương ứng được đưa vào prompt |
| Use case | [UC-05.06b](03-dac-ta-use-case/m05-sinh-tu-lieu.md#uc-0506b) · M05 — Sinh tư liệu: storyboard, ảnh, thuyết minh nguyên văn |
| Giai đoạn | P1 |
| Truy vết | FR-BOK-05, FR-BOK-08; BR-16; 04 §3.4 `shot_asset_refs`; seq-storyboard-sinh-anh |
| Story point | |

```gherkin
Feature: UC-05.06b Gắn cast / item / location
  Background:
    Given Shot thuộc bản nháp

  Scenario: Luồng chính
    When Editor thêm tài sản vào Cast, Items hoặc Location bằng cách chọn từ danh sách Story Assets, hoặc gỡ tài sản đã gắn
    And Hệ thống kiểm tra mỗi shot có tối đa 1 location
    And Hệ thống lưu shot_asset_refs và tăng version của shot
    And Ở lần sinh ảnh sau, UC-05.09 bước 2 đính kèm ảnh tham chiếu của các tài sản đã gắn
    Then shot_asset_refs của shot được cập nhật (vai trò CAST, ITEM, LOCATION)

  Scenario: 1a Editor nhập tên chưa có tài sản
    When Editor nhập tên chưa có tài sản
    Then lưu với raw_name, story_asset_id = NULL, hiện cảnh báo "chưa liên kết" kèm nút thêm tài sản (UC-04.02a) hoặc tự khớp (UC-05.06f)

  Scenario: 2a Thêm location thứ hai
    Given luồng chính đã tới bước 2
    When Thêm location thứ hai
    Then chặn, đề nghị thay location hiện có

  Scenario: 4a Tài sản chưa có ảnh tham chiếu
    Given luồng chính đã tới bước 4
    When Tài sản chưa có ảnh tham chiếu
    Then cảnh báo ảnh sinh ra có thể thiếu nhất quán, gợi ý UC-04.03

  Scenario: 3a 409
    Given luồng chính đã tới bước 3
    When 409
    Then xử lý theo UC-02.10
```

#### ST-05-06c Tách / gộp / xóa shot

| Mục | Nội dung |
|---|---|
| Story | Là **Owner**, tôi muốn tách / gộp / xóa shot |
| Mô tả | Thay đổi cấu trúc storyboard bằng cách tách, gộp hoặc xóa shot mà văn bản chương luôn được phủ kín |
| Use case | [UC-05.06c](03-dac-ta-use-case/m05-sinh-tu-lieu.md#uc-0506c) · M05 — Sinh tư liệu: storyboard, ảnh, thuyết minh nguyên văn |
| Giai đoạn | P1 |
| Truy vết | BR-06, BR-12, BR-20; IC-08, IC-09; 08 §5 (1–40 shot); API 2.5 `:split`, `:merge-up`, `:merge-down`, `DELETE …/shots/{shid}`; seq-storyboard-sinh-anh |
| Story point | |

```gherkin
Feature: UC-05.06c Tách / gộp / xóa shot
  Background:
    Given Bản nháp tồn tại; chương không bị khóa (BR-12)

  Scenario: Luồng chính
    When Editor chọn thao tác trên một shot
    And *Tách:* Editor chọn một ranh giới giữa hai câu trong đoạn nguồn (atSentence); shot thành hai shot liền nhau
    And *Gộp:* Editor chọn gộp với shot ngay trên hoặc ngay dưới; hai đoạn nguồn được nối lại theo thứ tự
    And *Xóa:* hệ thống không xóa văn bản; đoạn nguồn của shot bị xóa được gộp vào shot liền trước (hoặc liền sau nếu là shot đầu tiên)
    And Hệ thống thực hiện UC-05.01a để kiểm tra phủ kín và tính lại source_hash
    And Các thuyết minh của shot có đoạn nguồn đổi chuyển OUTDATED (IC-09); shot mới tạo ra chưa có ảnh và thuyết minh. Ảnh của các shot hiện có được giữ nguyên
    And Hệ thống phát shot.updated, đồng bộ timeline (UC-06.15) và gợi ý UC-05.07c để sinh phần thiếu
    Then các shot vẫn phủ kín 100% chương (IC-08); thuyết minh của shot bị đổi đoạn nguồn chuyển OUTDATED

  Scenario: 2a Shot chỉ có một câu
    Given luồng chính đã tới bước 2
    When Shot chỉ có một câu
    Then không tách được (mỗi shot ≥ 1 câu)

  Scenario: 2b Tách làm bản nháp vượt 40 shot
    Given luồng chính đã tới bước 2
    When Tách làm bản nháp vượt 40 shot
    Then chặn

  Scenario: 4a Bản nháp chỉ còn một shot
    Given luồng chính đã tới bước 4
    When Bản nháp chỉ còn một shot
    Then không xóa được (phải phủ kín chương)

  Scenario: 6a Chương đang bị khóa
    Given luồng chính đã tới bước 6
    When Chương đang bị khóa
    Then 423 RESOURCE_LOCKED

  Scenario: 6b 409
    Given luồng chính đã tới bước 6
    When 409
    Then xử lý theo UC-02.10
```

#### ST-05-06e Viết lại brief một shot bằng AI

| Mục | Nội dung |
|---|---|
| Story | Là **Owner**, tôi muốn viết lại brief một shot bằng AI |
| Mô tả | Nhờ AI viết lại brief minh họa của một shot theo ghi chú; đoạn nguồn không bao giờ bị đụng tới |
| Use case | [UC-05.06e](03-dac-ta-use-case/m05-sinh-tu-lieu.md#uc-0506e) · M05 — Sinh tư liệu: storyboard, ảnh, thuyết minh nguyên văn |
| Giai đoạn | P1 |
| Truy vết | FR-BOK-06; BR-21; NFR-INT-02; 08 §3.2 (`REWRITE_SHOT`); API 2.5 `POST …/shots/{shid}:rewrite`; seq-storyboard-sinh-anh |
| Story point | |

```gherkin
Feature: UC-05.06e Viết lại brief một shot bằng AI
  Background:
    Given Shot thuộc bản nháp; đủ số dư cho giá ước tính; chưa vượt giới hạn kỹ thuật (BR-32)

  Scenario: Luồng chính
    When Editor nhập ghi chú (ví dụ "trời tối hơn") và bấm gửi
    And Hệ thống hiện giá ước tính; Editor xác nhận; hệ thống giữ tiền (UC-05.17) và tạo job REWRITE_SHOT. Khi được gọi từ UC-03.02a, bước xác nhận đã làm ở đó
    And Worker gửi LLM brief hiện tại, ghi chú, tài sản của shot, style, Art Direction và Visual Rules; đoạn nguồn chỉ được đưa vào làm ngữ cảnh đọc
    And LLM trả brief mới theo schema 7 trường; hệ thống chỉ ghi vào trường brief (không có đường ghi vào đoạn nguồn)
    And Shot được cập nhật, version tăng; ảnh hiện tại được đánh dấu "brief đã đổi" và hệ thống gợi ý sinh lại ảnh (UC-05.09) kèm giá
    Then brief của shot được thay bằng bản mới

  Scenario: 2a Vượt giới hạn kỹ thuật (≤ 30 yêu cầu LLM/phút)
    Given luồng chính đã tới bước 2
    When Vượt giới hạn kỹ thuật (≤ 30 yêu cầu LLM/phút)
    Then 429 kèm Retry-After

  Scenario: 2b Không đủ số dư
    Given luồng chính đã tới bước 2
    When Không đủ số dư
    Then 402; chạm trần chi tiêu ngày: 503 DAILY_BUDGET_EXCEEDED

  Scenario: 4a LLM trả sai schema
    Given luồng chính đã tới bước 4
    When LLM trả sai schema
    Then thử lại tối đa 2 lần; vẫn lỗi thì job FAILED, brief cũ giữ nguyên, tiền giữ được hoàn

  Scenario: 4b Nội dung bị moderation chặn
    Given luồng chính đã tới bước 4
    When Nội dung bị moderation chặn
    Then job FAILED với CONTENT_POLICY (451); không tự sửa để vượt bộ lọc (BR-18)

  Scenario: 5a 409
    Given luồng chính đã tới bước 5
    When 409
    Then shot đã đổi trong lúc job chạy; kết quả không ghi đè, Editor chọn áp dụng hoặc bỏ (UC-02.10)
```

#### ST-05-06f Tự khớp tên với tài sản

| Mục | Nội dung |
|---|---|
| Story | Là **Owner**, tôi muốn tự khớp tên với tài sản |
| Mô tả | Tự gắn các tên chưa liên kết ở shot với đúng Story Asset |
| Use case | [UC-05.06f](03-dac-ta-use-case/m05-sinh-tu-lieu.md#uc-0506f) · M05 — Sinh tư liệu: storyboard, ảnh, thuyết minh nguyên văn |
| Giai đoạn | P1 |
| Truy vết | FR-BOK-08; BR-16; API 2.5 `POST …/storyboards/{did}:auto-link-assets`; seq-storyboard-sinh-anh |
| Story point | |

```gherkin
Feature: UC-05.06f Tự khớp tên với tài sản
  Background:
    Given Bản nháp có tham chiếu "chưa liên kết"; dự án có Story Assets

  Scenario: Luồng chính
    When Editor bấm "Scan the chapter text and auto-match"
    And Hệ thống lấy mọi shot_asset_refs của bản nháp có story_asset_id = NULL
    And Hệ thống so raw_name với tên và bí danh của Story Assets (không phân biệt hoa thường, dấu cách chuẩn hóa)
    And Khớp đúng một tài sản: gán story_asset_id. Khớp từ hai tài sản trở lên: bỏ qua và liệt kê. Không khớp: giữ "chưa liên kết"
    And Hệ thống báo "Đã liên kết N, còn M chưa liên kết" kèm danh sách phần còn lại
    Then các tham chiếu khớp duy nhất được liên kết

  Scenario: 2a Dự án chưa có tài sản nào
    Given luồng chính đã tới bước 2
    When Dự án chưa có tài sản nào
    Then gợi ý phân tích tài sản (UC-04.01) hoặc tạo tài sản (UC-04.02a)

  Scenario: 4a Không có tên nào cần khớp
    Given luồng chính đã tới bước 4
    When Không có tên nào cần khớp
    Then báo "Không còn tên chưa liên kết"
```

#### ST-05-08 Xem Tư liệu dự án (media bin)

| Mục | Nội dung |
|---|---|
| Story | Là **Owner**, tôi muốn xem Tư liệu dự án (media bin) |
| Mô tả | Xem toàn bộ ảnh và thuyết minh theo chương → shot; đầu vào của trình chỉnh sửa |
| Use case | [UC-05.08](03-dac-ta-use-case/m05-sinh-tu-lieu.md#uc-0508) · M05 — Sinh tư liệu: storyboard, ảnh, thuyết minh nguyên văn |
| Giai đoạn | P1 |
| Truy vết | FR-MED-03; FR-BOK-13; seq-sinh-tu-lieu |
| Story point | |

```gherkin
Feature: UC-05.08 Xem Tư liệu dự án (media bin)
  Background:
    Given Là thành viên dự án

  Scenario: Luồng chính
    When Editor mở Tư liệu dự án
    And Hệ thống liệt kê chương (trạng thái), mỗi shot: ảnh hiện hành, nút nghe thuyết minh, đoạn văn nguồn, thời lượng, trạng thái, cờ "cần sinh lại"
    And Editor lọc theo trạng thái ("Cần xử lý", OUTDATED, đã đánh dấu) hoặc mở shot để sửa (UC-05.10, UC-05.18)
    Then hiển thị tư liệu và trạng thái
```

#### ST-05-09 Sinh ảnh shot

| Mục | Nội dung |
|---|---|
| Story | Là **Owner (hoặc UC-05.07)**, tôi muốn sinh ảnh shot |
| Mô tả | Sinh ảnh minh họa cho một shot, giữ nhất quán nhân vật bằng ảnh tham chiếu |
| Use case | [UC-05.09](03-dac-ta-use-case/m05-sinh-tu-lieu.md#uc-0509) · M05 — Sinh tư liệu: storyboard, ảnh, thuyết minh nguyên văn |
| Giai đoạn | P1 |
| Truy vết | FR-BOK-09; BR-08; seq-storyboard-sinh-anh |
| Story point | |

```gherkin
Feature: UC-05.09 Sinh ảnh shot
  Background:
    Given Shot có brief; đủ số dư

  Scenario: Luồng chính
    When Hệ thống hiện giá ước tính (khi Editor bấm trên một shot), thực hiện UC-05.17 (giữ tiền) và tạo job GENERATE_SHOT_IMAGE
    And Worker ghép prompt theo BR-08: style → Art Direction → Visual Rules → Chapter rules → brief + facts; đính kèm ảnh tham chiếu cast/location/item; tỷ lệ theo khung hình dự án
    And Moderation đầu vào; gọi Image Provider (retry tối đa 3 lần)
    And Moderation đầu ra; lưu ảnh; tạo Illustration; trừ chi phí thực × 110%, hoàn phần dư; phát illustration.ready
    Then Illustration phiên bản mới DONE, đặt làm hiện hành; tiền trừ

  Scenario: 3a Lỗi sau 3 lần thử hoặc vi phạm chính sách
    Given luồng chính đã tới bước 3
    When Lỗi sau 3 lần thử hoặc vi phạm chính sách
    Then Illustration FAILED, hoàn tiền, shot có nút "Retry"
```

#### ST-05-10 Sửa ảnh

| Mục | Nội dung |
|---|---|
| Story | Là **Owner**, tôi muốn sửa ảnh |
| Mô tả | Chỉnh ảnh shot mà không phải sinh lại từ đầu |
| Use case | [UC-05.10](03-dac-ta-use-case/m05-sinh-tu-lieu.md#uc-0510) · M05 — Sinh tư liệu: storyboard, ảnh, thuyết minh nguyên văn |
| Giai đoạn | P1 |
| Truy vết | FR-BOK-10; BR-14; NFR-SEC-10; seq-storyboard-sinh-anh |
| Story point | |

```gherkin
Feature: UC-05.10 Sửa ảnh
  Background:
    Given Shot có ảnh (hoặc ảnh lỗi để Retry); đủ số dư

  Scenario: Luồng chính
    When Editor mở ảnh và chọn cách sửa (use case con)
    And Hệ thống hiện giá ước tính, giữ tiền, gửi yêu cầu
    And Hệ thống lưu ảnh mới làm hiện hành, trừ chi phí thực × 110%; timeline đồng bộ ảnh mới (UC-06.15)
    Then Illustration phiên bản mới (giữ phiên bản cũ)

  Scenario: 1a Editor chọn "Thay bằng ảnh của tôi" và tải ảnh lên (PNG/JPEG/WebP ≤ 10 MB, cạnh 
    When Editor chọn "Thay bằng ảnh của tôi" và tải ảnh lên (PNG/JPEG/WebP ≤ 10 MB, cạnh ngắn ≥ 512 px; kiểm tra MIME, malware, bỏ EXIF theo NFR-SEC-10). Bước 2 bỏ qua
    Then miễn phí, không tạo job, không gọi Image Provider. Hệ thống lưu Illustration phiên bản mới (edit_kind = UPLOAD, status = DONE), giữ phiên bản cũ, đặt làm hiện hành và đồng bộ timeline (UC-06.15). Ảnh này không bị sinh ảnh hàng loạt ghi đè (BR-14). Ảnh lệch tỷ lệ dự án được xử lý bằng khung hình ở UC-06.06
```

#### ST-05-10a Sửa ảnh theo mô tả (Describe → Edit)

| Mục | Nội dung |
|---|---|
| Story | Là **Owner**, tôi muốn sửa ảnh theo mô tả (Describe → Edit) |
| Mô tả | Sửa ảnh shot bằng cách mô tả thay đổi bằng lời, không sinh lại từ đầu |
| Use case | [UC-05.10a](03-dac-ta-use-case/m05-sinh-tu-lieu.md#uc-0510a) · M05 — Sinh tư liệu: storyboard, ảnh, thuyết minh nguyên văn |
| Giai đoạn | P1 |
| Truy vết | FR-BOK-10; BR-01, BR-02, BR-15, BR-18; 08 §3.2 (`IMAGE_EDIT`); API 2.5 `POST …/illustrations/{iid}:edit`; seq-storyboard-sinh-anh |
| Story point | |

```gherkin
Feature: UC-05.10a Sửa ảnh theo mô tả (Describe → Edit)
  Background:
    Given Shot có ảnh hiện hành DONE; đủ số dư cho giá ước tính

  Scenario: Luồng chính
    When Editor mở ảnh hiện hành và chọn "Describe → Edit"
    And Editor nhập mô tả thay đổi (ví dụ "đổi sang ánh chiều")
    And Hệ thống hiển thị giá ước tính; Editor xác nhận; hệ thống giữ tiền (UC-05.17) và tạo job EDIT_IMAGE
    And Worker chạy moderation đầu vào, gửi ảnh gốc cùng hướng dẫn tới Image Provider (retry tối đa 3 lần), rồi chạy moderation đầu ra
    And Hệ thống lưu Illustration mới (parent_illustration_id = ảnh gốc, instruction = mô tả), đặt làm hiện hành, CAPTURE chi phí thực × 110%, phát illustration.ready
    And Timeline được đồng bộ ảnh mới (UC-06.15)
    Then Illustration mới (edit_kind = EDIT) trở thành ảnh hiện hành; ảnh cũ giữ làm phiên bản trước

  Scenario: 2a Mô tả rỗng
    Given luồng chính đã tới bước 2
    When Mô tả rỗng
    Then không cho gửi

  Scenario: 3a Không đủ số dư
    Given luồng chính đã tới bước 3
    When Không đủ số dư
    Then 402

  Scenario: 4a Lỗi sau 3 lần thử hoặc vi phạm chính sách (451)
    Given luồng chính đã tới bước 4
    When Lỗi sau 3 lần thử hoặc vi phạm chính sách (451)
    Then Illustration FAILED, RELEASE tiền đã giữ, ảnh cũ vẫn là ảnh hiện hành, shot có nút "Retry"
```

#### ST-05-10c Khôi phục phiên bản ảnh

| Mục | Nội dung |
|---|---|
| Story | Là **Owner**, tôi muốn khôi phục phiên bản ảnh |
| Mô tả | Quay lại một phiên bản ảnh cũ của shot, không tốn phí |
| Use case | [UC-05.10c](03-dac-ta-use-case/m05-sinh-tu-lieu.md#uc-0510c) · M05 — Sinh tư liệu: storyboard, ảnh, thuyết minh nguyên văn |
| Giai đoạn | P1 |
| Truy vết | D-04; BR-15; API 2.5 `POST …/illustrations/{iid}:make-current`; seq-storyboard-sinh-anh |
| Story point | |

```gherkin
Feature: UC-05.10c Khôi phục phiên bản ảnh
  Background:
    Given Shot có từ hai phiên bản ảnh trở lên

  Scenario: Luồng chính
    When Editor mở lịch sử ảnh của shot; hệ thống liệt kê các Illustration theo thời gian kèm ảnh thu nhỏ, loại (GENERATE, EDIT, RETRY, UPLOAD), mô tả và thời điểm
    And Editor chọn một phiên bản và bấm "Make current"
    And Hệ thống cập nhật shots.current_illustration_id (không tạo bản ghi mới, không tốn phí)
    And Hệ thống phát illustration.ready và đồng bộ timeline (UC-06.15)
    Then shots.current_illustration_id trỏ phiên bản được chọn

  Scenario: 2a Chọn phiên bản FAILED hoặc PENDING
    Given luồng chính đã tới bước 2
    When Chọn phiên bản FAILED hoặc PENDING
    Then không cho chọn

  Scenario: 2b Phiên bản quá thời hạn lưu 90 ngày (BR-15)
    Given luồng chính đã tới bước 2
    When Phiên bản quá thời hạn lưu 90 ngày (BR-15)
    Then không còn trong danh sách

  Scenario: 3a Phiên bản được chọn sinh từ brief cũ hơn brief hiện tại
    Given luồng chính đã tới bước 3
    When Phiên bản được chọn sinh từ brief cũ hơn brief hiện tại
    Then sau khi khôi phục, shot hiện nhãn "brief đã đổi" như bình thường
```

#### ST-05-17 Giữ / trừ / hoàn tiền

| Mục | Nội dung |
|---|---|
| Story | Là **Hệ thống (được include bởi các use case tốn phí)**, tôi muốn giữ / trừ / hoàn tiền |
| Mô tả | Bảo đảm tiền chính xác cho mọi job AI: giữ giá ước tính tối đa khi tạo job, trừ chi phí thực × 110% khi thành công và hoàn phần dư, hoàn toàn bộ khi thất bại |
| Use case | [UC-05.17](03-dac-ta-use-case/m05-sinh-tu-lieu.md#uc-0517) · M05 — Sinh tư liệu: storyboard, ảnh, thuyết minh nguyên văn |
| Giai đoạn | P1 |
| Truy vết | FR-BIL-11; BR-01, BR-02, BR-03, BR-29; WR-01..05; IC-04, IC-05; act-giu-tru-tien; seq-vong-doi-job |
| Story point | |

```gherkin
Feature: UC-05.17 Giữ / trừ / hoàn tiền
  Background:
    Given Có giá theo price_rules hiệu lực

  Scenario: Luồng chính
    When Hệ thống kiểm tra Idempotency-Key; trùng thì trả kết quả cũ
    And Hệ thống tính giá ước tính tối đa x từ price_rules (đơn giá provider × giới hạn đầu ra × 1,10)
    And Trong một giao dịch: giữ chỗ trong trần chi tiêu ngày bằng câu cập nhật có điều kiện trên daily_ai_budgets (UC-10.12, BR-29, ADR-25)
    And Cùng giao dịch: khóa wallets (FOR UPDATE) của người kích hoạt (BR-03), kiểm tra available ≥ x, ghi HOLD x, tạo job (held_micro = x, budget_day, budget_reserved_micro). Thứ tự khóa luôn là ngân sách ngày → ví
    And Khi job thành công: tính c = min(Σ ai_usage_records.cost_usd × 1,10, x); ghi CAPTURE c và RELEASE x − c cùng giao dịch với kết quả job; đặt jobs.charged_micro = c; trả chỗ ngân sách (reserved −= budget_reserved_micro, spent += Σ cost_usd)
    And Khi job thất bại, bị hủy hoặc vi phạm chính sách: RELEASE x; trả chỗ ngân sách và cộng chi phí provider đã phát sinh (nếu có) vào spent
    And Hệ thống phát wallet.updated
    Then sổ cái có đúng một HOLD cho mỗi job; khi job kết thúc, CAPTURE + RELEASE bằng số đã HOLD và CAPTURE ≤ HOLD (IC-05)

  Scenario: 3a Câu cập nhật ngân sách không trúng dòng nào (vượt trần)
    Given luồng chính đã tới bước 3
    When Câu cập nhật ngân sách không trúng dòng nào (vượt trần)
    Then ROLLBACK, 503 DAILY_BUDGET_EXCEEDED; không giữ tiền, không tạo job

  Scenario: 4a Không đủ số dư
    Given luồng chính đã tới bước 4
    When Không đủ số dư
    Then ROLLBACK cả phần giữ chỗ ngân sách, 402 INSUFFICIENT_BALANCE kèm số còn thiếu

  Scenario: 5a Chi phí thực × 110% lớn hơn số đã giữ (ước tính sai)
    Given luồng chính đã tới bước 5
    When Chi phí thực × 110% lớn hơn số đã giữ (ước tính sai)
    Then chỉ trừ bằng số đã giữ, phần chênh do hệ thống chịu, ghi cảnh báo để chỉnh giới hạn đầu ra trong price_rules [ĐX]

  Scenario: 5b Provider không trả số liệu sử dụng
    Given luồng chính đã tới bước 5
    When Provider không trả số liệu sử dụng
    Then dùng đơn giá × đơn vị đo được (số ảnh, số ký tự) để tính chi phí thực

  Scenario: 5c Job thành công sau một hoặc nhiều lần thử lỗi
    Given luồng chính đã tới bước 5
    When Job thành công sau một hoặc nhiều lần thử lỗi
    Then chỉ tính chi phí của lần thử thành công; chi phí các lần lỗi do hệ thống chịu (WR-09)

  Scenario: 5d Job bị giao lại cho worker khác khi đã kết thúc
    Given luồng chính đã tới bước 5
    When Job bị giao lại cho worker khác khi đã kết thúc
    Then câu nhận việc không trúng dòng nào, worker bỏ qua; không gọi provider và không trừ tiền lần nữa (ADR-29)

  Scenario: *a Job mất heartbeat > 10 phút
    When Job mất heartbeat > 10 phút
    Then reconciler đặt FAILED và RELEASE
```

#### ST-10-01 Cấu hình bảng giá

| Mục | Nội dung |
|---|---|
| Story | Là **Admin**, tôi muốn cấu hình bảng giá |
| Mô tả | Đặt công thức giá cho từng loại thao tác AI (storyboard, ảnh, sửa ảnh, TTS…): hệ số trên chi phí thực (mặc định 1,10), đơn giá provider và giới hạn đầu ra dùng để ước tính |
| Use case | [UC-10.01](03-dac-ta-use-case/m10-quan-tri.md#uc-1001) · M10 — Quản trị |
| Giai đoạn | P1 |
| Truy vết | FR-ADM-01; BR-01; 08 §3 |
| Story point | |

```gherkin
Feature: UC-10.01 Cấu hình bảng giá
  Background:
    Given Là Admin

  Scenario: Luồng chính
    When Admin xem bảng giá hiện hành cùng chi phí AI thực tế trung bình (từ ai_usage_records) và tỷ lệ job bị trừ kịch số đã giữ (ước tính thấp)
    And Admin sửa công thức hoặc giới hạn đầu ra của một thao tác, đặt ngày hiệu lực
    And Hệ thống kiểm tra công thức, lưu phiên bản mới, thực hiện UC-10.09
    Then price_rules phiên bản mới với ngày hiệu lực; job tạo trước đó giữ giá cũ

  Scenario: 2a Hệ số nhỏ hơn 1,00 (bán dưới chi phí thực)
    Given luồng chính đã tới bước 2
    When Hệ số nhỏ hơn 1,00 (bán dưới chi phí thực)
    Then cảnh báo, yêu cầu xác nhận lần hai
```

#### ST-10-03 Quản lý provider & mô hình AI

| Mục | Nội dung |
|---|---|
| Story | Là **Admin**, tôi muốn quản lý provider & mô hình AI |
| Mô tả | Bật/tắt provider (LLM, Image, TTS, STT, Aligner), chọn adapter thật hay mock, thứ tự ưu tiên, mô hình cho người dùng chọn, chi phí đơn vị |
| Use case | [UC-10.03](03-dac-ta-use-case/m10-quan-tri.md#uc-1003) · M10 — Quản trị |
| Giai đoạn | P1 |
| Truy vết | FR-ADM-03; ADR-03, ADR-30; QĐ-119..125; 13 §11.3 |
| Story point | |

```gherkin
Feature: UC-10.03 Quản lý provider & mô hình AI
  Background:
    Given Là Admin; secret của provider đã có trong secret manager

  Scenario: Luồng chính
    When Admin xem danh sách provider: trạng thái, tỷ lệ lỗi, độ trễ, chi phí 24 giờ
    And Admin bật/tắt, đổi thứ tự ưu tiên, nhập tên secret (không nhập key)
    And Admin bấm "Kiểm tra kết nối"; hệ thống gọi thử
    And Hệ thống lưu, ghi audit log
    Then ai_providers/ai_models cập nhật; ProviderRouter dùng cấu hình mới

  Scenario: 3a Kiểm tra thất bại
    Given luồng chính đã tới bước 3
    When Kiểm tra thất bại
    Then không cho bật provider

  Scenario: 2a Tắt provider đang là duy nhất của một loại
    Given luồng chính đã tới bước 2
    When Tắt provider đang là duy nhất của một loại
    Then chặn
```

#### ST-10-04 Quản lý danh mục style

| Mục | Nội dung |
|---|---|
| Story | Là **Admin**, tôi muốn quản lý danh mục style |
| Mô tả | Thêm/sửa/ẩn style nghệ thuật (tên, mô tả, đoạn prompt, ảnh mẫu) |
| Use case | [UC-10.04](03-dac-ta-use-case/m10-quan-tri.md#uc-1004) · M10 — Quản trị |
| Giai đoạn | P1 |
| Truy vết | FR-ADM-03 |
| Story point | |

```gherkin
Feature: UC-10.04 Quản lý danh mục style
  Background:
    Given Là Admin

  Scenario: Luồng chính
    When Admin tạo hoặc sửa style, sinh ảnh mẫu thử
    And Admin kích hoạt; style xuất hiện trong Styles Library
    Then styles cập nhật; dự án đang dùng style bị ẩn không bị ảnh hưởng
```

#### ST-10-05 Quản lý danh mục giọng đọc

| Mục | Nội dung |
|---|---|
| Story | Là **Admin**, tôi muốn quản lý danh mục giọng đọc |
| Mô tả | Quản lý giọng TTS cho người dùng chọn (ngôn ngữ, giới tính, audio mẫu); giọng được chọn ở P0 theo WER trên golden set |
| Use case | [UC-10.05](03-dac-ta-use-case/m10-quan-tri.md#uc-1005) · M10 — Quản trị |
| Giai đoạn | P1 |
| Truy vết | FR-ADM-03 |
| Story point | |

```gherkin
Feature: UC-10.05 Quản lý danh mục giọng đọc
  Background:
    Given Là Admin; provider TTS đang bật

  Scenario: Luồng chính
    When Admin đồng bộ danh sách giọng từ provider hoặc thêm thủ công
    And Admin sinh audio mẫu (câu chuẩn tiếng Việt/Anh), đánh giá WER mẫu
    And Admin bật giọng (gán cho gói tiêu chuẩn / cao cấp: sau MVP)
    Then voices cập nhật

  Scenario: 2a WER mẫu > 3%
    Given luồng chính đã tới bước 2
    When WER mẫu > 3%
    Then cảnh báo, không khuyến nghị bật
```

#### ST-10-09 Ghi audit log

| Mục | Nội dung |
|---|---|
| Story | Là **Hệ thống (được include)**, tôi muốn ghi audit log |
| Mô tả | Ghi lại mọi hành động quản trị: thay đổi cấu hình, danh sách mời, điều chỉnh số dư |
| Use case | [UC-10.09](03-dac-ta-use-case/m10-quan-tri.md#uc-1009) · M10 — Quản trị |
| Giai đoạn | P1 |
| Truy vết | NFR-PRV-04 |
| Story point | |

```gherkin
Feature: UC-10.09 Ghi audit log
  Background:
    Given Có hành động cần kiểm toán

  Scenario: Luồng chính
    When Use case gọi ghi audit trong cùng giao dịch với thay đổi
    And Hệ thống lưu bản ghi chỉ thêm (append-only)
    Then bản ghi bất biến: ai, khi nào, đối tượng, giá trị trước/sau, lý do, IP. Giữ 2 năm

  Scenario: 2a Không ghi được audit
    Given luồng chính đã tới bước 2
    When Không ghi được audit
    Then rollback cả thay đổi
```

#### ST-10-11 Quản lý danh sách mời beta

| Mục | Nội dung |
|---|---|
| Story | Là **Admin**, tôi muốn quản lý danh sách mời beta |
| Mô tả | Thêm, gỡ và xem email được mời tham gia closed beta; chỉ email trong danh sách mới tạo được hồ sơ (BR-30) |
| Use case | [UC-10.11](03-dac-ta-use-case/m10-quan-tri.md#uc-1011) · M10 — Quản trị |
| Giai đoạn | P1 |
| Truy vết | FR-AUTH-11; BR-30; QĐ-25; 04 §3.1 `beta_invites` |
| Story point | |

```gherkin
Feature: UC-10.11 Quản lý danh sách mời beta
  Background:
    Given Là Admin; truy cập được môi trường chạy lệnh quản trị

  Scenario: Luồng chính
    When Admin chạy add với một hoặc nhiều email (hoặc file CSV), kèm ghi chú (ví dụ "nhóm khảo sát 1")
    And Hệ thống chuẩn hóa email (bỏ khoảng trắng, chữ thường), kiểm tra định dạng, tạo beta_invites cho email chưa có
    And Hệ thống thực hiện UC-10.09 và in kết quả: số email thêm mới, số đã có, số lỗi
    And Admin gửi lời mời cho người dùng qua kênh riêng (email, nhóm chat) kèm link ứng dụng
    And Lệnh list hiển thị email, ngày mời, đã tạo hồ sơ chưa (used_by_user_id), đã thu hồi chưa
    Then beta_invites cập nhật; có audit log

  Scenario: 2a Email sai định dạng
    Given luồng chính đã tới bước 2
    When Email sai định dạng
    Then bỏ qua email đó, báo trong kết quả

  Scenario: 2b Email đã có và đang hiệu lực
    Given luồng chính đã tới bước 2
    When Email đã có và đang hiệu lực
    Then không tạo trùng

  Scenario: 2c Email đã bị thu hồi trước đó
    Given luồng chính đã tới bước 2
    When Email đã bị thu hồi trước đó
    Then add mở lại lời mời (xóa revoked_at)

  Scenario: *a remove
    When remove
    Then đặt revoked_at; người chưa tạo hồ sơ không vào được nữa; người đã có hồ sơ vẫn đăng nhập được (BR-30). Muốn chặn hẳn thì Admin khóa hồ sơ (users.status = LOCKED)

  Scenario: *b Kết thúc beta, mở rộng
    When Kết thúc beta, mở rộng
    Then Admin đặt system_settings.beta_invite_only = false
```

### Giai đoạn P2

#### ST-01-03 Xem Dashboard

| Mục | Nội dung |
|---|---|
| Story | Là **User**, tôi muốn xem Dashboard |
| Mô tả | Xem tổng quan tài khoản: trạng thái (Free / Đã nạp tiền), số dư ví, phần Free đã dùng trong tháng, số dự án, lối tắt |
| Use case | [UC-01.03](03-dac-ta-use-case/m01-tich-hop-sso.md#uc-0103) · M01 — Tích hợp SSO & hồ sơ |
| Giai đoạn | P2 |
| Truy vết | FR-AUTH-09; FR-BIL-05, 12; API 2.1 `GET /me/dashboard` |
| Story point | |

```gherkin
Feature: UC-01.03 Xem Dashboard
  Background:
    Given Đã đăng nhập

  Scenario: Luồng chính
    When User mở Dashboard
    And Hệ thống trả về trạng thái tài khoản, số dư khả dụng và đang giữ, với tài khoản Free thêm số lần render và phút video đã dùng trong tháng (BR-27); số dự án; lối tắt "Nạp tiền", "Lịch sử chi tiêu", "Projects", "Pricing"
    And User chọn một lối tắt để đi tiếp
    Then hiển thị số liệu mới nhất

  Scenario: 2a Không lấy được số dư (lỗi tạm thời)
    Given luồng chính đã tới bước 2
    When Không lấy được số dư (lỗi tạm thời)
    Then hiển thị phần còn lại, ô số dư hiện "Đang cập nhật"
```

#### ST-01-05 Mở trang quản lý tài khoản SSO

| Mục | Nội dung |
|---|---|
| Story | Là **User**, tôi muốn mở trang quản lý tài khoản SSO |
| Mô tả | Chuyển tới trang hồ sơ của SSO để đổi mật khẩu, email, MFA |
| Use case | [UC-01.05](03-dac-ta-use-case/m01-tich-hop-sso.md#uc-0105) · M01 — Tích hợp SSO & hồ sơ |
| Giai đoạn | P2 |
| Truy vết | FR-AUTH-09, C-05 |
| Story point | |

```gherkin
Feature: UC-01.05 Mở trang quản lý tài khoản SSO
  Background:
    Given Đang ở Dashboard

  Scenario: Luồng chính
    When User bấm "Quản lý tài khoản" trên Dashboard
    And Hệ thống mở URL trang tài khoản của SSO (cấu hình) trong tab mới
    And Thay đổi email/tên trên SSO được đồng bộ ở lần đăng nhập kế tiếp (UC-01.01b)
    Then trang SSO mở trong tab mới
```

#### ST-03-01a Sao chép toàn văn

| Mục | Nội dung |
|---|---|
| Story | Là **Owner**, tôi muốn sao chép toàn văn |
| Mô tả | Sao chép toàn bộ văn bản truyện vào clipboard |
| Use case | [UC-03.01a](03-dac-ta-use-case/m03-ban-thao-chuong.md#uc-0301a) · M03 — Bản thảo & chương |
| Giai đoạn | P2 |
| Truy vết | FR-MAN-01; API 2.3 `GET /projects/{pid}/source` |
| Story point | |

```gherkin
Feature: UC-03.01a Sao chép toàn văn
  Background:
    Given Dự án có văn bản; đang ở màn hình Write (?v=source)

  Scenario: Luồng chính
    When Editor bấm "Copy text"
    And Hệ thống ghép tiêu đề và nội dung từng chương theo order_index, mỗi chương cách nhau một dòng trống [ĐX]
    And Hệ thống ghi chuỗi vào clipboard của trình duyệt
    And Giao diện báo "Đã sao chép N ký tự"
    Then clipboard chứa toàn văn

  Scenario: 3a Trình duyệt chặn quyền clipboard
    Given luồng chính đã tới bước 3
    When Trình duyệt chặn quyền clipboard
    Then hiện hộp văn bản đã chọn sẵn toàn bộ để Editor tự sao chép

  Scenario: 2a Dữ liệu chương chưa tải đủ ở client
    Given luồng chính đã tới bước 2
    When Dữ liệu chương chưa tải đủ ở client
    Then tải từ GET /source rồi mới ghép
```

#### ST-03-01b Nhập lại (Re-import)

| Mục | Nội dung |
|---|---|
| Story | Là **Owner**, tôi muốn nhập lại (Re-import) |
| Mô tả | Thay toàn bộ văn bản truyện bằng một bản mới; bản cũ vẫn còn trong Archive nếu Editor lưu |
| Use case | [UC-03.01b](03-dac-ta-use-case/m03-ban-thao-chuong.md#uc-0301b) · M03 — Bản thảo & chương |
| Giai đoạn | P2 |
| Truy vết | FR-PRJ-02, FR-PRJ-03; BR-06, BR-12, BR-19, BR-21; API 2.3 `PUT /projects/{pid}/source`; seq-import-chia-chuong |
| Story point | |

```gherkin
Feature: UC-03.01b Nhập lại (Re-import)
  Background:
    Given Dự án có văn bản; không chương nào đang bị khóa bởi job (BR-12)

  Scenario: Luồng chính
    When Editor chọn "Re-import". Hệ thống cảnh báo hậu quả (mọi storyboard, ảnh, thuyết minh và timeline của các chương hiện có sẽ OUTDATED) và gợi ý lưu Archive trước (UC-03.11)
    And Editor dán văn bản hoặc tải file mới (.txt, .md, .docx)
    And Hệ thống thực hiện UC-02.02a và hiển thị bản xem trước (số ký tự, số đoạn)
    And Editor xác nhận đã hiểu hậu quả
    And Trong một giao dịch, hệ thống tạo SourceText mới, thay các chương hiện có bằng một Chapter #1 chứa toàn văn mới, cập nhật projects.current_source_id
    And Hệ thống đánh dấu mọi tư liệu và timeline của các chương cũ là OUTDATED, phát chapters.restructured
    And Hệ thống mở màn hình Write và gợi ý bước "Chia chương" (UC-03.03)
    Then dự án có SourceText mới và đúng một Chapter #1 chứa toàn văn mới; tư liệu và timeline của các chương cũ chuyển OUTDATED

  Scenario: 1a Có chương đang bị khóa bởi job
    When Có chương đang bị khóa bởi job
    Then 423 RESOURCE_LOCKED, nêu job đang chạy

  Scenario: 3a File không đạt UC-02.02a
    Given luồng chính đã tới bước 3
    When File không đạt UC-02.02a
    Then báo lỗi, giữ nguyên văn bản hiện tại

  Scenario: 5a Dự án đã thay đổi (phiên bản khác) trong lúc Editor xem trước
    Given luồng chính đã tới bước 5
    When Dự án đã thay đổi (phiên bản khác) trong lúc Editor xem trước
    Then 409, yêu cầu tải lại rồi làm lại [ĐX]

  Scenario: 5b Lỗi ghi dữ liệu
    Given luồng chính đã tới bước 5
    When Lỗi ghi dữ liệu
    Then rollback toàn bộ, giữ nội dung đã nhập trên form
```

#### ST-03-02a Dời ranh giới shot ✂8

| Mục | Nội dung |
|---|---|
| Story | Là **Owner**, tôi muốn dời ranh giới shot |
| Mô tả | Kéo vạch ranh giới giữa hai shot liền kề ngay trên văn bản chương trong Workspace, theo từng câu; sau đó AI viết lại brief của 2 shot bị ảnh hưởng để ảnh khớp đoạn văn mới |
| Use case | [UC-03.02a](03-dac-ta-use-case/m03-ban-thao-chuong.md#uc-0302a) · M03 — Bản thảo & chương |
| Giai đoạn | P2 ✂8 |
| Truy vết | FR-BOK-01b, FR-NAR-09; BR-01, BR-06, BR-20, BR-33; IC-08, IC-09; 08 §3.2 (`REWRITE_SHOT`); API 2.5 `POST …/storyboards/{did}:move-boundary`, 06 §4.7; seq-doi-ranh-gioi-shot |
| Story point | |

```gherkin
Feature: UC-03.02a Dời ranh giới shot
  Background:
    Given Chương có storyboard hiện hành; không bị khóa (BR-12); đủ số dư cho giá ước tính

  Scenario: Luồng chính
    When Editor kéo vạch giữa shot trái và shot phải; vạch chỉ dừng ở ranh giới câu
    And Khi thả, client gọi :move-boundary?dryRun=true {leftShotId, rightShotId, deltaSentences}
    And Hệ thống hiện hộp xác nhận: câu nào chuyển sang shot nào, thời lượng đọc ước tính mới của hai shot, giá ước tính viết lại 2 brief (BR-01)
    And Editor bấm "Dời và viết lại brief"
    And Trong một giao dịch, hệ thống cập nhật source_start, source_end của hai shot, thực hiện UC-05.01a, giữ tiền (UC-05.17) và tạo 2 job REWRITE_SHOT (UC-05.06e, ghi chú "đoạn nguồn đã đổi")
    And Thuyết minh của hai shot chuyển OUTDATED (IC-09); hệ thống phát shot.updated và đồng bộ timeline (UC-06.15)
    And Khi job xong, brief mới được lưu; hệ thống gợi ý sinh lại ảnh và thuyết minh cho hai shot (UC-05.07c) kèm giá
    Then hai shot đổi đoạn nguồn, phủ kín vẫn 100% (IC-08); brief của hai shot được viết lại; thuyết minh của hai shot OUTDATED; ảnh hiện tại được đánh dấu "brief đã đổi"

  Scenario: 1a Kéo làm một shot không còn câu nào
    When Kéo làm một shot không còn câu nào
    Then vạch bật về vị trí cũ, hiện "Mỗi shot cần ít nhất một câu"

  Scenario: 1b Kéo vượt qua vạch kế bên
    When Kéo vượt qua vạch kế bên
    Then chặn; chỉ dời giữa hai shot liền kề

  Scenario: 3a Đoạn nguồn mới của một shot đọc quá 30 giây (khoảng 450 ký tự tiếng Việt)
    Given luồng chính đã tới bước 3
    When Đoạn nguồn mới của một shot đọc quá 30 giây (khoảng 450 ký tự tiếng Việt)
    Then cảnh báo, vẫn cho phép

  Scenario: 4a Editor bấm "Hủy"
    Given luồng chính đã tới bước 4
    When Editor bấm "Hủy"
    Then vạch bật về vị trí cũ, không thay đổi gì (BR-33)

  Scenario: 5a Không đủ số dư
    Given luồng chính đã tới bước 5
    When Không đủ số dư
    Then 402; vạch bật về, gợi ý nạp tiền (UC-09.03)

  Scenario: 5b Chạm trần chi tiêu ngày
    Given luồng chính đã tới bước 5
    When Chạm trần chi tiêu ngày
    Then 503 DAILY_BUDGET_EXCEEDED; không dời (BR-29)

  Scenario: 5c 409 (chương hoặc shot vừa đổi ở tab khác)
    Given luồng chính đã tới bước 5
    When 409 (chương hoặc shot vừa đổi ở tab khác)
    Then tải lại vạch ranh giới (BR-05)

  Scenario: 5d Chương đang bị khóa
    Given luồng chính đã tới bước 5
    When Chương đang bị khóa
    Then 423 RESOURCE_LOCKED

  Scenario: 7a Job viết lại brief lỗi
    Given luồng chính đã tới bước 7
    When Job viết lại brief lỗi
    Then ranh giới đã dời vẫn giữ, brief cũ giữ nguyên, tiền giữ được hoàn; shot có nút "Viết lại brief" (UC-05.06e)
```

#### ST-04-07 Xem dòng thời gian truyện ✂5

| Mục | Nội dung |
|---|---|
| Story | Là **Owner**, tôi muốn xem dòng thời gian truyện |
| Mô tả | Xem dòng thời gian (ngày, mùa, tóm tắt) theo chương do AI dựng |
| Use case | [UC-04.07](03-dac-ta-use-case/m04-the-gioi-truyen.md#uc-0407) · M04 — Thế giới truyện |
| Giai đoạn | P2 ✂5 |
| Truy vết | FR-WLD-08; seq-the-gioi-truyen |
| Story point | |

```gherkin
Feature: UC-04.07 Xem dòng thời gian truyện
  Background:
    Given Đã chạy phân tích (UC-04.09) ít nhất một lần

  Scenario: Luồng chính
    When Editor mở Story timeline
    And Hệ thống hiển thị các mốc (nhãn ngày, mùa, chương, tóm tắt)
    And Editor bấm một mốc để mở chương tương ứng
    Then hiển thị timeline truyện theo tỷ lệ thời gian

  Scenario: 2a Chưa có dữ liệu
    Given luồng chính đã tới bước 2
    When Chưa có dữ liệu
    Then hiện nút "Phân tích" (UC-04.09)

  Scenario: 2b Editor đổi chế độ xem
    Given luồng chính đã tới bước 2
    When Editor đổi chế độ xem
    Then "Theo mạch truyện" (thứ tự chương, mặc định) hoặc "Theo thứ tự thời gian" (sắp theo nhãn ngày/mùa, dùng cho truyện có hồi tưởng). Hệ thống sắp theo chrono_index; mốc chưa có (NULL) xếp cuối nhóm "Chưa xác định"
```

#### ST-04-08 Xem đồ thị quan hệ ✂4

| Mục | Nội dung |
|---|---|
| Story | Là **Owner**, tôi muốn xem đồ thị quan hệ |
| Mô tả | Xem đồ thị quan hệ giữa các nhân vật và diễn biến |
| Use case | [UC-04.08](03-dac-ta-use-case/m04-the-gioi-truyen.md#uc-0408) · M04 — Thế giới truyện |
| Giai đoạn | P2 ✂4 |
| Truy vết | FR-WLD-09; seq-the-gioi-truyen |
| Story point | |

```gherkin
Feature: UC-04.08 Xem đồ thị quan hệ
  Background:
    Given Đã chạy phân tích

  Scenario: Luồng chính
    When Editor mở Relationship graph
    And Hệ thống vẽ nút (nhân vật) và cạnh (nhãn quan hệ, diễn biến, chương bắt đầu)
    And Editor bấm một cạnh để đọc diễn biến
    Then hiển thị đồ thị
```

#### ST-04-09 Phân tích lại (Re-analyse) ✂4 ✂5

| Mục | Nội dung |
|---|---|
| Story | Là **Owner**, tôi muốn phân tích lại (Re-analyse) |
| Mô tả | Dựng lại Timeline và Relationships sau khi văn bản hoặc tài sản thay đổi |
| Use case | [UC-04.09](03-dac-ta-use-case/m04-the-gioi-truyen.md#uc-0409) · M04 — Thế giới truyện |
| Giai đoạn | P2 ✂4 ✂5 |
| Truy vết | FR-WLD-08, FR-WLD-09; BR-01, BR-02; 08 §3.2 (`STORY_META`); seq-the-gioi-truyen |
| Story point | |

```gherkin
Feature: UC-04.09 Phân tích lại (Re-analyse)
  Background:
    Given Có văn bản

  Scenario: Luồng chính
    When Editor bấm "Re-analyse"
    And Hệ thống hiện giá ước tính; Editor xác nhận; hệ thống giữ tiền (UC-05.17) và tạo job STORY_META; LLM trả mốc thời gian theo chương (kèm thứ hạng thời gian trong truyện, lưu chrono_index) và cặp quan hệ (theo tên/bí danh tài sản)
    And Hệ thống thay dữ liệu cũ, hiển thị kết quả
    Then timeline_events và relationships được thay mới

  Scenario: 2a Tên nhân vật không khớp tài sản
    Given luồng chính đã tới bước 2
    When Tên nhân vật không khớp tài sản
    Then bỏ qua cạnh đó, liệt kê để Editor thêm tài sản
```

#### ST-05-07 Sinh tư liệu chương

| Mục | Nội dung |
|---|---|
| Story | Là **Owner**, tôi muốn sinh tư liệu chương |
| Mô tả | Bước 4 của luồng: một thao tác sinh ảnh + thuyết minh nguyên văn cho mọi shot của một hoặc nhiều chương |
| Use case | [UC-05.07](03-dac-ta-use-case/m05-sinh-tu-lieu.md#uc-0507) · M05 — Sinh tư liệu: storyboard, ảnh, thuyết minh nguyên văn |
| Giai đoạn | P2 |
| Truy vết | FR-MED-01..05; BR-01, BR-02, BR-11, BR-29; WR-05; seq-sinh-tu-lieu |
| Story point | |

```gherkin
Feature: UC-05.07 Sinh tư liệu chương
  Background:
    Given Chương có văn bản; dự án có style; đã chọn giọng đọc (UC-05.11); khuyến nghị tài sản đã có ảnh tham chiếu

  Scenario: Luồng chính
    When Editor chọn một hoặc nhiều chương, bấm "Sinh tư liệu"
    And Hệ thống ước tính số shot (theo storyboard hiện có hoặc độ dài chương) và hiện một giá ước tính tối đa: storyboard (nếu chưa có) + số ảnh × đơn giá ảnh + số ký tự × đơn giá TTS, đã gồm phí 10%
    And Editor xác nhận; hệ thống thực hiện UC-05.17 (giữ tiền một lần cho cả lượt, ở job cha) và tạo job cha GENERATE_MEDIA_CHAPTER; job con không giữ tiền riêng (WR-05)
    And Chương chưa có storyboard hiện hành: thực hiện UC-05.07a
    And Với mỗi shot, chạy song song UC-05.09 (ảnh) và UC-05.13 (thuyết minh)
    And Mọi shot có ảnh và thuyết minh DONE: hệ thống đánh dấu chương "Sẵn sàng dựng", dựng bản nháp timeline, thông báo chapter.media-ready kèm số tiền thực đã trừ và số đã hoàn
    And Editor có thể nghe và đánh dấu shot cần sinh lại (UC-05.18); việc này không bắt buộc
    Then mọi shot có ảnh DONE và thuyết minh DONE; chương "Sẵn sàng dựng"; có bản nháp timeline (UC-06.01a)

  Scenario: 3a Không đủ số dư
    Given luồng chính đã tới bước 3
    When Không đủ số dư
    Then 402; gợi ý nạp tiền (UC-09.03) hoặc chọn ít chương hơn

  Scenario: 3b Chạm trần chi tiêu AI trong ngày
    Given luồng chính đã tới bước 3
    When Chạm trần chi tiêu AI trong ngày
    Then 503 DAILY_BUDGET_EXCEEDED, không tạo job (BR-29)

  Scenario: 4a Số shot thực tế khác ước tính
    Given luồng chính đã tới bước 4
    When Số shot thực tế khác ước tính
    Then không giữ thêm giữa chừng; giá ước tính đã tính theo trần trên (độ dài chương × 1,2), số trừ thực không vượt số đã giữ (WR-04, WR-05)

  Scenario: 5a Còn ảnh hoặc thuyết minh lỗi
    Given luồng chính đã tới bước 5
    When Còn ảnh hoặc thuyết minh lỗi
    Then chương "Cần xử lý", liệt kê shot; Editor xử lý qua UC-05.10 hoặc UC-05.07c

  Scenario: *a Editor sửa văn bản chương trong lúc job chạy
    When Editor sửa văn bản chương trong lúc job chạy
    Then chương bị khóa (BR-12) đến khi job xong. Khóa được mở trong cùng giao dịch kết thúc job cha (thành công, lỗi hay hủy); nếu worker chết, reconciler mở khóa trong ≤ 15 phút (05 §6.1 bước 8, ADR-29)
```

#### ST-05-07a Dựng storyboard tự động

| Mục | Nội dung |
|---|---|
| Story | Là **Hệ thống**, tôi muốn dựng storyboard tự động |
| Mô tả | Tự tạo storyboard cho chương chưa có storyboard hiện hành để việc sinh tư liệu chạy liền một mạch |
| Use case | [UC-05.07a](03-dac-ta-use-case/m05-sinh-tu-lieu.md#uc-0507a) · M05 — Sinh tư liệu: storyboard, ảnh, thuyết minh nguyên văn |
| Giai đoạn | P2 |
| Truy vết | FR-BOK-01; BR-07, BR-20; 08 §3.2 (`STORYBOARD_DRAFT`, nằm trong giá ước tính của UC-05.07); API 2.5 `POST …/media:generate`; seq-sinh-tu-lieu |
| Story point | |

```gherkin
Feature: UC-05.07a Dựng storyboard tự động
  Background:
    Given Chương có văn bản, không bị khóa; chưa có storyboard hiện hành

  Scenario: Luồng chính
    When Hệ thống kiểm tra chương đã có storyboard hiện hành hay chưa; nếu có thì bỏ qua use case này
    And Hệ thống lấy thời lượng mục tiêu mỗi ảnh từ projects.target_shot_seconds (mặc định 20 giây, QĐ-112)
    And Hệ thống chạy UC-05.01 (job con STORYBOARD_DRAFT, kind = INITIAL)
    And Hệ thống đặt bản nháp làm hiện hành (BR-07)
    And Hệ thống trả số shot thực tế cho UC-05.07 để fan-out job con; tiền đã giữ không đổi (UC-05.07 nhánh 4a, WR-05)
    Then chương có một bản nháp hiện hành gồm N shot phủ kín 100%

  Scenario: 3a Job lỗi sau retry (UC-05.01 nhánh 3a)
    Given luồng chính đã tới bước 3
    When Job lỗi sau retry (UC-05.01 nhánh 3a)
    Then chương NEEDS_ATTENTION, không sinh ảnh và thuyết minh cho chương này; các chương khác trong cùng lượt vẫn chạy

  Scenario: 1a Chương đang bị khóa
    When Chương đang bị khóa
    Then 423 RESOURCE_LOCKED
```

#### ST-05-07b Xem tiến độ theo shot

| Mục | Nội dung |
|---|---|
| Story | Là **Owner**, tôi muốn xem tiến độ theo shot |
| Mô tả | Theo dõi theo thời gian thực trạng thái ảnh và thuyết minh của từng shot trong lúc sinh tư liệu |
| Use case | [UC-05.07b](03-dac-ta-use-case/m05-sinh-tu-lieu.md#uc-0507b) · M05 — Sinh tư liệu: storyboard, ảnh, thuyết minh nguyên văn |
| Giai đoạn | P2 |
| Truy vết | FR-MED-01..05; API 2.5 `GET …/media?chapterId=`; API 3 sự kiện `illustration.ready`, `narration.updated`, `job.updated`; seq-sinh-tu-lieu |
| Story point | |

```gherkin
Feature: UC-05.07b Xem tiến độ theo shot
  Background:
    Given Có job GENERATE_MEDIA_CHAPTER đang chạy hoặc đã chạy cho chương

  Scenario: Luồng chính
    When Hệ thống tải ảnh chụp ban đầu từ media bin (GET /projects/{pid}/media?chapterId=)
    And Hệ thống hiển thị bảng: mỗi shot một hàng, hai cột Ảnh và Thuyết minh với trạng thái (PENDING, GENERATING, DONE, FAILED; thêm OUTDATED và cờ "cần sinh lại" cho thuyết minh)
    And Hệ thống cập nhật bảng qua SSE: illustration.ready, narration.updated, job.updated
    And Editor lọc các shot "Cần xử lý" hoặc đã đánh dấu và mở từng shot để xử lý: ảnh lỗi (UC-05.10), nghe thuyết minh (UC-05.18), sinh lại phần thiếu (UC-05.07c)
    Then Editor thấy trạng thái của từng shot

  Scenario: 3a Mất kết nối SSE
    Given luồng chính đã tới bước 3
    When Mất kết nối SSE
    Then client nối lại với Last-Event-ID; nếu thiếu sự kiện thì tải lại ảnh chụp ở bước 1

  Scenario: 3b Job bị hủy hoặc lỗi hàng loạt
    Given luồng chính đã tới bước 3
    When Job bị hủy hoặc lỗi hàng loạt
    Then bảng hiển thị trạng thái hiện có của từng shot, chương ở "Cần xử lý"
```

#### ST-05-07c Sinh lại phần thiếu / lỗi

| Mục | Nội dung |
|---|---|
| Story | Là **Owner**, tôi muốn sinh lại phần thiếu / lỗi |
| Mô tả | Chỉ sinh lại những phần còn thiếu, bị lỗi hoặc đã lỗi thời, không đụng tới phần đã đạt |
| Use case | [UC-05.07c](03-dac-ta-use-case/m05-sinh-tu-lieu.md#uc-0507c) · M05 — Sinh tư liệu: storyboard, ảnh, thuyết minh nguyên văn |
| Giai đoạn | P2 |
| Truy vết | BR-11, BR-12, BR-14; WR-05; API 2.5 `GET …/media:quote`, `POST …/media:generate {only, parts}`; seq-sinh-tu-lieu |
| Story point | |

```gherkin
Feature: UC-05.07c Sinh lại phần thiếu / lỗi
  Background:
    Given Chương có shot thiếu, lỗi, OUTDATED hoặc được đánh dấu cần sinh lại; chương không bị khóa; đủ số dư

  Scenario: Luồng chính
    When Editor chọn phạm vi: chỉ phần thiếu, chỉ phần lỗi, chỉ OUTDATED hoặc chỉ shot được đánh dấu; chỉ ảnh, chỉ thuyết minh hoặc cả hai
    And Hệ thống xác định danh sách shot và phần cần chạy. Ảnh đã DONE hợp lệ và ảnh do Editor tải lên (BR-14) không nằm trong danh sách
    And Hệ thống hiển thị giá ước tính (media:quote); Editor xác nhận
    And Hệ thống giữ tiền (UC-05.17) và tạo job cha, mỗi shot một hoặc hai job con (ảnh, thuyết minh)
    And Các job con chạy như bước 5 của UC-05.07; tiến độ hiển thị ở UC-05.07b
    And Khi mọi shot đạt, chương "Sẵn sàng dựng" và timeline được đồng bộ (UC-06.15)
    Then các shot được chọn có tư liệu đạt; chương tiến tới "Sẵn sàng dựng" khi mọi shot đạt

  Scenario: 2a Không có gì cần sinh trong phạm vi đã chọn
    Given luồng chính đã tới bước 2
    When Không có gì cần sinh trong phạm vi đã chọn
    Then báo "Không có phần nào cần sinh lại", không tạo job

  Scenario: 3a Không đủ số dư
    Given luồng chính đã tới bước 3
    When Không đủ số dư
    Then 402; gợi ý chọn phạm vi nhỏ hơn hoặc nạp tiền (UC-09.03)

  Scenario: 5a Vẫn còn shot lỗi
    Given luồng chính đã tới bước 5
    When Vẫn còn shot lỗi
    Then chương ở "Cần xử lý", liệt kê shot (UC-05.07 nhánh 5a)

  Scenario: *a Chương đang bị job khác khóa
    When Chương đang bị job khác khóa
    Then 423 RESOURCE_LOCKED
```

#### ST-05-11 Cài đặt thuyết minh

| Mục | Nội dung |
|---|---|
| Story | Là **Owner**, tôi muốn cài đặt thuyết minh |
| Mô tả | Chọn ngôn ngữ, giọng đọc, tốc độ, cao độ, khoảng nghỉ, quy tắc đọc ký hiệu trình bày |
| Use case | [UC-05.11](03-dac-ta-use-case/m05-sinh-tu-lieu.md#uc-0511) · M05 — Sinh tư liệu: storyboard, ảnh, thuyết minh nguyên văn |
| Giai đoạn | P2 |
| Truy vết | FR-NAR-01, 03; BR-19; 08 §6; API 2.5 `PUT …/narration-settings`; seq-thuyet-minh-nguyen-van |
| Story point | |

```gherkin
Feature: UC-05.11 Cài đặt thuyết minh
  Background:
    Given Là thành viên dự án

  Scenario: Luồng chính
    When Editor chọn ngôn ngữ (Auto, tiếng Việt hoặc tiếng Anh) và giọng trong danh mục
    And Editor chỉnh tốc độ (0,8–1,3×), cao độ, nghỉ câu/đoạn
    And Editor xem danh sách quy tắc ký hiệu SYM-01..05 (mẫu, ví dụ, cách đọc) và bật/tắt từng quy tắc cho dự án; mặc định bật tất cả
    And Hệ thống lưu
    Then narration_settings cập nhật; áp cho các lần sinh sau

  Scenario: 4a Đổi giọng, tốc độ hoặc quy tắc ký hiệu khi đã có thuyết minh
    Given luồng chính đã tới bước 4
    When Đổi giọng, tốc độ hoặc quy tắc ký hiệu khi đã có thuyết minh
    Then hỏi có sinh lại toàn bộ không (hiện giá ước tính); nếu không thì chỉ áp cho shot sinh mới

  Scenario: *a Ngưỡng WER chỉ hiện khi bật kiểm chứng ASR (sau MVP)
    When Ngưỡng WER chỉ hiện khi bật kiểm chứng ASR (sau MVP)
    Then hệ thống xử lý như mô tả
```

#### ST-05-11a Nghe thử giọng

| Mục | Nội dung |
|---|---|
| Story | Là **Owner**, tôi muốn nghe thử giọng |
| Mô tả | Nghe thử một giọng đọc trước khi chọn, bằng mẫu có sẵn hoặc bằng một câu trong truyện |
| Use case | [UC-05.11a](03-dac-ta-use-case/m05-sinh-tu-lieu.md#uc-0511a) · M05 — Sinh tư liệu: storyboard, ảnh, thuyết minh nguyên văn |
| Giai đoạn | P2 |
| Truy vết | FR-NAR-01; BR-32; QĐ-136; API 2.5 `GET /voices`, `POST …/pronunciations:preview`; seq-thuyet-minh-nguyen-van |
| Story point | |

```gherkin
Feature: UC-05.11a Nghe thử giọng
  Background:
    Given Là thành viên dự án; danh mục giọng có ít nhất một giọng đang bật

  Scenario: Luồng chính
    When Editor bấm ▶ cạnh một giọng trong danh mục
    And *Mẫu có sẵn:* hệ thống phát audio mẫu (voices.sample_media_id)
    And *Câu trong truyện:* Editor chọn hoặc nhập một câu (≤ 200 ký tự); hệ thống gọi pronunciations:preview {text} và phát audio ngắn (miễn phí, ≤ 10 lần/phút, QĐ-136)
    And Editor so sánh các giọng và chọn một giọng ở UC-05.11 bước 1
    Then Editor nghe được giọng

  Scenario: 3a Câu dài hơn 200 ký tự
    Given luồng chính đã tới bước 3
    When Câu dài hơn 200 ký tự
    Then cắt ở ranh giới câu hoặc báo lỗi

  Scenario: 3b Vượt giới hạn kỹ thuật
    Given luồng chính đã tới bước 3
    When Vượt giới hạn kỹ thuật
    Then 429 kèm Retry-After

  Scenario: 3c TTS lỗi
    Given luồng chính đã tới bước 3
    When TTS lỗi
    Then báo lỗi chung, Editor thử lại hoặc nghe mẫu có sẵn

  Scenario: 1a *(Sau MVP)* Giọng chỉ dành cho gói cao hơn (min_plan_code)
    When *(Sau MVP)* Giọng chỉ dành cho gói cao hơn (min_plan_code)
    Then hiện nhãn gói; vẫn nghe thử được, nhưng chọn dùng thì cần nâng cấp
```

#### ST-05-12 Quản lý từ điển phát âm ✂6

| Mục | Nội dung |
|---|---|
| Story | Là **Owner**, tôi muốn quản lý từ điển phát âm |
| Mô tả | Khai báo cách đọc tên riêng, từ mượn, từ Hán Việt; chỉ ảnh hưởng audio, không đổi chữ |
| Use case | [UC-05.12](03-dac-ta-use-case/m05-sinh-tu-lieu.md#uc-0512) · M05 — Sinh tư liệu: storyboard, ảnh, thuyết minh nguyên văn |
| Giai đoạn | P2 ✂6 |
| Truy vết | FR-NAR-04; BR-19. Vị trí ✂6 trong thứ tự cắt giảm (QĐ-05, QĐ-80); seq-thuyet-minh-nguyen-van |
| Story point | |

```gherkin
Feature: UC-05.12 Quản lý từ điển phát âm
  Background:
    Given Là thành viên dự án

  Scenario: Luồng chính
    When Editor thêm mục: từ viết, cách đọc, kiểu (alias / phoneme), phân biệt hoa thường
    And Editor nghe thử (UC-05.11a với câu chứa từ)
    And Hệ thống lưu; liệt kê các shot chứa từ này và gợi ý sinh lại thuyết minh (UC-05.07c)
    Then pronunciation_entries cập nhật; dùng ở lần sinh thuyết minh sau

  Scenario: 1a Vượt 500 mục hoặc trùng từ viết
    When Vượt 500 mục hoặc trùng từ viết
    Then báo lỗi

  Scenario: 1b Giọng của dự án thuộc TTS tự host (MVP, ADR-30)
    When Giọng của dự án thuộc TTS tự host (MVP, ADR-30)
    Then chỉ cho chọn kiểu alias; giao diện gợi ý viết lại cách đọc bằng chữ thay cho phoneme
```

#### ST-05-13 Sinh thuyết minh nguyên văn

| Mục | Nội dung |
|---|---|
| Story | Là **Owner (hoặc UC-05.07)**, tôi muốn sinh thuyết minh nguyên văn |
| Mô tả | Tạo audio đọc đúng từng chữ đoạn nguồn của shot, kèm timestamp từng từ để dựng phụ đề |
| Use case | [UC-05.13](03-dac-ta-use-case/m05-sinh-tu-lieu.md#uc-0513) · M05 — Sinh tư liệu: storyboard, ảnh, thuyết minh nguyên văn |
| Giai đoạn | P2 |
| Truy vết | FR-NAR-02, 03, 06; BR-19, BR-22, BR-34; ADR-12; seq-thuyet-minh-nguyen-van |
| Story point | |

```gherkin
Feature: UC-05.13 Sinh thuyết minh nguyên văn
  Background:
    Given Shot có đoạn nguồn; đã chọn giọng; đủ số dư

  Scenario: Luồng chính
    When Hệ thống giữ tiền theo số ký tự (UC-05.17), tạo job NARRATE_SEGMENT
    And Thực hiện UC-05.13a
    And Thực hiện UC-05.13b
    And Gọi TTS (chia theo câu nếu vượt giới hạn, rồi nối audio); lưu audio
    And Lấy thời gian từng từ trên bản đọc từ TTS nếu provider trả timestamp; nếu không, Aligner chạy forced alignment giữa audio và bản đọc. Ánh xạ về tọa độ chương bằng NormalizationMap theo 12 §2.3 để có word_timings
    And Lưu Narration DONE (phiên bản mới, đặt làm hiện hành, flagged_at rỗng), trừ chi phí thực × 110% và hoàn phần dư, phát narration.updated
    And *(Sau MVP)* Thực hiện UC-05.13c trước bước 6; trạng thái là VERIFIED hoặc NEEDS_REVIEW thay cho DONE
    Then Narration DONE kèm word_timings; cờ "cần sinh lại" (nếu có) được xóa

  Scenario: 2a Hash không khớp
    Given luồng chính đã tới bước 2
    When Hash không khớp
    Then OUTDATED, hoàn tiền, dừng

  Scenario: 4a TTS lỗi hoặc vi phạm chính sách
    Given luồng chính đã tới bước 4
    When TTS lỗi hoặc vi phạm chính sách
    Then retry; vẫn lỗi thì FAILED, hoàn tiền. Văn bản không được tự sửa để vượt bộ lọc (BR-18)

  Scenario: 5a Aligner lỗi sau retry
    Given luồng chính đã tới bước 5
    When Aligner lỗi sau retry
    Then Narration FAILED, hoàn tiền; shot có nút "Sinh lại"
```

#### ST-05-13a Cắt đoạn nguồn & kiểm tra hash

| Mục | Nội dung |
|---|---|
| Story | Là **Hệ thống**, tôi muốn cắt đoạn nguồn & kiểm tra hash |
| Mô tả | Lấy đúng đoạn văn nguồn của shot từ chương và bảo đảm nó chưa bị đổi kể từ khi chia shot |
| Use case | [UC-05.13a](03-dac-ta-use-case/m05-sinh-tu-lieu.md#uc-0513a) · M05 — Sinh tư liệu: storyboard, ảnh, thuyết minh nguyên văn |
| Giai đoạn | P2 |
| Truy vết | BR-19; IC-09; D-05; NFR-INT-02; seq-thuyet-minh-nguyen-van |
| Story point | |

```gherkin
Feature: UC-05.13a Cắt đoạn nguồn & kiểm tra hash
  Background:
    Given Shot có source_start, source_end, source_hash

  Scenario: Luồng chính
    When Hệ thống đọc chapters.content hiện tại của chương
    And Hệ thống cắt text = content[source_start:source_end]
    And Hệ thống tính sha256(text) và so với shots.source_hash
    And Khớp: hệ thống chuyển text cho UC-05.13b
    Then có text đúng bằng đoạn nguồn, sẵn sàng cho UC-05.13b

  Scenario: 4a Không khớp (chương đã đổi sau khi chia shot)
    Given luồng chính đã tới bước 4
    When Không khớp (chương đã đổi sau khi chia shot)
    Then Narration OUTDATED, RELEASE tiền đã giữ, phát narration.updated, dừng (UC-05.13 nhánh 2a)

  Scenario: *a Không có API nào nhận văn bản đọc từ client; use case này là nơi duy nhất hình t
    When Không có API nào nhận văn bản đọc từ client; use case này là nơi duy nhất hình thành text
    Then hệ thống xử lý như mô tả
```

#### ST-05-13b Chuẩn hóa phát âm (SSML)

| Mục | Nội dung |
|---|---|
| Story | Là **Hệ thống (SpeechNormalizer)**, tôi muốn chuẩn hóa phát âm (SSML) |
| Mô tả | Biến đoạn văn nguồn thành SSML để đọc đúng cách (số, ngày, từ mượn) mà không thêm, bớt, đổi hay sắp xếp lại từ nào |
| Use case | [UC-05.13b](03-dac-ta-use-case/m05-sinh-tu-lieu.md#uc-0513b) · M05 — Sinh tư liệu: storyboard, ảnh, thuyết minh nguyên văn |
| Giai đoạn | P2 |
| Truy vết | BR-19; FR-NAR-03, 04; NFR-INT-02; 08 §6; 12 §2.2 (`NormalizationMap`); 04 §3.4 `pronunciation_entries`, `narration_settings.symbol_rules`; seq-thuyet-minh-nguyen-van |
| Story point | |

```gherkin
Feature: UC-05.13b Chuẩn hóa phát âm (SSML)
  Background:
    Given Có text từ UC-05.13a; dự án có narration_settings và từ điển phát âm

  Scenario: Luồng chính
    When Hệ thống áp quy tắc tất định lên bản đọc: các quy tắc ký hiệu SYM-01..05 đang bật của dự án (08 §6: *Bố* đọc "Bố", [Về ăn cơm] đọc "Về ăn cơm", # Hồi 2 đọc "Hồi 2", dòng --- thành khoảng lặng 0,5 s); đọc số, ngày và đơn vị; ngắt nghỉ theo dấu câu với độ dài nghỉ câu và nghỉ đoạn từ narration_settings
    And Hệ thống áp từ điển phát âm bằng SSML alias hoặc phoneme (tôn trọng case_sensitive)
    And Hệ thống ghi normalization_log gồm bản đồ chuẩn hóa NormalizationMap (12 §2.2: các đoạn IDENTITY/DROP/EXPAND/ALIAS/PAUSE nối S với bản đọc) và danh sách quy tắc đã áp
    And Hệ thống kiểm tra ngược: gỡ thẻ SSML và đảo các alias thì phải ra đúng text, chỉ khác ở các biến đổi mức phát âm được phép (BR-19), tức là chỉ thiếu các ký tự ký hiệu đã bỏ theo quy tắc đang bật
    And Hệ thống trả ssml cho bước gọi TTS của UC-05.13
    Then có ssml và normalization_log; text gốc không đổi

  Scenario: 4a Kiểm tra ngược thất bại (có từ bị thêm, bớt hoặc đổi)
    Given luồng chính đã tới bước 4
    When Kiểm tra ngược thất bại (có từ bị thêm, bớt hoặc đổi)
    Then không gọi TTS, Narration FAILED, RELEASE tiền đã giữ, cảnh báo P1 vì đây là lỗi vi phạm bất biến [ĐX]

  Scenario: 2a Mục từ điển lỗi cú pháp phoneme
    Given luồng chính đã tới bước 2
    When Mục từ điển lỗi cú pháp phoneme
    Then bỏ qua mục đó, ghi vào normalization_log và cảnh báo trong kết quả

  Scenario: 2b Giọng thuộc TTS tự host (MVP, ADR-30)
    Given luồng chính đã tới bước 2
    When Giọng thuộc TTS tự host (MVP, ADR-30)
    Then mục PHONEME bị bỏ qua như 2a; SSML vẫn sinh để lưu và kiểm tra ngược, adapter chỉ gửi bản đọc chữ thuần

  Scenario: 1a Đoạn nguồn chỉ gồm dòng phân cách (SYM-05)
    When Đoạn nguồn chỉ gồm dòng phân cách (SYM-05)
    Then không gọi TTS; tạo Narration DONE là khoảng lặng 0,5 s, không có word_timings, không có phụ đề (BR-22)

  Scenario: 1b Quy tắc ký hiệu bị tắt ở dự án
    When Quy tắc ký hiệu bị tắt ở dự án
    Then ký hiệu được giữ trong bản đọc và gửi nguyên cho TTS
```

#### ST-05-18 Nghe & đánh dấu cần sinh lại

| Mục | Nội dung |
|---|---|
| Story | Là **Owner**, tôi muốn nghe & đánh dấu cần sinh lại |
| Mô tả | Kiểm chứng lời đọc thủ công: nghe thuyết minh từng shot, đánh dấu shot đọc sai để sinh lại sau. Không bắt buộc nghe hết mới được xuất video |
| Use case | [UC-05.18](03-dac-ta-use-case/m05-sinh-tu-lieu.md#uc-0518) · M05 — Sinh tư liệu: storyboard, ảnh, thuyết minh nguyên văn |
| Giai đoạn | P2 |
| Truy vết | FR-NAR-08; BR-23, BR-34; API 2.5 `POST/DELETE …/shots/{shid}/narration:flag`; seq-sinh-tu-lieu |
| Story point | |

```gherkin
Feature: UC-05.18 Nghe & đánh dấu cần sinh lại
  Background:
    Given Shot có thuyết minh DONE

  Scenario: Luồng chính
    When Editor bấm "Nghe"; hệ thống phát audio và tô sáng theo word_timings từng từ trên đoạn nguồn
    And Editor nghe thấy đọc sai (bỏ chữ, đọc nhầm tên riêng): bấm "Đánh dấu cần sinh lại"
    And Hệ thống ghi flagged_at, phát narration.updated; shot hiện nhãn "Cần sinh lại"
    And Khi đã đánh dấu xong, Editor chọn "Sinh lại shot đã đánh dấu" (UC-05.07c với phạm vi FLAGGED, hiện giá ước tính) hoặc thêm cách đọc vào từ điển phát âm (UC-05.12) rồi sinh lại
    And Sinh lại thành công thì cờ được xóa (UC-05.13 bước 6)
    Then narrations.flagged_at được đặt hoặc xóa theo lựa chọn

  Scenario: 2a Editor đổi ý
    Given luồng chính đã tới bước 2
    When Editor đổi ý
    Then bấm "Bỏ đánh dấu"; hệ thống xóa flagged_at

  Scenario: 4a Editor không sinh lại
    Given luồng chính đã tới bước 4
    When Editor không sinh lại
    Then vẫn xuất được video; báo cáo điều kiện xuất hiện cảnh báo "N shot được đánh dấu cần sinh lại" (UC-06.16a, BR-34)

  Scenario: *a Thuyết minh chuyển OUTDATED (văn bản hoặc ranh giới shot đổi)
    When Thuyết minh chuyển OUTDATED (văn bản hoặc ranh giới shot đổi)
    Then cờ được xóa khi sinh lại
```

#### ST-09-05 Xem số dư ví

| Mục | Nội dung |
|---|---|
| Story | Là **User**, tôi muốn xem số dư ví |
| Mô tả | Xem số dư khả dụng, phần đang giữ cho job đang chạy, trạng thái tài khoản và phần Free đã dùng trong tháng |
| Use case | [UC-09.05](03-dac-ta-use-case/m09-vi-thanh-toan.md#uc-0905) · M09 — Ví & thanh toán |
| Giai đoạn | P2 |
| Truy vết | FR-BIL-05, FR-BIL-12; BR-27; API 2.8 `GET /me/wallet`; seq-thanh-toan |
| Story point | |

```gherkin
Feature: UC-09.05 Xem số dư ví
  Background:
    Given Đã đăng nhập

  Scenario: Luồng chính
    When User bấm badge số dư
    And Hệ thống hiển thị: số dư khả dụng (USD, 4 chữ số thập phân khi < $1), đang giữ, trạng thái Free / Đã nạp tiền; với Free thêm phần đã dùng trong tháng (số lần render, phút video) và nút "Nạp tiền"
    And Số dư tự cập nhật qua sự kiện wallet.updated khi job giữ, trừ hoặc hoàn tiền
    Then số liệu khớp wallets và sổ cái

  Scenario: 2a Số dư khả dụng dưới giá ước tính của một chương mẫu
    Given luồng chính đã tới bước 2
    When Số dư khả dụng dưới giá ước tính của một chương mẫu
    Then hiện gợi ý nạp thêm
```

#### ST-10-12 Áp trần chi tiêu AI hằng ngày

| Mục | Nội dung |
|---|---|
| Story | Là **Hệ thống (BudgetGuard, Scheduler)**, tôi muốn áp trần chi tiêu AI hằng ngày |
| Mô tả | Giữ tổng chi phí AI thật của toàn hệ thống trong một ngày không vượt trần (closed beta: $10); chạm trần thì tạm dừng job mới và báo Admin |
| Use case | [UC-10.12](03-dac-ta-use-case/m10-quan-tri.md#uc-1012) · M10 — Quản trị |
| Giai đoạn | P2 |
| Truy vết | FR-ADM-07; BR-29; IC-18; ADR-25; QĐ-39; NFR-COST-02; 04 `daily_ai_budgets`; API `503 DAILY_BUDGET_EXCEEDED` |
| Story point | |

```gherkin
Feature: UC-10.12 Áp trần chi tiêu AI hằng ngày
  Background:
    Given system_settings.daily_ai_budget_usd đã cấu hình

  Scenario: Luồng chính
    When Khi có yêu cầu tạo job tốn phí, trong giao dịch của UC-05.17, BudgetGuard tạo dòng daily_ai_budgets của hôm nay nếu chưa có (cap_micro lấy từ system_settings), rồi chạy một câu UPDATE … SET reserved_micro = reserved_micro + x WHERE day = hôm nay AND spent_micro + reserved_micro + x <= cap_micro với x là chi phí provider ước tính
    And Câu lệnh trúng một dòng: chỗ đã được giữ, UC-05.17 tiếp bước 4. Khóa dòng của UPDATE bảo đảm các yêu cầu đồng thời được xếp hàng, không thể cùng vượt trần
    And Khi job kết thúc: reserved −= x, spent += chi phí thực (UC-05.17 bước 5–6)
    And Scheduler mỗi 5 phút đọc dòng của hôm nay; spent + reserved ≥ 80% trần và alert_80_sent_at rỗng thì gửi email cảnh báo sớm và ghi thời điểm; chạm trần thì làm tương tự với alert_100_sent_at
    And Sang ngày mới (00:00 giờ Việt Nam) dùng dòng mới; job tạo hôm trước vẫn trả chỗ vào dòng của ngày tạo (jobs.budget_day)
    And Reconciler hằng ngày đối chiếu spent_micro với Σ ai_usage_records.cost_usd của ngày; lệch thì sửa và cảnh báo
    Then tại mọi thời điểm spent + reserved ≤ cap của ngày (IC-18), kể cả khi nhiều yêu cầu đồng thời; chi phí thực chỉ có thể vượt trần một lượng bằng phần các job đang chạy tốn hơn ước tính; Admin nhận đúng một cảnh báo cho mỗi ngưỡng mỗi ngày

  Scenario: 2a Câu lệnh không trúng dòng nào (vượt trần)
    Given luồng chính đã tới bước 2
    When Câu lệnh không trúng dòng nào (vượt trần)
    Then ROLLBACK, 503 DAILY_BUDGET_EXCEEDED; giao diện hiện "Hệ thống tạm dừng tác vụ AI mới đến 00:00 do đạt giới hạn chi phí trong ngày"; email cho Admin (một lần, theo alert_100_sent_at) kèm tổng chi phí và 5 người dùng chi nhiều nhất

  Scenario: 2b Thao tác miễn phí (render, chỉnh sửa, tải lên)
    Given luồng chính đã tới bước 2
    When Thao tác miễn phí (render, chỉnh sửa, tải lên)
    Then không bị ảnh hưởng

  Scenario: *a Admin nâng trần tạm thời
    When Admin nâng trần tạm thời
    Then sửa daily_ai_budget_usd (seed hoặc CLI); lệnh đồng thời cập nhật cap_micro của dòng hôm nay nên có hiệu lực ngay; ghi audit (UC-10.09)
```

### Giai đoạn P3

#### ST-01-04 Đổi ngôn ngữ giao diện

| Mục | Nội dung |
|---|---|
| Story | Là **User**, tôi muốn đổi ngôn ngữ giao diện |
| Mô tả | Chọn ngôn ngữ giao diện (vi, en) |
| Use case | [UC-01.04](03-dac-ta-use-case/m01-tich-hop-sso.md#uc-0104) · M01 — Tích hợp SSO & hồ sơ |
| Giai đoạn | P3 |
| Truy vết | FR-AUTH-08 |
| Story point | |

```gherkin
Feature: UC-01.04 Đổi ngôn ngữ giao diện
  Background:
    Given Đã đăng nhập (Guest đổi được tạm thời qua cookie)

  Scenario: Luồng chính
    When User mở menu ngôn ngữ và chọn "Tiếng Việt" hoặc "English"
    And Hệ thống lưu locale vào hồ sơ và tải lại chuỗi giao diện
    Then users.locale cập nhật; giao diện hiển thị theo ngôn ngữ mới

  Scenario: *a Lần đăng nhập đầu
    When Lần đăng nhập đầu
    Then mặc định lấy claim locale của SSO nếu có
```

#### ST-02-09 Xem bản đồ quy trình (Map) ✂2

| Mục | Nội dung |
|---|---|
| Story | Là **Owner**, tôi muốn xem bản đồ quy trình (Map) |
| Mô tả | Xem 6 bước của luồng chính và vị trí hiện tại của dự án. Trang tĩnh, đứng thứ hai trong thứ tự cắt giảm, sau nạp tiền sandbox (✂2, QĐ-61, QĐ-116) |
| Use case | [UC-02.09](03-dac-ta-use-case/m02-du-an-cong-tac.md#uc-0209) · M02 — Quản lý dự án & cộng tác |
| Giai đoạn | P3 ✂2 |
| Truy vết | FR-PRJ-06 |
| Story point | |

```gherkin
Feature: UC-02.09 Xem bản đồ quy trình (Map)
  Background:
    Given Là thành viên dự án

  Scenario: Luồng chính
    When Editor mở Map
    And Hệ thống tính trạng thái 6 bước: (1) đã nhập truyện; (2) số chương; (3) số tài sản có ảnh tham chiếu; (4) số chương "Sẵn sàng dựng"; (5) số timeline đã chỉnh; (6) số bản xuất
    And Hệ thống làm nổi bật bước kế tiếp nên làm
    And Editor bấm một bước; hệ thống mở màn hình tương ứng
    Then hiển thị tiến độ từng bước; điều hướng tới bước được chọn
```

#### ST-06-01 Mở trình chỉnh sửa

| Mục | Nội dung |
|---|---|
| Story | Là **Owner**, tôi muốn mở trình chỉnh sửa |
| Mô tả | Mở timeline của một chương để dựng video (timeline cả dự án: sau MVP; cả dự án xuất thẳng ở UC-06.16, QĐ-141) |
| Use case | [UC-06.01](03-dac-ta-use-case/m06-trinh-chinh-sua-video.md#uc-0601) · M06 — Trình chỉnh sửa & xuất video |
| Giai đoạn | P3 |
| Truy vết | FR-EDT-01, 02; seq-chinh-sua-xuat-video |
| Story point | |

```gherkin
Feature: UC-06.01 Mở trình chỉnh sửa
  Background:
    Given Chương (hoặc các chương) có tư liệu

  Scenario: Luồng chính
    When Editor chọn một chương. *(Sau MVP)* phạm vi cả dự án (các chương nối tiếp trên một timeline)
    And Nếu phạm vi chưa có timeline, hệ thống thực hiện UC-06.01a
    And Hệ thống tải tracks + items và hiển thị: vùng preview, thư viện (tư liệu, âm thanh, chuyển cảnh), timeline nhiều track, bảng thuộc tính
    And Nếu tư liệu đã đổi kể từ lần mở trước, hệ thống thực hiện UC-06.15
    Then timeline được tải kèm ETag; preview sẵn sàng

  Scenario: 1a Chương chưa "Sẵn sàng dựng"
    When Chương chưa "Sẵn sàng dựng"
    Then vẫn mở được; clip thiếu ảnh/thuyết minh hiển thị dạng chỗ trống có nút "Sinh tư liệu" (UC-05.07c); không xuất được (UC-06.16a)
```

#### ST-06-01a Dựng bản nháp timeline từ tư liệu

| Mục | Nội dung |
|---|---|
| Story | Là **Hệ thống (TimelineBuilder)**, tôi muốn dựng bản nháp timeline từ tư liệu |
| Mô tả | Tự dựng bản nháp timeline từ ảnh, thuyết minh và phụ đề của các shot, để Editor chỉ phải chỉnh chứ không dựng từ đầu |
| Use case | [UC-06.01a](03-dac-ta-use-case/m06-trinh-chinh-sua-video.md#uc-0601a) · M06 — Trình chỉnh sửa & xuất video |
| Giai đoạn | P3 |
| Truy vết | FR-EDT-01..03; IC-10, IC-12; BR-24, BR-25; API 2.6 `POST /projects/{pid}/timelines`; seq-sinh-tu-lieu, seq-chinh-sua-xuat-video |
| Story point | |

```gherkin
Feature: UC-06.01a Dựng bản nháp timeline từ tư liệu
  Background:
    Given Chương chưa có timeline; mọi shot hiện hành có ảnh DONE và thuyết minh DONE (chương "Sẵn sàng dựng")

  Scenario: Luồng chính
    When Hệ thống tạo timelines với aspect_ratio theo dự án, framing mặc định và subtitle_style mặc định
    And Hệ thống tạo các track: Video, Thuyết minh (khóa, locked = true), Phụ đề, Nhạc nền, SFX (track Overlay sau MVP)
    And Với mỗi shot theo thứ tự: tạo item IMAGE (ảnh hiện hành) và item NARRATION (thuyết minh hiện hành); thời lượng ảnh bằng thời lượng audio cộng đệm 0,3 s / 0,5 s
    And Hệ thống dựng phụ đề từ word_timings và đoạn nguồn gốc, luôn nguyên văn kể cả ký hiệu trình bày; shot chỉ có dòng phân cách tạo khoảng lặng 0,5 s không có phụ đề (BR-22)
    And Hệ thống đặt mặc định Ken Burns luân phiên, chuyển cảnh crossfade 0,5 s
    And *(Sau MVP)* Với dự án nhiều chương: thêm clip tiêu đề chương (UC-06.07) nếu tùy chọn này bật
    And Hệ thống lưu timeline, kiểm tra IC-10 và phát timeline.updated
    Then timeline DRAFT thỏa IC-10, version = 1; nhạc nền và SFX để trống

  Scenario: 0a Phạm vi đã có timeline
    When Phạm vi đã có timeline
    Then POST /timelines trả timeline sẵn có, không dựng lại

  Scenario: 0b Chương chưa "Sẵn sàng dựng"
    When Chương chưa "Sẵn sàng dựng"
    Then 422 PRECONDITION_FAILED_BUSINESS, liệt kê shot còn thiếu [ĐX]

  Scenario: 7a IC-10 không thỏa sau khi dựng (lỗi lập trình)
    Given luồng chính đã tới bước 7
    When IC-10 không thỏa sau khi dựng (lỗi lập trình)
    Then không lưu, cảnh báo P1
```

#### ST-06-02 Thao tác timeline

| Mục | Nội dung |
|---|---|
| Story | Là **Owner**, tôi muốn thao tác timeline |
| Mô tả | Kéo thả, di chuyển, cắt (split), trim, nhân bản, xóa clip; zoom, snap, phím tắt, undo/redo |
| Use case | [UC-06.02](03-dac-ta-use-case/m06-trinh-chinh-sua-video.md#uc-0602) · M06 — Trình chỉnh sửa & xuất video |
| Giai đoạn | P3 |
| Truy vết | FR-EDT-03, 04, 18, 20; ADR-14; seq-chinh-sua-xuat-video |
| Story point | |

```gherkin
Feature: UC-06.02 Thao tác timeline
  Background:
    Given Timeline đang mở

  Scenario: Luồng chính
    When Editor thực hiện thao tác; client áp vào store cục bộ (có thể undo/redo ≥ 100 bước) và cập nhật preview ngay
    And Client kiểm tra sơ bộ UC-06.02a (chặn ngay thao tác cấm trên clip thuyết minh)
    And Sau 1–2 s không thao tác, client gửi lô apply-ops kèm ifMatch
    And Server thực hiện UC-06.02a, ghi items, tăng version, trả ETag mới
    Then thay đổi được lưu tự động (version tăng) và thỏa BR-24

  Scenario: 1a Editor muốn thuyết minh đọc nhanh/chậm hơn
    When Editor muốn thuyết minh đọc nhanh/chậm hơn
    Then không chỉnh trên timeline; giao diện chỉ tới cài đặt tốc độ đọc của dự án (UC-05.11) và sinh lại thuyết minh; timeline cập nhật qua UC-06.15 (QĐ-140)

  Scenario: 4a 422 NARRATION_LOCKED
    Given luồng chính đã tới bước 4
    When 422 NARRATION_LOCKED
    Then client hoàn tác thao tác vi phạm, hiện giải thích

  Scenario: 4b 409 (timeline vừa đổi ở tab khác)
    Given luồng chính đã tới bước 4
    When 409 (timeline vừa đổi ở tab khác)
    Then tải lại timeline (BR-05); sau MVP xử lý theo UC-02.10

  Scenario: *a Mất mạng
    When Mất mạng
    Then lô thao tác giữ trong bộ nhớ, thử lại có backoff; hiện "Chưa lưu"; đóng tab khi chưa lưu thì cảnh báo (không có hàng đợi offline lưu bền, QĐ-137)
```

#### ST-06-02a Kiểm tra khóa thuyết minh

| Mục | Nội dung |
|---|---|
| Story | Là **Hệ thống (NarrationGuard ở client và OpsApplier ở server)**, tôi muốn kiểm tra khóa thuyết minh |
| Mô tả | Bảo vệ track thuyết minh khỏi mọi thao tác làm thay đổi nội dung đọc; một bộ luật dùng chung cho client và server |
| Use case | [UC-06.02a](03-dac-ta-use-case/m06-trinh-chinh-sua-video.md#uc-0602a) · M06 — Trình chỉnh sửa & xuất video |
| Giai đoạn | P3 |
| Truy vết | BR-24, BR-25; IC-10, IC-12; ADR-16; NFR-INT-01; API 2.6 `POST …/timelines/{tlid}:apply-ops`; seq-chinh-sua-xuat-video |
| Story point | |

```gherkin
Feature: UC-06.02a Kiểm tra khóa thuyết minh
  Background:
    Given Có thao tác (hoặc lô thao tác) sắp áp lên timeline

  Scenario: Luồng chính
    When NarrationGuard ở client kiểm tra thao tác bằng bộ luật trong package TypeScript dùng chung (@studio/timeline-rules) trước khi áp vào TimelineStore
    And Thao tác hợp lệ được OpsBatcher gom và gửi apply-ops kèm ifMatch
    And OpsApplier ở server chạy lại cùng bộ luật trên toàn lô
    And Toàn lô hợp lệ: áp dụng nguyên tử, tăng version, phát timeline.updated
    And Có thao tác vi phạm: server từ chối cả lô, trả 422 NARRATION_LOCKED kèm opIndex; client hoàn tác thao tác đó và hiện lý do
    Then timeline luôn thỏa IC-10; độ phủ văn bản không bao giờ giảm

  Scenario: 1a Bị cấm với clip NARRATION
    When Bị cấm với clip NARRATION
    Then cắt, trim, xóa, đổi thứ tự, đổi tốc độ; hai clip chồng nhau

  Scenario: 1b Bị cấm
    When Bị cấm
    Then để clip ảnh của một shot kết thúc trước khi thuyết minh của shot đó đọc xong (BR-25); xóa track Thuyết minh (IC-12)

  Scenario: 1c Được cho phép
    When Được cho phép
    Then dời thời điểm clip thuyết minh (chèn khoảng lặng, kéo theo các clip phía sau); chỉnh âm lượng và keyframe âm lượng (BR-24)

  Scenario: 3a Client và server cho kết quả khác nhau (phiên bản bộ luật lệch)
    Given luồng chính đã tới bước 3
    When Client và server cho kết quả khác nhau (phiên bản bộ luật lệch)
    Then server là chuẩn; client nhận 422 và hiển thị như trên

  Scenario: 4a 409 VERSION_CONFLICT (timeline vừa đổi ở tab khác)
    Given luồng chính đã tới bước 4
    When 409 VERSION_CONFLICT (timeline vừa đổi ở tab khác)
    Then tải lại (BR-05)
```

#### ST-06-03 Quản lý track

| Mục | Nội dung |
|---|---|
| Story | Là **Owner**, tôi muốn quản lý track |
| Mô tả | Thêm, đổi tên, sắp xếp, ẩn, tắt tiếng, solo, xóa track |
| Use case | [UC-06.03](03-dac-ta-use-case/m06-trinh-chinh-sua-video.md#uc-0603) · M06 — Trình chỉnh sửa & xuất video |
| Giai đoạn | P3 |
| Truy vết | FR-EDT-02, 15; seq-chinh-sua-xuat-video |
| Story point | |

```gherkin
Feature: UC-06.03 Quản lý track
  Background:
    Given Timeline đang mở

  Scenario: Luồng chính
    When Editor chọn "Thêm track" (Nhạc nền, SFX; Overlay sau MVP) hoặc thao tác trên track có sẵn
    And Hệ thống áp thay đổi qua UC-06.02
    Then cấu trúc track cập nhật

  Scenario: 1a Xóa track Thuyết minh hoặc Video chính
    When Xóa track Thuyết minh hoặc Video chính
    Then bị chặn

  Scenario: 1b Xóa track có clip
    When Xóa track có clip
    Then yêu cầu xác nhận; có thể hoàn tác
```

#### ST-06-04 Đặt hiệu ứng Ken Burns & điểm tập trung

| Mục | Nội dung |
|---|---|
| Story | Là **Owner**, tôi muốn đặt hiệu ứng Ken Burns & điểm tập trung |
| Mô tả | Đặt chuyển động cho clip ảnh: none, zoom in/out, pan bốn hướng, cường độ, điểm tập trung, nhiều pha; keyframe (nâng cao) sau MVP |
| Use case | [UC-06.04](03-dac-ta-use-case/m06-trinh-chinh-sua-video.md#uc-0604) · M06 — Trình chỉnh sửa & xuất video |
| Giai đoạn | P3 |
| Truy vết | FR-EDT-06; seq-chinh-sua-xuat-video |
| Story point | |

```gherkin
Feature: UC-06.04 Đặt hiệu ứng Ken Burns & điểm tập trung
  Background:
    Given Có clip ảnh

  Scenario: Luồng chính
    When Editor chọn một hoặc nhiều clip ảnh
    And Editor chọn kiểu chuyển động, cường độ, bấm lên ảnh để đặt điểm tập trung
    And Hệ thống lưu qua UC-06.02, đánh dấu user_modified
    Then thuộc tính motion cập nhật; preview phản ánh ngay

  Scenario: 2a Clip dài > 30 s
    Given luồng chính đã tới bước 2
    When Clip dài > 30 s
    Then gợi ý chuyển động nhiều pha, hoặc tách shot trong Storyboard (UC-05.06c)
```

#### ST-06-05 Đặt chuyển cảnh ✂3

| Mục | Nội dung |
|---|---|
| Story | Là **Owner**, tôi muốn đặt chuyển cảnh |
| Mô tả | Đặt kiểu và thời lượng chuyển cảnh giữa hai clip ảnh |
| Use case | [UC-06.05](03-dac-ta-use-case/m06-trinh-chinh-sua-video.md#uc-0605) · M06 — Trình chỉnh sửa & xuất video |
| Giai đoạn | P3 (nâng cao ✂3) |
| Truy vết | FR-EDT-07; BR-25. Chuyển cảnh nâng cao ở vị trí ✂3 trong thứ tự cắt giảm; seq-chinh-sua-xuat-video |
| Story point | |

```gherkin
Feature: UC-06.05 Đặt chuyển cảnh
  Background:
    Given Có ≥ 2 clip ảnh liền kề

  Scenario: Luồng chính
    When Editor kéo kiểu chuyển cảnh vào mối nối: cơ bản cut, crossfade; nâng cao fade, fade-to-black/white, slide, wipe, zoom
    And Editor chỉnh thời lượng (0–1,5 s) hoặc chọn "Áp cho tất cả"
    And Hệ thống lưu qua UC-06.02
    Then transition_in cập nhật; vị trí clip thuyết minh không đổi

  Scenario: 2a Chuyển cảnh làm clip ảnh ngắn hơn khoảng đọc
    Given luồng chính đã tới bước 2
    When Chuyển cảnh làm clip ảnh ngắn hơn khoảng đọc
    Then hệ thống tự kéo dài clip ảnh tương ứng (BR-25)
```

#### ST-06-06 Chọn khung hình & tinh chỉnh màu

| Mục | Nội dung |
|---|---|
| Story | Là **Owner**, tôi muốn chọn khung hình & tinh chỉnh màu |
| Mô tả | Chọn cách khớp ảnh với khung video; chỉnh màu sau MVP (FR-EDT-09, mức C) |
| Use case | [UC-06.06](03-dac-ta-use-case/m06-trinh-chinh-sua-video.md#uc-0606) · M06 — Trình chỉnh sửa & xuất video |
| Giai đoạn | P3 |
| Truy vết | FR-EDT-08, 09; seq-chinh-sua-xuat-video |
| Story point | |

```gherkin
Feature: UC-06.06 Chọn khung hình & tinh chỉnh màu
  Background:
    Given Có clip ảnh

  Scenario: Luồng chính
    When Editor chọn khung hình cho toàn timeline: crop (theo điểm tập trung), fit (viền màu), nền mờ
    And *(Sau MVP)* Editor chỉnh độ sáng, tương phản, bão hòa, nhiệt độ màu hoặc chọn bộ lọc màu; áp cho clip đã chọn hoặc toàn video
    And Hệ thống lưu; preview cập nhật
    Then framing (timeline) và color (clip) cập nhật

  Scenario: *a Editor bật "Vùng an toàn" hoặc "Lưới căn chỉnh" trên preview để đặt phụ đề, over
    When Editor bật "Vùng an toàn" hoặc "Lưới căn chỉnh" trên preview để đặt phụ đề, overlay. Chỉ là lớp hỗ trợ khi chỉnh sửa, không được vẽ vào video xuất
    Then hệ thống xử lý như mô tả
```

#### ST-06-08 Định kiểu phụ đề ✂3

| Mục | Nội dung |
|---|---|
| Story | Là **Owner**, tôi muốn định kiểu phụ đề |
| Mô tả | Bật/tắt và định kiểu phụ đề; nội dung luôn nguyên văn, không sửa được |
| Use case | [UC-06.08](03-dac-ta-use-case/m06-trinh-chinh-sua-video.md#uc-0608) · M06 — Trình chỉnh sửa & xuất video |
| Giai đoạn | P3 (preset ✂3) |
| Truy vết | FR-EDT-11; BR-22. Preset ở vị trí ✂3 trong thứ tự cắt giảm; seq-chinh-sua-xuat-video |
| Story point | |

```gherkin
Feature: UC-06.08 Định kiểu phụ đề
  Background:
    Given Có clip thuyết minh có word_timings

  Scenario: Luồng chính
    When Editor bật phụ đề (kiểu cả câu, ≤ 2 dòng, ≤ 42 ký tự/dòng). Có thể áp một mẫu preset dựng sẵn (hằng số dùng chung, không lưu DB) làm điểm xuất phát; hệ thống chỉ sao chép giá trị vào subtitle_style, nên đổi preset sau này không ảnh hưởng timeline cũ
    And Editor chọn font, cỡ, màu, nền, vị trí trong vùng an toàn theo tỷ lệ khung hình
    And Hệ thống lưu; preview hiển thị phụ đề đồng bộ
    Then subtitle_style cập nhật

  Scenario: *a Editor cố sửa chữ trong phụ đề
    When Editor cố sửa chữ trong phụ đề
    Then bị chặn, hướng dẫn sửa văn bản chương trong Workspace (UC-03.02) rồi sinh lại thuyết minh

  Scenario: *b Phụ đề hiện nguyên ký hiệu trình bày (*Bố*, […]); không có tùy chọn ẩn ký hiệu (
    When Phụ đề hiện nguyên ký hiệu trình bày (*Bố*, […]); không có tùy chọn ẩn ký hiệu (QĐ-56)
    Then hệ thống xử lý như mô tả
```

#### ST-06-09 Thêm nhạc nền

| Mục | Nội dung |
|---|---|
| Story | Là **Owner**, tôi muốn thêm nhạc nền |
| Mô tả | Đặt một hoặc nhiều đoạn nhạc nền, fade, âm lượng, ducking dưới thuyết minh |
| Use case | [UC-06.09](03-dac-ta-use-case/m06-trinh-chinh-sua-video.md#uc-0609) · M06 — Trình chỉnh sửa & xuất video |
| Giai đoạn | P3 |
| Truy vết | FR-EDT-13; BR-25, BR-26; seq-chinh-sua-xuat-video |
| Story point | |

```gherkin
Feature: UC-06.09 Thêm nhạc nền
  Background:
    Given Timeline đang mở

  Scenario: Luồng chính
    When Editor thực hiện UC-06.11 để tìm và nghe thử nhạc
    And Editor kéo bài nhạc vào track Nhạc nền tại vị trí mong muốn
    And Editor cắt, trim, lặp; đặt fade in/out, âm lượng, mức ducking (mặc định −12 dB)
    And Hệ thống lưu qua UC-06.02; preview giảm nhạc khi có lời đọc
    Then item AUDIO trên track Nhạc nền; ducking bắt buộc khi chồng thuyết minh

  Scenario: 3a Nhạc ngắn hơn video
    Given luồng chính đã tới bước 3
    When Nhạc ngắn hơn video
    Then gợi ý "Lặp đến hết" hoặc thêm bài thứ hai với crossfade

  Scenario: 3b Editor tắt ducking khi nhạc chồng thuyết minh
    Given luồng chính đã tới bước 3
    When Editor tắt ducking khi nhạc chồng thuyết minh
    Then bị chặn, mức tối thiểu −6 dB (BR-25)
```

#### ST-06-10 Thêm SFX

| Mục | Nội dung |
|---|---|
| Story | Là **Owner**, tôi muốn thêm SFX |
| Mô tả | Đặt hiệu ứng âm thanh (mưa, bước chân, pháo hoa…) tại thời điểm cụ thể |
| Use case | [UC-06.10](03-dac-ta-use-case/m06-trinh-chinh-sua-video.md#uc-0610) · M06 — Trình chỉnh sửa & xuất video |
| Giai đoạn | P3 |
| Truy vết | FR-EDT-14; seq-chinh-sua-xuat-video |
| Story point | |

```gherkin
Feature: UC-06.10 Thêm SFX
  Background:
    Given Timeline đang mở

  Scenario: Luồng chính
    When Editor thực hiện UC-06.11 (lọc kind = SFX)
    And Editor kéo SFX vào track SFX tại thời điểm mong muốn (snap theo đầu câu nhờ word_timings)
    And Editor trim, fade, chỉnh âm lượng; có thể chồng nhiều SFX trên nhiều track
    And Hệ thống lưu qua UC-06.02
    Then item AUDIO trên track SFX
```

#### ST-06-11 Tìm trong thư viện âm thanh

| Mục | Nội dung |
|---|---|
| Story | Là **Owner**, tôi muốn tìm trong thư viện âm thanh |
| Mô tả | Tìm nhạc nền / SFX trong "Âm thanh của tôi" (file đã tải lên). Thư viện hệ thống CC0/CC-BY: sau MVP |
| Use case | [UC-06.11](03-dac-ta-use-case/m06-trinh-chinh-sua-video.md#uc-0611) · M06 — Trình chỉnh sửa & xuất video |
| Giai đoạn | P3 |
| Truy vết | FR-EDT-12, 27; BR-26; seq-chinh-sua-xuat-video |
| Story point | |

```gherkin
Feature: UC-06.11 Tìm trong thư viện âm thanh
  Background:
    Given Đã đăng nhập

  Scenario: Luồng chính
    When Editor nhập từ khóa (theo tên), chọn loại (Nhạc / SFX)
    And Hệ thống trả kết quả trong âm thanh của tôi kèm waveform, thời lượng. *(Sau MVP)* Thêm nguồn "Thư viện hệ thống" với lọc thể loại, tâm trạng, thời lượng và nhãn license
    And Editor nghe thử và kéo vào timeline
    Then danh sách kết quả, nghe thử được

  Scenario: 2a Không có kết quả phù hợp
    Given luồng chính đã tới bước 2
    When Không có kết quả phù hợp
    Then gợi ý tải lên (UC-06.11a)
```

#### ST-06-11a Tải nhạc / SFX lên

| Mục | Nội dung |
|---|---|
| Story | Là **Owner**, tôi muốn tải nhạc / SFX lên |
| Mô tả | Tải nhạc hoặc SFX của riêng mình lên thư viện cá nhân để dùng trong timeline |
| Use case | [UC-06.11a](03-dac-ta-use-case/m06-trinh-chinh-sua-video.md#uc-0611a) · M06 — Trình chỉnh sửa & xuất video |
| Giai đoạn | P3 |
| Truy vết | FR-EDT-27; BR-26; IC-15; NFR-SEC-10; 08 §5; API 2.6 `POST /audio-assets`; seq-chinh-sua-xuat-video |
| Story point | |

```gherkin
Feature: UC-06.11a Tải nhạc / SFX lên
  Background:
    Given Đã đăng nhập; file là MP3, WAV hoặc M4A

  Scenario: Luồng chính
    When Editor chọn file MP3, WAV hoặc M4A (≤ 100 MB, ≤ 15 phút), chọn loại Nhạc hoặc SFX và nhập tên. Giao diện ghi chú "Bạn tự chịu trách nhiệm bản quyền nội dung tải lên"; không có ô cam kết (BR-26)
    And Hệ thống tải file lên
    And Hệ thống kiểm tra MIME thật, kích thước, quét malware
    And Hệ thống tạo job PROCESS_AUDIO_UPLOAD (Media Processing Worker): đo thời lượng và tạo waveform
    And Xong job, tài sản hiện trong "Âm thanh của tôi", nghe thử và kéo vào timeline được (UC-06.09, UC-06.10). Miễn phí
    Then có audio_assets thuộc âm thanh của tôi (license = USER_UPLOAD, owner_user_id = Editor)

  Scenario: 3a Sai định dạng, MIME không khớp, vượt 100 MB hoặc 15 phút, hoặc phát hiện malware
    Given luồng chính đã tới bước 3
    When Sai định dạng, MIME không khớp, vượt 100 MB hoặc 15 phút, hoặc phát hiện malware
    Then báo lý do cụ thể

  Scenario: 4a File hỏng, không đọc được thời lượng
    Given luồng chính đã tới bước 4
    When File hỏng, không đọc được thời lượng
    Then job FAILED, tài sản không xuất hiện, báo lỗi

  Scenario: *a Chủ sở hữu xóa được tài sản của mình (DELETE /audio-assets/{aid}); tài sản của n
    When Chủ sở hữu xóa được tài sản của mình (DELETE /audio-assets/{aid}); tài sản của người khác không bao giờ xuất hiện trong kết quả tìm kiếm
    Then hệ thống xử lý như mô tả
```

#### ST-06-13 Xem trước ✂9

| Mục | Nội dung |
|---|---|
| Story | Là **Owner**, tôi muốn xem trước |
| Mô tả | Phát video theo thời gian thực trong trình duyệt, không cần render |
| Use case | [UC-06.13](03-dac-ta-use-case/m06-trinh-chinh-sua-video.md#uc-0613) · M06 — Trình chỉnh sửa & xuất video |
| Giai đoạn | P3 ✂9 |
| Truy vết | FR-EDT-17; NFR-PERF-11, 13; ADR-13; seq-chinh-sua-xuat-video |
| Story point | |

```gherkin
Feature: UC-06.13 Xem trước
  Background:
    Given Timeline đang mở

  Scenario: Luồng chính
    When Editor bấm Play hoặc kéo playhead
    And Client dựng khung hình bằng cùng component dùng khi xuất, phát audio đã trộn qua WebAudio
    And Editor dừng tại vị trí cần sửa và chỉnh trực tiếp
    Then hình, thuyết minh, nhạc, SFX, phụ đề đồng bộ (lệch ≤ 100 ms)

  Scenario: 2a Media chưa tải xong
    Given luồng chính đã tới bước 2
    When Media chưa tải xong
    Then hiện khung chờ, ưu tiên tải vùng quanh playhead

  Scenario: 2b Clip thiếu tư liệu
    Given luồng chính đã tới bước 2
    When Clip thiếu tư liệu
    Then hiện khung giữ chỗ và thời lượng ước tính
```

#### ST-06-15 Đồng bộ khi tư liệu thay đổi

| Mục | Nội dung |
|---|---|
| Story | Là **Hệ thống (khi Owner mở trình chỉnh sửa hoặc tư liệu đổi)**, tôi muốn đồng bộ khi tư liệu thay đổi |
| Mô tả | Cập nhật clip khi ảnh/thuyết minh được sinh lại hoặc storyboard thay đổi, giữ chỉnh sửa của người dùng |
| Use case | [UC-06.15](03-dac-ta-use-case/m06-trinh-chinh-sua-video.md#uc-0615) · M06 — Trình chỉnh sửa & xuất video |
| Giai đoạn | P3 |
| Truy vết | FR-EDT-19; BR-33; seq-chinh-sua-xuat-video |
| Story point | |

```gherkin
Feature: UC-06.15 Đồng bộ khi tư liệu thay đổi
  Background:
    Given Có thay đổi tư liệu kể từ phiên bản timeline hiện tại

  Scenario: Luồng chính
    When Hệ thống so tư liệu hiện hành với tham chiếu trong timeline
    And *Ảnh mới:* thay illustration_id, giữ motion/màu/chuyển cảnh
    And *Thuyết minh mới:* thay narration_id, giữ âm lượng Editor đã đặt, cập nhật độ dài; dời các clip phía sau theo độ chênh (nhạc, SFX dời theo nếu gắn với shot)
    And *Storyboard đổi (tách/gộp shot, dời ranh giới shot ở Workspace):* thêm hoặc bớt cặp clip ảnh/thuyết minh tương ứng, đặt hiệu ứng mặc định cho clip mới
    And Hệ thống đánh dấu các clip thay đổi, hiện thông báo "N clip đã cập nhật" để Editor kiểm tra
    Then clip trỏ tới tư liệu mới; IC-10 thỏa; clip bị ảnh hưởng được đánh dấu

  Scenario: 3a SFX đặt trong khoảng thời gian không còn tồn tại
    Given luồng chính đã tới bước 3
    When SFX đặt trong khoảng thời gian không còn tồn tại
    Then chuyển SFX về cuối clip gần nhất và đánh dấu cần xem lại
```

#### ST-06-16 Xuất video MP4

| Mục | Nội dung |
|---|---|
| Story | Là **Owner**, tôi muốn xuất video MP4 |
| Mô tả | Bước 6: render timeline thành MP4 kèm phụ đề |
| Use case | [UC-06.16](03-dac-ta-use-case/m06-trinh-chinh-sua-video.md#uc-0616) · M06 — Trình chỉnh sửa & xuất video |
| Giai đoạn | P3 |
| Truy vết | FR-EDT-21..24, 28; FR-BIL-12; BR-23, BR-27; QĐ-141; API 2.6 `POST /projects/{pid}/renders`; 12 §3 (`timeline_snapshot`, SNP-01..07); seq-chinh-sua-xuat-video |
| Story point | |

```gherkin
Feature: UC-06.16 Xuất video MP4
  Background:
    Given Timeline thỏa UC-06.16a

  Scenario: Luồng chính
    When Editor bấm "Xuất video"
    And Hệ thống thực hiện UC-06.16a và hiện báo cáo độ phủ, thời lượng
    And Editor chọn độ phân giải (720p / 1080p) và xác nhận. Tài khoản Free: chỉ 720p, hộp thoại hiện số lượt render và phút video còn lại trong tháng, và ghi chú video sẽ có watermark (BR-27)
    And Hệ thống chụp timeline_snapshot của phiên bản hiện tại (hợp lệ theo schemas/timeline-snapshot.schema.json và SNP-01..07, 12 §3) và tạo job RENDER_TIMELINE (miễn phí)
    And Render Worker kiểm schema snapshot, dựng khung hình (Ken Burns, chuyển cảnh, phụ đề dựng sẵn trong snapshot; watermark đường kẻ + logo nếu tài khoản Free) trong một lượt Remotion; trộn thuyết minh + nhạc (ducking) + SFX; chuẩn hóa loudness; encode H.264/AAC
    And Tiến độ gửi qua SSE; Editor có thể hủy
    And Hoàn tất: tạo Render READY + SRT/VTT; thông báo "Video đã sẵn sàng" và mở UC-06.17
    Then Render phiên bản mới READY, đặt làm bản chính, có MP4 + SRT/VTT; với tài khoản Free, lượt render và phút video của tháng được cộng

  Scenario: 1b *Xuất cả dự án* (MVP, không qua trình chỉnh sửa, QĐ-141)
    When *Xuất cả dự án* (MVP, không qua trình chỉnh sửa, QĐ-141)
    Then hệ thống lấy timeline của mọi chương theo thứ tự (chương chưa có timeline thì tự dựng bản nháp, UC-06.01a), chạy UC-06.16a cho từng chương và hiện báo cáo gộp (chương nào chưa đạt, tổng thời lượng). Editor chọn độ phân giải và xác nhận như bước 3. Hệ thống ghép snapshot các chương nối tiếp (cắt thẳng giữa hai chương; khung hình, kiểu phụ đề, âm lượng tổng theo chương đầu) thành một snapshot phạm vi PROJECT, tạo một job RENDER_TIMELINE; các bước 5–7 như luồng chính. Giới hạn Free tính theo tổng thời lượng video

  Scenario: 1c Xuất cả dự án khi có chương chưa đạt (chưa "Sẵn sàng dựng", thiếu ảnh, thuyết mi
    When Xuất cả dự án khi có chương chưa đạt (chưa "Sẵn sàng dựng", thiếu ảnh, thuyết minh lỗi hoặc OUTDATED)
    Then 422, liệt kê chương và lý do; Editor xử lý từng chương rồi xuất lại

  Scenario: 2a Chưa đạt điều kiện
    Given luồng chính đã tới bước 2
    When Chưa đạt điều kiện
    Then liệt kê vị trí lỗi trên timeline, có nút nhảy tới

  Scenario: 3a Tài khoản Free hết lượt render hoặc video vượt số phút còn lại trong tháng
    Given luồng chính đã tới bước 3
    When Tài khoản Free hết lượt render hoặc video vượt số phút còn lại trong tháng
    Then 403 FREE_LIMIT_REACHED, gợi ý nạp tiền (UC-09.03) hoặc đợi tháng sau

  Scenario: 3b Tài khoản Free chọn 1080p
    Given luồng chính đã tới bước 3
    When Tài khoản Free chọn 1080p
    Then không cho chọn, ghi chú "1080p khi đã nạp tiền"

  Scenario: 7a Tài khoản vừa nạp tiền sau khi render
    Given luồng chính đã tới bước 7
    When Tài khoản vừa nạp tiền sau khi render
    Then bản cũ giữ watermark; Editor render lại để có bản không watermark

  Scenario: 5a Lỗi encode
    Given luồng chính đã tới bước 5
    When Lỗi encode
    Then retry một lần; vẫn lỗi thì FAILED, hiện mã lỗi

  Scenario: 6a Editor hủy
    Given luồng chính đã tới bước 6
    When Editor hủy
    Then job CANCELLED
```

#### ST-06-16a Kiểm tra điều kiện & độ phủ 100%

| Mục | Nội dung |
|---|---|
| Story | Là **Hệ thống (ReadinessChecker)**, tôi muốn kiểm tra điều kiện & độ phủ 100% |
| Mô tả | Kiểm tra timeline đã đủ điều kiện xuất chưa, nhất là độ phủ văn bản 100%; không bắt buộc người dùng đã nghe hết thuyết minh |
| Use case | [UC-06.16a](03-dac-ta-use-case/m06-trinh-chinh-sua-video.md#uc-0616a) · M06 — Trình chỉnh sửa & xuất video |
| Giai đoạn | P3 |
| Truy vết | BR-11, BR-23, BR-24, BR-27, BR-34; IC-10, IC-11; NFR-INT-01; API 2.6 `GET …/timelines/{tlid}/readiness`; seq-chinh-sua-xuat-video |
| Story point | |

```gherkin
Feature: UC-06.16a Kiểm tra điều kiện & độ phủ 100%
  Background:
    Given Timeline đang mở

  Scenario: Luồng chính
    When Hệ thống kiểm tra mọi shot hiện hành có ảnh DONE
    And Hệ thống kiểm tra mọi shot có thuyết minh DONE (sau MVP: VERIFIED hoặc ACCEPTED), không có OUTDATED
    And Hệ thống kiểm tra timeline thỏa IC-10 và BR-24
    And Hệ thống kiểm tra tổng ký tự các đoạn nguồn có clip thuyết minh bằng tổng ký tự chương (100%)
    And Hệ thống liệt kê cảnh báo không chặn: các shot được đánh dấu cần sinh lại (BR-34); với tài khoản Free thêm lượt render, phút video còn lại và ghi chú watermark
    And Hệ thống trả { coverage: {covered, total}, missingImages[], notDone[], outdated[], violations[], warnings: {flagged[]}, freeQuota? }
    And Giao diện hiển thị kết quả; mục không đạt có vị trí trên timeline và nút nhảy tới
    Then có báo cáo điều kiện; chỉ cho xuất khi mọi mục đạt

  Scenario: 6a Bất kỳ mục điều kiện nào không đạt (bước 1–4)
    Given luồng chính đã tới bước 6
    When Bất kỳ mục điều kiện nào không đạt (bước 1–4)
    Then nút "Xuất" bị vô hiệu hóa; nếu vẫn gọi tạo render thì 422 (IC-11). Cảnh báo ở bước 5 không làm vô hiệu hóa nút

  Scenario: *a Xuất cả dự án (UC-06.16 nhánh 1b)
    When Xuất cả dự án (UC-06.16 nhánh 1b)
    Then kiểm từng chương; độ phủ tính trên tổng ký tự của mọi chương
```

#### ST-06-17 Tải MP4 / SRT / audio

| Mục | Nội dung |
|---|---|
| Story | Là **Owner**, tôi muốn tải MP4 / SRT / audio |
| Mô tả | Tải video và các file kèm theo về máy |
| Use case | [UC-06.17](03-dac-ta-use-case/m06-trinh-chinh-sua-video.md#uc-0617) · M06 — Trình chỉnh sửa & xuất video |
| Giai đoạn | P3 |
| Truy vết | FR-EDT-24, 25; NFR-SEC-05; seq-chinh-sua-xuat-video |
| Story point | |

```gherkin
Feature: UC-06.17 Tải MP4 / SRT / audio
  Background:
    Given Có Render READY

  Scenario: Luồng chính
    When Editor mở danh sách Renders (phiên bản, độ phân giải, thời lượng, ngày, bản chính)
    And Editor chọn file: MP4, SRT, VTT hoặc audio thuyết minh (MP3/WAV)
    And Hệ thống chuyển hướng tới link ký; trình duyệt tải file
    Then file được tải qua link ký có thời hạn 15 phút

  Scenario: 2a Editor đặt một phiên bản khác làm bản chính, hoặc xóa phiên bản (xác nhận)
    Given luồng chính đã tới bước 2
    When Editor đặt một phiên bản khác làm bản chính, hoặc xóa phiên bản (xác nhận)
    Then hệ thống xử lý như mô tả

  Scenario: 3a Link hết hạn
    Given luồng chính đã tới bước 3
    When Link hết hạn
    Then bấm lại để lấy link mới

  Scenario: *a Tài khoản Free
    When Tài khoản Free
    Then video 720p có watermark (08 §3.3)
```

#### ST-09-01 Xem bảng giá

| Mục | Nội dung |
|---|---|
| Story | Là **Guest**, tôi muốn xem bảng giá |
| Mô tả | Xem cách tính giá, đơn giá tham khảo từng thao tác, giới hạn tài khoản Free và quyền lợi khi đã nạp tiền, FAQ |
| Use case | [UC-09.01](03-dac-ta-use-case/m09-vi-thanh-toan.md#uc-0901) · M09 — Ví & thanh toán |
| Giai đoạn | P3 |
| Truy vết | FR-BIL-01; BR-01, BR-27, BR-28; 08 §3; API 2.8 `GET /pricing`; seq-thanh-toan |
| Story point | |

```gherkin
Feature: UC-09.01 Xem bảng giá

  Scenario: Luồng chính
    When Guest mở Pricing
    And Hệ thống hiển thị: nguyên tắc "giá = chi phí thực của nhà cung cấp AI × 110%"; bảng đơn giá tham khảo theo thao tác (storyboard, ảnh, sửa ảnh, thuyết minh theo 1.000 ký tự) lấy từ price_rules và ai_models; ước lượng chi phí cho một chương mẫu 10.000 ký tự; so sánh Free (1 dự án, 3 chương, 3 lần render và 10 phút video mỗi tháng, 720p có watermark) và Đã nạp tiền; tiền dùng thử $2; FAQ
    And Guest bấm "Bắt đầu" hoặc "Nạp tiền"; nếu chưa đăng nhập thì chuyển UC-01.01, sau đó tiếp UC-09.03
    Then hiển thị giá hiện hành từ cấu hình

  Scenario: 2a Người dùng chọn hiển thị VND
    Given luồng chính đã tới bước 2
    When Người dùng chọn hiển thị VND
    Then hệ thống quy đổi theo tỷ giá cấu hình (system_settings.vnd_rate), ghi chú "chỉ để tham khảo; thanh toán bằng USD"
```

#### ST-09-03 Nạp tiền vào ví ✂1

| Mục | Nội dung |
|---|---|
| Story | Là **User**, tôi muốn nạp tiền vào ví |
| Mô tả | Nạp một số tiền USD vào ví để dùng cho các thao tác AI; lần nạp đầu chuyển tài khoản sang "Đã nạp tiền" |
| Use case | [UC-09.03](03-dac-ta-use-case/m09-vi-thanh-toan.md#uc-0903) · M09 — Ví & thanh toán |
| Giai đoạn | P3 ✂1 |
| Truy vết | FR-BIL-03; BR-27; WR-06; API 2.8 `POST /billing/topup-sessions`; seq-thanh-toan |
| Story point | |

```gherkin
Feature: UC-09.03 Nạp tiền vào ví
  Background:
    Given Đã đăng nhập và đã đồng ý xử lý dữ liệu

  Scenario: Luồng chính
    When User chọn số tiền (gợi ý $2, $5, $10 hoặc nhập số khác)
    And Hệ thống thực hiện UC-09.03a
    And UC-09.08 ghi bút toán TOPUP, cộng available_micro và topup_total_micro
    And Hệ thống phát wallet.updated; nếu đây là lần nạp đầu, hiện "Tài khoản đã bỏ giới hạn Free. Video đã render trước đó vẫn có watermark; render lại để có bản không watermark."
    And Nếu User đến từ thông báo thiếu số dư hoặc vượt giới hạn, hệ thống đưa User về đúng thao tác đang dở
    Then wallets.available_micro và topup_total_micro tăng đúng số tiền; sổ cái có bút toán TOPUP; tài khoản ở trạng thái "Đã nạp tiền" (BR-27)

  Scenario: 1a Số tiền ngoài khoảng $1–$100
    When Số tiền ngoài khoảng $1–$100
    Then báo lỗi, không tạo phiên thanh toán [ĐX]
```

#### ST-09-03a Thanh toán qua checkout ✂1

| Mục | Nội dung |
|---|---|
| Story | Là **User**, tôi muốn thanh toán qua checkout |
| Mô tả | Đưa User sang trang thanh toán của cổng để trả tiền; ứng dụng không bao giờ nhận hay lưu thông tin thẻ |
| Use case | [UC-09.03a](03-dac-ta-use-case/m09-vi-thanh-toan.md#uc-0903a) · M09 — Ví & thanh toán |
| Giai đoạn | P3 ✂1 |
| Truy vết | ADR-08; FR-BIL-03; NFR-SEC-07; API 2.8 `POST /billing/topup-sessions`; seq-thanh-toan |
| Story point | |

```gherkin
Feature: UC-09.03a Thanh toán qua checkout
  Background:
    Given Đã đăng nhập; số tiền hợp lệ

  Scenario: Luồng chính
    When Client gọi POST /billing/topup-sessions với {amountUsd}
    And Hệ thống kiểm tra số tiền, tạo (nếu chưa có) khách hàng ở cổng và lưu users.gateway_customer_id
    And Hệ thống tạo payments (kind = TOPUP, status = PENDING) và Checkout Session dạng thanh toán một lần với client_reference_id = userId, metadata.paymentId, số tiền tương ứng, success_url và cancel_url
    And API trả { url }; client chuyển hướng trình duyệt tới trang thanh toán của cổng (môi trường sandbox, dùng thẻ thử)
    And User thanh toán; cổng chuyển về success_url (Dashboard hiện "Đang xử lý thanh toán")
    And Cổng phát webhook; UC-09.08 cộng tiền vào ví
    Then User hoàn tất thanh toán trên cổng và cổng phát webhook cho UC-09.08

  Scenario: 4a Cổng không phản hồi
    Given luồng chính đã tới bước 4
    When Cổng không phản hồi
    Then báo lỗi; payments giữ PENDING rồi hết hạn, không cộng tiền

  Scenario: 5a User hủy
    Given luồng chính đã tới bước 5
    When User hủy
    Then cổng chuyển về cancel_url; không có thay đổi

  Scenario: 5b Thanh toán thất bại tại cổng
    Given luồng chính đã tới bước 5
    When Thanh toán thất bại tại cổng
    Then User ở lại trang của cổng để thử lại

  Scenario: 6a Webhook đến chậm
    Given luồng chính đã tới bước 6
    When Webhook đến chậm
    Then không cộng tiền trước khi webhook xử lý xong
```

#### ST-09-06 Xem lịch sử chi tiêu

| Mục | Nội dung |
|---|---|
| Story | Là **User**, tôi muốn xem lịch sử chi tiêu |
| Mô tả | Xem sổ cái ví, lọc theo dự án và loại thao tác, thấy rõ chi phí thực và phí 10% |
| Use case | [UC-09.06](03-dac-ta-use-case/m09-vi-thanh-toan.md#uc-0906) · M09 — Ví & thanh toán |
| Giai đoạn | P3 |
| Truy vết | FR-BIL-06, 08; API 2.8 `GET /me/wallet/ledger`; seq-thanh-toan |
| Story point | |

```gherkin
Feature: UC-09.06 Xem lịch sử chi tiêu
  Background:
    Given Đã đăng nhập

  Scenario: Luồng chính
    When User mở lịch sử
    And Hệ thống liệt kê bút toán: thời gian, loại (TRIAL_GRANT, TOPUP, HOLD, CAPTURE, RELEASE), số tiền, dự án, thao tác; mỗi job hiển thị một dòng gộp "giữ $x → trừ $y (chi phí thực $z + phí 10%) → hoàn $x−y"
    And User lọc theo dự án, loại thao tác, khoảng thời gian; xem tổng
    Then hiển thị các bút toán (append-only)
```

#### ST-09-08 Xử lý webhook thanh toán ✂1

| Mục | Nội dung |
|---|---|
| Story | Là **Payment Gateway**, tôi muốn xử lý webhook thanh toán |
| Mô tả | Nhận sự kiện thanh toán và cập nhật ví (và gói, sau MVP) một cách idempotent |
| Use case | [UC-09.08](03-dac-ta-use-case/m09-vi-thanh-toan.md#uc-0908) · M09 — Ví & thanh toán |
| Giai đoạn | P3 ✂1 |
| Truy vết | FR-BIL-09; NFR-SEC-07; IC-07; seq-thanh-toan |
| Story point | |

```gherkin
Feature: UC-09.08 Xử lý webhook thanh toán
  Background:
    Given Webhook có chữ ký hợp lệ

  Scenario: Luồng chính
    When Cổng gửi event
    And Hệ thống xác thực chữ ký và timestamp (≤ 5 phút)
    And Hệ thống ghi payment_events (unique gateway_event_id)
    And Event mới: thực hiện UC-09.08a; đánh dấu processed_at
    And Trả 200
    Then mỗi event xử lý đúng một lần

  Scenario: 2a Chữ ký sai
    Given luồng chính đã tới bước 2
    When Chữ ký sai
    Then 400, ghi log bảo mật

  Scenario: 3a Event trùng
    Given luồng chính đã tới bước 3
    When Event trùng
    Then bỏ qua, trả 200

  Scenario: 4a Lỗi xử lý
    Given luồng chính đã tới bước 4
    When Lỗi xử lý
    Then trả 500 để cổng gửi lại; giao dịch DB rollback
```

#### ST-09-08a Ghi nạp tiền vào sổ cái ✂1

| Mục | Nội dung |
|---|---|
| Story | Là **Hệ thống**, tôi muốn ghi nạp tiền vào sổ cái |
| Mô tả | Biến mỗi sự kiện thanh toán thành thay đổi đúng ở payments và ví, với đầy đủ bút toán sổ cái |
| Use case | [UC-09.08a](03-dac-ta-use-case/m09-vi-thanh-toan.md#uc-0908a) · M09 — Ví & thanh toán |
| Giai đoạn | P3 ✂1 |
| Truy vết | FR-BIL-03, FR-BIL-09; WR-01..08; IC-06, IC-07; seq-thanh-toan |
| Story point | |

```gherkin
Feature: UC-09.08a Ghi nạp tiền vào sổ cái
  Background:
    Given Event mới đã qua kiểm tra chữ ký và chống trùng (UC-09.08 bước 2–3)

  Scenario: Luồng chính
    When Hệ thống xác định người dùng và payments từ client_reference_id và metadata.paymentId của event
    And Hệ thống xử lý trong một giao dịch theo loại event (các nhánh 2a–2d)
    And Hệ thống cập nhật wallets và ghi wallet_ledger_entries kèm payment_id cùng giao dịch
    And Hệ thống phát wallet.updated để Dashboard làm mới
    Then payments và ví khớp với cổng; mọi thay đổi số dư có bút toán

  Scenario: 2a checkout.session.completed với payment_status = paid cho nạp tiền
    Given luồng chính đã tới bước 2
    When checkout.session.completed với payment_status = paid cho nạp tiền
    Then payments.status = SUCCEEDED; ghi TOPUP; available_micro += x, topup_total_micro += x (WR-06)

  Scenario: 2b Số tiền trong event khác payments.amount_micro
    Given luồng chính đã tới bước 2
    When Số tiền trong event khác payments.amount_micro
    Then không cộng tiền, ghi cảnh báo P1 để kiểm tra thủ công [ĐX]

  Scenario: 2c Loại event không hỗ trợ
    Given luồng chính đã tới bước 2
    When Loại event không hỗ trợ
    Then chỉ ghi payment_events, không đổi dữ liệu khác, trả 200

  Scenario: 2d *(Sau MVP)* Sự kiện gói (invoice.paid, invoice.payment_failed, customer.subscrip
    Given luồng chính đã tới bước 2
    When *(Sau MVP)* Sự kiện gói (invoice.paid, invoice.payment_failed, customer.subscription.deleted)
    Then cập nhật Subscription theo state-subscription; refund hoặc chargeback ghi REFUND âm, số dư âm thì khóa thao tác tốn phí đến khi bù (WR-07)

  Scenario: *a Lỗi xử lý
    When Lỗi xử lý
    Then rollback; UC-09.08 trả 500 để cổng gửi lại
```

## 3. Epic sau MVP

Mỗi epic một dòng; tách story khi được đưa vào kế hoạch.

| Epic | Phân hệ | Use case | Số UC |
|---|---|---|---|
| EP-01 | M01 — Tích hợp SSO & hồ sơ | UC-01.06 Yêu cầu xóa dữ liệu ứng dụng; UC-01.07 Nhận đăng xuất back-channel | 2 |
| EP-02 | M02 — Quản lý dự án & cộng tác | UC-02.06 Tạo / thu hồi link mời; UC-02.07 Quản lý thành viên; UC-02.08 Tham gia dự án qua link; UC-02.10 Xử lý xung đột khi lưu; UC-02.10a Lưu bản của tôi thành nháp; UC-02.10b Tải bản của người khác; UC-02.11 Nhân bản dự án | 7 |
| EP-03 | M03 — Bản thảo & chương | UC-03.10 Tìm & thay thế; UC-03.10a Xem trước số kết quả; UC-03.11 Lưu Archive; UC-03.12 Xem / sao chép / xóa Archive; UC-03.13 Quản lý ghi chú (Notes); UC-03.13a Gắn ghi chú vào chương / shot; UC-03.14 Xem & khôi phục phiên bản chương | 7 |
| EP-04 | M04 — Thế giới truyện | UC-04.02c Thêm từ thư viện cá nhân; UC-04.11 Xuất ZIP ảnh tài sản | 2 |
| EP-05 | M05 — Sinh tư liệu: storyboard, ảnh, thuyết minh nguyên văn | UC-05.02 Quản lý bản nháp; UC-05.02a Đổi tên / nhân bản / xóa; UC-05.02b So sánh hai bản nháp; UC-05.04 Thiết lập Chapter rules; UC-05.05 Chỉ đạo lại cả chương (Re-direct); UC-05.13c Kiểm chứng lời đọc (WER); UC-05.14 Duyệt shot cần xem lại (NEEDS_REVIEW); UC-05.14a Chấp nhận thủ công; UC-05.15 Gán giọng theo nhân vật; UC-05.16 Tải ZIP ảnh | 10 |
| EP-06 | M06 — Trình chỉnh sửa & xuất video | UC-06.07 Thêm overlay chữ / logo, clip tiêu đề & kết; UC-06.12 Trộn âm & chuẩn hóa loudness; UC-06.14 Xem lịch sử & khôi phục phiên bản timeline; UC-06.16b Chia video thành phần | 4 |
| EP-07 | M07 — AI Director | UC-07.01 Ra lệnh bằng chat; UC-07.01a Hỏi lại khi lệnh mơ hồ; UC-07.01b Xác nhận thao tác tốn phí; UC-07.01c Từ chối sửa / tóm tắt văn bản; UC-07.01d Viết nội dung hộ người dùng; UC-07.02 Chạy chế độ tự động; UC-07.02a Lập & cập nhật kế hoạch bước; UC-07.03 Chọn style (điểm duyệt); UC-07.04 Duyệt cast (điểm duyệt); UC-07.05 Chọn giọng (điểm duyệt); UC-07.06 Duyệt thuyết minh (điểm duyệt); UC-07.07 Tạm dừng / tiếp tục / thoát; UC-07.08 Xem tiến độ & Director note | 13 |
| EP-08 | M08 — Thư viện tài sản cá nhân | UC-08.01 Xem thư viện; UC-08.01a Lọc & tìm kiếm; UC-08.02 Tạo tài sản từ ảnh hoặc mô tả; UC-08.02a Sinh ảnh tham chiếu; UC-08.03 Sửa / xóa tài sản; UC-08.04 Lưu tài sản từ dự án vào thư viện; UC-08.05 Thêm tài sản vào dự án | 7 |
| EP-09 | M09 — Ví & thanh toán | UC-09.02 Đăng ký gói; UC-09.04 Quản lý thanh toán | 2 |
| EP-10 | M10 — Quản trị | UC-10.02 Cấu hình gói đăng ký; UC-10.06 Quản lý thư viện nhạc & SFX có license; UC-10.07 Giám sát job; UC-10.07a Chạy lại job; UC-10.07b Hoàn tiền thủ công; UC-10.08 Điều chỉnh số dư người dùng; UC-10.10 Xem báo cáo | 7 |
