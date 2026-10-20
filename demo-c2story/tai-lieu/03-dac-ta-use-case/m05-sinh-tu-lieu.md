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

### UC-05.01a Tách câu & kiểm tra phủ kín
<a id="uc-0501a"></a>

| Mục | Nội dung |
|---|---|
| Loại | include của UC-05.01, UC-05.03, UC-05.06c, UC-05.06d |
| Tác nhân | Hệ thống (`CoverageValidator`) |
| Mô tả | Đổi chỉ số câu do LLM hoặc Editor đưa ra thành ranh giới ký tự và bảo đảm các shot phủ kín **100%** văn bản chương (IC-08, BR-20) |
| Tiền điều kiện | Chương có văn bản; có danh sách shot với chỉ số câu (từ LLM ở UC-05.01 bước 3, hoặc từ thao tác của Editor ở UC-05.03, UC-05.06c, UC-05.06d) |
| Hậu điều kiện | **Thành công:** các shot phủ kín chương, không chồng lấn, không sót; mỗi shot có `source_start`, `source_end`, `source_hash`. **Tối thiểu:** không lưu bản nháp vi phạm phủ kín |
| Kích hoạt | UC-05.01 bước 4; mỗi thao tác đổi ranh giới shot |
| Truy vết | BR-20; IC-08; NFR-INT-01; ADR-11; API 2.5 `…/storyboards/{did}/coverage`; `so-do/05-hoat-dong/act-phu-kin-van-ban.puml` |

**Luồng chính**
1. Hệ thống lấy bảng câu của chương (tách tất định, mỗi câu có offset `[start, end)`).
2. Hệ thống đổi `startSentence`, `endSentence` của từng shot thành `source_start`, `source_end`.
3. Hệ thống sắp shot theo thứ tự, kẹp chỉ số vào phạm vi hợp lệ và bỏ shot rỗng.
4. Khoảng hở giữa hai shot được gộp vào shot trước (khoảng hở ở đầu chương gộp vào shot đầu); phần chồng lấn được cắt theo shot sau.
5. Hệ thống dời mọi ranh giới về đầu câu; khoảng trắng giữa các câu gán cho shot trước.
6. Hệ thống kiểm tra IC-08: `shot[0].source_start = 0`, `shot[i].source_end = shot[i+1].source_start`, `shot[cuối].source_end` bằng độ dài chương, và `concat(đoạn nguồn) == chapter.content` (so sánh byte).
7. Hệ thống tính `source_hash` (sha256) từng đoạn nguồn và ghi `boundary_fixes` (số ranh giới đã sửa ở bước 3–5).

**Luồng thay thế / ngoại lệ**
- **6a.** Bất biến vẫn sai sau khi sửa (lỗi lập trình): từ chối lưu, không ghi gì, phát cảnh báo P1.
- **7a.** `boundary_fixes` vượt 20% số ranh giới: lưu bản nháp kèm Director note cảnh báo chất lượng và gợi ý tạo lại (UC-05.01 nhánh 4a).
- ***a.** Nội dung chương đổi trong lúc xử lý (phiên bản khác): hủy kết quả và chạy lại từ bước 1.
- **3a.** Bỏ shot rỗng làm số shot giảm: chấp nhận; số shot cuối cùng nằm trong 1–40 (08 §5).

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

| Mục | Nội dung |
|---|---|
| Loại | extend của UC-05.02 |
| Tác nhân | Editor |
| Mô tả | Đổi tên, nhân bản hoặc xóa một bản nháp storyboard của chương |
| Tiền điều kiện | Chương có bản nháp; chương không bị khóa (BR-12) |
| Hậu điều kiện | **Thành công:** danh sách bản nháp cập nhật; vẫn đúng một bản hiện hành (BR-07). **Tối thiểu:** không bao giờ xóa bản hiện hành |
| Kích hoạt | Menu "…" của một bản nháp trong danh sách UC-05.02 |
| Truy vết | BR-07, BR-12; API 2.5 `PATCH/DELETE …/storyboards/{did}`, `:duplicate` |

**Luồng chính**
1. Editor chọn một bản nháp và một hành động.
2. *Đổi tên:* Editor nhập tên mới (không rỗng); hệ thống cập nhật `name`.
3. *Nhân bản:* hệ thống tạo bản nháp `kind = DUPLICATE` có cùng các shot (ranh giới, brief, tham chiếu tài sản). Không sao chép file ảnh hay thuyết minh; shot mới trỏ tới cùng tư liệu hiện có khi `source_hash` khớp.
4. *Xóa:* hệ thống yêu cầu xác nhận, rồi xóa bản nháp cùng các shot của nó.
5. Danh sách bản nháp được làm mới.

**Luồng thay thế / ngoại lệ**
- **4a.** Xóa bản đang hiện hành: `422 PRECONDITION_FAILED_BUSINESS`, gợi ý đặt bản khác làm hiện hành trước (UC-05.02c).
- **1a.** Chương đang bị khóa bởi job: `423 RESOURCE_LOCKED`.

### UC-05.02b So sánh hai bản nháp
<a id="uc-0502b"></a>

| Mục | Nội dung |
|---|---|
| Loại | extend của UC-05.02 |
| Tác nhân | Editor |
| Mô tả | Xem song song hai bản nháp của cùng một chương để quyết định bản nào dùng |
| Tiền điều kiện | Chương có ít nhất hai bản nháp |
| Hậu điều kiện | **Thành công:** Editor thấy khác biệt giữa hai bản. **Tối thiểu:** không thay đổi dữ liệu |
| Kích hoạt | Chọn hai bản nháp và bấm "Compare" |
| Truy vết | FR-BOK-02; API 2.5 `GET …/storyboards/{did}/shots` |

