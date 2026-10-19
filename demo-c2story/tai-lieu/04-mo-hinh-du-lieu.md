# 04 — Mô hình dữ liệu

> **Phiên bản mô hình:** 2.0 (khớp luồng Studio 6 bước và 165 use case ở [03](03-dac-ta-use-case/00-muc-luc.md)).
> **Sơ đồ:** `../so-do/02-du-lieu/domain-class.puml` (mô hình miền); `../so-do/02-du-lieu/erd.puml` (mô hình vật lý đầy đủ, 55 bảng); ERD theo nhóm `../so-do/02-du-lieu/erd-1..6-*.puml`, sinh tự động từ `erd.puml` bằng `python3 so-do/tools/split_erd.py`. Chỉ sửa `erd.puml` rồi chạy lại script.
> **CSDL:** PostgreSQL 16. Khóa chính `uuid` (UUIDv7). Mọi bảng có thêm `created_at`, `updated_at` (`timestamptz`, không liệt kê ở dưới).

## 1. Nguyên tắc thiết kế

| # | Nguyên tắc |
|---|---|
| D-01 | Chuẩn hóa 3NF. Cấu trúc linh hoạt (brief, motion, style phụ đề, cài đặt) dùng `jsonb` có JSON Schema kiểm tra ở tầng ứng dụng. |
| D-02 | **Khóa lạc quan:** bảng có thể bị sửa đồng thời có cột `version int` (`projects`, `chapters`, `story_assets`, `shots`, `timelines`, `director_plans`); API dùng `If-Match`. |
| D-03 | **Bất biến (chỉ INSERT):** `archives`, `chapter_versions`, `timeline_versions`, `credit_ledger_entries`, `payment_events`, `audit_logs`. |
| D-04 | **Phiên bản hóa đầu ra AI:** ảnh (`illustrations`, `asset_images`), thuyết minh (`narrations`) và bản xuất (`renders`) không ghi đè; mỗi lần sinh tạo bản ghi mới, bảng cha trỏ bản hiện hành. |
| D-05 | **Nguyên văn được bảo vệ bằng dữ liệu:** `chapters.content` là nguồn duy nhất; shot chỉ lưu offset + hash (`source_start`, `source_end`, `source_hash`); thuyết minh lưu `source_hash` để phát hiện lệch. Không có cột nào chứa "văn bản đọc" do client gửi (BR-19). |
| D-06 | File nhị phân nằm ở object storage; DB chỉ lưu `media_files` (key, mime, kích thước, checksum). |
| D-07 | Bảng thuộc dự án có `project_id` (trực tiếp hoặc qua bảng cha) để phân quyền; RLS của Postgres là lớp bảo vệ thứ hai [ĐX]. |
| D-08 | Xóa mềm (`deleted_at`) cho `projects`, `library_assets`; người dùng xóa dữ liệu dùng `users.status = DELETED` + `deletion_requested_at`. |

## 2. Kiểu liệt kê (enum)

