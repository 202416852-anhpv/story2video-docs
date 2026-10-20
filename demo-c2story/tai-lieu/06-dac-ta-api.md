# 06 — Đặc tả API

> API của hệ thống mới, **thiết kế lại hoàn toàn** (clean-room, xem README §3). Chuẩn: REST, JSON, OpenAPI 3.1. File `openapi.yaml` sẽ sinh từ code (NestJS Swagger) và được review dựa trên tài liệu này.

## 1. Quy ước chung

| Hạng mục | Quy ước |
|---|---|
| Base URL | `https://api.<domain>/v1` |
| Xác thực | Đăng nhập qua **SSO có sẵn** (OIDC). API cấp cookie phiên httpOnly sau callback (mẫu BFF). Admin dùng cùng cơ chế, có kiểm tra role. |
| Định dạng | `application/json; charset=utf-8`; thời gian ISO-8601 UTC; id là UUIDv7 |
| Đặt tên | Danh từ số nhiều, kebab-case (`/story-assets`); hành động không thuần CRUD dùng hậu tố `:verb` (`/chapters:restructure`) theo Google AIP-136 |
| Phân trang | Cursor: `?limit=50&cursor=…` trả `{ items, nextCursor }` |
| Khóa lạc quan | Response có header `ETag: "<version>"`; request sửa gửi `If-Match: "<version>"`. Sai version trả `409`, thiếu header trả `428` |
| Idempotency | Mọi POST tạo job **bắt buộc** `Idempotency-Key` (UUID). Lặp key trong 24h thì trả lại kết quả cũ |
| Job bất đồng bộ | Trả `202 Accepted` + `{ jobId, status, creditCost }` + header `Location: /v1/jobs/{jobId}` |
| Lỗi | RFC 9457 Problem Details (§1.1) |
| Rate limit | `429` + `Retry-After`; mặc định 120 req/phút/người, 20 job tốn phí/phút/người |

### 1.1 Định dạng lỗi

```json
{
  "type": "https://docs.<domain>/errors/insufficient-credits",
  "title": "Insufficient credits",
  "status": 402,
  "code": "INSUFFICIENT_CREDITS",
  "detail": "Thao tác cần 30 credit, số dư khả dụng 12.",
  "required": 30,
  "available": 12
}
```

| HTTP | `code` | Khi nào |
|---|---|---|
| 400 | `VALIDATION_ERROR` | Body sai schema |
| 401 | `UNAUTHENTICATED` | Chưa đăng nhập |
| 402 | `INSUFFICIENT_CREDITS` | Không đủ credit |
| 403 | `FORBIDDEN` | Không đủ quyền trong dự án |
| 404 | `NOT_FOUND` | Không tồn tại hoặc không có quyền xem (không tiết lộ sự tồn tại) |
| 409 | `VERSION_CONFLICT` | Sai `If-Match`; body kèm `current` |
| 410 | `INVITE_REVOKED` | Link mời bị thu hồi hoặc hết hạn |
| 422 | `PRECONDITION_FAILED_BUSINESS` | Vi phạm quy tắc nghiệp vụ (vd. compile khi thiếu ảnh) |
| 423 | `RESOURCE_LOCKED` | Chương đang bị job khóa |
| 422 | `NARRATION_LOCKED` | Thao tác trên timeline vi phạm khóa thuyết minh (BR-24) |
| 451 | `CONTENT_POLICY` | Nội dung vi phạm chính sách |

## 2. Danh mục endpoint

Cột **Quyền**: `P` = public, `U` = user đăng nhập, `E` = Editor của dự án, `O` = Owner, `A` = Admin. Cột **Job** đánh ✓ nếu endpoint trả `202` và tốn credit.

### 2.1 Tích hợp SSO & hồ sơ (M01)

> Không có endpoint đăng ký, mật khẩu hay xác minh email; các chức năng này thuộc SSO có sẵn.

