# 01 — Đặc tả use case prototype

> 10 use case trên luồng **văn bản → thế giới truyện → MP4**. Mẫu Cockburn rút gọn, cùng quy ước với [`00-muc-luc.md`](../demo-c2story/tai-lieu/03-dac-ta-use-case/00-muc-luc.md) §2–3. Mỗi UC là **lát cắt dọc** của UC gốc: dùng đúng endpoint ([06](../demo-c2story/tai-lieu/06-dac-ta-api.md)), bảng ([04](../demo-c2story/tai-lieu/04-mo-hinh-du-lieu.md)), job ([05 §5.1](../demo-c2story/tai-lieu/05-kien-truc-he-thong.md)) của MVP. Dòng **Rút gọn** liệt kê phần chưa làm, kèm mã stub `PS-NN` ([02 §9](02-thiet-ke-ky-thuat.md)) nếu phần đó nằm sau một port.

## 1. Tổng quan

### 1.1 Tác nhân

| Tác nhân | Loại | Vai trò |
|---|---|---|
| User | Người | Người dùng dev duy nhất, đóng vai Owner (PS-01) |
| LLM | Hệ thống ngoài | Google Gemini: đề xuất tài sản, chia shot theo chỉ số câu, viết brief, nêu tên tài sản trong shot |
| Image | Hệ thống ngoài | Google Gemini: ảnh tham chiếu tài sản, ảnh shot (nhận ảnh tham chiếu) |
| TTS | Hệ thống ngoài | TTS Server tự host (ADR-30); Gemini TTS khi TTS Server chưa sẵn sàng (PS-08) |
| Aligner | Hệ thống ngoài | WhisperX tự host; ước lượng theo tỷ lệ ký tự khi chưa sẵn sàng (PS-07) |

Render Worker là thành phần bên trong hệ thống, không phải tác nhân (00-muc-luc §2).

### 1.2 Luồng chính

```
PT-01 Nhập truyện  ──  POST /projects:import
  └─► Thế giới truyện (khuyến nghị, bỏ qua được)
        PT-05 Phân tích tài sản  ──  job ANALYZE_ASSETS → duyệt → POST /story-assets
        PT-06 Quản lý Story Assets
        PT-07 Sinh ảnh tham chiếu  ──  job GENERATE_ASSET_IMAGE
  └─► PT-02 Sinh tư liệu chương  ──  job GENERATE_MEDIA_CHAPTER
        ├─ PT-02a  job con STORYBOARD_DRAFT (nếu chưa có storyboard hiện hành)
        └─ mỗi shot, song song:
             ├─ PT-02b  job con GENERATE_SHOT_IMAGE
             └─ PT-02c  job con NARRATE_SEGMENT
        → chương READY_TO_EDIT → tự dựng timeline (UC-06.01a)
  └─► PT-03 Xuất video  ──  job RENDER_TIMELINE  ──►  PT-04 Tải xuống
```

### 1.3 Trạng thái (enum của 04 §2)

| Cột | Giá trị dùng trong prototype | Ghi chú |
|---|---|---|
| `chapters.media_status` | `DRAFT` → `GENERATING` → `NEEDS_ATTENTION` / `READY_TO_EDIT` → `EXPORTED` | `EDITING`, `OUTDATED` chưa xảy ra vì chưa có editor và chưa sửa được văn bản |
| `illustrations.status` | `PENDING` → `GENERATING` → `DONE` / `FAILED` | |
| `narrations.status` | `PENDING` → `GENERATING` → `DONE` / `FAILED` / `OUTDATED` | `OUTDATED` chỉ khi lệch hash |
| `jobs.status` | `QUEUED` → `RUNNING` → `RETRYING` → `SUCCEEDED` / `FAILED` / `CANCELLED` | `state-job` |
| `renders.status` | `QUEUED` → `RENDERING` → `READY` / `FAILED` / `CANCELLED` | |

### 1.4 Quy ước chung cho mọi UC

- Mọi `POST` tạo job yêu cầu header `Idempotency-Key`, trả `202 {jobId, status, estimatedCostUsd: "0"}` và `Location: /v1/jobs/{jobId}` (giá luôn 0 vì PS-04).
- Lỗi theo RFC 9457 với `code` của 06 §1.1. Mọi UC có thể trả `404 NOT_FOUND`, `400 VALIDATION_ERROR`, `429` (rate limit).
- Tiến độ đọc bằng polling 2 s (`GET /jobs/{jid}`, `GET /projects/{pid}/media`) thay cho SSE (PS-06).
- Lỗi provider: job thử lại 3 lần, backoff 2 s / 8 s / 30 s + jitter (QĐ-133); LLM sai schema được gọi lại kèm thông báo lỗi tối đa 2 lần trong cùng lần thử.

