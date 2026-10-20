# 04 — Mô hình dữ liệu

> **Phiên bản mô hình:** 2.2 (khớp luồng Studio 6 bước, use case ở [03](03-dac-ta-use-case/00-muc-luc.md) và các quyết định ở [sổ quyết định](../quyet-dinh.md)). Bảng chỉ dùng sau MVP vẫn giữ trong mô hình và được đánh dấu *(sau MVP)*; ERD MVP (`../so-do/mvp/02-du-lieu/erd-mvp.puml`) sinh tự động bằng `python3 so-do/tools/gen_mvp.py` dựa trên các đánh dấu này.
> **Sơ đồ:** `../so-do/02-du-lieu/domain-class.puml` (mô hình miền); `../so-do/02-du-lieu/erd.puml` (mô hình vật lý đầy đủ, 56 bảng); ERD theo nhóm `../so-do/02-du-lieu/erd-1..6-*.puml`, sinh tự động từ `erd.puml` bằng `python3 so-do/tools/split_erd.py`. Chỉ sửa `erd.puml` rồi chạy lại script.
> **CSDL:** PostgreSQL 16. Khóa chính `uuid` (UUIDv7). Mọi bảng có thêm `created_at`, `updated_at` (`timestamptz`, không liệt kê ở dưới).

## 1. Nguyên tắc thiết kế

| # | Nguyên tắc |
|---|---|
| D-01 | Chuẩn hóa 3NF. Cấu trúc linh hoạt (brief, motion, style phụ đề, cài đặt) dùng `jsonb` có JSON Schema kiểm tra ở tầng ứng dụng. |
| D-02 | **Khóa lạc quan:** bảng có thể bị sửa đồng thời có cột `version int` (`projects`, `chapters`, `story_assets`, `shots`, `timelines`, `director_plans`); API dùng `If-Match`. |
| D-03 | **Bất biến (chỉ INSERT):** `archives`, `chapter_versions`, `timeline_versions`, `wallet_ledger_entries`, `payment_events`, `audit_logs`. |
| D-04 | **Phiên bản hóa đầu ra AI:** ảnh (`illustrations`, `asset_images`), thuyết minh (`narrations`) và bản xuất (`renders`) không ghi đè; mỗi lần sinh tạo bản ghi mới, bảng cha trỏ bản hiện hành. |
| D-05 | **Nguyên văn được bảo vệ bằng dữ liệu:** `chapters.content` là nguồn duy nhất; shot chỉ lưu offset + hash (`source_start`, `source_end`, `source_hash`); thuyết minh lưu `source_hash` để phát hiện lệch. Không có cột nào chứa "văn bản đọc" do client gửi (BR-19). |
| D-06 | File nhị phân nằm ở object storage; DB chỉ lưu `media_files` (key, mime, kích thước, checksum). |
| D-07 | Bảng thuộc dự án có `project_id` (trực tiếp hoặc qua bảng cha) để phân quyền; RLS của Postgres là lớp bảo vệ thứ hai [ĐX], **sau MVP** (ADR-23). |
| D-08 | Xóa mềm (`deleted_at`) cho `projects`, `library_assets`; người dùng xóa dữ liệu dùng `users.status = DELETED` + `deletion_requested_at`. |
| D-09 | **Tiền lưu bằng số nguyên micro-USD** (`bigint`, 1 USD = 1.000.000) ở mọi cột hậu tố `_micro`; không dùng số thực cho tiền. Chi phí thực của provider (`ai_usage_records.cost_usd`) giữ kiểu `numeric` để không mất độ chính xác khi nhân 110% (QĐ-30, QĐ-31). |
| D-10 | **Mọi offset và độ dài văn bản tính theo code unit UTF-16** (chỉ số chuỗi JavaScript) trên văn bản NFC: `shots.source_start/end`, `word_timings.charStart/End`, cue phụ đề, `char_count` của `chapters`, `source_texts`, `archives` (ADR-26). Giá trị do **ứng dụng** tính và ghi; **không** dùng `char_length()` / `substring()` của Postgres (đếm code point) để so khớp hay cắt văn bản. Thành phần ngoài TypeScript (Alignment Worker Python) nhận và trả offset đã đổi sang UTF-16 qua hàm chuyển đổi dùng chung có test. Giới hạn "ký tự" ở 08 §5 cũng đếm theo đơn vị này. |

## 2. Kiểu liệt kê (enum)