**Luồng chính**
1. Editor chọn hai bản nháp A và B của cùng chương.
2. Hệ thống tải shot của cả hai bản.
3. Hệ thống hiển thị hai cột song song, căn theo vị trí đoạn nguồn: số shot, ranh giới, tiêu đề và brief của từng shot.
4. Hệ thống đánh dấu nơi hai bản khác nhau (shot được tách hoặc gộp, ranh giới lệch, brief khác).
5. Editor có thể bấm "Đặt làm hiện hành" ngay trên một bản (UC-05.02c).

**Luồng thay thế / ngoại lệ**
- **1a.** Chọn cùng một bản hai lần hoặc chương chỉ có một bản nháp: vô hiệu hóa nút so sánh.

### UC-05.02c Đặt bản nháp hiện hành
<a id="uc-0502c"></a>

| Mục | Nội dung |
|---|---|
| Loại | extend của UC-05.02 |
| Tác nhân | Editor |
| Mô tả | Chọn bản nháp làm storyboard hiện hành của chương; tư liệu và timeline được cập nhật theo |
| Tiền điều kiện | Bản nháp thuộc chương và chưa phải bản hiện hành; chương không bị khóa (BR-12) |
| Hậu điều kiện | **Thành công:** `chapters.current_storyboard_id` trỏ bản mới (đúng một bản hiện hành, BR-07, IC-03). **Tối thiểu:** lỗi thì giữ nguyên bản hiện hành cũ |
| Kích hoạt | Bấm "Set as current" |
| Truy vết | BR-07, BR-12; IC-03; UC-06.15; API 2.5 `POST …/storyboards/{did}:set-current` |

**Luồng chính**
1. Editor chọn một bản nháp và bấm "Set as current".
2. Nếu chương đã có timeline được chỉnh sửa, hệ thống cảnh báo các clip sẽ được đồng bộ theo bản mới và hỏi xác nhận.
3. Hệ thống cập nhật `chapters.current_storyboard_id` trong một giao dịch; bản cũ thôi là hiện hành.
4. Các shot của bản mới chưa có ảnh hoặc thuyết minh được đánh dấu cần sinh; hệ thống gợi ý UC-05.07c kèm giá. Trạng thái media của chương được tính lại theo bản mới.
5. Hệ thống thực hiện UC-06.15 để đồng bộ timeline và phát `shot.updated`, `timeline.updated`.

**Luồng thay thế / ngoại lệ**
- **2a.** Editor không xác nhận: không đổi gì.
- **3a.** Chương đang bị job khóa: `423 RESOURCE_LOCKED`.
- **3b.** Có xung đột phiên bản: `409`, xử lý theo UC-02.10.

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

| Mục | Nội dung |
|---|---|
| Loại | extend của UC-05.06 |
| Tác nhân | Editor |
| Mô tả | Sửa các trường **minh họa** của shot; đoạn nguồn (văn bản truyện) chỉ đọc |
| Tiền điều kiện | Shot thuộc bản nháp; Editor đã chọn shot |
| Hậu điều kiện | **Thành công:** shot được lưu với `version` mới. **Tối thiểu:** văn bản truyện và thuyết minh không bị đổi |
| Kích hoạt | Sửa một trường trong panel shot |
| Truy vết | FR-BOK-05, FR-BOK-06; BR-21; 08 §5; API 2.5 `PATCH …/shots/{shid}` (If-Match) |

**Luồng chính**
1. Editor sửa một hoặc nhiều trường: tiêu đề, focus, 7 trường của brief (Subject, Environment, Composition, Camera, Lighting, Mood, Details), thời điểm trong ngày, ngày trong truyện, caption (≤ 300 ký tự).
2. Hệ thống gửi `PATCH` kèm `If-Match`, kiểm tra schema và giới hạn độ dài.
3. Hệ thống ghi shot, tăng `version`, phát `shot.updated`.
4. Nếu brief đổi, ảnh hiện tại được đánh dấu "brief đã đổi" (`illustrations.shot_version < shots.version`) và hệ thống gợi ý sinh lại ảnh (UC-05.09) kèm giá.

**Luồng thay thế / ngoại lệ**
- **2a.** Caption dài hơn 300 ký tự hoặc sai schema: `400 VALIDATION_ERROR`.
- **3a.** `409 VERSION_CONFLICT`: xử lý theo UC-02.10.
- ***a.** Editor cố sửa đoạn nguồn: trường chỉ đọc, hướng dẫn sửa văn bản chương trong Workspace (UC-03.02).

### UC-05.06b Gắn cast / item / location
<a id="uc-0506b"></a>

| Mục | Nội dung |
|---|---|
| Loại | extend của UC-05.06 |
| Tác nhân | Editor |
| Mô tả | Chọn nhân vật, đạo cụ và địa điểm xuất hiện trong shot để ảnh tham chiếu tương ứng được đưa vào prompt |
| Tiền điều kiện | Shot thuộc bản nháp |
| Hậu điều kiện | **Thành công:** `shot_asset_refs` của shot được cập nhật (vai trò `CAST`, `ITEM`, `LOCATION`). **Tối thiểu:** ảnh hiện có không đổi |
| Kích hoạt | Sửa mục Cast / Items / Location trong panel shot |
| Truy vết | FR-BOK-05, FR-BOK-08; BR-16; 04 §3.4 `shot_asset_refs` |

