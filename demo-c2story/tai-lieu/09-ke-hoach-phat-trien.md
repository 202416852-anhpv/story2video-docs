# 09 — Kế hoạch phát triển & ma trận truy vết

> Quyết định nguồn: [sổ quyết định](../quyet-dinh.md). Phạm vi MVP và giai đoạn của từng FR: [02 SRS](02-dac-ta-yeu-cau-phan-mem-SRS.md) (cột GĐ); của từng use case: dòng "Giai đoạn" trong [03](03-dac-ta-use-case/00-muc-luc.md). Sơ đồ phạm vi MVP: [`so-do/mvp/`](../so-do/mvp/README.md).

## 1. Lộ trình phát hành

> **Phiên bản 1.13 (2026-10-20):** áp các khuyến nghị đánh giá PM (QĐ-90..99): có khung chạy đầu-cuối sớm, rủi ro editor/render được đưa lên trước, cân lại khối lượng P1/P2, thêm thứ tự cắt giảm tầng 2 và kịch bản tối thiểu, đo vận tốc sớm, tính lịch Tết và thi, gán vai trò, bảng rủi ro có người chịu trách nhiệm.
>
> **Phiên bản 1.16 (2026-10-20):** áp đánh giá AI Engineering (QĐ-110..118): cách đo cụ thể cho các ngưỡng AI ở P0 (§1.5), thêm 4 mã EVAL, chốt mật độ ảnh và chi phí/phút ở M0, rủi ro moderation R-21, nạp tiền sandbox lên ✂1, ablation cho báo cáo.

### 1.1 Bối cảnh và năng lực

| Hạng mục | Giá trị | Nguồn |
|---|---|---|
| Loại dự án | Đồ án tốt nghiệp; thanh toán sandbox; closed beta | QĐ-01, QĐ-30 |
| Thời gian | 7 tháng phát triển ≈ **30 tuần lịch**, bắt đầu tuần của 2026-10-26 (T1). Kế hoạch làm việc **24 tuần**; sau đó 2 tháng viết báo cáo và bảo vệ | QĐ-01 |
| Lịch không làm việc | **Tết Nguyên đán 2027** (mùng 1 = 2027-02-06) rơi vào **T15–T16**: tính 50% năng lực mỗi tuần, tổng mất 1 tuần làm việc. **Kỳ thi / môn học song song**: nhóm điền tuần cụ thể vào §1.9 trong sprint đầu | QĐ-95 |
| Nhân sự | 3 người full-stack × 20 giờ/tuần, có Coding Agent; vai trò ở §2.1 | QĐ-02, QĐ-96 |
| Năng lực | 3 × 20 giờ × 24 tuần = 1.440 giờ ≈ **36 tuần-người**; khoảng **54–72 tuần-người** nếu Coding Agent tăng năng suất 1,5–2 lần | QĐ-02 |
| Khối lượng MVP | Ước tính từ trên xuống **50–63 tuần-người**; **chưa có story point**. Ước lượng lại từ dưới lên ở mốc đo vận tốc T8 (§1.4) | V3 câu 4 |
| Khoảng hở xấu nhất | 63 − 36 = **27 tuần-người** (nếu Coding Agent không giúp được gì). Thứ tự cắt giảm 2 tầng + kịch bản tối thiểu (§1.3) phải che được khoảng này | QĐ-91 |

### 1.2 Các giai đoạn và mốc

MVP = hết P3 (QĐ-03). Thứ tự làm theo nguyên tắc **rủi ro trước**: có video đầu-cuối từ T6, spike editor/render ở P2, không để rủi ro lớn nhất tới P3 mới lộ ra (QĐ-90, QĐ-92).

| Giai đoạn | Tuần | Mục tiêu | Phạm vi chính |
|---|---|---|---|
| **P0 — Nền tảng & PoC** | T1–T4 | Chọn provider bằng số liệu; khung hệ thống; kiểm chứng hạ tầng | Repo, CI/CD, docker-compose (Keycloak, MinIO, ClamAV); ADR chốt ở tuần 1: **ADR-26** (offset UTF-16), **ADR-27** (Kysely), **ADR-28** (semaphore), **ADR-29** (nguồn sự thật của job); `platform` (jobs nhận việc an toàn + HOLD, idempotency, rate limit, SSE, audit); AI Gateway + **mock adapter**; schema lõi; nền tảng kiểm thử §2.3; M01: đăng nhập Keycloak qua `IdentityProviderPort`, JIT hồ sơ (chưa bật danh sách mời); OpenAPI viết tay cho M01. **PoC:** LLM Gemini (chốt mã mô hình Flash/Pro), ảnh Gemini Image (QĐ-119, QĐ-120), **TTS tự host** (2–3 model mã nguồn mở) + chọn máy GPU bằng `BENCH-tts` (QĐ-121), aligner WhisperX tiếng Việt; golden set kèm **nhãn tay cho eval** (rubric ngoại hình, bản ghi giọng người cho WER nền, danh sách khó, biên từ; QĐ-110, 111, 115); **tỷ lệ ảnh bị từ chối** (QĐ-113); chốt **mật độ ảnh** và đo **chi phí AI/phút video** (QĐ-112); đo hệ số ký tự/token tiếng Việt cho `PriceEstimator`. **Benchmark render** FFmpeg/Remotion trên cấu hình máy staging (QĐ-98) |
| **P1 — Nhập truyện → thế giới truyện → ảnh** | T5–T11 | Bước 1–3 và ảnh; có video thô đầu-cuối | M02 (danh sách, import, tạo trống, cài đặt, xóa); M03 (văn bản gốc, Workspace, chia/gộp/dời/sắp xếp chương, tái cấu trúc nguyên tử); M04 (phân tích tài sản + `EVAL-asset-extraction` (QĐ-114), CRUD, ảnh tham chiếu, ảnh tải lên, style, Art Direction, Visual Rules); M05 (storyboard phủ kín, biên tập shot, chia lại, sinh/sửa/thay ảnh, media bin); M09 (ví, $2 dùng thử, giữ/trừ/hoàn, giới hạn Free dự án/chương); M10 (seed); **danh sách mời + màn hình đồng ý dữ liệu** (dời từ P0, QĐ-100); **khung chạy đầu-cuối** (mốc M1) |
| **P2 — Thuyết minh, sinh tư liệu, spike editor** | T12–T16 (Tết ở T15–T16) | Hoàn tất bước 4; gỡ rủi ro editor | Cài đặt thuyết minh, ký hiệu SYM, TTS + timestamp, từ điển phát âm ✂6, nghe & đánh dấu, "Sinh tư liệu", sinh lại chọn lọc, dời ranh giới shot ở Workspace, khóa chương; **dời từ P1:** Timeline truyện ✂5, Relationships ✂4, Dashboard, tài khoản SSO, sao chép/nhập lại văn bản gốc, xem số dư ví, **trần chi tiêu ngày**; **spike editor/render** (mốc M3) |
| **P3 — Trình chỉnh sửa, xuất video, thanh toán, Vbee** | T17–T24 | Bước 5–6; sẵn sàng closed beta | M06 (timeline, thuyết minh khóa, phụ đề, nhạc/SFX tải lên, Ken Burns, chuyển cảnh, preview, render, watermark & hạn mức Free, tải xuống); M09 (Pricing, nạp tiền sandbox, webhook, lịch sử chi tiêu); i18n; Map ✂2; **SSO Vbee** (§1.6) |
| UAT closed beta | T25–T27 | Thử nghiệm với người dùng thật | §1.8 |
| Dự phòng | T28–T30 | | Còn **2 tuần thực** sau khi trừ Tết (1 tuần) và UAT (3 tuần). Trễ thì dùng dự phòng trước, UAT rút tối thiểu còn 2 tuần |
| Báo cáo & bảo vệ | Tháng 8–9 | | Hoàn thiện báo cáo từ các bản nháp đã viết dần (§1.10); xóa dữ liệu beta sau ngày bảo vệ |
| **Sau MVP** | — | Hướng phát triển | Như bản đầy đủ: Director, thư viện, cộng tác, lịch sử phiên bản, kiểm chứng ASR, overlay/màu, thư viện âm thanh, gói đăng ký, giao diện admin… |

Phân bổ story (theo [11](11-product-backlog.md)): P0 6 · P1 51 · P2 21 · P3 26. So với bản 1.12 (P1 58 · P2 12), 9 use case đã được dời từ P1 sang P2 (QĐ-93); bản 1.15 dời UC-01.01d và UC-10.11 từ P0 sang P1 để giảm tải back-end ở P0 (QĐ-100).

**Các mốc (milestone):**

| Mốc | Tuần | Tiêu chí đạt | Nếu không đạt |
|---|---|---|---|
| **M0** Kết thúc P0 | T4 | Gemini Image đạt ngưỡng hoặc đã áp quy tắc dự phòng; model TTS tự host và máy GPU đã chọn (theo §1.5); mọi dòng của bảng P0 §1.5 có số liệu (ảnh, TTS, moderation, timestamp, chi phí/phút); mật độ ảnh đã chốt (QĐ-112); benchmark render trên máy staging có số liệu; đăng nhập Keycloak + JIT chạy được; ADR-26..29 đã chốt; nền tảng kiểm thử §2.3 chạy trong CI | Kéo dài P0 tối đa 1 tuần, lấy từ dự phòng |
| **M1** Khung chạy đầu-cuối | T6 | Một chương mẫu đi hết import → storyboard → ảnh → TTS → **MP4 có phụ đề** bằng FFmpeg, không cần giao diện editor; provider thật trên staging | Ưu tiên tuyệt đối sprint T7 cho tới khi đạt; đánh dấu R-15 là "đang xảy ra" |
| **M2** Đo vận tốc | T8 | Có vận tốc trung bình sprint T5–T8; toàn bộ story MVP đã có story point; dự báo ngày xong P3 | Áp thứ tự cắt giảm ngay (§1.4) |
| **M3** Spike editor/render | T14 | Prototype timeline (kéo thả, khóa thuyết minh) + Remotion Player; render cùng `timeline_snapshot` lệch preview ≤ 1 khung hình trên 3 chương mẫu. **Đồng thời chốt engine render:** nếu không đạt hoặc phải kích hoạt ✂9 thì render bằng **FFmpeg thuần** (`zoompan` cho Ken Burns, `xfade` cho chuyển cảnh, phụ đề ASS), bỏ Remotion và Chromium khỏi Render Worker | Kích hoạt ✂9 trước khi vào P3 |
| **M4** Kết thúc P1 / P2 | T11 / T16 | Tiêu chí §1.5; kiểm tra 80% (§1.4) | Áp thứ tự cắt giảm |
| **M5** Sẵn sàng beta | T24 | Luồng 6 bước chạy trên staging; danh sách mời, trần ngày, đồng ý dữ liệu bật | UAT lùi tối đa 1 tuần |

### 1.3 Thứ tự cắt giảm (QĐ-05, QĐ-91, QĐ-116)

Cắt theo thứ tự; mỗi mục là một khối độc lập, cắt không làm hỏng luồng 6 bước. Tiết kiệm ước tính tính bằng tuần-người (tn) [ĐX], hiệu chỉnh lại ở M2. Bản 1.16 đưa nạp tiền sandbox lên ✂1 và dời các mục tầng 1 cũ xuống một bậc (QĐ-116).

**Tầng 1 — tính năng phụ (QĐ-05, QĐ-116)**

