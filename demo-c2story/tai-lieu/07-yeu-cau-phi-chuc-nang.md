# 07 — Yêu cầu phi chức năng

> Phân loại theo ISO/IEC 25010. Mỗi yêu cầu có cách đo kiểm tra được. Mục tiêu đặt cho **closed beta 10–20 người** của đồ án (QĐ-71); các số liệu quy mô sản phẩm thật ghi "(sau MVP)".

## 1. Hiệu năng

| Mã | Yêu cầu | Cách đo |
|---|---|---|
| NFR-PERF-01 | API đọc (không gọi AI): p95 ≤ 300 ms, p99 ≤ 800 ms | APM, tải 200 RPS |
| NFR-PERF-02 | API tạo job trả `202` trong p95 ≤ 500 ms | APM |
| NFR-PERF-03 | Sự kiện job đến client ≤ 2 s sau khi trạng thái đổi | Đo end-to-end |
| NFR-PERF-04 | Sinh 1 ảnh shot: p90 ≤ 60 s (phụ thuộc provider; tính từ lúc job vào hàng đợi) | Thống kê job |
| NFR-PERF-05 | Storyboard 1 chương 10.000 ký tự: p90 ≤ 90 s | Thống kê job |
| NFR-PERF-06 | Trình soạn thảo Workspace mượt với dự án 300.000 ký tự / 50 chương (gõ không trễ > 50 ms) | Đo trên máy tham chiếu |
| NFR-PERF-07 | Restructure 50 chương hoàn tất ≤ 2 s | Benchmark |
| NFR-PERF-08 | "Sinh tư liệu" một chương 10.000 ký tự (≈ 10 ảnh + 12 phút audio): p90 ≤ 8 phút | Thống kê job |
| NFR-PERF-09 | Sinh thuyết minh 1 chương 10.000 ký tự (≈ 12 phút audio), gồm timestamp từng từ: p90 ≤ 5 phút | Thống kê job |
| NFR-PERF-10 | MVP: 1 phút video 720p render ≤ 2 phút trên máy staging thật (đo ở P0, QĐ-98). Sau MVP: render 1080p ≤ 1× thời lượng video trên worker tham chiếu 8 vCPU | `BENCH-render` |
| NFR-PERF-11 | Preview trong trình chỉnh sửa: bắt đầu phát ≤ 2 s; lệch hình–tiếng–phụ đề ≤ 100 ms | Đo thủ công + test tự động |
| NFR-PERF-12 | Trình chỉnh sửa mượt với timeline 30 phút / 300 item: kéo thả, scrub ở ≥ 50 fps; thao tác phản hồi ≤ 100 ms; autosave không chặn UI | Đo trên máy tham chiếu |
| NFR-PERF-13 | Bản xem trước khớp bản xuất: khác biệt khung hình ≤ 1 frame tại mọi ranh giới clip | Test so sánh khung hình tự động |

## 1b. Toàn vẹn nội dung (Verbatim)

| Mã | Yêu cầu | Cách đo |
|---|---|---|
| NFR-INT-01 | **Độ phủ văn bản = 100%** cho mọi render: tổng ký tự các đoạn nguồn bằng độ dài chương, và `concat` các đoạn nguồn bằng văn bản chương (so sánh byte) | Kiểm tra tự động trước render; test property-based cho `CoverageValidator` với 10.000 phân đoạn ngẫu nhiên |
| NFR-INT-02 | Không có đường code nào ghi đầu ra LLM vào `chapters.content` / `source_texts` / văn bản TTS | Review kiến trúc; test kiến trúc (ArchUnit-style) cấm import module LLM trong repository chương |
| NFR-INT-03 | WER hiệu chỉnh của thuyết minh (WER theo âm tiết trừ WER nền của ASR, QĐ-111) trung bình ≤ 3% trên golden set tiếng Việt và tiếng Anh với provider và giọng đã chọn. Bảo đảm ở **khâu chọn provider** (P0), không kiểm tra từng shot lúc chạy trong MVP (QĐ-54) | `EVAL-wer-golden` ở P0 và mỗi khi đổi provider, giọng hoặc quy tắc chuẩn hóa |
| NFR-INT-04 | Phụ đề khớp nguyên văn 100%, kể cả ký hiệu trình bày (so sánh ký tự sau khi bỏ ngắt dòng; trừ dòng phân cách không có phụ đề, BR-22) | Test tự động trên file SRT/VTT |
| NFR-INT-05 | Văn bản giữ nguyên qua import với các định dạng hỗ trợ (round-trip .txt/.md giống byte sau NFC) | Test tự động |
| NFR-INT-06 | Mỗi render lưu `timeline_snapshot` và hash các đoạn nguồn để kiểm toán lại sau này | Kiểm tra dữ liệu |