**Luồng chính**
1. Editor thêm tài sản vào Cast, Items hoặc Location bằng cách chọn từ danh sách Story Assets, hoặc gỡ tài sản đã gắn.
2. Hệ thống kiểm tra mỗi shot có tối đa 1 location.
3. Hệ thống lưu `shot_asset_refs` và tăng `version` của shot.
4. Ở lần sinh ảnh sau, UC-05.09 bước 2 đính kèm ảnh tham chiếu của các tài sản đã gắn.

**Luồng thay thế / ngoại lệ**
- **1a.** Editor nhập tên chưa có tài sản: lưu với `raw_name`, `story_asset_id = NULL`, hiện cảnh báo "chưa liên kết" kèm nút thêm tài sản (UC-04.02a) hoặc tự khớp (UC-05.06f).
- **2a.** Thêm location thứ hai: chặn, đề nghị thay location hiện có.
- **4a.** Tài sản chưa có ảnh tham chiếu: cảnh báo ảnh sinh ra có thể thiếu nhất quán, gợi ý UC-04.03.
- **3a.** `409`: xử lý theo UC-02.10.

### UC-05.06c Tách / gộp / xóa shot
<a id="uc-0506c"></a>

| Mục | Nội dung |
|---|---|
| Loại | extend của UC-05.06; include UC-05.01a |
| Tác nhân | Editor |
| Mô tả | Thay đổi cấu trúc storyboard bằng cách tách, gộp hoặc xóa shot mà văn bản chương luôn được phủ kín |
| Tiền điều kiện | Bản nháp tồn tại; chương không bị khóa (BR-12) |
| Hậu điều kiện | **Thành công:** các shot vẫn phủ kín 100% chương (IC-08); thuyết minh của shot bị đổi đoạn nguồn chuyển `OUTDATED`. **Tối thiểu:** lỗi thì giữ nguyên cấu trúc cũ |
| Kích hoạt | "Split here" giữa hai câu; "Merge up/down"; "Delete shot" |
| Truy vết | BR-06, BR-12, BR-20; IC-08, IC-09; 08 §5 (1–40 shot); API 2.5 `:split`, `:merge-up`, `:merge-down`, `DELETE …/shots/{shid}` |

**Luồng chính**
1. Editor chọn thao tác trên một shot.
2. *Tách:* Editor chọn một ranh giới giữa hai câu trong đoạn nguồn (`atSentence`); shot thành hai shot liền nhau.
3. *Gộp:* Editor chọn gộp với shot ngay trên hoặc ngay dưới; hai đoạn nguồn được nối lại theo thứ tự.
4. *Xóa:* hệ thống không xóa văn bản; đoạn nguồn của shot bị xóa được gộp vào shot liền trước (hoặc liền sau nếu là shot đầu tiên).
5. Hệ thống thực hiện **UC-05.01a** để kiểm tra phủ kín và tính lại `source_hash`.
6. Các thuyết minh của shot có đoạn nguồn đổi chuyển `OUTDATED` (IC-09); shot mới tạo ra chưa có ảnh và thuyết minh. Ảnh của các shot hiện có được giữ nguyên.
7. Hệ thống phát `shot.updated`, đồng bộ timeline (UC-06.15) và gợi ý UC-05.07c để sinh phần thiếu.

**Luồng thay thế / ngoại lệ**
- **2a.** Shot chỉ có một câu: không tách được (mỗi shot ≥ 1 câu).
- **2b.** Tách làm bản nháp vượt 40 shot: chặn.
- **4a.** Bản nháp chỉ còn một shot: không xóa được (phải phủ kín chương).
- **6a.** Chương đang bị khóa: `423 RESOURCE_LOCKED`.
- **6b.** `409`: xử lý theo UC-02.10.

### UC-05.06d Dời ranh giới đoạn nguồn
<a id="uc-0506d"></a>

| Mục | Nội dung |
|---|---|
| Loại | extend của UC-05.06; include UC-05.01a |
| Tác nhân | Editor |
| Mô tả | Dời ranh giới giữa hai shot kề nhau theo từng câu để đoạn nguồn chia hợp lý hơn |
| Tiền điều kiện | Hai shot liền kề trong cùng bản nháp; chương không bị khóa |
| Hậu điều kiện | **Thành công:** hai shot đổi đoạn nguồn, phủ kín vẫn 100%; thuyết minh của cả hai shot `OUTDATED`. **Tối thiểu:** lỗi thì giữ ranh giới cũ |
| Kích hoạt | Bấm ◀ hoặc ▶ ở ranh giới giữa hai shot |
| Truy vết | BR-06, BR-20; IC-08, IC-09; 08 §5; API 2.5 `POST …/storyboards/{did}:move-boundary` |

**Luồng chính**
1. Editor bấm ◀ hoặc ▶ ở ranh giới giữa shot trái và shot phải, mỗi lần dời một câu.
2. Giao diện xem trước câu nào chuyển sang shot nào và độ dài đọc mới của hai shot.
3. Editor xác nhận; hệ thống gọi `:move-boundary {leftShotId, rightShotId, deltaSentences}`.
4. Hệ thống thực hiện **UC-05.01a** và cập nhật `source_start`, `source_end`, `source_hash` của hai shot.
5. Thuyết minh của hai shot chuyển `OUTDATED`; ảnh được giữ nguyên (brief không đổi). Hệ thống phát `shot.updated` và đồng bộ timeline (UC-06.15).

**Luồng thay thế / ngoại lệ**
- **2a.** Dời làm một shot rỗng (không còn câu nào): chặn.
- **2b.** Đoạn nguồn mới của một shot đọc quá 30 giây (khoảng 450 ký tự tiếng Việt): cảnh báo, vẫn cho phép.
- **3a.** `409`: xử lý theo UC-02.10.
- **3b.** Chương đang bị khóa: `423 RESOURCE_LOCKED`.

