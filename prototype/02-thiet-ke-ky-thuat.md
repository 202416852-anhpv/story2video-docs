# 02 — Thiết kế kỹ thuật prototype tiến hóa

> Thiết kế để cài 10 use case ở [01](01-dac-ta-use-case.md) **trên đúng kiến trúc MVP** ([05](../demo-c2story/tai-lieu/05-kien-truc-he-thong.md), cấu hình rút gọn §4.1 theo ADR-23). Prototype chỉ hiện thực một phần mỗi module; phần chưa có nằm sau port với adapter đơn giản, ghi trong **sổ stub** (§9). Khi mâu thuẫn, bộ đặc tả `demo-c2story` là nguồn sự thật; tài liệu này chỉ quy định phần nào làm trước và làm gọn ra sao.

## 1. Kiến trúc

### 1.1 Container

| Container | Công nghệ (theo 05 §4) | Trong prototype | Ghi chú |
|---|---|---|---|
| **Web App** | Next.js 15, TanStack Query, Tailwind | 4 trang: danh sách dự án, nhập truyện, Thế giới truyện, Shot & xuất video | Client sinh từ `openapi/*.yaml`; trang sẽ được thay / mở rộng ở P1–P3 (PS-12) |
| **API Server** | NestJS (Node 22, TS), Kysely, OpenAPI 3.1 viết trước | Module `projects`, `manuscript`, `world`, `media`, `editor`; `platform/jobs`, `idempotency`, `storage`, `authz` | Module `auth`, `billing`, `admin` có mặt dưới dạng port + adapter stub |
| **Worker** | Node + BullMQ (một tiến trình đăng ký mọi queue, ADR-23) | Queue `orchestrator`, `llm`, `image`, `tts`, `align`; reconciler là repeatable job | Cùng mã nguồn với API (monorepo), khác entrypoint |
| **Render Worker** | Tách riêng (chiếm CPU lâu) | Queue `render`; `RenderEngine` = FFmpeg (PS-10) | Chỉ đọc `timeline_snapshot` |
| **TTS Server** | Python, model mã nguồn mở, GPU (ADR-30) | Tùy chọn; chưa có thì dùng adapter Gemini TTS (PS-08) | HTTP nội bộ |
| **Aligner** | Python, WhisperX (QĐ-122) | Tùy chọn; chưa có thì adapter ước lượng (PS-07) | HTTP nội bộ |
| **PostgreSQL 16**, **Redis 7**, **RustFS** | docker-compose | Có đủ | Giống staging của MVP |

```
Web (Next.js) ──HTTP /v1──► API (NestJS) ──SQL──► PostgreSQL
                               │  enqueue sau commit
                               ▼
                             Redis (BullMQ) ◄──► Worker ──► AI Gateway ──► Gemini (LLM, Image, [TTS])
                               │                    │                  └─► TTS Server, Aligner (tùy chọn)
                               ▼                    ▼
                         Render Worker ──────► RustFS (S3) ◄── presigned URL ── Web
```

### 1.2 Quy tắc phụ thuộc (giữ từ 05 §5)

- Module gọi nhau qua service interface công khai, không đọc bảng của module khác.
- `platform/*` không phụ thuộc module nghiệp vụ; `platform/jobs` khai báo `WalletPort`, `BudgetGuard`, `PriceEstimator`.
- Chỉ `manuscript` ghi `chapters.content`, `source_texts` (NFR-INT-02).
- Kiểm bằng `dependency-cruiser` trong CI **từ ngày đầu** (AC-E3).

## 2. Cấu trúc repo

```
story2video/                         # pnpm workspaces + Turborepo
├─ apps/
│  ├─ web/                           # Next.js
│  ├─ api/                           # NestJS: main.ts (HTTP), worker.ts (BullMQ) cùng một app module
│  │  └─ src/
│  │     ├─ modules/
│  │     │  ├─ auth/                 # IdentityProviderPort + DevIdentityAdapter (PS-01)
│  │     │  ├─ projects/             # ImportService, TextExtractor, TextNormalizer
│  │     │  ├─ manuscript/           # ManuscriptService (chỉ ghi chương)
│  │     │  ├─ world/                # AssetService, AnalyzeAssetsHandler, AssetImageHandler
│  │     │  ├─ media/                # MediaGenerationService, MediaOrchestrator
│  │     │  │  ├─ storyboard/        # StoryboardDraftHandler, AssetLinker
│  │     │  │  ├─ illustration/      # ShotImageHandler
│  │     │  │  └─ narration/         # NarrateSegmentHandler
│  │     │  ├─ editor/               # TimelineBuilder, ReadinessChecker, RenderService
│  │     │  ├─ billing/              # NoopWalletAdapter, AllowAllFreeLimitGuard (PS-02, PS-05)
│  │     │  └─ admin/                # seed CLI; NoopBudgetGuard (PS-03)
│  │     └─ platform/
│  │        ├─ authz/  jobs/  idempotency/  storage/
│  │        └─ (realtime/, audit/, outbox/ thêm ở P0–P1)
│  └─ render-worker/                 # nhận job render, RenderEngine
├─ packages/
│  ├─ core/                          # hàm thuần, không I/O: segmenter, coverage, asset-matcher,
│  │                                 # normalizer (NormalizationMap), timing-map, subtitles,
│  │                                 # timeline-rules (IC-10, SNP-01..07), snapshot schema
│  ├─ ai-gateway/                    # LlmPort, ImagePort, TtsPort, AlignerPort, PromptCompiler, adapter
│  ├─ db/                            # Kysely types, migrations, seed
│  └─ api-client/                    # sinh từ openapi/*.yaml
├─ openapi/                          # projects.yaml, world.yaml, media.yaml, editor.yaml, jobs.yaml
├─ services/ (tts-server/, aligner/) # Python, tùy chọn
├─ infra/docker-compose.yml
└─ docs/prototype-stubs.md           # bản sao sổ stub §9, CI so với mã
```

