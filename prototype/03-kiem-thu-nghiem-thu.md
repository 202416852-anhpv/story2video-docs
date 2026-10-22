# 03 — Kiểm thử, nghiệm thu và kế hoạch

> Prototype **đạt** khi (1) chạy được kịch bản §2 với đầu vào mẫu và mọi tiêu chí chức năng §1.1 đúng, và (2) mọi tiêu chí tiến hóa §1.2 đúng. Mã test dùng lại danh mục [09 §4.13](../demo-c2story/tai-lieu/09-ke-hoach-phat-trien.md); mã mới (đánh dấu ★) là đề xuất thêm vào danh mục đó.

## 1. Tiêu chí nghiệm thu

### 1.1 Chức năng

| Mã | Tiêu chí | Cách kiểm | UC |
|---|---|---|---|
| AC-01 | Nhập văn bản mẫu tạo được dự án; `chapters.content` giống hệt file sau chuẩn hóa NFC và `\n` | `IT-PRJ-import`; so `source_texts.sha256` | PT-01 |
| AC-02 | Một lần "Sinh tư liệu" cho ra mọi shot có ảnh và thuyết minh `DONE`; chương `READY_TO_EDIT`; có timeline bản nháp | `E2E-generate-media-chapter` | PT-02 |
| AC-03 | Các shot phủ kín 100%, nối lại đúng bằng chương | `PBT-coverage-validator`; `GET …/coverage` | PT-02a |
| AC-04 | Một lần "Xuất video" cho ra render `READY`; MP4 mở được, có hình, tiếng, phụ đề | `ffprobe`: 1 luồng H.264 720p, 1 luồng AAC | PT-03 |
| AC-05 | Phụ đề nguyên văn; ký hiệu `*Bố*`, `[…]`, `# …` vẫn hiện; không cue cho `---` | `IT-subtitle-verbatim` trên SRT đã xuất | PT-03 |
| AC-06 | Lời đọc nguyên văn: không bỏ, thêm, viết lại câu nào; không đọc to `*`, `[`, `#` | `IT-tts-input-equals-source` + nghe cả video một lần | PT-02c |
| AC-07 | Phụ đề khớp lời đọc: lệch ≤ 100 ms với WhisperX, ≤ 300 ms nếu đang dùng PS-07 | Kiểm 10 cue ngẫu nhiên | PT-03 |
| AC-08 | Thời lượng MP4 bằng thời lượng snapshot, lệch ≤ 1 khung | `ffprobe` | PT-03 |
| AC-09 | Tải được MP4, SRT, VTT, audio qua link ký | Bấm 4 nút tải | PT-04 |
| AC-10 | Shot lỗi không làm hỏng phần đã xong; "Sinh lại phần lỗi" chỉ chạy lại phần lỗi | ★`IT-retry-failed-only` | PT-02 |
| AC-11 | Văn bản tiếng Anh cũng chạy hết luồng | Lặp kịch bản §2 với ~1.000 ký tự tiếng Anh | Toàn bộ |
| AC-12 | Phân tích tài sản trên văn bản mẫu đề xuất ít nhất **Lan**, **Bố** và một địa điểm; chỉ mục được chọn mới được tạo | `IT-analyze-assets`; kiểm `story_assets` | PT-05 |
| AC-13 | **Nhất quán nhân vật:** mọi shot có Lan đính ảnh tham chiếu của Lan; người xem nhận ra cùng một người ở ≥ 80% số shot có Lan | `illustrations.prompt_snapshot.refs`; 2 người chấm độc lập (dạng thu nhỏ của `EVAL-consistency`) | PT-02a, 02b, 07 |
| AC-14 | Tạo, sửa (`If-Match`), gỡ tài sản đúng giới hạn; gỡ không đổi ảnh shot | `IT-story-asset-crud`, ★`IT-asset-unlink-on-delete` | PT-06 |
| AC-15 | Bỏ qua thế giới truyện vẫn ra video (cảnh báo không chặn) | Lặp kịch bản §2 bỏ bước 4–5 | PT-02 |

### 1.2 Tiến hóa