| Thứ tự | Phần bị cắt | FR / UC | Tiết kiệm | Ảnh hưởng |
|---|---|---|---|---|
| ✂1 | Nạp tiền sandbox + webhook | FR-BIL-03, 09; UC-09.03, 09.03a, 09.08, 09.08a | 2 tn | Admin cộng tiền bằng CLI `admin:wallet topup` (ghi bút toán `TOPUP` có `reason`, vẫn làm tài khoản thành "Đã nạp tiền"); BO-05 đo bằng câu hỏi khảo sát beta |
| ✂2 | Map | FR-PRJ-06, UC-02.09 | 0,5 tn | Người mới khó định hướng hơn |
| ✂3 | Phụ đề preset, chuyển cảnh nâng cao | FR-EDT-11 (preset), FR-EDT-07 (nâng cao) | 1 tn | Còn cut, crossfade, định kiểu tay |
| ✂4 | Relationships | FR-WLD-09, UC-04.08 | 1,5 tn | Prompt mất ngữ cảnh quan hệ |
| ✂5 | Timeline truyện | FR-WLD-08, UC-04.07, UC-04.09 | 1,5 tn | Prompt mất ngữ cảnh mùa/thời điểm |
| ✂6 | Từ điển phát âm | FR-NAR-04, UC-05.12 | 1,5 tn | Mất biện pháp chính cho R-06 (QĐ-80) |
| | **Cộng tầng 1** | | **≈ 8 tn** | |

**Tầng 2 — giảm độ hoàn thiện của phần lớn (QĐ-91)**

| Thứ tự | Phần bị cắt | FR / UC | Thay bằng | Tiết kiệm |
|---|---|---|---|---|
| ✂7 | Giới hạn Free + watermark | FR-BIL-12, FR-EDT-21 (phần Free) | Mọi người dùng beta không giới hạn; trần ngày vẫn bảo vệ ngân sách | 1,5 tn |
| ✂8 | Dời ranh giới shot ở Workspace | FR-BOK-01b, UC-03.02a | Chỉnh shot bằng tách / gộp / xóa ở storyboard | 1 tn |
| ✂9 | Preview thời gian thực bằng Remotion Player | FR-EDT-17, UC-06.13 | Xem trước bằng render nháp 480p (job render nhanh); bỏ yêu cầu NFR-PERF-11, 13 | 3 tn |
| ✂10 | Undo/redo đầy đủ, nhiều track nhạc/SFX, Ken Burns nhiều pha | FR-EDT-02, 03, 06 (một phần) | 1 track nhạc + 1 track SFX; undo 20 bước trong phiên; một pha chuyển động | 2 tn |
| | **Cộng tầng 2** | | | **≈ 7,5 tn** |

**Tầng 3 — kịch bản tối thiểu (cần PO duyệt, QĐ-91)**

Dùng khi M2 dự báo khoảng hở > 15 tn sau khi đã áp tầng 1–2: **bỏ trình chỉnh sửa timeline thủ công** (M06 chỉ còn UC-06.01a dựng timeline tự động, chọn một bài nhạc nền, xuất và tải). Video vẫn đủ 6 bước và nguyên văn 100%; trình chỉnh sửa trở thành hướng phát triển. Tiết kiệm khoảng 8–10 tn.

> Tổng có thể cắt ≈ 24–26 tn, xấp xỉ khoảng hở xấu nhất 27 tn. Việc **tích hợp SSO Vbee** không nằm trong danh sách vì là yêu cầu bắt buộc (QĐ-21); nếu Vbee chậm thì đi theo §1.6.

### 1.4 Kiểm soát tiến độ (QĐ-06, QĐ-94)

| Thời điểm | Việc làm | Quy tắc |
|---|---|---|
| Mỗi sprint | Burndown của giai đoạn; vận tốc sprint (story point hoàn thành theo DoD) | Hai sprint liên tiếp vận tốc < 70% kế hoạch → báo PO, xem xét cắt sớm |
| **M2 (T8)** | Ước lượng story point cho **toàn bộ** backlog MVP; dự báo = điểm còn lại ÷ vận tốc trung bình T5–T8 | Dự báo vượt T24 → cắt theo §1.3 cho tới khi vừa; vượt > 15 tn sau tầng 2 → đề xuất tầng 3 cho PO |
| **M4 (T11, T16)** | So điểm đã xong với kế hoạch giai đoạn | < 80% → áp thứ tự cắt giảm tiếp theo |
| Sau mỗi lần cắt | Ghi vào [sổ quyết định](../quyet-dinh.md); đổi dòng Giai đoạn của UC thành "Sau"; chạy `gen_mvp.py`, `gen_backlog.py` | |

### 1.5 Tiêu chí kết thúc giai đoạn (QĐ-07, QĐ-97, QĐ-110..115)

Mỗi giai đoạn: demo được luồng chính; test trong RTM (§4) của các UC thuộc giai đoạn đều pass; không còn lỗi mức High; PO ký nghiệm thu.

**P0 — chọn provider:**

| Loại | Ngưỡng đạt | Cách đo | Nếu **không provider nào** đạt (quy tắc dự phòng) |
|---|---|---|---|
| Ảnh | ≤ 10% shot sai ngoại hình trên golden set | `EVAL-consistency`: ≥ 150 shot mỗi provider; rubric 4 thuộc tính (khuôn mặt, tóc, trang phục, tuổi/vóc dáng); 2 người chấm độc lập, Cohen's κ ≥ 0,6; báo cáo khoảng tin cậy 95%, tách shot 1 nhân vật / ≥ 2 nhân vật (QĐ-110) | Gemini Image ≤ 15% (ngưỡng BO-02) thì vẫn dùng, ghi khoảng hở vào báo cáo; > 15% thì thử thêm 1 provider (tối đa 1 tuần, từ dự phòng) rồi chọn tốt nhất và ghi QĐ (QĐ-120) |
| Ảnh bị từ chối | ≤ 5% shot golden set bị provider chặn vì chính sách nội dung | `EVAL-refusal-rate` trên cùng các shot của `EVAL-consistency` (QĐ-113) | Thêm hướng dẫn tả gián tiếp vào prompt storyboard rồi đo lại; vẫn > 5% thì tính vào tiêu chí chọn provider và ghi R-21 là "đang xảy ra" |
| TTS | WER hiệu chỉnh ≤ 3% (vi và en); danh sách khó đọc đúng ≥ 95% | `EVAL-wer-golden`: WER theo âm tiết sau chuẩn hóa hai phía, trừ WER nền của ASR trên bản ghi giọng người; danh sách khoảng 100 tên riêng, Hán Việt, số, từ mượn chấm bằng tai (QĐ-111) | Áp cho các model TTS tự host. Chọn model có WER hiệu chỉnh thấp nhất nếu ≤ 5%; **đưa từ điển phát âm ra khỏi thứ tự cắt giảm** (bắt buộc làm ở P2) và ghi R-06 là "đang xảy ra"; > 5% thì PO chọn: chấp nhận, đổi giọng/ngôn ngữ ưu tiên, hoặc **đưa Vbee AIVoice vào MVP** (R-23) |
| Tốc độ TTS | Tổng hợp + căn timestamp ≤ 0,4× thời lượng audio trên máy GPU đã chọn (để đạt NFR-PERF-09) | `BENCH-tts`: 2 chương golden, đo thời gian TTS Server + Alignment Worker và giá GPU/giờ → `unit_cost_usd` (QĐ-123) | Thuê GPU mạnh hơn (báo PO chi phí), chọn model nhẹ hơn nếu WER vẫn đạt, hoặc nới NFR-PERF-09 cho MVP |
| Timestamp | Sai lệch biên từ trung vị ≤ 100 ms, p95 ≤ 250 ms; aligner tự host ≤ 0,5× thời lượng audio trên máy staging | `EVAL-alignment`: nhãn tay khoảng 200 từ mỗi ngôn ngữ; áp cho cả timestamp của TTS (QĐ-115) | TTS tự host không trả timestamp nên đo trên WhisperX (QĐ-122); không đạt thì thử MFA; vẫn không đạt thì nới p95 ≤ 400 ms và ghi vào báo cáo |
| Chi phí | Chi phí AI ≤ $0,15/phút video (BO-06) ở mật độ ảnh đã chốt (mặc định 3 ảnh/phút) | `EVAL-cost-per-minute`: chạy luồng đầy đủ trên 2 chương golden, cộng `ai_usage_records` (QĐ-112) | PO chọn: giảm mật độ (≥ 2 ảnh/phút), dùng mô hình Gemini rẻ hơn, hoặc nâng BO-06; kiểm lại $2 dùng thử còn đủ 1 chương |
| Render | 1 phút video 720p render ≤ 2 phút trên máy staging (QĐ-98) | `BENCH-render` | Giảm độ phân giải Free/nháp, giới hạn độ dài một lần render, hoặc nâng cấu hình máy (báo PO chi phí) |

Phần chấm và gán nhãn (khoảng 1 tn) do PO/BA và frontend làm, không lấy công của back-end & AI (QĐ-118). Chi phí sinh ảnh, TTS cho eval nằm trong ngân sách PoC $200.

### 1.6 Tích hợp SSO Vbee (QĐ-21..23)

| Mốc | Nội dung | Người chịu trách nhiệm |
|---|---|---|
| T1 | Gửi yêu cầu chính thức tới đội Vbee: tài liệu tích hợp, endpoint, cách cấp `client_id`/`client_secret`, người liên hệ | PO |
| T4, T6 | Nhắc lại và ghi trạng thái vào sổ quyết định; T6 chưa có phản hồi → báo trước rủi ro R-14 cho giảng viên hướng dẫn | PO |
| **T9 (hết tháng thứ 2)** | Hạn chót nhận tài liệu | PO |
| Có tài liệu, có OIDC | P3 (T21–T22): cấu hình `OidcAdapter`, test trên môi trường Vbee; ≈ 1 tn | Phụ trách backend |
| Có tài liệu, chỉ OAuth 2.0 | Thêm `OAuth2UserinfoAdapter`; **+1–2 tn**, lấy từ thứ tự cắt giảm §1.3 | Phụ trách backend |
| Quá hạn | Giữ Keycloak cho bản bảo vệ; báo cáo ghi "đã thiết kế adapter OIDC, chờ đối tác cung cấp thông tin" | PO |

### 1.7 Ngân sách AI và hạ tầng (QĐ-39..41, QĐ-98)

| Khoản | Mức | Cách giữ |
|---|---|---|
| P0 (PoC) | ≤ $200 | Golden set có kiểm soát; ghi `ai_usage_records` |
| P1–P3 | ≤ $50/tháng | Mock adapter cho dev/CI; provider thật khi demo, mốc M1 và E2E hằng tuần. Trước khi có trần chi tiêu ngày (P2), đặt **giới hạn chi tiêu trên console của từng provider** |
| UAT | ≤ $200 | Danh sách mời; $2 dùng thử/người; trần $10/ngày. Gồm ≤ $30 cho ablation (QĐ-117) |
| GPU cho TTS tự host | Theo `BENCH-tts` | Thuê theo giờ, chỉ bật khi demo, E2E, beta; hoặc máy có GPU của thành viên. Giờ GPU chạy job tính vào `ai_usage_records` (QĐ-123), giờ rảnh tính vào khoản hạ tầng; báo PO trước T8 |
| Hạ tầng | Ưu đãi sinh viên | Cấu hình máy staging chọn theo **benchmark render ở P0**; NFR-PERF-10 (1080p ≤ 1× thời lượng trên 8 vCPU) là mục tiêu sau MVP, MVP dùng ngưỡng §1.5. Chi phí nâng cấu hình (nếu cần) báo PO trước T8 |

### 1.8 UAT: closed beta (QĐ-71)

- **T25–T27**, 10–20 người được mời; mỗi người làm ít nhất 1 chương bằng $2 dùng thử; có thể nạp tiền sandbox (hoặc Admin cộng tiền nếu ✂1).
- **Chuẩn bị từ T20:** chốt danh sách người mời, nội dung thông báo đồng ý dữ liệu, phiếu khảo sát, chương mẫu cho người chưa có truyện.
- **Thu thập:** phiếu khảo sát, log sử dụng, chỉ số BO-01..BO-06.
- Đợt 2 mở rộng nếu còn thời gian. Dữ liệu beta xóa sau ngày bảo vệ.

### 1.9 Lịch không làm việc của nhóm (QĐ-95)

| Tuần | Lý do | Năng lực còn lại |
|---|---|---|
| T15–T16 | Tết Nguyên đán 2027 | 50% mỗi tuần |
| *(nhóm điền)* | Thi cuối kỳ / môn học song song | *(nhóm điền)* |

