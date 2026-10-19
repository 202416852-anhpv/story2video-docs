# M05 — Sinh tư liệu: storyboard, ảnh, thuyết minh nguyên văn

> Bước 4 của luồng chính. Đầu ra **chỉ gồm ảnh + thuyết minh nguyên văn**; nhạc nền và SFX được thêm ở M06.
> Sơ đồ: `../../so-do/01-use-case/phan-ra/uc-m05a-storyboard.puml` (UC-05.01..06), `uc-m05b-sinh-anh-thuyet-minh.puml` (UC-05.07..17); `../../so-do/04-tuan-tu/seq-sinh-tu-lieu.puml`, `seq-storyboard-sinh-anh.puml`, `seq-thuyet-minh-nguyen-van.puml`; `../../so-do/05-hoat-dong/act-phu-kin-van-ban.puml`, `act-giu-tru-credit.puml`.
> Yêu cầu: FR-MED-01..05, FR-BOK-01..10/13/16, FR-NAR-01..09. Quy tắc: BR-07, BR-08, BR-11, BR-19..BR-22.

---

## Phần A — Storyboard (chạy tự động trong UC-05.07, tinh chỉnh tùy chọn)

<a id="uc-0501"></a>
## UC-05.01 Tạo bản nháp storyboard

| Mục | Nội dung |
|---|---|
| Tác nhân chính / phụ | Editor (hoặc hệ thống qua UC-05.07a) / LLM |
| Mô tả | Chia **toàn bộ** văn bản chương thành các shot liên tục; mỗi shot = 1 ảnh + 1 đoạn văn nguồn |
| Tiền điều kiện | Chương có văn bản, không bị khóa |
| Hậu điều kiện | **Thành công:** StoryboardDraft có N shot, `concat(đoạn nguồn) == chapter.content`; nếu là bản đầu tiên thì đặt làm hiện hành. **Tối thiểu:** không lưu bản nháp vi phạm phủ kín |
| Kích hoạt | "Create storyboard draft", hoặc tự động trong UC-05.07 |
| Quan hệ | include UC-05.01a |
| Truy vết | FR-BOK-01, 01a, 05; BR-20; ADR-11 |

**Luồng chính**
1. Hệ thống dựng ngữ cảnh: văn bản chương, Story Assets (tên, bí danh, facts), timeline truyện, Visual Rules, Chapter rules, thời lượng mục tiêu mỗi ảnh.
2. Hệ thống tách câu tất định và đánh số câu.
3. Job `STORYBOARD_DRAFT`: LLM nhận danh sách câu, trả Shot[] gồm `startSentence`, `endSentence`, title, focus, cast, items, location, thời điểm, ngày, brief (Subject/Environment/Composition/Camera/Lighting/Mood/Details), caption. LLM **không chép lại văn bản**.
4. Hệ thống thực hiện **UC-05.01a**.
5. Hệ thống ánh xạ tên sang tài sản (tên + bí danh); tên không khớp đánh dấu "chưa liên kết".
6. Hệ thống lưu bản nháp, các shot (`source_start`, `source_end`, `source_hash`) và hiển thị đoạn nguồn nguyên văn bên cạnh mỗi shot.

**Luồng thay thế / ngoại lệ**
- **3a.** LLM trả sai schema: thử lại kèm thông báo lỗi, tối đa 2 lần; vẫn lỗi thì job `FAILED`.
- **4a.** Phải sửa > 20% ranh giới: lưu kèm Director note cảnh báo chất lượng, gợi ý tạo lại.
- **5a.** Có tên chưa liên kết: hiện "Some names here aren't linked to an asset yet" kèm nút thêm tài sản (UC-04.02a) hoặc tự khớp (UC-05.06f).