`packages/core` và `packages/ai-gateway` không phụ thuộc NestJS để render worker, web (preview ở P3) và test dùng chung.

## 3. Dữ liệu

### 3.1 Bảng tạo trong prototype

Migration `0001`..`0003` tạo các bảng dưới **với đủ cột như 04 §3** (kể cả cột chưa dùng, để NULL hoặc mặc định). Enum tạo đủ giá trị của 04 §2. Bảng không có ở đây được thêm bằng migration mới ở giai đoạn tương ứng; không bảng nào phải đổi tên hay chuyển dữ liệu.

| Nhóm (ERD) | Bảng | Cột prototype thực sự ghi |
|---|---|---|
| 1 Tài khoản | `users` | Một user dev từ seed (PS-01) |
| 2 Dự án | `projects`, `project_members`, `source_texts`, `chapters` | Theo PT-01; `chapters.media_status`, `current_storyboard_id`, `locked_by_job_id` |
| 3 Thế giới | `styles`, `story_assets`, `asset_images` | `story_assets`: `kind` ∈ `CHARACTER`/`LOCATION`/`PROP`, `use_exact_image = false`, `version` |
| 4 Sinh tư liệu | `storyboard_drafts`, `shots`, `shot_asset_refs`, `illustrations`, `narration_settings`, `voices`, `narrations` | `shots.focus`, `time_of_day`, `story_date`, `caption` để NULL; `narrations.wer`, `mismatches`, `accepted_*`, `flagged_at` để NULL |
| 5 Editor | `timelines`, `timeline_tracks`, `timeline_items`, `renders` | `renders.scope = CHAPTER`, `watermark = false` |
| 6 Hạ tầng | `jobs`, `ai_providers`, `ai_models`, `ai_usage_records`, `media_files`, `idempotency_keys`, `system_settings` | `jobs.held_micro = 0`, `charged_micro = 0`, `budget_*` NULL |

**Chưa tạo** (thêm ở giai đoạn ghi trong 09): `beta_invites`, `user_sessions`, `payments`, `payment_events`, `wallets`, `wallet_ledger_entries`, `audit_logs`, `price_rules`, `daily_ai_budgets`, `chapter_versions`, `story_asset_group_members`, `visual_rules`, `timeline_events`, `relationships`, `pronunciation_entries`, `audio_assets`; các bảng *(sau MVP)*.

Vì `jobs.user_id`, `media_files.owner_user_id` đã trỏ tới user dev, khi bật SSO (P0) chỉ cần gán `users.sso_subject` cho user dev hoặc tạo user mới; dữ liệu cũ vẫn hợp lệ.

### 3.2 Quy ước bắt buộc (từ 04 §1)

| Mã | Quy ước |
|---|---|
| D-01 | `id` là UUIDv7 sinh ở ứng dụng |
| D-02 | Offset văn bản là code unit UTF-16 trên văn bản NFC (ADR-26); không dùng `char_length()` của Postgres để cắt hay so độ dài |
| D-03 | File media lưu ở RustFS với `storage_key` theo mẫu `p/{projectId}/{loại}/{id}.{đuôi}`; DB chỉ lưu `media_files` và `media_id` |
| D-04 | Tiền là micro-USD `bigint`; prototype ghi 0 |
| D-05 | Cột có `version` dùng cho `ETag` / `If-Match` |

### 3.3 Seed (`pnpm db:seed`, thuộc module `admin`)