| Method | Path | Quyền | Mô tả |
|---|---|---|---|
| GET | `/auth/login?returnTo=` | P | Tạo state/nonce/PKCE, `302` tới `authorization_endpoint` của SSO. `returnTo` chỉ chấp nhận đường dẫn nội bộ |
| GET | `/auth/callback?code&state` | P | Đổi code lấy token, xác thực ID token, JIT hồ sơ, tạo cookie phiên, `302` về `returnTo` |
| POST | `/auth/logout` | U | Hủy phiên; trả `{ logoutUrl }` (end_session_endpoint của SSO) để client chuyển hướng |
| POST | `/auth/backchannel-logout` | P (xác thực `logout_token` theo JWKS) | SSO thông báo đăng xuất; hủy mọi phiên của `sub` / `sid` |
| GET | `/auth/session` | P | `{ authenticated, user? }` cho client kiểm tra trạng thái |
| GET | `/me` | U | Hồ sơ cục bộ (email/tên/avatar đồng bộ từ SSO) |
| PATCH | `/me` | U | Chỉ sửa trường riêng của ứng dụng (`locale`) |
| POST | `/me:request-data-deletion` | U | Yêu cầu xóa dữ liệu của ứng dụng (không xóa tài khoản SSO) |
| GET | `/me/dashboard` | U | Gói, credit, số dự án, link "Quản lý tài khoản" của SSO |
| POST | `/webhooks/sso` | P (xác thực chữ ký) | *Tùy chọn*: sự kiện vô hiệu hoặc xóa tài khoản từ SSO (nếu SSO hỗ trợ) |

### 2.2 Dự án & cộng tác (M02)

| Method | Path | Quyền | Job | Mô tả |
|---|---|---|---|---|
| GET | `/projects?q=&status=IN_PROGRESS\|DONE` | U | | Danh sách dự án (owner + editor); `q` tìm theo tiêu đề (không phân biệt hoa thường, dấu); `status` suy ra từ trạng thái chương (FR-PRJ-01) |
| POST | `/projects` | U | | Tạo dự án trống |
| POST | `/projects:import` | U | | Import (multipart hoặc JSON `{title, text, styleId, aspectRatio}`), luôn giữ nguyên văn; trả `sourceSha256` |
| GET | `/projects/{pid}` | E | | Chi tiết + tóm tắt tiến độ (dùng cho Map) |
| PATCH | `/projects/{pid}` | O | | Settings (If-Match) |
| DELETE | `/projects/{pid}` | O | | Xóa mềm |
| GET | `/projects/{pid}/members` | E | | Thành viên |
| DELETE | `/projects/{pid}/members/{uid}` | O | | Xóa thành viên |
| POST | `/projects/{pid}/invite-link` | O | | Tạo hoặc lấy link mời |
| DELETE | `/projects/{pid}/invite-link` | O | | Thu hồi |
| POST | `/invites/{token}:accept` | U | | Tham gia dự án |
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
| POST | `/projects/{pid}/chapters:restructure` | E | | Chia/gộp/dời ranh giới/sắp xếp nguyên tử (§4.1) |
| GET | `/projects/{pid}/chapters/{cid}/versions` | E | | Lịch sử phiên bản |
| POST | `/projects/{pid}/chapters/{cid}/versions/{v}:restore` | E | | Khôi phục |
| POST | `/projects/{pid}:find-replace` | E | | `{find, replace, dryRun}` |
| GET / POST | `/projects/{pid}/archives` | E | | Liệt kê / tạo archive |
| GET / DELETE | `/projects/{pid}/archives/{aid}` | E | | Đọc / xóa |
| GET / POST | `/projects/{pid}/notes` | E | | Ghi chú |
| PATCH / DELETE | `/projects/{pid}/notes/{nid}` | E | | |

### 2.4 Thế giới truyện (M04, M08)

| Method | Path | Quyền | Job | Mô tả |
|---|---|---|---|---|
| POST | `/projects/{pid}/story-assets:analyze` | E | ✓ | AI phân tích, trả danh sách đề xuất |
| GET / POST | `/projects/{pid}/story-assets` | E | | Liệt kê / tạo; tạo từ thư viện: `{libraryAssetId}` |
| PATCH / DELETE | `/projects/{pid}/story-assets/{sid}` | E | | Sửa / gỡ khỏi dự án |
| POST | `/projects/{pid}/story-assets/{sid}:generate-image` | E | ✓ | Sinh ảnh tham chiếu |
| POST | `/projects/{pid}/story-assets:regenerate-all` | E | ✓ | Sinh lại toàn bộ |
| POST | `/projects/{pid}/story-assets/{sid}/image` | E | | Tải ảnh lên (`useExact`) |
| POST | `/projects/{pid}/story-assets/{sid}:save-to-library` | E | | Lưu vào thư viện cá nhân |
| PUT | `/projects/{pid}/art-direction` | E | | Art direction |
| GET | `/projects/{pid}/timeline?order=narrative\|chronological` · `/relationships` | E | | Đọc. `order` mặc định `narrative` (`order_index`); `chronological` sắp theo `chrono_index`, mốc NULL xếp cuối |
| POST | `/projects/{pid}/story-meta:analyze` | E | ✓ | Re-analyse timeline + relationships |
| CRUD | `/projects/{pid}/visual-rules[/{rid}]` | E | | Visual Rules |
| CRUD | `/projects/{pid}/chapters/{cid}/rules[/{id}]` | E | | Chapter rules |
| CRUD | `/library-assets[/{id}]` | U | | Thư viện cá nhân |
| GET | `/styles` | P | | Danh mục style |