Kế hoạch sprint và dự báo ở M2 dùng năng lực sau khi trừ bảng này.

### 1.10 Viết báo cáo đồ án dần theo giai đoạn (QĐ-99)

| Cuối giai đoạn | Bản nháp chương báo cáo |
|---|---|
| P0 | Tổng quan, khảo sát, lựa chọn công nghệ, **kết quả PoC chọn provider** |
| P1 | Phân tích yêu cầu, thiết kế (lấy từ 01–08 và `so-do/mvp/`) |
| P2 | Thiết kế chi tiết luồng sinh tư liệu và thuyết minh nguyên văn |
| P3 | Cài đặt, kiểm thử (RTM, kết quả test) |
| UAT | Đánh giá với người dùng, chỉ số BO, **ablation** (`EVAL-consistency` trên 2–3 chương golden với 4 cấu hình: đầy đủ / bỏ ảnh tham chiếu / bỏ Visual Rules / bỏ Timeline truyện + Relationships; QĐ-117), hạn chế và hướng phát triển |

Mỗi bản nháp là một story trong sprint cuối giai đoạn (khoảng 1 ngày công).

## 2. Cách làm việc và tiêu chí hoàn thành

### 2.1 Vai trò và quy trình (QĐ-10..13, QĐ-50, QĐ-96)

**Vai trò** (nhóm điền tên trong sprint đầu; một người có thể giữ hai vai trò):

| Vai trò | Người | Phụ trách chính | Dự phòng (bus factor) |
|---|---|---|---|
| PO / trưởng nhóm + BA | *(TV3)* | Phạm vi, ưu tiên, nghiệm thu, **đầu mối Vbee**, ngân sách AI, giảng viên hướng dẫn, đặc tả, sổ quyết định, báo cáo đồ án; **gán nhãn và chấm eval** cùng frontend (QĐ-118). **Không giữ vai trò back-end** (QĐ-101) | TV2 |
| Phụ trách backend & AI | *(TV1)* | `platform`, AI Gateway, M05, M09 (ví), M01, PoC provider, ADR-26..29, OpenAPI của các module back-end | TV3 |
| Phụ trách frontend & editor | *(TV2)* | Studio, **M06 trình chỉnh sửa**, Remotion, spike M3; người chấm thứ hai của eval P0 (QĐ-118) | TV1 |
| Phụ trách DevOps & chất lượng | *(TV3, cùng PO)* | CI/CD, staging, benchmark render, test E2E hằng tuần, RTM; M02–M04 chia với TV1 khi P1 quá tải | TV1 |

Mỗi module có một người chính và một người review cố định để không có phần chỉ một người hiểu.

**Quy trình:**

| Hạng mục | Quy ước |
|---|---|
| Sprint | 1 tuần (QĐ-10), nghi thức gọn để không quá 10% thời gian: planning 30 phút đầu tuần; demo + retro gộp 45 phút cuối tuần; cập nhật trạng thái hằng ngày bằng tin nhắn, không họp |
| Ước lượng | Story point, planning poker; toàn bộ backlog MVP phải có điểm trước M2 (T8) |
| Theo dõi | GitHub Projects: burndown giai đoạn, vận tốc sprint (§1.4) |
| Backlog | Nháp sinh tự động ở [11](11-product-backlog.md); Gherkin là bản nháp, chỉ rà kỹ khi story được kéo vào sprint (không rà trước toàn bộ) |
| Ra quyết định | Họp chốt cả nhóm; bất đồng thì PO quyết định cuối; ghi vào [sổ quyết định](../quyet-dinh.md) |
| Thay đổi đặc tả | Commit kèm mô tả; BA cập nhật RTM và lịch sử phiên bản **cuối mỗi sprint** |

### 2.2 Definition of Done

- Đáp ứng mọi tiêu chí chấp nhận của story, có test tự động (unit + integration với mock adapter). Luồng tiền, quyền, danh sách mời và trần chi tiêu có test e2e. Công viết test **nằm trong story point** của story, không tách riêng.
- Đã cập nhật OpenAPI; endpoint mới có test ma trận quyền.
- Job mới có: dòng `price_rules` (công thức × 1,10 và giới hạn đầu ra), mock adapter, metric, ghi `ai_usage_records`.
- Review code bởi ít nhất 1 người; không còn cảnh báo bảo mật mức High.
- Đã cập nhật i18n (vi, en).
- Nếu thay đổi use case: cập nhật dòng Truy vết và Giai đoạn của UC, chạy `python3 so-do/tools/gen_mvp.py` và `python3 tools/gen_backlog.py`.

### 2.3 Nền tảng kiểm thử (QĐ-102)

| Mức | Công cụ | Ghi chú |
|---|---|---|
| UT, PBT | Vitest + **fast-check** | Package `@studio/timeline-rules`, `SentenceSegmenter`, `NormalizationMap`, `PriceEstimator`, sổ cái chạy hoàn toàn trong bộ nhớ |
| IT | Vitest + **Testcontainers** (PostgreSQL 16, Redis 7, MinIO) | Mỗi bộ test một schema sạch, migration Kysely chạy trước; provider AI là mock adapter |
| Mock adapter | Fixture **ghi lại từ phản hồi thật** của provider ở P0 (kể cả phản hồi lỗi, timeout, rate limit) | Đổi provider thì ghi lại fixture; tránh mock "xanh giả" |
| Contract | `IT-openapi-contract` so spec sinh từ code với `openapi/*.yaml` viết tay; `UT-snapshot-schema` kiểm `timeline_snapshot` | 06 §1.2, 12 §3 |
| E2E | **Playwright** trên staging; hằng tuần với provider thật, còn lại với mock | Có ngân sách riêng trong $50/tháng |
| Đồng thời | Test bắn song song có kiểm soát (`IT-daily-budget-concurrency`, `IT-flow-settlement`, `IT-job-redelivery`) | Chạy trên Testcontainers, không mock DB |

## 3. User story & tiêu chí chấp nhận mẫu (Gherkin)

> Mẫu viết tay cho các luồng quan trọng nhất. Gherkin của mọi story MVP sinh tự động ở [11](11-product-backlog.md).

### US-AUTH-11 Chỉ người được mời mới vào được beta

```gherkin
Feature: Danh sách mời closed beta
  Scenario: Email chưa được mời
    Given danh sách mời không có "a@example.com"
    When "a@example.com" đăng nhập SSO thành công lần đầu
    Then tôi thấy "Bạn chưa được mời tham gia beta"
    And không có hồ sơ và không có ví nào được tạo

  Scenario: Email được mời, lần đầu đăng nhập
    Given danh sách mời có "b@example.com"
    When "b@example.com" đăng nhập SSO lần đầu và đồng ý xử lý dữ liệu
    Then ví của tôi có số dư khả dụng $2.0000
    And sổ cái có đúng một bút toán TRIAL_GRANT
    And trạng thái tài khoản là "Free"
```

### US-BIL-11 Giữ giá ước tính, trừ chi phí thực × 110%

```gherkin
Feature: Tính phí theo chi phí thực
  Scenario: Sinh ảnh thành công, hoàn phần dư
    Given ví của tôi khả dụng $1.0000
    And giá ước tính tối đa của một ảnh là $0.0440
    When tôi bấm "Generate" trên shot "S1"
    Then số dư khả dụng là $0.9560 và đang giữ $0.0440
    When job hoàn tất với chi phí thực của provider là $0.0300
    Then số tiền bị trừ là $0.0330
    And số dư khả dụng là $0.9670 và đang giữ $0.0000

  Scenario: Provider lỗi, hoàn toàn bộ
    Given ví của tôi khả dụng $1.0000
    When tôi sinh ảnh "S1" và provider lỗi sau 3 lần thử
    Then "S1" hiển thị nút "Retry"
    And số dư khả dụng của tôi là $1.0000

  Scenario: Chạm trần chi tiêu ngày
    Given tổng chi phí AI hôm nay của hệ thống là $9.9900 và trần là $10
    When tôi bấm "Sinh tư liệu" với giá ước tính $0.5000
    Then tôi nhận lỗi "DAILY_BUDGET_EXCEEDED"
    And không có tiền nào bị giữ
```

### US-BOK-01a Storyboard phủ kín văn bản

```gherkin
Feature: Đoạn nguồn của shot phủ kín chương
  Scenario: LLM bỏ sót câu
    Given chương "C1" có 40 câu
    When LLM trả về các shot phủ câu 0-10, 12-25, 26-39
    Then câu 11 được gộp vào shot thứ nhất
    And nối các đoạn nguồn theo thứ tự bằng đúng văn bản "C1"
    And báo cáo độ phủ là 100%

  Scenario: Xóa shot không mất chữ
    Given storyboard có các shot S1, S2, S3 phủ kín chương
    When tôi xóa S2
    Then đoạn nguồn của S2 được nối vào cuối S1
    And độ phủ vẫn là 100%
```

### US-BOK-01b Dời ranh giới shot trong Workspace

```gherkin
Feature: Dời ranh giới shot ở Workspace
  Scenario: Dời hai câu và viết lại brief
    Given chương "C1" có storyboard với shot S4 và S5 liền kề
    When tôi kéo vạch ranh giới S4|S5 sang phải 2 câu trong Workspace
    Then tôi thấy hai câu sẽ chuyển sang S4 và giá ước tính viết lại 2 brief
    When tôi bấm "Dời và viết lại brief"
    Then độ phủ vẫn là 100%
    And thuyết minh của S4 và S5 có trạng thái "OUTDATED"
    And có 2 job REWRITE_SHOT được tạo

  Scenario: Hủy thì không đổi gì
    When tôi kéo vạch rồi bấm "Hủy"
    Then ranh giới S4|S5 giữ nguyên và không có tiền nào bị giữ
```

### US-NAR-02 Thuyết minh nguyên văn

```gherkin
Feature: Audio đọc đúng văn bản gốc
  Scenario: Văn bản TTS lấy từ chương
    Given shot "S3" có đoạn nguồn "Bỗng, âm báo tin nhắn của điện thoại Yên Vân reo lên."
    When tôi sinh thuyết minh cho "S3"
    Then văn bản gửi tới TTS sau khi bỏ thẻ SSML giống hệt đoạn nguồn
    And phụ đề của "S3" là "Bỗng, âm báo tin nhắn của điện thoại Yên Vân reo lên."

  Scenario: Ký hiệu trình bày chỉ bỏ khi đọc
    Given shot "S7" có đoạn nguồn "*Bố* [Về ăn cơm]"
    And quy tắc SYM-01 và SYM-02 đang bật
    When tôi sinh thuyết minh cho "S7"
    Then bản đọc gửi TTS là "Bố Về ăn cơm"
    And phụ đề của "S7" là "*Bố* [Về ăn cơm]"

  Scenario: Nghe và đánh dấu không chặn xuất
    Given mọi shot của "C1" có ảnh và thuyết minh "DONE"
    When tôi đánh dấu "S3" là "cần sinh lại"
    Then chương "C1" vẫn "Sẵn sàng dựng"
    And báo cáo điều kiện xuất có cảnh báo "1 shot được đánh dấu cần sinh lại"
    And nút "Xuất video" vẫn bật
```

### US-EDT-04 Track thuyết minh bị khóa

```gherkin
Feature: Trình chỉnh sửa không làm mất lời đọc
  Scenario: Không xóa được clip thuyết minh
    Given timeline chương "C1" có 8 clip thuyết minh
    When tôi chọn clip thuyết minh của shot 3 và nhấn Delete
    Then clip vẫn còn trên timeline
    And tôi thấy thông báo "Thuyết minh nguyên văn không thể xóa hoặc cắt"

  Scenario: Dời clip thuyết minh để chèn khoảng lặng
    When tôi kéo clip thuyết minh của shot 5 sang phải 1 giây
    Then clip ảnh của shot 5 kéo dài để phủ hết lời đọc
    And các clip phía sau dời theo 1 giây

  Scenario: Thêm SFX và nhạc nền tải lên
    Given timeline chương "C1" đã sẵn sàng và tôi đã tải lên "Calm piano" và "Pháo hoa"
    When tôi kéo SFX "Pháo hoa" vào track SFX tại 01:42
    And kéo nhạc "Calm piano" vào track Nhạc nền từ 00:00 với ducking -12 dB
    Then khi xem trước, nhạc nhỏ lại trong lúc thuyết minh đọc
    And độ phủ văn bản vẫn là 100%
```

