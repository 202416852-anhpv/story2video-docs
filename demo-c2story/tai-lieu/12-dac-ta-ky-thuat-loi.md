# 12 — Đặc tả kỹ thuật lõi

> Ba thành phần quyết định tính đúng của "thuyết minh nguyên văn" (BR-19..BR-22) được đặc tả ở mức đủ để cài đặt và viết test trước khi code: **tách câu** (§1), **ánh xạ timestamp từ bản đọc về văn bản gốc** (§2), **hợp đồng `timeline_snapshot`** (§3). Mỗi mục có bộ ca kiểm thử; mã test ở [09 §4.13](09-ke-hoach-phat-trien.md).
> Ký hiệu trong ca kiểm thử: `⏎` là ký tự xuống dòng `\n`; `|` là ranh giới giữa hai câu (không phải ký tự của văn bản); `␣` là dấu cách khi cần nhấn mạnh.

## 1. `SentenceSegmenter` — tách câu tất định

Dùng ở: UC-05.01 (storyboard), UC-05.01a (phủ kín), UC-05.06c (tách shot), UC-03.02a (dời ranh giới shot), §2 (dựng phụ đề). Thuộc AI Gateway (05 §7.1), viết bằng TypeScript, **hàm thuần** (không gọi mạng, không phụ thuộc thời gian hay cấu hình ngoài phiên bản).

### 1.1 Hợp đồng

```ts
const SEGMENTER_VERSION = 'seg-1';
interface Sentence { index: number; start: number; end: number; soft: boolean } // [start, end) theo code unit UTF-16 của chương
function segment(text: string, lang: 'vi' | 'en'): Sentence[];
```

| Mã | Bất biến (kiểm bằng property-based test) |
|---|---|
| SEG-I1 | `sentences[0].start = 0`, `sentences[i].end = sentences[i+1].start`, `sentences[last].end = text.length`: các câu nối lại **đúng bằng** `text` |
| SEG-I2 | Không câu nào rỗng; văn bản rỗng trả `[]` |
| SEG-I3 | Tất định: cùng `text`, `lang`, `SEGMENTER_VERSION` cho cùng kết quả |
| SEG-I4 | Ổn định cục bộ: sửa chữ bên trong một đoạn văn (giữa hai `\n`) không làm đổi ranh giới của đoạn văn khác |
| SEG-I5 | Mỗi câu chứa ít nhất một ký tự không phải khoảng trắng, trừ khi toàn bộ văn bản chỉ là khoảng trắng (khi đó trả một câu) |

Offset tính theo **code unit UTF-16** (chỉ số chuỗi của JavaScript) trên văn bản đã chuẩn hóa NFC (FR-PRJ-03), thống nhất với `shots.source_start/end` và `wordTimings.charStart`. `storyboard_drafts.segmenter_version` lưu phiên bản đã dùng; đổi quy tắc thì tăng phiên bản, bản nháp cũ vẫn hợp lệ vì đã lưu offset.

### 1.2 Quy tắc (áp theo thứ tự)