### 2.5 Sinh tư liệu: storyboard, ảnh, thuyết minh (M05)

**Điều phối**

| Method | Path | Quyền | Job | Mô tả |
|---|---|---|---|---|
| GET | `/projects/{pid}/media:quote?chapterIds=` | E | | Báo giá tổng `{shots, imageCredits, ttsChars, ttsCredits, total}` |
| POST | `/projects/{pid}/media:generate` | E | ✓ | `{chapterIds[], only?: MISSING\|FAILED\|ALL, parts?: [IMAGE, NARRATION]}`: storyboard tự động (nếu thiếu), rồi ảnh + thuyết minh cho từng shot |
| GET | `/projects/{pid}/media?chapterId=` | E | | **Media bin**: chương → shot → `{illustration, narration, sourceText, durationMs, wer, status}` |

**Storyboard & ảnh**

| Method | Path | Quyền | Job | Mô tả |
|---|---|---|---|---|
| GET | `/projects/{pid}/chapters/{cid}/storyboards` | E | | Các bản nháp |
| POST | `/projects/{pid}/chapters/{cid}/storyboards` | E | ✓ | Tạo bản nháp `{kind: INITIAL\|RESPLIT_MORE\|RESPLIT_FEWER}` |
| POST | `…/storyboards/{did}:duplicate` | E | | Nhân bản |
| POST | `…/storyboards/{did}:set-current` | E | | Đặt hiện hành |
| PATCH / DELETE | `…/storyboards/{did}` | E | | Đổi tên / xóa |
| POST | `…/storyboards/{did}:redirect` | E | ✓ | Viết lại mọi brief `{note?}` |
| GET | `…/storyboards/{did}/shots` | E | | Danh sách shot |
| PATCH | `…/shots/{shid}` | E | | Sửa shot (If-Match) |
| POST | `…/shots/{shid}:split` · `:merge-up` · `:merge-down` | E | | Cấu trúc shot; `split` nhận `{atSentence}` |
| POST | `…/storyboards/{did}:move-boundary` | E | | `{leftShotId, rightShotId, deltaSentences}`: dời ranh giới giữa hai shot kề nhau theo câu |
| DELETE | `…/shots/{shid}` | E | | Xóa shot; đoạn nguồn gộp vào shot kề (BR-20) |
| GET | `…/storyboards/{did}/coverage` | E | | `{totalChars, coveredChars, gaps[], overlaps[]}`; luôn 100% sau validator |
| POST | `…/shots/{shid}:rewrite` | E | ✓ | AI viết lại brief `{note}` |
| POST | `…/shots/{shid}:generate-image` | E | ✓ | Sinh ảnh |
| POST | `…/storyboards/{did}:generate-images` | E | ✓ | Sinh mọi ảnh thiếu |
| POST | `…/shots/{shid}/illustrations:upload` | E | | Thay ảnh bằng ảnh tự tải lên (multipart; PNG/JPEG/WebP ≤ 10 MB, cạnh ngắn ≥ 512 px; NFR-SEC-10). Tạo Illustration `UPLOAD` mới làm hiện hành, miễn phí, không tạo job |
| POST | `…/shots/{shid}/illustrations/{iid}:edit` | E | ✓ | `{instruction, mask?}` |
| POST | `…/shots/{shid}/illustrations/{iid}:make-current` | E | | Khôi phục phiên bản |
| POST | `…/storyboards/{did}:auto-link-assets` | E | | Tự khớp tên với tài sản |
| POST | `/projects/{pid}/exports` | E | | `{type: ZIP_IMAGES\|ZIP_ASSETS, scope: CHAPTER\|PROJECT, chapterId?}` (job miễn phí) |

**Thuyết minh nguyên văn**