## 2. Khả năng mở rộng

| Mã | Yêu cầu |
|---|---|
| NFR-SCAL-01 | API stateless, scale ngang; phiên lưu trong DB hoặc Redis |
| NFR-SCAL-02 | Worker scale theo độ dài queue, riêng từng queue `orchestrator` / `llm` / `image` / `tts` / `align` / `media-proc` / `render` / `export` (05 §3, §10) |
| NFR-SCAL-03 | Giới hạn đồng thời theo provider (rate limiter của BullMQ cho từng queue) và theo người dùng bằng semaphore Redis (BR-32, ADR-28): tối đa 8 job ảnh, 8 job TTS, 1 job render đồng thời; ≤ 30 yêu cầu LLM/phút |
| NFR-SCAL-04 | Closed beta: 20 người dùng, 5 người đồng thời. Kiến trúc không chặn scale ngang tới 10.000 MAU, 500 người dùng đồng thời (sau MVP) |

## 3. Độ tin cậy & sẵn sàng

| Mã | Yêu cầu |
|---|---|
| NFR-REL-01 | Trong 3 tuần closed beta: dịch vụ chạy liên tục, sự cố được khôi phục trong ngày làm việc. Uptime API ≥ 99,5%/tháng (sau MVP, không tính provider AI) |
| NFR-REL-02 | Không mất job: BullMQ persistence + reconciler đẩy lại job `QUEUED` bị sót và giải phóng job treo (MVP, ADR-23); outbox sau MVP (05 §6.1) |
| NFR-REL-03 | **Đúng tiền:** tổng sổ cái = số dư ví; mỗi job có HOLD và đúng một CAPTURE/RELEASE; số trừ ≤ số giữ; reconciler hằng ngày báo lệch bằng 0. Lệch thì cảnh báo P1 |
| NFR-REL-04 | Retry provider: tối đa 3 lần, backoff 2s/8s/30s + jitter; circuit breaker mở khi tỷ lệ lỗi > 50% trong 1 phút. Timeout mỗi lời gọi (QĐ-126): LLM 120 s, ảnh 90 s, TTS ≥ 2× thời lượng audio dự kiến (tối thiểu 30 s), nghe thử 15 s; quá hạn tính là lỗi tạm thời |
| NFR-REL-05 | Backup PostgreSQL: snapshot hằng ngày giữ 7 ngày trong closed beta. PITR, RPO ≤ 5 phút, RTO ≤ 2 giờ (sau MVP) |
| NFR-REL-06 | Object storage bật versioning cho bucket media |

## 4. Bảo mật

