# Prototype tiến hóa — Story2Video

> **Evolutionary prototype**: bản prototype là **phiên bản đầu tiên của chính mã nguồn MVP**, không phải bản nháp để vứt đi. Nó chạy được luồng lõi **truyện → thế giới truyện → MP4 có thuyết minh và phụ đề nguyên văn**, rồi được phát triển tiếp qua P1–P3 thành MVP bằng cách **thêm module, thay adapter**, không viết lại.
> Nguồn: bộ đặc tả đầy đủ ở [`../demo-c2story/`](../demo-c2story/). Prototype trùng với mốc **M1 "Khung chạy đầu-cuối"** của kế hoạch ([09 §1.2](../demo-c2story/tai-lieu/09-ke-hoach-phat-trien.md)), mở rộng thêm phần thế giới truyện.

## 1. Mục tiêu

| Mã | Mục tiêu | Đo bằng |
|---|---|---|
| PG-01 | Chạy hết luồng **văn bản → MP4** trên kiến trúc MVP (API, worker, render worker, Postgres, Redis, RustFS) | Kịch bản demo [03 §2](03-kiem-thu-nghiem-thu.md) |
| PG-02 | **Thuyết minh nguyên văn** (BR-19) và **phủ kín 100%** (BR-20) | `IT-tts-input-equals-source`, `PBT-coverage-validator` |
| PG-03 | **Phụ đề nguyên văn** (BR-22) | `IT-subtitle-verbatim` |
| PG-04 | **Nhân vật nhất quán** (BO-02) nhờ tài sản + ảnh tham chiếu | AC-13 ([03 §1](03-kiem-thu-nghiem-thu.md)) |
| PG-05 | **Tiến hóa được:** mã, schema, API, job là tập con của MVP; mọi chỗ cắt bớt nằm sau port và có trong sổ stub | AC-E1..E6 ([03 §1.2](03-kiem-thu-nghiem-thu.md)) |
| PG-06 | Có số liệu sớm cho P0: ảnh có tham chiếu, TTS tiếng Việt, aligner, thời gian render | Ghi chú spike ([03 §4](03-kiem-thu-nghiem-thu.md)) |

## 2. Nguyên tắc tiến hóa

| Mã | Nguyên tắc | Hệ quả |
|---|---|---|
| E-01 | **Cấu trúc mã = cấu trúc MVP** ([05 §5](../demo-c2story/tai-lieu/05-kien-truc-he-thong.md)): module `projects`, `manuscript`, `world`, `media`, `editor`… và `platform/*` | Module mới ở P1–P3 cắm vào chỗ đã định, không dời code |
| E-02 | **Schema DB = tập con của [04](../demo-c2story/tai-lieu/04-mo-hinh-du-lieu.md)**: tên bảng, cột, enum giữ nguyên; bảng đã tạo thì tạo **đủ cột** | Phát triển tiếp chỉ thêm migration, không đổi tên, không chuyển dữ liệu |
| E-03 | **API = tập con của [06](../demo-c2story/tai-lieu/06-dac-ta-api.md)**: đường dẫn, lỗi RFC 9457, `Idempotency-Key`, `If-Match`; OpenAPI viết trước | Client web và test hợp đồng dùng tiếp được |
| E-04 | **Mọi chỗ cắt bớt nằm sau một port có trong thiết kế MVP** (`IdentityProviderPort`, `WalletPort`, `TtsPort`, `AlignerPort`, `RenderEngine`…); prototype dùng adapter đơn giản | MVP thay adapter bằng cấu hình, không sửa chỗ gọi |
| E-05 | **Job đúng ADR-29 từ đầu**: bảng `jobs` là nguồn sự thật, BullMQ chỉ vận chuyển, nhận việc bằng `UPDATE … WHERE status IN (…)` | Ví, trần ngày, reconciler gắn thêm vào cùng vòng đời job |
| E-06 | **Hợp đồng lõi đúng [12](../demo-c2story/tai-lieu/12-dac-ta-ky-thuat-loi.md)**: `seg-1`, `NormalizationMap`, `word_timings` tọa độ chương, `timeline_snapshot` `schemaVersion 2` | Render, preview, phụ đề ở P3 dùng lại nguyên dữ liệu |
| E-07 | **Không có mã "dùng một lần" ở lõi.** Phần chắc chắn bị thay (giao diện tối giản) chỉ nằm ở lớp ngoài cùng và gọi API qua client sinh từ OpenAPI | Thay giao diện không đụng tới back-end |
| E-08 | **Sổ stub** ([02 §9](02-thiet-ke-ky-thuat.md)): mỗi chỗ đơn giản hóa có mã `PS-NN` và giai đoạn thay thế; trong mã đánh dấu `// @prototype-stub PS-NN` | Biết chính xác còn nợ gì; CI kiểm sổ và mã khớp nhau |

