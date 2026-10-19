# 09 — Kế hoạch phát triển & ma trận truy vết

## 1. Lộ trình phát hành

| Giai đoạn | Thời lượng (ước tính) | Mục tiêu | Phạm vi |
|---|---|---|---|
| **P0 — Nền tảng & PoC AI** | 3 tuần | Chọn provider bằng số liệu | Repo, CI/CD (lint kiến trúc), docker-compose (Keycloak dev realm, MinIO, ClamAV), lớp `platform` (jobs + HOLD + outbox, idempotency, realtime SSE, audit), Scheduler, **tích hợp SSO có sẵn (OIDC client, phiên BFF, JIT hồ sơ; khoảng 3–4 ngày công, cần môi trường SSO test và client_id)**, schema lõi, AI Gateway + adapter mock. PoC: (1) 2–3 provider ảnh về độ nhất quán nhân vật; (2) **2–3 provider TTS tiếng Việt về WER, độ tự nhiên, giá**; (3) aligner tiếng Việt |
| **P1 — Nhập truyện → tư liệu ảnh** | 6 tuần | Bước 1–3 và phần ảnh của bước 4 | M01, M02 (không realtime), M03, M04 (Story Assets, Art Direction), M05: storyboard tự động **kèm tách câu + CoverageValidator**, sinh/sửa ảnh, media bin; M09 (credit + Stripe), M10 (giá, job monitor) |
| **P2 — Thuyết minh nguyên văn** | 3 tuần | Hoàn tất bước 4 | M05: narration settings, TTS nguyên văn, alignment + WER, từ điển phát âm, nút "Sinh tư liệu" gộp ảnh + thuyết minh |
| **P3 — Trình chỉnh sửa & xuất video** | 7 tuần | Bước 5–6 | M06: timeline nhiều track (video, thuyết minh khóa, phụ đề, nhạc, SFX, overlay), Ken Burns, chuyển cảnh, tinh chỉnh màu, thư viện nhạc & SFX có license, trộn âm/ducking/loudness, undo/redo, autosave, preview, render FFmpeg từ timeline, tải xuống |
| **P4 — Director & cộng tác** | 5 tuần | Tự động hóa và làm việc nhóm | M07 (chat + auto đến bản nháp timeline), realtime SSE, invite và xung đột, Timeline truyện, Relationships, Visual Rules, Archives |
| **P5 — Hoàn thiện** | 3 tuần | Sẵn sàng thương mại | M08 thư viện, Find & replace, versions, AI nhạc/SFX + gợi ý SFX (C), đa giọng nhân vật, chia video theo thời lượng, báo cáo admin, kiểm thử bảo mật ASVS, a11y |

Tổng cộng khoảng 27 tuần với đội đề xuất: 1 PO/BA, 1 designer, 3 full-stack (1 người chuyên trình chỉnh sửa timeline), 1 backend/AI (audio/media), 1 QA, 0,5 DevOps. So với bản trước: bỏ phần sách tiết kiệm khoảng 2 tuần, trình chỉnh sửa timeline thêm khoảng 5 tuần.

## 2. Tiêu chí hoàn thành (Definition of Done)

- Đáp ứng mọi acceptance criteria của user story, có test tự động (unit + integration). Luồng tiền và quyền có test e2e.
- Đã cập nhật OpenAPI; endpoint mới có test ma trận quyền.
- Job mới có: giá trong `price_rules`, mock adapter, metric, ghi `ai_usage_records`.
- Review code bởi ít nhất 1 người; không còn cảnh báo bảo mật mức High.
- Đã cập nhật i18n (vi, en).

## 3. User story & tiêu chí chấp nhận mẫu (Gherkin)

### US-BOK-09 Sinh ảnh shot
```gherkin
Feature: Sinh ảnh cho shot
  Scenario: Đủ credit, sinh thành công
    Given tôi là Editor của dự án "P" và có 5 credit khả dụng
    And shot "S1" có brief và gắn nhân vật "Yên Vân" có ảnh tham chiếu
    When tôi bấm "Generate" trên "S1"
    Then tôi thấy trạng thái "generating" trong vòng 2 giây
    And số dư khả dụng của tôi là 4 và đang giữ 1
    When job hoàn tất thành công
    Then "S1" hiển thị ảnh mới là phiên bản hiện hành
    And số dư khả dụng là 4 và đang giữ 0

  Scenario: Provider lỗi, hoàn credit
    Given tôi có 5 credit
    When tôi sinh ảnh "S1" và provider lỗi sau 3 lần thử
    Then "S1" hiển thị nút "Retry"
    And số dư khả dụng của tôi là 5
```

### US-PRJ-11 Xung đột khi lưu chương
```gherkin
  Scenario: Hai người cùng sửa
    Given A và B cùng mở chương "C1" ở phiên bản 3
    When B lưu "C1"
    And A lưu "C1"
    Then A thấy hộp thoại xung đột ghi tên B là người sửa cuối
    When A chọn "Lưu bản của tôi thành nháp"
    Then có một Archive nguồn "CONFLICT" chứa văn bản của A
    And editor của A tải phiên bản 4
```