### UC-05.06e Viết lại brief một shot bằng AI
<a id="uc-0506e"></a>

| Mục | Nội dung |
|---|---|
| Loại | extend của UC-05.06 |
| Tác nhân | Editor / LLM |
| Mô tả | Nhờ AI viết lại **brief minh họa** của một shot theo ghi chú; đoạn nguồn không bao giờ bị đụng tới |
| Tiền điều kiện | Shot thuộc bản nháp; chưa vượt giới hạn tần suất (ví dụ 60 lần mỗi giờ mỗi dự án) |
| Hậu điều kiện | **Thành công:** brief của shot được thay bằng bản mới. **Tối thiểu:** đoạn nguồn, caption và thuyết minh không đổi |
| Kích hoạt | Bấm "Rewrite this shot" |
| Truy vết | FR-BOK-06; BR-21; NFR-INT-02; 08 §3.2 (`REWRITE_SHOT`, 0 credit, có giới hạn tần suất); API 2.5 `POST …/shots/{shid}:rewrite` |

**Luồng chính**
1. Editor nhập ghi chú (ví dụ "trời tối hơn") và bấm gửi.
2. Hệ thống tạo job `REWRITE_SHOT` (không tốn credit).
3. Worker gửi LLM brief hiện tại, ghi chú, tài sản của shot, style, Art Direction và Visual Rules; đoạn nguồn chỉ được đưa vào làm ngữ cảnh đọc.
4. LLM trả brief mới theo schema 7 trường; hệ thống chỉ ghi vào trường `brief` (không có đường ghi vào đoạn nguồn).
5. Shot được cập nhật, `version` tăng; ảnh hiện tại được đánh dấu "brief đã đổi" và hệ thống gợi ý sinh lại ảnh (UC-05.09) kèm giá.

**Luồng thay thế / ngoại lệ**
- **2a.** Vượt giới hạn tần suất: `429` kèm `Retry-After`.
- **4a.** LLM trả sai schema: thử lại tối đa 2 lần; vẫn lỗi thì job `FAILED`, brief cũ giữ nguyên.
- **4b.** Nội dung bị moderation chặn: job `FAILED` với `CONTENT_POLICY` (451); không tự sửa để vượt bộ lọc (BR-18).
- **5a.** `409`: shot đã đổi trong lúc job chạy; kết quả không ghi đè, Editor chọn áp dụng hoặc bỏ (UC-02.10).

### UC-05.06f Tự khớp tên với tài sản
<a id="uc-0506f"></a>

| Mục | Nội dung |
|---|---|
| Loại | extend của UC-05.06 |
| Tác nhân | Editor |
| Mô tả | Tự gắn các tên chưa liên kết ở shot với đúng Story Asset |
| Tiền điều kiện | Bản nháp có tham chiếu "chưa liên kết"; dự án có Story Assets |
| Hậu điều kiện | **Thành công:** các tham chiếu khớp duy nhất được liên kết. **Tối thiểu:** không liên kết nhầm khi khớp mơ hồ |
| Kích hoạt | Bấm "Scan the chapter text and auto-match" hoặc từ cảnh báo ở UC-05.01 nhánh 5a |
| Truy vết | FR-BOK-08; BR-16; API 2.5 `POST …/storyboards/{did}:auto-link-assets` |

**Luồng chính**
1. Editor bấm "Scan the chapter text and auto-match".
2. Hệ thống lấy mọi `shot_asset_refs` của bản nháp có `story_asset_id = NULL`.
3. Hệ thống so `raw_name` với tên và bí danh của Story Assets (không phân biệt hoa thường, dấu cách chuẩn hóa).
4. Khớp đúng một tài sản: gán `story_asset_id`. Khớp từ hai tài sản trở lên: bỏ qua và liệt kê. Không khớp: giữ "chưa liên kết".
5. Hệ thống báo "Đã liên kết N, còn M chưa liên kết" kèm danh sách phần còn lại.

**Luồng thay thế / ngoại lệ**
- **2a.** Dự án chưa có tài sản nào: gợi ý phân tích tài sản (UC-04.01) hoặc tạo tài sản (UC-04.02a).
- **4a.** Không có tên nào cần khớp: báo "Không còn tên chưa liên kết".

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

### UC-05.07a Dựng storyboard tự động
<a id="uc-0507a"></a>

| Mục | Nội dung |
|---|---|
| Loại | include của UC-05.07 (bước 4) |
| Tác nhân | Hệ thống / LLM |
| Mô tả | Tự tạo storyboard cho chương chưa có storyboard hiện hành để việc sinh tư liệu chạy liền một mạch |
| Tiền điều kiện | Chương có văn bản, không bị khóa; chưa có storyboard hiện hành |
| Hậu điều kiện | **Thành công:** chương có một bản nháp hiện hành gồm N shot phủ kín 100%. **Tối thiểu:** lỗi thì chương ở trạng thái cần xử lý, không có bản nháp dở dang |
| Kích hoạt | UC-05.07 bước 4; UC-07.02 bước `media` |
| Truy vết | FR-BOK-01; BR-07, BR-20; 08 §3.2 (`STORYBOARD_DRAFT`, 0 credit); API 2.5 `POST …/media:generate` |