| Mã | Tiêu chí | Cách kiểm (chạy trong CI) |
|---|---|---|
| AC-E1 | **Schema là tập con của 04:** mọi bảng đã tạo có đúng tên và đủ cột như 04 §3; enum đủ giá trị 04 §2 | ★`IT-schema-matches-spec`: script đọc bảng từ điển của 04 và so với `information_schema` |
| AC-E2 | **API là tập con của 06:** mọi đường dẫn trong `openapi/*.yaml` có trong 06 §2; spec sinh từ mã khớp file viết tay | ★`IT-api-subset-of-spec` + `IT-openapi-contract` |
| AC-E3 | **Ranh giới module đúng 05 §5:** không module đọc bảng của module khác; chỉ `manuscript` ghi `chapters.content` | `dependency-cruiser` + ★`IT-manuscript-sole-writer` |
| AC-E4 | **Sổ stub khớp mã:** tập `PS-NN` trong mã bằng tập trong 02 §9 | ★`CI-stub-ledger` |
| AC-E5 | **Thay adapter không sửa mã:** bộ IT chạy với mock adapter; kịch bản §2 chạy với adapter thật; đổi `TTS_ADAPTER` / `ALIGNER_ADAPTER` chỉ bằng biến môi trường | `IT-tts-port-contract` chạy cho mọi adapter TTS; ★`IT-aligner-port-contract` |
| AC-E6 | **Snapshot đúng hợp đồng 12 §3:** schema trong `packages/core` giống hệt bản trong `demo-c2story`; mọi snapshot ghi ra DB đều qua schema và SNP-01..07 | `UT-snapshot-schema` (SNP-T01..T08) + so hash file schema |

## 2. Kịch bản demo

**Chuẩn bị**

```bash
docker compose -f infra/docker-compose.yml up -d     # postgres, redis, rustfs (+ tts-server, aligner nếu có GPU)
pnpm install && pnpm db:migrate && pnpm db:seed
pnpm dev                                               # web, api, worker, render-worker
```

**Đầu vào:** [`mau/truyen-mau.txt`](mau/truyen-mau.txt): khoảng 1.000 ký tự tiếng Việt, có tiêu đề phụ `#`, ký hiệu `*Bố*`, khung tin nhắn `[…]`, số `2023`, lời thoại, một dòng phân cách `---`.

| Bước | Thao tác | Kết quả mong đợi |
|---|---|---|
| 1 | Mở `http://localhost:3000` | Danh sách dự án (rỗng) và nút "Nhập truyện" |
| 2 | Chọn file mẫu, tiêu đề "Cơn mưa đầu mùa", vi, 16:9, style `watercolor`; xem trước rồi bấm "Tạo dự án" | Xem trước ≈ 1.000 ký tự; trang dự án hiện toàn văn |
| 3 | Mở "Thế giới truyện", bấm "Phân tích bằng AI" | Sau ≈ 10–30 giây: Lan, Bố, bà chủ quán; quán nước, cánh đồng, nhà; có thể có xe đạp, điện thoại |
| 4 | Bỏ chọn đạo cụ, "Thêm vào dự án" | Tài sản xuất hiện theo nhóm, chưa có ảnh |
| 5 | "Sinh ảnh tham chiếu cho tất cả" | Mỗi tài sản lần lượt có ảnh theo style `watercolor` |
| 6 | Mở "Shot", bấm "Sinh tư liệu" | Vài giây sau có 3–5 shot, mỗi shot hiện đoạn nguồn nguyên văn và tài sản đã gắn; ảnh, audio lần lượt `DONE` |
| 7 | Chờ (≈ 1–3 phút) | Chương `READY_TO_EDIT`; nút "Xuất video" bật |
| 8 | Bấm "Xuất video" | Báo cáo điều kiện: phủ 100%, không thiếu; render `RENDERING` → `READY` sau ≈ 1–2 phút |
| 9 | Tải MP4, SRT, VTT, audio | ≈ 1–1,5 phút video; trình phát hiện video trên trang |

**Đầu ra mong đợi khi xem video**

| Đoạn văn bản | Nghe | Phụ đề |
|---|---|---|
| `# Cơn mưa đầu mùa` | "Cơn mưa đầu mùa" | `# Cơn mưa đầu mùa` |
| `*Bố* [Về ăn cơm thôi con, mẹ nấu canh chua rồi.]` | "Bố Về ăn cơm thôi con, mẹ nấu canh chua rồi." | Nguyên văn kể cả `*` và `[ ]` |
| `Từ năm 2023, …` | Số do TTS tự đọc (chưa có `EXPAND`) | `Từ năm 2023, …` |
| `---` | Lặng ~0,5 s | Không có phụ đề |
| Các shot có Lan | — | Ảnh giữ cùng ngoại hình Lan |

## 3. Kiểm thử

Mức theo 09 §4.13: UT, PBT trong `packages/core`; IT chạy API + Postgres + Redis + RustFS thật trong docker, provider AI bằng mock adapter; E2E trên trình duyệt với adapter thật (chạy tay hoặc nightly).

