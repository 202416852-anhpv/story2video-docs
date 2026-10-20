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

| Mục | Nội dung |
|---|---|
| Loại | include của UC-06.01 (bước 2) |
| Tác nhân | Hệ thống (`TimelineBuilder`) |
| Mô tả | Tự dựng bản nháp timeline từ ảnh, thuyết minh và phụ đề của các shot, để Editor chỉ phải chỉnh chứ không dựng từ đầu |
| Tiền điều kiện | Phạm vi (chương hoặc cả dự án) chưa có timeline; mọi shot hiện hành có ảnh `DONE` và thuyết minh `VERIFIED` hoặc `ACCEPTED` (chương "Sẵn sàng dựng") |
| Hậu điều kiện | **Thành công:** timeline `DRAFT` thỏa IC-10, `version = 1`; nhạc nền và SFX để trống. **Tối thiểu:** lỗi thì không tạo timeline dở dang |
| Kích hoạt | UC-06.01 bước 2; hoặc chương chuyển `READY_TO_EDIT` (`chapter.media-ready`) |
| Truy vết | FR-EDT-01..03; IC-10, IC-12; BR-24, BR-25; API 2.6 `POST /projects/{pid}/timelines` |

**Luồng chính**
1. Hệ thống tạo `timelines` với `aspect_ratio` theo dự án, `framing` mặc định và `subtitle_style` mặc định.
2. Hệ thống tạo các track: Video, Thuyết minh (khóa, `locked = true`), Phụ đề, Nhạc nền, SFX, Overlay.
3. Với mỗi shot theo thứ tự: tạo item `IMAGE` (ảnh hiện hành) và item `NARRATION` (thuyết minh hiện hành); thời lượng ảnh bằng thời lượng audio cộng đệm 0,3 s / 0,5 s.
4. Hệ thống dựng phụ đề từ `word_timings` và đoạn nguồn gốc, luôn nguyên văn (BR-22).
5. Hệ thống đặt mặc định Ken Burns luân phiên, chuyển cảnh crossfade 0,5 s.
6. Với dự án nhiều chương: thêm clip tiêu đề chương (UC-06.07) nếu tùy chọn này bật.
7. Hệ thống lưu timeline, kiểm tra IC-10 và phát `timeline.updated`.

**Luồng thay thế / ngoại lệ**
- **0a.** Phạm vi đã có timeline: `POST /timelines` trả timeline sẵn có, không dựng lại.
- **0b.** Chương chưa "Sẵn sàng dựng": `422 PRECONDITION_FAILED_BUSINESS`, liệt kê shot còn thiếu [ĐX].
- **7a.** IC-10 không thỏa sau khi dựng (lỗi lập trình): không lưu, cảnh báo P1.

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

### UC-06.02a Kiểm tra khóa thuyết minh
<a id="uc-0602a"></a>

| Mục | Nội dung |
|---|---|
| Loại | include của UC-06.02 |
| Tác nhân | Hệ thống (`NarrationGuard` ở client và `OpsApplier` ở server) |
| Mô tả | Bảo vệ track thuyết minh khỏi mọi thao tác làm thay đổi nội dung đọc; một bộ luật dùng chung cho client và server |
| Tiền điều kiện | Có thao tác (hoặc lô thao tác) sắp áp lên timeline |
| Hậu điều kiện | **Thành công:** timeline luôn thỏa IC-10; độ phủ văn bản không bao giờ giảm. **Tối thiểu:** thao tác vi phạm không được áp dụng một phần nào |
| Kích hoạt | Mỗi thao tác của Editor trên timeline (UC-06.02) và mỗi lần `apply-ops` |
| Truy vết | BR-24, BR-25; IC-10, IC-12; ADR-16; NFR-INT-01; API 2.6 `POST …/timelines/{tlid}:apply-ops` |

**Luồng chính**
1. `NarrationGuard` ở client kiểm tra thao tác bằng bộ luật trong package TypeScript dùng chung (`@studio/timeline-rules`) trước khi áp vào `TimelineStore`.
2. Thao tác hợp lệ được `OpsBatcher` gom và gửi `apply-ops` kèm `ifMatch`.
3. `OpsApplier` ở server chạy lại **cùng** bộ luật trên toàn lô.
4. Toàn lô hợp lệ: áp dụng nguyên tử, tăng `version`, phát `timeline.updated`.
5. Có thao tác vi phạm: server từ chối cả lô, trả `422 NARRATION_LOCKED` kèm `opIndex`; client hoàn tác thao tác đó và hiện lý do.

