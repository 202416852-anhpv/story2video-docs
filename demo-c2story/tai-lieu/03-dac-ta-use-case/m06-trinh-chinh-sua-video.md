# M06 — Trình chỉnh sửa & xuất video

> Bước 5–6 của luồng chính. Nhạc nền và SFX được thêm **tại đây**. Track thuyết minh bị khóa nội dung (BR-24).
> Sơ đồ: `../../so-do/01-use-case/phan-ra/uc-m06-trinh-chinh-sua-video.puml`, `../../so-do/04-tuan-tu/seq-chinh-sua-xuat-video.puml`, `../../so-do/06-trang-thai/state-narration-render.puml`.
> Yêu cầu: FR-EDT-01..26. Quy tắc: BR-22..BR-26. Mọi thao tác chỉnh sửa miễn phí, trừ AI âm thanh (UC-06.11b, UC-06.11c).

---

<a id="uc-0601"></a>
## UC-06.01 Mở trình chỉnh sửa

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Editor |
| Mô tả | Mở timeline của một chương hoặc cả dự án để dựng video |
| Tiền điều kiện | Chương (hoặc các chương) có tư liệu |
| Hậu điều kiện | **Thành công:** timeline được tải kèm ETag; preview sẵn sàng |
| Kích hoạt | "Mở trình chỉnh sửa" từ chương, Tư liệu, Map hoặc thông báo `chapter.media-ready` |
| Quan hệ | include UC-06.01a; được mở rộng bởi UC-06.15 |
| Truy vết | FR-EDT-01, 02 |

**Luồng chính**
1. Editor chọn phạm vi: một chương, hoặc cả dự án (các chương nối tiếp).
2. Nếu phạm vi chưa có timeline, hệ thống thực hiện **UC-06.01a**.
3. Hệ thống tải tracks + items và hiển thị: vùng preview, thư viện (tư liệu, âm thanh, chuyển cảnh), timeline nhiều track, bảng thuộc tính.
4. Nếu tư liệu đã đổi kể từ lần mở trước, hệ thống thực hiện UC-06.15.

**Luồng thay thế / ngoại lệ**
- **1a.** Chương chưa "Sẵn sàng dựng": vẫn mở được; clip thiếu ảnh/thuyết minh hiển thị dạng chỗ trống có nút "Sinh tư liệu" (UC-05.07c); không xuất được (UC-06.16a).

### UC-06.01a Dựng bản nháp timeline từ tư liệu
<a id="uc-0601a"></a>
- **Loại:** include.
- **Các bước:** (1) tạo các track: Video, Thuyết minh (khóa), Phụ đề, Nhạc nền, SFX, Overlay; (2) với mỗi shot theo thứ tự: item `IMAGE` và item `NARRATION`, thời lượng = audio + đệm 0,3 s / 0,5 s; (3) phụ đề dựng từ `word_timings` (nguyên văn); (4) mặc định Ken Burns luân phiên, crossfade 0,5 s, khung hình theo dự án; (5) với dự án nhiều chương: thêm clip tiêu đề chương (UC-06.07) nếu bật.
- **Kết quả:** timeline `DRAFT` thỏa IC-10; nhạc nền và SFX để trống.

---

<a id="uc-0602"></a>
## UC-06.02 Thao tác timeline

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Editor |
| Mô tả | Kéo thả, di chuyển, cắt (split), trim, nhân bản, xóa clip; zoom, snap, phím tắt, undo/redo |
| Tiền điều kiện | Timeline đang mở |
| Hậu điều kiện | **Thành công:** thay đổi được lưu tự động (version tăng) và thỏa BR-24. **Tối thiểu:** thao tác vi phạm bị hoàn tác, không làm hỏng timeline |
| Kích hoạt | Thao tác chuột/bàn phím trên timeline |
| Quan hệ | include UC-06.02a |
| Truy vết | FR-EDT-03, 04, 18; ADR-14 |

**Luồng chính**
1. Editor thực hiện thao tác; client áp vào store cục bộ (có thể undo/redo ≥ 100 bước) và cập nhật preview ngay.
2. Client kiểm tra sơ bộ **UC-06.02a** (chặn ngay thao tác cấm trên clip thuyết minh).
3. Sau 1–2 s không thao tác, client gửi lô `apply-ops` kèm `ifMatch`.
4. Server thực hiện **UC-06.02a**, ghi items, tăng version, trả ETag mới.