---

<a id="pt-01"></a>
## 2. PT-01 Nhập truyện giữ nguyên văn

| Mục | Nội dung |
|---|---|
| Gốc | UC-02.02, UC-02.02a |
| Tác nhân chính | User (trở thành Owner) |
| Mô tả | Đưa văn bản truyện vào để tạo dự án, **giữ nguyên từng chữ** |
| Tiền điều kiện | Có phiên của user dev (PS-01) |
| Hậu điều kiện | **Thành công:** trong **một giao dịch** có `projects`, `project_members (OWNER)`, `source_texts` (kèm `sha256`), `chapters` #1 chứa toàn văn (`version = 1`, `media_status = DRAFT`), `narration_settings` mặc định. **Tối thiểu:** lỗi thì không ghi gì |
| Kích hoạt | Bấm "Tạo dự án" |
| Truy vết | FR-PRJ-02, FR-PRJ-03; BR-19, BR-21; API `POST /projects:import` (có `?dryRun=true`); `IT-PRJ-import` |
| Rút gọn | Chỉ `.txt` / `.md`, ≤ 20.000 ký tự (PS-11); không kiểm giới hạn Free (PS-05) |

**Luồng chính**
1. User dán văn bản hoặc chọn file `.txt` / `.md`; trình duyệt đọc file bằng UTF-8 nghiêm ngặt.
2. Client gọi `POST /projects:import?dryRun=true` với `{text}`; hệ thống thực hiện UC-02.02a và trả `{chars, paragraphs, sourceSha256}` để xem trước, không ghi gì.
3. User nhập tiêu đề, chọn ngôn ngữ (vi / en), tỷ lệ khung hình (16:9 / 9:16 / 1:1) và style (`GET /styles`).
4. Client gọi `POST /projects:import` với `{title, text, language, aspectRatio, styleId}`; hệ thống kiểm tra lại (UC-02.02a) và ghi trong một giao dịch như hậu điều kiện. `projects` và `source_texts` do module `projects` ghi; `chapters.content` do `ManuscriptService` ghi (NFR-INT-02).
5. Hệ thống trả `201 {projectId, chapterId, sourceSha256}`; giao diện mở trang dự án.

**UC-02.02a (rút gọn):** kiểm tra 1–20.000 ký tự và có ký tự không trắng → chuẩn hóa NFC, `\r\n` / `\r` → `\n`, bỏ ký tự điều khiển vô hình và BOM → ghi `normalization_log` (loại biến đổi, số lần) → tính `sha256`, `char_count` (code unit UTF-16).

**Luồng thay thế / ngoại lệ**
- **1a.** File không phải `.txt` / `.md` hoặc không giải mã được UTF-8: trình duyệt báo lỗi, không gửi.
- **2a / 4a.** Văn bản rỗng, > 20.000 ký tự, tham số sai: `400 VALIDATION_ERROR` chỉ ra trường lỗi; giữ nguyên form.
- **2b.** Văn bản có ký hiệu trình bày (`*Bố*`, `[…]`, `# …`, `---`): giữ nguyên; chỉ bỏ khi đọc (PT-02c).
- **4b.** Lỗi DB: rollback, `500`; giữ nội dung trên form.
- Ghi chú: **không** có tùy chọn "AI viết lại" (BR-19, BR-21).

---

<a id="pt-02"></a>
## 3. PT-02 Sinh tư liệu chương

| Mục | Nội dung |
|---|---|
| Gốc | UC-05.07, UC-05.07a, UC-05.07b, UC-05.07c |
| Tác nhân chính / phụ | User / LLM, Image, TTS, Aligner |
| Mô tả | Một thao tác sinh storyboard (nếu chưa có), rồi **ảnh + thuyết minh nguyên văn** cho mọi shot |
| Tiền điều kiện | Chương có văn bản, không bị khóa (`locked_by_job_id` rỗng); dự án có style và giọng mặc định |
| Hậu điều kiện | **Thành công:** mọi shot có ảnh và thuyết minh `DONE`; chương `READY_TO_EDIT`; có timeline bản nháp (UC-06.01a). **Tối thiểu:** phần `DONE` được giữ; chương được mở khóa trong cùng giao dịch kết thúc job cha |
| Kích hoạt | Bấm "Sinh tư liệu" (`only: MISSING`) hoặc "Sinh lại phần lỗi" (`only: FAILED`) |
| Quan hệ | include PT-02a, PT-02b, PT-02c |
| Truy vết | FR-MED-01..05; BR-12, BR-19, BR-20; WR-05; API `POST /projects/{pid}/media:generate`, `GET /projects/{pid}/media?chapterId=`; seq-sinh-tu-lieu; `E2E-generate-media-chapter` |
| Rút gọn | Không báo giá, không giữ tiền (PS-02, PS-04), không trần ngày (PS-03); tiến độ bằng polling (PS-06); một chương mỗi lượt |