**Luồng thay thế / ngoại lệ**
- **1a.** Bị **cấm** với clip `NARRATION`: cắt, trim, xóa, đổi thứ tự, đổi tốc độ; hai clip chồng nhau.
- **1b.** Bị cấm: để clip ảnh của một shot kết thúc trước khi thuyết minh của shot đó đọc xong (BR-25); xóa track Thuyết minh (IC-12).
- **1c.** Được **cho phép**: dời thời điểm clip thuyết minh (chèn khoảng lặng, kéo theo các clip phía sau); chỉnh âm lượng và keyframe âm lượng.
- **3a.** Client và server cho kết quả khác nhau (phiên bản bộ luật lệch): server là chuẩn; client nhận `422` và hiển thị như trên.
- **4a.** `409 VERSION_CONFLICT` (người khác vừa sửa timeline): xử lý theo UC-02.10.

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
## UC-06.04 Đặt hiệu ứng Ken Burns & điểm tập trung

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
## UC-06.05 Đặt chuyển cảnh

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
## UC-06.06 Chọn khung hình & tinh chỉnh màu

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

**Luồng thay thế / ngoại lệ**
- **\*a.** Editor bật "Vùng an toàn" hoặc "Lưới căn chỉnh" trên preview để đặt phụ đề, overlay. Chỉ là lớp hỗ trợ khi chỉnh sửa, **không được vẽ vào video xuất**.

---

<a id="uc-0607"></a>
## UC-06.07 Thêm overlay chữ / logo, clip tiêu đề & kết

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
## UC-06.08 Định kiểu phụ đề

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Editor |
| Mô tả | Bật/tắt và định kiểu phụ đề; **nội dung luôn nguyên văn, không sửa được** |
| Tiền điều kiện | Có clip thuyết minh có `word_timings` |
| Hậu điều kiện | **Thành công:** `subtitle_style` cập nhật |
| Kích hoạt | Bảng "Phụ đề" |
| Truy vết | FR-EDT-11; BR-22 |

**Luồng chính**
1. Editor bật phụ đề, chọn kiểu cả câu hoặc karaoke (tô sáng từng từ). Có thể áp một **mẫu preset** dựng sẵn (hằng số dùng chung, không lưu DB) làm điểm xuất phát; hệ thống chỉ sao chép giá trị vào `subtitle_style`, nên đổi preset sau này không ảnh hưởng timeline cũ.
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

| Mục | Nội dung |
|---|---|
| Loại | extend của UC-06.11 (điểm mở rộng: kết quả tìm không phù hợp) |
| Tác nhân | Editor |
| Mô tả | Tải nhạc hoặc SFX của riêng mình lên thư viện cá nhân để dùng trong timeline |
| Tiền điều kiện | Đã đăng nhập; file là MP3, WAV hoặc M4A |
| Hậu điều kiện | **Thành công:** có `audio_assets` thuộc thư viện của tôi (`license = USER_UPLOAD`, `owner_user_id` = Editor). **Tối thiểu:** file không đạt thì không lưu gì |
| Kích hoạt | Bấm "Tải lên" trong tab Âm thanh |
| Truy vết | FR-EDT-12; BR-26; IC-15; NFR-SEC-10; 08 §5; API 2.6 `POST /audio-assets` |

**Luồng chính**
1. Editor chọn file MP3, WAV hoặc M4A (≤ 30 MB, ≤ 15 phút), chọn loại Nhạc hoặc SFX và nhập tên.
2. Editor đánh dấu "Tôi có quyền sử dụng" (bắt buộc); hệ thống gửi `licenseConfirmed: true`.
3. Hệ thống kiểm tra MIME thật, kích thước, quét malware.
4. Hệ thống tạo job `PROCESS_AUDIO_UPLOAD` (Media Processing Worker): đo thời lượng và tạo waveform.
5. Xong job, tài sản hiện trong "thư viện của tôi", nghe thử và kéo vào timeline được (UC-06.09, UC-06.10). Không tốn credit.

**Luồng thay thế / ngoại lệ**
- **2a.** Không đánh dấu quyền sử dụng: từ chối, không tải lên.
- **3a.** Sai định dạng, MIME không khớp, vượt 30 MB hoặc 15 phút, hoặc phát hiện malware: báo lý do cụ thể.
- **4a.** File hỏng, không đọc được thời lượng: job `FAILED`, tài sản không xuất hiện, báo lỗi.
- ***a.** Chủ sở hữu xóa được tài sản của mình (`DELETE /audio-assets/{aid}`); tài sản của người khác không bao giờ xuất hiện trong kết quả tìm kiếm.