**Luồng thay thế / ngoại lệ**
- **4a.** `422 NARRATION_LOCKED`: client hoàn tác thao tác vi phạm, hiện giải thích.
- **4b.** `409`: UC-02.10 (bản của người lưu sau được lưu thành phiên bản timeline có tên).
- **\*a.** Mất mạng: thao tác giữ trong hàng đợi cục bộ, đồng bộ khi có mạng; hiện trạng thái "Chưa lưu".

### UC-06.02a Kiểm tra khóa thuyết minh (BR-24)
<a id="uc-0602a"></a>
- **Loại:** include (client và server).
- **Các bước:** từ chối thao tác nếu: cắt, trim, xóa, đổi thứ tự, đổi tốc độ clip `NARRATION`; hai clip thuyết minh chồng nhau; clip ảnh của shot kết thúc trước khi thuyết minh của shot đó đọc xong; xóa track Thuyết minh. Cho phép: dời thời điểm clip thuyết minh (chèn khoảng lặng, kéo theo các clip phía sau), chỉnh âm lượng/keyframe âm lượng.
- **Kết quả:** timeline luôn thỏa IC-10; độ phủ văn bản không bao giờ giảm.

---

<a id="uc-0603"></a>
## UC-06.03 Quản lý track

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Editor |
| Mô tả | Thêm, đổi tên, sắp xếp, ẩn, tắt tiếng, solo, xóa track |
| Tiền điều kiện | Timeline đang mở |
| Hậu điều kiện | **Thành công:** cấu trúc track cập nhật |
| Kích hoạt | Menu của track |
| Truy vết | FR-EDT-02, 15 |

**Luồng chính**
1. Editor chọn "Thêm track" (Overlay, Nhạc nền, SFX) hoặc thao tác trên track có sẵn.
2. Hệ thống áp thay đổi qua UC-06.02.

**Luồng thay thế / ngoại lệ**
- **1a.** Xóa track Thuyết minh hoặc Video chính: bị chặn.
- **1b.** Xóa track có clip: yêu cầu xác nhận; có thể hoàn tác.

---

<a id="uc-0604"></a>
## UC-06.04 Hiệu ứng Ken Burns & điểm tập trung

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Editor |
| Mô tả | Đặt chuyển động cho clip ảnh: none, zoom in/out, pan bốn hướng, cường độ, điểm tập trung, nhiều pha, keyframe |
| Tiền điều kiện | Có clip ảnh |
| Hậu điều kiện | **Thành công:** thuộc tính `motion` cập nhật; preview phản ánh ngay |
| Kích hoạt | Chọn clip ảnh → bảng "Chuyển động" |
| Truy vết | FR-EDT-06 |

**Luồng chính**
1. Editor chọn một hoặc nhiều clip ảnh.
2. Editor chọn kiểu chuyển động, cường độ, bấm lên ảnh để đặt điểm tập trung.
3. Hệ thống lưu qua UC-06.02, đánh dấu `user_modified`.

**Luồng thay thế / ngoại lệ**
- **2a.** Clip dài > 30 s: gợi ý chuyển động nhiều pha, hoặc tách shot trong Storyboard (UC-05.06c).

---

<a id="uc-0605"></a>
## UC-06.05 Chuyển cảnh

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Editor |
| Mô tả | Đặt kiểu và thời lượng chuyển cảnh giữa hai clip ảnh |
| Tiền điều kiện | Có ≥ 2 clip ảnh liền kề |
| Hậu điều kiện | **Thành công:** `transition_in` cập nhật; vị trí clip thuyết minh không đổi |
| Kích hoạt | Kéo chuyển cảnh từ thư viện vào mối nối, hoặc chọn mối nối |
| Truy vết | FR-EDT-07; BR-25 |

**Luồng chính**
1. Editor kéo kiểu chuyển cảnh (cut, fade, crossfade, fade-to-black/white, slide, wipe, zoom) vào mối nối.
2. Editor chỉnh thời lượng (0–1,5 s) hoặc chọn "Áp cho tất cả".
3. Hệ thống lưu qua UC-06.02.

**Luồng thay thế / ngoại lệ**
- **2a.** Chuyển cảnh làm clip ảnh ngắn hơn khoảng đọc: hệ thống tự kéo dài clip ảnh tương ứng (BR-25).