| Method | Path | Quyền | Job | Mô tả |
|---|---|---|---|---|
| GET | `/voices?language=` | U | | Danh mục giọng, kèm URL nghe thử |
| GET / PUT | `/projects/{pid}/narration-settings` | E | | Giọng, tốc độ, ngắt nghỉ, ngưỡng WER |
| CRUD | `/projects/{pid}/pronunciations[/{id}]` | E | | Từ điển phát âm |
| POST | `/projects/{pid}/pronunciations:preview` | E | | `{text}` trả audio nghe thử ngắn (giới hạn tần suất, miễn phí) |
| GET | `/projects/{pid}/chapters/{cid}/narrations:quote` | E | | `{chars, credits}` |
| POST | `/projects/{pid}/chapters/{cid}/narrations` | E | ✓ | Sinh thuyết minh cả chương (job cha + job con theo shot) |
| POST | `…/shots/{shid}/narration:generate` | E | ✓ | Sinh hoặc sinh lại thuyết minh một shot |
| GET | `…/shots/{shid}/narration` | E | | Audio, `wordTimings`, `wer`, `mismatches`, `status` |
| POST | `…/shots/{shid}/narration:accept` | E | | Chấp nhận thủ công shot `NEEDS_REVIEW` |

> Không có endpoint nào nhận "văn bản đọc" từ client. Văn bản TTS luôn do server cắt từ chương (BR-19).

### 2.6 Trình chỉnh sửa & xuất video (M06)

**Timeline**

| Method | Path | Quyền | Job | Mô tả |
|---|---|---|---|---|
| POST | `/projects/{pid}/timelines` | E | | Tạo hoặc lấy timeline `{scope: CHAPTER\|PROJECT, chapterId?}`; tự dựng bản nháp từ tư liệu |
| GET | `/projects/{pid}/timelines/{tlid}` | E | | Timeline đầy đủ: tracks + items + ETag (dùng cho editor và preview) |
| PATCH | `/projects/{pid}/timelines/{tlid}` | E | | Thuộc tính chung: khung hình, kiểu phụ đề, master loudness (If-Match) |
| POST | `/projects/{pid}/timelines/{tlid}:apply-ops` | E | | **Lô thao tác** `{ifMatch, ops: [{op: ADD_ITEM\|UPDATE_ITEM\|MOVE_ITEM\|SPLIT_ITEM\|TRIM_ITEM\|DELETE_ITEM\|ADD_TRACK\|UPDATE_TRACK\|DELETE_TRACK, …}]}`, nguyên tử. Server kiểm tra BR-24/IC-10; vi phạm trả `422 NARRATION_LOCKED` |
| POST | `/projects/{pid}/timelines/{tlid}:sync-media` | E | | Đồng bộ với tư liệu mới nhất, giữ chỉnh sửa của người dùng; trả danh sách item đã thay đổi |
| GET / POST | `/projects/{pid}/timelines/{tlid}/versions` | E | | Lịch sử phiên bản / đặt tên phiên bản |
| POST | `/projects/{pid}/timelines/{tlid}/versions/{v}:restore` | E | | Khôi phục |

**Thư viện âm thanh (nhạc nền & SFX)**

| Method | Path | Quyền | Job | Mô tả |
|---|---|---|---|---|
| GET | `/audio-assets?kind=MUSIC\|SFX&q=&mood=&maxDuration=` | U | | Tìm trong thư viện hệ thống + thư viện của tôi, kèm URL nghe thử và waveform |
| POST | `/audio-assets` | U | | Tải nhạc/SFX lên (multipart, kèm `licenseConfirmed: true`) |
| DELETE | `/audio-assets/{aid}` | U | | Xóa tài sản âm thanh của tôi |
| POST | `/projects/{pid}/audio-assets:generate` | E | ✓ | *(C)* Sinh nhạc/SFX bằng AI `{kind, prompt, durationSec}` |
| POST | `/projects/{pid}/timelines/{tlid}:suggest-sfx` | E | ✓ | *(C)* AI gợi ý SFX theo đoạn văn từng shot; trả đề xuất `{shotId, atMs, query}` để người dùng duyệt |

**Xuất & tải**

| Method | Path | Quyền | Job | Mô tả |
|---|---|---|---|---|
| GET | `/projects/{pid}/timelines/{tlid}/readiness` | E | | `{coverage: {covered, total}, missingImages[], needsReview[], outdated[], violations[]}` |
| POST | `/projects/{pid}/timelines/{tlid}/renders` | E | | `{resolution, splitBy?: CHAPTER\|DURATION, maxMinutes?}`: chụp `timeline_snapshot` và tạo job xuất (miễn phí); `422` nếu chưa sẵn sàng |
| GET | `/projects/{pid}/renders?timelineId=&versions=latest\|all` | E | | Danh sách bản xuất |
| GET | `/projects/{pid}/renders/{rid}` | E | | Trạng thái, `progress` |
| GET | `/projects/{pid}/renders/{rid}/download?file=MP4\|SRT\|VTT\|NARRATION_AUDIO` | E | | `302` tới link ký có thời hạn (15 phút) |
| POST | `/projects/{pid}/renders/{rid}:make-primary` · `:cancel` | E | | |
| DELETE | `/projects/{pid}/renders/{rid}` | E | | Xóa phiên bản |

