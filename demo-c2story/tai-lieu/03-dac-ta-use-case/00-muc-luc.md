# 03 — Đặc tả Use Case

> Đặc tả đầy đủ **165 use case** của hệ thống: 107 use case gốc và 58 use case con (include/extend), khớp 1–1 với các sơ đồ phân rã trong `../../so-do/01-use-case/phan-ra/`. Mã use case được ghi trên chính sơ đồ.

## 1. Luồng chính của Studio

```
1. Nhập truyện        UC-02.02
2. Chia chương        UC-03.03 → UC-03.09
3. Thế giới truyện    UC-04.01 → UC-04.03
4. Sinh tư liệu       UC-05.07 ⊃ UC-05.01 (storyboard) + UC-05.09 (ảnh) + UC-05.13 (thuyết minh)
5. Chỉnh sửa video    UC-06.01 → UC-06.02 … UC-06.13 (nhạc nền UC-06.09, SFX UC-06.10)
6. Xuất & tải         UC-06.16 → UC-06.17
   Tự động hóa        UC-07.02 (bước 2 → 4 + bản nháp timeline)
```

## 2. Quy ước

| Hạng mục | Quy ước |
|---|---|
| Mã | `UC-<phân hệ>.<số>` cho use case gốc (vd. `UC-05.07`); `UC-<phân hệ>.<số><chữ>` cho use case con (vd. `UC-05.07a`) |
| Định dạng | Use case gốc: mẫu Cockburn "fully-dressed" (§3). Use case con: mẫu rút gọn, đặt ngay sau use case cha |
| Tác nhân | Guest, User, Editor (gồm cả Owner), Owner, Admin; hệ thống ngoài: SSO có sẵn, LLM, Image, TTS, STT/Aligner, Music/SFX Provider, Payment Gateway, Render Worker |
| Đánh số luồng | Luồng chính `1, 2, 3…`; nhánh thay thế/ngoại lệ `3a`, `3a1`; nhánh áp dụng mọi bước `*a` |
| Mức độ | Mọi use case gốc đều ở mức *mục tiêu người dùng* (user goal) trừ khi ghi khác (*tóm tắt* / *chức năng con*) |
| Truy vết | Mỗi use case ghi FR (02), BR (08) và sơ đồ liên quan |

## 3. Mẫu đặc tả

**Use case gốc**

| Mục | Nội dung |
|---|---|
| Tác nhân chính / phụ | Ai khởi động / hệ thống nào tham gia |
| Mô tả | Mục tiêu của use case |
| Tiền điều kiện | Điều phải đúng trước khi bắt đầu |
| Hậu điều kiện | **Thành công:** trạng thái khi đạt mục tiêu. **Tối thiểu:** điều luôn được bảo đảm kể cả khi thất bại |
| Kích hoạt | Sự kiện bắt đầu |
| Quan hệ | include / extend |
| Truy vết | FR, BR, sơ đồ |

Sau bảng là **Luồng chính** và **Luồng thay thế / ngoại lệ**.

**Use case con:** Loại (include/extend) · Điều kiện kích hoạt hoặc điểm mở rộng · Các bước · Kết quả.

## 4. Ánh xạ mã cũ (bản 1.5 trở về trước) → mã mới

| Mã cũ | Mã mới | | Mã cũ | Mã mới |
|---|---|---|---|---|
| UC-01 | UC-01.01, UC-01.02 | | UC-10 | UC-05.09, UC-05.10 |
| UC-02 | UC-02.02 | | UC-11 | UC-05.07 |
| UC-03 | UC-02.06, UC-02.08 | | UC-12 | UC-05.13 |
| UC-04 | UC-02.10 | | UC-13 | UC-06.01 – UC-06.15 |
| UC-05 | UC-03.03 – UC-03.09 | | UC-14 | UC-06.16, UC-06.17 |
| UC-06 | UC-03.11, UC-03.12 | | UC-15 | UC-07.02 |
| UC-07 | UC-04.01 – UC-04.03 | | UC-16 | UC-07.01 |
| UC-08 | UC-04.10 | | UC-17 | UC-09.02, UC-09.03 |
| UC-09 | UC-05.01 – UC-05.06 | | | |