---

<a id="uc-0606"></a>
## UC-06.06 Khung hình & tinh chỉnh màu

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Editor |
| Mô tả | Chọn cách khớp ảnh với khung video và chỉnh màu |
| Tiền điều kiện | Có clip ảnh |
| Hậu điều kiện | **Thành công:** `framing` (timeline) và `color` (clip) cập nhật |
| Kích hoạt | Bảng "Khung hình" / "Màu" |
| Truy vết | FR-EDT-08, 09 |

**Luồng chính**
1. Editor chọn khung hình cho toàn timeline: crop (theo điểm tập trung), fit (viền màu), nền mờ.
2. Editor chỉnh độ sáng, tương phản, bão hòa, nhiệt độ màu hoặc chọn bộ lọc màu; áp cho clip đã chọn hoặc toàn video.
3. Hệ thống lưu; preview cập nhật.

---

<a id="uc-0607"></a>
## UC-06.07 Overlay chữ / logo, clip tiêu đề & kết

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Editor |
| Mô tả | Thêm chữ (tên truyện, tên chương, credit), logo/watermark, clip mở đầu và kết |
| Tiền điều kiện | Timeline đang mở |
| Hậu điều kiện | **Thành công:** item `TITLE`/`TEXT`/`LOGO` được thêm trên track Overlay |
| Kích hoạt | "Thêm chữ" / "Thêm logo" / "Clip tiêu đề" |
| Truy vết | FR-EDT-05, 10 |

**Luồng chính**
1. Editor chọn loại overlay và vị trí trên timeline.
2. Editor nhập nội dung, chọn font (hỗ trợ tiếng Việt), cỡ, màu, viền/bóng, vị trí, hiệu ứng vào/ra.
3. Hệ thống lưu qua UC-06.02.

**Luồng thay thế / ngoại lệ**
- **1a.** Clip tiêu đề chương: mặc định không có thuyết minh; nếu bật "đọc tên chương" thì sinh audio tên chương (tính phí TTS).
- **2a.** Logo tải lên: kiểm tra như UC-04.04.

---

<a id="uc-0608"></a>
## UC-06.08 Kiểu phụ đề

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Editor |
| Mô tả | Bật/tắt và định kiểu phụ đề; **nội dung luôn nguyên văn, không sửa được** |
| Tiền điều kiện | Có clip thuyết minh có `word_timings` |
| Hậu điều kiện | **Thành công:** `subtitle_style` cập nhật |
| Kích hoạt | Bảng "Phụ đề" |
| Truy vết | FR-EDT-11; BR-22 |

**Luồng chính**
1. Editor bật phụ đề, chọn kiểu cả câu hoặc karaoke (tô sáng từng từ).
2. Editor chọn font, cỡ, màu, nền, vị trí trong vùng an toàn theo tỷ lệ khung hình.
3. Hệ thống lưu; preview hiển thị phụ đề đồng bộ.

**Luồng thay thế / ngoại lệ**
- **\*a.** Editor cố sửa chữ trong phụ đề: bị chặn, hướng dẫn sửa văn bản chương trong Workspace (UC-03.02) rồi sinh lại thuyết minh.

---

<a id="uc-0609"></a>
## UC-06.09 Thêm nhạc nền

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Editor |
| Mô tả | Đặt một hoặc nhiều đoạn nhạc nền, fade, âm lượng, ducking dưới thuyết minh |
| Tiền điều kiện | Timeline đang mở |
| Hậu điều kiện | **Thành công:** item `AUDIO` trên track Nhạc nền; ducking bắt buộc khi chồng thuyết minh |
| Kích hoạt | Kéo nhạc từ thư viện vào track Nhạc nền |
| Quan hệ | include UC-06.11 |
| Truy vết | FR-EDT-13; BR-25, BR-26 |

**Luồng chính**
1. Editor thực hiện **UC-06.11** để tìm và nghe thử nhạc.
2. Editor kéo bài nhạc vào track Nhạc nền tại vị trí mong muốn.
3. Editor cắt, trim, lặp; đặt fade in/out, âm lượng, mức ducking (mặc định −12 dB).
4. Hệ thống lưu qua UC-06.02; preview giảm nhạc khi có lời đọc.

