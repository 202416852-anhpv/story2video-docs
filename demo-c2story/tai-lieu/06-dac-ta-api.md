# 06 — Đặc tả API

> API của hệ thống mới, **thiết kế lại hoàn toàn** (clean-room, xem README §3). Chuẩn: REST, JSON, OpenAPI 3.1. File `openapi.yaml` sẽ sinh từ code (NestJS Swagger) và được review dựa trên tài liệu này. Endpoint chỉ dùng sau MVP ghi *(sau MVP)*.

## 1. Quy ước chung

| Hạng mục | Quy ước |
|---|---|
| Base URL | `https://api.<domain>/v1` |
| Xác thực | Đăng nhập qua SSO (Keycloak; Vbee trước khi bảo vệ). API cấp cookie phiên httpOnly sau callback (mẫu BFF). Phiên chưa đồng ý xử lý dữ liệu chỉ gọi được `/auth/*`, `/me`, `/me:consent` (`403 CONSENT_REQUIRED`). Admin dùng cùng cơ chế, có kiểm tra role. |
| Định dạng | `application/json; charset=utf-8`; thời gian ISO-8601 UTC; id là UUIDv7 |
| Đặt tên | Danh từ số nhiều, kebab-case (`/story-assets`); hành động không thuần CRUD dùng hậu tố `:verb` (`/chapters:restructure`) theo Google AIP-136 |
| Phân trang | Cursor: `?limit=50&cursor=…` trả `{ items, nextCursor }` |
| Khóa lạc quan | Response có header `ETag: "<version>"`; request sửa gửi `If-Match: "<version>"`. Sai version trả `409`, thiếu header trả `428` |
| Idempotency | Mọi POST tạo job **bắt buộc** `Idempotency-Key` (UUID). Lặp key trong 24h thì trả lại kết quả cũ |
| Job bất đồng bộ | Trả `202 Accepted` + `{ jobId, status, estimatedCostUsd }` (số đã giữ) + header `Location: /v1/jobs/{jobId}`. Khi job xong, `GET /jobs/{jid}` trả thêm `chargedUsd`, `releasedUsd` |
| Tiền | Trường tiền trong API là **chuỗi thập phân USD** (`"0.0132"`) để không mất độ chính xác; server lưu micro-USD (04 D-09) |
| Lỗi | RFC 9457 Problem Details (§1.1) |
| Rate limit | `429` + `Retry-After`; giới hạn **kỹ thuật**, không liên quan tính phí (BR-32): 120 req/phút/người; ≤ 30 yêu cầu LLM/phút/người; ≤ 8 job ảnh, 8 job TTS, 1 render đồng thời |

### 1.1 Định dạng lỗi

```json
{
  "type": "https://docs.<domain>/errors/insufficient-balance",
  "title": "Insufficient balance",
  "status": 402,
  "code": "INSUFFICIENT_BALANCE",
  "detail": "Thao tác cần giữ tối đa $0.4200, số dư khả dụng $0.1500.",
  "requiredUsd": "0.4200",
  "availableUsd": "0.1500"
}
```

| HTTP | `code` | Khi nào |
|---|---|---|
| 400 | `VALIDATION_ERROR` | Body sai schema |
| 401 | `UNAUTHENTICATED` | Chưa đăng nhập |
| 402 | `INSUFFICIENT_BALANCE` | Số dư khả dụng nhỏ hơn giá ước tính tối đa |
| 403 | `FORBIDDEN` | Không đủ quyền trong dự án |
| 403 | `NOT_INVITED` | Đăng nhập SSO thành công nhưng email không có trong danh sách mời beta (BR-30) |
| 403 | `CONSENT_REQUIRED` | Chưa đồng ý xử lý dữ liệu cá nhân (BR-31) |
| 403 | `FREE_LIMIT_REACHED` | Vượt giới hạn tài khoản Free (dự án, chương, lượt render, phút video; BR-27); body có `limit`, `used`, `max` |
| 404 | `NOT_FOUND` | Không tồn tại hoặc không có quyền xem (không tiết lộ sự tồn tại) |
| 409 | `VERSION_CONFLICT` | Sai `If-Match`; body kèm `current` |
| 410 | `INVITE_REVOKED` | Link mời bị thu hồi hoặc hết hạn |
| 422 | `PRECONDITION_FAILED_BUSINESS` | Vi phạm quy tắc nghiệp vụ (vd. xuất video khi còn shot thiếu ảnh) |
| 423 | `RESOURCE_LOCKED` | Chương đang bị job khóa |
| 422 | `NARRATION_LOCKED` | Thao tác trên timeline vi phạm khóa thuyết minh (BR-24) |
| 451 | `CONTENT_POLICY` | Nội dung vi phạm chính sách |
| 503 | `DAILY_BUDGET_EXCEEDED` | Chạm trần chi tiêu AI toàn hệ thống trong ngày (BR-29); thử lại sau 00:00 giờ Việt Nam |