| Enum | Giá trị | Dùng ở |
|---|---|---|
| `user_role` | `USER`, `ADMIN` | users |
| `user_status` | `ACTIVE`, `LOCKED`, `DELETED` | users |
| `sub_status` | `INCOMPLETE`, `ACTIVE`, `PAST_DUE`, `CANCEL_AT_PERIOD_END`, `CANCELED`, `EXPIRED` | subscriptions (`state-subscription`) |
| `payment_kind` | `SUBSCRIPTION`, `PACK` | payments |
| `credit_bucket` | `SUBSCRIPTION`, `PACK`, `BONUS` | credit_balances, credit_ledger_entries |
| `ledger_type` | `GRANT`, `PURCHASE`, `HOLD`, `CAPTURE`, `RELEASE`, `EXPIRE`, `ADJUST` | credit_ledger_entries |
| `member_role` | `OWNER`, `EDITOR` | project_members |
| `chapter_media_status` | `DRAFT`, `GENERATING`, `NEEDS_ATTENTION`, `READY_TO_EDIT`, `EDITING`, `EXPORTED`, `OUTDATED` | chapters (`state-chapter-media`) |
| `asset_kind` | `CHARACTER`, `LOCATION`, `PROP`, `GROUP` | story_assets, library_assets |
| `media_status` | `PENDING`, `GENERATING`, `DONE`, `FAILED` | illustrations |
| `narration_status` | `PENDING`, `GENERATING`, `VERIFIED`, `NEEDS_REVIEW`, `ACCEPTED`, `FAILED`, `OUTDATED` | narrations (`state-narration-render`) |
| `timeline_status` | `DRAFT`, `READY_TO_EXPORT` | timelines |
| `track_kind` | `VIDEO`, `OVERLAY`, `SUBTITLE`, `NARRATION`, `MUSIC`, `SFX` | timeline_tracks |
| `item_kind` | `IMAGE`, `NARRATION`, `TITLE`, `TEXT`, `LOGO`, `AUDIO` | timeline_items |
| `render_status` | `QUEUED`, `RENDERING`, `READY`, `FAILED`, `CANCELLED` | renders |
| `plan_status` | `RUNNING`, `AWAITING_INPUT`, `PAUSED`, `COMPLETED`, `CANCELLED` | director_plans (`state-director-plan`) |
| `job_status` | `QUEUED`, `RUNNING`, `RETRYING`, `SUCCEEDED`, `FAILED`, `CANCELLED` | jobs (`state-job`) |
| `provider_kind` | `LLM`, `IMAGE`, `TTS`, `STT`, `ALIGNER`, `MUSIC` | ai_providers |

Các cột kiểu `text` có tập giá trị cố định (vd. `storyboard_drafts.kind`, `timelines.scope`) được kiểm tra bằng `CHECK` và liệt kê ở cột Ghi chú.

## 3. Từ điển dữ liệu

Ký hiệu: **PK** khóa chính, **FK** khóa ngoại, **UQ** duy nhất, `?` cho phép NULL.

### 3.1 Tài khoản & thanh toán — `erd-1-tai-khoan-credit`

| Bảng | Cột | Ghi chú / Use case |
|---|---|---|
| `users` | id PK, sso_subject UQ (= claim `sub`), email, display_name, avatar_url, locale, role, status, gateway_customer_id?, last_login_at, last_daily_claim_on?, deletion_requested_at? | Hồ sơ cục bộ, **không lưu mật khẩu**. UC-01.01b (JIT), UC-01.06 (xóa dữ liệu), UC-09.07 (credit ngày) |
| `user_sessions` | id PK, user_id FK, session_hash UQ, sso_sid?, refresh_token_enc, id_token_hint_enc, expires_at, revoked_at?, last_seen_at | Phiên BFF; token mã hóa AES-GCM. UC-01.01, UC-01.02, UC-01.07 |
| `plans` | id PK, code UQ, name, monthly_credits, price_monthly, price_annual, gateway_price_ids, features, active | `features`: max_projects, max_members, max_resolution, watermark, premium_voices, queue_priority. UC-10.02 |
| `credit_packs` | id PK, code UQ, credits, price, gateway_price_id, active | UC-09.03, UC-10.02 |
| `subscriptions` | id PK, user_id FK, plan_id FK, status, billing_cycle (`MONTHLY`/`ANNUAL`), current_period_start, current_period_end, cancel_at_period_end, gateway_subscription_id UQ | UC-09.02, UC-09.04, UC-09.08a |
| `payments` | id PK, user_id FK, kind, plan_id FK?, credit_pack_id FK?, amount, currency, status, gateway_ref | Đúng một trong `plan_id` / `credit_pack_id` |
| `payment_events` | id PK, gateway_event_id UQ, type, payload, processed_at? | Idempotency webhook. UC-09.08 |
| `credit_balances` | (user_id FK, bucket) PK, available, held, expires_at? | Bảng tổng hợp, cập nhật cùng giao dịch với ledger. UC-09.05 |
| `credit_ledger_entries` | id PK, user_id FK, bucket, delta, type, job_id FK?, payment_id FK?, project_id FK?, actor_id FK?, reason?, expires_at? | Append-only. UC-05.17, UC-09.06, UC-10.08 |
| `audit_logs` | id PK, actor_id FK, action, target_type, target_id?, before?, after?, reason?, ip? | Append-only, giữ 2 năm. UC-10.09 |