**Luồng thay thế / ngoại lệ**
- **3a.** Nhạc ngắn hơn video: gợi ý "Lặp đến hết" hoặc thêm bài thứ hai với crossfade.
- **3b.** Editor tắt ducking khi nhạc chồng thuyết minh: bị chặn, mức tối thiểu −6 dB (BR-25).

---

<a id="uc-0610"></a>
## UC-06.10 Thêm SFX

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Editor |
| Mô tả | Đặt hiệu ứng âm thanh (mưa, bước chân, pháo hoa…) tại thời điểm cụ thể |
| Tiền điều kiện | Timeline đang mở |
| Hậu điều kiện | **Thành công:** item `AUDIO` trên track SFX |
| Kích hoạt | Kéo SFX vào track SFX |
| Quan hệ | include UC-06.11; được mở rộng bởi UC-06.11c |
| Truy vết | FR-EDT-14 |

**Luồng chính**
1. Editor thực hiện **UC-06.11** (lọc `kind = SFX`).
2. Editor kéo SFX vào track SFX tại thời điểm mong muốn (snap theo đầu câu nhờ `word_timings`).
3. Editor trim, fade, chỉnh âm lượng; có thể chồng nhiều SFX trên nhiều track.
4. Hệ thống lưu qua UC-06.02.

---

<a id="uc-0611"></a>
## UC-06.11 Tìm trong thư viện âm thanh

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Editor |
| Mô tả | Tìm nhạc nền / SFX có license trong thư viện hệ thống và thư viện của tôi |
| Tiền điều kiện | Đã đăng nhập |
| Hậu điều kiện | **Thành công:** danh sách kết quả, nghe thử được |
| Kích hoạt | Mở tab "Âm thanh" |
| Quan hệ | được include bởi UC-06.09, UC-06.10; được mở rộng bởi UC-06.11a, UC-06.11b |
| Truy vết | FR-EDT-12; BR-26 |

**Luồng chính**
1. Editor nhập từ khóa, chọn loại (Nhạc / SFX), thể loại, tâm trạng, thời lượng.
2. Hệ thống trả kết quả kèm waveform, thời lượng, nhãn license.
3. Editor nghe thử và kéo vào timeline.

**Luồng thay thế / ngoại lệ**
- **2a.** Không có kết quả phù hợp: gợi ý UC-06.11a hoặc UC-06.11b.

### UC-06.11a Tải nhạc / SFX lên
<a id="uc-0611a"></a>
- **Loại:** extend. **Các bước:** chọn file MP3/WAV/M4A (≤ 30 MB, ≤ 15 phút), chọn loại, đánh dấu "Tôi có quyền sử dụng" (bắt buộc), hệ thống kiểm tra định dạng, tạo waveform. **Kết quả:** `audio_assets` thuộc thư viện của tôi (`license = USER_UPLOAD`).

### UC-06.11b Sinh nhạc / SFX bằng AI
<a id="uc-0611b"></a>
- **Loại:** extend (C). **Tác nhân phụ:** Music/SFX Provider. **Các bước:** mô tả ("tiếng mưa nhẹ ngoài cửa sổ"), chọn thời lượng; hệ thống hiện giá (MUSIC_AI 2 / SFX_AI 1 credit), giữ credit (UC-05.17), sinh, nghe thử, lưu. **Kết quả:** `audio_assets` (`license = AI_GENERATED`).

### UC-06.11c Gợi ý SFX theo đoạn văn
<a id="uc-0611c"></a>
- **Loại:** extend UC-06.10 (C). **Tác nhân phụ:** LLM. **Các bước:** AI đọc đoạn nguồn từng shot, đề xuất danh sách `{shot, thời điểm theo word_timings, từ khóa SFX}`; hệ thống tìm SFX phù hợp trong thư viện; Editor duyệt từng mục (chèn / bỏ). **Kết quả:** các SFX được duyệt chèn vào track SFX; không có gì tự chèn khi chưa duyệt.

---

<a id="uc-0612"></a>
## UC-06.12 Trộn âm & chuẩn hóa loudness

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Editor |
| Mô tả | Cân âm lượng giữa thuyết minh, nhạc, SFX; đặt loudness đầu ra |
| Tiền điều kiện | Timeline có âm thanh |
| Hậu điều kiện | **Thành công:** âm lượng track và `master` cập nhật |
| Kích hoạt | Mở bảng "Âm thanh tổng" |
| Truy vết | FR-EDT-15; NFR-CMP-03 |