**Luồng chính**
1. User bấm "Sinh tư liệu". Nếu dự án chưa có tài sản, hoặc có tài sản chưa có ảnh tham chiếu, giao diện hiện cảnh báo **không chặn** "Nhân vật có thể không nhất quán" kèm nút sang Thế giới truyện.
2. Client gọi `POST /projects/{pid}/media:generate` với `{chapterIds: [cid], only: "MISSING"}`.
3. Trong một giao dịch, `JobService` tạo job cha `GENERATE_MEDIA_CHAPTER` (`held_micro = 0` qua `WalletPort`), đặt `chapters.locked_by_job_id`, `media_status = GENERATING`; sau commit enqueue BullMQ. Trả `202`.
4. `MediaOrchestrator`: chương chưa có storyboard hiện hành thì tạo job con `STORYBOARD_DRAFT` (**PT-02a**) và chờ.
5. Với mỗi shot cần sinh, orchestrator tạo hai job con song song `GENERATE_SHOT_IMAGE` (**PT-02b**) và `NARRATE_SEGMENT` (**PT-02c**); concurrency theo queue `image`, `tts`.
6. Trang dự án gọi `GET /projects/{pid}/media?chapterId=` mỗi 2 giây: chương → shot → `{sourceText, illustration, narration, durationMs, status}` với URL ký cho ảnh và audio (UC-05.07b).
7. Mọi job con xong: trong một giao dịch, orchestrator đặt `media_status` (`READY_TO_EDIT` nếu đủ `DONE`, ngược lại `NEEDS_ATTENTION`), xóa `locked_by_job_id`, kết thúc job cha.
8. Chương `READY_TO_EDIT`: hệ thống dựng timeline bản nháp (UC-06.01a, PT-03 bước 1); giao diện hiện nút "Xuất video".

**Luồng thay thế / ngoại lệ**
- **3a.** Chương đang khóa: `423 RESOURCE_LOCKED`.
- **4a.** `STORYBOARD_DRAFT` lỗi sau thử lại: chương `NEEDS_ATTENTION`, không sinh ảnh, thuyết minh; mở khóa.
- **7a.** Còn shot `FAILED`: chương `NEEDS_ATTENTION`, giao diện liệt kê shot và `error_code`. "Sinh lại phần lỗi" gửi `only: "FAILED"`: chỉ tạo job con cho phần `FAILED`, giữ phần `DONE` (UC-05.07c).
- **\*a.** Worker chết giữa chừng: reconciler (mỗi 1 phút) đẩy lại job `QUEUED` bị sót; job `RUNNING` có heartbeat > 10 phút thành `FAILED`, mở khóa chương (05 §6.1 bước 8).

<a id="pt-02a"></a>
### 3.1 PT-02a Tạo storyboard phủ kín

| Mục | Nội dung |
|---|---|
| Gốc | UC-05.01, UC-05.01a, UC-05.07a, UC-05.06f |
| Loại | include của PT-02 (bước 4); job `STORYBOARD_DRAFT`, `kind = INITIAL` |
| Tác nhân | Hệ thống / LLM |
| Mô tả | Chia **toàn bộ** văn bản chương thành shot liên tục; gắn tài sản cho shot theo tên |
| Hậu điều kiện | **Thành công:** `storyboard_drafts` (`segmenter_version = 'seg-1'`, `boundary_fixes`) đặt làm `chapters.current_storyboard_id`; N shot (1–40) có `source_start`, `source_end`, `source_hash`, `title`, `brief`; `shot_asset_refs` cho mọi tên LLM nêu. **Tối thiểu:** không lưu bản nháp vi phạm phủ kín |
| Truy vết | BR-07, BR-16, BR-20; IC-08; ADR-11; 12 §1; [02 §6.2–6.3](02-thiet-ke-ky-thuat.md); `IT-storyboard-schema`, `PBT-coverage-validator`, `IT-auto-link-assets` |
| Rút gọn | Brief là một đoạn văn thay cho 7 trường (`focus`, `time_of_day`, `story_date`, `caption` để NULL); chưa có Chapter rules, Visual Rules trong ngữ cảnh |