| Bảng | Nội dung |
|---|---|
| `users` | User dev: `email = dev@local`, `role = USER`, `consented_at = now()` |
| `styles` | 4–6 style (`code`, `name`, `description`, `prompt_fragment`), vd. `watercolor`, `anime`, `cinematic`, `ink` |
| `ai_providers`, `ai_models` | Gemini (LLM, IMAGE, TTS), TTS Server, WhisperX; `capabilities` của mô hình TTS theo 04 (`speedParam`, `wordTimestamps`, `timestampsTrusted`, `maxCharsPerCall`) |
| `voices` | 1–2 giọng vi, 1 giọng en cho adapter TTS đang bật |
| `system_settings` | `daily_ai_budget_usd = 10` (chưa dùng), `prototype_max_import_chars = 20000` |

## 4. API (tập con của 06)

Base URL `/v1`. Lỗi RFC 9457 (06 §1.1). Mọi `POST` tạo job yêu cầu `Idempotency-Key`; middleware `idempotency` lưu `idempotency_keys` 24 giờ. Mọi endpoint ✓ nhận `?dryRun=true` và trả `{estimatedCostUsd: "0", breakdown: []}` (PS-04).

| Phương thức | Đường dẫn (06) | UC | Job | Ghi chú prototype |
|---|---|---|---|---|
| GET | `/styles` | PT-01 | | |
| GET | `/projects` | — | | Không tìm, không lọc |
| POST | `/projects:import` | PT-01 | | JSON `{title, text, language, aspectRatio, styleId}`; `?dryRun=true` |
| GET | `/projects/{pid}` | — | | |
| GET | `/projects/{pid}/chapters/{cid}` | — | | Kèm `ETag` |
| POST | `/projects/{pid}/story-assets:analyze` | PT-05 | ✓ | Kết quả ở `jobs.result.proposals` |
| GET / POST | `/projects/{pid}/story-assets` | PT-06 | | |
| PATCH / DELETE | `/projects/{pid}/story-assets/{sid}` | PT-06 | | `If-Match` bắt buộc |
| POST | `/projects/{pid}/story-assets/{sid}:generate-image` | PT-07 | ✓ | |
| POST | `/projects/{pid}/media:generate` | PT-02 | ✓ | `{chapterIds, only: MISSING\|FAILED}`; `parts` mặc định cả hai |
| GET | `/projects/{pid}/media?chapterId=` | PT-02 | | Media bin, URL ký 15 phút |
| GET | `/projects/{pid}/chapters/{cid}/storyboards` · `…/storyboards/{did}/shots` | PT-02a | | Chỉ đọc |
| GET | `…/storyboards/{did}/coverage` | PT-02a | | |
| GET | `…/shots/{shid}/narration` | PT-02c | | Audio, `wordTimings`, `status` |
| POST | `/projects/{pid}/timelines` | PT-03 | | `{scope: CHAPTER, chapterId}` |
| GET | `/projects/{pid}/timelines/{tlid}` | PT-03 | | Chỉ đọc (chưa có `:apply-ops`) |
| GET | `/projects/{pid}/timelines/{tlid}/readiness` | PT-03 | | `freeQuota` bỏ trống |
| POST | `/projects/{pid}/timelines/{tlid}/renders` | PT-03 | (miễn phí) | `{resolution: "720p"}`; cần `Idempotency-Key` |
| GET | `/projects/{pid}/renders?timelineId=` · `/renders/{rid}` | PT-04 | | |
| GET | `/projects/{pid}/renders/{rid}/download?file=` | PT-04 | | `302` tới URL ký |
| POST | `/projects/{pid}/renders/{rid}:cancel` | PT-03 | | |
| GET | `/jobs/{jid}` | mọi UC | | `{status, result, errorCode, chargedUsd: "0"}` |

`openapi/*.yaml` chỉ chứa các endpoint trên, viết trước khi code; CI chạy `IT-openapi-contract` so spec sinh từ NestJS với file viết tay (06 §1.2). Endpoint MVP khác được **thêm vào cùng file** ở giai đoạn sau.

## 5. Job

### 5.1 Vòng đời (ADR-29, 05 §6.1, rút gọn)

| Bước | MVP | Prototype |
|---|---|---|
| Tạo job | Một giao dịch: `BudgetGuard.reserve` + `WalletPort.hold` + `INSERT jobs` (+ khóa chương) | Cùng một giao dịch; `NoopBudgetGuard`, `NoopWalletAdapter` trả về ngay, `held_micro = 0` |
| Enqueue | Sau commit, `bullmq.jobId = jobs.id` | Giống |
| Nhận việc | `UPDATE jobs SET status='RUNNING', attempts=attempts+1, started_at=now(), heartbeat_at=now() WHERE id=$1 AND status IN ('QUEUED','RETRYING') RETURNING *`; 0 dòng thì bỏ | Giống |
| Heartbeat | 30 s một lần | Giống |
| Thử lại | Lỗi tạm thời: `RETRYING`, BullMQ backoff 2 s / 8 s / 30 s + jitter, `attempts: 3`; gateway gọi provider một lần mỗi lượt (QĐ-133) | Giống |
| Kết thúc | Ghi kết quả + trạng thái + `WalletPort.capture/release` trong một giao dịch, rồi ack | Giống; capture/release no-op |
| Reconciler | 1 phút: đẩy lại `QUEUED` > 1 phút không có trong BullMQ; 5 phút: `RUNNING` heartbeat > 10 phút → `FAILED`, mở khóa chương | Giống (repeatable job trong worker) |