**Luồng chính**
1. Editor chỉnh âm lượng từng track, tắt tiếng hoặc solo để nghe riêng.
2. Editor chọn mức loudness đầu ra (mặc định −14 LUFS).
3. Hệ thống hiển thị đồng hồ mức; cảnh báo clipping.

---

<a id="uc-0613"></a>
## UC-06.13 Xem trước

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Editor |
| Mô tả | Phát video theo thời gian thực trong trình duyệt, không cần render |
| Tiền điều kiện | Timeline đang mở |
| Hậu điều kiện | **Thành công:** hình, thuyết minh, nhạc, SFX, phụ đề đồng bộ (lệch ≤ 100 ms) |
| Kích hoạt | Play, scrub, nhảy tới clip |
| Truy vết | FR-EDT-17; NFR-PERF-11, 13; ADR-13 |

**Luồng chính**
1. Editor bấm Play hoặc kéo playhead.
2. Client dựng khung hình bằng cùng component dùng khi xuất, phát audio đã trộn qua WebAudio.
3. Editor dừng tại vị trí cần sửa và chỉnh trực tiếp.

**Luồng thay thế / ngoại lệ**
- **2a.** Media chưa tải xong: hiện khung chờ, ưu tiên tải vùng quanh playhead.
- **2b.** Clip thiếu tư liệu: hiện khung giữ chỗ và thời lượng ước tính.

---

<a id="uc-0614"></a>
## UC-06.14 Lịch sử phiên bản & khôi phục

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Editor |
| Mô tả | Xem, đặt tên và khôi phục phiên bản timeline |
| Tiền điều kiện | Timeline có ≥ 1 phiên bản đã lưu |
| Hậu điều kiện | **Thành công:** khôi phục thành phiên bản mới; lịch sử không mất |
| Kích hoạt | Mở "Lịch sử" |
| Truy vết | FR-EDT-18 |

**Luồng chính**
1. Editor mở lịch sử: danh sách phiên bản (thời gian, người sửa, tên nếu có).
2. Editor xem trước một phiên bản.
3. Editor bấm "Khôi phục"; hệ thống tạo phiên bản mới với nội dung cũ, sau khi kiểm tra UC-06.02a với tư liệu hiện tại.

**Luồng thay thế / ngoại lệ**
- **3a.** Phiên bản cũ tham chiếu tư liệu đã thay đổi: khôi phục, rồi chạy UC-06.15 để cập nhật clip.

---

<a id="uc-0615"></a>
## UC-06.15 Đồng bộ khi tư liệu thay đổi

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Hệ thống (khi Editor mở trình chỉnh sửa hoặc tư liệu đổi) |
| Mô tả | Cập nhật clip khi ảnh/thuyết minh được sinh lại hoặc storyboard thay đổi, **giữ** chỉnh sửa của người dùng |
| Tiền điều kiện | Có thay đổi tư liệu kể từ phiên bản timeline hiện tại |
| Hậu điều kiện | **Thành công:** clip trỏ tới tư liệu mới; IC-10 thỏa; clip bị ảnh hưởng được đánh dấu |
| Kích hoạt | Mở trình chỉnh sửa (UC-06.01), sự kiện `narration.updated`/`illustration.ready`, đổi bản nháp hiện hành |
| Quan hệ | extend UC-06.01 |
| Truy vết | FR-EDT-19 |

**Luồng chính**
1. Hệ thống so tư liệu hiện hành với tham chiếu trong timeline.
2. *Ảnh mới:* thay `illustration_id`, giữ motion/màu/chuyển cảnh.
3. *Thuyết minh mới:* thay `narration_id`, cập nhật độ dài; dời các clip phía sau theo độ chênh (nhạc, SFX dời theo nếu gắn với shot).
4. *Storyboard đổi (tách/gộp shot):* thêm hoặc bớt cặp clip ảnh/thuyết minh tương ứng, đặt hiệu ứng mặc định cho clip mới.
5. Hệ thống đánh dấu các clip thay đổi, hiện thông báo "N clip đã cập nhật" để Editor kiểm tra.

**Luồng thay thế / ngoại lệ**
- **3a.** SFX đặt trong khoảng thời gian không còn tồn tại: chuyển SFX về cuối clip gần nhất và đánh dấu cần xem lại.