| Mã | Quy tắc |
|---|---|
| SEG-R1 | **Dòng là ranh giới cứng.** Mọi ký tự `\n` kết thúc câu hiện tại; `\n` và các dòng trống liền sau thuộc về câu đứng trước. |
| SEG-R2 | **Dòng đặc biệt là một câu riêng:** dòng phân cách (`---`, `***`, chỉ gồm ≥ 3 ký tự `-` / `*` / `_` và khoảng trắng; SYM-05), tiêu đề phụ (bắt đầu bằng `#`; SYM-04). |
| SEG-R3 | **Điểm kết câu ứng viên** trong một dòng: một chuỗi liền nhau gồm `.` `!` `?` `…` (kể cả `...`), tiếp theo tùy chọn là các ký tự đóng `”` `"` `’` `'` `»` `)` `]`, rồi **ít nhất một khoảng trắng**. Không có khoảng trắng phía sau (vd. `2.5`, `1.000.000`, `v.v.,`) thì không phải điểm kết câu. |
| SEG-R4 | Ứng viên chỉ thành **ranh giới** khi ký tự không trắng tiếp theo là "đầu câu": chữ hoa (Unicode `Lu`, gồm chữ hoa tiếng Việt), chữ số, ngoặc mở `“ " ‘ ' « ( [`, gạch thoại `– — -`, `*` hoặc `#`. Chữ thường đứng sau thì không tách (vd. `"Đi thôi!" anh nói.`, `Cô ấy… không nói gì.`). |
| SEG-R5 | **Ngoại lệ không tách:** "từ" là chuỗi ký tự không trắng liền trước điểm kết câu, bỏ các ký tự mở `( [ " “ ‘ '` ở đầu (vd. `(TP.` → `TP.`, `v.v.` giữ nguyên). Không tách nếu từ đó là (a) từ viết tắt trong danh sách §1.3, so khớp phân biệt hoa thường; (b) một chữ hoa đơn lẻ (tên viết tắt, vd. `A. Nguyễn`); (c) số thứ tự đầu dòng dạng `\d+[.)]` (vd. `1. Gạo`). |
| SEG-R6 | Khoảng trắng nằm giữa hai câu thuộc về **câu trước** (khớp UC-05.01a bước 5). Khoảng trắng ở đầu văn bản thuộc câu đầu tiên. |
| SEG-R7 | **Câu quá dài:** câu dài hơn 1.000 ký tự được tách mềm (`soft = true`) ngay sau dấu `,` `;` `:` + khoảng trắng gần nhất trước vị trí 1.000; không có thì sau khoảng trắng gần nhất; không có khoảng trắng thì cắt cứng tại 1.000. Lặp tới khi mọi câu ≤ 1.000 ký tự. |

### 1.3 Danh sách từ viết tắt (phiên bản `seg-1`)

| Ngôn ngữ | Từ viết tắt (không tách câu khi đứng trước khoảng trắng) |
|---|---|
| vi | `TP.` `Tp.` `Q.` `P.` `TT.` `TX.` `H.` `X.` `GS.` `PGS.` `TS.` `ThS.` `BS.` `KS.` `CN.` `Th.` `St.` `Ng.` `v.v.` `vd.` `VD.` `Mr.` `Mrs.` `Ms.` `Dr.` |
| en | `Mr.` `Mrs.` `Ms.` `Dr.` `Prof.` `Sr.` `Jr.` `St.` `Mt.` `vs.` `e.g.` `i.e.` `Inc.` `Ltd.` `No.` `Fig.` |

`etc.` cố ý **không** có trong danh sách vì thường kết thúc câu.

### 1.4 Ca kiểm thử (`UT-sentence-segmenter`)