| Enum | Giá trị | Dùng ở |
|---|---|---|
| `user_role` | `USER`, `ADMIN` | users |
| `user_status` | `ACTIVE`, `LOCKED`, `DELETED` | users |
| `sub_status` | `INCOMPLETE`, `ACTIVE`, `PAST_DUE`, `CANCEL_AT_PERIOD_END`, `CANCELED`, `EXPIRED` | subscriptions (`state-subscription`) |
| `payment_kind` | `TOPUP`, `SUBSCRIPTION` *(sau MVP)* | payments |
| `ledger_type` | `TRIAL_GRANT`, `TOPUP`, `HOLD`, `CAPTURE`, `RELEASE`, `ADJUST` *(sau MVP)*, `REFUND` *(sau MVP)* | wallet_ledger_entries (08 §4 WR-02) |
| `member_role` | `OWNER`, `EDITOR` | project_members |
| `chapter_media_status` | `DRAFT`, `GENERATING`, `NEEDS_ATTENTION`, `READY_TO_EDIT`, `EDITING`, `EXPORTED`, `OUTDATED` | chapters (`state-chapter-media`) |
| `asset_kind` | `CHARACTER`, `LOCATION`, `PROP`, `GROUP` | story_assets, library_assets |
| `media_status` | `PENDING`, `GENERATING`, `DONE`, `FAILED` | illustrations |
| `narration_status` | `PENDING`, `GENERATING`, `DONE`, `FAILED`, `OUTDATED`; khi bật kiểm chứng ASR *(sau MVP)*: `VERIFIED`, `NEEDS_REVIEW`, `ACCEPTED` thay cho `DONE` | narrations (`state-narration-render`) |
| `timeline_status` | `DRAFT`, `READY_TO_EXPORT` | timelines |
| `track_kind` | `VIDEO`, `OVERLAY`, `SUBTITLE`, `NARRATION`, `MUSIC`, `SFX` | timeline_tracks |
| `item_kind` | `IMAGE`, `NARRATION`, `TITLE`, `TEXT`, `LOGO`, `AUDIO` | timeline_items |
| `render_status` | `QUEUED`, `RENDERING`, `READY`, `FAILED`, `CANCELLED` | renders |
| `plan_status` | `RUNNING`, `AWAITING_INPUT`, `PAUSED`, `COMPLETED`, `CANCELLED` | director_plans (`state-director-plan`) |
| `job_status` | `QUEUED`, `RUNNING`, `RETRYING`, `SUCCEEDED`, `FAILED`, `CANCELLED` | jobs (`state-job`) |
| `provider_kind` | `LLM`, `IMAGE`, `TTS`, `STT`, `ALIGNER` | ai_providers |

Các cột kiểu `text` có tập giá trị cố định (vd. `storyboard_drafts.kind`, `timelines.scope`) được kiểm tra bằng `CHECK` và liệt kê ở cột Ghi chú.

## 3. Từ điển dữ liệu

Ký hiệu: **PK** khóa chính, **FK** khóa ngoại, **UQ** duy nhất, `?` cho phép NULL.

### 3.1 Tài khoản, ví & thanh toán — `erd-1-tai-khoan-vi`