### US-EDT-21 Giới hạn tài khoản Free

```gherkin
Feature: Render của tài khoản Free
  Scenario: Hết lượt render trong tháng
    Given tài khoản của tôi là "Free" và đã render 3 lần trong tháng này
    When tôi bấm "Xuất video"
    Then tôi nhận lỗi "FREE_LIMIT_REACHED"
    And tôi thấy gợi ý "Nạp tiền"

  Scenario: Nạp tiền rồi render lại
    Given video đã render khi tài khoản còn "Free" có watermark
    When tôi nạp $5 qua cổng sandbox và webhook xác nhận
    And tôi render lại
    Then video mới không có watermark và có thể chọn 1080p
```

### US-MAN-05 Chia chương nguyên tử

```gherkin
  Scenario: Một thao tác lỗi thì không thay đổi gì
    Given dự án có chương C1 (v2) và C2 (v5)
    When tôi gửi restructure gồm SPLIT C1 với ifMatch 2 và MERGE C2 với ifMatch 4
    Then tôi nhận lỗi 409
    And danh sách chương và phiên bản không thay đổi
```

> Hai mẫu của bản trước chuyển sang sau MVP: US-PRJ-11 (xung đột khi hai người cùng sửa, UC-02.10) và US-DIR-05 (điểm duyệt của Director, UC-07.03..06).

## 4. Ma trận truy vết yêu cầu (RTM)

Mỗi use case chính có một dòng. Cột "Yêu cầu chức năng" gộp mục Truy vết của use case chính và các use case con (include/extend) trong [03](03-dac-ta-use-case/00-muc-luc.md). Cột "GĐ" lấy từ dòng Giai đoạn của use case (P0–P3 thuộc MVP; "Sau" là sau MVP; ✂n là thứ tự cắt giảm). Cột "Sơ đồ" liệt kê sơ đồ dữ liệu, tuần tự, hoạt động, trạng thái liên quan (bản MVP cùng tên có hậu tố `-mvp` trong `so-do/mvp/`); sơ đồ use case phân rã không nhắc lại. Cột "Mục tiêu KD" theo [BRD §2](01-tai-lieu-yeu-cau-nghiep-vu-BRD.md); "—" là chức năng nền tảng. Mã test định nghĩa ở §4.13.

### 4.1 M01 — Tích hợp SSO & hồ sơ

| Use case | GĐ | Yêu cầu chức năng | Mục tiêu KD | Sơ đồ | Test chính |
|---|---|---|---|---|---|
| UC-01.01 Đăng nhập qua SSO | P0 | FR-AUTH-01..04, 06, 07, 11, 12, 13; FR-BIL-10 | — | act-m01-dang-nhap, seq-dang-nhap-sso | E2E-sso-login-logout, IT-id-token-validation, IT-invite-gate, IT-consent-required, IT-trial-grant, IT-vbee-adapter |
| UC-01.02 Đăng xuất | P0 | FR-AUTH-05 | — | act-m01-dang-nhap, seq-dang-nhap-sso | E2E-sso-login-logout |
| UC-01.03 Xem Dashboard | P2 | FR-AUTH-09; FR-BIL-05, 12 | BO-05 | seq-quan-ly-du-an | IT-dashboard-summary |
| UC-01.04 Đổi ngôn ngữ giao diện | P3 | FR-AUTH-08 | — | seq-quan-ly-du-an | IT-locale-preference |
| UC-01.05 Mở trang quản lý tài khoản SSO | P2 | FR-AUTH-09 | — | seq-quan-ly-du-an | E2E-sso-login-logout |
| UC-01.06 Yêu cầu xóa dữ liệu ứng dụng | Sau | FR-AUTH-10 | — | — | IT-account-deletion |
| UC-01.07 Nhận đăng xuất back-channel | Sau | FR-AUTH-05 | — | — | IT-backchannel-logout |

### 4.2 M02 — Quản lý dự án & cộng tác

| Use case | GĐ | Yêu cầu chức năng | Mục tiêu KD | Sơ đồ | Test chính |
|---|---|---|---|---|---|
| UC-02.01 Xem danh sách dự án | P1 | FR-PRJ-01 | — | seq-quan-ly-du-an | IT-project-list-filter |
| UC-02.02 Nhập truyện giữ nguyên văn (Import) | P1 | FR-PRJ-02, 03; FR-BIL-12 | BO-01, BO-03 | act-m03-ban-thao-chuong, seq-import-chia-chuong | IT-PRJ-import, IT-free-limits |
| UC-02.03 Tạo dự án trống | P1 | FR-PRJ-04; FR-BIL-12 | BO-01 | seq-import-chia-chuong | IT-project-list-filter, IT-free-limits |
| UC-02.04 Cài đặt dự án | P1 | FR-PRJ-07 | BO-02 | seq-quan-ly-du-an | IT-project-settings-authz |
| UC-02.05 Xóa dự án | P1 | FR-PRJ-01 | — | seq-quan-ly-du-an | IT-project-delete |
| UC-02.06 Tạo / thu hồi link mời | Sau | FR-PRJ-08 | — | seq-cong-tac-xung-dot | IT-invite-link |
| UC-02.07 Quản lý thành viên | Sau | FR-PRJ-09 | — | — | IT-member-remove |
| UC-02.08 Tham gia dự án qua link | Sau | FR-AUTH-03; FR-PRJ-08 | — | — | IT-invite-link, E2E-collab-conflict |
| UC-02.09 Xem bản đồ quy trình (Map) | P3 ✂2 | FR-PRJ-06 | BO-01 | seq-quan-ly-du-an | E2E-project-map |
| UC-02.10 Xử lý xung đột khi lưu | Sau | FR-EDT-18; FR-PRJ-11 | BO-03 | seq-cong-tac-xung-dot | E2E-collab-conflict, IT-chapter-save-optimistic-lock |
| UC-02.11 Nhân bản dự án | Sau | FR-PRJ-13 | — | — | IT-project-duplicate |

### 4.3 M03 — Bản thảo & chương

| Use case | GĐ | Yêu cầu chức năng | Mục tiêu KD | Sơ đồ | Test chính |
|---|---|---|---|---|---|
| UC-03.01 Xem văn bản gốc | P1 | FR-MAN-01; FR-PRJ-02, 03 | BO-03 | act-m03-ban-thao-chuong, seq-import-chia-chuong, seq-quan-ly-du-an | IT-PRJ-import |
| UC-03.02 Soạn thảo trong Workspace | P1 | FR-MAN-02, 11; FR-BOK-01b; FR-NAR-09 | BO-03 | act-m03-ban-thao-chuong, act-phu-kin-van-ban, seq-doi-ranh-gioi-shot | IT-chapter-save-optimistic-lock, IT-move-shot-boundary, PBT-coverage-validator |
| UC-03.03 Gợi ý chia chương bằng AI | P1 | FR-MAN-04; FR-BIL-12 | BO-01 | act-m03-ban-thao-chuong, seq-import-chia-chuong | IT-split-suggest-schema |
| UC-03.04 Chia chương tại vị trí | P1 | FR-MAN-03; FR-BIL-12 | BO-01 | act-m03-ban-thao-chuong, seq-import-chia-chuong | PBT-chapter-text-preserved, IT-free-limits |
| UC-03.05 Gộp chương vào chương trước | P1 | FR-MAN-05 | BO-01 | act-m03-ban-thao-chuong, seq-import-chia-chuong | PBT-chapter-text-preserved |
| UC-03.06 Dời ranh giới chương | P1 | FR-MAN-05 | BO-01 | act-m03-ban-thao-chuong, seq-import-chia-chuong | PBT-chapter-text-preserved |
| UC-03.07 Thêm / xóa / đổi tên chương | P1 | FR-MAN-05; FR-BIL-12 | BO-01 | act-m03-ban-thao-chuong, seq-import-chia-chuong | IT-restructure-atomic, IT-free-limits |
| UC-03.08 Sắp xếp lại chương | P1 | FR-MAN-05 | BO-01 | act-m03-ban-thao-chuong, seq-import-chia-chuong | IT-restructure-atomic |
| UC-03.09 Tái cấu trúc nguyên tử | P1 | FR-MAN-06 | BO-01, BO-03 | act-m03-ban-thao-chuong, seq-import-chia-chuong | IT-restructure-atomic, PBT-chapter-text-preserved |
| UC-03.10 Tìm & thay thế | Sau | FR-MAN-07 | BO-03 | — | IT-find-replace |
| UC-03.11 Lưu Archive | Sau | FR-MAN-08 | BO-03 | — | IT-archive-immutable |
| UC-03.12 Xem / sao chép / xóa Archive | Sau | FR-MAN-08 | BO-03 | — | IT-archive-immutable |
| UC-03.13 Quản lý ghi chú (Notes) | Sau | FR-MAN-09 | — | — | IT-notes-crud |
| UC-03.14 Xem & khôi phục phiên bản chương | Sau | FR-MAN-10 | BO-03 | — | IT-chapter-version-restore |

### 4.4 M04 — Thế giới truyện

| Use case | GĐ | Yêu cầu chức năng | Mục tiêu KD | Sơ đồ | Test chính |
|---|---|---|---|---|---|
| UC-04.01 Phân tích tài sản bằng AI | P1 | FR-WLD-01 | BO-01, BO-02 | act-m04-the-gioi-truyen, seq-the-gioi-truyen | IT-analyze-assets, EVAL-asset-extraction |
| UC-04.02 Quản lý Story Assets | P1 | FR-WLD-02, 03, 05, 11, 12, 13; FR-LIB-05 | BO-02 | act-m04-the-gioi-truyen, seq-the-gioi-truyen, seq-tai-san-phong-cach | IT-story-asset-crud |
| UC-04.03 Sinh ảnh tham chiếu | P1 | FR-WLD-03 | BO-02, BO-06 | act-m04-the-gioi-truyen, seq-the-gioi-truyen | EVAL-consistency, IT-wallet-refund |
| UC-04.04 Dùng ảnh tải lên nguyên bản | P1 | FR-WLD-04 | BO-02 | act-m04-the-gioi-truyen, seq-the-gioi-truyen | IT-exact-image-upload |
| UC-04.05 Chọn style dự án | P1 | FR-WLD-06 | BO-02 | act-m04-the-gioi-truyen, seq-tai-san-phong-cach | IT-regenerate-all |
| UC-04.06 Thiết lập Art Direction | P1 | FR-WLD-07 | BO-02 | act-m04-the-gioi-truyen, seq-tai-san-phong-cach | UT-prompt-compiler-order |
| UC-04.07 Xem dòng thời gian truyện | P2 ✂5 | FR-WLD-08 | BO-02 | act-m04-the-gioi-truyen, seq-the-gioi-truyen | IT-story-timeline |
| UC-04.08 Xem đồ thị quan hệ | P2 ✂4 | FR-WLD-09 | BO-02 | act-m04-the-gioi-truyen, seq-the-gioi-truyen | IT-relationship-graph, UT-relationship-at-chapter |
| UC-04.09 Phân tích lại (Re-analyse) | P2 ✂4 ✂5 | FR-WLD-08, 09 | BO-02 | act-m04-the-gioi-truyen, seq-the-gioi-truyen | IT-story-timeline, IT-relationship-graph, UT-relationship-at-chapter |
| UC-04.10 Quản lý Visual Rules | P1 | FR-WLD-10 | BO-02 | act-m04-the-gioi-truyen, seq-tai-san-phong-cach | UT-prompt-compiler-order |
| UC-04.11 Xuất ZIP ảnh tài sản | Sau | FR-WLD-11 | — | — | IT-asset-zip-export |