| Mã | Ngôn ngữ | Đầu vào | Kết quả mong đợi | Quy tắc |
|---|---|---|---|---|
| SEG-01 | vi | `Cô đi. Anh ở lại.` | `Cô đi.␣` \| `Anh ở lại.` | R3, R4, R6 |
| SEG-02 | vi | `Thật sao?! Không thể nào…` | `Thật sao?!␣` \| `Không thể nào…` | R3 |
| SEG-03 | vi | `Cô ấy… không nói gì.` | một câu | R4 (chữ thường) |
| SEG-04 | vi | `TP. Hồ Chí Minh rất nóng.` | một câu | R5a |
| SEG-05 | vi | `Giá 1.000.000 đồng, tăng 2.5%.` | một câu | R3 (không có khoảng trắng) |
| SEG-06 | vi | `"Đi thôi!" anh nói.` | một câu | R3 (ký tự đóng), R4 |
| SEG-07 | vi | `"Đi thôi!" Anh kéo tay cô.` | `"Đi thôi!"␣` \| `Anh kéo tay cô.` | R3, R4 |
| SEG-08 | vi | `Chương một⏎⏎Trời mưa.` | `Chương một⏎⏎` \| `Trời mưa.` | R1 |
| SEG-09 | vi | `– Con về rồi.⏎– Ừ.` | `– Con về rồi.⏎` \| `– Ừ.` | R1 |
| SEG-10 | vi | `*Bố* [Về ăn cơm]⏎Cô mỉm cười.` | `*Bố* [Về ăn cơm]⏎` \| `Cô mỉm cười.` | R1 |
| SEG-11 | vi | `Hết.⏎---⏎Sáng hôm sau.` | `Hết.⏎` \| `---⏎` \| `Sáng hôm sau.` | R1, R2 |
| SEG-12 | vi | `# Hồi 2⏎Cô tỉnh dậy.` | `# Hồi 2⏎` \| `Cô tỉnh dậy.` | R2 |
| SEG-13 | vi | `Cần mua:⏎1. Gạo⏎2. Muối` | `Cần mua:⏎` \| `1. Gạo⏎` \| `2. Muối` | R1, R5c |
| SEG-14 | vi | `Ông A. Nguyễn đến.` | một câu | R5b |
| SEG-15 | vi | `Mua gạo, muối v.v. rồi về.` | một câu | R5a, R4 |
| SEG-16 | vi | `␣␣Trời mưa.` | một câu, `start = 0` | R6 |
| SEG-17 | vi | `Trời mưa` (không dấu câu) | một câu | R1 |
| SEG-18 | vi | `Cô nói: "Về thôi." Rồi quay đi.` | `Cô nói: "Về thôi."␣` \| `Rồi quay đi.` | R3, R4 |
| SEG-19 | vi | 1.500 ký tự, một dấu `,` ở vị trí 900, không có dấu kết câu | hai câu: câu 1 kết thúc sau `,␣` (`soft = true`), câu 2 phần còn lại | R7 |
| SEG-20 | en | `Mr. Smith arrived. He sat down.` | `Mr. Smith arrived.␣` \| `He sat down.` | R5a |
| SEG-21 | en | `She bought apples, pears, etc. Then she left.` | `She bought apples, pears, etc.␣` \| `Then she left.` | §1.3 |
| SEG-22 | vi | `` (rỗng) | `[]` | I2 |

**Property-based test (`PBT-segmenter-coverage`)**: 10.000 chuỗi ngẫu nhiên sinh từ các mảnh tiếng Việt, dấu câu, ngoặc, số, ký hiệu `* [ ] # ---`, dòng trống, emoji (cặp surrogate): kiểm SEG-I1..I5. Thêm: tách → nối → tách lại cho cùng kết quả.

**Kiểm tra trên golden set (`EVAL-segmenter-golden`)**: trên 5–10 chương golden set (QĐ-70), người duyệt gán nhãn ranh giới câu; độ chính xác ranh giới ≥ 98% và **không** có ranh giới nào rơi giữa một từ.

## 2. Ánh xạ timestamp từ bản đọc về văn bản gốc

Dùng ở: UC-05.13 (bước 5–6), UC-06.01a (dựng phụ đề), `IT-subtitle-verbatim`, NFR-INT-04. Thuộc `SpeechNormalizer` (tạo bản đồ) và `narration` worker (áp bản đồ).

### 2.1 Ba hệ tọa độ

| Ký hiệu | Là gì | Ví dụ với đoạn nguồn `*Bố* [Về ăn cơm] năm 2023.` |
|---|---|---|
| **S** | Đoạn nguồn của shot: `chapter.content[sourceStart:sourceEnd]`, offset cục bộ 0..len(S) | `*Bố* [Về ăn cơm] năm 2023.` |
| **R** | Bản đọc (spoken text) do `SpeechNormalizer` sinh, là chữ thuần gửi TTS (SSML chỉ bọc thêm thẻ) | `Bố Về ăn cơm năm hai nghìn không trăm hai mươi ba.` |
| **T** | Thời gian audio (ms), từ timestamp của TTS hoặc forced alignment trên R | |