| Bảng | Cột | Ghi chú / Use case |
|---|---|---|
| `users` | id PK, sso_subject UQ (= claim `sub`), email, display_name, avatar_url, locale, role, status, gateway_customer_id?, last_login_at, consented_at?, consent_version?, deletion_requested_at? | Hồ sơ cục bộ, **không lưu mật khẩu**. `consented_at` NULL = chưa đồng ý xử lý dữ liệu (BR-31). UC-01.01b (JIT), UC-01.01d (đồng ý), UC-01.06 (xóa dữ liệu) |
| `beta_invites` | id PK, email UQ (citext, chữ thường), invited_by FK?, note?, used_by_user_id FK?, revoked_at? | Danh sách mời closed beta (BR-30). `used_by_user_id` ghi khi hồ sơ được tạo; gỡ = đặt `revoked_at`. UC-01.01b, UC-10.11 |
| `user_sessions` | id PK, user_id FK, session_hash UQ, sso_sid?, refresh_token_enc, id_token_hint_enc, expires_at, revoked_at?, last_seen_at | Phiên BFF; token mã hóa AES-GCM. UC-01.01, UC-01.02, UC-01.07 |
| `plans` *(sau MVP)* | id PK, code UQ, name, price_monthly, price_annual, gateway_price_ids, features, active | `features`: max_projects, max_members, max_resolution, watermark, premium_voices, queue_priority. UC-10.02. MVP dùng hai trạng thái Free / Đã nạp tiền suy từ `wallets.topup_total_micro` (BR-27), không có bảng gói |
| `subscriptions` *(sau MVP)* | id PK, user_id FK, plan_id FK, status, billing_cycle (`MONTHLY`/`ANNUAL`), current_period_start, current_period_end, cancel_at_period_end, gateway_subscription_id UQ | UC-09.02, UC-09.04, UC-09.08a |
| `payments` | id PK, user_id FK, kind, plan_id FK?, amount_micro, currency (`USD`), status, gateway_ref | `kind = TOPUP` thì `plan_id` NULL (IC-06). UC-09.03, UC-09.08a |
| `payment_events` | id PK, gateway_event_id UQ, type, payload, processed_at? | Idempotency webhook. UC-09.08 |
| `wallets` | user_id PK/FK, available_micro, held_micro, topup_total_micro, version | Một ví mỗi người dùng; cập nhật cùng giao dịch với sổ cái (WR-01). `topup_total_micro > 0` ⇔ "Đã nạp tiền". UC-09.05 |
| `wallet_ledger_entries` | id PK, user_id FK, entry_type, amount_micro (có dấu), job_id FK?, payment_id FK?, project_id FK?, actor_id FK?, reason? | Append-only. `TRIAL_GRANT` và `TOPUP` là hai loại khác nhau (QĐ-38). UC-05.17, UC-09.06, UC-10.08 |
| `audit_logs` | id PK, actor_id FK, action, target_type, target_id?, before?, after?, reason?, ip? | Append-only, giữ 2 năm. UC-10.09 |

### 3.2 Dự án & bản thảo — `erd-2-du-an-ban-thao`

| Bảng | Cột | Ghi chú / Use case |
|---|---|---|
| `projects` | id PK, owner_id FK, title, cover_media_id FK?, style_id FK?, image_model_id FK?, language, target_shot_seconds (mặc định 20, khoảng 3 ảnh/phút, QĐ-112), aspect_ratio (`16:9`/`9:16`/`1:1`), visibility (`PRIVATE`/`UNLISTED`), art_direction, current_source_id FK?, workflow_step (1–6, cache cho Map), version, deleted_at? | UC-02.02..05, UC-02.09, UC-04.05, UC-04.06 |
| `project_members` | (project_id FK, user_id FK) PK, role, joined_at, last_active_at | IC-01. UC-02.07, UC-02.08 |
| `invite_links` *(sau MVP)* | id PK, project_id FK, token_hash UQ, created_by FK, revoked_at?, expires_at? | Chỉ lưu SHA-256 của token. UC-02.06 |
| `source_texts` | id PK, project_id FK, content, char_count, sha256, normalization_log, original_media_id FK? | Mỗi lần import một bản, luôn nguyên văn. UC-02.02, UC-03.01b |
| `chapters` | id PK, project_id FK, order_index, title, content, char_count, content_sha256, **media_status**, current_storyboard_id FK?, locked_by_job_id FK?, last_edited_by FK?, version | Nguồn nguyên văn duy nhất (D-05). IC-02, IC-03. UC-03.02..09, UC-05.07 |
| `chapter_versions` | id PK, chapter_id FK, version, title, content, edited_by FK | Giữ 50 bản gần nhất. UC-03.14 |
| `archives` *(sau MVP)* | id PK, project_id FK, name, content, char_count, chapter_count, source (`MANUAL`/`CONFLICT`), created_by FK | Bất biến (BR-10). UC-03.11, UC-03.12, UC-02.10a |
| `notes` *(sau MVP)* | id PK, project_id FK, author_id FK?, author_kind (`USER`/`DIRECTOR`), content, target_type (`PROJECT`/`CHAPTER`/`SHOT`), target_id? | UC-03.13, UC-07.08 |

### 3.3 Thế giới truyện — `erd-3-the-gioi-truyen`