### UC-05.01a Tách câu & kiểm tra phủ kín (CoverageValidator)
<a id="uc-0501a"></a>
- **Loại:** include (UC-05.01, UC-05.03, UC-05.06c, UC-05.06d).
- **Các bước:** (1) đổi chỉ số câu sang offset ký tự; (2) sắp shot, kẹp chỉ số, bỏ shot rỗng; (3) khoảng hở → gộp vào shot trước; chồng lấn → cắt theo shot sau; (4) snap ranh giới về đầu câu, khoảng trắng gán cho shot trước; (5) kiểm tra `concat == content`; (6) tính `source_hash`.
- **Kết quả:** đoạn nguồn phủ kín 100%; nếu bất biến vẫn sai (lỗi lập trình) thì từ chối lưu và cảnh báo P1. Xem `act-phu-kin-van-ban.puml`.

---

<a id="uc-0502"></a>
## UC-05.02 Quản lý bản nháp

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Editor |
| Mô tả | Làm việc với nhiều bản nháp storyboard của một chương |
| Tiền điều kiện | Chương có ≥ 1 bản nháp |
| Hậu điều kiện | **Thành công:** đúng một bản nháp hiện hành (BR-07) |
| Kích hoạt | Mở danh sách bản nháp trong `?v=storyboard:<chapterId>` |
| Quan hệ | được mở rộng bởi UC-05.02a..c |
| Truy vết | FR-BOK-02 |

**Luồng chính**
1. Editor mở danh sách bản nháp (tên, loại, số shot, ngày, nhãn "Current").
2. Editor chọn một bản nháp để xem hoặc thực hiện use case con.

### UC-05.02a Đổi tên / nhân bản / xóa
<a id="uc-0502a"></a>
- **Loại:** extend. **Các bước:** đổi tên; nhân bản (sao chép shot, không sao chép ảnh/thuyết minh, các shot trỏ cùng tư liệu nếu hash khớp); xóa (xác nhận, không cho xóa bản hiện hành). **Kết quả:** danh sách bản nháp cập nhật.

### UC-05.02b So sánh hai bản nháp
<a id="uc-0502b"></a>
- **Loại:** extend. **Các bước:** chọn hai bản; hệ thống hiển thị song song ranh giới đoạn nguồn, số shot, brief. **Kết quả:** Editor thấy khác biệt, không thay đổi dữ liệu.

### UC-05.02c Đặt bản nháp hiện hành
<a id="uc-0502c"></a>
- **Loại:** extend. **Các bước:** "Set as current"; hệ thống cập nhật `chapters.current_storyboard_id`; các shot chưa có tư liệu cần sinh (UC-05.07c); timeline của chương được đồng bộ (UC-06.15). **Kết quả:** bản nháp mới cấp dữ liệu cho tư liệu và timeline.

---

<a id="uc-0503"></a>
## UC-05.03 Chia lại shot (nhiều / ít hơn)

| Mục | Nội dung |
|---|---|
| Tác nhân chính / phụ | Editor / LLM |
| Mô tả | Tạo bản nháp mới với nhiều shot hơn (mỗi nhịp truyện một ảnh) hoặc ít hơn |
| Tiền điều kiện | Chương có văn bản |
| Hậu điều kiện | **Thành công:** bản nháp mới (`RESPLIT_MORE`/`RESPLIT_FEWER`), bản cũ giữ nguyên |
| Kích hoạt | "Re-split shots" |
| Quan hệ | include UC-05.01a |
| Truy vết | FR-BOK-03 |

**Luồng chính**
1. Editor chọn "Nhiều hơn" hoặc "Ít hơn".
2. Hệ thống chạy UC-05.01 bước 1–6 với tham số tương ứng, tạo bản nháp mới (chưa hiện hành).
3. Editor so sánh (UC-05.02b) rồi quyết định có đặt làm hiện hành (UC-05.02c) hay không.

---

<a id="uc-0504"></a>
## UC-05.04 Thiết lập Chapter rules

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Editor |
| Mô tả | Thêm chỉ dẫn cố định cho chương mà AI tuân theo khi viết brief ảnh |
| Tiền điều kiện | Chương tồn tại |
| Hậu điều kiện | **Thành công:** `chapter_rules` cập nhật; áp cho các lần tạo/viết lại brief sau |
| Kích hoạt | "Chapter rules · show" |
| Truy vết | FR-BOK-04; BR-08 |