| Mã | Yêu cầu |
|---|---|
| NFR-SEC-01 | TLS 1.2+ mọi kết nối; HSTS |
| NFR-SEC-02 | Xác thực qua SSO có sẵn (OIDC Authorization Code + PKCE, `state`, `nonce`); ID token và logout token được xác thực theo JWKS; ứng dụng **không lưu mật khẩu**; refresh token SSO mã hóa khi lưu; cookie phiên `HttpOnly; Secure; SameSite=Lax`; chống CSRF bằng double-submit token cho mutation; `returnTo` chỉ cho phép đường dẫn nội bộ |
| NFR-SEC-02b | Thời gian sống phiên ứng dụng ≤ 12 giờ không hoạt động; tài khoản bị khóa ở SSO mất quyền truy cập trong ≤ 15 phút (chu kỳ refresh); ngay lập tức nếu có back-channel logout (sau MVP) |
| NFR-SEC-03 | Kiểm tra quyền cấp đối tượng cho **mọi** endpoint `/projects/{pid}/**` (chống IDOR); test tự động cho ma trận quyền |
| NFR-SEC-04 | Token mời: 256-bit ngẫu nhiên, DB chỉ lưu SHA-256; thu hồi có hiệu lực ngay |
| NFR-SEC-05 | Media private; presigned URL ≤ 15 phút |
| NFR-SEC-06 | Secret ở secret manager; không log prompt có PII ở mức INFO; key provider **không bao giờ** ra client |
| NFR-SEC-07 | Webhook xác thực chữ ký; chống replay theo timestamp (≤ 5 phút) và event id |
| NFR-SEC-08 | Phòng prompt injection cho Director: whitelist tool theo quyền; tool tốn phí cần người dùng xác nhận; văn bản truyện được bọc như dữ liệu, không phải chỉ dẫn |
| NFR-SEC-09 | Quét phụ thuộc (Dependabot, Trivy) trong CI và tự rà OWASP Top 10 trước closed beta; kiểm tra theo OWASP ASVS L2 trước khi mở rộng (sau MVP) |
| NFR-SEC-10 | Upload: kiểm MIME thật, giới hạn kích thước, quét malware, bỏ metadata EXIF |
| NFR-SEC-11 | Chống lạm dụng tiền dùng thử: chỉ tài khoản trong danh sách mời được tạo hồ sơ (BR-30); trần chi tiêu AI toàn hệ thống mỗi ngày (BR-29) |

## 5. Quyền riêng tư & tuân thủ

| Mã | Yêu cầu |
|---|---|
| NFR-PRV-01 | Tuân thủ Nghị định 13/2023/NĐ-CP: màn hình đồng ý ở lần đăng nhập đầu, lưu thời điểm và phiên bản đồng ý (BR-31); Admin xóa dữ liệu theo yêu cầu; xóa toàn bộ dữ liệu beta sau ngày bảo vệ |
| NFR-PRV-02 | Chỉ dùng provider AI cam kết **không huấn luyện** trên dữ liệu API của khách hàng; ghi rõ trong chính sách |
| NFR-PRV-03 | Người dùng tải xuống toàn bộ dữ liệu dự án (ZIP), quyền di chuyển dữ liệu (sau MVP) |
| NFR-PRV-04 | Audit log cho hành động Admin (danh sách mời, cấu hình, điều chỉnh số dư), giữ đến khi xóa dữ liệu đồ án |

## 6. Khả dụng (Usability) & tiếp cận

| Mã | Yêu cầu |
|---|---|
| NFR-USA-01 | Mọi thao tác tốn phí hiển thị giá ước tính tối đa **trước** khi xác nhận; thao tác hàng loạt hiển thị tổng; sau khi xong hiện số thực trừ và số hoàn |
| NFR-USA-02 | Trạng thái job hiển thị tại chỗ (shot, cảnh, tài sản) và trong trung tâm thông báo |
| NFR-USA-03 | Thao tác phá hủy (xóa chương, xóa dự án, xóa vĩnh viễn tài sản) có xác nhận; xóa chương có Undo trong 10 s |
| NFR-USA-04 | Giao diện đạt WCAG 2.1 AA: điều hướng bàn phím trong Studio, tương phản, nhãn ARIA |
| NFR-USA-05 | Đa ngôn ngữ giao diện (i18n), mặc định vi và en; nội dung truyện hỗ trợ Unicode đầy đủ, gồm tiếng Việt |
| NFR-USA-06 | Người dùng beta hoàn thành video chương đầu tiên mà không cần hướng dẫn trực tiếp (kiểm thử với 5 người dùng; đo bằng phiếu khảo sát closed beta) |