| Bảng | Cột | Ghi chú / Use case |
|---|---|---|
| `styles` | id PK, code UQ, name, description, prompt_fragment, preview_media_id FK?, active | Cấu hình. UC-04.05, UC-10.04 |
| `library_assets` *(sau MVP)* | id PK, owner_id FK, kind, name, aliases, appearance, facts, style_id FK?, reference_media_id FK?, use_exact_image, deleted_at? | Thư viện cá nhân. UC-08.01..05 |
| `story_assets` | id PK, project_id FK, kind, name, aliases, appearance, facts, current_image_id FK?, use_exact_image, source_library_asset_id FK?, version | UC-04.01..04 |
| `story_asset_group_members` | (group_asset_id FK, member_asset_id FK) PK | Nhóm có ≥ 2 thành viên. UC-04.02b |
| `asset_images` | id PK, story_asset_id FK, media_id FK, style_id FK?, prompt_snapshot, job_id FK? | Lịch sử ảnh tham chiếu. UC-04.03 |
| `visual_rules` | id PK, project_id FK, name, instruction, scope (`PROJECT`/`CHAPTER`), chapter_id FK?, active, order_index | BR-08. UC-04.10 |
| `chapter_rules` *(sau MVP)* | id PK, chapter_id FK, instruction, order_index | UC-05.04 |
| `timeline_events` | id PK, project_id FK, chapter_id FK, day_label, season, story_date, summary, order_index, chrono_index | Dòng thời gian **truyện** (khác `timelines` của video). `order_index` = thứ tự theo mạch truyện; `chrono_index` = thứ hạng theo thời gian trong truyện do AI gán khi phân tích (`story_date` là text tự do, không dùng để sắp xếp); NULL = chưa xác định. UC-04.07, UC-04.09 |
| `relationships` | id PK, project_id FK, asset_a_id FK, asset_b_id FK, label, dynamic, from_chapter_id FK? | UC-04.08, UC-04.09 |

### 3.4 Sinh tư liệu: storyboard, ảnh, thuyết minh — `erd-4-sinh-tu-lieu`

| Bảng | Cột | Ghi chú / Use case |
|---|---|---|
| `storyboard_drafts` | id PK, chapter_id FK, project_id FK, name, kind (`INITIAL`/`RESPLIT_MORE`/`RESPLIT_FEWER`/`DUPLICATE`), boundary_fixes, segmenter_version, created_by FK? | `boundary_fixes` = số ranh giới validator đã sửa (cảnh báo > 20%). `segmenter_version` = phiên bản `SentenceSegmenter` đã dùng (12 §1.1). UC-05.01..03 |
| `shots` | id PK, draft_id FK, project_id FK, order_index, title, focus, time_of_day, story_date, brief, caption, **source_start, source_end, source_hash**, current_illustration_id FK?, current_narration_id FK?, version | IC-08. UC-05.01, UC-05.06 |
| `shot_asset_refs` | id PK, shot_id FK, story_asset_id FK?, raw_name, role (`CAST`/`ITEM`/`LOCATION`) | `story_asset_id` NULL = chưa liên kết (BR-16). UC-05.06b, UC-05.06f |
| `illustrations` | id PK, shot_id FK, media_id FK?, status, edit_kind (`GENERATE`/`EDIT`/`RETRY`/`UPLOAD`), instruction?, prompt_snapshot, shot_version, parent_illustration_id FK?, job_id FK? | `shot_version` < `shots.version` = "brief đã đổi" (bản `UPLOAD` đặt `shot_version = shots.version`, `prompt_snapshot`/`job_id` rỗng, `status = DONE`). UC-05.09, UC-05.10 |
| `narration_settings` | project_id PK/FK, language, voice_id FK?, speed, pitch, sentence_pause_ms, paragraph_pause_ms, symbol_rules, wer_threshold (mặc định 0,03, sau MVP), multi_voice (sau MVP) | 1–1 với project. `symbol_rules`: `{SYM-01: true, …}` bật/tắt từng mẫu ký hiệu (08 §6); thiếu khóa = bật. UC-05.11 |
| `voices` | id PK, provider_id FK, code, name, language, gender, sample_media_id FK?, min_plan_code?, sample_wer?, enabled | Cấu hình. UC-05.11a, UC-10.05 |
| `pronunciation_entries` | id PK, project_id FK, written, spoken, kind (`ALIAS`/`PHONEME`), case_sensitive | Chỉ ảnh hưởng audio. TTS tự host (MVP) bỏ qua `PHONEME` (ADR-30). UC-05.12 |
| `character_voices` *(sau MVP)* | (project_id FK, story_asset_id FK) PK, voice_id FK | UC-05.15 |
| `dialogue_attributions` *(sau MVP)* | id PK, shot_id FK, char_start, char_end, story_asset_id FK?, confirmed | Người nói của từng câu thoại (offset trong chương). UC-05.15 |
| `narrations` | id PK, shot_id FK, project_id FK, version_no, **source_hash**, spoken_text, ssml, normalization_log, voice_id FK?, media_id FK?, duration_ms, **word_timings**, status, flagged_at?, wer?, mismatches?, accepted_by FK?, accepted_at?, job_id FK? | `spoken_text` = bản đọc do **server** sinh. `flagged_at` ≠ NULL = người dùng đánh dấu cần sinh lại (BR-34). `wer`, `mismatches`, `accepted_*` dùng khi bật kiểm chứng ASR (sau MVP). IC-09. UC-05.13, UC-05.18 |