## 5. Danh mục use case

### M01 — Tích hợp SSO & hồ sơ ([m01-tich-hop-sso.md](m01-tich-hop-sso.md))

| Mã | Use case | Loại |
|---|---|---|
| [UC-01.01](m01-tich-hop-sso.md#uc-0101) | Đăng nhập qua SSO | Gốc |
| [UC-01.01a](m01-tich-hop-sso.md#uc-0101a) | Xác thực ID token (JWKS, state, nonce, PKCE) | Con (include/extend) |
| [UC-01.01b](m01-tich-hop-sso.md#uc-0101b) | Tạo / đồng bộ hồ sơ cục bộ (JIT theo sub) | Con (include/extend) |
| [UC-01.01c](m01-tich-hop-sso.md#uc-0101c) | Quay về trang đã yêu cầu | Con (include/extend) |
| [UC-01.02](m01-tich-hop-sso.md#uc-0102) | Đăng xuất | Gốc |
| [UC-01.02a](m01-tich-hop-sso.md#uc-0102a) | Kết thúc phiên SSO (RP-initiated logout) | Con (include/extend) |
| [UC-01.03](m01-tich-hop-sso.md#uc-0103) | Xem Dashboard | Gốc |
| [UC-01.04](m01-tich-hop-sso.md#uc-0104) | Đổi ngôn ngữ giao diện | Gốc |
| [UC-01.05](m01-tich-hop-sso.md#uc-0105) | Mở trang quản lý tài khoản SSO | Gốc |
| [UC-01.06](m01-tich-hop-sso.md#uc-0106) | Yêu cầu xóa dữ liệu ứng dụng | Gốc |
| [UC-01.07](m01-tich-hop-sso.md#uc-0107) | Nhận đăng xuất back-channel | Gốc |

### M02 — Quản lý dự án & cộng tác ([m02-du-an-cong-tac.md](m02-du-an-cong-tac.md))

| Mã | Use case | Loại |
|---|---|---|
| [UC-02.01](m02-du-an-cong-tac.md#uc-0201) | Xem danh sách dự án | Gốc |
| [UC-02.02](m02-du-an-cong-tac.md#uc-0202) | Import truyện (giữ nguyên văn) | Gốc |
| [UC-02.02a](m02-du-an-cong-tac.md#uc-0202a) | Kiểm tra & chuẩn hóa kỹ thuật (NFC, xuống dòng) | Con (include/extend) |
| [UC-02.03](m02-du-an-cong-tac.md#uc-0203) | Tạo dự án trống | Gốc |
| [UC-02.04](m02-du-an-cong-tac.md#uc-0204) | Cài đặt dự án (style, model, ngôn ngữ, thời lượng mỗi ảnh, tỷ lệ khung hình) | Gốc |
| [UC-02.05](m02-du-an-cong-tac.md#uc-0205) | Xóa dự án | Gốc |
| [UC-02.06](m02-du-an-cong-tac.md#uc-0206) | Tạo / thu hồi link mời | Gốc |
| [UC-02.07](m02-du-an-cong-tac.md#uc-0207) | Quản lý thành viên | Gốc |
| [UC-02.08](m02-du-an-cong-tac.md#uc-0208) | Tham gia dự án qua link | Gốc |
| [UC-02.09](m02-du-an-cong-tac.md#uc-0209) | Xem bản đồ quy trình (Map) | Gốc |
| [UC-02.10](m02-du-an-cong-tac.md#uc-0210) | Xử lý xung đột khi lưu | Gốc |
| [UC-02.10a](m02-du-an-cong-tac.md#uc-0210a) | Lưu bản của tôi thành nháp | Con (include/extend) |
| [UC-02.10b](m02-du-an-cong-tac.md#uc-0210b) | Tải bản của người khác | Con (include/extend) |
| [UC-02.11](m02-du-an-cong-tac.md#uc-0211) | Nhân bản dự án | Gốc |

### M03 — Bản thảo & chương ([m03-ban-thao-chuong.md](m03-ban-thao-chuong.md))

| Mã | Use case | Loại |
|---|---|---|
| [UC-03.01](m03-ban-thao-chuong.md#uc-0301) | Xem văn bản gốc | Gốc |
| [UC-03.01a](m03-ban-thao-chuong.md#uc-0301a) | Sao chép toàn văn | Con (include/extend) |
| [UC-03.01b](m03-ban-thao-chuong.md#uc-0301b) | Nhập lại (Re-import) | Con (include/extend) |
| [UC-03.02](m03-ban-thao-chuong.md#uc-0302) | Soạn thảo trong Workspace | Gốc |
| [UC-03.03](m03-ban-thao-chuong.md#uc-0303) | Gợi ý chia chương bằng AI | Gốc |
| [UC-03.04](m03-ban-thao-chuong.md#uc-0304) | Chia chương tại vị trí | Gốc |
| [UC-03.05](m03-ban-thao-chuong.md#uc-0305) | Gộp chương vào chương trước | Gốc |
| [UC-03.06](m03-ban-thao-chuong.md#uc-0306) | Dời ranh giới chương | Gốc |
| [UC-03.07](m03-ban-thao-chuong.md#uc-0307) | Thêm / xóa / đổi tên chương | Gốc |
| [UC-03.08](m03-ban-thao-chuong.md#uc-0308) | Sắp xếp lại chương | Gốc |
| [UC-03.09](m03-ban-thao-chuong.md#uc-0309) | Tái cấu trúc nguyên tử (kiểm tra version, OUTDATED tư liệu) | Gốc |
| [UC-03.10](m03-ban-thao-chuong.md#uc-0310) | Tìm & thay thế | Gốc |
| [UC-03.10a](m03-ban-thao-chuong.md#uc-0310a) | Xem trước số kết quả | Con (include/extend) |
| [UC-03.11](m03-ban-thao-chuong.md#uc-0311) | Lưu Archive | Gốc |
| [UC-03.12](m03-ban-thao-chuong.md#uc-0312) | Xem / sao chép / xóa Archive | Gốc |
| [UC-03.13](m03-ban-thao-chuong.md#uc-0313) | Ghi chú (Notes) | Gốc |
| [UC-03.13a](m03-ban-thao-chuong.md#uc-0313a) | Gắn ghi chú vào chương / shot | Con (include/extend) |
| [UC-03.14](m03-ban-thao-chuong.md#uc-0314) | Xem & khôi phục phiên bản chương | Gốc |

### M04 — Thế giới truyện ([m04-the-gioi-truyen.md](m04-the-gioi-truyen.md))

| Mã | Use case | Loại |
|---|---|---|
| [UC-04.01](m04-the-gioi-truyen.md#uc-0401) | Phân tích tài sản bằng AI | Gốc |
| [UC-04.01a](m04-the-gioi-truyen.md#uc-0401a) | Duyệt tài sản đề xuất | Con (include/extend) |
| [UC-04.02](m04-the-gioi-truyen.md#uc-0402) | Quản lý Story Assets | Gốc |
| [UC-04.02a](m04-the-gioi-truyen.md#uc-0402a) | Tạo nhân vật / địa điểm / đạo cụ | Con (include/extend) |
| [UC-04.02b](m04-the-gioi-truyen.md#uc-0402b) | Tạo nhóm nhân vật | Con (include/extend) |
| [UC-04.02c](m04-the-gioi-truyen.md#uc-0402c) | Thêm từ thư viện cá nhân | Con (include/extend) |
| [UC-04.02d](m04-the-gioi-truyen.md#uc-0402d) | Gỡ khỏi dự án | Con (include/extend) |
| [UC-04.02e](m04-the-gioi-truyen.md#uc-0402e) | Quản lý bí danh & facts | Con (include/extend) |
| [UC-04.03](m04-the-gioi-truyen.md#uc-0403) | Sinh ảnh tham chiếu | Gốc |
| [UC-04.03a](m04-the-gioi-truyen.md#uc-0403a) | Sinh lại tất cả (Regenerate all) | Con (include/extend) |
| [UC-04.04](m04-the-gioi-truyen.md#uc-0404) | Dùng ảnh tải lên nguyên bản | Gốc |
| [UC-04.05](m04-the-gioi-truyen.md#uc-0405) | Chọn style dự án | Gốc |
| [UC-04.06](m04-the-gioi-truyen.md#uc-0406) | Thiết lập Art Direction | Gốc |
| [UC-04.07](m04-the-gioi-truyen.md#uc-0407) | Xem dòng thời gian truyện | Gốc |
| [UC-04.08](m04-the-gioi-truyen.md#uc-0408) | Xem đồ thị quan hệ | Gốc |
| [UC-04.09](m04-the-gioi-truyen.md#uc-0409) | Phân tích lại (Re-analyse) | Gốc |
| [UC-04.10](m04-the-gioi-truyen.md#uc-0410) | Quản lý Visual Rules | Gốc |
| [UC-04.11](m04-the-gioi-truyen.md#uc-0411) | Xuất ZIP ảnh tài sản | Gốc |

### M05 — Sinh tư liệu (storyboard, ảnh, thuyết minh) ([m05-sinh-tu-lieu.md](m05-sinh-tu-lieu.md))

| Mã | Use case | Loại |
|---|---|---|
| [UC-05.01](m05-sinh-tu-lieu.md#uc-0501) | Tạo bản nháp storyboard | Gốc |
| [UC-05.01a](m05-sinh-tu-lieu.md#uc-0501a) | Tách câu & kiểm tra phủ kín (CoverageValidator) | Con (include/extend) |
| [UC-05.02](m05-sinh-tu-lieu.md#uc-0502) | Quản lý bản nháp | Gốc |
| [UC-05.02a](m05-sinh-tu-lieu.md#uc-0502a) | Đổi tên / nhân bản / xóa | Con (include/extend) |
| [UC-05.02b](m05-sinh-tu-lieu.md#uc-0502b) | So sánh hai bản nháp | Con (include/extend) |
| [UC-05.02c](m05-sinh-tu-lieu.md#uc-0502c) | Đặt bản nháp hiện hành | Con (include/extend) |
| [UC-05.03](m05-sinh-tu-lieu.md#uc-0503) | Chia lại shot (nhiều / ít hơn) | Gốc |
| [UC-05.04](m05-sinh-tu-lieu.md#uc-0504) | Thiết lập Chapter rules | Gốc |
| [UC-05.05](m05-sinh-tu-lieu.md#uc-0505) | Chỉ đạo lại cả chương (Re-direct) | Gốc |
| [UC-05.06](m05-sinh-tu-lieu.md#uc-0506) | Biên tập shot | Gốc |
| [UC-05.06a](m05-sinh-tu-lieu.md#uc-0506a) | Sửa brief, thời điểm, caption | Con (include/extend) |
| [UC-05.06b](m05-sinh-tu-lieu.md#uc-0506b) | Gắn cast / item / location | Con (include/extend) |
| [UC-05.06c](m05-sinh-tu-lieu.md#uc-0506c) | Tách / gộp / xóa shot | Con (include/extend) |
| [UC-05.06d](m05-sinh-tu-lieu.md#uc-0506d) | Dời ranh giới đoạn nguồn | Con (include/extend) |
| [UC-05.06e](m05-sinh-tu-lieu.md#uc-0506e) | AI viết lại brief một shot | Con (include/extend) |
| [UC-05.06f](m05-sinh-tu-lieu.md#uc-0506f) | Tự khớp tên với tài sản | Con (include/extend) |
| [UC-05.07](m05-sinh-tu-lieu.md#uc-0507) | Sinh tư liệu chương (một báo giá tổng) | Gốc |
| [UC-05.07a](m05-sinh-tu-lieu.md#uc-0507a) | Storyboard tự động (M05a) | Con (include/extend) |
| [UC-05.07b](m05-sinh-tu-lieu.md#uc-0507b) | Xem tiến độ theo shot | Con (include/extend) |
| [UC-05.07c](m05-sinh-tu-lieu.md#uc-0507c) | Sinh lại phần thiếu / lỗi | Con (include/extend) |
| [UC-05.08](m05-sinh-tu-lieu.md#uc-0508) | Xem Tư liệu dự án (media bin) | Gốc |
| [UC-05.09](m05-sinh-tu-lieu.md#uc-0509) | Sinh ảnh shot | Gốc |
| [UC-05.10](m05-sinh-tu-lieu.md#uc-0510) | Sửa ảnh | Gốc |
| [UC-05.10a](m05-sinh-tu-lieu.md#uc-0510a) | Describe → Edit | Con (include/extend) |
| [UC-05.10b](m05-sinh-tu-lieu.md#uc-0510b) | Fix a spot (tô vùng) | Con (include/extend) |
| [UC-05.10c](m05-sinh-tu-lieu.md#uc-0510c) | Khôi phục phiên bản ảnh | Con (include/extend) |
| [UC-05.11](m05-sinh-tu-lieu.md#uc-0511) | Cài đặt thuyết minh (giọng, tốc độ, ngắt nghỉ) | Gốc |
| [UC-05.11a](m05-sinh-tu-lieu.md#uc-0511a) | Nghe thử giọng | Con (include/extend) |
| [UC-05.12](m05-sinh-tu-lieu.md#uc-0512) | Quản lý từ điển phát âm | Gốc |
| [UC-05.13](m05-sinh-tu-lieu.md#uc-0513) | Sinh thuyết minh nguyên văn | Gốc |
| [UC-05.13a](m05-sinh-tu-lieu.md#uc-0513a) | Cắt đoạn nguồn & kiểm tra hash | Con (include/extend) |
| [UC-05.13b](m05-sinh-tu-lieu.md#uc-0513b) | Chuẩn hóa phát âm (SSML) | Con (include/extend) |
| [UC-05.13c](m05-sinh-tu-lieu.md#uc-0513c) | Kiểm chứng lời đọc (WER) | Con (include/extend) |
| [UC-05.14](m05-sinh-tu-lieu.md#uc-0514) | Duyệt shot NEEDS_REVIEW | Gốc |
| [UC-05.14a](m05-sinh-tu-lieu.md#uc-0514a) | Chấp nhận thủ công | Con (include/extend) |
| [UC-05.15](m05-sinh-tu-lieu.md#uc-0515) | Gán giọng theo nhân vật | Gốc |
| [UC-05.16](m05-sinh-tu-lieu.md#uc-0516) | Tải ZIP ảnh | Gốc |
| [UC-05.17](m05-sinh-tu-lieu.md#uc-0517) | Giữ / trừ / hoàn credit | Gốc |

### M06 — Trình chỉnh sửa & xuất video ([m06-trinh-chinh-sua-video.md](m06-trinh-chinh-sua-video.md))

| Mã | Use case | Loại |
|---|---|---|
| [UC-06.01](m06-trinh-chinh-sua-video.md#uc-0601) | Mở trình chỉnh sửa (chương / cả dự án) | Gốc |
| [UC-06.01a](m06-trinh-chinh-sua-video.md#uc-0601a) | Dựng bản nháp timeline từ tư liệu | Con (include/extend) |
| [UC-06.02](m06-trinh-chinh-sua-video.md#uc-0602) | Thao tác timeline (kéo thả, cắt, trim, undo/redo) | Gốc |
| [UC-06.02a](m06-trinh-chinh-sua-video.md#uc-0602a) | Kiểm tra khóa thuyết minh (BR-24) | Con (include/extend) |
| [UC-06.03](m06-trinh-chinh-sua-video.md#uc-0603) | Quản lý track (thêm, ẩn, tắt tiếng) | Gốc |
| [UC-06.04](m06-trinh-chinh-sua-video.md#uc-0604) | Hiệu ứng Ken Burns & điểm tập trung | Gốc |
| [UC-06.05](m06-trinh-chinh-sua-video.md#uc-0605) | Chuyển cảnh | Gốc |
| [UC-06.06](m06-trinh-chinh-sua-video.md#uc-0606) | Khung hình & tinh chỉnh màu | Gốc |
| [UC-06.07](m06-trinh-chinh-sua-video.md#uc-0607) | Overlay chữ / logo, clip tiêu đề & kết | Gốc |
| [UC-06.08](m06-trinh-chinh-sua-video.md#uc-0608) | Kiểu phụ đề (nội dung nguyên văn) | Gốc |
| [UC-06.09](m06-trinh-chinh-sua-video.md#uc-0609) | Thêm nhạc nền (fade, ducking) | Gốc |
| [UC-06.10](m06-trinh-chinh-sua-video.md#uc-0610) | Thêm SFX | Gốc |
| [UC-06.11](m06-trinh-chinh-sua-video.md#uc-0611) | Tìm trong thư viện âm thanh | Gốc |
| [UC-06.11a](m06-trinh-chinh-sua-video.md#uc-0611a) | Tải nhạc / SFX lên | Con (include/extend) |
| [UC-06.11b](m06-trinh-chinh-sua-video.md#uc-0611b) | Sinh nhạc / SFX bằng AI | Con (include/extend) |
| [UC-06.11c](m06-trinh-chinh-sua-video.md#uc-0611c) | Gợi ý SFX theo đoạn văn | Con (include/extend) |
| [UC-06.12](m06-trinh-chinh-sua-video.md#uc-0612) | Trộn âm & chuẩn hóa loudness | Gốc |
| [UC-06.13](m06-trinh-chinh-sua-video.md#uc-0613) | Xem trước | Gốc |
| [UC-06.14](m06-trinh-chinh-sua-video.md#uc-0614) | Lịch sử phiên bản & khôi phục | Gốc |
| [UC-06.15](m06-trinh-chinh-sua-video.md#uc-0615) | Đồng bộ khi tư liệu thay đổi | Gốc |
| [UC-06.16](m06-trinh-chinh-sua-video.md#uc-0616) | Xuất video MP4 | Gốc |
| [UC-06.16a](m06-trinh-chinh-sua-video.md#uc-0616a) | Kiểm tra điều kiện & độ phủ 100% | Con (include/extend) |
| [UC-06.16b](m06-trinh-chinh-sua-video.md#uc-0616b) | Chia video thành phần | Con (include/extend) |
| [UC-06.17](m06-trinh-chinh-sua-video.md#uc-0617) | Tải MP4 / SRT / audio | Gốc |

### M07 — AI Director ([m07-ai-director.md](m07-ai-director.md))

| Mã | Use case | Loại |
|---|---|---|
| [UC-07.01](m07-ai-director.md#uc-0701) | Ra lệnh bằng chat | Gốc |
| [UC-07.01a](m07-ai-director.md#uc-0701a) | Hỏi lại khi lệnh mơ hồ | Con (include/extend) |
| [UC-07.01b](m07-ai-director.md#uc-0701b) | Xác nhận thao tác tốn phí | Con (include/extend) |
| [UC-07.01c](m07-ai-director.md#uc-0701c) | Từ chối sửa / tóm tắt văn bản (BR-19, BR-21) | Con (include/extend) |
| [UC-07.01d](m07-ai-director.md#uc-0701d) | Director viết nội dung hộ (prompt, caption, Visual Rule) | Con (include/extend) |
| [UC-07.02](m07-ai-director.md#uc-0702) | Chạy chế độ tự động (đến bản nháp timeline) | Gốc |
| [UC-07.02a](m07-ai-director.md#uc-0702a) | Lập & cập nhật kế hoạch bước | Con (include/extend) |
| [UC-07.03](m07-ai-director.md#uc-0703) | Chọn style (điểm duyệt) | Gốc |
| [UC-07.04](m07-ai-director.md#uc-0704) | Duyệt cast (điểm duyệt) | Gốc |
| [UC-07.05](m07-ai-director.md#uc-0705) | Chọn giọng (điểm duyệt) | Gốc |
| [UC-07.06](m07-ai-director.md#uc-0706) | Duyệt thuyết minh (điểm duyệt) | Gốc |
| [UC-07.07](m07-ai-director.md#uc-0707) | Tạm dừng / tiếp tục / thoát | Gốc |
| [UC-07.08](m07-ai-director.md#uc-0708) | Xem tiến độ & Director note | Gốc |

### M08 — Thư viện tài sản cá nhân ([m08-thu-vien-tai-san.md](m08-thu-vien-tai-san.md))

| Mã | Use case | Loại |
|---|---|---|
| [UC-08.01](m08-thu-vien-tai-san.md#uc-0801) | Xem thư viện (Characters / Locations / Items) | Gốc |
| [UC-08.01a](m08-thu-vien-tai-san.md#uc-0801a) | Lọc & tìm kiếm (All / My Created / From Projects) | Con (include/extend) |
| [UC-08.02](m08-thu-vien-tai-san.md#uc-0802) | Tạo tài sản từ ảnh hoặc mô tả | Gốc |
| [UC-08.02a](m08-thu-vien-tai-san.md#uc-0802a) | Sinh ảnh tham chiếu | Con (include/extend) |
| [UC-08.03](m08-thu-vien-tai-san.md#uc-0803) | Sửa / xóa tài sản | Gốc |
| [UC-08.04](m08-thu-vien-tai-san.md#uc-0804) | Lưu tài sản từ dự án vào thư viện | Gốc |
| [UC-08.05](m08-thu-vien-tai-san.md#uc-0805) | Thêm tài sản vào dự án | Gốc |

### M09 — Credit & thanh toán ([m09-credit-thanh-toan.md](m09-credit-thanh-toan.md))

| Mã | Use case | Loại |
|---|---|---|
| [UC-09.01](m09-credit-thanh-toan.md#uc-0901) | Xem bảng giá (Monthly / Annual / Packs) | Gốc |
| [UC-09.02](m09-credit-thanh-toan.md#uc-0902) | Đăng ký gói | Gốc |
| [UC-09.03](m09-credit-thanh-toan.md#uc-0903) | Mua gói credit | Gốc |
| [UC-09.03a](m09-credit-thanh-toan.md#uc-0903a) | Thanh toán qua checkout | Con (include/extend) |
| [UC-09.04](m09-credit-thanh-toan.md#uc-0904) | Quản lý thanh toán (đổi gói, thẻ, hóa đơn, hủy) | Gốc |
| [UC-09.05](m09-credit-thanh-toan.md#uc-0905) | Xem số dư credit | Gốc |
| [UC-09.06](m09-credit-thanh-toan.md#uc-0906) | Xem lịch sử tiêu credit | Gốc |
| [UC-09.07](m09-credit-thanh-toan.md#uc-0907) | Nhận credit hằng ngày | Gốc |
| [UC-09.08](m09-credit-thanh-toan.md#uc-0908) | Xử lý webhook thanh toán (idempotent) | Gốc |
| [UC-09.08a](m09-credit-thanh-toan.md#uc-0908a) | Cập nhật gói & nạp credit (ledger) | Con (include/extend) |

### M10 — Quản trị ([m10-quan-tri.md](m10-quan-tri.md))

| Mã | Use case | Loại |
|---|---|---|
| [UC-10.01](m10-quan-tri.md#uc-1001) | Cấu hình bảng giá credit | Gốc |
| [UC-10.02](m10-quan-tri.md#uc-1002) | Cấu hình gói & credit pack | Gốc |
| [UC-10.03](m10-quan-tri.md#uc-1003) | Quản lý provider & mô hình AI | Gốc |
| [UC-10.04](m10-quan-tri.md#uc-1004) | Quản lý danh mục style | Gốc |
| [UC-10.05](m10-quan-tri.md#uc-1005) | Quản lý danh mục giọng đọc | Gốc |
| [UC-10.06](m10-quan-tri.md#uc-1006) | Quản lý thư viện nhạc & SFX có license | Gốc |
| [UC-10.07](m10-quan-tri.md#uc-1007) | Giám sát job | Gốc |
| [UC-10.07a](m10-quan-tri.md#uc-1007a) | Chạy lại job | Con (include/extend) |
| [UC-10.07b](m10-quan-tri.md#uc-1007b) | Hoàn credit thủ công | Con (include/extend) |
| [UC-10.08](m10-quan-tri.md#uc-1008) | Điều chỉnh credit người dùng | Gốc |
| [UC-10.09](m10-quan-tri.md#uc-1009) | Ghi audit log | Gốc |
| [UC-10.10](m10-quan-tri.md#uc-1010) | Xem báo cáo (credit, chi phí AI, biên lợi nhuận) | Gốc |