**Luồng chính**
1. Editor mở Chapter rules, thêm/sửa/xóa/sắp xếp chỉ dẫn.
2. Hệ thống lưu và gợi ý "Re-direct" (UC-05.05) để áp lên các shot hiện có.

---

<a id="uc-0505"></a>
## UC-05.05 Chỉ đạo lại cả chương (Re-direct)

| Mục | Nội dung |
|---|---|
| Tác nhân chính / phụ | Editor / LLM |
| Mô tả | AI viết lại brief minh họa của mọi shot; **đoạn nguồn giữ nguyên** |
| Tiền điều kiện | Có bản nháp hiện hành |
| Hậu điều kiện | **Thành công:** brief mọi shot được cập nhật (version tăng); ảnh cũ giữ nguyên đến khi sinh lại |
| Kích hoạt | "Re-direct" |
| Truy vết | FR-BOK-07 |

**Luồng chính**
1. Editor tùy chọn nhập ghi chú, bấm "Re-direct".
2. Job `REDIRECT_CHAPTER`: LLM viết lại brief theo rules, tài sản, timeline.
3. Hệ thống cập nhật brief, đánh dấu shot "brief mới, ảnh cũ"; gợi ý sinh lại ảnh (UC-05.09) kèm giá.

---

<a id="uc-0506"></a>
## UC-05.06 Biên tập shot

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Editor |
| Mô tả | Chỉnh nội dung minh họa và cấu trúc của từng shot |
| Tiền điều kiện | Bản nháp tồn tại |
| Hậu điều kiện | **Thành công:** shot cập nhật (If-Match); phủ kín vẫn 100% |
| Kích hoạt | Chọn một shot trong Storyboard |
| Quan hệ | được mở rộng bởi UC-05.06a..f |
| Truy vết | FR-BOK-05, 06 |

**Luồng chính**
1. Editor chọn shot; hệ thống hiển thị các trường minh họa và đoạn nguồn (chỉ đọc).
2. Editor thực hiện một use case con; hệ thống lưu.

**Luồng thay thế / ngoại lệ**
- **2a.** `409`: UC-02.10.

### UC-05.06a Sửa brief, thời điểm, caption
<a id="uc-0506a"></a>
- **Loại:** extend. **Các bước:** sửa title, focus, brief (7 trường), thời điểm, ngày, caption. **Kết quả:** shot cập nhật; ảnh hiện tại được đánh dấu "brief đã đổi".

### UC-05.06b Gắn cast / item / location
<a id="uc-0506b"></a>
- **Loại:** extend. **Các bước:** thêm/gỡ tài sản cho shot (tối đa 1 location). **Kết quả:** ảnh tham chiếu tương ứng được dùng ở lần sinh sau.

### UC-05.06c Tách / gộp / xóa shot
<a id="uc-0506c"></a>
- **Loại:** extend; include UC-05.01a. **Các bước:** *Tách* tại một ranh giới câu → 2 shot; *Gộp* với shot trên/dưới → đoạn nguồn nối lại; *Xóa* → đoạn nguồn gộp vào shot liền trước (hoặc liền sau nếu là shot đầu). **Kết quả:** phủ kín vẫn 100%; shot mới cần sinh tư liệu; timeline đồng bộ (UC-06.15).

### UC-05.06d Dời ranh giới đoạn nguồn
<a id="uc-0506d"></a>
- **Loại:** extend; include UC-05.01a. **Các bước:** kéo ranh giới giữa hai shot liền kề theo từng câu (◀ ▶). **Kết quả:** hai shot đổi đoạn nguồn; thuyết minh của hai shot `OUTDATED`.

### UC-05.06e AI viết lại brief một shot
<a id="uc-0506e"></a>
- **Loại:** extend. **Tác nhân phụ:** LLM. **Các bước:** nhập ghi chú ("trời tối hơn"); job `REWRITE_SHOT` chỉ cập nhật brief của shot. **Kết quả:** brief mới; đoạn nguồn không đổi.