### 1.2 Phạm vi MVP và OpenAPI viết trước

- **Endpoint thuộc MVP** là mọi dòng ở §2 **không** có nhãn *(sau MVP)* (ở dòng hoặc ở tiêu đề mục). Hiện có **80 / 119** dòng endpoint thuộc MVP; phần quản trị §2.9 trong MVP là lệnh CLI/seed, không có endpoint HTTP.
- **Viết trước (design-first):** với mỗi module, file `openapi/<module>.yaml` (OpenAPI 3.1) cho các endpoint MVP được viết và review **trước** khi code, trong sprint đầu của giai đoạn chứa module đó (M01 ở P0; M02–M05 ở P1–P2; M06, M09 ở P3). Schema request/response dùng chung các định nghĩa ở §1.1 (lỗi), [12 §3](12-dac-ta-ky-thuat-loi.md) (`timeline_snapshot`) và quy ước tiền (chuỗi thập phân USD).
- **Kiểm trong CI:** spec sinh từ code (NestJS Swagger) được so với file viết tay; khác biệt không có trong file viết tay làm CI thất bại (`IT-openapi-contract`). Client Web App sinh kiểu TypeScript từ file viết tay.
- Mỗi endpoint trong file OpenAPI liệt kê đủ mã lỗi có thể trả (theo bảng §1.1) và yêu cầu `Idempotency-Key` / `If-Match` nếu có.

## 2. Danh mục endpoint

Cột **Quyền**: `P` = public, `U` = user đăng nhập, `E` = Editor của dự án (MVP: chỉ Owner), `O` = Owner, `A` = Admin. Cột **Job** đánh ✓ nếu endpoint trả `202` và tính phí theo BR-01. Mọi endpoint có ✓ nhận `?dryRun=true` để chỉ trả giá ước tính `{ estimatedCostUsd, breakdown[] }` mà không tạo job.

### 2.1 Tích hợp SSO & hồ sơ (M01)

> Không có endpoint đăng ký, mật khẩu hay xác minh email; các chức năng này thuộc SSO có sẵn.

| Method | Path | Quyền | Mô tả |
|---|---|---|---|
| GET | `/auth/login?returnTo=` | P | Tạo state/nonce/PKCE, `302` tới `authorization_endpoint` của SSO. `returnTo` chỉ chấp nhận đường dẫn nội bộ |
| GET | `/auth/callback?code&state` | P | Đổi code lấy token, xác thực ID token (hoặc gọi userinfo với adapter OAuth 2.0), kiểm tra danh sách mời, JIT hồ sơ, tạo cookie phiên, `302` về `returnTo` hoặc `/consent`. Email chưa được mời: `302` tới trang "Bạn chưa được mời tham gia beta" |
| POST | `/auth/logout` | U | Hủy phiên; trả `{ logoutUrl }` (end_session_endpoint của SSO) để client chuyển hướng |
| POST | `/auth/backchannel-logout` | P (xác thực `logout_token` theo JWKS) | *(sau MVP)* SSO thông báo đăng xuất; hủy mọi phiên của `sub` / `sid` |
| GET | `/auth/session` | P | `{ authenticated, user? }` cho client kiểm tra trạng thái |
| GET | `/me` | U | Hồ sơ cục bộ (email/tên/avatar đồng bộ từ SSO), `consentRequired`, `consentNotice` (nội dung + phiên bản) |
| POST | `/me:consent` | U | `{ noticeVersion }`: ghi `consented_at`, `consent_version`; lần đầu thì tạo ví và tặng tiền dùng thử (UC-01.01d) |
| PATCH | `/me` | U | Chỉ sửa trường riêng của ứng dụng (`locale`) |
| POST | `/me:request-data-deletion` | U | *(sau MVP)* Yêu cầu xóa dữ liệu của ứng dụng (không xóa tài khoản SSO) |
| GET | `/me/dashboard` | U | Trạng thái tài khoản (Free / Đã nạp tiền), số dư ví, phần Free đã dùng trong tháng, số dự án, link "Quản lý tài khoản" của SSO |

### 2.2 Dự án & cộng tác (M02)