---

<a id="uc-0616"></a>
## UC-06.16 Xuất video MP4

| Mục | Nội dung |
|---|---|
| Tác nhân chính / phụ | Editor / Render Worker |
| Mô tả | Bước 6: render timeline thành MP4 kèm phụ đề |
| Tiền điều kiện | Timeline thỏa UC-06.16a |
| Hậu điều kiện | **Thành công:** Render phiên bản mới `READY`, đặt làm bản chính, có MP4 + SRT/VTT. **Tối thiểu:** lỗi thì Render `FAILED`, không ảnh hưởng timeline |
| Kích hoạt | Bấm "Xuất video" |
| Quan hệ | include UC-06.16a; được mở rộng bởi UC-06.16b |
| Truy vết | FR-EDT-21..24, 26; BR-23; seq-chinh-sua-xuat-video |

**Luồng chính**
1. Editor bấm "Xuất video".
2. Hệ thống thực hiện **UC-06.16a** và hiện báo cáo độ phủ, thời lượng.
3. Editor chọn độ phân giải (720p nháp / 1080p) và xác nhận.
4. Hệ thống chụp `timeline_snapshot` của phiên bản hiện tại và tạo job `RENDER_TIMELINE` (miễn phí).
5. Render Worker dựng khung hình (Ken Burns, chuyển cảnh, overlay, màu, phụ đề) theo đoạn song song; trộn thuyết minh + nhạc (ducking) + SFX; chuẩn hóa loudness; encode H.264/AAC.
6. Tiến độ gửi qua SSE; Editor có thể hủy.
7. Hoàn tất: tạo Render `READY` + SRT/VTT; thông báo "Video đã sẵn sàng" và mở UC-06.17.

**Luồng thay thế / ngoại lệ**
- **2a.** Chưa đạt điều kiện: liệt kê vị trí lỗi trên timeline, có nút nhảy tới.
- **5a.** Lỗi encode: retry một lần; vẫn lỗi thì `FAILED`, hiện mã lỗi.
- **6a.** Editor hủy: job `CANCELLED`.

### UC-06.16a Kiểm tra điều kiện & độ phủ 100%
<a id="uc-0616a"></a>
- **Loại:** include.
- **Các bước:** kiểm tra (1) mọi shot có ảnh `DONE`; (2) mọi shot có thuyết minh `VERIFIED`/`ACCEPTED`, không `OUTDATED`; (3) timeline thỏa IC-10/BR-24; (4) tổng ký tự các đoạn nguồn có clip thuyết minh = tổng ký tự chương (100%).
- **Kết quả:** báo cáo `{coverage: covered/total, missingImages, needsReview, outdated, violations}`; chỉ cho xuất khi mọi mục đạt.

### UC-06.16b Chia video thành phần
<a id="uc-0616b"></a>
- **Loại:** extend. **Các bước:** chọn chia theo chương hoặc theo thời lượng tối đa (vd. 10 phút); hệ thống cắt tại ranh giới shot gần nhất, xuất nhiều Render. **Kết quả:** các file MP4 nối lại đủ 100% truyện.

---

<a id="uc-0617"></a>
## UC-06.17 Tải MP4 / SRT / audio

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Editor |
| Mô tả | Tải video và các file kèm theo về máy |
| Tiền điều kiện | Có Render `READY` |
| Hậu điều kiện | **Thành công:** file được tải qua link ký có thời hạn 15 phút |
| Kích hoạt | "Tải xuống" ở thông báo hoặc danh sách Renders |
| Truy vết | FR-EDT-24, 25; NFR-SEC-05 |

**Luồng chính**
1. Editor mở danh sách Renders (phiên bản, độ phân giải, thời lượng, ngày, bản chính).
2. Editor chọn file: MP4, SRT, VTT hoặc audio thuyết minh (MP3/WAV).
3. Hệ thống chuyển hướng tới link ký; trình duyệt tải file.

**Luồng thay thế / ngoại lệ**
- **2a.** Editor đặt một phiên bản khác làm bản chính, hoặc xóa phiên bản (xác nhận).
- **3a.** Link hết hạn: bấm lại để lấy link mới.
- **\*a.** Gói Free: video 720p có watermark (08 §3.5).