### 3.2 Dự án & bản thảo — `erd-2-du-an-ban-thao`

| Bảng | Cột | Ghi chú / Use case |
|---|---|---|
| `projects` | id PK, owner_id FK, title, cover_media_id FK?, style_id FK?, image_model_id FK?, language, target_shot_seconds (mặc định 15), aspect_ratio (`16:9`/`9:16`/`1:1`), visibility (`PRIVATE`/`UNLISTED`), art_direction, current_source_id FK?, workflow_step (1–6, cache cho Map), version, deleted_at? | UC-02.02..05, UC-02.09, UC-04.05, UC-04.06 |
| `project_members` | (project_id FK, user_id FK) PK, role, joined_at, last_active_at | IC-01. UC-02.07, UC-02.08 |
| `invite_links` | id PK, project_id FK, token_hash UQ, created_by FK, revoked_at?, expires_at? | Chỉ lưu SHA-256 của token. UC-02.06 |
| `source_texts` | id PK, project_id FK, content, char_count, sha256, normalization_log, original_media_id FK? | Mỗi lần import một bản, luôn nguyên văn. UC-02.02, UC-03.01b |
| `chapters` | id PK, project_id FK, order_index, title, content, char_count, content_sha256, **media_status**, current_storyboard_id FK?, locked_by_job_id FK?, last_edited_by FK?, version | Nguồn nguyên văn duy nhất (D-05). IC-02, IC-03. UC-03.02..09, UC-05.07 |
| `chapter_versions` | id PK, chapter_id FK, version, title, content, edited_by FK | Giữ 50 bản gần nhất. UC-03.14 |
| `archives` | id PK, project_id FK, name, content, char_count, chapter_count, source (`MANUAL`/`CONFLICT`), created_by FK | Bất biến (BR-10). UC-03.11, UC-03.12, UC-02.10a |
| `notes` | id PK, project_id FK, author_id FK?, author_kind (`USER`/`DIRECTOR`), content, target_type (`PROJECT`/`CHAPTER`/`SHOT`), target_id? | UC-03.13, UC-07.08 |

### 3.3 Thế giới truyện — `erd-3-the-gioi-truyen`

| Bảng | Cột | Ghi chú / Use case |
|---|---|---|
| `styles` | id PK, code UQ, name, description, prompt_fragment, preview_media_id FK?, active | Cấu hình. UC-04.05, UC-10.04 |
| `library_assets` | id PK, owner_id FK, kind, name, aliases, appearance, facts, style_id FK?, reference_media_id FK?, use_exact_image, deleted_at? | Thư viện cá nhân. UC-08.01..05 |
| `story_assets` | id PK, project_id FK, kind, name, aliases, appearance, facts, current_image_id FK?, use_exact_image, source_library_asset_id FK?, version | UC-04.01..04 |
| `story_asset_group_members` | (group_asset_id FK, member_asset_id FK) PK | Nhóm có ≥ 2 thành viên. UC-04.02b |
| `asset_images` | id PK, story_asset_id FK, media_id FK, style_id FK?, prompt_snapshot, job_id FK? | Lịch sử ảnh tham chiếu. UC-04.03 |
| `visual_rules` | id PK, project_id FK, name, instruction, scope (`PROJECT`/`CHAPTER`), chapter_id FK?, active, order_index | BR-08. UC-04.10 |
| `chapter_rules` | id PK, chapter_id FK, instruction, order_index | UC-05.04 |
| `timeline_events` | id PK, project_id FK, chapter_id FK, day_label, season, story_date, summary, order_index | Dòng thời gian **truyện** (khác `timelines` của video). UC-04.07, UC-04.09 |
| `relationships` | id PK, project_id FK, asset_a_id FK, asset_b_id FK, label, dynamic, from_chapter_id FK? | UC-04.08, UC-04.09 |