### 2.2 Bản đồ chuẩn hóa (`NormalizationMap`)

`SpeechNormalizer` trả, cùng với R và SSML, một danh sách đoạn phủ kín **cả S lẫn R**, đơn điệu tăng:

```ts
type SegKind = 'IDENTITY' | 'DROP' | 'EXPAND' | 'ALIAS' | 'PAUSE';
interface MapSeg { kind: SegKind; sStart: number; sEnd: number; rStart: number; rEnd: number; rule?: string } // rule: SYM-01, NUM, DATE, PRON:<id>…
```

| Loại | Ý nghĩa | Ràng buộc |
|---|---|---|
| `IDENTITY` | Chữ giữ nguyên | `S[sStart:sEnd] === R[rStart:rEnd]` |
| `DROP` | Ký hiệu bị bỏ khi đọc (SYM-01..04) | `rStart = rEnd` (độ dài 0 trên R) |
| `EXPAND` | Số, ngày, đơn vị đọc thành chữ | Một đoạn S → nhiều từ R |
| `ALIAS` | Từ điển phát âm `ALIAS` / `PHONEME` | Một đoạn S → cách đọc trên R (phoneme: R giữ chữ gốc, SSML mang phoneme) |
| `PAUSE` | Dòng phân cách SYM-05 hoặc ngắt nghỉ | `rStart = rEnd`; SSML `<break time="500ms"/>` |

Bất biến (`UT-normalization-map`): các `sStart..sEnd` nối liền phủ `[0, len(S))`; các `rStart..rEnd` nối liền phủ `[0, len(R))`; ghép S từ các đoạn `IDENTITY` + `DROP` + phần S của `EXPAND`/`ALIAS`/`PAUSE` bằng đúng S. Bản đồ được lưu trong `narrations.normalization_log` (`{segments: MapSeg[], rules: string[]}`).

### 2.3 Thuật toán ánh xạ

Đầu vào: `NormalizationMap`, danh sách từ trên R kèm thời gian `{rStart, rEnd, t0, t1}` (TTS trả theo ký tự thì gom các ký tự không trắng liền nhau thành từ). Đầu ra: `wordTimings` trong **tọa độ chương** `{w, charStart, charEnd, start, end}` (giây, như API 4.5).

1. **Gán đoạn:** với mỗi từ R, tìm các đoạn bản đồ giao với `[rStart, rEnd)`.
2. **`IDENTITY`:** `charStart = sourceStart + sStart + (rStart − seg.rStart)`; tương tự cho `charEnd`. Từ trải qua nhiều đoạn `IDENTITY` liền nhau thì lấy hợp.
3. **`EXPAND` / `ALIAS`:** mọi từ R thuộc cùng một đoạn gộp thành **một** từ nguồn phủ cả `[sStart, sEnd)`; `start = min(t0)`, `end = max(t1)`.
4. **`DROP`:** không có từ R; sinh một mục độ dài 0 `start = end = t0` của từ nguồn liền sau (cuối đoạn thì lấy `t1` của từ liền trước) để phụ đề vẫn bao được ký hiệu.
5. **`PAUSE`:** không sinh mục; khoảng lặng 0,5 s nằm sẵn trong audio.
6. **Từ thiếu thời gian** (aligner bỏ sót): nội suy tuyến tính theo số ký tự giữa hai từ đã biết gần nhất; không có hàng xóm thì dùng biên của audio.
7. **Đơn điệu:** ép `start` không giảm theo `charStart`; mục chồng lấn thì cắt `end` của mục trước bằng `start` mục sau.
8. **Tốc độ** (ADR-24): clip có `playbackRate = r ≠ 1` dùng file audio dẫn xuất; thời gian của clip là `t / r`. `wordTimings` gốc không đổi, `timeline_snapshot` lưu bản đã chia.