## 7. Khả năng bảo trì & quan sát

| Mã | Yêu cầu |
|---|---|
| NFR-MNT-01 | Test coverage ≥ 80% cho module `billing` và `authz` và package `@studio/timeline-rules`; ≥ 60% toàn hệ thống |
| NFR-MNT-09 | Nền tảng kiểm thử theo 09 §2.3: integration test chạy trên Testcontainers (Postgres, Redis, MinIO), không mock DB; property-based test bằng fast-check; OpenAPI viết trước so trong CI |
| NFR-MNT-02 | Provider AI có adapter **mock** chạy offline cho dev và CI (không cần key). Provider thật chỉ gọi khi demo và trong test E2E hằng tuần (QĐ-40) |
| NFR-MNT-03 | Tracing OpenTelemetry xuyên API → queue → worker → provider; correlation id = jobId |
| NFR-MNT-04 | Dashboard: độ dài queue, thời gian job, tỷ lệ lỗi theo provider, chi phí AI theo giờ, chi tiêu so với trần ngày, tỷ lệ job bị trừ kịch số đã giữ, độ trễ outbox relay, số job treo bị reconciler xử lý |
| NFR-MNT-07 | Luật khóa thuyết minh (BR-24) nằm trong một package dùng chung client/server (`@studio/timeline-rules`), có bộ test riêng chạy ở CI (ADR-16) |
| NFR-MNT-08 | Môi trường local chạy được toàn bộ luồng 6 bước không cần mạng ngoài: Keycloak dev realm, AI mock, MinIO, Stripe CLI (sandbox) |
| NFR-MNT-05 | Migration DB có phiên bản và có thể rollback; zero-downtime (expand/contract) |
| NFR-MNT-06 | Prompt template quản lý bằng file có phiên bản; có bộ eval hồi quy khi đổi prompt hoặc mô hình (`EVAL-consistency`, `EVAL-refusal-rate`, `EVAL-asset-extraction`, `EVAL-wer-golden`, `EVAL-alignment`, `EVAL-segmenter-golden`). Golden set: 5–10 chương tác phẩm hết thời hạn bảo hộ (tiếng Việt), Project Gutenberg (tiếng Anh) và 1–2 chương nhóm tự viết có tên riêng, số, từ mượn (QĐ-70) |

## 8. Tương thích

| Mã | Yêu cầu |
|---|---|
| NFR-CMP-01 | Trình duyệt: 2 phiên bản mới nhất của Chrome, Edge, Firefox, Safari |
| NFR-CMP-02 | Video xuất H.264/AAC MP4, tương thích TikTok, Reels, YouTube |
| NFR-CMP-03 | Âm thanh đầu ra AAC 48 kHz stereo, loudness −14 LUFS ±1, true peak ≤ −1 dBTP |

## 9. Chi phí

| Mã | Yêu cầu | Cách đo |
|---|---|---|
| NFR-COST-01 | Chi phí AI không vượt ngân sách do PO trả: P0 ≤ $200; P1–P3 ≤ $50/tháng; UAT ≤ $200 (QĐ-40) | Báo cáo tổng `ai_usage_records` theo tuần |
| NFR-COST-02 | Trần chi tiêu AI toàn hệ thống mỗi ngày $10 trong closed beta, chặn ở thời điểm tạo job (BR-29) | `IT-daily-budget-cap` |
| NFR-COST-03 | Mỗi job ghi chi phí thực (`ai_usage_records.cost_usd`) để tính giá ×110% và đối soát | `REC-ledger` |