### 4.5 M05 — Sinh tư liệu: storyboard, ảnh, thuyết minh nguyên văn

| Use case | GĐ | Yêu cầu chức năng | Mục tiêu KD | Sơ đồ | Test chính |
|---|---|---|---|---|---|
| UC-05.01 Tạo bản nháp storyboard | P1 | FR-BOK-01, 01a, 05 | BO-01, BO-03 | act-m05-sinh-tu-lieu, act-phu-kin-van-ban, seq-storyboard-sinh-anh | IT-storyboard-schema, PBT-coverage-validator, UT-sentence-segmenter, PBT-segmenter-coverage, EVAL-segmenter-golden |
| UC-05.02 Quản lý bản nháp | Sau | FR-BOK-02 | BO-03 | seq-storyboard-sinh-anh | IT-storyboard-schema |
| UC-05.03 Chia lại shot (nhiều / ít hơn) | P1 | FR-BOK-03 | BO-01 | seq-storyboard-sinh-anh | IT-redirect-preserves-source, PBT-coverage-validator |
| UC-05.04 Thiết lập Chapter rules | Sau | FR-BOK-04 | BO-02 | — | UT-prompt-compiler-order |
| UC-05.05 Chỉ đạo lại cả chương (Re-direct) | Sau | FR-BOK-07 | BO-01 | — | IT-redirect-preserves-source |
| UC-05.06 Biên tập shot | P1 | FR-BOK-05, 06, 08; FR-NAR-09 | BO-02, BO-03 | act-m05-sinh-tu-lieu, seq-storyboard-sinh-anh | PBT-coverage-validator, IT-auto-link-assets |
| UC-05.07 Sinh tư liệu chương | P2 | FR-BOK-01; FR-MED-01..05; FR-BIL-11 | BO-01, BO-06 | act-m05-sinh-tu-lieu, seq-sinh-tu-lieu, seq-storyboard-sinh-anh | E2E-generate-media-chapter, IT-quote-total, IT-daily-budget-cap, IT-flow-settlement, IT-chapter-lock-release, EVAL-cost-per-minute |
| UC-05.08 Xem Tư liệu dự án (media bin) | P1 | FR-BOK-13; FR-MED-03 | BO-01 | act-m05-sinh-tu-lieu, seq-sinh-tu-lieu | E2E-generate-media-chapter |
| UC-05.09 Sinh ảnh shot | P1 | FR-BOK-09 | BO-02 | act-m05-sinh-tu-lieu, seq-storyboard-sinh-anh | E2E-shot-image, IT-wallet-refund, EVAL-consistency, EVAL-refusal-rate |
| UC-05.10 Sửa ảnh | P1 | FR-BOK-10 | BO-02 | seq-storyboard-sinh-anh | E2E-shot-image |
| UC-05.11 Cài đặt thuyết minh | P2 | FR-NAR-01, 03 | BO-04 | act-m05-sinh-tu-lieu, seq-thuyet-minh-nguyen-van | IT-narration-settings, IT-symbol-rules |
| UC-05.12 Quản lý từ điển phát âm | P2 ✂6 | FR-NAR-04 | BO-04 | act-m05-sinh-tu-lieu, seq-thuyet-minh-nguyen-van | IT-pronunciation-dictionary |
| UC-05.13 Sinh thuyết minh nguyên văn | P2 | FR-NAR-02..04, 06 | BO-03, BO-04 | act-m05-sinh-tu-lieu, seq-thuyet-minh-nguyen-van | IT-tts-input-equals-source, IT-symbol-rules, EVAL-wer-golden, EVAL-alignment, BENCH-tts, UT-normalization-map, PBT-normalization-map, UT-timing-map, IT-tts-port-contract |
| UC-05.14 Duyệt shot cần xem lại (NEEDS_REVIEW) | Sau | FR-NAR-07 | BO-03, BO-04 | act-m05-sinh-tu-lieu, seq-thuyet-minh-nguyen-van, state-narration-render | E2E-needs-review |
| UC-05.15 Gán giọng theo nhân vật | Sau | FR-NAR-05 | BO-04 | — | IT-multi-voice |
| UC-05.16 Tải ZIP ảnh | Sau | FR-BOK-16 | — | — | IT-asset-zip-export |
| UC-05.17 Giữ / trừ / hoàn tiền | P1 | FR-BIL-11 | BO-06 | act-m05-sinh-tu-lieu, act-giu-tru-tien, seq-vong-doi-job | PBT-wallet-ledger, IT-wallet-refund, IT-daily-budget-cap, IT-daily-budget-concurrency, IT-job-redelivery |
| UC-05.18 Nghe & đánh dấu cần sinh lại | P2 | FR-NAR-08 | BO-03, BO-04 | act-m05-sinh-tu-lieu, seq-thuyet-minh-nguyen-van, state-narration-render, seq-sinh-tu-lieu | E2E-listen-flag, IT-render-readiness |

### 4.6 M06 — Trình chỉnh sửa & xuất video

| Use case | GĐ | Yêu cầu chức năng | Mục tiêu KD | Sơ đồ | Test chính |
|---|---|---|---|---|---|
| UC-06.01 Mở trình chỉnh sửa | P3 | FR-EDT-01..03 | BO-01 | act-m06-chinh-sua-xuat-video, seq-chinh-sua-xuat-video, seq-sinh-tu-lieu | IT-media-sync |
| UC-06.02 Thao tác timeline | P3 | FR-EDT-03, 04, 18, 20 | BO-01, BO-03 | act-m06-chinh-sua-xuat-video, seq-chinh-sua-xuat-video | UT-timeline-ops, UT-narration-track-locked |
| UC-06.03 Quản lý track | P3 | FR-EDT-02, 15 | BO-01 | act-m06-chinh-sua-xuat-video, seq-chinh-sua-xuat-video | UT-timeline-ops |
| UC-06.04 Đặt hiệu ứng Ken Burns & điểm tập trung | P3 | FR-EDT-06 | BO-01 | act-m06-chinh-sua-xuat-video, seq-chinh-sua-xuat-video | UT-visual-effects |
| UC-06.05 Đặt chuyển cảnh | P3 (nâng cao ✂3) | FR-EDT-07 | BO-01 | act-m06-chinh-sua-xuat-video, seq-chinh-sua-xuat-video | UT-visual-effects |
| UC-06.06 Chọn khung hình & tinh chỉnh màu | P3 | FR-EDT-08, 09 | BO-01 | act-m06-chinh-sua-xuat-video, seq-chinh-sua-xuat-video | UT-visual-effects |
| UC-06.07 Thêm overlay chữ / logo, clip tiêu đề & kết | Sau | FR-EDT-05, 10 | BO-01 | act-m06-chinh-sua-xuat-video, seq-chinh-sua-xuat-video | UT-overlay-title |
| UC-06.08 Định kiểu phụ đề | P3 (preset ✂3) | FR-EDT-11 | BO-03 | act-m06-chinh-sua-xuat-video, seq-chinh-sua-xuat-video | IT-subtitle-verbatim |
| UC-06.09 Thêm nhạc nền | P3 | FR-EDT-13 | BO-01 | act-m06-chinh-sua-xuat-video, seq-chinh-sua-xuat-video | E2E-editor-sfx-music |
| UC-06.10 Thêm SFX | P3 | FR-EDT-14 | BO-01 | act-m06-chinh-sua-xuat-video, seq-chinh-sua-xuat-video | E2E-editor-sfx-music |
| UC-06.11 Tìm trong thư viện âm thanh | P3 | FR-EDT-12, 14, 27 | BO-01 | act-m06-chinh-sua-xuat-video, seq-chinh-sua-xuat-video | E2E-editor-sfx-music, IT-audio-upload |
| UC-06.12 Trộn âm & chuẩn hóa loudness | Sau | FR-EDT-15 | BO-01 | — | IT-loudness-normalize |
| UC-06.13 Xem trước | P3 ✂9 | FR-EDT-17 | BO-01 | act-m06-chinh-sua-xuat-video, seq-chinh-sua-xuat-video | E2E-preview-sync |
| UC-06.14 Xem lịch sử & khôi phục phiên bản timeline | Sau | FR-EDT-18 | — | — | IT-timeline-autosave |
| UC-06.15 Đồng bộ khi tư liệu thay đổi | P3 | FR-EDT-19 | BO-03 | act-m06-chinh-sua-xuat-video, seq-chinh-sua-xuat-video | IT-media-sync |
| UC-06.16 Xuất video MP4 | P3 | FR-EDT-21..24, 26, 28; FR-BIL-12 | BO-03, BO-06 | act-m06-chinh-sua-xuat-video, seq-chinh-sua-xuat-video | IT-render-readiness, IT-subtitle-verbatim, IT-free-render-quota, BENCH-render, UT-snapshot-schema, IT-project-render |
| UC-06.17 Tải MP4 / SRT / audio | P3 | FR-EDT-24, 25 | BO-01 | act-m06-chinh-sua-xuat-video, seq-chinh-sua-xuat-video | IT-render-download |

### 4.7 M07 — AI Director

| Use case | GĐ | Yêu cầu chức năng | Mục tiêu KD | Sơ đồ | Test chính |
|---|---|---|---|---|---|
| UC-07.01 Ra lệnh bằng chat | Sau | FR-DIR-01..03, 08 | BO-01, BO-03 | seq-director, state-tool-proposal | IT-tool-authz, SEC-prompt-injection |
| UC-07.02 Chạy chế độ tự động | Sau | FR-DIR-04..07 | BO-01 | seq-director | E2E-director-draft-timeline |
| UC-07.03 Chọn style (điểm duyệt) | Sau | FR-DIR-05 | BO-02 | — | E2E-director-checkpoints |
| UC-07.04 Duyệt cast (điểm duyệt) | Sau | FR-DIR-05 | BO-02 | — | E2E-director-checkpoints |
| UC-07.05 Chọn giọng (điểm duyệt) | Sau | FR-DIR-05 | BO-04 | — | E2E-director-checkpoints |
| UC-07.06 Duyệt thuyết minh (điểm duyệt) | Sau | FR-DIR-05 | BO-03, BO-04 | — | E2E-director-checkpoints |
| UC-07.07 Tạm dừng / tiếp tục / thoát | Sau | FR-DIR-06 | BO-01 | — | IT-director-pause-resume |
| UC-07.08 Xem tiến độ & Director note | Sau | FR-DIR-06, 08 | BO-01 | — | IT-director-pause-resume |

### 4.8 M08 — Thư viện tài sản cá nhân

| Use case | GĐ | Yêu cầu chức năng | Mục tiêu KD | Sơ đồ | Test chính |
|---|---|---|---|---|---|
| UC-08.01 Xem thư viện | Sau | FR-LIB-01, 02 | BO-02 | — | IT-library-crud |
| UC-08.02 Tạo tài sản từ ảnh hoặc mô tả | Sau | FR-LIB-03 | BO-02 | — | IT-library-crud |
| UC-08.03 Sửa / xóa tài sản | Sau | FR-LIB-05; FR-WLD-05 | BO-02 | — | IT-library-crud, IT-library-copy-on-add |
| UC-08.04 Lưu tài sản từ dự án vào thư viện | Sau | FR-LIB-04 | BO-02 | — | IT-library-copy-on-add |
| UC-08.05 Thêm tài sản vào dự án | Sau | FR-LIB-05; FR-WLD-05 | BO-02 | — | IT-library-copy-on-add |

### 4.9 M09 — Ví & thanh toán