Mỗi lần gọi provider ghi một dòng `ai_usage_records` (kể cả lỗi) với `cost_usd` tính từ `ai_models.unit_cost_usd`. Nhờ đó số liệu chi phí có ngay từ prototype dù chưa trừ tiền.

### 5.2 Danh mục job

| `jobs.type` | Queue | Handler | Cha / con | UC |
|---|---|---|---|---|
| `ANALYZE_ASSETS` | `llm` | `AnalyzeAssetsHandler` | gốc | PT-05 |
| `GENERATE_ASSET_IMAGE` | `image` | `AssetImageHandler` | gốc | PT-07 |
| `GENERATE_MEDIA_CHAPTER` | `orchestrator` | `MediaOrchestrator` | cha | PT-02 |
| `STORYBOARD_DRAFT` | `llm` | `StoryboardDraftHandler` | con | PT-02a |
| `GENERATE_SHOT_IMAGE` | `image` | `ShotImageHandler` | con | PT-02b |
| `NARRATE_SEGMENT` | `tts` (+ gọi `AlignerPort`) | `NarrateSegmentHandler` | con | PT-02c |
| `RENDER_TIMELINE` | `render` | Render Worker | gốc, miễn phí | PT-03 |

`MediaOrchestrator` chạy hai pha: (1) nếu thiếu storyboard thì tạo con `STORYBOARD_DRAFT` và đợi; (2) tạo con ảnh + thuyết minh theo shot (BullMQ Flow), đợi tất cả, rồi kết thúc cha và mở khóa chương trong một giao dịch. Con kết thúc thì cập nhật `heartbeat_at` của cha.

## 6. Thuật toán lõi (`packages/core`, `packages/ai-gateway`)

### 6.1 `SentenceSegmenter`

Cài **nguyên văn** 12 §1 (hợp đồng §1.1, SEG-R1..R7, danh sách viết tắt §1.3, `SEGMENTER_VERSION = 'seg-1'`). Test SEG-01..23 + `PBT-segmenter-coverage`.

### 6.2 Storyboard và `CoverageValidator`

**Mục tiêu ký tự mỗi shot:** `target = target_shot_seconds × CHARS_PER_SECOND[lang]` (vi 14, en 15; đo lại ở spike), tối thiểu sao cho ≤ 40 shot: `target = max(target, ceil(charCount / 40))`.

**Prompt LLM** (structured output; `prompt_version` ghi vào `ai_usage_records`):

```
System: You split a story chapter into illustration shots. You never rewrite, summarize or quote the story text.
User:   Style: <style.prompt_fragment>. Target about <target> characters per shot, at most 40 shots.
        Story assets (kind | name | aliases | appearance):      ← bỏ khối khi chưa có tài sản
        CHARACTER | Lan | — | Vietnamese woman, mid 20s, …
        Sentences (index: text):
        0: <câu 0>
        …
        Return shots in reading order. Each shot starts at a sentence index and lasts until the next shot starts.
        For each shot: startSentence, short title, English image brief (subject, setting, composition,
        lighting, mood; 40–80 words; no text in image), and assetNames: names of story assets visible
        in the shot exactly as in the list, plus other recurring people or places by the name used in the story.
Schema: { shots: [ { startSentence: integer, title: string, brief: string, assetNames: string[] } ] }
```

**Phủ kín** — tương đương UC-05.01a bước 2–7 vì chỉ dùng điểm bắt đầu:

```ts
function buildShots(sentences: Sentence[], llm: LlmShot[]) {
  const n = sentences.length;
  const starts = [...new Map(llm.map(s =>
      [Math.min(Math.max(Math.trunc(s.startSentence), 0), n - 1), s] as const)).entries()]
    .sort((a, b) => a[0] - b[0]);
  let fixes = llm.length - starts.length;                       // trùng / ngoài phạm vi
  if (starts.length === 0) starts.push([0, EMPTY_SHOT]);
  if (starts[0][0] !== 0) { starts[0] = [0, starts[0][1]]; fixes++; } // khoảng hở đầu chương → shot đầu
  return { fixes, shots: starts.map(([s, meta], i) => {
    const e = i + 1 < starts.length ? starts[i + 1][0] : n;
    return { sourceStart: sentences[s].start, sourceEnd: sentences[e - 1].end, ...meta };
  }) };
}
```