### 3.5 Trình chỉnh sửa & xuất video — `erd-5-trinh-chinh-sua-video`

| Bảng | Cột | Ghi chú / Use case |
|---|---|---|
| `timelines` | id PK, project_id FK, scope (`CHAPTER`; `PROJECT` sau MVP, QĐ-141), chapter_id FK?, aspect_ratio, framing (`CROP`/`FIT`/`BLUR`), subtitle_style, master (`{loudnessLufs, volume}`), status, version, updated_by FK? | Tự dựng khi chương `READY_TO_EDIT`. UC-06.01, UC-06.06, UC-06.08, UC-06.12 |
| `timeline_versions` *(sau MVP)* | id PK, timeline_id FK, version, name?, snapshot, created_by FK? | Bất biến. UC-06.14, UC-02.10a |
| `timeline_tracks` | id PK, timeline_id FK, kind, name, order_index, muted, solo, hidden, locked, volume | Track `NARRATION`: `locked = true`, không xóa. UC-06.03 |
| `timeline_items` | id PK, track_id FK, kind, start_ms, duration_ms, source_in_ms, shot_id FK?, illustration_id FK?, narration_id FK?, audio_asset_id FK?, media_id FK? (logo), text?, text_style?, motion?, transition_in?, color?, volume, volume_keyframes?, fade_in_ms, fade_out_ms, ducking_db?, user_modified, sync_flag (`NONE`/`UPDATED`/`NEEDS_REVIEW`) | Một bảng cho mọi loại clip. IC-10. UC-06.02..10, UC-06.15 |
| `audio_assets` | id PK, owner_user_id FK? (NULL = hệ thống), kind (`MUSIC`/`SFX`), title, genre, mood, tags, media_id FK, duration_ms, waveform, license (`USER_UPLOAD`; `LIBRARY_CC0`/`LIBRARY_CC_BY` sau MVP), license_note (tác giả, nguồn, dòng ghi công CC-BY), published | BR-26. MVP chỉ có file người dùng tải lên. UC-06.11, UC-06.11a, UC-10.06 |
| `renders` | id PK, scope (`CHAPTER`/`PROJECT`), timeline_id FK? (NULL khi `PROJECT`), timeline_version?, project_id FK, render_group_id?, part_no?, version_no, is_primary, resolution, aspect_ratio, watermark, status, progress, media_id FK?, subtitle_srt_media_id FK?, subtitle_vtt_media_id FK?, narration_audio_media_id FK?, duration_ms, **coverage_chars, total_chars**, timeline_snapshot, job_id FK? | IC-11. `scope = PROJECT`: xuất cả dự án, ghép timeline các chương; `timeline_snapshot.sourceTimelines` ghi timeline và phiên bản của từng chương (QĐ-141). `render_group_id` + `part_no` khi chia phần. UC-06.16, UC-06.16b, UC-06.17 |

### 3.6 Director, job & hạ tầng — `erd-6-director-job-ha-tang`