| Use case | GĐ | Yêu cầu chức năng | Mục tiêu KD | Sơ đồ | Test chính |
|---|---|---|---|---|---|
| UC-09.01 Xem bảng giá | P3 | FR-BIL-01 | BO-05 | act-m09-vi-thanh-toan, seq-thanh-toan | IT-pricing-page |
| UC-09.02 Đăng ký gói | Sau | FR-BIL-02 | BO-05 | seq-thanh-toan, state-subscription | IT-webhook-idempotent |
| UC-09.03 Nạp tiền vào ví | P3 ✂1 | FR-BIL-03 | BO-05 | act-m09-vi-thanh-toan, seq-thanh-toan | E2E-topup-sandbox, IT-webhook-idempotent |
| UC-09.04 Quản lý thanh toán | Sau | FR-BIL-04 | BO-05 | seq-thanh-toan | IT-webhook-idempotent |
| UC-09.05 Xem số dư ví | P2 | FR-BIL-05, 12 | BO-05 | act-m09-vi-thanh-toan, seq-thanh-toan | IT-wallet-balance |
| UC-09.06 Xem lịch sử chi tiêu | P3 | FR-BIL-06, 08 | BO-05, BO-06 | act-m09-vi-thanh-toan, seq-thanh-toan | IT-spend-history, REC-ledger |
| UC-09.08 Xử lý webhook thanh toán | P3 ✂1 | FR-BIL-09 | BO-05 | act-m09-vi-thanh-toan, seq-thanh-toan | IT-webhook-idempotent, REC-ledger |

### 4.10 M10 — Quản trị

| Use case | GĐ | Yêu cầu chức năng | Mục tiêu KD | Sơ đồ | Test chính |
|---|---|---|---|---|---|
| UC-10.01 Cấu hình bảng giá | P1 | FR-ADM-01 | BO-06 | seq-quan-tri | IT-price-rules-versioned |
| UC-10.02 Cấu hình gói đăng ký | Sau | FR-ADM-02 | BO-05 | — | IT-plan-sync |
| UC-10.03 Quản lý provider & mô hình AI | P1 | FR-ADM-03 | BO-06 | seq-quan-tri | IT-catalog-admin |
| UC-10.04 Quản lý danh mục style | P1 | FR-ADM-03 | BO-02 | seq-quan-tri | IT-catalog-admin |
| UC-10.05 Quản lý danh mục giọng đọc | P1 | FR-ADM-03 | BO-04 | seq-quan-tri | IT-catalog-admin |
| UC-10.06 Quản lý thư viện nhạc & SFX có license | Sau | FR-ADM-03; FR-EDT-12 | — | — | IT-catalog-admin |
| UC-10.07 Giám sát job | Sau | FR-ADM-04, 05 | BO-06 | — | IT-job-monitor-actions |
| UC-10.08 Điều chỉnh số dư người dùng | Sau | FR-ADM-05 | BO-06 | — | IT-admin-audit, REC-ledger |
| UC-10.09 Ghi audit log | P1 | — | — | seq-quan-tri | IT-admin-audit |
| UC-10.10 Xem báo cáo | Sau | FR-ADM-06 | BO-05, BO-06 | — | IT-admin-reports |
| UC-10.11 Quản lý danh sách mời beta | P1 | FR-AUTH-11 | BO-06 | seq-dang-nhap-sso, seq-quan-tri | IT-invite-gate, IT-admin-audit |
| UC-10.12 Áp trần chi tiêu AI hằng ngày | P2 | FR-ADM-07 | BO-06 | act-giu-tru-tien, seq-quan-tri, seq-vong-doi-job | IT-daily-budget-cap, IT-daily-budget-concurrency |

### 4.11 Yêu cầu xuyên suốt và yêu cầu chưa có use case

| Yêu cầu chức năng | Nội dung | GĐ | Mục tiêu KD | Cách đáp ứng | Test chính |
|---|---|---|---|---|---|
| FR-PRJ-05 | Bố cục Studio (thanh trái, các nhóm màn hình) | P1 | BO-01 | Xuyên suốt mọi màn hình Studio, không gắn một use case | E2E-studio-navigation |
| FR-PRJ-10 | Ma trận quyền theo 08 §2 | P1 | — | Xuyên suốt; áp cho mọi use case có tiền điều kiện về vai trò | IT-permission-matrix |
| FR-PRJ-12 | Đẩy thay đổi của người khác theo thời gian thực | Sau | — | Xuyên suốt (SSE); trạng thái job vẫn đẩy qua SSE trong MVP | IT-realtime-events |
| FR-DIR-09 | Director đánh giá kết quả một bước và đề xuất sửa | Sau | BO-02 | **Chưa có use case.** Cần bổ sung use case con của UC-07.02 trước khi làm | — |
| BR-32 | Giới hạn kỹ thuật (≤ 30 yêu cầu LLM/phút/người, 1 render đang chạy/người, ≤ 10 lần nghe thử/phút) | P0 | — | Middleware rate limit ở `platform` | IT-rate-limit |
| 06 §1.2 | Hợp đồng API của các endpoint MVP | P0 | — | OpenAPI viết trước, so trong CI (06 §1.2) | IT-openapi-contract |
| Mốc M1 | Khung chạy đầu-cuối luồng 6 bước (không editor) | P1 | BO-01, BO-03 | Ghép UC-02.02, UC-05.07, UC-06.16 ở mức tối giản (§1.2) | E2E-walking-skeleton |

### 4.12 Độ phủ

| Chỉ số | Kết quả |
|---|---|
| Use case chính có trong RTM | 110 / 110 |
| Use case chính thuộc MVP | 68 / 110 |
| Use case chính có ít nhất một test | 110 / 110 |
| FR truy vết tới use case | 131 / 135 |
| FR thuộc MVP | 92 / 135 |
| FR xuyên suốt (§4.11) | 3 |
| FR chưa có use case | 1 (FR-DIR-09, xem §4.11) |

Khi thêm hoặc đổi use case, cập nhật mục Truy vết và Giai đoạn của use case đó trước, rồi cập nhật dòng tương ứng ở đây.

### 4.13 Danh mục mã test

Quy ước mã `<MỨC>-<chủ đề>`:

| Mức   | Ý nghĩa                                                                               |
| ----- | ------------------------------------------------------------------------------------- |
| UT    | Unit test                                                                             |
| IT    | Integration test (API + DB + hàng đợi, provider AI dùng mock adapter)                 |
| E2E   | Kiểm thử đầu-cuối trên trình duyệt                                                    |
| PBT   | Property-based test                                                                   |
| EVAL  | Bộ đánh giá chất lượng AI trên golden set, chạy khi đổi provider, mô hình hoặc prompt |
| BENCH | Benchmark hiệu năng trên máy tham chiếu                                               |
| SEC   | Kiểm thử bảo mật                                                                      |
| REC   | Đối soát dữ liệu định kỳ                                                              |