## 3. Đầu vào và đầu ra

| | Nội dung |
|---|---|
| **Đầu vào** | Văn bản truyện vi / en, dán hoặc tải `.txt` / `.md`, ≤ 20.000 ký tự (PS-11). Kèm tiêu đề, tỷ lệ khung hình, style |
| **Đầu vào tùy chọn** | Nhân vật, địa điểm, đạo cụ: AI đề xuất rồi User duyệt, hoặc User tự nhập; mỗi tài sản có ảnh tham chiếu |
| **Đầu ra** | Bản render `READY` gồm MP4 720p (H.264/AAC, phụ đề in sẵn), SRT, VTT, audio thuyết minh; tải qua link ký 15 phút |
| **Văn bản demo** | Nhóm tự chọn theo yêu cầu ở [03 §2](03-kiem-thu-nghiem-thu.md), kèm kết quả mong đợi |

## 4. Use case được chọn

Luồng: PT-01 → PT-05..07 → PT-02 → PT-03 → PT-04. Mã PT-05..07 thêm sau nên đánh số sau.

| Mã | Use case | Gộp / rút gọn từ | GĐ trong MVP | Đặc tả |
|---|---|---|---|---|
| PT-01 | Nhập truyện giữ nguyên văn | UC-02.02, UC-02.02a | P1 | [01 §2](01-dac-ta-use-case.md#pt-01) |
| PT-05 | Phân tích tài sản bằng AI (kèm duyệt đề xuất) | UC-04.01, UC-04.01a | P1 | [01 §6](01-dac-ta-use-case.md#pt-05) |
| PT-06 | Quản lý Story Assets (tạo, sửa, gỡ) | UC-04.02, 04.02a, 04.02d, 04.02e | P1 | [01 §7](01-dac-ta-use-case.md#pt-06) |
| PT-07 | Sinh ảnh tham chiếu | UC-04.03 | P1 | [01 §8](01-dac-ta-use-case.md#pt-07) |
| PT-02 | Sinh tư liệu chương | UC-05.07, 05.07a, 05.07b, 05.07c | P2 | [01 §3](01-dac-ta-use-case.md#pt-02) |
| PT-02a | Tạo storyboard phủ kín + tự khớp tài sản | UC-05.01, 05.01a, 05.06f | P1 | [01 §3.1](01-dac-ta-use-case.md#pt-02a) |
| PT-02b | Sinh ảnh shot (kèm ảnh tham chiếu) | UC-05.09 | P1 | [01 §3.2](01-dac-ta-use-case.md#pt-02b) |
| PT-02c | Sinh thuyết minh nguyên văn | UC-05.13, 05.13a, 05.13b | P2 | [01 §3.3](01-dac-ta-use-case.md#pt-02c) |
| PT-03 | Xuất video MP4 (tự dựng timeline, kiểm điều kiện) | UC-06.01a, 06.16, 06.16a | P3 | [01 §4](01-dac-ta-use-case.md#pt-03) |
| PT-04 | Tải MP4 / SRT / audio | UC-06.17 | P3 | [01 §5](01-dac-ta-use-case.md#pt-04) |

**10 use case**, gộp từ 24 UC gốc và con của bộ đặc tả. Mỗi UC prototype là **lát cắt dọc** của UC MVP tương ứng: cùng endpoint, cùng bảng, cùng job; phần thiếu được thêm dần mà không đổi phần đã có.

## 5. Phần chưa làm và chỗ cắm sẵn

| Nhóm | Chưa làm trong prototype | Thêm ở | Điểm cắm có sẵn |
|---|---|---|---|
| M01 SSO | Keycloak / Vbee, danh sách mời, đồng ý dữ liệu | P0–P1 | `IdentityProviderPort` (PS-01), bảng `users` |
| M02 Dự án | Tạo trống, cài đặt, xóa, Map | P1 | Module `projects`; cột `projects.*` đã đủ |
| M03 Bản thảo | Chia/gộp chương, Workspace, Re-import, .docx | P1 | Module `manuscript` là nơi duy nhất ghi `chapters.content`; `chapters.order_index` |
| M04 Thế giới | Nhóm, ảnh tải lên, Art Direction, Visual Rules, timeline truyện, quan hệ, sinh lại tất cả | P1–P2 | `PromptCompiler` có sẵn vị trí cho từng lớp chỉ dẫn (BR-08) |
| M05 Sinh tư liệu | Biên tập shot, chia lại, sửa ảnh, từ điển phát âm, nghe & đánh dấu | P1–P2 | Bảng `shots`, `illustrations`, `narrations` đủ cột; `NormalizationMap` có sẵn loại `EXPAND` / `ALIAS` |
| M06 Editor | Trình chỉnh sửa timeline, chuyển cảnh, nhạc/SFX, preview | P3 | Bảng `timelines`, `timeline_tracks`, `timeline_items`; `timeline_snapshot` v2; `RenderEngine` (PS-10) |
| M09 Ví | Ví, giữ/trừ/hoàn, giới hạn Free, nạp tiền | P1–P3 | `WalletPort` (PS-02), `PriceEstimator` (PS-04), `FreeLimitGuard` (PS-05), cột tiền trong `jobs` |
| M10 Quản trị | Trần ngày, seed đầy đủ | P1–P2 | `BudgetGuard` (PS-03); bảng `ai_providers`, `ai_models`, `styles`, `voices` |
| M07, M08 | Toàn bộ | Sau MVP | — |

## 6. Bất biến giữ nguyên từ bộ đặc tả

| Bất biến | Nguồn | Prototype bảo đảm ở |
|---|---|---|
| Văn bản lưu nguyên văn, chỉ chuẩn hóa kỹ thuật; chỉ `manuscript` ghi `chapters.content` | BR-19, BR-21, NFR-INT-02 | PT-01; lint kiến trúc |
| Offset là code unit UTF-16 trên văn bản NFC | ADR-26 | `packages/core` |
| Tách câu tất định `seg-1`; shot phủ kín 100%; LLM không chép lại văn bản | 12 §1, BR-20, IC-08 | PT-02a |
| Văn bản đọc chỉ hình thành từ `content[start:end]`, kiểm hash, kiểm tra ngược | BR-19, UC-05.13a/b | PT-02c |
| Phụ đề nguyên văn kể cả ký hiệu; không cue cho `---` | BR-22, 12 §2.4 | PT-03 |
| Chỉ xuất khi phủ 100%, mọi shot `DONE`; render chỉ đọc `timeline_snapshot` | BR-23, 12 §3 | PT-03 |
| AI chỉ đề xuất tài sản; sửa / gỡ tài sản không đổi ảnh shot đã sinh | UC-04.01a, 04.02d, 04.02e | PT-05, PT-06 |
| Bảng `jobs` là nguồn sự thật; thử lại một tầng ở mức job | ADR-29, QĐ-133 | Mọi job |

## 7. Danh mục tài liệu

| File | Nội dung |
|---|---|
| [01-dac-ta-use-case.md](01-dac-ta-use-case.md) | Đặc tả 10 use case (endpoint, job, bảng theo MVP) |
| [02-thiet-ke-ky-thuat.md](02-thiet-ke-ky-thuat.md) | Kiến trúc, cấu trúc repo, dữ liệu, API, job, thuật toán lõi, render, **sổ stub**, lộ trình tiến hóa |
| [03-kiem-thu-nghiem-thu.md](03-kiem-thu-nghiem-thu.md) | Tiêu chí nghiệm thu (chức năng + tiến hóa), kịch bản demo, test theo mã của 09 §4.13, kế hoạch T1–T6 |

> Quyết định dùng prototype này làm mốc M1 ghi ở **QĐ-153**, cho phép adapter thay thế ở M1 ghi ở **QĐ-154** ([`quyet-dinh.md`](../demo-c2story/quyet-dinh.md) §15).