### UC-06.11b Sinh nhạc / SFX bằng AI
<a id="uc-0611b"></a>

| Mục | Nội dung |
|---|---|
| Loại | extend của UC-06.11 (tùy chọn *Could*) |
| Tác nhân | Editor / Music và SFX Provider |
| Mô tả | Sinh nhạc nền hoặc hiệu ứng âm thanh bằng AI từ một mô tả |
| Tiền điều kiện | Đã đăng nhập; đủ credit; provider có quyền thương mại (BR-26) |
| Hậu điều kiện | **Thành công:** có `audio_assets` (`license = AI_GENERATED`) trong thư viện của tôi; credit được trừ. **Tối thiểu:** lỗi thì hoàn credit |
| Kích hoạt | Bấm "Sinh bằng AI" trong tab Âm thanh |
| Truy vết | FR-EDT-12; BR-01, BR-02, BR-26; 08 §3.3 (`MUSIC_AI` 2 credit mỗi bài ≤ 3 phút, `SFX_AI` 1 credit mỗi hiệu ứng ≤ 10 giây); API 2.6 `POST /projects/{pid}/audio-assets:generate` |

**Luồng chính**
1. Editor chọn loại (Nhạc hoặc SFX), nhập mô tả (ví dụ "tiếng mưa nhẹ ngoài cửa sổ") và thời lượng.
2. Hệ thống hiển thị giá và Editor xác nhận; hệ thống giữ credit (UC-05.17) và tạo job `GENERATE_MUSIC` hoặc `GENERATE_SFX`.
3. Worker chạy moderation đầu vào rồi gọi provider; kết quả qua moderation đầu ra.
4. Hệ thống lưu `audio_assets` (`AI_GENERATED`), CAPTURE credit và cho Editor nghe thử.
5. Editor kéo tài sản vào timeline hoặc bỏ đi.

**Luồng thay thế / ngoại lệ**
- **1a.** Thời lượng vượt giới hạn (nhạc 3 phút, SFX 10 giây): chặn.
- **2a.** Không đủ credit: `402`.
- **3a.** Lỗi provider sau retry hoặc vi phạm chính sách: job `FAILED`, RELEASE credit, không lưu đầu ra (BR-18).
- ***a.** Chức năng *Could*: bật/tắt theo cấu hình provider (UC-10.03).

### UC-06.11c Gợi ý SFX theo đoạn văn
<a id="uc-0611c"></a>

| Mục | Nội dung |
|---|---|
| Loại | extend của UC-06.10 (tùy chọn *Could*) |
| Tác nhân | Editor / LLM |
| Mô tả | AI đọc đoạn văn của từng shot và gợi ý chỗ nên chèn SFX; Editor duyệt từng gợi ý, không có gì tự chèn |
| Tiền điều kiện | Timeline đang mở; thư viện SFX có dữ liệu |
| Hậu điều kiện | **Thành công:** các gợi ý được Editor chấp nhận trở thành item `AUDIO` trên track SFX. **Tối thiểu:** không gợi ý nào được chèn khi chưa duyệt |
| Kích hoạt | Bấm "Gợi ý SFX" trong tab SFX |
| Truy vết | FR-EDT-14; BR-21; 08 §3.3 (`SFX_SUGGEST`, 0 credit, có giới hạn tần suất); 04 §3.5 `sfx_suggestions`; API 2.6 `POST …/timelines/{tlid}:suggest-sfx` |

**Luồng chính**
1. Editor bấm "Gợi ý SFX".
2. Hệ thống tạo job `SUGGEST_SFX` (miễn phí, có giới hạn tần suất).
3. LLM đọc đoạn nguồn từng shot (chỉ đọc) và đề xuất `{shot, thời điểm theo word_timings, từ khóa}`.
4. Hệ thống tìm SFX phù hợp với từ khóa trong thư viện và lưu `sfx_suggestions` ở trạng thái `PROPOSED`.
5. Hệ thống hiển thị danh sách có nút nghe thử; Editor chấp nhận hoặc bỏ từng mục.
6. Chấp nhận: hệ thống thêm item `AUDIO` vào track SFX qua `apply-ops` (UC-06.02) và đặt `ACCEPTED`. Bỏ: đặt `REJECTED`.