**Luồng chính**
1. Hệ thống tách câu bằng `SentenceSegmenter` (`seg-1`).
2. Hệ thống tính số ký tự mục tiêu mỗi shot từ `projects.target_shot_seconds` (mặc định 20) và tốc độ đọc tham chiếu ([02 §6.2](02-thiet-ke-ky-thuat.md)).
3. LLM nhận danh sách câu đánh số, style, mục tiêu và danh sách tài sản (loại, tên, bí danh, mô tả); trả `{shots: [{startSentence, title, brief, assetNames}]}`. LLM **không chép lại văn bản**.
4. `CoverageValidator` đổi chỉ số câu thành offset, sửa ranh giới, kiểm IC-08 (UC-05.01a), tính `source_hash`, `boundary_fixes`.
5. `AssetLinker` khớp từng tên trong `assetNames` với tên và bí danh tài sản (UC-05.06f): khớp duy nhất thì `story_asset_id` = tài sản đó, ngược lại NULL; `raw_name` luôn lưu; `role` theo loại tài sản (`CAST` / `LOCATION` / `ITEM`), tên chưa khớp mặc định `CAST`.
6. Hệ thống ghi bản nháp, shot, `shot_asset_refs` và `chapters.current_storyboard_id` trong một giao dịch.

**Luồng thay thế / ngoại lệ**
- **3a.** LLM sai schema sau 2 lần gọi lại: lỗi tạm thời của job → thử lại; hết lượt thì job `FAILED` (`LLM_SCHEMA`).
- **4a.** > 40 shot: gộp shot ngắn nhất vào shot trước tới khi còn 40. 0 shot hợp lệ: 1 shot phủ cả chương.
- **4b.** `boundary_fixes` > 20% số ranh giới: vẫn lưu, ghi cảnh báo vào `jobs.result`.
- **4c.** Bất biến sai sau khi sửa (lỗi lập trình): không lưu, job `FAILED` (`COVERAGE_INVARIANT`), log mức ERROR.

<a id="pt-02b"></a>
### 3.2 PT-02b Sinh ảnh shot

| Mục | Nội dung |
|---|---|
| Gốc | UC-05.09 |
| Loại | include của PT-02 (bước 5); job con `GENERATE_SHOT_IMAGE` (`held_micro = 0`, WR-05) |
| Tác nhân | Hệ thống / Image |
| Mô tả | Sinh ảnh minh họa cho shot, giữ nhất quán bằng ảnh tham chiếu |
| Hậu điều kiện | **Thành công:** `illustrations` mới (`edit_kind = GENERATE`, `status = DONE`, `prompt_snapshot`, `shot_version`), `media_files` mới, `shots.current_illustration_id` trỏ tới. **Tối thiểu:** lỗi thì `illustrations.status = FAILED` |
| Truy vết | FR-BOK-09; BR-08; 05 §7.4; [02 §6.4](02-thiet-ke-ky-thuat.md); `UT-prompt-compiler-order` |
| Rút gọn | Chưa có Art Direction, Visual Rules trong prompt (`PromptCompiler` để trống các lớp đó) |

**Luồng chính**
1. `PromptCompiler` ghép theo BR-08: style → (Art Direction) → (Visual Rules) → brief → mô tả và facts của từng tài sản đã liên kết.
2. Hệ thống chọn tối đa `MAX_REF_IMAGES` (mặc định 3) ảnh tham chiếu hiện hành của tài sản trong shot, ưu tiên `CHARACTER` → `LOCATION` → `PROP`.
3. Gọi `ImagePort.generate(prompt, {aspectRatio, refs})`; prompt và ảnh qua bộ lọc an toàn có sẵn của Gemini (QĐ-135).
4. Lưu ảnh vào RustFS qua `StoragePort`, ghi `media_files`, `illustrations`, đặt hiện hành; ghi `ai_usage_records`.

**Luồng thay thế / ngoại lệ**
- **2a.** Tài sản chưa có ảnh tham chiếu: vẫn đưa mô tả và facts vào prompt, chỉ không đính ảnh.
- **3a.** Lỗi tạm thời: job `RETRYING` theo backoff.
- **3b.** Bị chặn vì chính sách hoặc hết lượt thử: `illustrations.status = FAILED`, job `FAILED` (`CONTENT_POLICY` / `PROVIDER_ERROR`).
- **3c.** Ảnh sai tỷ lệ: chấp nhận; render cắt giữa theo `framing = CROP`.

<a id="pt-02c"></a>
### 3.3 PT-02c Sinh thuyết minh nguyên văn

