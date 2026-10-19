# 07 — Yêu cầu phi chức năng

> Phân loại theo ISO/IEC 25010. Mỗi yêu cầu có cách đo kiểm tra được.

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
| NFR-PERF-09 | Sinh và kiểm chứng thuyết minh 1 chương 10.000 ký tự (≈ 12 phút audio): p90 ≤ 5 phút | Thống kê job |
| NFR-PERF-10 | Render 1080p: thời gian ≤ 1× thời lượng video (10 phút video render ≤ 10 phút) trên worker tham chiếu 8 vCPU | Benchmark |
| NFR-PERF-11 | Preview trong trình chỉnh sửa: bắt đầu phát ≤ 2 s; lệch hình–tiếng–phụ đề ≤ 100 ms | Đo thủ công + test tự động |
| NFR-PERF-12 | Trình chỉnh sửa mượt với timeline 30 phút / 300 item: kéo thả, scrub ở ≥ 50 fps; thao tác phản hồi ≤ 100 ms; autosave không chặn UI | Đo trên máy tham chiếu |
| NFR-PERF-13 | Bản xem trước khớp bản xuất: khác biệt khung hình ≤ 1 frame tại mọi ranh giới clip | Test so sánh khung hình tự động |

## 1b. Toàn vẹn nội dung (Verbatim)

| Mã | Yêu cầu | Cách đo |
|---|---|---|
| NFR-INT-01 | **Độ phủ văn bản = 100%** cho mọi render: tổng ký tự các đoạn nguồn bằng độ dài chương, và `concat` các đoạn nguồn bằng văn bản chương (so sánh byte) | Kiểm tra tự động trước render; test property-based cho `CoverageValidator` với 10.000 phân đoạn ngẫu nhiên |
| NFR-INT-02 | Không có đường code nào ghi đầu ra LLM vào `chapters.content` / `source_texts` / văn bản TTS | Review kiến trúc; test kiến trúc (ArchUnit-style) cấm import module LLM trong repository chương |
| NFR-INT-03 | WER thuyết minh trung bình ≤ 3% trên golden set tiếng Việt và tiếng Anh; không shot nào > 10% mà không có người duyệt | Bộ eval TTS trong CI khi đổi provider hoặc giọng |
| NFR-INT-04 | Phụ đề khớp nguyên văn 100% (so sánh ký tự sau khi bỏ ngắt dòng) | Test tự động trên file SRT/VTT |
| NFR-INT-05 | Văn bản giữ nguyên qua import với các định dạng hỗ trợ (round-trip .txt/.md giống byte sau NFC) | Test tự động |
| NFR-INT-06 | Mỗi render lưu `timeline_snapshot` và hash các đoạn nguồn để kiểm toán lại sau này | Kiểm tra dữ liệu |

## 2. Khả năng mở rộng

| Mã | Yêu cầu |
|---|---|
| NFR-SCAL-01 | API stateless, scale ngang; phiên lưu trong DB hoặc Redis |
| NFR-SCAL-02 | Worker scale theo độ dài queue, riêng từng queue `orchestrator` / `llm` / `image` / `tts` / `align` / `audio-gen` / `media-proc` / `render` / `export` (05 §3, §10) |
| NFR-SCAL-03 | Giới hạn đồng thời theo provider (tôn trọng rate limit) và theo người dùng (tối đa 8 job ảnh, 8 job TTS và 1 job render đồng thời) |
| NFR-SCAL-04 | Mục tiêu năm đầu: 10.000 MAU, 500 người dùng đồng thời, 200.000 job ảnh/ngày |

## 3. Độ tin cậy & sẵn sàng

| Mã | Yêu cầu |
|---|---|
| NFR-REL-01 | Uptime API ≥ 99,5%/tháng (không tính provider AI) |
| NFR-REL-02 | Không mất job: outbox + BullMQ persistence; reconciler giải phóng job treo (§4 của 05) |
| NFR-REL-03 | **Đúng credit:** tổng ledger = số dư; reconciler hằng ngày báo lệch bằng 0. Lệch thì cảnh báo P1 |
| NFR-REL-04 | Retry provider: tối đa 3 lần, backoff 2s/8s/30s + jitter; circuit breaker mở khi tỷ lệ lỗi > 50% trong 1 phút |
| NFR-REL-05 | Backup PostgreSQL: PITR 7 ngày; snapshot hằng ngày giữ 30 ngày. RPO ≤ 5 phút, RTO ≤ 2 giờ |
| NFR-REL-06 | Object storage bật versioning cho bucket media |

## 4. Bảo mật