**Luồng thay thế / ngoại lệ**
- **3a.** LLM không đề xuất gì: báo "Không có gợi ý".
- **4a.** Không có SFX phù hợp trong thư viện: hiện từ khóa và gợi ý tải lên (UC-06.11a) hoặc sinh bằng AI (UC-06.11b).
- **6a.** Timeline hoặc storyboard đã đổi sau khi gợi ý: thời điểm có thể lệch; hệ thống cảnh báo và đánh dấu gợi ý lỗi thời.
- **2a.** Vượt giới hạn tần suất: `429`.

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
## UC-06.14 Xem lịch sử & khôi phục phiên bản timeline

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

| Mục | Nội dung |
|---|---|
| Loại | include của UC-06.16 (bước 2) |
| Tác nhân | Hệ thống (`ReadinessChecker`) |
| Mô tả | Kiểm tra timeline đã đủ điều kiện xuất chưa, nhất là độ phủ văn bản 100% |
| Tiền điều kiện | Timeline đang mở |
| Hậu điều kiện | **Thành công:** có báo cáo điều kiện; chỉ cho xuất khi mọi mục đạt. **Tối thiểu:** không thay đổi dữ liệu |
| Kích hoạt | UC-06.16 bước 2; mỗi lần Editor mở hộp thoại xuất |
| Truy vết | BR-11, BR-23, BR-24; IC-10, IC-11; NFR-INT-01; API 2.6 `GET …/timelines/{tlid}/readiness` |

**Luồng chính**
1. Hệ thống kiểm tra mọi shot hiện hành có ảnh `DONE`.
2. Hệ thống kiểm tra mọi shot có thuyết minh `VERIFIED` hoặc `ACCEPTED`, không có `OUTDATED`.
3. Hệ thống kiểm tra timeline thỏa IC-10 và BR-24.
4. Hệ thống kiểm tra tổng ký tự các đoạn nguồn có clip thuyết minh bằng tổng ký tự chương (100%).
5. Hệ thống trả `{ coverage: {covered, total}, missingImages[], needsReview[], outdated[], violations[] }`.
6. Giao diện hiển thị kết quả; mục không đạt có vị trí trên timeline và nút nhảy tới.

**Luồng thay thế / ngoại lệ**
- **5a.** Bất kỳ mục nào không đạt: nút "Xuất" bị vô hiệu hóa; nếu vẫn gọi tạo render thì `422` (IC-11).
- ***a.** Phạm vi cả dự án: độ phủ tính trên tổng ký tự của mọi chương trong timeline.

### UC-06.16b Chia video thành phần
<a id="uc-0616b"></a>

| Mục | Nội dung |
|---|---|
| Loại | extend của UC-06.16 |
| Tác nhân | Editor / Render Worker |
| Mô tả | Xuất video thành nhiều file nhỏ (theo chương hoặc theo thời lượng tối đa), cắt ở ranh giới shot để không mất lời đọc |
| Tiền điều kiện | Timeline thỏa UC-06.16a |
| Hậu điều kiện | **Thành công:** nhiều Render cùng `render_group_id`, mỗi phần có `part_no`; ghép lại đủ 100% truyện. **Tối thiểu:** không cắt giữa một shot |
| Kích hoạt | Chọn "Chia thành phần" trong hộp thoại xuất |
| Truy vết | FR-EDT-23; BR-23; IC-11; 04 §3.5 `renders`; API 2.6 `POST …/renders {splitBy, maxMinutes}` |

**Luồng chính**
1. Editor chọn chia theo chương hoặc theo thời lượng tối đa (nhập số phút).
2. Hệ thống tính điểm cắt: theo chương là ranh giới chương; theo thời lượng là ranh giới shot gần nhất mà phần không vượt quá số phút tối đa.
3. Hệ thống hiển thị danh sách phần (tên, thời lượng, phạm vi shot); Editor xác nhận.
4. Hệ thống tạo `render_group_id` và mỗi phần một Render (`part_no`) với `timeline_snapshot`; các phần được xếp hàng render theo giới hạn số render đồng thời của gói (NFR-SCAL-03).
5. Mỗi phần có MP4 và SRT/VTT riêng; phụ đề căn theo thời gian của phần đó.

**Luồng thay thế / ngoại lệ**
- **2a.** Một shot dài hơn số phút tối đa: shot đó không bị cắt, phần chứa nó vượt giới hạn; hệ thống cảnh báo.
- **4a.** Một phần lỗi: chỉ phần đó `FAILED`, các phần khác giữ nguyên; Editor render lại riêng phần lỗi [ĐX].
- **4b.** Editor hủy: các phần chưa xong chuyển `CANCELLED`.

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