### 3.4 Sinh tư liệu: storyboard, ảnh, thuyết minh — `erd-4-sinh-tu-lieu`

| Bảng | Cột | Ghi chú / Use case |
|---|---|---|
| `storyboard_drafts` | id PK, chapter_id FK, project_id FK, name, kind (`INITIAL`/`RESPLIT_MORE`/`RESPLIT_FEWER`/`DUPLICATE`), boundary_fixes, created_by FK? | `boundary_fixes` = số ranh giới validator đã sửa (cảnh báo > 20%). UC-05.01..03 |
| `shots` | id PK, draft_id FK, project_id FK, order_index, title, focus, time_of_day, story_date, brief, caption, **source_start, source_end, source_hash**, current_illustration_id FK?, current_narration_id FK?, version | IC-08. UC-05.01, UC-05.06 |
| `shot_asset_refs` | id PK, shot_id FK, story_asset_id FK?, raw_name, role (`CAST`/`ITEM`/`LOCATION`) | `story_asset_id` NULL = chưa liên kết (BR-16). UC-05.06b, UC-05.06f |
| `illustrations` | id PK, shot_id FK, media_id FK?, status, edit_kind (`GENERATE`/`EDIT`/`INPAINT`/`RETRY`), instruction?, mask_media_id FK?, prompt_snapshot, shot_version, parent_illustration_id FK?, job_id FK? | `shot_version` < `shots.version` = "brief đã đổi". UC-05.09, UC-05.10 |
| `narration_settings` | project_id PK/FK, language, voice_id FK?, speed, pitch, sentence_pause_ms, paragraph_pause_ms, wer_threshold (mặc định 0,03), multi_voice | 1–1 với project. UC-05.11 |
| `voices` | id PK, provider_id FK, code, name, language, gender, sample_media_id FK?, min_plan_code?, sample_wer?, enabled | Cấu hình. UC-05.11a, UC-10.05 |
| `pronunciation_entries` | id PK, project_id FK, written, spoken, kind (`ALIAS`/`PHONEME`), case_sensitive | Chỉ ảnh hưởng audio. UC-05.12 |
| `character_voices` | (project_id FK, story_asset_id FK) PK, voice_id FK | UC-05.15 |
| `dialogue_attributions` | id PK, shot_id FK, char_start, char_end, story_asset_id FK?, confirmed | Người nói của từng câu thoại (offset trong chương). UC-05.15 |
| `narrations` | id PK, shot_id FK, project_id FK, version_no, **source_hash**, spoken_text, ssml, normalization_log, voice_id FK?, media_id FK?, duration_ms, **word_timings**, wer, mismatches, status, accepted_by FK?, accepted_at?, job_id FK? | `spoken_text` = bản đọc do **server** sinh. IC-09. UC-05.13, UC-05.14 |

### 3.5 Trình chỉnh sửa & xuất video — `erd-5-trinh-chinh-sua-video`