**Luồng chính**
1. Hệ thống kiểm tra chương đã có storyboard hiện hành hay chưa; nếu có thì bỏ qua use case này.
2. Hệ thống lấy thời lượng mục tiêu mỗi ảnh từ `projects.target_shot_seconds` (mặc định 15 giây).
3. Hệ thống chạy UC-05.01 (job con `STORYBOARD_DRAFT`, `kind = INITIAL`).
4. Hệ thống đặt bản nháp làm hiện hành (BR-07).
5. Hệ thống trả số shot thực tế cho UC-05.07 để điều chỉnh phần credit đã giữ (UC-05.07 nhánh 4a).

**Luồng thay thế / ngoại lệ**
- **3a.** Job lỗi sau retry (UC-05.01 nhánh 3a): chương `NEEDS_ATTENTION`, không sinh ảnh và thuyết minh cho chương này; các chương khác trong cùng lượt vẫn chạy.
- **1a.** Chương đang bị khóa: `423 RESOURCE_LOCKED`.

### UC-05.07b Xem tiến độ theo shot
<a id="uc-0507b"></a>

| Mục | Nội dung |
|---|---|
| Loại | extend của UC-05.07 |
| Tác nhân | Editor |
| Mô tả | Theo dõi theo thời gian thực trạng thái ảnh và thuyết minh của từng shot trong lúc sinh tư liệu |
| Tiền điều kiện | Có job `GENERATE_MEDIA_CHAPTER` đang chạy hoặc đã chạy cho chương |
| Hậu điều kiện | **Thành công:** Editor thấy trạng thái của từng shot. **Tối thiểu:** không thay đổi dữ liệu |
| Kích hoạt | Mở bảng tiến độ sau khi bấm "Sinh tư liệu" |
| Truy vết | FR-MED-01..05; API 2.5 `GET …/media?chapterId=`; API 3 sự kiện `media.progress` |

**Luồng chính**
1. Hệ thống tải ảnh chụp ban đầu từ media bin (`GET /projects/{pid}/media?chapterId=`).
2. Hệ thống hiển thị bảng: mỗi shot một hàng, hai cột Ảnh và Thuyết minh với trạng thái (`PENDING`, `GENERATING`, `DONE`, `FAILED` cho ảnh; thêm `VERIFIED`, `NEEDS_REVIEW`, `ACCEPTED`, `OUTDATED` cho thuyết minh).
3. Hệ thống cập nhật bảng qua SSE: `media.progress`, `illustration.ready`, `narration.updated`, `job.updated`.
4. Editor lọc các shot "Cần xử lý" và mở từng shot để xử lý: ảnh lỗi (UC-05.10), thuyết minh cần xem lại (UC-05.14), sinh lại phần thiếu (UC-05.07c).

**Luồng thay thế / ngoại lệ**
- **3a.** Mất kết nối SSE: client nối lại với `Last-Event-ID`; nếu thiếu sự kiện thì tải lại ảnh chụp ở bước 1.
- **3b.** Job bị hủy hoặc lỗi hàng loạt: bảng hiển thị trạng thái hiện có của từng shot, chương ở "Cần xử lý".

### UC-05.07c Sinh lại phần thiếu / lỗi
<a id="uc-0507c"></a>

| Mục | Nội dung |
|---|---|
| Loại | extend của UC-05.07 |
| Tác nhân | Editor |
| Mô tả | Chỉ sinh lại những phần còn thiếu, bị lỗi hoặc đã lỗi thời, không đụng tới phần đã đạt |
| Tiền điều kiện | Chương có shot thiếu, lỗi hoặc `OUTDATED`; chương không bị khóa; đủ credit |
| Hậu điều kiện | **Thành công:** các shot được chọn có tư liệu đạt; chương tiến tới "Sẵn sàng dựng" khi mọi shot đạt. **Tối thiểu:** tư liệu đã đạt không bị ghi đè; credit phần lỗi được hoàn |
| Kích hoạt | Bấm "Sinh lại phần thiếu / lỗi" ở bảng tiến độ hoặc chương "Cần xử lý" |
| Truy vết | BR-11, BR-12, BR-14; CR-05; API 2.5 `GET …/media:quote`, `POST …/media:generate {only, parts}` |

**Luồng chính**
1. Editor chọn phạm vi: chỉ phần thiếu, chỉ phần lỗi hoặc chỉ `OUTDATED`; chỉ ảnh, chỉ thuyết minh hoặc cả hai.
2. Hệ thống xác định danh sách shot và phần cần chạy. Ảnh đã `DONE` hợp lệ và ảnh do Editor tải lên (BR-14) không nằm trong danh sách.
3. Hệ thống hiển thị báo giá (`media:quote`); Editor xác nhận.
4. Hệ thống giữ credit (UC-05.17) và tạo job cha, mỗi shot một hoặc hai job con (ảnh, thuyết minh).
5. Các job con chạy như bước 5 của UC-05.07; tiến độ hiển thị ở UC-05.07b.
6. Khi mọi shot đạt, chương "Sẵn sàng dựng" và timeline được đồng bộ (UC-06.15).

**Luồng thay thế / ngoại lệ**
- **2a.** Không có gì cần sinh trong phạm vi đã chọn: báo "Không có phần nào cần sinh lại", không tạo job.
- **3a.** Không đủ credit: `402`; gợi ý chọn phạm vi nhỏ hơn hoặc nạp credit (UC-09.03).
- **5a.** Vẫn còn shot lỗi hoặc `NEEDS_REVIEW`: chương ở "Cần xử lý", liệt kê shot (UC-05.07 nhánh 5a).
- ***a.** Chương đang bị job khác khóa: `423 RESOURCE_LOCKED`.

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
| Quan hệ | include UC-05.17 (trừ nhánh 1a); được mở rộng bởi UC-05.10a..c |
| Truy vết | FR-BOK-10; BR-14; NFR-SEC-10 |