| Bảng | Cột | Ghi chú / Use case |
|---|---|---|
| `director_plans` *(sau MVP)* | id PK, project_id FK, started_by FK, status, current_step (`pickStyle`/`split`/`cast`/`pickVoice`/`media`/`verify`/`draftTimeline`), awaiting_reason?, step_state, estimated_remaining_micro, version | UC-07.02..08 |
| `director_messages` *(sau MVP)* | id PK, project_id FK, plan_id FK?, sender (`USER`/`DIRECTOR`/`TOOL`), user_id FK?, content, tool_call? | UC-07.01 |
| `director_tool_proposals` *(sau MVP)* | id PK, message_id FK, tool, args, estimated_cost_micro, status (`PENDING`/`CONFIRMED`/`REJECTED`/`EXPIRED`), decided_by FK?, decided_at?, job_id FK? | Tool tốn phí chờ xác nhận. UC-07.01b |
| `jobs` | id PK, project_id FK?, user_id FK (người trả tiền), type, status, priority, target_type, target_id, params, result, error_code?, error_message?, attempts, held_micro (giá ước tính đã giữ), charged_micro? (số đã trừ = chi phí thực × 110%, ≤ `held_micro`), budget_day?, budget_reserved_micro? (chỗ đã giữ trong trần ngày, tính theo chi phí provider chưa cộng phí; ADR-25), idempotency_key UQ, parent_job_id FK?, heartbeat_at?, started_at?, finished_at? | `type`: danh mục và handler ở 05 §5.1, ánh xạ sang thao tác tính phí ở 08 §3.2. Job cha `GENERATE_MEDIA_CHAPTER` có job con. Job miễn phí (`PROCESS_AUDIO_UPLOAD`, `RENDER_TIMELINE`) và **job con** của Flow (`parent_job_id` ≠ NULL) có `held_micro = 0`, không giữ chỗ trần ngày; tiền nằm ở job gốc (WR-05). UC-05.07, UC-05.17, UC-10.07 |
| `ai_providers` | id PK, code UQ, kind, enabled, priority, config_ref | `config_ref` = **tên** secret, không lưu key. UC-10.03 |
| `ai_models` | id PK, provider_id FK, code, display_name, capabilities, unit_cost_usd, enabled, user_selectable | UC-10.03 |
| `ai_usage_records` | id PK, job_id FK, provider_id FK?, model, prompt_version?, seed?, unit (`TOKENS`/`IMAGES`/`SECONDS`/`CHARS`), quantity, cost_usd, latency_ms, request_id, attempt, succeeded | Mỗi lần gọi provider một dòng, kể cả lần lỗi; `attempt` = lần thử của job (ADR-29). CAPTURE chỉ tính các dòng `succeeded` của lần thử thành công (WR-09); tổng mọi dòng tính vào `daily_ai_budgets.spent_micro`. `prompt_version`, `seed` để tái lập kết quả LLM/ảnh (QĐ-127). TTS tự host ghi `SECONDS` = giây GPU (QĐ-123). Đối soát chi phí. UC-10.10 |
| `price_rules` | id PK, operation, formula, effective_from, effective_to?, created_by FK? | `formula` gồm hệ số (1,10), cơ sở tính chi phí và giới hạn đầu ra để ước tính (08 §3.2). Có phiên bản theo ngày hiệu lực; MVP nạp từ file seed. UC-10.01 |
| `daily_ai_budgets` | day PK (ngày giờ Việt Nam), cap_micro, reserved_micro, spent_micro, alert_80_sent_at?, alert_100_sent_at? | **Bộ đếm nguyên tử** cho trần chi tiêu ngày (BR-29, IC-18): giữ chỗ bằng một câu `UPDATE … WHERE spent + reserved + x ≤ cap` trong cùng giao dịch với HOLD. Tạo dòng của ngày khi cần (`INSERT … ON CONFLICT DO NOTHING`). UC-05.17, UC-10.12 |
| `system_settings` | key PK, value, updated_by FK? | Cấu hình vận hành: `daily_ai_budget_usd` (mặc định 10, BR-29), `beta_invite_only` (true, BR-30), `consent_notice_version`, `vnd_rate`. MVP sửa bằng file seed/CLI. UC-10.11, UC-10.12 |
| `media_files` | id PK, owner_user_id FK?, owner_project_id FK?, storage_key UQ, mime, bytes, width?, height?, duration_ms?, sha256, storage_class (`HOT`/`COLD`) | D-06 |
| `outbox_events` *(dùng sau MVP; ADR-23)* | id PK, aggregate_type, aggregate_id, event_type, payload, published_at? | Outbox pattern (ADR-07): ghi cùng giao dịch, relay đẩy sang queue/SSE |
| `idempotency_keys` | (key, user_id FK) PK, request_hash, response_status, response_body, expires_at | Giữ 24 giờ (06 §1) |

## 4. Ràng buộc toàn vẹn