| Bảng | Cột | Ghi chú / Use case |
|---|---|---|
| `timelines` | id PK, project_id FK, scope (`CHAPTER`/`PROJECT`), chapter_id FK?, aspect_ratio, framing (`CROP`/`FIT`/`BLUR`), subtitle_style, master (`{loudnessLufs, volume}`), status, version, updated_by FK? | Tự dựng khi chương `READY_TO_EDIT`. UC-06.01, UC-06.06, UC-06.08, UC-06.12 |
| `timeline_versions` | id PK, timeline_id FK, version, name?, snapshot, created_by FK? | Bất biến. UC-06.14, UC-02.10a |
| `timeline_tracks` | id PK, timeline_id FK, kind, name, order_index, muted, solo, hidden, locked, volume | Track `NARRATION`: `locked = true`, không xóa. UC-06.03 |
| `timeline_items` | id PK, track_id FK, kind, start_ms, duration_ms, source_in_ms, shot_id FK?, illustration_id FK?, narration_id FK?, audio_asset_id FK?, media_id FK? (logo), text?, text_style?, motion?, transition_in?, color?, volume, volume_keyframes?, fade_in_ms, fade_out_ms, ducking_db?, user_modified, sync_flag (`NONE`/`UPDATED`/`NEEDS_REVIEW`) | Một bảng cho mọi loại clip. IC-10. UC-06.02..10, UC-06.15 |
| `audio_assets` | id PK, owner_user_id FK? (NULL = hệ thống), kind (`MUSIC`/`SFX`), title, genre, mood, tags, media_id FK, duration_ms, waveform, license (`LIBRARY`/`USER_UPLOAD`/`AI_GENERATED`), license_note, published | BR-26. UC-06.11, UC-06.11a, UC-06.11b, UC-10.06 |
| `sfx_suggestions` | id PK, timeline_id FK, shot_id FK, at_ms, query, audio_asset_id FK?, status (`PROPOSED`/`ACCEPTED`/`REJECTED`), job_id FK? | Không tự chèn khi chưa duyệt. UC-06.11c |
| `renders` | id PK, timeline_id FK, timeline_version, project_id FK, render_group_id?, part_no?, version_no, is_primary, resolution, aspect_ratio, watermark, status, progress, media_id FK?, subtitle_srt_media_id FK?, subtitle_vtt_media_id FK?, narration_audio_media_id FK?, duration_ms, **coverage_chars, total_chars**, timeline_snapshot, job_id FK? | IC-11. `render_group_id` + `part_no` khi chia phần. UC-06.16, UC-06.16b, UC-06.17 |

### 3.6 Director, job & hạ tầng — `erd-6-director-job-ha-tang`

| Bảng | Cột | Ghi chú / Use case |
|---|---|---|
| `director_plans` | id PK, project_id FK, started_by FK, status, current_step (`pickStyle`/`split`/`cast`/`pickVoice`/`media`/`verify`/`draftTimeline`), awaiting_reason?, step_state, estimated_remaining_credits, version | UC-07.02..08 |
| `director_messages` | id PK, project_id FK, plan_id FK?, sender (`USER`/`DIRECTOR`/`TOOL`), user_id FK?, content, tool_call? | UC-07.01 |
| `director_tool_proposals` | id PK, message_id FK, tool, args, credit_cost, status (`PENDING`/`CONFIRMED`/`REJECTED`/`EXPIRED`), decided_by FK?, decided_at?, job_id FK? | Tool tốn phí chờ xác nhận. UC-07.01b |
| `jobs` | id PK, project_id FK?, user_id FK (người trả credit), type, status, priority, target_type, target_id, params, result, error_code?, error_message?, attempts, credit_cost, idempotency_key UQ, parent_job_id FK?, heartbeat_at?, started_at?, finished_at? | Job cha `GENERATE_MEDIA_CHAPTER` có job con. UC-05.07, UC-10.07 |
| `ai_providers` | id PK, code UQ, kind, enabled, priority, config_ref | `config_ref` = **tên** secret, không lưu key. UC-10.03 |
| `ai_models` | id PK, provider_id FK, code, display_name, capabilities, unit_cost_usd, enabled, user_selectable | UC-10.03 |
| `ai_usage_records` | id PK, job_id FK, provider_id FK?, model, unit (`TOKENS`/`IMAGES`/`SECONDS`/`CHARS`), quantity, cost_usd, latency_ms, request_id | Đối soát chi phí. UC-10.10 |
| `price_rules` | id PK, operation, formula, effective_from, effective_to?, created_by FK? | Có phiên bản theo ngày hiệu lực. UC-10.01 |
| `media_files` | id PK, owner_user_id FK?, owner_project_id FK?, storage_key UQ, mime, bytes, width?, height?, duration_ms?, sha256, storage_class (`HOT`/`COLD`) | D-06 |
| `outbox_events` | id PK, aggregate_type, aggregate_id, event_type, payload, published_at? | Outbox pattern (ADR-07): ghi cùng giao dịch, relay đẩy sang queue/SSE |
| `idempotency_keys` | (key, user_id FK) PK, request_hash, response_status, response_body, expires_at | Giữ 24 giờ (06 §1) |