### UC-05.06f Tự khớp tên với tài sản
<a id="uc-0506f"></a>
- **Loại:** extend. **Các bước:** "Scan the chapter text and auto-match"; hệ thống khớp `raw_name` với tên/bí danh tài sản. **Kết quả:** các tham chiếu "chưa liên kết" được liên kết khi khớp.

---

## Phần B — Sinh tư liệu: ảnh + thuyết minh

<a id="uc-0507"></a>
## UC-05.07 Sinh tư liệu chương

| Mục | Nội dung |
|---|---|
| Tác nhân chính / phụ | Editor / LLM, Image Provider, TTS, STT/Aligner |
| Mô tả | Bước 4 của luồng: một thao tác sinh **ảnh + thuyết minh nguyên văn** cho mọi shot của một hoặc nhiều chương |
| Tiền điều kiện | Chương có văn bản; dự án có style; đã chọn giọng đọc (UC-05.11); khuyến nghị tài sản đã có ảnh tham chiếu |
| Hậu điều kiện | **Thành công:** mọi shot có ảnh `DONE` và thuyết minh `VERIFIED`/`ACCEPTED`; chương "Sẵn sàng dựng"; có bản nháp timeline (UC-06.01a). **Tối thiểu:** phần thành công được giữ; credit phần lỗi được hoàn |
| Kích hoạt | Bấm "Sinh tư liệu" |
| Quan hệ | include UC-05.07a, UC-05.09, UC-05.13, UC-05.17; được mở rộng bởi UC-05.07b, UC-05.07c |
| Truy vết | FR-MED-01..05; BR-11; seq-sinh-tu-lieu |

**Luồng chính**
1. Editor chọn một hoặc nhiều chương, bấm "Sinh tư liệu".
2. Hệ thống ước tính số shot (theo storyboard hiện có hoặc độ dài chương) và hiện **một** báo giá tổng: ảnh × giá ảnh + ký tự × giá TTS.
3. Editor xác nhận; hệ thống thực hiện **UC-05.17** (giữ credit) và tạo job cha `GENERATE_MEDIA_CHAPTER`.
4. Chương chưa có storyboard hiện hành: thực hiện **UC-05.07a**.
5. Với mỗi shot, chạy song song **UC-05.09** (ảnh) và **UC-05.13** (thuyết minh).
6. Mọi shot đạt: hệ thống đánh dấu chương "Sẵn sàng dựng", dựng bản nháp timeline, thông báo `chapter.media-ready`.

**Luồng thay thế / ngoại lệ**
- **3a.** Không đủ credit: `402`; gợi ý nạp credit (UC-09.03) hoặc chọn ít chương hơn.
- **4a.** Số shot thực tế khác ước tính: điều chỉnh phần credit đã giữ (giữ thêm hoặc trả lại).
- **5a.** Còn ảnh lỗi hoặc thuyết minh `NEEDS_REVIEW`: chương "Cần xử lý", liệt kê shot; Editor xử lý qua UC-05.10, UC-05.14 hoặc UC-05.07c.
- **\*a.** Editor sửa văn bản chương trong lúc job chạy: chương bị khóa (BR-12) đến khi job xong.

### UC-05.07a Storyboard tự động
<a id="uc-0507a"></a>
- **Loại:** include (bước 4). **Các bước:** chạy UC-05.01 với thời lượng mục tiêu của dự án, đặt bản nháp làm hiện hành. **Kết quả:** chương có N shot phủ kín.

### UC-05.07b Xem tiến độ theo shot
<a id="uc-0507b"></a>
- **Loại:** extend. **Các bước:** bảng tiến độ cập nhật qua SSE `media.progress`: mỗi shot hai cột Ảnh / Thuyết minh với trạng thái. **Kết quả:** Editor biết shot nào xong, lỗi, cần duyệt.