| Mục | Nội dung |
|---|---|
| Gốc | UC-05.13, UC-05.13a, UC-05.13b |
| Loại | include của PT-02 (bước 5); job con `NARRATE_SEGMENT` |
| Tác nhân | Hệ thống / TTS, Aligner |
| Mô tả | Tạo audio đọc **đúng từng chữ** đoạn nguồn của shot, kèm `word_timings` theo tọa độ chương |
| Hậu điều kiện | **Thành công:** `narrations` mới (`version_no` tăng, `source_hash`, `spoken_text`, `ssml`, `normalization_log`, `voice_id`, `media_id`, `duration_ms`, `word_timings`, `status = DONE`), `shots.current_narration_id` trỏ tới. **Tối thiểu:** không có audio nào sinh từ văn bản khác đoạn nguồn |
| Truy vết | FR-NAR-02, 03, 06; BR-19, BR-22; IC-09; 08 §6; 12 §2; [02 §6.5](02-thiet-ke-ky-thuat.md); `IT-tts-input-equals-source`, `IT-symbol-rules`, `UT-normalization-map`, `UT-timing-map`, `IT-tts-port-contract` |
| Rút gọn | `NormalizationMap` chỉ sinh `IDENTITY` / `DROP` / `PAUSE` (chưa đọc số thành chữ `EXPAND`, chưa từ điển `ALIAS`); chưa kiểm chứng WER (sau MVP); TTS / Aligner có adapter thay thế (PS-07, PS-08) |

**Luồng chính**
1. **UC-05.13a:** đọc `chapters.content`, cắt `text = content.slice(source_start, source_end)`, so `sha256(text)` với `shots.source_hash`.
2. **UC-05.13b:** `SpeechNormalizer` áp SYM-01..05 đang bật (`narration_settings.symbol_rules`), sinh bản đọc R, SSML và `NormalizationMap`; **kiểm tra ngược**: ghép S từ bản đồ phải đúng `text`, và dãy chữ / số của R phải bằng dãy chữ / số của `text`.
3. Gọi `TtsPort.speak(R, {voice, speed})` theo đoạn giữa các `PAUSE`; đoạn dài hơn `capabilities.maxCharsPerCall` chia theo câu rồi nối; chèn 500 ms lặng tại `PAUSE`. Tốc độ đọc áp ở bước này (tham số mô hình nếu `capabilities.speedParam`, ngược lại đổi tốc độ giữ cao độ trước khi căn; QĐ-140).
4. Lấy thời gian từng từ trên R: dùng timestamp của TTS nếu `capabilities.timestampsTrusted`, ngược lại gọi `AlignerPort.align(audio, R)`.
5. Ánh xạ về tọa độ chương bằng `NormalizationMap` (12 §2.3) để có `word_timings`.
6. Lưu audio, `narrations` `DONE`, đặt hiện hành; ghi `ai_usage_records`.

**Luồng thay thế / ngoại lệ**
- **1a.** Hash không khớp: `narrations.status = OUTDATED`, job `FAILED` (`SOURCE_MISMATCH`), dừng.
- **2a.** Kiểm tra ngược thất bại: **không gọi TTS**, `FAILED` (`VERBATIM_CHECK_FAILED`), log ERROR.
- **2b.** Đoạn nguồn chỉ gồm dòng phân cách: không gọi TTS; narration `DONE` là 500 ms lặng, `word_timings` rỗng.
- **3a.** TTS lỗi tạm thời: `RETRYING`; bị chặn hoặc hết lượt: `FAILED`. Văn bản **không** được tự sửa để vượt bộ lọc (BR-18).
- **4a.** Aligner lỗi sau thử lại: `FAILED` (`ALIGN_ERROR`).

---

<a id="pt-03"></a>
## 4. PT-03 Xuất video MP4

| Mục | Nội dung |
|---|---|
| Gốc | UC-06.01a, UC-06.16, UC-06.16a |
| Tác nhân chính | User |
| Mô tả | Tự dựng timeline bản nháp, kiểm điều kiện, chụp `timeline_snapshot`, render MP4 kèm SRT / VTT |
| Tiền điều kiện | Chương `READY_TO_EDIT` hoặc `EXPORTED`; User không có render nào đang chạy |
| Hậu điều kiện | **Thành công:** `renders` mới `READY`, `is_primary = true`, có `media_id`, `subtitle_srt_media_id`, `subtitle_vtt_media_id`, `narration_audio_media_id`, `coverage_chars = total_chars`; chương `EXPORTED`. **Tối thiểu:** lỗi thì render `FAILED`, timeline không đổi |
| Kích hoạt | Bấm "Xuất video" |
| Truy vết | FR-EDT-01..03, 21..24; BR-22, BR-23, BR-24, BR-25; IC-10, IC-11; 12 §3; API `POST /projects/{pid}/timelines`, `GET …/timelines/{tlid}/readiness`, `POST …/timelines/{tlid}/renders`, `GET /projects/{pid}/renders/{rid}`; [02 §6.6–6.7](02-thiet-ke-ky-thuat.md); `UT-snapshot-schema`, `IT-subtitle-verbatim` |
| Rút gọn | Không trình chỉnh sửa; timeline mặc định không chuyển cảnh, Ken Burns cố định (PS-09); engine render FFmpeg (PS-10); chỉ 720p, không watermark (PS-05); chưa có nhạc / SFX (track để trống) |