| Mã | Mức | MVP | Nội dung kiểm tra |
|---|---|---|---|
| `E2E-sso-login-logout` | E2E | ✓ | Đăng nhập, quay về URL đích, đăng xuất RP-initiated trên môi trường SSO test |
| `IT-id-token-validation` | IT | ✓ | Từ chối ID token sai chữ ký JWKS, `iss`, `aud`, `nonce` hoặc hết hạn; JIT tạo hồ sơ một lần |
| `IT-invite-gate` | IT | ✓ | Email chưa có trong danh sách mời không tạo được hồ sơ, không nhận tiền dùng thử; email đã mời tạo được; thu hồi lời mời không khóa hồ sơ đã có (BR-30) |
| `IT-consent-required` | IT | ✓ | Chưa đồng ý xử lý dữ liệu thì mọi API ngoài /auth, /me, /me:consent trả 403 CONSENT_REQUIRED; đổi phiên bản thông báo thì hỏi lại (BR-31) |
| `IT-trial-grant` | IT | ✓ | Hồ sơ mới có đúng một TRIAL_GRANT $2; không tặng lại; tiền dùng thử không làm tài khoản thành "Đã nạp tiền" (BR-28, IC-16) |
| `IT-vbee-adapter` | IT | ✓ | Đổi IdentityProviderPort sang Vbee bằng cấu hình (OIDC hoặc OAuth 2.0 + userinfo); claims ánh xạ đúng (FR-AUTH-13) |
| `IT-backchannel-logout` | IT |  | Logout token hợp lệ hủy mọi phiên của `sid`/`sub`; token sai bị từ chối |
| `IT-dashboard-summary` | IT | ✓ | Dashboard trả đúng trạng thái Free / Đã nạp tiền, số dư khả dụng / đang giữ, phần Free đã dùng, số dự án |
| `IT-locale-preference` | IT | ✓ | Ngôn ngữ mặc định theo claim `locale`, ghi đè được và lưu ở hồ sơ |
| `IT-account-deletion` | IT |  | Yêu cầu xóa dữ liệu: ẩn ngay, xóa vĩnh viễn đúng hạn, giữ ledger theo luật |
| `IT-project-list-filter` | IT | ✓ | Danh sách dự án chỉ gồm dự án là Owner/Editor; tìm, lọc, trạng thái suy ra đúng |
| `IT-PRJ-import` | IT | ✓ | Import .txt/.md/.docx: văn bản sau chuẩn hóa kỹ thuật giữ nguyên từng chữ; vượt giới hạn bị chặn |
| `IT-free-limits` | IT | ✓ | Free: dự án thứ 2, chương thứ 4 bị chặn với 403 FREE_LIMIT_REACHED; đã nạp tiền thì không chặn (BR-27) |
| `IT-project-settings-authz` | IT | ✓ | Chỉ Owner đổi cài đặt và xóa dự án (ma trận quyền 08 §2) |
| `IT-project-delete` | IT | ✓ | Xóa dự án xóa mềm, hủy job đang chạy, RELEASE tiền đang giữ |
| `E2E-collab-conflict` | E2E |  | Mời qua link, tham gia làm Editor, hai người lưu cùng phiên bản thì hiện hộp thoại xung đột |
| `IT-invite-link` | IT |  | Link mời hết hạn hoặc bị thu hồi thì không tham gia được |
| `IT-member-remove` | IT |  | Owner xóa thành viên; thành viên mất quyền ngay ở request kế tiếp |
| `E2E-project-map` | E2E | ✓ | Map hiển thị đúng chặng hiện tại theo trạng thái dự án |
| `IT-project-duplicate` | IT |  | Nhân bản dự án sao chép chương và tài sản, không sao chép render |
| `IT-chapter-save-optimistic-lock` | IT | ✓ | Lưu chương với `If-Match` sai phiên bản trả `409`, không ghi đè ngầm (BR-05) |
| `IT-restructure-atomic` | IT | ✓ | Chuỗi split/merge/move/reorder chạy trong một giao dịch; một thao tác lỗi thì rollback toàn bộ |
| `IT-split-suggest-schema` | IT | ✓ | Gợi ý chia chương của LLM đúng schema; điểm chia rơi vào ranh giới đoạn |
| `PBT-chapter-text-preserved` | PBT | ✓ | Mọi thao tác chia/gộp/dời ranh giới: nối các chương lại bằng đúng văn bản trước đó |
| `IT-move-shot-boundary` | IT | ✓ | Dời ranh giới shot từ Workspace: dryRun trả giá và câu chuyển; xác nhận thì phủ kín 100%, 2 job REWRITE_SHOT, thuyết minh 2 shot OUTDATED; hủy thì không đổi gì (BR-33) |
| `IT-find-replace` | IT |  | Find & replace chỉ đổi chương được phép sửa; đánh dấu thuyết minh liên quan `OUTDATED` (BR-06) |
| `IT-archive-immutable` | IT |  | Archive chỉ đọc; sao chép thành dự án mới; xóa không ảnh hưởng chương |
| `IT-notes-crud` | IT |  | Ghi chú gắn dự án, chương hoặc shot; Director chỉ thêm loại "Director note" |
| `IT-chapter-version-restore` | IT |  | Khôi phục phiên bản chương tạo phiên bản mới, không xóa lịch sử |
| `IT-analyze-assets` | IT | ✓ | Job `ANALYZE_ASSETS` map-reduce trả danh sách đúng schema; không tạo tài sản khi chưa duyệt |
| `IT-story-asset-crud` | IT | ✓ | Tạo/sửa/gỡ Story Asset: giữ `id`, tăng `version`, `409` khi xung đột, giới hạn 200 tài sản, IC-13 cho nhóm |
| `EVAL-consistency` | EVAL | ✓ | Golden set: tỷ lệ shot sai ngoại hình nhân vật ≤ 10% khi chọn provider, ≤ 15% (BO-02); ≥ 150 shot, rubric 4 thuộc tính, 2 người chấm, κ ≥ 0,6, khoảng tin cậy 95%, tách shot 1 / ≥ 2 nhân vật (QĐ-110) |
| `EVAL-refusal-rate` | EVAL | ✓ | Tỷ lệ shot golden set bị provider ảnh chặn vì chính sách nội dung ≤ 5% (QĐ-113) |
| `EVAL-asset-extraction` | EVAL | ✓ | `ANALYZE_ASSETS` so với nhãn tay: recall nhân vật có tên ≥ 90%, precision ≥ 80%; chạy khi đổi prompt hoặc mô hình (QĐ-114) |
| `IT-exact-image-upload` | IT | ✓ | Ảnh tải lên qua kiểm tra MIME, kích thước, malware, EXIF; "use exact" không bao giờ bị vẽ lại (BR-14) |
| `IT-regenerate-all` | IT | ✓ | Regenerate all bỏ qua tài sản "use exact"; hoàn tiền giữ cho phần job lỗi |
| `UT-prompt-compiler-order` | UT | ✓ | Prompt ảnh ghép đúng thứ tự style → Art Direction → Visual Rules → mô tả → facts (BR-08) |
| `IT-story-timeline` | IT | ✓ | Phân tích lại gán `order_index`/`chrono_index`; hai chế độ xem sắp đúng |
| `IT-relationship-graph` | IT | ✓ | Đồ thị quan hệ bỏ qua cạnh có tên không khớp tài sản và liệt kê chúng |
| `UT-relationship-at-chapter` | UT | ✓ | Quan hệ hiệu lực ở chương N = giai đoạn có chương bắt đầu gần nhất không sau N; nhãn không đổi giữa các chương thì không tạo giai đoạn mới; cặp chưa bắt đầu thì không có cạnh (QĐ-143, IC-19) |
| `IT-asset-zip-export` | IT |  | ZIP ảnh tài sản/ảnh shot đủ file, tên file an toàn, link ký có thời hạn |
| `IT-storyboard-schema` | IT | ✓ | Bản nháp storyboard của LLM đúng schema, 1–40 shot; quản lý bản nháp, "Set as current" |
| `PBT-coverage-validator` | PBT | ✓ | Mọi bản nháp và mọi thao tác shot: đoạn nguồn liên tục, không chồng lấn, nối lại bằng đúng chương (BR-20) |
| `UT-sentence-segmenter` | UT | ✓ | 22 ca SEG-01..22 của `SentenceSegmenter` (12 §1.4) |
| `PBT-segmenter-coverage` | PBT | ✓ | 10.000 chuỗi ngẫu nhiên: bất biến SEG-I1..I5; tách → nối → tách lại ổn định |
| `EVAL-segmenter-golden` | EVAL | ✓ | Ranh giới câu trên golden set đúng ≥ 98%, không ranh giới nào giữa một từ (12 §1.4) |
| `IT-redirect-preserves-source` | IT | ✓ | Re-split / Re-direct / viết lại brief không đổi văn bản đoạn nguồn (BR-21) |
| `IT-auto-link-assets` | IT | ✓ | Tự khớp tên cast/item/location theo tên và bí danh; tên mơ hồ bị cảnh báo |
| `E2E-generate-media-chapter` | E2E | ✓ | "Sinh tư liệu" một chương: báo giá, sinh ảnh + thuyết minh song song, chương "Sẵn sàng dựng" |
| `IT-quote-total` | IT | ✓ | Giá ước tính tổng bằng tổng giá ước tính từng job (×1,10); sinh lại chọn lọc chỉ tính phần chọn |
| `E2E-shot-image` | E2E | ✓ | Sinh, sửa (Describe→Edit), thay ảnh shot bằng ảnh tải lên; ảnh cũ vẫn chọn lại được |
| `IT-wallet-refund` | IT | ✓ | Job lỗi sau 3 lần thử RELEASE toàn bộ tiền đang giữ; số dư khả dụng trở lại như trước |
| `IT-narration-settings` | IT | ✓ | Cài đặt giọng, tốc độ, ngôn ngữ, bật/tắt quy tắc ký hiệu; nghe mẫu có sẵn miễn phí |
| `IT-pronunciation-dictionary` | IT | ✓ | Từ điển phát âm chỉ đổi bản đọc, không đổi văn bản nguồn và phụ đề |
| `IT-tts-input-equals-source` | IT | ✓ | Văn bản gửi TTS sau khi bỏ SSML bằng đúng đoạn nguồn của shot (BR-19) |
| `IT-tts-port-contract` | IT | ✓ | Mọi adapter TTS (mock, tự host; Vbee sau MVP) chạy cùng bộ test hợp đồng `TtsPort` trên fixture: audio + `durationMs`, `wordTimings` trên bản đọc (UTF-16, đơn điệu), nhóm lỗi chung, `usage` đúng `ai_models.unit` (QĐ-145) |
| `IT-symbol-rules` | IT | ✓ | SYM-01..05: bản đọc bỏ ký hiệu giữ chữ, "---" thành lặng 0,5 s; quy tắc tắt thì giữ ký hiệu; phụ đề luôn hiện nguyên văn kể cả ký hiệu (BR-19, BR-22) |
| `UT-normalization-map` | UT | ✓ | `NormalizationMap` phủ kín cả S và bản đọc, đơn điệu; ghép lại đúng S (12 §2.2) |
| `PBT-normalization-map` | PBT | ✓ | S ngẫu nhiên có ký hiệu, số, mục từ điển: bất biến 12 §2.2 và ánh xạ bản đọc → S đơn điệu |
| `UT-timing-map` | UT | ✓ | Ca MAP-01..08: ánh xạ thời gian từ bản đọc về văn bản gốc và dựng cue phụ đề (12 §2.3–2.5) |
| `EVAL-wer-golden` | EVAL | ✓ | WER hiệu chỉnh (WER theo âm tiết sau chuẩn hóa hai phía − WER nền của ASR trên bản ghi giọng người) ≤ 3% trên golden set vi/en; danh sách khó đọc đúng ≥ 95% (QĐ-111; P0, chạy lại khi đổi provider, giọng, quy tắc chuẩn hóa) |
| `EVAL-alignment` | EVAL | ✓ | Timestamp của TTS hoặc aligner so với nhãn tay biên từ: trung vị ≤ 100 ms, p95 ≤ 250 ms; aligner tự host ≤ 0,5× thời lượng audio trên máy staging (QĐ-115) |
| `EVAL-cost-per-minute` | EVAL | ✓ | Chi phí AI/phút video trên 2 chương golden ở mật độ ảnh đã chốt ≤ $0,15 (BO-06, QĐ-112) |
| `E2E-needs-review` | E2E |  | (Sau MVP) Shot vượt ngưỡng WER chuyển NEEDS_REVIEW, tô đỏ chỗ lệch, khóa xuất cho tới khi xử lý |
| `E2E-listen-flag` | E2E | ✓ | Nghe thuyết minh tô sáng theo từ; đánh dấu / bỏ đánh dấu; sinh lại phạm vi FLAGGED xóa cờ; cờ không chặn xuất (BR-34) |
| `IT-multi-voice` | IT |  | Gán giọng theo nhân vật chỉ áp cho lời thoại trong ngoặc kép; văn bản không đổi |
| `PBT-wallet-ledger` | PBT | ✓ | Mọi chuỗi giữ/trừ/hoàn: số dư = tổng sổ cái, không âm, CAPTURE ≤ HOLD, CAPTURE + RELEASE = HOLD, không trừ hai lần (BR-02, IC-05) |
| `IT-daily-budget-cap` | IT | ✓ | Chạm trần chi tiêu ngày: job tốn phí mới bị 503 DAILY_BUDGET_EXCEEDED, job đang chạy vẫn xong, Admin nhận 1 email; qua 00:00 giờ Việt Nam thì mở lại (BR-29) |
| `IT-daily-budget-concurrency` | IT | ✓ | 50 yêu cầu đồng thời quanh ngưỡng trần: `spent + reserved` không bao giờ vượt `cap`; hết chỗ thì 503; thiếu số dư thì trả chỗ ngân sách (IC-18, ADR-25) |
| `IT-flow-settlement` | IT | ✓ | Sinh tư liệu một chương: chỉ job cha có HOLD, job con `held_micro = 0`; một số con lỗi → CAPTURE đúng chi phí các con thành công × 1,10, RELEASE phần còn lại, một giao dịch; job cha chờ con > 10 phút không bị reconciler coi là treo; worker chết → reconciler quyết toán job cha, hủy con còn chờ, mở khóa chương (WR-05, QĐ-134) |
| `IT-job-redelivery` | IT | ✓ | Giao lại job đã RUNNING/SUCCEEDED cho worker khác: không gọi provider lần hai, không trừ tiền hai lần; job thành công ở lần thử 3 chỉ CAPTURE chi phí lần 3, mọi lần thử đều có `ai_usage_records` (ADR-29, WR-09) |
| `IT-chapter-lock-release` | IT | ✓ | Job cha kết thúc (thành công, lỗi, hủy) mở khóa chương trong cùng giao dịch; worker chết thì reconciler mở khóa (BR-12, ADR-29) |
| `UT-narration-track-locked` | UT | ✓ | Clip thuyết minh không cắt, trim, xóa, đổi thứ tự được (BR-24) |
| `IT-timeline-autosave` | IT |  | Autosave debounce ≤ 2 s, khóa lạc quan; lịch sử phiên bản timeline khôi phục được (sau MVP) |
| `UT-timeline-ops` | UT | ✓ | Kéo thả, cắt, trim, nhân bản, undo/redo trên các track không phải thuyết minh |
| `UT-visual-effects` | UT | ✓ | Ken Burns, chuyển cảnh, khung hình sinh đúng tham số render; tinh chỉnh màu (sau MVP) |
| `UT-overlay-title` | UT |  | (Sau MVP) Overlay chữ/logo, clip tiêu đề và kết hiển thị đúng font tiếng Việt và vị trí |
| `IT-subtitle-verbatim` | IT | ✓ | Phụ đề SRT/VTT và trên video khớp nguyên văn 100%, kể cả ký hiệu trình bày; dòng phân cách không có phụ đề (BR-22) |
| `E2E-editor-sfx-music` | E2E | ✓ | Tải nhạc/SFX lên, thêm nhạc nền và SFX, ducking khi thuyết minh đọc; thư viện hệ thống (sau MVP) |
| `IT-audio-upload` | IT | ✓ | Tải nhạc/SFX: MIME thật, ≤ 100 MB, ≤ 15 phút, quét malware, waveform; không cần cờ cam kết (BR-26) |
| `IT-loudness-normalize` | IT |  | Đầu ra đạt mức loudness mục tiêu; mute/solo track đúng |
| `E2E-preview-sync` | E2E | ✓ | Xem trước bắt đầu ≤ 2 s; lệch hình–tiếng–phụ đề ≤ 100 ms (NFR-PERF-11) |
| `IT-media-sync` | IT | ✓ | Sinh lại ảnh/thuyết minh hoặc đổi storyboard thì timeline đồng bộ, giữ chỉnh sửa của người dùng |
| `IT-render-readiness` | IT | ✓ | Chặn xuất khi độ phủ < 100%, còn ảnh hoặc thuyết minh chưa DONE, hoặc OUTDATED; shot đã đánh dấu chỉ là cảnh báo (BR-23, BR-34) |
| `UT-snapshot-schema` | UT | ✓ | Ca SNP-T01..T06: `timeline_snapshot` theo `schemas/timeline-snapshot.schema.json` và SNP-01..07 (12 §3) |
| `IT-free-render-quota` | IT | ✓ | Free: chỉ 720p, watermark; lượt render thứ 4 hoặc vượt 10 phút/tháng bị 403; render lỗi không tính lượt; đã nạp tiền thì không watermark (BR-27) |
| `IT-project-render` | IT | ✓ | Xuất cả dự án: chương chưa có timeline được dựng bản nháp; một chương chưa đạt thì `422` liệt kê chương; snapshot `PROJECT` hợp lệ schema, thời gian mỗi chương nối tiếp đúng, `coverage` = tổng ký tự mọi chương; Free tính theo tổng thời lượng (QĐ-141) |
| `BENCH-tts` | BENCH | ✓ | P0: TTS tự host + căn timestamp ≤ 0,4× thời lượng audio trên máy GPU đã chọn; ra đơn giá giây GPU cho `ai_models.unit_cost_usd` (QĐ-121, QĐ-123) |
| `BENCH-render` | BENCH | ✓ | P0: đo trên cấu hình máy staging thật, ngưỡng MVP 1 phút 720p ≤ 2 phút (§1.5); sau MVP: 1080p ≤ 1× thời lượng trên 8 vCPU (NFR-PERF-10) |
| `E2E-walking-skeleton` | E2E | ✓ | Mốc M1 (T6): một chương mẫu đi hết import → storyboard → ảnh → TTS → MP4 có phụ đề trên staging với provider thật |
| `IT-render-download` | IT | ✓ | Tải MP4, SRT/VTT, audio qua link ký có thời hạn; link hết hạn bị từ chối |
| `IT-tool-authz` | IT |  | Tool của Director chỉ chạy trong quyền người dùng; tool tốn phí cần xác nhận |
| `SEC-prompt-injection` | SEC |  | Văn bản truyện chứa chỉ thị độc hại không khiến Director gọi tool ngoài whitelist hay sửa văn bản |
| `E2E-director-draft-timeline` | E2E |  | Director tự động chạy tới bản nháp timeline; bỏ qua bước đã xong |
| `E2E-director-checkpoints` | E2E |  | Director dừng ở điểm duyệt style, cast, giọng, thuyết minh; không tạo job tốn phí khi chưa duyệt (US-DIR-05) |
| `IT-director-pause-resume` | IT |  | Pause/Continue/Exit; kế hoạch tiếp tục đúng bước sau khi tải lại trang |
| `IT-library-crud` | IT |  | Thư viện: tạo, tìm, lọc, sửa, xóa; lọc All / My Created / From Projects |
| `IT-library-copy-on-add` | IT |  | Thêm vào dự án / lưu từ dự án sao chép tham chiếu; sửa một bên không đổi bên kia (FR-LIB-05) |
| `E2E-topup-sandbox` | E2E | ✓ | Nạp tiền qua checkout sandbox; webhook cộng TOPUP và topup_total; lần đầu chuyển tài khoản sang "Đã nạp tiền" |
| `IT-webhook-idempotent` | IT | ✓ | Webhook trùng event id chỉ xử lý một lần; chữ ký sai bị từ chối |
| `IT-wallet-balance` | IT | ✓ | Số dư khả dụng / đang giữ / tổng nạp và trạng thái tài khoản khớp sổ cái; cập nhật qua wallet.updated |
| `IT-spend-history` | IT | ✓ | Lịch sử chi tiêu lọc theo dự án và loại thao tác khớp sổ cái; hiện chi phí thực và phí 10% |
| `IT-pricing-page` | IT | ✓ | Pricing hiển thị cách tính giá, đơn giá tham khảo từ price_rules, giới hạn Free, tiền dùng thử |
| `REC-ledger` | REC | ✓ | Reconciler hằng ngày: sổ cái khớp số dư ví, giao dịch của cổng thanh toán và IC-05 |
| `IT-price-rules-versioned` | IT | ✓ | Đổi bảng giá (seed) tạo phiên bản mới; job đang chạy giữ giá cũ; hệ số < 1,00 bị cảnh báo |
| `IT-plan-sync` | IT |  | (Sau MVP) Cấu hình gói đồng bộ với cổng thanh toán |
| `IT-catalog-admin` | IT | ✓ | Seed / bật-tắt provider, style, giọng; mục tắt không còn chọn được; adapter mock / thật chọn bằng cấu hình |
| `IT-job-monitor-actions` | IT |  | (Sau MVP) Lọc job; chạy lại hoặc hoàn tiền thủ công có ghi audit |
| `IT-admin-audit` | IT | ✓ | Mọi thao tác admin (seed, danh sách mời, điều chỉnh số dư) ghi audit log bất biến |
| `E2E-studio-navigation` | E2E | ✓ | Thanh trái của Studio đủ nhóm Write / Your world / Make·Media, mở đúng màn hình `?v=` |
| `IT-permission-matrix` | IT | ✓ | Mọi endpoint theo ma trận quyền 08 §2: Owner, Editor, người ngoài dự án, Admin |
| `IT-realtime-events` | IT |  | Thay đổi chương và trạng thái job của người khác tới client qua SSE ≤ 2 s (NFR-PERF-03) |
| `IT-rate-limit` | IT | ✓ | Quá 30 yêu cầu LLM/phút/người, quá 10 lần nghe thử phát âm/phút hoặc tạo render khi đang có render chạy trả 429 kèm Retry-After (BR-32) |
| `IT-openapi-contract` | IT | ✓ | Spec sinh từ code khớp `openapi/*.yaml` viết tay cho mọi endpoint MVP; mỗi endpoint khai báo đủ mã lỗi (06 §1.2) |
| `IT-admin-reports` | IT |  | (Sau MVP) Báo cáo chi tiêu, chi phí AI theo provider, phí thu khớp ai_usage_records |