**Luồng chính**
1. Editor mở ảnh và chọn cách sửa (use case con).
2. Hệ thống hiện giá (1 credit), giữ credit, gửi yêu cầu.
3. Hệ thống lưu ảnh mới làm hiện hành, trừ credit; timeline đồng bộ ảnh mới (UC-06.15).

**Luồng thay thế / ngoại lệ**
- **1a.** Editor chọn "Thay bằng ảnh của tôi" và tải ảnh lên (PNG/JPEG/WebP ≤ 10 MB, cạnh ngắn ≥ 512 px; kiểm tra MIME, malware, bỏ EXIF theo NFR-SEC-10). Bước 2 bỏ qua: **không tốn credit**, không tạo job, không gọi Image Provider. Hệ thống lưu Illustration phiên bản mới (`edit_kind = UPLOAD`, `status = DONE`), giữ phiên bản cũ, đặt làm hiện hành và đồng bộ timeline (UC-06.15). Ảnh này không bị sinh ảnh hàng loạt ghi đè (BR-14). Ảnh lệch tỷ lệ dự án được xử lý bằng khung hình ở UC-06.06.

### UC-05.10a Sửa ảnh theo mô tả (Describe → Edit)
<a id="uc-0510a"></a>

| Mục | Nội dung |
|---|---|
| Loại | extend của UC-05.10 |
| Tác nhân | Editor / Image Provider |
| Mô tả | Sửa ảnh shot bằng cách mô tả thay đổi bằng lời, không sinh lại từ đầu |
| Tiền điều kiện | Shot có ảnh hiện hành `DONE`; đủ credit (1 credit) |
| Hậu điều kiện | **Thành công:** Illustration mới (`edit_kind = EDIT`) trở thành ảnh hiện hành; ảnh cũ giữ làm phiên bản trước. **Tối thiểu:** lỗi thì hoàn credit và giữ ảnh cũ làm hiện hành |
| Kích hoạt | Chọn "Describe → Edit" trên ảnh |
| Truy vết | FR-BOK-10; BR-01, BR-02, BR-15, BR-18; 08 §3.2 (`IMAGE_EDIT`, 1 credit); API 2.5 `POST …/illustrations/{iid}:edit` |

**Luồng chính**
1. Editor mở ảnh hiện hành và chọn "Describe → Edit".
2. Editor nhập mô tả thay đổi (ví dụ "đổi sang ánh chiều").
3. Hệ thống hiển thị giá 1 credit; Editor xác nhận; hệ thống giữ credit (UC-05.17) và tạo job `EDIT_IMAGE`.
4. Worker chạy moderation đầu vào, gửi ảnh gốc cùng hướng dẫn tới Image Provider (retry tối đa 3 lần), rồi chạy moderation đầu ra.
5. Hệ thống lưu Illustration mới (`parent_illustration_id` = ảnh gốc, `instruction` = mô tả), đặt làm hiện hành, CAPTURE credit, phát `illustration.ready`.
6. Timeline được đồng bộ ảnh mới (UC-06.15).

**Luồng thay thế / ngoại lệ**
- **2a.** Mô tả rỗng: không cho gửi.
- **3a.** Không đủ credit: `402`.
- **4a.** Lỗi sau 3 lần thử hoặc vi phạm chính sách (451): Illustration `FAILED`, RELEASE credit, ảnh cũ vẫn là ảnh hiện hành, shot có nút "Retry".

### UC-05.10b Sửa vùng tô trên ảnh (Fix a spot)
<a id="uc-0510b"></a>

| Mục | Nội dung |
|---|---|
| Loại | extend của UC-05.10 |
| Tác nhân | Editor / Image Provider |
| Mô tả | Sửa riêng một vùng của ảnh bằng cách tô vùng đó và mô tả điều muốn thấy (inpainting) |
| Tiền điều kiện | Shot có ảnh hiện hành `DONE`; đủ credit (1 credit) |
| Hậu điều kiện | **Thành công:** Illustration mới (`edit_kind = INPAINT`, có `mask_media_id`) trở thành ảnh hiện hành, chỉ vùng được tô thay đổi. **Tối thiểu:** lỗi thì hoàn credit và giữ ảnh cũ |
| Kích hoạt | Chọn "Fix a spot" trên ảnh |
| Truy vết | FR-BOK-10; BR-01, BR-02, BR-15, BR-18; 08 §3.2 (`IMAGE_EDIT`); API 2.5 `POST …/illustrations/{iid}:edit` với `mask` |

**Luồng chính**
1. Editor chọn "Fix a spot".
2. Editor tô vùng cần sửa bằng cọ (chỉnh cỡ cọ, xóa nét tô).
3. Editor mô tả điều muốn thấy trong vùng đã tô.
4. Hệ thống hiển thị giá 1 credit; Editor xác nhận; hệ thống giữ credit và lưu mask vào `media_files`.
5. Job `INPAINT_IMAGE` gửi ảnh gốc, mask và mô tả tới Image Provider; moderation hai chiều như UC-05.10a.
6. Hệ thống lưu Illustration mới, đặt làm hiện hành, CAPTURE credit, phát `illustration.ready` và đồng bộ timeline (UC-06.15).

**Luồng thay thế / ngoại lệ**
- **2a.** Mask rỗng: không cho gửi.
- **2b.** Vùng tô phủ gần hết ảnh: gợi ý dùng Describe → Edit (UC-05.10a) hoặc sinh lại [ĐX].
- **3a.** Không đủ credit: `402`.
- **5a.** Lỗi hoặc vi phạm chính sách: Illustration `FAILED`, RELEASE credit, ảnh cũ giữ làm hiện hành.