Câu là phân hoạch của chương (SEG-I1) nên shot *i* kết thúc đúng chỗ shot *i+1* bắt đầu; vẫn kiểm IC-08 làm hàng rào cuối (`shots[0].sourceStart = 0`, liền nhau, shot cuối kết thúc tại `content.length`, nối lại `=== content`). Quá 40 shot: gộp shot ngắn nhất vào shot trước.

### 6.3 Thế giới truyện

**Prompt phân tích tài sản** (`ANALYZE_ASSETS`, map theo chương):

```
System: You extract recurring visual entities from a story for an illustrator. You never rewrite the story.
User:   Story language: <lang>. Existing assets: <name | aliases> or "none".
        List characters, locations and props that appear more than once or matter visually.
        For each: kind, name (as written in the story), aliases (max 10), appearance (English, concrete:
        age, build, hair, clothes, colors; places: era, materials, weather), facts (short fixed traits
        in the story language, max 10). If the story gives no detail, infer a plausible appearance.
        Chapter: <content>
Schema: { assets: [ { kind: "CHARACTER"|"LOCATION"|"PROP", name, aliases: string[], appearance, facts: string[] } ] }
```

Reduce: gộp mục cùng `key(name)` (hợp bí danh, facts; giữ mô tả dài hơn). Với một chương, reduce chỉ làm sạch.

**`AssetMatcher`** (dùng cho đánh dấu trùng ở PT-05, cảnh báo trùng ở PT-06, `AssetLinker` ở PT-02a và endpoint `:auto-link-assets` ở P1):

```ts
const key = (s: string) => s.normalize('NFC').toLocaleLowerCase('vi').replace(/\s+/g, ' ').trim();
function matchNames(names: string[], assets: Asset[]): { name: string; assetId: string | null }[] {
  const index = new Map<string, Set<string>>();
  for (const a of assets) for (const n of [a.name, ...a.aliases])
    index.set(key(n), (index.get(key(n)) ?? new Set()).add(a.id));
  return names.map(name => {
    const ids = index.get(key(name));
    return { name, assetId: ids?.size === 1 ? [...ids][0] : null };   // không khớp hoặc mơ hồ → null
  });
}
```

So khớp chính xác sau chuẩn hóa, **không** so khớp mờ; tên mơ hồ để chưa liên kết (giống UC-05.06f).

### 6.4 `PromptCompiler` (BR-08)

Một hàm thuần nhận các lớp chỉ dẫn theo đúng thứ tự BR-08; prototype truyền lớp chưa có là rỗng, nên P1 chỉ cần cung cấp dữ liệu, không sửa hàm.

```ts
compileImagePrompt({
  style,                // styles.prompt_fragment
  artDirection: null,   // P1: projects.art_direction
  visualRules: [],      // P1: visual_rules (PROJECT rồi CHAPTER)
  chapterRules: [],     // sau MVP
  subject,              // brief của shot, hoặc khung theo loại tài sản (PT-07)
  assets,               // [{name, appearance, facts}] theo thứ tự ưu tiên CHARACTER → LOCATION → PROP
}) → { prompt, refs: mediaKey[] }   // refs ≤ MAX_REF_IMAGES
```

Mẫu kết quả cho ảnh shot:

```
<style>
Scene: <brief>
Characters and places in this scene (keep consistent with the attached reference images):
- Lan: <appearance>. Fixed traits: <facts nối bằng "; ">
- Quán nước đầu làng: <appearance>.
No text, no letters, no watermark in the image.
```

`prompt_snapshot` của `illustrations` / `asset_images` lưu nguyên prompt và danh sách `refs`.

### 6.5 Thuyết minh nguyên văn

**`SpeechNormalizer`** cài đúng kiểu dữ liệu 12 §2.2 (`MapSeg` với 5 loại). Prototype chỉ sinh 3 loại:

| Loại | Khi nào | Ví dụ |
|---|---|---|
| `IDENTITY` | Mọi đoạn chữ giữ nguyên | `Bố`, `Về ăn cơm` |
| `DROP` (SYM-01..04) | `*`, `**`, `_`, `~~`, `[`, `]`, `#` đầu dòng; mẫu nào tắt trong `symbol_rules` thì giữ là `IDENTITY` | `*`, `] ` |
| `PAUSE` (SYM-05) | Dòng phân cách `---` / `***` | `<break time="500ms"/>` |

`EXPAND` (số, ngày) và `ALIAS` (từ điển phát âm) được thêm ở P2 vào cùng hàm, không đổi kiểu. **Kiểm tra ngược** gồm hai điều kiện: (1) ghép S từ bản đồ bằng đúng `text`; (2) dãy ký tự `\p{L}\p{N}` của R bằng dãy đó của `text` (đúng khi chỉ có `IDENTITY` / `DROP` / `PAUSE`; khi thêm `EXPAND` ở P2 thì điều kiện 2 so trên các đoạn `IDENTITY`).