| Method | Path | Quyền | Job | Mô tả |
|---|---|---|---|---|
| GET | `/projects?q=&status=IN_PROGRESS\|DONE` | U | | Danh sách dự án (owner + editor); `q` tìm theo tiêu đề (không phân biệt hoa thường, dấu); `status` suy ra từ trạng thái chương (FR-PRJ-01) |
| POST | `/projects` | U | | Tạo dự án trống; Free đã có 1 dự án: `403 FREE_LIMIT_REACHED` |
| POST | `/projects:import` | U | | Import (multipart hoặc JSON `{title, text, styleId, aspectRatio}`), luôn giữ nguyên văn; trả `sourceSha256`; giới hạn Free như trên |
| GET | `/projects/{pid}` | E | | Chi tiết + tóm tắt tiến độ (dùng cho Map) |
| PATCH | `/projects/{pid}` | O | | Settings (If-Match) |
| DELETE | `/projects/{pid}` | O | | Xóa mềm |
| GET | `/projects/{pid}/members` | E | | *(sau MVP)* Thành viên |
| DELETE | `/projects/{pid}/members/{uid}` | O | | *(sau MVP)* Xóa thành viên |
| POST | `/projects/{pid}/invite-link` | O | | *(sau MVP)* Tạo hoặc lấy link mời |
| DELETE | `/projects/{pid}/invite-link` | O | | *(sau MVP)* Thu hồi |
| POST | `/invites/{token}:accept` | U | | *(sau MVP)* Tham gia dự án |
| GET | `/projects/{pid}/events` | E | | **SSE stream** (xem §3) |

### 2.3 Bản thảo & chương (M03)

| Method | Path | Quyền | Job | Mô tả |
|---|---|---|---|---|
| GET | `/projects/{pid}/source` | E | | Văn bản gốc |
| PUT | `/projects/{pid}/source` | E | | Re-import |
| POST | `/projects/{pid}/source:suggest-splits` | E | ✓ | AI gợi ý điểm chia |
| GET | `/projects/{pid}/chapters` | E | | Danh sách (không kèm content) |
| POST | `/projects/{pid}/chapters` | E | | Thêm chương `{afterChapterId?, title, content}` |
| GET | `/projects/{pid}/chapters/{cid}` | E | | Chi tiết + ETag |
| PATCH | `/projects/{pid}/chapters/{cid}` | E | | Sửa tiêu đề/nội dung (If-Match) |
| DELETE | `/projects/{pid}/chapters/{cid}` | E | | Xóa chương |
| POST | `/projects/{pid}/chapters:restructure` | E | | Chia/gộp/dời ranh giới/sắp xếp nguyên tử (§4.1); Free vượt 3 chương: `403 FREE_LIMIT_REACHED` |
| GET | `/projects/{pid}/chapters/{cid}/shot-boundaries` | E | | Vạch ranh giới shot của storyboard hiện hành trên văn bản chương: `[{leftShotId, rightShotId, offset, sentenceIndex}]` (UC-03.02a) |
| GET | `/projects/{pid}/chapters/{cid}/versions` | E | | *(sau MVP)* Lịch sử phiên bản |
| POST | `/projects/{pid}/chapters/{cid}/versions/{v}:restore` | E | | *(sau MVP)* Khôi phục |
| POST | `/projects/{pid}:find-replace` | E | | *(sau MVP)* `{find, replace, dryRun}` |
| GET / POST | `/projects/{pid}/archives` | E | | *(sau MVP)* Liệt kê / tạo archive |
| GET / DELETE | `/projects/{pid}/archives/{aid}` | E | | *(sau MVP)* Đọc / xóa |
| GET / POST | `/projects/{pid}/notes` | E | | *(sau MVP)* Ghi chú |
| PATCH / DELETE | `/projects/{pid}/notes/{nid}` | E | | *(sau MVP)* |

### 2.4 Thế giới truyện (M04, M08)