**Luồng chính**
1. **UC-06.01a** (tự chạy khi chương `READY_TO_EDIT`, hoặc khi client gọi `POST /projects/{pid}/timelines` với `{scope: "CHAPTER", chapterId}`): `TimelineBuilder` tạo `timelines` và 5 track (`VIDEO`, `NARRATION` khóa, `SUBTITLE`, `MUSIC`, `SFX`); mỗi shot một item `IMAGE` và một item `NARRATION`; kiểm IC-10.
2. User bấm "Xuất video"; client gọi `GET …/timelines/{tlid}/readiness`.
3. **UC-06.16a:** `ReadinessChecker` kiểm mọi shot có ảnh và thuyết minh `DONE`, không `OUTDATED`, IC-10, BR-24 và độ phủ 100%; trả `{coverage, missingImages[], notDone[], outdated[], violations[], warnings}`.
4. Client gọi `POST …/timelines/{tlid}/renders` với `{resolution: "720p"}`.
5. `RenderService` chụp `timeline_snapshot` (dựng cue phụ đề từ `word_timings`, 12 §2.4), kiểm JSON Schema và SNP-01..07, tạo `renders` (`QUEUED`) và job `RENDER_TIMELINE` (miễn phí) trong một giao dịch.
6. Render Worker nhận job, kiểm lại schema, gọi `RenderEngine.render(snapshot)`; cập nhật `renders.progress`.
7. Xong: tải MP4, SRT, VTT, audio lên storage, ghi `media_files`, render `READY`, `is_primary`; chương `EXPORTED`.

**Luồng thay thế / ngoại lệ**
- **1a.** Chương chưa `READY_TO_EDIT`: `422 PRECONDITION_FAILED_BUSINESS` kèm shot còn thiếu.
- **1b.** Đã có timeline: trả timeline sẵn có, không dựng lại.
- **3a / 4a.** Chưa đạt điều kiện: nút "Xuất" bị vô hiệu hóa; gọi thẳng thì `422 PRECONDITION_FAILED_BUSINESS` (IC-11).
- **4b.** Đang có render chạy của User: `429`.
- **5a.** Snapshot không qua schema hoặc SNP-01..07, hoặc phụ đề không đạt kiểm tra nguyên văn (lỗi lập trình): không tạo render, `500`, log ERROR.
- **6a.** Engine lỗi: thử lại một lần; vẫn lỗi thì render `FAILED` kèm mã lỗi.
- **6b.** User hủy (`POST …/renders/{rid}:cancel`): job và render `CANCELLED`.

---

<a id="pt-04"></a>
## 5. PT-04 Tải MP4 / SRT / audio

| Mục | Nội dung |
|---|---|
| Gốc | UC-06.17 |
| Tác nhân chính | User |
| Mô tả | Tải video và file kèm theo về máy |
| Tiền điều kiện | Có render `READY` |
| Hậu điều kiện | **Thành công:** trình duyệt tải file qua link ký có thời hạn 15 phút |
| Kích hoạt | Bấm "Tải MP4" / "Tải SRT" / "Tải VTT" / "Tải audio" |
| Truy vết | FR-EDT-24, 25; NFR-SEC-05; API `GET /projects/{pid}/renders?timelineId=`, `GET …/renders/{rid}/download?file=MP4\|SRT\|VTT\|NARRATION_AUDIO` |
| Rút gọn | Chưa đặt bản chính khác, chưa xóa phiên bản (`:make-primary`, `DELETE`) |

**Luồng chính**
1. User mở danh sách render (phiên bản, độ phân giải, thời lượng, ngày).
2. User bấm một nút tải; client mở `…/download?file=…`.
3. Hệ thống trả `302` tới URL ký của RustFS; trình duyệt tải file.

**Luồng thay thế / ngoại lệ**
- **3a.** Link hết hạn: bấm lại để lấy link mới.
- **3b.** `file` không thuộc danh sách cho phép: `400 VALIDATION_ERROR`.