**Ports** (`packages/ai-gateway`, theo 05 §7.2 và 04 `ai_models.capabilities`):

```ts
interface TtsPort {
  capabilities(): { ssml: boolean; phoneme: boolean; speedParam: boolean;
                    wordTimestamps: boolean; timestampsTrusted: boolean; maxCharsPerCall: number };
  speak(input: { text: string; ssml?: string; voice: string; speed: number }):
    Promise<{ audio: Buffer /* WAV PCM */; durationMs: number; words?: RWord[] }>;
}
interface AlignerPort {
  align(audio: Buffer, text: string, lang: 'vi' | 'en'): Promise<RWord[]>;  // RWord = {rStart, rEnd, t0, t1}, offset UTF-16 trên R
}
```

`NarrateSegmentHandler`: chia R theo các `PAUSE` và theo câu nếu vượt `maxCharsPerCall` → `speak` từng phần → nối PCM, chèn lặng 500 ms ở `PAUSE` → nếu `speedParam = false` và `speed ≠ 1` thì đổi tốc độ giữ cao độ (FFmpeg `atempo`) **trước** khi căn → lấy `words` (TTS nếu `timestampsTrusted`, ngược lại `AlignerPort`) → `mapTimings` (12 §2.3 bước 1–7) → `word_timings` theo tọa độ chương. Offset từ aligner Python (code point) được đổi sang UTF-16 trong adapter (MAP-10).

| Adapter | Port | Dùng khi | Stub? |
|---|---|---|---|
| `SelfHostedTtsAdapter` | `TtsPort` | TTS Server sẵn sàng (đích của MVP) | Không |
| `GeminiTtsAdapter` | `TtsPort` | TTS Server chưa sẵn sàng | PS-08 |
| `WhisperXAlignerAdapter` | `AlignerPort` | Aligner sẵn sàng (đích của MVP) | Không |
| `ProportionalAlignerAdapter` | `AlignerPort` | Aligner chưa sẵn sàng: chia thời lượng mỗi đoạn giữa hai `PAUSE` cho các từ theo số ký tự | PS-07 |
| `MockTts`, `MockAligner`, `MockLlm`, `MockImage` | mọi port | Test IT, chạy không cần mạng | Không (giữ mãi cho test) |

Mọi adapter TTS chạy chung bộ `IT-tts-port-contract`.

### 6.6 Timeline, phụ đề và `timeline_snapshot`

**`TimelineBuilder`** (UC-06.01a): tạo `timelines` (`scope = CHAPTER`, `aspect_ratio` của dự án, `framing = CROP`, `subtitle_style` mặc định, `status = DRAFT`, `version = 1`) và 5 track; với mỗi shot theo `order_index`: item `NARRATION` (`start_ms` nối tiếp, `duration_ms` = audio) và item `IMAGE` phủ trọn nó cộng đệm 300 ms cuối (BR-25); `motion` Ken Burns luân phiên `ZOOM_IN` / `ZOOM_OUT` cường độ 0,1, tâm (0,5; 0,45); `transition_in = NULL` (PS-09). Kiểm IC-10 trước khi ghi.

**Phụ đề** (12 §2.4, đầy đủ): cue theo câu, cắt theo ranh giới shot, văn bản lấy từ `chapters.content` giữ ký hiệu, tách > 84 ký tự, 2 dòng × 42, 833 ms – 7 s; thời gian từ `word_timings` quy về trục timeline. **Kiểm tra nguyên văn** chạy trước khi ghi snapshot (`IT-subtitle-verbatim`).

**`RenderService.snapshot()`** dựng đối tượng đúng `schemas/timeline-snapshot.schema.json` (`schemaVersion: 2`; copy schema vào `packages/core`, test so khớp với bản trong `demo-c2story`), `output = {aspectRatio, width, height, fps: 30, watermark: false}`, `mediaKey` thay cho URL; kiểm bằng Ajv (Draft 2020-12) và `timeline-rules` (SNP-01..07); lưu vào `renders.timeline_snapshot`.

### 6.7 `RenderEngine` (Render Worker)

```ts
interface RenderEngine {
  supports(snapshot: TimelineSnapshot): string[];   // trả danh sách tính năng chưa hỗ trợ; rỗng = render được
  render(snapshot: TimelineSnapshot, out: OutputPaths, onProgress: (pct: number) => void): Promise<void>;
}
```