### 2.4 Dựng phụ đề từ `wordTimings`

1. Lấy các câu (§1) giao với đoạn nguồn của shot; mỗi câu là một ứng viên cue, cắt theo ranh giới shot.
2. Câu chỉ là dòng phân cách (SYM-05) hoặc chỉ khoảng trắng: **không** tạo cue (BR-22).
3. Văn bản cue = `chapter.content[charStart:charEnd]` của câu, bỏ khoảng trắng hai đầu, **giữ nguyên ký hiệu**; xuống dòng bên trong thay bằng dấu cách.
4. Văn bản > 84 ký tự (2 dòng × 42): tách thành nhiều cue tại khoảng trắng gần điểm giữa nhất, ưu tiên sau dấu `,` `;`. Mỗi cue tối đa 2 dòng, mỗi dòng ≤ 42 ký tự, ngắt dòng tại khoảng trắng.
5. Thời gian cue = `start` của mục đầu, `end` của mục cuối trong cue; thời lượng tối thiểu 833 ms (kéo dài `end` nếu không chạm cue sau), tối đa 7 s (tách tiếp nếu vượt).

**Kiểm tra nguyên văn** (định nghĩa chính xác của NFR-INT-04): bỏ ngắt dòng trong cue, nối các cue bằng một dấu cách, gộp mọi chuỗi khoảng trắng thành một dấu cách; kết quả phải bằng văn bản chương sau khi bỏ các dòng phân cách và gộp khoảng trắng tương tự.

### 2.5 Ca kiểm thử (`UT-timing-map`, `IT-subtitle-verbatim`)

| Mã | Đoạn nguồn S | Bản đồ / dữ liệu vào | Kết quả mong đợi |
|---|---|---|---|
| MAP-01 | `Cô đi.` | 1 đoạn `IDENTITY` | `wordTimings` khớp từng từ; cue `Cô đi.` |
| MAP-02 | `*Bố* [Về ăn cơm]` | `DROP(*)`, `IDENTITY(Bố)`, `DROP(* [)`, `IDENTITY(Về ăn cơm)`, `DROP(])`; R = `Bố Về ăn cơm` | 4 từ R → 4 mục có thời gian + 3 mục `DROP` độ dài 0; cue văn bản `*Bố* [Về ăn cơm]`, bắt đầu tại `t0` của `Bố` |
| MAP-03 | `năm 2023.` | `IDENTITY(năm )`, `EXPAND(2023 → hai nghìn không trăm hai mươi ba)`, `IDENTITY(.)` | Mục `2023` có `charStart..charEnd` đúng 4 ký tự, `start` = `t0` của "hai", `end` = `t1` của "ba" |
| MAP-04 | `Yên Vân cười.` | từ điển `ALIAS(Yên Vân → Iên Vân)` | Một mục nguồn `Yên Vân` phủ hai từ R |
| MAP-05 | `Hết.⏎---⏎Sáng.` | `PAUSE` cho `---⏎` | Không cue cho `---`; khoảng cách giữa cue `Hết.` và `Sáng.` ≥ 500 ms |
| MAP-06 | `Một hai ba bốn.` | aligner thiếu thời gian của `ba` | `ba` được nội suy giữa `hai` và `bốn`; thứ tự không giảm |
| MAP-07 | 1 câu 130 ký tự | | 2 cue, mỗi cue ≤ 2 dòng × 42 ký tự; ghép lại đúng nguyên văn |
| MAP-08 | `Cô đi.` với `playbackRate = 1,25` | | Thời gian trong snapshot = thời gian gốc / 1,25 |
| MAP-09 | Mọi chương golden set | pipeline thật | Kiểm tra nguyên văn §2.4 đạt 100%; lệch cue so với lời đọc ≤ 100 ms (NFR-PERF-11) |