### 3.1 Dùng lại từ 09 §4.13

| Mã | Nội dung trong prototype |
|---|---|
| `UT-sentence-segmenter`, `PBT-segmenter-coverage` | SEG-01..23, bất biến SEG-I1..I5 |
| `PBT-coverage-validator` | `buildShots` với `startSentence` ngẫu nhiên: liền nhau, nối lại bằng chương; > 40 shot gộp còn 40 |
| `IT-storyboard-schema` | `MockLlm` trả JSON sai 2 lần rồi đúng → storyboard tạo được; 1–40 shot |
| `IT-auto-link-assets` | `assetNames: ["Lan", "lan", "Bố", "người lạ"]` với tài sản Lan, Bố → 2 ref liên kết, `người lạ` chưa liên kết; tên trùng hai tài sản → chưa liên kết |
| `IT-PRJ-import` | `.txt` / `.md`, NFC, `\r\n`, BOM; > 20.000 ký tự bị chặn; mọi bảng ghi trong một giao dịch |
| `IT-analyze-assets` | Job trả `proposals` đúng schema; không ghi `story_assets`; mục trùng có `duplicateOfAssetId` |
| `IT-story-asset-crud` | Tạo, sửa giữ `id` và tăng `version`; `409` khi sai `If-Match`, `428` khi thiếu; giới hạn 08 §5 |
| `UT-prompt-compiler-order` | Thứ tự style → (Art Direction) → (Visual Rules) → brief → tài sản; lớp rỗng không để lại dòng trống |
| `IT-tts-input-equals-source` | `MockTts` ghi lại mọi văn bản nhận; mỗi văn bản là bản đọc của đúng đoạn nguồn một shot |
| `IT-tts-port-contract` | Chạy cho `Mock`, `Gemini`, `SelfHosted`: audio + `durationMs`, nhóm lỗi chung |
| `IT-symbol-rules` | SYM-01..05; tắt một mẫu thì ký hiệu được giữ |
| `UT-normalization-map`, `PBT-normalization-map` | Bất biến 12 §2.2 với `IDENTITY` / `DROP` / `PAUSE` |
| `UT-timing-map` | MAP-01, 02, 05, 06, 07, 08, 10 (MAP-03, 04 cần `EXPAND` / `ALIAS`, để P2) |
| `IT-subtitle-verbatim` | Cue ghép lại bằng văn bản chương (12 §2.4) |
| `UT-snapshot-schema` | SNP-T01..T08 |
| `IT-openapi-contract` | Spec sinh từ mã khớp `openapi/*.yaml` |
| `E2E-generate-media-chapter` | Kịch bản §2 bước 6–7 (không có báo giá) |
| `EVAL-asset-extraction` | Chạy một lần trên văn bản mẫu + 1 chương golden nếu đã có |

### 3.2 Mã mới (★, đề xuất thêm vào 09 §4.13)

| Mã | Mức | Nội dung |
|---|---|---|
| `IT-job-claim` | IT | Hai worker cùng nhận một job: đúng một bên thắng (`UPDATE … WHERE status IN …`); BullMQ giao lại job đã `SUCCEEDED` thì bị bỏ |
| `IT-job-reconciler` | IT | Job `QUEUED` không có trong BullMQ > 1 phút được đẩy lại; `RUNNING` heartbeat > 10 phút → `FAILED` và chương được mở khóa |
| `IT-retry-failed-only` | IT | `MockImage` lỗi ở shot 2: chương `NEEDS_ATTENTION`; `only: FAILED` chỉ tạo `GENERATE_SHOT_IMAGE` cho shot 2, không tạo `NARRATE_SEGMENT` |
| `IT-chapter-lock` | IT | `media:generate` lần hai khi đang chạy → `423 RESOURCE_LOCKED` |
| `IT-idempotency-key` | IT | Lặp `Idempotency-Key` trả lại cùng `jobId`, không tạo job mới; thiếu header → `400` |
| `IT-render-not-ready` | IT | `POST …/renders` khi còn shot `FAILED` → `422` với `missingImages` đúng |
| `IT-ref-images-attached` | IT | Shot có Lan (ảnh có) và Bố (chưa ảnh): `MockImage` nhận 1 ref; prompt có mô tả cả hai |
| `IT-asset-unlink-on-delete` | IT | Gỡ tài sản đã gắn 2 shot: `shot_asset_refs.story_asset_id = NULL`, `raw_name` giữ; `illustrations` của 2 shot không đổi |
| `IT-aligner-port-contract` | IT | `Mock`, `Proportional`, `WhisperX`: `RWord` đơn điệu, offset UTF-16 trên R |
| `IT-render-engine-supports` | IT | Snapshot có `transitionIn` hoặc track `MUSIC` có item: `FfmpegRenderEngine.supports()` báo, render `FAILED` (`UNSUPPORTED_FEATURE`) |
| `IT-schema-matches-spec` | IT | AC-E1 |
| `IT-api-subset-of-spec` | IT | AC-E2 |
| `IT-manuscript-sole-writer` | IT | Lint SQL / Kysely: chỉ `modules/manuscript` có câu ghi `chapters.content`, `source_texts` |
| `CI-stub-ledger` | CI | AC-E4 |