| Method | Path | Quyền | Job | Mô tả |
|---|---|---|---|---|
| POST | `/projects/{pid}/story-assets:analyze` | E | ✓ | AI phân tích, trả danh sách đề xuất |
| GET / POST | `/projects/{pid}/story-assets` | E | | Liệt kê / tạo; tạo từ thư viện `{libraryAssetId}`: sau MVP |
| PATCH / DELETE | `/projects/{pid}/story-assets/{sid}` | E | | Sửa / gỡ khỏi dự án |
| POST | `/projects/{pid}/story-assets/{sid}:generate-image` | E | ✓ | Sinh ảnh tham chiếu |
| POST | `/projects/{pid}/story-assets:regenerate-all` | E | ✓ | Sinh lại toàn bộ |
| POST | `/projects/{pid}/story-assets/{sid}/image` | E | | Tải ảnh lên (`useExact`) |
| POST | `/projects/{pid}/story-assets/{sid}:save-to-library` | E | | *(sau MVP)* Lưu vào thư viện cá nhân |
| PUT | `/projects/{pid}/art-direction` | E | | Art direction |
| GET | `/projects/{pid}/timeline?order=narrative\|chronological` · `/relationships` | E | | Đọc. `order` mặc định `narrative` (`order_index`); `chronological` sắp theo `chrono_index`, mốc NULL xếp cuối |
| POST | `/projects/{pid}/story-meta:analyze` | E | ✓ | Re-analyse timeline + relationships |
| CRUD | `/projects/{pid}/visual-rules[/{rid}]` | E | | Visual Rules |
| CRUD | `/projects/{pid}/chapters/{cid}/rules[/{id}]` | E | | *(sau MVP)* Chapter rules |
| CRUD | `/library-assets[/{id}]` | U | | *(sau MVP)* Thư viện cá nhân |
| GET | `/styles` | P | | Danh mục style |

### 2.5 Sinh tư liệu: storyboard, ảnh, thuyết minh (M05)

**Điều phối**

| Method | Path | Quyền | Job | Mô tả |
|---|---|---|---|---|
| GET | `/projects/{pid}/media:quote?chapterIds=` | E | | Giá ước tính tối đa `{shots, storyboardUsd, imagesUsd, ttsChars, ttsUsd, totalUsd}` |
| POST | `/projects/{pid}/media:generate` | E | ✓ | `{chapterIds[], only?: MISSING\|FAILED\|OUTDATED\|FLAGGED\|ALL, parts?: [IMAGE, NARRATION]}`: storyboard tự động (nếu thiếu), rồi ảnh + thuyết minh cho từng shot |
| GET | `/projects/{pid}/media?chapterId=` | E | | **Media bin**: chương → shot → `{illustration, narration, sourceText, durationMs, status, flagged}` |

**Storyboard & ảnh**

| Method | Path | Quyền | Job | Mô tả |
|---|---|---|---|---|
| GET | `/projects/{pid}/chapters/{cid}/storyboards` | E | | Các bản nháp (giao diện quản lý nhiều bản sau MVP) |
| POST | `/projects/{pid}/chapters/{cid}/storyboards` | E | ✓ | Tạo bản nháp `{kind: INITIAL\|RESPLIT_MORE\|RESPLIT_FEWER}` |
| POST | `…/storyboards/{did}:duplicate` | E | | *(sau MVP)* Nhân bản |
| POST | `…/storyboards/{did}:set-current` | E | | Đặt hiện hành (MVP: dùng sau khi chia lại shot) |
| PATCH / DELETE | `…/storyboards/{did}` | E | | *(sau MVP)* Đổi tên / xóa |
| POST | `…/storyboards/{did}:redirect` | E | ✓ | *(sau MVP)* Viết lại mọi brief `{note?}` |
| GET | `…/storyboards/{did}/shots` | E | | Danh sách shot |
| PATCH | `…/shots/{shid}` | E | | Sửa shot (If-Match) |
| POST | `…/shots/{shid}:split` · `:merge-up` · `:merge-down` | E | | Cấu trúc shot; `split` nhận `{atSentence}` |
| POST | `…/storyboards/{did}:move-boundary` | E | ✓ | Gọi từ **Workspace** (UC-03.02a). `{leftShotId, rightShotId, deltaSentences}`: dời ranh giới giữa hai shot kề nhau theo câu, rồi tạo 2 job `REWRITE_SHOT` viết lại brief (BR-33). `?dryRun=true` trả giá ước tính và xem trước câu nào chuyển shot, không đổi gì |
| DELETE | `…/shots/{shid}` | E | | Xóa shot; đoạn nguồn gộp vào shot kề (BR-20) |
| GET | `…/storyboards/{did}/coverage` | E | | `{totalChars, coveredChars, gaps[], overlaps[]}`; luôn 100% sau validator |
| POST | `…/shots/{shid}:rewrite` | E | ✓ | AI viết lại brief `{note}` |
| POST | `…/shots/{shid}:generate-image` | E | ✓ | Sinh ảnh |
| POST | `…/storyboards/{did}:generate-images` | E | ✓ | Sinh mọi ảnh thiếu |
| POST | `…/shots/{shid}/illustrations:upload` | E | | Thay ảnh bằng ảnh tự tải lên (multipart; PNG/JPEG/WebP ≤ 10 MB, cạnh ngắn ≥ 512 px; NFR-SEC-10). Tạo Illustration `UPLOAD` mới làm hiện hành, miễn phí, không tạo job |
| POST | `…/shots/{shid}/illustrations/{iid}:edit` | E | ✓ | `{instruction}` (Describe → Edit) |
| POST | `…/shots/{shid}/illustrations/{iid}:make-current` | E | | Khôi phục phiên bản |
| POST | `…/storyboards/{did}:auto-link-assets` | E | | Tự khớp tên với tài sản |
| POST | `/projects/{pid}/exports` | E | | *(sau MVP)* `{type: ZIP_IMAGES\|ZIP_ASSETS, scope: CHAPTER\|PROJECT, chapterId?}` (job miễn phí) |