### UC-05.10c Khôi phục phiên bản ảnh
<a id="uc-0510c"></a>

| Mục | Nội dung |
|---|---|
| Loại | extend của UC-05.10 |
| Tác nhân | Editor |
| Mô tả | Quay lại một phiên bản ảnh cũ của shot, không tốn credit |
| Tiền điều kiện | Shot có từ hai phiên bản ảnh trở lên |
| Hậu điều kiện | **Thành công:** `shots.current_illustration_id` trỏ phiên bản được chọn. **Tối thiểu:** mọi phiên bản khác giữ nguyên |
| Kích hoạt | Mở lịch sử ảnh của shot |
| Truy vết | D-04; BR-15; API 2.5 `POST …/illustrations/{iid}:make-current` |

**Luồng chính**
1. Editor mở lịch sử ảnh của shot; hệ thống liệt kê các Illustration theo thời gian kèm ảnh thu nhỏ, loại (`GENERATE`, `EDIT`, `INPAINT`, `RETRY`, `UPLOAD`), mô tả và thời điểm.
2. Editor chọn một phiên bản và bấm "Make current".
3. Hệ thống cập nhật `shots.current_illustration_id` (không tạo bản ghi mới, không tốn credit).
4. Hệ thống phát `illustration.ready` và đồng bộ timeline (UC-06.15).

**Luồng thay thế / ngoại lệ**
- **2a.** Chọn phiên bản `FAILED` hoặc `PENDING`: không cho chọn.
- **2b.** Phiên bản quá thời hạn lưu 90 ngày (BR-15): không còn trong danh sách.
- **3a.** Phiên bản được chọn sinh từ brief cũ hơn brief hiện tại: sau khi khôi phục, shot hiện nhãn "brief đã đổi" như bình thường.

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

| Mục | Nội dung |
|---|---|
| Loại | extend của UC-05.11 |
| Tác nhân | Editor / TTS |
| Mô tả | Nghe thử một giọng đọc trước khi chọn, bằng mẫu có sẵn hoặc bằng một câu trong truyện |
| Tiền điều kiện | Là thành viên dự án; danh mục giọng có ít nhất một giọng đang bật |
| Hậu điều kiện | **Thành công:** Editor nghe được giọng. **Tối thiểu:** không lưu gì, không tốn credit |
| Kích hoạt | Bấm ▶ cạnh một giọng |
| Truy vết | FR-NAR-01; 08 §3.3 (`PRONUNCIATION_PREVIEW`, 0 credit); API 2.5 `GET /voices`, `POST …/pronunciations:preview` |

**Luồng chính**
1. Editor bấm ▶ cạnh một giọng trong danh mục.
2. *Mẫu có sẵn:* hệ thống phát audio mẫu (`voices.sample_media_id`).
3. *Câu trong truyện:* Editor chọn hoặc nhập một câu (≤ 200 ký tự); hệ thống gọi `pronunciations:preview {text}` và phát audio ngắn.
4. Editor so sánh các giọng và chọn một giọng ở UC-05.11 bước 1.

**Luồng thay thế / ngoại lệ**
- **3a.** Câu dài hơn 200 ký tự: cắt ở ranh giới câu hoặc báo lỗi.
- **3b.** Vượt giới hạn tần suất: `429` kèm `Retry-After`.
- **3c.** TTS lỗi: báo lỗi chung, Editor thử lại hoặc nghe mẫu có sẵn.
- **1a.** Giọng yêu cầu gói cao hơn (`min_plan_code`): hiện nhãn gói; vẫn nghe thử được, nhưng chọn dùng thì cần nâng cấp.

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

| Mục | Nội dung |
|---|---|
| Loại | include của UC-05.13 (bước 2) |
| Tác nhân | Hệ thống |
| Mô tả | Lấy đúng đoạn văn nguồn của shot từ chương và bảo đảm nó chưa bị đổi kể từ khi chia shot |
| Tiền điều kiện | Shot có `source_start`, `source_end`, `source_hash` |
| Hậu điều kiện | **Thành công:** có `text` đúng bằng đoạn nguồn, sẵn sàng cho UC-05.13b. **Tối thiểu:** không bao giờ có văn bản đọc nào đến từ client hoặc từ LLM |
| Kích hoạt | UC-05.13 bước 2 |
| Truy vết | BR-19; IC-09; D-05; NFR-INT-02 |

**Luồng chính**
1. Hệ thống đọc `chapters.content` hiện tại của chương.
2. Hệ thống cắt `text = content[source_start:source_end]`.
3. Hệ thống tính `sha256(text)` và so với `shots.source_hash`.
4. Khớp: hệ thống chuyển `text` cho UC-05.13b.

**Luồng thay thế / ngoại lệ**
- **4a.** Không khớp (chương đã đổi sau khi chia shot): Narration `OUTDATED`, RELEASE credit, phát `narration.updated`, dừng (UC-05.13 nhánh 2a).
- ***a.** Không có API nào nhận văn bản đọc từ client; use case này là nơi duy nhất hình thành `text`.

### UC-05.13b Chuẩn hóa phát âm (SSML)
<a id="uc-0513b"></a>