## 5. Bảng rủi ro triển khai (QĐ-96)

Xác suất (X) và tác động (T): **C** cao, **TB** trung bình, **T** thấp. "Ngưỡng" là dấu hiệu cho biết rủi ro đang xảy ra. Rà lại ở mỗi buổi retro; đổi trạng thái thì ghi vào sổ quyết định.

| Mã | Rủi ro | X | T | Ngưỡng kích hoạt | Ứng phó | Phụ trách |
|---|---|---|---|---|---|---|
| R-12 | Năng lực không đủ cho MVP | C | C | Vận tốc 2 sprint liên tiếp < 70% kế hoạch; dự báo M2 vượt T24 | Thứ tự cắt giảm 3 tầng (§1.3); kiểm soát tiến độ (§1.4) | PO |
| R-15 | Render / preview không đạt (chậm, lệch khung, máy staging yếu) | TB | C | Benchmark P0 vượt ngưỡng §1.5; M1 không ra MP4; M3 lệch > 1 khung hình | Khung chạy đầu-cuối T6; spike M3; ✂9; nâng cấu hình máy | Frontend & editor |
| R-14 | Vbee giao tài liệu muộn hoặc chỉ có OAuth 2.0 | C | TB | Không phản hồi ở T6; hết T9 chưa có tài liệu | Lịch liên hệ §1.6; adapter tách riêng; giữ Keycloak | PO |
| R-06 | TTS tiếng Việt đọc sai tên riêng, Hán Việt, số | TB | C | Không provider nào đạt WER hiệu chỉnh ≤ 3% ở P0; người dùng beta đánh dấu > 10% shot | Quy tắc dự phòng §1.5; nghe & đánh dấu; từ điển phát âm (thoát khỏi ✂6 nếu WER > 3%) | Backend & AI |
| R-02b | Provider ảnh không giữ được nhân vật | TB | TB | Tỷ lệ sai ngoại hình > 10% ở P0 | Quy tắc dự phòng §1.5; tăng ảnh tham chiếu; Visual Rules | Backend & AI |
| R-01 | Chi phí AI vượt ngân sách | TB | TB | `EVAL-cost-per-minute` ở M0 > $0,15/phút; chi tiêu tuần > 30% hạn mức tháng; chạm trần ngày ≥ 3 lần/tuần khi beta | Mock adapter; giới hạn console provider; trần ngày; danh sách mời | PO |
| R-16 | Mất năng lực do Tết, thi, ốm, một thành viên rời nhóm | C | TB | Thành viên vắng > 1 tuần ngoài §1.9 | Bảng lịch §1.9; người dự phòng theo vai trò §2.1; dùng tuần dự phòng | PO |
| R-17 | Báo cáo đồ án dồn cuối, không kịp | TB | C | Bản nháp chương của giai đoạn chưa xong khi kết thúc giai đoạn | Viết dần §1.10 | BA |
| R-18 | Ước tính giá thấp hơn chi phí thực (trừ kịch số đã giữ) | TB | T | > 5% job có CAPTURE = HOLD | Chỉnh giới hạn đầu ra trong seed theo số liệu PoC | Backend & AI |
| R-19 | Closed beta ít người tham gia | TB | TB | T22 chưa đủ 10 email đồng ý tham gia | Mời từ T20; chương mẫu sẵn; nhờ giảng viên giới thiệu | PO |
| R-07 | LLM chia shot kém / sai schema / vượt context | TB | T | > 20% ranh giới bị validator sửa; job lỗi schema > 5% | Validator tất định; retry có phản hồi; xử lý theo chương | Backend & AI |
| R-20 | Sổ cái ví sai lệch | T | C | Reconciler báo lệch ≠ 0 | Property-based test; reconciler hằng ngày; cảnh báo P1 | Backend & AI |
| R-21 | Provider ảnh từ chối cảnh trong văn học (bạo lực, nghèo đói, tình dục) | C | TB | `EVAL-refusal-rate` > 5% ở P0; > 10% job ảnh `CONTENT_POLICY` một tuần khi beta | Hướng dẫn tả gián tiếp trong prompt storyboard; người dùng sửa brief (BR-18); tính tỷ lệ từ chối vào tiêu chí chọn provider | Backend & AI |
| R-22 | Phụ thuộc một nhà cung cấp (Google) cho cả LLM và ảnh: sự cố, đổi giá, đổi chính sách nội dung ảnh hưởng hai bước cùng lúc | T | C | Gemini lỗi liên tục > 30 phút trong giờ demo; giá Gemini tăng làm `EVAL-cost-per-minute` > $0,15 | Port + fixture ghi lại để đổi provider bằng adapter (AG-02); fallback giữa các mô hình Gemini (QĐ-124); đặt giới hạn chi tiêu trên console Google | Backend & AI |
| R-23 | TTS tự host không đạt chất lượng tiếng Việt, chậm, hoặc thiếu GPU | TB | C | Không model nào đạt WER hiệu chỉnh ≤ 5% hoặc `BENCH-tts` > 0,4× ở P0; máy GPU không thuê được khi demo/beta | Quy tắc dự phòng §1.5; chọn model nhẹ hơn; PO có thể đưa Vbee AIVoice vào MVP (thêm `VbeeTtsAdapter`, ≈ 1 tn, lấy từ thứ tự cắt giảm) | Backend & AI |

## 6. Quyết định đã chốt và câu hỏi còn mở

Mọi câu hỏi của 4 vòng chốt phạm vi và kế hoạch đã được trả lời và ghi ở [sổ quyết định](../quyet-dinh.md). Các câu hỏi mở của bản trước (giá thao tác LLM, render Free, ví trong dự án chung, cộng tác thời gian thực, ngôn ngữ thuyết minh, đọc tiêu đề chương, đa giọng, ngưỡng WER, ký hiệu trình bày, SSO, thư viện nhạc) được giải quyết ở QĐ-31, QĐ-36, QĐ-42, QĐ-04, QĐ-60, QĐ-60, QĐ-60, QĐ-54, QĐ-56, QĐ-20..24, QĐ-58.

**Còn mở (chờ thông tin bên ngoài):**

| # | Câu hỏi | Ai trả lời | Hạn |
|---|---|---|---|
| 1 | Tài liệu tích hợp SSO Vbee: endpoint, có OIDC không, cách cấp `client_id`/`client_secret`, back-channel logout, người liên hệ | PO liên hệ đội Vbee | Hết tháng thứ 2 |
| 2 | Kết quả PoC: provider ảnh và TTS được chọn, đơn giá thực để điền `price_rules`, mật độ ảnh và chi phí/phút video (QĐ-112) | Nhóm | Cuối P0 |
| 3 | Nội dung chính thức của thông báo đồng ý xử lý dữ liệu (phiên bản 1) | PO soạn, nhóm duyệt | Trước closed beta |