### UC-05.07c Sinh lại phần thiếu / lỗi
<a id="uc-0507c"></a>
- **Loại:** extend. **Các bước:** chọn phạm vi (chỉ phần thiếu, chỉ lỗi, chỉ `OUTDATED`; chỉ ảnh hoặc chỉ thuyết minh); hiện giá; xác nhận; chạy lại bước 5 cho các shot đó. **Kết quả:** chương tiến tới "Sẵn sàng dựng"; timeline được đồng bộ.

---

<a id="uc-0508"></a>
## UC-05.08 Xem Tư liệu dự án (media bin)

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Editor |
| Mô tả | Xem toàn bộ ảnh và thuyết minh theo chương → shot; đầu vào của trình chỉnh sửa |
| Tiền điều kiện | Là thành viên dự án |
| Hậu điều kiện | **Thành công:** hiển thị tư liệu và trạng thái |
| Kích hoạt | Mở "Tư liệu" |
| Truy vết | FR-MED-03 |

**Luồng chính**
1. Editor mở Tư liệu dự án.
2. Hệ thống liệt kê chương (trạng thái), mỗi shot: ảnh hiện hành, nút nghe thuyết minh, đoạn văn nguồn, thời lượng, WER, trạng thái.
3. Editor lọc theo trạng thái ("Cần xử lý", `OUTDATED`) hoặc mở shot để sửa (UC-05.10, UC-05.14).

---

<a id="uc-0509"></a>
## UC-05.09 Sinh ảnh shot

| Mục | Nội dung |
|---|---|
| Tác nhân chính / phụ | Editor (hoặc UC-05.07) / Image Provider |
| Mô tả | Sinh ảnh minh họa cho một shot, giữ nhất quán nhân vật bằng ảnh tham chiếu |
| Tiền điều kiện | Shot có brief; đủ credit |
| Hậu điều kiện | **Thành công:** Illustration phiên bản mới `DONE`, đặt làm hiện hành; credit trừ. **Tối thiểu:** lỗi thì hoàn credit |
| Kích hoạt | "Generate" trên shot, hoặc UC-05.07 |
| Quan hệ | được include bởi UC-05.07; include UC-05.17 |
| Truy vết | FR-BOK-09; BR-08; seq-storyboard-sinh-anh |

**Luồng chính**
1. Hệ thống thực hiện UC-05.17 (giữ 1 credit) và tạo job `GENERATE_SHOT_IMAGE`.
2. Worker ghép prompt theo BR-08: style → Art Direction → Visual Rules → Chapter rules → brief + facts; đính kèm ảnh tham chiếu cast/location/item; tỷ lệ theo khung hình dự án.
3. Moderation đầu vào; gọi Image Provider (retry tối đa 3 lần).
4. Moderation đầu ra; lưu ảnh; tạo Illustration; trừ credit; phát `illustration.ready`.

**Luồng thay thế / ngoại lệ**
- **3a.** Lỗi sau 3 lần thử hoặc vi phạm chính sách: Illustration `FAILED`, hoàn credit, shot có nút "Retry".

---

<a id="uc-0510"></a>
## UC-05.10 Sửa ảnh

| Mục | Nội dung |
|---|---|
| Tác nhân chính / phụ | Editor / Image Provider |
| Mô tả | Chỉnh ảnh shot mà không phải sinh lại từ đầu |
| Tiền điều kiện | Shot có ảnh (hoặc ảnh lỗi để Retry); đủ credit |
| Hậu điều kiện | **Thành công:** Illustration phiên bản mới (giữ phiên bản cũ) |
| Kích hoạt | "Edit" trên ảnh |
| Quan hệ | include UC-05.17; được mở rộng bởi UC-05.10a..c |
| Truy vết | FR-BOK-10 |

**Luồng chính**
1. Editor mở ảnh và chọn cách sửa (use case con).
2. Hệ thống hiện giá (1 credit), giữ credit, gửi yêu cầu.
3. Hệ thống lưu ảnh mới làm hiện hành, trừ credit; timeline đồng bộ ảnh mới (UC-06.15).

### UC-05.10a Describe → Edit
<a id="uc-0510a"></a>
- **Loại:** extend. **Các bước:** mô tả thay đổi ("đổi sang ánh chiều"); job `EDIT_IMAGE` gửi ảnh + hướng dẫn. **Kết quả:** ảnh đã chỉnh.