**Property-based test (`PBT-normalization-map`)**: sinh S ngẫu nhiên có ký hiệu, số, mục từ điển; kiểm bất biến §2.2, và ánh xạ mọi vị trí R về S luôn đơn điệu.

## 3. Hợp đồng `timeline_snapshot`

`timeline_snapshot` là ảnh chụp **bất biến, tự đủ** của một phiên bản timeline, dùng chung cho: PreviewPlayer (dựng từ trạng thái hiện tại theo cùng cấu trúc), Render Worker (đầu vào duy nhất), kiểm toán (NFR-INT-06). Lưu ở `renders.timeline_snapshot` và `timeline_versions.snapshot`.

- **Schema:** [`schemas/timeline-snapshot.schema.json`](schemas/timeline-snapshot.schema.json) (JSON Schema 2020-12), ví dụ hợp lệ: [`schemas/timeline-snapshot.example.json`](schemas/timeline-snapshot.example.json).
- **Phiên bản:** trường `schemaVersion` (hiện `1`). Đổi không tương thích ngược thì tăng; Render Worker từ chối phiên bản lạ.
- **Media** tham chiếu bằng `mediaKey` (khóa object storage), **không** bằng URL ký (URL hết hạn sau 15 phút, NFR-SEC-05). Worker tự ký URL khi render.
- **Thời gian** là số nguyên mili-giây trên trục timeline; `wordTimings` trong snapshot đã quy về trục timeline của clip (đã chia `playbackRate`).
- **Phụ đề** được dựng sẵn thành cue (§2.4) trong snapshot, để preview và render không tự dựng lại theo hai cách khác nhau.

### 3.1 Ràng buộc ngoài JSON Schema (kiểm ở `ReadinessChecker` và `@studio/timeline-rules`)

| Mã | Ràng buộc |
|---|---|
| SNP-01 | Đúng một track `NARRATION`; mỗi shot hiện hành có đúng một item `NARRATION` và một item `IMAGE` (IC-10) |
| SNP-02 | Item `NARRATION` theo đúng thứ tự `order_index` của shot, không chồng lấn; `durationMs = round(audioDurationMs / playbackRate)`; `0,8 ≤ playbackRate ≤ 1,25` (IC-17) |
| SNP-03 | Item `IMAGE` của shot phủ trọn khoảng `[start, start + duration)` của item `NARRATION` cùng shot (BR-25) |
| SNP-04 | `coverage.covered = coverage.total` = tổng ký tự các chương trong phạm vi (IC-11) |
| SNP-05 | `sourceHash` của mọi item `NARRATION` khớp `shots.source_hash` tại thời điểm chụp |
| SNP-06 | Mọi `mediaKey` tồn tại trong `media_files`; item `NARRATION` có `playbackRate ≠ 1` phải trỏ tới file dẫn xuất (`derivedMediaKey`, ADR-24) |
| SNP-07 | Cue phụ đề đạt kiểm tra nguyên văn §2.4 |

### 3.2 Ca kiểm thử (`UT-snapshot-schema`)

| Mã | Biến đổi trên ví dụ hợp lệ | Kết quả |
|---|---|---|
| SNP-T01 | Không đổi | Hợp lệ theo schema và SNP-01..07 |
| SNP-T02 | Bỏ trường `schemaVersion` | Schema từ chối |
| SNP-T03 | `playbackRate = 1.5` trên item `NARRATION` | Schema từ chối (`maximum`) |
| SNP-T04 | Thêm `url` có chữ ký vào item | Schema từ chối (`additionalProperties: false`) |
| SNP-T05 | Rút `durationMs` của item `IMAGE` ngắn hơn thuyết minh | Schema chấp nhận; SNP-03 từ chối |
| SNP-T06 | Xóa item `NARRATION` của một shot | Schema chấp nhận; SNP-01 và SNP-04 từ chối |
| SNP-T07 | Render cùng snapshot hai lần | Hai file MP4 giống nhau về khung hình (so hash khung đầu mỗi shot) |