| Mã | Ràng buộc | Cách cài đặt |
|---|---|---|
| IC-01 | Mỗi project có đúng 1 thành viên `OWNER` | Partial unique index `(project_id) WHERE role='OWNER'` |
| IC-02 | `chapters.order_index` liên tục, duy nhất trong project | Unique DEFERRABLE INITIALLY DEFERRED; tái cấu trúc trong một giao dịch (UC-03.09) |
| IC-03 | Mỗi chương có tối đa 1 storyboard hiện hành | `chapters.current_storyboard_id` |
| IC-04 | `wallets.available_micro ≥ 0`, `held_micro ≥ 0`, `topup_total_micro ≥ 0` | CHECK + `SELECT … FOR UPDATE` khi HOLD |
| IC-05 | Mỗi job **gốc** tốn phí (`parent_job_id` NULL) có đúng một HOLD; job con không có bút toán; khi kết thúc, tổng CAPTURE + RELEASE bằng số đã HOLD, và CAPTURE ≤ HOLD | Service + reconciler định kỳ (`act-giu-tru-tien`) |
| IC-06 | `payments`: `kind = TOPUP` thì `plan_id` NULL; `kind = SUBSCRIPTION` thì `plan_id` NOT NULL | CHECK |
| IC-07 | `payment_events.gateway_event_id` duy nhất | Unique index |
| **IC-08** | **Phủ kín:** shot của mỗi bản nháp, sắp theo `order_index`: `shot[0].source_start = 0`, `shot[i].source_end = shot[i+1].source_start`, `shot[last].source_end = chapters.char_count` (độ dài UTF-16, D-10) | Service (CoverageValidator) trong cùng giao dịch ghi; constraint trigger DEFERRABLE sau MVP (ADR-23) |
| **IC-09** | `narrations` khác `OUTDATED` phải có `source_hash = shots.source_hash` | Service đặt `OUTDATED` khi chương đổi |
| **IC-10** | Timeline của chương: mỗi shot hiện hành có đúng 1 item `IMAGE` và 1 item `NARRATION`; item `NARRATION` đúng thứ tự, không chồng lấn, `duration_ms` = độ dài audio; item `IMAGE` phủ trọn khoảng đọc của shot | Service kiểm tra mỗi lần `apply-ops` (BR-24) |
| **IC-11** | Render chỉ được tạo khi `coverage_chars = total_chars` và IC-10 thỏa | Service (UC-06.16a) |
| IC-12 | `timeline_tracks`: mỗi timeline có đúng 1 track `NARRATION`, `locked = true` | Partial unique index + CHECK |
| IC-13 | `story_asset_group_members`: thành viên phải là `CHARACTER` cùng project, khác chính group | Trigger |
| IC-14 | `relationships.asset_a_id ≠ asset_b_id`, cùng project | CHECK + trigger |
| IC-15 | `audio_assets` có `license = USER_UPLOAD` thì `owner_user_id` NOT NULL; `published = false` không xuất hiện trong tìm kiếm | CHECK + điều kiện truy vấn |
| IC-16 | Mỗi người dùng có đúng một `TRIAL_GRANT` trong đời tài khoản; không tạo lại cho cùng email đã nhận (BR-28) | Partial unique index `(user_id) WHERE entry_type='TRIAL_GRANT'` + kiểm tra `beta_invites.used_by_user_id` |
| IC-17 | *(Đã bỏ, QĐ-140: không còn tốc độ từng clip.)* | — |
| IC-18 | `daily_ai_budgets`: `reserved_micro ≥ 0`, `spent_micro ≥ 0`, `spent_micro + reserved_micro ≤ cap_micro` tại mọi thời điểm giữ chỗ | CHECK + câu `UPDATE` có điều kiện (05 §6.1, ADR-25) |

## 5. Cột trạng thái ↔ sơ đồ trạng thái

| Cột | Sơ đồ | Ai đổi trạng thái |
|---|---|---|
| `chapters.media_status` | `state-chapter-media` | Orchestrator sinh tư liệu, trình chỉnh sửa, xuất video, sửa văn bản |
| `narrations.status` | `state-narration-render` (Narration) | Worker TTS/Align (`DONE`); service khi lệch hash (`OUTDATED`); sau MVP: Editor (`ACCEPTED`) |
| `renders.status` | `state-narration-render` (Render) | Render Worker |
| `jobs.status` | `state-job` | Worker, reconciler |
| `director_plans.status` | `state-director-plan` | Director module |
| `subscriptions.status` *(sau MVP)* | `state-subscription` | Webhook thanh toán |

## 6. Chỉ mục đề xuất