### UC-05.10b Fix a spot (tô vùng)
<a id="uc-0510b"></a>
- **Loại:** extend. **Các bước:** tô mask lên vùng cần sửa, mô tả; job `INPAINT_IMAGE`. **Kết quả:** chỉ vùng được tô thay đổi.

### UC-05.10c Khôi phục phiên bản ảnh
<a id="uc-0510c"></a>
- **Loại:** extend. **Các bước:** mở lịch sử ảnh, chọn phiên bản, "Make current". **Kết quả:** phiên bản cũ thành hiện hành; **không tốn credit**.

---

<a id="uc-0511"></a>
## UC-05.11 Cài đặt thuyết minh

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Editor |
| Mô tả | Chọn ngôn ngữ, giọng đọc, tốc độ, cao độ, khoảng nghỉ, ngưỡng WER |
| Tiền điều kiện | Là thành viên dự án |
| Hậu điều kiện | **Thành công:** `narration_settings` cập nhật; áp cho các lần sinh sau |
| Kích hoạt | Mở "Cài đặt thuyết minh", hoặc điểm duyệt UC-07.05 |
| Quan hệ | được mở rộng bởi UC-05.11a |
| Truy vết | FR-NAR-01 |

**Luồng chính**
1. Editor chọn ngôn ngữ (Auto hoặc cụ thể) và giọng trong danh mục.
2. Editor chỉnh tốc độ (0,8–1,3×), cao độ, nghỉ câu/đoạn, ngưỡng WER (0,01–0,10).
3. Hệ thống lưu.

**Luồng thay thế / ngoại lệ**
- **3a.** Đổi giọng khi đã có thuyết minh: hỏi có sinh lại toàn bộ không (hiện giá); nếu không thì chỉ áp cho shot sinh mới.

### UC-05.11a Nghe thử giọng
<a id="uc-0511a"></a>
- **Loại:** extend. **Tác nhân phụ:** TTS. **Các bước:** phát audio mẫu có sẵn của giọng, hoặc đọc thử một câu trong truyện (≤ 200 ký tự, miễn phí, giới hạn tần suất). **Kết quả:** Editor nghe trước khi chọn.

---

<a id="uc-0512"></a>
## UC-05.12 Quản lý từ điển phát âm

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Editor |
| Mô tả | Khai báo cách đọc tên riêng, từ mượn, từ Hán Việt; **chỉ ảnh hưởng audio, không đổi chữ** |
| Tiền điều kiện | Là thành viên dự án |
| Hậu điều kiện | **Thành công:** `pronunciation_entries` cập nhật; dùng ở lần sinh thuyết minh sau |
| Kích hoạt | Mở "Từ điển phát âm" hoặc từ một từ bị đánh dấu lệch (UC-05.14) |
| Truy vết | FR-NAR-04; BR-19 |

**Luồng chính**
1. Editor thêm mục: từ viết, cách đọc, kiểu (alias / phoneme), phân biệt hoa thường.
2. Editor nghe thử (UC-05.11a với câu chứa từ).
3. Hệ thống lưu; liệt kê các shot chứa từ này và gợi ý sinh lại thuyết minh (UC-05.07c).

**Luồng thay thế / ngoại lệ**
- **1a.** Vượt 500 mục hoặc trùng từ viết: báo lỗi.

---

<a id="uc-0513"></a>
## UC-05.13 Sinh thuyết minh nguyên văn

| Mục | Nội dung |
|---|---|
| Tác nhân chính / phụ | Editor (hoặc UC-05.07) / TTS, STT/Aligner |
| Mô tả | Tạo audio đọc **đúng từng chữ** đoạn nguồn của shot và kiểm chứng |
| Tiền điều kiện | Shot có đoạn nguồn; đã chọn giọng; đủ credit |
| Hậu điều kiện | **Thành công:** Narration `VERIFIED` hoặc `NEEDS_REVIEW` kèm `word_timings`, WER. **Tối thiểu:** không có audio nào sinh từ văn bản khác đoạn nguồn; lỗi thì hoàn credit |
| Kích hoạt | UC-05.07, hoặc "Sinh lại thuyết minh" trên shot |
| Quan hệ | include UC-05.13a, UC-05.13b, UC-05.13c, UC-05.17 |
| Truy vết | FR-NAR-02, 03, 06, 07; BR-19, BR-22; ADR-12; seq-thuyet-minh-nguyen-van |