**Thuyết minh nguyên văn**

| Method | Path | Quyền | Job | Mô tả |
|---|---|---|---|---|
| GET | `/voices?language=` | U | | Danh mục giọng, kèm URL nghe thử |
| GET / PUT | `/projects/{pid}/narration-settings` | E | | Giọng, tốc độ, ngắt nghỉ, `symbolRules` (bật/tắt SYM-01..05, 08 §6); ngưỡng WER sau MVP |
| CRUD | `/projects/{pid}/pronunciations[/{id}]` | E | | Từ điển phát âm |
| POST | `/projects/{pid}/pronunciations:preview` | E | ✓ | `{text}` (≤ 200 ký tự) trả audio nghe thử ngắn **đồng bộ** (ngoại lệ của AG-01, QĐ-131): HOLD → gọi TTS (timeout 15 s, không thử lại) → CAPTURE/RELEASE trong cùng request; tính phí TTS theo BR-01. Lỗi: `402`, `429`, `451`, `503` |
| GET | `/projects/{pid}/chapters/{cid}/narrations:quote` | E | | `{chars, estimatedCostUsd}` |
| POST | `/projects/{pid}/chapters/{cid}/narrations` | E | ✓ | Sinh thuyết minh cả chương (job cha + job con theo shot) |
| POST | `…/shots/{shid}/narration:generate` | E | ✓ | Sinh hoặc sinh lại thuyết minh một shot |
| GET | `…/shots/{shid}/narration` | E | | Audio, `wordTimings`, `status`, `flagged`; `wer`, `mismatches` khi bật kiểm chứng ASR (sau MVP) |
| POST / DELETE | `…/shots/{shid}/narration:flag` | E | | Đánh dấu / bỏ đánh dấu cần sinh lại (BR-34) |
| POST | `…/shots/{shid}/narration:accept` | E | | *(sau MVP)* Chấp nhận thủ công shot `NEEDS_REVIEW` |

> Không có endpoint nào nhận "văn bản đọc" từ client. Văn bản TTS luôn do server cắt từ chương (BR-19).

### 2.6 Trình chỉnh sửa & xuất video (M06)

**Timeline**

| Method | Path | Quyền | Job | Mô tả |
|---|---|---|---|---|
| POST | `/projects/{pid}/timelines` | E | | Tạo hoặc lấy timeline `{scope: CHAPTER\|PROJECT, chapterId?}`; tự dựng bản nháp từ tư liệu |
| GET | `/projects/{pid}/timelines/{tlid}` | E | | Timeline đầy đủ: tracks + items + ETag (dùng cho editor và preview) |
| PATCH | `/projects/{pid}/timelines/{tlid}` | E | | Thuộc tính chung: khung hình, kiểu phụ đề, master loudness (If-Match) |
| POST | `/projects/{pid}/timelines/{tlid}:apply-ops` | E | | **Lô thao tác** `{ifMatch, ops: [{op: ADD_ITEM\|UPDATE_ITEM\|MOVE_ITEM\|SPLIT_ITEM\|TRIM_ITEM\|DELETE_ITEM\|ADD_TRACK\|UPDATE_TRACK\|DELETE_TRACK, …}]}`, nguyên tử. `UPDATE_ITEM` trên clip thuyết minh chỉ nhận `startMs`, `volume`, `volumeKeyframes`, `playbackRate` (0,8–1,25); đổi `playbackRate` thì server tạo job `PROCESS_AUDIO_RATE` (miễn phí) và item có `rateStatus: PROCESSING\|READY\|FAILED` (ADR-24), báo kết quả qua `timeline.updated`. Server kiểm tra BR-24/IC-10/IC-17; vi phạm trả `422 NARRATION_LOCKED` |
| POST | `/projects/{pid}/timelines/{tlid}:sync-media` | E | | Đồng bộ với tư liệu mới nhất, giữ chỉnh sửa của người dùng; trả danh sách item đã thay đổi |
| GET / POST | `/projects/{pid}/timelines/{tlid}/versions` | E | | *(sau MVP)* Lịch sử phiên bản / đặt tên phiên bản |
| POST | `/projects/{pid}/timelines/{tlid}/versions/{v}:restore` | E | | *(sau MVP)* Khôi phục |