## 4. Kế hoạch (3 người, T1–T6)

Prototype chiếm sáu tuần đầu của kế hoạch MVP và **là** mốc M1 (09 §1.2). Phần P0 không thuộc prototype (Keycloak, golden set, EVAL đầy đủ, benchmark) vẫn phải làm song song để đạt M0 ở T4.

| Tuần | Việc | Đầu ra | Liên quan P0/P1 |
|---|---|---|---|
| T1 | Monorepo, CI (lint, `dependency-cruiser`, `CI-stub-ledger`), docker-compose; migration + seed; `openapi/*.yaml` viết tay; `SentenceSegmenter` + test. **Spike:** Gemini LLM structured output, Gemini Image có 1–3 ảnh tham chiếu, 2–3 model TTS tự host + WhisperX tiếng Việt | AC-E1, AC-E4 xanh; ghi chú spike | P0: repo, ADR-26..29, PoC provider |
| T2 | `platform/jobs` (nhận việc, thử lại, heartbeat, reconciler), `idempotency`, `storage`, `authz` + `DevIdentityAdapter`; PT-01; `buildShots`, `AssetMatcher` | `IT-job-claim`, `IT-job-reconciler`, `IT-PRJ-import` | P0: `platform` |
| T3 | `world`: PT-05, PT-06, PT-07; `PromptCompiler`; trang Nhập truyện, Thế giới truyện | AC-12, AC-14 với adapter thật | P1: M04 |
| T4 | `media`: orchestrator, PT-02a, PT-02b, PT-02c (`SpeechNormalizer`, `mapTimings`, adapter TTS / aligner); trang Shot | AC-02, AC-03, AC-06 | P1–P2: M05 |
| T5 | `editor`: `TimelineBuilder`, phụ đề, snapshot, `ReadinessChecker`; Render Worker + `FfmpegRenderEngine`; PT-04 | AC-04, AC-05, AC-08, AC-09 | M1; dữ liệu cho `BENCH-render` |
| T6 | IT / E2E còn lại, kịch bản §2 vi + en, chấm AC-13, rà sổ stub, báo cáo mốc M1 | Mọi AC đạt; video demo | M1 |

**Rủi ro chính**

| Rủi ro | Dấu hiệu | Ứng phó |
|---|---|---|
| Kiến trúc đầy đủ làm prototype chậm hơn một bản "vứt đi" | T3 chưa xong PT-01 + `platform/jobs` | Giữ phạm vi, không cắt nguyên tắc E-02..E-05; lùi PT-05 (phân tích AI) và chỉ giữ tạo tài sản thủ công cho tới T6 |
| Làm prototype lấn năng lực P0 (Keycloak, golden set), trượt M0 ở T4 | Cuối T3 chưa có đăng nhập Keycloak | Một người làm `OidcIdentityAdapter` ở T3–T4 thay cho phần web; PS-01 gỡ sớm |
| TTS Server / WhisperX chưa chạy kịp | Hết T2 chưa có máy GPU | Dùng PS-07, PS-08 cho demo M1; ghi rõ trong báo cáo mốc |
| Gemini TTS / TTS tự host đọc tiếng Việt kém | Spike: người nghe < 4/5, sai dấu thanh | Chọn model khác ở P0 (`EVAL-wer-golden`); không ảnh hưởng mã vì đi qua `TtsPort` |
| Ảnh shot không giữ được nhân vật dù có tham chiếu | AC-13 < 80% | Viết `appearance` cụ thể hơn; giảm còn 1–2 ref; ghi nhận cho quyết định provider ảnh ở M0 |
| FFmpeg `zoompan` chậm trên máy staging | > 2 phút cho 1 phút 720p | Giảm hệ số phóng; số liệu đưa vào `BENCH-render` cho quyết định M3 |