`FfmpegRenderEngine` (PS-10) hỗ trợ: item `IMAGE` với `motion` `ZOOM_IN` / `ZOOM_OUT`, item `NARRATION` (đặt theo `startMs`), cue phụ đề, `framing = CROP`. Gặp tính năng khác (chuyển cảnh, `AUDIO`, overlay) thì `supports()` báo và job `FAILED` (`UNSUPPORTED_FEATURE`) thay vì render sai.

1. Tải media theo `mediaKey` về thư mục tạm (URL ký tự tạo trong worker).
2. Mỗi item `IMAGE`: số khung = `round(endMs·fps/1000) − round(startMs·fps/1000)` (làm tròn **tuyệt đối** để không trôi khi nối); `scale` ×2 → `crop` theo khung → `zoompan` theo `motion` → H.264.
3. Nối các đoạn bằng concat demuxer.
4. Audio: đặt từng item `NARRATION` tại `startMs` (`adelay`) rồi `amix` thành một track, nhân `volume`, `master.volume`.
5. Ghi cue ra ASS theo `subtitleStyle`, in phụ đề bằng `subtitles` (libass, font có dấu tiếng Việt), encode H.264 / AAC, `+faststart`; một lần encode audio.
6. Xuất SRT, VTT từ cue; audio thuyết minh MP3.
7. `ffprobe` kiểm thời lượng; lệch > 1 khung so với snapshot thì ghi cảnh báo.

Mốc M3 (09 §1.2) quyết định giữ FFmpeg hay thêm `RemotionRenderEngine`; cả hai đọc cùng snapshot nên phần còn lại không đổi.

## 7. Bảo mật tối thiểu

| Hạng mục | Prototype |
|---|---|
| Truy cập | API chỉ lắng nghe `127.0.0.1` / mạng docker; `DevIdentityAdapter` không bao giờ bật khi `NODE_ENV=production` (khởi động thất bại) |
| Phân quyền | `authz` kiểm `project_members` cho mọi `/projects/{pid}/…` ngay từ đầu (chỉ có Owner) |
| Media | Chỉ qua URL ký 15 phút (NFR-SEC-05); không ghép đường dẫn từ input |
| Secret | `GEMINI_API_KEY` trong `.env`, `ai_providers.config_ref` chỉ lưu tên biến |
| Tiến trình ngoài | FFmpeg gọi bằng `spawn` với mảng tham số, không qua shell |

## 8. Cấu hình (`.env`)

| Biến | Mặc định | Ý nghĩa |
|---|---|---|
| `DATABASE_URL`, `REDIS_URL`, `S3_ENDPOINT`, `S3_BUCKET`, `S3_ACCESS_KEY`, `S3_SECRET_KEY` | theo `docker-compose` | |
| `GEMINI_API_KEY` | — | Bắt buộc khi dùng adapter Gemini |
| `IDENTITY_ADAPTER` | `dev` | `dev` (PS-01) / `oidc` (P0) |
| `TTS_ADAPTER` | `self-hosted` | `self-hosted` / `gemini` (PS-08) / `mock` |
| `ALIGNER_ADAPTER` | `whisperx` | `whisperx` / `proportional` (PS-07) / `mock` |
| `LLM_ADAPTER`, `IMAGE_ADAPTER` | `gemini` | `gemini` / `mock` |
| `TTS_SERVER_URL`, `ALIGNER_URL` | — | HTTP nội bộ |
| `MAX_REF_IMAGES` | `3` | |
| `QUEUE_CONCURRENCY_IMAGE` / `_TTS` / `_LLM` / `_RENDER` | `3` / theo VRAM / `2` / `1` | ADR-28 (MVP) |
| `MAX_IMPORT_CHARS` | `20000` | PS-11; MVP 500.000 |

Mã mô hình (`gemini-…`) nằm ở `ai_models` trong seed, không nằm trong mã; chốt ở spike.

## 9. Sổ stub

Mỗi dòng là một chỗ prototype đơn giản hóa **sau một port hoặc một giá trị cấu hình**. Mã đánh dấu `// @prototype-stub PS-NN`; CI chạy script so danh sách mã `PS-NN` trong mã với bảng này (AC-E4). Xóa stub = xóa dấu, thay adapter, xóa dòng.