**Âm thanh (nhạc nền & SFX)**

| Method | Path | Quyền | Job | Mô tả |
|---|---|---|---|---|
| GET | `/audio-assets?kind=MUSIC\|SFX&q=` | U | | Âm thanh của tôi, kèm URL nghe thử và waveform. Thư viện hệ thống (`&source=SYSTEM&mood=&maxDuration=`): sau MVP |
| POST | `/audio-assets` | U | | Tải nhạc/SFX lên (multipart; MP3/WAV/M4A ≤ 100 MB, ≤ 15 phút); không cần cờ cam kết (BR-26) |
| DELETE | `/audio-assets/{aid}` | U | | Xóa tài sản âm thanh của tôi |

**Xuất & tải**

| Method | Path | Quyền | Job | Mô tả |
|---|---|---|---|---|
| GET | `/projects/{pid}/timelines/{tlid}/readiness` | E | | `{coverage: {covered, total}, missingImages[], notDone[], outdated[], violations[], warnings: {flagged[]}, freeQuota?: {rendersLeft, minutesLeft, watermark}}` |
| POST | `/projects/{pid}/timelines/{tlid}/renders` | E | | `{resolution}`: chụp `timeline_snapshot` và tạo job xuất (miễn phí); `422` nếu chưa sẵn sàng; Free vượt lượt/phút hoặc chọn 1080p: `403 FREE_LIMIT_REACHED`. `splitBy`, `maxMinutes`: sau MVP |
| GET | `/projects/{pid}/renders?timelineId=&versions=latest\|all` | E | | Danh sách bản xuất |
| GET | `/projects/{pid}/renders/{rid}` | E | | Trạng thái, `progress` |
| GET | `/projects/{pid}/renders/{rid}/download?file=MP4\|SRT\|VTT\|NARRATION_AUDIO` | E | | `302` tới link ký có thời hạn (15 phút) |
| POST | `/projects/{pid}/renders/{rid}:make-primary` · `:cancel` | E | | |
| DELETE | `/projects/{pid}/renders/{rid}` | E | | Xóa phiên bản |

### 2.7 AI Director (M07) *(sau MVP)*

| Method | Path | Quyền | Job | Mô tả |
|---|---|---|---|---|
| GET | `/projects/{pid}/director/messages` | E | | Lịch sử chat |
| POST | `/projects/{pid}/director/messages` | E | | Gửi lệnh; response là **SSE stream** gồm token, `tool_proposal`, `tool_result` |
| POST | `/projects/{pid}/director/tool-proposals/{tpid}:confirm` | E | ✓ | Xác nhận tool tốn phí |
| GET | `/projects/{pid}/director/plan` | E | | Kế hoạch hiện tại |
| POST | `/projects/{pid}/director/plan` | E | | Bắt đầu chế độ tự động (bước 2 → 4 + bản nháp timeline) |
| POST | `/projects/{pid}/director/plan:continue` · `:pause` · `:exit` | E | | Điều khiển |
| POST | `/projects/{pid}/director/plan:submit-input` | E | | Trả lời điểm duyệt `{styleId}` / `{approvedAssetIds}` |

### 2.8 Job, ví & thanh toán (M09)

| Method | Path | Quyền | Mô tả |
|---|---|---|---|
| GET | `/jobs/{jid}` | U (người tạo hoặc Editor dự án) | Trạng thái job, `estimatedCostUsd`, `chargedUsd`, `releasedUsd` |
| POST | `/jobs/{jid}:cancel` | U | Hủy job đang `QUEUED` (RELEASE toàn bộ) |
| GET | `/me/wallet` | U | `{availableUsd, heldUsd, topupTotalUsd, accountStatus: FREE\|PAID, freeUsage: {projects, chapters, rendersThisMonth, minutesThisMonth}}` |
| GET | `/me/wallet/ledger?projectId=&type=&from=&to=` | U | Lịch sử chi tiêu: bút toán, job, chi phí thực, phí 10% |
| GET | `/pricing` | P | Cách tính giá, đơn giá tham khảo từng thao tác, giới hạn Free, tiền dùng thử |
| POST | `/billing/topup-sessions` | U | `{amountUsd}` ($1–$100), tạo Checkout Session ở **sandbox**, trả `{url}` |
| POST | `/billing/checkout-sessions` | U | *(sau MVP)* `{planCode, cycle}` đăng ký gói |
| POST | `/billing/portal-sessions` | U | *(sau MVP)* Trả `{url}` customer portal |
| POST | `/webhooks/stripe` | P (xác thực chữ ký) | Webhook |