- `chapters (project_id, order_index)`; `chapters (project_id, media_status)`
- `shots (draft_id, order_index)`
- `narrations (shot_id, version_no DESC)`; `narrations (project_id, status) WHERE status IN ('OUTDATED','FAILED')`; `narrations (project_id) WHERE flagged_at IS NOT NULL`
- `timeline_items (track_id, start_ms)`
- `audio_assets USING gin (tags)`, `audio_assets (kind, published)`, `audio_assets USING gin (to_tsvector('simple', title))`
- `jobs (status, priority, created_at) WHERE status IN ('QUEUED','RUNNING','RETRYING')`; `jobs (project_id, created_at DESC)`; `jobs (heartbeat_at) WHERE status = 'RUNNING'`
- `wallet_ledger_entries (user_id, created_at DESC)`; `ai_usage_records (created_at)` để reconciler đối chiếu `daily_ai_budgets.spent_micro` (BR-29, ADR-25)
- `outbox_events (published_at) WHERE published_at IS NULL` *(sau MVP)*
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
| **Toàn bộ dữ liệu closed beta** | Xóa sau ngày bảo vệ đồ án, theo thông báo người dùng đã đồng ý (BR-31) |
| `wallet_ledger_entries`, `payments` | Đến khi xóa dữ liệu beta (thanh toán sandbox, không có nghĩa vụ kế toán); sản phẩm thật: 10 năm, ẩn danh hóa khi người dùng bị xóa |
| `audit_logs` | 2 năm |
| `ai_usage_records` | 24 tháng |
| `outbox_events` đã publish *(sau MVP)* | 7 ngày |
| `idempotency_keys` | 24 giờ |

## 8. Lịch sử thay đổi mô hình

| Phiên bản | Nội dung |
|---|---|
| 1.x → 2.0: bảng mới | `audit_logs`, `outbox_events`, `idempotency_keys`, `director_tool_proposals`, `sfx_suggestions`, `dialogue_attributions`; đưa `ai_providers`, `ai_models`, `price_rules` vào ERD |
| 1.x → 2.0: cột mới | `users.gateway_customer_id`, `last_daily_claim_on`, `deletion_requested_at`; `user_sessions.last_seen_at`; `projects.cover_media_id`, `workflow_step`; `chapters.content_sha256`, `media_status`; `library_assets.style_id`; `asset_images.prompt_snapshot`; `visual_rules.order_index`; `storyboard_drafts.boundary_fixes`; `illustrations.instruction`, `mask_media_id`, `shot_version`; `voices.min_plan_code`, `sample_wer`; `narrations.normalization_log`; `timeline_tracks.solo`; `timeline_items.media_id`, `text`, `sync_flag`; `audio_assets.genre`, `published`; `renders.render_group_id`, `part_no`, `watermark`; `director_plans.estimated_remaining_credits`; `jobs.heartbeat_at`; `ai_models.unit_cost_usd`; `media_files.storage_class` |
| 1.x → 2.0: bỏ | `projects.status` (thay bằng `workflow_step` + `chapters.media_status`); `director_plans.target` (Director chỉ còn một luồng); các bảng sách/slideshow/video AI từ các bản trước |
| 1.x → 2.0: đổi tên nhóm | ERD chia 6 nhóm theo luồng: Tài khoản, Dự án & bản thảo, Thế giới truyện, Sinh tư liệu, Trình chỉnh sửa & xuất video, Director/job/hạ tầng |
| 2.0 → 2.1 | **Ví USD thay credit:** bỏ `credit_balances`, `credit_ledger_entries`, `credit_packs`, enum `credit_bucket`; thêm `wallets`, `wallet_ledger_entries`; tiền lưu micro-USD; `jobs.credit_cost` → `held_micro`, `charged_micro`. **Closed beta:** thêm `beta_invites`, `system_settings`, `users.consented_at`, `consent_version`; bỏ `users.last_daily_claim_on`. **Bỏ** `illustrations.mask_media_id`, `edit_kind = INPAINT`, `sfx_suggestions`, `license = AI_GENERATED`, `provider_kind = MUSIC`. **Thêm** `narrations.flagged_at`, trạng thái `DONE`; `narration_settings.symbol_rules`; `timeline_items.playback_rate` |
| 2.1 → 2.2 | **Bỏ tốc độ từng clip** (QĐ-140): bỏ `timeline_items.playback_rate`, `derived_media_id`, IC-17. **Xuất cả dự án** (QĐ-141): `renders.scope`, `timeline_id` và `timeline_version` cho phép NULL; `timelines.scope = PROJECT` thành sau MVP |