| Mục | Nội dung |
|---|---|
| Loại | include của UC-05.13 (bước 3) |
| Tác nhân | Hệ thống (`SpeechNormalizer`) |
| Mô tả | Biến đoạn văn nguồn thành SSML để đọc đúng cách (số, ngày, từ mượn) mà **không thêm, bớt, đổi hay sắp xếp lại từ nào** |
| Tiền điều kiện | Có `text` từ UC-05.13a; dự án có `narration_settings` và từ điển phát âm |
| Hậu điều kiện | **Thành công:** có `ssml` và `normalization_log`; `text` gốc không đổi. **Tối thiểu:** không gọi TTS khi kiểm tra ngược thất bại |
| Kích hoạt | UC-05.13 bước 3 |
| Truy vết | BR-19; FR-NAR-04; NFR-INT-02; 04 §3.4 `pronunciation_entries` |

**Luồng chính**
1. Hệ thống áp quy tắc tất định lên bản đọc: bỏ ký hiệu markdown, đọc số, ngày và đơn vị, ngắt nghỉ theo dấu câu với độ dài nghỉ câu và nghỉ đoạn từ `narration_settings`.
2. Hệ thống áp từ điển phát âm bằng SSML `alias` hoặc `phoneme` (tôn trọng `case_sensitive`).
3. Hệ thống ghi `normalization_log` liệt kê các biến đổi đã áp.
4. Hệ thống kiểm tra ngược: gỡ thẻ SSML và đảo các alias thì phải ra đúng `text`, chỉ khác ở các biến đổi mức phát âm được phép (BR-19).
5. Hệ thống trả `ssml` cho bước gọi TTS của UC-05.13.

**Luồng thay thế / ngoại lệ**
- **4a.** Kiểm tra ngược thất bại (có từ bị thêm, bớt hoặc đổi): không gọi TTS, Narration `FAILED`, RELEASE credit, cảnh báo P1 vì đây là lỗi vi phạm bất biến [ĐX].
- **2a.** Mục từ điển lỗi cú pháp phoneme: bỏ qua mục đó, ghi vào `normalization_log` và cảnh báo trong kết quả.

### UC-05.13c Kiểm chứng lời đọc (WER)
<a id="uc-0513c"></a>

| Mục | Nội dung |
|---|---|
| Loại | include của UC-05.13 (bước 5) |
| Tác nhân | Hệ thống / STT và Aligner |
| Mô tả | Chứng minh audio đọc đúng nguyên văn bằng căn chỉnh từng từ và chép lại bằng STT để tính WER |
| Tiền điều kiện | Đã có audio của shot và `text` gốc |
| Hậu điều kiện | **Thành công:** Narration có `word_timings`, `wer`, `mismatches` và trạng thái `VERIFIED` hoặc `NEEDS_REVIEW`. **Tối thiểu:** không để shot đạt khi chưa kiểm chứng |
| Kích hoạt | UC-05.13 bước 5 |
| Truy vết | FR-NAR-06, FR-NAR-07; BR-22, BR-23; NFR-INT-03; ADR-12; API 2.5 `GET …/shots/{shid}/narration` |

**Luồng chính**
1. Aligner thực hiện forced alignment giữa audio và `text`, tạo `word_timings` (từ, thời điểm bắt đầu và kết thúc, offset ký tự).
2. STT chép lại audio thành văn bản.
3. Hệ thống chuẩn hóa cả hai phía (chữ thường, bỏ dấu câu, giữ dấu thanh) rồi tính WER và danh sách chỗ lệch (`mismatches`: vị trí, từ mong đợi, từ nghe được).
4. WER ≤ ngưỡng của dự án (`narration_settings.wer_threshold`, mặc định 0,03): trạng thái `VERIFIED`.
5. Ngược lại: trạng thái `NEEDS_REVIEW` kèm `mismatches`.
6. `word_timings` được lưu để dựng phụ đề nguyên văn (BR-22).

**Luồng thay thế / ngoại lệ**
- **1a.** Aligner hoặc STT lỗi sau retry: Narration `FAILED`, RELEASE credit [ĐX].
- **5a.** WER lớn hơn 10%: luôn `NEEDS_REVIEW`; không shot nào quá 10% được qua mà không có người duyệt (NFR-INT-03).

---

<a id="uc-0514"></a>
## UC-05.14 Duyệt shot cần xem lại (NEEDS_REVIEW)

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

| Mục | Nội dung |
|---|---|
| Loại | extend của UC-05.14 |
| Tác nhân | Editor |
| Mô tả | Xác nhận thủ công rằng audio đúng nguyên văn khi STT nghe sai nhưng thực tế audio không sai |
| Tiền điều kiện | Narration của shot ở trạng thái `NEEDS_REVIEW` |
| Hậu điều kiện | **Thành công:** Narration `ACCEPTED` với `accepted_by`, `accepted_at`; shot đủ điều kiện xuất (BR-23). **Tối thiểu:** không chấp nhận khi Narration đã thay đổi |
| Kích hoạt | Bấm "Accept" ở UC-05.14 nhánh 2a |
| Truy vết | FR-NAR-08; BR-23; API 2.5 `POST …/shots/{shid}/narration:accept` |

**Luồng chính**
1. Editor nghe audio và xem các chỗ lệch (`mismatches`).
2. Editor tích xác nhận "Tôi đã nghe và lời đọc đúng nguyên văn".
3. Hệ thống gọi `narration:accept`; đặt trạng thái `ACCEPTED`, ghi `accepted_by` và `accepted_at`.
4. Hệ thống phát `narration.updated` và tính lại trạng thái chương (đủ điều kiện thì chương có thể "Sẵn sàng dựng").

**Luồng thay thế / ngoại lệ**
- **3a.** Narration vừa được sinh lại hoặc đã `OUTDATED`: `409` hoặc `422`, tải lại shot.
- **3b.** Người gọi không phải Editor của dự án: `403 FORBIDDEN`.
- **2a.** Editor không tích xác nhận: không cho gửi.

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