### 2.9 Quản trị (M10)

**MVP:** bảng giá, provider, mô hình, style, giọng và `system_settings` nạp từ file seed bằng lệnh `pnpm seed`; danh sách mời quản lý bằng CLI `pnpm admin:invites add|remove|list <email>` (UC-10.11). Không có endpoint quản trị qua HTTP.

**Sau MVP:** `/admin/price-rules`, `/admin/plans`, `/admin/ai-providers`, `/admin/ai-models`, `/admin/styles`, `/admin/invites`, `/admin/settings`, `/admin/jobs` (lọc, `:retry`, `:refund`), `/admin/users/{uid}/wallet:adjust`, `/admin/reports/*`. Tất cả yêu cầu quyền `A` và ghi audit log.

## 3. Sự kiện realtime (SSE)

`GET /projects/{pid}/events`. **MVP:** không phát lại sự kiện đã lỡ (không có kho sự kiện, ADR-23); khi nối lại, client tải lại ảnh chụp trạng thái (vd. `GET …/media`, `GET …/timelines/{tlid}`, `GET /me/wallet`) rồi nghe tiếp. **Sau MVP:** hỗ trợ `Last-Event-ID` để phát lại từ outbox. Các loại sự kiện:

| `event` | `data` |
|---|---|
| `job.updated` | `{jobId, type, status, progress?, targetType, targetId, error?}` |
| `chapter.updated` | `{chapterId, version, lastEditedBy}` |
| `chapters.restructured` | `{chapterIds[]}` |
| `shot.updated` | `{shotId, version}` |
| `illustration.ready` | `{shotId, illustrationId, url}` |
| `narration.updated` | `{shotId, narrationId, status, flagged}` |
| `media.progress` | `{chapterId, shotId, part: IMAGE\|NARRATION, status}` |
| `chapter.media-ready` | `{chapterId, timelineId}` |
| `timeline.updated` | `{timelineId, version, changedItemIds[]}` |
| `render.progress` | `{renderId, progress}` |
| `render.ready` | `{renderId, url}` |
| `asset.updated` | `{assetId}` |
| `director.plan` | `{status, currentStep, awaitingReason?}` |
| `member.changed` | `{userId, action: JOINED\|REMOVED}` *(sau MVP)* |
| `wallet.updated` | `{availableUsd, heldUsd, accountStatus}` (kênh của người dùng) |

## 4. Mẫu payload

### 4.1 Restructure chương

```http
POST /v1/projects/{pid}/chapters:restructure
Idempotency-Key: 0192a7c4-...
Content-Type: application/json

{
  "operations": [
    { "op": "SPLIT", "chapterId": "c1", "ifMatch": 7, "atParagraph": 42, "newTitle": "Chương 2" },
    { "op": "MERGE_INTO_PREVIOUS", "chapterId": "c5", "ifMatch": 3 },
    { "op": "MOVE_BOUNDARY", "chapterId": "c3", "ifMatch": 2, "deltaParagraphs": -1 },
    { "op": "REORDER", "chapterId": "c4", "beforeChapterId": "c2" }
  ],
  "acknowledgeOutdatedMedia": true
}
```

Response `200`: `{ "chapters": [ {id, orderIndex, title, version} ], "outdatedShotIds": [...] }`. Một thao tác lỗi thì rollback toàn bộ và trả `409` hoặc `422`.

### 4.2 Sinh ảnh shot

```http
POST /v1/projects/{pid}/chapters/{cid}/storyboards/{did}/shots/{shid}:generate-image
Idempotency-Key: 0192a7c5-...
```

```json
202 Accepted
{ "jobId": "0192a7c6-...", "status": "QUEUED", "estimatedCostUsd": "0.0440" }
```

### 4.3 Cập nhật shot

```json
PATCH /v1/.../shots/{shid}
If-Match: "4"
{
  "title": "Tin nhắn với ba",
  "timeOfDay": "Tối",
  "storyDate": "2023-01-17",
  "brief": {
    "subject": "Yên Vân (tóc đen ngang vai) cầm điện thoại",
    "environment": "Phòng khách căn hộ tầng 9",
    "composition": "Trung cảnh, nhân vật lệch phải",
    "camera": "Ngang tầm mắt",
    "lighting": "Ánh đèn vàng ấm, ngoài cửa sổ tối",
    "mood": "Cô đơn, trầm lặng",
    "details": "Màn hình điện thoại sáng"
  },
  "caption": "Tin nhắn từ ba hiện lên…",
  "assetRefs": [
    { "storyAssetId": "a1", "role": "CAST" },
    { "rawName": "điện thoại", "role": "ITEM" }
  ]
}
```