### US-DIR-05 Điểm duyệt của Director
```gherkin
  Scenario: Không tiêu credit khi chưa duyệt cast
    Given dự án có style và 3 chương, chưa có Story Assets
    When tôi bật Director tự động
    Then Director dừng ở bước "cast" với trạng thái "AWAITING_INPUT"
    And không có job sinh ảnh nào được tạo
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

### US-NAR-02 Thuyết minh nguyên văn
```gherkin
Feature: Audio đọc đúng văn bản gốc
  Scenario: Văn bản TTS lấy từ chương
    Given shot "S3" có đoạn nguồn "Bỗng, âm báo tin nhắn của điện thoại Yên Vân reo lên."
    When tôi sinh thuyết minh cho "S3"
    Then văn bản gửi tới TTS sau khi bỏ thẻ SSML giống hệt đoạn nguồn
    And phụ đề của "S3" là "Bỗng, âm báo tin nhắn của điện thoại Yên Vân reo lên."

  Scenario: TTS đọc thiếu từ
    Given ngưỡng WER là 3%
    When audio của "S3" bị STT nhận ra thiếu cụm "tin nhắn"
    Then thuyết minh "S3" có trạng thái "NEEDS_REVIEW"
    And cụm "tin nhắn" được tô đỏ
    And nút "Xuất video" bị khóa cho đến khi tôi sinh lại hoặc chấp nhận thủ công

  Scenario: Director từ chối tóm tắt
    When tôi nhắn Director "tóm tắt chương 1 cho video ngắn hơn"
    Then Director trả lời rằng thuyết minh luôn đọc nguyên văn
    And văn bản chương 1 không thay đổi
```

### US-EDT-04 Track thuyết minh bị khóa
```gherkin
Feature: Trình chỉnh sửa không làm mất lời đọc
  Scenario: Không xóa được clip thuyết minh
    Given timeline chương "C1" có 8 clip thuyết minh
    When tôi chọn clip thuyết minh của shot 3 và nhấn Delete
    Then clip vẫn còn trên timeline
    And tôi thấy thông báo "Thuyết minh nguyên văn không thể xóa hoặc cắt"

  Scenario: Thêm SFX và nhạc nền
    Given timeline chương "C1" đã sẵn sàng
    When tôi kéo SFX "Pháo hoa" vào track SFX tại 01:42
    And kéo nhạc "Calm piano" vào track Nhạc nền từ 00:00 với ducking -12 dB
    Then khi xem trước, nhạc nhỏ lại trong lúc thuyết minh đọc
    And độ phủ văn bản vẫn là 100%
```

### US-MAN-05 Chia chương nguyên tử
```gherkin
  Scenario: Một thao tác lỗi thì không thay đổi gì
    Given dự án có chương C1 (v2) và C2 (v5)
    When tôi gửi restructure gồm SPLIT C1 với ifMatch 2 và MERGE C2 với ifMatch 4
    Then tôi nhận lỗi 409
    And danh sách chương và phiên bản không thay đổi