## 4. Ràng buộc toàn vẹn

| Mã | Ràng buộc | Cách cài đặt |
|---|---|---|
| IC-01 | Mỗi project có đúng 1 thành viên `OWNER` | Partial unique index `(project_id) WHERE role='OWNER'` |
| IC-02 | `chapters.order_index` liên tục, duy nhất trong project | Unique DEFERRABLE INITIALLY DEFERRED; tái cấu trúc trong một giao dịch (UC-03.09) |
| IC-03 | Mỗi chương có tối đa 1 storyboard hiện hành | `chapters.current_storyboard_id` |
| IC-04 | `credit_balances.available ≥ 0`, `held ≥ 0` | CHECK + `SELECT … FOR UPDATE` khi HOLD |
| IC-05 | Mỗi job tốn phí có HOLD và đúng một trong CAPTURE / RELEASE | Reconciler định kỳ (`act-giu-tru-credit`) |
| IC-06 | `payments`: đúng một trong `plan_id`, `credit_pack_id` | CHECK |
| IC-07 | `payment_events.gateway_event_id` duy nhất | Unique index |
| **IC-08** | **Phủ kín:** shot của mỗi bản nháp, sắp theo `order_index`: `shot[0].source_start = 0`, `shot[i].source_end = shot[i+1].source_start`, `shot[last].source_end = char_length(chapter.content)` | Service (CoverageValidator) + constraint trigger DEFERRABLE |
| **IC-09** | `narrations` khác `OUTDATED` phải có `source_hash = shots.source_hash` | Service đặt `OUTDATED` khi chương đổi |
| **IC-10** | Timeline của chương: mỗi shot hiện hành có đúng 1 item `IMAGE` và 1 item `NARRATION`; item `NARRATION` đúng thứ tự, không chồng lấn, `duration_ms` = độ dài audio; item `IMAGE` phủ trọn khoảng đọc của shot | Service kiểm tra mỗi lần `apply-ops` (BR-24) |
| **IC-11** | Render chỉ được tạo khi `coverage_chars = total_chars` và IC-10 thỏa | Service (UC-06.16a) |
| IC-12 | `timeline_tracks`: mỗi timeline có đúng 1 track `NARRATION`, `locked = true` | Partial unique index + CHECK |
| IC-13 | `story_asset_group_members`: thành viên phải là `CHARACTER` cùng project, khác chính group | Trigger |
| IC-14 | `relationships.asset_a_id ≠ asset_b_id`, cùng project | CHECK + trigger |
| IC-15 | `audio_assets` có `license = USER_UPLOAD` thì `owner_user_id` NOT NULL; `published = false` không xuất hiện trong tìm kiếm | CHECK + điều kiện truy vấn |

## 5. Cột trạng thái ↔ sơ đồ trạng thái

| Cột | Sơ đồ | Ai đổi trạng thái |
|---|---|---|
| `chapters.media_status` | `state-chapter-media` | Orchestrator sinh tư liệu, trình chỉnh sửa, xuất video, sửa văn bản |
| `narrations.status` | `state-narration-render` (Narration) | Worker TTS/Align; Editor (`ACCEPTED`); service khi lệch hash (`OUTDATED`) |
| `renders.status` | `state-narration-render` (Render) | Render Worker |
| `jobs.status` | `state-job` | Worker, reconciler |
| `director_plans.status` | `state-director-plan` | Director module |
| `subscriptions.status` | `state-subscription` | Webhook thanh toán |