### 4.4 Cấu trúc output LLM bắt buộc (storyboard)

LLM nhận danh sách câu dạng `[{i: 0, text: "…"}, …]` và **chỉ trả chỉ số câu**, không chép lại văn bản (ADR-11).

```json
{
  "type": "object",
  "required": ["shots"],
  "properties": {
    "shots": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["startSentence", "endSentence", "title", "focus", "brief"],
        "properties": {
          "startSentence": {"type": "integer", "minimum": 0},
          "endSentence": {"type": "integer", "description": "chỉ số câu cuối, bao gồm"},
          "title": {"type": "string", "maxLength": 120},
          "focus": {"type": "string"},
          "cast": {"type": "array", "items": {"type": "string"}},
          "items": {"type": "array", "items": {"type": "string"}},
          "locations": {"type": "array", "items": {"type": "string"}, "maxItems": 1},
          "timeOfDay": {"type": "string"},
          "storyDate": {"type": "string"},
          "brief": {"$ref": "#/$defs/brief"},
          "caption": {"type": "string", "maxLength": 300}
        }
      }
    }
  }
}
```

Server: đổi chỉ số câu sang offset ký tự, chạy `CoverageValidator`, rồi lưu `source_start`, `source_end`, `source_hash`.

### 4.5 Narration của một shot

```json
GET /v1/projects/{pid}/.../shots/{shid}/narration
{
  "narrationId": "0192…",
  "status": "DONE",
  "flagged": false,
  "sourceStart": 1520, "sourceEnd": 1874,
  "sourceText": "Bỗng, âm báo tin nhắn của điện thoại Yên Vân reo lên. Người gửi tin là ba của cô.",
  "audioUrl": "https://cdn…/n.mp3?sig=…",
  "durationMs": 6240,
  "wordTimings": [ { "w": "Bỗng", "start": 0.12, "end": 0.48, "charStart": 1520, "charEnd": 1524 } ]
}
```

### 4.6 Lô thao tác trên timeline

```json
POST /v1/projects/{pid}/timelines/{tlid}:apply-ops
{
  "ifMatch": 12,
  "ops": [
    { "op": "ADD_ITEM", "trackId": "trk-music", "item": { "kind": "AUDIO", "audioAssetId": "calm-piano", "startMs": 0, "durationMs": 95000, "fadeInMs": 1500, "fadeOutMs": 3000, "volume": 0.6, "duckingDb": -12 } },
    { "op": "ADD_ITEM", "trackId": "trk-sfx-1", "item": { "kind": "AUDIO", "audioAssetId": "fireworks", "startMs": 102000, "durationMs": 4000, "volume": 0.8 } },
    { "op": "UPDATE_ITEM", "itemId": "img-shot-7", "patch": { "motion": { "type": "ZOOM_IN", "intensity": 0.15, "focusX": 0.6, "focusY": 0.4 }, "transitionIn": { "type": "CROSSFADE", "durationMs": 800 } } },
    { "op": "UPDATE_ITEM", "itemId": "nar-shot-5", "patch": { "playbackRate": 1.1 } },
    { "op": "DELETE_ITEM", "itemId": "nar-shot-3" }
  ]
}
```

Response `422` (op thứ 5 vi phạm BR-24, cả lô không được áp dụng; op thứ 4 đổi tốc độ 1,1× là hợp lệ):

```json
{ "code": "NARRATION_LOCKED", "status": 422, "detail": "Không thể xóa clip thuyết minh nguyên văn.", "opIndex": 4 }
```

### 4.7 Dời ranh giới shot từ Workspace

```http
POST /v1/projects/{pid}/chapters/{cid}/storyboards/{did}:move-boundary?dryRun=true
{ "leftShotId": "s4", "rightShotId": "s5", "deltaSentences": 2 }
```

```json
200 OK
{
  "movedSentences": ["Cô đặt điện thoại xuống.", "Ngoài cửa sổ, mưa bắt đầu rơi."],
  "from": "s5", "to": "s4",
  "affectedShotIds": ["s4", "s5"],
  "estimatedCostUsd": "0.0060",
  "breakdown": [ { "operation": "REWRITE_SHOT", "count": 2, "estimatedCostUsd": "0.0060" } ]
}
```

Gửi lại không có `dryRun` kèm `Idempotency-Key` để dời thật: `202 { jobIds: [..2], estimatedCostUsd }`. Thuyết minh của `s4`, `s5` chuyển `OUTDATED` (BR-33).