**Luồng chính**
1. Hệ thống giữ credit theo số ký tự (UC-05.17), tạo job `NARRATE_SEGMENT`.
2. Thực hiện **UC-05.13a**.
3. Thực hiện **UC-05.13b**.
4. Gọi TTS (chia theo câu nếu vượt giới hạn, rồi nối audio); lưu audio.
5. Thực hiện **UC-05.13c**.
6. Lưu Narration (phiên bản mới, đặt làm hiện hành), trừ credit, phát `narration.updated`.

**Luồng thay thế / ngoại lệ**
- **2a.** Hash không khớp: `OUTDATED`, hoàn credit, dừng.
- **4a.** TTS lỗi hoặc vi phạm chính sách: retry; vẫn lỗi thì `FAILED`, hoàn credit. Văn bản **không** được tự sửa để vượt bộ lọc (BR-18).

### UC-05.13a Cắt đoạn nguồn & kiểm tra hash
<a id="uc-0513a"></a>
- **Loại:** include. **Các bước:** `text = chapter.content[source_start:source_end]`; so `sha256(text)` với `shot.source_hash`. **Kết quả:** văn bản nguồn chính xác, hoặc dừng vì `OUTDATED`. Không có đường nào để client gửi văn bản đọc.

### UC-05.13b Chuẩn hóa phát âm (SSML)
<a id="uc-0513b"></a>
- **Loại:** include. **Các bước:** áp quy tắc tất định lên *bản đọc* (bỏ ký hiệu markdown, đọc số/ngày/đơn vị, ngắt nghỉ theo dấu câu), áp từ điển phát âm bằng SSML alias/phoneme, ghi log biến đổi; kiểm tra ngược: bỏ thẻ SSML và áp ngược alias thì phải ra đúng `text`. **Kết quả:** SSML không thêm, bớt hay đổi từ.

### UC-05.13c Kiểm chứng lời đọc (WER)
<a id="uc-0513c"></a>
- **Loại:** include. **Tác nhân phụ:** STT/Aligner. **Các bước:** forced alignment audio với `text` → `word_timings`; STT chép lại audio; chuẩn hóa hai phía (chữ thường, bỏ dấu câu, giữ dấu thanh); tính WER và vị trí lệch. **Kết quả:** `VERIFIED` nếu WER ≤ ngưỡng, ngược lại `NEEDS_REVIEW` kèm `mismatches`.

---

<a id="uc-0514"></a>
## UC-05.14 Duyệt shot NEEDS_REVIEW

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Editor |
| Mô tả | Xử lý thuyết minh có WER vượt ngưỡng |
| Tiền điều kiện | Có shot `NEEDS_REVIEW` |
| Hậu điều kiện | **Thành công:** shot thành `VERIFIED` (sau khi sinh lại) hoặc `ACCEPTED` |
| Kích hoạt | Mở shot từ danh sách "Cần xử lý" hoặc điểm duyệt UC-07.06 |
| Quan hệ | được mở rộng bởi UC-05.14a |
| Truy vết | FR-NAR-07, 08; BR-23 |

**Luồng chính**
1. Editor mở shot; hệ thống phát audio, tô đỏ các từ lệch (mong đợi / nghe được).
2. Editor thêm cách đọc vào từ điển (UC-05.12) và/hoặc đổi tốc độ/giọng.
3. Editor bấm "Sinh lại" (UC-05.13, hiện giá).
4. Kết quả `VERIFIED`: shot đạt.

**Luồng thay thế / ngoại lệ**
- **2a.** Editor nghe thấy audio đúng (STT nhận sai): chọn UC-05.14a.