```

## 4. Ma trận truy vết yêu cầu (RTM)

| Mục tiêu KD | Phân hệ | Yêu cầu chức năng | Use case | Sơ đồ | Test chính |
|---|---|---|---|---|---|
| BO-01 | M02 | FR-PRJ-02..03 | UC-02.02 | seq-import-chia-chuong | IT-PRJ-import |
| BO-04 | M02 | FR-PRJ-08..11 | UC-02.06, UC-02.08, UC-02.10 | seq-cong-tac-xung-dot | E2E-collab-conflict |
| BO-01 | M03 | FR-MAN-03..06 | UC-03.03..09 | seq-import-chia-chuong, state-chapter-media | IT-restructure-atomic |
| — | M03 | FR-MAN-08 | UC-03.11, UC-03.12 | — | IT-archive-immutable |
| BO-02 | M04 | FR-WLD-01..07 | UC-04.01..03 | c4-component-ai | IT-analyze-assets, EVAL-consistency |
| BO-02 | M04 | FR-WLD-10 | UC-04.10 | — | UT-prompt-compiler-order |
| BO-01, BO-03 | M05 | FR-BOK-01..08 (gồm 01a, 01b) | UC-05.01..06 | seq-storyboard-sinh-anh, act-phu-kin-van-ban | IT-storyboard-schema, PBT-coverage-validator |
| BO-02, BO-05 | M05 | FR-BOK-09..10 | UC-05.09, UC-05.10 | seq-storyboard-sinh-anh, act-giu-tru-credit, state-job | E2E-shot-image, IT-credit-refund |
| BO-01, BO-04 | M05 | FR-MED-01..05 | UC-05.07 | seq-sinh-tu-lieu, state-chapter-media | E2E-generate-media-chapter, IT-quote-total |
| BO-03, BO-04 | M05 | FR-NAR-01..09 | UC-05.13 | seq-thuyet-minh-nguyen-van, state-narration-render | IT-tts-input-equals-source, EVAL-wer-golden, E2E-needs-review |
| BO-01 | M06 | FR-EDT-01..20 | UC-06.01..15 | seq-chinh-sua-xuat-video | UT-narration-track-locked, IT-timeline-autosave, IT-media-sync, E2E-editor-sfx-music |
| BO-03, BO-06 | M06 | FR-EDT-21..26 | UC-06.16, UC-06.17 | seq-chinh-sua-xuat-video | IT-render-readiness, IT-subtitle-verbatim, BENCH-render |
| BO-01 | M07 | FR-DIR-04..07 | UC-07.02 | seq-director, state-director-plan | E2E-director-draft-timeline, US-DIR-05 |
| — | M07 | FR-DIR-01..03 | UC-07.01 | seq-director | IT-tool-authz, SEC-prompt-injection |
| BO-03, BO-05 | M09 | FR-BIL-01..09 | UC-09.02, UC-09.03 | seq-thanh-toan, state-subscription | IT-webhook-idempotent, REC-ledger |
| BO-05 | M10 | FR-ADM-01..06 | — | — | IT-admin-audit |
| — | M01 | FR-AUTH-01..10 | UC-01.01, UC-01.02 | seq-dang-nhap-sso | E2E-sso-login-logout (SSO test env), IT-id-token-validation, IT-backchannel-logout |

## 5. Rủi ro triển khai & giảm thiểu

| Rủi ro | Giai đoạn | Biện pháp |
|---|---|---|
| Provider ảnh không giữ được nhân vật | P0 | PoC trên golden set; tiêu chí chấp nhận BO-02 trước khi khóa lựa chọn |
| TTS tiếng Việt đọc sai tên riêng, từ Hán Việt, số | P0–P2 | PoC đo WER; từ điển phát âm; chọn provider có SSML phoneme |
| Aligner tiếng Việt kém chính xác làm lệch phụ đề | P2 | Dùng timestamp của TTS khi có; fallback aligner; test lệch ≤ 100 ms |
| Render chậm với video dài | P3 | Render theo đoạn song song; NVENC; 720p nháp |
| LLM chọn ranh giới shot kém (cắt giữa ý) | P1 | Prompt có quy tắc ranh giới đoạn văn; người dùng dời ranh giới; validator snap về câu |
| Ledger sai lệch | P1 | Reconciler hằng ngày; test property-based cho hold/capture/release |
| LLM trả JSON sai schema | P1 | Structured output + validate + retry có phản hồi lỗi; tối đa 2 lần |
| Văn bản dài vượt context | P1 | Xử lý theo chương, tóm tắt cuốn chiếu, cache prompt |

## 6. Câu hỏi mở cho Product Owner

1. Thao tác LLM (storyboard, phân tích) miễn phí kèm rate limit hay tính credit nhỏ?
2. Gói Free có được render video không (đề xuất: 720p có watermark)?
3. Credit dùng trong dự án chung: trừ ví người bấm (đề xuất hiện tại) hay ví Owner?
4. Có cần chế độ cộng tác thời gian thực (cùng gõ, như Google Docs) ở giai đoạn sau không?
5. Ngôn ngữ thuyết minh bắt buộc lúc ra mắt: tiếng Việt và tiếng Anh, hay nhiều hơn?
6. Tiêu đề chương có được đọc trong video không (mặc định: không, chỉ hiện clip tiêu đề)?
7. Lời thoại trong ngoặc kép: một giọng kể duy nhất (MVP) hay đa giọng theo nhân vật?
8. Ngưỡng WER mặc định 3% có phù hợp, hay cần 0% kèm duyệt tay mọi lệch?
9. Ký hiệu trình bày trong truyện (vd. tin nhắn dạng `*Bố* [ … ]`) đọc thế nào: đọc tên người gửi hay chỉ đọc nội dung? (Vẫn không đổi chữ, chỉ là quy tắc phát âm.)
10. **SSO có sẵn:** đó là SSO nào, chuẩn gì (OIDC / OAuth 2.0 / SAML / CAS)? Có `end_session_endpoint` và back-channel logout không? Claims nào có sẵn (`email`, `name`, `picture`, `locale`, `roles`)? Có môi trường test và quy trình cấp `client_id` cho ứng dụng mới không? Có webhook/SCIM báo tài khoản bị khóa hay xóa không?
11. **Thư viện nhạc & SFX:** dùng nguồn nào (mua license gói thư viện như Epidemic Sound / Artlist, nguồn miễn phí CC0 như Freesound/Pixabay, hay tự xây)? Có cho người dùng tải nhạc riêng lên không (rủi ro bản quyền khi đăng mạng xã hội)?