| Mã | Yêu cầu |
|---|---|
| NFR-SEC-01 | TLS 1.2+ mọi kết nối; HSTS |
| NFR-SEC-02 | Xác thực qua SSO có sẵn (OIDC Authorization Code + PKCE, `state`, `nonce`); ID token và logout token được xác thực theo JWKS; ứng dụng **không lưu mật khẩu**; refresh token SSO mã hóa khi lưu; cookie phiên `HttpOnly; Secure; SameSite=Lax`; chống CSRF bằng double-submit token cho mutation; `returnTo` chỉ cho phép đường dẫn nội bộ |
| NFR-SEC-02b | Thời gian sống phiên ứng dụng ≤ 12 giờ không hoạt động; tài khoản bị khóa ở SSO mất quyền truy cập trong ≤ 15 phút (chu kỳ refresh) hoặc ngay lập tức nếu có back-channel logout |
| NFR-SEC-03 | Kiểm tra quyền cấp đối tượng cho **mọi** endpoint `/projects/{pid}/**` (chống IDOR); test tự động cho ma trận quyền |
| NFR-SEC-04 | Token mời: 256-bit ngẫu nhiên, DB chỉ lưu SHA-256; thu hồi có hiệu lực ngay |
| NFR-SEC-05 | Media private; presigned URL ≤ 15 phút |
| NFR-SEC-06 | Secret ở secret manager; không log prompt có PII ở mức INFO; key provider **không bao giờ** ra client |
| NFR-SEC-07 | Webhook xác thực chữ ký; chống replay theo timestamp (≤ 5 phút) và event id |
| NFR-SEC-08 | Phòng prompt injection cho Director: whitelist tool theo quyền; tool tốn phí cần người dùng xác nhận; văn bản truyện được bọc như dữ liệu, không phải chỉ dẫn |
| NFR-SEC-09 | Kiểm tra bảo mật theo OWASP ASVS L2 trước khi go-live; quét phụ thuộc (Dependabot, Trivy) trong CI |
| NFR-SEC-10 | Upload: kiểm MIME thật, giới hạn kích thước, quét malware, bỏ metadata EXIF |

## 5. Quyền riêng tư & tuân thủ

| Mã | Yêu cầu |
|---|---|
| NFR-PRV-01 | Tuân thủ Nghị định 13/2023/NĐ-CP: thông báo xử lý dữ liệu, có cơ chế xóa dữ liệu |
| NFR-PRV-02 | Chỉ dùng provider AI cam kết **không huấn luyện** trên dữ liệu API của khách hàng; ghi rõ trong chính sách |
| NFR-PRV-03 | Người dùng tải xuống toàn bộ dữ liệu dự án (ZIP) — quyền di chuyển dữ liệu |
| NFR-PRV-04 | Audit log cho hành động Admin và thay đổi credit thủ công, giữ 2 năm |

## 6. Khả dụng (Usability) & tiếp cận

| Mã | Yêu cầu |
|---|---|
| NFR-USA-01 | Mọi thao tác tốn credit hiển thị giá **trước** khi xác nhận; thao tác hàng loạt hiển thị tổng |
| NFR-USA-02 | Trạng thái job hiển thị tại chỗ (shot, cảnh, tài sản) và trong trung tâm thông báo |
| NFR-USA-03 | Thao tác phá hủy (xóa chương, xóa dự án, xóa vĩnh viễn tài sản) có xác nhận; xóa chương có Undo trong 10 s |
| NFR-USA-04 | Giao diện đạt WCAG 2.1 AA: điều hướng bàn phím trong Studio, tương phản, nhãn ARIA |
| NFR-USA-05 | Đa ngôn ngữ giao diện (i18n), mặc định vi và en; nội dung truyện hỗ trợ Unicode đầy đủ, gồm tiếng Việt |
| NFR-USA-06 | Người mới hoàn thành chương đầu tiên bằng Director mà không cần đọc tài liệu (kiểm thử với 5 người dùng) |

## 7. Khả năng bảo trì & quan sát

| Mã | Yêu cầu |
|---|---|
| NFR-MNT-01 | Test coverage ≥ 80% cho module `billing` và `authz`; ≥ 60% toàn hệ thống |
| NFR-MNT-02 | Provider AI có adapter **mock** chạy offline cho dev và CI (không cần key) |
| NFR-MNT-03 | Tracing OpenTelemetry xuyên API → queue → worker → provider; correlation id = jobId |
| NFR-MNT-04 | Dashboard: độ dài queue, thời gian job, tỷ lệ lỗi theo provider, chi phí AI theo giờ, biên lợi nhuận credit, độ trễ outbox relay, số job treo bị reconciler xử lý |
| NFR-MNT-07 | Luật khóa thuyết minh (BR-24) nằm trong một package dùng chung client/server (`@studio/timeline-rules`), có bộ test riêng chạy ở CI (ADR-16) |
| NFR-MNT-08 | Môi trường local chạy được toàn bộ luồng 6 bước không cần mạng ngoài: OIDC giả lập (Keycloak dev realm), AI mock, MinIO, Stripe CLI |
| NFR-MNT-05 | Migration DB có phiên bản và có thể rollback; zero-downtime (expand/contract) |
| NFR-MNT-06 | Prompt template quản lý bằng file có phiên bản; có bộ eval hồi quy (golden set 30 chương mẫu) khi đổi prompt hoặc mô hình |

## 8. Tương thích

| Mã | Yêu cầu |
|---|---|
| NFR-CMP-01 | Trình duyệt: 2 phiên bản mới nhất của Chrome, Edge, Firefox, Safari |
| NFR-CMP-02 | Video xuất H.264/AAC MP4, tương thích TikTok, Reels, YouTube |
| NFR-CMP-03 | Âm thanh đầu ra AAC 48 kHz stereo, loudness −14 LUFS ±1, true peak ≤ −1 dBTP |