| Mã | Stub | Port / vị trí | Thay bằng | Giai đoạn |
|---|---|---|---|---|
| PS-01 | `DevIdentityAdapter`: mọi request là user dev | `IdentityProviderPort` (`auth`) | OIDC Keycloak, sau đó Vbee; phiên BFF; danh sách mời, đồng ý dữ liệu | P0 (đăng nhập), P1 (mời, đồng ý) |
| PS-02 | `NoopWalletAdapter`: hold / capture / release không làm gì | `WalletPort` (`platform/jobs`) | `WalletService` (M09) | P1 |
| PS-03 | `NoopBudgetGuard` | `BudgetGuard` (`platform/jobs`) | Giữ chỗ nguyên tử trên `daily_ai_budgets` (ADR-25) | P2 |
| PS-04 | `ZeroPriceEstimator`: mọi giá ước tính = 0 | `PriceEstimator` | `price_rules` + hệ số 1,10 | P1 |
| PS-05 | `AllowAllFreeLimitGuard`; `renders.watermark = false`; chỉ 720p | `FreeLimitGuard` (`billing`) | Giới hạn Free BR-27, watermark, 1080p | P1 (dự án, chương), P3 (render) |
| PS-06 | Polling thay cho SSE | Web App | `GET /projects/{pid}/events` (`platform/realtime`) | P0–P1 |
| PS-07 | `ProportionalAlignerAdapter` | `AlignerPort` | `WhisperXAlignerAdapter` | P0 (khi chọn xong máy GPU) |
| PS-08 | `GeminiTtsAdapter` | `TtsPort` | `SelfHostedTtsAdapter` (QĐ-121) | P0 |
| PS-09 | `TimelineBuilder`: không chuyển cảnh, Ken Burns cố định | Tham số mặc định của builder | Crossfade 0,5 s (UC-06.01a bước 5), chỉnh trong editor | P3 |
| PS-10 | `FfmpegRenderEngine` hỗ trợ tập con tính năng | `RenderEngine` | FFmpeg đầy đủ hoặc Remotion, chốt ở M3 | P2–P3 |
| PS-11 | Import chỉ `.txt` / `.md`, ≤ 20.000 ký tự | `TextExtractor`, `MAX_IMPORT_CHARS` | `.docx`, 500.000 ký tự, chia chương (M03) | P1 |
| PS-12 | Giao diện 4 trang tối giản | `apps/web` | Studio đầy đủ (Workspace, media bin, editor) | P1–P3 |
| PS-13 | Chưa có `audit_logs`, rate limit, SSE `Last-Event-ID` | `platform/*` | Module `platform` đầy đủ | P0 |

**Không phải stub** (giữ nguyên khi lên MVP): `packages/core`, schema DB đã tạo, endpoint đã có, vòng đời job, `PromptCompiler`, `SpeechNormalizer`, `TimelineBuilder` (trừ tham số PS-09), `RenderService.snapshot()`, các adapter Gemini LLM / Image, `StoragePort`, mock adapter.

## 10. Lộ trình tiến hóa

| Sau prototype | Thêm vào | Không phải sửa |
|---|---|---|
| **P0 còn lại** | OIDC (thay PS-01), SSE (PS-06), TTS Server + WhisperX (PS-07, PS-08), audit, rate limit (PS-13), golden set, EVAL | Module nghiệp vụ, schema, job |
| **P1** | Ví + giá (PS-02, PS-04), giới hạn Free (PS-05 phần dự án / chương), M03 chia chương + `.docx` (PS-11), M04 nhóm, ảnh tải lên, Art Direction, Visual Rules (truyền vào `PromptCompiler`), biên tập shot, chia lại shot, sửa ảnh, `:auto-link-assets` | `CoverageValidator`, `AssetMatcher`, job handler |
| **P2** | `EXPAND` / `ALIAS` + từ điển phát âm, cài đặt thuyết minh, nghe & đánh dấu, trần ngày (PS-03), timeline truyện, quan hệ, spike editor (M3) | `NormalizationMap`, `mapTimings`, `TimelineBuilder` |
| **P3** | Editor (`:apply-ops`, `NarrationGuard`), nhạc / SFX, chuyển cảnh (PS-09), engine render chốt ở M3 (PS-10), watermark, 1080p, nạp tiền, Vbee | `timeline_snapshot`, `ReadinessChecker`, `RenderService` |

## 11. Hạn chế đã biết

| Hạn chế | Hệ quả | Hướng ở MVP |
|---|---|---|
| Gắn tài sản cho shot chỉ qua so khớp tên LLM nêu | Shot nhắc nhân vật bằng đại từ có thể thiếu ảnh tham chiếu | Gắn cast thủ công (UC-05.06b), P1 |
| Không nhóm, Art Direction, Visual Rules, giai đoạn ngoại hình | Nhân vật đổi ngoại hình theo mạch truyện phải tạo hai tài sản | UC-04.02b, 04.06, 04.10, P1; FR-WLD-13 sau MVP |
| Số đọc do TTS tự xử lý (chưa `EXPAND`) | Có thể đọc sai số, ngày | P2 |
| `ProportionalAlignerAdapter` (nếu phải dùng) | Phụ đề lệch tới vài trăm ms trong đoạn dài | WhisperX (PS-07) |
| Mô hình ảnh nhận số ảnh tham chiếu có hạn | Shot đông nhân vật chỉ giữ được 3 nhân vật đầu | Chỉnh `MAX_REF_IMAGES` theo kết quả spike |