---

<a id="pt-05"></a>
## 6. PT-05 Phân tích tài sản bằng AI

| Mục | Nội dung |
|---|---|
| Gốc | UC-04.01, UC-04.01a |
| Tác nhân chính / phụ | User / LLM |
| Mô tả | AI đọc văn bản, **đề xuất** nhân vật, địa điểm, đạo cụ kèm bí danh, mô tả, facts; User duyệt rồi mới tạo |
| Tiền điều kiện | Dự án có ≥ 1 chương có văn bản |
| Hậu điều kiện | **Thành công:** các tài sản User chọn được tạo. **Tối thiểu:** User đóng hộp thoại thì không tạo gì |
| Kích hoạt | Bấm "Phân tích bằng AI" ở trang Thế giới truyện |
| Truy vết | FR-WLD-01; 08 §5; API `POST /projects/{pid}/story-assets:analyze`, `GET /jobs/{jid}`, `POST /projects/{pid}/story-assets`; [02 §6.3](02-thiet-ke-ky-thuat.md); `IT-analyze-assets`, `EVAL-asset-extraction` |
| Rút gọn | Job `ANALYZE_ASSETS` chạy map-reduce như MVP nhưng chỉ có 1 chương; chưa báo giá (PS-04) |

**Luồng chính**
1. User bấm "Phân tích bằng AI"; client gọi `POST /projects/{pid}/story-assets:analyze`; hệ thống tạo job `ANALYZE_ASSETS`, trả `202`.
2. `AnalyzeAssetsHandler` gửi LLM văn bản từng chương (map) kèm danh sách tài sản đang có; hợp nhất kết quả theo tên đã chuẩn hóa (reduce); làm sạch theo giới hạn 08 §5; gắn `duplicateOfAssetId` cho mục trùng tên / bí danh tài sản đã có; ghi `jobs.result = {proposals}`. **Không** ghi `story_assets`.
3. Client đọc `GET /jobs/{jid}` tới khi `SUCCEEDED`, hiện đề xuất theo nhóm Nhân vật / Địa điểm / Đạo cụ; mục trùng mặc định bỏ chọn (UC-04.01a).
4. User bỏ chọn mục không cần; sửa tên, loại, bí danh, mô tả, facts.
5. User bấm "Thêm vào dự án"; client kiểm tra giới hạn rồi gọi `POST /projects/{pid}/story-assets` cho từng mục đã chọn.
6. Giao diện gợi ý "Sinh ảnh tham chiếu cho tất cả" (PT-07 cho từng tài sản chưa có ảnh).

**Luồng thay thế / ngoại lệ**
- **2a.** LLM lỗi hoặc sai schema sau thử lại: job `FAILED`; gợi ý tạo tài sản thủ công (PT-06).
- **2b.** Không có tài sản lặp lại: `proposals` rỗng, báo "Không tìm thấy nhân vật hay địa điểm lặp lại".
- **5a.** Một mục bị từ chối (`400`): giao diện đánh dấu mục đó, các mục khác vẫn được tạo; User sửa rồi gửi lại riêng mục lỗi.
- **\*a.** User đóng hộp thoại: không tạo gì; đề xuất vẫn đọc lại được từ `jobs.result` cho tới lần phân tích mới.

---

<a id="pt-06"></a>
## 7. PT-06 Quản lý Story Assets

| Mục | Nội dung |
|---|---|
| Gốc | UC-04.02, UC-04.02a, UC-04.02d, UC-04.02e |
| Tác nhân chính | User |
| Mô tả | Xem, tạo thủ công, sửa, gỡ nhân vật, địa điểm, đạo cụ |
| Tiền điều kiện | Là Owner dự án |
| Hậu điều kiện | **Thành công:** `story_assets` phản ánh thế giới truyện; sửa giữ nguyên `id`, tăng `version`. **Tối thiểu:** ảnh shot đã sinh không bao giờ bị đổi |
| Kích hoạt | Mở trang "Thế giới truyện" |
| Truy vết | FR-WLD-02; BR-05, BR-14, BR-16; 08 §5; API `GET/POST /projects/{pid}/story-assets`, `PATCH/DELETE …/story-assets/{sid}` (`If-Match`); `IT-story-asset-crud` |
| Rút gọn | Chưa có nhóm (UC-04.02b), thêm từ thư viện (UC-04.02c), ảnh tải lên (UC-04.04); `use_exact_image = false` |

**Luồng chính — xem**
1. `GET /projects/{pid}/story-assets` trả tài sản theo loại, kèm ảnh tham chiếu hiện hành (URL ký) và trạng thái job ảnh gần nhất.