### UC-05.14a Chấp nhận thủ công
<a id="uc-0514a"></a>
- **Loại:** extend. **Các bước:** Editor xác nhận "Tôi đã nghe và lời đọc đúng nguyên văn"; hệ thống đặt `ACCEPTED`, lưu `accepted_by`, `accepted_at`. **Kết quả:** shot đủ điều kiện xuất (BR-23).

---

<a id="uc-0515"></a>
## UC-05.15 Gán giọng theo nhân vật

| Mục | Nội dung |
|---|---|
| Tác nhân chính / phụ | Editor / LLM |
| Mô tả | Đọc lời thoại trong ngoặc kép bằng giọng riêng của từng nhân vật; **nội dung vẫn nguyên văn** |
| Tiền điều kiện | Gói Creator trở lên; có nhân vật trong Story Assets |
| Hậu điều kiện | **Thành công:** `character_voices` cập nhật; `narration_settings.multi_voice = true` |
| Kích hoạt | Mở "Giọng nhân vật" |
| Truy vết | FR-NAR-05 (C) |

**Luồng chính**
1. Editor bật đa giọng và gán giọng cho từng nhân vật.
2. Hệ thống dùng LLM nhận diện người nói của từng câu thoại; Editor duyệt bảng nhận diện.
3. Ở lần sinh thuyết minh sau, câu thoại được đọc bằng giọng nhân vật, phần dẫn bằng giọng kể.

**Luồng thay thế / ngoại lệ**
- **2a.** Không xác định được người nói: dùng giọng kể.

---

<a id="uc-0516"></a>
## UC-05.16 Tải ZIP ảnh

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Editor |
| Mô tả | Tải ảnh minh họa hiện hành theo chương hoặc cả dự án |
| Tiền điều kiện | Có ít nhất một ảnh `DONE` |
| Hậu điều kiện | **Thành công:** link tải ZIP (hết hạn 15 phút) |
| Kích hoạt | "Tải ZIP ảnh" |
| Truy vết | FR-BOK-16 |

**Luồng chính**
1. Editor chọn phạm vi (chương / dự án).
2. Hệ thống tạo job `EXPORT_ZIP` (miễn phí), đặt tên file `ch<NN>-shot<NN>.png`.
3. Hệ thống cung cấp link tải.

---

<a id="uc-0517"></a>
## UC-05.17 Giữ / trừ / hoàn credit

| Mục | Nội dung |
|---|---|
| Tác nhân chính | Hệ thống (được include bởi các use case tốn phí) |
| Mức | Chức năng con |
| Mô tả | Bảo đảm credit chính xác cho mọi job AI: giữ khi tạo job, trừ khi thành công, hoàn khi thất bại |
| Tiền điều kiện | Có giá theo `price_rules` hiệu lực |
| Hậu điều kiện | **Thành công:** ledger có HOLD và đúng một trong CAPTURE / RELEASE cho mỗi job. **Tối thiểu:** không bao giờ trừ credit cho job thất bại |
| Kích hoạt | Tạo job tốn phí |
| Truy vết | BR-01, BR-02, BR-03; CR-01..05; IC-04, IC-05; act-giu-tru-credit |

**Luồng chính**
1. Hệ thống kiểm tra `Idempotency-Key`; trùng thì trả kết quả cũ.
2. Tính giá, khóa `credit_balances` (`FOR UPDATE`) của **người kích hoạt** (BR-03).
3. Giữ theo thứ tự bucket SUBSCRIPTION → BONUS → PACK; ghi ledger HOLD; tạo job + outbox trong cùng giao dịch.
4. Khi job thành công: CAPTURE. Khi thất bại, bị hủy hoặc vi phạm chính sách: RELEASE về đúng bucket.

**Luồng thay thế / ngoại lệ**
- **2a.** Không đủ credit: `402 INSUFFICIENT_CREDITS` kèm số còn thiếu.
- **\*a.** Job mất heartbeat > 10 phút: reconciler đặt `FAILED` và RELEASE.