## 6. Chỉ mục đề xuất

- `chapters (project_id, order_index)`; `chapters (project_id, media_status)`
- `shots (draft_id, order_index)`
- `narrations (shot_id, version_no DESC)`; `narrations (project_id, status) WHERE status IN ('NEEDS_REVIEW','OUTDATED','FAILED')`
- `timeline_items (track_id, start_ms)`
- `audio_assets USING gin (tags)`, `audio_assets (kind, published)`, `audio_assets USING gin (to_tsvector('simple', title))`
- `jobs (status, priority, created_at) WHERE status IN ('QUEUED','RUNNING','RETRYING')`; `jobs (project_id, created_at DESC)`; `jobs (heartbeat_at) WHERE status = 'RUNNING'`
- `credit_ledger_entries (user_id, created_at DESC)`
- `outbox_events (published_at) WHERE published_at IS NULL`
- `idempotency_keys (expires_at)`
- `story_assets USING gin (aliases)`; `chapters USING gin (to_tsvector('simple', content))` cho Find & replace

## 7. Lưu trữ & vòng đời dữ liệu

| Dữ liệu | Thời gian giữ |
|---|---|
| Ảnh, audio thuyết minh, render không phải phiên bản hiện hành | 90 ngày, sau đó chuyển `storage_class = COLD` [ĐX] |
| `chapter_versions` | 50 bản gần nhất mỗi chương |
| `timeline_versions` | 100 bản gần nhất mỗi timeline; bản có tên giữ vĩnh viễn |
| Dự án đã xóa (soft delete) | 30 ngày, sau đó xóa cứng cùng media |
| Người dùng yêu cầu xóa dữ liệu | 30 ngày (khôi phục được), sau đó xóa hoặc ẩn danh hóa |
| `credit_ledger_entries`, `payments` | 10 năm (yêu cầu kế toán; ẩn danh hóa khi người dùng bị xóa) |
| `audit_logs` | 2 năm |
| `ai_usage_records` | 24 tháng |
| `outbox_events` đã publish | 7 ngày |
| `idempotency_keys` | 24 giờ |

## 8. Thay đổi so với bản trước (1.x → 2.0)

| Loại | Nội dung |
|---|---|
| Bảng mới | `audit_logs`, `outbox_events`, `idempotency_keys`, `director_tool_proposals`, `sfx_suggestions`, `dialogue_attributions`; đưa `ai_providers`, `ai_models`, `price_rules` vào ERD |
| Cột mới | `users.gateway_customer_id`, `last_daily_claim_on`, `deletion_requested_at`; `user_sessions.last_seen_at`; `projects.cover_media_id`, `workflow_step`; `chapters.content_sha256`, `media_status`; `library_assets.style_id`; `asset_images.prompt_snapshot`; `visual_rules.order_index`; `storyboard_drafts.boundary_fixes`; `illustrations.instruction`, `mask_media_id`, `shot_version`; `voices.min_plan_code`, `sample_wer`; `narrations.normalization_log`; `timeline_tracks.solo`; `timeline_items.media_id`, `text`, `sync_flag`; `audio_assets.genre`, `published`; `renders.render_group_id`, `part_no`, `watermark`; `director_plans.estimated_remaining_credits`; `jobs.heartbeat_at`; `ai_models.unit_cost_usd`; `media_files.storage_class` |
| Bỏ | `projects.status` (thay bằng `workflow_step` + `chapters.media_status`); `director_plans.target` (Director chỉ còn một luồng); các bảng sách/slideshow/video AI từ các bản trước |
| Đổi tên nhóm | ERD chia 6 nhóm theo luồng: Tài khoản, Dự án & bản thảo, Thế giới truyện, Sinh tư liệu, Trình chỉnh sửa & xuất video, Director/job/hạ tầng |