### 2.7 AI Director (M07)

| Method | Path | Quyền | Job | Mô tả |
|---|---|---|---|---|
| GET | `/projects/{pid}/director/messages` | E | | Lịch sử chat |
| POST | `/projects/{pid}/director/messages` | E | | Gửi lệnh; response là **SSE stream** gồm token, `tool_proposal`, `tool_result` |
| POST | `/projects/{pid}/director/tool-proposals/{tpid}:confirm` | E | ✓ | Xác nhận tool tốn phí |
| GET | `/projects/{pid}/director/plan` | E | | Kế hoạch hiện tại |
| POST | `/projects/{pid}/director/plan` | E | | Bắt đầu chế độ tự động (bước 2 → 4 + bản nháp timeline) |
| POST | `/projects/{pid}/director/plan:continue` · `:pause` · `:exit` | E | | Điều khiển |
| POST | `/projects/{pid}/director/plan:submit-input` | E | | Trả lời điểm duyệt `{styleId}` / `{approvedAssetIds}` |

### 2.8 Job, credit & thanh toán (M09)

| Method | Path | Quyền | Mô tả |
|---|---|---|---|
| GET | `/jobs/{jid}` | U (người tạo hoặc Editor dự án) | Trạng thái job |
| POST | `/jobs/{jid}:cancel` | U | Hủy job đang `QUEUED` |
| GET | `/me/credits` | U | Số dư theo bucket |
| GET | `/me/credits/ledger?projectId=` | U | Lịch sử |
| POST | `/me/credits:daily-claim` | U | Nhận credit ngày |
| GET | `/pricing` | P | Gói, pack, bảng giá thao tác |
| POST | `/billing/checkout-sessions` | U | `{planCode, cycle}` hoặc `{packCode}`, trả `{url}` |
| POST | `/billing/portal-sessions` | U | Trả `{url}` customer portal |
| POST | `/webhooks/stripe` | P (xác thực chữ ký) | Webhook |

### 2.9 Quản trị (M10)

`/admin/price-rules`, `/admin/plans`, `/admin/ai-providers`, `/admin/ai-models`, `/admin/styles`, `/admin/jobs` (lọc, `:retry`, `:refund`), `/admin/users/{uid}/credits:adjust`, `/admin/reports/*`. Tất cả yêu cầu quyền `A` và ghi audit log.

## 3. Sự kiện realtime (SSE)

`GET /projects/{pid}/events` dùng `Last-Event-ID` để nối lại. Các loại sự kiện:

| `event` | `data` |
|---|---|
| `job.updated` | `{jobId, type, status, progress?, targetType, targetId, error?}` |
| `chapter.updated` | `{chapterId, version, lastEditedBy}` |
| `chapters.restructured` | `{chapterIds[]}` |
| `shot.updated` | `{shotId, version}` |
| `illustration.ready` | `{shotId, illustrationId, url}` |
| `narration.updated` | `{shotId, narrationId, status, wer?}` |
| `media.progress` | `{chapterId, shotId, part: IMAGE\|NARRATION, status}` |
| `chapter.media-ready` | `{chapterId, timelineId}` |
| `timeline.updated` | `{timelineId, version, changedItemIds[]}` |
| `render.progress` | `{renderId, progress}` |
| `render.ready` | `{renderId, url}` |
| `asset.updated` | `{assetId}` |
| `director.plan` | `{status, currentStep, awaitingReason?}` |
| `member.changed` | `{userId, action: JOINED\|REMOVED}` |

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
{ "jobId": "0192a7c6-...", "status": "QUEUED", "creditCost": 1 }
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
  "status": "NEEDS_REVIEW",
  "sourceStart": 1520, "sourceEnd": 1874,
  "sourceText": "Bỗng, âm báo tin nhắn của điện thoại Yên Vân reo lên. Người gửi tin là ba của cô.",
  "audioUrl": "https://cdn…/n.mp3?sig=…",
  "durationMs": 6240,
  "wer": 0.056,
  "mismatches": [ { "charStart": 1531, "charEnd": 1538, "expected": "âm báo", "heard": "âm bao" } ],
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
    { "op": "DELETE_ITEM", "itemId": "nar-shot-3" }
  ]
}
```

Response `422` (op thứ 4 vi phạm BR-24, cả lô không được áp dụng):

```json
{ "code": "NARRATION_LOCKED", "status": 422, "detail": "Không thể xóa clip thuyết minh nguyên văn.", "opIndex": 3 }
```