**Luồng chính — tạo (UC-04.02a)**
1. User chọn loại, nhập tên (1–80 ký tự), bí danh (≤ 10), mô tả ngoại hình, facts bất biến.
2. `POST /projects/{pid}/story-assets`; hệ thống kiểm 08 §5 (≤ 200 tài sản), lưu với `version = 1`.
3. User có thể bấm "Sinh ảnh" ngay (PT-07).

**Luồng chính — sửa (UC-04.02e)**
1. User sửa tên, bí danh, mô tả, facts; client gửi `PATCH` kèm `If-Match: "<version>"`.
2. Hệ thống ghi đè, tăng `version`; ảnh tham chiếu và ảnh shot đã sinh không đổi. Đổi mô tả / facts thì giao diện gợi ý "Sinh lại ảnh tham chiếu", không tự sinh.

**Luồng chính — gỡ (UC-04.02d)**
1. User bấm "Gỡ"; hệ thống hiện số shot đang tham chiếu; User xác nhận.
2. `DELETE`; trong một giao dịch hệ thống đặt `shot_asset_refs.story_asset_id = NULL` (giữ `raw_name`) rồi xóa tài sản. `asset_images`, `media_files` của tài sản giữ nguyên; ảnh shot không đổi.

**Luồng thay thế / ngoại lệ**
- **Tạo 1a / Sửa 1a.** Tên hoặc bí danh trùng tài sản khác: cảnh báo "khớp mơ hồ"; vẫn lưu được.
- **Tạo 2a / Sửa 1b.** Vi phạm giới hạn: `400 VALIDATION_ERROR`.
- **Sửa 2a / Gỡ 2a.** Sai `If-Match`: `409 VERSION_CONFLICT` kèm bản hiện tại; thiếu header: `428`.
- **\*a.** Đã có storyboard: tạo / đổi tên tài sản không tự khớp lại shot cũ (khớp lại theo yêu cầu là `…:auto-link-assets`, P1); mô tả và facts mới vẫn dùng khi sinh lại ảnh shot lỗi.

---

<a id="pt-07"></a>
## 8. PT-07 Sinh ảnh tham chiếu

| Mục | Nội dung |
|---|---|
| Gốc | UC-04.03 |
| Tác nhân chính / phụ | User / Image |
| Mô tả | Sinh ảnh chuẩn cho tài sản theo style + mô tả + facts, làm tham chiếu cho ảnh shot |
| Tiền điều kiện | Dự án có style; tài sản có mô tả ngoại hình |
| Hậu điều kiện | **Thành công:** `asset_images` mới (`style_id`, `prompt_snapshot`, `job_id`), `story_assets.current_image_id` trỏ tới; ảnh cũ vẫn còn trong lịch sử. **Tối thiểu:** lỗi thì ảnh hiện hành không đổi |
| Kích hoạt | "Sinh ảnh" / "Sinh lại" trên tài sản, hoặc "Sinh ảnh tham chiếu cho tất cả" (gọi lần lượt cho tài sản chưa có ảnh) |
| Truy vết | FR-WLD-03; BR-08, BR-14; API `POST /projects/{pid}/story-assets/{sid}:generate-image`; [02 §6.4](02-thiet-ke-ky-thuat.md) |
| Rút gọn | Địa điểm sinh một ảnh toàn cảnh thay cho reference sheet nhiều góc; chưa có Art Direction, Visual Rules |

**Luồng chính**
1. Client gọi `POST …/story-assets/{sid}:generate-image`; hệ thống tạo job `GENERATE_ASSET_IMAGE`, trả `202`.
2. `AssetImageHandler`: `PromptCompiler` ghép style → khung theo loại (nhân vật: toàn thân, chính diện, nền trơn; địa điểm: toàn cảnh, không người; đạo cụ: một vật, nền trơn) → tên, mô tả, facts.
3. Gọi Image: 1:1 cho nhân vật và đạo cụ, tỷ lệ dự án cho địa điểm.
4. Lưu ảnh, ghi `media_files`, `asset_images`, đặt `current_image_id`, tăng `story_assets.version`.

**Luồng thay thế / ngoại lệ**
- **1a.** Tài sản chưa có mô tả: `422 PRECONDITION_FAILED_BUSINESS`.
- **1b.** Đang có job `GENERATE_ASSET_IMAGE` chưa kết thúc cho tài sản này: trả lại job đó, không tạo job mới.
- **3a.** Bị chặn hoặc hết lượt thử: job `FAILED`; giữ ảnh hiện hành; gợi ý sửa mô tả.
